# Step 3 Final Critical Review — Deterministic Execution Boundary

Status: **FINAL CRITICAL REVIEW — NO UNRESOLVED STEP-3 BLOCKER / CLOSURE SUBJECT TO FINAL SAME-HEAD VERIFICATION**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed authority chain:

- `2026-08-19-step-3-execution-boundary-task-brief.md`
- `2026-08-19-step-3-execution-boundary-research-draft.md`
- `2026-08-19-step-3-execution-boundary-decision-brief.md`
- `2026-08-19-step-3-execution-boundary-candidate-spec.md`
- `2026-08-19-step-3-execution-boundary-adversarial-review.md`
- `2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `../plans/2026-08-19-step-3-execution-boundary-machine-contract.md`

Owner-approved architecture: **Alternative C**.

This review is the Step-3 roadmap exit-gate challenge. It tests whether the canonical execution ownership model is coherently represented by the current machine contracts and whether any unresolved issue must keep Step 3 open.

## 1. Verdict

```text
BLOCKER findings       0
FIXED findings         4
LATER-OWNER findings   5
ARCHITECTURE DEBT      1 non-authoritative historical-doc cleanup
```

Recommendation:

> **CLOSE Step 3 after the final documentation/status HEAD passes the same full maintenance + unit-test CI. Advance Step 4.**

Confidence: **HIGH**.

No new human architecture decision is required.

## 2. Canonical ownership graph re-check

The machine contract preserves the approved responsibility split:

```text
Interaction
    -> IntentPlan
        -> executable IntentClause
            -> RuntimeCommand
                -> ActionRequest -> Resolution(Activity)
                OR
                -> TransitionRequest -> direct deterministic execution

RuntimeCommand
    root mandatory execution-chain closure owner

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded ExecutionSegment(s)
        -> atomic committed state/runtime edge
        -> MechanicalEvents
        -> receipts/idempotency
        -> mandatory child descriptors

Continuation
    suspended Resolution generation
    references Procedure; never owns Procedure state
