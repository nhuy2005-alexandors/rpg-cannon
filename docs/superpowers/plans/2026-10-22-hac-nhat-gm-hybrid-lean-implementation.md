# HẮC NHẬT — Hybrid Lean GM / Reliability & Combat Realism V1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Make GM combat/resource checks and multi-actor tactical orders more reliable using a few pure, optional helpers while preserving HẮC NHẬT FAST MODE and the T345 checkpoint.

**Architecture:** Rules as Code, Narrative as AI. Add three independently testable standard-library Python helpers: combat math/availability, grounded tactical predicates, and idempotent turn delta validation. Reuse existing progression, world incidents, story lifecycle and cold-archive helpers; no runtime service, database, scheduler or mandatory per-turn connector/Python invocation.

**Tech Stack:** Python 3 standard library (unittest, copy, hashlib, json, dataclasses only if useful), Markdown, JSON, current GitHub repository.

**Spec:** docs/superpowers/specs/2026-10-22-hac-nhat-gm-hybrid-lean-design.md

## Global Constraints

- Approved architecture spec source commit: d703c74f548f09ff2dbfe4b1f5d973097bd8a3bd; original main baseline at design time: c74f77fe83fd490b85d8739be39056e0419331bb. Refresh current heads before coding; do not silently overwrite concurrent work.
- T345 last accepted SAVED turn; T346 UNPLAYED. Frozen player: Lv6, HP117/170, STA41/110, BLOOD46/50, TH0/20, Souls113, EXP380/400. No T346 world roll, time, movement, loot or battle as part of engineering.
- State/current.json Git blob SHA a03e0bb288fa7bab4bb5147e00c78012edd36acc; maps/active-scene.json SHA b6fd996a9778b52f8b3bf2d601edcae9ea0fc8c7. Original cold archives and quick start remain unchanged. Confirm these baseline hashes at execution start and before merge; if main has changed, investigate rather than replacing current data.
- Authority: verified accepted events > historical archive when relevant > new plausible GM details; unknown remains UNKNOWN. A player instruction is intent, not an achieved result; NPCs and Maela have independent, limited perception.
- Existing Progression V1.3 formulas, Soul once-per-corpse, Huyết Nha ordinary living-target +7 BLOOD cap50, Hấp Huyết heal floor(10% actual lost enemy HP), minimum1 for qualifying positive, maximum5 per combat turn; no damage/heal on misses or invalid targets. No retroactive awards or rerolls.
- No global Hit/Miss/Dodge/Critical % table authorized; current public RNG is forecastable, not secure hidden dice. Existing world_incidents.py may sample only verified eligible opportunities and does not auto-award loot.
- Normal same-chat RPG turn: no routine GitHub, Notion, Canva, Python call, Superpowers invocation or background service. Helpers only on genuinely material math/predicate checks with a real execution path.
- Apply TDD per independent task; verify real RED then GREEN on a fully checked-out repo using Python -m unittest, record command, environment, exit code and evidence. No claim of PASS from authored tests or static checks alone.
- Every new helper pure/deterministic, no network/file writes, no host hooks and no circular imports. Keep bounded files and no unrelated refactoring.

## Review Focus

1. Required cooldown evidence UNKNOWN: helper must not infer READY from elapsed noncombat time or treat missing activation history as zero; test in Task 3.
2. Compound player chase with an enemy behind cover and Maela shooting lane blocked by Vô Danh: pursuing can be conditional but cannot manufacture a clear shot; test in Task 4 and Task 6.
3. Replay of an action ID against a different pre-state, changing costs, or duplicate item/loot claim: reject mismatching replay and never subtract/grant twice; test in Task 5.
4. Legal melee sword hit that overkills a nearly dead enemy: Hấp Huyết is calculated from actual lost HP rather than theoretical damage, capped at 5 heal per combat turn, and +7 BLOOD only on qualified ordinary sword hit; test in Task 2.
5. Absence of historical receipts in compact hot state or unknown Maela ammo: do not infer never paid/infinite arrows; targeted cold restore or UNKNOWN/BLOCKED, and no accidental gameplay advance; test in Task 1, 4 and 5.

---

## File Structure and Interfaces

Keep this a single cohesive implementation plan with three reviewable batches; do not split existing source just for style.

