# RD-09 — Principal Authorization / LIVE Identity / Currentness — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize trustworthy principal resolution, PLAYER/control authorization, bounded LIVE claim/current-route lookup, source-native identity, exact-source CAS and the LIVE-side producer for accepted information normalization without creating a global LIVE, information or cross-domain freshness authority.

Direct readiness: `R013,R014,R019,R020,R040,R078,R079,R080`.
Composite slices: `R053.LIVE,R016.LIVE,R018.LIVE,R122.CURRENTNESS_SCENE`.
Canonical owners: Step-5.8, WP-16, WP-11 identity/routing, WP-12 HOT/currentness, Step-4 §12.2, R2.5/WP-17 downstream collaboration.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: Step-5.8, WP-16, WP-11/12, Step-4 §12.2, exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE: access/principal runtime, LIVE envelope/lifecycle/currentness, source-native identifier-policy projection.
EXPECTED CONSUMERS TO CHANGE: RD-05 execution join, RD-07 selected-LIVE recovery, RD-02 information normalization, RD-12 collaboration, RD-14 creator/product consumer.

ALLOWED CONTRACTS:
- Create `GAME/TOOLS/access_control.py`;
- create `GAME/TOOLS/live_state.py`;
- replace `GAME/SCHEMA/live_scene.schema.yaml`;
- inspect/consume `GAME/SCHEMA/player.schema.yaml` except where RD-12 later owns its collaboration companion;
- create `DEV/SCHEMAS/live-claim.schema.json` and `live-publication-attempt.schema.json`;
- modify exact identifier-policy/catalog projections required for `source_native_live`;
- create/modify `DEV/TESTS/test_rd09_access_live.py`, audit/project-map projections;
- consume `GAME/TOOLS/information.py` at the R053 integration checkpoint; RD-09 does not own that module.

PROTECTED INVARIANTS: login != principal; repository permission != gameplay authority; no global active player; claims are bounded typed ownership; source-native LIVE IDs never use campaign allocator; exact-source non-force CAS is currentness fence; currentness is domain-local; RD-02 owns information normalization; RD-13 owns native history.

## Task 1 — RED: trustworthy principal and PLAYER/control resolution

**Files**
- Create: `DEV/TESTS/test_rd09_access_live.py`
- Create in Task 2: `GAME/TOOLS/access_control.py`

**RED class**: `PrincipalAuthorizationTests`.

Cases: missing/ambiguous stable external user ID fails protected mutation closed; login/display metadata alone never binds; exactly one active PLAYER binding for ordinary authority; membership != controlled-PC authority; repository write permission != gameplay permission; session/card/cache may nominate but never authorize.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.PrincipalAuthorizationTests -v
```
Expected RED because resolver is absent. No RED-only checkpoint.

## Task 2 — GREEN: principal / PLAYER / control authorization

**Files**
- Create: `GAME/TOOLS/access_control.py`
- Modify: `DEV/TESTS/test_rd09_access_live.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Interfaces**
```text
resolve_principal(connector_identity) -> PrincipalEvidence | UNAVAILABLE
resolve_player(principal_id, current_player_records) -> PlayerBindingResult
authorize_operation(player, control_basis, operation, current_policy) -> AUTHORIZED | DENIED
```

Rules: stable external user ID distinct from mutable login; exact one active PLAYER match; controlled actor checked separately; operation-specific creator/member/mechanical/current-route laws remain with their owners; projections never become permission leases.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.PrincipalAuthorizationTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

REFACTOR: identity extraction adapters remain private; no generic ACL service.

Coherent checkpoint: access resolver + tests + audit/project-map projection.

## Task 3 — replace legacy LIVE envelope

**Files**
- Replace: `GAME/SCHEMA/live_scene.schema.yaml`
- Create: `DEV/SCHEMAS/live-claim.schema.json`
- Modify: `DEV/TESTS/test_rd09_access_live.py`

