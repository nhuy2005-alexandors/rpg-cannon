# HẮC NHẬT — Loot & Skill Progression Rules V1.2

Status: **OWNER-APPROVED BASELINE** after T194, BEFORE T195 (2026-10-20). Source: user explicitly requested souls upon looting eligible enemy corpses, Tử Huyết only if present, skill EXP/probabilistic bonus/level-up by use, and soul amounts scaled by enemy level and actual challenge. Supersedes former generic "Souls from defeated foes: ceil(base ×1.25)" rule for qualifying loot from this amendment onward; never silently revise historical rewards. External Superpowers audit requested separately. Audit proposals do not automatically amend this baseline.

## 0. Execution boundaries

- This is an approved GM game rule, not a hook, deployed program, real RNG, or an additional RPG turn. `last_completed_turn` stays T194; T195 must still be player-directed.
- Canon priority: explicit owner-approved rule and on-screen accepted events, then GitHub event ledger and `state/current.json`. Unknown properties remain unknown. No hidden XP/soul awards in earlier unlooted kills, replayed bosses or historical repeats.
- Existing HP/STA/BLOOD/TH caps and combat skill action/defensive-reaction/weapon constraints remain frozen. Souls, character EXP, skill EXP, BLOOD, and Tử Huyết are FIVE SEPARATE units. No exchange, transfers, uncapped regeneration, automatic player-level XP from skill XP or bounty payout from kills.

## 1. Soul yield on valid looting — S1.2

For one **eligible defeated living enemy or soul-bearing undead/construct** whose loot eligibility is real, from the corpse/essence remnant at **first irreversible qualifying loot/harvest**:

`S = ceil((2*L + 2) * R * D)` souls, where:
- `L` integer `>=1`: threat-equivalent enemy level *for reward computation*. Prefer explicitly established enemy level; if undisclosed, require declared evidence-backed encounter threat-equivalent with methodology and confidence. Enemy HP alone is NOT proof of level. Explicitly distinguish reward-calibration L from creature's undisclosed true level.
- `R` rank multiplier: normal1; enhanced-normal1.5; elite2.5; mini-boss4; boss6; world-boss12+ (world-boss above12 needs separately owner/GM-declared reason BEFORE loot).
- `D` strength mismatch relative to **player level at time enemy was defeated**: enemy >=player-2 levels and below the documented significantly stronger threshold:1; enemy 3 or4 levels below player:0.75; enemy ≥5 levels below player:0.5. **Significantly stronger enemy provisional factor1.25–1.5 is NOT numerically selected until a recorded threshold is approved; use D=1 pending such approval**, never invent a favorable factor post-kill. Do not lower D solely because the enemy was already wounded at encounter start, if the actual threat remained relevant; handle exploit deliberately during audit.
- Reward must be based on registered enemy type/rank/level BEFORE computing loot; no GM freehand soul additions. Show formula and arithmetic for every first-time yield in game log.
- If an applicable historical enemy has an earlier specifically accepted boss soul reward or replay deduplication, preserve that historical transaction. No duplicate farm of a unique killed enemy by reviving/replaying old scenes.
- Loot trigger is an on-screen action that obtains usable proof/material/essence from valid remains. **Kill without loot ≠ souls granted**. A verified eligible corpse's souls are granted automatically on successful qualifying loot; no second action to "collect souls" required. Separate one-time `soul_claimed` ledger record per corpse unique ID. Failed/no loot yields0, partial extraction may be evaluated if actual proof of valid harvest exists; never silently pay on an interrupted attempt.
- Soul balance is a nonnegative integer, cannot drop unless a chosen canon transaction explicitly spends it. Soul loot is a collectible game currency, not proof of an NPC's disembodied "soul" lore.
- An entity without soul-bearing remains can have0 if credible canon establishes that exclusion; **default** each legitimate monster corpse yields scaled souls, including bloodless undead if world lore specifies residual essence. No invisible universal zero for ordinary mobs.

### T194 one-time amendment correction (event separate from action T194)

