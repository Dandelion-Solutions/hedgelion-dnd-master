# HDM Product Owner Input Process

Status: **CANONICAL HDM PROCESS ADDENDUM**

Purpose: preserve Product Owner intent that appears outside the currently active work package, route one input across multiple present/future owners when necessary, and prevent autonomous architecture work from either losing product requirements or silently making Product Owner decisions.

Primary ledger:

- `DEV/PRODUCT_OWNER_INPUT.md`

This addendum supplements `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It does not weaken their evidence, Source Manifest, critic, Senior-review, sequencing, or human/agent decision-rights gates.

---

## 1. Authority boundary

`DEV/PRODUCT_OWNER_INPUT.md` is authoritative for **preserved Product Owner intent and verbatim Product Owner-authored input**.

It is NOT:

- accepted architecture merely because an idea is recorded;
- a runtime/gameplay instruction;
- a replacement for canonical owner decisions/specifications;
- a second roadmap/current-progress authority;
- an instruction to activate every routed future consequence immediately.

Accepted architecture remains in its normal owners/specifications. `DEV/CURRENT_PROGRESS.md` remains the sole global current-progress authority. Roadmaps own sequencing/scope, not the Product Owner ledger.

When agent interpretation or routing metadata conflicts with preserved Product Owner text, the preserved Product Owner text wins as evidence of intent and the agent metadata must be repaired. When accepted architecture appears to conflict with later Product Owner intent, reconcile the actual owners and classify the delta before changing either side.

---

## 2. What must be captured

Create or amend a ledger entry when the Product Owner supplies a material:

- product requirement;
- gameplay/user-facing semantic rule;
- correction to earlier product intent;
- program-direction change;
- explicit reopen request;
- scope/non-goal change;
- compatibility/lifecycle/risk preference;
- idea that may affect a later stage even when it is not current work.

Do not fill the ledger with casual conversation, purely mechanical implementation instructions, transient debugging detail, or ideas that have no plausible product/architecture/program consequence.

When one Product Owner message contains several independently routable requirements, split them into separate entries while preserving any shared verbatim context once and referencing it from all affected entries.

---

## 3. Verbatim Product Owner preservation

Product Owner-authored blocks are immutable to agents.

Agents MUST NOT polish, translate, normalize, shorten, expand or silently correct the text inside `PO input`, Product Owner correction/amendment, or explicitly shared verbatim context blocks.

Agent-owned interpretation/routing/status text is deliberately separate and may evolve.

When the Product Owner later corrects an input:

```text
preserve original immutable block
+ append new immutable Product Owner correction/amendment
+ update agent-owned disposition/routing
```

Do not rewrite the original to manufacture a cleaner historical narrative. Normal Git history is sufficient audit history; no extra integrity mechanism is required.

Public-material/privacy/legal rules override verbatim persistence where necessary. Never commit secrets, credentials, sensitive personal data, unlawful confidential material or prohibited third-party proprietary text just because it appeared in a Product Owner conversation.

---

## 4. Agent-owned routing and disposition

After capture, the AI architect owns the technical reconciliation work:

1. inspect current owners and consumers;
2. classify whether the input is already satisfied, a new consumer, an extension, a contradiction, or a material insufficiency;
3. determine affected current and future WPs/stages/owners;
4. record explicit activation/revisit triggers for future routes;
5. recommend/produce the correct accepted owner decision or specification when product semantics are already explicit;
6. surface only residual questions that genuinely require Product Owner judgment.

Useful relationship classification against closed/current architecture:

```text
NO DELTA / ALREADY SATISFIED
NEW CONSUMER
EXTENSION
CONTRADICTION
MATERIAL INSUFFICIENCY
```

Keyword/topic overlap does not reopen accepted architecture. A closed owner reopens only when the later input or evidence actually contradicts it, adds a consumer it cannot satisfy, or establishes material insufficiency under the existing HDM reopening rules.

---

## 5. One input may route to many stages

A Product Owner input is not required to belong to exactly one WP/stage.

For cross-cutting input, preserve one coherent original entry and record multiple routing targets. Each target may have an independent state and trigger.

Example shape:

```text
PO-XXX
    current semantic owner decision      -> INCORPORATED
    active WP consumer                    -> ACTIVE / PENDING
    future architecture consumer          -> DEFERRED until its stage
    implementation/test realization       -> DEFERRED until planning/execution gate
