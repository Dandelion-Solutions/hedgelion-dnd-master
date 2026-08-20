# Step 5.7 — Checkpoint / Recovery Protocol — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — PRE-CANDIDATE**

Date: 2026-08-20

Recommended direction under challenge:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED RECOVERY**

This review attacks the research recommendation before candidate canonicalization.

## 1. Challenge method

For each proposed rule, ask:

1. what is the strongest competing design;
2. what failure does the proposed rule create;
3. whether a simpler design is sufficient;
4. whether it leaks authority into recovery metadata;
5. whether it survives concurrent source movement;
6. whether it creates an unowned Step-5.8/5.9/6 decision;
7. whether it increases persistent metadata without measurable correctness value.

## 2. Challenge: current campaign HEAD as first anchor may itself move

### Attack

If recovery pins campaign H, then another writer advances the campaign ref to H2 while recovery hydrates. H may still be internally coherent, but releasing gameplay from H would resume a stale campaign view.

A checkpoint-first historical cut does not have this problem because it intentionally targets history.

### Resolution

Ordinary recovery is a **current-resume** operation, not historical replay.

Therefore:

- campaign H is a pinned attempt source, not automatically releasable current authority;
- before writable/current resume release, the recovery core performs a bounded final current-source validation for every authority-bearing ref/route whose movement could make the composition stale;
- if campaign ref moved, recovery does not label H corrupt and does not silently continue from H;
- it repins and re-resolves the affected composition;
- automatic recovery retries are bounded; persistent churn yields `RETRY_REQUIRED`/typed blocked retry rather than an infinite loop.

A read-only historical/support operation may intentionally retain H; that is not ordinary current recovery.

## 3. Challenge: live source may move independently after campaign routing is pinned

### Attack

Campaign H can point to active live scope L. Recovery pins live head L7, then the live ref moves to L8. Campaign H itself did not change.

If final validation checks only campaign H, runtime resumes stale live authority.

### Resolution

Final currentness validation is **per participating mutable authority source/owning route**, not campaign-only.

Conceptually:

```text
pin campaign H
resolve campaign route S -> live ref L
pin L@7
hydrate
before writable resume:
    verify campaign route still resolves S -> L
    verify current L head is still accepted for this attempt
```

If current L moved, repin/recover affected source and transitive dependents.

5.7 does not define epoch fencing/lease semantics. Step 5.8 may later strengthen what “still accepted” means and reduce retry windows.

## 4. Challenge: requiring every current source to remain unchanged may livelock recovery

### Attack

In active multiplayer, a live source can keep advancing. Requiring complete source immobility throughout hydration could prevent recovery indefinitely.

### Resolution

5.7 establishes correctness, not a global stop-the-world lock.

Initial conservative contract:

- exact source revisions are pinned for one hydration attempt;
- resume release requires validation under the owning source's currentness/fencing contract;
- bounded retries are permitted;
- repeated movement yields typed retry/coordination requirement rather than stale resume.

Step 5.8 owns the mechanism that may provide a recover/adopt fence, lease, epoch barrier or equivalent live-specific stabilization. 5.7 must not invent that protocol prematurely.

For campaign-only/single-writer recovery, ordinary HEAD recheck is sufficient.

## 5. Challenge: checkpoint as ordinary acceleration duplicates bounded native routing

### Attack

Step 5.2 already requires typed bounded operational-root routing. A checkpoint that also records root lists creates:

- duplicate membership evidence;
- staleness checks;
- extra schema fields;
- temptation to trust checkpoint completeness;
- little I/O savings if the routing partition itself is small.

### Resolution / refinement

Downgrade checkpoint acceleration from architectural requirement to optional optimization.

Canonical candidate should say:

> Ordinary recovery correctness SHALL NOT require reading a checkpoint. A checkpoint MAY be consulted as immutable verified hint/diagnostic evidence when doing so reduces bounded work. Any hint must be validated against current native routing/ownership before use.

Thus Alternative C (native routing only) is a valid execution path inside the recommended architecture.

No new checkpoint root-list/fingerprint field is required by 5.7 unless later implementation measurement proves value.

## 6. Challenge: if checkpoint is optional, why keep it at all?

### Attack

YAGNI suggests deleting checkpoint entirely.

### Evidence for limited retention

Existing product/runtime concepts already use checkpoint for:

