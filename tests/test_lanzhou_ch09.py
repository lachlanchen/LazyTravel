from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/lanzhou/book.json"
MAP_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-itinerary-days.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-itinerary-days"
GUIDE_PATHS = {
    "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png",
    "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg",
    "/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg",
    "/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class LanzhouChapterNineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][8]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertEqual(self.chapter["id"], "ch09-itinerary-days")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch09-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(self.book["chapters"][9]["id"], "ch10-next-gansu-leg")
        self.assertEqual(self.book["chapters"][9]["status"], "final")
        self.assertEqual(len(self.book["chapters"][9]["blocks"]), 10)
        self.assertEqual(self.book["chapters"][10]["id"], "ch11-nearby-day")
        self.assertEqual(self.book["chapters"][10]["status"], "final")
        self.assertEqual(len(self.book["chapters"][10]["blocks"]), 10)

    def test_alignment_and_readings_are_closed(self) -> None:
        self.assertEqual(
            [block["kind"] for block in self.chapter["blocks"]],
            [
                "figure",
                "map",
                "figure",
                "figure",
                "figure",
                "figure",
                "figure",
                "figure",
                "practical",
                "callout",
            ],
        )
        for block in self.chapter["blocks"]:
            self.assertEqual(set(block["text"]), {"zh", "ja", "en"})
            for language in ("zh", "ja", "en"):
                self.assertTrue(block["text"][language])
                self.assertEqual(block["review"][language]["state"], "final")
            for language in ("zh", "ja"):
                layer = block["readings"][language]
                self.assertEqual(layer["status"], "reviewed")
                reconstructed = "".join(token["text"] for token in layer["tokens"])
                self.assertEqual(reconstructed, block["text"][language])

    def test_context_sensitive_readings_are_reviewed(self) -> None:
        zh = {
            (token["text"], token.get("reading"))
            for block in self.chapter["blocks"]
            for token in block["readings"]["zh"]["tokens"]
        }
        ja = {
            (token["text"], token.get("reading"))
            for block in self.chapter["blocks"]
            for token in block["readings"]["ja"]["tokens"]
        }
        self.assertTrue(
            {
                ("四行", "sì háng"),
                ("不为", "bù wèi"),
                ("出土地", "chūtǔdì"),
                ("重走", "chóngzǒu"),
                ("白塔山", "báitǎshān"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("開館日", "かいかんび"),
                ("開館", "かいかん"),
                ("館内", "かんない"),
                ("三泊", "さんぱく"),
                ("二本目", "にほんめ"),
                ("保安検査", "ほあんけんさ"),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-river-valley-orientation",
            "asset-lanzhou-itinerary-days-map",
            "asset-lanzhou-zhongshan-bridge",
            "asset-lanzhou-gansu-provincial-museum-exterior",
            "asset-lanzhou-beef-noodle-morning",
            "asset-lanzhou-white-pagoda-hill",
            "asset-lanzhou-lanshan-santai-view",
            "asset-lanzhou-city-god-temple",
        }
        expected_citations = {
            "src-cma-lanzhou-climate",
            "src-lanzhou-airport-connections-2026",
            "src-lanzhou-arrival-map-data",
            "src-lanzhou-baita-current-2025",
            "src-lanzhou-beef-noodle-ich",
            "src-lanzhou-bridge-hill-map-data",
            "src-lanzhou-city-god-current-2026",
            "src-lanzhou-city-god-temple",
            "src-lanzhou-food-context-2026",
            "src-lanzhou-geography-2026",
            "src-lanzhou-height-choice-map-data",
            "src-lanzhou-heights-access-2026",
            "src-lanzhou-itinerary-days-map-data",
            "src-lanzhou-lanshan-record-2025",
            "src-lanzhou-metro-service",
            "src-lanzhou-museum-galleries-2026",
            "src-lanzhou-museum-route-map-data",
            "src-lanzhou-museum-visit-2026",
            "src-lanzhou-old-city-streets",
            "src-lanzhou-river-core-2024",
            "src-lanzhou-sanpaotai-consumer-2022",
            "src-lanzhou-stay-segment-map-data",
            "src-lanzhou-wuquan-flood-2026",
            "src-lanzhou-wuquan-heritage-2023",
        }
        used_assets = {
            asset_id
            for block in self.chapter["blocks"]
            for asset_id in block["asset_ids"]
        }
        used_citations = {
            citation_id
            for block in self.chapter["blocks"]
            for citation_id in block["citation_ids"]
        }
        self.assertEqual(used_assets, expected_assets)
        self.assertEqual(used_citations, expected_citations)

        assets = {item["id"]: item for item in self.book["assets"]}
        for asset_id in expected_assets:
            asset = assets[asset_id]
            self.assertTrue(asset["qa"]["approved"])
            self.assertTrue((ROOT / asset["path"]).is_file())
            provenance_path = (ROOT / asset["path"]).with_suffix(".provenance.json")
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            visual_qa = provenance["visual_qa"]
            self.assertTrue(visual_qa["approved"])
            if asset["kind"] == "map":
                self.assertEqual(visual_qa["print_300dpi"], "pass")
                self.assertEqual(visual_qa["mobile_390px"], "pass")
                self.assertEqual(visual_qa["label_collisions"], "pass")
            else:
                self.assertEqual(visual_qa["exact_guide_count_four"], "pass")
                self.assertEqual(visual_qa["b6_print"], "pass")
                self.assertEqual(visual_qa["mobile_390px"], "pass")
                references = {item["path"] for item in provenance["source_images"]}
                self.assertTrue(GUIDE_PATHS.issubset(references))
            for evidence in visual_qa.get("evidence", {}).values():
                path = ROOT / evidence["path"]
                self.assertTrue(evidence["path"].startswith("build/"))
                if asset["kind"] == "map":
                    self.assertTrue(evidence["path"].startswith("build/qa/"))
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                if path.is_file():
                    self.assertEqual(sha256(path), evidence["sha256"])

    def test_itinerary_map_rebuilds_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_itinerary_days_map.py"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        with Image.open(MAP_STEM.with_suffix(".png")) as image:
            self.assertEqual(image.size, (1620, 2280))
        provenance = json.loads(
            MAP_STEM.with_suffix(".provenance.json").read_text(encoding="utf-8")
        )
        for suffix, record in provenance["outputs"].items():
            path = MAP_STEM.with_suffix(f".{suffix}")
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_map_decisions_and_boundaries_are_explicit(self) -> None:
        config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual([lane["duration"] for lane in config["lanes"]], ["1", "2", "3"])
        self.assertEqual([len(lane["nodes"]) for lane in config["lanes"]], [4, 4, 4])
        self.assertTrue(config["lanes"][0]["nodes"][1]["choice"])
        self.assertTrue(config["lanes"][2]["nodes"][2]["choice"])
        self.assertIn("SWAP WHOLE DAYS", config["lanes"][1]["fallback"]["en"])
        self.assertIn("OUTDOOR CLIMB", config["cut_order"]["en"])
        boundaries = " ".join(config["generalizations"]).lower()
        self.assertIn("not official itineraries or timetables", boundaries)
        self.assertIn("alternatives", boundaries)
        self.assertIn("overrides the diagram", boundaries)

    def test_severe_rain_and_cut_order_remain_safe(self) -> None:
        weather = self.chapter["blocks"][8]["text"]
        self.assertIn("可靠的室内或休息", weather["zh"])
        self.assertIn("確かな屋内に移るか休む", weather["ja"])
        self.assertIn("During heavy rain, stay in a reliable indoor place or rest", weather["en"])
        self.assertIn("conditions in the city remain safe for walking", weather["en"])
        callout = self.chapter["blocks"][9]["text"]["en"]
        self.assertIn("extra snack, second street, then outdoor climb", callout)
        self.assertIn("documents, bags, rest, a seated meal", callout)

    def test_current_claims_are_dated_and_prose_avoids_old_shorthand(self) -> None:
        citations = {item["id"]: item for item in self.book["citations"]}
        for citation_id in (
            "src-cma-lanzhou-climate",
            "src-lanzhou-itinerary-days-map-data",
            "src-lanzhou-museum-visit-2026",
        ):
            self.assertEqual(citations[citation_id]["accessed_at"], "2026-08-23")
        english = " ".join(block["text"]["en"] for block in self.chapter["blocks"])
        for rejected in (
            "usable exit",
            "one morning bowl",
            "findspot",
            "recover something missed",
            "arrival and departure margin",
        ):
            self.assertNotIn(rejected, english.lower())


if __name__ == "__main__":
    unittest.main()
