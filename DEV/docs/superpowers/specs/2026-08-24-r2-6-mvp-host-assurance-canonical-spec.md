# R2.6 — MVP Host Assurance — Canonical Specification

Status: **CANONICAL — R2.6 ARCHITECTURE ASSURANCE CLOSED PENDING RESOLUTION GATE**

Date: 2026-08-24

Canonicalization basis:

- `../design/2026-08-24-r2-6-chatgpt-plus-assurance-task-brief.md` — task scope, refined by later owner clarifications;
- `../design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`;
- `2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`;
- `../design/2026-08-24-r2-6-current-host-assurance-synthesis.md`;
- `../design/2026-08-24-r2-6-production-like-assurance-protocol.md`;
- `../design/2026-08-24-r2-6-protocol-4-frozen-fixture-contract.md`;
- `../design/2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`;
- `../design/2026-08-24-r2-6-mvp-host-assurance-candidate-spec.md`;
- `../design/2026-08-24-r2-6-mvp-host-assurance-adversarial-review.md`;
- retained Protocols 1-3 role-containment evidence.

Owner-approved direction:

> **For the MVP, HDM requires observable behavioral containment, not physical/cognitive isolation. Production-like integrated evaluation belongs on the implemented MVP rather than in a pre-implementation parallel harness.**

This specification closes the architecture-stage host-assurance contract. It does not claim that downstream MVP acceptance tests have already executed.

---

# 1. Supported MVP host profile

Baseline:

```text
primary host              ChatGPT
plan                      ChatGPT Plus
surface                   ordinary Project-capable chat
per-player physical use   one human -> own chat/context
ordinary execution        one user request -> one assistant turn
reasoning recommendation  High when available
repository remote path    deterministic Python/core + fixed GitHub Connector
```

Campaign semantics and persistence do not depend on exact serving-model identity or equal reasoning settings across players.

---

# 2. Information-boundary guarantee

## LAW R2.6-1 — BEHAVIORAL CONTAINMENT IS CORRECTNESS

The MVP information-boundary guarantee is observable behavioral containment.

An active role and player-visible output SHALL NOT materially use or disclose information that is ineligible under the current role/context/handoff contract merely because that information is physically present elsewhere in the ChatGPT conversation.

A material observed ineligible use/reveal in the supported implemented profile is a correctness/release-support failure until resolved or explicitly classified. “Behavioral” does not mean best effort.

## LAW R2.6-2 — NO PHYSICAL/COGNITIVE ISOLATION CLAIM

HDM does not claim that ineligible information is absent from hidden model cognition or from the physical conversation context.

The internal mechanism by which the model achieves compliant behavior is outside the HDM correctness contract.

Suppression, ignoring, down-weighting or other internal handling is acceptable when the observable role contract is satisfied.

## LAW R2.6-3 — LAWFUL ELIGIBILITY RESTORES NORMAL USE

Prior ineligibility is not permanent forgetting.

When information becomes lawfully eligible through the owning evidence/context/handoff path, the applicable role SHALL be allowed to use it normally when relevant.

Protocols 1-3 provide sufficient pre-implementation feasibility evidence for both containment and lawful uptake to continue architecture work.

---

# 3. Instruction realization

R2.7 SHALL map an explicit shipped instruction/CORE behavior equivalent to:

```text
Use only information eligible to the active role under the current RoleContextBundle and lawful typed handoffs.
Physical presence elsewhere in the conversation does not make information eligible.
When information later becomes lawfully eligible, use it normally; prior ineligibility is not permanent forgetting.
```

Exact file ownership, wording, module activation and tests belong to R2.7 and implementation/TDD.

The rule must compose with Step-4 knowledge/disclosure, R2.3 Context Runtime, R2.4 rebinding/typed handoffs, R2.5 Dramaturg horizons and Step-5.12 recipient disclosure.

---

# 4. Narrator / `EMISSION_COMMIT`

## LAW R2.6-4 — PRE-NARRATOR SEMANTIC ADMISSION IS THE BASELINE REALIZATION

Supported baseline:

```text
accepted/current state
-> deterministic/typed recipient + source + material-reveal admission
-> fresh Narrator rebind to eligible RoleContextBundle
-> supported player-visible response representation
-> EMISSION_COMMIT
-> ordinary host output path
```

