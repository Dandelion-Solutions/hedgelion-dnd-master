# Step 5.7 — Checkpoint / Recovery Protocol — Candidate Specification

Status: **CANDIDATE — SUBJECT TO ADVERSARIAL REVIEW**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Candidate architecture direction:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

This candidate defines ordinary cold recovery and checkpoint semantics after canonical Steps 5.1–5.6. It does not implement schemas/runtime code and does not finalize Step-5.8 live epoch fencing.

---

# 1. Architecture invariant

A completely cold runtime SHALL recover by proving a current compatible Resumable Runtime Closure from actual domain-native durable authorities.

Conceptually:

```text
selected campaign identity
    -> current campaign ref
    -> pin campaign H
    -> read current campaign identity/runtime/routing at H
    -> resolve current owning scopes
    -> pin exact current native source revisions
    -> enumerate typed recovery roots from native routing
    -> hydrate native owners + required transitive dependencies
    -> rebuild derived state
    -> validate currentness + compatibility + integrity + RRC
    -> READY
```

Checkpoint is never inserted into that chain as mandatory authority.

A checkpoint MAY be read as optional immutable evidence/hint when useful:

```text
checkpoint hint
    -> validate against current native authority/routing
    -> use only if still applicable
```

---

# 2. Candidate laws

## LAW 5.7-1 — ORDINARY RECOVERY IS CURRENT-AUTHORITY-FIRST

Ordinary cold resume SHALL begin from the selected campaign's current authoritative campaign ref, not from `last_checkpoint_id`, checkpoint age, event cursor, commit timestamp or cached prior-chat state.

The pinned campaign commit is a campaign-domain attempt source. It is not a universal recovery frontier.

## LAW 5.7-2 — CAMPAIGN HEAD ANCHORS DISCOVERY, NOT THE COMPLETE RECOVERY STATE

Campaign H MAY route to current live/native operational sources that own state outside campaign H.

Therefore:

```text
campaign H alone
    != proof of complete current recovery closure
```

The runtime SHALL resolve all required current owning scopes before proving RRC.

## LAW 5.7-3 — CURRENT OWNING-SCOPE ROUTING SELECTS NATIVE AUTHORITY

For every scope whose current authority is routed to another native source, recovery SHALL use the current valid source selected by that owning contract.

It SHALL NOT select a source because it is:

- mentioned by an older checkpoint;
- newest by Git commit timestamp;
- lexically latest branch;
- numerically greatest unrelated revision;
- already cached from another domain.

## LAW 5.7-4 — NO CROSS-DOMAIN RECOVERY ORDER

One recovery attempt MAY compose exact revisions such as:

```text
campaign @ H
live scope A @ LA
runtime partition P @ RP
```

but SHALL NOT infer that H, LA and RP have a common scalar order.

Compatibility is an owning-contract relation, not a max/min operation.

## LAW 5.7-5 — EVERY MUTABLE NATIVE SOURCE IS PINNED EXACTLY PER ATTEMPT

Once selected for one hydration attempt, each mutable native source SHALL be read from an exact revision identity.

No single owner may be hydrated partly from one revision and partly from a later ambient revision.

## LAW 5.7-6 — RECOVERY ATTEMPT COMPOSITION IS EPHEMERAL, NOT A NEW AUTHORITY

The Python core MAY maintain an in-memory typed `RecoveryAttempt`/equivalent containing selected domain-typed source revisions, validation state and dependencies.

This value:

- is not persisted merely because recovery occurs;
- is not current gameplay authority;
- is not a universal `RecoveryCut` record;
- has no cross-domain total-order semantics.

## LAW 5.7-7 — STEP-5.2 NATIVE TYPED ROUTING OWNS BOUNDED ROOT DISCOVERY

Operational root membership SHALL be discovered from current typed routing/lifecycle evidence native to the owning scope/partition.

Checkpoint SHALL NOT be the only registry of:

- non-settled RuntimeCommands;
- active Procedures;
- promised unresolved accepted Interaction/IntentPlan evidence;
- armed independently-due temporal source owners;
- live-local operational roots.

