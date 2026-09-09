# R2.7 WP-26 Step 1 — Documentation / Routing / Supersession Consistency — Architecture Task Brief + Source Manifest

Status: **COMPLETE / REPAIRED AT WORKER LEVEL — PENDING MANDATORY INDEPENDENT SENIOR STEP-1 REVIEW**

Date: 2026-09-09

This artifact is design-process provenance for **R2.7 WP-26 Step 1 only**. It is not a canonical WP-26 specification, does not supersede any semantic owner by itself, and does not authorize Step 2, implementation planning, implementation, release/migration execution, or gameplay/bootstrap.

## 1. Authorization and hard stop

Product Owner authorization for this work is limited to:

```text
WP-26 Step 1
    -> open-world task-specific Source Manifest
    -> complete Architecture Task Brief
    -> mandatory whole-project Step-1 critic
    -> read actual owners/dependencies exposed by the critic
    -> mechanically repair all BLOCKING/SIGNIFICANT framing omissions
    -> publish/read back/verify
    -> STOP for mandatory independent Senior review
```

Not authorized:

```text
WP-26 Step 2 or later
implementation planning
implementation
release/migration execution
gameplay/bootstrap
new branch creation
root README editing
```

The authoritative starting cursor in `DEV/CURRENT_PROGRESS.md` authorizes exactly this Step-1 package and no later unit.

## 2. Problem statement

HDM already has a large accepted architecture/specification corpus distributed across durable architecture owners, final specifications, later amendments/owner decisions, Product Owner inputs, runtime/module projections, schemas, tests, tools, and retained design provenance.

WP-26 is **not a new functional subsystem**. Its purpose is to remove routing and supersession ambiguity so that a later implementation/planning agent can, from current repository sources and without chat history or filename-recency guessing, determine:

- the current semantic owner for each relevant responsibility;
- which later amendment/owner decision qualifies or supersedes an older statement;
- which documents are design/history/provenance only;
- which runtime/schema/test/tool surfaces are current realization, stale realization, deferred realization, or evidence;
- which current paths/names/schemas/terms are valid;
- which accepted requirements still require future realization;
- which closed architecture must not be redesigned merely because an older document overlaps it.

The WP-26 invariant is:

> implementation/planning discovery must not depend on filename recency, remembered topology, chat history, or bulk-reading the complete design corpus merely to know which law currently controls.

The cleanup must preserve useful history. Historical analysis is not rewritten as though later corrections were known when it was authored.

## 3. Selected Step-1 framing model

WP-26 uses the minimal project-aligned approach:

```text
OWNER-FIRST ROUTING
    + LOCAL SUPERSESSION
    + TARGETED MACHINE-GUARD RECONCILIATION
```

This means:

1. current semantic owners and accepted amendments/owner decisions remain the law;
2. `DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` remain derivative navigation surfaces;
3. stale current-looking wording receives a targeted supersession/disposition rather than history erasure;
4. schemas/tests/audits/runtime projections are checked bidirectionally against accepted law;
5. a machine guard that still enforces superseded semantics is a realization defect, not evidence that the old semantics remain current;
6. accepted-but-unrealized requirements are preserved explicitly for WP-27 rather than silently treated as either implemented or reopened architecture.

WP-26 does not create a global documentation database, universal supersession graph/runtime, Markdown metadata registry, duplicate canonical registry, global status hierarchy, or mandatory annotation framework.

## 4. In scope

WP-26 must later reconcile, at minimum:

- current owner routing through `DEV/PROJECT_MAP.md`, `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`, `DEV/CURRENT_PROGRESS.md`, the roadmap, applicable Product Owner routes, and the Superpowers taxonomy/router;
- canonical/current versus amendment/decision versus historical/design/provenance classification;
- accepted requirements hidden only in historical/design artifacts;
- conflicting current-looking specifications without explicit supersession;
- stale old-topology, old-path, old-schema, old-version-policy, old-Stage/Step framing, and old status pointers;
- CORE module headers/activation metadata, `CORE_INDEX.md`, Project Instructions/bootstrap/loading instructions, runtime behavior, schemas/templates, tests, and maintenance audit guards;
- PO-009 Commentator/Story corpus sufficiency routing and targeted supersession;
- PO-010 mutable GitHub artifact sizing-band routing and targeted threshold-policy supersession;
- Product Owner deferred/future realization obligations that must survive into WP-27;
- exact README mismatches as report-only findings unless separate Product Owner approval authorizes editing.

