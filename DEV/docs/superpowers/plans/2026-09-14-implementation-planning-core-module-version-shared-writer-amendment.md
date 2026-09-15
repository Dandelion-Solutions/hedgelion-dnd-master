# HDM Implementation Planning — CORE Module Version / Shared-Writer Closure Amendment

Status: **CURRENT HIGHEST-PRECEDENCE MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR FINDING 46 — SIGNIFICANT**
Production implementation: **NO**.

This amendment closes the exact Category-B `framework_module_version` census for the current RD-01..RD-16 package and repairs two known shared physical CORE-writer collisions. It changes no gameplay semantics, semantic owner, engine release version, schema version, catalog generation, storage generation or campaign generation.

## 1. Finding

The canonical version law defines `framework_module_version` as:

```text
ENGINE_MAJOR.ENGINE_MINOR.REVISION
```

where every later logical/material module change increments that module's revision exactly once and moves the prefix to the current engine major/minor line.

The current implementation package already contains material, mandatory edits to a bounded set of shipped `GAME/CORE/*.md` modules. Several plans still defer the version result to a worker-time `Version Impact Gate` even though the current bytes, current engine line and materiality are already known. More seriously, two modules have more than one independently scheduled material writer without one final CORE integration sink:

```text
GAME/CORE/BOOTSTRAP_RUNTIME.md
  RD-01 R003 transport/no-probe/no-fallback stale-projection repair
  + RD-14/bootstrap product/runtime-root/generator identity projection repair

GAME/CORE/STORAGE.md
  RD-04 owner-native routing/root-selector/storage projection repair
  + RD-07 current-native recovery/current-source/read-order repair
```

A legal worker could therefore either:

- publish one material edit with the old module version;
- let two writers each claim an independently final module generation;
- double-bump because two RDs touched the same module;
- lose the earlier owner's delta when the later worker rewrites the file;
- or decide at implementation time whether the final target is one or two revisions higher.

All are avoidable planning ambiguity. The package already uses the correct model for `MULTIPLAYER.md`: multiple owner deltas converge into one final physical edit and one module revision for the unpublished v1 rearchitecture cutover.

F46 makes that law exact for every currently proven material CORE edit.

## 2. Canonical Category-B law applied by this amendment

For this unreleased v1 package:

1. current engine line for a material CORE edit is `1.0`;
2. preserve the module-local numeric revision history and increment it once for the final logical/material edit;
3. changing `0.x.r` to `1.0.(r+1)` is one material revision, not a reset to revision 1;
4. an engine release/version change alone never bumps an untouched module;
5. inspect-only/currentness-only paths do not receive a speculative bump;
6. an absent retired module receives no tombstone or compatibility bump;
7. when multiple planned owner deltas are intentionally consolidated into one final unpublished v1 module edit, the final integrated file receives one bump, not one bump per RD/finding;
8. if a module were instead published as one independently final material generation and later materially changed again, the later edit would require another revision. F46 forbids that schedule for the two shared modules below by making their owner-local steps non-final delta producers and naming one final integration checkpoint.

## 3. Exact deterministic CORE cutover matrix

The following sixteen current modules have mandatory material changes in the present package and therefore have exact final targets now:

| CORE module | Current | Final v1 target | Mandatory material source(s) | Final version writer/checkpoint |
|---|---:|---:|---|---|
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | `0.8.8` | **`1.0.9`** | RD-01 R003 + RD-14/bootstrap projection repairs | `CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY` |
| `GAME/CORE/RANDOMNESS.md` | `0.1.2` | **`1.0.3`** | RD-01 R043 deterministic RNG consumer repair | RD-01 final RANDOMNESS repair checkpoint |
| `GAME/CORE/EXPLORATION.md` | `0.1.1` | **`1.0.2`** | RD-01 R048 active exploration projection repair | RD-01 final EXPLORATION repair checkpoint |
| `GAME/CORE/STORAGE.md` | `1.0.1` | **`1.0.2`** | RD-04 routing/storage + RD-07 recovery/current-source deltas | `CORE_STORAGE_FINAL_INTEGRATION_READY` |
| `GAME/CORE/SAVE_CONTRACT.md` | `0.2.1` | **`1.0.2`** | RD-06/SIRR SAVE_ALL_DIRTY native-domain publication cutover | RD-06 shipped save-consumer checkpoint |
| `GAME/CORE/PERSISTENCE.md` | `1.0.3` | **`1.0.4`** | RD-06/SIRR frozen-attempt/result-epistemics/publication currentness cutover | RD-06 shipped publication-consumer checkpoint |
| `GAME/CORE/CHRONOLOGY.md` | `0.1.1` | **`1.0.2`** | RD-08 frontier/provider authority replacement | RD-08 temporal machine-alignment checkpoint |
| `GAME/CORE/PROCESSES.md` | `0.1.2` | **`1.0.3`** | RD-08 correctness-dependency simulation/visibility repair | RD-08 temporal machine-alignment checkpoint |
| `GAME/CORE/AI_REASONING.md` | `0.1.3` | **`1.0.4`** | RD-10 ordinary-gameplay role/emission containment owner alignment | RD-10 instruction-owner checkpoint |
| `GAME/CORE/LIVE_SCENE.md` | `1.0.3` | **`1.0.4`** | SIRR2 LIVE consumer cutover, with later F24-F31/F36 requirements folded where they require shipped prose alignment | final LIVE shipped-consumer integration checkpoint |
| `GAME/CORE/MULTIPLAYER.md` | `0.1.7` | **`1.0.8`** | WP-15/WP-16/WP-17 shared multiplayer consumer deltas | existing final shared MULTIPLAYER checkpoint |
| `GAME/CORE/CAMPAIGN_SETUP.md` | `1.0.3` | **`1.0.4`** | author self-review bootstrap/generator/current-runtime correction | existing CAMPAIGN_SETUP repair checkpoint |
| `GAME/CORE/SESSION.md` | `1.0.1` | **`1.0.2`** | WP-17 shipped session/collaboration continuation consumer repair | F17/WP-17 shipped SESSION checkpoint |
| `GAME/CORE/PLAY_POLICY.md` | `0.8.4` | **`1.0.5`** | F14 catalog-backed executable-primitive fence | RD-15/F14 shipped-consumer checkpoint |
| `GAME/CORE/CORE_INDEX.md` | `0.3.1` | **`1.0.2`** | F14 catalog-backed executable-primitive fence | RD-15/F14 shipped-consumer checkpoint |
| `GAME/CORE/ADJUDICATION.md` | `1.0.2` | **`1.0.3`** | F14 catalog-backed executable-primitive fence | RD-15/F14 shipped-consumer checkpoint |

F54 source-binding correction: the `RANDOMNESS.md` row belongs to `R27-R043` / RD-01 `R043` (fixed RNG retention/recovery), not `R27-R050` (information/catalog prose alignment). This corrects the requirement-to-material-version route only; its one final writer, target `1.0.3` and existing proof obligations remain unchanged.

These targets are mandatory for the current package baseline. A worker must not leave any row as `Version Impact: classify` or choose a different target merely because multiple findings contribute to the same final unpublished edit.

If authorized execution begins from a legitimately advanced branch where an earlier accepted change has already materially advanced one of these modules, the worker must fresh-read that exact then-current module and reconcile against the same Category-B law rather than blindly writing the historical number. That future currentness safeguard does not make the present baseline targets uncertain.

## 4. Shared CORE integration — `BOOTSTRAP_RUNTIME.md`

RD-01 and the bootstrap/product repair both own valid but different deltas to one physical shipped module. They do not become two independently final writers.

Expose bounded owner-local readiness:

```text
RD01_BOOTSTRAP_RUNTIME_CORE_DELTA_READY
  = R003 transport/no-probe/no-fallback repair semantics and focused tests GREEN,
    with the exact BOOTSTRAP_RUNTIME prose delta known but not independently final.

RD14_BOOTSTRAP_RUNTIME_PRODUCT_DELTA_READY
  = exact selected-runtime/generator identity/root/bootstrap projection semantics GREEN,
    with the exact BOOTSTRAP_RUNTIME prose delta known but not independently final.
```