Step-5.12 does not require a byte-exact post-render outbox/interceptor for the MVP.

## LAW R2.6-5 — AUXILIARY SURFACES ARE NOT SECRET DELIVERY CHANNELS

Tool/debug/Connector/progress/approval surfaces SHALL NOT intentionally carry Narrator-ineligible campaign information for the player.

The implemented deployment must be evaluated with non-secret synthetic canaries where the assistant cannot inspect rendered UI directly.

If an unavoidable mandatory host surface later proves to expose protected material, the affected deployment profile is restricted/unsupported or the relevant architecture boundary is explicitly reopened.

---

# 5. Ambient Project/chat context

## LAW R2.6-6 — HOST MEMORY HAS NO CAMPAIGN AUTHORITY

Chat history, Project memory and other ambient host context:

```text
!= campaign canon
!= currentness evidence
!= Actor knowledge
!= human disclosure evidence
!= collaboration generation
!= Story coverage
```

Current routed semantic owners and role eligibility win over stale/conflicting ambient context.

Project-only memory may later be recommended as contamination reduction, but correctness cannot depend on it.

---

# 6. Context/resource behavior

## LAW R2.6-7 — NO EXACT HIDDEN-CAPACITY DEPENDENCY

HDM does not require exact remaining-context/token telemetry that consumer ChatGPT does not expose as a stable contract.

Physical realization uses:

- one central conservative/approximate estimator;
- R2.3 bounded lazy loading;
- required representation floors;
- optional degradation;
- `ASSEMBLED_DEGRADED`;
- finite `UNSATISFIABLE` fallback.

Estimator calibration and long-chat reliability are measured on the implemented MVP.

A later estimator error may affect quality or efficiency but never authorizes silent removal of required semantic evidence.

---

# 7. S53 — serving/profile semantics

## LAW R2.6-8 — SUPPORTED CAPABILITY ENVELOPE, NOT EXACT CROSS-PLAYER MODEL ID

Baseline multiplayer policy:

```text
recommended reasoning       High when available
exact shared model identity not required
exact shared reasoning      not required
campaign-persisted model ID not required
required property           each participant host satisfies the supported HDM behavioral/capability envelope
```

If later integrated evaluation shows a specific reasoning/profile class violates correctness-critical behavior, classify that profile degraded/unsupported rather than changing campaign semantics.

S53 is resolved by this capability/behavior-envelope contract.

---

# 8. Fixed repository transport

## LAW R2.6-9 — TRANSPORT SELECTION IS CLOSED

Supported remote repository path remains:

```text
deterministic Python/core preparation
-> GitHub Connector Git-data/ref operations
-> non-force authoritative ref transition
```

No runtime probing/fallback/comparison of:

- `gh`;
- remote native Git;
- direct private HTTP/API/token workarounds;
- custom MCP/backend write alternatives;
- GitHub Actions as gameplay bridge;
- transparent local-commit push.

Missing required Connector capability is a supported-profile capability failure.

Retained transport evidence is reused for stable primitives. R2.7 maps actual publication envelopes; implementation acceptance tests their integrated currentness/CAS/failure behavior.

---

# 9. Architecture-stage vs post-implementation evidence

## LAW R2.6-10 — DO NOT BUILD A PARALLEL MVP TO TEST THE MVP

Production-like integrated evaluation of R2.4/R2.5 interactions SHALL run on the implemented MVP, because meaningful tests require the actual:

- Context Runtime;
- TurnEnvelope/instruction assets;
- persistence/currentness mapping;
- collaboration/generation records;
- local/shared Dramaturg horizon realization;
- Narrator/Chronicler wiring.

A pre-implementation harness that recreates these components is not required as an architecture gate.

## LAW R2.6-11 — CHEAP BLOCKER CHECKS REMAIN ALLOWED

R2.6 may still use a cheap bounded capability check when a concrete architecture-blocker question can be answered without reconstructing the MVP.

Exploratory probes, prototype harnesses, raw transcripts and instrumentation belong in HDM Lab by default.

Public HDM receives sanitized/promoted durable conclusions and implementation-facing test obligations.

---

# 10. Post-implementation MVP acceptance obligations

R2.7 and implementation planning SHALL preserve explicit production-like acceptance coverage for at least:

1. hidden role information remains behaviorally contained;
2. lawfully eligible information is subsequently usable;
3. Dramaturg/Actor/Chronicler -> Narrator containment;
4. local/shared Dramaturg planning -> Narrator/catch-up containment;
5. no same-envelope Story feedback;
6. stale/foreign ambient Project/chat context loses to current owners;
7. instruction-like data cannot self-promote into role/authority/source eligibility;
8. Narrator/`EMISSION_COMMIT` and visible auxiliary-surface safety;
9. context-pressure degradation, required floors and `UNSATISFIABLE`;
10. Chronicler first-safe-opportunity anti-starvation;
11. multiplayer false-positive/false-negative agency barrier behavior;
12. maximal-safe-frontier narration;
13. stale collaboration generation, join/rejoin and external-consent impersonation;
14. local/shared Dramaturg coherence, lazy retrieval and no global planning scan;
15. shared-horizon conflict/rebase and no-plot-restoration;
16. fixed Connector currentness/CAS/conflict/failure regression;
17. Retry/regeneration without mechanics/RNG/canon replay;
18. supported reasoning-profile regression when material.

MVP release/readiness SHALL NOT claim the supported behavioral-containment envelope until the mapped implementation/evaluation suite has executed and material failures are resolved/classified.

---

# 11. Blocking semantics

## LAW R2.6-12 — ONLY KNOWN HOST/ARCHITECTURE INCOMPATIBILITY BLOCKS R2.7

R2.6 blocks R2.7 only when current evidence establishes a concrete incompatibility requiring architecture/product action before machine realization.

Examples:

- accepted semantics are known physically impossible on the selected host;
- fixed required Connector capability is absent;
- a mandatory host surface is known unavoidably unsafe;
- an upstream contract is contradictory under the selected topology;
- a genuine owner trade-off must be resolved before mapping.

Unknown integrated failure rates, quality variance, long-chat calibration or classifier accuracy that can only be measured meaningfully on the real implementation are downstream acceptance concerns, not reasons to build a parallel MVP test system before R2.7.

---

# 12. Chronicler / multiplayer / Dramaturg handoff

The following upstream semantics are unchanged and proceed to machine mapping:

- Chronicler service obligation and first-safe-opportunity policy;
- no same-envelope Story feedback;
- agency-safe maximal frontier;
- no transport-order fiction;
- recipient catch-up;
- player-local + multiplayer-only shared Dramaturg horizons;
- preparation has no entitlement to occur;
- canon invalidates preparation;
- shared-horizon current-generation/exact-base fencing and semantic rebase.

Their reliability is an implementation/MVP acceptance question, not an unresolved R2.6 architecture question.

---

# 13. D15 disposition

D15 remains **CONDITIONAL / DORMANT**.

Retry/regeneration exists, but its preserved trigger has not fired. No rejected-sibling advisory memory is introduced.

Revisit only if production-like Retry evaluation on the implemented MVP repeatedly demonstrates the exact material failure class D15 was preserved to address.

---

# 14. Diamond / Strong disposition

- **S53 — RESOLVED:** minimum supported behavioral/capability envelope; High recommended; exact cross-player model/reasoning equality rejected as semantic requirement.
- **D15 — DORMANT:** Retry existence alone does not fire the trigger.
- **D16 / S21 / S28 — INHERITED:** logical invisible phases, non-authoritative steering and structural player-visible fencing remain R2.4 laws and become implementation acceptance coverage.
- **S14 — INHERITED ACTIVE from R2.5:** retained local/shared noncanonical planning remains; R2.6 does not redesign it.
- **S39 — DORMANT:** no stable prompt-cache contract warrants cache-specific architecture.

No other dormant Diamond/Strong item is activated by R2.6.

---

# 15. Canonical conclusion

Current documentary, retained empirical and target-environment evidence exposes no known host-level incompatibility that requires architecture redesign before R2.7.

R2.6 therefore closes the **architecture assurance** question as:

> **ChatGPT Plus / ordinary one-chat-per-player HDM is a supported MVP architecture candidate under an observable behavioral-containment contract, fixed Connector repository path, logical pre-Narrator admission, conservative context degradation and explicit downstream production-like acceptance testing.**

This is not a claim that MVP evaluation has already passed. It is the architectural contract under which R2.7 may map the real machine/instruction/test realization.
