# S6D-02 — Catalog Admission and Gap Closure — Architecture Task Brief

Status: **STEP 1 COMPLETE — STEP 2 NOT STARTED**

Date: 2026-08-25

Authoritative preparation ref: `v1/engine-rearchitecture@eee4683b2b270a555105c19fc293d2bf4467530d`

Program owner inputs:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/design/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Predecessor: **S6D-01 architecture closed** by `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`.

Whole-project brief critique: `DEV/docs/superpowers/specs/2026-08-25-s6d-02-catalog-admission-gap-closure-brief-critic.md`.

This brief completes only S6D-02 Step 1. It does not execute Step 2 research, alter catalog/schema/runtime contracts, begin S6D-03, or resume R2.7 WP-06.

---

## 1. Problem statement

HDM currently exposes a broad machine vocabulary across `DEV/CATALOG/core-catalog.json`, the other coordinated catalog files, schemas, architecture owners, runtime contracts and tests. Earlier Steps 1–3 and Round-2 work admitted, retired and reshaped identifiers at different times. S6D-01 has now fixed how exact ruleset content and catalog context are identified, but it deliberately left the actual package instances, namespace claims, semantic content inventory and catalog failure admission to S6D-02.

The project therefore needs one evidence-backed admission decision for every currently registered machine ID relevant to the supported `v1.0-alpha` profile. Registration alone is not proof of product support; appearance in an older inventory is not proof of current ownership; a missing schema file is not automatically proof that an embedded or owner-local value is invalid; and a future/revisit item is not current work unless its trigger has fired.

For each admitted definition/world/runtime/value/selector/accessor/operation ID, S6D-02 must establish exactly one **admission disposition**:

1. **`ACTIVE_ADMITTED`** — current owner plus valid admission evidence exist, and the ID has a concrete machine destination adequate for admission;
2. **`EMBEDDED_NONOWNER`** — the ID is intentionally a bounded typed value/projection rather than independent canonical state, with its lifecycle and containing owner identified;
3. **`DORMANT_NONSELECTABLE`** — a current owning source preserves a meaningful activation trigger, the ID is not selectable/executable now, and no current consumer depends on it as active;
4. **`STALE_REMOVE`** — no valid current owner/evidence/trigger supports admission, so the ID and stale references must be retired coherently.

Admission is independent from **realization closure**. Every S6D-primary ID also receives a second axis: `COMPLETE`, or an exact downstream S6D-03…09/11 owner plus the missing contract. S6D-02 proves admission and machine destination; it does not falsely claim downstream metadata, schemas, primitive behavior or seed coverage are complete. Integrated S6D closure must eventually convert every S6D-primary active entry and residual Step-6 obligation to fully realized or remove it.

Inherited Round-2 vocabulary uses a stratum-appropriate terminal result: `INHERITED_ACTIVE — owner=<exact R2.x/WP>; consistency checked; no S6D realization obligation`. It enters S6D-primary scope only when concrete evidence exposes a contradiction or unsatisfied S6D consumer.

No fifth “registered placeholder”, “probably useful”, “documented somewhere”, or “implementation will decide later” state is admitted.

The central architecture risk is local reconciliation: deleting a suspicious ID because one catalog file lacks a consumer can break an indirect owner; retaining it because one historical document mentions it can preserve duplicate authority or executable vocabulary with no contract. S6D-02 must therefore reconcile the whole dependency subgraph, not audit `core-catalog.json` in isolation.

---

## 2. Goal

Produce a decision-ready, item-level catalog admission architecture that:

- accounts for every current registered ID in the S6D-02 scope;
- ties active IDs to actual canonical owners and valid admission evidence;
- records admission disposition separately from realization/closure state;
- distinguishes independent records from embedded values and noncanonical projections;
- distinguishes active support from dormant future triggers;
- removes stale vocabulary and stale references without preserving pre-release compatibility baggage;
- defines the bounded package/content inventory and namespace/failure obligations handed off by S6D-01;
- leaves metadata/shape/behavior completion to the correct later S6D domain instead of stealing its work;
- provides traceable closure evidence suitable for later S6D-11 machine verification and S6D-12 adversarial closure.

