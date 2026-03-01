# MDRealignment

Interactive Maryland county-level electoral realignment map and data pipeline covering general elections from 1986 to 2024. The project visualizes how Maryland's political geography has shifted across five statewide contest types over 16 election cycles, with per-county competitiveness ratings, candidate margins, and a sidebar of 10 data-grounded research findings.

**At its core, this project asks a single question:** how did Maryland go from a state where Republicans could plausibly win statewide in 1994 — Sauerbrey lost by fewer than 6,000 votes — to one where the best Republican candidate the party could produce (Hogan, 2024 Senate) lost by 12 points? The answer is in the county-level data, and this project makes it navigable, visual, and analytically rigorous.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Political Science Context](#political-science-context)
3. [Repository Structure](#repository-structure)
4. [Local Setup](#local-setup)
5. [Data Pipeline](#data-pipeline)
   - [Step 1 — Raw File Conversion](#step-1--convert-raw-files-to-openelections-style-csvs)
   - [Input Format Detection](#input-format-detection)
   - [Step 2 — Aggregation and JSON Build](#step-2--build-the-aggregated-county-results-json)
6. [Aggregated JSON Structure](#aggregated-json-structure)
7. [Competitiveness Scale](#competitiveness-scale)
8. [Contests and Years Covered](#contests-and-years-covered)
9. [Technical Architecture](#technical-architecture)
   - [Frontend Stack](#frontend-stack)
   - [Color Assignment](#color-assignment)
   - [Design Decisions](#design-decisions)
   - [Finding Cards CSS Classes](#finding-cards-css-classes)
10. [Map Features](#map-features)
11. [Adding a New Election Year](#adding-a-new-election-year)
12. [How to Query the Data](#how-to-query-the-data)
13. [Research Findings Summary](#research-findings-summary)
14. [Statewide Results Reference](#statewide-results-reference)
15. [Complete County Snapshots](#complete-county-snapshots)
16. [Key Dataset Records](#key-dataset-records)
17. [Known Limitations](#known-limitations)
18. [Data Sources and Notes](#data-sources-and-notes)

---

## Project Overview

MDRealignment tracks the transformation of Maryland's electoral map from a genuinely competitive state in the late 1980s — where Republicans could win statewide races — into one of the most structurally Democratic states in the country by 2024. The map allows users to explore how individual counties moved across contest types and election cycles, and the sidebar analysis panel synthesizes that data into 10 detailed research findings covering suburban realignment, the DC transplant effect, Western Maryland Republican consolidation, the candidate effect (Hogan, Alsobrooks), and the emergence of PG County as the foundation of modern Democratic statewide dominance.

The analytical thesis driving the project:

- **1986 baseline:** William Donald Schaefer (D) won every single Maryland county, including Carroll (D+58.49%), Harford (D+67.49%), and Garrett. The New Deal coalition was still intact.
- **1994 peak Republican threat:** Ellen Sauerbrey lost the governorship by fewer than 6,000 votes. The suburban counties not yet realigned — Howard, Frederick, Anne Arundel, Baltimore County — gave her the margins to nearly win.
- **2002–2018 split-ticket era:** Republicans could still win the governorship (Ehrlich 2002, Hogan 2014 and 2018) by running maximally crossover-capable candidates in low-turnout mid-term environments, even as presidential margins tilted Democratic by 20+ points per cycle.
- **2020–2024 structural lock:** Biden won the state 65.81% to 31.72% presidentially. Moore won the governorship 64.53% to 32.12%. Alsobrooks won the Senate 54.64% to 42.84% against Hogan himself — the best the Republican Party had. The suburban realignment is complete and irreversible.

---

## Political Science Context

### What "Realignment" Means in This Project

"Realignment" in American political science has two distinct meanings that are often conflated:

- **Critical realignment theory** (V.O. Key, 1955) — a sudden, durable shift in partisan coalitions, typically triggered by a crisis, producing a new majority that persists for a generation (the New Deal realignment of 1932 is the canonical example)
- **Secular realignment** — a slower, sustained directional drift driven by demographic and socioeconomic change rather than crisis events, accumulating over multiple election cycles without a single dramatic pivot point

Maryland's transformation is the latter type. There is no single year or event that "flipped" Maryland. The presidential trend moved in one direction continuously from 1988 to 2020 across every cycle. The gubernatorial trend followed on a lag, with Republican candidates winning by running against the national party's image rather than with it. The realignment was secular, structural, and demographic — not event-driven.

### Sorting vs. Conversion

A second key distinction: realignment can happen through **conversion** (existing voters changing parties) or **sorting** (the composition of an area changing as different types of voters move in or out). Both mechanisms operated in Maryland, but in different counties:

- **Sorting-dominant counties:** Charles County, Montgomery County, and to some extent Prince George's are primarily reshaped by in-migration of Democratic-leaning households from DC and inner suburbs. Very few individual voters "converted" — the electorate composition simply changed.
- **Conversion-dominant counties:** Carroll County, Harford County, and Western Maryland counties show the national partisan sorting of white rural and working-class voters who shifted Republican over the Reagan and post-Reagan era without large population replacement. These voters were always there; their party identity shifted.
- **Mixed (Baltimore County, Howard County):** Both sorting (professional in-migration from DC corridor and Baltimore) and conversion (college-educated suburbanites who began voting more Democratic after 2016) operated simultaneously.

The map makes this distinction visible: sorting-heavy counties show fast discontinuous transitions (Charles shifts dramatically between cycles as demographic composition tips); conversion-heavy counties show slower but ultimately complete repositioning (Harford and Carroll drift steadily Republican over 30+ years).

### Why Maryland Is an Analytically Ideal Case Study

Maryland is unusually well-suited for studying suburban realignment for several reasons:

1. **The DC gravity well is unique.** No other major American city exerts the same sustained professional-class economic pull on adjacent suburbs across such a wide geographic radius. DC's concentration of federal employment, defense contracting, international organizations, and professional services creates a distinctive migration attractor that has no close peer in other states.

2. **Deep pre-realignment electoral heterogeneity.** Maryland had genuine geographic diversity in 1986: Democratic dominance in Baltimore City and PG County, competitive near-tossup margins in Montgomery, and solid Republican performance in the suburbs and rural areas. This dynamic baseline makes the 2024 map's uniformity all the more analytically striking.

3. **The full split-ticket era is documented.** Most realignment datasets lose resolution because they don't capture the gubernatorial race independently from presidential years. The 16-cycle gubernatorial dataset here, covering 1986–2022, preserves the complete arc of when and how different counties stopped splitting their tickets.

4. **A natural controlled experiment exists.** Harford and Baltimore County are demographically similar — both working-class and middle-class suburban, both with significant commuter populations, both without major federal institutional employers. Yet their gubernatorial arcs diverge sharply after 2018 when Hogan's brand of Republicanism becomes unavailable: Baltimore County collapses 58 points in one cycle while Harford holds Republican by R+8.46%. This divergence isolates the role of specific geographic and economic differences even within seemingly similar suburban types.

---

## Repository Structure

```
MDRealignment/
│
├── index.html                                        # Entire application in a single file:
│                                                     # Mapbox GL JS map, sidebar analysis panel,
│                                                     # contest selector, year slider, county click
│                                                     # panel, statewide summary, legend, all inline
│                                                     # CSS and JavaScript (~4000 lines)
│
├── README.md                                         # This file
│
├── Data/
│   │
│   ├── md_county_aggregated_results_1986_2024.json   # PRIMARY DATA SOURCE for the map.
│   │                                                 # ~33,000 lines; 16 years × up to 5 contests
│   │                                                 # × 24 counties = 1,035 county results.
│   │                                                 # Regenerated by build script (Step 2).
│   │
│   ├── geo/
│   │   └── md_counties_2020.geojson                  # County boundary polygons (2020 Census).
│   │                                                 # Used by Mapbox GL JS for choropleth layer.
│   │                                                 # Includes NAMELSAD20 property that matches
│   │                                                 # the aggregated JSON county keys exactly.
│   │
│   ├── tl_2020_24_county20/                          # Census TIGER/Line shapefile for Maryland
│   │   ├── tl_2020_24_county20.shp                   # (FIPS 24). Used by build script (Step 2)
│   │   ├── tl_2020_24_county20.dbf                   # to resolve county name strings against
│   │   ├── tl_2020_24_county20.shx                   # canonical NAMELSAD20 identifiers,
│   │   ├── tl_2020_24_county20.prj                   # disambiguating "Baltimore County" from
│   │   ├── tl_2020_24_county20.cpg                   # "Baltimore City". Not served to the browser.
│   │   ├── tl_2020_24_county20.shp.iso.xml
│   │   └── tl_2020_24_county20.shp.ea.iso.xml
│   │
│   ├── openelections/                                # Normalized per-election county CSVs.
│   │   ├── 19861104__md__general__county.csv         # Named by OpenElections convention:
│   │   ├── 19881108__md__general__county.csv         # YYYYMMDD__md__general__county.csv
│   │   ├── 19901106__md__general__county.csv         # Generated by convert script (Step 1).
│   │   ├── 19921103__md__general__county.csv         # Columns: county, precinct, office,
│   │   ├── 19941108__md__general__county.csv         # district, party, candidate, votes, winner
│   │   ├── 19961105__md__general__county.csv
│   │   ├── 19981103__md__general__county.csv
│   │   ├── 20001107__md__general__county.csv
│   │   ├── 20021105__md__general__county.csv
│   │   ├── 20121106__md__general__county.csv
│   │   ├── 20141104__md__general__county.csv
│   │   ├── 20161108__md__general__county.csv
│   │   ├── 20181106__md__general__county.csv
│   │   ├── 20201103__md__general__county.csv
│   │   ├── 20221108__md__general__county.csv
│   │   └── 20241105__md__general__county.csv
│   │
│   ├── 1986 General Election.csv                     # Raw source election files as downloaded
│   ├── 1988 General Election.csv                     # from Maryland SBE. Format varies by year:
│   ├── 1990 General Election.csv                     # legacy matrix-style CSV (1986–2000, 2012+),
│   ├── 1992 General Election.csv                     # pipe-delimited TXT (2002), or modern
│   ├── 1994 General Election.csv                     # precinct-level CSV with "Candidate Name"
│   ├── 1996 General Election.csv                     # and "Office Name" columns (2014+).
│   ├── 1998 General Election.csv                     # The convert script auto-detects format.
│   ├── 2000 General Election.csv
│   ├── 2002 General Election.txt                     # Pipe-delimited (|) format; only .txt file
│   ├── 2012 General Election.csv
│   ├── 2014 General Election.csv
│   ├── 2016 General Election.csv
│   ├── 2018 General Election.csv
│   ├── 2020 General Election.csv
│   ├── 2022 General Election.csv
│   └── 2024 General Election.csv
│
└── Scripts/
    ├── convert_to_openelections.py                   # Step 1: normalize raw files → openelections/
    └── build_md_county_aggregated_results.py         # Step 2: aggregate → aggregated JSON
```

---

## Local Setup

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.11+ | f-strings, `match` syntax not used; 3.9+ likely fine |
| pyshp | any recent | `pip install pyshp` — used to read TIGER shapefile |
| Mapbox account | — | Free tier sufficient; public token only |
| Static file server | — | Required for JSON/GeoJSON fetches; `file://` blocked by CORS |

```bash
pip install pyshp
```

### Steps

1. **Set your Mapbox public token** in `index.html`:
   ```js
   // Near the top of the <script> block:
   const CONFIG = {
     mapboxToken: 'pk.your_token_here',
     ...
   };
   ```
   The token must be a **public** (`pk.`) token. Mapbox secret tokens (`sk.`) will not work in browser JS.

2. **Start a local static server** from the project root — required because `fetch()` calls to the JSON and GeoJSON files are blocked by browsers under `file://` CORS policy:
   ```bash
   # Python (built-in, no install needed)
   python -m http.server 8080

   # Node.js (via npx, no global install needed)
   npx serve .

   # VS Code Live Server extension
   # Right-click index.html → "Open with Live Server"
   ```

3. Open `http://localhost:8080` (or the port your server chose) in a browser.

### What You Do NOT Need to Do

The aggregated JSON (`Data/md_county_aggregated_results_1986_2024.json`) and GeoJSON (`Data/geo/md_counties_2020.geojson`) are already committed to the repository and ready to use. You only need to re-run the pipeline scripts if you are:
- Adding a new election year's data
- Fixing a source data error in a raw election file
- Changing the competitiveness scale thresholds
- Adding a new contest type

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Map doesn't load / blank screen | Invalid or missing Mapbox token | Replace `CONFIG.mapboxToken` with a valid `pk.` token |
| Counties are gray / no data visible | JSON fetch failed (CORS) | Make sure you're serving via a local HTTP server, not `file://` |
| Counties don't match GeoJSON features | County name mismatch | Re-run Step 2 (build script) to regenerate aggregated JSON |
| `ModuleNotFoundError: shapefile` | pyshp not installed | `pip install pyshp` |
| `UnicodeDecodeError` on a source CSV | Encoding issue in raw file | The convert script tries `utf-8-sig`, `cp1252`, and `latin-1` automatically |

---

## Data Pipeline

The pipeline runs in two sequential, independent steps. Both scripts are run from the project root directory.

### Step 1 — Convert raw files to OpenElections-style CSVs

```bash
python Scripts/convert_to_openelections.py
```

Optional arguments:
```
--data-dir    Path to directory containing raw election files  [default: Data]
--output-dir  Path for converted OpenElections CSVs           [default: Data/openelections]
```

The script scans `Data/` for files matching the pattern `YYYY General Election.(csv|txt)`, auto-detects the file format, converts each file to a standardized county-level CSV, and writes it to `Data/openelections/` with the OpenElections naming convention.

#### Input Format Detection

The raw election files come in three distinct formats depending on the year. The script detects and handles all three automatically:

**Format 1 — Legacy matrix-style CSV** (most years, 1986–2000 and some 2012+)

The source file uses a two-row header structure where the first row identifies the office (e.g., `"President and Vice President of the United States - Vote For One Pair"`) and the second row lists candidates with party designations embedded in parentheses. Subsequent rows are county × votes matrices.

Example header pattern:
```
"President and Vice President of the United States - Vote For One Pair",,,,,,
,"George Bush (Republican) Winner","Bill Clinton (Democratic)","Ross Perot (Reform)",...
"Allegany",7234,4892,1021,...
```

Parser behavior: office name extracted from the first non-empty cell, candidates parsed by splitting on parentheses for party extraction, county names extracted from the first column of each data row.

**Format 2 — Pipe-delimited TXT** (2002 only — `2002 General Election.txt`)

Each row is a flat record with 10+ fields separated by `|`:

```
office_raw|?|county|last|middle|first|party|winner_flag|?|votes|...
```

Field positions are fixed: `parts[0]` = office, `parts[2]` = county, `parts[3]` = last name, `parts[4]` = middle, `parts[5]` = first name, `parts[6]` = party, `parts[7]` = winner flag (1/0), `parts[9]` = votes. Candidate names are assembled as `first + middle + last`, stripping `\N` null markers. The special case `zz998` (Other Write-Ins placeholder) is normalized to `"Other Write-Ins"`.

**Format 3 — Modern precinct-level CSV** (2014+)

Newer SBE files use a wide-format CSV with explicit column headers including `"Candidate Name"`, `"Office Name"`, `"Party"`, `"County Name"`, and multiple `"*Votes"` columns. Detection: if the CSV header contains both `"Candidate Name"` and `"Office Name"`, the file is treated as modern format.

Vote totals are aggregated across all `"*Votes"` columns (excluding `"Against"` vote columns for judicial retention races). The county is resolved from `"County Name"` column first, falling back to the `"County"` code column if blank.

#### What All Three Parsers Do in Common

- **Office normalization:** Long canonical names mapped to short forms (`"President and Vice President of the United States"` → `"President"`, `"Governor / Lt. Governor"` → `"Governor"`)
- **Running mate removal:** Candidate names containing `/` or ` and ` are split; only the first-listed name is retained (`"Biden/Harris"` → `"Biden"`)
- **County name normalization:** `" County"` suffix stripped for internal matching; apostrophe variants fixed (`Prince George\`s` → `Prince George's`); `" City"` suffix cased consistently
- **Encoding fallback:** Files tried in order `utf-8-sig` → `cp1252` → `latin-1` before raising

### Step 2 — Build the aggregated county results JSON

```bash
python Scripts/build_md_county_aggregated_results.py
```

Reads all 16 CSVs from `Data/openelections/`, applies the contest filter, resolves county names to canonical Census identifiers, computes margins and competitiveness ratings, and writes `Data/md_county_aggregated_results_1986_2024.json`.

#### County Name Resolution

County names in the normalized CSVs are matched against the Census TIGER/Line shapefile (`tl_2020_24_county20.shp`) using the `NAMELSAD20` field. This is critical for the `"Baltimore"` disambiguation: the shapefile lookup explicitly prefers the record containing `" city"` in its `NAMELSAD20` value when the input is `"Baltimore City"`, and the record containing `" county"` when the input is `"Baltimore"` or `"Baltimore County"`. Unmatched names fall back to appending `" County"` to the raw name.

#### Margin and Competitiveness Calculation

For each county × contest × year result:

1. **Party totals** — votes summed across all candidate records per party code
2. **Two-party margin** — `|dem_votes − rep_votes|`
3. **Margin percent** — `margin / total_votes × 100`, rounded to 2 decimal places (note: denominator is **total votes**, not two-party total — see [Known Limitations](#known-limitations))
4. **Winner** — `"DEM"` if `dem_votes > rep_votes`, `"REP"` if `rep_votes > dem_votes`, `"TIE"` if equal
5. **Competitiveness rating** — look up the margin percent in the 8-tier scale (see [Competitiveness Scale](#competitiveness-scale))

The five tracked contests are filtered by office name match; all other offices (judicial, local, ballot measures) are silently dropped.

#### Office Priority / Ranking

| `office_rank` | Contest | `contest_type` |
|---|---|---|
| 1 | President | Federal |
| 2 | Governor | State |
| 3 | U.S. Senator | Federal |
| 4 | Attorney General | State |
| 5 | Comptroller | State |

The `office_rank` field is embedded in every county result and used by the map's contest selector to order the dropdown options.

---

## Aggregated JSON Structure

The JSON file has three top-level sections beyond the metadata: `categorization_system`, `summary`, and `results_by_year`.

### Top-level metadata

```jsonc
{
  "focus": "Maryland county-level political realignment patterns",
  "jurisdiction": {
    "state": "Maryland",
    "state_fips": "24",
    "geography_level": "County and county-equivalent"
  },
  "processed_date": "YYYY-MM-DD",   // date build script was last run
  "categorization_system": { ... }, // full competitiveness scale definitions embedded here
  "summary": {
    "total_years": 16,
    "total_contests": 5,
    "total_county_results": 1035,
    "years_covered": ["1986", "1988", "1990", ..., "2024"]
  },
  "results_by_year": { ... }
}
```

### `results_by_year` nested path

```
results_by_year
  └── [year string, e.g. "2020"]
        └── [contest name, e.g. "President"]
              └── [county NAMELSAD20, e.g. "Howard County"]
                    └── { county result object }
```

### County result object — all fields

```jsonc
{
  "county":         "Howard County",      // NAMELSAD20 canonical name
  "contest":        "President",          // one of the 5 tracked contests
  "contest_type":   "Federal",            // "Federal" or "State"
  "office_rank":    1,                    // 1–5, see priority table above
  "year":           "2020",               // string, 4-digit year
  "dem_candidate":  "Joseph R. Biden",    // running mate removed; first-listed candidate
  "rep_candidate":  "Donald J. Trump",    // running mate removed
  "dem_votes":      95184,                // raw integer vote total for DEM party
  "rep_votes":      33462,                // raw integer vote total for REP party
  "dem_pct":        72.73,                // dem_votes / total_votes × 100 (NOT two-party share)
  "rep_pct":        25.55,                // rep_votes / total_votes × 100 (NOT two-party share)
  "other_votes":    2224,                 // total_votes − dem_votes − rep_votes
  "total_votes":    130870,               // all votes cast across all parties
  "two_party_total":128646,              // dem_votes + rep_votes only
  "margin":         61722,               // |dem_votes − rep_votes| in raw votes
  "margin_pct":     "47.16",             // "margin / total_votes × 100", stored as STRING
  "winner":         "DEM",               // "DEM", "REP", or "TIE"
  "competitiveness": {
    "category":     "Annihilation",      // human-readable tier name
    "party":        "Democratic",        // "Democratic", "Republican", or "Tossup"
    "code":         "D_ANNIHILATION",    // programmatic code used by map color logic
    "color":        "#08306b",           // hex color for choropleth fill
    "label":        "Annihilation Democratic (>=40.00%)"
  },
  "all_parties": {                       // raw votes for ALL parties present
    "DEM": 95184,
    "REP": 33462,
    "LIB": 2224
  }
}
```

### Important field quirks

| Field | Quirk |
|---|---|
| `margin_pct` | Stored as a **string** (e.g. `"47.16"`), not a number. Parse with `parseFloat()` in JavaScript. |
| `dem_pct` / `rep_pct` | **Total vote share**, not two-party share. A candidate with 50% of votes in a race with a 5% Libertarian gets `dem_pct: 50.0`, not `dem_pct: 52.6`. |
| `dem_candidate` / `rep_candidate` | Empty string `""` if no candidate of that party ran in a given county/year. Check before display. |
| `all_parties` | Keys are normalized party codes (`DEM`, `REP`, `LIB`, `GRN`, `IND`, `REF`, `OTH`, etc.). Aggregated across all candidates of that party. |
| `two_party_total` | Useful for computing true two-party vote share: `dem_votes / two_party_total × 100`. |

---

## Competitiveness Scale

Margins are calculated as `|dem_votes − rep_votes| / total_votes × 100`. The scale is mirrored exactly between the build script and the map legend.

| Category | Margin Range | Dem Hex | Rep Hex | Notes |
|---|---|---|---|---|
| **Tossup** | < 0.50% | `#f7f7f7` | `#f7f7f7` | Always neutral regardless of leader |
| **Tilt** | 0.50 – 0.99% | `#e1f5fe` | `#fee8c8` | Near-tossup; very light shade |
| **Lean** | 1.00 – 5.49% | `#c6dbef` | `#fcae91` | Competitive; either party could win |
| **Likely** | 5.50 – 9.99% | `#9ecae1` | `#fb6a4a` | Moderate advantage |
| **Safe** | 10.00 – 19.99% | `#6baed6` | `#ef3b2c` | Clear advantage; upset unlikely |
| **Stronghold** | 20.00 – 29.99% | `#3182bd` | `#cb181d` | Dominant; rarely contested |
| **Dominant** | 30.00 – 39.99% | `#08519c` | `#a50f15` | Structural majority |
| **Annihilation** | ≥ 40.00% | `#08306b` | `#67000d` | Landslide; opposing party uncompetitive |

The color ramps are based on ColorBrewer sequential single-hue palettes (blue for Democratic, red for Republican), ensuring perceptual linearity from light (competitive) to dark (dominant).

The `competitiveness.code` field programmatic values follow the pattern `{D|R}_{CATEGORY}` (e.g., `D_ANNIHILATION`, `R_STRONGHOLD`) or `TOSSUP`. These are used directly by `index.html`'s color-assignment logic.

---

## Contests and Years Covered

### Contest types and availability

| `office_rank` | Contest | Type | When it appears |
|---|---|---|---|
| 1 | President | Federal | Presidential election years only (1988, 1992, 1996, 2000, 2012, 2016, 2020, 2024) |
| 2 | Governor | State | Gubernatorial years (1986, 1990, 1994, 1998, 2002, 2014, 2018, 2022); not every off-year cycle |
| 3 | U.S. Senator | Federal | Maryland has two Senate seats in different election classes. Class III (Mikulski → Cardin → Van Hollen): elections in 1986, 1992, 1998, 2004, 2010, 2016, 2022. Class II (Sarbanes → Mikulski → Cardin): elections in 1988, 1994, 2000, 2006, 2012, 2018, 2024. Only years present in the dataset appear in the map. |
| 4 | Attorney General | State | Appears in some years; may be absent in early cycles |
| 5 | Comptroller | State | Appears in some years; may be absent in early cycles |

> The year slider in the map automatically skips years where the selected contest type has no data. Selecting "President" while on year 1986 will jump to 1988.

### Election years included

| Year | Date | Notable races in dataset |
|---|---|---|
| 1986 | Nov 4 | Schaefer (D) gov landslide — won every county; Mikulski (D) Senate |
| 1988 | Nov 8 | Bush (R) carries Maryland presidentially; Mikulski Senate re-elect |
| 1990 | Nov 6 | Schaefer (D) re-elect governor |
| 1992 | Nov 3 | Clinton (D) presidential; Mikulski Senate by D+42.02% |
| 1994 | Nov 8 | Glendening (D) 50.22% def. Sauerbrey (R) 49.78% in governor's race — margin under 0.50%; Sarbanes (D) Senate D+18.21% same ballot |
| 1996 | Nov 5 | Clinton (D) presidential; Sarbanes Senate re-elect |
| 1998 | Nov 3 | Glendening (D) re-elect gov; Mikulski Senate by D+41.00% |
| 2000 | Nov 7 | Gore (D) presidential; Sarbanes Senate re-elect |
| 2002 | Nov 5 | Ehrlich (R) governor — first Republican gov since 1966; Mikulski Senate |
| ~~2004~~ | — | **Not included** |
| ~~2006~~ | — | **Not included** |
| ~~2008~~ | — | **Not included** |
| ~~2010~~ | — | **Not included** |
| 2012 | Nov 6 | Obama (D) presidential; Cardin (D) Senate; O'Malley (D) re-elect gov |
| 2014 | Nov 4 | Hogan (R) governor (D+4.5% loss for Brown); Van Hollen? / Mikulski Senate |
| 2016 | Nov 8 | Clinton (D) presidential; Van Hollen (D) Senate (open seat) |
| 2018 | Nov 6 | Hogan (R) governor re-elect vs. Jealous; Cardin (D) Senate re-elect |
| 2020 | Nov 3 | Biden (D) 65.81% presidential; Van Hollen (D) Senate re-elect |
| 2022 | Nov 8 | Moore (D) governor 64.53%; Cardin (D) Senate retirement/successor |
| 2024 | Nov 5 | Harris (D) presidential; Alsobrooks (D) Senate def. Hogan (R) 54.64–42.84% |

**Counties covered:** All 24 Maryland jurisdictions — 23 counties (Allegany, Anne Arundel, Baltimore, Calvert, Caroline, Carroll, Cecil, Charles, Dorchester, Frederick, Garrett, Harford, Howard, Kent, Montgomery, Prince George's, Queen Anne's, St. Mary's, Somerset, Talbot, Washington, Wicomico, Worcester) plus Baltimore City, treated as a distinct county-equivalent.

---

## Technical Architecture

### Frontend Stack

The entire application lives in a single `index.html` file with no external dependencies beyond Mapbox GL JS and its companion CSS (loaded from Mapbox CDN). There is no build system, no bundler, no framework. All CSS and JavaScript are inline within the HTML file.

| Layer | Technology | Notes |
|---|---|---|
| Map rendering | Mapbox GL JS (WebGL) | County polygon choropleth, styling by `competitiveness.code` |
| Data loading | Browser `fetch()` API | Loads `md_county_aggregated_results_1986_2024.json` and `md_counties_2020.geojson` on page init |
| UI interaction | Vanilla JavaScript | Contest selector, year slider, county click, search, sidebar minimize |
| Styling | Inline CSS | Single `<style>` block; custom CSS classes for finding cards, metric chips, legend items |
| Map data join | GeoJSON `NAMELSAD20` property | Matched against JSON keys in `results_by_year` to paint county fills |

### Color Assignment

The choropleth layer reads each county feature's `NAMELSAD20` property, looks up the corresponding county result in the loaded JSON for the current year + contest, reads `competitiveness.code`, and maps it to a Mapbox fill color expression. Counties with no data for the current year/contest are rendered in a neutral gray fallback color.

### Design Decisions

Several technical and analytical choices were made deliberately and are worth documenting:

**Single-file architecture (`index.html`)**
The entire application — map, data, styling, logic, and analysis — lives in one HTML file with zero build tooling. This was a deliberate choice for portability and simplicity: the project can be opened on any machine with a static server and a Mapbox token, with no `npm install`, no bundler, no environment setup. The single-file approach also makes the project fully self-auditable: every line of logic, every CSS rule, every data query is visible in one place without chasing imports.

**Total votes denominator, not two-party**
Margin percentages throughout the project use total votes (including third-party and independent) as the denominator, not the two-party total. This choice ensures that the competitiveness scale is consistent and comparable across cycles with very different third-party presence: 1992 (Ross Perot at 14–19% in some counties), 2000 (Nader), and 2016 (Johnson/Stein) would all look artificially more competitive on a two-party-only scale because the denominator shrinks. Using total votes keeps every cycle on the same baseline.

**2020 Census boundaries throughout**
All 16 election cycles (1986–2024) are displayed on 2020 Census county boundaries, even though county boundaries did change marginally over this period. Maryland's county borders are extremely stable — no county splits, mergers, or major annexations occurred 1986–2024 — so this introduces no material geographic distortion. The alternative (different boundaries per decade) would add complexity with no analytical payoff for a county-level analysis.

**Five contests, not all contests**
Only five statewide contest types are tracked. Maryland ballots include many other statewide and district races (Comptroller, Attorney General, congressional seats, judicial retentions, ballot questions). The five tracked contests are the ones that produce complete 24-county coverage in every relevant election year and have direct realignment-analytical value. Congressional races were excluded because district boundaries create uneven county coverage; judicial retentions were excluded because they are yes/no races with no party opposition.

**`NAMELSAD20` as the canonical county key**
The GeoJSON feature property `NAMELSAD20` (e.g., `"Baltimore County"`, `"Baltimore City"`) is used as the primary key linking the GeoJSON layer to the aggregated JSON. This was chosen over numeric FIPS codes for human readability in the JSON structure and over short names to preserve the County/City distinction in Baltimore. Every lookup in the JavaScript and Python code uses this string key.

### Finding Cards CSS Classes

The sidebar research findings use a set of custom CSS classes added to `index.html`:

| Class | Applied to | Effect |
|---|---|---|
| `.finding-card.finding-dem` | Democratic-analysis cards | Blue accent on `h5` heading |
| `.finding-card.finding-rep` | Republican-analysis cards | Red accent on `h5` heading |
| `.finding-card.finding-analysis` | Neutral/structural-analysis cards | Purple accent on `h5` heading |
| `.metric.dem-metric` | Inline stat chips | Blue pill background for Democratic margins |
| `.metric.rep-metric` | Inline stat chips | Red pill background for Republican margins |
| `.finding-subhead` | Bold subheadings within card `<p>` | 700 weight, dark gray, 13px |

---

## Map Features

### Core Navigation

- **Contest selector dropdown** — switch between the five tracked contests (President, Governor, U.S. Senator, Attorney General, Comptroller); the year slider automatically adjusts to only show years where the selected contest has data
- **Year slider** — step through all 16 election cycles; snaps to valid years only for the current contest

### County Interaction

- **Click any county** — opens a detail panel in the sidebar showing: county name, year, contest, Democratic and Republican candidates, vote totals and percentages for each party, other-party votes, total votes cast, margin in raw votes and %, and the full competitiveness rating label
- **County search** — type-ahead search field in the sidebar; filters the county list and highlights matching counties on the map; accepts partial matches

### Sidebar Analysis Panel

- **Statewide summary** — aggregated DEM and REP vote totals and percentages across all 24 jurisdictions for the current contest/year, calculated dynamically from the loaded JSON
- **Research Findings section** — 10 analytical cards (see [Research Findings Summary](#research-findings-summary)); cards are statically authored but all statistics cited are drawn from the live dataset
- **Sidebar minimize / expand** — the entire sidebar can be collapsed to maximize map view; a toggle button restores it

### Legend

- **Competitiveness scale legend** — displayed in the bottom-left corner; shows all 15 competitiveness categories (7 Democratic, 1 Tossup, 7 Republican) with their color swatches and margin ranges
- **Minimizable** — the legend can be collapsed to a header-only strip; state is retained during session

### Responsive Behavior

- On narrow viewports (mobile) the sidebar minimizes by default; the legend shifts to a bottom-sheet layout; touch targets are enlarged for slider and county click interaction

---

## Adding a New Election Year

When a new Maryland general election result file becomes available, follow this workflow:

1. **Download** the official canvass CSV from the Maryland State Board of Elections. Save it to `Data/` as `YYYY General Election.csv` (e.g., `2026 General Election.csv`).

2. **Add the election date mapping** in `Scripts/convert_to_openelections.py`:
   ```python
   YEAR_TO_ELECTION_DATE = {
       ...
       2026: "20261103",   # add actual election date
   }
   ```

3. **Run Step 1** to convert the file:
   ```bash
   python Scripts/convert_to_openelections.py
   ```
   Verify output in `Data/openelections/20261103__md__general__county.csv`.

4. **Run Step 2** to rebuild the aggregated JSON:
   ```bash
   python Scripts/build_md_county_aggregated_results.py
   ```
   The script will auto-discover the new file, add the new year to `results_by_year`, and update `summary.years_covered`.

5. **Update `index.html`** — the year slider is driven by the years present in the JSON, but you may need to:
   - Expand the slider's `max` value if it's hardcoded
   - Add the new year to any hardcoded year arrays in the contest-availability logic
   - Update the Research Findings cards if new data changes a narrative

6. **Regenerate the filename pattern** in the README years table.

---

## How to Query the Data

The aggregated JSON is designed to be queried directly without any server or database. Below are common query patterns in both JavaScript (for the browser or Node.js) and Python.

### JavaScript examples

```js
// Load the data (browser with fetch, or Node.js with require/fs)
const data = await fetch('Data/md_county_aggregated_results_1986_2024.json')
  .then(r => r.json());
const results = data.results_by_year;

// --- Get a single county result ---
const howardPres2020 = results['2020']['President']['Howard County'];
console.log(howardPres2020.dem_pct, howardPres2020.margin_pct);
// → 72.73, "44.27"

// --- All counties for a given year + contest (sorted by margin desc) ---
const gov2022 = results['2022']['Governor'];
const sorted = Object.entries(gov2022)
  .sort((a, b) => {
    const mA = parseFloat(a[1].margin_pct) * (a[1].winner === 'DEM' ? 1 : -1);
    const mB = parseFloat(b[1].margin_pct) * (b[1].winner === 'DEM' ? 1 : -1);
    return mB - mA;
  });
sorted.forEach(([county, r]) =>
  console.log(`${county}: ${r.winner === 'DEM' ? 'D' : 'R'}+${r.margin_pct}%`)
);

// --- Track a single county across all years for one contest ---
const tyears = Object.keys(results).filter(yr => results[yr]['Governor']?.['Carroll County']);
tyears.forEach(yr => {
  const r = results[yr]['Governor']['Carroll County'];
  console.log(`${yr}: ${r.winner === 'DEM' ? 'D' : 'R'}+${r.margin_pct}%`);
});

// --- Compute statewide DEM total for a contest/year ---
function statewideTotal(year, contest) {
  const counties = results[year]?.[contest];
  if (!counties) return null;
  return Object.values(counties).reduce(
    (acc, r) => ({
      dem: acc.dem + r.dem_votes,
      rep: acc.rep + r.rep_votes,
      total: acc.total + r.total_votes,
    }),
    { dem: 0, rep: 0, total: 0 }
  );
}
const sw = statewideTotal('2022', 'Governor');
console.log(`Moore: ${(sw.dem / sw.total * 100).toFixed(2)}%`);
// → 64.53%

// --- Find all counties that flipped D→R or R→D between two years ---
function flipsBeween(contest, yearA, yearB) {
  const a = results[yearA]?.[contest];
  const b = results[yearB]?.[contest];
  if (!a || !b) return [];
  return Object.keys(a)
    .filter(county => b[county] && a[county].winner !== b[county].winner)
    .map(county => ({
      county,
      from: `${a[county].winner} +${a[county].margin_pct}%`,
      to:   `${b[county].winner} +${b[county].margin_pct}%`,
    }));
}
console.log(flipsBeween('Governor', '2018', '2022'));
```

### Python examples

```python
import json
from pathlib import Path

data = json.loads(Path('Data/md_county_aggregated_results_1986_2024.json').read_text())
results = data['results_by_year']

# --- All counties for a year + contest, sorted by margin ---
def sorted_counties(year: str, contest: str):
    counties = results.get(year, {}).get(contest, {})
    return sorted(
        counties.items(),
        key=lambda x: float(x[1]['margin_pct']) * (1 if x[1]['winner'] == 'DEM' else -1),
        reverse=True,
    )

for county, r in sorted_counties('2022', 'Governor'):
    sign = 'D' if r['winner'] == 'DEM' else 'R'
    print(f"{county:30s} {sign}+{r['margin_pct']}%")

# --- Compute statewide margin for all years of a contest ---
def statewide_arc(contest: str):
    for year in sorted(results):
        counties = results[year].get(contest)
        if not counties:
            continue
        dem = sum(r['dem_votes'] for r in counties.values())
        rep = sum(r['rep_votes'] for r in counties.values())
        tot = sum(r['total_votes'] for r in counties.values())
        margin = abs(dem - rep) / tot * 100
        winner = 'D' if dem > rep else 'R'
        # grab candidate names from first county
        first = next(iter(counties.values()))
        print(f"{year}: {first['dem_candidate']} {dem/tot*100:.2f}% vs "
              f"{first['rep_candidate']} {rep/tot*100:.2f}% → {winner}+{margin:.2f}%")

statewide_arc('President')

# --- Single-county arc across all years ---
def county_arc(county: str, contest: str):
    for year in sorted(results):
        r = results[year].get(contest, {}).get(county)
        if r:
            sign = 'D' if r['winner'] == 'DEM' else 'R'
            print(f"{year}: {sign}+{r['margin_pct']}%  "
                  f"({r['dem_candidate']} vs {r['rep_candidate']})")

county_arc('Howard County', 'Governor')

# --- Find the record margin holder for each competitiveness category ---
records = {}
for year, contests in results.items():
    for contest, counties in contests.items():
        for county, r in counties.items():
            code = r['competitiveness']['code']
            margin = float(r['margin_pct'])
            if code not in records or margin > float(records[code]['margin_pct']):
                records[code] = {'year': year, 'contest': contest,
                                 'county': county, **r}

for code, r in sorted(records.items()):
    print(f"{code:20s}: {r['county']} {r['year']} {r['contest']} +{r['margin_pct']}%")
```

---

## Research Findings Summary

Ten analytical cards are embedded in the map sidebar, each backed by specific county-level statistics from the dataset. Each card uses colored inline metric chips (blue for Democratic margins, red for Republican) and bold subheadings to structure the data within each narrative.

### 1. The Great Suburban Reversal (1988–2024)
Documents the systematic conversion of four formerly Republican suburban counties in presidential voting. Howard County: R+12.92% (1988) → D+41.31% (2024). Frederick County: R+31.11% → D+8.74%. Anne Arundel: R+27.79% → D+13.82%. Baltimore County: R+14.73% → D+24.31%. The statewide presidential arc moved from R+2.63% (1988) to D+34.09% (2020). Explains the DC transplant frontier hypothesis: the Democratic suburban wave radiated outward from DC's economic core county-by-county from the 1990s through the 2020s.

### 2. Howard County: Most Dramatic Single-County Realignment
Traces all eight presidential cycles from R+12.92% (1988) to D+44.27% (2020). Explains the Hogan lag effect (Hogan won Howard R+19.66% in 2018 under Jealous) against the Moore 2022 payoff (D+43.38%, a 63-point swing in one cycle). Attributes the structural cause to Columbia — James Rouse's planned city, founded in 1967 with an explicit mission of racial integration and progressive community design — as having embedded a different civic and demographic baseline from Howard County's founding that took four decades to fully express itself electorally.

### 3. Baltimore County: The Last Suburban Domino to Fall
Documents the 26-year split-ticket era during which Baltimore County voted Democratic presidentially every cycle from 1992 onward while simultaneously giving Republicans enormous gubernatorial margins: R+23.14% for Ehrlich (2002), R+24.65% for Hogan (2014), R+27.84% for Hogan (2018). Then 2022: Moore carried Baltimore County by D+30.70% — a 58-point single-cycle collapse of the split. Explains why the split ended: the GOP's Trump-era alignment made Hogan-style crossover appeals structurally unreproducible; Dan Cox's candidacy was the stress test that confirmed the split was over.

### 4. Charles County: Fastest Total Reversal
Documents the deepest full reversal in the dataset: R+27.48% presidential (1988) to D+40.50% (2024), a net 68-point swing. Gubernatorially: R+12.94% (2002) → D+39.51% for Moore (2022). Explains the DC pricing-out chain: PG County's rising housing costs pushed Black middle-class buyers southward into Charles County's Waldorf area, carrying decades of embedded Democratic voting habits into a formerly conservative exurban county. Alsobrooks carried Charles by D+28.27% in the 2024 Senate race.

### 5. Montgomery County: Near-Tossup to Democratic Fortress
1988: D+3.43% — a genuine swing county. 2020: D+59.64%. 2024 Senate: Alsobrooks D+33.08% against Hogan, a Montgomery County native seeking his third statewide win. Explains the institutional concentration effect: NIH, FDA, World Bank, IMF, and dozens of federal agencies created a uniquely dense cluster of highly educated, internationally connected, progressive professional residents over decades; simultaneously, Montgomery became home to one of the largest and most diverse immigrant populations in the Mid-Atlantic, together making the 1988 composition unrecoverable for Republicans.

### 6. Prince George's County: America's Wealthiest Majority-Black County
Six-part deep dive: (1) Origin story — GI Bill, federal careers, Black professional migration from DC built a uniquely wealthy Black suburban county over 60 years; (2) Electoral foundation — at least D+36.74% gubernatorially every cycle since 1994, peaking at D+80.91% for Moore 2022; (3) The 2014 Brown warning — Brown as PG County Lt. Gov. won PG by D+67.47% and still lost statewide, proving PG alone couldn't substitute for incomplete suburban realignment; (4) Moore 2022 — both pillars finally aligned: PG D+80.91% + suburban floors held; (5) Alsobrooks 2024 — first Black and first female Maryland U.S. Senator, won statewide 54.64% against Hogan; (6) Key insight — PG is the engine, the suburbs are the transmission.

### 7. Western Maryland and the Republican Consolidation Belt
Garrett County: dataset records R+78.53% (2018 governor — the highest single margin of any county in any race in the entire dataset) and R+66.66% presidential (2016). Carroll County: a 129-point arc from D+58.49% in 1986 to R+70.87% in 2018. Explains the geometric problem: the western MD region combined casts roughly the same votes as a mid-sized Montgomery County precinct cluster. Republican consolidation is complete, deep, and structurally irreversible — and structurally insufficient to win anything statewide against metro-area Democratic vote factories.

### 8. 1986: The Pre-Realignment Baseline
Schaefer won every county: Carroll D+58.49%, Harford D+67.49%, Garrett D+22.27%, Baltimore County D+70.79%. Explains why — the New Deal coalition was still intact in Maryland; white rural and working-class voters had not yet undergone the national partisan sorting that followed the Reagan era. The 1986 result is not a historical footnote but the deepest possible baseline for measuring how total Maryland's realignment has been. The Senate exception: Democrats held every Senate seat across all 16 years in this dataset.

### 9. 1994: The Republican High-Water Mark
Sauerbrey lost by fewer than 6,000 votes of 1.4 million cast. Reconstructs the 1994 suburban map: Howard R+7.14% (last Republican gubernatorial result there for 28 years), Anne Arundel R+20.70%, Frederick R+29.08%, Harford R+29.59%, Carroll R+44.15%, Baltimore County R+13.60%. Notes the critical same-ballot Senate contrast: Sarbanes won D+18.20% that same day, revealing the Republican threat as a gubernatorial-race-specific candidate phenomenon, not structural competitiveness. Traces how the decade between 1994 and 2004 systematically closed each of the doors Sauerbrey had walked through.

### 10. The Candidate Effect: Hogan, Harford, and Alsobrooks
The most methodologically important card: distinguishes structural trend from candidate-driven aberration. Harford County as maximum-signal example: R+57.15% for Hogan (2014) vs. R+8.46% for Cox (2022) — a 51-point intra-party swing in one county between two Republican nominees with no demographic change. The 2018 compression map: Montgomery fell to D+5.39% gubernatorially; Howard went R+19.66%; Baltimore County R+27.84% — the same counties that gave Moore 59%, 43%, and 31% in 2022. Hogan's 2024 Senate ceiling: running as himself, maximally well-known, the best available Republican crossover candidate, he received 42.84% statewide — a D+11.80% Democratic win that is simultaneously Hogan's personal ceiling and the structural Democratic floor.

---

## Statewide Results Reference

Complete statewide aggregated results for all available years, computed from the county-level data. All percentages are share of total votes (including third-party); margins are `|D−R| / total`.

### Presidential (8 cycles)

| Year | Democratic Candidate | D% | Republican Candidate | R% | Margin |
|---|---|---|---|---|---|
| 1988 | Michael S. Dukakis | 48.20% | George Bush | 51.11% | **R+2.91%** |
| 1992 | Bill Clinton | 49.80% | George Bush | 35.62% | **D+14.18%** |
| 1996 | Bill Clinton | 54.26% | Bob Dole | 38.27% | **D+15.99%** |
| 2000 | Al Gore | 56.57% | George W. Bush | 40.18% | **D+16.39%** |
| 2012 | Barack Obama | 59.19% | Mitt Romney | 38.49% | **D+20.70%** |
| 2016 | Hillary Clinton | 53.99% | Donald J. Trump | 39.40% | **D+14.59%** |
| 2020 | Joe Biden | 65.36% | Donald J. Trump | 32.15% | **D+33.21%** |
| 2024 | Kamala D. Harris | 62.62% | Donald J. Trump | 34.09% | **D+28.53%** |

> Note: 1988 is the only presidential year in the dataset where Maryland voted Republican. Every subsequent cycle has been Democratic, with the margin growing through 2020 before a slight contraction in 2024.

### Governor (8 cycles)

| Year | Democratic Candidate | D% | Republican Candidate | R% | Margin |
|---|---|---|---|---|---|
| 1986 | William Donald Schaefer | 82.37% | Thomas J. Mooney | 17.63% | **D+64.74%** |
| 1990 | William Donald Schaefer | 59.76% | William S. Shepard | 40.23% | **D+19.53%** |
| 1994 | Parris N. Glendening | 50.22% | Ellen R. Sauerbrey | 49.78% | **D+0.43%** |
| 1998 | Parris N. Glendening | 55.18% | Ellen R. Sauerbrey | 44.82% | **D+10.37%** |
| 2002 | Kathleen Kennedy Townsend | 47.69% | Robert L. Ehrlich | 51.55% | **R+3.86%** |
| 2014 | Anthony G. Brown | 45.33% | Larry Hogan | 52.94% | **R+7.61%** |
| 2018 | Ben Jealous | 41.08% | Larry Hogan | 57.73% | **R+16.65%** |
| 2022 | Wes Moore | 64.53% | Dan Cox | 32.12% | **D+32.41%** |

> The gubernatorial arc shows the split-ticket era most clearly: Republicans won three of eight governorships (2002, 2014, 2018) even as the presidential race moved to D+33%.  The 2022 Moore result — D+32.41% — is the second-largest Democratic gubernatorial margin in the dataset, exceeded only by Schaefer's 1986 landslide (D+64.74%) when he was running essentially unopposed.

### U.S. Senator (11 cycles)

| Year | Democratic Candidate | D% | Republican Candidate | R% | Margin |
|---|---|---|---|---|---|
| 1986 | Barbara A. Mikulski | 60.69% | Linda Chavez | 39.31% | **D+21.37%** |
| 1988 | Paul S. Sarbanes | 61.79% | Alan L. Keyes | 38.19% | **D+23.60%** |
| 1992 | Barbara A. Mikulski | 71.00% | Alan L. Keyes | 28.98% | **D+42.02%** |
| 1994 | Paul S. Sarbanes | 59.10% | William Brock | 40.90% | **D+18.21%** |
| 1998 | Barbara Ann Mikulski | 70.50% | Ross Z. Pierpont | 29.50% | **D+41.01%** |
| 2000 | Paul S. Sarbanes | 63.18% | Paul H. Rappaport | 36.74% | **D+26.44%** |
| 2012 | Ben Cardin | 52.69% | Daniel John Bongino | 27.74% | **D+24.96%** |
| 2016 | Chris Van Hollen | 54.82% | Kathy Szeliga | 41.42% | **D+13.40%** |
| 2018 | Ben Cardin | 61.46% | Tony Campbell | 33.57% | **D+27.89%** |
| 2022 | Chris Van Hollen | 65.78% | Chris Chaffee | 34.07% | **D+31.71%** |
| 2024 | Angela Alsobrooks | 54.64% | Larry Hogan | 42.84% | **D+11.80%** |

> Democrats have won every Senate race in this dataset across 38 years. The closest Republican approach was Hogan in 2024 at D+11.80% — still a comfortable Democratic victory, and the product of running the most formidable Republican candidate the Maryland GOP had produced since the Sauerbrey era. The high-water mark for Democrats was Mikulski 1992 at D+42.02%, nearly matching Schaefer's pre-realignment gubernatorial landslide.

---

## Complete County Snapshots

Full 24-county results for two analytically critical election years.

### 2020 Presidential — Biden vs. Trump

The 2020 presidential results show Maryland's political geography at its most clearly sorted. Fourteen of 24 jurisdictions voted Democratic; 10 voted Republican. Biden carried the state D+33.21%.

| County | Winner | Margin | D% | R% |
|---|---|---|---|---|
| Prince George's County | **D** | D+80.53% | 89.26% | 8.73% |
| Baltimore city | **D** | D+76.62% | 87.30% | 10.68% |
| Montgomery County | **D** | D+59.64% | 78.61% | 18.97% |
| Charles County | **D** | D+40.90% | 69.49% | 28.59% |
| Howard County | **D** | D+44.27% | 70.70% | 26.43% |
| Baltimore County | **D** | D+27.04% | 62.28% | 35.24% |
| Anne Arundel County | **D** | D+14.53% | 55.82% | 41.29% |
| Frederick County | **D** | D+9.61% | 53.36% | 43.75% |
| Calvert County | R | R+5.62% | 45.99% | 51.61% |
| Kent County | **D** | D+1.24% | 49.37% | 48.13% |
| Talbot County | **D** | D+0.51% | 49.05% | 48.54% |
| Wicomico County | R | R+1.93% | 47.73% | 49.66% |
| Somerset County | R | R+14.76% | 41.80% | 56.56% |
| Dorchester County | R | R+11.94% | 42.92% | 54.86% |
| St. Mary's County | R | R+13.81% | 41.57% | 55.38% |
| Harford County | R | R+12.04% | 42.59% | 54.63% |
| Washington County | R | R+20.92% | 38.42% | 59.34% |
| Worcester County | R | R+18.97% | 39.63% | 58.60% |
| Carroll County | R | R+23.68% | 36.34% | 60.02% |
| Queen Anne's County | R | R+26.52% | 35.35% | 61.87% |
| Cecil County | R | R+26.62% | 35.42% | 62.04% |
| Caroline County | R | R+32.86% | 32.27% | 65.13% |
| Allegany County | R | R+38.29% | 29.90% | 68.19% |
| Garrett County | R | R+55.86% | 21.02% | 76.88% |

### 1994 Governor — Glendening vs. Sauerbrey

The 1994 gubernatorial results show the high-water mark of Republican statewide competitiveness. Sauerbrey carried 22 of 24 jurisdictions; Democrats held only Baltimore City and Prince George's County. Glendening won statewide by D+0.43% — a margin of fewer than 6,000 votes.

| County | Winner | Margin |
|---|---|---|
| Baltimore city | **D** | D+49.59% |
| Prince George's County | **D** | D+36.74% |
| Montgomery County | **D** | D+17.34% |
| Howard County | R | R+7.14% |
| Charles County | R | R+21.94% |
| Baltimore County | R | R+13.60% |
| Anne Arundel County | R | R+20.70% |
| Calvert County | R | R+21.74% |
| St. Mary's County | R | R+17.00% |
| Frederick County | R | R+29.08% |
| Harford County | R | R+29.59% |
| Carroll County | R | R+44.15% |
| Cecil County | R | R+27.68% |
| Kent County | R | R+15.68% |
| Queen Anne's County | R | R+30.19% |
| Talbot County | R | R+31.51% |
| Caroline County | R | R+33.90% |
| Dorchester County | R | R+21.59% |
| Wicomico County | R | R+19.22% |
| Somerset County | R | R+26.46% |
| Worcester County | R | R+24.06% |
| Washington County | R | R+28.68% |
| Allegany County | R | R+14.28% |
| Garrett County | R | R+54.25% |

> Compare the 2020 and 1994 maps side by side: every county that was competitive in 1994 (Howard, Baltimore County, Frederick, Anne Arundel) is now a solid Democratic county. In 1994 Sauerbrey won Howard by R+7.14%, Baltimore County by R+13.60%, and Frederick by R+29.08%. In 2020 those same three counties gave Biden D+44.27%, D+27.04%, and D+9.61% respectively. The combined swing in those three counties alone is over 150 points — enough to flip a competitive state into a structural Democratic fortress.

---

## Key Dataset Records

Statistically notable results from the 1,035 county-results in the dataset:

| Record | County | Year | Contest | Margin |
|---|---|---|---|---|
| Largest single margin (any category) | Garrett County | 2018 | Governor | R+78.53% (Hogan vs. Jealous) |
| Largest Democratic presidential margin | Prince George's County | 2020 | President | D+80.53% |
| Largest Republican presidential margin | Garrett County | 2016 | President | R+66.66% |
| Biggest total county swing (presidential) | Howard County | 1988→2020 | President | 57+ points (R+12.92 → D+44.27) |
| Biggest total county swing (gubernatorial) | Carroll County | 1986→2018 | Governor | 129+ points (D+58.49 → R+70.87) |
| Smallest margin in dataset | Multiple tossup results | Various | Various | < 0.50% |
| Largest statewide Democratic Senate margin | Barbara Mikulski | 1992 | U.S. Senator | D+42.02% |
| Closest gubernatorial result | Glendening vs. Sauerbrey | 1994 | Governor | < 0.50% statewide |
| Most dramatic single-cycle gubernatorial swing | Harford County | 2018→2022 | Governor | 51 points (R+59.31 → R+8.46) |
| Best Republicans have done in Senate since 2000 | Larry Hogan | 2024 | U.S. Senator | 42.84% (lost by D+11.80%) |

---

## Known Limitations

| Limitation | Impact | Notes |
|---|---|---|
| **Gap years 2004–2010** | No data for four election cycles; year slider jumps from 2002 to 2012 | Source files not available; this gap covers the Howard Dean era, the 2006 Democratic wave, and Obama's 2008 landslide — all analytically significant |
| **Margin uses total votes, not two-party** | A candidate winning 50% in a 5% third-party race shows a smaller `margin_pct` than their true two-party dominance | Use `dem_votes / two_party_total` for true two-party share comparisons |
| **Third-party candidates aggregated into `other_votes`** | Libertarian, Green, and Reform party performances not individually surfaced in the map UI | Available in `all_parties` field for custom queries |
| **No precinct-level data** | All margins are county-level aggregates; intra-county geographic variation (e.g., suburban vs. rural Howard County) is not visible | SBE precinct data exists for modern years but is not loaded by the map |
| **Presidential results in odd-year off-cycles** | Not applicable; Maryland votes for President every four years; 1986, 1990, 1994, 1998, 2002 have no presidential data | Expected behavior; contest selector skips to valid years |
| **Candidate name consistency across years** | The same candidate may appear with slight name variations across different years' raw files (e.g., `"Joseph R. Biden"` vs. `"Joe Biden"`) | Does not affect vote totals or margins; cosmetic only |
| **Running mate removal edge cases** | Unusual running mate formats not split on `/` or ` and ` may slip through | Affects display only; does not affect vote counts or competitiveness |

---

## Data Sources and Notes

- **Election results** — Maryland State Board of Elections official general election canvass reports, available at [elections.maryland.gov](https://elections.maryland.gov). Files downloaded and stored as `Data/YYYY General Election.(csv|txt)`.
- **OpenElections format** — normalized output follows the [OpenElections](https://openelections.net/) county-level CSV schema for Maryland; the OpenElections project is an open-data initiative publishing standardized election results for every U.S. state.
- **County boundaries** — 2020 Census TIGER/Line county shapefile for Maryland (FIPS state code 24), available from the [U.S. Census Bureau TIGER/Line program](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html). Canonical county identifiers throughout the project use the `NAMELSAD20` field.
- **GeoJSON** — `Data/geo/md_counties_2020.geojson` serves the county polygons to the browser via Mapbox GL JS. Derived from the same 2020 Census geometry.
- **Mapbox GL JS** — map rendering library, loaded from CDN at `api.mapbox.com/mapbox-gl-js/`. Requires a valid public Mapbox token for tile requests.
- **ColorBrewer palettes** — competitiveness scale colors use single-hue sequential ramps from [colorbrewer2.org](https://colorbrewer2.org/) (blues for Democratic, reds for Republican), ensuring accessibility-friendly perceptual linearity from light (competitive) to dark (dominant).
- **Baltimore City / Baltimore County disambiguation** — these two jurisdictions have shared a name root since Baltimore City separated from Baltimore County in 1851. The build script explicitly resolves this using the Census shapefile's `NAMELSAD20` values (`"Baltimore City"` vs. `"Baltimore County"`). Both are included in every contest year throughout the dataset.
- **Margin calculation methodology** — all margins in this project are calculated as `|dem_votes − rep_votes| / total_votes × 100`, where `total_votes` includes third-party and independent votes. This differs from the "two-party vote share" convention used by some political science publications; results are not directly comparable to sources using two-party denominators.