## 5. Out of scope

Step 1 and WP-26 do not:

- design a new gameplay subsystem;
- redesign WP-18, WP-19, Step-4 knowledge/disclosure/Story, R2.3 Context Runtime, WP-24, or WP-25 merely because later decisions qualify one consumer or threshold;
- implement Commentator Story projection/schema/cache;
- create a second ACL, `world.knowledge`, or `runtime.disclosure` owner;
- impose one shared Master/Commentator SQLite schema;
- implement generic `FailureDisposition` machinery;
- implement mutable-artifact partitioning/rollover;
- choose exact physical shard/page/SQLite topology before an owner-valid realization decision requires it;
- create new runtime scheduling, worker, heartbeat, retry, or global registry machinery;
- write an implementation plan;
- execute release/migration work;
- rewrite the root README without explicit Product Owner authorization.

## 6. Source-role model

Every material source in WP-26 is classified as one of:

```text
CANONICAL / OWNING
CANONICAL AMENDMENT / OWNER DECISION
PRODUCT OWNER INTENT / REQUIREMENT INPUT
DERIVATIVE LOCATOR / INDEX
IMPLEMENTATION / MACHINE CONTRACT / TEST
DESIGN PROVENANCE
HISTORICAL / SUPERSEDED
DEFERRED / FUTURE CONSUMER
```

Rules:

- placement in `specs/` does not prove that every sentence remains current;
- a later filename/date does not prove supersession;
- `CURRENT_PROGRESS.md` owns the global current cursor, not architecture semantics;
- Project Map / canonical index route to owners and never become owners themselves;
- current machine/runtime/tests can be stale realization and do not override accepted semantics;
- historical design artifacts remain inspectable when provenance, supersession, or hidden accepted semantics require them;
- an accepted owner decision can target only one law/consumer while leaving the rest of the older owner intact.

## 7. Dependency subgraph

The Step-1 dependency graph reconstructed from `DEV/PROJECT_MAP.md` and actual owners is:

```text
process / authority
    AGENTS
    -> DESIGN_PROCESS
    -> ARCHITECTURE/DESIGN_PROCESS
    -> PRODUCT_OWNER_INPUT_PROCESS
    -> CURRENT_PROGRESS
    -> PROJECT_MAP
    -> R2.7 owner clarification / roadmap

routing / implementation discovery
    CURRENT_PROGRESS
    -> applicable PRODUCT_OWNER_INPUT entries
    -> PROJECT_MAP / CANONICAL_ARCHITECTURE_INDEX
    -> durable owners + final accepted specs/amendments
    -> implicated runtime/schema/test/tool consumers

PO-009 Commentator / Story
    PO-009 accepted owner decision
    -> Story producer/persistence/retrospective contract
    -> Story baseline projection source contracts
    -> Story growth/sharding/consumer-decoupling owner decision
    -> WP-18 + final Senior recovery amendment
    -> WP-19 + PO-003 historical Actor basis owner
    -> Step-4 truth/knowledge/role-context/Story owner
    -> R2.3 Context Runtime + WP-09 realization
    -> ACCESS_CONTROL
    -> Story-related schema/test/runtime realization state
    -> PROJECT_MAP / canonical index

PO-010 mutable artifact sizing
    PO-010 accepted owner decision
    -> 2026-09-04 mutable-artifact size owner decision
    -> WP-24 LAW WP24-13
    -> Story growth/sharding owner decision
    -> persistence/storage/LIVE writers
    -> layout-determining schemas/templates
    -> tests/audits/deferred realization ledgers
    -> PROJECT_MAP / canonical index

runtime activation / readiness / onboarding
    PLAY_POLICY activation law
    -> CORE module headers
    -> CORE_INDEX
    -> CHARACTER_READINESS
    -> DIEGETIC_ONBOARDING
    -> WP-19
    -> NEW_CAMPAIGN_FAST_PATH
    -> RUNTIME / CAMPAIGN_SETUP / SAVE_CONTRACT
    -> INSTALL bootstrap / Project Instructions
    -> onboarding/bootstrap regression cases
    -> maintenance audit guards

WP-27 future input
    all current owners + amendments
    -> accepted-but-unrealized obligations
    -> exact stale-realization classifications
    -> implementation workstream/dependency/version/test derivation later
```

