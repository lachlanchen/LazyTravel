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
MAP_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-stay-segment.config.json"
FIGURE_CONFIG = ROOT / "data/images/lanzhou/ch08-figures.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-stay-segment"
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


class LanzhouChapterEightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][7]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertEqual(self.chapter["id"], "ch08-stay-segment")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch08-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(self.book["chapters"][8]["id"], "ch09-itinerary-days")
        self.assertEqual(self.book["chapters"][8]["status"], "researching")
        self.assertTrue(
            all(not chapter["blocks"] for chapter in self.book["chapters"][8:])
        )

    def test_alignment_and_readings_are_closed(self) -> None:
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

    def test_lodging_place_and_date_readings_are_reviewed(self) -> None:
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
                ("正宁路", "zhèngníng lù"),
                ("永昌南路", "yǒngchāng nánlù"),
                ("七里河", "qīlǐhé"),
                ("西站十字", "xīzhàn shízì"),
                ("建兰", "jiànlán"),
                ("天水中路", "tiānshuǐ zhōnglù"),
                ("中川机场", "zhōngchuān jīchǎng"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("正寧路", "せいねいろ"),
                ("永昌南路", "えいしょうなんろ"),
                ("七里河", "しちりが"),
                ("天水中路", "てんすいちゅうろ"),
                ("中川空港", "ちゅうせんくうこう"),
                ("深夜着", "しんやちゃく"),
                ("一泊", "いっぱく"),
                ("二十四時間", "にじゅうよじかん"),
                ("二〇二四年", "にせんにじゅうよねん"),
                (
                    "二〇二六年八月二十二日",
                    "にせんにじゅうろくねんはちがつにじゅうににち",
                ),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-central-side-street-arrival",
            "asset-lanzhou-stay-segment-map",
            "asset-lanzhou-west-station-arrival",
            "asset-lanzhou-railway-station-arrival",
            "asset-lanzhou-airport-buffer-night",
        }
        expected_citations = {
            "src-china-foreign-lodging-circular-2024",
            "src-china-hotel-registration-2025",
            "src-china-nia-registration-2026",
            "src-lanzhou-airport-connections-2026",
            "src-lanzhou-airport-t3-2025",
            "src-lanzhou-arrival-map-data",
            "src-lanzhou-geography-2026",
            "src-lanzhou-hiex-jianlan-2026",
            "src-lanzhou-hilton-city-center-2026",
            "src-lanzhou-ibis-airport-2026",
            "src-lanzhou-mercure-zhengning-2026",
            "src-lanzhou-metro-hubs-2026",
            "src-lanzhou-metro-service",
            "src-lanzhou-museum-visit-2026",
            "src-lanzhou-stay-segment-map-data",
            "src-lanzhou-tourism-2026",
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
                self.assertTrue(evidence["path"].startswith("build/qa/"))
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                if path.is_file():
                    self.assertEqual(sha256(path), evidence["sha256"])

    def test_stay_map_rebuilds_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_stay_segment_map.py"],
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

    def test_segment_and_figure_boundaries_are_explicit(self) -> None:
        map_config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        figure_config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            [segment["id"] for segment in map_config["segments"]],
            ["west", "centre", "east", "airport"],
        )
        self.assertIn("ARRIVAL POINT", map_config["rule"]["en"])
        self.assertTrue(
            any("no transfer line" in item for item in map_config["generalizations"])
        )
        self.assertTrue(
            any("No named property" in item for item in map_config["generalizations"])
        )
        self.assertEqual(len(figure_config["figures"]), 2)
        self.assertTrue(
            all(item["visual_qa"]["approved"] for item in figure_config["figures"])
        )

    def test_named_property_examples_are_dated_not_ranked(self) -> None:
        citations = {item["id"]: item for item in self.book["citations"]}
        operator_ids = {
            "src-lanzhou-mercure-zhengning-2026",
            "src-lanzhou-hiex-jianlan-2026",
            "src-lanzhou-hilton-city-center-2026",
            "src-lanzhou-ibis-airport-2026",
        }
        for citation_id in operator_ids:
            citation = citations[citation_id]
            self.assertEqual(citation["source_type"], "official-web")
            self.assertEqual(citation["accessed_at"], "2026-08-22")
            locator = citation["locator"].lower()
            self.assertIn("rechecked 2026-08-22", locator)
            boundaries = " ".join(citation["supports"]).lower()
            self.assertTrue(
                any(word in boundaries for word in ("boundary", "need to", "direct"))
            )


if __name__ == "__main__":
    unittest.main()
