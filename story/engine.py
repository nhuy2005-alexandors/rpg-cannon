"""Game Master story lifecycle, suggestion filtering and checkpoint triggers.
Pure functions; no Notion/GitHub background synchronization."""
from __future__ import annotations

ALLOWED = {"RUMORED","DISCOVERED","AVAILABLE","ACTIVE","BLOCKED","RESOLVED","FAILED","SUPERSEDED"}
TRANSITIONS = {
 "RUMORED":{"DISCOVERED","SUPERSEDED"},
 "DISCOVERED":{"AVAILABLE","ACTIVE","BLOCKED","RESOLVED","SUPERSEDED"},
 "AVAILABLE":{"ACTIVE","BLOCKED","RESOLVED","SUPERSEDED"},
 "ACTIVE":{"BLOCKED","RESOLVED","FAILED","SUPERSEDED"},
 "BLOCKED":{"AVAILABLE","ACTIVE","FAILED","RESOLVED","SUPERSEDED"},
 "RESOLVED":set(),
 "FAILED":set(),
 "SUPERSEDED":set(),
}
MAJOR_EVENTS={"NPC_DEATH","NPC_RECRUITMENT","NPC_DEPARTURE","QUEST_ACCEPTED","QUEST_RESOLVED","ARC_CREATED","ARC_RESOLVED","FACTION_CHANGED","LOCATION_DISCOVERED","WORLD_FLAG_CHANGED","IRREVERSIBLE_CHOICE"}

def validate_arc(arc: dict, known_ids: set[str]) -> list[str]:
    errors=[]
    if not arc.get("id","").startswith("arc:"):errors.append("bad arc id")
    if arc.get("status") not in ALLOWED:errors.append("invalid status")
    if not arc.get("source"):errors.append("missing provenance")
    if arc.get("last_evidence_turn",0)>153 and arc.get("as_of_turn",153)<=153:errors.append("future turn without current evidence")
    if arc.get("status")=="RESOLVED" and arc.get("next_action_ids"):errors.append("resolved arc has open actions")
    for dep in arc.get("dependencies",[]):
        if dep not in known_ids:errors.append("unknown arc dependency")
    if arc.get("player_commitment")=="COMPLETED" and arc.get("status")!="RESOLVED":errors.append("commitment/state contradiction")
    return errors

def transition(arc: dict, new_status: str, event: dict) -> dict:
    old=arc["status"]
    if new_status not in TRANSITIONS.get(old,set()):raise ValueError(f"illegal lifecycle {old}->{new_status}")
    if not event.get("source") or not isinstance(event.get("turn"),int):raise ValueError("transition requires verified turn/source")
    if event.get("outcome_verified") is not True:raise ValueError("user request alone is not confirmed outcome")
    updated=dict(arc,status=new_status,last_evidence_turn=event["turn"])
    return updated

def eligible_actions(arcs: list[dict], actions: list[dict], state: dict) -> list[dict]:
    by_id={x["id"]:x for x in arcs}
    location=state["location"]
    storage=state["base_storage"]
    choices=[]
    for a in actions:
        arc=by_id.get(a["arc_id"])
        if arc is None or arc["status"] in {"RESOLVED","FAILED","SUPERSEDED","BLOCKED"}:continue
        if a["id"] not in arc.get("next_action_ids",[]):continue
        requirements=a.get("requires",[])
        if "location:dien-te-huyet" in requirements and "Điện Tế Huyết" not in location:continue
        if "base_storage.TamTrao_map>=1" in requirements and storage.get("TamTrao_map",0)<1:continue
        if "base_storage.TamTrao_key>=1" in requirements and storage.get("TamTrao_key",0)<1:continue
        choices.append(a)
    return choices

def checkpoint_needed(turns_since_flush: int, event_types: set[str], switching_chat: bool=False, requested: bool=False) -> bool:
    if turns_since_flush < 0:raise ValueError("negative turn count")
    return turns_since_flush>=5 or bool(MAJOR_EVENTS & event_types) or switching_chat or requested

def classify_discovery(event: dict) -> str:
    """A mention is not an accepted quest or verified arc."""
    if event.get("confirmed_outcome") and event.get("unique_thread_evidence"):return "DISCOVERED"
    return "RUMORED"

def checkpoint_integrity(state: dict, arcs: list[dict]) -> list[str]:
    errors=[]
    if state["last_completed_turn"]!=153 or state["next_turn"]!=154:
        errors.append("current accepted snapshot changed")
    ids={x["id"] for x in arcs}
    if len(ids)!=len(arcs):errors.append("duplicate arcs")
    for arc in arcs:errors.extend(validate_arc(arc,ids))
    if any(x["id"]=="arc:wolf-king-hunt" and x["status"]!="RESOLVED" for x in arcs):errors.append("wolf boss should remain resolved")
    return errors
