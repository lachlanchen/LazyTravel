#!/usr/bin/env python3
"""Run the inspected ZhJpBook Marker/Surya route into a LazyTravel research cache."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/sources/catalog.json"
SERIES = ROOT / "data/series.json"
DEFAULT_MARKER = Path("/home/lachlan/ProjectsLFS/ZhJpBook/.venv/ocr/bin/marker_single")
DEFAULT_LOCK_DIR = Path("/tmp/pocketpolyglot-marker-slots")
IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)\n]+)(\))")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def content_chars(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9\u3400-\u4dbf\u4e00-\u9fff]", text))


def source_page_from_reference(reference: str) -> int | None:
    """Return Marker's zero-based page token as a one-based PDF page."""

    match = re.search(r"(?:^|[/_])page_(\d+)(?:_|\.)", reference)
    return int(match.group(1)) + 1 if match else None


def source_record(source_id: str) -> dict[str, Any]:
    catalog = read_json(CATALOG)
    matches = [source for source in catalog["sources"] if source["id"] == source_id]
    if len(matches) != 1:
        raise ValueError(f"source id must match exactly once: {source_id}")
    source = matches[0]
    if source["kind"] != "pdf":
        raise ValueError(f"source is not a private PDF: {source_id}")
    active_destination = read_json(SERIES)["active_destination"]
    if active_destination not in source["destination_ids"] or source.get("destination_gate"):
        raise ValueError(f"source {source_id} is gated; active destination is {active_destination}")
    return source


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"cannot determine PDF page count: {path}")
    return int(match.group(1))


@contextlib.contextmanager
def marker_slot(source_id: str, lock_dir: Path = DEFAULT_LOCK_DIR) -> Iterator[None]:
    """Use the shared ZhJpBook GPU lock so independent OCR jobs cannot collide."""

    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / "slot-01.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        waiting_reported = False
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if not waiting_reported:
                    print(f"[marker-slot] waiting: {source_id}", flush=True)
                    waiting_reported = True
                time.sleep(2)
        handle.seek(0)
        handle.truncate()
        handle.write(
            json.dumps({"pid": os.getpid(), "project": "LazyTravel", "source": source_id}) + "\n"
        )
        handle.flush()
        try:
            yield
        finally:
            handle.seek(0)
            handle.truncate()
            handle.flush()
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def marker_markdown(shard_dir: Path) -> Path | None:
    candidates = sorted(
        shard_dir.glob("**/*.md"), key=lambda path: path.stat().st_size, reverse=True
    )
    return candidates[0] if candidates else None


def copy_media(
    markdown: str, markdown_dir: Path, media_dir: Path, shard_id: str
) -> tuple[str, list[dict[str, Any]]]:
    media_dir.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, Any]] = []

    def replace(match: re.Match[str]) -> str:
        prefix, raw_path, suffix = match.groups()
        raw_path = raw_path.strip().strip("<>")
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw_path):
            return match.group(0)
        source = Path(raw_path)
        if not source.is_absolute():
            source = (markdown_dir / source).resolve()
        if not source.is_file():
            figures.append({"source_reference": raw_path, "status": "missing"})
            return match.group(0)
        digest = sha256_file(source)
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", source.name).strip("-") or "figure.bin"
        destination = media_dir / f"{digest[:12]}-{shard_id}-{safe_name}"
        if not destination.exists() or sha256_file(destination) != digest:
            shutil.copy2(source, destination)
        with Image.open(destination) as opened:
            width, height = opened.size
        substantive_candidate = width >= 300 and height >= 250 and width * height >= 100_000
        relative = destination.relative_to(media_dir.parent).as_posix()
        figures.append(
            {
                "source_reference": raw_path,
                "path": relative,
                "sha256": digest,
                "bytes": destination.stat().st_size,
                "width": width,
                "height": height,
                "source_page": source_page_from_reference(raw_path),
                "status": "extracted",
                "publishable": False,
                "substantive_candidate": substantive_candidate,
                "review_note": (
                    "candidate for source-figure review"
                    if substantive_candidate
                    else "rejected automatically as a small scan fragment"
                ),
            }
        )
        return f"{prefix}{relative}{suffix}"

    return IMAGE_RE.sub(replace, markdown), figures


