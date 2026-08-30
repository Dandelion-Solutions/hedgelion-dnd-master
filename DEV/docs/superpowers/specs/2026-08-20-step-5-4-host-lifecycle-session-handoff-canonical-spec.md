# Step 5.4 — Host Lifecycle & Session Handoff — Canonical Specification

Status: **CANONICAL ARCHITECTURE — STEP 5.4 CLOSED**

Date: 2026-08-20

Owner-approved architecture:

> **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF**

Owner-approved scope refinement:

> Host conversation/message/context capacity exhaustion is explicitly in Step-5.4 scope, but no trustworthy remaining-capacity signal is assumed. Future estimation is advisory only unless a host supplies a stronger explicit contract.

Derivation chain:

- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-analytical-challenge.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-decision-brief.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-candidate-spec.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-adversarial-review.md`
- `../design/2026-08-20-step-5-4-host-lifecycle-session-handoff-resolution-gate.md`

Prerequisites:

- Step-3 canonical deterministic execution ownership;
- Step-5.1 B-NARROW domain typing / no implicit cross-domain order;
- Step-5.2 canonical Resumable Runtime Closure v2;
- Step-5.3 canonical A-NARROW temporal/pending continuity.

This specification defines logical host lifecycle, controlled handoff and unexpected-loss semantics. It does not implement GAME/runtime changes, define the final SOFT/HARD/SAVE classifier, choose a Git publication algorithm, select checkpoint wire format, define live-epoch ownership transfer, choose transcript retention, or define host-delivery acknowledgement.

Where current runtime prose conflicts with this architecture, the runtime prose is pre-realization debt and must be aligned during the later integrated implementation program.

---

# 1. Canonical definition

**BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** means:

> Host/chat/process lifecycle is not gameplay authority. When a recovery-safe controlled handoff is intended and the current host has an actionable handoff reason, HDM establishes a scoped mutation-quiescence barrier, ensures every promised gameplay-significant semantic dependency is represented by its proper native owner, and acknowledges recovery-safe handoff only after the applicable Step-5.2/5.3 Resumable Runtime Closure is actually durable and compatible. A fresh host resumes by bounded hydration of native durable sources, not from a handoff snapshot or remembered model/process state.

If the host disappears before that success condition is reached:

> recovery uses the newest compatible **actually durable** native source set that can be selected and validated; destroyed unpublished HOT/SOFT state is not invented or reconstructed.

Step 5.4 introduces no mandatory durable handoff owner.

---

# 2. Authority geometry

Host lifecycle concepts are control-flow/recovery conditions only.

They do not own:

- current world truth;
- Procedure state;
- RuntimeCommand/Resolution/Continuation state;
- pending temporal obligations;
- current live scene truth;
- fictional chronology;
- player/NPC knowledge;
- human disclosure;
- write authorization;
- recovery frontier semantics.

Current native owners from Steps 3, 5.2 and 5.3 remain authoritative.

A handoff barrier composes/guards those owners; it does not replace them.

---

# 3. Logical host conditions

These conditions describe runtime behavior. They are not a required persistent state machine or new record class.

```text
ATTACHED
    host/context is usable and may operate under ordinary authority

HANDOFF_PENDING
    controlled handoff barrier is active for an affected scope

RELINQUISHED
    this host completed handoff for the scope and must not continue from
    its pre-handoff hot assumptions

LOST
    host/context disappeared without successful local handoff completion

HYDRATING
    fresh/restarted host is reconstructing current state from durable evidence
