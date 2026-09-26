"""
Thor's two dives: does the posterior widen enough to contain the observed closure?

Thor has no bottom lock, so during the dives only the water track (flagged invalid by the DVL but
physical), the propeller speed and the heading are available. delta comes from Thor's own surface
windows (GPS present, near-parallel headings so poorly identified); (s, c) come from the dive's own
windows. Same coupling variants as propagate.py (independent per window / same quantile in every
window). Nominal DR = DUNE heading + water-track values, no corrections. Observed closure of that same
nominal DR against the first accepted GPS fix: 224.4 m and 297.7 m (dive_results.md of the Thor log);
the onboard filter (propeller-speed based) was 291.6 m and 340.5 m off.
"""
from __future__ import annotations

import json
import numpy as np

from config import ANALYSIS, LOGS, RESULTS, T
from make_windows import series_1hz
from simulator import IDX
from common_sbi import load_model, posterior, load_windows

S = 400
rng = np.random.default_rng(2)
res_j = json.loads((ANALYSIS / LOGS["thor"] / "results" / "dive_results.json").read_text())
appr, stats = load_model()
W = load_windows()
surf_pool = posterior(appr, stats, W["thor_surface"]["x"], n=100).reshape(-1, 5)
dx, dt0 = W["thor_dive"]["x"], W["thor_dive"]["t0"]
dpost = posterior(appr, stats, dx, n=S)
x, t, ok, med = series_1hz(LOGS["thor"], "es")
psi_all = np.arctan2(x[:, IDX["sin_psi"]], x[:, IDX["cos_psi"]])
md, R = [], {}
say = lambda s_: (print(s_), md.append(s_))
say("# Thor dives: posterior-predicted vs observed dead-reckoning error\n")
say(f"delta from {len(W['thor_surface']['x'])} Thor surface windows: median {np.median(surf_pool[:, 0]):+.1f}° (5–95 %: {np.percentile(surf_pool[:, 0], 5):+.1f} to {np.percentile(surf_pool[:, 0], 95):+.1f}).\n")
say("| dive | duration [min] | observed closure of nominal water-track DR [m] | onboard filter jump [m] | predicted error at end, indep: median (90 %) | correlated: median (90 %) | percentile of observed closure, indep / corr |")
say("|---|---|---|---|---|---|---|")
m = (med == 3)
edges = np.flatnonzero(np.diff(m.astype(int)))
starts = [e + 1 for e in edges if not m[e]]; ends = [e + 1 for e in edges if m[e]]
for k, (a, b) in enumerate(zip(starts, ends), 1):
    ta, tb = t[a], t[b - 1]
    sel = np.flatnonzero((dt0 >= ta - 1) & (dt0 + T <= tb + 1))
    if len(sel) == 0:
        continue
    N = b - a
    psi = psi_all[a:b]
    u, v, mk = x[a:b, IDX["wt_u"]].copy(), x[a:b, IDX["wt_v"]].copy(), x[a:b, IDX["m_dvl"]]
    last = (0.0, 0.0)
    for i in range(N):
        if mk[i] > 0.5: last = (u[i], v[i])
        else: u[i], v[i] = last
    centres = dt0[sel] + T / 2
    assign = np.argmin(np.abs(t[a:b][:, None] - centres[None, :]), axis=1)
    post = dpost[sel]; srt = np.sort(post, axis=1)

    def track(delta, s, c):
        ang = psi + np.radians(delta)
        vn = s * (np.cos(ang) * u - np.sin(ang) * v) + c[:, 0]; ve = s * (np.sin(ang) * u + np.cos(ang) * v) + c[:, 1]
        return np.column_stack([np.cumsum(vn), np.cumsum(ve)])
    nom = track(0.0, np.ones(N), np.zeros((N, 2)))
    e_i, e_c = [], []
    for _ in range(S):
        d = surf_pool[rng.integers(len(surf_pool)), 0]
        j = rng.integers(S, size=len(post)); sc = post[np.arange(len(post)), j]
        e_i.append(np.hypot(*(nom[-1] - track(d, np.full(N, sc[assign, 1].mean()) * 0 + sc[assign, 1], sc[assign][:, 2:4])[-1])))
        r = rng.integers(S); sc = srt[:, r, :]
        e_c.append(np.hypot(*(nom[-1] - track(d, sc[assign, 1], sc[assign][:, 2:4])[-1])))
    e_i, e_c = np.array(e_i), np.array(e_c)
    obs = res_j[f"dive{k}"]["closures"]["water track"]["abs"]; jump = res_j[f"dive{k}"]["jump_abs"]
    pi, pc = np.mean(e_i <= obs), np.mean(e_c <= obs)
    say(f"| {k} | {N/60:.1f} | {obs:.0f} | {jump:.0f} | {np.median(e_i):.0f} ({np.percentile(e_i,5):.0f}–{np.percentile(e_i,95):.0f}) | {np.median(e_c):.0f} ({np.percentile(e_c,5):.0f}–{np.percentile(e_c,95):.0f}) | {pi*100:.0f} % / {pc*100:.0f} % |")
    R[f"dive{k}"] = dict(duration_min=N / 60, obs=obs, jump=jump, indep=[float(np.median(e_i)), float(np.percentile(e_i, 5)), float(np.percentile(e_i, 95))],
                         corr=[float(np.median(e_c)), float(np.percentile(e_c, 5)), float(np.percentile(e_c, 95))], pct_indep=float(pi), pct_corr=float(pc),
                         n_windows=int(len(sel)), s_median=float(np.median(post[:, :, 1])), cmag_median=float(np.median(np.hypot(post[:, :, 2], post[:, :, 3]))))
(RESULTS / "propagation_thor.md").write_text("\n".join(md)); (RESULTS / "propagation_thor.json").write_text(json.dumps(R, indent=1))
