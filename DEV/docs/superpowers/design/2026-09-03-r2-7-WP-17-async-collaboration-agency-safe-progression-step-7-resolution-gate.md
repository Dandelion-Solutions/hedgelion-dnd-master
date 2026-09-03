# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-7 Resolution Gate

Status: **STEP 7 COMPLETE — ALL STEP-6 BLOCKING/SIGNIFICANT FINDINGS RESOLVED / CANONICALIZATION READY**

Date: 2026-09-03

Step-6 findings:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-step-6-whole-project-adversarial-review.md`.

Step-6 counts:

```text
BLOCKING:     2
SIGNIFICANT:  4
MINOR:        0
```

The selected Step-3 Alternative C remains valid. Step 7 repairs its incomplete routing/handoff/privacy/identity laws without changing the product model, starting WP-18, or reopening an upstream owner.

---

# 1. F17-01 resolution — bounded current-obligation routing

## Finding

No exact bounded route existed from a recovered/rejoining current PLAYER to relevant nonterminal collaboration obligations without scan/index/session memory.

## Resolution

Introduce a **completeness-protected derived PLAYER routing companion** for nonterminal obligations materially tied to that PLAYER.

Conceptual route reference:

```text
RequiredCollaborationRouteRef {
    obligation_id
    generation
}
```

Conceptual PLAYER-side companion:

```text
collaboration_route_refs[]
```

Exact field spelling is downstream machine realization.

### 1.1 Route-holder set

For one nonterminal generation, route holders are the bounded current PLAYER identities whose recovery/participation must be able to rediscover the barrier, including at minimum:

1. every required contributor PLAYER;
2. every PLAYER owning a collaboration-held accepted input whose dependent semantic unit remains behind this obligation;
3. any additional PLAYER explicitly required by the generation's owner-defined bounded recovery/recipient scope.

Optional merely-eligible contributors are not route holders solely because they could have contributed.

The route-holder set is derived from the obligation's accepted semantic ownership/recovery relationships. It is routing metadata, not a second required-contributor owner.

### 1.2 Completeness publication law

Because obligation and PLAYER records are campaign-owned, any mutation that changes the nonterminal routing set publishes in one campaign native-domain closure:

```text
obligation create/successor/terminal change
+
all affected PLAYER collaboration_route_refs changes
```

No cross-domain transaction is introduced.

For an `OPEN` or `CLOSED` generation, every route holder must carry exactly the current `(obligation_id,generation)` route ref. On `RESOLVED`/`OBSOLETE`, the ref is removed in the same campaign-domain closure.

A generation change removes the old route ref and adds the successor route refs coherently.

### 1.3 Nonauthority law

The PLAYER companion:

- nominates an exact obligation ID/generation only;
- does not prove that the obligation is semantically current merely by containing the ref;
- cannot satisfy/close/obsolete an obligation;
- cannot authorize contribution;
- cannot transfer PC agency;
- cannot replace dereferencing the obligation and revalidating underlying currentness/PLAYER control;
- does not turn `PLAYER_INDEX.yaml` into a collaboration index.

An exact current PLAYER record whose routing companion passed its publication/completeness invariant may terminate ordinary routing when no matching route ref exists. This is a **complete protection/routing contract**, not semantic ownership of collaboration state. Any detected mismatch is `INTEGRITY_CONFLICT` / bounded repair territory, never permission for a broad ordinary scan.

### 1.4 Recovery/rejoin path

```text
trusted current principal
-> current PLAYER record by stable binding
-> exact current PLAYER collaboration route refs
-> direct WP-11 obligation route by ID
-> validate generation/state/required-or-held relation
-> validate underlying campaign/LIVE/native opportunity
-> build recipient-safe catch-up / accept current input
```

No generic collaboration index, queue, scheduler, background scan or PLAYER-index authority is introduced.

**F17-01:** `CLOSED`.

---

# 2. F17-02 resolution — collaboration-held actionable intent and native release

## Finding

The candidate did not make the pre-command boundary mandatory and did not close how several accepted Interactions return to Step-3 execution without a synthetic combined command.

## Resolution

### 2.1 Mandatory held-clause state

A dependent collaboration-held `ACTIONABLE_INTENT` remains its original accepted IntentClause:

```text
execution_state = intent.pending
command_id = absent
```

for the blocked dependent semantic unit while the collaboration generation owns waiting.

A RuntimeCommand MUST NOT be allocated/accepted for that dependent unit before collaboration handoff.

Any independent executable prefix must have been split into a distinct IntentClause before command acceptance. Already accepted independent commands/results remain real and are never moved back behind collaboration.

### 2.2 No synthetic collaboration command

Collaboration never creates:

- a `runtime.command` of its own;
- a synthetic system Interaction;
- a multi-Interaction command identity;
- an anchor chosen from message/Git/CAS/arrival order.

### 2.3 Deterministic handoff plan

When collection is CLOSED, a deterministic ephemeral handoff maps each frozen accepted semantic unit to exactly one legal next responsibility:

```text
RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
    original ACTIONABLE_INTENT clause becomes ready for ordinary Step-3 mapping

CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT
    OOC / communication / control / other owner-defined noncommand use

HAND_TO_EXISTING_NATIVE_OWNER
    an already-admitted Procedure/Continuation/Choice/Reaction/equivalent consumes the input without collaboration mirroring it

CLARIFICATION_OR_UNSUPPORTED
    no executable command is fabricated
```

If a single native command depends on several collaboration inputs, one semantically authorized **execution anchor IntentClause** must already be explicit in the generation/dependency contract. That clause owns the command through normal Step 3; the other closed input refs are fixed dependencies included in its accepted interpretation/input fingerprint. The anchor is never selected by transport order.

If no admitted command anchor/native mapping exists, collection cannot synthesize one. The engine requires an explicit current input/clarification or remains blocked under the owning contract.

### 2.4 Handoff precedes command acceptance

Only after the collaboration handoff has transferred a held actionable clause back to the existing IntentPlan/Step-3 input owner may that clause enter `intent.ready` and receive a RuntimeCommand.

**F17-02:** `CLOSED`.

---

# 3. F17-03 resolution — immutable, unitary accepted collaboration input semantics

## Finding

The candidate did not explicitly freeze accepted collaboration-relevant clause semantics or require one semantic unit/class per referenced clause.

## Resolution

For a collaboration-relevant accepted IntentClause, the following accepted interpretation payload is immutable while referenced:

```text
interaction_id
clause_id
collaboration_semantic_class
normalized_semantics
material exact_text_ref(s), if any
```

One collaboration-relevant IntentClause represents exactly **one** material R2.5 human semantic unit/class for collaboration association:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

If one host message contains several material units/classes, Interpreter creates distinct IntentClauses under the same Interaction.

Correction/reinterpretation never rewrites the accepted meaning behind the same `(interaction_id,clause_id)`. It creates a new accepted input/current interpretation path and is re-admitted explicitly.

Message compaction may change retained representation only after the normalized semantic owner and any required exact-text evidence remain content-sufficient.

**F17-03:** `CLOSED`.

---

# 4. F17-04 resolution — stable obligation lineage vs new obligation

## Finding

The candidate did not define when successor generations remain one stable obligation lineage versus when a new obligation ID is required.

## Resolution

One `obligation_id` owns one stable **bounded collaboration dependency lineage**.

Its lineage identity is anchored to the same admitted dependency/purpose family and original blocked decision lineage. Within that lineage, material current evolution uses successor generations, including:

- required authority/control set changes;
- current opportunity basis movement that preserves the same dependency lineage;
- current reinterpretation/reconfirmation where the same collaboration question continues;
- another generation-defining field change that does not create a semantically new decision opportunity.

A semantically unrelated/new decision opportunity receives a **new obligation ID**, even if:

- participants are the same;
- prose is similar;
- it occurs in the same scene;
- it immediately follows a terminal prior obligation.

Terminal IDs/generations are never repurposed.

`generation` may advance monotonically for implementation convenience, but numeric order remains owner-local lineage metadata and never fictional chronology/global currentness.

**F17-04:** `CLOSED`.

---

# 5. F17-05 resolution — recipient-safe obligation catch-up projection

## Finding

An obligation references multiple participants' accepted inputs, so “show my current obligation” could leak another participant's private/OOC semantic input.

## Resolution

Catch-up uses an ephemeral **recipient-safe obligation projection**, not the raw obligation/input bodies.

For one recipient it may expose only material independently eligible content such as:

- obligation identity/generation where useful;
- recipient-eligible purpose/status summary;
- the recipient's own current required action/non-action opportunity;
- safe-frontier/current-situation evidence independently eligible through R2.3/Step 4;
- information about other contributions only to the extent an existing `runtime.message`, `world.knowledge`, `runtime.disclosure` or other current owner independently grants that recipient access.

The following is not an eligibility rule:

```text
input ref appears in same collaboration obligation
    -> therefore recipient may see its semantic content
```

That implication is forbidden.

Another participant's private/OOC input, private context, planning material or undisclosed intent remains hidden unless separately eligible. The engine may provide a neutral status such as “another required input is still pending/has been received” only where that metadata itself is eligible and does not reveal protected content.

**F17-05:** `CLOSED`.

---

# 6. F17-06 resolution — collection resolution is handoff, not gameplay completion

## Finding

Candidate `RESOLVED` wording risked keeping collaboration coupled to downstream gameplay completion and creating replay risk if native execution progressed while terminal collaboration state did not publish.

## Resolution

### 6.1 Correct lifecycle meaning

```text
OPEN
    collection accepts current compatible human input

CLOSED
    exact accepted input set is frozen; no new input enters this generation;
    deterministic handoff is pending

RESOLVED
    collaboration collection responsibility has been successfully handed off /
    consumed by the existing accepted input/native owner boundary;
    collaboration no longer owns waiting for this generation

OBSOLETE
    opportunity/lineage generation became invalid before handoff
```

`RESOLVED` does **not** mean every downstream gameplay command/procedure has completed.

### 6.2 Closed input-set identity

At close, derive an immutable order-independent fingerprint over the frozen semantic use associations:

```text
ClosedCollectionBasis :=
    (obligation_id, generation, closed_input_set_fingerprint)