- Create story/combat_mechanics.py: resolve_damage(attack: dict, defender: dict, effects: dict) -> dict; check_skill_availability(skill_id: str, pre_state: dict, clock: dict, action_context: dict) -> dict.
- Create story/tactical_checks.py: check_tactical(intent: dict, observed_world: dict) -> dict.
- Create story/turn_ledger.py: stage_turn(pre_state: dict, intended_turn: dict, proposed_deltas: dict, receipts: list[dict]) -> dict; accept_turn(staged: dict, confirmed_result: dict) -> dict.
- Create verification/test_combat_mechanics.py, verification/test_tactical_checks.py and verification/test_turn_ledger.py: unittest-based synthetic tests; no actual RPG turn.
- Create verification/gm_reliability_scenarios.json and verification/test_gm_reliability_scenarios.py: 36 non-canon fixtures, validator tests, and distinct qualitative GM review cases.
- Create state/gm-fast-contract.md: <= 4096 UTF-8 bytes summary; never outranks canon.
- Modify docs/gm-storyline-protocol.md and canon/rules.md: short pointers + permitted-on-demand helper policy, no duplicate ruleset.
- Leave story/progression.py, story/world_incidents.py, story/proficiency.py, story/engine.py, state/compaction.py, state/current.json, maps/active-scene.json, both cold archives and accepted events unchanged unless a later targeted review proves a separate defect (stop and obtain owner approval for scope expansion).
- No new package manager/dependencies, UI, server, agent loop, or event bus.

Shared test projection for new helpers ONLY (not a second canonical storage format):
    pre_state = {
      "last_completed_turn": 345, "next_turn": 346,
      "resources": {
        "HP": {"current": 117, "max": 170},
        "STA": {"current": 41, "max": 110},
        "BLOOD": {"current": 46, "max": 50},
        "TuHuyet": {"current": 0, "max": 20},
        "souls": 113, "exp": 380
      },
      "inventory_counts": {"test-arrow": 2},
      "cooldowns": {}, "status_effects": {},
      "accepted_actions": {}
    }
The projection must be built from explicitly known data, not automatically from absent keys in historical/current hot JSON. Use original production JSON only read-only for G0 checks. UNKNOWN must be preserved explicitly instead of coercing None to 0. No real player inventory adjustment during fixture tests.

### Task 1 — Frozen Baseline and Synthetic Test Fixtures (G0)

**Files:**
- Create: verification/test_gm_baseline_guard.py
- Test: verification/test_gm_baseline_guard.py
- Read-only: state/current.json, maps/active-scene.json, both T345 cold archives

**Interfaces:**
- Consumes: canonical repository state and archives as read-only test data.
- Produces: an explicit regression guard for the T345 state/map boundary; no runtime package.

- [ ] Step 1: Before any new production file, record current main, the spec branch SHA and baseline Git blob hashes. Create an isolated worktree/branch using superpowers:using-git-worktrees; never directly edit active main.
- [ ] Step 2: Write unittest.test_frozen_T345_and_archive_references asserting last_completed_turn==345, next_turn==346, HP==117/170, STA==41/110, BLOOD==46/50, TuHuyet==0/20, souls==113, exp==380, map ID doc-da-xam-ba-vach-escort-second-bend, valid archive pointers and archive presence. Write unittest.test_no_false_receipt_absence demonstrating historical receipt fields can exist in cold archive despite being missing from hot.
- [ ] Step 3: Run: python -m unittest verification.test_gm_baseline_guard -v. RED must fail on the deliberately unimplemented fixture/archive check, not because the repository cannot import. Fix only the test fixture wiring, then rerun GREEN with zero failures; record concrete SHA receipts. If prior main changed, pause and reconcile before accepting tests.
- [ ] Step 4: Commit baseline guard and fixture only. Command: git add verification/test_gm_baseline_guard.py && git commit -m "test(gm): pin T345 continuity and cold archive guards"

### Task 2 — Combat Resolution and Blood/Heal Boundaries (Batch A)

**Files:**
- Create: story/combat_mechanics.py
- Test: verification/test_combat_mechanics.py

