#!/usr/bin/env python3
"""Build Lanzhou's opening river-valley orientation map."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shapely.geometry import GeometryCollection, LineString, MultiLineString, box, mapping, shape

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-valley-orientation.config.json"
GEOJSON_PATH = ROOT / "data/maps/lanzhou/lanzhou-valley-orientation.geojson"
OUTPUT_DIR = ROOT / "assets/maps/lanzhou"
OUTPUT_STEM = OUTPUT_DIR / "lanzhou-valley-orientation"
CACHE_DIR = ROOT / "build/maps/lanzhou-valley-orientation/source"
USER_AGENT = "LazyTravel/0.1 (https://github.com/lachlanchen/LazyTravel)"
FIXED_TIME = datetime(2026, 8, 21, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

COLORS = {
    "paper": "#FCFDFF",
    "ink": "#25313A",
    "muted": "#65717B",
    "river": "#1769D2",
    "river_light": "#B9DDF7",
    "vermilion": "#E44736",
    "jade": "#23836B",
    "coral": "#F06E65",
}

NODE_STYLES = {
    "arrival": {"marker": "s", "face": COLORS["vermilion"], "size": 54},
    "attraction": {"marker": "D", "face": COLORS["coral"], "size": 50},
    "anchor": {"marker": "o", "face": COLORS["jade"], "size": 46},
    "crossing": {"marker": "P", "face": COLORS["river"], "size": 62},
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


def fetch(url: str, cache_path: Path) -> bytes:
    if cache_path.exists():
        return cache_path.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                payload = response.read()
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(payload)
            return payload
        except Exception as error:  # pragma: no cover - network retry
            last_error = error
            time.sleep(2**attempt)
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def round_geometry(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, list | tuple):
        return [round_geometry(item) for item in value]
    if isinstance(value, dict):
        return {key: round_geometry(item) for key, item in value.items()}
    return value


def parse_way_xml(payload: bytes, way_id: int) -> dict[str, Any]:
    root = ET.fromstring(payload)
    nodes = {
        node.attrib["id"]: (float(node.attrib["lon"]), float(node.attrib["lat"]))
        for node in root.findall("node")
    }
    for way in root.findall("way"):
        if int(way.attrib["id"]) != way_id:
            continue
        coordinates = [nodes[nd.attrib["ref"]] for nd in way.findall("nd")]
        if len(coordinates) < 2:
            raise ValueError(f"OSM way {way_id} has fewer than two mapped nodes")
        return {"type": "LineString", "coordinates": coordinates}
    raise ValueError(f"OSM way {way_id} missing from API response")


def clipped_line(geometry: dict[str, Any], extent: list[float]) -> dict[str, Any]:
    clipped = shape(geometry).intersection(box(*extent))
    if clipped.is_empty:
        raise ValueError("river geometry does not intersect the configured extent")
    if isinstance(clipped, GeometryCollection):
        lines = [part for part in clipped.geoms if isinstance(part, LineString | MultiLineString)]
        if not lines:
            raise ValueError("river clip contains no line geometry")
        clipped = MultiLineString(
            [
                list(line.coords)
                for part in lines
                for line in (part.geoms if isinstance(part, MultiLineString) else [part])
            ]
        )
    return round_geometry(mapping(clipped))


def build_geojson(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    river = config["river"]
    cache_path = CACHE_DIR / f"way-{river['osm_way_id']}.osm"
    payload = fetch(river["source_url"], cache_path)
    river_geometry = clipped_line(parse_way_xml(payload, river["osm_way_id"]), config["extent"])
    features = [
        {
            "type": "Feature",
            "properties": {
                "kind": "river",
                "name": river["name"],
                "osm_way_id": river["osm_way_id"],
                "source": "OpenStreetMap",
            },
            "geometry": river_geometry,
        }
    ]
    features.extend(
        {
            "type": "Feature",
            "properties": {
                "kind": "anchor",
                "id": node["id"],
                "name": node["label"],
                "category": node["category"],
                "osm_object": node["osm_object"],
            },
            "geometry": {"type": "Point", "coordinates": node["position"]},
        }
        for node in config["nodes"]
    )
    document = {
        "type": "FeatureCollection",
        "name": config["id"],
        "bbox": config["extent"],
        "properties": {
            "snapshot_date": config["snapshot_date"],
            "license": config["sources"]["openstreetmap"]["license"],
            "generalizations": config["generalizations"],
        },
        "features": features,
    }
    source = {
        "url": river["source_url"],
        "cache_path": str(cache_path.relative_to(ROOT)),
        "cache_sha256": sha256(cache_path),
        "bytes": len(payload),
    }
    return document, source


def iter_lines(geometry: dict[str, Any]) -> Iterable[list[list[float]]]:
    if geometry["type"] == "LineString":
        yield geometry["coordinates"]
    elif geometry["type"] == "MultiLineString":
        yield from geometry["coordinates"]


def render_map(config: dict[str, Any], geojson: dict[str, Any]) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-lanzhou-valley-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.patheffects as path_effects
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import FancyBboxPatch, Polygon

    extent = config["extent"]
    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor=COLORS["paper"])
    fig.subplots_adjust(left=0.035, right=0.975, top=0.88, bottom=0.12)
    ax.set_facecolor(COLORS["paper"])
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")

    for hill in config["hill_bands"]:
        ax.add_patch(
            Polygon(
                hill["coordinates"],
                closed=True,
                facecolor=hill["fill"],
                edgecolor=hill["edge"],
                linewidth=1.0,
                zorder=1,
            )
        )
        ax.text(
            *hill["label_position"],
            hill["label"],
            color=hill["edge"],
            fontsize=7.4,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=7,
        )

    river_feature = next(
        feature for feature in geojson["features"] if feature["properties"]["kind"] == "river"
    )
    for coordinates in iter_lines(river_feature["geometry"]):
        xs = [point[0] for point in coordinates]
        ys = [point[1] for point in coordinates]
        ax.plot(xs, ys, color=COLORS["river_light"], linewidth=10.5, zorder=2)
        ax.plot(xs, ys, color=COLORS["river"], linewidth=6.2, zorder=3)

    ax.annotate(
        "黄河向东 · EAST",
        xy=(103.868, 36.059),
        xytext=(103.843, 36.061),
        color=COLORS["river"],
        fontsize=8.0,
        fontweight="bold",
        arrowprops={"arrowstyle": "-|>", "color": COLORS["river"], "lw": 1.4},
        zorder=8,
    )
    ax.text(103.780, 36.074, "北岸 · NORTH BANK", color=COLORS["muted"], fontsize=7.0, zorder=7)
    ax.text(103.782, 36.055, "南岸 · SOUTH BANK", color=COLORS["muted"], fontsize=7.0, zorder=7)

    for route in config["schematic_routes"]:
        coordinates = route["coordinates"]
        ax.plot(
            [point[0] for point in coordinates],
            [point[1] for point in coordinates],
            color=route["color"],
            linewidth=2.7,
            solid_capstyle="round",
            zorder=4,
        )

    text_effect = [path_effects.withStroke(linewidth=2.6, foreground=COLORS["paper"])]
    for node in config["nodes"]:
        style = NODE_STYLES[node["category"]]
        ax.scatter(
            [node["position"][0]],
            [node["position"][1]],
            s=style["size"],
            marker=style["marker"],
            facecolor=style["face"],
            edgecolor=COLORS["paper"],
            linewidth=0.9,
            zorder=9,
        )
        ax.annotate(
            node["label"],
            xy=node["position"],
            xytext=node["label_offset"],
            textcoords="offset points",
            ha=node["label_align"],
            va="center",
            color=COLORS["ink"],
            fontsize=8.0,
            fontweight="bold",
            linespacing=1.05,
            path_effects=text_effect,
            zorder=10,
        )

    ax.text(
        0.0,
        1.085,
        "先读河谷 · まず河谷を読む",
        transform=ax.transAxes,
        color=COLORS["ink"],
        fontsize=14,
        fontweight="bold",
        va="bottom",
    )
    ax.text(
        0.0,
        1.03,
        "READ THE VALLEY FIRST — RIVER, BANK, DIRECTION, ARRIVAL GATE",
        transform=ax.transAxes,
        color=COLORS["river"],
        fontsize=8.0,
        fontweight="bold",
        va="bottom",
    )

    airport = config["airport_inset"]
    box_patch = FancyBboxPatch(
        (0.755, 0.745),
        0.235,
        0.235,
        transform=ax.transAxes,
        boxstyle="round,pad=0.008,rounding_size=0.006",
        facecolor=COLORS["paper"],
        edgecolor=COLORS["coral"],
        linewidth=1.1,
        zorder=12,
    )
    ax.add_patch(box_patch)
    ax.annotate(
        "",
        xy=(0.79, 0.935),
        xytext=(0.79, 0.80),
        xycoords=ax.transAxes,
        arrowprops={"arrowstyle": "-|>", "color": COLORS["coral"], "lw": 1.7},
        zorder=13,
    )
    ax.text(0.82, 0.925, airport["direction"], transform=ax.transAxes, fontsize=7.4, color=COLORS["coral"], fontweight="bold", zorder=13)
    ax.text(0.82, 0.855, airport["label"], transform=ax.transAxes, fontsize=8.0, color=COLORS["ink"], fontweight="bold", va="center", zorder=13)
    ax.text(0.765, 0.775, airport["note"], transform=ax.transAxes, fontsize=4.8, color=COLORS["muted"], zorder=13)

    legend = [
        Line2D([0], [0], marker="s", color="none", markerfacecolor=COLORS["vermilion"], markeredgecolor=COLORS["paper"], markersize=6, label="到达站 · ARRIVAL"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor=COLORS["coral"], markeredgecolor=COLORS["paper"], markersize=5.5, label="地点 · PLACE"),
        Line2D([0], [0], color=COLORS["vermilion"], lw=2.7, label="地铁 1 · METRO 1"),
        Line2D([0], [0], color=COLORS["jade"], lw=2.7, label="地铁 2 · METRO 2"),
    ]
    ax.legend(
        handles=legend,
        loc="lower left",
        bbox_to_anchor=(0.0, -0.11),
        ncol=4,
        frameon=False,
        fontsize=5.6,
        handlelength=2.0,
        columnspacing=1.0,
    )

    bar_km = 2.0
    lon_per_km = 1 / (111.32 * math.cos(math.radians(mean_latitude)))
    bar_start = 103.807
    bar_end = bar_start + bar_km * lon_per_km
    bar_y = 36.030
    ax.plot([bar_start, bar_end], [bar_y, bar_y], color=COLORS["ink"], linewidth=2.0, zorder=14)
    ax.plot([bar_start, bar_start], [bar_y - 0.0006, bar_y + 0.0006], color=COLORS["ink"], linewidth=1.0, zorder=14)
    ax.plot([bar_end, bar_end], [bar_y - 0.0006, bar_y + 0.0006], color=COLORS["ink"], linewidth=1.0, zorder=14)
    ax.text((bar_start + bar_end) / 2, bar_y + 0.0012, "2 km", ha="center", fontsize=5.8, color=COLORS["ink"], zorder=14)

    ax.annotate(
        "N",
        xy=(0.985, 0.19),
        xytext=(0.985, 0.11),
        xycoords=ax.transAxes,
        ha="center",
        fontsize=7.4,
        fontweight="bold",
        color=COLORS["ink"],
        arrowprops={"arrowstyle": "-|>", "color": COLORS["ink"], "lw": 1.0},
        zorder=14,
    )
    ax.text(
        0.0,
        -0.155,
        "河道与地点：OpenStreetMap 2026-08-21 · 山地色带与地铁连线为方位示意，不用于导航",
        transform=ax.transAxes,
        fontsize=5.2,
        color=COLORS["muted"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_STEM.with_suffix(".png")
    pdf_path = OUTPUT_STEM.with_suffix(".pdf")
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    metadata = {"Creator": "LazyTravel", "Date": None}
    fig.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), metadata={"Software": "LazyTravel"})
    fig.savefig(pdf_path, facecolor=fig.get_facecolor(), metadata=metadata)
    fig.savefig(svg_path, facecolor=fig.get_facecolor(), metadata=metadata)
    plt.close(fig)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    return {
        "png": {"path": str(png_path.relative_to(ROOT)), "sha256": sha256(png_path), "bytes": png_path.stat().st_size, "width": 2100, "height": 1485},
        "pdf": {"path": str(pdf_path.relative_to(ROOT)), "sha256": sha256(pdf_path), "bytes": pdf_path.stat().st_size},
        "svg": {"path": str(svg_path.relative_to(ROOT)), "sha256": sha256(svg_path), "bytes": svg_path.stat().st_size},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-source",
        action="store_true",
        help="refresh the pinned OpenStreetMap-derived GeoJSON before rendering",
    )
    args = parser.parse_args()
    config = read_json(CONFIG_PATH)
    osm_source: dict[str, Any] | None = None
    if args.refresh_source or not GEOJSON_PATH.exists():
        geojson, osm_source = build_geojson(config)
        write_json(GEOJSON_PATH, geojson)
    else:
        geojson = read_json(GEOJSON_PATH)
    outputs = render_map(config, geojson)
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-lanzhou-valley-orientation-map",
        "created_at": config["snapshot_date"],
        "command": "python3 scripts/build_lanzhou_valley_orientation_map.py",
        "refresh_command": "python3 scripts/build_lanzhou_valley_orientation_map.py --refresh-source",
        "config": {"path": str(CONFIG_PATH.relative_to(ROOT)), "sha256": sha256(CONFIG_PATH)},
        "geojson": {"path": str(GEOJSON_PATH.relative_to(ROOT)), "sha256": sha256(GEOJSON_PATH)},
        "osm_refresh_source": osm_source,
        "sources": config["sources"],
        "generalizations": config["generalizations"],
        "outputs": outputs,
        "visual_qa": config["visual_qa"],
        "rights": "Map design © LazyTravel; river and point data © OpenStreetMap contributors, ODbL 1.0.",
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(f"rendered: {outputs['png']['path']}")
    print(f"vector: {outputs['svg']['path']}")
    print(f"provenance: {OUTPUT_STEM.with_suffix('.provenance.json').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
