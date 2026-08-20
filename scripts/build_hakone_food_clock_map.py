#!/usr/bin/env python3
"""Build Hakone Chapter 8's route-led food clock diagram."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-food-clock.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-food-clock"
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
            "svg.hashsalt": "lazytravel-hakone-food-clock-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

    colors = {
        "ink": "#13242F",
        "muted": "#536774",
        "paper": "#FBFDFF",
        "vermilion": "#E84A2A",
        "vermilion_fill": "#FFF1EC",
        "jade": "#008B72",
        "jade_fill": "#E8F8F2",
        "cobalt": "#1769D8",
        "cobalt_fill": "#EAF2FF",
        "coral": "#DF3F68",
        "coral_fill": "#FFF0F4",
        "line": "#9FB7C5",
    }

    fig, ax = plt.subplots(figsize=(7, 5.6), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.025, right=0.975, top=0.84, bottom=0.025)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.04, 0.967, config["title"]["zh"], fontsize=14.5, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.921, config["title"]["ja"], fontsize=10.6, fontweight="bold", color=colors["ink"])
    fig.text(0.04, 0.879, config["title"]["en"], fontsize=8.8, fontweight="bold", color=colors["cobalt"])
    fig.text(
        0.965,
        0.96,
        "食物角色图・食事役割図\nFOOD-ROLE DIAGRAM",
        fontsize=7.0,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    positions = {
        "odawara": (0.17, 0.80),
        "gora": (0.50, 0.80),
        "owakudani": (0.83, 0.80),
        "lake": (0.83, 0.47),
        "oldroad": (0.50, 0.47),
        "ryokan": (0.17, 0.47),
    }
    card_width = 0.29
    card_height = 0.25

    def arrow(
        start: tuple[float, float],
        end: tuple[float, float],
        *,
        dashed: bool = False,
    ) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=12,
                color=colors["line"],
                linewidth=2.0,
                linestyle="--" if dashed else "-",
                shrinkA=2,
                shrinkB=2,
                zorder=1,
            )
        )

    arrow((0.32, 0.80), (0.35, 0.80))
    arrow((0.65, 0.80), (0.68, 0.80))
    arrow((0.83, 0.67), (0.83, 0.60))
    arrow((0.68, 0.47), (0.65, 0.47), dashed=True)
    arrow((0.35, 0.47), (0.32, 0.47), dashed=True)

    for stage in config["stages"]:
        x_value, y_value = positions[stage["id"]]
        accent = colors[stage["color"]]
        fill = colors[f"{stage['color']}_fill"]
        ax.add_patch(
            FancyBboxPatch(
                (x_value - card_width / 2, y_value - card_height / 2),
                card_width,
                card_height,
                boxstyle="round,pad=0.008,rounding_size=0.018",
                facecolor=fill,
                edgecolor=accent,
                linewidth=1.35,
                zorder=2,
            )
        )
        ax.add_patch(
            Circle(
                (x_value - card_width / 2 + 0.032, y_value + card_height / 2 - 0.034),
                radius=0.024,
                facecolor=accent,
                edgecolor="none",
                zorder=4,
            )
        )
        ax.text(
            x_value - card_width / 2 + 0.032,
            y_value + card_height / 2 - 0.034,
            stage["number"],
            fontsize=7.3,
            color="#FFFFFF",
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value,
            y_value + 0.065,
            stage["zh"],
            fontsize=7.7,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value,
            y_value + 0.026,
            stage["zh_reading"],
            fontsize=4.65,
            color=accent,
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value,
            y_value - 0.016,
            stage["ja"],
            fontsize=6.8,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value,
            y_value - 0.053,
            stage["ja_reading"],
            fontsize=4.45,
            color=colors["muted"],
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value,
            y_value - 0.094,
            stage["en"],
            fontsize=5.25,
            color=accent,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

    decision = config["decision_band"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.015),
            0.95,
            0.22,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            facecolor=colors["cobalt_fill"],
            edgecolor=colors["cobalt"],
            linewidth=1.4,
            zorder=2,
        )
    )
    ax.text(0.05, 0.195, decision["zh"], fontsize=7.6, color=colors["ink"], fontweight="bold", va="center")
    ax.text(0.05, 0.155, decision["zh_reading"], fontsize=4.75, color=colors["cobalt"], va="center")
    ax.text(0.05, 0.114, decision["ja"], fontsize=6.8, color=colors["ink"], fontweight="bold", va="center")
    ax.text(0.05, 0.077, decision["ja_reading"], fontsize=4.55, color=colors["muted"], va="center")
    ax.text(0.05, 0.040, decision["en"], fontsize=6.0, color=colors["cobalt"], fontweight="bold", va="center")
    ax.text(
        0.95,
        0.006,
        "节点可跳过・地点は省略可・EVERY NODE IS OPTIONAL",
        fontsize=5.2,
        color=colors["muted"],
        ha="right",
        va="bottom",
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
        "method": "schematic-hakone-food-clock-render",
        "command": "python3 scripts/build_hakone_food_clock_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": "Diagram design © LazyTravel; food and operating facts derive from the listed official sources.",
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
        raise RuntimeError(f"diagram PNG is too small: {png_dimensions}")
    print(f"diagram: {OUTPUT_STEM.relative_to(ROOT)} (PNG {png_dimensions[0]}x{png_dimensions[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
