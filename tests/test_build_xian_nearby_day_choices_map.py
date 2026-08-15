from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class XianNearbyDayChoicesMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-nearby-day-choices.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_exactly_five_ordered_choices(self) -> None:
        choices = self.config["choices"]
        self.assertEqual([choice["order"] for choice in choices], [1, 2, 3, 4, 5])
        self.assertEqual(
            [choice["id"] for choice in choices],
            ["lintong", "huashan", "hanyangling", "cuihuashan", "qianling"],
        )

    def test_choice_positions_fit_the_declared_extent(self) -> None:
        west, south, east, north = self.config["extent"]
        for choice in self.config["choices"]:
            longitude, latitude = choice["position"]
            self.assertLess(west, longitude)
            self.assertLess(longitude, east)
            self.assertLess(south, latitude)
            self.assertLess(latitude, north)

    def test_connectors_are_direction_only(self) -> None:
        note = self.config["connector_note"].lower()
        self.assertIn("not railway lines", note)
        self.assertIn("measured travel times", note)
        self.assertIn("live navigation", note)
        for choice in self.config["choices"]:
            self.assertNotIn("route", choice)
            self.assertNotIn("journey_time", choice)
            self.assertNotIn("fare", choice)

    def test_trilingual_transport_cards_are_complete(self) -> None:
        for choice in self.config["choices"]:
            for field in ("label", "focus", "transport"):
                self.assertEqual(set(choice[field]), {"zh", "ja", "en"})
                self.assertTrue(all(choice[field].values()))


if __name__ == "__main__":
    unittest.main()