- complex mid-procedure pause support;
- migration/repair evidence;
- support/export diagnostics;
- potential historical recovery aid;
- human-meaningful sparse recovery landmark.

A checkpoint can serve those purposes without ordinary recovery depending on it.

### Resolution

Retain checkpoint architecture only as a **narrow optional immutable recovery/maintenance evidence artifact**.

Do not require ordinary recovery to use it. Revisit deletion if implementation/evaluation shows no meaningful support/diagnostic/recovery value.

This is lower risk than preserving current v2 semantics merely for compatibility.

## 7. Challenge: `MANIFEST.last_checkpoint_id` becomes hidden recovery authority

### Attack

Calling a pointer “last checkpoint” encourages startup code to treat it as the recovery frontier.

### Resolution

If retained, semantics are narrow:

```text
last_checkpoint_id
    = campaign-domain pointer to most recently selected/published checkpoint descriptor
```

It is not:

```text
latest gameplay state
best recoverable state
rollback authority
RRC proof
cross-domain frontier
```

Ordinary recovery may ignore it.

A missing target is a metadata/reference integrity defect scoped to checkpoint facilities, but does not block gameplay if current native RRC can independently be proven.

A future rename may improve machine clarity, but 5.7 need not choose wire spelling before implementation planning.

## 8. Challenge: missing checkpoint target should imply CANON_SUSPECT because MANIFEST has a dangling required ref

### Attack

Current integrity rules say required dangling references produce `CANON_SUSPECT`. If `last_checkpoint_id` exists and target is missing, silently ignoring it appears to weaken integrity.

### Resolution

Two dimensions remain distinct:

- the checkpoint metadata/reference scope can become `CANON_SUSPECT`;
- gameplay recovery readiness can still be `READY` if checkpoint is optional and RRC is independently proven.

Integrity failure remains scope-local, consistent with `INTEGRITY.md`.

If some future operation explicitly depends on that checkpoint (export/reset), that operation is blocked pending repair.

## 9. Challenge: removing `valid_through_event_id` loses a convenient recovery cursor

### Attack

An event cursor makes it easy to say “checkpoint covers everything through event E” and to catch up later.

### Resolution

That statement is unsound globally:

- event identity/order does not total-order campaign/live/runtime/chronology domains;
- operational owners may have state not reducible to event coverage;
- live scope can advance independently;
- due temporal owners can remain active without one global event boundary.

If a later event/history projection needs its own coverage marker, it should use a domain-typed event-history field owned by that projection.

**Retire `valid_through_event_id` from generic checkpoint semantics.**

## 10. Challenge: removing `expected_commit_sha` makes a checkpoint impossible to bind to repository history

### Attack

A commit SHA is excellent immutable provenance and can support historical reset.

### Resolution

Embedding the containing commit SHA in content included in that commit is self-referential under Git content addressing.

Alternatives:

1. repository fetch context already identifies the revision from which a checkpoint was read;
2. support tooling may locate checkpoint introduction/history when necessary;
3. a checkpoint may record non-self-referential observed source identifiers/fingerprints where useful;
4. guaranteed historical reset, if ever required, needs a separate retention/source-reference design rather than a circular field.

**Retire `expected_commit_sha` from checkpoint payload.**

Do not create a second metadata commit solely to fill it in; that would add repository noise and weaken atomicity.

## 11. Challenge: checkpoint-local `world_time` is useful for resume presentation

### Attack

A checkpoint that says “Day 12, evening” is convenient for resume UI and temporal recovery.

### Resolution

Human-readable presentation metadata is fine, but it cannot adjudicate chronology or due work.

5.9 owns chronology persistence. Therefore 5.7 should not require checkpoint-local world time.

If later retained as presentation/diagnostic observation:

- explicitly non-authoritative;
- domain typed;
- never used in due/not-due or current-source selection.

Default candidate: remove from minimum checkpoint contract.

## 12. Challenge: active PC/thread/scene lists are cheap and useful

### Attack

Those lists let cold recovery jump directly to relevant state.

### Resolution

They are already at risk of duplicating current routing and still do not cover operational roots.

Candidate should not require them for correctness. They may survive as optional checkpoint observations only if implementation measurements justify acceleration.

Current source selection comes from current native routing at pinned authority, not from checkpoint lists.

## 13. Challenge: checkpoint engine identity may conflict with current MANIFEST runtime

### Attack

Which should recovery trust?

### Resolution