S6D-02 does not prove that every active ID is fully realized. It proves that retaining the ID is justified now and records the exact later owner of any missing realization contract.

Success is not “the catalog validates against its current schema.” Success is that every admitted ID has a justified place in the already accepted HDM ownership system and every rejected ID is removed from all active authority/consumer surfaces.

---

## 3. Scope

### 3.1 Registry scope and census strata

The census preserves exact set accounting across the coordinated catalog but applies three ownership-safe strata:

1. **S6D-primary admission families** — `definition.*`, `world.*`, `runtime.*`, `value.*`, Calculation Selectors, MechanicalContext accessors and Activity `op.*` primitives receive full S6D-02 admission decisions.
2. **Cross-surface referenced engine enums/policies** — transition/event/resource/effect/condition/life/temporal/targeting/signal/failure and similar IDs receive exact equality/stale-reference checks and inherit their current semantic owner unless concrete contradiction or an unsatisfied consumer is found.
3. **Later Round-2 vocabulary** — role/context/collaboration/chronology/recovery/Story/durability vocabularies remain semantically owned by their accepted R2.1–R2.6/WP-03 sources. S6D-02 records `INHERITED_ACTIVE`, checks catalog/schema/consumer consistency and records the exact R2.x/future-WP owner. It creates no S6D realization obligation and does not reopen those decisions or pull paused WP-07+ realization forward unless concrete contradiction or an unsatisfied S6D consumer explicitly promotes an item into S6D-primary scope.

Reconcile all entries in the current coordinated machine vocabulary, including at minimum:

- reusable `definition.*` kinds;
- `world.*` record kinds;
- `runtime.*` record kinds;
- `value.*` protocol kinds;
- facets and policy/enumeration IDs that are selectable or machine-significant;
- Activity family IDs;
- Activity primitive `op.*` IDs;
- transition and event IDs;
- resource/effect/condition/life-state/temporal IDs;
- `rule.*` operations;
- Calculation Selector IDs;
- MechanicalContext accessor IDs;
- targeting, area, range, signal, duration, resolution, command, failure and mapping vocabularies;
- later Round-2 role/context/collaboration/chronology/recovery/Story vocabulary currently registered in the same catalog generation.

The final census cannot omit a registry, but full fresh semantic admission is required only for the S6D-primary stratum. Other strata inherit accepted ownership unless evidence proves a real contradiction, stale reference or unsatisfied consumer.

### 3.2 Coordinated catalog surfaces

Reconcile at least:

- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/entity-structures.json`;
- `DEV/CATALOG/identifier-policies.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- schemas that enumerate, reference or constrain those IDs;
- architecture prose inventories and owner contracts;
- focused conformance and execution tests;
- runtime/release consumers and shipped rules/package surfaces.

### 3.3 S6D-01 handoff

S6D-02 must determine the actual admitted package/content inventory required to realize the S6D-01 identity laws:

- package instance or instances for shipped reusable rules content;
- namespace claims for each package/content source;
- exact semantic-file inventory boundary;
- admission of finite package/catalog failure distinctions;
- relationship between engine capability registries and ruleset definition content;
- proof that each admitted reusable definition belongs to one permitted namespace and that no same-ID shadowing is required.

S6D-02 must consume S6D-01 identity/adoption/recovery laws, not redesign them.

### 3.4 Gap discovery scope

A “gap” includes more than a missing ID. Investigate:

- registered ID with no owner;
- registered ID with no supported consumer;
- consumer referencing an unregistered ID;
- prose inventory versus machine catalog disagreement;
- schema enum/reference disagreement;
- catalog family represented as executable although only narrative/projection behavior exists;
- independent record admitted where an existing owner/value already suffices;
- embedded value promoted to independent record without lifecycle proof;
- active ID whose implementation status is actually dormant;
- dormant ID accidentally selectable/executable;
- stale ID retained in examples, schemas, tests, runtime docs or release packaging;
- machine alias or near-duplicate spelling that creates two apparent authorities;
- placeholder operation/selector/accessor whose exact metadata belongs to S6D-03–06 but whose admission itself is unsupported;
- package semantic content omitted from the S6D-01 lock boundary;
- current supported consumer whose required ID has no admitted machine destination.

