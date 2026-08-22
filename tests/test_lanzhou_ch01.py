import json
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "data/china/cities/lanzhou/book.json"


class LanzhouChapterOneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapters = sorted(cls.document["chapters"], key=lambda item: item["order"])
        cls.chapter = cls.chapters[0]

    def test_locked_structure_and_gate(self) -> None:
        self.assertEqual(len(self.chapters), 11)
        self.assertEqual(self.chapter["id"], "ch01-read-valley")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(len(self.chapter["blocks"]), 8)
        self.assertEqual(self.chapters[1]["status"], "final")
        self.assertEqual(len(self.chapters[1]["blocks"]), 9)
        self.assertEqual(self.chapters[2]["status"], "final")
        self.assertEqual(len(self.chapters[2]["blocks"]), 9)
        self.assertEqual(self.chapters[3]["status"], "final")
        self.assertEqual(len(self.chapters[3]["blocks"]), 9)
        self.assertEqual(self.chapters[4]["id"], "ch05-museum-route")
        self.assertEqual(self.chapters[4]["status"], "final")
        self.assertEqual(len(self.chapters[4]["blocks"]), 10)
        self.assertEqual(self.chapters[5]["id"], "ch06-food-clock")
        self.assertEqual(self.chapters[5]["status"], "final")
        self.assertEqual(len(self.chapters[5]["blocks"]), 10)
        self.assertEqual(self.chapters[6]["status"], "final")
        self.assertEqual(len(self.chapters[6]["blocks"]), 10)
        self.assertEqual(self.chapters[7]["id"], "ch08-stay-segment")
        self.assertEqual(self.chapters[7]["status"], "final")
        self.assertEqual(len(self.chapters[7]["blocks"]), 10)
        self.assertEqual(self.chapters[8]["id"], "ch09-itinerary-days")
        self.assertEqual(self.chapters[8]["status"], "researching")
        self.assertTrue(all(not chapter["blocks"] for chapter in self.chapters[8:]))

    def test_readings_are_reviewed_and_reconstruct_text(self) -> None:
        for block in self.chapter["blocks"]:
            for language in ("zh", "ja"):
                layer = block["readings"][language]
                self.assertEqual(layer["status"], "reviewed")
                reconstructed = "".join(token["text"] for token in layer["tokens"])
                self.assertEqual(reconstructed, block["text"][language])
                self.assertEqual(block["review"][language]["state"], "final")

    def test_assets_and_citations_are_closed(self) -> None:
        citations = {item["id"] for item in self.document["citations"]}
        assets = {item["id"]: item for item in self.document["assets"]}
        used_assets = {
            asset_id
            for block in self.chapter["blocks"]
            for asset_id in block["asset_ids"]
        }
        self.assertEqual(
            used_assets,
            {
                "asset-lanzhou-river-valley-orientation",
                "asset-lanzhou-valley-orientation-map",
            },
        )
        for block in self.chapter["blocks"]:
            self.assertTrue(set(block["citation_ids"]).issubset(citations))
        for asset_id in used_assets:
            self.assertTrue(assets[asset_id]["qa"]["approved"])
            provenance_path = (ROOT / assets[asset_id]["path"]).with_suffix(
                ".provenance.json"
            )
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            self.assertTrue(provenance["visual_qa"]["approved"])

    def test_cover_is_exact_b6_underlay(self) -> None:
        cover = ROOT / "assets/images/lanzhou/lanzhou-cover-underlay.png"
        provenance = json.loads(
            cover.with_suffix(".provenance.json").read_text(encoding="utf-8")
        )
        with Image.open(cover) as image:
            self.assertEqual(image.size, (1476, 2079))
        self.assertTrue(provenance["visual_qa"]["approved"])
        self.assertEqual(provenance["visual_qa"]["exact_guide_count_four"], "pass")
        self.assertEqual(provenance["visual_qa"]["no_raster_text"], "pass")


if __name__ == "__main__":
    unittest.main()
