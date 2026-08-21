# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NOT CANONICAL**

Date: 2026-08-20

Challenges:

- `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`
- preliminary recommendation **EDGE-OBLIGATION / RECOVERY-CLOSURE DURABILITY**

This review incorporates the owner clarification that acceptable unpublished-state exposure is materially different between singleplayer/private state, multiplayer shared state, and same-scene live state.

---

# 1. Candidate under challenge

The research recommends:

```text
EPHEMERAL vs ESTABLISHED          semantic-survival axis
DURABLE vs VOLATILE_DIRTY         current durability status
MAY_DEFER vs MUST_DURABLE_BEFORE  current durability obligation

SOFT = established + volatile + may defer
HARD = outstanding MUST_DURABLE_BEFORE(edge) obligation
```

Ordinary mandatory durability uses a bounded recovery-complete closure.

Explicit `save` / `сохрани игру` seeds closure with all established dirty roots in the selected save scope.

Unpublished-state exposure is measured from the state actually becoming dirty, not from an arbitrary prior repository commit.

The challenged draft initially leaned toward pure dependency-rooted selective closure for ordinary HARD boundaries. This review tests whether that is too narrow for singleplayer and how exposure policy should be scoped.

---

# 2. Challenge: is dynamic HARD unnecessary over-formalization?

The current runtime has a simple apparent vocabulary:

```text
HARD
SOFT
EPHEMERAL
```

Could the architecture simply retain those intrinsic labels?

## Analysis

The existing system already has materially different HARD effects:

- live shared mutation must publish before reveal;
- explicit save must publish before saying `saved`;
- controlled handoff must publish before relinquishment;
- PLAY_READY must publish before first true live play;
- dirty-exposure protection blocks later ordinary extension only after its policy fires.

One intrinsic `HARD` bit does not identify the prohibited semantic edge.

The proposed model does not require three persistent fields on every fact. It normalizes concepts already present in separate runtime rules.

## Resolution

Retain `SOFT` / `HARD` as compact operational vocabulary, but define them as derived semantics rather than permanent fact classes:

```text
SOFT
    = established + currently unpublished + deferral still permitted

HARD
    = active durability obligation before a named semantic edge
```

Do not introduce a universal persisted HARD flag merely to encode the architecture.

**Challenge result: recommendation survives.**

---

# 3. Critical challenge: pure dependency-only closure can produce a surprising singleplayer durable point

Scenario:

```text
A = player accepted a quest
B = acquired an item
C = relationship changed
D = focal location changed and fires a normal forced durability boundary
```

Assume A/B/C are structurally independent of D.

A pure dependency-only closure could publish D while leaving A/B/C volatile. After a crash the player resumes in the new location but loses several earlier established events from the same continuous singleplayer play period.

That source set may be structurally self-consistent yet violate the product expectation encoded by current singleplayer batching: a natural forced save boundary normally protects accumulated established play, not only the trigger record.

## Analysis

Two closure-expansion relations are distinct:

1. **required dependency closure** — state must join because recovery/reference/interpretation correctness depends on it;
2. **policy-owned accumulation scope** — state joins because the durability policy intentionally promises to protect accumulated dirty progress in that scope at this boundary.

Therefore the closure function should be:

```text
DURABILITY_CLOSURE(D) =
    POLICY_ROOTS(D)
    UNION DIRTY_ACCUMULATION_SCOPE(D)
    then TRANSITIVE_REQUIRED_DEPENDENCY_CLOSURE
```

This preserves current singleplayer behavior without making every narrow shared boundary campaign-global.

### Singleplayer implication

For the normal singleplayer campaign-local durability partition, a forced boundary should ordinarily flush all accumulated established dirty state in that partition, then close over required dependencies.

This matches the useful existing `flush accumulated SOFT` promise.

### Multiplayer implication

A narrow shared/live/access boundary need not flush unrelated dirty private/local scopes. Its accumulation scope is whatever shared authority/visibility policy owns.

### Explicit save implication

Explicit save remains intentionally broader:

```text
DIRTY_ACCUMULATION_SCOPE(save)
    = all established dirty state in selected save scope
```

## Resolution

The initial pure dependency-only formulation was too narrow.

Adopt **policy accumulation scope + required dependency closure**.

**Significant refinement; top-level architecture survives.**

---

# 4. Owner clarification challenge: where does dirty exposure duration belong?

The owner correctly distinguishes three operational risk profiles:

```text
singleplayer/private
    only local host/context loss threatens unpublished state

multiplayer shared but not same live authority
    stale publication can affect another participant's decisions/conflicts

same-scene live
    other participants need the shared operational truth essentially immediately
```