## LAW 5.7-8 — ROOT ROUTING IS PARTITIONABLE BY NATIVE WRITABLE SCOPE

Recovery SHALL preserve Step-5.2 partitioning. It SHALL NOT require one campaign-global root manifest if independent live/native scopes own their routing separately.

## LAW 5.7-9 — TRANSITIVE HYDRATION IS CORRECTNESS-BOUNDED

From admitted roots, hydrate only required native dependencies/references/evidence needed to prove current resume correctness.

Do not recursively load:

- arbitrary WORLD graph;
- entire LOG/history;
- Story layers;
- all checkpoints;
- all runtime records;
- all engine versions;
- transcript unless exact retained wording remains a required recovery dependency.

## LAW 5.7-10 — NATIVE OWNER PAYLOADS REMAIN SOLE STATE AUTHORITY

Checkpoint, recovery routing, source lists, hashes and recovery results SHALL NOT copy native owner state as alternate writable/current authority.

Examples:

- Procedure ResourceState remains in Procedure;
- Continuation fixed RNG/pending response remains in Continuation;
- world state remains in its native current owner;
- temporal deadline/claim state remains in its native temporal owner.

## LAW 5.7-11 — DERIVED STATE REBUILDS

Recovery SHALL rebuild non-authoritative structures from validated native sources, including as applicable:

- Temporal Agenda;
- MechanicalContext;
- dependency/query DAG caches;
- condition/effect aggregation indexes where rebuildable;
- loaded-record caches;
- Context Assembler bundles;
- model-call context.

Their absence after crash is not canon loss.

## LAW 5.7-12 — CHECKPOINT IS OPTIONAL IMMUTABLE RECOVERY/MAINTENANCE EVIDENCE

A checkpoint is an optional immutable descriptor/evidence artifact that MAY assist:

- bounded diagnostics;
- support export;
- migration/repair analysis;
- complex suspension landmarks;
- explicit historical maintenance when exact historical native sources remain available;
- future measured acceleration.

Checkpoint is not required for healthy ordinary recovery.

## LAW 5.7-13 — ORDINARY RECOVERY MAY IGNORE CHECKPOINT COMPLETELY

If current native routing provides a bounded RRC proof without checkpoint, the runtime MAY perform zero checkpoint reads.

No architecture guarantee depends on checkpoint acceleration.

## LAW 5.7-14 — CHECKPOINT HINTS REQUIRE CURRENT VALIDATION

If checkpoint is consulted, every source/root/routing hint that could affect recovery work SHALL be validated against current owning-scope authority before being treated as current.

A checkpoint observation never establishes current membership merely because it was once valid.

## LAW 5.7-15 — STALE CHECKPOINT NEVER ROLLS CURRENT AUTHORITY BACK

If current native authority has legitimately advanced beyond a checkpoint observation, ordinary recovery SHALL follow current authority.

It SHALL NOT silently restore the checkpoint's older world/runtime/live composition.

## LAW 5.7-16 — CHECKPOINT ABSENCE IS NOT RECOVERY FAILURE

A campaign with no checkpoint can recover normally if bounded native source routing and RRC are valid.

This includes an explicit save that created no checkpoint.

## LAW 5.7-17 — CHECKPOINT FAILURE IS SCOPE-LOCAL WHEN CHECKPOINT IS OPTIONAL

A missing/malformed/stale checkpoint or dangling optional checkpoint pointer MAY make checkpoint metadata/maintenance functionality `CANON_SUSPECT` under existing integrity rules.

It SHALL NOT block independent gameplay recovery if current native RRC is otherwise provable.

Any operation explicitly requiring that checkpoint remains blocked until repaired/alternative evidence is selected.

## LAW 5.7-18 — `last_checkpoint_id` IS NOT A RECOVERY FRONTIER

If retained in machine realization, `MANIFEST.last_checkpoint_id` means only:

> campaign-domain pointer to the most recently selected/published immutable checkpoint descriptor.

It does not mean:

- most current gameplay state;
- globally latest native composition;
- RRC proof;
- required cold-start anchor;
- guaranteed rollback point.

## LAW 5.7-19 — GENERIC `valid_through_event_id` IS RETIRED