## 8. Open-world Source Manifest

`Inspection status` describes Step-1 evidence depth. `OPEN FAMILY` means the route is admitted to the manifest and must be exhausted to the claim-relevant depth during WP-26 before final coverage/canonicalization; it is not evidence of absence.

| Source / family | Role | Why relevant | Step-1 inspection status / disposition |
|---|---|---|---|
| `AGENTS.md` | CANONICAL / OWNING process | bootstrap, taxonomy, README, branch, version-impact, publication rules | INSPECTED |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | CANONICAL runtime overlay | authoritative Connector transport/verification mechanics | INSPECTED |
| `DEV/DESIGN_PROCESS.md` | CANONICAL / OWNING process | Source Manifest, critic, synthesis and decision gates | INSPECTED |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL project adapter | mandatory whole-project Step-1 critic and Senior stop | INSPECTED |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | CANONICAL process addendum | PO routing/status/trigger semantics | INSPECTED |
| `DEV/CURRENT_PROGRESS.md` | CURRENT-PROGRESS AUTHORITY | sole global cursor/gate | INSPECTED |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR / INDEX | dependency discovery and later routing repair target | INSPECTED |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE LOCATOR / INDEX | integrated accepted-architecture locator and supersession aid | INSPECTED |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | DERIVATIVE sequencing owner | R2 sequence/scope, not current cursor | INSPECTED |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | CANONICAL OWNER DECISION | WP-26 must reconcile whole accepted project, architecture↔machine bidirectionally | INSPECTED |
| `DEV/docs/superpowers/README.md` | DERIVATIVE TAXONOMY ROUTER | current research/design/specs/plans taxonomy | INSPECTED |
| `DEV/PRODUCT_OWNER_INPUT.md` PO-001..010 | PRODUCT OWNER INTENT / ROUTING | preserved intent, current/deferred consumers, WP-27 carry-forward | INSPECTED at routing/item level; owning consumers expand task-specifically |
| PO-009 owner decision | CANONICAL AMENDMENT / OWNER DECISION | current Commentator self-contained corpus/control law | INSPECTED |
| Story producer/persistence/retrospective contract | CURRENT IMPLEMENTATION-FACING SPEC with targeted PO-009 supersession | contains native fallback wording that can mislead baseline Commentator implementation | INSPECTED |
| Story baseline projection source contracts | CURRENT IMPLEMENTATION-FACING SPEC with targeted PO-009 supersession | contains native-only T0 representation allowance superseded for baseline Commentator retained basis | INSPECTED |
| Story growth/sharding/consumer-decoupling decision | CURRENT OWNER with targeted PO-010 threshold supersession | growth/decoupling current; hard 10 KiB threshold wording superseded | INSPECTED |
| WP-18 canonical + final Senior recovery amendment | CANONICAL / AMENDMENT | Story nonauthority, planning/consumer boundaries, realization policy | INSPECTED |
| WP-19 canonical + PO-003 Actor-basis decision | CANONICAL / OWNER DECISION | native T0 Actor authority and historical basis; PO-009 adds Story-local consumer projection only | INSPECTED |
| Step-4 truth/knowledge/role-context/Story owner | CANONICAL / OWNING | content/knowledge/disclosure authority and Story nonauthority | INSPECTED |
| R2.3 Context Runtime + WP-09 canonical | CANONICAL / REALIZATION OWNER | eligibility/retrieval/materialization and bounded context behavior | INSPECTED |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | CANONICAL / OWNING | campaign/player authorization; prevents Commentator ACL duplication | INSPECTED |
| Story-related `GAME/SCHEMA`, DEV schemas/tests/runtime consumers | IMPLEMENTATION / MACHINE CONTRACT / TEST | determine whether PO-009 projection is realized or deferred | HIGH-RISK INVENTORY INSPECTED; no dedicated baseline Commentator schema found; full task-specific sweep remains WP-26 obligation |
| `DEV/TESTS/test_step4_story_retirement_contract.py` | TEST EVIDENCE | guards retired Story topology, not PO-009 projection | INSPECTED |
| `DEV/TESTS/test_wp18_final_senior_recovery.py` | TEST EVIDENCE | WP-18 recovery/planning owner chain, not PO-009 projection | INSPECTED |
| PO-010 owner decision | CANONICAL AMENDMENT / OWNER DECISION | current sizing bands; supersedes universal exact-byte cutoff | INSPECTED |
| `2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` | PARTIALLY SUPERSEDED OWNER DECISION | no truncation/owner-valid representation retained; universal 10240 reject superseded | INSPECTED |
| WP-24 canonical, especially LAW WP24-13 | CANONICAL WP with targeted PO-010 supersession | closed WP-24 remains current except exact hard-cap threshold law | INSPECTED |
| `GAME/CORE/PERSISTENCE.md`, `STORAGE.md`, `LIVE_SCENE.md` | CURRENT RUNTIME OWNERS | writer/currentness/rollover surfaces; no universal 10240 cutoff found in inspected current text | INSPECTED |
| layout-determining schemas/templates | IMPLEMENTATION / MACHINE CONTRACT | may encode future partition/rollover decisions | OPEN FAMILY for WP-26 task-specific sweep |
| tests/audits with `10240`, `10 KiB`, `10,240`, `MAX_BYTES`, hard-cap/publication wording | TEST / MACHINE GUARD | can fossilize superseded threshold policy | OPEN FAMILY; known high-risk docs identified, exhaustive exact-ref sweep required in WP-26 execution |
| `GAME/CORE/PLAY_POLICY.md` | CURRENT RUNTIME OWNER | CORE cache/activation; headers control activation, CORE_INDEX derivative | INSPECTED |
| `GAME/CORE/CHARACTER_READINESS.md` | CURRENT RUNTIME OWNER | READY_PC is not a gate on beginning gameplay; provisional bounded play allowed | INSPECTED |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | CURRENT RUNTIME OWNER for onboarding | repaired no-hard-pre-live/live cutover semantics | INSPECTED |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | CURRENT RUNTIME OWNER | scaffold/bootstrap ordering and current provisional/READY transitions | INSPECTED |
| `GAME/CORE/RUNTIME.md`, `CAMPAIGN_SETUP.md`, `SAVE_CONTRACT.md` | CURRENT RUNTIME SURFACES with suspected stale realization | still contain hard pre-live/true-live/PLAY_READY framing inconsistent with current readiness/onboarding law | INSPECTED |
| `GAME/CORE/CORE_INDEX.md` | DERIVATIVE RUNTIME ROUTER | must summarize headers/owners without inventing activation or old lifecycle law | INSPECTED; stale pre-live descriptions identified |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `PROJECT_INSTRUCTIONS.txt` | INSTALL / ROUTING | bootstrap/loading/project-instruction consistency | INSPECTED |
| `DEV/TESTS/DIEGETIC_ONBOARDING_CASES.md`, `BOOTSTRAP_STORAGE_REGRESSION_CASES.md` | TEST EVIDENCE / MACHINE GUARD | include old true-live/pre-live assertions that can preserve stale topology | INSPECTED |
| `DEV/TOOLS/audit_engine.py` | MACHINE GUARD / AUDIT | activation guard is useful; persistence/onboarding checks currently require stale pre-live wording | INSPECTED |
| `DEV/TESTS/test_product_owner_routing_consistency.py` | TEST / ROUTING GUARD | guards some PO route consistency but not new PO-009/010 discovery semantics | INSPECTED |
| `DEV/TESTS/test_project_map_retrospective_hotfixes.py` | TEST / ROUTING GUARD | demonstrates derivative-map regression style; does not cover PO-009/010 | INSPECTED |
| current exact repository tree at starting HEAD | STRUCTURAL EVIDENCE | confirms current taxonomy/paths; no repository-root `docs/superpowers/` tree | INSPECTED |
| historical specs/design artifacts with transient `Target branch` / old status metadata | HISTORICAL / DESIGN PROVENANCE or current spec with stale metadata | transient branch/status text must not be mistaken for semantic currentness | REPRESENTATIVE CURRENT-RISK EXAMPLES INSPECTED; full WP-26 sweep required |
| root `README.md` | MANUALLY CURATED PUBLIC DOC | report-only mismatch boundary | INSPECTED; one exact path mismatch recorded below |
| `DEV/RELEASE/VERSIONING.md` + canonical compatibility/version policy | CANONICAL VERSION OWNER | Step-1 Version Impact Gate and later realization bump routing | INSPECTED |
| `DEV/SCHEMAS/*`, `GAME/SCHEMA/*`, `GAME/CAMPAIGN/*`, `DEV/TESTS/*`, DEV tools | IMPLEMENTATION / MACHINE CONTRACT / TEST | open-world bidirectional architecture↔realization coverage | OPEN FAMILIES; expand only by task-specific routes, not bulk-preload |
| `DEV/docs/superpowers/research/*` | RESEARCH INPUT | evidence only when applicability/reopening requires it | OPEN ON DEMAND |
| `DEV/docs/superpowers/design/*` | DESIGN PROVENANCE | inspect when hidden accepted semantics/supersession provenance must be recovered | OPEN ON DEMAND |
| `DEV/docs/superpowers/plans/*` | HISTORICAL/FUTURE IMPLEMENTATION PLANS | not architecture authority; inspect only where stale current implementation routing could mislead | OPEN ON DEMAND |

