# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Decision Brief

Status: **DECISION BRIEF — OWNER APPROVAL REQUIRED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Derivation:

- `2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-analytical-challenge.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-owner-clarification-addendum.md`

This brief asks for approval of one architecture direction. Mechanical details, schema names, transport protocol and later-slice bindings remain agent-owned/deferred after approval.

---

# 1. Decision requested

Approve or reject:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

Recommended architecture:

```text
semantic survival axis:
    EPHEMERAL | ESTABLISHED

current durability axis:
    DURABLE | VOLATILE_DIRTY

current durability obligation:
    MAY_DEFER
    MUST_BE_DURABLE_BEFORE(edge)

SOFT
    = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER

HARD
    = an active MUST_BE_DURABLE_BEFORE(edge) obligation,
      not a permanent intrinsic class of a fact
```

When durability is required, the publication promise is built from:

```text
POLICY ROOTS
    + DIRTY ACCUMULATION SCOPE selected by the owning policy
    + TRANSITIVE REQUIRED RECOVERY/REFERENCE/INTERPRETATION CLOSURE
```

The architecture introduces no universal persistent HARD flag, global save frontier, generic snapshot or global dirty timeout.

---

# 2. Why this model is recommended

## 2.1 The same state can be SOFT now and mandatory later

A quest acceptance, item change or relationship mutation may be established HOT state that can safely remain unpublished for many singleplayer turns.

Later that same state may become mandatory because:

- the player explicitly asks to save;
- controlled handoff is about to relinquish the host;
- a shared/multiplayer edge needs another participant to observe/use it;
- it becomes a required dependency of another durability-critical transition;
- a configured local/private risk-control policy requests an opportunistic flush.

Therefore static intrinsic HARD/SOFT labels cannot express the actual semantics cleanly.

## 2.2 Correct durability completeness is wider than direct causality

A durable point is invalid if it contains the apparent world mutation but omits something required to resume correctly, including as applicable:

- newly referenced native owner/record;
- required index/routing enrollment;
- unresolved RuntimeCommand/Resolution/Procedure/Continuation state;
- mandatory child/firing identity;
- fixed accepted RNG required by unfinished execution;
- source/claim/execution continuity from Step 5.3;
- irreducible accepted input/message evidence;
- compatible accepted runtime/catalog/rules interpretation context.

Therefore `causally related dirty files` is insufficient. Step 5.5 must require recovery-complete closure under Step 5.2/5.3.

## 2.3 Pure dependency-only publication is too narrow for normal singleplayer

Suppose a singleplayer session accumulates several independent SOFT facts and then reaches a normal durable location/lifecycle boundary.

Publishing only the dependency closure of the trigger could produce a structurally coherent but surprising recovery point that preserves the later location boundary while losing several earlier established events from the same local play period.

The current product behavior intentionally batches accumulated local SOFT at natural boundaries.

Therefore the owning durability policy also contributes a **dirty accumulation scope**.

For normal singleplayer this may conservatively be the active local campaign dirty partition. For narrow multiplayer/live/shared boundaries it can be much smaller.

---

# 3. Scope-aware durability policy

Unpublished exposure and accumulation are not campaign-global.

Conceptually:

```text
DurabilityPolicy(scope) {
    accumulation_scope
    barrier_edges
    unpublished_exposure_policy
    publication_authority
}
```

This is an architecture contract, not a required serialized object.

## Singleplayer / private-local

Primary risk is host/chat/context loss.

Ordinary established state may stay SOFT for long periods and batch at later boundaries.

A configured maximum intended unpublished exposure may exist, but Step 5.5 does not select a universal numeric value.

## Multiplayer private/local

Participation in multiplayer does not automatically make all state immediately shared. Truly private/local state may use a deferrable policy similar to singleplayer.

## Multiplayer shared outside active live epoch

Once state can affect another participant's observation, ownership, authorization, race-sensitive action or shared-world decision, stronger event-driven durability is expected.

Exact multiplayer ownership/binding rules remain Step 5.8.

## Same-scene live

Current architecture already implies an action-level shared boundary:

```text
resolve shared logical action
    -> publish live CAS delta
    -> then reveal/narrate the shared consequence
```

The campaign branch may legitimately lag while live authority owns the mutable scope.

---

# 4. Explicit `save` / `сохрани игру`

Recommended contract:

> A successful explicit save means every established gameplay-significant dirty root in the selected save scope, plus every required recovery/reference/interpretation dependency needed to resume that state honestly, is actually durable through its native authoritative representation.

