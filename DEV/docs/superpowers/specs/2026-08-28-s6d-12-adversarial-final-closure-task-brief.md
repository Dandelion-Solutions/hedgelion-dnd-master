# S6D-12 — Adversarial Final Closure — Architecture Task Brief

Status: **STEP 1 TASK BRIEF — WHOLE-PROJECT CRITIC REQUIRED**

Date: 2026-08-28

## 1. Purpose and stage boundary

S6D-12 is the final adversarial architecture/realization closure for the S6D workstream. It does not create another rules subsystem and does not reopen S6D-01…11 merely because their contracts meet at this gate.

Its question is:

> Given the current canonical S6D-01…11 owners, the exact current machine realization and the current runtime/product consumers, is there any remaining contradiction, duplicate authority, unsupported current promise, non-reconstructable identity, unowned active dependency, unsafe retention/retry behavior or falsely closed realization that prevents honest S6D integrated closure?

The target proof is:

```text
current S6D-01…11 canonical owners
+ current accepted post-canonical amendments
+ exact current machine contracts / schemas / validators / tests
+ current GAME runtime consumers
+ current persistence / recovery / update owners
    -> adversarial cross-owner reconciliation
    -> every current obligation classified item-by-item
    -> no undispositioned semantic or machine-closure blocker
    -> explicit final closure disposition
```

S6D-12 is not:

- a new product-scope pass;
- a full-SRD expansion;
- runtime implementation planning;
- a CI-cleanup project;
- a migration-policy project for released campaigns;
- a reason to activate dormant selectors/primitives/facts/content;
- a reason to redesign package identity;
- a reason to shard `domain-rules-coverage`;
- a repeat of S6D-11 package-builder implementation.

Production runtime implementation remains deferred to Implementation Planning except where an already-approved clean-slate architecture decision has an authorized machine-contract realization. The known B′ realization obligation below is deliberately not implemented inside Step 1.

## 2. Sequencing and authority baseline

Current sequencing authority is `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`:

```text
S6D-01…S6D-11: COMPLETE / CANONICAL
S6D-12: NEXT
R2.7 WP-06: PAUSED
R2.7 resume trigger: S6D integrated closure
```

S6D-12 inherits the S6D umbrella owner decision and decomposition, but current owning sources supersede dated plan assumptions where later stages amended them.

Closed architecture is preserved unless current evidence proves one of the accepted reopen conditions:

1. material extension;
2. real contradiction or invalid assumption;
3. new unsatisfied consumer;
4. accepted decision insufficient for a current requirement.

A stale assertion superseded by a later canonical owner is not itself a reason to reopen the earlier architecture. It is a reconciliation/repair item unless it exposes one of the four conditions above.

## 3. Settled S6D baseline

Treat the following as established unless fresh owning evidence proves a material contradiction.

### 3.1 S6D-01 — identity and reconstruction

`RulesetPackageManifest + exact declared semantic bytes -> RulesetPackageSnapshot.content_sha256 -> exact dependency-closed resolved lock -> ruleset_set_sha256` is the only canonical package/set identity chain. `ResolvedCatalogContext` remains a logical composition of natural owners; derived fingerprints and displayed digests are evidence, not new snapshot owners.

Recovery never substitutes model memory, ambient mutable files, fuzzy package matching or another set identity. A missing exact required set fails finitely.

### 3.2 S6D-02 — admission and realization accounting

The current core-catalog family/ID set and admission ledger are bidirectionally equal. Admission disposition and realization state are independent. Active, embedded, dormant and inherited items retain exact owner/evidence routing. Registration is never execution authority.

The built-in package admission profile is planning/admission evidence, not a runtime manifest or snapshot.

### 3.3 S6D-03 — selectable calculations

Exactly three selectors and two `rule.*` operations are currently executable through the S6D-03 calculation surface. Other registered selector/operation names remain dormant/nonselectable unless a later exact consumer and complete pair contract explicitly activate them.

### 3.4 S6D-04 — MechanicalContext

