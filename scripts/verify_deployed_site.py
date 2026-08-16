#!/usr/bin/env python3
"""Verify a deployed LazyTravel site against canonical JSON and its manifest."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

from build_website import DEFAULT_BOOK, PAYLOAD_PATH, public_projection, reading_counts, sha256

REQUIRED_SHELL_MARKERS = (
    'id="chapter-select"',
    'id="section-select"',
    'id="ruby-toggle"',
    'id="chapter-outline"',
    'id="section-outline"',
)
REQUIRED_FILES = {
    "index.html",
    "app.js",
    "styles.css",
    str(PAYLOAD_PATH),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def site_url(base_url: str, path: str, revision: str) -> str:
    base = base_url.rstrip("/") + "/"
    quoted_path = urllib.parse.quote(path, safe="/")
    return urllib.parse.urljoin(base, quoted_path) + f"?revision={revision[:16]}"


def safe_manifest_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not value or ".." in path.parts:
        raise RuntimeError(f"unsafe deployed path in manifest: {value!r}")
    return str(path)


def fetch_bytes(url: str, *, timeout: float = 30.0) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "User-Agent": "LazyTravel-deployment-verifier/1",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"unexpected HTTP {response.status} for {url}")
        return response.read()


def fetch_json(url: str, *, timeout: float = 30.0) -> dict[str, Any]:
    try:
        return json.loads(fetch_bytes(url, timeout=timeout).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid JSON from {url}: {error}") from error


def validate_site_metadata(
    source: dict[str, Any],
    source_sha256: str,
    manifest: dict[str, Any],
    payload: dict[str, Any],
    index_html: str,
) -> dict[str, dict[str, Any]]:
    source_record = manifest.get("source_json", {})
    if source_record.get("sha256") != source_sha256:
        raise RuntimeError("deployed manifest does not match the canonical JSON hash")

    expected_counts = reading_counts(source)
    expected_parity = {"status": "pass", **expected_counts}
    if manifest.get("parity") != expected_parity:
        raise RuntimeError(
            f"deployed parity differs: {manifest.get('parity')!r} != {expected_parity!r}"
        )

    projected = copy.deepcopy(payload)
    build_meta = projected.pop("_build", None)
    if not build_meta or build_meta.get("source_sha256") != source_sha256:
        raise RuntimeError("deployed payload build metadata is stale or missing")
    if projected != public_projection(source):
        raise RuntimeError("deployed payload differs from the canonical public projection")

    if any(marker not in index_html for marker in REQUIRED_SHELL_MARKERS):
        raise RuntimeError("deployed HTML is missing a required navigation control")
    if "/home/" in index_html or "ProjectsLFS" in index_html:
        raise RuntimeError("deployed HTML leaks a workstation path")

    files = manifest.get("files")
    if not isinstance(files, dict):
        raise RuntimeError("deployed manifest has no file table")
    normalized: dict[str, dict[str, Any]] = {}
    for raw_path, metadata in files.items():
        path = safe_manifest_path(raw_path)
        if not isinstance(metadata, dict):
            raise RuntimeError(f"invalid metadata for deployed path: {path}")
        digest = metadata.get("sha256")
        size = metadata.get("bytes")
        if not isinstance(digest, str) or len(digest) != 64:
            raise RuntimeError(f"invalid SHA-256 for deployed path: {path}")
        if not isinstance(size, int) or size < 0:
            raise RuntimeError(f"invalid byte count for deployed path: {path}")
        normalized[path] = metadata
    missing = sorted(REQUIRED_FILES - normalized.keys())
    if missing:
        raise RuntimeError(f"deployed manifest is missing files: {', '.join(missing)}")
    return normalized


def verify_file(
    base_url: str,
    revision: str,
    path: str,
    metadata: dict[str, Any],
    *,
    attempts: int = 3,
    delay: float = 2.0,
) -> tuple[str, int]:
    url = site_url(base_url, path, revision)
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            data = fetch_bytes(url)
            if len(data) != metadata["bytes"]:
                raise RuntimeError(
                    f"byte count mismatch for {path}: {len(data)} != {metadata['bytes']}"
                )
            digest = sha256_bytes(data)
            if digest != metadata["sha256"]:
                raise RuntimeError(
                    f"SHA-256 mismatch for {path}: {digest} != {metadata['sha256']}"
                )
            return path, len(data)
        except (OSError, RuntimeError, urllib.error.URLError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(delay)
    raise RuntimeError(f"failed to verify {path}: {last_error}")


def wait_for_current_site(
    base_url: str,
    source: dict[str, Any],
    source_sha256: str,
    *,
    attempts: int,
    delay: float,
) -> tuple[dict[str, Any], dict[str, Any], str, dict[str, dict[str, Any]]]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            manifest = fetch_json(site_url(base_url, "manifest.json", source_sha256))
            payload = fetch_json(site_url(base_url, str(PAYLOAD_PATH), source_sha256))
            index_html = fetch_bytes(
                site_url(base_url, "index.html", source_sha256)
            ).decode("utf-8")
            files = validate_site_metadata(
                source, source_sha256, manifest, payload, index_html
            )
            return manifest, payload, index_html, files
        except (OSError, RuntimeError, UnicodeDecodeError, urllib.error.URLError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(delay)
    raise RuntimeError(f"deployed site did not reach the current revision: {last_error}")


def verify_deployment(
    base_url: str,
    book_path: Path,
    *,
    attempts: int = 12,
    delay: float = 10.0,
    workers: int = 6,
) -> dict[str, Any]:
    source = json.loads(book_path.read_text(encoding="utf-8"))
    source_digest = sha256(book_path)
    _, _, _, files = wait_for_current_site(
        base_url,
        source,
        source_digest,
        attempts=attempts,
        delay=delay,
    )

    total_bytes = 0
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        future_paths = {
            executor.submit(
                verify_file,
                base_url,
                source_digest,
                path,
                metadata,
            ): path
            for path, metadata in sorted(files.items())
        }
        for future in concurrent.futures.as_completed(future_paths):
            path = future_paths[future]
            try:
                _, byte_count = future.result()
                total_bytes += byte_count
            except Exception as error:  # Collect every failed public file in one report.
                failures.append(f"{path}: {error}")
    if failures:
        raise RuntimeError("deployed file verification failed:\n" + "\n".join(failures))

    return {
        "url": base_url.rstrip("/") + "/",
        "source_sha256": source_digest,
        "files": len(files),
        "bytes": total_bytes,
        "parity": reading_counts(source),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Published site root URL")
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    report = verify_deployment(
        args.url,
        args.book.resolve(),
        attempts=max(1, args.attempts),
        delay=max(0.0, args.delay),
        workers=max(1, args.workers),
    )
    print(
        "verified deployed website: "
        f"{report['url']} ({report['files']} files, {report['bytes']} bytes, "
        f"source {report['source_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
