# Step 5.2 — Resumable Runtime Closure — Analytical Challenge

Status: **ANALYTICAL CHALLENGE COMPLETE — DECISION BRIEF NEXT**

Date: 2026-08-20

Challenged artifact:

- `2026-08-20-step-5-2-resumable-runtime-closure-research-draft.md`

This challenge attempts to falsify the draft recommendation rather than improve its presentation.

---

# 1. Challenged recommendation

Research proposed:

1. `Resumable Runtime Closure` is a correctness property over existing semantic owners, not a new state authority.
2. Step-3 runtime owners already contain most irreducible in-flight execution semantics.
3. Temporal Agenda remains rebuildable.
4. The missing capability is bounded typed discovery of active operational roots and otherwise-unreachable armed temporal owners.
5. Exact physical partitioning of that routing/index evidence should be deferred to 5.7/5.8 unless it changes semantics now.

The challenge attacks each point.

---

# 2. Challenge A — Is “root membership” secretly a new semantic authority?

## Attack

If cold recovery trusts a root projection, omission of an active Procedure or scheduled Effect causes gameplay-significant state to disappear. Therefore the projection appears authoritative: it decides what exists after restart.

If so, the draft has merely renamed a new authority as an “index”.

## Analysis

This is analogous to any required routing index:

```text
native owner state
    = semantic truth

routing/index membership
    = required evidence for bounded retrieval
```

The projection is not allowed to answer questions about the owner’s state. It cannot say:

- Procedure resources are X;
- Effect is active;
- child firing is pending;
- Choice option set is Y.

It can only route to the owner that answers those questions.

A mismatch has asymmetric semantics:

```text
projection says owner exists, owner missing
    -> recovery/integrity defect

owner says terminal, stale projection still lists it
    -> owner wins; projection is stale/corrupt routing evidence

owner active but projection omits it
    -> projection completeness defect
```

The last case is hard to detect during ordinary cold recovery because the omitted owner is not discovered. That does not make the projection semantic authority; it makes **transactional index completeness** a safety requirement, exactly as a database secondary index may be operationally required without becoming the row owner.

A repair/audit slow path may scan broader state when integrity is already suspect; ordinary recovery must not.

## Result

**Challenge rejected.** Required routing evidence can be correctness-critical without becoming writable semantic authority.

Required refinement:

> Step 5.2 must explicitly say that recovery-routing projections are **trusted for bounded discovery only under a coherence invariant**, while native owners remain authoritative for all state/lifecycle semantics.

---

# 3. Challenge B — Does one compact root projection become a global multiplayer write hotspot?

## Attack

If every new/settled Command, Procedure, pending interaction and temporal obligation updates one campaign-global `RECOVERY_ROOTS.yaml`, independent multiplayer scenes would contend on the same file.

This would directly undermine the project’s structural conflict-reduction strategy and could turn routine local mechanics into global synchronization.

## Analysis

The research draft kept physical representation open, but its “one lightweight projection” alternative is dangerous if interpreted as one hot singleton.

Existing architecture already establishes:

- independent scenes should normally touch separate records;
- `CURRENT` should not be updated for every local movement/action;
- live epochs own their local hot state independently;
- one entity may not be live-owned by two epochs;
- cross-scene synchronization is exceptional.

Therefore a Step-5.2 recovery-routing contract that **requires one global mutable root registry** would introduce a cross-scene authority/contention surface not justified by semantics.

The logical recovery root set can instead be **composed from bounded partitions**:

```text
campaign/global routing roots
+ independently owned scene/procedure/runtime partitions
+ live-epoch local roots
+ typed temporal-source indexes/partitions
```

A cold runtime may read several bounded root partitions. “Bounded” does not mean “one file”.

## Result

**Challenge succeeds against a singleton interpretation.**

Refined rule:

> Step 5.2 SHALL NOT require one globally hot recovery-root record/file. Recovery-routing evidence must be partitionable by existing writable/semantic ownership scope so independent gameplay does not gain artificial shared-write contention.

This materially weakens Alternative B as “one file”, but not the logical projection requirement.

---

# 4. Challenge C — Can filesystem placement eliminate explicit root projections entirely?

## Attack

Place only active runtime owners under deterministic directories:

```text
RUNTIME/ACTIVE/PROCEDURES/
RUNTIME/ACTIVE/COMMANDS/
```

Then a cold runtime lists those directories. No root index/descriptor is needed.

Likewise, place only armed temporal owners in active subdirectories.

## Analysis

This representation can satisfy bounded discovery if:

- directory cardinality scales with active owners only;
- owner activation/terminality atomically changes presence/location;
- cross-scope ownership is partitioned;
- historical retention does not accumulate in the active directory;
- live/campaign location rules remain coherent.

