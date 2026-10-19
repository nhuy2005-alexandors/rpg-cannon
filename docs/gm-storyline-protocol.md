# HẮC NHẬT — GM Storyline & Next Action Protocol V1

**Authority:** GitHub main, `state/current.json`, `events/`, `canon/`, `story/arcs.json`; Notion is a relation lookup/projection. **This is operational GM guidance**, not a new narrated turn or accepted quest.

## Per-turn execution

1. Start of a session: read current snapshot, `story/arcs.json`, `story/actions.json`, `state/quick-start.md`. When an NPC/location is relevant, load that canonical file or corresponding Notion neighborhood (Notion saved views preferred if query quota limited).
2. Understand the **player's actual action**. Suggested action buttons are optional proposals, never autoplay, guaranteed success or a formal quest accepted by the player.
3. Resolve one narrated turn from evidence and rules; audit HP/STA/BLOOD/TH, item inventory, status, time and all named affected NPCs. Offer 2–4 contextual optional next actions after resolution, plus free-form choice.
4. Before showing suggestions, call the pure filtering policy `eligible_actions` conceptually, or execute `python -m unittest verification.test_story_engine -v` when maintaining the engine. Verify that any action has a source and correct location/preconditions. Do not suggest already RESOLVED arcs as current active objectives.
5. When the scene introduces a new hook, classify it as RUMORED unless a witnessed GM outcome proves discovery; add an arc only with a stable ID, source, NPCs/places and current evidence. A rumor is not accepted quest. Store new storyline changes at the next checkpoint; important ARC_CREATED / ARC_RESOLVED triggers immediate flush.
6. A new NPC/locale may need `canon/` or graph seed updates. Commit canonical event + state + arc additions first, then project affected Entities/Relationships to Notion and confirm readback. Never silently change historical events or upgrade last-seen T93 to presence T153.
7. Checkpoint no later than 5 completed turns, upon any major irreversible event, before switching chat, or on request. After each successful flush, verify GitHub branch commit, changed files and state; if Notion projection fails, label its last-sync SHA STALE. If GitHub write fails, in-chat deltas remain **UNSAVED** and must not be described as persisted.
8. No unattended running/scheduled ingest is installed. GM can perform writes during an active turn only, using accessible connectors.

## Action-option presentation contract (based on user screenshot)

- Show a small section **Hành động tiếp theo** at the end of a normal GM reply, preferably 2–4 clickable choices when the chat UI supports interaction; a short plain-text list is an acceptable fallback. Avoid decorative UI that adds latency. Option cards should contain a clear short title and a one-line grounded rationale, using DIL `pressable` or `button` with `GenUI.issueNewTurn` when appropriate.
- Always permit a free-form player instruction. Choosing an option is a new user command, not an automatic action by GM.
- If the world state or user intent makes suggestions irrelevant, omit choices rather than force a stale menu.
- Last accepted state is T154 (see `events/0154.md`): **do not suggest “Cứu Maela” as if still captive, or “Săn Huyết Lang Vương Lv6” as an uncleared boss**. They appeared in a screenshot of an old GM turn, not the current situation.
- Safe T153 choices: ask Edran about Tam Nha, check last verified condition of Maela/Kharzug/pup (now confirmed physically present at the T154 council), inspect Tam Trảo map/key while staying at base, or ask about the sealed stone vessel only after inventory/availability is confirmed. These are directions to choose, not guaranteed NPC presence.
- Display combat tactical map if combat requires it, not merely as decoration in social scenes.

## Arc lifecycle and authority

`RUMORED → DISCOVERED → AVAILABLE/ACTIVE → BLOCKED/RESOLVED/FAILED`, with explicit, evidenced transition edges only. `SUPERSEDED` retains previous accepted branch history. Terminal states cannot reopen solely because a suggestion generator wants variety. Do not create a quest or grant rewards without an on-screen accepted action and causal event. Confirm branch merge or irreversible decisions from the owner/player before changing canon.

## Data boundaries / performance

- **Working Memory:** latest chat turn deltas, only durable after verified checkpoint.
- **Fast GitHub:** `state/quick-start.md`, `state/current.json`, `story/arcs.json`, `story/actions.json`.
- **Long-term:** `events/`, `canon/`, `sources/drive/`.
- **Graph:** Notion Entities/Relationships, source SHA and historical time qualifiers.
- Never query full Notion graph on a routine attack. Avoid new background scheduler/credentials, no implicit auto-sync outside the chat.

## Acceptance / limitations

This V1 creates static seed registries and a pure Python policy library with regression test definitions. It does **not** create a connected runtime command or host hook to run these functions automatically on every incoming chat message. GM must follow the runbook and explicitly use connected GitHub/Notion tools when writing. The tests need real Python execution evidence before their passing status may be asserted.

## T154 continuity delta (read from GitHub)

The player already held a council at the temple with Edran, Maela and Kharzug at T154; the unnamed pup was also present. Kharzug's hind-leg injury persists. Edran explicitly said the three-claw marks and interlocking three-fang collar may relate but do not establish the same organization. No quest acceptance, permanent party recruitment, departure, item consumption or battle. Resources unchanged. These facts supersede T153 uncertainty about NPC presence at the temple **at T154**, but do not prove where NPCs will be on later turns. GitHub `events/0154.md` is the source.
