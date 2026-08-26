# S6D-09 — Domain Rules Coverage Matrix — Architecture Task Brief

Status: **STEP 1 TASK BRIEF — READY FOR HUMAN REVIEW AFTER BRIEF-CRITIC PASS**

Date: 2026-08-26

## 1. Purpose and stage boundary

S6D-09 must produce an item-level proof that every mechanic in the currently supported MVP D&D surface has one honest architecture route:

```text
FORMALIZED_DETERMINISTIC_PATH
BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC_EXECUTION_PATH
OUT_OF_SUPPORTED_MVP_SEED
```

The matrix is audit evidence and a gap detector. It is not a new rules owner, runtime registry, execution engine, product capability declaration or substitute for the canonical owners it cites. A row may prove coverage only by tracing current product/support evidence through admitted definitions and machine contracts to an accepted execution, state, event, retry and recovery route. Prose narration is never an execution path.

This artifact is Step 1 only. It frames Steps 2–8 after human approval. It does not choose new supported product semantics, expand the bounded playable seed, activate catalog vocabulary or primitives, alter canonical owners, begin S6D-10/11/12, or resume R2.7.

## 2. What “supported MVP surface” means for this loop

S6D-09 must not equate any one of these with support by itself: presence in an SRD/reference source, mention in a CORE guidance document, registration in a catalog, existence of a schema, conformance-only fixture, dormant/quarantined vocabulary, or narrative plausibility.

Step 2 must build a support-evidence ledger and reconcile these independent axes:

1. **product/runtime claim** — current shipped guidance or an accepted owner says the MVP supports the mechanic;
2. **package/content claim** — the selected identity-bound package capability and exact seed admit a concrete definition/consumer;
3. **machine realization** — selectors, accessors/facts, values, primitives, state owners and execution/recovery contracts are active for that consumer;
4. **verification state** — current tests/fixtures prove the claimed route and negative space.

A mechanic is `IN_SUPPORTED_MVP` only when current owning evidence establishes the claim and the required axes reconcile. A machine registration without an admitted consumer remains dormant/quarantined; an SRD mechanic absent from the package is not implicitly promised; a shipped product claim without a closed machine route is `SUPPORTED_GAP`, not permission to relabel the mechanic out of scope. `OUT_OF_SUPPORTED_MVP_SEED` requires affirmative current product-owner scope evidence, not package absence. If evidence leaves a materially different product-scope choice, Step 3 must present it to the human architect.

Package presence, product scope and realization are separate required columns:

```text
package_presence = PRESENT_ACTIVE | PRESENT_CONFORMANCE_ONLY | PRESENT_DORMANT_OR_QUARANTINED | ABSENT
product_scope = SUPPORTED | EXPLICITLY_OUT_OF_SCOPE | UNRESOLVED
realization = COMPLETE | SUPPORTED_GAP | NOT_APPLICABLE
```

Only `product_scope=SUPPORTED` plus `realization=COMPLETE` can receive one of the two executable-path classifications. `OUT_OF_SUPPORTED_MVP_SEED` requires `product_scope=EXPLICITLY_OUT_OF_SCOPE`. `SUPPORTED_GAP` is an interim non-exit disposition that must be resolved, explicitly deferred to a named downstream owner without overstating current support, or escalated for a human product decision before S6D-09 canonicalization.

The real Human/Criminal/Fighter 1–2/Sorcerer 1 bounded package remains the minimum playable proof already accepted by S6D-07. It is a coverage floor, not by itself the complete definition of every gameplay-domain promise made elsewhere in the product.

## 3. Governing inputs and mandatory Source Manifest route

The loop must fresh-read the current authoritative remote ref and reconstruct the complete direct-and-indirect dependency subgraph through `DEV/PROJECT_MAP.md`. At minimum the Step-2 Source Manifest must include and classify:

1. **process/status:** `AGENTS.md`, `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/PROJECT_MAP.md`, `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`, the S6D owner decision, umbrella Task Brief and execution plan, and the paused R2.7 WP-06 cursor as derivative/historical routing where current roadmap text supersedes it;
2. **ruleset/catalog identity and admission:** `RULESET_PACKAGE_IDENTITY.md`, `CATALOG_RESOLUTION.md`, `CATALOG_CONTRACTS.md`, `CATALOG_ADMISSION.md`, package manifests/capability declarations/content digests, `core-catalog.json`, `catalog-admission-ledger.json`, `entity-structures.json`, `identifier-policies.json`, their schemas and focused S6D-01/02 tests;
3. **deterministic mechanics:** `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `CALCULATION_SELECTOR_METADATA.md`, `MECHANICAL_CONTEXT.md`, `PORTABLE_ACTIVITY_VALUES.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`, `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `HEALTH_EFFECTS_RECOVERY.md`, their complete S6D-03…08 closure chains, exact machine catalogs/schemas and tests;
4. **accepted upstream architecture:** the Steps 1–2 retrospective assurance final and every current Step-2 owner it routes; Step-3 execution-boundary canonical owner plus current ExecutionSegment, MechanicalEvent, receipt, reaction/suspension/Continuation contracts; relevant Step-5 retry, durability, chronology, multiplayer and recovery owners;
5. **typed adjudication and policy:** `CAMPAIGN_HOUSE_RULES.md`, its explicit owner decision/canonicalization, `GAME/CORE/ADJUDICATION.md`, current ActionRequest/Activity binding contracts and focused policy/adjudicated-input tests. S6D-09 consumes this boundary but does not preempt S6D-10’s integrated closure responsibility;
6. **shipped mechanics/runtime guards:** `GAME/CORE/RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, `CHARACTER_READINESS.md`, `CHARACTER.md`, `DIEGETIC_ONBOARDING.md`, `COMBAT.md`, `ENCOUNTERS.md`, `MAGIC.md`, `EXPLORATION.md`, `DIALOGUE.md`, `INFORMATION.md`, `ADVANCEMENT.md`, `REWARDS.md`, `CHRONOLOGY.md`, `MULTIPLAYER.md`, `LIVE_SCENE.md`, persistence/recovery owners, `GAME/RULES/README.md`, `GAME/RULES/INDEX.md`, `GAME/RULES/OFFICIAL_SOURCES.md` and `GAME/CORE/SOURCES.md`;
7. **exact supported package and verification:** the current `hdm.rules.dnd2024-srd52-core` capability record, `character-mvp-seed.json`, `health-effects-recovery-seed.json`, every transitive definition/activity/primitive/value dependency, relevant DEV schemas/validators/tests/fixtures, and current negative/quarantine assertions;
8. **domain consumers discovered during extraction:** equipment/Asset ownership and use, procedures/action economy, targeting/movement/areas, hazards, social checks, economy/reward or any other current owner whose claim can change a matrix disposition.

Routing files, search results, roadmap summaries and earlier coverage prose are locators only. Every coverage row must cite actual current owners and preserve scope qualifiers, exceptions, non-goals, negative findings and defer/revisit triggers. Enumerated source requirements require item-level accounting.

Public repository material must remain independently worded and legally conservative. Reference material may establish mechanics/scope, but S6D-09 must not copy protected rule text or imply full-corpus coverage from package naming.

## 4. Established laws that S6D-09 must preserve

- One semantic owner per mutable fact; definitions own reusable rules, while Actor/Asset/Effect/procedure/runtime owners hold their admitted instance state.
- LLM judgment may supply only explicitly authorized typed non-engine inputs. It does not own engine state, RNG, rule resolution or commit.
- Every formalized or adjudicated mechanic ends at the same accepted deterministic ExecutionSegment → owner mutation → MechanicalEvent → receipt/trace path.
- Missing input is not false; an absent or unsupported route fails closed and cannot be completed by narration.
- Coverage does not imply activation. Twenty S6D-06 primitives remain quarantined; the eleven replacements are active only for their reviewed exact consumers unless a new Primitive Necessity Challenge is separately passed.
- S6D-07 remains a bounded architecture/machine-contract playable seed, not full SRD character content and not a completed production runtime.
- S6D-08 preserves intrinsic Actor HP/LifeState, canonical `world.effect` envelopes, derived Condition aggregation, owner-local recovery and no generic scheduler/global scan.
- Signal, StateDelta, DurationSpec, occurrences, receipts and other embedded/protocol values gain no independent lifecycle merely because a matrix row mentions them.
- House Rules/prose policy cannot execute code, queries or mutations. Reusable formalized mechanics require existing typed realization owners; one-off judgment must enter through authorized typed bindings.
- Ordinary gameplay remains bounded/local: no campaign-wide scan, mandatory network lookup, extra LLM orchestration, background queue or development-only runtime dependency.
- No compatibility layer is required for nonexistent released campaigns.

If a fresh current owner contradicts one of these statements, Step 2 must report exact precedence evidence and classify the conflict instead of silently reopening or overriding architecture.

## 5. Required evidence products and questions

### 5.1 Supported-surface ledger

Before writing the coverage matrix, enumerate every candidate mechanic claim found in the mandatory domain families and classify it as:

```text
IN_SUPPORTED_MVP
SUPPORTED_GAP
CONFORMANCE_ONLY_NONSELECTABLE
DORMANT_OR_QUARANTINED
OUT_OF_SUPPORTED_MVP_SEED
UNRESOLVED_PRODUCT_SCOPE
```

For every item record: stable item ID; mechanic family and concrete scenario; product/runtime claim owner; package/definition/consumer evidence; catalog admission/realization state; qualifiers and negative space; current verification; disposition rationale; and exact human decision trigger if one remains.

Do not derive `OUT_OF_SUPPORTED_MVP_SEED` merely from absence in the current two representative character paths when a separate current product owner promises the mechanic. Such a promise is `SUPPORTED_GAP` until realized or explicitly changed by its owner. Conversely, do not activate content merely to make the matrix broad.

Completeness must be finite and bidirectional, not inferred from family sampling. Step 2 must construct three exact typed-key sets from current sources:

```text
PACKAGE_CLOSURE_KEYS = every definition, Activity exact consumer and transitive dependency in the identity-bound selected package
ACTIVE_MACHINE_CONSUMER_KEYS = every ACTIVE_ADMITTED/selectable selector, accessor, fact, value, operation and primitive plus every declared exact consumer edge
PRODUCT_PROMISE_KEYS = every explicit current mechanic/capability promise extracted from owning GAME/architecture/product sources

