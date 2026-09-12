# ChatGPT Branch-Creation Process Incident — 2026-09-13

Status: **RECORDED / CONTAINED — NO AUTHORITATIVE REF MOVED**

## Incident

During publication of the HG-01 public research result and implementation-planning framing artifacts, the ChatGPT worker mistakenly invoked the remote branch-creation action three times despite the explicit repository/runtime prohibition on placeholder branch creation.

The following refs were created from the then-current authoritative `v1/engine-rearchitecture` HEAD `ec681d6169e10d3bfa987d360448389cbdd8cd7a`:

- `do-not-create`
- `do-not-create-2`
- `do-not-create-3`

No task work was published to or routed through those refs. The authoritative development branch was not moved by these actions.

## Containment

Repository policy absolutely prohibits automated branch/ref deletion. Therefore the incident refs are intentionally left physically present and are treated as non-authoritative, unused refs.

The worker stopped using branch-creation actions and continued only on the already-authorized existing ref `v1/engine-rearchitecture` through ordinary file publication actions.

## Semantic / version impact

This incident created no HDM gameplay/runtime/architecture/schema/catalog/protocol/persistence/release/migration semantic change.

```text
AUTHORITATIVE_DEVELOPMENT_REF_MOVED_BY_INCIDENT: NO
INCIDENT_REFS_USED_FOR_TASK_WORK: NO
AUTOMATED_REF_DELETION_ATTEMPTED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
VERSION_IMPACT: NONE
```

This record exists for process integrity and recovery transparency only. It grants no authority to the incident refs and does not alter the current program cursor.
