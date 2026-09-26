"""
Independent per-window heading bias on the star, and comparison with the posterior.

Bottom track and GPS velocity are both over-ground, so the angle that rotates the heading-rotated
bottom-track vector onto the GPS vector is the heading bias delta of that window, whatever the current
or the speed scale. It is computed per 120 s window (speed-weighted: atan2(sum cross, sum dot)) and
compared with the posterior of delta. NOTE: this diagnostic was added after seeing that the posterior
under-covered the single all-leg reference; it is post hoc and is reported as such.
The window-level estimate has its own noise of about 0.5 deg (GPS-DVL discrepancy 0.15 m/s per axis,
1.5 m/s speed, 120 samples).
"""
import numpy as np
import matplotlib.pyplot as plt

from config import RESULTS, PLOTS
from simulator import IDX
from common_sbi import load_model, posterior, load_windows, COL, GREY

W = load_windows(); x = W["star"]["x"]; ref = W["star"]["ref"][0]
psi = np.arctan2(x[:, :, IDX["sin_psi"]], x[:, :, IDX["cos_psi"]])
bn = np.cos(psi) * x[:, :, IDX["bt_u"]] - np.sin(psi) * x[:, :, IDX["bt_v"]]
be = np.sin(psi) * x[:, :, IDX["bt_u"]] + np.cos(psi) * x[:, :, IDX["bt_v"]]
gn, ge = x[:, :, IDX["gps_vn"]], x[:, :, IDX["gps_ve"]]
dw = np.degrees(np.arctan2((bn * ge - be * gn).sum(1), (bn * gn + be * ge).sum(1)))
appr, stats = load_model(); ps = posterior(appr, stats, x, n=500)
pm = ps[:, :, 0].mean(1); lo, hi = np.percentile(ps[:, :, 0], [5, 95], axis=1)
hd = np.degrees(np.arctan2(np.sin(psi).mean(1), np.cos(psi).mean(1))) % 360
inside = (dw >= lo) & (dw <= hi)
md = ["# Per-window heading bias on the star: independent estimate vs posterior\n",
      f"- Window-level delta from bottom track vs GPS: mean {dw.mean():+.2f}°, std {dw.std():.2f}°, range {dw.min():+.1f} to {dw.max():+.1f}° over {len(dw)} windows.",
      f"- Posterior mean delta: mean {pm.mean():+.2f}°, std {pm.std():.2f}°, range {pm.min():+.1f} to {pm.max():+.1f}°.",
      f"- Correlation of the two across windows: {np.corrcoef(dw, pm)[0,1]:.2f}; mean difference (posterior − window estimate) {np.mean(pm-dw):+.2f}°, rms {np.sqrt(np.mean((pm-dw)**2)):.2f}°.",
      f"- Window-level estimate inside the posterior 90 % interval: {inside.sum()}/{len(dw)} ({inside.mean()*100:.0f} %).",
      f"- Single all-leg reference used in validation.md: {ref:+.2f}°; it lies inside the posterior 90 % interval in {(((ref>=lo)&(ref<=hi)).sum())}/{len(dw)} windows.",
      "- Post hoc diagnostic (see script docstring)."]
(RESULTS / "heading_bias_check.md").write_text("\n".join(md)); print("\n".join(md))
fig, ax = plt.subplots(figsize=(3.4, 2.5))
o = np.argsort(hd)
ax.errorbar(hd[o], pm[o], yerr=[pm[o] - lo[o], hi[o] - pm[o]], fmt="o", ms=3, color=COL[0], ecolor="#c8daf3", elinewidth=1.2, label="posterior (mean, 90 %)")
ax.plot(hd[o], dw[o], "s", ms=3, color=COL[1], label="bottom track vs GPS, per window")
ax.axhline(ref, color=GREY, lw=0.8, ls="--", label="all-leg constant fit")
ax.set_xlabel("mean window heading [deg]", fontsize=8); ax.set_ylabel(r"heading bias $\delta$ [deg]", fontsize=8); ax.tick_params(labelsize=7)
ax.legend(fontsize=6, loc="lower left"); fig.tight_layout(pad=0.4); fig.savefig(PLOTS / "heading_bias_check.png"); plt.close(fig)
