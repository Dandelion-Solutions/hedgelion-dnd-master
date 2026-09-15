# Implementation Planning — Principal -> PLAYER Completeness Routing Addendum

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 9 — SIGNIFICANT; extended by AUTHOR FINDING 50 shipped-consumer closure**

## Finding

WP-16 requires a current trustworthy stable external principal ID to resolve to exactly one current active `world.player` binding before ordinary multiplayer authority is granted. RD-09 Task 2 currently accepts a preassembled `current_player_records` collection, but no executable plan produces that collection by a bounded complete route. The generic `PLAYER_INDEX` is only a discovery projection and must not become authorization/completeness authority.

Therefore the package has a consumer without a completeness-protected producer. A worker following RD-09 literally would have to scan the PLAYER family, trust an incomplete projection, or invent a new security route.

## Required v1 realization

Create one fixed campaign-domain derivative companion at:

```text
<state_root>/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml
# default scaffold route: STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml
```

This artifact is **routing completeness evidence only**. It is not PLAYER authority, authorization authority, a login directory, a session registry, or a replacement for `world.player`.

Conceptual machine contract:

```text
PrincipalPlayerRouting {
  schema_version
  entries[]: {
    provider                 # baseline: github
    stable_external_user_id  # stable provider ID, never mutable login/display text
    candidate_player_ids[]   # deterministic unique/sorted set
  }
}
```

Rules:

1. Every current `world.player` with a non-null supported stable external binding appears in exactly one matching routing entry.
2. The companion includes bindings for active **and inactive** PLAYER records so permitted reactivation can find the existing stable `player_id`; activity/authorization is never copied into the companion.
3. Mutable login/display metadata is excluded from the lookup key and is not required in the companion.
4. One stable external ID may temporarily nominate more than one `player_id` only as integrity evidence. The authorization consumer loads every nominated current `world.player` and fails closed on ambiguous/multiple active matches.
5. A route entry only nominates candidate IDs. `resolve_player(...)` MUST direct-route and rehydrate the exact current PLAYER owner record(s), then validate `github_binding.user_id`, current `status`, controlled-PC relation and operation-specific policy under WP-16 before authority is granted.
6. `PLAYER_INDEX.yaml`, card/session/cache data and this companion never authorize.
7. No ordinary authorization path scans `WORLD/PLAYERS`, directory entries, all indexes, Git history, or all refs.

## Publication / writer closure

The companion is updated in the same campaign native-domain durability closure as every mutation that can change the stable principal-binding relation, including:

- creation/admission of a new `world.player` binding;
- supported external-user rebind/change;
- any future owner-approved operation that adds/removes a stable external binding.

Activation/deactivation alone does not need to rewrite the companion when the stable binding is unchanged; current status is always re-read from `world.player`.

A healthy publication may not establish a changed PLAYER stable binding without the matching companion delta, nor publish a companion delta whose referenced PLAYER owner is absent from the same resulting campaign authority state.

RD-06 owns campaign publication mechanics; it does not become authorization owner.

## Recovery and corruption semantics

Normal lookup:

```text
pin current campaign basis
-> load/validate current PRINCIPAL_PLAYER_ROUTING companion
-> lookup supported stable external user ID
-> direct-route candidate player_id(s)
-> rehydrate exact current world.player owner(s)
-> validate owner binding/status/control/operation authority
```

A structurally missing, invalid, stale/inconsistent or basis-incompatible companion is **not** proof of "no player" and must fail closed as bounded integrity/repair handling. It never grants permission to broad-scan on the ordinary hot path.

Maintenance/recovery may deterministically rebuild the companion from the current native PLAYER family because the companion is derivative. Such a family scan is a repair/rebuild operation, not ordinary authorization. Rebuilt output must be validated and published/adopted against the current campaign basis before its absence result is trusted.

An empty valid companion in a new blank campaign is legal.

## RD amendments

### RD-04 — derivative routing substrate / R018 integration

Add a fixed non-authoritative companion contract and schema support. It is not a generic family index and is not hashed native-record routing. Add focused proof equivalent to:

```text
PrincipalPlayerRouteCompanionTests
```

Required cases: complete stable-ID projection; deterministic duplicate aggregation; no login key; direct candidate IDs; non-authority; invalid/missing companion cannot prove absence; rebuild from PLAYER owners; no hot-path scan.

