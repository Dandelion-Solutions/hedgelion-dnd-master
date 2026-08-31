# Step 5.4 — Host Lifecycle & Session Handoff — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NOT CANONICAL**

Date: 2026-08-20

Challenges:

- `2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`
- preliminary recommendation **BARRIER-NATIVE**

---

# 1. Candidate under challenge

The research draft proposes:

```text
ATTACHED host
    -> reliable controlled destructive-lifecycle signal
    -> scoped HANDOFF BARRIER
       stop extending handed-off mutation closure
       materialize promised resume semantics into native owners
       make applicable Resumable Runtime Closure durable
    -> acknowledge RECOVERY_SAFE_HANDOFF
    -> old host relinquishes pre-handoff hot state

unexpected loss before successful barrier
    -> recover newest actually durable compatible native source set
```

No mandatory handoff record, campaign-global host lease, handoff snapshot, durable acknowledgement record or raw chat/model-memory persistence.

---

# 2. Strongest counterargument: without a durable handoff token, the old chat can come back

Suppose a controlled handoff occurs while all gameplay state is already durable. BARRIER-NATIVE performs no heartbeat write. The old host and new host therefore see the same campaign HEAD.

Later the user returns to the old chat. Nothing in campaign storage says “this host was relinquished.” Why is this not a stale-host correctness hole?

## Analysis

A durable token would prove a **host coordination fact**, but the question is whether that fact is required for gameplay correctness.

Current correctness already requires every mutation attempt to satisfy current native authorization, owning scope and revision/concurrency rules. An old chat does not gain the right to bypass those rules because it remembers old state.

If no state changed since handoff, the old durable view may still be valid. Treating the old host as unusable solely because a newer chat once existed would add serialization with no semantic benefit.

If state did change, existing branch/live revision checks force refresh/reconciliation before a correctness-sensitive write. In live mode the current live epoch state is authoritative regardless of old session memory.

For transport retry of already accepted execution, Step-3 stable identities provide idempotency. For a genuinely new later user message in the old chat, that is a new Interaction and should be adjudicated against current state after required synchronization.

A persistent “only host X is valid” token is therefore not necessary unless the product requires exclusive one-chat ownership independent of state revision. No such requirement exists, and it would conflict with legitimate multiplayer/multi-session operation.

### Resolution

Refine the stale-host rule:

> `RELINQUISHED` is a local lifecycle obligation on the host that completed the handoff, not a new campaign authority. A later resurrected host may operate only after normal current-source/authority validation; it must not trust pre-handoff dirty or transaction state. Storage does not need to remember the host’s death when native revision/ownership validation is sufficient.

Challenge result: **BARRIER-NATIVE survives; no durable handoff token required.**

Revisit only if a future product requirement demands exclusive host fencing even when native state/revisions are unchanged. Such fencing should then be scoped to the relevant native owner, not assumed campaign-global.

---

# 3. Counterargument: controlled handoff should persist a transfer record for observability

A durable record could answer:

- which host handed off;
- when;
- to which target;
- what recovery source was intended;
- whether transfer completed.

That seems operationally useful and could simplify debugging.

## Response

Observability is not sufficient reason to create a correctness owner.

A mandatory transfer record has several costs:

1. clean handoffs require writes even when all gameplay state is already recoverable;
2. its “recovery refs” risk becoming a universal scalar recovery cut contrary to Step 5.1/5.2 domain-native source composition;
3. target host may not yet exist or be identifiable;
4. the record itself does not prove underlying native state durability;
5. stale/incomplete transfer records need retention, GC and repair semantics;
6. live/multiplayer authority still requires native 5.8 ownership protocol.

Audit/support metadata may later record lifecycle facts if independently useful, but recovery correctness must not depend on such a record.

Challenge result: **no mandatory handoff record. Optional telemetry/audit remains outside Step-5.4 correctness contract.**

---

# 4. Critical challenge: what exactly must a controlled handoff preserve?

Could the runtime preserve only HARD state and intentionally drop current SOFT state, while still calling the handoff successful?

## Strongest case for partial preservation

SOFT by definition may remain unpublished during normal gameplay. Requiring every controlled handoff to flush all SOFT might make context switches expensive and convert ordinary handoff into an implicit SAVE_ALL_DIRTY.

A weaker guarantee could say “handoff resumes from last normal durable frontier,” exactly like crash recovery.

## Counter-analysis

That would erase the semantic distinction Step 5.4 is supposed to establish between:

```text
controlled recovery-safe handoff
unexpected loss
```

