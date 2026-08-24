# R2.4 Adversarial Review — Single-Context Turn Envelope and Chronicler Service

Status: **ADVERSARIAL REVIEW — REQUIRED AMENDMENTS IDENTIFIED / NO NEW OWNER DECISION**

Date: 2026-08-24

Reviewed candidate:

- `2026-08-24-r2-4-single-context-llm-execution-candidate-spec.md`

Owner-approved direction remains:

> **Registered Turn Envelope + Minimal Typed Gateways + first-safe-opportunity Chronicler service**

## 1. Review question

Can the candidate preserve one-context role containment, deterministic authority, Story non-authority, first-safe-opportunity Chronicler service and low ordinary-turn overhead without introducing a new scheduler, hidden feedback loop, replay edge or player-visible leakage path?

Result:

> **YES, after the amendments below. None requires a new product/owner trade-off.**

---

## AR-1 — Same-envelope Chronicler -> gameplay feedback loop

### Attack

The candidate permits Chronicler service before the final Narrator phase. A newly generated/published Story unit could therefore remain physically present and be treated by Narrator, Actor or Dramaturg as a fresh summary/evidence source in the same TurnEnvelope.

This creates an avoidable self-amplification loop:

```text
admitted source
    -> Chronicler prose
    -> Story
    -> same-turn gameplay role treats Story as new input
```

Even though Story is noncanonical, this can amplify unsupported wording, broaden emphasis, or leak broader Chronicler source material into a narrower role.

### Required amendment

Add a **NO SAME-ENVELOPE STORY FEEDBACK** law:

- Story created/changed by a Chronicler service slot in the current TurnEnvelope is not admitted as a new gameplay-role input in that same TurnEnvelope;
- subsequent Interpreter/Dramaturg/Actor/Narrator phases use their independently assembled eligible source basis and typed handoffs;
- newly published Story becomes ordinary retrieval/orientation input only in a later eligible assembly cycle, unless a separate explicit maintenance/Commentator mode contract says otherwise.

This is consistent with R2.1 Story non-authority and R2.3 source assembly.

Disposition: **BLOCKING WORDING DEFECT / AGENT-LEVEL FIX**.

---

## AR-2 — Service checkpoint accidentally tied to deterministic gameplay execution

### Attack

The candidate diagram places Story service after `deterministic execution / accepted state`.

A quiet roleplay turn, clarification turn or OOC-compatible gameplay turn may have no material deterministic execution. If implementation reads the diagram literally, these low-load turns — often the best Chronicler opportunities — could skip the service check.

### Required amendment

Define Chronicler opportunity evaluation as an **envelope-level pre-emission service checkpoint**, not as a child of successful mechanics/state execution.

It occurs once current-turn mandatory requirements and protected Narrator/output reservation are known, regardless of whether the turn contained mechanics, Actor work, Dramaturg work or state mutation.

Disposition: **BLOCKING PLACEMENT AMBIGUITY / AGENT-LEVEL FIX**.

---

## AR-3 — Durable Story must not outrun its admitted source basis

### Attack

A live turn may contain established HOT/SOFT current state newer than durable Git. If Chronicler were allowed to publish durable Story from merely physically present/unpublished state without the applicable Step-5.10 source contract, Story could become durably ahead of the evidence it cites or depend on a source lost at crash recovery.

Story is noncanonical, but source-bound provenance/restart/catch-up semantics would be damaged.

### Required amendment

Chronicler service may process/publish only source candidates admitted by the applicable Step-5.10 `StoryProjectionSourceContract` at a compatible source basis.

Merely being present in the current TurnEnvelope or HOT state does not make material eligible for durable Story publication.

If a source must first cross an existing durability/admission prerequisite, Story service for that candidate waits or participates only through the owning coherent publication contract if explicitly allowed there.

Disposition: **BLOCKING SOURCE-BASIS CLARIFICATION / AGENT-LEVEL FIX**.

---

## AR-4 — Story contention cannot consume protected Narrator latency

### Attack

Step 5.10 puts Story and campaign state on one ref. A Story publication CAS conflict immediately before Narrator could create retries that consume the response margin, contradicting the owner requirement that loaded current play wins.

### Required amendment

For ordinary TurnEnvelope service:

