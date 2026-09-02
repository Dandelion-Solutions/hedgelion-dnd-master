# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step 3 Decision Brief

Status: **STEP 3 COMPLETE — SYNTHESIS DECISION READY FOR CANDIDATE DEVELOPMENT**

Date: 2026-09-03

Evidence basis:

- repaired Step-1 Task Brief / Source Manifest / SR14-01..03 recovery;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest-step-2-expansion.md`.

---

## 1. Decision statement

WP-14 selects:

> **PINNED CURRENT-SOURCE RRC RECOVERY + OPTIONAL CHECKPOINT ASSISTANCE + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE**

This is not a new gameplay owner. It is the implementation-facing composition of already accepted Step-5.2/5.4/5.7/5.8, R2.6 and WP-10..WP-13 contracts.

Two operation classes are explicit:

1. **ordinary current recovery** — reconstruct a validated current Resumable Runtime Closure from current native authorities;
2. **explicit historical maintenance** — deliberately inspect/reconstruct an older evidence composition when retained dependencies permit it, without treating that composition as current authority until any separately authorized replacement is established by normal forward publication.

Checkpoint supports both only as descriptor/evidence. It owns neither current state nor historical native state.

No human product decision is required because accepted Step-5.7 laws already distinguish current recovery from historical maintenance and reject guaranteed rewind as a default checkpoint promise.

---

## 2. Selected machine shape

### 2.1 Ordinary current recovery attempt

Conceptual ephemeral operation:

```text
campaign selection
-> fixed-Connector exact campaign anchor H
-> bounded campaign identity/runtime/routing read
-> resolve current native owning routes
-> exact-pin each mutable participating source
-> enumerate typed independent RRC roots
-> hydrate root owners + correctness-required dependencies
-> preserve accepted execution/RNG/Continuation/temporal identities
-> optional checkpoint assistance only
-> rebuild derived indexes/Agenda/caches/context
-> validate interpretation + access + integrity + per-source currentness + RRC
-> READY | RETRY | BLOCKED
```

No persisted generic RecoveryCut/recovery journal/result record is required.

`READY` is an operation result, not a lease. Later writes still require their owning currentness/CAS/application-authorization rules.

### 2.2 Current source selection

Campaign H is a discovery anchor only.

For every required scope:

```text
current route
-> native source identity
-> exact current revision for this attempt
```

If current routing selects live authority, recovery exact-pins that live source. Campaign base is never silent fallback for the claimed scope.

Legitimate movement produces bounded `RETRY`; missing/incompatible/contradictory required basis produces typed scope-aware `BLOCKED`/integrity disposition.

### 2.3 Root/dependency closure

Recovery enumerates only current independent roots admitted by current owners/routing/lifecycle, including as applicable:

- non-settled RuntimeCommand;
- active Procedure;
- unresolved conditionally promised Interaction/IntentPlan;
- armed independently-due temporal source owner;
- future explicitly admitted independent root classes.

Transitive correctness dependencies are loaded under exact pinned source revisions. Multiple discovery paths deduplicate by stable semantic identity.

Accepted execution is resumed, never replayed merely because local/chat/process state was lost:

- stable Resolution/Procedure/Continuation identity;
- fixed accepted RNG evidence;
- mandatory child/firing identity;
- accepted Choice/Reaction generation/offer;
- accepted invocation/catalog/rules interpretation context.

### 2.4 Optional checkpoint assistance

Checkpoint may be skipped entirely during healthy current recovery.

If read:

- descriptor identity/campaign/schema/access is validated;
- positive source/root observations are hints only and validated against current native owners;
- omissions never prove absence;
- stale observations never choose current source;
- defects remain checkpoint-facility scoped unless the requested operation depends on them.

No checkpoint field becomes cross-domain completeness/currentness authority.

### 2.5 Session and ambient host context

`runtime.session`, cached HEAD/status/timestamps/notes, chat history, Project memory and model context may assist navigation/diagnostics/observability where allowed.

They do not select current campaign/live/native authority, reconstruct lost canon, prove handoff/save, or allow replay.

### 2.6 SQLite reuse

A surviving WP-12 SQLite database is reusable only after its relevant bytes/helpers are proven equal to or deterministically derivable from the selected compatible native current sources/evidence.

Local freshness/generation/mtime does not promote unpublished state.

### 2.7 Derived state

Indexes, Agenda, query/cache/context structures and other rebuildable projections reconstruct deterministically after native hydration. Index absence is not semantic absence.

### 2.8 Fixed runtime repository transport

Every remote recovery/currentness/publication read/write operation uses the supported gameplay path:

```text
deterministic Python/core
-> GitHub Connector
-> exact refs/Git-data evidence / non-force ref transition where writing
```

No runtime probing/fallback through `gh`, native remote Git, private HTTP/API/token workarounds, alternate App/MCP/backend, GitHub Actions or equivalent path.

Missing required Connector capability yields typed supported-profile capability failure/blocked operation; it does not activate an alternate transport selector.

---

## 3. Checkpoint wire-role decision

WP-14 does not freeze final YAML shape, but it fixes implementation-facing semantic disposition.

### Retain equivalent identity/association

A checkpoint descriptor minimally needs stable typed identity and campaign association plus individually justified immutable evidence/provenance fields.

### Retire generic authority-like fields

- generic `valid_through_event_id` completeness/frontier semantics;
- self-referential containing-commit `expected_commit_sha`.

### Optional/non-authoritative if retained

- created time;
- copied world-time observation;
- active PC/thread/scene observations;
- engine/runtime provenance;
- recovery notes;
- layout hint.

No replacement root/source completeness array is required by WP-14.

---

## 4. `MANIFEST.last_checkpoint_id`

Retain only as nullable campaign-domain pointer to the most recently selected/published checkpoint descriptor.

It is not:

- current gameplay frontier;
- cross-domain source composition;
- RRC proof;
- root-membership proof;
- SAVE proof;
- handoff proof;
- startup requirement;
- guaranteed rewind slot.

When checkpoint K is created and selected, K plus pointer update publish in the same campaign transaction. A prepared/unreachable checkpoint object is not selected evidence.

A dangling/malformed pointer is a checkpoint-facility integrity problem; unrelated current gameplay may still recover if native RRC proves independently.

`null` remains a valid healthy scaffold/runtime value.

---

## 5. Session record decision

Keep `runtime.session` as a narrow coordination/navigation/audit/observability record family.

Final field retention remains machine detail, but semantics are fixed:

- `base_head_sha` / `last_published_head_sha`: cached observations/evidence only;
- `status`: coordination hint, not host-liveness lease/write fence;
- `notes`: diagnostics only, not recovery payload;
- player/PC/scene references: context associations only, no authorization grant;
- timestamps: observability only, no chronology/currentness authority.

Ordinary cold recovery must not require a session record.

---

## 6. `HDM_EXPORT_CHECKPOINT_LOG`

Selected direction: retain as a **read-only checkpoint-facility diagnostic operation**, subject to later implementation verification.

Conceptual contract:

1. resolve `MANIFEST.last_checkpoint_id` from exact pinned campaign authority;
2. if null -> typed `NO_DURABLE_CHECKPOINT`/equivalent facility result;
3. resolve immutable descriptor through current authorized fixed Connector read path;
4. validate checkpoint format/campaign association and individually retained provenance/evidence;
5. export a diagnostic envelope with explicit validation/missing-data status;
6. do not hydrate/replace HOT or move current authority;
7. do not create gameplay events/turns or convert export into canon/recovery authority.

A dangling/malformed pointer produces typed checkpoint-facility diagnostic failure, not silent current-state fallback.

---

## 7. `HDM_RESET_LAST_CHECKPOINT`

Selected direction: **repair current proposal semantics; preserve only as explicit historical maintenance, not ordinary recovery rollback.**

Conceptual contract:

1. exact command is explicit maintenance authorization to attempt a scoped destructive local historical reconstruction; it is not proof of application write authority for durable current state;
2. resolve `last_checkpoint_id` from exact pinned campaign authority;
3. resolve the selected immutable checkpoint descriptor;
4. derive the exact required historical native source/revision/interpretation dependency set from owner-valid evidence; descriptor fields are locator/provenance evidence, not copied state authority;
5. resolve and validate every required historical dependency before replacing local HOT;
6. if any required dependency is unavailable/incompatible, return typed maintenance-unavailable/blocked result and leave local/current durable state unchanged;
7. build the historical local runtime store separately, preserving accepted IDs/RNG/execution/chronology evidence and rebuilding only derived projections;
8. validate reconstructed historical RRC/integrity for the maintenance scope;
9. atomically replace only the local runtime store when the requested local maintenance operation is valid, retaining the old store until replacement succeeds;
10. local historical reconstruction **does not itself move current campaign/live durable authority**;
11. if a separately application-authorized repair intends the reconstructed state to become new current durable state, perform owner-native forward publication/currentness/CAS/durability under the normal WP-13/R2.6 path; never force-push/ref-rewind;
12. write a narrow `runtime.maintenance_audit` record for the maintenance operation/outcome; the audit is not gameplay history/currentness/authority.

No guaranteed rewind window is promised. Retention loss is truthful typed unavailability.

This interpretation preserves the accepted command surface without granting checkpoint authority that Step 5.7 explicitly rejects.

---

## 8. `runtime.maintenance_audit`

Semantic role:

- narrow campaign-scoped support/diagnostic audit record;
- identity follows current `audit-*` campaign-scoped policy;
- physical route follows WP-11 `STATE/RUNTIME/MAINTENANCE_AUDITS` with no semantic index requirement;
- records requested operation, relevant evidence/provenance, scope and outcome at implementation-defined precision;
- receives no gameplay turn/Interaction/Resolution/fictional chronology authority;
- cannot make a failed/unavailable repair successful;
- does not become a recovery journal or currentness frontier.

Final wire schema is later machine-realization work; absence of current dedicated schema does not create an architecture trade-off.

---

## 9. Repair decision

Repair is explicit, bounded and evidence-gated.

Baseline dispositions:

```text
legitimate source/routing movement
    -> RETRY / repin / reselect

