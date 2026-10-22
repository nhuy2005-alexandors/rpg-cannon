"""Actual algorithmic execution of 36 NON-CANONICAL inputs, not GM text evaluation."""
import json
import unittest
from pathlib import Path
from story.combat_mechanics import resolve_damage, check_skill_availability
from story.tactical_checks import check_tactical
from story.turn_ledger import stage_turn

PATH=Path(__file__).parent/'gm_reliability_scenarios.json'

class ScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text())

    def test_distinct_groups_and_provenance(self):
        cases=self.data['cases']
        self.assertEqual(self.data['scope'],'NON_CANONICAL_SYNTHETIC_ONLY')
        self.assertEqual(len(cases),36)
        self.assertEqual(sorted(set(x['group'] for x in cases)),['combat','ledger','tactical'])
        self.assertEqual([sum(x['group']==k for x in cases) for k in ['combat','tactical','ledger']],[12,12,12])
        self.assertEqual(len(set(x['id'] for x in cases)),36)
        for x in cases:
            self.assertTrue(x['source_ref'])
            self.assertIn('expected',x)
            self.assertIn('forbidden',x)
            self.assertNotEqual(x['expected'],x['forbidden'])

    def test_execute_all_programmatic_predicates(self):
        for case in self.data['cases']:
            with self.subTest(id=case['id']):
                obj=case['input'];method=case['method']
                if method=='damage':
                    out=resolve_damage(obj['attack'],obj['defender'],obj['effects'])
                    actual=out[case['assert_key']]
                elif method=='availability':
                    out=check_skill_availability(obj['skill_id'],obj['pre_state'],obj['clock'],obj['action_context'])
                    actual=out['status']
                elif method=='tactical':
                    out=check_tactical(obj['intent'],obj['observed_world'])
                    actual=out['substeps'][0]['disposition']
                elif method=='ledger_valid':
                    try:
                        out=stage_turn(obj['pre_state'],obj['intended_turn'],obj['proposed_deltas'],obj['receipts'])
                        actual=out['status']
                    except ValueError as error:
                        actual='REJECTED'
                        self.assertIn(case['expected_error'],str(error))
                else: self.fail('unknown method '+method)
                self.assertEqual(actual,case['expected'])
                self.assertNotEqual(actual,case['forbidden'])

if __name__=='__main__':unittest.main()
