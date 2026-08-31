# Step 5.2 — Resumable Runtime Closure — Canonical Specification

Status: **CANONICAL ARCHITECTURE — STEP 5.2 CLOSED**

Date: 2026-08-20

Basis:

- `2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-task-brief.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-research-draft.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-analytical-challenge.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-decision-brief.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-candidate-spec.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate.md`

Prerequisites:

- Step 5.0 contamination cleanup;
- Step 5.1 B-NARROW frontier model;
- Step 3 deterministic execution ownership;
- Steps 1–2 temporal/recovery ownership;
- Step 4 truth/knowledge/disclosure/Story ownership.

This specification defines Step-5.2 logical architecture. It intentionally does
not select final repository paths, checkpoint wire format, Git publication
algorithm, live-epoch storage partition, due-work state machine, durability
cadence, chronology representation or GC policy.

---

# 1. Canonical definition

**Resumable Runtime Closure** is the correctness property that, for one promised
durable recovery operation, every gameplay-significant current owner, unresolved
execution dependency and pending obligation required to continue from the
selected compatible domain-native durable sources is recoverable through bounded
typed native routing, while non-authoritative derived state can be rebuilt.

Resumable Runtime Closure is **not**:

- a new semantic state owner;
- a mandatory first-class runtime record;
- a universal snapshot of HOT state;
- a generic pending-work table;
- a serialized Temporal Agenda;
- a common revision/frontier algebra;
- a scalar `RecoveryCut` identity;
- a transcript/model-memory snapshot;
- a reason to merge campaign and live writable authority.

A fresh runtime with no prior chat/model/process memory must be able to resume the
last **actually promised durable** gameplay point from the surviving native
sources. State that policy legitimately allowed to remain volatile ahead of that
point may be lost; the runtime never invents it after destruction.

---

# 2. Canonical laws

## LAW 5.2-1 — NATIVE OWNER PRESERVATION

Recovery metadata, checkpoints and routing projections SHALL NOT replace or
duplicate current writable authority.

Examples:

```text
Procedure ResourceState       -> runtime.procedure
Resolution execution state    -> runtime.resolution
suspended response state      -> runtime.continuation
mandatory child closure       -> runtime.command / committed segment evidence
Effect temporal state         -> world.effect
world HP/location/ownership   -> normal world owners
live-owned mutable truth      -> active live epoch
campaign allocation state     -> runtime.id_allocator
```

Recovery reads those values from their owners or accepted irreducible execution
evidence already owned by those records.

---

## LAW 5.2-2 — BOUNDED ROOT DISCOVERY

At every promised durable recovery source set, every gameplay-significant active
owner or armed due-capable obligation that is not guaranteed boundedly reachable
from another admitted root SHALL be discoverable through a bounded typed
routing/index mechanism.

Normal cold recovery SHALL NOT require:

- scanning all campaign files;
- scanning all historical runtime records;
- scanning broad Git history;
- loading the entire WORLD graph;
- reconstructing state from Story/transcript prose.

Exceptional integrity/maintenance repair may use broader evidence after the
normal bounded recovery path is already known to be suspect.

---

## LAW 5.2-3 — ROUTING IS RECOVERY EVIDENCE, NOT SEMANTIC AUTHORITY

Recovery-routing membership may answer only:

> Which typed native owner/reference should be loaded and validated?

It SHALL NOT independently own:

- owner lifecycle/current state;
- Procedure resources;
- pending-child payload;
- HP/resource/effect values;
- temporal deadline/due result/order;
- chronology relation;
- RNG result;
- Choice/Reaction option set;
- live overlay truth.

If a listed owner is terminal, native terminal state wins and stale routing is
repaired. If a required listed owner is missing/incompatible, recovery blocks or
raises scoped integrity suspicion. An omitted active owner is a routing
completeness defect, not evidence that the owner semantically ceased to exist.

---

## LAW 5.2-4 — PARTITIONABLE RECOVERY ROUTING

Recovery routing SHALL be partitionable by existing semantic/writable scope.

Step 5.2 SHALL NOT require all independent scene/session/live/runtime membership
changes to mutate one campaign-global hot singleton, generation, digest, count or
root registry.

A later implementation may encode bounded membership through:

- active-only path membership;
- typed per-kind indexes;
- per-scene/per-Procedure routing sections;
- campaign-global cold partitions for genuinely global roots;
- live-epoch-local partitions;
- a combination of these.

Exact representation is deferred to later persistence/recovery/live slices.

---

## LAW 5.2-5 — TRANSITIVE REQUIRED-DEPENDENCY CLOSURE

A promised durable recovery source set is valid only when every **semantically
required recovery dependency** of every recoverable owner is one of:

1. durable/recoverable in its appropriate native domain;
2. explicitly optional; or
3. deterministically rebuildable from surviving owner/evidence.

A recoverable owner SHALL NOT depend on required RAM-only, unpublished or
shorter-lived identity/state that will disappear on cold recovery.

This law does **not** recursively pull every informational/reference edge in the
world graph into recovery closure. Only dependencies whose absence can change
correct resume semantics are required.

Examples of required dependencies:

- active Procedure referenced by Resolution;
- fixed target/entity state required to resume a suspended mechanic;
- accepted catalog/rules context;
- fixed pending-response candidate identities;
- routed live scope owning current mutable truth.

Examples not automatically required:

- unrelated biography links;
- optional descriptive relationships;
- arbitrary historical lore provenance;
- Story projection dependencies that do not own current mechanics.

---

## LAW 5.2-6 — DERIVED STATE REBUILDS

Derived state SHALL NOT become recovery authority merely to avoid recomputation.

At minimum this includes:

- Temporal Agenda;
- MechanicalContext;
- Condition/Effect aggregation and reverse indexes;
- mechanical dependency DAG/cache state;
- loaded record/entity cache;
- derived AC/modifiers/speeds and similar calculations;
- Context Assembler bundles/source-selection working state;
- repository query/listing caches;
- Story rendering/editorial working buffers.

Missing derived state is rebuild work. If a serialized derived value disagrees
with its native owner inputs, discard/rebuild the derived value.

---

## LAW 5.2-7 — NO INVENTED LOST HOT STATE

Gameplay-significant HOT/SOFT state may legitimately exist ahead of the last
promised durable recovery source set under accepted sparse durability semantics.

If total process/chat/context loss destroys that volatile current state before a
later durability protocol successfully includes it in a promised durable source
set, recovery SHALL return to the last actual durable source set and SHALL NOT:

- invent the missing delta;
- infer player choices from plausibility;
- pretend unpublished state committed;
- replay old mechanics solely to recreate a desired newer state.

Step 5.2 does not decide when 5.4/5.5 must force a newer durable boundary.

---

## LAW 5.2-8 — DOMAIN-NATIVE RECOVERY SOURCES

One recovery operation may use several compatible native durable sources, for
example:

```text
campaign commit C
scene A live epoch/head LA
scene B live epoch/head LB
campaign/live-local runtime routing partitions
native chronology/Procedure references
```

Participation in one recovery operation SHALL NOT imply:

- scalar comparability;
- a total order;
- shared revision numbers;
- fictional chronology order;
- one merged writable authority.

Compatibility follows explicit native references/ownership contracts.

---

## LAW 5.2-9 — PINNED NATIVE HYDRATION

One recovery/hydration attempt SHALL resolve each participating mutable native
source to an exact revision before consuming dependent state from that source.

Dependent reads for that attempt are pinned to those exact native revisions.

If a required refresh or compatibility check changes the selected revision set,
the affected hydration selection is invalidated/reselected rather than silently
mixing branch-relative reads from different revisions.

This law does not create a common frontier or order among those revisions.

---

## LAW 5.2-10 — OWNING-SCOPE RESOLUTION

Required recovery dependencies SHALL resolve through the current native
ownership/routing contract for that identity and scope.

The existence of an older valid representation in another domain SHALL NOT
authorize fallback when a different native owner currently owns mutable truth.

In particular:

```text
campaign representation = durable base/reference
active live epoch        = current operational owner for live-owned mutable scope
```

If the pointed live owner is missing/incompatible, recovery blocks/suspects that
scope. It does not silently use stale campaign base state.

---

## LAW 5.2-11 — ROOT MEMBERSHIP COHERENCE