Accessors, invocation facts, derived nodes and runtime queries remain distinct surfaces. `fiction.target_reachable` is admitted only for the seven exact S6D-09 consumers; `fiction.target_visible` remains dormant. One bound dependency graph owns cycle/input-authority validation. Incomplete graph proof or a cycle fails closed; no fixed-point fallback exists.

### 3.5 S6D-05 — portable values

Portable Activity/execution values are embedded nonowners. Signal and StateDelta have no independent lifecycle/authority. There is no generic payload/query/expression/path/patch/event-bus language. Accepted adjudicated inputs retain exact provenance/currentness/policy-basis evidence as required by later S6D-09/10 amendments.

### 3.6 S6D-06 — Activity primitives

Exactly the current eleven S6D-07-activated primitive contracts are executable; the remaining registered primitive rows remain quarantined. Only `op.roll` owns RNG. Mutation candidates have no independent durable authority; enclosing execution/event/receipt owners prove commit and outcome.

### 3.7 S6D-07 — READY_PC and character seed

READY_PC is a deterministic initial mechanical commitment frontier over natural owners and the accepted catalog context. Provisional play remains legal only under local mechanical sufficiency. The current built-in character profile is deliberately bounded; unsupported content remains absent/nonselectable. READY_PC identity evidence uses canonical `ruleset_set_sha256`, not the retired aggregate identity.

### 3.8 S6D-08 — health/effects/recovery

Actor/Asset/procedure/Effect/Condition/chronology owners remain distinct. There is no background scheduler, global event queue or campaign-wide scan. Retry reuses fixed causal/RNG evidence and cannot duplicate already committed effects/transitions. Only the exact supported bounded package cases are current product support.

### 3.9 S6D-09 — domain coverage

The semantic completeness law remains:

```text
REQUIRED_COVERAGE_KEYS = union(PACKAGE_CLOSURE_KEYS,
                               ACTIVE_MACHINE_CONSUMER_KEYS,
                               PRODUCT_PROMISE_KEYS)
COVERAGE_LEDGER_KEYS == REQUIRED_COVERAGE_KEYS
```

Coverage is one semantic ledger; unsupported current surface is explicitly negative space. Generic contest/reaction/broad damage-defense/concentration/economy/crafting/teleportation/visibility-cover and broad corpora remain out of scope unless later exact current consumers prove otherwise.

### 3.10 S6D-10 — House-Rules boundary

Semantic rulings/policy are not execution authority. Durable policy materially used by an accepted adjudicated input is frozen by exact historical policy refs; one-off rulings may have an empty durable policy basis. The exact current package consumer surface remains two bounded adjudicated DC contracts plus seven reachability fact edges; current built-in reusable policy realization count remains zero.

### 3.11 S6D-11 — package machine closure

The built-in package is `ACTIVE_VERIFIED_MACHINE_CONTRACT` only through the exact manifest/snapshot/lock/set chain plus registered S6D-07…10 validators and path-neutral engine-contract conformance evidence. Changed-set same-version silent use requires the fail-closed compatible/additive comparator; ancestry, compatibility label or standalone load success is insufficient.

S6D-11 semantic architecture remains closed.

## 4. Explicit post-canonical carry-in — B′ realization obligation

Owner decision:

`DEV/docs/superpowers/specs/2026-08-28-domain-rules-coverage-derived-binding-owner-decision.md`

Disposition:

```text
architecture decision: B′ APPROVED
architecture semantics: settled
implementation/migration: BLOCKED_BY_EXECUTION_CAPABILITY
missing capability:
  execute deterministic repository producer on verified ref
  and return generated artifact bytes
required before:
  S6D final closure / R2.7 resume
```

B′ means:

