# R2.7 WP-09 Step 2 — Current Runtime and Retrieval Evidence

Status: **EVIDENCE SLICE 2 COMPLETE — MACHINE/TEST CONSUMERS NEXT**

## Scope and method

This reverse slice reads the current GAME runtime/cache, campaign routing schemas and
the directly named catalog/test consumers at the verified ref. It distinguishes a
current supporting surface from the R2.3 Context Runtime logical owner; it does not
claim a repo-wide absence from a selected-surface inspection.

## Extracted current-surface evidence

| ID | Actual current source / item | Evidence | Disposition against canonical owners |
|---|---|---|---|
| M01 | `GAME/CORE/PLAY_POLICY.md` — Immutable CORE context cache; Campaign data remains lazy | Complete selected local `CORE/*.md` plus two RULES routing files are immutable in-chat engine instruction cache. Campaign canon is explicitly excluded; campaign reads are targeted to hot state, current scenes, relevant records, exact index entries and bounded history actually required. | SUPPORTING only. The engine cache is not a role bundle, source basis, campaign canon or a substitute for R2.3 packet assembly. |
| M02 | `GAME/CORE/RUNTIME.md` — normal turn, targeted retrieval and sync | A normal in-scene turn uses the loaded working set. Additional retrieval requires a material current-decision, exact-mechanic, resync, race-sensitive or persistence reason; sync is HEAD probe, changed-path comparison, then exact relevant reads pinned to one HEAD. No ordinary broad scan/history retrieval is allowed. | SUPPORTS bounded reads and R2.6 conservative operation; does not itself allocate profile floors, representations or R2.3 terminal outcome. |
| M03 | `GAME/CORE/STORAGE.md` — Stable IDs and lazy retrieval | Compact INDEX entries route to exact records; the world graph is not recursively traversed. `STATE/CURRENT.yaml` is compact routing/hot state, not a transcript; LOG is compact semantic history, not a journal/transcript. | SUPPORTS discovery inputs only. Native owner/currentness and eligibility still require the R2.3/Step-5.14 route. |
| M04 | `GAME/SCHEMA/current_state.schema.yaml`, `scene.schema.yaml`, `location.schema.yaml` | CURRENT carries active scene id/path/PC routing; scenes contain current actionable summary and local participant/thread/environment references; locations deliberately do not require `present_entity_ids` to be authoritative. Biographies/history and generic pending/tactical state have typed owners elsewhere. | Directly confirms CURRENT/scene/location are high-yield, non-closed-world seeds. It forbids treating any one of them as universal closure. |
| M05 | `GAME/SCHEMA/index.schema.yaml` and current empty `GAME/CAMPAIGN/INDEX/{SCENE,LOCATION,NPC}_INDEX.yaml` templates | Index entries are compact id/name/aliases/status/path/parent/tags/last event routing records; the schema says they are not duplicate entity databases and aliases do not redefine identity. Current template indexes show only the declared index shape, not a populated-world completeness proof. | Directly supports R2.3 routing-only index law. No index completeness, partitioning or closed-world inference is admitted. |
| M06 | `GAME/CORE/CORE_INDEX.md` and `GAME/CORE/{INFORMATION,PREP,NPC,NARRATIVE}.md` | CORE routing preserves cached engine instructions versus active modules; information/narrative avoid unrelated disclosure; PREP distinguishes definite from remote material; NPC mechanics remain lazy and deterministic. | Adjacent consumer guidance. These files do not own ContextNeedProfile, source eligibility or a persistent context store. |
| M07 | `DEV/CATALOG/core-catalog.json` — type/registry rows | The current catalog registers `value.role_context_request`, `value.context_need_profile`, `value.role_context_bundle`, `value.context_trace`, `value.context_budget_envelope`; it also registers all seven discovery channels, five representation classes and all three assembly outcomes. | Machine vocabulary is aligned with R2.3. Registration alone is not behavioural execution, durable authority, or proof of a complete runtime realization. |
| M08 | `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md`, `RUNTIME_SCOPE_LATENCY_CASES.md`, `PERFORMANCE_CASES.md` | Existing regressions prove full-CORE cache distinction, campaign data laziness, targeted schema access and current-working-set latency discipline. | Useful partial regression base. They do not yet prove registered profile ownership, routed currentness/eligibility, legal floors/degradation, central estimation or finite `UNSATISFIABLE` caller handling. |
| M09 | `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` and `DEV/TESTS/test_s6d_04_mechanical_context_contract.py` | MechanicalContext is a bounded deterministic mechanical-stage accessor/invocation-fact contract with disposable derived caches and pinned state view. | Explicitly separate owner. It cannot carry R2.3 role-context source eligibility, broad retrieval, or role-private continuity/control already constrained by the closed WP-08 input. |
| M10 | `DEV/ARCHITECTURE/BRANCH_MODEL.md`, `RULESET_PACKAGE_MACHINE_CLOSURE.md`, `.github/workflows/validate.yml` | Runtime package excludes DEV; campaign storage is a separate persistent-data repository; package closure/audit and CI are development/release machinery. | Guards scope: no DEV path becomes runtime context authority, and no package/CI audit is normal gameplay retrieval. |

## Reverse result

The current runtime already has a **compatible supporting topology**:

```text
cached engine instructions != lazy campaign working set
CURRENT / scene / compact INDEX -> routing hints -> exact targeted record reads
```

This is compatible with, but is not an implementation of, the accepted R2.3
pipeline. The catalog has the required symbolic vocabulary, while the selected
runtime/test surfaces do not provide behavioural proof for profile-owned required
closure, currentness/eligibility validation, packet floors, controlled
degradation, conservative central estimate, or a finite caller path for
`UNSATISFIABLE`.

That is an implementation-facing realization obligation under the existing
canonical R2.3/R2.4/R2.6 law, not evidence for a new memory store, full preload,
provider token API, physical index partition or durable control schema.

## Negative and boundary evidence

- Do not infer that the template INDEX files prove world coverage; they are empty
  scaffold records at this ref.
- Do not infer a general negative for uninspected files from this slice.
- The CORE cache is intentionally in-chat and immutable, but it is not ChatGPT
  Memory or campaign authority.
- MechanicalContext's exact facts/accessors remain an S6D mechanical boundary;
  it is not the R2.3 Context Runtime.
- Physical root/template changes remain WP-10; index partition/topology remains
  WP-11; HOT/SQLite internals remain WP-12.

## Human decision

**NONE.**

## Next evidence slice

Inspect remaining DEV machine contracts, maintenance/audit route and test/CI
consumers, then consolidate Step 2 without turning evidence into a duplicate
canonical specification.
