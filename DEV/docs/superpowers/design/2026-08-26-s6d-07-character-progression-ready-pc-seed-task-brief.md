# S6D-07 — Character Progression and READY_PC Seed Closure — Architecture Task Brief

Status: **STEP 1 COMPLETE — WHOLE-PROJECT BRIEF CRITIC PASS — STEP 2 NOT STARTED**

Date: 2026-08-26  
Authoritative branch: `v1/engine-rearchitecture`  
Pinned Step-1 remote ref: `27cbe2485248d1efbd8cd4d0b6bf5e38bea77803`  
Predecessor: S6D-06 complete; all 31 registered Activity primitive names are quarantined with zero execution authority.

## 1. Assignment

Execute only Step 1 of the S6D-07 eight-step design loop.

Frame the evidence and decision work required to close the supported character-creation and advancement rules seed: species, background, class, subclass, feat, feature, spell and advancement definitions; stable choice slots/options and prerequisite/grant semantics; reconstructable Actor build selections; and deterministic READY_PC validation across initial creation and later advancement boundaries.

After mandatory whole-project brief criticism, publish the repaired Task Brief, critic and minimal routing/status updates, verify the authoritative branch, and stop. Do not begin Step 2 or S6D-08.

## 2. Problem

Accepted GAME owners define a progressive onboarding model and a reconstructable initial mechanical commitment frontier. Current machine artifacts already expose strict definition schemas, `build.choice_bindings`, class progression and spellcasting state, but the repository does not yet prove end-to-end that:

- every supported build grant and discretionary choice has stable definition-owned identity;
- initial choices cannot remain strategically open after READY_PC;
- future level-up/preparation/acquisition choices are distinguished from unresolved initial debt;
- Actor instance state stores selections rather than a duplicated flattened sheet;
- prerequisites, defaults, delegated selection and deterministic derivation are unambiguous;
- representative supported builds can be reconstructed from the accepted ruleset snapshot;
- readiness validation follows the current canonical provisional-gameplay law rather than stale completeness or “no scene before READY_PC” assumptions.

S6D-07 must close this seed without selecting unsupported content breadth, duplicating derived mechanics, turning prose/concept into execution authority, or silently activating quarantined S6D-06 operations.

## 3. Goals

The full loop must eventually prove:

1. exact supported definition inventory for species/background/class/subclass/feat/feature/spell/advancement;
2. strict schema and catalog identity for grants, prerequisites, choice slots and options;
3. stable `choice_id` and `option_id` semantics across package reconstruction;
4. exact initial-versus-future choice ownership and opening/closing boundaries;
5. deterministic/default/delegated choice policy fixed before situational exposure;
6. Actor `build.class_progression`, `build.choice_bindings` and spellcasting state sufficient for reconstruction without a flattened sheet;
7. exact READY_PC dependency predicate and failure evidence;
8. legal multiclass/subclass/feat/spell-selection and prerequisite handling for the supported seed;
9. representative initial-build and level-up cases, including martial and spellcasting paths;
10. compatibility with ruleset/package identity, catalog admission, selectors/accessors, portable values and quarantined primitive policy;
11. synchronization of GAME owners, architecture, schemas, catalogs, examples and tests;
12. no hidden LLM mechanical authority or opportunistic post-exposure selection.

## 4. In scope

### 4.1 Definition and seed census

- exact current definition kinds and registered/admitted IDs for the eight character families;
- strict data-schema coverage and cross-definition references;
- level-indexed grants, replacement/upgrade semantics and subclass timing;
- prerequisite predicates and applicability phase;
- feature/spell acquisition, known/prepared/spellbook distinctions where supported;
- starting proficiency, equipment/resource and ability-input references needed to prove READY_PC, while leaving their domain semantics with existing owners;
- stale, dormant, structural-example and unsupported-content dispositions.

### 4.2 Choice model

For every supported choice-producing definition:

- stable choice-slot identity, option identity and owning definition/revision;
- cardinality, uniqueness, ordering and repeatability;
- option source: closed inline set, catalog family, bounded predicate or deterministic grant;
- prerequisite evaluation point and pinned catalog/build context;
- instance binding shape and provenance;
- deterministic/default/delegated selection policy;
- whether the choice belongs to initial commitment, genuine future evolution or repeatable preparation;
- replacement, respec/correction and invalidation behavior;
- no choice after relevant situational exposure unless a precommitted policy already determines it.

### 4.3 Actor reconstruction and READY_PC

Trace definition grants and bound choices into the accepted `world.actor` model:

