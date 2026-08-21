import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/lanzhou/book.json"


class LanzhouChapterThreeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapters = sorted(cls.document["chapters"], key=lambda item: item["order"])
        cls.chapter = cls.chapters[2]

    def test_locked_structure_and_next_gate(self) -> None:
        self.assertEqual(len(self.chapters), 11)
        self.assertEqual(self.chapter["id"], "ch03-crossing-capital")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 9)
        self.assertEqual(self.chapters[3]["id"], "ch04-bridge-banks")
        self.assertEqual(self.chapters[3]["status"], "final")
        self.assertEqual(len(self.chapters[3]["blocks"]), 9)
        self.assertEqual(self.chapters[4]["id"], "ch05-museum-route")
        self.assertEqual(self.chapters[4]["status"], "researching")
        self.assertTrue(all(not chapter["blocks"] for chapter in self.chapters[4:]))

    def test_alignment_review_and_readings_are_closed(self) -> None:
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
                ("五泉", "wǔquán"),
                ("张掖路", "zhāngyè lù"),
                ("兰州府城隍庙", "lánzhōufǔ chénghuángmiào"),
                ("甘肃巡抚", "gānsù xúnfǔ"),
                ("陕甘总督", "shǎn-gān zǒngdū"),
                ("天兰铁路", "tiānlán tiělù"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("五泉", "ごせん"),
                ("張掖路", "ちょうえきろ"),
                ("蘭州府城隍廟", "らんしゅうふじょうこうびょう"),
                ("甘粛巡撫", "かんしゅくじゅんぶ"),
                ("陝甘総督", "せんかんそうとく"),
                ("天蘭鉄道", "てんらんてつどう"),
            }.issubset(ja)
        )

    def test_assets_and_citations_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-city-god-temple",
            "asset-lanzhou-history-walk-map",
        }
        expected_citations = {
            "src-gansu-brief-history-lanzhou",
            "src-lanzhou-1954-plan",
            "src-lanzhou-bridge-history",
            "src-lanzhou-chengguan-history",
            "src-lanzhou-city-chronicle",
            "src-lanzhou-city-god-current-2026",
            "src-lanzhou-city-god-temple",
            "src-lanzhou-history-map-data",
            "src-lanzhou-jincheng-debate",
            "src-lanzhou-old-city-gates",
            "src-lanzhou-old-city-streets",
            "src-lanzhou-railway-history",
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

        assets = {item["id"]: item for item in self.document["assets"]}
        for asset_id in expected_assets:
            asset = assets[asset_id]
            self.assertTrue(asset["qa"]["approved"])
            self.assertTrue((ROOT / asset["path"]).is_file())
            provenance_path = (ROOT / asset["path"]).with_suffix(".provenance.json")
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            self.assertTrue(provenance["visual_qa"]["approved"])
            if asset["kind"] == "illustration":
                self.assertEqual(
                    provenance["visual_qa"]["exact_guide_count_four"], "pass"
                )
                self.assertEqual(provenance["visual_qa"]["b6_print"], "pass")
                self.assertEqual(provenance["visual_qa"]["mobile_390px"], "pass")
            else:
                self.assertEqual(provenance["visual_qa"]["print_300dpi"], "pass")
                self.assertEqual(provenance["visual_qa"]["mobile_390px"], "pass")
                self.assertEqual(provenance["visual_qa"]["label_collisions"], "pass")

    def test_chapter_four_keeps_bridge_and_white_pagoda_hill(self) -> None:
        chapter_four = self.chapters[3]
        combined_title = " ".join(chapter_four["titles"].values())
        self.assertIn("黄河铁桥", combined_title)
        self.assertIn("白塔山", combined_title)
        self.assertIn("Yellow River Iron Bridge", combined_title)
        self.assertIn("White Pagoda Hill", combined_title)

    def test_rejected_name_typo_is_absent(self) -> None:
        chapter_json = json.dumps(self.chapter, ensure_ascii=False)
        self.assertNotIn("武泉", chapter_json)
        self.assertNotIn("Wuqan", chapter_json)


if __name__ == "__main__":
    unittest.main()
