# Step 1 Retrospective Assurance — Slice 0A Task Charter: Catalog Meta-Model and Class Boundaries

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct what an HDM catalog/meta-model must accomplish before judging the accepted class inventory, registries, facets, definition/world/runtime split, or machine catalog.

This charter asks **what categories and boundaries the engine needs**, not whether the current catalog already has the right ones.

## 2. System context

HDM is an engine where:

- an LLM interprets informal natural language and creates/extends fictional content;
- deterministic Python/runtime code owns executable mechanics and validation;
- reusable D&D/ruleset/campaign content must be describable as validated data;
- particular campaign entities/facts have identity and mutable lifecycle;
- active execution has operational state that is neither reusable content nor ordinary world canon;
- some typed values exist only while a request/calculation is in flight;
- definitions and instances may begin session-local and later become durable;
- the engine must support official D&D/SRD content plus campaign-specific and future ruleset content without requiring Python changes for ordinary data extensions;
- a limited context window means LLM use must depend on bounded discovery/hydration rather than memorizing all known content.

## 3. Problem statement

Define the minimum classification/meta-model that lets HDM answer, for any concept it encounters:

```text
What kind of thing is this?
Does it need stable identity?
Does it have independent lifecycle/state?
Is it reusable or an instance?
Does it carry executable engine semantics or only compose registered semantics?
Can campaign/LLM content create it?
Can it be stored durably?
Can it be searched as content?
What validates it?
Who may interpret/change it?
```

The catalog must prevent two opposite failures:

1. **under-modeling** — unrelated semantics collapse into generic blobs/classes that require runtime guessing or LLM interpretation;
2. **over-modeling** — every domain noun becomes a new engine class/entity/capability, producing duplicate authority and an unmaintainable taxonomy.

## 4. Goals

The meta-model must support at minimum:

1. closed executable engine semantics that content cannot invent;
2. reusable validated rules/content assembled from those semantics;
3. particular world identities with mutable state and provenance;
4. execution/operational records whose lifecycle is different from world entities;
5. transient typed request/result/calculation values that need schemas but not independent record identity;
6. classification of cross-cutting concepts without forcing single inheritance;
7. stable machine identifiers and unambiguous dispatch/validation ownership;
8. campaign/ruleset extension without Python changes where no new executable semantics are needed;
9. explicit handling of genuinely missing engine capability rather than silent LLM improvisation;
10. bounded search/discovery suitable for LLM semantic mapping;
11. version/migration compatibility sufficient that old durable records do not change meaning silently;
12. progressive materialization: incidental fiction need not become fully structured mechanics until required;
13. promotion of local definitions/entities without changing their semantic identity unexpectedly;
14. clean separation between descriptive metadata and mechanics;
15. future custom mechanics/rulesets without requiring a universal scripting language.

## 5. Non-goals

Slice 0A does not need to finalize:

- concrete mechanics of HP/Effects/Resources (Step 2 assurance);
- exact execution transaction protocol (Step 3);
- lore disclosure/context policy (Step 4);
- Git publication/multiplayer recovery details (Step 5);
- complete SRD seed population (Step 6);
- exact storage tables or Python class implementation.

It **must**, however, identify minimum contracts those later stages depend on.

## 6. Core classification questions

For every candidate concept, the architecture must distinguish as needed:

### Executable semantics

- Does this concept introduce behavior the deterministic engine must implement?
- Can it be expressed by composing already-known operations/policies?
- What prevents an LLM/campaign file from inventing executable meaning under a plausible ID?

### Reusability versus instance

- Is the concept a reusable template/rules identity or one particular thing/fact in a campaign?
- Can several independent instances share one definition?
- Can a reusable definition have mutable campaign state, and if so is that actually a hidden world instance?

### Identity and lifecycle

- Does the concept need independent stable identity?
- Can it be created, transformed, removed, referenced, promoted, or have provenance separately from its owner?
- If not, should it be an embedded typed value instead of a record/class?

### World versus operational execution state

- Is this fact part of the fictional/mechanical world, or only state of executing/transporting/validating work?
- Does its lifetime survive a gameplay action, session, chat, or process?
- Can runtime-only state be continuity-critical without becoming world canon?

### Record versus transient value

- Does the concept need independent lookup/reference and durable identity?
- Or is it only a typed request/result/contribution/delta used inside another owner?

### Classification versus mechanics

- Is a category merely descriptive/searchable classification?
- Does selecting the category itself alter mechanics?
- What prevents tags/facets/names from becoming hidden executable rules?

## 7. Required extension tests

The accepted catalog must explain, without ad-hoc exceptions, how to classify at least these examples:

1. a standard spell definition;
2. one casting of that spell;
3. a spell's reusable Activity/procedure;
4. a temporary pre-commit damage result;
5. committed damage/event history;
6. an active target-local magical effect;
7. a named Condition referenced by rules;
8. a mundane sword definition and one particular sword;
9. an improvised weapon use of a chair without inventing a new engine class;
10. a unique campaign artifact with new combinations of existing mechanics;
11. a campaign feature whose desired mechanic cannot be expressed with existing capabilities;
12. a newly invented NPC mentioned once in narration;
13. that NPC becoming mechanically relevant later;
14. a scene/encounter/procedure state object;
15. an interaction/request/receipt/continuation;
16. a reusable terrain/environment/hazard concept versus one placed instance;
17. a party/group/faction/organization distinction;
18. physical currency versus abstract account balance;
19. an item transformation that preserves identity but changes valid definition-dependent state;
20. a local/session-created definition later referenced by durable world state.

