#!/usr/bin/env python3
"""Build Hakone Chapter 6's old-Tokaido route-choice diagram."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-old-tokaido-choice.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-old-tokaido-choice"
FIXED_TIME = datetime(2026, 8, 20, 0, 0, tzinfo=timezone.utc)
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
            "svg.hashsalt": "lazytravel-hakone-old-tokaido-choice-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    colors = {
        "ink": "#142330",
        "muted": "#536775",
        "paper": "#FBFDFF",
        "jade": "#008E78",
        "jade_fill": "#E7F8F2",
        "cobalt": "#1769E0",
        "cobalt_fill": "#EAF1FF",
        "coral": "#E33E63",
        "coral_fill": "#FFF0F4",
        "vermilion": "#E94B2C",
        "orange_fill": "#FFF2E8",
        "stone": "#667780",
        "stone_fill": "#EEF2F4",
        "cedar": "#176B4F",
        "road": "#D7E2E8",
    }

    fig, ax = plt.subplots(figsize=(7, 5.15), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.025, right=0.985, top=0.80, bottom=0.09)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.04, 0.962, config["title"]["zh"], fontsize=14.2, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.915, config["title"]["ja"], fontsize=10.3, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.873, config["title"]["en"], fontsize=9.3, fontweight="bold", color=colors["cobalt"])
    fig.text(
        0.965,
        0.955,
        "步行选择图・歩行選択図\nWALK CHOICE",
        fontsize=7.0,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    ax.add_patch(
        FancyBboxPatch(
            (0.01, 0.035),
            0.63,
            0.92,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#F5FAFC",
            edgecolor="#BCD3DE",
            linewidth=1.1,
        )
    )
    nodes = {item["id"]: item for item in config["nodes"]}

    def node_box(
        node_id: str,
        xy: tuple[float, float],
        color: str,
        width: float = 0.25,
        font_size: float = 7.2,
        fill: str = "#FFFFFF",
    ) -> None:
        item = nodes[node_id]
        x_value, y_value = xy
        ax.add_patch(
            FancyBboxPatch(
                (x_value - width / 2, y_value - 0.061),
                width,
                0.122,
                boxstyle="round,pad=0.008,rounding_size=0.014",
                facecolor=fill,
                edgecolor=color,
                linewidth=1.65,
                zorder=5,
            )
        )
        ax.text(
            x_value,
            y_value,
            f"{item['zh']}  {item['zh_reading']}\n"
            f"{item['ja']}  {item['ja_reading']}\n{item['en']}",
            fontsize=font_size,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            linespacing=1.12,
            zorder=6,
        )

    def arrow(
        start: tuple[float, float],
        end: tuple[float, float],
        color: str,
        style: str = "-",
        width: float = 2.5,
    ) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=11,
                color=color,
                linewidth=width,
                linestyle=style,
                connectionstyle="arc3,rad=0",
                zorder=3,
            )
        )

    node_box("checkpoint", (0.23, 0.85), colors["vermilion"], width=0.26)
    node_box("cedars", (0.47, 0.70), colors["cedar"], width=0.25, fill="#F0FAF4")
    node_box("old_road_entrance", (0.23, 0.55), colors["cobalt"], width=0.26)
    node_box("stone", (0.47, 0.39), colors["stone"], width=0.25, fill=colors["stone_fill"])
    node_box("chaya", (0.23, 0.23), colors["coral"], width=0.26, fill=colors["coral_fill"])
    node_box("hatajuku", (0.47, 0.085), colors["vermilion"], width=0.25, fill=colors["orange_fill"])

    arrow((0.35, 0.82), (0.405, 0.735), colors["cedar"])
    arrow((0.405, 0.67), (0.30, 0.58), colors["cobalt"])
    arrow((0.35, 0.52), (0.405, 0.425), colors["stone"])
    arrow((0.405, 0.36), (0.30, 0.265), colors["coral"])
    arrow((0.35, 0.195), (0.405, 0.12), colors["vermilion"], "--", 2.0)

    for x_value, y_value in ((0.055, 0.85), (0.055, 0.55), (0.055, 0.23)):
        ax.add_patch(
            FancyBboxPatch(
                (x_value - 0.032, y_value - 0.022),
                0.064,
                0.044,
                boxstyle="round,pad=0.006,rounding_size=0.01",
                facecolor="#FFFFFF",
                edgecolor=colors["cobalt"],
                linewidth=1.0,
                zorder=7,
            )
        )
        ax.text(x_value, y_value, "BUS", fontsize=5.9, color=colors["cobalt"], fontweight="bold", ha="center", va="center", zorder=8)

    fills = {"jade": colors["jade_fill"], "cobalt": colors["cobalt_fill"]}
    choice_y = [0.78, 0.49]
    for choice, y_value in zip(config["choices"], choice_y, strict=True):
        accent = colors[choice["color"]]
        ax.add_patch(
            FancyBboxPatch(
                (0.675, y_value - (0.11 if choice["id"] == "short" else 0.13)),
                0.31,
                0.22 if choice["id"] == "short" else 0.26,
                boxstyle="round,pad=0.012,rounding_size=0.018",
                facecolor=fills[choice["color"]],
                edgecolor=accent,
                linewidth=1.25,
            )
        )
        if choice["id"] == "short":
            time_text = choice["time"]
        else:
            time_text = f"{choice['time']}\n{choice['ja_time']}\n{choice['en_time']}"
        ax.text(
            0.7,
            y_value + (0.073 if choice["id"] == "short" else 0.104),
            time_text,
            fontsize=7.1 if choice["id"] == "short" else 5.85,
            color=accent,
            fontweight="bold",
            va="top",
            linespacing=1.05,
        )
        ax.text(
            0.7,
            y_value - (0.025 if choice["id"] == "short" else 0.062),
            f"{choice['zh']}\n{choice['ja']}\n{choice['en']}",
            fontsize=6.3,
            color=colors["ink"],
            fontweight="bold",
            va="center",
            linespacing=1.12,
        )

    closure = config["closure"]
    ax.add_patch(
        FancyBboxPatch(
            (0.675, 0.045),
            0.31,
            0.245,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor=colors["orange_fill"],
            edgecolor=colors["vermilion"],
            linewidth=1.35,
        )
    )
    ax.text(0.7, 0.26, closure["dates"], fontsize=7.1, color=colors["vermilion"], fontweight="bold", va="top")
    ax.text(
        0.7,
        0.165,
        f"{closure['zh']}\n{closure['ja']}\n{closure['en']}",
        fontsize=6.8,
        color=colors["ink"],
        fontweight="bold",
        va="center",
        linespacing=1.12,
    )
    ax.text(
        0.7,
        0.086,
        f"{closure['instruction_zh']}\n{closure['instruction_ja']}\n{closure['instruction_en']}",
        fontsize=5.0,
        color=colors["muted"],
        va="center",
        linespacing=1.1,
    )

    fig.text(
        0.04,
        0.052,
        "选择图，不按比例，也不是时刻表。石板潮湿时明显更滑；另加关所参观、茶屋停留和等车时间。下段封闭与巴士班次须按出发日复查。",
        fontsize=5.62,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.029,
        "選択図で、縮尺図・時刻表ではない。濡れた石畳は滑りやすい。関所見学、茶屋、バス待ちを加え、下部通行止めと便を当日再確認する。",
        fontsize=5.48,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.006,
        "Choice diagram, not a scale map or timetable. Wet stone is slick. Add checkpoint, tea and waiting; recheck closure and buses on the day.",
        fontsize=5.38,
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
    files: dict[str, dict[str, Any]] = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    with Image.open(OUTPUT_STEM.with_suffix(".png")) as image:
        png_dimensions = [image.width, image.height]
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "schematic-old-road-choice-render",
        "command": "python3 scripts/build_hakone_old_tokaido_choice_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": "Map design © LazyTravel; route and operating facts derive from the listed official sources.",
        "files": files,
        "technical_qa": {
            "minimum_png_width": 2400,
            "png_dimensions": png_dimensions,
            "pdf_vector_output": True,
            "svg_selectable_text": True,
        },
        "visual_qa": config["visual_qa"],
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    if png_dimensions[0] < 2400:
        raise RuntimeError(f"map PNG is too small: {png_dimensions}")
    print(f"map: {OUTPUT_STEM.relative_to(ROOT)} (PNG {png_dimensions[0]}x{png_dimensions[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
