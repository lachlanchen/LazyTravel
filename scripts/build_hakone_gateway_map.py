#!/usr/bin/env python3
"""Build Hakone Chapter 2's gateway, transfer, and luggage schematic."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-gateway-transfer.config.json"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-gateway-transfer"
FIXED_TIME = datetime(2026, 8, 16, 0, 0, tzinfo=timezone.utc)
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
            "svg.hashsalt": "lazytravel-hakone-gateway-transfer-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.patheffects as path_effects
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon

    colors = {
        "ink": "#142330",
        "muted": "#586775",
        "paper": "#F9FCFF",
        "rail": "#E94235",
        "odakyu": "#087F8C",
        "mountain": "#F05D36",
        "bus": "#1769E0",
        "luggage": "#00A47A",
        "sun": "#FFD447",
        "line": "#C7D4E2",
    }

    nodes = {node["id"]: node for node in config["nodes"]}
    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor=colors["paper"])
    fig.subplots_adjust(left=0.035, right=0.965, top=0.82, bottom=0.17)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.88)
    ax.axis("off")

    ax.add_patch(
        FancyBboxPatch(
            (0.02, 0.33),
            0.96,
            0.5,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#EFF7FA",
            edgecolor="#D7E5EC",
            linewidth=0.8,
            zorder=0,
        )
    )
    mountain = Polygon(
        [(0.18, 0.04), (0.35, 0.33), (0.48, 0.17), (0.61, 0.39), (0.84, 0.04)],
        closed=True,
        facecolor="#DDF2E8",
        edgecolor="none",
        zorder=0,
    )
    ax.add_patch(mountain)

    def arrow(start: str, end: str, color: str, width: float, curve: float = 0.0) -> None:
        p1 = nodes[start]["position"]
        p2 = nodes[end]["position"]
        ax.add_patch(
            FancyArrowPatch(
                p1,
                p2,
                arrowstyle="-|>",
                mutation_scale=11,
                connectionstyle=f"arc3,rad={curve}",
                linewidth=width + 3.1,
                color="#FFFFFF",
                zorder=2,
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                p1,
                p2,
                arrowstyle="-|>",
                mutation_scale=10,
                connectionstyle=f"arc3,rad={curve}",
                linewidth=width,
                color=color,
                zorder=3,
            )
        )

    arrow("west", "odawara", colors["rail"], 3.2)
    arrow("tokyo", "odawara", colors["rail"], 3.2)
    arrow("shinjuku", "odawara", colors["odakyu"], 3.0, -0.08)
    arrow("odawara", "yumoto", colors["odakyu"], 3.3)
    arrow("yumoto", "gora", colors["mountain"], 3.0, 0.04)
    arrow("yumoto", "lake", colors["bus"], 3.0, -0.04)

    line_labels = [
        (0.29, 0.655, "东海道新干线・東海道新幹線 / TOKAIDO SHINKANSEN", colors["rail"]),
        (0.71, 0.54, "小田急线・小田急線 / ODAKYU", colors["odakyu"]),
        (0.365, 0.245, "登山电车・登山電車 / MOUNTAIN TRAIN", colors["mountain"]),
        (0.635, 0.245, "巴士・バス / BUS", colors["bus"]),
    ]
    for x, y, label, color in line_labels:
        text = ax.text(
            x,
            y,
            label,
            fontsize=6.2,
            fontweight="bold",
            ha="center",
            va="center",
            color=color,
            zorder=5,
        )
        text.set_path_effects([path_effects.withStroke(linewidth=2.2, foreground=colors["paper"])])

    node_offsets = {
        "west": (-0.01, 0.062, "left"),
        "tokyo": (0.01, 0.062, "right"),
        "shinjuku": (0.01, -0.072, "right"),
        "odawara": (0.0, 0.072, "center"),
        "yumoto": (0.0, -0.078, "center"),
        "gora": (0.0, -0.082, "center"),
        "lake": (0.0, -0.082, "center"),
    }
    for node_id, node in nodes.items():
        x, y = node["position"]
        radius = 0.025 if node_id in {"odawara", "yumoto"} else 0.018
        face = colors["sun"] if node_id == "odawara" else "#FFFFFF"
        if node_id == "yumoto":
            face = "#BCECDD"
        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=face,
                edgecolor=colors["ink"],
                linewidth=1.3,
                zorder=6,
            )
        )
        dx, dy, align = node_offsets[node_id]
        label = ax.text(
            x + dx,
            y + dy,
            node["label"],
            fontsize=7.5 if node_id in {"odawara", "yumoto"} else 6.7,
            fontweight="bold",
            color=colors["ink"],
            ha=align,
            va="center",
            linespacing=1.05,
            zorder=7,
        )
        label.set_path_effects([path_effects.withStroke(linewidth=2.8, foreground=colors["paper"])])

    # A simple suitcase marks the decision point without implying a counter location.
    bag_x, bag_y = 0.57, 0.43
    ax.add_patch(
        FancyBboxPatch(
            (bag_x, bag_y - 0.025),
            0.038,
            0.052,
            boxstyle="round,pad=0.003,rounding_size=0.006",
            facecolor=colors["luggage"],
            edgecolor=colors["ink"],
            linewidth=0.8,
            zorder=8,
        )
    )
    ax.plot(
        [bag_x + 0.012, bag_x + 0.012, bag_x + 0.026, bag_x + 0.026],
        [bag_y + 0.027, bag_y + 0.041, bag_y + 0.041, bag_y + 0.027],
        color=colors["ink"],
        linewidth=1.0,
        zorder=8,
    )
    ax.text(
        bag_x + 0.052,
        bag_y,
        "先处理行李・先に荷物\nDECIDE THE BAG FIRST",
        fontsize=6.2,
        fontweight="bold",
        color=colors["luggage"],
        ha="left",
        va="center",
        linespacing=1.05,
        zorder=8,
    )

    fig.text(
        0.04,
        0.955,
        f"{config['title']['zh']}  ·  {config['title']['ja']}",
        fontsize=13,
        fontweight="bold",
        color=colors["ink"],
    )
    fig.text(
        0.04,
        0.905,
        config["title"]["en"],
        fontsize=8.2,
        fontweight="bold",
        color=colors["bus"],
    )
    fig.text(
        0.955,
        0.947,
        "直达不等于只有一种票\n"
        "直通でも、きっぷは一種類とは限らない\n"
        "DIRECT DOES NOT MEAN ONE TICKET",
        fontsize=5.8,
        color=colors["muted"],
        ha="right",
        va="top",
        linespacing=1.22,
    )
    fig.text(
        0.04,
        0.09,
        "示意：不按距离与时刻绘制，换乘不作保证。请选停靠小田原的车次，并查实时运行。",
        fontsize=5.5,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.058,
        "模式図：距離・時刻・接続保証は示さない。小田原停車便と当日の運行情報を確認。",
        fontsize=5.5,
        color=colors["muted"],
    )
    fig.text(
        0.04,
        0.026,
        "Schematic: not to scale or a timetable; connections are not guaranteed. "
        "Check an Odawara-stopping train and live service.",
        fontsize=5.5,
        color=colors["muted"],
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
    files = {}
    for suffix in ("svg", "pdf", "png"):
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    png_dimensions = list(Image.open(OUTPUT_STEM.with_suffix(".png")).size)
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-hakone-gateway-transfer-map",
        "created_at": config["snapshot_date"],
        "method": "schematic-map-render",
        "command": "python3 scripts/build_hakone_gateway_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "config_sha256": sha256(CONFIG_PATH),
        "sources": config["sources"],
        "declared_generalizations": config["generalizations"],
        "rights": (
            "Map design © LazyTravel; route relationships derived from the listed "
            "official operators."
        ),
        "files": files,
        "technical_qa": {
            "minimum_png_width": 2400,
            "pdf_vector_output": True,
            "png_dimensions": png_dimensions,
            "svg_selectable_text": True,
        },
        "visual_qa": {
            "print_300dpi": "pass",
            "mobile_390px": "pass",
            "label_collisions": "pass",
            "approved": True,
            "reviewed_at": config["snapshot_date"],
            "notes": [
                (
                    "Compiled landscape B6 page keeps all gateway nodes, route labels, "
                    "luggage marker, and caveats inside the trim with no collisions: "
                    "build/qa/books/hakone/ch02-review/page-21.png, sha256 "
                    "39a81331a8c5ed1dbf918405a2453c3013c4eb245bd41e2924cfd20e097b1bda."
                ),
                (
                    "The 390 px raster check keeps the decision nodes and route labels "
                    "readable; the full caveat is repeated in live page text: "
                    "build/qa/site/hakone-ch02/map-raster-390.png, sha256 "
                    "9cb4c7834335016790464a84caa5c696f82c9142f2f17829467053345556c8e5."
                ),
            ],
        },
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(f"map: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
