"""Lossless cold-archive split for HẮC NHẬT snapshots (no game action)."""
from copy import deepcopy
import re

HISTORICAL = re.compile(r"^(?:battle_state|scene_state)_T\d+$")
ALWAYS_HOT_FLAGS = frozenset({
    "cam_lao_gate", "tam_trao_tripwire", "boss_replay",
    "kharzug_distinct_from_dead_wolf", "blackclaw_quest_evidence_collected_pairs",
    "blackclaw_quest_evidence_submitted_pairs", "blackclaw_quest_reward_paid_T207",
    "hai_cot_lang_thang_accepted_T210",
})


def _turn(data):
    turn = data.get("last_completed_turn")
    if not isinstance(turn, int) or data.get("next_turn") != turn + 1:
        raise ValueError("snapshot turns must be sequential")
    return turn


def _ref(data, kind):
    turn = _turn(data)
    directory = "state" if kind == "state" else "maps"
    return {"schema": "HN-COLD-ARCHIVE-V1", "turn": turn,
            "path": f"{directory}/archive/T{turn}-{kind}-cold.json"}


def split_state(state):
    if "_cold_archive" in state:
        raise ValueError("already compacted: merge archive before another split")
    ref = _ref(state, "state")
    hot = deepcopy(state)
    cold = dict(ref)
    cold["receipts"] = hot.pop("receipts", {})
    hot["receipts"] = {}
    cold["historical"] = {}
    for key in list(hot):
        if HISTORICAL.match(key) and key != f"scene_state_T{ref['turn']}":
            cold["historical"][key] = hot.pop(key)
    flags = hot.get("world_flags", {})
    cold["world_flags"] = {}
    for key in list(flags):
        if key not in ALWAYS_HOT_FLAGS and key != f"ba_vach_northern_checkpoint_T{ref['turn']}":
            cold["world_flags"][key] = flags.pop(key)
    hot["_cold_archive"] = ref
    return hot, cold


def restore_state(hot, cold):
    _validate(hot, cold, "state")
    result = deepcopy(hot)
    del result["_cold_archive"]
    for key, value in cold["historical"].items():
        if key in result:
            raise ValueError(f"archive collision: {key}")
        result[key] = deepcopy(value)
    for name in ("receipts", "world_flags"):
        target = result[name]
        for key, value in cold[name].items():
            if key in target:
                raise ValueError(f"archive collision: {name}.{key}")
            target[key] = deepcopy(value)
    return result


def split_scene(scene):
    if "_cold_archive" in scene:
        raise ValueError("already compacted scene")
    ref = _ref(scene, "scene")
    hot = deepcopy(scene)
    cold = dict(ref)
    cold["historical"] = {}
    for key in list(hot):
        if key.startswith("archived_current_T") or key.startswith("inactive_scene_T") or key == "legacy_timeline":
            cold["historical"][key] = hot.pop(key)
    hot["_cold_archive"] = ref
    return hot, cold


def restore_scene(hot, cold):
    _validate(hot, cold, "scene")
    result = deepcopy(hot)
    del result["_cold_archive"]
    for key, value in cold["historical"].items():
        if key in result:
            raise ValueError(f"archive collision: {key}")
        result[key] = deepcopy(value)
    return result


def _validate(hot, cold, kind):
    if not isinstance(cold, dict):
        raise ValueError("cold archive is mandatory")
    ref = _ref(hot, kind)
    if hot.get("_cold_archive") != ref or any(cold.get(k) != v for k, v in ref.items()):
        raise ValueError("cold archive ref/turn mismatch")
    if not isinstance(cold.get("historical"), dict):
        raise ValueError("missing historical keys")
    if kind == "state" and (not isinstance(cold.get("receipts"), dict) or not isinstance(cold.get("world_flags"), dict)):
        raise ValueError("missing receipts or world flags archive")
