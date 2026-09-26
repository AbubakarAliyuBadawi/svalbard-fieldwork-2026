# Dive/resurface results (074948_08_09_sidescan, lauv-marie)

Log 07:49:48–08:24:40 UTC (34.9 min). Local frame origin: first accepted GPS fix (78.25980N, 15.61419E). Track extent N -331..9 m, E -78..264 m.

Heading: EstimatedState psi − AHRS yaw = 12.74° constant (declination added by DUNE; AHRS psi == psi_magnetic). DR below uses the EstimatedState heading.

Surface-fitted corrections from star mission 7 Sept (analyze_star.py, DUNE heading): water track δ=+0.09°, s=0.965, c=(+0.003,-0.019) m/s; bottom track δ=+0.03°, s=0.992; RPM δ=-0.08°, k×0.841. Assumes the compass/DVL behaviour did not change between the two days.

## GPS / medium summary

- GpsFix: 2092 rows at 1 Hz; VALID_POS bit set on 8.5 %, accepted (hacc<15, hdop<4) 1.9 % (40 fixes), hacc<5 m 33 fixes.
- 138 fixes carry VALID_POS but hacc ≥ 15 m (median hacc 198 m, median satellites 3) at depths up to 61.2 m: receiver garbage while submerged, correctly rejected by the navigation (GpsFixRejection reasons: {1: 1914, 3: 121, 0: 21}; 1=INVALID, 3=ABOVE_MAX_HACC, 0=ABOVE_THRESHOLD).
- Header timestamp − GPS UTC of fix: median +0.243 s.
- VehicleMedium seconds: {3: 2052, 2: 41} (2=WATER, 3=UNDERWATER). Depth [CTD] max 61.3 m.
- DVL bottom track valid 98.4 % of 9068 samples; water track valid 98.6 %.
- USBL/LBL/range messages in the log: **none**. Acoustic frames received (UamRxFrame): 6.
- DUNE Navigation log entry at 08:24:37: `estimating error of 0.72% (19.6/2731.5m) in 2058s`

## Dive / resurface events: 1

### Dive 1: medium UNDERWATER 07:50:25 → 08:24:37 (34.2 min)

- Last accepted GPS before: 07:50:24 (hacc 13.0 m); first fix accepted by DUNE after: 08:24:37 (hacc 10.0 m, hdop 0.98, 14 sats); GPS gap **34.2 min**. First fix with hacc<5 m: none in this log.
- Depth max 61.3 m, mean 50.6 m; DVL altitude valid 99 %, median 7.0 m.
- DVL bottom lock while submerged: 98.6 % of 8867 samples, 8 dropouts, longest 20.2 s.
- USBL fixes while submerged: **0** (none logged at all). Acoustic frames received from the ship while submerged: 6.
- DUNE NavigationUncertainty at end of dive: σ_x = 1.0 m, σ_y = 1.0 m (max during dive 6.6 m).
- **DUNE estimate just before the first accepted fix minus that fix: ΔN +16.3 m, ΔE +11.4 m, |Δ| = 19.9 m** (fix hacc 10.0 m). Largest single-step EstimatedState correction within [-3,+5] s: 19.6 m.

  Own dead reckoning from the last accepted fix before the dive to the first accepted fix after it:

  | input | closure ΔN [m] | ΔE [m] | |Δ| [m] | |Δ| / path length | closure-implied δ [°], scale |
  |---|---|---|---|---|---|
  | bottom track | +41.3 | -4.4 | 41.5 | 1.52 % | +6.1, 1.094 |
  | bottom track + surface fit | +42.3 | -6.5 | 42.8 | 1.58 % | +6.1, 1.102 |
  | water track | -21.8 | +8.3 | 23.3 | 0.83 % | -2.1, 0.940 |
  | water track + surface fit | -8.3 | -39.6 | 40.5 | 1.50 % | -6.1, 1.087 |
  | RPM x 1.3e-3 | -20.7 | +72.5 | 75.4 | 2.38 % | +4.0, 0.814 |
  | RPM x 1.3e-3 + surface fit | -10.6 | -97.9 | 98.4 | 3.71 % | -15.6, 1.251 |

  GPS displacement over the dive: ΔN -187.9, ΔE +249.6 m (312 m); the closure-implied δ is only meaningful when this displacement is long compared with the closure error.
- A heading bias δ rotates a DR track about the dive point; with the surface-fitted δ = +0.09° this is a median 0.3 m, max 0.5 m during this dive (distance from dive point up to 328 m); per degree of bias: max 5.7 m. Reciprocal survey lines cancel most of it at the end, so closure errors understate mid-mission georeferencing error.
