#!/usr/bin/env python3
"""Render Xi'an's four arrival hubs and first-transfer decision spines."""

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
CONFIG_PATH = ROOT / "data/maps/xian/xian-arrival-hubs.config.json"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-arrival-hubs"
FIXED_TIME = datetime(2026, 8, 16, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#D9E2EC"
RIVER = "#1687C9"
CORE_FILL = "#FFF0EC"
CORE_EDGE = "#F05A47"
JADE = "#008C72"
COBALT = "#1769E0"
VERMILION = "#D93A32"
CORAL = "#F05A47"
HUB_COLORS = [CORAL, COBALT, VERMILION, JADE]


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
            "svg.hashsalt": "lazytravel-xian-arrival-hubs-v1",
            "pdf.fonttype": 42,
        }
    )


def set_extent(ax: Any, extent: list[float]) -> None:
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")


def draw_context(ax: Any, config: dict[str, Any]) -> None:
    features = config["schematic_features"]
    river = features["wei_river"]
    ax.plot(
        [point[0] for point in river["coordinates"]],
        [point[1] for point in river["coordinates"]],
        color=RIVER,
        linewidth=2.4,
        alpha=0.68,
        solid_capstyle="round",
        zorder=1,
    )
    ax.text(
        *river["label_position"],
        "渭河  渭水  WEI RIVER",
        fontsize=10.2,
        fontweight="bold",
        color=RIVER,
        ha="center",
        va="bottom",
        zorder=2,
    )

    bounds = features["walled_core"]["bounds"]
    ax.add_patch(
        Rectangle(
            (bounds[0], bounds[1]),
            bounds[2] - bounds[0],
            bounds[3] - bounds[1],
            facecolor=CORE_FILL,
            edgecolor=CORE_EDGE,
            linewidth=2.0,
            zorder=2,
        )
    )
    anchor = config["core_anchor"]
    ax.scatter(
        [anchor["position"][0]],
        [anchor["position"][1]],
        s=74,
        facecolor=CORE_EDGE,
        edgecolor=PAPER,
        linewidth=1.5,
        zorder=5,
    )
    ax.text(
        *features["walled_core"]["label_position"],
        "城墙 / 城壁 / WALL",
        fontsize=7.4,
        fontweight="bold",
        color=CORE_EDGE,
        ha="left",
        va="bottom",
        zorder=6,
    )


def draw_spines(ax: Any, config: dict[str, Any]) -> None:
    for spine in config["spines"]:
        x_values = [point[0] for point in spine["coordinates"]]
        y_values = [point[1] for point in spine["coordinates"]]
        ax.plot(
            x_values,
            y_values,
            color=PAPER,
            linewidth=6.5,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3,
        )
        ax.plot(
            x_values,
            y_values,
            color=spine["color"],
            linewidth=3.8,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=4,
        )
        label_x, label_y = spine["label_position"]
        ax.scatter(
            [label_x],
            [label_y],
            s=270,
            facecolor=spine["color"],
            edgecolor=PAPER,
            linewidth=2.0,
            zorder=7,
        )
        ax.text(
            label_x,
            label_y,
            spine["number"],
            fontsize=11.0,
            fontweight="bold",
            color=PAPER,
            ha="center",
            va="center",
            zorder=8,
        )


def draw_hubs(ax: Any, config: dict[str, Any]) -> None:
    for hub, color in zip(config["hubs"], HUB_COLORS, strict=True):
        x, y = hub["position"]
        dx, dy = hub["label_offset"]
        label_x, label_y = x + dx, y + dy
        align = "left" if dx >= 0 else "right"

        ax.scatter(
            [x],
            [y],
            s=440,
            facecolor=PAPER,
            edgecolor=color,
            linewidth=3.0,
            zorder=9,
        )
        ax.scatter(
            [x],
            [y],
            s=285,
            facecolor=color,
            edgecolor="none",
            zorder=10,
        )
        ax.text(
            x,
            y,
            str(hub["order"]),
            fontsize=14.0,
            fontweight="bold",
            color=PAPER,
            ha="center",
            va="center",
            zorder=11,
        )
        ax.plot(
            [x, label_x],
            [y, label_y],
            color=color,
            linewidth=1.25,
            zorder=8,
        )
        ax.text(
            label_x,
            label_y,
            hub["label"]["zh"],
            fontsize=14.5,
            fontweight="bold",
            color=INK,
            ha=align,
            va="bottom",
            zorder=12,
            bbox={
                "boxstyle": "round,pad=0.16,rounding_size=0.05",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.95,
            },
        )
        ax.text(
            label_x,
            label_y - 0.013,
            hub["label"]["en"],
            fontsize=9.1,
            fontweight="bold",
            color=color,
            ha=align,
            va="top",
            zorder=12,
        )


