#!/usr/bin/env bash
# Full amortized-inference pipeline. Run from anywhere; needs the venv (see README.md).
set -e
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
$PY make_windows.py                                              # real windows + heading programmes
$PY generate_data.py --n 40000 --out data/train.npz --seed 1     # simulation budget
$PY generate_data.py --n 4000  --out data/val.npz   --seed 2
$PY train.py --train data/train.npz --val data/val.npz --epochs 40 --batch-size 128
$PY validate.py                                                  # SBC, recovery, star windows, drift
$PY propagate.py                                                 # uncertainty envelope along the sidescan dive
$PY propagate_thor.py                                            # Thor's two dives
$PY detect.py                                                    # misspecification check
$PY heading_bias_check.py                                        # per-window heading bias vs posterior (post hoc)
