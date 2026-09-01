# R2.7 WP-11 Step 2 — DEV Machine and Verification Evidence

Status: **EVIDENCE SLICE COMPLETE — STEP-2 EXTRACTION COMPLETE**

## Source scope

This slice inspected every DEV catalog, JSON schema, scenario catalog, test,
audit entry point and CI workflow named in WP-11 Source Manifest sections 5.4
and 5.5. These are machine-contract and verification sources. They constrain
identity and lifecycle allocation but do not independently select GAME topology.

## WP-10 machine-accounting ledger

| Logical member | Identity or lifecycle evidence | Physical-family qualification |
|---|---|---|
| Actor-local continuity | `world.actor` has campaign-sequential `actor-*` identity and source-owned directed relationships. | Native owner record; relation remains under the source Actor and needs no symmetric/index authority. |
| Knowledge | Composite campaign key `(knower_id, fact_id)` plus stance. | No dedicated state-schema dispatch; no family follows merely from the catalog entry. |
| Effect/application | Campaign-sequential `effect-*`, target and lifecycle. | Natural owner family; condition aggregation remains derived. |
| Interaction | Campaign-sequential `turn-*`, binding campaign/session/player/input to the IntentPlan. | Separate runtime lifecycle, not Session or LOG. |
| IntentPlan and clauses | Plan derives from Interaction; clauses are ordered embedded values. | Plan requires a disposition; clauses do not form a separate family. |
| Command | Interaction-derived command identity and idempotency fingerprint. | Separate accepted-command lifecycle, not narration/history. |
| Procedure | Campaign-sequential `procedure-*` and procedure-local resources. | Separate native lifecycle, not generic Session state. |
| Resolution | Campaign-sequential `resolution-*` and pinned accepted inputs, RNG and children. | Separate invocation lifecycle, not current world state. |
| Continuation, choice and reaction | Continuation derives from Resolution and freezes causal inputs/RNG/dependencies; choice/reaction are embedded. | Continuation requires a distinct operational disposition; values do not. |
| MechanicalEvent and receipt | Campaign-sequential `event-*`; receipts are protocol values. | Immutable evidence family versus embedded receipt; neither becomes mutable world authority. |
| ResolutionTrace | Resolution-derived, bounded diagnostic entries. | Distinct bounded diagnostic evidence; hidden reasoning remains excluded. |
| SemanticEvent/relation | Campaign-sequential `semantic-*`. | Native semantic-history evidence, not a total clock/current-state surrogate. |
| Disclosure | Composite `(player_id, fact_id)` identity. | No current DEV state-schema route; recipient scope remains distinct from truth/knowledge/message. |
| Retained Message | Campaign-sequential `message-*`. | Requires an explicit native-family or no-native-family conclusion; no message-state schema is present here. |
| Story projection | Catalog contains draft/service values, not a `runtime.story` record kind. | No runtime-local family follows; Story owner remains separately noncanonical. |
| Native temporal component | `temporal-binding` is embedded by Actor, Asset or Effect and has no independent ID. | Remains with natural owner; Agenda is derivative. |
| Campaign ID allocator | Singleton `campaign-allocator`. | Operational singleton; no chronology or index authority. |
| Optional collaboration | Campaign-sequential `collaboration-*`. | Trigger-conditional; no unconditional root. |
| Multiplayer planning projection | Planning values exist without a matching runtime record kind/schema. | Conditional/dormant projection; no current physical family. |
| WP-09 context controls | Protocol values only; the WP-09 owner explicitly selects no campaign record. | Explicit no-campaign-record disposition. |

## Cross-cutting machine facts

- `identifier-policies.json` distinguishes sequential, derived, composite,
  singleton and non-record forms. A timeline slot is ordering evidence rather
  than identity; protocol values have no independent ID.
- `world-record.schema.json` dispatches only Actor, Asset, Location and Effect
  among the relevant world kinds. Missing dispatch is not permission to invent
  a physical owner.
- Execution schemas pin accepted causal inputs and fixed RNG. They preserve the
  existing deterministic lifecycle but specify neither a directory layout nor
  shard arithmetic.
- `mechanical-surfaces.json` keeps caches rebuildable/non-authoritative and
  rejects dormant consumers before input validation. It supplies no physical
  index authority.
- The audit and CI route verifies maintenance consistency and DEV tests; it does
  not currently prove the missing topology rules.

## Verification and consumer constraints

`BOOTSTRAP_STORAGE_REGRESSION_CASES.md` requires root-MANIFEST layout, a
generated scaffold boundary and bounded campaign discovery. `PERSISTENCE_TRANSACTION_CASES.md`
requires coherent `LOG`/Scene/Current/entity/index publication and independent
live CAS. `CHRONOLOGY_CASES.md` rejects Git order as fictional chronology and
requires bounded chronology inspection. `test_destination_template_boundary.py`
protects the release/template path boundary. These are forward verification
routes for topology realization, not evidence that an unimplemented route exists.

## Step-2 completeness check

- All WP-10 rows and all current GAME record/index/template families in the
  Task Brief have a source-accounted allocation or no-native-family finding.
- Canonical owners, current runtime consumers and DEV machine/verification
  consumers were reconciled; added Step-5 and catalog-resolution sources are
  recorded in the canonical-owner slice.
- Qualifiers retained for currentness, live state, chronology, eligibility,
  compaction, conditional collaboration and no-record concerns.
- No source produced a human-owned decision. Physical topology synthesis may
  proceed, bounded to WP-11 and without selecting downstream realization.
