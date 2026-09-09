# R2.7 WP-27 Step 1 — Mandatory Wide-Angle Critic

Status: **CRITIC COMPLETE / REPAIR REQUIRED BEFORE STEP-1 SENIOR GATE**

Date: 2026-09-09

Reviewed Step-1 framing artifact:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-task-brief-source-manifest.md`.

This critic is intentionally independent in attack shape. It does not ask whether the Task Brief repeats the project process correctly; it asks whether an implementation-planning-readiness audit following that brief could still produce a materially wrong handoff.

No implementation planning, implementation, migration/release execution or gameplay bootstrap is authorized by this review.

---

# 1. Verdict before repair

```text
STEP1_BLOCKING_FOUND: 0
STEP1_SIGNIFICANT_FOUND: 11
STEP1_MINOR_FOUND: 1
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
STEP1_SENIOR_READY: NO — REPAIRS REQUIRED
```

No finding proves a current semantic architecture defect. The findings are framing/coverage hazards that could cause WP-27 to derive the wrong implementation boundary or omit a required future obligation.

---

# 2. Independent reconstruction of the readiness problem

A correct WP-27 handoff must preserve four distinct layers:

```text
ACCEPTED OWNER LAW
    what must remain true

REALIZATION STATE
    what current machine/runtime/schema/tooling already does or does not do

FUTURE WORK / PROOF CLASS
    implementation obligation vs implementation choice vs deterministic test
    vs scenario/empirical/release-time obligation vs dormant/deferred trigger

ENTRY DECISION
    whether any unresolved issue still requires architecture/PO decision before planning
