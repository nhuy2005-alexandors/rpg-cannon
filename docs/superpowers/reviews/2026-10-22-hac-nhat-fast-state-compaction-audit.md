# HẮC NHẬT FAST RESPONSE — Superpowers Root-Cause Audit & State Compaction V1

Date 2026-10-22. Baseline commit `be13a5aadcce938ed62e92de2a352a83ae696b83`. **Read-only-in-game maintenance, frozen T345, next T346**.

## Reproducible findings and root causes

1. **MAJOR — Quick Start bloat / stale restore.** Baseline `state/quick-start.md` length 95235 JS chars; concatenated historical T312, T302, older T194 guidance. Contains mutually incompatible latest turn claims. Cause: append-in-place of prior quickstarts. Fix: archive byte-preserving original text; overwrite active quick-start with <=8KB T345-only current summary. Never append stale snapshots again.
2. **MAJOR — Historical data in current numerical snapshot.** Baseline `state/current.json` 228225 JS chars, 19 historical scene/battle fields, 122 receipt records, 29 long-lived historical flags. Cause: append-only event storage mixed with hot current state. Fix: stable explicit cold archive, hot current ~98771 chars. No lore/equipment/reward rewritten; full reconstructed deep equal to baseline.
3. **MAJOR — README conflicting pointer.** README at baseline claims latest T204 while live state is T345. Fixed header and explicit historical disclaimer. Do not rewrite every historical paragraph as current.
4. **MINOR — Scene overlay growth.** Baseline `maps/active-scene.json` 17419 chars and 7 historical overlay items. Fix archive historical only; hot scene ~3718 chars, preserve current tokens, static atlas immutable.
5. **MAJOR — Restore contract gap.** Neither a verified cold reference nor fail-closed restore check existed. Fix `state/compaction.py`, `verification/test_state_compaction.py`, archive metadata with source Git blob identity. Missing or wrong turn archive causes ValueError. Future archive re-compaction must rehydrate before re-splitting; never silently replace archives.

## Verification receipts and limitations

- **Red**: pre-change four problem probes failed, observed quickstart 95235>8192, README T204, 19 historical hot entries, 7 map archived hot entries.
- **TDD synthetic Python**: 5 tests saw expected import failure before production module, then 5/5 PASS using standard Python unittest in isolated sandbox. These tests must be re-run from a full GitHub checkout after commit; not claiming full repository suite PASS.
- **Live full snapshot JS structural check**: reconstructed hot+cold equals original source state (deep canonical equality), and scene hot+cold equals original scene; frozen HP117 STA41 BLOOD46 Souls113 EXP380, T345→T346 preserved. No NPCs deleted and no Quest payout/claim changed.
- Source baseline blobs: current JSON `e68f58ecfcf86666168b2a55ea8e21418d3dee3f`, scene `207708280dbce4a1b47684248fdf3c18ef01a68d`. Immutable GitHub parent `be13a5aadcce938ed62e92de2a352a83ae696b83` remains recovery fallback.
- Risk accepted: consumers directly accessing older `state.current.receipts.T###` or historical `world_flags` MUST call restore_state or targeted archive retrieval. Existing T153 `verification/check_state.py` is a historical fixture and already fails against later live states; it is not modern runtime verifier.
- No new runtime daemon, vector database, scheduled sync, agent loop, rules change, monetary transaction or T346 action.

## Success criteria

`state/quick-start.md` <= 8KB; hot state <= 120KB; hot scene <= 5KB (JS char approximation); source-to-restore deep-equality; no historic duplicate loot or deleted world flags; target next T346; target map ID unchanged; existing static atlas untouched; isolated branch commit/readback and Git tree receipt. Whole-suite Python tests require normal checkout with network or a locally mounted repository and remain a separate gate.

## Follow-up defect closed: future-turn archive validation

RED reproducer in isolated Python test: after `split_state(T345)`, advance hot `last_completed_turn=346,next_turn=347` without changing pinned archive ref T345. Previously `restore_state(hot,cold)` incorrectly recomputed expected archive path using live turn T346 and raised `ValueError: cold archive ref/turn mismatch`. Exact same bug affected scene rehydration. FIX: validation now checks the immutable archive's **pinned** turn and path, requires pinned turn <= live turn and rejects missing/wrong/tampered refs. Python regression: **6/6 PASS** (5 existing + 1 future-turn case) with `python -m unittest discover -s verification -p test_state_compaction.py -v`. The game's actual T346 remains NOT PLAYED; fixture is a simulated test only.