- `DEV/CATALOG/domain-rules-coverage.json` remains one semantic coverage artifact;
- the whole volatile package binding moves to `DEV/CATALOG/domain-rules-coverage-binding.json`;
- that binding contains exactly `profile_id`, `package_id`, `package_version`, `catalog_generation`, `gameplay_spine_member`, `package_content_sha256`, `ruleset_set_sha256`;
- no `coverage_semantic_sha256` or substitute semantic-ledger digest is introduced;
- semantic coverage remains proved by exact equality with its fresh deterministic producer;
- binding evidence remains strictly derived from the canonical S6D-11 identity chain;
- no sharding and no second identity owner are admitted.

S6D-12 SHALL NOT re-diagnose the already-established materialization cause or redesign B′. The open item is a realization/closure obligation only.

It does not block Steps 1–6 research/design. It DOES block an unconditional S6D final PASS and R2.7 resume until coherently materialized and verified, unless a later explicit human owner decision gives a different disposition.

## 5. Mandatory Source Manifest

Step 2 and both critics must use the current remote ref and `DEV/PROJECT_MAP.md` to reconstruct the relevant direct-and-indirect dependency graph. The list below is the minimum floor; discovered current consumers/owners must be added.

### 5.1 Process / sequencing / carry-in

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- S6D umbrella owner decision/task brief/decomposition plan;
- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md` only as the durable pre-pause R2.7 cursor where current roadmap does not supersede its sequencing text;
- the B′ owner decision above.

### 5.2 Canonical S6D owners

- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`;
- `DEV/ARCHITECTURE/CATALOG_ADMISSION.md`;
- `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`;
- `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`;
- `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md`;
- `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md`;
- `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`;
- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md`;
- `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`;
- `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md`.

Follow every later canonical amendment that changes the current meaning; do not infer current authority from date/order alone.

### 5.3 Machine realization and proof

At minimum inspect:

- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/` exact current declared member set;
- `GAME/TOOLS/ruleset_package.py`;
- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/catalog-admission-ledger.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- `DEV/CATALOG/portable-value-contracts.json` and `portable-value-routes.json`;
- `DEV/CATALOG/activity-primitive-contracts.json`;
- `DEV/CATALOG/product-promise-evidence.json`;
- `DEV/CATALOG/domain-rules-coverage.json`;
- `DEV/CATALOG/house-rules-mechanical-boundary.json`;
- `DEV/CATALOG/ruleset-package-closure.json`;
- strict schemas referenced by those contracts;
- `DEV/TOOLS/validate_character_mvp_seed.py`;
- `DEV/TOOLS/validate_health_effects_recovery_seed.py`;
- `DEV/TOOLS/validate_domain_rules_coverage.py`;
- `DEV/TOOLS/validate_house_rules_mechanical_boundary.py`;
- `DEV/TOOLS/validate_ruleset_package_closure.py`;
- focused S6D-07/08/09/10/11 tests and identity projections;
- release-builder/current-runtime provenance validation only where it consumes the S6D package closure.

The current known checked-in identity-evidence mismatch and B′ obligation must be represented as OPEN REALIZATION evidence, not silently counted as a current PASS.

### 5.4 Runtime/product consumers

At minimum inspect the current owners implicated by product-promise evidence and package identity:

- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/MECHANICS_INTEGRITY.md`;
- `GAME/CORE/RANDOMNESS.md`;
- `GAME/CORE/CHARACTER_READINESS.md`;
- `GAME/CORE/ADJUDICATION.md`;
- `GAME/CORE/COMBAT.md`;
- `GAME/CORE/MAGIC.md`;
- `GAME/CORE/EXPLORATION.md`;
- `GAME/CORE/DIALOGUE.md`;
- `GAME/CORE/ADVANCEMENT.md`;
- `GAME/CORE/REWARDS.md`;
- package/source-routing owners where an exact mechanic can be unavailable or unsupported.

Product promises must be interpreted with the exact qualifier recorded in `product-promise-evidence.json`; broad prose wording does not silently enlarge the supported machine surface.

### 5.5 State / execution / retention / recovery / update

Follow current owner dependencies into:

- ActionRequest / Resolution / Continuation / ExecutionSegment / MechanicalEvent / receipt contracts;
- Actor / Asset / Effect / Resource / Procedure state owners;
- chronology and boundary-processing owners;
- `GAME/CORE/STORAGE.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md`, `INTEGRITY.md` where accepted mechanics survive durability/recovery;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` and `ENGINE_UPDATES.md` where exact runtime/ruleset identity is selected or refreshed;
- current campaign/checkpoint/execution schemas that project `ruleset_set_sha256` and catalog-context identity;
- access-control/adoption owners where changed identity may persist.

