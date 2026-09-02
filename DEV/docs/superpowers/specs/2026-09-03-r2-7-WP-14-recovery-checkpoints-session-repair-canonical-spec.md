# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Canonical Specification

Status: **CANONICAL WP-14 RESULT — STEPS 1-8 + SR14-04 RECOVERY COMPLETE / MANDATORY FINAL SENIOR RE-AUDIT PENDING**

Date: 2026-09-03

Canonical direction:

> **PINNED CURRENT-SOURCE RRC RECOVERY + OPTIONAL CHECKPOINT ASSISTANCE + SEPARATE EVIDENCE-GATED HISTORICAL MAINTENANCE**

Canonicalization basis:

- repaired Step-1 Task Brief / Source Manifest / critic;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-senior-recovery-source-graph-omissions.md` (`SR14-01..SR14-03`);
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-2-evidence-extraction.md`;
- Step-2 / Step-6 Source Manifest expansions;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-4-collaborative-review.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-5-candidate-spec.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-7-resolution-gate.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-post-step-8-senior-recovery-checkpoint-field-disposition.md` (`SR14-04`).

This file is the final WP-14 implementation-facing architecture source of truth, subject to mandatory final Senior re-audit. Earlier Step-5 wording is derivation where it differs from this canonical result. Historical Step-6 F01-F08 remain unchanged; SR14-04 is a separate post-Step-8 canonical-completeness recovery.

---

# 1. Scope and ownership

WP-14 realizes accepted recovery/checkpoint/session/repair semantics over the existing Step-3/Step-5, R2.6 and WP-10..WP-13 owner graph.

It does not introduce a new gameplay authority, recovery frontier, checkpoint owner, session lease, repair journal, alternate repository transport, generic rollback authority or distributed transaction.

Conceptual recovery/maintenance operation objects are ephemeral unless an already accepted durable family explicitly owns a record.

---

# 2. Ordinary current recovery

## LAW WP14-1 — Ordinary recovery targets current native authority

Ordinary cold recovery reconstructs a compatible current Resumable Runtime Closure from the actual current native durable authorities selected by current owning routes.

Checkpoint, session, SQLite, ambient chat/model context, support exports, Story, maintenance reconstruction and repair evidence are not alternate current-state owners.

## LAW WP14-2 — Campaign revision is a discovery anchor, not complete current state

After campaign selection, recovery exact-pins the selected campaign ref to campaign revision H through the supported gameplay Connector path.

H supplies bounded campaign identity/layout/runtime/current-routing evidence. It is not a universal cross-domain frontier and cannot substitute for scopes currently owned elsewhere.

## LAW WP14-3 — Current routes select native sources

For each required mutable scope:

```text
current owning route
-> native source identity/ref
-> exact current revision for this attempt
```

No source is selected by checkpoint pointer, checkpoint age, session HEAD, commit timestamp, lexicographic ref order, local database freshness, maintenance export or ambient memory.

## LAW WP14-4 — Live-owned current truth never falls back to campaign state

When current routing selects a live-owned source, recovery exact-pins that selected live source under Step-5.8 currentness semantics.

ACTIVE and CLOSED_UNABSORBED/current-live states remain current truth for their claimed scope until lawful authority movement/absorption. Missing, incompatible or moving selected live authority yields owning `RETRY`/`BLOCKED` semantics, never silent campaign fallback.

## LAW WP14-5 — One attempt uses one exact pin per participating mutable source

A recovery attempt keeps an ephemeral exact source basis sufficient to validate that attempt. It does not persist a generic RecoveryCut/frontier/source manifest.

Mixed branch-relative revisions are invalid.

## LAW WP14-6 — Independent root discovery is typed and bounded

Recovery enumerates current independent roots from native routing/lifecycle evidence, including as applicable:

- non-settled RuntimeCommand;
- active Procedure;
- unresolved conditionally promised Interaction/IntentPlan;
- armed independently-due temporal source owner;
- future explicitly admitted independent root classes.

Known-ID reads use WP-11 exact derived routes. Ordinary recovery does not require campaign-wide scans, full WORLD traversal, full LOG/history, all checkpoints, all runtime records or broad Git history.

## LAW WP14-7 — Transitive hydration is correctness-required only

From admitted roots, recovery loads only native dependencies/references/evidence required to prove honest continuation under the pinned basis.

Multiple discovery paths deduplicate by stable semantic identity.

## LAW WP14-8 — Accepted execution resumes; recovery never replays it

Recovery preserves, as applicable:

- RuntimeCommand/Procedure/Resolution identity and lifecycle;
- fixed accepted RNG evidence;
- accepted invocation/catalog/rules/dependency interpretation;
- Continuation generation/offer and fixed pending response evidence;
- mandatory child/firing identities;
- accepted Choice/Reaction and causal receipts/evidence.

Process/chat/SQLite loss, publication uncertainty, source movement, checkpoint mismatch or repair attempt SHALL NOT reroll RNG, allocate replacement accepted IDs, regenerate accepted choices or replay settled semantic actions.

## LAW WP14-9 — Temporal recovery remains native-owner based

Armed temporal obligations are enrolled from native temporal owners. Once an occurrence crossed into accepted execution, stable accepted firing/execution identity suppresses duplicate rematerialization from a rebuilt Agenda.

Agenda remains derived and rebuildable; no generic pending/job queue becomes authority.

## LAW WP14-10 — Interpretation closure is required

Still-significant accepted work must recover compatible accepted runtime/catalog/rules/invocation/dependency context. Ambient current runtime or model memory cannot silently reinterpret historical accepted work.

Exact retained wording/evidence remains a recovery dependency only where its owning contract still makes it irreducible.

## LAW WP14-11 — Ambient host context has no recovery authority

Chat history, Project memory, model context and hidden reasoning cannot establish campaign canon/currentness, recover lost unpublished state, select sources or supply missing historical dependencies merely because material is physically present.

---

# 3. Local HOT / SQLite / derived state

## LAW WP14-12 — Surviving SQLite is conditional cache/acceleration only

A surviving WP-12 database may be reused only after proving the relevant bytes/helpers equal or are deterministically derivable from the selected compatible native source/evidence basis for the operation.

Local mtime, generation or apparent freshness cannot resurrect unpublished state or missing authority.

## LAW WP14-13 — Derived state rebuilds from validated native state

Agenda, query/index/cache/context structures and other rebuildable projections reconstruct after native hydration.

Index absence is not semantic absence. Broken/missing derivative state does not authorize broad semantic fallback when the native exact route is known.

---

# 4. Checkpoint role and pointer semantics

## LAW WP14-14 — Checkpoint is optional immutable descriptor/evidence

Checkpoint may support diagnostics/export, migration/repair evidence, complex suspension/handoff landmarks, explicit historical maintenance when retained dependencies permit it, or future measured bounded acceleration.

It is not current gameplay authority, root registry, SAVE/handoff proof, session lease, mandatory startup anchor or universal frontier.

Healthy ordinary recovery may read zero checkpoints.

## LAW WP14-15 — Checkpoint hints are positive, non-exhaustive and current-validated

Checkpoint observations affecting ordinary recovery are hints only:

- positive hints require current native owner/routing validation;
- omission never proves absence;
- stale observations never select older current authority;
- malformed/dangling optional checkpoint metadata is facility-scoped unless the requested operation depends on it.

## LAW WP14-16 — Every current checkpoint field has one explicit non-duplicating disposition

The current `GAME/SCHEMA/checkpoint.schema.yaml` and `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` SHALL be reconciled field-by-field against the following binding roles. These roles constrain later schema/template implementation; they do not require all optional current fields to survive.

Role vocabulary:

```text
REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION
OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT
RETIRED
SCHEMA_FORMAT_METADATA_ONLY
```

| Current schema field | Current template | Binding role | Canonical disposition / authority boundary |
|---|---|---|---|
| `schema_version` | `schema_version: 2` | `SCHEMA_FORMAT_METADATA_ONLY` | Equivalent checkpoint wire/format version identity only. It has no recovery/currentness/chronology authority. |
| `id` | `id: null` | `REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION` | Stable immutable checkpoint descriptor identity. Identity alone grants no gameplay/currentness authority. |
| `campaign_id` | `campaign_id: null` | `REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION` | Campaign association and descriptor validation only; not a source selector or recovery frontier. |
| `created_at` | `created_at: null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic/provenance timestamp only. Never chronology, freshness, currentness or latest-selection authority. |
| `valid_through_event_id` | `null` | `RETIRED` | Retired as generic checkpoint recovery-completeness/frontier semantics. Event-ID position cannot replace current native routing/currentness. |
| `expected_commit_sha` | `null` | `RETIRED` | Retired. A checkpoint in content-addressed Git cannot depend on embedding its own containing-commit identity. Use external/non-self-referential revision context when provenance is needed. |
| `world_time` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Not part of the minimum checkpoint contract. If retained later, it is domain-typed diagnostic/presentation observation only; never chronology, due/not-due or currentness authority. |
| `state` container | present | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Structural grouping of non-authoritative layout/root observations only. It is not a checkpoint-owned state snapshot or authority object. |
| `state.current_state_path` | `STATE/CURRENT.yaml` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Non-authoritative layout hint only if actual layout indirection needs it. **It is not a checkpoint-owned current-state selector, recovery frontier, root-completeness evidence, currentness authority, SAVE/handoff proof or fallback source.** Current native routing/owners select current state. |
| `state.active_pc_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if measured/proven useful. Omission never proves absence or root completeness. |
| `state.active_thread_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if measured/proven useful. Omission never proves absence or root completeness. |
| `state.active_scene_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if measured/proven useful. Omission never proves absence or root completeness. |
| `recovery_notes` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic/support notes only. They cannot supply missing native authority, accepted interpretation, exact evidence or hidden recovery state. |
| `engine` container | present | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional runtime provenance observation only. **Checkpoint engine projection is not current runtime authority and does not replace accepted interpretation dependencies of open execution.** |
| `engine.version` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Runtime-version provenance observation only; current campaign/runtime owner and open-work interpretation contracts govern actual compatibility. |
| `engine.package_id` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Package-identity provenance observation only; not runtime-selection/currentness authority. |
| `engine.source_commit_sha` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional source provenance observation only; not current campaign/ref/runtime authority. |
| `engine.package_sha256` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional package provenance/integrity observation only; cannot select current runtime or reinterpret accepted work. |
| `engine.adopted_at` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic adoption-time observation only; no ordering/currentness/chronology semantics. |
| `ruleset` container | absent from current template | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Schema-admitted non-authoritative ruleset provenance projection. Current template omission is implementation/template-alignment debt, not authority evidence. |
| `ruleset.ruleset_set_sha256` | absent from current template | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional ruleset-set provenance/integrity observation only. **It is not current ruleset authority, does not select a replacement ruleset set, and does not replace accepted rules/catalog/invocation interpretation dependencies of open execution.** |
| `schema_data_version` | `schema_data_version: 2` | `SCHEMA_FORMAT_METADATA_ONLY` | Retain only if checkpoint format/migration ownership needs it. It has no gameplay/recovery/currentness semantics. |

The current template materializes every schema member above except the optional schema-admitted `ruleset` container / `ruleset.ruleset_set_sha256`. That mismatch is later machine/template-alignment debt only. It does not imply that the field must be retained in the replacement schema.

No checkpoint field or container may become a RecoveryCut, current-state owner, source/root completeness manifest, universal frontier, session lease, SAVE proof or handoff proof by serialization alone.

This law does **not** introduce any new checkpoint source/root completeness manifest, RecoveryCut, frontier field or replacement selector. New completeness/root/source fields remain forbidden by default absent separate proven bounded value and preserved owner semantics.

## LAW WP14-17 — `MANIFEST.last_checkpoint_id` is only a nullable campaign-domain descriptor pointer

The pointer means only the most recently selected/published checkpoint descriptor in the campaign domain.

It is not gameplay frontier, cross-domain composition, RRC proof, SAVE/handoff proof, root completeness, startup requirement or guaranteed rewind slot.

`null` is a valid healthy campaign/scaffold value.

## LAW WP14-18 — Checkpoint selection publication is campaign metadata publication

When checkpoint K is created and selected together, K and `last_checkpoint_id = K` publish in one normal campaign tree/commit/ref transaction under WP-13/Step-5.6 currentness.

No pointer-only freshness heartbeat is justified. Prepared/unreachable K is not selected evidence.

## LAW WP14-19 — “Last checkpoint” never means guessed newest checkpoint

For operations defined against the selected last checkpoint, `MANIFEST.last_checkpoint_id` is the sole selector.

```text
null
    -> typed NO_SELECTED_CHECKPOINT / MAINTENANCE_UNAVAILABLE

