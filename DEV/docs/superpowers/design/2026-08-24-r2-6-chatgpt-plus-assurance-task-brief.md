# R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation — Task Brief

Status: **ACTIVE TASK BRIEF — R2.6 IN PROGRESS / REVISED AFTER OWNER TRANSPORT CLARIFICATION**

Date: 2026-08-24

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Owner clarification:

- `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`

Depends on:

- owner-approved ChatGPT Plus / ordinary public chat / one-user-request-one-assistant-turn baseline;
- R2.1 continuity/history architecture;
- R2.2 Actor continuity/cognition;
- R2.3 Context Runtime;
- R2.4 single-context TurnEnvelope/role containment/Chronicler service;
- R2.5 agency-safe multiplayer collaboration and Dramaturg coordination;
- Step-3 deterministic execution boundary;
- Step-4 truth/knowledge/disclosure/role-context law;
- Step-5 persistence/recovery/concurrency/emission boundaries;
- owner-approved fixed Python/core-prepared + GitHub Connector repository transport.

No implementation is authorized by this brief.

---

## 1. Purpose

R2.6 is an **assurance stage**, not a new orchestration, persistence or repository-transport design stage.

Its job is to determine which already-approved HDM semantics the current target host can realize reliably enough for the supported product profile:

```text
primary host          ChatGPT
plan                  ChatGPT Plus
surface               ordinary public chat / Project-capable workflow
per-player topology   one human -> own chat/context
multiplayer transport shared GitHub campaign/current frontiers
ordinary turn         one user request -> one assistant turn
repository path       deterministic Python/core preparation + fixed GitHub Connector remote operations
```

For every material obligation, R2.6 classifies current support as:

```text
SUPPORTED
SUPPORTED_WITH_DOCUMENTED_LIMITATION
DEGRADED_MODE
UNSUPPORTED
```

If the host cannot realize a required semantic boundary, R2.6 restricts/rejects the deployment profile or explicitly reopens the affected architecture decision. It must not silently weaken upstream semantics.

---

## 2. Current evidence warning

Time-sensitive product capabilities, model availability, Project behavior, permission UX and limits can change.

R2.6 SHALL reverify current host claims against:

1. current first-party product documentation where available;
2. the actual current target ChatGPT environment through bounded capability/behavior probes where documentation is insufficient;
3. existing HDM Protocols 1–3 for behavioral containment evidence;
4. new production-like regression probes derived from R2.3–R2.5.

Historical comparative-host research is routing/background evidence only. Its superseded physical-isolation and alternate-transport questions do not regain architecture authority.

---

## 3. Fixed repository transport boundary

Repository-transport selection is **closed and inherited**.

Supported gameplay path:

```text
DETERMINISTIC PYTHON / CORE
    prepare/freeze exact semantic publication state
    own currentness / transaction / retry decision
        |
        v
CHATGPT GITHUB CONNECTOR
    execute the approved remote GitHub operations only
        |
        v
NON-FORCE AUTHORITATIVE REF TRANSITION
```

Ordinary campaign publication remains:

```text
create_tree(base pinned tree, dirty delta)
-> ref check
-> create_commit(parent pinned HEAD)
-> update_ref(force=false)
```

R2.6 SHALL NOT try, compare or probe as runtime alternatives:

- `gh` / GitHub CLI;
- remote native Git, clone/fetch/pull/push/SSH;
- direct private-repository HTTP/API calls from Python/container;
- credential/token workarounds;
- custom MCP/backend/app write-service alternatives;
- GitHub Actions as an improvised gameplay bridge;
- local-commit transparent Connector push;
- any “try another Git transport” behavior after Connector failure.

A missing required Connector capability is a supported-profile capability failure, not a degraded transport-selection branch.

Repository assurance is limited to the fixed path's currentness, CAS, failure, latency, permission and user-visible-surface behavior.

---

## 4. Task-specific Source Manifest

### 4.1 Process / sequencing

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

### 4.2 Current canonical obligations

- Round-1 closure / Round-2 rebaseline owner decision;
- Step-4 single-context role-containment canonical amendment;
- R2.1 continuity canonical spec/gate;
- R2.2 Actor canonical spec/gate;
- R2.3 Context Runtime canonical spec/gate;
- R2.4 TurnEnvelope canonical spec/gate;
- R2.5 multiplayer collaboration canonical spec/gate;
- Step-5.4 host lifecycle/handoff;
- Step-5.8 multiplayer/live currentness;
- Step-5.12 host delivery/disclosure boundary;
- Step-5.14 integrated recovery/concurrency closure;
- `GAME/CORE/PLAY_POLICY.md`;
- `GAME/CORE/PERSISTENCE.md`.

### 4.3 Existing empirical/research evidence

- Protocol 1 sequential containment;
- Protocol 2 collapsed multi-role containment;
- Protocol 3 reasoning-budget comparison;
- retained transport feasibility evidence only for conclusions already established on the fixed Connector path;
- current R2.3/R2.4/R2.5 adversarial scenarios and assurance handoffs;
- `2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`;
- `2026-08-24-r2-6-production-like-assurance-protocol.md`;
- `2026-08-24-r2-6-protocol-4-frozen-fixture-contract.md`.

