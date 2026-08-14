from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_written_word_route_map import (  # noqa: E402
    haversine_km,
    iter_lines,
    ordered_sites,
)


class XianWrittenWordRouteMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads(
            (ROOT / "data/maps/xian/xian-written-word-route.config.json").read_text(
                encoding="utf-8"
            )
        )

    def test_route_uses_all_three_sites_in_declared_order(self) -> None:
        self.assertEqual(
            [site["id"] for site in ordered_sites(self.config)],
            [
                "big-wild-goose-pagoda",
                "small-wild-goose-pagoda",
                "beilin-museum",
            ],
        )

    def test_schematic_joins_have_plausible_city_scale(self) -> None:
        sites = ordered_sites(self.config)
        distance = sum(
            haversine_km(first["position"], second["position"])
            for first, second in zip(sites, sites[1:])
        )
        self.assertGreater(distance, 4.0)
        self.assertLess(distance, 6.0)

    def test_polygon_iterator_preserves_outer_and_inner_rings(self) -> None:
        geometry = {
            "type": "Polygon",
            "coordinates": [
                [[0.0, 0.0], [1.0, 0.0], [0.0, 0.0]],
                [[0.2, 0.2], [0.3, 0.2], [0.2, 0.2]],
            ],
        }
        self.assertEqual(len(list(iter_lines(geometry))), 2)


if __name__ == "__main__":
    unittest.main()
