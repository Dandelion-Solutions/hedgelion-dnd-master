# Documentation Corpus Refactor — Conflict / Dual-Authority / Deferred-Debt Register

Status: **ACTIVE DURABLE REGISTER — OWNER TRIAGE DEFERRED UNTIL CORPUS REFACTOR CLOSURE**

Date: 2026-08-29

Branch: `v1/engine-rearchitecture`

Purpose: preserve every documentation inconsistency, duplicate/competing source-of-truth condition, unresolved supersession question, stale wording surface, deferred cross-stage obligation, incomplete machine realization, forgotten/stranded requirement risk, and refactor-operational debt discovered while completing the Documentation Corpus Refactor.

This register is **not** architecture authority and does not itself resolve any issue. It exists so the corpus refactor can continue without silently fixing, forgetting, or normalizing unrelated debt. The owner will triage the final list separately.

At refactor closure, create a separate frozen final report containing the complete then-current issue set, including items resolved by the refactor and items intentionally deferred.

## 1. Recording protocol

Every material issue gets a stable `DCR-*` identifier and must preserve:

- `TYPE`
- `STATUS`
- `OWNER_TRIAGE: PENDING` unless the owner explicitly decides otherwise
- exact affected/current-owner files
- the competing/stale/deferred semantics
- whether a true contradiction exists or only an implementation/deployment gap
- why the condition matters
- currently named resolution stage / revisit trigger, if one exists
- whether the corpus refactor may mechanically resolve only placement/routing, or must leave semantic repair for later work

### Issue types

```text
DUAL_SOURCE_OF_TRUTH
EXPLICIT_SUPERSESSION_BUT_OLD_NORMATIVE_COPY_REMAINS
UNRESOLVED_SUPERSESSION
CONTRADICTORY_OR_STALE_WORDING
DUPLICATE_OWNER_RISK
DEFERRED_MACHINE_REALIZATION
DEFERRED_HOST_CAPABILITY
DEFERRED_LATER_STAGE_OBLIGATION
MISSING_REALIZATION
REFACTOR_OPERATIONAL_DEBT
OTHER_DOCUMENTATION_DEBT
```

### Status vocabulary

```text
OPEN
PENDING_CENSUS
EXPECTED_DEFERRED
RESOLVED_BY_CURRENT_OWNER_BUT_STALE_SURFACE_REMAINS
RESOLVED_BY_REFACTOR
OWNER_TRIAGE_REQUIRED
```

`EXPECTED_DEFERRED` does **not** mean harmless or complete. It means an explicit later owner/stage currently exists and the obligation must remain visible until that stage actually discharges it.

## 2. Accumulated issues

### DCR-001 — Step 5.2 canonical v1 and v2 both remain in `specs/`

- **TYPE:** `EXPLICIT_SUPERSESSION_BUT_OLD_NORMATIVE_COPY_REMAINS` / discovery-level `DUAL_SOURCE_OF_TRUTH` hazard.
- **STATUS:** `RESOLVED_BY_CURRENT_OWNER_BUT_STALE_SURFACE_REMAINS`.
- **OWNER_TRIAGE:** PENDING.
- **OLD SURFACE:** `DEV/docs/superpowers/design/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec.md`.
- **CURRENT OWNER:** `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`.
- **CONDITION:** both files advertise `CANONICAL ARCHITECTURE — STEP 5.2 CLOSED`, but v2 explicitly says it supersedes the original for current Step-5.2 authority. The original is historical derivation only.
- **WHY IT MATTERS:** a fresh reader can select the wrong canonical file from `specs/`, and the original contains a weaker temporal-enrollment rule later replaced by v2.
- **CURRENT DISPOSITION:** original belongs in `design/`; v2 remains `specs/`. Physical move/path repair is pending the repository-wide inbound-reference gate.

### DCR-002 — Step-2 mechanical-state ownership accepted sub-decisions not yet proven fully superseded

