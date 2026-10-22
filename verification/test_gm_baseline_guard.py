import json
import unittest
from pathlib import Path

FROZEN = Path(__file__).parent / 'fixtures' / 'T345-frozen.json'

class FrozenContinuity(unittest.TestCase):
    def test_frozen_canonical_receipt(self):
        x=json.loads(FROZEN.read_text())
        self.assertEqual((x['last_completed_turn'],x['next_turn']),(345,346))
        self.assertEqual(x['resources'],{'HP':[117,170],'STA':[41,110],'BLOOD':[46,50],'TuHuyet':[0,20],'souls':113,'exp':380})
        self.assertEqual(x['state_blob'],'a03e0bb288fa7bab4bb5147e00c78012edd36acc')
        self.assertEqual(x['scene_blob'],'b6fd996a9778b52f8b3bf2d601edcae9ea0fc8c7')
        self.assertEqual(x['map_id'],'doc-da-xam-ba-vach-escort-second-bend')

    def test_hot_receipt_omission_is_not_absence(self):
        x=json.loads(FROZEN.read_text())
        self.assertEqual(x['cold_archive_ref'],'state/archive/T345-state-cold.json')
        self.assertEqual(x['cold_archive_presence'],'VERIFIED_REFERENCE_ONLY')