```text
ResolvedCatalogContext
-> accepted build anchors/class progression
-> applicable definition grants and choice slots
-> Actor choice bindings/spellcasting + referenced Assets/Effects
-> uniquely derived capability/resource/defense surfaces
-> READY_PC predicate and evidence
```

READY_PC is neither a complete-sheet schema predicate nor a prerequisite for harmless provisional gameplay. It is the initial commitment frontier for unrestricted mechanics-capable play. The brief must require local mechanical sufficiency checks before READY_PC and forbid strategically open initial alternatives at the frontier.

### 4.4 Advancement boundary

- exact trigger/authority for a gained level or other advancement entitlement;
- separation between entitlement, pending choices, validation and committed Actor change;
- current-level reconstruction before and after advancement;
- multiclass/subclass/feat/spell-choice prerequisites where supported;
- transactional publication, retry/idempotency and recovery routing through accepted execution/persistence owners;
- READY_PC behavior while a genuine later advancement choice is pending;
- corrections/respec only through existing repair/house-rule authority, never silent retuning.

### 4.5 Machine closure and verification

- schema/catalog bidirectional equality for supported definition families;
- `$ref` and catalog-reference closure;
- positive and negative fixtures for initial build, delegated/default choices, unresolved material choices, level-up and spellcasting;
- exact readiness dependency/failure matrix;
- stale regression and prose-owner synchronization;
- TDD for structural changes in Steps 5–8.

## 5. Out of scope

- broad HP/LifeState/Resource/Effect/Condition/recovery semantics owned by S6D-08;
- whole-domain mechanics coverage owned by S6D-09;
- balance decisions or full publication of every possible D&D option;
- gameplay bootstrap or campaign creation;
- runtime implementation of a general character builder, planner or UI;
- generic rules query/expression language;
- a flattened authoritative character sheet duplicating definition/Asset/Effect owners;
- arbitrary LLM-authored grants, prerequisites, stats or capabilities;
- automatic activation of any S6D-06 primitive;
- reopening progressive onboarding/READY_PC semantics without a concrete canonical conflict and decision-ready proposal.

## 6. Inherited invariants and owner boundaries

1. `GAME/CORE/CHARACTER_READINESS.md` owns the current READY_PC semantic frontier; `CHARACTER.md` and `DIEGETIC_ONBOARDING.md` own progressive/provisional onboarding behavior.
2. Harmless or locally sufficient provisional gameplay may precede READY_PC. Ordinary unrestricted mechanics-capable play may not.
3. Player authority, delegated bookkeeping and deterministic defaults follow the accepted precedence; concept text is not executable mechanics.
4. A material initial choice cannot remain open until its advantageous situation is known.
5. Future evolution is not initial incompleteness; a later genuine choice may remain pending under its own boundary.
6. Actor stores instance-owned anchors/selections. Definitions own reusable grants/options; Assets and Effects retain their own state.
7. Derived values need not be persisted when uniquely reconstructable from pinned accepted dependencies.
8. `ResolvedCatalogContext` and ruleset-set identity pin the definition universe used for validation and reconstruction.
9. Catalog registration is not admission. Dormant/stale definitions and options remain nonselectable.
10. S6D-03/04 own selector/accessor/input/dependency metadata; S6D-05 owns portable choice values; S6D-06 grants zero primitive execution authority.
11. If S6D-07 needs an executable primitive, it must replace one quarantine with an exact owner-local contract and undergo whole-project review; a seed consumer alone cannot activate a draft.
12. Step-3/Step-5 owners retain commit, event, receipt, continuation, idempotency and recovery authority.
13. House rules may alter mechanics only through accepted typed policy/authority routes.
14. No normal-play web lookup or LLM round trip is required once the accepted build is reconstructable locally.

## 7. Mandatory Source Manifest for Step 2

Step 2 must fresh-read the remote ref and record authority role, applicability, supersession, extracted item-level evidence and conflicts for:

### 7.1 Process and sequence

- `AGENTS.md`, both design-process owners, `DEV/PROJECT_MAP.md`, current roadmap;
- S6D owner decision, Task Brief and execution plan;
- canonicalizations/owners for S6D-01 through S6D-06;
- current catalog-admission ledger and ruleset/package identity.

### 7.2 Character and onboarding owners

- `GAME/CORE/CHARACTER.md`;
- `GAME/CORE/CHARACTER_READINESS.md`;
- `GAME/CORE/DIEGETIC_ONBOARDING.md`;
- `GAME/CORE/ADVANCEMENT.md`;
- campaign setup, player authority/binding, durability and mechanics-integrity owners reached through PROJECT_MAP;
- current House-Rules/access-control owners for correction, override and delegated policy.

