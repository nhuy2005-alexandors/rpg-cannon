# HẮC NHẬT — KỶ NGUYÊN TÀN THẦN

**Canonical saved checkpoint T170; next turn T171.** This PUBLIC repo contains only fictional RPG lore/context, released with the owner's explicit approval 2026-10-19.

## Read first (<60 seconds)
1. [Fast start](state/quick-start.md)
2. [Exact current state](state/current.json)
3. [NPC canon](canon/npc/) and [world places](canon/world/places.md)
4. [Relevant historical event ledger](events/)

[GM rules](canon/rules.md) · [Storage/flush protocol](docs/storage-protocol.md) · [Source provenance](provenance/sources.md)

**Critical lore:** Edran = Tư Tế Xương; Maela = nữ thợ săn; Kharzug = chiến thú già Tam Nha; unnamed Huyết Lang pup. Historically alive T93; all four reconfirmed at temple T154, Kharzug still recovering. Kharzug is NOT the one-eyed wolf killed at T66. The Tam Trảo bone tripwire is not disarmed.

**Sync policy:** GitHub is the authority, Notion is a derived lookup. Flush by checkpoint/major event/session switch, no unattended background auto-capture. Immutable imported source documents in sources/drive/ are evidence, not competing current-state copies.

## Notion Knowledge Graph V1 (LIVE snapshot T153)

- [Hắc Nhật Context Hub](https://app.notion.com/p/3fe864d295ce817895aed0bcfde6ac34)
- [Entities database](https://app.notion.com/p/3e1a70d007444496874d9e9535071d6a) — nine canonical IDs
- [Relationships database](https://app.notion.com/p/4ea8c07ae96d4312b585acab207bc370) — seven directed evidence-backed edges
- [Registry and saved Notion views](graph/notion-registry.json); [initial verification receipts](verification/graph-receipts/initial-import.md)

Notion is only a read-optimized graph, **not a second source of truth**. GitHub remains canon for RPG numerical state and accepted world events. The projected source commit was `c47ba6254b042f016f8f53aafb2af346173674e4` (later docs/test commits do not imply changed gameplay). Current last verified RPG turn is T170; T171 has not started. Maela instructed Vô Danh through a 6-sequence legally loaded/unloaded Liên Nỏ sword-switch test: sequences1,3,4,5,6 PASS, sequence2 FAILED prematurely trying an unloaded trigger (no shot), achieved >=5/6 threshold and earned **Phối Hợp Kiếm–Nỏ Common Lv2**. Its up-to-10 percentage-point switch-specific accuracy-penalty reduction REPLACES Lv1 up-to-5pp, NOT a flat accuracy buff or an action/reload bypass. Separate Ngắm Bắn Ổn Định Common Lv2 still only reduces movement-specific penalty by up to15pp after <=3m move and full stop; cannot double count same penalty. T170 80 STA spent on training and 80 recovered across 4h safe rest; HP115/170 STA110/110 BLOOD15/50 TH0 souls5 EXP185/400 unchanged, owner ammunition and consumables intact. Garrick western bandit leader quest ACTIVE/unpaid, Vô Danh remains at Edran's temple, Tốc Mạch unlearned. Notion graph remains a T153 historical projection until updated. No background chat ingestion or timed auto-sync is installed.

## GM storyline mechanics V1

- [Story arc registry](story/arcs.json) — long-lived story threads and evidence-qualified lifecycle: Tam Nha, Kharzug & pup, sealed vessel, resolved Huyết Lang Vương.
- [Next action catalog](story/actions.json) — up to four grounded suggestions, not accepted quests; excludes old resolved boss and the obsolete “Cứu Maela” option.
- [Story policy functions](story/engine.py) and [regression tests](verification/test_story_engine.py) — lifecycle transitions, available actions and checkpoint triggers.
- [Game Master operational protocol](docs/gm-storyline-protocol.md) — how to integrate the above in each played turn. No unattended chat ingestion or background sync currently exists.