**Interfaces:**
- Consumes: attack {action_id, source_ref, rule_version, legal_hit, landed, raw_damage, kind, is_melee_sword, is_ordinary_sword}, defender {HP_current, HP_max, DEF, living_blood_bearing}, effects {mitigation, attacker_HP_current, attacker_HP_max, attacker_BLOOD_current, attacker_BLOOD_max, hap_heal_already_this_combat_turn}.
- Produces: resolve_damage(attack: dict, defender: dict, effects: dict) -> dict with {action_id, candidate_damage, actual_hp_lost, defender_hp_after, blood_gained, hap_heal_gained, attacker_hp_after, attacker_blood_after, qualified, reason, source_ref}. Return new receipt, never mutate arguments.

- [ ] Step 1: Write test_melee_damage_defense_and_hp_cap: raw=35, DEF=12, mitigation=0, target HP=14 -> candidate_damage=23, actual_hp_lost=14, target HP=0, not 23 HP removed. Write test_shield_mitigation: raw=33, DEF=14, mitigation=7, target HP=9 -> candidate_damage=12, actual_hp_lost=9.
- [ ] Step 2: Write test_blood_and_hap_caps: landed ordinary melee sword versus living blood-bearing target; attacker BLOOD46/50 -> +4 actual despite rule +7; Hấp Huyết floor(10% actual target HP lost), minimum1; with previous Hấp Huyết usage4 in same combat turn -> at most +1 and never overfill HP. Write test_skill_sword_no_ordinary_blood and test_miss_undead_wood_no_rewards.
- [ ] Step 3: Write test_invalid_inputs_fail_closed: unknown DEF/raw, bool masquerading as integer, negative mitigation, illegal contact and HP already invalid produce ValueError/blocked outcome, no invented calculations or retroactive loot.
- [ ] Step 4: Run: python -m unittest verification.test_combat_mechanics -v. RED must be ModuleNotFoundError or missing resolve_damage, not an unrelated environment failure.
- [ ] Step 5: Implement only resolve_damage in story/combat_mechanics.py. Formula: max(0, raw_damage - DEF - proven mitigation); actual=min(candidate,target HP). Hấp Huyết on actual positive MELEE SWORD target HP loss if blood-bearing, not necessarily an ordinary hit; +7 BLOOD only if ordinary eligible. Respect 5 HP cap per combat turn, current HP/BLOOD max. Make qualification reason explicit; never call a random roll.
- [ ] Step 6: Re-run the same test module; GREEN means all tests pass. Commit: git add story/combat_mechanics.py verification/test_combat_mechanics.py && git commit -m "feat(gm): pure combat damage and blood-heal receipts"

### Task 3 — Cooldown and Status Availability Guard (Batch A)

**Files:**
- Modify: story/combat_mechanics.py
- Test: verification/test_combat_mechanics.py

**Interfaces:**
- Consumes: skill_id, pre_state.cooldowns and status_effects, clock {combat_turn}, action_context {known_skill, costs, required_conditions, evidence_refs}. Requires an explicit approved cooldown ready_at_combat_turn (or explicit ready state) and authoritative evidence; absence is UNKNOWN, not READY.
- Produces: check_skill_availability(skill_id: str, pre_state: dict, clock: dict, action_context: dict) -> dict with {status: READY|BLOCKED|UNKNOWN, reasons, source_refs, cost_requirements}. This function never spends resources or advances cooldown counters.

- [ ] Step 1: Add test_explicit_ready_and_blocked: approved READY marker and sufficient exact resources -> READY; explicit ready_at_combat_turn=12 with clock combat_turn=11 -> BLOCKED, clock=12 -> READY. Do not infer ready_at from speculative prior turns.
- [ ] Step 2: Add test_unknown_cd_and_status, where missing activation evidence, unknown combat clock, lost cooldown ledger, or unresolved disabling status returns UNKNOWN; calendar minute increase/rest alone cannot move cooldown. Add test_insufficient_STA_HP_BLOOD_rejects with existing approved cost and exact source reference; no spending on check.
- [ ] Step 3: Run: python -m unittest verification.test_combat_mechanics -v. RED should fail because check_skill_availability is absent.
- [ ] Step 4: Implement the minimal pure tri-state check. Mark explicit contradictions UNKNOWN, hard physical/legal failure BLOCKED, and READY only when all required preconditions are evidenced. Do not assume an unavailable weapon or ammo is magically present.
- [ ] Step 5: Re-run GREEN, then focused progression and proficiency regression: python -m unittest verification.test_progression verification.test_organic_proficiency -v. Commit the same two files with message "feat(gm): source-aware cooldown and skill availability guard".

