#!/usr/bin/env python3
"""Build Lanzhou Chapter 9's deterministic itinerary decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-itinerary-days.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-itinerary-days"
FIXED_TIME = datetime(2026, 8, 23, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#20303A",
    "muted": "#5D6B74",
    "line": "#B8C5CE",
    "white": "#FFFFFF",
    "vermilion": "#E44736",
    "vermilion_light": "#FDE9E6",
    "jade": "#16836B",
    "jade_light": "#E4F4EE",
    "cobalt": "#1769D2",
    "cobalt_light": "#E7F0FC",
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


def file_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def verify_inputs(config: dict[str, Any]) -> None:
    for record in config["accepted_inputs"]:
        path = ROOT / record["path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        if sha256(path) != record["sha256"]:
            raise RuntimeError(f"accepted map input changed: {record['path']}")


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
            "svg.hashsalt": "lazytravel-lanzhou-itinerary-days-v1",
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
    radius: float = 0.012,
    linestyle: str = "solid",
    zorder: int = 1,
) -> None:
    from matplotlib.patches import FancyBboxPatch

    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle=f"round,pad=0.006,rounding_size={radius}",
            facecolor=face,
            edgecolor=edge,
            linewidth=linewidth,
            linestyle=linestyle,
            zorder=zorder,
        )
    )


def draw_label_stack(
    ax: Any,
    center_x: float,
    top_y: float,
    value: dict[str, str],
    accent: str,
    *,
    main_size: float = 7.8,
    english_size: float = 5.0,
) -> None:
    ax.text(
        center_x,
        top_y,
        value["zh"],
        color=COLORS["ink"],
        fontsize=main_size,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=8,
    )
    ax.text(
        center_x,
        top_y - 0.019,
        value["zh_reading"],
        color=accent,
        fontsize=4.55,
        ha="center",
        va="center",
        zorder=8,
    )
    ax.text(
        center_x,
        top_y - 0.040,
        value["ja"],
        color=COLORS["ink"],
        fontsize=6.6,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=8,
    )
    ax.text(
        center_x,
        top_y - 0.059,
        value["ja_reading"],
        color=COLORS["muted"],
        fontsize=4.2,
        ha="center",
        va="center",
        zorder=8,
    )
    ax.text(
        center_x,
        top_y - 0.078,
        value["en"],
        color=accent,
        fontsize=english_size,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=8,
    )


def draw_lane(ax: Any, lane: dict[str, Any], y: float) -> None:
    from matplotlib.patches import FancyArrowPatch

    accent = COLORS[lane["color"]]
    light = COLORS[f"{lane['color']}_light"]
    panel(
        ax,
        0.035,
        y,
        0.93,
        0.195,
        face=COLORS["white"],
        edge=accent,
        linewidth=1.3,
    )
    panel(
        ax,
        0.045,
        y + 0.070,
        0.118,
        0.111,
        face=light,
        edge=accent,
        linewidth=1.1,
    )
    label = lane["label"]
    ax.text(
        0.104,
        y + 0.158,
        label["zh"],
        color=COLORS["ink"],
        fontsize=9.2,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.104,
        y + 0.137,
        label["zh_reading"],
        color=accent,
        fontsize=5.0,
        ha="center",
        va="center",
    )
    ax.text(
        0.104,
        y + 0.112,
        label["ja"],
        color=COLORS["ink"],
        fontsize=7.2,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.104,
        y + 0.091,
        label["ja_reading"],
        color=COLORS["muted"],
        fontsize=4.6,
        ha="center",
        va="center",
    )
    ax.text(
        0.104,
        y + 0.074,
        label["en"],
        color=accent,
        fontsize=5.5,
        fontweight="bold",
        ha="center",
        va="center",
    )

    node_lefts = (0.177, 0.376, 0.575, 0.774)
    node_width = 0.175
    for index, (node, left) in enumerate(zip(lane["nodes"], node_lefts, strict=True)):
        edge = COLORS["coral"] if node.get("choice") else accent
        face = COLORS["coral_light"] if node.get("choice") else light
        linewidth = 1.45 if node.get("choice") else 0.95
        panel(
            ax,
            left,
            y + 0.070,
            node_width,
            0.111,
            face=face,
            edge=edge,
            linewidth=linewidth,
            radius=0.009,
            zorder=4,
        )
        draw_label_stack(
            ax,
            left + node_width / 2,
            y + 0.164,
            node,
            edge,
            main_size=7.45 if node.get("choice") else 7.75,
            english_size=4.8 if node.get("choice") else 4.95,
        )
        if index < 3:
            ax.add_patch(
                FancyArrowPatch(
                    (left + node_width + 0.004, y + 0.126),
                    (node_lefts[index + 1] - 0.005, y + 0.126),
                    arrowstyle="-|>",
                    mutation_scale=8,
                    color=accent,
                    linewidth=1.3,
                    zorder=10,
                )
            )

    fallback = lane["fallback"]
    panel(
        ax,
        0.177,
        y + 0.006,
        0.772,
        0.054,
        face=COLORS["paper"],
        edge=accent,
        linewidth=0.9,
        radius=0.007,
        linestyle="dashed",
    )
    ax.text(
        0.563,
        y + 0.050,
        fallback["zh"],
        color=COLORS["ink"],
        fontsize=5.05,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.563,
        y + 0.038,
        fallback["zh_reading"],
        color=accent,
        fontsize=3.25,
        ha="center",
        va="center",
    )
    ax.text(
        0.563,
        y + 0.027,
        fallback["ja"],
        color=COLORS["ink"],
        fontsize=4.55,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.563,
        y + 0.016,
        fallback["ja_reading"],
        color=COLORS["muted"],
        fontsize=3.05,
        ha="center",
        va="center",
    )
    ax.text(
        0.565,
        y + 0.007,
        fallback["en"],
        color=accent,
        fontsize=3.45,
        fontweight="bold",
        ha="center",
        va="center",
    )


def draw_conditions(ax: Any, config: dict[str, Any]) -> None:
    from matplotlib.patches import Circle

    panel(
        ax,
        0.035,
        0.084,
        0.93,
        0.096,
        face=COLORS["white"],
        edge=COLORS["line"],
        linewidth=1.0,
    )
    starts = (0.055, 0.285, 0.515, 0.745)
    for item, x in zip(config["conditions"], starts, strict=True):
        accent = COLORS[item["color"]]
        ax.add_patch(Circle((x + 0.018, 0.135), 0.019, facecolor=accent, edgecolor="none"))
        ax.text(
            x + 0.018,
            0.135,
            item["symbol"],
            color="white",
            fontsize=7.0,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.text(
            x + 0.045,
            0.164,
            item["zh"],
            color=COLORS["ink"],
            fontsize=6.25,
            fontweight="bold",
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.045, 0.145, item["zh_reading"], color=accent, fontsize=3.9, ha="left", va="center"
        )
        ax.text(
            x + 0.045,
            0.126,
            item["ja"],
            color=COLORS["ink"],
            fontsize=5.55,
            fontweight="bold",
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.045,
            0.108,
            item["ja_reading"],
            color=COLORS["muted"],
            fontsize=3.7,
            ha="left",
            va="center",
        )
        ax.text(
            x + 0.045,
            0.092,
            item["en"],
            color=accent,
            fontsize=4.0,
            fontweight="bold",
            ha="left",
            va="center",
        )


def render(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    import matplotlib.pyplot as plt

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(5.4, 7.6), dpi=300, facecolor=COLORS["paper"])
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(
        0.04,
        0.976,
        title["zh"],
        color=COLORS["ink"],
        fontsize=14.5,
        fontweight="bold",
        ha="left",
        va="top",
    )
    ax.text(
        0.04,
        0.946,
        title["zh_reading"],
        color=COLORS["vermilion"],
        fontsize=6.0,
        ha="left",
        va="top",
    )
    ax.text(
        0.04,
        0.922,
        title["ja"],
        color=COLORS["ink"],
        fontsize=9.0,
        fontweight="bold",
        ha="left",
        va="top",
    )
    ax.text(
        0.04, 0.900, title["ja_reading"], color=COLORS["muted"], fontsize=5.25, ha="left", va="top"
    )
    ax.text(
        0.96,
        0.881,
        title["en"],
        color=COLORS["cobalt"],
        fontsize=6.1,
        fontweight="bold",
        ha="right",
        va="bottom",
    )

    panel(
        ax,
        0.035,
        0.793,
        0.93,
        0.068,
        face=COLORS["cobalt_light"],
        edge=COLORS["cobalt"],
        linewidth=1.2,
    )
    rule = config["rule"]
    ax.text(
        0.055,
        0.848,
        rule["zh"],
        color=COLORS["ink"],
        fontsize=7.4,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0.055,
        0.829,
        rule["zh_reading"],
        color=COLORS["cobalt"],
        fontsize=4.7,
        ha="left",
        va="center",
    )
    ax.text(
        0.055,
        0.810,
        rule["ja"],
        color=COLORS["ink"],
        fontsize=6.5,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0.945,
        0.829,
        rule["ja_reading"],
        color=COLORS["muted"],
        fontsize=4.2,
        ha="right",
        va="center",
    )
    ax.text(
        0.945,
        0.808,
        rule["en"],
        color=COLORS["cobalt"],
        fontsize=4.8,
        fontweight="bold",
        ha="right",
        va="center",
    )

    for lane, y in zip(config["lanes"], (0.590, 0.386, 0.182), strict=True):
        draw_lane(ax, lane, y)

    draw_conditions(ax, config)

    panel(
        ax,
        0.035,
        0.010,
        0.93,
        0.064,
        face=COLORS["vermilion_light"],
        edge=COLORS["vermilion"],
        linewidth=1.15,
    )
    cut = config["cut_order"]
    ax.text(
        0.5,
        0.064,
        cut["zh"],
        color=COLORS["ink"],
        fontsize=5.65,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.051,
        cut["zh_reading"],
        color=COLORS["vermilion"],
        fontsize=3.35,
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.039,
        cut["ja"],
        color=COLORS["ink"],
        fontsize=5.0,
        fontweight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.027,
        cut["ja_reading"],
        color=COLORS["muted"],
        fontsize=3.15,
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.016,
        cut["en"],
        color=COLORS["vermilion"],
        fontsize=3.55,
        fontweight="bold",
        ha="center",
        va="center",
    )

    metadata = {
        "Title": "LazyTravel Lanzhou one-two-three-day itinerary map",
        "Author": "LazyTravel / lazying.art",
        "Subject": "Original B6 itinerary decision diagram",
        "Keywords": "Lanzhou, itinerary, one day, two days, three days, LazyTravel",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    outputs: dict[str, dict[str, Any]] = {}
    for suffix, options in {
        "svg": {"format": "svg", "metadata": {"Date": None}},
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
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        fig.savefig(path, bbox_inches=None, pad_inches=0, facecolor=COLORS["paper"], **options)
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
    png_path = OUTPUT_STEM.with_suffix(".png")
    with Image.open(png_path) as image:
        dimensions = [image.width, image.height]
    if dimensions != [1620, 2280]:
        raise RuntimeError(f"unexpected map dimensions: {dimensions}")
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "deterministic-matplotlib-itinerary-decision-map",
        "generator": "scripts/build_lanzhou_itinerary_days_map.py",
        "config": file_record(CONFIG_PATH),
        "accepted_inputs": config["accepted_inputs"],
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": (
            "Original LazyTravel diagram; no map tiles, operator diagrams, "
            "source-guide pages, or character references redistributed."
        ),
        "technical_qa": {
            "png_dimensions": dimensions,
            "pdf_vector_output": True,
            "svg_selectable_text": True,
        },
        "visual_qa": config["visual_qa"],
    }
    provenance_path = OUTPUT_STEM.with_suffix(".provenance.json")
    write_json(provenance_path, provenance)
    for suffix, record in outputs.items():
        print(f"{suffix}: {record['path']} ({record['sha256']})")
    print(f"provenance: {provenance_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
