"""Pure, idempotent session projection; not a durable checkpoint service."""
import copy
import hashlib
import json

def _hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def _int(v):
    if type(v) is not int:raise ValueError('exact integer required')
    return v

def stage_turn(pre_state:dict,intended_turn:dict,proposed_deltas:dict,receipts:list[dict], *, replay_commitment:str|None=None)->dict:
    original=copy.deepcopy(pre_state)
    original.setdefault('accepted_action_seals', {})
    ident=intended_turn.get('action_id')
    if not isinstance(ident,str) or not ident or not intended_turn.get('evidence_refs') or not intended_turn.get('rule_version'):
        raise ValueError('immutable action id and evidence required')
    if not isinstance(receipts, list) or not isinstance(proposed_deltas, dict):
        raise ValueError('receipts and deltas must have expected types')
    permitted={'resource_changes','inventory_changes','cooldown_changes','status_changes','elapsed_minutes'}
    if set(proposed_deltas)-permitted:
        raise ValueError('unsupported delta field')
    history=original.get('accepted_actions',{})
    if not isinstance(history,dict):raise ValueError('accepted actions ledger missing')
    # This detects a partial/accidental edit, not an attacker changing both seal and record.
    seals=original.get('accepted_action_seals', {})
    if not isinstance(seals,dict):raise ValueError('accepted action seal index missing')
    for action_id, entry in history.items():
        if seals.get(action_id) != _hash(entry):
            raise ValueError('tampered or unsealed accepted action')
    receipt_ids=set()
    previous_ids={r.get('receipt_id') for action in history.values()
                  if isinstance(action,dict) for r in action.get('input_receipts',[])
                  if isinstance(r,dict)}
    claims_this_turn=set()
    targets_this_turn=set()
    for item in receipts:
        if not isinstance(item,dict) or not isinstance(item.get('receipt_id'),str) or not item['receipt_id']:
            raise ValueError('a receipt requires immutable receipt_id')
        rid=item['receipt_id']
        if rid in receipt_ids:raise ValueError('duplicate receipt in one turn')
        receipt_ids.add(rid)
        cid=item.get('claim_id');target=item.get('claim_target_id')
        if cid and target:
            claim_key=(cid,item.get('kind'),item.get('resource'))
            target_key=(target,item.get('kind'),item.get('resource'))
            if claim_key in claims_this_turn or target_key in targets_this_turn:
                raise ValueError('duplicate reward claim inside one turn')
            claims_this_turn.add(claim_key);targets_this_turn.add(target_key)
    input_fp=_hash({'intent':intended_turn,'delta':proposed_deltas,'receipts':receipts})
    if ident in history:
        prior=history[ident]
        # The immutable commitment must come from outside the mutable state.
        if (not isinstance(replay_commitment,str) or replay_commitment != _hash(prior)):
            raise ValueError('missing or mismatched external replay commitment')
        if prior['input_fingerprint'] != input_fp:raise ValueError('conflicting replay')
        # The stored post-action projection excludes the receipt itself; it must
        # be identical on replay or the caller has supplied a drifted state.
        replay_projection=copy.deepcopy(original)
        replay_projection['accepted_actions'].pop(ident)
        replay_projection['accepted_action_seals'].pop(ident)
        if prior.get('post_projection_digest') != _hash(replay_projection):
            raise ValueError('replay against changed post-action state')
        return {'status':'REPLAY','input_fingerprint':input_fp,'projected_post_state':original,
                'prior_receipt':copy.deepcopy(prior),'intended_turn':copy.deepcopy(intended_turn),'delta':copy.deepcopy(proposed_deltas)}
    if receipt_ids & previous_ids:
        raise ValueError('reused historical receipt ID')
    if original.get('canonical_history_verified') is True:
        prior_ids = original.get('historical_receipt_ids')
        prior_claims = original.get('historical_claims')
        if not isinstance(prior_ids, list) or not isinstance(prior_claims, dict):
            raise ValueError('canonical history evidence missing')
        if receipt_ids & set(prior_ids):
            raise ValueError('reused canonical historical receipt ID')
        accepted_claim_ids = set()
        accepted_claim_targets = set()
        for previous in history.values():
            if not isinstance(previous, dict):
                raise ValueError('invalid prior accepted action')
            for entry in previous.get('input_receipts', []):
                if isinstance(entry, dict):
                    if entry.get('claim_id'):
                        accepted_claim_ids.add(entry['claim_id'])
                    if entry.get('claim_target_id'):
                        accepted_claim_targets.add(entry['claim_target_id'])
        for item in receipts:
            cid = item.get('claim_id')
            target = item.get('claim_target_id')
            if cid is not None and (not isinstance(cid, str) or not cid):
                raise ValueError('invalid claim identifier')
            if target is not None and (not isinstance(target,str) or not target):
                raise ValueError('invalid claim target')
            if cid and (cid in prior_claims.values() or cid in accepted_claim_ids):
                raise ValueError('reused canonical historical claim ID')
            if target and (target in prior_claims or target in accepted_claim_targets):
                raise ValueError('canonical target already looted')
            if item.get('kind') == 'RESOURCE_GRANT' and item.get('resource') == 'souls':
                if not cid or not target:
                    raise ValueError('canonical soul grant requires claim ID and target ID')
    # Grants must be prevalidated by a separate authoritative caller.
    # Proposed action/receipt must never manufacture this allowlist.
    grants=original.get('verified_grants', {})
    if not isinstance(grants,dict):raise ValueError('verified grant registry missing')
    def require_grants(kind, resource, expected):
        if expected<=0:return
        matching=[r for r in receipts if r.get('kind')==kind and r.get('resource')==resource
                  and r.get('action_id')==ident and type(r.get('amount')) is int and r['amount']>0]
        if sum(r['amount'] for r in matching)!=expected or not matching:
            raise ValueError('missing or mismatched positive grant receipt')
        for item in matching:
            if grants.get(item['receipt_id']) != item:
                raise ValueError('grant source not independently verified')
    for key,change in proposed_deltas.get('resource_changes',{}).items():
        _int(change)
        require_grants('RESOURCE_GRANT', key, change)
    for key,change in proposed_deltas.get('inventory_changes',{}).items():
        _int(change)
        require_grants('INVENTORY_GRANT', key, change)
    turn=_int(intended_turn.get('turn'))
    if turn!=original.get('next_turn') or turn!=original.get('last_completed_turn',-100)+1:
        raise ValueError('nonsequential turn')
    projected=copy.deepcopy(original)
    for key,change in proposed_deltas.get('resource_changes',{}).items():
        _int(change)
        if change > 0:
            sources=[r for r in receipts if r.get('kind')=='RESOURCE_GRANT'
                     and r.get('resource')==key and r.get('action_id')==ident
                     and isinstance(r.get('source_ref'),str) and r['source_ref']]
            if not sources or sum(r.get('amount',0) for r in sources)!=change or any(type(r.get('amount')) is not int or r['amount']<=0 for r in sources):
                raise ValueError('positive resource delta requires matching evidence receipt')
        record=projected['resources'].get(key)
        if isinstance(record,dict):
            current=_int(record['current'])+change
            limit=_int(record['max'])
            if not 0<=current<=limit:raise ValueError('resource over/underflow')
            record['current']=current
        elif type(record) is int:
            value=record+change
            if value<0:raise ValueError('resource underflow')
            projected['resources'][key]=value
        else:raise ValueError('unknown resource')
    for item,change in proposed_deltas.get('inventory_changes',{}).items():
        _int(change)
        old=projected['inventory_counts'].get(item)
        if type(old) is not int:raise ValueError('unknown inventory quantity')
        if old+change<0:raise ValueError('inventory underflow')
        projected['inventory_counts'][item]=old+change
    for field,target in (('cooldown_changes','cooldowns'),('status_changes','status_effects')):
        for key,value in proposed_deltas.get(field,{}).items():
            if (not isinstance(value,dict) or not isinstance(value.get('source_ref'),str) or
                value['source_ref'] not in original.get('verified_evidence_refs', [])):
                raise ValueError('effect requires independently verified source')
            if field=='status_changes' and not value.get('expires_when'):
                raise ValueError('effect expiration contract missing')
            projected[target][key]=copy.deepcopy(value)
    if _int(proposed_deltas.get('elapsed_minutes',0))<0:raise ValueError('negative time')
    projected['last_completed_turn']=turn
    projected['next_turn']=turn+1
    return {'trusted_observation_refs':copy.deepcopy(original.get('verified_evidence_refs', [])),
            'status':'STAGED','input_fingerprint':input_fp,'projected_post_state':projected,
            'pre_state_digest':_hash(original),'intended_turn':copy.deepcopy(intended_turn),
            'delta':copy.deepcopy(proposed_deltas),'receipts':copy.deepcopy(receipts)}

