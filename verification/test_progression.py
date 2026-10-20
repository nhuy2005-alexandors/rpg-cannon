import unittest

from story.progression import (
    soul_yield, encounter_bonus, claim_loot, skill_use,
    rerollable_draw, respec_branch,
)


class TestSoul(unittest.TestCase):
    def test_soul_curve_and_boundary(self):
        for lev, expected in [(1, 2), (2, 5), (3, 6), (4, 10), (5, 12),
                              (6, 14), (8, 18), (9, 25), (11, 36)]:
            with self.subTest(level=lev):
                self.assertEqual(soul_yield(lev, 'normal', 6), expected)
        self.assertEqual(soul_yield(20, 'boss', 6), 378)
        with self.assertRaises(ValueError): soul_yield(0, 'normal', 6)
        with self.assertRaises(ValueError): soul_yield(5, 'unconfirmed-elite', 6)

    def test_bonus_once_and_cap(self):
        self.assertEqual(encounter_bonus([12, 12, 12], .25), 9)
        self.assertEqual(encounter_bonus([12, 12], .10), 2)
        with self.assertRaises(ValueError): encounter_bonus([12], .30)

    def test_loot_claim_once_and_th_only_with_source(self):
        state = {'souls': 5, 'TH': 19, 'TH_max': 20, 'claims': {}}
        with self.assertRaises(ValueError): claim_loot(state, 'c1', 12, th=2, th_source=False)
        a = claim_loot(state, 'c1', 12, th=2, th_source=True)
        self.assertEqual((a['souls'], a['TH']), (17, 20))
        self.assertEqual(a['claims']['c1']['th_overflow'], 1)
        self.assertEqual(claim_loot(a, 'c1', 12, th=2, th_source=True), a)
        self.assertEqual(state['souls'], 5)
        self.assertEqual(claim_loot(a, 'c2', 12, th=0, th_source=False)['souls'], 29)


class TestMastery(unittest.TestCase):
    def test_rng_determinism(self):
        x = rerollable_draw('public-seed', 'turn195/a01/skill:parry')
        self.assertEqual(x, rerollable_draw('public-seed', 'turn195/a01/skill:parry'))
        self.assertTrue(0 <= x <= 0xffffffff)
        self.assertNotEqual(x, rerollable_draw('public-seed', 'turn195/a02/skill:parry'))

    def test_effective_use_awards_only_once_and_gates(self):
        entry = {'level': 2, 'rarity': 'Rare', 'skill_exp_current': 0, 'use_receipts': {}}
        a = skill_use(entry, 'use-1', 'effective', seed='public-seed', skill_id='double', eligible=True)
        self.assertIn(a['use_receipts']['use-1']['bonus_exp'], (0, 5))
        self.assertIn(a['skill_exp_current'], (2, 7))
        self.assertEqual(skill_use(a, 'use-1', 'effective', seed='public-seed', skill_id='double', eligible=True), a)
        b = skill_use(a, 'use-2', 'failure', seed='public-seed', skill_id='double', eligible=True)
        self.assertEqual(b['skill_exp_current'] - a['skill_exp_current'], 1)
        z = skill_use(b, 'use-3', 'effective', seed='public-seed', skill_id='double', eligible=False)
        self.assertEqual(z['skill_exp_current'], b['skill_exp_current'])

    def test_missing_seed_no_fabricated_roll(self):
        e = {'level': 1, 'rarity': 'Rare', 'skill_exp_current': 0, 'use_receipts': {}}
        x = skill_use(e, 'u1', 'effective', seed=None, skill_id='shadow-step', eligible=True)
        self.assertEqual(x['skill_exp_current'], 2)
        self.assertEqual(x['use_receipts']['u1']['bonus_status'], 'PENDING_UNROLLED')

    def test_level_up_only_if_approved_contract_and_preserves_excess(self):
        e = {'level': 2, 'rarity': 'Common', 'skill_exp_current': 89, 'use_receipts': {}}
        x = skill_use(e, 'u1', 'failure', seed='s', skill_id='parry', eligible=True)
        self.assertEqual(x['level'], 2)
        self.assertEqual(x['level_up_status'], 'BLOCKED_PENDING_CONTRACT')
        contract = {'from_level': 2, 'to_level': 3, 'version': 'skill-parry-v1.3', 'approved': True}
        y = skill_use(e, 'u1', 'failure', seed='s', skill_id='parry', eligible=True, next_contract=contract)
        self.assertEqual(y['level'], 3)
        self.assertEqual(y['skill_exp_current'], 0)
        self.assertEqual(skill_use(y, 'u1', 'failure', seed='s', skill_id='parry', eligible=True, next_contract=contract), y)

    def test_unverified_rarity_blocks_level_up(self):
        e = {'level': 1, 'rarity': 'UNVERIFIED', 'skill_exp_current': 999, 'use_receipts': {}}
        x = skill_use(e, 'u1', 'failure', seed='s', skill_id='unknown', eligible=True)
        self.assertEqual(x['level'], 1)
        self.assertEqual(x['skill_exp_current'], 1000)


class TestRespec(unittest.TestCase):
    def test_switch_only_in_safe_context_with_payment_and_preserved_cd(self):
        state = {'souls': 29, 'combat': False, 'safe': True, 'safe_minutes': 60,
                 'skill': {'level': 3, 'rarity': 'Rare', 'active_branch_id': 'parry',
                           'unlocked_branches': ['parry', 'blood'], 'cooldown_remaining': 2,
                           'skill_exp_current': 42}, 'respec_claims': {}}
        after = respec_branch(state, 'blood', 'respec-t1')
        self.assertEqual((after['souls'], after['skill']['active_branch_id']), (11, 'blood'))
        self.assertEqual((after['skill']['cooldown_remaining'], after['skill']['skill_exp_current']), (2, 42))
        self.assertEqual(respec_branch(after, 'blood', 'respec-t1'), after)
        with self.assertRaises(ValueError): respec_branch({**state, 'combat': True}, 'blood', 'respec-t2')
        with self.assertRaises(ValueError): respec_branch(state, 'unlearned', 'respec-t3')


if __name__ == '__main__': unittest.main()
