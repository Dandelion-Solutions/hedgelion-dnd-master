# R2.7 WP-18 — Step 7 Finding Resolution / Propagation Gate

Status: **STEP 7 COMPLETE — ALL STEP-6 BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-04

Step-6 basis: `8d4057c413c368cdee506d0e5b58d9a2de209c5c`

Step-6 findings:

```text
BLOCKING:     1
SIGNIFICANT:  7
```

This gate resolves and propagates every Step-6 finding into the final WP-18 architecture requirements. It does not modify implementation artifacts.

---

## F18-01 / BLOCKING — player-local horizon may omit consumed shared basis

**Resolution:** `CLOSED`.

Final rule:

A retained player-local horizon has explicit shared-dependency state:

```text
shared_basis.kind = ABSENT | BOUND
```

- `ABSENT`: the local horizon did not consume retained shared planning.
- `BOUND`: the local horizon consumed a shared retained generation. The record MUST preserve the exact consumed `shared_generation` plus bounded shared-basis identity sufficient to resolve that exact retained shared generation.

If `BOUND`, shared basis is mandatory, not an optional hint. Before material use after shared movement, the local horizon MUST be revalidated; incompatible local preparation is rebased or discarded.

This dependency is planning-local coordination only. It establishes neither fictional chronology nor universal campaign freshness.

**Propagation target:** final canonical spec: retained-player-local schema contract, currentness/revalidation, test obligations.

---

## F18-02 / SIGNIFICANT — retained-generation publication/currentness boundary

**Resolution:** `CLOSED`.

Final rule:

- newly computed/edited planning remains an EPHEMERAL candidate until successful publication of the retained-horizon record;
- only a successfully published generation is eligible to be the retained cross-context coordination basis;
- publication failure, defer or conflict does not select the unpublished candidate;
- the previously published compatible generation remains the retained basis where applicable; otherwise retained planning is absent/stale/incompatible;
- native gameplay/canon remains unaffected by planning-publication failure;
- this rule creates no generic gameplay HARD boundary and no second campaign frontier.

**Propagation target:** final canonical spec: lifecycle/publication/recovery; downstream runtime/persistence tests.

---

## F18-03 / SIGNIFICANT — multiplayer disable semantics incomplete

**Resolution:** `CLOSED`.

Final rule:

When campaign mode is not multiplayer, **both retained multiplayer planning families** are semantically inactive:

- `DRAMATURG/SHARED.yaml`;
- `DRAMATURG/PLAYERS/<player_id>.yaml`.

Physical bytes may remain. Single-player preparation remains EPHEMERAL ONLY and does not adopt those retained records as a durable single-player owner.

On multiplayer re-enable, retained shared/local horizons may be discovered and independently revalidated against current mode, membership/control/eligibility and source bases; compatible material may be reused, incompatible material is discarded/rebuilt.

**Propagation target:** final canonical spec: mode lifecycle, recovery, tests.

---

## F18-04 / SIGNIFICANT — player-local membership/control/eligibility invalidation

**Resolution:** `CLOSED`.

Final rule:

The stable PLAYER ID remains the physical route identity, but load/use/write eligibility is current:

- active PLAYER membership required;
- current Dramaturg role/recipient eligibility required;
- where an entry materially depends on a controlled PC/entity, current control/subject compatibility required through WP-16 owners.

PLAYER deactivation makes that retained local horizon unusable while inactive. Control transfer does not transfer another PLAYER's private planning to the successor controller. Incompatible horizon becomes stale/unusable even if bytes remain.

Planning never owns membership or control.

**Propagation target:** final canonical spec: authorization/privacy/currentness; downstream runtime tests.

---

## F18-05 / SIGNIFICANT — `source_basis[]` too generic

**Resolution:** `CLOSED`.

Final source-basis item is typed by the native owner:

```text
owner_domain
owner_type
bounded_identity_or_partition
expected_owner_currentness_evidence   # only where native owner defines it
```

No universal revision scalar/vector exists. Currentness/revalidation delegates to the referenced native owner/domain.

- `SOURCE_ANCHORED_CONSTRAINT` MUST carry sufficient declared source basis.
- `PROVISIONAL_DRAMATURGIC_DIRECTION` carries only the assumptions/anchors actually consumed.
- undeclared unrelated sources do not become dependencies.

**Propagation target:** final canonical spec: record contract and revalidation algorithm; downstream schema/tests.

---

## F18-06 / SIGNIFICANT — physical planning root ambiguous

**Resolution:** `CLOSED`.

WP-18 baseline routes are fixed campaign-root-relative paths:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

No planning registry/index/global graph is admitted. No new MANIFEST root selector is required by WP-18 architecture.

A configurable future selector, if ever justified by downstream scaffold/migration constraints, remains static routing only and cannot own planning currentness.

**Propagation target:** final canonical spec: physical topology; WP-19/WP-20 implementation-scaffold/migration consideration only.

---

## F18-07 / SIGNIFICANT — catalog admission provenance stale

**Resolution:** `CLOSED AS ARCHITECTURE / DOWNSTREAM MACHINE ALIGNMENT OBLIGATION RECORDED`.

Final rule:

`planning_entry_classes` vocabulary remains semantically unchanged, but downstream catalog-alignment work MUST update accepted owner provenance so current planning semantics trace through R2.5 and the final WP-18 realization owner as applicable rather than implying Story/continuity ownership.

No catalog implementation is modified in WP-18 design work.

**Propagation target:** final canonical spec machine-alignment section; Source Manifest traceability section; downstream catalog implementation/test work.

---

## F18-08 / SIGNIFICANT — Source Manifest false current Project-Map negative

**Resolution:** `CLOSED`.

The final open-world Source Manifest:

- removes the claim that current `DEV/PROJECT_MAP.md` routes Story through missing `GAME/CORE/STORY.md`;
- records current Project-Map Story routing through accepted Step-4/Step-5/R2.x owners and actual runtime consumers;
- treats the absent legacy `GAME/CORE/STORY.md` path, if mentioned, only as historical negative evidence that no current monolithic Story CORE owner may be assumed;
- adds `DEV/ARCHITECTURE/CATALOG_ADMISSION.md`, WP-14/WP-17 and other Step-6-discovered material owners.

**Propagation target:** final Source Manifest and canonical traceability.

---

## Step-7 cross-finding consistency check

The repaired requirements jointly preserve:

```text
Actor current intent owner
    != Story retrospective projection
    != Dramaturg prospective preparation

Story layer coverage
    != planning generation
    != campaign/LIVE currentness
    != fictional chronology

published retained planning
    != accepted fiction
    != execution
    != recovery authority
```

No finding requires:

- a global planning frontier;
- a planning scheduler/job queue;
- a global Story index;
- a second truth/knowledge/chronology/currentness owner;
- durable single-player planning;
- a generic source revision vector;
- a new catalog semantic identifier;
- R2.2/R2.3/R2.5/WP-13/WP-16/WP-17 reopen.

---

## Step-7 propagation status

```text
F18_01: CLOSED
F18_02: CLOSED
F18_03: CLOSED
F18_04: CLOSED
F18_05: CLOSED
F18_06: CLOSED
F18_07: CLOSED — downstream implementation alignment obligation retained
F18_08: CLOSED

STEP_6_BLOCKING:      1
STEP_6_SIGNIFICANT:   7
UNRESOLVED_BLOCKING:  0
UNRESOLVED_SIGNIFICANT: 0

HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_8_AUTHORIZED: YES
```

Step 8 may canonicalize only these established/repaired results. No implementation, WP-19 or implementation planning is authorized here.
