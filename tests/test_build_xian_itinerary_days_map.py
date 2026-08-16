from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class XianItineraryDaysMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-itinerary-days.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_nested_plan_has_exactly_five_days(self) -> None:
        self.assertEqual(
            [card["day"] for card in self.config["day_cards"]], [1, 2, 3, 4, 5]
        )
        rule = " ".join(self.config["nested_rule"].values())
        self.assertIn("2 DAYS", rule)
        self.assertIn("3 DAYS", rule)
        self.assertIn("5 DAYS", rule)

    def test_day_four_choices_are_mutually_exclusive(self) -> None:
        choices = self.config["regional_days"]["day_4_choices"]
        self.assertEqual(
            [choice["id"] for choice in choices],
            ["huashan", "hanyangling", "cuihuashan", "qianling"],
        )
        self.assertIn("CHOOSE ONE", self.config["regional_days"]["day_4_note"]["en"])

    def test_day_three_fallback_replaces_instead_of_extends(self) -> None:
        day_3 = self.config["urban_context"]["day_3"]
        self.assertEqual(len(day_3["sites"]), 2)
        self.assertEqual(day_3["fallback"]["id"], "small-wild-goose-pagoda")
        self.assertIn("replaces", day_3["note"])

    def test_map_declares_non_navigation_limits(self) -> None:
        notes = [
            self.config["urban_context"]["walled_core"]["note"],
            self.config["urban_context"]["day_1"]["note"],
            self.config["urban_context"]["day_3"]["note"],
            self.config["regional_days"]["day_2"]["note"],
        ]
        notes.extend(
            choice["note"]
            for choice in self.config["regional_days"]["day_4_choices"]
        )
        joined = " ".join(notes).lower()
        self.assertIn("not turn-by-turn navigation", joined)
        self.assertIn("not walking, metro, road", joined)
        self.assertIn("position only", joined)

    def test_all_pinned_points_fit_declared_extents(self) -> None:
        for group, extent in (
            (
                [
                    *self.config["urban_context"]["day_1"]["sites"],
                    *self.config["urban_context"]["day_3"]["sites"],
                    self.config["urban_context"]["day_3"]["fallback"],
                    self.config["urban_context"]["day_5"],
                ],
                self.config["urban_extent"],
            ),
            (
                [
                    self.config["regional_days"]["city_base"],
                    self.config["regional_days"]["day_2"],
                    *self.config["regional_days"]["day_4_choices"],
                ],
                self.config["regional_extent"],
            ),
        ):
            west, south, east, north = extent
            for item in group:
                longitude, latitude = item["position"]
                self.assertLess(west, longitude)
                self.assertLess(longitude, east)
                self.assertLess(south, latitude)
                self.assertLess(latitude, north)


if __name__ == "__main__":
    unittest.main()