Whenever a native owner transition changes whether that owner requires
independent recovery-root membership, the corresponding routing membership change
is a required derivative of the native lifecycle transition.

The native owner decides lifecycle; routing reflects it.

A durability acknowledgement that includes such an owner lifecycle change SHALL
include the required routing membership change in the same semantic durability
closure strongly enough to prevent:

- durable active owner + missing required enrollment;
- durable root + missing required owner;
- premature root removal that makes unfinished work unreachable.

Exact transaction mechanics are later Step-5 work.

---

## LAW 5.2-12 — INTERPRETABILITY CLOSURE

A promised recoverable operational owner is resumable only when the compatible
runtime/catalog/rules interpretation context accepted by that execution can be
resolved under the campaign engine/package compatibility contract.

A fresh runtime SHALL NOT silently reinterpret an open Resolution/Continuation
under arbitrary newer ambient mechanics.

Missing required compatible runtime/catalog interpretation context is a recovery
prerequisite failure or requires explicit authorized migration/adoption. Campaign
storage does not need to contain engine bytes merely to satisfy this law.

---

# 3. Recovery-state classification

Every gameplay/runtime concept used in cold recovery must fit one of these
classes:

```text
AUTHORITATIVE STATE
IRREDUCIBLE RECOVERY EVIDENCE / ROUTING
REBUILDABLE DERIVED STATE
TRULY EPHEMERAL STATE
VOLATILE CURRENT STATE AHEAD OF DURABLE SOURCE SET
DEFECT / UNOWNED REQUIRED STATE
```

A value is not promoted into durable recovery state merely because recomputation
is inconvenient.

A value is not classified ephemeral when losing it can change the gameplay point
that the system has explicitly promised to recover.

---

# 4. Native execution owners

## 4.1 RuntimeCommand

A non-settled RuntimeCommand is independently recovery-relevant while it owns
unfinished mandatory descendant closure.

Its native contract preserves accepted request identity/fingerprint, catalog
context, invocation facts, root execution linkage, disposition, pending mandatory
children and receipt evidence.

A settled Command need not be enumerated during every cold start solely because
it remains directly addressable for later idempotent retry/audit. Active-root
enumeration and terminal-record retention/addressability are distinct concerns.

---

## 4.2 Procedure

Procedure remains the sole owner of procedure-local ResourceState and has an
independent lifetime across Commands, Resolutions, reactions, suspensions and
retries.

Canonical logical lifecycle:

```text
Procedure ACTIVE
    after accepted Procedure creation/open semantics
    and across gaps between participating Commands/Resolutions

Procedure TERMINAL
    only after explicit typed Procedure-closing/reset/terminal semantics commit
```

Therefore:

- absence of an open Command does not terminate Procedure;
- Encounter/Scene status alone does not define Procedure lifetime;
- recovery routing membership cannot be the sole semantic evidence that Procedure
  is active;
- later machine realization must expose enough Procedure-owned typed state or
  accepted lifecycle evidence to validate active/terminal membership.

An active Procedure must be independently boundedly discoverable unless another
root is proven to reach it throughout the full Procedure lifetime.

---

## 4.3 Resolution

An active/suspended/blocked Resolution remains native operational state.

When boundedly reachable from an admitted root it need not be redundantly listed
as a separate recovery root.

Required native state as applicable includes:

- root/initiating command or causal invocation key;
- Activity/catalog binding;
- optional Procedure reference;
- status/cursor/safe recompute phase;
- fixed RNG results;
- invocation facts/prior typed exports;
- child references;
- current Continuation reference;
- committed segment/receipt evidence.

---

## 4.4 Continuation

Continuation remains one portable suspended Resolution generation.

It preserves the accepted Step-3 irreducible suspension payload and SHALL NOT gain
copied Procedure ResourceState, MechanicalContext, Temporal Agenda, Condition
indexes, DAG caches or trusted prospective StateDeltas for recovery convenience.

If the current Resolution durably references the current Continuation generation
and Resolution is boundedly reachable, Continuation need not be independently
rooted.

---

## 4.5 Pending Interaction / IntentPlan

A materially unresolved accepted player input before Command creation is
conditionally recovery-relevant only when the applicable durability/handoff
policy promises that exact semantic point across cold restart.

Existing Interaction/IntentPlan semantics own that state.

