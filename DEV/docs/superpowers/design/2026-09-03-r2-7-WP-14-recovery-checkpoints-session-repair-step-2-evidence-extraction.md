# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 2 Evidence Extraction

Status: **STEP 2 COMPLETE — EVIDENCE / COMPLETENESS GATE PASSED**

Date: 2026-09-03

Starting repaired Step-1 authority:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-senior-recovery-source-graph-omissions.md`

Companion Source-Manifest expansion:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-2-expansion.md`

---

## 1. Step-2 objective

Step 2 extracts the current owning recovery/currentness laws and reconciles them against the actual WP-10..WP-13 machine allocation plus current CORE/schema/template/support/test consumers before synthesis.

The Source Manifest remains open-world. This extraction treats every discovered current machine/support surface as evidence/consumer unless a current accepted owner grants it semantic authority.

Reopen threshold:

```text
REAL CONTRADICTION
NEW UNSATISFIED CONSUMER
MATERIAL UPSTREAM INSUFFICIENCY
```

No threshold fired.

---

## 2. Accepted owner-law extraction

### 2.1 Resumable Runtime Closure — Step 5.2

Binding consequences:

1. Recovery reconstructs only the compatible composition of **native durable owners** needed for honest continuation; it does not create a snapshot, universal recovery frontier, generic pending queue, persistent RecoveryCut or model-memory owner.
2. Fresh-process recovery may resume only state actually promised durably by the relevant native owners; destroyed unpublished HOT/SOFT state is not inferred.
3. Native ownership remains intact: world, Procedure, command/resolution, Continuation, temporal source, live owner and allocation owners remain authoritative for their state.
4. Independent roots and their correctness-required transitive dependencies are discovered through typed bounded routing/lifecycle evidence; broad campaign/WORLD/history scans are not ordinary recovery.
5. Accepted execution remains accepted: stable IDs, fixed accepted RNG, accepted invocation/interpretation evidence, mandatory child/firing identity and Continuation generation/offer are resumed rather than replayed, reallocated or rerolled.
6. If current routing selects a live/native source, that selected source is current truth for the claimed scope; an older campaign representation is not fallback truth.
7. Mutable participating sources are exact-pinned for one recovery attempt. The attempt composition is ephemeral operation evidence, not a durable authority object.
8. Derived Agenda/index/cache/context structures rebuild from validated native state.
9. Recovery requires compatible interpretation context for still-significant accepted work.
10. Ambient model/chat memory is never required recovery authority.

### 2.2 Temporal/pending continuity — Step 5.3

Binding consequences:

- independently due obligations remain owned by native temporal sources;
- once an occurrence crosses into accepted execution, stable execution/firing identity suppresses duplicate rematerialization from rebuilt Agenda;
- due/not-due is computed from owning typed chronology evidence, not ID/Git/storage/host-time order;
- no generic scheduler/job queue becomes durable authority;
- recovery preserves fixed RNG and accepted interpretation context.

### 2.3 Host/session lifecycle — Step 5.4

Binding consequences:

- host/chat/process/session lifecycle is not gameplay authority;
- controlled handoff succeeds only when the actual native durable closure needed for RRC is established;
- unexpected loss resumes only actual durable state;
- `runtime.session` is coordination/navigation/audit/observability evidence and hints only;
- session status/HEAD/timestamps/notes do not prove host liveness, current gameplay state, current live authority, successful save/handoff or a mutation lease;
- hidden model reasoning/context is not resume state;
- maintenance that invalidates the old host/context must preserve recovery-safe handoff where required.

### 2.4 SAVE/publication interaction — Steps 5.5, 5.6 and WP-13

Binding consequences:

- checkpoint existence is not SOFT/HARD/SAVE proof;
- deterministic Python/core owns publication semantics;
- campaign publication uses the fixed Connector path and an exact frozen attempt ending in non-force ref transition;
- publication outcome is accepted/rejected/indeterminate; ambiguity is resolved through bounded currentness/lineage evidence, not blind retry;
- semantic conflict rebuild preserves accepted IDs/RNG/execution;
- partial multi-domain success is real and is not rolled back merely to match a checkpoint;
- current compatible participating-source composition is required before durability acknowledgement;
- no global durability timer/frontier/queue/journal becomes recovery authority.

