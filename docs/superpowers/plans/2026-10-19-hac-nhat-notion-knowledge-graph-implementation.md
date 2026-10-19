# Hắc Nhật Notion Knowledge Graph V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy two linked Notion databases for evidence-backed Hắc Nhật entities and relationships, while preserving GitHub as sole gameplay canon and keeping ordinary RPG turns fast.

**Architecture:** GitHub `main` owns `state/current.json`, historical events, NPC canon and deterministic seed data. Notion Entities and Relationships are read-optimized derived projections. At a checkpoint: commit canonical deltas first, validate and upsert Notion rows, verify readback, then advance the Hub sync marker; failure never transfers authority away from GitHub.

**Tech Stack:** Connected GitHub and Notion tools, Markdown/UTF-8 JSON, Python 3.10+ stdlib `unittest` for pure validation/dry-run logic; no paid Notion AI Search, background worker, secrets or new external service.

**Spec:** `docs/superpowers/specs/2026-10-19-hac-nhat-notion-knowledge-graph-design.md`

## Global Constraints

- Owner chose **B: Entities + Relationships** and approved the written design spec in chat on 2026-10-19. This **implementation plan is NOT yet approved**; no schema/data implementation before plan approval and execution-method selection.
- Repository: `nhuy2005-alexandors/rpg-cannon` (public with explicit owner permission), main branch. Existing Notion Hub: `3fe864d2-95ce-8178-95ae-d0bcfde6ac34`.
- GitHub `state/current.json` is the only numerical state authority. At end T153: Lv6, EXP185/400, HP115/170, STA85/110, BLOOD25/50, Tử Huyết0/20, souls5, DEF22; T154 NOT played.
- Edran = Tư Tế Xương; Maela female hunter; Kharzug injured Tam Nha guardian at last observed T93; pup alive T93; Huyết Lang Độc Nhãn is DIFFERENT (killed T66). The exact T153 presence of those four NPCs is not confirmed.
- `cam_lao_gate=SEALED`, `tam_trao_tripwire=BYPASSED_NOT_DISARMED`; accepted boss replay T128–139 supersedes initial branch, no doubled loot.
- Notion records are evidence-qualified historical assertions, never automatically current. Separate `CONFIRMED`, `LAST_VERIFIED`, `PARTIAL`, `UNKNOWN`, `SUPERSEDED` from life status.
- Notion `query_data_sources` was confirmed `available_with_limit`; use bounded rows-mode one-source queries, stop on incomplete coverage. No premium-only features or broad SQL joins required.
- Checkpoint frequency **no later than 5 completed turns, on important NPC/quest change, or before changing chats** is a manual active-session policy, not unattended automatic synchronization. No chat-ingest service exists.
- Never modify unrelated Notion pages, delete Drive backup, change repo privacy, expose credentials, or assert independent validation without independent reviewer evidence.

## Review Focus

1. **Historical last seen vs current presence:** T93 last-seen link must not become T153 occupancy. Tests: Task 1 `test_last_seen_not_current`, Task 4 temple query.
2. **Confusable NPC IDs:** Kharzug survives T93, one-eyed enemy died T66. Tests: Task 1 `test_kharzug_distinct_from_one_eyed_wolf`, Task 3 page readback.
3. **Repeated/uncertain create results:** never create duplicate `Canonical ID` or `Edge ID`. Tests: Task 1 `test_repeat_upsert_zero_creates`, Tasks 3/4 second pass.
4. **Docs-only GitHub commit after projection:** do not claim game state changed or endlessly reproject. Test: Task 5 `test_docs_only_commit_not_dirty`.
5. **Mid-batch Notion failure and stale relation endpoints:** Hub marker remains old, resume by exact IDs; no fabricated graph. Tests: Task 5 `test_partial_failure_no_marker_advance`, Task 4 readback.

## Exact file and Notion object map