Current accepted campaign runtime identity from current campaign authority governs current ordinary recovery.

Checkpoint engine information is provenance/diagnostic evidence only. A stale checkpoint runtime does not force downgrade.

Open historical execution state may additionally require its own accepted interpretation context under Step 5.2/Step 3; that requirement is validated from the execution owner/evidence, not checkpoint's summary.

## 14. Challenge: current-authority-first cannot recover when current routing itself is corrupt

### Attack

A known-good older checkpoint might be the only path to recover a damaged current MANIFEST/routing record.

### Resolution

That is **repair**, not healthy ordinary recovery.

Ordinary recovery:

```text
current route broken -> block affected recovery scope + CANON_SUSPECT
```

Bounded repair may use:

- checkpoint evidence;
- current/nearby Git history;
- linked semantic events;
- other exact native evidence.

It must not silently substitute old checkpoint state as current authority.

After repair, a normal non-force corrective publication establishes new current authority.

This preserves `INTEGRITY.md` semantics.

## 15. Challenge: `READY | RETRY_REQUIRED | BLOCKED_*` proliferates status enums

### Attack

A separate enum per failure class becomes schema noise.

### Resolution / simplification

Use a compact recovery disposition plus typed reason:

```text
recovery_disposition:
    READY
    RETRY
    BLOCKED

reason_code / affected_scope / evidence
```

Examples:

```text
RETRY / SOURCE_MOVED
BLOCKED / REQUIRED_SOURCE_MISSING
BLOCKED / RUNTIME_UNAVAILABLE
BLOCKED / INTEGRITY_SUSPECT
BLOCKED / INTEGRITY_CORRUPT
BLOCKED / INTERPRETATION_UNRESOLVED
```

This need not be a persisted record; it may be a runtime result type.

Existing canon integrity status remains separate authority.

## 16. Challenge: `BLOCKED / REQUIRED_SOURCE_MISSING` versus `CANON_SUSPECT`

### Attack

A missing required current source is itself suspect canon, so why duplicate status?

### Resolution

Recovery disposition answers “may this process resume now?” Integrity answers “what is known about persisted canon?”.

They can co-occur:

```text
recovery = BLOCKED / REQUIRED_SOURCE_MISSING
integrity = CANON_SUSPECT(scope=S)
```

A runtime package unavailable case differs:

```text
recovery = BLOCKED / RUNTIME_UNAVAILABLE
integrity = CANON_OK
```

The distinction is useful and not duplicate authority.

## 17. Challenge: final currentness validation could re-read too much

### Attack

Revalidating every loaded file defeats bounded recovery performance.

### Resolution

Revalidate **authority selectors and root-membership/routing revisions**, not every immutable/loaded payload blindly.

If campaign ref and relevant live refs/routing generations are unchanged, exact pinned content hashes/revisions remain valid for that attempt.

If a selector moved, reload only affected routing/source/dependency partitions unless campaign movement invalidates the campaign-domain root basis broadly.

Implementation may optimize with revision/fingerprint evidence, but architecture does not require a new universal generation counter.

## 18. Challenge: campaign H movement could be proven disjoint and ignored, as in Step 5.6 conflict handling

### Attack

Always restarting on any H movement is conservative but expensive.

### Resolution

5.7 can permit a bounded disjointness optimization later, but SHOULD NOT require it initially.

Ordinary cold recovery is infrequent relative to turns. Simpler safe default:

```text
campaign anchor moved before writable release
    -> repin/re-resolve current campaign recovery basis
```

If profiling demonstrates material startup contention, a dependency-aware reuse optimization can be implemented while preserving the same semantics.

YAGNI favors correctness first.

## 19. Challenge: checkpoint creation with already-durable state is a prohibited no-op commit

### Attack

A metadata-only checkpoint commit changes no gameplay state.

### Resolution

It is not a no-op if checkpoint creation is independently requested/justified and creates meaningful recovery/diagnostic evidence.

However:

- do not create it merely because time passed;
- do not create/update checkpoint solely to refresh freshness timestamps;
- do not create it automatically on clean explicit save unless an independent checkpoint policy/request applies.

Thus no-heartbeat law remains intact.

## 20. Challenge: checkpoint creation alongside gameplay change cannot record exact containing commit

### Attack

This weakens historical reproducibility.

### Resolution

Accept the limitation rather than split publication into a second metadata commit.

