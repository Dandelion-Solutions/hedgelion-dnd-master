# Step 5.2 — Resumable Runtime Closure — Research & Architecture Draft

Status: **RESEARCH DRAFT — PRE-CHALLENGE**

Date: 2026-08-20

Classification: **Architectural**

Framing authority:

- `2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-task-brief.md`

Prerequisites:

- Step 5.0 final contamination audit;
- Step 5.1 canonical B-NARROW frontier model;
- Step 3 canonical execution boundary;
- accepted Step-2 temporal/resource/effect ownership;
- Step 4 truth/knowledge/disclosure/Story ownership.

This draft intentionally separates verified repository facts, inherited constraints, inferences, recommendations and unresolved questions. It does not yet constitute a candidate specification.

---

# 1. Executive finding

The repository evidence supports a **closure-over-native-owners** model, but the current shipped persistence layout does not yet provide enough bounded discovery to reconstruct that closure after total process/chat/model-memory loss.

The strongest current formulation is:

> **Resumable Runtime Closure is a correctness property of one durable recovery basis plus all gameplay-significant native owners and irreducible recovery evidence reachable from a bounded typed root set. It is not itself current-state authority.**

The primary missing architectural capability is **bounded active-root membership/discovery**, not another copy of Procedure/Resolution/Continuation/world state.

Step 3 already defines most irreducible in-flight execution payload semantics. Step 2 already places temporal obligations on their native owners. Step 5.1 already prevents a universal frontier object. What remains is to guarantee that a cold runtime can enumerate the relevant native owners without:

- scanning all campaign files/history;
- trusting prior chat memory;
- treating checkpoint as a mutable snapshot;
- serializing derived Agenda/DAG/cache state;
- reintroducing a generic pending-work owner.

Current confidence in this high-level finding: **HIGH**.

The main open architecture question is narrower:

> Should bounded root membership be expressed as one lightweight non-authoritative recovery-routing projection, or as several distributed native indexes/pointers whose union forms the recovery root set?

This is a representation/component-boundary question, not a current-state authority question. The analytical challenge must determine whether the distinction is material enough to require owner decision in Step 5.2 or can be deferred to Step 5.7.

---

# 2. Evidence map

## 2.1 Step 3 — portable execution semantics already exist

Verified:

- `runtime.command` is the accepted idempotent root execution request and mandatory-descendant closure owner.
- `runtime.resolution` owns exactly one Activity invocation and its execution state/cursor.
- `runtime.procedure` is independently addressable and solely owns procedure-local ResourceState.
- `runtime.continuation` owns one portable suspended Resolution generation.
- committed ExecutionSegments carry immutable/event/receipt/follow-up evidence but are not independent runtime owners.
- mandatory post-commit child work must be materialized atomically enough to prevent an Event -> lost-child crash window.
- Continuation preserves fixed historical inputs/safe recompute state and explicitly excludes Procedure-state copies, MechanicalContext, Temporal Agenda, condition indexes, DAG caches and trusted prospective deltas.

Current DEV machine schemas substantiate these contracts:

```text
runtime-command-state.schema.json
runtime-resolution-state.schema.json
runtime-procedure-state.schema.json
runtime-continuation-state.schema.json
execution-segment.schema.json
pending-child-invocation.schema.json
resolution-receipt.schema.json
```

Important existing Continuation state includes:

```text
generation
root_command_id
resolution_id
catalog_context_fingerprint
procedure_id?
safe_recompute_phase
invocation_facts
fixed_rng_results
prior_step_exports
committed_receipt_refs
dependency_frontier_refs
expected_child_resolution_ids
future_rng_frontier
pending_response?
unconsumed_advancement?
```

Research conclusion:

**Step 5.2 does not need to invent a second “execution snapshot”.** If a suspended execution is durably promised, its existing native Command/Resolution/Procedure/Continuation chain is the authoritative operational state that must survive.

---

## 2.2 Step 2 — temporal obligations already live on native owners

Verified examples:

- active `world.effect` owns its intrinsic lifetime TemporalBinding;
- active `world.effect.scheduled_trigger_state` owns trigger-local next-due TemporalBindings;
- terminal Effects cannot retain armed scheduled trigger state;
- actor/asset resources use owner current state;
- Procedure resources use Procedure-owned spent state;
- delayed resource recovery is encoded in the applicable resource/owner contract;
- no `runtime.scheduled_job` or `world.scheduled_job` class exists.

TemporalBinding is concrete and owner-local:

```text
temporal.metric_deadline
    context_id
    anchor_value
    deadline_value
    unit_id

temporal.procedure_boundary
    boundary_id
    procedure_id
    anchor_id
    subject_id?
    offset?

temporal.semantic_boundary
    boundary_id
    anchor_id
    subject_id?
    scope_id?
```

Research conclusion:

**Temporal Agenda remains reconstructible derived state only if every owner carrying a still-active temporal obligation is itself boundedly discoverable.**

Therefore Step 5.2’s temporal problem is primarily owner enumeration/reachability, not Agenda serialization.

---

## 2.3 Current GAME persistence contracts

Verified:

- campaign storage is separate from the runtime package;
- chat context and extracted runtime cache are temporary working state;
- HOT/SOFT current truth may be ahead of durable campaign publication;
- loss of unpublished HOT/SOFT after process/context destruction is not reconstructible and must not be invented;
- explicit save means materialize all established cross-session campaign state into normal authoritative representations;
- PERSISTENCE owns transport, not semantic ownership;
- checkpoints are sparse recovery descriptors/evidence, not snapshots/current-state owners;
- `MANIFEST.last_checkpoint_id` is the sole latest-checkpoint pointer;
- live scene pointers route scene-owned operational truth to live branches;
- `CANON_SUSPECT` already exists for missing/incompatible required references.

Current branch-root campaign template contains:

```text
MANIFEST.yaml
STATE/
INDEX/
WORLD/
LOG/
CHECKPOINTS/
SESSIONS/
...
```

There is no shipped `RUNTIME/` or equivalent root for the Step-3 runtime owners.

`STATE/CURRENT.yaml` currently roots only:

```text
campaign_id
world_time
active_scenes
active_threads
```

`runtime.session` persistent schema currently roots only coordination fields such as:

```text
session_id
player_id
pc_id
scene_id
base_head_sha
last_published_head_sha
```

Checkpoint currently roots:

```text
current_state_path
active_pc_ids
active_thread_ids
active_scene_ids
```

No current GAME schema/template provides bounded durable discovery of active:

```text
runtime.command
runtime.procedure
runtime.resolution
runtime.continuation
pending clarification Interaction/IntentPlan
```

Research conclusion:

**The accepted runtime owners have semantics and stable IDs but not yet a complete shipped repository placement/enumeration contract.** Step 5.0 explicitly deferred this issue to 5.2/5.7.

---

## 2.4 Multiplayer/live evidence

Verified:

- multiple independent chats/sessions may concurrently operate against one campaign;
- separate scenes may remain independent;
- `runtime.session` is therefore not a campaign-global operational owner;
- live scene state is authoritative for the mutable routed scene scope while an epoch is active;
- durable scene state contains the live epoch pointer needed to discover the live branch/state;
- missing/invalid pointed live state raises `CANON_SUSPECT`;
- an unpointed live branch is not authoritative.

Research conclusion:

The live model already demonstrates the correct pattern for recovery routing:

```text
durable native owner/pointer
    -> authoritative scoped operational state
```

The pointer is recovery/routing evidence; it does not copy live state or become the live owner.

A Step-5.2 active-root mechanism should preserve this pattern rather than merge campaign and live authorities into one snapshot.

---

## 2.5 Interaction/Intent evidence

Step 3 canonically defines:

- `runtime.interaction` as one accepted external exchange/invocation identity and raw-message linkage;
- `runtime.intent_plan` as all material interpreted clauses;
- clarification/narrative-only/unsupported clauses remain represented even without a RuntimeCommand.

Current machine realization includes `runtime-intent-plan-state.schema.json` and `intent-clause.schema.json`, including:

```text
mapping_outcome = clarification_required
execution_state = intent.pending
```

but no current DEV machine schema for `runtime.interaction` or `runtime.message` was found in the current schema tree.

Research conclusion:

For a **material unresolved player declaration/clarification** that is promised to survive a durability boundary, Interaction/IntentPlan are the natural existing owners. A new generic “pending player prompt” owner is not yet justified.

Exact prose need not be durable if the already interpreted semantic ambiguity/resume requirement is durably represented. If exact wording is needed because interpretation has not completed, retained `runtime.message`/Interaction evidence would be required; its machine realization is deferred implementation debt rather than proof of a new Step-5.2 class.

A generic Master prompt such as “what do you do?” is not itself a gameplay obligation. The current scene/actionable state is sufficient to re-establish control after recovery. Exact previous wording is presentation/history, not semantic authority.

---

# 3. Durable recovery basis versus current HOT state

Step 5.2 must not erase the existing sparse-durability policy.

Canonical conceptual distinction:

```text
CURRENT HOT TRUTH
    = native owners in current runtime/live state
      + unpublished accepted mutations

LAST DURABLE RECOVERY BASIS
    = latest set of successfully durable native-domain revisions
      that the applicable durability protocol promises after total context loss

RESUMABLE RUNTIME CLOSURE AT BASIS B
    = every gameplay-significant native owner/evidence required to continue
      from B without semantic invention/loss/replay
```

Important consequence:

If the player performs ordinary SOFT actions after durable basis B and the entire process/chat working set is destroyed before any applicable boundary, recovery truthfully returns to B. Those SOFT actions were current canon while memory survived but were outside the cold-recovery guarantee.

That is not a Step-5.2 defect by itself.

A defect exists when the system claims boundary B' is durable/recoverable while gameplay-significant state that is semantically part of B' cannot be reconstructed from B'.

---

# 4. Classification ledger

## 4.1 Campaign/world current state

### Ordinary world records

Classification: **AUTHORITATIVE STATE**.

Examples:

- actor HP/resources/location;
- asset ownership/status;
- current scene state;
- effect/condition lifecycle;
- active mission/contract/thread state;
- truth/knowledge/disclosure after their machine realization.

Cold-recovery rule:

At a durable recovery basis, any current record materially required by active execution/recovery must be retrievable by normal stable references/indexes.

Do not copy these fields into checkpoint/Continuation/root descriptors.

---

## 4.2 RuntimeCommand

Classification: **AUTHORITATIVE OPERATIONAL STATE** while non-settled.

Why:

- owns root accepted execution identity/input fingerprint;
- owns mandatory descendant closure disposition;
- owns pending child descriptors that may remain after a segment committed.

Cold-recovery requirement:

Every non-settled durable Command must be boundedly discoverable or reachable from another admitted active root.

Settled Commands may become historical/audit material and need not remain in the active recovery root set merely because records are retained.

---

## 4.3 Resolution

Classification: **AUTHORITATIVE OPERATIONAL STATE** while active/suspended/blocked and **recoverable historical evidence** after terminality as retention policy requires.

Required cold state as applicable:

- status/cursor/safe recompute;
- activity/catalog binding;
- fixed RNG already consumed;
- prior exports;
- child refs;
- causal invocation key;
- Continuation ref;
- root/procedure refs.

Do not reconstruct an active Resolution from SemanticEvent prose/history if the typed owner should have survived.

---

## 4.4 Procedure

Classification: **AUTHORITATIVE OPERATIONAL STATE**.

Procedure can outlive any one Command/Resolution and therefore cannot be discovered only by looking at one active Command.