A generic checkpoint SHALL NOT claim cross-domain recovery completeness through one event ID.

Any event/history coverage cursor must be domain-specific and owned by the event/history projection that uses it.

Current checkpoint `valid_through_event_id` is machine-realization debt to retire/narrow; it is noncanonical for 5.7.

## LAW 5.7-20 — SELF-REFERENTIAL `expected_commit_sha` IS RETIRED

A checkpoint included in a Git commit SHALL NOT rely on embedding the identity of that same containing commit.

Current `expected_commit_sha` checkpoint semantics are noncanonical.

Repository revision context and/or non-self-referential domain-native provenance provide revision evidence when needed.

Do not create a second metadata-only commit solely to fill a containing commit SHA after publication.

## LAW 5.7-21 — CHECKPOINT-LOCAL WORLD TIME IS NOT CHRONOLOGY AUTHORITY

Checkpoint SHALL NOT establish current chronology/due state through a copied `world_time` value.

If any time observation remains for diagnostics/presentation, it is explicitly non-authoritative and domain typed.

Step 5.9 owns final chronology persistence semantics.

## LAW 5.7-22 — CHECKPOINT ACTIVE LISTS DO NOT PROVE ROOT COMPLETENESS

Checkpoint observations such as active PC/thread/scene identities MAY remain optional hints if later measurement justifies them.

They SHALL NOT prove:

- current owning scope;
- complete operational roots;
- complete live routing;
- RRC.

## LAW 5.7-23 — CHECKPOINT ENGINE DATA IS PROVENANCE, NOT CURRENT RUNTIME AUTHORITY

Current campaign accepted runtime identity comes from current campaign authority.

Checkpoint engine/runtime metadata, if retained, is provenance/diagnostic evidence only.

Open execution may require a pinned accepted interpretation context from its native Step-3/5.2 execution owner/evidence even when current campaign runtime is newer but compatible.

## LAW 5.7-24 — RECOVERY RELEASE REQUIRES RRC PROOF

Recovery SHALL NOT release normal gameplay/writable resumption until:

1. required current native sources are selected;
2. exact revisions are pinned;
3. required roots are enumerated;
4. required native owner/dependency evidence is hydrated;
5. accepted runtime/catalog/rules interpretation prerequisites resolve compatibly;
6. required references/integrity constraints validate;
7. derived required runtime structures rebuild successfully;
8. source currentness/owning-scope validity required for resume is revalidated;
9. Resumable Runtime Closure holds.

## LAW 5.7-25 — SOURCE MOVEMENT DURING RECOVERY IS NOT CORRUPTION BY ITSELF

If an authoritative ref/source moves during hydration, recovery SHALL classify the attempt as stale/retryable unless independent evidence proves corruption.

Do not enter Canon Repair merely because another legitimate writer advanced authority.

## LAW 5.7-26 — RECOVERY RETRIES ARE BOUNDED

Automatic retries after source movement are bounded.

Persistent movement/contention yields a typed `RETRY`/coordination result rather than:

- stale resume;
- infinite loop;
- force-push;
- guessed freeze.

Step 5.8 may later provide stronger live-specific stabilization/fencing.

## LAW 5.7-27 — FINAL CURRENTNESS VALIDATION IS PER AUTHORITY SOURCE/ROUTE

Before writable/current resume release, validate all participating mutable authority selectors relevant to currentness, not merely campaign H.

At minimum:

- campaign ref/route basis;
- current live/native refs selected by that routing;
- operational routing/lifecycle revisions necessary to establish current root membership.

Do not blindly reread every immutable payload when selector/revision evidence proves it unchanged.

## LAW 5.7-28 — CONSERVATIVE CAMPAIGN ANCHOR MOVEMENT INVALIDATES CURRENT-RESUME BASIS

Initial architecture SHOULD repin/re-resolve current campaign recovery basis if campaign ref moved before writable release.

A dependency-disjoint reuse optimization MAY be added later if measured recovery contention justifies it, but it is not required by architecture.

## LAW 5.7-29 — LIVE MOVEMENT IS DEFERRED TO OWNING CURRENTNESS/FENCING CONTRACT

