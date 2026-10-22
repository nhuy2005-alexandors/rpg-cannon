import copy
import unittest
from story.combat_mechanics import resolve_damage, check_skill_availability


def attack(**changes):
    o=dict(action_id='T346/A01',source_ref='noncanon/fixture',rule_version='HN-V1.3',legal_hit=True,landed=True,raw_damage=35,kind='sword',is_melee_sword=True,is_ordinary_sword=True)
    o.update(changes);return o

def target(**changes):
    o=dict(HP_current=14,HP_max=92,DEF=12,living_blood_bearing=True)
    o.update(changes);return o

def effects(**changes):
    o=dict(mitigation=0,attacker_HP_current=117,attacker_HP_max=170,attacker_BLOOD_current=46,attacker_BLOOD_max=50,hap_heal_already_this_combat_turn=0)
    o.update(changes);return o

class DamageTests(unittest.TestCase):
    def test_overkill_caps_hp_loss_not_raw(self):
        x=resolve_damage(attack(),target(),effects())
        self.assertEqual((x['candidate_damage'],x['actual_hp_lost'],x['defender_hp_after']),(23,14,0))
        self.assertEqual(x['hap_heal_gained'],1)
        self.assertEqual(x['blood_gained'],4)

    def test_shield_mitigation(self):
        x=resolve_damage(attack(raw_damage=33),target(HP_current=9,DEF=14),effects(mitigation=7))
        self.assertEqual((x['candidate_damage'],x['actual_hp_lost']),(12,9))

    def test_hap_heal_capped_per_combat_turn_and_max_hp(self):
        x=resolve_damage(attack(raw_damage=130),target(HP_current=90,DEF=0,HP_max=90),effects(attacker_HP_current=169,hap_heal_already_this_combat_turn=4,attacker_BLOOD_current=46))
        self.assertEqual(x['hap_heal_gained'],1)
        self.assertEqual(x['attacker_hp_after'],170)
        self.assertEqual(x['attacker_blood_after'],50)
        self.assertEqual(x['blood_gained'],4)

    def test_nonordinary_melee_skill_may_heal_but_not_gain_blood(self):
        x=resolve_damage(attack(is_ordinary_sword=False),target(),effects())
        self.assertEqual(x['blood_gained'],0)
        self.assertEqual(x['hap_heal_gained'],1)

    def test_miss_undead_or_non_melee_no_gains(self):
        for a,t in [(attack(landed=False),target()),(attack(),target(living_blood_bearing=False)),(attack(is_melee_sword=False,is_ordinary_sword=False),target())]:
            with self.subTest(a=a,t=t):
                x=resolve_damage(a,t,effects())
                self.assertEqual((x['hap_heal_gained'],x['blood_gained']),(0,0))
        self.assertEqual(resolve_damage(attack(landed=False),target(),effects())['actual_hp_lost'],0)

    def test_landed_ordinary_sword_with_defense_zero_hp_loss_gains_blood_without_heal(self):
        x=resolve_damage(attack(raw_damage=8),target(DEF=12),effects())
        self.assertEqual((x['actual_hp_lost'],x['hap_heal_gained'],x['blood_gained']),(0,0,4))

    def test_missing_or_negative_values_fail_closed_and_input_immutable(self):
        for a,t,e in [(attack(raw_damage=None),target(),effects()),(attack(raw_damage=True),target(),effects()),(attack(),target(DEF=-1),effects()),(attack(),target(),effects(mitigation=-1)),(attack(),target(HP_current=94),effects()),(attack(legal_hit=False,landed=True),target(),effects())]:
            with self.subTest(a=a,t=t,e=e),self.assertRaises(ValueError):resolve_damage(a,t,e)
        a,t,e=attack(),target(),effects()
        originals=copy.deepcopy((a,t,e));resolve_damage(a,t,e)
        self.assertEqual((a,t,e),originals)

class AvailabilityTests(unittest.TestCase):
    def test_cooldown_explicit_ready_and_blocked(self):
        st={'cooldowns':{'dash':{'ready_at_combat_turn':12,'source_ref':'event/test'}},'resources':{'STA':{'current':41,'max':110}}}
        ctx={'known_skill':True,'costs':{'STA':10},'required_conditions':{},'evidence_refs':['event/test']}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':11},ctx)['status'],'BLOCKED')
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'READY')

    def test_unknown_cooldown_and_status_fail_closed(self):
        st={'cooldowns':{},'resources':{'STA':{'current':41,'max':110}}}
        ctx={'known_skill':True,'costs':{'STA':10},'required_conditions':{},'evidence_refs':['event/test']}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'UNKNOWN')
        self.assertEqual(check_skill_availability('dash',st,{'elapsed_rest_minutes':180},ctx)['status'],'UNKNOWN')
        st['cooldowns']['dash']={'ready_at_combat_turn':12,'source_ref':'event/test'}
        st['status_effects']={'silenced':{'blocks':'dash','expiration':'UNKNOWN'}}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'UNKNOWN')

    def test_insufficient_sta_and_known_physical_block(self):
        st={'cooldowns':{'dash':{'ready_at_combat_turn':12,'source_ref':'event/test'}},'resources':{'STA':{'current':4,'max':110}}}
        ctx={'known_skill':True,'costs':{'STA':10},'required_conditions':{},'evidence_refs':['event/test']}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'BLOCKED')
        st['resources']['STA']['current']=41
        ctx['required_conditions']={'weapon_ready':'blocked'}
        self.assertEqual(check_skill_availability('dash',st,{'combat_turn':12},ctx)['status'],'BLOCKED')

if __name__=='__main__':unittest.main()
