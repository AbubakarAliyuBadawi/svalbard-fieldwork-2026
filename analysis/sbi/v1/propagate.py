"""
Push the star-calibrated posterior through the recorded sidescan dive.

The whole submerged interval of the sidescan log is rebuilt at 1 Hz (same channels as the windows).
Nominal dead reckoning = sensed (DUNE) heading + DVL water track, no corrections.
For each posterior sample theta (pooled over the 23 star windows) the corrected dead reckoning
v = s R(psi + delta) v_wt + c is integrated over the dive; the difference to the nominal track is
the position error the nominal DR would have if theta were true. Reported: median and 90 %
envelope of |error| along the dive, and the predicted closure distribution at resurfacing against
the observed closure of the same water-track DR (23.3 m) and DUNE's own correction (19.9 m).
"""
from __future__ import annotations

import json
import numpy as np
import matplotlib.pyplot as plt

from config import ANALYSIS, LOGS, RESULTS, PLOTS
from make_windows import series_1hz
from simulator import IDX
from common_sbi import load_model, posterior, load_windows, COL, GREY

N_PER_WINDOW = 40
rng = np.random.default_rng(1)
dive_res = json.loads((ANALYSIS / LOGS["sidescan"] / "results" / "dive_results.json").read_text())
obs_wt = dive_res["dive1"]["closures"]["water track"]["abs"]
obs_dune = dive_res["dive1"]["jump_abs"]

appr, stats = load_model()
W = load_windows()
ps = posterior(appr, stats, W["star"]["x"], n=N_PER_WINDOW)     # (23, 40, 5)
theta_pool = ps.reshape(-1, 5)

x, t, ok, med = series_1hz(LOGS["sidescan"], "es")
m = (med == 3)
i0, i1 = np.argmax(m), len(m) - np.argmax(m[::-1])
xd = x[i0:i1]; td = t[i0:i1]
psi = np.arctan2(xd[:, IDX["sin_psi"]], xd[:, IDX["cos_psi"]])
u, v, mk = xd[:, IDX["wt_u"]].copy(), xd[:, IDX["wt_v"]].copy(), xd[:, IDX["m_dvl"]]
last = (0.0, 0.0)
for k in range(len(u)):
    if mk[k] > 0.5: last = (u[k], v[k])
    else: u[k], v[k] = last


def dr(theta=None):
    if theta is None:
        d, s, c = 0.0, 1.0, np.zeros(2)
    else:
        d, s, c = np.radians(theta[0]), theta[1], theta[2:4]
    a = psi + d
    vn = s * (np.cos(a) * u - np.sin(a) * v) + c[0]; ve = s * (np.sin(a) * u + np.cos(a) * v) + c[1]
    return np.column_stack([np.cumsum(vn), np.cumsum(ve)])


nom = dr()
errs = np.array([np.hypot(*(nom - dr(th)).T) for th in theta_pool])     # (S, N)
med_e, lo_e, hi_e = np.median(errs, 0), np.percentile(errs, 5, 0), np.percentile(errs, 95, 0)
closure = errs[:, -1]
tt = td - td[0]
md = []
say = lambda s="": (print(s), md.append(s))
say("# Posterior propagated through the sidescan dive\n")
say(f"- Submerged interval {len(td)} s, {len(theta_pool)} posterior samples pooled from the 23 star windows.")
say(f"- Predicted error of the nominal water-track DR: at 10 min median {med_e[600]:.1f} m (90 %: {lo_e[600]:.1f}–{hi_e[600]:.1f}); at the end median {med_e[-1]:.1f} m (90 %: {lo_e[-1]:.1f}–{hi_e[-1]:.1f}); maximum of the median along the dive {med_e.max():.1f} m.")
say(f"- Observed closure of the same water-track DR at resurfacing: {obs_wt:.1f} m; DUNE's own correction: {obs_dune:.1f} m. Percentile of the observed water-track closure in the predicted closure distribution: {np.mean(closure <= obs_wt)*100:.0f} %.")
R = dict(n_samples=int(len(theta_pool)), pred_end_median=float(med_e[-1]), pred_end_lo=float(lo_e[-1]), pred_end_hi=float(hi_e[-1]),
         pred_10min_median=float(med_e[600]), pred_max_median=float(med_e.max()), obs_wt_closure=obs_wt, obs_dune_closure=obs_dune,
         obs_percentile=float(np.mean(closure <= obs_wt)))
(RESULTS / "propagation.json").write_text(json.dumps(R, indent=1)); (RESULTS / "propagation.md").write_text("\n".join(md))

fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw=dict(width_ratios=[1.3, 1]))
ax = axs[0]
ax.plot(nom[:, 1], nom[:, 0], color=GREY, lw=1.0, label="nominal water-track DR (sensed heading)")
sel = rng.choice(len(theta_pool), 150, replace=False)
for k in sel:
    p = dr(theta_pool[k]); ax.plot(p[:, 1], p[:, 0], color=COL[0], lw=0.3, alpha=0.25)
ax.plot([], [], color=COL[0], lw=1, label="150 posterior-corrected tracks")
ax.set_aspect("equal"); ax.set_xlabel("east [m]"); ax.set_ylabel("north [m]"); ax.legend(fontsize=7, loc="lower left")
ax.set_title("Sidescan dive: spread of corrected tracks", fontsize=9)
ax = axs[1]
ax.fill_between(tt / 60, lo_e, hi_e, color="#c8daf3", label="90 % envelope"); ax.plot(tt / 60, med_e, color=COL[0], label="median")
ax.axhline(obs_wt, color=COL[1], lw=1.2, label=f"observed water-track closure {obs_wt:.0f} m")
ax.axhline(obs_dune, color=COL[2], lw=1.2, ls="--", label=f"DUNE correction {obs_dune:.0f} m")
ax.set_xlabel("time since dive [min]"); ax.set_ylabel("predicted |error| of nominal DR [m]"); ax.legend(fontsize=7)
ax.set_title("Predicted position error along the dive", fontsize=9)
fig.tight_layout(); fig.savefig(PLOTS / "sidescan_envelope.png"); plt.close(fig)
print("wrote", RESULTS / "propagation.md")
