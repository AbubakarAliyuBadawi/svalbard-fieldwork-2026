# Otter bathymetry plotting scripts

## All recordings and longitude–latitude mission tracks

To process every paired recording in the supplied directory:

```bash
python3 usv_otter/scripts/process_all_otter.py \
  '/home/badawi/OneDrive/PhD_BREACH/PhD_courses/AT-834 - Arctic Marine Measurements Techniques/Data/USV_Otter/06-09-2026'
```

Each recording has its own `results/YYYYMMDD_HHMMSS/` folder with the four
bathymetry/quality figures and `05_gps_longitude_latitude.png` / `.pdf`.
The GPS figure uses all valid recorded fixes, including times without a valid
bottom pick. Colour shows elapsed recorder time; arrows show travel direction;
circles and squares mark the first and last valid fixes. Axes show WGS84 decimal
longitude and latitude with the aspect ratio corrected for local latitude.
No smoothing is applied. Invalid fixes and gaps over one second break the line.

`gps_track.csv` preserves coordinates, GPS UTC, recorder time, validity and
segment IDs. `gps_track.geojson` can be opened in QGIS; its coordinates are
longitude, latitude. GeoJSON lines omit invalid fixes and retain breaks.

The `results/` folder also contains:

- `all_gps_tracks_panels.png` / `.pdf`: each recording shown at its own map extent,
  suitable for inspecting parallel passes and turns.
- `all_gps_tracks_overview.png` / `.pdf`: all recordings in geographic context.
- `all_gps_tracks.geojson`: separate features for each recorded route.
- `all_recordings_summary.csv`: comparable statistics for all recordings.

Add `--gps-only` to regenerate these GPS products from existing extracted data
without repeating sonar processing. A recording is not necessarily a complete
mission. No lines are drawn across files, and no planned route is inferred.
These tracks show how the vehicle actually moved. Planned waypoints or a
mission-plan export are required to quantify departures from the planned route.

## Single recording

Run from `/home/badawi/Desktop/field_work_data`:

```bash
python3 usv_otter/scripts/extract_otter.py
python3 usv_otter/scripts/plot_otter.py
```

The dependencies are already available in this workspace. On another computer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r usv_otter/scripts/requirements.txt
.venv/bin/python usv_otter/scripts/extract_otter.py
.venv/bin/python usv_otter/scripts/plot_otter.py
```

Both scripts accept `--help`, and resolve default paths relative to their own
location, so they can also be run from another working directory. Original sonar
files are read only. Rerunning overwrites derived files in the output folder.

## Outputs

`results/figures/` contains 300 dpi PNG and PDF versions of:

| File | Suggested report placement |
| --- | --- |
| `01_bathymetry_track` | Section 5.5.2: measured track coloured by bottom range |
| `02_bottom_profiles` | Section 5.5.2: bottom range along track and over time |
| `03_echogram` | Section 5.5.2 or appendix: uncalibrated echoes and bottom picks |
| `04_recording_quality` | Section 5.5.3 or appendix: ping intervals and invalid detections |

The same folder includes `survey_summary.csv` and `figure_captions.md`.
`results/` contains per-ping `soundings.csv`, `gps_fixes.csv`, all decoded
echo samples in `echogram.npz`, acquisition settings in `acquisition_config.xml`,
and provenance/checks in `metadata.json`.

## Read before using the figures in the report

**These are preliminary figures from an inferred binary decoder.** Compare a
selection of ping numbers, positions, bottom ranges and echogram sections with
Visual Acquisition / Visual Aquatic before treating them as report results.
The paired DT4 and RTPX bottom records agree exactly, but agreement between
two recordings of the same signal is not independent scientific validation.

The supplied recording positions span approximately 78.428–78.432° N,
17.121–17.144° E. These do not match the Adventfjorden site described in the
draft. Confirm the file/site association; do not caption these as Adventfjorden
without resolving the discrepancy. The scripts deliberately use no site name.

The ordinate is **acoustic bottom range below the transducer**, not chart-datum
depth. The acquisition configuration specifies a 1 m bottom-depth offset, but
the stored range values match sample number times sample spacing without that
offset. The scripts do not add it. Confirm the actual transducer immersion,
water-level reference, sound-speed settings, and any motion corrections before
converting range into corrected bathymetric depth. Do not add an offset twice
if later replacing this extraction with a vendor depth export.

The recorder clock is about 485.258 seconds ahead of GPS UTC. The scripts join
GPS and pings using the common recorder clock and preserve both timestamps.
No automatic clock shift is applied to raw records. Resolve the offset before
comparing the recording with a separate mission or communications log.

For this file there are 5,770 pings, of which 5,534 have a stored valid bottom
flag; the recording spans about 19.30 minutes. Accepted stored ranges are about
12.40–40.58 m. These counts and limits are not an estimate of measurement accuracy.

## Decoding and plotting choices

- DT4 records are checked against their trailing lengths; truncation fails.
- The supported split-beam tag is `0x001d`. Its payload contains a channel,
  ping number, millisecond tick, stored sample count, then interleaved 16-bit
  amplitude and angle words. Only amplitude is used. Zero-run markers expand to
  low-byte + 2 samples. Every expanded ping must match the configured count.
- Echo amplitudes use exponent/mantissa decoding. Plots show log10 raw counts,
  **not calibrated Sv or TS**. Neither substrate nor biological classes are inferred.
- DT4 tag `0x0032` stores channel, ping, tick, valid flag, sample index and range.
  These inferred fields are matched to RTPX `0x0dad` records, including time.
  Range versus sample number must agree to within 1 cm (observed maximum
  discrepancy approximately 0.00033 m, consistent with rounded settings).
- Sample spacing uses recorded sound speed (1469.5875 m/s) and interval (24 µs).
  The record reports 199000 Hz and serial `T200P316`; this is not a confirmed
  commercial sensor model. Configured temperature/salinity are inputs, not
  evidence that a CTD measured those values during the mission.
- NMEA checksums, RMC active status and GGA fix quality are checked. Positions
  are interpolated only between adjacent valid fixes at most 1 second apart.
  There is no extrapolation beyond the GPS time span.
- Invalid bottom flags remain in the exported data; their range is NaN. There
  is no smoothing or additional outlier filter, so manual review remains necessary.
- The map uses a local WGS84 azimuthal equidistant projection centred on the
  observations. No network basemap, coastline, or interpolated seabed is used.
- Distance sums geodesic distances between connected valid positions. GPS noise
  while stationary can increase the total; it is an observed-track estimate.
- Full samples are retained; the plotted echogram subsamples pings for readability.
- Recording continuity does not prove the reported communications outage time
  or establish that no data were lost before or after this file.

Reference for the DT4 settings, exponent/mantissa convention and range formula:
[rdbiosonics reader source](https://github.com/jklymak/rdbiosonics/blob/main/src/rdbiosonics/rddtx.py),
a port of Rich Pawlowicz's reader. Its public reader supports single-beam records;
this project's split-beam and stored-bottom extensions are inferred locally,
not documented or certified by that project or BioSonics.

## Checks

```bash
python3 -m unittest discover -s usv_otter/scripts -p 'test_*.py' -v
```

The checks cover NMEA checksums, coordinate signs, invalid-fix/gap handling and
truncated records. Extraction also performs the full-record structural checks
and paired-file comparisons described above.