def draw_card(
    fig: Any,
    card: dict[str, Any],
    color: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    panel = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.006,rounding_size=0.007",
        transform=fig.transFigure,
        facecolor=PAPER,
        edgecolor=FAINT,
        linewidth=0.9,
        zorder=20,
    )
    fig.add_artist(panel)
    fig.add_artist(
        plt.Line2D(
            [x + 0.014, x + width - 0.014],
            [y + height - 0.012, y + height - 0.012],
            transform=fig.transFigure,
            color=color,
            linewidth=4.0,
            solid_capstyle="round",
            zorder=21,
        )
    )
    fig.text(
        x + 0.016,
        y + height - 0.026,
        f"{card['order']}  {card['title']}",
        fontsize=10.7,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + height - 0.057,
        card["zh"],
        fontsize=8.1,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + height - 0.088,
        card["ja"],
        fontsize=7.4,
        color=MUTED,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.016,
        y + 0.015,
        card["en"],
        fontsize=6.9,
        fontweight="bold",
        color=color,
        ha="left",
        va="bottom",
        zorder=22,
    )


def draw_cards(fig: Any, config: dict[str, Any]) -> None:
    positions = [
        (0.055, 0.188),
        (0.515, 0.188),
        (0.055, 0.038),
        (0.515, 0.038),
    ]
    for card, color, (x, y) in zip(
        config["cards"], HUB_COLORS, positions, strict=True
    ):
        draw_card(fig, card, color, x, y, 0.43, 0.136)


def render(config: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(8, 7.2), facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.335, 0.89, 0.515], facecolor=PAPER)
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
        fontsize=13.0,
        fontweight="bold",
        color=JADE,
        ha="left",
        va="top",
    )
    fig.text(
        0.945,
        0.918,
        config["title"]["en"],
        fontsize=10.4,
        fontweight="bold",
        color=VERMILION,
        ha="right",
        va="top",
    )
    fig.text(
        0.945,
        0.881,
        "DECISION SPINES · NOT A COMPLETE METRO MAP",
        fontsize=8.2,
        fontweight="bold",
        color=COBALT,
        ha="right",
        va="top",
    )

    draw_context(ax, config)
    draw_spines(ax, config)
    draw_hubs(ax, config)
    draw_cards(fig, config)

    fig.text(
        0.055,
        0.015,
        "线条只帮助选择第一次换乘；请以当日官方线网、航班车次与现场标识为准。",
        fontsize=7.1,
        color=MUTED,
        ha="left",
        va="bottom",
    )
    fig.text(
        0.945,
        0.015,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=6.8,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Arrival Hubs",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Four arrival hubs and first-transfer decision spines",
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
        "hub_count": len(config["hubs"]),
        "spine_count": len(config["spines"]),
        "complete_network_claim": False,
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
    generalizations.append(
        {"id": config["core_anchor"]["id"], "note": config["core_anchor"]["note"]}
    )
    generalizations.extend(
        {"id": hub["id"], "note": hub["note"]} for hub in config["hubs"]
    )
    generalizations.extend(
        {"id": spine["id"], "note": spine["note"]} for spine in config["spines"]
    )
    write_json(
        OUTPUT_STEM.with_suffix(".provenance.json"),
        {
            "schema_version": 1,
            "asset_id": "asset-xian-arrival-hubs-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_arrival_hubs_map.py",
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
