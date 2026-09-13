# HDM Implementation Planning — Independent Senior Review Brief

Status: READY FOR GENUINELY INDEPENDENT SENIOR PLAN REVIEW
Author package head at brief creation: `e33d0ad2a1d735a114cdfaf39c50decc3f9279af`.
Production implementation authorized: NO.

## Reviewer role
Act as independent HDM Senior Plan Reviewer. Do not repair the author package while reviewing. Recompute material claims from authoritative repository sources. Author coverage/closure documents are evidence to challenge, not authority.

## Fresh bootstrap
Use GitHub Connector authoritative remote state only. Fresh-check branch `v1/engine-rearchitecture`, then current `AGENTS.md`, runtime overlay, required Superpowers, `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/PROJECT_MAP.md`, `DEV/CURRENT_PROGRESS.md`, near-term roadmap/status, then task owners.

## Mandatory review corpus
1. WP-27 final readiness spec + Step-2 evidence ledger.
2. Critic-approved `2026-09-13-implementation-planning-candidate-bounded-decomposition-v2.md` and final decomposition critic PASS result.
3. Package conventions + Impact/TDD contract + master/index.
4. All RD-01..RD-14 executable plans and PB-02..PB-05 source manifests/closures.
5. `2026-09-13-implementation-planning-execution-waves.md` + PB-06 closure.
6. `2026-09-13-implementation-planning-bidirectional-coverage.md`.
7. Current semantic/runtime/persistence/version owners required to validate any disputed route.

Do not inspect runtime release packages unless a review finding specifically concerns packaging/compatibility/release validation.

## Required independent checks

### A — canonical accounting
Independently reconstruct active 133, trigger-gated 12, no-work 79 and absent R004. Verify active set partitions exactly into 116 direct + 9 pure proof + 8 composite parents with no overlap/missing/extra identity.

### B — leaf/slice fidelity
For every active readiness identity, verify exact owner, disposition, qualifiers, negative laws, scenarios, defer/revisit semantics and planning route. Composite slices must preserve parent semantics without becoming new readiness IDs.

Pay special attention to author-repaired PB-05 routes:
- RD-12: R016.COLLAB, R018.COLLAB, R122.COLLABORATION_BRIDGE;
- RD-13: R016.STORY, R018.STORY, R062.SEMANTIC_EVENT_HISTORY, R087.SEMANTIC_EVENT_T0;
- RD-14: R029.ONBOARDING, R087.SAVE_SESSION_MENU.

### C — executable-plan quality
Check every RD plan for exact file actions/owners, bounded worker tasks, TDD RED/GREEN/REFACTOR/VERIFY, Impact Envelope, negative-law tests, Version Impact/schema/catalog/checkpoint/migration/HG-01 handling, coherent commit boundaries and currentness fence. Reject conditional design choices improperly delegated to implementation workers.

### D — dependency graph / execution waves
Recompute owner-derived E1-E15. Verify PB-06 neither serializes independent owners unnecessarily nor closes joins too early. Specifically test RD-11/RD-12 cycle handling, R124, R122, R029, R062, R087, selected-LIVE recovery, protected emission, T0/Commentator, save-and-exit and creator fail-closed joins.

### E — reverse coverage
Inspect implementation/proof/integration tasks in the plans and waves. Every task must trace to an admitted readiness leaf/slice, required owner integration, proof route, Version Impact projection or test/audit evidence. Report orphan work or architecture invention.

### F — currentness
Fresh-compare authoring refs to review HEAD. If canonical owners/decomposition/readiness changed, determine whether package is stale before judging it. Planning/control edits alone do not create semantic drift.

### G — protected invariants
Adversarially check no second gameplay/knowledge/history/currentness authority; eligibility before use; optional ranking cannot override authority/eligibility/requiredness; TurnEnvelope control not authority; physical presence not eligibility; late steering non-authoritative; only validated Narrator payload crosses EMISSION_COMMIT; no global active player; positive dependency before waiting; scope-local waiting; join/rejoin current frontier; catch-up recipient projection; Story noncanonical; T0 not parallel history; Context Runtime ephemeral.

## Finding severity / verdict
Report itemized `BLOCKING`, `SIGNIFICANT`, `MINOR` findings with exact source/plan evidence and affected readiness/tasks. Do not silently repair.

Final verdict must be exactly one:
- `PASS / GO FOR PRODUCTION IMPLEMENTATION PLANNING GATE` only if no unresolved blocking/significant defect and package is execution-ready;
- `FAIL / REPAIR REQUIRED` otherwise.

Even on PASS, this review authorizes the next repository gate only; it does not itself execute production implementation, migration, release or gameplay bootstrap.

## Expected result artifact
Publish an independent review result under `DEV/docs/superpowers/plans/` (or the current repository-mandated review location if owners changed), record reviewed HEAD, currentness evidence, independent accounting, findings, verdict and exact next authorized unit. Update `DEV/CURRENT_PROGRESS.md` only according to the resulting gate and repository process.