# S6D-12 — Adversarial Final Closure — Step 5 Candidate Final-Closure Specification

Status: **STEP 5 CANDIDATE SPECIFICATION — COMPLETE / READY FOR WHOLE-PROJECT CRITIC**

Date: 2026-08-28

Candidate base ref: `493b05108d698f6fe3520bc05bab273becf09b59`

## 1. Scope

This candidate specifies the exact final S6D closure law and the finite evidence required before R2.7 may resume. It preserves the current S6D-01…11 semantic owners and the approved B′ physical-realization decision.

It does not declare current machine PASS, implement the open realization work, broaden product scope, activate dormant mechanics, change package identity, or pull later implementation acceptance into architecture closure.

## 2. Final closure state machine

S6D-12 owns no new runtime state. These are review/closure predicates only:

```text
SEMANTIC_ARCHITECTURE_RECONCILED
MACHINE_REALIZATION_VERIFIED
S6D_FINAL_CLOSURE_AUTHORIZED
```

Candidate law:

```text
SEMANTIC_ARCHITECTURE_RECONCILED == true
    iff
      no current S6D obligation has an undispositioned SEMANTIC_ARCHITECTURE blocker
      and no duplicate current semantic authority exists
      and stale/superseded current-authority wording has been reconciled to controlling owners

MACHINE_REALIZATION_VERIFIED == true
    iff
      B′ is coherently materialized
      and every current derived package/set identity projection equals fresh canonical reconstruction
      and Mechanical-Null executable conformance evidence passes
      and the focused current S6D-07/08/09/10/11 closure suite passes on that same realized state

S6D_FINAL_CLOSURE_AUTHORIZED == true
    iff
      SEMANTIC_ARCHITECTURE_RECONCILED == true
      and MACHINE_REALIZATION_VERIFIED == true
      and no current blocker remains undispositioned
```

R2.7 resume law is unchanged:

```text
R2.7_WP06_RESUME_ALLOWED == S6D_FINAL_CLOSURE_AUTHORIZED
```

No architecture-review PASS may substitute for `MACHINE_REALIZATION_VERIFIED`.

## 3. Preserved semantic architecture

Final closure SHALL preserve without reopening:

1. S6D-01 manifest -> package snapshot -> exact dependency-closed resolved lock -> `ruleset_set_sha256` as the sole canonical package/set identity chain.
2. S6D-02 admission accounting and registration-vs-execution separation.
3. S6D-03 finite selectable selector/operation surface.
4. S6D-04 distinct MechanicalContext surfaces and fail-closed bound-DAG law.
5. S6D-05 portable values as embedded nonowners with no generic expression/query/path/patch language.
6. S6D-06 finite active primitive set with `op.roll` as sole RNG owner.
7. S6D-07 READY_PC as a deterministic commitment frontier over natural owners and accepted catalog context.
8. S6D-08 distinct health/effect/resource/procedure/chronology owners, bounded due processing and retry law.
9. S6D-09 exact three-source completeness union and one semantic coverage ledger.
10. S6D-10 typed House-Rules/adjudication boundary with no prose execution authority.
11. S6D-11 package machine closure, registered validator gate and complete changed-set additive compatibility proof.
12. existing execution, persistence, retention, recovery, source-routing, access-control and adoption owners followed by those S6D contracts.

## 4. Required semantic/evidence reconciliation

### C-01 — S6D-08 stale identity wording

Before `SEMANTIC_ARCHITECTURE_RECONCILED` becomes true, the final Machine Owner paragraph in `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` SHALL stop describing a two-file/per-file/aggregate-content-set identity as current authority.

The narrow replacement SHALL point to the current package manifest/snapshot/resolved-lock/set chain and the bounded S6D-08 seed member without changing health/effect/recovery semantics.

No new digest, owner or S6D-08 identity algorithm is permitted.

## 5. Required machine-realization closure

### MRC-01 — B′ coherent v2 -> v3 coverage realization

The realization SHALL be one coherent change set.

Required physical result:

```text
DEV/CATALOG/domain-rules-coverage.json
    one semantic coverage artifact
    schema version 3
    no package binding members

DEV/CATALOG/domain-rules-coverage-binding.json
    closed strictly-derived companion
    exactly:
      profile_id
      package_id
      package_version
      catalog_generation
      gameplay_spine_member
      package_content_sha256
      ruleset_set_sha256
```

Required implementation properties:

- coverage schema v3 removes package binding completely;
- a closed binding schema admits exactly the seven approved fields and no extras;
- deterministic production is split into semantic coverage production and derived binding production;
- semantic coverage production does not acquire a substitute semantic digest;
- validation fails closed unless the checked-in semantic artifact exactly equals the fresh deterministic semantic producer;
- validation fails closed unless the checked-in binding exactly equals fresh derivation from the expected profile/package/version/catalog/member context and the canonical S6D-11 package snapshot/resolved lock;
- the S6D-11 registered S6D-09 validator remains the integration authority; no second validation authority is introduced;
- the large semantic artifact is regenerated by the normal deterministic producer, not manually reconstructed or sharded.