5.7 requires exact pinning and final owning-source validation but SHALL NOT define final live epoch fencing/lease/adoption semantics.

Step 5.8 may strengthen or specialize currentness validation for live sources.

## LAW 5.7-30 — RECOVERY DISPOSITION IS SEPARATE FROM CANON INTEGRITY STATUS

Conceptual runtime recovery result:

```text
READY
RETRY
BLOCKED
```

plus typed reason/scope/evidence.

Existing persisted integrity semantics remain separately:

```text
CANON_OK
CANON_SUSPECT
CANON_CORRUPT
```

Recovery disposition need not be a new persisted record.

## LAW 5.7-31 — UNAVAILABLE PREREQUISITE IS NOT AUTOMATIC CORRUPTION

Examples:

- required runtime package temporarily absent;
- repository/read capability unavailable;
- current source moved during hydration.

These may block/retry recovery while canon remains `CANON_OK`.

## LAW 5.7-32 — MISSING/CONTRADICTORY CURRENT AUTHORITY USES EXISTING INTEGRITY OWNERSHIP

Examples:

- current route points to missing required native source -> affected scope `CANON_SUSPECT` + recovery BLOCKED;
- contradictory current owners confirmed -> affected scope `CANON_CORRUPT` + recovery BLOCKED.

5.7 SHALL NOT create competing corruption ownership.

## LAW 5.7-33 — RECOVERY FAILURE IS SCOPE-AWARE

A blocked/suspect independent scope SHALL NOT automatically block unrelated scopes that do not depend on it, consistent with Step 5.1 and `INTEGRITY.md`.

Whether gameplay host can meaningfully proceed in another scope depends on the requested operation's dependency closure.

## LAW 5.7-34 — STEP-5.6 POST-PUBLICATION CRASH RECOVERS FROM ACTUAL REF AUTHORITY

If campaign publication succeeded remotely and process crashed before local dirty/adoption bookkeeping, cold recovery reads actual current campaign authority and adopts that durable result.

It SHALL NOT replay semantic gameplay or reconstruct old dirty state.

## LAW 5.7-35 — LOST PUBLICATION ACK DOES NOT REQUIRE CHECKPOINT

On cold restart after a Step-5.6 indeterminate transport outcome:

- if current ref reflects the intended publication/current compatible descendants, recovery uses actual current authority;
- if it does not, recovery uses the actual older current authority;
- lost unpublished HOT state is not invented;
- checkpoint cannot override this observation.

## LAW 5.7-36 — PARTIAL MULTI-DOMAIN SUCCESS REMAINS REAL

If native domain A published and domain B did not, recovery starts from actual current sources.

It SHALL NOT roll A backward to recreate an old checkpoint composition merely for symmetry.

Compatibility/RRC determine whether current composed resume is READY, RETRY or BLOCKED.

## LAW 5.7-37 — ACCEPTED GAMEPLAY IS NOT REPLAYED TO RECOVER PERSISTENCE

Recovery SHALL restore accepted execution identities/results/evidence from native owners.

It SHALL NOT reroll RNG, regenerate accepted choices, recreate IDs or rerun settled semantic actions merely because a publication/restart path is uncertain.

## LAW 5.7-38 — CHECKPOINT CREATION REQUIRES INDEPENDENT VALUE

Checkpoint MAY be created when an owning policy/request identifies real recovery/maintenance value, such as:

- complex suspension;
- controlled pause/handoff support;
- migration/repair landmark;
- explicit support/export/diagnostic request;
- another measured/configured checkpoint policy.

Ordinary save does not imply checkpoint.

## LAW 5.7-39 — CHECKPOINT CREATION MAY BE METADATA-ONLY WITHOUT BEING HEARTBEAT

If current gameplay state is already durable, an independently justified new checkpoint descriptor MAY create a real campaign metadata publication.

This is allowed because it creates meaningful requested/owned recovery evidence.

It SHALL NOT be triggered merely by age/time/freshness or used to refresh timestamps.

## LAW 5.7-40 — CHECKPOINT + POINTER PUBLICATION IS ONE CAMPAIGN TRANSACTION

