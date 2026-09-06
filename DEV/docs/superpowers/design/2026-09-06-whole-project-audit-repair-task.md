# Whole-Project Audit Repair Task

Status: **AUTHORIZED REPAIR TASK — WP-21 HOLD**

Date: 2026-09-06

## Goal

Close the remaining whole-project integration defects before WP-21 without reopening accepted architecture wholesale, starting implementation planning, or running a real migration/gameplay bootstrap.

Current Product Owner authority that must be treated as fixed input:

- `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md`

Creator-login rename continuity is **not** a repair target. HDM deliberately fails closed when historical creator login cannot be proven; stable PLAYER/user identity must not be substituted to recover creator authority.

## Scope

This repair task owns exactly four root causes.

### R1 — Publication exact-source currentness proof

Current architecture requires stale-base publication to fail closed, but the supported host/ref-update realization must be proven against the actual authorized transport contract rather than assumed from `force=false`.

Required work:

1. fresh-inspect the current ChatGPT Work/GitHub Connector publication capability and relevant runtime overlay;
2. reconcile the actual ref-transition primitive with the current publication/currentness owners, especially WP-13, WP-16, WP-17, WP-19 and WP-20;
3. preserve the accepted stale-base safety invariant — do not silently weaken exact-source/currentness semantics to fit a weaker primitive;
4. establish one defensible realization:
   - an admitted atomic expected-source primitive/protocol; or
   - an explicit supported-ref monotonicity/fencing invariant under which the available non-force transition is sufficient, including treatment of out-of-band rewind/force history; or
   - fail-closed host capability classification where the required proof cannot be established;
5. add machine/acceptance evidence that falsifies stale-source success for every ref movement allowed by the chosen supported model;
6. preserve WP-13 publication outcome epistemics, including lineage/current-closure read-back; do not reduce ambiguous publication recovery to `ref == intended_commit` only.

If the evidence leaves a material safety-versus-availability policy choice rather than a derivable technical result, stop at the normal human/Senior gate instead of guessing.

### R2 — Product Owner routing closure

`DEV/PRODUCT_OWNER_INPUT.md` still contains stale agent-owned routing/status from before WP-20 closure.

Required work:

1. preserve all Product Owner verbatim blocks unchanged;
2. reconcile PO-004 to the accepted final WP-20 result;
3. retain only genuine deferred downstream implementation/test routes with their real triggers;
4. capture the 2026-09-06 creator-login decision in the normal Product Owner ledger and link its accepted owner decision;
5. reconcile terminal/current routing metadata with the actual global cursor;
6. add a bounded consistency guard so an active/pending Product Owner route cannot point to an already closed WP as its current pending consumer unless a distinct open route is explicitly documented.

No Product Owner decision is open for this repair.

### R3 — Version census must fail closed

`DEV/TESTS/test_versioning_namespace_policy.py` must not classify every unknown version-looking hit through a blanket `NON_VERSION_SEMANTIC_IDENTIFIER` fallback.

Required work:

1. make `UNCLASSIFIED` a real reachable fail state;
2. require explicit intentional rules/allowlisting for `NON_VERSION_SEMANTIC_IDENTIFIER`;
3. retain the independent forbidden-legacy checks;
4. rerun the full census;
5. disposition every newly exposed hit item-by-item against current versioning owners;
6. update completion/status evidence only after zero unclassified hits is genuinely proven;
7. apply the mandatory Version Impact Gate to every changed version-bearing owner/consumer and any newly discovered namespace.

Do not manufacture version bumps for non-material changes merely to make the census green.

### R4 — WP-20 canonical status synchronization

Synchronize the status/provenance wording of:

- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`

with the already-passed final Senior review and current global progress.

This is metadata/status repair only. Preserve the accepted WP-20 semantic laws and historical provenance of the prior candidate state.

## Required owner/evidence set

At minimum, reconstruct the relevant current dependency subgraph from `DEV/PROJECT_MAP.md` and inspect the current owners needed by each repair, including:

- `AGENTS.md` and the current runtime overlay;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` where machine/test changes are executed;
- `DEV/CURRENT_PROGRESS.md`;
- `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`;
- `DEV/PRODUCT_OWNER_INPUT.md`;
- `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md`;
- the current WP-13/WP-16/WP-17/WP-19/WP-20 publication/currentness owners implicated by R1;
- current versioning policy/spec/status owners implicated by R3;
- actual current Connector action schema/capability evidence for R1.

Private research/audit material is not public HDM authority and must not be copied or attributed into public artifacts.

## Boundaries

- Do not start WP-21.
- Do not start general implementation planning beyond the bounded repair work authorized here.
- Do not execute a real campaign/storage migration.
- Do not start gameplay/campaign bootstrap.
- Do not reopen creator-login rename support; the Product Owner decision is final unless explicitly changed later.
- Do not reopen versioning taxonomy or WP-20 architecture unless current public evidence proves material insufficiency that cannot be repaired by the bounded changes above.
- Do not modify the root README.
- Do not create a new branch.

## Execution / verification expectations

Use the lightest current HDM process sufficient for each repair. R1 is correctness-sensitive cross-owner architecture/host work and requires evidence-backed reconciliation before machine assertions are changed. R2/R4 are bounded authority/status propagation. R3 machine changes use TDD under the current execution process.

Before completion:

1. run the mandatory Version Impact Gate for the complete repair diff;
2. run the full maintenance audit;
3. run the full DEV unit suite;
4. obtain fresh hosted verification when available for the exact final public HEAD;
5. reverse-audit the four repair roots against their current owners/consumers;
6. create a repair-closure record under `DEV/docs/superpowers/design/` with item-level dispositions and evidence;
7. update `DEV/CURRENT_PROGRESS.md` truthfully to **repair complete / mandatory Senior repair review pending**;
8. stop. Do not authorize or start WP-21 yourself.

## Closure criteria

```text
R1_PUBLICATION_CURRENTNESS_PROOF: CLOSED
R2_PO_ROUTING_CLOSURE: CLOSED
R3_VERSION_CENSUS_FAIL_CLOSED: CLOSED
R4_WP20_STATUS_SYNC: CLOSED
CREATOR_LOGIN_RENAME_SUPPORT: NOT SUPPORTED / NO REOPEN
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
VERSION_IMPACT: VERIFIED
MAINTENANCE_AUDIT: PASS
DEV_UNIT_SUITE: PASS
WP21_STARTED: NO
NEXT_GATE: MANDATORY SENIOR REPAIR REVIEW
```