The final review must distinguish persistent authority from cache/index/trace/projection evidence and must reject any accidental second owner.

## 6. Required Step-2 evidence products

Step 2 shall produce a finite adversarial inventory, not a thematic essay.

### 6.1 Integrated obligation table

For every relevant current obligation record:

```text
obligation_id
source_owner
actual law / claim
current consumers
machine realization / proof
qualifiers / negative space
current disposition
cross-owner conflict, if any
closure status
repair owner, if any
```

Allowed dispositions include:

```text
SATISFIED_CURRENT
STALE_SUPERSEDED_ASSERTION
KNOWN_REALIZATION_BLOCKER
DORMANT_WITH_TRIGGER
OUT_OF_CURRENT_SCOPE
IMPLEMENTATION_ACCEPTANCE_DEFERRED
REAL_ARCHITECTURE_CONTRADICTION
```

Do not manufacture a current repair from a future revisit trigger.

### 6.2 Attack matrix

At minimum attack the integrated system for:

1. duplicate semantic owners;
2. narrative/LLM text acquiring deterministic authority;
3. arbitrary executable/query/path/payload escape hatches;
4. active registered IDs without complete machine contracts;
5. package/selectable content without current admission/consumer proof;
6. active consumers that require unmodeled state or unsupported primitives;
7. cycle/fixed-point/evaluation-order fallback assumptions;
8. background scheduler/global queue/global-scan assumptions;
9. retry/idempotency/RNG evidence that can be respun or reinterpreted;
10. accepted work whose exact ruleset/catalog context cannot be reconstructed;
11. retention/cleanup that can destroy still-required package or causal evidence;
12. changed-set compatibility that can bypass complete additive proof;
13. House-Rules/adjudication prose bypassing typed input/currentness/adoption authority;
14. product promises whose machine route is absent or broader than the exact current supported qualifier;
15. current identity projections that can disagree with the canonical lock;
16. stale/superseded prose or tests that falsely appear to remain current authority;
17. pre-release migration baggage being treated as current compatibility requirement without a current campaign consumer;
18. hot-path GitHub/network/global-work assumptions contrary to local/bounded runtime laws.

### 6.3 Exact closure blockers

Every blocker must be classified as one of:

```text
SEMANTIC_ARCHITECTURE
MACHINE_REALIZATION
STALE_SUPERSEDED_EVIDENCE
IMPLEMENTATION_ACCEPTANCE
FUTURE_NOT_DUE
OUT_OF_SCOPE
```

Only a material `SEMANTIC_ARCHITECTURE` issue or a new product/authority/risk choice requires a new human decision before Step 4. Mechanical consistency repairs implied by already accepted architecture remain agent work, but B′ implementation stays blocked by its separately recorded execution-capability prerequisite.

## 7. Known findings entering Step 2

These are carry-in evidence, not final conclusions.

### S6D12-CARRY-01 — B′ machine realization

Classification: `KNOWN_REALIZATION_BLOCKER` / `MACHINE_REALIZATION`.

The architecture is settled, but the coherent machine migration has not occurred. It prevents final S6D PASS/R2.7 resume; it does not reopen package identity or block Step-2 architecture research.

### S6D12-CARRY-02 — stale S6D-08 aggregate identity prose

`DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` still contains an older statement that the package capability record binds a two-file set with per-file hashes and an aggregate content-set digest.

Later S6D-11 canonical identity explicitly invalidates that aggregate authority. Current S6D-10 and S6D-11 owners likewise reject the former aggregate identity. Therefore the working classification entering Step 2 is `STALE_SUPERSEDED_ASSERTION`, not a reopened S6D-08 semantic decision.

