# Step 2 Retrospective Assurance — Slice B Coverage and Research

Status: **ASSURANCE SYNTHESIS — ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-2-assurance-slice-b-effects-conditions-task-charter.md`

## 1. Coverage summary

| Requirement family | Coverage | Finding |
|---|---|---|
| reusable Effect/Condition identity vs concrete application | FULL | definitions and `world.effect` applications are separate |
| one target/local independent application | FULL | single `target_id`; zones/assets/locations can themselves be targets |
| multi-target shared maintained episode | FULL | one root + per-target dependents; no CastGroup required |
| lifecycle versus suppression versus arbitration | FULL conceptually | separate axes; no copied winner/suppressed authority |
| refresh/replace/default new identity | FULL | matching and lifecycle action separated |
| overlap/application-family semantics | PARTIAL | conceptual derivation is sound; `rules_origin_id` reference semantics are not machine-closed |
| Condition aggregation | FULL | `presence` / `cumulative_units` + effective member set |
| source-relative intrinsic Condition rules | FULL | per-rule `aggregate_once` / `per_effective_application` |
| Condition immunity for new application | FULL | `condition.applicability` + `rule.immunity` |
| Condition immunity acquired after existing application | MISSING explicit pipeline rule | existing application must cease to affect target while immunity applies |
| cumulative provenance-sensitive removal | FULL minimum / Step 3 execution | concrete unit applications + typed provenance requirement; selection/adjudication later |
| maintained support/concentration | FULL | immutable zero/one parent, downward terminal cascade |
| multi-parent/reparenting | OUT_OF_SCOPE correctly | no proven seed need |
| terminal Effect retention/GC | FULL minimum / later policy | terminal and physical GC explicitly separate; history belongs events/traces/checkpoints |
| terminal reason vocabulary | IMPLICIT machine gap | schema accepts arbitrary machine ID despite closed registry |
| exact causal application identity/recency | DEFERRED_OK to Step 3 | mechanical recency explicitly requires committed causal ordering |
| source retirement/local promotion | DEFERRED_OK with minimum | retired records remain addressable; promotion closure required for durable refs |
| target transformation/new immunity | PARTIAL | general transform state migration exists; Condition availability effect needs explicit immunity rule |
| Zone/aura ownership | FULL minimum | zone-target Effect unless independent target-local state is created |
| end consequences | FULL minimum | typed Signal/Event + Trigger/Activity; no callbacks |
| bounded indexes | FULL | target/family/support/temporal indexes are derived projections |

## 2. Core architecture retained

The independent charter did not expose a need for:

- a separate `world.condition` entity;
- multi-target mutable Effect records;
- generic Effect stacks;
- persistent arbitration winners;
- generic support graphs;
- callbacks/scripts;
- a universal application group/cast group.

The existing decomposition remains coherent:

```text
Effect application identity/lifecycle/provenance
    !=
availability/suppression
    !=
Effect arbitration participation
    !=
Condition aggregation
    !=
Rule Element contribution combination
```

This separation is especially valuable for Conditions, where the same named state can have several source/duration applications while intrinsic semantics do not necessarily strengthen.

Official D&D 2024 rules directly support the model: multiple effects imposing the same Condition keep independent durations while the Condition normally does not stack, with Exhaustion as the exception. Concentration also has an independent creator-maintenance lifetime and explicit break conditions rather than being a generic timer mode.

## 3. Finding B-F1 — Condition immunity must participate in current effectiveness, not only new application

**Severity: SIGNIFICANT semantic gap.**

The accepted selector/query work currently frames:

```text
condition.applicability
    -> attempt to apply Condition X
    -> immunity may block creation
```

That handles a target already immune when a new Condition would be applied.

It is insufficient when immunity becomes true **after** a valid nonterminal Condition application already exists.

D&D 2024 states that if a creature has Immunity to a condition, that condition does not affect it in any way. `Petrified` explicitly grants Immunity to `Poisoned`. Therefore the following is a real rules case:

```text
Poisoned application exists with remaining duration
    -> target becomes Petrified
    -> Poisoned immunity becomes true
```

The Poisoned application need not be destroyed merely to make its mechanics stop; doing so would incorrectly make a temporary immunity erase independent duration/provenance. The existing architecture already has the correct axis for this: **availability/effectiveness is separate from lifecycle**.

### Required refinement

Use the same narrow Condition applicability/immunity calculation in two places:

```text
1. prospective new-application gate
2. per-application current Condition eligibility before aggregation
```

Conceptually:

```text
nonterminal Condition-bearing Effect application
    -> condition.applicability(target, condition, current application context)
    -> if immune: application is unavailable for Condition aggregation
    -> if not immune: application may participate
