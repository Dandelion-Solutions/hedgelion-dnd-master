# Step 5.4 — Host Lifecycle & Session Handoff — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE CHALLENGED, REFINEMENTS REQUIRED**

Date: 2026-08-20

Reviews:

- `2026-08-20-step-5-4-host-lifecycle-session-handoff-candidate-spec.md`
- owner-approved **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** direction
- owner-added host conversation/message/context capacity exhaustion case

Review objective:

> Attempt to break the candidate through lifecycle races, external source movement, host-capacity uncertainty, stale-host resurrection, partial semantic acceptance, multiplayer partitioning and misleading acknowledgement semantics before canonicalization.

---

# 1. Review result summary

The review does **not** find a reason to reopen the owner-approved BARRIER-NATIVE direction.

It does find six significant specification refinements required before canonicalization:

1. reliable imminent-destruction evidence does **not** imply sufficient execution budget remains to complete handoff;
2. handoff closure must remain compatible under external mutation of participating native sources without requiring a global lock;
3. post-freeze external/player input must not silently extend the frozen mutation closure;
4. old-host resurrection must not imply that another host's unpublished volatile state can be detected or merged;
5. advisory capacity warnings/heuristics must remain OOC/best-effort and may not themselves create a durability guarantee;
6. capacity-risk signals may be an input to later 5.5 durability policy, but Step 5.4 must not turn advisory risk into a hidden HARD classifier.

All six are compatible with the approved direction and can be resolved mechanically in the canonical specification.

---

# 2. Challenge A — “reliable warning” may arrive too late to save anything

## Attack

Candidate LAW 5.4-14 permits a reliable impending-destruction signal to enter the handoff barrier.

But a signal can be semantically reliable while still arriving with effectively zero remaining tool/model/runtime execution opportunity.

Example:

```text
T0 host says context will terminate
T1 runtime recognizes RELIABLE_DESTRUCTIVE
T2 host prevents further repository/tool execution
T3 context dies
```

If the architecture implicitly equates “reliable warning exists” with “controlled handoff is now achievable,” it creates a false guarantee.

## Resolution

Separate:

```text
DESTRUCTION PREDICTION RELIABILITY
from
HANDOFF EXECUTION OPPORTUNITY
```

A reliable signal is only a trigger/opportunity **if the host still permits the required barrier work**.

Canonical refinement:

> A reliable destructive signal may require/attempt the controlled handoff path, but safe-handoff success remains conditioned solely on actual durable closure. If the host removes execution opportunity before closure succeeds, the result is incomplete handoff/unexpected loss, not a violated or retroactively satisfied guarantee.

No minimum remaining token/message/time budget is assumed.

Finding disposition: **RESOLVED — specification refinement, no owner decision.**

---

# 3. Challenge B — local quiescence is insufficient if participating native sources move externally

## Attack

Suppose the old host freezes its own mutation scope and prepares closure against native source set `C + L1`.

Another valid host/player advances a participating live/campaign source to `L2` while the handoff publication/validation is in progress.

If Step 5.4 treats local freeze as enough, the old host might acknowledge a closure that is no longer the current compatible source set.

## Analysis

A campaign-global lock would violate Step 5.1/5.2 partitioning and legitimate multiplayer concurrency.

The existing architecture already relies on:

- exact pinned revisions for one operation;
- owning-scope routing;
- optimistic revision/CAS checks;
- transaction invalidation/reselection on relevant external movement.

Therefore handoff does not need to prevent all external mutation. It must prevent **local closure drift** and detect external invalidation.

## Resolution

Canonical refinement:

> Scoped quiescence freezes new acknowledged mutation by the handing-off host in the affected dependency closure. External/native-source movement that can invalidate the selected closure causes the relevant handoff selection/publication attempt to be revalidated, reselected or fail under the later 5.6–5.8 protocols. Handoff success requires a compatible durable source set at the success boundary, not merely a locally frozen snapshot.

No distributed lock or universal source generation is introduced.

Finding disposition: **RESOLVED — strengthens BARRIER-NATIVE.**

---

# 4. Challenge C — what happens to a new player message after the barrier freezes?

## Attack

