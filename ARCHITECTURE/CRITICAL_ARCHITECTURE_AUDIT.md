# HDM Critical Architecture Audit

Status: **COMPLETE — block review and cross-document review passed**

Roadmap owner: Step 1 of `ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Audit purpose

This audit checks the architecture already accepted during catalog and
mechanical-runtime design. It does not solve later blocks prematurely. Its job
is to find contradictions, missing ownership, duplicated authority, and choices
that would make a later implementation unnecessarily expensive or impossible.

The governing design rule is minimum sufficiency: add a type, field, state, or
workflow only when a concrete invariant needs it.

## 2. Reviewed blocks

| Block | Verdict | Notes / owner |
|---|---|---|
| Four catalog layers and class inventory | **PASS** | Capability registry, reusable definitions, world records, and runtime records are separated. Machine catalog 1.2.0 is the ID authority. |
| Universal definition/world envelopes | **PASS** | Minimum required fields, forward references, localization, metadata placement, and no per-record version duplication are coherent. |
| Identifier policy and HOT object cache | **PASS** | Runtime allocation, per-kind widths, local IDs before promotion, non-reuse, and optimistic multiplayer reconciliation have one owner. Concrete SQLite layout belongs to implementation, not this catalog contract. |
| Actor model | **PASS WITH DEPENDENCY** | Progressive materialization, one actor model, derived level, split modifiers, lazy combat statistics, groups, and ownership are coherent. Resource/effect state cannot close before Step 2. Life-state variants beyond zero-health death/destruction remain optional backlog work. |
| Asset model | **PASS WITH DEPENDENCY** | Placement, accessibility, hands, implicit draw/stow, stacks, attunement, improvised use, durability, destruction, and directed definition transformation are coherent. Resource/effect details belong to Step 2. |
| Activity model | **BASELINE, NOT CLOSED** | The recipe boundary and multi-intent distinction are sound. Exact operation schemas, segment commitment, suspension receipts, and focused examples belong to Step 3. |
| Rule Elements and Trigger Bindings | **BASELINE, NOT CLOSED** | Embedded pure Contributions and Signal/Event separation are sound. Exact selector/operation value contracts, stacking tables, trigger mode semantics, and chain limits belong to Steps 2–3. |
| Persistence and checkpoint transport | **CORE CURRENT; PROPOSAL CONFLICT IS QUARANTINED** | `DURABILITY_GUARD.md` owns WHEN, `PERSISTENCE.md` owns HOW, and campaign publication retains atomic tree/CAS semantics. The mechanical proposal may not introduce a one-file Contents fallback or continue irreversible mutations after a failed HARD boundary. Step 4 must reconcile any proposed policy change before CORE changes. |
| Gameplay chronology and event-local time | **PARTIAL** | Abstract ordered timeline and explicit local budgets are accepted. Spending/expiry and multiplayer cross-scene reconciliation belong to Steps 2 and 4. |
| Game modes and performance | **PARTIAL** | The fast path and presentation-detail policy exist, but mode profiles do not yet define enabled mechanics or strict context isolation. Step 5 owns this. |
| Lore, chapters, knowledge, and secrets | **PARTIAL** | Public-by-default lore and explicit restricted knowledge are conceptually accepted. Context assembly, disclosure views, chapter storage, and strict-isolation behavior belong to Step 6. |
| Promotion, migration, catalog-gap, and ruleset seed | **OPEN, OWNED** | These are not hidden blockers: Step 6 owns their contracts. Edited-message rollback remains deliberately deferred but must not be made impossible by checkpoint identity choices. |

## 3. Cross-document findings

### A1 — Normative authority is clear, but derivation tables are stale

`CATALOG_MODEL.md` intentionally preserves early derivation tables. Some IDs in
those tables, such as `asset.misc`, are absent from catalog 1.2.0. The document
labels those tables non-normative, so runtime correctness is not ambiguous, but
they remain a human-maintenance hazard.

**Disposition:** fix during Step 1. Historical reasoning may remain, but stale
concrete IDs must not look like selectable catalog values. Prefer references to
the machine catalog over a second manually maintained enumeration.

### A2 — Structural JSON Schema validation works, semantic dispatch is partial

The maintenance audit validates Draft 2020-12 schemas and current catalog
instances. Kind-specific dispatch currently exists for Activity and Asset only;
operation-specific Activity arguments/results and Rule Element values are still
registry promises rather than schemas.

**Disposition:** not a failure of the accepted envelope. Step 2 owns Resource,
Effect, and Condition schemas. Step 3 owns operation/result and Contribution
schemas. No implementation may treat today's broad `args` or `value` shapes as
permission for arbitrary executable data.

### A3 — Trigger Binding without `mode` has no defined behavior

The prose describes three materially different modes, while the structural
schema and minimum example require only `on` and `activity_id`. No default is
defined. An omitted field would therefore require runtime or LLM guessing.

**Disposition:** blocking within Step 3. Choose one explicit rule: require
`mode`, or define and schema-encode a single default. Do not add a workflow or
extra entity to solve it.

### A4 — Activity cardinality and operation contracts need compile-time checks

The structural schema cannot prove `targeting.minimum <= targeting.maximum`,
that referenced IDs exist, or that a selected operation accepts its arguments.
This is expected only if the catalog compiler owns those checks explicitly.

**Disposition:** Step 3 must publish the compiler validation table and focused
negative cases. JSON Schema remains the shape validator; cross-record and
operation-registry checks remain compiler validation, avoiding duplicated
authority.

### A5 — Resource identifiers are currently illustrative, not seed-complete

Examples use definition references such as `resource.action`, while the machine
catalog currently registers resource *mechanics*, not a complete standard
ruleset definition package. This is valid only while examples are clearly
illustrative and catalog loading performs reference validation against the
selected seed package.

**Disposition:** Step 2 defines the Resource contract; Step 6 assigns ownership
and packaging for the selected D&D/SRD seed. Do not put every concrete resource
definition into the engine capability registry.

### A6 — Proposed durability changes cannot bypass current CORE barriers

The mechanical proposal discusses more frequent HARD boundaries and is marked
as requiring a later CORE policy decision. Current CORE deliberately batches
ordinary singleplayer durable changes as SOFT. A transport adapter may cache
capabilities, but a general Contents-API checkpoint is not equivalent to an
atomic campaign-tree publication.

**Disposition:** Step 4 owns one explicit reconciliation decision. Until then,
current CORE behavior wins and the proposal remains non-authoritative.

### A7 — No hidden real-time loop may enter duration or multiplayer design

Current documents correctly reject wall-clock simulation and background event
processing. Durations advance only through explicit procedure/time/rest/event
commands; multiplayer ordering comes from canonical frontiers and live-scene
ownership.

**Disposition:** preserve as a mandatory constraint in Steps 2 and 4.

### A8 — Mode profiles must not fork the world-state schema

Quick narrative play may skip exact mechanics; canonical play may enforce them;
detective play may isolate context. Duplicating Actor/Asset/Event schemas per
mode would make later switching and persistence inconsistent.

**Disposition:** Step 5 must model modes as activation/adjudication/context
policy over the same canonical entities. A transition may be refused when
required historical mechanics were never materialized; the architecture must
not pretend every mode switch is lossless.

## 4. Deferred items that are not blockers

- edited-message branch detection and rollback to a matching checkpoint;
- richer actor life-cycle states beyond the current zero-health rule;
- a generalized prerequisite-expression language for attunement;
- a public catalog-gap/bug submission transport;
- measured limits for composition and trigger depth, pending focused tests.

These items remain visible, but none justifies a new universal entity or field
in the current contracts.

## 5. Step 1 exit checklist

- [x] Inventory every accepted design block and assign a verdict.
- [x] Assign every incomplete fundamental block to roadmap Steps 2–6.
- [x] Run machine schema/catalog consistency validation.
- [x] Remove or neutralize stale selectable IDs in derivation documentation.
- [x] Re-run the maintenance audit and repository diff review.
- [x] Update `CATALOG_DESIGN_STATUS.md` with the roadmap and exact continuation
  point.

Step 1 is closed. Step 2 may begin; later steps remain gated.
