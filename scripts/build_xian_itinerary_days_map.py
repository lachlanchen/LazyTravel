#!/usr/bin/env python3
"""Render Xi'an's nested two-, three-, and five-day itinerary map."""

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
CONFIG_PATH = ROOT / "data/maps/xian/xian-itinerary-days.config.json"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-itinerary-days"
FIXED_TIME = datetime(2026, 8, 16, tzinfo=timezone.utc)

PAPER = "#FCFDFF"
INK = "#17212B"
MUTED = "#52606D"
FAINT = "#D9E2EC"
GRID = "#E9EFF5"
CORAL = "#F05A47"
BERRY = "#B33273"
COBALT = "#1769E0"
JADE = "#008C72"
SAFFRON = "#E3A008"
DAY_COLORS = [CORAL, BERRY, COBALT, SAFFRON, JADE]


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
            "svg.hashsalt": "lazytravel-xian-itinerary-days-v1",
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
            boxstyle="round,pad=0.007,rounding_size=0.008",
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
        fontsize=12.5,
        fontweight="bold",
        color=accent,
        ha="left",
        va="top",
    )


def day_badge(ax: Any, x: float, y: float, day: int, color: str, size: int = 410) -> None:
    ax.scatter(
        [x],
        [y],
        s=size,
        facecolor=PAPER,
        edgecolor=color,
        linewidth=3.0,
        zorder=12,
    )
    ax.scatter(
        [x],
        [y],
        s=size * 0.66,
        facecolor=color,
        edgecolor="none",
        zorder=13,
    )
    ax.text(
        x,
        y,
        f"D{day}",
        fontsize=11.5,
        fontweight="bold",
        color=PAPER,
        ha="center",
        va="center",
        zorder=14,
    )


def label_box(
    ax: Any,
    x: float,
    y: float,
    primary: str,
    secondary: str,
    color: str,
    *,
    ha: str = "left",
) -> None:
    ax.text(
        x,
        y,
        primary,
        fontsize=13.0,
        fontweight="bold",
        color=INK,
        ha=ha,
        va="bottom",
        zorder=20,
        bbox={
            "boxstyle": "round,pad=0.18,rounding_size=0.06",
            "facecolor": PAPER,
            "edgecolor": "none",
            "alpha": 0.95,
        },
    )
    ax.text(
        x,
        y - 0.002,
        secondary,
        fontsize=8.2,
        fontweight="bold",
        color=color,
        ha=ha,
        va="top",
        zorder=21,
    )


def draw_urban_panel(ax: Any, config: dict[str, Any]) -> None:
    set_extent(ax, config["urban_extent"])
    context = config["urban_context"]
    wall = context["walled_core"]["bounds"]
    ax.add_patch(
        Rectangle(
            (wall[0], wall[1]),
            wall[2] - wall[0],
            wall[3] - wall[1],
            facecolor="#FFF0EC",
            edgecolor=CORAL,
            linewidth=2.1,
            zorder=2,
        )
    )
    day_1 = context["day_1"]
    d1_x = [site["position"][0] for site in day_1["sites"]]
    d1_y = [site["position"][1] for site in day_1["sites"]]
    ax.plot(d1_x, d1_y, color=CORAL, linewidth=4.5, alpha=0.38, zorder=4)
    ax.scatter(d1_x, d1_y, s=55, facecolor=CORAL, edgecolor=PAPER, linewidth=1.2, zorder=5)
    day_badge(ax, 108.9418, 34.2665, 1, CORAL, size=260)
    ax.text(
        108.919,
        34.285,
        "D1  城墙内 / 城壁内 / OLD CORE",
        fontsize=10.8,
        fontweight="bold",
        color=CORAL,
        ha="left",
        va="center",
        zorder=20,
    )

    day_3 = context["day_3"]
    d3_x = [site["position"][0] for site in day_3["sites"]]
    d3_y = [site["position"][1] for site in day_3["sites"]]
    ax.plot(d3_x, d3_y, color=COBALT, linewidth=4.5, alpha=0.42, zorder=4)
    ax.scatter(d3_x, d3_y, s=65, facecolor=COBALT, edgecolor=PAPER, linewidth=1.2, zorder=5)
    day_badge(ax, d3_x[0] - 0.006, d3_y[0] + 0.006, 3, COBALT, size=260)
    ax.text(
        108.983,
        34.211,
        "D3  博物馆 → 大雁塔 / MUSEUM → PAGODA",
        fontsize=9.4,
        fontweight="bold",
        color=COBALT,
        ha="right",
        va="bottom",
        zorder=20,
    )

    fallback = day_3["fallback"]
    fx, fy = fallback["position"]
    ax.scatter(
        [fx],
        [fy],
        s=150,
        facecolor=PAPER,
        edgecolor=COBALT,
        linewidth=2.3,
        linestyle=(0, (2, 1)),
        zorder=9,
    )
    ax.text(
        108.919,
        fy + 0.004,
        "预约替代 / FALLBACK\n小雁塔 + 西安博物院",
        fontsize=8.4,
        fontweight="bold",
        color=COBALT,
        ha="left",
        va="bottom",
        zorder=10,
    )

    day_5 = context["day_5"]
    x5, y5 = day_5["position"]
    day_badge(ax, x5, y5, 5, JADE, size=260)
    ax.text(
        108.982,
        34.309,
        "D5  大明宫或补回一处 / DEPTH OR RETURN",
        fontsize=9.6,
        fontweight="bold",
        color=JADE,
        ha="right",
        va="bottom",
        zorder=20,
    )


