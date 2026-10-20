# Hắc Nhật — Full Known-World Atlas Expansion Design V1.1

**Status:** Written consolidation of owner-approved direction for a complete reusable atlas. Submitted alongside an implementation plan for owner review; **not authorization to implement**. Date 2026-10-20. The accepted behavior comes from the conversation: one persistent editable area map, separate moving character/monster tokens and facing, no Canva redraw each turn, long-term GitHub/Notion indexing, and **no overengineering**.

## 1. Purpose and boundaries

Expand the existing three-map atlas to cover **every known story-relevant area at its actual evidence resolution**, without inventing unrevealed geography. “Entire atlas” means every named established region is discoverable from the atlas, **not** that every room, destination, enemy location or distance becomes known. Detailed floor plans appear only when witnessed or grounded.

- GitHub public `state/current.json`, `events/`, `canon/world/places.md` and `story/arcs.json` remain the gameplay/evidence authority. No retroactive edits to story.
- `maps/atlas-v1.json` is the public persistent map-object collection; preserve schema `HN-MAP-ATLAS-V1`, stable IDs and existing 22 objects from the current 3 maps.
- `maps/active-scene.json` remains the dynamic scene overlay. Never relocate Vô Danh without a narrated player action. At this design baseline: **T204 completed, T205 unplayed**; V inside NE iron shed, facing ENE, 68/170 HP, 28/110 STA, 28/50 BLOOD, 41 souls, 215/400 EXP, fang pairs 3/3 not submitted.
- `maps/render.py` is the reusable Python 3.10+ stdlib SVG renderer. No new map engine, services, agent graph, database, browser harness, job runner or background sync.
- Canva design `DAHYiYqsXEU` (https://www.canva.com/d/afa4HjByuyD2Dt6) currently has 3 pages. Canva is editable presentation; it does **not** automatically synchronize with GitHub. Notion Hub `3fe864d2-95ce-8178-95ae-d0bcfde6ac34` is a link/index/projection, not state authority.
- “Known region” ≠ guaranteed active encounter. Preserve resolved wolf boss, sealed Cấm Lao gate, bypassed-but-armed cave trap, and unpaid western-road bandit quest.

## 2. Evidence grades and public visibility

- **LAYOUT_CONFIRMED:** at least one observed spatial relationship exists (e.g. west entrance of NE shed, ring NW, table and movable board). Retain observed relational layout, label normalized 0–100 coordinates *schematic*.
- **SCHEMATIC:** name/connection or broad terrain known (e.g. western road beyond west gate, Dốc Đá Xám and Suối Cạn, Hắc Nha hub and temple). Place an icon/node or diagram only, **no fabricated exact coordinates or route length**.
- **PLACEHOLDER:** named/mentioned but layout, exact entrance, direction or access is uncertain. Render an explicit unknown/undiscovered panel; no fake room walls and no token movement into an invented area.
- **UNVERIFIED:** rumor, witness inference or an old uncorroborated alias; record text note in source-backed registry but do not draw as factual landmark. Secret GM-only data stays outside public maps entirely.
- Every map entry gains `evidence_level`, `evidence_sources` (canonical repo paths), and optional `known_limitations`; every drawable object keeps a stable ID, type, label and normalized coordinates. `maps/coverage.json` lists all relevant named places with evidence grade and an optional link to a drawable `map_id`, but never holds coordinates. Existing entries may be annotated, not moved without source.
- Recorded map paths/links are **known connectivity only** unless actual lengths, terrain and traversal were observed. If a node has no proven location, display it in an *unplaced* panel instead of assigning a coordinate.

## 3. Area coverage inventory

The following are coverage **targets to verify**, not automatic physical maps. Keep the first 3 map IDs and object identities unchanged. Area clusters may be represented by one regional overview and one or more local scenes where evidence exists; do not force one imaginary detailed floorplan per label.

| Cluster / initial ID | Evidence source(s) | Grade, key constraints |
| --- | --- | --- |
| Existing `hac-nha-east-approach` | `maps/atlas-v1.json`; T195–204 | LAYOUT_CONFIRMED only for schematic city→east scrapyard→NE shed links |
| Existing `bai-sat-ri` | `events/0195.md`–`0204.md` | LAYOUT_CONFIRMED at relative scale |
| Existing `nha-sat-dong-bac` | `events/0201.md`–`0204.md` | LAYOUT_CONFIRMED; board moved, vent destination UNKNOWN |
| `hac-nha-thanh-hub` | `canon/world/places.md`; `events/0163.md` | SCHEMATIC; temple, forge and Garrick are within hub, no precision |
| `dien-te-huyet` | `canon/world/places.md`; `events/0152.md`, `0160.md` | SCHEMATIC; Edran base, storage, safe rest, training court; no invented adjacent chambers |
| `lo-ren-hac-nha` | `canon/world/places.md`; `events/0096-0153.md` | SCHEMATIC; Durgan workshop, no unsupported room plan |
| `garrick-bang-nhiem-vu` | `canon/world/places.md`; `events/0163.md` | SCHEMATIC; quest office, bounty hand-in remains unperformed |
| `nghia-dia-tu-thiet` | `events/0050-0095.md`; `0096-0153.md` | SCHEMATIC; undead hunt recorded, unknown layout stays unknown |
| `rung-xuong` | `canon/world/places.md`; `events/0050-0095.md` | SCHEMATIC; wolf habitat, no complete trail network |
| `huyet-cot-ngoai-dong` | `events/0096-0153.md` T120–T140 | SCHEMATIC; historical boss battle, Huyết Lang Vương RESOLVED; T128–139 replay supersedes earlier attempt |
| `huyet-cot-hanh-lang` | `events/0096-0153.md` T142–T146 | LAYOUT_CONFIRMED only locally: cave corridor, hanging bone-spike trap BYPASSED_NOT_DISARMED, opened chest, bat location historically |
| `tram-tam-trao` | `canon/world/places.md`; `events/0096-0153.md` | PLACEHOLDER/control-station access below cave; do not portray fully visited interior or disarmed trap |
| `cam-lao` | `canon/world/places.md`; `events/0050-0095.md`; `story/arcs.json` | SCHEMATIC; three coffins and SEALED gate, no opened secret halls |
| `kho-quan-vu-dong` | `events/0050-0095.md` T77–89 | SCHEMATIC storeroom; no invented shelves/doors based only on old summary |
| `tram-gac-so-bon` | Historical conversation; require a supporting GitHub event before placing | PLACEHOLDER/UNVERIFIED until provenance matched; do not synonymize with Trạm Tam Trảo |
| `duong-gac-tay` | `canon/world/places.md`; `events/0096-0153.md` | SCHEMATIC city west access |
| `duong-tay-van-tai` | `canon/world/places.md`; `events/0163.md` | SCHEMATIC; road, not guaranteed safe |
| `doc-da-xam` | `events/0163.md` | SCHEMATIC; damaged wagon, north high ground, tracks disappear |
| `suoi-can` | `events/0163.md` | SCHEMATIC; dry channel and exposure risks; distance unknown |
| `western-bandit-hideout` | `events/0163.md`; `story/arcs.json` | **UNVERIFIED/UNPLACED**; do not map hideout as discovered |
| `deep-cave-unknown`, `coffin-interiors-unknown` | Historical mentions only | **PLACEHOLDER only**, no rooms, encounters, traps or loot added |
| `maela-or-kharzug-private-location` | NPC canon | **NO INDEPENDENT MAP** unless an established place is actually identified; NPC ≠ location |

Unverified label “Cấm Lao/Hầm Giam” may be displayed as an alias pending canonical reconciliation, not automatically as two separate mapped facilities. “Huyết Lang Vương boss zone” is an exterior/historical encounter context, not assumed deep inside the cave.

## 4. Architecture and rendering contract

1. Reuse the **same `atlas-v1.json` file** and `active-scene.json`. Append map entries only for certified scene maps; add verified location identities and unplaced names to a compact `maps/coverage.json` index (`schema: HN-MAP-COVERAGE-V1`; fields: `id`, `label`, `grade`, `sources`, `map_id` or null, optional `aliases`, `notes`). This index is evidence and map-resolution metadata ONLY, never a second source for coordinates.
2. Static object renderer honors existing `room`, `cover`, `clue`, `path`, `door`, etc.; may add one optional `evidence_level` rendering treatment and a **placeholder panel** for maps with no floor geometry. No metrical scale or navigation engine.
3. At most a readable number of numbered terrain pins per SVG panel (currently 1100×700 with sidebar labels, avoid >14 unless a single split into local scene/overview is necessary). Never clip the legend silently.
4. The live SVG has arrows for **character facing** (solid) and **movement** (dashed), separate from background topology. No corpse facing arrows. Area switch requires legitimate narrated player motion; never change current scene at planning or atlas expansion time.
5. Repeated inputs yield byte-identical SVG. Text is XML-escaped; malformed coordinates, duplicate map/object IDs, unknown directions, unsupported schema fail closed.
6. Canva presentation: use existing 3-page file for existing maps; add one-time editable *schematic* atlas pages for newly grounded clusters. Inspect actual editable elements and correct fake/unsafe labels before calling any result canonical. Canva can remain slightly stylized; GitHub map IDs, layout and source-grade prevail. Canva editing-transaction saves require user-visible preview and explicit approval. No promise of dynamic Canva↔JSON sync.
7. Notion Hub indexes links to GitHub data/SVG export and verified Canva page/design IDs, source SHA and statuses. Historical T153 graph is not silently rebuilt and Notion never becomes the map-state authority.

## 5. Verification and completion definition

- All locations in coverage inventory have a resolution: drawn at supported detail, SCHEMATIC node, or explicitly PLACEHOLDER/UNVERIFIED. No unsupported additions.
- Three existing map IDs, 22 object IDs and static coordinates remain unchanged except separately sourced object-state deltas.
- At least one test for each: ambiguous alias, unknown/unplaced region not plotted, world route without metric distance, SEALED gate, cave armed-but-bypassed trap, boss resolved/supersession, repeated data rendering, more labels than sidebar can hold, SVG/XML escaping, cross-map scene mismatch, frozen T204.
- Run focused `python -m unittest discover -s verification -p 'test_map*.py' -v` and broader repository tests; report actual receipts and pre-existing failures honestly.
- Sample SVG outputs for a regional overview, cave corridor, Cấm Lao and T204 active shed scene, without changing live T204 state or triggering T205.
- Canon commits and verified GitHub readback; Canva and Notion are separately inspected and linked, not claimed synchronized automatically.
- **No new gameplay, extra loot or rewards. No production/security/auth edits.** Work should be done in an isolated branch/worktree during implementation where possible. Only documentation of this specification and implementation plan is authorized at planning stage.
