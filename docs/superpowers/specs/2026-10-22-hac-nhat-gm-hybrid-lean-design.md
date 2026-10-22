# HẮC NHẬT — GM Hybrid Lean / Reliability & Combat Realism V1.0 — Design Spec

Date: 2026-10-22
Status: DESIGN SPEC — AWAITING OWNER REVIEW
Repository baseline: c74f77fe83fd490b85d8739be39056e0419331bb (main at initial inspection)
Scope: future-only GM improvements; T345 remains the last accepted gameplay turn, T346 is unplayed.
Design decision: Hybrid Lean = Rules as Code, Narrative as AI. This design does not authorize implementing code or changing battle odds before owner review of this written spec and a separately approved implementation plan.

## 1. Goal and user intent

Game Master must respond to custom instructions quickly and fairly, with independent NPC behavior and meaningful environmental events, while minimizing arithmetic errors, false RNG receipts, lost cooldown/status history, and continuity loss across thousands of turns. The game must remain an interactive dark-fantasy RPG, not a software demonstration.

Priority order: canon integrity and causality > resource/math correctness > independent agency > response-time efficiency > tool/token cost. Normal turns stay FAST: zero routine GitHub/Notion/Canva calls and no mandatory Python execution. An optional helper is used when deterministic checks are worth their cost; no automatic invocation is claimed.

Successful outcome is reusable components with narrow input/output contracts, proven by actual tests and limited pilot observations. Source of truth stays the verified in-chat state plus saved state/current.json and append-only accepted event receipts; design documents do not modify gameplay.

## 2. Baseline inventory, constraints and non-goals

Existing pure helpers, verified by reading source:
- story/progression.py: soul_yield, encounter_bonus, claim_loot, deterministic Skill EXP draw and skill_use, respec_branch; reuse exact formulas, no reimplementation.
- story/proficiency.py: proficiency receipts; reuse if applicable, do not merge incompatible skill/proficiency meanings.
- story/world_incidents.py: evidence-gated incident opportunities and optional explicit-odds contest. Public seed is predictable. The helper proposes an incident and does NOT automatically award loot or roll every turn.
- story/engine.py: arc lifecycle, checkpoint_needed and post_turn flags; returned flags are not persisted writes.
- state/compaction.py: snapshot split/restore with pinned cold archives; historical fields may be absent from hot state but remain archived.
- canon/tactical-orders-v1.md: player intent != guaranteed outcome; ally/enemy autonomy, visibility, terrain and finite time.
- docs/gm-storyline-protocol.md: logical session_base/current_state/recent_turn_deltas/unsaved_turns, 10 unsaved completed turns or major event checkpoint, readback verification. No ChatGPT host hook is installed.

Non-goals for V1.0: full RPG engine, auto-played turns, NPC agents, physics/pathfinding/navmesh, new LLM router, database, event bus, web service, background scheduler, new equipment durability meters, arbitrary numeric combat accuracy/critical/dodge chances, new status ailments or changes to existing V1.3 combat/loot formulas, reward rebalancing, retroactive skill bonuses or historical rerolls. The existing World Incidents probability tables remain unchanged.

## 3. Architecture and boundary of responsibility

GM (LLM): interprets freeform player command, generates plausible declared intents and sensory observations, selects physically possible NPC counter-actions, adjudicates unresolved narrative ambiguity, manages pacing and writes story. It must NOT manufacture a source-known measurement, assert it used a calculator when none ran, or treat a proposed event as resolved.

Pure deterministic helpers (on demand; not autonomous):
A. Combat Mechanics: calculate post-defense damage, HP caps and strictly evidenced resource effects; validate skill availability from explicit cooldown/state. No probability is silently assigned.
B. Tactical Validation: evaluate declared, grounded LOS/route/last-seen/companion availability predicates. Produce ALLOWED, BLOCKED, CONDITIONAL or UNKNOWN with evidence; GM retains authority for complex spatial/narrative events. No omniscient enemy AI and no numeric extrapolation from schematic map pixels.
C. Turn Ledger: stage a proposed single-turn state delta, validate resource bounds, duplicate IDs, cooldown/effect changes and accepted observations, and apply exactly once after adjudication. A staged delta is not an accepted or saved game turn.

Existing Progression, World Incidents, Engine and Compaction remain as imports when relevant. Do not duplicate their policies or introduce one master service coordinating every action. Proposed new small source units:
- story/combat_mechanics.py: pure damage/resource and skill-availability helpers
- story/tactical_checks.py: pure grounded predicate evaluation
- story/turn_ledger.py: immutable pre/post reconciliation and idempotent receipts
- state/gm-fast-contract.md: <= 4 KiB handoff/runbook for new-chat startup only; a summary, NOT new canon authority.
- verification/test_combat_mechanics.py, verification/test_tactical_checks.py, verification/test_turn_ledger.py and targeted adversarial scenario fixtures