```

The dangerous failure mode is collapse between these layers. Examples:

- “architecture accepted” -> falsely reported as implemented;
- “deferred” -> every named concept becomes required work;
- “future benchmark” -> optimization is activated now;
- “green CI” -> future MVP acceptance is falsely considered complete;
- “implementation choice” -> architecture is reopened without need;
- “persisted representation unspecified” -> a material interface decision is hidden inside planning.

The Step-1 package must prevent all six.

---

# 3. Findings

## F27-S1-01 — Closed-domain coverage can collapse into canonical-spec-only sampling

Severity: **SIGNIFICANT**

### Problem

WP-27 spans WP-01..WP-26, but the repository does not use one uniform artifact pattern across those domains. Early domains rely on design/research/Senior closure plus current architecture/model/machine owners; later domains increasingly expose one canonical WP specification.

A planner that reads only canonical specs would miss item-level implementation, verification, negative and forward obligations retained in:

- final Senior recovery artifacts;
- machine-realization evidence;
- Product Owner routing;
- current GAME/DEV consumers;
- accepted amendments and supersession repairs.

### Required repair

The Task Brief must explicitly require an item-level closed-domain extraction ledger for **every WP-01..WP-26**, while permitting source-family routing rather than pretending each WP has one canonical filename.

### Disposition

**REPAIRED IN TASK BRIEF** by sections 6.6–6.9 and `R27-E01`, which require domain-family extraction and preserve item semantics.

---

## F27-S1-02 — Current PO routing is stale at the WP-26 -> WP-27 transition

Severity: **SIGNIFICANT**

### Problem

The current `DEV/PRODUCT_OWNER_INPUT.md` agent-owned routing still contains transition-era wording such as:

- PO-009: final WP-26 Senior review remains the external closure gate;
- PO-010: final WP-26 Senior review remains the closure gate;
- PO-010: WP-27 readiness is deferred until WP-26 closure and explicit authorization;
- terminal routing state does not yet record WP-26 closed / WP-27 Step-1 active.

Those statements were accurate before the now-published WP-26 closure and current WP-27 authorization. They are stale now.

A readiness audit beginning from this ledger could incorrectly treat a satisfied gate as still pending or fail to recognize the active PO-009/010 readiness handoff.

### Required repair

Update **agent-owned routing/status only**. Product Owner verbatim blocks remain immutable.

Required current projection:

```text
WP26_FINAL_SENIOR_REVIEW: PASS / GO
WP26_CLOSED: YES
WP27_STEP1_AUTHORIZED: YES
WP27_STEP1_ACTIVE: YES
IMPLEMENTATION_PLANNING_STARTED: NO
```

PO-009/010 future realization remains deferred; only the readiness classification route is active.

### Disposition

**OPEN MECHANICAL REPAIR** at critic publication.

---

## F27-S1-03 — WP-25 deferred list can resurrect explicitly rejected global subsystems

Severity: **SIGNIFICANT**

### Problem

WP-25 contains a “Remaining deferred obligations” block that names both legitimate future realization candidates and concepts rejected by the canonical architecture, including global health state / generic ACL or operation registry / universal retry engine and a possible persisted failure schema/registry.

The same canonical owner elsewhere explicitly states:

```text
PERSISTED_GLOBAL_ERROR_AUTHORITY: NO
GLOBAL_HEALTH_STATE: NO
UNIVERSAL_RETRY_ENGINE: NO
GENERIC_WP25_ACL: NO
```

A mechanical “collect every deferred noun” pass would create implementation debt for rejected architecture.

### Required repair

WP-27 must classify WP-25 item-wise:

- focus-scoped evaluator/adapters and owner-local integration/proof -> candidate implementation/verification work where owner-required;
- exact common machine spelling -> implementation choice only if a consumer requires a common representation;
- persisted global failure registry -> **not required by current architecture**;
- global health/ACL/retry -> **OUT_OF_SCOPE_OR_REJECTED**;
- host-risk thresholds/calibration -> realization/real-target empirical obligation only when applicable;
- installed maintenance realization -> implementation obligation only if its existing maintenance owner still requires it.

### Disposition

**REPAIRED IN TASK BRIEF** by `R27-P02`, `R27-E06` and the unknown-classification rules.

---

## F27-S1-04 — PO-003 + PO-009 contains a genuine representation-risk seam that cannot be predeclared “implementation detail”

Severity: **SIGNIFICANT**

### Problem

Accepted semantics require all of the following simultaneously:

- native SemanticEvent/history retains historical ownership;
- bounded event-time T0 decision-basis meaning is Story-local recoverable for baseline Commentator;
- Commentator eligibility/control is self-contained after import and source-bound to current knowledge/disclosure/access owners;
- secrets/private/off-screen material remains retained but protected;
- baseline Commentator cannot require native-only fallback solely to recover required T0/control;
- Commentator-local SQLite is downstream/internal and not Master HOT;
- PO-003 zero-extra-serial latency law remains mandatory.

The exact HDM-side persisted/export shape is intentionally not yet selected. Depending on the representation, it could alter persistent semantic schema, versioning, producer/consumer interfaces or publication/currentness behavior.

Therefore WP-27 cannot assume in advance that all remaining PO-009 shape choices are implementation details.

### Required repair

Carry an explicit blocker probe:

```text
if current Story/source/control owners fully determine semantic fields,
identity/currentness/provenance and producer/consumer contract,
and only encoding/layout remains:
    IMPLEMENTATION_DETAIL / IMPLEMENTATION_OBLIGATION
else if unresolved choice changes persistent semantic contract/interface/version law:
    ARCHITECTURE_BLOCKER_CANDIDATE