### MRC-02 — all current identity projections synchronized

Fresh canonical reconstruction SHALL be performed on the realized ref. Every semantically current package/set projection SHALL agree with it in one coherent publication.

The known current carrier set includes at least:

- READY_PC fixture evidence;
- `DEV/CATALOG/ruleset-package-closure.json`;
- the new domain-rules coverage binding;
- `DEV/CATALOG/house-rules-mechanical-boundary.json`;
- focused S6D-08 current identity golden evidence;
- focused S6D-11 current identity golden evidence.

Current owner/consumer inspection at implementation time SHALL determine whether the verified ref contains any additional semantically current projection. Schema examples, nullable scaffolds, historical evidence and illustrative literals are not projections merely because they resemble hashes.

Partial synchronization is forbidden.

### MRC-03 — Mechanical-Null executable conformance

For each admitted generic resolution family (`activity.check.generic` and `activity.save.generic`), focused deterministic evidence SHALL execute the existing route and prove:

- accepted fixed inputs/RNG are deterministically resolved;
- authoritative world mutation is absent and affected world revision count is zero;
- the selected genuine resolution event (`event.check.resolved` or `event.save.resolved`) exists as required by the existing primitive/route owner;
- a valid existing resolution receipt links the accepted outcome/evidence;
- identical retry reuses accepted evidence without reroll or duplicate authoritative outcome;
- same idempotency key with changed accepted fingerprint fails closed;
- missing/invalid required input cannot fabricate mutation, event or success receipt.

No Mechanical-Null subsystem, synthetic StateDelta lifecycle or new event/receipt authority may be added merely to satisfy the test.

### MRC-04 — focused integrated verification

On the same final realized ref, fresh evidence SHALL include:

1. canonical package snapshot and `ruleset_set_sha256` reconstruction;
2. expected-vs-current projection comparison with zero mismatch;
3. focused S6D-07 verification;
4. focused S6D-08 verification;
5. focused S6D-09 verification, including B′ and Mechanical-Null conformance;
6. focused S6D-10 verification;
7. focused S6D-11 integrated package-closure verification;
8. diagnostic maintenance audit for stale derived-current identity literals/projections.

A newly red unrelated test is recorded separately and is not auto-fixed as part of S6D-12.

## 6. Deferred and negative-space dispositions

The following do not block S6D final architecture closure when their current disposition remains unchanged:

```text
production behavioral/playability/performance proof  -> IMPLEMENTATION_ACCEPTANCE_DEFERRED
released incompatible-campaign migration             -> FUTURE_NOT_DUE / R2.7 WP-20
nonselectable/quarantined mechanics                   -> DORMANT_WITH_TRIGGER
broad unsupported rules corpora                       -> OUT_OF_CURRENT_SCOPE
schema example hash literals                          -> NONAUTHORITATIVE_EXAMPLE
```

Coverage does not activate any of them.

## 7. Forbidden closure shortcuts

Final closure SHALL fail rather than:

- infer current identity from checked-in displayed hashes;
- accept five-of-six or other partial current-projection repair;
- keep volatile package binding inside semantic coverage;
- introduce `coverage_semantic_sha256` or equivalent;
- shard the coverage ledger;
- weaken S6D-11 canonical identity;
- manually reconstruct the generated coverage artifact to bypass missing execution capability;
- use CI/log output as an ad-hoc generated-artifact transport;
- claim Mechanical-Null conformance from route metadata alone;
- fabricate a mutation/event merely to satisfy an assertion;
- broaden package/product semantics to make an unsupported route look covered;
- resume R2.7 while either required closure predicate is false.

## 8. Step-8 acceptance record

Step 8 SHALL record the predicates explicitly.

Successful form:

```text
SEMANTIC_ARCHITECTURE_RECONCILED: TRUE
MACHINE_REALIZATION_VERIFIED: TRUE
S6D_FINAL_CLOSURE_AUTHORIZED: TRUE
R2_7_WP06_RESUME_ALLOWED: TRUE
```

If machine realization remains unavailable or any required verification fails:

```text
SEMANTIC_ARCHITECTURE_RECONCILED: <true only if independently proved>
MACHINE_REALIZATION_VERIFIED: FALSE
S6D_FINAL_CLOSURE_AUTHORIZED: FALSE
R2_7_WP06_RESUME_ALLOWED: FALSE
S6D_FINAL_CLOSURE: BLOCKED_BY_KNOWN_REALIZATION_OBLIGATION
```

The blocked form is an honest Step-8 disposition, not permission to weaken the gate.

## 9. Candidate disposition

```text
STEP 5: COMPLETE
SEMANTIC DIRECTION: SINGLE / DERIVED FROM ACCEPTED OWNERS
CURRENT MACHINE PASS CLAIM: NONE
OPEN MACHINE CLOSURE ITEMS: MRC-01, MRC-02, MRC-03, MRC-04
STALE-EVIDENCE RECONCILIATION: C-01
HUMAN DECISION REQUIRED: NO
NEXT: STEP 6 — MANDATORY WHOLE-PROJECT ADVERSARIAL CRITIC
```