```

Campaign lifecycle, session metadata status, Procedure lifecycle and live-epoch lifecycle remain separate.

Host/context destruction by itself does not:

- pause/end/complete a campaign;
- end a fictional scene;
- advance fictional time;
- terminate a Procedure;
- cancel accepted execution;
- resolve a player declaration;
- create NPC/world action;
- consume gameplay resources.

---

# 4. Canonical laws

## LAW 5.4-1 — HOST LIFECYCLE IS NOT GAMEPLAY AUTHORITY

Host/chat/process/model-context state SHALL NOT become an alternate owner of gameplay truth, execution, temporal work, chronology, knowledge, disclosure or live ownership.

## LAW 5.4-2 — CONTROLLED HANDOFF AND UNEXPECTED LOSS HAVE DIFFERENT GUARANTEES

A controlled recovery-safe handoff SHALL NOT be acknowledged until its required durability/compatibility conditions hold.

Unexpected loss has no retroactive finalization step and recovers only actual durable native state.

## LAW 5.4-3 — EXISTING NATIVE OWNERS CARRY RESUME SEMANTICS

Handoff SHALL preserve unresolved gameplay state through the narrowest existing native semantic/execution owner wherever such an owner exists.

No generic `resume_point`, handoff snapshot or transfer payload SHALL duplicate native authority.

## LAW 5.4-4 — SCOPED MUTATION QUIESCENCE

Once a handoff closure is frozen for scope `S`, the handing-off host SHALL NOT acknowledge a new gameplay mutation or accept a new dependent gameplay-semantic Interaction into `S` until either:

1. handoff succeeds and `S` is relinquished; or
2. handoff fails/is abandoned while the host survives and `S` is restored to valid ATTACHED operation.

Already accepted semantic state from before freeze that belongs to the handoff promise SHALL join the required closure.

OOC/control-flow communication or independent scopes that cannot affect `S` need not be globally blocked.

## LAW 5.4-5 — LOCAL FREEZE DOES NOT CREATE A GLOBAL LOCK

The barrier freezes closure drift by the handing-off host. It does not require all other valid hosts/scopes to stop.

If an external participating native source moves in a way that can invalidate the selected handoff closure, the relevant source selection/publication attempt SHALL be invalidated, revalidated, reselected or failed under its native/later protocol.

Handoff success requires a compatible durable source set at the success boundary.

No distributed campaign-global lock, global host generation or universal revision is introduced.

## LAW 5.4-6 — ACTUAL DURABILITY, NOT INTENT

Attempted, prepared, intended, locally cached or ambiguously acknowledged publication is not sufficient proof of recovery-safe handoff.

Actual authoritative durability is the correctness fact.

Steps 5.6/5.7 own physical proof/recovery after ambiguous transport outcomes.

## LAW 5.4-7 — NO HEARTBEAT HANDOFF WRITE

If all promised resume state and required recovery derivatives are already durably recoverable and compatible, handoff correctness SHALL NOT require a commit, checkpoint, transfer ticket, timestamp mutation or no-op write solely to record that handoff happened.

## LAW 5.4-8 — NO INVENTED LOST VOLATILE STATE

After unexpected loss, incomplete handoff or unwarned host hard stop, destroyed unpublished state SHALL NOT be reconstructed from:

- plausibility;
- stale/current-chat prose alone;
- remembered model context;
- intended writes;
- approximate message/token progress;
- guessed player choices;
- replay performed solely to synthesize the lost newer state.

## LAW 5.4-9 — RELINQUISHMENT IS HOST-LOCAL, NOT A CAMPAIGN-GLOBAL LEASE

A host that successfully handed off a scope SHALL locally discard/reject use of its pre-handoff hot/transaction assumptions for further gameplay mutation.

If that host/chat later becomes usable, it must re-enter through current-source/authority/revision validation appropriate to the scope.

No campaign-global “newest host wins” lease is introduced.

## LAW 5.4-10 — DURABLE HYDRATION DOES NOT PROVE ABSENCE OF VOLATILE STATE ELSEWHERE

A host that successfully hydrates a durable native source set proves only consistency with that source set.

It SHALL NOT infer that no other host contains newer unpublished volatile state.

Unknown volatile state in another unreachable host is outside the durable recovery guarantee and SHALL NOT be guessed or silently merged.

Controlled handoff avoids this ambiguity for the source host by making its promised state durable before relinquishment.

## LAW 5.4-11 — SESSION METADATA IS NON-AUTHORITATIVE

Persistent `session` records MAY provide coordination, navigation, audit, observability and known-frontier hints.

They SHALL NOT by themselves:

- grant gameplay write authority;
- own current world/execution/temporal state;
- define current live ownership;
- define the definitive recovery frontier;
- prove that a host is alive/dead;
- prove recovery-safe handoff success;
- fence stale gameplay writes by status alone.

## LAW 5.4-12 — DESTRUCTIVE MAINTENANCE USES THE SAME HANDOFF GUARANTEE

Maintenance that keeps the host/context usable may use ephemeral orientation/continuation hints.

Maintenance known to destroy/invalidate the current host/context SHALL satisfy the same recovery-safe handoff contract for every gameplay-semantic point promised after the transition.

## LAW 5.4-13 — ACCEPTED SEMANTICS, NOT PARTIAL MODEL REASONING

Partial hidden model reasoning, chain-of-thought, unaccepted candidate interpretation, full prompt/context state and opaque process memory SHALL NOT become resume authority.

Handoff continuity begins at established accepted semantic/execution boundaries.

If an Interaction has been accepted but complete material meaning is not yet represented in typed state, the specific message/provenance evidence required to continue interpretation honestly is irreducible until either:

1. sufficient typed semantic state is durably materialized; or
2. the specific evidence itself becomes recoverable under an owning retention contract.

A dangling message identifier whose content cannot be resolved after host destruction is not sufficient recovery evidence.

## LAW 5.4-14 — INTERPRETABILITY CLOSURE SURVIVES HANDOFF

Open accepted execution is recovery-safe only when its compatible accepted runtime/catalog/rules interpretation context is recoverable as required by Step 5.2.

A destructive maintenance/runtime switch SHALL NOT silently reinterpret open execution under arbitrary newer ambient mechanics.

## LAW 5.4-15 — HOST CAPACITY TELEMETRY IS OPTIONAL CAPABILITY

HDM correctness SHALL remain valid when the host exposes no reliable remaining-message, remaining-token, remaining-context-capacity, remaining-time or imminent-hard-stop metric.

Missing capacity telemetry/warning is a supported normal case, not an integrity defect.

## LAW 5.4-16 — RELIABLE WARNING DOES NOT GUARANTEE HANDOFF EXECUTION BUDGET

Reliability that destruction is imminent is distinct from having enough remaining host/tool/model execution opportunity to complete handoff.

A reliable destructive signal may trigger/require an attempt, but handoff success exists only if the durable closure actually completes.

If the host becomes unusable before completion, recovery follows incomplete/unexpected-loss semantics.

No minimum remaining token/message/time budget is assumed.

## LAW 5.4-17 — CAPACITY HEURISTICS ARE ADVISORY ONLY

Message count, approximate token count, chat age, remembered product limits, inferred context usage or any future locally derived predictor SHALL NOT be authoritative remaining-capacity evidence unless a later explicit host contract promotes a specific signal class.

An advisory heuristic MAY produce a warning or transfer recommendation.

It SHALL NOT:

- redefine durability;
- prove imminent destruction;
- prove enough time remains to flush;
- become recovery authority;
- weaken crash fallback;
- be required for correctness.

False positive => at most unnecessary early warning/proactive handoff.

False negative => unexpected-loss recovery.

## LAW 5.4-18 — RELIABLE HOST DESTRUCTION SIGNAL MAY TRIGGER CONTROLLED HANDOFF

A host adapter may map documented actionable imminent-destruction evidence to the controlled handoff path when recovery-safe continuity is intended and execution opportunity remains.

Step 5.4 defines no universal numerical trigger threshold.

## LAW 5.4-19 — ADVISORY CAPACITY SIGNAL IS OOC ASSISTANCE

When a host exposes only an advisory near-capacity condition, HDM SHOULD, when a useful player-facing interaction opportunity exists, warn that the current host/chat may be approaching a limit and recommend/offer proactive continuation in a fresh host/chat.

The warning is technical/OOC. It does not itself pause fiction, advance time, establish `HANDOFF_PENDING`, or prove remaining capacity.

If explicit transfer/handoff is then initiated, ordinary controlled handoff semantics apply.

Whether advisory risk also causes an opportunistic durability flush is a Step-5.5 policy question, not a Step-5.4 law.

## LAW 5.4-20 — HOST TIME DOES NOT ADVANCE FICTION

Context age, host TTL, inactivity, restart and handoff duration SHALL NOT themselves advance fictional chronology or make temporal obligations due. Step-5.3 owner/chronology rules remain authoritative.

---

# 5. Host lifecycle / capacity signal classes

The architecture recognizes three host-capability classes:

```text
RELIABLE_DESTRUCTIVE
    documented actionable evidence that current host/context will become unusable

