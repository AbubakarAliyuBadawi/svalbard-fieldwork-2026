# Dive/resurface results (094605_0700926LongYoYo1, lauv-thor)

Log 09:46:05–10:39:51 UTC (53.8 min). Local frame origin: first accepted GPS fix (78.65814N, 16.86423E). Track extent N -478..347 m, E -4509..5 m.

Heading: EstimatedState psi − AHRS yaw = 14.03° constant (declination added by DUNE; AHRS psi == psi_magnetic). DR below uses the EstimatedState heading.

Surface-fitted corrections from this log's surface runs (466 GPS epochs, DUNE headings 214–330°): water track δ=-3.91°, s=0.984, c=(-0.053,-0.058) m/s (rms 0.253); RPM δ=-0.95°, s=0.882, c=(-0.113,-0.156). All surface runs point roughly the same way, so δ and c are confounded here; the water-track rows flagged invalid are used as numbers.

## GPS / medium summary

- GpsFix: 3226 rows at 1 Hz; VALID_POS bit set on 18.8 %, accepted (hacc<15, hdop<4) 15.0 % (485 fixes), hacc<5 m 413 fixes.
- 120 fixes carry VALID_POS but hacc ≥ 15 m (median hacc 52 m, median satellites 10) at depths up to 20.6 m: receiver garbage while submerged, correctly rejected by the navigation (GpsFixRejection reasons: {1: 2621, 3: 108, 0: 18}; 1=INVALID, 3=ABOVE_MAX_HACC, 0=ABOVE_THRESHOLD).
- Header timestamp − GPS UTC of fix: median -0.020 s.
- VehicleMedium seconds: {3: 2621, 2: 606} (2=WATER, 3=UNDERWATER). Depth [SmartX] max 80.5 m.
- DVL bottom track valid 0.3 % of 16132 samples; water track valid 0.3 %.
- WaterVelocity rows flagged invalid still hold numbers: x vs RPM correlation 0.92 over 15957 samples; mean x/(RPM·1.3e-3) = 0.89. They are DVL water-track outputs whose quality flag failed; not used by the filter.
- USBL/LBL/range messages in the log: **none**. Acoustic frames received (UamRxFrame): 0.
- DUNE Navigation log entry at 10:09:01: `estimating error of 0.03% (0.6/1920.7m) in 1252s`
- DUNE Navigation log entry at 10:38:01: `estimating error of 0.02% (0.5/2249.2m) in 1500s`

## Dive / resurface events: 2

### Dive 1: medium UNDERWATER 09:49:48 → 10:08:48 (19.0 min)

- Last accepted GPS before: 09:48:13 (hacc 13.0 m); first fix accepted by DUNE after: 10:09:00 (hacc 15.0 m, hdop 1.47, 6 sats); GPS gap **20.8 min**. First fix with hacc<5 m: 10:09:56 (hacc 4.9 m).
- Depth max 69.3 m, mean 36.9 m; DVL altitude valid 1 %, median 24.6 m.
- DVL bottom lock while submerged: 0.8 % of 5700 samples, 6 dropouts, longest 831.4 s.
- USBL fixes while submerged: **0** (none logged at all). Acoustic frames received from the ship while submerged: 0.
- DUNE NavigationUncertainty at end of dive: σ_x = 5.1 m, σ_y = 5.1 m (max during dive 5.1 m).
- **DUNE estimate just before the first accepted fix minus that fix: ΔN +267.5 m, ΔE -116.0 m, |Δ| = 291.6 m** (fix hacc 15.0 m). Largest single-step EstimatedState correction within [-3,+5] s: 291.6 m.
- Same estimate propagated (bottom-track DR) to the first hacc<5 m fix at 10:09:56: ΔN +260.2, ΔE -95.7, |Δ| = 277.2 m.

  Own dead reckoning from the last accepted fix before the dive to the first accepted fix after it:

  | input | closure ΔN [m] | ΔE [m] | |Δ| [m] | |Δ| / path length | closure-implied δ [°], scale |
  |---|---|---|---|---|---|
  | bottom track | n/a (bottom lock 0.8 % of the dive) | | | | |
  | bottom track + surface fit | n/a (bottom lock 0.8 % of the dive) | | | | |
  | water track | +224.4 | +5.5 | 224.4 | 12.58 % | -7.6, 0.994 |
  | water track + surface fit | +42.0 | -51.4 | 66.3 | 3.64 % | -1.4, 0.970 |
  | RPM x 1.3e-3 | +277.7 | -194.3 | 339.0 | 16.97 % | -8.4, 0.886 |
  | RPM x 1.3e-3 + surface fit | +76.1 | -173.0 | 189.0 | 9.76 % | -2.3, 0.906 |

  GPS displacement over the dive: ΔN +10.8, ΔE -1677.5 m (1678 m); the closure-implied δ is only meaningful when this displacement is long compared with the closure error.
