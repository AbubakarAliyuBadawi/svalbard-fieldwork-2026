"""
Validation of the trained posterior:
  1. simulation-based calibration (SBC) on held-out simulations: rank histograms, ECDF deviation,
     empirical coverage of the 50 % and 90 % central intervals;
  2. recovery (posterior mean vs truth) on held-out simulations;
  3. posterior on the real star windows against the least-squares reference; per-window
     coverage; width on straight-heading vs turning windows;
  4. posterior-predicted vs observed 2-min dead-reckoning drift on the star windows;
  5. posterior on Thor's surface windows against Thor's own surface fit.
Writes results/validation.json, results/validation.md and plots/*.png.
"""
from __future__ import annotations

import json
import numpy as np
import matplotlib.pyplot as plt

from config import DATA, RESULTS, PLOTS, THETA, T
from simulator import IDX, dead_reckon
from common_sbi import load_model, posterior, load_windows, LABELS, COL, GREY

N_SBC = 1000
N_POST = 500
rng = np.random.default_rng(0)
R, md = {}, []
say = lambda s="": (print(s), md.append(s))

appr, stats = load_model()
val = np.load(DATA / "val.npz")
xv, tv = val["x"][:N_SBC], val["theta"][:N_SBC]

# ---------------------------------------------------------------- 1. SBC + 2. recovery
post = posterior(appr, stats, xv, n=N_POST)                  # (N, n, 5)
ranks = (post < tv[:, None, :]).sum(axis=1)                  # (N, 5) in 0..n
say("# Validation of the amortized posterior\n")
say(f"## SBC on {N_SBC} held-out simulations, {N_POST} posterior draws each\n")
say("| parameter | 50 % coverage | 90 % coverage | max |ECDF − uniform| | posterior mean r | mean 90 % width | prior 90 % width |")
say("|---|---|---|---|---|---|---|")
from config import PRIOR_LO, PRIOR_HI
sbc = {}
fig, axs = plt.subplots(2, 5, figsize=(13, 5))
for i, name in enumerate(THETA):
    lo50, hi50 = np.percentile(post[:, :, i], [25, 75], axis=1)
    lo90, hi90 = np.percentile(post[:, :, i], [5, 95], axis=1)
    cov50 = np.mean((tv[:, i] >= lo50) & (tv[:, i] <= hi50)); cov90 = np.mean((tv[:, i] >= lo90) & (tv[:, i] <= hi90))
    u = (ranks[:, i] + 0.5) / (N_POST + 1)
    ecdf_dev = np.max(np.abs(np.sort(u) - (np.arange(1, N_SBC + 1) / N_SBC)))
    r = np.corrcoef(post[:, :, i].mean(1), tv[:, i])[0, 1]
    width = np.mean(hi90 - lo90); prior_w = 0.9 * (PRIOR_HI[i] - PRIOR_LO[i])
    sbc[name] = dict(cov50=cov50, cov90=cov90, ecdf_dev=ecdf_dev, r=r, width90=width, prior_width90=prior_w)
    say(f"| {name} | {cov50:.2f} | {cov90:.2f} | {ecdf_dev:.3f} | {r:+.3f} | {width:.3f} | {prior_w:.3f} |")
    axs[0, i].hist(ranks[:, i], bins=20, color=COL[0], alpha=0.8)
    axs[0, i].axhline(N_SBC / 20, color=GREY, lw=0.8); axs[0, i].set_title(LABELS[i]); axs[0, i].set_xlabel("rank of truth")
    axs[1, i].errorbar(tv[:300, i], post[:300, :, i].mean(1), yerr=[post[:300, :, i].mean(1) - lo90[:300], hi90[:300] - post[:300, :, i].mean(1)],
                       fmt=".", ms=3, color=COL[0], ecolor="#c8daf3", elinewidth=0.5)
    axs[1, i].plot([PRIOR_LO[i], PRIOR_HI[i]], [PRIOR_LO[i], PRIOR_HI[i]], color=GREY, lw=0.8)
    axs[1, i].set_xlabel("true"); axs[1, i].set_ylabel("posterior mean, 90 %")
