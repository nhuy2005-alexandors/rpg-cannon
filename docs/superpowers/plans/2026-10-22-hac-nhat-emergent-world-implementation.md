# Emergent World V1 — Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL Superpowers test-driven-development, executing-plans and verification-before-completion.

**Goal:** An additive, reproducible incident sampler and optional chance roll, without altering T345 or automatic gameplay.
**Architecture:** Pure Python standard library in story/world_incidents.py; one test module; two policy addenda.
**Spec:** docs/superpowers/specs/2026-10-22-hac-nhat-emergent-world-design.md.

## Global constraints
Frozen T345 next T346; existing combat/Souls V1.3 untouched; no background host hook; no code-generated NPC secret or loot; public RNG predictable; no per-chat probability; future-only rules and fast response.

## Review focus
- Same opportunity ID with changed zone => error; same real segment with re-ID => error.
- Missing tag evidence or invalid kind/time => fail closed.
- Worn item failure cannot be rolled without recorded wear AND use pressure.
- Chance helper refuses unspecified hit probability; no automatic damage.
- Event category is not automatic award or discovered/claimed loot.

### Task 1 — TDD tests
- [x] Create verification/test_world_incidents.py with 10 checks: sum probabilities, idempotency, per-chat rejection, tags, no auto reward, duplicate physical opportunity, invalid tags, equipment gate, invalid turn/zone, explicit contest chance, determinism.
- [x] RED observed: ModuleNotFoundError story.world_incidents before source existed.
- [x] GREEN in isolated Python 3.13 environment: 10/10 pass.

### Task 2 — Source code
- [x] Add story/world_incidents.py: deterministic SHA256 domain-separated independent draws with modulo-bias rejection; immutable fingerprints; fixed catalog and tiers; no stat mutations.
- [x] Re-run all ten targeted tests in isolated sandbox.

### Task 3 — Integration
- [x] Add status/eligibility/runbook to canon/rules.md and docs/gm-storyline-protocol.md. Reuse approved GM Behavior V1.4 intent (enemy independent, legal LOS, time).
- [x] No modifications to T345 state or maps.

### Task 4 — Verification & rollout
- [ ] GitHub commit/branch readback and compare against last verified main SHA; then fast-forward main with expected SHA.
- [ ] Full repo test suite on accessible checkout; if checkout unavailable record BLOCKED, not PASS.
- [ ] Keep normal play fast: only call helper when a truly eligible time/segment/equipment-risk occurs. Do not treat technical docs change as T346.
