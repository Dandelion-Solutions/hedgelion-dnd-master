# S6D-01 — Ruleset / Package / Catalog Snapshot Identity — Architecture Task Brief

Status: **STEP 1 COMPLETE CANDIDATE / STEP 2 NOT STARTED**

Date: 2026-08-25

Program authority:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

This artifact is only Step 1 of the dedicated eight-step S6D-01 design loop. It defines and challenges the assignment. It does not select an architecture, create a package manifest, change a schema, begin research synthesis, or authorize S6D-02.

## 1. S6D decomposition coherence check

The current twelve-domain decomposition naturally covers all eleven residual obligations admitted by the S6D owner decision. Nothing is dropped, and no thirteenth domain is required:

1. **S6D-01 — Ruleset/package/catalog snapshot identity** closes exact engine/ruleset/package/catalog identity, compatibility metadata, package seed packaging, dependency basis, and deterministic `ResolvedCatalogContext` reconstruction.
2. **S6D-02 — Catalog admission and gap closure** closes the admitted machine vocabulary and the catalog-gap side of supported D&D seed coverage.
3. **S6D-03 — Complete Calculation Selector metadata** closes the selector-metadata obligation.
4. **S6D-04 — Mechanical accessors, invocation facts and dependency graph** closes accessor/input/dependency metadata and owns any scheduled-trigger or invocation-adjudicated fact-shape extension that evidence proves necessary.
5. **S6D-05 — Activity parameters, targeting, costs and portable protocol values** closes exact typed mechanical protocol values and the protocol-value portion of any proven invocation-shape extension.
6. **S6D-06 — Registered Activity primitive contracts** closes exact supported primitive argument/result and execution contracts.
7. **S6D-07 — Character progression and initial READY_PC seed closure** closes stable advancement and choice-slot realization sufficient for reconstructable Actor builds and `READY_PC`.
8. **S6D-08 — Resource / HP / LifeState / Effect / Condition / temporal seed closure** closes concrete state/recovery seed verification and the owner-local scheduled/temporal responder portion of proven shape extensions.
9. **S6D-09 — Domain rules coverage** closes the supported-MVP D&D mechanics-surface coverage half of the seed/catalog-gap obligation and demonstrates execution routes rather than vocabulary alone.
10. **S6D-10 — Campaign rulings / House Rules boundary** consumes the now-canonical House Rules architecture so seed mechanics preserve the accepted typed-adjudication/deterministic-execution boundary; this is a required whole-project integration dependency rather than a missing historical residual item.
11. **S6D-11 — Tests and machine-contract closure** supplies machine verification, including package/context reconstruction, for the preceding residual obligations.
12. **S6D-12 — Adversarial final closure** performs the final catalog/schema/seed gap audit and integrated architecture attack before R2.7 resumes.

The eleven residual obligations remain the completion ledger; the twelve domains are the execution decomposition. Later integrated closure must still item-level-disposition the original eleven obligations rather than infer coverage merely from completing twelve loops.

## 2. Problem statement

HDM already requires every loader, binder, MechanicalContext builder, Resolution, Continuation and compatible recovery path to operate against one logical `ResolvedCatalogContext`. Plain durable `definition_id` values are meaningful only inside that context. Current artifacts expose several distinct identities—semantic engine version, generated runtime-package provenance, human rules baseline, catalog generation, campaign engine provenance and Git/source provenance—but do not yet establish the exact package-level identity and dependency contract sufficient to reconstruct or reject one compatible reusable-definition context.

S6D-01 must frame the architecture question that closes this gap without collapsing distinct version axes, making Git ancestry or mutable tags semantic authority, repeating package versions on every record, treating a checkpoint as a global snapshot owner, or deciding later S6D catalog/seed contents prematurely.

## 3. Scope

S6D-01 investigates and will later decide the minimum machine-validatable identity contract needed to:

- identify the engine capability contract participating in interpretation;
- identify the selected ruleset definition package or package set;
- distinguish presentation/version labels, catalog generation, immutable content identity and compatibility identity where their semantics differ;
- express package namespace ownership and selected package dependency/basis closure;
- bind a `ResolvedCatalogContext` to the exact compatible interpretation needed by loaders, accepted execution, suspension/resume, campaign adoption and recovery;
- define validation and explicit failure categories for missing, ambiguous, incompatible or unreconstructable context identity;
- locate the natural owners and projections of that identity across built runtime package, campaign state, accepted operational work and optional recovery evidence;
- establish what S6D-11 must verify for deterministic reconstruction and incompatibility rejection;
- hand explicit downstream contracts to S6D-02 through S6D-12 and to paused R2.7 without performing those domains.

The investigation may conclude that one manifest, several owner-local records/projections, derived lock material, or deletion/derivation of existing fields is preferable. The terms “package”, “snapshot”, “generation”, “lock” and “manifest” are hypotheses to test, not preselected record types.

## 4. Goals

1. Produce a decision-ready model of the identity axes and their distinct semantics.
2. Define the minimum immutable or content-addressed evidence sufficient to reconstruct the selected definition context or fail safely.
3. Preserve one-definition-per-ID, namespace ownership and no-shadowing laws inside a resolved context.
4. Preserve accepted execution and recovery under compatible pinned interpretation without inventing a universal cross-domain snapshot/frontier.
5. Align runtime-package provenance, engine update/adoption, campaign provenance, catalog generation and future package compatibility without duplicate semantic owners.
6. Keep ordinary runtime resolution bounded and local after the context is loaded; no hot-path remote lookup, repository-wide scan or mutable-tag lookup.
7. Define clean-slate pre-release behavior separately from future released-campaign evolution hooks.
8. Give later S6D domains and R2.7 explicit integration and verification obligations.

## 5. Non-goals

- Do not enumerate or fill the supported D&D seed; S6D-02 and S6D-07 through S6D-09 own that work.
- Do not complete selector, accessor, Activity value or primitive contracts; S6D-03 through S6D-06 own them.
- Do not design House Rules semantics; S6D-01 consumes `CAMPAIGN_HOUSE_RULES.md` only where package/profile/realization identity intersects it.
- Do not create arbitrary executable rule packages, plugin loading, a package manager, a network registry, online dependency resolution or a global namespace service.
- Do not implement broad runtime orchestration, migration tooling or release automation.
- Do not preserve obsolete pre-release `1.6.0` catalog/schema shapes or manufacture a migration for nonexistent user campaigns.
- Do not settle the general future post-release campaign migration policy owned by R2.7 WP-20; define only the compatibility/identity boundary and hooks S6D-01 must supply.
- Do not add version fields to every definition, world record, Resolution or checkpoint merely for convenience.
- Do not make checkpoint, campaign HEAD, Git commit order, mutable tag, source ancestry, LLM memory or ambient filesystem layout the semantic catalog owner.
- Do not begin Step 2 research synthesis or any later S6D domain from this artifact.

## 6. Existing constraints and architecture invariants

The investigation must preserve unless current owning evidence proves an explicit approved amendment is required:

1. One logical `ResolvedCatalogContext` governs a loader/binder/Resolution.
2. Within it, one `definition_id` resolves to at most one reusable definition; loaded layers are assembly/dependency/discovery order, not override precedence.
3. Namespace ownership belongs at package/context level; definition/world records do not repeat package identity without an independently proven owner need.
4. `rules_baseline` text and `catalog_version`/generation alone are insufficient identity for an independently versioned reusable-definition snapshot.
5. Engine version, catalog generation, source provenance, artifact identity and semantic compatibility are distinct axes unless evidence proves equivalence.
6. Source ancestry and exact source SHA are provenance/currentness evidence, not proof of semantic catalog compatibility.
7. Mutable tags, model memory, search order and ambient files are never catalog authority.
8. Accepted Resolution/Continuation work pins compatible interpretation/dependency evidence; newer ambient mechanics cannot silently reinterpret it.
9. Recovery composes compatible owner-native sources. Checkpoint is optional immutable evidence, not a universal snapshot/current-state authority, and campaign HEAD alone need not identify every operational dependency.
10. No universal frontier, global scheduler, global snapshot owner or generic cross-domain compatibility scalar may be introduced.
11. Runtime artifacts are validated local packages. `ENGINE_VERSION.yaml` owns the semantic runtime projection; generated `RUNTIME_PACKAGE.yaml` owns exact built-artifact provenance; the runtime package, development source tree and campaign storage are different authority surfaces.
12. Exact artifact bytes are identified by artifact digest; a package must not falsely claim source provenance.
13. Ordinary gameplay must not require Git history, network package resolution, repository-wide scans or cross-cache file mixing.
14. Campaign engine provenance and current runtime requirements remain portable campaign contracts; they must not become a second reusable-definition catalog owner.
15. House Rules prose/sidecar may link to typed realizations but does not become executable engine state or silently fork package identity.
16. Cleanup/protection interpretation that affects surviving dependencies participates in runtime/catalog compatibility, but S6D-01 must not absorb cleanup ownership from Step 5.13.
17. There are no existing user campaigns requiring compatibility with the discarded current scaffold. Future published compatibility must remain possible without pre-release baggage.
18. Public HDM artifacts must use independently written HDM terminology and legally conservative content.

## 7. Known neighboring components and whole-project dependencies

### Upstream authorities

- S6D owner decision, workstream brief and sequencing decision establish admitted residual scope and the dedicated eight-step loop.
- `CATALOG_RESOLUTION.md`, `CATALOG_CONTRACTS.md` and Step-1 catalog-evolution assurance own resolved-context, stable-ID, namespace and no-shadowing semantics.
- engine-version split, runtime-package provenance, branch/release/versioning and runtime bootstrap/update owners distinguish semantic runtime identity, artifact provenance and campaign adoption.
- Step 3 and retrospective assurance require accepted execution/Continuation to retain compatible context identity.
- Steps 5.2 and 5.7 own compatible recovery composition and checkpoint nonauthority.
- Step 5.13 owns cleanup-contract compatibility and retention of still-promised interpretation dependencies.
- the canonical House Rules owner constrains any ruleset profile/fork or typed-realization integration.

### Direct machine surfaces