### Task 4 — Grounded Tactical Order Predicates (Batch B)

**Files:**
- Create: story/tactical_checks.py
- Test: verification/test_tactical_checks.py

**Interfaces:**
- Consumes: intent {source_ref, turn, substeps:[{id, actor, verb, target}]}, observed_world {substeps:{id:{target_visibility, los, crossfire, route, actor_ready, evidence_refs}}}. Allowed verbs initially: pursue, shoot, reposition, interact. Input predicates are evidence-grounded labels (visible|last_seen|unknown; clear|blocked|unknown; traversable|blocked|unknown; ready|blocked|unknown); do NOT compute distances from SVG normalized coordinates.
- Produces: check_tactical(intent: dict, observed_world: dict) -> dict with {overall, substeps:[{id, disposition:ALLOWED|BLOCKED|CONDITIONAL|UNKNOWN, reasons, evidence_refs, possible_reaction_window}], unresolved}. No movement, shooting, turn advancement or NPC AI is executed.

- [ ] Step 1: Write test_blocked_archery: target last_seen behind rock or friendly actor blocks crossfire -> shot BLOCKED, not hit. Write test_clear_los_is_legal_not_hit: visible+LOS clear+crossfire clear+actor READY -> ALLOWED with no hit/damage field. Write test_unknown_ammo_or_LOS_fails_closed -> UNKNOWN and no invented arrow count.
- [ ] Step 2: Write test_compound_chase_with_cover: pursue target last_seen with traversable route => CONDITIONAL follow/search, Maela shot behind rock => BLOCKED. Write test_enemy_movement_not_frozen: result includes possible reaction windows but not claimed enemy death or capture. Write test_unrecognized_verb_and_geometry -> UNKNOWN, not guessed coordinate/distance.
- [ ] Step 3: Run: python -m unittest verification.test_tactical_checks -v; expected RED import/missing function.
- [ ] Step 4: Implement check_tactical using only passed-in categorical facts; source_refs mandatory for asserted clear/blocked facts. Favor UNKNOWN when material input is missing; one individual blocked substep must not automatically make all other substeps blocked. Return each disposition without narrating outcomes.
- [ ] Step 5: Run GREEN and existing contract test: python -m unittest verification.test_tactical_checks verification.test_tactical_orders_contract -v. Commit: git add story/tactical_checks.py verification/test_tactical_checks.py && git commit -m "feat(gm): source-aware tactical feasibility guard"

### Task 5 — Idempotent Single-Turn Ledger (Batch C)

**Files:**
- Create: story/turn_ledger.py
- Test: verification/test_turn_ledger.py

**Interfaces:**
- Consumes: pre_state shared projection; intended_turn {turn, action_id, rule_version, evidence_refs}; proposed_deltas {resource_changes, inventory_changes, cooldown_changes, status_changes, elapsed_minutes}; receipts list of source-grounded intended effects. Action IDs use T###/A## from the GM session, immutable. Only confirmed_result {confirmed:True, action_id, disposition, observed_outcome, verification_refs} authorizes accept.
- Produces: stage_turn(pre_state: dict, intended_turn: dict, proposed_deltas: dict, receipts: list[dict]) -> dict {status:STAGED|REPLAY, input_fingerprint, projected_post_state, delta, pre_state_digest, evidence_refs}; accept_turn(staged: dict, confirmed_result: dict) -> dict {post_state, compact_delta, accepted_receipt}. Both return fresh data with no mutation to source arguments or files.

