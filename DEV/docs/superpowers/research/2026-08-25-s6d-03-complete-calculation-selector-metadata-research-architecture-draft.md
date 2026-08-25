# S6D-03 — Complete Calculation Selector Metadata — Research & Architecture Draft

Status: **STEP 2 COMPLETE — FINAL EVIDENCE SYNTHESIS**

Date: 2026-08-25

Preparation ref: `v1/engine-rearchitecture@4f951d242eb87bcfc42c744b2fe541862dc0cede`

## 1. Final result

All 34 selectors and 26 operations are accounted item by item.

Only three selectors have both a current canonical supported requirement and semantics that S6D-03 can close without inventing S6D-04 inputs or S6D-05 payload meaning:

- `health.maximum`;
- `resource.capacity`;
- `condition.applicability`.

Only two operations have independently proved closed pairs:

- `rule.add_flat`;
- `rule.immunity`.

Thirty-one selectors and twenty-four operations remain `DORMANT_NONSELECTABLE`. This includes `resource.recovery` and `effect.duration`: accepted architecture reserves those calculations, but their mode/unit/value semantics cannot honestly become selectable before S6D-05 shape closure.

Final whole-catalog disposition totals are **450 ACTIVE / 35 EMBEDDED / 86 DORMANT / 0 STALE**.

## 2. Source and evidence classification

The investigation followed process/roadmap/S6D owners, S6D-01/02 owners, Rule Element/Activity/Actor/Resource/Effect/Condition owners, accepted Step-2 designs, current catalogs/schemas/tests, GAME/CORE and GAME/RULES routing.

Evidence classes were applied strictly:

- accepted current semantic owner plus focused machine consumer can activate;
- a structural JSON-Schema example proves shape only;
- `test_step2_mechanical_examples.py` proves structural definition-schema acceptance only, because it never resolves selector metadata or admission;
- the historical runtime proposal and catalog model are derivation only;
- a reserved registry spelling or generic D&D relevance is not support;
- an accepted future calculation whose value semantics depend on unresolved S6D-05 shape remains dormant.

There is no semantic definition seed package under `GAME/RULES/`; only routing/source documents exist.

## 3. Why the active surface is three/two

`health.maximum` is an accepted derived calculation: base maximum plus pure contributions. `resource.capacity` is the equivalent accepted Resource calculation. Their only currently proved operation is finite-integer `rule.add_flat`, reduced by commutative sum.

`condition.applicability` is the accepted condition-application gate. `rule.immunity=true` is a monotone veto with focused current validation. Duplicate vetoes coalesce without losing provenance.

No invocation-adjudicated fact is required by these selectors. All admit only `ENGINE_STATE`, and `permitted_context_fact_ids` is exactly empty.

## 4. Why prior apparent consumers do not activate

| Surface | Classification |
|---|---|
| poisoned/frightened/grappled/exhaustion definitions in `test_step2_mechanical_examples.py` | structural schema examples; no catalog-aware selector legality |
| condition/effect/rule-element JSON Schema `examples` | illustrative structural shapes |
| `MECHANICAL_RUNTIME_PROPOSAL.md` selector names | historical proposal |
| accepted Step-2 retention of recovery/duration/cost/damage calculations | meaningful reservation, but exact S6D-03 compatibility is gated by unresolved portable/mode semantics |
| GAME/CORE prose concepts | domain requirement routing, not an exact selector/pair contract |

These references must not be deleted as if meaningless, but executable validation must reject their dormant selector/operation pairs until activated coherently.

## 5. Selector evidence ledger — exact 34

