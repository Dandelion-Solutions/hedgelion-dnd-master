# S6D-07 Step 6 — Independent Whole-Project Adversarial Review

Status: **FAIL — 4 BLOCKING, 2 SIGNIFICANT**

Date: 2026-08-26

## Review scope

The review followed `DEV/PROJECT_MAP.md` through the character/onboarding/readiness and advancement owners, Actor/Asset/Effect and catalog/package ownership, S6D-01–06, Step-3 execution and Step-5 recovery, House Rules, schemas, tests and runtime/package consumers. It then inspected the candidate specification, collaborative review, proposed canonical owner, package files, primitive activation overlay and focused test item by item.

## BLOCKING findings

### B1 — The activation overlay cannot activate quarantined S6D-06 drafts

`DEV/CATALOG/activity-primitive-activations.json` marks five primitives `ACTIVE_SELECTABLE` while its policy says the S6D-06 base contract is unchanged. The current S6D-06 owner, catalog, schema and tests deliberately classify all 31 rows `QUARANTINED`, grant zero execution authority, and require replacement plus whole-project re-review before activation. A consumer overlay cannot change selection state while leaving `realization_state=QUARANTINED`; this is exactly the bypass S6D-06 closed. The candidate therefore has no executable attack/save/damage path, and its READY_PC/playability claims are false.

Required correction: remove the five activations and reduce the supported seed to non-executable character data, or replace each needed primitive draft with an exact `COMPLETE` owner-local contract, close every prior S6D-06 evidence obligation, synchronize the base catalog/schema/tests, and submit those replacements to independent whole-project review before any activation ledger may select them.

### B2 — `character-mvp-seed.json` is a second inventory, not canonical definitions

The file embeds 24 abbreviated objects under a private `definitions` array. They are not individual catalog definitions validated against the existing species/background/class/advancement/feat/feature/spell schemas; most contain only `id`, `kind` and loose `references`. There is no package manifest/catalog builder/loader route proving these objects become the unique definitions in a `ResolvedCatalogContext`. The test proves equality only between `exact_definition_ids` and the same file's embedded array. This duplicates inventory and bypasses the accepted catalog-definition authority rather than realizing it.

Required correction: materialize each supported item in the canonical definition storage/layout and strict schema, include it through the accepted package/catalog construction route, and prove bidirectional equality between the resolved catalog and the capability declaration. If S6D-11 still owns the physical builder/manifest/lock, label this as a non-runtime admission plan and withdraw playable/READY_PC claims until that route exists.

### B3 — External and transitive dependencies are asserted, not admitted or realized

The seed treats every string in `external_dependency_ids` as admitted. Repository search finds the proposed activity, asset, proficiency, resource, size and ability IDs only in this self-declared seed/activation overlay, not as schema-valid definitions or admitted package content. In particular, no exact Activity definitions exist for the listed weapon attack, six spells or feature activities, and no machine contracts establish their parameters, selectors/accessors, costs, resources, targeting, effects or transitions. The focused test constructs `admitted = definitions | external_dependency_ids`, so the claimant supplies its own proof.

Required correction: produce an item-level transitive closure from each canonical definition through actual resolved catalog entries and current admission/realization/selectability ledgers. Every external ID needs an owning artifact, strict schema, package namespace, active disposition and executable consumer where playability is claimed. Missing items must be implemented in their owning S6D domain or the dependent feature/spell/profile claim removed.

### B4 — READY_PC and advancement are not machine-proven

`ready_pc.required_evidence` and `advancement_proof` are labels, not predicates or transitions. No Actor fixture supplies accepted build anchors and owner-relative bindings; no derivation proves legal abilities, assets, HP/LifeState, defense, proficiencies, resources, slots or spell state; no negative evidence identifies the exact blocker. Fighter 1→2 merely declares `ATOMIC_IDEMPOTENT_ACTOR_RECONSTRUCTION` and two grant IDs without an accepted command/ExecutionSegment/MechanicalEvent/receipt/Continuation/recovery trace. This cannot satisfy the current `CHARACTER_READINESS.md`, Actor ownership or Step-3/Step-5 contracts.

Required correction: add schema-valid initial and advanced Actor/Asset/resource fixtures under pinned catalog identity; implement the exact readiness predicate/evidence matrix and local provisional-mechanics gate; trace advancement through the actual accepted execution/publication/retry/recovery artifacts. Until then the capability profile must not call either route READY_PC or playable.

