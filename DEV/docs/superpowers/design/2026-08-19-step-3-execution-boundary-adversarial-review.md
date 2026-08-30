# Step 3 Adversarial Architecture Review — Deterministic Execution Boundary

Status: **ADVERSARIAL REVIEW COMPLETE — AMENDMENTS REQUIRED / NO NEW HUMAN TRADE-OFF FOUND**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed candidate:

- `2026-08-19-step-3-execution-boundary-candidate-spec.md`

Approved owner decision under review: **Alternative C**.

## 1. Review method

The review attacked the candidate for:

- duplicate state authority;
- lost mandatory consequences after commit/retry/crash;
- ambiguous parent/child execution ownership;
- stale reaction resume;
- procedure-state copying;
- idempotency holes;
- trace/event compaction dependencies;
- arbitrary ordering disguised as determinism;
- LLM authority leakage;
- catalog-context drift;
- cross-stage deferrals that are unsafe to postpone;
- narrative/history data accidentally becoming mechanical truth;
- unnecessary new runtime classes/workflow abstractions.

The strongest alternative considered was a more uniform persistent execution-chain/workflow object that owns Commands, Resolutions, Segments and children. It would make some recovery bookkeeping easier, but it duplicates lifetimes already owned by RuntimeCommand/Resolution/Continuation/Procedure and would immediately grow into a generic workflow subsystem. The candidate remains preferable if the concrete gaps below are repaired without adding that class.

## 2. Verdict summary

```text
CRITICAL findings   0
MAJOR findings      4
MODERATE findings   5
MINOR findings      2
```

All MAJOR findings have a mechanically derivable resolution consistent with the approved Alternative C. No new material product/ownership trade-off requires owner escalation.

Recommendation: **AMEND candidate, then canonicalize if fresh review/verification passes.**

Confidence: **HIGH**.

## 3. MAJOR-1 — mandatory child work lacks one explicit closure owner

### Attack

The candidate allows post-commit Event triggers and child Resolutions but does not state strongly enough who keeps a root execution nonterminal until mandatory descendants close.

Failure scenario:

```text
segment commits damage Event
    -> mandatory post-damage save trigger exists
process crashes before child Resolution is durably materialized
```

If the root RuntimeCommand/Resolution is already considered settled/completed and trigger discovery is reconstructed later from a compacted trace or mutable current state, the consequence can be lost or duplicated.

### Resolution

Use the existing RuntimeCommand as the root execution-chain closure owner; do NOT add `runtime.resolution_chain`.

Normative amendment:

- every root execution has one `root_command_id`;
- root action Resolution and all mandatory descendant Resolutions carry/reference that root command;
- RuntimeCommand remains `ACCEPTED` until its own root execution and every mandatory descendant/pending obligation required for the command's mechanically complete outcome is closed, suspended with a durable continuation, or typed-blocked;
- only then does RuntimeCommand become `SETTLED`;
- an IntentClause is `executed` only when its root command has reached the corresponding mechanically complete disposition;
- optional/non-blocking presentation work does not hold mechanical completion open.

This gives one closure owner without inventing a workflow entity.

Disposition: **AMEND**.

## 4. MAJOR-2 — post-commit trigger can be lost between Event commit and child creation

### Attack

Creating a MechanicalEvent first and discovering/materializing mandatory children afterward creates a crash window.

It also creates timing ambiguity if the triggering segment removes/suppresses the binding source that should nevertheless respond at that Event timing.

### Resolution

The triggering segment SHALL atomically materialize enough child/pending-invocation evidence for every mandatory post-commit firing selected by the registered Event timing view.

Conceptually, in the same SQLite transaction as the Event batch:

```text
MechanicalEvent identity
+ selected post-commit firing descriptors
+ stable firing keys
+ child Resolution identity when immediately allocatable
  OR pending child invocation descriptor when not yet runnable
+ root_command linkage
```

The Event binding's registered timing semantics determine whether candidate collection observes the appropriate pre-state/prospective-post-state source availability. Later SQL/current-state discovery SHALL NOT decide whether the historical firing existed.

Child execution may happen after commit; child *obligation identity* may not be lost after commit.

Disposition: **AMEND**.

## 5. MAJOR-3 — chain-limit handling says “preserve pending work” without an owner

### Attack

The candidate correctly rejects silent trigger truncation but does not name the record that owns a blocked mandatory firing when a depth/total-work safety bound is reached.

### Resolution

Reuse the root command/Resolution closure state introduced by MAJOR-1.

A bound-hit SHALL atomically leave an embedded `pending_child_invocation`/equivalent descriptor under the root execution closure with:

```text
firing key
triggering occurrence/Event
binding identity
intended Activity identity
procedure/root command linkage
reason = execution limit
```

The current root command remains non-SETTLED and returns a typed blocked/maintenance/adjudication-required outcome. Already committed ancestors remain committed.

