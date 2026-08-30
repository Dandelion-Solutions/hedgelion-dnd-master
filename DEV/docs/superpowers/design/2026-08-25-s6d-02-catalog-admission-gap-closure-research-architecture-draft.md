# S6D-02 — Catalog Admission and Gap Closure — Research & Architecture Draft

Status: **STEP 2 COMPLETE — DECISION-READY**

Date: 2026-08-25

Preparation ref: `v1/engine-rearchitecture@6cd408cc321a2c8745496215a29abb8d495da511`

Task Brief: `DEV/docs/superpowers/specs/2026-08-25-s6d-02-catalog-admission-gap-closure-task-brief.md`

## 1. Result

The current Catalog 2.0 registry contains **67 registry families and 571 IDs**. A complete item-level machine ledger was generated at `DEV/CATALOG/catalog-admission-ledger.json`; its schema is `DEV/SCHEMAS/catalog-admission-ledger.schema.json`.

Every registered ID is accounted by exact set equality with `core-catalog.json`:

| Stratum | IDs | S6D-02 treatment |
|---|---:|---|
| `S6D_PRIMARY` | 192 | full admission decision now; missing realization routed to S6D-03…09 |
| `ENGINE_ENUM_CONSISTENCY` | 276 | inherited engine owner; equality/stale-reference consistency |
| `INHERITED_ROUND2` | 103 | `INHERITED_ACTIVE`; exact R2.x/WP owner; no S6D realization obligation |
| **Total** | **571** | **zero unclassified** |

No registered ID remains in a placeholder admission state. No current machine ID requires removal in S6D-02: the Catalog 2.0 machine set was already materially cleaned by R2.7 WP-03 and later accepted Round-2 work. The remaining S6D-primary gaps are realization gaps, not admission gaps, and are routed exactly to S6D-03–09.

This is not a claim that all 571 IDs are fully implemented. Admission and realization are separate axes.

## 2. Source Manifest

### CANONICAL / AMENDMENT / DECISION

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- S6D sequencing decision, owner decision and parent brief
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`
- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`
- Actor/Asset/Activity/Rule Element and Step-2 owner contracts
- Step-3 execution canonical specification
- Step-5.2 resumable runtime, Step-5.7 checkpoint recovery and Step-5.13 cleanup/retention canonical owners
- R2.1 continuity, R2.2 Actor continuity, R2.3 Context Runtime, R2.4 single-context execution and R2.5 collaboration canonical owners
- Step-5 chronology, Story, retention, durability and publication owners
- Campaign House Rules canonical owner

### IMPLEMENTATION / TEST

- all four `DEV/CATALOG/*.json` files
- all current `DEV/SCHEMAS/*.json`
- current `GAME/SCHEMA/*`
- Step-1/2/3 and R2.7 WP-03–06 focused tests
- runtime `GAME/CORE/*` consumers
- `GAME/RULES/*`
- release/runtime provenance and builder tests

### HISTORICAL / RESEARCH

- `CATALOG_MODEL.md` and `CATALOG_DESIGN_STATUS.md` only as derivation/history where current owners supersede concrete IDs
- Step-1 catalog meta-model assurance chain
- Steps-1/2 retrospective assurance final
- R2.7 WP-06 rules/adjudication mini-report

Historical mentions were not counted as current admission evidence.

## 3. Evidence method

The audit used:

1. current remote tree and ref;
2. `PROJECT_MAP.md` ownership/dependency routing;
3. exact machine registry extraction;
4. family and per-ID mapping to current owners;
5. schema/catalog/test/runtime consumer comparison;
6. retired-ID search across active surfaces;
7. recovery/retention check for accepted work;
8. package/content/namespace check against S6D-01;
9. explicit downstream routing for incomplete realization.

Admission evidence followed the brief hierarchy. A baseline label, generic D&D familiarity, historical appearance or hypothetical future usefulness was never sufficient by itself.

## 4. Registry admission findings

### 4.1 S6D-primary

The primary families are:

- 37 reusable definition kinds;
- 15 world-record kinds;
- 17 runtime-record kinds;
- 22 Step-1/2/3 mechanical protocol values (13 later Round-2 values in the same registry are inherited instead);
- 31 Activity primitives;
- 26 Rule Element operations;
- 34 Calculation Selectors;
- 10 MechanicalContext accessors.

