# Feasibility report: amortized inference of navigation error from the Svalbard AUV logs

Scope: data feasibility only. Nothing was simulated or trained. All numbers come from
`analysis/*/results/*.md` (scripts in `analysis/scripts/`, rerun with `run_all.sh`).

## 1. Bottom line

The idea holds up, but not in the form written. What the data supports:

* **Star mission (Marie, surface, 13 min, 8 legs on 6 headings)**: excellent. 1 Hz GPS with
  hacc 1.2 m for 100 % of the log, 5 Hz DVL bottom *and* water track (98 % valid, seabed at
  ~60 m), 50 Hz AHRS, 10 Hz RPM. Heading bias, DVL scale, RPM-to-speed factor and current are all
  identifiable from it, with 1σ of 0.17° on the heading bias and 0.003 on scale.
* **The dominant "navigation error" parameters are not the ones in the proposal.** Heading bias
  on Marie is 0.03–0.09° ± 0.17° (DUNE already applies a 12.7° declination that the GPS course
  confirms to 0.01°). The current at the site was 0.02 m/s. What actually drives Marie's
  dead-reckoning drift is the DVL water-track scale (0.965) and, without DVL lock, the RPM
  speed model (16 % too fast). On Thor the picture is different: a residual heading error of
  about −4 to −8°, no bottom lock at all, and an RPM model 12 % too fast, producing
  **290 m and 340 m** position jumps after 21 and 25 min submerged.
* **USBL: nothing.** No `Usbl*`, `Lbl*` or range message exists in any vehicle log. The vehicles
  only received 15 (Marie, star), 3 (Marie, sidescan) and 0 (Thor) acoustic "pos" text requests
  from the ship gateway `manta-ntnu-4`. The `USBL Node -- Enabled = false` config confirms the
  vehicles never expected fixes. Design item 2 (USBL characterisation) and the "USBL in between"
  part of item 3 are dead unless you obtain the ship-side Neptus/Manta logs.
* **Dive-to-resurface validation points: 3 in total** (Marie 1, Thor 2), and Marie's single one is
  measured against a fix with hacc 10 m because the log ends 3 s after resurfacing.

Recommended reframing (section 7): infer the dead-reckoning error parameters
θ = (heading bias, speed scale, current N/E, velocity-noise level) from short surface windows,
push the posterior through the recorded dive to get a georeferencing-uncertainty envelope for the
sidescan lines, and use Thor and the raw-AHRS case as the misspecification/OOD tier. Same
pipeline, same SBC and Mahalanobis checks, but the current becomes a nuisance parameter that the
data say is ~0, not the headline.

## 2. What the logs actually are (discrepancies with the brief)

| log | vehicle (Config.ini, Announce, LoggingControl) | DUNE / IMC | when (UTC) | where | what |
|---|---|---|---|---|---|
| 101134_20260907_star | **lauv-marie** (not Thor) | 2025.06.03 / 5.5.4.9 | 7 Sept 10:11:35–10:24:45 | 78.662 N 16.89 E = **Adolfbukta, inner Billefjorden** (Nordenskiöldbreen), not Tempelfjorden | surface star, 8 Goto legs |
| 094605_0700926LongYoYo1 | lauv-thor | **2020.11.00 / 5.4.23** (older stack) | 7 Sept 09:46:05–10:39:51 | 78.65–78.66 N, 16.66–16.86 E = **Adolfbukta** (the group report says Tempelfjorden) | 3 surface Goto, YoYo1 (19 min dive), PopUp, Goto, YoYo2 (25 min dive), PopUp |
| 074948_08_09_sidescan | lauv-marie | 2025.06.03 / 5.5.4.9 | 8 Sept 07:49:48–08:24:40 | 78.26 N 15.61 E = Adventfjorden | Elevator to 25 m then 60 m, 9 lawnmower lines at 7 m altitude, PopUp |

* Both vehicles were in Adolfbukta at the same time on 7 Sept, 0.6–2 km apart. The group
  report's placement of Thor in Tempelfjorden is wrong at least for this log (check the other
  Thor logs before reusing that sentence).
* Both Config.ini files of Marie have the same size because they are the same vehicle; Thor's is
  different. The Marie config has Sidescan/Multibeam/CTD(AmlX)/Echo Sounder entities; Thor has
  SmartX CTD, Chlorophyll, Turbidity, EK60. Sonar payloads were skipped.