- [ ] Step 1: Write test_stage_is_pure_and_checks_caps: HP/STA/BLOOD/TH current stay between0/max, no negative Souls/EXP, exact integer checks and item quantities (UNKNOWN quantity cannot be spent); raise ValueError before creating receipt. Test rejected unknown Maela arrow count.
- [ ] Step 2: Write test_unique_ID_and_replay: initial accepted action recorded once; identical replay returns same stored post_state/delta, changed costs/source/pre_state digest with same action_id raises ValueError. This test must exercise reuse of pre_state.accepted_actions, not merely compare two empty dictionaries. No second item spend, Soul payout, skill EXP or RNG redraw.
- [ ] Step 3: Write test_turn_order_and_compound_partial: last_completed_turn345/next346 accepts at most one confirmed T346 delta even if intent has three substeps; unconfirmed action rejected; archived historical receipt absence cannot be treated as proof a corpse was never claimed.
- [ ] Step 4: Write test_status_effect_source_expiration and test_cooldown_changes_require_evidence: statuses preserve source and previously authorized expiration rules, do not fabricate turn duration, changing cooldown without approved action/source fails closed. elapsed_minutes nonnegative and not automatic passage of battle turns.
- [ ] Step 5: Run: python -m unittest verification.test_turn_ledger -v. RED expected import failure or missing stage_turn/accept_turn.
- [ ] Step 6: Implement exact two functions using deepcopy and canonical sorted-key JSON SHA256 digests. Replay checks fingerprint before turn sequence, preserves accepted old post-state rather than increments next_turn again. A digest is reproducibility of inputs, NOT evidence truth or secret signing. Idempotent accept stores source receipts in projection; do not modify state/current.json or create a second durable authority.
- [ ] Step 7: Run GREEN and source regression: python -m unittest verification.test_turn_ledger verification.test_story_engine verification.test_state_compaction -v. Commit: git add story/turn_ledger.py verification/test_turn_ledger.py && git commit -m "feat(gm): validated and idempotent in-session turn receipts"

### Task 6 — Adversarial Scenarios and Genuine GM Evaluation (G3)

**Files:**
- Create: verification/gm_reliability_scenarios.json
- Create: verification/test_gm_reliability_scenarios.py
- Create: verification/gm_reliability-review.md (fill findings at execution; no fabricated scores)

**Interfaces:**
- Consumes: three new pure helpers, frozen T345 fixture and existing tactical/world incident policies.
- Produces: 36 distinct NON_CANONICAL fixture cases and algorithmic test assertions, plus an honest separate qualitative GM review; no new accepted events.

- [ ] Step 1: Define 36 independently specified cases with stable IDs, preconditions/evidence, action, expected admissible/blocked outcomes, forbidden outcomes and source version. Allocate 12 combat/resource/cooldown, 12 chase/LOS/companion/enemy agency, 12 ledger/unknown/rest/loot/random-event eligibility/restore. Include adversarial damaged equipment and unknown ammo; never introduce a real T346 event.
- [ ] Step 2: Write test_case_count_groups_and_unique_ids, test_each_case_has_provenance_expected_forbidden and test_programmatic_predicates_against_pure_helpers. RED on absent fixture/required fields, GREEN only after every mechanistic case is actually checked; do not treat fixture presence as a behavioral PASS.
- [ ] Step 3: Run: python -m unittest verification.test_gm_reliability_scenarios -v, then add minimum scenario fixture data and deterministic assertions until GREEN.
- [ ] Step 4: If available, obtain at least 30 actual GM responses to independent, synthetic scenarios with no real player state mutation; record rubric for no auto-success, no omniscience, proper UNKNOWN, resource math and independent NPC agency. Mark separately PASSED/FAILED/NOT_RUN per scenario; do not say an LLM was independently tested based only on programmatic assertions.
- [ ] Step 5: Commit tests/fixtures and review artifact with accurate coverage labels. Command: git add verification/gm_reliability_scenarios.json verification/test_gm_reliability_scenarios.py verification/gm_reliability-review.md && git commit -m "test(gm): adversarial reliability fixtures and review receipts"

### Task 7 — Lean GM Handoff and Integrations (Batch C)

**Files:**
- Create: state/gm-fast-contract.md
- Modify: docs/gm-storyline-protocol.md
- Modify: canon/rules.md
- Test: verification/test_gm_fast_contract.py (new)

**Interfaces:**
- Consumes: names/signatures and source evidence limitations from Tasks 2–6.
- Produces: readable <= 4096-byte rules summary and two small pointers, NOT a new canon authority or installed runtime hook.

