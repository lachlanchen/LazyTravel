#!/usr/bin/env python3
"""Build the public LazyTravel website with one stable path per destination."""

from __future__ import annotations

import argparse
import json
import posixpath
import shutil
from pathlib import Path
from typing import Any

from build_website import build, destination_names, sha256, validate_output

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "site"
DEFAULT_DESTINATION = "hakone"
BOOK_PATHS = (
    ROOT / "data/china/cities/xian/book.json",
    ROOT / "data/japan/prefectures/kanagawa/hakone/book.json",
    ROOT / "data/china/cities/lanzhou/book.json",
)


def relative_href(current_path: str, target_path: str) -> str:
    relative = posixpath.relpath(target_path, start=current_path)
    return "./" if relative == "." else relative.rstrip("/") + "/"


def destination_records() -> list[dict[str, Any]]:
    records = []
    for book_path in BOOK_PATHS:
        document = json.loads(book_path.read_text(encoding="utf-8"))
        book = document["book"]
        records.append(
            {
                "id": book["id"],
                "series_path": book["series_path"],
                "names": destination_names(document),
                "book_path": book_path,
                "document": document,
            }
        )
    return records


def catalog_for(records: list[dict[str, Any]], current: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "current": current["id"],
        "destinations": [
            {
                "id": record["id"],
                "series_path": record["series_path"],
                "names": record["names"],
                "href": relative_href(current["series_path"], record["series_path"]),
            }
            for record in records
        ],
    }


def root_catalog(records: list[dict[str, Any]], default_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "current": default_id,
        "destinations": [
            {
                "id": record["id"],
                "series_path": record["series_path"],
                "names": record["names"],
                "href": record["series_path"].rstrip("/") + "/",
            }
            for record in records
        ],
    }


def root_redirect(destination_path: str) -> str:
    target = destination_path.rstrip("/") + "/"
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="0; url={target}">
    <meta name="robots" content="noindex">
    <title>LazyTravel</title>
    <script>window.location.replace(new URL({json.dumps(target)}, window.location.href));</script>
  </head>
  <body>
    <a href="{target}">LazyTravel</a>
  </body>
</html>
"""


def build_series(output: Path, default_id: str = DEFAULT_DESTINATION) -> dict[str, Any]:
    records = destination_records()
    by_id = {record["id"]: record for record in records}
    if default_id not in by_id:
        raise RuntimeError(f"unknown default destination: {default_id}")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    destination_reports = []
    for record in records:
        destination_output = output / record["series_path"]
        counts = build(
            record["book_path"],
            destination_output,
            catalog=catalog_for(records, record),
        )
        validate_output(record["book_path"], destination_output)
        destination_reports.append(
            {
                "id": record["id"],
                "series_path": record["series_path"],
                "book": str(record["book_path"].relative_to(ROOT)),
                "book_sha256": sha256(record["book_path"]),
                "manifest_sha256": sha256(destination_output / "manifest.json"),
                "parity": counts,
            }
        )

    default_record = by_id[default_id]
    (output / "index.html").write_text(
        root_redirect(default_record["series_path"]), encoding="utf-8"
    )
    root_data = output / "data"
    root_data.mkdir()
    (root_data / "destinations.json").write_text(
        json.dumps(root_catalog(records, default_id), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "schema_version": 1,
        "command": "python3 scripts/build_series_website.py",
        "default_destination": default_id,
        "default_path": default_record["series_path"],
        "destinations": destination_reports,
        "root_files": {
            "index.html": {"sha256": sha256(output / "index.html")},
            "data/destinations.json": {"sha256": sha256(root_data / "destinations.json")},
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--default", default=DEFAULT_DESTINATION)
    args = parser.parse_args()
    manifest = build_series(args.output.resolve(), args.default)
    counts = ", ".join(
        f"{record['id']}={record['parity']['blocks']} blocks" for record in manifest["destinations"]
    )
    print(
        f"validated series website: {args.output} "
        f"(default={manifest['default_destination']}; {counts})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
