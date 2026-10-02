# W05.T06 — Current Readiness and Ordinary Master Retrospective Canonical Specification

Status: **CANONICAL — REVIEW STOP 2 GO / ARCHITECTURE ACCEPTED**

Senior acceptance: DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-review-stop-2-senior.md.
Production implementation remains subject to the repaired W05 plan/Impact Envelope Senior GO.

This specification is the implementation-facing architecture owner for W05.T06 progressive readiness and ordinary active-player Master retrospective. It composes existing owners; it does not replace them.

## 1. Scope and authority

This specification owns only the missing machine composition for:

- current-owner observation required by the T06 consumers;
- deterministic production READY_PC/local mechanical sufficiency;
- bounded native historical discovery for ordinary Master retrospective;
- RuntimeHost orchestration and Context admission of retrospective evidence.

Semantic truth/currentness remains with native campaign/HOT/LIVE owners. Historical meaning remains with native History/SemanticEvent and its source owners. Current eligibility remains with PLAYER/knowledge/disclosure/access owners. Story remains noncanonical.

## 2. LAW T06A1-1 — one operation-scoped CurrentOwnerView

RuntimeHost SHALL own one internal CurrentOwnerView for authority-sensitive current semantic reads.

For one native owner identity the view resolves under one operation basis:

1. selected LIVE source when current LIVE routing owns the scope;
2. otherwise accepted established HOT/SOFT owner state when current;
3. otherwise exact pinned campaign owner state.

No timestamp, local insertion order, generation magnitude, repository recency or cached convenience may select authority.

CurrentOwnerView is a read composition boundary only. It owns no semantic state.

## 3. LAW T06A1-2 — HOT read coherence is operational, not a global frontier

One CurrentOwnerView operation SHALL observe a coherent HOT read snapshot or an equivalent validated read basis.

The snapshot/token:

- may support SQLite read consistency and stale-read detection;
- is ephemeral;
- does not establish semantic chronology/currentness by itself;
- is not a campaign-global dirty generation/frontier/lease.

An incompatible concurrent source change yields bounded revalidation/currentness failure rather than a mixed read.

Cold recovery follows WP12/WP14: stale surviving local bytes do not regain authority merely by existing.

## 4. LAW T06A1-3 — Context current families use CurrentOwnerView

Current Context Runtime resolution of PLAYER, knowledge, disclosure and registered current world/native families SHALL use the RuntimeHost current-owner boundary.

Direct pinned-repository reads may remain an implementation detail only where the current-owner boundary has selected the pinned campaign source for that owner.

This closes the existing repository-only stale-currentness seam.

## 5. LAW T06A1-4 — readiness is deterministic derivation, not state authority

Production runtime SHALL provide deterministic readiness evaluation under GAME/TOOLS. Runtime code SHALL NOT import DEV validation tooling.

ReadinessService SHALL distinguish:

- local mechanical sufficiency for one already-derived typed dependency set;
- canonical READY_PC;
- downstream PLAY_READY/durability composition.

No persisted ready boolean, readiness singleton or bootstrap-supplied readiness authority is introduced.

## 6. LAW T06A1-5 — READY_PC uses current owner and exact catalog evidence

READY_PC evaluation SHALL bind at least:

- exact current Actor identity/revision;
- exact current active PLAYER/control relation required by the use case;
- required current Asset/Effect/native mechanical dependencies;
- one admitted BoundCatalogContext;
- exact catalog generation, ruleset lock / ruleset_set_sha256 and required production conformance evidence.

The returned assessment SHALL contain deterministic blocker codes and reconstructive basis/attestation sufficient to explain the result without becoming a second owner.

A ready result may be consumed by the existing onboarding/durability path. The evaluator itself does not mutate Actor status, publish, save or establish PLAY_READY.

## 7. LAW T06A1-6 — readiness is re-evaluated

Readiness SHALL be recomputed after material accepted build/current-owner changes and on resume/rejoin when product correctness depends on READY_PC.

A stale prior result is never authority.

If current accepted state contradicts a previously assumed active/ready condition, fail closed through existing integrity/product semantics; do not invent missing mechanics or silently repair from memory.

## 8. LAW T06A1-7 — ordinary retrospective remains ordinary Master gameplay

An authorized active player retrospective uses the existing Interpreter and Narrator logical roles.

No MASTER role, Commentator transition or CLS dependency is introduced.

The registered Context consumer remains:

- role: NARRATOR;
- profile: profile.narration;
- purpose: narrate;
- retrospective: true.

RetrospectiveService is deterministic use-case orchestration, not an LLM role and not a prose generator.

## 9. LAW T06A1-8 — minimum native History discovery lives under existing EVENT_INDEX ownership

WP19-L36 is activated by current physical evidence.

The existing EVENT_INDEX SHALL remain the one durable SemanticEvent discovery projection. No second durable history/search index owner is created.

