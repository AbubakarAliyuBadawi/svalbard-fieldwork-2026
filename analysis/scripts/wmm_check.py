"""
Compare the constant offset that DUNE adds to the AHRS yaw (EstimatedState psi - EulerAngles psi)
with the World Magnetic Model declination at the position and date of each log.

Needs `pip install pygeomag` (open-source WMM implementation with the WMM2025 coefficients).
Writes analysis/wmm_check.md.
"""
import numpy as np
from common import ANALYSIS, load, wrap, interp_angle

try:
    from pygeomag import GeoMag
except ImportError:
    raise SystemExit("pip install pygeomag")

gm = GeoMag(coefficients_file="wmm/WMM_2025.COF")
rows = []
for log, label in [("101134_20260907_star", "Marie, star, 7 Sept"), ("094605_0700926LongYoYo1", "Thor, long yoyo, 7 Sept"), ("074948_08_09_sidescan", "Marie, sidescan, 8 Sept")]:
    es = load(log, "EstimatedState"); eu = load(log, "EulerAngles")
    off = np.degrees(wrap(es.psi.values - interp_angle(eu.timestamp.values, eu.psi.values, es.timestamp.values)))
    lat, lon = np.degrees(es.lat.iloc[0]), np.degrees(es.lon.iloc[0])
    t = 2026 + (np.datetime64(int(es.timestamp.iloc[0]), "s") - np.datetime64("2026-01-01T00:00:00")).astype(float) / (365.25 * 86400)
    wmm = gm.calculate(glat=lat, glon=lon, alt=0, time=t).d
    rows.append((label, lat, lon, t, np.median(off), wmm))
md = ["# DUNE heading offset vs WMM2025 declination\n", "| log | lat [deg] | lon [deg] | decimal year | offset added by DUNE [deg] | WMM2025 declination [deg] | difference |", "|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r[0]} | {r[1]:.3f} | {r[2]:.3f} | {r[3]:.3f} | {r[4]:.2f} | {r[5]:.2f} | {r[4]-r[5]:+.2f} |")
(ANALYSIS / "wmm_check.md").write_text("\n".join(md)); print("\n".join(md))
