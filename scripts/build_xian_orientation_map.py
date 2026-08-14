#!/usr/bin/env python3
"""Fetch normalized map evidence and render Xi'an's opening orientation map."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shapely.geometry import GeometryCollection, LineString, MultiLineString, box, mapping, shape

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/xian/xian-before-walls.config.json"
GEOJSON_PATH = ROOT / "data/maps/xian/xian-before-walls.geojson"
OUTPUT_DIR = ROOT / "assets/maps/xian"
OUTPUT_STEM = OUTPUT_DIR / "xian-before-walls"
CACHE_DIR = ROOT / "build/maps/xian-before-walls/source"
USER_AGENT = "LazyTravel/0.1 (https://github.com/lachlanchen/LazyTravel)"
FIXED_TIME = datetime(2026, 8, 14, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))


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


def clipped_geometry(geometry: dict[str, Any], extent: list[float]) -> dict[str, Any] | None:
    clipped = shape(geometry).intersection(box(*extent))
    if clipped.is_empty:
        return None
    if isinstance(clipped, GeometryCollection):
        lines = [part for part in clipped.geoms if isinstance(part, LineString | MultiLineString)]
        if not lines:
            return None
        clipped = MultiLineString(
            [
                list(line.coords)
                for part in lines
                for line in (part.geoms if isinstance(part, MultiLineString) else [part])
            ]
        )
    return round_geometry(mapping(clipped))


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


def build_geojson(config: dict[str, Any]) -> dict[str, Any]:
    extent = config["extent"]
    lookup_ids = ",".join(item["osm_id"] for item in config["lookup_objects"])
    query = urllib.parse.urlencode(
        {"format": "jsonv2", "polygon_geojson": 1, "osm_ids": lookup_ids}
    )
    lookup_url = f"https://nominatim.openstreetmap.org/lookup?{query}"
    lookup_payload = fetch(lookup_url, CACHE_DIR / "nominatim-lookup.json")
    lookup_values = {
        f"{item['osm_type'][0].upper()}{item['osm_id']}": item
        for item in json.loads(lookup_payload)
    }

    features: list[dict[str, Any]] = []
    for record in config["lookup_objects"]:
        source = lookup_values.get(record["osm_id"])
        if not source or "geojson" not in source:
            raise ValueError(f"Nominatim lookup missing geometry for {record['osm_id']}")
        geometry = clipped_geometry(source["geojson"], extent)
        if geometry is None:
            raise ValueError(f"lookup geometry outside extent for {record['osm_id']}")
        features.append(
            {
                "type": "Feature",
                "properties": {
                    **record,
                    "source": "OpenStreetMap",
                    "generalized": False,
                },
                "geometry": geometry,
            }
        )

    for record in config["way_objects"]:
        way_id = record["osm_id"]
        url = f"https://api.openstreetmap.org/api/0.6/way/{way_id}/full"
        payload = fetch(url, CACHE_DIR / f"way-{way_id}.osm")
        geometry = clipped_geometry(parse_way_xml(payload, way_id), extent)
        if geometry is None:
            continue
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "kind": "river",
                    **record,
                    "source": "OpenStreetMap",
                    "generalized": False,
                },
                "geometry": geometry,
            }
        )
        time.sleep(1.05)

    for index, record in enumerate(config["generalized_segments"], start=1):
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "kind": "river",
                    "id": f"generalized-{index:02d}",
                    "river_key": record["river_key"],
                    "name": record["name"],
                    "source": "editorial-generalization",
                    "reason": record["reason"],
                    "generalized": True,
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": round_geometry(record["coordinates"]),
                },
            }
        )

    features.sort(
        key=lambda feature: (
            feature["properties"].get("kind", ""),
            feature["properties"].get("river_key", ""),
            str(feature["properties"].get("osm_id", feature["properties"].get("id", ""))),
        )
    )
    return {
        "type": "FeatureCollection",
        "name": config["id"],
        "bbox": extent,
        "properties": {
            "snapshot_date": config["snapshot_date"],
            "license": "OpenStreetMap data © OpenStreetMap contributors, ODbL 1.0",
            "generalization": (
                "Dashed editorial corridors fill disclosed gaps in named minor channels; "
                "not for navigation."
            ),
        },
        "features": features,
    }


def iter_lines(geometry: dict[str, Any]) -> Iterable[list[list[float]]]:
    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]
    if geometry_type == "LineString":
        yield coordinates
    elif geometry_type == "MultiLineString":
        yield from coordinates
    elif geometry_type == "Polygon":
        yield from coordinates
    elif geometry_type == "MultiPolygon":
        for polygon in coordinates:
            yield from polygon


def render_map(config: dict[str, Any], geojson: dict[str, Any]) -> dict[str, Any]:
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
            "svg.hashsalt": "lazytravel-xian-before-walls-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.patheffects as path_effects
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    extent = config["extent"]
    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor="#F5F2EA")
    ax.set_facecolor("#F5F2EA")
    fig.subplots_adjust(left=0.035, right=0.97, top=0.94, bottom=0.07)
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")

    terrain = config["terrain_symbol"]
    ax.add_patch(
        Polygon(
            terrain["coordinates"],
            closed=True,
            facecolor="#DDE3DA",
            edgecolor="#315347",
            linewidth=1,
            zorder=1,
        )
    )
    ax.text(
        108.385,
        33.835,
        terrain["name"],
        color="#315347",
        fontsize=6.3,
        fontweight="bold",
        linespacing=1.05,
        zorder=6,
    )

    for feature in geojson["features"]:
        properties = feature["properties"]
        if properties.get("kind") != "river":
            continue
        is_wei = properties.get("river_key") == "wei"
        generalized = properties.get("generalized", False)
        for line in iter_lines(feature["geometry"]):
            if len(line) < 2:
                continue
            xs, ys = zip(*line)
            ax.plot(
                xs,
                ys,
                color="#237FA3",
                linewidth=1.8 if is_wei else (1.05 if not generalized else 0.9),
                linestyle=(0, (4, 3)) if generalized else "solid",
                alpha=0.96 if not generalized else 0.82,
                solid_capstyle="round",
                zorder=3 if is_wei else 2,
            )

    for feature in geojson["features"]:
        if feature["properties"].get("kind") != "wall":
            continue
        for line in iter_lines(feature["geometry"]):
            if len(line) < 2:
                continue
            xs, ys = zip(*line)
            ax.plot(xs, ys, color="#B44736", linewidth=1.4, zorder=5)

    for label in config["labels"]:
        artist = ax.text(
            *label["position"],
            label["text"],
            rotation=label["rotation"],
            rotation_mode="anchor",
            color="#176582",
            fontsize=7.5,
            fontweight="medium",
            ha="center",
            va="center",
            zorder=7,
        )
        artist.set_path_effects([path_effects.withStroke(linewidth=3.2, foreground="#F5F2EA")])

    city = config["city_marker"]
    ax.scatter(*city["position"], s=14, color="#202522", zorder=8)
    ax.annotate(
        city["label"],
        xy=city["position"],
        xytext=(10, -15),
        textcoords="offset points",
        color="#202522",
        fontsize=8,
        fontweight="bold",
        zorder=8,
    )

    titles = config["title"]
    fig.text(
        0.055,
        0.935,
        titles["zh"],
        fontsize=16,
        fontweight="bold",
        color="#202522",
        va="top",
    )
    fig.text(0.055, 0.885, titles["ja"], fontsize=8.5, color="#5C625E", va="top")
    fig.text(
        0.055,
        0.846,
        titles["en"],
        fontsize=8,
        fontweight="bold",
        color="#5C625E",
        va="top",
    )

    fig.text(
        0.945,
        0.925,
        "N\n↑",
        ha="center",
        va="top",
        fontsize=8,
        fontweight="bold",
        color="#202522",
        linespacing=0.9,
    )

    legend_x = 108.395
    for y, dashed, label in (
        (33.902, False, "OSM河道 / OSM河道 / OSM CENTERLINE"),
        (33.878, True, "概化河道 / 概略河道 / GENERALIZED"),
    ):
        ax.plot(
            [legend_x, legend_x + 0.065],
            [y, y],
            color="#237FA3",
            linewidth=1.05,
            linestyle=(0, (4, 3)) if dashed else "solid",
            zorder=9,
        )
        ax.text(
            legend_x + 0.075,
            y,
            label,
            va="center",
            fontsize=6.2,
            color="#315347",
            zorder=9,
        )

    km_per_lon_degree = 111.32 * math.cos(math.radians(mean_latitude))
    scale_degrees = 20 / km_per_lon_degree
    scale_y = 33.865
    scale_x = 109.085
    ax.plot(
        [scale_x, scale_x + scale_degrees],
        [scale_y, scale_y],
        color="#202522",
        linewidth=1.1,
        zorder=9,
    )
    for x in (scale_x, scale_x + scale_degrees):
        ax.plot(
            [x, x],
            [scale_y - 0.006, scale_y + 0.006],
            color="#202522",
            linewidth=0.9,
            zorder=9,
        )
    ax.text(
        scale_x + scale_degrees / 2,
        scale_y + 0.014,
        "20 km",
        ha="center",
        fontsize=6.5,
    )

    fig.text(
        0.055,
        0.024,
        "示意图，不能用于导航 / 模式図・ナビゲーション不可\nSCHEMATIC / NOT FOR NAVIGATION",
        fontsize=5.5,
        color="#5C625E",
        linespacing=1.1,
    )
    fig.text(
        0.945,
        0.024,
        "OpenStreetMap contributors · ODbL 1.0\nSnapshot 2026-08-14",
        fontsize=5.2,
        color="#5C625E",
        ha="right",
        linespacing=1.1,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": "Xi'an Before the Walls",
        "Author": "LazyTravel / lazying.art",
        "Creator": "LazyTravel reproducible map renderer",
        "Subject": "Schematic orientation map of Xi'an's Qinling-Wei River setting",
        "Keywords": "Xi'an, Chang'an, Qinling, Wei River, Eight Waters, LazyTravel",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), format="pdf", metadata=metadata)
    fig.savefig(
        OUTPUT_STEM.with_suffix(".svg"),
        format="svg",
        metadata={"Title": metadata["Title"], "Date": config["snapshot_date"]},
    )
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        format="png",
        dpi=480,
        metadata={
            "Title": metadata["Title"],
            "Author": metadata["Author"],
            "Creation Time": config["snapshot_date"],
        },
    )
    plt.close(fig)

    from PIL import Image

    with Image.open(OUTPUT_STEM.with_suffix(".png")) as image:
        png_dimensions = [image.width, image.height]
    return {"png_dimensions": png_dimensions}


def write_provenance(config: dict[str, Any], technical: dict[str, Any]) -> None:
    files = {}
    for suffix in (".svg", ".pdf", ".png"):
        path = OUTPUT_STEM.with_suffix(suffix)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-xian-before-walls-map",
        "created_at": config["snapshot_date"],
        "method": "map-render",
        "command": "python3 scripts/build_xian_orientation_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "normalized_data": {
            "path": str(GEOJSON_PATH.relative_to(ROOT)),
            "sha256": sha256(GEOJSON_PATH),
        },
        "sources": config["sources"],
        "osm_objects": {
            "lookup": [record["osm_id"] for record in config["lookup_objects"]],
            "ways": [record["osm_id"] for record in config["way_objects"]],
        },
        "generalized_features": [
            {
                "name": item["name"],
                "river_key": item["river_key"],
                "reason": item["reason"],
            }
            for item in config["generalized_segments"]
        ],
        "files": files,
        "technical_qa": {
            **technical,
            "minimum_png_width": 2400,
            "svg_selectable_text": True,
            "pdf_vector_output": True,
        },
        "visual_qa": {
            "print_300dpi": "pass",
            "mobile_390px": "fail",
            "label_collisions": "pass",
            "approved": False,
            "reviewed_at": "2026-08-14",
            "notes": [
                "Print and full-page PDF review passed with readable labels and no collisions.",
                "A full-fit 390 px rendering makes minor river labels too small; the website "
                "requires a mobile-specific crop, scroll, or detail view before approval.",
            ],
        },
        "rights": (
            "Map design © LazyTravel; OpenStreetMap-derived centerlines "
            "© OpenStreetMap contributors under ODbL 1.0."
        ),
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-data",
        action="store_true",
        help="refetch the declared OSM objects and rewrite normalized GeoJSON",
    )
    args = parser.parse_args()
    config = read_json(CONFIG_PATH)
    if args.refresh_data or not GEOJSON_PATH.exists():
        write_json(GEOJSON_PATH, build_geojson(config))
    geojson = read_json(GEOJSON_PATH)
    technical = render_map(config, geojson)
    write_provenance(config, technical)
    print(f"rendered: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(f"normalized data: {GEOJSON_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
