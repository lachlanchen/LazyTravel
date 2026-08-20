#!/usr/bin/env python3
"""Build Hakone Chapter 10's one-, two-, and three-day decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-itinerary-days.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-itinerary-days"
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
            "svg.hashsalt": "lazytravel-hakone-itinerary-days-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

    colors = {
        "ink": "#13242F",
        "muted": "#536774",
        "paper": "#FBFDFF",
        "line": "#A8BBC7",
        "vermilion": "#E84A2A",
        "vermilion_fill": "#FFF0EB",
        "jade": "#008B72",
        "jade_fill": "#E7F8F2",
        "cobalt": "#1769D8",
        "cobalt_fill": "#EAF2FF",
        "coral": "#D83D67",
        "coral_fill": "#FFF0F4",
        "white": "#FFFFFF",
    }

    fig, ax = plt.subplots(figsize=(5.1, 7.2), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.018, right=0.982, top=0.995, bottom=0.012)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(
        0.025,
        0.985,
        title["zh"],
        fontsize=13.0,
        fontweight="bold",
        color=colors["ink"],
        ha="left",
        va="top",
    )
    ax.text(
        0.025,
        0.952,
        title["ja"],
        fontsize=8.8,
        fontweight="bold",
        color=colors["ink"],
        ha="left",
        va="top",
    )
    ax.text(
        0.025,
        0.922,
        title["en"],
        fontsize=6.8,
        fontweight="bold",
        color=colors["cobalt"],
        ha="left",
        va="top",
    )

    rule = config["rule"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.822),
            0.95,
            0.080,
            boxstyle="round,pad=0.007,rounding_size=0.014",
            facecolor=colors["cobalt_fill"],
            edgecolor=colors["cobalt"],
            linewidth=1.2,
        )
    )
    ax.text(0.045, 0.888, rule["zh"], fontsize=7.2, fontweight="bold", color=colors["ink"], va="center")
    ax.text(0.045, 0.873, rule["zh_reading"], fontsize=4.8, color=colors["cobalt"], va="center")
    ax.text(0.045, 0.857, rule["ja"], fontsize=6.4, fontweight="bold", color=colors["ink"], va="center")
    ax.text(0.045, 0.842, rule["ja_reading"], fontsize=4.5, color=colors["muted"], va="center")
    ax.text(0.955, 0.835, rule["en"], fontsize=4.9, fontweight="bold", color=colors["cobalt"], ha="right", va="center")

    lane_bounds = (
        (0.025, 0.625, 0.95, 0.190),
        (0.025, 0.420, 0.95, 0.190),
        (0.025, 0.215, 0.95, 0.190),
    )
    node_x = (0.188, 0.392, 0.596, 0.800)
    node_width = 0.176

    for lane, (x, y, width, height) in zip(config["lanes"], lane_bounds, strict=True):
        accent = colors[lane["color"]]
        fill = colors[f"{lane['color']}_fill"]
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                width,
                height,
                boxstyle="round,pad=0.006,rounding_size=0.014",
                facecolor=colors["white"],
                edgecolor=accent,
                linewidth=1.25,
            )
        )
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.008, y + 0.077),
                0.128,
                0.102,
                boxstyle="round,pad=0.004,rounding_size=0.010",
                facecolor=fill,
                edgecolor=accent,
                linewidth=1.0,
            )
        )
        label = lane["label"]
        ax.text(x + 0.072, y + 0.159, label["zh"], fontsize=9.0, fontweight="bold", color=colors["ink"], ha="center", va="center")
        ax.text(x + 0.072, y + 0.136, label["zh_reading"], fontsize=5.2, color=accent, ha="center", va="center")
        ax.text(x + 0.072, y + 0.112, label["ja"], fontsize=7.3, fontweight="bold", color=colors["ink"], ha="center", va="center")
        ax.text(x + 0.072, y + 0.089, label["ja_reading"], fontsize=4.9, color=colors["muted"], ha="center", va="center")
        ax.text(x + 0.072, y + 0.063, label["en"], fontsize=5.5, fontweight="bold", color=accent, ha="center", va="center")

        for index, (node, node_left) in enumerate(zip(lane["nodes"], node_x, strict=True)):
            ax.add_patch(
                FancyBboxPatch(
                    (node_left, y + 0.074),
                    node_width,
                    0.102,
                    boxstyle="round,pad=0.004,rounding_size=0.010",
                    facecolor=fill,
                    edgecolor=accent,
                    linewidth=0.95,
                )
            )
            center = node_left + node_width / 2
            ax.text(center, y + 0.157, node["zh"], fontsize=7.7, fontweight="bold", color=colors["ink"], ha="center", va="center")
            ax.text(center, y + 0.137, node["zh_reading"], fontsize=4.8, color=accent, ha="center", va="center")
            ax.text(center, y + 0.116, node["ja"], fontsize=6.4, fontweight="bold", color=colors["ink"], ha="center", va="center")
            ax.text(center, y + 0.096, node["ja_reading"], fontsize=4.6, color=colors["muted"], ha="center", va="center")
            ax.text(center, y + 0.079, node["en"], fontsize=4.8, fontweight="bold", color=accent, ha="center", va="center")
            if index < len(lane["nodes"]) - 1:
                next_left = node_x[index + 1]
                ax.add_patch(
                    FancyArrowPatch(
                        (node_left + node_width + 0.003, y + 0.125),
                        (next_left - 0.004, y + 0.125),
                        arrowstyle="-|>",
                        mutation_scale=8,
                        color=accent,
                        linewidth=1.25,
                        zorder=5,
                    )
                )

        fallback = lane["fallback"]
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.150, y + 0.010),
                0.797,
                0.058,
                boxstyle="round,pad=0.003,rounding_size=0.008",
                facecolor=colors["paper"],
                edgecolor=accent,
                linewidth=0.9,
                linestyle=(0, (3, 2)),
            )
        )
        ax.text(x + 0.165, y + 0.056, fallback["zh"], fontsize=5.6, fontweight="bold", color=colors["ink"], ha="left", va="center")
        ax.text(x + 0.165, y + 0.038, fallback["zh_reading"], fontsize=4.1, color=accent, ha="left", va="center")
        ax.text(x + 0.940, y + 0.056, fallback["ja"], fontsize=5.2, fontweight="bold", color=colors["ink"], ha="right", va="center")
        ax.text(x + 0.940, y + 0.038, fallback["ja_reading"], fontsize=4.0, color=colors["muted"], ha="right", va="center")
        ax.text(x + 0.555, y + 0.018, fallback["en"], fontsize=4.3, fontweight="bold", color=accent, ha="center", va="center")

    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.105),
            0.95,
            0.095,
            boxstyle="round,pad=0.005,rounding_size=0.012",
            facecolor=colors["white"],
            edgecolor=colors["line"],
            linewidth=1.0,
        )
    )
    weather_x = (0.050, 0.370, 0.690)
    for item, x_value in zip(config["weather"], weather_x, strict=True):
        accent = colors[item["color"]]
        ax.add_patch(Circle((x_value, 0.153), 0.020, facecolor=accent, edgecolor="none"))
        ax.text(x_value, 0.153, item["symbol"], fontsize=7.2, fontweight="bold", color=colors["white"], ha="center", va="center")
        ax.text(x_value + 0.031, 0.183, item["zh"], fontsize=6.1, fontweight="bold", color=colors["ink"], ha="left", va="center")
        ax.text(x_value + 0.031, 0.164, item["zh_reading"], fontsize=3.85, color=accent, ha="left", va="center")
        ax.text(x_value + 0.031, 0.145, item["ja"], fontsize=5.4, fontweight="bold", color=colors["ink"], ha="left", va="center")
        ax.text(x_value + 0.031, 0.128, item["ja_reading"], fontsize=3.65, color=colors["muted"], ha="left", va="center")
        ax.text(x_value + 0.031, 0.112, item["en"], fontsize=3.9, fontweight="bold", color=accent, ha="left", va="center")

    cut = config["cut_order"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.015),
            0.95,
            0.080,
            boxstyle="round,pad=0.006,rounding_size=0.012",
            facecolor=colors["vermilion_fill"],
            edgecolor=colors["vermilion"],
            linewidth=1.1,
        )
    )
    ax.text(0.500, 0.083, cut["zh"], fontsize=5.25, fontweight="bold", color=colors["ink"], ha="center", va="center")
    ax.text(0.500, 0.068, cut["zh_reading"], fontsize=3.25, color=colors["vermilion"], ha="center", va="center")
    ax.text(0.500, 0.052, cut["ja"], fontsize=4.75, fontweight="bold", color=colors["ink"], ha="center", va="center")
    ax.text(0.500, 0.038, cut["ja_reading"], fontsize=3.15, color=colors["muted"], ha="center", va="center")
    ax.text(0.500, 0.023, cut["en"], fontsize=3.65, fontweight="bold", color=colors["vermilion"], ha="center", va="center")

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
        "method": "schematic-hakone-itinerary-days-render",
        "command": "python3 scripts/build_hakone_itinerary_days_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": "Map design © LazyTravel; route facts derive from the listed official sources.",
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
    print(f"map: {OUTPUT_STEM.relative_to(ROOT)} (PNG {png_dimensions[0]}x{png_dimensions[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
