from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class XianStayAreasMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-stay-areas.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_exactly_five_locked_zones(self) -> None:
        zones = self.config["zones"]
        self.assertEqual([zone["order"] for zone in zones], [1, 2, 3, 4, 5])
        self.assertEqual(
            [zone["id"] for zone in zones],
            [
                "inside-wall",
                "south-gate",
                "yanta-qujiang",
                "xian-north-corridor",
                "lintong",
            ],
        )

    def test_zones_fit_their_declared_panels(self) -> None:
        extents = {
            "central": self.config["central_extent"],
            "regional": self.config["regional_extent"],
        }
        for zone in self.config["zones"]:
            west, south, east, north = extents[zone["panel"]]
            longitude, latitude = zone["position"]
            self.assertLess(west, longitude)
            self.assertLess(longitude, east)
            self.assertLess(south, latitude)
            self.assertLess(latitude, north)

    def test_trilingual_cards_match_the_zones(self) -> None:
        cards = self.config["cards"]
        self.assertEqual([card["order"] for card in cards], [1, 2, 3, 4, 5])
        for card in cards:
            for language in ("zh", "ja", "en"):
                self.assertTrue(card[language])

    def test_map_declares_non_navigation_limits(self) -> None:
        notes = " ".join(
            [self.config["visual_qa"]["notes"]]
            + [feature["note"] for feature in self.config["schematic_features"].values()]
            + [zone["note"] for zone in self.config["zones"]]
            + [source["note"] for source in self.config["sources"]]
        ).lower()
        self.assertIn("not track geometry", notes)
        self.assertIn("omits the rest of the network", notes)
        self.assertIn("not a hotel boundary", notes)


if __name__ == "__main__":
    unittest.main()
