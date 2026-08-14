#!/usr/bin/env python3
"""Render the two-scale Qin mausoleum and warrior-pits schematic."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-qin-mausoleum-pits.config.json"
OUTPUT_STEM = ROOT / "assets/maps/xian/xian-qin-mausoleum-pits"
FIXED_TIME = datetime(2026, 8, 14, tzinfo=timezone.utc)

PAPER = "#F5F2EA"
INK = "#202522"
MUTED = "#5C625E"
GRID = "#C9C4B8"
TERRACOTTA = "#A8513E"
GOLD = "#B68A3A"
GREEN = "#56704F"


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
            "svg.hashsalt": "lazytravel-xian-qin-mausoleum-pits-v1",
            "pdf.fonttype": 42,
        }
    )


def panel_heading(fig: Any, x: float, number: str, zh: str, en: str) -> None:
    fig.text(x, 0.835, number, fontsize=9.5, fontweight="bold", color=TERRACOTTA)
    fig.text(x + 0.025, 0.835, zh, fontsize=12.5, fontweight="bold", color=INK)
    fig.text(x + 0.025, 0.806, en, fontsize=6.6, fontweight="bold", color=MUTED)


def draw_landscape_panel(ax: Any, config: dict[str, Any]) -> None:
    ax.set_xlim(-0.20, 1.72)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # A restrained foothill line gives directional context without implying a
    # surveyed topographic section.
    ax.fill_between(
        [-0.20, 0.05, 0.28, 0.50, 0.74, 0.98, 1.24, 1.48, 1.72],
        [0.12, 0.20, 0.14, 0.23, 0.13, 0.18, 0.12, 0.16, 0.11],
        0.02,
        color=GREEN,
        alpha=0.10,
        linewidth=0,
        zorder=0,
    )
    ax.text(-0.15, 0.06, "骊山北麓  LISHAN FOOTHILLS", fontsize=7.2, color=GREEN)

    mound_x, mound_y = config["landscape"]["mound_km"]
    sector_x, sector_y = config["landscape"]["warrior_sector_km"]
    ax.add_patch(
        Ellipse(
            (mound_x, mound_y),
            0.25,
            0.20,
            facecolor=GOLD,
            edgecolor=INK,
            linewidth=1.0,
            alpha=0.75,
            zorder=3,
        )
    )
    ax.plot([mound_x, mound_x], [0.58, 0.73], color=INK, linewidth=0.8)
    ax.text(
        mound_x,
        0.77,
        "陵墓封土\nBURIAL MOUND",
        ha="center",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
        color=INK,
    )
    ax.text(mound_x, 0.30, "丽山园\nLISHAN GARDEN", ha="center", fontsize=7.2, color=MUTED)

    for offset, width in ((0.00, 0.26), (0.07, 0.14), (-0.07, 0.08)):
        ax.add_patch(
            Rectangle(
                (sector_x - width / 2, sector_y + offset - 0.025),
                width,
                0.05,
                facecolor=TERRACOTTA,
                edgecolor=INK,
                linewidth=0.7,
                alpha=0.75,
                zorder=3,
            )
        )
    ax.plot([sector_x, sector_x], [0.58, 0.73], color=INK, linewidth=0.8)
    ax.text(
        sector_x,
        0.77,
        "兵马俑坑区域\nWARRIOR-PIT SECTOR",
        ha="center",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
        color=INK,
    )
    ax.text(
        sector_x,
        0.30,
        "兵马俑博物馆\nTERRACOTTA ARMY MUSEUM",
        ha="center",
        fontsize=7.2,
        color=MUTED,
    )

    ax.annotate(
        "",
        xy=(sector_x - 0.14, 0.49),
        xytext=(mound_x + 0.14, 0.49),
        arrowprops={"arrowstyle": "|-|", "color": INK, "lw": 1.0},
    )
    ax.text(
        (mound_x + sector_x) / 2,
        0.53,
        "约 1.5 km 向东  ·  ABOUT 1.5 KM EAST",
        ha="center",
        va="bottom",
        fontsize=7.6,
        color=INK,
    )
    ax.annotate(
        "E",
        xy=(1.70, 0.91),
        xytext=(1.54, 0.91),
        ha="right",
        va="center",
        fontsize=8.2,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 0.9, "color": INK},
    )
    ax.text(
        0.76,
        0.15,
        "俑坑不是墓室，也不是陵园的全部。\n"
        "THE WARRIOR PITS ARE NOT THE TOMB CHAMBER OR THE WHOLE COMPLEX.",
        ha="center",
        va="center",
        fontsize=7.4,
        fontweight="bold",
        color=TERRACOTTA,
        linespacing=1.35,
    )


def pit_two_polygon(pit: dict[str, Any]) -> list[tuple[float, float]]:
    x, y = pit["origin_m"]
    length = pit["length_m"]
    width = pit["width_m"]
    base_length = length * 0.80
    step_height = width * 0.36
    return [
        (x, y),
        (x + base_length, y),
        (x + base_length, y + step_height),
        (x + length, y + step_height),
        (x + length, y + width),
        (x, y + width),
    ]


def draw_detail_panel(ax: Any, config: dict[str, Any]) -> None:
    ax.set_xlim(-24, 252)
    ax.set_ylim(-25, 197)
    ax.set_aspect("equal")
    ax.axis("off")

    pits = {pit["id"]: pit for pit in config["pits"]}
    pit1 = pits["pit-1"]
    x1, y1 = pit1["origin_m"]
    ax.add_patch(
        Rectangle(
            (x1, y1),
            pit1["length_m"],
            pit1["width_m"],
            facecolor=pit1["color"],
            edgecolor=INK,
            linewidth=1.2,
            alpha=0.72,
            zorder=2,
        )
    )
    for corridor in range(1, 6):
        y = y1 + pit1["width_m"] * corridor / 6
        ax.plot(
            [x1 + 6, x1 + pit1["length_m"] - 6],
            [y, y],
            color=PAPER,
            linewidth=0.75,
            alpha=0.75,
        )
    ax.text(
        x1 + pit1["length_m"] / 2,
        y1 + pit1["width_m"] / 2,
        pit1["label"] + "\n230 × 62 m",
        ha="center",
        va="center",
        fontsize=10.5,
        fontweight="bold",
        color=PAPER,
    )

    pit2 = pits["pit-2"]
    polygon = pit_two_polygon(pit2)
    ax.add_patch(
        Polygon(
            polygon,
            closed=True,
            facecolor=pit2["color"],
            edgecolor=INK,
            linewidth=1.2,
            alpha=0.72,
            zorder=2,
        )
    )
    x2, y2 = pit2["origin_m"]
    ax.text(
        x2 + 49,
        y2 + 55,
        pit2["label"] + "\n124 × 98 m",
        ha="center",
        va="center",
        fontsize=9.3,
        fontweight="bold",
        color=PAPER,
    )

    pit3 = pits["pit-3"]
    x3, y3 = pit3["origin_m"]
    ax.add_patch(
        Rectangle(
            (x3, y3),
            pit3["length_m"],
            pit3["width_m"],
            facecolor=pit3["color"],
            edgecolor=INK,
            linewidth=1.1,
            alpha=0.78,
            zorder=2,
        )
    )
    ax.add_patch(
        Rectangle(
            (x3 + pit3["length_m"] * 0.46, y3 + pit3["width_m"] * 0.30),
            pit3["length_m"] * 0.54,
            pit3["width_m"] * 0.40,
            facecolor=PAPER,
            edgecolor="none",
            zorder=3,
        )
    )
    ax.annotate(
        pit3["label"] + "  28.8 × 24.57 m",
        xy=(x3 + 13, y3 + 12),
        xytext=(x3 + 34, y3 + 21),
        fontsize=7.5,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.8},
    )

    ax.annotate(
        "E",
        xy=(246, 185),
        xytext=(224, 185),
        ha="right",
        va="center",
        fontsize=8.2,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 0.9, "color": INK},
    )
    ax.annotate(
        "N",
        xy=(242, 178),
        xytext=(242, 154),
        ha="center",
        va="bottom",
        fontsize=8.2,
        fontweight="bold",
        color=INK,
        arrowprops={"arrowstyle": "-|>", "lw": 0.9, "color": INK},
    )

    sx, sy = 0, -13
    ax.plot([sx, sx + 50], [sy, sy], color=INK, linewidth=1.0)
    ax.plot([sx, sx], [sy - 2, sy + 2], color=INK, linewidth=0.9)
    ax.plot([sx + 50, sx + 50], [sy - 2, sy + 2], color=INK, linewidth=0.9)
    ax.text(sx + 25, sy + 5, "50 m", fontsize=7.5, ha="center", color=INK)
    ax.text(
        250,
        -15,
        "俑坑尺寸同一比例 · 坑间位置为概化\n"
        "PIT DIMENSIONS TO COMMON SCALE · PLACEMENT SCHEMATIC",
        fontsize=6.2,
        color=MUTED,
        ha="right",
        va="bottom",
        linespacing=1.3,
    )


def render(config: dict[str, Any]) -> dict[str, Any]:
    configure_fonts()
    fig = plt.figure(figsize=(14, 9), facecolor=PAPER)

    fig.text(0.055, 0.948, config["title"]["zh"], fontsize=22, fontweight="bold", color=INK)
    fig.text(0.055, 0.907, config["title"]["ja"], fontsize=11, color=GREEN)
    fig.text(
        0.945,
        0.925,
        config["title"]["en"],
        fontsize=9.6,
        fontweight="bold",
        color=TERRACOTTA,
        ha="right",
    )
    fig.text(
        0.945,
        0.896,
        "SCHEMATIC ORIENTATION · NOT FOR SITE NAVIGATION",
        fontsize=6.4,
        color=MUTED,
        ha="right",
    )

    panel_heading(fig, 0.055, "01", "陵园尺度", "MAUSOLEUM LANDSCAPE")
    panel_heading(fig, 0.535, "02", "俑坑尺度", "THREE PRINCIPAL WARRIOR PITS")

    landscape_ax = fig.add_axes([0.055, 0.135, 0.415, 0.64], facecolor=PAPER)
    detail_ax = fig.add_axes([0.535, 0.135, 0.410, 0.64], facecolor=PAPER)
    draw_landscape_panel(landscape_ax, config)
    draw_detail_panel(detail_ax, config)

    fig.add_artist(
        plt.Line2D(
            [0.502, 0.502],
            [0.14, 0.84],
            transform=fig.transFigure,
            color=GRID,
            linewidth=0.7,
        )
    )
    fig.text(
        0.055,
        0.050,
        "原创建筑关系示意，不是考古测绘图 / 独自作成の模式図・考古測量図ではない\n"
        "ORIGINAL SCHEMATIC · NO SOURCE FIGURE COPIED · NOT AN EXCAVATION SURVEY",
        fontsize=6.0,
        color=MUTED,
        linespacing=1.3,
    )
    fig.text(
        0.945,
        0.050,
        "LazyTravel · lazying.art\nSources: Qinshihuang Mausoleum Site Museum · UNESCO",
        fontsize=5.9,
        color=MUTED,
        ha="right",
        linespacing=1.3,
    )

    OUTPUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "One Mausoleum Landscape, Two Scales",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Schematic relationship of the Qin mausoleum mound and principal warrior pits",
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
            "asset_id": "asset-xian-qin-mausoleum-pits-map",
            "created_at": config["snapshot_date"],
            "method": "map-render",
            "command": "python3 scripts/build_xian_qin_mausoleum_pits_map.py",
            "config": {"path": str(CONFIG_PATH.relative_to(ROOT)), "sha256": sha256(CONFIG_PATH)},
            "declared_generalizations": [
                {"id": "landscape", "note": config["landscape"]["note"]},
                *[{"id": pit["id"], "note": pit["note"]} for pit in config["pits"]],
            ],
            "sources": config["sources"],
            "files": files,
            "technical_qa": technical,
            "visual_qa": config["visual_qa"],
            "rights": (
                "Map design © LazyTravel; original schematic synthesis from cited "
                "institutional records."
            ),
        },
    )


def main() -> None:
    config = read_json(CONFIG_PATH)
    technical = render(config)
    write_provenance(config, technical)
    print(json.dumps({"status": "ok", "output": str(OUTPUT_STEM), **technical}, indent=2))


if __name__ == "__main__":
    main()