### 8.1 Search/currentness limitation

Connector code-search covers the repository default branch, while this task's authority is `v1/engine-rearchitecture`. Therefore Step-1 absence claims do **not** rely on default-branch code-search results. Current-tree structural inventory plus exact-ref file/directory reads are used for authoritative evidence; later WP-26 consumer sweeps must continue with exact-ref/current-tree methods or another Connector read surface that proves the active ref.

## 9. Current routing / supersession model

WP-26 must converge on this discovery rule:

```text
current global cursor
    DEV/CURRENT_PROGRESS.md

applicable Product Owner intent/accepted decision
    DEV/PRODUCT_OWNER_INPUT.md
    -> accepted owner decision named by the route

semantic concern
    DEV/PROJECT_MAP.md / CANONICAL_ARCHITECTURE_INDEX.md as locators only
    -> actual current owner
    -> later accepted amendment/owner decision
    -> current realization/tests as consumers/evidence

historical/provenance artifact
    may explain derivation
    -> never overrides current owner merely by date/path/detail
```

For a targeted supersession:

```text
OLDER OWNER remains current for unaffected semantics
LATER OWNER DECISION controls only the explicitly superseded/extended law
DERIVATIVE ROUTING must make that relationship discoverable
STALE REALIZATION must be repaired or explicitly classified
```

