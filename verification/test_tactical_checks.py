import unittest
from story.tactical_checks import check_tactical

class TacticalTests(unittest.TestCase):
 def test_blocked_archery_and_friend(self):
  intent={'source_ref':'synthetic','turn':346,'substeps':[{'id':'s1','actor':'Maela','verb':'shoot','target':'A'}]}
  d={'target_visibility':'last_seen','los':'blocked','crossfire':'clear','route':'unknown','actor_ready':'ready','evidence_refs':['synthetic']}
  self.assertEqual(check_tactical(intent,{'substeps':{'s1':d}})['substeps'][0]['disposition'],'BLOCKED')
  d['target_visibility']='visible';d['los']='clear';d['crossfire']='blocked'
  self.assertEqual(check_tactical(intent,{'substeps':{'s1':d}})['substeps'][0]['disposition'],'BLOCKED')
 def test_clear_legal_not_auto_hit(self):
  i={'source_ref':'s','turn':346,'substeps':[{'id':'shot','actor':'Maela','verb':'shoot','target':'A'}]}
  d={'target_visibility':'visible','los':'clear','crossfire':'clear','route':'unknown','actor_ready':'ready','ammo':'available','evidence_refs':['s']}
  r=check_tactical(i,{'substeps':{'shot':d}})['substeps'][0]
  self.assertEqual(r['disposition'],'ALLOWED');self.assertNotIn('hit',r)
 def test_compound_conditional_pursuit(self):
  i={'source_ref':'s','turn':346,'substeps':[{'id':'chase','actor':'V','verb':'pursue','target':'A'},{'id':'shot','actor':'Maela','verb':'shoot','target':'A'}]}
  d={'chase':{'target_visibility':'last_seen','route':'traversable','actor_ready':'ready','evidence_refs':['s']},'shot':{'target_visibility':'last_seen','los':'blocked','crossfire':'clear','actor_ready':'ready','evidence_refs':['s']}}
  r=check_tactical(i,{'substeps':d})
  self.assertEqual([v['disposition'] for v in r['substeps']],['CONDITIONAL','BLOCKED']);self.assertTrue(r['substeps'][0]['possible_reaction_window'])
 def test_unknown_ammo_and_unsupported(self):
  i={'source_ref':'s','turn':346,'substeps':[{'id':'s','actor':'Maela','verb':'shoot','target':'A'}]}
  d={'target_visibility':'visible','los':'clear','crossfire':'clear','actor_ready':'unknown','evidence_refs':['s']}
  self.assertEqual(check_tactical(i,{'substeps':{'s':d}})['substeps'][0]['disposition'],'UNKNOWN')
  i['substeps'][0]['verb']='teleport'
  self.assertEqual(check_tactical(i,{'substeps':{'s':d}})['substeps'][0]['disposition'],'UNKNOWN')
