# R2.7 WP-27 — Final Implementation-Planning Readiness — Canonical Specification

Status: **CANONICAL — FINAL INDEPENDENT SENIOR REVIEW PASS / GO**

Date: 2026-09-11

This specification is the WP-27 integration owner for the final implementation-planning-readiness result produced by Steps 2–8. It is implementation-facing architecture/readiness law. It is not an implementation plan, does not authorize implementation planning, and does not replace the native semantic/runtime/persistence/release owners referenced by the underlying readiness leaves.

The mandatory independent final Senior review has passed. R2.7 final reconciliation remains mandatory after WP-27 closure and before implementation-planning entry can be resolved.

## 1. Primary provenance and evidence route

Controlling process/execution input:

- `DEV/docs/superpowers/plans/2026-09-11-r2-7-WP-27-steps-3-8-audit-execution-plan.md`.

Step-2 source roles are intentionally distinct:

- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-execution-amendment.md` — Step-2 execution owner;
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md` — current admitted item-level evidence/traceability owner, including the repaired durable closure and independent re-review PASS;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-2-independent-audit.md` — historical HOLD review provenance. Its findings were subsequently repaired and independently re-reviewed; it is not the current Step-2 acceptance owner.

Run-A / Run-B / Run-C provenance:

- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-4-review-disposition.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-5-candidate-readiness-spec.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-7-finding-resolution-and-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-8-canonicalization-self-review.md`.

The Step-2 ledger is the item-level evidence/traceability owner. This specification intentionally does not duplicate the complete 224-item ledger. For any correctness-sensitive planning derivation, trace from this specification to the exact `R27-R###` readiness leaf / explicit no-work terminal and then to that leaf's native owner/source evidence.

## 2. Canonical result

WP-27 establishes:

```text
OWNER-DERIVED IMPLEMENTATION READINESS GRAPH
+ LOSSLESS READINESS-LEAF TRACEABILITY
+ EXPLICIT ACTIVATION / DEFER / REJECT / PROOF CLASSIFICATION
+ MACHINE-TO-OWNER REVERSE CONFORMANCE
+ BLOCKER-ONLY ARCHITECTURE REOPEN BOUNDARY
```

The result is **planning-ready as an architectural input**, subject to the remaining mandatory gates. This means the accepted architecture and admitted machine/evidence obligations are sufficiently classified to derive a future implementation plan without silently deciding product semantics or reopening accepted architecture.

It does **not** mean:

- implementation planning is authorized now;
- all readiness leaves are active work;
- current CI proves future semantic/scenario/empirical/release acceptance;
- a workstream grouping owns semantics;
- deferred/rejected architecture becomes future backlog;
- R2.7 final reconciliation is complete.

## 3. Closure accounting

The admitted and independently reviewed closure set is:

```text
SOURCE_ITEMS: 224 / 224

READINESS_RECORDS: 145 / 145
READINESS_MISSING: []
READINESS_DUPLICATED: []
READINESS_ID_SET:
  R27-R001..R27-R003
  + R27-R005..R27-R146
R27_R004: REMOVED / NOT RESURRECTED

EXPLICIT_NO_WORK_TERMINALS: 79 / 79
NO_WORK_ACTIVATED: 0

PO001_010: 10 / 10

ROUND2_DIAMOND_STRONG: 82 / 82
S14_S53_D15_DELTAS: PRESERVED

MACHINE_RESPONSIBILITIES: 59 / 59
MACHINE_RECORDS: R27-M01..R27-M19
MACHINE_EXCEPTION_RECORDS: R27-X01..R27-X14
MACHINE_EXCEPTION_MEMBERS: 31 / 31
MACHINE_UNOWNED_OR_UNCLASSIFIED: []
MACHINE_FALSE_AUTHORITY_PROMOTIONS: 0

HIGH_RISK_PROBES: 8 / 8 PASS
ARCHITECTURE_BLOCKER_CANDIDATES: []
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
```

The mandatory Step-6 fresh-context critic found `0 BLOCKING / 0 SIGNIFICANT / 0 MINOR`. Step 7 accounted for the frozen set as `0 / 0`, verified that Run B did not mutate the Step-5 candidate, and required no finding-driven repair or propagation.

## 4. Authority and traceability laws

### LAW R27-1 — Native owner remains semantic authority

A readiness record, workstream, test, schema path, Story projection, cache, index, checkpoint, diagnostic, status file or planning artifact does not gain semantic authority merely by carrying implementation work.