ADVISORY_CAPACITY
    elevated-risk warning/estimate without guaranteed remaining capacity

NO_USABLE_SIGNAL
    no actionable warning, warning invisible to runtime, or cutoff arrives first
```

## 5.1 RELIABLE_DESTRUCTIVE

May initiate the controlled handoff path.

It does not guarantee enough execution opportunity remains to finish that path.

## 5.2 ADVISORY_CAPACITY

May produce an OOC warning/recommendation and may be carried forward as a later durability-risk input.

It does not establish a durability/recovery fact.

## 5.3 NO_USABLE_SIGNAL / HARD STOP

No pre-destruction action is guaranteed.

Recovery uses the unexpected-loss contract.

This explicitly covers a host/product conversation limit that physically prevents further messages or work in the current chat before HDM can perform a transfer.

---

# 6. Controlled handoff logical protocol

The protocol is semantic, not a wire/storage state machine:

```text
H0  ATTACHED

H1  establish controlled handoff reason
    - explicit user/runtime transfer intent
    - controlled destructive maintenance/restart
    - actionable reliable destructive-host signal

H2  determine affected native ownership/recovery dependency scope(s)

H3  freeze local semantic acceptance/mutation for those scopes

H4  include/materialize all pre-freeze accepted semantic dependencies promised
    across the handoff into their proper native owners/evidence