REQUIRED_COVERAGE_KEYS = PACKAGE_CLOSURE_KEYS union ACTIVE_MACHINE_CONSUMER_KEYS union PRODUCT_PROMISE_KEYS
COVERAGE_LEDGER_KEYS == REQUIRED_COVERAGE_KEYS
```

Use namespace-qualified stable keys and explicit cross-links where one mechanic has entries in multiple sets. Reject duplicate/unmapped keys. Prove both directions: every source key has exactly one ledger disposition, every ledger key originates in at least one source set, every active machine consumer edge resolves to a covered admitted consumer, and every matrix machine reference resolves back to current vocabulary/package identity. Every set difference, orphan edge or contradictory cross-link becomes a named gap/conflict; zero difference is required for the final completeness claim.

### 5.2 Domain coverage matrix

Cover at minimum:

- common ability/skill checks, saving throws and contests where current rules support them;
- attacks, hit/critical resolution, damage, healing, temporary HP, zero HP, stabilization and death;
- initiative, turn/round ordering, action economy, procedure budgets, reactions and suspension/resume;
- advantage/disadvantage, proficiency/expertise or other admitted contribution/combination rules;
- movement, reach/range, targeting, line/area shapes, visibility, cover, senses and spatially adjudicated inputs;
- damage resistance, immunity, vulnerability or any admitted damage-defense transformation;
- Effects, Conditions, concentration/support relationships and duration/expiry;
- spellcasting Activities, spell attack/save routes and admitted spell/resource pools;
- equipment/Asset ownership, ownership transfer, equipping/use requirements, charges or consumable uses only where supported;
- short/long rests, boundary qualification, owner-local recovery and retry;
- initial character commitments, READY_PC and later advancement choices;
- hazards, environmental/exploration mechanics and time/resource consequences;
- social or knowledge/adjudicated checks where mechanical resolution applies;
- rewards, ownership transfer and economy mechanics actually promised by the MVP.

Each atomic matrix row must include:

```text
coverage_id
family / concrete scenario
ruleset package / content-set / profile identity and applicability
package_presence / product_scope / realization disposition
canonical consumer and definition IDs
input provenance and missing-input behavior
binding identity / frozen accepted inputs / currentness token or explicit N/A reason
selector / operation / resolver policy
accessors / invocation facts / dependency edges
Activity / primitive / reaction or owner-policy route
RNG owner and fixed-result/retry obligations
mutable owner and exact prospective mutation
ExecutionSegment / event / receipt route
typed failure IDs, failure disposition and suspension/cancellation route or explicit N/A reason
idempotency key / retry identity / conflict or revision evidence
multiplayer concurrency/currentness behavior or explicit N/A reason
suspension / chronology / durability / recovery route when applicable
route classification
positive evidence
negative-space evidence
gap / downstream owner / decision trigger
```

Split rows whenever variants have materially different input, RNG, mutation, reaction, temporal or recovery behavior. A family-level slogan is not coverage.

### 5.3 Route classification proof

`FORMALIZED_DETERMINISTIC_PATH` requires a complete admitted machine route with no semantic step delegated to prose.

`BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC_EXECUTION_PATH` requires all of:

- a named current consumer that genuinely needs semantic judgment;
- an authorized typed parameter/binding and exact provenance class;
- a proof that the adjudicated value is not engine-owned state, RNG, capability or mutation authority;
- validation/freeze/currentness behavior across retry and suspension;
- deterministic downstream evaluation/commit/event/receipt behavior;
- failure-closed handling for missing, stale or unauthorized input.

`OUT_OF_SUPPORTED_MVP_SEED` requires affirmative current product-owner scope evidence or an explicit human decision when a current product claim would otherwise be reduced. Package absence or lack of implementation alone yields `SUPPORTED_GAP`, not scope evidence.

### 5.4 Gap and conflict handling

Every supported row without a complete route becomes an exact gap item. Classify the missing owner as S6D-01…08 regression, S6D-09 local evidence/contract repair, S6D-10 policy-boundary dependency, S6D-11 integrated machine-test debt, later implementation planning, or a human product/architecture decision.

Do not reopen a completed S6D domain for thematic overlap. Reopen/amend only when the matrix proves a contradiction, an unsatisfied current consumer or an accepted contract insufficient for a supported case. Any machine-contract repair must use RED→GREEN and repeat the whole-project Step-6 review.

### 5.5 Whole-project bidirectional consistency

Check upstream and downstream effects:

- upstream: package identity/admission, Step-2 ownership, Step-3 execution, Step-5 recovery/currentness, House Rules and S6D-01…08;
- lateral runtime: all CORE modules that claim, route, narrate or persist the mechanic;
- downstream: S6D-10 typed ruling integration, S6D-11 test closure, S6D-12 final adversarial closure, paused R2.7 WP-06, implementation planning and eventual behavioral playability verification.

The review must actively search for product prose that overpromises machine support, machine vocabulary with no product consumer, and apparently covered rows whose hidden spatial, reaction, ownership, temporal, multiplayer or recovery dependency changes the result.

## 6. Required Steps 2–8 outputs

1. **Step 2 — Research & architecture draft:** complete Source Manifest; support-evidence ledger; itemized candidate surface; preliminary atomic coverage matrix; route/gap/conflict ledger; inherited S6D-01…08 dependency ledger; exact recommendation and alternatives only where evidence leaves real choices.
2. **Step 3 — Decision Brief:** only materially different product scope, supported semantics, authority or risk choices. If no human choice remains, record the evidence-based no-decision result.
3. **Step 4 — Collaborative review:** challenge completeness, row atomicity, source/support evidence, route classifications, negative space and implementation-facing clarity; repair all blocking/significant findings.
4. **Step 5 — Candidate specification and authorized RED→GREEN realization:** define the matrix contract and close only proven local gaps. An affected S6D-01…08 owner may be amended only through that owner’s explicit regression/amendment gate, RED→GREEN evidence and renewed independent whole-project review; matrix-local evidence cannot itself activate vocabulary/content or supersede the owner. The matrix remains non-normative audit evidence.
5. **Step 6 — Independent whole-project adversarial solution review:** attack omitted mechanics, false support/out-of-scope classifications, narration-as-engine, incomplete machine paths, activation leaks, duplicate owners, arbitrary input/query/mutation, RNG/retry/reaction/temporal/multiplayer gaps and runtime product overclaims.
6. **Step 7 — Resolution Gate:** reconcile every finding and candidate item with fresh evidence. Zero unresolved `BLOCKING` or `SIGNIFICANT` findings is mandatory before canonicalization.
7. **Step 8 — Canonicalization/publication:** update only affected owners/contracts/tests and project routing; publish/read back the full chain and stop before S6D-10.

Both the Step-1 brief critic and Step-6 solution critic must begin from `DEV/PROJECT_MAP.md`, reconstruct the entire relevant direct-and-indirect dependency subgraph, inspect actual owners/consumers/tests and report `BLOCKING`, `SIGNIFICANT` and `MINOR` findings. Module-local review is invalid. Step 4 uses the same whole-project discipline collaboratively; Step 7 records resolution rather than replacing independent review.

## 7. Required acceptance walkthroughs

Before canonicalization, trace at least these representative routes end to end, or explicitly prove the scenario outside the supported MVP with valid scope evidence:

1. a common check whose difficulty or contextual premise requires bounded GM judgment, followed by deterministic roll/resolution and retry-safe evidence;
2. a saving throw or contested/opposed interaction, with exact current-rules applicability rather than assumed legacy semantics;
3. martial attack through targeting, roll/critical result, damage, HP/LifeState transition, event and receipt;
4. a reaction opportunity that suspends/resumes without rerolling or duplicating mutation;
5. movement/range/area case showing which spatial facts are engine-owned and which may be typed adjudication inputs;
6. spellcasting case covering spell selection, target/save or attack, resource cost, Effect/duration when present and recovery;
7. equipment/ownership/use case, if supported, without creating a second inventory or Resource owner;
8. Short or Long Rest qualification followed by exact owner-local responders and idempotent recovery;
9. initial READY_PC closure and one later advancement choice without opportunistic retrofitting;
10. hazard/exploration consequence using typed judgment where needed and deterministic mechanical application;
11. social/adjudicated check whose prose outcome remains distinct from mechanical state mutation;
12. supported reward/ownership/economy transition, or affirmative evidence that the concrete mechanic is outside the bounded MVP.

These are architecture and machine-contract walkthroughs, not production runtime tests. They must expose missing dependencies instead of filling them with procedural GM behavior.

## 8. Non-goals

- full SRD/PHB/DMG/bestiary/spell/equipment corpus coverage;
- redefining the supported product baseline without a human decision;
- adding representative content solely for breadth;
- production gameplay runtime, UI, combat orchestration or scripted GM behavior;
- a universal rules DSL, generic state mutation language, general query engine, scheduler, event queue or campaign-wide scan;
- activating dormant definitions, selectors, facts, values or primitives because a matrix category exists;
- treating narrative plausibility, schema existence or catalog registration as execution proof;
- copying external rule text into public HDM artifacts;
- S6D-10, S6D-11, S6D-12 or R2.7 execution.

## 9. Human decision and stop conditions

Stop for the human architect only when evidence leaves a material choice about supported mechanics/content, product behavior, semantic authority, a deliberate MVP scope reduction/expansion or nontrivial risk acceptance. Before stopping, exhaust repository evidence and present established facts, exact affected rows, viable alternatives, recommendation, consequences and the precise decision required.

Do not stop for repository discovery, corpus size, matrix bookkeeping, source-role classification, technical route reconciliation, test design, naming or representation choices dictated by accepted owners.

## 10. Step-1 exit gate

Step 1 closes only when:

- a whole-project brief-critic has reviewed this brief against the current remote dependency graph and actual owners/consumers;
- every `BLOCKING` and `SIGNIFICANT` finding is repaired or explicitly resolved;
- the final brief and critic record are published to the authoritative branch and read back;
- `DEV/PROJECT_MAP.md` routes S6D-09 through the brief and mandatory whole-project source graph;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` records S6D-09 Step 1 complete and Step 2 next;
- no Step-2 research draft, Decision Brief, candidate, matrix or machine-contract change has begun.