| Path / object | Owner / purpose |
| --- | --- |
| `graph/seed/entities.json` | 9 stable entity identities with canonical evidence |
| `graph/seed/relationships.json` | 7 directed, time-qualified, evidence-backed edges |
| `verification/graph_validation.py` | Pure validator and idempotent diff planner; never calls network |
| `verification/test_graph_validation.py` | Python unittest failure-mode tests |
| `graph/notion-registry.json` | Derived IDs for two Notion data sources, entity/edge pages and source SHA |
| `verification/graph-receipts/initial-import.md` | Readback facts, tested relations and known unresolved gates |
| `docs/storage-protocol.md` | Active-session projection and fallback runbook |
| `README.md` | Canon pointers and Notion graph entrypoint |
| Notion `Hắc Nhật — Entities` | Typed records for people/places/quest/item identities |
| Notion `Hắc Nhật — Relationships` | Directed edges `From` → `Predicate` → `To` |
| Existing Notion Hub | Graph links and last-projected source SHA; no duplicate hub |

Source-of-truth identity is the GitHub `canonical_id` or `edge_id`; Notion page UUID is a transport mapping, not NPC identity.

---

### Task 1: Offline seed and idempotent projection validation

**Files:** Create `graph/seed/entities.json`, `graph/seed/relationships.json`, `verification/graph_validation.py`, `verification/test_graph_validation.py`.

**Interfaces:** `validate_seed(entities: list[dict], relationships: list[dict]) -> list[str]` returns all validation errors (empty is PASS); `diff_projection(desired: list[dict], fetched: list[dict], key: str, complete: bool) -> dict[str, list[dict]]` returns `create`, `update`, `unchanged`, `duplicate`; if `complete=False`, disallow creates (raise a dedicated `IncompleteLookup` exception). Stable key matching only, never display names.

**Entity seed IDs (exactly 9):** `player:vo-danh`, `npc:edran`, `npc:maela`, `npc:kharzug`, `npc:huyet-lang-non`, `npc:huyet-lang-doc-nhan`, `location:dien-te-huyet`, `location:cam-lao`, `location:rung-xuong`.

**Edge key convention:** literal `from_id|PREDICATE|to_id|Tstart-Tend`. Seed exactly:
- `npc:edran|MENTORS|player:vo-danh|T50-T54`
- `npc:maela|COMBAT_ALLY_OF|player:vo-danh|T90-T93`
- `player:vo-danh|RESCUED|npc:kharzug|T73-T90`
- `npc:kharzug|PROTECTS|npc:huyet-lang-non|T90-T93`
- `npc:maela|FOUND|npc:huyet-lang-non|T68-T69`
- `npc:edran|LOCATED_AT_LAST_SEEN|location:dien-te-huyet|T93`
- `npc:kharzug|LOCATED_AT_LAST_SEEN|location:dien-te-huyet|T93`

Every row includes `github_source` / `github_evidence` pointing to a real repo file and temporal provenance, plus `evidence_quality`; no unsupported family relations or permanent party membership.

- [ ] Write tests: `test_last_seen_not_current`, `test_kharzug_distinct_from_one_eyed_wolf`, `test_duplicate_entities_and_edges_fail`, `test_dangling_endpoint_fails`, `test_missing_evidence_fails`, `test_repeat_upsert_zero_creates`, `test_incomplete_lookup_fails_closed`.
- [ ] Run `python -m unittest verification.test_graph_validation -v` and confirm relevant RED failures prior to validator implementation.
- [ ] Implement `validate_seed` and `diff_projection` (signatures above); populate both JSON files only from existing GitHub canon and event records. For T93 facts, preserve status `LAST_VERIFIED`; do not infer T153 position.
- [ ] Run `python -m unittest verification.test_graph_validation -v` and `python verification/check_state.py`; require all GREEN, exact 9 entities and 7 edges.
- [ ] Create/read back the four GitHub files and resulting commit SHA. If local test execution is unavailable, do not label validator PASS merely from source inspection.

