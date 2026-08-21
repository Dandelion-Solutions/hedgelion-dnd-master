# Step 1 Retrospective Assurance — Slice 0B Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — ONE MATERIAL DECISION CANDIDATE IDENTIFIED**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed:

- Slice 0B solution-blind Task Charter;
- Slice 0B coverage/research synthesis;
- current catalog strata/ID/version contracts;
- campaign engine/checkpoint identity and same-version update policy;
- Step-1 no-universal-override and stable-ID decisions.

## 1. Verdict

The research correctly identifies two real omissions:

1. `engine -> ruleset -> campaign -> session` is not sufficient unless duplicate-ID behavior is explicit;
2. durable plain `definition_id` references need one resolved catalog context/snapshot compatibility boundary rather than relying on ambient files/model memory.

The recommended package-level snapshot is stronger than per-record versions or layered shadowing. However, the critic finds one material semantic question hidden inside the duplicate-ID recommendation:

> How does a campaign intentionally change the meaning of an existing shipped ruleset definition such as a spell, item, class feature, or monster archetype?

That question must be answered before globally rejecting all same-ID campaign overrides is canonicalized.

## 2. Confirmed findings

### 0B-C1 — `resolution order` must not remain ambiguous

**Severity: BLOCKING ambiguity if left unspecified.**

A plain ID cannot safely be both stable semantic identity and subject to implicit last-layer-wins replacement. Loader behavior must be one of:

- reject duplicates;
- explicitly compose/patch them under a typed mechanism;
- resolve a prebuilt/forked package before the catalog is loaded.

It must never depend on path order or generic scope precedence.

### 0B-C2 — a logical ResolvedCatalogContext is required

**Severity: SIGNIFICANT.**

The critic narrows the recommendation: Step 1 does **not** need to create a new world/runtime record called `ResolvedCatalogSnapshot` today. It needs a normative logical contract:

```text
ResolvedCatalogContext
    = engine capability contract identity
    + selected ruleset package identity/set
    + campaign-definition frontier
    + optional session overlay frontier
```

Every loader/binder/Resolution operates against one such context. Durable state/checkpoints must retain enough package/frontier identity to reconstruct a compatible durable context. Step 6 may choose exact ruleset package manifest/storage fields; Step 5 may decide checkpoint publication mechanics.

This avoids prematurely inventing another persistent entity while preserving the required authority boundary.

### 0B-C3 — same-version refresh compatibility must include catalog semantics

**Severity: SIGNIFICANT.**

The current same-version engine refresh rule uses source ancestry as evidence of forward maintenance compatibility. That is insufficient if a descendant can incompatibly mutate the closed capability contract or existing shipped definition meaning.

Required architecture invariant:

```text
same-version runtime refresh is permissible only inside the same declared
catalog/capability compatibility line;
source ancestry is necessary provenance evidence, not semantic compatibility.
```

Exact release tooling/version field is later implementation. Existing Step-6 migration/catalog-gap closure is the natural owner for package compatibility validation.

### 0B-C4 — session definition promotion should preserve semantic definition ID

**Severity: MODERATE.**

Because reusable definitions already use semantic namespaced IDs rather than campaign allocators, a session definition promoted to campaign scope should normally keep the same ID. Its storage/origin changes; semantic identity does not. Collision or invalid campaign namespace causes explicit promotion failure/migration.

World `local-*` IDs continue to rekey separately.

### 0B-C5 — package namespace ownership is required but can remain package metadata

**Severity: MODERATE.**

The loaded ruleset/campaign package context must own permitted definition namespaces. This need not become a field on each definition. The loader rejects definitions outside the package's namespace declaration and rejects duplicate resolved IDs.

## 3. Material customization question

### Problem

Suppose the selected D&D ruleset defines:

```text
srd.spell.fireball
```

and a campaign house rule wants Fireball to use different damage, target rules, or another reusable semantic property.

Three credible models exist.

### Alternative A — campaign-layer same-ID shadowing

```text
ruleset:  srd.spell.fireball = RAW
campaign: srd.spell.fireball = house-rule version
```

**Benefit:** very convenient; existing references automatically observe the campaign variant.

**Costs/failure modes:**

- semantic meaning of an unchanged durable ID depends on ambient layer ordering;
- removing the campaign override silently changes every reference back;
- provenance/debugging must answer which layer supplied the definition;
- snapshots must preserve every shadow relation;
- session-local same-ID edits could silently alter mechanics;
- stale LLM/catalog caches become much harder to validate;
- generic shadowing becomes an undeclared override/inheritance mechanism already rejected by Step 1.

