import json
import unittest
from pathlib import Path
from story.engine import validate_arc, transition, eligible_actions, checkpoint_needed, classify_discovery, checkpoint_integrity, post_turn
from verification.graph_validation import projection_changed

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
        self.assertEqual(3,len(ids))  # unverified inventory action must be hidden

    def test_action_is_a_suggestion_not_accepted_quest(self):
        arcs,_,_=fixtures()
        self.assertTrue(all(a["player_commitment"]=="NONE" for a in arcs if a["status"]=="DISCOVERED"))

    def test_transition_requires_evidence(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[0],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":False})
        x=transition(arcs[0],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":True,"player_committed":True})
        self.assertEqual("ACTIVE",x["status"])

    def test_resolved_not_reopened_without_explicit_supersession(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[-1],"ACTIVE",{"turn":154,"source":"events/0154.md","outcome_verified":True})

    def test_rumor_not_automatically_accepted(self):
        self.assertEqual("RUMORED",classify_discovery({"unique_thread_evidence":False}))
        self.assertEqual("DISCOVERED",classify_discovery({"unique_thread_evidence":True,"confirmed_outcome":True}))

    def test_checkpoint_turns_and_major_events(self):
        for turn_count in range(10):
            with self.subTest(turns_since_flush=turn_count):
                self.assertFalse(checkpoint_needed(turn_count,set()))
        self.assertTrue(checkpoint_needed(10,set()))
        self.assertTrue(checkpoint_needed(11,set()))
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

    def test_unknown_requirement_fails_closed(self):
        arcs,actions,state=fixtures()
        fake=dict(actions[0],requires=["unrecognized.cooldown<=0"])
        self.assertEqual([],eligible_actions(arcs,[fake],state))

    def test_malformed_requirement_fails_closed(self):
        arcs,actions,state=fixtures()
        fake=dict(actions[0],requires=[{"unsupported":"condition"}])
        self.assertEqual([],eligible_actions(arcs,[fake],state))

    def test_unconfirmed_item_action_hidden(self):
        arcs,actions,state=fixtures()
        self.assertNotIn("action:review-sealed-vessel",[a["id"] for a in eligible_actions(arcs,actions,state)])

    def test_active_requires_player_commitment(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[0],"ACTIVE",{"turn":155,"source":"events/0155.md","outcome_verified":True})

    def test_transition_rejects_historical_turn(self):
        arcs,_,_=fixtures()
        with self.assertRaises(ValueError):
            transition(arcs[0],"AVAILABLE",{"turn":153,"source":"events/0153.md","outcome_verified":True})

    def test_resolved_arc_clears_stale_actions(self):
        arcs,_,_=fixtures()
        done=transition(arcs[0],"RESOLVED",{"turn":156,"source":"events/0156.md","outcome_verified":True})
        self.assertEqual([],done["next_action_ids"])

    def test_post_turn_rumor_no_checkpoint(self):
        result=post_turn({"confirmed":True,"event_types":set(),"unique_thread_evidence":False,
                          "turns_since_flush":1,"changed_paths":["events/0157.md"],"state_changed_fields":set()})
        self.assertFalse(result["arc_review"])
        self.assertFalse(result["checkpoint_due"])
        self.assertFalse(result["notion_projection_due"])

    def test_post_turn_discovery_flushes_but_not_notions_graph(self):
        result=post_turn({"confirmed":True,"event_types":set(),"unique_thread_evidence":True,
                          "turns_since_flush":1,"changed_paths":["events/0157.md"],"state_changed_fields":set()})
        self.assertTrue(result["arc_review"])
        self.assertTrue(result["checkpoint_due"])
        self.assertFalse(result["notion_projection_due"])

    def test_post_turn_npc_relation_triggers_changed_only_projection(self):
        result=post_turn({"confirmed":True,"event_types":{"NPC_RELATION_CHANGED"},
                          "turns_since_flush":1,"changed_paths":["events/0157.md"],"state_changed_fields":set()})
        self.assertTrue(result["checkpoint_due"])
        self.assertTrue(result["notion_projection_due"])

    def test_unconfirmed_turn_never_plans_persistence(self):
        with self.assertRaises(ValueError):
            post_turn({"confirmed":False,"event_types":{"NPC_DEATH"},"turns_since_flush":5})

if __name__=="__main__": unittest.main()