- `DEV/ENGINE_DEVELOPMENT.yaml` and `GAME/ENGINE_VERSION.yaml`;
- generated runtime `RUNTIME_PACKAGE.yaml` contract and `DEV/TOOLS/release_builder.py`;
- `DEV/CATALOG/core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, `mechanical-surfaces.json`;
- `DEV/SCHEMAS/core-catalog.schema.json`, `catalog-definition.schema.json`, and any campaign/runtime schema that currently stores engine, package, catalog or accepted-execution provenance;
- campaign `MANIFEST.yaml`/schema and initialization/update paths;
- release builder, release checklist and versioning/update tests.

### Downstream consumers that must be checked

- runtime bootstrap/package binding and multi-runtime cache isolation;
- catalog loaders, binders and validation paths;
- MechanicalContext, Resolution, Continuation and suspended/reaction work;
- campaign initialization, runtime adoption and creator/non-creator update rules;
- cold recovery, live/operational source routing and optional checkpoint diagnostics;
- definition promotion/dependency publication and namespace collision checks;
- House Rules typed realization/currentness linkage;
- cleanup/protection routing when accepted dependencies outlive a representation;
- release composition, exact artifact provenance and maintenance audit;
- S6D-02 admission, S6D-03–06 contract registries, S6D-07–10 seed/profile consumption, S6D-11 reconstruction tests, S6D-12 adversarial closure;
- paused R2.7 WP-06 and future WP-20 compatibility/evolution work.

## 8. Quality attributes and failure model

Decision-distinguishing qualities:

- **deterministic reconstructability:** identical accepted identity evidence selects one compatible definition context or fails explicitly;
- **semantic integrity:** no same-ID shadowing, mixed-package interpretation or silent reinterpretation;
- **authority clarity:** each identity field has one natural owner and explicit projections;
- **recovery safety:** accepted operational work remains resumable only with its required compatible interpretation evidence;
- **portability:** campaigns can name required compatible runtime/rules interpretation without depending on one machine’s cache layout;
- **bounded latency:** startup/adoption may validate a bounded dependency set; ordinary execution uses the already-bound context;
- **auditability:** package content, dependency basis and compatibility decisions are explainable without chain-of-thought or mutable external state;
- **evolvability:** future package/profile evolution and R2.7 WP-20 can extend the contract without redefining current IDs;
- **YAGNI/operational simplicity:** no package ecosystem, online solver or universal snapshot object without a proved consumer;
- **legal conservatism:** no copied third-party package metadata design or protected rules content.

Failure cases the later design must classify include missing package/dependency, digest mismatch, duplicate or unauthorized namespace, unsupported dependency relation, engine-capability mismatch, catalog-generation mismatch, incompatible cleanup/protection vocabulary, unresolved campaign/session dependency, ambiguous same-ID definition, stale/mutable provenance, suspended work whose required context cannot be resolved, and a package that claims inconsistent semantic/artifact/source identities.

## 9. Unknowns Step 2 must investigate

1. What are the irreducible identity axes, and which current fields are owner, projection, compatibility selector, provenance, display metadata or obsolete duplication?
2. Is the shipped baseline one ruleset package, a package set, an engine-adopted embedded package, or another independently simpler representation?
3. What exactly must be content-addressed: each package, resolved dependency set, catalog aggregate, release artifact, or a minimal combination?
4. Is compatibility equality, declared line/range, capability fingerprint, schema/catalog generation relation, or another typed relation—and which owner evaluates it?
5. How are namespace claims and dependency closure represented and validated without introducing online resolution or hidden precedence?
6. Which identity belongs in runtime package metadata, campaign manifest/adoption state, accepted execution/Continuation evidence and optional checkpoint diagnostics?
7. Can accepted execution pin a compact resolved-context identity while its reconstructable dependency evidence remains in natural package/campaign/session owners?
8. How do campaign and session definitions participate in a context without pretending they are immutable release packages or permitting silent same-ID override?
9. Does canonical House Rules typed realization require a derived/profile package identity, or can existing campaign-definition/currentness owners satisfy it?
10. Which clean-slate fields or schemas should be deleted/rederived rather than preserved?
11. What is the minimum future-compatibility hook S6D-01 must provide while leaving released-campaign migration sequencing to WP-20?
12. Which consumers need exact content identity versus compatibility identity, and what is the safe failure behavior when only one is available?
13. What bounded startup/adoption/recovery algorithm can prove the required context without a global snapshot or hot-path scan?
14. What exact invariants and negative cases must S6D-11 make executable?

## 10. Initial Source Manifest and discovery route

The Source Manifest is intentionally task-specific. Step 2 must refine it when concrete symbol/path searches expose additional owners or consumers.

| Source set | Authority role | Required inspection and reason | Important dependencies / status |
|---|---|---|---|
| `AGENTS.md`; both design-process owners | CANONICAL PROCESS | repository, evidence, Source Manifest, eight-step and transport rules | Inspected current; mandatory governance |
| `PROJECT_MAP.md`; `CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE LOCATORS | build whole-project ownership/dependency route | Inspected current; never semantic authority |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | STATUS AUTHORITIES | active stage, immutable R2.7 pause boundary, clean-slate identity facts | Inspected current |
| S6D owner decision, workstream brief, eight-step sequencing decision | OWNER DECISIONS / DECOMPOSITION INPUT | residual items, non-goals, exit criteria, dedicated domain loop | Inspected item-level for Step 1 |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-WP-03-catalog-class-capability-completeness-mini-report.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-WP-06-rules-adjudication-domain-compatibility-mini-report.md`; `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-source-manifest.md` | RESEARCH / CURRENT AUDIT EVIDENCE | current catalog generation, gaps, neighboring domain findings and qualifiers | Inspected relevant identity/dependency findings; not architecture authority |
| `CATALOG_RESOLUTION.md`, `CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md` | CANONICAL OWNERS | resolved context, stable IDs, namespace/package responsibility, class boundaries | Inspected relevant sections; read fully in Step 2 |
| `DEV/docs/superpowers/design/2026-08-19-step-1-assurance-slice-0a-catalog-meta-model-resolution.md`; `DEV/docs/superpowers/design/2026-08-19-step-1-assurance-slice-0b-catalog-evolution-resolution.md`; `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md` | CANONICAL ASSURANCE / DERIVATION | exact deferred package identity and pinned-context obligations | Inspected relevant enumerated findings; Step 2 reconciles full applicable chain |
| `DEV/ENGINE_DEVELOPMENT.yaml`; `GAME/ENGINE_VERSION.yaml` | MACHINE METADATA OWNERS / PROJECTION | present engine/rules/schema axes and shared-field equality | Inspected current |
| `DEV/docs/superpowers/specs/2026-08-18-engine-version-split-amendment.md`; `DEV/docs/superpowers/specs/2026-08-18-runtime-package-provenance-amendment.md`; `DEV/docs/superpowers/specs/2026-08-18-release-migration-safety-addendum.md` | CANONICAL AMENDMENTS | semantic identity vs built-artifact provenance and migration safety | Inspected relevant portions; Step 2 reads complete applicable sections |
| `BRANCH_MODEL.md`; `DEV/RELEASE/VERSIONING.md`; `GAME/CORE/BOOTSTRAP_RUNTIME.md`; `GAME/CORE/ENGINE_UPDATES.md` | CANONICAL / SHIPPED OWNERS | runtime asset, campaign provenance, adoption, cache and source/tag boundaries | Inspected relevant identity/update sections; Step 2 follows referenced schemas/tools |
| `DEV/TOOLS/release_builder.py`; `DEV/RELEASE/CHECKLIST.md` | MACHINE CONTRACT / VERIFICATION | generated package provenance, exact artifact digest, composition and validation | Inspected relevant portions; Step 2 traces generated fields and consumers |
| `DEV/CATALOG/*.json`; implicated `DEV/SCHEMAS/*` | CURRENT MACHINE CONTRACTS | current generation, registries, ID/namespace constraints and missing package structure | Core/identifier and core schemas inspected; Step 2 completes family inspection |
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`; `DEV/SCHEMAS/resolution-receipt.schema.json`; `DEV/SCHEMAS/runtime-resolution-state.schema.json`; `DEV/SCHEMAS/runtime-resolution-trace-state.schema.json` | CANONICAL + MACHINE CONSUMERS | pinned context identity and accepted work/retry/suspension semantics | Required in Step 2 |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`; `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`; `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | CANONICAL NEIGHBOR OWNERS | compatible recovery, checkpoint nonauthority, cleanup compatibility/protection | Relevant laws inspected; full applicable sections required in Step 2 |
| `GAME/CAMPAIGN/MANIFEST.yaml`; `GAME/SCHEMA/campaign_manifest.schema.yaml`; `GAME/TOOLS/init_campaign.py`; `GAME/CORE/ENGINE_UPDATES.md`; implicated `DEV/TESTS/test_engine_*`, `test_runtime_package_provenance.py`, `test_multi_runtime_release_consistency.py` | SHIPPED OWNER + MACHINE EVIDENCE | portable campaign provenance/current runtime requirement, initialization and adoption writes | Required in Step 2 via exact symbol/path search; test pattern is a homogeneous family plus named identity tests |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`; `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`; `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml`; `GAME/SCHEMA/house_rules_policy.schema.yaml`; implicated House Rules/adjudicated-input tests | CANONICAL + MACHINE CONSUMER | determine whether rules profiles/typed realizations create an identity consumer | Required in Step 2; do not reopen House Rules |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`; `DEV/docs/superpowers/specs/2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md`; `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | OWNER-APPROVED AUDIT DECOMPOSITION / STATUS | preserve the paused WP-06 handoff and the future WP-20 boundary | No separate WP-20 architecture owner exists yet; Step 2 must not invent migration requirements beyond the recorded boundary |
| catalog, runtime provenance, update, multi-runtime, R2.7 WP-03 and release tests | EXECUTABLE EVIDENCE | current enforced invariants and missing reconstruction coverage | Representative files inspected; Step 2 completes implicated tests |
| current repository symbol/path search for all identity fields and `ResolvedCatalogContext` consumers | DISCOVERY MECHANISM | find stale references, duplicate owners and unindexed consumers | Mandatory before synthesis; zero results are not absence evidence |

External research is not presumed necessary. Use primary standards/vendor sources only if repository evidence leaves a material representation or compatibility question unresolved; record why the external source changes the decision. Do not import distinctive third-party schemas or terminology into public HDM artifacts.

## 11. Questions the Step 2 result must answer

1. What exact semantic claim does each retained identity field make, and who owns it?
2. What minimum record/records reconstruct one `ResolvedCatalogContext`, including package dependency and namespace basis?
3. Which parts are immutable identity, compatibility policy, provenance, currentness/adoption state and derived fingerprints?
4. Where is each part stored or projected for runtime package binding, campaign portability, accepted execution and recovery?
5. What validation algorithm rejects incompatible, ambiguous, incomplete or dishonest identity combinations?
6. How are campaign/session definitions incorporated without shadowing or per-record version proliferation?
7. How does the design preserve Step-3/5 accepted-work and recovery laws without creating global snapshot authority?
8. What existing fields/records are retained, changed, derived or deleted under the clean-slate rule?
9. What contracts are handed to later S6D domains, S6D-11 tests, S6D-12 review and R2.7 WP-20?
10. Does any residual choice concern product semantics, authority, compatibility or material risk and therefore require a human decision?

## 12. Step 1 exit criteria

Step 1 is complete only when:

1. the twelve S6D domains have been checked as one natural decomposition against all eleven residual obligations with no dropped scope;
2. S6D-01 is bounded separately from S6D-02 and later seed/contract/implementation work;
3. the brief is solution-blind: evidence may select, split, merge, derive or reject proposed package/snapshot/manifest abstractions;
4. existing identity axes, accepted invariants, clean-slate rules and authority/non-equivalence boundaries are explicit;
5. the initial Source Manifest covers the relevant whole-project dependency subgraph, including owners, amendments, machine surfaces, runtime/recovery consumers and tests;
6. known unknowns and failure cases are decision-distinguishing rather than generic;
7. questions and exit criteria can drive a bounded Step 2 research result;
8. a separate brief critic has attacked framing, stale assumptions, whole-project dependencies, missing consumers, YAGNI and hidden solution bias;
9. all blocking/significant critic findings are resolved in this brief or explicitly shown not to apply;
10. the brief and critic record are published on the current authoritative development ref and publication is verified;
11. roadmap/status is not advanced beyond S6D-01 Step 1 unless the owning process explicitly requires a status edit;
12. work stops before S6D-01 Step 2 and before S6D-02.

## 13. Brief-framing challenge

The assignment is invalid if a competent investigation could satisfy it while doing any of the following:

- renaming current `catalog_version` as a snapshot ID without proving reconstruction;
- hashing one aggregate while ignoring campaign/session dependencies or namespace ownership;
- treating the runtime ZIP digest, engine version, source SHA or Git tag as interchangeable semantic identities;
- copying all identity fields into every durable record or checkpoint;
- introducing a generic package manager, global lock service or universal recovery snapshot without a proven consumer;
- optimizing release packaging while missing Continuation/recovery/House Rules/cleanup consumers;
- preserving pre-release baggage as compatibility work;
- solving S6D-02 catalog contents inside S6D-01;
- claiming whole-project coverage from indexes, search snippets or representative tests alone.

The Step 2 investigation must remain able to conclude that the smallest correct design is less package-like than the initial vocabulary suggests, or that multiple owner-local projections are required. No proposed record type is an accepted architecture result at Step 1.

