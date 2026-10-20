# Superpowers-guided methodological audit — HẮC NHẬT Loot/Soul/Skill Progression V1.2

Date: 2026-10-20. Scope: READ-ONLY review of the newly owner-approved rules baseline and correction (documentation of findings only; this report does not change game mechanics). Reviewed: `canon/loot-skill-progression-v1.2.md`, `canon/rules.md`, `state/current.json`, `events/rules-amendment-T194-v1.2.md`, `state/quick-start.md`, `README.md`, `verification/check_state.py` and original T185–T194 event receipts. Method: Superpowers brainstorming + verification-before-completion principles; single model self-review, **NOT INDEPENDENT reviewer / human adjudication**, no actual player combat simulation of new mechanics, no live RNG subsystem deployed.

## Scope and authority

- The user approved soul scaling by level and threat, appropriate soul drops on actual loot, conditional TH, and mastery EXP & chance bonuses by skill use. Frozen baseline is V1.2. Audit findings below are proposals only: owner approval and auditable delta spec required for V1.3.
- No new RPG turn narrated; current last completed T194, next T195. Frozen active encounter: Vô Danh HP90/170 STA53/110 BLOOD21/50 TH0/20 EXP205/400, amended souls29; proof2/3; C living100/100 ~12m and detected Vô Danh, has not attacked. No auto-loot or quest reward. Two corpse reward claims A+B already recorded once.
- Historical T194 souls5 remains in original T194 receipt, with separately linked C194-SOUL-V1.2 additive +24. Numeric authority state current souls29. Graph Notion T153 relationships not silently changed by rules doc.

## Verification performed

- Content/readback and pure invariant arithmetic: **11/11** checks from current GitHub state, including two unique claim IDs, delta 5+12+12=29, no duplicated A/B claim, TH0, XP205, 2 fang pairs, C HP100, preserved T194 original receipt, 13 learned-skill mastery entries initialized at0, rank2 Parry and Nhị Liên preserved, rules supersession, correct T195. These are state assertions, **not gameplay engine integration tests**.
- Analytical yield examples player Lv6, normal unless specified: target L1 R1 D0.5=>2; L3 D0.75=>6; L4 D1=>10; L5 D1=>12; L6 D1=>14; L10 D1=>22; elite L10 R2.5=>55; Boss L20 R6=>252; World Boss L50 R12=>1224 souls. These are a formula pressure probe, not evidence of in-world monster levels.
- Skill throughput with 25% additional +5 only on eligible successful use: E[EXP/use]=2+0.25*5=3.25. Approx successful casts Common Lv2→3 90/3.25=27.69, Rare Lv2→3 135/3.25=41.54, Rare Lv1→2 60/3.25=18.46 (not guaranteed ranks at those counts).
- `verification/check_state.py` still pins T153 and legacy resources; NOT a current T194 validator. Do not claim this stale test script passes current state. No actual verified RNG +5 rolled here.

## Findings, impact, action contracts

### F01 — CRITICAL / Calibration without a world-owned threat-level source
`L_reward` is adjustable GM estimation; A/B were fixed at L5 for first correction but no evidence-based objective calibration methodology or freeze-at-spawn record. Abuse: same HP/stat/damage yields different soul amounts if GM wants more/less rewards. Recommendation: define enemy template registry `enemy_type_id, threat_level, rank, template_version, traits, reference power band` and spawn snapshot pinned before player commits fight; do not infer solely from HP or successful kill. Fallback unknown level must use explicitly owner-accepted challenge-band defaults, mark estimate, and never assign after loot opportunistically. Keep T194 accepted +24 unless owner explicitly authorizes a new correction event. V1.3 gate.

### F02 — CRITICAL / Skill XP threshold does NOT itself level a skill
Owner desired skill upgrades upon enough experience. Current V1.2 marks `LEVEL_UP_ELIGIBLE` but leaves effect undefined and hence cannot genuinely auto-level. Recommendation: per-skill `next_rank_contract` with rank, attack/evasion/coefficient/cost changes, caps and upgraded effects, preregistered before threshold. Make promotion atomic only after sufficient EXP, valid preregistered contract and rank cap; carry XP over, emit `SKILL_LEVEL_UP` receipt and show delta. If contract absent, explicitly show BLOCKED_PENDING_RULE rather than imply leveled. Design Lv3 Parry and Nhị Liên first; no retrospective Edran exam requirement unless preregistered as promotion condition.