H5  establish complete applicable Step-5.2 Resumable Runtime Closure
    + Step-5.3 pending/temporal continuity
    + recovery routing/dependency/interpretation closure

H6  validate compatible participating native source revisions and determine
    that required durability actually succeeded

H7  acknowledge RECOVERY_SAFE_HANDOFF

H8  old host treats affected pre-handoff hot assumptions as RELINQUISHED
```

## 6.1 Scope selection

The handoff scope SHALL include every mutable/recovery dependency whose omission can change correct resume semantics for the promised point.

It is not limited to a remembered list of dirty world files.

It follows Step-5.2 transitive required-dependency closure and current owning-scope routing.

## 6.2 New input after H3

A newly arriving gameplay message affecting frozen scope SHALL NOT become a new accepted gameplay-semantic Interaction/IntentPlan for that scope until:

- H7/H8 complete and a fresh/resumed host accepts it against current state; or
- handoff is abandoned and ATTACHED operation resumes.

A host transport layer may buffer bytes, but a transport queue is not gameplay semantic acceptance.

## 6.3 Clean handoff

If H4–H6 determine that no new durable delta is required, H7 may succeed using the already valid durable closure.

No heartbeat write is required.

## 6.4 Confirmed failure while host survives

The host may:

- retry/repair the required durability operation; or
- abandon handoff and restore valid ATTACHED operation.

It SHALL NOT call the failed transition recovery-safe.

## 6.5 Destruction despite failed/incomplete barrier

External product/operator destruction cannot be prevented by architecture.

After destruction, recover actual durable state and report/represent the situation honestly; do not promote intended handoff to success.

---

# 7. Semantic resume owner matrix

| Resume situation | Native owner/evidence |
|---|---|
| current world/domain truth | native world owner or current live owner |
| accepted Interaction before complete typed interpretation | `runtime.interaction` plus resolvable required accepted message/provenance evidence |
| typed accepted player intent | `runtime.intent_plan` |
| accepted root execution | `runtime.command` |
| active/suspended Activity | `runtime.resolution` / `runtime.continuation` |
| Procedure between Commands | `runtime.procedure` |
| Choice/Reaction | same Continuation generation/offer/responder/options |
| mandatory child execution | Step-3 pending child/firing identity + root closure |
| armed independently-due temporal source | native temporal owner + Step-5.2 typed temporal routing |
| accepted temporal firing | Step-5.3 source occurrence/firing closure + Step-3 execution identity |
| fixed accepted RNG | owning Resolution/Continuation/execution evidence associated with stable experiment identity |
| runtime/catalog/rules interpretation | compatible accepted interpretation context required by Step 5.2 |
| exact wording only for narrative smoothness | not recovery-critical |
| exact wording is only evidence preserving accepted material meaning | narrow accepted message evidence until typed materialization |
| partial model reasoning | never a resume owner |

A prose recap/orientation frame may help presentation after hydration but cannot replace missing native or irreducible recovery state.

---

# 8. Unexpected-loss / hard-stop recovery contract

Unexpected loss includes:

- process crash;
- host/context eviction;
- product conversation hard stop;
- user closes/discards host without completed handoff;
- reliable warning arrives but execution opportunity disappears before closure;
- advisory heuristic fails to predict cutoff;
- destructive maintenance proceeds despite failed handoff.

Recovery conceptually performs:

```text
1. do not trust lost/unpublished hot assumptions
2. resolve selected campaign and exact compatible runtime identity
3. select/pin current compatible native durable source revisions
4. resolve current owning scope(s), including live ownership where applicable
5. boundedly enumerate required operational/temporal roots
6. validate owner, routing, dependency and interpretation closure
7. hydrate native state
8. rebuild derived state
9. classify recovery outcome
10. only then accept new dependent gameplay mutation
```

The final selection/checkpoint protocol and outcome names belong to Step 5.7.

## 8.1 Recovery objective / RPO statement

After unexpected host/context loss, HDM guarantees recovery to:

> the newest compatible **actually durable Resumable Runtime Closure** whose domain-native source set can be selected and validated.

This is a semantic/domain-typed guarantee and may compose multiple native durable sources. It is not necessarily one scalar campaign commit/event ID.

State newer than that closure may be lost if it existed only in destroyed volatile context.

---

# 9. Stale/reopened host semantics

A host is stale whenever its cached state/authority assumptions are insufficient for the mutation it is about to perform.

Before dependent mutation/write, it must satisfy current applicable:

- campaign/live ownership routing;
- player/campaign authorization;
- branch/live revision validation;
- pinned-source compatibility;
- execution idempotency/resume identity;
- accepted runtime/catalog/rules compatibility.

A host that locally completed handoff MUST NOT resume from its old hot transaction state.

If later reused, it begins through current validation/hydration.

### Explicit epistemic limit

Even after successful hydration:

```text
selected durable source set is current/valid
```

does **not** imply:

```text
no other live host currently has unpublished SOFT state
```

HDM does not infer or merge such invisible state.

A future requirement for strict exclusive singleplayer-host fencing even when durable state is unchanged would be a new product/architecture decision and may justify a scoped coordination token. Step 5.4 does not introduce one preemptively.

---

# 10. Session metadata disposition

Persistent session records remain allowed as non-authoritative coordination/recovery projections.

Potential uses:

- session start/end/audit information;
- player/PC/scene association hints;
- support/observability metadata;
- known/base branch frontier hints;
- bounded navigation aid.

They do not own handoff correctness.

Stale `session.status=active` does not prove a dead host still owns gameplay. `session.status=ended` does not terminate still-active native execution/Procedure state.

Machine realization may later simplify/reshape session fields after Steps 5.7/5.8, but shall preserve these authority limits.

---

# 11. Maintenance semantics

## 11.1 Non-destructive maintenance

If the same usable host/context survives:

- ephemeral maintenance continuation/orientation context is allowed;
- maintenance alone need not force publication;
- native owners remain gameplay truth;
- no fictional time/action occurs merely due to maintenance.

## 11.2 Destructive maintenance

If maintenance will destroy/invalidate the current host/context and current semantic point is promised after the operation:

- use the controlled handoff barrier;
- persist required native semantic dependencies first;
- do not rely solely on a RAM/current-chat continuation frame;
- preserve compatible interpretation context for open execution;
- acknowledge safe destructive transition only after actual durable closure.

---

# 12. Host conversation-capacity exhaustion

The architecture explicitly covers a product limit that can make the current chat physically unwritable.

## 12.1 No trusted capacity assumption

Step 5.4 assumes no trustworthy API for:

- messages remaining;
- tokens remaining;
- percentage conversation capacity remaining;
- exact time to context expiration;
- exact time to product hard stop.

## 12.2 Reliable host signal

If a host adapter exposes documented actionable imminent destruction:

```text
reliable signal
    -> controlled handoff opportunity/attempt
    -> barrier if execution opportunity remains
    -> success only after actual durable closure