## SIGNIFICANT findings

### S1 — The test suite is circular and does not validate authoritative schemas or consumers

`DEV/TESTS/test_s6d_07_character_mvp_seed.py` checks hand-written keys and set membership only. It does not run JSON Schema validation, resolve package/catalog references, load a `ResolvedCatalogContext`, validate Actor state, exercise readiness, compile Activities, check primitive base realization, or test execution/recovery. Its primitive test explicitly accepts `ACTIVE_SELECTABLE` without opening the S6D-06 catalog. Thus the reported TDD pass cannot support the candidate's closure claims.

Required correction: validate all artifacts against their canonical schemas; build/load the package through the real resolver; compare against admission ledgers; add positive and adversarial Actor/readiness/advancement cases; and assert that a quarantined primitive always blocks compilation regardless of overlay.

### S2 — Package identity and capability authority are disconnected

`character-capabilities.json` declares a profile, but no accepted package manifest, content identity/generation binding or catalog snapshot incorporates that declaration. `NOTICE.md` and a directory name do not establish adoption or reconstruction. The candidate also calls the capability file the breadth authority although accepted catalog/package owners retain machine identity and resolved-content authority.

Required correction: make the capability declaration a schema-valid, identity-bound package component consumed by the accepted builder/loader, or state it is a non-runtime plan pending S6D-11. Prove snapshot reconstruction and campaign adoption cannot infer broader SRD content.

## Findings that passed

- The candidate preserves the canonical progressive-onboarding rule: provisional locally sufficient play may precede READY_PC. It does not repeat the stale `CHARACTER_READINESS_CASES` C08 prohibition.
- Sparse Actor bindings versus definition-owned reusable choices is consistent with accepted ownership in principle.
- The proposed initial-versus-future choice distinction and no-post-exposure-selection law are correctly stated.
- No separate generic workflow queue, Signal lifecycle, StateDelta lifecycle, query engine or LLM mutation authority is explicitly introduced.

## Human decision

No new human product decision is required to repair these findings. The accepted owners force a fail-closed result: either reduce the profile to what is genuinely realized, or complete and independently review the missing canonical definitions, dependencies and primitive contracts. A human decision is needed only if the desired supported profile itself is changed.

## Verdict

**FAIL.** The candidate must not proceed to resolution/canonicalization while any BLOCKING or SIGNIFICANT finding remains.

---

## Second-pass re-review after repairs

Status: **FAIL — 4 BLOCKING, 2 SIGNIFICANT remain**

The second pass inspected the amended S6D-06 base catalog/schema/owner, the S6D-04 admission ledger, the expanded seed and Activity records, content hash, Actor/readiness/advancement fixtures and focused test. Deleting the overlay is correct, but moving activation into the base catalog does not itself prove the formerly quarantined contracts or their dependency closure.

### B1 remains — seven base activations are not proven replacements

The amended catalog now marks `op.select_targets`, `op.roll`, `op.resolve_attack`, `op.resolve_save`, `op.apply_damage`, `op.apply_healing` and `op.consume_resource` `COMPLETE / ACTIVE_ADMITTED`. Their executable rows still contain the same generic four-code failure templates and the same incomplete subject/authority semantics that caused S6D-06 quarantine. More importantly, attack/save/damage/healing rows read selectors such as `attack.roll`, `save.roll`, `defense.armor_class`, `damage.received` and `healing.received` without proving those selectors active and complete; the accepted S6D-03 result activated only its narrowly proven selector surface and left the unsupported pairs dormant. The focused S6D-07 test checks only primitive row state and argument names, not the selector/accessor/admission closure.

Required repair: either restore all seven rows to quarantine and reduce the executable profile, or provide exact replacement contracts with item-specific failures/subject/storage semantics and machine-verified closure against the current selector, accessor, value, event and transition owners. Any additionally required selector pair must itself be completed and independently re-reviewed; a primitive consumer does not activate it transitively.

### B2 remains — the expanded seed is still the sole self-describing inventory

`character-mvp-seed.json` now includes `definitions`, `support_definitions`, `activity_definitions` and `value_registrations`, but these remain bespoke abbreviated records in one aggregate file. They are not validated as canonical species/background/class/advancement/feat/feature/spell/Activity definitions through the established strict schemas, and no accepted package catalog builder/loader constructs a `ResolvedCatalogContext` from them. A SHA-256 binding proves file integrity, not uniqueness of semantic ownership or successful catalog reconstruction.

