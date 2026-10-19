# Hắc Nhật — Notion Knowledge Graph V1 (Formal Design Specification)

**Date:** 2026-10-19
**Status:** Awaiting owner review of written specification; NOT an implementation authorization.
**Design choice approved:** B — two Notion databases, Entities + Relationships.
**GitHub canon:** [rpg-cannon](https://github.com/nhuy2005-alexandors/rpg-cannon), public by explicit owner permission.
**Existing Notion hub:** [Hắc Nhật Context Hub](https://app.notion.com/p/3fe864d295ce817895aed0bcfde6ac34).
**Current gameplay:** T153 completed, T154 not started.

## 1. Purpose and constraints

Build a read-optimized relationship graph that remembers actors, places, quests and their historically evidenced links, preventing omissions such as Edran, Maela, Kharzug and the wolf pup. The owner prioritizes correct, quick RPG turn narration over frequent remote API calls. It must be possible to answer "Who is connected to this location and when were they last actually seen?" without inventing missing events.

**One authoritative source:** GitHub \`main\`, particularly \`state/current.json\`, \`canon/\`, and \`events/\`; Notion is a derived materialized index, NEVER a second canonical gameplay state or reverse-sync writer. Existing Drive extracts are frozen source evidence.

**Immutable accepted facts:** At T153: Lv6 EXP185/400, HP115/170, STA85/110, BLOOD25/50, Tử Huyết0/20, souls5, DEF22; Edran = Tư Tế Xương; Maela = female free hunter; Kharzug = ancient injured Tam Nha war beast, NOT the Huyết Lang Độc Nhãn killed T66; unnamed Huyết Lang pup alive T93; Cấm Lao gate SEALED; Tam Trảo trap \`BYPASSED_NOT_DISARMED\`; accepted T128–139 replay superseded the original fight and loot cannot double count. NO T154 world event shall be created as a side effect of graph setup.

**In scope:** two Notion databases under existing Hub, initial records from verified GitHub canon, tracked GitHub commit SHA, relationship lookup procedure, audit receipts, staged rollout.

**Out of scope:** change gameplay, edit/retcon source lore, full-text transcript reconstruction, third event database, realtime chat capture, always-on worker, scheduler, AI-agent simulation of offscreen events, modification of unrelated Notion databases, public publishing of real-life sensitive content.

## 2. Overall flow

\`\`\`text
ChatGPT narration (fast active-turn state; unsaved in-chat deltas)
    | only when checkpoint condition met and write tools actually run
    v
GitHub main (event ledger + current state + NPC canon) -- canonical commit SHA -->
    Notion projector: Entities -> Relationships -> verify -> Hub sync marker
                         |          |
                     entity IDs   From / To edges
\`\`\`

For each session, read \`state/quick-start.md\` and \`state/current.json\`; load targeted NPC and event context as needed. A routine combat reply does not wait for Notion or a GitHub commit. A critical NPC death/departure/quest transition triggers a checkpoint immediately; otherwise flush after no more than five completed turns, when the user changes chats, or on request. A "flush" is complete only after commit and readback. These triggers are a **procedural policy**, not an unattended timer. No background chat-message collector is configured.

## 3. Identity, evidence and time semantics

**Stable entity key**: prefix + ASCII slug. Seed:
- \`player:vo-danh\`; \`npc:edran\`; \`npc:maela\`; \`npc:kharzug\`; \`npc:huyet-lang-non\`; \`npc:huyet-lang-doc-nhan\`
- \`location:dien-te-huyet\`, \`location:cam-lao\`, \`location:rung-xuong\`; other places only when canonical source supports them.
- Entities may later be \`FACTION\`, \`QUEST\`, \`ITEM\`; no fabricated quest names to pad the graph.

An entity's mutable display name is not its identity. Projector enforces uniqueness on \`Canonical ID\` even though Notion RICH_TEXT has no database-level UNIQUE constraint.

**Directed assertion**: \`from_id —predicate→ to_id\`, annotated with source range, \`first_verified_turn\`, \`last_verified_turn\`, optional \`end_turn\`, \`evidence_quality\`, \`lifecycle\`, \`github_evidence\`. Use stable \`Edge ID\` deterministically derived from \`from|predicate|to|source_turn_or_range\`. Reprocessing the same evidence must upsert, not append duplicates. Different event/time assertion needs separate edge or explicit supersession.

Controlled predicates in V1: \`MENTORS\`, \`COMBAT_ALLY_OF\`, \`RESCUED\`, \`PROTECTS\`, \`FOUND\`, \`LOCATED_AT_LAST_SEEN\`, \`ASSOCIATED_WITH\`, \`GUARDED\`, \`KILLED\`. Direction matters: a scene may find inbound and outbound relationships, but \`RESCUED\` is not reversible. \`LOCATED_AT_LAST_SEEN\` does not prove present NOW. \`COMBAT_ALLY_OF\` is not permanent membership. Family, romance, ownership and permanent party membership are not inferred.

**Evidence Quality enum:** \`CONFIRMED\` (on-screen source), \`LAST_VERIFIED\` (historical; cannot assert still current), \`PARTIAL\` (user instruction or incomplete outcome), \`UNKNOWN\` (not established), \`SUPERSEDED\` (accepted correction/replay). These labels are independent of life status \`ALIVE\`, \`INJURED\`, \`DECEASED\`, \`UNKNOWN\`. T93 last-seen ≠ T153 observed. The GM's omission of NPCs at T152–153 is **not** evidence they left or died.

## 4. Notion schema: exactly TWO databases

Both are nested under the existing project Hub. Creation/relation configuration relies on actual fetched \`collection://\` data source IDs, not guessed page IDs.

### 4.1 Entities data source

| Property | Type | Contract |
| --- | --- | --- |
| \`Name\` | TITLE | Readable name |
| \`Canonical ID\` | RICH_TEXT | Projector-enforced unique stable ID |
| \`Kind\` | SELECT | PLAYER/NPC/LOCATION/FACTION/QUEST/ITEM |
| \`Life/World Status\` | SELECT | ALIVE/INJURED/DECEASED/UNKNOWN/ACTIVE/CLOSED |
| \`Evidence Quality\` | SELECT | CONFIRMED/LAST_VERIFIED/PARTIAL/UNKNOWN/SUPERSEDED |
| \`Last Verified Turn\` | NUMBER | Nullable, never invented |
| \`GitHub Source\` | URL | Canonical link |
| \`Summary\` | RICH_TEXT | Small derived abstract, not duplicated lore |
| \`Last Synced SHA\` | RICH_TEXT | GitHub commit incorporated into projection |

Entity page body holds brief in-world description and original turn refs. RPG numbers are NEVER pulled from Entities if \`state/current.json\` has newer numbers.

### 4.2 Relationships data source

| Property | Type | Contract |
| --- | --- | --- |
| \`Assertion\` | TITLE | Human-readable edge |
| \`Edge ID\` | RICH_TEXT | Deterministic upsert key |
| \`From\` | RELATION(Entities) | Exactly one valid logical endpoint |
| \`Predicate\` | SELECT | §3 controlled set |
| \`To\` | RELATION(Entities) | Exactly one valid logical endpoint |
| \`Evidence Quality\` | SELECT | §3 evidence labels |
| \`Lifecycle\` | SELECT | LAST_VERIFIED/ONGOING_CONFIRMED/ENDED/SUPERSEDED/UNKNOWN |
| \`First Verified Turn\` | NUMBER | Nullable |
| \`Last Verified Turn\` | NUMBER | Nullable |
| \`End Turn\` | NUMBER | Nullable |
| \`GitHub Evidence\` | URL | Source link to canon/event file |
| \`Last Synced SHA\` | RICH_TEXT | Canonical commit for projection |

**Schema construction:** create Entities first; fetch to obtain actual data source ID; create Relationships with scalar properties; then \`update_data_source\` to add two relations \`From\` and \`To\` referring to Entities. Read back the schema, confirm both are actual relation types to the same Entities source; only then seed rows. A Notion native RELATION may accept arrays; projector must enforce cardinality = 1 for these fields.

## 5. Initial projection, provenance and anti-hallucination

Import only evidenced facts from \`canon/npc/*.md\`, \`canon/world/places.md\`, \`events/*.md\`, and the accepted T153 state. Minimum six actors: Vô Danh, Edran, Maela, Kharzug, unnamed Huyết Lang pup, dead Huyết Lang Độc Nhãn. Create place entities only if supported.

Minimum seven directed edges to validate use cases:
1. Edran \`MENTORS\` Vô Danh — T50–54 (historical).
2. Maela \`COMBAT_ALLY_OF\` Vô Danh — T90–93 (historical; not permanent party).
3. Vô Danh \`RESCUED\` Kharzug — T73–90 (gate not opened).
4. Kharzug \`PROTECTS\` pup — T90–93 (not parentage).
5. Maela \`FOUND\` pup — T68–69 (not permanent ownership).
6. Edran \`LOCATED_AT_LAST_SEEN\` Điện Tế Huyết — last verified T93.
7. Kharzug \`LOCATED_AT_LAST_SEEN\` Điện Tế Huyết — last verified T93 while injured.

Other relationships can be added only after showing direct evidence. For each edge preserve exact canonical file, turn/range and evidence label. If source logs merely show player intent and not GM outcome, mark PARTIAL; do not record successful outcomes speculatively. No unsourced \`Kharzug is pup's biological parent\`, \`Maela permanently joined\`, \`Edran present at T153\`, \`Kharzug recovered\`, or \`Huyết Lang Độc Nhãn is Kharzug\`.

## 6. Query path optimized for gameplay

**Fast path:** execute the user turn from active chat context; only \`state/current.json\` is numerical authority. Avoid remote Notion query on every turn.

**Scene-related path:** when at temple or interacting with named NPC, look up exact \`Canonical ID\`, then fetch bounded edges where \`From\` OR \`To\` points to that entity's Notion page. Read immediately relevant neighbor IDs; fetch a canonical GitHub scene if a position/status is uncertain. This requires two filtered edge lookups, not a global graph scan. No full in-memory cache is promised between different chats.

**Plan/access limitations verified:** Notion create/update pages, schema and view tools are available; \`query_data_sources\` is \`available_with_limit\`, and AI Search may be unavailable. Use one-source filtered queries where supported, follow pagination on provider return, and declare partial coverage when not exhaustive. No claim of graph visualization generated by the database; V1 supports relational tables and backlinks, not a draggable node canvas.

**On tool failure:** return to GitHub NPC/event files and proceed with an honest known/unknown boundary. Never infer no allies exist from an incomplete Notion query.

## 7. Sync and recoverability contracts

- Source commit must be read from GitHub before projection. GitHub remains first in write ordering and uses an optimistic head check for multi-file checkpoint updates.
- Extract deltas by changed canonical IDs / edges; skip Notion work when HP/STA alone changes. Avoid renumbering/recreating old records.
- Upsert Entities by \`Canonical ID\`, then Relationships by \`Edge ID\`. If lookup returns ambiguous duplicates or coverage is incomplete, fail closed and request reconciliation rather than creating more duplicates.
- Read back all changed rows, \`From\`, \`To\`, evidence and \`Last Synced SHA\`; only after coverage PASS update the Hub's single \`last_synced_commit_sha\` marker. On partial failure, mark Hub STALE; never claim success.
- Idempotency: rerunning seed against same GitHub SHA creates zero additional rows and zero erroneous new facts.
- Corrections: old historical assertions kept or marked SUPERSEDED with reason; no silent alteration of a death or accepted replay. Notion edits cannot modify GitHub canon. If a Notion editor changes a derived row, next reconcile must compare with GitHub and either restore projection or surface a conflict; no reverse synchronization.
- World-state changes of NPCs (death, departure, healing, membership) must have a confirmed narrated event before canonical commit; no automatic offscreen changes.
- Last-synced SHA in Notion belongs to the entire relevant projection batch; a crash before marker write triggers safe rerun using stable IDs. The marker cannot be advanced to an unverified commit.

**Important:** the "every five turns or significant event" rhythm is a policy for actions performed during active ChatGPT operation. There is no background collector/scheduler capable of ingesting future messages. Separate approval/design is required for an autonomous service.

## 8. Rollout and minimum required receipts

**P0 read-only preflight:** verify GitHub canon T153 and Notion Hub; capture source commit and existing Hub page ID. No in-world turn advancement.

**P1 schema:** create only 2 Notion databases under Hắc Nhật Hub, then fetch schema to verify types, relation endpoint target, access. Do not touch unrelated Notion pages. Avoid duplicate database creation by inspecting Hub after any uncertain response.

**P2 migration:** seed entities and relations; record counts, source path, dedup keys, last-seen turns, Notion page IDs and GitHub source SHA. Retain all old Drive and GitHub files.

**P3 hub projection:** link both databases from existing Hub and correct obsolete STAGING/private-only paragraphs by a targeted, verified content update. Do not remove evidence history accidentally. Rename title to reflect LIVE graph only after verification.

**P4 protocol:** update GitHub \`docs/storage-protocol.md\` and add a projection mapping/readme as required, but avoid a SHA feedback cycle by not committing a new metadata file on every Notion sync. Keep Notion sync marker tied to the last canonical *gameplay* commit and clarify documentation-only commit handling.

**Go-live acceptance gates:**
- G0: GitHub T153 unchanged (HP115 STA85 BLOOD25 TH0 souls5; no new T154 event), reference SHA recorded.
- G1: exactly 2 project data sources with correct schema and actual \`From\`/\`To\` relations to Entities.
- G2: 6 minimum actors, all 7 exemplar edges, unique IDs, zero dangling edges, each cited to GitHub.
- G3: Kharzug distinct from dead Huyết Lang Độc Nhãn; pup survives T93; Kharzug injured last seen T93; exact T153 whereabouts unknown; Tam Trảo \`BYPASSED_NOT_DISARMED\`.
- G4: actual connector query yields both Kharzug→pup protection and Vô Danh→Kharzug rescue, correct directions; temple scene returns LAST_SEEN not "present now".
- G5: same seed rerun yields zero duplicates; partial projection failure results in visible STALE marker or failed gate, GitHub always authoritative.
- G6: a routine RPG turn requires no remote Notion writes, and source update claims require commit/readback.
- G7: Notion Hub links to actual databases; no obsolete private-only notice presented as live instructions.

## 9. Failure modes, limits and deferred work

- Provider schema may reject relation DDL: stop after readback and avoid fake graph. Actual DDL verified during P1 before migration.
- Limited Notion query coverage: bounded lookups, pagination where supported, no false "none found" on an incomplete result.
- Wrong IDs / homonyms: immutable Canonical ID/Edge ID, never match by name alone.
- Temporary connector outage: GitHub read-only gameplay fallback, Notion marked STALE when possible.
- Public repo: user approved fictional game canon only. Never add credentials, private personal facts or unrelated account data.
- Missing original GM answers: historical confidence labels preserved, no claim of complete 153-turn verbatim reproduction.
- Graph changes crossing multiple events: preserve temporal supersession; latest evidenced relation not a claim of continuous presence.
- True timed background sync/chat ingest is a separate subsystem and NOT part of this V1.

## 10. Design self-review (non-independent)

Reviewed scope, authority, schema, IDs, directionality, source evidence, temporal uncertainty, idempotency, read fallback, performance constraints, migration boundaries and gates. No known contradiction requires changing existing canon. **This document is a proposed approved-direction spec, awaiting the owner's SPEC review.** Owner approval of B did not automatically approve this written spec, an implementation plan, or database creation. Next authorized stage after spec approval: Superpowers \`writing-plans\`; plan will then require its own review and execution-method decision.