All independently admitted IDs are `ACTIVE_ADMITTED`; all `value.*` protocol kinds are `EMBEDDED_NONOWNER` because they have no independent lifecycle.

Definition/world/runtime class IDs are already owned by the accepted Catalog 2.0 class model and machine structure/identifier inventories. Their physical persistence/schema work outside S6D remains with named R2.7 owners; this does not invalidate class admission.

Mechanical protocol values are active typed interface obligations. Missing exact shape is S6D-05, not permission for an independent runtime record or arbitrary JSON.

Selectors and Rule Element operations are active because the accepted Step-2 model and WP-06 evidence explicitly preserve the full registered calculation surface for later metadata closure. Their realization owner is S6D-03.

Accessors are active with realization owner S6D-04.

Activity primitives are active closed execution vocabulary with realization owner S6D-06. Admission does not authorize an operation until its exact S6D-06 contract is satisfied.

Definition content families route to:

- S6D-07 for Actor construction/progression;
- S6D-08 for Resource/Effect/Condition/Rest semantics;
- S6D-09 for remaining supported mechanics/domain seed coverage.

### 4.2 Engine-enum consistency

The 276 IDs in facets, Activity families, transitions/events, resource/effect/life/condition/temporal/targeting/signal/duration and Step-3 execution enums remain under their existing engine/domain owners.

S6D-02 found no same-ID alias, duplicate registry authority or active reference requiring a new enum. These IDs are not independently reopened. Detailed contracts remain with their existing owners and later S6D domain where explicitly named.

### 4.3 Inherited Round-2 vocabulary

The 103 inherited IDs include:

- truth/lore/epistemic/disclosure;
- durability/publication/repository-ref outcomes;
- Actor continuity/cognition/relationship facets;
- logical roles and Context Runtime vocabulary;
- Story/Chronicler/planning vocabulary;
- collaboration/input vocabulary;
- chronology/recovery/message-retention vocabulary;
- 13 Round-2 typed values stored in `protocol_value_kinds`.

Each non-value ID is `ACTIVE_ADMITTED + INHERITED_ACTIVE`; inherited `value.*` IDs are `EMBEDDED_NONOWNER + INHERITED_ACTIVE`, always with an exact accepted R2.x/Step-5 owner. S6D-02 checks consistency only. No WP-07+ realization was pulled forward.

## 5. Cross-surface mismatch ledger

### M-01 — retired `world.relationship` remained in active structure prose

Machine catalogs, identifier policies, inventory and tests correctly retire the class, but `ENTITY_STRUCTURES.md` still contained a table row describing it.

Disposition: remove the stale table row. Explicit retirement/history and negative tests remain valid mentions.

### M-02 — Combat state wording obscured Procedure ownership

`COMBAT.md` listed initiative/order and other combat state without distinguishing world-facing encounter identity from Procedure-local timing/action-budget execution state.

Disposition: clarify that `runtime.procedure` owns Procedure-local initiative/order/turn/action-budget state; `world.encounter` is an optional world-facing referent only; Actor/Effect/etc. retain their natural state.

### M-03 — Rewards used retired ITEM vocabulary

`REWARDS.md` called significant items “ITEM records” and mixed objective item properties with per-PC identification.

Disposition: route significant item identity/current state to `world.asset`, reusable properties to `definition.asset`, and subject knowledge to the existing lore/knowledge boundary.

### M-04 — PC schema note used ITEM IDs

The `pc.schema.yaml` note repeated the retired vocabulary even though its field is a reference list pending later physical realization.

Disposition: say `world.asset` IDs; do not redesign the PC schema in S6D-02.

### M-05 — selector registry versus metadata surface

The catalog registers 34 selectors while `mechanical-surfaces.json` currently describes only five.

Disposition: all 34 remain admitted; realization is explicitly S6D-03. S6D-02 does not manufacture selector metadata.

### M-06 — protocol-value realization is uneven

Several registered values have strict schemas while others are vocabulary-only.

Disposition: all protocol values are `EMBEDDED_NONOWNER`; primary values retain S6D-05 realization and inherited Round-2 values retain their accepted owners. No value becomes an independent record merely to obtain a schema.

### M-07 — primitive registry lacks exact contracts

All 31 `op.*` IDs remain a closed admitted vocabulary, but exact args/results/reads/writes/RNG/failure/suspension contracts are not complete.

