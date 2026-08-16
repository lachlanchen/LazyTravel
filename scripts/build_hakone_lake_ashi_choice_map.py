#!/usr/bin/env python3
"""Build Hakone Chapter 5's Lake Ashi landing-choice diagram."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-lake-ashi-choice.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-lake-ashi-choice"
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
            "svg.hashsalt": "lazytravel-hakone-lake-ashi-choice-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

    colors = {
        "ink": "#142330",
        "muted": "#536775",
        "paper": "#FBFDFF",
        "lake": "#DFF5FA",
        "lake_edge": "#67BDD2",
        "jade": "#008E78",
        "jade_fill": "#E7F8F2",
        "cobalt": "#1769E0",
        "cobalt_fill": "#EAF1FF",
        "coral": "#E33E63",
        "coral_fill": "#FFF0F4",
        "orange": "#F06A24",
        "orange_fill": "#FFF3E8",
    }

    fig, ax = plt.subplots(figsize=(7, 5.15), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.025, right=0.985, top=0.80, bottom=0.08)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.04, 0.962, config["title"]["zh"], fontsize=14.2, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.915, config["title"]["ja"], fontsize=10.3, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.873, config["title"]["en"], fontsize=9.3, fontweight="bold", color=colors["cobalt"])
    fig.text(
        0.965,
        0.955,
        "选择图・選択図\nCHOICE DIAGRAM",
        fontsize=7.0,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    ax.add_patch(
        FancyBboxPatch(
            (0.01, 0.06),
            0.635,
            0.89,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#F4FAFC",
            edgecolor="#BED8E2",
            linewidth=1.1,
        )
    )
    lake_shape = [
        (0.27, 0.90),
        (0.39, 0.83),
        (0.43, 0.68),
        (0.54, 0.52),
        (0.48, 0.33),
        (0.31, 0.26),
        (0.16, 0.39),
        (0.22, 0.60),
        (0.18, 0.76),
    ]
    ax.add_patch(
        Polygon(
            lake_shape,
            closed=True,
            facecolor=colors["lake"],
            edgecolor=colors["lake_edge"],
            linewidth=1.4,
            zorder=0,
        )
    )
    ax.text(
        0.35,
        0.62,
        "芦之湖  Lúzhī Hú\n芦ノ湖  あしのこ\nLAKE ASHI",
        fontsize=8.0,
        color="#21738A",
        fontweight="bold",
        ha="center",
        va="center",
        linespacing=1.16,
        zorder=2,
    )

    nodes = {item["id"]: item for item in config["nodes"]}

    def node_box(
        node_id: str,
        xy: tuple[float, float],
        color: str,
        width: float = 0.19,
        font_size: float = 7.4,
    ) -> None:
        item = nodes[node_id]
        x_value, y_value = xy
        ax.add_patch(
            FancyBboxPatch(
                (x_value - width / 2, y_value - 0.067),
                width,
                0.134,
                boxstyle="round,pad=0.008,rounding_size=0.014",
                facecolor="#FFFFFF",
                edgecolor=color,
                linewidth=1.7,
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
            linespacing=1.13,
            zorder=6,
        )

    def arrow(start: tuple[float, float], end: tuple[float, float], color: str, style: str = "-") -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=11,
                color=color,
                linewidth=2.3,
                linestyle=style,
                connectionstyle="arc3,rad=0",
                zorder=3,
            )
        )

    node_box("togendai", (0.31, 0.86), colors["orange"], 0.205)
    node_box("motohakone", (0.16, 0.49), colors["jade"], 0.205)
    node_box("hakonemachi", (0.50, 0.49), colors["cobalt"], 0.205)
    arrow((0.285, 0.79), (0.18, 0.57), colors["jade"])
    arrow((0.335, 0.79), (0.48, 0.57), colors["cobalt"])
    ax.text(
        0.31,
        0.72,
        f"游览船・遊覧船・BOAT  {config['boat_minutes']}",
        fontsize=7.4,
        color=colors["ink"],
        fontweight="bold",
        ha="center",
        va="center",
        bbox={"boxstyle": "round,pad=0.32", "facecolor": "#FFFFFF", "edgecolor": colors["lake_edge"]},
        zorder=7,
    )

    node_box("shrine", (0.11, 0.24), colors["jade"], 0.19, 6.9)
    node_box("lunch", (0.325, 0.24), colors["coral"], 0.19, 6.9)
    node_box("park", (0.54, 0.24), colors["cobalt"], 0.18, 6.9)
    arrow((0.14, 0.42), (0.115, 0.315), colors["jade"])
    arrow((0.20, 0.44), (0.30, 0.315), colors["coral"], "--")
    arrow((0.50, 0.42), (0.535, 0.315), colors["cobalt"])
    ax.text(
        0.13,
        0.37,
        "约10分・約10分・~10 MIN",
        fontsize=6.5,
        color=colors["jade"],
        fontweight="bold",
        ha="center",
        va="center",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": "#FFFFFF", "edgecolor": "none"},
    )

    ax.text(
        0.326,
        0.09,
        "早到南岸：神社 → 午饭 → 公园 → 旅馆／返程巴士\n"
        "南岸へ早着：神社 → 昼食 → 公園 → 宿／帰路のバス\n"
        "EARLY SOUTH SHORE: SHRINE → LUNCH → PARK → STAY / RETURN BUS",
        fontsize=6.25,
        color=colors["ink"],
        fontweight="bold",
        ha="center",
        va="center",
        linespacing=1.13,
    )

    fills = {"jade": colors["jade_fill"], "cobalt": colors["cobalt_fill"], "coral": colors["coral_fill"]}
    choice_y = [0.82, 0.59, 0.34]
    for choice, y_value in zip(config["choices"], choice_y, strict=True):
        accent = colors[choice["color"]]
        ax.add_patch(
            FancyBboxPatch(
                (0.68, y_value - 0.09),
                0.305,
                0.18,
                boxstyle="round,pad=0.012,rounding_size=0.018",
                facecolor=fills[choice["color"]],
                edgecolor=accent,
                linewidth=1.2,
            )
        )
        ax.text(0.705, y_value + 0.047, choice["time"], fontsize=8.7, color=accent, fontweight="bold", va="center")
        ax.text(
            0.705,
            y_value - 0.025,
            f"{choice['zh']}\n{choice['ja']}\n{choice['en']}",
            fontsize=7.0,
            color=colors["ink"],
            fontweight="bold",
            va="center",
            linespacing=1.12,
        )

    ax.add_patch(
        FancyBboxPatch(
            (0.68, 0.02),
            0.305,
            0.18,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor=colors["orange_fill"],
            edgecolor=colors["orange"],
            linewidth=1.2,
        )
    )
    ax.text(
        0.705,
        0.17,
        "船停运？・運休？・NO BOAT?",
        fontsize=7.7,
        color=colors["orange"],
        fontweight="bold",
        va="top",
    )
    ax.text(
        0.705,
        0.108,
        "在桃源台巴士站重排\n"
        "桃源台バス停で組み直す\n"
        "REBUILD AT TOGENDAI BUS",
        fontsize=6.5,
        color=colors["ink"],
        fontweight="bold",
        va="center",
        linespacing=1.1,
    )
    fig.text(
        0.04,
        0.052,
        "计划图，不按比例，也不是时刻表。时间为 LazyTravel 计划范围；另加午饭、排队与等车。巴士不复制航线，以当日运行和实际到港为准。",
        fontsize=5.7,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.028,
        "計画図で、縮尺図・時刻表ではない。時間は旅行計画用の目安。昼食・列・待ち時間を加える。バスは航路を代行しないため、当日の運行と到着港を優先する。",
        fontsize=5.55,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.006,
        "Planning ranges, not a timetable or scale map. Add lunch, queues and waiting. Bus does not mirror boat; follow live service and the actual landing.",
        fontsize=5.45,
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
        "method": "schematic-landing-choice-render",
        "command": "python3 scripts/build_hakone_lake_ashi_choice_map.py",
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
            "svg_selectable_text": True,
        },
        "visual_qa": config["visual_qa"],
    }
    if png_dimensions[0] < provenance["technical_qa"]["minimum_png_width"]:
        raise RuntimeError(f"map PNG is too narrow: {png_dimensions}")
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print("map: assets/maps/hakone/hakone-lake-ashi-choice.[svg|pdf|png]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
