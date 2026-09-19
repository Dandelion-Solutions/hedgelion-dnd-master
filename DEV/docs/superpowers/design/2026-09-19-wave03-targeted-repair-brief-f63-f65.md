# Wave 03 targeted repair brief — F63–F65

Status: **DRAFT / TARGETED IMPLEMENTATION REPAIR REQUIRED**

This is a bounded repair brief from a post-closure author-side implementation audit. It is not a new canonical architecture, a replacement implementation plan, a product-owner decision, or a declaration that Wave 04 is globally blocked. Work from a fresh public ref and apply the normal HDM execution, System-Impact, Version-Impact, checkpoint, and independent re-review process.

## Audit basis

- audited public head: `cb9cd1c209886ecd2984529d3bd7d3f047d17ea7`;
- code-bearing Wave 03 Senior-reviewed head: `9ae3feb74a2d657a081140781899dcbe66819b5b`;
- the former differs from the reviewed head only in four control/plan files, so the audited implementation surfaces are unchanged;
- exact historic hosted validation for the reviewed head was successful, but it did not contain the negative witnesses below.

Primary implementation surfaces:

- `GAME/TOOLS/access_control.py`;
- `GAME/TOOLS/live_state.py`;
- `GAME/TOOLS/history.py`;
- `DEV/TESTS/test_rd09_access_live.py`;
- `DEV/TESTS/test_w03_t08_live_consumers.py`.

Read the current Wave 03 plan, its execution cursor, access-control architecture, LIVE/campaign canonical specs, and `DEV/PRODUCT_OWNER_INPUT.md` before changing behavior.

## Scope and non-negotiable preservation

Repair only the three defects stated here and their directly necessary tests/documentation/version evidence.

Preserve these accepted laws:

- creator authority remains the first campaign-specific initialization commit's authenticated GitHub **login** through the bounded RepositoryPort history route; do not add user-rename continuity;
- stable GitHub account ID is PLAYER binding evidence only; login remains the human-facing invitation/display identifier; do not introduce email identity;
- PLAYER authorization remains the principal -> candidate PLAYER -> exact current PLAYER route;
- selected LIVE source, cursor, route and campaign absorption remain source-native, exact-source and CAS-bound;
- no rollback/reopen path, neutral handoff issuer, secondary authority, global repository scan, or new cross-owner transaction;
- do not touch Wave 05 final-writer surfaces (including `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/MULTIPLAYER.md`, final shared catalog/identifier-policy bytes) unless the System-Impact Gate produces an explicit, accepted exception. None is expected for this repair;
- do not change Wave 04 task scope or represent this brief as a Wave 04 authorization/blocker change.

If an apparently necessary repair would create a new primitive, owner, writer, schema or cross-wave dependency, stop at the System-Impact Gate instead of silently extending this brief.

## F63 — PLAYER resolution can be copied/relocated into an unauthorized grant

### Reproduced counterexamples

The current public `PlayerResolution` is an init-enabled dataclass. `dataclasses.replace()` copies its issuer marker. Therefore:

1. Resolve an ordinary PLAYER whose `mechanical_override_policy` is false.
2. Copy the issued resolution and replace its `player` payload with an otherwise matching record where that field is true.
3. `authorize_operation(..., operation="mechanical_override_policy")` authorizes the copied resolution.

Separately, an issued resolution for campaign A can be supplied to ordinary PLAYER authorization with a different `campaign_id`; it authorizes because the decision is not bound to that selected campaign.

The existing direct-construction and wrong-principal controls do not close either case.

### Required repair outcome

An ordinary PLAYER operation is authorized only from an owner-issued, non-forgeable resolution whose actual decision inputs are bound to the exact selected campaign and exact PLAYER record used for the decision. Copying, rebinding, constructing, or otherwise tampering with a previously issued resolution must fail closed; a valid resolution from a different campaign must also fail closed.

Choose the narrowest owner-local mechanism compatible with the established route. Do not solve it by weakening the fresh PLAYER route or by converting stable ID into creator authority.

### Mandatory negative witnesses

Add RED-first tests demonstrating and then rejecting:

- copied/replaced resolution with escalated `mechanical_override_policy`;
- valid resolution for campaign A submitted as a decision for campaign B.

Retain a positive ordinary PLAYER authorization witness and the existing forged-direct-construction/wrong-principal controls.

## F64 — exact PLAYER currentness omits deactivation semantics

### Reproduced counterexamples

The shared `_player_semantics` projection excludes `status` and `deactivated_by`. That projection is used by exact-resolution checking, frozen access-policy recovery, and access-policy transition publication.

Two observed cases therefore pass when they must fail:

1. A frozen self-reactivation view is presented for publication while the current owner body has the same fields/revision but `deactivated_by="creator"` instead of `"self"`.
2. Recovery accepts an actual current PLAYER body that is inactive/creator-deactivated and returns the frozen active after-view.

### Required repair outcome

Every operation represented as exact current PLAYER/body validation must include the access-semantic status and deactivation provenance in its comparison. Publication and recovery must reject either altered status or altered deactivation actor even when other compared data and revision are unchanged.

Do not turn a current-owner comparison into a revision-only check, and do not create an alternate authority snapshot.

### Mandatory negative witnesses

Add RED-first tests that prove and then reject:

- publication with the `deactivated_by` drift above;
- recovery with inactive/creator-deactivated current PLAYER against the frozen active after-view.

Retain a valid self-reactivation publication/recovery positive path.

## F65 — forward publication accepts fabricated multi-LIVE freeze progress

### Reproduced counterexample

`MultiLiveFreezeProgress` is publicly constructible. `publish_forward_transition` accepts a caller-created `READY_TO_PUBLISH` object based on plan identity/final keys without proving that each asserted terminal source state is the required close successor of the plan's actual source route.

A fabricated progress object which keeps the H0 source `ACTIVE` while claiming `"CONFIRMED_CLOSED"` reaches a forward candidate carrying `FORWARD_SOURCE_FREEZE_COMPLETE`.

### Required repair outcome

Forward publication may proceed only from owner-produced progress whose final entries prove the exact terminal close state for every planned source, including the correct source identity and successor relationship. A caller-created or altered progress object cannot manufacture source-freeze completion. Preserve the legitimate fully verified close-to-forward path and existing no-rollback/reopen law.

The implementation may make progress unforgeable, independently re-derive/validate it at publication, or use an equally strong owner-local mechanism. It must not trust a public status string as the proof.

### Mandatory negative witnesses

Add RED-first tests that prove and then reject:

- a fabricated READY_TO_PUBLISH progress object that retains an active H0 source while asserting a terminal state.

Keep positive witnesses for a legitimate fully closed source set and the established recovery/partial-progress behavior.

## Completion and review gate

Before declaring this repair ready:

1. record the fresh public base and a narrow execution cursor/checkpoint under the existing HDM process;
2. run the focused amended tests, including all three new negative witnesses and their positives;
3. run the relevant Wave 03 cross-surface suite, full maintained DEV discovery, maintenance audit, and the Version-Impact Gate appropriate to the actual changed artifacts;
4. publish a coherent non-force checkpoint and read it back;
5. wait for exact-head hosted validation;
6. leave final disposition as **independent Senior re-review required**. Do not claim Senior PASS or re-close Wave 03 from this repair alone.

The independent review must inspect the final code and executable witnesses, not merely this brief.
