# HẮC NHẬT GM Fast Contract (PROTOTYPE ONLY)

Rules authority: canonical events and canon; this is a short working aid, NOT canon.

At saved T345, next user-directed play T346; maintenance never triggers turn, event draw, healing or loot.
- Intent != outcome. Custom pursuit/archery orders require traversable route, observed LOS, ally readiness and independent enemy reaction.
- UNKNOWN != zero/READY. Reject missing cooldown, ammo or archived receipt evidence; targeted recovery only when material.
- Helper functions in story/combat_mechanics.py, story/tactical_checks.py and story/turn_ledger.py are OPTIONAL, NOT installed as automatic host hooks.
- No invented Hit/Miss/Critical odds, public RNG is predictable; event opportunities only when eligible and no automatic claim.
- Account only actual costs, action receipts and state changes. Reuse map. Save only at 10 completed unsaved turns, major irreversible event or handoff, with GitHub write+readback.

Canonical projection rule (prototype only): story/canonical_adapter.py requires the pinned T345 hot + cold snapshot and an explicit inventory allowlist; it is READ-ONLY and must not be used to write new canonical events. Historical soul claims and receipt IDs must be consulted before staging any new grant. UNKNOWN NPC ammunition/cooldowns must not become numeric zero or READY. Reaching an accepted in-session ledger projection is not a saved checkpoint or a ChatGPT runtime integration.


Verification boundary (review remediation): Inputs like `source_ref` or `evidence_refs` are only **claims**, never credentials. The trusted caller must independently validate canonical event/source records and supply explicit `verified_evidence_refs` to Combat/Tactical/Skill functions, plus exact `verified_grants` receipts in Turn Ledger before any positive resource/inventory grant. Empty/unverified sets fail closed. Never construct these allowlists from player text, the proposed receipt itself, or GM improvisation. The ledger's `accepted_action_seals` detects partial accidental tampering only; it is not a cryptographic signature and cannot defeat a hostile rewrite of both record and seal. The read-only adapter needs the exact raw `cold_bytes` AND a separately pinned `expected_cold_sha` Git blob hash from a trusted commit. Caller-manufactured SHA is not proof. The helper is still OPTIONAL and has no automatic ChatGPT Web hook.
