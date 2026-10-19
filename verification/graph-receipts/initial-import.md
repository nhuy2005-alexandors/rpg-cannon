# Hắc Nhật Notion Knowledge Graph V1 — Initial Import Verification Receipt

**Review class:** Self-verified by Native implementation; not an independent code review.  
**Date:** 2026-10-19  
**Authoritative source:** https://github.com/nhuy2005-alexandors/rpg-cannon (`main`, public per owner's explicit approval).  
**Projected source SHA:** `c47ba6254b042f016f8f53aafb2af346173674e4` (seed + unchanged T153 canon).  
**Readback on GitHub after projection:** later documentation/validation commits do not imply a new gameplay projection.  
**Notion Hub:** https://app.notion.com/p/3fe864d295ce817895aed0bcfde6ac34  
**Entities:** https://app.notion.com/p/3e1a70d007444496874d9e9535071d6a, `collection://6f40f9fb-1bb7-48b9-9c84-a8f8bff91579`.  
**Relationships:** https://app.notion.com/p/4ea8c07ae96d4312b585acab207bc370, `collection://b3eeb1ac-138f-4dab-b7ad-6b63321f2b86`.

## Verification gates and receipts

| Gate | Result | Evidence |
| --- | --- | --- |
| G0 canonical invariants | PASS | GitHub `state/current.json` freshly fetched T153, next T154, HP115/170, STA85/110, BLOOD25/50, Tử Huyết0/20, souls5; `BYPASSED_NOT_DISARMED`; no RPG turn created. |
| G1 Notion schemas | PASS | Two data sources created under same existing Hub; Entities 9 fields, Relationships 12 fields; native `From` and `To` relation properties both target Entities data source. Both originally empty with `has_more=false`. |
| G2 entity and edge import | PASS | 9 Entities + 7 Relationships, all unique canonical IDs/edge IDs. Full saved-view scans returned 9 and 7, `has_more=false`, source SHA on every row. Fetched all seven edge pages individually, correct predicate, From/To cardinality one, directions and sources. |
| G3 temporal fidelity | PASS | Kharzug INJURED and alive last seen T93, Huyết Lang Độc Nhãn DECEASED T66 (different IDs), pup alive T93; no assertion of T153 NPC presence or biological kinship. |
| G4 actual Notion queries | PASS WITH LIMITATION | SQL `From LIKE ?` Kharzug yielded PROTECTS + last-seen, `To LIKE ?` yielded RESCUED. Saved view Kharzug Outbound returned 2, Inbound 1; Temple LAST SEEN returned Edran and Kharzug T93 (2), all `has_more=false`. Rows-mode `relation_contains` silently returned all 7 and **must NOT be trusted**; SQL/Rows allowance was then exhausted, saved-view mode remained usable. |
| G5 repeat/recovery contract | PASS AT OFFLINE/READBACK SCOPE | Re-query through saved views found 9 unique Entities + 7 unique Edges, 0 missing, 0 duplicates, so rerun would create 0 IDs. Python `unittest`: **17 tests PASS**, including Notion `\\|` normalization and simulated partial-batch marker gating. No fault-injected live API outage or autonomous projector service was tested or installed. |
| G6 fast path | PROCEDURAL PASS | No required Notion read/write on routine combat reply. Checkpoint triggers documented as at most 5 turns, major events and session boundary; manual active-session tools only. **Not a timed background sync guarantee.** |
| G7 Hub cutover | PASS | Hub title now `HẮC NHẬT — Knowledge Graph (LIVE · T153)`, links to two actual child databases, source SHA and canon; obsolete private-only migration blocker removed from current instructions. Fetched after edit, preserved two `<database>` child blocks. |

## Exact saved-view readbacks

- Entity Explorer: `view://3fe864d2-95ce-8116-9ad7-000c62f533e1` — 9 rows, no more.
- Relationship Explorer: `view://3fe864d2-95ce-810d-8c5c-000c3621bfb9` — 7 rows, no more.
- Temple LAST SEEN: `view://3fe864d2-95ce-81e1-abc2-000cbcede468` — 2 rows (Edran/Kharzug at T93).
- Kharzug Outbound: `view://3fe864d2-95ce-81f7-bf1e-000c4512af16` — 2 rows (PROTECTS pup, LAST_SEEN temple).
- Kharzug Inbound: `view://3fe864d2-95ce-81f2-8064-000ce0741e17` — 1 row (Vô Danh RESCUED Kharzug).

## TDD and provider integration notes

1. RED: `python -m unittest verification.test_graph_validation -v` initially errored because `verification.graph_validation` had not been implemented; then GREEN: 13 tests passed after seed/validator implementation.
2. RED: two new Notion-property key normalization tests failed against raw title-case and escaped pipes, then GREEN: local suite passed 15/15; later future-turn bound and negative-turn tests witnessed RED and then GREEN, final local suite **17/17**. GitHub version of validator and test suite was updated and each written file read back byte-for-byte.
3. SQL/Rows Notion MCP plan-limited quota reached after real reads; provider explicitly stated view mode still worked, verified using five saved views. Queries with `relation_contains` returned unfiltered data: post-filter or saved view required.
4. Last valid Hub projected source SHA `c47ba6...` refers to the graph seed source, not HEAD after later documentation commits. Upstream game checkpoint and historical source copies unchanged.
5. No adversarial failure of the remote Notion connector or scheduled ingest service tested. The graph is usable for manual/connector reads now, not continuously self-synchronizing.

## Recovery

If a future checkpoint changes gameplay: commit GitHub first; identify canon graph deltas; upsert by stable `Canonical ID`/`Edge ID`; verify row properties and directions; only then advance Hub source SHA. A failed Notion write leaves GitHub valid, and the Hub projected source marker must remain the last verified one. On rate-limit failure, use saved views and/or GitHub `canon/` directly. Never fill NPC presence gaps from a stale index.
