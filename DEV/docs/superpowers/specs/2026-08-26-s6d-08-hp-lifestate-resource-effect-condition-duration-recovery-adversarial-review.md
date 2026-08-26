# S6D-08 Step 6 — Independent Whole-Project Adversarial Solution Review

Status: **FINAL PASS — 0 BLOCKING, 0 SIGNIFICANT**

Date: 2026-08-26

Authoritative review base: `v1/engine-rearchitecture@b49135f398e130b7788068b0dc897ee4252ddc1a`

## Review scope

The review followed `DEV/PROJECT_MAP.md` through the actual Step-2 state/evaluation owners and assurance resolutions, Step-3 execution boundary, Step-5 temporal/currentness/checkpoint/GC owners, House Rules, S6D-03–07, catalogs/schemas/tests and S6D-09/S6D-11/R2.7 consumers. It inspected the Task Brief, research draft, accepted decision, collaborative review, candidate, proposed canonical owner, changed Actor schema and package files, the new mechanical-state seed and focused test. Production runtime execution was not required; implementable architecture and machine-contract closure were.

## BLOCKING findings

### B1 — The new machine seed is outside package content identity and reconstruction

`HEALTH_EFFECTS_RECOVERY.md` calls `health-effects-recovery-seed.json` the exact bounded machine seed, but `character-capabilities.json` still binds only `character-mvp-seed.json` through `content_file` and `content_sha256`. No manifest member, dependency digest or compiler input binds the new file. A package can therefore pass its current content identity while this supposed authority is absent, stale or modified. The candidate statement that package identity changed because `resource.hit_points` was removed does not bind the new S6D-08 contract.

Required repair: incorporate the S6D-08 seed into the accepted package content identity/compiler-source closure (for example an identity-bound closed content-file set with per-file digests and aggregate content identity), validate exact presence/digest/profile/catalog-generation compatibility, and add negative tests for missing, extra and modified S6D-08 content. Keep production S6D-11 loading deferred, but machine reconstruction inputs cannot remain unauthenticated.

### B2 — Actor schema does not bind health/LifeState state to a LifeStatePolicy or enforce a legal cross-field state

`world-actor-state.schema.json` requires `life_state_id` when `hp` exists, but does not require `life_state_policy_id`; an Actor can therefore carry material HP/LifeState without the policy that the canonical owner says exclusively controls transitions. It also permits semantically contradictory states such as active with current HP 0, dying with positive HP, dead with positive HP, or temporary/max/current combinations that violate the selected policy. Those are not merely runtime checks unless an exact named validator contract owns them; no such machine route is present in the candidate.

Required repair: require the policy identity whenever material health/LifeState exists and define the exact policy validation contract for HP/LifeState/progress cross-field invariants. Add schema/conformance negatives for missing policy and contradictory active/dying/stable/dead health states. Do not encode HP arithmetic as a second LifeState owner; route validation to the bound policy.

### B3 — Required zero-HP/death/stabilization semantics are materially incomplete

The machine table contains only damage-to-zero, healing-from-zero and third-success/third-failure transitions. The Task Brief explicitly requires damage while at zero and death. The candidate omits at least the supported character-like rules for instant death from remaining damage, damage while dying causing death-save failures (including critical-hit consequences), death-save natural-result behavior, and the stable creature's delayed recovery contract. `STABLE_RECOVERY_BINDING` is only a label: no exact RNG-backed duration/TemporalBinding, fixed retry evidence or due transition is defined. The acceptance text also says unconsciousness is derived from Effect sources but supplies no exact Effect source/application/removal route tied to dying/stable state, so a zero-HP Actor can be `life.dying` without the claimed unconscious aggregate.

Required repair: provide an item-level LifeState transition table with exact preconditions, arithmetic inputs, failure/success increments, immediate transitions and events; define the stable recovery RNG/TemporalBinding/retry route; and specify how dying/stable creates or supplies the applicable unconscious Condition source without duplicating LifeState. If any rule is intentionally unsupported, narrow the profile and acceptance criteria explicitly rather than calling the character-like policy/playable death path closed.

