#!/usr/bin/env python3
"""Build Lanzhou Chapter 8's deterministic lodging-segment map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-stay-segment.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
FIXED_TIME = datetime(2026, 8, 22, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#24313A",
    "muted": "#65727B",
    "line": "#B7C4CD",
    "panel": "#F3F7FA",
    "river": "#1769D2",
    "river_light": "#E6F1FC",
    "jade": "#23836B",
    "jade_light": "#E4F3ED",
    "vermilion": "#E44736",
    "vermilion_light": "#FCE9E6",
    "cobalt": "#1769D2",
    "cobalt_light": "#E6F1FC",
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


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def verify_inputs(config: dict[str, Any]) -> None:
    source = config["sources"]["accepted_arrival_map"]
    path = ROOT / source["path"]
    if not path.is_file():
        raise FileNotFoundError(path)
    if sha256(path) != source["sha256"]:
        raise RuntimeError(f"accepted arrival-map config changed: {path}")


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
            "svg.hashsalt": "lazytravel-lanzhou-stay-segment-v1",
            "axes.unicode_minus": False,
        }
    )


def panel(
    ax: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    face: str,
    edge: str,
    linewidth: float = 1.0,
    radius: float = 0.014,
    linestyle: str = "solid",
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
            0.022,
            facecolor=COLORS[color],
            edgecolor=COLORS["paper"],
            linewidth=1.4,
            zorder=8,
        )
    )
    ax.text(
        x,
        y,
        str(number),
        color="white",
        fontsize=8.2,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=9,
    )


def draw_orientation(ax: Any, config: dict[str, Any]) -> None:
    from matplotlib.patches import Rectangle

    panel(
        ax,
        0.045,
        0.555,
        0.91,
        0.315,
        face=COLORS["panel"],
        edge=COLORS["line"],
        linewidth=0.9,
    )

    airport = config["segments"][3]
    panel(
        ax,
        0.57,
        0.79,
        0.34,
        0.055,
        face=COLORS["coral_light"],
        edge=COLORS["coral"],
        linewidth=1.2,
        linestyle="dashed",
        zorder=4,
    )
    marker(ax, 0.60, 0.817, airport["number"], airport["color"])
    ax.text(
        0.63,
        0.823,
        f"{airport['label_zh']} · {airport['label_ja']} · {airport['label_en']}",
        color=COLORS["ink"],
        fontsize=7.4,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=6,
    )
    ax.text(
        0.63,
        0.802,
        "中川机场T3 · 中川空港T3 · NOT TO SCALE",
        color=COLORS["muted"],
        fontsize=6.3,
        ha="left",
        va="center",
        zorder=6,
    )
    ax.plot(
        [0.08, 0.92],
        [0.74, 0.74],
        color=COLORS["river_light"],
        linewidth=16,
        solid_capstyle="round",
        zorder=2,
    )
    ax.plot(
        [0.08, 0.92],
        [0.74, 0.74],
        color=COLORS["river"],
        linewidth=2.5,
        solid_capstyle="round",
        zorder=3,
    )
    ax.text(
        0.16,
        0.763,
        "黄河 · 黄河 · YELLOW RIVER",
        color=COLORS["river"],
        fontsize=6.8,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=5,
    )

    starts = [0.075, 0.36, 0.645]
    width = 0.28
    city_segments = config["segments"][:3]
    for segment, x in zip(city_segments, starts, strict=True):
        color = segment["color"]
        ax.add_patch(
            Rectangle(
                (x, 0.585),
                width,
                0.115,
                facecolor=COLORS[f"{color}_light"],
                edgecolor=COLORS[color],
                linewidth=1.25,
                zorder=3,
            )
        )
        marker(ax, x + 0.032, 0.674, segment["number"], color)
        ax.text(
            x + 0.061,
            0.678,
            f"{segment['label_zh']} · {segment['label_ja']} · {segment['label_en']}",
            color=COLORS[color],
            fontsize=8.1,
            fontweight="bold",
            ha="left",
            va="center",
            zorder=6,
        )
        ax.text(
            x + width / 2,
            0.649,
            segment["anchors_zh"],
            color=COLORS["ink"],
            fontsize=7.0,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=6,
        )
        ax.text(
            x + width / 2,
            0.624,
            segment["anchors_ja"],
            color=COLORS["ink"],
            fontsize=6.7,
            ha="center",
            va="center",
            zorder=6,
        )
        ax.text(
            x + width / 2,
            0.599,
            segment["anchors_en"],
            color=COLORS["muted"],
            fontsize=5.9,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=6,
        )

    ax.annotate(
        "",
        xy=(0.92, 0.56),
        xytext=(0.08, 0.56),
        arrowprops={"arrowstyle": "-|>", "color": COLORS["ink"], "lw": 1.4},
    )
    ax.text(
        0.08,
        0.539,
        "西  WEST",
        color=COLORS["muted"],
        fontsize=6.5,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0.92,
        0.539,
        "EAST  东",
        color=COLORS["muted"],
        fontsize=6.5,
        fontweight="bold",
        ha="right",
        va="center",
    )


def draw_choice_cards(ax: Any, config: dict[str, Any]) -> None:
    positions = [(0.05, 0.345), (0.515, 0.345), (0.05, 0.175), (0.515, 0.175)]
    for segment, (x, y) in zip(config["segments"], positions, strict=True):
        color = segment["color"]
        panel(
            ax,
            x,
            y,
            0.435,
            0.135,
            face=COLORS[f"{color}_light"],
            edge=COLORS[color],
            linewidth=1.25,
        )
        marker(ax, x + 0.033, y + 0.103, segment["number"], color)
        ax.text(
            x + 0.065,
            y + 0.106,
            f"{segment['label_zh']} · {segment['label_ja']} · {segment['label_en']}",
            color=COLORS[color],
            fontsize=7.7,
            fontweight="bold",
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.025,
            y + 0.073,
            segment["choose_zh"],
            color=COLORS["ink"],
            fontsize=6.9,
            fontweight="bold",
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.025,
            y + 0.049,
            segment["choose_ja"],
            color=COLORS["ink"],
            fontsize=6.5,
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.025,
            y + 0.027,
            segment["choose_en"],
            color=COLORS["muted"],
            fontsize=5.7,
            fontweight="bold",
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.41,
            y + 0.007,
            segment["boundary_en"],
            color=COLORS[color],
            fontsize=5.2,
            fontweight="bold",
            ha="right",
            va="bottom",
        )


def render(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    import matplotlib.pyplot as plt

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = OUTPUT_DIR / "lanzhou-stay-segment"
    fig = plt.figure(figsize=(5.4, 7.6), dpi=300, facecolor=COLORS["paper"])
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.05,
        0.947,
        config["title"]["zh"],
        color=COLORS["ink"],
        fontsize=15.0,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0.05,
        0.914,
        f"{config['title']['ja']}  ·  {config['title']['en']}",
        color=COLORS["muted"],
        fontsize=8.3,
        fontweight="bold",
        ha="left",
        va="center",
    )
    draw_orientation(ax, config)
    draw_choice_cards(ax, config)

    panel(
        ax,
        0.05,
        0.075,
        0.90,
        0.06,
        face=COLORS["ink"],
        edge=COLORS["ink"],
        linewidth=0,
    )
    ax.text(
        0.5,
        0.111,
        config["rule"]["zh"],
        color="white",
        fontsize=7.5,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.086,
        f"{config['rule']['ja']}  ·  {config['rule']['en']}",
        color="white",
        fontsize=5.9,
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.035,
        "SCHEMATIC · NO HOTEL PINS · VERIFY LIVE ROUTES AND THE EXACT BOOKING",
        color=COLORS["muted"],
        fontsize=5.8,
        fontweight="bold",
        ha="center",
        va="center",
    )

    metadata = {
        "Title": "LazyTravel Lanzhou lodging-segment map",
        "Author": "LazyTravel / lazying.art",
        "Subject": "Original route-segment schematic for a B6 pocket guide",
        "Keywords": "Lanzhou, lodging, route segment, LazyTravel",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    outputs: dict[str, dict[str, Any]] = {}
    for suffix, options in {
        "svg": {"format": "svg"},
        "pdf": {"format": "pdf", "metadata": metadata},
        "png": {
            "format": "png",
            "dpi": 300,
            "metadata": {
                "Title": metadata["Title"],
                "Author": metadata["Author"],
                "Subject": metadata["Subject"],
            },
        },
    }.items():
        path = stem.with_suffix(f".{suffix}")
        fig.savefig(
            path,
            bbox_inches=None,
            pad_inches=0,
            facecolor=COLORS["paper"],
            **options,
        )
        if suffix == "svg":
            normalize_svg(path)
        outputs[suffix] = file_record(path)
    plt.close(fig)
    return outputs


def main() -> int:
    config = read_json(CONFIG_PATH)
    verify_inputs(config)
    configure_matplotlib()
    outputs = render(config)
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "deterministic-matplotlib-route-segment-schematic",
        "generator": "scripts/build_lanzhou_stay_segment_map.py",
        "config": {**file_record(CONFIG_PATH)},
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": (
            "Original LazyTravel diagram; no third-party map tiles or hotel "
            "imagery redistributed."
        ),
        "visual_qa": config["visual_qa"],
    }
    provenance_path = OUTPUT_DIR / "lanzhou-stay-segment.provenance.json"
    write_json(provenance_path, provenance)
    for suffix, record in outputs.items():
        print(f"{suffix}: {record['path']} ({record['sha256']})")
    print(f"provenance: {display_path(provenance_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
