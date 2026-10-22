"""Compaction invariants: lossless round trip, archive fail-closed, no gameplay advances."""
import copy
import unittest
from state.compaction import split_state, restore_state, split_scene, restore_scene


class CompactionTests(unittest.TestCase):
    def setUp(self):
        self.state = {'snapshot_version': 'sample', 'last_completed_turn': 345, 'next_turn': 346,
            'player': {'level': 6, 'resources': {'HP': {'current': 117, 'max': 170}, 'souls': 113}},
            'inventory': {'two_bundles_stash': 1},
            'receipts': {'T153': {'paid': True}, 'T345': {'evidence': 'ok'}},
            'world_flags': {'tam_trao_tripwire': 'BYPASSED_NOT_DISARMED',
                'kharzug_distinct_from_dead_wolf': True, 'west_road_T274_T283': {'caravan': 'old'},
                'ba_vach_northern_checkpoint_T345': {'escort': 'wounded'}},
            'battle_state_T194': {'enemy': 'C'}, 'scene_state_T312': {'gate': 'barred'},
            'scene_state_T345': {'escort': 73}, 'checkpoint': {'last_completed_turn': 345}}
        self.scene = {'schema': 'HN-MAP-SCENE-V1', 'last_completed_turn': 345, 'next_turn': 346,
            'map_id': 'bend', 'current': {'tokens': [{'id': 'vo-danh', 'x': 55, 'y': 77}]},
            'archived_current_T273': {'old_x': 4}, 'legacy_timeline': {'old': 3}}

    def test_state_round_trip_no_mutation(self):
        original = copy.deepcopy(self.state)
        hot, cold = split_state(self.state)
        self.assertEqual(self.state, original)
        self.assertNotIn('battle_state_T194', hot)
        self.assertNotIn('T153', hot['receipts'])
        self.assertNotIn('west_road_T274_T283', hot['world_flags'])
        self.assertEqual(hot['world_flags']['tam_trao_tripwire'], 'BYPASSED_NOT_DISARMED')
        self.assertEqual(hot['scene_state_T345'], {'escort': 73})
        self.assertEqual(restore_state(hot, cold), original)

    def test_missing_wrong_or_colliding_archive_fails(self):
        hot, cold = split_state(self.state)
        with self.assertRaises(ValueError): restore_state(hot, None)
        wrong = copy.deepcopy(cold)
        wrong['turn'] = 344
        with self.assertRaises(ValueError): restore_state(hot, wrong)
        hot['battle_state_T194'] = {'evil': True}
        with self.assertRaises(ValueError): restore_state(hot, cold)

    def test_new_receipts_survive_restore(self):
        hot, cold = split_state(self.state)
        hot['receipts']['T346'] = {'new': True}
        restored = restore_state(hot, cold)
        self.assertTrue(restored['receipts']['T153']['paid'])
        self.assertTrue(restored['receipts']['T346']['new'])

    def test_old_archive_remains_readable_after_T346(self):
        hot, cold = split_state(self.state)
        hot['last_completed_turn'] = 346
        hot['next_turn'] = 347
        hot['receipts']['T346'] = {'new': True}
        restored = restore_state(hot, cold)
        self.assertEqual(restored['last_completed_turn'], 346)
        self.assertTrue(restored['receipts']['T153']['paid'])
        self.assertTrue(restored['receipts']['T346']['new'])
        mhot, mcold = split_scene(self.scene)
        mhot['last_completed_turn'] = 346
        mhot['next_turn'] = 347
        self.assertEqual(restore_scene(mhot, mcold)['last_completed_turn'], 346)

    def test_scene_round_trip(self):
        original = copy.deepcopy(self.scene)
        hot, cold = split_scene(self.scene)
        self.assertNotIn('archived_current_T273', hot)
        self.assertNotIn('legacy_timeline', hot)
        self.assertEqual(restore_scene(hot, cold), original)
        self.assertEqual(hot['current']['tokens'][0]['x'], 55)

    def test_reject_nonsequential_turn_and_wrong_scene_ref(self):
        bad = copy.deepcopy(self.state)
        bad['next_turn'] = 348
        with self.assertRaises(ValueError): split_state(bad)
        hot, cold = split_scene(self.scene)
        cold['turn'] = 344
        with self.assertRaises(ValueError): restore_scene(hot, cold)


if __name__ == '__main__': unittest.main()