Required repair: validate and load every record through the canonical definition schemas and package/catalog construction route, or explicitly downgrade the file and capability declaration to a non-runtime admission plan pending S6D-11. Bidirectional equality must compare the resolved catalog content to the capability declaration, not arrays within the same file.

### B3 remains — dependency admission is circular

The revised test defines `realized_dependencies` as the IDs in the seed's own support/activity arrays plus its own value-registration list, then asserts that this equals the seed's own `external_dependency_ids`. The S6D-04 admission ledger still owns the fixed core registry census; it does not thereby admit these new package content IDs or prove their schema, namespace, consumer and lifecycle. Activity records compile only by matching operation names and required argument keys; their referenced selectors/accessors/resources/assets/proficiencies and semantic results are not resolved through authoritative owners.

Required repair: build an external item-level dependency ledger from independent canonical sources and verify each dependency's actual admission, realization and selectability in the resolved package context. Reject any Activity whose transitive selector/accessor/value/resource/asset/proficiency dependency is dormant, absent or only declared by the claimant file.

### B4 remains — READY_PC and advancement fixtures are internally inconsistent and non-authoritative

The new Python `ready()` helper is a test-local four-condition approximation, not the canonical READY_PC predicate. It does not validate option ownership/revision, admitted spell state, assets, proficiencies, defense/resources or catalog reconstruction. The `sorcerer_ready` fixture is concretely inconsistent: its spell state selects `spell.ray_of_frost`, `spell.shocking_grasp` and `spell.acid_splash`, while the package's sole Sorcerer option grants `spell.light`, `spell.mage_hand` and `spell.prestidigitation`; the test still returns READY. The advancement fixture is a hand-authored after-image plus booleans claiming idempotency, not an executed transition/retry/recovery trace, and it drops most initial bindings/state from the level-1 Actor.

Required repair: validate schema-conformant Actor fixtures against the exact pinned option grants and full readiness dependency matrix; add negative tests for mismatched spell state and missing assets/proficiencies/resources. Execute advancement through the accepted transition/receipt/recovery path and compare retry outputs, rather than asserting prewritten evidence fields.

### S1 remains — tests still prove shape by reimplementing the claims

No JSON Schema validation, package resolver, catalog builder, authoritative READY_PC evaluator or execution/recovery implementation is invoked. The tests reproduce desired sets and a local readiness function, so they cannot detect semantic drift such as the Sorcerer spell mismatch.

Required repair: replace self-referential assertions with canonical schema validation, actual resolved-catalog construction, authoritative readiness evaluation, Activity compilation with dependency admission and executed advancement/recovery scenarios.

### S2 remains — hash binding is not package identity/adoption closure

`character-capabilities.json` now names package/version/generation and hashes the aggregate seed, which is useful integrity evidence. It still is not an accepted package manifest/lock/content identity consumed by the package builder/loader, and no campaign adoption or compatibility reconstruction test reads it. The capability file therefore cannot yet be the machine breadth authority asserted by the candidate.

Required repair: integrate it into the S6D-01/S6D-11 package identity, manifest/lock/builder/loader route and test exact reconstruction/adoption, or retain an explicit non-runtime-plan disposition.

### Second-pass conclusion

The previous findings are not closed. The overlay bypass was removed, but equivalent authority was moved into base rows without proving the quarantined contracts and dependencies. The aggregate file is richer but remains a second, self-certifying inventory. No human product decision is required: fail closed and reduce claims, or complete the canonical owner routes and re-review them.

---

## Third-pass re-review

Status: **FAIL — 4 BLOCKING, 2 SIGNIFICANT remain**

The third pass corrects one stale second-pass statement: the current sole Sorcerer option and `sorcerer_ready` Actor now agree on `fire_bolt`, `ray_of_frost`, `shocking_grasp`, `acid_splash`, `magic_missile` and `burning_hands`. The prior spell-list mismatch is closed. The focused 11-test suite passes when run from the candidate repository root. The remaining findings below arise from the current files.

### B1 remains — metadata presence is not semantic or transitive executable closure

Five formerly dormant selector IDs now have metadata rows and `ACTIVE_ADMITTED` ledger entries, but the new test checks only owner/input/trace labels. It does not prove their actual accessor/derived inputs, contribution producers, binding resolution or supported consumer semantics. The seven primitive rows still retain generic four-code failure sets and broad draft authority shapes. Adding `exact_seed_consumer_ids` and `authority_denied` proves naming equality, not exact execution behavior or recovery.