- Story work remains bounded;
- Story publication conflict/retry obeys Step-5.10 gameplay-priority/yield law;
- once the current turn's protected Narrator/output margin would be threatened, Story service terminates/defer for this envelope rather than blocking visible response completion;
- no Story retry may replay accepted gameplay mechanics/RNG.

Disposition: **REQUIRED PRIORITY CLARIFICATION / AGENT-LEVEL FIX**.

---

## AR-5 — Chronicler -> Narrator is a new concrete containment channel

### Attack

Protocols 1–3 strongly tested Dramaturg/Actor/Narrator and multiple Actor epistemics. The new owner requirement makes Chronicler a recurring internal role that may read broad historical material immediately before a narrower Narrator phase.

This is a new concrete consumer pattern even though it uses the same general containment law.

### Required amendment

R2.6 must include dedicated Chronicler->Narrator containment/adversarial cases:

- Chronicler sees player-ineligible historical/Story source material;
- Narrator later in the same physical turn must not expose or materially rely on it unless independently eligible;
- positive controls make the same material lawfully eligible later;
- newly generated Story text in the same TurnEnvelope must not become Narrator evidence under AR-1.

This is evaluation scope, not a new architecture decision.

Disposition: **DOWNSTREAM ASSURANCE REQUIREMENT**.

---

## AR-6 — Per-turn backlog check must not become an unbounded Story scan

### Attack

"Evaluate Story backlog every TurnEnvelope" could be implemented by enumerating Story/history every turn, defeating the latency/context goals and turning Chronicler scheduling into a campaign-size cost.

### Required amendment

The service-opportunity check must use Step-5.10 compact typed coverage/source-basis metadata sufficient to answer whether compatible backlog exists and select a bounded candidate window.

Full source bodies/Story history are loaded only after `SERVICE(window)` is selected and only for that bounded window.

Disposition: **PERFORMANCE/CORRECTNESS CLARIFICATION / AGENT-LEVEL FIX**.

---

## AR-7 — Deferral reason must remain operational, not durable scheduler state

### Attack

A typed `DEFER(reason)` could accidentally grow into a persistent job lifecycle or become a second source of whether Story work remains owed.

### Required amendment

`DEFER(reason)` is turn-local trace/control evidence unless an existing diagnostic surface independently retains it. The durable/recomputable fact that work remains owed is still only Step-5.10 source basis minus compatible coverage.

Disposition: **YAGNI CLARIFICATION / AGENT-LEVEL FIX**.

---

## AR-8 — Narrator rebind must occur after broad Chronicler work

### Attack

If implementation assembles/reuses a Narrator role frame before Chronicler, executes broad Chronicler work, and then resumes Narrator without explicit rebind, the phase boundary becomes ambiguous and private Chronicle material can influence presentation.

### Required amendment

Whenever Chronicler/Story service executes before Narrator, Narrator must undergo a fresh explicit logical phase rebind after the service slot. Its eligible `RoleContextBundle`/typed handoffs remain independently controlled by R2.3 and AR-1.

Disposition: **ROLE-CONTAINMENT CLARIFICATION / AGENT-LEVEL FIX**.

---

## 2. Rejected adversarial overreactions

The findings do **not** justify:

- returning to mandatory separate model calls/physical isolation;
- a durable Story job queue;
- persistent per-turn deferral ledger;
- Story commit after every gameplay response;
- a deterministic checkpoint FSM for every role;
- making Story current gameplay authority;
- blocking gameplay until Story is caught up.

---

## 3. Owner-decision check

No finding changes the approved product trade-off.

The owner already decided:

- current gameplay correctness and protected Narrator/output capacity outrank Story service under genuine load;
- Story service is mandatory at first safe opportunity;
- no scheduler/background-worker requirement;
- Alternative B is the baseline.

AR-1 through AR-8 specify the minimum safe realization of that decision.

No new owner decision is required.

---

## 4. Canonicalization recommendation

Canonicalize Alternative B only after incorporating all AR-1..AR-8 amendments into the canonical specification.

Before declaring R2.4 closed, verify:

- all R2.4 exit criteria;
- D16/S21/S28 disposition;
- Chronicler first-safe-opportunity service and anti-starvation;
- no same-envelope Story feedback;
- source-basis/durability compatibility;
- nonblocking Story contention;
- Narrator rebind after Chronicler;
- R2.6 Chronicler->Narrator assurance handoff;
- R2.7 machine-realization handoff.
