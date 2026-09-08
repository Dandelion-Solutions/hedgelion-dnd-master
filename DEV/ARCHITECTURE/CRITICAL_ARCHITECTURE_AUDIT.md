# HDM Critical Architecture Audit — Historical Source-Neutral Retention

Status: **HISTORICAL / SUPERSEDED DERIVATION — NOT CURRENT IMPLEMENTATION AUTHORITY**

This file preserves the material HDM conclusions of the early catalog/mechanical-runtime critical audit after public-provenance sanitation. Current durable architecture owners, final accepted specifications, machine contracts and tests supersede this historical derivation wherever they are more specific or later.

## 1. Audit purpose

The audit challenged accepted catalog and mechanical-runtime design for duplicated authority, missing ownership, impossible later dependencies and unnecessary universal infrastructure. Its governing rule was minimum sufficiency: add a type, field, state or workflow only when a concrete invariant requires it.

## 2. Preserved first-pass conclusions

- Catalog capability, reusable definition, world-record and runtime-record classes require distinct ownership.
- Universal envelopes must not duplicate per-record version authority.
- Runtime identity allocation and HOT projection are implementation concerns constrained by stable identity/non-reuse law, not permission for duplicate canon.
- Actor HP/LifeState, Asset state, Activity execution, Rule Elements and persistence boundaries require explicit owners rather than prose inference.
- Activity and Rule Element shapes are bounded/typed contracts; broad argument/value containers are never permission for arbitrary executable data.
- Trigger behavior, operation arguments/results, cardinality and reference validity require deterministic compile/load validation where structural schema alone is insufficient.
- Persistence timing and publication mechanics must remain with their accepted owners; a convenience transport cannot weaken atomic publication/currentness requirements.
- Duration, recovery and multiplayer progression must not introduce a hidden wall-clock/background simulation loop.
- Mode profiles operate over the same canonical entity model; they must not fork world-state schemas merely for presentation or enforcement differences.

## 3. Preserved adversarial conclusions

### P2-1 — Dependency order must be executable

Knowledge/visibility and promotion boundaries needed by later multiplayer/mode work must exist before those consumers close. Rich authoring may remain later, but a backward dependency must not be hidden by roadmap order.

### P2-2 — HP and LifeState have one clear ownership split

Actor HP/temporary HP remain intrinsic Actor-state authority where materialized. Generic Resource machinery must not store a second copy of the same values. LifeState remains a separate Actor-state authority and is not permanently inferred from a numeric counter.

### P2-3 — Asset durability is not a duplicate Resource

Tracked structural integrity belongs to Asset durability. A distinct spend/recover pool such as charges or fuel may be a Resource; the same physical integrity value may not be stored in both places.

### P2-4 — Currency representation cannot create two writable authorities

One account/domain uses one authoritative representation. Conversion between physical holdings and a balance is an explicit atomic transition, not bidirectional passive duplication.

### P2-5 — Transformation has a bounded state-migration boundary

A definition-changing transformation preserves universal instance identity/placement/lineage while explicitly removing invalid definition-dependent state and initializing required new state. Unknown old fields are not copied forward and arbitrary patch payloads are not accepted.

### P2-6 — Resource lifetime/scope is explicit

Persistent pools, procedure-local budgets and derived capacities have different owners/lifetimes. One Resource definition concept may support them, but the storage model must not collapse them into one undifferentiated writable map.

### P2-7 — Passive equipment must not manufacture duplicate Effects

A separate Effect instance is justified only when independent lifecycle/target/parameter/duration state exists. Pure passive contributions may evaluate from their existing owner without materializing duplicate effect authority.

### P2-8 — Recovery and periodic mechanics are boundary-driven

Advancement occurs through explicit runtime/procedure/time/rest/event boundaries. The engine does not scan/tick the world continuously in the background.

### P2-9 — Resource availability and Activity commitment are distinct

Resource contracts expose validated spend/restore behavior; Activity execution owns the exact irreversible commitment point. A generic consume moment must not erase suspension/reaction semantics.

### P2-10 — Executable fixtures use production contracts

Minimum seed fixtures needed for contract/execution testing must use the same schemas and validation paths as production definitions. Fixture convenience does not create a second ruleset model.

### P2-11 — Closed mechanical surfaces require explicit registration

A semantic selector/accessor used by accepted mechanics must be present in the closed machine registry before executable use; prose examples do not authorize invented runtime surfaces.

### P2-12 — Health, effects and procedure budgets remain separate owners

The validated HDM conclusion is one intrinsic health authority, explicit Effect lifecycle/duration authority, and procedure-local action-economy/resource state. Zero HP is not a universal death rule, and no separate canonical entity is justified for every counter.

## 4. Deferred historical items

The early audit left several items as non-blocking until a current owner proved need, including richer lifecycle variants, generalized prerequisite expressions, catalog-gap transport, edited-message recovery and measured composition/trigger limits. Later accepted owners control their current disposition.

## 5. Public provenance note

The current public tree retains these HDM conclusions without preserving the external development-source trail used during the historical investigation. Required legal attribution, operational rules-source routing and HDM technical artifact provenance remain owned by their current dedicated surfaces.
