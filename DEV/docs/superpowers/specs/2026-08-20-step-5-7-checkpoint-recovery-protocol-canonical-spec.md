# Step 5.7 — Checkpoint / Recovery Protocol — Canonical Specification

Status: **CANONICAL — STEP 5.7 ARCHITECTURE CLOSED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Canonical architecture direction:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

Canonicalization basis:

- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-task-brief.md`
- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-research-draft.md`
- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-analytical-challenge.md`
- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-candidate-spec.md`
- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-adversarial-review.md`
- `../design/2026-08-20-step-5-7-checkpoint-recovery-protocol-resolution-gate.md`

This specification defines ordinary cold recovery and checkpoint semantics on top of canonical Steps 5.1–5.6. It does not implement runtime/schema changes and does not finalize live epoch fencing/authority transfer, chronology, Story/transcript retention, physical GC, or deployment transport.

---

# 1. Canonical recovery model

A completely cold runtime with no trusted prior chat/model/process memory recovers current gameplay from actual domain-native durable authorities:

```text
selected campaign
    |
    v
pin current campaign authority H
    |
    v
read bounded campaign identity/runtime/current owning routes at H
    |
    v
resolve + exact-pin every required current native mutable source
    |
    v
enumerate Step-5.2 roots from current native typed routing/lifecycle
    |
    v
hydrate roots + correctness-required transitive dependencies
    |
    +--> optionally consult checkpoint evidence/hints
    |
    v
rebuild derived runtime state
    |
    v
validate current source/routing basis
validate authorization where required
validate interpretation/reference/integrity contracts
prove Resumable Runtime Closure
    |
    v
