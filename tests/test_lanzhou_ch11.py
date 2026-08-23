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
MAP_CONFIG = ROOT / "data/maps/lanzhou/lanzhou-nearby-day.config.json"
FIGURE_CONFIG = ROOT / "data/images/lanzhou/ch11-figures.config.json"
MAP_STEM = ROOT / "assets/maps/lanzhou/lanzhou-nearby-day"
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


class LanzhouChapterElevenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.book = json.loads(BOOK_PATH.read_text(encoding="utf-8"))
        cls.chapter = cls.book["chapters"][10]

    def test_destination_and_locked_chapter_are_complete(self) -> None:
        self.assertEqual(self.book["book"]["status"], "complete")
        self.assertEqual(self.book["book"]["edition"], "research-edition-2026-08-23")
        self.assertEqual(len(self.book["chapters"]), 11)
        self.assertTrue(all(chapter["status"] == "final" for chapter in self.book["chapters"]))
        self.assertEqual(self.chapter["id"], "ch11-nearby-day")
        self.assertEqual(
            [block["id"] for block in self.chapter["blocks"]],
            [f"ch11-b{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(
            [block["kind"] for block in self.chapter["blocks"]],
            [
                "figure",
                "map",
                "figure",
                "practical",
                "figure",
                "figure",
                "figure",
                "practical",
                "practical",
                "callout",
            ],
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
                self.assertEqual(
                    "".join(token["text"] for token in layer["tokens"]),
                    block["text"][language],
                )

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
                ("炳灵寺", "bǐnglíngsì"),
                ("刘家峡", "liújiāxiá"),
                ("黄洮交汇", "huáng-táo jiāohuì"),
                ("兴隆山", "xīnglóngshān"),
                ("水墨丹霞", "shuǐmò dānxiá"),
                ("建弘元年", "jiànhóng yuánnián"),
                ("西秦", "xīqín"),
                ("去程", "qùchéng"),
            }.issubset(zh)
        )
        self.assertTrue(
            {
                ("炳霊寺", "へいれいじ"),
                ("劉家峡", "りゅうかきょう"),
                ("興隆山", "こうりゅうざん"),
                ("水墨丹霞", "すいぼくたんか"),
                ("建弘元年", "けんこうがんねん"),
                ("西秦", "せいしん"),
                ("石窟", "せっくつ"),
                ("水況", "すいきょう"),
                ("市内", "しない"),
            }.issubset(ja)
        )

    def test_assets_citations_and_visual_evidence_are_closed(self) -> None:
        expected_assets = {
            "asset-lanzhou-nearby-day-choice",
            "asset-lanzhou-nearby-day-map",
            "asset-lanzhou-bingling-grottoes-day",
            "asset-lanzhou-yellow-tao-confluence",
            "asset-lanzhou-xinglong-forest-gorge",
            "asset-lanzhou-ink-danxia-route",
        }
        expected_citations = {
            "src-bingling-closure-2025",
            "src-bingling-dha",
            "src-bingling-history-420",
            "src-bingling-route-2024",
            "src-bingling-traffic-safety-2026",
            "src-cma-lanzhou-climate",
            "src-gansu-brief-history-bingling",
            "src-gansu-ningxia-guide-2014",
            "src-ink-danxia-2026",
            "src-ink-danxia-weather-2025",
            "src-lanzhou-itinerary-days-map-data",
            "src-lanzhou-nearby-day-map-data",
            "src-linxia-nearby-route-2026",
            "src-unesco-silk-roads",
            "src-xinglong-landscape-2024",
            "src-xinglong-recovery-2026",
            "src-xinglong-s104-2026",
            "src-yellow-tao-viewpoint-2025",
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
            path = ROOT / asset["path"]
            self.assertTrue(asset["qa"]["approved"])
            self.assertTrue(path.is_file())
            provenance = json.loads(
                path.with_suffix(".provenance.json").read_text(encoding="utf-8")
            )
            visual = provenance["visual_qa"]
            self.assertTrue(visual["approved"])
            if asset["kind"] == "map":
                self.assertEqual(visual["print_300dpi"], "pass")
                self.assertEqual(visual["mobile_390px"], "pass")
                self.assertEqual(visual["label_collisions"], "pass")
            else:
                self.assertEqual(visual["exact_guide_count_four"], "pass")
                self.assertEqual(visual["no_anonymous_people"], "pass")
                self.assertEqual(visual["b6_print"], "pass")
                self.assertEqual(visual["mobile_390px"], "pass")
                references = {item["path"] for item in provenance["source_images"]}
                self.assertTrue(GUIDE_PATHS.issubset(references))
            self._assert_evidence_hashes(visual["evidence"])

    def _assert_evidence_hashes(self, evidence: dict[str, dict[str, object]]) -> None:
        self.assertTrue(evidence)
        for record in evidence.values():
            path = ROOT / str(record["path"])
            self.assertTrue(str(record["path"]).startswith("build/qa/"))
            self.assertTrue(path.is_file())
            self.assertRegex(str(record["sha256"]), r"^[0-9a-f]{64}$")
            self.assertEqual(sha256(path), record["sha256"])

    def test_nearby_map_rebuilds_at_b6_print_resolution(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_lanzhou_nearby_day_map.py"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        with Image.open(MAP_STEM.with_suffix(".png")) as image:
            self.assertEqual(image.size, (1620, 2280))
        provenance = json.loads(
            MAP_STEM.with_suffix(".provenance.json").read_text(encoding="utf-8")
        )
        for record in provenance["outputs"].values():
            path = ROOT / record["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(sha256(path), record["sha256"])

    def test_map_keeps_three_exclusive_complete_return_branches(self) -> None:
        config = json.loads(MAP_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["snapshot_date"], "2026-08-23")
        self.assertEqual(len(config["branches"]), 3)
        self.assertEqual(
            [branch["name"]["en"] for branch in config["branches"]],
            [
                "BINGLING TEMPLE + LIUJIAXIA",
                "XINGLONG: DIRECT REOPENING CHECK",
                "LANZHOU INK DANXIA",
            ],
        )
        self.assertEqual([len(branch["nodes"]) for branch in config["branches"]], [3, 3, 3])
        self.assertIn("conditional", config["branches"][0])
        self.assertNotIn("conditional", config["branches"][1])
        self.assertNotIn("conditional", config["branches"][2])
        self.assertIn("CHOOSE ONE OF THREE", config["rule"]["en"])
        self.assertIn("DROP THE WHOLE BRANCH", config["cancel"]["en"])
        boundaries = " ".join(config["generalizations"]).lower()
        self.assertIn("mutually exclusive complete-return choices", boundaries)
        self.assertIn("not included in a boat ticket or transfer", boundaries)
        self.assertIn("does not establish current reopening", boundaries)
        self.assertIn("not distance, direction, duration", boundaries)

    def test_figure_config_uses_the_exact_four_guides(self) -> None:
        config = json.loads(FIGURE_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual({guide["path"] for guide in config["guides"]}, GUIDE_PATHS)
        self.assertEqual(len(config["figures"]), 5)
        self.assertEqual(
            {figure["asset_id"] for figure in config["figures"]},
            {
                "asset-lanzhou-nearby-day-choice",
                "asset-lanzhou-bingling-grottoes-day",
                "asset-lanzhou-yellow-tao-confluence",
                "asset-lanzhou-xinglong-forest-gorge",
                "asset-lanzhou-ink-danxia-route",
            },
        )
        for figure in config["figures"]:
            self.assertTrue(figure["selected_raw"].startswith("build/research/"))
            self.assertTrue(figure["visual_qa"]["approved"])
            self.assertEqual(figure["visual_qa"]["exact_guide_count_four"], "pass")
            self.assertRegex(figure["qa_evidence"]["b6_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(figure["qa_evidence"]["mobile_sha256"], r"^[0-9a-f]{64}$")

    def test_volatile_advice_is_dated_and_bounded(self) -> None:
        citations = {item["id"]: item for item in self.book["citations"]}
        used_citations = {
            citation_id
            for block in self.chapter["blocks"]
            for citation_id in block["citation_ids"]
        }
        self.assertTrue(
            all(citations[citation_id]["accessed_at"] == "2026-08-23" for citation_id in used_citations)
        )
        english = " ".join(block["text"]["en"] for block in self.chapter["blocks"])
        self.assertIn("At this book's check on 23 August 2026", english)
        self.assertIn("no authoritative notice was found", english)
        self.assertIn("preserves neither a price nor a promise of free entry", english)
        self.assertIn("prints no train, boat, fare, or fixed duration", english)
        self.assertIn("Current site, transport, road", " ".join(json.loads(MAP_CONFIG.read_text())["generalizations"]))

    def test_release_builder_includes_chapter_eleven_generators(self) -> None:
        builder = (ROOT / "scripts/build_lanzhou_review.py").read_text(encoding="utf-8")
        self.assertIn("scripts/build_lanzhou_nearby_day_map.py", builder)
        self.assertIn("scripts/prepare_lanzhou_ch11_figures.py", builder)


if __name__ == "__main__":
    unittest.main()
