"""Pure in-session turn staging and exactly-once receipts. Not persistent storage."""
from __future__ import annotations
import hashlib
import json
import re
from copy import deepcopy


def _hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def _without_accepts(value):
    out=deepcopy(value)
    out.pop('accepted_actions',None)
    return out


def _signed_int(value):
    if type(value) is not int:raise ValueError('delta must be exact integer')
    return value


def stage_turn(pre_state:dict,intended_turn:dict,proposed_deltas:dict,receipts:list[dict])->dict:
    if not all(isinstance(x,dict) for x in (pre_state,intended_turn,proposed_deltas)) or not isinstance(receipts,list):
        raise ValueError('structured turn inputs required')
    action=intended_turn.get('action_id')
    turn=intended_turn.get('turn')
    if not isinstance(action,str) or not action or type(turn) is not int or turn < 346 or not isinstance(intended_turn.get('rule_version'),str):
        raise ValueError('action/turn/rules required')
    if not re.fullmatch(rf'T{turn}/A[0-9]+', action):
        raise ValueError('action ID must match requested turn')
    refs=intended_turn.get('evidence_refs')
    if not isinstance(refs,list) or not refs or any(not isinstance(r,str) or not r for r in refs):
        raise ValueError('source references required')
    if any(not isinstance(r,dict) or not r.get('source_ref') or not isinstance(r.get('id'),str) or not r['id'] for r in receipts):
        raise ValueError('receipt sources required')
    pools=pre_state.get('resources')
    if not isinstance(pools,dict):raise ValueError('resource snapshot required')
    for key,pool in pools.items():
        if isinstance(pool,dict):
            value,cap=pool.get('current'),pool.get('max')
            if type(value) is not int or type(cap) is not int or cap<0 or not 0<=value<=cap:
                raise ValueError('invalid prior resource pool '+str(key))
        elif key in ('souls','exp'):
            if type(pool) is not int or pool<0:raise ValueError('invalid prior resource '+key)
        else:raise ValueError('invalid unknown resource '+str(key))
    ids=[r['id'] for r in receipts]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate effect receipt in action')
    request_fp=_hash({'intent':intended_turn,'deltas':proposed_deltas,'receipts':receipts})
    pre_digest=_hash(_without_accepts(pre_state))
    accepted=pre_state.get('accepted_actions',{})
    if not isinstance(accepted,dict):raise ValueError('accepted receipt ledger invalid')
    prior_ids={k for r in accepted.values() if isinstance(r,dict) for k in r.get('effect_ids',[])}
    if action not in accepted and any(k in prior_ids for k in ids):
        raise ValueError('previously claimed effect receipt reused by another action')
    if action in accepted:
        prior=accepted[action]
        if (prior.get('request_fingerprint')!=request_fp or pre_digest not in
            (prior.get('pre_state_digest'),prior.get('post_state_digest'))):
            raise ValueError('conflicting action replay')
        return {'status':'REPLAY','saved_receipt':deepcopy(prior),'post_state':deepcopy(pre_state),
                'action_id':action,'turn':turn}
    if pre_state.get('next_turn') != turn or pre_state.get('last_completed_turn') != turn-1:
        raise ValueError('nonsequential or duplicated turn')
    for field in ('resource_changes','inventory_changes','cooldown_changes','status_changes'):
        if not isinstance(proposed_deltas.get(field),dict):raise ValueError('missing delta map '+field)
    elapsed=proposed_deltas.get('elapsed_minutes')
    if type(elapsed) is not int or elapsed < 0:raise ValueError('invalid elapsed time')
    post=deepcopy(pre_state)
    for key,change in proposed_deltas['resource_changes'].items():
        change=_signed_int(change)
        pool=post.get('resources',{}).get(key)
        if isinstance(pool,dict):
            current, cap=pool.get('current'),pool.get('max')
            if type(current) is not int or type(cap) is not int or not 0<=current<=cap:
                raise ValueError('unknown/invalid resource pool '+key)
            result=current+change
            if not 0<=result<=cap:raise ValueError('resource out of range '+key)
            pool['current']=result
        elif key in ('souls','exp'):
            if type(pool) is not int or pool+change<0:raise ValueError('unknown/depleted '+key)
            post['resources'][key]=pool+change
        else:raise ValueError('unknown resource '+key)
        if change>0 and not receipts:
            raise ValueError('positive resource delta needs evidence receipt')
    for key,change in proposed_deltas['inventory_changes'].items():
        change=_signed_int(change)
        current=post.get('inventory_counts',{}).get(key)
        if type(current) is not int or current+change<0:
            raise ValueError('unknown or insufficient inventory '+key)
        if change>0 and not receipts:raise ValueError('new inventory requires receipt')
        post['inventory_counts'][key]=current+change
    for key,item in proposed_deltas['cooldown_changes'].items():
        if not isinstance(item,dict) or type(item.get('ready_at_combat_turn')) is not int or not item.get('source_ref'):
            raise ValueError('cooldown change lacks accepted source/clock')
        post.setdefault('cooldowns',{})[key]=deepcopy(item)
    for key,item in proposed_deltas['status_changes'].items():
        if not isinstance(item,dict) or not item.get('source_ref') or not item.get('expiration'):
            raise ValueError('status change lacks source/expiration contract')
        post.setdefault('status_effects',{})[key]=deepcopy(item)
    claims=proposed_deltas.get('unique_claim_ids',[])
    if not isinstance(claims,list) or len(claims)!=len(set(claims)) or any(not isinstance(c,str) or not c for c in claims):
        raise ValueError('invalid unique claim IDs')
    if claims and (not receipts or pre_state.get('historical_claim_coverage')=='ARCHIVED_UNVERIFIED'):
        raise ValueError('claim sources/archived coverage unresolved')
    for claim_id in claims:
        if claim_id in post.setdefault('claims',{}):raise ValueError('duplicate unique claim '+claim_id)
        post['claims'][claim_id]={'claim_action':action,'source_refs':list(refs)}
    post['last_completed_turn']=turn
    post['next_turn']=turn+1
    post_digest=_hash(_without_accepts(post))
    compact={'turn':turn,'action_id':action,'disposition':'PENDING','deltas':deepcopy(proposed_deltas),
             'evidence_refs':list(refs),'elapsed_minutes':elapsed}
    return {'status':'STAGED','action_id':action,'turn':turn,'request_fingerprint':request_fp,
            'pre_state_digest':pre_digest,'post_state_digest':post_digest,
            'projected_post_state':post,'delta':compact,'evidence_refs':list(refs),
            'receipts':deepcopy(receipts),'effect_ids':list(ids),
            'rule_version':intended_turn['rule_version']}


