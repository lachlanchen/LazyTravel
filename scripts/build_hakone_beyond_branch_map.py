#!/usr/bin/env python3
"""Build Hakone Chapter 11's three-branch onward-choice map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-beyond-branch.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-beyond-branch"
FIXED_TIME = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
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
            "svg.hashsalt": "lazytravel-hakone-beyond-branch-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    colors = {
        "ink": "#13242F",
        "muted": "#536774",
        "paper": "#FBFDFF",
        "line": "#A8BBC7",
        "white": "#FFFFFF",
        "vermilion": "#E84A2A",
        "vermilion_fill": "#FFF0EB",
        "jade": "#008B72",
        "jade_fill": "#E7F8F2",
        "cobalt": "#1769D8",
        "cobalt_fill": "#EAF2FF",
        "coral": "#D83D67",
        "coral_fill": "#FFF0F4",
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
        0.951,
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
        fontsize=6.7,
        fontweight="bold",
        color=colors["cobalt"],
        ha="left",
        va="top",
    )

    gate = config["gate"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.817),
            0.95,
            0.083,
            boxstyle="round,pad=0.007,rounding_size=0.014",
            facecolor=colors["cobalt_fill"],
            edgecolor=colors["cobalt"],
            linewidth=1.2,
        )
    )
    ax.text(
        0.045,
        0.883,
        gate["zh"],
        fontsize=8.0,
        fontweight="bold",
        color=colors["ink"],
        ha="left",
        va="center",
    )
    ax.text(
        0.045,
        0.865,
        gate["zh_reading"],
        fontsize=4.9,
        color=colors["cobalt"],
        ha="left",
        va="center",
    )
    ax.text(
        0.045,
        0.846,
        gate["ja"],
        fontsize=6.7,
        fontweight="bold",
        color=colors["ink"],
        ha="left",
        va="center",
    )
    ax.text(
        0.045,
        0.829,
        gate["ja_reading"],
        fontsize=4.5,
        color=colors["muted"],
        ha="left",
        va="center",
    )
    ax.text(
        0.955,
        0.824,
        gate["en"],
        fontsize=4.5,
        fontweight="bold",
        color=colors["cobalt"],
        ha="right",
        va="center",
    )

    column_x = (0.225, 0.420, 0.615, 0.810)
    for heading, x_value in zip(config["columns"], column_x, strict=True):
        ax.text(
            x_value,
            0.795,
            heading["zh"],
            fontsize=6.0,
            fontweight="bold",
            color=colors["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            x_value,
            0.781,
            heading["ja"],
            fontsize=5.0,
            fontweight="bold",
            color=colors["muted"],
            ha="center",
            va="center",
        )
        ax.text(
            x_value,
            0.768,
            heading["en"],
            fontsize=4.0,
            fontweight="bold",
            color=colors["cobalt"],
            ha="center",
            va="center",
        )

    lane_y = (0.572, 0.355, 0.138)
    lane_height = 0.198
    node_width = 0.172
    node_left = (0.139, 0.334, 0.529, 0.724)

    for branch, y in zip(config["branches"], lane_y, strict=True):
        accent = colors[branch["color"]]
        fill = colors[f"{branch['color']}_fill"]
        ax.add_patch(
            FancyBboxPatch(
                (0.025, y),
                0.95,
                lane_height,
                boxstyle="round,pad=0.006,rounding_size=0.014",
                facecolor=colors["white"],
                edgecolor=accent,
                linewidth=1.25,
            )
        )

        destination = branch["destination"]
        ax.add_patch(
            FancyBboxPatch(
                (0.037, y + 0.068),
                0.090,
                0.118,
                boxstyle="round,pad=0.004,rounding_size=0.010",
                facecolor=fill,
                edgecolor=accent,
                linewidth=1.0,
            )
        )
        ax.text(
            0.082,
            y + 0.165,
            destination["zh"],
            fontsize=8.7,
            fontweight="bold",
            color=colors["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            0.082,
            y + 0.143,
            destination["zh_reading"],
            fontsize=5.0,
            color=accent,
            ha="center",
            va="center",
        )
        ax.text(
            0.082,
            y + 0.119,
            destination["ja"],
            fontsize=7.2,
            fontweight="bold",
            color=colors["ink"],
            ha="center",
            va="center",
        )
        ax.text(
            0.082,
            y + 0.097,
            destination["ja_reading"],
            fontsize=4.8,
            color=colors["muted"],
            ha="center",
            va="center",
        )
        ax.text(
            0.082,
            y + 0.076,
            destination["en"],
            fontsize=4.8,
            fontweight="bold",
            color=accent,
            ha="center",
            va="center",
        )

        for index, (node, left) in enumerate(zip(branch["nodes"], node_left, strict=True)):
            ax.add_patch(
                FancyBboxPatch(
                    (left, y + 0.068),
                    node_width,
                    0.118,
                    boxstyle="round,pad=0.004,rounding_size=0.010",
                    facecolor=fill,
                    edgecolor=accent,
                    linewidth=0.9,
                )
            )
            center = left + node_width / 2
            ax.text(
                center,
                y + 0.165,
                node["zh"],
                fontsize=7.0,
                fontweight="bold",
                color=colors["ink"],
                ha="center",
                va="center",
            )
            ax.text(
                center,
                y + 0.145,
                node["zh_reading"],
                fontsize=4.0,
                color=accent,
                ha="center",
                va="center",
            )
            ax.text(
                center,
                y + 0.122,
                node["ja"],
                fontsize=5.8,
                fontweight="bold",
                color=colors["ink"],
                ha="center",
                va="center",
            )
            ax.text(
                center,
                y + 0.102,
                node["ja_reading"],
                fontsize=3.95,
                color=colors["muted"],
                ha="center",
                va="center",
            )
            ax.text(
                center,
                y + 0.080,
                node["en"],
                fontsize=4.0,
                fontweight="bold",
                color=accent,
                ha="center",
                va="center",
            )
            if index < len(branch["nodes"]) - 1:
                ax.add_patch(
                    FancyArrowPatch(
                        (left + node_width + 0.003, y + 0.127),
                        (node_left[index + 1] - 0.004, y + 0.127),
                        arrowstyle="-|>",
                        mutation_scale=8,
                        color=accent,
                        linewidth=1.15,
                        zorder=5,
                    )
                )

        constraint = branch["constraint"]
        ax.add_patch(
            FancyBboxPatch(
                (0.139, y + 0.010),
                0.850,
                0.047,
                boxstyle="round,pad=0.003,rounding_size=0.008",
                facecolor=colors["paper"],
                edgecolor=accent,
                linewidth=0.85,
                linestyle=(0, (3, 2)),
            )
        )
        ax.text(
            0.155,
            y + 0.044,
            constraint["zh"],
            fontsize=5.6,
            fontweight="bold",
            color=colors["ink"],
            ha="left",
            va="center",
        )
        ax.text(
            0.155,
            y + 0.028,
            constraint["zh_reading"],
            fontsize=3.8,
            color=accent,
            ha="left",
            va="center",
        )
        ax.text(
            0.975,
            y + 0.044,
            constraint["ja"],
            fontsize=5.0,
            fontweight="bold",
            color=colors["ink"],
            ha="right",
            va="center",
        )
        ax.text(
            0.975,
            y + 0.028,
            constraint["ja_reading"],
            fontsize=3.7,
            color=colors["muted"],
            ha="right",
            va="center",
        )
        ax.text(
            0.565,
            y + 0.014,
            constraint["en"],
            fontsize=3.7,
            fontweight="bold",
            color=accent,
            ha="center",
            va="center",
        )

    final_rule = config["final_rule"]
    ax.add_patch(
        FancyBboxPatch(
            (0.025, 0.022),
            0.95,
            0.098,
            boxstyle="round,pad=0.006,rounding_size=0.012",
            facecolor=colors["coral_fill"],
            edgecolor=colors["coral"],
            linewidth=1.1,
        )
    )
    ax.text(
        0.500,
        0.105,
        final_rule["zh"],
        fontsize=5.5,
        fontweight="bold",
        color=colors["ink"],
        ha="center",
        va="center",
    )
    ax.text(
        0.500,
        0.085,
        final_rule["zh_reading"],
        fontsize=3.7,
        color=colors["coral"],
        ha="center",
        va="center",
    )
    ax.text(
        0.500,
        0.064,
        final_rule["ja"],
        fontsize=4.9,
        fontweight="bold",
        color=colors["ink"],
        ha="center",
        va="center",
    )
    ax.text(
        0.500,
        0.046,
        final_rule["ja_reading"],
        fontsize=3.55,
        color=colors["muted"],
        ha="center",
        va="center",
    )
    ax.text(
        0.500,
        0.029,
        final_rule["en"],
        fontsize=3.8,
        fontweight="bold",
        color=colors["coral"],
        ha="center",
        va="center",
    )

    ax.text(
        0.500,
        0.004,
        config["footer"],
        fontsize=3.6,
        color=colors["muted"],
        ha="center",
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
        "method": "schematic-hakone-beyond-branch-render",
        "command": "python3 scripts/build_hakone_beyond_branch_map.py",
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
