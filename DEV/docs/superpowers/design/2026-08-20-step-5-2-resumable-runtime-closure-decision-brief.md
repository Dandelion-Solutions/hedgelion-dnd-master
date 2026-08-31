# Step 5.2 — Resumable Runtime Closure — Decision Brief

Status: **DECISION BRIEF — NO NEW OWNER DECISION REQUIRED**

Date: 2026-08-20

Basis:

- fixed pre-research charter;
- architecture task brief;
- research & architecture draft;
- analytical challenge;
- accepted Steps 2–5.1 constraints.

---

# 1. Decision statement

Step 5.2 should adopt the following architecture:

> **Resumable Runtime Closure is a correctness property over a compatible set of domain-native durable sources and the transitive closure of gameplay-significant native owners reachable from bounded typed recovery-routing evidence. It is not a new semantic owner, universal snapshot, scalar frontier, or mandatory first-class runtime record.**

At any recovery point the system promises after total process/chat/model-memory loss:

1. every gameplay-significant active native owner must be durable/recoverable in its own domain;
2. every independently active owner that cannot be discovered transitively from another guaranteed root must be reachable through bounded typed recovery routing;
3. every otherwise-unreachable armed temporal source owner must be boundedly discoverable so derived Temporal Agenda can be rebuilt;
4. fixed/accepted execution inputs, pending responses, mandatory-child identities, idempotency evidence and other irreducible continuation state remain with existing Step-3 owners;
5. derived caches/indexes are rebuilt and never win over native owners;
6. missing/incompatible required root targets are recovery/integrity defects rather than permission to guess or silently drop work;
7. recovery routing must be partitionable by existing writable/semantic scope and must not impose one globally hot mutable singleton across independent gameplay scopes.

---

# 2. Why no new human architecture decision is required

The remaining alternatives do not represent balanced product semantics or competing state-owner models.

The following choices are already eliminated by accepted architecture and evidence:

- **new semantic recovery authority** — violates existing owner boundaries without a proven independent lifecycle;
- **checkpoint as sole current root source** — incompatible with sparse checkpoint cadence;
- **runtime.session as sole root** — incompatible with multiplayer/multi-session lifetime;
- **CURRENT as copied runtime snapshot** — duplicates Step-3 owners and revives generic tactical/pending state;
- **event/history scan** — historical evidence cannot replace current owners and is unbounded;
- **serialized Temporal Agenda** — duplicates owner-local temporal authority;
- **one globally hot root registry** — creates artificial cross-scene write contention.

What remains is a later physical representation choice among equivalent implementations of the same routing contract:

- active-only path membership;
- typed per-kind indexes;
- per-scope routing sections;
- combinations of campaign and live-local indexes.

That choice depends on 5.3–5.8 protocol constraints and is owned primarily by 5.7/5.8. Choosing it now would be premature implementation/storage architecture, not a product-semantic decision.

---

# 3. Alternatives and dispositions

## Alternative A — native owners + unbounded discovery

Example: scan all runtime/world records and inspect status.

Disposition: **REJECTED**.

Reason:

Recovery cost scales with campaign age/storage size and can miss hidden semantic assumptions in historical records. Violates bounded-recovery requirement.

---

## Alternative B — first-class `runtime.recovery_closure`

Dedicated independently identified record that owns the complete closure.

Disposition: **REJECTED**.

Reason:

No independent semantic authority/lifecycle is proven. Native campaign/live/runtime sources already identify the state; a closure ID would duplicate composition identity and introduce lifecycle/versioning/GC obligations.

---

## Alternative C — one global recovery-root singleton/index

One campaign-global mutable root file listing every active owner.

Disposition: **REJECTED AS A REQUIRED ARCHITECTURE**.

Reason:

Creates unnecessary contention between independent scenes/sessions and conflicts with established partition-by-structure multiplayer design.

A cold, rarely changed global partition may still exist later for genuinely global roots, but Step 5.2 must not require all roots to mutate one singleton.

---

## Alternative D — partitionable typed recovery-routing projections over native owners

Active root membership is encoded through bounded typed indexes/references/active-only placements partitioned by native writable scope. Owner payloads remain in owners.