**Critic verdict:** not recommended.

### Alternative B — new campaign definition ID + explicit reference migration

```text
campaign.spell.fireball_house
```

Any actor/build/feature/rules package reference that should use the house version must explicitly refer to the new ID or be migrated.

**Benefits:** strongest identity semantics; no ambient override; easy audit.

**Costs:** global campaign changes to ubiquitous standard content may require broad reference migration or a higher-level rules policy; authoring friction can be significant.

**Critic verdict:** safe but possibly too cumbersome as the only customization mechanism.

### Alternative C — selected ruleset package/fork resolves customization before IDs enter the runtime catalog

The campaign selects one resolved ruleset package/snapshot whose internal definition IDs remain stable. A house-rule customization of shipped definitions creates or derives a new **ruleset package identity/snapshot** rather than a layer-shadow record.

Conceptually:

```text
ruleset package DND-2024-SRD@5.2.1
    srd.spell.fireball -> RAW

campaign-derived ruleset package DND-2024-SRD+campaign-X@R17
    srd.spell.fireball -> house-rule definition
```

Only one definition with that ID enters a given ResolvedCatalogContext.

**Benefits:**

- preserves plain stable IDs within one context;
- ubiquitous references do not need migration merely because the selected rules profile changed;
- exact package/snapshot identity records the changed semantics;
- no runtime shadowing or per-record version fields;
- compatible with future custom rulesets.

**Costs:**

- introduces a ruleset package/fork concept and package-level derivation/compatibility tooling;
- a campaign house rule that changes ruleset definitions becomes part of rules-package state rather than an isolated overlay object;
- Step 6 must own package construction/migration and avoid copying an entire SRD package unnecessarily.

**Critic verdict:** recommended for true modifications of existing reusable ruleset definitions, while Alternative B remains appropriate for genuinely new campaign content.

## 4. Strongest counterargument to Alternative C

HDM may be overengineering a package system for a single D&D ruleset. A simple campaign overlay with deterministic precedence is much easier to author and has decades of precedent in configuration systems/mod loaders.

The response is project-specific: HDM's LLM authoring boundary and durable plain IDs make ambient overrides unusually risky. A model can produce a plausible same-ID object, and a silent overlay would immediately change executable meaning across existing references. A package/fork boundary makes such a semantic change explicit and auditable.

Still, the cost is real: if house-rule editing of existing standard definitions is expected to be frequent and user-facing, package derivation ergonomics become a product concern rather than a purely technical detail.

## 5. Simplest viable alternative

If the project does not need direct mutation of shipped definitions during ordinary campaign play, the simplest safe initial rule is:

```text
- resolved definition IDs are unique; duplicates fail;
- campaign layer is additive only;
- new campaign content receives new IDs;
- global house rules are represented through existing policy/Feature/Rule Element
  mechanisms where possible;
- true ruleset-definition replacement is deferred to Step 6 ruleset-package
  migration/fork design.
```

This preserves the option for Alternative C without implementing package forks now.

## 6. Recommendation

The critic recommends **not** introducing runtime shadowing.

Canonicalize now:

1. one ResolvedCatalogContext per loaded execution state;
2. globally unique definition IDs inside that context;
3. duplicate IDs across loaded sources are validation errors;
4. layer order is assembly/dependency order, not override precedence;
5. same-version maintenance cannot incompatibly alter existing catalog semantics;
6. session definition promotion normally preserves semantic ID;
7. package namespace ownership belongs at package/context level.

Defer the exact package/fork implementation to Step 6, but record the intended direction:

- new campaign content -> new campaign IDs;
- modifications of existing standard reusable definitions -> existing typed house-rule mechanics when sufficient, otherwise a future explicit ruleset-package/fork/migration mechanism, **not implicit shadowing**.

## 7. Does this require a human decision now?

**Critic assessment: probably NO**, provided the human has not established a product requirement that campaign authors must be able to transparently replace any shipped definition by reusing its ID.

The current accepted architecture already says:

- IDs are stable and not silently repurposed;
- definitions have no universal inheritance/override mechanism;
- executable semantics are closed;
- campaign content may add/compose validated data.

Therefore rejecting implicit same-ID shadowing is the consistent interpretation of existing decisions rather than a new reversal.

A human gate is required only if transparent same-ID house-rule replacement is a desired product semantic.

Recommendation: **AMEND / KEEP STEP 1 CLOSED**.

Confidence: **HIGH** on unique resolved IDs and ResolvedCatalogContext; **MEDIUM-HIGH** that package-fork implementation can safely wait until Step 6.
