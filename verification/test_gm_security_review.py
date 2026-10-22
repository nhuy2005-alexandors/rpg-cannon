"""Adversarial review regressions. Synthetic only, no T346 gameplay."""
import unittest,copy,json,hashlib
from pathlib import Path
from story.turn_ledger import stage_turn,accept_turn
from story.canonical_adapter import project_canonical_state
from story.tactical_checks import check_tactical
from story.combat_mechanics import check_skill_availability,resolve_damage
from verification.test_turn_ledger import LedgerTests

ROOT=Path(__file__).parents[1]
def cmd():return {'turn':346,'action_id':'T346/A01','rule_version':'HN-V1.3','evidence_refs':['synthetic']}
def grant():return {'receipt_id':'r1','action_id':'T346/A01','kind':'RESOURCE_GRANT','resource':'souls','amount':12,'source_ref':'accepted:T346','claim_id':'claim1','claim_target_id':'corpse1'}
class SecurityReview(unittest.TestCase):
 def state(self):return LedgerTests().s()
 def test_inventory_mint_without_receipt(self):
  with self.assertRaises(ValueError):stage_turn(self.state(),cmd(),{'inventory_changes':{'arrow':1000}},[])
 def test_souls_forged_receipt(self):
  with self.assertRaises(ValueError):stage_turn(self.state(),cmd(),{'resource_changes':{'souls':12}},[grant()])
 def test_preverified_souls_exact(self):
  s=self.state();r=grant();s['verified_grants']={r['receipt_id']:copy.deepcopy(r)}
  self.assertEqual(stage_turn(s,cmd(),{'resource_changes':{'souls':12}},[r])['projected_post_state']['resources']['souls'],125)
  with self.assertRaises(ValueError):stage_turn(s,cmd(),{'resource_changes':{'souls':11}},[r])
 def test_unsupported_delta(self):
  with self.assertRaises(ValueError):stage_turn(self.state(),cmd(),{'free_gold':999},[])
 def test_receipt_metadata_replay_tamper(self):
  staged=stage_turn(self.state(),cmd(),{'resource_changes':{'STA':-1}},[])
  accepted=accept_turn(staged,{'confirmed':True,'action_id':'T346/A01','disposition':'DONE','observed_outcome':'spent','verification_refs':['synthetic']})['post_state']
  for key,val in [('disposition','FORGED'),('verification_refs',['fake'])]:
   bad=copy.deepcopy(accepted);bad['accepted_actions']['T346/A01'][key]=val
   with self.subTest(key=key),self.assertRaises(ValueError):stage_turn(bad,cmd(),{'resource_changes':{'STA':-1}},[])
 def test_archive_pin_and_tampered_content(self):
  h=json.loads((ROOT/'state/current.json').read_text());raw=(ROOT/'state/archive/T345-state-cold.json').read_bytes();c=json.loads(raw)
  sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  self.assertTrue(project_canonical_state(h,c,inventory_keys=[],cold_bytes=raw,expected_cold_sha=sha)['canonical_history_verified'])
  bad=copy.deepcopy(c);bad['source_state_blob_sha']='bogus'
  with self.assertRaises(ValueError):project_canonical_state(h,bad,inventory_keys=[],cold_bytes=raw,expected_cold_sha=sha)
  with self.assertRaises(ValueError):project_canonical_state(h,c,inventory_keys=[],cold_bytes=raw,expected_cold_sha='0'*40)
 def test_fake_skill_ready(self):
  st={'resources':{'STA':40},'cooldowns':{'dash':{'ready_at_combat_turn':12,'source_ref':'forged'}},'status_effects':{}}
  ctx={'known_skill':True,'costs':{'STA':15},'evidence_refs':['forged']}
  self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'UNKNOWN')
 def test_fake_tactical_shot(self):
  d={'evidence_refs':['forged'],'actor_ready':'ready','target_visibility':'visible','los':'clear','crossfire':'clear','ammo':'available'}
  i={'substeps':[{'id':'a','actor':'Maela','verb':'shoot','target':'A'}]}
  self.assertEqual(check_tactical(i,{'substeps':{'a':d}})['substeps'][0]['disposition'],'UNKNOWN')
 def test_fake_melee_heal(self):
  a={'action_id':'T346/A01','source_ref':'forged','rule_version':'HN-V1.3','legal_hit':True,'landed':True,'raw_damage':35,'is_melee_sword':True,'is_ordinary_sword':True}
  d={'HP_current':30,'HP_max':92,'DEF':12,'living_blood_bearing':True}
  e={'mitigation':0,'attacker_HP_current':117,'attacker_HP_max':170,'attacker_BLOOD_current':35,'attacker_BLOOD_max':50,'hap_heal_already_this_combat_turn':0}
  with self.assertRaises(ValueError):resolve_damage(a,d,e)