Required repair: for each active selector and primitive, provide exact bound input/dependency graphs, item-specific failure semantics, subject/storage constraints and executed positive/negative traces through the accepted Resolution/ExecutionSegment/MechanicalEvent/receipt path. Restore any row to quarantine if this cannot be proven.

### B2 remains — the custom resolver does not validate canonical schemas or construct the accepted catalog

`DEV/TOOLS/validate_character_mvp_seed.py` manufactures `{id, kind, name, data}` envelopes and checks a few hand-selected required keys (`size_options/speed`, `hit_die/advancement_id`, `levels`, and spell fields). It never loads or validates the established species/background/class/advancement/feat/feature/spell/Activity schemas, resolves their transitive `$ref`s, or invokes the accepted catalog/package builder. Consequently `support_definitions` and Activity records can be structurally or semantically invalid while this tool calls them resolved.

Required repair: validate every record with the canonical JSON Schemas and reference registry, then construct the actual `ResolvedCatalogContext` through the accepted package resolver. If that builder remains S6D-11 work, retain non-runtime-plan status and withdraw playable/READY_PC closure.

### B3 remains — the Activity programs are not actually executable and open unowned mechanics

The compiler checks only operation existence and argument-key presence. It does not resolve step exports, role bindings, value cardinality/types or selector dependencies. Concrete failures include multi-target `burning_hands`, `acid_splash` and `magic_missile` using one linear select/roll/resolve/apply sequence without bounded per-target/dart iteration or result binding; `threshold: selector.spell.save_dc` is not among the newly proven selector set; and `result.roll`/compiled symbols are never type- or provenance-checked. `ray_of_frost` and `shocking_grasp` also carry secondary movement/reaction consequences that require effect/condition/duration/reaction ownership, yet their Activities only apply damage. Feature Activities are similarly incomplete: Action Surge only consumes a resource, Tactical Mind omits failed-check gating/result recomputation/refund semantics, and Innate Sorcery omits its lasting mechanical effect.

Required repair: either remove every content item whose exact mechanics exceed the active surface, or supply schema-valid typed Activity programs with bounded iteration, exports/bindings, all required selectors and exact owner-local effect/resource/duration/reaction semantics. Compilation must reject unresolved symbols, wrong cardinality and missing semantic consequences.

### B4 remains — readiness and advancement are still local simulators, not owner-integrated proofs

`evaluate_ready_pc()` now catches exact Sorcerer spell-set mismatch, which is a real improvement, but it still hard-codes only Human and the two classes and checks anchors, three binding IDs, HP/LifeState and spell equality. It does not validate binding owner revision/options/basis, abilities, Asset/equipment/proficiency/defense/resource closure, primitive dependency closure, or the schema-valid Actor projection. `advance_fighter_to_level_2()` deep-copies a dictionary and stores a receipt in an in-memory map; it does not execute the accepted Step-3 command/segment/event/receipt contracts or Step-5 persistence, checkpoint/currentness/recovery paths. Identity equality of an in-memory cached object is not durable idempotency evidence.

Required repair: route readiness through the complete canonical dependency matrix and validated Actor/Asset state. Execute advancement with the accepted command, transition, receipt and durable retry/recovery machinery, including restart/reload and conflict/stale-revision cases.

### S1 remains — the passing tests exercise only the candidate's parallel implementation

The suite passes, but it calls the custom resolver/readiness/advancement helpers rather than canonical schemas, catalog resolver, readiness owner, runtime execution or persistence. It therefore cannot establish whole-project conformance and misses the Activity semantic gaps above.

Required repair: add integration tests against the authoritative components and negative cases for unresolved step exports/types/cardinality, dormant transitive selectors, incomplete feature consequences, invalid Actor bindings and restart recovery.

### S2 remains — content SHA still does not establish accepted package identity/adoption

The SHA/profile checks close accidental content-file substitution. They still do not create the S6D-01/S6D-11 manifest/lock/dependency/content identity, loader reconstruction or campaign adoption evidence. The custom capability JSON cannot independently become package breadth authority.

Required repair: bind the capability/content digest into the accepted manifest and lock, prove loader reconstruction and compatibility failure behavior, and test campaign adoption; otherwise keep it explicitly non-runtime.

