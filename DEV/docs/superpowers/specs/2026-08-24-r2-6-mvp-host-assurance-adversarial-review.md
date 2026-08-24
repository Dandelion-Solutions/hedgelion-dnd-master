# R2.6 — MVP Host Assurance — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE SURVIVES WITH AMENDMENTS**

Date: 2026-08-24

Reviewed candidate:

- `2026-08-24-r2-6-mvp-host-assurance-candidate-spec.md`

Owner clarification:

- `2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`

Question:

> Does moving production-like behavioral testing after MVP implementation hide a known architecture blocker, weaken information-boundary semantics, or merely move empirical reliability measurement to the first point where the actual integrated system exists?

Verdict:

> **The candidate survives. No new owner trade-off is required.**

The review found no current evidence that the accepted ChatGPT Plus / ordinary-chat / one-context topology is architecturally impossible. It did identify several wording and downstream-gating requirements that must be explicit in the canonical spec.

---

# AR-1 — “Behavioral containment” must not be misread as best-effort secrecy

Attack:

> If the architecture stops requiring physical/cognitive isolation, can an observed secret leak simply be dismissed as an expected model imperfection?

Finding:

No. The MVP guarantee is behavioral, but that behavior is still correctness-critical.

Required amendment:

- no claim about hidden cognition;
- but a material observed ineligible use/reveal in the implemented supported profile is a release/support blocker until resolved/classified;
- “behavioral” describes the observable contract, not a permission to knowingly ship recurrent leaks.

Disposition: **AMEND**.

---

# AR-2 — Over-suppression could make NPCs permanently ignorant

Attack:

> A model might satisfy hidden-fact tests by suppressing the fact even after it becomes eligible.

Evidence:

Retained Protocols 1-3 include lawful eligibility/update controls; Protocol 3 recorded full expected uptake on its witness-scored lawful-update channel and manual review found the same semantic pattern elsewhere.

Finding:

This is already sufficient feasibility evidence for architecture continuation. The real MVP must still retain lawful-uptake tests.

Required amendment:

- canonicalize “prior ineligibility is not permanent forgetting”;
- R2.7 maps this into CORE/instruction/test obligations.

Disposition: **AMEND / NO BLOCKER**.

---

# AR-3 — Deferring Protocol 4 could recreate the test/implementation gap later

Attack:

> If Protocol 4 is simply postponed, implementation may finish without anyone executing it.

Finding:

Valid process risk, not architecture blocker.

Required amendment:

- Protocol-4-derived scenarios must become explicit R2.7 machine/test obligations;
- implementation planning must map them to TDD/integration/evaluation suites;
- MVP release/readiness cannot claim supported behavioral containment without executing the mapped production-like tests.

Disposition: **AMEND**.

---

# AR-4 — A pre-MVP harness might still reveal a blocker cheaply

Attack:

> Some bounded probe could expose a fatal host limitation without building the whole MVP. Should all pre-implementation probes be banned?

Finding:

No. The owner clarification only rejects the full abstract production-like corpus as a prerequisite.

Cheap bounded checks remain valid when they answer a concrete architecture question without recreating runtime machinery.

Required amendment:

- distinguish `CHEAP CAPABILITY CHECK` from `INTEGRATED BEHAVIORAL ACCEPTANCE`;
- the former may still occur during architecture if a concrete blocker question appears;
- experiments/prototypes remain in Lab.

Disposition: **AMEND**.

---

# AR-5 — Mandatory visible host/tool surface could bypass Narrator

Attack:

> Even perfect Narrator behavior does not help if a mandatory Connector/tool/approval card exposes raw secret-bearing payload to the player.

Finding:

This remains a real deployment risk, but no current evidence establishes that such unsafe exposure is unavoidable in the selected configuration.

Required amendment:

- no intentional secret-bearing payload in auxiliary surfaces;
- R2.7 maps a deployment/UI acceptance test with synthetic canaries;
- if an unavoidable unsafe surface is later demonstrated, classify that profile unsupported/restricted or reopen the boundary.

Disposition: **POST-IMPLEMENTATION / DEPLOYMENT GATE, NO CURRENT BLOCKER**.

---

# AR-6 — Project memory can inject stale/foreign context

Attack:

> Ambient Project/chat memory may reintroduce old facts despite repository currentness.

Finding:

This is exactly the single-context law: physical presence is not eligibility or authority.

Existing containment evidence makes the architecture plausible; integrated memory contamination must be tested on the actual MVP/configuration.

Required amendment:

- ambient host memory never becomes authority;
- Project-only memory may be a recommended narrowing setting, not correctness dependency;
- stale-memory-vs-current-owner scenario remains mandatory acceptance coverage.

Disposition: **NO BLOCKER / DOWNSTREAM TEST**.

---

# AR-7 — Context pressure may invalidate role containment at realistic scale

Attack:

> Long chats and realistic campaign packets may weaken role discipline or force hidden truncation.

Finding:

R2.3 already defines the architecture-level response: bounded lazy loading, required floors, degradation, finite `UNSATISFIABLE`.

Exact failure rates and calibration require the implemented packet assembler and therefore are downstream.

Required amendment:

- no silent required-context truncation remains a release-blocking failure;
- estimator/long-chat calibration is implementation/evaluation work.

Disposition: **NO BLOCKER / DOWNSTREAM TEST**.

---

# AR-8 — Chronicler anti-starvation cannot be validated without an integrated TurnEnvelope

