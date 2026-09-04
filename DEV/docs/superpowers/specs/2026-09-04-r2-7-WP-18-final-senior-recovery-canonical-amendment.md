# R2.7 WP-18 — Final Senior Recovery Canonical Amendment

Status: **CANONICAL AMENDMENT — MANDATORY FINAL SENIOR RE-AUDIT PENDING**

Date: 2026-09-04

Amends:

- `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md`.

Recovery provenance:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-final-senior-recovery.md`.

This amendment is narrow. All WP-18 architecture laws, planning IDs, topology, ownership boundaries, deferred/dormant/rejected items and acceptance cases remain unchanged unless this amendment says otherwise.

---

## Amendment A — mechanical synchronization is not categorically deferred

Canonical §13 remains the implementation-facing obligation list, but its final paragraph must not be read as a blanket prohibition on repository synchronization before implementation planning.

When accepted architecture has already determined an exact repository value and synchronization requires no material schema, algorithm, runtime-orchestration, migration, persistence, instruction or product-semantics choice, that synchronization may be performed as mechanical recovery work.

Such synchronization does not authorize substantive implementation or implementation planning.

---

## Amendment B — planning catalog provenance is realized now

Canonical §13 item 10 is no longer merely a future obligation.

The current `planning_entry_classes` vocabulary remains exactly:

```text
planning.source_anchored_constraint
planning.provisional_dramaturgic_direction
```

Its current machine-readable semantic/downstream provenance MUST trace through this exact accepted chain:

```text
DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md + DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md
```

This applies to:

- `family_policies.planning_entry_classes.semantic_owner`;
- `family_policies.planning_entry_classes.default_downstream_owner`;
- both admitted entries' `semantic_owner`;
- both admitted entries' `downstream_owner`;
- both admitted entries' `evidence_citation`.

The current catalog ledger was mechanically synchronized at `bbf0b6ad04a78f5df701197957e751fde19b1464` without changing planning IDs or semantics.

A focused regression test must prevent reintroduction of stale Story/continuity provenance.

---

## Amendment C — remaining §13 classification

The following canonical §13 duties remain `SUBSTANTIVE_IMPLEMENTATION_LATER`:

```text
1-9
11-13
```

Rationale: each requires one or more still-downstream implementation choices in schema realization, runtime orchestration, persistence/publication behavior, authorization integration, instruction mapping, acceptance-suite realization or post-implementation evaluation.

Canonical §13 item 12 remains downstream for the full behavioral acceptance suite. The narrow provenance regression added by this recovery is only the mechanically implicated guard for item 10 and does not constitute WP-18 runtime/schema implementation.

---

## Final amended disposition

```text
SR18_FINAL_01: CLOSED
F18_07_ARCHITECTURE: CLOSED
F18_07_MACHINE_PROVENANCE: CLOSED
MECHANICAL_SYNC_NOW_COMPLETED: YES
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
WP_19_AUTHORIZED: NO
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
NEXT_GATE: MANDATORY FINAL SENIOR RE-AUDIT
```
