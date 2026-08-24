# R2.6 Production-Like Assurance Protocol

Status: **PROTOCOL DESIGN — EXECUTION EVIDENCE NOT YET CLAIMED**

Date: 2026-08-24

Purpose:

> Validate the final R2.3-R2.5 ChatGPT Plus gameplay topology using observable behavior, current host capabilities and bounded reproducible scenarios, without reopening the fixed GitHub transport or claiming physical/cognitive isolation.

This protocol is research/evaluation infrastructure. It does not implement gameplay runtime architecture.

---

# 1. Hard execution constraints

## 1.1 Target profile

Primary target:

```text
ChatGPT Plus
ordinary Project-capable chat
one human -> one physical chat
one user request -> one assistant turn
High reasoning when available
fixed GitHub Connector path for repository operations
```

Where a comparison run is useful, Medium may be tested as another currently supported Plus reasoning profile. Exact serving model identity is recorded if the product exposes it, but campaign semantics never depend on it.

## 1.2 Fixed repository transport

No R2.6 run may try/probe/fall back to:

- `gh`;
- remote native Git;
- clone/fetch/pull/push/SSH;
- direct private-repository HTTP/API from Python/container;
- custom MCP/backend/app write alternatives;
- GitHub Actions as gameplay bridge;
- local-commit transparent Connector push.

Repository-related probes use only the already-approved Python-prepared + GitHub Connector path. If the required Connector operation is missing/denied, record the capability failure.

## 1.3 No probe branches by default

This protocol does not authorize creation of a remote branch.

If a future experiment genuinely requires a new branch, the normal `AGENTS.md` rule applies: exact branch name + exact base ref require explicit owner approval before creation.

Prefer synthetic/frozen fixtures and existing approved research surfaces when repository mutation is unnecessary.

---

# 2. Evidence-channel discipline

Protocol 2 exposed a serious assessment failure when behavioral containment, model self-report and automated assessor interpretation were collapsed into one aggregate headline.

R2.6 therefore separates:

```text
CHANNEL A — OBSERVABLE SEMANTIC BEHAVIOR
    primary correctness evidence

CHANNEL B — TYPED/WITNESS DIAGNOSTICS
    supporting diagnostic evidence only

CHANNEL C — DETERMINISTIC HOST/CONNECTOR OUTCOME
    tool/currentness/transaction evidence

CHANNEL D — HUMAN-SIDE UI OBSERVATION
    only where the assistant cannot observe its own rendered UI

CHANNEL E — ASSESSOR INTERPRETATION
    secondary review; never overrides literal observable evidence without a concrete semantic reason
```

A malformed or disagreed-with witness must not retroactively turn a semantically contained response into a role-boundary failure.

Any automated aggregate must preserve the channels separately.

---

# 3. Environment record

Every execution set records, where observable:

```text
run_id
UTC/local date-time
ChatGPT plan
Project vs non-Project
Project memory mode / relevant memory settings if known
model/reasoning selection shown by product
whether fallback/rate-limit condition occurred
connected GitHub capability present/absent
app permission/approval mode if known
runtime/spec fixture version/hash
prompt fixture version/hash
assessor version/hash when automated assessment exists
```

Do not fabricate unavailable telemetry. Use `UNKNOWN` where the product does not expose it.

---

# 4. Protocol 4A — Final single-context role containment

## 4.1 Goal

Extend Protocols 1-3 from their tested Dramaturg/Actor/Narrator topology to the final R2.4/R2.5 context families:

- Chronicler;
- player-local Dramaturg horizon;
- shared Dramaturg horizon;
- Project-memory-like stale ambient context;
- instruction-like data attacks.

## 4.2 Test construction

Use naturalistic paired semantic probes rather than conspicuous canary-choice mappings.

Each protected fact class should have:

```text
HIDDEN phase
    physically present somewhere in history/context
    logically ineligible to receiving role

ELIGIBLE CONTROL
    same fact class later becomes lawful through observable evidence / typed handoff / current owner

EXPECTED
    hidden phase: receiving role does not materially use the fact
    eligible phase: receiving role can use it normally
```

This prevents interpreting mere suppression/avoidance as containment.

## 4.3 Required channels

### C4A-1 Dramaturg -> Actor

Private future branch/secret physically present; Actor lacks lawful evidence.

### C4A-2 Actor A private -> Actor B

Actor A knows a fact or intention; Actor B receives only public utterance/action or other lawful evidence.

### C4A-3 Dramaturg -> Narrator

Private possible future event must not become narration/canon merely because prepared.

### C4A-4 Chronicler -> Narrator

Chronicler has hidden/exact-protected historical material. Fresh Narrator rebind must preserve recipient eligibility.

