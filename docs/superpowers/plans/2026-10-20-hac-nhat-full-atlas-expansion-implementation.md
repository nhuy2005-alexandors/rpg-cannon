# Hắc Nhật Full Known-World Atlas Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend Hắc Nhật's persistent, evidence-backed editable atlas from three local maps to cover all story-relevant known areas without redrawing terrain on every turn or revealing unknown geography.

**Architecture:** Keep `maps/atlas-v1.json` as the only authority for drawable public terrain and `maps/active-scene.json` for current positions/facing. Add a coordinate-free evidence/coverage index, append only justified schematic or local layouts, and extend the existing stdlib SVG renderer just enough to handle placeholders and readable legends. Canva is a separately editable visual presentation; Notion is a durable link index, with no automatic sync.

**Tech Stack:** Existing GitHub repository `nhuy2005-alexandors/rpg-cannon`, Python 3.10+ stdlib (`json`, `unittest`, `xml.etree`, SVG), existing Canva and Notion connectors.

**Spec:** `docs/superpowers/specs/2026-10-20-hac-nhat-full-atlas-expansion-design.md`

## Global Constraints

- **Planning only until owner explicitly approves this plan and execution method.** Use isolated branch/worktree at execution time; do not write map implementation directly to production during planning.
- Gameplay authority: `state/current.json`, events and canon. **T204 remains the last completed turn; T205 must NOT be played or anticipated.** End T204: HP68/170 STA28/110 BLOOD28/50 TH0/20 Souls41 EXP215/400, 3/3 fang pairs collected but bounty UNPAID.
- Preserve `HN-MAP-ATLAS-V1`, `HN-MAP-SCENE-V1` and ALL 3 existing map IDs and 22 existing static object IDs/coordinates; additive metadata only unless a witnessed world delta requires an update.
- All static coordinates 0–100 mean **schematic positions, NOT meters**. Unknown places must remain unplaced; inferred connectivity is not a surveyed road or player-accessible shortcut.
- Huyết Lang Vương RESOLVED via accepted replay T128–139; Cấm Lao gate SEALED; hanging cave bone trap BYPASSED_NOT_DISARMED; Trạm Tam Trảo deep interior NOT confirmed; western bandit hideout UNKNOWN. No fake battles, treasure or new quest state.
- NO new engine/service/db/worker/Canva-per-turn regeneration; no Python packages beyond stdlib. Existing `maps/render.py` remains read-only with respect to game state and maps.
- Public GitHub data contains only player-discovered geography. Unrevealed GM secrets stay private. Notion is a derived index; old T153 entity graph is not live T204 map authority.
- Normal turn performance is protected: no Canva/Notion/network calls each turn; persist only on accepted existing checkpoint cadence or major event. Rendering is a separate optional operation, not a chat hook.
- Edit existing Canva design through a preview/review/commit workflow; do not assert every generated shape is separately movable without inspecting its elements.

## Review Focus

1. **Provenance conflicts:** “Trạm Gác Số Bốn” and “Trạm Tam Trảo” must never become one place based on a similar name. Task 1 `test_tram_gac_unknown_and_distinct`.
2. **Maps that falsely reveal secrets:** western bandit camp, sealed rooms and unseen cave depths must not become coordinates. Task 1 `test_unknowns_unplaced`; Task 3 `test_no_secret_rooms_plotted`.
3. **Temporal state inflation:** boss replay's old attempt must not be shown as another encounter; tripwire remains armed and gate remains sealed. Task 3 `test_historical_states_are_preserved`.
4. **Dense atlas display overflow:** a regional hub with too many pins must not silently clip the SVG sidebar or erase labels. Task 4 `test_dense_map_fails_readably`.
5. **Unintentional state/game progression during cartography:** sample renders and publishing to Notion/Canva must not modify T204, player stats or pending reward. Task 5 `test_frozen_game_state` + GitHub readback.

---

## File ownership map

| File or external object | Purpose |
| --- | --- |
| `maps/coverage.json` — CREATE | Evidence-backed region registry without coordinates; points to map IDs or null |
| `verification/test_atlas_coverage.py` — CREATE | Coverage, aliases, source validity, grade, historical freeze checks |
| `maps/atlas-v1.json` — MODIFY | Only supported new area maps and referenced terrain objects |
| `verification/test_map_renderer.py` — MODIFY | Rendering of expanded real maps, long labels, placeholders, overflow |
| `maps/render.py` — MODIFY MINIMALLY | Grade/placeholder treatment and fail-loud sidebar overflow |
| `maps/README.md` — MODIFY | List maps/coverage and commands; explain evidence levels, Canva limitations |
| `state/quick-start.md` — MODIFY DOC ONLY | Point the next GM session to full atlas, still next T205 |
| Canva existing design `DAHYiYqsXEU` + grouped new map pages | Reusable editable visual views, not geometry authority |
| Notion Hub `3fe864d2-95ce-8178-95ae-d0bcfde6ac34` | Index and verified source links, not gameplay mutations |
| `state/current.json`, `events/` | **READ ONLY** throughout atlas expansion |