```

### Disposition

**REPAIRED IN TASK BRIEF** by architecture-blocker test + `R27-P01`.

---

## F27-S1-05 — PO-003/009 could accidentally create duplicate history or access owners or add serial LLM latency

Severity: **SIGNIFICANT**

### Problem

A naive implementation decomposition may create independent workstreams for:

- “native T0 store”;
- “Story T0 store”;
- “Commentator ACL snapshot”;
- “Commentator lookup”; 

and accidentally grant those derived copies independent authority or add an extra mandatory per-event/per-turn LLM/tool round trip.

That would contradict existing ownership and the explicit interactivity constraint.

### Required repair

The readiness graph must bind these as one composed consumer path with negative constraints:

```text
native SemanticEvent/history owner remains singular
Story retains/projection-copies bounded required meaning with source/provenance binding
control projection remains derived from native access/knowledge/disclosure owners
Commentator cache remains non-authoritative downstream read model
no extra mandatory serial LLM stage merely to persist the already-selected bounded basis
```

### Disposition

**REPAIRED IN TASK BRIEF** by `R27-P01` and the owner-derived graph model.

---

## F27-S1-06 — PO-010/WP-24 can be misread as immediate universal partition implementation

Severity: **SIGNIFICANT**

### Problem

Current law requires safe bounded partitionability for plausibly unbounded growth-bearing collections and defines sizing review bands, but explicitly does **not** select one universal shard/page/rollover geometry and states that coverage is not activation.

A plan that creates a “partition everything >16 KiB” project would over-activate the architecture and may destroy atomicity/identity/provenance for indivisible owner units.

### Required repair

WP-27 must separate:

- hard owner requirement to have a safe bounded path where a growth-bearing representation is admitted;
- writer-specific implementation needed for currently implemented growth-bearing writers;
- concrete geometry delegated to implementation where semantic reconstruction/currentness/identity are already fixed;
- measurement-dormant optimizations and future trigger-driven repartitioning.

### Disposition

**REPAIRED IN TASK BRIEF** by sections 4.1, 8 `R27-P03`, and the blocker test.

---

## F27-S1-07 — Delegated representation choices may be mistaken for architecture gaps

Severity: **SIGNIFICANT**

### Problem

Several owners intentionally delegate exact physical/serialization choices:

- WP-20 defers exact migration-edge serialization, transform artifact/module format and evaluator implementation;
- WP-24 defers concrete Story/index partition geometry and exact universal rollover threshold.

Those omissions are not automatically architecture blockers. Reopening closed architecture for every implementation representation would make WP-27 non-terminating and violate the closed-topic rule.

### Required repair

The blocker test must distinguish semantic/interface insufficiency from delegated representation choice.

### Disposition

**REPAIRED IN TASK BRIEF** by section 5 and `R27-P04`.

---

## F27-S1-08 — Green current CI can be falsely promoted to future MVP verification completeness

Severity: **SIGNIFICANT**

### Problem

Current exact-head maintenance audit/unit tests are strong evidence about current realized checks only. WP-22 explicitly says they do not establish:

- future semantic-owner universe completeness by themselves;
- scenario execution;
- Protocol-4 execution;
- empirical product quality;
- deferred future proof work.

A readiness plan could otherwise mark future verification “done” because current CI is green.

### Required repair

The readiness graph must carry separate proof channels:

```text
current already-realized deterministic proof
future deterministic TDD obligation
scenario acceptance obligation
real-target empirical obligation
release-time acceptance obligation
```

Protocol 4 remains post-implementation on the real MVP.

### Disposition

**REPAIRED IN TASK BRIEF** by `R27-P05`, `R27-E01` and the classification vocabulary.

---

## F27-S1-09 — WP-23 release-time acceptance can be pulled prematurely into implementation work

Severity: **SIGNIFICANT**

### Problem

WP-23 requires a strict future release sequence including pre-tag fresh-Project acceptance, immutable tag/publication, exact uploaded-asset verification, post-upload fresh-Project acceptance and release announcement gate.

These are release-time forward obligations. They cannot be executed in WP-27 and should not be modeled as ordinary implementation tasks that block coding completion prematurely.

### Required repair

Carry them as `RELEASE_TIME_FORWARD_OBLIGATION` with predecessor relationships to a version-coherent implemented candidate and actual release authorization.

### Disposition

**REPAIRED IN TASK BRIEF** by `R27-P06` and classification rules.

---

## F27-S1-10 — Dependency/version/migration ordering can become a fake global sequence or miss per-workstream Version Impact

Severity: **SIGNIFICANT**

### Problem

Some implementation families are independent while others have strict predecessor relations. A single project-wide linear order is unnecessary; no order is unsafe.

Particularly dangerous is planning migration machinery before the target persistent schemas/interfaces and compatibility declarations are known, or predeclaring version bumps before an implementation shape is selected.

### Required repair

WP-27 must derive a dependency DAG, not one universal sequence, and attach Version Impact routing per workstream:

```text
semantic/persistent contract
-> implementation shape where needed
-> local schema/generation/version classification
-> migration/compatibility support if required
-> producer/consumer/runtime integration
-> deterministic tests
-> empirical/release-time gates later
```

Independent workstreams may proceed in parallel after dependencies are satisfied.

### Disposition

**REPAIRED IN TASK BRIEF** by `R27-E04` and `R27-E05`.

---

## F27-S1-11 — WP-27 can be mistaken for direct implementation-planning authorization

Severity: **SIGNIFICANT**

### Problem

WP-27 is the last numbered audit domain, but the R2.7 process requires a distinct final reconciliation after WP-27 closure. Therefore a WP-27 PASS cannot itself flip the program into implementation planning.

### Required repair

The Step-1 brief and final WP-27 canonical result must preserve:

```text
WP27 CLOSED
-> R2.7 FINAL RECONCILIATION
-> implementation-planning entry resolution
-> implementation planning only after explicit resulting gate/authorization
```

### Disposition

**REPAIRED IN TASK BRIEF** by sections 0–1 and exit criteria.

---

## F27-S1-M01 — Root README known builder-path mismatch remains manual-editorial only

Severity: **MINOR**

### Problem

The known root README path mismatch remains discoverable. WP-27's broad readiness scope could tempt opportunistic cleanup.

### Required repair

Carry as report-only unless the Product Owner separately authorizes README editing. It is not a WP-27 architecture blocker.

### Disposition

**REPAIRED IN TASK BRIEF** explicit non-goals.

---

# 4. Additional negative findings

The critic specifically looked for the following and found no current Step-1 framing requirement for them:

```text
NEW GLOBAL IMPLEMENTATION-READINESS REGISTRY: NOT REQUIRED
NEW GLOBAL DEPENDENCY GRAPH RUNTIME SERVICE: NOT REQUIRED
NEW MIGRATION GRAPH DATABASE/SERVICE: NOT REQUIRED
NEW STORY AUTHORITY: NOT REQUIRED
NEW COMMENTATOR ACL AUTHORITY: NOT REQUIRED
NEW GLOBAL FAILURE/HEALTH/RETRY OWNER: REJECTED
NEW UNIVERSAL PARTITION TOPOLOGY: NOT REQUIRED
NEW RELEASE AUTHORITY: NOT REQUIRED
WHOLESALE REOPEN OF WP-01..WP-26: NOT REQUIRED
```

The implementation graph is a DEV audit/planning derivation artifact only.

---

# 5. Required repairs before Senior review

At critic publication, only one significant finding still requires repository mutation beyond the already-repaired Task Brief:

```text
F27-S1-02 — synchronize agent-owned PO-009/PO-010 routing and terminal ledger state
```

After that repair, perform a fresh read of:

- `DEV/PRODUCT_OWNER_INPUT.md`;
- `DEV/CURRENT_PROGRESS.md`;
- the WP-27 Task Brief;
- this critic;

and update this critic's final accounting to prove all significant findings are closed.

Do not alter immutable Product Owner text.

---

# 6. Current accounting at critic publication

```text
STEP1_BLOCKING_FOUND: 0
STEP1_SIGNIFICANT_FOUND: 11
STEP1_MINOR_FOUND: 1

SIGNIFICANT_REPAIRED_IN_TASK_BRIEF: 10 / 11
SIGNIFICANT_OPEN_MECHANICAL_REPAIR: 1 / 11
MINOR_REPAIRED_IN_TASK_BRIEF: 1 / 1

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 1
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO

WP27_STEP2_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
STEP1_SENIOR_READY: NO
```

The next action is the bounded PO-routing repair, followed by critic closure/readback and then the mandatory independent Step-1 Senior gate.
