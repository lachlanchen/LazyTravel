from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_inside_wall_route_map import (  # noqa: E402
    iter_lines,
    route_length_km,
)


class XianInsideWallRouteMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-inside-wall-route.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_numbered_sites_are_complete_and_ordered(self) -> None:
        self.assertEqual(
            [site["order"] for site in self.config["sites"]],
            list(range(1, 7)),
        )
        self.assertEqual(len({site["id"] for site in self.config["sites"]}), 6)

    def test_core_and_optional_routes_have_walking_scale_lengths(self) -> None:
        lengths = {
            route["id"]: route_length_km(route["coordinates"])
            for route in self.config["routes"]
        }
        self.assertGreater(lengths["core-route"], 1.5)
        self.assertLess(lengths["core-route"], 2.5)
        self.assertLess(lengths["shuyuanmen-detour"], 0.5)
        self.assertLess(lengths["hui-lanes-detour"], 1.2)

    def test_multilinestring_iterator_preserves_each_line(self) -> None:
        geometry = {
            "type": "MultiLineString",
            "coordinates": [
                [[0.0, 0.0], [1.0, 1.0]],
                [[2.0, 2.0], [3.0, 3.0]],
            ],
        }
        self.assertEqual(len(list(iter_lines(geometry))), 2)


if __name__ == "__main__":
    unittest.main()
