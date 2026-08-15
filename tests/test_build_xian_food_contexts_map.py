from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_food_contexts_map import wall_ring  # noqa: E402


class XianFoodContextsMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-food-contexts.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_four_contexts_are_complete_and_ordered(self) -> None:
        contexts = self.config["contexts"]
        self.assertEqual([context["order"] for context in contexts], [1, 2, 3, 4])
        self.assertEqual(len({context["id"] for context in contexts}), 4)

    def test_context_centres_fit_the_declared_extent(self) -> None:
        west, south, east, north = self.config["extent"]
        for context in self.config["contexts"]:
            longitude, latitude = context["position"]
            self.assertLess(west, longitude)
            self.assertLess(longitude, east)
            self.assertLess(south, latitude)
            self.assertLess(latitude, north)

    def test_contexts_are_areas_not_restaurant_pins(self) -> None:
        for context in self.config["contexts"]:
            self.assertGreater(context["radius"], 0.002)
            self.assertNotIn("restaurant", context)
            self.assertNotIn("price", context)
            self.assertNotIn("hours", context)

    def test_present_wall_polygon_is_available(self) -> None:
        wall_geojson = json.loads(
            (ROOT / "data/maps/xian/xian-before-walls.geojson").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreater(len(wall_ring(wall_geojson)), 10)


if __name__ == "__main__":
    unittest.main()