READY | RETRY | BLOCKED
```

Checkpoint is not a required node in this chain.

---

# 2. Authority laws

## LAW 5.7-1 — ORDINARY RECOVERY IS CURRENT-AUTHORITY-FIRST

Ordinary cold resume SHALL begin from the selected campaign's current authoritative campaign ref.

It SHALL NOT choose ordinary recovery authority from:

- `last_checkpoint_id`;
- checkpoint age/time;
- event cursor;
- commit timestamp;
- a previously cached local/chat source;
- an arbitrary historical “last known good” cut.

The pinned campaign commit is a campaign-domain recovery-attempt source, not a universal recovery frontier.

## LAW 5.7-2 — CAMPAIGN HEAD ANCHORS DISCOVERY, NOT COMPLETE STATE

Campaign H MAY route current authority for some scope to another native source such as an active live source or operational partition.

Therefore:

```text
campaign H alone != complete current Resumable Runtime Closure
```

Recovery SHALL resolve all required current owning scopes before declaring current recovery complete.

## LAW 5.7-3 — CURRENT OWNING-SCOPE ROUTING SELECTS NATIVE AUTHORITY

For every routed scope, recovery SHALL use the source selected by the current owning contract.

It SHALL NOT choose a source merely because it is:

- named by a checkpoint;
- newer by Git timestamp;
- lexically “latest”;
- numerically greater in an unrelated domain;
- already loaded from another source.

## LAW 5.7-4 — NO IMPLICIT CROSS-DOMAIN RECOVERY ORDER

One recovery attempt MAY compose exact source revisions such as:

```text
campaign @ H
live scope A @ LA
operational partition P @ RP
```

but there is no implied scalar order among H, LA and RP.

Compatibility is the conjunction of explicit owner/domain-native relations needed by the closure, not a global max/min/frontier comparison.

## LAW 5.7-5 — EACH MUTABLE NATIVE SOURCE IS EXACT-REVISION PINNED PER ATTEMPT

Once selected for a recovery attempt, every mutable source SHALL be read from one exact revision identity for that attempt.

No owner may be hydrated partly from one revision and partly from a later ambient revision.

## LAW 5.7-6 — RECOVERY ATTEMPT COMPOSITION IS EPHEMERAL OPERATIONAL STATE

Python core MAY hold an in-memory typed recovery-attempt value containing selected domain-typed revisions, roots, dependencies and validation state.

That value:

- is not gameplay authority;
- is not automatically durable;
- is not a universal `RecoveryCut` record;
- does not create cross-domain total order;
- SHALL NOT later override current native routing merely because it existed during a prior recovery.

---

# 3. Root discovery and native-owner laws

## LAW 5.7-7 — NATIVE TYPED ROUTING OWNS BOUNDED ROOT DISCOVERY

Step-5.2 current typed routing/lifecycle evidence native to each owning scope/partition SHALL establish recoverable root membership.

Checkpoint SHALL NOT be the only registry of:

- non-settled RuntimeCommands with unfinished mandatory closure;
- active Procedures;
- promised materially unresolved accepted Interaction/IntentPlan evidence where applicable;
- all armed independently-due temporal source owners;
- live-local operational roots;
- any future independently recoverable root class admitted by its owner contract.

## LAW 5.7-8 — ROUTING REMAINS PARTITIONED BY NATIVE WRITABLE/SEMANTIC SCOPE

Recovery SHALL preserve Step-5.2 routing partitioning.

No campaign-global root manifest is required merely because one recovery operation composes several scopes.

## LAW 5.7-9 — OWNER LIFECYCLE AND ROOT ENROLLMENT FORM ONE RECOVERY INVARIANT

For each independently rootable owner, current lifecycle state and current root-routing membership SHALL agree according to the owning contract.

Activation/termination and enrollment/removal must be realized transactionally enough that healthy durable state cannot expose a lifecycle/root split.

During recovery:

- legitimate movement of that basis => `RETRY`;
- persisted mismatch at one pinned current basis => integrity suspicion for the affected scope;
- checkpoint never resolves the mismatch by becoming alternate membership authority.

## LAW 5.7-10 — ROOT-MEMBERSHIP BASIS PARTICIPATES IN FINAL VALIDATION

Before `READY`, recovery SHALL validate that the routing/lifecycle basis used to enumerate roots is still accepted for the recovered attempt.

No universal routing generation is mandated. Representation remains native/implementation-specific.

## LAW 5.7-11 — TRANSITIVE HYDRATION IS CORRECTNESS-BOUNDED

Recovery hydrates admitted roots and only the transitive native dependencies/references/evidence required to prove honest resume.

Normal cold start SHALL NOT require:

- arbitrary WORLD traversal;
- entire LOG/history;
- all Story layers;
- all checkpoints;
- all runtime records;
- all engine/runtime versions;
- transcript except where exact retained wording remains a live recovery dependency.

## LAW 5.7-12 — NATIVE OWNER PAYLOADS REMAIN SOLE STATE AUTHORITY

Checkpoint, routing records, source lists, recovery diagnostics and source hashes SHALL NOT copy native current/operational state as alternate writable authority.

Examples:

- Procedure owns Procedure ResourceState;
- Continuation owns its fixed RNG/pending response/suspension evidence;
- world records own world state;
- temporal source owners own their deadline/claim/lifecycle state;
- accepted execution owners retain accepted causal inputs.

## LAW 5.7-13 — CURRENT-AUTHORITY-FIRST DOES NOT REBIND ACCEPTED HISTORICAL EXECUTION INPUTS

Selecting current mutable authorities SHALL NOT overwrite or reinterpret accepted historical/causal inputs legitimately pinned by an open Step-3 execution owner.

Recovery must resolve those accepted interpretation/dependency inputs exactly enough to resume under their owning contract, even when ambient current campaign runtime/state has advanced compatibly.

## LAW 5.7-14 — MULTIPLE DISCOVERY PATHS DO NOT MULTIPLY SEMANTIC OWNERS OR OBLIGATIONS

The same native owner/temporal obligation discovered through more than one root/path is hydrated and enrolled by stable semantic identity, not duplicated by discovery multiplicity.

In particular, Step-5.2's deliberate independently-due temporal enrollment plus another reachability path SHALL NOT create duplicate Agenda entries, occurrences or executions.

---

# 4. Rebuild laws

## LAW 5.7-15 — DERIVED STATE REBUILDS

After native hydration, recovery rebuilds non-authoritative runtime structures as applicable, including:

- Temporal Agenda;
- MechanicalContext;
- dependency/query DAG caches;
- rebuildable condition/effect indexes;
- loaded-record caches;
- Context Assembler bundles;
- model-call context;
- other derived indexes whose owner contracts define deterministic reconstruction.

Their loss across process/chat restart is not canon loss.

## LAW 5.7-16 — LOST UNPUBLISHED VOLATILE STATE IS NEVER INVENTED

If HOT/SOFT state existed only in destroyed volatile memory and never entered a promised durable closure, recovery SHALL NOT infer or reconstruct it from conversational memory, checkpoint guesses, Story prose or expected player intent.

---

# 5. Checkpoint authority and optionality laws

## LAW 5.7-17 — CHECKPOINT IS OPTIONAL IMMUTABLE RECOVERY/MAINTENANCE EVIDENCE

Checkpoint is an optional immutable descriptor/evidence artifact.

It MAY serve bounded purposes such as:

- diagnostics/support export;
- migration/repair evidence;
- complex suspension/handoff landmarks;
- explicit historical maintenance when exact dependencies remain retained;
- a future measured bounded-read optimization.

It is not current-state authority.

## LAW 5.7-18 — ORDINARY RECOVERY MAY READ ZERO CHECKPOINTS

If current typed native routing yields bounded RRC recovery directly, ordinary cold start MAY ignore checkpoint completely.

Checkpoint acceleration is not an architecture requirement.

## LAW 5.7-19 — CHECKPOINT HINTS REQUIRE CURRENT OWNER VALIDATION

Any checkpoint source/root/routing observation that could affect current recovery SHALL be validated against current native ownership/routing before use.

Historical validity does not establish present membership.

## LAW 5.7-20 — CHECKPOINT HINT SETS ARE NON-EXHAUSTIVE BY DEFAULT

Generic checkpoint observations SHALL NOT implicitly claim to enumerate every current RRC source/root.

Absence from checkpoint is not proof of current absence.

No generic checkpoint negative/completeness authority exists.

If a future specifically typed historical/maintenance contract requires a complete retained source descriptor, that contract must state its own completeness/retention semantics; it does not change ordinary checkpoint authority.

## LAW 5.7-21 — STALE CHECKPOINT NEVER ROLLS CURRENT AUTHORITY BACK

When current native authority has legitimately advanced beyond a checkpoint observation, ordinary recovery follows current authority.

It SHALL NOT silently resume the older checkpoint composition.

## LAW 5.7-22 — CHECKPOINT ABSENCE IS NOT RECOVERY FAILURE

A campaign with no checkpoint may recover normally when current native routing and RRC are valid.

An explicit save remains valid without checkpoint when Step-5.5 save durability was satisfied.

## LAW 5.7-23 — OPTIONAL CHECKPOINT DEFECTS ARE FACILITY-SCOPED

A missing/malformed/stale checkpoint or dangling optional checkpoint pointer may make checkpoint metadata/maintenance functionality `CANON_SUSPECT` under existing integrity rules.

It SHALL NOT automatically invalidate independent gameplay current-state scopes when current native RRC can be proven without the checkpoint.

Operations explicitly depending on the defective checkpoint remain blocked.

## LAW 5.7-24 — CHECKPOINT NEVER PROVES SAVE OR HANDOFF SUCCESS

Checkpoint existence/publication does not establish that Step-5.5 explicit save closure or Step-5.4 controlled handoff closure succeeded.

Those promises require their actual native durable source closure independently.

## LAW 5.7-25 — CHECKPOINT MAY AID REPAIR BUT IS NEVER SILENT FALLBACK AUTHORITY

If current routing/current authority is missing, contradictory or suspect, ordinary recovery SHALL block/retry under current authority/integrity semantics.

Checkpoint/history may provide bounded repair evidence, but SHALL NOT silently replace defective current authority with historical state.

---

# 6. Current checkpoint field disposition

Step 5.7 fixes semantics but does not freeze final replacement wire schema.

## LAW 5.7-26 — GENERIC `valid_through_event_id` IS NONCANONICAL

One event ID cannot prove campaign/live/runtime/chronology recovery completeness across independent domains.

Current checkpoint `valid_through_event_id` SHALL be retired as generic recovery completeness/frontier semantics.

A later event/history owner may define a domain-specific event coverage cursor for its own projection.

## LAW 5.7-27 — CHECKPOINT `expected_commit_sha` IS NONCANONICAL

A checkpoint stored inside a Git commit SHALL NOT depend on embedding the identity of that same containing commit.

That is self-referential under content-addressed Git construction.

Use repository revision context or other non-self-referential provenance when needed. Do not create a follow-up metadata commit solely to fill the containing SHA.

## LAW 5.7-28 — CHECKPOINT-LOCAL WORLD TIME IS NOT CHRONOLOGY AUTHORITY

Checkpoint SHALL NOT establish current chronology or due/not-due decisions from a copied `world_time` field.

Any retained human-readable time observation is diagnostics/presentation only, explicitly non-authoritative and domain typed.

Step 5.9 owns final chronology persistence.

## LAW 5.7-29 — CHECKPOINT ACTIVE PC/THREAD/SCENE LISTS DO NOT PROVE RECOVERY ROOT COMPLETENESS

Such lists MAY remain optional non-exhaustive observations only if implementation measurement shows value.

Current native routing/lifecycle, not checkpoint lists, determines current ownership/root membership.

## LAW 5.7-30 — CHECKPOINT ENGINE DATA IS OPTIONAL PROVENANCE, NOT CURRENT RUNTIME AUTHORITY

Current campaign runtime identity comes from current campaign authority.

Checkpoint runtime/engine metadata, if retained, is provenance/diagnostic evidence only.

Open accepted execution still resolves its own pinned compatible interpretation dependencies.

## LAW 5.7-31 — `last_checkpoint_id` IS A NARROW CAMPAIGN-DOMAIN DESCRIPTOR POINTER

If retained, `MANIFEST.last_checkpoint_id` means only:

> the campaign-domain pointer to the most recently selected/published checkpoint descriptor.

It is not:

- current gameplay frontier;
- latest cross-domain source composition;
- RRC proof;
- mandatory startup anchor;
- guaranteed rewind slot.

Its integrity scope is checkpoint facility metadata unless another operation explicitly depends on it.

## LAW 5.7-32 — NO NEW CHECKPOINT COMPLETENESS FIELDS WITHOUT PROVEN VALUE

Step 5.7 does not mandate new root manifests, global routing fingerprints, source-cut arrays or recovery frontier fields inside checkpoint.

Add a checkpoint hint field only when machine design/evaluation proves concrete bounded recovery/diagnostic value and preserves the authority laws above.

---

# 7. Recovery protocol

## 7.1 Preconditions

Ordinary recovery starts only after campaign selection and minimum repository/access resolution.

Do not deeply recover unselected campaigns speculatively.

No prior model/chat memory is trusted as gameplay authority.

## 7.2 Phase A — pin current campaign authority

Resolve the selected campaign ref and pin exact commit H.

At H read only bounded structural data necessary to establish:

- campaign identity/layout;
- accepted current campaign runtime identity;
- current native owning-scope routes;
- campaign-local operational routing partitions;
- minimum schema/integrity prerequisites.

## 7.3 Phase B — resolve participating native authority sources

For every required routed scope:

```text
current owning route
    -> native source identity/ref
    -> resolve current valid revision
    -> exact-pin revision for this attempt