dangling or malformed selected target
    -> checkpoint-facility suspect/unavailable for the dependent operation

valid selected target
    -> resolve exactly from the pinned campaign basis
```

Directory enumeration, highest `rev-*`, ID magnitude, timestamp, Git order, nearest surviving checkpoint, session HEAD or SQLite observation SHALL NOT provide fallback “latest checkpoint” selection.

An explicitly addressed future command taking a checkpoint ID is a distinct historical-maintenance operation, not fallback semantics.

---

# 5. Session role

## LAW WP14-20 — `runtime.session` is coordination/navigation/audit/observability only

Session records may carry associations and cached observations such as player/PC/scene IDs, base/published HEAD observations, status, timestamps and notes.

They do not independently prove host liveness/death, current gameplay/live state, write authority, successful save/handoff, recovery frontier or Procedure/Resolution/fictional-scene termination.

Ordinary cold recovery does not require a session record.

---

# 6. Recovery result and final validation

## LAW WP14-21 — Ordinary recovery result is ephemeral `READY | RETRY | BLOCKED`

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

## LAW WP14-22 — `READY` requires final validation of the participating basis

Before `READY`, validate as applicable:

- campaign anchor/current route basis;
- each participating mutable current source under its native currentness contract;
- operational root-routing/lifecycle basis;
- required application read/write authorization for requested capability;
- disclosure eligibility for material that may become player-visible;
- accepted runtime/catalog/rules interpretation compatibility;
- required native references/integrity;
- complete RRC for the requested operation scope.

`READY` is not a lock or lease. Later writes still obey owner currentness/CAS/fencing/authorization.

## LAW WP14-23 — Legitimate movement is `RETRY`, not corruption

Campaign/source/route/root-lifecycle movement during recovery is normal concurrency until evidence establishes inconsistency. Recovery repins/re-resolves under bounded retry policy.

Persistent churn yields typed coordination/retry exhaustion, not infinite loop.

## LAW WP14-24 — Unsatisfied required basis is scope-aware `BLOCKED`

Missing/incompatible required current source, unavailable interpretation/runtime, repository/capability failure, authorization denial or proven integrity defect blocks the dependent requested scope/capability. Independent scopes are not automatically invalidated.

---

# 7. Fixed gameplay repository transport

## LAW WP14-25 — Recovery/maintenance uses the fixed R2.6 gameplay Connector path

Supported runtime remote operations remain:

```text
deterministic Python/core preparation/validation
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition where writing
```

No recovery/save/maintenance/live operation probes or falls back to `gh`, remote native Git, private HTTP/API/token paths, alternate App/MCP/backend transport, GitHub Actions gameplay bridge or equivalent alternatives.

## LAW WP14-26 — Missing required Connector capability is typed supported-profile failure

If the fixed runtime path lacks a required operation, return the appropriate typed blocked/capability/maintenance outcome. Do not activate a transport selector.

Exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence remains part of recovery/repair verification.

---

# 8. Repair

## LAW WP14-27 — Repair is explicit, bounded and evidence-gated

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

## LAW WP14-28 — Mutating durable repair requires application authorization and owner-native currentness

Technical repository/Connector write capability and maintenance-token recognition are insufficient for arbitrary durable gameplay mutation.

A mutating repair must satisfy current application authorization, native owner rules, currentness/CAS/conflict semantics and WP-13 durability/publication requirements.

---

# 9. Historical maintenance

## LAW WP14-29 — Historical maintenance is distinct from ordinary current recovery

Historical maintenance deliberately reconstructs/inspects an older evidence composition. It never changes the source-selection target of ordinary cold recovery.

No guaranteed rewind window exists unless a future separately approved product/retention contract creates one.

## LAW WP14-30 — Historical reconstruction requires complete provable required historical composition

For the requested maintenance scope, every required historical native source/revision/interpretation dependency must remain resolvable, compatible and attributable to owner-valid evidence.

Checkpoint descriptor is locator/provenance evidence, not automatically a complete source manifest. Omitted checkpoint hints do not prove absence. Nearest timestamps/IDs/commits and campaign fallback are not allowed guesses.

If required composition cannot be proven, historical maintenance is truthfully unavailable.

## LAW WP14-31 — Historical live-owned truth may not fall back to campaign state

If the historical maintenance scope was live-owned, the required historical live source/revision/ownership basis must be resolvable from retained owner-valid evidence. Otherwise dependent reconstruction is unavailable.

## LAW WP14-32 — Historical local reconstruction is maintenance-isolated, non-current and non-playable

A validated historical local store may be built separately and locally substituted only as an explicit maintenance state.

Until lawful current promotion succeeds, it SHALL NOT drive:

- ordinary gameplay `READY`;
- ordinary gameplay Context Assembly;
- Narrator/player-visible gameplay emission;
- Interaction/turn/Action/RuntimeCommand/Resolution/Procedure creation;
- current chronology progression;
- ordinary RNG consumption;
- current campaign-scoped ID allocation;
- current `runtime.disclosure` establishment;
- ordinary SAVE/HARD success claims;
- live authority opening/claiming.

It may feed only explicitly authorized maintenance diagnostics/validation, themselves subject to access/disclosure constraints.

## LAW WP14-33 — Current promotion starts from a fresh current basis, not historical reconstruction

If a separately authorized historical repair is intended to become new current durable state, begin a distinct promotion attempt:

1. resolve current owning routes for every affected scope;
2. exact-pin current native source revisions/currentness bases;
3. resolve current application authorization/principal/delegation as required;
4. define the explicit repair footprint;
5. transform historical evidence into owner-native replacement proposals **against the fresh current basis**;
6. freeze payload, reads/dependencies, currentness and authorization basis before remote mutation;
7. publish only through normal owner-native non-force/CAS/currentness/durability edges;
8. movement/rejection/ambiguity causes bounded re-evaluation/retry or typed conflict/blocked outcome.

Historical local state is proposal/evidence input only. Never force-push, ref-rewind or treat a stale reconstructed basis as current write authority.

## LAW WP14-34 — Multi-domain promotion is native-edge composition, never distributed rollback

Historical current promotion across multiple authority domains has no global transaction/rollback.

- confirmed accepted native transitions remain real;
- rejected/indeterminate edges follow their own ambiguity/currentness rules;
- after partial outcome, recover/compose actual current authorities;
- if compatible current RRC cannot be proven for an affected scope, that scope remains `BLOCKED` / maintenance-incomplete until lawful forward repair/reconciliation completes;
- unrelated scopes remain governed by their own dependency closure;
- accepted mechanics/RNG/IDs/execution are never replayed/rerolled to imitate atomic rollback;
- maintenance outcome reports complete/partial/blocked/indeterminate state truthfully.

---

# 10. Identity, knowledge and disclosure preservation during historical repair

## LAW WP14-35 — Historical repair cannot regress published allocation history

Historical allocator state may be inspected diagnostically, but current promotion SHALL NOT regress current `runtime.id_allocator` published-allocation/collision bookkeeping.

Every previously published campaign-scoped ID remains permanently non-reusable even if repaired current state removes the old record.

New repair/replacement/audit records allocate through the current allocator owner and normal publication/conflict rules. Reconciliation may retain or advance allocator state, never restore it below published allocation history.

## LAW WP14-36 — Historical repair does not implicitly rewind disclosure or fictional knowledge

Historical world/runtime repair does not copy older `runtime.disclosure` or `world.knowledge` state into current replacement state by default.

Prior real human exposure cannot be erased by checkpoint/world/history rollback. Current fictional knowledge changes only through its owning correction/transition semantics.

If a maintenance operation explicitly targets either domain, it must name that owner scope and satisfy its owner-specific authorization/evidence/correction contract.

---

# 11. Maintenance commands

## LAW WP14-37 — `HDM_EXPORT_CHECKPOINT_LOG` is read-only diagnostic export

The command:

1. pins campaign revision H through the fixed Connector path;
2. resolves `last_checkpoint_id` as-of H using LAW WP14-19;
3. returns typed no-selected-checkpoint when null;
4. resolves/validates the immutable descriptor under applicable access rules;
5. exports allowed diagnostic/provenance/validation evidence tied explicitly to H;
6. does not hydrate/replace HOT or move authority;
7. does not create gameplay turn/event/chronology/currentness evidence.

If current pointer later moves, output remains truthfully labelled as-of H or the command may boundedly repin/retry when its UI contract explicitly asks for current-latest semantics. It never silently claims stale evidence is current.

## LAW WP14-38 — `HDM_RESET_LAST_CHECKPOINT` is conditional historical maintenance, not generic rollback

The exact maintenance token may authorize the defined maintenance attempt subject to support/application access policy.

Required flow:

1. pin current campaign basis and resolve selected checkpoint pointer using LAW WP14-19;
2. resolve/validate immutable descriptor;
3. prove complete required historical native composition for the maintenance scope;
4. load exact historical native sources/dependencies/accepted interpretation evidence without replay/reroll;
5. on retention/compatibility gap, return typed maintenance unavailability and leave current durable state unchanged;
6. build and validate a separate historical local store;
7. atomically substitute local storage only into maintenance-isolated/non-current state while preserving previous local store until local substitution succeeds;
8. do not resume gameplay/emission from that state;
9. any current durable promotion follows LAWS WP14-33..36;
10. record operation/outcome through the narrow audit family without converting audit into authority.

The command does not promise guaranteed rewind availability.

## LAW WP14-39 — Historical readers use exact pinned basis without a durable GC lease

A maintenance/export reader that resolves checkpoint/descriptor/evidence from exact campaign revision H reads required evidence against that exact pinned basis.

Later current-tree cleanup does not retroactively invalidate the already pinned historical read. No durable reader lease is required.

If required dependencies were already semantically retired/not protected before the attempt, residual old Git bytes do not automatically become ordinary retained semantic evidence. Bounded authorized maintenance may inspect transport history only under its explicit evidence contract.

Current recovery never depends on old checkpoint retention.

---

# 12. Maintenance audit

## LAW WP14-40 — `runtime.maintenance_audit` is narrow support audit evidence

The family is campaign-scoped, uses current `audit-*` identity policy and WP-11 `STATE/RUNTIME/MAINTENANCE_AUDITS` route with no semantic index requirement.

It may record stable maintenance operation identity, command/type, scope, observed evidence/provenance and outcome at implementation-defined precision.

It is not gameplay history, chronology, currentness, recovery journal, root registry or mutation authority.

## LAW WP14-41 — Durable maintenance audit writes use current authority and current allocator

Creating/publishing a durable maintenance audit is itself a current campaign-domain mutation.

It SHALL use:

- current campaign authority;
- current `runtime.id_allocator`;
- current application authorization/currentness;
- normal WP-13 publication semantics.

Historical local allocator/state cannot supply write authority. Audit record creation plus required allocator mutation join their owner-valid local/publication closure. Retry preserves one semantic maintenance operation identity and avoids duplicate audit meaning.

## LAW WP14-42 — Reconstruction, repair publication and audit publication are separate atomicity domains

Local historical reconstruction, owner-native current repair publication and durable audit publication are not one distributed transaction.

Partial/indeterminate outcomes must be represented honestly. Audit success cannot establish gameplay repair; audit failure cannot roll back an already accepted gameplay repair.

---

# 13. Diagnostic, chronology and identity boundaries

## LAW WP14-43 — Support exports cannot self-promote into recovery authority

Maintenance exports, copied logs, support files, chat text and diagnostics may be used only under an owning contract granting the exact artifact evidence meaning.

Generic export content cannot backfill missing current/historical native authority.

## LAW WP14-44 — Diagnostics respect access/disclosure boundaries

Support/owner diagnostics may project only application-visible evidence permitted for that diagnostic capability. Credentials, hidden instructions, unavailable model context and chain-of-thought are not exportable recovery state.

## LAW WP14-45 — Recovery/storage order does not create fictional chronology

Checkpoint timestamps/world time, event IDs, Git/source/storage/session/audit order do not decide fictional temporal relations absent the owning chronology contract.

## LAW WP14-46 — Record/path/ID identity does not grant authority

Checkpoint `rev-*`, session `session-*`, audit `audit-*`, route path, index membership and repository object existence identify/locate records only. Semantic authority remains with the owning contract.

---

# 14. Cross-system consistency constraints

The final realization must preserve these owner boundaries:

- **Step 3:** accepted execution, Continuation, RNG, child/firing and idempotency identities resume rather than replay;
- **Step 4 / Step 5.12:** `world.knowledge` and `runtime.disclosure` remain independent owners; historical repair does not erase actual exposure;
- **Step 5.1:** domain markers are not global frontiers; current allocator published IDs never become reusable;
- **Step 5.2 / 5.7:** recovery targets bounded current native RRC; checkpoint remains optional evidence; every checkpoint field remains within LAW WP14-16's non-duplicating role;
- **Step 5.8:** current live owner/source exactness governs live scopes; no campaign fallback;
- **Step 5.11 / 5.13:** retained exact evidence and cleanup/GC semantics constrain historical maintenance; residual Git bytes do not automatically restore semantic retention;
- **R2.6:** shipped gameplay repository transport remains fixed Connector-only path;
- **WP-11:** exact routes/index rebuild locate native owners without promoting indexes;
- **WP-12:** surviving SQLite is reusable only after source-equivalence proof and cannot become authority;
- **WP-13:** repair publication uses current frozen owner-native attempts, no distributed transaction and truthful partial/indeterminate outcomes.

No upstream architecture is reopened by WP-14 or SR14-04.

---

# 15. Implementation-facing reconciliation obligations

Later implementation planning/TDD must reconcile at least:

1. current-authority-first deterministic recovery executor and CORE wording;
2. typed current routing/root lifecycle consumption;
3. exact source pin/currentness and bounded retry;
4. healthy recovery with no checkpoint;
5. checkpoint schema/template reduction/alignment under the exhaustive LAW WP14-16 field dispositions, without preserving optional fields by inertia or inventing new completeness fields;
6. `MANIFEST.last_checkpoint_id` narrow nullable pointer semantics and no guessed-latest fallback;
7. session schema/template non-authority wording/consumer behavior;
8. surviving SQLite equivalence/adoption proof;
9. live current-source recovery without campaign fallback;
10. accepted execution/RNG/Continuation/temporal no-replay recovery;
11. runtime/catalog/rules interpretation closure;
12. derived index/Agenda rebuild;
13. fixed Connector capability/currentness/conflict/failure behavior;
14. checkpoint export exact-basis diagnostics;
15. `HDM_RESET_LAST_CHECKPOINT` retention-unavailable, no-guessed-pointer and maintenance-isolation behavior;
16. fresh-current-basis forward promotion of approved historical repair;
17. partial multi-domain promotion/recomposition and truthful incomplete/indeterminate outcomes;
18. allocator non-regression/permanent published-ID non-reuse across repair;
19. disclosure/knowledge preservation across historical repair;
20. maintenance-isolated no-gameplay/no-emission/no-RNG/no-ID-allocation fence;
21. `runtime.maintenance_audit` machine representation/current allocator/current publication/idempotency;
22. Step-5.13 pinned historical reader and semantic-retention boundary;
23. access/disclosure/application authorization for recovery/repair/support;
24. removal of stale checkpoint-at-PLAY_READY/ordinary-save assumptions;
25. WP-22 conformance/failure coverage for all final laws, Step-7 repairs and SR14-04 checkpoint-field authority boundaries.

WP-16 retains final live physical machine ownership; WP-19/WP-20 retain bootstrap/migration integration; WP-22 owns executable conformance coverage; WP-24 owns performance measurement; WP-26 retains separately routed documentation consistency work.

No implementation work is authorized by this specification.

---

# 16. Canonical closure

WP-14 closes with this invariant:

> HDM ordinary recovery always reconstructs a validated current RRC from exact current native owners and routes; checkpoint/session/SQLite/ambient context remain subordinate evidence or acceleration only. Every checkpoint field is either narrow descriptor identity/association, optional diagnostic/provenance/hint, retired legacy semantics, or schema/format metadata; no checkpoint path, runtime/ruleset projection or list becomes currentness/root/interpretation authority. Historical checkpoint-based reconstruction is an explicitly separate maintenance operation whose availability depends on retained exact owner-valid evidence, remains isolated and non-playable until lawful current promotion, and can become current only by fresh-basis owner-native forward publication that preserves live ownership, accepted execution, allocator identity history, disclosure/knowledge owners and truthful partial outcomes.

Final historical Step-6/Step-7 state plus post-Step-8 recovery:

```text
STEP_6_BLOCKING:         3
STEP_6_SIGNIFICANT:      5
SR14-04:                 CLOSED
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
NEXT_GATE:               MANDATORY FINAL SENIOR RE-AUDIT
```