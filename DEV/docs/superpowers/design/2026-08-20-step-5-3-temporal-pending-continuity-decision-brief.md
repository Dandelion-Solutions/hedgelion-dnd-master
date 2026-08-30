# Step 5.3 — Temporal & Pending-Obligation Continuity — Decision Brief

Status: **HUMAN ARCHITECT DECISION REQUIRED**

Date: 2026-08-20

Inputs:

- `2026-08-20-step-5-3-temporal-pending-continuity-pre-research-charter.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-task-brief.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-research-draft.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-analytical-challenge.md`

## 1. Decision to make

Choose how a native temporal owner represents an occurrence that has already crossed from rebuildable `DUE` candidate into long-lived mandatory execution but whose child execution has not yet settled.

This decision applies only when accepted execution outlives the materializing segment. One-step deterministic expiration/recovery may still transition directly with no visible in-flight phase.

The two credible alternatives are:

```text
A-NARROW — OWNER CLAIM
    native owner marks that exact occurrence as claimed/in-flight
    + existing Step-3 firing/pending child identity is materialized

B-IDEMPOTENT-LOOKUP — OWNER REMAINS ARMED
    native owner keeps the same armed/due binding
    + every materialization attempt derives firing key and looks up
      existing active/retained execution identity before creating work
```

A standalone firing/job record was analyzed and rejected as unjustified YAGNI; it is not part of this decision.

---

# 2. Facts already settled regardless of choice

The following do **not** require decision:

1. Temporal Agenda is rebuildable projection, not authority.
2. Step-5.2 temporal routing enrolls every armed independently-due owner for its armed lifetime.
3. Temporal comparison is conceptually three-valued:
   - `NOT_DUE`
   - `DUE`
   - `INDETERMINATE` when chronology is insufficient.
4. Storage/Git/ID order cannot resolve temporal ambiguity.
5. Every independently materializable occurrence requires stable identity distinct from timing value; BoundaryOccurrence already supplies this for boundary cases, while metric obligations need owner-local occurrence/generation identity unless uniqueness is otherwise proven.
6. Step-3 ExecutionSegment/pending-child/firing-key/idempotency semantics remain the execution mechanism.
7. No generic scheduler/job/pending-obligation subsystem is introduced.
8. No synthetic background/internal RuntimeCommand is introduced under the current host model; causal advancement supplies an existing execution root, and a passed durable due boundary with missing mandatory execution identity is a defect.
9. Already generated/accepted RNG remains fixed in native execution owners.
10. Generic mandatory `Continuation.future_rng_frontier` is not justified architecturally; later machine realization should retire it unless a concrete reservation-before-generation mechanic is proven.

---

# 3. Alternative A-NARROW — owner claim

## Semantics

When occurrence `G` is accepted for long-lived execution:

```text
ARMED(G, binding B)
    -> CLAIMED(G, firing F)
       + existing Step-3 pending child / child Resolution F

child settles
    -> REARM(G+1, binding B2)
       OR UNARM
       OR OWNER TERMINAL
```

`CLAIMED` is a logical owner-local state/reference. It does not require a universal field name or common record schema across every owner family.

Minimal claim contains only enough to establish:

```text
this owner-local occurrence G
is already committed to stable firing/execution identity F
```

It does **not** copy:

- child payload/status;
- deadline/due result;
- chronology relation;
- Procedure state;
- RNG result;
- execution receipt bodies.

Those remain in their native owners.

## Advantages

- local owner state says whether the occurrence is still available for fresh materialization;
- due evaluation does not require a negative scan/lookup across active execution roots;
- suspended reactions/choices cannot leave the owner falsely presenting the occurrence as freshly selectable;
- owner lifecycle remains locally inspectable/debuggable;
- idempotency evidence remains duplicate-suppression evidence rather than becoming implicit eligibility authority;
- clearer integrity invariant: claim and execution identity must exist together.

## Costs

- owner schemas/lifecycles that support outcome-dependent long-lived scheduled work need a minimal claimed/in-flight representation;
- more lifecycle states/relations than B;
- publication 5.6 must preserve claim + execution materialization closure;
- later 5.7/5.8 routing must ensure bounded recovery when an armed temporal membership transitions into claimed execution state.

## Complexity profile

```text
owner-state complexity       higher
runtime lookup complexity    lower
semantic locality            stronger
cross-root dependency        lower
observability/debuggability  stronger
```

---

