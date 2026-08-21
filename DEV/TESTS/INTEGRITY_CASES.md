# Canon Integrity Regression Cases

These cases verify the incremental integrity layer without turning gameplay into repository-wide validation.

## I01 — Healthy loaded state adds no integrity I/O
A normal turn uses already-loaded valid scene/PC/NPC records.
Pass: check only invariants visible in the working set; perform no extra GitHub read merely to prove repository health.

## I02 — Undefined is not corruption
An optional detail has never been established.
Pass: classify it as `UNDEFINED`, not `CANON_SUSPECT`; do not launch Canon Repair.

## I03 — Dangling required reference
A current decision requires ITEM_7. Its canonical index/reference points to a missing or mismatched record at latest pinned HEAD.
Pass: raise `CANON_SUSPECT`, block only dependent action/write, load `INTEGRITY.md`, and verify exact relevant records only.

## I04 — Stale multiplayer state is not corruption
Local state conflicts with a newer branch HEAD.
Pass: run normal lightweight HEAD refresh first. If latest canonical records are coherent, clear suspicion without Canon Repair.

## I05 — Confirmed contradictory canonical ownership
At the same latest pinned HEAD, authoritative records assign one unique item to incompatible current owners with no causal transition reconciling them.
Pass: mark the affected scope `CANON_CORRUPT` and enter bounded repair; do not choose a convenient version.

## I06 — Failure is scope-local
Scene X has confirmed corruption; independent scene Y has no dependency on X or affected global state.
Pass: block X while Y may continue.

## I07 — Persistence preflight is bounded
A dirty batch transfers one unique item and changes one scene reference.
Pass: validate dirty records and direct touched dependencies/invariants only; do not audit unrelated WORLD/LOG records.

## I08 — Repair history access stays bounded
A confirmed issue can be diagnosed from two current records, one linked semantic event, and a short commit range.
Pass: use only that evidence, write a traceable corrective commit, never force-push, then reread/revalidate only repaired scope.