## 10. Known inconsistency / debt seeds established in Step 1

These are **not unresolved Step-1 framing findings** after the critic repair below. They are proven WP-26 cleanup obligations for later authorized Steps 2–8.

### D26-01 — PO-009 native-fallback leakage

Current-looking Story integration/source-contract text still allows the baseline Commentator to depend on native WP-19 T0 navigation/fallback. PO-009 now requires retained Story-local bounded T0 values plus a self-contained derived eligibility/control projection for the baseline Commentator.

Disposition:

```text
TARGETED SUPERSESSION / EXTENSION
no WP-18/WP-19/Step-4/R2.3 wholesale reopen
native Master owners remain canon
Story remains noncanonical
baseline Commentator native fallback for required T0/control basis is not conforming
realization remains future work
```

### D26-02 — PO-010 hard-cap leakage

The old mutable-artifact owner, WP-24 LAW WP24-13, and Story growth/sharding owner still contain current-looking universal `10240` / hard-publication-cutoff language. PO-010 supersedes only that threshold policy with sizing decision bands.

Disposition:

```text
TARGETED THRESHOLD-POLICY SUPERSESSION
WP-24 remains CLOSED
Story growth/partition/currentness law otherwise retained
no truncation retained
owner-valid partition/rollover retained
no universal >10240 => invalid/reject law
realization remains future work
```

### D26-03 — provisional gameplay / pre-live topology contradiction

Current `CHARACTER_READINESS.md`, repaired `DIEGETIC_ONBOARDING.md`, and WP-19 allow gameplay before READY_PC when exact local mechanic dependencies for the bounded outcome are sufficient. Current `RUNTIME.md`, `CAMPAIGN_SETUP.md`, `SAVE_CONTRACT.md`, `CORE_INDEX.md`, onboarding regression cases, and maintenance-audit assertions still contain hard `pre-live` / `true live` / post-PLAY_READY-only framing.

This is a cross-module current-realization contradiction, not a new product question.

Disposition:

```text
STALE CURRENT REALIZATION / MACHINE-GUARD DEBT
repair under WP-26 only after Step-1 Senior GO
preserve readiness/lifecycle/durability owners
no new lifecycle subsystem
```