### 3.5 Supported-profile boundary

Applicability is the supported HDM `v1.0-alpha` product/rules profile established by current engine/rules/runtime owners. Version metadata and `rules_baseline: D&D 2024 / SRD 5.2.1` identify a baseline, not the exact supported MVP seed. Full mechanics-family sufficiency belongs to S6D-09.

Use this admission-evidence hierarchy:

1. current canonical owner plus active machine/runtime consumer;
2. accepted supported-profile requirement with an exact downstream S6D realization owner;
3. reachable accepted-work, recovery, retention or package dependency;
4. otherwise an owner-approved dormant trigger, or `STALE_REMOVE`.

Generic D&D familiarity, rules-baseline metadata, a prose mention, historical inventory presence or the possibility that a future S6D domain might need an ID is not active admission evidence.

When support status is unclear, locate the current product/domain owner and preserve the ambiguity as an evidence issue. Do not ask the human architect to reconstruct repository facts. Escalate only a genuine product-scope or material authority/trade-off decision after the technical evidence is complete.

---

## 4. Non-goals

S6D-02 does not:

- complete per-selector metadata; that is S6D-03;
- complete MechanicalContext accessor/fact/dependency metadata; that is S6D-04;
- define full protocol-value schemas or targeting/cost contracts; that is S6D-05;
- define exact Activity primitive argument/result/read/write/RNG/atomicity contracts; that is S6D-06;
- close READY_PC progression content; that is S6D-07;
- prove HP/Resource/Effect/Condition/temporal seed behavior; that is S6D-08;
- claim full D&D mechanics-family coverage; that is S6D-09;
- redesign House Rules or policy adoption; S6D-10 consumes the closed owner;
- implement final catalog/schema test closure; that is S6D-11, although focused evidence/tests may be required to support an S6D-02 decision;
- perform the integrated adversarial closeout reserved for S6D-12;
- implement broad gameplay orchestration, a registry service, online discovery, arbitrary query/executable plugins or a compatibility layer for nonexistent released campaigns;
- reopen accepted Steps 1–5, House Rules or S6D-01 merely because their vocabulary overlaps this audit.

An incomplete detailed contract is not automatically an S6D-02 removal if admission is independently justified and the missing detail is explicitly owned by S6D-03–11. Conversely, a named later domain is not admission evidence by itself and cannot launder a placeholder.

---

## 5. Governing invariants

The work must preserve these accepted constraints unless current evidence proves a material conflict requiring a human superseding decision:

1. **Machine catalog authority.** Exact active IDs and validation shapes are machine-owned; prose inventories classify and explain but do not create a second enumeration authority.
2. **Minimum-sufficient class admission.** Capability, reusable definition, world record, runtime record, embedded value and noncanonical projection remain distinct by responsibility/lifecycle.
3. **No duplicate state authority.** Definitions do not own mutable instance state; runtime/evidence records do not become world truth; projections/indexes/checkpoints do not replace their natural owners.
4. **No prose-as-code.** Campaign/LLM content cannot invent executable primitives, selectors, accessors, state mutation or RNG authority.
5. **Inherited class model.** The accepted capability/definition/world/runtime/embedded-value/noncanonical-projection model is not a peer alternative in S6D-02. Individual entries change only on concrete contradiction, unsatisfied consumer or explicit superseding decision.
6. **One resolved definition identity.** One `ResolvedCatalogContext` contains at most one definition for each ID; layer order does not authorize same-ID shadowing.
7. **Package namespace ownership.** Reusable definitions must belong to a claimed package/source namespace; overlaps, out-of-claim definitions and ambiguous duplicates fail finitely.
8. **Exact reconstruction.** Active rules content participates in S6D-01 snapshot/lock identity; model memory, mutable tags, ambient files and discovery ranking are not authority.
9. **Discovery is not admission.** Search/ranking may find candidates, but only validated current owners and exact IDs authorize use.
10. **Coverage is not activation.** Supported, embedded, dormant and stale are distinct dispositions; future triggers are preserved without making dormant vocabulary selectable.
11. **Clean-slate pre-release rule.** No released campaign depends on superseded catalog generation shapes; stale IDs may be removed rather than migrated, while accepted current architecture and real consumers remain binding.
12. **Owner-local lifecycle.** A class/value cannot be admitted merely because storage technology can represent it; independent identity, lifecycle, retry/recovery or collaboration requirements must be proved.
13. **Bounded runtime.** No global repository scan, online registry, hidden scheduler, arbitrary executable/query surface or per-turn catalog archaeology is introduced.
14. **Accepted-work stability.** Catalog maintenance cannot reinterpret already accepted execution through a different unresolved rules basis.
15. **House Rules boundary.** Policy text/sidecars and `realization_refs` do not create catalog execution authority or same-ID overrides.
16. **Authority follows owning contracts.** If a current candidate conflicts with accepted architecture, first determine whether the candidate is wrong or the accepted owner is insufficient; do not silently rewrite either.