```

Physical array order does not affect the fingerprint's semantic set identity.

### 6.3 Campaign-domain handoff

The baseline handoff is between campaign-owned runtime records:

- `runtime.collaboration_obligation`;
- referenced `runtime.intent_plan` / embedded IntentClauses.

For collaboration-held actionable clauses, handoff makes the released original clauses `intent.ready` (or another legal noncommand disposition selected by deterministic interpretation) while preserving their original identities.

Where the handoff mutates campaign-owned IntentPlan/obligation records, publish the complete handoff as one campaign native-domain closure when practical/required for correctness:

```text
closed collection basis
+ affected IntentPlan clause readiness/disposition updates
+ obligation RESOLVED
+ routing companion removals
```

This is one campaign transaction, not a distributed transaction.

If the complete handoff cannot be established, the obligation remains `CLOSED`; no dependent command is accepted.

### 6.4 Native execution after handoff

After `RESOLVED`, Step 3 owns released actionable clauses normally. RuntimeCommand input/dependency fingerprinting must preserve the collaboration source basis where material:

```text
obligation_id
generation
closed_input_set_fingerprint
accepted dependent input refs
```

This is causal/idempotency evidence, not a second execution owner.

Choice/Reaction/Continuation/procedure suspension after handoff is purely native; collaboration never reopens to mirror it.

### 6.5 Failure/recovery law

If a handoff campaign transaction failed, no `RESOLVED` handoff was established and no dependent RuntimeCommand may have been accepted under the baseline rule.

If later native execution exists, its accepted source basis proves it came from a completed handoff; recovery never re-releases/rerolls/replays that accepted execution. Any metadata inconsistency is repaired forward from accepted evidence.

`CLOSED -> OBSOLETE` is permitted only before successful handoff. Once handoff establishes `RESOLVED`, later gameplay invalidation belongs to the native owner and does not resurrect collaboration.

**F17-06:** `CLOSED`.

---

# 7. Consolidated repaired architecture delta

The selected direction is now:

> **SCOPED CAMPAIGN-OWNED COLLABORATION OBLIGATION / IMMUTABLE INTERACTION-CLAUSE HUMAN INPUT / COMPLETENESS-PROTECTED PLAYER ROUTING / EXPLICIT COLLECTION-TO-STEP-3 HANDOFF / NATIVE-OWNER-FIRST PROGRESSION**

Key repaired chain:

```text
current accepted human input
-> immutable collaboration-relevant IntentClause identity/semantics
-> coordination-family admission
-> if durable AGENCY_DEPENDENT_COLLECTIVE:
     campaign-owned obligation OPEN
     + completeness-protected PLAYER route refs
-> maximal safe prefix under native owners
-> required current inputs associated idempotently
-> explicit CLOSED frozen set
-> deterministic campaign-domain handoff
     held actionable clauses: pending -> ready on original Step-3 path
     noncommand/native-owner inputs: consumed by their existing owner
     no synthetic command
-> obligation RESOLVED + route refs removed
-> Step-3/native execution proceeds independently
```

---

# 8. Item-level propagation matrix

| Finding | Step-3 Decision | Step-4 Review | Step-5 Candidate | Step-8/final canonical | Downstream routing |
|---|---|---|---|---|---|
| F17-01 | Alternative C retained; adds exact PLAYER routing companion | supersedes issue 12's deferred-helper wording | WP17-54..56 incomplete; superseded | MUST include routing completeness/nonauthority/rejoin law | PLAYER schema + collaboration schema + recovery tests |
| F17-02 | existing input owner retained; adds mandatory pre-command/handoff boundary | strengthens issues 5/6 | WP17-15 wording superseded | MUST include held clause/no synthetic command/release law | IntentPlan/Command schemas/tests |
| F17-03 | input identity retained; content contract hardened | strengthens issues 2/3 | WP17-11..14 extended | MUST include immutable one-unit-per-clause law | IntentClause schema/interpreter tests |
| F17-04 | generation model retained; lineage boundary added | no product-direction change | WP17-7..9 extended | MUST include new-ID vs successor law | obligation identity/schema tests |
| F17-05 | catch-up direction retained; projection eligibility narrowed | strengthens issue 10 | WP17-42..47 extended | MUST include recipient-safe obligation projection | Context/catch-up disclosure tests |
| F17-06 | collection-only owner retained; RESOLVED meaning corrected | supersedes issue 6/8 completion wording | WP17-17..20/48..54 superseded where different | MUST include CLOSED handoff + RESOLVED collection discharge | IntentPlan/obligation publication/recovery tests |

Earlier artifacts remain design provenance. Where they differ from this Step-7 resolution or the final Step-8 canonical spec, the later resolution/final spec governs.

---

# 9. Resolution gate

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
STEP_6_MINOR:             0
RESOLVED_BLOCKING:        2
RESOLVED_SIGNIFICANT:     4
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
SELECTED_ALTERNATIVE:     C / RETAINED WITH REPAIRS
STEP_8_READY:             YES
WP18_STARTED:             NO
IMPLEMENTATION_PLANNING:  NO
```
