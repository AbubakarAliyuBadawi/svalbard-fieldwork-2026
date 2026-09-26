"""
Build 1 Hz observation windows from the extracted CSV tables of the field logs.

Sets written to data/windows.npz:
    star            Marie star, DUNE heading, GPS + water track + bottom track   (calibration set)
    star_raw        same windows with the raw magnetic AHRS heading (declination omitted)
    sidescan_dive   Marie sidescan, submerged: water + bottom track, no GPS
    thor_surface    Thor surface runs: GPS + (flag-invalid) water track, no bottom track
    thor_dive       Thor submerged: water track only
Also writes data/programmes.npz: (psi, rpm) sequences from all logs used to drive the simulator.

Construction (no smoothing beyond 1 s bin means):
    heading    EstimatedState psi (DUNE heading) -> cos, sin ; 'raw' uses EulerAngles psi
    wt_u, wt_v WaterVelocity x, y, mean of samples with validity==7 (Thor: x > -30) in the bin
    bt_u, bt_v GroundVelocity x, y, validity==7
    rpm_k      Rpm value / 1000
    gps_vn/ve  sog*cos(cog), sog*sin(cog) of accepted fixes (VALID_POS, hacc<15, hdop<4, COG/SOG valid)
    masks      1 where the bin has data, else 0 and the value is 0
Windows are 120 s long with a stride of 30 s; a window is kept if the DVL mask covers >= 80 %
(thor_surface: medium WATER with an accepted GPS fix on >= 90 % of the seconds).
Reference theta for each set comes from the least-squares fits in analysis/*/results/*.json.
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd

from config import ANALYSIS, DATA, LOGS, T, C, CHANNELS
from simulator import IDX

STRIDE = 30
star_res = json.loads((ANALYSIS / LOGS["star"] / "results" / "star_results.json").read_text())
thor_res = json.loads((ANALYSIS / LOGS["thor"] / "results" / "dive_results.json").read_text())


def load(log, name):
    return pd.read_csv(ANALYSIS / log / "csv" / f"{name}.csv")


def bin_mean(t, v, edges):
    """mean of v in each [edges[i], edges[i+1]); NaN where empty"""
    idx = np.searchsorted(edges, t, side="right") - 1
    ok = (idx >= 0) & (idx < len(edges) - 1)
    out = np.full((len(edges) - 1,) + v.shape[1:], np.nan)
    cnt = np.zeros(len(edges) - 1)
    np.add.at(cnt, idx[ok], 1)
    acc = np.zeros_like(out)
    np.add.at(acc, idx[ok], v[ok])
    nz = cnt > 0
    out[nz] = acc[nz] / cnt[nz][:, None] if v.ndim > 1 else acc[nz] / cnt[nz]
    return out


def series_1hz(log: str, heading: str = "es"):
    es = load(log, "EstimatedState"); eu = load(log, "EulerAngles")
    wv = load(log, "WaterVelocity"); gv = load(log, "GroundVelocity"); rpm = load(log, "Rpm")
    g = load(log, "GpsFix"); g = g[g.src_ent_label == "GPS"].copy()
    vm = load(log, "VehicleMedium")
    t0 = np.floor(es.timestamp.iloc[0]); t1 = np.ceil(es.timestamp.iloc[-1])
    edges = np.arange(t0, t1 + 1, 1.0)
    n = len(edges) - 1
    src = es if heading == "es" else eu
    psi_u = np.unwrap(src.psi.values)
    cs = bin_mean(src.timestamp.values, np.column_stack([np.cos(psi_u), np.sin(psi_u)]), edges)
    psi = np.arctan2(cs[:, 1], cs[:, 0])
    thor = "Thor" in log or "YoYo" in log
    wv_ok = (wv.x > -30) if thor else (wv.validity == 7)
    wt = bin_mean(wv.timestamp.values[wv_ok], wv[["x", "y"]].values[wv_ok], edges)
    gv_ok = gv.validity == 7
    bt = bin_mean(gv.timestamp.values[gv_ok], gv[["x", "y"]].values[gv_ok], edges)
    r = bin_mean(rpm.timestamp.values, rpm.value.values.astype(float), edges)
    day0 = pd.to_datetime(dict(year=g.utc_year, month=g.utc_month, day=g.utc_day), utc=True)
    t_fix = (day0 - pd.Timestamp(0, tz="UTC")).dt.total_seconds() + g.utc_time   # explicit seconds (pandas>=3 changes astype(int64) resolution)
    acc = ((g.validity & 0x4) > 0) & (g.hacc < 15) & (g.hdop < 4) & ((g.validity & 0x18) == 0x18)
    vg = bin_mean(t_fix.values[acc], np.column_stack([g.sog * np.cos(g.cog), g.sog * np.sin(g.cog)]).astype(float)[acc], edges)
    med = bin_mean(vm.timestamp.values, vm.medium.values.astype(float), edges)
    x = np.zeros((n, C))
    x[:, IDX["cos_psi"]] = np.cos(psi); x[:, IDX["sin_psi"]] = np.sin(psi)
    m_dvl = np.isfinite(wt[:, 0]); x[:, IDX["wt_u"]] = np.where(m_dvl, wt[:, 0], 0); x[:, IDX["wt_v"]] = np.where(m_dvl, wt[:, 1], 0); x[:, IDX["m_dvl"]] = m_dvl
    m_bt = np.isfinite(bt[:, 0]); x[:, IDX["bt_u"]] = np.where(m_bt, bt[:, 0], 0); x[:, IDX["bt_v"]] = np.where(m_bt, bt[:, 1], 0); x[:, IDX["m_bt"]] = m_bt
    x[:, IDX["rpm_k"]] = np.where(np.isfinite(r), r, 0) / 1000
    m_gps = np.isfinite(vg[:, 0]); x[:, IDX["gps_vn"]] = np.where(m_gps, vg[:, 0], 0); x[:, IDX["gps_ve"]] = np.where(m_gps, vg[:, 1], 0); x[:, IDX["m_gps"]] = m_gps
    heading_ok = np.isfinite(psi)
    return x, edges[:-1], heading_ok, med


def cut(x, t, ok, cond, min_cond=1.0):
    """windows of length T with stride STRIDE where cond (per second) holds on >= min_cond of the window"""
    out, starts = [], []
    for s in range(0, len(t) - T + 1, STRIDE):
        w = x[s:s + T]
        if ok[s:s + T].all() and cond[s:s + T].mean() >= min_cond and w[:, IDX["m_dvl"]].mean() >= 0.8:
            out.append(w); starts.append(t[s])
    return np.array(out), np.array(starts)


def main():
    sets, meta = {}, {}
    fc = star_res["current"]["fit_c_delta_scale"]
    ref_star = np.array([fc["delta_deg"], fc["scale"], fc["cN"], fc["cE"], np.log10(fc["rms"])])
    fr = star_res["current"]["fit_ahrs_raw"]
    ref_star_raw = np.array([fr["delta_deg"], fr["scale"], fr["cN"], fr["cE"], np.log10(fr["rms"])])
    tw = thor_res["gps"]["corrections"]["water"]
    ref_thor = np.array([tw["delta_deg"], tw["scale"], tw["cN"], tw["cE"], np.log10(tw["rms"])])

    x, t, ok, med = series_1hz(LOGS["star"], "es")
    sets["star"], meta["star"] = cut(x, t, ok, med == 2)
    x, t, ok, med = series_1hz(LOGS["star"], "raw")
    sets["star_raw"], meta["star_raw"] = cut(x, t, ok, med == 2)
    x, t, ok, med = series_1hz(LOGS["sidescan"], "es")
    sets["sidescan_dive"], meta["sidescan_dive"] = cut(x, t, ok, med == 3)
    x, t, ok, med = series_1hz(LOGS["thor"], "es")
    sets["thor_surface"], meta["thor_surface"] = cut(x, t, ok, (med == 2) & (x[:, IDX["m_gps"]] > 0), min_cond=0.9)
    sets["thor_dive"], meta["thor_dive"] = cut(x, t, ok, med == 3)
    refs = {"star": ref_star, "star_raw": ref_star_raw, "sidescan_dive": ref_star, "thor_surface": ref_thor, "thor_dive": ref_thor}
    out = {}
    for k in sets:
        out[f"x_{k}"] = sets[k].astype("float32"); out[f"t0_{k}"] = meta[k]; out[f"ref_{k}"] = refs[k]
        print(f"{k:14s} {len(sets[k]):4d} windows   ref theta = {np.round(refs[k], 3)}")
    np.savez(DATA / "windows.npz", channels=np.array(CHANNELS), **out)

    # programmes for the simulator: (psi, rpm) 1 Hz sequences from all three logs
    progs = []
    for name in LOGS.values():
        x, t, ok, med = series_1hz(name, "es")
        psi = np.arctan2(x[:, IDX["sin_psi"]], x[:, IDX["cos_psi"]]); rpm = x[:, IDX["rpm_k"]] * 1000
        good = ok & (rpm > 300)
        # contiguous runs of good samples
        s = 0
        while s < len(t):
            if good[s]:
                e = s
                while e < len(t) and good[e]: e += 1
                if e - s >= T:
                    progs.append(np.column_stack([np.unwrap(psi[s:e]), rpm[s:e]]))
                s = e
            else:
                s += 1
    np.savez(DATA / "programmes.npz", **{f"p{i}": p for i, p in enumerate(progs)})
    print(f"{len(progs)} heading/rpm programmes, {sum(len(p) for p in progs)} s total")


if __name__ == "__main__":
    main()
