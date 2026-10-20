# HẮC NHẬT — KỶ NGUYÊN TÀN THẦN

**Canonical saved checkpoint T194; next turn T195.** This PUBLIC repo contains only fictional RPG lore/context, released with the owner's explicit approval 2026-10-19.

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

Notion is only a read-optimized graph, **not a second source of truth**. GitHub remains canon for RPG numerical state and accepted world events. The projected source commit was `c47ba6254b042f016f8f53aafb2af346173674e4` (later docs/test commits do not imply changed gameplay). Current last verified RPG turn is T194; T195 has not started. T171 Edran trained sword arts (Huyết Trảm and Thiết Cốt Trảm actually cast, Huyết Trảm Nhị Liên/Huyết Nguyệt shadow only), HP115→105, STA expenditure65 fully recovered by safe rest, no skill upgraded. T172/T173 discussed two Huyết Trảm Nhị Liên Lv2 trials ONLY, no costs: original2 real casts 24HP+60STA, alternate 'Nhị Liên Tiết Huyết' one cast12HP+60STA after rigorous foundation checks. At T174 Vô Danh accepted the alternate: 4/5 dry chains, 3/3 controlled flow drills (no HP/BLOOD), 3/3 rotating bone target criteria on ONE real Nhị Liên cast (12HP+25STA). Edran confirmed earned **Huyết Trảm Nhị Liên Rare Lv2**: first125% and second100% physical, replacing Lv1 120%+90%, cost per cast12HP+25STA CD3 unchanged, no bonus attack or auto-hit. End Lv6 EXP185/400 HP93/170 STA110/110 BLOOD15/50 TH0 souls5; all ammo and potions untouched, Huyết Bộc Tốc Mạch still unlearned, western bandit leader bounty ACTIVE and unpaid, Vô Danh at Điện Tế Huyết. GM Fast Mode T174 checkpoint early because of permanent upgrade; ordinary turns use in-context state. Notion graph remains a T153 historical projection until updated. No background chat ingestion or timed auto-sync is installed.

## GM storyline mechanics V1

- [Story arc registry](story/arcs.json) — long-lived story threads and evidence-qualified lifecycle: Tam Nha, Kharzug & pup, sealed vessel, resolved Huyết Lang Vương.
- [Next action catalog](story/actions.json) — up to four grounded suggestions, not accepted quests; excludes old resolved boss and the obsolete “Cứu Maela” option.
- [Story policy functions](story/engine.py) and [regression tests](verification/test_story_engine.py) — lifecycle transitions, available actions and checkpoint triggers.
- [Game Master operational protocol](docs/gm-storyline-protocol.md) — how to integrate the above in each played turn. No unattended chat ingestion or background sync currently exists.

## T175–176 Parry training update

T175 practice did not qualify. At T176, Vô Danh passed Edran's three tests: basic 7/8, rapid 6/8, close range 5/6. Gạt Kiếm Cận Chiến Common Lv1 is learned with 8 STA per attempted valid melee defensive reaction. No automatic success, extra attack or BLOOD use. Huyết Nhận Hộ Thế remains unverified and unlearned. Final HP93/170 STA110/110 BLOOD15/50 TH0 souls5 EXP185/400. The western bandit bounty remains active and unpaid; Vô Danh remains in Điện Tế Huyết. See events/0175.md and events/0176.md and current state.

## T177–182 Parry LV2 checkpoint

T177 tested sword Parry under speed, feints and heavy strikes without an upgrade. T178 designed the three-part Phản Kiếm Vô Kẽ test. T179 stopped after passing stage I 7/8 but failing stage II 5/8; stage III was not attempted. T180 and T181 were remedial drills, not certification. At T182 Vô Danh retook and passed all three tests: Hư Thực Kiếm 7/8, Phản Thủ Liên Hoàn 6/8, Kiếm Thế Sinh Tồn 5/6. Edran confirmed Gạt Kiếm Cận Chiến Common Lv2: 7 STA per legal real-combat Parry attempt, more controlled recovery to guard if feasible; NO bonus reaction, attack, guarantee, or BLOOD infusion. Current resources HP93/170 STA110/110 BLOOD15/50 TH0 souls5 EXP185/400. All items intact. The western bandit-leader bounty remains active and unpaid, and the character remains at Điện Tế Huyết. See events/0177.md to events/0182.md and state/current.json. No Notion update required.

