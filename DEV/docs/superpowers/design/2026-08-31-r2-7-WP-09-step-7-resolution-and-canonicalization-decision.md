# R2.7 WP-09 Step 7 — Resolution and Canonicalization Decision

Status: **STEP 7 COMPLETE — CANONICALIZATION REQUIRED**

## Resolution

The repaired candidate contains a durable implementation-facing allocation that is
not merely audit evidence:

- existing full CORE cache is operational support and must remain distinct from
  a profile-scoped role-context packet;
- current compact routing surfaces may seed discovery but cannot become source
  authority, currentness or eligibility proof;
- profile-owned, runtime-local packet control must use one conservative
  no-hidden-telemetry allocation path and terminal one-alternative fallback;
- current machine vocabulary/tests are supporting only and conformance is
  behavioral.

Each statement preserves existing R2.3/R2.4/R2.6/WP-08 semantics, but together
they provide a stable realization boundary future implementation must obey.
Leaving that allocation only in Step-5/6 design artifacts would make accepted
implementation-facing law non-canonical.

**Decision: create one concise canonical realization specification in Step 8.**

## Canonicalization scope

The Step-8 specification shall:

1. restate only the realization allocation and its direct behavioral acceptance
   boundaries, referring to R2.3/R2.4/R2.6/WP-08 as semantic owners;
2. declare runtime-local/ephemeral no-representation for role context/bundle/
   trace/source-basis/estimator control;
3. retain non-authoritative cache/current/index and MechanicalContext boundaries;
4. state terminal exactly-one-alternative fallback;
5. keep physical roots, topology, HOT/SQLite, numeric scale, broader failures
   and implementation planning out of scope.

It shall not copy the evidence tables or create a new schema/catalog/runtime
change.

## Typed obligations

| ID | Classification | Owner / trigger | Obligation |
|---|---|---|---|
| WP-09/F01 | IMPLEMENTATION_OBLIGATION | future approved implementation cycle | Realize registered profile -> bounded discovery/closure -> currentness/eligibility -> floors/optional allocation -> outcome as runtime-local behavior. |
| WP-09/F02 | VERIFICATION_OBLIGATION | future approved implementation/release cycle | Prove all C-WP09-6 acceptance probes, including terminal fallback and no hidden token telemetry. |
| WP-09/F03 | FORWARD_OBLIGATION | WP-10, only if a concrete realization needs durable roots/templates | Decide record/template delta without making control artifacts durable by default. |
| WP-09/F04 | SAFE_DEFERRED | WP-11 | Revisit physical partition only on the R2.3 measured trigger. |
| WP-09/F05 | SAFE_DEFERRED | WP-12 | Realize any cache/HOT/SQLite operation while preserving authority classification. |
| WP-09/F06 | SAFE_DEFERRED | WP-18/WP-24/WP-25 | Register Story consumers, numeric evaluation, and broad failure semantics under their own owners. |

## Decision gate

No product-owner, architecture-owner, authority, compatibility, risk or scope
choice remains. Proceed to Step 8, then stop for mandatory Senior audit.
