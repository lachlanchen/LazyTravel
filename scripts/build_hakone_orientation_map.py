#!/usr/bin/env python3
"""Build Hakone's opening terrain, transfer, and elevation map."""

from __future__ import annotations

import hashlib
import json
import math
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from shapely.geometry import mapping, shape

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/maps/hakone/hakone-orientation.config.json"
GEOJSON_PATH = ROOT / "data/maps/hakone/hakone-orientation.geojson"
OUTPUT_DIR = ROOT / "assets/maps/hakone"
OUTPUT_STEM = OUTPUT_DIR / "hakone-orientation"
CACHE_DIR = ROOT / "build/maps/hakone-orientation/source"
USER_AGENT = "LazyTravel/0.1 (https://github.com/lachlanchen/LazyTravel)"
FIXED_TIME = datetime(2026, 8, 16, 0, 0, tzinfo=timezone.utc)
os.environ.setdefault("SOURCE_DATE_EPOCH", str(int(FIXED_TIME.timestamp())))

ROUTE_STYLES = {
    "gateway-rail": {"color": "#E24736", "width": 2.3, "linestyle": "solid"},
    "mountain-rail": {"color": "#E24736", "width": 2.3, "linestyle": "solid"},
    "cable-car": {"color": "#008C72", "width": 2.6, "linestyle": "solid"},
    "ropeway": {"color": "#7A3EC8", "width": 2.6, "linestyle": "solid"},
    "sightseeing-cruise": {"color": "#1769E0", "width": 2.5, "linestyle": "solid"},
    "bus-link": {"color": "#52606D", "width": 1.25, "linestyle": (0, (3, 2))},
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


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


def lon_to_tile_x(lon: float, zoom: int) -> float:
    return (lon + 180.0) / 360.0 * 2**zoom


def lat_to_tile_y(lat: float, zoom: int) -> float:
    latitude = math.radians(lat)
    return (1.0 - math.asinh(math.tan(latitude)) / math.pi) / 2.0 * 2**zoom


def tile_x_to_lon(x: float, zoom: int) -> float:
    return x / 2**zoom * 360.0 - 180.0


def tile_y_to_lat(y: float, zoom: int) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / 2**zoom))))


