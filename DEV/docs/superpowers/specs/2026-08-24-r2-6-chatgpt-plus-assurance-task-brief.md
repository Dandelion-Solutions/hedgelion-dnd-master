# R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation — Task Brief

Status: **ACTIVE TASK BRIEF — R2.6 IN PROGRESS**

Date: 2026-08-24

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Depends on:

- owner-approved ChatGPT Plus / ordinary public chat / one-user-request-one-assistant-turn baseline;
- R2.1 continuity/history architecture;
- R2.2 Actor continuity/cognition;
- R2.3 Context Runtime;
- R2.4 single-context TurnEnvelope/role containment/Chronicler service;
- R2.5 agency-safe multiplayer collaboration and Dramaturg coordination;
- Step-3 deterministic execution boundary;
- Step-4 truth/knowledge/disclosure/role-context law;
- Step-5 persistence/recovery/concurrency/emission boundaries.

No implementation is authorized by this brief.

---

## 1. Purpose

R2.6 is an **assurance stage**, not a new orchestration-design stage.

Its job is to determine which already-approved HDM semantics the current target host can realize reliably enough for the supported product profile:

```text
primary host          ChatGPT
plan                  ChatGPT Plus
surface               ordinary public chat / Project-capable workflow
per-player topology   one human -> own chat/context
multiplayer transport shared GitHub campaign/current frontiers
ordinary turn         one user request -> one assistant turn
```

For every material obligation, R2.6 must classify current support as:

```text
SUPPORTED
SUPPORTED_WITH_DOCUMENTED_LIMITATION
DEGRADED_MODE
UNSUPPORTED
```

If the host cannot realize a required semantic boundary, R2.6 must restrict/reject the deployment profile or explicitly reopen the affected architecture decision. It must not silently weaken upstream semantics.

---

## 2. Current evidence warning

The August-22 platform-feasibility research is routing/background evidence only. Product capabilities, model availability, app/plugin behavior and limits can change quickly.

R2.6 SHALL reverify time-sensitive host claims against:

1. current first-party product documentation where available;
2. the actual current target ChatGPT environment through bounded capability probes where documentation is insufficient;
3. existing HDM Protocols 1–3 for behavioral containment evidence;
4. new production-like HDM regression probes derived from R2.3–R2.5.

Do not treat old comparative host claims as current truth without revalidation.

---

## 3. Task-specific Source Manifest

### 3.1 Process / sequencing

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

### 3.2 Current canonical obligations

- Round-1 closure / Round-2 rebaseline owner decision;
- Step-4 single-context role-containment canonical amendment;
- R2.1 canonical continuity specification;
- R2.2 canonical Actor specification;
- R2.3 canonical Context Runtime specification + resolution gate;
- R2.4 canonical TurnEnvelope specification + resolution gate;
- R2.5 canonical multiplayer collaboration specification + resolution gate;
- Step-5.4 host lifecycle/handoff;
- Step-5.8 multiplayer/live currentness;
- Step-5.12 host delivery/disclosure boundary;
- Step-5.14 integrated recovery/concurrency closure.

### 3.3 Existing empirical/research evidence

- `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-comparative-research.md`
- `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-economic-profile-amendment.md`
- `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md`
- `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`
- `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-3-reasoning-budget.md`
- any retained protocol fixtures/results needed to reproduce or extend the tested channels;
- current R2.3/R2.4/R2.5 adversarial scenarios and assurance handoffs.

### 3.4 Current first-party host documentation

R2.6 evidence extraction must recheck current official documentation for at least:

- ChatGPT Plus model/tool availability and the fact that model availability/limits change over time;
- Projects: project instructions, project files/context, tool availability and Plus file limits;
- Apps/Plugins: search/fetch/write-action capability classes, permission/confirmation behavior and plan/surface variability;
- GitHub integration: built-in GitHub app behavior, repository authentication and documented read/write boundaries;
- custom/app action availability where relevant to the supported Plus profile;
- any documented context/message/reasoning/model limitations relevant to HDM;
- any documented host lifecycle/output/tool-call behavior required by current assurance questions.

Only first-party sources may establish current product capability claims in the public assurance artifact unless a separate stage explicitly admits another evidence class.

