# Local dashboard projection contract

This is a development-only interchange format for five visual skills, not an HDM semantic owner, persistent campaign schema or scheduling API. Evidence -> projection -> HTML is one-way. Neither HTML edits nor local JSON may approve gates, change canonical state, activate work or become test/audit verdicts.

## Local storage and inputs

Resolve the actual project root from the session/workspace; do not guess home-directory clones. Keep all generated data in `.hdm-dashboard/`: `state/`, `html/`, `history/`, and optional `config.json`. Check that this root is ignored before writing inside a tracked checkout. If it is not ignored and source edits are outside current authorization, use an external local work directory and report its path. Never commit projections, rendered HTML, snapshots, comments, raw source extracts or private configuration.

Use `state/{architecture,python-core,llm-runtime,audit,development,po-cockpit}.json` and corresponding HTML names. Development is cockpit's internal projection, not a sixth skill. Each specialist also works independently. Missing companion output is an explicit missing tile; invoking a specialist is not permission to change roles or sources.

Private audit repository/ref/bootstrap route and optional local cache path belong only in local config/session inputs. Do not put private repository identities, URLs, findings, screenshots or copied private text into tracked public skill examples or evidence reports. A clone is an optional cache, not authority in a Connector runtime. Do not switch another checkout's branch.

## Common envelope — all projections

Use exactly these common keys so cockpit can consume outputs without semantic re-analysis:

```json
{
  "schema_version": 1,
  "kind": "architecture",
  "authoritative": false,
  "generated_at": "ISO-8601 timestamp",
  "sources": [],
  "freshness": {"state": "UNKNOWN", "reason": "", "checked_at": null},
  "coverage": {"scope": [], "inspected": [], "uninspected": [], "complete_for_scope": false},
  "claims": [],
  "payload": {}
}
```

`kind` is one of the six filenames above. Unknown values are `null` with a reason, never fabricated timestamps, hashes, zeroes or PASS. Consumers reject unsupported schema versions or malformed/missing required fields; show “projection unavailable/incompatible” and preserve the last valid snapshot as historical.

Every source entry has `id`, `repository`, `ref`, `analyzed_head`, `observed_head`, `path`, `locator`, `role`, `inspection`, `qualifiers`. Record a blob hash when supplied. Roles distinguish owning law, accepted amendment, PO intent, current status, implementation/test, derivative, research and historical. A supplied synthetic fixture may have null locations with that limitation stated; production facts require recoverable source locations. Resolve HEAD before reads, read a coherent pinned basis, and re-read the ref after collection. Never stamp yesterday's analysis with today's HEAD.

Every claim has `id`, `type` (`FACT / DERIVED / RISK / UNKNOWN`), `text`, `source_ids`, `scope`, `status`, `qualifiers`, `consequence`, and `revisit_trigger` (nullable). Preserve source vocabulary in `status`. A DERIVED claim identifies its reasoning basis briefly; a RISK is not a confirmed defect. Negative findings, exceptions, non-goals, confidence and defer conditions belong in qualifiers. An UNKNOWN can have no source only when its missing evidence is explicit. Graph nodes, edges, gates and counters reference claim IDs. Keep IDs stable across refreshes; labels are not identities.

## Freshness and incremental refresh

- `CURRENT`: complete declared scope at current checked inputs, or complete comparison plus unchanged relevant owners/dependency closure proves reuse; preserve analyzed and observed heads separately.
- `PARTIAL`: some required scope unavailable/uninspected, mixed incompatible bases, or only a bounded subset refreshed.
- `STALE`: known relevant changes invalidate a retained projection/claim.
- `UNKNOWN`: HEAD, comparison or dependency applicability cannot be established.

Fresh input retrieval does not make an old audit verdict current. Keep audit currency separate in its payload.

Fast mode: cockpit status/gates and audit-currency check; retain other tiles with their actual freshness. Normal: compare prior analyzed heads with fresh refs; refresh changed owners AND known consumers, including renames, deletions, process/PO/supersession changes. Reuse only with a complete relevant comparison and dependency basis. Deep: rebuild the selected ownership subgraph, never imply whole-repository coverage from a selected view. Truncated/incomplete comparisons cannot prove “unchanged.” If no prior snapshot exists show “first view,” not “no changes.”

Write a complete validated candidate before replacing the previous local projection. Keep prior successfully presented snapshot for `changed since last view`; generation is not proof the user viewed it. When actual presentation cannot be observed, label the comparison “since last generated snapshot.” Do not overwrite the prior snapshot before computing the change set.

## Presentation semantics

Every page shows source basis, freshness and scope. Every material tile drills down to claim -> exact evidence -> qualifier/consequence. Separate accepted design, implementation reported/observed, independent review, integrated verification and activation; they are not one completion flag. No aggregate health percentage or completion bar from task counts. A coverage count needs an explicit enumerated denominator and per-item disposition. A change impact metric such as “0 new model calls” needs inspected proof; otherwise unknown.

Gates preserve `source_status` and use a separate display state (`OPEN / IN_PROGRESS / BLOCKED / CLOSED / DEFERRED / UNKNOWN`) with evidence for the mapping. Keep `gate_kind` (`PO_DECISION / SENIOR_REVIEW / TECHNICAL_DEPENDENCY`) and decision owner separate. A Senior stop is not automatically a PO decision. Dashboard controls navigate/filter/review; they never authorize work or write owner state.