### B4 — `condition.exhaustion` is activated as a partial counter without its intrinsic mechanics or terminal consequence

The seed presents Exhaustion as a supported cumulative Condition with range 0–6 and long-rest decrement, but does not define the per-level mechanical contributions or the level-6 death consequence. A cumulative count alone is not an exact D&D Condition contract, and the focused test checks only the aggregation label. This risks making an admitted condition appear playable while selectors, speed and LifeState behavior remain undefined.

Required repair: either mark Exhaustion `CONFORMANCE_ONLY_NONSELECTABLE` like concentration and use a neutral synthetic cumulative case, or close the exact supported Exhaustion selector/accessor/rule-element and level-6 LifeState transition dependencies with admission and negative tests. Long-rest decrement alone is insufficient activation evidence.

## SIGNIFICANT findings

### S1 — Maximum-HP and Resource invariants are underconstrained

The brief requires maximum-HP interaction, but the machine seed defines only damage and healing. It does not state what happens when `maximum_adjustment` changes below current HP, whether maximum can fall below zero/one for the selected policy, or how temporary HP interacts with maximum changes. The Actor schema also permits fractional `ResourceState.current` and has no machine link from each resource instance to its definition-selected storage/lifetime/capacity, while the supported pools are discrete bounded uses.

Required repair: add exact maximum-change normalization and same-segment LifeState implications; constrain supported resource instances to integer bounded state and bind each to its admitted ResourceDefinition/lifetime owner/capacity. Add over-capacity, negative/fractional and max-reduction tests.

### S2 — Verification is declarative self-assertion, not schema/catalog/behavioral conformance

The ten tests read strings from the new seed and inspect selected schema fragments. They do not validate the changed Actor schema with Draft 2020-12 and resolved `temporal-binding` refs, validate the new seed against a strict schema, cross-check package identity, execute reference state transitions, test retry/idempotency, rebuild agenda/DAG/aggregates, or prove catalog registration/admission equality. No negative state fixture is exercised.

Required repair: create a strict schema for the machine seed; validate all changed artifacts and refs; add reference transition functions/fixtures for damage, healing, death saves, stable recovery, rest responders, effect replace/expiry/support loss and recovery reconstruction; add adversarial duplicate/ordering/retry/missing-evidence cases and catalog-aware nonselectability tests. Production runtime remains out of scope.

## Findings that pass

- Mutable ownership is correctly separated: Actor HP/LifeState, owner-local Resources, world Effects and derived Conditions.
- HP is no longer modeled as a generic Resource.
- ExecutionSegment, MechanicalEvent and receipt ownership remains intact.
- RestPolicy emits qualification/completion boundaries without cross-domain mutation.
- Temporal Agenda and dependency DAG are explicitly disposable indexes; no background scheduler, global queue or campaign-wide scan is introduced.
- The exact S6D-07 Innate Sorcery and Action Surge authority boundaries are preserved, and no new Activity primitive is activated.
- Periodic content and generic concentration content remain nonselectable.

## Human decision

No new human product decision is required to repair these findings. Existing accepted scope and D&D character-like semantics determine the fail-closed corrections. A human decision is necessary only if the supported death/Exhaustion profile is intentionally reduced.

## Verdict

**FAIL — 4 BLOCKING, 2 SIGNIFICANT.** Do not proceed to the Resolution Gate or canonicalization while these findings remain unresolved.

---

## Re-review after B1–B4/S1–S2 repairs

Status: **FAIL — 3 BLOCKING, 1 SIGNIFICANT**

The package content-set identity, policy requirement/cross-field validator, massive-damage/death-save/stable-recovery cases, Exhaustion quarantine, maximum/resource checks and strict seed/reference test harness close substantial parts of the original review. All 20 focused tests pass. The following whole-project gaps remain in the current implementation.

