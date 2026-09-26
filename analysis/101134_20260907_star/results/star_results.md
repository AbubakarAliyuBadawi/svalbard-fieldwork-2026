# Star mission results (101134_20260907_star, lauv-marie)

Log span 10:11:35–10:24:44 UTC, 790 s. Origin of local N/E frame: first accepted GPS fix (78.66227N, 16.89959E).

## 4a. Surface, GPS, DVL, headings

- VehicleMedium samples: {2: 790} (2 = WATER/surface, 3 = UNDERWATER). Vehicle at the surface for the whole log: **True**.
- Depth [CTD]: n=3950, mean -0.29 m, min -0.39, max -0.17 m
- Depth [DVL]: n=3931, mean 0.15 m, min 0.12, max 0.18 m
- GpsFix (GPS entity): 790 fixes, median interval 1.00 s, max gap 1.00 s -> rate 1.00 Hz.
- VALID_POS set: 100.0 %; accepted (hacc<15, hdop<4): 100.0 %; hacc<5 m: 100.0 %. hacc median 1.20 m (max 1.60), hdop median 0.63, satellites median 17. Fix type: [0] (0 = standalone, no RTK/DGPS).
- COG/SOG validity bits set on 99.2 % of fixes; SOG median 1.49 m/s.
- Header timestamp minus GPS UTC of fix: median +0.316 s (std 0.020).
- DVL bottom track (GroundVelocity, 5 Hz): 98.3 % valid (67 invalid of 3950); water track (WaterVelocity): 98.1 % valid.
- Bottom-track dropouts: 34 episodes, longest 0.7 s.
- DVL filtered altitude: valid 98.3 %, 33.4–73.2 m (median 60.5 m). So the seabed is within DVL range and the vehicle has bottom lock at the surface, not only RPM speed.
- EulerAngles psi − psi_magnetic: median 0.00°, max |.| 0.00° -> **no magnetic declination is applied** in the AHRS output (Svalbard declination in 2026 is of order +10° E; verify with WMM).
- Rpm (Motor, 10 Hz): median 1363 rpm, min 0, max 1633.
- NavigationUncertainty: sqrt(var x) stays 0.03–0.18 m (GPS-aided all along).

Legs (Goto maneuvers from PlanControlState). Circular means; 'steady' excludes the first 20 s of each leg (the turn). AHRS yaw is magnetic; DUNE heading = AHRS + declination:

| leg | start UTC | dur [s] | AHRS yaw mean [°] | AHRS yaw steady [°] (std) | DUNE heading steady [°] | GPS COG mean [°] | SOG mean [m/s] | GPS track length [m] |
|---|---|---|---|---|---|---|---|---|
| Goto1 | 10:11:38 | 72 | 295.5 | 292.2 (2.8) | 304.9 | 305.7 | 1.63 | 113 |
| Goto2 | 10:12:50 | 143 | 319.5 | 320.4 (1.7) | 333.1 | 330.2 | 1.49 | 212 |
| Goto3 | 10:15:13 | 75 | 76.1 | 82.9 (10.4) | 95.6 | 87.9 | 1.50 | 111 |
| Goto4 | 10:16:28 | 138 | 193.1 | 195.1 (8.3) | 207.8 | 208.3 | 1.50 | 205 |
| Goto5 | 10:18:46 | 70 | 316.9 | 325.2 (14.3) | 337.9 | 326.4 | 1.51 | 104 |
| Goto6 | 10:19:56 | 142 | 75.9 | 79.5 (8.7) | 92.2 | 89.1 | 1.48 | 208 |
| Goto7 | 10:22:18 | 72 | 191.9 | 195.9 (10.5) | 208.6 | 205.6 | 1.53 | 108 |
| Goto8 | 10:23:30 | 74 | 124.1 | 122.2 (1.1) | 134.9 | 142.3 | 1.47 | 107 |

## 4b. USBL / acoustic positioning