- **TYPE:** `UNRESOLVED_SUPERSESSION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md` (`S-010`).
- **CONDITION:** document is mostly design provenance but contains preliminary accepted sub-blocks. Later Step-2/current owners are expected to control, but item-level survival has not yet been proven.
- **RISK:** moving/demoting it before proof could strand accepted implementation-relevant law; keeping it in `specs/` risks duplicate authority.
- **CURRENT DISPOSITION:** remain in `specs/` pending final supersession proof.

### DCR-003 — Step-1/2 retrospective architecture assurance final may overlap later current owners

- **TYPE:** `UNRESOLVED_SUPERSESSION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md` (`S-015`).
- **CONDITION:** integrated accepted assurance/amendment surface is potentially superseded in parts by later architecture, but item-level supersession remains unproven.
- **CURRENT DISPOSITION:** remain in `specs/` until later-owner comparison closes.

### DCR-004 — Step-2 temporal/recovery resolution current-law survival not yet proven

- **TYPE:** `UNRESOLVED_SUPERSESSION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md` (`S-035`).
- **CONDITION:** human-approved Variant A owner-local scheduled-trigger/adaptive chronology decision explicitly controlled earlier conflicts. A later complete owner is expected but has not yet been proven to fully carry every accepted clause.
- **CURRENT DISPOSITION:** remain in `specs/` pending proof.

### DCR-005 — Condition aggregation/intrinsic-rule-scope decision current-law survival not yet proven

- **TYPE:** `UNRESOLVED_SUPERSESSION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/specs/2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md` (`S-041`).
- **CONDITION:** human-approved orthogonal `ConditionAggregationPolicy × IntrinsicRuleScope` decision is accepted law at that checkpoint; later complete owner has not yet been proven to fully consolidate it.
- **CURRENT DISPOSITION:** remain in `specs/` pending proof.

### DCR-006 — Step-2 final critical review current-law survival not yet proven

- **TYPE:** `UNRESOLVED_SUPERSESSION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md` (`S-043`).
- **CONDITION:** integrated Step-2 final review contains authoritative corrections; later retrospective/current architecture likely supersedes or extends it, but the complete mapping is still pending.
- **CURRENT DISPOSITION:** remain in `specs/` pending proof.

### DCR-007 — WP-06/F02 stale pre-realization B′ wording remains in domain-rules coverage documentation

- **TYPE:** `CONTRADICTORY_OR_STALE_WORDING` / `DEFERRED_LATER_STAGE_OBLIGATION`.
- **STATUS:** `EXPECTED_DEFERRED`.
- **OWNER_TRIAGE:** PENDING.
- **STALE SURFACE:** `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`.
- **CURRENT AUTHORITY:** current machine binding + completed S6D closure.
- **CONDITION:** pre-realization wording still says B′ is not materialized/blocked although the current machine binding and S6D closure already control.
- **NAMED RESOLUTION STAGE:** `WP-26` under preserved `WP-06/F02` obligation.
- **REFRACTOR RULE:** do not opportunistically discharge or rewrite the WP-06 finding during this refactor; preserve the debt explicitly.

### DCR-008 — WP-06/F03 Exploration spatial guidance is not aligned with current bounded spatial contract

- **TYPE:** `CONTRADICTORY_OR_STALE_WORDING` / `DEFERRED_LATER_STAGE_OBLIGATION`.
- **STATUS:** `EXPECTED_DEFERRED`.
- **OWNER_TRIAGE:** PENDING.
- **STALE SURFACE:** `GAME/CORE/EXPLORATION.md` spatial-record/map guidance.
- **CURRENT AUTHORITY:** bounded location/procedure/applicability contract established by current architecture.
- **CONDITION:** wording needs alignment without introducing a generalized spatial engine.
- **NAMED RESOLUTION STAGE:** `WP-26` under preserved `WP-06/F03` obligation.
- **REFRACTOR RULE:** do not opportunistically discharge during this refactor.

### DCR-009 — Legacy `runtime.message` campaign-sequential identity conflicts with Step-5.8 live-born identity law