### 4.4 Current first-party host documentation

Recheck current official documentation for at least:

- ChatGPT Plus reasoning/model availability and fallback behavior;
- Projects: instructions, files/context and project-memory behavior;
- app/Connector permission/approval behavior relevant to the **already-selected** GitHub path;
- any documented context/message/host-output behavior needed by current assurance questions;
- Retry/regeneration/branching behavior where it affects accepted Step-5.12 semantics.

Official documentation may establish current product facts. It does **not** authorize alternate runtime transport experiments.

### 4.5 Actual target-environment evidence

Empirically inventory only capabilities needed by the selected profile, including:

- authenticated GitHub identity/principal resolution;
- repository read/search/permission operations;
- exact source/ref reads;
- fixed Git-data/ref mutation operations required by `PERSISTENCE.md`;
- current approval/UI behavior where it can affect latency or disclosure;
- model/reasoning labels exposed by the current product;
- actual visible auxiliary surfaces relevant to gameplay secrecy.

Do not infer unavailable telemetry. Record `UNKNOWN` when the host does not expose it.

---

## 5. Assurance domains

### 5.1 Fixed Connector-path assurance

Determine whether the selected profile reliably supports:

- authenticated acting principal / stable GitHub identity;
- exact pinned ref/source reads;
- bounded repository discovery required by current runtime routing;
- Python-owned frozen publication envelope;
- `create_tree` / current ref check / `create_commit` / non-force `update_ref`;
- stale-source/non-fast-forward handling;
- clear confirmed/conflict/ambiguous failure behavior as far as the host exposes it;
- no force push;
- no partial per-record campaign publication;
- live/shared-planning CAS/current-generation semantics on their owning paths;
- permission/approval behavior compatible with secrecy and ordinary gameplay.

Do not compare another backend.

### 5.2 Logical role containment

Revalidate Protocols 1–3 against final R2.4/R2.5 consumers:

- Interpreter/Dramaturg/Actor/Narrator rebinding;
- multi-Actor separation;
- lawful handoffs vs raw private context;
- long-history containment;
- fresh Narrator after Chronicler;
- no same-envelope Story feedback;
- shared/local Dramaturg planning -> Narrator/catch-up containment;
- stale/foreign Project-memory-like ambient context.

Behavioral containment is the baseline guarantee. Do not claim physical/cognitive isolation.

### 5.3 Instruction/data/role-switch security

Test instruction-like content inside:

- player text;
- campaign records;
- Story;
- Actor dialogue;
- local/shared Dramaturg horizons;
- connected-app/tool output.

Data must not self-promote into engine instruction, role switch, authority or source eligibility.

### 5.4 Narrator emission/disclosure fencing

Assure the Step-5.12 logical boundary without inventing a stronger byte-exact outbox requirement.

Required target behavior:

```text
accepted/current state
-> deterministic/typed recipient + source + material-reveal admission
-> fresh Narrator rebind to eligible bundle
-> supported player-visible response representation
-> EMISSION_COMMIT
-> ordinary host output path
```

R2.6 must:

- test material lawful-vs-forbidden reveal pairs;
- inventory mandatory player-visible tool/app/approval surfaces;
- ensure auxiliary surfaces do not intentionally carry Narrator-ineligible campaign material;
- state the supported guarantee no stronger than evidence allows.

If the ordinary host cannot provide an equivalent safe material-output boundary, restrict/reopen explicitly rather than silently weaken Step 5.12.

### 5.5 Project memory / ambient host context

Current host memory/history may make prior chats physically available.

Assure:

```text
Project/chat memory
    != campaign authority
    != currentness evidence
    != Actor knowledge
    != disclosure evidence
```

Current routed owners and logical eligibility must win over stale ambient context.

Project-only memory may be evaluated as a contamination-reduction recommendation, not assumed as campaign authority or a substitute for role containment.

### 5.6 Context/token/resource pressure

R2.3 correctness cannot depend on exact hidden remaining-context telemetry.

Verify:

- what host capacity information is actually available;
- centralized conservative/approximate budgeting;
- required representation floors;
- optional degradation;
- `ASSEMBLED_DEGRADED`;
- `UNSATISFIABLE` non-looping behavior;
- long-chat degradation and lazy retrieval.

No copied API/model context value becomes a permanent ChatGPT runtime constant.

### 5.7 Reasoning/model profile — S53 delta

Protocol 3 shows strong containment across tested profiles while style/quality differs. High remains owner-selected working default.

R2.6 determines whether the supported multiplayer policy is a minimum behavioral/capability envelope rather than exact cross-player serving identity.

Campaign semantics/persistence remain model-profile independent.

### 5.8 Chronicler service / latency / anti-starvation

Test mixed-load sequences containing:

