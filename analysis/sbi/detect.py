"""
Misspecification detection in summary space.

The summary network maps a window to a 32-d vector h. The reference distribution of h is
estimated from 4000 training simulations (mean, covariance); the null distribution of the
squared Mahalanobis distance d^2 comes from the held-out validation simulations, and the
threshold is its 99th percentile. Real window sets are then scored: fraction flagged and median
d^2. For sets with a reference theta, the posterior coverage is also reported, split into flagged
and unflagged windows, so the reader can see whether flagging coincides with a wrong posterior.
"""
from __future__ import annotations

import json
import numpy as np
import matplotlib.pyplot as plt

from config import DATA, RESULTS, PLOTS, THETA
from common_sbi import load_model, posterior, summaries, load_windows, COL, GREY

appr, stats = load_model()
tr = np.load(DATA / "train.npz"); va = np.load(DATA / "val.npz")
h_ref = summaries(appr, stats, tr["x"][:4000])
mu = h_ref.mean(0); cov = np.cov(h_ref.T) + 1e-6 * np.eye(h_ref.shape[1]); icov = np.linalg.inv(cov)
d2 = lambda h: np.einsum("ij,jk,ik->i", h - mu, icov, h - mu)
d2_null = d2(summaries(appr, stats, va["x"][:2000]))
thr = np.percentile(d2_null, 99)
W = load_windows()
md, R = [], dict(threshold=float(thr), null_median=float(np.median(d2_null)), dim=int(h_ref.shape[1]))
say = lambda s="": (print(s), md.append(s))
say("# Misspecification detection (Mahalanobis distance in summary space)\n")
say(f"Summary dimension {h_ref.shape[1]}; null d² from 2000 held-out simulations: median {np.median(d2_null):.1f}, 99th percentile (threshold) {thr:.1f}.\n")
say("| window set | n | median d² | flagged (d² > threshold) | 90 % coverage of reference, unflagged | flagged |")
say("|---|---|---|---|---|---|")
scores = {}
for k in ["star", "sidescan_dive", "thor_surface", "thor_dive", "star_raw"]:
    x = W[k]["x"]
    if len(x) == 0:
        continue
    s = d2(summaries(appr, stats, x)); flag = s > thr
    ps = posterior(appr, stats, x, n=300)
    lo, hi = np.percentile(ps, 5, 1), np.percentile(ps, 95, 1)
    ref = W[k]["ref"]
    inside = ((ref >= lo) & (ref <= hi))[:, :4]     # (n, 4): delta, s, c_N, c_E (no like-for-like reference for sigma_v)
    cov_un = inside[~flag].mean() if (~flag).any() else np.nan
    cov_fl = inside[flag].mean() if flag.any() else np.nan
    # for the raw-heading set the interesting parameter is delta specifically
    d_in_un = inside[~flag, 0].mean() if (~flag).any() else np.nan
    d_in_fl = inside[flag, 0].mean() if flag.any() else np.nan
    scores[k] = dict(n=int(len(x)), median_d2=float(np.median(s)), flagged_frac=float(flag.mean()), cov_unflagged=float(cov_un), cov_flagged=float(cov_fl),
                     delta_cov_unflagged=float(d_in_un), delta_cov_flagged=float(d_in_fl), d2=s.tolist(),
                     delta_post_median=float(np.median(ps[:, :, 0])), delta_post_lo=float(np.median(lo[:, 0])), delta_post_hi=float(np.median(hi[:, 0])))
    say(f"| {k} | {len(x)} | {np.median(s):.1f} | {flag.mean()*100:.0f} % | {cov_un*100 if np.isfinite(cov_un) else float('nan'):.0f} % (δ: {d_in_un*100 if np.isfinite(d_in_un) else float('nan'):.0f} %) | {cov_fl*100 if np.isfinite(cov_fl) else float('nan'):.0f} % (δ: {d_in_fl*100 if np.isfinite(d_in_fl) else float('nan'):.0f} %) |")
    say(f"|  | | | | posterior δ median {np.median(ps[:, :, 0]):+.2f}° [{np.median(lo[:, 0]):+.2f}, {np.median(hi[:, 0]):+.2f}] vs reference {ref[0]:+.2f}° | |")
R["sets"] = scores
say("\nCoverage = fraction of (window, parameter) pairs whose 90 % interval contains the reference value; 'δ:' the same for the heading bias only.")
(RESULTS / "detection.md").write_text("\n".join(md)); (RESULTS / "detection.json").write_text(json.dumps(R, indent=1))
fig, ax = plt.subplots(figsize=(7, 3.4))
ax.hist(d2_null, bins=60, color="#c8daf3", density=True, label="held-out simulations (null)")
ax.axvline(thr, color=GREY, lw=1, ls="--", label="99th percentile threshold")
for i, k in enumerate(scores):
    s = np.array(scores[k]["d2"])
    ax.scatter(s, np.full_like(s, -0.004 * (i + 1)), s=12, color=COL[i], label=f"{k} (n={len(s)})", zorder=5)
ax.set_xscale("log"); ax.set_xlabel("squared Mahalanobis distance of the summary vector"); ax.set_ylabel("density"); ax.legend(fontsize=7, loc="upper right")
ax.set_title("Summary-space misspecification check", fontsize=9)
fig.tight_layout(); fig.savefig(PLOTS / "mahalanobis.png"); plt.close(fig)
print("wrote", RESULTS / "detection.md")