For any conflict or ambiguity:

```text
accepted native semantic/product owner
  > exact Step-2 readiness/source record for classification/traceability
  > this WP-27 integration/readiness specification
  > planning workstream summary
  > derivative router/index/status/history
```

This ordering is scope-sensitive: WP-27 owns readiness integration/classification, while the native owner still owns the underlying domain semantics.

### LAW R27-2 — Individual readiness leaves are the lossless planning atoms

Every future implementation task derived from WP-27 must name the exact readiness leaf or leaves it discharges. A task may satisfy several leaves, but an umbrella task may not erase distinct owner, activation, proof, negative-law, version/migration or defer semantics.

If a grouping cannot preserve those distinctions, split the grouping rather than weaken the leaf.

### LAW R27-3 — Coverage does not imply activation

Being present in the 224-source closure, 145 readiness leaves, 82 Round-2 records, 59 machine responsibilities or a planning workstream does not make an item current implementation work.

Activation remains controlled by the exact readiness/no-work record and its owner-defined trigger.

### LAW R27-4 — Derived structures remain derived

Story, cache, index, diagnostic, checkpoint, planning and routing structures remain projections/helpers under their accepted owners. They do not become canonical gameplay truth, knowledge, disclosure, access, chronology, currentness, identity, recovery or persistence authority.

### LAW R27-5 — Blocker-only architecture reopen

Later planning/implementation may select delegated technical details while accepted semantics stay fixed. Escalation/reopen is required if the proposed detail would determine or change:

- semantic authority or canonical state ownership;
- persistent/interface policy;
- compatibility or migration policy;
- information eligibility, disclosure or access;
- hard-to-reverse product semantics;
- another human-owned architectural boundary.

A convenient implementation choice is not permission to decide one of those boundaries silently.

## 5. Readiness disposition classes

Every source/readiness route remains in one of the following semantically distinct classes. Planning must not collapse them into one generic backlog state.

### 5.1 `ALREADY_REALIZED`

Current machine/document realization already satisfies the accepted obligation. It remains evidence/support and is not reintroduced as reimplementation debt merely because WP-27 enumerates it.

### 5.2 Implementation obligation

Accepted semantics require future concrete runtime/schema/instruction/consumer realization after the later planning/execution authorization gates.

### 5.3 Deterministic / machine verification obligation

Static/schema/unit/integration/TDD proof required for a realized contract. Verification does not create semantics and cannot substitute for another required proof class.

### 5.4 Scenario verification obligation

Scenario/adversarial acceptance over realized behavior and negative/failure/indeterminate cases. Unit/schema/static proof alone does not discharge it.

### 5.5 Empirical obligation

Supported-target / Protocol-4 / measured host-scale-performance-risk evidence. It remains dormant until the required real target/measurement condition exists.

### 5.6 Release-time obligation

Fresh-Project, exact candidate/tag/uploaded-asset, provenance/legal/package acceptance that exists only at the applicable release-candidate/release-execution boundary.

### 5.7 Dormant / deferred obligation

A current terminal disposition with an explicit revisit trigger. It is evidence that work is *not active now*, not hidden backlog.

### 5.8 Rejected / out-of-scope item

An idea or architecture path explicitly rejected or outside current scope. It is not retained as “future planning convenience.” A future change requires the proper owner/reopen process.

### 5.9 Explicit no-work terminal

A Step-2 source record whose current terminal route requires no implementation work. All 79 remain outside the active readiness partition unless their exact accepted trigger later changes the disposition.

## 6. Planning-container projection

The Step-5 workstream decomposition is accepted only as a planning projection over the 145 readiness leaves:

| Workstream | Planning concern | Readiness count |
|---|---|---:|
| `WS27-01` | supported host, transport, package and release projection | 7 |
| `WS27-02` | authority/schema/catalog convergence | 18 |
| `WS27-03` | Actor/entity execution, lifecycle, rules and projection alignment | 30 |
| `WS27-04` | role containment and Context Runtime | 7 |
| `WS27-05` | native state topology, persistence, recovery, temporal currentness and LIVE authority | 19 |
| `WS27-06` | collaboration, Story and retained Dramaturg planning surfaces | 5 |
| `WS27-07` | bootstrap/product consumers and proof-channel integration | 5 |
| `WS27-08` | writer growth and focus-scoped failure/host-risk branches | 4 |
| `WS27-09` | direct accepted Product Owner consumer integration | 7 |
| `WS27-10` | active Round-2 DIAMOND continuity | 21 |
| `WS27-11` | active Round-2 STRONG continuity | 22 |
| **TOTAL** | | **145** |

