# Rules Activation — HN-V1.3 LEAN, after T194 and before T195

**NOT a gameplay turn. No combat, player movement, resting, kill, inventory extraction, quest return or awards took place.** User requested to apply the accepted V1.3 design pragmatically, no overengineering.

- Approved V1.3 minimal policy: `canon/progression-rules-v1.3.md`, pure calculation code `story/progression.py`, tests `verification/test_progression.py`. System remains GM-driven, not an installed autonomous engine.
- Public RNG seed created using Python `secrets.token_hex(32)` and stored `state/current.json` prior to any V1.3 random awards. No RNG draw on this rules-only event. Future public outcomes are predictable by design.
- M1 reward-only migration for previously seen but unengaged living C: conservative same-species rank Normal, reward calibration level5, future potential Soul12 at first valid corpse loot if player Lv6; **no Soul granted now**, no retroactive Encounter Bonus; TH positive yield unverified. C's HP100/100, ~12m NE shed, player detected, did not attack. No retroactively frozen unknown C combat stats.
- Private GM Registry stored as workspace-private Notion draft and verified by readback. SHA256 precommit `78aba9f325e62df78aa662a7750609a8d16993332453c6f6f7f4d95f67388e3c`; public hash refers only to this **reward-calibration** contract; not proof of any hidden combat ability. Do not store Notion private nonce in GitHub public.
- Frozen original V1.2 correction for A/B remains: T194 original souls5, add-on +12 A and +12 B, currently souls29, claimed once each. No re-award, no new quest payout.
- Current Vô Danh Lv6 EXP205/400 HP90/170 STA53/110 BLOOD21/50 Tử Huyết0/20 Souls29, 2/3 fang pairs; C alive100/100; **last completed T194; next T195**.
- Skill mastery EXP counters remain0 for all 13 known skills. Two Lv3 next-rank contracts now configured for future eligibility; existing skill ranks and cooldowns untouched. No branch evolved, no respec, no fees paid.
- No full private encounter engine or background worker was created. The private page is a user-owned draft; actual permission policy beyond private mode has not been independently audited. For future hidden NPC templates, register a genuinely specified and verified contract before applying it; otherwise fail closed.