---

## 6. Mandatory whole-project Source Manifest

The Step-2 investigation must begin from the current remote ref and refine this manifest as dependencies are discovered. Every source receives a role label: CANONICAL, AMENDMENT/DECISION, DERIVATIVE, IMPLEMENTATION/TEST, RESEARCH or HISTORICAL.

### 6.1 Process, sequencing and scope owners

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- the S6D sequencing decision, S6D owner decision and parent S6D task brief;
- the S6D-01 eight-step chain and canonical `RULESET_PACKAGE_IDENTITY.md`.

### 6.2 Current catalog/class/identity owners

- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`;
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` as a locator only;
- catalog model/status/audit artifacts only with their current authority role and supersession understood.

### 6.3 Current machine realization

- every file in `DEV/CATALOG/`;
- every implicated file in `DEV/SCHEMAS/`, including catalog/envelope/entity/mechanical-surface and ID-bearing domain schemas;
- package/release manifests and builder inputs that select semantic rules content;
- current shipped rules/package content under `GAME/RULES/` and related templates.

### 6.4 Mechanical, execution and accepted-work retention owners

Inspect actual owners wherever their IDs appear, including:

- Actor, Asset, Resource, Effect, Condition, Duration/Recovery, Activity and Rule Element architecture;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`;
- Resolution/Continuation/receipt schemas and Step-3 execution/resume tests;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` and its resolution gate;
- S6D-01 §§6, 8, 10–12;
- mechanical evaluation, selectors, accessors, invocation facts and dependency laws;
- randomness, transition/state-delta and persistence owners;
- focused Step-1/2/3 conformance and example tests.

S6D-02 has one narrow retention duty: do not remove, reclassify or omit package content/IDs still required by a reachable accepted-work or typed retention owner. It does not redesign Resolution/Continuation recovery, checkpoints or garbage collection.

### 6.5 Round-2 and runtime consumers

The registry also contains vocabulary created by later accepted architecture. Follow it to its actual owners and consumers, including as applicable:

- truth/knowledge/information and Actor continuity;
- Context Runtime/logical roles/TurnEnvelope;
- Chronicler/Story and noncanonical Dramaturg projections;
- durability/publication/recovery/currentness;
- multiplayer collaboration/input coordination and chronology;
- House Rules realization linkage;
- `GAME/CORE/MECHANICS_INTEGRITY.md`, `ADJUDICATION.md`, `CHARACTER_READINESS.md`, `COMBAT.md`, `MAGIC.md`, `EXPLORATION.md`, `DIALOGUE.md`, `ADVANCEMENT.md`, `REWARDS.md` and any other discovered consumer.

### 6.6 Historical debt evidence

Inspect the accepted Step-1/2 assurance chain and R2.7 WP-03–06 artifacts that created or exposed catalog debt, including:

- critical catalog audit and catalog meta-model/class/evolution assurance;
- Step-2 final critical review and Steps 1–2 retrospective assurance;
- current R2.7 catalog/rules conformance tests and their owning specs;
- explicit deferred/revisit/gap items, preserving qualifiers and activation triggers.

Historical inventories are evidence, not current ID authority.

### 6.7 Consumer and stale-reference search

After structural routing through `PROJECT_MAP.md`:

- search every registered ID and every candidate retired ID across the current branch;
- distinguish authoritative uses from examples, tests, historical records and dead references;
- inspect schema `enum`/`const`/`$ref` consumers and generated/derived lists;
- inspect runtime branching/dispatch tables, validation code and release packaging;
- treat zero search results as non-evidence until the relevant directory/tree and owner route have been checked.

The final Source Manifest must record additions, exclusions and why each source can or cannot change the conclusion.

---

## 7. Required evidence products

Step 2 must produce item-level evidence rather than a thematic summary.

### 7.1 Registry census

For every registry family:

```text
Registry family:
Machine owner/path:
Schema owner/path:
Prose classification owner:
Consumer search boundary:
Total IDs:
IDs accounted:
Unresolved IDs:
```

The census must prove set equality between the machine authority and the admission ledger.

### 7.2 ID admission ledger

For every ID:

```text
ID:
Registry family:
Admission disposition:
Admission evidence class:
Realization/closure state (`COMPLETE`, exact downstream S6D owner, or `INHERITED_ACTIVE` with exact R2.x/WP owner):
Canonical semantic owner:
Machine destination:
Supported consumer(s) or accepted dependency:
Lifecycle/authority class:
Identity/namespace owner (N/A with reason when not package-scoped):
Applicability to supported profile:
Missing detailed contract, if any:
Exact downstream S6D/R2.7 owner:
Historical source/revisit trigger:
Conflicts/stale references:
Decision:
Exact closure evidence:
Confidence:
```

`ACTIVE_ADMITTED` means enough current evidence and machine destination exist to justify admission. `COMPLETE` is a separate realization claim. Package namespace/collision checks apply to reusable package content; engine capability/protocol IDs remain engine-owned vocabulary, and world/runtime instance identities are not package namespace claims.

### 7.3 Cross-surface mismatch ledger

Record each mismatch between:

- catalog and schema;
- catalog and prose owner;
- catalog and runtime consumer;
- catalog and test;
- current and historical terminology;
- package semantic inventory and registered content;
- admission status and selectability/executability.

Each mismatch receives a disposition and owner; no mismatch is hidden by editing only one side.

### 7.4 Package/content admission ledger

For each shipped/admitted semantic package or owner-local source:

```text
Source/package identity:
Namespace claim:
Semantic content paths:
Registered definition IDs:
Catalog generation/compatibility requirements:
Dependencies:
Collision result:
Lock participation:
Failure behavior:
```

Do not invent multiple packages merely to demonstrate the model. Prefer the minimum package structure proved by current shipped content and consumers.

### 7.5 Deferred-detail boundary ledger

For every active ID lacking full detail:

```text
ID:
Admission evidence:
Missing detail:
Why admission can be decided now:
Exact later S6D owner:
What would invalidate admission:
```

This prevents both premature deletion and placeholder laundering.

---

## 8. Questions the investigation must answer

