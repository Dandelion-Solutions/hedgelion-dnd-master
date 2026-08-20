# Step 5.2 — Resumable Runtime Closure — Candidate Specification

Status: **CANDIDATE ARCHITECTURE — ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-20

Basis:

- pre-research charter;
- architecture task brief;
- research & architecture draft;
- analytical challenge;
- decision brief.

This specification defines Step-5.2 logical architecture only. It does not select the final repository paths, checkpoint schema, publication protocol, live CAS placement, due-work state machine or retention algorithm.

---

# 1. Canonical concept

## 1.1 Definition

**Resumable Runtime Closure** is the correctness property that, for one promised durable recovery source set, every gameplay-significant current owner, unresolved execution dependency and pending obligation required to resume from that source set is recoverable from bounded typed native routing evidence, while all non-authoritative derived state can be rebuilt.

Resumable Runtime Closure is **not**:

- a new semantic state owner;
- a mandatory persistent record;
- a universal snapshot;
- a copy of all HOT state;
- a generic pending-work table;
- a Temporal Agenda serialization;
- a universal frontier/comparison algebra;
- a scalar `RecoveryCut` identity;
- a transcript/model-memory snapshot.

---

# 2. Core laws

## LAW 5.2-1 — NATIVE OWNER PRESERVATION

Recovery metadata and routing evidence SHALL NOT replace or duplicate current writable authority.

Every recovered gameplay-significant value is read from its accepted native semantic owner or from accepted irreducible execution evidence owned by that runtime record.

Examples:

- Procedure resources come from Procedure;
- active Effect temporal bindings come from Effect;
- pending Choice/Reaction comes from Continuation;
- live-owned scene mutation comes from the live epoch;
- world HP/location/ownership come from their normal world owners.

---

## LAW 5.2-2 — BOUNDED ROOT DISCOVERY

At every promised durable recovery source set, every gameplay-significant active owner or armed obligation that is not guaranteed reachable from another admitted root SHALL be discoverable through a bounded typed routing/index mechanism whose membership is coherent with the native owner state.

Normal cold recovery SHALL NOT require:

- scanning all campaign files;
- scanning all historical runtime records;
- scanning Git history;
- loading all WORLD entities;
- semantic inference from narrative/transcript text.

Exceptional integrity repair may use broader bounded evidence after recovery integrity is already suspect.

---

## LAW 5.2-3 — ROUTING IS EVIDENCE, NOT AUTHORITY

Recovery-routing membership may answer only:

> Which typed owner/reference must be loaded and validated for recovery?

It SHALL NOT independently own:

- owner lifecycle/state;
- Procedure resources;
- pending child state;
- due order/deadlines;
- current HP/resources/effects;
- chronology ordering;
- RNG outcomes;
- Choice/Reaction options;
- live overlay truth.

If routing evidence conflicts with the native owner, the native owner owns semantic truth and the routing projection is stale/corrupt evidence.

---

## LAW 5.2-4 — PARTITIONABLE RECOVERY ROUTING

Recovery-routing evidence SHALL be partitionable by existing semantic/writable scope.

Step 5.2 SHALL NOT require every independent scene/session/live/runtime mutation to update one campaign-global hot singleton root registry.

Equivalent physical implementations may include:

- active-only path membership;
- typed per-kind indexes;
- per-scene/per-procedure routing references;
- campaign-global cold partitions for genuinely global roots;
- live-epoch-local partitions;
- combinations of the above.

Exact representation is owned by later persistence/recovery/live slices.

---

## LAW 5.2-5 — TRANSITIVE CLOSURE COMPLETENESS

A promised durable recovery source set is valid only when every required root and every **required** dependency reachable from a recoverable owner is itself:

1. durable/recoverable in its native domain; or
2. explicitly optional; or
3. deterministically rebuildable from surviving owners/evidence.

A durably recoverable owner SHALL NOT depend on a required identity/state whose lifetime is shorter than the promised recovery source set.

This includes unpublished local identities, RAM-only Procedure state and missing required live/runtime targets.

---

## LAW 5.2-6 — DERIVED STATE REBUILDS