```

Do not select by checkpoint hint, branch name ordering or commit timestamp.

## 7.4 Phase C — enumerate current operational roots

Enumerate Step-5.2 independent roots from native typed routing/lifecycle evidence.

Expected conceptual classes include:

```text
non-settled RuntimeCommand
active Procedure
conditionally promised unresolved Interaction/IntentPlan
armed independently-due temporal source owner
future explicitly admitted independent root classes
```

Do not redundantly root descendants already guaranteed boundedly reachable.

## 7.5 Phase D — hydrate correctness-required native closure

Load root owner state and required transitive dependencies under exact source revisions.

As applicable validate:

- stable IDs/types;
- owner lifecycle;
- required references;
- accepted runtime/catalog/rules interpretation;
- fixed RNG/choice/invocation evidence;
- pending child/Continuation relations;
- required current native world dependencies;
- routing/lifecycle consistency.

## 7.6 Phase E — optional checkpoint assistance

Checkpoint MAY be loaded when useful.

Safe semantics:

1. resolve immutable descriptor;
2. validate descriptor schema/campaign identity/access;
3. treat observations as hints/provenance only;
4. validate positive hints against current native routing/authority;
5. never treat omitted hints as proof of absence;
6. ignore stale observations for current source selection;
7. preserve scope-local integrity suspicion for malformed checkpoint metadata when appropriate.

An implementation MAY fetch checkpoint earlier for I/O optimization but SHALL NOT interpret it as current authority before the same validations.

## 7.7 Phase F — rebuild derived state

Rebuild required Agenda/index/cache/context structures from validated native state.

## 7.8 Phase G — final recovery gate

Before `READY`, validate at least:

- campaign anchor/current route basis relevant to the attempt;
- each participating mutable authority source under its currentness contract;
- operational routing/lifecycle root-membership basis;
- required application read/write authorization for requested capability;
- runtime/catalog/rules interpretation compatibility;
- required native references/integrity;
- Resumable Runtime Closure.

If current campaign anchor moved, conservative default is repin/re-resolve the current campaign recovery basis.

A later implementation MAY preserve proven-unaffected hydrated data after bounded disjointness proof; no such optimization is required.

If a live source moved, use the current owning live contract. Step 5.8 will define stronger live-specific stabilization/fencing/adoption rules.

Automatic retries are bounded.

---

# 8. `READY | RETRY | BLOCKED`

## LAW 5.7-33 — RECOVERY DISPOSITION IS OPERATIONAL AND NON-AUTHORITATIVE

Recovery may return a deterministic in-process result conceptually shaped as:

```text
RecoveryResult {
    disposition: READY | RETRY | BLOCKED
    reason_code?: typed reason
    affected_scopes?: typed scopes
    diagnostic_evidence?: references only
}
```

No persisted generic RecoveryResult/RecoveryCut record is required.

## LAW 5.7-34 — `READY` MEANS VALIDATED RECOVERY BASIS, NOT PERMANENT CURRENTNESS

`READY` means:

> the requested recovery/read basis passed the recovery gate and RRC was proven for that basis.

`READY` SHALL NOT mean:

- a global lock exists;
- sources cannot move after the gate;
- the runtime owns a permanent mutation lease;
- the next write may skip CAS/currentness/fencing;
- repository write capability equals gameplay authorization.

Subsequent mutations remain subject to Step-5.6 or Step-5.8 owning concurrency/authorization rules.

If authority moves immediately after `READY`, the next owning mutation/read-currentness contract detects/revalidates as required; recovery does not promise impossible race-free permanence.

## LAW 5.7-35 — `RETRY` REPRESENTS MOVEMENT/TRANSIENT STALENESS WITHOUT INVENTING CORRUPTION

Examples:

- campaign source moved while recovering;
- current route changed;
- live source advanced under legitimate writer.

Movement alone does not create `CANON_SUSPECT`.

Retries are bounded; persistent churn yields typed coordination/retry outcome rather than infinite loop.

## LAW 5.7-36 — `BLOCKED` REPRESENTS UNSATISFIED RESUME PREREQUISITE

Typed reasons may include equivalents of:

- required current source missing;
- runtime unavailable;
- accepted interpretation unresolved;
- repository/access unavailable;
- authorization denied;
- integrity suspect/corrupt.

Keep reason vocabulary bounded and typed, not one value per transport exception string.

---

# 9. Integrity composition

## LAW 5.7-37 — RECOVERY READINESS AND CANON INTEGRITY ARE DISTINCT DIMENSIONS

Existing integrity status remains:

```text
CANON_OK
CANON_SUSPECT
CANON_CORRUPT
```

Recovery disposition answers whether this runtime can resume the requested scope/capability now.

Examples:

```text
source moved:
    recovery = RETRY
    integrity = no new suspicion implied

