# Step 1 Retrospective Assurance — Slice 0B Task Charter: Catalog Evolution, Identity, Strata and Discoverability

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct the minimum evolution/identity/discovery contract required for an HDM catalog that must survive engine upgrades, ruleset packages, campaign extensions, local/session authoring, promotion, migration, LLM lookup, and durable references.

This charter asks what guarantees are required over time and across catalog scopes before judging the accepted engine/ruleset/campaign/session strata, ID policy, version placement, promotion model, seed boundary, or catalog-gap behavior.

## 2. System context

HDM has several unusual constraints:

- deterministic code executes only registered mechanics;
- an LLM may create ordinary campaign content and semantic names dynamically;
- campaigns outlive one chat/process and can outlive an engine version;
- standard ruleset definitions and campaign definitions coexist;
- session-local content may become durable later;
- durable world records may reference definitions created at different scopes;
- a limited context window requires bounded search/hydration rather than prompt-memory authority;
- multiplayer/publication later introduces concurrent frontiers;
- a catalog upgrade must not silently change the meaning of existing durable references;
- full SRD seed population is separate from engine capability semantics.

## 3. Problem statement

Define a catalog evolution contract that can answer deterministically:

```text
Which package/scope owns this definition ID?
Which definition wins if multiple loaded sources use the same ID?
May a higher scope replace, shadow, extend, or merely add definitions?
What does a durable definition reference mean after an engine/catalog upgrade?
How is a local definition promoted without changing semantic identity unexpectedly?
How are its dependent local world records/references handled?
What happens if a referenced definition disappears or changes incompatible kind/schema?
How does the LLM discover relevant definitions/capabilities without knowing the whole catalog?
How is a genuinely unsupported mechanic distinguished from an undiscovered existing one?
What version information must be durable, and at what owner level?
```

The design must prevent both:

1. **semantic drift** — an old ID resolves to new incompatible meaning;
2. **catalog fragmentation** — every record copies versions/source metadata or every campaign forks the entire ruleset package.

## 4. Goals

The catalog evolution layer must provide at least:

1. stable definition identity within a resolved catalog snapshot;
2. explicit namespace/ownership rules preventing accidental ID collision;
3. deterministic load/resolution order with defined collision behavior;
4. no silent repurposing of an existing machine or reusable definition ID;
5. explicit compatibility/migration behavior across engine/catalog/schema changes;
6. a selected ruleset package identity/version sufficient to interpret durable references;
7. campaign extensions that can add content without editing engine/ruleset sources;
8. session-local definitions/entities that may stay local or be promoted;
9. promotion closure ensuring durable records cannot depend on unpublished local definitions/entities;
10. stable lineage/provenance sufficient to audit rekey/promotion/migration without making lineage a second identity;
11. a clear seed boundary: engine capabilities versus standard ruleset definitions versus campaign data;
12. catalog-gap behavior that reports missing executable semantics rather than inventing them;
13. bounded typed discovery/hydration for LLM interpretation and authoring;
14. discovery that distinguishes capabilities from content definitions and respects visibility/knowledge policy where applicable;
15. deterministic failure for stale/missing/incompatible references;
16. upgrade behavior that preserves explicit option value rather than forcing universal per-record versions.

## 5. Non-goals

Slice 0B does not finalize:

- exact Step-3 natural-language binder protocol;
- Step-4 secret/knowledge disclosure policy;
- Step-5 Git publication/multiplayer merge mechanics;
- Step-6 complete SRD package content;
- migration implementation code or database layout.

It must determine the minimum earlier contracts those stages require.

## 6. Required questions

### Package and namespace ownership

- Is a definition ID globally unique across engine/ruleset/campaign/session, or unique only within a package?
- What prevents two packages from claiming the same semantic namespace?
- Is the namespace part of stable identity or only a lookup convenience?
- Can a campaign intentionally replace a ruleset definition with the same ID? If yes, what compatibility rules prevent semantic drift? If no, how is customization represented?

### Resolution order

- What exactly does `engine -> ruleset -> campaign -> session` mean: additive search, shadowing, override, fallback, or source priority?
- Are duplicate IDs rejected or resolved by priority?
- Can two selected ruleset packages coexist?
- Can a session definition refer to campaign/ruleset definitions? Can the reverse direction ever be durable?

### Version ownership

