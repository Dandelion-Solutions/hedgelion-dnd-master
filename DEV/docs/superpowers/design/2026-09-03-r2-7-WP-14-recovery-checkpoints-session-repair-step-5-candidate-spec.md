# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 5 Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE READY FOR MANDATORY WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-03

Selected direction:

> **PINNED CURRENT-SOURCE RRC RECOVERY + OPTIONAL CHECKPOINT ASSISTANCE + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE**

---

## 1. Scope and authority

This candidate specifies the WP-14 implementation-facing recovery/checkpoint/session/repair contract. It composes accepted Step-3/Step-5, R2.6 and WP-10..WP-13 authority; it does not create a new gameplay state owner.

Conceptual operation objects in this specification are ephemeral unless an existing durable family explicitly owns a record.

---

# 2. Ordinary current recovery

## LAW WP14-1 — ORDINARY RECOVERY TARGETS CURRENT NATIVE AUTHORITY

Ordinary cold recovery reconstructs a compatible current Resumable Runtime Closure from the actual current native durable authorities selected by current owning routes.

Checkpoint, session, SQLite, ambient chat/model context, support exports, Story and repair evidence are not alternate current-state owners.

## LAW WP14-2 — CAMPAIGN REVISION IS A DISCOVERY ANCHOR, NOT COMPLETE CURRENT STATE

After campaign selection, recovery exact-pins the selected campaign ref to campaign revision H through the supported gameplay Connector path.

H supplies bounded campaign identity/layout/runtime/current-routing evidence. H is not a universal cross-domain frontier and is not fallback truth for scopes currently owned elsewhere.

## LAW WP14-3 — CURRENT ROUTES SELECT NATIVE SOURCES

For every required mutable scope:

```text
current owning route
-> native source identity/ref
-> exact current revision for this attempt
```

No source is selected by checkpoint pointer, checkpoint age, session HEAD, commit timestamp, lexicographic ref order, local database freshness or ambient memory.

## LAW WP14-4 — LIVE-OWNED CURRENT TRUTH NEVER FALLS BACK TO CAMPAIGN STATE

When current routing selects a live-owned source, recovery exact-pins that selected live source under Step-5.8 currentness semantics.

ACTIVE and CLOSED_UNABSORBED/current-live states remain current truth for their claimed scope until lawful authority movement/absorption. Missing/incompatible/moving selected live authority yields owning `RETRY`/`BLOCKED` semantics, never silent campaign fallback.

## LAW WP14-5 — ONE RECOVERY ATTEMPT USES ONE EXACT PIN PER PARTICIPATING MUTABLE SOURCE

A recovery attempt records an ephemeral exact source basis sufficient to validate the attempt. It does not persist a generic RecoveryCut/frontier/source manifest.

Mixed branch-relative revisions are invalid.

## LAW WP14-6 — INDEPENDENT ROOT DISCOVERY IS TYPED AND BOUNDED

Recovery enumerates current independent roots from native routing/lifecycle evidence, including as applicable:

- non-settled RuntimeCommand;
- active Procedure;
- unresolved conditionally promised Interaction/IntentPlan;
- armed independently-due temporal source owner;
- future explicitly admitted independent root classes.

Known-ID reads use WP-11 exact derived routes. Ordinary recovery does not require campaign-wide directory scans, full WORLD traversal, full LOG/history, all checkpoints, all runtime records or broad Git history.

## LAW WP14-7 — TRANSITIVE HYDRATION IS CORRECTNESS-REQUIRED ONLY

From admitted roots, recovery loads only native dependencies/references/evidence required to prove honest continuation under the pinned source basis.

Multiple discovery paths deduplicate by stable semantic identity.

## LAW WP14-8 — ACCEPTED EXECUTION IS RESUMED, NEVER REPLAYED BY RECOVERY

Recovery preserves, as applicable:

- RuntimeCommand/Procedure/Resolution identity and lifecycle;
- fixed accepted RNG evidence;
- accepted invocation/catalog/rules/dependency interpretation;
- Continuation generation/offer and fixed pending response evidence;
- mandatory child/firing identities;
- accepted Choice/Reaction and causal receipts/evidence.