No standalone generic obligation/job class is introduced.

Disposition: **AMEND**.

## 6. MAJOR-4 — Effect recency evidence is too deferred to guarantee implementability

### Attack

The candidate requires a compact `application_order_key` but leaves encoding/cross-session behavior largely to Step 5. Step 3 implementation would still need a deterministic way to allocate a comparable key without relying on old Event bodies, wall time, Effect ID order, or a campaign-global total chronology.

### Simplest viable solution

Recency arbitration is scoped to a target + application family and only compares simultaneously nonterminal candidate applications.

Therefore allocate an immutable family-local episode ordinal atomically:

```text
new_order = 1 + max(application_order_key)
            over the complete nonterminal candidate set
            for (target, application family)
```

Rules:

- candidate-set completeness is a hydration/query precondition;
- suppressed but nonterminal candidates remain in the max set;
- terminal applications need not remain comparable after they leave the candidate set;
- refresh preserves the ordinal;
- replace computes a new ordinal while the replaced episode is still visible in the prospective candidate set, then atomically terminates old + creates new;
- several mechanically order-sensitive same-segment creations for the same target/family require registered ordering/adjudication rather than arbitrary operation-list order.

This removes dependence on global time, event retention, session counters, and cross-scene chronology for the ordinary local arbitration problem.

Disposition: **AMEND**.

## 7. MODERATE-1 — retry lookup can conflict after ambient catalog refresh

### Attack

The command fingerprint includes ResolvedCatalogContext identity. If an exact retry arrives after the host has adopted a newer compatible ambient context, naïvely rebinding first can produce a different fingerprint and falsely report `IDEMPOTENCY_CONFLICT`.

### Resolution

Idempotency lookup order SHALL be:

```text
lookup existing command/resume identity first
    if found:
        compare incoming normalized retry against STORED accepted input/context
        return stored result/current suspension on exact retry
    else:
        bind new request under current accepted ResolvedCatalogContext
```

Hydration retries do not change accepted command identity/fingerprint merely because additional records were loaded.

Disposition: **AMEND**.

## 8. MODERATE-2 — external reaction response versus new IntentPlan is ambiguous

### Attack

A player response such as “Shield” while a ReactionWindow is pending is not an ordinary unrelated new turn. Treating it automatically as a fresh IntentPlan risks losing the parent continuation generation/offer identity.

### Resolution

When an external response is solicited by a current ChoiceRequest/ReactionWindow, the host SHALL first interpret/bind it as a response to that pending continuation generation/offer.

The accepted response uses a stable resume identity tied to:

```text
continuation generation
+ choice/reaction offer identity
+ responder identity
+ selected bounded option/Activity
```

A reaction Activity may create a child Resolution under the same root command/procedure. Extra unrelated intent in the same user message may be parsed only after the pending response is resolved and must not be silently folded into the reaction child.

Disposition: **AMEND**.

## 9. MODERATE-3 — command closure versus narration timing is underspecified

### Attack

If host narration is generated immediately after the root segment but before mandatory post-commit descendants close, the model can narrate an outcome that a mandatory consequence changes moments later.

### Resolution

The execution API SHALL distinguish:

- mechanically complete/settled command receipt;
- suspended/blocked/follow-up-required command state.

Final outcome narration for one executable clause SHOULD normally be based on the mechanically complete receipt closure. Interim prompts for choices/reactions are presentation of suspension state, not final narration.

A host may intentionally narrate an already committed intermediate fact, but it must not present unresolved mandatory descendants as if the clause were fully settled.

Disposition: **AMEND**.

## 10. MODERATE-4 — same-coordinate closure needs an explicit advancement barrier

### Attack

The candidate discovers the complete immediately-due set but does not explicitly repeat the Step-2 rule that time/procedure advancement cannot move beyond the reached coordinate while mandatory same-coordinate consequences remain unresolved.

### Resolution

At a reached metric/procedure/semantic boundary:

```text
freeze advancement at reached coordinate
capture complete immediately-due set
resolve/serialize mandatory same-coordinate consequences to closure
only then expose/consume remaining requested advancement
```

If order-sensitive work suspends for choice/adjudication, the remainder stays unconsumed in continuation state.

Disposition: **AMEND**.

## 11. MODERATE-5 — one-guard IntentPlan surface is intentionally narrow but needs a revisit trigger

### Attack

One prior-clause guard may be insufficient for common natural-language conjunction/disjunction.

### Resolution

Keep the minimal one-guard surface for Step 3 to avoid a workflow DSL. Record a revisit trigger:

> If focused compound-intent tests show that ordinary player messages repeatedly require two or more prior-result conditions that cannot be split naturally without changing meaning, reopen only the bounded guard vocabulary.

No current blocker.

