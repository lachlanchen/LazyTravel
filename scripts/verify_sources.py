#!/usr/bin/env python3
"""Verify every external research source and write reproducible evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data/sources/catalog.json"
DEFAULT_SCHEMA = ROOT / "schemas/source-catalog.schema.json"
DEFAULT_OUTPUT = ROOT / "build/research/source-verification.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def records(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for collection in ("tooling", "references", "sources"):
        for record in catalog[collection]:
            result.append({"collection": collection, **record})
            if record.get("source_snapshot_path"):
                result.append(
                    {
                        "collection": collection,
                        "id": f"{record['id']}-snapshot",
                        "path": record["source_snapshot_path"],
                        "sha256": record["source_snapshot_sha256"],
                    }
                )
    return result


def verify(catalog_path: Path, schema_path: Path) -> dict[str, Any]:
    catalog = read_json(catalog_path)
    schema = read_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(catalog), key=lambda error: list(error.path))
    if schema_errors:
        messages = [f"{'/'.join(map(str, error.path))}: {error.message}" for error in schema_errors]
        raise ValueError("source catalog schema errors:\n" + "\n".join(messages))

    checks: list[dict[str, Any]] = []
    for record in records(catalog):
        path = Path(record["path"])
        exists = path.is_file()
        actual_sha = sha256(path) if exists else None
        checks.append(
            {
                "id": record["id"],
                "collection": record["collection"],
                "path": str(path),
                "exists": exists,
                "expected_sha256": record["sha256"],
                "actual_sha256": actual_sha,
                "sha256_matches": actual_sha == record["sha256"],
                "bytes": path.stat().st_size if exists else None,
            }
        )

    return {
        "schema_version": 1,
        "catalog": str(catalog_path.relative_to(ROOT)),
        "catalog_sha256": sha256(catalog_path),
        "all_passed": all(check["exists"] and check["sha256_matches"] for check in checks),
        "check_count": len(checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = verify(args.catalog.resolve(), args.schema.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "all_passed": result["all_passed"],
                "checks": result["check_count"],
            }
        )
    )
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
