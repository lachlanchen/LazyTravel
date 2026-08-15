#!/usr/bin/env python3
"""Render Xi'an's inside-the-wall route at wall and lane scales."""

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
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-inside-wall-route.config.json"
STREET_GEOJSON_PATH = ROOT / "data/maps/xian/xian-inside-wall-route.geojson"
WALL_GEOJSON_PATH = ROOT / "data/maps/xian/xian-before-walls.geojson"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-inside-wall-route"
FIXED_TIME = datetime(2026, 8, 15, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#CBD5E1"
PALE_BLUE = "#EAF2FF"
PALE_JADE = "#E7F7F3"
COBALT = "#1769E0"
JADE = "#008C72"
VERMILION = "#E24736"
CORAL = "#FF6B4A"
SUN = "#F4B63D"


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


def configure_fonts() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK JP"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-xian-inside-wall-route-v1",
            "pdf.fonttype": 42,
        }
    )


def set_map_extent(ax: Any, extent: list[float]) -> None:
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")


def wall_ring(wall_geojson: dict[str, Any]) -> list[list[float]]:
    for feature in wall_geojson["features"]:
        if feature["properties"].get("kind") != "wall":
            continue
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            return geometry["coordinates"][0]
    raise RuntimeError("present city-wall polygon is missing")


def draw_overview(
    ax: Any, config: dict[str, Any], wall_geojson: dict[str, Any]
) -> None:
    extent = config["overview_extent"]
    set_map_extent(ax, extent)
    ring = wall_ring(wall_geojson)
    ax.add_patch(
        Polygon(
            ring,
            closed=True,
            facecolor=PALE_BLUE,
            edgecolor=VERMILION,
            linewidth=2.7,
            zorder=2,
        )
    )

    bell = next(site for site in config["sites"] if site["id"] == "bell-tower")
    bell_position = bell["position"]
    for gate in config["gates"]:
        gate_position = gate["position"]
        ax.plot(
            [bell_position[0], gate_position[0]],
            [bell_position[1], gate_position[1]],
            color=PAPER,
            linewidth=5.0,
            solid_capstyle="round",
            zorder=3,
        )
        ax.plot(
            [bell_position[0], gate_position[0]],
            [bell_position[1], gate_position[1]],
            color=COBALT,
            linewidth=1.35,
            solid_capstyle="round",
            alpha=0.78,
            zorder=4,
        )

    # The southern highlight communicates a short-segment choice, not gate access.
    ax.plot(
        [108.9390, 108.9497],
        [34.25223, 34.25223],
        color=CORAL,
        linewidth=6.2,
        solid_capstyle="round",
        zorder=5,
    )
    ax.text(
        108.9444,
        34.2501,
        "短走一段  SHORT WALL SEGMENT",
        color=CORAL,
        fontsize=6.0,
        fontweight="bold",
        ha="center",
        va="top",
    )

    for gate in config["gates"]:
        x, y = gate["position"]
        ax.scatter(
            [x],
            [y],
            s=34,
            facecolor=PAPER,
            edgecolor=VERMILION,
            linewidth=1.4,
            zorder=7,
        )
        horizontal = "center"
        vertical = "center"
        dx, dy = 0.0, 0.0
        if gate["id"] == "anding-gate":
            horizontal, dx = "right", -0.0012
        elif gate["id"] == "changle-gate":
            horizontal, dx = "left", 0.0012
        elif gate["id"] == "anyuan-gate":
            vertical, dy = "bottom", 0.0012
        else:
            vertical, dy = "top", -0.0015
        ax.text(
            x + dx,
            y + dy,
            f"{gate['label']['zh']}\n{gate['label']['en']}",
            fontsize=5.6,
            fontweight="bold",
            color=INK,
            ha=horizontal,
            va=vertical,
            linespacing=1.25,
            zorder=8,
        )

    ax.scatter(
        [bell_position[0]],
        [bell_position[1]],
        s=82,
        facecolor=JADE,
        edgecolor=PAPER,
        linewidth=1.5,
        zorder=9,
    )
    ax.text(
        bell_position[0],
        bell_position[1],
        "钟",
        fontsize=7.0,
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=10,
    )

    detail = config["detail_extent"]
    ax.add_patch(
        Rectangle(
            (detail[0], detail[1]),
            detail[2] - detail[0],
            detail[3] - detail[1],
            fill=False,
            edgecolor=JADE,
            linewidth=1.2,
            linestyle=(0, (4, 2)),
            zorder=8,
        )
    )
    ax.text(
        detail[2] + 0.0005,
        detail[3],
        "详图\nDETAIL",
        fontsize=5.4,
        fontweight="bold",
        color=JADE,
        va="top",
        linespacing=1.15,
    )

    bubble_x, bubble_y = 108.9585, 34.2757
    ax.add_patch(
        Circle(
            (bubble_x, bubble_y),
            radius=0.0044,
            facecolor=COBALT,
            edgecolor=PAPER,
            linewidth=1.7,
            zorder=9,
        )
    )
    ax.text(
        bubble_x,
        bubble_y + 0.0003,
        "13.74",
        fontsize=8.4,
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=10,
    )
    ax.text(
        bubble_x,
        bubble_y - 0.0020,
        "KM CIRCUIT",
        fontsize=4.2,
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=10,
    )

    ax.text(
        108.918,
        34.2803,
        "A  城墙全貌  ·  WALL SCALE",
        fontsize=7.2,
        fontweight="bold",
        color=VERMILION,
        va="top",
    )