```

The application remains nonterminal unless a separate rule explicitly ends it.
If immunity later ends while the application's own duration/lifecycle still exists, it can become effective again through derived recomputation rather than resurrection mutation.

### Source-relative immunity

The selector context must permit only the closed current application binding needed by proven rules, such as condition target/source/rules origin and declared parameters. This does not authorize arbitrary queries.

The hybrid dependency DAG already includes Effect availability, Condition aggregation, and Condition intrinsic mechanics, so immunity-induced cycles remain rejectable.

This is a semantic extension of the existing `condition.applicability` selector, not a new authority or stored suppression flag.

## 4. Finding B-F2 — `rules_origin_id` is a mechanically important reference but its semantics are under-specified

**Severity: SIGNIFICANT reference-contract gap, mechanically resolvable.**

Effect design correctly distinguishes:

```text
effect_id       concrete application
definition_id   reusable Effect/Condition mechanics
rules origin    reusable rule identity that created/defines sameness
source          concrete source instance
causal origin   concrete execution/event occurrence
```

Application-family/reapplication/arbitration may depend on the **rules origin** rather than Effect template identity. Yet `world-effect-state.schema.json` currently validates `rules_origin_id` only as a machine-like string.

This permits semantically meaningless state and gives the loader no typed invariant for application-family derivation.

### Required reference semantics

`rules_origin_id`, when present, must resolve in the same `ResolvedCatalogContext` to a reusable definition that is the mechanically relevant rules origin for the application.

The minimum family derivation is:

```text
Condition application:
    family = Condition definition identity unless a future registered grouping policy says otherwise

non-Condition Effect with explicit rules_origin_id:
    family = rules_origin_id

otherwise direct generic Effect:
    family = Effect definition identity
```

`source_id` remains the concrete world/source identity and does not replace rules origin. Same-spell applications from different casters therefore share family while preserving distinct sources.

Exact allowed rules-bearing definition kinds can be compiler metadata rather than encoded by ID spelling; a reusable definition ID's kind is known from the ResolvedCatalogContext.

A causal occurrence/Event/segment ID is **not** the same field. Step 3 still owns causal execution identity and mechanical recency.

## 5. Finding B-F3 — closed terminal reason registry is not enforced by the Effect state schema

**Severity: MODERATE machine-contract gap.**

`core-catalog.json` has a closed initial set:

```text
effect_end.expired
effect_end.removed
effect_end.replaced
effect_end.support_lost
```

but terminal `world.effect.lifecycle.terminal_reason_id` accepts any machine ID.

The schema should either enumerate the current closed values or compiler validation must explicitly enforce registry membership. Since this is a fixed Step-2 registry today, schema-enumerating the values is the simplest current contract. Future registry expansion updates schema/catalog together.

## 6. Causal origin and mechanical recency

**Coverage: DEFERRED_OK, critical carry-forward to Step 3.**

`potency_then_recency` cannot use wall-clock time, SQL row order, or arbitrary Effect ID lexical order. It requires committed causal/mechanical ordering.

The current Effect schema need not invent `created_at` or a duplicate application ordinal. Step 3 already owns stable segment/Event identity and causal ordering. It must ensure a durable Effect can recover the creation/last-refresh ordering facts required by registered arbitration after restart/compaction.

Acceptable implementations include a stable creator event/segment reference on the application or a durable event/index relation, but the information must survive any history compaction that still leaves overlapping applications alive.

Slice E must reject a Step-3 design that makes recency available only in ephemeral trace cache.

## 7. Source lifetime and retirement

No additional source-liveness rule is needed.

`source_id` is provenance, not structural support. An Effect whose rules permit persistence after the source dies/retires continues until its own terminal mechanisms. Entity retirement must preserve addressable/tombstoned identity sufficiently for durable provenance, or Step-5 compaction must preserve the necessary causal projection.

If rules say source disappearance ends the Effect, that rule must be represented explicitly through support/Trigger/Activity semantics rather than by making all source references structural lifecycle dependencies.

A durable Effect cannot depend on a local-only source/definition/support root when that dependency is mechanically/audit significant; publication promotion closure must resolve it.

## 8. Condition removal and provenance

The cumulative Condition design already establishes the right minimum contract:

- removal works over concrete applications/units, not a shared integer;
- provenance-sensitive eligibility uses typed rules origin/family/context;
- source-scoped removal is distinct from generic remove-count;
- if several mechanically non-equivalent eligible units remain and rules do not select one, Step 3 produces typed adjudication rather than SQL-order choice.

The current `automatic_boundary_responses.remove_count` schema intentionally does not embed a filter/query language. It is automatic only when the exact eligible result can be derived. More complex source-specific removal belongs to typed Step-3 operations.

No new Condition removal DSL is justified.

## 9. Support forest result

No official D&D/SRD case examined requires multiple simultaneous structural maintenance parents for one application. Concentration itself has one creator-maintenance episode; additional independent termination requirements remain intrinsic duration, Effect predicates, or explicit triggers rather than structural parents.

The one-parent forest remains the simplest sufficient model:

- parent suppression does not terminate children;
- parent terminal state expires descendant closure;
- child terminal state does not mutate parent;
- no reparenting; transfer creates new episode/application;
- reverse child indexes remain derived.

A future rules case requiring `child survives while ANY of parents A/B exists` or another genuine multi-parent lifetime should reopen this narrow primitive with evidence.

## 10. Zone/aura result

The one-target invariant remains compatible with spatial mechanics:

```text
persistent spatial state
    -> Effect targets Zone/Location/Asset as one lifecycle owner

