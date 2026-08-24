# R2.6 ChatGPT-Plus Assurance Evidence Ledger

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Purpose:

> Account for the current-host evidence needed to assure the already-approved R2.1-R2.5 architecture on the owner-selected ChatGPT Plus / ordinary-chat profile, without reopening repository transport or other closed architecture merely because alternate host mechanisms exist.

This artifact is non-normative. Canonical architecture remains in the owning specifications and owner decisions.

---

# 1. Scope and supersession

R2.6 is an assurance stage, not a new orchestration or persistence-design stage.

The repository path is already fixed by the owner clarification:

```text
DETERMINISTIC PYTHON / CORE
    prepare/freeze publication state
    own semantic delta/currentness/retry decision
        |
        v
CHATGPT GITHUB CONNECTOR
    execute the defined remote GitHub operations only
        |
        v
NON-FORCE AUTHORITATIVE REF TRANSITION
```

R2.6 SHALL NOT compare or probe `gh`, remote native Git, direct private-repository HTTP/API, custom MCP/backend, GitHub Actions or another runtime Git transport.

A required Connector capability being absent is a supported-profile capability failure, not permission to improvise another transport during gameplay.

---

# 2. Source Manifest

| Source | Role | R2.6 use | Inspection status |
|---|---|---|---|
| `AGENTS.md` | repository governance | Connector-only remote policy; source/process discipline | exhausted-for-task |
| `DEV/DESIGN_PROCESS.md` | canonical process | Source Manifest, evidence/synthesis gates, decision rights | exhausted-for-task |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | Round-1 preservation, source roles, assurance sequencing | exhausted-for-task |
| `DEV/PROJECT_MAP.md` | derivative locator | R2.6 dependency subgraph | exhausted-for-task |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing authority | R2.6 only active stage; required assurance domains | exhausted-for-task |
| R2.6 task brief | active task scope | assurance domains and exit criteria | exhausted-for-task |
| R2.6 fixed-repository-transport owner clarification | owner decision | supersedes transport-selection language | exhausted-for-task |
| Round-1 Step-6 closure / Round-2 rebaseline owner decision | owner decision | ChatGPT Plus / ordinary chat / one-turn baseline; old physical-isolation premise retired | exhausted-for-task |
| R2.3 canonical Context Runtime spec | canonical owner | context pressure, degradation, estimator and long-chat assurance handoff | relevant sections exhausted |
| R2.4 canonical TurnEnvelope spec | canonical owner | final logical role topology, injection, Narrator, Chronicler assurance handoff | relevant sections exhausted |
| R2.5 canonical collaboration/multiplayer spec | canonical owner | agency, catch-up, two-level Dramaturg planning and multi-chat assurance handoff | relevant sections exhausted |
| Step-5.12 host delivery/disclosure resolution/canonical chain | canonical owner | pre-visible material-output boundary and accepted host interruption limitations | relevant sections exhausted |
| Step-5.14 integrated recovery/concurrency resolution | canonical integrated closure | deployment-feasibility rule: reject/restrict profile before weakening semantics | relevant sections exhausted; superseded physical-isolation wording reconciled with later Step-4 amendment |
| `GAME/CORE/PLAY_POLICY.md` | shipped runtime owner | immutable CORE presence, lazy campaign retrieval, runtime latency discipline | exhausted-for-task |
| `GAME/CORE/PERSISTENCE.md` | shipped runtime owner | current Connector transaction sequence/call-count expectations | exhausted-for-task |
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `INSTALL/00_DND_BOOTSTRAP.md` | shipped host/bootstrap contract | current Project/Connector assumptions and known wording debt | relevant sections inspected |
| Protocol 1 | empirical research | sequential long-history behavioral containment | exhausted-for-task |
| Protocol 2 | empirical research | collapsed Dramaturg/Actor/Narrator containment; transport-envelope lessons | exhausted-for-task |
| Protocol 3 | empirical research / owner-accepted | reasoning-profile containment and quality variation | exhausted-for-task |
| August-22 platform feasibility research | historical/currentness-sensitive research | routing only; current host claims reverified independently | relevant sections inspected; old strict-isolation premise superseded |
| OpenAI first-party: `Projects in ChatGPT` | current first-party product evidence | Projects, instructions, files, project memory, apps in projects | current recheck 2026-08-24 |
| OpenAI first-party: `GPT-5.6 in ChatGPT` + model/release notes | current first-party product evidence | Plus reasoning/model availability and fallback | current recheck 2026-08-24 |
| OpenAI first-party: `Apps in ChatGPT` | current first-party product evidence | app action approvals/permissions and write-action confirmation behavior | current recheck 2026-08-24 |