But the directory membership itself is the routing projection:

```text
path membership == active recovery membership evidence
```

The logical contract remains identical. Physical placement merely encodes it without a separate YAML index.

Further, moving records between ACTIVE/HISTORY has publication/retention/GC semantics that belong to 5.6/5.7/5.13.

## Result

**Challenge does not invalidate the logical projection requirement.** It proves that the Step-5.2 contract should be representation-neutral enough to allow directory membership as an implementation of bounded root membership.

---

# 5. Challenge D — Is bounded temporal-owner enumeration really necessary?

## Attack

Perhaps off-screen Effects/resources can be loaded lazily only when their entity becomes relevant. Then no global temporal-source index is needed and Agenda can rebuild incrementally.

## Counterexample

An off-screen owner can carry a mechanically active deadline whose firing changes world state before that owner is otherwise loaded.

Examples:

- disease save on an absent NPC;
- curse expiration or periodic effect;
- delayed recovery that changes capability before later encounter;
- world-process consequence represented by an admitted owner-local temporal mechanism.

If the runtime cannot know the obligation exists until somebody happens to load the owner, elapsed time can pass beyond the deadline without processing required work.

That violates the central Step-5 continuity invariant.

## Scope qualification

Not every dormant world record must be indexed.

Only owners carrying an **armed mechanically relevant temporal obligation** that can become due independently of ordinary direct retrieval require membership in the temporal-source discovery set.

If a temporal rule is defined to be evaluated lazily only on owner access, that is a different semantic contract and must be explicit; the current Step-2 scheduled-trigger model does not establish such a lazy-only rule.

## Result

**Challenge rejected.** Bounded armed-temporal-owner discovery is necessary unless 5.3 explicitly proves a narrower lazy semantic for a specific mechanism.

---

# 6. Challenge E — Does this accidentally recreate Temporal Agenda durably?

## Attack

A temporal-source membership index might end up storing deadline/order/due state. At that point it is effectively serialized Temporal Agenda.

## Analysis

Step 5.2 can draw a hard line:

Allowed routing projection fields conceptually:

```text
owner_kind
owner_id / owner_ref
scope_ref if required for retrieval
```

Not owned by the routing projection:

```text
deadline
priority/order
next_due
firing status
selected trigger
chronology comparison result
```

Those values come from the owner/TemporalBinding/chronology context or, once selected, Step-3 pending invocation state.

A storage implementation may duplicate a deadline as a disposable search optimization only if later architecture explicitly treats it as an invalidatable projection. Step 5.2 does not need or authorize that optimization.

## Result

**Challenge rejected with a stronger exclusion rule.**

---

# 7. Challenge F — Could all active Procedures be discovered from open Commands?

## Attack

If every Procedure exists only while a root Command/Resolution chain is open, Procedure membership need not be separately rooted.

## Counterexample

Step 3 deliberately defined Procedure as an independently addressable lifetime owner that survives multiple Resolutions, reactions, suspensions and retries.

Turn/action budgets in an encounter-like rules procedure can exist:

```text
Command A settled
Procedure still active
no current Resolution
player/actor handoff
Command B not yet accepted
```

Procedure state must survive that interval.

Making Procedure lifetime equal one Command would contradict the accepted Step-3 boundary.

## Result

**Challenge rejected.** Active Procedure discovery is independently required.

New implementation observation:

Current `runtime-procedure-state.schema.json` lacks explicit lifecycle/status. Later machine realization must provide a deterministic way for storage/root membership to know whether Procedure remains active; this need does not change Procedure ownership.

---

# 8. Challenge G — Is a pending Interaction/IntentPlan actually a durable root class?

## Attack

Persisting pending clarifications could bloat runtime history and create artificial durability around ordinary conversational turns.

Perhaps all such state should be reconstructed from transcript/chat.

## Analysis by cases

### Generic open handoff

“Что делаешь?” after a settled state does not need durable prompt identity. Scene/world state suffices.

### Pure OOC question

No gameplay semantic resume owner required unless it changed durable configuration/state through another admitted owner.

### Player declaration awaiting material clarification

Example:

```text
"I attack the guard" when two materially different guards are valid targets
```

If the system has already accepted the declaration and asks a clarification, losing the declaration and restarting with generic scene narration can alter player intent or cause the player to unknowingly issue a second action.

Step 3 explicitly permits `clarification_required` IntentClauses without Command creation.

Therefore **some** pending Interaction/IntentPlan state is gameplay-significant.

However it need be durably rooted only when an applicable durability/handoff boundary claims that unresolved point will survive. Ordinary same-chat clarification remains hot/volatile under existing policy.

