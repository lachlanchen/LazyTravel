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
MAP_CONFIG = ROOT / "data/maps/hakone/hakone-beyond-branch.config.json"
MAP_PROVENANCE = ROOT / "assets/maps/hakone/hakone-beyond-branch.provenance.json"
FIGURE_CONFIG = ROOT / "data/images/hakone/ch11-figures.config.json"
FIGURE_STEMS = (
    "hakone-odawara-castle-stop",
    "hakone-mishima-taisha-stop",
    "hakone-gotemba-niihashi-stop",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HakoneChapterElevenAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK.read_text(encoding="utf-8"))
        cls.chapter = next(
            chapter for chapter in cls.book["chapters"] if chapter["id"] == "ch11-beyond-hakone"
        )
        cls.map_config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        cls.figure_config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))

    def test_chapter_is_final_and_complete(self) -> None:
        self.assertEqual(self.chapter["order"], 11)
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 10)
        self.assertTrue(
            {
                "attractions",
                "transport",
                "itineraries",
                "history",
                "cultural-context",
                "practical",
                "maps",
            }.issubset(self.chapter["coverage"])
        )
        visual_blocks = [
            block for block in self.chapter["blocks"] if block["kind"] in {"map", "figure"}
        ]
        self.assertEqual(
            [block["kind"] for block in visual_blocks],
            [
                "map",
                "figure",
                "figure",
                "figure",
            ],
        )

    def test_map_has_three_alternative_onward_branches(self) -> None:
        self.assertEqual(self.map_config["asset_id"], "asset-hakone-beyond-branch-map")
        self.assertEqual(
            [branch["destination"]["en"] for branch in self.map_config["branches"]],
            ["ODAWARA", "MISHIMA", "GOTEMBA"],
        )
        visual_qa = self.map_config["visual_qa"]
        self.assertTrue(visual_qa["approved"])
        self.assertEqual(visual_qa["print_300dpi"], "pass")
        self.assertEqual(visual_qa["mobile_390px"], "pass")
        self.assertEqual(visual_qa["evidence"]["physical_page"], 182)
        self.assertEqual(visual_qa["evidence"]["pan_offsets_css_px"], [0, 185, 370])

    def test_map_variants_match_approved_provenance(self) -> None:
        provenance = json.loads(MAP_PROVENANCE.read_text(encoding="utf-8"))
        self.assertTrue(provenance["visual_qa"]["approved"])
        self.assertTrue(provenance["technical_qa"]["svg_selectable_text"])
        self.assertEqual(provenance["technical_qa"]["png_dimensions"], [2448, 3456])
        for filename, record in provenance["files"].items():
            path = MAP_PROVENANCE.parent / filename
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_renderer_selects_portrait_map_page(self) -> None:
        block = self.chapter["blocks"][0]
        citation_numbers = {
            citation_id: index for index, citation_id in enumerate(block["citation_ids"], start=1)
        }
        assets = {asset["id"]: asset for asset in self.book["assets"]}
        rendered = block_tex(block, citation_numbers, assets)
        self.assertIn(r"\LTPortraitMapPage", rendered)
        self.assertNotIn(r"\LTMapPage", rendered)

    def test_figures_use_four_guides_and_approved_evidence(self) -> None:
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
        self.assertEqual(len(self.figure_config["figures"]), 3)
        self.assertTrue(self.figure_config["visual_qa"]["approved"])
        self.assertEqual(
            [figure["qa_evidence"]["physical_page"] for figure in self.figure_config["figures"]],
            [185, 190, 197],
        )
        for figure in self.figure_config["figures"]:
            evidence = figure["qa_evidence"]
            self.assertEqual(evidence["viewport_css_px"], 390)
            self.assertEqual(evidence["display_width_css_px"], 390)

    def test_figure_outputs_match_approved_provenance(self) -> None:
        for stem in FIGURE_STEMS:
            provenance_path = ROOT / "assets/images/hakone" / f"{stem}.provenance.json"
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            self.assertTrue(provenance["visual_qa"]["approved"])
            for record in [provenance["output"], *provenance["variants"].values()]:
                path = ROOT / record["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(sha256(path), record["sha256"])

    def test_release_build_and_website_include_chapter_assets(self) -> None:
        build_script = (ROOT / "scripts/build_hakone_review.py").read_text(encoding="utf-8")
        self.assertIn("build_hakone_beyond_branch_map.py", build_script)
        self.assertIn("prepare_hakone_ch11_figures.py", build_script)

        app = (ROOT / "website/app.js").read_text(encoding="utf-8")
        for asset_id in (
            "asset-hakone-beyond-branch-map",
            "asset-hakone-odawara-castle-stop",
            "asset-hakone-mishima-taisha-stop",
            "asset-hakone-gotemba-niihashi-stop",
        ):
            self.assertIn(f'"{asset_id}"', app)


if __name__ == "__main__":
    unittest.main()
