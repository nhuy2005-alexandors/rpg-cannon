# Hắc Nhật — Atlas Snapshot T204 (Library Index)

**Status:** 5 map IDs saved as 5 PNG + 3 SVG files in the user's persistent ChatGPT Library, not Canva slide exports. Date: 2026-10-20. Game state is T204, **T205 unplayed**.

## Durable Library storage

Folder: `/HacNhat/Atlas/Snapshots/T204/`

| Map ID | Files | Source |
| --- | --- | --- |
| `hac-nhat-world` | `hac_nhat_world.png`, `hac_nhat_world.svg` | GitHub SVG renderer |
| `vung-hac-nha` | `vung_hac_nha.png`, `vung_hac_nha.svg` | GitHub SVG renderer |
| `hac-nha-east-approach` | `hac_nha_area_base.png` | GitHub SVG renderer |
| `bai-sat-ri` | `bai_sat_ri_base.png` | GitHub SVG renderer |
| `nha-sat-dong-bac` | `t204_shed_map.png`, `t204_shed_map.svg` | GitHub SVG renderer, T204 overlay |

Folder also contains `manifest-v2.json` (size + SHA256 + map IDs and provenance), and `HacNhat-Atlas-T204-5-Maps.zip` (downloadable five PNG and three SVG assets). The original `manifest.json` covered only World + Regional.

**Important distinction:** These are **stable renderer snapshots** from atlas coordinates, not visual PNG exports of editable Canva pages. They preserve map topology and T204 state but do not reproduce Canva design styling.

## Editable Canva masters (20 total pages)

- World/Regional 2-page, design `DAHYjCS3NKI`: https://www.canva.com/d/Bpix2upN2ykgShg
- Supplement 15-page, design `DAHYiz8iryA`: https://www.canva.com/d/tpCkYiVOf3jAXHj
- Original 3-page, design `DAHYiYqsXEU`: https://www.canva.com/d/afa4HjByuyD2Dt6

**20 Canva page PNG exports NOT COMPLETE**: current connector supports listing 20 page thumbnails and their transient signed URLs but has no reliable accessible direct export-to-container action. Never classify thumbnail URL metadata or the five renderer images as archived Canva page exports.

## Update rule

Gameplay progresses from authoritative `state/current.json` and `events/`; the atlas source remains `maps/atlas-v1.json` and `maps/active-scene.json`. New confirmed geography updates source before manually regenerated exports. Canva does not auto-sync from GitHub. No action to advance T205 was taken during archival.