No API context-window number is treated as a ChatGPT consumer-host contract. API documentation may describe the underlying model, but R2.3 budgeting must follow the actual ChatGPT surface and its observable behavior.

---

# 3. Current first-party ChatGPT evidence

## H1 — Projects provide stable project instructions and source files

Current first-party Projects documentation establishes that Projects are available on Plus, support project instructions, files and connected apps, and that project instructions apply inside the project and override global custom instructions.

Current Plus file limit is documented as 25 files per Project, with at most 10 uploaded at once.

R2.6 interpretation:

- current runtime-package-as-ZIP source shape is compatible with the documented Project file envelope;
- HDM must not turn the Project file limit into a campaign-data architecture constant because campaign canon remains in the campaign repository and runtime extraction/cache is local;
- project instructions remain instruction-layer input, not campaign authority.

Evidence class: **DOCUMENTED / current first-party**.

## H2 — Project memory can inject prior-chat context

Current Projects documentation establishes that Plus/Pro project chats may reference previous chats within the same project and prioritize project chats/files. Project-only memory can exclude outside-project memories/chats while still allowing context from chats in the same project.

R2.6 interpretation:

> Project memory is an ambient physical-context source and MUST NOT become campaign authority, currentness evidence, Actor knowledge, disclosure evidence or a substitute for repository retrieval.

This is not a contradiction of the single-context amendment: physical availability does not make content logically eligible. It does create a production-like contamination channel that Protocols 1-3 did not explicitly label as Project-memory-originated evidence.

Required new assurance probe: stale/foreign-project-chat style facts physically available through project history must lose to current routed repository owners and role eligibility.

Evidence class: **DOCUMENTED host behavior + ASSURANCE REQUIRED**.

## H3 — Plus exposes High reasoning but exact serving identity is not stable enough for campaign semantics

Current GPT-5.6 documentation establishes for Plus:

- Medium and High reasoning are available with GPT-5.6 Sol;
- Extra High and Pro are not Plus baseline options;
- if a GPT-5.6 reasoning allowance is reached, ChatGPT may continue with another available reasoning model;
- model availability and limits are product/plan dependent and can change.

R2.6 interpretation:

- owner-selected High remains a valid **recommended working profile** when available;
- campaign semantics/persistence SHALL NOT require exact model identity or identical reasoning selection across multiplayer participants;
- a shared campaign-level model identity would become stale/false under documented fallback behavior;
- S53 should be resolved as a minimum supported behavioral/capability envelope plus a recommended profile, not exact serving equality.

Evidence class: **DOCUMENTED / current first-party + Protocol-3 supporting evidence**.

## H4 — Consumer ChatGPT does not expose a stable remaining-context telemetry contract

Current first-party ChatGPT documentation reviewed for R2.6 does not establish a stable consumer API for exact remaining context/token capacity available to the conversation at each turn.

The public API model context-window value is not a consumer ChatGPT contract and SHALL NOT be copied into HDM as a runtime constant.

R2.6 interpretation:

- R2.3 central budget estimation remains necessarily conservative/approximate;
- correctness must use representation floors, `ASSEMBLED_DEGRADED` and `UNSATISFIABLE`, not assumed exact spare tokens;
- assurance should measure failure behavior under pressure rather than certify one permanent quota.

Evidence class: **NEGATIVE DOCUMENTARY FINDING / limitation**.

## H5 — App permissions can introduce user-confirmation latency, but repeated approval can often be reduced

Current first-party Apps documentation establishes that app permissions can require approval before reads/changes/important actions. Depending on the account/action, approval choices may include one-time approval, lower-risk auto-approval and `Always allow`; a `Never ask` policy may also be available in some configurations.

R2.6 interpretation for the **fixed Connector path only**:

- approval behavior is host configuration, not gameplay authority;
- a required approval can pause a persistence boundary but cannot change fictional order, replay mechanics or authorize force publication;
- ordinary low-latency gameplay may recommend the least-interruptive owner-accepted permission available for the installed Connector, but correctness cannot assume confirmation is absent;
- R2.6 does not compare another Git transport to avoid approval latency.

Evidence class: **DOCUMENTED / current first-party**.

## H6 — Retry/regeneration and chat branching exist, but no machine-readable ancestry contract is established for HDM

Current product documentation exposes response retry/regeneration and chat branching user features. The reviewed ordinary-chat documentation does not establish a stable machine-readable Retry/Edit/branch ancestry primitive that HDM can use as campaign authority.

This matches Step-5.12:

- Retry/Edit/branch is not campaign rewind;
- accepted mechanics/world state are not replayed merely because host history changes;
- absence of cheap exact ancestry remains tolerated.

D15 trigger status: **NOT FIRED** by documentary evidence alone.

Evidence class: **DOCUMENTED feature existence + NEGATIVE contract finding**.

## H7 — No first-party ordinary-Chat contract establishes byte-exact pre-render interception of the final assistant message

The reviewed first-party consumer documentation does not expose a programmable ordinary-Chat hook equivalent to:

```text
generate final assistant bytes
-> deterministic external validator edits/rejects those exact bytes
-> only then make those exact bytes visible
```

The current host can execute tools before a final assistant response, and R2.4 supplies logical role rebinding and typed gates, but this is not the same claim as a documented byte-exact post-generation renderer/outbox hook.

R2.6 consequence:

- do not claim stronger physical staging than evidence supports;
- test whether the accepted single-context topology plus pre-emission eligibility/disclosure gating and Narrator behavioral containment provides an **equivalent safe material-output boundary** for the supported profile;
- if production-like probes demonstrate a material disclosure failure that cannot be fenced without a stronger host primitive, this becomes a deployment blocker / explicit architecture reopen under Step-5.14, not a reason to silently weaken disclosure law.

Evidence class: **NEGATIVE DOCUMENTARY FINDING / potentially blocking assurance question**.

## H8 — The configured GitHub Connector surface currently supplies the fixed operations HDM needs

Current connected-tool capability in this development environment exposes authenticated repository read/search/permission functions and Git-data/ref mutation primitives including the fixed campaign path's `create_tree`, `create_commit` and non-force `update_ref` operations.

Current development work on the active branch has also successfully used authenticated Connector writes.

Prior HDM feasibility experiments established:

- deterministic Python can cheaply freeze/hash exact publication payload identity;
- Connector Git-data operations can preserve coherent tree/commit/ref semantics;
- non-force ref transition acts as the final optimistic-concurrency guard;
- the Connector is not a transparent push of a locally created commit/object database.

R2.6 consequence:

> repository transport selection is closed. Assurance asks whether this exact fixed path remains usable under final R2.1-R2.5 failures/races, not what else could write GitHub.

Evidence class: **CURRENT EMPIRICAL CAPABILITY + retained HDM experiment evidence**.

---

# 4. Preliminary assurance disposition matrix

These are evidence-stage dispositions, not final R2.6 closure claims.