Process/chat/SQLite loss, publication uncertainty, source movement or checkpoint mismatch SHALL NOT reroll RNG, allocate replacement accepted IDs, regenerate accepted choices or replay settled semantic actions.

## LAW WP14-9 — TEMPORAL RECOVERY REMAINS NATIVE-OWNER BASED

Armed temporal obligations are enrolled from native temporal owners. Once an occurrence crossed into accepted execution, stable accepted firing/execution identity suppresses duplicate rematerialization from a rebuilt Agenda.

Agenda is derived and rebuildable; no generic pending/job queue becomes authority.

## LAW WP14-10 — INTERPRETATION CLOSURE IS REQUIRED

Still-significant accepted work must recover compatible accepted runtime/catalog/rules/invocation/dependency context. Ambient current runtime or model memory may not silently reinterpret historical accepted work.

Exact retained wording/evidence remains a recovery dependency only where its owning contract still makes it irreducible.

## LAW WP14-11 — AMBIENT HOST CONTEXT HAS NO RECOVERY AUTHORITY

Chat history, Project memory, model context and hidden reasoning may not establish campaign canon/currentness, recover lost unpublished state, select sources or supply missing historical dependencies merely because the material is physically present.

Lawfully eligible current owner evidence remains usable normally; ambient presence alone is insufficient.

---

# 3. Local HOT / SQLite / derived state

## LAW WP14-12 — SURVIVING SQLITE IS CONDITIONAL CACHE/ACCELERATION ONLY

A surviving WP-12 database may be reused only after proving the relevant bytes/helpers are equal to or deterministically derivable from the selected compatible native source/evidence basis for the operation.

Local mtime, generation or apparent freshness cannot resurrect unpublished state or missing historical authority.

## LAW WP14-13 — DERIVED STATE REBUILDS FROM VALIDATED NATIVE STATE

Agenda, query/index/cache/context structures and other rebuildable projections reconstruct after native hydration.

Index absence is not semantic absence. A broken/missing derived index does not authorize broad semantic fallback when the native exact route is known.

---

# 4. Checkpoint role

## LAW WP14-14 — CHECKPOINT IS OPTIONAL IMMUTABLE DESCRIPTOR/EVIDENCE

A checkpoint may support diagnostics/export, migration/repair evidence, complex suspension/handoff landmarks, explicit historical maintenance when retained dependencies permit it, or future measured bounded acceleration.

It is not current gameplay authority, a root registry, SAVE/handoff proof, session lease, mandatory startup anchor or universal frontier.

Healthy ordinary recovery may read zero checkpoints.

## LAW WP14-15 — CHECKPOINT HINTS ARE POSITIVE/NON-EXHAUSTIVE AND CURRENT-VALIDATED

Checkpoint observations that could affect ordinary current recovery are hints only:

- positive hints require validation against current native owner/routing evidence;
- omitted hints never prove absence;
- stale hints never select older current authority;
- malformed/dangling optional checkpoint metadata is checkpoint-facility scoped unless the requested operation depends on it.

## LAW WP14-16 — CURRENT CHECKPOINT FIELD DISPOSITION IS BINDING

Implementation must reconcile current schema/template as follows:

- retire generic `valid_through_event_id` recovery-completeness/frontier semantics;
- retire self-referential containing-commit `expected_commit_sha`;
- checkpoint world-time observation is non-authoritative diagnostics only if retained;
- active PC/thread/scene lists are optional non-exhaustive hints only if proven useful;
- engine/runtime metadata is optional provenance/diagnostics, not current runtime authority;
- no replacement global root/source completeness array is introduced without separate proven bounded value and preserved ownership.

WP-14 fixes semantics, not final YAML field names.

## LAW WP14-17 — `MANIFEST.last_checkpoint_id` IS ONLY A NULLABLE CAMPAIGN-DOMAIN DESCRIPTOR POINTER

The pointer means only the most recently selected/published checkpoint descriptor in the campaign domain.

It is not gameplay frontier, cross-domain composition, RRC proof, SAVE/handoff proof, root completeness, startup requirement or guaranteed rewind slot.

`null` is a valid healthy campaign/scaffold value.

## LAW WP14-18 — CHECKPOINT SELECTION PUBLICATION IS CAMPAIGN METADATA PUBLICATION