If one campaign transaction creates a checkpoint and selects it as current `last_checkpoint_id`, checkpoint file + pointer change SHALL publish coherently in the same Step-5.6 campaign tree/commit/ref transaction.

No separate pointer commit is required.

## LAW 5.7-41 — CHECKPOINT IS IMMUTABLE AFTER PUBLICATION

A published checkpoint descriptor SHALL NOT be edited to “refresh” its observations or fill a self-referential commit field.

A materially new descriptor receives a new identity and is selected by normal campaign publication when warranted.

## LAW 5.7-42 — CHECKPOINT RETENTION CANNOT BE REQUIRED FOR CURRENT RECOVERY CORRECTNESS

Deleting an old optional checkpoint after it is no longer required by an explicit maintenance/history promise SHALL NOT destroy the ability to recover current gameplay state.

Physical retention/GC policy belongs primarily to Step 5.13.

## LAW 5.7-43 — GUARANTEED HISTORICAL REWIND IS NOT A DEFAULT CHECKPOINT PROPERTY

Checkpoint does not, by itself, guarantee exact rewind to old gameplay state.

An explicit historical maintenance operation may target a checkpoint only if every required historical native source/revision/interpretation dependency remains resolvable and compatible.

Otherwise it fails truthfully.

A future explicit product requirement for guaranteed rewind slots must define retention guarantees separately.

## LAW 5.7-44 — HISTORICAL MAINTENANCE DOES NOT REWRITE GIT HISTORY

Historical recovery/repair may inspect/select old evidence, but establishing a new current state after approved repair/rollback uses a normal forward corrective publication.

No force-push/ref rewind is the recovery mechanism.

## LAW 5.7-45 — CHECKPOINT MAY AID REPAIR BUT NEVER SILENTLY REPLACES CURRENT AUTHORITY

When current routing/state is suspect, checkpoint may provide bounded diagnostic/history evidence.

Selecting old checkpoint payload as current gameplay state without explicit repair/maintenance adjudication is forbidden.

## LAW 5.7-46 — IRREDUCIBLE ACCEPTED TEXT/EVIDENCE REMAINS A REAL DEPENDENCY

If accepted unresolved execution depends on exact wording/evidence not represented by structured native state, recovery must resolve that durable evidence according to Step 5.2.

Checkpoint summary does not replace it.

## LAW 5.7-47 — NO BROAD HISTORY/WORLD/CHECKPOINT SCAN ON NORMAL COLD START

Normal recovery SHALL NOT require:

- repository clone/pull;
- all WORLD traversal;
- full Git history scan;
- scanning all checkpoints to choose a maximum;
- Story/transcript catch-up;
- loading all catalog/runtime versions.

It follows typed current routes and required dependencies only.

## LAW 5.7-48 — OPTIONAL CHECKPOINT OPTIMIZATION MUST PROVE VALUE BEFORE NEW MACHINE FIELDS

5.7 SHALL NOT require new checkpoint routing fingerprints/root manifests solely on speculation.

If implementation measurement shows a bounded checkpoint hint materially reduces startup I/O, add the minimum validated hint representation without changing authority semantics.

---

# 3. Recovery protocol

## 3.1 Input

Ordinary recovery begins after campaign selection and repository/access resolution.

Conceptual input:

```text
campaign identity
selected campaign ref
acting user/session authorization context
available runtime packages/catalog resources
repository read capability
```

No prior model/chat memory is trusted as gameplay authority.

## 3.2 Phase A — pin campaign domain

Read exact current campaign ref -> H.

At H load only structural records necessary to establish:

- campaign identity/layout;
- current accepted runtime identity;
- current native owning-scope routing;
- campaign-local operational root routing partitions;
- minimum integrity/version prerequisites.

## 3.3 Phase B — resolve native source composition

For each routed native scope:

```text
route(scope) -> native source identity/ref
resolve exact current valid source revision
pin revision
```

A recovery composition is a typed set, not an ordered vector.

Missing required route/source is handled under integrity/recovery disposition; no stale checkpoint fallback.

## 3.4 Phase C — enumerate roots

Enumerate current Step-5.2 roots from native typed routing/lifecycle evidence.

