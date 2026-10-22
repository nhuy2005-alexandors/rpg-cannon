"""Non-simulating tactical legality from externally evidenced categorical observations."""

def check_tactical(intent: dict, observed_world: dict) -> dict:
    trusted=observed_world.get('verified_evidence_refs', [])
    if not isinstance(trusted,(list,tuple,set)):
        trusted=[]
    result=[]
    for step in intent.get('substeps',[]):
        sid=step['id'];verb=step['verb'];facts=observed_world.get('substeps',{}).get(sid,{})
        evidence=facts.get('evidence_refs',[])
        status='UNKNOWN';reasons=[]
        if verb not in {'pursue','shoot','reposition','interact'}:
            reasons=['unknown verb']
        elif not evidence or not isinstance(evidence,list) or not set(evidence).issubset(set(trusted)):
            reasons=['missing observation evidence']
        else:
            ready=facts.get('actor_ready','unknown')
            visibility=facts.get('target_visibility','unknown')
            route=facts.get('route','unknown')
            los=facts.get('los','unknown')
            crossfire=facts.get('crossfire','unknown')
            if ready=='blocked':status='BLOCKED';reasons=['actor unavailable']
            elif ready!='ready':reasons=['readiness unknown']
            elif verb=='shoot':
                if los=='blocked' or crossfire=='blocked':status='BLOCKED';reasons=['no safe lane']
                elif visibility=='last_seen':status='BLOCKED';reasons=['target not visible']
                elif visibility=='visible' and los=='clear' and crossfire=='clear':
                    ammo=facts.get('ammo','unknown')
                    if ammo=='available':status='ALLOWED'
                    elif ammo=='empty':status='BLOCKED';reasons=['no ammunition']
                    else:reasons=['ammunition unknown']
                else:reasons=['target or line unknown']
            elif verb in {'pursue','reposition'}:
                if route=='blocked':status='BLOCKED';reasons=['path blocked']
                elif route=='traversable' and visibility=='last_seen':status='CONDITIONAL';reasons=['target last seen; search required']
                elif route=='traversable':status='ALLOWED' if visibility=='visible' else 'CONDITIONAL'
                else:reasons=['route unknown']
            else:
                status='CONDITIONAL';reasons=['interaction needs narrative adjudication']
        result.append({'id':sid,'disposition':status,'reasons':reasons,'evidence_refs':evidence,
                       'possible_reaction_window':verb in {'pursue','reposition','interact'}})
    kinds={r['disposition'] for r in result}
    overall='BLOCKED' if kinds=={'BLOCKED'} else 'UNKNOWN' if not result else 'CONDITIONAL' if ('CONDITIONAL' in kinds or len(kinds)>1) else result[0]['disposition']
    return {'overall':overall,'substeps':result,'unresolved':[r['id'] for r in result if r['disposition'] in ('UNKNOWN','CONDITIONAL')]}
