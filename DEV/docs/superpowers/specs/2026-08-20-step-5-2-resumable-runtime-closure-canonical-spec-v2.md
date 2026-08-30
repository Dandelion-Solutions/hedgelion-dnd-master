# Step 5.2 — Resumable Runtime Closure — Canonical Specification v2

Status: **CANONICAL ARCHITECTURE — STEP 5.2 CLOSED**

Date: 2026-08-20

Supersedes for current Step-5.2 authority:

- `2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec.md`

The superseded file remains historical derivation. This v2 incorporates the post-canonical adversarial and resolution addenda without changing the accepted native-owner model.

Derivation chain:

- `2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-task-brief.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-research-draft.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-analytical-challenge.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-decision-brief.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-candidate-spec.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review-addendum.md`
- `../design/2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate-addendum.md`

Prerequisites:

- Steps 1–2 temporal/resource/effect/recovery ownership;
- Step 3 deterministic execution ownership;
- Step 4 truth/knowledge/disclosure/Story ownership;
- Step 5.0 contamination cleanup;
- Step 5.1 B-NARROW frontier model.

This specification defines Step-5.2 logical architecture only. It does not select repository paths, checkpoint wire format, due-work state machine, durability cadence, campaign publication algorithm, live CAS/compaction protocol, chronology representation, Story/transcript retention, delivery acknowledgement or GC policy.

---

# 1. Canonical definition

**Resumable Runtime Closure** is a correctness property over a compatible set of domain-native durable sources: every gameplay-significant current owner, unresolved execution dependency and pending obligation required to continue from the promised durable point must be recoverable through bounded typed native routing and transitive required-dependency closure, while non-authoritative derived state is rebuilt.

It is not:

- a semantic state owner;
- a mandatory first-class runtime record;
- a universal HOT snapshot;
- a generic pending-work table;
- a serialized Temporal Agenda;
- a common frontier/comparison algebra;
- a scalar `RecoveryCut` identity;
- transcript/model memory;
- a merged campaign/live writable authority.

A fresh runtime with no prior chat/model/process memory must be able to resume the last **actually promised durable** gameplay point from surviving native sources. Volatile state legitimately ahead of that point may be lost; recovery never invents it.

---

# 2. Canonical laws

## LAW 5.2-1 — NATIVE OWNER PRESERVATION

Recovery metadata, checkpoints and routing projections SHALL NOT replace or duplicate current writable authority.

Examples:

```text
Procedure ResourceState       -> runtime.procedure
Resolution execution state    -> runtime.resolution
suspended response state      -> runtime.continuation
mandatory child closure       -> runtime.command / committed execution evidence
Effect temporal state         -> world.effect
world HP/location/ownership   -> normal world owners
live-owned mutable truth      -> active live epoch
campaign allocation state     -> runtime.id_allocator
```

## LAW 5.2-2 — BOUNDED OPERATIONAL ROOT DISCOVERY

Every independently recovery-relevant active native owner that is not guaranteed boundedly reachable from another admitted operational root SHALL be discoverable through typed bounded routing.

Normal cold recovery SHALL NOT require campaign-wide file scans, historical-runtime scans, broad Git-history scans, full WORLD traversal or semantic reconstruction from Story/transcript prose.

Exceptional integrity repair may use broader evidence only after the bounded path is suspect.

## LAW 5.2-3 — ROUTING IS RECOVERY EVIDENCE, NOT SEMANTIC AUTHORITY

Routing answers only which typed native owner/reference to load and validate. It does not own owner lifecycle/current values, Procedure resources, pending-child payload, HP/resources/effects, temporal deadlines/due results/order, chronology, RNG results, Choice/Reaction options or live overlays.

Native owner semantics win after the owner is loaded. Missing/incompatible required targets block or suspect recovery; omitted active owners are routing-completeness defects, not semantic termination.

## LAW 5.2-4 — PARTITIONABLE RECOVERY ROUTING

Recovery routing SHALL be partitionable by existing semantic/writable scope. No invariant requires one campaign-global hot singleton, generation, digest, count or root registry for all independent scenes/sessions/live/runtime owners.

Physical representation may later use active-only paths, typed indexes, per-scene/per-Procedure partitions, cold global partitions, live-local partitions or combinations thereof.

## LAW 5.2-5 — TRANSITIVE REQUIRED-DEPENDENCY CLOSURE

