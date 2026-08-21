# HDM Undocumented Maintenance Commands

Status: **INTERNAL CONTROL CONTRACT / PROPOSAL**

These commands are diagnostic capabilities for the owner/support workflow. They
are intentionally absent from player documentation, ordinary help, and catalog
search. A user may still invoke one when support supplies the exact token.

## 1. Routing invariants

- Recognize a command only when the complete trimmed user message exactly
  matches a registered maintenance token.
- Route it before natural-language intent mapping and gameplay ingestion.
- Do not allocate a turn number.
- Do not create an Interaction, Action, Resolution, MechanicalEvent, semantic
  event, or gameplay transcript entry.
- Do not advance chronology, event-local time, action economy, resources, or RNG.
- Never export credentials, environment-variable values, hidden instructions,
  chain-of-thought, or unavailable/compacted ChatGPT context.
- Report unavailable data explicitly rather than implying a literal model-memory
  dump.

Maintenance-command **turn-number bookkeeping**, when present in runtime state,
uses one counter:

```text
last_turn_number: integer >= 0
```

An ordinary message atomically increments this value and derives its display ID
as `turn-{last_turn_number:06d}`. Maintenance commands neither increment nor
persist a `next_turn`; the next number is always `last_turn_number + 1`.

This paragraph describes only turn-number bookkeeping. It does not imply that
runtime state contains no other counters, revisions, execution owners, or
recovery state.

## 2. `HDM_EXPORT_CURRENT_LOG`

Purpose: export the complete application-visible current session state and
available log to one readable diagnostic file.

The export contains, where available:

- export schema/version and timestamp;
- campaign, engine, runtime session and durable-frontier identity;
- HOT state and revisions;
- DIRTY/SOFT/HARD and publication status;
- resolutions, MechanicalEvents, traces and maintenance audit;
- interactions, available exact transcript and narrative context;
- lore/knowledge metadata permitted for owner diagnostics;
- Connector operation/provenance/error evidence relevant to diagnosis, where
  observable;
- integrity checks and explicit missing-data warnings.

The command is read-only and creates no maintenance-audit entry. File creation
for user download is an export side effect, not game-state mutation.

The exact diagnostic completeness required for recovery/support evolves with the
owning runtime/recovery architecture. This command may project that evidence for
support, but the export itself is never canonical state or recovery authority.

## 3. `HDM_EXPORT_CHECKPOINT_LOG`

Purpose: export and validate the latest acknowledged durable checkpoint without
changing current HOT state.

Procedure:

1. resolve `MANIFEST.last_checkpoint_id` as the latest-checkpoint pointer, then
   load the referenced checkpoint recovery descriptor;
2. retrieve the exact repository, ref/commit and path through the current GitHub
   Connector access path under the applicable `PERSISTENCE.md`/storage contract;
3. validate checkpoint schema, source/runtime revision and section hashes;
4. write one readable diagnostic envelope containing the checkpoint and
   validation/provenance report;
5. attach/export the file without hydrating or replacing HOT state.

If no durable checkpoint exists, return `NO_DURABLE_CHECKPOINT`. Retrieval or
validation failure returns a typed error and leaves HOT state untouched. The
command creates no maintenance-audit entry.

The checkpoint is recovery evidence/description; `MANIFEST.last_checkpoint_id`
is the pointer to it. Neither should be treated as a universal cross-domain
frontier merely because the export operation resolves both.

## 4. `HDM_RESET_LAST_CHECKPOINT`

Purpose: discard local state after the latest acknowledged checkpoint and
reconstruct from that checkpoint.

The exact command is explicit authorization for this scoped destructive local
operation. It never changes GitHub history or deletes the durable checkpoint.

Safe procedure:

1. identify current runtime session and latest acknowledged checkpoint;
2. retrieve and validate all recovery inputs before modifying HOT state;
3. build the replacement in a separate temporary runtime store;
4. verify state/audit consistency, applicable domain markers and required active
   recovery roots;
5. atomically swap the validated replacement into the session;
6. retain the previous local store until the atomic replacement succeeds, then
   dispose of it according to local recovery policy;
7. write one `runtime.maintenance_audit` record outside gameplay chronology.

Failure before the swap leaves the current HOT store unchanged. Failure during
an atomic replacement restores the previous store or reports
`MAINTENANCE_RESET_FAILED` without pretending success.

Minimum maintenance record:

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

The record does not receive a turn ID and is not published as campaign history
unless an explicit diagnostics policy later requests that artifact.

## 5. Repository transport

Maintenance commands use the already selected and authorized GitHub Connector
access path and the applicable runtime `PERSISTENCE.md` / storage contract.
They do not probe shell/native Git, do not create a parallel transport selector,
and do not persist a maintenance-only `runtime.session.transport_mode`.

Where transport behavior is diagnostically relevant, exports may include the
observable Connector operations, repository/ref identities, failures and retry
provenance needed to investigate the problem. Such diagnostic evidence is a
support projection, not session authority or gameplay state.