def draw_street_geometry(ax: Any, street_geojson: dict[str, Any]) -> None:
    for feature in street_geojson["features"]:
        kind = feature["properties"]["kind"]
        if kind == "site":
            continue
        color = COBALT if kind == "major-street" else FAINT
        linewidth = 1.15 if kind == "major-street" else 0.65
        alpha = 0.50 if kind == "major-street" else 0.95
        for line in iter_lines(feature["geometry"]):
            ax.plot(
                [point[0] for point in line],
                [point[1] for point in line],
                color=color,
                linewidth=linewidth,
                alpha=alpha,
                solid_capstyle="round",
                zorder=2,
            )


def draw_routes(ax: Any, config: dict[str, Any]) -> dict[str, float]:
    lengths: dict[str, float] = {}
    for route in config["routes"]:
        points = route["coordinates"]
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]
        color = JADE if route["kind"] == "core" else CORAL
        linestyle: str | tuple[int, tuple[int, ...]] = "-"
        linewidth = 2.5
        if route["kind"] == "optional":
            linestyle = (0, (4, 2.5))
            linewidth = 1.7
        ax.plot(
            x_values,
            y_values,
            color=PAPER,
            linewidth=linewidth + 3.0,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=4,
        )
        ax.plot(
            x_values,
            y_values,
            color=color,
            linewidth=linewidth,
            linestyle=linestyle,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=5,
        )
        lengths[route["id"]] = route_length_km(points)
    return lengths


def route_length_km(points: list[list[float]]) -> float:
    total = 0.0
    for first, second in zip(points, points[1:]):
        lon1, lat1 = map(math.radians, first)
        lon2, lat2 = map(math.radians, second)
        delta_lon = lon2 - lon1
        delta_lat = lat2 - lat1
        value = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(delta_lon / 2) ** 2
        )
        total += 6371.0088 * 2 * math.asin(math.sqrt(value))
    return total


