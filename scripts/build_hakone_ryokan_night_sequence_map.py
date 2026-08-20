#!/usr/bin/env python3
"""Build Hakone Chapter 7's one-night ryokan decision sequence."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-ryokan-night-sequence.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-ryokan-night-sequence"
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
            "svg.hashsalt": "lazytravel-hakone-ryokan-night-sequence-v1",
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
        "顺序图・順序図\nDECISION SEQUENCE",
        fontsize=7.0,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    positions = {
        "arrive": (0.17, 0.81),
        "confirm": (0.50, 0.81),
        "bath": (0.83, 0.81),
        "dinner": (0.83, 0.45),
        "sleep": (0.50, 0.45),
        "morning": (0.17, 0.45),
    }
    card_width = 0.29
    card_height = 0.285

    def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=13,
                color=colors["line"],
                linewidth=2.1,
                shrinkA=2,
                shrinkB=2,
                zorder=1,
            )
        )

    arrow((0.32, 0.81), (0.35, 0.81))
    arrow((0.65, 0.81), (0.68, 0.81))
    arrow((0.83, 0.66), (0.83, 0.60))
    arrow((0.68, 0.45), (0.65, 0.45))
    arrow((0.35, 0.45), (0.32, 0.45))

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
        zh_size = 8.0 if stage["id"] == "sleep" else 8.8
        zh_reading_size = 5.15 if stage["id"] == "sleep" else 5.65
        ax.text(x_value, y_value + 0.078, stage["zh"], fontsize=zh_size, color=colors["ink"], fontweight="bold", ha="center", va="center", zorder=5)
        ax.text(x_value, y_value + 0.035, stage["zh_reading"], fontsize=zh_reading_size, color=accent, ha="center", va="center", zorder=5)
        ax.text(x_value, y_value - 0.012, stage["ja"], fontsize=7.65, color=colors["ink"], fontweight="bold", ha="center", va="center", zorder=5)
        ax.text(x_value, y_value - 0.052, stage["ja_reading"], fontsize=5.45, color=colors["muted"], ha="center", va="center", zorder=5)
        ax.text(x_value, y_value - 0.097, stage["en"], fontsize=5.75, color=accent, fontweight="bold", ha="center", va="center", zorder=5)

    delay = config["delay_branch"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.005),
            0.95,
            0.22,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            facecolor=colors["vermilion_fill"],
            edgecolor=colors["vermilion"],
            linewidth=1.4,
            zorder=2,
        )
    )
    ax.text(0.05, 0.188, delay["zh"], fontsize=8.0, color=colors["ink"], fontweight="bold", va="center")
    ax.text(0.05, 0.153, delay["zh_reading"], fontsize=5.3, color=colors["vermilion"], va="center")
    ax.text(0.05, 0.116, delay["ja"], fontsize=7.2, color=colors["ink"], fontweight="bold", va="center")
    ax.text(0.05, 0.083, delay["ja_reading"], fontsize=5.15, color=colors["muted"], va="center")
    ax.text(0.05, 0.049, delay["en"], fontsize=6.1, color=colors["vermilion"], fontweight="bold", va="center")
    ax.text(
        0.95,
        0.021,
        "具体时刻看预订确认・具体的な時刻は予約確認で・USE YOUR BOOKING'S ACTUAL TIMES",
        fontsize=5.45,
        color=colors["muted"],
        ha="right",
        va="center",
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
        "method": "schematic-ryokan-night-sequence-render",
        "command": "python3 scripts/build_hakone_ryokan_night_sequence_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": "Diagram design © LazyTravel; operating guidance derives from the listed official sources.",
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