def decode_gsi_dem(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB"), dtype=np.int64)
    encoded = rgb[:, :, 0] * 65536 + rgb[:, :, 1] * 256 + rgb[:, :, 2]
    values = np.where(encoded < 2**23, encoded, encoded - 2**24).astype(float) * 0.01
    values[encoded == 2**23] = np.nan
    return values


def terrain_mosaic(
    config: dict[str, Any], zoom: int = 12
) -> tuple[np.ndarray, tuple[float, float, float, float], dict[str, Any]]:
    west, south, east, north = config["extent"]
    x_min = math.floor(lon_to_tile_x(west, zoom))
    x_max = math.floor(lon_to_tile_x(east, zoom))
    y_min = math.floor(lat_to_tile_y(north, zoom))
    y_max = math.floor(lat_to_tile_y(south, zoom))
    rows: list[np.ndarray] = []
    tile_records: list[dict[str, Any]] = []
    template = config["sources"]["terrain"]["url_template"]
    for y in range(y_min, y_max + 1):
        columns: list[np.ndarray] = []
        for x in range(x_min, x_max + 1):
            url = template.format(z=zoom, x=x, y=y)
            cache_path = CACHE_DIR / f"gsi-dem5a-z{zoom}-{x}-{y}.png"
            payload = fetch(url, cache_path)
            image = Image.open(cache_path)
            columns.append(decode_gsi_dem(image))
            tile_records.append(
                {
                    "z": zoom,
                    "x": x,
                    "y": y,
                    "url": url,
                    "bytes": len(payload),
                    "sha256": sha256(cache_path),
                }
            )
        rows.append(np.concatenate(columns, axis=1))
    elevation = np.concatenate(rows, axis=0)
    mosaic_extent = (
        tile_x_to_lon(x_min, zoom),
        tile_x_to_lon(x_max + 1, zoom),
        tile_y_to_lat(y_max + 1, zoom),
        tile_y_to_lat(y_min, zoom),
    )
    return elevation, mosaic_extent, {"zoom": zoom, "tiles": tile_records}


def sample_elevation(
    elevation: np.ndarray,
    mosaic_extent: tuple[float, float, float, float],
    position: list[float],
) -> float:
    west, east, south, north = mosaic_extent
    lon, lat = position
    x = round((lon - west) / (east - west) * (elevation.shape[1] - 1))
    y = round((north - lat) / (north - south) * (elevation.shape[0] - 1))
    return float(elevation[y, x])


def normalized_geojson(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    lake = config["lake"]
    query = urllib.parse.urlencode(
        {"format": "jsonv2", "polygon_geojson": 1, "osm_ids": lake["osm_id"]}
    )
    url = f"https://nominatim.openstreetmap.org/lookup?{query}"
    cache_path = CACHE_DIR / "nominatim-lake-lookup.json"
    values = json.loads(fetch(url, cache_path))
    if not values or "geojson" not in values[0]:
        raise ValueError("Nominatim did not return Lake Ashi geometry")
    lake_geometry = shape(values[0]["geojson"]).simplify(0.00006, preserve_topology=True)
    features = [
        {
            "type": "Feature",
            "properties": {
                "kind": "lake",
                "name": lake["name"],
                "osm_id": lake["osm_id"],
            },
            "geometry": mapping(lake_geometry),
        }
    ]
    features.extend(
        {
            "type": "Feature",
            "properties": {
                "kind": "transport-node",
                "id": node["id"],
                "name": node["label"],
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
            "license": "OpenStreetMap data © OpenStreetMap contributors, ODbL 1.0",
        },
        "features": features,
    }
    source = {
        "url": url,
        "cache_sha256": sha256(cache_path),
        "lake_osm_id": lake["osm_id"],
        "node_osm_objects": [node["osm_object"] for node in config["nodes"]],
    }
    return document, source


def route_coordinates(route: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> list[list[float]]:
    if "coordinates" in route:
        return route["coordinates"]
    return [nodes[node_id]["position"] for node_id in route["node_ids"]]


def render_map(
    config: dict[str, Any],
    geojson: dict[str, Any],
    elevation: np.ndarray,
    mosaic_extent: tuple[float, float, float, float],
) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "lazytravel-hakone-orientation-v1",
            "axes.unicode_minus": False,
        }
    )
    import matplotlib.patheffects as path_effects
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.patches import Polygon

    extent = config["extent"]
    terrain_colors = ["#E9F4F5", "#BDE1D0", "#72B98D", "#34765E", "#244C46"]
    terrain_cmap = LinearSegmentedColormap.from_list("hakone-terrain", terrain_colors)
    fig, ax = plt.subplots(figsize=(7, 4.95), facecolor="#FCFDFF")
    fig.subplots_adjust(left=0.035, right=0.975, top=0.87, bottom=0.07)
    ax.set_facecolor("#EAF2FF")
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[1], extent[3])
    mean_latitude = (extent[1] + extent[3]) / 2
    ax.set_aspect(1 / math.cos(math.radians(mean_latitude)))
    ax.axis("off")

    ax.imshow(
        elevation,
        extent=mosaic_extent,
        origin="upper",
        cmap=terrain_cmap,
        vmin=0,
        vmax=1250,
        interpolation="bilinear",
        alpha=0.88,
        zorder=0,
    )
    west, east, south, north = mosaic_extent
    lons = np.linspace(west, east, elevation.shape[1])
    lats = np.linspace(north, south, elevation.shape[0])
    ax.contour(
        lons,
        lats,
        elevation,
        levels=[200, 400, 600, 800, 1000, 1200],
        colors="#173F3B",
        linewidths=0.32,
        alpha=0.32,
        zorder=1,
    )

    lake_feature = next(
        feature for feature in geojson["features"] if feature["properties"]["kind"] == "lake"
    )
    lake_geometry = shape(lake_feature["geometry"])
    polygons = (
        list(lake_geometry.geoms) if lake_geometry.geom_type == "MultiPolygon" else [lake_geometry]
    )
    for polygon in polygons:
        ax.add_patch(
            Polygon(
                list(polygon.exterior.coords),
                facecolor="#2A78D1",
                edgecolor="#0F4E91",
                linewidth=0.9,
                zorder=2,
            )
        )

    nodes = {node["id"]: node for node in config["nodes"]}
    for route in config["routes"]:
        coordinates = route_coordinates(route, nodes)
        xs, ys = zip(*coordinates)
        style = ROUTE_STYLES[route["mode"]]
        ax.plot(
            xs,
            ys,
            color=style["color"],
            linewidth=style["width"] + 2.2,
            linestyle=style["linestyle"],
            alpha=0.78,
            solid_capstyle="round",
            zorder=3,
        )
        ax.plot(
            xs,
            ys,
            color="#FFFFFF",
            linewidth=style["width"] + 0.8,
            linestyle=style["linestyle"],
            alpha=0.97,
            solid_capstyle="round",
            zorder=4,
        )
        ax.plot(
            xs,
            ys,
            color=style["color"],
            linewidth=style["width"],
            linestyle=style["linestyle"],
            solid_capstyle="round",
            zorder=5,
        )

    for node in config["nodes"]:
        lon, lat = node["position"]
        ax.scatter(lon, lat, s=25, color="#FFFFFF", edgecolor="#17212B", linewidth=0.9, zorder=7)
        label = ax.annotate(
            node["label"],
            xy=(lon, lat),
            xytext=tuple(node["label_offset"]),
            textcoords="offset points",
            fontsize=6.7,
            fontweight="bold",
            color="#17212B",
            linespacing=1.05,
            ha="left",
            va="center",
            zorder=8,
        )
        label.set_path_effects([path_effects.withStroke(linewidth=2.6, foreground="#FCFDFF")])

    lake_label = ax.text(
        139.003,
        35.215,
        config["lake"]["name"],
        color="#FFFFFF",
        fontsize=7.1,
        fontweight="bold",
        rotation=70,
        ha="center",
        va="center",
        zorder=8,
    )
    lake_label.set_path_effects([path_effects.withStroke(linewidth=2.2, foreground="#0F4E91")])

    ax.annotate(
        "N",
        xy=(139.159, 35.268),
        xytext=(139.159, 35.259),
        arrowprops={"arrowstyle": "-|>", "color": "#17212B", "lw": 1.2},
        ha="center",
        va="bottom",
        fontsize=7.5,
        fontweight="bold",
        zorder=9,
    )
    scale_lat = 35.184
    scale_start = 138.978
    scale_lon = 5 / (111.32 * math.cos(math.radians(scale_lat)))
    ax.plot(
        [scale_start, scale_start + scale_lon],
        [scale_lat, scale_lat],
        color="#17212B",
        linewidth=2.2,
        zorder=9,
    )
    ax.text(
        scale_start + scale_lon / 2,
        scale_lat + 0.0022,
        "5 km",
        fontsize=6.2,
        ha="center",
        color="#17212B",
        zorder=9,
    )

    profile_ids = config["profile_node_ids"]
    profile_nodes = [nodes[node_id] for node_id in profile_ids]
    profile_values = [
        round(sample_elevation(elevation, mosaic_extent, node["position"]) / 10) * 10
        for node in profile_nodes
    ]
    profile_ax = ax.inset_axes([0.55, 0.035, 0.43, 0.27], facecolor="#FCFDFFF2", zorder=10)
    profile_x = np.arange(len(profile_nodes))
    profile_ax.fill_between(profile_x, profile_values, color="#FF6B4A", alpha=0.24)
    profile_ax.plot(
        profile_x, profile_values, color="#E24736", linewidth=2.0, marker="o", markersize=3.8
    )
    profile_ax.set_ylim(0, max(profile_values) + 180)
    profile_ax.set_xticks(profile_x)
    profile_ax.set_xticklabels(
        [
            "小田原",
            "湯本",
            "宮ノ下",
            "強羅",
            "早雲山",
            "大涌谷",
            "桃源台",
            "元箱根",
        ],
        fontsize=4.8,
        rotation=32,
        ha="right",
    )
    profile_ax.set_yticks([0, 500, 1000])
    profile_ax.set_yticklabels(["0", "500 m", "1000 m"], fontsize=5)
    profile_ax.grid(axis="y", color="#CBD5E1", linewidth=0.5)
    profile_ax.tick_params(length=0, pad=1)
    for spine in profile_ax.spines.values():
        spine.set_color("#CBD5E1")
        spine.set_linewidth(0.6)
    profile_ax.set_title(
        "地形高度 · 地形標高 / TERRAIN HEIGHT",
        fontsize=6.2,
        fontweight="bold",
        color="#17212B",
        pad=3,
    )

    title = config["title"]
    fig.text(
        0.04,
        0.955,
        f"{title['zh']}  ·  {title['ja']}",
        fontsize=13,
        fontweight="bold",
        color="#17212B",
    )
    fig.text(0.04, 0.91, title["en"], fontsize=8.2, fontweight="bold", color="#1769E0")
    fig.text(
        0.965,
        0.948,
        "地图距离短，山路时间长\n"
        "地図では近く見えても、移動には時間がかかる\n"
        "DISTANCES LOOK SHORT; MOUNTAIN TRAVEL TAKES TIME",
        fontsize=5.6,
        color="#52606D",
        ha="right",
        va="top",
        linespacing=1.25,
    )

    legend_items = [
        ("#E24736", "铁路 / 鉄道 / RAIL"),
        ("#008C72", "缆车 / ケーブルカー / CABLE"),
        ("#7A3EC8", "索道 / ロープウェイ / ROPEWAY"),
        ("#1769E0", "游船 / 船 / CRUISE"),
        ("#52606D", "巴士连接 / バス / BUS LINK"),
    ]
    legend_x = 0.045
    for color, label in legend_items:
        fig.add_artist(
            plt.Line2D(
                [legend_x, legend_x + 0.023],
                [0.035, 0.035],
                transform=fig.transFigure,
                color=color,
                linewidth=2.4,
            )
        )
        fig.text(legend_x + 0.027, 0.035, label, fontsize=4.9, va="center", color="#17212B")
        legend_x += 0.182
    fig.text(
        0.04,
        0.008,
        "节点连线表示换乘结构，并非轨道测绘。出发当天复核天气、火山与交通状态。  "
        "Node links show transfer structure, not surveyed alignments. "
        "Recheck weather, volcano and services on travel day.",
        fontsize=4.7,
        color="#52606D",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {"CreationDate": FIXED_TIME, "ModDate": FIXED_TIME}
    svg_path = OUTPUT_STEM.with_suffix(".svg")
    fig.savefig(svg_path, format="svg", metadata={"Date": None})
    normalize_svg(svg_path)
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), format="pdf", metadata=metadata)
    fig.savefig(OUTPUT_STEM.with_suffix(".png"), format="png", dpi=480, metadata={"Date": None})
    plt.close(fig)
    return {
        "profile": [
            {"id": node["id"], "gsi_terrain_m_rounded_10": value}
            for node, value in zip(profile_nodes, profile_values, strict=True)
        ]
    }


