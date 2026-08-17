# HDM Critical Architecture Audit

Status: **COMPLETE — PASS 2 OWNER-APPROVED**

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

**Disposition:** Step 5 owns one explicit reconciliation decision. Until then,
current CORE behavior wins and the proposal remains non-authoritative.

### A7 — No hidden real-time loop may enter duration or multiplayer design

Current documents correctly reject wall-clock simulation and background event
processing. Durations advance only through explicit procedure/time/rest/event
commands; multiplayer ordering comes from canonical frontiers and live-scene
ownership.

**Disposition:** preserve as a mandatory constraint in Steps 2 and 5.

### A8 — Mode profiles must not fork the world-state schema

Quick narrative play may skip exact mechanics; canonical play may enforce them;
detective play may isolate context. Duplicating Actor/Asset/Event schemas per
mode would make later switching and persistence inconsistent.

**Disposition:** Step 6 must model modes as activation/adjudication/context
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

The first two checks passed, but Step 1 was reopened for the independent
adversarial dependency pass below. Step 2 remains blocked until its findings
are dispositioned.

## 6. Pass 2 — adversarial dependency and authority review

The first pass asked whether every known gap had an owner. This pass asks the
harder questions: whether the proposed order is actually executable, whether
two records can become competing authorities, and whether a locally reasonable
contract produces an impossible later migration.

### P2-1 — The roadmap contains backward dependencies

The current order places durability/multiplayer before knowledge and visibility,
yet multiplayer narration and shared events require a minimum disclosure model.
Game-mode design also places strict detective isolation before the knowledge
model that would enforce it. Promotion is postponed to the final step even
though publication closure already requires promotion of durable dependencies.

**Validated verdict:** reorder the remaining roadmap so the minimum
knowledge/visibility and promotion interfaces are defined before multiplayer
and mode profiles close. Rich chapter/lore authoring and public catalog-gap
transport can remain later.

### P2-2 — Health currently has two plausible authorities

`ACTOR_MODEL.md` stores `hp.current`, maximum components, and `hp.temporary`,
while the capability catalog registers `resource.health` and
`resource.temporary_health`, and Actors also own a generic resource map. Without
an explicit boundary, an implementation could store the same current HP twice.

**Validated verdict:** preserve the accepted fast-path Actor `hp` object as
the single state authority for hit points and temporary hit points. Generic
Resource definitions may describe other pools; health mechanics may be reused
as resolver capability/schema vocabulary but must not create a second Actor
counter. Step 2 must either encode this distinction or present a demonstrably
simpler single-authority alternative.

### P2-3 — Asset durability has the same duplication risk

`ASSET_MODEL.md` gives durable Assets a direct durability state, while generic
Resources can also represent bounded pools. Treating every bottle's structural
integrity as a Resource instance adds IDs, recovery semantics, and joins with no
benefit; storing it in both places is invalid.

**Validated verdict:** direct Asset durability is authoritative when tracked.
Do not create a generic Resource instance for the same integrity value. A
Resource is justified only for a distinct spend/recover mechanic such as
charges or fuel.

### P2-4 — Currency permits two representations but not two authorities

The catalog permits physical currency Assets and a
`resource.currency_balance` mechanic. That is useful for different campaign
styles, but the same funds cannot simultaneously exist as coins in inventory
and as an unrelated balance.

**Validated verdict:** the selected currency/denomination definition declares
one storage representation for a given account/domain. Conversion is an atomic
transition, not a passive projection written in both directions. No universal
currency-ledger entity is added now.

### P2-5 — Transformation needs an explicit state migration boundary

Changing a stable Asset's `definition_id` preserves physical identity, but the
documents do not yet say what happens to definition-owned resources and other
state that are invalid for the new form. A healing potion transformed into an
empty bottle must not retain a usable healing charge; a refilled bottle needs a
new valid resource state.

**Validated verdict:** `op.transform_entity` requires a validated, bounded
state transition supplied by the selected Activity/operation contract. Runtime
preserves universal instance state (identity, placement, lineage) and validates
the exact removal/initialization of definition-dependent state. It must not
copy unknown old state forward or let the LLM submit arbitrary JSON Patch.

### P2-6 — Persistent, procedure-local, and derived resources are different

Spell slots and item charges persist on an Actor/Asset. Action, reaction, and
movement budgets exist only inside an encounter/turn/procedure. Maximum values
may be derived from build and active Effects while current values are mutable.
Putting all three in one undifferentiated map makes recovery, persistence, and
cache invalidation ambiguous.

