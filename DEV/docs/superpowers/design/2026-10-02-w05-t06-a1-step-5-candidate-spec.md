# W05.T06-A1 — Step 5 Candidate Specification

Status: CANDIDATE FOR ADVERSARIAL REVIEW

## 1. Scope

This candidate realizes:

- coherent current native-owner reads for T06 consumers;
- deterministic production READY_PC/local mechanical sufficiency;
- bounded ordinary Master retrospective;
- the minimum native history-discovery metadata required by WP19-L36.

It does not create product semantics, new durable truth/history owners, a seventh LLM role or a generic search subsystem.

## 2. CurrentOwnerView

RuntimeHost owns an internal operation-scoped CurrentOwnerView.

Inputs are host-owned:

- pinned campaign basis;
- selected LIVE route/source;
- coherent HOT read observation.

For one native owner identity the view resolves:

- selected LIVE current state when LIVE owns the scope;
- otherwise valid established HOT/SOFT state when current;
- otherwise exact pinned campaign state.

It returns an owner-issued observation carrying enough internal source/currentness evidence for downstream validation. Callers cannot inject or replace its source basis.

Context Runtime current-family resolvers SHALL use this boundary instead of direct repository-only reads.

## 3. ReadinessService

RuntimeHost exposes ReadinessService.

### assess_local_sufficiency

Input is one already-derived typed mechanical dependency set. The service checks only those current owner/catalog dependencies. It never expands into arbitrary catalog/world discovery.

### assess_ready_pc

Input identifies one Actor, one current player binding and one admitted BoundCatalogContext.

The service deterministically evaluates the canonical READY_PC predicate against current Actor/PLAYER/Asset/Effect and required definition/rules evidence.

Output is a typed assessment with ready status, blocker codes, current Actor revision/source basis, catalog/ruleset identity and reconstructive attestation.

No readiness result becomes an independent state owner. PLAY_READY remains downstream durability/product composition.

## 4. History discovery

The existing EVENT_INDEX remains the single durable event discovery projection.

runtime.semantic_event semantic_delta may include validated discovery_refs consisting only of native owner_family + owner_identity references already supported by accepted event inputs/provenance.

EVENT_INDEX entries may copy index-safe discovery_refs. The index never stores prose, current knowledge/disclosure, T0 values or motive.

HistoryService supports bounded structured discovery over:

- exact event/source refs;
- typed native owner refs;
- session refs when accepted;
- recent tail.

The result is candidate event identity/origin/ordinal only. Exact event/native evidence is loaded separately.

## 5. Current unpublished history

Accepted unpublished runtime.semantic_event establishment atomically updates a HOT derived discovery helper. HistoryService merges durable EVENT_INDEX and valid HOT helper candidates for the current operation. Selected LIVE history participates only through the exact current LIVE source.

## 6. RetrospectiveService

RuntimeHost exposes RetrospectiveService for ordinary active-player gameplay.

It:

1. validates current active PLAYER and selected controlled PC as applicable;
2. resolves current orientation through CurrentOwnerView;
3. obtains bounded History candidate refs;
4. exact-loads shortlisted native evidence;
5. gathers current knowledge/disclosure eligibility;
6. issues a host-sealed RetrospectiveEvidenceSet;
7. invokes Context Runtime assembly using existing profile.narration, purpose narrate, retrospective=True.

RetrospectiveService does not generate prose and is not an LLM role.

## 7. Context retrospective admission

Direct external retrospective=True remains fail-closed unless the call carries the RuntimeHost-issued sealed retrospective evidence for the same operation basis.

Context Runtime:

- validates the evidence seal and source basis;
- revalidates current PLAYER/control;
- applies current knowledge/disclosure/source eligibility;
- excludes private historical material not currently eligible;
- returns only eligible historical/current projections in the Narrator role bundle.

Raw private History bodies are not exposed to the model merely because deterministic runtime can read them.

## 8. Story

No public Master Story adapter is required by this candidate.

Story may be reconsidered only under the explicit revisit triggers in Step 2. If added later, it can nominate bounded refs only; native/current proof and eligibility remain mandatory.

## 9. Failure semantics

- stale/incompatible current source: revalidation/currentness failure, not mixed read;
- missing READY_PC dependency: blocker, not invention;
- invalid/incomplete history index: direct known evidence may still work; no scan fallback;
- selected LIVE discovery unavailable: typed inability; no campaign fallback as current live truth;
- insufficient historical/T0 evidence: explicitly insufficient, not reconstructed motive;
- inactive/missing player or invalid PC control: ordinary active-player retrospective fails closed;
- Story missing/stale: no baseline failure;
- cold restart after unpublished HOT loss: no recovery claim from surviving bytes without source-equivalence proof.

## 10. Performance

The design adds no mandatory serial LLM call.

Historical requests may read the one monolithic event index plus a bounded number of exact event/current-owner records. No ordinary request scans event bodies campaign-wide.

Partitioning remains WP24-triggered by measured size/latency/tool evidence.

## 11. Versioning

This architecture does not assign runtime version bumps. Implementation must perform the normal Version Impact Gate for modified GAME modules/index/schema contracts.

No compatibility layer is required solely for pre-release structures when accepted clean-slate rules apply.
