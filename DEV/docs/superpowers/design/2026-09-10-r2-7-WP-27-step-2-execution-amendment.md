# R2.7 WP-27 Step 2 — Evidence-Extraction Execution Amendment

Status: **CURRENT TASK-BRIEF AMENDMENT — STEP 2 EXECUTION OWNER / STEP 3 NOT AUTHORIZED BY THIS ASSIGNMENT**

Date: 2026-09-10

Amends:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-task-brief-senior-repair-amendment.md`.

Purpose: make WP-27 Step 2 mechanically auditable and safe to execute in bounded slices by a fresh worker without relying on chat context, filename symmetry, thematic summaries, or corpus-wide rereading.

This amendment changes **audit execution and evidence structure only**. It does not change accepted HDM architecture, Product Owner semantics, closed WP decisions, version law, implementation authorization, release authorization, or gameplay/runtime behavior.

Where this amendment is more specific than the earlier WP-27 Task Brief for **Step 2 execution**, this amendment controls. All earlier Step-1 architecture-blocker tests, Source Manifest roles, negative laws, high-risk probes, Senior findings, and `R27-E01..R27-E07` obligations remain in force.

---

# 1. Step-2 hard boundary

This assignment executes **WP-27 Step 2 only**.

The worker MUST NOT proceed to Step 3 in the same assignment, even though the broader WP-27 stage authorization normally permits automatic continuation after Step-1 GO.

Required terminal state:

```text
WP27_STEP2: COMPLETE or BLOCKED_WITH_EXACT_RESIDUAL
WP27_STEP3: NOT_STARTED
IMPLEMENTATION_PLANNING: NOT_STARTED
IMPLEMENTATION: NOT_STARTED
RELEASE_EXECUTION: NOT_STARTED
MIGRATION_EXECUTION: NOT_STARTED
GAMEPLAY_BOOTSTRAP: NOT_STARTED
```

If Step 2 finishes successfully, publish a durable Step-2 closure checkpoint and STOP for independent review of the evidence package.

If a genuine human-owned decision is discovered, exhaust mechanical evidence work first, publish a decision-ready blocker with exact affected item IDs/owners/alternatives, and STOP.

---

# 2. Core evidence rule — three ledgers, never one blurred summary

Step 2 must preserve three distinct evidence levels:

```text
A. SOURCE-ITEM LEDGER
   exact accepted / historical-closure / PO / Round-2 items and their current dispositions

B. READINESS / FUTURE-WORK COMPOSITION LEDGER
   lossless aggregation of source items into future implementation/proof/defer workstreams

C. MACHINE -> OWNER REVERSE-CONFORMANCE LEDGER
   material current GAME/DEV responsibilities mapped back to accepted owners or explicit non-owner classes