- Which object identifies the loaded engine capability version?
- Which object identifies the selected ruleset definition package/version?
- Which object identifies campaign schema/content compatibility?
- When is one catalog-wide version sufficient, and when would package-level versioning be required?
- How does a checkpoint prove which definition snapshot a durable `definition_id` referred to?

### Compatibility and migration

- Which changes are additive and safe without migration?
- Which changes require catalog version bump only?
- Which changes require campaign migration?
- What happens when an ID keeps its spelling but changes kind or semantics?
- Can a definition be removed while durable records still reference it?
- How are old campaign-created definitions validated after engine capability changes?

### Local authoring and promotion

- Does promotion preserve the same logical identity while changing storage ID, or create a new durable identity with lineage?
- What happens to direct references during rekey?
- What if a durable publication depends on a local definition and local world record recursively?
- Can promotion discover/reference dependencies without a campaign-global scan?
- How are conflicting allocations/IDs resolved under later concurrency?

### LLM discovery and catalog gaps

- How does runtime search by natural-language semantics, facets, tags, kinds, applicable capability, and bounded context?
- What minimum typed candidate metadata does the LLM receive?
- What prevents search rank from becoming mechanical authority?
- How does runtime distinguish `not found because not hydrated/searched correctly` from `known catalog gap`?
- How are newly authored campaign definitions indexed for subsequent lookup?
- Can the LLM propose a definition ID, or must every executable/reference ID originate from bounded candidate lookup/validated creation?

## 7. Failure scenarios

The accepted architecture must survive at least:

1. ruleset package v2 removes a spell definition referenced by a durable Actor/Asset;
2. a definition ID retains the same string but changes from `definition.asset` to another kind;
3. two packages define the same ID differently;
4. a campaign wants a modified Fireball without altering the shipped ruleset record;
5. a session-local custom artifact is promoted after several local Effects/Assets already reference it;
6. local and durable records form a dependency chain during promotion;
7. two concurrent writers independently allocate/promote local records;
8. an old campaign is opened under a newer engine whose capability registry no longer accepts one embedded Rule Element;
9. the LLM remembers an old catalog ID that is no longer loaded;
10. semantic search returns a similarly named but mechanically incompatible candidate;
11. the catalog contains the needed capability but the current bounded search missed it;
12. the desired mechanic genuinely requires Python/registry extension;
13. a campaign definition refers to another campaign definition that is later retired/replaced;
14. a snapshot/checkpoint survives while the working-tree ruleset package has advanced;
15. a definition is renamed for presentation but semantic identity should remain stable;
16. a definition's human-readable name collides across languages while machine identity stays distinct;
17. a custom future ruleset wants to coexist with D&D vocabulary without accidental namespace collision.

## 8. Quality attributes / fitness criteria

### Semantic stability

- durable references never silently resolve to incompatible meaning;
- ID spelling alone is not enough to authorize executable behavior after an incompatible package/engine change;
- no implicit override based on filesystem order.

### Extensibility

- campaigns can add ordinary data without copying/forking the ruleset;
- local experimentation is cheap;
- genuine new executable semantics remain explicit engine work.

### Recoverability

- a restored checkpoint can identify the compatible catalog snapshot/package set needed to interpret its references;
- missing dependencies fail explicitly rather than being regenerated by the LLM.

### Performance

- lookup/hydration is bounded and indexed;
- promotion/rekey cost scales with known dependency closure, not the entire campaign;
- catalog startup validation may be broader than per-action lookup but remains deterministic.

### LLM safety/usability

- LLM receives compact semantic candidates, not unbounded raw catalog dumps;
- names/tags/rank guide selection but do not bypass deterministic kind/capability validation;
- stale model memory cannot substitute for a loaded catalog candidate.

### Migration

- incompatible changes have a named owner and migration path;
- no per-record version fields are added merely to avoid defining package/snapshot compatibility;
- old meaning remains recoverable or failure is explicit.

## 9. Done criteria

Slice 0B is assured only when:

- package/scope/namespace identity and collision behavior are explicit;
- load/resolution semantics are unambiguous;
- durable catalog snapshot/version ownership is sufficient for restoration;
- promotion semantics and dependency closure are coherent;
- seed/capability/campaign boundaries remain non-duplicative;
- LLM discovery/gap behavior has a safe minimum contract;
- incompatible upgrade cases have explicit failure/migration semantics;
- an adversarial review finds no unowned Step-1 blocker.
