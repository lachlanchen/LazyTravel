#!/usr/bin/env python3
"""Extract an EPUB spine and referenced figures into an ignored research cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import posixpath
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/sources/catalog.json"
CONTAINER_XML = "META-INF/container.xml"
TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "figcaption"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_member(name: str) -> str:
    normalized = posixpath.normpath(name.replace("\\", "/"))
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe EPUB member path: {name}")
    return pure.as_posix()


def resolve_member(base: str, href: str) -> str:
    clean_href = href.split("#", 1)[0].split("?", 1)[0]
    return safe_member(posixpath.join(posixpath.dirname(base), clean_href))


def find_source(source_id: str) -> dict[str, Any]:
    catalog = read_json(CATALOG)
    matches = [source for source in catalog["sources"] if source["id"] == source_id]
    if len(matches) != 1:
        raise ValueError(f"source id must match exactly once: {source_id}")
    source = matches[0]
    if source["kind"] != "epub":
        raise ValueError(f"source is not an EPUB: {source_id}")
    return source


def parse_package(archive: zipfile.ZipFile) -> tuple[str, ET.Element]:
    container = ET.fromstring(archive.read(CONTAINER_XML))
    rootfile = container.find(".//{*}rootfile")
    if rootfile is None or not rootfile.attrib.get("full-path"):
        raise ValueError("EPUB container has no package rootfile")
    package_path = safe_member(rootfile.attrib["full-path"])
    return package_path, ET.fromstring(archive.read(package_path))


def text_blocks(raw: bytes, document_path: str) -> tuple[list[dict[str, Any]], list[str]]:
    soup = BeautifulSoup(raw, "xml")
    for node in soup.find_all(["script", "style"]):
        node.decompose()

    image_members: list[str] = []
    for image in soup.find_all("img"):
        src = image.get("src")
        if src:
            image_members.append(resolve_member(document_path, src))

    blocks: list[dict[str, Any]] = []
    for sequence, node in enumerate(soup.find_all(list(TEXT_TAGS)), start=1):
        if node.find_parent(TEXT_TAGS):
            continue
        text = re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()
        if not text:
            continue
        blocks.append(
            {
                "sequence": sequence,
                "tag": node.name,
                "text": text,
            }
        )
    return blocks, image_members


def extract(source: dict[str, Any], output_root: Path) -> dict[str, Any]:
    source_path = Path(source["path"])
    source_hash = sha256_file(source_path)
    if source_hash != source["sha256"]:
        raise RuntimeError(
            f"source checksum mismatch for {source['id']}: "
            f"expected {source['sha256']}, got {source_hash}"
        )

    output_dir = output_root / source["id"]
    asset_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source_path) as archive:
        archive_names = {
            safe_member(name): name for name in archive.namelist() if not name.endswith("/")
        }
        package_path, package = parse_package(archive)
        manifest_by_id: dict[str, dict[str, str]] = {}
        for item in package.findall(".//{*}manifest/{*}item"):
            item_id = item.attrib.get("id")
            href = item.attrib.get("href")
            if item_id and href:
                manifest_by_id[item_id] = {
                    "href": resolve_member(package_path, href),
                    "media_type": item.attrib.get("media-type", ""),
                }

        spine_ids = [
            node.attrib["idref"]
            for node in package.findall(".//{*}spine/{*}itemref")
            if node.attrib.get("idref")
        ]
        documents: list[dict[str, Any]] = []
        referenced_images: list[str] = []
        markdown_parts: list[str] = [f"# {source['title']}"]

        for spine_index, item_id in enumerate(spine_ids, start=1):
            item = manifest_by_id.get(item_id)
            if item is None:
                raise ValueError(f"spine item missing from package manifest: {item_id}")
            member = item["href"]
            if member not in archive_names:
                raise FileNotFoundError(f"EPUB spine document missing: {member}")
            raw = archive.read(archive_names[member])
            blocks, image_members = text_blocks(raw, member)
            referenced_images.extend(image_members)
            documents.append(
                {
                    "spine_index": spine_index,
                    "item_id": item_id,
                    "member": member,
                    "media_type": item["media_type"],
                    "sha256": sha256_bytes(raw),
                    "blocks": blocks,
                    "image_members": image_members,
                }
            )
            markdown_parts.append(f"\n<!-- spine:{spine_index} member:{member} -->")
            for block in blocks:
                prefix = (
                    "#" * int(block["tag"][1]) + " "
                    if re.fullmatch(r"h[1-6]", block["tag"])
                    else ""
                )
                markdown_parts.append(f"\n{prefix}{block['text']}")

        figures: list[dict[str, Any]] = []
        for member in sorted(set(referenced_images)):
            original = archive_names.get(member)
            if original is None:
                figures.append({"member": member, "status": "missing"})
                continue
            data = archive.read(original)
            digest = sha256_bytes(data)
            suffix = (
                Path(member).suffix.lower()
                or mimetypes.guess_extension(mimetypes.guess_type(member)[0] or "")
                or ".bin"
            )
            safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(member).stem).strip("-") or "image"
            destination = asset_dir / f"{digest[:12]}-{safe_stem}{suffix}"
            if not destination.exists() or sha256_file(destination) != digest:
                destination.write_bytes(data)
            figures.append(
                {
                    "member": member,
                    "path": destination.relative_to(output_dir).as_posix(),
                    "sha256": digest,
                    "bytes": len(data),
                    "media_type": mimetypes.guess_type(member)[0] or "application/octet-stream",
                    "status": "extracted",
                    "publishable": False,
                }
            )

    result = {
        "schema_version": 1,
        "source_id": source["id"],
        "source_path": str(source_path),
        "source_sha256": source_hash,
        "rights_status": source["rights"]["status"],
        "raw_extraction_publishable": False,
        "extractor": {
            "name": "LazyTravel EPUB spine extractor",
            "design_reference": (
                "/home/lachlan/ProjectsLFS/ZhJpBook/scripts/books/" "build_pocket_tex_queue.py"
            ),
            "safety": [
                "source-hash-gate",
                "zip-path-traversal-rejection",
                "content-addressed-assets",
            ],
        },
        "package_path": package_path,
        "spine_count": len(documents),
        "block_count": sum(len(document["blocks"]) for document in documents),
        "figure_count": len(figures),
        "missing_figure_count": sum(figure["status"] == "missing" for figure in figures),
        "documents": documents,
        "figures": figures,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "source.md").write_text(
        "\n".join(markdown_parts).strip() + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-id", required=True)
    parser.add_argument(
        "--output-root", type=Path, default=ROOT / "build/research/xian/source-extraction"
    )
    args = parser.parse_args()

    source = find_source(args.source_id)
    result = extract(source, args.output_root.resolve())
    print(
        json.dumps(
            {
                "source_id": result["source_id"],
                "spine_count": result["spine_count"],
                "block_count": result["block_count"],
                "figure_count": result["figure_count"],
                "missing_figure_count": result["missing_figure_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["missing_figure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
