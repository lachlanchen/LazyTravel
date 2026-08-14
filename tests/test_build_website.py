from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_website import (  # noqa: E402
    DEFAULT_BOOK,
    build,
    public_projection,
    validate_output,
)


class WebsiteBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(DEFAULT_BOOK.read_text(encoding="utf-8"))

    def test_public_projection_strips_private_paths_only(self) -> None:
        projected = public_projection(self.document)
        self.assertEqual(projected["chapters"], self.document["chapters"])
        self.assertTrue(any("path" in citation for citation in self.document["citations"]))
        self.assertTrue(all("path" not in citation for citation in projected["citations"]))

    def test_build_preserves_aligned_content_and_readings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            counts = build(DEFAULT_BOOK, output)
            expected = {
                "blocks": sum(
                    len(chapter["blocks"]) for chapter in self.document["chapters"]
                ),
                "zh_tokens": sum(
                    len(block["readings"]["zh"]["tokens"])
                    for chapter in self.document["chapters"]
                    for block in chapter["blocks"]
                ),
                "ja_tokens": sum(
                    len(block["readings"]["ja"]["tokens"])
                    for chapter in self.document["chapters"]
                    for block in chapter["blocks"]
                ),
            }
            self.assertEqual(counts, expected)
            self.assertGreaterEqual(counts["blocks"], 18)
            self.assertEqual(validate_output(DEFAULT_BOOK, output), counts)
            payload = json.loads((output / "data/xian.json").read_text(encoding="utf-8"))
            payload.pop("_build")
            self.assertEqual(payload, public_projection(self.document))

    def test_static_renderer_has_no_external_runtime_dependency(self) -> None:
        index = (ROOT / "website/index.html").read_text(encoding="utf-8")
        self.assertNotIn("https://cdn", index)
        self.assertNotIn("<script src=\"http", index)


if __name__ == "__main__":
    unittest.main()
