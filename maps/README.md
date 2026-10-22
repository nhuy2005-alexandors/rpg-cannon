# HẮC NHẬT — Editable Map Atlas V1

**Owner intent:** persistent editable maps; do not redraw an entire area every RPG turn. This is a small data-driven system, not a new orchestration service. **No gameplay turn beyond T204 is implied.**

## Reusable assets
- **Canva editable presentation, 3 pages (region, Bãi Sắt Rỉ, NE iron shed):** [Atlas Hắc Nhật](https://www.canva.com/d/afa4HjByuyD2Dt6) — design ID `DAHYiYqsXEU`. Created 2026-10-20. Contains individually editable text labels; other geometry should be checked in Canva before assuming every object is independently movable. Canva AI may insert invented decorations or inaccurate labels: NONE become canonical from a Canva image alone.
- [atlas-v1.json](atlas-v1.json): persistent **canonical public location objects and approximate relative coordinates** for the three areas.
- [active-scene.json](active-scene.json): mutable scene token layer (currently T204); `facing` and movement must be displayed independently. This is not the authoritative RPG numerical state — see [state/current.json](../state/current.json).
- [current-state](../state/current.json) + [T204 event](../events/0204.md): numerical/gameplay authority. Private GM facts are NOT stored in public atlas.

## Fast update workflow
1. At the start of a location, read the relevant `atlas-v1.json` map entry (static walls/terrain) and `active-scene.json` (dynamic tokens, facing, traversed path). Reuse the **same location IDs and coordinate frame**.
2. On a normal move/combat turn, **only update scene tokens and path** in-session for the chat map. Do not modify static terrain or create a new Canva design. The existing narrative checkpoint cadence (max10 turns or major event) still governs GitHub state persistence.
3. When a *confirmed* world change occurs (a board moved, a bridge collapses, a new place is discovered), update only that object's JSON entry, increment the map revision, and optionally adjust the **same existing Canva design** through Canva editing; do not overwrite historic events. Canva edits require preview and explicit save approval. Do not claim Canva synchronizes automatically with GitHub.
4. During a verified game checkpoint, persist and read back both game state and current scene, confirming matching turn numbers. Notion remains a searchable index with links, not a competing map/position authority.
5. Unconfirmed enemies, secret locations, loot and traps must NOT be placed in the public map. Inferred relative layout is a visualization aid, never a new canon distance or a precise metric scale.

## Layer convention
- Terrain/static map objects: `maps[].objects[]`, stable `id` and normalized coordinates 0–100.
- Dynamic overlay: `active-scene.json` `current.tokens[]` and `current.movement[]`.
- A live entity has a `facing` in {N,NE,ENE,E,SE,S,SW,W,NW} with north at top. Dead bodies are **not** active facing targets.
- Include a clear movement arrow on each turn and distinguish it from a facing arrow; show only known/observed positions.

## Canonical atlas limits
The region map is schematic: relative Hắc Nha Thành → eastern scrapyard → NE shed is confirmed, but exact scale and many distant area coordinates are not. The current T204 map is the shed interior. Vô Danh stands near the board moved in the northeast interior, facing ENE, from the NW ring. A/B/C dead and Soul-claimed; quest fang proof3/3 held but **quest reward unpaid**. No added treasure or hidden chamber.

This design deliberately does **not** run a background browser, generate new images per turn, install dependencies, or introduce a new RPG state engine.

## SVG renderer V1 — implemented

The reusable zero-dependency script [render.py](render.py) draws the public static map and the current active scene as an SVG. It reads JSON and writes ONLY the requested SVG output: it does not change gameplay, trigger T205, claim loot, edit Canva, synchronize Notion, or save `state/current.json` on its own.

Run from the repository root (PowerShell or any shell with Python 3.10+):

```powershell
python maps/render.py --output maps/exports/current.svg
python maps/render.py --map bai-sat-ri --base-only --output maps/exports/bai-sat-ri.svg
python maps/render.py --map hac-nha-east-approach --base-only --output maps/exports/region.svg
python -m unittest discover -s verification -p test_map_renderer.py -v
```

`--map` chooses the stable map ID; omit it only when rendering the current scene, which supplies its own `map_id`. With `--base-only`, `--map` is required. Without `--output`, the SVG prints to stdout.

**Layer convention actually implemented:** static object IDs and coordinates are read without changes from `atlas-v1.json`; independently movable tokens and facing vectors come from `active-scene.json`. The facing vector is a solid pale arrow and movement is a dashed arrow. The normalized coordinate system (0–100) denotes relative positions only, **not accurate meters**. Numbered object markers have a sidebar legend so previously established features need not be relabelled each turn. Rendering the exact same inputs yields byte-identical SVG output.

**Important limitation:** this renderer is an executable tool and is not automatically connected to ChatGPT responses or to Canva. In future turns, GM should update **only** `active-scene.json` as movements are adjudicated, or a specific map object when a real world change is confirmed; renderer should be run when an updated SVG is needed. Atlas and scene checkpoint updates still follow existing RPG save policy. Canva is a separately editable decorative design, not the rendering engine or numeric authority. No claim of end-to-end speedup was benchmarked; local Python-only render cost was approximately 0.1ms per map with 10 objects on the verification environment.

**Regression receipt (2026-10-20):** focused `python -m unittest discover -s verification -p test_map_renderer.py -v` reported **9 tests passing**, covering all three static maps plus active scene, deterministic SVG, unchanged static objects after token moves, correct arrow differentiation, XML validity, invalid coords/facing rejection, duplicate IDs and escaped labels.

## Full Atlas V1.1 selectively integrated into T345 main — 2026-10-22

Source feature branch commit `06b6eb62a18c2f3c5b2fe8a8a20263b4d53ec284`, previous main `0e559ed2fe25954a4b92ff1aad267e9fa599f33c`. All existing main map IDs including the old three static maps and newer T345 tactical scene were **retained by ID unchanged**; only 17 unseen feature-branch static maps were added. Now 21 maps, 27 coverage entries. Copy of old T204 dynamic scene deliberately excluded. No gameplay turn advanced; `state/current.json` remains T345, next T346. Historic feature T204 PNG/SVG exports remain labeled T204. World and region unknown geography are still UNKNOWN / unplaced. Canva layer separately editable, not synced. 

Updated original brittle frozen-game-fixture tests to T345 for this checked snapshot; do not assume tests executed in runner just because saved. Follow static base + overlay pattern; no invented metric distances.