Examples:

- accepted target declaration awaiting material clarification;
- compound IntentPlan where earlier clauses committed and a later material clause
  remains unresolved.

Not independent recovery owners merely by existing:

- generic open `what do you do?` presentation;
- optional suggestion lists;
- unaccepted generated narration;
- ordinary prompt wording.

No generic `pending_prompt` / `semantic_resume_point` class is admitted.

If exact message wording remains the only evidence preserving a materially
accepted intent, that specific message/Interaction evidence is temporarily
irreducible until sufficient typed semantic pending-input state is materialized.
This does not make the complete transcript universal authority.

---

# 5. Minimum current root classes

Current minimum logical independently rootable classes are:

```text
A. non-settled RuntimeCommand
   when unfinished descendant closure remains

B. active Procedure
   independently of Command lifetime

C. materially unresolved accepted Interaction/IntentPlan
   only when an applicable durability/handoff policy promises that point

D. otherwise-unreachable armed due-capable temporal source owner
```

Known singleton:

```text
runtime.id_allocator = campaign-allocator
```

The allocator does not require active-membership discovery because its identity
is deterministic.

Common transitive descendants need not be redundantly rooted when validated
forward references already provide bounded traversal:

```text
Command
  -> Resolution
      -> Continuation
      -> child Resolutions
      -> Procedure ref
      -> receipts / MechanicalEvents
  -> pending child descriptors
```

General future root-admission rule:

> Any admitted native operational owner with independently active recoverable
> lifetime that is not guaranteed boundedly reachable from another admitted root
> must itself receive typed recovery routing through normal architecture/catalog
> evolution.

No untyped generic pending/work registry is allowed.

---

# 6. Irreducible execution continuity

## 6.1 Mandatory post-commit child identity

If a committed segment/Event requires mandatory descendant work, stable pending
child/firing identity is irreducible execution evidence until that work is
materialized/settled.

Recovery SHALL NOT substitute a later scan of current trigger bindings for a
missing historical selected firing.

If the parent causal commit exists but required child identity was not durably
materialized as required by Step 3, that is an integrity/persistence defect.

---

## 6.2 Fixed RNG

Already generated/accepted raw RNG whose dependent execution remains unfinished
must survive with Resolution/Continuation/committed continuity evidence.

Cold recovery SHALL NOT reroll it merely because the process restarted.

Verbose ResolutionTrace SHALL NOT be its sole continuity owner.

---

## 6.3 Future RNG

Step 5.2 does not require all future random experiments to reproduce one global
sequence after restart.

Only already committed/reserved future RNG identity/state whose reservation has
itself entered accepted execution semantics must survive.

Step 5.3 owns exact future-RNG representation and no-double-consumption behavior.

---

## 6.4 Pending Choice / Reaction

A fixed Choice/Reaction offer that belongs to a durable Continuation must preserve
at least the semantic identity needed for exact resume:

- Continuation generation;
- offer identity;
- responder identity;
- bounded candidate/option identities;
- applicable single-consume/idempotency relation.

Recovery SHALL NOT regenerate a materially different offer from post-restart
ambient state.

---

## 6.5 Accepted context / invocation / dependency evidence

Invocation facts, accepted catalog context, committed typed prior exports,
dependency/revision refs and receipt refs remain with native execution owners as
long as they are required to preserve retry/recompute semantics.

Open execution is interpreted using accepted stored context first, not silently
rebound under later ambient rules/state.

---

# 7. Temporal source continuity

## 7.1 Native authority

Temporal obligation state remains on native owners, including as applicable:

- Effect intrinsic TemporalBinding;
- Effect scheduled-trigger state;
- Resource delayed recovery binding/state;
- LifeState temporal recovery state;
- Procedure-bound temporal state;
- later admitted owner-local temporal mechanisms.

---

## 7.2 Armed due-capable source discovery

An otherwise-unreachable native owner carrying an armed temporal obligation that
can become mechanically due independently of ordinary direct retrieval must be
boundedly discoverable through typed source-owner routing/index evidence.

Redundant enrollment is not required if another guaranteed bounded root already
reaches the owner.

Recovery routing is reference-only for correctness. It SHALL NOT require or
trust duplicated:

- deadline;
- next-due coordinate;
- priority/order;
- due/not-due result;
- selected trigger;
- firing generation;
- chronology comparison result.

Any later duplicated values for search performance are disposable projections and
must be rebuildable/validatable against native owner state.

---

## 7.3 Temporal Agenda rebuild

Cold recovery reconstructs Temporal Agenda from:

1. boundedly discovered armed due-capable native owners;
2. their native TemporalBindings/current state;
3. applicable Procedure/chronology/context evidence.

Agenda ordering/cache state is disposable.

Once a due candidate crosses the selected/committed execution boundary, its
stable firing/pending-child/Resolution identity becomes Step-3 execution
continuity and recovery must not select it again from Agenda.

Step 5.3 owns exact transition/no-lost/no-double semantics.

---

# 8. Identity and promotion closure

`runtime.id_allocator` remains the authoritative campaign allocator singleton.

Rules:

1. published campaign-scoped IDs remain immutable/nonreused;
2. durable allocation state must remain recoverable as required by that contract;
3. volatile session-local reservations may disappear when no promised durable
   owner depends on them;
4. a promised recoverable owner cannot contain a required reference to a
   session-local identity that disappears on cold restart;
5. such dependencies must be promoted/rekeyed/materialized coherently before the
   recovery source set is acknowledged;
6. live-epoch provisional identities may remain valid within the authoritative
   durable live-epoch lifetime but cannot escape that scope before promotion or
   compaction.

This is a recovery consequence of existing publication/promotion closure, not a
new allocator authority.

---

# 9. Live / multiplayer composition

The existing scene -> live-epoch pointer pattern is preserved.

Rules:

1. durable scene routing discovers active live epoch state;
2. live-owned mutable truth stays live-owned until compaction/absorption;
3. active runtime roots whose native scope is live-owned must be discoverable
   through the live scope’s bounded routing chain/partition;
4. campaign recovery does not copy live current state into campaign merely to
   create one snapshot;
5. independent live epochs remain independent native sources;
6. no global enrollment mutation is required for every independent live/local
   root change;
7. missing/incompatible pointed live state blocks/suspects the scope instead of
   silently falling back to campaign base;
8. closed-but-unabsorbed live epoch is a recoverable operational condition but is
   not normal writable gameplay state;
9. Step 5.8 owns exact root movement/adoption across freeze/compaction/rollover.

---

# 10. Recovery-routing implementation contract

Step 5.2 defines logical requirements, not one wire format.

Any later physical representation must satisfy all of:

## 10.1 Typed membership

Membership identifies enough semantic kind/scope/reference to load and validate
the native owner without interpreting arbitrary prose.

## 10.2 Reference-only authority boundary

Required routing stores references/path membership, not copies of native owner
payload.

## 10.3 Sparse active membership

Active recovery routing scales with currently recovery-relevant roots/source
owners, not all historical records.

Terminal/history retention is independent.

## 10.4 Lifecycle-derived enrollment

Native activation/terminality transitions determine whether independent routing
membership is required. Routing does not infer lifecycle from its own presence.

## 10.5 Coherent durability

Acknowledged durable owner state and required enrollment cannot expose dangling
or omitted active roots under normal operation.

## 10.6 Partitionability

Representation admits native writable-scope partitioning and does not impose one
global hot contention point.

## 10.7 Boundedness

Normal cold-start enumeration cost scales with active recovery scope rather than
campaign age.

## 10.8 Testability

Implementation must test owner activation/terminality enrollment obligations and
publication completeness for every admitted independently rootable kind.

Exceptional maintenance/integrity audit may perform broader enumeration to find
orphan-active or stale-root drift; normal recovery does not.

---

# 11. Checkpoint relationship

Checkpoint remains an immutable sparse recovery descriptor/evidence object.

It may later capture or reference the then-current recovery-routing/source
selection for historical/checkpoint recovery, but it SHALL NOT become:

- current-state authority;
- sole source of current active root membership;
- mandatory hot record updated on every operational owner transition.

A current campaign state newer than the latest checkpoint is not silently rolled
back merely because the checkpoint is older.

Step 5.7 owns checkpoint source selection, historical recovery validation,
hydration and physical routing representation.

---

# 12. Semantic resume outside mechanics

