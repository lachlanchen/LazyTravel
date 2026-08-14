#!/usr/bin/env python3
"""Build and validate the deterministic Xi'an Chapter 1 review PDF."""

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

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/xian/book.json"
BOOK_SCHEMA = ROOT / "schemas/destination-book.schema.json"
SOURCE_CATALOG = ROOT / "data/sources/catalog.json"
SOURCE_SCHEMA = ROOT / "schemas/source-catalog.schema.json"
CHAPTER_ID = "ch01-ground-before-time"
BUILD_DIR = ROOT / "build/books/xian/ch01-review"
DIST_DIR = ROOT / "dist/books/xian"
DIST_PDF = DIST_DIR / "xian-ch01-review.pdf"
DIST_MANIFEST = DIST_DIR / "xian-ch01-review.manifest.json"
SOURCE_DATE_EPOCH = "1786636800"
LOG_REJECTION = re.compile(
    r"Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning|"
    r"^! |:[0-9]+: .*Error",
    re.MULTILINE,
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


def write_manifest(page_count: int, font_count: int, text_characters: int) -> None:
    inputs = [
        BOOK_PATH,
        BOOK_SCHEMA,
        SOURCE_CATALOG,
        SOURCE_SCHEMA,
        ROOT / "books/china/cities/xian/latex/book.tex",
        ROOT / "scripts/build_xian_review.py",
        ROOT / "scripts/build_xian_orientation_map.py",
        ROOT / "scripts/render_destination_tex.py",
        ROOT / "scripts/validate_json.py",
        ROOT / "assets/maps/xian/xian-before-walls.png",
        ROOT / "assets/maps/xian/xian-before-walls.provenance.json",
        ROOT / "data/maps/xian/xian-before-walls.config.json",
        ROOT / "data/maps/xian/xian-before-walls.geojson",
    ]
    manifest = {
        "schema_version": 1,
        "artifact": str(DIST_PDF.relative_to(ROOT)),
        "chapter_id": CHAPTER_ID,
        "build_date": "2026-08-14",
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
    run(
        [
            sys.executable,
            "scripts/render_destination_tex.py",
            "--book",
            str(BOOK_PATH),
            "--chapter",
            CHAPTER_ID,
            "--output-dir",
            str(BUILD_DIR),
        ]
    )

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
    if page_count < 10:
        raise RuntimeError(f"unexpectedly short review PDF: {page_count} pages")
    text = run(["pdftotext", str(pdf), "-"])
    text_characters = len("".join(text.split()))
    if text_characters < 4_000:
        raise RuntimeError(f"PDF text layer is unexpectedly short: {text_characters} characters")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, DIST_PDF)
    write_manifest(page_count, font_count, text_characters)
    print(f"validated PDF: {DIST_PDF.relative_to(ROOT)}")
    print(f"manifest: {DIST_MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
