from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_website import public_projection, reading_counts  # noqa: E402
from verify_deployed_site import (  # noqa: E402
    REQUIRED_FILES,
    safe_manifest_path,
    validate_site_metadata,
)


class DeployedSiteVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = {
            "book": {"edition": "test"},
            "citations": [{"id": "source-a", "path": "/home/private/source.pdf"}],
            "assets": [],
            "chapters": [
                {
                    "id": "chapter-a",
                    "blocks": [
                        {
                            "text": {"zh": "西安", "ja": "西安", "en": "Xi'an"},
                            "readings": {
                                "zh": {"tokens": [{"text": "西安", "reading": "xī'ān"}]},
                                "ja": {"tokens": [{"text": "西安", "reading": "せいあん"}]},
                            },
                        }
                    ],
                }
            ],
        }
        self.digest = "a" * 64
        self.payload = public_projection(self.source)
        self.payload["_build"] = {"source_sha256": self.digest}
        self.manifest = {
            "source_json": {"sha256": self.digest},
            "parity": {"status": "pass", **reading_counts(self.source)},
            "files": {
                path: {"sha256": "b" * 64, "bytes": 1}
                for path in REQUIRED_FILES
            },
        }
        self.index = " ".join(
            (
                'id="chapter-select"',
                'id="section-select"',
                'id="ruby-toggle"',
                'id="chapter-outline"',
                'id="section-outline"',
            )
        )

    def test_matching_public_projection_passes(self) -> None:
        files = validate_site_metadata(
            self.source,
            self.digest,
            self.manifest,
            self.payload,
            self.index,
        )
        self.assertEqual(set(files), REQUIRED_FILES)

    def test_changed_deployed_text_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["chapters"][0]["blocks"][0]["text"]["en"] = "Changed"
        with self.assertRaisesRegex(RuntimeError, "public projection"):
            validate_site_metadata(
                self.source,
                self.digest,
                self.manifest,
                payload,
                self.index,
            )

    def test_parent_manifest_path_is_rejected(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "unsafe deployed path"):
            safe_manifest_path("../private.json")


if __name__ == "__main__":
    unittest.main()