Expected conceptual categories include:

```text
non-settled RuntimeCommand
active Procedure
conditionally promised unresolved Interaction/IntentPlan
armed independently-due temporal source owner
other future root class explicitly admitted by its owning contract
```

Do not redundantly root descendants already guaranteed reachable.

## 3.5 Phase D — hydrate transitive required closure

Hydrate roots and required dependencies from their pinned native sources.

Validate as encountered:

- IDs/types;
- owner lifecycle;
- required references;
- accepted interpretation context;
- fixed accepted inputs/RNG/choice evidence;
- pending child/continuation linkage;
- current world/native dependencies required to resume.

## 3.6 Phase E — optional checkpoint assistance

Only if useful for the selected recovery/diagnostic path:

1. resolve pointed/selected checkpoint immutably;
2. validate descriptor schema/campaign identity;
3. classify each observation as hint/provenance only;
4. compare relevant hints against already current native routing/source evidence;
5. use matching hints to narrow additional reads if safe;
6. ignore stale mismatches as current selectors;
7. record metadata suspicion if descriptor/pointer is malformed as appropriate.

Checkpoint MAY be read earlier as an optimization only if doing so cannot make it the source of current authority and the same validations remain mandatory.

## 3.7 Phase F — rebuild derived runtime state

Rebuild required derived indexes/caches/agendas from hydrated native authorities.

No LLM hidden state is restored.

## 3.8 Phase G — final validation/currentness gate

Before writable/current resume:

```text
validate campaign anchor currentness
validate owning routes still select expected native sources
validate currentness/fencing of participating mutable native refs
validate root routing/lifecycle consistency
validate runtime/catalog/rules compatibility
validate native required references/integrity
prove RRC
```

If source moved:

```text
RETRY / SOURCE_MOVED
```

and repin/recover affected basis subject to bounded retry policy.

If required source missing:

```text
BLOCKED / REQUIRED_SOURCE_MISSING
+ integrity suspect where persisted authority/reference is defective
```

If all pass:

```text
READY
```

---

# 4. Recovery disposition model

Conceptual result:

```text
RecoveryResult {
    disposition: READY | RETRY | BLOCKED
    reason_code?: typed reason
    affected_scopes?: typed scopes
    selected_source_evidence?: diagnostic only
}
```

This may be an in-process deterministic result; no persisted generic recovery record is required.

Initial reason vocabulary should remain bounded and implementation-owned, including equivalents of:

```text
SOURCE_MOVED
CURRENT_ROUTE_CHANGED
REQUIRED_SOURCE_MISSING
RUNTIME_UNAVAILABLE
INTERPRETATION_UNRESOLVED
INTEGRITY_SUSPECT
INTEGRITY_CORRUPT
REPOSITORY_UNAVAILABLE
AUTHORIZATION_BLOCKED
```

Do not create one reason per exception string.

---

# 5. Integrity composition

Examples:

### Healthy current campaign, no checkpoint

```text
Recovery = READY
Integrity = CANON_OK
```

### Malformed optional checkpoint, healthy native current closure

```text
Recovery = READY
Integrity(checkpoint metadata scope) = CANON_SUSPECT
Gameplay current scopes = OK
```

### Required current live route missing

```text
Recovery(scope) = BLOCKED / REQUIRED_SOURCE_MISSING
Integrity(scope) = CANON_SUSPECT
```

### Current ref moved during hydration

```text
Recovery = RETRY / SOURCE_MOVED
Integrity = no new suspicion implied
```

### Runtime package unavailable but persisted state coherent

```text
Recovery = BLOCKED / RUNTIME_UNAVAILABLE
Integrity = CANON_OK
```

### Confirmed duplicate current owner

```text
Recovery(scope) = BLOCKED / INTEGRITY_CORRUPT
Integrity(scope) = CANON_CORRUPT
```

---

# 6. Checkpoint minimum semantic contract

5.7 does not freeze a final wire schema. The minimum semantic contract is intentionally small.

A checkpoint requires stable identity and campaign association sufficient to be an immutable descriptor under repository storage.

It MAY contain:

- creation metadata for diagnostics;
- observed domain-typed source hints;
- observed active/routing hints;
- runtime provenance observation;
- maintenance/recovery notes;
- future measured acceleration evidence.

It SHALL NOT claim semantic completeness outside a specifically typed owner/domain contract.

It SHALL NOT be required to list all RRC sources.

Current v2 fields are classified as:

| Current field | Candidate disposition |
|---|---|
| `schema_version` | retain equivalent descriptor schema version |
| `id` | retain stable checkpoint identity |
| `campaign_id` | retain association |
| `created_at` | diagnostic metadata; allowed, not authority |
| `valid_through_event_id` | retire from generic checkpoint |
| `expected_commit_sha` | retire |
| `world_time` | remove from minimum; diagnostics-only if later justified/domain typed |
| `state.current_state_path` | not authority; retain only if layout indirection proves necessary |
| active PC/thread/scene lists | optional hints only; not root completeness |
| `recovery_notes` | diagnostic-only |
| `engine` | optional provenance/compatibility observation |
| `schema_data_version` | schema/migration metadata if still required by owning format |

---

# 7. Checkpoint lifecycle

Conceptual lifecycle:

```text
ABSENT
    -> optional checkpoint creation justified
PUBLISHED_IMMUTABLE
    -> may be selected by last_checkpoint pointer
    -> may become stale as native authority advances
    -> may remain useful for diagnostics/history
    -> retention may later expire
GC_ELIGIBLE
    -> physical cleanup under Step 5.13 policy
```

“Stale” is not a mutation state stored in checkpoint; it is a relation observed between immutable descriptor hints and current authority.

No refresh/update heartbeat.

---

# 8. Checkpoint creation and Step 5.6 publication

If checkpoint creation is justified in a campaign transaction:

```text
complete campaign write-set
    includes checkpoint descriptor
    includes last_checkpoint pointer update if selected
    includes any same-domain required companion state
        -> one tree
        -> one commit
        -> one non-force ref transition
```

No checkpoint-created commit becomes authority before the ref transition.

If the publication fails, the checkpoint is not selected/current merely because an unreachable commit/object exists.

If publication succeeds but local process crashes, cold recovery reads actual current campaign authority and can discover the checkpoint if needed.

---

# 9. Historical maintenance

Historical maintenance is explicitly separate from ordinary recovery.

Conceptual request:

```text
restore/inspect checkpoint K
```

Protocol:

1. resolve immutable K and its repository/history context;
2. determine exact historical native source requirements from available evidence;
3. verify every required historical source still exists;
4. verify compatibility/interpretation prerequisites;
5. produce historical diagnostic/view or proposed repair state;
6. if approved operation establishes a new current state, publish a normal forward corrective transaction.

Failure to retain dependencies => truthful typed failure.

No force-ref rewind.

No claim that all old checkpoints are forever restorable.

---

# 10. Failure scenario matrix