A single campaign-global dirty timeout cannot model these correctly.

## Analysis

Dirty exposure should be a property of a **durability policy applied to an authority/writable/visibility scope**, not one scalar campaign clock.

Conceptually:

```text
DurabilityPolicy(scope) {
    accumulation_scope
    barrier_edges
    unpublished_exposure_policy
    publication_authority
}
```

This is a conceptual policy contract, not a required record schema.

### 4.1 Singleplayer / private-local scope

Risk:

- process/chat/context loss;
- controlled handoff opportunity may arrive late or not at all.

There is no concurrent writer whose correctness depends on seeing every ordinary update immediately.

Therefore:

- ordinary gameplay remains SOFT for long periods;
- configured maximum intended unpublished exposure may be comparatively large;
- ordinary forced boundaries can batch the active local dirty partition;
- no heartbeat exists when clean;
- if no runtime opportunity exists, no exact timed write is promised.

The exposure ceiling is a risk-control policy, not shared-world synchronization.

### 4.2 Multiplayer private/local scope

A change that is still genuinely private/local and cannot affect another participant may remain buffered similarly to singleplayer, subject to the applicable exposure/host-loss policy.

Participation in a multiplayer campaign does not by itself make every local fact immediately shared.

### 4.3 Multiplayer shared, outside an active live epoch

Once a fact can affect another participant's observation, authorization, ownership, race-sensitive action or shared-world decision, elapsed-time batching is secondary.

The stronger policy is normally **event/edge driven**:

```text
shared established mutation
    -> durable promptly before later shared/conflicting use
```

The exact ownership and synchronization rule remains Step 5.8.

A time ceiling may still exist as a fallback, but it is not the primary correctness mechanism.

### 4.4 Same-scene active live scope

Current live architecture already establishes the strongest profile:

```text
resolve one logical shared action
    -> apply complete shared delta
    -> publish one live CAS mutation
    -> only then reveal/narrate shared consequence
```

Therefore a shared live mutation has no legitimate multi-turn dirty exposure window. The only unpublished interval is the local in-flight action/transaction before the required live write succeeds.

The durable campaign branch may lag because live authority owns current mutable truth until compaction; this is not equivalent to the live state being “unsaved.”

### 4.5 Cross-scope propagation

A previously private/local dirty fact may acquire a stronger durability obligation when it crosses an ownership/visibility/causal boundary.

Example:

```text
private/local fact X may defer

later X becomes prerequisite for:
    another player's observation
    shared item ownership
    cross-scene causal event
    shared NPC state

=> stronger shared policy now applies
=> X joins the relevant closure before that shared edge
```

This avoids classifying facts permanently as “singleplayer-like” or “multiplayer-like.”

## Ownership split between roadmap slices

Recommended boundary:

```text
STEP 5.5
    canonicalizes that unpublished exposure is scope-policy-owned,
    not campaign-global;
    defines generic policy semantics and interaction with SOFT/HARD/SAVE;

STEP 5.8
    binds concrete multiplayer/live ownership/visibility conditions
    to stronger event-driven durability edges and live publication authority.
```

5.5 must not pre-decide the full live ownership protocol, but it must leave the policy interface capable of expressing it.

## Resolution

Replace any implication of one global `max_dirty_age` with **scope-aware unpublished-exposure policy**.

No universal numeric duration is canonicalized.

**Challenge result: owner clarification materially strengthens the model.**

---

# 5. Challenge: should exposure policy be per native owner, per file, per scene, or per campaign?

Over-granularity can create bookkeeping overhead; under-granularity can reset old dirty state incorrectly.

## Alternatives

### E-A — one campaign-global exposure bucket

Simple but incorrect when unrelated publication resets dirty state that remains unpublished elsewhere, and incompatible with partitioned live/shared ownership.

Reject as architecture requirement.

### E-B — one clock per file/record

Precise but unnecessarily coupled to physical storage representation and potentially high bookkeeping overhead.

Reject as architecture requirement.

### E-C — policy-owned durability partition/scope — RECOMMENDED

The policy defines the smallest practical accumulation/exposure partition compatible with actual ownership and publication authority.

Examples may include:

- one aggregate singleplayer campaign-local dirty partition;
- one player-private partition;
- one shared non-live scope;
- active live epoch scope;
- another future native writable partition.

A singleplayer implementation may conservatively use one aggregate campaign-local bucket because there is only one effective writer, provided no unrelated publication can falsely reset dirty state outside that bucket.

