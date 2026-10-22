"""Focused regression tests for the public reusable maps, no network/dependencies."""
import copy
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'maps'))
from render import render_map  # noqa: E402


ATLAS = {"schema": "HN-MAP-ATLAS-V1", "maps": [
    {"id": "shed", "name": "Nhà sắt & dấu xích", "revision": 1, "objects": [
        {"id": "room", "label": "Nội thất", "type": "room", "x": 50, "y": 50, "w": 80, "h": 70},
        {"id": "ring", "label": "Vòng sắt", "type": "clue", "x": 24, "y": 24},
        {"id": "road", "label": "Lối đi", "type": "path", "points": [[5, 40], [25, 50]]},
    ]}
]}
SCENE = {"schema": "HN-MAP-SCENE-V1", "map_id": "shed", "last_completed_turn": 204,
         "next_turn": 205, "current": {"tokens": [
             {"id": "vo-danh", "label": "V", "category": "player", "status": "ALIVE", "x": 75, "y": 47, "facing": "ENE"}],
             "movement": [{"entity_id": "vo-danh", "from": [33, 34], "to": [75, 47]}]}}


class TestSVGAtlas(unittest.TestCase):
    def test_valid_svg_stable_and_does_not_mutate_inputs(self):
        a, s = copy.deepcopy(ATLAS), copy.deepcopy(SCENE)
        svg = render_map(a, s, 'shed')
        self.assertEqual(render_map(a, s, 'shed'), svg)
        self.assertEqual((a, s), (ATLAS, SCENE))
        self.assertTrue(ET.fromstring(svg).tag.endswith('svg'))
        self.assertIn('data-object-id="ring"', svg)
        self.assertIn('data-token-id="vo-danh"', svg)
        self.assertIn('marker-end="url(#facingArrow)"', svg)
        self.assertIn('marker-end="url(#routeArrow)"', svg)
        self.assertIn('Cuối T204', svg)

    def test_moving_only_updates_token_overlay(self):
        original = render_map(ATLAS, SCENE, 'shed')
        new = copy.deepcopy(SCENE)
        new['current']['tokens'][0].update(x=12, y=55, facing='W')
        new['current']['movement'][0]['to'] = [12, 55]
        newer = render_map(ATLAS, new, 'shed')
        self.assertNotEqual(original, newer)
        for key in ('data-object-id="room"', 'data-object-id="ring"', 'data-object-id="road"'):
            self.assertIn(key, newer)
        self.assertEqual(ATLAS['maps'][0]['objects'][1]['x'], 24)

    def test_base_map_never_discloses_tokens(self):
        svg = render_map(ATLAS, None, 'shed')
        self.assertNotIn('data-token-id', svg)
        self.assertIn('data-object-id="ring"', svg)

    def test_rejects_wrong_map_and_unknown_data(self):
        with self.assertRaisesRegex(ValueError, 'Map ID missing'):
            render_map(ATLAS, SCENE, 'nonexistent')

    def test_bad_scene_map_rejected(self):
        s = copy.deepcopy(SCENE)
        s['map_id'] = 'elsewhere'
        with self.assertRaisesRegex(ValueError, 'Scene must match'):
            render_map(ATLAS, s, 'shed')

    def test_bad_coordinate_and_facing_rejected(self):
        s = copy.deepcopy(SCENE)
        s['current']['tokens'][0]['x'] = 102
        with self.assertRaises(ValueError):
            render_map(ATLAS, s, 'shed')
        s['current']['tokens'][0]['x'] = 12
        s['current']['tokens'][0]['facing'] = 'NNE'
        with self.assertRaises(ValueError):
            render_map(ATLAS, s, 'shed')

    def test_escaping_prevents_svg_injection(self):
        a = copy.deepcopy(ATLAS)
        a['maps'][0]['objects'][1]['label'] = 'Vòng & móng <sắt>'
        svg = render_map(a, SCENE, 'shed')
        self.assertNotIn('Vòng & móng <sắt>', svg)
        self.assertIn('Vòng &amp; móng &lt;sắt&gt;', svg)
        ET.fromstring(svg)

    def test_repository_fixtures_render_all_three_maps(self):
        root = Path(__file__).resolve().parents[1] / 'maps'
        atlas = json.loads((root / 'atlas-v1.json').read_text(encoding='utf-8'))
        scene = json.loads((root / 'active-scene.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(atlas['maps']), 21)
        for area in atlas['maps']:
            svg = render_map(atlas, None, area['id'])
            self.assertTrue(ET.fromstring(svg).tag.endswith('svg'))
        current = render_map(atlas, scene, scene['map_id'])
        self.assertIn('data-token-id="vo-danh"', current)
        self.assertIn(f"Cuối T{scene['last_completed_turn']}", current)

    def test_text_only_movement_does_not_invent_coordinates(self):
        sample = copy.deepcopy(SCENE)
        sample['current']['movement'] = [{'actor':'vo-danh', 'turn':204,
                                          'description':'Moved using real cover, no measured endpoints'}]
        svg = render_map(ATLAS, sample, 'shed')
        self.assertNotIn('data-entity-id="vo-danh"', svg)
        self.assertIn('data-token-id="vo-danh"', svg)
        ET.fromstring(svg)

    def test_duplicate_objects_fail_closed(self):
        a = copy.deepcopy(ATLAS)
        a['maps'][0]['objects'].append(copy.deepcopy(a['maps'][0]['objects'][0]))
        with self.assertRaisesRegex(ValueError, 'unique'):
            render_map(a, SCENE, 'shed')


if __name__ == '__main__':
    unittest.main()
