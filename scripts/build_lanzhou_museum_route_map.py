#!/usr/bin/env python3
"""Build Lanzhou Chapter 5's Gansu Provincial Museum route schematic."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-museum-route.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-museum-route"
FIXED_TIME = datetime(2026, 8, 22, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#24313A",
    "muted": "#63717B",
    "line": "#B6C2CB",
    "panel": "#F4F7FA",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F1FC",
    "vermilion": "#E44736",
    "vermilion_light": "#FCEAE7",
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


def output_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def render_map(config: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-museum-route-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.045, right=0.955, top=0.975, bottom=0.03)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(
        0,
        0.987,
        title["zh"],
        color=COLORS["ink"],
        fontsize=15.2,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0,
        0.948,
        title["ja"],
        color=COLORS["ink"],
        fontsize=8.6,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0,
        0.919,
        title["en"],
        color=COLORS["cobalt"],
        fontsize=7.4,
        fontweight="bold",
        va="top",
    )
    ax.text(
        1,
        0.919,
        "FLOW DIAGRAM · CHECK DISPLAY TODAY",
        color=COLORS["muted"],
        fontsize=5.8,
        fontweight="bold",
        ha="right",
        va="top",
    )

    floor_boxes = {
        "3F": (0.02, 0.625, 0.96, 0.25),
        "2F": (0.02, 0.385, 0.96, 0.205),
        "1F": (0.02, 0.145, 0.96, 0.205),
    }
    floor_colors = {"3F": "vermilion_light", "2F": "jade_light", "1F": "cobalt_light"}
    for floor in config["floors"]:
        label = floor["floor"]
        x, y, width, height = floor_boxes[label]
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                width,
                height,
                boxstyle="round,pad=0.008,rounding_size=0.014",
                facecolor=COLORS[floor_colors[label]],
                edgecolor=COLORS["line"],
                linewidth=1.1,
            )
        )
        ax.text(
            x + 0.025,
            y + height - 0.03,
            label,
            color=COLORS["ink"],
            fontsize=13.5,
            fontweight="bold",
            va="top",
        )

    route_points = {
        1: (0.27, 0.255),
        2: (0.30, 0.755),
        3: (0.72, 0.755),
        4: (0.51, 0.49),
        5: (0.67, 0.255),
    }

    def arrow(start: tuple[float, float], end: tuple[float, float], color: str) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=2.8,
                color=COLORS[color],
                connectionstyle="arc3,rad=0",
                zorder=3,
            )
        )

    arrow((0.27, 0.29), (0.30, 0.715), "cobalt")
    arrow((0.335, 0.755), (0.68, 0.755), "vermilion")
    arrow((0.72, 0.715), (0.53, 0.53), "coral")
    arrow((0.51, 0.45), (0.64, 0.29), "jade")

    stops = {
        stop["number"]: stop
        for floor in config["floors"]
        for stop in floor["stops"]
    }

    def draw_stop(number: int) -> None:
        stop = stops[number]
        x, y = route_points[number]
        color = stop["color"]
        ax.add_patch(
            Circle(
                (x, y),
                0.031,
                facecolor=COLORS[color],
                edgecolor=COLORS["paper"],
                linewidth=1.8,
                zorder=7,
            )
        )
        ax.text(
            x,
            y,
            str(number),
            color="white",
            fontsize=9.4,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=8,
        )
        align = "right" if number in (2, 4) else "left"
        label_x = x - 0.055 if align == "right" else x + 0.055
        ax.text(
            label_x,
            y + 0.033,
            stop["zh"],
            color=COLORS["ink"],
            fontsize=8.7,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y + 0.008,
            stop["ja"],
            color=COLORS["ink"],
            fontsize=7.6,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y - 0.018,
            stop["en"],
            color=COLORS[color],
            fontsize=6.9,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y - 0.052,
            f"{stop['note_zh']}\n{stop['note_ja']}\n{stop['note_en']}",
            color=COLORS["muted"],
            fontsize=6.15,
            ha=align,
            va="center",
            linespacing=1.14,
        )

    for number in range(1, 6):
        draw_stop(number)

    optional = next(floor["optional"] for floor in config["floors"] if "optional" in floor)
    ax.add_patch(
        FancyBboxPatch(
            (0.64, 0.402),
            0.31,
            0.092,
            boxstyle="round,pad=0.007,rounding_size=0.012",
            facecolor=COLORS["paper"],
            edgecolor=COLORS["jade"],
            linestyle=(0, (4, 2)),
            linewidth=1.1,
        )
    )
    ax.text(
        0.795,
        0.472,
        optional["zh"],
        color=COLORS["ink"],
        fontsize=6.7,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.795,
        0.446,
        optional["ja"],
        color=COLORS["ink"],
        fontsize=6.2,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.795,
        0.419,
        optional["en"],
        color=COLORS["jade"],
        fontsize=6.0,
        fontweight="bold",
        ha="center",
        va="center",
    )

    ax.text(
        0,
        0.105,
        "先查当天展厅与文物 · 先確認してから進む · VERIFY BEFORE COMMITTING TO THE ROUTE",
        color=COLORS["ink"],
        fontsize=6.25,
        fontweight="bold",
        va="center",
    )
    ax.text(
        0,
        0.075,
        "No room-level turns · no promised lift, queue, duration, or object display",
        color=COLORS["muted"],
        fontsize=5.8,
        va="center",
    )
    ax.text(
        1,
        0.019,
        "Map design © LazyTravel · floor relationship: Gansu Provincial Museum",
        color=COLORS["muted"],
        fontsize=4.55,
        ha="right",
        va="bottom",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "LazyTravel", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        dpi=300,
        facecolor=COLORS["paper"],
        metadata={"Software": "LazyTravel"},
    )
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), facecolor=COLORS["paper"], metadata=metadata)
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(
        svg_path,
        facecolor=COLORS["paper"],
        metadata={"Creator": "LazyTravel", "Date": "2026-08-22"},
    )
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def main() -> int:
    config = read_json(CONFIG_PATH)
    render_map(config)
    outputs = {
        path.suffix.lstrip("."): output_record(path)
        for path in (
            OUTPUT_STEM.with_suffix(".svg"),
            OUTPUT_STEM.with_suffix(".pdf"),
            OUTPUT_STEM.with_suffix(".png"),
        )
    }
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-lanzhou-museum-route-map",
        "method": "deterministic-map-render",
        "created_at": config["snapshot_date"],
        "source_config": output_record(CONFIG_PATH),
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": "Map design © LazyTravel; floor relationships derive from the current Gansu Provincial Museum guide.",
        "visual_qa": config["visual_qa"],
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(json.dumps({"outputs": outputs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