Derived caches/indexes SHALL NOT be required as state authority for cold recovery when their semantic inputs survive.

At minimum this applies to:

- Temporal Agenda;
- MechanicalContext;
- condition/effect aggregation indexes;
- mechanical dependency DAG caches;
- loaded-record caches;
- derived AC/modifiers/speeds and similar calculations;
- Context Assembler bundles/source manifests after immediate trace need;
- repository search/listing caches;
- Story rendering/editorial working buffers.

Missing derived state is rebuild work, not canon corruption.

---

## LAW 5.2-7 — NO INVENTED LOST HOT STATE

Gameplay-significant HOT/SOFT state may exist ahead of the last durable recovery source set under accepted sparse durability semantics.

If that volatile current state is destroyed before a boundary successfully makes it part of a promised durable source set, cold recovery SHALL return to the last actual durable source set and SHALL NOT invent the missing HOT/SOFT changes.

Step 5.2 does not determine when later slices must force a newer durable boundary.

---

## LAW 5.2-8 — DOMAIN-NATIVE RECOVERY SOURCES

A recovery source set may contain several compatible domain-native durable revisions, including campaign and independent live scopes.

Their inclusion in one recovery operation SHALL NOT imply:

- scalar comparability;
- total ordering;
- shared revision numbers;
- fictional chronology ordering;
- one merged writable authority.

Compatibility is established through explicit native references/ownership relations.

---

# 3. State classification

Every gameplay/runtime concept participating in recovery SHALL be classifiable as one of:

```text
AUTHORITATIVE STATE
IRREDUCIBLE RECOVERY EVIDENCE / ROUTING
REBUILDABLE DERIVED STATE
TRULY EPHEMERAL STATE
VOLATILE CURRENT STATE AHEAD OF DURABLE SOURCE SET
DEFECT / UNOWNED REQUIRED STATE
```

A value SHALL NOT be promoted into durable recovery state merely because recomputation is inconvenient.

A value SHALL NOT be marked ephemeral if losing it can change the promised recovered gameplay point or deterministic continuation.

---

# 4. Authoritative recovery participants

## 4.1 World/current state owners

Ordinary current world facts remain in the accepted world/domain owner.

A recovery projection may reference those owners but SHALL NOT copy their current values as a second authority.

---

## 4.2 RuntimeCommand

A non-settled RuntimeCommand is an independently recovery-relevant owner when it still owns unfinished descendant closure.

It may own/refer to:

- accepted input identity/fingerprint;
- root Resolution;
- mandatory pending child descriptors;
- invocation facts;
- disposition;
- receipt evidence.

A settled Command need not remain in active recovery routing solely because it is retained for history/audit.

---

## 4.3 Procedure

An active Procedure is independently recovery-relevant and SHALL remain boundedly discoverable for its full active lifetime.

Procedure discovery SHALL NOT depend solely on an open Command because Procedure may survive between Commands/Resolutions.

Procedure remains sole owner of procedure-local ResourceState.

Later machine realization SHALL provide an unambiguous active-versus-terminal lifecycle/membership contract without transferring lifecycle authority to a recovery index.

---

## 4.4 Resolution

An active/suspended/blocked Resolution remains native operational state.

When reachable from an admitted root, Resolution need not be redundantly listed as a separate root.

Required state as applicable includes:

- root/initiating command or causal invocation key;
- Activity/catalog context;
- Procedure ref;
- status/cursor/safe recompute phase;
- fixed RNG results;
- invocation facts/prior exports;
- child refs;
- Continuation ref;
- committed segment/receipt evidence.

---

## 4.5 Continuation

Continuation remains one portable suspended Resolution generation.

It SHALL preserve the already accepted irreducible suspension state and SHALL NOT acquire copied Procedure state or derived caches merely for Step-5 recovery.

If Resolution durably references its current Continuation generation and Resolution is boundedly reachable, Continuation need not be independently rooted.

---

## 4.6 Pending Interaction / IntentPlan

A materially unresolved accepted player input before Command creation is conditionally recovery-relevant when the applicable durability/handoff protocol promises that exact semantic point will survive.

