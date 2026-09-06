# HDM Branch / Ref Deletion Prohibition — Product Owner Decision

Status: **OWNER-APPROVED AUTHORITY / SAFETY / REPOSITORY-OPERATION POLICY — CANONICAL INPUT**

Date: 2026-09-06

Purpose:

> Make branch/ref deletion unavailable to HDM automation. Authority ends through routing/currentness and lifecycle state, never by deleting a Git branch/ref.

This is a direct Product Owner override of the previously optional ref-deletion capability in Step 5.13 / Step 5.14. It is a targeted supersession; it does not reopen the rest of Step-5 cleanup, retention, survivor, currentness or publication architecture.

## Product Owner input — VERBATIM / IMMUTABLE

```text
На счет permanent delete: нет, никакая LLMка не имеет права удалять ветки в репозитории. Можешь так прямо и зафиксировать в core-файлах HDM и GAME, что удаление веток не предусмотрено, и команда `delete branch` не должна вызываться вообще никогда, ни при каких обстоятельствах.
```

---

## 1. Absolute prohibition

### LAW BRANCH-DELETE-1 — HDM NEVER DELETES A BRANCH OR REF

No HDM development agent, gameplay/runtime agent, maintenance routine, migration, repair, cleanup path, test helper or other HDM-controlled automation may delete a Git branch/ref in any repository.

The prohibition applies regardless of:

- repository ownership or collaborator/Admin/Write permission;
- branch kind (`campaign/*`, `live/*`, development, maintenance or other);
- branch age, inactivity, absorption, orphan classification or storage pressure;
- whether a Connector/API/CLI/runtime technically exposes a deletion capability;
- whether the branch is non-authoritative, stale, superseded, closed or believed unused.

There is no HDM `delete branch` / `delete ref` operation. An agent MUST NOT invoke, synthesize, wrap, script or probe such an operation through Connector, API, CLI, native Git or another transport.

### LAW BRANCH-DELETE-2 — TASK-LOCAL AUTHORIZATION DOES NOT OVERRIDE THIS POLICY

Ordinary task instructions, cleanup authorization, maintenance authorization, migration authority, campaign ownership or repository write permission do not grant branch/ref deletion authority.

Changing this rule requires a later explicit Product Owner policy decision that supersedes this owner decision.

---

## 2. Authority and retained refs

### LAW BRANCH-DELETE-3 — BRANCH EXISTENCE IS NOT AUTHORITY

A branch/ref becomes authoritative or non-authoritative only through its existing native routing/currentness/lifecycle owners.

Therefore an absorbed live ref, prepared orphan ref, stale ref or other non-current ref may remain physically present indefinitely without regaining gameplay authority.

### LAW BRANCH-DELETE-4 — MISSING REF IS OBSERVED, NOT ATTRIBUTED TO HDM DELETION

A ref may be absent because of out-of-band human/repository administration or another external condition. HDM may observe and safely classify that state under existing integrity/recovery contracts, but HDM must not perform the deletion itself.

A stale host must never recreate old authority merely because a previously known ref is absent or because it remembers the branch name.

---

## 3. What this policy does not prohibit

The following are distinct operations and are not branch/ref deletion:

- semantic retirement of a record from a current campaign tree when its owner-specific cleanup contract permits it;
- deleting a file/path as part of one validated campaign-tree transaction when the existing semantic cleanup law permits that path deletion;
- compaction/replacement of retained records under their native owners;
- host-managed reclamation of unreachable Git objects outside HDM semantic/runtime control;
- a human repository administrator manually changing repository refs outside HDM automation.

HDM does not turn any of these into authority to call a branch/ref-delete operation.

---

## 4. Supersession of previous cleanup capability

This decision supersedes only the branch/ref-deletion portions of the existing Step-5 corpus.

In `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`:

```text
LAW 5.13-4      superseded for ref deletion
LAW 5.13-71     superseded
LAW 5.13-72     superseded
LAW 5.13-73     superseded
```

The resulting current rule is:

```text
eligible non-authoritative ref
    -> retain the ref as non-authoritative transport residue
    -> never invoke branch/ref deletion
```

All other Step-5.13 laws remain in force, including native-owner liveness, typed blocker proof, survivor-before-removal, current-basis validation, conservative retention, campaign-path cleanup and host-managed unreachable-object semantics.

In `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`, feasibility item `SD-6 live-ref deletion capability` is superseded. Ref-deletion capability is neither required nor optional for HDM; it is forbidden.

---

## 5. Required DEV/GAME realization

Current core projections must make the prohibition explicit:

- `AGENTS.md` — all development agents treat branch/ref deletion as forbidden regardless of tool availability;
- `GAME/CORE/PERSISTENCE.md` — RepositoryPort/write sequencing contains no branch/ref-delete operation;
- `GAME/CORE/LIVE_SCENE.md` — absorbed/orphan live branches remain retained non-authoritative refs rather than deletion candidates;
- `DEV/PRODUCT_OWNER_INPUT.md` — preserve and route this Product Owner decision;
- DEV regression tests — fail if executable HDM tooling introduces a branch/ref-delete invocation or required core projections regress to permitting it.

WP-21 must consume this decision in its diagnostics/cleanup/retirement framing. WP-24 may evaluate the operational cost of retained non-authoritative refs, but such evaluation cannot silently re-enable branch deletion.

---

## 6. Version Impact

This decision changes runtime behavior in two version-bearing CORE modules and therefore requires module-local revision bumps under `DEV/RELEASE/VERSIONING.md`:

```text
GAME/CORE/PERSISTENCE.md: 0.2.1 -> 1.0.2
GAME/CORE/LIVE_SCENE.md:  0.1.2 -> 1.0.3
```

No engine release identity, campaign/storage/catalog generation or persistent record schema changes merely because branch/ref deletion is prohibited.
