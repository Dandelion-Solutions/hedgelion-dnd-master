# Character Progression and READY_PC Seed

Status: **CANONICAL S6D-07 OWNER**

Realization boundary: **CANONICAL ARCHITECTURE AND MACHINE CONTRACT; PRODUCTION RUNTIME DEFERRED TO IMPLEMENTATION PLANNING**

## Scope

This owner defines character-definition grants and stable choices, sparse Actor build bindings, the initial READY_PC dependency frontier, bounded advancement reconstruction and the built-in MVP character capability declaration. It does not own HP/LifeState/resource/effect internals, execution commit/event/receipt/recovery, UI/dialogue, or broad D&D corpus coverage.

## Laws

1. Definitions own reusable grants, prerequisites and owner-relative choice slots. Actor owns accepted anchors and selections; flattened sheet fields are derived projections only.
2. Every choice ID is stable within its owning definition revision and accepted catalog context. Option IDs do not become globally interchangeable merely because their strings match.
3. Initial selections are fixed before relevant situational exposure. Rules-valid inference, deterministic defaults and accepted delegation are recorded selection bases, not hidden LLM authority.
4. Provisional gameplay may precede READY_PC. An attempted mechanic is permitted only when its local committed dependencies are sufficient.
5. READY_PC requires a uniquely reconstructable legal initial build, all material initial choices closed, and every selected mechanical dependency admitted. It does not require a completed questionnaire or persisted derived sheet.
6. Future advancement is not initial debt. A choice becomes blocking only when its actual acquisition boundary opens.
7. Advancement validates and publishes through the existing atomic, idempotent execution/durability path; this owner creates no workflow queue or independent pending-state lifecycle.
8. Unsupported character content is absent/nonselectable. Package provenance or identity never implies complete SRD content.
9. The built-in `character.mvp_vertical_slice.v1` profile is exhaustive at Human + Criminal + Fighter 1–2 + Sorcerer 1 and the exact transitive items declared by its machine seed.
10. Activity primitive registration is not activation. S6D-07 replaces exactly eleven S6D-06 base rows with `COMPLETE / ACTIVE_ADMITTED` contracts after exact consumers and dependencies are closed, including one bounded compiler form and one closed Action Surge `op.emit_fact` variant; a side overlay cannot activate a quarantined row. Every other primitive remains quarantined.
11. Package compilation fails closed on an unresolved definition/activity/asset/resource/proficiency/value reference, a quarantined primitive, duplicate slot/binding/option, illegal cardinality/default, failed prerequisite or catalog-context mismatch.
12. Concept/prose and GM adjudication may supply only accepted input facts. They cannot author grants, RNG, arithmetic, mutation or commit disposition.

## Reconstruction

```text
accepted ResolvedCatalogContext
-> species/background/class anchors + level
-> applicable grants and opened choice slots
-> accepted sparse Actor bindings and spell state
-> admitted Assets/resources/Activities/primitives
-> uniquely derived health/defense/capabilities
-> READY_PC evidence or exact blocking dependency
```

## MVP acceptance

The martial route supports an inferred/defaulted Human/Criminal Fighter and at most one unresolved material Archery-versus-Defense decision. The spellcaster route supports an inferred/defaulted Human/Criminal Sorcerer with one delegated recommended six-spell bundle that can be overridden before READY_PC. Neither route may be implemented as a field-by-field questionnaire.

Fighter level 2 is the later boundary proof. It atomically adds its deterministic grants and reconstructs affected capabilities/resources without reopening the initial style.

Action Surge is machine-owned current-turn procedure state, never a prose hint or durable Actor flag. Its Activity atomically consumes one `resource.action_surge` and emits one typed entitlement for the same actor: one additional `resource.action`, consumed by the next eligible activation, excluding `activity.magic`, usable once, and expired at the current-turn boundary. Replay with the same Resolution idempotency key returns the same grant/receipt and cannot duplicate the entitlement.

Innate Sorcery uses a deliberately narrow Effect boundary needed by this real level-1 path. The admitted `attack.roll × rule.grant_advantage` pair is scoped to spell attacks and combines by the selector's accepted advantage/disadvantage cancellation policy. `effect.innate_sorcery` has a stable target/source/definition instance key, starts at its causing commit, expires one minute later in the same local chronology, atomically replaces the same instance on reapplication, and reconstructs from committed Effect evidence plus its pinned temporal binding. The Temporal Agenda owns idempotent expiry publication. This contract activates no generic Effect authoring, matching, cleanup or recovery authority; S6D-08 remains owner of the general model.

READY_PC evidence is a typed derivation attestation bound to `actor_id`, Actor `state_revision`, exact package content hash and catalog generation. Each asset, proficiency, selector result and admitted Activity claim names its canonical derivation/admission owner. The validator cross-checks the identities, definition-derived requirements, Actor-owned resources and resolved catalog membership; caller-supplied unbound lists never establish readiness.

The package's capability file is the breadth authority. `full_srd_character_corpus=false` and `ABSENT_NONSELECTABLE` are mandatory until a later reviewed package generation expands the surface.

## Implementation and acceptance boundary

S6D-07 proves the real seed's complete implementable contract. Its compiler/readiness/advancement conformance tool and fixtures validate identities, closure and owner transitions; they do not replace the future accepted resolver, Activity executor, publisher or durable repository.

After those runtime components implement this slice, behavioral acceptance must replay the martial and spellcaster fast-start walkthroughs. It must confirm that provisional play begins from locally sufficient state, READY_PC closes within the first meaningful interactions, only materially unavoidable player-owned choices are asked, and no procedural GM behavior, excessive questioning, post-exposure selection or hidden dependency appears. A failure is architecture/implementation evidence requiring reconciliation before broader content expansion.

## S6D-09 package-content amendment

S6D-09 adds `gameplay-spine-seed.json` to the same identity-bound package content set. That member adds generic check/save and bounded gameplay-spine contracts but does not change this owner's character definitions, READY_PC predicate, progression choices, representative paths or deferred behavioral fast-start proof. The senior-audit spatial repair adds exact TargetSpec/AreaSpec values and accepted `fiction.target_reachable` argument bindings to the seven existing `op.select_targets` Activity consumers; it does not add character content, Activities or primitive authority. `character-capabilities.json` binds all three members through their member digests and aggregate `content_set_sha256`; readiness evidence uses the amended aggregate identity.

