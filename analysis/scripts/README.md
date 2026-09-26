# Feasibility analysis scripts

Self-contained Python (numpy, pandas, matplotlib only) to decode the LSTS/DUNE `.lsf` logs of the
Svalbard field campaign and answer the questions in the feasibility check. Original log folders are
never written to; everything goes to `analysis/<log_name>/`.

```
scripts/
  lsf_reader.py      generic LSF/IMC decoder driven by the IMC.xml.gz shipped with each log
  extract_logs.py    inventory.md + one CSV per message type, native rate, for the three logs
  common.py          shared helpers: geodesy, body->NED rotation, GPS acceptance rule, plotting style
  analyze_star.py    star mission: surface/GPS/DVL checks, per-leg current, joint (c, delta, s) fits,
                     synthetic GPS outages, plots
  analyze_dives.py   sidescan + long-yoyo missions: dive/resurface events, DUNE correction jumps,
                     own dead-reckoning closures, plots
  run_all.sh         runs the three steps in order (~2 min total)
  requirements.txt
```

## Run

```bash
cd field_work_data/analysis/scripts
python3 -m pip install -r requirements.txt
./run_all.sh
```

Outputs per log: `inventory.md`, `csv/*.csv` (timestamp = vehicle clock, `utc` column added;
nested IMC messages stored as JSON strings), `results/*.md|json`, `plots/*.png` (300 dpi).
The feasibility report is `analysis/feasibility_report.md`.

## LSF format handled by `lsf_reader.py`

Header `sync(u16) mgid(u16) size(u16) timestamp(f64) src(u16) src_ent(u8) dst(u16) dst_ent(u8)`,
then `size` payload bytes, then CRC-16-IBM. The sync value (0xFE54 for IMC 5.4, 0xFE55 for
IMC 5.5) is read from `<header>` in IMC.xml; a byte-swapped sync means big-endian. Variable fields:
`plaintext`/`rawdata` = u16 length + bytes; `message` = u16 id (0xFFFF = null) + inline payload;
`message-list` = u16 count + inline messages. Messages not in the wanted set are skipped by
seeking, so sonar payloads cost nothing. CRC is verified on a sample (the first 5000 messages plus
0.2 % of the rest); a full pure-Python CRC pass would take minutes on the 133 MB log.

## Processing choices (also stated in each results file)

* Nothing is smoothed. Time alignment is by linear interpolation of angles (unwrapped) to DVL
  sample times and by +-0.5 s bin means at GPS epochs.
* GPS epoch = UTC time of fix from the message itself. The vehicle-clock header timestamp lags it
  by 0.32 s (Marie, GPS over TCP) / -0.02 s (Thor); the vehicle clocks are GPS-synced.
* "accepted" GPS fix = receiver VALID_POS and hacc < 15 m and hdop < 4 (the DUNE thresholds).
  `analyze_dives.py` additionally uses the fixes DUNE actually accepted (not in GpsFixRejection).
* DVL velocities are body-frame; verified against GPS (RMS 0.17 m/s with rotation vs 2.1 m/s without).
* Heading for dead reckoning = EstimatedState psi (DUNE heading). EulerAngles psi is the magnetic
  AHRS heading (psi == psi_magnetic); DUNE adds a constant declination (12.72-12.74 deg on Marie,
  14.03 deg on Thor).
* Dead reckoning: forward Euler at 5 Hz DVL times; invalid DVL samples hold the last valid value.

## Paper draft

`analysis/paper/` holds the IEEE-format draft (`main.tex`, `refs.bib`, `figures/`, `Makefile`).
`make` builds with a local TeX Live (needs IEEEtran, siunitx, booktabs, cite, hyperref);
`make docker` builds in a container. Red `\todo{}` marks are results that do not exist yet.

`wmm_check.py` compares the heading offset DUNE adds with the WMM2025 declination at each log's position and date (needs `pygeomag`); output `analysis/wmm_check.md`. The amortized-inference pipeline is in `analysis/sbi/`.