# 4. Alternative B-IDEMPOTENT-LOOKUP — owner remains armed

## Semantics

When occurrence `G` is accepted:

```text
owner remains ARMED(G, B)
Step-3 pending execution F is materialized

any later/recovery attempt:
    derive F from owner occurrence G
    search active/retained execution identity
    F exists -> resume/suppress duplicate
    F absent -> materialize

child settles atomically:
    owner -> REARM(G+1) | UNARM | TERMINAL
```

## Advantages

- less owner schema/lifecycle expansion;
- maximizes reuse of Step-3 firing-key idempotency;
- no explicit claim reference on owner;
- mechanically smaller representation if lookup infrastructure is already cheap.

## Costs

- owner continues to look `DUE` while execution is already committed/in flight;
- every due materialization requires a bounded cross-root firing-key existence lookup;
- due eligibility becomes a join of temporal owner state + execution-root state rather than native owner semantics alone;
- firing-key evidence retention/indexability becomes correctness-critical while old binding remains visible;
- long Choice/Reaction suspension can keep one owner visibly due for an extended period;
- same-owner rules that need to distinguish “freshly armed” from “already committed to executing this occurrence” must consult execution state;
- a missing execution lookup can cause duplicate materialization even though owner data itself appears valid.

## Complexity profile

```text
owner-state complexity       lower
runtime lookup complexity    higher
semantic locality            weaker
cross-root dependency        higher
observability/debuggability  weaker
```

---

# 5. Why separate firing record is not recommended

A first-class firing record would add an independent lifecycle between source owner and Step-3 execution.

No current requirement demonstrates independent:

- authority;
- permissions;
- lifetime after both source and execution disappear;
- queue semantics;
- payload ownership.

It would create new publication/routing/retention/migration work and risk becoming a generic job table. Existing source owner + execution owner already cover the required semantics.

Confidence in rejection: **HIGH**.

---

# 6. Recommendation

**Recommend A-NARROW / OWNER CLAIM.**

Confidence: **HIGH**.

Reason:

> Once a temporal occurrence has become accepted mandatory execution, the source owner should no longer present that exact occurrence as freely materializable. Keeping this fact local to the owner preserves HDM's ownership discipline and prevents idempotency lookup from becoming an implicit second authority over temporal eligibility.

The extra state is narrow and conditional: only temporal obligations whose accepted execution outlives the current segment need the logical claimed/in-flight relation.

One-step deterministic recovery/expiration does not gain an unnecessary intermediate phase.

---

# 7. Strongest reason to choose B instead

Choose **B-IDEMPOTENT-LOOKUP** if the project prioritizes minimal persistent owner schemas over local semantic clarity and is willing to make bounded firing-key lookup a mandatory part of temporal materialization correctness.

B is not architecturally invalid. It trades durable owner-state complexity for runtime coupling and lookup complexity.

If the expected number of active roots/temporal candidates is extremely small and owner schemas are unusually costly to evolve, B becomes more attractive.

No current repository evidence shows those conditions outweigh the locality/correctness advantages of A.

---

# 8. Reversibility

A -> B later:

- remove claimed state after ensuring firing-key lookup/index/retention is complete;
- migration of active claimed occurrences required if changing live persisted formats.

B -> A later:

- add owner claimed relation;
- materialize it for any in-flight temporal firings during migration;
- easier before production campaigns contain durable in-flight state.

Both are reversible, but choosing before machine realization avoids migration complexity.

---

# 9. What the decision will unlock

If **A-NARROW** is approved, Candidate Spec will formalize:

- owner occurrence identity/generation;
- `ARMED -> CLAIMED -> REARM|UNARM|TERMINAL` only for long-lived outcome-dependent work;
- direct one-step owner transitions where no child persists;
- claim + Step-3 execution atomic semantic closure;
- three-valued temporal comparison;
- recovery/idempotency crash matrix;
- fixed RNG continuity and retirement direction for generic `future_rng_frontier`;
- later 5.5–5.9 requirements without physical protocol design.

If **B-IDEMPOTENT-LOOKUP** is chosen, Candidate Spec will instead make bounded firing-key lookup an explicit mandatory eligibility step and define its retention/recovery invariants.

No implementation begins at this decision.

---

# 10. Requested owner decision

Choose one:

```text
A-NARROW — owner-local claim/in-flight relation   [RECOMMENDED]
B-IDEMPOTENT-LOOKUP — owner stays armed/due; firing lookup suppresses duplicate
```