### Third-pass conclusion

The repairs close the stale Sorcerer-list inconsistency and improve local integrity/accounting, but they do not close the whole-project execution, schema/catalog, READY_PC or durability obligations. No human decision is required: unsupported mechanics must be reduced, or their owning contracts must be completed and independently reviewed.

---

## Fourth-pass review under the clarified implementation boundary

Status: **FAIL — 3 BLOCKING, 2 SIGNIFICANT**

The accepted human clarification changes the gate: production resolver, Activity runtime and Step-3/Step-5 persistence execution are deferred to Implementation Planning. The conformance compiler/readiness/advancement helpers may be reference validators rather than runtime owners. Accordingly, the third-pass demands for production execution/restart evidence are withdrawn. The remaining findings below are architecture and machine-contract gaps that would force future implementation to invent behavior.

### B1 — `op.for_each_target` is declared but not composed into any Activity program

The four alleged consumers list `op.for_each_target` only in `data.details.compiler_forms`. Their actual `steps` arrays never invoke it and never supply its required `targets` and `steps` arguments. The validator and test count the annotation as a consumer, so exact-consumer equality passes without an executable compiler-form tree. The linear save Activities still roll/resolve/apply only once; Magic Missile still applies one damage step. This leaves target/dart binding, child-step substitution, result cardinality, segment grouping and failure propagation for future implementers to invent.

Required repair: represent compiler forms in the canonical Activity AST itself, with typed prior target export, closed child step list, per-target role/result bindings, deterministic ordering and bounds. Validate the nested tree against the `op.for_each_target` contract. A metadata annotation cannot grant compiler semantics.

### B2 — save outcome and half/no-damage behavior has no machine control contract

`thunderclap`, `acid_splash`, `poison_spray` and `burning_hands` place `op.apply_damage` after `op.resolve_save` unconditionally. `save_damage_policy` exists only as descriptive `details`; `op.branch` remains quarantined, and no active primitive or typed Activity construct owns “none on success” or “half on success.” Thus the machine contract cannot implement the stated spells without inventing conditional and damage-scaling behavior. Activating `spell.dc` does not close this control/data-flow gap.

Required repair: add an exact typed, bounded conditional/result-routing contract (whether a reviewed compiler form or an owner-approved operation) and represent the success/failure/half-damage branches in the Activity AST. Prove rounding and per-target result binding. Otherwise remove save-based spells from the playable profile.

### B3 — several selected class/feature contracts still omit their supported mechanical effect

Changing the cantrips correctly removes durable secondary spell effects. However, the Fighter/Sorcerer feature Activities remain under-specified: Action Surge only consumes a resource and never grants the action-economy entitlement; Tactical Mind consumes Second Wind and rolls but has no failed-check precondition, additive check result, success test or conditional resource retention/refund; Innate Sorcery only consumes a resource and does not express its duration, spell DC/attack advantage changes or active-state ownership. These are not deferred runtime details; they are missing architecture contracts for content the profile calls playable and for Fighter 1→2, the chosen advancement proof.

Required repair: either remove/replace the affected supported features and advancement claim, or define their exact typed Activity/Rule Element/resource/effect/duration/action-economy contracts through the existing owners. Any required S6D-08/09 surface must remain explicitly routed and cannot be treated as already playable.

### S1 — the package compiler is still a partial surrogate for canonical schemas

The implementation-boundary clarification permits a conformance compiler, but it must validate the actual machine contract. `resolve_package()` still synthesizes envelopes and checks only a few manually chosen keys rather than validating the established strict definition and Activity schemas with transitive `$ref`s. A future implementation could therefore discover schema-invalid records or divergent field meaning.

Required repair: make the reference compiler validate the canonical schemas (or generate the source from those exact schemas) and record any intentionally deferred S6D-11 manifest/loader layer separately. Production loading is not required now; canonical schema conformance is.

### S2 — READY_PC reference validation does not yet cover its own declared evidence surface

Production READY_PC execution is correctly deferred, but the reference predicate still checks only anchors, a few binding IDs, HP/LifeState and exact Sorcerer spell set. Its declared evidence includes derived defense, assets/resources and admitted mechanical dependencies, while the function does not validate those. It could certify a Fighter without equipment/defense/proficiencies or a selected path whose nested Activity dependency is unresolved.