If a host knows it is about to destroy the only copy of established gameplay-significant current state and intentionally declines to preserve it, the newer state is knowingly discarded. Calling that a successful continuity handoff is misleading.

The remaining question is not whether current established gameplay state must survive, but **which state is genuinely gameplay-significant/established versus ephemeral**. That classification belongs to 5.5.

Therefore Step 5.4 should require:

> A `RECOVERY_SAFE_HANDOFF` preserves every gameplay-significant current/operational state included by the 5.5 handoff durability class and every Step-5.2/5.3 dependency necessary to resume the current promised semantic point.

This is conceptually close to “flush all established dirty state relevant to current gameplay continuity,” but Step 5.4 must not preempt the exact 5.5 class definitions.

If an operator/user deliberately abandons newer volatile progress after a failed barrier, that is not a successful recovery-safe handoff; it is a destructive termination with recovery to an older durable point.

Challenge result: **BARRIER-NATIVE survives; successful handoff cannot knowingly discard state that the handoff continuity promise includes.**

---

# 5. Critical challenge: must the barrier block new mutation?

Could the runtime publish a handoff closure while continuing to accept gameplay actions, then simply hand off whichever state happened to be latest when destruction occurs?

## Failure case

```text
T1 barrier publication snapshot S selected
T2 publication begins
T3 player action A mutates hot state -> S+A
T4 publication of S succeeds
T5 runtime says handoff safe
T6 old host dies
```

The user reasonably expects A to survive, but only S is durable.

If publication continuously chases new mutations, the barrier may never converge.

## Resolution

A successful handoff needs a **mutation quiescence boundary for the affected ownership scope**.

This does not mean a campaign-global lock. It means:

- once the handoff closure is frozen, no additional gameplay mutation may be acknowledged inside that handed-off scope until either:
  - handoff succeeds and the old host relinquishes; or
  - handoff is explicitly abandoned/failed and normal attached operation resumes from a valid current working state.

OOC responses or independent scopes that cannot affect the closure may continue when safe.

Challenge result: **scoped freeze is required.**

---

# 6. Counterargument: freeze can deadlock when publication fails

If publication stalls/fails, does the host become permanently unusable?

## Resolution

The barrier is not a durable lock and requires no endless wait.

On a confirmed failure while the host remains alive:

```text
HANDOFF_PENDING
    -> report/return typed handoff failure when material
    -> retain current hot state
    -> either retry the durability operation
       OR abandon the handoff and return to ATTACHED operation
```

If the host is externally destroyed despite failure, recovery follows uncontrolled-loss semantics.

This gives bounded failure behavior without a durable lock owner.

Challenge result: **no deadlock requirement; barrier is host-local control flow plus durability precondition.**

---

# 7. Critical challenge: ambiguous publication result and acknowledgement

Suppose the ref update actually succeeds, but the host dies before receiving/recording the response. Is the handoff invalid because no acknowledgement was emitted?

## Analysis

Gameplay durability authority is actual native repository/live state, not the old host’s local acknowledgement bit.

If the write became authoritative, a fresh host should use it even if the old host never got to say “handoff complete.” Conversely, intended/created-but-unreachable writes must not count merely because the old host planned them.

Therefore there are two different concepts:

```text
DURABLE CLOSURE ESTABLISHED
    objective storage/recovery fact

HANDOFF ACKNOWLEDGED
    host/user-facing control-flow fact
```

The first determines what can be recovered. The second determines whether the old host was permitted to intentionally relinquish before the failure.

5.6/5.7 must allow the new host to determine the actual durable result after an ambiguous transport failure.

### Resolution

No durable acknowledgement record is required for gameplay correctness.

Challenge result: **BARRIER-NATIVE survives.**

---

# 8. Counterargument: current `session` record already looks like a lease

It has:

```text
session_id
status
player_id
pc_id
scene_id
base_head_sha
last_published_head_sha
```

Could Step 5.4 simply declare the newest active session authoritative and mark the old session ended during handoff?

## Strongest case

- reuses an existing schema;
- gives explicit stale-host fencing;
- provides a natural transfer marker;
- avoids a new class.

## Failure modes

### 8.1 Coordination metadata would become gameplay authority

Current schema explicitly describes session metadata as coordination/recovery data. Promoting `status` to write authority would silently create a new ACL/lifecycle owner.

### 8.2 “Newest” has no safe universal meaning

Git order is not fictional chronology, and multiple legitimate sessions exist in multiplayer. A campaign-global newest-session winner would serialize independent players/scopes.

### 8.3 Stale status requires liveness protocol

If a host crashes without updating `status`, the durable session remains `active`. Correctness would then need lease expiry/steal rules, clocks or operator repair.

