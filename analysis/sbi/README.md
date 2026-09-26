# Amortized inference of the dead-reckoning error budget

Self-contained pipeline (nothing imported from other projects). It learns a posterior over
theta = (heading bias, speed scale, current N, current E, log10 velocity noise) from 120 s
windows of AUV sensor data, using a kinematic simulator and BayesFlow (JAX backend).

```
config.py        window definition, parameter names and priors, simulator noise settings, paths
simulator.py     kinematic simulator + dead_reckon() (nominal or corrected)
make_windows.py  real 1 Hz windows from analysis/<log>/csv/*.csv -> data/windows.npz,
                 heading/rpm programmes for the simulator -> data/programmes.npz
generate_data.py simulation budget -> data/train.npz, data/val.npz
train.py         TimeSeriesTransformer summary net + CouplingFlow -> models/posterior.keras, stats.npz
validate.py      SBC, recovery, posterior on the real star windows, predicted vs observed drift
propagate.py     posterior pushed through the recorded sidescan dive -> uncertainty envelope
propagate_thor.py same for Thor's two dives (delta from its surface windows, s and c from its dive windows)
detect.py        Mahalanobis misspecification check in summary space on all real window sets
heading_bias_check.py  per-window heading bias from bottom track vs GPS, compared with the posterior (post hoc)
run_all.sh       everything in order (~2 h on a 20-core CPU, dominated by training)
v1/              frozen first run (fixed GPS noise 0.05 m/s, bottom-track noise tied to sigma_v, sigma prior from 0.05):
                 models, results, plots and the config/simulator/scripts that produced them
```

## Setup

```bash
cd field_work_data/analysis/sbi
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run_all.sh
```

`extract_logs.py` and `analyze_*.py` in `../scripts` must have been run first: the windows are
built from their CSV tables and the reference parameter values come from their JSON results.

## Outputs

* `data/windows.npz`: real windows per set (`star`, `star_raw`, `sidescan_dive`, `thor_surface`,
  `thor_dive`), each `(N, 120, 12)` with the channel list, start times and reference theta.
* `models/posterior.keras`, `models/stats.npz`, `models/history.npz`.
* `results/validation.{md,json}`, `results/propagation.{md,json}`, `results/detection.{md,json}`.
* `plots/sbc_recovery.png`, `posterior_star_windows.png`, `drift_pred_vs_obs.png`,
  `sidescan_envelope.png`, `mahalanobis.png`, `training_loss.png`.

## Observation window (12 channels at 1 Hz)

`cos_psi, sin_psi` (sensed heading), `wt_u, wt_v` (DVL water track, body frame), `rpm_k`
(rpm/1000), `gps_vn, gps_ve` (GPS velocity over ground), `m_dvl, m_gps` (masks), `bt_u, bt_v,
m_bt` (DVL bottom track and mask). Absent channels are zero with mask 0, in simulation and in
the real windows alike.

## Simulator

See the docstring of `simulator.py`. Nuisances that are sampled but not inferred: rpm-to-speed
factor, DVL dropout probability, availability of GPS and bottom track, AR(1) sway.
Heading/rpm programmes are half replayed from the field logs (rotated randomly), half synthetic.

## Version history (both are reported in the paper)

* **v1** used a fixed GPS velocity noise of 0.05 m/s, a bottom-track noise tied to sigma_v and a
  sigma_v prior starting at 0.05 m/s. It was well calibrated on simulations but overconfident on the
  real star windows: the real DVL is self-consistent to 0.03 m/s while GPS and DVL disagree by
  0.15 m/s per axis, and the real DVL noise lay below the prior. See `v1/results/`.
* **v2** (current files) samples the GPS noise (0.03-0.25 m/s) and the bottom-track noise
  (0.01-0.15 m/s) per window as broad nuisances, and starts the sigma_v prior at 0.01 m/s.
  The nuisance ranges are broad on purpose, not tuned to the star.
* The propagation step was also changed between the two: carrying the star's current to another site
  and day is invalid, so v2 takes the heading bias from the star and speed scale and current from the
  dive's own windows (variant B), keeping the carried-over variant (A) for comparison.

All posterior sampling uses a fixed seed (`common_sbi.posterior(..., seed=0)`), so the numbers in
`results/*.md` are reproducible from the saved model.
