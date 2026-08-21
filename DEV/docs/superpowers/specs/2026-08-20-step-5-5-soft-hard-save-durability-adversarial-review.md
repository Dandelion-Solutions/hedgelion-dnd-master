# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE CHALLENGED**

Date: 2026-08-20

Reviews:

- `2026-08-20-step-5-5-soft-hard-save-durability-candidate-spec.md`

Owner-approved direction under review:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

The review attempts to falsify the candidate without reopening already approved product semantics unless a contradiction is found.

---

# 1. Review result summary

No finding requires rejection or reopening of the approved architecture direction.

Three significant refinements are required before canonicalization:

1. explicit save over more than one native durability domain must be defined as a **compatible composed durable source-set promise**, not as one global transaction/commit;
2. a partially successful multi-source publication is not successful save, but already published native state is not rolled back by fiction or ignored — continuation requires a coherent refreshed/revalidated source composition;
3. explicit save with no dirty required roots is allowed to succeed without a heartbeat/no-op write when the promised state is already durably recoverable.

Several smaller wording clarifications are also required around prospective live deltas, scope escalation, and degraded risk-control retries.

---

# 2. Attack: does LAW 5.5-1 make unpublished live prospective state “truth” too early?

Candidate wording says established semantic truth precedes durability.

Potential failure:

```text
same-scene shared action resolves locally
    -> prospective shared delta exists
    -> live CAS has not succeeded
```

If this delta were already authoritative current truth, another participant could legally depend on state that the live authority has not accepted.

## Analysis

Step 3 distinguishes prospective candidate calculation from committed local execution. `LIVE_SCENE.md` further makes successful live publication part of the shared operational establishment/reveal edge.

Therefore “established HOT truth” must mean **established under the owning semantic contract**, not merely computed/proposed in memory.

For ordinary singleplayer local owners, a committed local execution result can be established before campaign durability.

For a live-shared owner whose contract defines publication/CAS as the acceptance edge, the pre-CAS delta remains prospective/in-flight rather than established shared truth.

## Resolution

Canonical wording must explicitly state:

> establishment is owner-contract-relative; a prospective mutation that has not crossed its owning acceptance edge is not ESTABLISHED merely because it exists in memory.

No architecture change.

---

# 3. Attack: can explicit save require one impossible cross-domain atomic transaction?

Suppose the selected save promise includes state whose current authority is composed from:

```text
campaign durable source C
active live source L
runtime routing/owner source R
```

Step 5.1 forbids pretending these domains share one scalar frontier/order. Step 5.2 explicitly permits recovery from compatible native source composition.

Candidate language about “all established dirty roots in selected save scope” could be misread as requiring one physical atomic publication across all participating domains.

## Analysis

That would violate established ownership boundaries and steal 5.6/5.8 physical design.

The correct save postcondition is:

```text
for every required participating native durability domain:
    required roots/dependencies are actually durable

AND

selected revisions/source identities form a compatible
Resumable Runtime Closure for the promised save point
```

No cross-domain total order or distributed transaction is implied.

## Resolution — SIGNIFICANT REFINEMENT

Canonical explicit-save law must say:

> Successful save is a property of a compatible composed set of domain-native durable sources, not necessarily one repository commit or one writable transaction.

Within one native transaction domain, the domain's own coherence/atomicity rules apply. Cross-domain compatibility/recovery selection remains 5.6–5.8 work.

---

# 4. Attack: partial multi-source success after failed save

Scenario:

```text
SAVE requires native sources A and B
A publication succeeds
B publication fails
```

The candidate says failed save preserves HOT state and allows later local/private continuation.

Danger: treating the whole attempt as if nothing durable changed may let the host continue from an obsolete base or later overwrite the successfully advanced native source.

## Analysis

The save promise failed, but actual native publication cannot be fictionalized away.

Required behavior at semantic level:

```text
save status = FAILED / NOT CONFIRMED

but

successful native publication(s) remain real durable authority
```

Before further mutation that depends on those domains, the host must establish a coherent current working composition through normal refresh/revalidation/own-publication adoption rules.

