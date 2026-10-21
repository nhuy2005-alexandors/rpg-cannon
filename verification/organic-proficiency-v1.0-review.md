# HẮC NHẬT — Organic Proficiency V1.0: Targeted Verification Receipt

**Verdict:** `PROFICIENCY_V1_0_TARGETED_ACCEPT` — implementation tested and safe to apply prospectively after T244 in the **supported, manual GM-initiated evidence flow**. This is NOT a full RPG simulation certification, full-repository regression, or autonomous runtime system.

## Independent source identity / executed environment

- Working environment: local isolated temporary project directory, Python 3.13.5, `unittest` standard library; no network/mutating actual game while running.
- Production baseline `story/progression.py` was copied from GitHub current main and verified byte-exact against existing Git blob **`4daee1763859b40a3b8ae641f53b3737c711b9a9`** using `git hash-object`. No changes to its code.
- Preexisting regression tests `verification/test_progression.py` were copied byte-exact; Git blob **`336bb2a6d7cad900848562dac37ab807280753d1`** confirmed locally against remote SHA; no modifications to test contents.
- New executed module: `story/proficiency.py` Git blob **`e8a96427f5ef47fc78b0230a8474ee497a22aae2`**, read back from GitHub matching local `git hash-object`.
- New executed tests: `verification/test_organic_proficiency.py` Git blob **`070654a3e832788d0e1be84ccba8fadf957de78b`**, read back from GitHub matching local `git hash-object`.

Command actually executed in isolated runtime:

```sh
PYTHONPATH=. python -m unittest -v verification.test_progression verification.test_organic_proficiency
```

Observed output at final patch:

```text
Ran 31 tests in 0.013s

OK
```

**31/31 PASS:** 9 existing progression tests, 22 new proficiency tests. The new suite additionally enumerates **195** combinations (39 starting mastery values × 5 attempted-usage lengths) inside one test and six invalid-cue subcases inside another. No failed test after final fix. Python syntax compiled and no external dependency required.

## Verified categories

| Category | Evidence |
|---|---|
| Existing V1.3 Soul/TH/loot math, RNG, skill use and branch respec | Original 9 tests PASS with hash-identical unchanged `story/progression.py` and `test_progression.py` |
| +2 effective / +1 meaningful failure / zero invalid | Assertions on base EXP and zero-credit receipts |
| Absent or unobservable ally, missing adjudication, trivial/repeated act | Invalid cue/precondition gates produce zero EXP and zero RNG bonus |
| No retroactive T244 exam EXP | Skill learned on turn244; action turn244 yields zero |
| Duplicate use/evidence IDs | Idempotence for identical repeat, hard reject contradictory evidence or new ID for same evidence |
| Equivalent-context anti-farm | Up to 3 eligible credited uses; later repeats zero; new evidenced context counts separately |
| Immutable input | No mutation to caller skill/event dictionaries |
| No fabricated RNG | No seed -> `PENDING_UNROLLED`; fixed supplied seed deterministic |
| No unintended stat changes | Skill gate returns skill entry only, never HP/STA/BLOOD/Souls/character EXP |
| Locked absent level-up contract | 40 EXP preserves Lv1 and reports `BLOCKED_PENDING_CONTRACT`; arbitrary next_contract for `NhanQuanHiepChien` rejected |
| No upgrade on invalid action even with available unrelated approved contract | Targeted added test with prior EXP40; Lv1 preserved |
| Real legacy T244 field shape | Vietnamese-name fallback works when entry lacks `skill_id`; forged mismatched ID rejected |
| Cross-domain design sanity | Synthetic `Woodcutting` skill without ally is eligible given distinct actual meaningful context; **no woodcutting skill added to RPG canon** |

## Findings, fixes, limits

- **FIXED F-01 (MAJOR):** A helper trusting an arbitrary caller-provided `next_contract` could prematurely grant Nhãn Quan Hiệp Chiến Lv2 although no such effect contract exists. Now reject non-null next_contract for this skill under V1.0; explicitly tested.
- **FIXED F-02 (MAJOR):** `skill_use` can check a threshold even after an ineligible zero-credit action; forwarding an otherwise-approved contract could allow a level advance without a qualified event. Helper now forwards contracts only if `eligible=True`; regression test added.
- **FIXED F-03 (MINOR):** Existing T244 skill entry lacks `skill_id`. Helper supports the specific canonical name and rejects mismatched IDs; regression covered.

**Residual limitations (known, not acceptance blockers for a human-GM game):**
1. The helper cannot independently verify whether in-world observations, ally visibility, source note, practice-context novelty or adjudicated results were *true*. Evidence is supplied by the GM and should be reviewable in turn receipts. A malicious or careless GM could lie by renaming contexts; this requires semantic review, not a new database/agent.
2. Deterministic bonus seed must be supplied from canonical `state/current.json` and the action key must actually be immutable; helper does not independently query GitHub or validate the seed against an authenticated source. If unable to verify, pass `seed=None`; award baseline only. No fake 2d10/draw receipts.
3. The focused local test has NOT executed the entire current repository regression suite, live GitHub concurrency cases, GUI/Canva/Notion integration or real in-world combat engine. The GM remains responsible for actor time, line of sight and NPC agency.
4. Other previously learned skills lacking a `skill_id` can keep using the existing V1.3 `skill_use`; adding Organic Proficiency to another domain requires a declared stable ID and vetted contract. Avoid arbitrary cross-skill migration.
5. No automatic skill XP or NPC changes occur until the player actually takes T245+ action. No live hook/scheduled code deployment implied.

## Release and continuity

- Source module and tests pushed to GitHub main with confirmed byte-level blob SHA readback. Organic spec: `canon/organic-proficiency-v1.0.md`; this report: `verification/organic-proficiency-v1.0-review.md`.
- The latest verified gameplay checkpoint remains **T244** (`state/current.json`). HP170/170, STA70/110, BLOOD28/50, TH0/20, Souls68, EXP300/400, Maela voluntarily cooperates from Điện Tế Huyết, western bandit leader bounty ACTIVE/unpaid, new **Nhãn Quan Hiệp Chiến Common Lv1 Skill EXP0/40** unchanged by engineering test.
- Next **T245 is not played**. Scope: spec/code/tests/docs only; no game event, loot or new passive level granted.
