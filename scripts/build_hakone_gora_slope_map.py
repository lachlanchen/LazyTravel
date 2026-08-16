#!/usr/bin/env python3
"""Build Hakone Chapter 3's railway elevation and switchback diagram."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-gora-slope.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-gora-slope"
FIXED_TIME = datetime(2026, 8, 16, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def render(config: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-hakone-gora-slope-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.patheffects as path_effects
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Polygon

    colors = {
        "ink": "#142330",
        "muted": "#586775",
        "paper": "#F9FCFF",
        "grid": "#CBD9E4",
        "rail": "#F05D36",
        "switch": "#E53D63",
        "museum": "#008E87",
        "cable": "#1769E0",
        "mountain": "#DFF2E8",
    }
    stations = config["stations"]
    x_values = [0.07, 0.20, 0.35, 0.50, 0.65, 0.79, 0.92]
    x_by_id = {station["id"]: x_values[index] for index, station in enumerate(stations)}
    elevation_by_id = {station["id"]: station["elevation_m"] for station in stations}

    def profile_y(elevation: float) -> float:
        return 0.16 + ((elevation - 90) / (550 - 90)) * 0.57

    y_values = [profile_y(station["elevation_m"]) for station in stations]

    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.055, right=0.975, top=0.78, bottom=0.17)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(
        FancyBboxPatch(
            (0.015, 0.075),
            0.97,
            0.79,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#F2F8FB",
            edgecolor="#D5E3EB",
            linewidth=0.9,
            zorder=0,
        )
    )

    for elevation in (100, 300, 500):
        y_value = profile_y(elevation)
        ax.plot([0.045, 0.955], [y_value, y_value], color=colors["grid"], lw=0.7, zorder=0)
        ax.text(
            0.042,
            y_value,
            f"{elevation} m",
            fontsize=5.4,
            color=colors["muted"],
            ha="right",
            va="center",
        )

    mountain_points = [(0.045, 0.11)]
    mountain_points.extend(zip(x_values, y_values, strict=True))
    mountain_points.extend([(0.955, y_values[-1] - 0.02), (0.955, 0.11)])
    ax.add_patch(
        Polygon(
            mountain_points,
            closed=True,
            facecolor=colors["mountain"],
            edgecolor="none",
            zorder=1,
        )
    )

    ax.plot(x_values, y_values, color="#FFFFFF", lw=8.0, solid_capstyle="round", zorder=2)
    ax.plot(
        x_values,
        y_values,
        color=colors["rail"],
        lw=4.2,
        solid_capstyle="round",
        zorder=3,
    )

    label_offsets = {
        "yumoto": (0.0, -0.105),
        "tonosawa": (0.0, 0.095),
        "ohiradai": (0.025, -0.16),
        "miyanoshita": (0.035, 0.125),
        "kowakidani": (-0.005, -0.12),
        "chokoku": (-0.035, -0.15),
        "gora": (0.015, -0.14),
    }
    for index, station in enumerate(stations):
        x_value = x_values[index]
        y_value = y_values[index]
        decision = station.get("decision")
        node_color = colors["paper"]
        edge_color = colors["ink"]
        radius = 0.014
        if decision == "museum":
            node_color = "#BDEFE5"
            edge_color = colors["museum"]
            radius = 0.019
        elif decision == "cable-car":
            node_color = "#CFE0FF"
            edge_color = colors["cable"]
            radius = 0.019
        ax.add_patch(
            Circle(
                (x_value, y_value),
                radius,
                facecolor=node_color,
                edgecolor=edge_color,
                linewidth=1.5,
                zorder=5,
            )
        )
        dx, dy = label_offsets[station["id"]]
        label = (
            f"{station['zh']}・{station['ja']}\n"
            f"{station['en']}\n"
            f"{station['elevation_m']} m"
        )
        text = ax.text(
            x_value + dx,
            y_value + dy,
            label,
            fontsize=5.75,
            fontweight="bold",
            color=colors["ink"],
            ha="center",
            va="center",
            linespacing=1.12,
            zorder=7,
        )
        text.set_path_effects(
            [path_effects.withStroke(linewidth=2.2, foreground=colors["paper"])]
        )

    def interpolated_position(switchback: dict[str, Any]) -> tuple[float, float]:
        if switchback.get("at_station"):
            station_id = switchback["at_station"]
            return x_by_id[station_id], profile_y(elevation_by_id[station_id])
        start_id, end_id = switchback["position_between"]
        fraction = switchback["fraction"]
        start_x = x_by_id[start_id]
        end_x = x_by_id[end_id]
        start_y = profile_y(elevation_by_id[start_id])
        end_y = profile_y(elevation_by_id[end_id])
        return (
            start_x + (end_x - start_x) * fraction,
            start_y + (end_y - start_y) * fraction,
        )

    switch_offsets = {1: (-0.01, 0.095), 2: (0.0, 0.105), 3: (-0.015, 0.09)}
    for switchback in config["switchbacks"]:
        x_value, y_value = interpolated_position(switchback)
        number = switchback["number"]
        ax.add_patch(
            Circle(
                (x_value, y_value),
                0.024,
                facecolor=colors["switch"],
                edgecolor="#FFFFFF",
                linewidth=1.4,
                zorder=6,
            )
        )
        ax.text(
            x_value,
            y_value,
            str(number),
            fontsize=6.1,
            color="#FFFFFF",
            fontweight="bold",
            ha="center",
            va="center",
            zorder=7,
        )
        if number == 2:
            continue
        dx, dy = switch_offsets[number]
        compact_name = "出山" if number == 1 else "上大平台"
        label = f"{compact_name} / {switchback['en']}"
        text = ax.text(
            x_value + dx,
            y_value + dy,
            label,
            fontsize=5.15,
            color=colors["switch"],
            fontweight="bold",
            ha="center",
            va="bottom",
            linespacing=1.08,
            zorder=7,
        )
        text.set_path_effects(
            [path_effects.withStroke(linewidth=2.2, foreground=colors["paper"])]
        )

    ax.text(
        0.745,
        0.84,
        "主停留 90-120分\n主な立ち寄り 90-120分\nMAIN STOP 90-120 MIN",
        fontsize=5.55,
        color=colors["museum"],
        fontweight="bold",
        ha="center",
        va="center",
        linespacing=1.13,
        bbox={
            "boxstyle": "round,pad=0.38,rounding_size=0.9",
            "facecolor": "#E8FAF5",
            "edgecolor": colors["museum"],
            "linewidth": 0.9,
        },
        zorder=8,
    )
    ax.text(
        0.905,
        0.84,
        "换乘缆车\nケーブルカーへ\nCHANGE MODE",
        fontsize=5.55,
        color=colors["cable"],
        fontweight="bold",
        ha="center",
        va="center",
        linespacing=1.13,
        bbox={
            "boxstyle": "round,pad=0.38,rounding_size=0.9",
            "facecolor": "#EDF3FF",
            "edgecolor": colors["cable"],
            "linewidth": 0.9,
        },
        zorder=8,
    )

    fig.text(
        0.04,
        0.953,
        config["title"]["zh"],
        fontsize=13.2,
        fontweight="bold",
        color=colors["ink"],
    )
    fig.text(
        0.04,
        0.91,
        config["title"]["ja"],
        fontsize=9.3,
        fontweight="bold",
        color=colors["ink"],
    )
    fig.text(
        0.04,
        0.872,
        config["title"]["en"],
        fontsize=8.15,
        fontweight="bold",
        color=colors["cable"],
    )
    fig.text(
        0.96,
        0.952,
        "看上升，不按距离\n高低差を読み、距離図にしない\nREAD ELEVATION, NOT DISTANCE",
        fontsize=5.7,
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.18,
    )

    metrics = config["metrics"]
    fig.text(
        0.04,
        0.817,
        f"{metrics['route_km']} km  ·  约{metrics['journey_minutes_approx']}分 / "
        f"約{metrics['journey_minutes_approx']}分 / ABOUT "
        f"{metrics['journey_minutes_approx']} MIN",
        fontsize=6.2,
        color=colors["rail"],
        fontweight="bold",
    )
    fig.text(
        0.46,
        0.817,
        f"最大坡度・最急勾配 / MAX {metrics['maximum_grade_permille']}‰",
        fontsize=6.2,
        color=colors["switch"],
        fontweight="bold",
    )
    fig.text(
        0.755,
        0.817,
        f"折返{metrics['switchback_count']}处 / {metrics['switchback_count']}か所\n"
        f"{metrics['switchback_count']} SWITCHBACKS",
        fontsize=5.9,
        color=colors["museum"],
        fontweight="bold",
        linespacing=1.05,
    )

    fig.text(
        0.04,
        0.104,
        "示意：横向只表车站顺序；纵向采用公开海拔。信号场位置与站间坡线不按比例。",
        fontsize=5.35,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.068,
        "模式図：横軸は駅順のみ。縦軸は公表標高。信号場位置と駅間勾配は縮尺外。",
        fontsize=5.35,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.032,
        "Schematic: station order is not distance; vertical values use published elevations. "
        "Signal positions and slopes are not to scale.",
        fontsize=5.35,
        color=colors["muted"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(svg_path, format="svg", metadata={"Date": None})
    normalize_svg(svg_path)
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), format="pdf", metadata=metadata)
    fig.savefig(OUTPUT_STEM.with_suffix(".png"), format="png", dpi=480, metadata={"Date": None})
    plt.close(fig)


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    render(config)
    files = {}
    for suffix in ("svg", "pdf", "png"):
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    png_dimensions = list(Image.open(OUTPUT_STEM.with_suffix(".png")).size)
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "schematic-elevation-render",
        "command": "python3 scripts/build_hakone_gora_slope_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": (
            "Map design © LazyTravel; station order, elevations, and railway facts are "
            "derived from the listed official sources."
        ),
        "files": files,
        "technical_qa": {
            "minimum_png_width": 2400,
            "pdf_vector_output": True,
            "png_dimensions": png_dimensions,
            "svg_selectable_text": True,
        },
        "visual_qa": config["visual_qa"],
    }
    if png_dimensions[0] < provenance["technical_qa"]["minimum_png_width"]:
        raise RuntimeError(f"map PNG is too narrow: {png_dimensions}")
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print("map: assets/maps/hakone/hakone-gora-slope.[svg|pdf|png]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
