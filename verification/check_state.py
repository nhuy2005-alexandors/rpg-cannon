#!/usr/bin/env python3
import json
from pathlib import Path
s=json.loads((Path(__file__).resolve().parents[1]/"state/current.json").read_text(encoding="utf-8"))
a=s["player"]["resources"];t=s["receipts"]["T153"]
assert (s["last_completed_turn"],s["next_turn"])==(153,154)
assert tuple(a[k]["current"] for k in ["HP","STA","BLOOD","TuHuyet"])==(115,85,25,0)
assert a["souls"]==5
assert t["HP_before"]+5*12==t["HP_after"]==115
assert t["STA_before"]-5*5==t["STA_after"]==85
assert t["TuHuyet_before"]-5==t["TuHuyet_after"]==0
assert s["inventory"]["HuyetDuocQuanDung"]==2 and t["potions_spent"]==0
assert s["world_flags"]["tam_trao_tripwire"]=="BYPASSED_NOT_DISARMED"
assert len(s["npc_last_verified_T93"])==4 and s["world_flags"]["kharzug_distinct_from_dead_wolf"]
print("PASS: T153 resources, casts, NPCs and world flags")
