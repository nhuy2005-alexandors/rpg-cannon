"""Synthetic-only boundary; live baseline is verified separately through GitHub connector."""
import unittest
class BaselineGuard(unittest.TestCase):
 def test_synthetic_boundary(self):
  fixture={'last_completed_turn':345,'next_turn':346,'HP':117,'STA':41,'BLOOD':46,'Souls':113,'EXP':380}
  self.assertEqual((fixture['last_completed_turn'],fixture['next_turn']),(345,346))
  self.assertEqual((fixture['HP'],fixture['STA'],fixture['BLOOD'],fixture['Souls'],fixture['EXP']),(117,41,46,113,380))