**Claim grammar**
```text
EXACT_OWNER(native_family, native_identity)
EPOCH_LOCAL_CREATION(native_family)
OWNER_DEFINED_PARTITION(partition_type, partition_key)
```
`OWNER_DEFINED_PARTITION` requires pre-existing deterministic bounded owner semantics.

**RED/GREEN class**: `LiveEnvelopeClaimTests`.

Remove/demote objective-fact, knowledge/disclosure, arbitrary overlay or path-glob authority. References never expand claims; overlapping selected claims are integrity conflict.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveEnvelopeClaimTests -v
```
Expected GREEN after replacement.

Coherent checkpoint: LIVE schema + claim schema + focused tests.

## Task 4 — LIVE route/currentness lookup

**Files**
- Create: `GAME/TOOLS/live_state.py`
- Modify: `DEV/TESTS/test_rd09_access_live.py`

**Interfaces**
```text
lookup_write_authority(target_owner, campaign_routing) -> WriteAuthority
select_live_source(epoch, route_basis) -> SelectedLiveSource
validate_exact_source(expected_revision, current_revision) -> SourceValidation
```
Where `WriteAuthority = CAMPAIGN | LIVE(epoch, source, exact_revision) | INTEGRITY_CONFLICT`.

Rules: ACTIVE selected LIVE is current truth/writer for admitted claims; CLOSED_UNABSORBED remains selected truth with zero ordinary writers; campaign base cannot replace it; campaign/LIVE/HOT currentness remain separate domains.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveCurrentnessTests -v
```

Coherent checkpoint: LIVE source/currentness runtime + tests.

## Task 5 — source-native LIVE identity

**Files**
- Modify exact current identifier-policy/catalog artifacts admitting externally referenceable LIVE-born families;
- Modify: `DEV/TESTS/test_rd09_access_live.py`
- Modify: `DEV/TOOLS/audit_engine.py`

Identity basis: stable epoch/source identity + native family + accepted source-local creation coordinate/equivalent. Identity freezes at acceptance, is collision-free across independent LIVE sources, never rekeys on absorption and conveys no chronology/priority.

**RED/GREEN class**: `SourceNativeIdentityTests` proves campaign allocator is never called for LIVE-born Message/execution evidence.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.SourceNativeIdentityTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: identifier-policy/catalog projection + tests/audit. Version Impact Gate runs here.

## Task 6 — frozen LIVE mutation + exact-source CAS

**Files**
- Create: `DEV/SCHEMAS/live-publication-attempt.schema.json`
- Modify: `GAME/TOOLS/live_state.py`
- Modify: `DEV/TESTS/test_rd09_access_live.py`

**Interfaces**
```text
freeze_live_attempt(...) -> FrozenLiveAttempt
revalidate_application_authorization(attempt, current_campaign_basis) -> AuthorizationResult
classify_cas_result(...) -> ACCEPTED | REJECTED_STALE | INDETERMINATE
reconcile_indeterminate(attempt, current_source) -> ReconciliationResult
```

Frozen attempt includes principal/PLAYER/control basis, selected epoch/claims, target ref, exact expected source revision, affected native identities/generations and accepted execution/idempotency refs as applicable.

Cases: authorization revalidated independently of source CAS; non-force exact-source transition is fence; created object alone not accepted mutation; ambiguity reconciles by bounded source/lineage read; accepted remote edge not rolled back on local adoption failure.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.LivePublicationTests -v
```

Coherent checkpoint: attempt schema + CAS runtime + tests.

## Task 7 — LIVE close/absorb/revocation lifecycle

**Files**
- Modify: `GAME/TOOLS/live_state.py`
- Modify: `DEV/TESTS/test_rd09_access_live.py`

Rules: ACTIVE -> CLOSED monotonic; route-away validates exact final CLOSED source; absorption is forward publication not Git merge/replay; authority withdrawal closes affected LIVE before campaign authorization/routing transition; route/control/membership closure uses RD-06 campaign publication where coherence requires it.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveLifecycleTests -v
```

Coherent checkpoint: lifecycle behavior/tests; RD-06 publication remains external owner.

## Task 8 — R053 LIVE producer -> RD-02 information normalizer