Existing Interaction/IntentPlan semantics own that state.

Examples:

- target clarification after an accepted declaration;
- compound IntentPlan with committed earlier clauses and a later unresolved clause.

Not recovery owners by themselves:

- generic open handoff prose;
- optional suggestions;
- unaccepted generated narration;
- ordinary prompt wording.

Step 5.2 admits no new generic `pending_prompt` or `resume_point` class.

---

# 5. Irreducible execution continuity

## 5.1 Mandatory child descriptors

If a committed segment/event causes mandatory child work, the stable pending-child descriptor is irreducible execution evidence until the child is materialized/settled.

Recovery SHALL NOT rediscover historical mandatory firing by rescanning current trigger bindings as a substitute for a missing committed descriptor.

Missing required descriptor after the parent commit is an integrity defect.

---

## 5.2 Fixed RNG

An already generated/accepted RNG value that remains relevant to unfinished execution SHALL survive with the owning Resolution/Continuation/committed evidence.

Cold recovery SHALL NOT reroll it merely because the process restarted.

ResolutionTrace SHALL NOT be the sole authoritative storage for such a value.

---

## 5.3 Future RNG

Step 5.2 does not require all future randomness to be reproducible across restart.

Only already committed/reserved future RNG identity/state whose preservation is itself part of accepted execution semantics must survive.

Step 5.3 owns exact future-RNG representation/continuity.

---

## 5.4 Pending Choice / Reaction

A fixed Choice/Reaction offer embedded in Continuation is part of the durable suspension state when that Continuation belongs to the promised recovery source set.

Recovery SHALL preserve:

- offer identity;
- responder identity;
- bounded candidate/option identity set;
- Continuation generation;
- applicable single-consume/idempotency semantics.

It SHALL NOT regenerate a materially different offer from ambient post-restart state.

---

## 5.5 Accepted invocation/catalog/dependency evidence

Invocation facts, catalog-context identity, prior committed exports, dependency/revision refs and committed receipt refs remain part of recovery continuity while needed to preserve safe recompute/retry meaning.

Recovery SHALL prefer accepted stored context over rebinding under later ambient context when the accepted execution is still open.

---

# 6. Temporal continuity source contract

## 6.1 Native temporal authority

Temporal obligations remain on their admitted native owners, including as applicable:

- active Effect temporal binding;
- Effect scheduled-trigger state;
- Resource delayed recovery state/policy;
- LifeState temporal recovery state;
- Procedure-bound temporal state;
- other later admitted owner-local temporal obligations.

Recovery routing SHALL NOT copy deadline/order/due semantics as authority.

---

## 6.2 Armed temporal-source discovery

Any armed temporal owner that can become mechanically due independently of being otherwise loaded SHALL be boundedly discoverable through typed temporal-source routing/index evidence unless another guaranteed active root already reaches it.

This requirement is sparse: it does not require indexing every world record.

---

## 6.3 Temporal Agenda rebuild

Cold recovery rebuilds Temporal Agenda from:

1. boundedly discovered armed temporal owners;
2. each native owner’s TemporalBinding/current state;
3. applicable Procedure/chronology/context evidence.

Agenda-local sort/order/cache state is disposable.

Once a due occurrence has been selected/materialized into committed execution semantics, its identity belongs to Step-3 pending child/Resolution continuity rather than to Agenda reconstruction.

Step 5.3 owns due selection, firing lifecycle and no-lost/no-double execution.

---

# 7. Root classes and closure traversal

The minimum current logical root classes are:

```text
A. non-settled RuntimeCommand
   when unfinished descendant closure exists

B. active Procedure
   independently of Command lifetime

C. pending Interaction/IntentPlan
   only when materially unresolved and promised durable

D. armed temporal source owner
   only when otherwise not guaranteed reachable from another root/native active index
```

Known singleton:

```text
runtime.id_allocator = campaign-allocator
```

The allocator does not require active-membership discovery because its identity is deterministic.

Common transitive descendants need not be redundant roots:

```text
Command
  -> Resolution
      -> Continuation
      -> child Resolutions
      -> Procedure ref
      -> receipts / MechanicalEvents
  -> pending child descriptors

Procedure
  -> participant-local procedure state
  -> procedure-bound temporal context
```

---

# 8. Recovery-routing projection contract

Step 5.2 defines logical properties but not a mandatory wire format.

Any later physical recovery-routing representation SHALL satisfy:

## 8.1 Typed membership

Each entry/path/membership relation must identify enough semantic kind/scope to load the correct owner without interpreting arbitrary prose.

Untyped `pending[]`, `jobs[]` or `consequences[]` buckets are forbidden.

## 8.2 Reference-only semantics

Routing representation stores references/placement membership, not copies of current owner payloads.

## 8.3 Sparse membership

Only currently recovery-relevant roots/source owners belong in active routing.

Historical/terminal record retention is separate.

## 8.4 Coherent durability

Owner activation/terminality and corresponding required routing membership changes must become durable coherently enough that an acknowledged recovery source set cannot expose:

- a root to a missing owner;
- an active owner omitted from required routing;
- premature root removal that drops unfinished work.

Exact Git transaction mechanics belong to 5.6/5.7/5.8.

## 8.5 Partitionability

Physical routing may be divided by campaign/global, scene, Procedure, live epoch, runtime kind or another existing semantic/writable scope as later design proves useful.

No Step-5.2 requirement forces one global mutable file.

## 8.6 Boundedness

Normal cold-start enumeration cost must scale with active recovery-relevant owners/partitions rather than campaign age/history.

---

# 9. Durable dependency closure

A recoverable root may reference:

- durable campaign identities;
- durable live-epoch identities within their authoritative scope/lifetime;
- other recoverable runtime owners;
- immutable catalog/rules identity accepted by the execution;
- rebuildable/optional dependencies explicitly marked as such.

A recoverable root SHALL NOT require:

- session-local entity identity that will vanish at cold restart;
- RAM-only Procedure/Resolution state;
- unpublished campaign record absent from the recovery source set;
- raw model context;
- a Story/transcript record as substitute for semantic owner state.

Before a durability protocol acknowledges a source set, required shorter-lived dependencies must be promoted/rekeyed/materialized or the durability attempt is invalid.

---

# 10. Live-scope composition

Step 5.2 preserves live ownership.

Rules:

1. durable campaign scene pointer discovers active live epoch state;
2. live-owned world truth remains live-owned until compaction/absorption;
3. active runtime roots belonging to the live scope must be discoverable through the live scope’s admitted routing partition/chain;
4. campaign recovery SHALL NOT copy live state into campaign merely to create one snapshot;
5. independent live epochs remain independent and incomparable unless an owning contract defines a relation;
6. missing pointed live state is recovery/integrity failure, not silent fallback to campaign base;
7. closed-unabsorbed live epoch is a recoverable operational condition but not a normal writable gameplay state.

Exact root placement and handoff across live compaction belong to 5.8.

---

# 11. Campaign allocator / identity continuity

`runtime.id_allocator` remains the authoritative campaign allocator singleton.

Rules:

1. published campaign-scoped IDs are immutable and never reused;
2. allocation state needed to preserve that contract must be recoverable;
3. volatile session-local IDs/reservations may disappear if nothing durably recoverable depends on them;
4. no promised durable root/dependency closure may contain a required reference to a vanished local ID;
5. live-epoch provisional IDs are valid only within the authoritative epoch lifetime until promotion/compaction.

Exact conflict/rekey/publication mechanics remain later Step-5 work.

---

# 12. Semantic resume outside mechanics

Cold recovery does not require exact prose continuity unless exact wording itself is an admitted retained artifact for a separate reason.

Recovery categories:

```text
settled/open scene
    -> reload semantic state and regenerate equivalent handoff

pending mechanical response
    -> Continuation pending_response

pending accepted clarification before Command
    -> Interaction/IntentPlan semantic state when promised durable

maintenance same-context handoff
    -> maintenance continuation frame may assist, but is not cold authority
```

A fresh runtime SHALL NOT invent an exact quote/action merely to appear seamless when only semantic evidence survives.