- USBL/LBL/range messages in the log: **none**. There is no acoustic position fix in the vehicle log, so USBL error against GPS cannot be computed from this data.
- Acoustic frames received by the vehicle (UamRxFrame): 17; of these 15 are 'pos' text requests from `['manta-ntnu-4']` (the ship-side gateway). Frames transmitted (UamTxFrame): 28 (periodic state reports, broadcast).
- Reception times (UTC): 10:13:59, 10:14:08, 10:14:36, 10:15:01, 10:15:36, 10:15:56, 10:16:30, 10:17:12, 10:17:45, 10:19:15, 10:20:01, 10:20:45, 10:21:12, 10:21:54, 10:23:27, 10:23:44, 10:23:57.
- Config: `[Transports.UAN] USBL Node -- Enabled = false` — the vehicle was not configured to receive USBL fixes. Any USBL solution would only exist in the ship-side (Manta/Neptus) logs.

## Heading sources

- EstimatedState psi − AHRS EulerAngles psi = 12.72° (1st–99th pct 12.47–12.97°), constant over the log. EulerAngles psi equals psi_magnetic, so the AHRS reports magnetic heading and DUNE adds a fixed declination (World Magnetic Model at the initialisation fix; DUNE 2025.06.03). All fits below use the EstimatedState heading; the raw AHRS heading appears only as the 'no declination' case.

## Frame check: DVL bottom track vs GPS velocity at GPS epochs

- n epochs = 784. RMS |v_gps − R(φ,θ,ψ)·v_bt| = **0.167 m/s**; if the DVL values were already NED (no rotation): 2.138 m/s. Body frame confirmed. Mean residual N/E = [0.006, -0.006] m/s.

## 4e. Least-squares current at the surface

Current c = v_GPS − R·v_watertrack (per fix, then averaged). Independent check: DVL bottom track minus water track (no GPS involved).

| leg | n | c_N [m/s] | c_E [m/s] | |c| | dir to [°] | std N/E | DVL bt−wt: c_N | c_E | |c| | dir [°] |
|---|---|---|---|---|---|---|---|---|---|---|
| Goto1 | 52 | +0.014 | +0.048 | 0.050 | 74 | 0.05/0.04 | -0.019 | +0.020 | 0.027 | 133 |
| Goto2 | 123 | -0.040 | +0.018 | 0.044 | 156 | 0.05/0.04 | -0.041 | +0.009 | 0.042 | 168 |
| Goto3 | 55 | -0.033 | -0.074 | 0.081 | 246 | 0.11/0.05 | -0.008 | -0.051 | 0.051 | 262 |
| Goto4 | 118 | +0.082 | -0.052 | 0.097 | 328 | 0.07/0.07 | +0.038 | +0.006 | 0.039 | 9 |
| Goto5 | 50 | -0.053 | +0.029 | 0.061 | 152 | 0.06/0.07 | -0.051 | -0.006 | 0.051 | 186 |
| Goto6 | 122 | -0.013 | -0.063 | 0.064 | 258 | 0.09/0.06 | +0.001 | -0.052 | 0.052 | 271 |
| Goto7 | 52 | +0.102 | -0.085 | 0.133 | 320 | 0.09/0.08 | +0.033 | -0.002 | 0.033 | 357 |
| Goto8 | 54 | +0.027 | -0.050 | 0.057 | 298 | 0.03/0.04 | +0.027 | -0.039 | 0.048 | 305 |
| **all** | 784 | +0.004 | -0.018 | 0.019 | 282 | | -0.003 | -0.012 | 0.013 | 258 |

- Per-leg spread of the GPS-based estimate: std of c_N = 0.057, c_E = 0.052 m/s; range |c| 0.044–0.133 m/s. Per-leg spread of the DVL-only estimate: std 0.034/0.029 m/s.
- Mean over legs of the GPS-based estimate: (+0.011, -0.029) m/s; DVL-only: (-0.002, -0.014) m/s.

Joint fits over all legs, model v_GPS = c + s·Rz(δ)·v_in (Gauss-Newton; se = 1σ from residuals):