### F03 — MAJOR / Probability without verifiable RNG
Nominal 25% for +5 cannot be operational without a reproducible actual roll; GM freehand success violates reliability. Recommendation: versioned campaign RNG algorithm using a fixed registered campaign seed, immutable per-use ID/skill key, replay-safe draw (e.g. `u = first_32_bits(SHA256(seed|turn|encounter_id|skill_id|use_seq)) mod 10000; bonus if u<2500`). Commit or retain full input, output and seed provenance with receipts. Protect duplicate/reroll and preselected outcomes. Test uniformity on a seeded batch and collision/idempotency; no actual roll = PENDING_UNROLLED, not recorded +0/failed. For non-coding interactive turns use a small reproducible calculator/tool on eligible uses, not pretend a UI hook exists.

### F04 — MAJOR / Difficulty factor D has open and discontinuous bands
Above-player threshold (1.25–1.5) unspecified; D changes abruptly near weak3, weak5 level gaps. Current safe D1 for stronger monsters undershoots the user's scaling intent. Recommendation: define explicit all-integer `delta = L_reward-player_level_at_kill` table and a bounded monotonic curve, e.g. D=max(0.5,min(1.5,1+0.1*delta)) or transparent piecewise table, chosen only after testing equivalence with already approved A/B (delta=-1 stays D1 under old rule, proposed curve would imply D0.9 and change reward; require owner approval to amend). Specify rounding ONCE at end, player level reference, summon/party scaling, prewounded mobs and weak-foe repeat penalties; freeze old A/B amount.

### F05 — MAJOR / Farming valid skills through low-risk repetitions
+2 useful /+1 failure can reward farming soft target, summoned mobs, friendly sparring dummies, purposely failed Parry, recasts without challenge, and passive HapHuyet proc per hit. Recommendation: `practice_context_id` and threat/novelty guard, one skill EXP receipt per meaningful activation and per passive opportunity, encounter caps with diminishing returns after equivalent repeated attacks, distinct authentic Edran practice certification. Do not ban all legitimate training, but no infinite XP from staged harmless targets. Test multi-hit Nhị Liên counts once and Parry reaction budget remains7STA/try.

### F06 — MAJOR / Economy inflation vs item prices/rewards
Scalable souls dwarf the current 20-soul bounty quickly: three ordinary L5 hyenas yield 3*12=36 plus quest20, Boss L20 yields252 and World Boss L50 yields1224. Prices/sinks and NPC exchange rates are not benchmarked. Recommendation: build canonical shop/equipment/skill-upgrade cost ladder (no hidden rescaling), calculate expected souls per 30min/1h and affordable purchases through Lv1–20/elite runs. Tradeoff: preserve generous soul gain but calibrate consumption/upgrades/travel costs; do NOT nerf V1.2 silently.

### F07 — MAJOR / Tử Huyết presence and amount underspecified
Valid source = death/corruption residue but no source tier, drop amount, extraction hazards or overflow handling. Recommendation: explicit `TH_source_type, purity_grade, guaranteed_or_chance, extraction_conditions, yield_distribution, TH_cap_overflow` for undead/dark elites/bosses. No free TH on ordinary hyenas. Make yield conditional on actual evidence, not based on wanting resource to cast Tử Huyết Hồi Sinh.

### F08 — MAJOR / Loot trigger, corpse ownership, idempotence edge cases
A first valid fang harvest grants souls once, but interrupted multi-stage harvest, corpse theft, looting a found corpse by another NPC, dismemberment, looting under pressure and revived/cloned summons are not specified. Recommendation: exact state machine `UNLOOTED -> PARTIALLY_HARVESTED? -> SOUL_CLAIMED -> DEPLETED`, unique corpse/encounter identity and per-resource claim keys, separate soul/TH/item flags, deterministic event idempotency. Failed harvest costs time and may provoke attacks but earns no phantom rewards. All boss replay/de-dup receipts retain old canon precedence.

### F09 — MAJOR / Current validator and Notion summary are stale
`verification/check_state.py` asserts last_turn153, resources HP115 STA85 BLOOD25 souls5, so it does not validate current T194; future reviewers could mistake failures or rely on old success. Notion Hub remains T153 historical graph; newly added rules index under Hub is current only for rules. Recommendation: make turn-agnostic schema validator with receipt-chain correction reconciliation, replay-aware rewards and mastery state; preserve original T153 checker explicitly as historical fixture. Update Hub's display to distinguish NPC graph snapshot T153 vs latest GitHub T194 and rules V1.2, without asserting stale graph rows are synchronized.

