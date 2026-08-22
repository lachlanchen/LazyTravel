#!/usr/bin/env python3
"""Build Lanzhou Chapter 5's Gansu museum-object findspot map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-museum-findspots.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-museum-findspots"
FIXED_TIME = datetime(2026, 8, 22, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#24313A",
    "muted": "#63717B",
    "line": "#B6C2CB",
    "land": "#EEF3F7",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F1FC",
    "vermilion": "#E44736",
    "vermilion_light": "#FCEAE7",
    "jade": "#23836B",
    "jade_light": "#E5F3EE",
    "coral": "#F06E65",
    "coral_light": "#FDECEA",
}

GROUP_COLORS = {
    "museum": "cobalt",
    "pottery": "vermilion",
    "buddhist": "coral",
    "movement": "jade",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def polygon_rings(geojson: dict[str, Any]) -> list[list[list[float]]]:
    geometry = geojson["features"][0]["geometry"]
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"][0]]
    if geometry["type"] == "MultiPolygon":
        return [polygon[0] for polygon in geometry["coordinates"]]
    raise ValueError(f"unsupported boundary geometry: {geometry['type']}")


def render_map(config: dict[str, Any], boundary: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-museum-findspots-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Polygon

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.045, right=0.955, top=0.975, bottom=0.025)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(
        0,
        0.987,
        title["zh"],
        color=COLORS["ink"],
        fontsize=15.3,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0,
        0.948,
        title["ja"],
        color=COLORS["ink"],
        fontsize=8.6,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0,
        0.919,
        title["en"],
        color=COLORS["cobalt"],
        fontsize=7.5,
        fontweight="bold",
        va="top",
    )
    ax.text(
        1,
        0.919,
        "COUNTY / CITY ANCHORS · NOT EXCAVATION COORDINATES",
        color=COLORS["muted"],
        fontsize=5.45,
        fontweight="bold",
        ha="right",
        va="top",
    )

    rings = polygon_rings(boundary)
    all_coords = [coord for ring in rings for coord in ring]
    min_lon = min(coord[0] for coord in all_coords)
    max_lon = max(coord[0] for coord in all_coords)
    min_lat = min(coord[1] for coord in all_coords)
    max_lat = max(coord[1] for coord in all_coords)
    map_box = (0.035, 0.405, 0.93, 0.47)

    def project(lon: float, lat: float) -> tuple[float, float]:
        x0, y0, width, height = map_box
        x = x0 + (lon - min_lon) / (max_lon - min_lon) * width
        y = y0 + (lat - min_lat) / (max_lat - min_lat) * height
        return x, y

    ax.add_patch(
        FancyBboxPatch(
            (map_box[0] - 0.012, map_box[1] - 0.012),
            map_box[2] + 0.024,
            map_box[3] + 0.024,
            boxstyle="round,pad=0.005,rounding_size=0.014",
            facecolor="#F8FAFC",
            edgecolor=COLORS["line"],
            linewidth=1.0,
        )
    )
    for ring in rings:
        ax.add_patch(
            Polygon(
                [project(float(lon), float(lat)) for lon, lat in ring],
                closed=True,
                facecolor=COLORS["land"],
                edgecolor=COLORS["ink"],
                linewidth=1.15,
                zorder=2,
            )
        )

    label_offsets = {
        "museum": (0.018, -0.02, "left"),
        "qinan": (0.025, 0.005, "left"),
        "gangu": (-0.025, -0.025, "right"),
        "jingchuan": (0.02, 0.025, "left"),
        "wuwei": (0.02, 0.025, "left"),
        "jiayuguan": (-0.018, 0.03, "right"),
        "dunhuang": (0.018, 0.025, "left"),
    }
    short_labels = {
        "museum": "兰州 / 蘭州",
        "qinan": "秦安",
        "gangu": "甘谷",
        "jingchuan": "泾川 / 涇川",
        "wuwei": "武威",
        "jiayuguan": "嘉峪关 / 嘉峪関",
        "dunhuang": "敦煌",
    }
    marker_offsets = {
        "qinan": (0.024, 0.016),
        "gangu": (-0.024, -0.016),
    }
    for point in config["points"]:
        anchor_x, anchor_y = project(float(point["lon"]), float(point["lat"]))
        offset_x, offset_y = marker_offsets.get(point["id"], (0.0, 0.0))
        x, y = anchor_x + offset_x, anchor_y + offset_y
        color = COLORS[GROUP_COLORS[point["group"]]]
        radius = 0.025 if point["group"] == "museum" else 0.019
        if offset_x or offset_y:
            ax.plot(
                [anchor_x, x],
                [anchor_y, y],
                color=color,
                linewidth=1.0,
                zorder=4,
            )
        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=color,
                edgecolor=COLORS["paper"],
                linewidth=1.7,
                zorder=6,
            )
        )
        symbol = "◆" if point["group"] == "museum" else str(point["number"])
        ax.text(
            x,
            y,
            symbol,
            color="white",
            fontsize=7.8 if point["group"] == "museum" else 7.2,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=7,
        )
        dx, dy, align = label_offsets[point["id"]]
        ax.text(
            x + dx,
            y + dy,
            short_labels[point["id"]],
            color=COLORS["ink"],
            fontsize=7.5,
            fontweight="bold",
            ha=align,
            va="center",
            zorder=8,
            bbox={"facecolor": COLORS["paper"], "edgecolor": "none", "pad": 1.2, "alpha": 0.9},
        )

    museum = config["points"][0]
    ax.add_patch(
        FancyBboxPatch(
            (0.035, 0.329),
            0.93,
            0.055,
            boxstyle="round,pad=0.007,rounding_size=0.011",
            facecolor=COLORS["cobalt_light"],
            edgecolor=COLORS["cobalt"],
            linewidth=1.1,
        )
    )
    ax.text(0.055, 0.367, "◆", color=COLORS["cobalt"], fontsize=8.0, fontweight="bold", va="center")
    ax.text(0.085, 0.369, museum["zh"], color=COLORS["ink"], fontsize=8.0, fontweight="bold", va="center")
    ax.text(0.085, 0.349, museum["ja"], color=COLORS["ink"], fontsize=7.0, fontweight="bold", va="center")
    ax.text(0.60, 0.358, museum["en"], color=COLORS["cobalt"], fontsize=6.7, fontweight="bold", va="center")

    cards = config["points"][1:]
    for index, point in enumerate(cards):
        col = index % 2
        row = index // 2
        x = 0.035 + col * 0.475
        y = 0.235 - row * 0.09
        color_key = GROUP_COLORS[point["group"]]
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                0.455,
                0.072,
                boxstyle="round,pad=0.006,rounding_size=0.01",
                facecolor=COLORS[f"{color_key}_light"],
                edgecolor=COLORS[color_key],
                linewidth=0.95,
            )
        )
        ax.add_patch(
            Circle(
                (x + 0.027, y + 0.036),
                0.017,
                facecolor=COLORS[color_key],
                edgecolor=COLORS["paper"],
                linewidth=1.0,
            )
        )
        ax.text(
            x + 0.027,
            y + 0.036,
            str(point["number"]),
            color="white",
            fontsize=6.6,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(x + 0.055, y + 0.057, point["zh"], color=COLORS["ink"], fontsize=7.1, fontweight="bold", va="center")
        ax.text(x + 0.055, y + 0.036, point["ja"], color=COLORS["ink"], fontsize=6.2, fontweight="bold", va="center")
        ax.text(x + 0.055, y + 0.015, point["en"], color=COLORS[color_key], fontsize=5.7, fontweight="bold", va="center")

    ax.text(
        0,
        0.032,
        "位置用于省域辨认，不表示考古点、路线或车程 · ORIENTATION ONLY",
        color=COLORS["ink"],
        fontsize=5.8,
        fontweight="bold",
        va="center",
    )
    ax.text(
        1,
        0.012,
        "Map design © LazyTravel · boundary/anchors © OpenStreetMap contributors (ODbL)",
        color=COLORS["muted"],
        fontsize=4.35,
        ha="right",
        va="bottom",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "LazyTravel", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        dpi=300,
        facecolor=COLORS["paper"],
        metadata={"Software": "LazyTravel"},
    )
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), facecolor=COLORS["paper"], metadata=metadata)
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(
        svg_path,
        facecolor=COLORS["paper"],
        metadata={"Creator": "LazyTravel", "Date": "2026-08-22"},
    )
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def main() -> int:
    config = read_json(CONFIG_PATH)
    boundary_path = ROOT / config["boundary_geojson"]
    boundary = read_json(boundary_path)
    render_map(config, boundary)
    outputs = {
        path.suffix.lstrip("."): output_record(path)
        for path in (
            OUTPUT_STEM.with_suffix(".svg"),
            OUTPUT_STEM.with_suffix(".pdf"),
            OUTPUT_STEM.with_suffix(".png"),
        )
    }
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-lanzhou-museum-findspots-map",
        "method": "deterministic-map-render",
        "created_at": config["snapshot_date"],
        "source_config": output_record(CONFIG_PATH),
        "source_geojson": output_record(boundary_path),
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": "Map design © LazyTravel; boundary and orientation anchors derived from OpenStreetMap under ODbL; object relationships derive from the cited museum catalogue.",
        "visual_qa": config["visual_qa"],
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(json.dumps({"outputs": outputs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
