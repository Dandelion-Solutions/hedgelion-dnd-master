# S6D-12 — Adversarial Final Closure — Step 2 Evidence Extraction

Status: **STEP 2 RESEARCH / EVIDENCE EXTRACTION — COMPLETE**

Date: 2026-08-28

## 1. Scope and method

This research executes the corrected Step-1 Task Brief and its whole-project critic. It is an item-level cross-owner reconciliation, not a redesign pass.

Current evidence was read from the active remote ref after Step-1 publication. Source roles were kept distinct:

- **CANONICAL / OWNING** — current S6D and inherited architecture owners;
- **CANONICAL AMENDMENT / OWNER DECISION** — B′ and later accepted supersessions;
- **IMPLEMENTATION / MACHINE CONTRACT / TEST** — current package, catalogs, schemas, validators and focused tests;
- **RUNTIME CONSUMER** — GAME owners whose promises/behavior consume the contracts;
- **DERIVATIVE STATUS / LOCATOR** — roadmap/project-map/closure evidence that cannot override owners;
- **HISTORICAL / SUPERSEDED** — prior aggregate-identity wording or examples retained only as provenance.

No claim below treats a schema example, nullable scaffold, illustrative hash literal, routing index or model prose as authority merely because its shape resembles a current projection.

## 2. Source Manifest

### Process / sequencing

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- S6D umbrella owner decision/task brief/decomposition plan;
- current R2.7 durable pause cursor;
- S6D-12 Step-1 Task Brief, amendment and whole-project critic.

### Current S6D owners

- `RULESET_PACKAGE_IDENTITY.md`;
- `CATALOG_ADMISSION.md`;
- `CALCULATION_SELECTOR_METADATA.md`;
- `MECHANICAL_CONTEXT.md`;
- `PORTABLE_ACTIVITY_VALUES.md`;
- `ACTIVITY_PRIMITIVE_CONTRACTS.md`;
- `CHARACTER_PROGRESSION_READY_PC_SEED.md`;
- `HEALTH_EFFECTS_RECOVERY.md`;
- `DOMAIN_RULES_COVERAGE.md`;
- `HOUSE_RULES_MECHANICAL_BOUNDARY.md`;
- `RULESET_PACKAGE_MACHINE_CLOSURE.md`;
- B′ owner decision `2026-08-28-domain-rules-coverage-derived-binding-owner-decision.md`.

### Inherited owners

- `CATALOG_CONTRACTS.md`;
- `CATALOG_RESOLUTION.md`;
- `ACCESS_CONTROL.md`;
- `BRANCH_MODEL.md`;
- accepted Step-3 execution-boundary canonical spec;
- accepted Step-5.11 retention/compaction canonical spec;
- accepted Step-5.13 owner-routed cleanup canonical spec;
- `GAME/CORE/SOURCES.md`;
- `GAME/CORE/PLAY_POLICY.md`.

### Runtime/product consumers

