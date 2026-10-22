"""HN-WIE-V1: evidence-gated, deterministic world-event opportunities. No auto-loot or background hook."""
from __future__ import annotations
import hashlib
import json
from copy import deepcopy

PROFILES = {
    'safe': {'none': 8000, 'ambient': 1200, 'encounter': 600, 'hazard': 200},
    'dangerous': {'none': 5000, 'ambient': 2000, 'encounter': 2000, 'hazard': 1000},
}
FORTUNE_TIERS = {'ordinary': 7000, 'notable': 2300, 'rare': 600, 'exceptional': 100}
CATALOG = (
    {'id': 'passing_traces', 'category': 'ambient', 'requires': ('outdoors',)},
    {'id': 'weather_change', 'category': 'ambient', 'requires': ('outdoors', 'clouds')},
    {'id': 'distant_animal', 'category': 'ambient', 'requires': ('wildland',)},
    {'id': 'lost_purse', 'category': 'encounter', 'requires': ('inhabited_road',), 'fortune': True},
    {'id': 'trader_encounter', 'category': 'encounter', 'requires': ('trade_route',)},
    {'id': 'medicinal_herbs', 'category': 'encounter', 'requires': ('wildland',), 'fortune': True},
    {'id': 'lost_traveler', 'category': 'encounter', 'requires': ('inhabited_road',)},
    {'id': 'loose_stones', 'category': 'hazard', 'requires': ('rocky_path', 'unstable_rocks')},
    {'id': 'bandit_scout', 'category': 'hazard', 'requires': ('bandit_territory',)},
    {'id': 'strap_failure', 'category': 'hazard', 'requires': ('worn_strap', 'load_bearing')},
    {'id': 'pack_animal_startle', 'category': 'hazard', 'requires': ('pack_animal', 'sudden_noise')},
)

def _canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def _randbelow(seed, key, bound):
    if not isinstance(seed, str) or not seed or not isinstance(key, str) or not key:
        raise ValueError('seed and key required')
    if type(bound) is not int or not (1 <= bound <= 2**32):
        raise ValueError('invalid bound')
    sb = seed.encode('utf-8')
    limit = 2**32 - 2**32 % bound
    counter = 0
    while True:
        kb = f'{key}/{counter}'.encode('utf-8')
        message = (b'HN-WORLD-INCIDENTS-V1\0' + len(sb).to_bytes(4, 'big') + sb
                   + len(kb).to_bytes(4, 'big') + kb)
        number = int.from_bytes(hashlib.sha256(message).digest()[:4], 'big')
        if number < limit:
            return number % bound
        counter += 1

def _choose(roll, weights):
    total = 0
    for key, weight in weights.items():
        total += weight
        if roll < total:
            return key
    raise ValueError('weight table invalid')