1. What exact registry families and IDs are active machine vocabulary at the current ref?
2. For every ID, which current canonical owner and supported consumer justify it?
3. Which IDs are intentionally embedded/ephemeral values rather than independent records?
4. Which IDs are dormant, who owns the trigger, and how is accidental current selection prevented?
5. Which IDs are stale, and what active prose/schema/test/runtime/package references must be removed with them?
6. Are any active consumers using unregistered IDs, aliases or historical spellings?
7. Do prose inventories and machine catalogs disagree, including known class-table drift such as retired kinds persisting in another surface?
8. Does any concrete entry contradict the inherited minimum-sufficient class model or expose an unsatisfied consumer? The class model itself is not reopened by default.
9. Which current registry entries are capability vocabulary versus reusable ruleset definition content?
10. What is the minimum actual shipped ruleset package/content/namespace structure needed by S6D-01?
11. Do all active reusable definition IDs have one namespace owner without overlap or implicit same-ID shadowing?
12. Which package/catalog failure distinctions require machine admission now, and which exact failure envelope owns them?
13. Which selectors/accessors/operations are admission-valid but await S6D-03/04/06 metadata, and which lack any supported consumer and must be removed?
14. Which protocol values are admission-valid but await S6D-05 shape closure, and which are duplicate wrappers or stale?
15. Does any Round-2 vocabulary accidentally promote a projection/index/context product into canonical world/runtime authority?
16. Does any active ID imply arbitrary executable code, generic query access, hidden scheduling, ambient discovery authority or LLM-owned mutation?
17. Does accepted-work recovery require retention/admission not visible from ordinary current gameplay consumers?
18. Are current tests asserting only catalog/schema self-consistency, or do they prove real owner/consumer admission?
19. Which findings are purely technical consequences of accepted architecture, and which expose a genuine product-scope/material authority decision for the human architect?
20. Can the final ledger prove zero unclassified registered IDs—meaning every ID has a census stratum plus its stratum-appropriate disposition—and zero unresolved active references to removed/unregistered IDs?

---

## 9. Alternatives the investigation must compare

The research must remain solution-blind and compare at least:

### A. Evidence-backed per-ID admission ledger with coordinated cleanup

Treat the machine catalog as exact vocabulary authority, but require every ID to earn admission through current owner/consumer evidence. Remove stale vocabulary coherently and record dormant/embedded states explicitly.

### B. Registry-family admission with per-ID exceptions only

Attempt to admit whole coherent families from their owner contracts and enumerate only exceptions. This may reduce work but is acceptable only if it still proves item-level coverage and does not hide unsupported members.

### C. Preserve the existing registry and mark known gaps for later domains

This is the least disruptive approach, but it risks laundering placeholders and transferring an unbounded admission problem into S6D-03–11.

### D. Conditional minimality challenge, not a peer architecture

Use YAGNI to challenge individual admissions, but do not treat wholesale replacement by a “direct-flow-only” catalog as a credible alternative unless Step-2 evidence first proves the accepted class/admission architecture insufficient. Recovery, collaboration, package and other indirect current owners are valid evidence.

The Decision Brief may recommend a composition or a better evidence-derived alternative. It must compare complexity, traceability, false-retention risk, false-deletion risk, package/recovery impact and downstream S6D burden. Do not manufacture alternatives merely to reach a count.

---

## 10. Human/agent decision boundary

The agent owns:

- repository-wide source discovery and Source Manifest maintenance;
- registry census and item-level extraction;
- owner/consumer tracing;
- reconciliation of current and superseded sources;
- stale-reference search;
- identification of technically forced dispositions;
- cross-system impact analysis;
- alternatives and recommendation;
- propagation of accepted decisions across affected owners/catalogs/schemas/tests;
- proof of completeness.

Continue automatically when accepted architecture and current evidence determine one clearly preferable disposition.

Stop for the human architect only when evidence exposes a genuine unresolved decision involving:

- supported product/rules baseline scope;
- creation/removal of a user-visible capability with material product impact;
- a material authority/ownership trade-off between valid alternatives;
- explicit supersession of accepted architecture;
- acceptance of a critical compatibility/recovery/security risk.

Do not escalate catalog bookkeeping, obvious stale-reference cleanup, schema synchronization or consequences mechanically implied by accepted owners.

---

## 11. Step outputs and review gates

S6D-02 must complete its own full eight-step loop:

1. **Architecture Task Brief** — this artifact plus separate whole-project brief-critic record.
2. **Research & Architecture Draft** — complete Source Manifest, census, admission/mismatch/package/deferred-detail ledgers, alternatives and recommendation.
3. **Decision Brief** — decision-ready deltas and only genuine human decisions.
4. **Collaborative Architecture Review** — owner decisions where required.
5. **Candidate Specification** — exact admission laws, dispositions and coordinated change set.
6. **Adversarial Architecture Review** — independent whole-project critic, again reconstructing the direct/indirect dependency subgraph through `PROJECT_MAP.md`.
7. **Resolution Gate** — every BLOCKING/SIGNIFICANT finding resolved, rejected with evidence or escalated.
8. **Canonicalization** — owning contracts/catalogs/schemas/tests/status/PROJECT_MAP updated as required, publication verified, exact next continuation recorded.

