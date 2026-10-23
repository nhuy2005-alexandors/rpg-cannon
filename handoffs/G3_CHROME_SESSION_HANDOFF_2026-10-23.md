# HẮC NHẬT — G3 ChatGPT Web / Chrome session handoff

**Handoff checkpoint:** 2026-10-23 (Asia/Ho_Chi_Minh) · **Scope:** GM Hybrid Lean V1.0 G3/G4/G5 acceptance work, not gameplay.  
**Source:** owner-directed current ChatGPT conversation, attached runner and 3 successive Chrome pilot JSON exports, plus GitHub PR #2 evidence. This is a **curated technical checkpoint**, **not a verbatim/complete transcript** or a CSC validated cross-chat restore.  
**Privacy:** technical facts only. No authentication cookies, credentials, private ChatGPT conversation URLs, or verbatim responses are published in this public repo.

## 1. Authoritative project / immutable pins

- Repository: `nhuy2005-alexandors/rpg-cannon` (PUBLIC).
- PR: [#2](https://github.com/nhuy2005-alexandors/rpg-cannon/pull/2), **DRAFT / OPEN / NOT MERGED** at checkpoint.
- Candidate branch: `feat/gm-hybrid-lean-v1-verified`.
- Candidate HEAD: `c70c5827d3fc67f753b9e5568fada6d774b47d0b`.
- Base/default branch `main` HEAD: `c74f77fe83fd490b85d8739be39056e0419331bb`.
- This handoff is on a **separate handoff branch** and MUST NOT move either pinned candidate or main as a side effect.
- Last real gameplay turn: **T345 completed**; **T346 NOT PLAYED**. Do not play T346, update canonical state, advance world clock, issue rewards, or write back any synthetic result.
- Protected files and their Git blob SHAs:
  - `state/current.json`: `a03e0bb288fa7bab4bb5147e00c78012edd36acc`
  - `maps/active-scene.json`: `b6fd996a9778b52f8b3bf2d601edcae9ea0fc8c7`
  - `state/archive/T345-state-cold.json`: `59cd3d2b1cf3580f581adced36efebfccc0c3353`
  - `maps/archive/T345-scene-cold.json`: `47d7e05dbddbdb6e344da42d2a475756f83941a9`
- Last reported source CI: [run 39845508619](https://github.com/nhuy2005-alexandors/rpg-cannon/actions/runs/39845508619), **169/169 Python unit tests PASS** on pinned candidate. Reconfirm if claiming fresh test evidence.

## 2. Gates / what IS and IS NOT accepted

- G0–G2: earlier acceptance evidence recorded in PR history.
- **G3 behavioral GM adjudication: OPEN / INCOMPLETE**. 36 fixed synthetic cases: 12 COMBAT, 12 TACTICS, 12 LEDGER. Must be **36 isolated model inference calls**, one new chat per case, exact response, unique chat URL, displayed model, prompt version/hash, and independent blind rubric results. Never turn a collected response into a PASS merely because fields are present.
- Earlier mechanical oracle over helper functions was **36/36 PASS**; earlier illustrative narrative smoke was **36/36 PASS from ONE model completion** with deterministic nonblind grading and 5/5 negative mutation checks. **Neither satisfies actual G3 acceptance.**
- **G4: OPEN.** 20 paired same-model/config baseline-vs-candidate real ChatGPT end-to-end measurements incl. p50/p95, TTFT, tool calls. Python helper timings are NOT ChatGPT latency and MUST NOT be counted as G4.
- **G5: G5_ACCEPT_STATIC**, from independent TinyFish static source review, 0 Critical/Important reported, not a submitted GitHub APPROVE review and not a runtime test. Reviewer: [independent run](https://agent.tinyfish.ai/runs/0b628903-e913-4f4c-845a-5de5dbe97ee0).
- Critical trust limitation: Python helpers require *trusted upstream* for `verified_grants`, `verified_evidence_refs`, external replay commitment and `expected_cold_sha`; local seals/self-declared inputs are not proof. Helpers are **not automatically wired into a ChatGPT Web GM runtime**.
- **DO NOT MERGE** PR or call full G3/G4 accepted without real receipts and owner gate process.

## 3. Actual Chrome Pilot collection (owner-operated ChatGPT Web)

Three successive file exports were supplied; **same growing pilot**, NOT independent duplicate runs:
- `G3_Pilot_COMBAT_01_03_ungraded.json`: COMBAT-01 captured (other two blank).
- `G3_Pilot_COMBAT_01_03_ungraded (1).json`: COMBAT-01/02 captured (03 blank).
- `G3_Pilot_COMBAT_01_03_ungraded (2).json`: COMBAT-01/02/03-V1 captured; exported **2026-10-23T07:59:17.715Z**. Immutable original file SHA-256 `20e330e9f876dd449598f837468b7a1b7a99d8f8b0f8b26df53d37b185cc979c`.

Observed response semantics (not independent graded):
- **COMBAT-01 / overkill**: verified hit, raw 60, DEF 12, enemy HP 9/90 → after-DEF 48, **actual HP loss 9**, overkill 39, enemy 0/90. No automatic loot/EXP/Souls. Pilot content judged internally correct.
- **COMBAT-02 / defense**: hit raw 34, DEF 11, verified reduction 3, enemy HP 70 → **20 damage**, HP 50. No auto rewards. Pilot content judged internally correct.
- **COMBAT-03-V1 / heal cap**: actual enemy HP lost 41, player HP 169/170, already healed 4 this turn. V1 prompt **omitted the lifesteal formula/turn cap**, so observed model reply said **UNKNOWN / BLOCKED** rather than invent an unverified rule. **Fixture defect; NOT a model failure.** Keep reply as `superseded_evidence`, not a pass for V2.
- Model field recorded as `Gpt 6 sol high` vs `gpt 6 sol high`. Early validator flagged **false positive for capitalization only**. V2 normalizes case/whitespace. It is **user-entered metadata**, not externally verified model provenance.
- The three actual chats have separate URLs in the owner's private local JSON; **never publish those URLs to this public repo.**

**Accepted continuation count: 2/36.** COMBAT-03-V1 is archive-only; **34 fresh chats remaining** (COMBAT-03-V2 + COMBAT-04..12 [9] + TACTICS-01..12 [12] + LEDGER-01..12 [12] = 34).

## 4. COMBAT-03 amendment V2 — explicit fixture, not RPG canon

The owner approved proceeding with a versioned fixture correction while preserving all original evidence. The next fresh chat MUST use **COMBAT-03-V2** with explicit synthetic rule:

```text
heal_new = min(
  5 - healed_this_turn,
  max(1, floor(actual_HP_lost / 10)),
  HP_max - HP_current
)
```

Inputs: `actual_HP_lost=41`, `healed_this_turn=4`, `HP_current=169`, `HP_max=170`. Therefore **synthetic oracle expected heal_new=1**, resulting player HP 170/170; no additional reward or unrelated effect. **This is not canon authorization** and does not retroactively change the V1 prompt. Test V2 in **a different new ChatGPT chat with a new URL**, never reuse the V1 URL.

Prompt manifest: 36 exact prompts, 35 retained V1; only COMBAT-03 uses V2. The prompt itself says SYNTHETIC-ONLY, no memory/history/files/GitHub/canon, no tools, no invented RNG/effects, UNKNOWN/BLOCKED when missing evidence.

## 5. Runner artifacts and receipts (private/local, not pushed here)

These filenames were created during this ChatGPT conversation and exist as chat artifacts, **not as files in this GitHub branch**. A new chat should ask owner to attach the relevant ZIP or JSON if it cannot retrieve old conversation files.

- **PRIMARY CONTINUATION:** `G3_HacNhat_Chrome_Continue_36_V2_20261023.zip` — SHA-256 `b527b3f40c68c1045705a4756bb694d9fe6f100c28039b4b93218e303723b834`. Contains `G3_Chrome_36_Continue_V2.html`, `README_VI_CONTINUE.md`, `g3_36_prompts_synthetic_only.json`, `g3_36_prompts_synthetic_only.txt`, `validate_collection_v2.py`, immutable pilot JSON, preload/archive JSON, test files and SHA manifest. **The HTML contains preloaded private responses and chat URLs; do not commit it to this public repository.**
- Original pilot raw JSON SHA-256: `20e330e9f876dd449598f837468b7a1b7a99d8f8b0f8b26df53d37b185cc979c`.
- Historical standalone runner: `G3_HacNhat_Chrome_Manual_36_Cases.zip` (older than V2; do not regress fixture).
- Earlier pilot: `G3_HacNhat_Pilot_3_Cases_Chrome.zip`.
- Earlier reviewed pilot: `G3_Pilot_Reviewed_Continuation_20261023.zip`.
- Earlier prepared `hac-nhat-g3-36-batch-smoke-20261023.zip` — one-completion smoke, **not independent G3**.

Runner V2 functional behaviors:
- Opens on COMBAT-03-V2, with COMBAT-01/02 **preloaded**; normal completion displayed as **2/36**.
- Preserves raw COMBAT-03-V1 as superseded archive; rejects treating V1 response as V2.
- Buttons: copy fixed prompt, open new ChatGPT chat, save response / URL / exact model label, next unfinished, export/import JSON.
- Validates duplicate chat URLs, missing fields, same-model normalizations, prompt version/hash and pinned commits. A syntactically complete collection only yields `COLLECTION_COMPLETE_UNGRADED`; **never** `G3_ACCEPT`.
- Earlier-session report: **16/16 offline tests PASS** (11 validator + 5 Chromium DOM/UI); Chromium HTML was loaded as content because `file://` navigation was restricted in that test environment. This is **not** authenticated ChatGPT browser execution.

## 6. Browser automation blocker and permission boundary

Owner explored eliminating 34 manual chats with an agent/plugin/MCP:
- TinyFish **Agent** answering `2 + 2 = 4` proved only TinyFish itself can respond, not that it successfully interacted with ChatGPT Web.
- Authenticated TinyFish **browser** could open new ChatGPT conversations/send prompts, but ChatGPT replies repeatedly displayed **`This response couldn't load`**. COMBAT-01 could not be counted from TinyFish.
- Connected Browser/Work host policy explicitly **blocked `chatgpt.com`** at the observation/control boundary. Owner's "cấp quyền" in chat did not override host policy. Browser plugin permission inspected: global **Allow low-risk actions**, plugin **Use my default**. Turning on general `Full access` is not an established fix and is not recommended to bypass a host security policy.
- Do not circumvent the browser host restriction via alternative endpoints, extensions, debugging shortcuts or hidden credentials. Use only properly supported, independently authorized access.
- Available legitimate paths: **(A)** continue manual Chrome owner-operated runner (meets ChatGPT Web scope), **(B)** use a supported browser tool/workflow *if* host officially allows it and a one-case control passes, **(C)** API/harness for truly automated isolated inference (may cost money; **not an equivalent proof of ChatGPT Web behavior/latency**). TinyFish was **not** established usable for G3.
- The latest user question about "plugin hay MCP nào giải quyết" is still **unresolved**: investigate only approved browser integration capabilities, without overpromising a workaround.

## 7. Next chat execution checklist / restart instructions

1. Read **this handoff** and [PR #2](https://github.com/nhuy2005-alexandors/rpg-cannon/pull/2), especially comments `6357623477` (one-completion smoke) and `6360800131` (COMBAT-03-V2 amendment).
2. Read/verify **candidate pinned SHA**, main SHA, PR Draft, and T345 protected blob hashes. **Do not change game source/canon.** This checkpoint's branch is documentation only.
3. If owner asks to resume G3, use **V2 ZIP** (owner re-attaches if inaccessible), not original V1 fixture. Preserve immutable COMBAT-01/02 receipts and V1 archived response.
4. First run just **COMBAT-03-V2** in a **new synthetic chat** on ChatGPT Web by a permitted/owner-operated workflow; capture exact response, new unique URL, model label, prompt hash/version, timestamp. Only then consider automating/collecting COMBAT-04..LEDGER-12.
5. To count a response, ensure isolated inference, genuine ChatGPT reply, unique URL, consistent model/config, no invented values and prompt fixture integrity. User-entered URL/model/response can be incomplete evidence; verify where possible.
6. Once **36/36** separately collected: run **independent blind grading** against the locked oracle with provenance; record per-case decision and exceptions. If any fixture gaps, preserve old versions and make explicit amendments rather than silent changes.
7. G4 still needs 20 baseline/candidate **paired ChatGPT observations** and comparable p50/p95/TTFT/tool counts. G5 static result remains bounded. Keep PR Draft until gates pass or owner explicitly changes acceptance criteria.
8. If blocked, state exactly which browser/security/UI limitation applies; report collection count **2/36** until *new actual evidence* is provided. Do not fabricate progress or claim a future/background execution.
9. Preferred answer style: **Vietnamese**, engineering receipts, concise and precise; don't ask the owner to rerun COMBAT-01/02.

## 8. Relevant GitHub receipts

- [PR #2 — candidate / gate discussion](https://github.com/nhuy2005-alexandors/rpg-cannon/pull/2).
- [CI run 39845508619](https://github.com/nhuy2005-alexandors/rpg-cannon/actions/runs/39845508619).
- [G5 independent static review](https://agent.tinyfish.ai/runs/0b628903-e913-4f4c-845a-5de5dbe97ee0).
- [G3 one-completion smoke PR comment](https://github.com/nhuy2005-alexandors/rpg-cannon/pull/2#issuecomment-6357623477).
- [COMBAT-03 V2 amendment PR comment](https://github.com/nhuy2005-alexandors/rpg-cannon/pull/2#issuecomment-6360800131).

## 9. Integrity / coverage caveats

This handoff was reconstructed from the **visible active session and attached files** plus verified GitHub readback; it is a curated project-critical digest and **cannot certify complete conversational coverage** or restore private chat receipts by itself. Repo is **PUBLIC**; no actual chat transcript, exact private chat URLs, secrets, authentication material, or original 3 JSON exports were uploaded. The separately connected `chatgpt-session-continuity` repository is PRIVATE and has its own **consent-gated export** runbook; this checkpoint does **not** pretend to have executed that workflow.