## Resolution

Canonicalize semantics at the **durability-policy scope/partition** level, not record/file level.

Physical representation remains implementation/later-slice detail.

**Challenge result: E-C recommended.**

---

# 6. Challenge: should a numeric exposure ceiling be architecture or configuration?

A universal value such as one hour is easy to test and explain.

However risk profiles differ dramatically:

- same-scene live: effectively action-level publication;
- shared multiplayer: event-driven prompt publication;
- private multiplayer/singleplayer: host-loss risk only, potentially long window;
- different host products may have different context-loss behavior.

## Resolution

Architecture defines semantics, not a universal number.

A policy may provide a configured maximum intended unpublished exposure for deferrable scopes.

The old hard-coded `one hour` is not canonical.

A later product/config decision may choose defaults by mode/profile/host characteristics, but correctness cannot rely on a single magic constant.

**Challenge result: numeric value remains unresolved policy/configuration, not architecture constant.**

---

# 7. Challenge: does a SOFT exposure ceiling become non-abandonable once fired?

Suppose singleplayer dirty state has exceeded its configured exposure ceiling but storage is temporarily unavailable. The host still owns coherent HOT state.

Could the player intentionally continue despite risk?

## Analysis

If the ceiling is merely advisory, it does not actually bound exposure.

If the engine silently continues after failure, the configured maximum has no enforceable meaning during available runtime opportunities.

Therefore once the exposure policy reaches its enforcement condition, it should create:

```text
MUST_BE_DURABLE_BEFORE(NEXT_ORDINARY_GAMEPLAY_EXTENSION)
```

OOC discussion, retry, repair, save/handoff control and independent unaffected scopes may continue.

The next gameplay extension of the affected scope remains blocked until durability succeeds or a higher-level policy explicitly disables/changes the configured protection.

This is different from a user-requested explicit save, whose abandonability is separately challenged below.

## Resolution

Treat a fired configured exposure ceiling as a real non-silent durability barrier for the affected scope.

**Challenge result: recommend non-abandonable at runtime absent explicit policy reconfiguration.**

---

# 8. Challenge: plain explicit save in-flight — what must block?

A player says `сохрани игру` while current state is coherent HOT.

Should the engine accept the next gameplay action while save publication is still unresolved?

## Analysis

Allowing further mutation before resolving the requested save changes the root set being promised and makes the acknowledgement ambiguous: did `save` mean state at request time or state after later gameplay?

The simplest semantics are a short scoped save barrier:

```text
save intent accepted
    -> freeze selected save root set / relevant mutation scope
    -> establish SAVE_CLOSURE durability
    -> success or failure result
    -> unfreeze / continue according to outcome
```

This is analogous in shape to Step-5.4 handoff quiescence but does not relinquish the host.

OOC communication may continue; independent scopes may continue if truly outside the selected save promise.

## Resolution

Plain save should not accept further dependent gameplay mutations into the selected save scope until the save attempt resolves success/failure.

This avoids moving-target save semantics.

**Challenge result: add scoped save quiescence.**

---

# 9. Owner-level product choice: what happens after explicit save fails but HOT state survives?

After failure the save attempt is resolved as failed; state remains coherent locally.

Two credible policies remain.

## S-F1 — FAILED SAVE MAY BE EXPLICITLY ABANDONED — RECOMMENDED

- report that save failed;
- preserve dirty HOT state;
- do not say `saved`;
- player may explicitly continue without that requested durability guarantee;
- independent non-abandonable HARD obligations still apply;
- if player does not explicitly abandon/cancel, keep ordinary gameplay in the save scope paused.

Advantages:

- transient storage outage does not permanently lock singleplayer;
- preserves honest current state;
- explicit acknowledgement prevents silent risk escalation.

Risk:

- user can choose to continue with larger loss exposure.

## S-F2 — FAILED SAVE BLOCKS UNTIL SUCCESS

- ordinary gameplay remains blocked until persistence succeeds;
- no cancellation path.

Advantages:

- strongest protection;
- very simple guarantee.

Risk:

- storage outage can make coherent local singleplayer unplayable.

## Recommendation

**S-F1**.

This is a material product-semantics decision and requires owner approval before canonicalization.

---

# 10. Challenge: explicit save vs controlled handoff

Both need recovery-complete state, but should they be identical operations?

## Analysis

They can reuse the same closure machinery but differ in policy roots and postcondition:

```text
SAVE
    protect all established dirty state in selected save scope
    host remains attached after success

HANDOFF
    protect every state promised for handed-off scope
    host relinquishes that scope after success
```

