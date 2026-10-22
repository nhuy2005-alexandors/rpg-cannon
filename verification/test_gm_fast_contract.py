import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

class FastContractTests(unittest.TestCase):
    def test_bounded_bytes_and_authority(self):
        p=ROOT/'state/gm-fast-contract.md'
        content=p.read_bytes()
        self.assertLessEqual(len(content),4096)
        t=content.decode('utf-8')
        for word in ('T345','T346','UNKNOWN','intent','outcome','Maela','GitHub','10','public seed'):
            with self.subTest(word=word):self.assertIn(word.casefold(),t.casefold())
        self.assertIn('optional',t)
        self.assertIn('NOT an automatically installed',t)

    def test_short_fast_contract_not_new_canon(self):
        s=(ROOT/'state/gm-fast-contract.md').read_text()
        self.assertIn('summary only',s)
        self.assertIn('no game turn',s)

if __name__=='__main__':unittest.main()