At minimum a durable active Procedure must remain a root or be reachable from another durable active root that is guaranteed to exist throughout the Procedure lifetime.

Current evidence does not prove that every Procedure always has an open Command. Combat between player invocations is the obvious counterexample.

Therefore active Procedure membership requires independent bounded discovery.

---

## 4.5 Continuation

Classification: **AUTHORITATIVE PORTABLE SUSPENSION STATE** for one generation.

Not a root by itself when its Resolution durably references it, provided Resolution discovery is guaranteed.

Its payload already contains most irreducible suspension semantics.

No separate recovery copy is needed.

---

## 4.6 Pending mandatory child invocation

Classification: **IRREDUCIBLE EXECUTION EVIDENCE embedded in RuntimeCommand/committed segment** until materialized child execution closes it.

Why irreducible:

- a historical Event alone cannot safely rediscover whether/which binding had been selected;
- later current-state scanning is explicitly forbidden from retroactively deciding a firing;
- crash after Event commit must not lose child obligation identity.

Cold recovery must preserve the owner containing this descriptor and its stable firing key/root/procedure/activity/trigger linkage.

Do not create a generic pending-job table merely for these descriptors.

---

## 4.7 Fixed RNG already generated

Classification: **AUTHORITATIVE EXECUTION INPUT / IRREDUCIBLE RECOVERY STATE** when an active execution has accepted or consumed the raw value but not yet completely settled all dependent semantics.

The value belongs on Resolution/Continuation/committed execution evidence according to Step 3.

`runtime.resolution_trace` alone is insufficient as the authoritative resume source because GAME currently treats traces as compactable operational evidence.

Once all mechanically material consequences are durably committed and no retry/resume/audit contract requires the raw value, ordinary retention policy may compact trace detail while durable semantic/mechanical evidence preserves required causality.

---

## 4.8 Future RNG state/frontier

Classification: **CONDITIONAL IRREDUCIBLE RECOVERY EVIDENCE** only when the runtime has already established a future RNG stream/substream reservation whose identity affects deterministic resume.

Current GAME randomness uses actual RNG but does not require all not-yet-drawn future rolls to be reproducible across restart.

Therefore Step 5.2 must not invent a campaign-global RNG stream merely for recovery symmetry.

Step 5.3 owns exact RNG continuity rules. Its constraint is:

> already-fixed or already-reserved randomness that would otherwise change accepted execution semantics must survive; genuinely future independent random experiments need not be precommitted merely because restart is possible.

---

## 4.9 Pending Choice / Reaction

Classification: **AUTHORITATIVE SUSPENSION INPUT CONTRACT** embedded in Continuation.

Must survive when the associated Continuation is part of the durable basis:

```text
kind
offer_id
responder_id
bounded candidate/option IDs
continuation generation
single-consume/idempotency relation
```

Recovery may not regenerate a materially different option/reaction set from current ambient state after the offer was already fixed.

---

## 4.10 Invocation facts / prior exports / accepted catalog context

Classification: **IRREDUCIBLE EXECUTION INPUT/EVIDENCE** while the execution remains resumable or retryable.

Reason:

Rebinding under later ambient catalog/state can change meaning and violate idempotency. Step 3 explicitly requires retry lookup against accepted stored context first.

---

## 4.11 MechanicalEvent / receipt refs

Classification: **COMMITTED EVIDENCE**, not current state authority.

Required while active execution depends on them for:

- idempotency;
- already-committed segment frontier;
- typed prior exports;
- mandatory descendant linkage;
- no-double replay.

The referenced current state remains owned by the world/runtime owners.

---

## 4.12 ResolutionTrace

Classification: mixed:

- **REBUILDABLE / RETAINED DIAGNOSTIC EVIDENCE** for many calculations;
- **must not be sole owner** of fixed RNG or accepted execution inputs needed for resume;
- may be dropped after safe compaction when no audit/recovery consumer remains.

A durable recovery closure must not depend on verbose trace retention when compact typed owner fields already carry the irreducible state.

---

## 4.13 TemporalBindings and scheduled trigger state

Classification: **AUTHORITATIVE OWNER-LOCAL STATE**.

They survive with their native Effect/Resource/LifeState/Procedure owners.

Temporal Agenda classification: **REBUILDABLE DERIVED STATE**.

But this proof has a precondition:

> every still-armed temporal owner must be enumerable from bounded durable routing/index evidence.

Current template does not have a general Effect/temporal-owner index. Therefore the semantic ownership is correct but the cold-rebuild enumeration path remains incomplete.

Step 5.2 must require bounded temporal-owner discovery; Step 5.3 decides Agenda rebuild/due processing and no-lost/no-double firing.

---

## 4.14 Derived mechanical caches

Classification: **REBUILDABLE DERIVED STATE**.

Includes:

- MechanicalContext;
- effect/condition aggregation indexes;
- dependency DAG cache;
- derived AC/modifiers/speeds/etc.;
- loaded entity cache;
- repository listing/search cache;
- Context Assembler bundles/source manifests after their immediate trace need;
- Story editing/rendering buffers.

Cold recovery recomputes from surviving owners and accepted catalog context.

A cache disagreement with its owner must be resolved in favor of the owner; serialized cache bytes never win because they are “newer”.

---

## 4.15 Prospective/uncommitted ExecutionSegment state

Classification: normally **TRULY EPHEMERAL / VOLATILE CURRENT COMPUTATION** until segment commit.

If a process dies before the atomic segment commit, prospective deltas/RNG that were not accepted as fixed continuity state are discarded and the segment is recomputed from the last committed execution owner state.

If a random value was already fixed before suspension/commit under Step-3 continuity semantics, that fixed value is no longer merely prospective and must be represented by the owner before claiming a durable suspension point.

---

## 4.16 Dirty HOT/SOFT working set

