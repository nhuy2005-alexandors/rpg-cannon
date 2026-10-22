import unittest
from story.combat_mechanics import resolve_damage, check_skill_availability

class CombatTests(unittest.TestCase):
    def a(self, **k):
        return dict(action_id='T346/A01', source_ref='synthetic', rule_version='HN-V1.3', legal_hit=True, landed=True, raw_damage=35, kind='melee', is_melee_sword=True,is_ordinary_sword=True) | k
    def d(self, **k): return dict(HP_current=14,HP_max=92,DEF=12,living_blood_bearing=True) | k
    def e(self, **k): return dict(mitigation=0,attacker_HP_current=117,attacker_HP_max=170,attacker_BLOOD_current=46,attacker_BLOOD_max=50,hap_heal_already_this_combat_turn=4, verified_evidence_refs=['synthetic']) | k
    def test_overkill(self):
        r=resolve_damage(self.a(),self.d(),self.e())
        self.assertEqual((r['candidate_damage'],r['actual_hp_lost'],r['defender_hp_after']),(23,14,0))
        self.assertEqual((r['blood_gained'],r['hap_heal_gained']), (4,1))
    def test_skill_blood_exclusion(self):
        r=resolve_damage(self.a(is_ordinary_sword=False),self.d(),self.e())
        self.assertEqual(r['blood_gained'],0)
        self.assertEqual(r['hap_heal_gained'],1)
    def test_miss_undead(self):
        miss=resolve_damage(self.a(landed=False),self.d(),self.e())
        self.assertEqual(miss['actual_hp_lost'],0)
        self.assertEqual(miss['blood_gained'],0)
        undead=resolve_damage(self.a(),self.d(living_blood_bearing=False),self.e())
        self.assertEqual((undead['hap_heal_gained'],undead['blood_gained']),(0,0))
    def test_invalid_bool_and_missing(self):
        for attack in (self.a(raw_damage=True),self.a(raw_damage=None)):
            with self.assertRaises(ValueError): resolve_damage(attack,self.d(),self.e())
    def test_availability_unknown_and_blocked(self):
        ctx={'known_skill':True,'costs':{'STA':15},'evidence_refs':['synthetic'],'verified_evidence_refs':['synthetic']}
        st={'resources':{'STA':41},'cooldowns':{},'status_effects':{}}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'UNKNOWN')
        st['cooldowns']['dash']={'ready_at_combat_turn':13,'source_ref':'synthetic'}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'BLOCKED')
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':13},ctx)['status'],'READY')
        st['resources']['STA']=10
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':13},ctx)['status'],'BLOCKED')
