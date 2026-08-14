from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_epub import resolve_member, safe_member, sha256_bytes  # noqa: E402


class EpubPathSafetyTests(unittest.TestCase):
    def test_normalizes_relative_member(self) -> None:
        self.assertEqual(
            resolve_member("OPS/Text/chapter.xhtml", "../Images/map.jpg"), "OPS/Images/map.jpg"
        )

    def test_rejects_parent_escape(self) -> None:
        with self.assertRaises(ValueError):
            safe_member("../../outside.txt")

    def test_rejects_absolute_member(self) -> None:
        with self.assertRaises(ValueError):
            safe_member("/tmp/outside.txt")

    def test_content_hash_is_stable(self) -> None:
        self.assertEqual(
            sha256_bytes(b"LazyTravel"),
            "552be1fd192804eac56af064da678cb0d027e84be1b129a1214330b148d28a65",
        )


if __name__ == "__main__":
    unittest.main()
