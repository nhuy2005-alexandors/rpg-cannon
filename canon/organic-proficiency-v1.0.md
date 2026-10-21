# HẮC NHẬT — Organic Proficiency V1.0 (Approved Lean Addendum)

Status: **OWNER APPROVED for prospective gameplay after completed T244** (design consent in the active conversation). Tested helper `story/proficiency.py`; adversarial tests `verification/test_organic_proficiency.py`. This is a **prospective additive evidence gate** to existing `canon/progression-rules-v1.3.md`. No modification to the frozen V1.3 reward math, skill EXP amounts, skill level thresholds, RNG, combat action economy or accepted T194–T244 narration; no retroactive mastery credit. No game turn is consumed by drafting/testing this spec.

## Design intent

Real-life craft mastery (e.g. decades of woodcutting) comes from selecting better angles, recognizing material/terrain patterns, economizing effort and correcting errors, not necessarily stronger muscles. Apply domain-specific progressive competence across crafts and tactics. **Do not create an independent 'Battle IQ', STR, DEX or numerical global bonus stat.** A skilled actor obtains/uses *contextually perceptible* information more reliably and selects better-intentioned actions. Ordinary adjudication of sight, hearing, reach, physical time, cover, uncertainty, adversarial feints, movement, injury, fatigue and ally autonomy remains mandatory.

## Canon progression integration

1. Only pre-existing **learned, verified Common/Rare** entries may gain proficiency EXP. New skill unlocks require separate trainer/exam/feat with predeclared contract, as with `Nhãn Quan Hiệp Chiến` Common Lv1 at **T244**, SkillEXP **0/40** upon unlock. No prior or exam use backfill.
2. For each later **meaningful, GM-adjudicated** challenge attempt, record one immutable action ID, evidence ID, source turn/file, domain-specific challenge signature, practice-context identity and concrete observation/novelty rationale. Merely *requesting* improvement or explaining a plan does not qualify.
3. V1.3 remains authoritative: **+2 Skill EXP** per legitimately effective meaningful activation; **+1 Skill EXP** per legitimately attempted valid failure; **0** for invalid/idle/spam/duplicated/unseen or nonadjudicated events. The optional +5 only follows an actually executed, independently reproducible V1.3 public RNG draw using the already pinned canonical seed/action key; if no verified draw, baseline only with `PENDING_UNROLLED`. No user-facing fabricated roll.
4. At most **3 credited equivalent meaningful uses per `practice_context_id`**. A materially new encounter, enemy behavior or instructor-certified changed drill may form a genuinely new context, with **auditable independent evidence**. Changing a text label without a real material change is not a valid new context. There is no machine-verified proof of world novelty; the GM remains responsible.
5. `story/proficiency.py:proficiency_use` is **one pure, opt-in evidence gate** before the existing `story/progression.py:skill_use`. It stores idempotent per-use receipts in the existing skill's `use_receipts` (no new persistence service). Duplicate use IDs cannot be double-credited; the same evidence ID under a new use ID is rejected; a conflicting evidence ID under an existing use ID is rejected. Ineligible attempts get zero-credit receipts.
6. Level thresholds stay **Common 40/90/160** and **Rare 60/135/240** by from-level. A level increase still requires independently preapproved, versioned from→to skill effect contracts. If absent, EXP is preserved and `BLOCKED_PENDING_CONTRACT`. No new bonuses or evolution trees implied by milestone names.

## Nhãn Quan Hiệp Chiến — current scope

- **T244 certified Lv1 already exists; do not relock or award it.** Lv1 grants relevant recognition of ONE **observable** ally-coordination cue in a legal combat beat when an actual ally is cooperating, V is attentive and cue perception is plausible. Examples: ally's safe shooting lane becomes blocked, ally changes stance/angle, ally visibly readies aim or signals withdrawal. GM can surface the cue to the player before selection where naturally observable; never infer information from unseen/inaudible allies or enemies.
- Failure in a material fresh attempt may produce a normal +1 mastery receipt (after unlock), without causing fictional extra harm or rewarding inaction. Effective use may yield +2 (and RNG only if actually verified).
- **Lv2 is NOT approved and cannot be injected with arbitrary next_contract into V1.0 `proficiency_use`.** Reaching 40 EXP preserves the excess and blocks auto-level. Later user-reviewed version can define carefully bounded higher competence (e.g., anticipating allied movement using actual available patterns) without automatic accuracy/attack/DEF/skill costs or mind reading.
- Existing `Phối Hợp Kiếm–Nỏ Lv2` applies to V's **own weapon switch** penalty; `Ngắm Bắn Ổn Định Lv2` applies to V's **own short-movement-to-aim** penalty. Organic team awareness adds NEITHER percent-based aim boost nor additional shot. Maela remains an autonomous free hunter, may refuse an unsafe shot, misses still possible, loading and ammo required.

## Safety and evidence gates for future turns

`preconditions_met`, `action_adjudicated`, `meaningful_challenge`, `novelty_evidence`, `ally_cooperating` and `observable_ally_cue` (team skill only) must reflect *observable events*, not desired outcome. Test harness deliberately treats these as GM-supplied input—not a deployed world simulator or oracle. If in doubt, mark ineligible and award zero; never alter previously accepted receipts. Skill-level increases, physical buffs, bonus EXP and new passive effects require their own recorded approval.

**What does NOT happen on adopting V1.0:** no new game turn, no rest or heal, no grant of +2 EXP to T244 exam, no repeat quest payment, no V/ Maela relocation, no equipment changes, no auto-creation of woodcutting skills. Resume canonical game at **T245**, after T244 checkpoint, player Lv6 HP170/170 STA70/110 BLOOD28/50 TH0/20 Souls68 EXP300/400, Maela voluntary partner at temple range, western bandit bounty ACTIVE/unpaid. GM runs gameplay only on next player action.

## Test and release boundary

Targeted tests and exact SHA readback are recorded in `verification/organic-proficiency-v1.0-review.md`. The helper is pure; no always-running hook automatically invokes it. The currently approved GM must call it or apply the same auditable eligibility rules when new qualified in-game events occur. No full-project E2E claims from a targeted test run.
