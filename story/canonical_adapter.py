"""Read-only, fail-closed projection from saved canonical Hac Nhat state.

This is not a canonical writer and deliberately never synthesizes an
accepted-action log from freeform historical narrative receipts.
"""
from __future__ import annotations

from copy import deepcopy
from state.compaction import restore_state


def project_canonical_state(hot: dict, cold: dict, *, inventory_keys: list[str]) -> dict:
    if not isinstance(hot, dict) or not isinstance(cold, dict):
        raise ValueError('both hot state and pinned cold archive required')
    if not isinstance(inventory_keys, list) or any(not isinstance(x, str) or not x for x in inventory_keys):
        raise ValueError('explicit inventory key list required')
    if len(set(inventory_keys)) != len(inventory_keys):
        raise ValueError('duplicate requested inventory key')
    archive = hot.get('_cold_archive')
    if not isinstance(archive, dict) or archive.get('schema') != 'HN-COLD-ARCHIVE-V1':
        raise ValueError('canonical cold archive reference required')
    pinned_turn = archive.get('turn')
    if type(pinned_turn) is not int or pinned_turn < 345 or archive.get('path') != f'state/archive/T{pinned_turn}-state-cold.json':
        raise ValueError('invalid versioned cold archive reference')
    if not isinstance(cold.get('source_state_blob_sha'), str) or not cold['source_state_blob_sha']:
        raise ValueError('cold archive provenance missing')
    full = restore_state(hot, cold)
    player = full.get('player')
    if not isinstance(player, dict):
        raise ValueError('canonical player unavailable')
    resources = player.get('resources')
    if not isinstance(resources, dict) or type(player.get('exp')) is not int:
        raise ValueError('canonical resource fields unavailable')
    out_resources = deepcopy(resources)
    out_resources['exp'] = player['exp']
    inventory = full.get('inventory')
    if not isinstance(inventory, dict):
        raise ValueError('canonical inventory unavailable')
    counts = {key: inventory[key] if key in inventory and type(inventory[key]) is int and inventory[key] >= 0 else 'UNKNOWN'
              for key in inventory_keys}
    claims = full.get('soul_loot', {}).get('first_loot_claims')
    if not isinstance(claims, dict):
        raise ValueError('canonical soul claim history unavailable')
    historical_claims = {}
    for target, receipt in claims.items():
        if not isinstance(target, str) or not isinstance(receipt, dict):
            raise ValueError('invalid historical claim')
        if receipt.get('claimed') is True:
            claim_id = receipt.get('claim_id')
            if not isinstance(claim_id, str) or not claim_id:
                raise ValueError('claimed reward lacks historical claim id')
            historical_claims[target] = claim_id
    old_receipts = full.get('receipts')
    if not isinstance(old_receipts, dict):
        raise ValueError('historical receipts unavailable')
    if not all(isinstance(k,str) for k in old_receipts):
        raise ValueError('non-string receipt identifier')
    return {'last_completed_turn':full['last_completed_turn'],
            'next_turn':full['next_turn'],
            'resources':out_resources,
            'inventory_counts':counts,
            'cooldowns':{}, 'status_effects':{}, 'accepted_actions':{},
            'historical_receipt_ids':sorted(old_receipts),
            'historical_claims':historical_claims,
            'canonical_history_verified':True,
            # Adapter cannot certify cooldown/status or NPC ammo from archival
            # prose; explicit narrow authoritative evidence is still required.
            'cooldowns_status':'UNKNOWN', 'npc_ammunition_status':'UNKNOWN'}
