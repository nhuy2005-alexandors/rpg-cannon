"""More integrity regressions found by pre-merge adversarial review."""
import unittest
from story.combat_mechanics import check_skill_availability
from story.turn_ledger import stage_turn, accept_turn
from verification import test_turn_ledger as ledger_fixture

class ExtraIntegrity(unittest.TestCase):
 def test_structured_known_sta_is_supported(self):
  st={'resources':{'STA':{'current':41,'max':110}},'cooldowns':{'dash':{'ready_at_combat_turn':12,'source_ref':'event:T345'}},'status_effects':{}}
  ctx={'known_skill':True,'costs':{'STA':15},'evidence_refs':['event:T345'],'verified_evidence_refs':['event:T345']}
  self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'READY')

 def test_positive_souls_without_source_receipt_denied(self):
  t=ledger_fixture.LedgerTests()
  with self.assertRaises(ValueError):stage_turn(t.s(),t.i(),{'resource_changes':{'souls':100}},[])

 def test_positive_souls_with_source_receipt_allowed_once(self):
  t=ledger_fixture.LedgerTests()
  receipt={'receipt_id':'corpse:a', 'kind':'RESOURCE_GRANT','resource':'souls','amount':14,'source_ref':'event:T346','action_id':'T346/A01'}
  inp=t.i(); state=t.s();state['verified_grants']={receipt['receipt_id']:dict(receipt)}
  r=stage_turn(state,inp,{'resource_changes':{'souls':14}},[receipt])
  accepted=accept_turn(r,{'confirmed':True,'action_id':'T346/A01','disposition':'SUCCESS','observed_outcome':'looted','verification_refs':['event:T346']})
  self.assertEqual(accepted['post_state']['resources']['souls'],127)
  st=accepted['post_state']
  next_intent={'turn':347, 'action_id':'T347/A01','evidence_refs':['event:T347'],'rule_version':'HN-V1.3'}
  new_receipt={**receipt,'action_id':'T347/A01'}
  with self.assertRaises(ValueError):stage_turn(st,next_intent,{'resource_changes':{'souls':14}},[new_receipt])
