"""Hac Nhat V1.3: small, pure progression helpers. No auto-run, storage or GM secrets."""
from __future__ import annotations

import copy
import hashlib
import math
from fractions import Fraction

RANK = {'normal': Fraction(1), 'enhanced': Fraction(3, 2), 'elite': Fraction(5, 2),
        'mini_boss': Fraction(4), 'boss': Fraction(6), 'world_boss': Fraction(12)}
BONUS = {Fraction(0), Fraction(1, 10), Fraction(3, 20), Fraction(1, 4)}
THRESHOLDS = {'Common': {1: 40, 2: 90, 3: 160},
              'Rare': {1: 60, 2: 135, 3: 240}}


def soul_yield(threat_level: int, rank: str, player_level_at_kill: int) -> int:
    """Soul scaling for pre-registered template level/rank; no HP-derived guesses."""
    if type(threat_level) is not int or threat_level < 1 or type(player_level_at_kill) is not int or player_level_at_kill < 1:
        raise ValueError('levels must be positive integers')
    if rank not in RANK:
        raise ValueError('rank must be a registered tier')
    delta = threat_level - player_level_at_kill
    difficulty = (Fraction(1, 2) if delta <= -5 else Fraction(3, 4) if delta <= -3
                  else Fraction(1) if delta <= 2 else Fraction(5, 4) if delta <= 4
                  else Fraction(3, 2))
    amount = (2 * threat_level + 2) * RANK[rank] * difficulty
    return math.ceil(amount)


def encounter_bonus(soul_claims: list[int], rate: float) -> int:
    """Calculate a pre-authorized one-time encounter bonus; caller records claim id."""
    factor = Fraction(str(rate))
    if factor not in BONUS or any(type(x) is not int or x < 0 for x in soul_claims):
        raise ValueError('invalid bonus tier or soul claims')
    return (sum(soul_claims) * factor).__floor__()


def claim_loot(state: dict, corpse_id: str, souls: int, *, th: int = 0, th_source: bool = False) -> dict:
    """Idempotent first corpse claim; returns a new state; caller persists atomically."""
    if not isinstance(corpse_id, str) or not corpse_id.strip():
        raise ValueError('corpse id required')
    if type(souls) is not int or souls < 0 or type(th) is not int or th < 0 or (th and not th_source):
        raise ValueError('invalid reward or Tử Huyết source')
    out = copy.deepcopy(state)
    if corpse_id in out['claims']:
        return out
    if type(out['TH']) is not int or type(out['TH_max']) is not int or not (0 <= out['TH'] <= out['TH_max']):
        raise ValueError('invalid TH reservoir')
    got_th = min(th, out['TH_max'] - out['TH'])
    out['souls'] += souls
    out['TH'] += got_th
    out['claims'][corpse_id] = {'souls': souls, 'th_received': got_th, 'th_overflow': th - got_th}
    return out


def rerollable_draw(seed: str, action_key: str) -> int:
    """Versioned public deterministic 32-bit draw; exact UTF-8 byte encoding."""
    if not isinstance(seed, str) or not seed or not isinstance(action_key, str) or not action_key:
        raise ValueError('fixed public seed and immutable action id required')
    msg = b'HN-RNG-V1.3\0' + len(seed.encode('utf-8')).to_bytes(4, 'big') + seed.encode('utf-8') + len(action_key.encode('utf-8')).to_bytes(4, 'big') + action_key.encode('utf-8')
    return int.from_bytes(hashlib.sha256(msg).digest()[:4], 'big')


def skill_use(entry: dict, use_id: str, outcome: str, *, seed: str | None, skill_id: str,
              eligible: bool, next_contract: dict | None = None) -> dict:
    """Award once per legal meaningful activation, not per hit or passive tick."""
    if not use_id or not skill_id or outcome not in {'effective', 'failure'}:
        raise ValueError('missing immutable use id, skill id or invalid outcome')
    out = copy.deepcopy(entry)
    receipts = out.setdefault('use_receipts', {})
    if use_id in receipts:
        return out
    base = (2 if outcome == 'effective' else 1) if eligible else 0
    bonus = 0
    status = 'NOT_ELIGIBLE'
    draw = None
    if eligible and outcome == 'effective':
        if seed is None:
            status = 'PENDING_UNROLLED'
        else:
            draw = rerollable_draw(seed, f'{skill_id}/{use_id}')
            bonus = 5 if draw < (1 << 30) else 0
            status = 'AWARDED' if bonus else 'ROLLED_NO_BONUS'
    out['skill_exp_current'] += base + bonus
    receipts[use_id] = {'base_exp': base, 'bonus_exp': bonus, 'bonus_status': status,
                        'draw': draw, 'rng_version': 'HN-RNG-V1.3' if draw is not None else None}
    level = out.get('level')
    threshold = THRESHOLDS.get(out.get('rarity'), {}).get(level)
    if threshold is not None and out['skill_exp_current'] >= threshold:
        if (next_contract and next_contract.get('approved') is True
            and next_contract.get('from_level') == level
            and next_contract.get('to_level') == level + 1
            and next_contract.get('version')):
            out['skill_exp_current'] -= threshold
            out['level'] = level + 1
            out['level_up_contract_version'] = next_contract['version']
            out['level_up_status'] = 'APPLIED'
        else:
            out['level_up_status'] = 'BLOCKED_PENDING_CONTRACT'
    return out


def respec_branch(state: dict, branch_id: str, transaction_id: str) -> dict:
    """One-branch active, safely paid respec. Caller supplies verified safe elapsed time."""
    if not transaction_id or not branch_id:
        raise ValueError('id required')
    out = copy.deepcopy(state)
    if transaction_id in out.setdefault('respec_claims', {}):
        return out
    if out.get('combat') or not out.get('safe') or out.get('safe_minutes', 0) < 60:
        raise ValueError('respec requires an uninterrupted safe hour outside combat')
    skill = out['skill']
    if branch_id not in skill.get('unlocked_branches', ()):
        raise ValueError('branch is not unlocked')
    if branch_id == skill.get('active_branch_id'):
        raise ValueError('branch already active')
    if skill.get('rarity') not in ('Common', 'Rare') or type(skill.get('level')) is not int:
        raise ValueError('unverified skill tier/level')
    cost = 3 * skill['level'] * (2 if skill['rarity'] == 'Rare' else 1)
    if out['souls'] < cost:
        raise ValueError('insufficient souls')
    out['souls'] -= cost
    skill['active_branch_id'] = branch_id
    out['respec_claims'][transaction_id] = {'cost': cost, 'to': branch_id}
    return out
