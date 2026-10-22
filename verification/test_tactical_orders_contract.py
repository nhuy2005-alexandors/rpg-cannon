"""Static policy integrity test; it does NOT simulate the generative GM runtime."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

class TacticalOrdersContractTests(unittest.TestCase):
    def test_normative_contract(self):
        src = (ROOT / "canon/tactical-orders-v1.md").read_text(encoding="utf-8")
        for phrase in ("Tactical Orders & Autonomous Resolution V1.0",
                       "DECOMPOSE", "OBSERVE", "LEGALITY + TIME", "AUTONOMY",
                       "INTERLEAVE", "VERIFY + REPORT", "Intent != outcome",
                       "T345 remains saved / T346 unplayed",
                       "No fake hidden RNG", "FAST response"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), src.casefold())

    def test_authority_links(self):
        for path in ("canon/rules.md", "docs/gm-storyline-protocol.md"):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("canon/tactical-orders-v1.md", text)

    def test_adversarial_examples_are_unique_and_noncanon(self):
        content = json.loads((ROOT / "verification/tactical-orders-v1-scenarios.json")
                             .read_text(encoding="utf-8"))
        self.assertEqual(content["scope"], "NON_CANONICAL_SCENARIOS")
        self.assertEqual(len(content["cases"]), 10)
        ids = [c["id"] for c in content["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in content["cases"]:
            for k in ("given", "expected", "forbidden"):
                self.assertTrue(entry.get(k))

    def test_example_restricts_auto_success(self):
        items = json.loads((ROOT / "verification/tactical-orders-v1-scenarios.json")
                           .read_text(encoding="utf-8"))["cases"]
        self.assertIn("HOLD_OR_REPOSITION", [x["expected"] for x in items])
        self.assertIn("SHOT_IS_LEGAL_NOT_GUARANTEED", [x["expected"] for x in items])
        self.assertIn("NO_GAME_TURN", [x["expected"] for x in items])

if __name__ == "__main__":
    unittest.main()