Cold recovery does not require exact prose continuity as universal state.

Canonical cases:

```text
settled current scene / open player handoff
    -> reload semantic current state and regenerate equivalent presentation

pending mechanical Choice/Reaction
    -> Continuation owns the fixed response contract

pending materially accepted clarification before Command
    -> Interaction/IntentPlan carries sufficient semantic state when promised

same-context maintenance switch
    -> ephemeral maintenance continuation frame may assist, but does not replace
       durable native owners for cold recovery
```

If an accepted material meaning cannot be reconstructed from admitted semantic
owners and only survives in raw conversation, the durability materialization is
incomplete; transcript does not silently become universal gameplay authority.

---

# 13. Recovery integrity semantics

## 13.1 Expected loss of volatile-ahead-of-durable state

Not canon corruption by itself. Resume the last actual durable source set.

## 13.2 Missing derived projection

Rebuild silently from surviving native owners/evidence.

## 13.3 Stale coordination/session routing

Refresh/rebind through domain-native current routing.

## 13.4 Malformed required recovery routing

Block normal recovery for the affected scope and enter targeted
integrity/recovery validation.

## 13.5 Required root/target missing or incompatible

Treat the affected recovery scope as blocked / `CANON_SUSPECT`; validate/repair
with evidence. Never guess, drop work or blindly replay committed mechanics.

## 13.6 Stale root lists terminal owner

Native terminal owner wins. Repair stale routing; do not replay the owner.

## 13.7 Active owner omitted from required routing

Publication/root-membership completeness defect. Prevent through lifecycle tests
and durability completeness validation; exceptional maintenance audit may detect
historical drift through broader structural checks.

---

# 14. Host delivery boundary carry-forward

Step 5.2 recovers canonical/operational state but does not define whether a
generated player-facing response was emitted or durably acknowledged.

A process can fail after mechanics commit but before delivery state is known.

Until Step 5.12 defines this layer:

- committed mechanics are never rolled back/replayed solely to reproduce
  narration;
- transcript text never becomes mechanical authority;
- if emitted/acknowledged delivery state affects what may safely be re-emitted or
  what a human player is known to have received, Step 5.12 must represent that
  state through admitted owner/evidence and make it recoverable where required;
- `delivery state unknown` is a host-layer recovery condition, not permission to
  invent whether the player saw an output.

---

# 15. Explicit later-slice ownership

## Step 5.3 — Temporal & Pending-Obligation Continuity

Owns:

- exact armed temporal-owner enumeration/rebuild mechanics;
- due selection/materialization transition;
- no-lost/no-double firing;
- pending temporal child lifecycle;
- exact fixed/reserved RNG continuation behavior.

Must preserve owner-local TemporalBindings and this Step-5.2 routing boundary.

## Step 5.4 — Host Lifecycle & Session Handoff

Owns:

- controlled restart/new chat/context expiration;
- when volatile current closure must become durable before intentional context
  destruction;
- degraded handoff when exact current-chat evidence cannot survive.

## Step 5.5 — SOFT / HARD / SAVE Semantics

Owns when a recovery source set is promised and therefore when native owners and
required routing/dependencies must be materialized.

## Step 5.6 — Publication & Crash Consistency

Owns crash-consistent/idempotent publication of owner changes + root enrollment +
dependency promotion.

## Step 5.7 — Checkpoint / Recovery Protocol

Owns physical root/index/checkpoint representation, hydration order, exact source
pinning/validation, repair behavior and historical checkpoint recovery.

## Step 5.8 — Multiplayer / Live Ownership

Owns campaign/live root partition placement and movement across epoch lifecycle.

## Step 5.9 — Chronology Persistence

Owns chronology evidence required to interpret recovered temporal owners without
using Git/recovery ordering as fiction.

## Step 5.12 — Host Delivery / Disclosure Boundary

Owns generated/emitted/durably-acknowledged player delivery recovery semantics.

## Step 5.13 — GC / Orphan Cleanup

Owns retention/deletion of terminal runtime owners, receipts, routing projections
and direct idempotency evidence after active membership ends.

---

# 16. Implementation debt exposed by Step 5.2

These are later realization obligations, not open Step-5.2 architecture
decisions:

1. shipped GAME storage/schema placement for accepted Step-3 runtime owners;
2. bounded active Command/Procedure/pending-Interaction recovery routing;
3. bounded armed due-capable temporal-owner routing sufficient for Agenda rebuild;
4. deterministic Procedure active/terminal machine evidence;
5. complete Interaction/message machine realization for material pending input;
6. SAVE/session completeness alignment with active operational owners;
7. fixed RNG runtime prose/machine alignment with Step-3 owner semantics;
8. checkpoint `valid_through_event_id`/legacy event-frontier cleanup in 5.7;
9. maintenance diagnostics able to validate/export current recovery roots after
   machine realization;
10. runtime/package/catalog interpretability validation during cold hydration.

No implementation is authorized by this list before the remaining architecture
sequence and approved implementation planning.

---

# 17. Canonical recovery examples

## A — Clean durable scene, no in-flight execution

Recover campaign/current scene/world roots and armed temporal source owners as
applicable; rebuild caches/Agenda; hand control back to player.

No runtime execution root is manufactured.

## B — Suspended attack awaiting reaction

Bounded routing finds non-settled Command; Command reaches Resolution;
Resolution reaches current Continuation and Procedure. Recover fixed RNG, pending
reaction offer, accepted context and receipts from owners. Rebuild MechanicalContext
and continue from safe recompute semantics. Do not reroll.

## C — Active combat Procedure between player Commands

No Command need be open. Active Procedure remains independently rooted and its
spent ResourceState survives. Fresh runtime restores Procedure context before the
next participating Command.

## D — Damage Event committed, mandatory follow-up not yet executed

Root Command/pending child descriptor survive. Recovery starts from already
committed damage state and executes/resumes the child once. It does not rescan
current bindings to rediscover whether the historical firing existed.

## E — Off-screen scheduled Effect, Agenda lost

Temporal-source routing finds Effect. Load owner TemporalBinding and applicable
chronology context, rebuild Agenda. No durable Agenda authority required.

## F — Two independent live epochs

Pin campaign source and each routed live source to exact native revisions.
Recover each live-owned scope through its own routing partition. Do not order the
two live revisions globally.

## G — Pointed live branch missing

Do not use stale campaign base as fallback. Mark/block affected recovery scope and
enter targeted integrity/repair.

## H — Player declaration awaiting target clarification

If no durability/handoff policy promised the pending declaration, it may be lost
with volatile context under current RPO. If the point was promised durable,
bounded routing restores Interaction/IntentPlan semantic state sufficiently to
ask the same material clarification without inventing a different intent.

## I — Checkpoint older than current campaign state

Current cold recovery does not silently roll back to checkpoint. Checkpoint
remains historical/selectable recovery evidence under later 5.7 rules.

## J — Runtime package missing for suspended old catalog context

Owner records remain present but execution interpretation is unavailable. Recovery
is blocked pending compatible package resolution or explicit authorized migration;
do not resume under arbitrary ambient rules.

---

# 18. Step-5.2 closure verdict

```text
Resumable Runtime Closure concept      CANONICAL PROPERTY
new semantic recovery owner            NO
new first-class closure record         NO
bounded typed recovery routing         REQUIRED
routing globally hot singleton         FORBIDDEN AS REQUIREMENT
routing partitionable                  REQUIRED
Procedure independent recovery root    REQUIRED WHILE ACTIVE
Temporal Agenda serialization          FORBIDDEN AS AUTHORITY
armed temporal source discovery        REQUIRED WHEN OTHERWISE UNREACHABLE
fixed accepted execution inputs        PRESERVE IN NATIVE OWNERS
lost unpublished HOT reconstruction    FORBIDDEN
mixed native revision hydration        FORBIDDEN
stale wrong-scope fallback              FORBIDDEN
compatible interpretation context      REQUIRED
checkpoint sole current root source     FORBIDDEN
exact physical representation          DEFERRED TO 5.7/5.8
blocking human decision                NONE
```

**Step 5.2 / Resumable Runtime Closure is CLOSED.**

The next numbered slice is **Step 5.3 / Temporal & Pending-Obligation
Continuity**. Step 5.3 must preserve this specification and must not begin until
Step-5.2 closure/status verification is complete.
