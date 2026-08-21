# Step 2 Retrospective Assurance — Slice B Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — BOUNDED CORRECTIONS REQUIRED, NO HUMAN GATE**

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Verdict

The critic could not justify replacing the accepted Effect/Condition architecture. The one-application/one-target model, Condition-as-named-definition-over-Effect-applications, two Condition axes, support forest, and separation of lifecycle/availability/arbitration all survive.

The synthesis correctly found three gaps. The critic tightens B-F1/B-F2 to avoid introducing new ambiguity and adds one downstream retention invariant for causal ordering.

## 2. Finding B-C1 — `condition.applicability` is a state-effectiveness calculation, not merely a create gate

**Severity: SIGNIFICANT semantic correction.**

The official D&D rule says condition Immunity means the condition does not affect the creature in any way. Since immunity itself can be gained from another active Condition (Petrified grants Poisoned immunity), an application-only gate is insufficient.

The correct narrow meaning is:

> `condition.applicability` resolves whether a specific named Condition may mechanically affect a specific subject in the current pinned/prospective application context.

Consumers are limited to:

1. validation/planning of a new Condition application;
2. current eligibility of an existing nonterminal Condition-bearing Effect before Condition aggregation.

It is **not** a generic Condition lifecycle resolver, arbitrary suppression policy, or removal operation.

### Existing application under newly gained immunity

```text
application remains nonterminal
condition applicability becomes immune/blocked
application is excluded from effective Condition aggregation
```

If immunity disappears before the application independently ends, normal derived reevaluation may make it effective again. No lifecycle resurrection occurs because lifecycle never ended.

A rule that explicitly says immunity/removal **ends** an application may still produce a normal terminal transition. Immunity alone does not silently rewrite lifecycle.

### Binding

For existing-application evaluation the selector may receive only the bounded current application context needed by registered mechanics:

```text
condition identity
target
source/rules-origin roles when declared by the selector contract
declared application parameters
```

This preserves the query boundary. Slice D must encode these consumer/binding/dependency restrictions in machine metadata.

## 3. Finding B-C2 — three provenance identities must stay separate

**Severity: SIGNIFICANT ambiguity prevention.**

The synthesis correctly identifies `rules_origin_id` as under-specified, but the critic makes the separation normative:

```text
definition_id
    reusable mechanics payload applied by this world.effect

rules_origin_id
    reusable definition whose rule semantically created/owns the application family
    e.g. spell/feature/hazard/condition/Activity definition

source_id
    concrete world source instance, when one exists
    e.g. caster/asset/hazard/zone/another Effect

causal execution origin
    concrete Step-3 command/Resolution/segment/Event occurrence that created or
    last lifecycle-materially changed this application
```

The last item must **not** be stuffed into `rules_origin_id` or `source_id`.

### Application-family derivation

Initial deterministic family rule:

```text
Condition-bearing application:
    family = definition_id (the named Condition)

non-Condition application with explicit rules_origin_id:
    family = rules_origin_id

otherwise:
    family = definition_id
```

Source identity does not define family by default. A same-source requirement is an explicit reapplication match policy, not a family rewrite.

`rules_origin_id`, when present, must resolve to reusable content in the same `ResolvedCatalogContext`; it is not an arbitrary world ID/string. Exact allowed rules-bearing definition kinds belong to compiler/reference-contract metadata rather than string-prefix inference.

### Causal origin deferral

Step 3 may decide whether the durable causal relation is stored directly on `world.effect`, in immutable MechanicalEvents, or in another one-authority indexed relation. It must preserve enough identity/order for:

- retry/idempotency;
- `potency_then_recency` or another registered mechanical-recency comparator;
- audit/provenance after restart;
- replacement/refresh causal receipts.

No current Step-2 field choice is required before that execution identity contract exists.

## 4. Finding B-C3 — terminal reasons are closed machine semantics

**Severity: MODERATE.**

`terminal_reason_id` is not descriptive provenance. It selects registered lifecycle semantics and therefore must resolve through the closed `effect_terminal_reasons` registry.

The current schema's arbitrary machine ID is too broad. Restrict it to the current registered values and keep schema/catalog synchronized.

## 5. Attack: should immunity terminate existing Condition applications instead?

Terminating them is simpler for `condition.present`, but it destroys independent duration/provenance merely because a potentially temporary immunity appears. If immunity later disappears, recreating the old application would require inventing remaining duration and identity or treating the terminal record as resurrectable, both worse.

The existing lifecycle/availability separation is specifically designed for this case. Therefore derived unavailability is preferred unless the concrete rule explicitly ends the source effect.

## 6. Attack: should Condition immunity be a stored Actor immunity list?

Rejected. Immunity may come from archetype/build/equipment/Conditions/Effects and can be prospective. A writable list would duplicate those rule sources and require synchronization. The registered calculation selector is the correct derived surface.

## 7. Attack: store application family canonically

A canonical `family_id` would make queries cheap and provenance explicit, but it duplicates a deterministic function of definition/rules-origin in the accepted baseline. The family should remain derived/indexed unless a future grouping rule proves it cannot be reconstructed from stable authoritative inputs.

## 8. Attack: one generic `origin_id` for rules + source + event

Rejected. Reusable semantic sameness, concrete source identity, and concrete causal occurrence have different cardinality/lifetime/migration behavior. Combining them makes same-spell/different-caster arbitration and retry provenance ambiguous.

## 9. Attack: keep every terminal Effect forever for provenance

Rejected. The accepted Effect design already separates terminal lifecycle from physical retention. Once no active support/reference/publication/audit obligation requires the row, persistence policy may compact/GC it while committed history retains required causal facts.

However Step 3/5 must not GC the only durable representation of a mechanical recency/provenance fact still needed by a live overlapping application. This is an explicit retention dependency, not a reason to retain all terminal Effects forever.

## 10. Attack: multi-parent support

No proven D&D/SRD case requires one dependent application's existence to be structurally maintained by multiple alternative/conjunctive parents. Adding a graph would create cycle, removal, promotion, and closure semantics without evidence. Keep one parent.

## 11. Attack: zone-target Effects lose per-creature source-relative mechanics

A zone-target Effect is correct only while the mechanic is truly spatial/owner-local. If entering creates an independent Condition, duration, save result, parameter, or consequence that must survive leaving, create a target-local child application. This boundary remains sufficient and does not need a multi-target record.

## 12. Attack: source retirement should automatically end Effects

Rejected. Source identity is provenance, not support. Some effects explicitly persist after caster/source absence; others end through Concentration/support or another rule. Automatic source-liveness coupling would conflate provenance with lifecycle.

## 13. Deferral audit

### Step 3 — safe but mandatory

Must close:

- concrete causal application origin/ordering;
- refresh/replace/create Event/receipt identity;
- provenance-sensitive remove-one operation/adjudication;
- same-time end ordering;
- typed source/rules-origin binding validation during execution.

### Step 5 — safe but mandatory

Must close:

- promotion/retention closure for local source/support/definition dependencies;
- GC/compaction without losing live recency/provenance requirements;
- cross-scene shared spatial Effect ownership.

### Step 6 — safe

May add new arbitration/support/removal policies only from proven seed/ruleset cases.

## 14. Recommendation

Apply B-C1–B-C3 mechanically. Record B-C2 causal-origin requirements explicitly for Step 3 and retention dependency for Step 5/Slice E.

Recommendation: **AMEND / KEEP STEP 2 CLOSED**.

Human decision required: **NO**.

Confidence: **HIGH**.
