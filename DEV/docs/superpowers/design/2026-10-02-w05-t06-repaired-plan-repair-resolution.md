# W05.T06 Repaired Plan — Targeted Repair Resolution

Status: **REPAIRED PACKAGE CANDIDATE — FINAL SENIOR PLAN RE-REVIEW REQUIRED**

Date: 2026-10-02
Repair basis: `5830fcca01fa4f2bc2231ed50254e4b6f680dad8`

This is planning provenance, not a second executable plan. The only executable
route remains the stable Wave-05 plan plus implementation-plan index.

## Senior findings

### SP06-01 — ordinary Master / Commentator eligibility

Resolved. P3 no longer imports PO-012's Commentator formula. Ordinary Master
uses current gameplay subject + active PLAYER/control and source/aspect-specific
native knowledge/disclosure/access eligibility. Epistemic stance is preserved;
belief/suspicion never becomes objective fact. PO-012 remains separate
Commentator regression coverage.

### SP06-02 — accepted HOT producer/admission join

Resolved by making the WP12 establishment/adoption boundary explicit.

NativeHotStore/CurrentOwnerView trusts no raw row from gameplay/model input.
Rows are current only after trusted native-owner code reaches LOCAL_ESTABLISHED
or post-CAS LIVE_ADOPTED through the infrastructure-only HOT establishment
entry. Admission is process-local operational evidence; cold restart discards
it until current native sources are revalidated. P0 uses an existing real
owner-validated Actor continuity after-image as its producer witness; P1A and P2
supply the T06-specific PC-character and SemanticEvent producers later.

This does not make HOT a semantic acceptance authority: native owner code
validates meaning first; WP12's local transaction establishes the already
accepted after-image.

### SP06-03 — expanding read coherence

Resolved. P0 now defines a finite operation-scoped read session. Any dependency
expansion rereads the full accumulated key union from one closed SQLite
snapshot, invalidates earlier derivations, includes explicit absences and
per-owner source bases, and performs final union revalidation. Movement yields
REVALIDATION_REQUIRED rather than mixed state. No remote I/O occurs inside the
SQLite transaction.

### SP06-04 — P1 issuer/catalog path

Resolved by splitting the lane:

- P1A binds the already-admitted BoundCatalogContext into RuntimeHost and
  implements the S6D-07 production character materialization resolver;
- P1B ReadinessService is the sole issuer of BoundMechanicalDependencySet from
  exact admitted executable/invocation bindings and current owner closure.

Wrong-host/stale catalog and forged dependency carriers fail closed.

## Additional Senior current-consumer findings found during repair

### SP06-05 — actual selected product host lacked HOT wiring

Resolved. P0 now includes bootstrap.compose_selected_runtime_host and RD14.
Trusted HOT capability is supplied at infrastructure composition and is not a
gameplay/model argument. Missing capability cannot mean “HOT is empty”.

### SP06-06 — READY_PC signature lacked PLAYER binding

Resolved. P1B assess_ready_pc takes explicit Actor and PLAYER refs, resolves
both current owners and proves active PLAYER controls that Actor. No reverse
PLAYER scan/index inference is admitted.

### SP06-07 — generic index schema was the wrong EVENT_INDEX contract

Resolved. P2 leaves GAME/SCHEMA/index.schema.yaml on native_family_index
responsibility and creates/finalizes a dedicated strict event_index.schema.yaml
for the already-existing EVENT_INDEX artifact. Template/generator/RuntimeHost/
tests use that event-specific contract. No second history index/owner is added.

### SP06-08 — multi-source History result had singular source basis

Resolved. P2 result is bound to one RuntimeHost operation token and a bounded
collection of contributing source bases; every candidate retains its exact
origin/ref/revision and is exact-revalidated.

### SP06-09 — progressive onboarding had no production materialization resolver

Resolved by P1A. GAME runtime currently has no producer of PC
class_progression/choice_bindings/spellcasting; S6D-07 explicitly deferred the
future production resolver and DIEGETIC_ONBOARDING requires validated native
materialization. P1A implements that already-accepted obligation from typed
accepted anchors/selections plus deterministic inheritance/defaults. It does
not infer rules from prose, create new content, publish or declare READY_PC.

## Gate

```text
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
T06_A1_ARCHITECTURE: ACCEPTED
PLAN_FINDINGS_REPAIRED: SP06-01..SP06-09
PRODUCTION_IMPLEMENTATION: HELD
NEXT: FINAL SENIOR PLAN RE-REVIEW
```

The final Senior review must compare the repaired stable plan against T06-A1,
S6D-07/DIEGETIC_ONBOARDING, WP12 current establishment, current bootstrap
composition and the actual event/index contracts before granting P0 RED/GREEN.
