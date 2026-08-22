#!/usr/bin/env python3
"""Build Lanzhou Chapter 7's deterministic three-height choice map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-height-choice.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
FIXED_TIME = datetime(2026, 8, 22, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#24313A",
    "muted": "#63717B",
    "line": "#B6C2CB",
    "panel": "#F4F7FA",
    "city": "#E9EDF1",
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


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def file_record(path: Path) -> dict[str, Any]:
    return {
        "path": display_path(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def verify_external_sources(config: dict[str, Any]) -> None:
    source = config["sources"]["open_guide_lanshan"]
    path = Path(source["path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    if sha256(path) != source["sha256"]:
        raise RuntimeError(f"external plotting lead hash changed: {path}")


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
            "svg.hashsalt": "lazytravel-lanzhou-height-choice-v1",
            "axes.unicode_minus": False,
        }
    )


def rounded_panel(
    ax: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    face: str,
    edge: str,
    linewidth: float = 1.1,
    linestyle: str | tuple[int, tuple[int, ...]] = "solid",
    radius: float = 0.014,
    zorder: int = 1,
) -> None:
    from matplotlib.patches import FancyBboxPatch

    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle=f"round,pad=0.008,rounding_size={radius}",
            facecolor=face,
            edgecolor=edge,
            linewidth=linewidth,
            linestyle=linestyle,
            zorder=zorder,
        )
    )


def marker(ax: Any, x: float, y: float, number: int, color: str) -> None:
    from matplotlib.patches import Circle

    ax.add_patch(
        Circle(
            (x, y),
            0.024,
            facecolor=COLORS[color],
            edgecolor=COLORS["paper"],
            linewidth=1.5,
            zorder=8,
        )
    )
    ax.text(
        x,
        y,
        str(number),
        color="white",
        fontsize=8.0,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=9,
    )


def draw_spatial_panel(ax: Any) -> None:
    import numpy as np
    from matplotlib.patches import Polygon, Rectangle

    rounded_panel(
        ax,
        0.035,
        0.525,
        0.93,
        0.355,
        face=COLORS["panel"],
        edge=COLORS["line"],
        linewidth=0.9,
    )

    ax.text(
        0.065,
        0.852,
        "北岸  NORTH BANK",
        color=COLORS["muted"],
        fontsize=6.4,
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.935,
        0.852,
        "N",
        color=COLORS["ink"],
        fontsize=8.2,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.annotate(
        "",
        xy=(0.935, 0.873),
        xytext=(0.935, 0.835),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["ink"], "lw": 1.4},
    )

    river_x = np.linspace(0.06, 0.94, 220)
    river_y = 0.716 + 0.008 * np.sin((river_x - 0.06) * 3.3 * np.pi)
    ax.plot(river_x, river_y, color=COLORS["cobalt_light"], linewidth=15, zorder=2)
    ax.plot(river_x, river_y, color=COLORS["cobalt"], linewidth=2.7, zorder=3)
    ax.text(
        0.78,
        0.748,
        "黄河  ·  黄河  ·  YELLOW RIVER",
        color=COLORS["cobalt"],
        fontsize=6.8,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=5,
    )

    ax.add_patch(
        Rectangle(
            (0.07, 0.625),
            0.86,
            0.062,
            facecolor=COLORS["city"],
            edgecolor=COLORS["line"],
            linewidth=0.8,
            zorder=1,
        )
    )
    for x, width in ((0.105, 0.035), (0.17, 0.052), (0.255, 0.03), (0.34, 0.06),
                     (0.455, 0.04), (0.54, 0.065), (0.655, 0.04), (0.75, 0.055),
                     (0.855, 0.03)):
        ax.add_patch(
            Rectangle(
                (x, 0.642),
                width,
                0.026,
                facecolor=COLORS["paper"],
                edgecolor=COLORS["line"],
                linewidth=0.55,
                zorder=2,
            )
        )
    ax.text(
        0.5,
        0.656,
        "市区东西展开  ·  市街は東西へ  ·  CITY EXTENDS EAST–WEST",
        color=COLORS["ink"],
        fontsize=6.6,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=4,
    )

    ax.plot([0.29, 0.29], [0.682, 0.744], color=COLORS["ink"], linewidth=3.0, zorder=5)
    ax.plot([0.275, 0.305], [0.689, 0.689], color=COLORS["ink"], linewidth=1.4, zorder=5)
    ax.plot([0.275, 0.305], [0.705, 0.705], color=COLORS["ink"], linewidth=1.4, zorder=5)
    ax.plot([0.275, 0.305], [0.721, 0.721], color=COLORS["ink"], linewidth=1.4, zorder=5)
    ax.text(
        0.29,
        0.695,
        "中山桥  ·  中山橋  ·  BRIDGE",
        color=COLORS["ink"],
        fontsize=5.9,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=6,
    )

    north_hill = Polygon(
        [[0.16, 0.759], [0.25, 0.837], [0.34, 0.759]],
        closed=True,
        facecolor=COLORS["vermilion_light"],
        edgecolor=COLORS["vermilion"],
        linewidth=1.4,
        zorder=4,
    )
    ax.add_patch(north_hill)
    marker(ax, 0.25, 0.797, 1, "vermilion")
    ax.text(
        0.39,
        0.805,
        "白塔山\n白塔山\nWHITE PAGODA",
        color=COLORS["ink"],
        fontsize=6.7,
        fontweight="bold",
        va="center",
    )

    south_base = Polygon(
        [[0.1, 0.545], [0.33, 0.615], [0.52, 0.545]],
        closed=True,
        facecolor=COLORS["jade_light"],
        edgecolor=COLORS["jade"],
        linewidth=1.4,
        zorder=4,
    )
    ax.add_patch(south_base)
    marker(ax, 0.32, 0.576, 3, "jade")
    ax.text(
        0.14,
        0.572,
        "五泉山\n五泉山\nWUQUAN",
        color=COLORS["ink"],
        fontsize=6.7,
        fontweight="bold",
        va="center",
        zorder=7,
    )

    south_high = Polygon(
        [[0.5, 0.545], [0.71, 0.625], [0.92, 0.545]],
        closed=True,
        facecolor=COLORS["coral_light"],
        edgecolor=COLORS["coral"],
        linewidth=1.4,
        zorder=4,
    )
    ax.add_patch(south_high)
    marker(ax, 0.71, 0.584, 2, "coral")
    ax.text(
        0.765,
        0.586,
        "兰山·三台阁\n蘭山・三台閣\nLANSHAN · SANTAI",
        color=COLORS["ink"],
        fontsize=6.1,
        fontweight="bold",
        va="center",
        zorder=7,
    )

    ax.text(
        0.5,
        0.536,
        "南侧高度已概化 · NO THROUGH-ROUTE SHOWN · 南側の高所は模式化",
        color=COLORS["muted"],
        fontsize=5.8,
        fontweight="bold",
        ha="center",
        va="center",
    )


def draw_choice_cards(ax: Any, config: dict[str, Any]) -> None:
    card_xs = [0.035, 0.35, 0.665]
    for choice, x in zip(config["choices"], card_xs):
        color = choice["color"]
        rounded_panel(
            ax,
            x,
            0.285,
            0.30,
            0.205,
            face=COLORS[f"{color}_light"],
            edge=COLORS[color],
            linewidth=1.2,
        )
        marker(ax, x + 0.035, 0.463, choice["number"], color)
        ax.text(
            x + 0.068,
            0.47,
            choice["zh"],
            color=COLORS["ink"],
            fontsize=8.35,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.068,
            0.441,
            choice["ja"],
            color=COLORS["ink"],
            fontsize=6.55,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.068,
            0.414,
            choice["en"],
            color=COLORS[color],
            fontsize=6.4,
            fontweight="bold",
            va="center",
        )
        ax.plot(
            [x + 0.025, x + 0.275],
            [0.386, 0.386],
            color=COLORS[color],
            linewidth=0.8,
            alpha=0.75,
        )
        ax.text(
            x + 0.025,
            0.362,
            "折返点 · 折り返し · STOP",
            color=COLORS["muted"],
            fontsize=6.4,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.025,
            0.335,
            choice["stop_zh"],
            color=COLORS["ink"],
            fontsize=7.1,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.025,
            0.311,
            choice["stop_ja"],
            color=COLORS["ink"],
            fontsize=6.4,
            va="center",
        )
        ax.text(
            x + 0.025,
            0.291,
            choice["stop_en"],
            color=COLORS[color],
            fontsize=5.9,
            fontweight="bold",
            va="center",
        )


def draw_checks(ax: Any, config: dict[str, Any]) -> None:
    from matplotlib.patches import FancyArrowPatch

    ax.text(
        0.035,
        0.252,
        "入口前四项检查  ·  入口前の四確認  ·  FOUR GO / NO-GO CHECKS",
        color=COLORS["ink"],
        fontsize=7.1,
        fontweight="bold",
        va="center",
    )
    xs = [0.09, 0.35, 0.61, 0.87]
    for index, (check, x) in enumerate(zip(config["checks"], xs)):
        color = check["color"]
        marker(ax, x, 0.19, check["number"], color)
        ax.text(
            x,
            0.154,
            check["zh"],
            color=COLORS["ink"],
            fontsize=7.25,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            x,
            0.129,
            check["ja"],
            color=COLORS["ink"],
            fontsize=6.4,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            x,
            0.105,
            check["en"],
            color=COLORS[color],
            fontsize=5.85,
            fontweight="bold",
            ha="center",
            va="center",
        )
        if index < len(xs) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (x + 0.04, 0.19),
                    (xs[index + 1] - 0.04, 0.19),
                    arrowstyle="-|>",
                    mutation_scale=9,
                    linewidth=1.2,
                    color=COLORS["line"],
                    zorder=2,
                )
            )

    rounded_panel(
        ax,
        0.035,
        0.025,
        0.93,
        0.055,
        face=COLORS["cobalt_light"],
        edge=COLORS["cobalt"],
        linewidth=1.1,
        linestyle=(0, (4, 2)),
    )
    fallback = config["fallback"]
    ax.text(
        0.5,
        0.066,
        fallback["zh"],
        color=COLORS["ink"],
        fontsize=7.05,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.045,
        fallback["ja"],
        color=COLORS["ink"],
        fontsize=6.2,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.027,
        fallback["en"],
        color=COLORS["cobalt"],
        fontsize=5.65,
        fontweight="bold",
        ha="center",
        va="center",
    )


def render(config: dict[str, Any]) -> tuple[Any, Any]:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.4, 7.6), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.045, right=0.955, top=0.98, bottom=0.025)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(0, 0.987, title["zh"], color=COLORS["ink"], fontsize=15.2,
            fontweight="bold", va="top")
    ax.text(0, 0.948, title["ja"], color=COLORS["ink"], fontsize=8.6,
            fontweight="bold", va="top")
    ax.text(0, 0.919, title["en"], color=COLORS["cobalt"], fontsize=7.4,
            fontweight="bold", va="top")
    ax.text(1, 0.919, "SCHEMATIC · NOT NAVIGATION", color=COLORS["muted"],
            fontsize=5.8, fontweight="bold", ha="right", va="top")
    ax.text(
        0,
        0.893,
        "先定想看什么，再确认回程  ·  目的と帰路を先に決める  ·  PURPOSE FIRST, RETURN INCLUDED",
        color=COLORS["ink"],
        fontsize=6.4,
        fontweight="bold",
        va="top",
    )

    draw_spatial_panel(ax)
    draw_choice_cards(ax, config)
    draw_checks(ax, config)
    return fig, ax


def save_outputs(config: dict[str, Any]) -> dict[str, Any]:
    import matplotlib.pyplot as plt

    fig, _ = render(config)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = OUTPUT_DIR / config["id"]
    metadata = {"Creator": "LazyTravel", "CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    png_path = stem.with_suffix(".png")
    pdf_path = stem.with_suffix(".pdf")
    svg_path = stem.with_suffix(".svg")
    fig.savefig(
        png_path,
        dpi=300,
        facecolor=COLORS["paper"],
        metadata={"Software": "LazyTravel"},
    )
    fig.savefig(pdf_path, facecolor=COLORS["paper"], metadata=metadata)
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
    return {path.suffix.lstrip("."): file_record(path) for path in (svg_path, pdf_path, png_path)}


def main() -> int:
    config = read_json(CONFIG_PATH)
    verify_external_sources(config)
    configure_matplotlib()
    outputs = save_outputs(config)
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "method": "deterministic-map-render",
        "created_at": config["snapshot_date"],
        "command": "python3 scripts/build_lanzhou_height_choice_map.py",
        "source_config": file_record(CONFIG_PATH),
        "spatial_anchors": config["spatial_anchors"],
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": (
            "Map design © LazyTravel; OSM park anchors are used under ODbL; "
            "the read-only open-guide plotting lead remains attributed under "
            "CC BY-SA 4.0; no basemap tiles are redistributed."
        ),
        "visual_qa": config["visual_qa"],
    }
    provenance_path = OUTPUT_DIR / f"{config['id']}.provenance.json"
    write_json(provenance_path, provenance)
    print(
        json.dumps(
            {"outputs": outputs, "provenance": file_record(provenance_path)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