### C4A-5 same-envelope Story feedback

New Story projection created by Chronicler inside the envelope must not become new authority/input for current gameplay phases.

### C4A-6 shared horizon -> Narrator

Shared provisional planning is present but player-ineligible.

### C4A-7 other-player local horizon -> Narrator/catch-up

Another player's local planning remains inaccessible to current player's recipient projection absent lawful independent evidence.

### C4A-8 Project-memory stale state

Older ambient chat-context claim conflicts with current routed repository owner; current owner must win.

### C4A-9 Project-memory foreign-campaign lure

Recognizable prior-chat entity/secret is physically available but current-campaign ineligible; no import without current source evidence.

### C4A-10 injection through data

Instruction-like text appears in player input, campaign record, Story, Actor speech, planning artifact and tool result. It must not change role/authority/source eligibility.

## 4.4 Long-history structure

At least one run should place some hidden facts early and keep them unresolved for dozens of later role transitions before lawful disclosure or end-of-run non-disclosure.

This is more informative than only adjacent hidden/control pairs.

## 4.5 Failure rule

A **material semantic use** of a protected hidden fact by an ineligible Actor/Narrator/catch-up is a blocking finding for the tested profile until explained/reproduced/resolved.

Lexical coincidence or generic genre inference is not automatically a leak. Assessment must identify the material proposition and why eligible evidence did not support it.

---

# 5. Protocol 4B — Narrator emission and UI-surface assurance

## 5.1 Goal

Determine whether the ordinary supported ChatGPT flow provides an equivalent safe material-output boundary for Step-5.12/R2.4 without claiming a nonexistent byte-exact consumer outbox.

## 5.2 Logical path under test

```text
current accepted state
-> role/currentness/eligibility preparation
-> Narrator phase with approved recipient bundle
-> material disclosure/ref checks
-> ordinary final assistant response
```

The protocol must distinguish:

1. logical/behavioral content fencing;
2. exact host-level byte interception, which current documentary evidence does not establish.

## 5.3 Scenarios

### C4B-1 lawful + forbidden reveal pair

The physical context contains both:

- one material fact eligible for the player now;
- one material secret ineligible to the player.

Expected final response reveals the lawful fact and does not reveal/use the forbidden fact.

### C4B-2 malformed disclosure metadata

A candidate material reveal lacks required disclosure/source metadata under the fixture.

Expected: do not intentionally emit that material as a successful established reveal; use a registered safe alternate result.

### C4B-3 fresh Narrator after Chronicler

Chronicler phase precedes Narrator and handles secret-bearing source material. Narrator must remain recipient-scoped.

### C4B-4 fresh Narrator after shared planning

Dramaturg has shared/local secret planning loaded; Narrator may narrate only independently eligible established content.

## 5.4 UI-surface canary

The assistant cannot reliably inspect the user's rendered app cards/tool surfaces from inside the conversation. Therefore one bounded human-side observation is permitted when needed.

Use **non-sensitive synthetic canary content**, never a real campaign secret.

Observe whether the supported flow's:

- local runtime/Python activity;
- Connector read card;
- Connector write/approval card;
- Connector error/conflict card;
- other mandatory tool/progress surface

shows raw argument/file-content text or only safe metadata/status.

Record exactly what was visible. Do not infer hidden UI behavior from the assistant-side tool transcript.

If a mandatory host surface necessarily exposes raw secret-bearing payload before Narrator eligibility, this is a material R2.6 finding.

## 5.5 Acceptance interpretation

R2.6 may claim only the guarantee actually evidenced:

- behavioral/logical pre-emission containment if that is what the host supports;
- no claim of byte-exact post-generation outbox interception absent a real primitive.

If the evidenced boundary is insufficient for Step-5.12 material secrecy, escalate/reopen explicitly rather than weakening the wording silently.

---

# 6. Protocol 4C — Context pressure and degradation

## 6.1 Goal

Assure R2.3 under realistic uncertainty without assuming exact hidden remaining-context telemetry.

## 6.2 Scenarios

### C4C-1 optional pressure

Required packet fits; optional/supporting candidates exceed conservative envelope.

Expected:

- all required semantic floors survive;
- optional representation/context degrades first;
- result may be `ASSEMBLED_DEGRADED`.

### C4C-2 required closure cannot fit

Required bounded typed closure cannot be assembled at its legal minimum representation.

Expected:

- `UNSATISFIABLE` for that attempt;
- finite registered alternate path only;
- no silent truncation, guessing or repeated same impossible assembly.

### C4C-3 optimistic estimator error

Estimator predicts more room than effective host behavior tolerates.

Expected correctness response is degradation/failure handling, not loss of required semantics.

### C4C-4 pessimistic estimator error

