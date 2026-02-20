import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import shapefile


INPUT_DIR = Path("Data/openelections")
OUTPUT_PATH = Path("Data/md_county_aggregated_results_1986_2024.json")
COUNTY_SHP_PATH = Path("Data/tl_2020_24_county20/tl_2020_24_county20.shp")

# Keep this to clean statewide-style geographic patterns.
CONTEST_FILTER = {
    "President": {"contest_type": "Federal", "office_rank": 1},
    "Governor": {"contest_type": "State", "office_rank": 2},
    "U.S. Senator": {"contest_type": "Federal", "office_rank": 3},
    "Attorney General": {"contest_type": "State", "office_rank": 4},
    "Comptroller": {"contest_type": "State", "office_rank": 5},
}

PARTY_MAP = {
    "democratic": "DEM",
    "republican": "REP",
    "libertarian": "LIB",
    "independent": "IND",
    "reform": "REF",
    "green": "GRN",
    "alliance": "ALL",
    "taxpayers": "TAX",
    "natural-law": "NAT",
    "other": "OTH",
    "both parties": "BTH",
}


def normalize_contest_name(office: str) -> str:
    office = office.strip()
    if office.startswith("Comptroller"):
        return "Comptroller"
    return office


def normalize_party(party: str) -> str:
    p = (party or "").strip().lower()
    if p in PARTY_MAP:
        return PARTY_MAP[p]
    if not p:
        return "OTH"
    return p.upper()


def remove_running_mate(name: str) -> str:
    candidate = (name or "").strip()
    if not candidate:
        return candidate
    if "/" in candidate:
        return candidate.split("/", 1)[0].strip()
    if " and " in candidate.lower():
        parts = candidate.split(" and ", 1)
        if len(parts) == 2:
            return parts[0].strip()
    return candidate


def _norm(s: str) -> str:
    return " ".join((s or "").replace("`", "'").strip().lower().split())


def load_namelsad20_lookup() -> dict:
    reader = shapefile.Reader(str(COUNTY_SHP_PATH))
    fields = [f[0] for f in reader.fields[1:]]
    i_state = fields.index("STATEFP20")
    i_name = fields.index("NAME20")
    i_namelsad = fields.index("NAMELSAD20")

    by_name = defaultdict(list)
    for rec in reader.iterRecords():
        if rec[i_state] != "24":
            continue
        by_name[_norm(rec[i_name])].append(rec[i_namelsad])
    return by_name


def to_namelsad20(county: str, by_name: dict) -> str:
    raw = county.strip().replace("`", "'")
    nraw = _norm(raw)

    if nraw == "baltimore city":
        baltimore = by_name.get("baltimore", [])
        city_name = next((x for x in baltimore if " city" in x.lower()), None)
        if city_name:
            return city_name

    base = nraw
    if base.endswith(" county"):
        base = base[:-7].strip()
    elif base.endswith(" city"):
        base = base[:-5].strip()

    candidates = by_name.get(base, [])
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        if "city" in nraw:
            city_name = next((x for x in candidates if " city" in x.lower()), None)
            if city_name:
                return city_name
        county_name = next((x for x in candidates if " county" in x.lower()), None)
        if county_name:
            return county_name
        return candidates[0]

    # Fallback if county not found in lookup.
    if raw.lower().endswith(" county") or raw.lower().endswith(" city"):
        return raw
    return f"{raw} County"


