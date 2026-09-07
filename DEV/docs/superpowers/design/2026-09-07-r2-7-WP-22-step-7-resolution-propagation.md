# R2.7 WP-22 Step 7 — Critic Resolution and Finding Propagation

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-07

Input critic:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-step-6-whole-project-adversarial-review.md`

Scope remains WP-22 only. No implementation planning, runtime implementation, Protocol-4 execution or WP-23 work is authorized by this resolution.

---

## 1. Resolution summary

```text
BLOCKING: 0 -> 0
SIGNIFICANT: 2 -> 0 unresolved
MINOR: 1 -> 0 unresolved

SR22-06-01: RESOLVED
SR22-06-02: RESOLVED
SR22-06-03: RESOLVED

HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
```

The findings exposed representation/source-role defects in WP-22 design artifacts, not a defect in accepted upstream HDM semantics. Resolution therefore conforms WP-22 to existing authority rather than changing upstream architecture.

---

## 2. SR22-06-01 — semantic-owner contamination

### Issue

The Step-2 matrix occasionally placed routing, provenance or acceptance artifacts in the `Current semantic owner(s)` column.

### Do we agree?

**YES.** `DEV/PROJECT_MAP.md` explicitly declares itself non-normative; scenario/fixture/design artifacts do not become semantic owners merely because they are current verification sources.

### Resolution

The final WP-22 contract distinguishes three roles:

```text
SEMANTIC_OWNER
VERIFICATION_OR_ACCEPTANCE_ARTIFACT
SUPPORTING_PROVENANCE_OR_ROUTING
```

Only accepted semantic owners may occupy `SEMANTIC_OWNER`:

- accepted architecture/model/runtime owner;
- accepted canonical specification/amendment/owner decision;
- machine schema/catalog/contract only where the accepted owner delegates exact machine authority to it.

The following are never promoted into semantic ownership merely by presence:

- `DEV/PROJECT_MAP.md` or another derivative locator;
- raw `DEV/PRODUCT_OWNER_INPUT.md` routing/intent entries that have not been incorporated into accepted architecture;
- design/research provenance;
- tests;
- CI workflows;
- scenario catalogs;
- Protocol-4 design/frozen fixtures;
- historical/TODO evidence.

### Corrected Step-2 row interpretation

- **VCM-01** — semantic owner: `DEV/CURRENT_PROGRESS.md` plus the accepted current-progress authority amendment/process law. `DEV/PROJECT_MAP.md` is routing support only.
- **VCM-40** — semantic owner: accepted game/dev boundary and runtime-package provenance owners. `DEV/PROJECT_MAP.md` and release process are navigation/consumer/process context, not semantic runtime-boundary owners.
- **VCM-41** — semantic owner: R2.6 accepted assurance/architecture owner. Protocol-4 design and frozen fixture are `SCENARIO_ACCEPTANCE_CURRENT` verification/acceptance artifacts.
- **VCM-49** — semantic owner: accepted GM/AI/product-quality owners. Scenario catalogs are bounded acceptance support only.

Any equivalent source-role shorthand elsewhere in Step 2 is interpreted under this same correction.

### Architectural consequences

None upstream. The owner-first architecture is strengthened and made mechanically unambiguous.

### Human decision required?

**NO.**

---

## 3. SR22-06-02 — ambiguous composite proof states

### Issue

Step 5 required exactly one primary verification disposition per material law slice, but Step 2 used composite strings (`+`, `/`, or prose combinations) in several aggregated rows.

### Do we agree?

**YES.** The intended semantics were usually correct, but the representation could allow a future consumer to confuse current scenario design, current bounded executable proof and future deferred execution.

### Resolution

For every material law slice, final WP-22 mapping SHALL keep these fields distinct:

```text
MACHINE_REALIZATION_STATUS
PRIMARY_VERIFICATION_STATE      # exactly one allowed proof-state value
VERIFICATION_ARTIFACTS
ACTUAL_CURRENT_ROUTE
REMAINING_GAP
SAFE_DEFER_OR_REVISIT_TRIGGER
OPTIONAL_SUPPORTING_ACCEPTANCE  # does not replace primary state
```

`PRIMARY_VERIFICATION_STATE` uses exactly one of:

```text
EXECUTABLE_CURRENT
STATIC_AUDIT_CURRENT
SCENARIO_ACCEPTANCE_CURRENT
EMPIRICAL_EVALUATION_CURRENT
DEFERRED_UNTIL_REALIZATION
VERIFICATION_GAP
SUPERSEDED_OR_HISTORICAL
NOT_MACHINE_CHECKABLE
```

If one aggregated row contains independently realized slices with different primary states, that row must be split into bounded sub-rows. A `+` or `/` concatenation is not a canonical primary state.

### Corrected interpretation of Step-2 composite rows

The Step-2 matrix remains design evidence; the following normalization controls its composite shorthand:

- **VCM-17** — bounded publication outcome algebra: `EXECUTABLE_CURRENT`; end-to-end transport is a separate `DEFERRED_UNTIL_REALIZATION` sub-slice.
- **VCM-23** — current scenario/acceptance contract: `SCENARIO_ACCEPTANCE_CURRENT`; executable authorization enforcement remains a named future gap triggered by runtime realization.
- **VCM-25, VCM-26, VCM-27, VCM-29, VCM-30, VCM-36** — where a current mapped scenario/Protocol-4 acceptance artifact exists, primary state is `SCENARIO_ACCEPTANCE_CURRENT`; machine/runtime realization and executed acceptance remain deferred in the separate realization/gap fields.
- **VCM-32** — local deterministic bootstrap scaffold/audit slice: `STATIC_AUDIT_CURRENT`; remote campaign publication/activation is a separate `DEFERRED_UNTIL_REALIZATION` sub-slice.
- **VCM-38** — PO-006 branch/ref policy slice: `EXECUTABLE_CURRENT`; non-ref runtime cleanup families remain separate `DEFERRED_UNTIL_REALIZATION` slices.
- **VCM-40** — source/layout structural boundary is `STATIC_AUDIT_CURRENT`; executable package/provenance/tooling contracts form a separate `EXECUTABLE_CURRENT` sub-slice.
- **VCM-41** — Protocol-4 design/fixture mapping: `SCENARIO_ACCEPTANCE_CURRENT`; execution result remains absent and post-implementation execution remains a separately recorded defer obligation.
- **VCM-42..VCM-48** — current frozen scenario/fixture obligations: `SCENARIO_ACCEPTANCE_CURRENT`; production-like execution/empirical acceptance remains deferred until the real MVP exists.
- **VCM-49** — open-ended semantic quality judgment: `NOT_MACHINE_CHECKABLE`; any bounded scenario-checkable constraint is a separate `SCENARIO_ACCEPTANCE_CURRENT` sub-slice.

Rows whose primary state was already singular remain unchanged.

### Important semantic consequence

`DEFERRED_UNTIL_REALIZATION` is not used as an extra badge beside an existing current scenario proof merely to say that the scenario has not been executed. Machine realization and empirical execution status already have separate fields. Conversely, a law with no current executable/static/scenario/empirical proof artifact and an intentionally unrealized target may use `DEFERRED_UNTIL_REALIZATION` as its primary verification state.

### Human decision required?

**NO.**

---

## 4. SR22-06-03 — hosted-route currentness

### Issue

Exact workflow commands are current operational facts, not timeless architecture constants.

### Resolution

The final contract states:

```text
actual CI/audit/evaluation route is checkpoint evidence
-> read it fresh at each completeness/closure claim
-> bind any green-result claim to the exact HEAD and actual checks executed
```

The current checkpoint route is still:

```text
DEV/TOOLS/run_maintenance_audit.py
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