| input | params | c_N | c_E | δ [°] | s | residual RMS [m/s] |
|---|---|---|---|---|---|---|
| water track | cN+cE | +0.004±0.005 | -0.018±0.005 | +0.00 | 1.000 | 0.179 |
| water track | cN+cE+delta_deg | +0.004±0.005 | -0.018±0.005 | +0.09±0.17 | 1.000 | 0.179 |
| water track | cN+cE+delta_deg+scale | +0.003±0.004 | -0.019±0.004 | +0.09±0.16 | 0.965±0.003 | 0.171 |
| bottom track | cN+cE+delta_deg+scale | +0.006±0.004 | -0.006±0.004 | +0.03±0.16 | 0.992±0.003 | 0.166 |
| RPM×1.3e-3 | cN+cE+delta_deg+scale | -0.011±0.005 | -0.058±0.005 | -0.08±0.20 | 0.841±0.003 | 0.209 |
| water track, raw AHRS yaw (no declination) | cN+cE | +0.008±0.010 | -0.022±0.010 | +0.00 | 1.000 | 0.386 |
| water track, raw AHRS yaw (no declination) | cN+cE+delta_deg+scale | +0.003±0.004 | -0.019±0.004 | +12.81±0.17 | 0.965±0.003 | 0.172 |

- Bottom-track row: with GPS as truth, δ is the residual heading bias of DUNE's heading and s the DVL scale error (the current cancels because both are over-ground velocities).
- Raw-AHRS rows show what happens if the declination is not applied: a c-only fit returns a spurious ~0.4 m/s 'current' that rotates with the vehicle, while the δ fit recovers the declination.
- Water-track rows: the extra parameters (δ, s) are identifiable only if they lower the residual RMS noticeably relative to the c-only fit and their 1σ excludes 0/1.

## 4f. Synthetic GPS outages: dead reckoning drift

Dead reckoning restarted from the GPS position every 10 s; drift = |DR − GPS| after 2, 5 and 10 min (windows overlap, so the n are not independent):

| DR input | window | n windows | median drift [m] | 95th pct [m] | max [m] |
|---|---|---|---|---|---|
| water track | 2 min | 67 | 4.7 | 7.8 | 12.0 |
| water track | 5 min | 49 | 5.8 | 12.9 | 14.7 |
| water track | 10 min | 19 | 8.5 | 18.3 | 19.0 |
| bottom track | 2 min | 67 | 2.2 | 4.2 | 8.1 |
| bottom track | 5 min | 49 | 3.2 | 5.3 | 6.0 |
| bottom track | 10 min | 19 | 4.3 | 6.8 | 7.0 |
| RPM x 1.3e-3 | 2 min | 67 | 23.4 | 33.9 | 34.4 |
| RPM x 1.3e-3 | 5 min | 49 | 25.7 | 50.9 | 58.5 |
| RPM x 1.3e-3 | 10 min | 19 | 40.2 | 65.5 | 69.8 |
| RPM x fitted k | 2 min | 67 | 5.8 | 12.0 | 16.7 |
| RPM x fitted k | 5 min | 49 | 14.7 | 17.5 | 18.7 |
| RPM x fitted k | 10 min | 19 | 28.5 | 32.1 | 32.2 |
| water track + fitted (δ, s, c) | 2 min | 67 | 2.3 | 5.7 | 7.2 |
| water track + fitted (δ, s, c) | 5 min | 49 | 2.0 | 5.4 | 7.2 |
| water track + fitted (δ, s, c) | 10 min | 19 | 3.4 | 6.2 | 7.6 |
| water track, raw AHRS yaw (no declination) | 2 min | 67 | 28.1 | 42.5 | 49.7 |
| water track, raw AHRS yaw (no declination) | 5 min | 49 | 25.6 | 55.4 | 59.4 |
| water track, raw AHRS yaw (no declination) | 10 min | 19 | 26.6 | 62.7 | 68.8 |

- All variants use DUNE's heading (AHRS + declination) except the last. 'water track' is the realistic underwater case without a current estimate; 'bottom track' is what DUNE integrates when the DVL has bottom lock; 'RPM' is the fallback without DVL; the fitted variant applies δ=+0.09°, s=0.965, c=(+0.003,-0.019) from 4e; the raw-AHRS variant shows the drift if the declination were not applied.