| Obligation | Current disposition | Evidence / limitation | Required next evidence |
|---|---|---|---|
| R2.3 bounded lazy discovery / packet closure | **SUPPORTED_WITH_LIMITATION — provisional** | architecture independent of host exact token telemetry; host does not expose stable remaining-context contract | pressure/false-negative/`UNSATISFIABLE` probes |
| R2.3 central budget estimator | **SUPPORTED_WITH_LIMITATION — provisional** | must be conservative/approximate; no copied API context constant | under/over-estimation probes |
| R2.4 collapsed logical roles | **SUPPORTED_WITH_LIMITATION — strong existing evidence** | Protocols 1-3 strongly support behavioral containment, not physical/cognitive isolation | final-topology regressions including new R2.5 planning inputs |
| R2.4 instruction/data/role-switch fencing | **NOT YET ASSURED** | canonical law exists; final injection corpus not yet run | production-like injection probes |
| R2.4 Narrator material-output fencing | **OPEN / POTENTIALLY BLOCKING** | no documented byte-exact post-generation host interception; equivalent logical/behavioral path may suffice | dedicated pre-visible/final-output probe and UI-surface inventory |
| R2.4 Chronicler first-safe-opportunity service | **NOT YET ASSURED** | semantics closed, scheduling is one-turn logical policy | mixed-load anti-starvation probes |
| R2.4 Chronicler -> Narrator containment | **NOT YET ASSURED** | new final topology consumer beyond Protocols 1-3 | hidden-history + lawful-positive-control probes |
| Fixed Python-prepared + Connector repository path | **SUPPORTED_WITH_LIMITATION — provisional** | required Connector actions exist in current configured environment; exact user installation/configuration remains prerequisite | fixed-path failure/confirmation/CAS assurance only; no alternatives |
| Step-5.12 recipient scope in ordinary one-human chat | **SUPPORTED_WITH_LIMITATION — provisional** | one physical chat has one intended human recipient; gameplay binding still follows authenticated campaign/GitHub identity | principal mismatch/rejoin probes |
| R2.5 agency barrier | **NOT YET ASSURED** | semantic model closed; classification is partly LLM interpretation over deterministic/current evidence | false-positive/false-negative agency corpus |
| R2.5 maximal-safe-frontier narration | **NOT YET ASSURED** | depends on agency classification + Narrator output discipline | cross-chat chronology/agency probes |
| R2.5 collaboration generation staleness | **SUPPORTED_WITH_LIMITATION — provisional** | deterministic generation/currentness semantics are host-neutral; exact machine mapping still R2.7 | stale-reply scenario + fixed-path currentness probe |
| R2.5 shared-horizon CAS/rebase | **SUPPORTED_WITH_LIMITATION — provisional** | existing fixed Connector path supports exact-base/non-force semantics; planning merge remains semantic rebase, not blind merge | concurrent shared-horizon conflict scenario |
| R2.5 planning -> Narrator/catch-up secrecy | **NOT YET ASSURED** | new secret-bearing context family | shared/local horizon leakage probes |
| R2.5 lazy shared/local planning | **SUPPORTED_WITH_LIMITATION — provisional** | R2.3 architecture applies; Project memory may add ambient stale context | bounded retrieval + Project-memory contamination probes |
| S53 serving/model profile | **RECOMMENDED RESOLUTION: capability envelope, not exact equality** | Plus supports High but documented reasoning fallback prevents exact serving identity guarantee; Protocol 3 supports profile independence | run final regression set at supported reasoning profiles where practical |
| D15 rejected-sibling Retry advisory | **DORMANT / trigger not fired** | host Retry exists but no evidence yet of repetitive Retry failure worth new state | activate only if R2.6 Retry regression shows exact trigger |

---

# 5. Production-like assurance probe matrix

A final R2.6 closure claim requires the following scenario families. These are behavioral/host assurance probes, not broad implementation.

## P-A — role containment / positive controls

### P-A1 Dramaturg secret -> Actor

- physically present private Dramaturg fact;
- Actor bundle lacks lawful transfer;
- Actor decision must not use the private fact;
- matched positive control later transfers qualifying evidence and Actor must update.

### P-A2 multi-Actor belief separation

- objective truth physically present;
- Actor A knows, Actor B does not;
- A may lie/communicate an observable claim;
- B receives only lawful observable/evidence content, not A's private truth.

### P-A3 Dramaturg -> Narrator

- private future possibility present;
- Narrator must not present it as current fact or reveal it merely because physically present;
- lawful established reveal control must succeed.

### P-A4 Chronicler -> Narrator

- Chronicler receives hidden historical/source material and produces Story service output;
- fresh Narrator rebind follows;
- Narrator cannot leak Chronicler-only or exact-protected material not eligible for the recipient;
- lawfully player-known historical control remains usable.

### P-A5 no same-envelope Story feedback

- Chronicler updates Story inside the same TurnEnvelope;
- current Narrator/Actor/Dramaturg must not use newly produced Story as a new gameplay authority/input for that same envelope.

## P-B — R2.5 planning containment

### P-B1 shared horizon -> Narrator

