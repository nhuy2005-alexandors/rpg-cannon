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
