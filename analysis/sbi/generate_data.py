"""
Pre-generate the simulation budget for training and validation.

    python generate_data.py --n 40000 --out data/train.npz --seed 1
    python generate_data.py --n 4000  --out data/val.npz   --seed 2

Half of the heading/rpm programmes are replayed 120 s cuts of the field logs (data/programmes.npz,
built by make_windows.py), half are synthetic piecewise-constant headings. The standardisation
statistics of the training set are stored inside train.npz and reused everywhere else.
"""
from __future__ import annotations

import argparse
import numpy as np

from config import DATA, T, THETA, CHANNELS
from simulator import sample_prior, simulate, synthetic_programme


def load_programmes():
    d = np.load(DATA / "programmes.npz")
    return [d[k] for k in d.files]


def draw_programme(rng, progs):
    if rng.random() < 0.5 or not progs:
        return synthetic_programme(rng)
    p = progs[rng.integers(len(progs))]
    s = rng.integers(0, len(p) - T + 1)
    seg = p[s:s + T]
    psi = seg[:, 0] + rng.uniform(-np.pi, np.pi)     # random rotation of the replayed pattern
    rpm = seg[:, 1] * rng.uniform(0.85, 1.15)
    return psi, rpm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40000)
    ap.add_argument("--out", default=str(DATA / "train.npz"))
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    progs = load_programmes()
    theta = sample_prior(rng, a.n)
    x = np.empty((a.n, T, len(CHANNELS)), dtype="float32")
    for i in range(a.n):
        psi, rpm = draw_programme(rng, progs)
        x[i] = simulate(theta[i], psi, rpm, rng)
        if (i + 1) % 10000 == 0:
            print(f"  {i+1}/{a.n}")
    mean = x.mean(axis=(0, 1)); std = x.std(axis=(0, 1)) + 1e-6
    np.savez(a.out, x=x, theta=theta.astype("float32"), x_mean=mean, x_std=std,
             theta_names=np.array(THETA), channels=np.array(CHANNELS))
    print(f"wrote {a.out}: x {x.shape}, theta {theta.shape}")


if __name__ == "__main__":
    main()
