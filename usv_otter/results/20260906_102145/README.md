# Otter recording 20260906_102145

Processed from the paired DT4 and RTPX files in the supplied OneDrive directory.
Original recordings were read only. Derived data and figures are saved here.

## Results

| Metric | Value |
| --- | --- |
| Recorder duration | 22.403 min |
| Observed track distance | 755.43 m |
| Pings | 6,711 |
| Stored valid bottom picks | 6,697 (99.79%) |
| Invalid bottom picks | 14 |
| Valid bottom picks with GPS | 6,696 |
| Minimum bottom range below transducer | 28.53 m |
| Maximum bottom range below transducer | 43.73 m |
| Median bottom range | 37.21 m |
| Maximum interval between recorded pings | 0.400 s |

The map shows a track towards the southeast, several small loops, and a return
towards the southwest. Bottom ranges fluctuate along the route and become
shallower near the end. These are measurements along the track, not a continuous
survey surface. Changes during turns may include vessel-motion effects; no
attitude correction has been applied.

Invalid bottom picks occur near elapsed minutes 5.42 and 8.26–8.30.
The first ping has no bracketed GPS fix and is excluded from the map and
distance profile, but its valid range is retained in the time profile.
The observed track distance excludes that initial interval.

## Verification and interpretation

- All record-length checks and expanded echo sample counts passed.
- DT4 and RTPX bottom flags, sample numbers and range values match exactly.
  Times agree within the decoder's 2 ms tolerance.
- The maximum difference between stored range and sample-index-derived range
  is 0.00036 m. This checks decoding consistency, not survey accuracy.
- All four PNG figures were visually inspected. The stored picks follow the
  prominent bottom echo in the echogram.
- The binary layouts remain inferred; compare with a BioSonics export before
  using the plots as final scientific results.
- Ranges are below the transducer. The configured 1 m depth offset is not added.
  No tide, draft, sound-speed reprocessing, or attitude correction is applied.
- Coordinates centre near 78.44849° N, 17.36428° E, differing from the
  Adventfjorden location in the draft. Confirm the site/file association.
- The recorder clock is approximately 485.0 seconds ahead of GPS UTC.
  GPS and sonar are aligned on their common recorder clock; both times remain
  in the exported CSV. Do not use the filename time as GPS UTC without resolving
  this offset.
- Echo colours are log10 raw counts, not calibrated acoustic backscatter.

## Files

`figures/` contains four numbered figures in 300 dpi PNG and PDF formats,
`survey_summary.csv`, and `figure_captions.md`. Use the track map and profiles
in Section 5.5.2, and the quality figure in Section 5.5.3 or the appendix.

`soundings.csv` contains all pings, ranges and aligned positions;
`gps_fixes.csv` preserves parsed fixes; `echogram.npz` holds every decoded ping.
`metadata.json` records checks, source SHA-256 hashes and settings.

## Reproduce

Run from `/home/badawi/Desktop/field_work_data`:

```bash
python3 usv_otter/scripts/extract_otter.py \
  --dt4 '/home/badawi/OneDrive/PhD_BREACH/PhD_courses/AT-834 - Arctic Marine Measurements Techniques/Data/USV_Otter/06-09-2026/20260906_102145.dt4' \
  --rtpx '/home/badawi/OneDrive/PhD_BREACH/PhD_courses/AT-834 - Arctic Marine Measurements Techniques/Data/USV_Otter/06-09-2026/20260906_102145.rtpx' \
  --out usv_otter/results/20260906_102145

python3 usv_otter/scripts/plot_otter.py \
  --data usv_otter/results/20260906_102145 \
  --out usv_otter/results/20260906_102145/figures
```
