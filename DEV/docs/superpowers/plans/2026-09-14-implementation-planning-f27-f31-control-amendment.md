# Implementation Planning — F27–F31 Control Amendment

Status: **CURRENT LATER-PRECEDENCE CONTROL AMENDMENT — PLANNING ONLY**
Date: 2026-09-14
Production implementation: **NO**.

This file amends the current post-graph proof ledger, bidirectional coverage v3 and execution-wave v2 only for Findings 27–31. Exact mechanism text remains in the mandatory LIVE overlays, especially `2026-09-14-implementation-planning-live-epoch-route-identity-addendum.md` and `2026-09-14-implementation-planning-live-opening-routing-native-state-addendum.md`. Exact witnesses/channels are in `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md`.

## Proof routing

Add required post-WP27 rows:

- `PG27`: exact epoch/opening route identity and full route/body/opening-basis validation.
- `PG28`: deterministic candidate preparation idempotency and acknowledgement reconciliation.
- `PG29`: exact pinned campaign `H` to initial LIVE native-state equivalence.
- `PG30`: completeness-protected `STATE/RUNTIME/LIVE_ROUTING.yaml` and bounded write-authority lookup.
- `PG31`: typed LIVE native-state packing, exact selected-source recovery and lossless/idempotent forward absorption.

`PG22` meta-proof must route all five rows. Identity proof alone does not discharge opening, routing, packing or absorption.

## Coverage routing

Forward route:

```text
Step-5.8 / WP-16 / WP-11 accepted LIVE laws
-> F27 exact opening identity/ref realization
-> F28 idempotent candidate preparation
-> F29 exact initial native-state seed from H
-> F30 complete campaign LIVE route companion
-> F31 typed LIVE native-state packing/absorption
-> RD-09 owner mechanisms
-> RD-06 campaign selection/absorption publication joins
-> RD-07 selected-LIVE recovery
-> RD-14 blank routing scaffold
-> RD-16 strict family validation where applicable
```

Reverse route includes the F27 LIVE envelope/opening fields, F28 frozen opening attempt, F29 seed evidence, F30 `LIVE_ROUTING.yaml`, and F31 native-state packing/absorption evidence. All reverse to the accepted owners above; no new readiness ID or native family is created.

## Execution routing

Add owner-local checkpoints:

```text
RD09_LIVE_EPOCH_ROUTE_IDENTITY_READY
RD09_LIVE_OPENING_PREPARATION_READY
RD09_LIVE_OPENING_SEED_READY
RD09_LIVE_ROUTING_READY
RD09_LIVE_NATIVE_PACKING_CORE_READY
```

Campaign opening selection joins those exact RD-09 checkpoints with the RD-06 campaign publication foundation.

RD-16 consumes the earlier RD-09 source-native/live-birth inputs as already required by F24–F26. After RD-16 shared-machine integration, RD-09 performs the final strict-family validation of packed native state. This is checkpoint-level and does not create a whole-RD cycle.

Absorption readiness joins final RD-09 packing validation, exact CLOSED source/lifecycle, required native normalization outputs where material, and RD-06 campaign publication. RD-07 waits only for the route/identity/packing checkpoints it consumes.

## Current closure rule

The current package is RD-01..RD-16 with 22 mandatory overlays and Findings 1–31 planning-repaired / independently unconfirmed. Zero-open author closure is not yet declared. Independent Senior review and production implementation remain blocked.
