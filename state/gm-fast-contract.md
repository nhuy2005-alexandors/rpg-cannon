# HẮC NHẬT GM Fast Contract (PROTOTYPE ONLY)

Rules authority: canonical events and canon; this is a short working aid, NOT canon.

At saved T345, next user-directed play T346; maintenance never triggers turn, event draw, healing or loot.
- Intent != outcome. Custom pursuit/archery orders require traversable route, observed LOS, ally readiness and independent enemy reaction.
- UNKNOWN != zero/READY. Reject missing cooldown, ammo or archived receipt evidence; targeted recovery only when material.
- Helper functions in story/combat_mechanics.py, story/tactical_checks.py and story/turn_ledger.py are OPTIONAL, NOT installed as automatic host hooks.
- No invented Hit/Miss/Critical odds, public RNG is predictable; event opportunities only when eligible and no automatic claim.
- Account only actual costs, action receipts and state changes. Reuse map. Save only at 10 completed unsaved turns, major irreversible event or handoff, with GitHub write+readback.

Canonical projection rule (prototype only): story/canonical_adapter.py requires the pinned T345 hot + cold snapshot and an explicit inventory allowlist; it is READ-ONLY and must not be used to write new canonical events. Historical soul claims and receipt IDs must be consulted before staging any new grant. UNKNOWN NPC ammunition/cooldowns must not become numeric zero or READY. Reaching an accepted in-session ledger projection is not a saved checkpoint or a ChatGPT runtime integration.