Classification: **VOLATILE CURRENT STATE AHEAD OF DURABLE BASIS** until an applicable durability boundary successfully publishes it.

At a boundary where it becomes part of the promised durable basis, its owning records—not a generic dirty snapshot—must be durably materialized.

Dirty-set bookkeeping itself remains operational representation deferred to 5.5.

---

## 4.17 Publication preparation snapshot

Classification: **EPHEMERAL TRANSPORT/RETRY STATE** for Step 5.2 purposes unless Step 5.6 later proves an independent crash-retry lifecycle requirement.

It does not become gameplay authority and is not required to reconstruct the last successfully durable basis.

---

## 4.18 Campaign allocator

Classification: **AUTHORITATIVE OPERATIONAL/IDENTITY STATE** with known singleton identity `campaign-allocator`.

Because its identity is globally known, allocator membership does not require an active-root index.

Its durable counter/conflict state must be recoverable whenever campaign-scoped identities already published or durably referenced depend on it.

Local/session-scoped unpublished reservations may disappear with the volatile working set unless a durable recovery owner already references them.

Critical promotion rule:

> No durably recoverable record may depend on a session-local/unpublished entity identity that will disappear on cold recovery.

At a durability boundary, such a dependency must be promoted/rekeyed/materialized coherently or the publication is invalid.

This follows existing durable-reference/promotion closure; Step 5.6 owns publication mechanics.

---

## 4.19 Runtime session

Classification: **COORDINATION / RECOVERY METADATA**, not campaign-wide gameplay authority.

A session can help identify a returning human/player/scene and may carry session-local recovery routing metadata if later design admits it.

It cannot be the sole global closure root because:

- multiplayer has several sessions;
- active Procedure/state may outlive one session;
- live scene authority is scene/epoch scoped;
- an ended/stale session cannot erase campaign-operational work owned elsewhere.

---

## 4.20 Interaction / IntentPlan pending clarification

Classification when materially unresolved and promised at a durable basis:

- Interaction: **AUTHORITATIVE OPERATIONAL INPUT BOUNDARY**;
- IntentPlan/clause: **AUTHORITATIVE INTERPRETED PENDING INTENT STATE**.

A pending clarification can be recovered without a new class if its Interaction/IntentPlan state is durably retained and boundedly rooted.

If the unresolved material is merely an open narrative opportunity with no accepted player declaration, scene/world state is enough; exact Master wording is EPHEMERAL presentation.

---

## 4.21 Maintenance continuation frame

Classification in current runtime: **EPHEMERAL CURRENT-CHAT RECOVERY AID**.

It exists to bridge controlled maintenance while the same chat/context survives.

It is not sufficient for cold recovery after total context loss. If the underlying unresolved gameplay point is promised to survive cold recovery, the actual semantic owners described above must be durable.

Step 5.4 may decide when controlled handoff must force publication of those owners before destroying the old context.

---

## 4.22 Story / transcript projections

Story: **DURABLE NONCANONICAL PROJECTION**, not a canonical operational recovery prerequisite.

A missing/lagging Story layer must not prevent gameplay recovery when canonical/current operational owners are intact.

Transcript exactness is separately owned by 5.11 and cannot be required for deterministic mechanics unless a supposedly semantic input was never materialized into its actual owner—in which case that is a recovery defect, not a reason to make transcript authority.

---

# 5. Bounded recovery-root graph

The minimum conceptual cold-start graph currently implied by accepted ownership is:

```text
selected campaign branch / durable campaign HEAD
    |
    +-> MANIFEST
    |     -> runtime package identity
    |     -> storage roots
    |     -> latest checkpoint pointer (optional recovery descriptor)
    |
    +-> STATE/CURRENT
    |     -> active scenes
    |     -> active threads
    |     -> global chronology evidence
    |
    +-> active scene records
    |     -> world/entity refs
    |     -> live_epoch pointer when applicable
    |           -> live branch + LIVE_STATE
    |
    +-> [MISSING/DEFERRED BOUNDED OPERATIONAL ROOT MEMBERSHIP]
    |     -> non-settled RuntimeCommands
    |     -> active Procedures
    |     -> pending Interaction/IntentPlan where materially unresolved
    |     -> from those, Resolutions/Continuations/children/receipts
    |
    +-> [MISSING/DEFERRED BOUNDED TEMPORAL-OWNER MEMBERSHIP]
    |     -> Effects/Resources/LifeState/other owners with armed obligations
    |     -> rebuild Temporal Agenda
    |
    +-> campaign-allocator (known singleton)
```

The bracketed lines are the central Step-5.2 gaps.

They are **membership/routing projections**, not new state owners.

---

# 6. Why the obvious existing roots are insufficient by themselves

## 6.1 `runtime.session` as sole root — rejected

Failure:

- several sessions can exist concurrently;
- Procedure may outlive one session;
- session closure/staleness cannot imply gameplay work is settled;
- a campaign-wide temporal obligation may not belong to any currently active human session.

Useful role:

session may point into the root set for returning-user convenience, but cannot define the root set.

---

## 6.2 `STATE/CURRENT` containing copied runtime state — rejected

Failure:

- duplicates Command/Procedure/Resolution/Continuation authority;
- recreates the generic tactical/pending bucket Step 5.0 retired;
- turns a compact routing record into an execution snapshot.

Possible role:

`CURRENT` could eventually contain **typed references or a pointer to routing projections** if 5.7 selects that representation, just as it already points to active scenes. References are not copies.

---

## 6.3 latest checkpoint as sole root — rejected

Failure:

- checkpoints are intentionally sparse;
- ordinary durable publication may occur without a checkpoint;
- latest checkpoint can legitimately be older than campaign HEAD;
- current active operational owners after that checkpoint must not disappear merely because no new checkpoint was created.

Possible role:

checkpoint may capture/validate a recovery-root set for a selected historical recovery cut in 5.7, but current active-root membership must have a durable source independent of checkpoint cadence.

---

## 6.4 event-log scan as recovery enumeration — rejected

Failure:

- Event/LOG is history/evidence, not current owner authority;
- determining current open work from historical events risks replay/closure ambiguity;
- broad history scans violate bounded recovery/performance goals;
- Step 3 explicitly materializes pending child identity so historical rediscovery is unnecessary.

---

## 6.5 filesystem/directory scan of all runtime/world records — insufficient as canonical design

A bounded physical directory containing *only active owners* could theoretically act as a routing structure, but then file placement/movement itself becomes the active-membership projection and acquires lifecycle/atomicity requirements.

That is not meaningfully “no descriptor”; it is one representation of a descriptor/index and belongs in later storage/protocol design.

Scanning an ever-growing history directory and inspecting every record status is explicitly not bounded by active gameplay size and is rejected.

---

# 7. Root-membership requirement

Step 5.2 should establish the following semantic requirement independent of final wire/file shape:

> At every promised durable recovery basis, all gameplay-significant **currently active operational roots** and all otherwise-unreachable **armed temporal owners** must be discoverable from a bounded typed recovery-routing projection or an equivalent bounded native index structure published coherently with the owner membership change.

Properties:

1. **Non-authoritative:** membership says “load/check this owner”; it does not copy or override owner state.
2. **Typed:** a root identifies semantic kind/scope; no untyped `pending[]` bag.
3. **Sparse:** only active/recovery-relevant owners are listed.
4. **Closure-oriented:** descendants already reachable from roots need not be redundantly rooted.
5. **Domain-preserving:** campaign/live/runtime/chronology markers remain native; root membership does not compare them.
6. **Coherent:** a durable root pointer may not reference a missing unpublished owner.
7. **Retirement-aware:** owner terminality/removal must eventually remove active membership in the same semantic durability closure.
8. **Recoverability-only:** it does not decide fictional chronology, scheduling order, publication priority or gameplay authority.
9. **Bounded:** recovery cost scales with active gameplay obligations/owners, not campaign age.

---

# 8. Minimal root classes

The research currently supports only these logically independent active-root classes.

## 8.1 Open root execution chains

Root candidate:

```text
runtime.command where disposition != SETTLED
```

From Command discover:

- root Resolution;
- pending child descriptors;
- child Resolutions;
- Continuations;
- receipt/event refs;
- Procedure refs where present.

However Procedures cannot be rooted only transitively from Commands because they may remain active between Commands.

---

## 8.2 Active Procedures

Root candidate:

```text
runtime.procedure still active under procedure lifecycle semantics
```

Step 3 machine state does not yet define explicit Procedure lifecycle/status. This is an implementation/schema gap that later implementation must address or derive from typed procedure semantics. Step 5.2 need only require unambiguous active/terminal membership for recovery.

Do not infer Procedure lifetime solely from world.encounter status.

---

## 8.3 Material pending external-input interactions without a Command

Root candidate only when an accepted Interaction/IntentPlan remains semantically unresolved and the durable recovery promise includes resuming that exact declaration/clarification.

Examples:

- ambiguous target clarification after a player declaration;
- accepted compound IntentPlan with earlier clauses committed and a later clause awaiting clarification.

Not a root:

- generic open-ended “what do you do?” presentation;
- unaccepted generated prose;
- optional suggestion list.

This root class may disappear if later machine design proves every materially unresolved durable player input can be represented by another existing owner. Do not create a new class.

---

## 8.4 Armed temporal owners not guaranteed reachable from the above/world active scene roots

Examples:

- off-screen active Effect with a metric scheduled trigger;
- delayed recovery on an owner no longer loaded in the active scene;
- another owner-local timer/process that remains mechanically due-capable.

These need bounded membership for Agenda rebuild if ordinary world indexes do not already provide an efficient typed active-owner route.

This membership is **not Temporal Agenda ordering**. It is only the set of source owners from which Agenda is derived.

---

# 9. Temporal Agenda rebuild proof

Agenda can remain disposable if recovery can execute:

```text
load armed-temporal-owner root/index entries
    -> load each native owner
    -> validate owner is still active and binding is well-formeded
    -> read current chronology/context evidence
    -> derive due ordering/index entries
```

No agenda-local datum is currently proven irreducible.

What must survive instead:

- owner identity;
- owner lifecycle/current state;
- TemporalBinding;
- metric anchor/deadline/context or semantic/procedure boundary anchor;
- stable firing identity if a due occurrence was already selected/committed into pending work;
- relevant chronology/procedure context owner.

Once a due firing becomes selected/committed, it crosses from “Agenda-derived candidate” into Step-3 pending child/Resolution semantics and must no longer depend on reconstructing the Agenda decision.

Step 5.3 owns that transition/no-double behavior.

---

# 10. Live-scope cold-recovery constraints

Step 5.2 does not decide live placement, but imposes these constraints:

1. A campaign scene’s durable live pointer remains the bounded root for live-owned world/scene state.
2. Any active runtime owner whose authoritative state is stored/routed in a live scope must be discoverable from that live scope’s durable routing chain.
3. Campaign recovery must not copy live-owned mutable truth back into campaign state merely to create one recovery snapshot.
4. A missing pointed live branch/state is integrity suspicion, not permission to fall back silently to stale campaign base state.
5. Independent live epochs remain independent domain-native roots; no total ordering is implied by recovery enumeration.
6. A closed-but-unabsorbed epoch is a valid non-playable recovery condition: the runtime must resume/complete the appropriate bounded recovery/compaction protocol rather than replay gameplay from the campaign base.

Step 5.8 owns exact branch/CAS/adoption/compaction mechanics.

---

# 11. Identity and promotion closure

Durable recoverability requires a stronger statement of the existing publication-closure rule:

> Every durable recovery root and every owner reachable from it must have a transitive dependency closure that contains no reference to an identity/state whose lifetime is shorter than the promised recovery basis unless that reference is explicitly optional/rebuildable.

Consequences:

- session-local local entity IDs may exist in volatile play;
- once a durably recoverable Resolution/Continuation/Effect/etc. refers to such an entity as a required dependency, the entity must be promoted/rekeyed/materialized coherently before the recovery basis is acknowledged;
- campaign allocator state must move coherently with published campaign-scoped IDs;
- a durable root may not point to a runtime owner that exists only in process RAM;
- a live-epoch provisional ID may remain valid inside the durable live epoch because the live epoch itself owns that identity’s bounded lifetime, but it cannot escape that epoch before promotion/compaction.

Exact publication/rekey transaction mechanics remain 5.6/5.8.

---

# 12. Semantic resume point outside active mechanics

Research distinguishes four cases.

## Case A — no unresolved player declaration

Example: scene ended with ordinary “what do you do?” handoff.

Required recovery:

- current scene/world/knowledge/disclosure state;
- no exact prompt text.

The fresh runtime can regenerate a semantically equivalent actionable handoff.

Classification: presentation EPHEMERAL.

## Case B — player declaration accepted and deterministically resolved

Current state/Event/Command closure contains the result.

No separate prompt/declaration owner is needed after settlement except ordinary history/audit retention.

## Case C — mechanical choice/reaction is pending

Continuation owns the typed bounded offer.

No separate interaction prompt owner required for the choice semantics.

## Case D — player declaration accepted but clarification remains before Command acceptance

Interaction + IntentPlan/IntentClause are the natural existing operational owners.

At a promised durable boundary, enough interpreted semantic state must survive to ask the same material clarification without guessing the original intent.

This may require eventual machine fields beyond the current generic `details`, but it does not justify a new fundamental owner.

Research conclusion:

**No new “semantic resume point” class is currently justified.**

---

# 13. Recovery integrity taxonomy

Step 5.2 should distinguish conceptually:

## 13.1 Expected rollback to last durable basis

Condition:

- volatile HOT/SOFT state was never included in a successful promised durability boundary;
- process/context is destroyed.

Outcome:

- resume from prior durable basis;
- do not classify missing unpublished bytes as canon corruption;
- may inform the user only if product/session policy requires it.

## 13.2 Recovery dependency missing/stale but refreshable

Examples:

- stale session pointer;
- cached old campaign/live revision.

Outcome:

- refresh/rebind through domain-native routing;
- no canon corruption if authoritative target exists and is coherent.

## 13.3 Required durable recovery root/target missing or incompatible

Examples:

- root projection says active Procedure P, but P record is missing;
- Continuation references missing required Procedure/current owner;
- scene points to missing authoritative live branch;
- root owner depends on vanished local ID.

Outcome:

- scoped `CANON_SUSPECT` / recovery-blocked condition;
- targeted validation/repair;
- do not guess or silently drop the root.

Exact runtime failure code/status belongs to 5.7 implementation/protocol design.

## 13.4 Derived cache missing

Outcome:

- rebuild silently;
- never mark canon corrupt merely because Agenda/DAG/cache is absent.

## 13.5 Derived cache conflicts with owner

Outcome:

- discard/rebuild cache;
- owner wins;
- if the owner itself is incoherent, raise integrity suspicion for owner scope.

---

# 14. Mandatory scenario analysis

## 14.1 Clean turn boundary; no in-flight mechanics

Authority:
world/current owners.

Required roots:
active scene/thread/world refs; armed temporal owners if any.

Runtime execution roots:
none.

Rebuild:
context/cache/Agenda.

---

## 14.2 HOT/SOFT ahead of durable publication; abrupt crash

Authority before crash:
HOT working set.

Promised cold basis:
older durable basis.

Result:
unpublished delta truthfully lost; resume older basis; no invention.

Not a 5.2 defect unless a durability policy had already promised those changes.

---

## 14.3 Controlled handoff while HOT/SOFT exists

5.2 constraint:
if 5.4 decides controlled handoff must preserve current point, all owning state + required roots must become durable before old context is destroyed.

5.2 does not decide whether/when that force occurs.

---

## 14.4 Resolution awaiting player choice/reaction

Required:
Command + Resolution + Continuation generation + pending response + Procedure if referenced + fixed RNG/exports/receipts/dependencies.

Agenda/cache:
rebuild/irrelevant.

---

## 14.5 Procedure with spent ResourceState between commands

Required:
Procedure remains independently rooted even if no open Command exists.

This defeats “non-settled Commands are the only runtime roots”.

---

## 14.6 Segment committed; mandatory child materialized but not run

Required:
Command remains open and descriptor/firing key survives.

Recovery starts from committed state and executes/resumes child exactly once under later 5.3 logic.

---

## 14.7 Event committed but mandatory child descriptor absent

If the event semantically required mandatory child work, this violates Step-3 atomicity and is a persistence/integrity defect.

Recovery must not rediscover historical firing by scanning current bindings and pretending equivalence.

---

## 14.8 Fixed RNG drawn before suspension

Fixed value survives in Resolution/Continuation.

Fresh roll is forbidden.

---

## 14.9 Future RNG not yet drawn

No general need to preserve a deterministic global stream merely for restart.

If a substream/future draw was already reserved as accepted execution input, preserve its frontier/state under 5.3.

---

## 14.10 Active scheduled Effect; Agenda absent

Load Effect from bounded temporal-owner route, rebuild Agenda from its binding/context.

No defect merely because Agenda bytes vanished.

---

## 14.11 Two independent live epochs

Campaign scene pointers independently route to each live branch.

Recovery composes a read view as required but does not compare/order the live revisions merely because both are roots.

---

## 14.12 Live epoch durable but not campaign-absorbed

