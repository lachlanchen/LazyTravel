#!/usr/bin/env python3
"""Build and validate the static LazyTravel website from canonical book JSON."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/china/cities/xian/book.json"
DEFAULT_OUTPUT = ROOT / "site"
WEBSITE_SOURCE = ROOT / "website"
STATIC_FILES = ("index.html", "styles.css", "app.js")
PAYLOAD_PATH = Path("data/destination.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def public_projection(document: dict[str, Any]) -> dict[str, Any]:
    """Remove workstation-only citation paths without changing editorial content."""
    projected = copy.deepcopy(document)
    for citation in projected["citations"]:
        citation.pop("path", None)
    return projected


def public_provenance(value: Any) -> Any:
    """Remove local filesystem coordinates from a publishable provenance record."""
    if isinstance(value, dict):
        return {
            key: public_provenance(item)
            for key, item in value.items()
            if not (
                isinstance(item, str)
                and (item.startswith("/home/") or "ProjectsLFS" in item)
            )
        }
    if isinstance(value, list):
        return [public_provenance(item) for item in value]
    return value


def asset_paths(document: dict[str, Any]) -> set[Path]:
    paths: set[Path] = set()
    for asset in document["assets"]:
        for value in [asset["path"], *asset.get("variants", {}).values()]:
            candidate = ROOT / value
            if candidate.exists():
                paths.add(candidate)
        provenance = (ROOT / asset["path"]).with_suffix(".provenance.json")
        if provenance.exists():
            paths.add(provenance)
    return paths


def reading_counts(document: dict[str, Any]) -> dict[str, int]:
    counts = {"blocks": 0, "zh_tokens": 0, "ja_tokens": 0}
    for chapter in document["chapters"]:
        for block in chapter["blocks"]:
            counts["blocks"] += 1
            counts["zh_tokens"] += len(block["readings"]["zh"]["tokens"])
            counts["ja_tokens"] += len(block["readings"]["ja"]["tokens"])
    return counts


def validate_output(
    book_path: Path,
    output: Path,
    *,
    allow_pending_visual_qa: bool = False,
) -> dict[str, int]:
    source = json.loads(book_path.read_text(encoding="utf-8"))
    payload_path = output / PAYLOAD_PATH
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    build_meta = payload.pop("_build", None)
    if payload != public_projection(source):
        raise RuntimeError("website payload differs from the canonical public projection")
    if not build_meta or build_meta.get("source_sha256") != sha256(book_path):
        raise RuntimeError("website payload does not identify the current canonical JSON")

    for chapter in source["chapters"]:
        for block in chapter["blocks"]:
            for language in ("zh", "ja"):
                reconstructed = "".join(
                    token["text"] for token in block["readings"][language]["tokens"]
                )
                if reconstructed != block["text"][language]:
                    raise RuntimeError(f"reading parity failed: {block['id']} {language}")

    used_asset_ids = {
        asset_id
        for chapter in source["chapters"]
        for block in chapter["blocks"]
        for asset_id in block["asset_ids"]
    }
    for asset in source["assets"]:
        if asset["id"] not in used_asset_ids:
            continue
        qa = asset["qa"]
        if not qa["approved"] or any(
            qa[field] != "pass" for field in ("resolution", "legibility", "content")
        ):
            raise RuntimeError(f"website asset has not passed visual QA: {asset['id']}")
        if asset["kind"] == "map":
            provenance_path = output / Path(asset["path"]).with_suffix(".provenance.json")
            visual = json.loads(provenance_path.read_text(encoding="utf-8"))["visual_qa"]
            visual_pending = not visual["approved"] or any(
                visual[field] != "pass"
                for field in ("print_300dpi", "mobile_390px", "label_collisions")
            )
            if visual_pending and not allow_pending_visual_qa:
                raise RuntimeError(
                    f"website map provenance has not passed visual QA: {asset['id']}"
                )

    required = [output / filename for filename in STATIC_FILES]
    required.extend(output / path.relative_to(ROOT) for path in asset_paths(source))
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError(f"website build is missing files: {', '.join(missing)}")

    for path in output.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".pdf"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "/home/" in text or "ProjectsLFS" in text:
            raise RuntimeError(f"website leaks a workstation path: {path.relative_to(output)}")

    index = (output / "index.html").read_text(encoding="utf-8")
    javascript = (output / "app.js").read_text(encoding="utf-8")
    for marker in (
        "chapter-select",
        "section-select",
        "ruby-toggle",
        "chapter-outline",
        "section-outline",
    ):
        if marker not in index:
            raise RuntimeError(f"website shell is missing required control: {marker}")
    for marker in (
        "renderTokens",
        "renderMap",
        "renderFigure",
        "activateChapter",
        "renderSources",
        str(PAYLOAD_PATH),
    ):
        if marker not in javascript:
            raise RuntimeError(f"website renderer is missing required behavior: {marker}")
    return reading_counts(source)


def build(
    book_path: Path,
    output: Path,
    *,
    review_preview: bool = False,
) -> dict[str, int]:
    document = json.loads(book_path.read_text(encoding="utf-8"))
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    for filename in STATIC_FILES:
        shutil.copyfile(WEBSITE_SOURCE / filename, output / filename)

    for source_path in asset_paths(document):
        destination = output / source_path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source_path.name.endswith(".provenance.json"):
            provenance = json.loads(source_path.read_text(encoding="utf-8"))
            destination.write_text(
                json.dumps(public_provenance(provenance), ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )
        else:
            shutil.copyfile(source_path, destination)

    payload = public_projection(document)
    payload["_build"] = {
        "source": str(book_path.relative_to(ROOT)),
        "source_sha256": sha256(book_path),
        "command": "python3 scripts/build_website.py",
    }
    data_dir = output / "data"
    data_dir.mkdir(parents=True)
    (output / PAYLOAD_PATH).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    counts = validate_output(
        book_path,
        output,
        allow_pending_visual_qa=review_preview,
    )
    files = {
        str(path.relative_to(output)): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    manifest = {
        "schema_version": 1,
        "destination": document["book"]["id"],
        "edition": document["book"]["edition"],
        "command": "python3 scripts/build_website.py",
        "source_json": {
            "path": str(book_path.relative_to(ROOT)),
            "sha256": sha256(book_path),
        },
        "release_ready": not review_preview,
        "parity": {"status": "pass", **counts},
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--review-preview",
        action="store_true",
        help="build a local review preview while platform visual QA is pending",
    )
    args = parser.parse_args()
    counts = build(
        args.book.resolve(),
        args.output.resolve(),
        review_preview=args.review_preview,
    )
    label = "review website" if args.review_preview else "validated website"
    print(
        f"{label}: {args.output} "
        f"({counts['blocks']} blocks, {counts['zh_tokens']} zh tokens, "
        f"{counts['ja_tokens']} ja tokens)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