def accept_turn(staged:dict,confirmed_result:dict)->dict:
    if not isinstance(staged,dict) or not isinstance(confirmed_result,dict) or confirmed_result.get('confirmed') is not True or confirmed_result.get('action_id')!=staged.get('action_id'):
        raise ValueError('explicit matching confirmation required')
    if staged.get('status')=='REPLAY':
        old=staged['saved_receipt']
        if (confirmed_result.get('disposition') != old['compact_delta']['disposition']
            or confirmed_result.get('observed_outcome') != old['compact_delta']['observed_outcome']
            or confirmed_result.get('verification_refs') != old['accepted_receipt']['verification_refs']):
            raise ValueError('replayed confirmation contradicts accepted event')
        return {'post_state':deepcopy(staged['post_state']), 'compact_delta':deepcopy(old['compact_delta']),
                'accepted_receipt':deepcopy(old['accepted_receipt'])}
    if staged.get('status')!='STAGED':raise ValueError('unresolved staged turn')
    if confirmed_result.get('disposition') not in ('SUCCESS','PARTIAL','FAILED','BLOCKED','UNKNOWN') or not confirmed_result.get('observed_outcome'):
        raise ValueError('resolution requires actual disposition')
    refs=confirmed_result.get('verification_refs')
    if not isinstance(refs,list) or not refs:raise ValueError('confirmed evidence required')
    post=deepcopy(staged['projected_post_state'])
    delta=deepcopy(staged['delta'])
    delta.update({'disposition':confirmed_result['disposition'],'observed_outcome':confirmed_result['observed_outcome']})
    receipt={'kind':'GM_TURN_V1','action_id':staged['action_id'],'turn':staged['turn'],
             'pre_state_digest':staged['pre_state_digest'],'post_state_digest':staged['post_state_digest'],
             'request_fingerprint':staged['request_fingerprint'],
             'rule_version':staged['rule_version'],'verification_refs':list(refs),
             'verification_status':'CONFIRMED_IN_SESSION_NOT_SAVED'}
    post.setdefault('accepted_actions',{})[staged['action_id']]={
      'request_fingerprint':staged['request_fingerprint'],'pre_state_digest':staged['pre_state_digest'],
      'post_state_digest':staged['post_state_digest'],'effect_ids':list(staged['effect_ids']),
      'compact_delta':deepcopy(delta),
      'accepted_receipt':deepcopy(receipt)}
    return {'post_state':post,'compact_delta':delta,'accepted_receipt':receipt}
