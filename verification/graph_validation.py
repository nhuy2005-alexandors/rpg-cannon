"""Pure, dependency-free schema and projection guards for Hắc Nhật."""
from collections import Counter

KINDS={'PLAYER','NPC','LOCATION','FACTION','QUEST','ITEM'}
LIFE={'ALIVE','INJURED','DECEASED','UNKNOWN','ACTIVE','CLOSED'}
QUALITY={'CONFIRMED','LAST_VERIFIED','PARTIAL','UNKNOWN','SUPERSEDED'}
PREDICATES={'MENTORS','COMBAT_ALLY_OF','RESCUED','PROTECTS','FOUND','LOCATED_AT_LAST_SEEN','ASSOCIATED_WITH','GUARDED','KILLED'}
LIFECYCLE={'LAST_VERIFIED','ONGOING_CONFIRMED','ENDED','SUPERSEDED','UNKNOWN'}

class IncompleteLookup(ValueError):
    """Fail closed: provider results may be truncated, so absence is unproved."""

def validate_seed(entities: list[dict], relationships: list[dict]) -> list[str]:
    errors=[]
    entity_ids=[e.get('canonical_id') for e in entities]
    for k,c in Counter(entity_ids).items():
        if not k or c!=1:errors.append(f'duplicate or absent canonical_id: {k}')
    known=set(entity_ids)
    for i,e in enumerate(entities):
        key=e.get('canonical_id')
        if e.get('kind') not in KINDS:errors.append(f'entity {i} invalid kind')
        if e.get('life_world_status') not in LIFE:errors.append(f'entity {i} invalid status')
        if e.get('evidence_quality') not in QUALITY:errors.append(f'entity {i} invalid evidence quality')
        if not isinstance(e.get('last_verified_turn'),int) or e['last_verified_turn']>153:errors.append(f'entity {i} invalid last turn')
        if not e.get('github_source'):errors.append(f'entity {i} missing evidence source')
        if not key or ':' not in key:errors.append(f'entity {i} invalid ID')
    edge_ids=[r.get('edge_id') for r in relationships]
    for k,c in Counter(edge_ids).items():
        if not k or c!=1:errors.append(f'duplicate or absent edge_id: {k}')
    for i,r in enumerate(relationships):
        a,b,p=r.get('from_id'),r.get('to_id'),r.get('predicate')
        if a not in known or b not in known:errors.append(f'edge {i} unknown endpoint')
        if p not in PREDICATES:errors.append(f'edge {i} unknown predicate')
        if r.get('evidence_quality') not in QUALITY:errors.append(f'edge {i} invalid evidence quality')
        if r.get('lifecycle') not in LIFECYCLE:errors.append(f'edge {i} invalid lifecycle')
        s,t=r.get('first_verified_turn'),r.get('last_verified_turn')
        if not isinstance(s,int) or not isinstance(t,int) or s>t or t>153:errors.append(f'edge {i} invalid turn interval')
        if not r.get('github_evidence'):errors.append(f'edge {i} missing evidence')
        expected_range=f'T{s}' if s==t else f'T{s}-T{t}'
        if r.get('edge_id')!=f'{a}|{p}|{b}|{expected_range}':errors.append(f'edge {i} id does not match source')
        if p=='LOCATED_AT_LAST_SEEN' and (r.get('evidence_quality')!='LAST_VERIFIED' or r.get('lifecycle')!='LAST_VERIFIED'):
            errors.append(f'edge {i} last-seen wrongly current')
    return errors

def diff_projection(desired: list[dict], fetched: list[dict], key: str, complete: bool) -> dict[str, list[dict]]:
    if not complete:raise IncompleteLookup('Incomplete query coverage; no new creates permitted')
    records={};dupes=[]
    notion_labels={'canonical_id':'Canonical ID','edge_id':'Edge ID'}
    def lookup_id(row):
        value=row.get(key, row.get(notion_labels.get(key,'')))
        if key=='edge_id' and isinstance(value,str):
            value=value.replace('\\|','|')
        return value
    for x in fetched:
        k=lookup_id(x)
        if not k or k in records:dupes.append(x)
        else:records[k]=x
    out={'create':[],'update':[],'unchanged':[],'duplicate':dupes}
    if dupes:return out
    for x in desired:
        k=lookup_id(x)
        if k not in records:out['create'].append(x)
        elif x==records[k]:out['unchanged'].append(x)
        else:out['update'].append(x)
    return out

def projection_changed(changed_paths: list[str], state_changed_fields: set[str]) -> bool:
    if any(p.startswith(('canon/','events/','graph/seed/')) for p in changed_paths):return True
    if 'state/current.json' in changed_paths:
        return any(not field.startswith(('player.resources.HP.','player.resources.STA.','player.resources.BLOOD.','player.resources.TuHuyet.')) for field in state_changed_fields)
    return False

def may_advance_marker(expected_count: int, verified_count: int, all_valid: bool) -> bool:
    return all_valid and verified_count==expected_count
