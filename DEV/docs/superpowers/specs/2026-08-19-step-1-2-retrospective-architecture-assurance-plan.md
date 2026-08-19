# Steps 1–2 Retrospective Architecture Assurance Plan

Status: **ACTIVE ASSURANCE OVERLAY — STEPS 1–2 BASELINES REMAIN ACCEPTED**

Target branch: `feature/mechanical-runtime-hot-state`

Process: `DEV/DESIGN_PROCESS.md` plus `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

## 1. Purpose

Steps 1 and 2 are already closed and remain the accepted architecture baseline. This assurance pass exists because substantial early architecture work was framed through human-directed exploration before the current canonical deep-design process was established.

The primary risk being tested is not merely whether accepted solutions are internally consistent with their original problem statements. The harder question is whether the **problems themselves were framed completely enough**: whether a material class, requirement, failure mode, quality attribute, dependency, extension constraint, or ownership question was never asked and therefore escaped later reviews.

This is not a redesign exercise. Existing Step-1/Step-2 decisions remain accepted until a concrete finding demonstrates that the baseline fails a requirement or creates a material cross-system risk.

## 2. Governing rules

1. **Baseline-preserving.** Do not reopen or replace accepted architecture without a concrete finding.
2. **Problem-first.** Each review slice begins with a solution-blind Architecture Task Charter reconstructed from project goals, invariants, downstream consumers, domain mechanics, and quality attributes before reading the detailed accepted local solution.
3. **Coverage before invention.** Compare the accepted solution against independently reconstructed requirements before proposing alternatives.
4. **Research only gaps.** Research targets missing, partial, weakly evidenced, contradictory, high-risk, or unsafe-deferred requirements rather than repeating already sufficient work.
5. **Finding burden.** A finding must identify the requirement/failure mode, show why current architecture does not fully cover it, give a concrete counterexample or cross-system consequence, assess severity, and recommend the smallest sufficient correction.
6. **Deferral audit.** A deferred item is not automatically valid merely because it has an owner. Review whether delaying it is safe and whether an earlier minimum contract was required.
7. **No cosmetic reopening.** Naming/style/schema polish does not reopen architecture unless it causes semantic ambiguity, duplicate authority, invalid extensibility, migration risk, or other material harm.
8. **Human gates only for material decisions.** Mechanically implied fixes are agent-owned. Escalate only genuine product/architecture trade-offs or changes to canonical ownership/boundaries.
9. **Evidence separation.** Keep FACT / CONSTRAINT / ASSUMPTION / INFERENCE / RECOMMENDATION / DECISION explicit.
10. **Global check last.** Slice-local success does not prove integrated success; a dedicated Step-1+2 cross-system pass is mandatory.

## 3. Standard mini-cycle for each slice

### A. Solution-blind Task Charter

Construct the problem independently of the accepted local solution. Cover as applicable:

- purpose and success criteria;
- goals and non-goals;
- upstream/downstream dependencies;
- authority, identity, ownership and lifecycle questions;
- domain/SRD cases that must be representable;
- deterministic/LLM boundary implications;
- persistence/recovery implications;
- performance/index/query/discovery implications;
- observability/testability;
- versioning/migration/compatibility implications;
- failure scenarios and known unknowns;
- what must be fixed now versus may safely wait.

### B. Coverage audit

Map every charter requirement to the accepted baseline:

```text
FULL          explicitly and correctly covered
IMPLICIT      covered in effect but insufficiently specified/tested
PARTIAL       some semantics exist but requirement is not fully closed
MISSING       no valid representation/ownership exists
DEFERRED_OK   later owner is explicit and current minimum contract is sufficient
DEFERRED_RISK deferral leaves an unsafe missing contract
OUT_OF_SCOPE  correctly excluded
```

### C. Targeted research

Research only `IMPLICIT`, `PARTIAL`, `MISSING`, `DEFERRED_RISK`, weak assumptions, and credible counterexamples. Prefer project contracts, official SRD/vendor documentation, standards/primary sources, and comparable-engine implementation evidence.

### D. Assurance synthesis

Per slice record:

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

A separate critic attacks the Task Charter, coverage mapping, research applicability, and synthesis. It must test:

- omitted requirement classes;
- accidental satisfaction mistaken for designed satisfaction;
- duplicate/missing authority or identity;
- lifecycle and restart/recovery gaps;
- local optimization that harms another subsystem;
- interactions among independently correct mechanisms;
- hidden execution/persistence assumptions;
- unsafe deferrals;
- unnecessary abstraction/YAGNI;
- architecture prematurely frozen for later Steps 3–6.

### F. Resolution

If no material finding remains, mark the slice `ASSURED / KEEP` and preserve the baseline.

If findings are mechanical consequences of accepted decisions, amend specs/schemas/tests directly and rerun review.

If a material architecture decision is required, present one decision-ready brief to the human architect. A numbered roadmap stage is formally reopened only if its accepted ownership/boundary model cannot remain valid without a material change.

## 4. Review slices

### Slice 0A — Catalog meta-model and class boundaries

Scope:

- engine capability registry;
- reusable content-definition classes;
- world-record classes;
- runtime-record classes;
- transient protocol/value classes;
- facets/tags versus executable capability;
- identity/lifecycle test for deciding when a concept deserves a class/record;
- duplicate and missing class boundaries;
- definition/instance/runtime separation;
- whether the catalog actually supports HDM's LLM + deterministic-core split.

This slice asks whether the fundamental vocabulary decomposition is correct before auditing individual mechanics built on it.

### Slice 0B — Catalog evolution, identity, strata and discoverability

Scope:

- engine/ruleset/campaign/session definition strata;
- stable IDs, namespaces and non-repurposing;
- catalog versioning and compatibility;
- forward/cross references and validation;
- local/session definitions and durable promotion;
- definition transformation/migration consequences;
- standard ruleset seed versus engine capability boundary;
- campaign extensions and catalog-gap handling;
- LLM discovery/search/hydration requirements;
- prevention of prompt-memory becoming a hidden catalog authority;
- loader/resolution-order semantics and conflict behavior.

### Slice A — Actor mechanical state

Scope:

- HP and temporary HP;
- maximum-HP derivation;
- LifeState and state-local progress;
- persistent Actor/Asset Resources;
- procedure-local Resources/action economy;
- health/lifecycle/resource ownership and lifetime interaction.

A solution-blind charter already exists:

- `2026-08-19-step-2-assurance-slice-a-actor-state-task-charter.md`

It remains valid but is processed only after Slices 0A and 0B.

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

### Slice E — Whole Steps 1–2 integrated architecture

Scope:

- all Slice 0A–D interactions;
- whether catalog taxonomy and mechanical ownership reinforce or contradict each other;
- authority/identity graph completeness;
- whether Step-2 mechanics require classes/capabilities omitted or misclassified by Step 1;
- lifecycle/transaction assumptions exposed by Step 3;
- LLM/core integration minimum contract;
- continuity/checkpoint minimum contract;
- Step 3/4/5/6 deferral safety;
- performance/index/discovery implications;
- migration/versioning and extension implications;
- representative multi-feature and custom-ruleset counterexamples.

Slice E is not a summary-only review. It independently attacks compositions that local slices may miss.

## 5. Finding severity

```text
BLOCKER      accepted ownership/class boundary cannot represent required behavior safely
SIGNIFICANT  architecture remains viable but requires a nontrivial amendment/missing contract
MODERATE     specification/test/dependency gap with bounded architectural impact
MINOR        clarity/coverage issue that does not alter architecture
```

Only BLOCKER or a SIGNIFICANT finding involving a genuine trade-off automatically creates a human decision gate.

## 6. Artifacts

Per slice:

- `...-task-charter.md`
- `...-coverage-research.md`
- `...-adversarial-review.md`
- `...-resolution.md` when findings require correction; otherwise synthesis may close the slice directly.

Final:

- `...-step-1-2-retrospective-architecture-assurance-final.md`

The final artifact records retained decisions, amendments, unresolved human decisions, safe deferrals, and whether either closed stage must be formally reopened.

## 7. Step 3 preservation

Step 3 remains the single numbered `IN PROGRESS` roadmap stage but is temporarily paused at its already-persisted first Decision Gate while this assurance overlay runs.

Preserved checkpoint:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-research-draft.md`

No Step-3 design decision is lost or implicitly accepted/rejected by this assurance pass.

## 8. Execution order

```text
0A Catalog meta-model/class boundaries
  -> 0B Catalog evolution/identity/strata/discovery
      -> A Actor state
          -> B Effects/Conditions
              -> C Temporal/Recovery
                  -> D Evaluation/read boundaries
                      -> E Whole Steps 1–2 integration
```

A later slice may expose a contradiction in an earlier slice. If so, reopen only the smallest affected assurance result rather than restarting the full sequence.

## 9. Exit criteria

The retrospective assurance closes when:

1. all seven slices have solution-blind charters;
2. every charter requirement has an explicit coverage status;
3. all material gaps/weak assumptions have targeted research;
4. all slices have adversarial review;
5. every finding is resolved, safely deferred, or escalated;
6. final integrated assurance finds no unowned architecture risk;
7. accepted changes, if any, are reflected in normative specs/schemas/catalogs/tests/status artifacts;
8. Steps 1–2 are explicitly reaffirmed or consciously amended/reopened;
9. Step 3 resumes from its saved Decision Gate against the assured baseline.