| Selector | Decision | Evidence/references | Closure |
|---|---|---|---|
| `ability.score` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `ability.modifier` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `test.roll` | DORMANT / S6D-03 trigger | `DEV/TESTS/test_step2_mechanical_examples.py` | structural/historical/unresolved; nonselectable |
| `check.roll` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `contest.roll` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `save.roll` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `initiative.roll` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `check.dc` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `save.dc` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `spell.dc` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `attack.roll` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`<br>`DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`<br>`DEV/SCHEMAS/condition-definition-data.schema.json`<br>`DEV/TESTS/test_step2_mechanical_examples.py` | structural/historical/unresolved; nonselectable |
| `attack.critical_threshold` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `defense.armor_class` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`<br>`DEV/SCHEMAS/effect-definition-data.schema.json` | structural/historical/unresolved; nonselectable |
| `damage.weapon` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/CATALOG_MODEL.md`<br>`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`<br>`DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`<br>`DEV/SCHEMAS/rule-element.schema.json` | structural/historical/unresolved; nonselectable |
| `damage.spell` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `damage.dealt` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `damage.received` | DORMANT / S6D-03 trigger | `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md` | structural/historical/unresolved; nonselectable |
| `healing.done` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `healing.received` | DORMANT / S6D-03 trigger | `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md` | structural/historical/unresolved; nonselectable |
| `resource.cost` | DORMANT / S6D-03 trigger | `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md` | structural/historical/unresolved; nonselectable |
| `resource.capacity` | ACTIVE / COMPLETE | accepted Step-2 owner + current focused validation | complete machine metadata |
| `resource.recovery` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`<br>`DEV/CATALOG/mechanical-surfaces.json`<br>`DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`<br>`DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`<br>`DEV/TESTS/test_step2_evaluation_input_contract.py` | structural/historical/unresolved; nonselectable |
| `activity.availability` | DORMANT / S6D-03 trigger | `DEV/TESTS/test_step2_mechanical_examples.py` | structural/historical/unresolved; nonselectable |
| `activity.activation` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `target.count` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `target.range` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `target.area` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `effect.duration` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`<br>`DEV/CATALOG/mechanical-surfaces.json`<br>`DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`<br>`DEV/TESTS/test_step2_evaluation_input_contract.py` | structural/historical/unresolved; nonselectable |
| `health.maximum` | ACTIVE / COMPLETE | accepted Step-2 owner + current focused validation | complete machine metadata |
| `condition.applicability` | ACTIVE / COMPLETE | accepted Step-2 owner + current focused validation | complete machine metadata |
| `movement.speed` | DORMANT / S6D-03 trigger | `DEV/TESTS/test_step2_mechanical_examples.py` | structural/historical/unresolved; nonselectable |
| `sense.range` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `proficiency.rank` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |
| `actor.trait` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | structural/historical/unresolved; nonselectable |

## 6. Operation evidence ledger — exact 26

| Operation | Decision | Evidence/references | Closure |
|---|---|---|---|
| `rule.add_flat` | ACTIVE / COMPLETE | accepted closed pair semantics + focused validation | complete pair contract |
| `rule.add_dice` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.replace_dice` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.grant_advantage` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.grant_disadvantage` | DORMANT / S6D-03 trigger | `DEV/SCHEMAS/condition-definition-data.schema.json`<br>`DEV/TESTS/test_step2_mechanical_examples.py` | no independently proven closed pair |
| `rule.set_minimum` | DORMANT / S6D-03 trigger | `DEV/CATALOG/mechanical-surfaces.json` | no independently proven closed pair |
| `rule.set_maximum` | DORMANT / S6D-03 trigger | `DEV/CATALOG/mechanical-surfaces.json` | no independently proven closed pair |
| `rule.multiply` | DORMANT / S6D-03 trigger | `DEV/CATALOG/mechanical-surfaces.json` | no independently proven closed pair |
| `rule.override` | DORMANT / S6D-03 trigger | `DEV/CATALOG/mechanical-surfaces.json`<br>`DEV/TESTS/test_step2_mechanical_examples.py` | no independently proven closed pair |
| `rule.add_damage_component` | DORMANT / S6D-03 trigger | `DEV/ARCHITECTURE/CATALOG_MODEL.md`<br>`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`<br>`DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`<br>`DEV/SCHEMAS/rule-element.schema.json` | no independently proven closed pair |
| `rule.resistance` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.immunity` | ACTIVE / COMPLETE | accepted closed pair semantics + focused validation | complete pair contract |
| `rule.vulnerability` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_cost` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_dc` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_critical` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_target` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_range` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.adjust_duration` | DORMANT / S6D-03 trigger | `DEV/CATALOG/mechanical-surfaces.json` | no independently proven closed pair |
| `rule.grant_activity` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.restrict_activity` | DORMANT / S6D-03 trigger | `DEV/TESTS/test_step2_mechanical_examples.py` | no independently proven closed pair |
| `rule.grant_movement` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.grant_sense` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.grant_proficiency` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.grant_trait` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |
| `rule.usage_gate` | DORMANT / S6D-03 trigger | no current reference outside registry/ledger | no independently proven closed pair |

## 7. Final machine contracts

### `health.maximum`

- contribution: numeric finite integer;
- result: integer, minimum 1;
- subject: `world.actor`;
- binding: subject;
- operation: `rule.add_flat`;
- combination: sum applicable values, then enforce minimum;
- inputs: `ENGINE_STATE` only.

### `resource.capacity`

- contribution: numeric finite integer;
- result: integer, minimum 0;
- subject: `world.actor|world.asset`;
- bindings: subject + resource definition;
- operation: `rule.add_flat`;
- combination: sum applicable values, then enforce minimum;
- inputs: `ENGINE_STATE` only.

### `condition.applicability`

- contribution/result: applicability boolean;
- subject: `world.actor`;
- bindings: subject + condition definition;
- operation: `rule.immunity` with literal `true`;
- combination: any true vetoes application;
- inputs: `ENGINE_STATE` only.

All three declare dependency kinds `accessor|derived`, no architecture-fixed static edges, no permitted context facts, selector-owned resolution and provenance-retaining trace.

## 8. Dependency-kind correction

The previous schema mixed dependency kinds with derived-node names. Kinds are now only `selector|accessor|derived`. Exact dependencies retain typed references such as `derived:effect_availability`. The current selectors permit `accessor|derived`. All inherited `derived_nodes` are also normalized so their kind sets contain only `selector|accessor|derived`; exact node identities remain solely in prefixed `dependencies`. `condition_intrinsic` retains its pre-existing `INVOCATION_ADJUDICATED` input class as explicitly unresolved S6D-04-owned graph state. S6D-04 owns exact fact/accessor references, binding compatibility and transitive graph closure.

No class-only claim is presented as a fact allowlist. `permitted_context_fact_ids=[]` is explicit.

## 9. S6D-05 boundary

No active pair depends on an unresolved portable payload shape. Recovery, duration, cost, damage-component and activity-restriction pairs remain dormant. S6D-05 may define portable members but cannot activate them; activation still requires a coordinated S6D-03 evidence/metadata change.

## 10. Resolver semantics

Only two policies remain:

- `integer_additive_v1`: filter predicates/gates, sum finite integer contributions as a commutative multiset, add to the selector's authoritative base, enforce selector minimum, retain all provenance. No rounding/order/override/bounds ambiguity exists.
- `immunity_any_true_v1`: any applicable literal-true immunity vetoes; duplicates coalesce semantically and retain provenance.

Serialization order is never authority. There is no damage precedence, mode combination or override policy to invent in this stage.

## 11. Mismatch resolutions

- previously active recovery/duration selectors were false-complete: demote until S6D-05 + exact S6D-03 semantics;
- min/max/multiply/override/adjust-duration operations lacked independent closed-pair evidence: demote;
- test/schema examples are labeled structural and covered by catalog-aware dormant rejection;
- selector metadata gains result constraints, subject/bindings, exact empty fact allowlist, static edges, policy owner and trace policy;
- dependency kind/reference distinction is repaired;
- admission ledger and S6D-02 verification totals update atomically.

## 12. Alternatives

A. Three/two complete active surface with explicit dormant gates — **selected**.

B. Keep five/seven active and label unresolved semantics complete — rejected as false closure.

C. Promote example-driven D&D surface — rejected as evidence laundering.

D. Remove all dormant IDs — rejected because accepted future owners/triggers remain meaningful.

## 13. Decision boundary

No human decision remains. The correction removes invented semantics rather than selecting among material rules alternatives. Concrete later seed/value evidence may trigger a new coordinated activation.