When checkpoint K is created and selected together, K and `last_checkpoint_id = K` publish in one normal campaign tree/commit/ref transaction under WP-13/Step-5.6 currentness.

No pointer-only freshness heartbeat is justified. Prepared/unreachable K is not selected evidence.

---

# 5. Session role

## LAW WP14-19 — `runtime.session` IS COORDINATION/NAVIGATION/AUDIT/OBSERVABILITY ONLY

Session records may carry associations and cached observations such as player/PC/scene IDs, base/published HEAD observations, status, timestamps and notes.

They do not independently prove:

- host liveness/death;
- current gameplay/live state;
- write authority;
- successful save/handoff;
- recovery frontier;
- Procedure/Resolution/fictional-scene termination.

Ordinary cold recovery does not require a session record.

---

# 6. Recovery result and final validation

## LAW WP14-20 — ORDINARY RECOVERY RESULT IS EPHEMERAL `READY | RETRY | BLOCKED`

Conceptually:

```text
RecoveryResult {
  disposition: READY | RETRY | BLOCKED
  reason_code?: bounded typed reason
  affected_scopes?: typed scopes
  diagnostic_evidence?: references only
}
```

No persisted generic RecoveryResult/RecoveryCut is required.

## LAW WP14-21 — `READY` REQUIRES FINAL VALIDATION OF THE PARTICIPATING BASIS

Before `READY`, validate as applicable:

- campaign anchor/current route basis;
- each participating mutable current source under its native currentness contract;
- operational root-routing/lifecycle basis;
- required application read/write authorization for requested capability;
- disclosure eligibility for material that may become player-visible;
- accepted runtime/catalog/rules interpretation compatibility;
- required native references/integrity;
- complete RRC for the requested operation scope.

`READY` is not a lock/lease. Every later write still obeys owner currentness/CAS/fencing/authorization.

## LAW WP14-22 — LEGITIMATE MOVEMENT IS `RETRY`, NOT CORRUPTION

Campaign/source/route/root-lifecycle movement during recovery is normal concurrency until evidence establishes inconsistency. Recovery repins/re-resolves under bounded retry policy.

Persistent churn yields typed coordination/retry exhaustion, not infinite loop.

## LAW WP14-23 — UNSATISFIED REQUIRED BASIS IS SCOPE-AWARE `BLOCKED`

Missing/incompatible required current source, unavailable interpretation/runtime, repository/capability failure, authorization denial or proven integrity defect blocks the dependent requested scope/capability. Independent scopes are not automatically invalidated.

---

# 7. Fixed gameplay repository transport

## LAW WP14-24 — RECOVERY USES THE FIXED R2.6 GAMEPLAY CONNECTOR PATH

Supported runtime remote operations remain:

```text
deterministic Python/core preparation/validation
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition where writing
```

No recovery/save/maintenance/live operation probes or falls back to `gh`, remote native Git, private HTTP/API/token paths, alternate App/MCP/backend transport, GitHub Actions gameplay bridge or equivalent alternatives.

## LAW WP14-25 — MISSING REQUIRED CONNECTOR CAPABILITY IS TYPED SUPPORTED-PROFILE FAILURE

If the fixed runtime path lacks a required operation, return the appropriate typed blocked/capability/maintenance outcome. Do not activate a transport selector.

Exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence remains part of recovery/repair verification.

---

# 8. Repair

## LAW WP14-26 — REPAIR IS EXPLICIT, BOUNDED AND EVIDENCE-GATED

Baseline:

```text
legitimate current source/routing movement
  -> RETRY / repin

required pinned basis missing/incompatible/contradictory
  -> BLOCKED affected scope
  -> integrity classification according to evidence

optional checkpoint facility defect, independent current RRC healthy
  -> checkpoint facility suspect/blocked as applicable
  -> unrelated gameplay may READY
```

Checkpoint/history/session/transcript/support export may aid diagnosis only under their owning evidence roles. No historical evidence silently replaces current authority.

## LAW WP14-27 — MUTATING DURABLE REPAIR REQUIRES APPLICATION AUTHORIZATION AND OWNER-NATIVE CURRENTNESS

Technical repository/Connector write capability and maintenance-token recognition are insufficient for arbitrary durable gameplay mutation.

