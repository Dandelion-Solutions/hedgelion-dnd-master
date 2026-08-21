# Step 5.14 — Full Recovery & Concurrency Adversarial Review — Analytical Challenge

Status: **ANALYTICAL CHALLENGE COMPLETE — RESOLUTION GATE PENDING**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Inputs:

- Step-5.14 task brief;
- Step-5.14 integrated adversarial review;
- canonical Steps 3–5.13 and owner decisions;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
- current preliminary Step-6 RepositoryPort feasibility evidence.

Purpose: attempt to falsify the preliminary conclusion that Step 5 has no unresolved architecture blocker.

---

# 1. Strongest opposing thesis

The strongest case against closing Step 5 is:

> The architecture appears coherent only because difficult cross-domain atomicity, source-currentness, host-delivery and cleanup problems are repeatedly deferred to bounded routing, exact-source validation and Step 6. Without a universal transaction/snapshot/clock or durable job/ack system, a sufficiently adversarial combination may expose either two current owners, a lost accepted obligation, a stale disclosure leak or an irreversible cleanup race.

This challenge treats that thesis as serious and attacks each claimed escape hatch.

---

# 2. Challenge A — Is “coherent source composition” secretly an underspecified global snapshot?

## Attack

Recovery begins from campaign H selecting live A and B. While hydration runs:

```text
A ACTIVE @ A10 -> A11 -> CLOSED A12
B CLOSED @ B7 -> campaign absorption attempt
campaign H -> H2 route movement
```

A naive implementation could combine campaign routing from H, A10 payload, B7 payload and later H2 dependencies and call the result recovered.

If Step 5 requires one hidden globally simultaneous cut to avoid this, B-NARROW failed.

## Existing laws that must close it

- each mutable native source is exact-revision pinned for one recovery attempt;
- campaign H anchors current route discovery but is not complete state;
- route-selected source authority is owner-defined, not timestamp selected;
- final root/routing/current-source basis is validated before READY;
- movement is RETRY until a coherent accepted source composition is proven;
- no source marker is compared numerically across domains.

## Result

No global simultaneity is actually required. The operation needs a **compatible source composition**, not a claim that all source revisions existed at one wall-clock instant.

For independent scopes, compatibility is simply independent current authority. For related scopes, the owning route/transfer/recovery contract supplies the relation being proved. A source movement that invalidates that relation invalidates the attempt.

The architecture would fail only if implementation treated “I successfully read all files” as compatibility proof. That is already forbidden.

Verdict: **challenge rejected — NO DEFECT**.

---

# 3. Challenge B — Does multi-live global execution require an impossible distributed transaction?

## Attack

One accepted command intends a global consequence over three active live scenes. A closes, B closes, C continues changing. Host crashes. Later C closes. Before campaign absorption, another unrelated campaign commit advances HEAD.

Could the command have been partially established fictionally, requiring rollback or distributed commit?

## Existing laws that must close it

- live atomicity is per native durability edge, not per user action;
- affected live sources close/freeze independently;
- partial freeze is explicitly not partial fictional transfer/global-event establishment;
- accepted execution/Continuation survives close;
- only after all required final sources are known does one campaign transition establish the cross-scope effect/transfer;
- campaign conflict causes current revalidation/transport rebuild or semantic conflict handling, never force rollback;
- chronology does not infer fictional order from close/commit order.

## Result

The command may be accepted/open as an execution owner while its final global state transition remains unsettled. Freeze operations are prerequisite ownership/currentness transitions, not pieces of the final fictional consequence. Therefore crash recovery can resume the open execution against actual CLOSED/ACTIVE states without rolling back already closed sources and without claiming that the global event happened early.

Verdict: **challenge rejected — NO DEFECT**.

Critical realization constraint: do not serialize the final semantic consequence piecemeal into several live refs.

---

# 4. Challenge C — Can cleanup race a new consumer without a distributed lock?

## Attack

