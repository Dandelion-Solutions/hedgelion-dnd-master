# R2.6 — MVP Host Assurance — Candidate Specification

Status: **CANDIDATE SPECIFICATION — PRE-ADVERSARIAL**

Date: 2026-08-24

Purpose:

> Define the minimum host-assurance contract required to close R2.6 and enter R2.7 without requiring an abstract pre-implementation test harness to recreate the MVP.

This candidate is based on:

- owner-approved ChatGPT Plus / ordinary-chat baseline;
- R2.1-R2.5 canonical architecture;
- Step-5.12 emission/disclosure law;
- fixed Python/core-prepared + GitHub Connector repository path;
- Protocols 1-3 retained role-containment evidence;
- current first-party host evidence already synthesized in R2.6;
- `2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`.

No implementation is authorized by this candidate.

---

# 1. Supported MVP host profile

Baseline deployment profile:

```text
host                     ChatGPT
plan                     ChatGPT Plus
surface                  ordinary Project-capable chat
per-player topology      one human -> own physical chat/context
ordinary gameplay        one user request -> one assistant turn
reasoning recommendation High when available
exact model identity     not campaign semantics
repository path          deterministic Python/core + fixed GitHub Connector
```

Exact serving-model equality across multiplayer participants is not required.

Campaign authority remains repository/native semantic owners. Project/chat memory is ambient physical context only.

---

# 2. MVP information-boundary contract

## LAW R2.6-1 — BEHAVIORAL CONTAINMENT IS THE MVP GUARANTEE

HDM MVP requires observable behavioral information containment.

An active Actor, Narrator or other logical role SHALL NOT materially use or disclose information that is not eligible under its current role/context/handoff contract merely because that information is physically present elsewhere in the ChatGPT conversation.

HDM does not claim physical or cognitive isolation.

## LAW R2.6-2 — CONTAINMENT MECHANISM IS OUT OF CONTRACT

The internal model mechanism used to achieve containment is not an HDM correctness property.

Suppression, ignoring, down-weighting or other internal handling of physically present ineligible information is acceptable if observable role behavior remains compliant.

## LAW R2.6-3 — LAWFUL UPTAKE MUST WORK

Once information becomes lawfully eligible through the owning context/evidence path, prior ineligibility SHALL NOT make it permanently unavailable.

Roles may and should use newly eligible information normally when relevant.

Protocols 1-3 provide sufficient pre-implementation feasibility evidence for this architecture-stage conclusion. Production-specific reliability remains a post-implementation acceptance concern.

---

# 3. Instruction realization handoff

R2.7 SHALL map an explicit instruction-level rule equivalent to:

```text
Use only information eligible to the active role under the current RoleContextBundle and lawful typed handoffs.
Physical presence elsewhere in the conversation does not make information eligible.
When information later becomes lawfully eligible, use it normally; prior ineligibility is not permanent forgetting.
```

Exact owning CORE file(s), phrasing, module activation and test IDs remain R2.7/implementation work.

This rule must compose with:

- Step-4 role-context/knowledge/disclosure law;
- R2.3 Context Runtime;
- R2.4 role rebinding and typed handoffs;
- R2.5 local/shared Dramaturg horizons;
- Step-5.12 Narrator/recipient disclosure boundary.

---

# 4. Narrator / emission host realization

## LAW R2.6-4 — PRE-NARRATOR SEMANTIC ADMISSION IS THE BASELINE

The ordinary ChatGPT baseline realizes Step-5.12 through:

```text
accepted/current state
-> deterministic/typed recipient + source + material-reveal admission
-> fresh Narrator rebind to an eligible RoleContextBundle
-> supported player-visible response representation
-> EMISSION_COMMIT
-> ordinary host output path
```

No byte-exact post-render outbox/interceptor is required by the MVP architecture.

## LAW R2.6-5 — AUXILIARY SURFACES MAY NOT BE INTENTIONAL SECRET CHANNELS

Tool/debug/Connector/progress surfaces SHALL NOT intentionally carry Narrator-ineligible campaign information for the player.

Whether a particular current host card exposes unsafe raw payload is an implementation/deployment acceptance question unless documentary/current evidence already proves it unavoidable.

If later integrated evaluation proves a mandatory surface necessarily exposes protected material, the affected profile is restricted/unsupported or architecture is explicitly reopened.

---

# 5. Project memory / ambient host context

## LAW R2.6-6 — AMBIENT HOST MEMORY HAS NO CAMPAIGN AUTHORITY

Chat history, Project memory and other ambient host context:

```text
!= campaign canon
!= currentness evidence
!= Actor knowledge
!= player disclosure evidence
!= collaboration generation
!= Story coverage
```

Current routed owners and logical eligibility win over ambient stale/conflicting context.

Project-only memory may be recommended later as contamination reduction, but correctness does not depend on it.

---

# 6. Context/resource envelope

## LAW R2.6-7 — NO EXACT HIDDEN-CAPACITY DEPENDENCY

HDM SHALL NOT require an exact consumer-ChatGPT remaining-context/token telemetry contract that the host does not expose.

Physical realization uses:

- one central conservative/approximate estimator;
- required representation floors;
- bounded lazy loading;
- `ASSEMBLED_DEGRADED`;
- finite `UNSATISFIABLE` fallback.

Estimator calibration and realistic long-chat behavior are post-implementation evaluation concerns.

A later measured estimator defect may degrade quality/efficiency; it may not authorize silent omission of required semantics.

---

# 7. Reasoning/model profile — S53 resolution

## LAW R2.6-8 — CAPABILITY ENVELOPE, NOT EXACT SERVING IDENTITY

Supported multiplayer does not require identical model IDs or reasoning settings across participant chats.

Baseline policy:

```text
recommended profile        High reasoning when available
exact shared model ID      not required
exact shared reasoning     not required
campaign-persisted model   not required
required property          each participant host satisfies the supported HDM behavioral/capability envelope
```

If post-implementation evaluation shows a specific profile cannot satisfy correctness-critical behavior, that profile is degraded/unsupported rather than changing campaign semantics.

S53 is therefore resolved as a minimum supported capability/behavior envelope.

---

# 8. Fixed repository-path assurance

## LAW R2.6-9 — TRANSPORT SELECTION REMAINS CLOSED

Supported remote repository path remains:

```text
deterministic Python/core preparation
-> GitHub Connector Git-data/ref operations
-> non-force authoritative ref transition
```

R2.6/R2.7/implementation SHALL NOT probe or fall back to `gh`, remote native Git, direct private HTTP/API/token workarounds, custom MCP/backend alternatives or GitHub Actions as gameplay transport.

Missing required Connector capability is a supported-profile capability failure.

Retained prior transport evidence is reused where it already answers stable primitives. Integrated currentness/CAS regression belongs to implementation acceptance where actual mapped record families exist.

---

# 9. Chronicler / multiplayer / planning assurance timing

The following canonical semantics remain unchanged:

- Chronicler first-safe-opportunity service;
- no same-envelope Story feedback;
- agency-safe maximal frontier;
- no transport-order fiction;
- recipient catch-up;
- local + multiplayer-only shared Dramaturg horizons;
- preparation has no entitlement to occur;
- shared-horizon current-generation/CAS/rebase semantics.

R2.6 does not require complete abstract production-like execution of these systems before R2.7.

## LAW R2.6-10 — INTEGRATED BEHAVIOR IS TESTED ON THE INTEGRATED MVP

Production-like validation of these interacting behaviors SHALL be performed on the implemented MVP because meaningful evaluation requires the actual Context Runtime, TurnEnvelope, persistence/currentness mapping, instruction assets and multiplayer record realization.

Protocol 4 remains the primary scenario inventory/input for those tests.

---

# 10. Post-implementation acceptance handoff

R2.7 and the later implementation plan SHALL preserve explicit test obligations for at least:

1. hidden role information remains behaviorally contained;
2. lawfully eligible information is subsequently usable;
3. Dramaturg/Actor/Chronicler -> Narrator containment;
4. local/shared planning -> Narrator/catch-up containment;
5. stale ambient Project/chat context loses to current routed owners;
6. instruction-like data does not self-promote;
7. Narrator/`EMISSION_COMMIT` and visible auxiliary-surface safety;
8. context-pressure degradation and `UNSATISFIABLE`;
9. Chronicler anti-starvation;
10. multiplayer agency/maximal-safe-frontier scenarios;
11. stale generation/join-rejoin;
12. shared-horizon conflict/rebase and no-plot-restoration;
13. fixed Connector currentness/CAS/failure regression;
14. Retry/regeneration without accepted gameplay replay;
15. supported reasoning-profile regression when needed.

Exploratory fixtures/raw run evidence belong in HDM Lab. Public HDM holds only sanitized test obligations and promoted conclusions.

---

# 11. Architecture-stage blocking rule

## LAW R2.6-11 — ONLY KNOWN HOST/ARCHITECTURE INCOMPATIBILITY BLOCKS R2.7

R2.6 blocks R2.7 only when current evidence establishes a concrete incompatibility requiring architecture/product action before machine realization.

Examples:

- approved semantics are known impossible on the selected host;
- fixed required Connector capability is absent;
- a mandatory host surface is known unavoidably unsafe;
- an upstream contract is contradictory under the selected topology;
- a material owner trade-off must be resolved before mapping.

Unknown integrated failure rates or quality variation that can only be measured after implementation do not justify constructing a parallel MVP test harness before R2.7.

---

# 12. Candidate closure disposition

Current evidence shows no known architecture-level blocker requiring R2.6 to remain open:

- Protocols 1-3 support behavioral containment and lawful uptake sufficiently for architecture feasibility;
- single-context physical co-presence is an accepted product assumption, not a newly discovered contradiction;
- Step-5.12 requires a logical `EMISSION_COMMIT`, not a byte-exact outbox;
- R2.3 already defines graceful context degradation without exact telemetry;
- current configured Connector supplies the selected repository operations and transport selection is closed;
- S53 can be resolved without exact cross-player model equality;
- D15 remains dormant;
- R2.4/R2.5 integrated reliability questions are meaningful post-implementation acceptance work.

Recommendation: **advance this candidate through adversarial review; if no concrete host incompatibility emerges, close R2.6 and enter R2.7.**
