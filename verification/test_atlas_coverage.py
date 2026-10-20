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
            # During Task 1, future map IDs are forward references resolved by Tasks 2/3.

    def test_city_and_western_road_maps(self):
        ids = {"hac-nha-thanh-hub", "dien-te-huyet", "lo-ren-hac-nha",
               "garrick-bang-nhiem-vu", "duong-gac-tay",
               "duong-tay-van-tai", "doc-da-xam", "suoi-can"}
        self.assertTrue(ids.issubset(self.maps))
        for key in ids:
            self.assertEqual(self.maps[key]["evidence_level"], "SCHEMATIC")
            self.assertTrue(self.maps[key]["evidence_sources"])
        self.assertFalse(any("bandit hideout" in str(obj).lower()
                             for key in ids for obj in self.maps[key]["objects"]))

    def test_old_static_map_unchanged(self):
        before = {"hac-nha-east-approach": {"hac-nha-thanh": (18,45), "east-shed": (87,23)},
                  "bai-sat-ri": {"western-ore-wagon": (19,52), "northeast-ruined-shed": (81,23)},
                  "nha-sat-dong-bac": {"northwest-ring": (24,24), "moved-board": (70,51)}}
        for key, objects in before.items():
            by = {o["id"]: o for o in self.maps[key]["objects"]}
            for oid, pos in objects.items():
                self.assertEqual((by[oid]["x"], by[oid]["y"]), pos)

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