### 3.5 Actual target-environment capability evidence

The currently connected GitHub tool surface in this development environment already demonstrates that **this configured environment** exposes:

- authenticated-user/profile resolution;
- repository discovery/read/search;
- collaborator-permission inspection;
- exact file/ref operations;
- repository write operations including create/update/delete and branch/ref operations.

This empirical fact must be kept distinct from generic ChatGPT Plus product availability.

R2.6 must determine whether the supported HDM deployment profile may require an explicitly installed/configured action-capable GitHub app/plugin and what behavior is unsupported when only the standard read-only GitHub app is present.

---

## 4. Assurance domains

### 4.1 RepositoryPort / GitHub action capability

Determine whether the supported profile can reliably provide:

- authenticated acting principal / stable GitHub identity;
- exact ref/source reads;
- bounded directory/file/search discovery;
- create/update operations with stale-source fencing/CAS as required;
- branch/ref operations used by campaign/live architecture;
- permission checks;
- clear failure/ambiguity outcomes;
- write-action approval settings compatible with ordinary gameplay latency.

Important current tension to test:

> current first-party documentation describes the standard ChatGPT GitHub app as read-only, while the current configured project environment exposes GitHub write actions. R2.6 must classify the exact supported configuration rather than conflating these surfaces.

### 4.2 Logical role containment

Revalidate Protocols 1–3 against the final R2.4 topology:

- Interpreter/Dramaturg/Actor/Narrator phase rebinding;
- multi-Actor sequential phases;
- lawful handoffs vs raw private context;
- long-history containment;
- reasoning-profile variation;
- fresh Narrator rebind after Chronicler;
- planning-loaded Dramaturg -> Narrator containment from R2.5.

Behavioral containment is the relevant baseline guarantee. Do not claim physical/cognitive isolation unless the host actually provides and documents it.

### 4.3 Instruction/data/role-switch security

Test instruction-like content inside:

- player text;
- campaign records;
- Story;
- Actor dialogue;
- Dramaturg horizons;
- connected-app/tool output.

Data must not self-promote into engine instruction, role switch, authority or source eligibility.

### 4.4 Narrator emission/disclosure fencing

Determine whether the ordinary ChatGPT surface can realize the required logical behavior:

```text
internal role/tool work
-> NarrationResult
-> validation against eligible bundle/disclosure refs
-> player-visible response
```

R2.6 must be precise about what is behaviorally controllable by instructions/tool sequencing versus what would require a stronger transport-level pre-render interception guarantee.

### 4.5 Context/token/resource pressure

R2.3 correctness cannot depend on exact hidden tokenizer/context telemetry.

Verify:

- what host/model capacity information is actually available;
- whether reliable remaining-context/message telemetry exists;
- how to test centralized approximate budgeting without pretending exact capacity knowledge;
- behavior when `ASSEMBLED_DEGRADED` or `UNSATISFIABLE` paths occur;
- long-chat degradation and retrieval/lazy-load behavior.

No copied fixed context quotas or remembered product limits become architecture constants.

### 4.6 Reasoning/model profile

Protocol 3 shows strong containment across tested fast/medium/high profiles while quality style differs; high reasoning is the owner-selected working default.

R2.6 must determine whether current ChatGPT Plus exposes sufficiently stable profile/model selection to make that a hard requirement, recommendation or merely test profile.

Campaign semantics and persistence must remain model-profile independent.

### 4.7 Chronicler service / latency / anti-starvation

Test mixed-load sequences containing:

- heavy Dramaturg setup;
- multi-Actor scenes;
- mechanics/tool work;
- normal quiet turns;
- save/recovery boundaries;
- compatible Story backlog.

Verify first-safe-opportunity service without starving current response or letting Story become correctness-critical.

### 4.8 Multiplayer multi-chat assurance

Using R2.5 scenarios, test:

- false-positive agency waiting;
- false-negative agency waiting;
- maximal-safe-frontier narration;
- stale/superseded collaboration generation;
- external-consent impersonation;
- join/rejoin catch-up/currentness;
- split-party independent progress;
- cross-scene causal bridge behavior;
- shared/local Dramaturg horizon lazy discovery;
- shared-horizon update/rebase conflict;
- cross-player planning secrecy containment.