The candidate says no new gameplay mutation may be acknowledged after H3, but it does not fully classify a new input arriving while handoff is pending.

Potential failure:

```text
H3 closure frozen at S
player sends action A
runtime accepts Interaction/IntentPlan A
but does not include A in closure
H6 S becomes durable
H7 handoff declared safe
```

Now accepted semantic state exists outside the promised closure.

## Resolution

Canonical refinement:

After the barrier freezes one scope:

- an already accepted Interaction/IntentPlan from before freeze that belongs to the handoff promise MUST be included/materialized as required;
- a new gameplay input affecting the frozen scope SHALL NOT cross its semantic acceptance boundary until handoff succeeds or is abandoned;
- host/OOC communication that cannot mutate or create accepted gameplay-semantic state may continue when useful;
- if architecture/runtime later supports queued external input, queueing is host transport state only until a fresh accepted Interaction is created under the resumed host/current state.

This avoids serializing raw inbound messages into the handoff closure merely because they arrived physically.

Finding disposition: **RESOLVED — acceptance barrier made explicit.**

---

# 5. Challenge D — old host cannot know whether another host has unpublished SOFT state

## Attack

Candidate stale-host semantics say an old/relinquished chat may rehydrate the same durable state and continue if durable state has not changed.

But another host may currently hold newer gameplay-significant SOFT state only in its own volatile context. Repository state is unchanged, so the old host cannot detect it.

This creates a temptation to claim that rehydration proves the old host is current. It does not.

## Strongest argument for introducing a global host lease

A durable active-host/session token could fence the old chat even when campaign state has not advanced, preventing two singleplayer chats from building incompatible unpublished branches of reality.

## Counter-analysis

A global lease would:

- require a durable write/claim on clean chat startup/handoff;
- add crash/expiry/takeover semantics;
- conflict with legitimate multi-host multiplayer scopes;
- need a new product policy for whether singleplayer is exclusive-host;
- exceed the approved Step-5.4 requirements and re-open a material owner decision that current recovery correctness does not require.

More importantly, **no persistence architecture can discover state that exists only in another unreachable volatile host without some separately persisted coordination authority**. BARRIER-NATIVE intentionally does not promise that.

## Resolution

Canonical refinement must state the limit explicitly:

> Rehydration proves consistency with the selected durable native source set; it does not prove that no other host currently contains unpublished volatile state. Controlled handoff prevents this ambiguity for the source host by requiring its promised state durable before relinquishment. Outside a completed handoff, parallel/abandoned volatile host state is outside the durable recovery guarantee and must never be silently inferred or merged.

For a host that **knows locally** it has relinquished, normal gameplay continuation from pre-handoff hot state is forbidden. If deliberately reused later, it begins as fresh/stale hydration and cannot claim preservation of unknown volatile progress elsewhere.

A future exclusive-singleplayer-host requirement would be a separate product/architecture decision and could justify a scoped coordination token. It is not silently introduced here.

Finding disposition: **RESOLVED WITH EXPLICIT LIMIT / REVISIT TRIGGER. No current owner decision required because BARRIER-NATIVE approval explicitly rejected campaign-global lease semantics.**

---

# 6. Challenge E — advisory capacity warning can accidentally become a hidden durability authority

## Attack

The user wants a warning when a chat appears near a host cutoff. Candidate LAW 5.4-15 says HDM SHOULD warn and recommend transfer on advisory signals.

A future implementation might then accidentally encode:

```text
heuristic >= threshold
    => must flush
    => HARD
```

or treat the warning as proof that context destruction is imminent.

That would silently move 5.5 policy into 5.4 and turn a false-positive-prone estimate into correctness logic.

## Resolution

Canonical refinement:

- advisory warning is OOC/presentation/control-flow assistance;
- it does not itself establish `HANDOFF_PENDING` unless explicit transfer is accepted/initiated or the host adapter upgrades the signal to a documented reliable destructive condition;
- it does not itself define a forced durability class;
- later 5.5 MAY use host-risk telemetry as one policy input, but must preserve the distinction between advisory risk and actual durability evidence;
- warning delivery success is not recovery correctness and remains outside 5.4/inside later host-delivery concerns where relevant.