It must not “roll back” the successful source by pretending the old durable point remains authoritative.

Exact ambiguous-ack and physical partial-publication detection belongs to 5.6/5.8.

## Resolution — SIGNIFICANT REFINEMENT

Friendly continuation is conditional on a **coherent surviving/revalidated HOT source composition**, not merely on old in-memory bytes still existing.

No hard lock is introduced: if the runtime can establish coherence, play continues; if a correctness-critical source is unresolved/suspect, only dependent scope is gated under existing integrity rules.

---

# 5. Attack: explicit save when everything is already durable

Player says `сохрани игру`, but selected save scope has no established dirty roots and all required recovery dependencies are already durable.

Could LAW 5.5-15 “no heartbeat” conflict with the user's explicit request?

## Analysis

A save request asks for a durability guarantee, not for a mandatory new commit object.

If the guarantee already holds, a no-op physical write adds no semantic protection.

The runtime may truthfully acknowledge the state as saved after validating from its already-known compatible durable frontier/source set; it need not manufacture a heartbeat commit.

No unnecessary remote read is required merely to reconfirm the runtime's own known-good durable state unless concurrency/authority rules independently require refresh.

## Resolution — SIGNIFICANT REFINEMENT

Canonical law:

```text
SAVE with empty required dirty closure
    + already known compatible durable source set
    -> success may be acknowledged
    -> zero gameplay publication required
```

This is not a no-op “save failure”; the requested postcondition already holds.

---

# 6. Attack: policy accumulation scope can become hidden global SAVE_ALL_DIRTY

Candidate allows ordinary singleplayer policy to flush a whole local dirty partition at a natural boundary.

Could implementations choose “campaign” as the partition even in multiplayer and recreate global synchronization?

## Analysis

LAW 5.5-4 already binds policy to authority/writable/visibility scope, and Step 5.1/5.2 require partitionability.

Canonical wording should strengthen that an accumulation partition must not cross independently writable/owned scopes merely for convenience when doing so would create false synchronization or authority.

A conservative aggregate singleplayer partition is acceptable because one effective local writer/authority can make it coherent. The same aggregation is not automatically valid in multiplayer.

## Resolution

Add explicit anti-overaggregation constraint.

No architecture change.

---

# 7. Attack: can risk-control failure warnings become noisy every turn?

Owner direction says safety-flush failure does not block local/private play and should remain visible as degraded durability.

Naive implementation could retry/report on every subsequent gameplay turn, harming UX and latency.

## Analysis

Step 5.5 defines semantics, not retry cadence. “Remain visible” means do not silently claim the risk target is satisfied, not “repeat the same warning every turn.”

Policy may use bounded retry/backoff/opportunity rules later, provided:

- it does not falsely reset exposure;
- it does not promise background execution unavailable to the host;
- it does not hide a materially relevant persistent failure forever;
- correctness-critical edges remain separate.

## Resolution

Clarify that notification/retry cadence is policy/UX implementation detail; no per-turn spam requirement exists.

---

# 8. Attack: advisory host-capacity opportunistic flush can race accepted gameplay

A host heuristic warns near capacity while a gameplay action is being adjudicated.

Could opportunistic flush capture half of an unresolved action?

## Analysis

No. An advisory signal has no authority to cut through an owning atomic/semantic execution edge.

Opportunistic flush may occur only at a safe closure point where the selected roots are established and the required closure can be frozen/revalidated.

If a reliable destructive signal arrives during unresolved execution, Step 5.4 handoff semantics govern and may require materializing accepted semantic evidence/native execution state rather than persisting partial model reasoning.

## Resolution

Add safe-point requirement for advisory/risk-control flush requests.

---

# 9. Attack: does explicit save silently promise transcript preservation?

Player may interpret “save game” as being able to return to the same conversation wording.

## Analysis

The architecture explicitly separates gameplay recovery from Story/transcript retention. Requiring full transcript freshness at every save would duplicate authority and create heavy synchronous writes.

However accepted exact wording that remains the only evidence preserving unresolved meaning is already irreducible recovery evidence under 5.2/5.4 and therefore belongs in the closure until typed meaning replaces it.

