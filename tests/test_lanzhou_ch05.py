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
ROUTE_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-museum-route.config.json"
FINSPOTS_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-museum-findspots.config.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class LanzhouChapterFiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][4]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(self.chapter["id"], "ch05-museum-route")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch05-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(self.book["chapters"][5]["id"], "ch06-food-clock")
        self.assertEqual(self.book["chapters"][5]["status"], "researching")
        self.assertTrue(all(not chapter["blocks"] for chapter in self.book["chapters"][5:]))

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

    def test_specialist_readings_are_reviewed(self) -> None:
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
                ("甘肃省博物馆", "gānsù shěng bówùguǎn"),
                ("人头形器口彩陶瓶", "réntóuxíng qìkǒu cǎitáopíng"),
                ("鲵鱼纹彩陶瓶", "níyúwén cǎitáopíng"),
                ("棨传", "qǐ chuán"),
                ("长尾", "chángwěi"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("甘粛省博物館", "かんしゅくしょうはくぶつかん"),
                ("人頭形器口彩陶瓶", "じんとうけいきこうさいとうへい"),
                ("鯢魚文彩陶瓶", "げいぎょもんさいとうへい"),
                ("三本", "さんぼん"),
                ("四段階", "よんだんかい"),
                ("一組", "ひとくみ"),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-gansu-provincial-museum-exterior",
            "asset-lanzhou-museum-route-map",
            "asset-lanzhou-museum-pottery-gallery",
            "asset-lanzhou-museum-findspots-map",
        }
        expected_citations = {
            "src-lanzhou-museum-buddhist-objects-2026",
            "src-lanzhou-museum-findspot-map-data",
            "src-lanzhou-museum-floor-2026",
            "src-lanzhou-museum-galleries-2026",
            "src-lanzhou-museum-pottery-objects-2026",
            "src-lanzhou-museum-route-map-data",
            "src-lanzhou-museum-silk-objects-2026",
            "src-lanzhou-museum-visit-2026",
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
        self.assertEqual(
            [assets[asset_id]["kind"] for asset_id in expected_assets].count("map"),
            2,
        )
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
            for evidence in visual_qa["evidence"].values():
                path = ROOT / evidence["path"]
                self.assertTrue(evidence["path"].startswith("build/qa/"))
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                if path.is_file():
                    self.assertEqual(sha256(path), evidence["sha256"])

    def test_maps_rebuild_at_b6_print_resolution(self) -> None:
        scripts = (
            "scripts/build_lanzhou_museum_route_map.py",
            "scripts/build_lanzhou_museum_findspots_map.py",
        )
        stems = (
            ROOT / "assets/maps/lanzhou/lanzhou-museum-route",
            ROOT / "assets/maps/lanzhou/lanzhou-museum-findspots",
        )
        for script, stem in zip(scripts, stems, strict=True):
            subprocess.run(
                [sys.executable, script],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            with Image.open(stem.with_suffix(".png")) as image:
                self.assertEqual(image.size, (1620, 2280))
            for suffix in (".svg", ".pdf", ".png", ".provenance.json"):
                self.assertTrue(stem.with_suffix(suffix).is_file())

    def test_route_and_findspot_boundaries_are_explicit(self) -> None:
        route = json.loads(ROUTE_CONFIG.read_text(encoding="utf-8"))
        findspots = json.loads(FINSPOTS_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            [stop["number"] for floor in route["floors"] for stop in floor["stops"]],
            [2, 3, 4, 1, 5],
        )
        self.assertEqual([point["number"] for point in findspots["points"]], list(range(7)))
        self.assertTrue(
            any("room-level navigation map" in item for item in route["generalizations"])
        )
        self.assertTrue(any("not excavation coordinates" in item for item in findspots["generalizations"]))


if __name__ == "__main__":
    unittest.main()