because `.github/workflows/validate.yml` currently declares those commands. Future workflow changes do not require an architecture amendment unless they change verification semantics; they do require fresh route mapping before a new completeness claim.

### Human decision required?

**NO.**

---

## 5. Mandatory finding-propagation sweep

| Artifact | SR22-06-01 | SR22-06-02 | SR22-06-03 | Final disposition |
|---|---|---|---|---|
| Step-1 Task Brief / Source Manifest | not affected; already distinguishes source roles | not affected; vocabulary requirement preserved | not affected | retained current Step-1 provenance |
| Step-1 critic | not affected | not affected | not affected | retained historical gate evidence |
| Step-2 Verification Coverage Matrix | **affected** | **affected** | route wording affected | retained as historical Step-2 design evidence with an artifact-local supersession notice naming `SR22-06-01` / `SR22-06-02` and routing to Step 6, Step 7 and the final canonical owner; historical cells remain unchanged and non-current |
| Step-3 Decision Brief | recommendation remains valid; source-role wording interpreted under repair | layered recommendation remains valid | not materially affected | retained design provenance; no rewrite required |
| Step-4 Collaborative Review | CR22-01 principle remains valid but Step-6 found mechanical leakage in Step 2 | partial-realization review remains valid but representation is normalized here | not materially affected | retained design provenance; Step-6/7 provides later correction |
| Step-5 Candidate Specification | **affected** by missing explicit source-role split | **affected** by ambiguous mapping representation | bounded wording affected | retained as historical candidate design provenance with an artifact-local supersession notice; materially qualified candidate wording is non-current, final canonical WP-22 spec controls, and the candidate is not implementation-planning authority |
| Step-6 critic | owns finding evidence | owns finding evidence | owns finding evidence | current design-provenance finding owner |
| Step-7 resolution | owns repair/propagation | owns repair/propagation | owns repair/propagation | current design-provenance resolution owner |
| Final canonical WP-22 spec | incorporates corrected source roles | incorporates single-primary-state model | incorporates fresh-route rule | one final semantic owner for WP-22 |
| `DEV/CURRENT_PROGRESS.md` | synchronized at Step-8/final-repair gate | same | same | current status routes to repeat final Senior review |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | no routing change | same | same | no update required |
| Near-term roadmap | no sequence/scope change | no sequence/scope change | no sequence/scope change | no update required |
| Deferred/debt state | no new activation | existing future verification obligations retain their triggers | no new debt | no new backlog/debt artifact required |

