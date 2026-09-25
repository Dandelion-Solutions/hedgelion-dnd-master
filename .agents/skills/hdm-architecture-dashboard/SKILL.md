---
name: hdm-architecture-dashboard
description: Use when the HDM PO or architect wants a clickable system map, ownership or dependency impact view, or comparison of accepted architecture with implementation evidence.
---

# HDM architecture dashboard

Produce a local evidence view of the accepted system and its realization. This skill advises no architecture change and grants no implementation or audit authority.

Read [projection contract](references/projection-contract.md) for every refresh and [local review](references/local-review.md) before rendering or opening HTML. Those references also serve the other four dashboard skills.

## Evidence route

Complete current HDM `AGENTS.md` and runtime bootstrap. Use `DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` to construct a bounded Source Manifest, then inspect actual owners, amendments, relevant PO routes, schemas, code and tests. Index entries locate evidence; they cannot settle disputed ownership. Load the project-local Clean Architecture skill as a diagnostic lens under HDM authority, without numeric scoring or textbook relabeling.

## Output recipe

Write `architecture.json` and `architecture.html` under the contract's local directories.

| Surface | Required contents |
|---|---|
| Overview | Small clickable map of actual HDM responsibilities; group by evidenced ownership, progressively expand neighborhoods |
| Canonical / actual comparison | Separate `canonical_graph` and `actual_graph`, joined by stable responsibility IDs; never one graph that mixes accepted law with reported realization |
| Selected responsibility | Purpose, canonical owners, contracts, state/persistence ownership, incoming/outgoing typed edges, implementation modules, tests, downstream consumers |
| Conformance | Per obligation: expected owner law, observed behavior, evidence basis, `SUPPORTED / CONTRADICTION / UNVERIFIED / DEFERRED`, consequence and revisit trigger |
| Impact | Selected change -> directly affected owners -> evidenced downstream consumers; uninspected reach is visibly unknown |

Each graph has `nodes` and `edges`; each node/edge points to claim IDs from the common envelope, and every endpoint resolves to a node in that graph. Edges distinguish imports, calls, data flow, semantic dependency, physical persistence and semantic state ownership. Label Storage -> event as `persists`, never `owns`, unless the accepted owner explicitly grants semantic ownership. An import is evidence of an import, not a verdict about policy direction. A contradiction requires both the current accepted constraint and incompatible observed behavior. Missing code or tests is an evidence gap; deferred realization remains deferred until its exact trigger.

Display current progress only to explain capability state and touched boundaries. Reuse compatible Python/LLM projections for actual topology and the audit projection for audit claims; absent projections are marked missing, not re-created by guessing. Do not call every module implemented because its specification is accepted.

## Example

An accepted owner says Acceptance owns event identity; code calls Storage.save. Show the accepted ownership edge in the canonical plane and the observed call in the actual plane. Mark identity conformance unverified until validation behavior is inspected. If an index assigns identity to Storage, record a derivative-routing conflict, not a newly discovered product owner.

## Common mistakes / final check

Red flags: one blended diagram, score without a defined basis, global green from a narrow review, or an uninspected node colored compliant. Correct these with the explicit comparison slots above. Verify every selectable node/edge opens its claim, source and consequence; account for the bounded scope and unresolved evidence before delivery.
