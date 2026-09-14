# Implementation Planning — WP-16 Proof-Ledger Post-Graph Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14

This amendment supersedes only the supporting implementation/test routes for R080 items 1–4 and 12–15 in `2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md`. All other R080/R083 rows retain their existing item-level semantics unless another current overlay explicitly supersedes them.

The base ledger remains a proof plan, not proof result. This amendment exists because the authority/dependency graph audit found producer/mechanism gaps behind several rows that were already marked `CURRENT_PLANNED`.

## R080 exact supersessions

| Item | Exact owner duty | Current supporting route after graph repair | Required item-bound witness state |
|---|---|---|---|
| 1 | stable external user ID distinct from mutable login/display metadata | RD-09 `resolve_principal(...)` + `PrincipalAuthorizationTests`; Finding 9 principal-routing companion excludes mutable login from key | `CURRENT_PLANNED` only while both principal evidence and route-key negatives remain explicit |
| 2 | stable user ID resolves to exactly one current active PLAYER binding | Finding 8 `world.player` machine admission + Finding 9 `PRINCIPAL_PLAYER_ROUTING.yaml` completeness producer + exact direct reload of nominated `world.player` owner(s) + RD-09 current status/binding validation | `CURRENT_PLANNED`; route metadata alone is never the witness |
| 3 | controlled-PC and operation-specific authorization are separate from PLAYER membership | Item-2 exact current PLAYER reload + RD-09 `authorize_operation(...)` + current control basis + RD-12 agency consumer; principal route carries no control grant | `CURRENT_PLANNED` |
| 4 | post-selection mutable gameplay revalidates current owner/application authority | pin current campaign -> current principal-route companion -> exact PLAYER owner reload -> current control/policy -> current campaign/LIVE route -> exact native source; stale card/session/cache/index/companion metadata cannot authorize by itself | `CURRENT_PLANNED` |
| 12 | additive activation/reactivation may avoid rollover only under owner-proven no-conflict conditions | Finding 7 `classify_additive_authorization_change(...)` exact six-predicate decision + `LiveAdditiveAuthorizationTests`/equivalent RD-09 cases; otherwise `LIVE_TRANSITION_REQUIRED` | `CURRENT_PLANNED`; generic `LiveLifecycleTests` alone is insufficient |
| 13 | externally referenceable LIVE-born identity uses explicit `source_native_live`/owner-equivalent admission | Finding 7 identifier-policy schema v3 + exhaustive per-kind `live_birth` disposition table + RD-09 claim admission + `SourceNativeIdentityTests`; Finding 10 supplies MechanicalEvent owner-equivalent composite identity | `CURRENT_PLANNED`; unspecified/conditional per-kind selection is RED |
| 14 | LIVE-born identity never falls back to campaign allocator and never rekeys on absorption | Finding 7 source-native/owner-equivalent/FORBIDDEN table + RD-04 `CampaignAllocatorTests` exact participation set + RD-09 retry/close/absorb tests + Finding 10 MechanicalEvent no-surrogate/no-rekey proof | `CURRENT_PLANNED` |
| 15 | multi-LIVE freeze/forward transition does not create distributed rollback/transaction semantics | Finding 7 ephemeral `FrozenMultiLiveForwardPlan` protocol + `MultiLiveForwardTransitionTests` + RD-09 exact-source close/currentness + RD-06 final campaign forward publication; RD-07 recovery re-derives outstanding forward work | `CURRENT_PLANNED`; generic publication tests without partial-close cases are insufficient |

## Mandatory negatives added to the package witness

The eventual `Wp16LiveAccessProofTests` (or equivalent item-bound implementation proof suite) must explicitly include these negatives; nearby broad tests do not satisfy the row by implication:

### Items 1–4

- mutable login/display metadata cannot resolve PLAYER;
- `PLAYER_INDEX`, session/card/cache and repository write permission cannot authorize;
- missing/invalid/stale principal-route companion is repair/integrity handling, not proof of no PLAYER;
- valid absence from a current complete companion may nominate no PLAYER, but cannot bypass owner-specific onboarding/reactivation rules;
- stale route candidate whose exact PLAYER no longer carries the binding grants nothing;
- multiple current active exact PLAYER matches fail closed;
- inactive same-binding PLAYER may be discoverable for owner-approved reactivation but is not ordinary active authority.

### Item 12

- a participant addition that changes no claims/control/current writer semantics may avoid rollover;
- claim expansion, current-writer revocation or controlled-PC transfer cannot use the additive path;
- insufficient evidence cannot choose optimistic no-rollover;
- activation never grants LIVE write authority without reacquiring current obligations.

### Items 13–14

- identifier-policy schema without explicit `live_birth` disposition for an admitted native kind is incomplete;
- unknown future/stale kind is not silently LIVE-creatable;
- `FORBIDDEN` family cannot appear in `EPOCH_LOCAL_CREATION`;
- `SOURCE_NATIVE_LIVE` accepted creation never calls the campaign allocator and never rekeys on absorption;
- `OWNER_EQUIVALENT` family does not gain a second surrogate merely because it is physically established inside LIVE;
- rejected prospective source-local coordinates are noncanonical.

### Item 15

- one source may become CLOSED while another rejects/stays indeterminate; the accepted close remains real;
- partially frozen state never establishes the dependent fictional/campaign transition;
- campaign publication failure after all closes does not reopen predecessors;
- accepted mechanics/RNG/event identities in one source are never rolled back because another source fails;
- technical close/CAS order is not chronology;
- no 2PC, global LIVE coordinator, rollback transaction, leader, lease or all-ref scan is introduced.

## Proof-closure rule

R080 rows 1–4 and 12–15 may not be considered implementation-proof ready from row count, test-class name or RD adjacency. Closure is item-bound:

```text
owner law
+ executable producer/mechanism
+ exact consumer
+ publication/currentness/recovery join where applicable
+ named positive and negative witness
```

If any component becomes conditional, unnamed or worker-discovered again, that row reverts to RED/OPEN regardless of whether the overall R080 witness count remains 22.

## Final consolidation requirement

Before the next independent Senior plan review handoff, fold these exact route changes into the primary WP-16/WP-17 lossless proof ledger or make the package index/master plan explicitly declare this amendment later/higher precedence. There must be one unambiguous current supporting route per item at the review checkpoint.

```text
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