---

# 13. Checkpoint relation

Checkpoint remains sparse immutable recovery description/evidence.

Step 5.2 establishes:

1. checkpoint is not the sole source of current active-root membership;
2. checkpoint may later capture/reference the root-routing state appropriate to the historical recovery source set it describes;
3. current campaign/live durable state may advance without checkpoint creation;
4. a checkpoint older than current durable state does not force current cold recovery backward merely because it is the latest checkpoint;
5. exact historical cut/reference/hydration semantics remain 5.7.

Step 5.2 introduces no universal `RecoveryCut` record.

---

# 14. Story/transcript relation

Gameplay cold recovery SHALL NOT depend on Story projection catch-up or exact transcript retention when canonical/runtime semantic owners are sufficient.

If gameplay correctness depends on meaning that exists only in noncanonical Story/transcript because it was never materialized into the proper owner, that is a materialization/recovery defect.

Story/transcript durability remains separately owned by later slices.

---

# 15. Integrity outcomes

## 15.1 Missing rebuildable state

Examples:

- Agenda absent;
- derived mechanics cache absent;
- context bundle absent.

Outcome:

```text
rebuild from owners
```

No canon suspicion solely from absence.

## 15.2 Stale coordination/routing cache with valid native source

Example:

- stale Session base SHA.

Outcome:

```text
refresh/rebind through normal native routing
```

## 15.3 Required recovery root/target missing or incompatible

Examples:

- routing lists active Procedure but record missing;
- Continuation requires missing Procedure;
- durable root requires vanished local entity;
- scene points to missing/invalid live epoch;
- required catalog context cannot be resolved compatibly.

Outcome conceptually:

```text
recovery blocked for affected scope
-> CANON_SUSPECT / typed recovery failure
-> bounded validation/repair
```

Exact failure code/state belongs to 5.7 implementation design.

## 15.4 Routing projection conflicts with owner

Owner semantics win; routing projection is repaired.

An omitted owner that should have been enrolled is a projection-completeness defect. Normal recovery cannot silently assume omission means terminality if other evidence establishes required existence.

---

# 16. Boundary interaction

Step 5.2 defines closure completeness, not boundary timing.

When later authority declares a state must become durable, the publication/handoff must include all currently required closure participants for the promised point.

Therefore later slices SHALL NOT acknowledge a save/handoff/durability boundary while leaving behind in volatile memory:

- active Procedure state required for resume;
- current Continuation/fixed response state;
- mandatory pending child identity;
- required armed temporal owner state/root membership;
- required promoted identity dependency.

Which events trigger that obligation belongs to 5.4/5.5.

---

# 17. Explicit-save constraint

Step 5.2 constrains future alignment of `SAVE_CONTRACT.md`:

If an explicit save occurs while recovery-relevant runtime owners/obligations are active, “save all established cross-session state” includes those native operational owners and required routing evidence.

A save that persists world records but loses an active Procedure/Continuation the system promises to resume is incomplete.

Step 5.5 owns final save/durability semantics; Step 5.7 owns recovery representation.

---

# 18. Current implementation/debt ledger

The following are not implemented by this architecture closure and remain explicit debt:

1. physical repository placement for Step-3 runtime owners;
2. active-root routing/index representation;
3. temporal-source routing/index representation;
4. Procedure lifecycle/status machine realization;
5. Interaction/message machine realization for durable pending clarification where needed;
6. GAME schemas for Step-3 runtime owners;
7. SAVE_CONTRACT operational-owner alignment;
8. RANDOMNESS/MECHANICS_INTEGRITY wording alignment with Step-3 fixed RNG ownership;
9. checkpoint root-cut representation/hydration;
10. live runtime-root partition placement/compaction handoff;
11. exact recovery failure/status vocabulary;
12. retention/GC of terminal runtime owners/routing entries.

These are implementation/later-slice obligations, not unresolved Step-5.2 semantic decisions.

---

# 19. Later-slice obligations

## 5.3 Temporal & Pending-Obligation Continuity

MUST define:

- Agenda rebuild algorithm from bounded temporal-source membership;
- due selection/materialization boundary;
- no-lost/no-double firing;
- fixed/reserved RNG continuity;
- transition from temporal source obligation to Step-3 mandatory invocation.

MUST NOT make Agenda authority.

## 5.4 Host Lifecycle & Session Handoff

MUST decide when controlled context/process destruction requires current closure durability before handoff.

MUST distinguish ephemeral same-context continuation frame from cold-recovery state.

## 5.5 SOFT / HARD / SAVE

MUST make a durability acknowledgement cover the entire required closure for the promised point.

## 5.6 Campaign Publication & Crash Consistency

MUST publish owner/root-membership/dependency-promotion changes coherently.

MUST NOT expose durable routing to missing owners or prematurely drop unfinished roots.

## 5.7 Checkpoint / Recovery Protocol

MUST choose physical recovery routing/checkpoint representation and hydration order.

MUST preserve domain-native source identity and B-NARROW laws.

## 5.8 Multiplayer / Live-Epoch Ownership

MUST decide live-local runtime root placement and membership transfer/compaction behavior.

MUST preserve partitionability and avoid global hot serialization.

## 5.9 Chronology

MUST supply material chronology/context evidence required to interpret recovered TemporalBindings without deriving fictional order from storage/root order.

## 5.10–5.13

MUST treat Story/transcript/GC as separate from canonical operational authority unless explicit dependencies require otherwise.

---

# 20. Acceptance scenarios

The candidate is valid only if later realization can satisfy all of these without violating the laws above.

### A. Clean restart

No in-flight execution; scene/world state + temporal-source roots rebuild exact actionable state.

### B. Lost unpublished SOFT

Cold restart returns to prior durable source set without inventing lost SOFT changes.

### C. Suspended reaction

Command/Resolution/Procedure/Continuation + fixed RNG + offer survive; same reaction opportunity resumes.

### D. Active Procedure between Commands

Procedure remains discoverable despite no non-settled Command.

### E. Post-commit mandatory child

Descriptor survives; child cannot be silently lost or doubled.

### F. Agenda loss

Agenda rebuilt from temporal owners; no due obligation silently disappears.

### G. Off-screen timer

Owner discoverable without loading all WORLD records.

### H. Two independent live epochs

Both recover through native scene/live routing without global root contention or inferred order.

### I. Pending clarification

Material accepted declaration can resume from Interaction/IntentPlan without full transcript.

### J. Stale session

Session refreshes; stale coordination metadata cannot override campaign/live authority.

### K. Checkpoint behind HEAD

Current recovery uses current durable source set; checkpoint remains optional historical recovery evidence.

### L. Missing root target

Recovery blocks affected scope and raises integrity/recovery failure rather than dropping work.

### M. Local identity leakage

Durability validation rejects root/dependency closure that requires vanished session-local identity.

### N. Story lag

Gameplay recovery succeeds independently; Story catches up later.

---

# 21. Non-goals restated

This candidate does not define:

- exact active-root file/path/schema;
- generic universal recovery record;
- checkpoint cut wire shape;
- due-work state machine;
- SOFT/HARD timing;
- publication transaction algorithm;
- live CAS/lease/compaction algorithm;
- chronology representation;
- Story/transcript retention;
- host disclosure delivery acknowledgement;
- GC algorithm;
- physical LLM topology.

---

# 22. Candidate verdict

```text
Resumable Runtime Closure             = property over native owners/evidence
new semantic recovery authority       = forbidden / not justified
new first-class closure record        = not justified
bounded typed root discovery          = required
routing evidence                      = non-authoritative, coherence-critical
routing physical shape                = partitionable, deferred
active Procedure independent rooting  = required
Temporal Agenda persistence           = forbidden as authority; rebuild
fixed accepted RNG                    = preserve with execution owner
future RNG                            = preserve only if already semantically reserved
pending clarification                 = existing Interaction/IntentPlan when durable
checkpoint                            = sparse descriptor, not current root authority
Story/transcript                      = not universal gameplay-recovery prerequisite
```

Next required stage: adversarial review of this candidate before canonicalization.
