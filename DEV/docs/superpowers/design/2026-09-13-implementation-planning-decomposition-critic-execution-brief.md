# HDM Implementation Planning — Independent Decomposition Critic Execution Brief

Status: **ACTIVE REVIEW ROUTE — INDEPENDENT REVIEWER ONLY**

Date: 2026-09-13

This brief operationalizes the mandatory Decomposition Critic gate defined by `2026-09-13-implementation-planning-decomposition-critic-amendment.md`.

It does not authorize detailed executable plan authoring or production implementation.

---

## 1. Reviewer isolation requirement

The reviewer executing this brief MUST be independent from the authoring context/model that produced:

- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-p3-dependency-dag.md`;
- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-candidate-bounded-decomposition.md`.

Independence means a separate reviewer model/context that did not author the candidate decomposition and is free to reject it completely. A second pass by the decomposition author, a persona switch, an author self-review, or an unverified claim of reviewer separation does not satisfy this gate.

If reviewer independence cannot be established, publish no PASS/FAIL verdict and do not allow detailed plan authoring to proceed.

---

## 2. Fresh bootstrap and authoritative state

Use GitHub Connector as the only authoritative repository transport/state source.

Fresh bootstrap in this order:

```text
current remote HEAD/ref
-> AGENTS.md
-> applicable runtime overlay
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> DEV/CURRENT_PROGRESS.md
-> DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md
-> task-local amendment / P1-P2 / P3 / candidate decomposition
-> exact task-specific native owners/evidence required to validate challenged edges and units
```

Do not rely on chat history, handoff prose, the candidate's own counts, or its stated dependencies as proof.

The expected planning baseline is:

```text
PLANNING_BASELINE_SHA: 85311db76be2e440c97baf0b0625177de2eb0774
EXPECTED_ACTIVE_READINESS: 133
EXPECTED_TRIGGER_GATED_READINESS: 12
EXPECTED_EXPLICIT_NO_WORK_TERMINALS: 79
R27_R004_EXPECTED: ABSENT
```

Fresh-check whether current repository state has moved. If semantic/runtime/version owners or P1/P2 dispositions changed after the candidate, classify currentness impact before reviewing the decomposition.

---

## 3. Mandatory review inputs

Read at minimum:

1. `DEV/docs/superpowers/design/2026-09-13-implementation-planning-decomposition-critic-amendment.md`;
2. `DEV/docs/superpowers/design/2026-09-13-implementation-planning-p1-p2-readiness-active-set.md`;
3. `DEV/docs/superpowers/design/2026-09-13-implementation-planning-p3-dependency-dag.md`;
4. `DEV/docs/superpowers/design/2026-09-13-implementation-planning-candidate-bounded-decomposition.md`;
5. `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md` for exact item fields;
6. `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md` for integration law only;
7. `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` for Impact Envelope/System Impact/TDD/version-gate feasibility;
8. native owner/spec artifacts necessary to verify every material challenged dependency, boundary, owner/consumer join, dormant trigger or negative law.

Use `DEV/PROJECT_MAP.md` for discovery only. WP-27 workstream groupings and the candidate's `CD-*` labels are planning projections, not semantic authority.

---

## 4. Independent reconstruction requirement

Before judging the candidate, reconstruct the relevant whole-project dependency subgraph independently from exact readiness/native-owner evidence.

At minimum independently establish:

- the exact current active readiness set;
- the exact trigger-gated readiness set and each trigger class;
- the exact no-work terminal set and the absence of `R27-R004`;
- material owner -> machine/consumer -> proof relationships;
- hard predecessor edges versus integration joins versus non-ordering constraints;
- current parallel roots;
- proof-only routes;
- derived/rebuildable surfaces that must not become predecessor authority;
- any version/migration-sensitive boundary that affects decomposition isolation;
- any HG-01-sensitive runtime seam that affects unit boundaries.

Do not begin from the candidate's 14-unit split and merely inspect it for plausibility.

---

## 5. Mandatory adversarial tests

The critic MUST actively test for all amendment obligations:

1. missing or duplicate readiness/proof coverage;
2. false ordering and hidden dependencies;
3. incorrect parallelism or unnecessary serialization;
4. native owner responsibilities merged for implementation convenience;
5. one native responsibility fragmented into units that create duplicated authority or cross-plan atomicity;
6. units too large for bounded TDD/review/commit or artificially tiny units that only move coupling elsewhere;
7. cycles hidden by arbitrary ordering;
8. proof-only obligations turned into fake runtime subsystems;
9. implementation work missing deterministic/scenario proof routes;
10. empirical/release proof activated without its exact trigger;
11. dormant/deferred/future/no-work obligations activated prematurely;
12. rejected architecture reintroduced by a unit boundary;
13. hidden cross-plan coupling or missing integration joins;
14. plan boundaries that silently decide a human-owned product/architecture/scope/compatibility/material-risk question;
15. version/migration blast radius crossing candidate boundaries in a way that defeats independent execution;
16. Impact Envelope boundaries too vague to enumerate owners, consumers, interfaces, protected invariants, architecture-sensitive surfaces and integration verification;
17. HG-01 novel-action constraints hidden behind generic runtime units;
18. any candidate unit that would force detailed plan authors to rediscover architecture rather than execute a settled owner contract.

The critic MUST specifically stress `CD-02`, `CD-03`, `CD-04`, `CD-05`, `CD-07`, `CD-08`, `CD-10`, `CD-12`, `CD-13`, and `CD-14`, because the candidate itself identifies these as material coupling risks. This is not a limit: any or all 14 units may be rejected.

---

## 6. Finding schema

Each finding must be itemized as:

```text
FINDING_ID: DC-###
SEVERITY: BLOCKING | SIGNIFICANT | MINOR
STATUS: OPEN | RESOLVED_ON_REREVIEW
CANDIDATE_UNIT(S): CD-xx [, ...] | WHOLE_DECOMPOSITION
READINESS_ID(S): exact R27-R### set
NATIVE_OWNER_REF(S): exact controlling owner path/section
P3_EDGE_OR_MISSING_EDGE: exact dependency/join/constraint if applicable
EVIDENCE: repository-grounded evidence with applicability/qualifiers
FAILURE_MODE: what becomes incorrect, unbounded, unverifiable, falsely serialized, prematurely activated or architecturally unsafe
REQUIRED_REPAIR: concrete re-decomposition/boundary/dependency/coverage change; no implementation code
REVIEWER_RETEST: exact condition that must hold on independent re-review
```

Preserve negative findings, scope limits and “no issue found” results where they materially support coverage claims.

---

## 7. Verdict rules

Allowed verdicts:

- `REJECT / RE-DECOMPOSE` — decomposition is structurally unsound or requires a substantially different cut;
- `FAIL / REPAIR REQUIRED` — one or more `BLOCKING` or `SIGNIFICANT` findings remain open;
- `PASS` — no unresolved `BLOCKING` or `SIGNIFICANT` finding remains and the reviewer independently verifies decomposition coverage/dependency/boundary fitness. Any MINOR findings must be explicitly non-gating and must not undermine executable-plan readiness.

A PASS may not be based on author assertions, count-only coverage, or absence of obvious contradictions.

If the critic exposes a genuine human-owned decision, mark it explicitly and stop only that decision path. Do not manufacture a human gate for routine technical decomposition work.

---

## 8. Publication contract

Initial independent result path:

`DEV/docs/superpowers/design/2026-09-13-implementation-planning-decomposition-critic-result.md`

The critic result must record:

```text
REVIEWER_ISOLATION: ESTABLISHED
REVIEW_BASELINE_HEAD: <fresh remote SHA>
RECONSTRUCTED_ACTIVE_READINESS: <count and exact discrepancy if any>
RECONSTRUCTED_TRIGGER_GATED: <count and exact discrepancy if any>
RECONSTRUCTED_NO_WORK_TERMINALS: <count and exact discrepancy if any>
BLOCKING_FOUND: <n>
SIGNIFICANT_FOUND: <n>
MINOR_FOUND: <n>
VERDICT: REJECT / RE-DECOMPOSE | FAIL / REPAIR REQUIRED | PASS
DETAILED_EXECUTABLE_PLAN_AUTHORING_AUTHORIZED: YES only on PASS
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

Publish the critic result as its own coherent commit after a fresh remote-ref check; use non-force publication; read it back; verify applicable CI.

On `REJECT` or `FAIL`, the decomposition author repairs/re-decomposes in a separate commit. The independent reviewer then fresh-checks the repaired remote state and publishes a re-review result. Repeat until PASS.

Do not edit production implementation surfaces while executing this brief.

---

## 9. Exit condition

This brief is complete only when either:

- a genuinely independent critic publishes `PASS`; or
- a genuine human-owned decision is identified and precisely scoped; or
- the current runtime cannot establish independent reviewer execution, in which case the project remains at this gate and no detailed executable plan authoring is authorized.