### RD-09 — authorization consumer

Supersede the Task-2 worker-facing input:

```text
resolve_player(principal_id, current_player_records)
```

with the bounded form conceptually equivalent to:

```text
resolve_player(
    principal_evidence,
    current_principal_player_route,
    load_current_player_by_id,
) -> PlayerBindingResult
```

`PlayerBindingResult` is authoritative only after exact current PLAYER rehydration/revalidation. Add negatives for stale route, route/owner mismatch, duplicate active binding, inactive binding, login rename and previous-user rebind.

### RD-06 — publication join

PLAYER stable-binding mutation plus required companion delta is one campaign-domain publication closure. A publication conflict refreshes/revalidates the affected owner + companion basis; it does not accept a split result.

### RD-07 — recovery

Cold recovery uses the current companion as bounded route evidence and exact PLAYER bodies as authority. Companion corruption yields repair/block handling, not fallback to cache/card/session or arbitrary family scan in the ordinary recovery-to-play authorization path.

### RD-14 — scaffold / product consumer

The v1 blank campaign scaffold includes a valid empty `PRINCIPAL_PLAYER_ROUTING.yaml` under `state_root/RUNTIME`. Bootstrap validates it structurally but does not require any PLAYER binding for single-player/new-game readiness unless the owning product mode requires one.

## Proof amendments

WP-16 proof duties 1–4 must include the complete route producer/consumer chain, not only `PrincipalAuthorizationTests`:

```text
stable external principal evidence
-> completeness-protected principal->PLAYER route
-> exact current PLAYER owner reload
-> status/control/operation authorization
```

Required negatives include:

- login-only evidence cannot bind;
- missing valid route entry means no binding only when companion completeness/currentness is proven;
- missing/invalid companion is integrity/repair, not "no player";
- stale candidate no longer matching owner binding grants nothing;
- two active candidates for one stable external ID fail closed;
- inactive self-reactivation candidate is discoverable without treating it active;
- no authorization result comes from `PLAYER_INDEX`, route metadata, session/card/cache, repository write permission or broad scan.

## Shared-file / execution ordering

This repair composes with the family-reconciliation addendum that admits `world.player` into the v1 catalog machine surfaces. The sequence is:

```text
world.player semantic/machine admission
-> fixed principal-routing companion schema/scaffold
-> RD-09 bounded consumer
-> RD-06 publication closure
-> RD-07 recovery proof
-> RD-14 product/scaffold proof
```

No production implementation is authorized by this addendum.

## Finding 50 — shipped MULTIPLAYER join/rejoin consumer cutover

### Proven defect

The current shipped `GAME/CORE/MULTIPLAYER.md` still instructs the join path:

```text
Before treating somebody as a new player, search the player index for an existing binding to the same stable GitHub user ID.
```

That instruction contradicts this addendum's accepted completeness route. Current generic `GAME/SCHEMA/index.schema.yaml` exposes only compact entity-routing fields (`id`, `name`, `aliases`, `status`, `path`, `parent_id`, `tags`, `last_event_id`) and no stable external-user key; current `GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml` is an instance of that generic index contract. Therefore a worker cannot implement the shipped instruction literally without inventing an unowned index field, abusing mutable aliases, or broad-scanning PLAYER records/indexes. All three violate the principal-routing law above.

The existing SIRR2 shared `MULTIPLAYER.md` physical writer correctly cuts over several WP-15/WP-16 stale consumers, but its named final-byte acceptance does not include this later F9 principal-routing join/rejoin instruction. F37/F38 consume the F9 route for access transitions but likewise do not replace the shipped lookup text. F48 removes the separate manifest membership list but does not repair this stale index lookup.

This is a shipped-consumer / worker-must-invent defect, not a new architecture decision.

### Required physical cutover

The already-mandatory SIRR2 RD-09 `MULTIPLAYER.md` shared consumer edit must also reconcile the complete join/rejoin path to the accepted F9 route:

```text
authenticated supported stable external user ID
-> exact current PRINCIPAL_PLAYER_ROUTING companion at one pinned campaign basis
-> bounded lookup of candidate_player_ids, including inactive bindings
-> direct-load every nominated exact current PLAYER owner
-> validate github_binding.user_id + current status + current control/policy
-> decide existing active binding / permitted reactivation / genuinely new enrollment
```