The checkpoint can be part of the same coherent campaign tree transaction when independently required, but does not embed its containing commit SHA.

Repository history itself identifies the actual commits in which the descriptor exists.

If guaranteed exact historical source composition later becomes a product requirement, design a non-circular retention/reference mechanism explicitly.

## 21. Challenge: historical rollback is materially user-facing and therefore needs owner approval now

### Evidence

The current explicit consumer is `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`, itself a proposal, with `HDM_RESET_LAST_CHECKPOINT`.

No current canonical gameplay contract promises save-slot rewind/checkpoint rewind as a normal player feature.

### Resolution

Do not impose a guaranteed rewind product promise in 5.7.

Define only:

> Explicit historical maintenance MAY target an immutable checkpoint descriptor when its exact required historical native sources are still resolvable and compatible. Otherwise the operation fails truthfully.

This is a conservative technical interpretation of an internal maintenance command, not a product-semantic removal.

Reopen only if owner requests guaranteed rewind/retention.

## 22. Challenge: exact historical source can be discovered by scanning Git history, violating bounded recovery

### Resolution

Ordinary recovery never scans history for checkpoint source selection.

Maintenance/history operations have a different boundedness budget. They may use path-specific/short-range history where required by a diagnostic command, under `INTEGRITY.md` bounded repair principles.

Do not make broad history scan part of cold-start path.

## 23. Challenge: accepted unresolved Interaction/IntentPlan evidence may be raw text outside structured owners

### Attack

If exact user wording was irreducible recovery evidence and transcript is missing, recovery may be impossible even though checkpoint is valid.

### Resolution

Correct. Step 5.2 already states that promised accepted unresolved input must have durable resolvable evidence, be explicitly optional, or be deterministically rebuildable.

Checkpoint cannot summarize away this requirement.

Recovery blocks if the required accepted evidence is unavailable. Later transcript retention policy cannot retroactively delete irreducible evidence while it remains a recovery dependency.

## 24. Challenge: a checkpoint could safely copy Procedure/Continuation to make recovery independent of routing

### Resolution

Reject. That creates duplicate writable/current authority and risks divergence.

Checkpoint may reference/hint owner identities but native owner records remain sole state authority.

## 25. Challenge: checkpoint may be the easiest place to persist recovery root routing

### Resolution

Reject as primary routing owner.

Reasons:

- routing changes whenever native root lifecycle changes;
- checkpoints are sparse/optional;
- forcing checkpoint refresh on root enrollment would recreate high-churn snapshots;
- independent writable scopes require partitioned routing;
- one campaign checkpoint cannot atomically own all live-local root membership.

Typed native routing required by 5.2 remains the recovery membership source.

## 26. Challenge: current routing changes and checkpoint old routing differ — should that be suspicious?

Not by itself.

Checkpoint is historical/observational. Difference is expected after valid progress.

Suspicion arises only if current native routing/lifecycle are internally inconsistent or a current required reference is missing/contradictory.

## 27. Challenge: a newer campaign HEAD can reference an older live source intentionally

This is valid if owning contract says so. 5.7 must never assume “newest live branch commit” independently.

Recovery resolves **the current valid source under owning-scope rules**, not `max(commit time)` or `latest discovered branch`.

Step 5.8 will specify exact live epoch source selection/fencing.

## 28. Challenge: orphan live branch contains newer data than pointed branch

Do not adopt it automatically. Current durable routing determines authority. Orphan/newer-by-time is not current authority merely because it exists.

It may be repair evidence under bounded investigation.

## 29. Challenge: partial multi-domain publication creates a composition not represented by any checkpoint

Correct and expected.

Cold recovery composes actual current native sources. It does not require a checkpoint record proving the composition existed as one atomic cut.

RRC compatibility validation determines whether resume is possible.

If composed current sources are incompatible/incomplete, recovery blocks/retries according to owning contracts; it does not force rollback of the already-published domain.

## 30. Challenge: no checkpoint after explicit save surprises users

Step 5.5 already defines successful save by durable native source closure, not checkpoint creation. 5.7 cannot redefine that semantics.

User-facing save remains successful when required durable closure exists, even with zero checkpoint.

## 31. Challenge: checkpoint pointer update itself can race

It is a campaign-domain record and follows Step 5.6 single-ref CAS publication like any other campaign metadata.

If a campaign transaction creates a checkpoint and updates its pointer, both belong in one campaign tree/commit/ref transition.

