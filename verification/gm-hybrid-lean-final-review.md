# GM Hybrid Lean — pre-merge audit, 2026-10-22

Status: **NO-GO MAIN MERGE**. Source remains a local candidate.

## Confirmed GitHub baseline
- main HEAD: `c74f77fe83fd490b85d8739be39056e0419331bb` (fresh connector readback).
- `story/combat_mechanics.py`, `story/tactical_checks.py`, `story/turn_ledger.py`, and `state/gm-fast-contract.md` are ABSENT from main. No main mutation executed.
- T345 last saved; T346 unplayed per existing repository. This candidate does not edit state/current.json, map or events.

## Focused review fixes (verified RED then GREEN)
- DR-01 CRITICAL: same action replay after HP state drift silently returned REPLAY. Fixed with post-projection digest check; regression `test_replay_after_modified_hp_is_rejected`.
- DR-02 IMPORTANT: active stun status did not block skill use. Fixed source-aware skill-blocking status test.
- DR-03 IMPORTANT: Maela could shoot with unknown ammunition count. Fixed tri-state shooting eligibility; unknown ammo => UNKNOWN, explicit available => legal attempt only.
- DR-04 IMPORTANT: known structured STA resource `{current, max}` yielded UNKNOWN. Fixed check_skill_availability resource adapter for known projected reservoirs.
- DR-05 CRITICAL: positive Souls could be awarded without a source receipt. Fixed evidence receipt requirement for positive resource deltas.
- DR-06 CRITICAL: same receipt could grant Souls again under a new action ID. Fixed one-time input receipt IDs across in-session accepted_actions. Historical cold-archive linkage still needs review before real integration.

## Local verification
- Command: `cd /mnt/data/hac-gm && python -m unittest discover -s verification -p 'test_*.py' -v`
- **23 unique tests, 0 failures, 0 errors** after correcting duplicate imported TestCase discovery. Existing original baseline draft had 16 tests, and seven unique adversarial tests were added.
- This is NOT the HẮC NHẬT repository-wide suite. The original baseline archive and canonical state are not present in this candidate; synthetic tests alone do not establish G0/G2 PASS.
- The 36 scenario records are fixtures, not 36 executed GM responses. No end-to-end FAST latency pilot, independent reviewer, or combined full-suite verification.

## Blockers to user-authorized merge
- G0/G2: A full GitHub repository checkout is unavailable to this execution environment (`git ls-remote` fails due to DNS for github.com). A real repository full-suite run is required.
- G3: 36 synthetic GM behavior probes need real execution and review; fixture structure is not behavioral proof.
- G4: 20-turn representative ChatGPT runtime pilot p50/p95 and tool-call counts not measured.
- G5: independent review and repository branch commit/readback not yet obtained.

## Safe next action
Maintain this as an isolated candidate. Do not merge to main or claim ChatGPT runtime hooks have been installed. For deployment, obtain a repository checkout on a machine with GitHub access; run `python -m unittest discover -s verification -p 'test_*.py' -v`, run behavioral/FAST pilot and independent review, then fast-forward merge using expected head SHA after green receipts.
