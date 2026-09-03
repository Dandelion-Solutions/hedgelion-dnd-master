# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-3 Decision Brief

Status: **STEP 3 DECISION BRIEF — DECISION MECHANICALLY DERIVED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-03

Evidence basis:

- repaired WP-17 Step-1 package + `SR17-01`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-2-source-manifest-expansion.md`.

---

## 1. Decision question

What implementation-facing WP-17 architecture realizes R2.5 asynchronous collaboration while preserving native execution/chronology/access/information/persistence owners and avoiding a generic queue, global collaboration frontier or a second human-input identity system?

---

## 2. Established facts

1. R2.5 requires three coordination families and admits a durable collaboration obligation only for unresolved collective human input that must survive participant/chat gaps and is not already owned by a native ordered owner.
2. Catalog Contracts already admits `runtime.collaboration_obligation` as an independently addressable runtime family, while WP-11 gives it a campaign native route and no baseline discovery index.
3. Step 3 already owns accepted external input identity as `runtime.interaction -> runtime.intent_plan -> IntentClause`; command/procedure/continuation ownership begins only when the clause crosses the applicable execution boundary.
4. One Interaction may contain several material interpreted clauses, so `runtime.message` or `interaction_id` alone is too coarse for one collaboration semantic input.
5. Step 5.11 requires semantic consumers to remain content-sufficient before raw message payload compaction.
6. Current `IntentClause` machine shape provides stable `clause_id` but lacks a closed collaboration semantic class/content representation. This is realization debt, not a missing semantic identity owner.
7. `value.contribution` already belongs to Rule Element deterministic calculation mechanics and cannot be repurposed.
8. WP-16 requires current trusted principal -> PLAYER -> control -> purpose-specific authorization for agency-bearing input and separates campaign/LIVE/HOT currentness.
9. WP-15 forbids technical/message/ref/CAS order from becoming fictional chronology.
10. R2.3/Step 4/Step 5.11/5.12 already own bounded context, truth, knowledge, message evidence and human disclosure needed by catch-up.
11. WP-13/WP-14 already provide native-domain durability/current-authority-first recovery without distributed transactions or a generic job registry.
12. Current shipped CORE/session/schema/test material is consumer evidence and contains no contrary product owner requiring a different collaboration architecture.

---

## 3. Alternatives

### Alternative A — use only native Procedure/Continuation/Choice/Reaction

No separate collaboration record. Every delayed participant dependency must be represented as a native ordered execution owner.

**Benefit:** fewest runtime families.

**Reject because:** R2.5 explicitly distinguishes collective asynchronous collection from native ordered responder semantics. Forcing cross-chat joint agency into Procedure/Continuation duplicates/warps execution ownership and cannot represent independent durable collection without making Step-3 owners generic collaboration queues.

### Alternative B — generic collaboration queue/registry with messages as entries

Create one campaign-wide pending-contribution registry, use `runtime.message`/arrival order, timeouts/presence and per-participant queue positions.

**Benefit:** straightforward centralized operational model.

**Reject because:** violates R2.5 no-global-active-player/native-owner/maximal-safe-frontier laws, turns message/transport order into authority pressure, invites timeout correctness, duplicates current owners, increases global contention and creates a scheduler/registry explicitly unsupported by evidence.

### Alternative C — scoped campaign-owned obligation + existing accepted input semantic unit

Use `runtime.collaboration_obligation` only for durable `AGENCY_DEPENDENT_COLLECTIVE`. Keep the accepted human input owner in the existing `Interaction/IntentPlan/IntentClause` chain. Identify one semantic unit by `(interaction_id, clause_id)`, require bounded normalized R2.5-class semantics in that clause, use `runtime.message` only for communication/exact-text evidence, and store only references in the collaboration obligation.

**Benefits:** realizes R2.5 exactly; no duplicate input identity; no `value.contribution` collision; content survives lawful message compaction; native ordered owners still win; campaign routing/recovery already exists; bounded currentness and catch-up compose with accepted owners.

**Cost:** later machine realization must add explicit collaboration semantic fields to IntentClause and materialize the collaboration-obligation schema/tests.

**Recommendation:** SELECT.

### Alternative D — new `value.collaboration_input` / independent `runtime.collaboration_input`

Create a new protocol kind or durable record specifically for human async input.

**Reject because:** current Interaction/IntentPlan already owns accepted semantic input identity. A new value/record would duplicate identity/provenance/retry rules and fail the minimum-sufficient-owner test. The real gap is content-sufficient typed semantics in the existing clause owner.

---

## 4. Selected direction

> **SCOPED CAMPAIGN-OWNED COLLABORATION OBLIGATION / INTERACTION-CLAUSE HUMAN INPUT IDENTITY / CONTENT-SUFFICIENT SEMANTIC REFERENCES / NATIVE-OWNER-FIRST PROGRESSION**

Conceptually:

```text
accepted external message
    -> runtime.interaction
    -> runtime.intent_plan
    -> IntentClause
         identity = (interaction_id, clause_id)
         R2.5 semantic class
         bounded normalized semantic content
         optional exact-text ref when exact wording is still required

