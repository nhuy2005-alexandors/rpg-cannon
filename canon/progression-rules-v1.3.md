# HẮC NHẬT — Progression Rules V1.3 (Lean Implementation)

**Status: OWNER AUTHORIZED 2026-10-20.** Minimal practical update. Supersedes future loot, mastery, RNG and branch progression clauses of V1.2 when conflict exists. Historical T194 and its +24 souls correction are APPEND-ONLY, untouched. **No T195 game action performed.**

This is a narrative GM game with a small pure Python calculation helper, `story/progression.py`, not an always-running engine. The GM invokes it when needed, records receipts and updates public state at existing checkpoint cadence. Never claim automatic tool execution or a live scheduler.

## Canon and confidentiality

- GitHub public `state/current.json` is authority for revealed numeric player state and gameplay history. No hidden combat skills or unread storyline secrets should be placed in public GitHub.
- Private GM note: Notion workspace-private draft `https://app.notion.com/p/3ff864d295ce81aa8a84cc628b21ef2a`. It is a separate *reference for undisclosed GM-specific fields*, not an overwrite authority for HP/quests or a deployed secure backend. Owner can access it. Restrict link sharing, and do not promise provider-level privacy beyond draft state.
- Before future new encounters with actual hidden mechanics, prepare and save a concrete locked GM template, commit its `SHA256(domain||canonical_json||nonce)` hash in public canon BEFORE resolving consequential gameplay. Freeze template/instance data. If private storage or verification fails, do not claim hidden template was committed or manufacture ungrounded abilities. No multi-repo database, jobs, agent dispatcher or background sync.

## Soul and Encounter rules

First valid loot of unique defeated corpse/essence grants `S=ceil((2*L_reward+2)*R*D)`. L_reward is a **predeclared** threat-equivalent reward level; do NOT claim it reveals biological level. R: normal1, enhanced1.5, elite2.5, mini_boss4, boss6, world_boss12. D from `L_reward - Vô Danh level at kill`: delta<=-5 ->0.5; -4..-3 ->0.75; -2..+2 ->1; +3..+4 ->1.25; delta>=+5 ->1.5. Use `story.progression.soul_yield` for arithmetic. Formula is future-facing: do not reprice A/B T194 correction (two 12 soul claims, current balance29).

Encounter Bonus: 0%, 10%, 15%, 25% of summed eligible BASE soul claims, floored once; bonus must have a **predeclared** encounter ID and documented challenge condition. Claim after encounter has fully closed, once per encounter, and do not retroactively award to currently ongoing A/B/C legacy scene. Normal self-induced difficulty cannot inflate bonus. `encounter_bonus` only computes a number: GM enforces eligibility and records one-time encounter claim id.

Tử Huyết only from confirmed TH-bearing source. Pending rank/source-specific positives cannot be invented. A/B:0TH. C: source UNVERIFIED -> positive yield NOT AUTHORIZED. TH cap20, actual overflow dropped and explicitly receipted; BLOOD and TH remain distinct. Loot once per corpse for Soul; physical fangs/materials use separate evidence receipts, not automatically granted by Soul claim. `claim_loot` pure helper accepts registered corpse id, source-approved TH; it returns a new state and per-corpse claim. Retried ID must not pay again. Actual GitHub writes still require read-modify-write concurrency/revision checks; the helper itself is not network-atomic.

## Minimal M1: legacy Linh Cẩu C

At end T194 C remains HP100/100, ~12m at western opening of NE shed, detected player, did not attack. Old A/B corpse Soul claims already fully paid. **M1 reward-only migration** before T195 uses same-species A/B ordinary level-calibration `L_reward=5`, `rank=normal`, D1 for player Lv6, so **potential 12 souls only upon C's future confirmed first corpse loot**; NEVER immediately. Legacy Encounter Bonus0, no retrospective bonus to A/B. C's actual true level/alpha abilities/ATK/DEF remain unverified; no hidden elite powers shall be invented or claimed preregistered. Private registry draft records calibration and reveals precommit hash `78aba9f325e62df78aa662a7750609a8d16993332453c6f6f7f4d95f67388e3c` (nonce private until reveal). This commit reflects **reward-only** agreement, NOT a fully specified secret combat template.

## Skill EXP & natural level-up