def evaluate_world_opportunity(
    ledger: dict, *, seed: str, opportunity_id: str, turn: int, kind: str,
    zone: str, tags: dict[str, str], segment_id: str, elapsed_minutes: int
) -> dict:
    """Each unique physical opportunity rolls once; receipt is not a game consequence."""
    if not isinstance(ledger, dict):
        raise ValueError('ledger required')
    if not isinstance(opportunity_id, str) or not opportunity_id.strip():
        raise ValueError('opportunity ID required')
    if type(turn) is not int or turn < 346:
        raise ValueError('future-only activation from T346')
    if zone not in PROFILES or kind not in {'travel_segment', 'significant_time', 'equipment_stress'}:
        raise ValueError('unsupported opportunity')
    if not isinstance(segment_id, str) or not segment_id.strip():
        raise ValueError('physical segment required')
    if type(elapsed_minutes) is not int or elapsed_minutes < 0:
        raise ValueError('elapsed minutes invalid')
    if kind == 'significant_time' and elapsed_minutes < 30:
        raise ValueError('significant time requires >=30 verified minutes')
    if not isinstance(tags, dict) or any(not isinstance(k, str) or not k or
       not isinstance(v, str) or not v.strip() for k, v in tags.items()):
        raise ValueError('all tags require source evidence')
    if kind == 'equipment_stress' and not {'worn_strap', 'load_bearing'}.issubset(tags):
        raise ValueError('wear and load evidence required')
    context = {'opportunity_id': opportunity_id, 'turn': turn, 'kind': kind, 'zone': zone,
               'tags': tags, 'segment_id': segment_id, 'elapsed_minutes': elapsed_minutes,
               'seed': seed, 'version': 'HN-WORLD-INCIDENTS-V1'}
    fingerprint = hashlib.sha256(_canonical(context).encode('utf-8')).hexdigest()
    if opportunity_id in ledger:
        prior = ledger[opportunity_id]
        if prior.get('fingerprint') != fingerprint:
            raise ValueError('opportunity replay with changed preconditions')
        return deepcopy(prior)
    if any(v.get('turn') == turn and v.get('kind') == kind and
           v.get('segment_id') == segment_id for v in ledger.values()):
        raise ValueError('physical segment already evaluated under another ID')
    roll = _randbelow(seed, f'world/{opportunity_id}/category', 10000)
    proposed = _choose(roll, PROFILES[zone])
    options = sorted(x['id'] for x in CATALOG if x['category'] == proposed and
                     set(x['requires']).issubset(tags))
    chosen = None
    tier = None
    category = proposed if proposed == 'none' or options else 'none'
    if options:
        chosen = options[_randbelow(seed, f'world/{opportunity_id}/selection', len(options))]
        item = next(x for x in CATALOG if x['id'] == chosen)
        if item.get('fortune'):
            tier = _choose(_randbelow(seed, f'world/{opportunity_id}/fortune-tier', 10000), FORTUNE_TIERS)
    receipt = {'version': 'HN-WORLD-INCIDENTS-V1', 'opportunity_id': opportunity_id,
               'turn': turn, 'kind': kind, 'segment_id': segment_id, 'zone': zone,
               'category': category, 'gated_out_category': proposed if category != proposed else None,
               'roll': roll, 'incident_id': chosen, 'fortune_tier': tier,
               'fingerprint': fingerprint, 'auto_claim': False,
               'status': 'PROPOSED_NOT_ADJUDICATED',
               'note': 'No HP/loot/coins/inventory/hidden NPC changed by sampling'}
    ledger[opportunity_id] = deepcopy(receipt)
    return deepcopy(receipt)

def resolve_contest(ledger: dict, *, seed: str, action_id: str,
                    chance_basis_points: int | None, evidence: str) -> dict:
    """Optional explicit-odds draw; no default hit chance or automatic damage."""
    if not isinstance(ledger, dict) or not isinstance(action_id, str) or not action_id.strip():
        raise ValueError('ledger and unique action ID required')
    if type(chance_basis_points) is not int or not 0 <= chance_basis_points <= 10000:
        raise ValueError('separately approved hit chance required')
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError('evidence source required')
    fp = hashlib.sha256(_canonical({'seed': seed, 'action_id': action_id,
                   'chance': chance_basis_points, 'evidence': evidence}).encode('utf-8')).hexdigest()
    if action_id in ledger:
        prior = ledger[action_id]
        if prior.get('fingerprint') != fp:
            raise ValueError('same action cannot be rerolled with new chance')
        return deepcopy(prior)
    roll = _randbelow(seed, f'contest/{action_id}', 10000)
    receipt = {'version': 'HN-WORLD-INCIDENTS-V1', 'action_id': action_id,
               'chance_basis_points': chance_basis_points, 'roll': roll,
               'hit': roll < chance_basis_points, 'evidence': evidence,
               'fingerprint': fp, 'auto_damage': False,
               'status': 'DRAW_ONLY_NO_AUTOMATIC_DAMAGE'}
    ledger[action_id] = deepcopy(receipt)
    return deepcopy(receipt)
