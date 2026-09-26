"""
Push posteriors through the recorded sidescan dive.

Which parameters may be carried from the star to the dive?
  delta (heading bias) and s (speed scale) are properties of the vehicle and could plausibly transfer;
  the current c belongs to the site and the day (Adolfbukta, 7 Sept vs Adventfjorden, 8 Sept) and must not.
Two propagation variants are therefore computed:
  A  'carried over'  all of (delta, s, c) drawn from the star posteriors (pooled over the 23 star windows).
                     This is the naive use and is reported to show what carrying a current across sites does.
  B  'dive-informed' delta from the star posteriors (heading bias is unobservable without GPS), and (s, c)
                     from the posteriors of the dive's own windows (bottom track present, no GPS), applied
                     piecewise: second t uses the window whose centre is nearest. Two couplings across windows:
                       B-indep  independent draws per window          (lower bound on the spread)
                       B-corr   same posterior quantile in every window, per parameter (upper bound)
Reported for each: median and 90 % envelope of |error| of the nominal water-track dead reckoning
(sensed DUNE heading, water track, no corrections) along the dive, the predicted closure distribution
at resurfacing, and the percentile of the observed closure (23.3 m; DUNE's own correction 19.9 m).
"""
from __future__ import annotations

import json
import numpy as np
import matplotlib.pyplot as plt

from config import ANALYSIS, LOGS, RESULTS, PLOTS, T
from make_windows import series_1hz
from simulator import IDX
from common_sbi import load_model, posterior, load_windows, COL, GREY

S = 400
rng = np.random.default_rng(1)
dive_res = json.loads((ANALYSIS / LOGS["sidescan"] / "results" / "dive_results.json").read_text())
obs_wt = dive_res["dive1"]["closures"]["water track"]["abs"]
obs_dune = dive_res["dive1"]["jump_abs"]

appr, stats = load_model()
W = load_windows()
star_post = posterior(appr, stats, W["star"]["x"], n=50)              # (23, 50, 5)
star_pool = star_post.reshape(-1, 5)
dive_x, dive_t0 = W["sidescan_dive"]["x"], W["sidescan_dive"]["t0"]
dive_post = posterior(appr, stats, dive_x, n=S)                       # (Wn, S, 5)

x, t, ok, med = series_1hz(LOGS["sidescan"], "es")
m = (med == 3)
i0, i1 = np.argmax(m), len(m) - np.argmax(m[::-1])
xd, td = x[i0:i1], t[i0:i1]
N = len(td)
psi = np.arctan2(xd[:, IDX["sin_psi"]], xd[:, IDX["cos_psi"]])
u, v, mk = xd[:, IDX["wt_u"]].copy(), xd[:, IDX["wt_v"]].copy(), xd[:, IDX["m_dvl"]]
last = (0.0, 0.0)
for k in range(N):
    if mk[k] > 0.5: last = (u[k], v[k])
    else: u[k], v[k] = last

# window assignment: nearest window centre
centres = dive_t0 + T / 2
assign = np.argmin(np.abs(td[:, None] - centres[None, :]), axis=1)     # (N,)


def track(delta, s, c):
    """delta scalar; s (N,), c (N, 2) per second"""
    a = psi + np.radians(delta)
    vn = s * (np.cos(a) * u - np.sin(a) * v) + c[:, 0]
    ve = s * (np.sin(a) * u + np.cos(a) * v) + c[:, 1]
    return np.column_stack([np.cumsum(vn), np.cumsum(ve)])


nom = track(0.0, np.ones(N), np.zeros((N, 2)))
res, md = {}, []
say = lambda s_: (print(s_), md.append(s_))


def run(name, sampler):
    errs = np.empty((S, N))
    for k in range(S):
        delta, s_t, c_t = sampler(k)
        errs[k] = np.hypot(*(nom - track(delta, s_t, c_t)).T)
    return errs


# A: everything from the star
def samp_A(k):
    th = star_pool[rng.integers(len(star_pool))]
    return th[0], np.full(N, th[1]), np.tile(th[2:4], (N, 1))
# B-indep: delta from star, per-window independent (s, c) from the dive windows
def samp_Bi(k):
    d = star_pool[rng.integers(len(star_pool)), 0]
    j = rng.integers(S, size=len(dive_post))
    sc = dive_post[np.arange(len(dive_post)), j]                      # (Wn, 5)
    return d, sc[assign, 1], sc[assign][:, 2:4]
# B-corr: same rank in every window
dive_sorted = np.sort(dive_post, axis=1)
def samp_Bc(k):
    d = star_pool[rng.integers(len(star_pool)), 0]
    r = rng.integers(S)
    sc = dive_sorted[:, r, :]
    return d, sc[assign, 1], sc[assign][:, 2:4]