**Gate T1:** Unique stable IDs, direction/evidence/turn ranges valid, no dangling edges, duplicate-safe dry-run, gameplay state unchanged.

### Task 2: Create two typed Notion databases and real relation columns

**Objects:** Existing Hub page; newly nested Entities and Relationships. No seed rows yet.

- [ ] Fetch Hub `3fe864d2-95ce-8178-95ae-d0bcfde6ac34`; inspect child DBs and stop if matching project DB already exists until reusing its ID/schema is established. Capture original Hub snapshot (no edits).
- [ ] Call `notion_create_database` with `parent:{page_id:"3fe864d2-95ce-8178-95ae-d0bcfde6ac34"}`, title `Hắc Nhật — Entities`, SQL DDL defining `Name TITLE`, `Canonical ID RICH_TEXT`, `Kind SELECT(PLAYER,NPC,LOCATION,FACTION,QUEST,ITEM)`, `Life/World Status SELECT(ALIVE,INJURED,DECEASED,UNKNOWN,ACTIVE,CLOSED)`, `Evidence Quality SELECT(CONFIRMED,LAST_VERIFIED,PARTIAL,UNKNOWN,SUPERSEDED)`, `Last Verified Turn NUMBER`, `GitHub Source URL`, `Summary RICH_TEXT`, `Last Synced SHA RICH_TEXT`. Options use exact provider form `'NPC':green` etc. Fetch created database and `collection://` data source.
- [ ] Create `Hắc Nhật — Relationships` in the same Hub with `Assertion TITLE`, `Edge ID RICH_TEXT`, `Predicate SELECT(MENTORS,COMBAT_ALLY_OF,RESCUED,PROTECTS,FOUND,LOCATED_AT_LAST_SEEN,ASSOCIATED_WITH,GUARDED,KILLED)`, `Evidence Quality` enum as above, `Lifecycle SELECT(LAST_VERIFIED,ONGOING_CONFIRMED,ENDED,SUPERSEDED,UNKNOWN)`, `First Verified Turn NUMBER`, `Last Verified Turn NUMBER`, `End Turn NUMBER`, `GitHub Evidence URL`, `Last Synced SHA RICH_TEXT`. Fetch returned data source.
- [ ] Call `notion_update_data_source` on **fetched Relationships data source ID**, with `ADD COLUMN "From" RELATION('<Entities data-source ID>'); ADD COLUMN "To" RELATION('<Entities data-source ID>')`. Use actual `collection://` ID and valid DDL quoting. Do not invent IDs.
- [ ] Fetch both schemas again; verify 9 fields on Entities, 12 fields on Relationships (including two actual `relation` fields that target Entities); query each via `query_data_sources({mode:"rows",data_source_url:"collection://...",limit:100})` and require zero initial rows or audited reuse.
- [ ] Record actual database + data source IDs, schema verification receipts. If Notion relation DDL is unsupported, STOP G1; do not replace relationships with text and call it a graph.

**Gate G1:** exactly two intended databases, property types match spec, `From` and `To` native Relations to Entities, no unrelated Notion mutation.

### Task 3: Import Entities with source receipts

**Inputs:** Validated `entities.json`, Entities `collection://` ID, exact GitHub source SHA after Task 1 commit.