Import discipline: dependency only Python standard library plus existing in-repo pure helpers; no cyclic imports. Files should stay focused and small. Do not create a GUI, generic plugin framework or provider abstraction.

## 4. Interfaces and data contracts

4.1 Common inputs. All computation consumes explicitly supplied immutable pre_state and evidence: saved/working turn, action_id, skill_id when needed, measured or legally established range/LOS, exact numeric resources if known, and source_ref such as accepted event turn or map revision. Unknown is represented as UNKNOWN, not numeric zero or assumed absence. Source turn and rule_version travel with each receipt. Helpers must not reach out to GitHub, Notion or external networks.

4.2 Damage function:
resolve_damage(attack, defender, effects) -> DamageReceipt
Required: accepted legal hit (or documented other interaction), nonnegative integer raw damage, defender DEF and other already-proven mitigation, defender known current/max HP, explicit applicable approved modifiers. Compute candidate = max(0, raw - DEF - proven_mitigation); actual_hp_lost = min(candidate, hp_before); hp_after = hp_before - actual_hp_lost. No implicit crit/hit probability or live mutating writes. For qualifying ordinary landed sword hits versus living blood-bearing target, apply the separately established +7 BLOOD only with cap, and Hấp Huyết's floor(10% actual HP lost), min 1 and cap 5 per combat turn, with per-turn accumulator and real current HP cap. Skill strikes, misses, non-blood targets or inorganic materials do not grant ordinary hit BLOOD. Where an already approved exception exists, defer to its versioned rule contract; no double-award. Return raw, mitigation, candidate, actual HP removed, resource deltas, eligibility rationale and source ids. Validation failure cannot grant damage/loot.

4.3 Skill check:
check_skill_availability(skill_id, pre_state, clock, action_context) -> AvailabilityReceipt
Tri-state READY/BLOCKED/UNKNOWN with reasons and evidence. Cooldowns use only accepted combat-turn activations and versioned skill cost/rule definitions. Calendar time/ordinary rest does not silently advance a combat-turn counter. A cooldown with missing activation or previous inconsistent narration remains UNKNOWN pending targeted evidence; no imaginary number, automatic refresh or free recast. Never create new cooldowns or rewrite old turns. A separate accepted action updates cooldown ledger once.

4.4 Tactical check:
check_tactical(intent, observed_world) -> FeasibilityReport
Result contains per-substep disposition ALLOWED/BLOCKED/CONDITIONAL/UNKNOWN, known/last-seen target, LOS and crossfire state, traversable path evidence, companion perception and equipment readiness, time-consuming substeps, and unresolved conditions. This is a guard, not line-of-sight simulation: geometric truth is supplied by verified map+event observations, not invented from SVG coordinates. If target hides behind rock, ally shot BLOCKED unless repositioning truly restores LOS; even ALLOWED means legal attempt only, never automatic hit. GM then interleaves autonomous enemy and ally reactions according to Tactical Orders V1.0.

4.5 Ledger:
stage_turn(pre_state, intended_turn, proposed_deltas, receipts) -> StagedTurn or ValidationError
accept_turn(staged, confirmed_result) -> PostState + CompactDelta
Exactly one logical game turn per user-directed action; multi-step instructions may end PARTIAL, BLOCKED or UNKNOWN and can trigger enemy reactions. Stage has no storage effects. Source identifiers for attack/corpse claims/consumables/world opportunities are immutable. Duplicate action_id returns an identical accepted receipt when source+precondition match, otherwise rejects conflicting replay; must not replay world side effects or spend resources twice. All HP, STA, BLOOD, TH, Souls, EXP, ammunition, inventory possession, skill mastery, cooldown/status and elapsed-time deltas are checked against known bounds. Unknown inventory quantity cannot be invented; fail closed on a required unknown resource. Status effects record source, condition and expiration rule as accepted, without inventing duration. Historical cold archives are consulted only when a material predicate requires them.

Receipt schema: kind, action_id, turn, rule_version, evidence_refs, pre_state_digest, input_parameters, disposition, observed_outcome, resource_deltas, post_state_digest, verification_status. Digest uses canonical sorted-keys serialization; digest proves reproducibility of given data, NOT truth of narrative inputs. No falsely claimed signed or secret proof. Receipts and deltas remain in session until actual checkpoint write and readback, then marked SAVED.

4.6 RNG boundary. Existing story/progression.rerollable_draw and story/world_incidents sampling are reused when actually called with eligible immutable IDs. Public RNG remains forecastable; label honestly. Existing world-event helper's explicit chance argument is NOT authorization to invent a combat hit table. A universal hit/miss/dodge/critical probability model is a separately scoped numeric rules decision with comparative tests and player approval. Until that gate, the GM can narrate misses on grounded context but must not invent quantitative odds or claim an executed roll.

## 5. Game Master turn flow and failure behavior