`DEV/TESTS/CHARACTER_READINESS_CASES.md` is a regression/evidence artifact, not semantic authority. Its C08 “no first scene before READY_PC” wording conflicts with the current canonical progressive-onboarding law and must be reconciled or replaced; it cannot silently override the owner.

### 7.3 Architecture and execution owners

- Actor, Asset, Entity Structures, Catalog Contracts/Resolution/Admission;
- Rule Element, Calculation Selector, MechanicalContext, Portable Activity Values and Activity Primitive Contracts;
- Step-3 execution boundary and Step-5 durability/currentness/recovery owners;
- identity, chronology and correction/repair owners reached by exact references.

### 7.4 Machine artifacts

- `core-catalog.json`, `catalog-admission-ledger.json`, `entity-structures.json` and relevant package manifests;
- `actor-archetype`, `advancement`, `background`, `build-choice-slot`, `class`, `subclass`, `species`, `feat`, `feature`, `spell`, `catalog-definition` and `world-actor-state` schemas;
- `GAME/SCHEMA/pc.schema.yaml` and `GAME/SCHEMA/player.schema.yaml`, every transitive schema they reference, and the exact loaders/readiness/bootstrap/runtime consumers that read or write those shapes;
- every transitive `$ref`, discriminator and catalog lookup reached from those roots;
- definition examples/seed files and all exact IDs actually presented as supported.

The GAME schemas are not presumed authoritative for mechanical state merely because they are shipped. Step 2 must build a field-level projection/debt ledger for every readiness/build/progression/spell/equipment field: canonical Actor/Asset/Effect/definition owner, GAME-schema representation, actual reader/writer, derived compatibility projection status, duplicate-owner risk, and required `retain as projection / reroute / remove` disposition. S6D-02 uncertified legacy PC fields remain debt until this reconciliation proves otherwise.

### 7.5 Tests and consumers

- character readiness cases and their current executable consumer, if any;
- catalog-definition binding and WP-04 Actor/Asset conformance tests;
- all schema/catalog tests mentioning class progression, choice bindings, readiness, spellcasting, advancement, initial build, level-up or PLAY_READY;
- runtime/bootstrap/release validation that consumes these artifacts;
- every actual loader/test/command path consuming `pc.schema.yaml` or `player.schema.yaml`, including readiness and bootstrap projections.

Use PROJECT_MAP before repository search. Search all exact schema fields and definition kinds; a zero-result search is non-evidence until owners/directories and transitive references are inspected. External rules research is not presumed in Step 2; if exact public seed content is later required, use only legally admissible official/public sources and independently word HDM artifacts.

## 8. Required Step-2 evidence products

### 8.1 Definition-family census

One row per family and current registered/seed item: identity, owner, schema, admission state, consumers, cross-references, applicability by level, current realization, and `supported / dormant / stale / structural-only` disposition.

### 8.2 Grant and choice-slot matrix

One row per supported grant/choice slot: stable owner-relative ID, acquisition boundary, option source, cardinality, prerequisites, deterministic/default/delegated policy, Actor binding, replacement/correction rule, readiness relevance and tests.

### 8.3 Initial commitment frontier matrix

Account for every current canonical READY_PC bullet and classify it as stored Actor state, referenced Asset/Effect/definition, uniquely derived value, conditionally inapplicable, or blocking unresolved choice. For every corresponding GAME PC/player field, record whether it is a derived projection, illegal duplicate owner, stale compatibility field or absent-by-design, plus every reader/writer that must be synchronized. Preserve qualifiers; “representative sheet fields exist” is not coverage.

### 8.4 Advancement transition matrix

Trace entitlement -> applicable grants/choices -> pending state -> validation -> atomic publication -> reconstructed build -> receipt/recovery. Distinguish initial creation, level-up, subclass threshold, feat acquisition, spell known/prepared/spellbook changes and multiclassing where supported.

### 8.5 Representative seed cases

At minimum: level-1 martial; level-1 spellcaster; delegated concept-to-build; deterministic default; materially ambiguous choice requiring player input; subclass/feat threshold; level-up with new and deterministic grants; multiclass attempt; known/prepared/spellbook distinction; invalid/stale option; retry/recovery; provisional locally sufficient action before READY_PC; READY_PC rejection with strategically open choice.

### 8.6 Cross-owner graph

For each case trace definition identity -> grant/choice -> Actor/Asset/Effect storage -> selectors/accessors -> readiness/advancement validation -> execution/publication/recovery. Mark every dormant dependency and prove no S6D-06 quarantine is bypassed.

### 8.7 Verification matrix