Accepted runtime.semantic_event records MAY retain deterministic typed discovery_refs inside semantic_delta. Each ref identifies a registered native owner family plus complete owner identity and MUST be validated against already accepted event input/provenance; model prose cannot create authority by naming a ref.

EVENT_INDEX may copy the index-safe subset of those refs into the event entry.

Discovery refs are routing metadata only. They contain no prose, motive, T0 value, knowledge/disclosure state or current authority.

Missing discovery refs mean unknown/not-indexed for that selector, never semantic absence.

## 10. LAW T06A1-9 — EVENT_INDEX remains derived and exact evidence terminates claims

EVENT_INDEX may nominate candidate event IDs/ordinals/paths and index-safe typed refs.

A material/source-specific historical claim SHALL terminate in an exact owner-issued NativeSemanticEvent or exact native source evidence.

The index cannot establish:

- event truth by itself;
- current world state;
- current eligibility;
- historical motive;
- absence of an event.

Existing exact identity/currentness/fingerprint validation remains mandatory.

The campaign blank template/writer/schema SHALL be aligned with the already accepted complete/upper_ordinal History enrollment contract when this work is implemented.

## 11. LAW T06A1-10 — bounded History query, not generic search

HistoryService SHALL expose bounded structured discovery sufficient for the proven Master consumers.

Allowed selectors are limited to already admitted typed evidence such as:

- exact event/source ref;
- typed current native owner ref;
- accepted session ref;
- recent bounded tail;
- bounded provenance/source ref from eligible current evidence.

The request SHALL carry a finite max-candidate bound.

There is no baseline raw-text search, regex, embedding search, arbitrary predicate, global relevance graph or unbounded pagination loop.

Reading the one accepted monolithic EVENT_INDEX artifact and filtering it in memory is allowed under current WP11 law. Whole-campaign event-body scans are not.

## 12. LAW T06A1-11 — accepted unpublished and LIVE history participate correctly

Durable EVENT_INDEX alone is not a complete current discovery view.

When an accepted unpublished runtime.semantic_event is established in HOT, the same local atomic establishment SHALL update a narrow derived HOT event-discovery helper. The helper owns no semantics and is rebuildable/discardable under WP12 rules.

One History query composes:

- durable EVENT_INDEX at the pinned campaign basis;
- accepted current HOT discovery rows under the operation snapshot;
- selected LIVE history discovery metadata when LIVE owns that current source.

Pre-CAS prospective LIVE state is excluded.

Selected LIVE lacking a required bounded discovery route produces typed bounded inability. Campaign history SHALL NOT be substituted as current LIVE truth.

## 13. LAW T06A1-12 — exact current questions resolve from current owners

Historical evidence may explain how the game reached a state. It does not replace current owners.

Questions whose answer depends on NOW SHALL resolve the relevant current Actor/world/knowledge/disclosure/LIVE owners through CurrentOwnerView even when History or Story supplied orientation.

No retrospective path restores T0 state into current owners.

## 14. LAW T06A1-13 — RetrospectiveService owns use-case orchestration only

RuntimeHost SHALL provide a RetrospectiveService or equivalently narrow product use-case boundary that:

1. validates current active PLAYER and selected controlled PC where applicable;
2. obtains current orientation through CurrentOwnerView;
3. issues bounded History discovery;
4. exact-loads shortlisted native evidence;
5. obtains current knowledge/disclosure/access evidence;
6. creates a RuntimeHost-issued sealed RetrospectiveEvidenceSet bound to the same operation basis;
7. requests Context Runtime assembly for profile.narration / retrospective=True.

The service does not own truth, History, disclosure or narration.

## 15. LAW T06A1-14 — historical evidence admission is sealed and recipient-safe

Raw History payload is not caller authority.

The ordinary external Context candidate mapping SHALL NOT be able to inject runtime.semantic_event payloads or make retrospective=True sufficient for historical admission.

Historical evidence entering Context requires a RuntimeHost-issued same-operation seal or equivalent unforgeable owner-issued carrier.

Context SHALL revalidate:

- current active PLAYER/recipient;
- selected PC control where applicable;
- current knowledge/disclosure/source eligibility;
- exact historical source binding/currentness.

Only eligible projections cross into the Narrator role bundle. Raw private event bodies, EVENT_INDEX rows, HOT helper rows and protected routing diagnostics remain deterministic internal material.

If an exact historical field cannot be tied to an applicable eligibility basis, omit/fail closed rather than expose it.

## 16. LAW T06A1-15 — T0 motive evidence remains exact and bounded

For a historical motive/decision explanation, retained actor_decision_basis inside the accepted NativeSemanticEvent is the historical evidence owner already selected by WP19.

Current T1 Actor state SHALL NOT be used to reconstruct missing T0 motive as established history.

T0 factor availability classification is necessary but does not override current recipient eligibility.

Insufficient or ineligible T0 evidence remains insufficient and visible output must distinguish evidence from inference.