```

The warning may still arrive too late. Trigger reliability does not imply completion capacity.

## 12.3 Advisory host signal or future heuristic

If only elevated risk is known:

```text
advisory risk
    -> technical/OOC warning when useful
    -> recommend/offer proactive move to a fresh chat/runtime
    -> explicit accepted transfer uses normal handoff barrier
```

The warning SHALL NOT claim exact remaining messages/tokens/time unless a future host contract actually guarantees that information.

Possible future heuristics are deliberately noncanonical optimization. They may use host telemetry if available but remain advisory unless separately promoted by an explicit architecture decision backed by a reliable host contract.

## 12.4 No-warning hard stop

If the host stops before HDM can act:

- no final flush/handoff is promised;
- recover actual durable closure only;
- treat loss of newer volatile progress as expected RPO exposure, not corruption;
- Step 5.5 owns policy intended to bound that exposure during normal operation.

---

# 13. Failure / lifecycle matrix

| Case | Canonical result |
|---|---|
| fresh new host, prior state durable | bounded hydrate from native sources; no old chat required |
| controlled handoff, no required delta | validate existing durable closure; no heartbeat write |
| controlled handoff, dirty gameplay state | scoped barrier -> complete required closure -> acknowledge only after actual durability |
| active RuntimeCommand/Resolution | preserve/resume same execution/root identity |
| active Procedure between Commands | Procedure remains independently recoverable |
| pending Choice/Reaction | preserve same Continuation generation/offer; no regeneration |
| accepted Interaction incomplete | make typed meaning or required literal evidence recoverable before safe handoff |
| only hidden partial interpretation exists | no recovery promise for hidden reasoning |
| new gameplay input after barrier freeze | do not semantically accept into frozen scope until success/abandon |
| external native source moves during barrier | invalidate/revalidate affected closure; no global lock |
| reliable destruction signal with enough execution opportunity | normal controlled handoff attempt |
| reliable signal but host cuts off before closure | incomplete/unexpected-loss fallback |
| advisory capacity warning | OOC warning/recommendation; no durability authority |
| heuristic false positive | unnecessary early warning/handoff at worst |
| heuristic false negative | hard-stop/unexpected-loss fallback |
| no warning, chat becomes unwritable | recover actual durable closure only |
| publication failure while old host survives | safe handoff not acknowledged; retry/repair or abandon |
| write may have succeeded, acknowledgement lost | new host determines authoritative durable result under 5.6/5.7 |
| durable write succeeded but handoff message not delivered | newer durable closure remains valid; no rollback |
| intended/prepared write never authoritative | prior durable closure remains recovery point |
| relinquished old host reopened | rehydrate/resync; pre-handoff hot state not reused |
| another host has invisible unpublished SOFT | not discoverable/mergeable by inference; outside durable guarantee |
| active live scope newer than campaign base | current live owner wins; campaign base not fallback current truth |
| non-destructive maintenance | ephemeral orientation allowed; no lifecycle publication solely from maintenance |
| destructive maintenance | controlled handoff barrier |
| no dirty/recovery delta at warning/handoff | no heartbeat/no-op write |
| warning output itself is lost | no gameplay effect; delivery concern remains Step 5.12 |

---

# 14. Relationship to Step 5.5 periodic durability

Step 5.4 owns event-driven host lifecycle conditions and the guarantee of a controlled handoff.

Step 5.5 owns ordinary durability classification/cadence and bounded exposure when no actionable host warning exists.

Canonical handoff boundary:

```text
explicit/reliable destructive handoff reason
    -> Step 5.4 barrier/continuity guarantee
