#!/usr/bin/env python3
"""Validate pinyin/furigana coverage and source-text parity."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "data/china/cities/xian/book.json"
HAN_RE = re.compile(r"[\u3007\u3400-\u4dbf\u4e00-\u9fff]")


def valid_pinyin(value: str) -> bool:
    return all(
        unicodedata.category(character).startswith("L") or character in "' -" for character in value
    )


def valid_furigana(value: str) -> bool:
    return all("\u3040" <= character <= "\u30ff" or character in "ー・ " for character in value)


def reading_errors(document: dict[str, Any], *, require_reviewed: bool = True) -> list[str]:
    errors: list[str] = []
    for chapter in document["chapters"]:
        for block in chapter["blocks"]:
            readings = block.get("readings")
            if not readings:
                errors.append(f"{block['id']}: missing readings")
                continue
            for language, validator in (("zh", valid_pinyin), ("ja", valid_furigana)):
                layer = readings.get(language)
                if not layer:
                    errors.append(f"{block['id']}/{language}: missing reading layer")
                    continue
                if require_reviewed and layer.get("status") != "reviewed":
                    errors.append(f"{block['id']}/{language}: reading layer is not reviewed")
                tokens = layer.get("tokens", [])
                rebuilt = "".join(token.get("text", "") for token in tokens)
                if rebuilt != block["text"][language]:
                    errors.append(f"{block['id']}/{language}: tokens do not reconstruct text")
                for index, token in enumerate(tokens):
                    text = token.get("text", "")
                    reading = token.get("reading")
                    if HAN_RE.search(text) and not reading:
                        errors.append(
                            f"{block['id']}/{language}/{index}: missing reading for {text!r}"
                        )
                    if reading and not validator(reading):
                        errors.append(
                            f"{block['id']}/{language}/{index}: invalid reading {reading!r}"
                        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument(
        "--allow-candidates",
        action="store_true",
        help="validate candidate layers without requiring reviewed status",
    )
    args = parser.parse_args()

    document = json.loads(args.book.read_text(encoding="utf-8"))
    errors = reading_errors(document, require_reviewed=not args.allow_candidates)
    for error in errors:
        print(error)
    if errors:
        return 1
    counts = {
        language: sum(
            len(block["readings"][language]["tokens"])
            for chapter in document["chapters"]
            for block in chapter["blocks"]
        )
        for language in ("zh", "ja")
    }
    print(f"valid readings: zh={counts['zh']} tokens, ja={counts['ja']} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