## 17. LAW T06A1-16 — Story is dormant for baseline Master retrospective

No public Master Story reader is required by this baseline.

Story may orient a later implementation only after a new design/review trigger proves one of:

1. measured native/index discovery cannot satisfy bounded interaction cost without broad event-body reads; or
2. concrete product evaluation shows bounded Story orientation materially improves navigation.

If activated later:

- read is bounded and read-only;
- entity_refs/source_refs/story_refs are nominations only;
- Story absence/staleness is nonfatal;
- exact native evidence and current eligibility remain mandatory;
- Story never becomes current truth or History replacement.

Current implementation work SHALL NOT create the adapter solely because Story lookup metadata exists.

## 18. LAW T06A1-17 — failure and recovery are explicit

The following do not authorize guessing or broad fallback:

- missing readiness dependency;
- invalid/incomplete derived event index;
- absent LIVE discovery metadata;
- stale source/currentness;
- lost unpublished state after crash;
- inactive PLAYER or invalid PC control;
- missing/ineligible historical or T0 evidence;
- Story unavailable.

Existing typed revalidation/failure/UNSATISFIABLE paths are used as appropriate.

Direct known evidence may still be used when a coarse discovery projection is invalid, but no coarse-selector failure authorizes a whole-history scan.

## 19. LAW T06A1-18 — no extra serial LLM or publication boundary

This architecture adds no mandatory sequential model call.

Readiness is deterministic.

Retrospective discovery/evidence binding is deterministic and occurs only for a material retrospective request. The existing logical Interpreter/Narrator phases remain under the accepted single-context execution design.

Discovery/readiness creates no independent save/publication boundary. Dirty required history joins existing durability behavior.

## 20. Cross-system impact

Depends on:

- Step-4 truth/knowledge/disclosure/role law;
- R2.3 Context Runtime;
- Step-5.1 current view;
- WP11 routing/index;
- WP12 HOT;
- WP14 recovery;
- WP16 LIVE/access;
- WP19 retrospective/T0/history;
- S6D READY_PC;
- existing RuntimeHost/History/Context/catalog machine contracts.

Constrains:

- W05.T06 onboarding/rejoin/ordinary retrospective;
- Context Runtime current-owner reads;
- History query/read surfaces;
- EVENT_INDEX writer/template;
- HOT helper maintenance;
- RuntimeHost composition.

Owns:

- no semantic or durable state owner;
- only the T06 machine composition contracts above.

May observe:

- selected current owners;
- exact native history;
- current eligibility;
- derived indexes/helpers.

May mutate:

- architecture selects only derived EVENT_INDEX/HOT helper maintenance as companions of existing SemanticEvent establishment/publication;
- readiness/retrospective reads themselves do not mutate semantic owners.

Consumers:

- onboarding;
- join/rejoin readiness verification;
- ordinary active-player Master retrospective;
- existing Context Runtime current-family resolution.

Operational effect:

- ordinary non-retrospective gameplay receives no new History read;
- ordinary current Context reads can use HOT without waiting for SAVE;
- retrospective performs bounded index/current-owner/exact evidence reads only;
- WP24 remains the trigger for measured index partitioning.

## 21. Decision log

T06A1-D1
Context: shared stale-currentness gap.
Chosen: one RuntimeHost internal CurrentOwnerView.
Status: ACCEPTED — REVIEW STOP 2 GO.

T06A1-D2
Context: READY_PC has semantic owner but no production callable.
Chosen: deterministic production ReadinessService over current owners + admitted catalog.
Status: ACCEPTED — REVIEW STOP 2 GO.

T06A1-D3
Context: ordinal EVENT_INDEX cannot satisfy semantic retrospective discovery.
Chosen: minimum typed discovery refs in existing EVENT_INDEX plus HOT/LIVE companions.
Status: ACCEPTED — REVIEW STOP 2 GO.

T06A1-D4
Context: ordinary retrospective spans History + current eligibility + Context.
Chosen: thin RetrospectiveService and sealed Context evidence, existing Narrator profile.
Status: ACCEPTED — REVIEW STOP 2 GO.

T06A1-D5
Context: Story lookup exists.
Chosen: DORMANT, not baseline implementation.
Status: ACCEPTED — REVIEW STOP 2 GO.

## 22. Risk/deferred record

Risk: CurrentOwnerView accidentally becomes new authority.
Mitigation: source choice must remain delegated to accepted campaign/HOT/LIVE rules; view is read-only and operation-scoped.

Risk: event discovery leaks protected material.
Mitigation: index-safe identifiers only in durable index, raw data deterministic-only, current eligibility before model context.

Risk: monolithic EVENT_INDEX grows.
Mitigation: current WP11 rule remains; WP24 measured trigger controls partitioning.

Dormant item: public Master Story orientation adapter.
Trigger: measured native discovery cost or concrete product navigation-quality evidence.
Current action: none.

No unresolved blocking architecture debt remains.
