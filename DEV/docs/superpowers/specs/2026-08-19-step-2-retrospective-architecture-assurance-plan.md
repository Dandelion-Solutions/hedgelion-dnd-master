# Step 2 Retrospective Architecture Assurance Plan

Status: **ACTIVE ASSURANCE OVERLAY — STEP 2 BASELINE REMAINS ACCEPTED**

Target branch: `feature/mechanical-runtime-hot-state`

Process: `DEV/DESIGN_PROCESS.md` plus `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

## 1. Purpose

Step 2 is already closed and remains the accepted architecture baseline. This assurance pass exists because a substantial early portion of Step 2 was framed through human-directed exploration before the current canonical deep-design process was established.

The risk being tested is therefore not merely whether the accepted solution is internally consistent with its original problem statement. The primary question is whether the **problem itself was framed completely enough**: whether a material requirement, failure mode, quality attribute, dependency, or ownership question was never asked and was therefore absent from later reviews.

This is not a redesign exercise. Existing Step-2 decisions remain accepted until a new review produces a concrete finding demonstrating that the baseline fails a requirement or creates a material cross-system risk.

## 2. Governing rules

1. **Baseline-preserving.** Do not reopen or replace accepted architecture without a concrete finding.
2. **Problem-first.** Each review slice begins with a solution-blind Architecture Task Charter reconstructed from project goals, invariants, downstream consumers, domain mechanics, and quality attributes before reading the detailed Step-2 solution for that slice.
3. **Coverage before invention.** Compare the accepted solution against the reconstructed requirements before proposing alternatives.
4. **Research only gaps.** External/project research is targeted to missing, partial, weakly evidenced, contradictory, or high-risk requirements; do not repeat broad research already sufficient for covered requirements.
5. **Finding burden.** A finding must identify the requirement/failure mode, show why current architecture does not fully cover it, provide a concrete counterexample or cross-system consequence, assess severity, and recommend the smallest sufficient correction.
6. **Deferral audit.** A deferred item is not automatically valid merely because it has an owner. Review whether delaying it is actually safe and whether Step 2 already needed a minimum contract.
7. **No cosmetic reopening.** Naming/style/schema polish does not reopen architecture unless it causes semantic ambiguity, duplicate authority, invalid extensibility, migration risk, or other material harm.
8. **Human gates only for material decisions.** Mechanically implied fixes are agent-owned. Escalate only genuine product/architecture trade-offs or changes to canonical ownership/boundaries.
9. **Evidence separation.** Keep FACT / CONSTRAINT / ASSUMPTION / INFERENCE / RECOMMENDATION / DECISION explicit.
10. **Global check last.** Slice-local success does not prove integrated success; a dedicated cross-system pass is mandatory.

## 3. Standard mini-cycle for each slice

### A. Solution-blind Task Charter

Construct the problem independently of the accepted local solution. It must cover:

- purpose and success criteria;
- goals and non-goals;
- upstream/downstream dependencies;
- authority and ownership questions;
- lifecycle/state transitions;
- domain/SRD cases that must be representable;
- determinism and LLM-boundary implications;
- persistence/recovery implications where relevant;
- performance/index/query implications;
- observability/testability;
- versioning/migration implications;
- failure scenarios and known unknowns;
- what must be decided now versus may safely wait.

### B. Coverage audit

Map each charter requirement to the accepted Step-2 baseline:

```text
FULL        explicitly and correctly covered
IMPLICIT    covered by architecture but insufficiently specified/tested
PARTIAL     some semantics exist but requirement is not fully closed
MISSING     no valid representation/ownership exists
DEFERRED_OK later owner is explicit and Step 2 has sufficient minimum contract
DEFERRED_RISK deferral leaves an unsafe missing contract
OUT_OF_SCOPE correctly excluded
```

### C. Targeted research

Research only `IMPLICIT`, `PARTIAL`, `MISSING`, `DEFERRED_RISK`, weak assumptions, and credible counterexamples. Prefer project contracts, SRD/official documentation, standards/primary technical sources, and comparable engine implementations.

### D. Assurance synthesis

For the slice produce:

```text
Existing design retained
Requirements newly proven
Gaps/findings
Corrections or additions
Safe deferrals
Debt/backlog
Cross-system effects
Recommendation: KEEP | AMEND | REOPEN
Human decision required: YES | NO
Confidence
```

### E. Adversarial review

A separate critic attacks the Task Charter, coverage mapping, research applicability, and synthesis. The critic must specifically test:

- omitted requirement classes;
- accidental satisfaction mistaken for designed satisfaction;
- duplicate/missing authority;
- lifecycle and restart/recovery gaps;
- local optimization that harms another subsystem;
- interaction between otherwise-correct mechanics;
- hidden execution/persistence assumptions;
- unsafe deferrals;
- unnecessary abstraction/YAGNI;
- architecture frozen for later Step 3/4/5 without necessity.

### F. Resolution

If no material finding remains, mark the slice `ASSURED / KEEP` and preserve the baseline.

If findings are mechanical consequences of accepted decisions, amend specs/schemas/tests directly and rerun review.

If a material architecture decision is required, present one decision-ready brief to the human architect. Step 2 is formally reopened only if the accepted baseline cannot remain valid without changing a Step-2 ownership/boundary decision.

## 4. Review slices

### Slice A — Actor mechanical state

Scope:

- HP and temporary HP;
- maximum-HP derivation;
- LifeState and state-local progress;
- persistent Actor/Asset Resources;
- procedure-local Resources/action economy;
- health/lifecycle/resource ownership and lifetime interaction.

Key cross-system consumers: Activities/Resolution, healing/damage, rests/recovery, effects/conditions, transformations, persistence, multiplayer revisions.

### Slice B — Effects and Conditions

Scope:

- Effect identity/application/lifecycle/provenance;
- reapplication, arbitration, suppression/availability;
- Condition identity and aggregation;
- intrinsic rule scope;
- maintained support/concentration;
- removal/expiry/provenance-sensitive behavior;
- zone/owner edge cases where they touch the same model.

### Slice C — Temporal and Recovery

Scope:

- reusable DurationSpec;
- concrete TemporalBinding;
- metric/procedure/semantic bases;
- boundary vocabulary and occurrence ownership;
- automatic state-owner responses;
- Temporal Agenda/index semantics;
- recovery after interruption/environment loss;
- cross-basis re-anchoring and pending obligations.

### Slice D — Mechanical evaluation and read boundaries

Scope:

- Calculation Selectors;
- MechanicalContext facts/accessors;
- runtime-only domain queries;
- pinned committed/prospective views;
- scoped dependency DAG/cycle rejection;
- indexing/hydration implications;
- LLM versus deterministic mechanical authority.

### Slice E — Whole-Step-2 integrated architecture

Scope:

- all Slice A-D interactions;
- authority graph completeness;
- lifecycle/transaction assumptions exposed by Step 3;
- LLM/core integration minimum contract;
- continuity/checkpoint minimum contract;
- Step 4/5/6 deferral safety;
- performance/index and migration/versioning implications;
- representative multi-feature counterexamples.

Slice E is not a summary-only review. It independently attacks compositions that local slices may miss.

## 5. Finding severity

```text
BLOCKER      accepted Step-2 ownership/boundary cannot represent required behavior safely
SIGNIFICANT  architecture remains viable but requires a nontrivial amendment or missing contract
MODERATE     specification/test/dependency gap with bounded architectural impact
MINOR        clarity/coverage issue that does not alter architecture
```

Only BLOCKER or a SIGNIFICANT finding involving a genuine trade-off automatically creates a human decision gate.

## 6. Artifacts

Per slice:

- `...-task-charter.md`
- `...-coverage-research.md`
- `...-adversarial-review.md`
- `...-resolution.md` when findings require correction; otherwise the assurance synthesis may close the slice directly.

Final:

- `...-step-2-retrospective-architecture-assurance-final.md`

The final artifact records retained decisions, amendments, unresolved human decisions, safe deferrals, and whether Step 2 remains closed or must be formally reopened.

## 7. Step 3 preservation

Step 3 remains the single numbered `IN PROGRESS` roadmap stage but is temporarily paused at its already-persisted first Decision Gate while this assurance overlay runs.

The preserved Step-3 checkpoint is:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-research-draft.md`

No Step-3 design decision is lost or implicitly accepted/rejected by this assurance pass.

## 8. Exit criteria

The retrospective assurance closes when:

1. all five slices have solution-blind charters;
2. every charter requirement has an explicit coverage status;
3. all material gaps/weak assumptions have targeted research;
4. all slices have adversarial review;
5. every finding is resolved, safely deferred, or escalated to a human decision;
6. final integrated assurance finds no unowned architecture risk;
7. accepted changes, if any, are reflected in normative specs/schemas/tests/status artifacts;
8. Step 3 can resume from its saved Decision Gate with the Step-2 baseline explicitly reaffirmed or consciously amended.
