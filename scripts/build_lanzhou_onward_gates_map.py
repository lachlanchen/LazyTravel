#!/usr/bin/env python3
"""Build Lanzhou Chapter 10's deterministic onward-gate decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-onward-gates.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-onward-gates"
FIXED_TIME = datetime(2026, 8, 23, 0, 0, tzinfo=timezone.utc)
os.environ["SOURCE_DATE_EPOCH"] = str(int(FIXED_TIME.timestamp()))

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
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-onward-gates-v1",
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
    radius: float = 0.010,
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
            zorder=zorder,
        )
    )


def stack(
    ax: Any,
    x: float,
    top: float,
    value: dict[str, str],
    accent: str,
    *,
    align: str = "center",
    zh_size: float = 7.0,
    en_size: float = 4.25,
) -> None:
    ax.text(x, top, value["zh"], color=COLORS["ink"], fontsize=zh_size,
            fontweight="bold", ha=align, va="center", zorder=8)
    ax.text(x, top - 0.017, value["zh_reading"], color=accent, fontsize=3.65,
            ha=align, va="center", zorder=8)
    ax.text(x, top - 0.035, value["ja"], color=COLORS["ink"], fontsize=5.7,
            fontweight="bold", ha=align, va="center", zorder=8)
    ax.text(x, top - 0.052, value["ja_reading"], color=COLORS["muted"], fontsize=3.35,
            ha=align, va="center", zorder=8)
    ax.text(x, top - 0.068, value["en"], color=accent, fontsize=en_size,
            fontweight="bold", ha=align, va="center", zorder=8)


def draw_lane(ax: Any, lane: dict[str, Any], y: float) -> None:
    from matplotlib.patches import FancyArrowPatch

    accent = COLORS[lane["color"]]
    light = COLORS[f"{lane['color']}_light"]
    panel(ax, 0.035, y, 0.93, 0.188, face=COLORS["white"], edge=accent, linewidth=1.25)
    panel(ax, 0.047, y + 0.102, 0.906, 0.070, face=light, edge=accent, linewidth=1.0)
    stack(ax, 0.065, y + 0.170, lane["gate"], accent, align="left", zh_size=8.0, en_size=4.6)

    node_lefts = (0.052, 0.282, 0.512, 0.742)
    node_width = 0.205
    for index, (node, left) in enumerate(zip(lane["nodes"], node_lefts, strict=True)):
        panel(ax, left, y + 0.010, node_width, 0.078, face=COLORS["paper"], edge=accent,
              linewidth=0.9, radius=0.007, zorder=4)
        stack(ax, left + node_width / 2, y + 0.075, node, accent,
              zh_size=6.15, en_size=3.45)
        if index < 3:
            ax.add_patch(
                FancyArrowPatch(
                    (left + node_width + 0.004, y + 0.049),
                    (node_lefts[index + 1] - 0.005, y + 0.049),
                    arrowstyle="-|>", mutation_scale=8, color=accent,
                    linewidth=1.25, zorder=10,
                )
            )


def draw_callout(ax: Any, value: dict[str, str], x: float, width: float,
                 color: str, light: str) -> None:
    panel(ax, x, 0.064, width, 0.098, face=light, edge=color, linewidth=1.05)
    stack(ax, x + width / 2, 0.149, value, color, zh_size=5.8, en_size=3.35)


def render(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    import matplotlib.pyplot as plt

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(5.4, 7.6), dpi=300, facecolor=COLORS["paper"])
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(0.04, 0.976, title["zh"], color=COLORS["ink"], fontsize=14.3,
            fontweight="bold", ha="left", va="top")
    ax.text(0.04, 0.947, title["zh_reading"], color=COLORS["vermilion"],
            fontsize=5.8, ha="left", va="top")
    ax.text(0.04, 0.922, title["ja"], color=COLORS["ink"], fontsize=8.9,
            fontweight="bold", ha="left", va="top")
    ax.text(0.04, 0.900, title["ja_reading"], color=COLORS["muted"],
            fontsize=5.1, ha="left", va="top")
    ax.text(0.96, 0.880, title["en"], color=COLORS["cobalt"], fontsize=5.85,
            fontweight="bold", ha="right", va="bottom")

    panel(ax, 0.035, 0.776, 0.93, 0.088, face=COLORS["cobalt_light"],
          edge=COLORS["cobalt"], linewidth=1.2)
    stack(ax, 0.055, 0.852, config["rule"], COLORS["cobalt"], align="left",
          zh_size=7.1, en_size=4.1)

    for lane, y in zip(config["lanes"], (0.580, 0.377, 0.174), strict=True):
        draw_lane(ax, lane, y)

    draw_callout(ax, config["keep"], 0.035, 0.455, COLORS["jade"], COLORS["jade_light"])
    draw_callout(ax, config["cut_first"], 0.510, 0.455, COLORS["coral"], COLORS["coral_light"])

    boundary = config["boundary"]
    ax.text(0.5, 0.047, boundary["zh"], color=COLORS["ink"], fontsize=4.65,
            fontweight="bold", ha="center", va="center")
    ax.text(0.5, 0.034, boundary["zh_reading"], color=COLORS["vermilion"],
            fontsize=2.75, ha="center", va="center")
    ax.text(0.5, 0.022, boundary["ja"], color=COLORS["ink"], fontsize=4.0,
            ha="center", va="center")
    ax.text(0.5, 0.011, boundary["en"], color=COLORS["cobalt"], fontsize=2.75,
            fontweight="bold", ha="center", va="center")

    outputs: dict[str, dict[str, Any]] = {}
    for suffix, kwargs in (
        ("png", {"dpi": 300, "pil_kwargs": {"compress_level": 9}}),
        ("pdf", {"metadata": {"CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}}),
        ("svg", {"metadata": {"Date": "2026-08-23T00:00:00+00:00"}}),
    ):
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        fig.savefig(path, format=suffix, facecolor=COLORS["paper"],
                    bbox_inches=None, pad_inches=0, **kwargs)
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
    with Image.open(OUTPUT_STEM.with_suffix(".png")) as image:
        if image.size != (1620, 2280):
            raise RuntimeError(f"unexpected map raster size: {image.size}")
    provenance = {
        "schema_version": 1,
        "asset_id": config["asset_id"],
        "created_at": config["snapshot_date"],
        "method": "deterministic-matplotlib-map-render",
        "source": {
            "path": str(CONFIG_PATH.relative_to(ROOT)),
            "sha256": sha256(CONFIG_PATH),
        },
        "accepted_inputs": config["accepted_inputs"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "rights": (
            "Original LazyTravel diagram; no map tiles, operator diagrams, "
            "source-guide pages, or character references redistributed."
        ),
        "visual_qa": config["visual_qa"],
    }
    provenance_path = OUTPUT_STEM.with_suffix(".provenance.json")
    write_json(provenance_path, provenance)
    for record in outputs.values():
        print(f"map: {record['path']}")
    print(f"provenance: {provenance_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