- **TYPE:** `CONTRADICTORY_OR_STALE_WORDING` / `DEFERRED_MACHINE_REALIZATION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **STALE/MACHINE SURFACE:** current catalog/identifier policy describing `runtime.message` as campaign-scoped sequential stable ID.
- **CURRENT LAW:** Step 5.11 delegates live-born message identity to Step 5.8: independently writable live sources require collision-free source-native/live-epoch-safe stable identity, preserved through close/absorption without renumbering.
- **WHY IT MATTERS:** a single campaign sequential allocator creates contention/collision semantics inconsistent with accepted live ownership.
- **NAMED RESOLUTION STAGE:** R2.7 machine realization / implementation planning after architecture closure.

### DCR-010 — Legacy live-scene knowledge/disclosure wording risks duplicate writable authority

- **TYPE:** `DUPLICATE_OWNER_RISK` / `CONTRADICTORY_OR_STALE_WORDING`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **STALE SURFACE:** legacy `LIVE_SCENE.md` wording allowing compact per-PC knowledge/disclosure information.
- **CURRENT OWNERS:** `world.knowledge` for fictional epistemic state and `runtime.disclosure` for material human-player exposure under Step 4.
- **CONDITION:** live-local operational evidence/routing may still be valid, but it must not survive machine realization as a second writable global knowledge/disclosure owner.
- **NAMED RESOLUTION STAGE:** machine realization / live normalization.

### DCR-011 — Step-3 stable host invocation identity requirement lacks a proven ordinary-ChatGPT primitive

- **TYPE:** `DEFERRED_HOST_CAPABILITY`.
- **STATUS:** `EXPECTED_DEFERRED`.
- **OWNER_TRIAGE:** PENDING.
- **SEMANTIC REQUIREMENT:** Step 3 distinguishes same intentional prose later (new Interaction) from transport retry of the same invocation (same Interaction), requiring stable invocation identity semantics.
- **CAPABILITY GAP:** current ordinary ChatGPT product/runtime documentation/tool surface has not proven a stable machine-visible host invocation/message/revision identity or retry ancestry primitive sufficient for this mapping.
- **WHY IT MATTERS:** content hash/equality cannot safely distinguish retry from a later intentional same-text action.
- **NAMED RESOLUTION STAGE:** Step 6 / host-deployment feasibility and capability profiles.
- **NOTE:** this is not yet a contradiction in accepted architecture; it is a deployment prerequisite that must not be forgotten or silently assumed solved.

### DCR-012 — `runtime.disclosure` is canonical semantic authority but missing from current machine catalog/schema

- **TYPE:** `MISSING_REALIZATION` / `DEFERRED_MACHINE_REALIZATION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT LAW:** Step 4 establishes `runtime.disclosure` as durable human-player exposure authority for material information whose prior exposure matters.
- **MACHINE GAP:** current `core-catalog.json`/schemas do not yet realize this runtime kind/schema.
- **NAMED RESOLUTION STAGE:** R2.7 machine realization.

### DCR-013 — `runtime.message` / `runtime.interaction` semantic contracts are ahead of schema realization

- **TYPE:** `MISSING_REALIZATION` / `DEFERRED_MACHINE_REALIZATION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT LAW:** Step 3/Step 5.11 define accepted Interaction/message identities, message retention/compaction semantics and stable linkage.
- **MACHINE GAP:** concepts are admitted in catalogs/policy, but current DEV schemas do not yet fully define their runtime-record structures.
- **NAMED RESOLUTION STAGE:** R2.7 machine realization / implementation planning.

### DCR-014 — Story architecture is canonical but the current campaign machine layout lacks its realization

- **TYPE:** `MISSING_REALIZATION` / `DEFERRED_MACHINE_REALIZATION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT OWNERS:** Step 4 + Step 5.10.
- **MACHINE GAPS (preserve item-level):**
  1. campaign template has no realized `STORY/` tree;
  2. manifest has no static `story_root` routing field;
  3. no four-layer Story record/index schemas;
  4. no `StoryLayerProjectionState` schema;
  5. no Story-local non-reusing allocator realization;
  6. no typed source projection-domain/coverage protocol;
  7. no semantic projection-contract generation compatibility/migration realization;
  8. no deterministic `StorySourceBundle` / `StoryProjectionDraft` machine protocol;
  9. no Story-only movement classification in RepositoryPort conflict handling;
  10. no Commentator/retrieval lag-status machine representation;
  11. no structural correction/no-dangling-ref tooling;
  12. no Story-specific integrity/repair tooling.
