# HẮC NHẬT Hybrid Lean V1 — Verification Ledger

Date: 2026-10-22. Status: **PARTIAL / NO-GO for complete acceptance** until full checkout/regression, qualitative GM evaluation, and comparable fast-response pilot.

## Observed locally
- Test-first isolated harness: missing-file/module RED for each main feature; RED actual assertion for malformed LOS, ordinary sword BLOOD edge, and duplicate effect receipt. GREEN after correction.
- `python -m unittest discover -s verification -p 'test_*.py' -v`: **34 tests, 0 failures, 0 errors** in isolated local workspace.
- 36 synthetic adversarial case inputs are algorithmically evaluated in two unittest methods: all comparison assertions passed. 12 combat, 12 tactical, 12 ledger. These are **not** 36 independent GM narrative responses.
- `python -m compileall -q story verification`: exit 0.
- 20 synthetic local helper calls: p50=0.0151 ms, p95=0.1878 ms, max=0.2956 ms. **NOT ChatGPT turn latency**; no comparable end-to-end FAST baseline.

## Critical limitations and final gate
- Local container had no DNS/egress to github.com; full original repository couldn't be cloned. Existing repository-wide tests **not run**, source integration with existing modules not proven. GitHub connector verified main HEAD `c74f77fe83fd490b85d8739be39056e0419331bb`, T345 state blob `a03e0bb288fa7bab4bb5147e00c78012edd36acc`, map blob `b6fd996a9778b52f8b3bf2d601edcae9ea0fc8c7`.
- This local suite uses a read-only manifest fixture for T345 rather than original whole current.json. That cannot prove actual integration/cold archive round trip. Re-verify exact SHA at GitHub update time.
- No 30+ actual independent GM narrative model responses; qualitative agency and hallucination review NOT_RUN.
- No true ChatGPT response-time pilot; speedup not claimed.
- No independent fresh reviewer: author self-review only. Independent ACCEPT cannot be claimed.
- Repo source was uploaded to isolated GitHub branch; do not fast-forward main until G2/G3/G4/review accepted or owner explicitly waives gates.

## Self-review findings already RED→GREEN
- Tactic dictionary mistakenly accepted wrong predicate vocabulary, e.g. target_visibility=ready -> ALLOWED. Fixed with predicate-specific enums.
- Combat engine tied ordinary sword BLOOD to actual HP loss despite canon only requiring valid landed ordinary hit. Fixed after RED, while Hấp Huyết remains tied to actual positive HP loss.
- Ledger initially allowed the same effect receipt ID across actions and replay with altered verification_refs. RED added and corrected.
- Ledger initially ignored invalid UNCHANGED resource pools and accepted an action_id inconsistent with its turn; RED→GREEN completed. Accepted receipt now includes rule_version.

## Deferred nonblocking limitations
- Source evidence tags and fictional NPC motives are still asserted by GM, not cryptographically verified by helpers.
- Public event RNG remains forecastable; no new hit/miss probabilities assigned.
- Pure helpers are not installed as automatic host hooks. Calling them manually for routine turns would incur tool overhead.
- Normal save cadence stays ten confirmed UNSAVED turns or material irreversible event.

## Suggested next gate
Run full checkout tests in an environment with repository access, collect true response-time and 30+ GM qualitative replay samples, review independent findings, only then decide on fast-forward main.