Finding disposition: **RESOLVED.**

---

# 7. Challenge F — false-positive heuristic could create fictional effects

## Attack

A capacity heuristic fires while the player is in a tense scene. If the engine treats the warning like a session pause/end or fictional delay, it could mutate lifecycle/time incorrectly.

## Resolution

Capacity warnings and handoff plumbing are technical/OOC host events.

They SHALL NOT by themselves:

- pause/complete the campaign;
- advance world time;
- end a scene/encounter/Procedure;
- create NPC activity;
- consume resources;
- resolve pending player declarations.

A clean handoff resumes the same semantic point unless later gameplay/campaign intent separately changes it.

Finding disposition: **RESOLVED; already implied by LAW 5.4-1/16, make explicit in canonical capacity section.**

---

# 8. Challenge G — could an advisory signal reasonably cause an opportunistic safety flush anyway?

## Attack

Even if the user does not transfer chats, a near-capacity warning may be valuable evidence that volatile-state loss risk is elevated. Why prohibit a flush until explicit handoff?

## Analysis

This is a legitimate **durability policy** question, not host-lifecycle correctness.

Possible later policies include:

- advisory signal only warns;
- advisory signal lowers the temporary dirty-exposure budget;
- advisory signal immediately forces a safety publication;
- no special durability response beyond normal cadence.

Those choices trade I/O/latency against expected loss and belong to Step 5.5.

## Resolution

Step 5.4 carries the signal semantics forward but does not choose the durability reaction.

Finding disposition: **DEFERRED TO 5.5 — explicitly owned, not lost.**

---

# 9. Challenge H — “all promised state durable” can hide cross-domain dependency omissions

## Attack

The phrase “all promised state” could be implemented as only the dirty world files the old host remembers, while missing:

- active Procedure root;
- accepted Continuation/Choice;
- temporal routing membership;
- interpretation context;
- live-owned dependency;
- stable message evidence for accepted but not-yet-materialized input.

## Resolution

The handoff closure is not an arbitrary dirty list. It is the Step-5.2 Resumable Runtime Closure plus Step-5.3 continuity requirements under the durability class later chosen by 5.5.

Canonical spec should restate this by reference and require transitive recovery dependencies/recovery-routing coherence.

Finding disposition: **RESOLVED — no new owner.**

---

# 10. Challenge I — do we need durable acknowledgement after a clean no-write handoff?

## Attack

If no commit is made and acknowledgement is lost, the new host cannot tell whether the old host intended a handoff.

## Analysis

Intent is not recovery authority. If existing native state was already durable, the new host can safely hydrate it regardless of whether the old host emitted a handoff-success message.

A durable acknowledgement would only record coordination/history, not improve gameplay-state correctness.

## Resolution

No mandatory durable acknowledgement/ticket.

Optional future audit telemetry remains allowed if non-authoritative.

Finding disposition: **RESOLVED — candidate survives.**

---

# 11. Challenge J — accepted message evidence and host transcript may be unavailable cross-chat

## Attack

At handoff, Interaction U2 is accepted but typed IntentPlan is incomplete. The only evidence of exact player wording lives in the doomed chat host and is not independently durable.

A generic claim that “Interaction owns message linkage” is insufficient if that linkage cannot be resolved after host destruction.

## Resolution

Step 5.4 requires **recoverable evidence, not merely an identifier**.

Before safe handoff at U2, one of these must become true:

1. complete enough typed semantic meaning is materialized into durable Interaction/IntentPlan state; or
2. the specific accepted message evidence required to complete interpretation becomes durably/recoverably available under the later transcript/message-evidence contract.

A dangling pointer to inaccessible host text is not a valid Resumable Runtime Closure.

Exact representation/retention remains 5.11.

Finding disposition: **RESOLVED — strengthen wording; physical representation deferred.**

---

# 12. Challenge K — destructive maintenance can switch interpretation context

## Attack

A handoff triggered by runtime-package switch could persist open execution and then hydrate it under a newer incompatible runtime.

## Resolution

Step 5.2 INTERPRETABILITY CLOSURE already forbids arbitrary reinterpretation of open execution.