**Files**
- Modify: `GAME/TOOLS/live_state.py`
- Consume: `GAME/TOOLS/information.py`
- Modify: `DEV/TESTS/test_rd09_access_live.py`
- Consume RD-13 native SemanticEvent/history interface once its checkpoint exists.

**Interfaces produced/consumed**
```text
extract_material_live_information(selected_live_source, exact_revision) -> tuple[LiveInformationEvidence, ...]
normalize_live_material_evidence(live_evidence, source_basis, recipient_scope) -> InformationNormalizationResult  # RD-02
apply_normalization_candidates_under_native_owners(result, owner_context) -> OwnerApplyResult
```

`apply_normalization_candidates_under_native_owners` is integration orchestration only: it dispatches each typed candidate to its existing owner API. It contains no knowledge/disclosure/history semantics.

**Order**
```text
pin selected LIVE source/revision
-> extract typed material evidence
-> RD-02 normalize
-> validate/apply Lore/Knowledge/Disclosure candidates under native owners
-> validate/apply SemanticEvent draft under RD-13 native history owner when material
-> durable closure/publication under existing owners
-> only then complete handoff/absorption for evidence that must survive
```

**Integration tests** (`LiveInformationNormalizationIntegrationTests`)
- material subject knowledge becomes one native relation; LIVE array is not second current authority after accepted handoff;
- exposure goes only to exact player recipient;
- claim statement alone cannot establish objective truth;
- history draft goes to native SemanticEvent owner, never Story;
- source revision movement invalidates normalization basis;
- required normalization/apply failure blocks/retries handoff rather than dropping material evidence;
- non-material evidence may remain ephemeral without durable relation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveInformationNormalizationIntegrationTests -v
python3 -m unittest DEV.TESTS.test_rd02_information_native_contracts.InformationNormalizationTests -v
```
Expected GREEN before `R053` can close.

Coherent checkpoint: smallest RD-09/RD-02/RD-13 integration wiring + tests; no owner transfer.

## Task 9 — `R122.CURRENTNESS_SCENE` material-bridge slice

**Files**
- Modify: `GAME/TOOLS/live_state.py` only if the currentness evidence adapter is not already produced by Tasks 4/6;
- Modify: `DEV/TESTS/test_rd09_access_live.py`.

Supply only smallest currentness/scene-route evidence for a concrete positive material cross-scope dependency. No chronology, Context Runtime relevance, collaboration waiting, global frontier or universal scene barrier.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.MaterialBridgeCurrentnessTests -v
```

Coherent checkpoint: currentness-scene evidence adapter + tests, or evidence-only no-code closure if Task 4 already exposes the exact interface.

## Task 10 — RD-09 integrated verification / joins

Integration must prove:
- R040 execution uses current authenticated/LIVE source, not source-only tests;
- RD-07 selected-LIVE recovery consumes R079/R080 exact source and respects CLOSED_UNABSORBED zero-writer state;
- R053 normalization join from Task 8 is green;
- creator/product consumer later consumes principal evidence without substituting PLAYER ID for creator provenance.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for current deterministic/scenario obligations.

Version Impact Gate: classify LIVE schema/identifier/API changes and synchronize required projections. `player.schema.yaml` remains inspect/consumer authority for RD-09; RD-12 may explicitly modify it for its collaboration companion under its own repaired plan.

System Impact Gate stops if implementation requires global LIVE ownership, generic ACL/currentness service, campaign allocator for LIVE-born IDs, changed publication authority or information/history ownership.

Negative stale proof: no login-as-ID, global LIVE owner, branch/integer freshness authority, wildcard claim expansion, force update, campaign allocator dependency for LIVE-born identity, presence-based revocation, ID chronology, or LIVE epistemic arrays surviving as second current authority after accepted normalization.

Currentness fence: fresh-read WP-16, Step-5.8, WP-11/12, Step-4 §12.2, RD-02 current plan and exact touched files. Semantic owner/decomposition drift stops execution.

RD-09 closes only its direct leaves and listed slices after their named joins. R053 and R122 parent closure remain package reconciliation work.