### B1 — LifeState-owned unconsciousness is still written into an invalid Actor-side pseudo-store

`HEALTH_EFFECTS_RECOVERY.md` and the seed correctly assign an unconscious application to `WORLD_EFFECT` and forbid a mutable Actor condition list. The reference transitions instead call `_set_unconscious()`, which inserts `effect_changes` inside the Actor dictionary. `world-actor-state.schema.json` has `additionalProperties: false` and no `effect_changes` member, so the returned Actor is schema-invalid. The health validator ignores unknown fields, allowing the tests to pass while introducing a second Actor-local Effect mutation channel. No stable world.effect identity, rules origin, lifecycle or atomic sibling prospective change is produced.

Required repair: keep the Actor output schema-valid and return an explicit segment-local owner-change set separate from Actor state. The LifeState policy must propose a stable, schema-valid world.effect application/termination (definition, target, policy rules origin, instance key, lifecycle and support/temporal fields as applicable) in the same ExecutionSegment as the Actor transition. Add schema validation of every returned Actor and tests proving atomic Actor+Effect candidates and idempotent retry without an Actor condition/effect list.

### B2 — Damage to a stable zero-HP Actor loses the required damage-at-zero consequence

`apply_damage()` applies the damage-at-zero failure path only when state is exactly `life.dying`. A stable Actor at zero follows the ordinary branch, re-enters dying and initializes death saves to 0/0. The supported rules require stability to end on damage and the zero-HP damage consequence to be applied; critical/massive behavior must remain consistent. This omission contradicts the required stabilization/damage-at-zero walkthrough and can materially delay death.

Required repair: make zero-HP damage policy-owned for both dying and stable states. Define exact stable→dying progress for ordinary and critical damage, retain massive-damage immediate death, and add ordinary/critical/massive stable-damage tests plus retry evidence.

### B3 — The S6D-07 Second Wind resource/recovery contract is not the supported 2024 bounded pool

The current character seed defines `resource.second_wind` capacity 1 and S6D-08 restores it to capacity on short-rest completion only. The selected 2024 Fighter 1–2 path has a multi-use Second Wind pool and distinguishes short-rest recovery of one expended use from long-rest restoration. `resource_recovery.restore_to_capacity` on every short rest collapses those semantics and also affects Tactical Mind, which spends the same pool. The research draft labels this inherited contract accepted without item-level rules evidence, so the error is propagated rather than reconciled.

Required repair: reconcile against the exact supported Fighter definition evidence, encode the correct level-appropriate capacity and separate short-rest `restore_amount(1)` from long-rest restore-to-capacity behavior, then update Actor fixtures, package digest, responder matrix and boundary tests (including partially spent and fully spent pools). If the package intentionally supports a nonstandard one-use profile, that is a House Rule/product decision and must be named rather than presented as the SRD-based Fighter.

### S1 — New transition tests still do not validate their outputs against the changed schemas

The strict seed schema is validated, but Actor outputs from damage/healing/max/death/stable functions are checked only by `validate_actor_health()`, not Draft-2020-12 validation against `world-actor-state.schema.json` and resolved TemporalBinding refs. This is why the illegal `effect_changes` field survives. Effect outputs likewise are not validated against the canonical world Effect schema.

Required repair: run canonical schema validation on every reference input/output owner record, including stable TemporalBinding and world.effect application/lifecycle records; add mutation-negative fixtures for extra fields, wrong owners and malformed effect identity/bindings.

## Re-review verdict

**FAIL — 3 BLOCKING, 1 SIGNIFICANT remain.** Package identity and most original semantics are repaired, but the current reference contract still duplicates Effect authority in Actor state, mishandles damage to stable creatures and misstates the selected Fighter's Second Wind pool/recovery.

---

## Re-review after repair round 2

