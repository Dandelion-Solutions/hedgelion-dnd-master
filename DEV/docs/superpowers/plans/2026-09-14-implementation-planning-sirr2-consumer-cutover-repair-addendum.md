# HDM Implementation Planning — SIRR2 Shipped LIVE / Chronology Consumer Cutover Repair Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR OVERLAY AFTER INDEPENDENT SENIOR RE-REVIEW #2 — EXECUTION NOT AUTHORIZED**
Date: 2026-09-14
Repair baseline: `10a75f6d713044a6f7b7d9799166539179739cd6`
Finding authority: `2026-09-13-implementation-planning-independent-senior-re-review-2-result.md`
Production implementation authorized: **NO**.

This addendum repairs `SIRR2-001`. It is a mandatory later-precedence overlay on the current implementation-planning package. It does not change accepted architecture, create a readiness identity, activate trigger-gated work, or authorize production implementation.

Effective precedence for affected material is:

```text
base RD plan
-> 2026-09-13-implementation-planning-sirr-repair-amendments.md
-> 2026-09-13-implementation-planning-author-self-review-repair-addendum.md
-> 2026-09-13-implementation-planning-author-second-pass-repair-addendum.md
-> THIS SIRR2 ADDENDUM
```

Later text supersedes only conflicting repaired detail.

## 1. Root-cause disposition

The independent finding is confirmed.

The planning package correctly routed `GAME/CORE/LIVE_SCENE.md` and `GAME/CORE/MULTIPLAYER.md` to WP-16/RD-09 ownership, but `OWNER_ROUTED` was mistakenly treated as sufficient consumer closure even though no executable RD task named those file modifications, their RED/GREEN acceptance, their module-version consequences, or their cross-owner proof joins.

The same trace exposed additional stale shipped-consumer assertions already identified by canonical WP-16 §16 but omitted from the worker route:

- `LIVE_SCENE.md` still makes physical scene participation a write-owner boundary;
- `LIVE_SCENE.md` still describes epoch-local provisional IDs that rekey/convert on compaction instead of preserving accepted `source_native_live` identity;
- `LIVE_SCENE.md` still treats one logically resolved player action as at most one LIVE write instead of native durability-edge granularity;
- `LIVE_SCENE.md` still permits scene-centric physical packaging wording to look like Knowledge/Disclosure/history authority;
- `MULTIPLAYER.md` still contains the stale close -> compact -> deactivation sequence instead of the no-window campaign authority closure required where revocation intersects LIVE routing/control;
- `MULTIPLAYER.md` still names `CURRENT.world_time.frontier` and local scene frontiers as chronology representation;
- `DEV/TESTS/LIVE_SCENE_CASES.md` still preserves stale one-action/one-write, scene-ownership and orphan-cleanup expectations;
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` still preserves the stale LIVE-removal sequencing.

These are realization/consumer debt under already-accepted WP-15/WP-16 laws. No Product-Owner decision, architecture reopening or new semantic owner is required.

## 2. RD-09 impact-envelope replacement/addition

Base route: `2026-09-13-RD-09-principal-live-currentness-plan.md` plus earlier mandatory overlays.

Add the following exact writable surfaces:

```text
EXISTING_MODIFY GAME/CORE/LIVE_SCENE.md
EXISTING_MODIFY GAME/CORE/MULTIPLAYER.md
EXISTING_MODIFY DEV/TESTS/LIVE_SCENE_CASES.md
EXISTING_MODIFY DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md
EXISTING_MODIFY DEV/TESTS/test_rd09_access_live.py
```

`GAME/CORE/MULTIPLAYER.md` is one shared shipped consumer of both WP-16 LIVE/access semantics and WP-15 chronology semantics. RD-09 performs the one physical file edit because the file already requires the broader WP-16 cutover; the chronology subsection **consumes** the current RD-08/WP-15 typed sparse chronology contract. This physical writer assignment transfers no chronology ownership to RD-09.

RD-08 remains semantic/machine owner for WP-15 realization. RD-09 must fresh-read the current RD-08 plan, WP-15 owner and current `MULTIPLAYER.md` before the shared consumer write. The package proof joins both owners afterward.

## 3. New RD-09 task — shipped LIVE / multiplayer CORE consumer cutover

Insert after the owner-local claim/currentness/identity/lifecycle semantics exist and before RD-09 integrated completion is claimed.

### Files

- Modify: `GAME/CORE/LIVE_SCENE.md`.
- Modify: `GAME/CORE/MULTIPLAYER.md`.
- Modify: `DEV/TESTS/LIVE_SCENE_CASES.md`.
- Modify: `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md`.
- Modify: `DEV/TESTS/test_rd09_access_live.py`.
- Modify `DEV/TOOLS/audit_engine.py` only if a stable exact stale-contract assertion is useful and does not substitute for the focused behavior/integration witnesses.

### RED — `ShippedLiveCoreCutoverTests`

Required named cases:

```text
test_live_core_claim_scope_is_not_scene_membership
test_live_core_preserves_source_native_identity_without_rekey
test_live_core_uses_native_durability_edges_not_one_action_one_write
test_live_core_physical_information_is_not_native_information_authority
test_live_core_closed_unabsorbed_remains_selected_truth_without_fallback
test_live_case_catalog_preserves_retained_refs_and_current_claim_semantics
```

The suite is RED while current shipped prose/case catalogs still permit any of:

- physical scene membership or same-scene reference proximity as write authority;
- one scene-wide implicit mutable-owner set instead of immutable typed claims;
- accepted LIVE-born identity replacement/rekey on absorption;
- one high-level message/action as the required atomic LIVE durability boundary;
- physical LIVE fields as a second Knowledge/Disclosure/history authority;
- campaign base as fallback for selected `CLOSED_UNABSORBED` truth;
- orphan/stale live-ref deletion/cleanup as a normal runtime action.

### GREEN — `LIVE_SCENE.md`

Reconcile the current module to the already-accepted WP-16 contract:

1. Replace scene-wide ownership wording with an immutable typed claim-set/currentness model. A live source may physically pack several owners, but authority exists only for admitted `EXACT_OWNER`, `EPOCH_LOCAL_CREATION`, or already-owner-defined partition claims.
2. State explicitly that scene membership, co-location, participants, references and physical presence in `LIVE_STATE` do not expand the claim set or transfer native semantic ownership.
3. Replace provisional-ID/rekey wording with `source_native_live` semantics for externally referenceable durable LIVE-born owners: identity is accepted at the native LIVE edge, needs no campaign allocator and survives recovery/absorption unchanged.
4. Replace “one logically resolved shared action -> at most one LIVE write” as a correctness law. Physical one-file packing remains an optimization only; one high-level action may contain multiple native establishment/durability edges and those edges retain owner-defined atomicity.
5. Recast physical objective/information/event fields as evidence/projections unless their native owner is itself lawfully claimed/routed. Knowledge, Disclosure, accepted SemanticEvent/history and Story remain their existing owners.
6. Preserve exact-source ACTIVE -> CLOSED fencing and the two-phase close/normalize/handoff/absorb law. If later work fails/indeterminate, exact final CLOSED source remains `CLOSED_UNABSORBED` selected truth with zero ordinary writers; no reopen and no campaign-base fallback.
7. Recast overlap/transfer/recovery wording in terms of exact claimed native owners/owner-defined partitions and selected exact source revisions, not scene/entity physical participation or touched-path ownership.
8. Preserve the accepted retained-ref policy: old/orphan/nonselected live refs may remain physically present but are non-authoritative; runtime never deletes/recreates authority from their mere existence.

### RED — `MultiplayerCoreCutoverTests`

Required named cases:

```text
test_multiplayer_live_authority_is_claim_scoped_not_scene_wide
test_multiplayer_revocation_uses_no_window_campaign_authority_closure
test_multiplayer_has_no_global_or_scene_chronology_frontier_authority
test_multiplayer_uses_typed_sparse_chronology_for_material_bridges
test_multiplayer_transport_order_does_not_create_fictional_chronology
test_membership_case_catalog_matches_no_window_revocation
```

The suite is RED while current shipped wording still:

- treats the whole shared scene/per-PC physical live payload as one authority boundary;
- permits route release/absorption and membership/control revocation to publish separately in an order that leaves stale authorization usable;
- names `CURRENT.world_time.frontier` or generic local scene frontiers as chronology authority;
- derives fictional ordering from commit/CAS/ref/source-transition order.

### GREEN — `MULTIPLAYER.md`

Reconcile the current module without changing semantic ownership:

1. Shared LIVE authority is selected per exact typed claim/current source, not from physical scene participation. Campaign branch remains current for unclaimed owners.
2. For deactivation/controller/policy withdrawal intersecting ACTIVE LIVE claims: exact-source close/fence occurs first; then, where separate campaign writes could leave old routing or authorization usable, route/claim release or absorption and PLAYER/control/policy change publish in one coherent campaign authority closure; successor selection starts only from the new current campaign basis.
3. Additive activation/reactivation may avoid rollover only when immutable claims and existing writer authorization remain compatible under WP-16.
4. Replace the generic global/local frontier chronology paragraph. Cross-scene chronology uses only the minimum owner/evidence-anchored typed sparse relation/provider evidence produced by the current WP-15/RD-08 contract when a concrete material bridge requires it. Independent facts may remain unordered.
5. Git commit order, ref movement, LIVE revision, CAS winner/freeze order, IDs and list order remain non-authoritative for fictional chronology.
6. Campaign/live write-routing prose refers to exact claimed owners and native durability edges, not “everything in the scene”.
7. Physical per-PC observations/live evidence do not become Knowledge/Disclosure authority merely because the shared live source stores them.

## 4. Regression-case catalog cutover

`DEV/TESTS/LIVE_SCENE_CASES.md` is modified in the same coherent checkpoint. At minimum:

- L04 becomes native-durability-edge granularity: one high-level action may require more than one accepted native edge; one-file packing does not merge those semantics.
- L07/L08 state that live physical perception/observation data is evidence/projection and that native Knowledge/Disclosure owners determine semantic/human eligibility.
- L12 states that orphan/nonselected live refs remain retained non-authoritative artifacts and are never deleted/recreated by normal runtime cleanup.
- L19 uses exact claim/current-source transfer and overlap rules, not “entity belongs to scene epoch because it is there”.
- L23–L27 preserve explicit `CLOSED_UNABSORBED` selected truth, zero writers, no reopen and no campaign fallback while phase-B handoff/absorption is incomplete.

`DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` is modified in the same checkpoint. M10 must prove:

```text
exact-source close/fence
-> exact final closed source
-> coherent campaign authority closure when needed:
     absorption/route release + PLAYER/control/policy withdrawal
