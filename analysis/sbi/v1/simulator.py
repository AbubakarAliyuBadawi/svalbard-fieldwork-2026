"""
Kinematic simulator for the dead-reckoning error parameters of a survey AUV.

theta = (delta [deg], scale, c_N, c_E, log10 sigma_v)

Given a heading programme psi_true[t] and a propeller-speed programme rpm[t] (both at 1 Hz,
replayed from the field logs or drawn synthetically), the true velocity through water is
u_true = k * rpm plus a small AR(1) sway; the over-ground velocity is
    v_og = R(psi_true) [u_true, v_true] + c.
Measurements:
    psi_meas   = psi_true - delta + noise
    water track (body) = [u_true, v_true] / scale + N(0, sigma_v^2)
    bottom track (body) = R(-psi_true) v_og + N(0, (BT_NOISE_FACTOR sigma_v)^2)
    GPS velocity (NED)  = v_og + N(0, GPS_VEL_NOISE^2)
Masks: DVL dropouts in bursts; bottom track and GPS present or absent for the whole window.
Absent channels are zero with mask 0, exactly as the real windows are built.
"""
from __future__ import annotations

import numpy as np

from config import (T, C, CHANNELS, PRIOR_LO, PRIOR_HI, RPM_K_RANGE, HEADING_NOISE_DEG,
                    GPS_VEL_NOISE, BT_NOISE_FACTOR, SWAY_SD, P_DROP_RANGE, P_BT_AVAILABLE,
                    P_GPS_AVAILABLE)

IDX = {c: i for i, c in enumerate(CHANNELS)}


def sample_prior(rng: np.random.Generator, n: int = 1) -> np.ndarray:
    return rng.uniform(PRIOR_LO, PRIOR_HI, size=(n, len(PRIOR_LO)))


def synthetic_programme(rng: np.random.Generator):
    """Piecewise-constant heading with turns at ~10 deg/s and a constant-ish rpm."""
    psi = np.zeros(T)
    h = rng.uniform(-np.pi, np.pi)
    t = 0
    while t < T:
        seg = int(rng.integers(20, 90))
        psi[t:t + seg] = h
        t += seg
        h_new = h + rng.uniform(-np.pi, np.pi) * (rng.random() < 0.8)
        # turn ramp
        n_turn = int(abs(h_new - h) / np.radians(10)) + 1
        ramp = np.linspace(h, h_new, n_turn)
        psi[t:t + n_turn] = ramp[:max(0, min(n_turn, T - t))]
        t += n_turn
        h = h_new
    rpm = np.full(T, rng.uniform(900, 1700)) + rng.normal(0, 15, T)
    return psi, rpm


def simulate(theta: np.ndarray, psi_true: np.ndarray, rpm: np.ndarray,
             rng: np.random.Generator, gps: bool | None = None, bt: bool | None = None) -> np.ndarray:
    delta = np.radians(theta[0]); s = theta[1]; c = theta[2:4]; sig = 10 ** theta[4]
    k = rng.uniform(*RPM_K_RANGE)
    u = k * rpm
    # AR(1) sway
    v = np.zeros(T); phi = 0.9
    e = rng.normal(0, SWAY_SD * np.sqrt(1 - phi**2), T)
    for t in range(1, T):
        v[t] = phi * v[t - 1] + e[t]
    cp, sp = np.cos(psi_true), np.sin(psi_true)
    vn = cp * u - sp * v + c[0]
    ve = sp * u + cp * v + c[1]
    psi_m = psi_true - delta + rng.normal(0, np.radians(HEADING_NOISE_DEG), T)
    x = np.zeros((T, C))
    x[:, IDX["cos_psi"]] = np.cos(psi_m); x[:, IDX["sin_psi"]] = np.sin(psi_m)
    # water track with dropouts
    p_drop = rng.uniform(*P_DROP_RANGE)
    m = np.ones(T)
    t = 0
    while t < T:
        if rng.random() < p_drop:
            L = int(rng.geometric(1 / 3.0)); m[t:t + L] = 0; t += L
        else:
            t += 1
    x[:, IDX["wt_u"]] = (u / s + rng.normal(0, sig, T)) * m
    x[:, IDX["wt_v"]] = (v / s + rng.normal(0, sig, T)) * m
    x[:, IDX["m_dvl"]] = m
    x[:, IDX["rpm_k"]] = rpm / 1000 + rng.normal(0, 0.005, T)
    if gps is None:
        gps = rng.random() < P_GPS_AVAILABLE
    if gps:
        x[:, IDX["gps_vn"]] = vn + rng.normal(0, GPS_VEL_NOISE, T)
        x[:, IDX["gps_ve"]] = ve + rng.normal(0, GPS_VEL_NOISE, T)
        x[:, IDX["m_gps"]] = 1
    if bt is None:
        bt = rng.random() < P_BT_AVAILABLE
    if bt:
        bu = cp * vn + sp * ve; bv = -sp * vn + cp * ve
        x[:, IDX["bt_u"]] = (bu + rng.normal(0, BT_NOISE_FACTOR * sig, T)) * m
        x[:, IDX["bt_v"]] = (bv + rng.normal(0, BT_NOISE_FACTOR * sig, T)) * m
        x[:, IDX["m_bt"]] = m
    return x


def dead_reckon(x: np.ndarray, theta: np.ndarray | None = None, source: str = "wt") -> np.ndarray:
    """Position (N, E) over the window from a real or simulated window, in metres.
    theta=None: nominal DR (sensed heading, water track as is). theta given: corrected DR
    v = s R(psi_meas + delta) v_wt + c. Dropped DVL samples hold the last valid value."""
    psi = np.arctan2(x[:, IDX["sin_psi"]], x[:, IDX["cos_psi"]])
    if source == "wt":
        u, v, m = x[:, IDX["wt_u"]], x[:, IDX["wt_v"]], x[:, IDX["m_dvl"]]
    else:
        u, v, m = x[:, IDX["bt_u"]], x[:, IDX["bt_v"]], x[:, IDX["m_bt"]]
    u = u.copy(); v = v.copy()
    last = (0.0, 0.0)
    for t in range(T):
        if m[t] > 0.5:
            last = (u[t], v[t])
        else:
            u[t], v[t] = last
    if theta is None:
        d, s, c = 0.0, 1.0, np.zeros(2)
    else:
        d, s, c = np.radians(theta[0]), theta[1], np.asarray(theta[2:4])
    ang = psi + d
    vn = s * (np.cos(ang) * u - np.sin(ang) * v) + c[0]
    ve = s * (np.sin(ang) * u + np.cos(ang) * v) + c[1]
    return np.column_stack([np.cumsum(vn), np.cumsum(ve)])
