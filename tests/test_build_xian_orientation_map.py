from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_xian_orientation_map import clipped_geometry, parse_way_xml  # noqa: E402


class XianOrientationMapTests(unittest.TestCase):
    def test_parses_only_requested_osm_way(self) -> None:
        payload = b"""<osm>
          <node id="1" lat="34.0" lon="108.0"/>
          <node id="2" lat="34.1" lon="108.1"/>
          <way id="20"><nd ref="1"/><nd ref="2"/></way>
        </osm>"""
        self.assertEqual(
            parse_way_xml(payload, 20),
            {"type": "LineString", "coordinates": [(108.0, 34.0), (108.1, 34.1)]},
        )

    def test_clips_geometry_to_declared_extent(self) -> None:
        geometry = {
            "type": "LineString",
            "coordinates": [[107.9, 34.0], [108.1, 34.0], [108.3, 34.0]],
        }
        clipped = clipped_geometry(geometry, [108.0, 33.9, 108.2, 34.1])
        self.assertEqual(
            clipped,
            {
                "type": "LineString",
                "coordinates": [[108.0, 34.0], [108.1, 34.0], [108.2, 34.0]],
            },
        )


if __name__ == "__main__":
    unittest.main()
