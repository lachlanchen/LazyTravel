#!/usr/bin/env python3
"""Render the schematic Xi'an successive-capitals map from declared data."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-capital-layers.config.json"
BASE_GEOJSON_PATH = ROOT / "data/maps/xian/xian-before-walls.geojson"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-capital-layers"
FIXED_TIME = datetime(2026, 8, 14, tzinfo=timezone.utc)

PAPER = "#F5F2EA"
INK = "#202522"
MUTED = "#5C625E"
WATER = "#4D94AE"
VERMILION = "#B44736"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_lines(geometry: dict[str, Any]) -> Iterable[list[list[float]]]:
    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]
    if geometry_type == "LineString":
        yield coordinates
    elif geometry_type == "MultiLineString":
        yield from coordinates
    elif geometry_type == "Polygon":
        yield from coordinates
    elif geometry_type == "MultiPolygon":
        for polygon in coordinates:
            yield from polygon


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def configure_fonts() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK JP"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )


def draw_geography(ax: Any, geojson: dict[str, Any]) -> None:
    for feature in geojson["features"]:
        properties = feature["properties"]
        kind = properties.get("kind")
        if kind not in {"river", "wall"}:
            continue
        for line in iter_lines(feature["geometry"]):
            xs = [point[0] for point in line]
            ys = [point[1] for point in line]
            if kind == "wall":
                ax.plot(xs, ys, color=VERMILION, linewidth=2.0, zorder=8)
            else:
                ax.plot(
                    xs,
                    ys,
                    color=WATER,
                    linewidth=1.0 if properties.get("river_key") in {"wei", "feng"} else 0.55,
                    alpha=0.70 if properties.get("river_key") in {"wei", "feng"} else 0.35,
                    linestyle=(0, (4, 3)) if properties.get("generalized") else "solid",
                    zorder=1,
                )


def draw_schematic_area(ax: Any, area: dict[str, Any]) -> None:
    color = area["color"]
    if area["shape"] == "ellipse":
        patch = Ellipse(
            area["center"],
            area["width"],
            area["height"],
            facecolor=color,
            edgecolor=color,
            linewidth=1.2,
            linestyle=(0, (5, 3)),
            alpha=0.22,
            zorder=3,
        )
        label_x, label_y = area["center"]
    else:
        patch = Polygon(
            area["coordinates"],
            closed=True,
            facecolor=color,
            edgecolor=color,
            linewidth=1.3,
            linestyle=(0, (5, 3)),
            alpha=0.18,
            zorder=2,
        )
        label_x = sum(point[0] for point in area["coordinates"]) / len(area["coordinates"])
        label_y = sum(point[1] for point in area["coordinates"]) / len(area["coordinates"])
    ax.add_patch(patch)

    offsets = {
        "feng": (-0.010, 0.003),
        "hao": (0.010, -0.006),
        "qin-xianyang": (0.000, 0.004),
        "han-changan": (-0.004, 0.000),
        "sui-tang": (-0.015, -0.047),
        "daming": (0.000, 0.002),
    }
    dx, dy = offsets[area["id"]]
    ax.text(
        label_x + dx,
        label_y + dy,
        area["label"],
        ha="center",
        va="center",
        fontsize=12.5 if area["id"] != "sui-tang" else 13.0,
        fontweight="bold",
        color=INK,
        zorder=9,
        bbox={
            "boxstyle": "square,pad=0.18",
            "facecolor": PAPER,
            "edgecolor": "none",
            "alpha": 0.78,
        },
    )


def render(config: dict[str, Any], geojson: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    extent = config["extent"]
    fig = plt.figure(figsize=(14, 9), facecolor=PAPER)
    ax = fig.add_axes([0.045, 0.105, 0.91, 0.77], facecolor=PAPER)
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")

    fig.text(0.055, 0.948, config["title"]["zh"], fontsize=22, fontweight="bold", color=INK)
    fig.text(0.055, 0.907, config["title"]["ja"], fontsize=11, color="#315347")
    fig.text(
        0.945,
        0.925,
        config["title"]["en"],
        fontsize=10,
        fontweight="bold",
        color=VERMILION,
        ha="right",
    )
    fig.text(
        0.945,
        0.895,
        "RELATIVE POSITION · SCHEMATIC EXTENTS",
        fontsize=6.6,
        color=MUTED,
        ha="right",
    )

    draw_geography(ax, geojson)
    for area in config["schematic_areas"]:
        draw_schematic_area(ax, area)

    ax.text(108.690, 34.393, "渭河  WEI RIVER", fontsize=11.5, color=WATER, rotation=2)
    ax.text(108.758, 34.165, "沣河\nFENG RIVER", fontsize=10.5, color=WATER, ha="center")

    for landmark in config["landmarks"]:
        x, y = landmark["position"]
        ax.scatter(
            [x],
            [y],
            marker="o",
            s=20,
            facecolor=PAPER,
            edgecolor=INK,
            linewidth=0.8,
            zorder=10,
        )
        ax.text(
            x + 0.006,
            y - 0.002,
            landmark["label"],
            fontsize=8.8,
            va="center",
            color=MUTED,
            zorder=10,
        )

    ax.annotate(
        "明清西安 / MING-QING\nTODAY'S WALL",
        xy=(108.946, 34.268),
        xytext=(109.013, 34.265),
        fontsize=10.5,
        fontweight="bold",
        color=VERMILION,
        ha="center",
        arrowprops={"arrowstyle": "-", "color": VERMILION, "lw": 0.9},
        zorder=11,
    )

    ax.annotate(
        "N",
        xy=(109.026, 34.382),
        xytext=(109.026, 34.350),
        ha="center",
        fontsize=10.5,
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": INK},
    )

    km_per_lon_degree = 111.32 * math.cos(math.radians(mean_latitude))
    scale_degrees = 10 / km_per_lon_degree
    sx, sy = 108.655, 34.153
    ax.plot([sx, sx + scale_degrees], [sy, sy], color=INK, linewidth=1.0, zorder=12)
    ax.plot([sx, sx], [sy - 0.003, sy + 0.003], color=INK, linewidth=0.9, zorder=12)
    ax.plot(
        [sx + scale_degrees, sx + scale_degrees],
        [sy - 0.003, sy + 0.003],
        color=INK,
        linewidth=0.9,
        zorder=12,
    )
    ax.text(sx + scale_degrees / 2, sy + 0.006, "10 km", fontsize=8.8, ha="center", color=INK)

    fig.text(
        0.055,
        0.050,
        "概化范围，不是考古边界 / 概略範囲・考古学的境界ではない\n"
        "SCHEMATIC EXTENTS · NOT FOR SITE ACCESS OR NAVIGATION",
        fontsize=6.0,
        color=MUTED,
        linespacing=1.25,
    )
    fig.text(
        0.945,
        0.050,
        "Original synthesis: LazyTravel · lazying.art\n"
        "Present geography: OpenStreetMap contributors · ODbL 1.0",
        fontsize=5.8,
        color=MUTED,
        ha="right",
        linespacing=1.25,
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Successive Capitals, Different Sites",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Schematic relative positions of Xi'an capital sites",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), format="pdf", metadata=metadata)
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(
        svg_path,
        format="svg",
        metadata={"Title": metadata["Title"], "Date": config["snapshot_date"]},
    )
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        format="png",
        dpi=400,
        metadata={"Title": metadata["Title"], "Author": metadata["Author"]},
    )
    plt.close(fig)

    from PIL import Image

    with Image.open(OUTPUT_STEM.with_suffix(".png")) as image:
        dimensions = [image.width, image.height]
    return {
        "png_dimensions": dimensions,
        "minimum_png_width": 3600,
        "pdf_vector_output": True,
        "svg_selectable_text": True,
    }


def write_provenance(config: dict[str, Any], technical: dict[str, Any]) -> None:
    files = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    write_json(
        OUTPUT_STEM.with_suffix(".provenance.json"),
        {
            "schema_version": 1,
            "asset_id": "asset-xian-capital-layers-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_capital_layers_map.py",
            "config": {
                "path": str(CONFIG_PATH.relative_to(ROOT)),
                "sha256": sha256(CONFIG_PATH),
            },
            "present_geography": {
                "path": str(BASE_GEOJSON_PATH.relative_to(ROOT)),
                "sha256": sha256(BASE_GEOJSON_PATH),
            },
            "sources": config["sources"],
            "declared_generalizations": [
                {"id": item["id"], "note": item["note"]} for item in config["schematic_areas"]
            ],
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; present geography © OpenStreetMap contributors, "
                "ODbL 1.0."
            ),
        },
    )


def main() -> int:
    config = read_json(CONFIG_PATH)
    geojson = read_json(BASE_GEOJSON_PATH)
    technical = render(config, geojson)
    write_provenance(config, technical)
    print(f"rendered: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(f"dimensions: {technical['png_dimensions'][0]} x {technical['png_dimensions'][1]} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