### 8.4 Native ownership still wins

A session record cannot override an active live epoch, PLAYER deactivation, campaign authorization, Procedure state or changed branch revision.

### Resolution

Keep session records non-authoritative. They may point to known frontiers or support UX/audit, but native authority/revision checks fence writes.

Challenge result: **authoritative session-lease alternative rejected.**

---

# 9. Critical challenge: exact player message during mid-interpretation handoff

A destructive warning may arrive after the player sent a message but before RuntimeCommand acceptance.

What exactly is promised?

## Distinguish three states

### U1 — host received bytes, but no accepted Interaction exists

No gameplay-semantic acceptance boundary has been crossed. Internal partial model interpretation is not authority.

If the host disappears, the system may require the external request to be retried/re-presented by the host/user. Step 5.4 must not serialize partial chain-of-thought to preserve it.

### U2 — Interaction accepted, meaning not fully materialized

Step 3 gives the Interaction stable host invocation/message linkage. If the handoff promises this point, enough literal message evidence must survive to reconstruct/complete the accepted interpretation honestly.

### U3 — IntentPlan/typed accepted meaning exists

The semantic typed state is the preferred recovery source. Exact original wording need not be retained merely for seamless prose unless another live semantic dependency requires it.

## Resolution

Handoff promises begin at existing **accepted semantic boundaries**, not arbitrary internal inference progress.

If a destructive handoff occurs at U2, either:

- make the specific accepted message evidence recoverable; or
- finish materializing the stable semantic interpretation before safe handoff acknowledgement.

Do not persist full context/model state.

Challenge result: **existing Interaction/IntentPlan ownership is sufficient, with a later realization requirement for accepted message evidence where necessary.**

---

# 10. Counterargument: platform maximum lifetime should itself force a 5.4 timer

If a platform is known to expire a context after approximately N hours, why not schedule handoff publication before N?

## Analysis

Two cases differ:

### Observable reliable TTL / expiry callback

The runtime can know that this concrete context is approaching destruction. That is legitimate host lifecycle evidence and may trigger the 5.4 barrier.

### Generic documented/observed maximum lifetime without reliable current TTL

This is a risk distribution/policy input, not a concrete lifecycle event. The engine may also lack background execution when the user is inactive.

Hard-coding a platform-specific duration into 5.4 would:

- make architecture depend on a changing host product detail;
- duplicate 5.5 dirty-exposure policy;
- falsely imply exact timed publication when no callback exists.

### Resolution

Reliable current lifecycle signal -> 5.4.

Generic context-expiry risk -> input to 5.5 policy/host adapter, not a canonical 5.4 timer.

The owner’s “one hour” example remains noncanonical.

Challenge result: **scope boundary survives.**

---

# 11. Critical challenge: live/multiplayer transfer may need fencing

Could rejecting a generic transfer token now make Step 5.8 impossible?

## Analysis

Live state already has native epoch identity, active/closed lifecycle, exact live HEAD and CAS. Multiplayer authorization uses PLAYER binding and current synchronization.

A later 5.8 design may discover a need for:

- scoped ownership lease generation;
- transfer/compaction token;
- participant/session fencing inside one live owner.

That would be a **native live ownership mechanism**, not evidence for a campaign-global host/session ticket.

Step 5.4 only requires:

> A controlled handoff may not acknowledge safety while it would strand an active live-owned recovery dependency, and a stale host must not mutate a scope whose current native ownership/revision it has not revalidated.

### Resolution

Defer exact fencing to 5.8 without authorizing a generic host lease.

Challenge result: **BARRIER-NATIVE remains compatible with 5.8.**

---

# 12. Counterargument: no handoff record makes debugging impossible

Not true. Debugging can use existing:

- campaign/live revisions;
- session coordination records if retained;
- runtime execution roots;
- receipts/events;
- publication/audit logs where available.

A correctness-neutral lifecycle audit event could be added later if operational value justifies it. It must remain evidence, not recovery authority.

Challenge result: **observability does not force semantic ownership.**

---

# 13. Crash-window challenge

## W1 — destructive signal before any dirty state

Existing durable closure already sufficient. Barrier may validate no required delta. No heartbeat write. Safe handoff can be acknowledged.

## W2 — dirty canonical state, barrier not yet started

Host still ATTACHED. If it crashes now, recover previous durable closure. If controlled handoff continues, enter barrier and publish required closure.

## W3 — barrier frozen, before publication attempt

No new mutation acknowledged. If crash occurs, only old durable closure is guaranteed.

## W4 — tree/commit preparation in progress

No success assumption. Physical outcome 5.6.

