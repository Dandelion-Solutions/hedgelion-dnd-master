# Campaign House Rules — Step 3 Decision Brief

Status: **STEP 3 COMPLETE / DECISION AUTHORIZED BY OWNER GO FOR STEPS 2–8 / STEP 4 NEXT**

Date: 2026-08-25

Inputs:

- Step-1 Task Brief: `2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
- Step-2 research: `../design/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`
- owner authorization: senior architecture audit verdict **GO FOR STEP 2–8** and explicit instruction to complete the cycle before S6D.

---

## 1. Decision required

Choose the durable architecture for campaign House Rules / established rulings without:

- turning natural-language policy into a second mechanical rules engine;
- losing identity/currentness/recovery semantics in one undifferentiated prose blob;
- violating role/consumer information eligibility;
- creating a House-Rules-specific multiplayer synchronization frontier;
- allowing campaign prose to self-promote into system instruction or canonical state authority.

---

## 2. Alternatives

### A — Unstructured campaign Markdown only

Preserve only prose and let the Master search/read it as needed.

**Material benefit:** lowest authoring complexity.

**Material defect:** insufficient durable identity, revision/currentness, bounded retrieval, conflict/supersession, frozen-input and admission semantics. It also encourages full-corpus hot-path reads.

**Decision:** reject as complete architecture. Markdown remains a valid human/LLM-facing representation inside a stronger semantic envelope.

### B — Executable policy DSL / natural-language compiler

Represent House Rules as executable predicates/effects or compile prose into engine behavior.

**Material benefit:** apparent uniformity with deterministic mechanics.

**Material defect:** destroys the intended semantic judgment layer, duplicates Activity/Rule Element authority, formalizes criteria that are intentionally contextual, and creates a second path to mechanical authority.

**Decision:** reject.

### C — Lightweight semantic policy envelope + inherited runtime/currentness + typed deterministic handoff

Durable campaign policy has stable semantic identity/lifecycle/provenance/applicability material and LLM-readable normative content. R2.3 retrieves a bounded eligible packet. R2.4 treats the packet as admitted gameplay-policy data under constitutional instruction hierarchy. Existing Step-5 publication/currentness/recovery mechanisms make policy authoritative/current across sessions. Mechanical consequence crosses only existing typed deterministic boundaries.

**Decision:** accept.

---

## 3. Accepted decision

Adopt **Alternative C**.

### 3.1 Authority split

```text
HDM constitutional architecture
    constrains
campaign House Rules / established Rulings
    inform semantic interpretation/applicability
LLM / Master adjudication
    emits bounded typed result
existing deterministic capability
    validates / executes / owns RNG and state mutation
```

The policy layer is an authority for **campaign game-rule/adjudication meaning**, not for state mutation, RNG, event commit, repository currentness, truth/knowledge/disclosure or role authorization.

### 3.2 Durable semantic policy contract

A durable policy entry must have enough semantic identity to support:

- stable identity;
- kind: House Rule or established Ruling;
- active lifecycle and explicit supersession/retirement;
- bounded applicability/domain/scope discovery;
- normative policy content;
- adoption/provenance authority;
- current publication/revision identity sufficient for stale-context and recovery checks;
- explicit conflict handling where multiple active entries materially overlap.

This is a **semantic contract**, not approval of any specific JSON/YAML schema or executable language.

### 3.3 House Rule vs Ruling

- `House Rule`: deliberately adopted forward-looking campaign gameplay/adjudication policy.
- `Ruling`: reusable precedent retained from a concrete adjudication.
- a one-off adjudication remains ephemeral unless explicitly adopted;
- once validly adopted/published, both participate in the same campaign policy authority layer;
- separate physical stores are not required by architecture.

### 3.4 Precedence / legality

Interpretation order is constrained as follows:

1. constitutional HDM architecture and native owner invariants;
2. applicable current explicit campaign House Rule;
3. applicable current established campaign Ruling;
4. adopted baseline/structured rules sources within their owned semantics;
5. lawful local Master adjudication for remaining ambiguity/gap.

This is not permission for prose to override deterministic acceptance. If current campaign policy makes a baseline realization stale, the engine must either realize the current policy through a legal capability or surface a finite realization/catalog gap.

A same-level material conflict between current entries is not silently broken by model preference.

### 3.5 Information eligibility

The policy consumer receives only sources admitted by existing Step-4/R2.3 role/player/subject/purpose rules. Physical co-residence in one chat context does not grant use eligibility.

House Rules is not a truth, secret, lore, player-preference or policy mega-store. It may reference eligible canonical facts but never owns them by restatement.

### 3.6 Instruction/data fence

Admitted House Rule content is normative **campaign gameplay-policy data**. Authority comes from admitted/published policy identity, not from imperative wording or Markdown location alone.

It remains below host/project/CORE constitutional instruction authority. Quoted/example/source text inside a policy record does not self-promote to a rule or role-switch instruction.

### 3.7 Publication, currentness and recovery

Reuse Step-5.6/5.7/5.8 and R2.3/R2.5:

- authoritative publication, not local file existence, makes durable policy current;
- no House-Rules global epoch/frontier is introduced;
- a new affected Resolution must use current policy context before acceptance;
- another/joining/rejoining participant/session must acquire current routed policy context before its first affected mutable Resolution;
- stale policy context before acceptance fails/reassembles through inherited currentness behavior;
- policy inputs already accepted/frozen for a Resolution remain stable across retry/resume and later policy publication.

### 3.8 Typed deterministic handoff

Allowed semantic results include, where the existing consumer supports them:

- selection of an existing Activity/capability;
- binding legal typed parameters/targets;
- an admitted semantic applicability/classification fact;
- selection among already permitted deterministic consequences;
- purely narrative adjudication with no canonical mechanical mutation.

Forbidden:

- direct state mutation from policy prose;
- invented effect/activity/state owner;
- fabricated random result;
- bypass of deterministic validation/authorization/idempotency;
- using policy prose as a fallback transaction language.

Missing realization is `CATALOG GAP / POLICY-REALIZATION GAP`.

### 3.9 Retrieval

Use R2.3 registered bounded discovery/closure/currentness/eligibility/allocation. A derived policy index/cache may route candidates but is not authority. No ordinary-turn whole-policy-corpus scan is required as the architecture baseline.

### 3.10 Promotion

Promotion remains optional:

`one-off adjudication -> durable ruling/House Rule -> structured campaign mechanic -> generalized engine/core`.

Fundamentally contextual semantic policy may remain prose indefinitely.

---

## 4. Material trade-offs accepted by existing owner authorization

The accepted design adds small durable metadata/identity complexity to avoid much larger correctness costs from unstructured prose. It deliberately leaves exact machine schema/storage syntax for realization work so the design does not become schema-first.

It also accepts that some mechanically meaningful campaign policies may temporarily expose a catalog/realization gap rather than being executable immediately. This is preferable to silently granting the LLM mechanical authority.

No new human decision is required because these trade-offs are direct consequences of the already owner-approved Step-1 semantics and the explicit GO to complete Steps 2–8.

---

## 5. Decision gate

`DECISION: ALTERNATIVE C — ACCEPTED`

`OWNER_GATE: SATISFIED BY EXPLICIT GO FOR STEP 2–8`

`NEW_PRODUCT_SEMANTIC_DECISION_REQUIRED: NO`

Next: **Step 4 — Collaborative Architecture Review**.
