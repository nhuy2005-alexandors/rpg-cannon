# HẮC NHẬT — GM Map Behavior & Session Handoff V1

**Saved:** 2026-10-21 (Vietnam time)  
**Scope:** Persistent operating rules and provenance for subsequent ChatGPT sessions. **Not a game turn; no T205 action.**  
**Working atlas branch:** `feat/full-atlas-v1-20261020` (**UNMERGED**; do not claim present on `main`).  
**Gameplay canon authority:** `state/current.json`, `events/`, `canon/`, `story/arcs.json`. The map is a derived PLAYER-KNOWN representation, never an oracle for hidden information.

## A. New-session start — mandatory minimal restore

1. Read this file and `state/quick-start.md`. Read `state/current.json` (from canonical `main`, or the last **verified** gameplay checkpoint), plus `maps/atlas-v1.json`, `maps/coverage.json`, `maps/active-scene.json` from `feat/full-atlas-v1-20261020` while it is not merged. Do **not** assume the feature atlas already exists on `main`.
2. If any source or version conflicts, prefer verified gameplay state and original events; distinguish evidence from visualization. Don't hallucinate missing turns or unsaved checkpoints.
3. Restore historical last finished RPG turn **T204**, next **T205 ONLY after a player action**. Scene: Vô Danh inside NE iron shed at NE recess after moving the slanted board, facing ENE toward shallow niche and low vent. HP 68/170; STA 28/110; BLOOD 28/50; Tử Huyết 0/20; Souls 41; EXP 215/400. Three intact Black-Claw Hyena fang pairs 3/3 carried, quest ACTIVE, bounty **UNPAID**. Cave spike trap BYPASSED_NOT_DISARMED; Cấm Lao gate SEALED; Huyết Lang Vương historical boss RESOLVED after accepted T128–139 replay, no repeat loot.
4. Read the GM policy in `docs/gm-storyline-protocol.md` once on session bootstrap, not before each turn. Never play T205 or teleport Vô Danh just to validate/print/update atlas.

## B. Three-tier atlas and persistence contract

| Level | Source map ID / files | Behavior |
| --- | --- | --- |
| WORLD / Level 0 | `hac-nhat-world` in `maps/atlas-v1.json` | Only discovered **Vùng Hắc Nha** is public. Everything else is UNKNOWN; expanding the world is additive when the story establishes another region. No invented nations, coastlines, mountains, rivers, cities or destinations. |
| REGION / Level 1 | `vung-hac-nha` | Grounded directional relations: city hub, western gate and Dốc Đá Xám to the west, eastern Bãi Sắt Rỉ, NE shed inside the scrapyard. Other known-by-name places remain `unplaced_known_names`; do NOT assign geographic pins from narrative familiarity. |
| AREA / TACTICAL / Level 2 | Other existing `maps[].id` | Reuse each area's stable object IDs, local walls/cover and known investigation clues. Draw live entities in a **separate scene overlay**; never redraw or re-author the fixed terrain for a normal move. |

`maps/coverage.json` indexes named locations with source-based evidence grades and nullable `map_id`, **not** geographic coordinates. `maps/atlas-v1.json` owns public drawable objects and optional unplaced labels. `maps/active-scene.json` owns active token positions/directions. `state/current.json` owns numerical gameplay. The normalized [0,100] schematic coordinates DO NOT define game meters, sight distance or a precise travel-time scale.

**Immutable until the world actually changes:** maps' static objects and IDs. A real new discovered landmark or changed door/board updates only the affected object, increments the map revision where appropriate and gains a corresponding event source. Draw no GM-private dungeon entrances, enemies, loot, traps, or future plot branches before they are discovered. Do not equate Trạm Tam Trảo with Trạm Gác Số Bốn. Sào huyệt cướp Đường Tây location UNKNOWN.

## C. Expected GM behavior on each gameplay turn

**Normal action (fast path):** adjudicate the player's chosen action using accepted gameplay canon and current in-chat working state; update scene *in memory*; update only token(s), `x/y`, `facing` and dashed movement path. A live token receives a **solid facing arrow** and **dashed movement arrow**. Dead entities have **no facing**; don't spawn or mark hidden enemies.

**Complex combat/investigation:** show the existing tactical/area map only where it helps decisions and spatial relationships. Orient consistently with north-up as a SCHEMATIC convention; use confirmed encounter-range facts rather than assume SVG schematic distance = meters. Player choices remain free-form; no autoplay.

