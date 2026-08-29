# Documentation Corpus Refactor — Execution Plan

Status: **OWNER-APPROVED / EXECUTING**
Date: 2026-08-29

## Goal

Refactor `DEV/docs/superpowers/` from the historical three-directory artifact model into a four-directory semantic taxonomy:

```text
research/  durable research / experiment / idea results
design/    design-process and provenance history
specs/     final accepted implementation-facing specifications/decisions
plans/     implementation plans after approved design
```

The refactor must complete before substantive R2.7 WP-07 analysis. It is an inserted workstream, not a numbered R2.7 WP.

## Approved design / source

The repository owner approved the complete taxonomy, census, split/promotion-before-move, reference-repair and closure requirements in the 2026-08-29 Documentation Corpus Refactor assignment. No gameplay or mechanical architecture semantics are changed by this plan.

## Implementation Impact Envelope

```text
SPEC / APPROVED DESIGN:
  2026-08-29 owner-approved Documentation Corpus Refactor assignment

BASELINE REF OR SHA:
  v1/engine-rearchitecture @ 06f70919d52739f72515a5d315bb0998d7c34c6e

EXPECTED OWNERS TO CHANGE:
  AGENTS.md
  DEV/DESIGN_PROCESS.md
  DEV/ARCHITECTURE/DESIGN_PROCESS.md
  DEV/DEVELOPMENT_EXECUTION_PROCESS.md
  DEV/PROJECT_MAP.md
  DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md
  DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md
  DEV/docs/superpowers/** documentation corpus
  maintenance/path validation only when needed to guard taxonomy/routing

EXPECTED CONSUMERS TO CHANGE:
  current live Markdown routing references, Source Manifests, status/cursors,
  derivative indexes and any tests/tools/scripts with hard-coded migrated paths

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
  development-document placement/routing taxonomy and documentation paths only

PROTECTED ARCHITECTURE INVARIANTS:
  all accepted gameplay/mechanical/LLM/persistence/authority semantics
  WP-06 findings and forward obligations WP-06/F02/F03
  WP-07 substantive analysis remains not started
  root README editorial contract
  no hidden final semantic authority may remain only in research/ or design/

ARCHITECTURE-SENSITIVE SURFACES:
  final accepted owner/spec discoverability
  supersession/current-authority routing
  research evidence/provenance preservation
  R2.7 durable cursor and sequencing

EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION:
  semantic census completeness
  moved-file/reference reconciliation
  stale-path/broken-link scan
  final-authority stranding/duplication checks
  maintenance audit + full DEV unit suite + hosted CI + remote read-back

KNOWN OUT-OF-SCOPE OWNERS / SURFACES:
  gameplay semantics
  new machine vocabulary
  broad CORE cleanup
  WP-06/F02 and WP-06/F03 discharge
  WP-07 substantive analysis
  root README edits
```

## Task 1 — Synchronize routing/status

- Record WP-06 `CLOSED / SENIOR REVIEW PASS` and exact final SHA/workflow evidence.
- Keep `CURRENT_DOMAIN: WP-07`, but mark substantive WP-07 not started.
- Activate Documentation Corpus Refactor as an inserted required-before-WP-07 workstream; do not number it.
- Synchronize roadmap, derivative canonical index and durable R2.7 cursor.
- Publish and remote-read-back.

## Task 2 — Activate four-directory public instructions

- Update `AGENTS.md`, generic/HDM design process, implementation execution process and `DEV/PROJECT_MAP.md` where they encode artifact placement/discovery.
- Add `DEV/docs/superpowers/README.md` as short non-authoritative navigation entry.
- Create `design/` via a tracked README/manifest artifact or first migrated design artifact.
- Define eight-step output routing: standalone research -> `research/`; intermediate/provenance -> `design/`; final accepted implementation-facing result -> `specs/`; implementation plan -> `plans/`.
- Add focused maintenance validation only if it materially prevents regression.
- Verify before mass migration.

## Task 3 — Complete semantic census

- Enumerate every pre-refactor file under `research/` and `specs/`.
- Read each nontrivial source deeply enough to classify all material sections.
- Persist a census with section/range class, authority/supersession, destination, split/extraction requirements, live consumers and duplication/provenance risks.
- Do not infer classification from filename/folder/front matter alone.

## Task 4 — Migrate homogeneous design history

- Move process/provenance artifacts to `design/` using original blobs where no content edit is required.
- Preserve exact historical content and provenance.
- Do not strand implementation-relevant final law in the moved design corpus.

## Task 5 — Clean research and perform promotion/splits

- Keep durable experiments/research findings/idea dossiers in `research/`.
- For mixed sources, split only when taxonomy/discoverability requires it.
- Promote exact accepted semantics into an appropriate final spec/durable architecture owner before demoting process/research history.
- Preserve methods, qualifiers, negative findings, limitations and revisit triggers.

## Task 6 — Consolidate implementation-facing specs

- Keep only final approved specs, accepted canonical amendments, final accepted owner decisions and other genuinely required implementation-facing final documents in `specs/`.
- Move raw briefs/critics/candidates/reviews/status/history out unless they are themselves the final required accepted source.
- Prove a fresh implementation planner can discover accepted architecture from durable architecture owners + `specs/` without bulk-reading `design/`/`research/`.

## Task 7 — Repair live routing/references

- Perform repository-wide inbound-reference/path census.
- Update current live Markdown/routing consumers, process/index/status docs, tests/tools/scripts and current Source Manifests.
- Preserve historical old paths when they are exact historical statements rather than live routes.
- Do not edit root `README.md`; record any exact stale mismatch for owner review.

## Task 8 — Final verification and closure

- Verify four-directory taxonomy and every census disposition.
- Verify no stale live migrated paths, broken live Markdown references, hard-coded old paths, stranded final authority or duplicate current owner.
- Run maintenance audit, complete DEV unit suite and applicable hosted CI.
- Remote-read-back final SHA and write exact durable closure cursor.
- Stop for Senior review; do not begin WP-07.
