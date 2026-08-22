#!/usr/bin/env python3
"""Prepare reproducible print/web variants and provenance for Lanzhou Chapter 6."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/images/lanzhou/ch06-figures.config.json"
OUTPUT_DIR = ROOT / "assets/images/lanzhou"
PRINT_SIZE = (3600, 2025)
WEB_SIZE = (1920, 1080)


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
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def centre_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_ratio = size[0] / size[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        crop_width = round(image.height * target_ratio)
        left = (image.width - crop_width) // 2
        box = (left, 0, left + crop_width, image.height)
    else:
        crop_height = round(image.width / target_ratio)
        top = (image.height - crop_height) // 2
        box = (0, top, image.width, top + crop_height)
    return image.crop(box).resize(size, Image.Resampling.LANCZOS)


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
    guide_sources = []
    for guide in config["guides"]:
        path = resolve_path(guide["path"])
        if not path.is_file():
            raise FileNotFoundError(path)
        guide_sources.append(
            {"path": guide["path"], "sha256": sha256(path), "role": guide["role"]}
        )

    for figure in config["figures"]:
        raw_path = resolve_path(figure["selected_raw"])
        prompt_path = resolve_path(figure["prompt"])
        if not raw_path.is_file() or not prompt_path.is_file():
            raise FileNotFoundError(raw_path if not raw_path.is_file() else prompt_path)

        with Image.open(raw_path) as opened:
            source = ImageOps.exif_transpose(opened).convert("RGB")
            print_image = centre_crop(source, PRINT_SIZE)
            web_image = centre_crop(source, WEB_SIZE)

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
                    "path": reference["path"],
                    "sha256": sha256(path),
                    "reference_url": reference["reference_url"],
                    "role": reference["role"],
                }
            )

        lineage = []
        selected_manifest: dict[str, Any] | None = None
        for item in figure["provider_lineage"]:
            path = resolve_path(item["path"])
            if not path.is_file():
                raise FileNotFoundError(path)
            manifest = json.loads(path.read_text(encoding="utf-8"))
            lineage.append({**path_record(path), "role": item["role"]})
            if "Selected" in item["role"]:
                selected_manifest = manifest
        if selected_manifest is None:
            raise RuntimeError(f"selected provider lineage is missing: {figure['asset_id']}")

        qa = dict(figure["visual_qa"])
        evidence = figure.get("qa_evidence")
        if evidence:
            b6_path = resolve_path(evidence["b6_path"])
            mobile_path = resolve_path(evidence["mobile_path"])
            if not b6_path.is_file() or not mobile_path.is_file():
                raise FileNotFoundError(b6_path if not b6_path.is_file() else mobile_path)
            qa["evidence"] = {
                "b6": {**path_record(b6_path), "physical_page": evidence["physical_page"]},
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
            "prompt": {"path": figure["prompt"], "sha256": sha256(prompt_path)},
            "provider_lineage": lineage,
            "selected_raw": path_record(raw_path, include_dimensions=True),
            "postprocess": "Pillow sRGB conversion, centre-cropped 16:9 print/web variants, Lanczos resampling, JPEG quality 92; web quality 88",
            "output": {**path_record(print_path, include_dimensions=True), "color_space": "sRGB"},
            "variants": {"web": path_record(web_path, include_dimensions=True)},
            "factual_limits": figure["factual_limits"],
            "reader_caption_policy": figure["reader_caption_policy"],
            "rights": "Original LazyTravel composition; external imagery was used only as an unredistributed visual reference",
            "visual_qa": qa,
        }
        provenance_path = stem.with_suffix(".provenance.json")
        provenance_path.write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"figure: {print_path.relative_to(ROOT)}")
        print(f"web: {web_path.relative_to(ROOT)}")
        print(f"provenance: {provenance_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
