"""Pure grounded combat calculations; no dice, state writes or invented skill costs."""

def _int(v, field):
    if type(v) is not int or v < 0:
        raise ValueError(f'{field} requires nonnegative integer')
    return v

def resolve_damage(attack: dict, defender: dict, effects: dict) -> dict:
    verified=effects.get('verified_evidence_refs', [])
    if (not isinstance(verified, (list, tuple, set)) or
        attack.get('source_ref') not in verified):
        raise ValueError('combat source not independently verified')
    for field in ('action_id','source_ref','rule_version'):
        if not isinstance(attack.get(field), str) or not attack[field].strip():
            raise ValueError(f'missing {field}')
    for field in ('raw_damage',): _int(attack.get(field),field)
    for field in ('HP_current','HP_max','DEF'): _int(defender.get(field),field)
    for field in ('mitigation','attacker_HP_current','attacker_HP_max','attacker_BLOOD_current','attacker_BLOOD_max','hap_heal_already_this_combat_turn'):
        _int(effects.get(field),field)
    if not(0 <= defender['HP_current'] <= defender['HP_max'] and
           effects['attacker_HP_current']<=effects['attacker_HP_max'] and
           effects['attacker_BLOOD_current']<=effects['attacker_BLOOD_max'] and
           effects['hap_heal_already_this_combat_turn']<=5):
        raise ValueError('invalid reservoir')
    if attack.get('legal_hit') is not True or not isinstance(attack.get('landed'),bool):
        raise ValueError('legal adjudication required')
    actual=0
    candidate=0
    if attack['landed']:
        candidate=max(0,attack['raw_damage']-defender['DEF']-effects['mitigation'])
        actual=min(candidate,defender['HP_current'])
    qualifying=bool(actual>0 and defender.get('living_blood_bearing') is True and attack.get('is_melee_sword') is True)
    heal=0
    blood=0
    if qualifying:
        heal=min(5-effects['hap_heal_already_this_combat_turn'], max(1,actual//10),effects['attacker_HP_max']-effects['attacker_HP_current'])
        if attack.get('is_ordinary_sword') is True:
            blood=min(7,effects['attacker_BLOOD_max']-effects['attacker_BLOOD_current'])
    return {'action_id':attack['action_id'],'source_ref':attack['source_ref'],
      'candidate_damage':candidate,'actual_hp_lost':actual,'defender_hp_after':defender['HP_current']-actual,
      'blood_gained':blood,'hap_heal_gained':heal,'attacker_hp_after':effects['attacker_HP_current']+heal,
      'attacker_blood_after':effects['attacker_BLOOD_current']+blood,'qualified':qualifying,
      'reason':'QUALIFYING_BLOOD_HIT' if qualifying else 'NO_BLOOD_HEAL'}

def check_skill_availability(skill_id: str, pre_state: dict, clock: dict, action_context: dict) -> dict:
    if not isinstance(skill_id,str) or not skill_id.strip():raise ValueError('skill id required')
    sources=action_context.get('evidence_refs', [])
    trusted=action_context.get('verified_evidence_refs', [])
    if (not isinstance(trusted,(list,tuple,set)) or not isinstance(sources,list) or not sources or
        not set(sources).issubset(set(trusted)) or not action_context.get('known_skill')):
        return {'status':'UNKNOWN','reasons':['skill or contract unverified'],'source_refs':sources}
    entry=pre_state.get('cooldowns',{}).get(skill_id)
    now=clock.get('combat_turn')
    if not isinstance(entry,dict) or type(now) is not int or now<0:
        return {'status':'UNKNOWN','reasons':['cooldown or combat clock unknown'],'source_refs':sources}
    if not entry.get('source_ref') or entry['source_ref'] not in trusted:
        return {'status':'UNKNOWN','reasons':['cooldown lacks accepted evidence'],'source_refs':sources}
    ready=entry.get('ready_at_combat_turn')
    if type(ready) is not int or ready<0:
        return {'status':'UNKNOWN','reasons':['ready turn unknown'],'source_refs':sources}
    if ready>now:return {'status':'BLOCKED','reasons':['cooldown active'],'source_refs':sources}
    for resource,price in action_context.get('costs',{}).items():
        if type(price) is not int or price<0:raise ValueError('invalid known cost')
        amount=pre_state.get('resources',{}).get(resource)
        if isinstance(amount,dict):
            amount=amount.get('current')
        if type(amount) is not int:return {'status':'UNKNOWN','reasons':[f'{resource} unknown'],'source_refs':sources}
        if amount<price:return {'status':'BLOCKED','reasons':[f'{resource} insufficient'],'source_refs':sources}
    active_effects=pre_state.get('status_effects')
    if not isinstance(active_effects,dict):
        return {'status':'UNKNOWN','reasons':['status ledger missing'],'source_refs':sources}
    for name, effect in active_effects.items():
        if not isinstance(effect,dict) or not effect.get('source_ref'):
            return {'status':'UNKNOWN','reasons':[f'{name} status evidence missing'],'source_refs':sources}
        if effect.get('blocks_skills') is True:
            return {'status':'BLOCKED','reasons':[f'{name} blocks skills'],'source_refs':sources}
        if effect.get('blocks_skills') not in (False,None):
            return {'status':'UNKNOWN','reasons':[f'{name} skill restrictions unknown'],'source_refs':sources}
    return {'status':'READY','reasons':[],'source_refs':sources}