Exact membership remains the Step-5/Step-2 traceability route. The grouping is neither a semantic owner nor a mandated implementation phase sequence.

### LAW R27-6 — No universal implementation sequence

The readiness graph is a DAG. For each activated leaf, the default dependency direction is:

```text
accepted owner semantics
  -> required owner-local schema / route / template / validator
  -> required owner-local producer / consumer / runtime behavior
  -> deterministic contract/TDD proof
  -> scenario/adversarial acceptance
  -> empirical/supported-target proof when required
  -> release-time exact-asset/fresh-Project proof when applicable
```

Independent leaves/workstreams may proceed independently after future authorization when no owner/dependency edge orders them.

## 7. Product Owner continuity

All ten Product Owner entries are accounted exactly once through readiness or no-work terminal routes:

```text
PO001-01 -> R27-R097
PO002-01 -> R27-R098
PO003-01 -> R27-R099
PO004-01 -> NO_WORK_DEFERRED / released-compatibility trigger only
PO005-01 -> R27-R100
PO006-01 -> explicit no-work terminal
PO007-01 -> explicit no-work terminal; public-provenance boundary retained
PO008-01 -> R27-R101
PO009-01 -> R27-R102
PO010-01 -> R27-R103
```

```text
PO001_010: 10 / 10
OPEN_PRODUCT_OWNER_DECISION: 0
```

Incorporated Product Owner intent does not imply concrete machine realization where the accepted owner still delegates representation.

## 8. Round-2 continuity

The mandatory Round-2 evidence set remains:

```text
D01..D24 + S01..S58 = 82 / 82
MISSING: []
DUPLICATED: []
```

Changed dispositions are preserved:

```text
S14 -> R27-R131 — active narrow multiplayer Dramaturg representation
S53 -> NO_WORK_ALREADY_REALIZED
D15 -> NO_WORK_DEFERRED / measurement-dormant trigger
```

No older/weaker disposition is restored. Active DIAMOND/STRONG readiness leaves may be grouped for planning; no-work members remain terminals and are not pulled into a workstream merely to make the future plan symmetrical.

## 9. Machine reverse-conformance result

WP-27 preserves the admitted reverse mapping from machine responsibilities to accepted owners/classifications:

```text
R27-M01..R27-M19: 19 machine records
MATERIAL_RESPONSIBILITIES: 59 / 59
R27-X01..R27-X14: 14 exception records
EXCEPTION_MEMBERS: 31 / 31
UNOWNED_OR_UNCLASSIFIED: []
MIXED_GROUPS_WITHOUT_BREAKDOWN: []
FALSE_AUTHORITY_PROMOTIONS: 0
```

The audited machine families include the implicated `GAME/CORE`, `GAME/SCHEMA`, `GAME/CAMPAIGN`, `GAME/TEMPLATE`, `GAME/INSTALL`, `GAME/RULES`, `GAME/MIGRATIONS`, `GAME/TOOLS`, `GAME/ENGINE_VERSION.yaml`, and the corresponding `DEV/ARCHITECTURE`, `DEV/CATALOG`, `DEV/SCHEMAS`, `DEV/TESTS`, `DEV/TOOLS`, `DEV/RELEASE`, `.github/workflows`, `DEV/ENGINE_DEVELOPMENT.yaml` and legal/release surfaces.

Machine presence is implementation/evidence, not automatic semantic authority. Existing support is not proof of a deferred behavior unless the owning acceptance route says so.

## 10. High-risk seam probes

All eight admitted probes remain PASS:

```text
R27-P01 Story-local T0/control: PASS
R27-P02 WP-25 deferred vs rejected: PASS
R27-P03 writer-specific partition activation: PASS
R27-P04 migration/version dependency order: PASS
R27-P05 proof-channel separation: PASS
R27-P06 release-time forward gates: PASS
R27-P07 dormant scale/host triggers: PASS
R27-P08 machine reverse conformance: PASS
```

These probes are readiness evidence. They do not replace the underlying owners or future proof obligations.

## 11. Cross-system laws that implementation planning must preserve

### LAW R27-7 — LLM semantic judgment and deterministic execution remain separated

LLMs may interpret, propose, narrate, rank or otherwise perform owner-admitted semantic judgment. Accepted deterministic mechanics/execution, validation, publication/currentness and other machine-owned boundaries remain deterministic under their native owners. Model output never gains canon merely by generation.