runtime package unavailable:
    recovery = BLOCKED
    integrity = CANON_OK possible

required current route points to confirmed missing source:
    recovery = BLOCKED
    integrity(scope) = CANON_SUSPECT

confirmed contradictory current authority:
    recovery = BLOCKED
    integrity(scope) = CANON_CORRUPT

malformed optional checkpoint:
    recovery gameplay = READY possible
    integrity(checkpoint facility) = CANON_SUSPECT
```

## LAW 5.7-38 — RECOVERY/INTEGRITY FAILURE IS SCOPE-AWARE

One blocked or suspect independent scope SHALL NOT automatically invalidate unrelated scopes with no dependency on it.

The requested operation's dependency closure determines what can proceed.

---

# 10. Authorization laws

## LAW 5.7-39 — TECHNICAL REPOSITORY ACCESS IS NOT GAMEPLAY AUTHORITY

Recovery SHALL distinguish repository read/write capability from application/gameplay authorization and Step-4 disclosure eligibility.

As relevant to the requested operation, validate:

- permission to read/recover the scope;
- permission to receive player-visible material;
- permission to mutate/adopt current scope.

Authorization changes during recovery may cause `RETRY`/`BLOCKED` without implying canon corruption.

Observer/read recovery readiness does not imply write authority.

---

# 11. Source movement and concurrency laws

## LAW 5.7-40 — SOURCE MOVEMENT DURING RECOVERY IS NORMAL CONCURRENCY UNTIL PROVEN OTHERWISE

A moved authoritative source/ref does not by itself mean corruption.

Recovery SHALL repin/revalidate under bounded retry rules.

## LAW 5.7-41 — FINAL CURRENTNESS VALIDATION IS PER PARTICIPATING AUTHORITY BASIS

Recovery final validation covers each mutable authority selector relevant to current resume, including as applicable:

- campaign ref/route basis;
- routed live/native refs;
- operational root-routing/lifecycle basis.

Do not blindly reread every immutable payload when revision evidence proves it unchanged.

## LAW 5.7-42 — LIVE STABILIZATION IS OWNED BY STEP 5.8

5.7 requires exact pinning and refusal to guess stale live authority.

Step 5.8 must define practical current live adoption/fencing/epoch semantics under active concurrent writers and campaign/live transfer states.

Until then, repeated live movement may produce bounded `RETRY`/coordination requirement.

---

# 12. Step-5.6 crash-consistency interaction

## LAW 5.7-43 — POST-PUBLICATION PROCESS CRASH RECOVERS ACTUAL CURRENT AUTHORITY

If Step-5.6 campaign publication succeeded remotely but process died before local dirty/adoption bookkeeping, cold recovery pins the actual current campaign ref and adopts that durable authority.

No semantic action replay and no reconstruction of old local dirty flags.

## LAW 5.7-44 — LOST PUBLICATION ACK IS RESOLVED BY ACTUAL CURRENT SOURCES, NOT CHECKPOINT

After restart from a prior `INDETERMINATE` publication outcome:

- if current authority contains the publication/current compatible descendant state, recover it;
- if not, recover the actual older current authority;
- lost unpublished volatile state is not invented.

Checkpoint cannot override the observed current authority.

## LAW 5.7-45 — PARTIAL MULTI-DOMAIN PUBLICATION REMAINS REAL

If domain A published and domain B did not, recovery composes actual current native authorities.

It SHALL NOT roll A backward merely because no checkpoint describes the partial composition.

If current owning contracts cannot yet produce a compatible RRC, recovery returns `RETRY`/`BLOCKED`; it does not guess authority.

## LAW 5.7-46 — PERSISTENCE UNCERTAINTY NEVER REPLAYS ACCEPTED GAMEPLAY BY DEFAULT

Recovery restores accepted execution identities/results/evidence from native owners.

It SHALL NOT reroll RNG, regenerate accepted choices, allocate replacement IDs or rerun settled semantic actions merely to determine persistence outcome.

---

# 13. Checkpoint creation/publication laws

## LAW 5.7-47 — CHECKPOINT CREATION REQUIRES INDEPENDENT RECOVERY/MAINTENANCE VALUE

Checkpoint creation MAY be justified by a real owning policy/request such as:

- complex suspension landmark;
- controlled handoff/pause where descriptor adds real recovery evidence/value;
- migration/repair boundary;
- explicit support/export/historical diagnostic request;
- future event-driven checkpoint policy tied to meaningful recovery structure change.

The sole reason SHALL NOT be:

- elapsed time;
- checkpoint age;
- session count;
- “keep latest fresh”;
- clean save;
- heartbeat/capacity timestamp refresh.

If implementation cannot identify what new recovery/maintenance evidence/value is created, skip checkpoint publication.

## LAW 5.7-48 — INDEPENDENTLY JUSTIFIED METADATA-ONLY CHECKPOINT IS NOT A HEARTBEAT

A checkpoint may be a real metadata publication even when gameplay state is already durable, but only under LAW 5.7-47.

This exception does not weaken the no-heartbeat/no-op law.

## LAW 5.7-49 — CHECKPOINT + SELECTION POINTER PUBLISH IN ONE CAMPAIGN TRANSACTION

When one transaction creates checkpoint K and selects `last_checkpoint_id = K`, both changes belong to the same Step-5.6 campaign tree/commit/ref publication.

Do not create a separate pointer-update commit merely for checkpoint selection.

## LAW 5.7-50 — CHECKPOINT IS IMMUTABLE AFTER PUBLICATION

A published checkpoint descriptor SHALL NOT be edited to refresh age/time/source observations or backfill a containing commit SHA.

A materially new descriptor receives a new identity and is published only when justified.

## LAW 5.7-51 — PREPARED/UNREACHABLE CHECKPOINT OBJECTS ARE NOT SELECTED EVIDENCE

If a commit containing a new checkpoint never becomes authoritative by ref publication, the checkpoint is not selected/current checkpoint metadata merely because Git objects exist.

Step 5.6 authority rules govern.

---

# 14. Historical maintenance laws

## LAW 5.7-52 — GUARANTEED HISTORICAL REWIND IS NOT A DEFAULT CHECKPOINT PROPERTY

Checkpoint does not guarantee that historical gameplay state can always be restored.

An explicit historical maintenance operation may use checkpoint only if every required historical native source/revision/interpretation dependency is still resolvable and compatible.

Failure to retain required history produces truthful typed maintenance unavailability.

If a future product explicitly promises rewind/save slots, it requires separate retention/history/knowledge/disclosure semantics and owner approval.

## LAW 5.7-53 — HISTORICAL MAINTENANCE IS DISTINCT FROM ORDINARY CURRENT RECOVERY

Ordinary recovery targets current valid authority.

Historical maintenance intentionally inspects/selects older evidence and therefore uses a different operation contract.

Do not make ordinary cold startup scan history merely to support maintenance rewind.

## LAW 5.7-54 — HISTORICAL RESTORE/REPAIR ESTABLISHES NEW CURRENT STATE BY FORWARD PUBLICATION

After approved historical repair/rollback semantics produce a replacement current state, establish it through normal forward non-force publication.

Do not force-push/ref-rewind Git history as recovery.

## LAW 5.7-55 — CURRENT RECOVERY CORRECTNESS SHALL NOT DEPEND ON OLD CHECKPOINT RETENTION

Old optional checkpoint deletion must not destroy the ability to recover current valid gameplay state once no explicit maintenance/history promise depends on it.

Step 5.13 owns physical retention/GC details.

---

# 15. Exact accepted evidence and later retention

## LAW 5.7-56 — IRREDUCIBLE ACCEPTED EVIDENCE REMAINS A LIVE RECOVERY DEPENDENCY

If materially unresolved accepted execution depends on exact wording/evidence not yet replaced by sufficient typed state, that exact evidence must remain durably resolvable under Step 5.2.

Checkpoint prose/summary cannot replace it.

Step 5.11 transcript/history retention SHALL NOT delete such evidence merely because generic retention duration expires while the dependency remains live.

---

# 16. Normal cold-start boundedness

## LAW 5.7-57 — NO BROAD RECOVERY SCANS

Normal cold recovery SHALL NOT require:

- clone/pull;
- full repository traversal;
- all WORLD records;
- all LOG/history;
- all checkpoints;
- broad Git history;
- all Story/transcript;
- all runtime versions;
- comparison of unrelated domain revisions.

It follows current typed routes and only correctness-required dependencies.

## LAW 5.7-58 — OPTIONAL OPTIMIZATIONS MAY NOT WEAKEN CURRENT VALIDATION

Batch reads, compact routing manifests, checkpoint hints, caching or future RepositoryPort optimizations MAY reduce I/O.

They SHALL NOT replace current owning-source/root-lifecycle/compatibility validation required by this specification.

---

# 17. Minimum checkpoint semantic contract

Step 5.7 intentionally does not prescribe final schema shape.

A retained checkpoint needs only enough stable typed identity/association to function as an immutable descriptor, plus individually justified evidence fields.

Current field disposition:

| Current field | Canonical Step-5.7 disposition |
|---|---|
| `schema_version` | retain equivalent format/version identity |
| `id` | retain stable descriptor identity |
| `campaign_id` | retain campaign association |
| `created_at` | optional diagnostic metadata; no authority/order semantics |
| `valid_through_event_id` | retire as generic checkpoint recovery frontier |
| `expected_commit_sha` | retire |
| `world_time` | remove from minimum; diagnostics-only if later justified and domain typed |
| `state.current_state_path` | non-authoritative layout hint only if actual layout indirection needs it |
| active PC/thread/scene lists | optional non-exhaustive hints only |
| `recovery_notes` | diagnostic only |
| `engine` | optional runtime provenance observation |
| `schema_data_version` | retain only if format/migration ownership needs it |
| `MANIFEST.last_checkpoint_id` | optional campaign-domain pointer to selected descriptor; never recovery frontier |

The replacement schema should be minimized during implementation planning rather than preserving legacy fields by inertia.

---

# 18. Representative failure matrix

| Scenario | Canonical outcome |
|---|---|
| no checkpoint, healthy campaign-only state | native routing recovery -> READY |
| valid checkpoint available | may read or ignore; cannot change current authority result |
| stale checkpoint, newer healthy authority | stale hint ignored; no rollback |
| missing checkpoint pointer target | checkpoint facility suspect; gameplay may READY independently |
| malformed checkpoint | same facility-local handling |
| required current native source missing | BLOCKED + affected scope suspect |
| campaign source moves during recovery | bounded RETRY |
| live source moves during recovery | bounded RETRY / Step-5.8 owning contract |
| root-routing basis changes | bounded RETRY |
| root-routing/lifecycle persisted mismatch | BLOCKED + affected scope suspect |
| active Procedure with no Command | found through Procedure-native routing |
| suspended Continuation with fixed RNG | exact owner/evidence hydrated; no reroll |
| mandatory pending child | recovered through native Command/child evidence |
| armed temporal owner found through two paths | deduplicate by native identity; one obligation |
| exact accepted unresolved wording missing | BLOCKED if still required dependency |
| runtime package unavailable | BLOCKED; canon may remain OK |
| checkpoint runtime older than current campaign runtime | checkpoint provenance only; current/accepted execution contracts govern |
| confirmed campaign publish then local crash | current ref recovers published state |
| lost ACK, remote did publish | actual current source wins |
| lost ACK, remote did not publish | actual old source wins; lost HOT not invented |
| partial multi-domain publish | preserve actual sources; prove/deny current RRC |
| checkpoint created on clean state for explicit support landmark | allowed metadata publication if genuine new evidence/value |
| checkpoint created only because age threshold elapsed | forbidden heartbeat-like write |
| pointer-only freshness update | forbidden |
| old checkpoint dependencies GC'd | current recovery unaffected; historical maintenance may fail |
| current route corrupt, old checkpoint coherent | BLOCKED/repair; no silent old-source fallback |
| orphan newer-looking live branch | not authority without owning current route |
| observer has read but not write authority | recovered read basis possible; no implied write permission |
| source moves immediately after READY | next normal CAS/fencing/currentness contract protects write; READY was not a lease |

---

# 19. Machine-realization obligations

Current machine/runtime artifacts remain behind this canonical architecture.

Implementation planning must reconcile at least:

1. Step-5.2 typed partitioned recovery-routing representation;
2. Procedure lifecycle/root-enrollment evidence and atomic lifecycle/routing updates;
3. `GAME/SCHEMA/checkpoint.schema.yaml` reduction/narrowing;
4. checkpoint template alignment;
5. narrow `campaign_manifest.last_checkpoint_id` wording/validation;
6. current-authority-first `BOOTSTRAP_RUNTIME.md` recovery order;
7. `STORAGE.md` / `SESSION.md` recovery flow alignment;
8. deterministic Python cold-recovery executor;
9. non-authoritative `RecoveryResult`/reason vocabulary;
10. exact native source pinning/currentness validation;
11. root-routing/lifecycle final validation;
12. bounded retry behavior;
13. no-checkpoint healthy recovery regression;
14. stale/malformed optional checkpoint non-blocking regression;
15. missing current source -> scoped integrity/recovery regression;
16. post-publication crash/lost-ACK recovery regressions;
17. partial multi-domain recovery regression;
18. duplicate root-path temporal/owner deduplication regression;
19. authorization movement/read-vs-write recovery tests;
20. accepted exact evidence retention dependency regression;
21. maintenance checkpoint export/reset semantics;
22. remove stale assumptions requiring checkpoint at ordinary PLAY_READY/save absent independent justification.

These obligations do not authorize broad GAME/schema implementation before the architecture sequence's implementation gate.

---

# 20. Later-slice binding constraints

## Step 5.8 — Multiplayer / Live-Epoch Ownership

Must define live-specific currentness/fencing/adoption semantics sufficient for:

- cold host recovery while another live writer may exist;
- repeated live source movement;
- closed-but-unabsorbed/abandoned/rollover states;
- partial campaign/live authority-transfer crash windows;
- unambiguous current source selection without checkpoint/time guessing.

## Step 5.9 — Chronology

Checkpoint-local time cannot substitute for chronology authority.

## Step 5.11 — Transcript/history retention

Exact wording/evidence that remains an irreducible Step-5.2 recovery dependency is not deletion-eligible merely because general transcript retention expires.

## Step 5.13 — GC/orphans

Owns physical checkpoint retention/deletion/orphan cleanup. Current recovery correctness cannot depend on arbitrary old checkpoint retention.

## Step 6

Owns final runtime/migration/package and RepositoryPort host/deployment realization. It may optimize physical recovery transport but cannot weaken current-authority/native-routing semantics.

---

# 21. What Step 5.7 does NOT introduce

No:

- universal RecoveryCut record;
- global recovery frontier/sequence;
- checkpoint snapshot authority;
- checkpoint-owned runtime state;
- checkpoint-owned operational root registry;
- global compatibility scalar;
- serialized Temporal Agenda;
- automatic historical rollback;
- force-push recovery;
- checkpoint heartbeat;
- requirement to checkpoint every save/handoff;
- requirement to scan all history/checkpoints/world on cold start;
- raw LLM/process memory persistence.

---

# 22. Canonical closure statement

Step 5.7 architecture is closed with this invariant:

> A cold HDM runtime recovers current gameplay by following current native authority and typed recovery routing, pinning exact participating source revisions, hydrating only the correctness-required native owner closure, rebuilding derived state, and releasing a validated recovery basis only after currentness/routing, authorization where relevant, interpretation, integrity and RRC checks pass. Checkpoint is optional immutable evidence/maintenance metadata; it may be absent, stale or ignored without becoming a second current-state authority or universal recovery frontier.

`READY` is deliberately not a post-recovery lock or write lease. Every later mutation still obeys its owning CAS/fencing/currentness/authorization contract.