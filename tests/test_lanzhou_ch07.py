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
MAP_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-height-choice.config.json"
FIGURE_CONFIG = ROOT / "data/images/lanzhou/ch07-figures.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-height-choice"
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


class LanzhouChapterSevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][6]

    def test_locked_blocks_and_next_gate(self) -> None:
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertEqual(self.chapter["id"], "ch07-city-heights")
        self.assertEqual(self.chapter["status"], "final")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch07-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(self.book["chapters"][7]["id"], "ch08-stay-segment")
        self.assertEqual(self.book["chapters"][7]["status"], "researching")
        self.assertTrue(
            all(not chapter["blocks"] for chapter in self.book["chapters"][7:])
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

    def test_height_and_spring_readings_are_reviewed(self) -> None:
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
                ("白塔山", "báitǎshān"),
                ("中山桥", "zhōngshānqiáo"),
                ("兰山", "lánshān"),
                ("三台阁", "sāntáigé"),
                ("五泉山", "wǔquánshān"),
                ("摸子", "mōzǐ"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("白塔山", "はくとうざん"),
                ("中山橋", "ちゅうざんきょう"),
                ("蘭山", "らんざん"),
                ("三台閣", "さんたいかく"),
                ("五泉山", "ごせんざん"),
                ("摸子", "もーず"),
            }.issubset(ja)
        )

    def test_assets_citations_and_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-white-pagoda-hill",
            "asset-lanzhou-height-choice-map",
            "asset-lanzhou-lanshan-santai-view",
            "asset-lanzhou-wuquan-heritage-park",
        }
        expected_citations = {
            "src-lanzhou-baita-current-2025",
            "src-lanzhou-baita-gazetteer",
            "src-lanzhou-bridge-hill-map-data",
            "src-lanzhou-geography-2026",
            "src-lanzhou-height-choice-map-data",
            "src-lanzhou-heights-access-2026",
            "src-lanzhou-heights-geography-2025",
            "src-lanzhou-lanshan-holiday-bus-2026",
            "src-lanzhou-lanshan-record-2025",
            "src-lanzhou-wuquan-flood-2026",
            "src-lanzhou-wuquan-heritage-2021",
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
                self.assertTrue(evidence["path"].startswith("build/qa/"))
                self.assertRegex(evidence["sha256"], r"^[0-9a-f]{64}$")
                if path.is_file():
                    self.assertEqual(sha256(path), evidence["sha256"])

    def test_height_map_rebuilds_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_height_choice_map.py"],
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

    def test_choice_map_and_figure_boundaries_are_explicit(self) -> None:
        map_config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        figure_config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            [choice["id"] for choice in map_config["choices"]],
            ["white-pagoda-hill", "lanshan-santai", "wuquan-mountain-park"],
        )
        self.assertEqual(
            [check["number"] for check in map_config["checks"]], [1, 2, 3, 4]
        )
        self.assertTrue(
            any("No path is drawn" in item for item in map_config["generalizations"])
        )
        self.assertEqual(len(figure_config["figures"]), 2)
        self.assertTrue(
            all(item["visual_qa"]["approved"] for item in figure_config["figures"])
        )


if __name__ == "__main__":
    unittest.main()
