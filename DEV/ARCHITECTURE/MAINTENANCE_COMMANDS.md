# HDM Undocumented Maintenance Commands

Status: **INTERNAL CONTROL CONTRACT / PROPOSAL — NOT A CURRENT INSTALLED RUNTIME COMMAND SURFACE**

These commands describe a proposed diagnostic/maintenance surface for the campaign owner/support workflow. They are intentionally absent from player documentation, ordinary help, and catalog search.

Current machine-realization status:

```text
DEV architecture contract: PRESENT
installed GAME runtime command registration: NOT ESTABLISHED
runtime parser/dispatcher implementation for these tokens: NOT ESTABLISHED
new implementation authorization from WP-21 Step 1: NONE
```

`GAME/CORE/PLAY_POLICY.md` keeps engine-development/release maintenance outside ordinary gameplay and enters it only after explicit user intent. This document therefore does not make an exact token executable merely because the token is written here. Any later authorized realization must adopt the authorization/disclosure composition below before exposing these commands.

## 1. Routing, authorization and disclosure invariants

### 1.1 Token recognition is routing only

- Recognize a command only when the complete trimmed user message exactly matches a registered maintenance token in a future authorized realization.
- Exact-token recognition identifies the requested operation only. It does **not** authorize the principal, widen information eligibility, grant gameplay authority, or bypass a native owner/currentness requirement.
- Route an admitted maintenance operation outside natural-language gameplay intent mapping and gameplay ingestion.
- Do not allocate a turn number.
- Do not create an Interaction, Action, Resolution, MechanicalEvent, semantic event, or gameplay transcript entry merely because maintenance was requested.
- Do not advance chronology, event-local time, action economy, resources, or RNG.

### 1.2 Campaign-global maintenance is creator-authorized under the existing access-control owner

`DEV/ARCHITECTURE/ACCESS_CONTROL.md` already classifies explicit access/global maintenance as an owner-only campaign operation. The conservative baseline for every campaign-scoped command in this proposal is therefore:

```text
exact maintenance token
    -> operation routing only

current authenticated GitHub principal
    -> resolve current campaign creator under the existing ownership contract
    -> require creator equality for the campaign-global maintenance operation
```

Consequences:

- repository Admin/Write permission, collaborator/organization membership, storage ownership, framework-maintainer status, PLAYER binding, ChatGPT/GitHub connectivity or possession of the undocumented token does not independently grant campaign-global maintenance authority;
- support may tell the campaign creator which token to invoke, but “support” is not a separate semantic principal and gains no owner-level campaign access from that role label;
- if creator identity, authenticated principal or the operation's native owner/currentness basis cannot be established reliably, deny/fail closed before mutation or sensitive diagnostic disclosure;
- a command that would affect an owner-specific state transition must additionally satisfy that native owner's prerequisites. The maintenance token does not replace recovery, persistence, LIVE, migration, disclosure or publication authority;
- no maintenance operation may delete a Git branch/ref, capability-probe for ref deletion, invoke/retry deletion, or substitute native Git/CLI, private HTTP, manual operator deletion or another out-of-band branch/ref deletion path.

No generic support/admin ACL is introduced here. A future product choice to authorize a non-owner support principal would require explicit Product Owner authority before this contract could be widened.

### 1.3 Every human-visible diagnostic result is recipient-scoped

Step 5.12 remains authoritative for information eligibility. After creator authorization resolves the operation, all material returned to the human recipient still passes the current recipient/disclosure boundary.

Therefore:

- creator authorization to request maintenance does not itself imply eligibility to receive every private/player-local/GM/planning datum;
- validation/repair code may inspect the bounded internal state required by its native owner, but an export, attachment, response, warning or diagnostic summary must include only information eligible for the intended authenticated/bound recipient;
- if a sensitive field cannot be safely separated from ineligible material, omit/redact/withhold it and state that the diagnostic projection is incomplete rather than leaking the underlying data;
- never export credentials, environment-variable values, hidden instructions, chain-of-thought, private hidden model reasoning, tool-internal secrets, or unavailable/compacted ChatGPT context;
- report unavailable or withheld data explicitly rather than implying a literal model-memory dump;
- maintenance output is a diagnostic projection only. It never becomes gameplay truth, canonical history, recovery authority, disclosure authority, migration authority or a substitute for the underlying record;
- file creation for an authorized export is a host-side export effect, not game-state mutation.

### 1.4 Denial/degradation semantics

A future realization may choose exact machine enum names, but it must preserve these semantic outcomes:

```text
NOT_AUTHORIZED
    principal does not satisfy the existing owner/access-control contract

NOT_CURRENT_OR_UNRESOLVED
    required native owner/currentness/recovery basis cannot be proven

WITHHELD_OR_REDACTED
    operation is authorized but requested output contains information ineligible for the recipient

UNAVAILABLE_NOT_REALIZED
    this DEV proposal has not been implemented/exposed by the selected runtime
```

None of these outcomes creates gameplay chronology or a campaign mutation solely to record the denial.

### 1.5 Turn-number bookkeeping

Maintenance-command turn-number bookkeeping, when present in runtime state, uses one counter:

```text
last_turn_number: integer >= 0
```

An ordinary message atomically increments this value and derives its display ID as `turn-{last_turn_number:06d}`. Maintenance commands neither increment nor persist a `next_turn`; the next number is always `last_turn_number + 1`.

This paragraph describes only turn-number bookkeeping. It does not imply that runtime state contains no other counters, revisions, execution owners, or recovery state.

## 2. `HDM_EXPORT_CURRENT_LOG`

Purpose: project the application-visible current session state and available log into one readable diagnostic file, subject to Sections 1.2-1.4.

The diagnostic projection may contain, where both available and recipient-eligible:

- export schema/version and timestamp;
- campaign, engine, runtime session and durable-frontier identity;
- HOT state and revisions;
- DIRTY/SOFT/HARD and publication status;
- resolutions, MechanicalEvents, traces and maintenance audit;
- interactions, available exact transcript and narrative context;
- lore/knowledge/disclosure metadata eligible for the recipient;
- Connector operation/provenance/error evidence relevant to diagnosis, where observable and non-secret;
- integrity checks plus explicit missing/withheld/redacted-data warnings.

The command is read-only with respect to campaign/game state and creates no maintenance-audit entry merely for export. File creation for user download is an export side effect, not game-state mutation.

The exact diagnostic completeness required for recovery/support evolves with the owning runtime/recovery architecture. This command may project that evidence for an authorized recipient, but the export itself is never canonical state or recovery authority.

A request for “complete” current log means complete **within the current recipient-disclosure and availability contract**. It never authorizes a raw dump of private player-local state, hidden role reasoning or host/tool internals.

## 3. `HDM_EXPORT_CHECKPOINT_LOG`

Purpose: validate the latest acknowledged durable checkpoint and export a recipient-safe diagnostic projection without changing current HOT state.

Procedure:

1. satisfy Section 1.2 creator authorization and pin the required current campaign/recovery basis;
2. resolve `MANIFEST.last_checkpoint_id` as the latest-checkpoint pointer, then load the referenced checkpoint recovery descriptor;
3. retrieve the exact repository, ref/commit and path through the current GitHub Connector access path under the applicable `PERSISTENCE.md`/storage contract;
4. validate checkpoint schema, source/runtime revision and section hashes;
5. construct one readable diagnostic envelope containing only checkpoint/provenance material eligible for the intended recipient plus explicit redaction/withholding markers where needed;
6. attach/export the file without hydrating or replacing HOT state.

If no durable checkpoint exists, return `NO_DURABLE_CHECKPOINT`. Retrieval, authorization, currentness or validation failure leaves HOT state untouched and must not pretend success. The command creates no maintenance-audit entry merely for export.