Required repair: make the conformance predicate consume the complete machine readiness dependency matrix, including option ownership/revision/cardinality, assets/proficiencies/resources/defense and transitive Activity/selector/primitive admission. Keep runtime integration deferred.

### Fourth-pass items now accepted as deferred implementation

- The custom advancement function may remain a reference transition/receipt/idempotency model; production Step-3/Step-5 execution, durable repository retry and restart tests belong to Implementation Planning.
- The content hash plus capability identity may remain conformance identity evidence while S6D-11 supplies the production manifest/lock/builder/loader, provided the candidate does not claim those runtime components already exist.
- The mandatory behavioral fast-start test is correctly recorded as a post-runtime trigger and need not run in S6D-07.

### Fourth-pass conclusion

The new boundary is coherent and removes out-of-sequence implementation demands, but future implementers would still need to invent multi-target composition, save branching/half-damage behavior and major selected-feature semantics. Those are blocking architecture gaps, not deferred runtime evidence.

---

## Fifth-pass review

Status: **FAIL — 2 BLOCKING, 2 SIGNIFICANT**

The actual nested `op.for_each_target` AST, recursive compiler checks, typed `when` branches, full/half floor policy and effect-free cantrip substitutions close fourth-pass B1 and B2. Tactical Mind now has a coherent frozen-roll/check/conditional-consumption contract. The remaining findings are below.

### B1 — Innate Sorcery depends on an unadmitted operation and unclosed S6D-08 lifecycle

`effect.innate_sorcery` contributes `rule.grant_advantage` to `attack.roll`, but the current admission ledger explicitly records `rule.grant_advantage` as reserved/not executable, and the active `attack.roll` metadata does not admit that pair. The candidate also activates generic `op.create_effect` and claims one-minute/reapplication behavior before S6D-08 has closed Effect/Duration expiration, replacement and recovery semantics. Merely embedding `duration` and `reapplication` strings in the definition leaves expiry, same-source identity and cleanup ownership open.

Required repair: either remove Innate Sorcery from the playable level-1 Sorcerer profile, or close and independently review the exact `attack.roll × rule.grant_advantage` pair plus the narrow Effect instance identity, one-minute expiration, replacement, recovery and cleanup contract with S6D-08 ownership. `op.create_effect` may be active only for that exact closed contract; generic effect lifecycle authority remains quarantined.

### B2 — Action Surge remains descriptive metadata rather than a machine transition

`activity.feature.action_surge` executes only `op.consume_resource`. Its additional-action entitlement, current-turn scope, excluded activity family and atomic publication exist only in `data.details` strings. No typed result, transition, Rule Element, procedure-state owner or action-economy consumer receives `ONE_ADDITIONAL_ACTION_CURRENT_TURN`. Future implementation would still have to invent how the entitlement is represented, checked, consumed and cleared, and Fighter 1→2 is the selected advancement proof that introduces it.

Required repair: define an exact transient action-economy entitlement value/owner and typed Activity output or owner-local transition, including atomic resource consumption, permitted action family, one-use/current-turn expiry and retry semantics. Otherwise replace the level-2 advancement proof with a feature whose full mechanics fit the closed surface.

### S1 — canonical schema validation is still partial

The reference compiler now validates nested AST structure but still synthesizes envelopes and checks selected required keys instead of executing the established strict schemas and transitive `$ref`s. It also accepts a `when` condition when a `result` string is merely present; it does not prove the referenced export/result member exists or that `in` values belong to the result enum.

Required repair: validate every canonical definition/Activity envelope against its actual schema and resolve `$ref`s. Type-check export/member references, condition enum values, nested cardinality and compiled symbols. This is machine-contract conformance, not deferred runtime implementation.

### S2 — READY_PC evidence remains caller-asserted rather than provenance-checked

The expanded predicate checks the right categories, but accepts arbitrary `owned_asset_definition_ids`, `derived_proficiency_ids`, `selector_results` and `admitted_activity_ids` from an untyped evidence dictionary. It does not bind those facts to the Actor, catalog generation, state revision or authoritative derivation/admission owners. A caller can certify READY_PC by listing expected IDs even when the Actor/catalog does not produce them.

Required repair: define the typed readiness-evidence contract with Actor/catalog/state identity and provenance, and have the reference validator derive or cross-check every item against resolved definitions, Actor/Asset state and admission metadata. Production computation may remain deferred.

### Fifth-pass conclusion