In ordinary singleplayer these root sets may often coincide.

Making them definitionally identical would unnecessarily constrain partitioned multiplayer and future scoped handoff.

## Resolution

Share closure semantics; keep intent/postcondition distinct.

**Challenge result: recommendation survives.**

---

# 11. Challenge: should Story/transcript freshness be part of save?

The phrase “save game” could be interpreted as saving everything visible to the user, including narrative history.

## Analysis

Step 4 makes Story noncanonical projection. Step 5.11 will separately govern transcript retention. Making all projections synchronous with save would broaden the canonical durability barrier without improving recovery of gameplay truth.

Exception: literal message/provenance evidence that remains irreducibly necessary to resume accepted semantics under Step 5.4 is not “mere transcript projection”; that specific evidence belongs to recovery closure.

## Resolution

Save guarantees current canonical gameplay/operational recovery closure, not arbitrary Story/transcript projection freshness.

**Challenge result: no change.**

---

# 12. Challenge: advisory host-capacity risk

Should a near-capacity heuristic force an early SOFT flush?

## Analysis

False negatives mean correctness cannot depend on it. False positives can generate unnecessary I/O/barriers.

Step 5.4 already gives a clean path:

```text
advisory risk
    -> warn/recommend handoff

explicit/controlled handoff intent
    -> real BARRIER-NATIVE durability obligation
```

A product profile may opportunistically flush at a safe point, but that is optimization, not authority.

## Resolution

Do not make advisory capacity a HARD reason by itself.

Permit optional opportunistic flush as non-correctness policy.

**Challenge result: recommendation survives.**

---

# 13. Refined recommended architecture

The challenged and refined direction is:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

Core model:

```text
semantic survival:
    EPHEMERAL | ESTABLISHED

current durability:
    DURABLE | VOLATILE_DIRTY

current obligation:
    MAY_DEFER
    MUST_BE_DURABLE_BEFORE(edge)

SOFT = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
HARD = active MUST_BE_DURABLE_BEFORE(edge)
```

Closure:

```text
DURABILITY_CLOSURE(D) =
    POLICY_ROOTS(D)
    + DIRTY_ACCUMULATION_SCOPE(D)
    + transitive REQUIRED_DEPENDENCY_CLOSURE
```

Exposure:

```text
unpublished exposure is owned by DurabilityPolicy(scope)
not by one campaign-global timer
not by time since arbitrary last commit
```

Profiles implied by current architecture:

```text
singleplayer/private local:
    long deferrable exposure allowed
    configured host-loss protection ceiling

multiplayer private/local:
    may defer while truly non-shared

multiplayer shared/non-live:
    stronger event-driven prompt durability
    exact ownership policy finalized by 5.8

same-scene live:
    shared mutation live-published before reveal
    no multi-turn shared dirty window
```

Explicit save:

```text
save scope frozen while attempt resolves
SAVE_ROOTS = all established dirty state in selected save scope
SAVE_CLOSURE = roots + required dependency closure
success only after actual durability
no mandatory checkpoint
no pause/activation implied
no heartbeat if already durable
```

SOFT exposure ceiling:

```text
when configured policy limit is exceeded
at first available authoritative opportunity
    -> MUST_BE_DURABLE_BEFORE(NEXT_ORDINARY_GAMEPLAY_EXTENSION)
```

No universal numeric threshold is selected.

---

# 14. Remaining owner decision

After challenge, one material choice remains:

> If an explicit player save fails while coherent HOT state survives and no other non-abandonable HARD obligation exists, may the player explicitly cancel/abandon the save request and continue playing with acknowledged unsaved risk?

Recommendation:

> **YES — explicit abandonment allowed (S-F1).**

Do not silently continue. Until success or explicit abandonment, keep the selected save scope quiescent.

All other major Step-5.5 results are derivable mechanical architecture from closed Steps 3/5.1–5.4 plus the owner clarification on scope-dependent exposure.

---

# 15. Challenge verdict

**PASS WITH SIGNIFICANT REFINEMENTS.**

The preliminary architecture survives, with three important changes:

1. ordinary durability closure includes policy-owned accumulated dirty scope before dependency closure; it is not pure trigger dependency closure;
2. dirty exposure is explicitly scope-policy-owned, allowing long singleplayer buffering, event-driven multiplayer sharing, and action-level live publication;
3. explicit save receives scoped quiescence while the requested save frontier is being established.

No evidence requires a global dirty timer, global SAVE_ALL_DIRTY for every HARD reason, universal checkpoint, or background scheduler.