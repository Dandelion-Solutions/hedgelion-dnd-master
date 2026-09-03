# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-2 Source Manifest Expansion

Status: **STEP 2 — OPEN-WORLD SOURCE MANIFEST EXPANDED / INSPECTED**

Date: 2026-09-03

Step-2 verified start:

- `cc4edd01a2c7b68a0a749041bb2f8aa1987d1be3`.

Companion Step-1 manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-source-manifest.md`.

Companion Step-2 evidence extraction:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-2-evidence-extraction.md`.

This artifact extends, rather than closes, the Step-1 Source Manifest. Discovery remains open-world through Steps 3–8. Any actual owner, consumer, schema, test, currentness path, recovery route, counterexample or superseding decision reached during later synthesis/review must be added before a coverage claim relies on it.

---

## 1. Step-2 expansion result

Step 2 traversed the repaired Step-1 graph through current `DEV/PROJECT_MAP.md`, direct canonical owners, machine schemas/catalogs, shipped CORE consumers and executable/regression consumers.

The expansion materially added direct evidence for:

- current accepted external-input identity (`runtime.interaction`);
- exact semantic-unit addressability (`runtime.intent_plan` / `IntentClause`);
- current machine incompleteness of collaboration-relevant normalized IntentClause semantics;
- existing mechanical `value.contribution` ownership;
- conditional collaboration record identity/root;
- campaign-native publication/recovery composition;
- current shipped session/multiplayer/chronology/information assumptions.

No discovered source requires a new generic input record, collaboration queue, scheduler or global collaboration frontier.

---

## 2. Existing input identity / semantic-unit route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | `CANONICAL_OWNER` | `Interaction -> IntentPlan -> IntentClause -> RuntimeCommand/...`; stable Interaction retry identity; same prose in later intentional turn is new Interaction; every material interpreted clause has a stable clause identity/disposition; native Procedure/Continuation/Choice/Reaction wins where it owns waiting/resume. |
| `DEV/SCHEMAS/runtime-interaction-state.schema.json` | `CURRENT_MACHINE_CONTRACT` | Interaction binds campaign/session/player, `input_message_id`, `intent_plan_id`, optional authenticated-principal/host-invocation evidence. Interaction is the stable accepted external invocation owner. |
| `DEV/SCHEMAS/runtime-intent-plan-state.schema.json` | `CURRENT_MACHINE_CONTRACT` | IntentPlan is bound to one `interaction_id` and contains bounded ordered IntentClauses. |
| `DEV/SCHEMAS/intent-clause.schema.json` | `CURRENT_MACHINE_CONTRACT / REALIZATION_GAP` | Stable `clause_id`, mapping/execution disposition and optional command link exist. Closed collaboration semantic class/content fields do not yet exist. |
| `DEV/TESTS/test_step3_command_intent_contract.py` | `CURRENT_TEST_CONSUMER` | RuntimeCommand explicitly links `interaction_id + intent_plan_id + clause_id`; IntentPlan allows partial/non-transactional clause completion. |

Disposition:

```text
accepted human collaboration semantic identity
    -> existing Interaction + IntentClause identity
    -> no second independent input record

collaboration-relevant semantic content
    -> must become content-sufficient in the existing accepted input owner
    -> not copied into collaboration obligation
```

Current schema absence is machine-alignment debt, not evidence that transcript prose or `value.contribution` should be reused.

---

## 3. SR17-01 mechanical `value.contribution` collision route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` | `CANONICAL_OWNER` | Rule Element is a pure embedded mechanical value object. Evaluation returns typed `value.contribution` to a deterministic Calculation Selector resolver. |
| `DEV/CATALOG/core-catalog.json` — `protocol_value_kinds/value.contribution` | `CURRENT_MACHINE_CONTRACT` | Existing exact protocol kind is already registered for mechanical Rule-Element contribution semantics. |
| `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-step-1-senior-recovery-SR17-01.md` | `SENIOR_REPAIR_AUTHORITY` | Requires mandatory semantic separation and Step-2 Interaction/message/input evidence route. |