def draw_regional_panel(ax: Any, config: dict[str, Any]) -> None:
    set_extent(ax, config["regional_extent"])
    regional = config["regional_days"]
    city_x, city_y = regional["city_base"]["position"]
    day_2 = regional["day_2"]
    d2_x, d2_y = day_2["position"]

    for choice in regional["day_4_choices"]:
        choice_x, choice_y = choice["position"]
        ax.plot(
            [city_x, choice_x],
            [city_y, choice_y],
            color=SAFFRON,
            linewidth=1.6,
            linestyle=(0, (3, 5)),
            alpha=0.48,
            zorder=1,
        )

    ax.plot(
        [city_x, d2_x],
        [city_y, d2_y],
        color=BERRY,
        linewidth=3.2,
        alpha=0.48,
        zorder=2,
    )
    ax.scatter([city_x], [city_y], s=190, facecolor=INK, edgecolor=PAPER, linewidth=2, zorder=8)
    ax.text(
        city_x - 0.055,
        city_y - 0.035,
        regional["city_base"]["label"],
        fontsize=12.5,
        fontweight="bold",
        color=INK,
        ha="right",
        va="top",
        zorder=9,
    )

    day_badge(ax, d2_x, d2_y, 2, BERRY, size=470)
    ax.text(
        d2_x + 0.07,
        d2_y - 0.04,
        "秦陵 / QIN MUSEUM",
        fontsize=10.5,
        fontweight="bold",
        color=BERRY,
        ha="left",
        va="center",
        zorder=20,
    )

    label_positions = {
        "huashan": (110.12, 34.515, "right"),
        "hanyangling": (108.72, 34.545, "left"),
        "cuihuashan": (109.06, 33.94, "left"),
        "qianling": (108.12, 34.50, "left"),
    }
    for choice in regional["day_4_choices"]:
        x, y = choice["position"]
        label_x, label_y, align = label_positions[choice["id"]]
        ax.scatter(
            [x],
            [y],
            s=230,
            facecolor=PAPER,
            edgecolor=SAFFRON,
            linewidth=2.6,
            zorder=7,
        )
        ax.scatter([x], [y], s=105, facecolor=SAFFRON, edgecolor="none", zorder=8)
        ax.text(
            label_x,
            label_y,
            choice["label"],
            fontsize=9.3,
            fontweight="bold",
            color=INK,
            ha=align,
            va="center",
            zorder=10,
            bbox={
                "boxstyle": "round,pad=0.15,rounding_size=0.05",
                "facecolor": PAPER,
                "edgecolor": "none",
                "alpha": 0.94,
            },
        )

    ax.text(
        0.5,
        0.98,
        "D4  四选一 / 一か所 / CHOOSE ONE",
        transform=ax.transAxes,
        fontsize=10.5,
        fontweight="bold",
        color=SAFFRON,
        ha="center",
        va="top",
        bbox={
            "boxstyle": "round,pad=0.22,rounding_size=0.08",
            "facecolor": PAPER,
            "edgecolor": "none",
            "alpha": 0.95,
        },
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
    fig.add_artist(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.006,rounding_size=0.007",
            transform=fig.transFigure,
            facecolor=PAPER,
            edgecolor=FAINT,
            linewidth=1.0,
            zorder=20,
        )
    )
    fig.add_artist(
        plt.Line2D(
            [x + 0.012, x + width - 0.012],
            [y + height - 0.012, y + height - 0.012],
            transform=fig.transFigure,
            color=color,
            linewidth=4.4,
            solid_capstyle="round",
            zorder=21,
        )
    )
    fig.text(
        x + 0.015,
        y + height - 0.029,
        card["title"],
        fontsize=12.6,
        fontweight="bold",
        color=color,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + height - 0.061,
        card["zh"],
        fontsize=9.8,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + height - 0.091,
        card["ja"],
        fontsize=8.9,
        color=MUTED,
        ha="left",
        va="top",
        zorder=22,
    )
    fig.text(
        x + 0.015,
        y + 0.015,
        card["en"],
        fontsize=7.7,
        fontweight="bold",
        color=color,
        ha="left",
        va="bottom",
        zorder=22,
        linespacing=1.08,
    )