### Task 1: Evidence coverage registry

**Files:**
- Create: `maps/coverage.json`
- Create: `verification/test_atlas_coverage.py`
- Read: `canon/world/places.md`, `story/arcs.json`, `events/0050-0095.md`, `events/0096-0153.md`, `events/0163.md`, `events/0195.md`–`0204.md`

**Interfaces:**
- Produces `maps/coverage.json` schema `HN-MAP-COVERAGE-V1`:
  `{"schema":"HN-MAP-COVERAGE-V1","areas":[{"id":str,"label":str,"grade":"LAYOUT_CONFIRMED|SCHEMATIC|PLACEHOLDER|UNVERIFIED","sources":[str],"map_id":str|null,"aliases":[str],"notes":[str]}]}`.
- No coordinates anywhere in this registry. An area can be known without a drawable map.

- [ ] **Step 1: Write failing tests** in `verification/test_atlas_coverage.py`: `test_unique_area_ids_and_existing_sources` loads `maps/coverage.json` and checks unique IDs, grade enum and each confirmed source path exists in the repo; `test_tram_gac_unknown_and_distinct` asserts `tram-gac-so-bon` has `map_id is None` pending event provenance and remains distinct from `tram-tam-trao`; `test_unknowns_unplaced` asserts `western-bandit-hideout` and `deep-cave-unknown` have no drawable `map_id`; `test_known_three_maps_retained` checks `hac-nha-east-approach`, `bai-sat-ri`, `nha-sat-dong-bac` in atlas and coverage.
- [ ] **Step 2: Run RED:** `python -m unittest discover -s verification -p test_atlas_coverage.py -v`. Expected FAIL because `maps/coverage.json` is absent.
- [ ] **Step 3: Create `maps/coverage.json`** using the spec's §3 inventory. Provide source repo paths for confirmed claims, no unsupported precise locations; `map_id:null` for unknown hideout, Trạm Gác Số Bốn pending source, deep cave and any unverified room. Keep place aliases distinct from new real locations.
- [ ] **Step 4: Run GREEN:** the same command, expected tests PASS. Record count of grade categories and source coverage as a receipt.
- [ ] **Step 5: Commit:** `git add maps/coverage.json verification/test_atlas_coverage.py && git commit -m "maps: register all known and unknown regions with evidence grades"`.

### Task 2: City, base and western-road schematic maps

**Files:**
- Modify: `maps/atlas-v1.json`
- Test: `verification/test_atlas_coverage.py`

**Interfaces:**
- Consumes Task 1 coverage `areas[].map_id`, `grade`, `sources`.
- Produces additive `maps[]` entries with stable IDs, `evidence_level`, `evidence_sources`, `revision:1`, `objects[]` (using existing renderer types), `known_limitations`; references no secret features.

- [ ] **Step 1: Write failing test** `test_city_and_western_road_maps` asserting map IDs `hac-nha-thanh-hub`, `dien-te-huyet`, `lo-ren-hac-nha`, `garrick-bang-nhiem-vu`, `duong-gac-tay`, `duong-tay-van-tai`, `doc-da-xam`, `suoi-can` are present with `SCHEMATIC` grade, canonical source fields, unique object IDs and no object labelled as a *confirmed* bandit hideout. Add `test_old_static_map_unchanged` pinning an immutable fixture of original 3 map IDs plus 22 object coordinates (capture reference from original commit `aea88e7ad45847ba0ba36738a85c2e70095fde0a`, not modified live atlas).
- [ ] **Step 2: Run RED:** `python -m unittest discover -s verification -p test_atlas_coverage.py -v`; expect missing new IDs.
- [ ] **Step 3: Append the minimum schematic data** in `maps/atlas-v1.json`: Hắc Nha hub with temple, Durgan forge, Garrick board (no fake street distances); limited temple base/training context; Durgan workshop and Garrick office as one-node interiors if layout unverified; west access, winding road, damaged wagon at Dốc Đá Xám, northern high ground, Suối Cạn relation from T163 without exact meters. Preserve prior three maps byte-equivalent in `objects`.
- [ ] **Step 4: Run GREEN:** focused tests PASS; visually inspect one sample SVG from each city and western-road cluster.
- [ ] **Step 5: Commit:** `git add maps/atlas-v1.json verification/test_atlas_coverage.py && git commit -m "maps: add city and western-road evidence-backed schematics"`.