This preserves the useful existing `SAVE_ALL_DIRTY` meaning while updating `all` to mean semantic roots + required closure rather than every loaded/cache/projection file.

Explicit save:

- does not create canon from unresolved guesses;
- does not replace structured native owners with a prose summary;
- does not imply pause/end unless separately requested;
- does not imply activation/readiness;
- does not require a checkpoint merely because the user said save;
- does include unresolved accepted operational state when that state is part of the promised resume point;
- need not synchronously refresh arbitrary noncanonical Story/transcript projections unless specific evidence is irreducible for recovery.

During the save attempt, the selected save root set is scoped/quiesced enough to avoid a moving-target acknowledgement.

A save may be called successful only after the promised closure is actually durable.

---

# 5. Friendly save/publication failure semantics — owner direction already resolved

The owner has explicitly rejected hard-locking coherent local/private play merely because an explicit save publication failed.

Canonical candidate should therefore implement the following semantic distinction.

## Explicit save failure

If save fails while coherent HOT state survives:

- do not say `saved`;
- preserve the dirty HOT state;
- report the failure briefly and honestly;
- offer retry/repair where useful;
- allow later ordinary gameplay if the player proceeds;
- do not require a ritualized explicit `continue without saving` confirmation when subsequent intent already makes the choice clear;
- retain the enlarged unpublished-loss exposure;
- if the HOT state is later destroyed, recover only actual durable state.

An explicit save request promises durability only on **success**, not permanent gameplay availability of storage.

## Correctness-critical durability edge

This friendliness does not waive a semantic edge whose postcondition itself requires durability.

Examples:

- live shared mutation before shared reveal;
- controlled handoff before acknowledging recovery-safe relinquishment;
- another domain-defined visibility/ownership transition that cannot be correct without publication.

Such an edge may fail or remain incomplete, but it cannot be falsely acknowledged as crossed successfully.

Independent unaffected scopes/OOC communication may remain available where safe.

---

# 6. Bounded SOFT exposure / periodic safety flush

The old hard-coded `one hour` contract is rejected as an architecture constant.

Recommended semantic policy:

```text
scope has established unpublished SOFT
    -> exposure age begins when that scope/partition becomes dirty
    -> configured policy threshold may request durability at an available runtime opportunity
```

Important properties:

- measure exposure from actual dirty establishment, not merely from age of the latest campaign commit;
- unrelated publication must not falsely reset another still-dirty partition;
- clean state never creates a heartbeat/no-op write;
- without background execution, no exact wall-clock publication instant can be promised;
- a stronger immediate semantic edge always dominates the deferrable exposure policy;
- no numeric duration is selected by Step 5.5.

Following owner direction, a local/private exposure ceiling is a **risk-control/SLO policy**, not a correctness barrier.

If its flush attempt fails while coherent HOT state survives:

- remain honest that protection is degraded;
- allow local/private play to continue;
- retry at later suitable opportunities;
- do not pretend the desired exposure target was satisfied.

For shared/live scope, stronger event-driven Step-5.8 policies may be non-deferrable for correctness.

---

# 7. Advisory host-capacity signals

Step 5.4 already established that approximate message/token/chat-age/capacity heuristics are not authoritative.

Recommended 5.5 disposition:

- advisory capacity risk may warn/recommend handoff;
- it may request an opportunistic SOFT flush at a safe point;
- false positives must cause at most unnecessary I/O/warning, not semantic corruption;
- false negatives fall back to ordinary durability + crash recovery;
- advisory risk alone does not create a correctness-critical HARD edge.

A reliable destructive lifecycle signal remains Step-5.4 controlled-handoff input.

---

# 8. Alternatives considered

## Alternative A — intrinsic static HARD / SOFT fact labels

Example:

```text
quest = SOFT
PC death = HARD
```

### Advantages

- simple vocabulary;
- easy local classification tables.

### Problems

- same fact changes durability requirement as it crosses save/handoff/shared boundaries;
- does not encode what semantic edge is blocked;
- encourages universal behavior for materially different boundaries;
- tends toward persistent HARD flags with duplicate/unclear authority.

**Recommendation: reject.**

---

## Alternative B — every HARD boundary means global `SAVE_ALL_DIRTY`

### Advantages

- simple recovery promise;
- minimizes selective-closure reasoning.

### Problems

- breaks scope partitioning;
- narrow multiplayer/live visibility changes would flush unrelated private/local state;
- increases latency and write contention;
- conflicts with Step-5.1 no-global-frontier and Step-5.2 partitionable routing direction;
- creates hidden campaign-global synchronization pressure.