```

Canonical carry-forward:

```text
no usable warning + risk of abrupt host loss
    -> Step 5.5 maximum unpublished-SOFT age/exposure policy

advisory capacity warning / heuristic
    -> may be a Step-5.5 risk-policy input
    -> exact durability reaction NOT decided by Step 5.4
```

No numerical dirty-age/exposure threshold is approved by Step 5.4.

The currently hard-coded runtime `one hour` value is provisional/stale policy pending Step 5.5. It must not be treated as an inherited architectural constant.

The semantic exposure metric should concern gameplay-significant unpublished state, not merely time since any Git commit.

Clean state does not create heartbeat writes.

---

# 15. Rejected abstractions / non-goals

Step 5.4 introduces none of the following:

- `runtime.handoff` current-state class;
- durable generic handoff ticket;
- universal transfer ledger;
- generic `resume_point` snapshot;
- campaign-global host lease;
- campaign-global current-session generation;
- mandatory durable RELINQUISHED marker;
- mandatory handoff checkpoint;
- universal recovery-cut scalar;
- serialized raw prompt/context/model memory;
- chain-of-thought persistence;
- generic host TTL timer;
- exact remaining-message/token estimator;
- authoritative capacity heuristic;
- background save daemon.

A later native subsystem may introduce a narrower scoped ownership/fencing concept only if its own requirements justify it, notably Step 5.8 live ownership.

---

# 16. Later-slice requirements

## Step 5.5 — SOFT / HARD / SAVE durability semantics

Must define:

- exact gameplay-significant state/dependency closure required by a forced controlled handoff;
- relation between handoff and accumulated SOFT/operational state;
- independent maximum age/exposure policy for unpublished gameplay-significant SOFT;
- behavior when no background execution opportunity exists;
- whether/how advisory host-risk telemetry changes durability risk policy;
- no-heartbeat rule for clean state;
- final disposition of current hard-coded `one hour` runtime policy.

## Step 5.6 — Campaign publication & crash consistency

Must make the authoritative outcome of publication decidable/recoverable across preparation, commit, ref-update and acknowledgement failures.

Handoff success cannot depend on intended-but-unproven writes.

## Step 5.7 — Checkpoint / recovery protocol

Must select/pin the newest compatible valid native recovery source set and hydrate it without requiring a handoff ticket, old chat memory or authoritative session status.

It must define normal/suspect/blocked recovery outcomes and exact source-selection protocol.

## Step 5.8 — Multiplayer / live-epoch ownership

Must define any actually necessary native scoped fencing/lease/transfer semantics for shared/live authority.

Step 5.4 does not authorize a campaign-global session lease.

## Step 5.11 — Transcript / history retention

Must retain exact literal input only while an actual live semantic/evidentiary dependency requires it. Narrative smoothness alone does not make full transcript recovery authority.

## Step 5.12 — Host delivery / disclosure boundary

Must define generated/emitted/acknowledged player-facing output across crash/retry, including best-effort capacity warnings where delivery status matters.

Durable gameplay state does not prove a warning/narration was displayed/read.

---

# 17. Runtime/machine realization debt

Later integrated implementation must review at minimum:

- `GAME/CORE/SESSION.md` — split non-destructive maintenance continuation from destructive handoff semantics;
- `GAME/CORE/RUNTIME.md` — align context-loss/handoff guarantees and lost volatile state wording;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` — ensure fresh host recovery depends on durable native evidence only;
- `GAME/CORE/DURABILITY_GUARD.md`, `SESSION.md`, `STORAGE.md`, `PERSISTENCE.md` and affected tests — remove/retain/replace unapproved hard-coded `one hour` policy only after Step 5.5;
- `GAME/SCHEMA/session.schema.yaml` — preserve non-authoritative role or reshape after 5.7/5.8 if justified;
- runtime tests for controlled handoff, interrupted barrier, host hard stop, reliable/advisory/no-signal capacity cases, heuristic false positive/negative, accepted-message evidence, stale/relinquished host and external source movement.