def run_marker_shard(
    *,
    source: Path,
    source_id: str,
    source_hash: str,
    marker: Path,
    shard_dir: Path,
    page_start: int,
    page_end: int,
    timeout_seconds: int,
) -> Path:
    status_path = shard_dir / "status.json"
    existing = marker_markdown(shard_dir)
    marker_hash = sha256_file(marker)
    if status_path.exists() and existing:
        status = read_json(status_path)
        if (
            status.get("status") == "complete"
            and status.get("source_sha256") == source_hash
            and status.get("marker_sha256") == marker_hash
            and status.get("page_start") == page_start
            and status.get("page_end") == page_end
        ):
            print(f"[reuse] pages {page_start}-{page_end}", flush=True)
            return existing

    if shard_dir.exists():
        shutil.rmtree(shard_dir)
    shard_dir.mkdir(parents=True)
    log_path = shard_dir / "marker.log"
    command = [
        str(marker),
        str(source),
        "--page_range",
        f"{page_start - 1}-{page_end - 1}",
        "--output_dir",
        str(shard_dir),
        "--output_format",
        "markdown",
        "--disable_multiprocessing",
        "--disable_tqdm",
        "--highres_image_dpi",
        "240",
    ]
    printable_command = [str(marker), str(source), *command[2:]]
    print(f"[marker] pages {page_start}-{page_end}", flush=True)
    with marker_slot(source_id):
        with log_path.open("w", encoding="utf-8") as log_handle:
            result = subprocess.run(
                command,
                text=True,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds if timeout_seconds > 0 else None,
                check=False,
            )
    markdown = marker_markdown(shard_dir)
    status = {
        "status": "complete" if result.returncode == 0 and markdown else "blocked",
        "source_id": source_id,
        "source_sha256": source_hash,
        "marker_path": str(marker),
        "marker_sha256": marker_hash,
        "page_start": page_start,
        "page_end": page_end,
        "exit_code": result.returncode,
        "command": printable_command,
        "log": log_path.relative_to(shard_dir).as_posix(),
    }
    if markdown:
        status["markdown"] = markdown.relative_to(shard_dir).as_posix()
    write_json(status_path, status)
    if result.returncode != 0 or markdown is None:
        raise RuntimeError(f"Marker failed for pages {page_start}-{page_end}; see {log_path}")
    return markdown


