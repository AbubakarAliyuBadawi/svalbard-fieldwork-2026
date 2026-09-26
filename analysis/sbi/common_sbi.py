"""Shared helpers for the post-training scripts (validate, propagate, detect)."""
from __future__ import annotations

import os
os.environ.setdefault("KERAS_BACKEND", "jax")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import MODELS, DATA, THETA

COL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
GREY = "#8a8985"
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.color": "#e6e5e1", "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False, "savefig.dpi": 300})
LABELS = [r"$\delta$ [deg]", r"$s$", r"$c_N$ [m/s]", r"$c_E$ [m/s]", r"$\log_{10}\sigma_v$"]


def load_model():
    import bayesflow as bf  # noqa: F401  (registers the classes)
    import keras
    appr = keras.saving.load_model(MODELS / "posterior.keras")
    st = np.load(MODELS / "stats.npz")
    return appr, (st["x_mean"], st["x_std"])


def standardize(x, stats):
    return ((x - stats[0]) / stats[1]).astype("float32")


def posterior(appr, stats, x, n=500, batch_size=64, seed=0):
    """x: (N, T, C) raw windows -> samples (N, n, 5); fixed seed so that every reported number is reproducible"""
    out = appr.sample(num_samples=n, conditions={"x": standardize(x, stats)}, batch_size=batch_size, seed=seed)
    return np.asarray(out["theta"])


def summaries(appr, stats, x, batch_size=256):
    hs = []
    for i in range(0, len(x), batch_size):
        hs.append(np.asarray(appr.summarize({"x": standardize(x[i:i + batch_size], stats)})))
    return np.concatenate(hs)


def load_windows():
    d = np.load(DATA / "windows.npz")
    sets = {}
    for k in ["star", "star_raw", "sidescan_dive", "thor_surface", "thor_dive"]:
        sets[k] = dict(x=d[f"x_{k}"], t0=d[f"t0_{k}"], ref=d[f"ref_{k}"])
    return sets


def interval(samples, lo=5, hi=95):
    return np.percentile(samples, lo, axis=-2), np.percentile(samples, hi, axis=-2)