## 8. Quality attributes / fitness criteria

### Semantic correctness

- one concept has one primary classification/authority;
- two classes do not independently represent the same mutable fact;
- reusable definitions are not confused with instances;
- transient/prospective values cannot be mistaken for committed world truth;
- descriptive classification cannot execute mechanics by itself.

### Extensibility

- adding ordinary campaign content normally uses data, not Python;
- adding genuinely new executable semantics is explicit and reviewable;
- a new domain noun does not automatically require a new engine class;
- a new independent lifecycle owner can be introduced without abusing an unrelated existing class.

### Determinism / safety

- unknown IDs and incompatible class/capability combinations fail deterministically;
- LLM output cannot create executable meaning merely through naming;
- dispatch does not depend on prose, filename, prompt memory, or ambiguous inheritance.

### LLM usability

- content search can return compact typed candidates with enough semantic metadata for mapping natural language;
- the model need not memorize the entire registry/seed;
- engine capabilities and content definitions are distinguishable in context so the LLM cannot treat both as equally inventable.

### Maintainability

- the class inventory has principled extension rules;
- machine-readable registry is the single selectable ID authority;
- human design documents do not need parallel manually synchronized enumerations to remain correct;
- invalid combinations can be rejected by schema/compiler validation rather than runtime guesswork.

### Performance

- class/kind dispatch and relevant discovery are bounded/indexable;
- normal gameplay does not require loading/searching every definition or world record;
- taxonomy does not force unnecessary materialization/entities/joins for simple content.

### Migration/versioning

- an existing machine ID cannot silently change semantic class/meaning;
- class-boundary changes have an identifiable migration consequence;
- durable records remain interpretable across engine/catalog upgrades or fail explicitly.

## 9. Failure scenarios the accepted design must survive

1. The LLM invents `activity.disintegrate_everything` as if it were an engine capability.
2. A campaign creates a valid new artifact by composing existing mechanics.
3. A campaign needs a mechanic no registered capability can express.
4. One concept appears simultaneously as a definition, world record and runtime object with similar names; the engine must not confuse their authority.
5. A transient calculation result is accidentally persisted as canonical truth.
6. A runtime continuation survives a crash although it is not a world entity.
7. A session-local definition becomes referenced by a durable entity.
8. An entity changes definition/type and some old state is invalid for the new definition.
9. A tag/facet is accidentally treated as a mechanical permission.
10. A new D&D feature crosses several descriptive categories but has one mechanical payload.
11. Two ruleset packages define the same machine/content ID incompatibly.
12. A catalog upgrade removes/renames/repurposes a referenced ID.
13. An old snapshot is loaded with a newer engine where class taxonomy changed.
14. A content-search result includes runtime records or secret/non-searchable state as if it were reusable content.
15. A ubiquitous lightweight concept is modeled as a standalone entity, creating huge join/index/lifecycle overhead without independent identity need.
16. A concept with independent provenance/lifecycle is embedded as anonymous JSON and later cannot be targeted/referenced/expired correctly.
17. Similar domain concepts from another ruleset do not fit D&D-specific class assumptions.

## 10. Known unknowns requiring investigation

- Whether the accepted class inventory uses a sufficiently explicit identity/lifecycle criterion rather than historical taxonomy choices.
- Whether world records, runtime records and transient protocol values have any ambiguous boundary cases.
- Whether `facets/tags + capabilities` is sufficient for multi-role classification without hiding mechanical semantics.
- Whether any accepted class is a premature special case that should be an existing class plus definition/facet/value.
- Whether any major concept needed by later Steps 2–5 has no correct class/owner.
- Whether comparable VTT/rules engines reveal recurring class-boundary failures relevant to HDM rather than merely different implementation preferences.
- Whether the LLM discovery requirements demand catalog metadata/index contracts that Step 1 never specified.

These are investigation questions, not findings.

## 11. Evidence to inspect after this charter is frozen

Project evidence:

- catalog model/inventory/contracts;
- machine catalog and schemas;
- entity structures, Actor/Asset/Activity/Rule Element architecture;
- identifier policy and promotion/materialization contracts;
- Step-1 critical audits;
- Step-2 and saved Step-3 designs only as downstream consumers/counterexamples.

External evidence only where a gap/assumption warrants it:

- SRD 5.2.1 concept coverage;
- current Foundry D&D5e data models/Activities;
- Avrae automation/content boundaries;
- PF2e Rule Elements/data models;
- relevant schema/versioning standards or primary implementation documentation.

Comparable systems are evidence for failure modes, not automatic templates for HDM.

## 12. Exit criteria for Slice 0A

Slice 0A is assured only when:

1. every requirement/question above has an explicit coverage status against the accepted catalog baseline;
2. every `PARTIAL`, `MISSING`, `DEFERRED_RISK`, and material `IMPLICIT` item has targeted investigation;
3. representative extension/classification cases have been attempted, including non-D&D-shaped and LLM-created content;
4. an independent adversarial review attacks both this charter and the coverage/synthesis;
5. every material finding is resolved, safely deferred, or escalated;
6. the result states `KEEP`, `AMEND`, or `REOPEN` with confidence and reasons.
