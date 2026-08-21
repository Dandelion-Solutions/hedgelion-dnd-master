# Step 5.1 — Frontier Model — Decision Brief

Status: **HUMAN ARCHITECT DECISION REQUIRED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- `2026-08-20-step-5-1-frontier-model-task-brief.md`
- `2026-08-20-step-5-1-frontier-model-research-draft.md`
- `2026-08-20-step-5-1-frontier-model-analytical-challenge.md`
- owner feedback after the first Decision Brief;
- current `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` identifier/allocation contract.

No candidate/canonical Step-5.1 specification should be produced until this decision is made.

---

# 1. What are we deciding?

Whether HDM should adopt a small cross-domain semantic discipline for frontier/progress concepts, or keep every subsystem entirely domain-local.

The decision is **not** whether to introduce a generic Frontier runtime object. Research rejects that.

The material choice is:

### Option A — Domain-local only

Every subsystem defines its own revision/cursor/frontier/coverage semantics. No shared cross-domain rules beyond ordinary prose.

### Option B-NARROW — Shared semantic invariants, domain-native representations **(recommended)**

Adopt only two hard cross-cutting laws plus a small vocabulary:

```text
LAW 1 — DOMAIN TYPING
Every frontier/progress claim must identify the semantic domain/scope in which
it is meaningful.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
No ordering/comparison is valid between different domains unless a specific
contract explicitly defines that relation.
```

Keep all actual values and comparison rules domain-specific. Introduce no generic Frontier record/schema/API/registry.

Use `coherent source cut` only as a conceptual term for a scope-indexed set of compatible pinned source markers used by one read/recovery operation. It has no independent ID or storage contract in 5.1.

### Option C — Unified first-class Frontier model

Generic typed Frontier values/comparison/composition framework.

Research recommends rejecting C as unsupported overengineering.

---

# 2. Why must this be decided now?

Steps 5.2–5.13 must talk about:

- campaign durable publication;
- HOT state ahead of publication;
- active live-scene authority;
- recovery/checkpoint composition;
- chronology partial order;
- Story source coverage;
- stale sessions versus lagging projections;
- retention/GC safety.

If Step 5.1 leaves the relationship rules ambiguous, later slices can independently invent incompatible meanings for `frontier`, compare unrelated IDs, or accidentally create new current-state authority.

If Step 5.1 over-generalizes, later slices become constrained by a framework that current requirements do not need.

---

# 3. Verified findings that do not require a decision

These follow mechanically from current accepted architecture.

## 3.1 Not everything called a frontier is a frontier

```text
HOT state          = working view over durable base + accepted delta
Dirty set          = unpublished delta/closure
SOFT/HARD          = durability classification/requirement
Checkpoint ID      = pointer
Checkpoint         = recovery descriptor/evidence
Session HEAD       = observation/coordination evidence
Resolution.cursor  = execution cursor
Temporal Agenda    = derived index
ID allocator state = identity-allocation authority/bookkeeping, not progress
```

## 3.2 Campaign Git revision is scoped durability evidence

A commit becomes current durable campaign publication only when reachable through the authoritative campaign ref. An unreachable prepared commit is not campaign canon.

This does not mean campaign SHA alone describes all current state while active live authority exists.

## 3.3 Active live authority is scope-local

For a live-owned scene, current mutable truth is inherited campaign base + authoritative live state. Campaign routing activates that authority. Different live epochs have incomparable revision domains.

## 3.4 Chronology is a separate partial-order domain

Git order, SemanticEvent ID allocation order and fictional chronology are distinct.

## 3.5 Story coverage is a projection concern

Story can be durably behind canonical source and remain correct. Source coverage and literary/editorial revision are different concepts.

## 3.6 Campaign-scoped ID allocation already has a separate central owner

The current catalog contract already defines `runtime.id_allocator` / `campaign-allocator` as the owner of persistent campaign-scoped numeric allocation state.

Current accepted semantics include:

```text
one campaign-allocator singleton
    -> last_allocated by identity policy
    -> next is derived

allocation + record creation
    -> one atomic HOT operation

canonical allocation change
    -> allocator change joins the same durable publication closure

multiplayer stale-publication conflict
    -> reload current allocator
    -> rekey only conflicting unpublished records
    -> rebuild publication batch

published IDs
    -> never changed
    -> never reused
```

This is the mechanism relevant to centralized counters for scenes, actors, assets, semantic/mechanical events and other campaign-scoped sequential record kinds.

It is **not** a frontier/coverage mechanism. The exact Git publication failure/retry details remain Step 5.6 work, while live-epoch provisional identity and Story layer-local allocation remain in their owning later slices.

## 3.7 `CURRENT.last_event_id` does not solve reconnect or allocator concurrency globally

The field may have originated as a convenient fast-resume/event cursor, and that intent is understandable. Current architecture now has more precise mechanisms for the problems it would otherwise blur together:

- campaign reconnect/resync pins/probes campaign HEAD and, when changed, compares changed paths before fetching affected records;
- active shared-scene reconnect/synchronization uses the live epoch/head/state protocol;
- campaign-scoped ID collision handling belongs to `campaign-allocator` plus optimistic publication/rekey semantics;
- fictional chronology belongs to causal/order evidence, not event-ID order;
- exact cold recovery may require checkpoint + typed operational roots, not one semantic-event scalar.

A sequential SemanticEvent ID remains useful as record identity and may be referenced as provenance. But a single `CURRENT.last_event_id` cannot prove a complete coherent current/recovery state across campaign, live, runtime and chronology domains, and it duplicates no indispensable reconnect function once the scoped revision mechanisms above are used.

