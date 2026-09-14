# HDM Implementation Planning — Authority / Dependency Graph Audit

Status: **ACTIVE AUTHOR ADVERSARIAL PLANNING AUDIT — NON-CANONICAL EVIDENCE LEDGER**
Date: 2026-09-14
Initial audit baseline: `94e416c58633912a97308c1bfa95762951f0f8a4`
Current graph synchronization basis: `5b0dcd4dd285d26c610d633416270901b9b3d5cb`
Synchronized through: **F36**
Production implementation authorized: **NO**.

This artifact is an audit/traceability ledger. It does not replace canonical owners, RD plans, proof ledgers, package precedence or readiness authorities. Its purpose is to keep the current typed dependency/authority graph explicit while the author adversarial audit searches for hidden implementation-planning defects that document-by-document review can miss.

The graph is a live audit instrument. Every confirmed finding/repair that changes dependency, authority, currentness, shared-writer or proof topology must be reflected here before the next graph pass continues.

## 1. Graph model

The audit treats the planning package as a typed directed multigraph.

### Node classes

- `SEMANTIC_OWNER` — world/runtime/value owner and lifecycle.
- `POLICY_OWNER` — authorization/currentness/chronology/publication/recovery law.
- `MACHINE_KIND` — catalog/admission kind.
- `STRUCTURE` — exact machine/schema shape.
- `IDENTITY_POLICY` — allocation/derived/composite/singleton/source-native identity.
- `PHYSICAL_ROUTE` — fixed/root/route/index/storage location.
- `DERIVATIVE_ROUTE` — completeness/index/routing evidence that is not semantic authority.
- `RUNTIME_API` — deterministic producer/validator/consumer method.
- `DURABILITY_EDGE` — local atomic segment, campaign publication, LIVE exact-source CAS, Story publication, etc.
- `RECOVERY_CONSUMER` — cold hydration/currentness/rebuild path.
- `SHIPPED_CONSUMER` — CORE/setup/session/bootstrap prose or schema that directs actual behavior.
- `READINESS_DUTY` — R001..R084 item or owner-enumerated machine duty.
- `PROOF_WITNESS` — focused/integration/static/hosted/empirical proof.
- `RD_OWNER` — RD-01..RD-16 executable plan.
- `EXECUTION_EDGE` — prerequisite, constraint, bounded integration join, currentness barrier or shared-writer checkpoint.

### Edge classes

```text
OWNS
ADMITS
STRUCTURES
IDENTIFIES
ROUTES
DERIVES_FROM
MUTATES_WITH
PUBLISHED_BY
SELECTS_AUTHORITY
CONSUMES
RECOVERS_FROM
PROVES
IMPLEMENTS
HARD_PRECEDES
JOINS_BEFORE_INTEGRATION
SHARED_FILE_CHECKPOINT
PROOF_AFTER_TARGET
CONSTRAINS_WITHOUT_ORDERING
MUST_NOT_OWN
SUPERSEDES
```

## 2. Required closure patterns

A worker-ready family/owner path must satisfy the applicable closure, not merely contain similarly named files.

### Native durable owner

```text
SEMANTIC_OWNER
 -> MACHINE_KIND/admission
 -> STRUCTURE
 -> IDENTITY_POLICY
 -> PHYSICAL_ROUTE
 -> RD producer/mutator
 -> DURABILITY_EDGE
 -> RECOVERY_CONSUMER
 -> READINESS_DUTY
 -> item-bound PROOF_WITNESS
```

### Correctness-critical derivative routing

```text
SEMANTIC_OWNER lifecycle
 -> derivative route computation
 -> same acknowledged durability closure as owner transition
 -> bounded recovery/invalidation consumer
 -> basis/currentness validation
 -> proof of completeness + non-authority
```

### Shipped consumer cutover

```text
canonical owner law
 -> runtime/schema realization
 -> shipped CORE/setup/session consumer
 -> stale formulation negative search/test
```

### Cross-domain operation

```text
native source A exact edge
 + native source B exact edge
 -> forward owning transition
```

There is no implied distributed transaction, rollback, scalar currentness, fictional chronology or newest-wins edge unless a canonical owner explicitly grants it.

## 3. Defect patterns searched

The audit marks a planning defect when it finds any of:

1. semantic owner with no admitted machine kind or explicit no-record disposition;
2. physical family/route with no semantic owner;
3. catalog kind with no exact structure or identifier policy;
4. independently addressable owner with a shorter-lived ID than its accepted durability;
5. lifecycle transition with no coherent derivative routing/index mutation;
6. derivative completeness consumer with no bounded producer;
7. proof witness whose executable mechanism is absent or underdefined;
8. shipped consumer that preserves contradicted authority/currentness guidance;
9. multiple independent writers for one physical shared file without an ordered join;
10. publishable checkpoint that commits intentional RED future tests;
11. currentness route that nominates authority but has no exact selected-source fence;
12. recovery path that can only succeed by forbidden broad scan/fallback;
13. aggregate readiness coverage that can hide a missing concrete family/item;
14. stale legacy v0.8 preservation assumption constraining the clean-slate v1.0 `GAME/**` design;
15. architecture owner contradiction where a lower-scope physical owner invents/duplicates semantic ownership;
16. two individually valid completeness companions that can jointly describe contradictory current placement;
17. mutation trigger whose owner transition and derivative companions are not frozen/revalidated against one basis;
18. schema/generation cutover where a later strict integrator can erase an earlier semantic delta;
19. checkpoint-level dependency that is absent from the declared DAG and therefore permits an invalid legal execution order;
20. dormant/trigger/no-work accounting that can accidentally activate work or hide a required trigger realization.

## 4. Findings currently established

All dispositions below are author-side planning dispositions only and remain independently unconfirmed until the mandatory Senior re-review.

| Finding | Graph break | Current disposition |
|---|---|---|
| F1 | Scene LIVE route shipped/schema consumer stale relative to owner-typed currentness | repaired by mandatory scene-routing overlay |
| F2 | Publishable RD checkpoints contained future-task intentional RED tests | repaired by checkpoint-coherence overlay |
| F3 | RD-01 contained another instance of the same checkpoint break | incorporated into checkpoint-coherence repair |
| F4 | `world.thread` semantic owner lacked complete catalog admission/structure/identity projection | repaired by WP-15 thread-catalog overlay |
| F5 | WP-17 shipped collaboration guidance had proof/search but no executable consumer cutover | repaired by WP-17 shipped-consumer overlay |
| F6 | temporal lifecycle had Agenda/recovery consumers but no durable completeness-routing producer | repaired by temporal completeness-routing overlay |
| F7 | WP-16 duties 12/13/15 claimed proof without complete executable lifecycle/identity/multi-source mechanism | repaired by WP-16 executable-closure + proof-ledger amendments |
| F8 | family graph contained false `world.faction` physical family and missing `world.player` machine admission | repaired by family-reconciliation overlay; final integration delegated to RD-16 |
| F9 | principal authorization consumed PLAYER binding without a bounded completeness-protected producer | repaired by `PRINCIPAL_PLAYER_ROUTING.yaml` producer/consumer/publication/recovery chain |
| F10 | `runtime.mechanical_event` semantic composite identity conflicted with stale sequential allocator policy | repaired as composite key `[segment_id,event_ordinal]`; no campaign allocator participation |
| F11 | RD-10 -> RD-05 catalog-backed execution seam had no worker-ready deterministic binding owner; durable catalog-gap family had no complete producer path | repaired by new bounded RD-15 |
| F12 | accepted 17-world-family set lacked strict per-family world-state machine realization | repaired by RD-16 strict schema/dispatch integration plan |
| F13 | multiple RDs independently planned writes to shared catalog/identity machine files | repaired by RD-16 single final shared-machine integration checkpoint |
| F14 | shipped CORE/adjudication prose still allowed a model-memory/quick-ruling bypass around deterministic catalog binding | repaired by catalog-binding shipped-consumer cutover |
| F15 | package router still exposed only the older 14-RD/8-overlay state and could legally omit later mandatory repairs | repaired by post-graph package/execution integration and current package router |
| F16 | native `world.player` had ambiguous duplicate campaign identity representation | repaired: enclosing world-record `id` is the single campaign key; no second persisted `player_id` |
| F17 | RD-15/RD-16 checkpoint tests could violate checkpoint-coherence by appearing before their own RED->GREEN task | repaired by preserving overlay-5 checkpoint law |
| F18 | RD-05 catalog-backed command acceptance could bypass RD-15 same-context validated binding | repaired by RD-15 -> RD-05 hard edge for catalog-backed acceptance |
| F19 | earlier coverage artifact did not represent the 16-RD / 17+17-family package | repaired by coverage v3 post-graph route |
| F20 | proof ledger did not make RD-15/RD-16 mandatory for R018/post-WP27 closure | repaired by proof-ledger v3/post-graph amendments |
| F21 | current execution topology still depended on older 14-RD wave graph | repaired by execution-waves v2 post-graph |
| F22 | post-graph proof could close from thematic tests without exact named witnesses | repaired by mandatory exact witness matrix |
| F23 | accepted catalog-backed execution could retain only fingerprint/current context and lose reconstructive exact basis | repaired by one `CatalogContextBasis` carried RD-15 -> RD-05 -> RD-06 -> RD-07 |
| F24 | SOURCE_NATIVE_LIVE identity encoding/allocation was underdefined | repaired by CAS-owned `uint64` source-local ordinal + `framed_base32hex_v1`; no campaign allocator/rekey |
| F25 | canonical LIVE campaign identity could be confused with physical route token | repaired: semantic `campaign_id`; derived `c1-<sha256>` physical token with body validation |
| F26 | multiple SOURCE_NATIVE_LIVE creations in one mutation lacked exact deterministic slot normalization | repaired by family/index/slot normalization and ambiguity fail-closed |
| F27 | LIVE epoch/route/opening identity/currentness fence underdefined | repaired with exact `c1`/`s1`/`e1`, opening-basis equality and prepared-source non-authority |
| F28 | deterministic LIVE candidate preparation lacked idempotent occupant/lost-ack reconciliation | repaired by deterministic preparation/currentness rules |
| F29 | initial LIVE state did not exactly seed pre-existing claimed owners from one pinned campaign revision | repaired by exact `H` seed; `EPOCH_LOCAL_CREATION` seeds nothing |
| F30 | selected LIVE route/claim completeness lacked a campaign-side protected companion | repaired by `LIVE_ROUTING.yaml`; missing/stale/inconsistent companion cannot prove CAMPAIGN routing |
| F31 | final v1 LIVE source packing/absorption was not fully lossless/idempotent with stable IDs and required companions | repaired by typed native-state packing and forward absorption contract |
| F32 | possible need for a new publication REST/GraphQL primitive | negative finding: existing exact-ref read + single-parent successor + non-force stale-head rejection boundary is sufficient; planning must not invent a new transport primitive |
| F33 | `CURRENT_PROGRESS.md` lost markers required by maintenance-audit control validation | repaired; exact repair checkpoint had hosted maintenance audit + full DEV discovery GREEN |
| F34 | R018 runtime-family proof could close from count/catalog/world-only evidence without exact runtime schema/root realization | repaired: exact 17-row runtime family matrix + `R018RuntimeFamilyProofTests` mandatory |
| F35 | RD-12 `PLAYER.collaboration_route_refs` could be erased/diverged by later RD-16 strict `world.player` integration | repaired by `RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY -> RD16_PLAYER_STRICT_STATE_INTEGRATION_JOIN`; RD-16 final physical PLAYER schema generation |
| F36 | campaign/LIVE authority movement could update LIVE routing and temporal completeness routing independently, yielding duplicate/missing current temporal enrollment | repaired by one campaign publication handoff for `LIVE_ROUTING` + campaign `TEMPORAL_ROUTING` movement against exact prepared/closed LIVE state |