### 2.5 Checkpoint/recovery — Step 5.7

Binding consequences:

1. Ordinary cold recovery is **current-authority-first** and **checkpoint-optional**.
2. Campaign H is a bounded discovery anchor, not complete current state or a global frontier.
3. Current owning routes select every required native source; each mutable source is exact-pinned.
4. Root hydration preserves Step-3 accepted execution, temporal obligations and interpretation dependencies.
5. Checkpoint may be read zero times during healthy ordinary recovery.
6. Checkpoint hints require validation against current owners and are non-exhaustive by default.
7. A stale checkpoint never rolls current authority backward.
8. Checkpoint absence/malformed metadata is facility-scoped when current native RRC independently proves.
9. Repair may use checkpoint/history as bounded evidence after a detected defect; no silent historical fallback is allowed.
10. Recovery result is ephemeral `READY | RETRY | BLOCKED`; `READY` is not a lock/lease; movement normally yields bounded `RETRY`; unsatisfied prerequisite yields typed `BLOCKED`.
11. Final currentness validation is per participating authority basis.
12. Publication uncertainty never replays accepted gameplay.
13. Checkpoint creation requires independent recovery/maintenance value and is not a heartbeat, age timer, clean-save requirement or PLAY_READY requirement.
14. Checkpoint + `last_checkpoint_id` selection publish in the same campaign transaction when created/selected together.
15. Checkpoint is immutable after authoritative publication.

Current field dispositions:

| Current concept | Accepted disposition |
|---|---|
| `valid_through_event_id` | retire as generic recovery completeness/frontier semantics |
| `expected_commit_sha` | retire as self-referential containing-commit identity |
| checkpoint `world_time` | diagnostics/presentation only if retained; not chronology/currentness authority |
| active PC/thread/scene lists | optional non-exhaustive hints only if proven useful |
| checkpoint engine/runtime data | optional provenance/diagnostics; not current runtime authority |
| `MANIFEST.last_checkpoint_id` | nullable campaign-domain pointer to most recently selected/published checkpoint descriptor only |
| replacement completeness/root/source arrays | forbidden by default; require concrete bounded value and preserved ownership |

`last_checkpoint_id` is explicitly **not** current gameplay frontier, cross-domain composition, RRC proof, mandatory startup anchor or guaranteed rewind slot.

### 2.6 Historical maintenance — Step 5.7 laws 52–55

This is the controlling reconciliation for `HDM_RESET_LAST_CHECKPOINT`.

- Guaranteed historical rewind is **not** a default checkpoint property.
- Explicit historical maintenance may use a checkpoint only when every required historical native source/revision/interpretation dependency remains resolvable and compatible.
- Missing retained history produces truthful typed maintenance unavailability; it does not authorize invention.
- Historical maintenance is distinct from ordinary current recovery and must not make cold startup scan history.
- If approved historical restore/repair is intended to become new current durable state, it is established by normal **forward non-force publication** under native owner/currentness/authorization/durability rules; Git history/ref is not force-rewound.
- Current recovery correctness cannot depend on retention of old optional checkpoints.

Therefore `HDM_RESET_LAST_CHECKPOINT` cannot remain a generic “checkpoint is the rollback state” primitive. Its admissible meaning is an explicit maintenance operation using the descriptor to locate/validate a resolvable historical native composition; any current durable replacement requires a separately valid forward publication. Local reconstruction alone is not new current canon.

### 2.7 Live ownership — Step 5.8

Binding consequences:

- current campaign routing selects current live epoch/source where a scope is live-claimed;
- ACTIVE live mutation is exact-source CAS; CLOSED remains current truth until lawful absorption/forward authority movement;
- campaign base is never silent fallback current truth for a still-live claimed scope;
- stale/failed CAS does not replay mechanics/RNG/IDs;
- recovery must preserve exact-source selection while WP-16 remains owner of final physical live machine realization.

### 2.8 Chronology — Step 5.9

Checkpoint world time, event IDs, Git/source/storage/session order do not establish fictional chronology unless an owning chronology contract grants that evidence meaning. Recovery must reproduce lawful typed chronology basis without broad temporal scans.