A mutating repair must satisfy current application authorization, native owner rules, currentness/CAS/conflict semantics and WP-13 durability/publication requirements.

---

# 9. Historical maintenance

## LAW WP14-28 — HISTORICAL MAINTENANCE IS DISTINCT FROM ORDINARY CURRENT RECOVERY

Historical maintenance deliberately reconstructs/inspects an older evidence composition. It never changes the source-selection target of ordinary cold recovery.

No guaranteed rewind window exists unless a future separately approved product/retention contract creates one.

## LAW WP14-29 — HISTORICAL RECONSTRUCTION REQUIRES COMPLETE PROVABLE REQUIRED HISTORICAL COMPOSITION

For the requested maintenance scope, every required historical native source/revision/interpretation dependency must remain resolvable, compatible and attributable to owner-valid evidence.

Checkpoint descriptor is locator/provenance evidence, not automatically a complete source manifest. Omitted checkpoint hints do not prove absence. Nearest timestamps/IDs/commits and campaign fallback are not allowed guesses.

If required historical composition cannot be proven, historical maintenance is truthfully unavailable.

## LAW WP14-30 — HISTORICAL LIVE-OWNED TRUTH MAY NOT FALL BACK TO CAMPAIGN STATE

If the historical maintenance scope was live-owned, the required historical live source/revision/ownership basis must be resolvable from retained owner-valid evidence. Otherwise the dependent reconstruction is unavailable.

## LAW WP14-31 — HISTORICAL LOCAL RECONSTRUCTION IS MAINTENANCE-ISOLATED/NON-CURRENT

A validated historical local store may be built separately and locally substituted only as an explicit maintenance state.

It SHALL NOT become ordinary gameplay `READY` or current canon merely because local integrity/RRC validation passes.

Until lawful current promotion succeeds, the runtime must not accept new ordinary gameplay mutation as though the historical store were current authority.

## LAW WP14-32 — CURRENT PROMOTION OF HISTORICAL REPAIR IS FORWARD PUBLICATION ONLY

If a separately application-authorized historical repair/rollback is intended to become new current durable state:

- construct owner-native replacement state under accepted semantics;
- satisfy current application authorization and currentness/conflict requirements;
- establish new current authority through normal forward non-force publication/CAS/durability contracts;
- adopt the accepted new current authority locally only after confirmed establishment.

Never force-push, ref-rewind or treat local historical reconstruction as remote authority.

---

# 10. Maintenance commands

## LAW WP14-33 — `HDM_EXPORT_CHECKPOINT_LOG` IS READ-ONLY DIAGNOSTIC EXPORT

The command:

1. pins campaign revision H through the fixed Connector path;
2. resolves `last_checkpoint_id` as-of H;
3. returns typed no-checkpoint result if null;
4. resolves/validates the immutable descriptor under applicable access rules;
5. exports allowed diagnostic/provenance/validation evidence, explicitly tied to its observed basis;
6. does not hydrate/replace HOT or move authority;
7. does not create gameplay turn/event/chronology/currentness evidence.

If campaign pointer moves during export, output must remain truthfully labelled as-of its pinned basis or the command may boundedly repin/retry when its UI contract requires current-latest semantics. It may not silently claim stale evidence is current.

## LAW WP14-34 — `HDM_RESET_LAST_CHECKPOINT` IS CONDITIONAL HISTORICAL MAINTENANCE, NOT GENERIC ROLLBACK

The exact maintenance token may authorize the defined local destructive maintenance attempt, subject to support/application access policy.

Required flow:

1. pin current campaign basis and resolve selected checkpoint pointer;
2. resolve/validate immutable descriptor;
3. prove the complete required historical native composition for the maintenance scope;
4. load exact historical native sources/dependencies/accepted interpretation evidence without replay/reroll;
5. on any required retention/compatibility gap, return typed maintenance unavailability and leave current local/durable state unchanged;
6. build and validate a separate historical local store;
7. atomically substitute the local store only into maintenance-isolated/non-current state while preserving the previous local store until success;
8. do not resume ordinary gameplay from that state until lawful current promotion is accepted, or discard it and return to ordinary current recovery;
9. any current durable promotion follows LAW WP14-32;
10. record maintenance operation/outcome through the narrow audit family without converting audit into authority.

