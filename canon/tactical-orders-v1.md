# HẮC NHẬT — Tactical Orders & Autonomous Resolution V1.0

Status: APPROVED by owner, 2026-10-22. Forward-only from T346; writing rules does NOT play T346, heal, spend anything, reroll, alter HP, or move NPCs. No new combat probabilities, cooldowns or attribute coefficients.

## Purpose
Freeform custom commands, including coordinated instructions, are goals/intentions, NEVER completed screenplay. Separate what Vô Danh orders, what a companion plausibly understands, and what hostile NPCs can independently attempt. The GM adjudicates causally with Harsh but Fair; never force success or force failure for drama.

## Execution sequence (normal FAST in-chat pass)
1. **DECOMPOSE:** Break command into player intent, allied orders, target and conditional sequence. "Vô Danh truy sát A; Maela giữ tầm bắn" means pursue A IF physically possible and request Maela to preserve feasible distance/cover, NOT guaranteed catch/kill/shot/hit.
2. **OBSERVE:** Respect current vs LAST-SEEN target positions, terrain, actual LOS, friendly-fire lanes, weapons and ammunition if verified, relevant range, movement capacity, STA/cooldowns, injury, load, NPC motivations, training, morale, local world time. Unknown remains UNKNOWN; map pixels are not authoritative meters.
3. **LEGALITY + TIME:** Decide independently for each ordered substep whether available now, conditional on movement, delayed, blocked or unknown. Multi-action command is not infinite action economy: moving, looting, searching, aiming and reloading may let enemies react and time elapse. Do not invent new arbitrary action costs.
4. **AUTONOMY:** Allies act based on actual perception/capability, obey feasible directions when reasonable, but may hold a shot, reposition, fall behind or protect themselves; no omniscient remote turret, guaranteed hit or infinite ammo. Enemies have their own goals and limited perception, choose plausible flight, feint, attack, defense, confusion, mistakes, surrender or ambush. Do NOT freeze A waiting for Vô Danh, or make A perfect/omniscient to frustrate the player.
5. **INTERLEAVE:** Adjudicate the attainable substeps with allied/enemy actions at physically plausible time boundaries, respecting terrain and world clock. A shot with clean LOS is a LEGAL ATTEMPT, never an automatic hit. An enemy ducked behind boulder is not a clear target. If the target escapes into unknown terrain, pursuit can become search or lose contact.
6. **VERIFY + REPORT:** Narrate effective outcome, partial outcome, interruptions and misses honestly. Deduct only actual spent HP/STA/BLOOD/ammunition; compute damage only for successful legal contacts with existing rules. Show relevant enemy HP and player resources; report unresolved conditions explicitly, not automatically advancing more turns.
7. **SAVE:** Retain the accepted event delta in session, write GitHub only when regular 10-unsaved-turn checkpoint or consequential action/explicit save/handoff occurs. Do not call GitHub/Notion, invoke Superpowers, generate a new map, or roll World Events merely for a custom order.

## Mandatory invariants
- I1 Intent != outcome. A pursuit command is not guaranteed capture, killing, hit, character reposition or ally obedience to impossible orders.
- I2 Awareness boundary. Last seen != currently visible; no arrow through friendly character/stone or acting on unheard commands.
- I3 Independent reaction. NPCs pursue plausible goals, perceive only what senses and time allow, and can fail as humans do. No perfect counterplay quota.
- I4 Ally capability. Maela maintains a firing lane only if actual terrain/movement/readiness permits; preserving herself and friendlies can require HOLD FIRE.
- I5 Time and economy. Every substep consumes realistic opportunity; opponents do not wait through multi-step commands. A user message does not equal instant completion.
- I6 Fair chance. A good legal player plan may work; GM cannot sabotage it solely for drama, or award auto-win. No fake hidden RNG or unapproved new odds.
- I7 Canon integrity. T345 remains saved / T346 unplayed until actual user-directed play; this document and test fixtures never grant loot, change inventory or retroactively roll.
- I8 FAST response. Use local trusted chat state, no mandatory external calls per game turn; always respect persisted checkpoint provenance when due.

## Non-canonical demonstration
Given A last seen behind stone on a northward winding path, Vô Danh tries to pursue while Maela stays back with bow. GM checks path and stamina; A may flee or counter; Maela may reposition for LOS or HOLD FIRE if V blocks. Without actual visibility no free shot; a clear shot still may miss. This is only a scenario, not T346 gameplay.

## Scope guard
No new initiative mechanics, NPC multi-agent system, full world simulator, artificial odds, additional numeric durability meters or changes to V1.3 progression.
