#!/usr/bin/env python3
"""Build Hakone Chapter 4's Owakudani route and stop-choice diagram."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-owakudani-decision.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-owakudani-decision"
FIXED_TIME = datetime(2026, 8, 17, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def render(config: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-hakone-owakudani-decision-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

    colors = {
        "ink": "#142330",
        "muted": "#526574",
        "paper": "#FBFDFF",
        "panel": "#F2F8FB",
        "line": "#1769E0",
        "vermilion": "#F05D36",
        "jade": "#008E87",
        "cobalt": "#1769E0",
        "coral": "#E53D63",
        "amber": "#FFB000",
        "danger": "#B8243F",
    }

    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.035, right=0.975, top=0.81, bottom=0.11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.04, 0.958, config["title"]["zh"], fontsize=13.2, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.915, config["title"]["ja"], fontsize=9.3, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.878, config["title"]["en"], fontsize=8.2, fontweight="bold", color=colors["cobalt"])
    fig.text(
        0.96,
        0.953,
        "计划图・計画図\nPLANNING DIAGRAM",
        fontsize=6.1,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    ax.add_patch(
        FancyBboxPatch(
            (0.015, 0.60),
            0.97,
            0.35,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor=colors["panel"],
            edgecolor="#CADAE5",
            linewidth=1.0,
        )
    )

    station_x = [0.085, 0.37, 0.66, 0.91]
    station_y = 0.755
    line_start = station_x[0]
    line_end = station_x[-1]
    ax.plot([line_start, line_end], [station_y, station_y], color="#FFFFFF", lw=10, solid_capstyle="round", zorder=1)
    ax.plot([line_start, line_end], [station_y, station_y], color=colors["line"], lw=5, solid_capstyle="round", zorder=2)

    for index in range(len(station_x) - 1):
        midpoint = (station_x[index] + station_x[index + 1]) / 2
        ax.text(
            midpoint,
            station_y + 0.038,
            f"约{config['segment_minutes_approx']}分 / 約{config['segment_minutes_approx']}分 / ~{config['segment_minutes_approx']} MIN",
            fontsize=5.5,
            color=colors["line"],
            fontweight="bold",
            ha="center",
            va="bottom",
        )

    node_colors = [colors["amber"], colors["vermilion"], colors["jade"], colors["cobalt"]]
    for station, x_value, node_color in zip(config["stations"], station_x, node_colors, strict=True):
        radius = 0.025 if station["id"] == "owakudani" else 0.019
        ax.add_patch(
            Circle(
                (x_value, station_y),
                radius,
                facecolor="#FFFFFF",
                edgecolor=node_color,
                linewidth=3 if station["id"] == "owakudani" else 2,
                zorder=4,
            )
        )
        ax.text(
            x_value,
            station_y - 0.055,
            f"{station['zh']}  {station['zh_reading']}\n"
            f"{station['ja']}  {station['ja_reading']}\n{station['en']}",
            fontsize=6.15,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="top",
            linespacing=1.12,
        )
        ax.text(
            x_value,
            station_y - 0.18,
            station["role"],
            fontsize=5.25,
            color=node_color,
            fontweight="bold",
            ha="center",
            va="top",
        )

    ax.text(
        station_x[1],
        0.918,
        "必须下车换舱\n必ず降りて乗り換え\nEXIT + CHANGE CABIN",
        fontsize=6.15,
        color="#FFFFFF",
        fontweight="bold",
        ha="center",
        va="center",
        linespacing=1.08,
        bbox={
            "boxstyle": "round,pad=0.42,rounding_size=0.9",
            "facecolor": colors["vermilion"],
            "edgecolor": colors["vermilion"],
            "linewidth": 0.8,
        },
        zorder=6,
    )
    ax.add_patch(
        FancyArrowPatch(
            (station_x[1], 0.875),
            (station_x[1], station_y + 0.03),
            arrowstyle="-|>",
            mutation_scale=8,
            color=colors["vermilion"],
            linewidth=1.2,
            zorder=5,
        )
    )

    choice_y = [0.465, 0.315, 0.165]
    fills = {"vermilion": "#FFF0EB", "jade": "#E8FAF5", "cobalt": "#EDF3FF"}
    for choice, y_value in zip(config["choices"], choice_y, strict=True):
        accent = colors[choice["color"]]
        ax.add_patch(
            FancyBboxPatch(
                (0.02, y_value - 0.058),
                0.67,
                0.116,
                boxstyle="round,pad=0.01,rounding_size=0.014",
                facecolor=fills[choice["color"]],
                edgecolor=accent,
                linewidth=1.0,
            )
        )
        ax.text(0.045, y_value + 0.022, choice["time"], fontsize=6.5, color=accent, fontweight="bold", va="center")
        ax.text(
            0.25,
            y_value,
            f"{choice['zh']}\n{choice['ja']}\n{choice['en']}",
            fontsize=5.75,
            color=colors["ink"],
            fontweight="bold",
            va="center",
            linespacing=1.1,
        )

    ax.add_patch(
        FancyBboxPatch(
            (0.72, 0.105),
            0.265,
            0.42,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#FFF4F6",
            edgecolor=colors["danger"],
            linewidth=1.1,
        )
    )
    ax.text(
        0.745,
        0.49,
        "三类活动，条件不同\n利用条件はそれぞれ異なる\nCHECK EACH ACCESS RULE",
        fontsize=6.2,
        color=colors["danger"],
        fontweight="bold",
        va="top",
        linespacing=1.12,
    )
    ax.text(
        0.745,
        0.37,
        "索道乘坐・ロープウェイ乗車\nROPEWAY RIDE\n"
        "公共展望区・一般見学エリア\nPUBLIC OVERLOOK\n"
        "预约研究路・予約制自然研究路\nBOOKED TRAIL",
        fontsize=5.1,
        color=colors["ink"],
        fontweight="bold",
        va="top",
        linespacing=1.08,
    )
    ax.text(
        0.745,
        0.122,
        "停运或封闭 → 听从现场人员\n"
        "運休・閉鎖 → 係員に従う\n"
        "CLOSED → FOLLOW STAFF",
        fontsize=5.15,
        color=colors["danger"],
        va="bottom",
        linespacing=1.05,
    )

    fig.text(
        0.04,
        0.073,
        "停留时间为 LazyTravel 计划范围，不是运营方承诺；研究路正餐另计。当天核对索道、火山与预约状态。",
        fontsize=5.35,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.043,
        "滞在時間は旅行計画用の目安で、運行保証ではない。自然研究路の日は食事時間を別に取り、当日の運行・火山・予約状況を確認する。",
        fontsize=5.25,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.013,
        "LazyTravel planning ranges, not operator guarantees. Add meal time to a trail booking; recheck ropeway, volcanic and reservation status that day.",
        fontsize=5.2,
        color=colors["muted"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(svg_path, format="svg", metadata={"Date": None})
    normalize_svg(svg_path)
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), format="pdf", metadata=metadata)
    fig.savefig(OUTPUT_STEM.with_suffix(".png"), format="png", dpi=480, metadata={"Date": None})
    plt.close(fig)


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    render(config)
    files = {}
    for suffix in ("svg", "pdf", "png"):
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    png_dimensions = list(Image.open(OUTPUT_STEM.with_suffix(".png")).size)
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "schematic-route-decision-render",
        "command": "python3 scripts/build_hakone_owakudani_decision_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": "Map design © LazyTravel; route and operating facts derive from the listed official sources.",
        "files": files,
        "technical_qa": {
            "minimum_png_width": 2400,
            "pdf_vector_output": True,
            "png_dimensions": png_dimensions,
            "svg_selectable_text": True
        },
        "visual_qa": config["visual_qa"]
    }
    if png_dimensions[0] < provenance["technical_qa"]["minimum_png_width"]:
        raise RuntimeError(f"map PNG is too narrow: {png_dimensions}")
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print("map: assets/maps/hakone/hakone-owakudani-decision.[svg|pdf|png]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
