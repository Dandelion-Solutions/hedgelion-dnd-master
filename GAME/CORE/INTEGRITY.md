# Canon Integrity and Repair

framework_module_version: 0.1.1
load_when: CANON_SUSPECT, confirmed canon corruption, bounded integrity diagnosis or repair

Integrity checks are incremental and scope-local. During normal play validate only loaded records, dirty records, and direct dependencies required by the current decision or pending write. Never scan the full campaign, traverse the full entity graph, or read broad Git history merely to prove health.

Use scoped states:
- `CANON_OK`: no known integrity violation in the checked scope;
- `CANON_SUSPECT`: evidence may indicate persisted corruption, but stale state/incomplete retrieval has not yet been excluded;
- `CANON_CORRUPT`: incompatible persisted facts or a required unusable/missing canonical record are confirmed at the current canonical frontier.

Raise `CANON_SUSPECT` when a required loaded record is malformed/schema-invalid, a required ID/reference resolves to no valid target, authoritative loaded records assert mutually exclusive current state for the same entity/time, CURRENT/checkpoint/scene pointers cannot be reconciled with required target state, a pending write would violate a directly touched invariant, or a semantic conflict remains after refresh to latest pinned HEAD.

Do not treat genuine `UNDEFINED`, absent optional fields, unloaded irrelevant references, contradictory NPC/PC beliefs, legitimate perception differences, stale pre-refresh multiplayer state, or incomplete prose as corruption.

On `CANON_SUSPECT`:
1. block only adjudication/writes that depend on the suspect scope;
2. refresh/pin to latest relevant HEAD using the lightweight read path;
3. reread only exact suspect records/indexes/direct dependencies required to test the invariant;
4. clear suspicion if refreshed state is coherent;
5. otherwise mark the affected scope `CANON_CORRUPT` and perform bounded repair.

Independent scenes/entities may continue if they do not depend on the suspect scope and no shared/global invariant is affected.

For Canon Repair, use only as needed: current authoritative records, directly related index/state/checkpoint records, linked semantic events/bounded log, then the smallest relevant commit/compare range. Repair the lowest authoritative layer supported by evidence. Prefer a traceable corrective commit; never force-push live campaign history. Never invent an in-world explanation for a storage/system error. If evidence is insufficient, do not guess.

Before any gameplay persistence batch, validate only dirty-record local invariants, IDs/paths/direct references created or changed, cross-record invariants directly touched by the batch, and compatibility with latest HEAD. Do not validate unrelated records/history.

Normal `CANON_OK` gameplay should add zero GitHub calls when these checks are decidable from the already-loaded working set. Extra reads are allowed only for a direct current-decision dependency, write preflight, or actual `CANON_SUSPECT` diagnosis. Broad audits are maintenance operations, not ordinary gameplay.