A promised durable recovery source set is valid only when every semantically required recovery dependency of every recoverable owner is:

1. durable/recoverable in its native domain;
2. explicitly optional; or
3. deterministically rebuildable from surviving owners/evidence.

This law does not recursively materialize arbitrary world-graph references. Only dependencies whose absence can change correct resume semantics are in closure.

## LAW 5.2-6 — DERIVED STATE REBUILDS

Derived state SHALL NOT become recovery authority merely to avoid recomputation.

At minimum this includes Temporal Agenda, MechanicalContext, Condition/Effect aggregation/reverse indexes, dependency DAG caches, loaded-record caches, derived mechanics, Context Assembler working bundles, repository query caches and Story editorial/render buffers.

Missing derived state is rebuild work, not canon corruption.

## LAW 5.2-7 — NO INVENTED LOST HOT STATE

If total process/chat/context loss destroys HOT/SOFT state before an applicable protocol successfully makes that point durable, recovery returns to the last actual durable source set. It SHALL NOT fabricate lost deltas, infer player choices, pretend publication occurred or replay old mechanics solely to synthesize the lost newer state.

## LAW 5.2-8 — DOMAIN-NATIVE RECOVERY SOURCES

One recovery operation may compose several compatible native durable sources, e.g. campaign commit C plus independent live epoch heads LA/LB plus campaign/live-local runtime routing partitions.

Participation does not create scalar comparability, total ordering, shared revision numbers, fictional chronology order or merged writable authority.

## LAW 5.2-9 — PINNED NATIVE HYDRATION

One hydration attempt SHALL resolve each participating mutable native source to an exact revision before consuming dependent state from that source. Reads stay pinned for that attempt.

If compatibility/refresh changes the selected source revisions, the affected selection is invalidated/reselected rather than mixing branch-relative revisions.

## LAW 5.2-10 — OWNING-SCOPE RESOLUTION

Required identities/states SHALL resolve through the native ownership/routing contract applicable to that identity/scope at the selected source set.

An older durable representation in another domain is not fallback authority. If live routing says the active live epoch owns mutable truth, missing/incompatible live state blocks/suspects that scope rather than silently falling back to campaign base.

## LAW 5.2-11 — ROOT MEMBERSHIP COHERENCE

When a native lifecycle transition creates, changes or removes independent recovery-root eligibility, the required routing-membership mutation is a derivative of that native transition and SHALL join the same promised durability closure strongly enough to prevent:

- durable active owner + missing required enrollment;
- durable routing root + missing required owner;
- premature root removal that strands unfinished work.

Routing reflects lifecycle; it does not define lifecycle.

## LAW 5.2-12 — INTERPRETABILITY CLOSURE

A promised recoverable operational owner is resumable only when the compatible runtime/catalog/rules interpretation context accepted by that execution is resolvable through the campaign engine/package compatibility contract.

A fresh runtime SHALL NOT silently reinterpret open execution under arbitrary newer ambient mechanics. Missing compatible interpretation context is a recovery prerequisite failure or requires explicit compatible migration/adoption.

## LAW 5.2-13 — ARMED TEMPORAL ENROLLMENT

Every armed native temporal source owner whose admitted obligation can become mechanically due independently of ordinary direct owner loading SHALL remain enrolled in bounded typed temporal-source routing for its entire armed lifetime, even when that owner is also transitively reachable through another active recovery root.

This law deliberately rejects a reachability-based enrollment optimization.

Enrollment applies only when:

1. an admitted temporal obligation is armed;
2. it can become mechanically due without another gameplay reason first loading the owner; and
3. losing that due processing would change gameplay-significant state/continuity.

It does **not** require routing every record with temporal metadata. Procedure-local/non-independent temporal state need not be separately enrolled unless Step 5.3 establishes that it can fire independently.

Temporal routing duplicates only owner identity/retrieval evidence. It SHALL NOT own deadline, next-due, due/not-due, priority, selected trigger, firing generation, chronology relation or owner lifecycle.

---

# 3. Recovery-state classification

Every relevant value fits one of:

```text
AUTHORITATIVE STATE
IRREDUCIBLE RECOVERY EVIDENCE / ROUTING
REBUILDABLE DERIVED STATE
TRULY EPHEMERAL STATE
VOLATILE CURRENT STATE AHEAD OF DURABLE SOURCE SET
DEFECT / UNOWNED REQUIRED STATE
```

