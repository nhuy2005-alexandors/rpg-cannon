import json
import unittest
from pathlib import Path
from verification.graph_validation import validate_seed, diff_projection, IncompleteLookup, projection_changed

ROOT=Path(__file__).resolve().parents[1]
def fixtures():
    e=json.loads((ROOT/'graph/seed/entities.json').read_text(encoding='utf-8'))
    r=json.loads((ROOT/'graph/seed/relationships.json').read_text(encoding='utf-8'))
    return e,r

class GraphValidationTests(unittest.TestCase):
    def test_valid_seed(self):
        entities,edges=fixtures()
        self.assertEqual([], validate_seed(entities,edges))
        self.assertEqual(9,len(entities))
        self.assertEqual(7,len(edges))

    def test_last_seen_not_current(self):
        _, edges=fixtures()
        x=[r for r in edges if r['predicate']=='LOCATED_AT_LAST_SEEN']
        self.assertEqual(2,len(x))
        for edge in x:
            self.assertEqual(93,edge['last_verified_turn'])
            self.assertEqual('LAST_VERIFIED',edge['evidence_quality'])
            self.assertNotIn('current_location',edge)
            self.assertNotIn('now',edge['lifecycle'].lower())

    def test_kharzug_distinct_from_one_eyed_wolf(self):
        entities,_=fixtures()
        d={e['canonical_id']:e for e in entities}
        self.assertEqual('INJURED',d['npc:kharzug']['life_world_status'])
        self.assertEqual(93,d['npc:kharzug']['last_verified_turn'])
        self.assertEqual('DECEASED',d['npc:huyet-lang-doc-nhan']['life_world_status'])
        self.assertEqual(66,d['npc:huyet-lang-doc-nhan']['last_verified_turn'])

    def test_duplicate_entities_and_edges_fail(self):
        e,r=fixtures()
        self.assertTrue(any('duplicate' in x for x in validate_seed(e+[e[0]],r)))
        self.assertTrue(any('duplicate' in x for x in validate_seed(e,r+[r[0]])))

    def test_dangling_endpoint_fails(self):
        e,r=fixtures(); copy=[dict(x) for x in r]; copy[0]['to_id']='npc:missing'
        self.assertTrue(any('unknown endpoint' in x for x in validate_seed(e,copy)))

    def test_missing_evidence_fails(self):
        e,r=fixtures(); copy=[dict(x) for x in r];copy[0]['github_evidence']=''
        self.assertTrue(any('evidence' in x for x in validate_seed(e,copy)))

    def test_repeat_upsert_zero_creates(self):
        e,r=fixtures()
        got=diff_projection(e,[dict(x) for x in e],'canonical_id',complete=True)
        self.assertEqual(0,len(got['create']))
        self.assertEqual(9,len(got['unchanged']))
        self.assertFalse(got['duplicate'])
        got2=diff_projection(r,[dict(x) for x in r],'edge_id',complete=True)
        self.assertEqual(0,len(got2['create']))

    def test_incomplete_lookup_fails_closed(self):
        e,_=fixtures()
        with self.assertRaises(IncompleteLookup):
            diff_projection(e,[],'canonical_id',complete=False)

    def test_notion_escaped_edge_id_reimport_has_no_create(self):
        e,edges=fixtures()
        fetched=[{"Edge ID":r["edge_id"].replace("|",r"\|")} for r in edges]
        result=diff_projection(edges,fetched,"edge_id",complete=True)
        self.assertEqual([],result["create"])
        self.assertFalse(result["duplicate"])

    def test_notion_entity_titlecase_id_reimport_has_no_create(self):
        e,_=fixtures()
        fetched=[{"Canonical ID":r["canonical_id"]} for r in e]
        result=diff_projection(e,fetched,"canonical_id",complete=True)
        self.assertEqual(0,len(result["create"]))
        self.assertFalse(result["duplicate"])

    def test_partial_failure_no_marker_advance(self):
        from verification.graph_validation import may_advance_marker
        self.assertFalse(may_advance_marker(7,6,True))
        self.assertFalse(may_advance_marker(7,7,False))
        self.assertTrue(may_advance_marker(7,7,True))

    def test_docs_only_commit_not_dirty(self):
        self.assertFalse(projection_changed(['README.md','docs/storage-protocol.md'],set()))
        self.assertTrue(projection_changed(['canon/npc/kharzug.md'],set()))

    def test_hp_only_checkpoint_not_graph_dirty(self):
        self.assertFalse(projection_changed(['state/current.json'],{'player.resources.HP.current'}))
        self.assertTrue(projection_changed(['state/current.json'],{'npc_last_verified_T93'}))

    def test_stale_endpoint_blocks_edge(self):
        e,r=fixtures();copy=[dict(x) for x in r]; copy[0]['to_id']='npc:renamed'
        self.assertTrue(validate_seed(e,copy))

    def test_unknown_current_npc_presence_not_inferred(self):
        e,_=fixtures()
        for x in e:
            if x['kind']=='NPC' and x['canonical_id']!='npc:huyet-lang-doc-nhan':
                self.assertLessEqual(x['last_verified_turn'],93)
                self.assertNotIn('T153: present',x['summary'])

if __name__ == '__main__': unittest.main()
