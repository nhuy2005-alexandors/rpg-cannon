"""Three-tier public map hierarchy: no invented locations or game changes."""
import copy
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "maps"))
from render import render_map


class TestHierarchy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads((ROOT/"maps/atlas-v1.json").read_text(encoding="utf-8"))
        cls.cov = json.loads((ROOT/"maps/coverage.json").read_text(encoding="utf-8"))
        cls.maps = {m["id"]: m for m in cls.atlas["maps"]}
        cls.areas = {a["id"]: a for a in cls.cov["areas"]}

    def test_two_levels_added_and_linked(self):
        world = self.maps["hac-nhat-world"]
        region = self.maps["vung-hac-nha"]
        self.assertEqual(world["level"], "WORLD")
        self.assertEqual(region["level"], "REGION")
        self.assertEqual(region["parent_map_id"], "hac-nhat-world")
        self.assertIn("vung-hac-nha", [p["map_id"] for p in world["links"]])
        for target in ("hac-nha-thanh-hub", "bai-sat-ri", "duong-tay-van-tai"):
            self.assertIn(target, [p["map_id"] for p in region["links"]])

    def test_world_contains_only_known_region(self):
        world = self.maps["hac-nhat-world"]
        self.assertEqual([o["id"] for o in world["objects"]], ["vung-hac-nha-marker"])
        self.assertEqual(world["evidence_level"], "SCHEMATIC")

    def test_regional_positions_and_unknown_locations(self):
        region = self.maps["vung-hac-nha"]
        pins = {o["id"]: o for o in region["objects"] if o["type"] != "path"}
        self.assertLess(pins["doc-da-xam"]["x"], pins["duong-gac-tay"]["x"])
        self.assertLess(pins["duong-gac-tay"]["x"], pins["hac-nha-thanh"]["x"])
        self.assertLess(pins["hac-nha-thanh"]["x"], pins["bai-sat-ri"]["x"])
        self.assertLess(pins["nha-sat-dong-bac"]["y"], pins["bai-sat-ri"]["y"])
        for label in ("Suối Cạn", "Nghĩa Địa Tử Thiết", "Rừng Xương",
                      "Huyết Cốt Động", "Cấm Lao", "Kho Quân Vụ Đông"):
            self.assertTrue(any(label in s for s in region["unplaced_known_names"]), label)
        self.assertFalse({"cam-lao", "kho-quan-vu-dong", "western-bandit-hideout"}
                         & set(pins))

    def test_registry_indexes_both_without_coordinates(self):
        for key in ("hac-nhat-world", "vung-hac-nha"):
            item = self.areas[key]
            self.assertEqual(item["grade"], "SCHEMATIC")
            self.assertEqual(item["map_id"], key)
            self.assertTrue(item["sources"])
            self.assertNotIn("x", item)
            self.assertNotIn("y", item)

    def test_svg_outputs_are_valid_and_idempotent(self):
        for key in ("hac-nhat-world", "vung-hac-nha"):
            svg = render_map(self.atlas, None, key)
            self.assertTrue(ET.fromstring(svg).tag.endswith("svg"))
            self.assertEqual(svg, render_map(copy.deepcopy(self.atlas), None, key))
            self.assertNotIn("data-token-id=", svg)

    def test_unknown_names_are_visible_without_map_pins(self):
        svg = render_map(self.atlas, None, "vung-hac-nha")
        self.assertIn("data-unplaced-name=", svg)
        self.assertIn("CHƯA ĐỊNH VỊ", svg)
        for word in ("Nghĩa Địa Tử Thiết", "Rừng Xương", "Suối Cạn"):
            self.assertIn(word, svg)
        self.assertNotIn('data-object-id="nghia-dia-tu-thiet"', svg)

    def test_unknown_legend_overflow_fails_readably(self):
        altered = copy.deepcopy(self.atlas)
        region = next(m for m in altered["maps"] if m["id"] == "vung-hac-nha")
        region["unplaced_known_names"] *= 4
        with self.assertRaisesRegex(ValueError, "split"):
            render_map(altered, None, "vung-hac-nha")

    def test_active_game_remains_t204(self):
        game = json.loads((ROOT/"state/current.json").read_text(encoding="utf-8"))
        scene = json.loads((ROOT/"maps/active-scene.json").read_text(encoding="utf-8"))
        self.assertEqual((game["last_completed_turn"], game["next_turn"]), (345, 346))
        self.assertEqual((scene["last_completed_turn"], scene["next_turn"]), (345, 346))
        self.assertEqual(scene["map_id"], "doc-da-xam-ba-vach-escort-second-bend")


if __name__ == "__main__":
    unittest.main()