```

Do not duplicate or paraphrase the Product Owner input into multiple independent “original” entries merely because several stages consume it.

---

## 6. Coverage does not imply activation

Recording a future consequence is not authorization to begin it.

A routed/deferred item must preserve:

- target owner/stage where known;
- why it belongs there;
- activation/revisit trigger;
- current non-activation reason;
- any upstream accepted semantic owner it must later consume.

A new Product Owner idea that belongs wholly to a later stage normally leaves the current cursor untouched.

If the input materially affects the currently active WP/stage, integrate it through that stage's normal process. If it does not, route it and continue the authorized current work.

---

## 7. Required lookup at architecture boundaries

At the start/recovery of every HDM architecture WP/stage, the architect must inspect the ledger's active routing index and the full applicable entries whose routes, owners or activation triggers intersect the task-specific dependency subgraph.

Do NOT preload the entire historical ledger merely because it exists. Use the active index, target/owner routing and current stage to identify the relevant entries.

Applicable Product Owner ledger entries are part of the task-specific Source Manifest/evidence set as **PRODUCT OWNER INTENT / REQUIREMENT INPUT**, distinct from canonical architecture authority.

Before claiming a Task Brief, Decision Brief, candidate specification, canonical result or coverage closure complete, verify that every applicable ledger route is dispositioned as one of:

```text
INCORPORATED
ACTIVE / addressed by current artifact
DEFERRED with valid trigger
NOT APPLICABLE with rationale
SUPERSEDED by later explicit Product Owner input
NEEDS_PO
```

---

## 8. Critic obligations

Both mandatory HDM architecture critics must inspect applicable Product Owner input routes as part of whole-project reconstruction.

A critic must explicitly test whether:

- a current Product Owner input was omitted from framing/candidate scope;
- agent interpretation changed the Product Owner's meaning;
- one cross-stage input was incorrectly collapsed into only one consumer;
- a future/deferred route was prematurely activated;
- an accepted owner already satisfies the requirement;
- a new consumer exposes real insufficiency in accepted architecture;
- a genuine unresolved Product Owner decision has been hidden as a technical default.

`NEEDS_PO` on an applicable route is blocking for dependent architecture. A critic cannot return PASS for architecture that silently resolves an identified Product Owner decision.

An entry may remain globally `PARTIALLY_INCORPORATED` because another route is legitimately future/deferred; that alone does not block the current critic. Blocking is determined by the state of the route applicable to the current scope.

---

## 9. New Product Owner input arriving mid-stage

When new Product Owner input arrives after a Task Brief/critic/candidate/review checkpoint:

1. record the input before relying on conversational memory;
2. classify whether it materially affects the current stage or only future routes;
3. if it affects the current stage, invalidate only the review/critic/coverage claim whose evidence basis did not include it;
4. return to the earliest process point necessary to incorporate the new requirement honestly;
5. retain already-valid findings/owners that are not contradicted;
6. do not reopen unrelated closed architecture merely because the new input overlaps its topic;
7. do not begin implementation merely because the new product requirement is now known.

This is an evidence-basis correction, not permission to erase history or restart the project.

---

## 10. Product Owner hard-stop semantics

After technical evidence work, mark `NEEDS_PO` only when a genuine unresolved Product Owner judgment remains, such as:

- product/user semantics;
- material priority/quality trade-off;
- explicit risk acceptance;
- hard-to-reverse lifecycle/scope behavior;
- meaningful compatibility policy;
- canonical authority/ownership choice that remains genuinely reasonable either way;
- another human-owned decision under `DEV/DESIGN_PROCESS.md`.

Before asking, the agent must provide decision-ready facts, alternatives, consequences, recommendation, uncertainty and the exact residual decision.

A generic `continue`, `Продолжай`, or similar continuation after an interruption does NOT resolve an identified `NEEDS_PO` item.

Conversely, when the Product Owner's input already clearly settles the product semantics, do not manufacture a second approval request. Formalize the decision, route the technical consequences, and continue within the authorized process.

---

## 11. Incorporation and downstream authority

When Product Owner intent is accepted/formalized into a canonical owner decision/specification:

- retain the original ledger entry permanently as intent/provenance;
- link the accepted owner as incorporation evidence;
- update routing states;
- downstream architecture/implementation consumes the accepted owner, not the ledger as if it were a runtime spec.

`INCORPORATED` means current product intent has an accepted semantic owner and every known downstream route is either incorporated or safely deferred with a valid trigger. It does not mean all future implementation has already happened.

Do not delete incorporated entries merely to keep the ledger short. Keep the active routing index compact and allow historical incorporated entries to remain below it.

---

## 12. Relationship to current progress and roadmaps

The ledger does not move `DEV/CURRENT_PROGRESS.md` by itself.

Update current progress only when a Product Owner input actually changes the truthful current stage/gate, for example because:

- a current review basis becomes incomplete;
- a `NEEDS_PO` gate blocks the active stage;
- an explicit program-direction decision changes the authorized sequence;
- the current stage must incorporate a newly applicable requirement before proceeding.

Update the roadmap only when intended sequencing/scope/dependencies change. Merely routing an idea to an already existing future stage does not require roadmap churn.

---

## 13. No duplicate communication channel required

HDM does not require a separate mailbox conversation between Product Owner and architect.

The normal direct Product Owner/architect conversation is the input channel. The ledger is the durable repository record that prevents requirements from being lost across sessions, stages, model/tool interruptions or future agent handoffs.

The architect is responsible for recording and routing material Product Owner input without requiring the Product Owner to restate it later.