- `RUNTIME.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, `CHARACTER_READINESS.md`, `ADJUDICATION.md`, `COMBAT.md`, `MAGIC.md`, `EXPLORATION.md`, `DIALOGUE.md`, `ADVANCEMENT.md`, `REWARDS.md`, `PERSISTENCE.md`, `ENGINE_UPDATES.md`;
- `DEV/CATALOG/product-promise-evidence.json` as exact evidence/qualifier routing, not product authority.

### Machine realization / proof

- current package manifest and its five declared content members;
- `GAME/TOOLS/ruleset_package.py` and S6D-11 orchestration;
- current S6D catalogs and strict schemas;
- `domain-rules-coverage.json`, `house-rules-mechanical-boundary.json`, `ruleset-package-closure.json`;
- READY_PC identity fixture;
- focused S6D-07/08/09/10/11 validators/tests;
- current Resolution/Continuation schemas and execution evidence schemas.

## 3. Current machine observations

### M-01 — exact package declaration remains bounded

The current manifest declares exactly one built-in package, no dependencies, fixed package/version/catalog line and five explicit self-including semantic members. No wildcard/discovery semantics or manifest-embedded digest authority is present.

Disposition: `SATISFIED_CURRENT`.

### M-02 — current product evidence remains finite

`product-promise-evidence.json` contains atomic supported/out-of-scope rows with exact owner paths, evidence patterns, qualifiers and route IDs. Broad product prose is therefore narrowed by explicit machine evidence rather than treated as an implicit full-rules promise.

Current explicit negative space includes contest-specific resolution, generic reaction, broad damage-defense, generic concentration, generic visibility/cover, generic hazard time/resource machinery and currency economy.

Disposition: `SATISFIED_CURRENT`.

### M-03 — current identity evidence is stale

The checked-in semantic coverage artifact currently remains schema v2 and embeds a package binding carrying the previously checked-in set digest. The House-Rules mechanical-boundary evidence, READY_PC fixture and package-closure evidence carry the same stale set projection, and focused S6D-08/S6D-11 golden assertions pin it directly.

This is the already-established current machine-realization defect. The architecture owner decision B′ records its disposition and its execution-capability prerequisite. Step 2 does not repeat hash-root-cause diagnosis.

Disposition: `KNOWN_REALIZATION_BLOCKER` / `MACHINE_REALIZATION`.

### M-04 — stale package-closure positive-proof text is evidence, not authority

`ruleset-package-closure.json` labels its displayed package/set digests `DERIVED_NONAUTHORITATIVE_VERIFICATION_EVIDENCE`, which is architecturally correct. Some row wording currently claims validators/fixtures agree with reconstructed identity although current checked-in evidence is known stale. That wording is therefore stale realization evidence, not an alternative identity law.

Disposition: same closure item as M-03; do not create a second architecture issue.

### M-05 — Resolution/Continuation own exact identity fields, not example hashes

Current Resolution and Continuation schemas require both `ruleset_set_sha256` and `catalog_context_fingerprint` and retain accepted invocation facts/fixed RNG evidence across execution/suspension. Their example objects contain illustrative hash literals, but those examples are not selected current package projections and are not classified as current identity carriers.

Disposition: structural law `SATISFIED_CURRENT`; example literals `NONAUTHORITATIVE_EXAMPLE`.

## 4. Integrated obligation table

| ID | Source owner / law | Current consumer/proof | Qualifier / negative space | Disposition | Closure status |
|---|---|---|---|---|---|
| O-01 | S6D-01: manifest + exact bytes -> package snapshot -> resolved lock -> set identity | shipped package builder/loader, S6D-11 validator | no fuzzy discovery/substitution | `SATISFIED_CURRENT` semantically | machine projection repair remains O-20 |
| O-02 | S6D-01/Catalog Resolution: context is composition of natural owners | Resolution/Continuation identity fields | no global catalog snapshot owner | `SATISFIED_CURRENT` | closed |
| O-03 | S6D-02: admission ledger/core catalog bidirectional accounting | catalog admission machine contract | registration != execution | `SATISFIED_CURRENT` | closed |
| O-04 | S6D-03: only exact selectable selector/operation pairs execute | mechanical-surface contracts | dormant names remain nonselectable | `SATISFIED_CURRENT` | closed |
| O-05 | S6D-04: accessors/facts/derived/query surfaces distinct; bound DAG fail-closed | MechanicalContext + exact consumer permissions | no fixed-point/cycle fallback | `SATISFIED_CURRENT` | closed |
| O-06 | S6D-05: portable values are embedded nonowners | Activity parameter/fact/result schemas | no generic expression/query/path/patch language | `SATISFIED_CURRENT` | closed |
| O-07 | S6D-06: current executable primitive set finite; only `op.roll` owns RNG | primitive contracts + exact seed consumers | quarantined rows stay nonselectable | `SATISFIED_CURRENT` | closed |
| O-08 | S6D-07: READY_PC is deterministic frontier over natural owners + accepted context | readiness validator/fixture | provisional play remains local-sufficiency based | `SATISFIED_CURRENT` semantically | identity fixture included in O-20 |
| O-09 | S6D-08: HP/LifeState/Effect/Condition/Resource/Procedure owners remain separate | bounded health/effect seed and tests | no scheduler/global queue/campaign scan | `SATISFIED_CURRENT` | closed |
| O-10 | S6D-08: fixed RNG/causal evidence survives retry/recovery | health transitions + Step-3/5 owners | no reroll/reapply after accepted work | `SATISFIED_CURRENT` | closed |
| O-11 | S6D-09: required coverage is exact union of three finite source sets | deterministic coverage producer/validator | unsupported rows explicitly negative space | `SATISFIED_CURRENT` semantically | B′ physical migration O-20 open |
| O-12 | S6D-09: exact product promises route to exact supported mechanics | product-promise evidence + runtime owners | utterances are not coverage keys | `SATISFIED_CURRENT` | closed |
| O-13 | S6D-10: 2 adjudicated parameter + 7 reachability consumers | House-Rules machine boundary | no current reusable built-in policy realization | `SATISFIED_CURRENT` semantically | identity projection included in O-20 |
| O-14 | House Rules: policy/ruling prose never owns deterministic execution/RNG/state | typed parameter/fact bindings, Resolution freeze | one-off basis may be empty; durable policy basis exact when used | `SATISFIED_CURRENT` | closed |
| O-15 | S6D-11: registered S6D-07…10 validators are activation prerequisites | package-closure orchestration | validator pass cannot be inferred from labels | `SATISFIED_CURRENT` as law | current integrated PASS blocked by O-20 |
| O-16 | S6D-11: changed set silent use requires complete compatible/additive proof | comparator + engine-contract inventory | ancestry/label/load success insufficient | `SATISFIED_CURRENT` | closed |
| O-17 | Step-3: Resolution/Continuation retain accepted context/RNG/adjudicated evidence | strict runtime schemas | trace/receipt are evidence, not state/package owners | `SATISFIED_CURRENT` | closed |
| O-18 | Step-5.11/5.13: live typed consumers protect required evidence; cleanup fail-safe | retention/cleanup owner routing | no universal refcount/global GC/all-live scan | `SATISFIED_CURRENT` | closed; implementation acceptance later |
| O-19 | Source/access/adoption: package/source availability cannot persist campaign adoption without authority | Sources/Play Policy/Access Control/Engine Updates | runtime use != creator persistence authority | `SATISFIED_CURRENT` | closed |
| O-20 | all current derived package/set identity projections must equal canonical reconstruction | coverage, closure, House-Rules, READY_PC, S6D-08/S6D-11 golden evidence | one coherent repair; no partial five-of-six publication | `KNOWN_REALIZATION_BLOCKER` | **OPEN; required before final closure** |
| O-21 | B′: semantic coverage remains one exact producer-equal artifact; volatile package binding moves to small derived companion | approved post-canonical owner decision | no semantic digest, no sharding, no second identity owner | `KNOWN_REALIZATION_BLOCKER` | **architecture settled; migration blocked by execution capability** |
| O-22 | S6D-08 final machine-owner paragraph must not retain aggregate identity authority after S6D-11 | current prose vs later S6D-11 owner | later canonical identity supersedes it | `STALE_SUPERSEDED_ASSERTION` | narrow prose reconciliation due before final canonical status |
| O-23 | schema examples must not be mistaken for selected current projections | Resolution/Continuation examples | examples validate shape only | `SATISFIED_CURRENT` | no repair required for closure unless separately editorially desired |
| O-24 | production behavioral playability/performance execution remains implementation acceptance | S6D owners + roadmap baseline | architecture/machine contracts do not claim full runtime implementation | `IMPLEMENTATION_ACCEPTANCE_DEFERRED` | safe defer |
| O-25 | incompatible released-campaign migration remains R2.7 WP-20 | S6D-01/roadmap | no existing user campaigns requiring compatibility | `FUTURE_NOT_DUE` | do not activate now |

## 5. Attack matrix

### A-01 Duplicate semantic owners

No duplicate current owner found. Package identity, catalog composition, deterministic execution, campaign policy, state mutation and cleanup remain with distinct natural owners.

Disposition: `SATISFIED_CURRENT`.

### A-02 Narrative/LLM deterministic authority

Current adjudication/House-Rules boundaries require typed accepted inputs and keep RNG/mutation with deterministic owners. No current evidence grants prose execution authority.

Disposition: `SATISFIED_CURRENT`.

### A-03 Generic executable/query/path/payload escape hatch

S6D-05/06/09 retain closed typed value/primitive/routes; no generic expression/patch/query DSL is admitted.

Disposition: `SATISFIED_CURRENT`.

### A-04 Active registered ID without complete machine contract

Current S6D-03/04/06 laws distinguish registered from active/selectable. No current evidence requires promotion of quarantined rows.

Disposition: `SATISFIED_CURRENT`.

### A-05 Package/selectable content without admission/consumer proof

S6D-02 admission plus S6D-06/09 exact-consumer closure supplies the current finite route. No new orphan consumer identified.

Disposition: `SATISFIED_CURRENT`.

### A-06 Active consumer requires unsupported state/primitive

Current supported product rows lower either to exact S6D-07/08 routes, generic check/save, Procedure/movement, bounded spatial applicability or significant-Asset routes. Explicit negative-space rows prevent implied unsupported engines.

Disposition: `SATISFIED_CURRENT`.

### A-07 Cycle/fixed-point/evaluation-order fallback

MechanicalContext requires finite bound DAG/cycle rejection; no fixed-point fallback appears in current S6D scope.

Disposition: `SATISFIED_CURRENT`.

### A-08 Scheduler/global queue/global scan

S6D-08 and Step-5 cleanup explicitly reject background scheduler/global event queue/campaign-wide scan; due/index structures remain disposable routing evidence.

Disposition: `SATISFIED_CURRENT`.

### A-09 Retry/idempotency/RNG respin

Step-3 plus S6D-07/08/09/10 preserve fixed accepted inputs/RNG and idempotent result reuse. `op.roll` remains sole RNG owner.

Disposition: `SATISFIED_CURRENT`.

### A-10 Accepted work unreconstructable through exact ruleset/catalog context

Resolution/Continuation schemas require set identity + context fingerprint. S6D-01/11 require exact reconstruction and fail closed on absence. The law is complete; current stale derived development projections do not change accepted-work ownership semantics.

Disposition: `SATISFIED_CURRENT` semantic law; O-20 machine blocker remains.

### A-11 Cleanup destroys required package/causal evidence

S6D-01 retention joins owner-specific protection routing; Step-5.13 requires fail-safe retain and enrollment before new consumers depend on retireable artifacts. No universal cleanup owner can override a live dependency.

Disposition: `SATISFIED_CURRENT`; production exercise remains implementation acceptance.

### A-12 Changed-set compatibility bypass

S6D-11 comparator requires independently valid sets, complete engine inventory and durable dependency frontier. Candidate-only addition is allowed only after independent validation/collision checks.

Disposition: `SATISFIED_CURRENT`.

### A-13 House-Rules/adjudication bypass

Exact current surface remains nine adjudicated consumer edges and zero current built-in reusable policy realization. Historical durable policy refs are frozen only when policy materially contributed.

Disposition: `SATISFIED_CURRENT`.

### A-14 Product promise broader than machine route

Atomic product evidence records exact qualifiers and explicit out-of-scope rows. No present promise forces broad reaction, economy, geometry, concentration or full corpus support.

Disposition: `SATISFIED_CURRENT`.

### A-15 Current identity projections disagree canonical lock

Known current defect, already accepted into B′/post-canonical realization checkpoint.

Disposition: `KNOWN_REALIZATION_BLOCKER`; exact closure condition O-20/O-21.

### A-16 Stale/superseded prose/tests appear current

Two classes exist:

1. old hard-coded current identity expectations in current verification carriers — part of O-20 machine repair;
2. S6D-08 aggregate-content-set prose — O-22 stale superseded assertion.

Neither creates a parallel identity owner because later S6D-11 owners are explicit and controlling.

Disposition: `STALE_SUPERSEDED_EVIDENCE` plus O-20 machine repair.

### A-17 Pre-release migration baggage treated as compatibility requirement

Roadmap explicitly states no existing user campaigns requiring compatibility and current v2-generation structures are not a compatibility freeze. No current evidence activates released-campaign migration work.

Disposition: `FUTURE_NOT_DUE`.

### A-18 Hot-path GitHub/network/global work

Ruleset package loading is bounded to declared local package inputs; ordinary runtime uses bound context. No current architecture requires repository/network/extra-LLM round trips or global scans in ordinary gameplay.

Disposition: `SATISFIED_CURRENT`.

## 6. Current blocker classification

```text
SEMANTIC_ARCHITECTURE:       0
MACHINE_REALIZATION:         1 coherent blocker family (O-20/O-21)
STALE_SUPERSEDED_EVIDENCE:   1 narrow prose item (O-22) + identity assertions folded into O-20
IMPLEMENTATION_ACCEPTANCE:   deferred production behavioral proof
FUTURE_NOT_DUE:              released incompatible-campaign migration / dormant triggers
OUT_OF_SCOPE:                explicit S6D-09 negative space
```

No evidence in Step 2 requires a new product, authority or risk trade-off from the human architect.

## 7. Synthesis completeness gate

All eighteen required attack categories have an explicit disposition. The integrated obligation table accounts separately for current satisfied laws, stale superseded evidence, the known realization blocker, implementation acceptance, future-not-due work and explicit negative space.

The known B′ execution-capability limitation is preserved only as a prerequisite to machine materialization; it is not re-diagnosed and it is not converted into architecture work.

No dormant/future trigger has been promoted into current scope merely because S6D-12 is a final review.

## 8. Step-2 disposition

```text
S6D-12 STEP 2: COMPLETE
NEW SEMANTIC ARCHITECTURE CONTRADICTION: NONE FOUND
MATERIAL HUMAN PRODUCT/AUTHORITY DECISION EXPOSED: NO
KNOWN MACHINE-REALIZATION BLOCKER: PRESERVED
STALE SUPERSEDED S6D-08 IDENTITY PROSE: CONFIRMED NONAUTHORITATIVE
R2.7: REMAINS PAUSED
NEXT: S6D-12 STEP 3 — DECISION BRIEF
```
