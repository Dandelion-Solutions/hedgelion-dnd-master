# Step 2 Retrospective Assurance — Slice B Task Charter: Effects and Conditions

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct the minimum architecture required for persistent and transient rules-bearing states that attach mechanics to actors/assets/locations/zones, including named Conditions, overlapping applications, source/target provenance, suppression, expiry/removal, reapplication, maintained dependencies, and multi-target phenomena.

The charter does not assume the current `world.effect`/Condition design is correct. It asks what ownership/lifecycle semantics are required first.

## 2. Problem statement

HDM needs to represent statements such as:

```text
target is Poisoned by source A until time X
target is Frightened by source B while source is visible
target is affected by Bless from caster C
several targets share one concentration episode
two applications of the same named Condition coexist but may not stack mechanically
one application is suppressed without ending
an old application is refreshed/replaced by a new casting
an aura/zone causes effects while subjects enter/leave
an effect ends and causes a typed follow-up consequence
```

The architecture must distinguish:

- reusable rules identity;
- one concrete application/lifecycle episode;
- named status meaning;
- whether an application currently participates;
- how multiple participating applications combine;
- structural dependency/maintenance relationships;
- temporary suppression versus terminal end;
- provenance/source/target relations;
- derived read/index state versus canonical application state.

## 3. Goals

The design must support at minimum:

1. independently addressable effect applications with stable lifecycle identity when required;
2. named Conditions referenced by other rules;
3. multiple simultaneous applications from different or same sources;
4. deterministic non-stacking/aggregation/overlap semantics without duplicate state authority;
5. application-local typed parameters/severity/provenance;
6. refresh, replacement, removal, dispel, expiry, and source-driven end semantics;
7. temporary suppression/unavailability without destroying lifecycle identity;
8. structural maintained dependencies such as concentration/support;
9. multi-target spells/features without accidental shared target-local mutation authority;
10. genuine shared-lifecycle owners such as zones/auras/objects where appropriate;
11. source-relative Condition mechanics;
12. valued/cumulative Conditions such as Exhaustion-like states;
13. immunity/application gates and removal eligibility;
14. rule contributions/triggers carried by definitions/applications without arbitrary callbacks;
15. bounded indexed discovery by target/condition/source/family/support relation;
16. deterministic prospective activation/termination before atomic commit;
17. continuity/recovery without relying on disposable arbitration/index caches;
18. campaign/local promotion without dangling lifecycle/provenance references.

## 4. Non-goals

This slice does not finalize:

- exact Step-3 trigger/event execution order;
- exact temporal/boundary scheduler/index contract beyond Effect requirements (Slice C);
- LLM natural-language binding protocol (Step 3);
- full SRD condition/spell seed (Step 6);
- arbitrary user scripting or generic callback language.

## 5. Authority questions

### Definition versus application

- Which mechanics belong to reusable definition and which to concrete application?
- When does a rule need an independently identified application rather than direct evaluation from its owner?
- Can one application own multiple targets, and if so under what lifecycle semantics?
- Does a named Condition require a separate application entity from an Effect?

### Lifecycle

- What are nonterminal/terminal states?
- Is suppression a lifecycle state or independent derived participation state?
- Does terminal state retain provenance/history?
- Can an application be reactivated after terminal end or must a new episode be created?
- Which fields are immutable during an application episode?

### Reapplication

- How is an existing episode selected for refresh/replace?
- Is matching by target/source/origin/family/definition identity?
- What prevents SQL uniqueness constraints from becoming rules semantics?
- Does refresh preserve provenance/source/parameters or may they change?

### Multiple applications and combination

- Which layer decides application participation/arbitration?
- Which layer combines individual Rule Element contributions?
- Which layer gives a named Condition its effective presence/value?
- How are cumulative versus non-cumulative states represented without a generic stack counter?
- How are source-relative intrinsic rules evaluated when the named Condition itself is logically present only once?

### Source/target/provenance

- What does `source` mean: causal actor, immediate object/effect, rules origin, or all of these?
- Which provenance links must survive source retirement/transformation/promotion?
- What if source ceases to exist but the effect rule says the application persists?
- What if target retires/dies/transforms?

### Structural support

- Can an application depend on another application's existence?
- Is one parent sufficient for proven maintained mechanics?
- What happens on parent suppression versus terminal end?
- How are descendant cascades validated/committed without reverse canonical lists?
- Are cycles possible and how are they rejected?

### Removal/expiry

- Does removal target named Condition, exact application, family, source, tag, or another closed criterion?
- How are provenance-sensitive removable units selected?
- Can an automatic boundary response make a choice? If not, where does adjudication go?
- How are end-trigger consequences represented without callbacks?

## 6. Multi-target and spatial cases

The later assurance must test:

1. one spell affects five actors and caster stops concentration;
2. one target dispels only its own application while the shared maintenance episode continues/ends according to rules;
3. an aura exists independently of any one target and subjects enter/leave repeatedly;
4. a zone persists after its creator leaves/dies;
5. an Effect owned by an Asset moves with the Asset;
6. two targets receive different parameters/durations from one source operation;
7. one target-local application is promoted while its support root remains local;
8. a location/world effect has one lifecycle owner but creates target-local consequences.

## 7. Condition cases

Test at minimum:

- Poisoned from two sources: one named Condition, no doubled generic penalty;
- Frightened/Charmed from multiple sources: source-relative rules remain distinguishable;
- Grappled by multiple grapplers: aggregate and per-source rules coexist;
- Exhaustion-like cumulative units with per-unit provenance/removal constraints;
- immunity prevents new application without writing copied immunity flags;
- removing one application does not erase another valid source;
- a source-specific cure cannot remove ineligible applications;
- a Condition can be suppressed while its application lifecycle remains active if a rule requires it;
- Condition ends and triggers a typed consequence.

## 8. Failure scenarios

1. Two identical same-source applications occur in the same segment.
2. A retry repeats an application command after commit.
3. Refresh is attempted against a stale/terminal episode.
4. Replace ends an old application and creates a new one while triggers observe the edge.
5. Parent support and intrinsic duration expire at the same boundary.
6. Parent is suppressed but not terminal.
7. Parent termination has a deep descendant tree.
8. An application cycle is attempted during prospective creation.
9. Arbitration winner changes because one application becomes unavailable.
10. Condition aggregate value crosses a lethal or other threshold.
11. Automatic remove-one has multiple provenance-sensitive eligible candidates.
12. Source Actor dies/retires while application duration says it persists.
13. Target transforms into a form immune to the Condition while applications already exist.
14. Definition changes/migrates while durable applications reference the old definition snapshot.
15. A canonical child points to local-only support parent/source/definition.
16. A zone/aura disappears while target-local effects created by it remain indexed.
17. Multiple same-time end causes race; final lifecycle must not depend on SQL order.
18. LLM claims a target "is poisoned" without a valid engine application.

## 9. Quality attributes

### Correctness

- application identity/lifecycle/provenance has one authority;
- effective Condition/arbitration state is deterministic and derived;
- terminal application does not silently reactivate;
- overlapping mechanics do not rely on row order or accidental uniqueness.

### Determinism

- same pinned application set + definitions + context yields same participation/aggregation;
- no fixed-point recursion or LLM adjudication for engine-owned Effect/Condition truth.

### Performance

- target/source/condition/family/support/due lookups are bounded/indexable;
- no campaign-wide scans for ordinary application/arbitration/removal;
- reverse support/condition indexes may be disposable projections.

### Recovery

- authoritative application fields are enough to rebuild participation/support/due indexes;
- continuity-critical local applications/support roots are included in promotion/checkpoint closure when required;
- source/definition references remain interpretable against the catalog context.

### Extensibility

- adding a new Condition/Effect normally uses definitions/registered policies rather than Python subclasses;
- unusual application rules do not force a generic scripting/graph language without proof.

## 10. Cross-system dependencies

### Slice A

- HP/LifeState/Resource contributions and transition prevention;
- effects changing true Resource capacity versus mere availability;
- death does not automatically purge all applications.

### Slice C

- intrinsic duration, semantic/procedure boundaries, periodic consequences;
- same-time expiry/support loss/recovery closure.

### Slice D

- effect availability/arbitration/Condition aggregation in dependency DAG;
- selectors/accessors versus runtime domain queries.

### Step 3

- application creation/reapplication/removal atomicity;
- Signals/Events/end consequences;
- reaction/choice/adjudication;
- idempotency and same-segment ordering.

### Step 5

- promotion/durability of support/source/target/definition closure;
- shared/cross-scene effect ownership.

## 11. Known unknowns requiring investigation

- Whether one immutable `support_effect_id` parent is sufficient for proven mechanics beyond concentration.
- Whether current source/provenance fields distinguish causal actor, immediate source object, and rules origin sufficiently.
- Whether `source_id` should be allowed to reference terminal/retired entities without invalidating a still-active application.
- Whether Effect arbitration needs a stable application-family identity beyond derivation from rules origin/definition/context.
- Whether current Condition removal contracts can express provenance-sensitive cures without arbitrary queries.
- Whether area/aura/zone ownership is sufficiently separated from target-local Effect applications.
- Whether active Effect application schema has enough durable information to survive catalog/version migration and local promotion.
- Whether any SRD rules require multi-parent maintained support or mutable reparenting.

## 12. Exit criteria

Slice B closes only when every charter requirement has coverage status, all material gaps/unsafe deferrals receive targeted research, multi-feature counterexamples are attempted, an independent critic attacks the synthesis, and every finding is fixed/deferred/escalated with `KEEP|AMEND|REOPEN` verdict.
