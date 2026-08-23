#!/usr/bin/env python3
"""Build Lanzhou Chapter 11's deterministic nearby-day decision map."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-nearby-day.config.json"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-nearby-day"
FIXED_TIME = datetime(2026, 8, 23, 0, 0, tzinfo=timezone.utc)
os.environ["SOURCE_DATE_EPOCH"] = str(int(FIXED_TIME.timestamp()))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#20303A",
    "muted": "#5D6B74",
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
            "svg.hashsalt": "lazytravel-lanzhou-nearby-day-v1",
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
    ja_size: float = 5.6,
    en_size: float = 4.0,
    spacing: float = 0.016,
) -> None:
    ax.text(x, top, value["zh"], color=COLORS["ink"], fontsize=zh_size,
            fontweight="bold", ha=align, va="center", zorder=8)
    ax.text(x, top - spacing, value["zh_reading"], color=accent, fontsize=3.45,
            ha=align, va="center", zorder=8)
    ax.text(x, top - spacing * 2, value["ja"], color=COLORS["ink"], fontsize=ja_size,
            fontweight="bold", ha=align, va="center", zorder=8)
    ax.text(x, top - spacing * 3, value["ja_reading"], color=COLORS["muted"],
            fontsize=3.2, ha=align, va="center", zorder=8)
    ax.text(x, top - spacing * 4, value["en"], color=accent, fontsize=en_size,
            fontweight="bold", ha=align, va="center", zorder=8)


def draw_branch(
    ax: Any,
    branch: dict[str, Any],
    y: float,
    height: float,
    *,
    conditional: bool = False,
) -> None:
    from matplotlib.patches import FancyArrowPatch

    accent = COLORS[branch["color"]]
    light = COLORS[f"{branch['color']}_light"]
    panel(ax, 0.035, y, 0.93, height, face=COLORS["white"], edge=accent,
          linewidth=1.25)
    panel(ax, 0.047, y + height - 0.073, 0.906, 0.060, face=light, edge=accent,
          linewidth=1.0)
    stack(ax, 0.065, y + height - 0.018, branch["name"], accent, align="left",
          zh_size=7.5, ja_size=5.8, en_size=4.2, spacing=0.012)

    node_y = y + (0.092 if conditional else 0.020)
    node_height = 0.072
    node_lefts = (0.052, 0.357, 0.662)
    node_width = 0.272
    for index, (node, left) in enumerate(zip(branch["nodes"], node_lefts, strict=True)):
        panel(ax, left, node_y, node_width, node_height, face=COLORS["paper"],
              edge=accent, linewidth=0.9, radius=0.007, zorder=4)
        stack(ax, left + node_width / 2, node_y + 0.061, node, accent,
              zh_size=5.65, ja_size=4.75, en_size=3.25, spacing=0.0125)
        if index < 2:
            ax.add_patch(
                FancyArrowPatch(
                    (left + node_width + 0.005, node_y + node_height / 2),
                    (node_lefts[index + 1] - 0.006, node_y + node_height / 2),
                    arrowstyle="-|>", mutation_scale=8, color=accent,
                    linewidth=1.2, zorder=10,
                )
            )

    if conditional:
        panel(ax, 0.052, y + 0.014, 0.882, 0.061, face=COLORS["coral_light"],
              edge=COLORS["coral"], linewidth=1.0, radius=0.007, zorder=3)
        stack(ax, 0.493, y + 0.064, branch["conditional"], COLORS["coral"],
              zh_size=5.35, ja_size=4.35, en_size=3.05, spacing=0.0115)


def render(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    import matplotlib.pyplot as plt

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(5.4, 7.6), dpi=300, facecolor=COLORS["paper"])
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = config["title"]
    ax.text(0.04, 0.978, title["zh"], color=COLORS["ink"], fontsize=14.1,
            fontweight="bold", ha="left", va="top")
    ax.text(0.04, 0.949, title["zh_reading"], color=COLORS["vermilion"],
            fontsize=5.6, ha="left", va="top")
    ax.text(0.04, 0.923, title["ja"], color=COLORS["ink"], fontsize=8.5,
            fontweight="bold", ha="left", va="top")
    ax.text(0.04, 0.901, title["ja_reading"], color=COLORS["muted"],
            fontsize=4.85, ha="left", va="top")
    ax.text(0.96, 0.879, title["en"], color=COLORS["cobalt"], fontsize=5.55,
            fontweight="bold", ha="right", va="bottom")

    panel(ax, 0.035, 0.783, 0.93, 0.078, face=COLORS["cobalt_light"],
          edge=COLORS["cobalt"], linewidth=1.2)
    stack(ax, 0.055, 0.850, config["rule"], COLORS["cobalt"], align="left",
          zh_size=7.0, ja_size=5.6, en_size=3.95, spacing=0.0135)

    draw_branch(ax, config["branches"][0], 0.515, 0.245, conditional=True)
    draw_branch(ax, config["branches"][1], 0.318, 0.180)
    draw_branch(ax, config["branches"][2], 0.121, 0.180)

    panel(ax, 0.035, 0.025, 0.93, 0.074, face=COLORS["coral_light"],
          edge=COLORS["coral"], linewidth=1.15)
    stack(ax, 0.5, 0.088, config["cancel"], COLORS["coral"], zh_size=5.95,
          ja_size=4.8, en_size=3.35, spacing=0.0127)

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
            "source-guide pages, official photographs, or character references redistributed."
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