- A heading bias δ rotates a DR track about the dive point; with the surface-fitted δ = -3.91° this is a median 57.8 m, max 113.7 m during this dive (distance from dive point up to 1668 m); per degree of bias: max 29.1 m. Reciprocal survey lines cancel most of it at the end, so closure errors understate mid-mission georeferencing error.

### Dive 2: medium UNDERWATER 10:13:15 → 10:37:56 (24.7 min)

- Last accepted GPS before: 10:13:05 (hacc 13.0 m); first fix accepted by DUNE after: 10:38:00 (hacc 13.0 m, hdop 1.59, 5 sats); GPS gap **24.9 min**. First fix with hacc<5 m: 10:38:11 (hacc 4.7 m).
- Depth max 80.5 m, mean 38.2 m; DVL altitude valid 0 %, median nan m.
- DVL bottom lock while submerged: 0.0 % of 7405 samples, 1 dropouts, longest 1480.8 s.
- USBL fixes while submerged: **0** (none logged at all). Acoustic frames received from the ship while submerged: 0.
- DUNE NavigationUncertainty at end of dive: σ_x = 5.5 m, σ_y = 5.5 m (max during dive 5.5 m).
- **DUNE estimate just before the first accepted fix minus that fix: ΔN +276.0 m, ΔE -199.4 m, |Δ| = 340.5 m** (fix hacc 13.0 m). Largest single-step EstimatedState correction within [-3,+5] s: 340.5 m.
- Same estimate propagated (bottom-track DR) to the first hacc<5 m fix at 10:38:11: ΔN +278.9, ΔE -197.1, |Δ| = 341.5 m.

  Own dead reckoning from the last accepted fix before the dive to the first accepted fix after it:

  | input | closure ΔN [m] | ΔE [m] | |Δ| [m] | |Δ| / path length | closure-implied δ [°], scale |
  |---|---|---|---|---|---|
  | bottom track | n/a (bottom lock 0.0 % of the dive) | | | | |
  | bottom track + surface fit | n/a (bottom lock 0.0 % of the dive) | | | | |
  | water track | +282.9 | -92.6 | 297.7 | 13.92 % | -8.1, 0.994 |
  | water track + surface fit | +72.6 | -111.3 | 132.9 | 6.02 % | -2.8, 0.962 |
  | RPM x 1.3e-3 | +253.5 | -355.9 | 436.9 | 18.21 % | -8.7, 0.885 |
  | RPM x 1.3e-3 + surface fit | +105.6 | -306.9 | 324.6 | 13.62 % | -4.9, 0.890 |

  GPS displacement over the dive: ΔN -718.4, ΔE -1986.7 m (2113 m); the closure-implied δ is only meaningful when this displacement is long compared with the closure error.
- A heading bias δ rotates a DR track about the dive point; with the surface-fitted δ = -3.91° this is a median 76.7 m, max 150.7 m during this dive (distance from dive point up to 2211 m); per degree of bias: max 38.6 m. Reciprocal survey lines cancel most of it at the end, so closure errors understate mid-mission georeferencing error.
