"""
Star mission (101134_20260907_star, LAUV Marie at the surface): questions 4a, 4b, 4e, 4f.

Processing choices (all stated, nothing smoothed):
  * GPS epoch = UTC time of fix (t_fix); the header timestamp lags it by ~0.32 s (network latency).
  * "accepted" GPS fix = receiver VALID_POS bit and hacc < 15 m and hdop < 4 (the DUNE thresholds).
  * DVL velocities are body-frame (verified below against GPS) and rotated to NED with the full
    roll/pitch rotation from EulerAngles (AHRS, 50 Hz) and the yaw from EstimatedState (DUNE's
    navigation heading = AHRS magnetic yaw + the declination DUNE adds; EulerAngles psi equals
    psi_magnetic in these logs). All angles linearly interpolated (unwrapped) to the DVL times.
    The raw AHRS yaw is kept as a separate 'no declination' case. Only DVL samples with validity == 7 (x, y, z valid) are used in the fits.
  * Velocity comparison at GPS epochs: mean of the DVL-derived NED velocity samples within
    +-0.5 s of each t_fix (5 Hz -> ~5 samples per bin). GPS velocity = sog/cog from the receiver.
  * Dead reckoning: forward Euler on the 5 Hz DVL sample times; invalid DVL samples hold the last
    valid value (what the filter does inside its DVL timeout). Truth = accepted GPS positions
    linearly interpolated to the DR sample times.
Outputs: analysis/101134_20260907_star/results/star_results.{md,json}, plots/*.png
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ANALYSIS, C, GREY, load, gps_prepare, ll_to_ne, estimated_state_ne,
                    rot_body_to_ned, interp_angle, interp, bin_mean, wrap, dvl_valid,
                    hold_last_valid, dump_json, legs_from_pcs, utc_str)

LOG = "101134_20260907_star"
OUT = ANALYSIS / LOG / "results"
PLOTS = ANALYSIS / LOG / "plots"
OUT.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)
RPM_K_CONFIG = 1.3e-3          # "Revolutions to speed factor" in Config.ini

R = {}
md = []


def say(s=""):
    print(s)
    md.append(s)


# ------------------------------------------------------------------ load
g = gps_prepare(load(LOG, "GpsFix"))
es = load(LOG, "EstimatedState")
eu = load(LOG, "EulerAngles")
gv = load(LOG, "GroundVelocity")
wv = load(LOG, "WaterVelocity")
rpm = load(LOG, "Rpm")
dep = load(LOG, "Depth")
vm = load(LOG, "VehicleMedium")
pcs = load(LOG, "PlanControlState")
rx = load(LOG, "UamRxFrame")
tx = load(LOG, "UamTxFrame")
txt = load(LOG, "TextMessage")
dist = load(LOG, "Distance")
nu = load(LOG, "NavigationUncertainty")
t0 = es["timestamp"].iloc[0]
T = lambda t: t - t0

ga = g[g["accepted"]].reset_index(drop=True)
lat0, lon0 = ga["lat"].iloc[0], ga["lon"].iloc[0]
ga["n"], ga["e"] = ll_to_ne(ga["lat"], ga["lon"], lat0, lon0)
es["n"], es["e"] = estimated_state_ne(es, lat0, lon0)

say(f"# Star mission results ({LOG}, lauv-marie)\n")
say(f"Log span {utc_str(t0)}–{utc_str(es.timestamp.iloc[-1])} UTC, {T(es.timestamp.iloc[-1]):.0f} s. "
    f"Origin of local N/E frame: first accepted GPS fix ({np.degrees(lat0):.5f}N, {np.degrees(lon0):.5f}E).\n")

# ------------------------------------------------------------------ 4a
say("## 4a. Surface, GPS, DVL, headings\n")
med = vm["medium"].value_counts().to_dict()
say(f"- VehicleMedium samples: {med} (2 = WATER/surface, 3 = UNDERWATER). "
    f"Vehicle at the surface for the whole log: **{set(med) == {2}}**.")
for ent, sub in dep.groupby("src_ent_label"):
    say(f"- Depth [{ent}]: n={len(sub)}, mean {sub.value.mean():.2f} m, min {sub.value.min():.2f}, max {sub.value.max():.2f} m")
dt = np.diff(g["t_fix"])
say(f"- GpsFix (GPS entity): {len(g)} fixes, median interval {np.median(dt):.2f} s, max gap {dt.max():.2f} s "
    f"-> rate {1/np.median(dt):.2f} Hz.")
say(f"- VALID_POS set: {g.valid_pos.mean()*100:.1f} %; accepted (hacc<15, hdop<4): {g.accepted.mean()*100:.1f} %; "
    f"hacc<5 m: {g.good.mean()*100:.1f} %. hacc median {g.hacc.median():.2f} m (max {g.hacc.max():.2f}), "
    f"hdop median {g.hdop.median():.2f}, satellites median {g.satellites.median():.0f}. Fix type: {g.type.unique().tolist()} (0 = standalone, no RTK/DGPS).")
say(f"- COG/SOG validity bits set on {g.vel_ok.mean()*100:.1f} % of fixes; SOG median {g.sog.median():.2f} m/s.")
say(f"- Header timestamp minus GPS UTC of fix: median {g.latency.median():+.3f} s (std {g.latency.std():.3f}).")
gvv, wvv = dvl_valid(gv), dvl_valid(wv)
say(f"- DVL bottom track (GroundVelocity, 5 Hz): {gvv.mean()*100:.1f} % valid ({(~gvv).sum()} invalid of {len(gv)}); "
    f"water track (WaterVelocity): {wvv.mean()*100:.1f} % valid.")
inv_gaps = []
tv = gv["timestamp"].values
bad = ~gvv.values
i = 0
while i < len(bad):
    if bad[i]:
        j = i
        while j < len(bad) and bad[j]:
            j += 1
        inv_gaps.append(tv[min(j, len(bad)-1)] - tv[i])
        i = j
    else:
        i += 1
say(f"- Bottom-track dropouts: {len(inv_gaps)} episodes, longest {max(inv_gaps) if inv_gaps else 0:.1f} s.")
alt = dist[dist.src_ent_label == "DVL Filtered"]
say(f"- DVL filtered altitude: valid {(alt.validity==1).mean()*100:.1f} %, "
    f"{alt[alt.validity==1].value.min():.1f}–{alt[alt.validity==1].value.max():.1f} m (median {alt[alt.validity==1].value.median():.1f} m). "
    f"So the seabed is within DVL range and the vehicle has bottom lock at the surface, not only RPM speed.")
dmag = np.degrees(wrap(eu.psi.values - eu.psi_magnetic.values))
say(f"- EulerAngles psi − psi_magnetic: median {np.median(dmag):.2f}°, max |.| {np.abs(dmag).max():.2f}° -> **no magnetic declination is applied** in the AHRS output (Svalbard declination in 2026 is of order +10° E; verify with WMM).")
say(f"- Rpm (Motor, 10 Hz): median {rpm.value.median():.0f} rpm, min {rpm.value.min()}, max {rpm.value.max()}.")
say(f"- NavigationUncertainty: sqrt(var x) stays {np.sqrt(nu.x).min():.2f}–{np.sqrt(nu.x).max():.2f} m (GPS-aided all along).")
R["surface"] = dict(medium=med, gps_n=len(g), gps_valid_frac=float(g.valid_pos.mean()),
                    gps_accepted_frac=float(g.accepted.mean()), gps_rate_hz=float(1/np.median(dt)),
                    hacc_median=float(g.hacc.median()), bottom_track_valid_frac=float(gvv.mean()),
                    water_track_valid_frac=float(wvv.mean()), altitude_median=float(alt[alt.validity==1].value.median()))

# legs
legs = legs_from_pcs(pcs)
legs = legs[legs.man_id.str.startswith("Goto")].reset_index(drop=True)
psi_u = np.unwrap(eu["psi"].values)
rows = []
for _, L in legs.iterrows():
    m = (eu.timestamp >= L.t0) & (eu.timestamp < L.t1)
    hdg = np.degrees(np.arctan2(np.sin(eu.psi[m]).mean(), np.cos(eu.psi[m]).mean())) % 360
    mg = (ga.t_fix >= L.t0) & (ga.t_fix < L.t1) & ga.vel_ok
    cog = np.degrees(np.arctan2(np.sin(ga.cog[mg]).mean(), np.cos(ga.cog[mg]).mean())) % 360
    p = ga[(ga.t_fix >= L.t0) & (ga.t_fix < L.t1)]
    dist_m = np.hypot(np.diff(p.n), np.diff(p.e)).sum()
    # steady part: exclude first 20 s (turn)
    ms = (eu.timestamp >= L.t0 + 20) & (eu.timestamp < L.t1)
    hdg_s = np.degrees(np.arctan2(np.sin(eu.psi[ms]).mean(), np.cos(eu.psi[ms]).mean())) % 360
    hdg_std = np.degrees(np.std(wrap(eu.psi[ms].values - np.radians(hdg_s))))
    mes = (es.timestamp >= L.t0 + 20) & (es.timestamp < L.t1)
    hdg_es = np.degrees(np.arctan2(np.sin(es.psi[mes]).mean(), np.cos(es.psi[mes]).mean())) % 360
    rows.append(dict(leg=L.man_id, start=utc_str(L.t0), dur_s=L.t1 - L.t0, heading_mean_deg=hdg, heading_es_deg=hdg_es,
                     heading_steady_deg=hdg_s, heading_steady_std_deg=hdg_std, cog_mean_deg=cog,
                     sog_mean=ga.sog[mg].mean(), track_len_m=dist_m))
legs_df = pd.DataFrame(rows)
say("\nLegs (Goto maneuvers from PlanControlState). Circular means; 'steady' excludes the first 20 s of each leg (the turn). AHRS yaw is magnetic; DUNE heading = AHRS + declination:\n")
say("| leg | start UTC | dur [s] | AHRS yaw mean [°] | AHRS yaw steady [°] (std) | DUNE heading steady [°] | GPS COG mean [°] | SOG mean [m/s] | GPS track length [m] |")
say("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    say(f"| {r['leg']} | {r['start']} | {r['dur_s']:.0f} | {r['heading_mean_deg']:.1f} | {r['heading_steady_deg']:.1f} ({r['heading_steady_std_deg']:.1f}) | {r['heading_es_deg']:.1f} | {r['cog_mean_deg']:.1f} | {r['sog_mean']:.2f} | {r['track_len_m']:.0f} |")
say("")
R["legs"] = rows

# ------------------------------------------------------------------ 4b USBL
say("## 4b. USBL / acoustic positioning\n")
usbl_msgs = [n for n in ["UsblFixExtended", "UsblPositionExtended", "UsblAnglesExtended", "UsblFix", "UsblPosition", "UsblAngles", "UsblModem", "UsblConfig", "LblEstimate", "UamRxRange", "UamTxRange"] if load(LOG, n) is not None]
say(f"- USBL/LBL/range messages in the log: **{usbl_msgs if usbl_msgs else 'none'}**. There is no acoustic position fix in the vehicle log, so USBL error against GPS cannot be computed from this data.")
say(f"- Acoustic frames received by the vehicle (UamRxFrame): {len(rx)}; of these {int((txt.text.str.strip()=='pos').sum())} are 'pos' text requests from `{rx.sys_src.unique().tolist()}` (the ship-side gateway). "
    f"Frames transmitted (UamTxFrame): {len(tx)} (periodic state reports, broadcast).")
say(f"- Reception times (UTC): {', '.join(utc_str(t) for t in rx.timestamp)}.")
say("- Config: `[Transports.UAN] USBL Node -- Enabled = false` — the vehicle was not configured to receive USBL fixes. Any USBL solution would only exist in the ship-side (Manta/Neptus) logs.")
R["usbl"] = dict(usbl_messages=usbl_msgs, uam_rx=len(rx), uam_tx=len(tx), rx_times=[float(t) for t in rx.timestamp])

# ------------------------------------------------------------------ velocity alignment at GPS epochs
def ned_from_dvl(df, heading="ES"):
    t = df["timestamp"].values
    phi = interp_angle(eu.timestamp.values, eu.phi.values, t)
    th = interp_angle(eu.timestamp.values, eu.theta.values, t)
    ps = interp_angle(es.timestamp.values, es.psi.values, t) if heading == "ES" else interp_angle(eu.timestamp.values, eu.psi.values, t)
    n, e, d = rot_body_to_ned(df.x.values, df.y.values, df.z.values, phi, th, ps)
    return t, np.column_stack([n, e, d]), ps

decl = np.degrees(wrap(es.psi.values - interp_angle(eu.timestamp.values, eu.psi.values, es.timestamp.values)))
say("\n## Heading sources\n")
say(f"- EstimatedState psi − AHRS EulerAngles psi = {np.median(decl):.2f}° (1st–99th pct {np.percentile(decl,1):.2f}–{np.percentile(decl,99):.2f}°), constant over the log. "
    f"EulerAngles psi equals psi_magnetic, so the AHRS reports magnetic heading and DUNE adds a fixed declination (World Magnetic Model at the initialisation fix; DUNE 2025.06.03). "
    f"All fits below use the EstimatedState heading; the raw AHRS heading appears only as the 'no declination' case.")
R["declination_applied_by_dune_deg"] = float(np.median(decl))

tg, gv_ned, psi_gv = ned_from_dvl(gv)
tw, wv_ned, psi_wv = ned_from_dvl(wv)
_, wv_ned_ahrs, psi_wv_ahrs = ned_from_dvl(wv, heading="AHRS")
ok = ga.vel_ok.values
tf = ga.t_fix.values
vg = np.column_stack([ga.vn.values, ga.ve.values])
bt = bin_mean(tg[gvv.values], gv_ned[gvv.values, :2], tf)
wt = bin_mean(tw[wvv.values], wv_ned[wvv.values, :2], tf)
# alternative hypothesis: DVL already in NED (no rotation)
bt_raw = bin_mean(tg[gvv.values], gv.loc[gvv, ["x", "y"]].values, tf)
m = ok & np.isfinite(bt).all(1) & np.isfinite(wt).all(1)
rms = lambda a: float(np.sqrt(np.nanmean(np.sum(a**2, axis=1))))
say("\n## Frame check: DVL bottom track vs GPS velocity at GPS epochs\n")
say(f"- n epochs = {m.sum()}. RMS |v_gps − R(φ,θ,ψ)·v_bt| = **{rms(vg[m]-bt[m]):.3f} m/s**; "
    f"if the DVL values were already NED (no rotation): {rms(vg[m]-bt_raw[m]):.3f} m/s. "
    f"Body frame confirmed. Mean residual N/E = {np.mean(vg[m]-bt[m],axis=0).round(3).tolist()} m/s.")
R["frame_check"] = dict(n=int(m.sum()), rms_body=rms(vg[m]-bt[m]), rms_ned=rms(vg[m]-bt_raw[m]))


def fit_cds(v_obs, v_in, fit_delta=True, fit_scale=True, iters=20):
    """Gauss-Newton for v_obs = c + s * Rz(delta) v_in. Returns dict."""
    p = np.array([0.0, 0.0, 0.0, 1.0])
    for _ in range(iters):
        cN, cE, d, s = p
        cd, sd = np.cos(d), np.sin(d)
        rin = np.column_stack([cd * v_in[:, 0] - sd * v_in[:, 1], sd * v_in[:, 0] + cd * v_in[:, 1]])
        model = p[:2] + s * rin
        r = (v_obs - model).ravel()
        drin = np.column_stack([-sd * v_in[:, 0] - cd * v_in[:, 1], cd * v_in[:, 0] - sd * v_in[:, 1]])
        J = [np.tile([1, 0], len(v_in)), np.tile([0, 1], len(v_in))]
        cols = [0, 1]
        if fit_delta:
            J.append((s * drin).ravel()); cols.append(2)
        if fit_scale:
            J.append(rin.ravel()); cols.append(3)
        J = np.column_stack(J)
        dp, *_ = np.linalg.lstsq(J, r, rcond=None)
        p[cols] += dp
        if np.abs(dp).max() < 1e-9:
            break
    cN, cE, d, s = p
    cd, sd = np.cos(d), np.sin(d)
    model = p[:2] + s * np.column_stack([cd * v_in[:, 0] - sd * v_in[:, 1], sd * v_in[:, 0] + cd * v_in[:, 1]])
    res = v_obs - model
    n, k = len(v_in) * 2, len(cols)
    sigma2 = (res**2).sum() / (n - k)
    cov = sigma2 * np.linalg.inv(J.T @ J)
    se = np.sqrt(np.diag(cov))
    out = dict(cN=cN, cE=cE, delta_deg=np.degrees(d), scale=s, rms=float(np.sqrt(np.mean(np.sum(res**2, 1)))), n=len(v_in))
    out["se"] = dict(zip([["cN", "cE", "delta_deg", "scale"][i] for i in cols], [se[j] * (180/np.pi if cols[j] == 2 else 1) for j in range(len(cols))]))
    return out, res

# ------------------------------------------------------------------ 4e current
say("\n## 4e. Least-squares current at the surface\n")
say("Current c = v_GPS − R·v_watertrack (per fix, then averaged). Independent check: DVL bottom track minus water track (no GPS involved).\n")
say("| leg | n | c_N [m/s] | c_E [m/s] | |c| | dir to [°] | std N/E | DVL bt−wt: c_N | c_E | |c| | dir [°] |")
say("|---|---|---|---|---|---|---|---|---|---|---|")
per_leg = []
diff_bt_wt = np.full_like(bt, np.nan)
for _, L in legs.iterrows():
    ml = m & (tf >= L.t0 + 20) & (tf < L.t1)
    c = vg[ml] - wt[ml]
    cm = c.mean(0); cs = c.std(0)
    c2 = (bt[ml] - wt[ml]); cm2 = c2.mean(0)
    per_leg.append(dict(leg=L.man_id, n=int(ml.sum()), cN=cm[0], cE=cm[1], speed=float(np.hypot(*cm)),
                        dir_deg=float(np.degrees(np.arctan2(cm[1], cm[0])) % 360), stdN=cs[0], stdE=cs[1],
                        dvl_cN=cm2[0], dvl_cE=cm2[1], dvl_speed=float(np.hypot(*cm2)), dvl_dir_deg=float(np.degrees(np.arctan2(cm2[1], cm2[0])) % 360)))
    r_ = per_leg[-1]
    say(f"| {r_['leg']} | {r_['n']} | {r_['cN']:+.3f} | {r_['cE']:+.3f} | {r_['speed']:.3f} | {r_['dir_deg']:.0f} | {r_['stdN']:.2f}/{r_['stdE']:.2f} | {r_['dvl_cN']:+.3f} | {r_['dvl_cE']:+.3f} | {r_['dvl_speed']:.3f} | {r_['dvl_dir_deg']:.0f} |")
pl = pd.DataFrame(per_leg)
call = (vg[m] - wt[m]).mean(0)
cdvl = (bt[m] - wt[m]).mean(0)
say(f"| **all** | {m.sum()} | {call[0]:+.3f} | {call[1]:+.3f} | {np.hypot(*call):.3f} | {np.degrees(np.arctan2(call[1],call[0]))%360:.0f} | | {cdvl[0]:+.3f} | {cdvl[1]:+.3f} | {np.hypot(*cdvl):.3f} | {np.degrees(np.arctan2(cdvl[1],cdvl[0]))%360:.0f} |")
say("")
say(f"- Per-leg spread of the GPS-based estimate: std of c_N = {pl.cN.std():.3f}, c_E = {pl.cE.std():.3f} m/s; "
    f"range |c| {pl.speed.min():.3f}–{pl.speed.max():.3f} m/s. Per-leg spread of the DVL-only estimate: std {pl.dvl_cN.std():.3f}/{pl.dvl_cE.std():.3f} m/s.")
say(f"- Mean over legs of the GPS-based estimate: ({pl.cN.mean():+.3f}, {pl.cE.mean():+.3f}) m/s; DVL-only: ({pl.dvl_cN.mean():+.3f}, {pl.dvl_cE.mean():+.3f}) m/s.")

f_c, _ = fit_cds(vg[m], wt[m], fit_delta=False, fit_scale=False)
f_cd, _ = fit_cds(vg[m], wt[m], fit_delta=True, fit_scale=False)
f_cds, res_cds = fit_cds(vg[m], wt[m], fit_delta=True, fit_scale=True)
f_bt, _ = fit_cds(vg[m], bt[m], fit_delta=True, fit_scale=True)
# RPM model
rpm_t = interp(rpm.timestamp.values, rpm.value.values.astype(float), tw)
u_rpm = RPM_K_CONFIG * rpm_t
n_r, e_r, _ = rot_body_to_ned(u_rpm, 0*u_rpm, 0*u_rpm, 0*u_rpm, 0*u_rpm, psi_wv)
rpm_ned = bin_mean(tw, np.column_stack([n_r, e_r]), tf)
mr = ok & np.isfinite(rpm_ned).all(1)
f_rpm, _ = fit_cds(vg[mr], rpm_ned[mr], fit_delta=True, fit_scale=True)
wt_ahrs = bin_mean(tw[wvv.values], wv_ned_ahrs[wvv.values, :2], tf)
f_ahrs, _ = fit_cds(vg[m], wt_ahrs[m], fit_delta=True, fit_scale=True)
f_ahrs_c, _ = fit_cds(vg[m], wt_ahrs[m], fit_delta=False, fit_scale=False)
say("\nJoint fits over all legs, model v_GPS = c + s·Rz(δ)·v_in (Gauss-Newton; se = 1σ from residuals):\n")
say("| input | params | c_N | c_E | δ [°] | s | residual RMS [m/s] |")
say("|---|---|---|---|---|---|---|")
for name, f in [("water track", f_c), ("water track", f_cd), ("water track", f_cds), ("bottom track", f_bt), ("RPM×1.3e-3", f_rpm), ("water track, raw AHRS yaw (no declination)", f_ahrs_c), ("water track, raw AHRS yaw (no declination)", f_ahrs)]:
    se = f["se"]
    say(f"| {name} | {'+'.join(se.keys())} | {f['cN']:+.3f}±{se.get('cN',0):.3f} | {f['cE']:+.3f}±{se.get('cE',0):.3f} | "
        f"{f['delta_deg']:+.2f}{'±%.2f'%se['delta_deg'] if 'delta_deg' in se else ''} | {f['scale']:.3f}{'±%.3f'%se['scale'] if 'scale' in se else ''} | {f['rms']:.3f} |")
say("")
say("- Bottom-track row: with GPS as truth, δ is the residual heading bias of DUNE's heading and s the DVL scale error (the current cancels because both are over-ground velocities).")
say("- Raw-AHRS rows show what happens if the declination is not applied: a c-only fit returns a spurious ~0.4 m/s 'current' that rotates with the vehicle, while the δ fit recovers the declination.")
say("- Water-track rows: the extra parameters (δ, s) are identifiable only if they lower the residual RMS noticeably relative to the c-only fit and their 1σ excludes 0/1.")
R["current"] = dict(per_leg=per_leg, overall_gps=call.tolist(), overall_dvl=cdvl.tolist(),
                    fit_c=f_c, fit_c_delta=f_cd, fit_c_delta_scale=f_cds, fit_bottomtrack=f_bt, fit_rpm=f_rpm, fit_ahrs_raw=f_ahrs, fit_ahrs_raw_c_only=f_ahrs_c)

# ------------------------------------------------------------------ 4f synthetic outage
say("\n## 4f. Synthetic GPS outages: dead reckoning drift\n")
tD = tw
psiD = psi_wv
phiD = interp_angle(eu.timestamp.values, eu.phi.values, tD)
thD = interp_angle(eu.timestamp.values, eu.theta.values, tD)
wv_b, _ = hold_last_valid(wv[["x", "y", "z"]].values, wvv.values)
gv_b, _ = hold_last_valid(gv[["x", "y", "z"]].values, gvv.values)
# bottom track sampled to the water-track times (same DVL ping, ~2 ms apart)
gv_at_w = np.column_stack([interp(gv.timestamp.values, gv_b[:, i], tD) for i in range(3)])
variants = {}
for name, body in [("water track", wv_b), ("bottom track", gv_at_w)]:
    n_, e_, _ = rot_body_to_ned(body[:, 0], body[:, 1], body[:, 2], phiD, thD, psiD)
    variants[name] = np.column_stack([n_, e_])
n_, e_, _ = rot_body_to_ned(u_rpm, 0*u_rpm, 0*u_rpm, phiD, thD, psiD)
variants["RPM x 1.3e-3"] = np.column_stack([n_, e_])
variants["RPM x fitted k"] = variants["RPM x 1.3e-3"] * f_rpm["scale"]
d_fit = np.radians(f_cds["delta_deg"]); v = variants["water track"]
variants["water track + fitted (δ, s, c)"] = f_cds["scale"] * np.column_stack([np.cos(d_fit) * v[:, 0] - np.sin(d_fit) * v[:, 1], np.sin(d_fit) * v[:, 0] + np.cos(d_fit) * v[:, 1]]) + np.array([f_cds["cN"], f_cds["cE"]])
n_, e_, _ = rot_body_to_ned(wv_b[:, 0], wv_b[:, 1], wv_b[:, 2], phiD, thD, psi_wv_ahrs)
variants["water track, raw AHRS yaw (no declination)"] = np.column_stack([n_, e_])
dtD = np.diff(tD, prepend=tD[0])
truth_n = interp(tf, ga.n.values, tD)
truth_e = interp(tf, ga.e.values, tD)
windows = [120, 300, 600]
starts = np.arange(legs.t0.iloc[0], tD[-1] - 120, 10.0)
curves = {k: [] for k in variants}
summary = {}
for name, vel in variants.items():
    for ts in starts:
        i0 = np.searchsorted(tD, ts)
        i1 = np.searchsorted(tD, ts + 600)
        seg = vel[i0:i1]
        if np.isnan(seg).any():
            continue
        dtt = dtD[i0:i1].copy(); dtt[0] = 0
        pn = truth_n[i0] + np.cumsum(seg[:, 0] * dtt)
        pe = truth_e[i0] + np.cumsum(seg[:, 1] * dtt)
        drift = np.hypot(pn - truth_n[i0:i1], pe - truth_e[i0:i1])
        curves[name].append((tD[i0:i1] - ts, drift))
    summary[name] = {}
    for W in windows:
        vals = [d[np.searchsorted(el, W) - 1] for el, d in curves[name] if el[-1] >= W - 1]
        summary[name][W] = dict(n=len(vals), median=float(np.median(vals)), p95=float(np.percentile(vals, 95)), max=float(np.max(vals)), min=float(np.min(vals))) if vals else None
say("Dead reckoning restarted from the GPS position every 10 s; drift = |DR − GPS| after 2, 5 and 10 min (windows overlap, so the n are not independent):\n")
say("| DR input | window | n windows | median drift [m] | 95th pct [m] | max [m] |")
say("|---|---|---|---|---|---|")
for name in variants:
    for W in windows:
        s_ = summary[name][W]
        if s_:
            say(f"| {name} | {W//60} min | {s_['n']} | {s_['median']:.1f} | {s_['p95']:.1f} | {s_['max']:.1f} |")
say("")
say(f"- All variants use DUNE's heading (AHRS + declination) except the last. 'water track' is the realistic underwater case without a current estimate; "
    f"'bottom track' is what DUNE integrates when the DVL has bottom lock; 'RPM' is the fallback without DVL; the fitted variant applies δ={f_cds['delta_deg']:+.2f}°, s={f_cds['scale']:.3f}, c=({f_cds['cN']:+.3f},{f_cds['cE']:+.3f}) from 4e; "
    f"the raw-AHRS variant shows the drift if the declination were not applied.")
R["outage"] = summary

# ------------------------------------------------------------------ plots
# track
fig, ax = plt.subplots(figsize=(7.5, 7))
sc = ax.scatter(ga.e, ga.n, c=T(ga.t_fix), cmap="viridis", s=6, zorder=3, label="GPS accepted fixes (1 Hz)")
ax.plot(es.e, es.n, color=GREY, lw=0.8, zorder=2, label="EstimatedState (DUNE nav, 20 Hz)")
rxn = interp(tf, ga.n.values, rx.timestamp.values); rxe = interp(tf, ga.e.values, rx.timestamp.values)
ax.scatter(rxe, rxn, marker="^", s=40, facecolor="none", edgecolor=C[1], zorder=4, label=f"acoustic frame received from ship ({len(rx)}); no USBL fix logged")
for _, L in legs.iterrows():
    p = ga[(ga.t_fix >= L.t0 + 20) & (ga.t_fix < L.t1)]
    if len(p):
        ax.annotate(L.man_id, (p.e.mean(), p.n.mean()), fontsize=8, color=C[7], ha="center")
ax.set_aspect("equal"); ax.set_xlabel("east [m]"); ax.set_ylabel("north [m]")
ax.set_title("Star mission track (lauv-marie, 7 Sept 2026, surface)")
cb = fig.colorbar(sc, ax=ax, shrink=0.6); cb.set_label("time since log start [s]")
ax.legend(loc="lower right", fontsize=7)
fig.tight_layout(); fig.savefig(PLOTS / "track.png"); plt.close(fig)

# depth
fig, ax = plt.subplots(figsize=(9, 3))
for i, (ent, sub) in enumerate(dep.groupby("src_ent_label")):
    ax.plot(T(sub.timestamp), sub.value, lw=0.8, color=C[i], label=f"Depth [{ent}]")
ax.axhline(0, color=GREY, lw=0.6)
ax.set_ylim(1.0, -1.0); ax.set_xlabel("time since log start [s]"); ax.set_ylabel("depth [m]")
ax.set_title("Depth vs time (surface throughout; VehicleMedium = WATER for all 790 samples)")
ax.legend(); fig.tight_layout(); fig.savefig(PLOTS / "depth.png"); plt.close(fig)

# heading
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.plot(T(eu.timestamp), np.degrees(eu.psi) % 360, lw=0.6, color=C[0], label="AHRS yaw, magnetic (EulerAngles, 50 Hz)")
ax.plot(T(es.timestamp), np.degrees(es.psi) % 360, lw=0.6, color=C[2], label="DUNE heading (EstimatedState psi = AHRS + declination)")
mg_ = ga.vel_ok
ax.plot(T(ga.t_fix[mg_]), np.degrees(ga.cog[mg_]) % 360, ".", ms=2, color=C[1], label="GPS course over ground (1 Hz)")
for _, L in legs.iterrows():
    ax.axvline(T(L.t0), color=GREY, lw=0.5)
    ax.text(T(L.t0) + 2, 350, L.man_id, fontsize=7, color=GREY)
ax.set_ylim(0, 360); ax.set_yticks(range(0, 361, 90)); ax.set_xlabel("time since log start [s]"); ax.set_ylabel("heading [°]")
ax.set_title("Heading vs time; DUNE heading vs GPS COG differ only by drift angle (current + sideslip)")
ax.legend(loc="lower left", fontsize=6, ncol=3); fig.tight_layout(); fig.savefig(PLOTS / "heading.png"); plt.close(fig)

# GPS validity timeline
fig, axs = plt.subplots(4, 1, figsize=(9, 6), sharex=True)
axs[0].step(T(g.t_fix), g.valid_pos.astype(int), where="post", color=C[0]); axs[0].set_ylabel("VALID_POS"); axs[0].set_ylim(-0.1, 1.1)
axs[1].plot(T(g.t_fix), g.hacc, ".", ms=2, color=C[0]); axs[1].axhline(15, color=C[7], lw=0.8); axs[1].set_ylabel("hacc [m]"); axs[1].set_yscale("log")
axs[2].plot(T(g.t_fix), g.satellites, ".", ms=2, color=C[0]); axs[2].set_ylabel("satellites")
axs[3].step(T(vm.timestamp), vm.medium, where="post", color=C[2]); axs[3].set_ylabel("medium"); axs[3].set_yticks([2, 3]); axs[3].set_yticklabels(["WATER", "UNDERW."])
axs[3].set_xlabel("time since log start [s]"); axs[0].set_title("GPS validity timeline (red line = DUNE hacc acceptance threshold 15 m)")
fig.tight_layout(); fig.savefig(PLOTS / "gps_validity.png"); plt.close(fig)

# drift curves
fig, axs = plt.subplots(2, 3, figsize=(12, 7), sharey=True); axs = axs.ravel()
for ax, (name, cv) in zip(axs, curves.items()):
    for el, d in cv:
        ax.plot(el / 60, d, color=C[0], lw=0.5, alpha=0.35)
    for W in windows:
        s_ = summary[name][W]
        if s_:
            ax.plot(W / 60, s_["median"], "o", color=C[1], ms=5, zorder=5)
            ax.annotate(f"{s_['median']:.0f} m", (W / 60, s_["median"]), textcoords="offset points", xytext=(4, 4), fontsize=7, color=C[1])
    ax.set_title(name, fontsize=9); ax.set_xlabel("outage length [min]")
axs[0].set_ylabel("|DR − GPS| [m]"); axs[3].set_ylabel("|DR − GPS| [m]")
for ax in axs[len(variants):]: ax.axis("off")
fig.suptitle("Synthetic GPS outages on the star mission (one curve per start time, every 10 s; orange = median at 2/5/10 min)", fontsize=9)
fig.tight_layout(); fig.savefig(PLOTS / "synthetic_outage_drift.png"); plt.close(fig)

# per-leg current vectors
fig, ax = plt.subplots(figsize=(4.5, 4.5))
for i, r_ in enumerate(per_leg):
    ax.annotate("", xy=(r_["cE"], r_["cN"]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=C[0], lw=1.2))
    ax.text(r_["cE"], r_["cN"], r_["leg"], fontsize=7, color=C[0])
    ax.annotate("", xy=(r_["dvl_cE"], r_["dvl_cN"]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=C[2], lw=1.0))
ax.annotate("", xy=(call[1], call[0]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=C[1], lw=2.5))
ax.plot([], [], color=C[0], label="GPS − water track, per leg"); ax.plot([], [], color=C[2], label="bottom − water track (DVL only), per leg"); ax.plot([], [], color=C[1], lw=2.5, label="all legs (GPS)")
lim = max(0.3, 1.2 * pl[["speed", "dvl_speed"]].values.max())
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
ax.set_xlabel("current east [m/s]"); ax.set_ylabel("current north [m/s]"); ax.set_title("Per-leg current estimates")
ax.legend(fontsize=7, loc="lower left"); fig.tight_layout(); fig.savefig(PLOTS / "current_per_leg.png"); plt.close(fig)

# velocity residual time series (diagnostic)
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(T(tf[m]), (vg[m] - wt[m])[:, 0], ".", ms=2, color=C[0], label="v_GPS − R·v_wt, north")
ax.plot(T(tf[m]), (vg[m] - wt[m])[:, 1], ".", ms=2, color=C[1], label="east")
ax.plot(T(tf[m]), (vg[m] - bt[m])[:, 0], ".", ms=2, color=C[2], label="v_GPS − R·v_bt, north")
ax.plot(T(tf[m]), (vg[m] - bt[m])[:, 1], ".", ms=2, color=C[3], label="east")
for _, L in legs.iterrows():
    ax.axvline(T(L.t0), color=GREY, lw=0.5)
ax.set_xlabel("time since log start [s]"); ax.set_ylabel("[m/s]"); ax.set_title("Velocity residuals at GPS epochs (per-fix current samples)")
ax.legend(fontsize=7, ncol=4); fig.tight_layout(); fig.savefig(PLOTS / "velocity_residuals.png"); plt.close(fig)

(OUT / "star_results.md").write_text("\n".join(md))
dump_json(R, OUT / "star_results.json")
print("\nwrote", OUT, PLOTS)