### Task 3: Historical hunts, cave, Tam Trảo, Cấm Lao and military maps

**Files:**
- Modify: `maps/atlas-v1.json`
- Modify: `maps/coverage.json` only to link source-verified local maps (no new invented places)
- Test: `verification/test_atlas_coverage.py`

**Interfaces:**
- Consumes Tasks 1–2 coverage/map object contract; all new `map_id` values are stable.
- Produces supported `nghia-dia-tu-thiet`, `rung-xuong`, `huyet-cot-ngoai-dong`, `huyet-cot-hanh-lang`, `cam-lao`, `kho-quan-vu-dong` map entries. `tram-tam-trao` stays a declared PLACEHOLDER until source-backed local room geometry exists. Optional deeper map IDs remain null. The original 3 and Task 2 maps remain intact.

- [ ] **Step 1: Write failing tests** `test_historic_hunts_and_military_coverage` asserts the six map IDs plus non-empty source paths; `test_historical_states_are_preserved` asserts `cave-bone-tripwire.status == "BYPASSED_NOT_DISARMED"`, `cave-iron-chest.status == "OPENED_T145"`, `cam-lao-sealed-gate.status == "SEALED"`, and `huyet-cot-ngoai-dong.known_limitations` includes the **RESOLVED_REPLAY_T139** boss result; `test_no_secret_rooms_plotted` asserts no fabricated Tam Trảo station interior, bandit camp or hidden coffin room with unsupported geometry.
- [ ] **Step 2: Run RED** the focused coverage suite; expect absent IDs.
- [ ] **Step 3: Add layouts at evidence granularity only:** cemetery/rừng wolf habitat as schematic single-scene nodes; outer cave historic boss staging context; local cave corridor (known entry trap/corpse/chest/crevice, not full dungeon) with the exact trap and chest states; Cấm Lao gate with three known coffins as schematic features but no opened gate; military storehouse only as broadly witnessed storage area. If a location cannot be drawn without inventing a room, leave its coverage `map_id:null`.
- [ ] **Step 4: Run GREEN** with all maps; also rerun `python -m unittest discover -s verification -p test_map_renderer.py -v`; expected PASS on expanded atlas.
- [ ] **Step 5: Commit:** `git add maps/atlas-v1.json maps/coverage.json verification/test_atlas_coverage.py && git commit -m "maps: add witnessed cave, cemetery and military atlas areas"`.

### Task 4: Renderer correctness on the expanded atlas

**Files:**
- Modify: `maps/render.py` (minimal changes)
- Modify: `verification/test_map_renderer.py`
- Modify: `maps/README.md`

**Interfaces:**
- Consumes unchanged `render_map(atlas: dict, scene: dict|None, map_id: str) -> str` and CLI `--map`, `--base-only`, `--output`.
- Produces valid SVG for every mapped area, with `evidence_level` display and an explicit incomplete/unknown legend for maps without measured layouts. Empty supported placeholder maps must say `CHƯA CÓ BỐ CỤC ĐƯỢC XÁC MINH`, not draw invented walls.

- [ ] **Step 1: Write failing tests** `test_all_atlas_maps_render_as_xml` loops through every mapped ID; `test_dense_map_fails_readably` creates a 15-pin fixture and expects `ValueError("...split...")` rather than clipping the sidebar; `test_placeholder_has_no_fake_floorplan` tests an empty PLACEHOLDER map; `test_scene_mismatch_rejected_and_t204_frozen` preserves original `active-scene.json` and facing `ENE`; retain existing `test_escaping_prevents_svg_injection`, coordinate rejects, deterministic byte equality and solid/dashed arrow assertions.
- [ ] **Step 2: Run RED:** `python -m unittest discover -s verification -p test_map_renderer.py -v`; expect failure on unsupported 15-pin/placeholder behavior.
- [ ] **Step 3: Implement only necessary checks** in `render_map`: if more than 14 sidebar entries, raise actionable "split into local map" error; show grade/placeholder banner where appropriate; do not alter token placement or numeric state; ensure 0-object map works and all labels remain XML-safe.
- [ ] **Step 4: Run GREEN:** focused map tests and `python -m unittest discover -s verification -p 'test_*.py' -v`; record actual totals, failures and baseline drift rather than asserting a clean suite without output. Generate sample regional/west road, cave corridor, Cấm Lao and T204 room SVGs using existing CLI. All should parse via stdlib `xml.etree.ElementTree.parse`; review at display size.
- [ ] **Step 5: Update `maps/README.md`** with coverage grades, map ID examples, branch-safe verification commands and limitation that Canva does not auto-update. Commit: `git add maps/render.py verification/test_map_renderer.py maps/README.md && git commit -m "maps: safely render expanded atlas and unknown-region placeholders"`.