```

No `runtime.execution_segment`, `runtime.resolution_chain`, scheduler, job or generic workflow class has been introduced.

Disposition: **ASSURED**.

## 3. IntentPlan non-atomicity

Machine evidence:

- `runtime-intent-plan-state.schema.json` owns only Interaction linkage + bounded clauses;
- `intent-clause.schema.json` owns one clause and at most one narrow forward guard;
- focused tests accept two executed clauses followed by a failed third clause;
- closed schemas reject plan-level world delta, RNG, procedure-resource and transaction authority.

The plan therefore cannot become a hidden all-or-nothing mechanical transaction.

Disposition: **ASSURED**.

## 4. RuntimeCommand root closure

Machine evidence:

- `runtime-command-state.schema.json` separates `action` from `transition`;
- action requires a root Resolution; transition requires its direct typed request and cannot masquerade as an Activity Resolution;
- dispositions are closed as `command.accepted` / `command.settled`;
- a settled command cannot contain pending mandatory child descriptors;
- integrated Case M keeps an execution-limit child under an accepted root command instead of silently dropping it.

This is sufficient to represent the canonical root-chain closure rule without a ResolutionChain entity.

Disposition: **ASSURED**.

## 5. Procedure sole ownership

Machine evidence:

- `runtime.procedure` is a registered runtime class with stable campaign-scoped identity;
- `runtime-procedure-state.schema.json` owns participant -> Resource -> `spent` state;
- stored capacity is schema-rejected for procedure resources;
- Resolution and Continuation can reference `procedure_id` but closed schemas reject procedure state copies;
- integrated Case K represents a reaction child under the same Procedure after procedure Resource spending.

No writable duplicate exists across Encounter, Resolution, Continuation or checkpoint representations.

Disposition: **ASSURED**.

## 6. ExecutionSegment atomic boundary

`execution-segment.schema.json` is an embedded committed execution value rather than an independent runtime entity. It carries:

- stable owner-local sequence;
- committed Event identities;
- mandatory child descriptors;
- typed exports;
- affected revision references;
- optional Continuation reference.

It cannot embed arbitrary world-state snapshots.

The implementation invariant remains that world/procedure/RNG/execution/Event/idempotency updates belonging to one segment commit in one local transaction. Physical SQLite implementation is intentionally not fabricated in this architecture repository stage.

Disposition: **ASSURED**.

## 7. MechanicalEvent and mandatory post-commit work

Machine evidence:

- `runtime-mechanical-event-state.schema.json` requires `segment_id + event_ordinal` identity, root command and causal reference;
- payload equality is explicitly not Event identity;
- committed segments can atomically carry mandatory child invocation descriptors;
- pending child descriptors require firing key, root command, Activity and triggering occurrence/Event reference.

One cross-field membership rule cannot be expressed by ordinary JSON Schema alone:

```text
pending_child.trigger_ref must refer to the triggering Event/occurrence selected for that committed execution edge
```

This remains a runtime transaction validation invariant and is explicitly tested/documented rather than falsely claimed as JSON-Schema enforcement.

Disposition: **ASSURED / IMPLEMENTATION INVARIANT EXPLICIT**.

## 8. Reaction/choice suspension and recomputation

Machine evidence:

- Continuation generation is positive and independently identifiable;
- reaction offers contain stable offer/responder identity plus a nonempty bounded Activity candidate set;
- choice offers contain nonempty bounded option IDs;
- fixed RNG, prior exports, dependency frontier, expected child refs and future RNG frontier are portable;
- cached MechanicalContext, Temporal Agenda, prospective deltas and Procedure state copies are rejected;
- unconsumed time-advancement remainder is explicit and positive;
- child Resolution without player initiating command requires stable causal invocation key.

The canonical resume rule therefore remains representable:

```text
consume expected child receipt
re-pin frontier
re-read Procedure
rebuild MechanicalContext
recompute safe phase
preserve fixed historical RNG/choice inputs
```

Disposition: **ASSURED**.

## 9. Retry/idempotency and catalog-context barrier

Machine evidence:

- RuntimeCommand stores `catalog_context_fingerprint` and `input_fingerprint`;
- Continuation stores the accepted catalog-context fingerprint;
- execution failures include idempotency conflict and catalog-context incompatibility;
- integrated Cases G and L cover stable accepted fingerprints and typed incompatible-context failure.

The canonical algorithm still requires identity lookup against stored accepted context before ambient rebind. That algorithm is a future runtime implementation responsibility, not duplicated into schema.

Disposition: **ASSURED**.

## 10. LLM authority boundary

Machine evidence:

- `invocation-fact.schema.json` requires explicit boolean value and stable adjudication provenance;
- missing and false are structurally different;
- `mechanical-surfaces.json` continues to register which facts/selectors may consume invocation-adjudicated input;
- Step-2 state-sensitive selectors remain `ENGINE_STATE` only;
- arbitrary engine-owned facts are not given a generic command-state escape hatch.

The LLM remains semantic interpreter/adjudicator of explicitly permitted fiction-dependent inputs, not mechanical state authority.

Disposition: **ASSURED**.

## 11. Effect recency without history retention

Machine evidence:

- live `world.effect` may own positive integer `application_order_key`;
- `entity-structures.json` exposes that compact field;
- no `created_at`, recency timestamp or global-order authority is introduced;
- integrated Case N proves arbitration evidence is representable without trace body.

Canonical allocation remains target/application-family-local over the complete nonterminal candidate set. Refresh preserves the episode ordinal; replace/new episode receives a new one.

Disposition: **ASSURED**.

## 12. Boundary / same-coordinate / scheduled-trigger execution

Machine evidence:

- `boundary-occurrence.schema.json` has stable producer/scope/occurrence/causal identity;
- Continuation can retain an explicit unconsumed advancement remainder;
- scheduled owner-local due work uses an ordinary pending child/Resolution firing key;
- no scheduler/job entity or privileged callback surface was added.

Exact noncommutative same-time order continues to require registered rule semantics or typed `failure.order_adjudication_required`; SQL/list order is not gameplay authority.

Disposition: **ASSURED**.

## 13. Failure vocabulary consistency

### FIXED finding F1 — unregistered `BLOCKED` state

An intermediate TDD expectation used receipt status `BLOCKED`, which was not present in the closed `resolution_states` registry. Adding it would have created an unnecessary extra state/catalog-version change.

Resolution:

- keep existing registered `FAILED`/other terminal/suspension states;
- express the cause through the typed `failure.*` code;
- receipt schema now rejects a failure code paired with `COMPLETED`.

This is simpler and avoids duplicate state/cause axes.

Disposition: **FIXED**.

## 14. Machine-catalog coherence

### FIXED finding F2 — Step-3 catalog vocabulary

Catalog version advanced coherently to `1.4.0` when Step-3 protocol/failure IDs were admitted.

All machine catalogs now share `1.4.0`:

- `core-catalog.json`;
- `entity-structures.json`;
- `identifier-policies.json`;
- `mechanical-surfaces.json`.

### FIXED finding F3 — audit did not enforce all four catalogs / Step-3 schemas

The maintenance audit now:

- requires the complete Step-3 schema set;
- validates `mechanical-surfaces.json` against its schema;
- includes all four machine catalogs in the version-coherence barrier.

Disposition: **FIXED**.

## 15. Integrated A–N cases

`DEV/TESTS/test_step3_execution_examples.py` covers representability of:

```text
A ordinary action
B reaction suspension
C atomic post-commit follow-up descriptor
D partial IntentPlan completion
E direct deterministic transition
F clarification/no-command outcome
G stable retry fingerprints
H portable suspended closure without caches
I BoundaryOccurrence identity
J scheduled due child firing key
K shared Procedure / no state copy
L incompatible catalog-context failure
M execution-limit pending child preserved under open root command
N Effect recency without trace history
```

All A–N cases pass on the pre-closure machine HEAD together with the full maintenance audit and full unit suite.

Disposition: **ASSURED**.

## 16. Documentation/version drift

### FIXED finding F4 — normative inventory version

`DEV/ARCHITECTURE/CATALOG_INVENTORY.md` is updated to catalog version `1.4.0` and now reflects the Step-3 runtime/protocol boundary.

### ARCHITECTURE DEBT D1 — historical derivation documents

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` contain older explanatory examples/version labels that predate the current canonical Step-2/3 contracts.