```

These ledgers may live in one or several files, but their identities and cross-references must remain explicit.

A future workstream record may aggregate many source items **only if** every source item has an explicit `source_item_id -> readiness_id[]` mapping and no qualifier, trigger, negative law, proof class, activation state or already-realized status is lost.

A machine family may be grouped **only if** the grouped members are materially homogeneous for owner/disposition purposes. `mixed`, `partial`, `legacy`, `stale`, or semantically heterogeneous families require an exception/material-responsibility breakdown sufficient to prove reverse conformance.

Counts alone are never coverage evidence.

Examples of invalid closure shortcuts:

```text
"WP-03 covered"
"82 IDs present"
"459 files scanned"
"GAME/SCHEMA mostly owner-routed"
"all PO entries incorporated"
```

without the required item-level / exception-level traceability.

---

# 3. Required stable identifiers

Use stable audit identifiers so an independent reviewer can mechanically trace coverage.

Recommended namespaces:

```text
WP01-... through WP26-...      closed-domain / owner-chain source items
PO001-... through PO010-...    Product Owner carry-forward items where separate identity is useful
D01..D24                      Round-2 DIAMOND items — retain original IDs
S01..S58                      Round-2 STRONG items — retain original IDs
R27-R###                      readiness/composite future-work records
R27-M###                      machine/reverse-conformance records or homogeneous groups
R27-X###                      explicit exceptions inside grouped machine families
```

Exact spelling is documentation-level, but IDs must be unique, stable inside Step 2, and cross-referenced bidirectionally.

Do not replace original D/S IDs with new aliases.

---

# 4. Required source-item record shape

For every **material enumerated obligation/findings item** that contributes to readiness, record enough fields to recover:

```text
source_item_id
source_owner_or_provenance_ref
source_role: CANONICAL | AMENDMENT | PO_INTENT | CLOSURE_PROVENANCE | MACHINE_EVIDENCE | TEST_EVIDENCE
actual_surviving_claim_or_boundary
qualifiers_and_applicability
later_owner_or_supersession_ref
current_disposition
activation_state
implementation_consequence
verification_or_scenario_consequence
empirical_or_release_consequence
defer_or_revisit_trigger
negative_or_rejected_constraint
current_machine_realization_state
readiness_ids[]
notes_on_conflict_extension_or_no_delta
```

Not every field needs prose when `N/A`, but the semantic distinction must remain explicit.

Current owner beats historical closure wording. Historical evidence may explain the route but does not regain authority merely because it contains more detail.

---

# 5. Step-2 execution slices

The worker executes the following slices **in order**. Each slice ends with a durable checkpoint/update before the next slice begins. A long-running worker may commit after each coherent slice. Do not wait until the end to preserve several hours of evidence work.

## S2-A — control plane and inventory initialization

Goal: establish the evidence container and exact completion counters before substantive extraction.

Required:

1. fresh bootstrap from current repository owners/process;
2. load WP-27 Task Brief, Senior repair amendment, this execution amendment, current WP-27 mini-report and current R2.7 cursor;
3. create/update the Step-2 durable evidence ledger/checkpoint;
4. record the source families from the Task Brief, including the Senior additions:

```text
GAME/TEMPLATE/*
GAME/ENGINE_VERSION.yaml
DEV/ENGINE_DEVELOPMENT.yaml
```

5. initialize completion counters for:

```text
WP01_07
WP08_26
PO001_010
ROUND2_D_S_82
ARCH_TO_READINESS
MACHINE_TO_OWNER
VERSION_MIGRATION
PROOF_CHANNELS
DEFER_DORMANT_REJECTED
HIGH_RISK_PROBES
```

Exit criterion: evidence structure exists; no domain is falsely marked complete merely because files were located.

STOP/commit checkpoint for this slice before continuing.

---

## S2-B — WP-01..WP-07 bounded owner-chain recovery

These domains are intentionally asymmetric with later WPs. Absence of a one-file-per-WP canonical specification is **not** a gap and must not trigger corpus-wide archaeology.

Required route:

```text
closed WP domain provenance / mini-report / closure evidence
-> current semantic/model/spec owner(s)
-> later accepted amendments / supersession
-> surviving enumerated implementation / proof / defer / negative items
-> implicated current machine/test consumers
```

Rules:

- WP-01..WP-06 predate the later canonical-WP file pattern.
- WP-07 routes through its closure/mini-report plus current Step-4/Step-5 information owners and later consumers.
- Read historical design/research/critic artifacts only where needed to recover a concrete enumerated item, qualifier, applicability condition, supersession or consumer boundary not recoverable from current owner + closure evidence.
- Do not manufacture retroactive WP-01..07 canonical specs for symmetry.
- Do not use filename/date recency as authority.
- Do not introduce a private/external research source as a public current owner. Private research may contribute only through an accepted/sanitized public owner or as non-normative evidence where the public process explicitly admits that role.

For every material surviving item create a source-item record and map it to zero or more readiness records only after the current disposition is established.

Specific audit guard:

```text
if a closed-domain repair is already realized in current machine/docs/tests,
classify that repair ALREADY_REALIZED rather than recreating future implementation debt.
```

Exit criterion:

```text
WP01_07_SOURCE_ITEMS: individually accounted
WP01_07_RESIDUAL_OWNER_GAPS: 0
or exact blocker IDs listed
WP01_07_FILENAME_SYMMETRY_GAP: never used as a reason for reopen
```

STOP/commit checkpoint for this slice before continuing.

---

## S2-C — WP-08..WP-26 canonical-owner extraction

For WP-08..WP-26, start from each current canonical WP owner plus required amendments/final closure evidence. Do **not** reduce one WP to one summary row when the owner contains multiple material implementation-facing laws or realization boundaries.

For each WP extract all surviving material items affecting any of:

```text
implementation destination
persistent/runtime representation boundary
identity/root/index/currentness
cross-component interface
version/migration consequence
TDD/deterministic verification
scenario acceptance
empirical/real-target acceptance
release-time acceptance
defer/revisit trigger
negative/rejected architecture
already-realized machine repair
```

The extraction may group several adjacent owner laws into one source-item record only when they have the same current owner, activation/disposition, destination, proof class and negative/defer semantics. Otherwise keep them separate.

Mandatory anti-regression checks:

### WP-20

Preserve the distinction between:

- accepted compatibility/migration laws;
- future realization obligations such as exact migration-edge/compatibility declaration machine shape, transform execution boundary, evaluator/path resolver, validators/fixtures/tests;
- activation only when a qualifying released-v1.0+ source/target obligation exists;
- implementation-neutral representation choices explicitly delegated by the owner.

Do not collapse the whole WP into a generic `migration deferred` row.

### WP-22 / WP-23

Preserve proof-channel separation. Current CI/test existence does not discharge later scenario, Protocol-4, empirical or release-time acceptance.

### WP-24 / WP-25

Preserve activation/defer/rejected distinctions. Do not manufacture universal optimization, health, ACL, retry, autosave or partition subsystems.

### WP-26

WP-26 already performed concrete routing/supersession/current-machine repairs and five Category-B CORE revisions. Those completed repairs are **ALREADY_REALIZED**, not a future WP-26 implementation workstream.

Downstream unrealized Story/runtime/schema/writer obligations remain owned by their native semantic owners / PO-009 / PO-010 / applicable WPs. Do not use WP-26 as a catch-all future implementation owner.

Exit criterion:

```text
WP08_26: every material surviving owner item mapped
CLOSED_REPAIRS_REINTRODUCED_AS_WORK: 0
UNRESOLVED_OWNER_GAPS: 0 or exact blocker IDs listed
```

STOP/commit checkpoint for this slice before continuing.

---

## S2-D — PO-001..PO-010 carry-forward reconciliation

The PO ledger is authoritative for preserved Product Owner intent/routing, not semantic architecture by itself. Current accepted owner decisions/specifications control architectural semantics.

For each PO entry record:

```text
PO id
current incorporated owner(s)
material surviving requirement(s) relevant to implementation planning
source_item_ids[]
future implementation consumers[]
proof consumers[]
activation/defer state
remaining representation risk
architecture-blocker test result
readiness_ids[]
```

`INCORPORATED` means semantics have an accepted route; it does **not** mean runtime/test/release realization is complete.

Do not create an open PO decision unless the current accepted owners actually leave a material human-owned choice unresolved after evidence work.

Mandatory seams:

```text
PO-003 + PO-009: historical T0 / Story-local baseline Commentator sufficiency / zero-extra-serial law
PO-008 + WP-25: native failure/degradation/durability-risk realization without rejected global abstractions
PO-010 + WP-24/Story: bounded writer path versus evidence-driven concrete topology
```

Exit criterion: all PO-001..010 individually cross-referenced to source items/readiness/proof with no orphan route.

STOP/commit checkpoint for this slice before continuing.

---

## S2-E — mandatory 82-item DIAMOND/STRONG reconciliation

This slice is independent and mandatory. It cannot be satisfied by listing IDs in disposition buckets.

Authoritative completeness source:

- `DEV/docs/superpowers/design/2026-08-24-round-2-evidence-disposition-ledger.md`;
- plus later accepted owner changes, specifically including S14, S53 and D15 and any other later supersession discovered through their owner routes.

Create **82 item-level records** retaining the original IDs:

```text
D01..D24
S01..S58
```

For each item record at least:

```text
item_id
original_disposition
original_claim / qualifier
current_owner / later_supersession
current_disposition
activation_state
implementation_consequence
verification/scenario/empirical consequence
defer/revisit trigger
negative constraint
current machine realization state
readiness_ids[]
```

A bucket list such as `CURRENT ACTIVE: D01 D02 ...` is useful as a derived summary but never substitutes for these records.

Mechanical closure checks:

```text
EXPECTED: 82
PRESENT: 82
MISSING: []
DUPLICATES: []
UNKNOWN_IDS: []
S14_CURRENT_DELTA: explicitly reconciled
S53_CURRENT_DELTA: explicitly reconciled
D15_CURRENT_DELTA: explicitly reconciled
UNMAPPED_TO_READINESS_OR_EXPLICIT_NO_WORK: []
```

Dormant coverage does not activate work. Rejected items do not become debt.

Exit criterion: the complete per-item ledger exists and the mechanical accounting above is clean.

STOP/commit checkpoint for this slice before continuing.

---

## S2-F — architecture/source-items -> readiness composition

Only after S2-B through S2-E are complete may the worker construct/normalize composite readiness records.

Each readiness record must retain fields equivalent to the Task Brief readiness model, including owner refs, destination, predecessors, shape boundary, version/migration consequence, proof classes, activation, remaining implementation choices, blocker result, defer trigger and negative laws.

Lossless aggregation law:

```text
for every material source_item_id:
    readiness_ids[] is non-empty
    OR disposition explicitly proves:
        ALREADY_REALIZED
        NO REPRESENTATION / NO CURRENT WORK
        SAFE_DEFERRED_TRIGGER
        MEASUREMENT_DORMANT
        RELEASE_TIME_FORWARD only
        OUT_OF_SCOPE_OR_REJECTED
```

A readiness record that aggregates multiple source items must not erase distinct triggers/proof classes/negative constraints. Split the record if necessary.

The number of readiness records is not a goal. Fewer records are preferred only when traceability remains lossless.

Exit criterion:

```text
SOURCE_ITEMS_WITHOUT_TERMINAL_ROUTE: []
READINESS_RECORDS_WITHOUT_OWNER: []
AGGREGATION_QUALIFIER_LOSS: 0
```

STOP/commit checkpoint for this slice before continuing.

---

## S2-G — current machine -> architecture reverse conformance

This slice proves `R27-M01/R27-M02`; it is not a file-count exercise.

Mandatory discovery families remain at least:

```text
GAME/CORE/*.md
GAME/SCHEMA/*
GAME/CAMPAIGN/*
GAME/TEMPLATE/*
GAME/INSTALL/*
GAME/RULES/*
GAME/MIGRATIONS/*
GAME/TOOLS/*
GAME/ENGINE_VERSION.yaml

DEV/ARCHITECTURE/*
DEV/CATALOG/*
DEV/SCHEMAS/*
DEV/TESTS/*
DEV/TOOLS/*
DEV/RELEASE/*
DEV/ENGINE_DEVELOPMENT.yaml
.github/workflows/*
```

Top-level legal/publication surfaces are included when their release/legal owner route is implicated.

For every **material current machine/runtime responsibility**, assign:

```text
accepted owner
or explicit class:
  ALREADY_REALIZED_SUPPORT
  DERIVED_SUPPORT
  IMPLEMENTATION_ONLY
  VERIFICATION_ONLY
  HISTORICAL
  STALE
  DEBT
  INTENTIONALLY_DEFERRED
  OUT_OF_SCOPE
```

Grouping rule:

- homogeneous group: allowed if common responsibility + common owner/disposition can be demonstrated;
- heterogeneous/mixed/legacy/partial/stale family: create explicit material exceptions/subgroups until every material responsibility has an unambiguous classification;
- artifact presence never proves behavior or semantic authority;
- test presence never proves execution;
- catalog/schema presence never proves shipped GAME realization;
- path/index/template presence never creates identity/currentness authority.

Required accounting should expose both:

```text
tracked/discovered artifact count by family
AND
material responsibility / exception coverage count
```

`R27-M02 COMPLETE` is forbidden while any material group is described only as `mostly`, `many`, `mixed`, `generally`, or equivalent without the necessary exception ledger.

Exit criterion:

```text
MATERIAL_MACHINE_RESPONSIBILITIES_WITHOUT_OWNER_OR_CLASS: []
MIXED_GROUPS_WITHOUT_EXCEPTION_BREAKDOWN: []
MACHINE_SURFACE_FALSE_AUTHORITY_PROMOTIONS: 0
```

STOP/commit checkpoint for this slice before continuing.

---

## S2-H — cross-cutting readiness dimensions

Reconcile the now-complete source/readiness/machine evidence across:

### dependency DAG

Derive prerequisites; do not invent one universal sequence where owner-local work can proceed independently.

### Version Impact / migration

For each material readiness record classify whether later implementation must run a Version Impact Gate for affected namespaces. Do not predeclare a bump/migration merely because a future implementation may touch a versioned surface.

### proof channels

Keep distinct:

```text
current source CI / maintenance audit
TDD deterministic unit/contract/integration proof
scenario/adversarial acceptance
Protocol-4 / supported-target empirical acceptance
release-time fresh-Project / exact-asset acceptance
```

### deferred / dormant / rejected

Retain exact activation/revisit triggers and negative laws. Coverage is not activation.

### high-risk probes

Re-run at least the Task Brief probes:

```text
R27-P01 PO-003 + PO-009 Story-local T0/control
R27-P02 WP-25 deferred-vs-rejected
R27-P03 PO-010/WP-24 bounded writer/partition activation
R27-P04 WP-20 migration/version dependency order
R27-P05 proof-channel separation
R27-P06 release-time gates
R27-P07 dormant scale/host triggers
R27-P08 reverse conformance
```

A probe result must cite the exact source-item/readiness/machine records it relies on.

Exit criterion: no cross-cutting claim depends only on thematic summary or family count.

STOP/commit checkpoint for this slice before continuing.

---

## S2-I — Step-2 internal completeness audit

This is an **evidence-admission gate inside Step 2**, not the later Step-6 adversarial architecture review.

Before any `STEP2_COMPLETE` claim, mechanically and semantically check:

```text
WP01_07 source items complete
WP08_26 source items complete
PO001_010 individually routed
82/82 D/S records present exactly once
all S14/S53/D15 changes reconciled
all material source items have readiness/no-work terminal route
all readiness records have accepted owner(s)
all material machine responsibilities have owner/class
all mixed machine groups have exception breakdown
all version/migration consequences classified
all proof channels classified without over-credit
all defer/dormant/rejected triggers preserved
all high-risk probes completed
no closed already-realized repair reintroduced as future work
no private/external evidence promoted to public owner without accepted public route
no unresolved architecture-blocker candidate hidden as implementation detail
```

The Step-2 package must publish explicit counts and lists, not only `PASS` labels.

If any line fails, keep Step 2 ACTIVE, repair the evidence, and rerun this gate.

---

## S2-J — durable Step-2 closure checkpoint

Only after S2-I passes may Step 2 be marked complete.

Required closure report:

```text
STEP2_FINAL_HEAD:
SOURCE_ITEM_COUNT:
WP01_07_ITEM_COUNT:
WP08_26_ITEM_COUNT:
PO001_010: 10/10
ROUND2_82: 82/82
ROUND2_MISSING: []
ROUND2_DUPLICATES: []
READINESS_RECORD_COUNT:
SOURCE_ITEMS_WITHOUT_TERMINAL_ROUTE: []
MACHINE_GROUP_OR_RECORD_COUNT:
MACHINE_EXCEPTIONS_COUNT:
MACHINE_UNOWNED_OR_UNCLASSIFIED: []
MIXED_GROUPS_WITHOUT_BREAKDOWN: []
HIGH_RISK_PROBES: 8/8
ARCHITECTURE_BLOCKER_CANDIDATES:
UNRESOLVED_BLOCKING:
UNRESOLVED_SIGNIFICANT:
HUMAN_DECISION_REQUIRED:
PRODUCT_OWNER_DECISION_REQUIRED:
VERSION_IMPACT_OF_STEP2_DOCUMENTATION:
VERIFICATION_EVIDENCE:
WP27_STEP2: COMPLETE
WP27_STEP3: NOT_STARTED
```

Update the WP-27 mini-report and applicable durable cursors to the actual Step-2 closure/review state. Obtain the verification/read-back required by the active runtime policy.

Then STOP.

---

# 6. Anti-patterns that invalidate Step-2 closure

Any of the following is a review failure unless repaired:

1. **Filename symmetry archaeology** — creating or searching for retroactive WP-01..07 canonical files instead of following their actual owner chains.
2. **One-row-per-WP compression** — using a WP summary row where enumerated surviving obligations have different destinations/triggers/proof/negative semantics.
3. **82-ID bucket accounting** — listing all D/S IDs in groups without per-item current owner/disposition/consequence records.
4. **Raw file-count reverse audit** — counting machine files and calling the reverse ledger complete without material responsibility classifications.
5. **`mostly/mixed/many` closure language** — unresolved heterogeneous machine groups without explicit exceptions.
6. **Closed repair resurrection** — converting already-completed WP repairs into future implementation obligations.
7. **Deferred noun activation** — treating every noun mentioned in a historical/deferred section as current implementation debt.
8. **Rejected abstraction resurrection** — global health/ACL/retry/migration/readiness/partition services reappearing for convenience.
9. **Current proof over-credit** — green CI or test-file existence treated as future scenario/empirical/release acceptance.
10. **Private/external authority promotion** — deriving public normative work directly from private/external evidence without an accepted public owner/decision.
11. **Aggregation without reverse traceability** — readiness records cannot be traced back to all source items they replace.
12. **Step creep** — beginning Step 3, implementation planning, implementation, release, migration or gameplay in this assignment.

---

# 7. Independent-review design goal

The Step-2 package must be reviewable by a different Senior without rereading the entire corpus.

A Senior must be able to select any:

```text
WP source item
PO requirement
D/S item
readiness record
machine responsibility
```

and follow explicit references in both directions:

```text
owner/provenance -> current disposition -> readiness/proof/defer
readiness -> source items + machine consumers
machine responsibility -> accepted owner/disposition -> readiness impact
```

The package is not required to reproduce entire owner texts. It is required to preserve enough exact references and qualifiers that spot-checks against owning sources can validate the synthesis.

This independent-review property is a Step-2 acceptance requirement, not optional presentation polish.

---

# 8. Final execution instruction

Use the narrowest owner/dependency route that can establish each record correctly. Do not bulk-read the entire design/research corpus merely because WP-27 is a whole-project audit.

At the same time, do not use bounded routing as an excuse for representative sampling. Once an enumerated source set or material machine group is admitted into Step 2, exhaust that set to the level required by its coverage claim.

The intended balance is:

```text
NO corpus-wide blind scan
+ NO thematic sampling shortcut
+ owner-first targeted extraction
+ exhaustive accounting inside each admitted enumerated/material set
+ durable checkpoint after every coherent slice
```

Step 2 succeeds only when the implementation-planning handoff can be independently audited without hidden architecture decisions or missing material obligations.