## Result

**Challenge partially succeeds.** Pending Interaction/IntentPlan is not an always-durable root family. It is a **conditional root class at a promised durable boundary** when losing the already-accepted unresolved declaration would change resume semantics.

This keeps ordinary conversational overhead sparse.

---

# 9. Challenge H — Does fixed RNG belong only in ResolutionTrace?

## Attack

GAME `RANDOMNESS.md` and `MECHANICS_INTEGRITY.md` emphasize an in-memory resolution trace. Maybe recovery can retain/persist trace rather than duplicate fixed RNG in Resolution/Continuation.

## Analysis

Step 3 already establishes fixed RNG fields on the execution owners. Trace is explicitly compactable after safe boundaries and exists for audit/calculation explanation.

If trace were the sole continuity owner:

- Continuation could not be portable independently;
- trace retention lifecycle would control execution correctness;
- retry could depend on verbose diagnostics;
- a compacted trace could accidentally permit reroll.

That would invert accepted ownership.

## Result

**Challenge rejected.** Fixed accepted RNG belongs in execution owner continuity state; trace remains audit evidence.

Runtime prose should eventually be aligned during implementation, but no architecture change is needed.

---

# 10. Challenge I — Must future RNG stream state always survive?

## Attack

Continuation schema currently requires `future_rng_frontier`. Does 5.2 therefore require one persistent deterministic RNG stream for all resumable execution?

## Analysis

The accepted invariant is “do not reroll already fixed inputs,” not “all future randomness across restarts must produce the same sequence”.

A future RNG frontier is only mechanically necessary if runtime semantics already reserve/allocate a stream/substream/draw identity before suspension.

If the next roll is a genuinely future experiment whose stakes/mechanics have not yet required a draw, new actual RNG after restart is valid.

## Result

**Challenge succeeds against an over-broad interpretation.**

Refined 5.2 rule:

- fixed/accepted/generated values must survive;
- pre-reserved future RNG identity/state must survive if already semantically committed;
- 5.2 does not mandate a global deterministic RNG stream;
- 5.3 must reconcile this with the existing required schema field and may narrow/redefine its representation without weakening Step-3 fixed-input semantics.

This is a later machine-contract issue, not a new owner decision.

---

# 11. Challenge J — Can checkpoint be made current by simply creating one at every active-runtime change?

## Attack

If checkpoints always follow any creation/change of active Procedure/Continuation, checkpoint could be the active root registry and solve bounded discovery.

## Analysis

That would silently rewrite accepted persistence cadence:

- checkpoints are intentionally sparse;
- ordinary saves/publications do not require checkpoint creation;
- Procedure state can change frequently;
- forcing checkpoint per execution change would create write/retention overhead and make a recovery descriptor into a de facto hot state mechanism.

This belongs to neither Step 5.2 nor the accepted sparse model.

## Result

**Challenge rejected.** Checkpoint may capture a historical/selectable root cut but cannot be the only current active-root source.

---

# 12. Challenge K — Does one “durable recovery basis” violate B-NARROW when live epochs are active?

## Attack

The phrase “last durable recovery basis” sounds scalar. With campaign HEAD plus independent live revisions, recovery may require several durable domain-native revisions.

## Analysis

Step 5.1 already forbids a universal comparable frontier. Therefore “basis” must mean:

> the compatible set of native durable sources selected for one recovery operation, not one scalar/version.

Conceptually:

```text
campaign HEAD C
scene A -> live epoch LA@rev17
scene B -> live epoch LB@rev8
runtime root partitions at their owning scopes
```

No order is inferred between LA and LB.

The recovery operation verifies compatibility/reference relations, not scalar dominance.

## Result

**Challenge succeeds against scalar wording.**

Refinement:

Use **durable recovery source set/basis** as a composed compatible selection of domain-native revisions. Do not introduce a universal RecoveryCut identity in Step 5.2.

---

# 13. Challenge L — Is Story/transcript needed to recover player meaning?

## Attack

A player declaration or social exchange may be semantically rich enough that typed state alone loses nuance. Perhaps exact transcript must be part of every recovery closure.

## Analysis

If future mechanics/canon depends on a meaning, that meaning must be represented by the accepted semantic owner before the system promises durable resume.

Using transcript as hidden semantic authority would violate:

- Step-4 Story noncanonicality;
- runtime.message retention optionality;
- bounded cold-recovery semantics;
- deterministic ownership.

Exact wording may be retained for history/audit when useful, but inability to reconstruct a required semantic rule from canonical/runtime owners is a materialization defect.

## Result

**Challenge rejected.** Transcript is not a universal closure prerequisite.

---