Canonical 5.4 must explicitly inherit that requirement: handoff success for open execution includes recoverable compatible accepted runtime/catalog/rules interpretation context. Migration/adoption may separately transform it only through an authorized compatible protocol.

Finding disposition: **RESOLVED — inherited constraint.**

---

# 13. Challenge L — player-facing warning may itself be cut off

## Attack

An advisory warning could be generated but the host hard-stops before the player sees it. Does that create a broken handoff state?

## Resolution

No. Warning delivery is best-effort UX and not the handoff authority.

If no explicit controlled handoff actually completes, recovery remains governed by actual durable state.

Host-delivery acknowledgement semantics remain Step 5.12.

Finding disposition: **RESOLVED / 5.12 boundary preserved.**

---

# 14. Revised crash/lifecycle matrix

| Window/case | Required result |
|---|---|
| reliable signal but no further execution opportunity | no false success; unexpected/incomplete-loss recovery |
| reliable signal + barrier work available | normal controlled handoff attempt |
| advisory signal only | OOC warning/recommendation; no automatic correctness claim |
| heuristic false positive | early warning/transfer at worst |
| heuristic false negative | hard-stop fallback to durable closure |
| barrier freezes after accepted Interaction | accepted semantic dependency joins closure |
| new gameplay input arrives after freeze | do not accept into frozen scope until success/abandon; transport queue is not semantic acceptance |
| external source moves during barrier | selected closure invalidated/revalidated under native protocol; no global lock |
| old host local hot state relinquished | do not continue from it directly |
| old host rehydrates same durable revision | valid only relative to durable state; does not prove absence of volatile state elsewhere |
| unknown other host has unpublished SOFT | not discoverable/mergeable by inference; outside durable guarantee |
| accepted message pointer cannot resolve cross-host | handoff closure invalid until meaning/evidence is made recoverable |
| warning output never reaches player | no gameplay effect; 5.12 delivery concern |

---

# 15. Authority contamination check

Candidate introduces only these new logical concepts:

```text
handoff scope
HANDOFF_PENDING behavioral barrier
host lifecycle signal class
RELINQUISHED host-local obligation
```

Classification:

| Concept | Class | Authority risk |
|---|---|---|
| handoff scope | derived operation/dependency scope | not current-state owner |
| barrier | host-local control-flow / durability precondition | not persisted gameplay authority |
| lifecycle signal class | host capability input | not gameplay state |
| RELINQUISHED | host-local lifecycle obligation | not campaign/global lease |

No new durable current-state owner is justified.

Review result: **no contamination blocker** provided canonical wording keeps these concepts non-authoritative.

---

# 16. Revisit triggers

Reopen Step-5.4 ownership only if a later requirement proves one of the following:

1. singleplayer product semantics require strict exclusive one-host fencing even when durable gameplay state/revisions have not changed;
2. a host platform provides a durable cross-chat session/transfer primitive whose semantics materially improve correctness rather than UX only;
3. Step 5.8 demonstrates that existing native live/CAS state cannot fence stale hosts without a new scoped ownership token;
4. accepted message semantics cannot be made recoverable through existing Interaction/IntentPlan plus narrowly retained message evidence;
5. a future host-capacity contract exposes reliable semantics that require a stronger adapter-level lifecycle state than the generic signal classes defined here.

These are explicit revisit triggers, not current blockers.

---

# 17. Review conclusion

**BARRIER-NATIVE survives adversarial review.**

No new human product/architecture choice remains after the owner-approved direction and host-capacity scope addition.

Required canonical refinements are mechanical consequences of the decision:

1. reliable warning != guaranteed execution budget;
2. freeze local mutation + validate external native-source compatibility;
3. block semantic acceptance of new dependent gameplay input after closure freeze;
4. state the limit around undiscoverable volatile state in another host;
5. keep advisory warnings/OOC heuristics non-authoritative;
6. defer any opportunistic durability reaction to advisory risk to 5.5;
7. require resolvable accepted message evidence, not dangling host-only references;
8. preserve Step-5.2 interpretation-context closure.

Recommendation: incorporate these refinements into a resolution gate and canonical specification without reopening the owner decision.