Then require:

```text
RD01_BOOTSTRAP_RUNTIME_CORE_DELTA_READY
+ RD14_BOOTSTRAP_RUNTIME_PRODUCT_DELTA_READY
  JOIN_BEFORE_INTEGRATION
CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY
```

The final physical writer is the RD-14/bootstrap integration checkpoint because it owns the final shipped bootstrap/product projection. It must fresh-read the current module, integrate both accepted deltas, preserve unrelated valid behavior, run both focused requirement families, and set exactly:

```text
framework_module_version: 1.0.9
```

RD-01 may prove its owner-local repair before this join, but it must not publish an independently final BOOTSTRAP_RUNTIME generation that would force a second package revision or permit the RD-14 worker to erase it.

F39 remains unchanged: it coordinates the separate `GAME/INSTALL/*` shared files. F46 adds only the missing CORE-module join.

## 5. Shared CORE integration — `STORAGE.md`

RD-04 and RD-07 likewise contribute separate owner deltas to one physical module.

Expose:

```text
RD04_STORAGE_CORE_DELTA_READY
  = owner-native route/root-selector/index/storage projection semantics GREEN,
    with the STORAGE prose delta known but not independently final.

RD07_STORAGE_RECOVERY_CORE_DELTA_READY
  = current-source/recovery/checkpoint/currentness read-order semantics GREEN,
    with the STORAGE prose delta known but not independently final.
```

Then require:

```text
RD04_STORAGE_CORE_DELTA_READY
+ RD07_STORAGE_RECOVERY_CORE_DELTA_READY
  JOIN_BEFORE_INTEGRATION
CORE_STORAGE_FINAL_INTEGRATION_READY
```

The final physical writer is the RD-07 recovery/current-source integration checkpoint. It must preserve the RD-04 routing/storage laws and apply the RD-07 recovery/currentness laws in one coherent final module edit, with exactly:

```text
framework_module_version: 1.0.2
```

This does not claim that two separately published logical edits normally share one revision. The package intentionally prevents them from becoming separate final module generations: both are inputs to one unpublished v1 integrated STORAGE edit. If an implementation schedule attempts to make RD-04's STORAGE bytes independently final and later materially rewrite them under RD-07, it violates this amendment and would also violate the target matrix.

F41 remains about `GAME/SCHEMA/README.md` and `GAME/TEMPLATE/STORAGE_README.md`; it does not substitute for this CORE integration checkpoint.

## 6. Existing shared-module checkpoint preserved

`GAME/CORE/MULTIPLAYER.md` already has the correct shared-writer law. Keep its existing WP-15/WP-16/WP-17 final integration checkpoint and exact target `1.0.8`.

Do not create a second F46-specific MULTIPLAYER writer or bump to `1.0.9` merely because this audit records the row.

Likewise, later LIVE amendments do not automatically add another `LIVE_SCENE.md` revision. Any shipped prose changes required to make the final accepted F24-F31/F36 semantics true must be folded into the one current unpublished LIVE consumer edit targeting `1.0.4`; a genuinely later separately published material change would be a different future revision.

## 7. Conditional / negative rows — no speculative bump

The following current package paths do **not** receive a deterministic F46 bump:

- `GAME/CORE/DOMAIN_RULES_COVERAGE.md` — absent; F44 forbids recreating it for R047; version impact `NONE`.
- `GAME/CORE/INFORMATION.md` — RD-02 edits only if exact current focused evidence proves a contradiction; no mandatory current material edit is established by planning.
- `GAME/CORE/RUNTIME.md` — F14/RD-10 inspection only unless exact current contradiction is found.
- `GAME/CORE/MECHANICS_INTEGRITY.md` — F14 inspection only unless exact current contradiction is found.
- `GAME/CORE/DURABILITY_GUARD.md` and `GAME/CORE/ENGINE_UPDATES.md` — RD-06 disposition/inspection paths only unless exact current contradiction requires a material correction.