* Marie's star log was recorded ~50 min after Thor's start; the "star" was almost certainly the
  USBL calibration pattern that the group report says failed. That explains why the ship kept
  sending `pos` requests every ~40 s.
* Clocks: vehicle clocks are GPS-synced; header timestamps lag the GPS UTC of fix by +0.32 s
  (Marie, GPS over TCP) and −0.02 s (Thor). I use the UTC of fix as the epoch. Negligible for
  current estimation, 0.5 m at 1.5 m/s for position matching.
* `EstimatedStreamVelocity` is listed in every logging config but **never dispatched** in any log
  (DUNE's navigation task does not produce it in these versions). No DUNE current baseline
  exists. `NavigationData.bias_psi` is identically 0 (no IMU alignment: AlignmentState =
  NOT_ALIGNED on Marie, NOT_SUPPORTED on Thor).
* `EulerAngles.psi == psi_magnetic` in all logs. DUNE adds a constant declination internally:
  EstimatedState.psi − AHRS psi = 12.72° (Marie 7 Sept), 12.74° (Marie 8 Sept), **14.03° (Thor)**.
  The star fit confirms the Marie offset to 0.1° (residual +0.09 ± 0.16°). The size is that of the local
  magnetic declination: WMM2025 gives 14.02° at the star site on 7 Sept, 14.00° at Thor's site and
  12.86° at the sidescan site on 8 Sept (`scripts/wmm_check.py`). Thor's offset matches the model;
  Marie's is 1.3° smaller at the star site (0.1° at the sidescan site) and the reason was not
  established. Thor's residual heading error (−4 to −8°) therefore does not come from the declination.
* The receiver keeps emitting "valid" positions at 60 m depth with hacc of hundreds of metres and
  3 satellites (138 such fixes on the sidescan log). DUNE rejects them (`GpsFixRejection`). Do not
  use the VALID_POS bit alone.
* Thor's DVL water track is flagged invalid 99.7 % of the time but the numbers are physical
  (correlation 0.92 with RPM, ratio 0.89 to the RPM model). DUNE ignored them and ran on RPM.

## 3. Answers to the specific questions

### 4a. Star mission

* Surface the whole time: yes. VehicleMedium = WATER for all 790 samples; CTD depth −0.29 m
  (sensor above the waterline), DVL depth 0.15 m.
* GPS: 790 fixes, 1.00 Hz, no gaps, 100 % VALID_POS, 100 % pass DUNE's hacc<15/hdop<4 rule,
  100 % hacc < 5 m (median 1.2 m, hdop 0.63, 17 satellites, standalone fix type, no RTK).
  COG/SOG valid on 99.2 %.
* DVL: bottom track valid 98.3 % (34 dropouts, longest 0.7 s), water track 98.1 %, altitude
  33–73 m (median 60.5 m). So both DVL bottom lock and water track exist at the surface; RPM is
  a third, independent speed source (median 1363 rpm).
* Legs (DUNE heading, steady part): 292, 320, 83, 195, 325, 80, 196, 122° → six distinct
  directions, 70–143 s each, 104–212 m each, SOG 1.47–1.63 m/s. Good geometry for separating
  an earth-fixed current from body-fixed biases.

### 4b. USBL

Zero acoustic position fixes in any log. 17 acoustic frames received during the star (15 `pos`
requests), 28 state reports transmitted. USBL error vs GPS cannot be computed from the vehicle
side. If the ship's Manta/Neptus log exists it will contain `UsblFixExtended`/`UsblPositionExtended`
(or at least the raw ranges) and this question becomes answerable; ask for
`manta-ntnu-4` logs and the Neptus console log of 7 Sept 10:11–10:25 UTC.

### 4c. Diving missions

Marie sidescan (1 dive, medium UNDERWATER 07:50:25–08:24:37, 34.2 min, GPS gap 34.2 min):

| quantity | value |
|---|---|
| DUNE estimate just before first accepted fix − that fix | ΔN +16.3, ΔE +11.4, **19.9 m** (fix hacc 10 m; DUNE's own log says 19.6 m / 2731 m = 0.72 %) |
| first fix with hacc < 5 m | none: the log ends 3 s after resurfacing (next log `20260908/082440` is needed) |
| DVL bottom lock while submerged | 98.6 %, 8 dropouts, longest 20.2 s; altitude median 7.0 m; depth max 61.3 m |
| USBL fixes / acoustic frames received while submerged | 0 / 6 (all in the first 5 min) |
| DUNE σ_x at end of dive | 1.0 m (max 6.6 m) — the filter's own uncertainty is far below the 20 m jump |
| my DR closure over the dive: bottom track / water track / RPM | 41 m (1.5 %) / 23 m (0.8 %) / 75 m (2.4 %) — endpoints have hacc 13 and 10 m, so ±20 m on all of these |

Thor long yoyo (2 dives, no bottom lock, filter ran on RPM×1.3e-3):

| dive | submerged | first DUNE-accepted fix (hacc) | DUNE jump | my RPM DR closure | water-track DR closure | water track + own surface fit |
|---|---|---|---|---|---|---|
| 1 | 19.0 min (GPS gap 20.8) | 15 m | **291.6 m** (15 % of 1.9 km) | 339 m | 224 m | 66 m |
| 2 | 24.7 min (GPS gap 24.9) | 13 m | **340.5 m** (16 % of 2.1 km) | 437 m | 298 m | 133 m |

DUNE's log lines "estimating error of 0.03 % (0.6/1920.7 m)" for Thor are wrong by three orders
of magnitude (they are evaluated after the correction); the 20 Hz EstimatedState shows the real
292/340 m steps. Do not quote those log lines.

### 4d. DUNE current estimate

Not logged (see section 2). The DVL bottom-minus-water track is the available current measurement:
0.013 m/s over the star (per-leg 0.03–0.05 m/s, directions scattered), i.e. below the water-track
noise. The GPS-minus-water-track estimate agrees: 0.019 m/s overall.

### 4e. Least-squares current, star mission

Per-leg c = mean(v_GPS − R·v_watertrack) with DUNE heading: |c| = 0.04–0.13 m/s, directions all
over the compass, std across legs 0.057/0.052 m/s; overall (+0.004, −0.018) m/s ± 0.005. Joint
Gauss-Newton fits v_GPS = c + s·Rz(δ)·v_in over 784 epochs:

| input | c_N | c_E | δ | s | residual RMS |
|---|---|---|---|---|---|
| water track, c only | +0.004±0.005 | −0.018±0.005 | – | – | 0.179 m/s |
| water track, c+δ+s | +0.003±0.004 | −0.019±0.004 | +0.09±0.16° | 0.965±0.003 | 0.171 |
| bottom track, c+δ+s | +0.006 | −0.006 | +0.03±0.16° | 0.992±0.003 | 0.166 |
| RPM×1.3e-3, c+δ+s | −0.011 | −0.058 | −0.08±0.20° | 0.841±0.003 (k = 1.09e-3) | 0.209 |
| water track, **raw AHRS yaw**, c only | +0.008 | −0.022 | – | – | 0.386 |
| water track, raw AHRS yaw, c+δ+s | +0.003 | −0.019 | **+12.81±0.17°** | 0.965 | 0.172 |

Per-leg estimates are consistent (they scatter around zero at the level of the water-track noise,
`plots/current_per_leg.png`). The raw-AHRS rows are the cautionary example: with the declination
omitted, a current-only model returns a spurious 0.33–0.48 m/s "current" on every leg that rotates
with the vehicle, and only the heading-diverse star exposes it. That is exactly the
misspecification mechanism the paper can be built around.

### 4f. Synthetic outages (DR restarted every 10 s, DUNE heading)

| DR input | 2 min median / max | 5 min | 10 min |
|---|---|---|---|
| DVL water track (realistic, no current estimate) | 4.7 / 12.0 m | 5.8 / 14.7 | 8.5 / 19.0 |
| DVL bottom track | 2.2 / 8.1 | 3.2 / 6.0 | 4.3 / 7.0 |
| RPM × 1.3e-3 (config value) | 23 / 34 | 26 / 59 | 40 / 70 |
| RPM × fitted k | 5.8 / 17 | 15 / 19 | 28 / 32 |
| water track + fitted (δ, s, c) | 2.3 / 7.2 | 2.0 / 7.2 | 3.4 / 7.6 |
| water track, raw AHRS yaw (no declination) | 28 / 50 | 26 / 59 | 27 / 69 |

Only 19 non-overlapping-ish 10-min windows exist (the mission is 13 min), so the 10-min numbers
are weak. The message: on Marie, a calibrated (s, c) turns a 0.9 % drift into 0.35 %; the RPM
fallback is 4–5 % of distance unless k is calibrated.

## 4. What is possible with this data

1. Amortized posterior over θ = (δ, s, c_N, c_E, σ) from surface windows, trained on a kinematic
   simulator, validated on the 8 star legs and on 67 synthetic-outage windows (drift prediction vs
   observed), with SBC on the simulator. Truth on the star is known to ±0.17° / ±0.003 / ±0.005 m/s.
2. Propagation of that posterior through the recorded sidescan dive (the actual heading, water-
   track and RPM sequences) to give a per-sample georeferencing uncertainty for the 9 sidescan
   lines, with one closure check (19.9 ± 10 m) and a sensitivity statement (5.7 m per degree of
   heading bias at the far end of the pattern; 8 m per line per 3.5 % speed-scale error).
3. A genuine misspecification test without inventing anything: apply the Marie-trained network to
   Thor windows (no bottom lock, invalid-flagged water track, older DUNE, −4 to −8° heading
   error, 12 % RPM error) and to Marie windows with the raw AHRS heading. Both should trip the
   Mahalanobis check; the raw-AHRS case is the "silent confident wrong posterior" example if it
   doesn't. Thor's two 290/340 m closures are the ground truth that the Marie model is wrong there.
4. Thor's own surface runs (466 GPS epochs, 3 runs) give a weak in-sample calibration (δ −3.9°,
   s 0.98 for water track; s 0.88 for RPM) that reduces the dive closures from 224→66 m and
   298→133 m. That is a second, poorer, calibration set and a nice contrast to the star.

## 5. What is not possible

* Any USBL statement (no fixes anywhere).
* A posterior on a *non-zero* current validated against truth: the current was ~0.02 m/s during the
  star. The current parameter will only ever be shown to be "consistent with zero" here.
* A dive-by-dive validation curve with several Marie dives: there is one Marie dive, its end-fix
  has 10 m accuracy, and its closure error (20 m over 2.7 km) is at the level of the endpoint
  uncertainty. It is a sanity check, not a validation set.
* Reproducing DUNE's EKF exactly: my plain integrations close 20–40 m differently from DUNE on the
  sidescan dive. Fine for a kinematic-tier simulator, but the "observation" you feed the network
  must be raw sensor streams, not EstimatedState, otherwise you are learning DUNE, not physics.
* Sub-metre statements: standalone GPS, hacc 1.2 m at best, 10–15 m at reacquisition.

## 6. Biggest risks to the paper

1. **The headline parameter is ~0.** Reviewers will ask why you infer a current that is
   indistinguishable from zero. Answer by promoting δ, s and k to the headline (they are large on
   Thor and on the raw-AHRS case), and keep c as a nuisance parameter with a prior wide enough to
   be interesting.
2. **Identifiability depends on heading diversity.** On Thor's runs (all ~290–330°) δ and c are
   confounded (the fit moves 0.17 m/s of "current" into 3.9° of δ). Your identifiability gate must
   include the heading sequence as part of x, and the network must learn to widen the posterior on
   straight runs. That is a good result if SBC shows it; a silent failure if it doesn't.
3. **One vehicle, one day, one dive.** Any statement about transfer from surface to underwater
   rests on 1 (Marie) + 2 (Thor) points. More Marie dive logs would change this (section 8).
4. **The simulator must model the real failure modes:** flagged-invalid DVL, dropouts (20 s on
   the dive), pitch of up to 21° during the elevator (the full rotation matters), RPM-speed
   nonlinearity, hacc ramp at reacquisition. Purely kinematic is right, but these switches are the
   misspecification you'll hit.
5. Deadline. The lecture slides say the extended abstract is 6–8 pages, IMRAD, "due four weeks
   after exam" (exam 19 Sept → ~17 Oct), but the assessment table on the same deck says
   "deadline 1–2 weeks after the written exam". Confirm with the course responsible now. There is
   no template in the course folder; the outline PDF you pointed to is the group-report outline.

## 7. Recommended SBI setup (given what is logged)

**θ (5–6 parameters, all identifiable from a star and all with measured truth):**

| parameter | prior (suggested, from data) | truth on star | note |
|---|---|---|---|
| δ heading bias [°] | U(−15, 15) | +0.09 ± 0.16 | covers raw-AHRS (+12.8) and Thor (−4…−8) |
| s speed scale (DVL water track) or k (RPM, m/s per rpm) | U(0.8, 1.1) or U(0.9e-3, 1.5e-3) | 0.965 / 1.09e-3 | one or the other depending on which speed source the window uses; flag in x |
| c_N, c_E current [m/s] | U(−0.4, 0.4) each | +0.003, −0.019 | Cartesian, not polar (as in your DT8122 code) |
| σ_v velocity noise [m/s] | log-U(0.05, 0.5) | 0.17 (residual RMS) | absorbs waves/sideslip |
| (optional) p_drop DVL dropout probability | U(0, 0.3) | 0.017 | only if you include the invalid-flag channel |

**x (one window, fixed length, native-ish rate):** 120 s at 1 Hz (or 2 Hz) with channels
`[cos ψ, sin ψ, u_wt, v_wt, rpm/1000, v_N^gps, v_E^gps, dvl_valid, gps_valid]`, where ψ is the
DUNE heading (AHRS + declination) — or the raw AHRS heading if you want the declination to be part
of what the network must infer. At the surface all channels are present; for an underwater window
set the GPS channels to 0 with `gps_valid = 0`, so the same network handles both and the posterior
simply widens. Optionally append the bottom-track `u_bt, v_bt` with its own valid flag: on Marie
it is present underwater and makes c identifiable there too (bt − wt = current). Standardise with
training statistics; keep the summary network a time-series transformer as before.

**Simulator (kinematic, seconds per draw):** sample θ; take a heading programme either replayed
from the real logs (best: it reproduces the exact star and lawnmower geometry) or from a random
piecewise-constant heading with turns; true water speed from a commanded speed profile; over-
ground velocity = R(ψ_true)·[u,0] + c; measurements: ψ_meas = ψ_true − δ + n, water track =
[u,0]/s + n, bottom track = R(−ψ_meas)·(over-ground) + n, GPS velocity = over-ground + n_gps,
dropouts via p_drop. Position DR is then a deterministic function of (x, θ), so the georeferencing
uncertainty is a push-forward of posterior samples through the recorded window sequence.

**Validation tiers:** (i) SBC on the simulator; (ii) star legs and synthetic-outage windows
(posterior-predicted drift vs observed drift distribution, table 4f); (iii) sidescan dive closure
(19.9 ± 10 m) and the uncertainty envelope along the lines; (iv) OOD/misspecification: Thor
windows and raw-AHRS windows through the Mahalanobis check, with Thor's 292/340 m closures as
the consequence of ignoring the flag. DUNE-simulator (`dune -c lauv-simulator-1`) can later sit
between (i) and (ii) as your intermediate tier, but it is not needed for the paper.

## 8. Extra data that would materially help (ask now)

1. **`20260908/082440` and the other Marie logs of 8 Sept** (helicopter wreck ×2 patterns,
   shipwreck, test runs): each adds a dive/resurface pair and the post-resurface GPS with hacc < 5 m
   that this log lacks. This is the single most valuable addition (3 → ~6 Marie closures).
2. **Ship-side logs** (Neptus console / `manta-ntnu-4` LSF) of 7 Sept 10:11–10:25 and 8 Sept:
   the only place USBL fixes or ranges can exist.
3. Thor's remaining yoyo legs of 7 Sept: 3 more dive pairs and, if any leg ran across-fjord,
   heading diversity for Thor's surface calibration.
4. Any Marie compass-calibration or second star/USBL pattern log.

## 9. File index

```
analysis/<log>/inventory.md            vehicle, span, clock check, message counts/rates, entities
analysis/<log>/csv/*.csv               native-rate tables (43–44 message types per log)
analysis/101134_20260907_star/results/star_results.md|json   4a, 4b, 4e, 4f
analysis/101134_20260907_star/plots/   track, depth, heading, gps_validity, synthetic_outage_drift,
                                       current_per_leg, velocity_residuals
analysis/074948_08_09_sidescan/results/dive_results.md|json   4c (Marie)
analysis/094605_0700926LongYoYo1/results/dive_results.md|json 4c (Thor)
analysis/<dive log>/plots/             track (+ own DR overlays), depth (+ seabed), heading, gps_validity
analysis/scripts/                      lsf_reader.py, extract_logs.py, common.py, analyze_star.py,
                                       analyze_dives.py, run_all.sh, README.md, requirements.txt
```