def merge_complete_shards(
    output_dir: Path, source_id: str, source_hash: str, total_pages: int
) -> dict[str, Any]:
    shard_root = output_dir / "marker-shards"
    media_dir = output_dir / "media"
    parts: list[str] = []
    shard_records: list[dict[str, Any]] = []
    all_figures: list[dict[str, Any]] = []
    covered_pages: set[int] = set()

    for status_path in sorted(shard_root.glob("pages-*/status.json")):
        status = read_json(status_path)
        if status.get("status") != "complete" or status.get("source_sha256") != source_hash:
            continue
        shard_dir = status_path.parent
        markdown_path = shard_dir / status["markdown"]
        if not markdown_path.is_file():
            continue
        page_start = int(status["page_start"])
        page_end = int(status["page_end"])
        shard_id = f"pages-{page_start:04d}-{page_end:04d}"
        markdown = markdown_path.read_text(encoding="utf-8", errors="replace")
        markdown, figures = copy_media(markdown, markdown_path.parent, media_dir, shard_id)
        for figure in figures:
            figure["source_page_range"] = [page_start, page_end]
        all_figures.extend(figures)
        parts.append(f"<!-- source-pages:{page_start}-{page_end} -->\n\n{markdown.strip()}")
        covered_pages.update(range(page_start, page_end + 1))
        shard_records.append(
            {
                "id": shard_id,
                "page_start": page_start,
                "page_end": page_end,
                "markdown": markdown_path.relative_to(output_dir).as_posix(),
                "content_chars": content_chars(markdown),
                "figure_references": len(figures),
            }
        )

    merged = "\n\n".join(parts).strip() + "\n"
    merged_path = output_dir / "source.raw.md"
    merged_path.write_text(merged, encoding="utf-8")
    coverage = sorted(covered_pages)
    complete = coverage == list(range(1, total_pages + 1))
    manifest = {
        "schema_version": 1,
        "source_id": source_id,
        "source_sha256": source_hash,
        "engine": "marker-surya-local-sharded",
        "design_reference": (
            "/home/lachlan/ProjectsLFS/ZhJpBook/scripts/books/build_pocket_tex_queue.py"
        ),
        "status": "complete" if complete else "partial",
        "total_pages": total_pages,
        "covered_pages": coverage,
        "covered_page_count": len(coverage),
        "content_chars": content_chars(merged),
        "raw_extraction_publishable": False,
        "shards": shard_records,
        "figures": all_figures,
        "figure_count": len(all_figures),
        "substantive_figure_candidate_count": sum(
            figure.get("substantive_candidate") is True for figure in all_figures
        ),
        "rejected_scan_fragment_count": sum(
            figure.get("substantive_candidate") is False for figure in all_figures
        ),
        "missing_figure_count": sum(figure["status"] == "missing" for figure in all_figures),
        "merged_markdown": merged_path.relative_to(output_dir).as_posix(),
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def compile_review_tex(output_dir: Path, title: str) -> dict[str, Any]:
    markdown = output_dir / "source.raw.md"
    exact_dir = output_dir / "exact"
    exact_dir.mkdir(parents=True, exist_ok=True)
    tex_path = exact_dir / "source.tex"
    header_path = exact_dir / "review-header.tex"
    header_path.write_text(
        "\\usepackage{ucharclasses}\n"
        "\\newfontfamily\\devanagarifont{Noto Serif Devanagari}\n"
        "\\setTransitionTo{Devanagari}{\\devanagarifont}\n"
        "\\setTransitionFrom{Devanagari}{\\normalfont}\n",
        encoding="utf-8",
    )
    pandoc_command = [
        "pandoc",
        str(markdown),
        "--from",
        "markdown+raw_tex+tex_math_dollars",
        "--to",
        "latex",
        "--standalone",
        "--toc",
        "--top-level-division=chapter",
        "--metadata",
        f"title={title} OCR review edition",
        "--variable",
        "documentclass=ctexbook",
        "--variable",
        "mainfont=Noto Serif CJK SC",
        "--variable",
        "CJKmainfont=Noto Serif CJK SC",
        "--variable",
        "papersize=a4",
        "--variable",
        "geometry:margin=22mm",
        "--include-in-header",
        str(header_path),
        "--output",
        str(tex_path),
    ]
    pandoc = subprocess.run(
        pandoc_command,
        cwd=output_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (exact_dir / "pandoc.log").write_text(pandoc.stdout, encoding="utf-8")
    if pandoc.returncode:
        raise RuntimeError(f"Pandoc failed; see {exact_dir / 'pandoc.log'}")
    tex = tex_path.read_text(encoding="utf-8")
    tex = tex.replace(
        r"\def\maxheight{\ifdim\Gin@nat@height>\textheight\textheight\else\Gin@nat@height\fi}",
        (
            r"\def\maxheight{\ifdim\Gin@nat@height>.72\textheight "
            r".72\textheight\else\Gin@nat@height\fi}"
        ),
    )
    tex_path.write_text(tex, encoding="utf-8")

    latex_logs: list[str] = []
    return_code = 0
    for _ in range(2):
        latex = subprocess.run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(exact_dir),
                str(tex_path),
            ],
            cwd=output_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        latex_logs.append(latex.stdout)
        return_code = latex.returncode
        if return_code:
            break
    (exact_dir / "compile.stdout.log").write_text("\n\n".join(latex_logs), encoding="utf-8")
    pdf_path = exact_dir / "source.pdf"
    if return_code or not pdf_path.is_file():
        raise RuntimeError(f"XeLaTeX failed; see {exact_dir / 'compile.stdout.log'}")
    qpdf = subprocess.run(
        ["qpdf", "--check", str(pdf_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    final_log_path = exact_dir / "source.log"
    final_log = final_log_path.read_text(encoding="utf-8", errors="replace")
    missing_character_count = len(re.findall(r"^Missing character:", final_log, re.MULTILINE))
    overfull_values = [
        float(value)
        for value in re.findall(r"Overfull \\[hv]box \(([-0-9.]+)pt too (?:wide|high)\)", final_log)
    ]
    fatal_error_count = len(
        re.findall(
            r"^! |Fatal error|Emergency stop|Undefined control sequence",
            final_log,
            re.MULTILINE,
        )
    )
    worst_overfull_pt = max(overfull_values, default=0.0)
    compiled = return_code == 0 and qpdf.returncode == 0
    accepted = (
        compiled
        and missing_character_count == 0
        and fatal_error_count == 0
        and worst_overfull_pt <= 18.0
    )
    report = {
        "tex": tex_path.relative_to(output_dir).as_posix(),
        "pdf": pdf_path.relative_to(output_dir).as_posix(),
        "pdf_sha256": sha256_file(pdf_path),
        "qpdf_exit_code": qpdf.returncode,
        "qpdf_output": qpdf.stdout.strip(),
        "missing_character_count": missing_character_count,
        "fatal_error_count": fatal_error_count,
        "overfull_box_count": len(overfull_values),
        "worst_overfull_pt": worst_overfull_pt,
        "compiled": compiled,
        "accepted": accepted,
    }
    write_json(exact_dir / "compile-report.json", report)
    return report


def extract(args: argparse.Namespace) -> dict[str, Any]:
    source = source_record(args.source_id)
    source_path = Path(source["path"])
    source_hash = sha256_file(source_path)
    if source_hash != source["sha256"]:
        raise RuntimeError(f"source checksum mismatch: {source_path}")
    if not args.marker.is_file() or not os.access(args.marker, os.X_OK):
        raise FileNotFoundError(f"Marker executable is unavailable: {args.marker}")

    total_pages = pdf_pages(source_path)
    page_start = args.page_start
    page_end = args.page_end or total_pages
    if not 1 <= page_start <= page_end <= total_pages:
        raise ValueError(
            f"invalid page range {page_start}-{page_end}; source has {total_pages} pages"
        )

    output_dir = args.output_root.resolve() / source["id"]
    shard_root = output_dir / "marker-shards"
    for start in range(page_start, page_end + 1, args.shard_pages):
        end = min(page_end, start + args.shard_pages - 1)
        shard_dir = shard_root / f"pages-{start:04d}-{end:04d}"
        run_marker_shard(
            source=source_path,
            source_id=source["id"],
            source_hash=source_hash,
            marker=args.marker,
            shard_dir=shard_dir,
            page_start=start,
            page_end=end,
            timeout_seconds=args.timeout_seconds,
        )

    manifest = merge_complete_shards(output_dir, source["id"], source_hash, total_pages)
    if args.compile_tex:
        manifest["review_build"] = compile_review_tex(output_dir, source["title"])
        write_json(output_dir / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--page-start", type=int, default=1)
    parser.add_argument("--page-end", type=int, default=0)
    parser.add_argument("--shard-pages", type=int, default=12)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--marker", type=Path, default=DEFAULT_MARKER)
    parser.add_argument(
        "--output-root", type=Path, default=ROOT / "build/research/xian/source-extraction"
    )
    parser.add_argument("--compile-tex", action="store_true")
    args = parser.parse_args()
    if args.shard_pages < 1:
        parser.error("--shard-pages must be positive")

    result = extract(args)
    print(
        json.dumps(
            {
                "source_id": result["source_id"],
                "status": result["status"],
                "covered_pages": result["covered_page_count"],
                "total_pages": result["total_pages"],
                "content_chars": result["content_chars"],
                "figures": result["figure_count"],
                "missing_figures": result["missing_figure_count"],
                "compiled": bool(result.get("review_build", {}).get("compiled")),
                "accepted": bool(result.get("review_build", {}).get("accepted")),
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["missing_figure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