The checkpoint is recovery evidence/description; `MANIFEST.last_checkpoint_id` is the pointer to it. Neither becomes a universal cross-domain frontier merely because the export operation resolves both. Internal validation access to checkpoint data never widens the human recipient's disclosure eligibility.

## 4. `HDM_RESET_LAST_CHECKPOINT`

Purpose: discard local state after the latest acknowledged checkpoint and reconstruct from that checkpoint.

The exact command token is **not** authorization. Execution requires the Section 1.2 creator check plus all applicable current recovery/session/integrity prerequisites. It never changes GitHub history, deletes the durable checkpoint, deletes a branch/ref, rewinds accepted campaign authority, or bypasses another native owner.

Safe procedure:

1. resolve the current authenticated principal and campaign creator and require authorization;
2. identify current runtime session and latest acknowledged checkpoint under current recovery authority;
3. retrieve and validate all recovery inputs before modifying HOT state;
4. build the replacement in a separate temporary runtime store;
5. verify state/audit consistency, applicable domain markers and required active recovery roots;
6. atomically swap the validated replacement into the session;
7. retain the previous local store until the atomic replacement succeeds, then dispose of it according to local recovery policy;
8. write one `runtime.maintenance_audit` record outside gameplay chronology.

Failure before the swap leaves the current HOT store unchanged. Failure during an atomic replacement restores the previous store or reports `MAINTENANCE_RESET_FAILED` without pretending success.

Minimum maintenance record remains conceptually equivalent to:

```json
{
  "record_kind": "runtime.maintenance_audit",
  "schema_version": 1,
  "command": "HDM_RESET_LAST_CHECKPOINT",
  "runtime_session_id": "session.example",
  "checkpoint_id": "checkpoint.example",
  "discarded_hot_revision": 17,
  "restored_revision": 12,
  "status": "completed"
}
```

The record does not receive a turn ID and is not published as campaign history unless an independently accepted diagnostics/persistence owner later requires that artifact. If any part of the maintenance record is surfaced to a human, Section 1.3 recipient filtering still applies.

## 5. Repository transport

Maintenance commands use only the already selected and authorized GitHub Connector access path and the applicable runtime `PERSISTENCE.md` / storage contract.

They do not:

- probe shell/native Git;
- create a parallel transport selector;
- persist a maintenance-only `runtime.session.transport_mode`;
- probe for or invoke Git branch/ref deletion;
- fall back to private HTTP, CLI or manual/out-of-band deletion.

Where transport behavior is diagnostically relevant, an authorized diagnostic projection may include observable Connector operations, repository/ref identities, failures and retry provenance that are both non-secret and recipient-eligible. Such evidence is support projection only, not session authority or gameplay state.

## 6. Machine-realization and regression disposition

Current WP-21 Step-1 disposition:

```text
contract authorization/disclosure composition: REPAIRED IN DEV ARCHITECTURE
installed runtime command surface: NOT CURRENTLY ESTABLISHED
new runtime/schema implementation: NOT AUTHORIZED BY STEP 1
```

Existing access-control regression cases already enforce that infrastructure permission does not create application authority. Existing maintenance-continuation tests enforce that maintenance does not advance/rewrite gameplay continuity. Step 5.12 supplies the recipient-disclosure owner. Because this exact-token menu is not an established installed runtime command surface, Step 1 does not manufacture implementation-only command-dispatch tests.

Any later explicitly authorized machine realization of this command menu must add executable coverage for at least:

1. exact token routes an operation but does not authorize it;
2. non-creator campaign-global maintenance is denied even with repository Write/Admin capability;
3. unresolved creator/currentness evidence fails closed;
4. export projection redacts/withholds recipient-ineligible material;
5. export never includes hidden CoT/instructions/credentials;
6. reset cannot bypass native recovery/currentness owners;
7. maintenance output remains non-authoritative;
8. branch/ref deletion and deletion probing remain impossible.