### 2.9 Integrated recovery/concurrency — Step 5.14

Whole-system recovery requires zero-model-memory correctness and does not permit physical convenience to weaken native ownership/currentness. Checkpoint/frontier/Agenda/Story/session/host context cannot become substitute authority.

### 2.10 R2.6 host and fixed runtime repository transport — SR14-01

`DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` and `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md` bind WP-14 as follows:

- chat history, Project memory and other ambient host/model context are not campaign canon/currentness/recovery authority;
- supported gameplay/runtime path is fixed:

```text
deterministic Python/core
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition
```

- recovery/runtime may not probe/fallback through `gh`, remote native Git, private HTTP/API/token workarounds, alternate App/MCP/backend write transport, GitHub Actions gameplay bridge or equivalent paths;
- missing required Connector capability is a supported-profile capability failure;
- exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence on the fixed Connector path is part of recovery evidence.

These are shipped gameplay/runtime constraints and remain distinct from development-agent Connector discipline in `AGENTS.md` / `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`.

---

## 3. Closed R2.7 realization constraints

### WP-10

- `runtime.checkpoint`, `runtime.session`, and `runtime.maintenance_audit` are narrow admitted durable record families.
- Their existence does not create a recovery/session/repair mega-owner.

### WP-11

- checkpoint route: `CHECKPOINTS`, no semantic index;
- session route: `SESSIONS`, no semantic index;
- maintenance-audit route: `STATE/RUNTIME/MAINTENANCE_AUDITS`, no baseline semantic index;
- known-ID reads use deterministic derived exact routes;
- index absence is never semantic absence;
- derived indexes rebuild from native records;
- F03 requires current-route-first recovery and deterministic index rebuild.

### WP-12

- SQLite is HOT/cache/acceleration, not authority;
- surviving DB may be reused only after source-equivalence/deterministic-derivability proof against currently selected compatible native sources;
- local mtime/generation cannot resurrect unpublished state;
- accepted gameplay is not replayed during adoption/recovery;
- recovery composition remains ephemeral.

### WP-13

- durability is native-domain composition;
- checkpoint never proves SAVE/current/handoff;
- no universal timer/frontier/journal;
- fixed Connector gameplay path remains binding;
- current-compatible source proof is required before durable success acknowledgement.

No contradiction with Step-5 owners was found.

---

## 4. Current machine/support/test reconciliation evidence

### 4.1 `GAME/CORE/BOOTSTRAP_RUNTIME.md`

Conforming evidence:

- campaign-selection barrier and pinned campaign source;
- bounded lazy reads;
- cached base HEAD as observation/cache;
- Connector repository access path.

Debt:

- startup prose still says “latest checkpoint/hot STATE” and places checkpoint/STATE early in canonical read order.

Required machine direction: selection -> current campaign anchor -> current native routes/exact pins -> RRC roots/dependencies -> optional checkpoint -> derived rebuild -> final gate.

### 4.2 `GAME/CORE/RUNTIME.md` / `SESSION.md`

Conforming:

- current-chat continuation is ephemeral;
- session is a play/coordination container rather than gameplay state;
- cached HEAD is observable metadata.

Debt:

- session fallback-summary prose is checkpoint-centric;
- global/hourly durability language is stale WP-13 debt;
- session schema/prose lacks sufficiently explicit non-authority fences.

### 4.3 `GAME/CORE/INTEGRITY.md`

Useful current direction:

- bounded verification;
- affected mutation stops on suspect state;
- bounded repository/history evidence may assist diagnosis;
- model-memory reconstruction is disallowed.

Required refinement: “latest HEAD” must mean the current native authority composition for the affected scope, including selected live source where applicable; repair must remain owner/currentness/auth/publish constrained.

### 4.4 `GAME/CORE/STORAGE.md` / `PERSISTENCE.md`

Conforming pieces:

- fixed Connector publication flow/non-force currentness;
- cached remote basis only;
- publication race handling can preserve accepted semantic identity.

Debt:

- stale checkpoint/STATE-first recovery order;
- campaign+live overlay prose lags final Step-5.8 ownership;
- global hourly frontier language is WP-13 debt.