- **NAMED RESOLUTION STAGE:** R2.7 realization / later implementation planning; physical invocation policy remains Step 6.

### DCR-015 — Step-5.11 message retention/compaction architecture has substantial unrealized machine obligations

- **TYPE:** `DEFERRED_MACHINE_REALIZATION`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT OWNER:** `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`.
- **UNREALIZED OBLIGATIONS (preserve item-level):**
  1. `runtime.message` schema/paths;
  2. interaction/message publication closure;
  3. accepted-text normalization/exactness contract;
  4. whole/slice exact-text references;
  5. content/slice digest rules;
  6. `EXACT_RETAINED -> COMPACTED` state transition;
  7. compact provenance envelope;
  8. semantic-content discharge validation;
  9. typed exact dependency declaration by admitted owner kinds;
  10. durable bounded reverse protection routing/index;
  11. natural-owner promotion for contracts/documents/puzzles/mechanics;
  12. Story/Transcript source contract under Selective Exact;
  13. `MAY_OMIT` and typed `MUST_MATERIALIZE` archival rules;
  14. deterministic Transcript exact certification/revocation;
  15. source-enumeration/cursor continuity through compaction;
  16. Step-5.8-compatible live message IDs/routing;
  17. host edit/retry/branch divergence hooks;
  18. OOC/private/safety minimization policy realization;
  19. multiplayer provenance/availability integration;
  20. exact-unavailable historical query semantics;
  21. legacy migration statuses;
  22. Step-5.12 outbound qualification integration;
  23. Step-5.13 envelope-GC integration;
  24. compaction CAS/ambiguous-ACK handling;
  25. integrity/repair tooling;
  26. bounded maintenance/performance tests.
- **NAMED RESOLUTION STAGE:** R2.7 realization/implementation; 5.12, 5.13 and Step 6 own their named handoffs.

### DCR-016 — Physical corpus migration is not yet executable with proven branch-complete inbound-reference repair

- **TYPE:** `REFACTOR_OPERATIONAL_DEBT`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CONDITION:** semantic destinations are already known for many files, but current GitHub code-search behavior on the non-default branch has not proved a branch-complete repository-wide inbound-reference census.
- **WHY IT MATTERS:** moving files without complete path repair can create broken live Markdown/tool/test references; duplicating files to avoid broken refs would violate the no-duplicate-current-owner goal.
- **CURRENT DISPOSITION:** physical moves remain deferred until a reliable inbound-reference/path-repair method is established. Semantic census continues independently.

### DCR-017 — Active R2.7 audit-status artifact is semantically `design/` but still physically under `research/`

- **TYPE:** `REFACTOR_OPERATIONAL_DEBT` / taxonomy misplacement.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **FILE:** `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`.
- **CURRENT TAXONOMY:** audit mini-reports/status/cursors are `design/` provenance/operational process artifacts, not research results.
- **SPECIAL REQUIREMENT:** this is the active operational cursor, so migration must be a true move with all live references repaired; no duplicate temporary owner.

### DCR-018 — Step-5.12 host delivery/disclosure contract has residual machine and host-profile realization obligations

