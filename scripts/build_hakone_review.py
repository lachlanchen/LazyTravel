#!/usr/bin/env python3
"""Build, validate, and optionally sync the current Hakone B6 pocket review."""

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
BOOK_PATH = ROOT / "data/japan/prefectures/kanagawa/hakone/book.json"
BOOK_SCHEMA = ROOT / "schemas/destination-book.schema.json"
SOURCE_CATALOG = ROOT / "data/sources/catalog.json"
SOURCE_SCHEMA = ROOT / "schemas/source-catalog.schema.json"
COVER_ASSET = ROOT / "assets/images/hakone/hakone-cover-underlay.png"
COVER_PROVENANCE = COVER_ASSET.with_suffix(".provenance.json")
BUILD_DIR = ROOT / "build/books/hakone/pocket-review"
DIST_DIR = ROOT / "dist/books/hakone"
DIST_PDF = DIST_DIR / "hakone-pocket-review.pdf"
DIST_MANIFEST = DIST_DIR / "hakone-pocket-review.manifest.json"
NUTSTORE_PDF = (
    Path("/home/lachlan/Nutstore Files/Share/LazyTravel")
    / "LazyTravel-Hakone-ZH-JA-EN-B6-Pocket.pdf"
)
SOURCE_DATE_EPOCH = "1786924800"
EXPECTED_PAGE_POINTS = (125 / 25.4 * 72, 176 / 25.4 * 72)
EXPECTED_CHAPTERS = 11
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


def active_chapter_ids(document: dict[str, Any]) -> list[str]:
    chapters = sorted(document["chapters"], key=lambda chapter: chapter["order"])
    if len(chapters) != EXPECTED_CHAPTERS:
        raise RuntimeError(
            f"Hakone structure must remain exactly {EXPECTED_CHAPTERS} chapters"
        )
    active = [chapter for chapter in chapters if chapter["blocks"]]
    if not active:
        raise RuntimeError("Hakone has no compiled chapter content")
    expected_orders = list(range(1, len(active) + 1))
    if [chapter["order"] for chapter in active] != expected_orders:
        raise RuntimeError("compiled Hakone chapters must form a consecutive prefix")
    return [chapter["id"] for chapter in active]


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


def validate_variant_hash(path: Path, provenance: dict[str, Any]) -> None:
    candidates = [provenance.get("output", {})]
    candidates.extend(provenance.get("variants", {}).values())
    record = next(
        (item for item in candidates if item.get("path") == str(path.relative_to(ROOT))),
        None,
    )
    if record and record.get("sha256") != sha256(path):
        raise RuntimeError(f"asset provenance hash mismatch: {path.relative_to(ROOT)}")


def validate_asset_qa(document: dict[str, Any], chapter_ids: list[str]) -> None:
    chapters = {chapter["id"]: chapter for chapter in document["chapters"]}
    used_asset_ids = {
        asset_id
        for chapter_id in chapter_ids
        for block in chapters[chapter_id]["blocks"]
        for asset_id in block["asset_ids"]
    }
    assets = {asset["id"]: asset for asset in document["assets"]}
    for asset_id in sorted(used_asset_ids):
        asset = assets[asset_id]
        qa = asset["qa"]
        if not qa["approved"] or any(
            qa[field] != "pass" for field in ("resolution", "legibility", "content")
        ):
            raise RuntimeError(f"asset has not passed visual QA: {asset_id}")
        paths = {
            ROOT / asset["path"],
            *(ROOT / value for value in asset.get("variants", {}).values()),
        }
        missing = [path for path in paths if not path.is_file()]
        if missing:
            raise RuntimeError(f"asset file is missing: {missing[0].relative_to(ROOT)}")
        provenance_path = (ROOT / asset["path"]).with_suffix(".provenance.json")
        if not provenance_path.is_file():
            raise RuntimeError(f"asset provenance is missing: {asset_id}")
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        for path in paths:
            validate_variant_hash(path, provenance)
        if asset["kind"] == "map":
            visual = provenance["visual_qa"]
            required = ("print_300dpi", "mobile_390px", "label_collisions")
            if not visual["approved"] or any(visual[field] != "pass" for field in required):
                raise RuntimeError(f"map provenance has not passed visual QA: {asset_id}")
            continue
        references = {item.get("path") for item in provenance.get("source_images", [])}
        missing_guides = sorted(REQUIRED_FIGURE_GUIDES - references)
        if missing_guides:
            raise RuntimeError(
                f"non-map asset lacks Aya-chan/Lala Xia references: {asset_id}: "
                f"{', '.join(missing_guides)}"
            )
        visual = provenance.get("visual_qa", {})
        if not visual.get("approved") or any(
            visual.get(field) != "pass" for field in ("b6_print", "mobile_390px")
        ):
            raise RuntimeError(f"figure provenance has not passed visual QA: {asset_id}")


