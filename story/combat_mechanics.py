"""Pure Hac Nhat combat math and skill readiness guards. No RNG or story progression."""
from __future__ import annotations


def _integer(value, key, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'invalid {key}')
    return value


def _pool(current, maximum, kind):
    current = _integer(current, kind+' current')
    maximum = _integer(maximum, kind+' maximum', 1)
    if current > maximum:
        raise ValueError(f'{kind} exceeds maximum')
    return current, maximum


def resolve_damage(attack: dict, defender: dict, effects: dict) -> dict:
    """Compute a *known, legal* contact; never decide hit chance or mutate input."""
    if not all(isinstance(x, dict) for x in (attack, defender, effects)):
        raise ValueError('source maps required')
    if not all(isinstance(attack.get(x), str) and attack[x] for x in ('action_id', 'source_ref', 'rule_version')):
        raise ValueError('stable action and evidence required')
    for field in ('legal_hit', 'landed', 'is_melee_sword', 'is_ordinary_sword'):
        if type(attack.get(field)) is not bool:
            raise ValueError(f'{field} must be explicit boolean')
    if attack['landed'] and not attack['legal_hit']:
        raise ValueError('illegal landed contact')
    if attack['is_ordinary_sword'] and not attack['is_melee_sword']:
        raise ValueError('ordinary sword hit requires melee sword')
    raw = _integer(attack.get('raw_damage'), 'raw damage')
    defense = _integer(defender.get('DEF'), 'DEF')
    mitigation = _integer(effects.get('mitigation'), 'mitigation')
    enemy_hp, enemy_max = _pool(defender.get('HP_current'), defender.get('HP_max'), 'enemy HP')
    atk_hp, atk_hp_max = _pool(effects.get('attacker_HP_current'), effects.get('attacker_HP_max'), 'attacker HP')
    atk_blood, atk_blood_max = _pool(effects.get('attacker_BLOOD_current'), effects.get('attacker_BLOOD_max'), 'attacker BLOOD')
    already = _integer(effects.get('hap_heal_already_this_combat_turn'), 'heal accumulator')
    if already > 5 or type(defender.get('living_blood_bearing')) is not bool:
        raise ValueError('invalid source or heal accumulator')
    landed = attack['landed'] and attack['legal_hit']
    candidate = max(0, raw-defense-mitigation) if landed else 0
    actual = min(candidate, enemy_hp)
    qualifies = bool(actual > 0 and defender['living_blood_bearing'] and attack['is_melee_sword'])
    heal_proposed = max(1, actual // 10) if qualifies else 0
    heal = min(heal_proposed, 5-already, atk_hp_max-atk_hp)
    blood_proposed = 7 if landed and defender['living_blood_bearing'] and attack['is_ordinary_sword'] else 0
    blood = min(blood_proposed, atk_blood_max-atk_blood)
    return {'action_id': attack['action_id'], 'source_ref': attack['source_ref'],
            'rule_version': attack['rule_version'], 'qualified': qualifies,
            'reason': 'QUALIFIED_MELEE_BLOOD_CONTACT' if qualifies else 'NO_ELIGIBLE_BLOOD_CONTACT',
            'candidate_damage': candidate, 'actual_hp_lost': actual,
            'defender_hp_after': enemy_hp-actual, 'blood_gained': blood,
            'hap_heal_gained': heal, 'attacker_hp_after': atk_hp+heal,
            'attacker_blood_after': atk_blood+blood}


def check_skill_availability(skill_id: str, pre_state: dict, clock: dict, action_context: dict) -> dict:
    """READY/BLOCKED/UNKNOWN using explicit accepted data, not inferred elapsed time."""
    if not isinstance(skill_id, str) or not skill_id or not all(isinstance(x, dict) for x in (pre_state, clock, action_context)):
        raise ValueError('skill id and inputs required')
    sources = action_context.get('evidence_refs')
    if not isinstance(sources, list) or not sources or any(not isinstance(s, str) or not s for s in sources):
        raise ValueError('evidence references required')
    if action_context.get('known_skill') is False:
        return {'status': 'BLOCKED', 'reasons':['SKILL_NOT_LEARNED'], 'source_refs': sources, 'cost_requirements': {}}
    if action_context.get('known_skill') is not True:
        return {'status': 'UNKNOWN', 'reasons':['SKILL_UNVERIFIED'], 'source_refs': sources, 'cost_requirements': {}}
    reasons = []
    unknown = []
    cost = action_context.get('costs', {})
    conditions = action_context.get('required_conditions', {})
    if not isinstance(cost, dict) or not isinstance(conditions, dict):
        raise ValueError('invalid cost/conditions')
    for resource, amount in cost.items():
        _integer(amount, f'{resource} cost')
        pool = pre_state.get('resources', {}).get(resource)
        if not isinstance(pool, dict) or pool.get('current') == 'UNKNOWN' or pool is None:
            unknown.append('UNKNOWN_RESOURCE_'+resource)
        elif type(pool.get('current')) is not int:
            unknown.append('UNKNOWN_RESOURCE_'+resource)
        else:
            _pool(pool['current'], pool.get('max'), resource)
            if pool['current'] < amount:
                reasons.append('INSUFFICIENT_'+resource)
    for cond, status in conditions.items():
        if status == 'blocked':reasons.append('BLOCKED_CONDITION_'+str(cond))
        elif status != 'ready':unknown.append('UNKNOWN_CONDITION_'+str(cond))
    cd = pre_state.get('cooldowns', {}).get(skill_id)
    if not isinstance(cd, dict) or not isinstance(cd.get('source_ref'), str) or not cd.get('source_ref'):
        unknown.append('UNKNOWN_COOLDOWN_EVIDENCE')
    else:
        now = clock.get('combat_turn')
        ready_at = cd.get('ready_at_combat_turn')
        if type(ready_at) is not int or type(now) is not int or ready_at < 0 or now < 0:
            unknown.append('UNKNOWN_COMBAT_CLOCK')
        elif now < ready_at:
            reasons.append('COOLDOWN_ACTIVE')
    status_effects=pre_state.get('status_effects', {})
    if not isinstance(status_effects, dict):unknown.append('UNKNOWN_STATUS_LEDGER')
    else:
        for name, value in status_effects.items():
            if not isinstance(value, dict):unknown.append('UNKNOWN_STATUS_'+str(name));continue
            if value.get('blocks') in (skill_id,'all'):
                if value.get('expiration') == 'UNKNOWN':unknown.append('UNKNOWN_STATUS_'+str(name))
                elif value.get('active') is True:reasons.append('STATUS_BLOCK_'+str(name))
                elif value.get('active') is not False:unknown.append('UNKNOWN_STATUS_'+str(name))
    return {'status': 'BLOCKED' if reasons else 'UNKNOWN' if unknown else 'READY',
            'reasons': reasons+unknown, 'source_refs': list(sources), 'cost_requirements': dict(cost)}