Disposition: **RECOMMENDED**.

Why:

- satisfies bounded recovery;
- preserves owner authority;
- supports multiple independent campaign/live scopes;
- keeps checkpoints sparse;
- keeps Agenda rebuildable;
- permits later 5.7/5.8 physical optimization;
- scales with active obligations rather than campaign history.

---

# 4. Canonical classification decisions

## Authoritative current state

Remain native:

- world/entity state;
- active Effect/Resource/LifeState temporal bindings;
- RuntimeCommand;
- Resolution;
- Procedure;
- Continuation;
- campaign allocator;
- live epoch state for routed live scopes;
- Interaction/IntentPlan when a materially unresolved accepted input is itself part of a promised durable resume point.

## Irreducible recovery evidence / routing

Includes as applicable:

- typed active-root membership/ref evidence;
- committed receipt/Event refs required for idempotency;
- fixed RNG already generated/accepted;
- pending Choice/Reaction offer identity/options;
- mandatory pending child descriptor/firing key;
- accepted invocation facts/catalog-context/dependency revision evidence;
- temporal anchors/context stored by native temporal owner;
- scene -> live-epoch routing pointer;
- recovery/checkpoint pointer/evidence where applicable.

## Rebuildable derived state

Includes:

- Temporal Agenda;
- MechanicalContext;
- condition/effect aggregate indexes;
- rule dependency DAG cache;
- loaded-record cache;
- derived mechanical values;
- Context Assembler bundles;
- repository query/listing caches;
- Story rendering/editorial buffers.

## Truly ephemeral or volatile-ahead-of-durable

Includes:

- uncommitted prospective segment deltas;
- presentation-only prompt wording;
- generic open “what do you do?” handoff text;
- HOT/SOFT changes not yet included in a promised durable source set;
- maintenance continuation frame when it is merely same-context handoff aid;
- transport preparation state unless 5.6 later proves independent crash-retry persistence need.

---

# 5. Recovery-routing law

Candidate canonical law:

> **BOUNDed ROOT DISCOVERY LAW** — At every promised durable recovery source set, every gameplay-significant active owner or armed obligation that is not guaranteed reachable from another admitted root must be discoverable through a bounded typed routing/index mechanism whose membership is coherent with the native owner state. Routing membership is recovery evidence, not semantic authority.

Supporting law:

> **PARTITIONABLE ROUTING LAW** — Recovery routing must admit partitioning by existing semantic/writable scope. No Step-5.2 invariant requires all independent campaign/live/runtime roots to update one shared mutable registry.

---

# 6. Execution-root decision

Minimum independently rootable execution classes:

```text
non-settled RuntimeCommand          when it owns unfinished descendant closure
active Procedure                    independently of Command lifetime
pending Interaction/IntentPlan      only when materially unresolved and promised durable
```

Transitively reached where applicable:

```text
Resolution
Continuation
child Resolution
pending child descriptors
receipts / MechanicalEvents
Procedure referenced by execution chain
```

Do not redundantly root every descendant if its parent/root relationship is durable and validated.

A Procedure must remain independently discoverable because it may be active between Commands.

---

# 7. Temporal-source decision

Temporal Agenda remains non-authoritative and disposable.

Cold recovery requires only:

1. bounded membership of otherwise-unreachable armed temporal source owners;
2. native owner state/TemporalBinding;
3. applicable chronology/procedure context evidence;
4. selected firing/mandatory child identity only after due work has crossed into committed execution semantics.

Do not store due order, next-due decisions or selected trigger state in the recovery-routing projection itself.

Step 5.3 owns the exact due-selection transition and no-lost/no-double processing.

---

# 8. Durable source-set decision

“Durable recovery basis” is not a scalar frontier.

For one recovery operation it means a compatible selection of native sources such as:

```text
campaign HEAD C
+ scene A live epoch LA at native live revision/head
+ scene B live epoch LB at its native revision/head
+ campaign/live-local runtime root partitions
+ native chronology/owner references
```

No implicit ordering is inferred among different domains.

Step 5.2 introduces no `RecoveryCut` record or universal source-set ID.