**Recommendation: reject.**

---

## Alternative C — pure trigger dependency closure only

### Advantages

- minimal write set;
- strong locality.

### Problems

- normal singleplayer durability boundaries could preserve later trigger state while losing earlier independent established play;
- violates current product expectation that natural singleplayer forced boundaries protect accumulated local progress.

**Recommendation: reject in pure form.**

The recommended model keeps dependency closure but adds policy-owned dirty accumulation scope.

---

# 9. Strongest counterargument to recommendation

The recommended model has more conceptual dimensions than the current three words `HARD/SOFT/EPHEMERAL`.

A simpler implementation could say:

```text
all established state is dirty until saved
specific runtime rules simply call save when needed
```

and avoid formal `MUST_BE_DURABLE_BEFORE(edge)` semantics.

Why this is insufficient:

- it cannot mechanically distinguish write-before-reveal from save acknowledgement from handoff relinquishment;
- failure behavior becomes ad hoc in each module;
- future multiplayer/live policies would duplicate persistence semantics;
- recovery completeness risks being specified differently at each call site;
- the same physical `save` helper would acquire accidental product semantics.

The recommended model is slightly richer but centralizes exactly the distinctions already required by current architecture.

---

# 10. What approval fixes

If the owner approves **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**, Step 5.5 candidate/canonical work will treat the following as decided:

1. `EPHEMERAL` concerns whether material is intended/required to survive; `SOFT` is established volatile state whose durability may currently defer.
2. `HARD` means an active durability obligation tied to a named semantic edge, not a permanent intrinsic state category.
3. Required publication uses policy roots + policy-owned dirty accumulation scope + transitive recovery/reference/interpretation closure.
4. Normal singleplayer forced boundaries may flush the accumulated local dirty partition rather than only trigger dependencies.
5. Explicit `save` is intentionally broad within its selected save scope and preserves all established dirty roots + required closure.
6. Save success acknowledgement requires actual durability; save failure does not hard-lock coherent local/private gameplay.
7. Correctness-critical durability edges cannot be falsely crossed/acknowledged without durability.
8. Dirty exposure is scope-policy-owned, not campaign-global or per-file by architecture.
9. No universal numeric dirty-age threshold is canonicalized.
10. Local/private exposure threshold is a risk-control/SLO trigger; failure degrades protection but does not permanently block play.
11. Shared/live scope may receive stricter event-driven policies in Step 5.8.
12. Advisory host-capacity heuristics may prompt warning/opportunistic flush but are never correctness authority.
13. Clean state never creates heartbeat publication.
14. Exact physical publication/crash consistency remains Step 5.6.

---

# 11. Deferred mechanical/later-slice work

Approval does not decide:

- wire/schema representation of dirty policy/exposure tracking;
- exact singleplayer/default exposure duration;
- product/config location for exposure defaults;
- exact physical dirty partitions where implementation can safely aggregate;
- Git tree/commit/ref transaction and ambiguous write proof — Step 5.6;
- checkpoint/source-selection representation — Step 5.7;
- exact multiplayer/live ownership/visibility bindings and CAS policy — Step 5.8;
- chronology persistence — Step 5.9;
- Story projection durability — Step 5.10;
- transcript retention — Step 5.11;
- exact host-delivery acknowledgement — Step 5.12;
- machine realization of current stale runtime `one hour` tests/prose.

These are explicit downstream obligations, not gaps in the Step-5.5 semantic decision.

---

# 12. Recommendation and confidence

**Recommendation:** approve **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**.

**Confidence:** HIGH.

Reason confidence is high:

- it composes directly with Step 5.1 partitioning, Step 5.2 recovery closure, Step 5.3 execution/temporal continuity and Step 5.4 handoff barrier;
- it preserves existing zero-I/O singleplayer behavior;
- it explains current live write-before-reveal without making every multiplayer fact synchronous;
- it preserves the established player meaning of `сохрани игру`;
- it avoids a universal snapshot/frontier/lease;
- it separates correctness from loss-risk policy cleanly;
- major alternatives fail either scope partitioning, recovery completeness or player-visible semantics.

What would materially change the recommendation:

- a future product requirement that every established fact must be globally durable immediately;
- a single authoritative storage engine that eliminates partitioned live/current sources;
- a requirement that explicit save intentionally means only a narrow named subset rather than the current campaign/save scope;
- evidence that policy accumulation scopes cannot be determined without an unacceptable global scan/coordination step.

No such requirement/evidence is present in the current architecture.
