import unittest
from story.tactical_checks import check_tactical


def fixture(verb='shoot', **facts):
    base=dict(target_visibility='visible',los='clear',crossfire='clear',route='traversable',actor_ready='ready',evidence_refs=['noncanon/map','noncanon/event'])
    base.update(facts)
    return ({'source_ref':'noncanon/order','turn':346,'substeps':[{'id':'s1','actor':'Maela','verb':verb,'target':'A'}]}, {'substeps':{'s1':base}})

class TacticalTests(unittest.TestCase):
    def test_target_last_seen_blocks_shot(self):
        a,b=fixture(target_visibility='last_seen',los='blocked')
        x=check_tactical(a,b)['substeps'][0]
        self.assertEqual(x['disposition'],'BLOCKED')
        self.assertNotIn('hit',x)

    def test_clear_shot_is_legal_not_guaranteed_hit(self):
        a,b=fixture()
        x=check_tactical(a,b)['substeps'][0]
        self.assertEqual(x['disposition'],'ALLOWED')
        self.assertNotIn('damage',x)
        self.assertTrue(x['possible_reaction_window'])

    def test_crossfire_blocks_and_unknown_ammo_fails_closed(self):
        a,b=fixture(crossfire='blocked')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'BLOCKED')
        a,b=fixture(actor_ready='unknown')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')

    def test_compound_chase_allows_conditional_and_blocked_ally(self):
        a,b=fixture()
        a['substeps']=[{'id':'s1','actor':'Vô Danh','verb':'pursue','target':'A'},{'id':'s2','actor':'Maela','verb':'shoot','target':'A'}]
        b={'substeps':{'s1':dict(target_visibility='last_seen',route='traversable',actor_ready='ready',evidence_refs=['noncanon/map']),
                       's2':dict(target_visibility='last_seen',los='blocked',crossfire='clear',actor_ready='ready',evidence_refs=['noncanon/map'])}}
        x=check_tactical(a,b)
        self.assertEqual([k['disposition'] for k in x['substeps']],['CONDITIONAL','BLOCKED'])
        self.assertNotIn('enemy_killed',x)

    def test_malformed_predicate_cannot_legalize_shot(self):
        a,b=fixture(target_visibility='ready')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')
        a,b=fixture(los='visible')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')

    def test_missing_predicate_unknown_and_no_coordinates(self):
        a,b=fixture(los='unknown')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')
        a,b=fixture('teleport')
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')
        a,b=fixture(evidence_refs=[])
        self.assertEqual(check_tactical(a,b)['substeps'][0]['disposition'],'UNKNOWN')

if __name__=='__main__':unittest.main()