Current author-open findings after F36: **none yet recorded**, but the adversarial graph audit is explicitly still active and has not issued zero-open closure.

## 5. Family-level R018 graph — current evidence

Current final planned v1 world-family census is 17:

```text
world.actor
world.actor_group
world.asset
world.location
world.connection
world.zone
world.organization
world.contract
world.mission
world.scene
world.encounter
world.hazard
world.effect
world.lore_fact
world.knowledge
world.thread
world.player
```

`world.faction` is not an independent v1 family; faction remains classification/facet state under `world.organization`.

Current final planned runtime-family census is also 17:

```text
runtime.session
runtime.message
runtime.interaction
runtime.procedure
runtime.intent_plan
runtime.command
runtime.resolution
runtime.continuation
runtime.mechanical_event
runtime.semantic_event
runtime.resolution_trace
runtime.disclosure
runtime.collaboration_obligation
runtime.checkpoint
runtime.id_allocator
runtime.maintenance_audit
runtime.catalog_gap_report
```

Counts are routing aids, not proof. Current R018 closure requires, per concrete family, the full owner -> admission -> exact structure/schema -> identity policy -> route/root -> RD producer/integrator -> durability/recovery -> item-bound witness chain. F34 additionally requires the exact 17-row runtime schema/root matrix and `R018RuntimeFamilyProofTests`.

RD-16 is the final physical shared-machine writer for the coordinated world-family/catalog/identifier-policy integration; semantic ownership remains with the producing RDs/owners.

