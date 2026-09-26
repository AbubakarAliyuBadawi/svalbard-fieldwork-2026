#!/usr/bin/env bash
# Reproduce the full feasibility analysis from the raw logs. Run from anywhere.
set -e
cd "$(dirname "$0")"
python3 extract_logs.py        # decode LSF -> analysis/<log>/inventory.md + csv/
python3 analyze_star.py        # 4a, 4b, 4e, 4f + plots   -> analysis/101134_20260907_star/{results,plots}
python3 analyze_dives.py       # 4c + plots                -> analysis/{074948_08_09_sidescan,094605_0700926LongYoYo1}/{results,plots}
