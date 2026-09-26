"""
Decode the three DUNE/LSF logs, write an inventory and per-message CSV tables.

Usage:
    python3 extract_logs.py                 # all three logs
    python3 extract_logs.py 101134_20260907_star

Outputs go to  <field_work_data>/analysis/<log_name>/
    inventory.md              vehicle, time span, message counts/rates, entities, sources, clock check
    csv/<Message>.csv         one CSV per decoded message type, native rate, nothing filtered
Original log folders are only read.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from lsf_reader import IMCDefs, read_lsf

ROOT = Path(__file__).resolve().parents[2]          # field_work_data
OUT = ROOT / "analysis"
LOGS = ["101134_20260907_star", "094605_0700926LongYoYo1", "074948_08_09_sidescan"]

WANTED = {
    # navigation / positioning
    "GpsFix", "GpsFixRejection", "EstimatedState", "NavigationUncertainty", "NavigationData",
    "EstimatedStreamVelocity", "AlignmentState", "SimulatedState",
    # DVL
    "GroundVelocity", "WaterVelocity", "DvlRejection", "Distance", "VelocityDelta",
    # propulsion / attitude / pressure
    "Rpm", "SetThrusterActuation", "EulerAngles", "AngularVelocity", "Acceleration", "MagneticField",
    "Depth", "Pressure",
    # acoustics / USBL
    "UsblFixExtended", "UsblPositionExtended", "UsblAnglesExtended", "UsblFix", "UsblPosition",
    "UsblAngles", "UsblModem", "UsblConfig", "AcousticOperation", "UamRxFrame", "UamTxFrame",
    "UamRxRange", "UamTxRange", "UamTxStatus", "LblEstimate", "LblRangeAcceptance",
    # supervision
    "PlanControlState", "PlanControl", "ManeuverControlState", "PathControlState", "VehicleMedium",
    "VehicleState", "DesiredSpeed", "DesiredHeading", "DesiredPath", "DesiredZ",
    # CTD / environment
    "Temperature", "Salinity", "Conductivity", "SoundSpeed", "WaterDensity", "Chlorophyll", "Turbidity",
    # bookkeeping
    "EntityInfo", "EntityList", "LoggingControl", "Announce", "EntityActivationState", "LogBookEntry",
    "SatellitesInView", "GnssHwMon", "TextMessage",
}


def utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"


def flatten(df: pd.DataFrame) -> pd.DataFrame:
    """Nested inline messages / lists are stored as JSON strings so the CSV stays flat."""
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object and df[c].map(lambda v: isinstance(v, (dict, list))).any():
            df[c] = df[c].map(lambda v: json.dumps(v) if isinstance(v, (dict, list)) else v)
    return df


def config_vehicle(cfg: Path) -> str:
    for line in cfg.read_text(errors="replace").splitlines():
        if line.strip().startswith("Vehicle ="):
            return line.split("=", 1)[1].strip()
    return "?"


def process(log_name: str) -> None:
    src = ROOT / log_name
    out = OUT / log_name
    (out / "csv").mkdir(parents=True, exist_ok=True)
    print(f"=== {log_name}")
    defs = IMCDefs(src / "IMC.xml.gz")
    lsf = src / "Data.lsf.gz"
    r = read_lsf(lsf, defs, wanted=WANTED)
    dur = r.t_end - r.t_start

    # ---- vehicle identity (three independent sources)
    ann = r.tables.get("Announce")
    own = ann[(ann["src"] == 8259) | (ann["sys_type"] == 2)] if ann is not None else None
    ann_names = sorted(set(own["sys_name"])) if own is not None and len(own) else []
    logctl = r.tables.get("LoggingControl")
    log_label = logctl["name"].iloc[0] if logctl is not None and len(logctl) else "?"
    cfg_vehicle = config_vehicle(src / "Config.ini")

    # ---- clock check: GpsFix header timestamp vs GPS UTC-of-fix
    clock_lines = []
    g = r.tables.get("GpsFix")
    if g is not None and len(g):
        gg = g[(g["validity"] & 0x3) == 0x3].copy()   # valid date and time
        if len(gg):
            day0 = pd.to_datetime(dict(year=gg.utc_year, month=gg.utc_month, day=gg.utc_day), utc=True)
            gps_t = (day0 - pd.Timestamp(0, tz="UTC")).dt.total_seconds() + gg.utc_time
            d = gg["timestamp"].values - gps_t.values
            for ent, sub in gg.assign(dt=d).groupby("src_ent_label"):
                clock_lines.append(
                    f"| {ent} | {len(sub)} | {sub.dt.median():+.3f} | {sub.dt.mean():+.3f} | "
                    f"{sub.dt.std():.3f} | {sub.dt.min():+.3f} | {sub.dt.max():+.3f} |")

    # ---- inventory.md
    L = []
    L.append(f"# Inventory: {log_name}\n")
    L.append(f"Source: `{lsf.relative_to(ROOT)}` ({lsf.stat().st_size/1e6:.1f} MB gz), IMC {defs.version}, "
             f"sync 0x{defs.sync:04X}, byte order {'little' if r.endian == '<' else 'big'}-endian.\n")
    L.append(f"Messages: {r.n_messages}. CRC-16 checked on {r.crc_checked} sampled messages, "
             f"{r.crc_failed} failures.\n")
    L.append("## Vehicle identity\n")
    L.append(f"- Config.ini `Vehicle =` : **{cfg_vehicle}**")
    L.append(f"- Announce sys_name (own system, src 8259): **{ann_names}**")
    L.append(f"- LoggingControl label: `{log_label}`")
    L.append(f"- IMC source addresses seen: {dict(r.sources.most_common(8))} (8259 = the vehicle itself)\n")
    L.append("## Time span (header timestamps, vehicle clock)\n")
    L.append(f"- start: {r.t_start:.3f} = {utc(r.t_start)}")
    L.append(f"- end:   {r.t_end:.3f} = {utc(r.t_end)}")
    L.append(f"- duration: {dur:.1f} s = {dur/60:.2f} min\n")
    L.append("## Clock check: header timestamp minus GPS UTC time of fix (s)\n")
    if clock_lines:
        L.append("| entity | n | median | mean | std | min | max |")
        L.append("|---|---|---|---|---|---|---|")
        L += clock_lines
    else:
        L.append("no GpsFix with valid date+time")
    L.append("")
    L.append("## Message types (count, mean rate over the log, first/last time)\n")
    L.append("| message | count | rate [Hz] | first | last | decoded |")
    L.append("|---|---|---|---|---|---|")
    for ab, c in sorted(r.counts.items(), key=lambda kv: -kv[1]):
        L.append(f"| {ab} | {c} | {c/dur:.3f} | {utc(r.first_ts[ab])[11:23]} | {utc(r.last_ts[ab])[11:23]} | "
                 f"{'yes' if ab in r.tables else ''} |")
    L.append("")
    L.append("## Source entities per decoded message type\n")
    L.append("| message | entity id | label | count |")
    L.append("|---|---|---|---|")
    for (ab, ent), c in sorted(r.counts_by_entity.items(), key=lambda kv: (kv[0][0], -kv[1])):
        if ab in r.tables:
            L.append(f"| {ab} | {ent} | {r.entities.get(ent, '?')} | {c} |")
    L.append("")
    L.append("## Entity table (EntityInfo)\n")
    L.append(", ".join(f"{k}={v}" for k, v in sorted(r.entities.items())))
    L.append("")
    L.append("## Requested messages NOT present in this log\n")
    absent = sorted(a for a in WANTED if a not in r.counts)
    L.append(", ".join(absent) if absent else "none")
    L.append("")
    (out / "inventory.md").write_text("\n".join(L))

    # ---- CSVs
    for ab, df in r.tables.items():
        df = flatten(df)
        df.insert(1, "utc", pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        df.to_csv(out / "csv" / f"{ab}.csv", index=False)
    print(f"  {r.n_messages} messages, {dur/60:.1f} min, vehicle {cfg_vehicle} / {ann_names}, "
          f"{len(r.tables)} tables written to {out}")


if __name__ == "__main__":
    names = sys.argv[1:] or LOGS
    for n in names:
        process(n)
