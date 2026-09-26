"""
Shared helpers for the feasibility analysis. No smoothing/filtering lives here; every
function is a plain transform (frame rotation, geodesy, time alignment by binning).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis"

# categorical palette, fixed order (dataviz reference palette, light mode)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
GREY = "#8a8985"
plt.rcParams.update({
    "figure.dpi": 100, "savefig.dpi": 300, "font.size": 9, "axes.grid": True,
    "grid.color": "#e6e5e1", "grid.linewidth": 0.6, "axes.edgecolor": "#c3c2b7",
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.2,
    "legend.frameon": False,
})

# GPS acceptance used throughout, mirroring the DUNE Navigation.AUV.Navigation thresholds
# (GPS Maximum HACC = 15 m, GPS Maximum HDOP = 4) plus the receiver's own VALID_POS bit.
GPS_MAX_HACC = 15.0
GPS_MAX_HDOP = 4.0
GPS_GOOD_HACC = 5.0     # "precise" fix used when a truth position is needed

VALID_POS, VALID_COG, VALID_SOG = 0x0004, 0x0008, 0x0010

# WGS84
_A, _F = 6378137.0, 1 / 298.257223563
_E2 = _F * (2 - _F)


def load(log: str, name: str) -> pd.DataFrame | None:
    p = ANALYSIS / log / "csv" / f"{name}.csv"
    return pd.read_csv(p) if p.exists() else None


def radii(lat0: float):
    s = np.sin(lat0) ** 2
    rn = _A / np.sqrt(1 - _E2 * s)
    rm = _A * (1 - _E2) / (1 - _E2 * s) ** 1.5
    return rm, rn


def ll_to_ne(lat, lon, lat0, lon0):
    """rad -> local north/east metres about (lat0, lon0). Adequate for a few km."""
    rm, rn = radii(lat0)
    return (np.asarray(lat) - lat0) * rm, (np.asarray(lon) - lon0) * rn * np.cos(lat0)


def estimated_state_ne(es: pd.DataFrame, lat0, lon0):
    """EstimatedState absolute position: reference (lat, lon) displaced by (x north, y east)."""
    n, e = ll_to_ne(es["lat"].values, es["lon"].values, lat0, lon0)
    return n + es["x"].values, e + es["y"].values


def gps_prepare(g: pd.DataFrame) -> pd.DataFrame:
    """GpsFix rows from the GPS entity with derived fields. t_fix = GPS UTC time of fix,
    used as the epoch on the vehicle clock (DUNE syncs the clock to GPS; the header
    timestamp lags by the NMEA/network latency measured in inventory.md)."""
    g = g[g["src_ent_label"] == "GPS"].copy()
    day0 = pd.to_datetime(dict(year=g.utc_year, month=g.utc_month, day=g.utc_day), utc=True)
    g["t_fix"] = (day0 - pd.Timestamp(0, tz="UTC")).dt.total_seconds() + g["utc_time"]
    g["latency"] = g["timestamp"] - g["t_fix"]
    g["valid_pos"] = (g["validity"] & VALID_POS) > 0
    g["accepted"] = g["valid_pos"] & (g["hacc"] < GPS_MAX_HACC) & (g["hdop"] < GPS_MAX_HDOP)
    g["good"] = g["accepted"] & (g["hacc"] < GPS_GOOD_HACC)
    g["vn"] = g["sog"] * np.cos(g["cog"])
    g["ve"] = g["sog"] * np.sin(g["cog"])
    g["vel_ok"] = ((g["validity"] & VALID_COG) > 0) & ((g["validity"] & VALID_SOG) > 0)
    return g


def rot_body_to_ned(x, y, z, phi, theta, psi):
    """Full ZYX rotation of body-frame vectors (x fwd, y stbd, z down) to NED."""
    cph, sph = np.cos(phi), np.sin(phi)
    cth, sth = np.cos(theta), np.sin(theta)
    cps, sps = np.cos(psi), np.sin(psi)
    n = (cps * cth) * x + (cps * sth * sph - sps * cph) * y + (cps * sth * cph + sps * sph) * z
    e = (sps * cth) * x + (sps * sth * sph + cps * cph) * y + (sps * sth * cph - cps * sph) * z
    d = (-sth) * x + (cth * sph) * y + (cth * cph) * z
    return n, e, d


def interp_angle(t_src, ang_src, t_dst):
    """Linear interpolation of an angle via unwrapping (no smoothing)."""
    return np.interp(t_dst, t_src, np.unwrap(ang_src))


def interp(t_src, v_src, t_dst):
    return np.interp(t_dst, t_src, v_src)


def bin_mean(t, v, t_centres, half=0.5):
    """Mean of samples within +-half s of each centre; NaN where empty."""
    t = np.asarray(t); v = np.asarray(v)
    out = np.full((len(t_centres), v.shape[1] if v.ndim > 1 else 1), np.nan)
    lo = np.searchsorted(t, np.asarray(t_centres) - half)
    hi = np.searchsorted(t, np.asarray(t_centres) + half)
    for i, (a, b) in enumerate(zip(lo, hi)):
        if b > a:
            out[i] = v[a:b].mean(axis=0)
    return out.squeeze()


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def dvl_valid(df: pd.DataFrame) -> pd.Series:
    return df["validity"] == 7


def hold_last_valid(vals: np.ndarray, valid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Replace invalid rows by the last valid row (what a DR filter effectively does within
    its DVL timeout). Returns (filled, was_filled). Leading invalid rows become NaN."""
    vals = np.array(vals, dtype=float)
    out = vals.copy()
    last = None
    filled = np.zeros(len(vals), bool)
    for i in range(len(vals)):
        if valid[i]:
            last = vals[i]
        elif last is not None:
            out[i] = last
            filled[i] = True
        else:
            out[i] = np.nan
    return out, filled


def dump_json(obj, path: Path):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    path.write_text(json.dumps(obj, indent=2, default=conv))


def legs_from_pcs(pcs: pd.DataFrame) -> pd.DataFrame:
    """Maneuver intervals from PlanControlState man_id transitions."""
    p = pcs.copy()
    p["man_id"] = p["man_id"].fillna("")
    ch = p[(p["man_id"] != p["man_id"].shift())].reset_index(drop=True)
    rows = []
    for i, r in ch.iterrows():
        t1 = ch.loc[i + 1, "timestamp"] if i + 1 < len(ch) else p["timestamp"].iloc[-1]
        if r["man_id"]:
            rows.append(dict(man_id=r["man_id"], man_type=int(r["man_type"]), t0=r["timestamp"], t1=t1))
    return pd.DataFrame(rows)


def utc_str(ts: float) -> str:
    return pd.to_datetime(ts, unit="s", utc=True).strftime("%H:%M:%S")