If a future execution-currentness test proves a material edit is actually necessary to one of these files, that exact file becomes a named writer input and receives one fresh Category-B increment from its then-current bytes. Do not pre-bump it merely because it was inspected.

## 8. Package proof obligation

Add a package-level witness when implementation/proof execution is authorized, conceptually:

```text
DEV/TESTS/test_implementation_package_core_module_versions.py
  CoreFrameworkModuleVersionCutoverTests
```

It must prove from exact final package bytes:

1. all sixteen deterministic rows carry the target versions above;
2. each version bump accompanies the accepted material behavior, not merely a changed header;
3. `BOOTSTRAP_RUNTIME.md` contains both RD-01 and RD-14 requirement sets and is bumped exactly once;
4. `STORAGE.md` contains both RD-04 and RD-07 requirement sets and is bumped exactly once;
5. `MULTIPLAYER.md` remains the existing one-bump shared integration target `1.0.8`;
6. F14's three mandatory shipped consumers are bumped exactly once and the three inspect-only consumers are not changed solely by F14;
7. F44's absent historical module is not recreated and has no tombstone/version artifact;
8. no deterministic row keeps an old module version after material behavior changes;
9. no module is advanced twice merely because more than one RD/finding contributed to one final unpublished logical edit;
10. no untouched CORE module is mechanically rewritten to the current engine line.

Conceptual proof sink:

```text
all sixteen final module checkpoints GREEN
+ CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY
+ CORE_STORAGE_FINAL_INTEGRATION_READY
+ existing MULTIPLAYER final integration GREEN
  -> CORE_FRAMEWORK_MODULE_VERSION_CUTOVER_PROOF_READY
```

This is a proof sink only. It adds no semantic owner and does not serialize unrelated implementation work.

## 9. Execution-graph consequence

F46 adds exactly two new physical-integration joins plus the package proof sink:

```text
RD01_BOOTSTRAP_RUNTIME_CORE_DELTA_READY ----\
                                             +-> CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY
RD14_BOOTSTRAP_RUNTIME_PRODUCT_DELTA_READY -/

RD04_STORAGE_CORE_DELTA_READY ---------------\
                                              +-> CORE_STORAGE_FINAL_INTEGRATION_READY
RD07_STORAGE_RECOVERY_CORE_DELTA_READY -------/
```

Both integration nodes are sinks for their owner-local prose deltas and feed only their normal downstream shipped-package/proof readiness. Neither feeds back into an earlier semantic prerequisite, so these edges introduce no cycle by construction. They will be re-checked in the dedicated checkpoint-DAG pass.

No whole-RD `HARD_PRECEDES` edge is created. Semantic ownership remains with the existing RDs.

## 10. Namespace and migration exclusions

F46 does not imply or authorize changes to:

```text
engine_version
schema_version
catalog_generation
campaign_contract_generation
storage_format_generation
install_layout_revision
ruleset digest generations
```

The F43 retained-schema matrix remains separate. Catalog generation remains at its separately audited current disposition; module revision numerics do not drive catalog generation.

Because this is an unreleased clean-slate v1 package, F46 introduces no compatibility aliases, dual-read paths or migrations for old CORE prose/module revisions.

## 11. Disposition

```text
AUTHOR_FINDING_46: SIGNIFICANT
ROOT_CAUSE: deterministic material CORE edits were left as worker-time version choices and two known shared CORE files lacked one final physical/version integration sink
DETERMINISTIC_CORE_CUTOVER_COUNT: 16
BOOTSTRAP_RUNTIME_FINAL_TARGET: 1.0.9
STORAGE_FINAL_TARGET: 1.0.2
DOUBLE_BUMP_PER_CONTRIBUTING_RD: FORBIDDEN
SPECULATIVE_BUMP_FOR_INSPECT_ONLY_MODULE: FORBIDDEN
NEW_RD: NO
NEW_SEMANTIC_OWNER: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```

F46 is author-side planning repair only. It does not constitute zero-open closure and does not unblock independent Senior review.