# Campaign House Rules — Step 8 Canonicalization

Status: **STEP 8 COMPLETE / HOUSE RULES ARCHITECTURE CANONICAL / STOP BEFORE S6D**

Date: 2026-08-25

Owner direction:

- senior architecture audit: **GO FOR STEP 2–8**;
- explicit continuation instruction: complete this design cycle and **stop before S6D**.

---

# 1. Eight-step closure record

| Step | Artifact | Result |
|---|---|---|
| 1 — Architecture Task Brief | `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md` | COMPLETE / owner-amended / critic pass |
| 2 — Research & Architecture Draft | `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md` | COMPLETE / Source Manifest complete |
| 3 — Decision Brief | `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief.md` | Alternative C accepted under explicit owner GO |
| 4 — Collaborative Architecture Review | `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review.md` | PASS / no new owner decision |
| 5 — Candidate Specification | `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec.md` | COMPLETE |
| 6 — Adversarial Architecture Review | `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review.md` | PASS / 0 BLOCKER / 0 SIGNIFICANT / 1 MINOR |
| 7 — Resolution Gate | `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate.md` | PASS / canonicalization authorized |
| 8 — Canonicalization | this artifact | COMPLETE |

---

# 2. Canonical owner

The primary House Rules / established Rulings architecture owner is now:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

It canonically establishes that House Rules / Rulings are a campaign-persistent, LLM-interpreted **semantic gameplay-policy layer** constrained by HDM constitutional/native-owner invariants and handed off through existing typed deterministic execution boundaries.

The design does not create:

- a second rules engine;
- a natural-language executable DSL/compiler;
- a parallel truth/knowledge/secrecy owner;
- direct LLM state/RNG authority;
- a House-Rules-specific global synchronization/frontier;
- mandatory whole-corpus hot-path retrieval;
- forced formalization of intrinsically semantic policy.

---

# 3. Runtime-facing policy contract

The campaign-facing policy surface has been aligned with the canonical architecture:

- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

It now states the runtime-facing purpose and limits of the layer while containing no actual additional campaign House Rules at canonicalization time.

This file remains campaign policy data, not an engine/system instruction tier.

---

# 4. Required inherited owners resolved in Step 2

The pre-flight evidence hardening requested by the owner is part of the closed evidence basis.

Required exact owners include:

- Step-4 truth/knowledge/role-context canonical specification;
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` as the superseding physical-topology correction;
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` for bounded discovery/closure/currentness/eligibility/allocation;
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` for role rebinding, typed handoffs and instruction/data fencing;
- Step-5.6 campaign publication/CAS canonical specification;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` for current-authority-first recovery and accepted historical causal inputs;
- Step-5.8 multiplayer live/currentness canonical specification;
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` for participant current-frontier/context obligations;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md` and `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` for deterministic mechanical handoff ownership.

No evidence demonstrated that these accepted mechanisms are insufficient for House Rules currentness/propagation. Therefore no policy-specific global synchronization mechanism was added.

---

# 5. Canonical result summary

The closed design establishes all of the following:

1. **Semantic authority only.** House Rules govern campaign game-rule/adjudication interpretation and applicability, not direct mechanical execution.
2. **Constitutional upper boundary.** Existing HDM invariants/native owners constrain every policy.
3. **Deterministic lower boundary.** Mechanically material consequences cross existing admitted typed capabilities and deterministic validation/execution.
4. **Current campaign rules context matters.** Stale baseline realization is not constitutional authority; missing faithful realization becomes a finite gap rather than prose execution.
5. **Lightweight durable semantic identity.** Stable policy identity is distinct from exact revision/publication/source basis; exact schema remains downstream realization work.
6. **House Rule vs Ruling vs ephemeral adjudication.** Their semantic adoption/lifecycle roles are distinct without requiring separate execution subsystems.
7. **Live adjudication != policy adoption.** A lawful one-off ruling can resolve play without campaign-wide publication; durable precedent requires explicit authorized adoption.
8. **Conflict is explicit.** Same-precedence material conflict cannot be resolved by hidden model preference.
9. **Decision-specific information eligibility.** Step-4/R2.3 remains deny-by-default for role/consumer/purpose; physical one-context presence grants no eligibility.
10. **Instruction/data fencing.** Admitted House Rule text is scoped gameplay-policy data below R2.4 constitutional instruction authority.
11. **Bounded retrieval.** R2.3 owns discovery/closure/currentness/eligibility; derived indexes/caches are routing only.
12. **Inherited publication/currentness.** Step-5.6/5.8 and R2.5 own authoritative publication/current-source/multiplayer semantics; no chat-copy propagation model exists.
13. **Historical stability.** Step-5.7 recovery preserves already accepted/frozen policy-dependent inputs while new work uses current policy.
14. **Finite realization gap.** Missing deterministic capability never authorizes direct LLM mutation.
15. **Optional promotion.** Semantic policy may remain prose indefinitely; formalizable mechanics may promote without duplicate execution ownership.
16. **Bounded ordinary-turn performance.** House Rules adds no baseline requirement for unnecessary repository/network round trips, full scans or extra LLM passes.

---

# 6. Adversarial disposition

Step 6 closed with:

```text
BLOCKER:    0 OPEN
SIGNIFICANT: 0 OPEN
MINOR:      1 OPEN / NONBLOCKING / PRE-EXISTING NAVIGATION DEBT
```

The MINOR concerns the absent convenience path:

- `DEV/ARCHITECTURE/CONTEXT_RUNTIME.md`

The actual semantic owner is present and explicit:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`

This is documentation/navigation maintenance debt only. House Rules does not duplicate or reconstruct R2.3 to compensate.

---

# 7. Navigation and durable cursor

Navigation addendum:

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX_HOUSE_RULES_ADDENDUM.md`

Program status/sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Durable R2.7 pause cursor:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

These now route the program to the explicit boundary:

```text
HOUSE RULES: COMPLETE / CANONICAL
S6D: NEXT / PREPARED / NOT STARTED
R2.7 WP-06: PAUSED
```

The immutable pre-pause R2.7 obligation checkpoint remains:

```text
PRE_PAUSE_STATUS_BLOB_SHA: d486825dc5c9463b2e2159086e6c7102c3caf354
```

---

# 8. Downstream obligations, not activated work

The canonical House Rules owner creates downstream machine-realization obligations around:

- durable policy identity/lifecycle/current revision realization;
- R2.3 policy discovery profile(s)/routing metadata;
- typed accepted semantic-result/frozen-basis evidence;
- finite policy conflict/staleness/realization-gap behavior;
- deterministic capability coverage needed by supported promoted/hybrid rules;
- conformance tests listed in the canonical architecture owner.

Those obligations belong to later S6D/R2.7/implementation stages according to their existing scopes. This Step 8 does **not** implement them and does **not** start S6D.

---

# 9. Explicit stop gate

Owner requested a stop before S6D.

Therefore the post-canonicalization cursor is intentionally:

```text
HOUSE_RULES_DESIGN: CLOSED
HOUSE_RULES_IMPLEMENTATION: NOT STARTED
S6D_START_PREREQUISITE: SATISFIED
S6D_STATUS: NEXT / NOT STARTED
S6D_ACTIVE_TASK_OR_DOMAIN: NONE
R2_7_WP06: PAUSED
```

A later explicit continuation must begin the next S6D Task/Domain at **Step 1 — Architecture Task Brief**, using the S6D plan only as decomposition/coverage evidence, and must not resume WP-06 before S6D integrated closure.

---

# 10. Step-8 result

`HOUSE_RULES_EIGHT_STEP_CYCLE: COMPLETE`

`HOUSE_RULES_ARCHITECTURE: CANONICAL / CLOSED`

`S6D: STOPPED BEFORE START`

`R2_7_WP06: REMAINS PAUSED`