Status: **FAIL — 1 BLOCKING, 1 SIGNIFICANT**

Fresh execution of the S6D-08 suite passes all 20 focused tests. The separate world Effect change set, stable-at-zero damage paths, two-use shared Second Wind/Tactical Mind pool, content-set identity and S6D-07 regression repairs close the prior B1–B3 behavior findings. Two canonicalization gaps remain.

### B1 — The proposed canonical owner still contradicts the repaired Second Wind machine contract

`DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` line 56 still says that Second Wind and Action Surge both “use pools restore to capacity on short-rest completion.” The repaired package and S6D-08 seed instead correctly give `resource.second_wind` capacity 2, `restore_amount(1)` on `boundary.short_rest_complete`, and restore-to-capacity only on long-rest completion. Because this document is the proposed canonical semantic owner, publishing it would leave two authoritative answers for the same supported resource despite the JSON and focused assertions being correct.

Required repair: change the canonical recovery bullet to state the exact separate policies: Second Wind restores one expended use on short-rest completion and restores to capacity on long-rest completion; Action Surge restores to capacity on short-rest completion. Add a test that asserts the canonical statement or an exact structured owner route so prose/machine drift cannot recur.

### S1 — Output validation is still a hand-written subset, not canonical schema/$ref validation

`validate_actor_and_effect_outputs()` does not evaluate `world-actor-state.schema.json` or `world-effect-state.schema.json` as JSON Schema. It compares top-level key sets and calls `validate_actor_health`; for Effect state it checks required/allowed keys and one exact lifecycle value, but does not enforce referenced machine-ID patterns, property types, `temporal-binding.schema.json`, lifecycle alternatives or the schema's conditional rules. It also specially exempts Actor `id` even though the passed state schema has `additionalProperties: false`, showing that envelope/state separation is not actually being validated against their canonical owners. The currently generated unconscious Effect happens to satisfy the visible shape, but the claimed canonical-output assurance remains false and malformed referenced members can pass.

Required repair: validate the Actor envelope/state at its correct boundary and every created world Effect state with Draft 2020-12 plus the repository schema store/resolver for transitive `$ref`s. Retain the policy cross-field validator as an additional semantic check. Add negative mutations for invalid machine IDs, wrong scalar/object types, malformed lifecycle, malformed TemporalBinding and envelope/state mixing.

## Final re-review verdict

**FAIL — 1 BLOCKING, 1 SIGNIFICANT remain.** No new human product decision is required. The repaired behavior is coherent, but the proposed canonical prose and its schema-conformance evidence are not yet safe to publish.

---

## Final re-review after canonical-owner and schema-validation repairs

Status: **PASS — 0 BLOCKING, 0 SIGNIFICANT**

The final repair closes both remaining findings:

- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` now states the exact supported shared Second Wind/Tactical Mind pool contract: capacity two, regain one expended use on short-rest completion and restore to capacity on long-rest completion. Action Surge remains a distinct short-rest restore-to-capacity responder.
- `validate_actor_and_effect_outputs()` now constructs canonical `world.actor` and `world.effect` envelopes and validates them through `world-record.schema.json`. `CanonicalSchemaValidator` resolves the repository schema store and transitive `$ref`s and now enforces `dependentRequired`; the policy validator remains the additional cross-field semantic gate. Negative tests reject an invalid machine ID and an Actor-local pseudo Effect field.

Fresh combined verification:

`python -m unittest DEV.TESTS.test_s6d_08_health_effects_recovery_contract DEV.TESTS.test_s6d_07_character_mvp_seed`

Result: **36 tests run, 36 passed**.

No new whole-project conflict, authority leak, activation leak, package-identity gap or unresolved human product decision was found in the repaired candidate.

## Final verdict

**PASS — 0 BLOCKING, 0 SIGNIFICANT.** The candidate may proceed to the Step-7 Resolution Gate; this review does not itself approve or publish it.