Normal same-chat turn:
1. Read trusted logical working state already in context; no routine remote fetch.
2. Parse freeform intent, including Vô Danh action and Maela/other companion orders.
3. Identify the smallest material legal/visibility/skill/math checks; use no helper for purely narrative exchanges.
4. Interleave feasible actions, enemy objectives and own mistakes, allied agency, time and verified qualified World Incidents opportunities. Never convert command into guaranteed success or script failure merely to create drama.
5. If numeric calculation required, call applicable pure helper IF a Python execution path is genuinely available and action requires it. If unavailable, perform explicit source-grounded calculation and verify arithmetic locally; do not say code executed.
6. Stage and accept one turn only after adjudicating actual outcome. Display meaningful causal result, relevant HP/STA/BLOOD/TH/Souls/EXP, enemy HP known, costs, skill cooldown deltas, and concise options. Reuse tactical map base unless positions/terrain materially changed.
7. Update unsaved in-session deltas. At 10 completed unsaved turns, material irreversible event or handoff, commit changed state/events/maps to GitHub with expected-head compare and successful readback. Notion only for real NPC/relationship changes.

Failure contract:
- Contradictory state or required missing authoritative value: UNKNOWN/BLOCKED, targeted lookup; never infer from outdated quick-start or pretend archive deletion.
- Negative or out-of-cap resources, duplicate claim, illegal reach/LOS: reject candidate action outcome before committed state.
- Failure or unavailability of optional tool: retain valid in-chat adjudication with honest verification status, no fictitious tool execution or persisted receipt.
- Checkpoint conflict or failed readback: keep unsaved deltas, do not advance durable watermark; resolve conflicting versions before retry.
- New spec/maintenance commit: no RPG time, EXP, items, movement or RNG sampling.

## 6. Testing and evidence gates

G0 — frozen baseline: main HEAD recorded; T345 source snapshot and map archived/pinned. Never rewrite historical accepted turns or T345 HP117/170, STA41/110, BLOOD46/50, TH0/20, Souls113, EXP380/400, Maela last seen ~5m behind.
G1 — unit Red/Green: each new pure function receives failing tests first, then minimal production code. Validate formula boundaries (defense, 0/overkill HP, cap HP and BLOOD, Hấp Huyết one-per-turn cap), cooldown ready/blocked/unknown, LOS+crossfire, compound order with enemy moving, idempotent receipts, and invalid state.
G2 — integration: run complete offline repository unittest discovery (including existing progression, story, world incidents, compaction, tactical contract) on a real isolated checkout. Explicitly report tests run, failures and environment. Tests written into GitHub but not executed are NOT PASS.
G3 — adversarial non-canon replay: >= 30 independently defined situations across pursuit/cover/arrow lanes/skill activation/statuses/loot/time/rest/random event eligibility; no regression to accepted story. Include a few deliberate contradictory/missing-evidence fixtures. Human qualitative GM grading is reported separately from algorithmic test results; never claim prompts alone mechanically guarantee GM behavior.
G4 — FAST Mode performance: compare a representative 20-turn synthetic pilot against existing FAST baseline, with normal vs consequential/checkpoint turns separated. Log wall-clock p50/p95, tool calls, outcome correctness and evidence-recovery exceptions. Target for normal in-chat turns is 0 routine connector calls and no observed systematic p50/p95 regression relative to a recorded comparable baseline; do NOT claim a speed gain without actual measurement. No continuous autonomous runner is installed.
G5 — branch readback: verify changed files/commit SHA and exactly preserved gameplay snapshot, then require owner plan authorization before source rollout. Owner approves the spec separately; subsequent implementation plan is a distinct gate.

## 7. Small-batch implementation boundaries (only after approval)

Batch A: combat math + status/cooldown guard and focused tests. Do not tackle new probabilistic hit formula.
Batch B: tactical predicate guard and compound-command adversarial fixtures. GM retains narrative agency.
Batch C: turn ledger/idempotent receipts, short GM Fast Contract and integration+pilot. Reuse progression/incidents/engine/compaction in place.

Each batch must have own regression and narrow changed-file review. If the selected integration approach demonstrably adds more latency or complexity than value, prefer a smaller pure helper and the existing GM in-chat procedure. A full event-driven runtime is NOT a fallback.

## 8. Acceptance criteria and explicit exclusions

Acceptance is conditional on (a) proven state/scene preservation and no historical retcon, (b) deterministic resource math and duplicate-receipt prevention, (c) never treating custom intent as outcome, (d) assistant/NPC autonomy without omniscience, (e) correct UNKNOWN on missing evidence, (f) complete real tests and a measured pilot, (g) no unsupported RNG or secret GM precommit claims, and (h) FAST response preserved under representative conditions.

This spec is the only deliverable in the current Superpowers brainstorming stage. Do not generate implementation plan or modify production files until the owner reviews and explicitly approves this committed document.