**Validated verdict:** keep one Resource definition concept, but require its
scope/state owner to be explicit in the definition contract. Do not create
separate entity classes. Step 2 must distinguish persistent stored current
state, procedure-local current state, and derived capacity without duplicating
the resolved maximum as canon.

### P2-7 — Passive equipment must not manufacture duplicate Effects

Rule Elements embedded in an equipped/accessible Asset can already become
active through predicates. Creating a `world.effect` copy for every passive
piece of equipment would duplicate provenance, activation, and removal state.

**Validated verdict:** an Effect instance exists only when the mechanic has
independent duration, stacks, parameters, targets, or lifecycle. Pure equipment
passives evaluate from the Asset owner directly. The `effect.equipment_passive`
facet is valid for a genuine Effect granted by equipment, not a requirement to
materialize every embedded equipment rule as an Effect.

### P2-8 — Recovery and periodic effects cannot imply a background clock

Recovery triggers, periodic damage/healing, expiry, and concentration cleanup
could accidentally reintroduce a timer/event loop. Existing chronology rejects
that model.

**Validated verdict:** every advancement occurs inside an explicit runtime
command or Activity boundary (turn/round transition, rest completion, local-time
advance, named event). Runtime queries only affected indexed Effects/Resources;
it never scans or ticks the world in the background.

### P2-9 — Resource gates and Activity costs have different commitment rules

A pure Rule Element gate normally proves availability and may request atomic
consumption with its contribution. Activity costs may become irreversible at a
specific segment even when a later reaction prevents the primary effect, as
with a spell slot and Counterspell. Treating both as one generic `consume`
moment would make suspension semantics incorrect.

**Validated verdict:** Step 2 owns Resource state/recovery; Step 3 owns the
commitment point. The Resource contract exposes validated spend/restore
operations but does not decide Activity segment timing.

### P2-10 — Exact seed IDs are needed before executable examples can close

Focused Activity tests cannot validate references such as action budgets,
damage types, or standard resources unless a small selected ruleset seed exists.
Postponing all seed ownership to the final step would make Step 3 tests
syntactic rather than executable.

**Validated verdict:** Step 2 may introduce only the minimum seed fixtures
needed to validate its contracts; Step 3 may add the minimum executable fixtures
needed by its cases. Full SRD seed coverage and packaging remain final closure
work. Fixtures must use the same schemas as future production definitions.

### P2-11 — The current selector registry omits an accepted HP selector

`ACTOR_MODEL.md` already refers to `actor.hp.maximum` as an Effect contribution
surface, but catalog 1.2.0 does not register it. Because Rule Elements use a
closed selector registry, leaving this mismatch until implementation would
force either prose-driven arithmetic or an invented runtime selector.

**Disposition:** Step 2 must settle and register the minimum health selectors
alongside the Resource/Effect boundary. Step 1 records the dependency; it does
not guess the final selector family before the health contract is written.

### P2-12 — D&D validation supports separate intrinsic health and local budgets

The official 2024 Basic Rules treat temporary HP as distinct from normal HP,
not healing, non-stacking, and normally lasting until depleted or a Long Rest.
They require player-character death saves at zero HP and refresh a spent
Reaction at the start of the creature's next turn. Spell duration and
Concentration are likewise explicit effect/procedure rules rather than a
wall-clock service.

These rules support the ownership split above: one intrinsic Actor health
object, explicit Effect duration, and procedure-local action-economy state.
They do not justify a separate canonical entity for every counter.

Primary references:

- <https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game>
- <https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary>
- <https://www.dndbeyond.com/sources/dnd/br-2024/spells>

## 7. Pass 2 exit gate

- [x] Challenge stage ordering for backward dependencies.
- [x] Search accepted Actor/Asset/Activity contracts for duplicate authorities.
- [x] Check transformation, recovery, trigger, and procedure-scope boundaries.
- [x] Validate or revise each preliminary verdict against the repository's
  authoritative contracts and D&D requirements.
- [x] Reorder the six-step roadmap without changing its six-stage gate.
- [x] Apply accepted corrections to normative architecture; defer schema fields
  whose exact shape is the explicitly gated output of Step 2 or Step 3.
- [x] Run schema/catalog audit and review the final diff.
- [x] Architecture owner accepts or revises the Pass 2 verdict package.

Step 1 is closed. The architecture owner accepted this package after the
current environment's unavailable Superpowers integration was disclosed. This
is the initial explicit fallback recorded under `DESIGN_PROCESS.md`; it does
not waive the Superpowers gate for Step 2 or later stages.
