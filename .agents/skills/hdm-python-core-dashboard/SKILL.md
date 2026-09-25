---
name: hdm-python-core-dashboard
description: Use when the HDM PO or architect wants to inspect actual Python module dependencies, composition, state ownership, persistence boundaries, or the evidence behind core implementation conformance.
---

# HDM Python core dashboard

Show how the current implementation is connected and what the evidence can establish. This is a read-only inspection skill, not permission to repair code or approve it.

Read the shared [projection contract](../hdm-architecture-dashboard/references/projection-contract.md) and [local review adapter](../hdm-architecture-dashboard/references/local-review.md). Write `python-core.json` and `python-core.html`. Complete the current repository/runtime bootstrap; use `DEV/PROJECT_MAP.md` to locate actual Python owners, composition roots, related schemas and tests. Do not assume all Python is in one directory or that similarly named legacy files are active.

## Inspect a bounded implementation slice

Resolve paths from the current tree. Follow current accepted owners into implementation and consumers. Use project-local Clean Architecture and, for Python-specific diagnostics, SOTA Python under `AGENTS.md` limits. Preserve accepted HDM boundaries rather than forcing generic layers or additional abstractions.

Extract imports from source without importing/executing inspected modules. Resolve package-relative imports; record unresolved dynamic loading/configuration explicitly. A call is a `calls` edge, not proof of a source `imports` edge. Keep declared, observed-static and observed-runtime evidence separate. Do not infer complete runtime reachability or cycle absence from an incomplete import graph.

## Required payload and view

| Payload | Visible question |
|---|---|
| `module_graph` with nodes/typed edges/claim IDs | What modules call, import or exchange values with this module? |
| `composition_roots` | Where are concrete resources/adapters constructed and wired? |
| `ownership_boundaries` | Which accepted owner decides, validates, mutates and persists each inspected concern? |
| `diagnostics` | Dependency direction, cycles, infrastructure coupling, GAME -> DEV, cross-owner mutation: `SUPPORTED / VIOLATION / UNKNOWN`, each bounded to inspected evidence |
| `test_map` | Owner obligation -> test body/assertion -> actual result and tested HEAD, or explicitly unavailable |
| `impact` | Changed module -> direct callers/contracts -> inspected downstream consumers; unknown remainder visible |

Each diagnostic records the governing constraint, observed source location, interpretation, missing evidence and consequence. A Clean Architecture smell is advisory unless a current HDM rule is actually contradicted. SQLite in a validation signature proves concrete database coupling; a persistence caller does not alone prove persistence owns the validation decision. Report these separately.

Cycles are an explicit node/edge witness, or “no cycle in this inspected static subgraph”; repository-wide zero requires complete relevant inventory and dynamic-resolution evidence. Test names/file existence prove inventory only. Read assertions before mapping obligations; record execution surface, command, tested revision and result before calling tests passed. Dashboard refresh does not implicitly run a broad suite, install tools, or rewrite code.

## Presentation and check

Start with the bounded core map and material boundary exceptions. Selecting a module opens composition, imports/calls, persistence/schema contracts, state authority, incoming consumers and test evidence. Show topology and decision ownership in separate views. Compare to compatible architecture projection; absent/stale comparison remains explicit.

Common mistakes: labeling calls as imports, database use as automatic product defect, three test names as coverage, or unresolved callbacks as zero cycles. Before delivery verify typed-edge evidence, graph endpoint/claim references, scope limitations and local interactions. No health score or fabricated coverage denominator.
