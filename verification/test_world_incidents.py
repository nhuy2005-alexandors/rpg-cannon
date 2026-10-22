import copy
import unittest
from story.world_incidents import evaluate_world_opportunity, resolve_contest, PROFILES

SEED = 'public-test-seed'

def kwargs(**extra):
    d = dict(seed=SEED, opportunity_id='T346/road/segment-a', turn=346,
             kind='travel_segment', zone='dangerous', tags={
                'outdoors': 'events/0345.md', 'rocky_path': 'maps/atlas-v1.json',
                'bandit_territory': 'events/0345.md'},
             segment_id='bend-to-north', elapsed_minutes=12)
    d.update(extra)
    return d

class WorldIncidents(unittest.TestCase):
    def test_profile_totals_and_types(self):
        self.assertEqual(sum(PROFILES['safe'].values()), 10000)
        self.assertEqual(sum(PROFILES['dangerous'].values()), 10000)
        self.assertEqual(PROFILES['safe']['hazard'], 200)
        self.assertEqual(PROFILES['dangerous']['hazard'], 1000)
    def test_repeat_id_idempotent_and_context_tamper_rejected(self):
        ledger = {}
        receipt = evaluate_world_opportunity(ledger, **kwargs())
        self.assertEqual(evaluate_world_opportunity(ledger, **kwargs()), receipt)
        self.assertEqual(len(ledger), 1)
        with self.assertRaises(ValueError):
            evaluate_world_opportunity(ledger, **kwargs(zone='safe'))
    def test_no_tick_per_chat_and_no_unbounded_spam(self):
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(kind='chat_turn'))
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(kind='significant_time', elapsed_minutes=1))
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(kind='equipment_stress'))
    def test_evidence_tags_mandatory_and_no_hidden_rewards(self):
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(tags={'outdoors': ''}))
        state = {'HP': 117, 'souls': 113, 'copper': 48}
        before = copy.deepcopy(state)
        receipt = evaluate_world_opportunity({}, **kwargs())
        self.assertEqual(state, before)
        self.assertIn(receipt['category'], ('none', 'ambient', 'encounter', 'hazard'))
        self.assertFalse(receipt['auto_claim'])
        self.assertEqual(receipt['turn'], 346)
    def test_duplicate_segment_cannot_be_repeated_under_new_id(self):
        ledger = {}
        evaluate_world_opportunity(ledger, **kwargs())
        with self.assertRaises(ValueError):
            evaluate_world_opportunity(ledger, **kwargs(opportunity_id='T346/road/reroll'))
    def test_invalid_tag_type_fail_closed(self):
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(tags=None))
    def test_item_failure_is_condition_gated(self):
        req = kwargs(kind='equipment_stress', segment_id='loaded-strap',
                     tags={'worn_strap': 'events/0345.md', 'load_bearing': 'events/0345.md'})
        receipt = evaluate_world_opportunity({}, **req)
        if receipt['incident_id'] == 'strap_failure':
            self.assertEqual(receipt['category'], 'hazard')
        with self.assertRaises(ValueError):
            evaluate_world_opportunity({}, **kwargs(kind='equipment_stress', segment_id='strap',
                                                    tags={'outdoors': 'evidence'}))
    def test_unknown_location_and_bad_ids_fail_closed(self):
        for updates in [dict(zone='unknown'), dict(opportunity_id=''), dict(turn=345),
                        dict(segment_id=''), dict(elapsed_minutes=-1)]:
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                evaluate_world_opportunity({}, **kwargs(**updates))
    def test_action_chance_requires_grounded_explicit_rate(self):
        with self.assertRaises(ValueError):
            resolve_contest({}, seed=SEED, action_id='T346/shot1',
                            chance_basis_points=None, evidence='events/test.md')
        ledger = {}
        receipt = resolve_contest(ledger, seed=SEED, action_id='T346/shot1',
                                  chance_basis_points=3700, evidence='events/test.md')
        self.assertEqual(resolve_contest(ledger, seed=SEED, action_id='T346/shot1',
                         chance_basis_points=3700, evidence='events/test.md'), receipt)
        self.assertEqual(receipt['hit'], receipt['roll'] < 3700)
        with self.assertRaises(ValueError):
            resolve_contest(ledger, seed=SEED, action_id='T346/shot1',
                            chance_basis_points=9900, evidence='events/test.md')
    def test_no_pity_and_determinism(self):
        x = evaluate_world_opportunity({}, **kwargs())
        self.assertEqual(x, evaluate_world_opportunity({}, **kwargs()))
        self.assertNotIn('pity', x)
        self.assertTrue(0 <= x['roll'] < 10000)

if __name__ == '__main__':
    unittest.main()
