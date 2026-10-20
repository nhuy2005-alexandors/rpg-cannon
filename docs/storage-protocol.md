# Fast-play persistence: GitHub canonical, Notion projection

- GitHub main: single current numeric snapshot at state/current.json, immutable event history in events/, NPC/world lore in canon/, imported evidence in sources/drive/.
- Notion: read-optimized index of changed NPCs, quests and latest checkpoint. Store last_synced_commit_sha; do not override GitHub canon.
- During normal gameplay: resolve turns in ChatGPT; track deltas locally in the chat. Flush to GitHub every 10 completed turns since the latest verified GitHub checkpoint maximum, on major NPC/quest event, before moving chats, or on user demand (whichever first).
- Each flush: read head -> resolve delta -> check arithmetic/causality -> commit with expected-head guard -> fetch/read-back -> update Notion projection. On write failure, distinguish UNSAVED delta from canonical state.
- **No automatic ingestion or background timer is currently configured.** A scheduled reminder alone cannot access new chat turn events.
- Special invariants: Edran=Tư Tế Xương, Maela hunter, Kharzug old Tam Nha war beast NOT Huyết Lang Độc Nhãn killed T66, unnamed pup safe T93; no arbitrary deaths/teleports; Cam Lao gate still sealed; Tam Trao tripwire bypassed not disarmed; no boss loot double count after accepted replay.
- Repo is PUBLIC by explicit owner approval. Do not add real-world secrets, credentials or unrelated personal records.
- Drive folder remains available for provenance; do not delete or rewrite it automatically.

## Knowledge Graph V1 — Notion projection (2026-10-19)

- Project Hub: https://app.notion.com/p/3fe864d295ce817895aed0bcfde6ac34
- Entities database: https://app.notion.com/p/3e1a70d007444496874d9e9535071d6a
  data source: `collection://6f40f9fb-1bb7-48b9-9c84-a8f8bff91579`
- Relationships database: https://app.notion.com/p/4ea8c07ae96d4312b585acab207bc370
  data source: `collection://b3eeb1ac-138f-4dab-b7ad-6b63321f2b86`
- Seeded entity and relation identities: `graph/seed/entities.json` and `graph/seed/relationships.json` (9 entities, 7 edges from evidence).
- The initial **projected source SHA** is `c47ba6254b042f016f8f53aafb2af346173674e4`. Later documentation, test and registry commits do NOT imply a newer NPC/relationship projection. Compare changed canonical inputs, not `HEAD != last_synced_commit_sha`.
- Notion relation fields `From` and `To` are genuine relations to Entities. Use exact `Canonical ID` and directed `Edge ID` for upsert; display names are not stable keys.
- The provider **rows-mode relation_contains filter was observed to return unfiltered rows** in this workspace. Do not interpret these results as an exact neighborhood. SQL `"From" LIKE ?` / `"To" LIKE ?` worked when query allowance was available, but the allowance was then exhausted. Revalidate and client-side check actual endpoint IDs before using any matched edge.
- Saved-view **view mode** remains usable after ordinary SQL/rows query quota exhaustion. Use the browser views and/or connector with `mode:view` as a bounded alternative:
  - Entity Explorer: `view://3fe864d2-95ce-8116-9ad7-000c62f533e1`
  - Relationship Explorer: `view://3fe864d2-95ce-810d-8c5c-000c3621bfb9`
  - Temple LAST SEEN: `view://3fe864d2-95ce-81e1-abc2-000cbcede468` (two T93 edges, NOT T153 presence)
  - Kharzug Outbound: `view://3fe864d2-95ce-81f7-bf1e-000c4512af16` (PROTECTS, LOCATED_AT_LAST_SEEN)
  - Kharzug Inbound: `view://3fe864d2-95ce-81f2-8064-000ce0741e17` (RESCUED)
- The Notion Rows response can escape pipes in `Edge ID` as `\\|`; canonical IDs use unescaped `|`. Normalize before equality comparison; fail closed on incomplete retrieval or duplicate IDs. `verification/graph_validation.py` implements stable-key normalization and dry-run diff.
- The GitHub file `state/current.json` is still the sole authority for actual gameplay numbers and flags. At T153 all major NPCs only have last-seen evidence T93; unknown current location is not death or movement.
- Flush during active session at most every ten completed turns since the latest verified checkpoint, upon significant canonical NPC/quest/world change, or before changing conversations. Write GitHub first using commit head checks, verify commit/readback, then project changed entities/edges to Notion. Do not update the Hub sync marker until every projected row was verified. Notion partial failure makes projection STALE; replay must reuse IDs, not duplicate pages.
- There is **no background agent, webhook or scheduler ingesting this chat**. No assumption of automatic saving between replies; only successful tool writes produce durable changes. If Notion cannot be queried or has exhausted limits, read GitHub canon directly and do not invent graph edges.


## Minimal GM after-turn guard (v1.1)

- Evaluate `story.engine.post_turn` **only after adjudicating a confirmed turn**, using explicit `event_types` and `changed_paths`. This is a pure decision function; it does not call connectors, run in the background, or guarantee automatic invocation by the ChatGPT host.
- When `checkpoint_due`: save GitHub canon and event/state/storyline changes, guard the branch head and verify readback. No remote write for an ordinary non-checkpoint combat turn.
- When `notion_projection_due`: project **only changed NPC/entity/relationship evidence** to the existing Notion Entities/Relationships. `events/` alone (combat log) is insufficient; classify graph-relevant event types. If classification is absent, fail closed instead of claiming graph synchronization. A docs-only or HP/STA-only commit does not trigger Notion.
- A failed Notion projection leaves the GitHub commit authoritative and the Notion Hub visibly STALE. Mark it SYNCED only after reading back changed rows and source SHA. These rules avoid updating Notion after every turn; they do **not** install an unattended sync service.

## Owner-approved autonomous cadence (2026-10-20)

- During an active game session the GM initiates GitHub checkpoint automatically after **10 completed turns since the last verified GitHub checkpoint**, without requiring a save command. Reset counter only after successful GitHub commit + readback. Failed write keeps pending deltas UNSAVED.
- Major NPC/quest/world events, impending context loss, chat change and direct save request override the 10-turn cadence and trigger earlier saving. This also limits reliance on long-context retention; ten turns are a preferred batch size, not a guaranteed memory horizon.
- Notion remains selective for actual graph changes; no scheduled polling, external timer, automatic ingestion or background execution is installed. Checkpoint turns may run longer than ordinary turns to ensure verification.

## Read avoidance and sliding-window continuity (2026-10-20)

- One GitHub bootstrap per **new chat** only if no reliable in-chat checkpoint exists. Reuse the last verified checkpoint readback plus the current in-chat state for subsequent turns. Specifically, T163 after a verified T162 in the same chat must NOT re-fetch T162.
- Track `session_base` (verified checkpoint SHA and turn), `current_state`, a sliding window of up to 10 compact turn deltas, and `unsaved_turns` inside the active conversation. This is a conceptual context ledger; there is no new local cache process or background service.
- Ordinary turns use in-chat context with zero provider calls by default. Missing evidence, a context reset/compaction, a new chat or a real continuity conflict permits **targeted** GitHub recovery; Notion remains selective for relevant graph lookups.
- When 10 turns accumulate or a major event/explicit save/session handoff/context risk occurs, commit and verify GitHub ONCE; adopt its readback as the new session base. Do not repeat readback on the next turn. Never reset `unsaved_turns` after failed writes.
- This rule is operational GM behavior, not a host-installed hook; repository documentation alone does not guarantee compliance by other chat instances.