A value is not made durable merely because recomputation is inconvenient. A value is not ephemeral if losing it can change a gameplay point explicitly promised recoverable.

---

# 4. Native execution owners

## 4.1 RuntimeCommand

A non-settled RuntimeCommand is independently recovery-relevant while unfinished mandatory descendant closure remains. Its accepted request identity/fingerprint, catalog context, invocation facts, root execution linkage, disposition, pending mandatory children and receipt evidence remain native.

Settled Commands may remain directly addressable for idempotent retry/audit without belonging to active cold-start enumeration.

## 4.2 Procedure

Procedure remains sole owner of procedure-local ResourceState and has an independent lifetime across Commands/Resolutions/reactions/suspensions/retries.

Logical lifecycle:

```text
ACTIVE
    from accepted Procedure opening
    across gaps between participating Commands/Resolutions

TERMINAL
    only after explicit typed Procedure closing/reset/terminal semantics commit
```

Absence of an open Command and Encounter/Scene status alone do not terminate Procedure. Recovery routing cannot be the sole lifecycle evidence. Later machine realization must expose deterministic Procedure-native lifecycle evidence sufficient to validate membership.

## 4.3 Resolution

Active/suspended/blocked Resolution remains native operational state. When boundedly reachable from an admitted root, it need not be separately rooted.

Its required continuity may include causal/root command identity, Activity/catalog binding, Procedure ref, status/cursor/safe recompute phase, fixed RNG, invocation facts/prior exports, child refs, Continuation ref and committed receipt evidence.

## 4.4 Continuation

Continuation remains one portable suspended Resolution generation. It preserves accepted irreducible suspension payload and SHALL NOT copy Procedure ResourceState, MechanicalContext, Temporal Agenda, Condition indexes, DAG caches or trusted prospective deltas.

When durably referenced by a reachable Resolution, it need not be separately rooted.

## 4.5 Pending Interaction / IntentPlan

A materially unresolved accepted player input before Command creation is conditionally recovery-relevant only when the applicable durability/handoff protocol promises that semantic point across cold restart.

Existing Interaction/IntentPlan/message evidence owns sufficient accepted semantic input. Generic open handoff prose, optional suggestions and unaccepted narration are not new recovery owners.

If exact wording is temporarily the only evidence preserving accepted meaning, that specific evidence is irreducible until sufficient typed semantic state is materialized; the complete transcript does not become universal authority.

---

# 5. Current root classes and admission

Current independently rootable operational classes are:

```text
A. non-settled RuntimeCommand
   when unfinished descendant closure remains

B. active Procedure
   independently of Command lifetime

C. materially unresolved accepted Interaction/IntentPlan
   only when durability/handoff policy promises that point
```

Temporal-source routing is governed separately and unconditionally by LAW 5.2-13 for the armed independently-due lifetime.

Known singleton:

```text
runtime.id_allocator = campaign-allocator
```

It needs no active-membership discovery because its identity is deterministic.

Common descendants such as Resolution, Continuation, child Resolution, pending-child evidence and receipts need not be redundantly rooted when durable forward references provide bounded traversal.

Future admission rule:

> Any later native operational owner with independently active recoverable lifetime that is not guaranteed boundedly reachable from another admitted operational root must receive typed recovery routing through normal architecture/catalog evolution.

No untyped `pending[]`, `jobs[]` or generic work registry is admitted.

Duplicate **references** to one owner are allowed when they simplify bounded correctness (notably temporal routing). Duplicate owner payload/current-state authority is forbidden.

---

# 6. Irreducible execution continuity

## Mandatory child identity

Once committed execution creates mandatory descendant work, stable pending-child/firing identity is irreducible until materialized/settled. Recovery SHALL NOT replace missing selected historical work by rescanning current trigger bindings.

## Fixed RNG

Already generated/accepted RNG whose dependent execution remains unfinished must survive with Resolution/Continuation/committed continuity evidence. Cold recovery SHALL NOT reroll it because the process restarted. ResolutionTrace is not its sole owner.

## Future RNG

Only future RNG identity/state already semantically committed/reserved must survive. Step 5.2 does not require one global deterministic future RNG stream. Step 5.3 must reconcile this with the current `Continuation.future_rng_frontier` machine field.

## Pending Choice / Reaction