A stale CAS attempt is rebuilt/revalidated; no separate pointer transaction required.

## 32. Challenge: checkpoint corruption could poison startup merely by being pointed

Ordinary recovery should not deserialize optional checkpoint before establishing that it is useful/required.

Safe pattern:

```text
pin current campaign H
load minimal current routing/identity
if checkpoint hint is useful:
    load/validate checkpoint
    if invalid:
        mark checkpoint metadata scope suspect
        continue current recovery if native RRC independent
```

This prevents optional stale metadata from becoming a single point of failure.

## 33. Challenge: checkpoint can only accelerate if it has some validation key

True, but 5.7 should avoid prematurely inventing a routing fingerprint field.

Potential implementation strategies include:

- source/path identity plus immutable object hashes;
- current routing revision native to the owning partition;
- exact source revision at which hint was observed;
- simply validating each hinted identity against current routing.

Choose during machine implementation based on actual routing representation and measured cost.

Architecture needs only the semantic rule: **unvalidated checkpoint hints never establish current membership/authority.**

## 34. Challenge: runtime identity in MANIFEST could itself change during recovery

Campaign ref movement catches campaign-domain MANIFEST changes. If H remains pinned/unchanged, the accepted campaign runtime identity at H is stable for the attempt.

Open execution may pin an older compatible interpretation context independently; validate both according to owner contracts.

## 35. Failure-mode matrix after challenge

| Scenario | Recovery disposition | Integrity consequence | Checkpoint role |
|---|---|---|---|
| no checkpoint, complete campaign-only routing | READY | OK | none |
| stale checkpoint, healthy newer current authority | READY | OK | ignore/historical |
| pointer missing but no checkpoint dependency | READY | checkpoint metadata may be suspect | none |
| pointed checkpoint malformed | READY if native RRC proven | checkpoint scope suspect | diagnostic only |
| required current owner missing | BLOCKED | affected scope SUSPECT | may aid diagnosis |
| ref moves during hydration | RETRY | no corruption implied | none |
| runtime package unavailable | BLOCKED | canon may remain OK | provenance hint only |
| accepted interpretation unresolved | BLOCKED | depends on evidence defect | cannot substitute |
| contradictory current owner records | BLOCKED | CORRUPT if confirmed | may aid repair only |
| post-publication local crash | recover current ref | OK if closure valid | stale pointer ignored |
| lost ACK, remote advanced | current ref contains advance | OK if closure valid | stale hint ignored |
| lost ACK, remote not advanced | old current ref | OK absent other defect | cannot invent lost HOT |
| partial multi-domain publication | compose actual native sources | validate scope-wise | no all-or-nothing cut |
| historical reset requested | maintenance validation | no current mutation until explicit corrective publication | possible target evidence |

## 36. Resulting recommendation

Refine the research direction to:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

Key decisions mechanically supported by prior canon:

1. current campaign authority anchors ordinary discovery;
2. current owning-scope routing selects participating native authorities;
3. each mutable source is exact-revision pinned per attempt;
4. typed native routing, not checkpoint, proves root membership;
5. checkpoint is optional immutable hint/diagnostic/maintenance evidence;
6. ordinary recovery may ignore checkpoint completely;
7. checkpoint absence/staleness/corruption does not block healthy independent RRC;
8. stale checkpoint never rolls current authority backward;
9. final writable release requires currentness/compatibility/integrity/RRC validation;
10. source movement causes bounded retry, not automatic canon suspicion;
11. recovery disposition is `READY | RETRY | BLOCKED` with typed reasons, separate from canon integrity status;
12. retire generic `valid_through_event_id` and self-referential `expected_commit_sha`;
13. checkpoint-local world time and active lists are not required recovery authority;
14. guaranteed historical rewind is not a default checkpoint invariant;
15. checkpoint/root-routing machine realization remains deferred implementation work.

## 37. Owner decision gate assessment

No blocking owner-level decision emerged.

The only plausible product-semantic question is guaranteed historical rewind. Current canonical gameplay does not promise it, and the current consumer is a proposal-level maintenance command. Therefore the conservative architecture is to support historical maintenance only when exact retained native sources make it truthful.

If a future product requirement explicitly promises rewind slots/checkpoint rollback, reopen retention/history guarantees then.

Proceed to candidate specification and adversarial review without an owner approval gate for technical mechanics.