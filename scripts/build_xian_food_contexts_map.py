#!/usr/bin/env python3
"""Render a clean four-context food map for central Xi'an."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-food-contexts.config.json"
WALL_GEOJSON_PATH = ROOT / "data/maps/xian/xian-before-walls.geojson"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-food-contexts"
FIXED_TIME = datetime(2026, 8, 15, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#CBD5E1"
PALE_BLUE = "#EAF2FF"
COBALT = "#1769E0"
JADE = "#008C72"
VERMILION = "#E24736"
CORAL = "#FF6B4A"

CONTEXT_COLORS = [COBALT, JADE, CORAL, VERMILION]


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
            "svg.hashsalt": "lazytravel-xian-food-contexts-v2",
            "pdf.fonttype": 42,
        }
    )


def wall_ring(wall_geojson: dict[str, Any]) -> list[list[float]]:
    for feature in wall_geojson["features"]:
        if feature["properties"].get("kind") != "wall":
            continue
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            return geometry["coordinates"][0]
    raise RuntimeError("present Xi'an wall polygon is missing")


def set_extent(ax: Any, extent: list[float]) -> None:
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")


def draw_wall(ax: Any, ring: list[list[float]]) -> None:
    ax.add_patch(
        Polygon(
            ring,
            closed=True,
            facecolor=PALE_BLUE,
            edgecolor=COBALT,
            linewidth=2.2,
            zorder=1,
        )
    )


def draw_guide_streets(ax: Any, config: dict[str, Any]) -> None:
    for street in config["guide_streets"]:
        points = street["coordinates"]
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]
        ax.plot(
            x_values,
            y_values,
            color=PAPER,
            linewidth=5.0,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=2,
        )
        ax.plot(
            x_values,
            y_values,
            color=FAINT,
            linewidth=1.2,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3,
        )


def draw_gates(ax: Any, config: dict[str, Any]) -> None:
    for gate in config["gates"]:
        x, y = gate["position"]
        ax.scatter(
            [x],
            [y],
            s=31,
            facecolor=PAPER,
            edgecolor=COBALT,
            linewidth=1.2,
            zorder=5,
        )

        dx, dy, horizontal, vertical = 0.0, 0.0, "center", "center"
        if gate["id"] == "west-gate":
            dx, horizontal = -0.0011, "right"
        elif gate["id"] == "east-gate":
            dx, horizontal = 0.0011, "left"
        elif gate["id"] == "north-gate":
            dy, vertical = 0.0011, "bottom"
        else:
            dy, vertical = -0.0012, "top"
        ax.text(
            x + dx,
            y + dy,
            gate["label"],
            fontsize=10.5,
            color=MUTED,
            ha=horizontal,
            va=vertical,
            zorder=6,
        )


def draw_reference(ax: Any, config: dict[str, Any]) -> None:
    reference = config["reference"]
    x, y = reference["position"]
    ax.scatter(
        [x],
        [y],
        s=72,
        facecolor=INK,
        edgecolor=PAPER,
        linewidth=1.5,
        zorder=8,
    )
    ax.text(
        x,
        y,
        "+",
        fontsize=12.0,
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=9,
    )
    ax.text(
        x + 0.0010,
        y - 0.0005,
        "钟楼  BELL TOWER",
        fontsize=11.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=9,
    )


def draw_contexts(ax: Any, config: dict[str, Any]) -> None:
    contexts = config["contexts"]
    if len(contexts) != len(CONTEXT_COLORS):
        raise RuntimeError("food map requires exactly four contexts")

    for context, color in zip(contexts, CONTEXT_COLORS, strict=True):
        x, y = context["position"]
        radius = context["radius"]
        dx, dy = context["label_offset"]
        ax.add_patch(
            Circle(
                (x, y),
                radius=radius,
                facecolor=color,
                edgecolor="none",
                alpha=0.14,
                zorder=4,
            )
        )
        ax.scatter(
            [x],
            [y],
            s=118,
            facecolor=color,
            edgecolor=PAPER,
            linewidth=1.8,
            zorder=8,
        )
        ax.text(
            x,
            y,
            str(context["order"]),
            fontsize=12.0,
            fontweight="bold",
            color=PAPER,
            ha="center",
            va="center",
            zorder=9,
        )

        label_x, label_y = x + dx, y + dy
        horizontal = "left" if dx >= 0 else "right"
        ax.plot(
            [x, label_x],
            [y, label_y],
            color=color,
            linewidth=0.9,
            zorder=6,
        )
        ax.text(
            label_x,
            label_y,
            context["label"]["zh"],
            fontsize=16.0,
            fontweight="bold",
            color=INK,
            ha=horizontal,
            va="bottom",
            zorder=9,
            bbox={
                "boxstyle": "square,pad=0.18",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.94,
            },
        )
        ax.text(
            label_x,
            label_y - 0.00035,
            context["label"]["en"],
            fontsize=11.5,
            fontweight="bold",
            color=color,
            ha=horizontal,
            va="top",
            zorder=9,
        )


def draw_context_key(fig: Any, config: dict[str, Any]) -> None:
    start_x = 0.055
    width = 0.215
    for index, (context, color) in enumerate(
        zip(config["contexts"], CONTEXT_COLORS, strict=True)
    ):
        x = start_x + index * 0.232
        fig.text(
            x,
            0.115,
            f"{context['order']}",
            fontsize=12.0,
            fontweight="bold",
            color=PAPER,
            ha="center",
            va="center",
            bbox={
                "boxstyle": "circle,pad=0.34",
                "facecolor": color,
                "edgecolor": "none",
            },
        )
        fig.text(
            x + 0.018,
            0.122,
            context["context"]["zh"],
            fontsize=13.2,
            fontweight="bold",
            color=INK,
            ha="left",
            va="center",
        )
        fig.text(
            x + 0.018,
            0.100,
            context["context"]["en"],
            fontsize=9.4,
            color=MUTED,
            ha="left",
            va="center",
        )
        fig.add_artist(
            plt.Line2D(
                [x - 0.008, x + width - 0.012],
                [0.079, 0.079],
                transform=fig.transFigure,
                color=FAINT,
                linewidth=0.6,
            )
        )


def render(config: dict[str, Any], wall_geojson: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(14, 9), facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.18, 0.89, 0.66], facecolor=PAPER)
    set_extent(ax, config["extent"])

    fig.text(
        0.055,
        0.948,
        config["title"]["zh"],
        fontsize=22,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.055, 0.906, config["title"]["ja"], fontsize=13, color=JADE)
    fig.text(
        0.945,
        0.925,
        config["title"]["en"],
        fontsize=11.5,
        fontweight="bold",
        color=VERMILION,
        ha="right",
    )
    fig.text(
        0.945,
        0.892,
        "CHOOSE A CONTEXT · CHECK THE DAY · LEAVE ROOM TO SIT",
        fontsize=9.0,
        fontweight="bold",
        color=COBALT,
        ha="right",
    )

    draw_wall(ax, wall_ring(wall_geojson))
    draw_guide_streets(ax, config)
    draw_gates(ax, config)
    draw_contexts(ax, config)
    draw_reference(ax, config)
    draw_context_key(fig, config)

    fig.text(
        0.055,
        0.035,
        "区域示意，不代表商户、营业时间、清真认证或实时路线。",
        fontsize=10.5,
        color=MUTED,
        va="bottom",
    )
    fig.text(
        0.50,
        0.035,
        "AREA LOGIC · NOT A RESTAURANT RANKING OR A FOUR-STOP FOOD CRAWL",
        fontsize=9.0,
        color=MUTED,
        ha="center",
        va="bottom",
    )
    fig.text(
        0.945,
        0.035,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=8.5,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Food Contexts",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Four eating contexts inside Xi'an's city wall",
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
        "context_count": len(config["contexts"]),
        "restaurant_pin_count": 0,
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
            "asset_id": "asset-xian-food-contexts-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_food_contexts_map.py",
            "config": {
                "path": str(CONFIG_PATH.relative_to(ROOT)),
                "sha256": sha256(CONFIG_PATH),
            },
            "present_geography": [
                {
                    "path": str(WALL_GEOJSON_PATH.relative_to(ROOT)),
                    "sha256": sha256(WALL_GEOJSON_PATH),
                }
            ],
            "sources": config["sources"],
            "declared_generalizations": [
                *[
                    {"id": street["id"], "note": street["note"]}
                    for street in config["guide_streets"]
                ],
                *[
                    {"id": context["id"], "note": context["note"]}
                    for context in config["contexts"]
                ],
            ],
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; present wall and named-place positions "
                "© OpenStreetMap contributors, ODbL 1.0."
            ),
        },
    )


def main() -> int:
    config = read_json(CONFIG_PATH)
    wall_geojson = read_json(WALL_GEOJSON_PATH)
    technical = render(config, wall_geojson)
    write_provenance(config, technical)
    print(f"rendered: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(f"dimensions: {technical['png_dimensions'][0]} x {technical['png_dimensions'][1]} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
