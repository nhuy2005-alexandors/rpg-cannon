# Superpowers Review — WIE-V1 Emergent World and Fortune

Date: 2026-10-22. Root cause: narrative GM lacks audited event sampling; existing V1.3 public RNG is only used for skill EXP. A proposed per-turn chance would incentivize player message spam and arbitrary GM selection.

- EW-01 MAJOR: per-message roll exploitable. Fix qualified physical opportunity + segment dedup + idempotency, not normal turn RNG.
- EW-02 MAJOR: arbitrary random gift/hostile/accident with no physical conditions. Fix fixed catalog + evidence tags + no replacement draw on invalid candidate.
- EW-03 MAJOR: automatic fortune credits and catastrophic breakage. Fix PROPOSED_NOT_ADJUDICATED and separate custody/repair/payment/owner decision.
- EW-04 MAJOR: inaccurate hidden RNG claim. Existing seed is public; replayable SHA256 stream is forecastable. Feature documents this and refuses hidden-roll claims.
- EW-05 MAJOR: fabricated combat hit odds and auto-hit from clean LOS. Fix explicit separately approved chance required, otherwise no numeric roll.
- EW-06 MODERATE: retry and renaming opportunity create re-roll. Fix full input fingerprint and one per physical segment per turn and kind.
- EW-07 MODERATE: NPC blunders occur only for cinematic convenience. GM must use training, awareness, fatigue, wounds, physical pressure; no forced stupidity quotas.
- EW-08 MODERATE: equipment failure on intact gear. Fix wear+load prerequisite; no per-item 0–100 durability subsystem.
- EW-09 MODERATE: double payout and quest inflation from event sampler. No resource writes; established Soul unique-corpse and separate money transactions still govern.

TDD evidence: RED missing module then GREEN 10/10 pass in local isolated Python 3.13. Full source checked-out repository tests still a separate gate; never conflate them. No gameplay T346 generated; world incident trigger requires an actual new turn and qualifying opportunity.