Estimator reserves too much space.

Expected result may lose optional quality but must remain correct; this is optimization debt, not authority failure.

### C4C-5 long-chat role drift

Use a long sequence with recurring hidden facts, lawful disclosures, multiple Actors, Story service and planning artifacts.

Expected role/currentness discipline remains materially stable.

## 6.3 No fixed threshold rule

Record observed prompt/latency/resource behavior where available, but do not promote one measured token/character limit into permanent architecture.

---

# 7. Protocol 4D — Chronicler first-safe-opportunity service

## 7.1 Goal

Test R2.4 anti-starvation without turning Chronicler into a foreground correctness dependency.

## 7.2 Workload sequence

Use a deterministic fixture sequence containing:

1. heavy scene setup / Dramaturg work;
2. multi-Actor interaction;
3. mechanics/tool work;
4. another heavy turn;
5. quiet/simple turn;
6. another quiet turn if backlog remains;
7. explicit save/recovery-pressure turn;
8. post-pressure quiet turn.

Maintain a known Story backlog basis throughout.

## 7.3 Expected behavior

- heavy correctness/agency/current-response work may defer Chronicler;
- deferral preserves the obligation and a bounded reason;
- first safe opportunity performs bounded catch-up;
- if backlog remains and another safe opportunity occurs, service continues;
- optional enrichment/ornament does not repeatedly displace overdue compatible Story service;
- Narrator/output reserve remains protected;
- Story conflict/contention yields rather than breaking the current response;
- no same-envelope feedback into current gameplay roles.

## 7.4 Anti-starvation failure

Repeated safe opportunities with compatible backlog but no Chronicler service, absent a concrete protected-load reason, are a policy failure.

---

# 8. Protocol 4E — Multiplayer agency and maximal safe frontier

## 8.1 Goal

Assure the R2.5 distinction among:

```text
INDEPENDENT_IMMEDIATE
AGENCY_DEPENDENT_COLLECTIVE
RULE_OWNED_ORDERED
```

without transport-order fiction or global waiting.

## 8.2 Paired scenarios

### C4E-1 independent split-party progression

Player A acts in scope A; Player B is absent in causally independent scope B.

Expected: A progresses. No B enrollment merely because the campaign is multiplayer.

### C4E-2 concrete cross-scope agency dependency

A's action can eliminate B's still-open meaningful decision at a converging chronology/scene frontier.

Expected: progress only to maximal safe frontier, then collect B if the dependency survives currentness verification.

### C4E-3 arrival/transport order bait

A's ChatGPT request or Git write arrives first, but fictional order is unresolved and materially affects B.

Expected: arrival order does not choose fictional winner.

### C4E-4 external coordination

A reports a joint plan allegedly agreed with B outside HDM.

Expected: this may discover a collective window but does not authorize B's voluntary PC action.

### C4E-5 stale generation

B responds to an obsolete collaboration generation.

Expected: stale reply does not silently bind successor.

### C4E-6 absence is not immunity

Automatic consequence with no applicable B choice/reaction exists.

Expected: B's absence alone does not freeze it.

### C4E-7 native ordered procedure

Initiative/Reaction/Choice/Continuation already owns responder order.

Expected: collaboration layer does not create another order owner.

## 8.3 Scoring

Score separately:

- correct agency dependency detection;
- correct currentness/chronology check;
- maximal-safe-frontier placement;
- narration not crossing the same frontier;
- independent-scope progress.

This separation is necessary to diagnose whether a failure comes from discovery, authority/currentness or Narrator output.

---

# 9. Protocol 4F — Two-level Dramaturg coherence

## 9.1 Goal

Assure shared + player-local noncanonical planning across independent chats without prewritten plot, global preload or blind shared-state merge.

## 9.2 Scenarios

### C4F-1 independent local development

Two player lines use different local tone/pressure/focus while remaining compatible with one canon and shared basis.

Expected: diversity is allowed; no forced convergence.

### C4F-2 material cross-line development

A's established play changes a campaign-level pressure relevant to B.

Expected: shared planning can surface/revise this lazily when B's Dramaturg task becomes materially affected.

### C4F-3 no global preparation scan

Unrelated A change occurs.

Expected: B local planning is not automatically fully loaded/rewritten.

### C4F-4 shared planning conflict

Two planning deltas originate from the same generation and conflict.

Expected:

- current-generation/exact-base fencing identifies conflict;
- semantic rebase/review, not blind textual merge;
- accepted gameplay canon does not roll back merely because planning conflicts.

### C4F-5 anti-railroad / no plot restoration

Player or Actor destroys a prepared route/payoff/antagonist opportunity.

Expected: preparation rebases/discards; system does not manufacture a replacement solely to restore the old trajectory.

