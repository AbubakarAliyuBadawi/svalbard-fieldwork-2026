#!/usr/bin/env python3
"""Process paired DT4/RTPX files and create WGS84 recorded GPS track figures."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.ticker import ScalarFormatter, MaxNLocator
import numpy as np
import pandas as pd
from pyproj import Geod


def track(folder):
    df = pd.read_csv(folder / 'gps_fixes.csv').sort_values('recorder_seconds').drop_duplicates('recorder_seconds')
    good = df.gps_valid.to_numpy(dtype=bool)
    xy = df[['longitude', 'latitude']].to_numpy()
    elapsed = (df.recorder_seconds.to_numpy() - df.recorder_seconds.iloc[0]) / 60
    dt = np.diff(df.recorder_seconds.to_numpy())
    joined = good[:-1] & good[1:] & (dt > 0) & (dt <= 1.)
    segments = np.stack([xy[:-1], xy[1:]], axis=1)[joined]
    if not len(segments):
        raise ValueError(f'No connected GPS fixes: {folder}')
    # A segment ID preserves breaks in CSV and GeoJSON; no lines between files.
    ids = np.cumsum(np.r_[True, ~joined])
    df['segment_id'] = ids
    df['gps_utc'] = pd.to_datetime(df.gps_utc_seconds, unit='s', utc=True)
    df['elapsed_recorder_min'] = elapsed
    df.to_csv(folder / 'gps_track.csv', index=False)
    lines = [xy[(ids == s) & good].tolist() for s in np.unique(ids)]
    lines = [line for line in lines if len(line) >= 2]
    feature = dict(type='Feature', properties=dict(recording=folder.name, kind='recorded GPS track'),
                   geometry=dict(type='MultiLineString', coordinates=lines))
    (folder / 'gps_track.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=[feature])))
    return dict(name=folder.name, xy=xy, good=good, segments=segments,
                times=elapsed[:-1][joined], feature=feature, df=df)


def axes_style(ax, latitude):
    # Geographic axes with local distance proportions at this Arctic latitude.
    ax.set_aspect(1 / np.cos(np.deg2rad(latitude)))
    ax.set_xlabel('Longitude (° E)')
    ax.set_ylabel('Latitude (° N)')
    for axis in (ax.xaxis, ax.yaxis):
        formatter = ScalarFormatter(useOffset=False)
        formatter.set_scientific(False)
        axis.set_major_formatter(formatter)
        axis.set_major_locator(MaxNLocator(5))
    ax.tick_params(axis='x', labelrotation=25)
    ax.grid(alpha=.2)
    ax.margins(.12)


def draw_track(ax, tr, color=None, endpoints=True):
    lc = LineCollection(tr['segments'], cmap='viridis', linewidths=1.3,
                        rasterized=True, colors=color)
    if color is None:
        lc.set_array(tr['times'])
    ax.add_collection(lc)
    valid_xy = tr['xy'][tr['good']]
    ax.update_datalim(valid_xy)
    ax.autoscale_view()
    # Direction arrows follow individual valid segments, without bridging gaps.
    lengths = Geod(ellps='WGS84').inv(tr['segments'][:, 0, 0], tr['segments'][:, 0, 1],
                                     tr['segments'][:, 1, 0], tr['segments'][:, 1, 1])[2]
    cumulative = np.cumsum(lengths)
    for target in np.linspace(0, cumulative[-1], 10)[1:-1]:
        k = min(np.searchsorted(cumulative, target), len(lengths) - 1)
        a, b = tr['segments'][k]
        if lengths[k] > .02:
            ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='->', color=color or '#333333', lw=1, mutation_scale=11))
    if endpoints:
        for point, marker, label, offset in [(valid_xy[0], 'o', 'Start', (7, 9)),
                                               (valid_xy[-1], 's', 'End', (7, -17))]:
            ax.scatter(*point, marker=marker, s=42, facecolor='white', edgecolor=color or 'black', zorder=4)
            ax.annotate(label, point, xytext=offset, textcoords='offset points', fontsize=8)
    axes_style(ax, float(np.median(valid_xy[:, 1])))
    return lc


def save(fig, folder, name, note='Recorded GPS tracks • arrows show travel direction • planned routes not supplied'):
    fig.text(.5, .008, note, ha='center', fontsize=8, color='.4')
    fig.tight_layout(rect=(0, .055, 1, .96))
    for suffix in ('png', 'pdf'):
        fig.savefig(folder / f'{name}.{suffix}', dpi=300, bbox_inches='tight')
    plt.close(fig)


def gps_figures(folders, out):
    plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42})
    tracks = [track(folder) for folder in folders]
    for folder, tr in zip(folders, tracks):
        fig, ax = plt.subplots(figsize=(8, 7))
        lc = draw_track(ax, tr)
        ax.set_title(f"Otter recorded GPS route — {tr['name']}", pad=18)
        fig.colorbar(lc, ax=ax, label='Elapsed recorder time (min)', shrink=.7)
        save(fig, folder / 'figures', '05_gps_longitude_latitude')
    fig, axes = plt.subplots(int(np.ceil(len(tracks) / 2)), 2, figsize=(12, 4.8 * np.ceil(len(tracks) / 2)), squeeze=False)
    for ax, tr in zip(axes.flat, tracks):
        lc = draw_track(ax, tr)
        ax.set_title(tr['name'], pad=14)
        fig.colorbar(lc, ax=ax, label='Elapsed min', shrink=.65)
    for ax in list(axes.flat)[len(tracks):]:
        ax.axis('off')
    fig.suptitle('Otter recorded routes — individual views (different map extents)')
    save(fig, out, 'all_gps_tracks_panels')
    fig, ax = plt.subplots(figsize=(10, 7))
    for k, tr in enumerate(tracks):
        color = f'C{k}'
        draw_track(ax, tr, color=color, endpoints=False)
        ax.plot([], [], color=color, label=tr['name'])
    latitude = np.median(np.concatenate([tr['xy'][tr['good'], 1] for tr in tracks]))
    axes_style(ax, latitude)
    ax.set_title('Otter recordings — geographic overview', pad=18)
    ax.legend(loc='upper left', fontsize=8)
    save(fig, out, 'all_gps_tracks_overview', 'Recorded GPS tracks • separate recordings are not joined • no planned routes supplied')
    (out / 'all_gps_tracks.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=[t['feature'] for t in tracks])))
    summaries = []
    for folder in folders:
        table = pd.read_csv(folder / 'figures' / 'survey_summary.csv')
        summaries.append(dict(recording=folder.name, **dict(zip(table.Metric, table.Value))))
    pd.DataFrame(summaries).to_csv(out / 'all_recordings_summary.csv', index=False)
    print(pd.DataFrame(summaries).to_string(index=False))


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, default=root / 'results')
    parser.add_argument('--gps-only', action='store_true', help='Use existing processed data; regenerate GPS figures only')
    args = parser.parse_args()
    files = sorted(args.source.glob('*.dt4'))
    if not files:
        parser.error('No DT4 files found')
    folders = []
    for file in files:
        pair = file.with_suffix('.rtpx')
        if not pair.exists():
            raise FileNotFoundError(pair)
        folder = args.out / file.stem
        if not args.gps_only:
            for script, options in [('extract_otter.py', ['--dt4', str(file), '--rtpx', str(pair), '--out', str(folder)]),
                                    ('plot_otter.py', ['--data', str(folder), '--out', str(folder / 'figures')])]:
                print(f'{file.stem}: {script}', flush=True)
                subprocess.run([sys.executable, str(Path(__file__).with_name(script)), *options], check=True,
                               stdout=subprocess.DEVNULL)
        folders.append(folder)
    gps_figures(folders, args.out)


if __name__ == '__main__':
    main()
