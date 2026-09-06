# R2.7 WP-21 Step 1 — Independent Senior Review

Status: **HOLD — BOUNDED STEP-1 RECOVERY REQUIRED**

Date: 2026-09-06

Reviewed worker checkpoint: `0db29e365434512c0d35442109f5ba60ecb007ab`.

Reviewed package:

- `DEV/docs/superpowers/design/2026-09-06-r2-7-WP-21-task-brief-source-manifest.md`;
- the Step-1 repairs and current owners referenced by that package;
- current process/current-progress/project-map routing;
- directly relevant maintenance, access-control, disclosure, cleanup and late WP-17/WP-18 owners.

Domain: **Diagnostics, observability, cleanup and retirement**.

This is the mandatory independent Senior review stop after WP-21 Step 1. It does not authorize Step 2, WP-22, implementation planning or substantive implementation.

---

## 1. Senior verdict

```text
WP21_STEP1_SENIOR_REVIEW: HOLD
STEP1_RECOVERY_REQUIRED: YES
STEP2_AUTHORIZED: NO
WP22_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
HUMAN_DECISION_REQUIRED_NOW: NO
```

The WP-21 direction is sound: reconciliation should dominate invention; no generic observability subsystem, universal GC graph/frontier, new repair authority or new support/admin authority should be created merely because the domain overlaps them.

The worker also correctly detected and repaired the conflict between the old optional physical-ref cleanup assumption and fixed Product Owner policy. That repair is not reopened by this HOLD.

The HOLD is caused by insufficient whole-project coverage proof for the remaining WP-21 questions, not by a rejection of the WP-21 architectural direction.

---

## 2. Findings

### SR21-01 — BLOCKER — Step-1 Source Manifest does not satisfy the mandatory machine-realization/consumer route

The current Step-1 Source Manifest is dominated by canonical specifications. That is insufficient for this WP because both the generic evidence gate and the HDM whole-project critic gate require actual owners plus implicated runtime consumers, schemas, tests, support contracts and tooling where they can change the conclusion.

`DEV/PROJECT_MAP.md` explicitly routes **Support / diagnostics / maintenance** through:

- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`;
- `DEV/TOOLS/run_maintenance_audit.py`;
- `DEV/TOOLS/audit_engine.py`;
- neighboring session/integrity/storage/persistence/checkpoint schemas/tests.

The same map routes persistence/recovery through current `GAME/CORE` owners and their schemas/tests.

The published Step-1 manifest does not account for that machine/runtime/support subgraph deeply enough to support broad `SATISFIED` conclusions for diagnostics, repair or support safety.

#### Required recovery

Expand the WP-21 Source Manifest and evidence matrix from the current project map to the directly and indirectly relevant realization surfaces. At minimum, inspect and disposition the implicated:

- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` support contract;
- maintenance/audit tooling under `DEV/TOOLS/`;
- relevant `GAME/CORE` persistence/session/integrity/recovery/live/multiplayer consumers;
- relevant runtime/development schemas and executable tests;
- stale/debt markers already routed by accepted WPs where they affect a WP-21 claim.

For each materially relevant machine/runtime surface, record one explicit disposition such as:

```text
CONFORMS
STALE_DEBT_ALREADY_ROUTED
GAP_REQUIRING_STEP1_REPAIR
NO_MACHINE_REPRESENTATION_REQUIRED
NOT_APPLICABLE
```

A whole-project `SATISFIED` claim must not rely only on the prose owner when a current machine/support consumer exists.

---

### SR21-02 — SIGNIFICANT — maintenance/debug authorization and disclosure safety are asserted, not proven

`DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` remains an **INTERNAL CONTROL CONTRACT / PROPOSAL** and defines powerful support surfaces including:

- `HDM_EXPORT_CURRENT_LOG`;
- `HDM_EXPORT_CHECKPOINT_LOG`;
- `HDM_RESET_LAST_CHECKPOINT`.

The current text establishes exact-token routing and says exported material must exclude credentials, hidden instructions and chain-of-thought. However, exact-token recognition answers **what operation is requested**; it does not by itself prove **which principal is authorized to perform it** or **which diagnostic payload is eligible for that recipient**.

Current accepted owners already impose stronger boundaries:

- repository permission alone is not semantic/application authorization;
- explicit access/global maintenance is owner/creator-scoped under `DEV/ARCHITECTURE/ACCESS_CONTROL.md`;
- Step 5.12 forbids maintenance/debug/auxiliary surfaces from intentionally carrying campaign information ineligible for the recipient;
- diagnostics/export projection never becomes gameplay or recovery authority.