- [ ] Query each `Canonical ID` using rows-mode exact property filter; example `{mode:"rows",data_source_url:"collection://<ID>",filter:{type:"group",operator:"and",filters:[{type:"property",property:"Canonical ID",propertyType:"text",operator:"string_is",value:{type:"exact",value:"npc:edran"}}]},limit:20}`. Zero is missing, one is existing, two or incomplete coverage is BLOCKED. Do not retry a timed-out create without requery.
- [ ] Create only missing records via `notion_create_pages({parent:{data_source_id:"<ID>"},pages:[{properties:{Name:"Edran","Canonical ID":"npc:edran",...}}]})`; actual property names/types must match fetched SQL schema. Set `Last Synced SHA` to captured GitHub source commit SHA; a later docs-only commit does not invalidate the source.
- [ ] Fetch all nine page IDs. Confirm Kharzug status `INJURED` and last verified T93; slain Huyết Lang Độc Nhãn status `DECEASED` T66; Edran/Maela/pup alive last verified T93; player T153 known from canon, but no fabricated NPC T153 occupancy.
- [ ] Re-query the nine stable IDs and compute `diff_projection`; require `create=0`, `duplicate=0` and 9 unique page IDs. Record mappings for registry.
- [ ] Record actual Notion IDs and source SHA as migration receipts; any incomplete Notion coverage is a failed gate, not evidence that absent records should be created.

**Gate G2-Entities:** 9/9 fetched and unique, source links intact, no world-state changes.

### Task 4: Import Relationships and prove directed neighborhood queries

**Inputs:** 7 validated edges, source SHA, actual Entity page IDs and native relation schema.

- [ ] Run `validate_seed` against a test edge with non-existent `to_id` and require rejection before any Notion write. Query exact `Edge ID` values to establish missing/existing rows; ambiguous duplicates block creation.
- [ ] Create missing Relationships via `notion_create_pages`; `From` and `To` are arrays of **one** actual Notion Entity page ID/URL, not text labels. Populate Predicate, Evidence Quality, Lifecycle, turn ranges, GitHub Evidence URL and Last Synced SHA.
- [ ] Fetch all seven edges; assert `From.length===1`, `To.length===1`, directions correspond to seed, and evidence fields/turn ranges match source. Relationship title is display only.
- [ ] Run actual `query_data_sources` rows-mode `relation_contains` on `From=Kharzug` and `To=Kharzug`; assert `Kharzug --PROTECTS--> Sói con` and `Vô Danh --RESCUED--> Kharzug` respectively. Query inbound `To=Điện Tế Huyết`; find Edran and Kharzug `LOCATED_AT_LAST_SEEN` (T93), **not** current T153 presence.
- [ ] Re-run exact `Edge ID` queries; require `create=0`, 7 unique records, 0 dangling endpoints, 0 invented biological kinship. Persist page mappings and readback receipts.

**Gates G2-Edges/G3/G4:** 7/7 evidenced directed edges and working bounded Notion queries, not just table-shaped text.

### Task 5: Failure recovery, source-change semantics and fast-path tests

**Files:** Extend `verification/graph_validation.py`, `verification/test_graph_validation.py`; modify `docs/storage-protocol.md` after fetching its current GitHub blob SHA; draft `verification/graph-receipts/initial-import.md`.

**Interfaces:** `diff_projection(..., complete=False)` must block writes; `projection_changed(changed_paths: list[str], state_changed_fields: set[str]) -> bool` is true for material NPC/relationship input changes (`events/`, `canon/`, `graph/seed/`, or relevant `state/current.json` fields such as NPC/quest/world flags), false for docs-only changes or `state/current.json` HP/STA-only arithmetic. GitHub still persists the numeric checkpoint; Notion graph is not rewritten without graph-relevant change.

- [ ] Add tests `test_partial_failure_no_marker_advance`, `test_docs_only_commit_not_dirty`, `test_hp_only_checkpoint_not_graph_dirty`, `test_stale_endpoint_blocks_edge`, `test_duplicate_edge_ids_fail`, `test_unknown_current_npc_presence_not_inferred`.
- [ ] Run `python -m unittest verification.test_graph_validation -v` to show RED failures for new behavior.
- [ ] Implement only pure validation/change detection and documented connector-runbook: GitHub-first, expected-head check when game state changes, Notion Entities then Relationships, readback all changes, Hub marker last. Failed Notion batch retains prior Hub SHA and allows deterministic retry by IDs.
- [ ] Run the test suite and `python verification/check_state.py` to GREEN; ensure T153 numeric snapshot unchanged.
- [ ] Validate quick-read scenario: routine attack has 0 required Notion calls; first scene with Kharzug uses one exact Entity lookup and inbound/outbound bounded relation lookups; failure falls back to GitHub `canon/npc/kharzug.md`.
- [ ] Commit/read back validator/tests/protocol and record separate `projected_source_commit_sha` vs later `documentation_commit_sha`. Do not mark Notion stale merely because README/spec documentation changed.