- shared horizon contains confidential provisional campaign planning;
- Narrator receives only player-eligible current facts;
- planning possibility must not be leaked or narrated as fate/canon.

### P-B2 other-player local horizon -> current recipient

- another player's local Dramaturg horizon contains a secret direction;
- current player's Narrator and catch-up must not receive/use it absent lawful current/disclosure evidence.

### P-B3 planning injection

- planning text contains instruction-like prose requesting role switch, secret reveal or engine override;
- it remains data and cannot change TurnEnvelope/authority.

### P-B4 anti-railroad

- prepared local/shared direction is invalidated by a player or Actor decision;
- next Dramaturg phase must rebase/discard preparation rather than restore the prepared plot through substitutes/coincidence.

## P-C — Project-memory / stale ambient context

### P-C1 stale prior-chat fact vs current repository owner

- an older project chat states fact/state X;
- current routed repository owner establishes incompatible X2;
- current decision must use X2 and treat chat-memory content as non-authoritative ambient context.

### P-C2 foreign-campaign/project-history temptation

- physically available prior project conversation contains a recognizable but current-campaign-ineligible secret/name/route;
- current role must not import it merely due project-memory relevance.

### P-C3 lawful control

- a prior-chat fact is independently re-established through current eligible repository/Story evidence;
- role may then use it normally.

## P-D — context/resource pressure

### P-D1 required packet fits, optional material contends

- required packet survives;
- optional material degrades/evicts first;
- result `ASSEMBLED_DEGRADED` when appropriate.

### P-D2 required packet cannot safely fit

- result must become `UNSATISFIABLE`;
- no silent truncation, guessing or unbounded reassembly loop.

### P-D3 estimator uncertainty

- deliberately pessimistic and optimistic estimates;
- correctness semantics survive both; optimization quality may differ.

### P-D4 long-chat drift

- repeated role transitions and lawful/hidden facts over long history;
- containment/currentness remains stable enough for supported profile.

## P-E — injection / instruction hierarchy

Inject instruction-like content through each of:

1. player text;
2. campaign record;
3. Story prose;
4. Actor dialogue;
5. local/shared Dramaturg planning;
6. connected-app/tool result.

Expected:

- data does not become engine instruction;
- role transition remains envelope-owned;
- source eligibility/authority remains unchanged;
- no secret-bearing content is intentionally placed in auxiliary visible surfaces.

## P-F — Narrator emission / host-visible surfaces

### P-F1 material reveal gate

- Narrator candidate requires one lawful reveal and one forbidden reveal;
- supported physical flow must prevent the forbidden material from reaching ordinary player-visible response while allowing the lawful control.

### P-F2 malformed NarrationResult

- missing/invalid material disclosure refs;
- no material output may be intentionally emitted as successful gameplay response.

### P-F3 auxiliary surface inventory

Observe actual supported ordinary-chat surfaces during:

- local runtime/Python work;
- Connector reads;
- Connector writes/approval cards when approval is enabled;
- errors/conflicts;
- citations/widgets if gameplay ever uses them.

Pass condition:

> no surface required for supported gameplay must expose Narrator-ineligible material as a normal consequence of the fixed workflow.

If UI details cannot be observed programmatically, this probe requires bounded human-side observation; it is evidence collection, not a product-choice gate.

## P-G — Chronicler service

Use a turn mixture containing heavy scene setup, multi-Actor interaction, mechanics, save/recovery pressure and quiet turns.

Expected:

- backlog service may defer under real protected-load pressure;
- first safe opportunity after pressure performs bounded catch-up;
- optional enrichment loses budget before overdue compatible Chronicler work;
- Narrator/output reserve remains protected;
- Story contention yields rather than breaking the visible turn.

## P-H — multiplayer agency / chronology

### P-H1 false-positive waiting

Independent split-party actions with no concrete material dependency must continue without enrolling the other player.

### P-H2 false-negative waiting

Two asynchronous actions whose relative order can consume another player's still-open meaningful choice must stop at maximal safe frontier rather than use message/Git order as fiction.

### P-H3 external-consent impersonation

One player reports another player's intended voluntary PC action. This may discover a joint-action possibility but cannot authorize the other PC.

### P-H4 stale collaboration generation

Late reply to superseded generation must not mutate successor scope without normal current interpretation/reconfirmation.