| # | Scenario | Required result |
|---:|---|---|
| 1 | no checkpoint, simple campaign only | native current routing -> READY |
| 2 | valid recent checkpoint | may use/ignore; same current authority result |
| 3 | stale checkpoint, newer campaign authority | ignore stale current-selection hints; no rollback |
| 4 | pointer absent | healthy recovery unaffected |
| 5 | pointer target missing | checkpoint scope suspect; independent RRC may READY |
| 6 | checkpoint malformed | same as above; no automatic gameplay block |
| 7 | required current owner missing | BLOCKED + affected scope SUSPECT |
| 8 | active Procedure without Command | Procedure found through native routing |
| 9 | suspended Resolution/Continuation/fixed RNG | hydrate from native owners; no reroll |
| 10 | committed event with pending mandatory child | root/command closure reaches descriptor; no duplicate/loss |
| 11 | armed temporal owner also reachable elsewhere | independently-due routing still contains owner; deduplicate by identity |
| 12 | promised unresolved accepted input | exact required evidence recovered or BLOCKED |
| 13 | current live head newer than checkpoint | current live owning source wins |
| 14 | pointed required live branch missing | BLOCKED + SUSPECT; no checkpoint fallback |
| 15 | closed-unabsorbed live source | classify per current live contract; Step 5.8 finalizes ownership transition |
| 16 | checkpoint engine observation old but current runtime compatible | current campaign/accepted execution contracts govern |
| 17 | open execution interpretation unavailable | BLOCKED / INTERPRETATION_UNRESOLVED |
| 18 | remote campaign save succeeded, local crash before dirty clear | current ref shows publication; resume it |
| 19 | lost ACK and remote advanced | current ref determines actual publication |
| 20 | lost ACK and remote not advanced | old current authority; lost HOT not invented |
| 21 | partial multi-domain publication | preserve actual sources; prove/deny compatible RRC |
| 22 | historical checkpoint dependencies GC'd | current recovery unaffected; historical maintenance unavailable |
| 23 | explicit historical reset | validate retained sources; forward corrective publication if performed |
| 24 | all derived caches absent | rebuild; no canon loss |
| 25 | transcript absent but typed accepted state sufficient | resume without transcript |
| 26 | exact transcript/writing is irreducible accepted dependency and missing | BLOCKED; checkpoint summary cannot substitute |
| 27 | explicit save created no checkpoint | valid save/recovery remains valid |
| 28 | independently requested checkpoint on clean durable state | metadata publication allowed; not heartbeat |
| 29 | attempted timestamp/pointer freshness checkpoint | forbidden/no write |
| 30 | campaign H moves during hydration | bounded RETRY |
| 31 | live ref moves while campaign H stays | bounded RETRY/Step-5.8 owning validation |
| 32 | repeated source churn | stop automatic retries; return typed coordination/retry result |
| 33 | orphan live branch appears newer by time | not selected without current ownership route |
| 34 | checkpoint disagrees with current root routing | current routing wins; difference not itself corruption |
| 35 | current routing internally contradicts owner lifecycle | BLOCKED + integrity diagnosis |

---

# 11. Non-goals / deferred ownership

Step 5.7 candidate does not:

- implement routing/checkpoint schema updates;
- define exact file/path names for operational root indexes;
- define final live epoch fencing/adoption/close/absorb semantics — 5.8;
- define final chronology fields — 5.9;
- define Story/transcript catch-up/retention — 5.10/5.11;
- define host disclosure delivery — 5.12;
- define physical checkpoint/orphan deletion — 5.13;
- define Python RepositoryPort transport — Step 6/deployment implementation;
- promise guaranteed historical rewind slots;
- create a universal RecoveryCut/Frontier/snapshot record.

---

# 12. Machine-realization debt

After architecture closes, implementation planning must reconcile at least:

1. `GAME/SCHEMA/checkpoint.schema.yaml`:
   - remove/narrow `valid_through_event_id`;
   - remove `expected_commit_sha`;
   - remove/narrow `world_time`;
   - reclassify active lists and engine as optional evidence/hints;
2. checkpoint template aligned to revised schema;
3. `campaign_manifest.schema.yaml` wording for `last_checkpoint_id`;
4. `BOOTSTRAP_RUNTIME.md` checkpoint-first/canon-priority wording;
5. `STORAGE.md` / `SESSION.md` detailed recovery order;
6. Step-5.2 typed partitioned recovery-routing machine representation;
7. Procedure lifecycle/root-membership machine state;
8. root-routing atomic lifecycle tests;
9. cold recovery executor in deterministic Python core;
10. recovery disposition/reason result type;
11. source-movement/final-currentness retry tests;
12. no-checkpoint recovery regression;
13. stale/malformed optional checkpoint non-blocking regression;
14. post-publication-crash/lost-ACK recovery regressions;
15. historical maintenance command wording/behavior;
16. remove stale test assumptions such as startup requiring checkpoint creation at PLAY_READY unless independently justified.

---

# 13. Candidate exit claim

If adversarial review confirms these laws, Step 5.7 will establish:

> A cold runtime recovers current gameplay by following current native authority and typed recovery routing, pinning exact participating source revisions, hydrating only correctness-required owner closure, rebuilding derived state, and releasing resume only after RRC/currentness/compatibility/integrity validation. Checkpoint remains optional immutable evidence, never a second current-state authority or universal recovery frontier.