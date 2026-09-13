# RD-09 — Principal Authorization / LIVE Identity / Currentness — Executable Implementation Plan

Goal: realize trustworthy principal resolution, PLAYER/control authorization, bounded LIVE claim/current-route lookup, source-native identity and exact-source CAS without creating a global LIVE owner or cross-domain freshness scalar.

Direct readiness: `R013,R014,R019,R020,R040,R078,R079,R080`.
Composite slices: `R053.LIVE,R016.LIVE,R018.LIVE,R122.CURRENTNESS_SCENE`.
Canonical owners: Step-5.8, WP-16, WP-11 identity/routing, WP-12 HOT/currentness, R2.5/WP-17 downstream collaboration.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/access_control.py`
- `NEW_CREATE GAME/TOOLS/live_state.py`
- `EXISTING_REPLACE GAME/SCHEMA/live_scene.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/player.schema.yaml` — current v1 contract already carries stable `github_binding.user_id`, canonical `player_id`, active/inactive state and controlled-PC relations; RD-09 must consume it rather than create a duplicate authority
- `NEW_CREATE DEV/SCHEMAS/live-claim.schema.json`
- `NEW_CREATE DEV/SCHEMAS/live-publication-attempt.schema.json`
- identifier-policy/catalog projections required for `source_native_live`
- `NEW_CREATE DEV/TESTS/test_rd09_access_live.py`
- direct audit/project-map projections only.

Forbidden: login-as-stable-principal, self-declared player authority, global active player, presence/heartbeat authority, scene-wide wildcard claims, path-glob claims, LIVE semantic mega-owner, integer revision/currentness authority, force update, branch-name authority, campaign allocator for LIVE-born identities, ID-order chronology.

## Task 1 — RED: trustworthy principal and PLAYER/control resolution

Create `DEV/TESTS/test_rd09_access_live.py` with failing cases:
- missing/ambiguous stable external user ID fails protected mutation closed;
- GitHub login/display metadata alone never establishes binding;
- exactly one active PLAYER binding is required for ordinary authority;
- active membership does not imply controlled-PC authority;
- repository write permission does not imply gameplay permission;
- session/card/cache projections may nominate but never authorize.

Expected RED: no shipped resolver exists.

## Task 2 — GREEN: `access_control.py`

Implement bounded interfaces equivalent to:
```text
resolve_principal(connector_identity) -> PrincipalEvidence | UNAVAILABLE
resolve_player(principal_id, current_player_records) -> PlayerBindingResult
authorize_operation(player, control_basis, operation, current_policy) -> AUTHORIZED | DENIED
```

Rules:
- stable external user ID and mutable login remain distinct;
- current active PLAYER resolution is exact and non-ambiguous;
- controlled-PC relation is independently checked;
- operation-specific creator/member/mechanical-policy/current-route constraints remain native-owner governed;
- projections never become permission leases.

Commit boundary: principal/PLAYER/control authorization + tests.

## Task 3 — RED/GREEN: replace legacy LIVE envelope

Replace `GAME/SCHEMA/live_scene.schema.yaml` so it represents one selected LIVE epoch/currentness envelope and immutable typed claims, not a scene-owned semantic mega-record.

Required claim grammar:
```text
EXACT_OWNER(native_family, native_identity)
EPOCH_LOCAL_CREATION(native_family)
OWNER_DEFINED_PARTITION(partition_type, partition_key)
```
`OWNER_DEFINED_PARTITION` is legal only when a native owner already defines deterministic bounded partition semantics.

Remove/demote fields that imply LIVE ownership of objective facts, knowledge/disclosure, arbitrary entity overlays or path-glob authority. Retain only lawful source/currentness/claim/lifecycle/evidence projections needed by the accepted owner graph.

Tests prove references do not expand claims and overlapping selected claims produce integrity conflict.

## Task 4 — LIVE route/currentness lookup

Implement in `GAME/TOOLS/live_state.py`:
```text
lookup_write_authority(target_owner, campaign_routing)
select_live_source(epoch, route_basis)
validate_exact_source(expected_revision, current_revision)
```

Result for an owner is bounded `CAMPAIGN | LIVE(epoch, source, exact_revision) | INTEGRITY_CONFLICT`.

Rules:
- ACTIVE selected LIVE is current truth and ordinary writable authority for admitted claims;
- CLOSED_UNABSORBED remains selected truth with zero ordinary writers;
- campaign base cannot silently replace selected LIVE truth;
- campaign, LIVE and local HOT currentness remain domain-separated.

## Task 5 — source-native LIVE identity

Update current identifier-policy/catalog machinery so every admitted externally referenceable LIVE-born native family explicitly supports `source_native_live` or an owner-defined collision-free equivalent.

Identity basis includes stable epoch/source identity + native family domain + accepted source-local creation coordinate/equivalent. It is fixed at acceptance, collision-free across independent LIVE sources, never rekeyed on absorption and has no chronology/priority meaning.

This closes `R013,R019` identity debt and forbids global pre-response/campaign allocator dependency for LIVE-born records.

## Task 6 — frozen LIVE mutation + exact-source CAS result

Add `DEV/SCHEMAS/live-publication-attempt.schema.json` for ephemeral validation and implement:
```text
freeze_live_attempt(...)
revalidate_application_authorization(attempt, current_campaign_basis)
classify_cas_result(...) -> ACCEPTED | REJECTED_STALE | INDETERMINATE
reconcile_indeterminate(...)
```

Frozen attempt contains principal/PLAYER/control basis, selected epoch/claims, target ref, expected exact source revision, affected native owner identities/generations and accepted execution/idempotency refs as applicable.

Rules:
- application authorization is revalidated independently of source CAS;
- non-force exact-source transition is authoritative fence;
- created object alone never proves accepted mutation;
- ambiguity triggers bounded source/lineage reconciliation, not blind replay;
- accepted remote edge is not rolled back because local HOT adoption fails.

## Task 7 — close/absorb/revocation no-window path

Implement owner-lawful lifecycle transitions:
- ACTIVE -> CLOSED is monotonic;
- route-away validates exact final CLOSED source;
- absorption is forward publication, never Git merge/replay semantics;
- authority withdrawal affecting ACTIVE LIVE closes affected source before campaign authorization/routing transition;
- where separate campaign publications would expose stale authority, publish route/control/membership closure coherently under the existing campaign publication owner.

RD-09 prepares typed inputs/results; RD-06 retains campaign publication authority.

## Task 8 — `R122.CURRENTNESS_SCENE` slice

Supply only the currentness/scene-route evidence needed by the composite. Do not infer chronology, Context Runtime relevance or collaboration/waiting semantics.

Activation requires a concrete positive material cross-scope dependency. No campaign-global frontier, universal scene barrier or active-player gate is introduced.

## Task 9 — verification / Version Impact

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact Gate classifies LIVE schema and identifier-policy changes. `player.schema.yaml` is read as existing authority and is not modified by this RD unless a later planning repair, not the implementation worker, explicitly changes that file action. Migration execution remains prohibited.

Negative stale proof must find no active login-as-ID rule, global LIVE owner, branch/integer freshness authority, wildcard claim expansion, force update, allocator dependency for LIVE-born identity, presence-based revocation or ID chronology.

## Currentness fence

Worker must fresh-read WP-16, Step-5.8, WP-11/12 and exact touched files at worker HEAD. Mechanical path drift may be adapted and recorded; semantic owner/decomposition drift stops execution and returns to planning authority.

RD-09 closes only its direct leaves and listed slices. `R122` remains incomplete until RD-08 chronology + RD-11 context + RD-12 collaboration bridge plus parent proof/Version Impact closure.