Disposition: realization is S6D-06; until then registration is not execution permission.

### M-08 — S6D-01 package identity has no admitted logical package profile

S6D-01 defines exact snapshots/locks but intentionally leaves actual package admission to S6D-02.

Disposition: admit one minimum built-in pre-release package profile:

```text
package_id: hdm.rules.dnd2024-srd52-core
compatibility_id: hdm.rules.dnd2024-srd52.v1
catalog_generation: 2.0.0
semantic_content_root: GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/
namespace_claims: one top-level semantic prefix per admitted definition family
selectable_now: false
```

No fake empty rules definition seed is created. Activation requires S6D-07–09 content plus S6D-11 manifest/lock/builder/loader verification.

### M-09 — finite package failure distinctions

S6D-01 lists finite mismatch causes. Adding many top-level failure IDs now would duplicate the existing typed execution failure owner.

Disposition: retain `failure.catalog_context_incompatible` as the execution failure code with a typed reason to be materialized by S6D-11; retain `runtime.catalog_gap_report` for unsupported capability after bounded discovery.

## 6. Retired-reference audit

Confirmed retired machine IDs:

- `world.relationship`;
- `world.timeline_marker`;
- `runtime.dirty_record`;
- `runtime.publication_batch`;
- `runtime.execution_segment`;
- `runtime.resolution_chain`.

After M-01 cleanup, remaining mentions are explicit retirement history or negative tests. `value.execution_segment` is distinct from retired `runtime.execution_segment`.

No obsolete migration layer is required because Catalog 2.0 is unreleased.

## 7. Package/content/namespace ledger

Only one built-in rules package is currently required. Multiple artificial packages would create complexity without a current consumer.

Namespace claims follow the existing semantic definition-ID convention: `ability.*`, `skill.*`, `resource.*`, `spell.*`, and the corresponding prefix for each of the 37 admitted definition families.

Engine capabilities and protocol IDs do not belong to the ruleset namespace. Campaign/session definitions remain owner-local frontiers and cannot shadow package IDs.

Exact content bytes are not fabricated before seed work. The admission profile fixes the logical package identity, compatibility line, content root, namespace boundary and activation gate. S6D-11 later owns the physical manifest/lock/digest verification.

## 8. Alternatives

### A — per-ID ledger plus registry-family profiles and coordinated cleanup

Selected. It proves exact set equality while avoiding 571 copies of identical family semantics.

### B — family admission with undocumented exceptions

Rejected. Smaller document, but cannot prove every ID is classified or route mixed `protocol_value_kinds` correctly.

### C — preserve the registry and defer all gaps

Rejected. It would retain no explicit admission/realization distinction and leave stale active prose unresolved.

### D — direct-flow-only minimal catalog

Rejected as a default architecture. It would discard valid recovery, collaboration, package and operational owners. YAGNI remains an item-level challenge, not permission to replace the accepted class model.

## 9. Recommendation

Adopt:

- `CATALOG_ADMISSION.md` as the semantic owner of admission status/strata/evidence laws;
- `catalog-admission-ledger.json` as exact item-level accounting;
- its strict schema and focused tests;
- one required but currently nonselectable built-in package profile;
- the four bounded stale-owner wording repairs;
- no removal from the current 571-ID machine registry;
- exact downstream realization routing without claiming downstream completion.

## 10. Human decision assessment

Human decision required: **NO**.

The recommendation follows accepted catalog/class/identity/execution/Round-2 owners and the already approved S6D scope. It does not change product scope, introduce a second state authority, supersede accepted architecture or accept a new critical risk.

## Step-6 evidence correction

The final ledger does not rely on family defaults as item-level proof. Every one of the 571 entries carries its effective disposition, stratum, realization, exact semantic owner, evidence class, evidence citation, and consumer/reachable accepted dependency. Final post-critic disposition totals are 457 `ACTIVE_ADMITTED`, 35 `EMBEDDED_NONOWNER`, 79 `DORMANT_NONSELECTABLE` and 0 stale; stratum totals remain 192 / 276 / 103.

Executable registration correction: only 5 selectors, 7 rule operations, and 10 accessors have current structured support in `mechanical-surfaces.json`; 29 selectors, 19 operations, and all 31 primitives are dormant with exact activation triggers.
