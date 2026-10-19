# HẮC NHẬT — GM Storyline & Next Action Protocol V1

**Authority:** GitHub main, `state/current.json`, `events/`, `canon/`, `story/arcs.json`; Notion is a relation lookup/projection. **This is operational GM guidance**, not a new narrated turn or accepted quest.

## GM Turn Response-Time Policy (Owner-approved 2026-10-20)

**Owner acceptance:** 1–2 minutes for a normal RPG turn is acceptable; roughly 3 minutes is still acceptable for a complex turn. A 7-minute turn caused by routine tool/plugin orchestration is NOT the desired operating mode. These are practical targets rather than hard response-time guarantees. Narrative quality, combat math, resource accuracy, and continuity still take priority over arbitrary speed.

- **Default game turn:** Narrate and adjudicate directly from active-chat working memory; do not invoke Superpowers for normal RPG gameplay, and do not call GitHub/Notion simply to generate action choices.
- **When to retrieve:** At the start of a new chat or after evidence is missing/contradictory, fetch the minimal canonical GitHub snapshot and only scene-relevant lore. Use Notion only for important unresolved NPC/relationship context. Avoid full repository scans, global audits, extra agents, and running test suites inside ordinary gameplay turns.
- **When to persist:** Honor the existing checkpoint policy: at most five completed turns, significant irreversible/story/NPC event, explicit save request, or session handoff. Batch related GitHub changes, verify the written commit, and project to Notion only if graph data actually changed. Never claim unsaved turns are durable.
- **If persistence takes time:** Do not silently let routine bookkeeping dominate the turn. Report an actual sync blocker or failure succinctly when relevant; do not assert a background sync, invent a successful write, or postpone an explicitly requested checkpoint.
- **Superpowers boundary:** Use for explicit brainstorming/engineering design, audit, and maintenance only; never require it to start or finish a player action.
- **Budget and evidence:** Judge cost by observed latency and necessary work rather than invented timings. Do not add new services, workers, scheduled tasks, or databases for speculative optimization.

## Per-turn execution

1. Start of a session: read current snapshot, `story/arcs.json`, `story/actions.json`, `state/quick-start.md`. When an NPC/location is relevant, load that canonical file or corresponding Notion neighborhood (Notion saved views preferred if query quota limited).
2. Understand the **player's actual action**. Suggested action buttons are optional proposals, never autoplay, guaranteed success or a formal quest accepted by the player.
3. Resolve one narrated turn from evidence and rules; audit HP/STA/BLOOD/TH, item inventory, status, time and all named affected NPCs. Offer 2–4 contextual optional next actions after resolution, plus free-form choice.
4. Before showing suggestions, apply `eligible_actions`: allow only understood preconditions and verified availability. The sealed-vessel option remains hidden until access to the relevant item is confirmed; keep free-form play open. Verify that any action has a source and correct location/preconditions. Do not suggest already RESOLVED arcs as current active objectives.
5. After each **confirmed** turn, evaluate `post_turn({confirmed, event_types, unique_thread_evidence, turns_since_flush, changed_paths, state_changed_fields, switching_chat, requested})` (pure, no network). Review a new storyline only with unique witnessed evidence; a mention stays a rumor. The returned flags are decisions, **not completed writes**. `ARC_CREATED` or `ARC_RESOLVED` requires immediate GitHub checkpoint.
6. Commit accepted event + state + changed story arcs to GitHub when `checkpoint_due` and verify the commit/readback. Project only if `notion_projection_due`: actual NPC/entity/relation change or a graph seed/canonical NPC change. An ordinary combat event, HP/STA delta, or docs-only commit must not rewrite Notion. Never silently change historical events or upgrade last-seen T93 to presence T153.
7. Checkpoint no later than 5 completed turns, upon any major irreversible event, before switching chat, or on request. After each successful flush, verify GitHub branch commit, changed files and state; if Notion projection fails, label its last-sync SHA STALE. If GitHub write fails, in-chat deltas remain **UNSAVED** and must not be described as persisted.
8. No unattended running/scheduled ingest is installed. GM can perform writes during an active turn only, using accessible connectors.

## Action-option presentation contract (based on user screenshot)

- Show a small section **Hành động tiếp theo** at the end of a normal GM reply, preferably 2–4 clickable choices when the chat UI supports interaction; a short plain-text list is an acceptable fallback. Avoid decorative UI that adds latency. Option cards should contain a clear short title and a one-line grounded rationale, using DIL `pressable` or `button` with `GenUI.issueNewTurn` when appropriate.
- Always permit a free-form player instruction. Choosing an option is a new user command, not an automatic action by GM.
- If the world state or user intent makes suggestions irrelevant, omit choices rather than force a stale menu.
- Last accepted state is T154 (see `events/0154.md`): **do not suggest “Cứu Maela” as if still captive, or “Săn Huyết Lang Vương Lv6” as an uncleared boss**. They appeared in a screenshot of an old GM turn, not the current situation.
- Derive choices from the **latest GitHub snapshot and scene**, never a frozen T153 menu. The sealed-vessel choice is excluded until inventory/availability is confirmed. Previously resolved boss rescue/hunt options stay excluded. These are directions to choose, not guaranteed NPC presence.
- Display combat tactical map if combat requires it, not merely as decoration in social scenes.

## Arc lifecycle and authority

`RUMORED → DISCOVERED → AVAILABLE/ACTIVE → BLOCKED/RESOLVED/FAILED`, with explicit, evidenced transition edges only; `ACTIVE` also requires verified player commitment, and transition events cannot predate last evidence. `SUPERSEDED` retains previous accepted branch history. Terminal states cannot reopen solely because a suggestion generator wants variety. Do not create a quest or grant rewards without an on-screen accepted action and causal event. Confirm branch merge or irreversible decisions from the owner/player before changing canon.

## Data boundaries / performance

- **Working Memory:** latest chat turn deltas, only durable after verified checkpoint.
- **Fast GitHub:** `state/quick-start.md`, `state/current.json`, `story/arcs.json`, `story/actions.json`.
- **Long-term:** `events/`, `canon/`, `sources/drive/`.
- **Graph:** Notion Entities/Relationships, source SHA and historical time qualifiers.
- Never query full Notion graph on a routine attack. Avoid new background scheduler/credentials, no implicit auto-sync outside the chat.

## Acceptance / limitations

This V1 creates static seed registries and a pure Python policy library with regression test definitions. It does **not** create a connected runtime command or host hook to run these functions automatically on every incoming chat message. GM must follow the runbook and explicitly use connected GitHub/Notion tools when writing. Python regression tests must be executed and verified before asserting PASS. The `post_turn` function is a lightweight **decision helper**, not an installed ChatGPT host hook. The GM still has to invoke connected GitHub/Notion tools explicitly during active chat and verify each write.

## T154 continuity delta (read from GitHub)

The player already held a council at the temple with Edran, Maela and Kharzug at T154; the unnamed pup was also present. Kharzug's hind-leg injury persists. Edran explicitly said the three-claw marks and interlocking three-fang collar may relate but do not establish the same organization. No quest acceptance, permanent party recruitment, departure, item consumption or battle. Resources unchanged. These facts supersede T153 uncertainty about NPC presence at the temple **at T154**, but do not prove where NPCs will be on later turns. GitHub `events/0154.md` is the source.