Attack:

> Pre-implementation testing of first-safe-opportunity service either mocks scheduling or rebuilds the TurnEnvelope.

Finding:

Agreed. R2.4 semantics are closed; the meaningful test needs real workload/budget/currentness behavior.

Required amendment:

- retain anti-starvation acceptance scenarios;
- do not hold R2.7 hostage to a synthetic parallel scheduler.

Disposition: **DOWNSTREAM TEST**.

---

# AR-9 — Multiplayer agency tests require real shared currentness

Attack:

> Maximal-safe-frontier and stale-generation behavior cannot be validated faithfully if the test does not have the actual collaboration/currentness records selected in R2.7.

Finding:

Correct. An abstract test would either omit the decisive machinery or implement a provisional version that R2.7 may later change.

Required amendment:

- R2.7 must map generation IDs, currentness owners, collaboration records and test fixtures before production-like multi-chat evaluation;
- later evaluation uses two independent participant chats over the actual mapped campaign state.

Disposition: **DOWNSTREAM TEST**.

---

# AR-10 — Two-level Dramaturg coherence tests can become a parallel narrative engine

Attack:

> A rich pre-MVP Dramaturg harness risks implementing shared/local planning storage, discovery, CAS and rebase purely to test them.

Finding:

This is the strongest argument for deferral.

Required amendment:

- do not build a second planning implementation in Lab merely to precede the real one;
- Lab may hold synthetic fixtures/evaluators, while the real production-like test runs against the mapped MVP.

Disposition: **DOWNSTREAM TEST / AVOID PARALLEL MVP**.

---

# AR-11 — S53 could still require exact model equality for multiplayer fairness

Attack:

> Different reasoning profiles could produce materially different quality or strictness, so perhaps every player must use exactly the same model.

Finding:

Current product behavior does not make exact serving identity a robust semantic primitive, and Protocol 3 already showed containment across tested reasoning profiles.

Fairness/quality differences are deployment-quality concerns unless they cross correctness criteria.

Required amendment:

- capability/behavior envelope remains the canonical S53 resolution;
- exact shared serving identity stays out of campaign state;
- profile-specific correctness failures later restrict that profile.

Disposition: **NO BLOCKER**.

---

# AR-12 — Retry / sibling behavior might need architecture before MVP

Attack:

> If Retry repeatedly creates bad trajectories, delaying D15 could make the MVP architecture incomplete.

Finding:

The trigger has not fired. Step-5.12 already protects accepted gameplay from Retry replay.

Required amendment:

- D15 remains dormant;
- later Retry evaluation may activate it only on its preserved trigger.

Disposition: **NO BLOCKER**.

---

# AR-13 — Fixed Connector path may need revalidation but not reselection

Attack:

> If final record mapping changes call shape/currentness pressure, perhaps transport must be re-explored now.

Finding:

No. Transport selection is closed. R2.7 may map actual publication envelopes and later integration tests may expose capability/latency defects, but no alternative runtime transport is permitted.

Required amendment:

- missing selected Connector primitive is a profile blocker;
- failure does not authorize `gh`/native Git/direct API/MCP fallback experiments.

Disposition: **NO BLOCKER / FIXED PATH**.

---

# AR-14 — Public HDM must not become the experiment workspace

Attack:

> Deferring tests could tempt implementation-time probes/temporary branches in the public repository.

Finding:

This is a governance risk proven by the accidental `probe-temp` incident, not an architecture requirement.

Required amendment:

- exploratory probes/raw fixtures/instrumentation belong in HDM Lab by default;
- public HDM gets sanitized durable test contracts/results only;
- no probe branch creation in public HDM absent explicit owner approval under `AGENTS.md`.

Disposition: **AMEND**.

---

# 15. Required canonical amendments

The canonical R2.6 spec must add/retain all of the following:

1. Behavioral containment remains a correctness guarantee, not best-effort prose quality.
2. No physical/cognitive isolation claim.
3. Lawful eligibility restores normal usability; prior suppression is not permanent forgetting.
4. Protocols 1-3 are sufficient feasibility evidence for architecture continuation.
5. Full Protocol-4 execution is post-implementation MVP acceptance, not R2.7 prerequisite.
6. Cheap bounded capability checks remain allowed when a concrete architecture blocker question exists.
7. Protocol-4-derived scenarios must be mapped in R2.7 and implementation planning; they may not disappear.
8. Mandatory auxiliary surfaces must be evaluated with non-secret synthetic canaries on the real deployment.
9. Ambient host memory is never campaign authority/currentness/knowledge/disclosure.
10. Context-pressure calibration occurs on the implemented Context Runtime; required semantic floors may never be silently dropped.
11. Chronicler/multiplayer/Dramaturg production-like evaluation uses the actual integrated MVP.
12. S53 resolves to a capability/behavior envelope, not exact cross-player model identity.
13. D15 remains dormant pending its exact Retry trigger.
14. Experiments/prototypes/instrumentation belong in HDM Lab by default; public HDM remains clean.

---

# 16. Final review verdict

No evidence currently establishes a host-level incompatibility that requires R2.6 to stay open before R2.7.

The strongest remaining uncertainties are implementation/evaluation questions whose meaningful test requires artifacts that R2.7 has not yet mapped and the MVP has not yet implemented.

Therefore:

> **R2.6 may proceed to canonicalization and closure with the fourteen amendments above. No new human product decision is required.**
