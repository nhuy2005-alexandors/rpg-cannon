"""Non-canonical checks of the read-only canonical -> ledger projection boundary."""
import copy
import json
import unittest
from pathlib import Path

from story.canonical_adapter import project_canonical_state
from story.turn_ledger import stage_turn

ROOT = Path(__file__).resolve().parents[1]


def snapshot():
    return (json.loads((ROOT / 'state/current.json').read_text(encoding='utf-8')),
            json.loads((ROOT / 'state/archive/T345-state-cold.json').read_text(encoding='utf-8')))


class CanonicalProjectionTests(unittest.TestCase):
    def test_projection_preserves_t345_without_mutation(self):
        hot, cold = snapshot()
        frozen = copy.deepcopy((hot, cold))
        p = project_canonical_state(hot, cold, inventory_keys=['steel_bolts', 'Maela_ArrowStatus_T345'])
        self.assertEqual((hot, cold), frozen)
        self.assertEqual((p['last_completed_turn'], p['next_turn']), (345, 346))
        self.assertEqual(p['resources']['exp'], 380)
        self.assertEqual((p['resources']['HP']['current'], p['resources']['STA']['current'],
                          p['resources']['BLOOD']['current'], p['resources']['souls']), (117, 41, 46, 113))
        self.assertEqual(p['inventory_counts']['steel_bolts'], 2)
        self.assertEqual(p['inventory_counts']['Maela_ArrowStatus_T345'], 'UNKNOWN')
        self.assertEqual(p['historical_receipt_ids'].count('T207'), 1)
        self.assertGreaterEqual(len(p['historical_receipt_ids']), 122)
        self.assertIn('enemy:blackclaw-A', p['historical_claims'])
        self.assertEqual(p['accepted_actions'], {})
        self.assertTrue(p['canonical_history_verified'])

    def test_invalid_cold_pointer_rejected(self):
        hot, cold = snapshot()
        hot['_cold_archive']['turn'] = 344
        with self.assertRaises(ValueError): project_canonical_state(hot, cold, inventory_keys=[])

    def test_future_versioned_archive_pointer_accepted(self):
        hot, cold = snapshot()
        hot['last_completed_turn'] = 356
        hot['next_turn'] = 357
        hot['_cold_archive']['turn'] = 356
        hot['_cold_archive']['path'] = 'state/archive/T356-state-cold.json'
        cold['turn'] = 356
        cold['path'] = 'state/archive/T356-state-cold.json'
        p = project_canonical_state(hot, cold, inventory_keys=[])
        self.assertEqual((p['last_completed_turn'],p['next_turn']),(356,357))

    def test_missing_archive_rejected(self):
        hot, _ = snapshot()
        with self.assertRaises(ValueError): project_canonical_state(hot, None, inventory_keys=[])

    def test_duplicate_historical_corpse_claim_rejected(self):
        hot, cold = snapshot()
        p = project_canonical_state(hot, cold, inventory_keys=[])
        cmd = {'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['synthetic']}
        r = [{'receipt_id':'future-grant', 'kind':'RESOURCE_GRANT','resource':'souls',
              'amount':12,'action_id':'T346/A01','source_ref':'events/synthetic',
              'claim_target_id':'enemy:blackclaw-A','claim_id':'claim:T194:hyena-A:soul-v1.2'}]
        with self.assertRaises(ValueError):
            stage_turn(p,cmd,{'resource_changes':{'souls':12}},r)

    def test_positive_souls_missing_claim_provenance_rejected(self):
        hot, cold = snapshot()
        p = project_canonical_state(hot, cold, inventory_keys=[])
        cmd = {'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['synthetic']}
        r = [{'receipt_id':'future-grant','kind':'RESOURCE_GRANT','resource':'souls',
              'amount':12,'action_id':'T346/A01','source_ref':'events/synthetic'}]
        with self.assertRaises(ValueError):
            stage_turn(p,cmd,{'resource_changes':{'souls':12}},r)

    def test_unclaimed_future_target_is_not_automatically_awarded(self):
        hot, cold = snapshot()
        p = project_canonical_state(hot, cold, inventory_keys=[])
        cmd = {'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['synthetic']}
        r = [{'receipt_id':'future-grant','kind':'RESOURCE_GRANT','resource':'souls','amount':12,
              'action_id':'T346/A01','source_ref':'events/synthetic',
              'claim_target_id':'synthetic-never-looted','claim_id':'synthetic-new-claim'}]
        staged=stage_turn(p,cmd,{'resource_changes':{'souls':12}},r)
        self.assertEqual(staged['status'],'STAGED')
        self.assertEqual(staged['projected_post_state']['resources']['souls'],125)
        self.assertEqual(p['resources']['souls'],113)

class FutureClaimReplayTests(unittest.TestCase):
    def test_claimed_target_cannot_receive_second_distinct_id(self):
        from story.turn_ledger import accept_turn
        hot, cold = snapshot()
        state = project_canonical_state(hot, cold, inventory_keys=[])
        def input_at(turn, key, claim):
            command = {'turn':turn, 'action_id':key, 'rule_version':'HN-V1.3', 'evidence_refs':['synthetic']}
            r = [{'receipt_id':claim+'-receipt', 'kind':'RESOURCE_GRANT','resource':'souls',
                 'amount':12, 'action_id':key, 'source_ref':'synthetic',
                 'claim_target_id':'synthetic-future-target', 'claim_id':claim}]
            return command, r
        intent, rs = input_at(346,'T346/A01','newclaim-1')
        a = stage_turn(state,intent,{'resource_changes':{'souls':12}},rs)
        accepted=accept_turn(a,{'confirmed':True,'action_id':'T346/A01','disposition':'DONE',
                                'observed_outcome':'synthetic','verification_refs':['synthetic']})['post_state']
        intent2, rs2 = input_at(347,'T347/A01','newclaim-2')
        with self.assertRaises(ValueError):
            stage_turn(accepted,intent2,{'resource_changes':{'souls':12}},rs2)