def competitiveness(margin_pct: float, winner: str) -> dict:
    """
    Mirror the refined index criteria exactly:
    - Use rounded margin (already rounded before calling this).
    - Tossup is always neutral (<0.50%), regardless of winner.
    """
    if winner == "TIE" or margin_pct < 0.5:
        return {
            "category": "Tossup",
            "party": "Tossup",
            "code": "TOSSUP",
            "color": "#f7f7f7",
            "label": "Tossup (<0.50%)",
        }

    party = "Republican" if winner == "REP" else "Democratic"
    prefix = "R" if winner == "REP" else "D"

    if margin_pct >= 40:
        return {
            "category": "Annihilation",
            "party": party,
            "code": f"{prefix}_ANNIHILATION",
            "color": "#67000d" if winner == "REP" else "#08306b",
            "label": f"Annihilation {party} (>=40.00%)",
        }
    if margin_pct >= 30:
        return {
            "category": "Dominant",
            "party": party,
            "code": f"{prefix}_DOMINANT",
            "color": "#a50f15" if winner == "REP" else "#08519c",
            "label": f"Dominant {party} (30.00-39.99%)",
        }
    if margin_pct >= 20:
        return {
            "category": "Stronghold",
            "party": party,
            "code": f"{prefix}_STRONGHOLD",
            "color": "#cb181d" if winner == "REP" else "#3182bd",
            "label": f"Stronghold {party} (20.00-29.99%)",
        }
    if margin_pct >= 10:
        return {
            "category": "Safe",
            "party": party,
            "code": f"{prefix}_SAFE",
            "color": "#ef3b2c" if winner == "REP" else "#6baed6",
            "label": f"Safe {party} (10.00-19.99%)",
        }
    if margin_pct >= 5.5:
        return {
            "category": "Likely",
            "party": party,
            "code": f"{prefix}_LIKELY",
            "color": "#fb6a4a" if winner == "REP" else "#9ecae1",
            "label": f"Likely {party} (5.50-9.99%)",
        }
    if margin_pct >= 1:
        return {
            "category": "Lean",
            "party": party,
            "code": f"{prefix}_LEAN",
            "color": "#fcae91" if winner == "REP" else "#c6dbef",
            "label": f"Lean {party} (1.00-5.49%)",
        }
    return {
        "category": "Tilt",
        "party": party,
        "code": f"{prefix}_TILT",
        "color": "#fee8c8" if winner == "REP" else "#e1f5fe",
        "label": f"Tilt {party} (0.50-0.99%)",
    }