Require tests for schema strictness, stable ID uniqueness, reference/admission closure, prerequisites/cardinality, duplicate/stale options, deterministic reconstruction, initial/future separation, no-situational-selection, readiness positive/negative cases, provisional-play compatibility, advancement idempotency/recovery, no flattened duplicate sheet and no hidden primitive activation.

## 9. Questions Step 2 must answer

1. What exact public supported character seed is currently claimed, and where is it packaged?
2. Which definition IDs are active, dormant, structural-only or stale?
3. Which owner defines grants and which Actor fields bind selections?
4. Are `choice_id` and `option_id` stable within definition revision, package snapshot or global catalog?
5. How are catalog-backed option sets frozen against later package changes?
6. What distinguishes deterministic grant, initial choice, future advancement choice and repeatable preparation?
7. Which current READY_PC bullets are machine-checkable, and what gaps remain?
8. Can readiness be proven without persisting derived sheet values?
9. How are delegated/default selections fixed before situational exposure?
10. What is the pending representation for later advancement choices, and does it duplicate Continuation/workflow ownership?
11. How do multiclass, subclass, feat and spell prerequisites compose without a query DSL or fixed-point engine?
12. What happens when an adopted package update invalidates a previously legal option?
13. Which stale readiness tests/prose must be synchronized to progressive onboarding?
14. Does any representative seed require replacing an S6D-06 quarantine, and if so is the full primitive contract actually proven?
15. What genuine product-semantic/scope choice, if any, remains for the human architect after evidence work?

## 10. Candidate approaches to evaluate

### A. Definition-owned stable choice slots + sparse Actor bindings — recommended starting hypothesis

Reusable definitions own level-indexed grants and closed choice slots/options; Actor stores only selected owner-relative bindings and progression anchors. READY_PC derives closure from pinned definitions and referenced state.

Benefits: one semantic owner, reconstructability and no flattened sheet. Risk: requires rigorous package/revision pinning and dependency closure.

### B. Materialized resolved build manifest per Actor

Compile definitions into a complete immutable resolved-build snapshot and keep it as Actor authority.

Benefit: simple reads. Risk: duplicates reusable definition semantics, complicates upgrades/corrections and can become a second character sheet owner.

### C. Runtime recomputation with unbound flexible choices

Resolve options only when encountered.

Rejected default: enables situational optimization, weakens READY_PC and creates repeated lookup/LLM dependency.

Hybrid caches may be evaluated only as derivative non-authoritative acceleration with exact invalidation.

## 11. Agent/human responsibility

The agent owns source discovery, item-level definition/choice/readiness accounting, conflict reconciliation, machine-gap proof, alternatives and recommendation. Stop for the human only if evidence leaves a material supported-content scope, player authority, advancement semantics or risk decision. Schema placement, stale-test repair, technically forced IDs/references and dormant classification are agent work.

## 12. Eight-step loop

1. Architecture Task Brief plus independent whole-project brief critic.
2. Research & Architecture Draft.
3. Decision Brief.
4. Collaborative Review.
5. Candidate Specification and TDD machine realization where authorized.
6. Independent whole-project adversarial solution review.
7. Resolution Gate.
8. Canonicalization and verified publication.

Both critics must rebuild the complete direct and indirect dependency graph through current PROJECT_MAP and inspect actual owners, amendments, schemas, catalogs, tests and consumers. Module-local review is invalid.

## 13. Step-1 exit criteria

Step 1 is complete only when scope, inherited owners, definition/choice/readiness/advancement evidence products, representative cases, S6D-06 quarantine boundary, stale-readiness conflict, GAME PC/player projection debt and machine/test/loader routes are explicit; critic has zero unresolved BLOCKING/SIGNIFICANT findings; brief, critic and minimal routing/status changes are published and verified; Step 2 and S6D-08 remain unstarted.

## 14. Full-loop exit criteria

S6D-07 closes only when every supported definition/choice is accounted; Actor reconstruction and READY_PC are proven without duplicate authority; every GAME PC/player readiness/build field and reader/writer is retained only as an explicit derived projection or rerouted/removed; initial/future choice boundaries and advancement transitions are exact; representative seed cases pass; quarantined dependencies remain rejected unless independently replaced and reviewed; stale regression semantics are synchronized; machine tests pass; critic has zero unresolved BLOCKING/SIGNIFICANT findings; and S6D-08 Step 1 is next but unstarted.

## 15. Stop boundary

After brief criticism, repair all BLOCKING/SIGNIFICANT framing defects, publish only Step-1 artifacts and minimal routing/status updates, verify remote content and stop before Step 2.

