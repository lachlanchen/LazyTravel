from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/destination-book.schema.json"


def validate(path: Path) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    document = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(document)]


def test_xian_book_matches_destination_schema() -> None:
    assert validate(ROOT / "data/china/cities/xian/book.json") == []


def test_nested_japan_destination_matches_destination_schema() -> None:
    assert validate(ROOT / "data/japan/prefectures/kanagawa/hakone/book.json") == []


def test_lanzhou_book_matches_destination_schema() -> None:
    assert validate(ROOT / "data/china/cities/lanzhou/book.json") == []