## Resolution

Candidate distinction is correct. No change beyond preserving explicit wording.

---

# 10. Attack: does failed explicit save allow bypass of another HARD edge?

Scenario:

```text
save fails
player immediately issues action
same scope also has independent live write-before-reveal / ownership transfer obligation
```

Friendly-save law alone might be read as permission to continue everything.

## Analysis

Owner clarification and LAW 5.5-10 already say friendliness does not waive independent correctness-critical obligations.

Canonical text should order rules explicitly:

```text
failed SAVE permission to continue
    is subordinate to any independently active
    MUST_BE_DURABLE_BEFORE(edge)
```

## Resolution

Clarify precedence. No architecture change.

---

# 11. Attack: save roots and dirty accumulation can omit required clean-but-revision-sensitive evidence

Some recovery dependency may not itself be dirty but its exact compatible revision matters to interpretation or source composition.

If `DURABILITY_CLOSURE` is read only as a set of dirty writes, the save might omit the revision pin/evidence needed to rehydrate correctly.

## Analysis

Step 5.2 already defines closure as a property over compatible sources; required dependencies may be already durable and need not be rewritten.

Therefore distinguish:

```text
REQUIRED DURABLE SOURCE CLOSURE
    all owners/dependencies/revisions required for the promise

PENDING WRITE SET
    only the subset that must actually be newly published/updated
```

This is critical: closure is not synonymous with dirty file delta.

## Resolution — SIGNIFICANT REFINEMENT

Canonical spec must explicitly separate **durability closure** from **physical pending write set**.

Existing compatible durable dependencies participate in the proof/source composition without being rewritten.

---

# 12. Attack: can exposure age be reset by semantic replacement rather than publication?

Suppose dirty fact X is replaced/superseded by newer established fact Y before either is published.

Does X's old age continue forever?

## Analysis

Exposure tracks the oldest still-relevant unpublished state/closure within the policy partition, not historical dirty deltas that no longer survive as current/recovery-relevant truth.

If X is lawfully superseded and no longer required for current state, accepted execution continuity, audit/provenance, or recovery, it need not keep the exposure age alive.

If Y semantically depends on X's accepted occurrence/provenance, required closure may still carry relevant evidence.

Exact bookkeeping representation is implementation detail.

## Resolution

Clarify “oldest still-relevant unpublished established/recovery state” rather than append-only first-dirty history.

---

# 13. Strongest alternative re-evaluation

## Alternative: remove `HARD` entirely

Use only explicit per-call rules:

```text
save() requires closure
handoff() requires closure
live_reveal() requires closure
```

and retain `SOFT` only as dirty state.

### Strength

This is slightly simpler vocabulary and avoids users treating HARD as a persistent label.

### Failure

The same generic question recurs across domains: what semantic edge is gated, what closure proves it, what failure means, and which independent scope may continue. Without a normalized `MUST_BE_DURABLE_BEFORE(edge)` concept, each domain reimplements those semantics.

The approved architecture already avoids the main risk by defining HARD only as shorthand, not as a required stored flag/type.

**Alternative remains weaker.**

---

# 14. Review disposition

The candidate may proceed to canonicalization after applying these refinements:

1. establishment is owner-contract-relative; prospective/in-flight deltas are not automatically established;
2. successful explicit save may be a compatible composition of multiple native durable domains and does not imply one global transaction;
3. partial native success means overall save failure/not-confirmed, but successful native publications remain real and must be coherently adopted/revalidated before dependent continuation;
4. already-durable clean save may succeed with zero heartbeat publication;
5. distinguish required durable source closure from physical pending write set;
6. prohibit convenience accumulation scopes that cross independent writable/authority scopes and create false synchronization;
7. opportunistic/risk-control flush only at safe established-state points;
8. failed-save friendly continuation remains subordinate to any independent correctness-critical HARD edge;
9. exposure age tracks oldest still-relevant unpublished established/recovery state, not superseded historical dirtiness;
10. degraded-risk retry/warning cadence need not spam every turn.

No new owner decision is required. These are mechanical consistency refinements of the approved model.

**Review confidence: HIGH.**
