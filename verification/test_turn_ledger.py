import unittest
from story.turn_ledger import stage_turn,accept_turn

class LedgerTests(unittest.TestCase):
 def s(self): return {'last_completed_turn':345,'next_turn':346,'resources':{'HP':{'current':117,'max':170},'STA':{'current':41,'max':110},'BLOOD':{'current':46,'max':50},'TuHuyet':{'current':0,'max':20},'souls':113,'exp':380},'inventory_counts':{'arrow':2},'cooldowns':{},'status_effects':{},'accepted_actions':{}}
 def i(self):return {'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['synthetic']}
 def test_resource_cap_and_pure(self):
  pre=self.s();o=stage_turn(pre,self.i(),{'resource_changes':{'STA':-15},'inventory_changes':{'arrow':-1},'elapsed_minutes':1},[])
  self.assertEqual(pre['resources']['STA']['current'],41);self.assertEqual(o['projected_post_state']['resources']['STA']['current'],26)
  with self.assertRaises(ValueError):stage_turn(pre,self.i(),{'resource_changes':{'BLOOD':7}},[])
  with self.assertRaises(ValueError):stage_turn(pre,self.i(),{'inventory_changes':{'missing':-1}},[])
 def test_confirm_idempotent_and_conflict(self):
  pre=self.s();a=stage_turn(pre,self.i(),{'resource_changes':{'STA':-15}},[])
  result=accept_turn(a,{'confirmed':True,'action_id':'T346/A01','disposition':'PARTIAL','observed_outcome':'ran','verification_refs':['synthetic']})
  again=stage_turn(result['post_state'],self.i(),{'resource_changes':{'STA':-15}},[])
  self.assertEqual(again['status'],'REPLAY');self.assertEqual(again['projected_post_state'],result['post_state'])
  with self.assertRaises(ValueError):stage_turn(result['post_state'],self.i(),{'resource_changes':{'STA':-20}},[])
 def test_turn_boundary(self):
  pre=self.s()
  with self.assertRaises(ValueError):stage_turn(pre,dict(self.i(),turn=347),{},[])
  a=stage_turn(pre,self.i(),{},[])
  with self.assertRaises(ValueError):accept_turn(a,{'confirmed':False,'action_id':'T346/A01'})
 def test_cooldown_and_status_source(self):
  pre=self.s()
  with self.assertRaises(ValueError):stage_turn(pre,self.i(),{'cooldown_changes':{'dash':{'ready_at_combat_turn':3}}},[])
  a=stage_turn(pre,self.i(),{'cooldown_changes':{'dash':{'ready_at_combat_turn':3,'source_ref':'synthetic'}},'status_changes':{'bleed':{'source_ref':'synthetic','expires_when':'healed'}}},[])
  self.assertEqual(a['projected_post_state']['cooldowns']['dash']['ready_at_combat_turn'],3)