Resume live-owned truth from live branch.

Do not roll back to campaign base just because campaign HEAD is older for that scope.

---

## 14.13 Stale session points older revision

Session is coordination evidence; refresh against campaign/live routing.

Stale session never overrides current native authority.

---

## 14.14 Campaign allocator referenced by durable owners

Fetch known singleton allocator; validate campaign-scoped IDs.

If owner references a vanished session-local ID, recovery closure was invalidly published.

---

## 14.15 Player declaration pending clarification

Persist/root Interaction+IntentPlan only if the declaration is part of promised durable resume.

Do not require full chat transcript.

---

## 14.16 Maintenance restart during unresolved mechanics

Ephemeral maintenance frame may aid same-context switch, but cold-correctness comes from durable native owners.

If maintenance destroys context, 5.4 must ensure applicable durability boundary first if current point is promised.

---

## 14.17 Checkpoint older than current campaign HEAD

Current recovery is not forced backward to checkpoint.

Checkpoint remains selectable historical recovery evidence. Current active-root membership comes from current durable state/routing.

---

## 14.18 Story missing or lagging

Gameplay operational recovery proceeds.

Story catch-up is 5.10.

---

## 14.19 Serialized cache disagrees with owner

Discard cache; rebuild.

Cache never resolves conflict in its own favor.

---

## 14.20 Cold recovery requires scanning every Effect/Command/history record

Design fails bounded-recovery quality gate.

Need compact typed root/index membership.

---

# 15. Simplest viable architecture

The minimum architecture consistent with evidence is:

```text
Resumable Runtime Closure
    = property, not authority

At durable basis B:

1. native current-state owners are durable in their own domains;
2. active runtime owners retain their Step-3 typed state;
3. active live scopes remain routed by native scene/live pointers;
4. campaign allocator remains its known singleton owner;
5. all otherwise-unbounded active operational roots are represented in
   a compact typed recovery-routing membership projection;
6. all otherwise-unbounded armed temporal source owners are represented in
   a compact typed owner-routing/index projection;
7. descendants/references are followed transitively from roots;
8. derived Agenda/DAG/cache/context state is rebuilt;
9. missing required root/target is integrity/recovery failure;
10. checkpoint may describe/validate a selected recovery cut but does not own
    the state or determine current root membership merely by being latest.
```

This architecture requires **no new semantic state owner**.

It likely requires one or more **non-authoritative recovery projections/indexes** in later machine realization.

---

# 16. Credible representation alternatives

These are deliberately representation/component alternatives, not authority alternatives.

## Alternative A — distributed native routing/indexes

Example conceptually:

```text
CURRENT / scene / session native routing refs
+ runtime-kind active indexes
+ temporal-owner indexes
+ scene.live_epoch pointers
```

No single “closure descriptor” file.

Advantages:

- ownership/routing stays close to native domain;
- no apparently universal recovery object;
- updates can be scoped to changed domain.

Risks:

- more cross-file invariants;
- cold-start recovery must know and validate several root sources;
- easy for a new owner kind to forget enrollment in all required indexes;
- checkpoint 5.7 must compose a coherent set without accidentally inventing a universal frontier.

## Alternative B — lightweight typed recovery-root projection

One compact non-authoritative projection lists only active **root references**, grouped by semantic kind/scope. It does not copy owner payloads or domain revisions into one comparable scalar.

Conceptually:

```text
operational roots:
    open_command_refs[]
    active_procedure_refs[]
    pending_interaction_refs[]

temporal source roots/index refs:
    ...

live roots:
    normally remain scene-native pointers rather than copied here
```

This could eventually be embedded in CURRENT, represented as a dedicated routing/index file, or referenced by checkpoint depending 5.7.

Advantages:

- one bounded cold-start location for active operational roots;
- simpler completeness assertion at durability boundary;
- support/maintenance diagnostics straightforward;
- still no state duplication.

Risks:

- can look like a generic universal recovery owner unless semantics are tightly constrained;
- every root membership mutation joins the durable closure;
- may become a dumping ground if untyped future state is admitted.

## Alternative C — checkpoint-only closure manifest

Checkpoint lists all active roots.

Rejected as current-primary mechanism because checkpoint cadence is intentionally sparse and may lag ordinary durable current state.

Could still be used in 5.7 for historical/selectable checkpoint validation by recording the then-current root projection.

## Alternative D — first-class `runtime.recovery_closure` record

Rejected by current evidence.

No independent semantic lifecycle or writable authority has been demonstrated. The only proven need is routing/membership evidence attached to a durability basis.

A dedicated runtime record would add identity/lifecycle/GC/versioning complexity without a proven consumer that cannot use a projection/index.

---

# 17. Preliminary recommendation

Recommendation before challenge:

> **Adopt the closure-over-native-owners model and require a bounded typed active-root projection/index contract, while deferring its exact physical placement (single projection versus distributed indexes) to Step 5.7 unless the analytical challenge finds that this choice changes semantics, concurrency or failure recovery.**

In other words:

- 5.2 should canonicalize **what belongs in the closure and what may not**;
- 5.2 should canonicalize **bounded typed root discoverability**;
- 5.2 should reject a new `runtime.recovery_closure` authority/record;
- 5.2 should not prematurely choose `STATE/CURRENT.recovery_roots` versus `RUNTIME/ACTIVE_INDEX.yaml` versus several domain indexes;
- 5.7 should choose the physical checkpoint/recovery routing representation after 5.3–5.6 have supplied due-work, lifecycle, durability and crash-consistency constraints.

Confidence: **MEDIUM-HIGH**, pending challenge of whether root projection placement itself is a fundamental architectural decision that cannot safely wait until 5.7.

---

# 18. Strongest counterargument

The strongest objection is:

> Deferring the shape of root membership to 5.7 may make 5.2 too abstract. If bounded recovery is central, the system may need one explicit durable active-root registry now so later slices can reason concretely about membership updates, crash consistency, live ownership and checkpoint cuts.

This objection is serious because:

- membership updates must be coherent with owner creation/terminality;
- temporal owner enrollment has no existing complete index;
- multiplayer may update different scopes independently;
- a single global file could become a write-conflict hotspot;
- distributed indexes could complicate atomic closure assertions.

However those exact trade-offs depend heavily on:

- 5.3 due-work transitions;
- 5.5 durability classification;
- 5.6 transaction grouping;
- 5.8 live-scope write ownership.

Choosing a physical registry before those constraints are designed risks making 5.2 own later-slice protocol architecture.

Current response:

5.2 should establish the **logical projection contract and completeness invariant**, but leave physical partitioning and transaction placement open.

---

# 19. Current repository gaps / implementation debt exposed

These are findings, not implementation authorization.

1. No shipped repository placement/enumeration contract exists for accepted Step-3 runtime owners.
2. Current `SESSION`, `CURRENT` and checkpoint schemas do not root active Commands/Procedures/Continuations.
3. Current GAME schema set does not machine-realize the Step-3 runtime owners even though DEV schemas do.
4. Current persistent template has no general temporal-owner/Effect active index sufficient to prove bounded Agenda rebuild.
5. Procedure machine state lacks an explicit lifecycle/status field, yet recovery must distinguish active versus terminal Procedure membership somehow.
6. Interaction/message machine realization is incomplete relative to Step-3 accepted runtime classes; material pending clarification recovery needs eventual typed representation.
7. `SAVE_CONTRACT.md` does not yet explicitly include active runtime operational owners in its cross-session completeness checklist.
8. `RANDOMNESS.md` wording about in-memory trace could be misread as sufficient continuity, but Step-3 fixed RNG state must own mechanically material suspended values.
9. Checkpoint legacy field `valid_through_event_id` and wording “recovery via event frontier” remain 5.7 debt after 5.1 retirement of a global last-event cursor.
10. Maintenance commands correctly refer to required active recovery roots but cannot yet enumerate them from current GAME schemas.

These gaps are expected realization/design debt, not evidence that Steps 2–3 ownership is wrong.

---

# 20. Later-slice constraints

## Step 5.3

Must define:

- transition from owner-local due candidate to selected mandatory invocation;
- Agenda rebuild from bounded temporal-owner roots;
- no-lost/no-double due work;
- fixed/reserved RNG continuity.

May not make Agenda the temporal authority.

## Step 5.4

Must decide when controlled context/process destruction forces current closure to become durable before handoff.

May not rely on ephemeral maintenance frame as the only cold-recovery state.

## Step 5.5

Must make SOFT/HARD/SAVE semantics include complete owning closure at the boundary, not just world files.

## Step 5.6

Must publish root-membership changes coherently with newly reachable owners and dependency promotion.

A durable root may not point to a missing owner; removal from roots may not precede terminal owner state becoming durable when that would drop required work.

## Step 5.7

Owns physical recovery-root/checkpoint representation, hydration order, validation and historical checkpoint cuts.

Must preserve B-NARROW domain typing.

## Step 5.8

Must decide where runtime roots live when their authoritative scope is live-owned and how membership moves across compaction/rollover.

## Step 5.9

Must provide the chronology/context evidence needed to interpret recovered TemporalBindings without converting commit/root ordering into fictional chronology.

## Step 5.10–5.13

Must not make Story/transcript/GC projections a prerequisite for gameplay recovery unless a specific canonical owner dependency proves otherwise.

---

# 21. Assumptions / evidence ledger

## Verified facts

- Step-3 portable owners and payload semantics exist in canonical spec + DEV schemas/tests.
- Procedure is an independent owner and may survive retries/suspensions/recovery.
- Continuation excludes derived caches and includes fixed inputs/pending responses.
- mandatory child identity must survive Event commit.
- temporal obligations are owner-local; no scheduler record exists.
- current GAME campaign layout lacks runtime owner placement/rooting.
- session/checkpoint/CURRENT do not currently enumerate runtime owners.
- live scene state has durable native routing from scene pointer.
- checkpoints are sparse and may lag ordinary durable HEAD.
- multiplayer allows several sessions/scenes.
- current indexes do not include a general Effect/temporal-owner index.

## Inferences

- one session cannot be the global runtime closure root.
- checkpoint cannot be sole current root source.
- active Procedure needs root membership independent of open Command unless a later proven invariant guarantees otherwise.
- Agenda can remain rebuildable only with bounded temporal-owner enumeration.
- some recovery-routing membership projection/index is required unless physical storage itself supplies an equivalent bounded active set.

## Recommendations

- no new semantic recovery authority;
- closure as property over native owners;
- bounded typed root membership as required recovery evidence;
- exact physical partitioning deferred to 5.7 unless challenge disproves that deferral.

## Unknowns deliberately deferred

- exact root file/path/schema;
- exact Procedure lifecycle wire state;
- exact due-work lifecycle;
- exact controlled handoff boundary;
- exact publication transaction protocol;
- exact live runtime-root placement;
- exact checkpoint cut format;
- exact retention/GC.

---

# 22. Research-phase decision status

At the end of research, no evidence requires:

- a new semantic state authority;
- changing Step-2/Step-3 owner boundaries;
- serializing Temporal Agenda;
- persisting raw model/chat context;
- a first-class `runtime.recovery_closure` record;
- a global total-order recovery frontier.

One architecture question remains for analytical challenge:

> Is the logical bounded active-root projection enough for Step 5.2, with physical partitioning deferred to 5.7, or must Step 5.2 choose a concrete single-vs-distributed root-registry architecture now because that choice materially constrains later durability/concurrency semantics?

No owner decision is requested yet. The next required step is analytical challenge of this recommendation.