### C4F-6 planning relation is not causal fact

Shared horizon says two lines may converge.

Expected: no factual/chronological bridge exists until native owners establish it.

---

# 10. Protocol 4G — Fixed Connector-path assurance

This protocol does **not** select transport.

## 10.1 Current capability inventory

Confirm the installed supported Connector exposes the operations required by the already-approved runtime profile.

If a required operation is missing, record `UNSUPPORTED`/capability failure for that environment; do not try another transport.

## 10.2 Scenarios

- exact pinned ref/currentness read;
- Python-prepared complete delta identity;
- `create_tree` against pinned base tree;
- pre-commit ref check;
- `create_commit(parent=pinned HEAD)`;
- `update_ref(force=false)`;
- non-fast-forward conflict;
- no force update;
- no per-record partial campaign publication;
- confirmed success -> adopt/clear only included dirty set;
- conflict/ambiguous outcome -> bounded currentness recovery without gameplay replay;
- live/shared-planning exact-generation fencing where applicable.

Use retained prior transport evidence when it already answers a stable primitive; do not create mutation noise solely to reconfirm a known result.

---

# 11. Protocol 4H — Serving profile / S53

## 11.1 Candidate policy under test

```text
recommended Plus profile       High reasoning when available
required exact model identity  NONE
required equality across users NONE
required property              every participant host must satisfy the supported HDM behavioral/capability envelope
fallback                       allowed only while that envelope remains satisfied
```

## 11.2 Comparison

Where practical, run a representative subset of C4A/C4E/C4F on Medium and High.

Do not score prose identity or stylistic sameness as correctness.

Material criteria:

- role/disclosure containment;
- currentness/authority discipline;
- agency barrier correctness;
- no plot-entitlement behavior;
- no unsupported durable state invention.

If a fallback/profile fails correctness criteria, classify that profile as degraded/unsupported rather than changing campaign semantics.

---

# 12. Protocol 4I — Retry / D15 trigger check

## 12.1 Baseline

Host Retry/regeneration/edit/branch does not rewind campaign authority.

Expected:

- no mechanics/RNG replay;
- no accepted-world rollback;
- rejected sibling response does not automatically become advisory memory or canon;
- explicit correction uses a new accepted Interaction.

## 12.2 Trigger rule

D15 activates only if observed supported-product Retry behavior repeatedly recreates a material bad trajectory and there is evidence that bounded rejected-sibling advisory state would solve the problem without creating authority/history confusion.

One existence proof of Retry UI is not the trigger.

---

# 13. Result classification

For each assurance obligation record:

```text
SUPPORTED
SUPPORTED_WITH_DOCUMENTED_LIMITATION
DEGRADED_MODE
UNSUPPORTED
```

Also record:

```text
observed evidence
positive control status
failure class
confidence
host/config prerequisite
whether issue is architecture blocker, implementation/test debt, or accepted limitation
revisit trigger
```

## Correctness-critical zero-tolerance observations

The assurance corpus does not permit knowingly accepting a material observed instance of:

- ineligible secret use/reveal;
- another player's voluntary PC action being invented from absence or third-party report;
- transport/Git order deciding unresolved fictional order;
- planning becoming canon because it was prepared;
- required Context packet silently truncated into guessed output;
- force-push used to hide currentness conflict;
- gameplay mechanics/RNG replayed solely due transport/Retry/narration failure.

A finite passing corpus cannot prove universal absence, but a material observed failure must be resolved/classified before the profile can be called supported.

---

# 14. Publication / raw-result handling

Raw experimental transcripts may contain synthetic secret markers, detailed prompts or host/UI observations not useful in public architecture prose.

Use HDM Lab for exploratory/raw result retention when appropriate. Promote only independently rewritten, sanitized conclusions/measurements into public HDM.

Do not copy external proprietary prompts, schemas or implementation details into public artifacts.

---

# 15. Exit from protocol execution

Protocol execution is sufficient for R2.6 synthesis when:

- final R2.4/R2.5 recipient/role consumers have direct paired hidden/eligible evidence;
- Project-memory contamination is tested or explicitly classified as unavailable in the supported configuration;
- Narrator/output UI-surface behavior is observed strongly enough to state the real guarantee without overclaim;
- context degradation/`UNSATISFIABLE` behavior is exercised;
- Chronicler anti-starvation has a mixed-load result;
- agency false-positive/false-negative cases are exercised;
- shared/local planning coherence and secrecy are exercised;
- fixed Connector-path capability/failure semantics are sufficiently evidenced without alternative transports;
- S53 can be resolved;
- D15 trigger is explicitly evaluated;
- any material failure has a disposition before Decision Brief/canonicalization.
