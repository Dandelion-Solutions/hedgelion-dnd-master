# R2.6 — MVP Behavioral Assurance / Post-Implementation Evaluation — Owner Clarification

Status: **OWNER-APPROVED ARCHITECTURE PROGRAM CLARIFICATION**

Date: 2026-08-24

Purpose:

> Clarify the MVP assurance standard for single-context information containment and move production-like behavioral evaluation to the implemented MVP, where the actual runtime/context/instruction topology exists to be tested.

This clarification refines R2.6 sequencing and acceptance scope. It does not reopen the owner-approved single-context architecture, Step-4 eligibility law, R2.4 TurnEnvelope, R2.5 multiplayer semantics, or the fixed repository transport.

---

# 1. Owner decision

For the HDM MVP, the required information-boundary guarantee is **observable behavioral containment**, not physical or cognitive isolation.

The model may physically receive information that is ineligible for the active logical role. The MVP is acceptable when the active role and player-visible output do not materially use or disclose that information before lawful eligibility.

The internal mechanism by which the model achieves this result is outside the HDM correctness contract. In particular, it is acceptable if the model effectively suppresses, ignores, down-weights, or otherwise does not use physically present ineligible context while performing the active role.

HDM SHALL NOT claim that ineligible information is absent from hidden model cognition.

---

# 2. Lawful information must remain usable

Behavioral containment must not become universal forgetting.

When information becomes lawfully eligible to an Actor/Narrator/other role through the owning evidence/context path, the role should be able to use it normally.

Existing HDM Lab role-containment evidence already supports this property strongly enough for architecture continuation:

- hidden information remained behaviorally contained in the tested scenarios;
- lawfully disclosed information was subsequently used by the applicable roles;
- Protocol 3 recorded full expected uptake on its witness-scored lawful-update channel;
- multi-Actor dialogue preserved public transfer while withholding private transfer.

R2.6 does not require another pre-implementation abstract experiment merely to prove the same mechanism again.

Exact runtime/instruction wording that reinforces both sides of this contract belongs to R2.7 machine/instruction mapping and implementation/TDD.

Candidate instruction-level semantic rule:

```text
Use only information eligible to the active role under the current RoleContextBundle and lawful typed handoffs.
Physical presence elsewhere in the conversation does not make information eligible.
When information later becomes lawfully eligible, use it normally; prior ineligibility is not permanent forgetting.
```

The exact owning CORE file(s), wording and tests are not selected by this clarification.

---

# 3. Production-like tests move after MVP implementation

The owner explicitly rejects making the full Protocol-4 production-like corpus a prerequisite for R2.7 architecture work.

Reason:

> Abstract pre-implementation testing cannot faithfully exercise many of the actual failure modes without recreating substantial parts of the MVP runtime, context assembler, persistence behavior, multiplayer coordination and instruction stack inside the test harness. At that point the test harness becomes a parallel MVP rather than evidence about the real implementation.

Therefore:

```text
R2.6 architecture assurance
    -> R2.7 machine/instruction/test mapping
    -> implementation planning
    -> MVP implementation (TDD)
    -> production-like Protocol-4-derived acceptance/evaluation on the real MVP
```

Protocol 4 remains valuable as a **test-design inventory and acceptance corpus source**, not as a mandatory complete pre-R2.7 execution campaign.

---

# 4. What may still block R2.6 architecture closure

R2.6 may remain blocked only by a concrete architecture/host incompatibility already established by documentary evidence, existing empirical evidence, or a cheap bounded capability check that does not require constructing the MVP.

Examples:

- an approved semantic boundary is known to be physically impossible on the selected ordinary ChatGPT profile;
- the fixed required GitHub Connector capability is absent;
- a mandatory player-visible host surface is known to unavoidably disclose Narrator-ineligible raw campaign material;
- an accepted R2.1-R2.5 contract is internally contradictory under the selected host topology;
- a current host limitation requires a genuine owner-level product trade-off before machine realization can be mapped.

Unknown empirical failure rates, long-chat quality, classifier accuracy or realistic integrated behavior are **not** architecture blockers by themselves when they can only be meaningfully measured on the implemented MVP.

---

# 5. What becomes post-implementation MVP acceptance

At minimum, implementation/evaluation must later exercise the real MVP for:

- final Dramaturg/Actor/Narrator/Chronicler containment;
- lawful post-disclosure uptake;
- local/shared Dramaturg horizon -> Narrator/catch-up secrecy;
- Project-memory/stale ambient context vs current routed owners;
- instruction/data/role-switch injection;
- Narrator / `EMISSION_COMMIT` behavior and mandatory visible auxiliary surfaces;
- context pressure, `ASSEMBLED_DEGRADED`, `UNSATISFIABLE`, and estimator calibration;
- Chronicler first-safe-opportunity anti-starvation;
- multiplayer agency barrier and maximal-safe-frontier behavior;
- stale collaboration generation and join/rejoin;
- two-level Dramaturg coherence and shared-horizon conflict/rebase;
- fixed Connector-path currentness/CAS failures where retained evidence is insufficient;
- Retry/regeneration no-replay behavior;
- supported reasoning-profile regression where needed.

A material observed failure at that stage is not ignored. It becomes an MVP release blocker, implementation defect, supported-profile restriction, or explicit architecture reopen depending on root cause.

---

# 6. Experiment repository boundary

Exploratory probes, frozen experimental fixtures, raw transcripts, prototype harnesses and instrumentation belong in **HDM Lab** by default.

Public HDM receives only independently rewritten/sanitized durable conclusions, canonical architecture, test obligations and implementation-facing contracts.

No experimental branch or probe mutation is authorized in public HDM by this clarification.

---

# 7. R2.6 consequence

R2.6 should now close on an **MVP host-assurance contract**, not on completion of the entire Protocol-4 behavioral corpus.

Closure requires:

1. the observable behavioral-containment MVP guarantee is explicit;
2. no physical/cognitive isolation guarantee is claimed;
3. existing Protocols 1-3 are accepted as sufficient pre-implementation evidence for role-containment feasibility and lawful uptake;
4. current host/documentary evidence reveals no known architecture blocker;
5. fixed Connector-path prerequisites remain explicit and closed to alternative transport selection;
6. degradation/unsupported behavior is defined rather than silently weakening semantics;
7. deferred Protocol-4-derived scenarios are mapped into R2.7 and post-implementation MVP acceptance;
8. any unresolved question requiring actual integrated runtime behavior is classified as downstream evaluation rather than an abstract architecture prerequisite.

If those conditions hold after adversarial review, R2.6 may close and R2.7 may begin.