coordination-family classifier
    -> INDEPENDENT_IMMEDIATE
         native progression, no obligation
    -> RULE_OWNED_ORDERED
         Procedure/Continuation/Choice/Reaction, no obligation
    -> AGENCY_DEPENDENT_COLLECTIVE
         if collection must survive gap:
             runtime.collaboration_obligation
                 accepted_input_refs -> existing IntentClause identities
```

Hard namespace law:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != runtime.collaboration_obligation lifecycle
```

---

## 5. Required architecture consequences

### 5.1 Obligation owner

`runtime.collaboration_obligation` is campaign-owned and independently durable only when its admission premise is satisfied. It is not LIVE-owned merely because its dependent decision concerns a LIVE source.

### 5.2 Generation identity

```text
(obligation_id, generation)
```

is the semantic collaboration generation identity. Purpose/scope/dependency/required agency basis are generation-defining. Campaign commit/ref is publication fencing, not generation or fictional chronology.

### 5.3 Accepted human input

One accepted collaboration semantic unit is identified by:

```text
(interaction_id, clause_id)
```

and carries exactly one admitted R2.5 semantic class for that association. The existing IntentClause/input owner must retain normalized semantic content sufficient for the collaboration consumer. Exact wording is separately protected through Step-5.11 message evidence only when materially required.

### 5.4 No copied transcript

The obligation stores accepted input refs, not transcript prose or a second semantic input body.

### 5.5 Native owner wins

`RULE_OWNED_ORDERED` never creates a mirrored obligation. If a current Procedure/Continuation/Choice/Reaction takes ownership of responder/order/resume semantics, collaboration does not compete with it.

### 5.6 Monotonic lifecycle

Baseline generation lifecycle is equivalent to:

```text
OPEN -> CLOSED -> RESOLVED
OPEN -> OBSOLETE
CLOSED -> OBSOLETE
```

No reopening of a terminal/closed generation. New material need creates a successor generation.

### 5.7 Required/optional contributor semantics

Only positive bounded material dependencies create required entries. Optional contributors never block. Agency-bearing requirements bind current PLAYER/PC authority and must be superseded if controller/membership changes make the generation's admission basis invalid.

### 5.8 Input acceptance/currentness

Before an agency-bearing input is associated:

```text
current principal
-> current PLAYER
-> current controlled PC
-> purpose-specific authorization
-> current obligation generation
-> current underlying campaign/LIVE/native opportunity
-> accepted Interaction/IntentClause
-> allowed semantic class
```

A stale session/message/old obligation ref grants no authority.

### 5.9 Duplicate/stale/late behavior

- same `(interaction_id, clause_id)` against same generation is idempotent;
- same prose in a new Interaction is new input;
- old-generation input never mutates successor automatically;
- explicit current reinterpretation/reconfirmation is required for any compatible reuse;
- accepted command/segment/RNG/Continuation is never replayed/rerolled because a reply was late.

### 5.10 Maximal safe frontier

Progress every consequence independent of the missing human input, establish and expose only that safe prefix, then wait at the first dependency. The safe-frontier association uses native owner/chronology evidence, not a new global scalar.

### 5.11 Absence

Absence/silence/offline/disconnect is not consent, pass, PC speech/action/belief or control transfer. It is also not immunity from automatic owner-required consequences after no applicable voluntary opportunity remains. No timeout/presence/heartbeat/message-age correctness authority.

### 5.12 Chronology

Message/Interaction/ref/CAS/commit/array/wall-clock order never chooses fictional order. WP-15/native owners decide the minimum material ordering or leave it unresolved.

### 5.13 Catch-up

Join/rejoin uses current identity/control/routing first, then R2.3 bounded recipient-eligible context + current truth/knowledge/message/disclosure owners + own unresolved obligation requirements. No transcript/context/planning dump and no cursor-as-read-proof.

### 5.14 Durability/recovery

Obligation publication uses normal WP-11/WP-13 campaign native semantics. LIVE/native dependencies are revalidated, not transactionally coupled. WP-14 recovery loads current obligation and its referenced accepted input dependencies as a typed bounded root when lifecycle/routing says it is current.

### 5.15 Performance

No global obligation scan/index is required for ordinary play. Known ID routes directly; participant/native routing may nominate relevant current obligations. Derived helpers remain optional/non-authoritative and require measured need before introduction.

---

## 6. Machine-realization obligations downstream

Later authorized realization must:

1. add closed collaboration-relevant semantic class + normalized semantic content to the existing IntentClause/input contract;
2. preserve `(interaction_id, clause_id)` identity and existing Step-3 retry/idempotency ownership;
3. materialize the final `runtime.collaboration_obligation` schema/lifecycle/reference contract;
4. keep `value.contribution` untouched as mechanical Rule Element vocabulary;
5. add bounded current-obligation discovery/routing without a global authority index;
6. add tests for all three coordination families, generation supersession, control changes, duplicates/late replies, safe frontier, catch-up secrecy, recovery and no technical-order chronology;
7. reconcile shipped CORE/session prose against the final canonical owner model;
8. keep WP-18 planning separate.

No implementation work is authorized by this Decision Brief.

---

## 7. Decision status

```text
SELECTED: ALTERNATIVE C
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
CONFIDENCE: HIGH
STEP_4_READY: YES
```

The recommendation follows mechanically from accepted R2.5/Step-3/Step-4/Step-5/WP-11..WP-16 owners and current machine evidence. No product-semantic/material trade-off remains for human judgment at Step 3.
