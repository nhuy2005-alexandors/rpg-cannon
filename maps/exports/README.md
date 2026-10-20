# Hắc Nhật — Persisted Map Images (T204)

These **two SVG files are GitHub-persisted static snapshots** drawn from the public `maps/atlas-v1.json` map objects as of the end of **T204**:

- [Hắc Nhật World Map — T204](hac-nhat-world-t204.svg) — world-level one known region only.
- [Vùng Hắc Nha Regional Map — T204](vung-hac-nha-t204.svg) — relative west-to-east roads, city and eastern scrapyard; unplaced known locations listed but not plotted.

**These are NOT raster exports of Canva pages.** They are standalone, editable-as-vector SVG snapshot images derived from the canonical atlas; the canonical editable Canva master is [World & Regional Atlas (2 pages)](https://www.canva.com/d/Bpix2upN2ykgShg), design ID `DAHYjCS3NKI`. Other editable Canva maps: [15-page extension](https://www.canva.com/d/tpCkYiVOf3jAXHj) and [original 3-page atlas](https://www.canva.com/d/afa4HjByuyD2Dt6).

**Version semantics:** graphics are reference views frozen at T204. For later revisions, edit `maps/atlas-v1.json` based on newly verified story evidence, increment map revision, render fresh SVG with `maps/render.py`, and store it with a new provenance-labeled filename; never overwrite a historical T204 image and assert it depicts T205. If a Canva edit is needed, inspect and approve edits separately. SVG backgrounds and object positions are schematic, not physical distances.

**Source authority:** `state/current.json` / `events/` (game), `maps/atlas-v1.json` (map objects), `maps/coverage.json` (evidence grade), `maps/active-scene.json` (token overlay). These two SVG snapshots are **not** the active tactical map and contain no secret GM information.

**Excluded:** AI-generated decorative fantasy terrain/art from earlier chat, including uncertain rivers, mountain chains, and coastline, is not treated as verified geographical canon and has not been committed here as a verified map. There is no automatic Canva↔GitHub renderer hook and no full 20-page Canva PNG export in this directory.

Continue rules: [GM Map Behavior & Session Handoff V1](../../docs/gm-map-behavior-handoff-v1.md). Branch: `feat/full-atlas-v1-20261020` (not merged).
