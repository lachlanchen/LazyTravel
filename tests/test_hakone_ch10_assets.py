from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_destination_tex import block_tex  # noqa: E402

BOOK = ROOT / "data/japan/prefectures/kanagawa/hakone/book.json"
MAP_CONFIG = ROOT / "data/maps/hakone/hakone-itinerary-days.config.json"
MAP_PROVENANCE = ROOT / "assets/maps/hakone/hakone-itinerary-days.provenance.json"
FIGURE_CONFIG = ROOT / "data/images/hakone/ch10-figures.config.json"
FIGURE_PROVENANCE = (
    ROOT / "assets/images/hakone/hakone-pola-rain-arrival.provenance.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HakoneChapterTenAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK.read_text(encoding="utf-8"))
        cls.chapter = next(
            chapter
            for chapter in cls.book["chapters"]
            if chapter["id"] == "ch10-one-two-three-days"
        )
        cls.map_config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        cls.figure_config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))

    def test_chapter_is_final_and_route_complete(self) -> None:
        self.assertEqual(self.chapter["order"], 10)
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 10)
        self.assertTrue(
            {
                "itineraries",
                "transport",
                "attractions",
                "food",
                "hotels",
                "practical",
                "maps",
            }.issubset(self.chapter["coverage"])
        )
        self.assertEqual(
            [block["kind"] for block in self.chapter["blocks"]].count("figure"),
            6,
        )

    def test_portrait_map_has_three_distinct_duration_lanes(self) -> None:
        self.assertEqual(
            self.map_config["asset_id"], "asset-hakone-itinerary-days-map"
        )
        self.assertEqual(
            [lane["duration"] for lane in self.map_config["lanes"]],
            ["1", "2", "3"],
        )
        visual_qa = self.map_config["visual_qa"]
        self.assertTrue(visual_qa["approved"])
        self.assertEqual(visual_qa["mobile_390px"], "pass")
        self.assertEqual(
            visual_qa["evidence"]["pan_offsets_css_px"], [0, 185, 370]
        )

    def test_map_variants_match_approved_provenance(self) -> None:
        provenance = json.loads(MAP_PROVENANCE.read_text(encoding="utf-8"))
        self.assertTrue(provenance["visual_qa"]["approved"])
        self.assertEqual(provenance["technical_qa"]["svg_selectable_text"], True)
        self.assertEqual(provenance["technical_qa"]["png_dimensions"], [2448, 3456])
        for filename, record in provenance["files"].items():
            path = MAP_PROVENANCE.parent / filename
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_renderer_selects_portrait_map_page(self) -> None:
        block = self.chapter["blocks"][0]
        citation_numbers = {
            citation_id: index
            for index, citation_id in enumerate(block["citation_ids"], start=1)
        }
        assets = {asset["id"]: asset for asset in self.book["assets"]}
        rendered = block_tex(block, citation_numbers, assets)
        self.assertIn(r"\LTPortraitMapPage", rendered)
        self.assertNotIn(r"\LTMapPage", rendered)

    def test_pola_figure_uses_complete_guide_team_and_approved_evidence(self) -> None:
        expected_guides = {
            "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png",
            "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg",
            "/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg",
            "/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png",
        }
        self.assertEqual(
            {guide["path"] for guide in self.figure_config["guides"]},
            expected_guides,
        )
        self.assertEqual(len(self.figure_config["figures"]), 1)
        self.assertTrue(self.figure_config["visual_qa"]["approved"])
        evidence = self.figure_config["figures"][0]["qa_evidence"]
        self.assertEqual(evidence["physical_page"], 172)
        self.assertEqual(evidence["viewport_css_px"], 390)

    def test_pola_figure_outputs_match_provenance(self) -> None:
        provenance = json.loads(FIGURE_PROVENANCE.read_text(encoding="utf-8"))
        self.assertTrue(provenance["visual_qa"]["approved"])
        for record in [provenance["output"], *provenance["variants"].values()]:
            path = ROOT / record["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_website_exposes_reader_facing_visual_labels(self) -> None:
        app = (ROOT / "website/app.js").read_text(encoding="utf-8")
        self.assertIn('"asset-hakone-itinerary-days-map"', app)
        self.assertIn('"asset-hakone-pola-rain-arrival"', app)


if __name__ == "__main__":
    unittest.main()
