# R2.7 — Whole-Project Final Architecture Audit — Owner Clarification

Status: **OWNER-APPROVED ARCHITECTURE PROGRAM CLARIFICATION**

Date: 2026-08-24

Purpose:

> Correct the scope of the final architecture stage before implementation planning.

---

# 1. Owner decision

R2.7 SHALL be a **whole-project final architecture and machine-realization audit**.

It SHALL NOT be bounded to Round-2 external-idea deltas, R2.1-R2.6 semantics, or only the machine surfaces newly introduced by Round 2.

The reason is structural:

```text
R2.7
    -> final architecture closure
    -> implementation planning
```

Therefore R2.7 is the last architecture opportunity to detect missing owners, stale machine contracts, schema/runtime contradictions, incomplete bootstrap/migration/release obligations, or cross-round composition failures before implementation is decomposed.

---

# 2. Required coverage horizon

R2.7 must cover and reconcile:

- all accepted Round-1 architecture (Steps 1-5 and owning model contracts);
- all later accepted amendments/owner decisions;
- all accepted Round-2 architecture (R2.1-R2.6);
- all current shipped GAME runtime contracts and persistent schema/template surfaces;
- all current DEV machine catalogs/schemas relevant to runtime realization;
- bootstrap/install/update/migration behavior;
- persistence/recovery/concurrency/session/live/chronology behavior;
- access control and multiplayer authority;
- rules/domain CORE integration with deterministic mechanics;
- diagnostics/maintenance/cleanup;
- test/CI/release/version/package/legal boundaries where they constrain implementation correctness/readiness.

Round-2 DIAMOND/STRONG accounting remains required evidence but is only one sub-ledger inside the final whole-project coverage gate.

---

# 3. Bidirectional audit requirement

R2.7 must prove both directions:

```text
A. ARCHITECTURE -> MACHINE
Every accepted semantic responsibility has a concrete machine/runtime/instruction/test destination or explicit NO-REPRESENTATION disposition.

B. MACHINE -> ARCHITECTURE
Every current runtime/schema/catalog/template/tool/test responsibility has an accepted semantic owner or is explicitly classified as derived, implementation-only, stale, debt, historical or out of scope.
```

A one-way Round-2 mapping is insufficient for implementation-planning entry.

---

# 4. Physical realization scope

Storage/root/index/sharding/HOT/SQLite mapping must also be project-wide.

R2.7 must not resolve only newly introduced Round-2 record families while leaving pre-existing Actor/Asset/mechanical/event/session/current/checkpoint/world/template families on unreviewed scaffold assumptions.

The final mapping must identify exact physical realization for every material accepted current/durable/derived/operational family, including explicit `NO DURABLE RECORD`, `NO SQLITE OWNER`, `DERIVED ONLY`, or equivalent where appropriate.

---

# 5. Whole-project instruction scope

Instruction/CORE/Project-Instructions mapping is also project-wide.

R2.7 must verify that all shipped role, mechanics, source, persistence, recovery, multiplayer, narration, preparation and domain-module instructions compose with accepted architecture and do not create hidden duplicate authorities or bypass deterministic gates.

---

# 6. Round-2-specific holistic review remains required

The previous whole-Round-2 composition review is retained, including:

- all 82 DIAMOND/STRONG dispositions plus later S14/S53/D15 changes;
- R2.1-R2.6 cross-composition;
- dormant/revisit trigger preservation;
- no accidental reactivation of rejected/negative ideas.

This Round-2 review is nested inside the broader whole-project audit rather than defining its outer scope.

---

# 7. Scope-discovery basis

The required question inventory is established in:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`

That inventory defines the initial whole-project audit horizon. During the actual Source Manifest/evidence pass, newly discovered owning/consumer dependencies may add audit questions; the inventory is a minimum, not a closed excuse to ignore newly found dependencies.

---

# 8. Supersession

The existing:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md`

is superseded as the active task brief because its exit/mapping language is too strongly centered on R2.1-R2.6.

Its valid detailed requirements remain evidence/input to the replacement brief, especially physical storage/index/HOT mapping, Context Runtime/TurnEnvelope realization, R2.5 collaboration/planning mapping, instruction ownership, Protocol-4 acceptance handoff and adversarial composition checks.

A replacement whole-project R2.7 Task Brief v2 owns current execution scope.

---

# 9. Implementation gate

Implementation planning remains blocked until the whole-project R2.7 audit closes.

R2.7 closure must establish that no unresolved architecture question remains whose answer could materially change:

- component/authority ownership;
- persistent data model;
- runtime interfaces;
- transaction/currentness/recovery topology;
- bootstrap/migration/update path;
- instruction architecture;
- test/release acceptance topology.

Only then may implementation planning begin.

---

# 10. Pre-release data compatibility / migration clarification

Owner clarification on 2026-08-24:

> No real campaigns/games currently depend on the existing campaign schemas, catalog shapes, templates or folder structures. R2.7 may therefore replace or delete stale machine structures directly without preserving backward compatibility with the current scaffold.

For the current architecture-finalization transition:

```text
EXISTING USER CAMPAIGNS REQUIRING MIGRATION: NONE
BACKWARD-COMPATIBILITY REQUIREMENT FOR CURRENT SCAFFOLD: NONE
LEGACY FIELD/RECORD PRESERVATION REQUIREMENT: NONE
```

Consequences:

- stale/retired fields, record classes, catalog entries, templates and roots MAY be removed rather than carried as aliases/dual-write compatibility surfaces;
- final schemas/catalogs/templates/folder structures SHALL represent only the accepted final architecture unless a separate current consumer proves otherwise;
- no migration artifact is required merely to transform the present unreleased scaffold into the final R2.7 machine model;
- this clarification does **not** remove the requirement for WP-20 to define a coherent future schema/version/evolution policy for campaigns created after release;
- this clarification does **not** authorize implementation before R2.7 closure; R2.7 still maps exact final replacements and implementation planning remains the next gate.

The final R2.7 closure target is therefore not a compatibility-preserving compromise. It is one **self-consistent final architecture with complete data models, schemas, catalogs, templates and folder structures** suitable for implementation planning.