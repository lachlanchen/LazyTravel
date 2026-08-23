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
MAP_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-onward-gates.config.json"
FIGURE_CONFIG = ROOT / "data/images/lanzhou/ch10-figures.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-onward-gates"
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


class LanzhouChapterTenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][9]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertEqual(self.chapter["id"], "ch10-next-gansu-leg")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch10-b{number:03d}" for number in range(1, 11)],
        )
        next_chapter = self.book["chapters"][10]
        self.assertEqual(next_chapter["id"], "ch11-nearby-day")
        self.assertEqual(next_chapter["status"], "outlined")
        self.assertFalse(next_chapter["blocks"])

    def test_alignment_and_readings_are_closed(self) -> None:
        self.assertEqual(
            [block["kind"] for block in self.chapter["blocks"]],
            [
                "figure",
                "map",
                "figure",
                "practical",
                "figure",
                "figure",
                "practical",
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
                ("张掖", "zhāngyè"),
                ("河西走廊", "héxī zǒuláng"),
                ("祁连山", "qíliánshān"),
                ("一行", "yī háng"),
                ("六行", "liù háng"),
                ("出发点", "chūfādiǎn"),
                ("中川机场东", "zhōngchuān jīchǎng dōng"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("張掖", "ちょうえき"),
                ("河西回廊", "かせいかいろう"),
                ("祁連山", "きれんざん"),
                ("中川空港", "ちゅうせんくうこう"),
                ("空港行き", "くうこうゆき"),
                ("蘭州西駅", "らんしゅうにしえき"),
                ("蘭州駅", "らんしゅうえき"),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-airport-buffer-night",
            "asset-lanzhou-departure-table",
            "asset-lanzhou-onward-gates-map",
            "asset-lanzhou-railway-station-arrival",
            "asset-lanzhou-west-station-arrival",
            "asset-lanzhou-zhongchuan-t3-arrival",
        }
        expected_citations = {
            "src-china-rail-boarding-2026",
            "src-china-rail-live-booking",
            "src-china-rail-priority-service",
            "src-gansu-brief-history-corridor",
            "src-lanzhou-airport-connections-2026",
            "src-lanzhou-airport-rail-2026",
            "src-lanzhou-airport-t3-2025",
            "src-lanzhou-arrival-map-data",
            "src-lanzhou-ibis-airport-2026",
            "src-lanzhou-itinerary-days-map-data",
            "src-lanzhou-metro-hubs-2026",
            "src-lanzhou-metro-service",
            "src-lanzhou-ndrc-airport-2025",
            "src-lanzhou-onward-gates-map-data",
            "src-lanzhou-rail-summer-2026",
            "src-lanzhou-stay-segment-map-data",
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
            self.assertTrue(provenance["visual_qa"]["approved"])

        figure = assets["asset-lanzhou-departure-table"]
        figure_provenance = json.loads(
            (ROOT / figure["path"])
            .with_suffix(".provenance.json")
            .read_text(encoding="utf-8")
        )
        figure_qa = figure_provenance["visual_qa"]
        self.assertEqual(figure_qa["exact_guide_count_four"], "pass")
        self.assertEqual(figure_qa["no_anonymous_people"], "pass")
        self.assertEqual(figure_qa["no_reader_visible_raster_text"], "pass")
        self.assertEqual(figure_qa["b6_print"], "pass")
        self.assertEqual(figure_qa["mobile_390px"], "pass")
        references = {item["path"] for item in figure_provenance["source_images"]}
        self.assertEqual(references, GUIDE_PATHS)
        self._assert_evidence_hashes(figure_qa["evidence"])

        map_provenance = json.loads(
            MAP_STEM.with_suffix(".provenance.json").read_text(encoding="utf-8")
        )
        map_qa = map_provenance["visual_qa"]
        self.assertEqual(map_qa["print_300dpi"], "pass")
        self.assertEqual(map_qa["mobile_390px"], "pass")
        self.assertEqual(map_qa["label_collisions"], "pass")
        self._assert_evidence_hashes(map_qa["evidence"])

    def _assert_evidence_hashes(self, evidence: dict[str, dict[str, object]]) -> None:
        for record in evidence.values():
            path = ROOT / str(record["path"])
            self.assertTrue(str(record["path"]).startswith("build/qa/"))
            self.assertTrue(path.is_file())
            self.assertRegex(str(record["sha256"]), r"^[0-9a-f]{64}$")
            self.assertEqual(sha256(path), record["sha256"])

    def test_onward_map_rebuilds_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_onward_gates_map.py"],
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

    def test_map_keeps_three_exclusive_departure_gates(self) -> None:
        config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            [lane["gate"]["en"] for lane in config["lanes"]],
            [
                "TICKET: LANZHOU WEST",
                "TICKET: LANZHOU STATION",
                "FLIGHT: ZHONGCHUAN T3",
            ],
        )
        self.assertEqual([len(lane["nodes"]) for lane in config["lanes"]], [4, 4, 4])
        self.assertTrue(config["rule"]["en"].startswith("CHOOSE THE NEXT OVERNIGHT"))
        boundary = config["boundary"]["en"].lower()
        self.assertIn("no timetable, fare, or connection is promised", boundary)
        generalizations = " ".join(config["generalizations"]).lower()
        self.assertIn("alternatives selected only by the live booking", generalizations)
        self.assertIn("arrows show planning order", generalizations)
        self.assertIn("does not imply", generalizations)
        serialized = json.dumps(config, ensure_ascii=False).lower()
        for destination in ("wuwei", "zhangye", "jiayuguan", "dunhuang"):
            self.assertNotIn(destination, serialized)

    def test_new_figure_config_uses_only_the_four_guides(self) -> None:
        config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual({guide["path"] for guide in config["guides"]}, GUIDE_PATHS)
        self.assertEqual(len(config["figures"]), 1)
        figure = config["figures"][0]
        self.assertEqual(figure["asset_id"], "asset-lanzhou-departure-table")
        self.assertTrue(figure["selected_raw"].startswith("build/research/"))
        self.assertFalse(figure["official_references"])
        self.assertIn("Blank tickets and screens", " ".join(figure["factual_limits"]))
        self.assertTrue(figure["visual_qa"]["approved"])

    def test_volatile_rules_are_dated_and_bounded(self) -> None:
        citations = {item["id"]: item for item in self.book["citations"]}
        for citation_id in (
            "src-china-rail-boarding-2026",
            "src-china-rail-priority-service",
            "src-lanzhou-rail-summer-2026",
            "src-lanzhou-onward-gates-map-data",
        ):
            self.assertEqual(citations[citation_id]["accessed_at"], "2026-08-23")

        assistance = self.chapter["blocks"][8]["text"]["en"]
        self.assertIn("checked on 23 August 2026", assistance)
        self.assertIn("at least six hours before departure", assistance)
        self.assertIn("no later than 60 minutes before departure", assistance)
        self.assertIn("These timings can change", assistance)

        english = " ".join(block["text"]["en"] for block in self.chapter["blocks"])
        self.assertNotIn("printed gate", english.lower())
        self.assertNotIn("direct train", english.lower())
        self.assertNotIn("guaranteed connection", english.lower())

    def test_lanzhou_station_caption_keeps_the_direction_correct(self) -> None:
        assets = {item["id"]: item for item in self.book["assets"]}
        captions = assets["asset-lanzhou-railway-station-arrival"]["captions"]
        self.assertIn("向东", captions["zh"])
        self.assertNotIn("向西", captions["zh"])
        self.assertIn("東へ", captions["ja"])
        self.assertNotIn("西へ", captions["ja"])
        self.assertIn("eastbound", captions["en"])
        self.assertNotIn("westward", captions["en"])


if __name__ == "__main__":
    unittest.main()