The Step-1 package therefore cannot mark the support-surface route `SATISFIED` until this composition is explicitly demonstrated against the real maintenance surface.

#### Required recovery

Determine from current owners whether the maintenance contract can be reconciled mechanically without a new architecture owner. The expected conservative composition is:

```text
exact maintenance token
    -> operation routing only
    != authorization

sensitive/global maintenance operation
    -> current creator/owner authorization as required by existing access-control owners

export payload
    -> current disclosure/information eligibility for the authorized recipient
    -> no hidden CoT / hidden instructions / credentials / unavailable host context

maintenance output
    -> diagnostic projection only
    -> never gameplay/recovery authority
```

If current owners settle this unambiguously, repair the affected Step-1 framing/derivative contract(s) mechanically and add/route regression evidence as appropriate. Do **not** create a generic support/admin privilege subsystem.

Escalate to Product Owner only if recovery exposes a genuine unresolved product choice, for example an intentional non-owner support principal that should receive owner-level diagnostics. No such human decision is established by this review itself.

---

### SR21-03 — SIGNIFICANT — obsolete/terminal record-family coverage is not item-level complete

WP-21 asks whether cleanup/retirement is mapped for **all record families that can become obsolete**. Step 5.13 supplies the generic owner-gated cleanup law, but it predates later R2.7 families and explicitly requires new consumer classes to enroll before accepted durable dependence may rely on cleanup semantics.

The current Step-1 package infers broad coverage from Step 5.13 without an item-level census of later families.

Concrete late examples that must be accounted for include, at minimum:

- WP-17 `runtime.collaboration_obligation`, whose generations can become terminal `RESOLVED` / `OBSOLETE` and whose PLAYER routing companions are removed at terminal transition;
- WP-18 retained multiplayer Dramaturg horizons and player-local/shared planning generations, which are noncanonical, may become stale/incompatible/inactive and may be recomputed, discarded, retained or selectively rebased under their native owner.

This does **not** imply that either family needs automatic deletion or a new GC subsystem. `RETAIN`, `NO AUTOMATIC RETIREMENT`, native-owner replacement, recomputation, or an existing compatible cleanup contract may all be valid dispositions.

#### Required recovery

Create a finite item-level WP-21 retirement/rebuild census for relevant obsolete/terminal/replaceable families, especially those introduced after Step 5.13.

For each family record at least:

```text
family / representation
native owner
terminal / obsolete / stale condition
currentness basis
retirement disposition
cleanup-contract / protection-routing requirement, if any
survivor / rebuild / recompute obligation
machine realization status
```

Where no automatic cleanup contract is admitted, say so explicitly and preserve Step-5.13's fail-safe bias:

```text
uncertain cleanup eligibility -> RETAIN
```

Do not manufacture current work from a future revisit condition and do not infer physical branch/ref deletion from semantic retirement. PO-006 remains fixed: HDM never deletes Git branches/refs.

---

## 3. Findings that remain accepted

The following worker findings remain valid and are not reopened:

```text
F21-01: physical branch/ref deletion assumptions conflict with fixed PO policy
         -> repaired through logical de-authorization/de-routing semantics

F21-02: stale R1 review-status metadata
         -> repaired as status-only synchronization
```

The Senior HOLD does not authorize wholesale reopening of Step 5, WP-16, WP-17, WP-18, WP-20 or another closed block. A closed owner is changed only if the expanded evidence proves an actual contradiction, unsatisfied consumer or insufficiency.

---

## 4. PASS conditions for Step-1 recovery

A repaired WP-21 Step-1 package is ready for Senior re-review only when all are true:

```text
[ ] SR21-01 machine/runtime/support dependency subgraph is explicitly covered.
[ ] Relevant owners, consumers, schemas, tests and tooling have item-level dispositions.
[ ] SR21-02 maintenance authorization + disclosure composition is proven or a real residual human decision is isolated.
[ ] SR21-03 obsolete/terminal/replaceable family census is complete enough to support the all-family coverage claim.
[ ] Existing F21-01/F21-02 repairs remain reconciled and are not regressed.
[ ] No generic observability/GC/support-authority subsystem is invented without evidence.
[ ] PO-006 branch/ref deletion prohibition remains absolute.
[ ] Version Impact is re-evaluated for any actual semantic/machine repair made during recovery.
[ ] Exact-head verification is recorded for the repaired checkpoint.
```

After the worker publishes the repaired Step-1 package, stop again for mandatory independent Senior re-review.

---

## 5. Version Impact

This Senior review artifact changes review/status provenance only.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
```

No GAME runtime module, persistent/protocol schema, engine release identity, campaign/storage/catalog generation, ruleset identity or compatibility-bearing namespace is changed by this review itself.
