# GM Hybrid Lean — Review remediation

The implementation fails closed on missing external evidence: positive Souls/EXP/inventory grants require an exact receipt in the trusted caller's independently verified `verified_grants`; combat, skill and tactical guards require caller-authenticated `verified_evidence_refs`. A caller cannot treat the submitted `source_ref` as authentication.

Accepted receipts have separate partial-tampering seals. This is **not** a signature; both record and seal can be rewritten by a malicious caller. The cold archive adapter requires exact raw bytes and a pinned Git blob SHA supplied independently from the canonical commit. This helper is read-only, never an autonomous writer.

Security-review RED reproducers cover phantom rewards, altered receipt metadata, bogus archive provenance, forged skill/LOS/hit evidence and unknown delta fields. No T346 event is played.

Python mechanical tests alone do NOT close behavioral GM evaluation, ChatGPT end-to-end FAST benchmark, or external independent review. Do not merge without those gates.

Re-review follow-up: same-turn claim/target duplicates now rejected for the same reward kind/resource; `accept_turn` requires independently preverified outcome refs; replay requires a digest pinned outside the mutable state. A hostile caller controlling both record and its only externally held digest remains outside pure-helper guarantees.
