# Implementation Planning — Principal -> PLAYER Completeness Routing Addendum

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 9 — SIGNIFICANT**

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

## Disposition

```text
AUTHOR_GRAPH_FINDING_9: REPAIRED_IN_PLANNING
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
