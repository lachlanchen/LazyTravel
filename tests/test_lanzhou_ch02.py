import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/lanzhou/book.json"


class LanzhouChapterTwoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapters = sorted(cls.document["chapters"], key=lambda item: item["order"])
        cls.chapter = cls.chapters[1]

    def test_locked_structure_and_next_gate(self) -> None:
        self.assertEqual(len(self.chapters), 11)
        self.assertEqual(self.chapter["id"], "ch02-arrival-gates")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 9)
        self.assertEqual(self.chapters[2]["id"], "ch03-crossing-capital")
        self.assertEqual(self.chapters[2]["status"], "final")
        self.assertEqual(len(self.chapters[2]["blocks"]), 9)
        self.assertEqual(self.chapters[3]["id"], "ch04-bridge-banks")
        self.assertEqual(self.chapters[3]["status"], "final")
        self.assertEqual(len(self.chapters[3]["blocks"]), 9)
        self.assertEqual(self.chapters[4]["id"], "ch05-museum-route")
        self.assertEqual(self.chapters[4]["status"], "final")
        self.assertEqual(len(self.chapters[4]["blocks"]), 10)
        self.assertEqual(self.chapters[5]["id"], "ch06-food-clock")
        self.assertEqual(self.chapters[5]["status"], "final")
        self.assertEqual(len(self.chapters[5]["blocks"]), 10)
        self.assertEqual(self.chapters[6]["status"], "researching")
        self.assertTrue(all(not chapter["blocks"] for chapter in self.chapters[6:]))

    def test_alignment_review_and_readings_are_closed(self) -> None:
        for block in self.chapter["blocks"]:
            self.assertEqual(set(block["text"]), {"zh", "ja", "en"})
            self.assertTrue(all(block["text"][language] for language in ("zh", "ja", "en")))
            for language in ("zh", "ja", "en"):
                self.assertEqual(block["review"][language]["state"], "final")
            for language in ("zh", "ja"):
                layer = block["readings"][language]
                self.assertEqual(layer["status"], "reviewed")
                reconstructed = "".join(token["text"] for token in layer["tokens"])
                self.assertEqual(reconstructed, block["text"][language])

    def test_station_and_checklist_readings_are_reviewed(self) -> None:
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
                ("中川机场东", "zhōngchuān jīchǎng dōng"),
                ("兰州西站北广场", "lánzhōu xīzhàn běiguǎngchǎng"),
                ("兰州火车站", "lánzhōu huǒchēzhàn"),
                ("第一行", "dìyī háng"),
                ("第二行", "dì'èr háng"),
                ("第三行", "dìsān háng"),
                ("三行", "sān háng"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("中川机场东", "ちゅうせんくうこうひがし"),
                ("兰州西站北广场", "らんしゅうにしえききたひろば"),
                ("兰州火车站", "らんしゅうえき"),
                ("七里河", "しちりが"),
            }.issubset(ja)
        )

    def test_assets_and_citations_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-zhongchuan-t3-arrival",
            "asset-lanzhou-arrival-gates-map",
            "asset-lanzhou-west-station-arrival",
            "asset-lanzhou-railway-station-arrival",
        }
        expected_citations = {
            "src-china-rail-live-booking",
            "src-lanzhou-airport-connections-2026",
            "src-lanzhou-airport-rail-2026",
            "src-lanzhou-airport-t3-2025",
            "src-lanzhou-arrival-map-data",
            "src-lanzhou-metro-hubs-2026",
            "src-lanzhou-metro-service",
            "src-lanzhou-ndrc-airport-2025",
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
        kinds = [assets[asset_id]["kind"] for asset_id in expected_assets]
        self.assertEqual(kinds.count("map"), 1)
        self.assertEqual(kinds.count("illustration"), 3)
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


if __name__ == "__main__":
    unittest.main()
