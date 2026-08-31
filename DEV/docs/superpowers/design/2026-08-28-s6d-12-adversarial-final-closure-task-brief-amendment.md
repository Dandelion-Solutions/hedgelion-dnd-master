# S6D-12 — Adversarial Final Closure — Task Brief Source-Manifest Amendment

Status: **STEP 1 TASK-BRIEF AMENDMENT — APPLIES WITH ORIGINAL BRIEF**

Date: 2026-08-28

Applies with:

`DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-task-brief.md`

Together, the original brief and this amendment are the corrected S6D-12 Step-1 Task Brief presented to the mandatory whole-project critic.

## 1. Reason for amendment

Self-review against current `DEV/PROJECT_MAP.md` and the actual current owner graph found that the initial Source Manifest named the S6D-01…11 owners and broad execution/persistence concerns, but did not explicitly pin several inherited owners whose laws materially constrain final cross-owner closure.

This is a source-discovery completeness repair. It does not widen S6D-12 product scope, reopen S6D-01…11, or introduce a new architecture choice.

## 2. Additional canonical/inherited owners

The Source Manifest SHALL additionally include:

### Catalog definition/resolution inheritance

- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` — definition/world/runtime admission and envelope ownership; runtime references do not create durable definition authority; caches/indexes remain non-authoritative.
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md` — `ResolvedCatalogContext` remains a logical composition of natural owners; exact resolution, collision/currentness and retry/recovery laws constrain S6D package/context closure without introducing a global snapshot owner.

These owners matter because final S6D closure must prove that package identity, catalog admission and runtime resolution compose without duplicate authority.

### Repository/source/adoption authority

- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — engine/package authority versus campaign creator/player adoption and persistence rights.
- `DEV/ARCHITECTURE/BRANCH_MODEL.md` — engine repository, runtime package and campaign-storage topology and authority boundaries.
- `GAME/CORE/SOURCES.md` — runtime rules/source routing and unsupported-source behavior.
- `GAME/CORE/PLAY_POLICY.md` — current play-policy boundary and what mechanics may be used for play.

These owners matter because a reconstructable package is not by itself authority to persist campaign adoption, and source visibility/availability must not become a second rules owner.

## 3. Exact execution owners

The Source Manifest SHALL explicitly include:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` as the accepted Execution/Resolution/Continuation owner;
- current machine schemas implementing that boundary, at minimum:
  - `DEV/SCHEMAS/action-request.schema.json`;
  - `DEV/SCHEMAS/runtime-command-state.schema.json`;
  - `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
  - `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
  - `DEV/SCHEMAS/execution-segment.schema.json`;
  - `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json`;
  - `DEV/SCHEMAS/resolution-receipt.schema.json`;
  - `DEV/SCHEMAS/pending-child-invocation.schema.json`;
  - `DEV/SCHEMAS/runtime-procedure-state.schema.json` where Procedure continuity participates;
  - `DEV/SCHEMAS/runtime-resolution-trace-state.schema.json` only as diagnostic/evidence state, never as outcome authority.

The critic and Step 2 must test that accepted work retains exact ruleset/catalog identity and fixed causal/RNG/adjudicated evidence across retry/recovery, while ExecutionSegment/MechanicalEvent/receipt ownership remains distinct from package/catalog ownership.

## 4. Exact retention/cleanup owners

The Source Manifest SHALL explicitly include:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`.

Step 5.13 is material because it requires owner-gated fail-safe retirement, rejects universal semantic mark-and-sweep/refcount/global-GC authority, requires new consumer classes to enroll before they may depend on cleanup targets, protects active/unsettled execution and fixed RNG/accepted interpretation evidence, and forbids stale protection-routing evidence from authorizing irreversible loss.

S6D-12 therefore must prove that exact package snapshots and other retry/recovery evidence cannot be retired while a typed current consumer still requires them, without inventing a new global retention owner.

## 5. Machine-evidence floor clarified

The machine route in the original brief SHALL be read to include the exact current schemas/projections consumed by the S6D-07…11 validators, not merely the validator source files. In particular, Step 2 must inspect the current runtime Resolution/Continuation package-identity projections, resolved-lock/package-closure schemas and the focused tests that claim those projections are current.

A schema example, nullable scaffold or generic illustrative value is not a current identity projection merely because it contains a hash-shaped field. Current-carrier classification remains consumer/owner based.

## 6. Existing carry-ins unchanged

This amendment does not change the prior carry-in dispositions:

- B′ remains `KNOWN_REALIZATION_BLOCKER / MACHINE_REALIZATION`, with settled architecture and no repeated root-cause diagnosis;
- the checked-in derived identity mismatch remains a current machine-realization defect, not new identity architecture;
- the old S6D-08 aggregate-content-set prose remains provisionally `STALE_SUPERSEDED_ASSERTION`, subject only to Step-2 confirmation that no current consumer still treats it as authority.

No B′ machine-contract implementation is authorized by this amendment. R2.7 remains paused.

## 7. Corrected Step-1 critic gate

The mandatory brief critic must review the original Task Brief plus this amendment against the current `PROJECT_MAP`-derived dependency graph. Step 1 may pass only if no remaining blocking/significant owner or consumer omission changes the S6D-12 problem framing.
