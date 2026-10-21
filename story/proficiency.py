"""Organic Proficiency V1.0 — evidence gate before existing V1.3 skill_use.

Pure, side-effect-free. No GM action execution, character stats, or automatic skill grants.
"""
from __future__ import annotations

import copy
from story.progression import skill_use

FIELDS = ('use_id', 'evidence_id', 'source', 'practice_context_id',
          'challenge_signature', 'skill_id', 'outcome', 'turn')


def proficiency_use(entry: dict, event: dict, *, seed: str | None = None,
                    next_contract: dict | None = None) -> dict:
    """Receipt one observed, meaningful domain-specific use; V1.3 computes XP.

    Preconditions and outcome are GM-adjudicated evidence, not inferred by code.
    Existing receipt identities are immutable. Three credited uses per equivalent
    practice context max unless a genuinely distinct context is evidenced.
    """
    if not isinstance(entry, dict) or not isinstance(event, dict):
        raise ValueError('skill entry and evidence event must be objects')
    for key in FIELDS:
        val = event.get(key)
        if key == 'turn':
            if type(val) is not int or val < 1:
                raise ValueError('turn must be a positive integer')
        elif not isinstance(val, str) or not val.strip():
            raise ValueError(f'missing nonempty {key}')
    if event['outcome'] not in ('effective', 'failure'):
        raise ValueError('outcome must be effective or failure')
    if type(entry.get('level')) is not int or entry['level'] < 1 or entry.get('rarity') not in ('Common', 'Rare'):
        raise ValueError('only verified learned Common/Rare skills are eligible')
    # The T244 legacy state stores the Vietnamese name but not yet an ID field.
    entry_id = entry.get('skill_id') or (
        'NhanQuanHiepChien' if entry.get('name') == 'Nhãn Quan Hiệp Chiến' else None)
    if entry_id != event['skill_id']:
        raise ValueError('skill identity mismatch')
    if entry_id == 'NhanQuanHiepChien' and next_contract is not None:
        raise ValueError('Lv2 contract for this passive is not approved under V1.0')
    receipts = entry.get('use_receipts', {})
    if not isinstance(receipts, dict):
        raise ValueError('invalid receipts')
    if event['use_id'] in receipts:
        prior = receipts[event['use_id']]
        if prior.get('evidence_id') != event['evidence_id']:
            raise ValueError('conflicting evidence for already claimed action')
        return copy.deepcopy(entry)
    if any(x.get('evidence_id') == event['evidence_id'] for x in receipts.values()):
        raise ValueError('same witnessed action presented under another id')

    # Explicit GM checks, not a heuristic score or automatic verification.
    preconditions = event.get('preconditions_met') is True
    resolved = event.get('action_adjudicated') is True
    meaningful = event.get('meaningful_challenge') is True
    novelty = isinstance(event.get('novelty_evidence'), str) and bool(event['novelty_evidence'].strip())
    prior_equivalent_uses = sum(
        x.get('practice_context_id') == event['practice_context_id']
        and x.get('base_exp', 0) > 0
        for x in receipts.values()
    )
    below_cap = prior_equivalent_uses < 3
    unlocked_before_action = event['turn'] > entry.get('earned_turn', 0)
    # For a team-cue passive, perceived cues and cooperative ally are essential.
    if event['skill_id'] == 'NhanQuanHiepChien':
        cue_valid = (event.get('ally_cooperating') is True
                     and event.get('observable_ally_cue') is True)
    else:
        cue_valid = True
    eligible = all((preconditions, resolved, meaningful, novelty,
                    below_cap, unlocked_before_action, cue_valid))
    result = skill_use(entry, event['use_id'], event['outcome'], seed=seed,
                       skill_id=event['skill_id'], eligible=eligible,
                       next_contract=next_contract)
    receipt = result['use_receipts'][event['use_id']]
    receipt.update({
        'evidence_id': event['evidence_id'],
        'source': event['source'],
        'turn': event['turn'],
        'challenge_signature': event['challenge_signature'],
        'practice_context_id': event['practice_context_id'],
        'novelty_evidence': event.get('novelty_evidence', ''),
        'qualified': eligible,
        'ineligible_reasons': [name for name, ok in (
            ('preconditions', preconditions), ('not_adjudicated', resolved),
            ('trivial_or_idle', meaningful), ('no_novelty_receipt', novelty),
            ('repeated_context_cap', below_cap),
            ('unlock_exam_or_old_turn', unlocked_before_action),
            ('unperceived_or_absent_ally', cue_valid),
        ) if not ok],
    })
    return result
