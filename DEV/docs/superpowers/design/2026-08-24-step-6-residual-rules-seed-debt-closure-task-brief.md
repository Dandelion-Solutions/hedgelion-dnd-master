# S6D — Step-6 Residual Rules/Seed Debt Closure — Task Brief

Status: **PREPARED / NOT STARTED**

Date: 2026-08-24

Owner decision:

- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`

R2.7 remains paused until S6D closes.

## 1. Purpose

Close the concrete rules/catalog/seed obligations historically deferred by accepted Steps 1–2 to a later Step 6 and proven still relevant by the R2.7 WP-06 reverse audit.

S6D is a bounded architecture/machine-contract closure workstream. It is not the retired physical-LLM Step 6 and it is not broad runtime implementation.

Primary result:

```text
supported D&D rules seed
    -> complete admitted catalog vocabulary
    -> complete selector/accessor/input/dependency contracts
    -> complete Activity/primitive/protocol contracts
    -> strict reusable-definition schemas
    -> reconstructable package/catalog snapshot
    -> focused regression coverage
```

## 2. Source Manifest minimum

Before any coverage or closure claim, read current owning sources including at least:

### Program/process

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- current R2.7 durable audit status
- S6D owner decision and this brief

### Historical owners that created the debt

- Step-1 catalog/class/evolution canonical and assurance artifacts
- Step-2 Actor/Asset/Resource/Effect/Condition/Duration/Recovery/Rule-Element/Activity canonical and assurance artifacts
- Step-2 final critical review
- Steps 1–2 retrospective architecture assurance final
- Step-3 execution canonical owners where they constrain typed inputs/results
- Round-1 Step-6 closure / Round-2 rebaseline owner decision

### Current machine realization

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`
- all implicated `DEV/SCHEMAS/*.json`
- all Step-1/2/3 and R2.7 regression tests
- `DEV/ARCHITECTURE/CATALOG_*`
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`
- Actor/Asset/Effect/Resource/temporal owning architecture

### Runtime consumers

At least:

- `GAME/CORE/MECHANICS_INTEGRITY.md`
- `GAME/CORE/ADJUDICATION.md`
- `GAME/CORE/CHARACTER_READINESS.md`
- `GAME/CORE/COMBAT.md`
- `GAME/CORE/MAGIC.md`
- `GAME/CORE/EXPLORATION.md`
- `GAME/CORE/DIALOGUE.md`
- `GAME/CORE/ADVANCEMENT.md`
- `GAME/CORE/REWARDS.md`
- `GAME/RULES/README.md`

Any other domain consumer discovered through the dependency graph becomes part of the manifest.

## 3. Evidence extraction requirements

Build an item-level debt ledger. For every deferred or discovered item preserve:

- original requirement/claim;
- current owning source;
- applicability to current `v1.0-alpha` supported profile;
- current machine representation, if any;
- missing/stale/partial status;
- qualifiers/non-goals;
- relation to accepted Steps 1–5/Round-2 decisions;
- disposition;
- exact closure evidence.

Do not turn historical future/revisit language into active work unless the current supported seed actually fires it.

## 4. Required S6D domains

### S6D-01 — Ruleset/package/catalog snapshot identity

Close exact identity needed to reconstruct one compatible `ResolvedCatalogContext`:

```text
engine identity/version
ruleset package identity/version
catalog generation
content/compatibility identity as required
selected package dependencies/basis
```

Do not put package-version fields on every world record/definition unless an owning requirement proves them necessary.

Current clean-slate pre-release schemas need no backward-compatibility layer.

### S6D-02 — Catalog admission and gap closure

Reconcile all admitted definition/world/runtime/value/selector/accessor/operation IDs against real supported consumers.

Every ID must be one of:

- supported and fully realized;
- embedded/ephemeral with explicit non-owner disposition;
- future/dormant with a preserved trigger and not selectable now;
- stale and removed.

No placeholder executable vocabulary survives merely because it appeared in an old inventory.

### S6D-03 — Complete Calculation Selector metadata

For every supported registered selector define exact structured metadata sufficient for deterministic validation:

- contribution/result type;
- legal `rule.*` operations;
- operation-specific value contract where required;
- legal dependency kinds;
- legal input provenance classes;
- subject/binding restrictions where needed;
- static dependency edges where architecture fixes them;
- combination/resolution policy ownership.

Registry equality between selectable selectors and machine metadata is required.

### S6D-04 — Mechanical accessors, invocation facts and dependency graph

Close every supported accessor/fact required by the seed.

Preserve:

- engine-owned state cannot be supplied through LLM adjudication;
- missing invocation fact != false;
- state-sensitive derived invariants admit only safe input classes;
- one scoped dependency graph rather than hidden fixed-point/evaluation-order semantics;
- runtime domain queries remain infrastructure-only and nonserializable from content.

Extend invocation-fact shapes only when a supported seed case proves boolean-only insufficient.

### S6D-05 — Activity parameters, targeting, costs and portable protocol values

Finalize exact reusable value contracts needed by supported Activities, including where applicable:

- `TargetSpec`;
- `AreaSpec`;
- `CostSpec`;
- `DurationSpec`;
- Activity parameter declarations/bindings;
- `RollRequest`/`RollResult`;
- Choice/Reaction portable payloads;
- Signal/StateDelta dispositions.

Do not create independent record classes for embedded execution values.

### S6D-06 — Registered Activity primitive contracts

For every supported `op.*` primitive define exact argument/result/reads/mutation contract required by compilation and deterministic execution.

Each primitive must declare enough to prove:

- allowed owner mutations;
- RNG requirements;
- target/source bindings;
- exports/results;
- atomic segment expectations;
- legal failure/suspension paths;
- no arbitrary code/query/file/network capability.

Remove or quarantine primitives that have no supported seed consumer and no current product requirement.

### S6D-07 — Character progression and initial READY_PC seed closure

Close:

- species/background/class/subclass/feat/feature/spell strict definition data;
- stable definition-owned choice slots/options;
- Actor `choice_bindings` validation;
- multiclass/current-level progression reconstruction;
- spell-selection state distinctions where applicable;
- deterministic/default/delegated initial choice policies;
- distinction between initial commitment choices and genuine future level-up/evolution choices.

Prove the supported seed can reach READY_PC without a second flattened sheet owner and without situation-aware retrofitting.

### S6D-08 — Resource / HP / LifeState / Effect / Condition / temporal seed closure

Run concrete seed coverage against accepted ownership, including at least:

- HP maximum/current/temp ownership;
- LifeState transitions/progress;
- successful rest owner-local responses;
- persistent and procedure-local Resource patterns;
- recovery/boundary responses;
- Condition aggregation/intrinsic rule scopes;
- Effect lifecycle/reapplication/support/arbitration;
- concentration/maintenance patterns;
- durations and owner-local scheduled triggers;
- periodic elapsed mechanics;
- derived capacity normalization.

A concrete seed case may extend a typed contract only when the existing architecture cannot represent it without cheating or duplicate authority.

### S6D-09 — Domain rules coverage matrix

Map the supported MVP D&D mechanics surface through the architecture, at minimum:

- common checks/saves/contests;
- attacks/damage/healing/death;
- action economy/reactions;
- movement/range/areas;
- conditions/effects/concentration;
- spellcasting/resources;
- equipment/ownership/uses;
- rests/recovery;
- advancement/character choices;
- hazards/exploration mechanics;
- social/adjudicated checks where mechanics apply;
- reward/economy mechanics that are actually supported by the MVP seed.

For each family prove one of:

```text
FORMALIZED DETERMINISTIC PATH
BOUNDED LLM-ADJUDICATED INPUT -> DETERMINISTIC EXECUTION PATH
OUT OF SUPPORTED MVP SEED
```

No material mechanic may silently use prose narration as its execution engine.

### S6D-10 — Campaign rulings/house-rule boundary dependency

Consume the separately approved Campaign Rulings / House Rules architecture once available.

S6D only needs to prove the mechanical interface:

- nonformalizable LLM judgment can produce only authorized typed adjudication inputs/proposals;
- deterministic state/RNG/owner mutations remain in the kernel;
- formalizable reusable house mechanics use typed definitions/policies;
- prose rulings do not become arbitrary executable code.

If the ruling architecture is still unresolved when S6D reaches this domain, this is an owner/design dependency rather than permission to guess.

### S6D-11 — Tests and machine-contract closure

Use RED→GREEN for structural changes.

Required regression families include:

- selector registry == metadata registry;
- operation registry == exact contract registry for supported primitives;
- strict character definition validation;
- choice-slot / Actor binding closure;
- seed examples for each admitted mechanics family;
- forbidden old authorities/duplicate representations;
- dependency/input-class legality;
- representative suspension/reaction/temporal cases;
- package/catalog snapshot reconstruction/compatibility validation.

Executable CI must be run when the supported branch/tooling path permits it; otherwise no false PASS claim is allowed and the execution obligation remains explicit.

### S6D-12 — Adversarial final closure

Attack the integrated result for:

- duplicate semantic owners;
- hidden LLM engine authority;
- arbitrary executable/query surfaces;
- incomplete registered metadata;
- catalog IDs with no real machine contract;
- seed cases that require unmodeled state;
- dependency cycles/fixed-point assumptions;
- scheduler/background-worker assumptions;
- retry/RNG violations;
- hot-path global scans or unnecessary external calls;
- ruleset identity that cannot reconstruct compatible definitions;
- accidental reintroduction of current-surface migration baggage.

## 5. Structural output authorized inside S6D

Consistent with the clean-slate R2.7 owner decision, S6D may directly canonicalize:

- `DEV/CATALOG/*`;
- `DEV/SCHEMAS/*`;
- owning `DEV/ARCHITECTURE/*` mechanical/catalog contracts;
- focused DEV regression tests;
- ruleset/package machine manifests/schemas required by S6D;
- shipped schema/template/rules-package structural artifacts where S6D is the owning domain.

Do not implement broad gameplay orchestration/runtime algorithms that belong to post-R2.7 implementation planning.

## 6. Exit criteria

S6D may close only when all are true:

1. Source Manifest complete.
2. Historical Step-6 residual ledger complete.
3. No undispositioned deferred Step-6 rules/seed obligation remains.
4. Ruleset/package/catalog snapshot identity is explicit and machine-validatable.
5. Supported registered selectors have complete metadata.
6. Supported accessors/facts/dependencies have complete metadata.
7. Supported Activity protocol values have exact contracts.
8. Supported Activity primitives have exact machine contracts.
9. Character advancement/choice seed is reconstructable and READY_PC-compatible.
10. Resource/HP/LifeState/Effect/Condition/temporal supported seed passes architecture coverage.
11. Domain coverage matrix has no silent prose-execution hole.
12. House-rule/ruling mechanical boundary is explicitly integrated or blocks closure pending its owner decision.
13. No obsolete migration compatibility is retained for nonexistent current campaigns.
14. No new duplicate authority or generic executable subsystem is introduced.
15. Structural changes have regression contracts.
16. Adversarial review has zero unresolved architecture blockers.
17. Exact human decisions, if any, are recorded.
18. Closure gate explicitly authorizes R2.7 WP-06 resume.

## 7. Stop conditions

Stop for the owner only if evidence requires a material choice in supported semantics/scope/authority/risk. Technical representation choices that follow deterministically from accepted architecture are resolved by the agent and recorded.