### Task 5: Persistent Canva presentation, Notion index and final non-retcon gate

**Files:**
- Modify DOC ONLY: `state/quick-start.md`, `maps/README.md`
- Inspect/read-only: `state/current.json`, `events/0204.md`
- External: existing Canva `DAHYiYqsXEU`; Notion Hub `3fe864d2-95ce-8178-95ae-d0bcfde6ac34`
- Test: `verification/test_atlas_coverage.py`, `verification/test_map_renderer.py`

**Interfaces:**
- Consumes all certified `maps[].id`, `maps/coverage.json` resolution and sample SVG renders; produces durable design links and a GitHub commit receipt. **No** automatic bidirectional Canva/Notion synchronizer.

- [ ] **Step 1: Write/run failing non-retcon guard** `test_frozen_game_state` with a fixture independent of mutable atlas: asserts saved `state/current.json` remains last_completed_turn204/next205, HP68 STA28 BLOOD28 TH0 Souls41 EXP215 and quest 3/3 unpaid; run it BEFORE presentation writes. If anything already drifted, stop and reconcile rather than forcing it back.
- [ ] **Step 2: Produce editable Canva atlas coverage** using existing design and one-time grouped map pages, not a new design on each turn. Inspect `get_design_pages`/`start_editing_transaction` to verify specific text/object editability, review each output against `maps/coverage.json`; remove unsupported drawn secrets/false scales. When a Canva editing transaction is needed, generate preview and **request owner approval before commit**. If API cannot add independent editable geometry to the same design, report limitation and offer grouped additional designs with stable links rather than pretending success.
- [ ] **Step 3: Verify Canva source links/pages** through `get_design` and `get_design_pages`; update Notion Hub with exact verified links, coverage grade summary, map IDs, latest authoritative GitHub source SHA. No update to historic T153 NPC graph unless user explicitly requests a separate graph task.
- [ ] **Step 4: Update quick-start/map docs** pointing to the completed atlas. Include a zero-per-turn-Canva-call operational instruction and example CLI. Do not touch live `state/current.json`, `maps/active-scene.json` or any T205 event. Commit docs only after consistency check.
- [ ] **Step 5: Final verification:** run both focused test suites + broad `test_*.py`, read back atlas/coverage and GitHub HEAD, and assert 3 legacy maps untouched, every registered area accounted for at correct grade, secret-only areas not plotted, T204 frozen, no new Souls/EXP/items. Read back Notion and Canva links. Record verified/failed/blocked separately; if approval for Canva commits is outstanding, label design projection PENDING and never claim complete.
- [ ] **Step 6: Commit/report:** `git add state/quick-start.md maps/README.md && git commit -m "docs: publish complete evidence-scoped Hac Nhat atlas index"`. Report commit SHAs, test receipts, coverage grade counts and any remaining PLACEHOLDER/UNVERIFIED locations.

## Self-review against design

- **Coverage:** Spec §2–3 -> Tasks 1–3; §4 static/dynamic policy -> Tasks 2–4; §4 Canva/Notion projection -> Task 5; §5 acceptance -> Task 5.
- **Type consistency:** `maps/coverage.json` stores only evidence/aliases/link IDs; `maps/atlas-v1.json` alone stores drawable coordinates. Renderer signature and scene schema remain unchanged.
- **Risk tests:** ambiguous Trạm Gác/Tam Trảo; unverified bandit hideout; historical sealed/bypassed/resolved states; SVG sidebar overflow and labels; frozen gameplay all have assigned regression tests.
- **YAGNI:** no navigation graph shortest-path, extra DB, custom GUI, image-generation loop or live Canva synchronization. A provisional location node is better than a fictional complete floorplan.
- **Approval gate:** This document and accompanying design are **planning artifacts**, not evidence that any new atlas region has already been created. Owner approval and execution approach selection required before implementation.

## Execution handoff

Recommend **Native execution** for this small Python/JSON/Canva documentation extension, because Tasks 2–4 share one atlas JSON file and sequential commits avoid conflicting edits. At execution, isolate branch/worktree if available and retain source SHA receipts. **Stop after this plan for owner review.**