axs[0, 0].set_ylabel("count")
fig.suptitle(f"SBC rank histograms (top; grey = uniform) and recovery (bottom) on {N_SBC} held-out simulations", fontsize=9)
fig.tight_layout(); fig.savefig(PLOTS / "sbc_recovery.png"); plt.close(fig)
R["sbc"] = sbc
# KS-type p-value bound: with N=1000, the 95 % critical max deviation is 1.36/sqrt(N)
say(f"\nReference: for {N_SBC} draws the 95 % critical value of the max ECDF deviation is {1.36/np.sqrt(N_SBC):.3f}.\n")

# ---------------------------------------------------------------- 3. real star windows
W = load_windows()
star = W["star"]; ref = star["ref"]
ps = posterior(appr, stats, star["x"], n=N_POST)             # (23, n, 5)
say("## Posterior on the real star windows (120 s, stride 30 s) vs least-squares reference\n")
say(f"Reference (all-leg fit): δ={ref[0]:+.2f}°, s={ref[1]:.3f}, c=({ref[2]:+.3f},{ref[3]:+.3f}) m/s, log10σ={ref[4]:.2f}\n")
say("| parameter | median of posterior means | median 90 % interval | windows whose 90 % interval contains the reference |")
say("|---|---|---|---|")
starres = {}
for i, name in enumerate(THETA):
    lo, hi = np.percentile(ps[:, :, i], [5, 95], axis=1)
    inside = np.mean((ref[i] >= lo) & (ref[i] <= hi))
    pm = ps[:, :, i].mean(1)
    starres[name] = dict(median_mean=float(np.median(pm)), median_lo=float(np.median(lo)), median_hi=float(np.median(hi)), coverage=float(inside), ref=float(ref[i]))
    say(f"| {name} | {np.median(pm):+.3f} | [{np.median(lo):+.3f}, {np.median(hi):+.3f}] | {inside*100:.0f} % ({int(inside*len(ps))}/{len(ps)}) |")
R["star"] = starres
# straight vs turning windows
psi = np.unwrap(np.arctan2(star["x"][:, :, IDX["sin_psi"]], star["x"][:, :, IDX["cos_psi"]]), axis=1)
span = np.degrees(psi.max(1) - psi.min(1))
straight = span < 20
say(f"\nWindows with heading span < 20°: {straight.sum()}; with a turn: {(~straight).sum()}.")
say("| group | n | 90 % width δ [°] | 90 % width |c| [m/s] | 90 % width s |")
say("|---|---|---|---|---|")
grp = {}
for lab, m in [("straight", straight), ("with turn", ~straight)]:
    if m.sum() == 0:
        continue
    wd = np.mean(np.percentile(ps[m, :, 0], 95, 1) - np.percentile(ps[m, :, 0], 5, 1))
    cmag = np.hypot(ps[m, :, 2], ps[m, :, 3]); wc = np.mean(np.percentile(cmag, 95, 1) - np.percentile(cmag, 5, 1))
    ws = np.mean(np.percentile(ps[m, :, 1], 95, 1) - np.percentile(ps[m, :, 1], 5, 1))
    grp[lab] = dict(n=int(m.sum()), width_delta=wd, width_cmag=wc, width_s=ws)
    say(f"| {lab} | {m.sum()} | {wd:.2f} | {wc:.3f} | {ws:.3f} |")
R["star_groups"] = grp
fig, axs = plt.subplots(1, 5, figsize=(13, 2.8))
for i in range(5):
    lo, hi = np.percentile(ps[:, :, i], [5, 95], axis=1); pm = ps[:, :, i].mean(1)
    axs[i].errorbar(np.arange(len(pm)), pm, yerr=[pm - lo, hi - pm], fmt="o", ms=3, color=COL[0], ecolor="#c8daf3")
    axs[i].axhline(ref[i], color=COL[1], lw=1.2, label="least-squares reference")
    axs[i].set_title(LABELS[i]); axs[i].set_xlabel("star window")
axs[0].legend(fontsize=7); fig.suptitle("Posterior (mean, 90 % interval) on the 23 star windows vs the all-leg reference", fontsize=9)
fig.tight_layout(); fig.savefig(PLOTS / "posterior_star_windows.png"); plt.close(fig)