## 6. Current identity / source graph

Identity classification must distinguish:

- independently allocated campaign identities;
- parent-derived identities;
- semantic composite identities;
- singletons/campaign-only owners;
- `SOURCE_NATIVE_LIVE` identities;
- `OWNER_EQUIVALENT` LIVE birth;
- `FORBIDDEN` LIVE birth.

Current high-risk exact identities include:

```text
world.player
  campaign-owned stable world-record id
  LIVE birth FORBIDDEN

runtime.mechanical_event
  composite_key [segment_id,event_ordinal]
  campaign allocator forbidden
  LIVE owner-equivalent; no second surrogate

SOURCE_NATIVE_LIVE applicable families
  semantic source key = LiveSourceKey(campaign_id, scene_id, epoch_id)
  physical campaign route token = c1-<domain-separated framed sha256(campaign_id)>
  source-local creation ordinal = CAS-owned uint64
  encoding = framed_base32hex_v1
  accepted ID survives close/absorption unchanged
```

Unknown/unspecified future family disposition fails closed rather than silently selecting an allocator/identity mode.

## 7. High-risk derivative/currentness subgraph

These companions are correctness-critical routing evidence but remain non-authoritative. Their lifecycle edges must stay explicit because several recent defects arose only at companion intersections.

### Principal -> PLAYER completeness

```text
world.player stable external binding mutation
  + PRINCIPAL_PLAYER_ROUTING delta
    MUTATES_WITH
one RD-06 campaign resulting-tree closure

ordinary authorization
  current complete principal route
  -> direct exact PLAYER reload
  -> binding/status/control/operation revalidation
```

`PLAYER_INDEX`, session/card/cache data and routing metadata never authorize.

### Collaboration -> PLAYER completeness

```text
runtime.collaboration_obligation generation/terminal transition
  + all affected world.player collaboration_route_refs deltas
    MUTATES_WITH
one RD-06 campaign resulting-tree closure

RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY
  HARD_PRECEDES / JOINS_BEFORE_INTEGRATION
RD16_PLAYER_STRICT_STATE_INTEGRATION_JOIN
```

The refs nominate completeness/routing only; they do not satisfy an obligation or grant PLAYER authority.

### Campaign <-> LIVE selection/currentness

```text
prepared LIVE candidate
  contains prospective exact native state + LIVE temporal routing
  but SELECTS_AUTHORITY = false

campaign -> LIVE selection publication
  + LIVE_ROUTING selected route
  - moved campaign TEMPORAL_ROUTING entries
  + other required campaign companions
    MUTATES_WITH
one RD-06 campaign resulting-tree closure
  validated against exact prepared LIVE basis

selected LIVE mutation
  native owner + LIVE temporal-routing delta
    MUTATES_WITH
one exact-source LIVE CAS

LIVE -> campaign absorption publication
  materialized native owners
  + restored campaign TEMPORAL_ROUTING
  - LIVE_ROUTING selected route
  + other required campaign companions
    MUTATES_WITH
one RD-06 campaign resulting-tree closure
  derived from exact CLOSED terminal source
```

Duplicate or missing current temporal enrollment across campaign and selected LIVE domains is an integrity conflict. Recovery uses the disjoint union of validated current source-domain enrollments only.

### Authorization/control mutation intersection still under audit

The following transitions may touch more than one of the above subgraphs and therefore remain a concentrated contradiction-pair target:

```text
PLAYER creation/admission
external principal rebind
PLAYER activation/reactivation/deactivation
controlled-PC transfer
collaboration generation/terminalization
LIVE claim expansion/revocation
campaign -> LIVE selection
LIVE -> campaign absorption
```

A legal execution order must not permit any acknowledged resulting state in which semantic owner state and one or more required companions describe different current authority/binding/enrollment facts.

## 8. Current checkpoint / shared-writer graph

Current key joins include:

```text
RD10 typed InterpreterResult
  -> RD15 deterministic same-context binding
  -> RD05 catalog-backed RuntimeCommand acceptance

RD15 catalog basis
+ RD05 accepted catalog execution
  -> RD06 catalog-basis durability
  -> RD07 exact catalog-basis recovery

RD14_CAMPAIGN_IDENTITY_CREATION_READY
+ RD06_CAMPAIGN_IDENTITY_IMMUTABILITY_READY
+ RD09 LIVE route/order/cursor checkpoints
  -> RD09_SOURCE_NATIVE_ID_READY

RD09_SOURCE_NATIVE_ID_READY
  -> RD16 shared identifier-policy integration
  -> RD07 selected-LIVE recovery join

RD08 thread LOCAL_SEMANTIC_READY
+ RD04 player/faction disposition LOCAL_SEMANTIC_READY
+ RD05 MechanicalEvent identity LOCAL_SEMANTIC_READY
+ RD09/WP16 live_birth table LOCAL_SEMANTIC_READY
+ RD12 PLAYER collaboration-route companion LOCAL_SEMANTIC_READY
+ RD15 catalog-gap policy input LOCAL_SEMANTIC_READY
+ RD16 strict world-family schemas ready
  -> RD16 SHARED_MACHINE_INTEGRATION_JOIN

RD16 shared machine integration
  -> R018 final closure
  -> RD14 late final topology/scaffold validation
```

F36 adds bounded campaign/LIVE temporal-companion handoff joins around RD-06 publication; it does not add a distributed transaction or whole-RD serialization.

The declared checkpoint-level graph must remain acyclic after every new repair. Whole-RD apparent cycles must be decomposed only when there are genuinely distinct owner-local checkpoints; checkpoint splitting may not be used to hide a real semantic cycle.

## 9. Proof graph status

Current proof route is:

```text
historical v2 ledger/appendices
+ lossless proof ledger v3 post-graph
+ F27-F31 control amendment
+ exact post-graph witness matrix
+ F34 runtime-family R018 amendment
+ F35 PLAYER strict-state integration amendment
+ F36 LIVE/temporal handoff amendment
```

Proof closure is item-bound. A row/test-class/count is insufficient when the named executable producer, consumer, durability/currentness/recovery join or required negative is absent.

Historical readiness accounting remains:

```text
133 active = 116 direct + 9 pure proof + 8 composite parents
12 trigger-gated
79 no-work
R004 absent
```

Post-WP27 author findings repair implementation planning; they do not invent historical readiness IDs.

## 10. Active audit queue after F36

The graph audit remains open. Next passes, in current priority order:

1. **Mutation-trigger contradiction pairs** across principal -> PLAYER routing, PLAYER collaboration refs, activation/control changes, LIVE claims/selection and temporal handoff. Freeze each mutation's semantic owners + all affected companions and test whether every legal partial/order outcome fails closed.
2. **All remaining shared physical writers.** Build a file -> planned-writers -> semantic-deltas -> final-writer table and find any later writer that can erase an earlier accepted delta or publish two independently-final generations.
3. **Schema/version-generation cutovers.** Check schema-version bumps, catalog generation, strict wrapper dispatch and shipped schema projections for mixed-generation states that the declared checkpoints still permit.
4. **Checkpoint DAG cycle proof.** Rebuild hard/join edges at checkpoint granularity including F34-F36 and prove acyclicity without relying on informal whole-RD ordering.
5. **Dormant / trigger / no-work activation safety.** Verify trigger-gated and no-work rows cannot silently become current implementation obligations or remain dormant after their exact trigger has become true.
6. **Stale shipped-consumer reverse scan.** Starting from every repaired owner law, search current shipped CORE/setup/session/bootstrap/schema consumers for any shorter contradictory authority/currentness path.
7. **Recovery negative-path scan.** For every completeness companion, prove missing/stale/ambiguous state cannot degrade into broad scan, newest-wins, cache authority or false absence.
8. **Proof asymmetry scan.** Mechanism-without-proof and proof-without-mechanism at concrete family/item/companion level, including all later F34-F36 repairs.
9. **Final reverse-coverage/currentness sweep.** Only after the above passes produce no open item.

Any confirmed planning/control defect is published immediately and this graph is synchronized before the next pass continues.

## 11. Completion condition

This audit may close only when:

```text
OPEN AUTHOR BLOCKING    = 0
OPEN AUTHOR SIGNIFICANT = 0
OPEN AUTHOR MINOR       = 0

and

all active readiness/owner duties have:
  exact current owner
  executable RD route
  physical/shared-writer disposition
  required durability/currentness/recovery joins
  item-bound proof
  reverse coverage

and

all correctness-critical derivative companions have:
  complete producer
  same-edge mutation rule with their owner transition
  bounded currentness/recovery consumer
  corruption/ambiguity fail-closed rule
  exact positive + negative witness

and

checkpoint-level hard/join graph is acyclic at the exact final package state.
```

Only then may the package move to mandatory independent Senior plan re-review / GO. Production implementation remains forbidden until that independent gate passes.
