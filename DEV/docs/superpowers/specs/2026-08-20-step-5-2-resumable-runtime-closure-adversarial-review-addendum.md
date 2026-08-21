# Step 5.2 — Resumable Runtime Closure — Adversarial Review Addendum

Status: **ADVERSARIAL ADDENDUM — ONE SIGNIFICANT REFINEMENT RESOLVED**

Date: 2026-08-20

This addendum supplements:

- `2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review.md`

It does not reopen that review’s accepted S1–S6 findings. It challenges one minor disposition in the existing review because the proposed optimization adds a correctness dependency without a demonstrated need.

---

## A1 — Conditional temporal-source enrollment creates avoidable reachability-transition risk

Severity: **SIGNIFICANT — RESOLVED BY SIMPLIFICATION**

### Existing reviewed wording

The prior review retained the candidate rule that an armed due-capable temporal source owner needs independent temporal routing only when it is otherwise unreachable from another guaranteed recovery root.

### Attack

Consider an active Effect with a due-capable TemporalBinding.

At time T1:

```text
Effect E is armed
E is transitively reachable from active root R
therefore E is omitted from temporal-source routing
```

At time T2:

```text
R becomes terminal / leaves active recovery routing
E remains armed and mechanically due-capable
```

Correctness now requires the unrelated root-lifecycle transition for R to detect that E changed from “redundantly reachable” to “independently discoverable” and enroll E before acknowledging the new durable recovery source set.

That introduces:

- dynamic transitive-reachability analysis into owner/root transitions;
- coupling between temporal continuity and unrelated recovery-root lifecycle;
- an extra omission crash window;
- harder publication validation;
- harder audit reasoning;
- no demonstrated semantic or scaling benefit beyond saving one routing reference.

The optimization becomes even less attractive under partitionable routing, because temporal-source membership can live in the same natural writable scope as the armed owner instead of one global hot singleton.

### Simpler invariant

Adopt:

> **ARMED TEMPORAL ENROLLMENT LAW** — Every armed native temporal source owner that can become mechanically due independently of ordinary direct owner loading SHALL remain enrolled in bounded typed temporal-source routing for its entire armed lifetime, even when the same owner is also transitively reachable through another active recovery root.

This does **not** mean every record containing temporal metadata is enrolled.

Enrollment applies only when all of the following hold:

1. the owner currently carries an armed admitted temporal obligation;
2. that obligation can become mechanically due without the owner first being explicitly loaded for another gameplay reason;
3. loss of that due processing would change gameplay-significant state/continuity.

Procedure-local or otherwise non-independent temporal metadata whose semantics are only evaluated while its already-rooted owner is actively traversed need not become a separate due-capable source class unless 5.3 establishes that it can fire independently.

### Authority remains unchanged

Temporal routing duplicates only owner identity/retrieval evidence.

It SHALL NOT own or determine:

```text
deadline
next_due
due/not-due
priority
selected trigger
firing generation
chronology relation
owner lifecycle
```

Those remain native owner/TemporalBinding/chronology/execution semantics.

### Trade-off

Cost:

- possibly more routing references while an owner is armed.

Benefit:

- no reachability-status optimization in the correctness path;
- no root-disappearance handoff rule for temporal enrollment;
- locally testable invariant: armed due-capable owner ↔ temporal membership;
- easier crash-consistent publication validation;
- simpler cold recovery enumeration.

The routing set still scales with active due-capable temporal obligations, not campaign age or total world-record count.

### Disposition

**Resolve in favor of unconditional armed-lifetime enrollment for independently due-capable temporal source owners.**

This is the simplest viable correctness model and does not require an owner/product decision.

The canonical Step-5.2 specification must supersede the prior review’s conditional “otherwise-unreachable” optimization with this stronger law.