---

# 9. Closure/dependency rule

Candidate canonical rule:

> A promised durable recovery source set is valid only if every required root and the transitive required dependency closure of every recoverable owner is itself durable/reachable in the appropriate native domain, or explicitly rebuildable/optional. A recoverable owner may not depend on an unpublished shorter-lived identity/state.

This strengthens existing promotion/publication closure without changing its owner.

Examples:

- durable Continuation cannot require a vanished session-local entity;
- campaign-published owner cannot point to RAM-only Procedure;
- live-local provisional entity may remain valid inside the authoritative durable live epoch but cannot escape before promotion;
- root entry cannot point to a record absent from the same compatible durable source set.

---

# 10. Integrity decision

Missing cache:

```text
rebuild
```

Stale coordination/session pointer:

```text
refresh/rebind
```

Missing/incompatible required durable root or target:

```text
recovery blocked / scoped CANON_SUSPECT
-> targeted validation/repair
-> never guess/drop/replay silently
```

Exact runtime status/error code remains Step 5.7 implementation/protocol design.

---

# 11. RNG decision

Step 5.2 requires preservation of:

- already generated/fixed RNG values whose dependent execution is not fully settled;
- already committed/reserved RNG identity/state if such a reservation is itself part of accepted execution semantics.

Step 5.2 does **not** require:

- all future rolls to be reproducible across restart;
- one campaign-global deterministic RNG stream;
- persistence of verbose ResolutionTrace merely to retain fixed RNG.

Step 5.3 owns exact future RNG continuity representation.

---

# 12. Semantic resume decision outside mechanics

No new semantic resume-point class is admitted.

Rules:

- settled state + generic open handoff: recover scene/world state and regenerate presentation;
- pending mechanical choice/reaction: Continuation owns it;
- pending materially unresolved accepted declaration before Command: existing Interaction/IntentPlan owns it when the durability policy promises that unresolved point;
- exact transcript/prompt wording is not universal state authority.

---

# 13. Risks and mitigations

## Risk: projection omission silently loses owner

Mitigation:

- root membership changes join the same durability closure as owner activation/terminality;
- validation/maintenance tests assert enrollment completeness for known owner kinds;
- missing target causes typed recovery/integrity failure;
- broad scan permitted only as exceptional repair/audit, not normal recovery.

## Risk: projection becomes generic dumping ground

Mitigation:

- typed root classes only;
- references only, no copied owner state;
- no deadlines/order/priority/current resource values;
- class admission follows existing catalog rules.

## Risk: global contention

Mitigation:

- partitionable routing law;
- exact partitioning deferred to 5.7/5.8 with multiplayer write scopes as constraint.

## Risk: later protocol makes current decision impossible

Mitigation:

- representation-neutral logical contract;
- explicit change conditions recorded below.

---

# 14. Confidence and change conditions

Confidence: **HIGH** for:

- closure as property rather than authority;
- need for bounded root membership;
- Procedure independent rootability;
- Agenda rebuildability contingent on temporal-owner enumeration;
- no checkpoint/session singleton solution;
- no globally hot root singleton requirement.

Confidence: **MEDIUM** for exact eventual partitioning because 5.3–5.8 are intentionally unfinished.

Would change recommendation if later evidence proves:

- native source compatibility needs independent closure identity;
- distributed membership cannot be made crash-consistent;
- cross-domain active roots require one atomic transaction impossible under current branch topology;
- temporal due semantics require irreducible Agenda-local state;
- every Procedure can be proven durably reachable from another guaranteed root for its entire lifetime;
- a new fundamental semantic resume owner is required for unresolved player input.

Any such finding would reopen the relevant architecture decision rather than being patched into implementation.

---

# 15. Decision gate result

```text
new product-semantic decision required from owner: NO
new semantic state authority required: NO
new first-class recovery record required: NO
bounded typed recovery routing required: YES
routing must be partitionable: YES
exact storage/layout representation decided now: NO
next step: Candidate Specification
```

The recommended decisions are derived consequences of already accepted ownership, recovery and multiplayer constraints rather than a new balanced trade-off requiring human selection.