Binding separation:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != collaboration-obligation lifecycle
```

No later WP-17 artifact may use “Contribution” alone as a machine-kind shorthand for human async input without explicitly disambiguating the domain.

---

## 4. Collaboration semantic owner / admission threshold

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | `CANONICAL_OWNER` | Three coordination families; positive bounded dependency; maximal safe frontier; required/optional contributors; absence laws; collection-only owner; reference accepted input identities; purpose/scope/generation; obsolete generation; join/rejoin/catch-up. |
| `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md` | `CANONICAL_OWNER` | `runtime.*` admitted only for independently addressable non-world operational/evidence owner needed across retry/suspension/recovery/collaboration; a durable operational lifecycle may not be hidden in chat/index/checkpoint. |
| `DEV/CATALOG/core-catalog.json` — `runtime.collaboration_obligation` | `CURRENT_MACHINE_CONTRACT` | Conditional runtime record kind already exists; presence is not per-case semantic activation. |
| `DEV/CATALOG/identifier-policies.json` | `CURRENT_MACHINE_CONTRACT` | `runtime.collaboration_obligation` currently has campaign-scoped sequential stable identity; ID order has no chronology/currentness meaning. |
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | `CANONICAL_OWNER` | Conditional `STATE/RUNTIME/COLLABORATION` campaign native root; direct known-ID route; no baseline discovery index. |

Disposition:

- record admission is activated only for durable/recoverable `AGENCY_DEPENDENT_COLLECTIVE` collection lifecycle;
- `INDEPENDENT_IMMEDIATE` creates no obligation;
- `RULE_OWNED_ORDERED` uses native owner;
- the admitted obligation is campaign-owned even when it references a LIVE/native decision opportunity;
- no baseline global collaboration index/registry is introduced.

---

## 5. Message/exact-text/content-sufficiency route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | `CANONICAL_OWNER` | `runtime.message` is stable accepted communication evidence; Interaction raw-message reference is stable evidence linkage; message may compact; semantic consumers must be content-sufficient before payload loss; exact slices are protected only when an owner requires exact form. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | `CANONICAL_OWNER` | `runtime.message` does not own gameplay obligation; disclosure is recipient-scoped; presentation retry does not replay gameplay; pending gameplay-significant communication remains with native runtime owner. |
| `DEV/SCHEMAS/runtime-interaction-state.schema.json` | `CURRENT_MACHINE_CONTRACT` | Direct `input_message_id` evidence link from Interaction. |

Disposition:

- message ID alone is too coarse for one-of-many semantic units;
- raw message prose is not copied into collaboration state;
- normalized semantic content belongs with the accepted IntentClause/input owner;
- exact wording, if still materially required, is referenced/protected through Step-5.11 exact-text evidence;
- a compacted message cannot leave a live collaboration consumer with an uninterpretable bare ID.

---

## 6. Principal / PLAYER / control / currentness route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | `CANONICAL_OWNER` | Trusted stable principal -> current PLAYER -> controlled PC -> purpose-specific authorization; campaign/LIVE/HOT currentness separation; projection nonauthority; no presence-derived authority; exact LIVE source/currentness; no stale authorization window. |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | `CANONICAL_OWNER` | Campaign membership/control/authorization policy. |
| `GAME/CORE/MULTIPLAYER.md` | `CURRENT_RUNTIME_CONSUMER` | Stable external identity binding, rejoin/controller transfer, no presence dependency, shared-scene currentness and Git-order-not-fiction behavior. |
| `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md` | `CURRENT_TEST_CONSUMER` | M05-M13 cover same PLAYER reuse, controller transfer, stale chat and no fictional side-effect from removal. |
| `GAME/SCHEMA/session.schema.yaml` | `CURRENT_MACHINE_CONTRACT / PROJECTION` | Session player/pc/base-head values are coordination observations; not current authorization or collaboration authority. |

Disposition:

- an old Interaction proves what accepted input occurred, not that its author remains authorized for a successor opportunity;
- new mutable collaboration input revalidates current principal/PLAYER/control/authorization;
- required contributor/control changes are generation-defining when they change agency admission;
- session/LIVE participant/cache/card projections may nominate only.

---

## 7. Chronology / maximal-safe-frontier route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md` | `CANONICAL_OWNER` | Native owner wins; chronology is sparse owner-anchored evidence; technical/Git/message order is not chronology; accepted execution identity/RNG persists; no global temporal frontier. |
| `GAME/CORE/CHRONOLOGY.md` | `CURRENT_RUNTIME_CONSUMER` | Partial ordering, minimum material reconciliation, Git commit order not fictional chronology, no total campaign timeline. |
| `GAME/CORE/MULTIPLAYER.md` | `CURRENT_RUNTIME_CONSUMER` | If actions are simultaneous/contested, adjudicate under rules/world timing instead of commit order; independent scenes may progress. |