**Confirmed geometry change / discovery:** append or update just the certified object with provenance. If a known name lacks bearing, list it under **CHƯA ĐỊNH VỊ**, not as a map pin. When story enters a new geographical region, add its WORLD node and REGIONAL map and link existing scene(s) to it, preserving all previously created locations.

**Persistence:** no GitHub/Notion/Canva calls merely because another normal turn started. Reuse in-chat state. Write full gameplay state/events/scene at existing verified checkpoint cadence: after up to 10 unsaved completed turns, major event, explicit save, handoff/context risk; read back and confirm changed paths. Never claim durable save without real commit/readback. World and regional map change only on meaningful geographical evidence, not per turn. If an assistant cannot execute a renderer in the session, state this clearly and use a schematic description; never claim automatic image generation.

**Visualization:** `python maps/render.py --base-only --map hac-nhat-world --output maps/exports/hac-nhat-world.svg` (and `--map vung-hac-nha`) generates static map SVG from JSON. For tactical scene use `python maps/render.py --output <file.svg>`, which reads the current `active-scene.json`. Canva is a **separate editable visual presentation**, not a renderer hook nor an automatic GitHub sync. Avoid ImageGen/Canva regeneration per turn. Update Canva *only when materially needed* after proper visual preview and explicit approval before editing-transaction commit.

## D. Exact official Canva designs and exclusion

- **Official World + Regional overview, 2 editable pages:** [Hắc Nhật — World & Regional Atlas (Canon-safe)](https://www.canva.com/d/Bpix2upN2ykgShg), Canva ID `DAHYjCS3NKI`. Import was based on hand-controlled HTML; readback verified 2 pages, 33 separate text elements, 4 shapes, no invented place names. These 2 pages serve as the **long-lived visual master for Level 0 and Level 1**, alongside GitHub geometry.
- **Existing Area atlas, 15 editable pages:** [Atlas Hắc Nhật V1.1](https://www.canva.com/d/tpCkYiVOf3jAXHj), Canva ID `DAHYiz8iryA`.
- **Earlier Area atlas, 3 editable pages:** [Atlas Hắc Nhật](https://www.canva.com/d/afa4HjByuyD2Dt6), Canva ID `DAHYiYqsXEU`.
- **REJECTED, do not use as canon:** Canva `DAHYi1nKV3E` (“Bản đồ Hắc Nhật”, 2 pages), screenshot supplied 2026-10-20. This auto-generated design fabricated e.g. “Thung Lũng Tro Tàn”, “Rừng Lai Khói”, “Hồ Mực”, “Bến Than Đen”. The generated mountains, rivers, coastlines and decorative geography in such designs or ImageGen artwork are **artistic, not canon**.
- **Images vs design:** a rasterized page/image is a snapshot, not an editable Canva layer. Keep stable Canva design IDs and `atlas-v1.json` separate from exported PNG/SVG screenshots. Every illustration/export needs a source/design ID and a `grounded_through_turn` or clear “decorative/noncanon” label.

## E. Current implementation/gates (read before claiming completion)

At latest branch inspection: **19 drawable map IDs, 25 evidence coverage entries**, 17 pre-existing maps retained and two higher-level maps appended; six place/topic entries remain unlocated. `maps/render.py` has a sidebar for `unplaced_known_names`; it refuses overcrowded panels rather than silently hiding names. New hierarchy tests at `verification/test_atlas_hierarchy.py` exist. The implementation resides on `feat/full-atlas-v1-20261020` only and is **NOT MERGED** into main. Some focused map tests were exercised in an isolated local mirror and GitHub data structure was read back; that is **not** a full in-repository CI run or independent code-review acceptance. Don't upgrade gate to ACCEPT or merge until actually verified.

The Notion hub is a link/projection: https://app.notion.com/p/3fe864d295ce817895aed0bcfde6ac34 . Its old T153 knowledge-graph title doesn't imply current T204 NPC presence.

## F. Minimal owner-facing response after importing this handoff

Say where the player is (NE shed, facing ENE, end T204), indicate World/Region/Area map reuse is ready from the named branch, provide the appropriate verified Canva link if asked, and **wait for the player's T205 choice**. Never spontaneously run T205, create new NPC/loot, or ask to redesign already frozen map decisions.

**No automatic background map updates, no permanently running Canva/GitHub synchronizer, no independent renderer hook in ChatGPT.** This is an explicit GM workflow that is performed on user actions and checkpoint events.