- heavy Dramaturg setup;
- multi-Actor scenes;
- mechanics/currentness work;
- ordinary quiet turns;
- save/recovery pressure;
- compatible Story backlog.

Verify first-safe-opportunity service without starving current response or making Story correctness-critical.

### 5.9 Multiplayer multi-chat assurance

Test:

- false-positive agency waiting;
- false-negative agency waiting;
- maximal-safe-frontier semantics and narration;
- stale/superseded collaboration generation;
- external-consent impersonation;
- join/rejoin catch-up/currentness;
- split-party independent progress;
- cross-scene material bridges;
- shared/local Dramaturg horizon lazy discovery;
- shared-horizon CAS/rebase conflict;
- cross-player planning secrecy;
- no-plot-restoration after preparation is invalidated.

Each player retains their own ChatGPT conversation and campaign repository access/binding. No shared group chat is required.

### 5.10 Retry / D15 dormant trigger

D15 remains dormant unless actual R2.6 Retry evaluation shows repetitive/rejected-sibling behavior is a real supported-product failure worth solving.

Retry existence alone does not activate rejected-sibling memory.

---

## 6. Required evidence ledger semantics

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

Keep documentary claims, empirical behavior, deterministic tool outcomes, human-side UI observations and architectural inference separate.

---

## 7. Required adversarial / regression scenarios

At minimum:

1. Narrator secret leak after secret-bearing Dramaturg phase;
2. Narrator leak after other-player/shared Dramaturg horizon load;
3. Chronicler -> Narrator contamination;
4. same-envelope Story feedback attempt;
5. stale/foreign Project-memory context vs current repository owner;
6. instruction-like attack text in data/tool/planning channels;
7. long-chat role drift;
8. multi-Actor false-knowledge transfer;
9. lawful disclosure/update positive controls;
10. `UNSATISFIABLE` context packet under pressure;
11. approximate-budget underestimate/overestimate;
12. Connector approval/denial/failure on the fixed path;
13. stale/non-fast-forward Connector conflict on the fixed path;
14. authenticated-principal mismatch;
15. false-positive agency barrier;
16. false-negative agency barrier;
17. stale collective-window reply;
18. shared-horizon concurrent update conflict;
19. split-party planning coherence without global preload;
20. no-plot-restoration after player/Actor destroys prepared trajectory;
21. Chronicler backlog under sustained high-load mixture;
22. host/model profile variation across participants;
23. Retry/regeneration without mechanics/RNG/canon replay;
24. human-side synthetic canary for mandatory player-visible tool/approval surfaces where the assistant cannot inspect rendered UI.

---

## 8. YAGNI / non-goals

R2.6 does not:

- build an API orchestration service;
- require private hosting;
- introduce provider abstraction;
- select or test another Git/repository transport;
- redesign upstream semantics because another topology might be easier;
- assume background workers/tasks for correctness;
- promise secure physical secret isolation inside one model context;
- require byte-exact post-render interception unless evidence proves the accepted semantic boundary cannot otherwise be realized;
- standardize exact token/message limits the host does not expose as a stable contract;
- require all players to use a shared Project/group chat;
- implement schemas/runtime/migrations — R2.7;
- create probe branches or disposable repository mutations by default.

---

## 9. Exit criteria

R2.6 closes only when:

1. every material R2.1–R2.5 host obligation has an assurance disposition;
2. exact supported ChatGPT Plus deployment prerequisites are explicit;
3. the **fixed** GitHub Connector path's read/write/auth/currentness/permission behavior is classified without transport reselection;
4. role containment is tested against final R2.4/R2.5 consumers;
5. Project-memory ambient-context behavior is dispositioned;
6. injection/role-confusion and recipient secrecy are tested;
7. Narrator/`EMISSION_COMMIT` guarantee is stated no stronger than actual host evidence;
8. mandatory visible auxiliary surfaces are inventoried sufficiently for secret-bearing gameplay;
9. context/resource limits have graceful degradation without fake exact telemetry;
10. Chronicler anti-starvation/latency behavior is tested;
11. multiplayer agency/catch-up/planning scenarios are tested;
12. S53 shared-profile delta is resolved or proven unnecessary;
13. D15 remains dormant or activates only by its exact trigger with evidence;
14. unsupported/limited capabilities have explicit product behavior rather than silent semantic weakening;
15. R2.7 machine/test obligations are explicit;
16. adversarial review closes all material blockers;
17. no broad implementation is started.

---

## 10. Immediate next activity

Current documentary/source extraction and protocol design are complete enough to enter empirical assurance collection.

```text
Protocol 4 frozen fixtures
    -> fresh-history target-host runs where required
    -> bounded fixed-Connector assurance using retained evidence where sufficient
    -> one synthetic human-side UI observation only where rendered UI cannot be inspected by the agent
    -> result classification
    -> Decision Brief only if multiple material product policies remain
```

Do not claim Protocol-4 execution results until actual target-host evidence exists.

Broad implementation remains **BLOCKED**.