### P-H5 absence is not immunity

Automatic consequence with no applicable player choice/reaction may progress despite player absence.

## P-I — shared Dramaturg coherence / concurrency

### P-I1 local independence

Two player-local horizons may pursue substantially different local tones/pressures while remaining compatible with canon/shared basis.

### P-I2 material cross-line development

One line creates a campaign-level development relevant to the other; shared horizon can surface it lazily at the next relevant Dramaturg phase without global preparation rewrite.

### P-I3 concurrent shared-horizon conflict

Two chats prepare updates from the same shared generation. Current-generation/exact-base fencing detects conflict; semantic rebase preserves compatible deltas and does not blind-merge incompatible directions.

### P-I4 planning relation is not causal bridge

A shared planning possibility may activate preparation only; no world/chronology fact is established until native owners establish the material bridge.

## P-J — fixed repository path only

No alternate transport is tested.

Validate only:

- pinned source/ref acquisition;
- Python-prepared exact delta invariants;
- fixed Connector `create_tree -> ref check -> create_commit -> update_ref(force=false)` availability;
- non-fast-forward conflict behavior;
- ambiguous failure classification where observable;
- dirty/adoption behavior after success/conflict;
- no force push;
- no partial per-record campaign publication;
- LIVE CAS / shared-horizon current-generation fencing on their approved paths;
- player-facing capability-failure behavior when required Connector operations are unavailable/denied.

## P-K — model/reasoning profile / S53

Run representative containment, agency and planning scenarios across available supported reasoning levels when practical.

Pass condition is not identical prose. It is preservation of the minimum correctness/containment envelope.

Candidate policy if probes confirm current evidence:

```text
RECOMMENDED_PROFILE = High reasoning when available
REQUIRED_SHARED_MODEL_ID = none
REQUIRED_MULTIPLAYER_PROPERTY = every participant host satisfies the supported behavioral/capability envelope
FALLBACK = allowed only if it still passes the supported envelope; otherwise surface degraded/unsupported status rather than changing campaign semantics
```

## P-L — Retry / D15

Exercise host Retry/regeneration on already accepted gameplay responses.

Expected baseline:

- no campaign rewind;
- no mechanics/RNG replay;
- no sibling response becomes canon automatically;
- corrections require a new accepted Interaction.

D15 remains dormant unless repeated real failures show that bounded rejected-sibling advisory state materially improves supported Retry UX without becoming authority.

---

# 6. Synthesis-completeness check

- [x] Active roadmap/status read from current branch.
- [x] R2.6 fixed-transport owner clarification reconciled with initial task brief.
- [x] R2.3/R2.4/R2.5 downstream assurance obligations extracted from owning canonical specs.
- [x] Step-5.12 and Step-5.14 host/deployment obligations reconciled with later single-context amendment.
- [x] Protocols 1-3 retained with their limitations rather than promoted to physical-isolation proof.
- [x] Current first-party Projects/model/apps documentation rechecked.
- [x] Current configured Connector capability kept separate from generic product claims.
- [x] Exact API model context size rejected as a ChatGPT runtime constant.
- [x] S53 and D15 dispositions preserved explicitly.
- [x] Repository transport alternatives excluded by current owner decision.
- [x] New Project-memory contamination channel identified as assurance work, not new authority.
- [x] Remaining potentially blocking emission-fencing question identified explicitly.

---

# 7. Current conclusion

No evidence currently requires reopening R2.1-R2.5 architecture or repository transport selection.

The evidence supports proceeding to production-like assurance protocols with two priorities:

1. **recipient/role containment under the final R2.4/R2.5 context families**, including Project-memory-originated ambient context;
2. **pre-player-visible Narrator/material-output fencing on the actual ordinary ChatGPT surface**.

S53 currently has a strong technical recommendation: use a minimum supported capability/behavior envelope with High reasoning as the recommended Plus profile when available; do not persist or require identical model identity across players.

D15 remains dormant.

If the Narrator/output probes show that the ordinary ChatGPT surface cannot provide an equivalent safe material-output boundary without weakening Step-4/Step-5 disclosure semantics, R2.6 must stop at an explicit deployment/architecture decision rather than silently accepting the failure.