### D26-04 — current-looking status / transient branch metadata

Several accepted/current specs retain historical worker status such as final Senior review pending even though `CURRENT_PROGRESS.md` records closure, and older accepted specs can retain transient `Target branch` metadata from prior development branches.

Disposition:

```text
semantic owner remains determined by accepted owner chain, not header recency
historical provenance is retained
WP-26 must distinguish harmless historical metadata from live routing that requires correction
CURRENT_PROGRESS remains sole global cursor
```

### D26-05 — derivative routing lag for PO-009 / PO-010

`PROJECT_MAP` and `CANONICAL_ARCHITECTURE_INDEX` predate the September 9 PO-009/010 decisions and do not yet provide a sufficiently direct targeted-supersession route for both decisions.

Disposition:

```text
DERIVATIVE ROUTING DEBT
repair during WP-26 after Step-1 Senior GO unless Senior requires a Step-1 routing amendment
no new semantic owner created by the indexes
```

The final Step-1 Source Manifest above provides the authoritative review route for this gate without pretending the derivative indexes have already been reconciled.

### D26-06 — stale/deferred Product Owner route lifecycle

The PO ledger itself contains future-consumer wording that can age. Concrete example: PO-006 still describes WP-24 operational-budget consumption as deferred/when WP-24 opens, while WP-24 is now closed and explicitly preserves retained-ref non-authority/no-delete constraints.

Disposition:

```text
ROUTING/STATUS STALENESS
not product-semantic reopen
reconcile ledger route during WP-26
preserve still-deferred implementation consumers from PO-001..010 for WP-27
```

### D26-07 — accepted decision != realized implementation

PO-009 and PO-010 are accepted architecture decisions, but Step-1 evidence does not establish dedicated Commentator projection schema/tests/cache realization or a complete sizing-band writer/schema/test realization.

Disposition:

```text
ACCEPTED / CURRENT SEMANTICS
+ DEFERRED FUTURE REALIZATION
!= absent requirement
!= already implemented
!= permission to fall back to superseded baseline
```

## 11. PO-009 impact and attack line

Attack question:

> Can a future implementation agent, following current routing/spec corpus without chat history, incorrectly implement a baseline Commentator that requires native Master fallback for WP-19 T0 basis or live native eligibility reads?

Step-1 answer:

```text
YES — BEFORE WP-26 CLEANUP
```

Evidence:

- the Story producer/persistence/retrospective contract still describes native T0 escalation after Story insufficiency;
- the baseline projection source contracts still permit native-only T0 factor navigation instead of retaining all mandatory baseline T0 values Story-locally;
- PO-009 now explicitly makes `Story corpus + Commentator eligibility/control projection` the baseline Commentator's self-contained factual-support universe.

Current owner precedence for WP-26 is therefore:

```text
Master gameplay truth/Actor/access/knowledge/disclosure owners
    remain canonical for Master gameplay

PO-009
    targetedly supersedes baseline Commentator representation/fallback requirement

Story
    remains noncanonical to gameplay
    but must retain the bounded T0 values required by the baseline Commentator

Commentator control projection
    is derived/self-contained for the snapshot
    != new ACL owner
    != live native eligibility oracle
```

Mandatory later WP-26 cleanup must make that relationship discoverable without needing this Step-1 brief.

## 12. PO-010 impact and attack line

Attack question:

> Can a future implementation agent, following current specs/tests/routing, still implement unconditional `>10240 bytes => reject` as an HDM-wide law?

Step-1 answer:

```text
YES — BEFORE WP-26 CLEANUP
```

Evidence:

- the September 4 owner decision defines an exact universal 10240-byte hard cap;
- WP-24 LAW WP24-13 repeats it as a mandatory hard publication trigger;
- the Story growth/sharding owner also consumes it as a hard invariant;
- PO-010 later supersedes that exact-byte validity rule with sizing decision bands.

Current controlling threshold policy is:

```text
preferred target          ~10–12 KiB or smaller
normal review zone        ~13–16 KiB
above ~16 KiB             review / partition / rollover default expectation
```

`10 KiB` may survive as simple human shorthand. It must not survive as a universal exact validity/rejection enum.

## 13. Current-vs-historical handling rules

WP-26 cleanup uses the least destructive sufficient operation:

1. targeted correction on a current implementation-facing owner when its current wording is wrong;
2. explicit supersession notice when an older source remains valuable/current in unaffected scope;
3. compact later owner/amendment when that is already the accepted authority;
4. derivative routing update so implementation discovery reaches the later owner;
5. historical/provenance classification when the artifact should remain readable but not current;
6. consolidation only when it materially improves implementation discovery and leaves one unambiguous current owner.

Do not back-edit historical analysis so it appears to have anticipated later findings. Do not delete useful provenance just to reduce file count.

## 14. README boundary

Root `README.md` remains manually curated Product Owner editorial material.

Step-1 exact mismatch found:

```text
README nerd-section path: DEV/TOOLS/run_release_build
current repository/AGENTS canonical entry point: DEV/TOOLS/run_release_build.py
```

Classification:

```text
MINOR NAVIGATION/PATH MISMATCH
NO ARCHITECTURE AUTHORITY IMPACT
REPORT ONLY
README EDIT NOT AUTHORIZED
```

WP-26 must report any additional README mismatch it finds; it must not opportunistically rewrite the README.

## 15. Machine/runtime/schema/test consistency boundary

WP-26 performs bidirectional reconciliation:

```text
accepted semantic law
    -> current runtime/module projection
    -> schema/template representation where needed
    -> test/audit guard

and

current runtime/schema/template/test/audit responsibility
    -> accepted owner
    OR explicit stale/deferred/evidence classification
```

A current test/audit that requires superseded wording is a defect in the guard. Green CI against stale expectations cannot make superseded architecture current.

Mechanically implied synchronization is eligible only when the accepted result is already uniquely determined and no new material architecture choice is introduced. Step 1 records those obligations; it does not execute the full cleanup.

## 16. Repair-now versus retain/defer criteria

Repair during WP-26 when all are true:

- a current implementation-facing/routing/machine surface conflicts with an already accepted current owner;
- the exact correction is mechanically implied;
- the repair does not choose a new topology/data model/interface/product semantic trade-off;
- leaving it would materially misroute WP-27 or implementation planning.

Retain as historical/provenance when:

- the statement is accurate for its historical decision point;
- current routing clearly marks it non-current/qualified;
- rewriting it would falsify derivation history.

Defer realization when:

- accepted semantics are clear;
- no current correctness/routing claim requires pretending realization exists;
- realization needs implementation planning, schema/code work, empirical calibration, or a later authorized gate.

Escalate to Product Owner only if evidence leaves a genuine product semantic/material trade-off/authority/compatibility/risk/scope choice.

## 17. Anti-overengineering constraints

WP-26 must not introduce by default:

- global documentation authority database;
- universal supersession graph/runtime;
- metadata registry for every Markdown file;
- duplicate canonical architecture registry;
- new mandatory annotation framework;
- global currentness/status hierarchy beyond existing owners;
- runtime dependencies whose only purpose is development-document bookkeeping.

Prefer local links/notices and existing derivative routers.

## 18. WP-27 handoff / readiness obligations

WP-26 closure must leave WP-27 a clean evidence input, not an implementation plan.

At minimum, WP-27 must later be able to derive without reopening settled architecture:

### PO-009

- Story-local bounded T0 values required by baseline Commentator;
- private/off-screen/secret retention with protection metadata;
- self-contained derived eligibility/control projection per snapshot;
- `CONTENT BASIS != CONTROL/ELIGIBILITY BASIS`;
- `CONTENT_FINAL != ACCESS_FINAL`;
- deterministic filtering before LLM materialization;
- anti-oracle/anti-ACL-duplication tests;
- Commentator cache/schema isolation from Master HOT/cache;
- applicable schema/version/test work.

### PO-010

- writer/layout decisions needed for campaign-growing mutable artifacts;
- sizing-band review/partition/rollover behavior;
- owner-valid deterministic partition/rollover;
- no truncation and authority/currentness preservation;
- schemas/tests/version impact where realization requires them.

### Other accepted Product Owner routes

WP-27 must preserve all still-deferred/current consumers from PO-001..008 and later accepted inputs, including examples already explicit in the ledger such as creator-login fail-closed realization, WP-25 generic `FailureDisposition`/host-risk realization and empirical proof, and any other consumer that remains `DEFERRED` after WP-26 reconciliation.

A closed architecture WP does not imply every implementation consumer is realized.

