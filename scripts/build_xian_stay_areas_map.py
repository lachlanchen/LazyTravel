#!/usr/bin/env python3
"""Render Xi'an's five itinerary-led stay areas."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-stay-areas.config.json"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-stay-areas"
FIXED_TIME = datetime(2026, 8, 16, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#D9E2EC"
GRID = "#E9EFF5"
WALL_FILL = "#FFF0EC"
WALL_EDGE = "#F05A47"
CORAL = "#F05A47"
COBALT = "#1769E0"
JADE = "#008C72"
BERRY = "#B33273"
SAFFRON = "#E3A008"
ZONE_COLORS = [CORAL, COBALT, JADE, BERRY, SAFFRON]


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


def configure_fonts() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK JP"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-xian-stay-areas-v1",
            "pdf.fonttype": 42,
        }
    )


def set_extent(ax: Any, extent: list[float]) -> None:
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")


def panel_frame(fig: Any, bounds: list[float], title: str, accent: str) -> None:
    x, y, width, height = bounds
    fig.add_artist(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.008,rounding_size=0.009",
            transform=fig.transFigure,
            facecolor=PAPER,
            edgecolor=FAINT,
            linewidth=1.1,
            zorder=0,
        )
    )
    fig.text(
        x + 0.014,
        y + height - 0.014,
        title,
        fontsize=9.1,
        fontweight="bold",
        color=accent,
        ha="left",
        va="top",
    )


def draw_zone(
    ax: Any, zone: dict[str, Any], color: str, marker_scale: float = 1.0
) -> None:
    x, y = zone["position"]
    dx, dy = zone["label_offset"]
    label_x, label_y = x + dx, y + dy
    align = "left" if dx >= 0 else "right"

    ax.scatter(
        [x],
        [y],
        s=470 * marker_scale,
        facecolor=PAPER,
        edgecolor=color,
        linewidth=3.0,
        zorder=9,
    )
    ax.scatter(
        [x],
        [y],
        s=300 * marker_scale,
        facecolor=color,
        edgecolor="none",
        zorder=10,
    )
    ax.text(
        x,
        y,
        str(zone["order"]),
        fontsize=14.0 * math.sqrt(marker_scale),
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=11,
    )
    ax.plot([x, label_x], [y, label_y], color=color, linewidth=1.35, zorder=8)
    ax.text(
        label_x,
        label_y,
        zone["label"]["zh"],
        fontsize=13.0,
        fontweight="bold",
        color=INK,
        ha=align,
        va="bottom",
        zorder=12,
        bbox={
            "boxstyle": "round,pad=0.14,rounding_size=0.05",
            "facecolor": PAPER,
            "edgecolor": "none",
            "alpha": 0.94,
        },
    )
    ax.text(
        label_x,
        label_y,
        zone["label"]["en"],
        fontsize=7.9,
        fontweight="bold",
        color=color,
        ha=align,
        va="top",
        zorder=12,
    )


def draw_regional_panel(ax: Any, config: dict[str, Any]) -> None:
    set_extent(ax, config["regional_extent"])
    focus = config["schematic_features"]["central_focus"]
    bounds = focus["bounds"]
    ax.add_patch(
        Rectangle(
            (bounds[0], bounds[1]),
            bounds[2] - bounds[0],
            bounds[3] - bounds[1],
            facecolor=WALL_FILL,
            edgecolor=WALL_EDGE,
            linewidth=2.0,
            linestyle=(0, (4, 2)),
            zorder=2,
        )
    )
    ax.text(
        *focus["label_position"],
        "CENTRAL INSET",
        fontsize=8.4,
        fontweight="bold",
        color=WALL_EDGE,
        ha="left",
        va="bottom",
        zorder=3,
    )

    anchors = {anchor["id"]: anchor for anchor in config["regional_anchors"]}
    central = anchors["central-xian"]["position"]
    north = anchors["xian-north"]["position"]
    lintong = anchors["lintong"]["position"]
    ax.plot(
        [central[0], north[0]],
        [central[1], north[1]],
        color=GRID,
        linewidth=2.1,
        linestyle=(0, (3, 3)),
        zorder=1,
    )
    ax.plot(
        [central[0], lintong[0]],
        [central[1], lintong[1]],
        color=GRID,
        linewidth=2.1,
        linestyle=(0, (3, 3)),
        zorder=1,
    )
    ax.text(
        109.083,
        34.303,
        "POSITION ONLY · NOT A ROUTE",
        fontsize=7.2,
        fontweight="bold",
        color=MUTED,
        rotation=14,
        ha="center",
        va="center",
        zorder=2,
    )

    lintong_sources = anchors["lintong"]["source_positions"]
    ax.plot(
        [item["position"][0] for item in lintong_sources],
        [item["position"][1] for item in lintong_sources],
        color=SAFFRON,
        linewidth=4.0,
        alpha=0.28,
        solid_capstyle="round",
        zorder=2,
    )
    for item in lintong_sources:
        ax.scatter(
            [item["position"][0]],
            [item["position"][1]],
            s=36,
            facecolor=SAFFRON,
            edgecolor=PAPER,
            linewidth=1.0,
            zorder=5,
        )

    for zone, color in zip(config["zones"], ZONE_COLORS, strict=True):
        if zone["panel"] == "regional":
            draw_zone(ax, zone, color)


def draw_central_panel(ax: Any, config: dict[str, Any]) -> None:
    set_extent(ax, config["central_extent"])
    features = config["schematic_features"]
    wall = features["walled_core"]
    bounds = wall["bounds"]
    ax.add_patch(
        Rectangle(
            (bounds[0], bounds[1]),
            bounds[2] - bounds[0],
            bounds[3] - bounds[1],
            facecolor=WALL_FILL,
            edgecolor=WALL_EDGE,
            linewidth=2.2,
            zorder=2,
        )
    )
    ax.text(
        *wall["label_position"],
        "明城墙  明城壁  MING WALL",
        fontsize=8.4,
        fontweight="bold",
        color=WALL_EDGE,
        ha="left",
        va="bottom",
        zorder=5,
    )

    line_2 = features["line_2_orientation"]
    ax.plot(
        [point[0] for point in line_2["coordinates"]],
        [point[1] for point in line_2["coordinates"]],
        color=PAPER,
        linewidth=6.0,
        solid_capstyle="round",
        zorder=3,
    )
    ax.plot(
        [point[0] for point in line_2["coordinates"]],
        [point[1] for point in line_2["coordinates"]],
        color=line_2["color"],
        linewidth=3.2,
        solid_capstyle="round",
        zorder=4,
    )
    ax.text(
        *line_2["label_position"],
        f"LINE {line_2['number']}",
        fontsize=7.6,
        fontweight="bold",
        color=line_2["color"],
        ha="center",
        va="center",
        zorder=7,
        bbox={
            "boxstyle": "round,pad=0.16,rounding_size=0.05",
            "facecolor": PAPER,
            "edgecolor": line_2["color"],
            "linewidth": 1.1,
        },
    )

    interchange = features["lines_3_4_anchor"]
    ax.scatter(
        [interchange["position"][0]],
        [interchange["position"][1]],
        s=250,
        facecolor=PAPER,
        edgecolor=JADE,
        linewidth=2.0,
        zorder=6,
    )
    ax.text(
        interchange["position"][0],
        interchange["position"][1] - 0.0055,
        f"METRO {interchange['numbers']}",
        fontsize=7.1,
        fontweight="bold",
        color=JADE,
        ha="center",
        va="top",
        zorder=7,
    )

    for zone, color in zip(config["zones"], ZONE_COLORS, strict=True):
        if zone["panel"] == "central":
            draw_zone(ax, zone, color, marker_scale=0.7)


def draw_card(
    fig: Any,
    card: dict[str, Any],
    color: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    fig.add_artist(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.006,rounding_size=0.007",
            transform=fig.transFigure,
            facecolor=PAPER,
            edgecolor=FAINT,
            linewidth=0.95,
            zorder=20,
        )
    )
    fig.add_artist(
        plt.Line2D(
            [x + 0.014, x + width - 0.014],
            [y + height - 0.012, y + height - 0.012],
            transform=fig.transFigure,
            color=color,
            linewidth=4.2,
            solid_capstyle="round",
            zorder=21,
        )
    )
    fig.text(
        x + 0.016,
        y + height - 0.029,
        f"{card['order']}  {card['title']}",
        fontsize=10.8,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + height - 0.066,
        card["zh"],
        fontsize=9.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + height - 0.103,
        card["ja"],
        fontsize=8.1,
        color=MUTED,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + 0.017,
        card["en"],
        fontsize=6.9,
        fontweight="bold",
        color=color,
        ha="left",
        va="bottom",
        zorder=22,
        linespacing=1.12,
    )


def draw_cards(fig: Any, config: dict[str, Any]) -> None:
    positions = [
        (0.055, 0.276, 0.282),
        (0.359, 0.276, 0.282),
        (0.663, 0.276, 0.282),
        (0.055, 0.086, 0.43),
        (0.515, 0.086, 0.43),
    ]
    for card, color, (x, y, width) in zip(
        config["cards"], ZONE_COLORS, positions, strict=True
    ):
        draw_card(fig, card, color, x, y, width, 0.17)


def render(config: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(8, 8.8), facecolor=PAPER)

    fig.text(
        0.055,
        0.967,
        config["title"]["zh"],
        fontsize=23.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
    )
    fig.text(
        0.055,
        0.925,
        config["title"]["ja"],
        fontsize=12.6,
        fontweight="bold",
        color=JADE,
        ha="left",
        va="top",
    )
    fig.text(
        0.055,
        0.892,
        config["title"]["en"],
        fontsize=9.9,
        fontweight="bold",
        color=BERRY,
        ha="left",
        va="top",
    )
    fig.text(
        0.945,
        0.858,
        "FIVE ITINERARY ANCHORS · NOT A HOTEL INVENTORY",
        fontsize=7.8,
        fontweight="bold",
        color=COBALT,
        ha="right",
        va="top",
    )

    regional_bounds = [0.055, 0.49, 0.43, 0.335]
    central_bounds = [0.515, 0.49, 0.43, 0.335]
    panel_frame(fig, regional_bounds, "CITY + LINTONG · 城市与临潼 · 市街と臨潼", BERRY)
    panel_frame(fig, central_bounds, "CENTRAL INSET · 城墙到雁塔 · 城壁から雁塔", JADE)
    regional_ax = fig.add_axes([0.074, 0.511, 0.392, 0.267], facecolor=PAPER)
    central_ax = fig.add_axes([0.534, 0.511, 0.392, 0.267], facecolor=PAPER)
    draw_regional_panel(regional_ax, config)
    draw_central_panel(central_ax, config)
    draw_cards(fig, config)

    fig.text(
        0.055,
        0.027,
        "区域只帮助选择行程落点；酒店入口、房型、价格与交通请在付款前及抵达前复核。",
        fontsize=7.3,
        color=MUTED,
        ha="left",
        va="bottom",
    )
    fig.text(
        0.945,
        0.027,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=6.8,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Stay Areas",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Five itinerary-led stay areas in Xi'an",
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
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        format="png",
        dpi=700,
        metadata={"Title": metadata["Title"], "Author": metadata["Author"]},
    )
    plt.close(fig)

    from PIL import Image

    with Image.open(OUTPUT_STEM.with_suffix(".png")) as image:
        dimensions = [image.width, image.height]
    return {
        "png_dimensions": dimensions,
        "minimum_png_width": 5000,
        "pdf_vector_output": True,
        "svg_selectable_text": True,
        "zone_count": len(config["zones"]),
        "panel_count": 2,
        "complete_network_claim": False,
        "hotel_inventory_count": 0,
        "live_route_count": 0,
    }


def write_provenance(config: dict[str, Any], technical: dict[str, Any]) -> None:
    files = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    generalizations = [
        {"id": key, "note": feature["note"]}
        for key, feature in config["schematic_features"].items()
    ]
    generalizations.extend(
        {"id": anchor["id"], "note": anchor["note"]}
        for anchor in config["regional_anchors"]
    )
    generalizations.extend(
        {"id": zone["id"], "note": zone["note"]} for zone in config["zones"]
    )
    write_json(
        OUTPUT_STEM.with_suffix(".provenance.json"),
        {
            "schema_version": 1,
            "asset_id": "asset-xian-stay-areas-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_stay_areas_map.py",
            "config": {
                "path": str(CONFIG_PATH.relative_to(ROOT)),
                "sha256": sha256(CONFIG_PATH),
            },
            "present_geography": [
                {
                    "kind": "pinned-place-positions",
                    "source": "OpenStreetMap and reviewed LazyTravel map configs",
                    "snapshot_date": config["snapshot_date"],
                }
            ],
            "sources": config["sources"],
            "declared_generalizations": generalizations,
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; pinned named-place positions "
                "© OpenStreetMap contributors, ODbL 1.0."
            ),
        },
    )


def main() -> int:
    config = read_json(CONFIG_PATH)
    technical = render(config)
    write_provenance(config, technical)
    print(f"rendered: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(
        f"dimensions: {technical['png_dimensions'][0]} x "
        f"{technical['png_dimensions'][1]} px"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