Existing 13 learned skills tracked from T195, no XP backfill. One meaningful effective activation +2 Skill EXP; one valid failure +1; invalid/idle/spam0. Effectively used skills receive ONE 25% roll for bonus +5 via Public Deterministic RNG. Per-activation receipt ID, never per sword strike (Nhị Liên = one activation) or per passive heal tick. Anti-farm: within equivalent `practice_context_id`, grant no more than 3 meaningful repeated uses without a genuine new test (enemy phase shift/attack pattern or certified training); restating the same action, harmless target or self-injury is not novel. Legitimate challenging encounters and distinct exam drills may count as fresh contexts, evidence required.

Common thresholds by from-level 1:40, 2:90, 3:160. Rare 1:60, 2:135, 3:240. Carry XP excess. Never infer rarity or level for currently `UNVERIFIED` skills. Upon threshold, level-up only from independently approved and versioned next-level contract; missing contract -> `BLOCKED_PENDING_CONTRACT` with EXP preserved, no invented buff.

**V1.3 level-up contracts approved with this amendment for future qualification only:**
- `GatKiemCanChien` Common Lv2->3 at90 Skill EXP: Parry reaction STA7→6 per legal attempt; no extra reactions, counters, stuns, invincibility, or increased automatic success.
- `HuyetTramNhiLien` Rare Lv2->3 at135 Skill EXP: first melee strike125%→130%, second100%→105%; cost12HP+25STA and CD3 unchanged, exactly two independently resolved sword hits; Huyết Nha +7 BLOOD still only for ordinary landed strikes and Hấp Huyết still capped5HP/combat turn.
- Other rank effects remain `BLOCKED_PENDING_CONTRACT`, no auto boost.

Evolution branches remain **not unlocked** for any skill at T194. To open a branch: (1) prerequisite skill mastery level, (2) evidenced authentic combat feat, (3) insight/discovery or trainer, each registered before grant. No existing skill automatically evolves. Only one active branch; `respec_branch` calculates cost3×skill_level×rankFactor (Common1/Rare2) and requires unlocked destination, outside combat, 60 verified safe minutes, enough souls. Respec retains EXP/cooldowns and cannot be used during T194 showdown. Branch modifiers for Phản Kiếm/Huyết Thủ and Nhị Liên evolution are **not yet activated** absent dedicated branch-effect contracts.

## Public Deterministic RNG V1.3

Public seed and version in `state/current.json` must exist BEFORE first RNG-enabled action. `rerollable_draw(seed,action_key)` hashes UTF-8 bytes `b'HN-RNG-V1.3\\0' + uint32_BE(len(seed_bytes)) + seed_bytes + uint32_BE(len(action_key_bytes)) + action_key_bytes` using SHA-256; reads first4 bytes uint32 big-endian. Bonus if `draw < 2**30` (25% of uniform 32-bit outputs). The engine uses action key `skill_id + '/' + use_id`. Action ID assigned by T### + sequential action ordinal *before* computing draw. No random action ID rerolls. Same ID on retry returns same receipt (idempotent). A public seed allows future outcomes to be predicted; **this is NOT commit-reveal and not anti-forecast protection**. No executed helper/no valid seed => baseline EXP only, bonus `PENDING_UNROLLED`, never fake a roll.

## Fast Mode receipt contract and checks

At a game turn, adjudicate real action, call the pure helper when relevant, show concise `HP/STA/BLOOD/TH/Souls/EXP; enemy HP; skill EXP Δ; source claim/roll if relevant`. Keep compact top-down battle SVG and practical prose. Continue GitHub checkpoint at10 turns since verified last base or earlier on major/irreversible durable event. No Notion sync for ordinary combat. Use `python -m unittest discover -s verification -p 'test_*.py'` when modifying code; do not claim tests passed without actually running them. Treat legacy `verification/check_state.py` as a historical T153 fixture, not a current-state validator.

**Non-retcon T194 facts:** current Vô Danh Lv6 EXP205/400 HP90/170 STA53/110 BLOOD21/50 TH0/20 souls29, 2/3 fang pairs; hyenas A/B killed and claimed; C alive100/100, alert~12m; next T195 not played. Nothing is automatically looted, no extra EXP/quest payout, and V1.3 does not retroactively re-roll past actions.