# ---------------------------------------------------------------- 4. predicted vs observed drift
say("\n## Posterior-predicted vs observed 2-min dead-reckoning drift (star windows)\n")
obs, pred_med, pred_lo, pred_hi = [], [], [], []
for w in range(len(ps)):
    x = star["x"][w]
    nom = dead_reckon(x)                                       # nominal DR (sensed heading, water track)
    gps = np.column_stack([np.cumsum(x[:, IDX["gps_vn"]]), np.cumsum(x[:, IDX["gps_ve"]])])
    obs.append(np.hypot(*(nom[-1] - gps[-1])))
    d = []
    for k in rng.choice(N_POST, 100, replace=False):
        corr = dead_reckon(x, ps[w, k])
        d.append(np.hypot(*(nom[-1] - corr[-1])))
    pred_med.append(np.median(d)); pred_lo.append(np.percentile(d, 5)); pred_hi.append(np.percentile(d, 95))
obs, pred_med, pred_lo, pred_hi = map(np.array, (obs, pred_med, pred_lo, pred_hi))
inside = np.mean((obs >= pred_lo) & (obs <= pred_hi))
say(f"- Observed nominal-DR drift after 120 s: median {np.median(obs):.1f} m (range {obs.min():.1f}–{obs.max():.1f}).")
say(f"- Posterior-predicted drift: median of window medians {np.median(pred_med):.1f} m; observed drift inside the 90 % predictive interval in {inside*100:.0f} % of windows.")
say(f"- Correlation observed vs predicted median across windows: {np.corrcoef(obs, pred_med)[0,1]:+.2f}.")
R["drift"] = dict(obs_median=float(np.median(obs)), pred_median=float(np.median(pred_med)), coverage90=float(inside), corr=float(np.corrcoef(obs, pred_med)[0, 1]),
                  obs=obs.tolist(), pred_med=pred_med.tolist(), pred_lo=pred_lo.tolist(), pred_hi=pred_hi.tolist())
fig, ax = plt.subplots(figsize=(4, 4))
ax.errorbar(obs, pred_med, yerr=[pred_med - pred_lo, pred_hi - pred_med], fmt="o", ms=4, color=COL[0], ecolor="#c8daf3")
lim = max(obs.max(), pred_hi.max()) * 1.1
ax.plot([0, lim], [0, lim], color=GREY, lw=0.8); ax.set_xlim(0, lim); ax.set_ylim(0, lim)
ax.set_xlabel("observed drift of nominal DR after 120 s [m]"); ax.set_ylabel("posterior-predicted drift [m] (median, 90 %)")
ax.set_title("Star windows: predicted vs observed drift", fontsize=9); fig.tight_layout(); fig.savefig(PLOTS / "drift_pred_vs_obs.png"); plt.close(fig)

# ---------------------------------------------------------------- 5. Thor surface windows
th = W["thor_surface"]
if len(th["x"]):
    pt = posterior(appr, stats, th["x"], n=N_POST)
    say(f"\n## Posterior on Thor's {len(pt)} surface windows vs Thor's own surface fit\n")
    say(f"Reference (Thor surface fit, δ and c confounded): δ={th['ref'][0]:+.2f}°, s={th['ref'][1]:.3f}, c=({th['ref'][2]:+.3f},{th['ref'][3]:+.3f})\n")
    say("| parameter | median of posterior means | median 90 % interval | windows containing the reference |")
    say("|---|---|---|---|")
    thres = {}
    for i, name in enumerate(THETA):
        lo, hi = np.percentile(pt[:, :, i], [5, 95], axis=1); pm = pt[:, :, i].mean(1)
        inside = np.mean((th["ref"][i] >= lo) & (th["ref"][i] <= hi))
        thres[name] = dict(median_mean=float(np.median(pm)), median_lo=float(np.median(lo)), median_hi=float(np.median(hi)), coverage=float(inside), ref=float(th["ref"][i]))
        say(f"| {name} | {np.median(pm):+.3f} | [{np.median(lo):+.3f}, {np.median(hi):+.3f}] | {inside*100:.0f} % |")
    R["thor_surface"] = thres

(RESULTS / "validation.md").write_text("\n".join(md))
(RESULTS / "validation.json").write_text(json.dumps(R, indent=1, default=float))
print("wrote", RESULTS / "validation.md")
