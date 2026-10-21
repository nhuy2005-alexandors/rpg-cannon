"""Adversarial tests for the minimal organic skill-evidence gate."""
import copy
import unittest
from story.proficiency import proficiency_use


def learned(xp=0, level=1):
    return {'name': 'Nhãn Quan Hiệp Chiến', 'skill_id': 'NhanQuanHiepChien',
            'rarity': 'Common', 'level': level, 'earned_turn': 244,
            'skill_exp_current': xp, 'use_receipts': {}}


def event(n=1, **overrides):
    x = {'use_id': f'T{244+n}/A01', 'evidence_id': f'visible-event-{n}',
         'source': f'events/{244+n:04d}.md', 'practice_context_id': 'west-road-v1',
         'challenge_signature': 'enemy-archer-cover-shift', 'skill_id': 'NhanQuanHiepChien',
         'outcome': 'effective', 'turn': 244+n, 'preconditions_met': True,
         'action_adjudicated': True, 'meaningful_challenge': True,
         'novelty_evidence': 'seen teammate moving off firing lane against enemy',
         'ally_cooperating': True, 'observable_ally_cue': True}
    x.update(overrides)
    return x


class TestProficiency(unittest.TestCase):
    def test_effective_earns_base_2_without_fabricated_rng(self):
        a = proficiency_use(learned(), event(), seed=None)
        self.assertEqual(a['skill_exp_current'], 2)
        self.assertEqual(a['use_receipts']['T245/A01']['bonus_status'], 'PENDING_UNROLLED')
        self.assertIsNone(a['use_receipts']['T245/A01']['draw'])

    def test_failure_after_real_attempt_earns_1(self):
        a = proficiency_use(learned(), event(outcome='failure'), seed=None)
        self.assertEqual(a['skill_exp_current'], 1)

    def test_ineligible_cues_do_not_reward(self):
        for override in ({'ally_cooperating': False}, {'observable_ally_cue': False},
                         {'preconditions_met': False}, {'action_adjudicated': False},
                         {'meaningful_challenge': False}, {'novelty_evidence': ''}):
            with self.subTest(override=override):
                a = proficiency_use(learned(), event(**override), seed='known-seed')
                self.assertEqual(a['skill_exp_current'], 0)
                self.assertFalse(a['use_receipts']['T245/A01']['qualified'])
                self.assertEqual(a['use_receipts']['T245/A01']['bonus_exp'], 0)

    def test_skill_not_earned_before_T244(self):
        a = proficiency_use(learned(), event(turn=244), seed=None)
        self.assertEqual(a['skill_exp_current'], 0)
        self.assertIn('unlock_exam_or_old_turn', a['use_receipts']['T245/A01']['ineligible_reasons'])

    def test_replay_same_action_id_idempotent(self):
        a = proficiency_use(learned(), event(), seed=None)
        b = proficiency_use(a, event(), seed='known-seed')
        self.assertEqual(a, b)

    def test_replay_action_with_changed_evidence_rejected(self):
        a = proficiency_use(learned(), event(), seed=None)
        with self.assertRaisesRegex(ValueError, 'conflicting evidence'):
            proficiency_use(a, event(evidence_id='forged-second-evidence'))

    def test_same_evidence_new_action_id_rejected(self):
        a = proficiency_use(learned(), event(), seed=None)
        with self.assertRaisesRegex(ValueError, 'same witnessed action'):
            proficiency_use(a, event(2, evidence_id='visible-event-1'))

    def test_three_equivalent_meaningful_uses_cap(self):
        s = learned()
        for n in (1, 2, 3, 4, 5):
            s = proficiency_use(s, event(n), seed=None)
        self.assertEqual(s['skill_exp_current'], 6)
        self.assertEqual([s['use_receipts'][f'T{244+n}/A01']['base_exp'] for n in (1,2,3,4,5)],
                         [2,2,2,0,0])

    def test_genuinely_distinct_context_can_qualify(self):
        s = learned()
        for n in (1, 2, 3):
            s = proficiency_use(s, event(n), seed=None)
        s = proficiency_use(s, event(4, practice_context_id='new-real-raid',
                                    challenge_signature='new-two-archer-ambush',
                                    novelty_evidence='different actual enemy and direction'), seed=None)
        self.assertEqual(s['skill_exp_current'], 8)

    def test_zero_credit_does_not_exhaust_context_quota(self):
        s = learned()
        s = proficiency_use(s, event(1, preconditions_met=False), seed=None)
        for n in (2, 3, 4):
            s = proficiency_use(s, event(n), seed=None)
        self.assertEqual(s['skill_exp_current'], 6)

    def test_skill_exp_threshold_block_without_approved_contract(self):
        s = proficiency_use(learned(xp=39), event(), seed=None)
        self.assertEqual((s['level'], s['skill_exp_current']), (1, 41))
        self.assertEqual(s['level_up_status'], 'BLOCKED_PENDING_CONTRACT')

    def test_unapproved_l2_contract_cannot_be_injected(self):
        contract = {'approved': True, 'from_level': 1, 'to_level': 2, 'version': 'invented-v2'}
        with self.assertRaisesRegex(ValueError, 'not approved'):
            proficiency_use(learned(xp=39), event(), seed=None, next_contract=contract)

    def test_existing_v13_approved_contract_path_remains_for_other_domain(self):
        contract = {'approved': True, 'from_level': 1, 'to_level': 2, 'version': 'approved-elsewhere'}
        s = {'skill_id': 'Woodcutting', 'rarity': 'Common', 'level': 1,
             'earned_turn': 10, 'skill_exp_current': 39, 'use_receipts': {}}
        x = proficiency_use(s, event(skill_id='Woodcutting', turn=12), seed=None, next_contract=contract)
        self.assertEqual((x['level'], x['skill_exp_current']), (2, 1))

    def test_legacy_T244_entry_without_skill_id_accepts_only_correct_id(self):
        x = learned(); del x['skill_id']
        self.assertEqual(proficiency_use(x, event(), seed=None)['skill_exp_current'], 2)
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            proficiency_use(x, event(skill_id='FakeSkill'), seed=None)

    def test_invalid_action_cannot_trigger_otherwise_approved_levelup(self):
        contract = {'approved': True, 'from_level': 1, 'to_level': 2, 'version': 'approved-elsewhere'}
        s = {'skill_id': 'Woodcutting', 'rarity': 'Common', 'level': 1,
             'earned_turn': 10, 'skill_exp_current': 40, 'use_receipts': {}}
        x = proficiency_use(s, event(skill_id='Woodcutting', turn=12,
                                     action_adjudicated=False), seed=None,
                            next_contract=contract)
        self.assertEqual(x['level'], 1)
        self.assertEqual(x['skill_exp_current'], 40)
        self.assertEqual(x['level_up_status'], 'BLOCKED_PENDING_CONTRACT')

    def test_no_input_mutation(self):
        entry = learned()
        e = event()
        entry_pre = copy.deepcopy(entry)
        event_pre = copy.deepcopy(e)
        proficiency_use(entry, e, seed=None)
        self.assertEqual(entry, entry_pre)
        self.assertEqual(e, event_pre)

    def test_invalid_ids_and_outcome(self):
        for ov in ({'use_id': ''}, {'evidence_id': ''}, {'source': ''},
                   {'practice_context_id': ''}, {'turn': 0}, {'turn': True},
                   {'outcome': 'success'}):
            with self.subTest(override=ov), self.assertRaises(ValueError):
                proficiency_use(learned(), event(**ov))

    def test_wrong_skill_and_unverified_rarity(self):
        with self.assertRaises(ValueError):
            proficiency_use(learned(), event(skill_id='different'))
        s = learned(); s['rarity'] = 'UNVERIFIED'
        with self.assertRaises(ValueError):
            proficiency_use(s, event())

    def test_non_team_domain_does_not_require_ally(self):
        s = {'skill_id': 'Woodcutting', 'rarity': 'Common', 'level': 1,
             'earned_turn': 10, 'skill_exp_current': 0, 'use_receipts': {}}
        a = proficiency_use(s, event(skill_id='Woodcutting', turn=12,
                                     ally_cooperating=False, observable_ally_cue=False,
                                     practice_context_id='distinct-timber-felling'), seed=None)
        self.assertEqual(a['skill_exp_current'], 2)
        self.assertNotIn('grants_strength', a)

    def test_no_backfill_extra_stats_or_resources(self):
        a = proficiency_use(learned(), event(), seed=None)
        for forbidden in ('STR', 'DEF', 'BLOOD', 'HP', 'STA', 'souls', 'character_exp'):
            self.assertNotIn(forbidden, a)

    def test_seed_draw_only_if_verified_rng_used(self):
        a = proficiency_use(learned(), event(), seed='seed-fixed')
        b = proficiency_use(learned(), event(), seed='seed-fixed')
        self.assertEqual(a, b)
        receipt = a['use_receipts']['T245/A01']
        self.assertIsInstance(receipt['draw'], int)
        self.assertIn(receipt['bonus_exp'], (0,5))

    def test_many_independent_unique_uses_nonnegative_under_cap(self):
        for initial in range(0, 39):
            for attempts in range(1, 6):
                s = learned(xp=initial)
                for n in range(1, attempts + 1):
                    s = proficiency_use(s, event(n), seed=None)
                self.assertEqual(s['skill_exp_current'], initial + 2 * min(attempts, 3))
                self.assertLessEqual(sum(x['base_exp'] for x in s['use_receipts'].values()), 6)


if __name__ == '__main__':
    unittest.main()