Disposition:

- maximal safe frontier is owner-native evidence/reference, not a new scalar;
- visible established output stops at the same dependency frontier;
- accepted-input array/Interaction/message/ref/CAS order never becomes fictional winner/order;
- chronology ambiguity that affects outcome blocks only the dependent scope.

---

## 8. Truth / knowledge / disclosure / catch-up route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | `CANONICAL_OWNER` | Current truth stays with natural owners; `world.knowledge` owns fictional subject epistemics; `runtime.disclosure` owns human-player exposure; no role/context promotion. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | `CANONICAL_OWNER` | Bounded typed discovery, routed currentness, recipient/role eligibility, packet-first required closure, representation floors, no global scans, ContextTrace nonauthority. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | `CANONICAL_OWNER` | Message evidence and selective exactness. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | `CANONICAL_OWNER` | Recipient-scoped disclosure + EMISSION_COMMIT; no delivery ACK subsystem. |
| `GAME/CORE/INFORMATION.md` | `CURRENT_RUNTIME_CONSUMER` | Distinguishes objective truth, character knowledge/belief and what each player was told. |
| `GAME/CORE/SESSION.md` | `CURRENT_RUNTIME_CONSUMER / DEBT` | Session recap is orientation, not canon; old chat should not be reread for startup. Contains stale elapsed-time durability wording that must not become collaboration timeout authority. |

Disposition:

- catch-up is ephemeral recipient-safe projection;
- only current eligible facts/evidence + own unresolved obligations are loaded;
- full transcript/context/planning dump is forbidden;
- player exposure and PC knowledge remain distinct;
- session/collaboration cursor cannot prove human reading or currentness.

---

## 9. Durability / publication / recovery route

| Source | Class | Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | `CANONICAL_OWNER` | Exact native route, no collaboration index, index/path nonauthority. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | `CANONICAL_OWNER` | Scope-evaluated native-domain durability, immutable publication attempt, no global frontier, partial native success real, no distributed transaction, exact current composition at success. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | `CANONICAL_OWNER` | Current-authority-first recovery, typed bounded independent roots, resume accepted work not replay, session/checkpoint/cache nonauthority. |
| `GAME/CORE/RUNTIME.md` | `CURRENT_RUNTIME_CONSUMER / DEBT` | Current fast-path/agency/information laws are relevant; stale one-hour HARD wording is subordinate to WP-13 and cannot close collaboration. |

Disposition:

- an admitted open obligation is durable because survival across participant/chat loss is its admission premise;
- durability is owner-triggered, not per-message heartbeat;
- obligation publication is a normal campaign native-domain write;
- a LIVE/native dependency is revalidated, not atomically transacted with the campaign record;
- recovery can admit current open collaboration obligation as a typed root when routing/lifecycle evidence identifies it;
- referenced Interaction/IntentPlan semantic input evidence participates in required recovery closure.

---

## 10. Current machine negative evidence

At the verified Step-2 base:

- no dedicated `runtime.collaboration_obligation` schema exists in current `DEV/SCHEMAS/` or `GAME/SCHEMA/` traversal;
- current `intent-clause.schema.json` lacks closed R2.5 collaboration semantic-class + normalized-content fields;
- no dedicated async-collaboration executable regression suite surfaced;
- no current evidence establishes a required collaboration queue/scheduler/index/global frontier;
- no current evidence permits reusing `value.contribution`.

Negative evidence constrains later realization; it does not block architecture synthesis because accepted owners already determine identity/responsibility/lifecycle boundaries.

---

## 11. Consumer/debt disposition

| Consumer/debt | Current disposition |
|---|---|
| `GAME/CORE/MULTIPLAYER.md` | Preserve stable binding/currentness/no-Git-order laws; later align waiting/catch-up to final WP-17 owner model. |
| `GAME/CORE/SESSION.md` | Session remains projection/orientation. Stale elapsed-time durability language cannot become collaboration closure authority; cleanup later. |
| `GAME/CORE/RUNTIME.md` | Preserve turn/agency/currentness/input boundaries; stale one-hour HARD wording is unrelated implementation consistency debt. |
| `GAME/CORE/CHRONOLOGY.md` | Preserve partial-order/no-commit-order semantics. |
| `GAME/CORE/INFORMATION.md` | Preserve perspective separation; Step-4/R2.3/5.12 remain normative. |
| Interaction/IntentPlan/IntentClause schemas | Extend later with content-sufficient collaboration-relevant clause semantics; do not create second input record. |
| collaboration schema | Later materialize final WP-17 owner fields only if canonical result survives Step 6. |
| tests | Add WP-17 cases later under WP-22/approved implementation; no Step-2 test edits. |

---

## 12. Open-world continuation obligations

Steps 3–8 must continue discovery if they encounter material evidence outside this set.

Mandatory later checks include:

1. challenge campaign-owned obligation against LIVE close/absorption and controller-transfer cases;
2. challenge generation immutability against required-set/purpose/scope changes;
3. challenge content-sufficient IntentClause semantics against message compaction and non-executable OOC/control input;
4. challenge obligation durability against cross-chat visibility without turning every message into a persistence edge;
5. independently reconstruct Step-6 graph from `DEV/PROJECT_MAP.md`, including current consumers not used to derive the Step-3 recommendation;
6. propagate every Step-6 BLOCKING/SIGNIFICANT finding to all affected Step-3/4/5/final/status artifacts;
7. keep WP-18 downstream unless a proven contradiction makes WP-17 impossible to close.

---

## 13. Step-2 manifest gate

```text
PROJECT_MAP_TRAVERSAL_USED:                  YES
OPEN_WORLD_MANIFEST:                        YES
SR17_01_DIRECT_OWNER_ROUTE_PRESENT:         YES
R2_5_PRIMARY_OWNER_PRESENT:                 YES
STEP3_INTERACTION_INTENT_OWNER_PRESENT:      YES
STEP5_11_MESSAGE_CONTENT_SUFFICIENCY:        YES
WP16_AUTH_CURRENTNESS_PRESENT:              YES
WP15_CHRONOLOGY_PRESENT:                    YES
STEP4_R2_3_DISCLOSURE_CONTEXT_PRESENT:       YES
WP11_WP13_WP14_DURABILITY_RECOVERY:          YES
RULE_ELEMENT_VALUE_CONTRIBUTION_OWNER:       YES
INTENT_CLAUSE_MACHINE_GAP_RECORDED:          YES
COLLABORATION_SCHEMA_ABSENCE_RECORDED:       YES
CURRENT_RUNTIME_CONSUMERS_PRESENT:           YES
CURRENT_TEST_CONSUMERS_PRESENT:              YES
GENERIC_QUEUE_SCHEDULER_REQUIRED:            NO
UPSTREAM_REOPEN_REQUIRED:                    NO
HUMAN_DECISION_REQUIRED:                     NO
WP18_STARTED:                                NO
SOURCE_MANIFEST_CLOSED_WORLD:                NO
IMPLEMENTATION_CHANGED:                      NO
```
