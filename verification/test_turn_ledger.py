import copy
import unittest
from story.turn_ledger import stage_turn,accept_turn

def state():
    return {'last_completed_turn':345,'next_turn':346,
            'resources':{'HP':{'current':117,'max':170},'STA':{'current':41,'max':110},'BLOOD':{'current':46,'max':50},'TuHuyet':{'current':0,'max':20},'souls':113,'exp':380},
            'inventory_counts':{'test-arrow':2,'Maela-arrows':'UNKNOWN'},'cooldowns':{},'status_effects':{},'accepted_actions':{},'claims':{}}

def intent(**kw):
    x={'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['noncanon/event']};x.update(kw);return x

def deltas(**kw):
    x={'resource_changes':{'STA':-5},'inventory_changes':{},'cooldown_changes':{},'status_changes':{},'elapsed_minutes':1};x.update(kw);return x

def accept(s,d=None,i=None,receipts=None):
    return accept_turn(stage_turn(s,i or intent(),d or deltas(),receipts if receipts is not None else []),
                       {'confirmed':True,'action_id':(i or intent())['action_id'],'disposition':'PARTIAL','observed_outcome':'noncanon verified','verification_refs':['noncanon/event']})

class LedgerTests(unittest.TestCase):
    def test_stage_checks_caps_and_does_not_mutate(self):
        s=state();copy_s=copy.deepcopy(s)
        staged=stage_turn(s,intent(),deltas(),[])
        self.assertEqual(s,copy_s)
        self.assertEqual(staged['projected_post_state']['resources']['STA']['current'],36)
        for change in ({'HP':-118},{'BLOOD':6},{'TuHuyet':21},{'souls':-114},{'exp':-381},{'STA':True}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                stage_turn(s,intent(),deltas(resource_changes=change),[])

    def test_unknown_ammo_fails_closed(self):
        with self.assertRaises(ValueError):stage_turn(state(),intent(),deltas(inventory_changes={'Maela-arrows':-1}),[])

    def test_one_completed_turn_even_with_multiple_substeps(self):
        s=state();it=intent(substeps=['pursue','aim','shoot'])
        result=accept(s,i=it)
        self.assertEqual(result['post_state']['last_completed_turn'],346)
        self.assertEqual(result['post_state']['next_turn'],347)
        self.assertEqual(result['compact_delta']['action_id'],'T346/A01')
        self.assertEqual(s['next_turn'],346)

    def test_unconfirmed_or_wrong_action_id_rejected(self):
        staged=stage_turn(state(),intent(),deltas(),[])
        for confirmation in ({'confirmed':False,'action_id':'T346/A01'}, {'confirmed':True,'action_id':'T346/A02'}):
            with self.assertRaises(ValueError):accept_turn(staged, confirmation)

    def test_idempotent_replay_uses_saved_receipt_and_prestate(self):
        s=state();r=accept(s)
        after=r['post_state']
        staged=stage_turn(after,intent(),deltas(),[])
        self.assertEqual(staged['status'],'REPLAY')
        r2=accept_turn(staged,{'confirmed':True,'action_id':'T346/A01','disposition':'PARTIAL','observed_outcome':'noncanon verified','verification_refs':['noncanon/event']})
        self.assertEqual(r2,r)
        with self.assertRaises(ValueError):stage_turn(after,intent(),deltas(resource_changes={'STA':-9}),[])
        modified=copy.deepcopy(after);modified['resources']['STA']['current']=1
        with self.assertRaises(ValueError):stage_turn(modified,intent(),deltas(),[])

    def test_no_duplicate_unique_claim(self):
        s=state();s['claims']={'corpse:1':{'claim_action':'T345/A01'}}
        with self.assertRaises(ValueError):stage_turn(s,intent(),deltas(unique_claim_ids=['corpse:1']),[{'id':'loot1','source_ref':'noncanon/event'}])
        with self.assertRaises(ValueError):stage_turn(state(),intent(),deltas(resource_changes={'souls':14},unique_claim_ids=['corpse:2']),[])

    def test_status_and_cooldown_require_evidence(self):
        for bad in [deltas(cooldown_changes={'dash':{'ready_at_combat_turn':12}}),
                    deltas(status_changes={'bleed':{'active':True,'expiration':'3 turns'}})]:
            with self.subTest(bad=bad),self.assertRaises(ValueError):stage_turn(state(),intent(),bad,[])
        ok=deltas(cooldown_changes={'dash':{'ready_at_combat_turn':12,'source_ref':'noncanon/skill'}},
                   status_changes={'bleed':{'active':True,'expiration':'until-rest-approved','source_ref':'noncanon/event'}})
        self.assertIn('dash',accept(state(),d=ok)['post_state']['cooldowns'])

    def test_reusing_receipt_id_across_accepted_actions_is_rejected(self):
        first = accept(state(), receipts=[{'id':'effect:melee-hit-1','source_ref':'noncanon/event'}])
        post = first['post_state']
        new_intent = intent(turn=347, action_id='T347/A01')
        with self.assertRaises(ValueError):
            stage_turn(post, new_intent, deltas(), [{'id':'effect:melee-hit-1','source_ref':'noncanon/event'}])

    def test_replay_cannot_change_verification_references(self):
        original = accept(state())
        replay = stage_turn(original['post_state'],intent(),deltas(),[])
        with self.assertRaises(ValueError):
            accept_turn(replay,{'confirmed':True,'action_id':'T346/A01','disposition':'PARTIAL',
                  'observed_outcome':'noncanon verified','verification_refs':['evil/unverified']})

    def test_unknown_hot_archive_does_not_authorize_duplicate_loot(self):
        s=state();s['historical_claim_coverage']='ARCHIVED_UNVERIFIED'
        with self.assertRaises(ValueError):
            stage_turn(s,intent(),deltas(resource_changes={'souls':12},unique_claim_ids=['corpse:old']),[{'id':'claim','source_ref':'noncanon/old'}])

if __name__=='__main__': unittest.main()