- Both A and B were legally defeated (T191/T193) and had their fangs harvested at T194 (first qualifying corpse loot). T194 receipts originally logged exactly souls5 and no credit for souls under prior rules.
- Fix a **transparent reward-calibration estimate** for these two ordinary black-claw hyenas, `L_reward=5`, `R=1`, player level6 at kills, `D=1` (only one level below). This is a bounded encounter-reward calibration from their previously observed ordinary combat role, not a discovery/claim that the animals' actual true level is canonically five or that their stats are newly known. This calibration should be revisited by Superpowers audit, but changes are not retroactive absent separately authorized correction.
- Yield per corpse `ceil((2*5+2)*1*1)=12`. A +12, B +12, both at first T194 qualifying loot. **Idempotent amendment adjustment total +24 souls**: T194 snapshot historical5 remains TRUE as-recorded; new correction event `events/rules-amendment-T194-v1.2.md` points to both corpses and compensates once, producing amended current souls `5+24=29`. Replay MUST NOT pay A/B again. Player EXP remains205/400, proof2/3 pairs, HP90 STA53 BLOOD21 TH0. C alive100/100 no loot yet and no projected yield awarded. This is a SYSTEM CORRECTION, not new in-world turn, no time passes, no extra loot action.
- If separately confirmed evidence later shows a different reward-calibration L or an error, produce a new dated correction event explicitly rather than editing this accepted original arithmetic silently.

## 2. Tử Huyết (TH) on valid looting — TH1.2

- Every qualifying loot attempt checks **presence** of death/corruption/dark residue as witnessed/established in target lore. `TH_drop=0` for ordinary creatures lacking confirmed residue, including A and B; **NOT automatic +TH on every soul drop**. For source-bearing undead, dark-essence monsters, elites/bosses with evidenced TH: log initial TH source/purity, exact nonnegative integer yield, collection conditions, current/max TH20, and overflow explicitly. Amounts need rank-based tables and proof/ability gating in audit before generic automatic positive awards; unknown source means no GM-forced TH.
- No convert TH→BLOOD or replenish HP/STA on loot. Tử Huyết Hồi Sinh costs1TH+5STA and heals12HP only when resources are present.

## 3. Skill mastery by genuine active use — XP1.1

For each already learned skill, independently track `skill_exp_current`, `skill_level`, `mastery_receipts`, `required_for_next`; do not mix with character EXP or unlock unlearned skills. Previous ranks and training passes remain authoritative.

- One **legally resolved use** per activation (for Parry one legal defensive reaction attempt), with meaningful encounter/practice stakes and valid skill conditions:
  - Effective use, independent of whether enemy dies: +2 skill EXP baseline.
  - Valid failure with genuine practice/adversarial uncertainty: +1 skill EXP baseline.
  - Illegal/unavailable/spam/no plausible real training stimulus: 0 skill EXP and no bonus-roll attempt.
- Once per eligible **effective use**, skill gains +5 additional EXP with 25% nominal chance, not a 25% chance of a free skill LEVEL. Multi-hit Huyết Trảm Nhị Liên is ONE activation/roll even with two separate attack resolutions. Skill cost, CD, target defenses, reaction budget and action count unchanged.
- Do NOT invent random/dice receipt. Before awarding any +5, actually execute and store a verifiable seeded or transparent random draw with immutable `turn, use_id, skill_id, roll_method, roll_input, draw, threshold, awarded`. If no verified draw available, record deterministic baseline exp and mark bonus `PENDING_UNROLLED`, not a fabricated failed roll. **Superpowers audit must determine anti-reroll/nonce/cross-session reproducibility**. Outcomes not retroactive T187–T194: skill_exp counters START fresh at0 at effective turn T195, existing skill levels preserved.
- Proposed thresholds (cumulative *within each level*, carry excess to next): Common L1→2:40; L2→3:90; L3→4:160. Rare L1→2:60; L2→3:135; L3→4:240. Higher than L4 needs an additional accepted threshold. Threshold crossing marks `LEVEL_UP_ELIGIBLE`; **actual new level/effect can only be applied if the ability's next-level mechanics were specified and accepted in advance**; otherwise pause auto-upgrade rather than invent bonuses. Never re-run accepted Edran trial retroactively. T182 Parry already Common Lv2, T174 Huyết Trảm Nhị Liên already Rare Lv2. Unlearned Huyết Bộc/Tốc Mạch and hypothetical Huyết Nhận Hộ Thế remain unlearned, no XP.
- To protect game realism, no idle/parry feints against defenseless consenting props, self-harm, trivial-spam training or repeated non-threatening targets for unlimited mastery. Actual objective difficulty calibration and per-encounter XP caps are pending audit; do not retro-award unverified training EXP.

## 4. Audit boundary

- Superpowers methodological audit is requested AFTER writing this baseline. Explicitly record MAJOR/MINOR findings, risks, comparisons and precise proposed revisions. Findings may recommend alternative soul curves, fixed D thresholds, verified RNG, TH loot rates, skill XP anti-farm, level effect contracts and balancing against soul sinks. Mark these **PROPOSED / NOT IMPLEMENTED**; no stealth change to approved V1.2 parameters without owner approval.
