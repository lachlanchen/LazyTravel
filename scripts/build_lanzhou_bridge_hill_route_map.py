#!/usr/bin/env python3
"""Build Lanzhou Chapter 4's bridge-to-White-Pagoda-Hill decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-bridge-hill-route.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-bridge-hill-route"
FIXED_TIME = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#24313A",
    "muted": "#63717B",
    "line": "#B6C2CB",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F1FC",
    "vermilion": "#E44736",
    "vermilion_light": "#FCEAE7",
    "jade": "#23836B",
    "jade_light": "#E5F3EE",
    "coral": "#F06E65",
    "coral_light": "#FDECEA",
    "steel": "#54636D",
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
            "svg.hashsalt": "lazytravel-lanzhou-bridge-hill-route-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.05, right=0.95, top=0.97, bottom=0.035)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(
        0,
        0.985,
        f"{title['zh']} · {title['ja']}",
        color=COLORS["ink"],
        fontsize=16.4,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0,
        0.936,
        title["en"],
        color=COLORS["cobalt"],
        fontsize=8.7,
        fontweight="bold",
        va="top",
    )
    ax.text(
        1,
        0.936,
        "SCHEMATIC · NOT NAVIGATION",
        color=COLORS["muted"],
        fontsize=6.3,
        fontweight="bold",
        ha="right",
        va="top",
    )

    ax.add_patch(
        FancyBboxPatch(
            (0, 0.17),
            1,
            0.73,
            boxstyle="round,pad=0.009,rounding_size=0.015",
            facecolor="#F8FAFC",
            edgecolor=COLORS["line"],
            linewidth=1.1,
        )
    )

    hill = Polygon(
        [(0.17, 0.565), (0.09, 0.89), (0.91, 0.89), (0.83, 0.565)],
        closed=True,
        facecolor=COLORS["jade_light"],
        edgecolor=COLORS["jade"],
        linewidth=1.2,
    )
    ax.add_patch(hill)
    for y in (0.68, 0.76, 0.84):
        ax.plot(
            [0.24, 0.39],
            [y, y],
            color=COLORS["jade"],
            lw=1.15,
            alpha=0.75,
        )

    ax.add_patch(Rectangle((0.01, 0.405), 0.98, 0.145, facecolor=COLORS["cobalt_light"], edgecolor="none"))
    ax.annotate(
        "",
        xy=(0.95, 0.535),
        xytext=(0.05, 0.535),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["cobalt"], "lw": 2.4},
    )
    river = config["river"]
    ax.text(
        0.75,
        0.51,
        f"{river['zh']} · {river['ja']} · {river['en']}  {river['flow']}",
        color=COLORS["cobalt"],
        fontsize=7.9,
        fontweight="bold",
        ha="center",
        va="center",
        bbox={"facecolor": COLORS["cobalt_light"], "edgecolor": "none", "pad": 2},
    )

    bridge_x = 0.46
    ax.add_patch(
        Rectangle(
            (bridge_x - 0.044, 0.405),
            0.088,
            0.145,
            facecolor="#F8FAFC",
            edgecolor=COLORS["steel"],
            linewidth=1.5,
        )
    )
    for y in (0.414, 0.442, 0.470, 0.498, 0.526):
        ax.plot(
            [bridge_x - 0.042, bridge_x + 0.042],
            [y, y + 0.024],
            color=COLORS["steel"],
            lw=1.0,
        )
        ax.plot(
            [bridge_x + 0.042, bridge_x - 0.042],
            [y, y + 0.024],
            color=COLORS["steel"],
            lw=1.0,
        )

    ax.plot([bridge_x, bridge_x], [0.225, 0.735], color=COLORS["vermilion"], lw=4.0, solid_capstyle="round")
    ax.annotate(
        "",
        xy=(bridge_x, 0.735),
        xytext=(bridge_x, 0.66),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["vermilion"], "lw": 2.6},
    )
    ax.plot(
        [bridge_x, bridge_x],
        [0.735, 0.855],
        color=COLORS["jade"],
        lw=3.0,
        linestyle=(0, (4, 2)),
        solid_capstyle="round",
    )
    ax.annotate(
        "",
        xy=(bridge_x, 0.855),
        xytext=(bridge_x, 0.79),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["jade"], "lw": 2.2},
    )
    ax.annotate(
        "",
        xy=(0.86, 0.625),
        xytext=(bridge_x + 0.02, 0.625),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["coral"], "lw": 2.5, "linestyle": (0, (4, 2))},
    )

    def draw_stop(stop: dict[str, Any]) -> None:
        x = float(stop["x"])
        y = float(stop["y"])
        side = stop["side"]
        color = COLORS["jade"] if stop["number"] == 5 else COLORS["vermilion"]
        ax.add_patch(Circle((x, y), 0.025, facecolor=color, edgecolor=COLORS["paper"], lw=1.7, zorder=8))
        ax.text(
            x,
            y,
            str(stop["number"]),
            color="white",
            fontsize=8.5,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=9,
        )
        if side == "left":
            label_x, align = x - 0.075, "right"
        else:
            label_x, align = x + 0.075, "left"
        ax.text(
            label_x,
            y + 0.035,
            stop["zh"],
            color=COLORS["ink"],
            fontsize=7.8,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y + 0.014,
            stop["ja"],
            color=COLORS["ink"],
            fontsize=6.7,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y - 0.009,
            stop["en"],
            color=color,
            fontsize=6.1,
            fontweight="bold",
            ha=align,
            va="center",
        )
        ax.text(
            label_x,
            y - 0.041,
            f"{stop['note_zh']}\n{stop['note_ja']}\n{stop['note_en']}",
            color=COLORS["muted"],
            fontsize=5.35,
            ha=align,
            va="center",
            linespacing=1.16,
        )

    for stop in config["stops"]:
        draw_stop(stop)

    branches = config["branches"]
    ax.text(
        0.04,
        0.872,
        f"{config['orientation']['north']} ↑",
        color=COLORS["jade"],
        fontsize=6.4,
        fontweight="bold",
        va="top",
    )
    ax.text(
        0.04,
        0.19,
        f"↓ {config['orientation']['south']}",
        color=COLORS["muted"],
        fontsize=6.4,
        fontweight="bold",
        va="bottom",
    )
    ax.text(
        0.96,
        0.605,
        f"{branches['riverfront']['zh']}\n{branches['riverfront']['ja']}\n{branches['riverfront']['en']}",
        color=COLORS["coral"],
            fontsize=5.9,
        fontweight="bold",
        ha="right",
        va="top",
        linespacing=1.25,
    )

    for x, fill, edge, branch in (
        (0.015, COLORS["vermilion_light"], COLORS["vermilion"], branches["lower"]),
        (0.51, COLORS["jade_light"], COLORS["jade"], branches["full"]),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.075),
                0.475,
                0.072,
                boxstyle="round,pad=0.008,rounding_size=0.012",
                facecolor=fill,
                edgecolor=edge,
                linewidth=1.1,
            )
        )
        ax.text(
            x + 0.02,
            0.132,
            branch["zh"],
            color=COLORS["ink"],
            fontsize=6.15,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.02,
            0.111,
            branch["ja"],
            color=COLORS["ink"],
            fontsize=5.7,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.02,
            0.086,
            branch["en"],
            color=edge,
            fontsize=5.45,
            fontweight="bold",
            va="center",
        )

    ax.text(
        0,
        0.035,
        "CURRENT GATES · PATHS · WEATHER · RIVER CONDITIONS: CHECK TODAY",
        color=COLORS["ink"],
        fontsize=6.1,
        fontweight="bold",
        va="center",
    )
    ax.text(
        1,
        0.012,
        "Map design © LazyTravel · orientation © OpenStreetMap contributors (ODbL)",
        color=COLORS["muted"],
        fontsize=4.9,
        ha="right",
        va="bottom",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "LazyTravel", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    fig.savefig(OUTPUT_STEM.with_suffix(".png"), dpi=300, facecolor=COLORS["paper"], metadata={"Software": "LazyTravel"})
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), facecolor=COLORS["paper"], metadata=metadata)
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(svg_path, facecolor=COLORS["paper"], metadata={"Creator": "LazyTravel", "Date": "2026-08-21"})
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
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
        "asset_id": "asset-lanzhou-bridge-hill-route-map",
        "method": "deterministic-map-render",
        "created_at": config["snapshot_date"],
        "source_config": output_record(CONFIG_PATH),
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": "Map design © LazyTravel; orientation derived from OpenStreetMap under ODbL; historical and current relationships derive from the listed institutional sources.",
        "visual_qa": config["visual_qa"],
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(json.dumps({"outputs": outputs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