Final shipped wording must state explicitly:

1. Generic `PLAYER_INDEX` remains compact entity discovery/routing only and is not the stable-principal completeness route.
2. Join/rejoin must query `PRINCIPAL_PLAYER_ROUTING`, not search `PLAYER_INDEX` for a field it does not own.
3. Inactive bindings remain discoverable through the principal companion so returning users reuse the same PLAYER identity.
4. A missing/invalid/stale/inconsistent principal companion is integrity/repair handling and cannot be interpreted as "never bound".
5. Normal join/rejoin must not scan the PLAYER family, all indexes, Git history or all refs. A deterministic PLAYER-family rebuild is maintenance/recovery only.
6. Candidate route metadata never authorizes; exact current PLAYER reload/revalidation remains mandatory.
7. Mutable GitHub login/display/aliases never substitute for the stable external user ID.

The existing `MULTIPLAYER.md` final shared writer remains the one physical integration point. F50 adds an acceptance obligation to that writer; it does not create a second writer or semantic owner.

### TDD / exact proof obligation

Extend the existing SIRR2 `MultiplayerCoreCutoverTests` with exact final-byte/behavior cases conceptually named:

```text
test_multiplayer_join_uses_principal_route_not_player_index
test_multiplayer_rejoin_finds_inactive_binding_via_principal_route
test_multiplayer_missing_principal_route_fails_closed_without_broad_scan
```

Required proof:

- final integrated `GAME/CORE/MULTIPLAYER.md` contains the principal-route -> exact PLAYER reload chain for join/rejoin;
- final bytes no longer instruct stable-user lookup through generic `PLAYER_INDEX`;
- `PrincipalPlayerRouteCompanionTests` proves complete active+inactive projection and no hot-path scan;
- `PrincipalAuthorizationTests` proves route nomination is non-authoritative and exact PLAYER reload controls authorization;
- `PlayerAccessTransitionTests` proves genuinely new enrollment/reactivation mutations use the same current owner/companion law;
- stale/missing route negatives cannot fall back to generic index/cache/session/card/broad scan.

`STATIC_AUDIT` over the final integrated CORE bytes plus the focused runtime tests is the primary proof route for the shipped-consumer assertion. A machine-only principal resolver test cannot close F50 while contradictory shipped instructions remain.

### Physical writer / version consequence

F50 is folded into the already-planned single unpublished v1 `MULTIPLAYER.md` integration edit. Preserve F46's exact target:

```text
framework_module_version: 0.1.7 -> 1.0.8
```

Do **not** bump to `1.0.9` merely because F50 was found later; the file has not yet been published as an independently final v1 generation. The SIRR2 WP-15/WP-16 consumer deltas, WP-17 consumer deltas and this F9/F50 principal-route cutover converge into the same final shared edit.

### Runtime-performance consequence

Normal join/rejoin becomes bounded by one completeness-protected principal-route lookup plus direct current PLAYER loads for nominated candidates. Any full PLAYER-family scan is repair-only. This prevents runtime remote/repository work from growing linearly with campaign membership on the ordinary join/rejoin path while preserving fail-closed authority semantics.

### Execution-graph consequence

No new RD, readiness ID, whole-RD ordering edge or independent checkpoint is required. The existing F9 principal-route readiness constrains the already-existing SIRR2 RD-09/WP-16 shared `MULTIPLAYER.md` final integration checkpoint. F50 extends that checkpoint's acceptance/proof surface only.

## Disposition

```text
AUTHOR_GRAPH_FINDING_9: REPAIRED_IN_PLANNING
AUTHOR_FINDING_50: SIGNIFICANT / REPAIRED_IN_PLANNING
F50_ROOT_CAUSE: later principal-routing law was not propagated into the existing shared shipped MULTIPLAYER final-byte acceptance
NEW_RD: NO
NEW_SEMANTIC_OWNER: NO
NEW_EXECUTION_EDGE: NO
MULTIPLAYER_FINAL_TARGET: 1.0.8
NORMAL_JOIN_REJOIN_BROAD_SCAN: FORBIDDEN
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