Disposition: **KEEP + DEFERRED REVISIT TRIGGER**.

## 12. MINOR-1 — ExecutionSegment class-admission challenge

### Attack

MechanicalEvents reference segment identity; retries inspect segment receipts. This could be read as an independent-addressing requirement forcing `runtime.execution_segment` under the class-admission rule.

### Resolution

Keep ExecutionSegment embedded.

All required addressing is resolvable through an already independent owner (`resolution_id` or direct `command_id`) plus segment sequence. Segment has no lifecycle, permissions, references, or state transition independent of that owner. Disposable indexes may accelerate lookup.

Introduce a runtime class only if future design requires segment lifecycle/reference independent of its owner.

Disposition: **KEEP**.

## 13. MINOR-2 — narrative/history layering must not imply current transcript durability

### Attack

The candidate's future layering can be misread as saying full transcript publication to Git already exists. Current campaign session schema explicitly says session metadata is not full chat history, and semantic events explicitly are not transcript/narration.

### Resolution

Keep Step-3 wording conditional (`when retained`) and assign full transcript retention/publication to Steps 4/5.

For future spectator use, recommend a visibility-safe public projection rather than direct exposure of a private campaign branch containing hidden facts.

Disposition: **KEEP / CARRY FORWARD**.

## 14. LLM authority attack

Attempted bypasses:

```text
LLM asserts target HP through invocation fact
LLM supplies remembered Activity ID absent from bounded candidate set
LLM says target_visible=false was omitted and runtime treats missing as false
LLM narration claims an Effect ended and later mechanics read the prose
```

Candidate protections survive:

- engine facts use accessors/state owners, not invocation fact channel;
- binder revalidates IDs under pinned catalog/state;
- true/false/missing remain distinct;
- narration/history is not mechanical input.

Disposition: **ASSURED**.

## 15. Procedure authority attack

Attempted duplicate-owner scenarios:

- reaction child copies Action/Reaction spent state;
- Continuation serializes procedure budget and restores it over child changes;
- world.encounter becomes a second budget store;
- checkpoint stores independently mutable procedure snapshot.

Candidate protections survive if MAJOR-1 closure amendments are applied:

- Procedure remains sole live owner;
- Resolution/Continuation reference it;
- checkpoint is immutable recovery representation;
- world Encounter is optional world-facing context only.

Disposition: **ASSURED**.

## 16. Persistence/recovery attack

The review tested:

- crash after segment commit before response delivery;
- crash while suspended;
- crash after Event commit but before child execution;
- retry after child already committed;
- trace compaction while live recency arbitration remains;
- incompatible catalog adoption during suspension.

With MAJOR-1/2/4 and MODERATE-1 amendments, all cases have one recoverable authority path without full replay or SQLite snapshot semantics.

Disposition: **ASSURED AFTER AMENDMENTS**.

## 17. Narrative/spectator cross-stage finding

The user's spectator/history objective is architecturally compatible with the execution design and strengthens the value of keeping semantic history separate from transcript and authored chapters.

Recommended later stack:

```text
private execution/canon sources
    runtime.message when retained
    MechanicalEvents / world state / lore
        -> visibility-aware SemanticEvents
        -> visibility-aware authored Chapters
        -> optional public/spectator Git projection
```

A second ChatGPT can reconstruct a high-quality narrative more reliably from:

```text
public SemanticEvents = factual spine
+ selected public transcript = dialogue/voice/scene texture
+ Chapters = existing authored continuity/style
```

than from transcript alone.

Directly publishing the private campaign branch is unsafe when hidden facts/secrets are stored there. Exact retention, filtering, projection branch/repository structure and guest authorization remain Steps 4/5.

Disposition: **CARRY FORWARD — NOT STEP-3 BLOCKER**.

## 18. Resolution gate recommendation

Apply these candidate amendments before canonicalization:

1. RuntimeCommand/root command owns mandatory execution-chain closure; no ResolutionChain class.
2. Mandatory post-commit firing identity/pending child descriptor is atomically materialized with triggering Event segment.
3. Chain-limit blocked work is owned by root command/Resolution pending-child state.
4. Effect recency uses immutable target+family-local nonterminal episode ordinal rather than unspecified future global order.
5. Retry lookup checks stored command/continuation context before ambient rebind.
6. Solicited choice/reaction responses bind to pending continuation/offer first.
7. Final clause narration distinguishes settled versus suspended/follow-up-required closure.
8. Same-coordinate advancement is blocked until mandatory due closure or durable suspension.
9. Keep narrow IntentPlan guard with explicit empirical revisit trigger.
10. Keep ExecutionSegment embedded.
11. Keep transcript/spectator publication deferred to Steps 4/5 with visibility-safe projection requirement.

Human decision required: **NO**.

No amendment changes the owner-approved Alternative C boundary or introduces a competing architecture.
