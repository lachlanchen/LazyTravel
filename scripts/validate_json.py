#!/usr/bin/env python3
"""Validate a LazyTravel JSON document against a repository schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()

    document = json.loads(args.document.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    for error in errors:
        location = "/".join(map(str, error.absolute_path)) or "<root>"
        print(f"{location}: {error.message}")
    if errors:
        return 1
    display_path = (
        args.document.relative_to(ROOT) if args.document.is_relative_to(ROOT) else args.document
    )
    print(f"valid: {display_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
