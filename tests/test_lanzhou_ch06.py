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
ORDER_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-noodle-order.config.json"
CLOCK_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-food-clock.config.json"
FIGURE_CONFIG = ROOT / "data/images/lanzhou/ch06-figures.config.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class LanzhouChapterSixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][5]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertEqual(self.chapter["id"], "ch06-food-clock")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch06-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(self.book["chapters"][6]["id"], "ch07-city-heights")
        self.assertEqual(self.book["chapters"][6]["status"], "researching")
        self.assertTrue(all(not chapter["blocks"] for chapter in self.book["chapters"][6:]))

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

    def test_food_and_menu_readings_are_reviewed(self) -> None:
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
                ("牛肉面", "niúròumiàn"),
                ("毛细", "máoxì"),
                ("二细", "èrxì"),
                ("韭叶", "jiǔyè"),
                ("酿皮子", "niàngpízi"),
                ("灰豆子", "huīdòuzi"),
                ("甜醅子", "tiánpēizi"),
                ("三炮台", "sānpàotái"),
                ("兰州百合", "lánzhōu bǎihé"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("毛细", "まおしー"),
                ("二细", "あるしー"),
                ("韭叶", "じういえ"),
                ("酿皮子", "にゃんぴーず"),
                ("灰豆子", "ふいどうず"),
                ("甜醅子", "てぃえんぺいず"),
                ("三炮台", "さんぱおたい"),
                ("蘭州百合", "らんしゅうゆり"),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-beef-noodle-morning",
            "asset-lanzhou-noodle-order-diagram",
            "asset-lanzhou-food-clock-diagram",
            "asset-lanzhou-afternoon-snacks",
            "asset-lanzhou-lily-sanpaotai",
        }
        expected_citations = {
            "src-lanzhou-food-source-2020",
            "src-lanzhou-beef-noodle-ich",
            "src-lanzhou-noodle-order-2022",
            "src-lanzhou-food-context-2026",
            "src-lanzhou-summer-foods-2023",
            "src-lanzhou-lily-gi-2025",
            "src-lanzhou-sanpaotai-consumer-2022",
            "src-lanzhou-noodle-order-map-data",
            "src-lanzhou-food-clock-map-data",
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
                references = {item["path"] for item in provenance["source_images"]}
                self.assertTrue(
                    {
                        "/home/lachlan/ProjectsLFS/LALACHAN/ayachan.png",
                        "/home/lachlan/ProjectsLFS/LALACHAN/raraxia.jpeg",
                        "/home/lachlan/ProjectsLFS/LALACHAN/sasakun.jpeg",
                        "/home/lachlan/ProjectsLFS/LALACHAN/LazyingArtRobot.png",
                    }.issubset(references)
                )
            for evidence in visual_qa.get("evidence", {}).values():
                path = ROOT / evidence["path"]
                self.assertTrue(evidence["path"].startswith("build/qa/"))
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                if path.is_file():
                    self.assertEqual(sha256(path), evidence["sha256"])

    def test_diagrams_rebuild_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_food_diagrams.py"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        for stem in (
            ROOT / "assets/maps/lanzhou/lanzhou-noodle-order",
            ROOT / "assets/maps/lanzhou/lanzhou-food-clock",
        ):
            with Image.open(stem.with_suffix(".png")) as image:
                self.assertEqual(image.size, (1620, 2280))
            for suffix in (".svg", ".pdf", ".png", ".provenance.json"):
                self.assertTrue(stem.with_suffix(suffix).is_file())

    def test_diagram_boundaries_are_explicit(self) -> None:
        order = json.loads(ORDER_CONFIG.read_text(encoding="utf-8"))
        clock = json.loads(CLOCK_CONFIG.read_text(encoding="utf-8"))
        figures = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual([step["number"] for step in order["steps"]], list(range(1, 6)))
        self.assertEqual(len(order["shape_groups"]), 3)
        self.assertTrue(any("not a plan" in item for item in order["generalizations"]))
        self.assertEqual([phase["number"] for phase in clock["phases"]], list(range(1, 5)))
        self.assertTrue(any("opening-hours" in item for item in clock["generalizations"]))
        self.assertEqual(len(figures["figures"]), 3)


if __name__ == "__main__":
    unittest.main()