# 14. Challenge M — Does root membership need one independent lifecycle/ID?

## Attack

The root set changes over time. Perhaps each set version needs identity so checkpoint/support/recovery can reference it, implying `runtime.recovery_closure`.

## Analysis

A changing projection does not automatically deserve record identity.

The relevant evidence can be pinned by the native durable source that contains it:

- campaign commit SHA for campaign-owned root projection/index;
- live branch HEAD/revision for live-owned projection/index;
- checkpoint can later reference the native source revisions it describes.

Step 5.1 already gives these domains identity. Adding a closure ID would duplicate composition identity without an independent consumer/lifecycle.

## Result

**Challenge rejected.** No first-class closure record/ID is currently justified.

---

# 15. Adversarial scenario matrix

| Scenario | Draft result under challenge | Survives? |
|---|---|---:|
| clean durable state, no runtime work | native world roots + temporal-source membership | yes |
| SOFT state lost before boundary | rollback to previous durable source set | yes |
| suspended Resolution | typed execution owners + root membership | yes |
| active Procedure between Commands | separately rooted Procedure | yes |
| post-commit mandatory child | Command/segment descriptor survives | yes |
| missing child descriptor after Event commit | integrity defect; no rediscovery | yes |
| off-screen scheduled Effect | temporal-source membership required | yes |
| Agenda missing | rebuild | yes |
| two live epochs | independent scene-native live roots | yes |
| stale session | refresh; session not authority | yes |
| pending clarification | conditional Interaction/Intent root at durability boundary | yes |
| checkpoint behind HEAD | current root membership independent of checkpoint | yes |
| omitted root index entry | projection coherence defect | yes, with invariant |
| stale index lists terminal owner | owner wins, repair index | yes |
| one global root file under multiplayer | rejected as mandatory architecture | no singleton requirement |
| transcript absent | semantics must live elsewhere | yes |

---

# 16. Strongest remaining architecture

After challenge, the recommended architecture is more precise:

```text
RESUMABLE RUNTIME CLOSURE
    = correctness property
    = compatible durable native source set
      + transitive closure from bounded typed recovery-routing roots

semantic authority
    remains in native world/runtime/live owners

recovery-routing evidence
    may be partitioned/distributed
    must be typed, sparse, coherent and bounded
    must not own copied state, due order or chronology

active execution roots
    non-settled Commands (as needed)
    active Procedures independently
    conditional pending Interaction/IntentPlan at promised durable boundary

active temporal source membership
    otherwise-unreachable armed owner refs
    not Agenda order/state

transitive descendants
    Resolution
    Continuation
    pending children
    receipts/events/dependencies
    need not be redundant roots when reachable

known singleton
    campaign allocator

live
    remains routed through scene/live native pointers and local partitions
```

---

# 17. Single versus distributed projection decision

The challenge changes the status of this question.

A **single globally hot projection** is now rejected as a required design because it would create unnecessary shared-write contention.

A **distributed/partitionable logical routing model** is required.

However Step 5.2 still does not need to choose the exact files/fields because several implementations satisfy the same architecture:

- active-only directories whose membership encodes the projection;
- typed per-kind indexes;
- per-scene/per-procedure recovery routing sections;
- one cold campaign-level index for rare global roots plus local live partitions;
- a combination chosen by 5.7/5.8.

The semantic decision is therefore no longer “single vs distributed”. It is:

> **Recovery routing must be partitionable by existing writable/semantic scope and must not impose a new campaign-global hot serialization point.**

This follows directly from accepted multiplayer/ownership constraints and does not require a new product trade-off decision.

---

# 18. What would change this recommendation

A first-class closure record or mandatory singleton projection would become justified only if later evidence proves that:

- native source compatibility cannot be validated without one independent composition identity;
- crash-consistent root membership cannot be expressed through native transaction scopes;
- support/checkpoint/handoff requires durable closure identity across revisions independent of any source revision;
- distributed routing makes correctness untestable or requires unbounded discovery;
- live/campaign recovery requires one atomic cross-domain transaction that the current branch topology cannot provide.

None of those conditions is currently established.

---

# 19. Challenge verdict

The core research recommendation survives, with four important refinements:

1. **No globally hot singleton root registry is required or preferred.**
2. Recovery-routing projections are **partitionable trusted indexes**, not semantic authorities.
3. “Durable recovery basis” means a **compatible native source set**, not one scalar frontier/cut ID.
4. Future RNG continuity is conditional on already committed/reserved randomness; Step 5.2 does not mandate a global deterministic RNG stream.

No material owner/product trade-off remains unresolved after this challenge.

Therefore the next step is a Decision Brief that can recommend canonical semantics without asking the human architect to choose among raw representation options.