def accept_turn(staged:dict,confirmed_result:dict)->dict:
    if staged.get('status')!='STAGED' or confirmed_result.get('confirmed') is not True or confirmed_result.get('action_id')!=staged['intended_turn']['action_id']:
        raise ValueError('confirmed matching staged action required')
    trusted=staged.get('trusted_observation_refs', [])
    refs=confirmed_result.get('verification_refs', [])
    if (not isinstance(trusted,list) or not isinstance(refs,list) or not refs or
        any(not isinstance(r,str) or not r or r not in trusted for r in refs)):
        raise ValueError('confirmed outcome evidence was not independently verified')
    out=copy.deepcopy(staged['projected_post_state'])
    aid=staged['intended_turn']['action_id']
    receipt={'action_id':aid,'turn':staged['intended_turn']['turn'],'rule_version':staged['intended_turn']['rule_version'],
             'input_fingerprint':staged['input_fingerprint'],'pre_state_digest':staged['pre_state_digest'],
             'disposition':confirmed_result['disposition'],'observed_outcome':confirmed_result['observed_outcome'],
             'resource_deltas':copy.deepcopy(staged['delta']),'input_receipts':copy.deepcopy(staged['receipts']),
             'verification_refs':confirmed_result['verification_refs'],
             'post_projection_digest':_hash(staged['projected_post_state']),
             'verification_status':'ACCEPTED_IN_SESSION_NOT_SAVED'}
    out['accepted_actions'][aid]=receipt
    out.setdefault('accepted_action_seals', {})[aid]=_hash(receipt)
    return {'post_state':out,'compact_delta':copy.deepcopy(staged['delta']),
            'accepted_receipt':receipt,'acceptance_commitment':_hash(receipt)}
