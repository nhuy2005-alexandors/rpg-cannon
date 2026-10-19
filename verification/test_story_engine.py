import json
import unittest
from pathlib import Path
from story.engine import validate_arc, transition, eligible_actions, checkpoint_needed, classify_discovery, checkpoint_integrity

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def fixtures():
    return load("story/arcs.json")["arcs"],load("story/actions.json")["actions"],load("state/current.json")

class TestStoryMechanics(unittest.TestCase):
    def test_seed_lifecycle_integrity(self):
        arcs,_,state=fixtures()
        self.assertEqual([],checkpoint_integrity(state,arcs))
        self.assertEqual(4,len(arcs))

    def test_old_boss_is_not_an_action(self):
        arcs,actions,state=fixtures()
        ids=[a["id"] for a in eligible_actions(arcs,actions,state)]
        self.assertNotIn("action:boss-wolf-king",ids)
        self.assertEqual(4,len(ids))

    def test_action_is_a_suggestion_not_accepted_quest(self):
        arcs,_,_=fixtures()
        self.assertTrue(all(a["player_commitment"]=="NONE" for a in arcs if a["status"]=="DISCOVERED"))

    def test_transition_requires_evidence(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[0],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":False})
        x=transition(arcs[0],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":True})
        self.assertEqual("ACTIVE",x["status"])

    def test_resolved_not_reopened_without_explicit_supersession(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[-1],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":True})

    def test_rumor_not_automatically_accepted(self):
        self.assertEqual("RUMORED",classify_discovery({"unique_thread_evidence":False}))
        self.assertEqual("DISCOVERED",classify_discovery({"unique_thread_evidence":True,"confirmed_outcome":True}))

    def test_checkpoint_turns_and_major_events(self):
        self.assertFalse(checkpoint_needed(4,set()))
        self.assertTrue(checkpoint_needed(5,set()))
        self.assertTrue(checkpoint_needed(1,{"ARC_CREATED"}))
        self.assertTrue(checkpoint_needed(0,set(),switching_chat=True))
        self.assertTrue(checkpoint_needed(0,set(),requested=True))
        with self.assertRaises(ValueError):checkpoint_needed(-1,set())

    def test_future_turn_snapshot_supported(self):
        arcs,_,state=fixtures()
        state=dict(state,last_completed_turn=154,next_turn=155)
        self.assertEqual([],checkpoint_integrity(state,arcs))

    def test_unknown_trama_dependency_rejected(self):
        arcs,_,_=fixtures()
        x=dict(arcs[0],dependencies=["arc:nonexistent"])
        self.assertTrue(validate_arc(x,{z["id"] for z in arcs}))

    def test_tram_tam_trao_requires_key(self):
        arcs,actions,state=fixtures()
        st=dict(state,base_storage=dict(state["base_storage"],TamTrao_key=0))
        ids=[a["id"] for a in eligible_actions(arcs,actions,st)]
        self.assertNotIn("action:plan-tam-trao",ids)

if __name__=="__main__": unittest.main()
