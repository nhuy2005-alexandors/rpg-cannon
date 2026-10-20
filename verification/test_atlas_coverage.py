"""Evidence and regression gates for persistent Hac Nhat atlas expansion."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRADES = {"LAYOUT_CONFIRMED", "SCHEMATIC", "PLACEHOLDER", "UNVERIFIED"}
LEGACY = {"hac-nha-east-approach", "bai-sat-ri", "nha-sat-dong-bac"}


class TestAtlasCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coverage = json.loads((ROOT / "maps/coverage.json").read_text(encoding="utf-8"))
        cls.areas = {item["id"]: item for item in cls.coverage["areas"]}
        cls.atlas = json.loads((ROOT / "maps/atlas-v1.json").read_text(encoding="utf-8"))
        cls.maps = {item["id"]: item for item in cls.atlas["maps"]}

    def test_unique_area_ids_and_existing_sources(self):
        self.assertEqual(self.coverage["schema"], "HN-MAP-COVERAGE-V1")
        self.assertEqual(len(self.areas), len(self.coverage["areas"]))
        for item in self.coverage["areas"]:
            self.assertIn(item["grade"], GRADES)
            self.assertTrue(item["sources"], item["id"])
            for path in item["sources"]:
                self.assertTrue((ROOT / path).is_file(), (item["id"], path))
            self.assertNotIn("x", item)
            self.assertNotIn("y", item)
            if item["map_id"] is not None:
                self.assertIn(item["map_id"], self.maps)

    def test_tram_gac_unknown_and_distinct(self):
        self.assertIsNone(self.areas["tram-gac-so-bon"]["map_id"])
        self.assertNotEqual(self.areas["tram-gac-so-bon"]["id"], self.areas["tram-tam-trao"]["id"])

    def test_unknowns_unplaced(self):
        for key in ("western-bandit-hideout", "deep-cave-unknown", "coffin-interiors-unknown"):
            self.assertIsNone(self.areas[key]["map_id"])

    def test_known_three_maps_retained(self):
        self.assertTrue(LEGACY.issubset(self.maps))
        self.assertTrue(LEGACY.issubset(self.areas))


if __name__ == "__main__":
    unittest.main()
