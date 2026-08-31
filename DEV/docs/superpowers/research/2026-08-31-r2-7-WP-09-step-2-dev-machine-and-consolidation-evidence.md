# R2.7 WP-09 Step 2 — DEV Machine Contracts, Verification and Consolidation

Status: **EVIDENCE SLICE 3 COMPLETE — STEP 2 COMPLETE**

## Scope and method

This final Step-2 slice completes the direct Source Manifest route: package/bootstrap
boundary, implicated runtime-state schemas, MechanicalContext, catalog/test and
maintenance/CI consumers. A targeted GitHub code-symbol query returned no results
for the R2.3 terms on this service; that query is recorded only as a discovery
limitation, not as absence proof. Dispositions are based on the opened primary
owners and exact current named consumers.

## Extracted evidence

| ID | Actual source / item | Evidence | WP-09 disposition |
|---|---|---|---|
| D01 | `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`; `GAME/INSTALL/00_DND_BOOTSTRAP.md`; `GAME/SCHEMA/dnd_storage.schema.yaml` | A verified local runtime ZIP and ephemeral `current_runtime_root` provide engine bytes. GitHub campaign storage does not supply engine source; package cache paths are explicitly non-durable. | Preserve the R2.6 host/package boundary. No GitHub source scan or durable context/cache root is authorized for normal play. |
| D02 | `DEV/SCHEMAS/runtime-{command,continuation,intent-plan,interaction,mechanical-event,procedure,resolution,resolution-trace}-state.schema.json` | These schemas describe deterministic/adjudication state: catalog fingerprints, accepted bindings, continuation, mechanical procedure and mechanical trace. The word “context” there is catalog/mechanical context, not the R2.3 role-context contract. | Existing distinct owner. Do not repurpose a continuation, resolution trace or catalog fingerprint as RoleContextBundle, ContextTrace or context-source eligibility. |
| D03 | `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`; `DEV/TESTS/test_s6d_04_mechanical_context_contract.py` | Mechanical accessor/fact registry restricts mechanical-stage input and marks derived caches disposable. Its test validates that bounded contract. | Confirms the negative boundary already found in M09: mechanical context cannot be a general discovery, continuity or role-cognition store. |
| D04 | `DEV/TOOLS/run_maintenance_audit.py`; `.github/workflows/validate.yml` | Push/PR CI invokes maintenance audit and DEV unit discovery. The maintenance wrapper is a development-root tool, not a campaign runtime operation. | Documentation checkpoints require remote diff/read-back; runtime behavior remains future verification work. Do not invoke an engine-maintenance scan as ordinary gameplay retrieval. |
| D05 | `DEV/CATALOG/core-catalog.json`; direct CORE/test sources from slice 2 | The catalog’s R2.3 vocabulary and current lazy-read/cache regressions are machine-adjacent but do not expose an execution owner or tests for profile floors, currentness/eligibility, legal degradation, estimator, or finite caller alternatives. | Record a **realization/test gap**, not an authority or product decision. Its implementation mapping belongs to the later approved implementation cycle; this WP does not plan or implement it. |

## Step-2 consolidated conformance result

| Mandatory WP-09 question | Evidence result | Disposition |
|---|---|---|
| Bounded discovery before full load | CURRENT/scene/INDEX schemas and CORE targeted-read policy can serve as compact routing inputs; canonical R2.3 supplies typed finite closure and full-load boundary. | Compatible support; no physical root or partition decision. |
| Floors/degradation/`UNSATISFIABLE` without hidden telemetry | R2.3/R2.4/R2.6 own the legal contract; catalog registers the vocabulary. Current selected tests do not behaviourally prove it. | Existing-law realization and verification obligation. |
| Hidden campaign-wide hot-path scans | PLAY_POLICY, RUNTIME and STORAGE expressly forbid broad ordinary scans; existing regressions cover selected lazy/targeted cases. | No contradiction found in inspected current hot-path owners; future behavior tests must keep the negative proof. |
| Scene/location/current/index as routing but not closed-world authority | Schema invariants expressly make index routing-only and mobile presence/current truth typed/routed; templates are empty scaffolds. | Compatible; no completeness inference or WP-11 topology decision. |
| Supported ChatGPT profile | Bootstrap uses ephemeral local package cache; R2.6 prohibits exact hidden telemetry; CORE working set distinction remains intact. | Compatible with conservative estimator/fallback direction; no provider capability claim. |

## Findings and operational dispositions

1. **F01 — supporting topology, not replacement authority.** Preserve the
   CORE-cache/lazy-campaign-working-set distinction. Future Context Runtime
   realization must consume routing hints rather than make cache, index, current
   chat, SQLite, trace, or DEV catalog the semantic source of truth.
2. **F02 — implementation-facing behavior gap.** Current catalog registration
   and targeted-read tests are insufficient evidence for the full accepted
   profile/packet/currentness/eligibility/outcome contract. Carry precise
   behavioral acceptance obligations forward; do not create a new specification
   merely to repeat research evidence.
3. **F03 — no hidden broad scan found in inspected owners.** This is a scoped
   positive result, not a repo-wide search claim. Future tests must retain normal
   hot-path negative cases.
4. **F04 — MechanicalContext and S6D continuations remain separate.** They
   provide deterministic mechanical inputs/traces only; no R2.3 role-context or
   Actor-private continuity authority is added.
5. **F05 — cross-domain physical work is deferred.** WP-10 owns record roots,
   WP-11 partition/topology, WP-12 HOT/SQLite realization, WP-24 numeric scale
   policy and WP-25 full failures. No routing trigger was found that requires
   reopening WP-08 or those domains.

## Decision gate

**NO HUMAN DECISION.** The accepted canonical owners resolve the discovered
choices. Step 3 shall map these evidence findings to existing logical owners and
future verification obligations without implementation planning.
