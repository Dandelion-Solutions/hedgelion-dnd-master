# R2.7 — Machine Realization Mapping & Holistic Architecture Closure — Task Brief

Status: **ACTIVE TASK BRIEF — R2.7 IN PROGRESS**

Date: 2026-08-24

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Depends on:

- all accepted Round-1 architecture;
- Step-4 single-context canonical amendment;
- R2.1 continuity/history-aligned projections;
- R2.2 Actor continuity/cognition/relationships;
- R2.3 Context Runtime/retrieval/allocation;
- R2.4 TurnEnvelope/instruction/Chronicler execution contract;
- R2.5 multiplayer collaboration and two-level Dramaturg coordination;
- R2.6 MVP host-assurance contract;
- Step-5 persistence/durability/recovery/concurrency/emission owners.

No broad implementation is authorized by this brief.

---

# 1. Purpose

R2.7 is the final Round-2 architecture stage.

Its job is to answer:

> **Where, exactly, does every accepted semantic responsibility live in the shipped runtime, persistent formats, transient HOT/SQLite realization, indexes, catalogs, instructions, tooling and tests — without creating duplicate owners or inventing new architecture merely because machine mapping exposes implementation detail?**

R2.7 is not a new semantics stage.

A prior accepted decision may be reopened only under the Round-1/Round-2 preservation rule:

1. mapping exposes a real contradiction or impossible realization;
2. a concrete consumer is unsatisfied;
3. two accepted owners overlap incompatibly;
4. the selected host/machine topology makes the accepted contract insufficient.

Otherwise, R2.7 maps rather than redesigns.

---

# 2. Required output shape

The primary R2.7 result is a **machine-realization responsibility matrix** that traces accepted semantics into concrete implementation surfaces.

For each material responsibility/record/result family, map where applicable:

```text
semantic owner / authority
    -> shipped runtime CORE owner(s)
    -> persistent native representation
    -> durable root/path
    -> stable identity policy
    -> flat vs deterministic sharded layout
    -> monolithic index owner/path
    -> discovery metadata / currentness route
    -> HOT / SQLite realization
    -> transient typed result/schema
    -> durability/publication behavior
    -> Project Instructions / host instruction obligation
    -> DEV machine catalog/schema obligation
    -> migration/seed/template obligation
    -> executable regression tests
    -> production-like MVP acceptance cases
```

Not every semantic concept needs every row. Absence must be explicit where material, e.g. `NO DURABLE RECORD`, `NO SQLITE OWNER`, `INSTRUCTION ONLY`, `DERIVED INDEX ONLY`.

---

# 3. Task-specific Source Manifest

R2.7 must build and exhaust the relevant dependency subgraph before any canonical coverage claim.