Step 2/critic must confirm there is no current consumer that still makes the old wording authoritative. If confirmed, final reconciliation owns a narrow prose repair; no new identity algorithm or owner is introduced.

### S6D12-CARRY-03 — checked-in derived identity mismatch

The current checked-in package/set identity projections are known to differ from canonical reconstruction under the current S6D-11 algorithm. This is the concrete defect that motivated B′. It remains `MACHINE_REALIZATION` and must not be counted as proof of current integrated closure.

S6D-12 shall preserve exact current evidence and closure prerequisite but shall not redo the already-completed root-cause analysis.

## 8. Step sequence and deliverables

### Step 1 — Architecture Task Brief

This document plus a mandatory whole-project brief critic. Exit only when critic finds no missing current owner/consumer that would materially change the problem framing.

### Step 2 — Research / evidence extraction

Produce the Source Manifest, integrated obligation table, attack-matrix evidence, current-machine/projection census and explicit dispositions. Preserve qualifiers and negative findings.

### Step 3 — Decision Brief

Determine whether Step 2 exposes any genuine material architecture choice. If all remaining work follows mechanically from accepted owners, record `HUMAN_DECISION_REQUIRED: NO` and continue without manufacturing a choice. If a real product/authority/risk trade-off remains, return to the human architect with decision-ready alternatives.

### Step 4 — Collaborative review

Reconcile the selected/derived result against current owners, current machine consumers and the B′ carry-in. Do not implement machine changes.

### Step 5 — Candidate final-closure specification

Specify exact final S6D closure law, finite blockers/deferred acceptance and required evidence for R2.7 resume.

### Step 6 — Mandatory whole-project adversarial critic

Use `DEV/PROJECT_MAP.md` and the full task-specific dependency subgraph. A module-local critic is invalid. Classify findings BLOCKING / SIGNIFICANT / MINOR and resolve or explicitly disposition all of them.

### Step 7 — Resolution Gate

PASS only if the candidate is internally consistent, all semantic architecture blockers are resolved, machine-realization blockers have exact closure conditions and no false claim of current machine PASS is made.

A Step-7 architecture/design PASS does not by itself authorize R2.7 resume while B′ machine realization remains open.

### Step 8 — Canonicalization / final S6D disposition

Canonical final S6D closure may declare R2.7 resume only after every required current machine-realization blocker is actually closed and verified. If B′ remains blocked, Step 8 must record `S6D_FINAL_CLOSURE: BLOCKED_BY_KNOWN_REALIZATION_OBLIGATION` and keep R2.7 paused; it must not weaken the architecture to force a PASS.

## 9. Hard non-goals

Do not:

- implement B′ while execution capability remains unavailable;
- edit schemas/validators/generated coverage/digest carriers as a partial B′ migration;
- redesign CI or chase unrelated historical red tests;
- broaden package content or MVP/product promises;
- activate dormant/quarantined IDs;
- introduce a generic rules DSL/query engine;
- introduce package registry/network discovery;
- introduce global scheduler/queue/refcount/scan infrastructure;
- invent compatibility migration for nonexistent current campaigns;
- resume R2.7 before an honest S6D final closure gate authorizes it.

## 10. Step-1 exit criteria

Step 1 is complete when:

1. the current source/owner subgraph is identified through `PROJECT_MAP` plus actual owners;
2. the B′ realization obligation is an explicit final-closure carry-in without re-diagnosis;
3. S6D-01…11 settled semantics and negative space are preserved;
4. the attack matrix covers identity, authority, machine completeness, product promises, retry/RNG, retention/recovery, House Rules and performance boundaries;
5. known stale/superseded assertions are separated from real architecture contradictions;
6. the whole-project brief critic reports no blocking/significant omission in the task framing;
7. no S6D-12 implementation or R2.7 work has started.

Step 2 begins only after these conditions are satisfied.