Target X is campaign-owned. Cleanup pins campaign H and complete protection routing showing no blocker. Independently writable live source L can create consumer Y referring to X. L does not need campaign HEAD movement for its normal CAS.

Without a global lock, Y could commit after cleanup's negative proof but before X deletion.

## Candidate escapes

1. scan all live sources immediately before delete;
2. create a global durable GC/reference graph;
3. hold a distributed lock/fence on all sources;
4. require a source-specific safe pattern.

Options 1–3 violate established constraints or scale poorly.

## Required safe pattern analysis

Step 5.13 admits X for automatic cleanup only if every blocker-creating source class uses at least one:

```text
SELF-CONTAINED
PROTECTION REGISTERED BEFORE/AT CONSUMER ACCEPTANCE
SOURCE FENCED/SYNCHRONIZED
```

The important ordering for registration is asymmetric and conservative:

```text
add durable protection first
then accept Y
```

not:

```text
accept Y
then eventually publish protection
```

Release may similarly lag after Y ends, producing retention rather than deletion risk.

If L cannot satisfy any safe pattern, X is not automatically deletable while L may create blockers.

## Result

Optional cleanup can safely sacrifice liveness/space reclamation rather than correctness. No universal transaction is required because cleanup eligibility itself is conditional on source-specific admission/fencing semantics.

Verdict: **challenge rejected — NO DEFECT**.

Severity of realization risk: **SIGNIFICANT**. Protection-before-acceptance ordering must be testable and mechanically enforced.

---

# 5. Challenge D — Does normally-SOFT disclosure create two current semantic owners?

## Attack

The same human/player has two concurrent host/session executions. Both are initially authorized and each emission-commits information about the same fact. Neither disclosure update is yet durable. Later both try to publish against campaign state.

If disclosure is one owner `(player,fact)`, are there now two incompatible current HOT truths?

## Analysis

Exposure semantics are monotonic for the exact information exposed:

- `statement_exposed` only grows true;
- objective-status exposure advances by the fact owner's semantic truth-transition relation, not by delivery/Git order;
- repeated compatible exposures can therefore join through native-owner reconciliation;
- Step 5.6 explicitly refuses generic text/last-writer merge and requires owner-defined deterministic reconciliation for overlapping state.

A later stale exposure of an earlier truth revision does not erase the fact that the player had already been exposed to a later semantic revision. Communication history may record both occurrences; disclosure current state keeps the strongest semantic exposure relation.

Where exposure evidence is genuinely contradictory/incomparable and the owner contract requires a linear result, Step 5.12 already requires scoped reconciliation/integrity rather than transport tie-breaking.

This reasoning does **not** generalize to non-monotonic owners. `world.knowledge`, Procedure state, ordinary world state and similar owners remain subject to one writable partition / live containment / synchronization rules.

## Result

The semantic owner remains single even with optimistic unpublished proposals because compatible exposure deltas are joinable by the owner contract; publication establishes the shared durable current result. No last-writer-wins rule is permitted.

Verdict: **challenge rejected — NO DEFECT**.

Realization requirement: explicitly encode/test disclosure merge semantics; never infer this merge property for other owners.

---

# 6. Challenge E — Can revocation race player-visible emission and leak after authority removal?

## Attack

Player P submits an Interaction while authorized. Another host revokes P and closes/absorbs the affected live epoch. P's stale host is still generating a response containing a secret and reaches emission after the revocation campaign transaction.

Could the stale host leak information despite write fencing?

## Distinguish two cases

### E1 — interaction/output semantics were accepted before revocation boundary

Revocation does not retroactively cancel already accepted execution. Step 5.8 already preserves accepted work that won before close. The response remains attributable to the previously accepted interaction/recipient identity, subject to its already validated information eligibility.

The revocation changes future authority; it does not rewrite accepted history.

### E2 — stale host attempts to accept new post-revocation gameplay/output work

Session metadata grants no authority. Current application authorization/routing must be revalidated before accepted gameplay mutation. A stale live write is fenced by CLOSED/exact-source CAS.