A durable Continuation with a fixed Choice/Reaction preserves Continuation generation, offer identity, responder, bounded candidates/options and single-consume/idempotency semantics. Recovery does not regenerate a materially different offer from ambient state.

## Accepted interpretation/dependency evidence

Catalog-context identity, invocation facts, prior committed exports, dependency revision refs and committed receipt refs remain recoverable while required to preserve safe recompute/retry meaning.

---

# 7. Temporal continuity source contract

Temporal authority remains owner-local: Effect TemporalBindings/scheduled-trigger state, Resource/LifeState delayed recovery state, Procedure-bound temporal state and any later admitted owner-local temporal mechanism.

Cold recovery:

1. enumerates all LAW-5.2-13 temporal-source memberships;
2. loads each native owner from its pinned owning scope;
3. loads required Procedure/chronology/context evidence;
4. rebuilds Temporal Agenda/due projection;
5. if due work already crossed the committed materialization boundary, resumes from Step-3 firing/pending-child/Resolution identity instead of selecting it again from Agenda.

Agenda ordering/cache state is disposable. Step 5.3 owns due selection, no-lost/no-double processing and exact transition from temporal obligation to committed execution.

---

# 8. Live-scope composition

Campaign scene routing may point to an active live epoch. While live owns that scope:

- live mutable truth remains live-owned;
- campaign representation is base/reference, not fallback current truth;
- participating live reads are pinned to one exact live revision for the hydration attempt;
- live-local runtime routing may remain partitioned from campaign routing;
- independent live epochs remain incomparable absent explicit relation;
- missing pointed live state blocks/suspects recovery;
- closed-unabsorbed live state is a recoverable operational condition, not ordinary writable gameplay state.

Step 5.8 owns exact root movement/adoption/compaction/rollover.

---

# 9. Identity/promotion closure

A promised recoverable owner cannot require identity/state with a shorter lifetime than the recovery promise.

Therefore:

- session-local identities must be promoted/rekeyed/materialized before durable recoverable owners depend on them across cold restart;
- published campaign IDs remain immutable and allocator-owned;
- live provisional IDs may remain valid within the durable authoritative live-epoch lifetime until promotion/compaction;
- no durable root may require RAM-only owner state.

---

# 10. Checkpoint relation

Checkpoint remains sparse immutable recovery descriptor/evidence, not current state authority or the sole current active-root source.

An older latest checkpoint does not by itself force rollback. Conversely, campaign HEAD alone is not proof of a complete recovery source set when live/operational domains participate.

Step 5.7 owns selection of the most current compatible valid durable source set, historical checkpoint source references, hydration order and repair outcomes. Step 5.2 introduces no universal `RecoveryCut` record.

---

# 11. Story / transcript / host-delivery relation

Gameplay recovery does not require Story catch-up or universal exact transcript retention when native semantic owners are sufficient. If correctness-relevant meaning exists only in Story/transcript because it was never materialized into its proper owner, that is a materialization defect.

Host delivery is separate: a crash may occur after mechanics/disclosure state commits but before it is known whether output reached the player. Step 5.2 does not infer that state. Step 5.12 must own generated/emitted/acknowledged delivery semantics where recoverability matters.

Committed mechanics are never rolled back or replayed merely to reproduce narration.

---

# 12. Integrity outcomes

```text
missing derived cache
    -> rebuild

stale session/coordination pointer
    -> refresh/rebind through native routing

malformed required routing
    -> scoped recovery/integrity mode

required root/target missing or incompatible
    -> recovery blocked / CANON_SUSPECT
    -> targeted validation/repair

stale routing lists terminal owner
    -> native terminal owner wins; repair routing; do not replay

active owner omitted from mandatory routing
    -> publication/root-enrollment completeness defect
```

Because omission can be invisible during ordinary cold recovery, activation/terminality and publication validation must assert root-enrollment obligations. Maintenance repair may use broader structural enumeration; normal recovery remains bounded.

---

# 13. Boundary consequence

Step 5.2 defines completeness, not when durability is required.

Whenever later policy promises a gameplay point durable, that promise cannot be acknowledged while required closure state remains only volatile, including as applicable:

- active Procedure state;
- current Continuation/fixed response state;
- mandatory child identity;
- armed independently-due temporal owner and required temporal routing;
- promoted identity dependency;
- required compatible interpretation context.

5.4/5.5 determine when that promise is required; 5.6–5.8 determine how it is made crash-consistent and recovered.

---

