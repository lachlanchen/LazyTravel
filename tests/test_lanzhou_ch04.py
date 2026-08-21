from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/lanzhou/book.json"
CONFIG_PATH = ROOT / "data/maps/lanzhou/lanzhou-bridge-hill-route.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-bridge-hill-route"


class LanzhouChapterFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][3]
        cls.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    def test_locked_destination_and_route(self) -> None:
        titles = " ".join(self.chapter["titles"].values())
        self.assertIn("黄河铁桥", titles)
        self.assertIn("白塔山", titles)
        self.assertIn("Yellow River Iron Bridge", titles)
        self.assertIn("White Pagoda Hill", titles)

    def test_map_has_five_stops_and_two_climb_depths(self) -> None:
        self.assertEqual(len(self.config["stops"]), 5)
        self.assertEqual(
            [stop["id"] for stop in self.config["stops"]],
            [
                "south-approach",
                "bridge",
                "north-entry",
                "lower-terraces",
                "pagoda",
            ],
        )
        self.assertIn("lower", self.config["branches"])
        self.assertIn("full", self.config["branches"])
        self.assertIn("riverfront", self.config["branches"])

    def test_map_rejects_false_precision(self) -> None:
        for rejected in ("walking_minutes", "elevation_gain", "step_free", "cableway"):
            for stop in self.config["stops"]:
                self.assertNotIn(rejected, stop)
            self.assertNotIn(rejected, self.config["branches"])

    def test_map_build_is_deterministic_and_print_sized(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_bridge_hill_route_map.py"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        with Image.open(MAP_STEM.with_suffix(".png")) as image:
            self.assertEqual(image.size, (1620, 2280))
        for suffix in (".svg", ".pdf", ".png", ".provenance.json"):
            self.assertTrue(MAP_STEM.with_suffix(suffix).is_file())

    def test_chapter_blocks_remain_gate_controlled(self) -> None:
        if not self.chapter["blocks"]:
            self.assertEqual(self.chapter["status"], "researching")
            return
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 9)
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch04-b{number:03d}" for number in range(1, 10)],
        )
        asset_ids = {
            asset_id
            for block in self.chapter["blocks"]
            for asset_id in block["asset_ids"]
        }
        self.assertIn("asset-lanzhou-bridge-hill-route-map", asset_ids)
        self.assertEqual(self.book["chapters"][4]["id"], "ch05-museum-route")
        self.assertEqual(self.book["chapters"][4]["status"], "researching")
        self.assertFalse(self.book["chapters"][4]["blocks"])

    def test_reviewed_place_and_context_readings(self) -> None:
        zh_readings = {
            (token["text"], token.get("reading"))
            for block in self.chapter["blocks"]
            for token in block["readings"]["zh"]["tokens"]
        }
        ja_readings = {
            (token["text"], token.get("reading"))
            for block in self.chapter["blocks"]
            for token in block["readings"]["ja"]["tokens"]
        }
        self.assertIn(("将军铁柱", "jiāngjūn tiězhù"), zh_readings)
        self.assertIn(("系在", "jìzài"), zh_readings)
        self.assertIn(("背着", "bēizhe"), zh_readings)
        self.assertIn(("中山橋", "ちゅうざんきょう"), ja_readings)
        self.assertIn(("鎮遠浮橋", "ちんえんふきょう"), ja_readings)
        self.assertIn(("白塔寺", "はくとうじ"), ja_readings)


if __name__ == "__main__":
    unittest.main()
