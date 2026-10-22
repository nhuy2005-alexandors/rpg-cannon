import unittest,json,pathlib
class ScenarioFixtures(unittest.TestCase):
 def test_36_distinct_noncanonical_cases(self):
  doc=json.loads((pathlib.Path(__file__).parents[0]/'gm_reliability_scenarios.json').read_text())
  self.assertEqual(doc['scope'],'NON_CANONICAL');self.assertEqual(len(doc['cases']),36)
  self.assertEqual(len({x['id'] for x in doc['cases']}),36)
  self.assertEqual({g:sum(x['group']==g for x in doc['cases']) for g in ('combat','tactics','ledger')},{'combat':12,'tactics':12,'ledger':12})
  for x in doc['cases']:
   self.assertTrue(x['expected']);self.assertTrue(x['forbidden']);self.assertTrue(x['preconditions'])
