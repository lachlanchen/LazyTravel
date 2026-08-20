from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_series_website import build_series, relative_href  # noqa: E402
from build_website import validate_output  # noqa: E402

XIAN_BOOK = ROOT / "data/china/cities/xian/book.json"
HAKONE_BOOK = ROOT / "data/japan/prefectures/kanagawa/hakone/book.json"
XIAN_PATH = Path("china/cities/xian")
HAKONE_PATH = Path("japan/prefectures/kanagawa/hakone")


class SeriesWebsiteBuildTests(unittest.TestCase):
    def test_relative_destination_links_are_directory_safe(self) -> None:
        self.assertEqual(
            relative_href(XIAN_PATH.as_posix(), HAKONE_PATH.as_posix()),
            "../../../japan/prefectures/kanagawa/hakone/",
        )
        self.assertEqual(
            relative_href(HAKONE_PATH.as_posix(), XIAN_PATH.as_posix()),
            "../../../../china/cities/xian/",
        )
        self.assertEqual(relative_href(XIAN_PATH.as_posix(), XIAN_PATH.as_posix()), "./")

    def test_series_build_publishes_both_canonical_destinations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            manifest = build_series(output)

            self.assertEqual(manifest["default_destination"], "hakone")
            self.assertEqual(
                [record["id"] for record in manifest["destinations"]],
                ["xian", "hakone"],
            )
            self.assertIn(
                "japan/prefectures/kanagawa/hakone/",
                (output / "index.html").read_text(encoding="utf-8"),
            )

            self.assertGreater(validate_output(XIAN_BOOK, output / XIAN_PATH)["blocks"], 0)
            self.assertGreater(validate_output(HAKONE_BOOK, output / HAKONE_PATH)["blocks"], 0)

            xian_catalog = json.loads(
                (output / XIAN_PATH / "data/destinations.json").read_text(encoding="utf-8")
            )
            hakone_catalog = json.loads(
                (output / HAKONE_PATH / "data/destinations.json").read_text(encoding="utf-8")
            )
            self.assertEqual(xian_catalog["current"], "xian")
            self.assertEqual(hakone_catalog["current"], "hakone")
            self.assertEqual(
                xian_catalog["destinations"][1]["href"],
                "../../../japan/prefectures/kanagawa/hakone/",
            )
            self.assertEqual(
                hakone_catalog["destinations"][0]["href"],
                "../../../../china/cities/xian/",
            )


if __name__ == "__main__":
    unittest.main()