For player-visible content, physical recipient/currentness/staging enforcement is a Step-6 host capability obligation. If the chosen host cannot prevent an unvalidated stale context from rendering to the wrong audience, that deployment profile fails Step-4/5.12 feasibility; Step 5 does not add a delivery queue to conceal the problem.

## Result

No semantic contradiction requires reopening Step 5, but physical enforcement is genuinely critical.

Verdict: **STEP-6 FEASIBILITY DEPENDENCY — BLOCKING for secure multiplayer presentation profile**.

---

# 7. Challenge F — Does Step-4 `pinned_campaign_frontier` reintroduce a universal frontier after Step 5?

## Attack

Step 4 describes a RoleContextRequest/Bundle using a pinned campaign/source frontier. Later Steps 5.1/5.7/5.8 establish that campaign HEAD alone is not complete current truth when live/native sources own scopes.

A literal old reading could cause Narrator/Actor/Interpreter to consume stale campaign copies while live source is current authority.

## Resolution

Later canonical ownership/currentness laws narrow the interpretation:

```text
Step-4 coherent role context basis
    = campaign-domain pin where required
    + exact current native source pins selected by current routing
    + accepted historical pinned inputs where the receiving owner requires them
```

The resulting per-invocation source composition is ephemeral evidence, not a universal stored Frontier/RecoveryCut.

Step-4's requirement against branch-relative mixed reads remains valid; what changes is that “coherent” cannot mean “campaign HEAD only.”

Verdict: **SIGNIFICANT CROSS-STEP CLARIFICATION, RESOLVED WITHOUT REOPENING STEP 4**.

This clarification should be carried into the Step-5.14 canonical closure and later Step-6 Context Assembler realization.

---

# 8. Challenge G — Does Story compaction make projection coverage lie?

## Attack

Story layer coverage is far behind. Old `runtime.message` payloads are compacted and eventually envelopes retire. Later the current projection generation reaches those candidate identities.

Could coverage advance despite no source content, falsely claiming genuine consideration?

## Analysis

- exact payload removal does not erase candidate/source-domain identity while currently supported projection coverage still needs it;
- `MAY_OMIT` may be terminally considered without materialized Story output, including where exact source payload is lawfully unavailable;
- `MUST_MATERIALIZE` blocks the source-retention transition until required Story output exists or the obligation lawfully ends;
- source cursor/enumeration continuity must migrate before whole envelope retirement;
- future projection contract changes cannot invent deleted source and cannot silently inherit incompatible coverage.

Thus coverage means “terminally considered under this exact typed projection contract,” not “all original source bytes are still available.”

Verdict: **challenge rejected — NO DEFECT**.

Accepted limitation: later richer Story regeneration may be impossible after lawful source loss.

---

# 9. Challenge H — Does verified Transcript become secret canonical authority after source deletion?

## Attack

A Transcript record becomes the only exact copy after raw source compaction. Later a gameplay mechanic needs exact wording.

Could runtime use Story and thereby violate Story nonauthority?

## Analysis

No. Step 5.11 requires correctness-critical exact semantics to remain in canonical/runtime evidence or a natural canonical owner before source loss. Story Transcript may be sole exact copy only for historical/presentation exactness, not as the only gameplay-semantic owner.

If a future gameplay mechanic newly decides old optional text matters after all canonical exact protection ended, the text is unavailable for correctness unless a retained accepted owner independently provides it. Story coincidence cannot silently promote it.

Verdict: **challenge rejected — NO DEFECT**.

---

# 10. Challenge I — Does append-only Git undo compaction semantics?

## Attack

Old exact payload remains reachable through ancestor Git history after current-tree deletion. A retrieval helper discovers it.

If “data exists physically” means it can be used, Selective Exact is false and cleanup retention semantics are meaningless.

## Analysis

Step 5.13 explicitly separates current semantic retention from Git transport/audit history. Ordinary Master/Story/history query does not mine ancestors to restore lawfully retired exact capability. Explicit forensic/integrity access is separate and does not change semantic retained-memory state.