independent lasting consequence on creature
    -> create one creature-local Effect application
```

Mere presence inside an aura/zone does not require a durable child Effect unless independent state/lifecycle/provenance must survive or be targeted separately. Current target-local indexes and later spatial/procedure queries can derive transient participation.

No record explosion or multi-target Effect map is required.

## 11. Terminal Effect retention

The prior Effect design already explicitly separates terminal lifecycle from physical deletion/GC. This survives assurance.

Once all end consequences/publication/audit obligations and durable references permit it, terminal/local Effects may be garbage-collected under later persistence policy. Long-term causal history belongs to committed events/traces/checkpoint history rather than requiring every terminal application to remain in active world state forever.

This prevents one-application-per-target/unit from implying unbounded active-state growth. Step 5 owns exact safe-retention/compaction mechanics.

## 12. Counterexamples attempted

### Poisoned then Petrified

Previously incomplete. Under B-F1, existing Poisoned application remains lifecycle-active but unavailable to Condition aggregation while Poisoned immunity applies. PASS.

### Petrified ends before Poisoned duration

No resurrection mutation is required. Immunity contribution disappears; the still-nonterminal Poisoned application can participate again. PASS.

### Same Effect template reused by two spells

With `rules_origin_id`, families remain distinct. Without it, definition fallback would incorrectly group them. B-F2 closes the requirement.

### Same spell from two casters

Same rules origin -> same family; different `source_id` remains provenance and supports source-sensitive removal/reapplication where explicitly configured. PASS.

### Source actor dies but spell/effect should persist

Source reference is provenance only, not automatic support. Application persists. PASS.

### Concentration creator dies

This is not generic source retirement behavior. Concentration's maintenance root ends due to LifeState/Condition rule and descendant support closure follows. PASS.

### Deep support cascade + intrinsic expiry at same boundary

Prospective descendant closure plus temporal same-time closure prevents SQL order from changing final state. Exact events belong Step 3. PASS with downstream dependency.

### Two mechanically distinct eligible Exhaustion units at Long Rest

Boundary response cannot invent a SQL-order choice. Step-3 adjudication path handles underdetermination. PASS.

### Terminal Effect accumulation over long campaign

Prior design permits GC after obligations/refs are closed; Effect world state need not retain every terminal row forever. PASS with Step-5 compaction dependency.

## 13. Recommendation

**AMEND, do not REOPEN Step 2.**

Required amendments:

1. define `condition.applicability` as both new-application gate and current Condition-application eligibility for aggregation;
2. define/validate `rules_origin_id` as a reusable-definition provenance reference and formalize application-family fallback;
3. close terminal reason validation against the registered vocabulary;
4. carry durable causal-recency availability explicitly into Step 3/Slice E.

No human decision is currently required: B-F1 follows official D&D immunity semantics and uses an already accepted availability/lifecycle split; B-F2/B-F3 formalize existing accepted concepts.

Recommendation confidence: **HIGH**.