### LAW R27-8 — Truth, knowledge, disclosure and access remain distinct

Objective/canonical world truth, fictional actor knowledge, human/player disclosure and access/eligibility are separate concerns under their accepted owners. Physical possession of data, Story locality, cache/index presence or Context materialization does not grant disclosure/access authority.

### LAW R27-9 — One physical context may preserve logical role/information containment

Accepted role isolation does not require inventing separate global context authorities. A single physical host/context may carry logically separated role/information views when the current Context Runtime/role owners preserve eligibility, containment and safe emission.

### LAW R27-10 — Publication/currentness and recovery remain owner-based

Current authority comes from current owner routing and exact owner/source currentness/publication rules, not filename recency, wall-clock time, branch appearance, cache state, checkpoint age, index order or remembered chat.

Recovery starts from current authority and owner-valid source composition. Checkpoints/caches/indexes may accelerate/rebuild but do not become canon by usefulness.

### LAW R27-11 — Retry/recovery freezes causal inputs where required

Where accepted execution has fixed causal inputs/randomness/identity, downstream retry, recovery, Story/presentation repair or transport retry must preserve them. A downstream failure must not replay already accepted mechanics, RNG or fictional action merely to regenerate presentation/transport/projection output.

### LAW R27-12 — Context Runtime remains bounded

Context Runtime remains an ephemeral/bounded assembly and delivery mechanism under accepted role/information owners. It does not become durable world state, a generic memory bus, global discovery authority or alternate knowledge/disclosure owner.

### LAW R27-13 — Catalog and current-definition identity remain exact-owner concerns

Catalog/ruleset/current-definition identity, compatibility and exact content/provenance remain under their dedicated owners. Numeric generation/version order, path identity, cache/index contents or “latest-looking” files do not substitute for exact admitted identity/currentness rules.

### LAW R27-14 — Story/T0/control authority limits survive planning

Story remains noncanonical to gameplay. Baseline Commentator self-containment may require Story-local recoverability of qualifying retained T0 meaning plus derived control/eligibility information, while native gameplay/history/knowledge/disclosure/access owners remain authoritative. No Story/cache/control projection becomes a second ACL or gameplay authority.

### LAW R27-15 — Ordinary-turn zero-extra-serial constraints remain owner-valid

Planning must preserve accepted ordinary-turn latency/serial-call constraints and may not insert an extra mandatory semantic/LLM/network serial hop merely because a workstream grouping makes centralized routing convenient.

### LAW R27-16 — WP-25 deferred versus rejected boundaries remain distinct

Owner-local failure/degradation realization may be required for the exact activated focus. Rejected global failure/health/retry/queue/scheduler/ACL architecture remains rejected. Dormant focus/measurement branches remain dormant until their exact trigger.

### LAW R27-17 — Partition/scale behavior is trigger-gated and writer-specific

PO-010/WP-24 sizing/growth law does not activate a universal partitioning project. Writer-specific measurement/size triggers may activate owner-valid partition/rollover while preserving semantic integrity, identity/currentness, atomicity and no-truncation law. No universal shard identity/topology is selected by WP-27.

### LAW R27-18 — Migration/version selection is exact-target and delta-driven

No migration exists merely because a readiness leaf names future compatibility. A concrete released source/target obligation must activate WP-20's migration boundary; the actual semantic/schema/generation delta then determines explicit directed support/migration. Version arithmetic never manufactures a path.

Current pre-release documentation canonicalization creates no migration debt.

### LAW R27-19 — Proof channels are non-substitutable

Deterministic/static/TDD proof, scenario/adversarial acceptance, empirical/supported-target measurement and release-time exact-asset acceptance are distinct. Earlier/current green evidence may support readiness but does not pre-credit a later proof class.

## 12. Explicit no-work and rejected architecture

All 79 explicit no-work terminals remain current terminals. Their exact item-level disposition and revisit trigger remain in Step-2 evidence. Cross-cutting categories include:

- released-compatibility-only migration/support obligations;
- measurement-dormant scale/host branches;
- optional extension/auxiliary/spatial/index/cache features awaiting explicit consumer/measurement triggers;
- conditional collaboration/planning work requiring owner-proven multiplayer/collective need;
- already-realized closed repairs that must not be recreated as debt.

The following generalizations remain rejected/non-authoritative and must not be revived merely to simplify future planning:

- generic memory blob or Story-as-canon/history authority;
- global context/memory bus or durable Context Runtime authority;
- global fictional chronology/currentness frontier;
- global migration registry or pre-release migration project;
- universal partition/sharding service or universal exact text-size rejection/truncation law;
- persisted global failure/health registry, generic ACL, retry/replay service, queue, scheduler or heartbeat;
- global ID registry/service where native owners already own identity;
- generic collaboration authority, transcript coordinator, global safe frontier or universal active-player gate;
- durable single-player Dramaturg/global plot graph/index/scheduler;
- checkpoint-first recovery, SQLite-as-canon, index-as-authority or path-derived identity/currentness;
- alternate gameplay Git transport fallback/probing;
- current CI/maintenance audit as semantic, empirical or release authority.

## 13. Implementation-selectable details

The following remain delegated implementation choices **only while accepted semantics remain fixed**:

- task/package/module/class/function decomposition and local internal APIs;
- exact owner-local schema spelling/encoding where the semantic contract is already determined;
- HOT/SQLite table/index/query strategy consistent with native authority and rebuildability;
- exact Story event/control-projection fields, Story-local persistence spelling, snapshot/cache layout and shard geometry;
- writer-specific page/bucket/rollover geometry after the exact growth trigger;
- exact bounded failure evaluator/adapter representation where an activated leaf requires it;
- test fixture/harness organization and diagnostic presentation;
- owner-local derived discovery/index physical layout;
- WP-20 migration declaration/transform representation only after an activating released compatibility obligation;
- performance tuning after the accepted measurement trigger.

If selecting one of these details would in fact determine semantic authority, canonical ownership, persistent/interface policy, compatibility/migration policy, disclosure/access eligibility, hard-to-reverse product semantics or another human-owned boundary, it is no longer a mere implementation detail and must return to the proper decision gate.

## 14. Version Impact Gate

This Run-C Step-8 delta canonicalizes already accepted/readiness-reviewed semantics and synchronizes development documentation. It changes no runtime module contract, persistent/protocol schema, compatibility generation, campaign/storage/catalog/ruleset generation, package/release format, release identity or migration law.

Current version owners remain unchanged:

```text
ENGINE_VERSION: 1.0-alpha
CAMPAIGN_CONTRACT_GENERATION: 2
```

Run-C classification:

```text
VERSION_IMPACT: NONE
ENGINE_VERSION_BUMP_REQUIRED: NO
MODULE_REVISION_REQUIRED: NO
PERSISTENT_SCHEMA_OR_GENERATION_BUMP_REQUIRED: NO
CATALOG_OR_RULESET_GENERATION_BUMP_REQUIRED: NO
MIGRATION_REQUIRED: NO
RELEASE_EXECUTION_REQUIRED: NO
```

Future implementation checkpoints must run the Version Impact Gate against their actual concrete delta; WP-27 preselects no future version bump.

## 15. Readiness conclusion and remaining gates

The reviewed WP-27 result is:

```text
WP27_STEP7: COMPLETE
WP27_STEP8: COMPLETE

SOURCE_ITEMS: 224 / 224
READINESS_RECORDS: 145 / 145
READINESS_MISSING: []
READINESS_DUPLICATED: []
EXPLICIT_NO_WORK_TERMINALS: 79 / 79
NO_WORK_ACTIVATED: 0
PO001_010: 10 / 10
ROUND2_DIAMOND_STRONG: 82 / 82
S14_S53_D15_DELTAS: PRESERVED
MACHINE_RESPONSIBILITIES: 59 / 59
MACHINE_EXCEPTION_MEMBERS: 31 / 31
HIGH_RISK_PROBES: 8 / 8 PASS
R27_R004: REMOVED / NOT RESURRECTED

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO

WP27_FINAL_SENIOR_REVIEW: PASS / GO
WP27_CLOSED_STATE: SEE DEV/CURRENT_PROGRESS.md — closure publication/read-back follows the Senior gate
R2_7_FINAL_RECONCILIATION: REQUIRED AFTER WP-27 CLOSURE
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
MIGRATION_EXECUTION_STARTED: NO
RELEASE_EXECUTION_STARTED: NO
GAMEPLAY_BOOTSTRAP_STARTED: NO
```

The mandatory independent Senior review found no blocking/significant defect. The only final-review finding, `SR27-FINAL-M01`, was a source-role wording defect in §1 and is corrected in this canonical text. After verified WP-27 closure publication, the exact next program unit is R2.7 final reconciliation; implementation planning remains unauthorized until that reconciliation resolves its own entry gate.