def validate_cover_qa() -> None:
    if not COVER_ASSET.is_file() or not COVER_PROVENANCE.is_file():
        raise RuntimeError("Hakone cover underlay or provenance is missing")
    provenance = json.loads(COVER_PROVENANCE.read_text(encoding="utf-8"))
    output = provenance.get("output", {})
    if output.get("sha256") != sha256(COVER_ASSET):
        raise RuntimeError("Hakone cover provenance hash mismatch")
    if (output.get("width"), output.get("height")) != (1476, 2079):
        raise RuntimeError("Hakone cover is not the required 300 ppi B6 geometry")
    visual = provenance.get("visual_qa", {})
    required = (
        "exact_guide_count_four",
        "aya_and_lala_present",
        "identity_continuity",
        "no_raster_text",
        "live_text_selectable",
        "title_safe_zone",
        "footer_safe_zone",
        "b6_print",
    )
    if not visual.get("approved") or any(visual.get(field) != "pass" for field in required):
        raise RuntimeError("Hakone cover has not passed compiled-page visual QA")


def build_inputs(document: dict[str, Any], chapter_ids: list[str]) -> list[Path]:
    inputs = {
        BOOK_PATH,
        BOOK_SCHEMA,
        SOURCE_CATALOG,
        SOURCE_SCHEMA,
        COVER_ASSET,
        COVER_PROVENANCE,
        ROOT / "books/china/cities/xian/latex/book.tex",
        ROOT / "scripts/build_hakone_review.py",
        ROOT / "scripts/build_hakone_gateway_map.py",
        ROOT / "scripts/build_hakone_gora_slope_map.py",
        ROOT / "scripts/build_hakone_owakudani_decision_map.py",
        ROOT / "scripts/build_hakone_orientation_map.py",
        ROOT / "scripts/render_destination_tex.py",
        ROOT / "scripts/validate_json.py",
        ROOT / "scripts/validate_readings.py",
    }
    for folder in (ROOT / "data/maps/hakone", ROOT / "data/images/hakone"):
        inputs.update(path for path in folder.rglob("*") if path.is_file())
    chapters = {chapter["id"]: chapter for chapter in document["chapters"]}
    used_asset_ids = {
        asset_id
        for chapter_id in chapter_ids
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
    document: dict[str, Any],
    chapter_ids: list[str],
    page_count: int,
    font_count: int,
    text_characters: int,
) -> None:
    inputs = build_inputs(document, chapter_ids)
    manifest = {
        "schema_version": 1,
        "artifact": str(DIST_PDF.relative_to(ROOT)),
        "chapter_ids": chapter_ids,
        "planned_chapters": EXPECTED_CHAPTERS,
        "build_date": "2026-08-17",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "command": "python3 scripts/build_hakone_review.py",
        "inputs": {
            str(path.relative_to(ROOT)): {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
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


def sync_nutstore() -> None:
    NUTSTORE_PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DIST_PDF, NUTSTORE_PDF)
    if sha256(NUTSTORE_PDF) != sha256(DIST_PDF):
        raise RuntimeError("Nutstore copy hash differs from the validated pocket PDF")
    print(f"synced pocket PDF: {NUTSTORE_PDF}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-map", action="store_true")
    parser.add_argument(
        "--sync-nutstore",
        action="store_true",
        help="copy only the verified B6 PDF to the shared LazyTravel folder",
    )
    args = parser.parse_args()

    require_tools(["xelatex", "qpdf", "pdffonts", "pdfinfo", "pdftotext"])
    if not args.skip_map:
        run([sys.executable, "scripts/build_hakone_orientation_map.py"])
        run([sys.executable, "scripts/build_hakone_gateway_map.py"])
        run([sys.executable, "scripts/build_hakone_gora_slope_map.py"])
        run([sys.executable, "scripts/build_hakone_owakudani_decision_map.py"])
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
    chapter_ids = active_chapter_ids(document)
    validate_asset_qa(document, chapter_ids)
    validate_cover_qa()

    render_command = [
        sys.executable,
        "scripts/render_destination_tex.py",
        "--book",
        str(BOOK_PATH),
        "--output-dir",
        str(BUILD_DIR),
    ]
    for chapter_id in chapter_ids:
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
    validate_log(BUILD_DIR / "main.log")
    run(["qpdf", "--check", str(pdf)])
    font_count = validate_fonts(run(["pdffonts", str(pdf)]))
    info = run(["pdfinfo", str(pdf)])
    page_count = extract_page_count(info)
    page_size = extract_page_size(info)
    if any(
        abs(actual - expected) > 0.25
        for actual, expected in zip(page_size, EXPECTED_PAGE_POINTS)
    ):
        raise RuntimeError(f"PDF is not B6 125 x 176 mm: {page_size}")
    if page_count < 14:
        raise RuntimeError(f"unexpectedly short Hakone review PDF: {page_count} pages")
    text = run(["pdftotext", str(pdf), "-"])
    text_characters = len("".join(text.split()))
    if text_characters < 12_000:
        raise RuntimeError(
            f"Hakone PDF text layer is unexpectedly short: {text_characters} characters"
        )
    for marker in ("箱根旅行手册", "箱根旅の手引き", "Hakone Pocket Travel Guide"):
        if marker not in text:
            raise RuntimeError(f"Hakone PDF text layer is missing live cover text: {marker}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, DIST_PDF)
    write_manifest(document, chapter_ids, page_count, font_count, text_characters)
    print(f"validated PDF: {DIST_PDF.relative_to(ROOT)}")
    print(f"manifest: {DIST_MANIFEST.relative_to(ROOT)}")
    if args.sync_nutstore:
        sync_nutstore()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
