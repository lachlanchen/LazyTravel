from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class XianArrivalHubsMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-arrival-hubs.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_exactly_four_named_hubs(self) -> None:
        hubs = self.config["hubs"]
        self.assertEqual([hub["order"] for hub in hubs], [1, 2, 3, 4])
        self.assertEqual(
            [hub["id"] for hub in hubs],
            ["xian-airport", "xian-north", "xian-station", "xian-east"],
        )

    def test_hubs_fit_the_declared_extent(self) -> None:
        west, south, east, north = self.config["extent"]
        for hub in self.config["hubs"]:
            longitude, latitude = hub["position"]
            self.assertLess(west, longitude)
            self.assertLess(longitude, east)
            self.assertLess(south, latitude)
            self.assertLess(latitude, north)

    def test_only_first_transfer_spines_are_shown(self) -> None:
        self.assertEqual(
            [spine["number"] for spine in self.config["spines"]],
            ["14", "2", "4", "5"],
        )
        notes = " ".join(
            [self.config["visual_qa"]["notes"]]
            + [source["note"] for source in self.config["sources"]]
        ).lower()
        self.assertIn("omits the rest of the network", notes)
        self.assertIn("no line claims a full route", notes)

    def test_trilingual_decision_cards_are_complete(self) -> None:
        cards = self.config["cards"]
        self.assertEqual([card["order"] for card in cards], [1, 2, 3, 4])
        for card in cards:
            for language in ("zh", "ja", "en"):
                self.assertTrue(card[language])


if __name__ == "__main__":
    unittest.main()