### F10 — MAJOR / Skill rarity/level metadata incomplete
During audit a concrete metadata bug was **repaired without altering gameplay**: Huyết Trảm, Thiết Cốt Trảm, Tử Huyết Hồi Sinh, Tử Huyết Cảm Tri had unverified Common/Rare tiers assigned during registry creation; now `rarity=UNVERIFIED`, `next_threshold=null`; Tử Huyết Cảm Tri rank unverified -> `level=null`. Skill EXP can accrue from T195, promotion by class-specific threshold waits canonical rarity validation. No invented rank eligibility. Recommend create skill registry with explicit provenance `learned_turn/source/rank/rarity/current_effect` from historical events.

### F11 — MODERATE / Inconsistent combat status effects
Wounded hyena shoulder/legs impaired mobility in narration without registered wound tier, duration or movement penalties. Propose named statuses (Bleeding, Wounded Limb, Staggered, Fear, Exposed Guard, Corruption), action application, resistances, immunity, expiration and capped stacking. Distinguish environmental narration from formal debuffs; no automatic bleed ticks from generic sword hits.

### F12 — MODERATE / Resource/action-economy interaction completeness
Casting then "guarding", dash-plus-attack, parry reaction count, stamina burn and resting in unsafe terrain need consistent sequencing in future fights. Propose per-turn action budget (move/main/reaction), interrupt/ambush rules, enemy autonomous actions, windup and recovery windows, `guard_posture` vs `guard_skill`, cooldown time transition (combat turns vs 8min noncombat), exhaustion thresholds, carrying capacity constraints for loot. Preserve Parry Lv2 7STA and no free riposte.

### F13 — MODERATE / Presentation and audit provenance for chance rewards
Every game result should include compact `Enemy HP | Souls gained/claimed | TH earned | Skill EXP delta | Skill Lv | HP/STA/BLOOD`, with source tags and rng receipt if used. Players requested only one simple SVG/canvas tactical map in combat, not separately generated artwork or duplicative caption. Add regression tests for exactly-once loot, buff/skill activation, multi-hit overkill Hấp Huyết, CD, XP threshold/carry and T194 correction replay.

## Recommended repair sequence (NOT APPROVED)

1. **V1.3 CRITICAL gates:** F01 template threat registry, F02 rank effect contracts, F03 verifiable RNG and F08 corpse loot idempotency; minimal mechanics before another loot or rank increase.
2. **V1.3 balance pass:** F04 fully defined D, F05 anti-farm, F06 3–5 economy fixtures, F07 TH source/drop tables. Preserving T194 +24 as recognized correction avoids silent rerolls.
3. **V1.3 verification & presentation:** F09 turn-agnostic tests; F10 complete missing rank metadata; F11–F13 statuses, action contract, concise receipts. Do not implement or alter numeric V1.2 baseline until owner reviews specific deltas.

## Acceptance-test outline for future V1.3

- SOUL-01: same corpse first verified harvest gives fixed yield and a unique claim; second harvest gives0 souls; quest proof remains separate.
- SOUL-02: L_reward, R, D and version frozen at spawn and persisted, no adjustment via player narrative or kill ease.
- SOUL-03: boundary D values for delta(-5,-4,-3,-2,-1,0,1,3,5), monotonic after final rounding, no negative/zero monster yield unless an explicitly non-soul-bearing entity is exempt.
- TH-01: normal living hyena gives0TH; proven corruption source gives only preregistered amount; TH cap overflow correct.
- SKILL-01: action success +2, legitimate failure +1, invalid +0, no bonus attempt for invalid/failure.
- SKILL-02: 25% seeded bonus deterministic across repeated state reads and independent of retelling; retried action same use-ID awards at most once.
- SKILL-03: Nhị Liên two hits = one skill activation and one XP award, even when first hit kills; no free third hit.
- SKILL-04: crossing threshold triggers *specified* atomic rank promotion once, carried excess, old rank effect not double stacked; if specification lacking hold with explicit BLOCKED status.
- STATE-01: replay T194 original receipt5 + correction+24 produces29 without changing HP90 STA53 BLOOD21 TH0 EXP205, next195; A/B claims unique.
- STATE-02: Notion rule page is read-only derivative of GitHub canon, T153 NPC graph not falsely marked current.