## LAW WP14-35 — `runtime.maintenance_audit` IS A NARROW SUPPORT AUDIT RECORD

The family is campaign-scoped, uses current `audit-*` identity policy and WP-11 `STATE/RUNTIME/MAINTENANCE_AUDITS` route with no semantic index requirement.

It may record stable maintenance operation identity, command/type, scope, observed evidence/provenance and outcome at implementation-defined precision.

It is not gameplay history, chronology, currentness, recovery journal, root registry or mutation authority.

## LAW WP14-36 — LOCAL RECONSTRUCTION, CURRENT REPAIR PUBLICATION AND AUDIT PUBLICATION ARE NOT ONE DISTRIBUTED TRANSACTION

These have distinct native atomicity/currentness boundaries.

Partial/indeterminate outcomes must be reported honestly. Audit publication cannot define whether gameplay authority moved; a successful gameplay repair cannot be rolled back merely because a later audit write failed.

If audit publication is retried, stable maintenance operation identity must prevent duplicate semantic audit meaning. Exact wire/idempotency mechanics belong to implementation planning/TDD.

---

# 11. Diagnostic and disclosure boundaries

## LAW WP14-37 — SUPPORT EXPORTS ARE NOT RECOVERY EVIDENCE BY SELF-PROMOTION

Maintenance exports, copied logs, support files, chat text or other diagnostics may be used only under an owning contract that grants the exact artifact evidence meaning.

Generic export content cannot backfill missing current/historical native authority.

## LAW WP14-38 — DIAGNOSTIC EXPORT MUST RESPECT ACCESS/DISCLOSURE BOUNDARIES

Support/owner diagnostics may project only application-visible evidence permitted for that diagnostic capability. Credentials, hidden instructions, unavailable model context and chain-of-thought are not exportable recovery state.

---

# 12. Chronology and identity

## LAW WP14-39 — RECOVERY/STORAGE ORDER DOES NOT CREATE FICTIONAL CHRONOLOGY

Checkpoint timestamps/world time, event IDs, Git/source/storage/session/audit order do not decide fictional temporal relations absent the owning chronology contract.

## LAW WP14-40 — RECORD/PATH/ID IDENTITY DOES NOT GRANT AUTHORITY

Checkpoint `rev-*`, session `session-*`, maintenance audit `audit-*`, route path, index membership and repository object existence identify/locate records only. Semantic authority remains with the owning contract.

---

# 13. Implementation-facing reconciliation obligations

Later implementation/planning must reconcile at least:

1. current-authority-first deterministic recovery executor/CORE wording;
2. typed current routing/root lifecycle consumption;
3. exact source pin/currentness and bounded retry;
4. no-checkpoint healthy recovery;
5. checkpoint schema/template reduction under LAW WP14-16;
6. `last_checkpoint_id` narrow pointer schema/consumer/scaffold behavior;
7. session schema/template non-authority wording/consumer behavior;
8. surviving SQLite equivalence/adoption proof;
9. live current-source recovery integration without campaign fallback;
10. accepted execution/RNG/Continuation/temporal no-replay recovery;
11. runtime/catalog/rules interpretation closure;
12. derived index/Agenda rebuild;
13. fixed Connector capability/currentness/conflict/failure behavior;
14. checkpoint export exact-basis diagnostics;
15. historical reset retention-unavailable and maintenance-isolation behavior;
16. forward current promotion of approved historical repair, never ref rewind;
17. `runtime.maintenance_audit` machine representation/identity/route/idempotency;
18. access/disclosure/application authorization for recovery/repair/support;
19. remove stale checkpoint-at-PLAY_READY/ordinary-save assumptions;
20. WP-22 current recovery/historical maintenance/adversarial failure coverage.

WP-16 retains final live physical machine ownership; WP-19/WP-20 retain bootstrap/migration integration; WP-15 is not started.

---

# 14. Candidate gate

```text
CANDIDATE_DIRECTION_CONFORMS_TO_STEP_2: YES
SR14_01_03_CONSUMED:                  YES
UPSTREAM_REOPEN_REQUIRED:             NO
HUMAN_DECISION_REQUIRED:              NO
READY_FOR_STEP_6_ADVERSARIAL_REVIEW:  YES
```

No runtime/schema/template/catalog/test implementation is changed by this candidate.