Recommendation independent of Option A/B: **retire `CURRENT.last_event_id` as a global semantic-log/recovery/reconnect cursor.**

Per-record `last_event_id` provenance pointers are a separate issue and are not covered by this retirement.

## 3.8 Checkpoint event anchor needs later refinement

`checkpoint.valid_through_event_id` may remain useful as one provenance/recovery anchor, but it cannot be treated as the universal recovery frontier for campaign + live + operational state. Step 5.7 must decide its final role.

---

# 4. Why Option B-NARROW is recommended

Two current consumers already need a common cross-domain consistency rule.

## 4.1 Context Assembler

Step 4 requires coherent pinned source input.

In an active live scene one campaign SHA does not contain current live-owned mutable truth. A role context may need:

```text
campaign-owned scope -> pinned campaign revision
live-owned scene scope -> authoritative live epoch revision based on its campaign base
```

The source markers cannot be compared numerically, but they must be proven compatible for the requested scope.

## 4.2 Cold recovery/checkpoint

Step 3 requires exact recovery of suspended Procedure/Continuation/RNG/pending work. Active live scope may also be independently authoritative.

A recovery basis therefore may require several domain-specific roots/markers. The shared requirement is compatibility and domain typing, not one universal Frontier value.

Without Option B's two laws, those same rules must be re-invented separately in Context Assembler, checkpoint, live recovery and later projection tooling.

---

# 5. What Option B-NARROW does *not* create

Explicit non-goals:

```text
NO runtime.frontier class
NO Frontier JSON schema
NO frontier registry
NO generic comparison API
NO universal dominates() function
NO global monotonic sequence
NO generic RecoveryCut record
NO replacement for runtime.id_allocator
NO requirement that all domains use the word frontier
NO physical representation decision for 5.2/5.7/5.8/5.9
```

Native representations remain native:

```text
campaign revision -> Git commit/ref semantics
live revision     -> epoch/head/blob/revision semantics
chronology        -> causal/order evidence
RNG               -> stream state/cursor
Continuation      -> generation/dependency refs
ID allocation     -> campaign-allocator / identity-policy semantics
Story             -> source-coverage semantics + separate layer-local IDs
```

---

# 6. Strongest weakness of Option B-NARROW

It may still be more terminology than the runtime needs.

A disciplined team could state every domain contract explicitly and never introduce a shared term. The danger is that `frontier` and especially `coherent source cut` later become excuses to build a generalized framework.

This is why the challenged recommendation makes Option B deliberately non-machine:

- semantic definitions only;
- two enforceable laws only;
- every concrete representation must still be justified in its owning slice;
- later slices may remove a conceptual term if it proves unnecessary.

---

# 7. Trade-offs

| Concern | A — domain-local only | B-NARROW — shared laws | C — generic model |
|---|---|---|---|
| Immediate complexity | lowest | low | high |
| Prevents false cross-domain comparison | convention only | explicit invariant | mechanically possible |
| Helps recovery/context composition | ad hoc | yes, semantically | yes |
| Risk of generic framework creep | lowest | low if guarded | high |
| Domain-specific fidelity | highest | highest | risk of loss |
| Later reversibility | high | very high | lower |
| Current concrete consumer support | sufficient but repetitive | strongest balance | unnecessary |

---

# 8. Recommended decision

Approve **Option B-NARROW** with the following exact boundaries:

1. `frontier` means only a domain-typed boundary of established progress, coverage or constraint knowledge;
2. frontier is never semantic authority merely by existing;
3. every frontier interpretation names its domain/scope;
4. no implicit comparison/order across domains;
5. any cross-domain relation must be explicitly named by the owning contracts (`based_on`, `projected_through`, `absorbed_from`, `compatible_with`, etc. as actually needed; no mandatory global relation enum);
6. no common machine type/schema/API in Step 5.1;
7. `coherent source cut` is conceptual only: a scope-indexed compatible selection of source markers for one read/recovery operation;
8. HOT/dirty/SOFT/HARD/pointers/cursors/revisions/allocator state remain separately classified;
9. preserve `runtime.id_allocator` as the distinct campaign-scoped identity-allocation owner; do not turn allocator counters into progress/frontier semantics;
10. retire `CURRENT.last_event_id` global cursor;
11. do not treat `checkpoint.valid_through_event_id` as universal recovery frontier; final field fate belongs to 5.7.

---

# 9. Confidence and falsifiability

Recommendation confidence: **HIGH**.

Evidence that would change the recommendation toward A:

- Context Assembler and cold recovery prove they need no common domain/scope compatibility rule at all;
- shared vocabulary yields no testable invariant beyond naming style.

Evidence that would change it toward C:

- several concrete later consumers prove they require exactly the same heterogeneous marker interface/comparison/composition behavior;
- domain-native contracts repeatedly produce correctness bugs that a common machine type would actually prevent.

Neither condition is currently established.

The allocator review does **not** move the recommendation toward C. It is instead evidence for domain-native ownership: identity allocation already has a concrete specialized owner and conflict contract that should not be generalized into Frontier semantics.

---

# 10. Human decision requested

Decision requested from project owner / human architect:

```text
A — Domain-local only
B — B-NARROW shared semantic laws (RECOMMENDED)
C — Unified first-class frontier model
```

If B is approved, the next design-cycle stages remain inside Step 5.1:

```text
owner decision
    -> candidate specification
    -> adversarial review
    -> resolution/canonical Step-5.1 spec
    -> Step-5.1 summary/review
```

Step 5.2 must not start as part of this decision.
