#!/usr/bin/env python3
"""Prepare reproducible full-frame figure variants for Hakone Chapter 11."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/images/hakone/ch11-figures.config.json"
OUTPUT_DIR = ROOT / "assets/images/hakone"
PRINT_WIDTH = 3600
WEB_WIDTH = 1920


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def display_path(path: Path) -> str:
    if path.is_absolute() and not path.is_relative_to(ROOT):
        return str(path)
    return str(path.relative_to(ROOT))


def path_record(path: Path, *, include_dimensions: bool = False) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": display_path(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }
    if include_dimensions:
        with Image.open(path) as image:
            record.update({"width": image.width, "height": image.height})
    return record


def resize_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_jpeg(image: Image.Image, path: Path, quality: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(
        path,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling=0,
    )


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    guide_sources: list[dict[str, Any]] = []
    for guide in config["guides"]:
        path = resolve_path(guide["path"])
        if not path.is_file():
            raise FileNotFoundError(path)
        guide_sources.append({**path_record(path), "role": guide["role"]})

    for figure in config["figures"]:
        raw_path = resolve_path(figure["selected_raw"])
        prompt_path = resolve_path(figure["prompt"])
        if not raw_path.is_file() or not prompt_path.is_file():
            raise FileNotFoundError(raw_path if not raw_path.is_file() else prompt_path)

        with Image.open(raw_path) as opened:
            source = ImageOps.exif_transpose(opened).convert("RGB")
            print_image = resize_width(source, PRINT_WIDTH)
            web_image = resize_width(source, WEB_WIDTH)

        stem = OUTPUT_DIR / figure["stem"]
        print_path = stem.with_suffix(".jpg")
        web_path = stem.with_name(f"{stem.name}-web.jpg")
        save_jpeg(print_image, print_path, 92)
        save_jpeg(web_image, web_path, 88)

        source_images = list(guide_sources)
        for reference in figure["official_references"]:
            path = resolve_path(reference["path"])
            if not path.is_file():
                raise FileNotFoundError(path)
            source_images.append(
                {
                    **path_record(path),
                    "page_url": reference["page_url"],
                    "role": reference["role"],
                }
            )

        lineage: list[dict[str, Any]] = []
        selected_manifest: dict[str, Any] | None = None
        for item in figure["provider_lineage"]:
            path = resolve_path(item["path"])
            if not path.is_file():
                raise FileNotFoundError(path)
            manifest = json.loads(path.read_text(encoding="utf-8"))
            lineage.append({**path_record(path), "role": item["role"]})
            if item["role"].startswith("Selected"):
                selected_manifest = manifest
        if selected_manifest is None:
            raise RuntimeError(f"selected provider lineage is missing: {figure['asset_id']}")

        qa = dict(config["visual_qa"])
        evidence = figure.get("qa_evidence")
        if evidence:
            b6_path = resolve_path(evidence["b6_path"])
            mobile_path = resolve_path(evidence["mobile_path"])
            if not b6_path.is_file() or not mobile_path.is_file():
                raise FileNotFoundError(b6_path if not b6_path.is_file() else mobile_path)
            qa["evidence"] = {
                "b6": {
                    **path_record(b6_path),
                    "physical_page": evidence["physical_page"],
                },
                "mobile": {
                    **path_record(mobile_path, include_dimensions=True),
                    "viewport_css_px": evidence["viewport_css_px"],
                    "display_width_css_px": evidence["display_width_css_px"],
                },
            }
        elif qa["approved"]:
            raise RuntimeError(f"approved figure lacks QA evidence: {figure['asset_id']}")

        provenance = {
            "schema_version": 1,
            "asset_id": figure["asset_id"],
            "created_at": config["created_at"],
            "method": figure["method"],
            "generator": config["generator"],
            "task_id": selected_manifest["taskId"],
            "source_images": source_images,
            "fact_sources": figure["fact_sources"],
            "prompt": {"path": figure["prompt"], "sha256": sha256(prompt_path)},
            "provider_lineage": lineage,
            "selected_raw": path_record(raw_path, include_dimensions=True),
            "postprocess": (
                "Pillow EXIF transpose and sRGB conversion; uncropped full-frame "
                "Lanczos resize; metadata-free JPEG quality 92 for print and 88 for web"
            ),
            "output": {
                **path_record(print_path, include_dimensions=True),
                "color_space": "sRGB",
            },
            "variants": {"web": path_record(web_path, include_dimensions=True)},
            "factual_limits": figure["factual_limits"],
            "reader_caption_policy": figure["reader_caption_policy"],
            "rights": (
                "Original LazyTravel composition; external location and character "
                "references are hash-pinned and not redistributed"
            ),
            "visual_qa": qa,
        }
        provenance_path = stem.with_suffix(".provenance.json")
        provenance_path.write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"figure: {print_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