They are explicitly non-normative relative to:

- `CATALOG_INVENTORY.md`;
- machine catalogs/schemas;
- the Step-2 canonical assurance chain;
- this Step-3 canonical specification.

Cleanup/supersession warning remains documentation debt. Implementation MUST NOT infer current IDs/ownership from those older examples.

This debt is not a Step-3 blocker because no machine/runtime authority depends on it.

## 17. Later-owner findings

### L1 — lore / truth / disclosure authority — Step 4

Invocation facts influencing one execution do not automatically become durable lore. Step 4 must define truth promotion and knowledge/disclosure authority.

### L2 — transcript / SemanticEvent / Chapter transformation — Step 4

The architecture intentionally keeps:

```text
Transcript/runtime.message
SemanticEvent
world.chapter
```

as separate narrative representations, with MechanicalEvent as the technical committed layer beneath semantic history. Step 4 owns factual projection/authoring semantics.

### L3 — spectator-safe public history projection — Steps 4–5

A public viewer/guest surface must not expose private campaign secrets merely because they exist in private Git storage. Step 4 owns visibility semantics; Step 5 owns publication/transport shape.

### L4 — repository checkpoint publication/restoration — Step 5

Step 3 defines portable continuity payload sources; Step 5 owns Git publication/restoration, shared revisions and cleanup.

### L5 — full rules seed / simultaneous-order proof — Step 6

Concrete D&D seed review may prove a specialized same-time policy or additional execution vocabulary. Such extension requires a concrete rules case; the generic engine does not speculate now.

## 18. Final exit-gate assessment

Step-3 exit criteria are satisfied at the architecture/machine-contract level:

- multiple intents and partial completion: covered;
- distinct Activity/Transition paths: covered;
- Procedure-local ownership: covered;
- segment atomicity contract: covered;
- reactions/choices/suspension/resume: covered;
- retries/idempotency identity: covered;
- mandatory trigger chains and limits: covered;
- deterministic receipt/Event identity: covered;
- LLM/core binding boundary: covered;
- in-flight recovery source contract: covered;
- focused A–N cases: covered;
- adversarial review: covered;
- catalog/schema/audit alignment: covered.

No unresolved Step-3 blocker remains.

## 19. Closure condition

After this review plus roadmap/status updates are on the branch, run fresh verification on that exact final HEAD:

```text
DEV/TOOLS/run_maintenance_audit.py
full DEV unit suite
GitHub Actions: Validate engine source
```

If the final same-head workflow concludes `success`, Step 3 is closed and Step 4 becomes the sole `IN PROGRESS` numbered stage.

Human decision required: **NO**.
