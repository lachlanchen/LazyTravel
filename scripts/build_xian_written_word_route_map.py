#!/usr/bin/env python3
"""Render Xi'an's pagodas-to-Beilin written-word route schematic."""

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
from matplotlib.patches import Circle, Polygon

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-written-word-route.config.json"
BASE_GEOJSON_PATH = ROOT / "data/maps/xian/xian-before-walls.geojson"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-written-word-route"
FIXED_TIME = datetime(2026, 8, 15, tzinfo=timezone.utc)

PAPER = "#F5F2EA"
INK = "#202522"
MUTED = "#5C625E"
GRID = "#C9C4B8"
TANG = "#C87532"
VERMILION = "#A84B3C"
ROUTE = "#356B61"


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


def haversine_km(first: list[float], second: list[float]) -> float:
    lon1, lat1 = map(math.radians, first)
    lon2, lat2 = map(math.radians, second)
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 6371.0088 * 2 * math.asin(math.sqrt(value))


def ordered_sites(config: dict[str, Any]) -> list[dict[str, Any]]:
    sites = {site["id"]: site for site in config["sites"]}
    return [sites[site_id] for site_id in config["route"]["sequence"]]


def configure_fonts() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK JP"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-xian-written-word-route-v1",
            "pdf.fonttype": 42,
        }
    )


def draw_present_wall(ax: Any, geojson: dict[str, Any]) -> None:
    for feature in geojson["features"]:
        if feature["properties"].get("kind") != "wall":
            continue
        for line in iter_lines(feature["geometry"]):
            ax.plot(
                [point[0] for point in line],
                [point[1] for point in line],
                color=VERMILION,
                linewidth=2.1,
                zorder=4,
            )


def draw_scale(ax: Any, extent: list[float]) -> None:
    mean_latitude = (extent[1] + extent[3]) / 2
    scale_degrees = 2 / (111.32 * math.cos(math.radians(mean_latitude)))
    sx, sy = extent[0] + 0.010, extent[1] + 0.010
    ax.plot([sx, sx + scale_degrees], [sy, sy], color=INK, linewidth=1.1, zorder=10)
    ax.plot([sx, sx], [sy - 0.0018, sy + 0.0018], color=INK, linewidth=0.9, zorder=10)
    ax.plot(
        [sx + scale_degrees, sx + scale_degrees],
        [sy - 0.0018, sy + 0.0018],
        color=INK,
        linewidth=0.9,
        zorder=10,
    )
    ax.text(sx + scale_degrees / 2, sy + 0.0035, "2 km", fontsize=8.0, ha="center")


def draw_sites(ax: Any, config: dict[str, Any]) -> float:
    sites = ordered_sites(config)
    route_x = [site["position"][0] for site in sites]
    route_y = [site["position"][1] for site in sites]
    ax.plot(
        route_x,
        route_y,
        color=PAPER,
        linewidth=5.0,
        solid_capstyle="round",
        zorder=5,
    )
    ax.plot(
        route_x,
        route_y,
        color=ROUTE,
        linewidth=1.8,
        linestyle=(0, (5, 3)),
        solid_capstyle="round",
        zorder=6,
    )

    for site in sites:
        x, y = site["position"]
        dx, dy = site["label_offset"]
        label_x, label_y = x + dx, y + dy
        marker = Circle(
            (x, y),
            radius=0.0042,
            transform=ax.transData,
            facecolor=ROUTE,
            edgecolor=PAPER,
            linewidth=1.6,
            zorder=8,
        )
        ax.add_patch(marker)
        ax.text(
            x,
            y,
            str(site["order"]),
            color=PAPER,
            fontsize=9.0,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=9,
        )
        align = "left" if dx > 0 else "right"
        connector_x = label_x - 0.002 if dx > 0 else label_x + 0.002
        ax.plot([x, connector_x], [y, label_y], color=ROUTE, linewidth=0.8, zorder=6)
        ax.text(
            label_x,
            label_y,
            site["label"]["zh"],
            ha=align,
            va="center",
            fontsize=10.4,
            fontweight="bold",
            color=INK,
            zorder=9,
            bbox={
                "boxstyle": "square,pad=0.24",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.94,
            },
        )
        ax.text(
            label_x,
            label_y - 0.0067,
            site["label"]["en"],
            ha=align,
            va="top",
            fontsize=6.3,
            fontweight="bold",
            color=MUTED,
            zorder=9,
        )

    return sum(
        haversine_km(first["position"], second["position"])
        for first, second in zip(sites, sites[1:])
    )