## T183–184 minor hunt and eastern scrapyard recon

T183 Vô Danh requested a small hunting bounty to replenish resources before undertaking Garrick's more dangerous western-bandit-leader hunt. The Hắc Nha Thành market board offered Ổ Chuột Huyết (5 tails, reward12 souls+20EXP), Linh Cẩu Móng Đen (3 pairs distinctive fangs, reward20 souls+30EXP), and Hài Cốt Lang Thang (3 cores, reward16 souls+25EXP). No offer accepted in T183. At T184 Vô Danh explicitly accepted ONLY Linh Cẩu Móng Đen, registered as ACTIVE, and reached Bãi Sắt Rỉ beyond Cổng Đông after ~35min ordinary travel and ~10min concealed observation. Two black-claw hyenas were directly sighted (~16m by fallen cage and ~24m by refuse pit). A growl from behind the northeastern ruined iron shed is UNVERIFIED, not a confirmed third hyena; count/alpha unknown. Vô Danh is on the WESTERN edge behind an overturned ore wagon and low berm, not confirmed detected; a ~9m exposed central gap, noisy northern scrap piles and northeastern blind spot constrain approaches. No attack, fight, kill, shot, blood absorption, trophy or reward occurred. Side-quest evidence 0/3 pairs and both this and Garrick's west-road quest remain ACTIVE and UNPAID. Stats Lv6 EXP185/400 HP93/170 STA110/110 BLOOD15/50 TH0 souls5; all equipment, potions and ammo intact, Parry Common Lv2 remains 7STA per valid defensive reaction. Quest acceptance triggered early saved checkpoint; next T185 awaits user action. See events/0183.md, events/0184.md, state/current.json and state/quick-start.md.

## T185–194 Bãi Sắt Rỉ combat and fang proof checkpoint

Ten-turn periodic checkpoint. T185 only analyzes how to lure Hyena A from western wagon concealment, T186 tosses a found pebble southwest of A (A moves ~2m, B alert). T187 loads and fires ONE Liên Nỏ steel bolt, hits A shoulder (18 actual damage as fixed in T188), and leaves four owned steel bolts. T188 ordinary Huyết Nha strike does26 HP (A72→46), heals2HP and +7 BLOOD. T189 Parry Common Lv2 defensive reaction stops A bite for7STA, no free counterattack. T190 ordinary sword strike does28HP A46→18, +2HP and +7BLOOD. T191 Huyết Ảnh Bộ reposition and legal normal sword attack kills A, +7BLOOD, +1HP, +10EXP. T192 Huyết Nguyệt Trảm 15BLOOD+10STA does39 HP, B90→51, no blood/heal proc because ranged special attack. T193 Huyết Trảm Nhị Liên Lv2 costs12HP+25STA and kills B with two separately resolved melee blows (37+actual14 HP), heals4HP via Hấp Huyết, +10EXP; no weapon ordinary hit BLOOD regeneration. T194 spends ~8 minutes carefully harvesting exactly **two intact pairs** of black-claw hyena fangs from corpses A/B (2/3 quest proof physically held, still awaiting issuer validation). A third Black-Claw Hyena C emerges from the west opening of the NE shed at ~12m, **100/100 HP and detects Vô Danh**, growls but does not attack yet. No additional XP, wounds, ammo, consumables or STA regeneration during harvest. Player next T195 stands by B corpse, Huyết Nha ready. Total current Lv6 EXP205/400 HP90/170 STA53/110 BLOOD21/50 TH0 souls5, steel bolts4, 1 Nanh Cốt Tiễn, 2 Huyết Dược. The 'Linh Cẩu Móng Đen' quest remains ACTIVE, pays 20souls+30EXP ONLY after third fang pair and verified market hand-in; Garrick's west road quest separately ACTIVE/unpaid. Existing skill cooldowns have elapsed during ~8 minutes after T193 battle, but usual skill costs and action limits still apply. See events/0185.md through events/0194.md and state/current.json. No Notion sync required. Future encounter maps: simple canvas-like top-down SVG only, no generated art or redundant caption.
