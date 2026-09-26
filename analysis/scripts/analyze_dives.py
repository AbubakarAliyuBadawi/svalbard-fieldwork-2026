"""
Dive / resurface analysis (question 4c) for the sidescan mission (lauv-marie, 8 Sept) and the
long yoyo mission (lauv-thor, 7 Sept), plus overview plots for both.

Processing choices:
  * Submerged interval = VehicleMedium UNDERWATER (3) episodes. GPS gap = last accepted fix
    before the dive to first accepted fix after it ("accepted" as in common.py: VALID_POS,
    hacc < 15 m, hdop < 4, i.e. the DUNE acceptance rule).
  * "DUNE jump" = EstimatedState position immediately before the first accepted fix minus that
    fix's position; and the largest step between consecutive 20 Hz EstimatedState samples in
    [-3, +5] s around it (the filter's correction).
  * Own dead-reckoning closure: forward Euler at DVL sample times from the last accepted fix
    before the dive to the first accepted fix after it, with the same rotation/hold-last-valid
    rules as analyze_star.py, heading = EstimatedState psi (DUNE heading, AHRS + declination).
    Variants: DVL bottom track, DVL water track, RPM x 1.3e-3, and each corrected with the
    (delta, scale, current) fitted on the surface: for lauv-marie from the star mission
    (star_results.json); for lauv-thor from its own three surface runs in this log (all on similar
    headings, so heading bias and current are poorly separated there).
  * "DUNE-accepted" fix = VALID_POS fix whose utc_time does not appear in GpsFixRejection.
  * Closure-implied (delta, scale): the rotation+scale that maps the raw DR displacement onto
    the GPS displacement (2 equations, 2 unknowns; one number per dive, so only a consistency check).
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ANALYSIS, C, GREY, load, gps_prepare, ll_to_ne, estimated_state_ne,
                    rot_body_to_ned, interp_angle, interp, wrap, dvl_valid, hold_last_valid,
                    dump_json, legs_from_pcs, utc_str)

RPM_K = 1.3e-3
star = json.loads((ANALYSIS / "101134_20260907_star" / "results" / "star_results.json").read_text())


def analyze(log: str, vehicle: str, corr: dict | None):
    OUT = ANALYSIS / log / "results"; PLOTS = ANALYSIS / log / "plots"
    OUT.mkdir(exist_ok=True, parents=True); PLOTS.mkdir(exist_ok=True, parents=True)
    md, R = [], {}
    say = lambda s="": (print(s), md.append(s))

    g = gps_prepare(load(log, "GpsFix"))
    es = load(log, "EstimatedState"); eu = load(log, "EulerAngles")
    gv = load(log, "GroundVelocity"); wv = load(log, "WaterVelocity"); rpm = load(log, "Rpm")
    dep = load(log, "Depth"); vm = load(log, "VehicleMedium"); pcs = load(log, "PlanControlState")
    rx = load(log, "UamRxFrame"); nu = load(log, "NavigationUncertainty"); lb = load(log, "LogBookEntry")
    dist = load(log, "Distance"); rj = load(log, "GpsFixRejection")
    t0 = es.timestamp.iloc[0]; T = lambda t: t - t0
    ga = g[g.accepted].reset_index(drop=True)
    lat0, lon0 = ga.lat.iloc[0], ga.lon.iloc[0]
    ga["n"], ga["e"] = ll_to_ne(ga.lat, ga.lon, lat0, lon0)
    es["n"], es["e"] = estimated_state_ne(es, lat0, lon0)
    depth_ent = "CTD" if (dep.src_ent_label == "CTD").any() else "SmartX"
    dp = dep[dep.src_ent_label == depth_ent]

    say(f"# Dive/resurface results ({log}, {vehicle})\n")
    say(f"Log {utc_str(t0)}–{utc_str(es.timestamp.iloc[-1])} UTC ({T(es.timestamp.iloc[-1])/60:.1f} min). Local frame origin: first accepted GPS fix "
        f"({np.degrees(lat0):.5f}N, {np.degrees(lon0):.5f}E). Track extent N {es.n.min():.0f}..{es.n.max():.0f} m, E {es.e.min():.0f}..{es.e.max():.0f} m.\n")

    # DUNE acceptance from GpsFixRejection
    if rj is not None and len(rj):
        rej = np.sort(rj.utc_time.values)
        k_ = np.searchsorted(rej, g.utc_time.values)
        near = np.minimum(np.abs(rej[np.clip(k_, 0, len(rej)-1)] - g.utc_time.values), np.abs(rej[np.clip(k_-1, 0, len(rej)-1)] - g.utc_time.values))
        g["dune_accepted"] = g.valid_pos & (near > 0.01)
    else:
        g["dune_accepted"] = g.accepted
    gd = g[g.dune_accepted].reset_index(drop=True)
    gd["n"], gd["e"] = ll_to_ne(gd.lat, gd.lon, lat0, lon0)
    decl = np.degrees(wrap(es.psi.values - interp_angle(eu.timestamp.values, eu.psi.values, es.timestamp.values)))
    say(f"Heading: EstimatedState psi − AHRS yaw = {np.median(decl):.2f}° constant (declination added by DUNE; AHRS psi == psi_magnetic). DR below uses the EstimatedState heading.\n")

    # surface corrections (delta, scale, current) for the DR variants
    if corr is None:
        # fit on this log's own surface runs (same model as analyze_star.fit_cds, imported lazily)
        import importlib.util
        src = (ANALYSIS.parent / "analysis" / "scripts" / "analyze_star.py").read_text()
        i0, i1 = src.index("def fit_cds"), src.index("# ------------------------------------------------------------------ 4e")
        ns = {"np": np}; exec(src[i0:i1], ns); fit_cds = ns["fit_cds"]
        gg = g[g.accepted & g.vel_ok & (g.sog > 0.5)]
        tf = gg.t_fix.values; vgg = np.column_stack([gg.vn.values, gg.ve.values])
        tw = wv.timestamp.values
        phi = interp_angle(eu.timestamp.values, eu.phi.values, tw); th = interp_angle(eu.timestamp.values, eu.theta.values, tw); ps = interp_angle(es.timestamp.values, es.psi.values, tw)
        okw = (wv.x > -30).values
        n_, e_, _ = rot_body_to_ned(wv.x.values, wv.y.values, wv.z.values, phi, th, ps)
        from common import bin_mean
        wt = bin_mean(tw[okw], np.column_stack([n_, e_])[okw], tf)
        r_ = interp(rpm.timestamp.values, rpm.value.values.astype(float), tw); u_ = RPM_K * r_
        n2, e2, _ = rot_body_to_ned(u_, 0*u_, 0*u_, phi, th, ps); rp = bin_mean(tw, np.column_stack([n2, e2]), tf)
        mw = np.isfinite(wt).all(1); mr = np.isfinite(rp).all(1)
        fw, _ = fit_cds(vgg[mw], wt[mw]); fr, _ = fit_cds(vgg[mr], rp[mr])
        hd = np.degrees(interp_angle(es.timestamp.values, es.psi.values, tf[mw])) % 360
        corr = dict(source=f"this log's surface runs ({mw.sum()} GPS epochs, DUNE headings {np.percentile(hd,5):.0f}–{np.percentile(hd,95):.0f}°)",
                    water=dict(delta_deg=fw["delta_deg"], scale=fw["scale"], cN=fw["cN"], cE=fw["cE"], rms=fw["rms"]),
                    bottom=dict(delta_deg=fw["delta_deg"], scale=1.0, cN=0.0, cE=0.0),
                    rpm=dict(delta_deg=fr["delta_deg"], scale=fr["scale"], cN=fr["cN"], cE=fr["cE"], rms=fr["rms"]))
        say(f"Surface-fitted corrections from {corr['source']}: water track δ={fw['delta_deg']:+.2f}°, s={fw['scale']:.3f}, c=({fw['cN']:+.3f},{fw['cE']:+.3f}) m/s (rms {fw['rms']:.3f}); "
            f"RPM δ={fr['delta_deg']:+.2f}°, s={fr['scale']:.3f}, c=({fr['cN']:+.3f},{fr['cE']:+.3f}). All surface runs point roughly the same way, so δ and c are confounded here; the water-track rows flagged invalid are used as numbers.\n")
    else:
        say(f"Surface-fitted corrections from {corr['source']}: water track δ={corr['water']['delta_deg']:+.2f}°, s={corr['water']['scale']:.3f}, c=({corr['water']['cN']:+.3f},{corr['water']['cE']:+.3f}) m/s; "
            f"bottom track δ={corr['bottom']['delta_deg']:+.2f}°, s={corr['bottom']['scale']:.3f}; RPM δ={corr['rpm']['delta_deg']:+.2f}°, k×{corr['rpm']['scale']:.3f}. Assumes the compass/DVL behaviour did not change between the two days.\n")

    # GPS summary
    say("## GPS / medium summary\n")
    say(f"- GpsFix: {len(g)} rows at 1 Hz; VALID_POS bit set on {g.valid_pos.mean()*100:.1f} %, accepted (hacc<15, hdop<4) {g.accepted.mean()*100:.1f} % ({g.accepted.sum()} fixes), hacc<5 m {g.good.sum()} fixes.")
    spur = g[g.valid_pos & ~g.accepted]
    if len(spur):
        idx = np.clip(np.searchsorted(dp.timestamp.values, spur.timestamp.values), 0, len(dp) - 1)
        say(f"- {len(spur)} fixes carry VALID_POS but hacc ≥ 15 m (median hacc {spur.hacc.median():.0f} m, median satellites {spur.satellites.median():.0f}) at depths up to {dp.value.values[idx].max():.1f} m: receiver garbage while submerged, correctly rejected by the navigation (GpsFixRejection reasons: {rj.reason.value_counts().to_dict() if rj is not None else 'n/a'}; 1=INVALID, 3=ABOVE_MAX_HACC, 0=ABOVE_THRESHOLD).")
    say(f"- Header timestamp − GPS UTC of fix: median {g.latency.median():+.3f} s.")
    med = vm.medium.value_counts().to_dict()
    say(f"- VehicleMedium seconds: {med} (2=WATER, 3=UNDERWATER). Depth [{depth_ent}] max {dp.value.max():.1f} m.")
    gvv, wvv = dvl_valid(gv), dvl_valid(wv)
    say(f"- DVL bottom track valid {gvv.mean()*100:.1f} % of {len(gv)} samples; water track valid {wvv.mean()*100:.1f} %.")
    if wvv.mean() < 0.5:
        # are the 'invalid' water-track values meaningful?
        r_at = interp(rpm.timestamp.values, rpm.value.values.astype(float), wv.timestamp.values)
        mm = (wv.x > -30) & (r_at > 300)
        cc = np.corrcoef(wv.x[mm], r_at[mm])[0, 1]
        say(f"- WaterVelocity rows flagged invalid still hold numbers: x vs RPM correlation {cc:.2f} over {mm.sum()} samples; mean x/(RPM·1.3e-3) = {np.mean(wv.x[mm]/(r_at[mm]*RPM_K)):.2f}. They are DVL water-track outputs whose quality flag failed; not used by the filter.")
    usbl = [n for n in ["UsblFixExtended", "UsblPositionExtended", "UsblAnglesExtended", "UsblFix", "UsblPosition", "UsblAngles", "LblEstimate", "UamRxRange"] if load(log, n) is not None]
    say(f"- USBL/LBL/range messages in the log: **{usbl if usbl else 'none'}**. Acoustic frames received (UamRxFrame): {0 if rx is None else len(rx)}.")
    nav_msgs = lb[lb.text.str.contains("estimating error", na=False)]
    for _, r in nav_msgs.iterrows():
        say(f"- DUNE Navigation log entry at {r.utc[11:19]}: `{r.text}`")
    R["gps"] = dict(n=len(g), valid_pos_frac=float(g.valid_pos.mean()), accepted=int(g.accepted.sum()), dune_accepted=int(g.dune_accepted.sum()), medium=med,
                    bottom_track_valid_frac=float(gvv.mean()), water_track_valid_frac=float(wvv.mean()), usbl=usbl,
                    uam_rx=0 if rx is None else len(rx), corrections=corr, declination_deg=float(np.median(decl)))

    # ---------------------------------------------------------------- DR inputs
    tD = wv.timestamp.values
    phiD = interp_angle(eu.timestamp.values, eu.phi.values, tD)
    thD = interp_angle(eu.timestamp.values, eu.theta.values, tD)
    psiD = interp_angle(es.timestamp.values, es.psi.values, tD)
    wv_b, _ = hold_last_valid(wv[["x", "y", "z"]].values, wvv.values)
    gv_b, _ = hold_last_valid(gv[["x", "y", "z"]].values, gvv.values)
    gv_at = np.column_stack([interp(gv.timestamp.values, gv_b[:, i], tD) for i in range(3)])
    r_at = interp(rpm.timestamp.values, rpm.value.values.astype(float), tD)
    if wvv.mean() < 0.5:   # lauv-thor: use the flag-invalid water-track numbers, hold only sentinel rows
        wv_b, _ = hold_last_valid(wv[["x", "y", "z"]].values, (wv.x > -30).values)
    vel = {}
    for name, body, cc in [("bottom track", gv_at, corr["bottom"]), ("water track", wv_b, corr["water"]), ("RPM x 1.3e-3", np.column_stack([RPM_K * r_at, 0 * r_at, 0 * r_at]), corr["rpm"])]:
        n_, e_, _ = rot_body_to_ned(body[:, 0], body[:, 1], body[:, 2], phiD, thD, psiD)
        v = np.column_stack([n_, e_]); vel[name] = v
        dl = np.radians(cc["delta_deg"])
        vel[name + " + surface fit"] = cc["scale"] * np.column_stack([np.cos(dl) * v[:, 0] - np.sin(dl) * v[:, 1], np.sin(dl) * v[:, 0] + np.cos(dl) * v[:, 1]]) + np.array([cc["cN"], cc["cE"]])
    dtD = np.diff(tD, prepend=tD[0])

    # ---------------------------------------------------------------- dives
    ch = vm[vm.medium != vm.medium.shift()].reset_index(drop=True)
    dives = []
    for i, r in ch.iterrows():
        if r.medium == 3:
            t_end = ch.loc[i + 1, "timestamp"] if i + 1 < len(ch) else vm.timestamp.iloc[-1]
            dives.append((r.timestamp, t_end))
    say(f"\n## Dive / resurface events: {len(dives)}\n")
    dr_tracks = []
    for k, (td, ts) in enumerate(dives, 1):
        before = ga[ga.t_fix < td]; after = gd[gd.t_fix > ts - 2]
        if not len(before) or not len(after):
            say(f"### Dive {k}: {utc_str(td)} → {utc_str(ts)}: no accepted GPS on one side, skipped"); continue
        a = before.iloc[-1]; b = after.iloc[0]
        good_after = after[after.good]
        bg = good_after.iloc[0] if len(good_after) else None
        say(f"### Dive {k}: medium UNDERWATER {utc_str(td)} → {utc_str(ts)} ({(ts-td)/60:.1f} min)\n")
        say(f"- Last accepted GPS before: {utc_str(a.t_fix)} (hacc {a.hacc:.1f} m); first fix accepted by DUNE after: {utc_str(b.t_fix)} (hacc {b.hacc:.1f} m, hdop {b.hdop:.2f}, {int(b.satellites)} sats); GPS gap **{(b.t_fix-a.t_fix)/60:.1f} min**. "
            f"First fix with hacc<5 m: {utc_str(bg.t_fix)+' (hacc %.1f m)'%bg.hacc if bg is not None else 'none in this log'}.")
        seg = dp[(dp.timestamp >= td) & (dp.timestamp <= ts)]
        alt = dist[(dist.src_ent_label == "DVL Filtered") & (dist.timestamp >= td) & (dist.timestamp <= ts)]
        altv = alt[alt.validity == 1].value
        say(f"- Depth max {seg.value.max():.1f} m, mean {seg.value.mean():.1f} m; DVL altitude valid {(alt.validity==1).mean()*100:.0f} %, median {altv.median() if len(altv) else float('nan'):.1f} m.")
        gvs = gv[(gv.timestamp >= td) & (gv.timestamp <= ts)]
        bt_ok = dvl_valid(gvs)
        gaps = []
        tv, bad = gvs.timestamp.values, (~bt_ok).values
        i = 0
        while i < len(bad):
            if bad[i]:
                j = i
                while j < len(bad) and bad[j]: j += 1
                gaps.append(tv[min(j, len(bad)-1)] - tv[i]); i = j
            else: i += 1
        say(f"- DVL bottom lock while submerged: {bt_ok.mean()*100:.1f} % of {len(gvs)} samples, {len(gaps)} dropouts, longest {max(gaps) if gaps else 0:.1f} s.")
        nrx = 0 if rx is None else int(((rx.timestamp >= td) & (rx.timestamp <= ts)).sum())
        say(f"- USBL fixes while submerged: **0** (none logged at all). Acoustic frames received from the ship while submerged: {nrx}.")
        nus = nu[(nu.timestamp >= td) & (nu.timestamp <= ts)]
        say(f"- DUNE NavigationUncertainty at end of dive: σ_x = {np.sqrt(nus.x.iloc[-1]):.1f} m, σ_y = {np.sqrt(nus.y.iloc[-1]):.1f} m (max during dive {np.sqrt(nus.x.max()):.1f} m).")
        # DUNE jump
        i_b = np.searchsorted(es.timestamp.values, b.timestamp) - 1
        es_b = es.iloc[i_b]
        jump_vec = np.array([es_b.n - b.n, es_b.e - b.e])
        win = es[(es.timestamp > b.timestamp - 3) & (es.timestamp < b.timestamp + 5)]
        steps = np.hypot(np.diff(win.n), np.diff(win.e))
        say(f"- **DUNE estimate just before the first accepted fix minus that fix: ΔN {jump_vec[0]:+.1f} m, ΔE {jump_vec[1]:+.1f} m, |Δ| = {np.hypot(*jump_vec):.1f} m** (fix hacc {b.hacc:.1f} m). Largest single-step EstimatedState correction within [-3,+5] s: {steps.max():.1f} m.")
        if bg is not None and bg.t_fix != b.t_fix:
            # propagate the pre-correction estimate to the good fix with the raw bottom-track DR
            i0 = np.searchsorted(tD, b.timestamp); i1 = np.searchsorted(tD, bg.t_fix)
            v = vel["bottom track"][i0:i1]; dtt = dtD[i0:i1].copy(); dtt[0] = 0
            if len(v) and not np.isnan(v).any():
                pn = es_b.n + np.sum(v[:, 0] * dtt); pe = es_b.e + np.sum(v[:, 1] * dtt)
                say(f"- Same estimate propagated (bottom-track DR) to the first hacc<5 m fix at {utc_str(bg.t_fix)}: ΔN {pn-bg.n:+.1f}, ΔE {pe-bg.e:+.1f}, |Δ| = {np.hypot(pn-bg.n, pe-bg.e):.1f} m.")
        # own DR closure
        i0 = np.searchsorted(tD, a.t_fix); i1 = np.searchsorted(tD, b.t_fix)
        say("\n  Own dead reckoning from the last accepted fix before the dive to the first accepted fix after it:\n")
        say("  | input | closure ΔN [m] | ΔE [m] | |Δ| [m] | |Δ| / path length | closure-implied δ [°], scale |")
        say("  |---|---|---|---|---|---|")
        gps_disp = np.array([b.n - a.n, b.e - a.e])
        closures = {}
        for name, v in vel.items():
            seg_v = v[i0:i1]
            if name.startswith("bottom") and bt_ok.mean() < 0.5:
                say(f"  | {name} | n/a (bottom lock {bt_ok.mean()*100:.1f} % of the dive) | | | | |"); continue
            if np.isnan(seg_v).any():
                say(f"  | {name} | n/a (NaN, no valid samples at start) | | | | |"); continue
            dtt = dtD[i0:i1].copy(); dtt[0] = 0
            pn = a.n + np.cumsum(seg_v[:, 0] * dtt); pe = a.e + np.cumsum(seg_v[:, 1] * dtt)
            path = np.sum(np.hypot(seg_v[:, 0], seg_v[:, 1]) * dtt)
            cl = np.array([pn[-1] - b.n, pe[-1] - b.e])
            dr_disp = np.array([pn[-1] - a.n, pe[-1] - a.e])
            ang = np.degrees(np.arctan2(gps_disp[1], gps_disp[0]) - np.arctan2(dr_disp[1], dr_disp[0]))
            ang = (ang + 180) % 360 - 180
            sc = np.hypot(*gps_disp) / max(np.hypot(*dr_disp), 1e-9)
            closures[name] = dict(dN=cl[0], dE=cl[1], abs=float(np.hypot(*cl)), path=path, implied_delta_deg=ang, implied_scale=sc)
            say(f"  | {name} | {cl[0]:+.1f} | {cl[1]:+.1f} | {np.hypot(*cl):.1f} | {np.hypot(*cl)/path*100:.2f} % | {ang:+.1f}, {sc:.3f} |")
            if "fit" not in name:
                dr_tracks.append((k, name, tD[i0:i1], pn, pe))
        say("")
        say(f"  GPS displacement over the dive: ΔN {gps_disp[0]:+.1f}, ΔE {gps_disp[1]:+.1f} m ({np.hypot(*gps_disp):.0f} m); the closure-implied δ is only meaningful when this displacement is long compared with the closure error.")
        # heading-bias georeferencing error
        e_seg = es[(es.timestamp >= td) & (es.timestamp <= ts)]
        d_from_dive = np.hypot(e_seg.n - e_seg.n.iloc[0], e_seg.e - e_seg.e.iloc[0])
        dlt = np.radians(corr["water"]["delta_deg"])
        rot_err = 2 * np.sin(abs(dlt) / 2) * d_from_dive
        say(f"- A heading bias δ rotates a DR track about the dive point; with the surface-fitted δ = {np.degrees(dlt):+.2f}° this is a median {rot_err.median():.1f} m, max {rot_err.max():.1f} m during this dive (distance from dive point up to {d_from_dive.max():.0f} m); per degree of bias: max {2*np.sin(np.radians(0.5))*d_from_dive.max():.1f} m. Reciprocal survey lines cancel most of it at the end, so closure errors understate mid-mission georeferencing error.")
        say("")
        R[f"dive{k}"] = dict(t_dive=td, t_surface=ts, gps_gap_min=(b.t_fix - a.t_fix) / 60, first_fix_hacc=b.hacc, jump_N=jump_vec[0], jump_E=jump_vec[1], jump_abs=float(np.hypot(*jump_vec)),
                             max_step=float(steps.max()), bottom_lock_frac=float(bt_ok.mean()), longest_dropout_s=float(max(gaps) if gaps else 0), acoustic_rx=nrx,
                             sigma_end=float(np.sqrt(nus.x.iloc[-1])), closures=closures, depth_max=float(seg.value.max()), rot_err_per_deg_max=float(2*np.sin(np.radians(0.5))*d_from_dive.max()))

    # ---------------------------------------------------------------- plots
    legs = legs_from_pcs(pcs)
    fig, ax = plt.subplots(figsize=(8, 7.5))
    sc = ax.scatter(es.e[::5], es.n[::5], c=T(es.timestamp[::5]), cmap="viridis", s=2, zorder=2, label="EstimatedState (DUNE, coloured by time)")
    ax.scatter(gd.e, gd.n, s=10, facecolor="none", edgecolor=C[7], zorder=4, label=f"GPS fixes accepted by DUNE ({len(gd)})")
    for k, name, tt, pn, pe in dr_tracks:
        ls = {"bottom track": "-", "water track": "--", "RPM x 1.3e-3": ":"}[name]
        ax.plot(pe, pn, ls, color=C[1], lw=0.8, zorder=3, label=f"own DR, {name} (dive {k})")
    if rx is not None and len(rx):
        rn = interp(es.timestamp.values, es.n.values, rx.timestamp.values); re_ = interp(es.timestamp.values, es.e.values, rx.timestamp.values)
        ax.scatter(re_, rn, marker="^", s=40, facecolor="none", edgecolor=C[3], zorder=5, label=f"acoustic frame received ({len(rx)}); no USBL fix logged")
    for k, (td, ts) in enumerate(dives, 1):
        for tt, lab, mk in [(td, f"dive {k}", "v"), (ts, f"surface {k}", "^")]:
            n_ = interp(es.timestamp.values, es.n.values, tt); e_ = interp(es.timestamp.values, es.e.values, tt)
            ax.plot(e_, n_, mk, color=C[6], ms=8, zorder=6); ax.annotate(lab, (e_, n_), fontsize=7, color=C[6], xytext=(5, 5), textcoords="offset points")
    ax.set_aspect("equal"); ax.set_xlabel("east [m]"); ax.set_ylabel("north [m]")
    ax.set_title(f"{log} ({vehicle}) track")
    cb = fig.colorbar(sc, ax=ax, shrink=0.6); cb.set_label("time since log start [s]")
    ax.legend(fontsize=7, loc="best"); fig.tight_layout(); fig.savefig(PLOTS / "track.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 3.2))
    for i, (ent, sub) in enumerate(dep.groupby("src_ent_label")):
        ax.plot(T(sub.timestamp), sub.value, lw=0.7, color=C[i], label=f"Depth [{ent}]")
    altf = dist[dist.src_ent_label == "DVL Filtered"]; altf = altf[altf.validity == 1]
    ax.plot(T(altf.timestamp), dp.value.values[np.clip(np.searchsorted(dp.timestamp.values, altf.timestamp.values), 0, len(dp)-1)] + altf.value.values, lw=0.5, color=GREY, label="depth + DVL altitude (seabed)")
    for td, ts in dives:
        ax.axvspan(T(td), T(ts), color=C[0], alpha=0.06)
    ax.invert_yaxis(); ax.set_xlabel("time since log start [s]"); ax.set_ylabel("depth [m]"); ax.set_title("Depth vs time (shaded = VehicleMedium UNDERWATER)")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(PLOTS / "depth.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(T(eu.timestamp), np.degrees(eu.psi) % 360, lw=0.5, color=C[0], label="AHRS yaw (50 Hz)")
    ax.plot(T(es.timestamp), np.degrees(es.psi) % 360, lw=0.5, color=C[2], alpha=0.7, label="EstimatedState psi (20 Hz)")
    mg_ = ga.vel_ok & (ga.sog > 0.8)
    ax.plot(T(ga.t_fix[mg_]), np.degrees(ga.cog[mg_]) % 360, ".", ms=2, color=C[1], label="GPS COG (accepted, sog>0.8)")
    for _, L in legs.iterrows():
        ax.axvline(T(L.t0), color=GREY, lw=0.4); ax.text(T(L.t0) + 2, 350, L.man_id, fontsize=6, color=GREY, rotation=90, va="top")
    ax.set_ylim(0, 360); ax.set_yticks(range(0, 361, 90)); ax.set_xlabel("time since log start [s]"); ax.set_ylabel("heading [°]"); ax.set_title("Heading vs time")
    ax.legend(fontsize=7, loc="lower left"); fig.tight_layout(); fig.savefig(PLOTS / "heading.png"); plt.close(fig)

    fig, axs = plt.subplots(5, 1, figsize=(10, 7.5), sharex=True)
    axs[0].step(T(g.t_fix), g.valid_pos.astype(int), where="post", color=C[0]); axs[0].set_ylabel("VALID_POS"); axs[0].set_ylim(-0.1, 1.1)
    axs[1].plot(T(g.t_fix), g.hacc, ".", ms=2, color=C[0]); axs[1].axhline(15, color=C[7], lw=0.8); axs[1].set_yscale("log"); axs[1].set_ylabel("hacc [m]")
    axs[2].plot(T(g.t_fix), g.satellites, ".", ms=2, color=C[0]); axs[2].set_ylabel("satellites")
    axs[3].step(T(g.t_fix), g.accepted.astype(int), where="post", color=C[2]); axs[3].set_ylabel("accepted"); axs[3].set_ylim(-0.1, 1.1)
    axs[4].step(T(vm.timestamp), vm.medium, where="post", color=C[1]); axs[4].set_yticks([2, 3]); axs[4].set_yticklabels(["WATER", "UNDERW."]); axs[4].set_ylabel("medium")
    axs[4].set_xlabel("time since log start [s]"); axs[0].set_title("GPS validity timeline (red = 15 m hacc acceptance threshold; 'accepted' = VALID_POS & hacc<15 & hdop<4)")
    fig.tight_layout(); fig.savefig(PLOTS / "gps_validity.png"); plt.close(fig)

    (OUT / "dive_results.md").write_text("\n".join(md)); dump_json(R, OUT / "dive_results.json")
    print("wrote", OUT, "\n")


if __name__ == "__main__":
    sc = star["current"]
    MARIE = dict(source="star mission 7 Sept (analyze_star.py, DUNE heading)",
                 water=dict(delta_deg=sc["fit_c_delta_scale"]["delta_deg"], scale=sc["fit_c_delta_scale"]["scale"], cN=sc["fit_c_delta_scale"]["cN"], cE=sc["fit_c_delta_scale"]["cE"]),
                 bottom=dict(delta_deg=sc["fit_bottomtrack"]["delta_deg"], scale=sc["fit_bottomtrack"]["scale"], cN=0.0, cE=0.0),
                 rpm=dict(delta_deg=sc["fit_rpm"]["delta_deg"], scale=sc["fit_rpm"]["scale"], cN=sc["fit_rpm"]["cN"], cE=sc["fit_rpm"]["cE"]))
    analyze("074948_08_09_sidescan", "lauv-marie", MARIE)
    analyze("094605_0700926LongYoYo1", "lauv-thor", None)