- [ ] Step 1: Write RED tests for length <=4096 UTF-8 bytes; no hardcoded stale T153/T204 commands; includes T345->T346, intent!=outcome, UNKNOWN, source-verified costs/LOS, public-seed caveat, world-incident eligibility, and checkpoint cadence. Verify the runbook explicitly says Python helper calls are OPTIONAL and NOT automatically installed.
- [ ] Step 2: Run: python -m unittest verification.test_gm_fast_contract -v; expected missing runbook/contract content RED.
- [ ] Step 3: Author small state/gm-fast-contract.md from approved current canon. Only add short links to this file and helper APIs in canon/rules.md and docs/gm-storyline-protocol.md; do not paste duplicate 20 KB rules. Do not change state/quick-start.md during planning or gameplay; if the implementation needs a startup pointer later, keep it additive and read-only-state.
- [ ] Step 4: Run GREEN and syntax/document integrity checks. Ensure no docs promise automatic Python, unattended clock, secured hidden RNG or extra GitHub calls. Commit: git add state/gm-fast-contract.md canon/rules.md docs/gm-storyline-protocol.md verification/test_gm_fast_contract.py && git commit -m "docs(gm): compact fast-path rule handoff and optional helpers"

### Task 8 — Integration Regression, Performance and Rollout Gates (G2, G4, G5)

**Files:**
- Modify only genuine defects found in files from prior tasks with targeted RED first.
- Create: verification/gm-hybrid-lean-final-review.md with test receipts/performance/outstanding limitations.

**Interfaces:**
- Consumes: the full planned implementation branch, prior commits, synthetic non-canon scenario outputs.
- Produces: GO/NO-GO recommendation supported by source/readback/tests/latency evidence. No live gaming turn.

- [ ] Step 1: Run from isolated full repository checkout: python -m unittest discover -s verification -p 'test_*.py' -v. Record Python version, total run/fail/errors and exact command. Existing red tests are not waived; distinguish pre-existing failures with baseline receipts, no blanket skipping.
- [ ] Step 2: Run explicit negative/replay tests: same action ID different pre_state; cooldown UNKNOWN; wall-blocked Maela shot; overkill Hấp Huyết cap; duplicate world opportunity; event sampler offers NO automatic loot; cold archive relevant historical receipt does not become false by omission.
- [ ] Step 3: Test same inputs with and without optional pure helper through a reproducible 20-step synthetic scenario set. Record correct outcomes, number of external connector calls, real wall-clock timings by category (normal, consequential, checkpoint). Compute comparable p50/p95 only from measured samples; no claim that function runtime alone is actual ChatGPT end-to-end latency. If representative GM execution/call path cannot be measured, mark performance UNVERIFIED and withhold FAST performance acceptance.
- [ ] Step 4: Validate canon state/current.json and maps/active-scene.json still have original pinned Git blob SHAs, no new T346 event, no historical modifications, and 36 fixture scenarios explicitly non-canon. Detect uncommitted files, conflicts or branch drift and stop before integration.
- [ ] Step 5: Perform fresh whole-branch independent review focusing on critical integrity and scope boundaries, documenting reproducer, severity and either changes required or acceptance. If independent reviewer unavailable, mark UNREVIEWED and do not fabricate signoff.
- [ ] Step 6: If full tests, quality, canon-freeze and measured performance pass, prepare a fast-forward-only GitHub update using expected-main-SHA guard and read back commit/files. Do not merge without owner-authorized execution/method and the normal pre-merge review. If a gate fails, leave code isolated, publish specific blocker, and preserve original gameplay canon.
- [ ] Step 7: Commit verification receipts to implementation branch: git add verification/gm-hybrid-lean-final-review.md && git commit -m "test(gm): integration, baseline and performance verification receipts"

## Plan Self-Review and Stop Conditions

Coverage: Sections1–2 -> Global Constraints and Task1; architecture/API boundary -> Tasks2–5; GM turn fast path -> Tasks4,7; UNKNOWN/failure/receipt correctness -> Tasks2–6; RNG existing/no new hit table -> Global Constraints and Task6; G0/G1/G2/G3/G4/G5 -> Tasks1,2–5,8,6,8,8 respectively. No prompt-only assurance is counted as automated enforcement. The synthetic pilot is a benchmark, not a fabricated in-world T346–T365.

Implementation starts only after owner reviews THIS written plan and explicitly selects an execution method. For this repo, Native/executing-plans is recommended for the tightly coupled three pure helper interfaces and the lower overhead, plus a single whole-branch review; Subagent-driven offers stronger per-task independence at higher context and time cost. The current step is planning ONLY: do not modify source, current state or gameplay in this commit.
