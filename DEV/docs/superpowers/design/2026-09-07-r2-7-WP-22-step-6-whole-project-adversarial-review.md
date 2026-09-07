# R2.7 WP-22 Step 6 — Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — 2 SIGNIFICANT FINDINGS / 1 MINOR FINDING — STEP 7 REPAIR REQUIRED**

Date: 2026-09-07

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-step-5-candidate-specification.md`

Required reconstruction route:

```text
DEV/PROJECT_MAP.md
-> current process/current-progress owners
-> accepted verification-relevant architecture/spec owners
-> later owner decisions/amendments
-> GAME runtime consumers
-> DEV schemas/catalogs/tests/tools
-> hosted CI route
-> R2.6 assurance/Protocol-4 provenance
-> WP-08..WP-21 final accepted owners and deferred boundaries
```

The critic did not treat the Step-5 candidate, its Source Manifest, test filenames, scenario files, research ledgers or `DEV/PROJECT_MAP.md` as semantic authority by themselves.

Scope remains WP-22 only. WP-23, implementation planning, substantive implementation and Protocol-4 execution remain out of scope.

---

## 1. Whole-project dependency subgraph inspected

The critic re-walked the current repository map and checked the following owner/consumer classes relevant to the candidate:

- process/current authority: `AGENTS.md`, `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/CURRENT_PROGRESS.md`, `DEV/PROJECT_MAP.md`;
- current R2.1–R2.6 accepted specs and current R2.7 WP-08..WP-21 specs/amendments/owner decisions routed by the project map;
- authority/currentness: `DEV/ARCHITECTURE/ACCESS_CONTROL.md`, PO-005 creator-login decision, PO-006 branch/ref deletion prohibition, publication-currentness repair;
- persistence/publication/recovery/bootstrap/update owners and their current runtime/schema/test surfaces;
- chronology/LIVE/collaboration/Story/Dramaturg owners and current scenario/test/deferred-machine state;
- support/diagnostics/cleanup owners and maintenance command proposal boundary;
- verification infrastructure: `DEV/TOOLS/run_maintenance_audit.py`, `DEV/TOOLS/audit_engine.py`, `DEV/TESTS/`, `.github/workflows/validate.yml`;
- R2.6 Protocol-4 canonical owner, design source and frozen fixture source.

Key source-role facts preserved:

1. `DEV/PROJECT_MAP.md` is explicitly a **non-normative navigation index**, never a semantic owner.
2. `DEV/docs/superpowers/design/*.md` normally carries design provenance/process history; exact physical placement does not promote it to semantic authority.
3. Markdown scenario/acceptance catalogs are verification/acceptance artifacts, not architecture owners merely by existence.
4. Product Owner intent/routing is not accepted architecture unless incorporated into an accepted owner decision/specification.
5. Green CI proves only the checks actually executed on the exact HEAD.

---

## 2. Findings

### SR22-06-01 — SIGNIFICANT — semantic-owner column is contaminated by non-semantic routing / acceptance artifacts

**Mechanism**

Step 2 correctly states an owner-first model, but several rows place artifacts that are explicitly non-semantic into the `Current semantic owner(s)` column.

Concrete examples:

- `VCM-01` lists `DEV/PROJECT_MAP.md` together with actual current-progress authority. The project map explicitly says it is non-normative and cannot own semantics.
- `VCM-40` includes project-map/current-release-process routing material in the semantic-owner cell even though those surfaces are process/navigation/consumer context rather than the runtime/source-boundary semantic owner.
- `VCM-41` lists the Protocol-4 design and frozen fixture beside the R2.6 canonical owner. The design/fixture are current acceptance sources, not the semantic architecture owner of the behavior they test.
- `VCM-49` refers to scenario catalogs together with product-quality owners in the semantic-owner field. Scenario catalogs may own bounded acceptance cases, but they do not become the semantic owner of GM/AI/product quality.

**Why material**

WP-22's central purpose is to prevent verification artifacts from becoming architecture authority. If the canonical matrix itself mixes `semantic owner` with `verification/acceptance owner`, later planning can mechanically derive requirements from the wrong source and recreate exactly the authority inversion WP-22 forbids.

**Probability:** HIGH if the matrix becomes downstream implementation-planning input.

**Impact:** HIGH on traceability/authority; low immediate runtime impact because no implementation is authorized yet.

**Reversibility:** HIGH now; cheap Step-7 document repair.

**Detection difficulty:** MEDIUM; the rows look plausible unless source roles are checked against `DEV/PROJECT_MAP.md` and process authority.

**Required repair**

Split the concepts explicitly:

```text
semantic owner(s)
verification / acceptance artifact(s)
supporting provenance / routing only
```

Remove non-semantic routing/provenance/scenario sources from semantic-owner positions. Protocol-4 design/frozen fixture remain current `SCENARIO_ACCEPTANCE_CURRENT` sources while the R2.6 accepted spec remains the semantic owner.

**Human decision required:** NO.

---

### SR22-06-02 — SIGNIFICANT — proof-state representation is internally ambiguous against the candidate's own primary-state law

**Mechanism**

Step 5 states:

> Every material matrix row SHALL use exactly one primary current disposition.

It permits a bounded secondary disposition only when an explicit split exists.

Step 2, however, records several rows with composite state strings such as:

```text
DEFERRED_UNTIL_REALIZATION + SCENARIO_ACCEPTANCE_CURRENT
STATIC_AUDIT_CURRENT + DEFERRED_UNTIL_REALIZATION
NOT_MACHINE_CHECKABLE / SCENARIO_ACCEPTANCE_CURRENT
EXECUTABLE_CURRENT for bounded algebra; DEFERRED_UNTIL_REALIZATION for end-to-end transport
```

The semantic intent is often correct, but the representation does not explicitly identify:

- the primary current verification disposition for the law slice;
- whether the second state applies to the same slice or a separately bounded sub-slice;
- whether a scenario is supporting acceptance design while machine proof is deferred;
- whether `NOT_MACHINE_CHECKABLE` applies only to the open-ended judgment while a separate bounded rule is scenario-checkable.

**Why material**

Without normalization, downstream consumers cannot distinguish a legitimate split realization from an accidental multi-state row. A later implementation plan could incorrectly treat `SCENARIO_ACCEPTANCE_CURRENT` as evidence that deferred runtime behavior has already been accepted, or could lose the distinction between deterministic and empirical obligations.

**Probability:** MEDIUM-HIGH downstream.

**Impact:** HIGH on verification routing/completeness claims; no immediate runtime impact.

**Reversibility:** HIGH now.

**Detection difficulty:** MEDIUM.

**Required repair**

Canonicalize the representation so every material law slice has exactly one explicit primary state, for example:

```text
PRIMARY_VERIFICATION_STATE: <one allowed value>
SUPPORTING_ACCEPTANCE_STATE: <optional allowed value>
BOUNDED_SPLIT: <named realized/deferred sub-slice when needed>
```

The precise serialization is not being designed now; the architecture requirement is that ambiguity is forbidden. Step-2 composite rows must be rewritten or explicitly split so they conform.

**Human decision required:** NO.

---

### SR22-06-03 — MINOR — hosted-route facts need explicit checkpoint-currentness semantics

**Mechanism**

The candidate correctly limits green-CI claims, and the current `.github/workflows/validate.yml` indeed runs the maintenance audit plus DEV unittest discovery. However, wording such as `Current hosted validation runs ...` can be retained too long and later read as timeless canonical workflow structure.

**Risk**

A future workflow change could leave the canonical verification model citing an obsolete execution route even though the owner/proof taxonomy remains correct.

**Required repair**

State that exact workflow commands/routes are **checkpoint evidence and must be freshly read at every completeness/closure claim**. The invariant is not that validation forever uses exactly these two commands; it is that every claimed proof names the actual current route and exact HEAD.

**Human decision required:** NO.

---

## 3. Adversarial checks with no new material finding

The critic specifically attacked the candidate for the following failure modes and found the current design direction sound once the three findings above are repaired:

- green CI as completeness oracle — rejected by WP22-11;
- stale tests as architecture authority — rejected by WP22-1/WP22-7;
- deferred architecture mistaken for implementation defect — rejected by WP22-8/WP22-9;
- Protocol-4 premature/surrogate execution — rejected by WP22-14/WP22-15;
- loss of negative/fail-closed/indeterminate laws — explicitly inventoried;
- PO-005 creator-login fail-closed semantics omitted from future proof routing — explicitly retained;
- PO-006 branch/ref deletion/probe/retry/fallback reintroduced by test cleanup — explicitly prohibited and currently guarded;
- partial-realization proof inflated to subsystem proof — rejected by WP22-10;
- release-tool tests activating WP-23 — rejected by WP22-17;
- static maintenance audit cited as runtime/behavior authority — rejected by WP22-12;
- empirical results outranking deterministic architecture — rejected by the semantic-owner-first model;
- coverage activating dormant/deferred work — rejected by WP22-2;
- ordinary novel player/GM behavior forced into closed vocabulary — rejected by WP22-6/WP22-18;
- research/provenance becoming semantic owner — rejected conceptually, but SR22-06-01 shows the Step-2 table must conform mechanically.

No accepted upstream architecture needs reopening. No Product Owner decision is exposed by this review.

---

## 4. Finding summary

```text
BLOCKING: 0
SIGNIFICANT: 2
MINOR: 1

SR22-06-01: OPEN — Step-7 repair required
SR22-06-02: OPEN — Step-7 repair required
SR22-06-03: OPEN — Step-7 repair required

HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
WP23_ACTIVATED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
PROTOCOL_4_EXECUTED: NO
```

Step 7 must repair and propagate SR22-06-01/SR22-06-02 to the Step-2 matrix, Decision Brief/review where materially affected, candidate/final canonical owner, and final status/traceability. SR22-06-03 is a bounded wording/currentness repair.
