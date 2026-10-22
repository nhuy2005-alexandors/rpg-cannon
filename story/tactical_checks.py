"""Grounded feasibility checks. This module does NOT simulate movement or choose NPC intentions."""
from __future__ import annotations

VERBS={'shoot','pursue','reposition','interact'}


def check_tactical(intent: dict, observed_world: dict) -> dict:
    if not isinstance(intent,dict) or not isinstance(observed_world,dict) or not isinstance(intent.get('substeps'),list):
        raise ValueError('structured declared intent and observed world required')
    if not isinstance(intent.get('source_ref'),str) or not intent['source_ref'] or type(intent.get('turn')) is not int:
        raise ValueError('source and turn required')
    observations=observed_world.get('substeps',{})
    if not isinstance(observations,dict):raise ValueError('observations must be keyed by substep')
    results=[]
    seen=set()
    for step in intent['substeps']:
        if not isinstance(step,dict) or not all(isinstance(step.get(k),str) and step[k] for k in ('id','actor','verb','target')):
            raise ValueError('each substep requires fixed ID/actor/verb/target')
        ident=step['id']
        if ident in seen:raise ValueError('duplicate substep ID')
        seen.add(ident)
        e=observations.get(ident,{})
        refs=e.get('evidence_refs') if isinstance(e,dict) else None
        notes=[]
        if not isinstance(refs,list) or not refs or any(not isinstance(s,str) or not s for s in refs):
            disposition='UNKNOWN';notes.append('SOURCE_EVIDENCE_MISSING')
        elif step['verb'] not in VERBS:
            disposition='UNKNOWN';notes.append('UNKNOWN_VERB')
        else:
            pred=[]
            def chk(name):
                v=e.get(name,'unknown')
                allowed={'target_visibility':{'visible','last_seen','unknown'},'los':{'clear','blocked','unknown'},'crossfire':{'clear','blocked','unknown'},'route':{'traversable','blocked','unknown'},'actor_ready':{'ready','blocked','unknown'}}[name]
                if v not in allowed:
                    pred.append('UNKNOWN_'+name); return 'unknown'
                if v in ('blocked',):pred.append('BLOCKED_'+name)
                elif v in ('unknown',None):pred.append('UNKNOWN_'+name)
                elif v not in ('ready','clear','visible','last_seen','traversable'):
                    pred.append('UNKNOWN_'+name)
                return v
            verb=step['verb']
            if verb=='shoot':
                vis=chk('target_visibility');chk('los');chk('crossfire');chk('actor_ready')
                if vis=='last_seen':pred.append('BLOCKED_NO_CURRENT_TARGET')
            elif verb=='pursue':
                vis=chk('target_visibility');chk('route');chk('actor_ready')
                if vis=='last_seen':pred.append('CONDITIONAL_SEARCH_REQUIRED')
            elif verb in ('reposition','interact'):
                chk('route');chk('actor_ready')
            notes=pred
            disposition=('BLOCKED' if any(x.startswith('BLOCKED') for x in pred)
                         else 'UNKNOWN' if any(x.startswith('UNKNOWN') for x in pred)
                         else 'CONDITIONAL' if any(x.startswith('CONDITIONAL') for x in pred)
                         else 'ALLOWED')
        results.append({'id':ident,'disposition':disposition,'reasons':notes,
                        'evidence_refs':list(refs) if isinstance(refs,list) else [],
                        'possible_reaction_window':step['verb'] in VERBS})
    return {'overall':'BLOCKED' if results and all(x['disposition']=='BLOCKED' for x in results)
            else 'UNKNOWN' if any(x['disposition']=='UNKNOWN' for x in results)
            else 'CONDITIONAL' if any(x['disposition'] in ('BLOCKED','CONDITIONAL') for x in results)
            else 'ALLOWED',
            'substeps':results,
            'unresolved':[x['id'] for x in results if x['disposition'] in ('UNKNOWN','CONDITIONAL')]}