No machine/runtime realization is performed by Step 5.4 architecture closure.

---

# 18. Revisit triggers

Reopen the relevant Step-5.4 decision only if a future requirement proves one of:

1. **exclusive singleplayer host fencing** is required even when durable state/revisions have not changed;
2. a host provides a durable cross-chat transfer/session primitive whose semantics materially improve correctness rather than UX only;
3. Step 5.8 proves native live/CAS state cannot fence stale hosts without a new scoped ownership token;
4. accepted-message semantics cannot be made recoverable through existing Interaction/IntentPlan plus narrowly retained message evidence;
5. a future host-capacity contract exposes reliable semantics that require a stronger adapter lifecycle contract;
6. a generic handoff audit record becomes operationally valuable — it may be added only as non-authoritative evidence unless a separate decision changes that role.

---

# 19. Closure checks

Step 5.4 is architecturally closed because:

- controlled handoff and unexpected loss have distinct honest guarantees;
- handoff success cannot precede actual durable recovery closure;
- local quiescence prevents closure drift without introducing a global lock;
- external native-source movement is revalidated rather than ignored;
- semantic resume state remains in existing native owners;
- accepted-but-not-typed input has an explicit recoverable-evidence rule;
- stale session/host metadata cannot become gameplay authority;
- fresh hydration requires no old chat/model/process memory;
- host capacity exhaustion is supported with reliable/advisory/no-signal semantics;
- no trustworthy remaining-capacity metric is assumed;
- future capacity heuristics are advisory only;
- unwarned hard stop degrades to the normal durable recovery guarantee;
- periodic unpublished-SOFT exposure policy remains explicitly owned by Step 5.5;
- physical publication/recovery/live/delivery protocols remain with their later owners;
- adversarial review produced no unresolved owner-level blocker.

---

# 20. Final Step-5.4 result

```text
BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF   CANONICAL

controlled handoff        actual durable closure before safe acknowledgement
unexpected/hard-stop loss recover newest compatible actually durable closure
host capacity telemetry   optional capability
capacity heuristic         advisory only
handoff snapshot           not introduced
campaign-global host lease not introduced
session authority          rejected
raw model/chat memory      not recovery authority
periodic SOFT exposure     deferred to Step 5.5
```

Next architecture slice after roadmap/status update:

> **Step 5.5 — SOFT / HARD / SAVE Durability Semantics**

Step 5.5 is not started by this specification.