**Gates G5/G6:** zero duplicates on replay, controlled failure recovery, no pretend background sync, no extra latency for normal turns.

### Task 6: Hub cutover and final verification receipts

**Files/objects:** Actual Notion Hub page, optional Notion database views, `graph/notion-registry.json`, `verification/graph-receipts/initial-import.md`, `README.md`.

- [ ] Re-fetch GitHub state `state/current.json`, Hub page, all required Notion rows and source commit; require G0–G6 PASS before changing Hub's live label.
- [ ] After fetching database IDs, create basic `table` views in Notion: Entities showing Name/Kind/Life/Last Verified Turn, Relationships showing Assertion/From/Predicate/To/Last Verified Turn. Do not claim an interactive node canvas exists.
- [ ] Target-edit the existing Hub: link real Entities & Relationships databases, GitHub source, sync status and SHA; demote obsolete STAGING/private-only notices to clearly historical references. Only rename Hub `HẮC NHẬT — Knowledge Graph (LIVE / T153)` if all earlier gates PASS. Never create a second Hub.
- [ ] Fetch Hub + both databases again; prove correct links, SHA, 9 Entities, 7 Relationships, no duplicate keys, and that T154 has not started. When Notion query coverage is partial, mark G7 BLOCKED, not PASS.
- [ ] Save real Notion IDs and actual readback evidence to `graph/notion-registry.json` and `verification/graph-receipts/initial-import.md`; update `README.md` links. Commit these docs and read them back. Distinguish this later documentation commit from the gameplay/source SHA used for projection.
- [ ] Publish a gate matrix G0–G7 with source GitHub commit, Notion URLs, row counts, unresolved restrictions and run commands; clearly state real timed background automation remains deferred.

**Gate G7:** a player can open Notion and follow Kharzug→wolf pup and Vô Danh→Kharzug via native relations. GitHub gameplay remains canonical and unchanged.

## Stop and rollback semantics

- Tasks are sequential; never reissue an ambiguous create before fetching the provider's state.
- Keep successful Notion DB/page IDs, no destructive deletes or force pushes. If partial migration fails, Hub remains not-live/STALE while GitHub canonical gameplay remains playable.
- Any false T153 NPC presence, unsupported kinship, or wrong relation endpoint is a hard NO-GO. Correct the source/model only with verified evidence, not a speculative patch.
- Cross-chat context is read from GitHub at the beginning of the next conversation; Notion cannot guarantee automatic per-turn ingestion or persistent in-memory caching.

## Plan self-review (author; not independent)

- Scope/spec coverage: Task1→identity/evidence, Task2→schema, Task3–4→seed/graph query, Task5→idempotency/failure/performance, Task6→Hub rollout. G0 (state preflight) and G1–G7 all assigned.
- Step scan: all actions have an explicit object/file/tool and a checkable result; no open-ended "build sync service" placeholder.
- Interface consistency: `validate_seed`, `diff_projection`, `projection_changed`, `Canonical ID`, `Edge ID`, `From`, `To`, `Last Synced SHA` use consistent names.
- Review Focus: all five failure inputs have named tests or provider readbacks. Red→green tests required for code changes, readback required for connector writes.
- Proportion: plan is bounded to existing repository and two Notion databases; no extra infrastructure. This is not a claim of executed tests or implemented graph.
- **Next gate:** owner reviews this PLAN and chooses `Native` or `Subagent-driven` execution; approval of the spec alone did not authorize implementation.
