# W05.T06 Senior Entry Gate

Status: **PASS / W05.T06 AUTHORIZED**

Date: **2026-10-02**

Reviewed public basis:
`90bed94945c453b0aa5d5d4ae5776e2a6ca0208e`

## Disposition

```text
W05.T05: ACCEPTED / READ BACK
W05.T06 HARD INPUTS: SATISFIED
PRODUCT_OWNER_DECISION_REQUIRED: NO
SYSTEM_IMPACT_GATE_AT_ENTRY: PASS
W05.T06: AUTHORIZED
OUTPUT: W05_PRODUCT_PATHS_READY
W05.T07: NOT STARTED
```

Exact current-head hosted validation:
`Validate engine source` run `36937045996` — SUCCESS, including maintenance
and DEV unit suite.

## Hard-input reconciliation

The stable W05.T06 plan requires:

- `W04_RUNTIME_HOST_COMPOSITION_READY`;
- `W04_RUNTIME_HOST_IO_EXTENSIONS_READY`;
- accepted T07E RuntimeHost/W02 exact-size measurement contract;
- PO-012;
- every completed owner checkpoint consumed by the product paths.

Those inputs are GREEN/current:

1. Wave-04 Senior closure accepted the RuntimeHost trusted-composition chain
   (T00H) and coherent IO/publication/History bridge (T00P) with no remaining
   System-Impact defect.
2. T07E is accepted; RuntimeHost is at 1.0.11 and
   `CampaignPublicationTransport.measure_path_operations(...)` requires exact
   serializer parity with `create_tree` and fail-closed absence.
3. PO-012 is the accepted Commentator perspective owner.
4. W02 durability/publication/recovery owners are accepted.
5. W03 principal/PLAYER/access/LIVE currentness owners are accepted.
6. W04 Context/protected-emission, History/Story/T0/Commentator and
   multiplayer/session consumer outputs are accepted.
7. W05.T02-T04 final catalog/schema inputs are accepted.
8. W05.T05 now supplies accepted bounded discovery, initial-publication and
   blank-scaffold outputs.

No named T06 hard input remains open.

## T07 is not a T06 prerequisite

`MANIFEST.players.player_ids` remains physically present under manifest v4
until W05.T07. That does not block T06.

T06 join/rejoin must route through the accepted principal route and exact
current PLAYER reload and must not consult `players.player_ids` as authority.
This is precisely the behavior T07 later makes physically unrepresentable by
removing the field.

T06 must not edit manifest v5/membership-retirement bytes merely to make its
product tests pass.

## T06 product-composition boundary

T06 owns product-facing composition/use of already accepted runtime
capabilities after campaign selection:

- campaign selection/onboarding;
- creator identity checks;
- multiplayer join/rejoin;
- ordinary retrospective;
- save/exit;
- creation/reuse of one campaign-bound RuntimeHost composition root;
- fail-closed verification that the supplied campaign publication transport
  exposes the accepted exact-size capability.

T06 does **not** own a new repository transport protocol or provider-specific
Git implementation.

The W05.T05-P1 pre-campaign create-if-absent capability is a different
bootstrap phase. It may be physically backed by the same deployment adapter,
but T06 must not treat that pre-campaign capability as sufficient gameplay
publication authority unless the adapter separately satisfies the accepted
`CampaignPublicationTransport` contract.

T08 later owns the final shipped CORE/install/module projection of this wiring.
T08 does not defer the product behavior or capability checks required by T06.

If implementation discovers that the real product composition requires a new
transport operation, changes `CampaignPublicationTransport` semantics, or
allows gameplay/model input to supply/replace repository/LIVE/Context/History
services, stop at System Impact.

## PO-012 boundary

Ordinary retrospective must preserve exactly:

```text
PUBLIC
+ exact current PLAYER disclosure when present
+ at most one explicitly selected currently-controlled PC's
  exact-current epistemic.known knowledge
```

No PLAYER -> PUBLIC-only.

Never union multiple controlled PCs. Caller Story IDs, legacy `visible_to`,
repository possession and session metadata grant no access.

## Entry conclusion

```text
W05.T06: READY
NEXT_EXACT_OUTPUT: W05_PRODUCT_PATHS_READY
```
