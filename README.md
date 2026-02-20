# MDRealignment

Interactive Maryland political realignment map and data pipeline (1986-2024), with county-level contest aggregation and competitiveness ratings.

## What is included

- `index.html`: map UI and analysis panels
- `Data/`: raw election files, county shapefile assets, aggregated JSON outputs
- `Data/openelections/`: OpenElections-style normalized files
- `Scripts/convert_to_openelections.py`: converts source election files to OpenElections-style CSV
- `Scripts/build_md_county_aggregated_results.py`: builds county-level aggregated JSON used by the map

## Local setup

1. Set a valid Mapbox public token in `index.html`:
   - `CONFIG.mapboxToken`
2. Open `index.html` with a local static server (recommended) so JSON fetches work.

## Data outputs

- County GeoJSON: `Data/geo/md_counties_2020.geojson`
- Aggregated JSON (current): `Data/md_county_aggregated_results_1986_2024.json`

## Notes

- Competitiveness bins follow the refined rating criteria used in the map legend.
- Candidate fields in aggregated JSON remove running mates for cleaner county-level analysis labels.
