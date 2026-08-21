#!/usr/bin/env python3
"""Build Lanzhou Chapter 3's current-walk and historical-layers map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-history-walk.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-history-walk"
FIXED_TIME = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#25313A",
    "muted": "#65717B",
    "line": "#B8C3CB",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F1FC",
    "vermilion": "#E44736",
    "vermilion_light": "#FCEBE8",
    "jade": "#23836B",
    "jade_light": "#E5F3EE",
    "coral": "#F06E65",
    "coral_light": "#FDECEA",
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
            "svg.hashsalt": "lazytravel-lanzhou-history-walk-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.055, right=0.945, top=0.96, bottom=0.04)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(COLORS["paper"])

    title = config["title"]
    ax.text(
        0,
        0.98,
        f"{title['zh']} · {title['ja']}",
        fontsize=16.2,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )
    ax.text(
        0,
        0.928,
        title["en"],
        fontsize=8.8,
        fontweight="bold",
        color=COLORS["cobalt"],
        va="top",
    )
    ax.text(
        1,
        0.928,
        "SCHEMATIC · NOT NAVIGATION",
        fontsize=6.2,
        fontweight="bold",
        color=COLORS["muted"],
        ha="right",
        va="top",
    )

    walk = config["walk"]
    panel = FancyBboxPatch(
        (0, 0.505),
        1,
        0.39,
        boxstyle="round,pad=0.012,rounding_size=0.016",
        facecolor="#F7FAFC",
        edgecolor=COLORS["line"],
        linewidth=1.2,
    )
    ax.add_patch(panel)

    ax.add_patch(
        FancyBboxPatch(
            (0.23, 0.59),
            0.59,
            0.15,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor=COLORS["jade_light"],
            edgecolor=COLORS["jade"],
            linewidth=1.3,
            linestyle=(0, (4, 3)),
        )
    )
    ax.text(
        0.525,
        0.722,
        f"{walk['old_core']['zh']} · {walk['old_core']['ja']}",
        fontsize=7.6,
        fontweight="bold",
        color=COLORS["jade"],
        ha="center",
        va="center",
    )
    ax.text(
        0.525,
        0.699,
        walk["old_core"]["en"],
        fontsize=5.7,
        fontweight="bold",
        color=COLORS["jade"],
        ha="center",
        va="center",
    )

    ax.add_patch(
        Rectangle((0.01, 0.823), 0.98, 0.058, facecolor=COLORS["cobalt_light"], edgecolor="none")
    )
    ax.annotate(
        "",
        xy=(0.95, 0.852),
        xytext=(0.05, 0.852),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["cobalt"], "lw": 2.4},
    )
    ax.text(
        0.5,
        0.852,
        f"{walk['river']['zh']} · {walk['river']['ja']} · {walk['river']['en']}  →",
        fontsize=8.2,
        fontweight="bold",
        color=COLORS["cobalt"],
        ha="center",
        va="center",
        bbox={"facecolor": COLORS["cobalt_light"], "edgecolor": "none", "pad": 2.2},
    )

    road_y = 0.644
    ax.plot([0.15, 0.88], [road_y, road_y], color=COLORS["ink"], lw=5.5, solid_capstyle="round")
    ax.text(
        0.53,
        0.616,
        f"{walk['road']['zh']} · {walk['road']['ja']} · {walk['road']['en']}",
        fontsize=8.0,
        fontweight="bold",
        color=COLORS["ink"],
        ha="center",
        va="top",
    )
    ax.annotate(
        "",
        xy=(0.17, road_y),
        xytext=(0.87, road_y),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["vermilion"], "lw": 2.3},
    )
    ax.plot([0.17, 0.17], [road_y, 0.797], color=COLORS["vermilion"], lw=2.3)
    ax.annotate(
        "",
        xy=(0.17, 0.807),
        xytext=(0.17, 0.758),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["vermilion"], "lw": 2.3},
    )

    ax.add_patch(Circle((0.88, road_y), 0.018, facecolor=COLORS["coral"], edgecolor=COLORS["paper"], lw=1.5))
    ax.text(
        0.88,
        0.583,
        f"{walk['start']['zh']}\n{walk['start']['ja']}\n{walk['start']['en']}",
        fontsize=5.8,
        fontweight="bold",
        color=COLORS["coral"],
        ha="center",
        va="top",
        linespacing=1.2,
    )

    for x, gate, direction in (
        (0.30, walk["west_gate"], "west"),
        (0.76, walk["east_gate"], "east"),
    ):
        diamond = Polygon(
            [(x, road_y + 0.018), (x + 0.018, road_y), (x, road_y - 0.018), (x - 0.018, road_y)],
            closed=True,
            facecolor=COLORS["paper"],
            edgecolor=COLORS["vermilion"],
            linewidth=1.5,
        )
        ax.add_patch(diamond)
        align = "right" if direction == "west" else "left"
        label_x = x - 0.025 if direction == "west" else x + 0.025
        ax.text(
            label_x,
            0.674,
            f"{gate['zh']}\n{gate['en']}",
            fontsize=5.7,
            color=COLORS["vermilion"],
            fontweight="bold",
            ha=align,
            va="bottom",
            linespacing=1.15,
        )

    temple_x = 0.54
    ax.add_patch(
        FancyBboxPatch(
            (temple_x - 0.025, road_y - 0.024),
            0.05,
            0.048,
            boxstyle="round,pad=0.003,rounding_size=0.006",
            facecolor=COLORS["vermilion"],
            edgecolor=COLORS["paper"],
            linewidth=1.3,
        )
    )
    ax.text(
        temple_x,
        0.752,
        f"{walk['temple']['zh']} · {walk['temple']['ja']}\n{walk['temple']['en']}",
        fontsize=7.0,
        fontweight="bold",
        color=COLORS["vermilion"],
        ha="center",
        va="bottom",
        linespacing=1.25,
    )

    ax.add_patch(Circle((0.17, road_y), 0.018, facecolor=COLORS["jade"], edgecolor=COLORS["paper"], lw=1.5))
    ax.text(
        0.13,
        0.59,
        f"{walk['xiguan']['zh']} · {walk['xiguan']['ja']}\n{walk['xiguan']['en']}",
        fontsize=6.2,
        fontweight="bold",
        color=COLORS["jade"],
        ha="center",
        va="top",
    )
    ax.add_patch(Circle((0.17, 0.807), 0.019, facecolor=COLORS["cobalt"], edgecolor=COLORS["paper"], lw=1.5))
    ax.text(
        0.205,
        0.798,
        f"{walk['bridge']['zh']} · {walk['bridge']['ja']}\n{walk['bridge']['en']}",
        fontsize=6.3,
        fontweight="bold",
        color=COLORS["cobalt"],
        ha="left",
        va="center",
        linespacing=1.18,
    )

    ax.annotate(
        "",
        xy=(0.02, 0.54),
        xytext=(0.27, 0.54),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["jade"], "lw": 1.8},
    )
    ax.text(
        0.02,
        0.515,
        f"{walk['west_expansion']['zh']} · {walk['west_expansion']['en']}",
        fontsize=5.8,
        fontweight="bold",
        color=COLORS["jade"],
        ha="left",
        va="top",
    )
    ax.annotate(
        "",
        xy=(0.98, 0.54),
        xytext=(0.73, 0.54),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["coral"], "lw": 1.8},
    )
    ax.text(
        0.98,
        0.515,
        f"{walk['east_expansion']['zh']} · {walk['east_expansion']['en']}",
        fontsize=5.8,
        fontweight="bold",
        color=COLORS["coral"],
        ha="right",
        va="top",
    )

    ax.text(
        0,
        0.475,
        "四层，不是一条不变的古城 · 四層は一つの不変な都市ではない · FOUR LAYERS, NOT ONE UNCHANGED CITY",
        fontsize=7.0,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )

    fills = {
        "cobalt": COLORS["cobalt_light"],
        "jade": COLORS["jade_light"],
        "vermilion": COLORS["vermilion_light"],
        "coral": COLORS["coral_light"],
    }
    positions = [(0, 0.265), (0.51, 0.265), (0, 0.055), (0.51, 0.055)]
    for (x, y), layer in zip(positions, config["layers"]):
        color = COLORS[layer["color"]]
        card = FancyBboxPatch(
            (x, y),
            0.49,
            0.18,
            boxstyle="round,pad=0.009,rounding_size=0.012",
            facecolor=fills[layer["color"]],
            edgecolor=color,
            linewidth=1.35,
            linestyle=(0, (3, 2)) if layer["symbol"] == "uncertain" else "solid",
        )
        ax.add_patch(card)
        ax.text(
            x + 0.025,
            y + 0.148,
            layer["date"],
            fontsize=8.2,
            fontweight="bold",
            color=color,
            va="center",
        )
        ax.text(
            x + 0.025,
            y + 0.111,
            f"{layer['zh']} · {layer['ja']}",
            fontsize=7.4,
            fontweight="bold",
            color=COLORS["ink"],
            va="center",
        )
        ax.text(
            x + 0.025,
            y + 0.080,
            layer["en"],
            fontsize=5.8,
            fontweight="bold",
            color=color,
            va="center",
        )
        ax.add_line(Line2D([x + 0.025, x + 0.465], [y + 0.055, y + 0.055], color=color, alpha=0.35, lw=1.0))
        ax.text(
            x + 0.025,
            y + 0.031,
            f"{layer['note_zh']} · {layer['note_ja']}",
            fontsize=5.6,
            color=COLORS["ink"],
            va="center",
        )
        ax.text(
            x + 0.465,
            y + 0.012,
            layer["note_en"],
            fontsize=4.7,
            fontweight="bold",
            color=COLORS["muted"],
            ha="right",
            va="bottom",
        )

    ax.text(
        0,
        0.012,
        "旧城门为约位；金城县治比定有争议 · FORMER GATES APPROXIMATE; EARLY JINCHENG SEAT DISPUTED",
        fontsize=5.3,
        color=COLORS["muted"],
        va="bottom",
    )
    ax.text(1.0, 0.884, "N ↑", fontsize=6.2, fontweight="bold", color=COLORS["ink"], ha="right", va="top")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_STEM.with_suffix(".png")
    pdf_path = OUTPUT_STEM.with_suffix(".pdf")
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    metadata = {"Creator": "LazyTravel", "Date": None}
    fig.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), metadata={"Software": "LazyTravel"})
    fig.savefig(pdf_path, facecolor=fig.get_facecolor(), metadata=metadata)
    fig.savefig(svg_path, facecolor=fig.get_facecolor(), metadata=metadata)
    plt.close(fig)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n", encoding="utf-8")
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
        "asset_id": "asset-lanzhou-history-walk-map",
        "created_at": config["snapshot_date"],
        "command": "python3 scripts/build_lanzhou_history_walk_map.py",
        "config": {
            "path": str(CONFIG_PATH.relative_to(ROOT)),
            "sha256": sha256(CONFIG_PATH),
        },
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "visual_qa": config["visual_qa"],
        "rights": "Map design © LazyTravel; historical relationships derive from the listed institutional and local-chronicle sources.",
    }
    provenance_path = OUTPUT_STEM.with_suffix(".provenance.json")
    write_json(provenance_path, provenance)
    print(f"wrote {outputs['png']['path']}")
    print(f"wrote {outputs['pdf']['path']}")
    print(f"wrote {outputs['svg']['path']}")
    print(f"wrote {provenance_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