def draw_sites(ax: Any, config: dict[str, Any]) -> None:
    colors = [VERMILION, CORAL, COBALT, SUN, JADE, COBALT]
    for site, color in zip(config["sites"], colors, strict=True):
        x, y = site["position"]
        dx, dy = site["label_offset"]
        optional = site.get("optional", False)
        ax.scatter(
            [x],
            [y],
            s=85,
            facecolor=PAPER if optional else color,
            edgecolor=color,
            linewidth=1.8,
            zorder=8,
        )
        ax.text(
            x,
            y,
            str(site["order"]),
            fontsize=7.2,
            fontweight="bold",
            color=color if optional else PAPER,
            ha="center",
            va="center",
            zorder=9,
        )
        horizontal = "left" if dx >= 0 else "right"
        label_x, label_y = x + dx, y + dy
        ax.text(
            label_x,
            label_y,
            site["label"]["zh"],
            fontsize=6.7,
            fontweight="bold",
            color=INK,
            ha=horizontal,
            va="bottom",
            zorder=9,
            bbox={
                "boxstyle": "square,pad=0.15",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.92,
            },
        )
        ax.text(
            label_x,
            label_y - 0.00020,
            site["label"]["en"],
            fontsize=4.4,
            fontweight="bold",
            color=color,
            ha=horizontal,
            va="top",
            zorder=9,
        )


def draw_lane_labels(ax: Any, config: dict[str, Any]) -> None:
    for label in config["lane_labels"]:
        x, y = label["position"]
        ax.text(
            x,
            y,
            f"{label['name']}  {label['en']}",
            fontsize=4.2,
            color=MUTED,
            rotation=label["rotation"],
            rotation_mode="anchor",
            ha="center",
            va="center",
            zorder=3,
            bbox={
                "boxstyle": "square,pad=0.10",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.84,
            },
        )


def draw_scale(ax: Any, extent: list[float]) -> None:
    mean_latitude = (extent[1] + extent[3]) / 2
    scale_degrees = 0.25 / (111.32 * math.cos(math.radians(mean_latitude)))
    start_x, start_y = extent[2] - scale_degrees - 0.0012, extent[1] + 0.0008
    ax.plot(
        [start_x, start_x + scale_degrees],
        [start_y, start_y],
        color=INK,
        linewidth=1.2,
        zorder=10,
    )
    ax.plot(
        [start_x, start_x],
        [start_y - 0.00016, start_y + 0.00016],
        color=INK,
        linewidth=0.9,
        zorder=10,
    )
    ax.plot(
        [start_x + scale_degrees, start_x + scale_degrees],
        [start_y - 0.00016, start_y + 0.00016],
        color=INK,
        linewidth=0.9,
        zorder=10,
    )
    ax.text(
        start_x + scale_degrees / 2,
        start_y + 0.00028,
        "250 m",
        fontsize=4.5,
        color=INK,
        ha="center",
        va="bottom",
    )


def draw_detail(
    ax: Any, config: dict[str, Any], street_geojson: dict[str, Any]
) -> dict[str, float]:
    extent = config["detail_extent"]
    set_map_extent(ax, extent)
    ax.add_patch(
        Rectangle(
            (extent[0], extent[1]),
            extent[2] - extent[0],
            extent[3] - extent[1],
            facecolor=PALE_JADE,
            edgecolor="none",
            alpha=0.40,
            zorder=0,
        )
    )
    draw_street_geometry(ax, street_geojson)
    lengths = draw_routes(ax, config)
    draw_lane_labels(ax, config)
    draw_sites(ax, config)
    draw_scale(ax, extent)
    ax.text(
        108.9323,
        34.2677,
        "B  中心与小路  ·  STREET SCALE",
        fontsize=7.2,
        fontweight="bold",
        color=JADE,
        va="top",
    )
    ax.annotate(
        "N",
        xy=(108.9491, 34.2671),
        xytext=(108.9491, 34.2658),
        ha="center",
        va="bottom",
        fontsize=5.4,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 0.9, "color": INK},
    )
    return lengths