def build() -> dict:
    files = sorted(INPUT_DIR.glob("*__md__general__county.csv"))
    namelsad_lookup = load_namelsad20_lookup()

    # year -> contest -> county -> party -> candidate votes
    tally = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        )
    )

    years_seen = set()
    contests_seen = set()

    for path in files:
        year = path.name[:4]
        try:
            year_int = int(year)
        except ValueError:
            continue
        years_seen.add(year)
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contest = normalize_contest_name((row.get("office") or "").strip())
                if contest not in CONTEST_FILTER:
                    continue

                county = to_namelsad20((row.get("county") or "").strip(), namelsad_lookup)
                party_code = normalize_party(row.get("party") or "")
                candidate = remove_running_mate((row.get("candidate") or "").strip()) or "Unknown"

                try:
                    votes = int((row.get("votes") or "0").strip())
                except ValueError:
                    votes = 0

                tally[year][contest][county][party_code][candidate] += votes
                contests_seen.add(contest)

    results_by_year = {}
    total_county_results = 0

    for year in sorted(tally.keys()):
        results_by_year[year] = {}
        for contest in sorted(tally[year].keys()):
            results_by_year[year][contest] = {}
            for county in sorted(tally[year][contest].keys()):
                by_party = tally[year][contest][county]
                party_totals = {p: sum(cands.values()) for p, cands in by_party.items()}

                dem_votes = party_totals.get("DEM", 0)
                rep_votes = party_totals.get("REP", 0)
                total_votes = sum(party_totals.values())
                two_party_total = dem_votes + rep_votes
                other_votes = total_votes - two_party_total

                dem_candidate = ""
                rep_candidate = ""
                if "DEM" in by_party and by_party["DEM"]:
                    dem_candidate = Counter(by_party["DEM"]).most_common(1)[0][0]
                if "REP" in by_party and by_party["REP"]:
                    rep_candidate = Counter(by_party["REP"]).most_common(1)[0][0]

                margin = abs(dem_votes - rep_votes)
                if total_votes > 0:
                    margin_pct = round((margin / total_votes) * 100, 2)
                else:
                    margin_pct = 0.0

                if dem_votes > rep_votes:
                    winner = "DEM"
                elif rep_votes > dem_votes:
                    winner = "REP"
                else:
                    winner = "TIE"

                if total_votes > 0:
                    dem_pct = round((dem_votes / total_votes) * 100, 2)
                    rep_pct = round((rep_votes / total_votes) * 100, 2)
                else:
                    dem_pct = 0.0
                    rep_pct = 0.0

                results_by_year[year][contest][county] = {
                    "county": county,
                    "contest": contest,
                    "contest_type": CONTEST_FILTER[contest]["contest_type"],
                    "office_rank": CONTEST_FILTER[contest]["office_rank"],
                    "year": year,
                    "dem_candidate": dem_candidate,
                    "rep_candidate": rep_candidate,
                    "dem_votes": dem_votes,
                    "rep_votes": rep_votes,
                    "dem_pct": dem_pct,
                    "rep_pct": rep_pct,
                    "other_votes": other_votes,
                    "total_votes": total_votes,
                    "two_party_total": two_party_total,
                    "margin": margin,
                    "margin_pct": f"{margin_pct:.2f}",
                    "winner": winner,
                    "competitiveness": competitiveness(margin_pct, winner),
                    "all_parties": party_totals,
                }
                total_county_results += 1

    payload = {
        "focus": "Maryland county-level political realignment patterns",
        "jurisdiction": {
            "state": "Maryland",
            "state_fips": "24",
            "geography_level": "County and county-equivalent",
        },
        "processed_date": str(date.today()),
        "categorization_system": {
            "competitiveness_scale": {
                "Republican": [
                    {"category": "Annihilation", "range": "R+40%+", "color": "#67000d"},
                    {"category": "Dominant", "range": "R+30.00-39.99%", "color": "#a50f15"},
                    {"category": "Stronghold", "range": "R+20.00-29.99%", "color": "#cb181d"},
                    {"category": "Safe", "range": "R+10.00-19.99%", "color": "#ef3b2c"},
                    {"category": "Likely", "range": "R+5.50-9.99%", "color": "#fb6a4a"},
                    {"category": "Lean", "range": "R+1.00-5.49%", "color": "#fcae91"},
                    {"category": "Tilt", "range": "R+0.50-0.99%", "color": "#fee8c8"},
                ],
                "Tossup": [
                    {"category": "Tossup", "range": "<0.50%", "color": "#f7f7f7"},
                ],
                "Democratic": [
                    {"category": "Tilt", "range": "D+0.50-0.99%", "color": "#e1f5fe"},
                    {"category": "Lean", "range": "D+1.00-5.49%", "color": "#c6dbef"},
                    {"category": "Likely", "range": "D+5.50-9.99%", "color": "#9ecae1"},
                    {"category": "Safe", "range": "D+10.00-19.99%", "color": "#6baed6"},
                    {"category": "Stronghold", "range": "D+20.00-29.99%", "color": "#3182bd"},
                    {"category": "Dominant", "range": "D+30.00-39.99%", "color": "#08519c"},
                    {"category": "Annihilation", "range": "D+40%+", "color": "#08306b"},
                ],
            },
            "office_types": ["Federal", "State", "Judicial", "Other"],
            "enhanced_features": [
                "Maryland county-level competitiveness categorization for each contest",
                "Maryland-specific contest type classification (Federal/State/Judicial)",
                "Office ranking system tuned for statewide Maryland analysis",
                "Color coding aligned to Maryland county political geography visualization",
            ],
        },
        "summary": {
            "total_years": len(years_seen),
            "total_contests": len(contests_seen),
            "total_county_results": total_county_results,
            "years_covered": sorted(years_seen),
        },
        "results_by_year": results_by_year,
    }
    return payload


def main() -> None:
    payload = build()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    print(
        "Summary:",
        payload["summary"]["total_years"],
        "years,",
        payload["summary"]["total_contests"],
        "contests,",
        payload["summary"]["total_county_results"],
        "county results",
    )


if __name__ == "__main__":
    main()