Multi-target/save branching and Tactical Mind are now architecturally closed. Innate Sorcery's dormant selector operation/effect lifecycle and Action Surge's missing machine entitlement remain blockers. No further human product decision is required: either close those exact owner contracts or reduce/replace the affected supported features.

---

## Sixth-pass review

Status: **FAIL — 1 BLOCKING, 0 SIGNIFICANT**

The Action Surge repair is now machine-closed: `op.emit_fact` is a single typed current-turn entitlement variant, its value/read/event/failure dependencies are registered, procedure-state ownership and one-use/turn-boundary/idempotency laws are explicit, and arbitrary event authorship remains denied. The canonical schema/$ref validator, nested export/member/condition-enum checks, and Actor/revision/package-bound READY_PC evidence with provenance and derived cross-checks close the prior significant findings. The 14 focused tests pass.

### B1 — the machine `op.create_effect` contract still contradicts the claimed narrow Innate Sorcery lifecycle

The prose owner and `effect.innate_sorcery.details` now state stable `(target, source, definition)` identity, commit-pinned TemporalBinding, same-instance replacement, recovery reconstruction and Temporal Agenda expiry. The active `op.create_effect` row and its validation matrix do not encode those obligations:

- `causal_recovery` is still `NOT_APPLICABLE`;
- `chronology_barrier` is still `NOT_APPLICABLE`;
- the row has no typed TemporalBinding input/result/evidence field and only returns a generic `entity_ref`;
- `bounds` is empty and failures remain the generic four codes, with no invalid-duration/reapplication/identity/temporal-publication conflict;
- `prospective_outputs.transition_kinds` is `transition.actor_state`, although the candidate explicitly assigns stable lifecycle state to the Effect owner;
- the catalog row is structurally capable of accepting any `effect_definition_ref`; the only narrowness is consumer prose and an `authority_denied` label, not a machine const/allowlist binding to `effect.innate_sorcery`.

This leaves future implementation to choose the exact identity derivation, temporal-binding publication, replacement conflict behavior and expiry recovery despite the claimed architecture closure. It also risks granting generic S6D-08 authority through an active primitive row.

Required repair: specialize the active row/matrix to the exact `effect.innate_sorcery` definition and bound self target/source; materialize the stable instance-key derivation and commit-pinned TemporalBinding in typed arguments/results/evidence; name the Effect-owner transition and exact event; encode same-instance atomic replacement, idempotent expiry causal key/recovery owner/chronology barrier, bounds and item-specific failures. Keep every other Effect definition/use rejected until S6D-08. Add negative tests for another effect ID, mismatched target/source, invalid duration, duplicate/reapplication conflict and replay/expiry identity.

### Sixth-pass conclusion

All other prior BLOCKING/SIGNIFICANT findings are closed under the accepted architecture-plus-machine-contract boundary. S6D-07 cannot PASS while the active machine row says recovery/chronology are not applicable where the canonical owner says they are mandatory.

---

## Seventh-pass targeted review

Status: **PASS — 0 BLOCKING, 0 SIGNIFICANT**

The sole sixth-pass blocker is closed across the complete machine chain:

- the active `op.create_effect` argument contracts admit only literal `effect.innate_sorcery`, the bound self actor as both source and target, and the exact one-minute metric `DurationSpec`;
- results include the stable Effect instance key and typed `TemporalBinding`, not only a generic entity reference;
- the prospective transition is now `transition.effect_state`, with `event.effect.created`, and both are registered/admitted for this narrow consumer;
- the validation matrix defines the Effect/Temporal Agenda causal recovery owner, instance-key plus causing-segment idempotency key, retained committed event/binding, start-at-commit and same-chronology idempotent expiry barrier;
- atomicity, bounds and item-specific identity/duration failures are machine-enforced and registered;
- seed Activity arguments use the exact literal contracts, and negative tests reject another Effect ID, non-self roles and a different duration while proving stable replay/reapplication identity;
- arbitrary Effect authorship, target discovery, duration-owner bypass and direct commit remain denied, so no generic S6D-08 lifecycle authority leaks through this replacement.

The focused suite passes all 16 tests. No unresolved architecture or product question remains under the accepted architecture-plus-machine-contract boundary. Production Effect/Temporal Agenda execution and broader generic lifecycle behavior remain correctly deferred to their implementation/S6D-08 owners.

## Final Step-6 verdict

**PASS — 0 BLOCKING, 0 SIGNIFICANT.**