WP-14 consumes only recovery/currentness implications; it does not reopen unrelated storage/publication architecture.

### 4.5 `GAME/CORE/SAVE_CONTRACT.md`

Checkpoint remains separate from save, but the current file contains campaign-centric WP-13 machine debt. WP-14 must not import it as recovery authority or duplicate WP-13 scope.

### 4.6 `LIVE_SCENE.md` / `MULTIPLAYER.md`

Current prose contains useful no-campaign-fallback/close-until-absorption direction but older physical “overlay/base + live” details. WP-14 canonical result must refer to selected current live owner/source and exact pin; WP-16 remains owner of final physical live currentness/CAS machine.

### 4.7 Checkpoint/session/current-state schemas

`checkpoint.schema.yaml` and template currently encode fields already dispositioned by Step 5.7. `session.schema.yaml` carries cached HEAD/status/notes without strong enough authority fencing. `current_state.schema.yaml` includes stale global `durable_frontier_time`; WP-14 must not turn that projection into recovery authority.

### 4.8 `MANIFEST.last_checkpoint_id` — SR14-03

`GAME/SCHEMA/campaign_manifest.schema.yaml` states that `last_checkpoint_id` is the sole latest-checkpoint pointer while current chronology frontier/log cursor belong to `STATE/CURRENT`. `GAME/CAMPAIGN/MANIFEST.yaml` scaffolds it as `null`.

`GAME/TOOLS/init_campaign.py` copies/scaffolds the campaign and does not create a checkpoint to satisfy startup. Therefore:

- null is a valid normal campaign state;
- pointer lifecycle must remain checkpoint-facility metadata;
- when checkpoint K and pointer selection are published together, Step-5.7 law 49 requires one campaign transaction;
- pointer cannot select gameplay currentness/root completeness/SAVE/handoff;
- scaffold must not make checkpoint creation mandatory.

### 4.9 Maintenance commands — SR14-02

`DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` is exactly `INTERNAL CONTROL CONTRACT / PROPOSAL`: a direct support/recovery consumer, not semantic owner.

`HDM_EXPORT_CHECKPOINT_LOG` may remain a read-only checkpoint-facility diagnostic operation:

- resolve selected descriptor pointer;
- retrieve/validate through fixed Connector path;
- export provenance/validation evidence;
- never hydrate/replace HOT;
- no checkpoint means typed `NO_DURABLE_CHECKPOINT`/equivalent facility result;
- export is not authority.

`HDM_RESET_LAST_CHECKPOINT` requires semantic repair:

- exact command may authorize a destructive **maintenance** operation, but not ordinary cold-recovery rollback;
- descriptor identifies a candidate historical maintenance landmark only;
- operation must resolve all required historical native sources/revisions/interpretation dependencies before modifying local HOT;
- if historical composition is unavailable/incompatible, return typed maintenance unavailability and leave current HOT/current durable authority unchanged;
- local replacement may be built/validated/atomically swapped only as an explicitly historical local reconstruction;
- local reconstruction does not itself rewrite current durable campaign/live authority;
- if product-authorized repair is to become new current durable state, establish it by normal owner-native forward non-force publication/currentness/authorization rules;
- no force ref rewind, no alternate transport, no silent fallback;
- audit operation/outcome in `runtime.maintenance_audit` without turning audit into gameplay/event/currentness authority.

`runtime.maintenance_audit` allocation evidence:

- WP-10 admits the narrow family;
- WP-11 routes it to `STATE/RUNTIME/MAINTENANCE_AUDITS`, no semantic index;
- `DEV/CATALOG/identifier-policies.json` allocates campaign-scoped `audit-*` identity;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` classifies maintenance/diagnostic audit object;
- no separate active-branch maintenance-audit wire schema was found in Step 2. That is a later machine-realization detail, not a new authority gap.

`DEV/TOOLS/run_maintenance_audit.py` is a developer test/audit launcher, not the shipped `runtime.maintenance_audit` record owner and not part of runtime recovery authority.

### 4.10 Access and authorization

`DEV/ARCHITECTURE/ACCESS_CONTROL.md` confirms that technical GitHub/Connector capability is insufficient for application mutation authority. Any mutating repair/historical restore must have current application authorization in addition to transport currentness and native owner rules.

### 4.11 Chronology / engine interpretation

`GAME/CORE/CHRONOLOGY.md` preserves typed chronology separation. `GAME/CORE/ENGINE_UPDATES.md` requires still-significant accepted work to retain compatible interpretation basis across runtime changes/recovery. Neither checkpoint nor ambient host context may substitute.

### 4.12 Regression surfaces

Current tests split into conforming and stale expectations:

- bootstrap B25/B12 checkpoint-at-first-scene assumptions are stale unless independently justified;
- B42 already points toward loading only actually required recovery state;
- persistence PT17 permits ordinary save without checkpoint;
- PT18 demonstrates deliberately created mid-procedure checkpoint evidence including Procedure/Resolution/Continuation/fixed RNG/mandatory child/temporal refs without making checkpoint owner;
- PT19 sparse checkpoint cannot suppress current live recovery;
- PT20 checkpoint engine data is not current runtime authority;
- explicit-save cases preserve checkpoint optionality while other campaign-only SAVE debt remains WP-13-owned.

No stale test reopens accepted architecture.

---

## 5. Source-Manifest open-world expansion result

New real direct consumers/evidence identified during Step 2 and added in the companion expansion:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/CATALOG/identifier-policies.json`;
- `DEV/TOOLS/run_maintenance_audit.py` as an explicit **negative-scope/development-tool distinction** rather than runtime recovery owner;
- direct Step-5.7 laws 52–55 historical-maintenance route promoted to mandatory synthesis evidence.

Previously conditional/current consumers promoted to mandatory where Step-2 evidence proved material:

- `GAME/CORE/CHRONOLOGY.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/TOOLS/init_campaign.py`;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md`.

No new semantic owner was discovered.

---

## 6. Synthesis-completeness accounting

| Step-1 extraction axis | Result |
|---|---|
| cold recovery start/selection | COVERED |
| campaign anchor vs native source composition | COVERED |
| exact mutable-source pinning | COVERED |
| live ACTIVE/CLOSED current-source routing | COVERED |
| typed independent roots | COVERED |
| transitive dependency hydration | COVERED |
| accepted execution/Continuation/fixed RNG | COVERED |
| temporal enrollment/no duplicate materialization | COVERED |
| interpretation/catalog/rules compatibility | COVERED |
| derived rebuild | COVERED |
| surviving SQLite reuse | COVERED |
| session non-authority | COVERED |
| checkpoint optionality/facility defects | COVERED |
| checkpoint field dispositions | COVERED |
| `last_checkpoint_id` pointer/consumers/scaffold | COVERED |
| WP-11 exact routes/index rebuild | COVERED |
| READY/RETRY/BLOCKED | COVERED |
| bounded repair/no silent fallback | COVERED |
| no invented lost state | COVERED |
| chronology/currentness separation | COVERED |
| checkpoint != SAVE/handoff proof | COVERED |
| bootstrap/runtime/integrity machine debt | COVERED |
| test expectation classification | COVERED |
| ambient host/model-memory non-authority | COVERED |
| fixed gameplay Connector and failure evidence | COVERED |
| maintenance export/reset/audit route | COVERED |
| historical maintenance retention/forward-publication semantics | COVERED |
| downstream implementation/conformance routes | COVERED |

Completeness gate:

```text
SOURCE_MANIFEST_OPEN_WORLD:       YES
NEW_REAL_CONSUMERS_ADDED:         YES
SR14_01_FULLY_CONSUMED:           YES
SR14_02_FULLY_CONSUMED:           YES
SR14_03_FULLY_CONSUMED:           YES
UNRESOLVED_EVIDENCE_GAPS:         0
UPSTREAM_CONTRADICTION:           NO
NEW_UNSATISFIED_CONSUMER:         NO
MATERIAL_UPSTREAM_INSUFFICIENCY:  NO
UPSTREAM_REOPEN_REQUIRED:         NO
HUMAN_DECISION_REQUIRED:          NO
STEP_3_SYNTHESIS_ALLOWED:         YES
```

Step 2 changes no runtime/schema/template/catalog/test implementation.