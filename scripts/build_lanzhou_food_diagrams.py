#!/usr/bin/env python3
"""Build the two deterministic decision diagrams for Lanzhou Chapter 6."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "data/maps/lanzhou"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
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


def configure_matplotlib() -> None:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Noto Sans CJK SC",
                "Noto Sans CJK JP",
                "Noto Sans",
            ],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-food-diagrams-v1",
            "axes.unicode_minus": False,
        }
    )


def new_canvas(config: dict[str, Any], descriptor: str) -> tuple[Any, Any]:
    import matplotlib.pyplot as plt

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
        descriptor,
        color=COLORS["muted"],
        fontsize=5.8,
        fontweight="bold",
        ha="right",
        va="top",
    )
    return fig, ax


def rounded_panel(
    ax: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    color: str,
    *,
    linestyle: str | tuple[int, tuple[int, ...]] = "solid",
) -> None:
    from matplotlib.patches import FancyBboxPatch

    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.008,rounding_size=0.014",
            facecolor=COLORS[f"{color}_light"],
            edgecolor=COLORS[color],
            linewidth=1.15,
            linestyle=linestyle,
        )
    )


def draw_number(ax: Any, x: float, y: float, number: int, color: str) -> None:
    from matplotlib.patches import Circle

    ax.add_patch(
        Circle(
            (x, y),
            0.029,
            facecolor=COLORS[color],
            edgecolor=COLORS["paper"],
            linewidth=1.6,
            zorder=6,
        )
    )
    ax.text(
        x,
        y,
        str(number),
        color="white",
        fontsize=9.2,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=7,
    )


def draw_arrow(ax: Any, start: tuple[float, float], end: tuple[float, float], color: str) -> None:
    from matplotlib.patches import FancyArrowPatch

    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=2.25,
            color=COLORS[color],
            connectionstyle="arc3,rad=0",
            zorder=3,
        )
    )


def render_order(config: dict[str, Any]) -> tuple[Any, Any]:
    fig, ax = new_canvas(config, "SERVICE FLOW · SHOP SIGNS OVERRIDE THIS PAGE")
    step_ys = [0.79, 0.655, 0.52, 0.385, 0.25]

    for start, end in zip(step_ys, step_ys[1:]):
        draw_arrow(ax, (0.095, start - 0.035), (0.095, end + 0.035), "cobalt")

    for step, y in zip(config["steps"], step_ys):
        color = step["color"]
        rounded_panel(ax, 0.15, y - 0.054, 0.39, 0.108, color)
        draw_number(ax, 0.095, y, step["number"], color)
        ax.text(
            0.175,
            y + 0.027,
            step["zh"],
            color=COLORS["ink"],
            fontsize=8.7,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.175,
            y + 0.002,
            step["ja"],
            color=COLORS["ink"],
            fontsize=6.9,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.175,
            y - 0.022,
            step["en"],
            color=COLORS[color],
            fontsize=6.2,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.175,
            y - 0.044,
            f"{step['note_zh']} · {step['note_ja']}",
            color=COLORS["muted"],
            fontsize=5.55,
            va="center",
        )

    rounded_panel(ax, 0.58, 0.365, 0.38, 0.48, "cobalt")
    ax.text(
        0.61,
        0.815,
        "先看面型名称",
        color=COLORS["ink"],
        fontsize=10.4,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0.61,
        0.783,
        "表示を見分ける · RECOGNISE THE SIGN",
        color=COLORS["cobalt"],
        fontsize=6.25,
        fontweight="bold",
        va="top",
    )

    group_ys = [0.715, 0.59, 0.465]
    group_widths = [2.5, 5.5, 9.5]
    for group, y, line_width in zip(config["shape_groups"], group_ys, group_widths):
        color = group["color"]
        ax.plot(
            [0.615, 0.655],
            [y, y],
            color=COLORS[color],
            linewidth=line_width,
            solid_capstyle="round",
        )
        ax.text(
            0.67,
            y + 0.028,
            f"{group['zh']} · {group['ja']}",
            color=COLORS["ink"],
            fontsize=7.0,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.67,
            y + 0.002,
            group["en"],
            color=COLORS[color],
            fontsize=6.0,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.67,
            y - 0.033,
            "  ·  ".join(group["names"]),
            color=COLORS["ink"],
            fontsize=8.2,
            fontweight="bold",
            va="center",
        )

    notice = config["variation_notice"]
    rounded_panel(ax, 0.03, 0.085, 0.94, 0.095, "coral", linestyle=(0, (4, 2)))
    ax.text(
        0.5,
        0.151,
        notice["zh"],
        color=COLORS["ink"],
        fontsize=7.7,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.121,
        notice["ja"],
        color=COLORS["ink"],
        fontsize=6.5,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.095,
        notice["en"],
        color=COLORS["coral"],
        fontsize=5.8,
        fontweight="bold",
        ha="center",
        va="center",
    )
    return fig, ax


def render_clock(config: dict[str, Any]) -> tuple[Any, Any]:
    fig, ax = new_canvas(config, "DAY PHASES · NOT OPENING HOURS")
    phase_ys = [0.79, 0.625, 0.435, 0.205]

    for start, end in zip(phase_ys, phase_ys[1:]):
        draw_arrow(ax, (0.115, start - 0.037), (0.115, end + 0.037), "cobalt")

    for phase, y in zip(config["phases"], phase_ys):
        color = phase["color"]
        height = 0.12 if phase["number"] != 3 else 0.23
        rounded_panel(ax, 0.19, y - height / 2, 0.77, height, color)
        draw_number(ax, 0.115, y, phase["number"], color)
        title_offset = 0.06 if phase["number"] == 3 else 0.035
        ax.text(
            0.225,
            y + title_offset,
            phase["zh"],
            color=COLORS["ink"],
            fontsize=10.0,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.225,
            y + title_offset - 0.03,
            phase["ja"],
            color=COLORS["ink"],
            fontsize=7.3,
            fontweight="bold",
            va="center",
        )
        ax.text(
            0.225,
            y + title_offset - 0.059,
            phase["en"],
            color=COLORS[color],
            fontsize=6.5,
            fontweight="bold",
            va="center",
        )
        if phase["number"] != 3:
            ax.text(
                0.225,
                y + title_offset - 0.087,
                f"{phase['note_zh']} · {phase['note_ja']}",
                color=COLORS["muted"],
                fontsize=5.75,
                va="center",
            )

    choice_xs = [0.225, 0.585]
    for choice, x in zip(config["afternoon_choices"], choice_xs):
        color = choice["color"]
        rounded_panel(ax, x, 0.33, 0.33, 0.075, color, linestyle=(0, (3, 2)))
        ax.text(
            x + 0.165,
            0.385,
            f"{choice['zh']} · {choice['ja']}",
            color=COLORS["ink"],
            fontsize=5.85,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.165,
            0.36,
            choice["en"],
            color=COLORS[color],
            fontsize=5.55,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.165,
            0.338,
            choice["items"],
            color=COLORS["ink"],
            fontsize=5.8,
            ha="center",
            va="center",
        )

    fallback = config["fallback"]
    rounded_panel(ax, 0.03, 0.05, 0.94, 0.08, "cobalt", linestyle=(0, (4, 2)))
    ax.text(
        0.5,
        0.108,
        fallback["zh"],
        color=COLORS["ink"],
        fontsize=7.7,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.081,
        fallback["ja"],
        color=COLORS["ink"],
        fontsize=6.45,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.058,
        fallback["en"],
        color=COLORS["cobalt"],
        fontsize=5.75,
        fontweight="bold",
        ha="center",
        va="center",
    )
    return fig, ax


def save_outputs(config: dict[str, Any], renderer: Callable[[dict[str, Any]], tuple[Any, Any]]) -> dict[str, Any]:
    import matplotlib.pyplot as plt

    fig, ax = renderer(config)
    ax.text(
        1,
        0.012,
        "Diagram design © LazyTravel · verify the actual shop and day",
        color=COLORS["muted"],
        fontsize=4.55,
        ha="right",
        va="bottom",
    )
    stem = OUTPUT_DIR / config["id"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "LazyTravel", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    fig.savefig(
        stem.with_suffix(".png"),
        dpi=300,
        facecolor=COLORS["paper"],
        metadata={"Software": "LazyTravel"},
    )
    fig.savefig(stem.with_suffix(".pdf"), facecolor=COLORS["paper"], metadata=metadata)
    svg_path = stem.with_suffix(".svg")
    fig.savefig(
        svg_path,
        facecolor=COLORS["paper"],
        metadata={"Creator": "LazyTravel", "Date": "2026-08-22"},
    )
    svg_path.write_text(
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)

    outputs = {
        path.suffix.lstrip("."): output_record(path)
        for path in (
            stem.with_suffix(".svg"),
            stem.with_suffix(".pdf"),
            stem.with_suffix(".png"),
        )
    }
    config_path = CONFIG_DIR / f"{config['id']}.config.json"
    provenance = {
        "schema_version": 1,
        "asset_id": f"asset-{config['id']}-diagram",
        "method": "deterministic-map-render",
        "created_at": config["snapshot_date"],
        "source_config": output_record(config_path),
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": "Diagram design © LazyTravel; factual relationships derive from the listed sources.",
        "visual_qa": config["visual_qa"],
    }
    write_json(stem.with_suffix(".provenance.json"), provenance)
    return outputs


def main() -> int:
    configure_matplotlib()
    jobs = {
        "lanzhou-noodle-order": render_order,
        "lanzhou-food-clock": render_clock,
    }
    results = {}
    for config_id, renderer in jobs.items():
        config = read_json(CONFIG_DIR / f"{config_id}.config.json")
        results[config_id] = save_outputs(config, renderer)
    print(json.dumps({"outputs": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