def draw_cards(fig: Any, config: dict[str, Any]) -> None:
    positions = [
        (0.045, 0.235, 0.29),
        (0.355, 0.235, 0.29),
        (0.665, 0.235, 0.29),
        (0.12, 0.035, 0.36),
        (0.52, 0.035, 0.36),
    ]
    for card, color, (x, y, width) in zip(
        config["day_cards"], DAY_COLORS, positions, strict=True
    ):
        draw_card(fig, card, color, x, y, width, 0.17)


def render(config: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(10, 7.2), facecolor=PAPER)
    fig.text(
        0.045,
        0.965,
        config["title"]["zh"],
        fontsize=24.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
    )
    fig.text(
        0.045,
        0.918,
        config["title"]["ja"],
        fontsize=13.5,
        fontweight="bold",
        color=JADE,
        ha="left",
        va="top",
    )
    fig.text(
        0.955,
        0.918,
        config["title"]["en"],
        fontsize=10.5,
        fontweight="bold",
        color=BERRY,
        ha="right",
        va="top",
    )

    fig.add_artist(
        FancyBboxPatch(
            (0.045, 0.84),
            0.91,
            0.055,
            boxstyle="round,pad=0.005,rounding_size=0.012",
            transform=fig.transFigure,
            facecolor="#EEF5FF",
            edgecolor="#C9DCF8",
            linewidth=1.0,
            zorder=1,
        )
    )
    fig.text(
        0.5,
        0.868,
        config["nested_rule"]["zh"],
        fontsize=13.2,
        fontweight="bold",
        color=COBALT,
        ha="center",
        va="center",
        zorder=2,
    )
    fig.text(
        0.5,
        0.846,
        config["nested_rule"]["en"],
        fontsize=8.0,
        fontweight="bold",
        color=MUTED,
        ha="center",
        va="center",
        zorder=2,
    )

    urban_bounds = [0.045, 0.405, 0.44, 0.405]
    regional_bounds = [0.515, 0.405, 0.44, 0.405]
    panel_frame(fig, urban_bounds, "CITY DAYS · 城市日 · 市内の日", COBALT)
    panel_frame(fig, regional_bounds, "OUTSIDE THE CORE · 城外 · 市外", BERRY)
    urban_ax = fig.add_axes([0.064, 0.432, 0.402, 0.315], facecolor=PAPER)
    regional_ax = fig.add_axes([0.534, 0.432, 0.402, 0.315], facecolor=PAPER)
    draw_urban_panel(urban_ax, config)
    draw_regional_panel(regional_ax, config)
    draw_cards(fig, config)

    fig.text(
        0.045,
        0.008,
        "每一天只保留一条地理主线；预约、开放、天气、入口与交通在出发前再核。",
        fontsize=7.8,
        color=MUTED,
        ha="left",
        va="bottom",
    )
    fig.text(
        0.955,
        0.008,
        "© LazyTravel · MAP DATA © OPENSTREETMAP CONTRIBUTORS",
        fontsize=7.5,
        color=MUTED,
        ha="right",
        va="bottom",
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Nested Itinerary Days",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Nested two-, three-, and five-day Xi'an itinerary map",
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
        "minimum_png_width": 6000,
        "pdf_vector_output": True,
        "svg_selectable_text": True,
        "day_card_count": len(config["day_cards"]),
        "day_4_choice_count": len(config["regional_days"]["day_4_choices"]),
        "panel_count": 2,
        "complete_network_claim": False,
        "live_route_count": 0,
        "journey_time_count": 0,
    }


def write_provenance(config: dict[str, Any], technical: dict[str, Any]) -> None:
    files = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    generalizations = [
        {"id": "walled-core", "note": config["urban_context"]["walled_core"]["note"]},
        {"id": "day-1-sequence", "note": config["urban_context"]["day_1"]["note"]},
        {"id": "day-3-sequence", "note": config["urban_context"]["day_3"]["note"]},
        {"id": "day-5-example", "note": config["urban_context"]["day_5"]["note"]},
        {"id": "day-2-position", "note": config["regional_days"]["day_2"]["note"]},
    ]
    generalizations.extend(
        {"id": choice["id"], "note": choice["note"]}
        for choice in config["regional_days"]["day_4_choices"]
    )
    write_json(
        OUTPUT_STEM.with_suffix(".provenance.json"),
        {
            "schema_version": 1,
            "asset_id": "asset-xian-itinerary-days-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_itinerary_days_map.py",
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