This is consistent with Step 4's stronger statement that repository readability is not player/PC knowledge/disclosure authority.

Verdict: **challenge rejected — NO DEFECT**.

Realization requirement: ordinary retrieval tooling must enforce current semantic source contracts rather than opportunistically search Git history.

---

# 11. Challenge J — Are Step-6 deferrals hiding a semantic hole?

The unresolved Step-6 gates are:

- deterministic authenticated RepositoryPort;
- physical role-context isolation/reset;
- pre-player-visible Narrator staging/validation;
- stable host invocation/message/retry identity;
- authenticated acting-principal mapping;
- recipient/audience mapping and visible-surface fencing.

A deferral is legitimate only if at least one plausible physical realization exists and the Step-5 semantic contract remains clear regardless of which realization is selected.

Current evidence satisfies that threshold:

- RepositoryPort has multiple plausible backend forms and current lab evidence validates exact tree/race semantics;
- role isolation can be realized by separate invocations or genuine reset/isolation;
- pre-visible validation can be realized by staged internal generation/buffering/outer rendering if the host supports the topology;
- application-level stable identities may be minted or host profiles can be restricted based on available invocation/retry metadata;
- acting principal/audience can be provided by authenticated host/app bindings in capable profiles.

If a selected deployment cannot realize one of these, Step 6 must reject/refine that deployment topology rather than weakening Step-5 correctness.

Verdict: **deferral is architecturally legitimate; feasibility remains materially open**.

---

# 12. YAGNI / simpler-alternative challenge

Could a simpler architecture replace the composed model?

## Universal snapshot + global sequence

Would simplify recovery reasoning superficially but would duplicate native authority, impose cross-domain order on independent live/chronology domains, increase write contention and still not solve host rendering/disclosure. Rejected.

## Durable central pending queue/scheduler

Would simplify temporal restart superficially but creates a second obligation authority and requires synchronization with each native temporal owner. Existing owner+Agenda design is safer and bounded. Rejected.

## Story/event sourcing as recovery authority

Would simplify “replay everything” but conflicts with current-state owners, Story nonauthority, compaction, RNG/interpretation pinning and bounded startup. Rejected.

## Mandatory per-response disclosure persistence/outbox

Would reduce disclosure RPO but adds a repository/network round trip and durable delivery subsystem to every response, contradicting the owner-approved product scope. Not justified by current product promise.

## Generic mark-and-sweep GC

Would simplify conceptual cleanup but cannot faithfully represent semantic protection, source movement, exact-text promises or live currentness; would require broad scans/refcounts and still need owner-specific rules. Rejected.

Conclusion: no simpler general replacement has a better correctness/complexity profile under the accepted requirements.

---

# 13. Final falsification result

The analytical challenge did **not** produce an unresolved Step-5 architecture contradiction.

It did produce one important cross-step interpretive clarification and sharpened several realization obligations:

```text
AC-1  Step-4 coherent role-context frontier is not campaign-HEAD-only;
      use domain-typed current native source composition under Steps 5.1/5.7/5.8.

AC-2  cross-source cleanup protection registration is protection-before-consumer-acceptance;
      otherwise the cleanup contract is nonconforming.

AC-3  disclosure may use owner-defined monotonic merge;
      this property must never be generalized to non-monotonic world/knowledge/execution owners.

AC-4  global multi-live final semantic consequence is established only after prerequisite
      source freezes and final campaign transition; partial freeze is never partial fiction.

AC-5  Step-6 host/transport feasibility gates are genuinely blocking for affected deployment
      profiles but do not justify weakening Step-5 semantics.
```

Current blocker count after challenge:

```text
unresolved Step-5 architecture blockers = 0
```

Recommended next action: pass the Step-5.14 resolution gate, canonicalize the integrated review/clarifications, close Step 5, update roadmap/index, and make Step 6 the next stage without starting it.