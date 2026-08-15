#!/usr/bin/env python3
"""Build and validate the deterministic Xi'an B6 pocket review."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/xian/book.json"
BOOK_SCHEMA = ROOT / "schemas/destination-book.schema.json"
SOURCE_CATALOG = ROOT / "data/sources/catalog.json"
SOURCE_SCHEMA = ROOT / "schemas/source-catalog.schema.json"
CHAPTER_IDS = (
    "ch01-ground-before-time",
    "ch02-capitals-on-different-maps",
    "ch03-army-under-earth",
    "ch04-let-text-lead",
    "ch05-inside-the-wall",
    "ch06-beginning-with-bread",
    "ch07-beyond-the-center",
)
BUILD_DIR = ROOT / "build/books/xian/pocket-review"
DIST_DIR = ROOT / "dist/books/xian"
DIST_PDF = DIST_DIR / "xian-pocket-review.pdf"
DIST_MANIFEST = DIST_DIR / "xian-pocket-review.manifest.json"
SOURCE_DATE_EPOCH = "1786723200"
EXPECTED_PAGE_POINTS = (125 / 25.4 * 72, 176 / 25.4 * 72)
LOG_REJECTION = re.compile(
    r"Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning|"
    r"^! |:[0-9]+: .*Error",
    re.MULTILINE,
)
REQUIRED_FIGURE_GUIDES = frozenset(
    {
        "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png",
        "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg",
    }
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_tools(names: list[str]) -> None:
    missing = [name for name in names if shutil.which(name) is None]
    if missing:
        raise RuntimeError(f"missing build tools: {', '.join(missing)}")


def run(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    printable = " ".join(command)
    print(f"+ {printable}")
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed with exit code {completed.returncode}: {printable}\n"
            f"{completed.stdout}"
        )
    return completed.stdout


def validate_log(path: Path) -> None:
    log = path.read_text(encoding="utf-8", errors="replace")
    rejected = sorted(set(match.group(0) for match in LOG_REJECTION.finditer(log)))
    if rejected:
        raise RuntimeError(f"TeX log contains rejected diagnostics: {', '.join(rejected)}")


def validate_fonts(output: str) -> int:
    rows = [
        line.split()
        for line in output.splitlines()
        if line.strip() and not line.startswith(("name ", "---"))
    ]
    if not rows:
        raise RuntimeError("pdffonts reported no embedded fonts")
    unembedded = [row[0] for row in rows if len(row) < 6 or row[-5] != "yes"]
    if unembedded:
        raise RuntimeError(f"PDF contains unembedded fonts: {', '.join(unembedded)}")
    return len(rows)


def extract_page_count(output: str) -> int:
    match = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not report a page count")
    return int(match.group(1))


def extract_page_size(output: str) -> tuple[float, float]:
    match = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", output, re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not report a page size")
    return float(match.group(1)), float(match.group(2))


def validate_figure_cast(asset_id: str, provenance: dict[str, Any]) -> None:
    reference_paths = {
        source.get("path") for source in provenance.get("source_images", [])
    }
    missing = sorted(REQUIRED_FIGURE_GUIDES - reference_paths)
    if missing:
        raise RuntimeError(
            f"non-map asset is missing required Aya-chan/Lala Xia references: "
            f"{asset_id}: {', '.join(missing)}"
        )


def validate_asset_qa(document: dict[str, Any]) -> None:
    chapters = {chapter["id"]: chapter for chapter in document["chapters"]}
    asset_ids = {
        asset_id
        for chapter_id in CHAPTER_IDS
        for block in chapters[chapter_id]["blocks"]
        for asset_id in block["asset_ids"]
    }
    assets = {asset["id"]: asset for asset in document["assets"]}
    for asset_id in asset_ids:
        asset = assets[asset_id]
        asset_path = ROOT / asset["path"]
        if not asset_path.is_file():
            raise RuntimeError(f"asset file is missing: {asset_id}")
        qa = asset["qa"]
        if not qa["approved"] or any(
            qa[field] != "pass" for field in ("resolution", "legibility", "content")
        ):
            raise RuntimeError(f"asset has not passed visual QA: {asset_id}")
        provenance_path = asset_path.with_suffix(".provenance.json")
        if not provenance_path.is_file():
            raise RuntimeError(f"asset provenance is missing: {asset_id}")
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        if asset["kind"] != "map":
            validate_figure_cast(asset_id, provenance)
            if provenance.get("output", {}).get("sha256") != sha256(asset_path):
                raise RuntimeError(f"asset provenance hash mismatch: {asset_id}")
            continue
        visual = provenance["visual_qa"]
        if not visual["approved"] or any(
            visual[field] != "pass"
            for field in ("print_300dpi", "mobile_390px", "label_collisions")
        ):
            raise RuntimeError(f"map provenance has not passed visual QA: {asset_id}")


def build_inputs(document: dict[str, Any]) -> list[Path]:
    inputs = {
        BOOK_PATH,
        BOOK_SCHEMA,
        SOURCE_CATALOG,
        SOURCE_SCHEMA,
        ROOT / "books/china/cities/xian/latex/book.tex",
        ROOT / "scripts/build_xian_review.py",
        ROOT / "scripts/build_xian_orientation_map.py",
        ROOT / "scripts/build_xian_capital_layers_map.py",
        ROOT / "scripts/build_xian_qin_mausoleum_pits_map.py",
        ROOT / "scripts/build_xian_written_word_route_map.py",
        ROOT / "scripts/build_xian_inside_wall_route_map.py",
        ROOT / "scripts/build_xian_food_contexts_map.py",
        ROOT / "scripts/build_xian_nearby_day_choices_map.py",
        ROOT / "scripts/render_destination_tex.py",
        ROOT / "scripts/validate_json.py",
        ROOT / "scripts/validate_readings.py",
        ROOT / "data/maps/xian/xian-before-walls.config.json",
        ROOT / "data/maps/xian/xian-before-walls.geojson",
        ROOT / "data/maps/xian/xian-capital-layers.config.json",
        ROOT / "data/maps/xian/xian-qin-mausoleum-pits.config.json",
        ROOT / "data/maps/xian/xian-written-word-route.config.json",
        ROOT / "data/maps/xian/xian-inside-wall-route.config.json",
        ROOT / "data/maps/xian/xian-inside-wall-route.geojson",
        ROOT / "data/maps/xian/xian-food-contexts.config.json",
        ROOT / "data/maps/xian/xian-nearby-day-choices.config.json",
        ROOT / "data/maps/xian/xian-before-walls.geojson",
        ROOT / "data/images/xian/xian-daming-site-impression.prompt.md",
        ROOT / "data/images/xian/xian-terracotta-conservation-impression.prompt.md",
        ROOT / "data/images/xian/xian-rubbing-replica-demonstration.prompt.md",
        ROOT / "data/images/xian/xian-big-wild-goose-pagoda-visit.prompt.md",
        ROOT / "data/images/xian/xian-lane-courtyard-threshold.prompt.md",
        ROOT / "data/images/xian/xian-city-wall-walk.prompt.md",
        ROOT / "data/images/xian/xian-breaking-mo-table.prompt.md",
        ROOT / "data/images/xian/xian-managed-mountain-day.prompt.md",
        ROOT / "data/images/xian/xian-yongning-gate-arrival.prompt.md",
        ROOT / "data/images/xian/xian-terracotta-pit-one-visit.prompt.md",
        ROOT / "data/images/xian/xian-bell-tower-orientation.prompt.md",
    }
    chapters = {chapter["id"]: chapter for chapter in document["chapters"]}
    used_asset_ids = {
        asset_id
        for chapter_id in CHAPTER_IDS
        for block in chapters[chapter_id]["blocks"]
        for asset_id in block["asset_ids"]
    }
    for asset in document["assets"]:
        if asset["id"] not in used_asset_ids:
            continue
        for value in [asset["path"], *asset.get("variants", {}).values()]:
            path = ROOT / value
            if path.is_file():
                inputs.add(path)
        provenance = (ROOT / asset["path"]).with_suffix(".provenance.json")
        if provenance.is_file():
            inputs.add(provenance)
    return sorted(inputs)


def write_manifest(
    document: dict[str, Any], page_count: int, font_count: int, text_characters: int
) -> None:
    inputs = build_inputs(document)
    manifest = {
        "schema_version": 1,
        "artifact": str(DIST_PDF.relative_to(ROOT)),
        "chapter_ids": list(CHAPTER_IDS),
        "build_date": "2026-08-15",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "command": "python3 scripts/build_xian_review.py",
        "inputs": {
            str(path.relative_to(ROOT)): {"sha256": sha256(path), "bytes": path.stat().st_size}
            for path in inputs
        },
        "output": {
            "sha256": sha256(DIST_PDF),
            "bytes": DIST_PDF.stat().st_size,
            "pages": page_count,
            "trim_mm": [125, 176],
            "embedded_fonts": font_count,
            "searchable_characters": text_characters,
            "qpdf_check": "pass",
            "tex_log": "pass",
        },
    }
    DIST_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-map",
        action="store_true",
        help="reuse the committed map variants instead of regenerating them",
    )
    args = parser.parse_args()

    require_tools(["xelatex", "qpdf", "pdffonts", "pdfinfo", "pdftotext"])
    if not args.skip_map:
        run([sys.executable, "scripts/build_xian_orientation_map.py"])
        run([sys.executable, "scripts/build_xian_capital_layers_map.py"])
        run([sys.executable, "scripts/build_xian_qin_mausoleum_pits_map.py"])
        run([sys.executable, "scripts/build_xian_written_word_route_map.py"])
        run([sys.executable, "scripts/build_xian_inside_wall_route_map.py"])
        run([sys.executable, "scripts/build_xian_food_contexts_map.py"])
        run([sys.executable, "scripts/build_xian_nearby_day_choices_map.py"])
    run(
        [
            sys.executable,
            "scripts/validate_json.py",
            str(SOURCE_CATALOG),
            "--schema",
            str(SOURCE_SCHEMA),
        ]
    )
    run(
        [
            sys.executable,
            "scripts/validate_json.py",
            str(BOOK_PATH),
            "--schema",
            str(BOOK_SCHEMA),
        ]
    )
    run([sys.executable, "scripts/validate_readings.py", "--book", str(BOOK_PATH)])
    document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
    validate_asset_qa(document)
    render_command = [
        sys.executable,
        "scripts/render_destination_tex.py",
        "--book",
        str(BOOK_PATH),
        "--output-dir",
        str(BUILD_DIR),
    ]
    for chapter_id in CHAPTER_IDS:
        render_command.extend(["--chapter", chapter_id])
    run(render_command)

    tex_env = os.environ.copy()
    tex_env.update({"SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH, "FORCE_SOURCE_DATE": "1"})
    tex_command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "main.tex",
    ]
    run(tex_command, cwd=BUILD_DIR, env=tex_env)
    run(tex_command, cwd=BUILD_DIR, env=tex_env)

    pdf = BUILD_DIR / "main.pdf"
    log = BUILD_DIR / "main.log"
    validate_log(log)
    run(["qpdf", "--check", str(pdf)])
    font_count = validate_fonts(run(["pdffonts", str(pdf)]))
    info = run(["pdfinfo", str(pdf)])
    page_count = extract_page_count(info)
    page_size = extract_page_size(info)
    if any(
        abs(actual - expected) > 0.25 for actual, expected in zip(page_size, EXPECTED_PAGE_POINTS)
    ):
        raise RuntimeError(f"PDF is not B6 125 x 176 mm: {page_size[0]} x {page_size[1]} pt")
    if page_count < 50:
        raise RuntimeError(f"unexpectedly short review PDF: {page_count} pages")
    text = run(["pdftotext", str(pdf), "-"])
    text_characters = len("".join(text.split()))
    if text_characters < 55_000:
        raise RuntimeError(f"PDF text layer is unexpectedly short: {text_characters} characters")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, DIST_PDF)
    write_manifest(document, page_count, font_count, text_characters)
    print(f"validated PDF: {DIST_PDF.relative_to(ROOT)}")
    print(f"manifest: {DIST_MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
