"""Regression for merge-blocking findings reproduced during review."""
import copy
import unittest
from story.turn_ledger import stage_turn, accept_turn
from story.combat_mechanics import check_skill_availability
from story.tactical_checks import check_tactical
from verification import test_turn_ledger as ledger_fixture

class MergeBlockerRegression(unittest.TestCase):
 def test_replay_after_modified_hp_is_rejected(self):
  t=ledger_fixture.LedgerTests();first=stage_turn(t.s(),t.i(),{'resource_changes':{'STA':-15}},[])
  result=accept_turn(first,{'confirmed':True,'action_id':'T346/A01','disposition':'PARTIAL', 'observed_outcome':'ran','verification_refs':['synthetic']})
  changed=copy.deepcopy(result['post_state']);changed['resources']['HP']['current']=1
  with self.assertRaises(ValueError):stage_turn(changed,t.i(),{'resource_changes':{'STA':-15}},[])

 def test_stunned_skill_cannot_be_ready(self):
  st={'resources':{'STA':41},'cooldowns':{'dash':{'ready_at_combat_turn':12,'source_ref':'event:T345'}},'status_effects':{'stun':{'source_ref':'event:T345','expires_when':'cured','blocks_skills':True}}}
  ctx={'known_skill':True,'costs':{'STA':15},'evidence_refs':['event:T345']}
  result=check_skill_availability('dash',st,{'combat_turn':12},ctx)
  self.assertEqual(result['status'],'BLOCKED')

 def test_unknown_ally_ammo_does_not_allow_shot(self):
  facts={'evidence_refs':['T345'], 'actor_ready':'ready','target_visibility':'visible','los':'clear','crossfire':'clear'}
  r=check_tactical({'substeps':[{'id':'s','actor':'Maela','verb':'shoot','target':'A'}]}, {'substeps':{'s':facts}})
  self.assertEqual(r['substeps'][0]['disposition'],'UNKNOWN')

 def test_confirmed_ammo_allows_attempt_not_hit(self):
  facts={'evidence_refs':['T345'], 'actor_ready':'ready','target_visibility':'visible','los':'clear','crossfire':'clear','ammo':'available'}
  r=check_tactical({'substeps':[{'id':'s','actor':'Maela','verb':'shoot','target':'A'}]}, {'substeps':{'s':facts}})
  self.assertEqual(r['substeps'][0]['disposition'],'ALLOWED')
  self.assertNotIn('hit',r['substeps'][0])
