import pathlib,unittest
class Contract(unittest.TestCase):
 def test_short_and_safe(self):
  s=(pathlib.Path(__file__).parents[1]/'state/gm-fast-contract.md').read_bytes()
  self.assertLessEqual(len(s),4096)
  for term in (b'UNKNOWN',b'T345',b'T346',b'OPTIONAL',b'10 completed'):
   self.assertIn(term,s)