tt = td - td[0]
say("# Posterior propagated through the sidescan dive\n")
say(f"Dive {N} s ({N/60:.1f} min), {len(dive_post)} dive windows. Observed closure of the nominal water-track DR: {obs_wt:.1f} m; DUNE's own correction: {obs_dune:.1f} m.\n")
say("| variant | median error at 10 min [m] | median error at end [m] | 90 % at end [m] | predicted-closure percentile of the observed 23.3 m |")
say("|---|---|---|---|---|")
envs = {}
for name, f in [("A carried over from star (delta, s, c)", samp_A), ("B-indep dive-informed (s, c per window)", samp_Bi), ("B-corr dive-informed, correlated", samp_Bc)]:
    e = run(name, f)
    med_e, lo_e, hi_e = np.median(e, 0), np.percentile(e, 5, 0), np.percentile(e, 95, 0)
    pct = float(np.mean(e[:, -1] <= obs_wt))
    envs[name] = (med_e, lo_e, hi_e)
    res[name] = dict(median_10min=float(med_e[600]), median_end=float(med_e[-1]), lo_end=float(lo_e[-1]), hi_end=float(hi_e[-1]), obs_percentile=pct,
                     max_median=float(med_e.max()), median_of_path=float(np.median(med_e)))
    say(f"| {name} | {med_e[600]:.1f} | {med_e[-1]:.1f} | {lo_e[-1]:.1f}–{hi_e[-1]:.1f} | {pct*100:.0f} % |")
# dive-window posterior summary (for the text)
cm = np.hypot(dive_post[:, :, 2], dive_post[:, :, 3])
say(f"\nDive-window posteriors (bottom track present, no GPS): median s {np.median(dive_post[:, :, 1]):.3f} (median 90 % width {np.median(np.percentile(dive_post[:, :, 1], 95, 1) - np.percentile(dive_post[:, :, 1], 5, 1)):.3f}); "
    f"median c_N {np.median(dive_post[:, :, 2]):+.3f}, c_E {np.median(dive_post[:, :, 3]):+.3f} m/s; median |c| {np.median(cm):.3f} m/s; "
    f"median 90 % width of c_N {np.median(np.percentile(dive_post[:, :, 2], 95, 1) - np.percentile(dive_post[:, :, 2], 5, 1)):.3f} m/s; "
    f"δ from these windows (unobservable without GPS): median 90 % width {np.median(np.percentile(dive_post[:, :, 0], 95, 1) - np.percentile(dive_post[:, :, 0], 5, 1)):.1f}° vs prior 27°.")
say(f"Star posterior pool: δ median {np.median(star_pool[:, 0]):+.2f}° (5–95 %: {np.percentile(star_pool[:, 0], 5):+.2f} to {np.percentile(star_pool[:, 0], 95):+.2f}), s median {np.median(star_pool[:, 1]):.3f}.")
res["dive_windows"] = dict(s_median=float(np.median(dive_post[:, :, 1])), cn_median=float(np.median(dive_post[:, :, 2])), ce_median=float(np.median(dive_post[:, :, 3])),
                           cmag_median=float(np.median(cm)), n_windows=int(len(dive_post)), duration_s=int(N))
res["observed"] = dict(wt_closure=obs_wt, dune=obs_dune)
(RESULTS / "propagation.json").write_text(json.dumps(res, indent=1)); (RESULTS / "propagation.md").write_text("\n".join(md))

fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw=dict(width_ratios=[1, 1.15]))
ax = axs[0]
ax.plot(nom[:, 1], nom[:, 0], color=GREY, lw=1.0, label="nominal water-track DR")
for k in range(80):
    d_, s_, c_ = samp_Bi(k); p = track(d_, s_, c_); ax.plot(p[:, 1], p[:, 0], color=COL[0], lw=0.4, alpha=0.3)
ax.plot([], [], color=COL[0], lw=1, label="80 dive-informed corrected tracks")
ax.set_aspect("equal"); ax.set_xlabel("east [m]"); ax.set_ylabel("north [m]"); ax.legend(fontsize=7, loc="lower left"); ax.set_title("Spread of corrected tracks (variant B, independent windows)", fontsize=8)
ax = axs[1]
names = list(envs)
for i, (nm, colr) in enumerate(zip(names, [COL[1], COL[0], COL[2]])):
    med_e, lo_e, hi_e = envs[nm]
    ax.fill_between(tt / 60, lo_e, hi_e, color=colr, alpha=0.15); ax.plot(tt / 60, med_e, color=colr, lw=1.3, label=nm)
ax.axhline(obs_wt, color="k", lw=1.0, ls=":", label=f"observed closure {obs_wt:.0f} m")
ax.set_yscale("log"); ax.set_ylim(1, 1000); ax.set_xlabel("time since dive [min]"); ax.set_ylabel("predicted |error| of nominal DR [m]")
ax.legend(fontsize=6.5, loc="upper left"); ax.set_title("Predicted position error along the dive (median, 90 %)", fontsize=8)
fig.tight_layout(); fig.savefig(PLOTS / "sidescan_envelope.png"); plt.close(fig)
print("wrote", RESULTS / "propagation.md")
