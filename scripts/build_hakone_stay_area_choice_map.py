#!/usr/bin/env python3
"""Build Hakone Chapter 9's five-zone lodging decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-stay-area-choice.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-stay-area-choice"
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
            "svg.hashsalt": "lazytravel-hakone-stay-area-choice-v1",
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
        "berry": "#A43A78",
        "berry_fill": "#FAEFF7",
        "line": "#9FB7C5",
    }

    fig, ax = plt.subplots(figsize=(7, 5.6), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.025, right=0.975, top=0.84, bottom=0.025)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(
        0.04,
        0.967,
        config["title"]["zh"],
        fontsize=14.5,
        fontweight="bold",
        color=colors["ink"],
    )
    fig.text(
        0.04,
        0.921,
        config["title"]["ja"],
        fontsize=10.6,
        fontweight="bold",
        color=colors["ink"],
    )
    fig.text(
        0.04,
        0.879,
        config["title"]["en"],
        fontsize=8.8,
        fontweight="bold",
        color=colors["cobalt"],
    )
    fig.text(
        0.965,
        0.96,
        config["flow"]["label"],
        fontsize=7.0,
        fontweight="bold",
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.12,
    )

    flow_y = 0.935
    flow_x = (0.26, 0.50, 0.74)
    for index, item in enumerate(config["flow"]["steps"]):
        x_value = flow_x[index]
        ax.add_patch(
            Circle(
                (x_value, flow_y),
                radius=0.054,
                facecolor=colors[f"{item['color']}_fill"],
                edgecolor=colors[item["color"]],
                linewidth=1.35,
                zorder=3,
            )
        )
        ax.text(
            x_value,
            flow_y + 0.017,
            item["zh"],
            fontsize=7.7,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )
        ax.text(
            x_value,
            flow_y - 0.018,
            item["en"],
            fontsize=5.2,
            color=colors[item["color"]],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )

    def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=10,
                color=colors["line"],
                linewidth=1.8,
                shrinkA=2,
                shrinkB=2,
                zorder=2,
            )
        )

    arrow((flow_x[0] + 0.066, flow_y), (flow_x[1] - 0.066, flow_y))
    arrow((flow_x[1] + 0.066, flow_y), (flow_x[2] - 0.066, flow_y))

    slots = [
        (0.025, 0.625, 0.300, 0.245),
        (0.350, 0.625, 0.300, 0.245),
        (0.675, 0.625, 0.300, 0.245),
        (0.085, 0.335, 0.390, 0.245),
        (0.525, 0.335, 0.390, 0.245),
    ]
    for zone, (x_value, y_value, card_width, card_height) in zip(
        config["zones"], slots, strict=True
    ):
        accent = colors[zone["color"]]
        fill = colors[f"{zone['color']}_fill"]
        ax.add_patch(
            FancyBboxPatch(
                (x_value, y_value),
                card_width,
                card_height,
                boxstyle="round,pad=0.008,rounding_size=0.016",
                facecolor=fill,
                edgecolor=accent,
                linewidth=1.35,
                zorder=2,
            )
        )
        ax.add_patch(
            Circle(
                (x_value + 0.032, y_value + card_height - 0.034),
                radius=0.024,
                facecolor=accent,
                edgecolor="none",
                zorder=4,
            )
        )
        ax.text(
            x_value + 0.032,
            y_value + card_height - 0.034,
            zone["number"],
            fontsize=7.3,
            color="#FFFFFF",
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value + card_width / 2,
            y_value + card_height - 0.056,
            zone["zh"],
            fontsize=9.0 if card_width < 0.35 else 9.6,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value + card_width / 2,
            y_value + card_height - 0.094,
            zone["zh_reading"],
            fontsize=5.0 if card_width < 0.35 else 5.2,
            color=accent,
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value + card_width / 2,
            y_value + card_height - 0.135,
            zone["ja"],
            fontsize=7.7 if card_width < 0.35 else 8.1,
            color=colors["ink"],
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value + card_width / 2,
            y_value + card_height - 0.172,
            zone["ja_reading"],
            fontsize=4.75 if card_width < 0.35 else 5.0,
            color=colors["muted"],
            ha="center",
            va="center",
            zorder=5,
        )
        ax.text(
            x_value + card_width / 2,
            y_value + 0.025,
            zone["en"],
            fontsize=5.5 if card_width < 0.35 else 5.9,
            color=accent,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

    decision = config["decision_band"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.035),
            0.95,
            0.245,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            facecolor=colors["cobalt_fill"],
            edgecolor=colors["cobalt"],
            linewidth=1.4,
            zorder=2,
        )
    )
    ax.text(
        0.05,
        0.238,
        decision["zh"],
        fontsize=8.3,
        color=colors["ink"],
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.05,
        0.201,
        decision["zh_reading"],
        fontsize=4.9,
        color=colors["cobalt"],
        va="center",
    )
    ax.text(
        0.05,
        0.160,
        decision["ja"],
        fontsize=7.3,
        color=colors["ink"],
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.05,
        0.123,
        decision["ja_reading"],
        fontsize=4.75,
        color=colors["muted"],
        va="center",
    )
    ax.text(
        0.05,
        0.079,
        decision["en"],
        fontsize=6.2,
        color=colors["cobalt"],
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.95,
        0.046,
        config["footer"],
        fontsize=4.8,
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
        "method": "schematic-hakone-stay-area-choice-render",
        "command": "python3 scripts/build_hakone_stay_area_choice_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": (
            "Map design © LazyTravel; area and transport facts derive from the listed "
            "official sources."
        ),
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