- **TYPE:** `MISSING_REALIZATION` / `DEFERRED_MACHINE_REALIZATION` / `DEFERRED_HOST_CAPABILITY`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT OWNER:** `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`.
- **ALREADY TRACKED ELSEWHERE:** message ID conflict (`DCR-009`), live knowledge/disclosure duplicate-owner risk (`DCR-010`), host invocation/retry identity (`DCR-011`), missing `runtime.disclosure` kind/schema (`DCR-012`), incomplete message/interaction record realization (`DCR-013`). These are not duplicated here.
- **RESIDUAL OBLIGATIONS (preserve item-level):**
  1. typed `NarrationResult` material `disclosure_refs` plus deterministic completeness/eligibility validation before player-visible admission;
  2. coherent HOT `OutboundEmissionClosure` joining admitted outbound `runtime.message` evidence with recipient-scoped `runtime.disclosure` transitions and required provenance/index updates;
  3. Step-5.5/5.6 dirty publication plus SAVE/controlled-handoff integration without introducing a generic second per-response repository write;
  4. authenticated player/session recipient or audience binding sufficient for the supported per-player disclosure profile;
  5. physical host realization of the pre-player-visible admission/staging boundary and inventory/fencing of auxiliary player-visible surfaces under the R2.6 behavioral-containment contract;
  6. player-facing interruption/Retry/edit/branch guidance that accurately documents the owner-accepted presentation-risk boundary.
- **WHY IT MATTERS:** these obligations are part of current accepted Step-5.12 semantics but are not discharged merely by the existing catalog identifiers or host-assurance architecture candidate. Losing them during later planning would weaken the information/disclosure boundary or accidentally reintroduce a delivery subsystem the owner rejected.
- **NAMED RESOLUTION STAGE:** R2.7 machine/instruction/test realization and later implementation/MVP acceptance under R2.6; physical host/profile details remain governed by the accepted host-assurance contract.
- **REFRACTOR RULE:** preserve visibility only; do not implement or redesign these obligations during the documentation corpus refactor.

### DCR-019 — Step-5.13 cleanup contract is canonical but its machine/protection/ref-cleanup realization is not yet closed

- **TYPE:** `MISSING_REALIZATION` / `DEFERRED_MACHINE_REALIZATION` / `DEFERRED_HOST_CAPABILITY`.
- **STATUS:** `OPEN`.
- **OWNER_TRIAGE:** PENDING.
- **CURRENT OWNER:** `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`.
- **ALREADY TRACKED ELSEWHERE:** Step-5.11 message-envelope compaction/GC integration remains visible in `DCR-015`; this item preserves the broader Step-5.13 cleanup contract without duplicating that message-specific debt.
- **RESIDUAL OBLIGATIONS (preserve item-level):**
  1. target-kind cleanup-contract admission and contract-generation/runtime compatibility semantics, including retain-only handling for unknown/incompatible legacy targets;
  2. deterministic ephemeral current-basis `SafeRetirementAssessment`/equivalent implementing native terminality/replacement, blocker closure, survivor closure, reference-survival validation and resulting-state validation;
  3. explicit distinction between best-effort candidate discovery and correctness-complete typed protection routing whose absence may participate in irreversible negative proof;
  4. protection-routing enrollment/removal/currentness coherence with consuming native owners, plus safe retirement of old protection-routing generations after a compatible successor is current;
  5. blocker-creation source classification and bounded cross-source protection registration/self-contained-consumer/source-fence protocol; campaign CAS alone is insufficient where an independent writable source can create a blocker;
  6. machine reference-survival semantics equivalent to `REQUIRES_CURRENT_TARGET`, `OPAQUE_STABLE_PROVENANCE`, and `SURVIVOR_BACKED`, with unknown legacy references conservative by default;
  7. survivor-before-removal ordering and coherent same-domain replace+delete versus cross-domain survivor-first publication behavior;
  8. minimum long-lived execution/idempotency/result survivors after detailed command/resolution/trace retirement, without invented time-based expiry;
  9. checkpoint retirement including coherent `last_checkpoint_id` replacement/clear semantics and pinned-revision bounded support reads;
  10. message-envelope retirement only after Interaction/raw-link/idempotency/reference contracts are discharged or migrated; verified-exact Story certification/source-enumeration continuity must survive where promised;
  11. chronology and Story cleanup must consume their owner-specific protected-consumer/coverage/reference contracts rather than introduce a global graph/frontier;
  12. valid sparse `runtime.disclosure` rows remain outside generic age/progression-based GC absent an explicit owner-preserving migration contract;
  13. live-ref cleanup classes and nonreused epoch/source identity: ACTIVE and CLOSED_UNABSORBED cannot be removed, absorbed/proven orphan refs are optional cleanup, unclassified noncurrent refs retain/report rather than gain or lose authority by branch existence;
  14. RepositoryPort/host ref-delete capability plus accepted/rejected/indeterminate delete-result verification; the current Connector surface does not itself prove an available delete-ref operation for runtime use;
  15. semantic retention/current-tree retirement/Git-history reachability remain distinct; ordinary runtime must not mine transport history to silently restore semantically compacted exact text and must not claim secure erasure without a separate explicit protocol;
  16. bounded maintenance candidate enumeration, integrity/repair diagnostics, concurrency/currentness retry behavior, and focused regression/performance coverage without a mandatory background worker or all-campaign ordinary-path scan.