def main() -> int:
    config = read_json(CONFIG_PATH)
    elevation, mosaic_extent, terrain_sources = terrain_mosaic(config)
    geojson, osm_sources = normalized_geojson(config)
    write_json(GEOJSON_PATH, geojson)
    render_details = render_map(config, geojson, elevation, mosaic_extent)
    files = {}
    for suffix in ("svg", "pdf", "png"):
        path = OUTPUT_STEM.with_suffix(f".{suffix}")
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    provenance = {
        "schema_version": 1,
        "asset_id": "asset-hakone-orientation-map",
        "created_at": config["snapshot_date"],
        "method": "map-render",
        "command": "python3 scripts/build_hakone_orientation_map.py",
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "normalized_data": {
            "path": str(GEOJSON_PATH.relative_to(ROOT)),
            "sha256": sha256(GEOJSON_PATH),
        },
        "sources": config["sources"],
        "terrain_tiles": terrain_sources,
        "osm_lookup": osm_sources,
        "declared_generalizations": [
            (
                "Colored node links show the operator's transfer structure and are not "
                "surveyed rail, cable, ropeway, bus, or ship alignments"
            ),
            (
                "The elevation profile samples GSI terrain at transfer nodes, rounds to "
                "10 metres, and is not a station-platform survey"
            ),
        ],
        "render_details": render_details,
        "rights": (
            "Map design © LazyTravel; elevation data from GSI; water and node "
            "locations © OpenStreetMap contributors, ODbL 1.0."
        ),
        "files": files,
        "technical_qa": {
            "minimum_png_width": 2400,
            "pdf_vector_output": True,
            "png_dimensions": list(Image.open(OUTPUT_STEM.with_suffix(".png")).size),
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
                    "Full-resolution SVG and PNG show no overlapping place labels or "
                    "clipped legend text."
                ),
                (
                    "Compiled B6 landscape review keeps node labels, transport modes, "
                    "north arrow, caveat, and elevation profile legible; evidence "
                    "build/qa/books/hakone/ch01-milestone/page-08.png, sha256 "
                    "397a3dfe3c156adb53f07f4d039c24605d87f71010ee9c1a88192f70a4dba4eb."
                ),
                (
                    "At 390 px, the website keeps the SVG in a pannable 760 px viewport "
                    "with working zoom and reset controls instead of shrinking the full "
                    "map; evidence build/qa/site/hakone-ch01/mobile-01-map.png, sha256 "
                    "e45757f045c966ee0214d467dffeefbe5c3b1c144b4d86546bf71db5c9db586a."
                ),
            ],
        },
    }
    write_json(OUTPUT_STEM.with_suffix(".provenance.json"), provenance)
    print(f"map: {OUTPUT_STEM.relative_to(ROOT)}.[svg|pdf|png]")
    print(f"geojson: {GEOJSON_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