def draw_legend(fig: Any) -> None:
    y = 0.075
    items = [
        (0.055, JADE, "半日主线  HALF-DAY CORE", "solid"),
        (0.285, CORAL, "可选支线  OPTIONAL DETOUR", "dashed"),
        (0.555, COBALT, "四条大街  FOUR MAIN STREETS", "solid"),
        (0.805, VERMILION, "明城墙  MING WALL", "solid"),
    ]
    for x, color, label, style in items:
        line = plt.Line2D(
            [x, x + 0.027],
            [y, y],
            transform=fig.transFigure,
            color=color,
            linewidth=2.2,
            linestyle=(0, (4, 2.5)) if style == "dashed" else "-",
            solid_capstyle="round",
        )
        fig.add_artist(line)
        fig.text(x + 0.034, y, label, fontsize=5.4, color=INK, va="center")


def render(
    config: dict[str, Any],
    street_geojson: dict[str, Any],
    wall_geojson: dict[str, Any],
) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(14, 9), facecolor=PAPER)
    overview = fig.add_axes([0.055, 0.16, 0.37, 0.66], facecolor=PAPER)
    detail = fig.add_axes([0.455, 0.16, 0.49, 0.66], facecolor=PAPER)

    fig.text(
        0.055,
        0.948,
        config["title"]["zh"],
        fontsize=22,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.055, 0.906, config["title"]["ja"], fontsize=11, color=JADE)
    fig.text(
        0.945,
        0.925,
        config["title"]["en"],
        fontsize=8.8,
        fontweight="bold",
        color=VERMILION,
        ha="right",
    )
    fig.text(
        0.945,
        0.892,
        "WALL SCALE + STREET SCALE",
        fontsize=6.2,
        fontweight="bold",
        color=COBALT,
        ha="right",
    )

    draw_overview(overview, config, wall_geojson)
    route_lengths = draw_detail(detail, config, street_geojson)
    draw_legend(fig)
    fig.add_artist(
        plt.Line2D(
            [0.055, 0.945],
            [0.118, 0.118],
            transform=fig.transFigure,
            color=FAINT,
            linewidth=0.7,
        )
    )
    fig.text(
        0.055,
        0.035,
        "路线示意，不替代当日导航、门点开放或现场边界。",
        fontsize=5.4,
        color=MUTED,
        va="bottom",
    )
    fig.text(
        0.50,
        0.035,
        "ROUTE LOGIC · CHECK LIVE NAVIGATION, ACCESS POINTS AND ON-SITE LIMITS",
        fontsize=5.1,
        color=MUTED,
        ha="center",
        va="bottom",
    )
    fig.text(
        0.945,
        0.035,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=5.0,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Inside the Wall: Crossroads and Lanes",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Two-scale route map for central Xi'an",
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
        "route_lengths_km": {
            route_id: round(length, 3) for route_id, length in route_lengths.items()
        },
        "street_feature_count": len(street_geojson["features"]),
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
            "asset_id": "asset-xian-inside-wall-route-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_inside_wall_route_map.py",
            "config": {
                "path": str(CONFIG_PATH.relative_to(ROOT)),
                "sha256": sha256(CONFIG_PATH),
            },
            "present_geography": [
                {
                    "path": str(STREET_GEOJSON_PATH.relative_to(ROOT)),
                    "sha256": sha256(STREET_GEOJSON_PATH),
                },
                {
                    "path": str(WALL_GEOJSON_PATH.relative_to(ROOT)),
                    "sha256": sha256(WALL_GEOJSON_PATH),
                },
            ],
            "sources": config["sources"],
            "declared_generalizations": [
                {"id": "wall-segment", "note": config["wall"]["note"]},
                *[
                    {"id": route["id"], "note": route["note"]}
                    for route in config["routes"]
                ],
            ],
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; present wall, street, and site geometry "
                "© OpenStreetMap contributors, ODbL 1.0."
            ),
        },
    )


def main() -> int:
    config = read_json(CONFIG_PATH)
    street_geojson = read_json(STREET_GEOJSON_PATH)
    wall_geojson = read_json(WALL_GEOJSON_PATH)
    technical = render(config, street_geojson, wall_geojson)
    write_provenance(config, technical)
    print(f"rendered: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(f"dimensions: {technical['png_dimensions'][0]} x {technical['png_dimensions'][1]} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