- **WHY IT MATTERS:** moving Step-5.13 derivation out of `specs/` is correct only if the final canonical owner plus durable debt routing still expose every implementation obligation required to prevent false-positive irreversible cleanup.
- **NAMED RESOLUTION STAGE:** R2.7 machine realization / later implementation planning and maintenance tooling; transport-specific ref deletion remains capability-gated.
- **REFRACTOR RULE:** preserve and route these obligations; do not implement cleanup architecture or change retention semantics during the documentation corpus refactor.

### DCR-020 — Step-5.14 canonical retains stale physical role-isolation/reset feasibility wording after single-context amendment

- **TYPE:** `CONTRADICTORY_OR_STALE_WORDING` / `EXPLICIT_SUPERSESSION_BUT_OLD_NORMATIVE_COPY_REMAINS`.
- **STATUS:** `RESOLVED_BY_CURRENT_OWNER_BUT_STALE_SURFACE_REMAINS`.
- **OWNER_TRIAGE:** PENDING.
- **STALE SURFACE:** `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`, specifically the Law 5.14-5 example list and Step-6 feasibility ledger SD-5 that treat genuine role-context isolation/reset as a blocking baseline physical requirement.
- **CURRENT AUTHORITY:** `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` plus `2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md` for physical role-containment/topology sequencing. They explicitly supersede mandatory physical role isolation/reset for baseline gameplay and adopt one LLM / one physical chat context with logical role rebinding/eligibility boundaries.
- **PRESERVED STEP-5.14 AUTHORITY:** Step-5.14 remains current for its Step-5 closure, Laws 5.14-1..4 and the general Law 5.14-5 principle that deployment infeasibility must not silently weaken accepted semantics. Only the conflicting physical role-isolation/reset implication is stale.
- **WHY IT MATTERS:** an implementation planner reading only the current Step-5.14 canonical final could incorrectly resurrect a retired baseline topology requirement and reopen solved physical-role-isolation work.
- **CURRENT DISPOSITION:** keep Step-5.14 canonical final in `specs/`; do not demote/split it. During final routing/consolidation repair, make the later single-context amendment/program owner route unambiguous and ensure SD-5 is not treated as a current baseline obligation.
- **REFRACTOR RULE:** documentation/routing repair only; do not redesign role containment.

## 3. Global tracking notes

- The five unresolved early supersession cases are currently exactly `DCR-002` through `DCR-006`.
- New issues discovered during every subsequent specs/research file review must be appended here before the corresponding census slice is considered complete.
- A design file being noncanonical is **not** automatically an issue. Record it only when there is real duplicate-current-owner ambiguity, stale/contradictory wording, unresolved accepted law, named deferred obligation, missing realization, or another material debt.
- Coverage does not activate deferred work. `EXPECTED_DEFERRED` items remain obligations, but the refactor must not manufacture current implementation work from them.
- At final closure, produce a separate frozen report grouped at least by:
  - unresolved dual/current-owner conflicts;
  - stale or contradictory documentation;
  - unresolved supersession;
  - later-stage obligations/deferred architecture;
  - machine realization debt;
  - host/deployment capability debt;
  - refactor/path-migration debt;
  - issues resolved by this refactor.