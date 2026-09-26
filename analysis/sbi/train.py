"""
Train the amortized posterior q(theta | x) with BayesFlow (JAX backend).

    python train.py --train data/train.npz --val data/val.npz --epochs 40

Summary network: TimeSeriesTransformer (the window is an ordered sequence; the heading
programme carries the identifiability). Inference network: CouplingFlow.
Saves models/posterior.keras and models/stats.npz (standardisation), and the training loss.
"""
from __future__ import annotations

import argparse
import os
os.environ.setdefault("KERAS_BACKEND", "jax")

import numpy as np

from config import MODELS, PLOTS, THETA


def load(path, stats=None):
    d = np.load(path, allow_pickle=True)
    mean, std = (d["x_mean"], d["x_std"]) if stats is None else stats
    x = ((d["x"] - mean) / std).astype("float32")
    return {"theta": d["theta"].astype("float32"), "x": x}, (mean, std)


def build_workflow(summary_dim=32, checkpoint=None):
    import bayesflow as bf
    adapter = (bf.Adapter()
               .convert_dtype("float64", "float32")
               .rename("theta", "inference_variables")
               .rename("x", "summary_variables"))
    summary_net = bf.networks.TimeSeriesTransformer(summary_dim=summary_dim, time_axis=-2)
    inference_net = bf.networks.CouplingFlow()
    return bf.BasicWorkflow(adapter=adapter, inference_network=inference_net, summary_network=summary_net,
                            inference_variables=["theta"], summary_variables=["x"],
                            checkpoint_filepath=checkpoint, standardize="inference_variables")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/train.npz")
    ap.add_argument("--val", default="data/val.npz")
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--summary-dim", type=int, default=32)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    import keras
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

    train, stats = load(a.train)
    val, _ = load(a.val, stats)
    if a.smoke:
        train = {k: v[:512] for k, v in train.items()}; val = {k: v[:128] for k, v in val.items()}; a.epochs = 2
    print(f"train {train['x'].shape}, val {val['x'].shape}")
    wf = build_workflow(a.summary_dim, checkpoint=str(MODELS))
    hist = wf.fit_offline(data=train, epochs=a.epochs, batch_size=a.batch_size, validation_data=val)
    wf.approximator.save(MODELS / "posterior.keras")
    np.savez(MODELS / "stats.npz", x_mean=stats[0], x_std=stats[1])
    h = hist.history
    np.savez(MODELS / "history.npz", **{k: np.array(v) for k, v in h.items()})
    fig, ax = plt.subplots(figsize=(5, 3))
    for k in h:
        if "loss" in k:
            ax.plot(h[k], label=k)
    ax.set_xlabel("epoch"); ax.set_ylabel("loss"); ax.legend(); fig.tight_layout(); fig.savefig(PLOTS / "training_loss.png", dpi=200)
    # quick recovery on validation
    k = min(500, len(val["theta"]))
    post = wf.sample(num_samples=200, conditions={"x": val["x"][:k]})["theta"]
    print("recovery (corr of posterior mean with truth):")
    for i, n in enumerate(THETA):
        r = np.corrcoef(post[:, :, i].mean(1), val["theta"][:k, i])[0, 1]
        print(f"  {n:14s} r = {r:+.3f}")
    print("saved", MODELS / "posterior.keras")


if __name__ == "__main__":
    main()