def render(config: dict[str, Any], geojson: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    extent = config["extent"]
    fig = plt.figure(figsize=(14, 9), facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.13, 0.89, 0.72], facecolor=PAPER)
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")

    fig.text(0.055, 0.948, config["title"]["zh"], fontsize=22, fontweight="bold", color=INK)
    fig.text(0.055, 0.907, config["title"]["ja"], fontsize=11, color=ROUTE)
    fig.text(
        0.945,
        0.925,
        config["title"]["en"],
        fontsize=9.5,
        fontweight="bold",
        color=VERMILION,
        ha="right",
    )
    fig.text(
        0.945,
        0.896,
        "ONE COMMON SCALE · SOUTH TO NORTH",
        fontsize=6.4,
        color=MUTED,
        ha="right",
    )

    tang = config["tang_outer_city"]
    ax.add_patch(
        Polygon(
            tang["coordinates"],
            closed=True,
            facecolor=TANG,
            edgecolor=TANG,
            linewidth=1.4,
            linestyle=(0, (6, 3)),
            alpha=0.10,
            zorder=1,
        )
    )
    ax.text(
        108.875,
        34.294,
        tang["label"],
        fontsize=7.4,
        fontweight="bold",
        color=TANG,
        va="top",
        linespacing=1.35,
    )
    draw_present_wall(ax, geojson)
    ax.text(
        108.922,
        34.279,
        "今城墙  PRESENT CITY WALL",
        fontsize=7.1,
        fontweight="bold",
        color=VERMILION,
        va="bottom",
    )
    route_length = draw_sites(ax, config)
    draw_scale(ax, extent)
    ax.annotate(
        "N",
        xy=(108.998, 34.297),
        xytext=(108.998, 34.279),
        ha="center",
        va="bottom",
        fontsize=9.0,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": INK},
    )

    fig.add_artist(
        plt.Line2D(
            [0.055, 0.945],
            [0.105, 0.105],
            transform=fig.transFigure,
            color=GRID,
            linewidth=0.7,
        )
    )
    fig.text(
        0.055,
        0.061,
        "半日选两处 · 三处留整日 / 半日は二か所 · 三か所なら一日\n"
        "HALF DAY: CHOOSE TWO · FULL DAY: ALL THREE",
        fontsize=6.4,
        fontweight="bold",
        color=INK,
        linespacing=1.3,
    )
    fig.text(
        0.945,
        0.061,
        "章节顺序，不是步行或公交线路 / 章の順序・経路案内ではない\n"
        "CHAPTER SEQUENCE · NOT A STREET OR TRANSIT ROUTE",
        fontsize=5.9,
        color=MUTED,
        ha="right",
        linespacing=1.3,
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Three Places to Read the City",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Schematic route from Xi'an's pagodas to Beilin",
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
        "schematic_join_length_km": round(route_length, 3),
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
            "asset_id": "asset-xian-written-word-route-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_written_word_route_map.py",
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
                {"id": "tang-outer-city", "note": config["tang_outer_city"]["note"]},
                {"id": "written-word-route", "note": config["route"]["note"]},
                *[{"id": site["id"], "note": site["note"]} for site in config["sites"]],
            ],
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; present wall geometry © OpenStreetMap "
                "contributors, ODbL 1.0; open-guide coordinates CC BY-SA 4.0."
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
