# All Otter recordings — 6 September 2026

All five paired recordings in the supplied OneDrive directory were processed. Each numbered folder contains five PNG/PDF figures, soundings, GPS fixes, GPS tracks in CSV/GeoJSON, the echogram array, and metadata.

## GPS routes

Start with [individual track panels](all_gps_tracks_panels.png) to inspect route geometry, or [the combined overview](all_gps_tracks_overview.png) to locate the recordings relative to one another. Each recording also has its own `figures/05_gps_longitude_latitude.png` and PDF.

These are recorded GPS positions, not planned waypoints. The routes visible in these files are predominantly loops, a triangular route and irregular tracks. They do not show an obvious sequence of closely spaced parallel lawnmower passes. This does not establish what was planned or whether another recording contains the lawnmower mission. File boundaries are not assumed to be mission boundaries. No trajectory is fabricated or joined between recordings.

## Summary

Ranges are acoustic ranges below the transducer, without tide, draft or motion corrections. Track lengths are approximate observed distances calculated from connected GPS positions aligned to pings.

| Recording | Duration (min) | Track (m) | Range (m) | Valid / total pings |
| --- | ---: | ---: | ---: | ---: |
| [20260906_102145](20260906_102145/figures) | 22.40 | 755 | 28.53–43.73 | 6,697 / 6,711 |
| [20260906_132119](20260906_132119/figures) | 19.33 | 1155 | 9.81–20.86 | 5,800 / 5,800 |
| [20260906_134902](20260906_134902/figures) | 25.03 | 1480 | 5.61–18.31 | 7,510 / 7,510 |
| [20260906_141611](20260906_141611/figures) | 24.82 | 742 | 15.15–21.67 | 7,446 / 7,446 |
| [20260906_144107](20260906_144107/figures) | 19.30 | 1455 | 12.40–40.58 | 5,534 / 5,770 |

## Verification and report use

DT4/RTPX bottom-value comparisons and structural checks passed for all five recordings. Extractor tests passed. The new bathymetry plots and combined GPS maps were visually reviewed. Binary sonar decoding remains preliminary pending comparison with a BioSonics export; stored valid flags are not an independent accuracy assessment. GPS routes use checksum-validated active fixes, broken at invalid fixes or recorder gaps over one second.

Longitude–latitude plots preserve approximate local distance proportions at the survey latitude. Colours encode elapsed recorder time within each recording; colour scales and map extents differ between individual panels. Arrows show travel direction. GPS UTC is preserved alongside the recorder clock, whose offset must be resolved before comparison with external mission logs.

Use the individual GPS route figures in Section 5.5.1 and bathymetry/profile figures in Section 5.5.2. A planned-versus-actual comparison requires a separate mission-plan or waypoint export.

Reproduce all outputs with `scripts/process_all_otter.py`; see [the main README](../README.md) for the full command.
