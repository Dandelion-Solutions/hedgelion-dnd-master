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
  event, chapter entry, or gameplay transcript entry.
- Do not advance chronology, event-local time, action economy, resources, or RNG.
- Never export credentials, environment-variable values, hidden instructions,
  chain-of-thought, or unavailable/compacted ChatGPT context.
- Report unavailable data explicitly rather than implying a literal model-memory
  dump.

Runtime state stores one counter only:

```text
last_turn_number: integer >= 0
```

An ordinary message atomically increments this value and derives its display ID
as `turn-{last_turn_number:05d}`. Maintenance commands neither increment nor
persist a `next_turn`; the next number is always `last_turn_number + 1`.

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
- active transport mode and the recorded native-probe result;
- integrity checks and explicit missing-data warnings.

The command is read-only and creates no maintenance-audit entry. File creation
for user download is an export side effect, not game-state mutation.

## 3. `HDM_EXPORT_CHECKPOINT_LOG`

Purpose: export and validate the latest acknowledged durable checkpoint without
changing current HOT state.

Procedure:

1. resolve the canonical latest-checkpoint pointer/frontier;
2. retrieve the exact repository, ref/commit and path using the already selected
   session transport mode;
3. validate checkpoint schema, source/runtime revision and section hashes;
4. write one readable diagnostic envelope containing the checkpoint and
   validation/provenance report;
5. attach/export the file without hydrating or replacing HOT state.

If no durable checkpoint exists, return `NO_DURABLE_CHECKPOINT`. Retrieval or
validation failure returns a typed error and leaves HOT state untouched. The
command creates no maintenance-audit entry.

## 4. `HDM_RESET_LAST_CHECKPOINT`

Purpose: discard local state after the latest acknowledged checkpoint and
reconstruct from that checkpoint.

The exact command is explicit authorization for this scoped destructive local
operation. It never changes GitHub history or deletes the durable checkpoint.

Safe procedure:

1. identify current runtime session and latest acknowledged checkpoint;
2. retrieve and validate all recovery inputs before modifying HOT state;
3. build the replacement in a separate temporary runtime store;
4. verify state/audit/frontier consistency and required active roots;
5. atomically swap the validated replacement into the session;
6. preserve the session transport mode (`native_git` or `connector_fallback`);
7. retain the previous local store until the atomic replacement succeeds, then
   dispose of it according to local recovery policy;
8. write one `runtime.maintenance_audit` record outside gameplay chronology.

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

## 5. Transport-mode caching

At the first GitHub operation in a new game/runtime environment, probe native
Git once. Store the result in `runtime.session.transport_mode`:

```text
native_git | connector_fallback
```

After a confirmed native failure, all later GitHub operations in the same
game/chat environment use `connector_fallback` directly. A new environment or
an explicit operator maintenance action may probe again. Normal save, restore,
export and reset commands do not repeat a known-failing probe.