Neither critic may review only the local S6D-02 artifacts. Both must locate actual owners and indirect consumers, test for pre-existing rules and decide whether a conflict belongs in the candidate or requires a superseding human decision.

---

## 12. Step-1 exit criteria

Step 1 is complete only when:

1. the brief defines bounded admission work without stealing downstream realization;
2. the initial Source Manifest and dependency routes cover all source classes capable of changing the framing;
3. admission and realization are separate axes;
4. registry strata prevent accidental reopening of later Round-2 owners;
5. the independent whole-project brief critic has no unresolved BLOCKING/SIGNIFICANT finding;
6. brief and critic are published and verified on the authoritative branch;
7. roadmap/status records S6D-02 Step 1 complete / Step 2 next;
8. no Step-2 census, per-ID disposition, cleanup or machine change has begun.

## 13. Full-loop exit criteria for S6D-02

S6D-02 may close only when:

1. the final Source Manifest covers the relevant direct and indirect ownership/dependency subgraph;
2. every current registry family has a census and exact machine owner;
3. every registered ID has a census stratum and exactly one stratum-appropriate admission disposition;
4. ledger-to-machine set equality is proven;
5. every S6D-primary `ACTIVE_ADMITTED` ID has a current semantic owner and valid admission evidence; every `INHERITED_ACTIVE` ID has an exact accepted R2.x/WP owner and no invented S6D realization obligation;
6. every embedded/ephemeral ID has a containing owner and no false independent lifecycle;
7. every dormant ID has a meaningful owner/trigger and is not currently selectable/executable;
8. every stale ID and all active stale references are removed coherently;
9. active consumers have no unresolved unregistered/alias IDs;
10. catalog, schema, prose, tests and runtime/package surfaces have no unresolved admission contradiction;
11. actual ruleset package/content/namespace admission required by S6D-01 is explicit and collision-safe;
12. active semantic content is included in the exact package lock boundary;
13. incomplete S6D-primary details are routed item-by-item to S6D-03–11 without using later work as justification for unsupported admission; inherited Round-2 details remain routed to their exact R2.x/WP owner;
14. no duplicate state/execution/LLM/query/scheduler authority is introduced or retained;
15. accepted-work/recovery consumers are preserved;
16. no obsolete pre-release compatibility scaffold remains solely for hypothetical campaigns;
17. focused verification proves the changed admission contracts and repository consistency;
18. the adversarial review has zero unresolved BLOCKING/SIGNIFICANT findings;
19. canonical owners and `PROJECT_MAP.md` are synchronized where responsibility/routing changed;
20. roadmap/status records S6D-02 closed and names S6D-03 Step 1 as next, without starting it.

---

## 14. Stop conditions

Stop and request a human decision only if:

- the supported `v1.0-alpha` product surface must materially expand or shrink;
- two valid canonical owners make incompatible claims and neither clearly supersedes the other;
- preserving accepted-work recovery conflicts with clean-slate removal in a way not resolved by current owners;
- a package/namespace choice creates a material ecosystem/evolution commitment;
- a critical risk must be explicitly accepted.

Do not stop merely because the registry is large, documentation is dispersed, stale references are numerous, or cleanup crosses several files. Those are agent evidence and consistency responsibilities.

---

## 15. Step-1 publication boundary

After the whole-project brief critic:

- repair every BLOCKING and SIGNIFICANT framing/source/dependency issue;
- publish this brief and the critic record to the authoritative branch;
- verify exact remote contents and branch HEAD through the GitHub Connector;
- update roadmap/status only if necessary to represent “S6D-02 Step 1 complete / Step 2 next” without marking S6D-02 architecture complete;
- stop before executing Step 2.