Targeted final Senior repair `SR22-FINAL-01` completed the required artifact-local propagation for Step 2 and Step 5. Both affected historical artifacts now self-identify the `SR22-06-01` / `SR22-06-02` qualification, preserve the reviewed historical wording, prohibit current use of those formulations, and route directly to Step 6, this Step-7 resolution, and the final canonical WP-22 owner.

No rejected formulation remains as current normative law. Step-2/3/4/5 documents are design provenance; implementation planning must route from the final accepted spec plus actual current semantic owners, not from those historical shorthand cells.

---

## 6. Risk re-check after repair

The repair introduces no new semantic owner, runtime state, schema field, implementation obligation, Protocol-4 execution or release-readiness claim.

Residual risks are intentionally bounded:

- a future matrix can still be stale if owners change -> mandatory bidirectional reconciliation and fresh current-owner read;
- a future workflow can change -> actual route must be read fresh;
- deferred obligations can later become realizable -> revisit on the named realization trigger, not before;
- scenario/empirical evidence can be over-credited -> primary proof-state law and semantic-owner separation prevent promotion by presence.

No further adversarial loop is required because the Step-6 significant findings are representation/traceability repairs and do not alter the architectural choice or create a new material trade-off.

---

## 7. Step-7 exit

```text
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
UNRESOLVED_MINOR: 0
SR22_FINAL_01_TARGETED_PROPAGATION_REPAIR: COMPLETE
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
READY_FOR_STEP8_CANONICALIZATION: YES
WP23_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
PROTOCOL_4_EXECUTED: NO
```