## 3.1 Process / sequencing

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 3.2 Canonical architecture owners

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` only as locator;
- all owning Round-1 canonical specs implicated by persistence, execution, role/context, Story, multiplayer, delivery/recovery;
- Step-4 single-context canonical amendment;
- R2.1-R2.6 canonical specs/resolution gates/owner decisions;
- current durable architecture docs under `DEV/ARCHITECTURE/` where they own machine contracts.

## 3.3 Shipped runtime owners

At minimum inspect relevant current modules under `GAME/CORE/`:

- `CORE_INDEX.md`
- `RUNTIME.md`
- `AI_REASONING.md`
- `PLAY_POLICY.md`
- `INFORMATION.md`
- `NPC.md`
- `PREP.md`
- `NARRATIVE.md`
- `GM_CRAFT.md`
- `STORAGE.md`
- `PERSISTENCE.md`
- `DURABILITY_GUARD.md`
- `SAVE_CONTRACT.md`
- `INTEGRITY.md`
- `SESSION.md`
- `MULTIPLAYER.md`
- `LIVE_SCENE.md`
- `CHRONOLOGY.md`
- `PROCESSES.md`
- `RANDOMNESS.md`
- other domain modules only where the ownership matrix proves them consumers.

## 3.4 Persistent runtime schemas / campaign template

- all current `GAME/SCHEMA/*.schema.yaml` families implicated by accepted semantics;
- `GAME/CAMPAIGN/` root/template layout;
- `GAME/TOOLS/init_campaign.py` where seed/bootstrap realization matters;
- `GAME/MIGRATIONS/` conventions;
- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and paired install/runtime instruction source.

## 3.5 DEV machine contracts

- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `CATALOG_INVENTORY.md`
- `ENTITY_STRUCTURES.md`
- `CATALOG_RESOLUTION.md`
- `ACTIVITY_MODEL.md`
- `RULE_ELEMENT_MODEL.md`
- Actor/Asset architecture where needed;
- `DEV/CATALOG/*.json`;
- relevant `DEV/SCHEMAS/*.schema.json`;
- current identifier policies;
- current maintenance/audit/release constraints.

## 3.6 Tests/evaluation

- relevant `DEV/TESTS/test_*.py`;
- relevant `DEV/TESTS/*_CASES.md`;
- Step-5/Round-2 adversarial cases;
- Protocols 1-3 promoted behavioral conclusions;
- R2.6 Protocol-4 scenario inventory/frozen-fixture contract as **post-implementation acceptance input**, not a pre-R2.7 execution gate.

## 3.7 Private Lab evidence boundary

HDM Lab may be consulted for private exploratory evidence where necessary, but public R2.7 artifacts must retain only sanitized, independently rewritten conclusions/test obligations.

Exploratory probes/prototypes/instrumentation belong in Lab by default.

---

# 4. Required mapping domains

## 4.1 Authority / duplicate-owner matrix

For every accepted current-state, derived-state, operational and planning responsibility, establish exactly one semantic owner or an explicit derived/non-authoritative relation.

Mandatory cross-checks include:

- durable native files vs HOT/SQLite;
- current owner vs derived index/cache;
- Story vs canonical history/current state;
- Actor source continuity vs `world.knowledge`;
- player disclosure vs PC knowledge;
- local/shared Dramaturg planning vs canon;
- collaboration/generation state vs gameplay consequence;
- session metadata vs currentness/gameplay authority;
- LIVE scene state vs campaign durable frontier;
- deterministic acceptance vs LLM proposal/narration.

No duplicate semantic owner may survive closure.

## 4.2 Persistent record families and roots

Map all durable/current campaign families to exact physical roots.

This stage owns the exact family mapping deferred by R2.3, including which high-cardinality file-per-record families are deterministically sharded.

Current constraints:

- stable ID remains semantic identity; path is routing only;
- current per-type `*_INDEX.yaml` files remain **monolithic single-file indexes**;
- index partitioning/sharding remains dormant until the accepted measured trigger fires;
- ordinary exact lookup must not enumerate a large sharded directory;
- naturally small collections remain flat unless a concrete reason says otherwise.

Candidate high-cardinality families to resolve, not blindly assume:

- semantic LOG/history events;
- durable NPC Actor records;
- items/assets where file-per-record/high-cardinality applies;
- knowledge/event-like families if represented file-per-record;
- scene records only if actual expected cardinality justifies it;
- other world families based on current contracts/scale semantics.

R2.7 must specify deterministic shard arithmetic/routing for every sharded family.

## 4.3 Index realization

For each index family:

- semantic purpose;
- projection/source basis;
- monolithic path;
- rebuild/audit behavior;
- currentness rules;
- permitted compact discovery metadata;
- prohibited secret-bearing/authority-bearing fields;
- relationship to sharded durable roots.

Index omission must not silently become semantic absence unless the owning contract explicitly grants exhaustiveness.

## 4.4 HOT / SQLite mapping

Resolve the current physical SQLite/HOT realization without creating a second canon.

For each relevant table/log/cache/projection:

- semantic owner represented;
- current vs cache/derived status;
- hydration source;
- dirty/publication state;
- transaction/CAS role;
- loss/recovery consequence;
- durable materialization target;
- indexes/query acceleration;
- whether the structure is rebuildable/disposable.

Preserve the established law:

> SQLite format creates no authority. HOT may contain newer current SOFT owner state than the durable Git frontier, but caches/indexes/projections never outrank their owning semantic source.

Exact SQLite table layout is owned here only to the degree needed for implementation planning and schema/test mapping.

## 4.5 Context Runtime / typed operational results

Map R2.3/R2.4 logical results into concrete machine contracts, including as applicable:

- `RoleContextRequest`;
- `ContextNeedProfile`;
- candidate/discovery records;
- required packet closure representation;
- `RoleContextBundle`;
- `ContextTrace`;
- `ASSEMBLED` / `ASSEMBLED_DEGRADED` / `UNSATISFIABLE`;
- `TurnEnvelope` phase records where any machine representation is actually required;
- minimal Interpreter/Dramaturg/Actor/Chronicler/Narrator handoffs.

Do not persist hidden chain-of-thought or create durable phase state merely for inspectability.

Do not require the LLM to emit large strict transport JSON in the hot loop; deterministic Python/core owns serialization/validation/bookkeeping.

## 4.6 Actor continuity / relationships / knowledge

Map R2.2 into current `npc`/actor/knowledge schemas and runtime surfaces:

- source-Actor non-epistemic continuity;
- foundation/durable evolving/transient private lifetimes;
- directed relationship facets;
- sparse cognition / `NO_CHANGE`;
- current `world.knowledge` ownership for proposition stance;
- player-owned voluntary PC mental state;
- lazy discovery/index hints that do not require full Actor load.

Do not duplicate knowledge state inside Actor records merely for convenience.

## 4.7 Story / Chronicler

Map Step-5.10/R2.1/R2.4 into concrete:

- Story layer roots/coverage/projection state;
- source-basis tracking;
- bounded catch-up realization;
- Chronicler activation/service decision representation if any;
- deterministic vs generative Story transform boundary;
- no same-envelope feedback;
- no Story scheduler/job queue unless a later trigger fires;
- same-ref gameplay priority/yield behavior;
- post-implementation anti-starvation tests.

Story remains durable noncanonical projection, not gameplay authority.

## 4.8 Multiplayer collaboration / agency-safe progression

Map R2.5 into concrete records and currentness routes for:

- `INDEPENDENT_IMMEDIATE`;
- `AGENCY_DEPENDENT_COLLECTIVE`;
- `RULE_OWNED_ORDERED`;
- positive material agency dependency evidence;
- maximal safe frontier;
- scoped collaboration obligation/window;
- required/optional contributors;
- contribution identity and purpose/scope/generation binding;
- stale/superseded generation behavior;
- join/rejoin/current route/admission/catch-up;
- external coordination without third-party PC authority.

The collaboration layer may own collection/generation, not gameplay consequence or fictional chronology.

## 4.9 Two-level Dramaturg planning

Map the R2.5 S14 activation into concrete machine/runtime surfaces:

```text
singleplayer
    player-local Dramaturg planning only

multiplayer
    shared noncanonical Dramaturg horizon
    + player-local Dramaturg horizons
```

Resolve:

- physical root(s);
- stable identities/generation semantics;
- current-generation/exact-base fencing;
- shared-horizon CAS/rebase behavior;
- local/shared discovery metadata;
- lazy loading and relevance routing;
- source-anchored constraint vs provisional direction representation;
- retention/invalidation/rebase rules;
- transition multiplayer -> singleplayer and singleplayer -> multiplayer;
- Story vs prospective-planning separation;
- recipient secrecy and post-MVP acceptance coverage.

Hard law:

> Preparation has no entitlement to occur. Canon invalidates preparation, never vice versa. Shared coherence constrains preparation, not player/Actor freedom.

## 4.10 Instruction architecture / CORE mapping

R2.7 must identify exact shipped instruction owners for accepted behavior without duplicating giant prompts.

Mandatory mapping includes the R2.6 MVP rule:

```text
ineligible now -> do not materially use/disclose
lawfully eligible later -> may use normally
```

Candidate owners to inspect rather than assume:

- `AI_REASONING.md` for always-active correctness/role eligibility;
- `INFORMATION.md` for knowledge/disclosure semantics;
- `NPC.md` for Actor-local use;
- `PREP.md` for Dramaturg planning constraints;
- `NARRATIVE.md` for Narrator/recipient emission;
- `PLAY_POLICY.md` / `CORE_INDEX.md` for activation/routing;
- Project Instructions for host-level orchestration boundaries.

R2.7 should prefer one strong owning rule plus module-local application notes over duplicated prose in every CORE file.

## 4.11 Project Instructions / bootstrap / forbidden transport behavior

Map the fixed runtime transport and host profile into shipped installation/Project Instructions.

Known wording debt must be resolved in mapping:

- `gh`, remote native Git, direct private API/token workarounds and alternative runtime transports are forbidden, not merely “do not try first”;
- missing Connector capability is a supported-profile failure;
- ordinary campaign repository operations use only the approved Python/core + Connector path.

Exact edits happen during implementation, not in this architecture stage.

## 4.12 Tests / evaluation / release-readiness mapping

Every material law introduced or materially extended in R2.1-R2.6 must map to:

- deterministic unit/contract tests where machine-checkable;
- integration tests where runtime state/persistence is involved;
- scenario/adversarial cases where semantic classification is required;
- production-like ChatGPT evaluation where LLM behavior is the thing being tested.

Protocol-4-derived post-MVP acceptance scenarios must receive durable test IDs/owners in R2.7.

MVP release/readiness may not claim supported behavioral containment until the implemented acceptance suite runs and material failures are resolved/classified.

---

# 5. Holistic closure review

R2.7 must perform a cross-round composition pass, not merely create a mapping table.

At minimum verify:

1. no duplicate semantic owner;
2. no circular currentness/authority dependency;
3. no durable projection self-promotes to canon;
4. no derived index/cache becomes closed-world proof accidentally;
5. retry/narration/Story failure cannot replay accepted mechanics/RNG;
6. Git/host arrival order cannot become fictional chronology;
7. human disclosure remains recipient-scoped and separate from PC knowledge;
8. multiplayer collaboration cannot authorize absent PC voluntary action;
9. shared Dramaturg planning cannot become plot authority;
10. Story and prospective Dramaturg planning remain distinct;
11. HOT/SQLite vs durable Git frontier semantics are unambiguous;
12. monolithic indexes and sharded record roots compose without directory enumeration hot paths;
13. migrations/bootstrap/seeds can construct every required persistent owner;
14. every deferred/dormant trigger remains preserved without accidental activation;
15. no R2.6 post-implementation evaluation obligation disappears during mapping.

---

# 6. Diamond / Strong completeness

R2.7 is the final Round-2 coverage gate.

Before canonical closure, recheck all 82 original DIAMOND/STRONG items plus later narrow activation changes:

- inherited/satisfied remains satisfied in machine mapping;
- active items have concrete implementation/test destinations;
- dormant items retain exact revisit triggers;
- rejected/negative constraints remain protected by tests or explicit non-goals where material;
- S14 narrow multiplayer activation is mapped without expanding into generic Narrative Dynamics;
- S53 capability-envelope result is mapped without exact-model persistence;
- D15 remains dormant unless its trigger has actually fired.

Coverage does not activate dormant work.

---

# 7. Expected decision gates

R2.7 may expose owner decisions only where machine realization leaves multiple materially different viable semantics/cost profiles.

Likely areas to investigate before deciding whether a human gate is needed:

- exact physical record-family roots/sharding for newly mapped durable families;
- exact retained planning persistence shape where several representations satisfy R2.5;
- exact SQLite/HOT physical organization where it materially affects durability/recovery/performance rather than being replaceable implementation detail;
- any persistent schema compatibility/migration choice with meaningful product cost;
- any instruction placement choice that changes product behavior rather than merely wording/organization.

Do not escalate replaceable implementation detail as a product decision.

---

# 8. Exit criteria

R2.7 closes only when:

1. the task-specific Source Manifest is complete enough for a final Round-2 coverage claim;
2. every accepted R2.1-R2.6 semantic responsibility has a concrete machine/instruction/test destination or explicit `NO ...` disposition;
3. durable record families have exact physical roots/layout/index policies;
4. all required sharded families have deterministic routing arithmetic and monolithic-index interaction defined;
5. HOT/SQLite authority/currentness/dirty/publication roles are concretely mapped;
6. Context Runtime/TurnEnvelope/minimal handoff machine boundaries are mapped without hidden-CoT persistence or large LLM transport JSON;
7. Actor continuity/knowledge/relationship ownership is concretely mapped without duplication;
8. Story/Chronicler physical realization is mapped without scheduler/job-queue authority creep;
9. multiplayer collaboration/current-generation/maximal-safe-frontier realization is mapped;
10. local/shared Dramaturg planning persistence/discovery/CAS/rebase/lifecycle is mapped;
11. exact CORE/Project-Instructions responsibility is mapped, including behavioral containment + lawful uptake and fixed-transport prohibition;
12. Protocol-4-derived implemented-MVP acceptance obligations have durable test/evaluation owners/IDs;
13. migrations/templates/bootstrap implications are explicit;
14. holistic duplicate-owner/currentness/retry/recovery/history/multiplayer composition review passes;
15. all 82 DIAMOND/STRONG items plus later activation changes are disposition-rechecked at machine/test level without manufacturing dormant work;
16. stale derivative/status/documentation references that would misroute implementation are identified for repair;
17. any genuine owner trade-offs are resolved;
18. implementation-planning entry criteria are explicit;
19. broad implementation has not started before architecture closure.

---

# 9. Immediate next activity

```text
build R2.7 Source Manifest from current owning artifacts
    -> construct semantic-owner -> machine-surface matrix
    -> resolve physical persistent/HOT/index/instruction/test mapping deltas
    -> adversarial holistic composition review
    -> owner decisions only for genuine machine-realization trade-offs
    -> canonical mapping / final Round-2 resolution gate
    -> implementation planning
```

Broad implementation remains **BLOCKED**.