## 19. Risks and adversarial questions

The mandatory critic must attack at least:

1. Did the manifest miss a current owner or superseding decision?
2. Can a current-looking historical/status artifact override a later owner by accident?
3. Are accepted semantics stranded only in design/history?
4. Do two current-looking specs answer the same implementation question differently without an explicit supersession route?
5. Can PO-009 still be implemented with native baseline T0/control fallback?
6. Can PO-009 create an information oracle or second ACL accidentally?
7. Can PO-010 still become an unconditional 10240-byte reject law?
8. Are old pre-live/true-live assumptions still encoded in current CORE/tests/audit guards?
9. Are old paths/schema/topology/version names still live consumers rather than harmless historical text?
10. Is root README being treated as ordinary cleanup material?
11. Is WP-26 inventing a central documentation subsystem instead of fixing existing routing?
12. Is implementation being smuggled into architecture cleanup?
13. Are deferred realization obligations being lost before WP-27?
14. Is filename/date/status-header recency being used as authority evidence?

## 20. Version Impact expectation — Step 1

Step-1 planned writes are design-process provenance and current-progress/routing bookkeeping only. No version-bearing runtime semantic module, persistent/protocol schema, catalog/ruleset generation, package format, migration law, or engine release identity is changed by the Step-1 package.

Expected Step-1 gate:

```text
VERSION_IMPACT: NONE
ENGINE_VERSION_BUMP_REQUIRED: NO
MODULE_VERSION_BUMP_REQUIRED: NO
SCHEMA/GENERATION_BUMP_REQUIRED: NO
```

This expectation must be rechecked against the actual published Step-1 changed-file set before completion evidence is reported.

## 21. Step-1 whole-project critic repair overlay

The mandatory critic recorded in the companion Step-1 critic artifact found no BLOCKING issue and seven SIGNIFICANT framing/completeness defects. All seven were mechanically repaired in this final Task Brief by:

1. making PO-009 targeted supersession and the native-fallback attack line explicit;
2. making PO-010 targeted threshold supersession and exact hard-cap attack explicit;
3. adding the current readiness/onboarding/activation runtime + audit/test contradiction to the WP-26 graph;
4. adding derivative-router/current-looking-status/transient-metadata ambiguity as an explicit concern family;
5. adding PO-ledger route aging plus PO-001..010 deferred-consumer preservation for WP-27;
6. separating accepted PO-009/010 semantics from their still-deferred machine/schema/test realization;
7. expanding the Source Manifest from prose owners into the implicated schema/template/test/audit/runtime families and recording the exact-ref search limitation.

The underlying corpus cleanup obligations `D26-01..07` remain intentionally open for later WP-26 Steps 2–8 after Senior GO. That is not an unresolved Step-1 framing defect.

## 22. Step-1 exit criteria

Step 1 is worker-complete only when all are true:

```text
[ ] authoritative branch/ref was fresh-checked
[ ] current cursor authorized WP-26 Step 1 only
[ ] current process owners were read
[ ] open-world Source Manifest exists and distinguishes source roles
[ ] actual high-risk owners/consumers were inspected
[ ] complete Task Brief exists
[ ] PO-009 attack line is answered from current evidence
[ ] PO-010 attack line is answered from current evidence
[ ] CORE/readiness/activation + machine-guard contradiction is in scope
[ ] current-vs-history and repair/defer rules are explicit
[ ] README is report-only
[ ] WP-27 deferred-realization handoff is explicit
[ ] whole-project Step-1 critic ran independently over the dependency graph
[ ] all mechanically resolvable BLOCKING/SIGNIFICANT Step-1 framing findings are repaired
[ ] HUMAN_DECISION_REQUIRED is truthfully established
[ ] actual Step-1 Version Impact Gate is complete
[ ] coherent publication/readback/exact-head verification is complete
[ ] CURRENT_PROGRESS points to mandatory independent Senior review
[ ] NEXT_AUTHORIZED_UNIT = NONE
```

## 23. Mandatory Senior stop

Worker disposition after publication:

```text
STEP1_SOURCE_MANIFEST: COMPLETE
STEP1_TASK_BRIEF: COMPLETE / REPAIRED
STEP1_CRITIC: COMPLETE
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
WP26_STEP2_AUTHORIZED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-26 Step-1 Senior review
```

Do not begin Step 2 until that review returns GO.