# 14. Acceptance scenarios

The architecture must support without violating the laws above:

1. clean cold restart with no in-flight execution;
2. loss of unpublished SOFT state without invention;
3. suspended reaction with fixed RNG/offer/Procedure;
4. active Procedure between Commands;
5. post-commit mandatory child without loss/double execution;
6. complete loss/rebuild of Temporal Agenda;
7. off-screen armed independently-due timer discovered without WORLD scan;
8. armed temporal owner remaining discoverable after an unrelated active root terminates;
9. two independent live epochs with no global root hotspot or inferred order;
10. pending accepted clarification resumed semantically without universal transcript authority;
11. stale Session metadata unable to override campaign/live authority;
12. checkpoint behind newer valid durable source composition;
13. missing root target causing typed recovery failure rather than dropped work;
14. rejection of durable closure that depends on vanished local identity;
15. Story lag not blocking gameplay recovery;
16. missing compatible runtime/catalog interpretation context blocking unsafe resume;
17. hydration pinning campaign/live sources rather than mixing revisions;
18. live-owned identity refusing stale campaign fallback.

---

# 15. Explicit later-slice obligations

## Step 5.3 — Temporal & Pending-Obligation Continuity

Must define Agenda rebuild algorithm, due-selection/materialization boundary, no-lost/no-double firing, selected-firing identity, fixed/reserved RNG continuity and reconciliation of `future_rng_frontier`. Must preserve LAW 5.2-13 and must not make Agenda authority.

## Step 5.4 — Host Lifecycle & Session Handoff

Must decide when controlled context/process destruction forces current required closure durable before handoff, and separate cold-recovery semantics from same-context maintenance convenience.

## Step 5.5 — SOFT / HARD / SAVE

Must define when the system promises a point durable. Any such acknowledgement covers the whole required closure.

## Step 5.6 — Campaign Publication & Crash Consistency

Must make native owner state, required root membership and dependency promotion coherent across publication/crash/retry windows.

## Step 5.7 — Checkpoint / Recovery Protocol

Must select physical recovery-routing/checkpoint representation, source pinning, compatible source-set selection, hydration order, validation and repair behavior.

## Step 5.8 — Multiplayer / Live-Epoch Ownership

Must decide live-local routing placement and transfer/compaction behavior without introducing a global hot enrollment barrier.

## Step 5.9 — Chronology

Must provide chronology/context evidence needed to interpret recovered temporal bindings without deriving fiction from Git/root order.

## Steps 5.10–5.13

Story, transcript, host delivery and GC remain separate from canonical operational authority unless explicit dependencies require recoverable evidence. GC cannot remove active-root, idempotency, chronology or projection dependencies prematurely.

---

# 16. Machine/debt ledger

Step 5.2 closes semantics but does not claim implementation of:

1. physical repository placement for Step-3 runtime owners;
2. active operational-root routing representation;
3. temporal-source routing representation;
4. Procedure lifecycle/status machine realization;
5. durable pending Interaction/IntentPlan semantic payload where applicable;
6. GAME schemas for Step-3 runtime owners;
7. SAVE_CONTRACT operational-owner alignment;
8. RANDOMNESS/MECHANICS_INTEGRITY wording alignment with fixed RNG ownership;
9. checkpoint source-set/hydration representation;
10. live runtime-root placement/compaction handoff;
11. exact recovery failure/status vocabulary;
12. terminal runtime/routing retention and GC;
13. exact future-RNG representation.

These are explicitly owned by later slices/integrated implementation; none is an unresolved Step-5.2 state-owner decision.

---

# 17. Final architecture disposition

```text
Resumable Runtime Closure             = correctness property
new semantic recovery authority       = NO
new first-class closure record        = NO
bounded typed operational routing     = YES
partitionable routing                 = YES
pinned native hydration               = YES
owning-scope recovery                 = YES
root membership coherence             = YES
interpretability closure              = YES
active Procedure independent rooting  = YES
Temporal Agenda persistence authority = NO
armed independently-due enrollment    = ALWAYS WHILE ARMED
fixed accepted RNG survives           = YES
future global deterministic RNG       = NOT REQUIRED
checkpoint as current authority       = NO
Story/transcript as universal owner   = NO
human architecture decision required  = NO
```

**Step 5.2 is CLOSED.**

Next slice: **Step 5.3 — Temporal & Pending-Obligation Continuity**, not started by this specification.