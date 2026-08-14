#!/usr/bin/env python3
"""Validate that the generated website remains in parity with canonical JSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_website import DEFAULT_BOOK, DEFAULT_OUTPUT, validate_output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", type=Path, default=DEFAULT_BOOK)
    parser.add_argument("--site", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    counts = validate_output(args.book.resolve(), args.site.resolve())
    print(
        "site parity: pass "
        f"({counts['blocks']} blocks, {counts['zh_tokens']} zh tokens, "
        f"{counts['ja_tokens']} ja tokens)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