No shared Project/group chat is required for correctness; each player retains their own ChatGPT conversation and GitHub identity/connection.

### 4.9 Shared serving/profile semantics — S53 delta

Determine whether multiplayer requires:

- identical model/reasoning configuration across players;
- only a minimum supported capability envelope with a recommended profile;
- an explicit campaign-visible profile declaration;
- or no persistent shared serving profile at all.

Do not assume one host setting governs all independent player chats.

This is a likely owner-level decision only if evidence leaves multiple materially different viable product policies.

### 4.10 Retry / D15 dormant trigger

D15 remains dormant unless current Retry/Edit evaluation shows repetitive/rejected-sibling behavior is a real supported-product problem worth solving.

Do not activate rejected-sibling memory merely because Retry exists.

---

## 5. Required evidence ledger semantics

For every material assurance requirement record:

```text
requirement / source law
exact host capability needed
current documentary evidence
current empirical evidence
confidence / limitations
failure mode
SUPPORTED | SUPPORTED_WITH_DOCUMENTED_LIMITATION | DEGRADED_MODE | UNSUPPORTED
required deployment prerequisite if any
architecture consequence
R2.7 test/mapping consequence
```

Keep documentation claims, empirical probe results and architectural inference in separate columns/sections.

---

## 6. Required adversarial / regression scenarios

At minimum:

1. Narrator secret leak after secret-bearing Dramaturg phase;
2. Narrator leak after other-player Dramaturg horizon load;
3. Chronicler -> Narrator contamination;
4. tool/campaign record containing instruction-like attack text;
5. long-chat role drift;
6. multi-Actor false-knowledge transfer;
7. lawful disclosure/update positive controls;
8. `UNSATISFIABLE` context packet under pressure;
9. approximate-budget underestimate/overestimate;
10. write-action denial/confirmation/failure during a gameplay persistence edge;
11. ambiguous/stale GitHub write conflict;
12. authenticated-principal mismatch;
13. false-positive agency barrier;
14. false-negative agency barrier;
15. stale collective-window reply;
16. shared-horizon concurrent update conflict;
17. split-party genre/planning coherence without global preload;
18. no-plot-restoration after player/Actor destroys prepared trajectory;
19. Chronicler backlog under sustained high-load mixture;
20. host/model profile variation across participants.

---

## 7. YAGNI / non-goals

R2.6 does not:

- build an API orchestration service;
- require private hosting;
- introduce provider abstraction;
- redesign upstream semantics because another topology might be easier;
- assume background workers/tasks for correctness;
- promise secure physical secret isolation inside one model context;
- standardize exact token/message limits that the host does not expose as stable contract;
- require all players to use a shared Project/group chat;
- implement the action-capable GitHub app/plugin;
- perform R2.7 schema/runtime mapping.

---

## 8. Exit criteria

R2.6 closes only when:

1. every material R2.1–R2.5 host obligation has an assurance disposition;
2. exact supported ChatGPT Plus deployment prerequisites are explicit;
3. GitHub read/write/auth/principal/currentness capability is empirically/documentarily classified;
4. role containment is tested against final R2.4/R2.5 consumers;
5. injection/role-confusion and recipient secrecy are tested;
6. Narrator emission guarantee is stated no stronger than the actual host supports;
7. context/resource limits have explicit graceful-degradation behavior without fake exact telemetry;
8. Chronicler anti-starvation/latency behavior is tested;
9. multiplayer agency/catch-up/planning scenarios are tested;
10. S53 shared-profile delta is resolved or proven unnecessary;
11. D15 remains dormant or is activated only by its exact trigger with evidence;
12. unsupported/limited capabilities have explicit product behavior rather than silent semantic weakening;
13. R2.7 machine/test obligations are explicit;
14. adversarial review closes all material blockers;
15. no broad implementation is started.

---

## 9. Immediate next activity

```text
current official host-doc revalidation
+
current target-environment capability inventory
+
Protocols 1–3 / upstream assurance handoff extraction
    -> R2.6 evidence ledger
    -> production-like probe matrix
    -> only then Decision Brief for any genuine remaining owner trade-off
```

Broad implementation remains **BLOCKED**.