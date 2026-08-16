from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/japan/prefectures/kanagawa/hakone/book.json"
MAP_CONFIG = ROOT / "data/maps/hakone/hakone-lake-ashi-choice.config.json"
MAP_PROVENANCE = ROOT / "assets/maps/hakone/hakone-lake-ashi-choice.provenance.json"
FIGURE_CONFIG = ROOT / "data/images/hakone/ch05-figures.config.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HakoneChapterFiveAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK.read_text(encoding="utf-8"))
        cls.map_config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        cls.figure_config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))

    def test_chapter_is_place_and_food_led(self) -> None:
        chapter = self.book["chapters"][4]
        self.assertEqual(chapter["id"], "ch05-lake-ashi")
        self.assertEqual(len(chapter["blocks"]), 10)
        self.assertTrue(
            {"attractions", "food", "transport", "maps"}.issubset(chapter["coverage"])
        )
        self.assertEqual(
            [block["category"] for block in chapter["blocks"]].count("food"), 2
        )

    def test_decision_map_connects_ports_places_and_lunch(self) -> None:
        self.assertEqual(
            self.map_config["asset_id"], "asset-hakone-lake-ashi-choice-map"
        )
        self.assertEqual(
            [node["id"] for node in self.map_config["nodes"]],
            ["togendai", "motohakone", "hakonemachi", "shrine", "lunch", "park"],
        )
        self.assertEqual(
            [choice["id"] for choice in self.map_config["choices"]],
            ["shrine_first", "park_first", "both"],
        )
        limitations = " ".join(self.map_config["generalizations"]).lower()
        self.assertIn("not to scale", limitations)
        self.assertIn("lunch time", limitations)

    def test_map_variants_match_approved_provenance(self) -> None:
        provenance = json.loads(MAP_PROVENANCE.read_text(encoding="utf-8"))
        self.assertTrue(provenance["visual_qa"]["approved"])
        self.assertEqual(provenance["technical_qa"]["svg_selectable_text"], True)
        for filename, record in provenance["files"].items():
            path = MAP_PROVENANCE.parent / filename
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_five_figures_use_the_complete_guide_team(self) -> None:
        expected_guides = {
            "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png",
            "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg",
            "/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg",
            "/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png",
        }
        self.assertEqual(
            {guide["path"] for guide in self.figure_config["guides"]}, expected_guides
        )
        self.assertEqual(len(self.figure_config["figures"]), 5)
        self.assertTrue(self.figure_config["visual_qa"]["approved"])
        self.assertEqual(
            [figure["qa_evidence"]["physical_page"] for figure in self.figure_config["figures"]],
            [64, 68, 71, 74, 77],
        )


if __name__ == "__main__":
    unittest.main()