-> optional successor from new current campaign basis
```

A stale participant cannot retain an authorization window between those campaign-domain facts.

## 5. Focused verification and coherent green checkpoint

Focused commands:

```bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.ShippedLiveCoreCutoverTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.MultiplayerCoreCutoverTests -v
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalMachineAlignmentTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveEnvelopeClaimTests DEV.TESTS.test_rd09_access_live.SourceNativeIdentityTests DEV.TESTS.test_rd09_access_live.LiveLifecycleTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

The coherent green checkpoint contains together:

```text
LIVE_SCENE.md current WP-16 projection
MULTIPLAYER.md current WP-16 projection + consumed WP-15 chronology projection
LIVE_SCENE_CASES.md current regression catalog
MULTIPLAYER_MEMBERSHIP_CASES.md current regression catalog
focused RD-09 shipped-consumer witnesses
RD-08 chronology witness still green
maintenance audit green
```

Do not publish/close an intermediate checkpoint that changes one of the two CORE modules but leaves its paired stale regression catalog as current guidance.

## 6. Version Impact and migration disposition

Planning repair itself changes DEV planning/control documentation only: `VERSION_IMPACT: NONE`.

Future implementation of this task is a material edit to two versioned CORE modules and therefore must perform exactly these module-local updates under current engine `1.0-alpha`:

```text
GAME/CORE/LIVE_SCENE.md
  framework_module_version: 1.0.3 -> 1.0.4

GAME/CORE/MULTIPLAYER.md
  framework_module_version: 0.1.7 -> 1.0.8
```

The `MULTIPLAYER.md` prefix moves to current engine line `1.0` and its existing module-local revision increments `7 -> 8`, exactly once for this coherent logical edit.

These CORE consumer/projection edits alone do **not** require a campaign-contract-generation or storage-format-generation bump. Any persistent schema/catalog/identifier version consequence remains with its existing owning RD checkpoint and is not manufactured here.

No legacy pre-v1 compatibility shim is added merely to preserve the stale prose contracts.

## 7. Shared-file/currentness join

`GAME/CORE/MULTIPLAYER.md` is a physical shared consumer across WP-15 and WP-16 concerns. The package uses this checkpoint:

```text
RD-08/WP-15 chronology contract + current TemporalMachineAlignment witness
    CONSTRAINS_WITHOUT_ORDERING
RD-09/WP-16 shipped-consumer cutover
    -> one physical MULTIPLAYER.md edit against fresh current bytes
    -> RD-08 TemporalMachineAlignmentTests + RD-09 MultiplayerCoreCutoverTests green
```

This is a shared-file/currentness coordination rule, not a new semantic prerequisite between the owner-local RD-08 and RD-09 runtimes. No second writer should independently patch the chronology paragraph from stale content.

Before this task writes, fresh-read:

- current branch HEAD;
- WP-15 and WP-16 canonical owners;
- RD-08 v2 and current RD-09 route plus all mandatory overlays;
- the four exact shipped consumers/case catalogs above;
- current versioning owner.

Semantic owner/decomposition drift stops the worker and returns to planning authority.

## 8. Proof-row supersession and executable closure

