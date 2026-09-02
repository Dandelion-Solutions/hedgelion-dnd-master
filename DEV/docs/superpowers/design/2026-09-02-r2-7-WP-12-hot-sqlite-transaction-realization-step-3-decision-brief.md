# R2.7 WP-12 — Step 3 Decision Brief

Status: **COMPLETE — HUMAN DECISION REQUIRED: NO**

## 1. What is being decided

Select the local HOT/SQLite realization shape that can implement the already
accepted native-owner, ExecutionSegment, durability, publication, recovery,
currentness and live-CAS laws without creating a second semantic authority.

This decision does not select exact SQL DDL, database filename/path, library/API,
performance thresholds, publication cadence, recovery wire format or migration.
Those are later implementation/downstream concerns unless evidence promotes them.

## 2. Distinguishing requirements

A viable realization must:

1. preserve native semantic owners and owner-defined identities;
2. permit current established singleplayer SOFT owner state to be newer locally
   than the durable Git frontier;
3. provide one local atomic ExecutionSegment commit across the implicated native
   owner/runtime/evidence state;
4. keep external dialogue and repository/live network I/O outside SQLite
   transactions;
5. preserve distinct Interaction/IntentPlan/Command/Procedure/Resolution/
   Continuation lifecycles and embedded ExecutionSegment semantics;
6. hydrate known IDs through the WP-11 direct route and validate native identity;
7. retain exact source/currentness basis and invalidate stale local state;
8. keep routing/query/index/mechanical/context caches rebuildable and
   non-authoritative;
9. support generation-specific dirty/publication bookkeeping without a global
   timer/frontier or generic journal;
10. treat live shared establishment as exact-source CAS-bound rather than local
    SQLite-commit-bound;
11. remain evolvable while pre-release owner schemas are still being reconciled.

## 3. Alternatives

### Alternative A — Typed native-owner envelope + narrow derived helpers

SQLite stores validated typed native owner payloads under explicit owner-defined
identity, plus operational source/generation/dirty metadata. Separate helper
structures exist only for concrete bounded routing/query needs and are marked
rebuildable/non-authoritative.

Execution owners remain separate logical rows/classes. ExecutionSegment remains
embedded. Publication/recovery attempts remain ephemeral operation objects.

**Benefits**

- one transactional local substrate for Step-3 segment atomicity;
- minimal duplication of native machine schemas;
- owner identity/lifecycle remains explicit;
- pre-release schema evolution does not require a second full semantic schema to
  be independently maintained;
- derived helpers can be added/removed without owner migration;
- direct fit with R2.3 SQLite-format non-authority and WP-11 routing.

**Weaknesses**

- some owner fields are not first-class SQL columns;
- correctness depends on strict payload validation and typed accessors rather
  than arbitrary JSON use;
- measured query hotspots may later justify narrowly normalized projections.

### Alternative B — Dedicated normalized SQL table per native owner family

Each Actor/Asset/Effect/runtime family receives a dedicated relational schema
mirroring its current machine contract.

**Benefits**

- strong column-level constraints;
- direct SQL querying and conventional relational introspection;
- potential optimization for known stable query shapes.

**Weaknesses**

- duplicates the existing owner schema surface and creates a second migration
  problem;
- increases risk that SQL shape becomes de facto semantic authority;
- high churn while record families/contracts remain pre-release;
- encourages joins/foreign-key assumptions that can bypass native source/currentness
  and embedded-value boundaries;
- substantially larger implementation/test surface without a current measured
  requirement.

### Alternative C — Pure in-memory owners; SQLite only derived/cache support

Keep current owner state in process objects; use SQLite solely for derived indexes,
query caches or diagnostics.

**Benefits**

- smallest SQL semantic surface;
- no risk that local owner payload storage is mistaken for durable canon.

**Weaknesses**

- requires a separate transactional commit mechanism to atomically advance the
  accepted multi-owner Step-3 segment edge;
- recreates consistency/idempotency machinery already supplied by SQLite;
- weaker deterministic inspection/recovery testing of local transaction state;
- moves complexity into bespoke in-memory transaction code without an accepted
  reason.

## 4. Recommendation

**Choose Alternative A: typed native-owner envelope + narrow derived helpers.**

The envelope is a physical persistence/transaction mechanism, not a semantic
owner class. Every accepted owner payload remains validated by its own family
contract, identified by its native identity and routed/current through its
accepted source contract.

A dedicated helper/table is justified only by a concrete current operation that
cannot be represented safely as owner payload or a narrow rebuildable
projection. No generic `pending_work`, scheduler, publication journal, recovery
cut or global snapshot is admitted.

## 5. Strongest weakness

The main risk is accidental genericization: an envelope table can become a
schema-less property bag if callers are allowed to write arbitrary payloads or
perform semantic operations without family validation/typed accessors.

The candidate specification must therefore make owner-contract validation,
native identity, typed family admission and non-authoritative helper status hard
requirements rather than implementation advice.

## 6. Consequences versus alternatives

- Versus B, A trades some direct SQL expressiveness for substantially less schema
  duplication and lower authority-drift risk.
- Versus C, A accepts local physical owner payload storage in exchange for one
  deterministic transactional commit kernel already compatible with the accepted
  Step-3 architecture.
- A preserves option value: a measured hotspot may later receive a family-specific
  projection/table without redefining native owner authority or durable format.

## 7. Remaining uncertainty

Exact DDL, serialization choice inside the owner payload, helper-index selection,
database file lifecycle/path and performance tuning remain implementation details
subject to the later approved implementation plan and measured WP-24 work. They do
not affect the architectural choice while owner validation/currentness boundaries
are preserved.

Recommendation confidence: **HIGH**

What evidence would change this recommendation: a current accepted/measured
requirement for broad relational field-level operations that bounded derived
helpers cannot satisfy, or an owner requirement that cannot be validated/committed
through the typed envelope without duplicating semantic authority.

## 8. Human decision

**Human decision required: NO.**

The inspected accepted architecture already determines the authority and
transaction boundaries strongly enough that Alternative A is the mechanically
best-fitting realization. No product semantic, ownership transfer, hard-to-reverse
compatibility choice or material risk acceptance remains for the human architect.