## W5 — authoritative publication succeeds and host receives success

Closure durable. Safe handoff may be acknowledged; host relinquishes old hot state.

## W6 — authoritative publication succeeds but acknowledgement is lost

Fresh host recovers new durable closure. Lack of friendly handoff acknowledgement does not roll back canon.

## W7 — publication fails while old host alive

Safe handoff not acknowledged. Hot state remains current in old host. Retry or abandon handoff.

## W8 — publication fails then host is externally destroyed

Uncontrolled/degraded loss. Recover prior durable closure.

## W9 — old host reappears after new host changed campaign

Must refresh/revalidate before mutation. Old hot transaction state cannot be published blindly.

## W10 — old host reappears but nothing changed

It may rehydrate/validate the same durable state and continue; no semantic need to reject it solely due to identity.

## W11 — live epoch advanced while old host slept

Current live owner/revision wins. Old host must adopt current live state before dependent action/write.

## W12 — accepted Interaction survives but raw wording does not

If typed IntentPlan preserves complete accepted meaning, resume from it. If not, this is insufficient recovery evidence and must not be filled by invented text.

No crash window establishes a need for a generic handoff record.

---

# 14. Strongest remaining objection: handoff barrier is just a renamed HARD boundary

Why have 5.4 at all if 5.5 will define HARD?

## Response

They answer different questions.

Step 5.4 owns **the lifecycle condition and guarantee**:

```text
known destructive context loss + recovery-safe transfer intent
    -> do not relinquish until promised resume state is durably recoverable
```

Step 5.5 owns **which state classes/dirty closure must be published and how ordinary buffering behaves**.

The lifecycle condition is independent of whether the eventual durability vocabulary calls it HARD, HANDOFF_REQUIRED, SAVE-equivalent, or another typed reason.

This separation is necessary because:

- unexpected crash does not have the barrier opportunity;
- clean handoff need not write;
- destructive maintenance is different from ordinary SOFT cadence;
- the same lifecycle barrier can apply to campaign + runtime operational/native sources without defining their physical transaction.

Challenge result: **5.4 remains a distinct necessary slice.**

---

# 15. Revised recommendation

After challenge, recommend **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** with HIGH confidence.

Refined laws for a candidate specification:

1. host/context lifecycle is distinct from campaign/session/procedure/fictional lifecycle;
2. only a reliable current destructive-lifecycle signal or explicit handoff intent creates a 5.4 controlled handoff opportunity;
3. a successful recovery-safe handoff requires a scoped mutation quiescence barrier;
4. the barrier preserves every gameplay-significant semantic state that the 5.5 handoff durability class promises, plus all Step-5.2/5.3 required dependencies;
5. native world/execution/temporal/live owners remain authority; no handoff snapshot copies them;
6. if the promised closure is already durable, no heartbeat/handoff commit is required;
7. safe handoff is acknowledged only after durable closure is known established;
8. publication failure while the host survives leaves handoff incomplete; host may retry or abandon the handoff;
9. external destruction after failed/incomplete handoff is treated as uncontrolled/degraded loss;
10. after unexpected loss, recovery resumes the newest actually durable compatible native source set and never invents lost HOT/SOFT state;
11. ambiguous old-host write acknowledgement is resolved from actual durable evidence under 5.6/5.7;
12. persistent `session` metadata remains coordination/projection, not gameplay or write authority;
13. relinquished/stale hosts must revalidate current native owning scope/revisions before mutation; no campaign-global host lease is introduced;
14. accepted Interaction/IntentPlan boundaries define recoverable input semantics; partial model reasoning is never persisted as authority;
15. exact message evidence is retained only when it is genuinely required to preserve accepted meaning;
16. non-destructive maintenance may use ephemeral orientation context; destructive maintenance uses the handoff barrier;
17. reliable host TTL/expiry signal may trigger the barrier; generic platform lifetime risk does not become a 5.4 timer;
18. independent max unpublished-SOFT age belongs to 5.5, with no approved numeric value yet;
19. exact live/multiplayer fencing remains 5.8;
20. host delivery acknowledgement remains 5.12.

---

# 16. Human-decision assessment

The analytical challenge does **not** find a remaining product-semantic trade-off that justifies choosing B or C over BARRIER-NATIVE.

The rejected alternatives add persistent authority/coordination machinery without a current correctness requirement.

However, this is still an architectural design and requires owner approval before candidate canonicalization under the project/Superpowers process.

Recommended approval target:

> Adopt **BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF** as the Step-5.4 architecture direction, with later slices owning the durability class, physical publication, recovery wire protocol and live fencing details.

No implementation should begin on this approval.