required pinned basis missing/incompatible
    -> BLOCKED affected dependency scope
    -> integrity classification as evidence warrants

optional checkpoint facility defect, current RRC healthy
    -> checkpoint facility suspect/blocked as applicable
    -> independent gameplay recovery may READY

historical maintenance requested, retained composition unavailable
    -> typed maintenance unavailability
    -> no invented reconstruction / no fallback
```

Any mutating durable repair additionally requires application authorization and normal owning currentness/publication/durability rules. Technical Connector write capability is insufficient.

---

## 10. Alternatives rejected

### Alternative B — checkpoint-centered cold recovery / last-checkpoint rollback

Rejected because it contradicts Step-5.2/5.7 current-authority-first semantics, fails partial multi-domain durability, can overwrite selected live authority and turns optional evidence into a second state owner.

### Alternative C — durable RecoveryCut / recovery journal / global source manifest

Rejected because it introduces a new cross-domain authority/frontier owner, duplicates native currentness and recreates the global serialization object explicitly rejected upstream.

### Alternative D — session/SQLite/ambient-host warm state as fallback authority

Rejected because session, local cache and host memory are observations/acceleration only and may contain stale or unpublished data.

### Alternative E — guaranteed N-checkpoint rewind as an implicit current promise

Rejected because Step-5.7 explicitly leaves guaranteed historical retention/rewind as a future product policy requiring separate owner approval, retention/history/disclosure semantics and implementation cost acceptance.

---

## 11. Boundary with downstream work

WP-14 canonical result may require later implementation changes to:

- recovery executor/CORE prose;
- checkpoint/session/MANIFEST schemas/templates;
- maintenance support command semantics;
- maintenance-audit machine representation;
- bootstrap/scaffold/tests;
- current-state/checkpoint-related stale fields;
- WP-22 conformance/failure injection.

This architecture pass does not implement those changes.

WP-16 still owns final live physical currentness/CAS/close/absorption machine. WP-19/WP-20 own later bootstrap/migration integration. WP-15 is not started.

---

## 12. Decision gate

```text
SELECTED_DIRECTION:
  PINNED CURRENT-SOURCE RRC RECOVERY
  + OPTIONAL CHECKPOINT ASSISTANCE
  + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE

UPSTREAM_CONTRADICTION:          NO
NEW_UNSATISFIED_CONSUMER:        NO
MATERIAL_UPSTREAM_INSUFFICIENCY: NO
UPSTREAM_REOPEN_REQUIRED:        NO
HUMAN_DECISION_REQUIRED:         NO
STEP_4_ALLOWED:                  YES
```

No product semantic choice remains for human resolution at this stage.