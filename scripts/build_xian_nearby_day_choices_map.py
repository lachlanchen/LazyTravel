#!/usr/bin/env python3
"""Render Xi'an's five nearby day choices as a schematic regional map."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-nearby-day-choices.config.json"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-nearby-day-choices"
FIXED_TIME = datetime(2026, 8, 15, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#D9E2EC"
RIVER = "#1687C9"
MOUNTAIN_FILL = "#DDF5E8"
MOUNTAIN_EDGE = "#2C9C72"
COBALT = "#1769E0"
JADE = "#008C72"
CORAL = "#F05A47"
VERMILION = "#D93A32"
MAGENTA = "#B33273"
CHOICE_COLORS = [CORAL, VERMILION, COBALT, JADE, MAGENTA]


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
            "svg.hashsalt": "lazytravel-xian-nearby-day-choices-v1",
            "pdf.fonttype": 42,
        }
    )


def set_extent(ax: Any, extent: list[float]) -> None:
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")


def draw_regional_context(ax: Any, config: dict[str, Any]) -> None:
    features = config["schematic_features"]
    band = features["qinling_band"]
    ax.add_patch(
        Polygon(
            band["coordinates"],
            closed=True,
            facecolor=MOUNTAIN_FILL,
            edgecolor="none",
            zorder=0,
        )
    )
    ridge_x = [point[0] for point in band["coordinates"][6:]]
    ridge_y = [point[1] for point in band["coordinates"][6:]]
    ax.plot(
        ridge_x,
        ridge_y,
        color=MOUNTAIN_EDGE,
        linewidth=1.15,
        alpha=0.72,
        zorder=1,
    )
    ax.text(
        *band["label_position"],
        "秦岭  秦嶺  QINLING",
        fontsize=13.5,
        fontweight="bold",
        color=MOUNTAIN_EDGE,
        ha="center",
        va="center",
        rotation=8,
        zorder=2,
    )

    river = features["wei_river"]
    ax.plot(
        [point[0] for point in river["coordinates"]],
        [point[1] for point in river["coordinates"]],
        color=RIVER,
        linewidth=2.5,
        alpha=0.72,
        solid_capstyle="round",
        zorder=2,
    )
    ax.text(
        *river["label_position"],
        "渭河  渭水  WEI RIVER",
        fontsize=11.5,
        fontweight="bold",
        color=RIVER,
        ha="center",
        va="bottom",
        rotation=-2,
        zorder=3,
    )


def draw_origin_and_connectors(ax: Any, config: dict[str, Any]) -> None:
    origin = config["origin"]
    ox, oy = origin["position"]
    for choice, color in zip(config["choices"], CHOICE_COLORS, strict=True):
        cx, cy = choice["position"]
        ax.plot(
            [ox, cx],
            [oy, cy],
            color=color,
            linewidth=1.25,
            linestyle=(0, (4, 5)),
            alpha=0.56,
            zorder=3,
        )

    ax.scatter(
        [ox],
        [oy],
        s=220,
        facecolor=INK,
        edgecolor=PAPER,
        linewidth=2.2,
        zorder=8,
    )
    ax.scatter(
        [ox],
        [oy],
        s=32,
        facecolor=PAPER,
        edgecolor="none",
        zorder=9,
    )
    ax.text(
        ox - 0.035,
        oy - 0.035,
        "西安  XI'AN",
        fontsize=17.5,
        fontweight="bold",
        color=INK,
        ha="right",
        va="top",
        zorder=10,
        bbox={
            "boxstyle": "round,pad=0.18,rounding_size=0.08",
            "facecolor": PAPER,
            "edgecolor": "none",
            "alpha": 0.94,
        },
    )


def draw_choices(ax: Any, config: dict[str, Any]) -> None:
    for choice, color in zip(config["choices"], CHOICE_COLORS, strict=True):
        x, y = choice["position"]
        dx, dy = choice["label_offset"]
        label_x, label_y = x + dx, y + dy
        horizontal = "left" if dx >= 0 else "right"

        ax.scatter(
            [x],
            [y],
            s=340,
            facecolor=PAPER,
            edgecolor=color,
            linewidth=3.0,
            zorder=7,
        )
        ax.scatter(
            [x],
            [y],
            s=215,
            facecolor=color,
            edgecolor="none",
            zorder=8,
        )
        ax.text(
            x,
            y,
            str(choice["order"]),
            fontsize=14.0,
            fontweight="bold",
            color=PAPER,
            ha="center",
            va="center",
            zorder=9,
        )
        ax.plot(
            [x, label_x],
            [y, label_y],
            color=color,
            linewidth=1.2,
            zorder=6,
        )
        place_label = choice["label"]["zh"]
        if choice["label"]["ja"] != place_label:
            place_label = f"{place_label} / {choice['label']['ja']}"
        ax.text(
            label_x,
            label_y,
            place_label,
            fontsize=17.0,
            fontweight="bold",
            color=INK,
            ha=horizontal,
            va="bottom",
            zorder=10,
            bbox={
                "boxstyle": "round,pad=0.18,rounding_size=0.06",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.94,
            },
        )
        ax.text(
            label_x,
            label_y - 0.018,
            choice["label"]["en"],
            fontsize=11.5,
            fontweight="bold",
            color=color,
            ha=horizontal,
            va="top",
            zorder=10,
        )


def draw_card(
    fig: Any,
    choice: dict[str, Any],
    color: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    card = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.006,rounding_size=0.008",
        transform=fig.transFigure,
        facecolor=PAPER,
        edgecolor=FAINT,
        linewidth=0.9,
        zorder=20,
    )
    fig.add_artist(card)
    fig.add_artist(
        plt.Line2D(
            [x + 0.012, x + width - 0.012],
            [y + height - 0.010, y + height - 0.010],
            transform=fig.transFigure,
            color=color,
            linewidth=4.0,
            solid_capstyle="round",
            zorder=21,
        )
    )
    fig.text(
        x + 0.015,
        y + height - 0.028,
        f"{choice['order']}  {choice['label']['zh']} / {choice['label']['en']}",
        fontsize=12.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + height - 0.066,
        choice["transport"]["zh"],
        fontsize=9.2,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + height - 0.098,
        choice["transport"]["ja"],
        fontsize=8.5,
        color=MUTED,
        ha="left",
        va="bottom",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + 0.016,
        choice["transport"]["en"],
        fontsize=7.5,
        fontweight="bold",
        color=MUTED,
        ha="left",
        va="bottom",
        zorder=22,
    )


def draw_choice_cards(fig: Any, config: dict[str, Any]) -> None:
    width = 0.282
    height = 0.145
    top_y = 0.212
    bottom_y = 0.048
    positions = [
        (0.055, top_y),
        (0.359, top_y),
        (0.663, top_y),
        (0.207, bottom_y),
        (0.511, bottom_y),
    ]
    for choice, color, (x, y) in zip(
        config["choices"], CHOICE_COLORS, positions, strict=True
    ):
        draw_card(fig, choice, color, x, y, width, height)


def render(config: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(8, 7.2), facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.385, 0.89, 0.445], facecolor=PAPER)
    set_extent(ax, config["extent"])

    fig.text(
        0.055,
        0.953,
        config["title"]["zh"],
        fontsize=24.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
    )
    fig.text(
        0.055,
        0.902,
        config["title"]["ja"],
        fontsize=13.5,
        fontweight="bold",
        color=JADE,
        ha="left",
        va="top",
    )
    fig.text(
        0.945,
        0.918,
        config["title"]["en"],
        fontsize=10.8,
        fontweight="bold",
        color=VERMILION,
        ha="right",
        va="top",
    )
    fig.text(
        0.945,
        0.881,
        "DIRECTION ONLY · COUNT TRANSFERS BEFORE DISTANCE",
        fontsize=8.3,
        fontweight="bold",
        color=COBALT,
        ha="right",
        va="top",
    )

    draw_regional_context(ax, config)
    draw_origin_and_connectors(ax, config)
    draw_choices(ax, config)
    draw_choice_cards(fig, config)

    fig.text(
        0.055,
        0.018,
        "虚线只示方向，不是铁路、公路、时间或实时导航。",
        fontsize=7.7,
        color=MUTED,
        ha="left",
        va="bottom",
    )
    fig.text(
        0.945,
        0.018,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=7.1,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Nearby Day Choices",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Five one-day choices around Xi'an with schematic transport chains",
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
        "choice_count": len(config["choices"]),
        "connector_kind": "schematic-direction-only",
        "live_route_count": 0,
    }


def write_provenance(config: dict[str, Any], technical: dict[str, Any]) -> None:
    files = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    generalizations = [
        {"id": config["origin"]["id"], "note": config["origin"]["note"]},
        {"id": "direction-connectors", "note": config["connector_note"]},
        *[
            {"id": key, "note": feature["note"]}
            for key, feature in config["schematic_features"].items()
        ],
        *[
            {"id": choice["id"], "note": choice["note"]}
            for choice in config["choices"]
        ],
    ]
    write_json(
        OUTPUT_STEM.with_suffix(".provenance.json"),
        {
            "schema_version": 1,
            "asset_id": "asset-xian-nearby-day-choices-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_nearby_day_choices_map.py",
            "config": {
                "path": str(CONFIG_PATH.relative_to(ROOT)),
                "sha256": sha256(CONFIG_PATH),
            },
            "present_geography": [
                {
                    "kind": "pinned-place-positions",
                    "source": "OpenStreetMap",
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
    print(f"dimensions: {technical['png_dimensions'][0]} x {technical['png_dimensions'][1]} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