This section supersedes only the affected supporting-route/disposition cells in the existing lossless proof ledgers.

### WP-13 §15 row 38 / R071

Replace the pointer-only dispositions with:

```text
GAME/CORE/MULTIPLAYER.md
  MODIFY — SIRR2 RD-09 shipped-consumer task
  witness: MultiplayerCoreCutoverTests + RD-06 native-domain composition integration

GAME/CORE/LIVE_SCENE.md
  MODIFY — SIRR2 RD-09 shipped-consumer task
  witness: ShippedLiveCoreCutoverTests + LiveLifecycleTests

DEV/TESTS/LIVE_SCENE_CASES.md
  MODIFY — retire stale one-action/scene-owner/cleanup expectations
  witness: ShippedLiveCoreCutoverTests.test_live_case_catalog_preserves_retained_refs_and_current_claim_semantics

DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md
  MODIFY — retire stale revocation sequence
  witness: MultiplayerCoreCutoverTests.test_membership_case_catalog_matches_no_window_revocation
```

`Wp13DurabilityProofTests.test_wp13_38_stale_consumer_and_test_dispositions_are_complete` remains RED until these exact current bodies and their owner tests are green. “OWNER_ROUTED”, aggregate stale scan, maintenance audit or CI success alone cannot discharge row 38.

### WP-15 §13 item 16 / R077

Expand the current item-16 route from only `CHRONOLOGY.md + PROCESSES.md` to:

```text
RD-08 TemporalMachineAlignmentTests:
  CHRONOLOGY.md + PROCESSES.md + temporal owner contract

RD-09 MultiplayerCoreCutoverTests:
  MULTIPLAYER.md chronology consumer has no CURRENT.world_time.frontier / generic scene-frontier authority
  and consumes only typed sparse WP-15 relation/provider evidence for concrete material bridges
```

`Wp15TemporalProofTests.test_16_core_temporal_wording_reconciled` requires both sides green.

### WP-16 §15 / R080

The existing item witnesses remain, but the following rows additionally require shipped-consumer proof from this task:

```text
5/7   typed claims + bounded WriteAuthority -> ShippedLiveCoreCutoverTests claim-scope witness
10/11 lifecycle/revocation -> LiveLifecycleTests + both shipped CORE cutover classes + M10 catalog witness
14    no allocator/rekey -> SourceNativeIdentityTests + shipped LIVE identity wording witness
17    transport order not chronology -> ChronologyBridgeTests + MultiplayerCoreCutoverTests
18    information-owner separation -> LiveInformationNormalizationIntegrationTests + shipped LIVE/multiplayer wording witness
20    recovery state matrix -> LiveCurrentness/LiveLifecycle + CLOSED_UNABSORBED shipped wording witness
21    native durability-edge granularity -> accepted execution/CAS tests + shipped LIVE/case-catalog witness
```

A machine-only test is not proof that contradictory shipped runtime guidance was removed.

## 9. Bidirectional coverage / package completion reconciliation

Readiness identity accounting remains unchanged:

```text
DIRECT 116
PURE_PROOF 9
COMPOSITE_PARENTS 8
ACTIVE 133
TRIGGER_GATED 12
NO_WORK 79
R004 ABSENT
RD_UNITS 14
```

Repair reverse routes:

```text
R071 / WP13-38 -> RD-06 proof owner + RD-09 exact shipped LIVE/multiplayer consumer cutover
R077 / WP15-16 -> RD-08 chronology owner + RD-09 MULTIPLAYER shared consumer witness
R079/R080 -> RD-09 exact LIVE claim/currentness/lifecycle + shipped CORE/case-catalog convergence
SIP-002 -> closes residual shipped-consumer gap only after exact cutover checkpoint
SIP-008 -> package executability no longer requires worker-invented CORE edits
SIP-009 -> proof completeness binds the actual consumer edits, not OWNER_ROUTED pointers
```

No new readiness ID, RD unit, semantic owner, global frontier, runtime subsystem or wave barrier is introduced.

## 10. Author repair gate

After publishing this addendum and routing it through package/current-progress control:

1. read back exact remote bytes and changed-file list;
2. require hosted validation success on the exact repair HEAD;
3. perform a fresh author adversarial investigation of the repaired package, including adjacent WP-15/WP-16 shipped consumers and case catalogs rather than only SIRR2-001's quoted lines;
4. repair any newly found author defect before another independent Senior review;
5. only a zero-open-finding author investigation checkpoint may hand off to the next genuinely independent Senior review.

```text
SIRR2-001: AUTHOR REPAIR SPECIFIED
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
NEXT_AUTHOR_GATE: PUBLISH + VERIFY + ADVERSARIAL INVESTIGATION
```