#!/usr/bin/env python3
"""Build Lanzhou's three-arrival-gates pocket map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-arrival-gates.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-arrival-gates"
FIXED_TIME = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#25313A",
    "muted": "#65717B",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F1FC",
    "vermilion": "#E44736",
    "vermilion_light": "#FCEBE8",
    "jade": "#23836B",
    "jade_light": "#E5F3EE",
    "coral": "#F06E65",
    "coral_light": "#FDECEA",
    "line": "#B9C4CC",
}


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


def render_map(config: dict[str, Any]) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-arrival-gates-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
    from matplotlib.path import Path as MplPath

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.055, right=0.945, top=0.96, bottom=0.04)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(COLORS["paper"])

    title = config["title"]
    ax.text(
        0.0,
        0.978,
        f"{title['zh']} · {title['ja']}",
        fontsize=17.0,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )
    ax.text(
        0.0,
        0.927,
        title["en"],
        fontsize=9.0,
        fontweight="bold",
        color=COLORS["cobalt"],
        va="top",
    )
    ax.text(
        1.0,
        0.927,
        "NO TIMES · NO FARES · CHECK LIVE",
        fontsize=6.5,
        fontweight="bold",
        color=COLORS["muted"],
        va="top",
        ha="right",
    )

    airport = config["airport"]
    airport_box = FancyBboxPatch(
        (0.0, 0.665),
        1.0,
        0.22,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        facecolor=COLORS["cobalt_light"],
        edgecolor=COLORS["cobalt"],
        linewidth=1.8,
    )
    ax.add_patch(airport_box)
    ax.text(
        0.03,
        0.854,
        f"{airport['gate_zh']} · {airport['gate_ja']}",
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )
    ax.text(
        0.03,
        0.814,
        airport["gate_en"],
        fontsize=8.0,
        fontweight="bold",
        color=COLORS["cobalt"],
        va="top",
    )
    ax.text(
        0.03,
        0.775,
        f"{airport['rail_zh']} · {airport['rail_ja']}",
        fontsize=9.0,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )
    ax.text(
        0.03,
        0.742,
        airport["rail_en"],
        fontsize=7.0,
        color=COLORS["muted"],
        va="top",
    )
    ax.text(
        0.97,
        0.854,
        airport["scale_note"],
        fontsize=6.7,
        fontweight="bold",
        color=COLORS["cobalt"],
        ha="right",
        va="top",
    )
    mode_x = [0.60, 0.76, 0.92]
    for x, mode, color in zip(
        mode_x,
        airport["modes"],
        (COLORS["vermilion"], COLORS["jade"], COLORS["coral"]),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.07, 0.694),
                0.14,
                0.074,
                boxstyle="round,pad=0.005,rounding_size=0.008",
                facecolor=COLORS["paper"],
                edgecolor=color,
                linewidth=1.4,
            )
        )
        ax.text(
            x,
            0.746,
            mode["zh"],
            fontsize=6.5,
            fontweight="bold",
            color=COLORS["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            x,
            0.724,
            mode["ja"],
            fontsize=5.8,
            color=COLORS["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            x,
            0.703,
            mode["en"],
            fontsize=5.8,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
        )

    ax.annotate(
        "",
        xy=(0.5, 0.615),
        xytext=(0.5, 0.662),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["cobalt"], "lw": 1.8},
    )
    ax.text(
        0.5,
        0.635,
        "按住宿方向选择 · 宿の方向で選ぶ · CHOOSE BY LODGING DIRECTION",
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["cobalt"],
        ha="center",
        va="center",
        bbox={"facecolor": COLORS["paper"], "edgecolor": "none", "pad": 2.0},
    )

    segment_colors = [COLORS["vermilion"], COLORS["jade"], COLORS["coral"]]
    segment_fills = [
        COLORS["vermilion_light"],
        COLORS["jade_light"],
        COLORS["coral_light"],
    ]
    segment_x = [0.0, 0.34, 0.68]
    for x, segment, color, fill in zip(
        segment_x, config["segments"], segment_colors, segment_fills
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.477),
                0.32,
                0.122,
                boxstyle="round,pad=0.008,rounding_size=0.009",
                facecolor=fill,
                edgecolor=color,
                linewidth=1.5,
            )
        )
        ax.text(
            x + 0.16,
            0.572,
            f"{segment['title_zh']} · {segment['title_ja']} · {segment['title_en']}",
            fontsize=8.2,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.16,
            0.535,
            segment["anchors_zh"],
            fontsize=7.4,
            fontweight="bold",
            color=COLORS["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.16,
            0.511,
            segment["anchors_en"],
            fontsize=5.2,
            color=COLORS["muted"],
            ha="center",
            va="center",
            linespacing=1.15,
        )
    ax.annotate(
        "",
        xy=(0.965, 0.458),
        xytext=(0.035, 0.458),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["line"], "lw": 2.0},
    )
    ax.text(
        0.5,
        0.44,
        "城市东西方向 · 市街の東西軸 · CITY WEST–EAST SPINE",
        fontsize=6.8,
        color=COLORS["muted"],
        ha="center",
        va="top",
    )

    gate_positions = [(0.0, 0.205), (0.52, 0.205)]
    gate_width = 0.48
    for (x, y), gate, edge, fill in zip(
        gate_positions,
        config["rail_gates"],
        (COLORS["vermilion"], COLORS["coral"]),
        (COLORS["vermilion_light"], COLORS["coral_light"]),
    ):
        if gate["shape"] == "cut-corner":
            cut = 0.035
            vertices = [
                (x, y),
                (x + gate_width - cut, y),
                (x + gate_width, y + cut),
                (x + gate_width, y + 0.195),
                (x + cut, y + 0.195),
                (x, y + 0.195 - cut),
                (x, y),
            ]
            codes = [
                MplPath.MOVETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.LINETO,
                MplPath.CLOSEPOLY,
            ]
            patch = PathPatch(
                MplPath(vertices, codes), facecolor=fill, edgecolor=edge, linewidth=1.7
            )
        else:
            patch = FancyBboxPatch(
                (x, y),
                gate_width,
                0.195,
                boxstyle="round,pad=0.009,rounding_size=0.018",
                facecolor=fill,
                edgecolor=edge,
                linewidth=1.7,
            )
        ax.add_patch(patch)
        ax.text(
            x + 0.025,
            y + 0.166,
            f"{gate['rail_zh']} · {gate['rail_ja']}",
            fontsize=9.1,
            fontweight="bold",
            color=COLORS["ink"],
            va="top",
        )
        ax.text(
            x + 0.025,
            y + 0.124,
            gate["rail_en"],
            fontsize=6.8,
            fontweight="bold",
            color=edge,
            va="top",
        )
        ax.add_patch(
            Rectangle(
                (x + 0.024, y + 0.085),
                gate_width - 0.048,
                0.002,
                facecolor=edge,
                edgecolor="none",
                alpha=0.55,
            )
        )
        ax.text(
            x + 0.025,
            y + 0.071,
            gate["metro_zh"],
            fontsize=7.1,
            fontweight="bold",
            color=COLORS["ink"],
            va="top",
        )
        ax.text(
            x + 0.025,
            y + 0.045,
            gate["metro_ja"],
            fontsize=6.3,
            color=COLORS["ink"],
            va="top",
        )
        ax.text(
            x + 0.025,
            y + 0.017,
            gate["metro_en"],
            fontsize=5.3,
            color=COLORS["muted"],
            va="top",
        )

    ax.annotate(
        "",
        xy=(0.16, 0.472),
        xytext=(0.24, 0.407),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["vermilion"], "lw": 1.8},
    )
    ax.annotate(
        "",
        xy=(0.84, 0.472),
        xytext=(0.76, 0.407),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["coral"], "lw": 1.8},
    )

    steps = [
        ("1", "读票面", "券面を読む", "READ TICKET", COLORS["vermilion"]),
        ("2", "放第一站", "最初を置く", "PLACE FIRST STOP", COLORS["jade"]),
        ("3", "留备用", "代案を持つ", "KEEP FALLBACK", COLORS["cobalt"]),
    ]
    for index, (number, zh, ja, en, color) in enumerate(steps):
        x = index * 0.34
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.075),
                0.32,
                0.087,
                boxstyle="round,pad=0.006,rounding_size=0.008",
                facecolor=COLORS["paper"],
                edgecolor=color,
                linewidth=1.3,
            )
        )
        ax.text(
            x + 0.033,
            0.119,
            number,
            fontsize=14.0,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.063,
            0.136,
            f"{zh} · {ja}",
            fontsize=7.1,
            fontweight="bold",
            color=COLORS["ink"],
            va="center",
        )
        ax.text(
            x + 0.063,
            0.101,
            en,
            fontsize=6.1,
            fontweight="bold",
            color=color,
            va="center",
        )
    ax.text(
        0.0,
        0.026,
        "SCHEMATIC · 检查完整站名、当日运行与住宿地址 · 正式名・当日運行・宿の住所を確認",
        fontsize=5.8,
        color=COLORS["muted"],
        va="bottom",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_STEM.with_suffix(".png")
    pdf_path = OUTPUT_STEM.with_suffix(".pdf")
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    metadata = {"Creator": "LazyTravel", "Date": None}
    fig.savefig(
        png_path,
        dpi=300,
        facecolor=fig.get_facecolor(),
        metadata={"Software": "LazyTravel"},
    )
    fig.savefig(pdf_path, facecolor=fig.get_facecolor(), metadata=metadata)
    fig.savefig(svg_path, facecolor=fig.get_facecolor(), metadata=metadata)
    plt.close(fig)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    return {
        "png": {
            "path": str(png_path.relative_to(ROOT)),
            "sha256": sha256(png_path),
            "bytes": png_path.stat().st_size,
            "width": 1620,
            "height": 2280,
        },
        "pdf": {
            "path": str(pdf_path.relative_to(ROOT)),
            "sha256": sha256(pdf_path),
            "bytes": pdf_path.stat().st_size,
        },
        "svg": {
            "path": str(svg_path.relative_to(ROOT)),
            "sha256": sha256(svg_path),
            "bytes": svg_path.stat().st_size,
        },
    }


def main() -> int:
    config = read_json(CONFIG_PATH)
    outputs = render_map(config)
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-lanzhou-arrival-gates-map",
        "created_at": config["snapshot_date"],
        "command": "python3 scripts/build_lanzhou_arrival_gates_map.py",
        "config": {
            "path": str(CONFIG_PATH.relative_to(ROOT)),
            "sha256": sha256(CONFIG_PATH),
        },
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "visual_qa": config["visual_qa"],
        "rights": "Map design © LazyTravel; transport relationships derive from the listed official sources.",
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(f"rendered: {outputs['png']['path']}")
    print(f"vector: {outputs['svg']['path']}")
    print(f"provenance: {OUTPUT_STEM.with_suffix('.provenance.json').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
