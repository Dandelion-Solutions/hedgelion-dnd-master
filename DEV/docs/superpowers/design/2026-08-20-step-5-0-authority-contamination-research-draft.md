# Step 5.0 — Authority / Contamination Audit Research Draft

Status: **RESEARCH / ANALYTICAL DRAFT — NOT CANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Parent artifacts:

- `DEV/docs/superpowers/design/2026-08-20-step-5-expanded-architecture-agenda.md`
- `DEV/docs/superpowers/design/2026-08-20-step-5-0-authority-contamination-task-brief.md`

This draft records verified repository state, authority classifications, contamination findings, analytical challenge, and recommendations. It intentionally does not design Step 5.1 frontier representation or later Step-5 wire formats.

---

# 1. Executive finding

The active repository does **not** contain one broad persistence architecture failure. Its core ownership boundaries are mostly compatible with Steps 1–4:

- domain/world records remain current-state owners;
- `runtime.procedure`, Resolution, Continuation, RuntimeCommand and pending-child descriptors have distinct Step-3 lifetimes;
- Temporal Agenda is correctly derived rather than authoritative;
- campaign Git and temporary live epochs have distinct durable/operational roles;
- SemanticEvent/MechanicalEvent/checkpoint/session/Story are conceptually separated from current state.

However, the audit found several **early-project abstractions and duplicate pointers that are still physically present in active machine/runtime/template surfaces**. Some are known legacy leaks; others are registered Step-5 placeholders whose presence can prematurely constrain the upcoming design.

The critical Step-5.0 distinction is:

```text
A. PROVEN OBSOLETE / DUPLICATE
   remove or retire before later slices depend on it

B. ACCEPTED SEMANTIC OWNER, DURABILITY PLACEMENT STILL UNDESIGNED
   preserve owner; assign placement/enumeration to 5.2/5.7/etc.

C. EARLY RESERVED STEP-5 CONCEPT
   do not treat registration as approved authority;
   retire now or explicitly re-admit only after its owning slice proves need

D. LEGITIMATE PROJECTION / EVIDENCE / CACHE
   preserve but make non-authority classification explicit
```

The strongest contamination findings are:

1. current-layout CORE docs still contain legacy `CAMPAIGN/LIVE/LIVE_STATE.yaml` paths although current root-layout contract is `LIVE/LIVE_STATE.yaml`;
2. `WORLD/SECRETS/` remains in the new-campaign template despite Step 4 retiring Secret as an independent authority;
3. `STATE/TACTICAL/` plus `scene.tactical_state_path` form an untyped generic tactical-state slot despite Step 3 assigning operational owners to Procedure/Resolution/Continuation/world state;
4. `world.timeline_marker` still encodes the old scalar numeric-slot chronology model, while current chronology is a partial order over events/frontiers;
5. `STATE/CURRENT.pending_global_consequences` is an untyped generic pending-work container with no accepted owner/lifecycle and overlaps newer owner-local/pending-child designs;
6. latest checkpoint state is represented in three potential pointer locations (`MANIFEST.last_checkpoint_id`, `CURRENT.last_checkpoint_id`, `CHECKPOINTS/LATEST.yaml`);
7. global current chronology/event-frontier fields are duplicated between MANIFEST and CURRENT;
8. `runtime.dirty_record` and `runtime.publication_batch` remain registered runtime classes inherited from the early SQLite proposal even though their independent identity/lifecycle has not passed Step-5 design and they have no dedicated current machine-state schemas;
9. multiple legitimate Step-3 runtime owners have machine schemas but still lack an explicit durable storage placement/recovery enumeration contract — an intentional Step-5 carry-forward, not permission to create a generic runtime snapshot;
10. several live/scene generic fields (`live_facts`, `pending_durable_events`, `scene.environment.transient_facts`) require later-slice narrowing so they do not become catch-all current/pending authorities.

Recommendation confidence: **HIGH** for the classification and cleanup directions below. Exact frontier/recovery formats remain deliberately undecided.

---

# 2. Verified current architecture baseline

## 2.1 Campaign storage and durability boundaries

Current CORE already separates:

```text
STORAGE
    what campaign storage is / how records are organized

DURABILITY_GUARD
    WHEN canonical HOT/SOFT state must become durable

SAVE_CONTRACT
    explicit SAVE_ALL_DIRTY semantics

PERSISTENCE
    HOW an already-decided publication is transported
```

`STORAGE.md` explicitly states:

- persistent campaign canon lives only in campaign storage;
- chat context and extracted runtime cache are temporary;
- current campaign layout is at branch root;
- new writes must not create a `CAMPAIGN/` wrapper;
- a new durable reference to a new ID must publish the referenced record/index in the same closure;
- hot working state carries known HEAD/tree, loaded records, dirty records and durable-frontier time;
- LOG is semantic history, not transaction journal/transcript;
- checkpoints are sparse recovery frontiers.

`PERSISTENCE.md` defines one non-force campaign tree transaction and makes an unreachable prepared commit acceptable after a race. This reduces pressure to invent a second durable publication-journal authority.

`DURABILITY_GUARD.md` already admits a safety flush when known context loss/maintenance would otherwise destroy dirty HOT state, while acknowledging that truly lost unpublished RAM cannot be reconstructed.

`SAVE_CONTRACT.md` requires all established cross-session state to materialize through its normal authoritative representation rather than prose notes.

Conclusion: the high-level WHEN/HOW split is healthy and should survive Step 5.

## 2.2 Step-3 runtime ownership

The accepted Step-3 owner graph remains coherent:

```text
runtime.command
    root executable request + mandatory descendant closure

runtime.resolution
    one Activity invocation + cursor/fixed RNG/child refs

runtime.procedure
    sole procedure-local ResourceState owner

runtime.continuation
    one suspended Resolution generation

pending child descriptor
    embedded mandatory unexecuted descendant identity

MechanicalEvent / receipt / trace
    committed evidence, not current world owner
```

The current DEV machine schemas materially reflect those distinctions.

Step 3 explicitly deferred **Git publication/restoration** of these continuity payloads to Step 5 and requires recovery roots to preserve, as applicable:

- active Procedure identity/state roots;
- suspended Resolution/Continuation;
- fixed RNG/choice inputs;
- committed segment/Event frontier;
- mandatory reaction/trigger/scheduled pending descriptors;
- accepted invocation facts/provenance;
- mechanically material local temporal evidence;
- idempotency state.

Therefore the absence of a current campaign storage root for these runtime records is a **placement/enumeration gap**, not an ownership gap. Step 5.0 must not invent a generic `TACTICAL` or runtime snapshot owner to fill it.

## 2.3 Temporal ownership

Step-2 assurance is explicit:

```text
world.effect
    temporal_binding
    scheduled_trigger_state[key]

other state owners
    Resource delayed recovery
    LifeState recovery
    checkpointable runtime/procedure obligations

Temporal Agenda
    disposable derived due-work index
```

Losing Agenda cannot lose or alter a deadline. The required Step-5 work is durable continuity and bounded rebuilding from the owners.

## 2.4 Live-scene ownership

Current live architecture is conceptually consistent:

```text
campaign branch
    durable long-term canon / base

active live epoch
    temporary OPERATIONAL authority for one scene-owned mutable scope

last_absorbed_live_head_sha
    handoff/idempotency evidence
```

One entity may not be owned by two live epochs. Orphan live branches are explicitly non-authoritative. `closed` freezes an epoch but does not itself prove durable absorption.

The core authority model is healthy; some path and Step-4 knowledge fields are stale/underspecified.

## 2.5 Chronology

Current `CHRONOLOGY.md` uses:

- causal `caused_by_event_ids`;
- noncausal order `after_event_ids`;
- local scene ordering/frontiers;
- optional exact/approximate world time;
- a sparse globally reconciled `CURRENT.world_time.frontier`;
- partial rather than total ordering.

Git commit order is explicitly not fictional chronology.

This directly conflicts with an older catalog derivation that modeled gameplay chronology as globally comparable numeric `world.timeline_marker.slot` values allocated in steps of ten.

---

# 3. Authority classification ledger

This table records current semantic classification, not final Step-5 storage format.

| Concept | Classification | Current semantic owner / source | 5.0 disposition |
|---|---|---|---|
| world/entity current state | `CURRENT_AUTHORITY` | owning `world.*` / domain record | KEEP |
| `runtime.command` | `OPERATIONAL_AUTHORITY` | RuntimeCommand | KEEP; durable placement 5.2/5.7 |
| `runtime.resolution` | `OPERATIONAL_AUTHORITY` | Resolution | KEEP; durable placement 5.2/5.7 |
| `runtime.procedure` | `OPERATIONAL_AUTHORITY` | Procedure | KEEP; durable placement 5.2/5.7 |
| `runtime.continuation` | `OPERATIONAL_AUTHORITY` | Continuation generation | KEEP; durable placement 5.2/5.7 |
| pending child invocation | `PENDING_OBLIGATION_AUTHORITY` embedded in command/execution owner | RuntimeCommand / execution owner | KEEP; continuity 5.3 |
| Effect temporal binding | `PENDING_OBLIGATION_AUTHORITY` | `world.effect` application | KEEP |
| Effect scheduled trigger state | `PENDING_OBLIGATION_AUTHORITY` | `world.effect` application | KEEP |
| Resource/LifeState delayed recovery | `PENDING_OBLIGATION_AUTHORITY` | owning state record | KEEP |
| fixed RNG in active/suspended execution | `OPERATIONAL_AUTHORITY` | Resolution/Continuation | KEEP |
| Temporal Agenda | `DERIVED_INDEX_CACHE` | rebuilt from temporal owners | KEEP derived; never serialize as authority |
| MechanicalContext / dependency DAG / effect/condition indexes | `DERIVED_INDEX_CACHE` | rebuilt from authoritative loaded state | KEEP derived |
| SemanticEvent/LOG | `HISTORICAL_EVIDENCE` | append-only semantic history | KEEP |
| MechanicalEvent | `HISTORICAL_EVIDENCE` / committed mechanical fact | execution segment | KEEP |
| receipt/trace | `HISTORICAL_EVIDENCE` / diagnostic evidence | execution owner | KEEP; retention later |
| checkpoint record | `RECOVERY_PROJECTION` | immutable recovery descriptor | KEEP; exact protocol 5.7 |
| `runtime.session` | `RECOVERY_PROJECTION` + coordination metadata | session record | KEEP, explicitly non-authoritative for campaign HEAD |
| `runtime.message` | retained discourse/evidence candidate | message record | KEEP reserved; exact retention 5.11 |
| `STATE/CURRENT` | compact current routing + selected frontier projection | CURRENT file | KEEP, narrow mixed fields |
| MANIFEST engine/mode/storage/access config | current campaign configuration authority | MANIFEST | KEEP |
| MANIFEST current chronology frontier | duplicate current-state metadata | MANIFEST vs CURRENT | RETIRE MANIFEST copy; CURRENT is existing chronology owner |
| MANIFEST global event pointer | ambiguous duplicate | MANIFEST vs CURRENT | candidate RETIRE MANIFEST copy; see §6 |
| MANIFEST checkpoint pointer | checkpoint routing metadata | MANIFEST | KEEP as current normative pointer pending 5.7 |
| CURRENT checkpoint pointer | duplicate routing metadata | CURRENT | RETIRE |
| `CHECKPOINTS/LATEST.yaml` | duplicate latest-checkpoint projection | separate file | RETIRE from new template; 5.7 defines deterministic lookup |
| known HEAD/tree cache | `TRANSPORT_METADATA` | active working set | KEEP ephemeral/cache; never campaign truth |
| dirty HOT set | current unpublished canonical state + bookkeeping | owning hot records/working set | KEEP concept; exact bookkeeping 5.5 |
| `runtime.dirty_record` | early reserved independent-record candidate | old SQLite design | RETIRE from active runtime class inventory; re-admit only if 5.5 proves independent lifecycle |
| transaction snapshot | `TRANSPORT_METADATA` | one PERSISTENCE operation | KEEP embedded/ephemeral |
| `runtime.publication_batch` | early reserved independent-record candidate | old SQLite design | RETIRE from active runtime class inventory; re-admit only if 5.6 proves independent lifecycle |
| `value.publication_manifest` | embedded transport-value candidate | publication planner | QUARANTINE until 5.6; no authority |
| `runtime.id_allocator` | `OPERATIONAL_AUTHORITY` for campaign sequential allocation | campaign allocator | KEEP; durable placement/atomicity 5.2/5.6 |
| campaign branch HEAD | durable storage frontier evidence | Git ref/commit | KEEP; frontier semantics 5.1 |
| active live HEAD/state | temporary `OPERATIONAL_AUTHORITY` for owned scope | live epoch | KEEP; refine 5.8 |
| `last_absorbed_live_head_sha` | handoff/idempotency evidence | durable scene | KEEP evidence |
| live cached head/blob | `TRANSPORT_METADATA` | session cache | KEEP derived/cache |
| Dramaturg prep | `EPHEMERAL_WORKING_STATE` / optional noncanonical cache | preparation | KEEP noncanonical; retention Step 6 |
| Context Assembler bundle/source manifest | `EPHEMERAL_WORKING_STATE` / trace evidence | one role request | KEEP non-authoritative |
| Story records | `PRESENTATION_PROJECTION` | `STORY/*` | KEEP; durability 5.10 |
| transcript | retained discourse evidence / presentation input | Story/message retention | KEEP; exact owner/retention 5.11 |
| `WORLD/SECRETS` template root | obsolete implied Secret authority | none after Step 4 | RETIRE |
| `STATE/TACTICAL` template root | obsolete generic state bucket | none | RETIRE |
| `scene.tactical_state_path` | pointer to undefined generic tactical owner | none | RETIRE |
| `CURRENT.pending_global_consequences` | undefined generic future-work bag | none | RETIRE |
| `world.timeline_marker(slot)` | obsolete scalar chronology authority | old timeline model | RETIRE |
| `transition.timeline_place` / `event.timeline.placed` | mutation/evidence surface for obsolete marker | old timeline model | RETIRE with marker |
| `transition.event_time_advance` / `event.event_time.advanced` | event/local-time transition candidates | not yet fully reviewed | KEEP QUARANTINED to 5.9; do not treat as global clock |
| scene chronology frontier | compact local chronology state/reference | scene | KEEP; 5.9 |
| CURRENT global chronology frontier | compact reconciled chronology state/reference | CURRENT | KEEP; 5.1/5.9 refine |
| `world.timeline_marker` historical prose examples | historical derivation only | non-authoritative docs | do not rewrite history |
| live `known_by_pc_ids` / perception arrays | operational perception/compaction evidence candidate | live epoch | KEEP but not durable knowledge authority; align 5.8/Step-4 implementation |
| live `pending_durable_events` | staging/compaction candidate | live epoch | QUARANTINE to 5.8; no generic pending-work authority |
| scene `environment.transient_facts` | ambiguous scene-local embedded facts | scene | QUARANTINE; constrain in 5.2/Step-6 gap review |

---

# 4. Proven contamination findings

## F-01 — Legacy `CAMPAIGN/LIVE/LIVE_STATE.yaml` leaks into current CORE

### Verified state

Current storage/bootstrap contracts require root-layout campaign paths and forbid new `CAMPAIGN/` wrappers. `live_scene.schema.yaml` already states:

```text
current: LIVE/LIVE_STATE.yaml
legacy:  CAMPAIGN/LIVE/LIVE_STATE.yaml
```

But `LIVE_SCENE.md` and `MULTIPLAYER.md` still instruct the ordinary current hot path to use `CAMPAIGN/LIVE/LIVE_STATE.yaml`.

### Classification

Documentation/runtime routing defect; no architecture decision required.

### Recommendation

Replace current-path references with resolved current `LIVE/LIVE_STATE.yaml`; mention legacy path only under an explicit legacy-layout resolver rule.

Owner: immediate 5.0 cleanup.

---

## F-02 — `WORLD/SECRETS/` survives Step-4 Secret retirement

### Verified state

`GAME/CAMPAIGN/WORLD/SECRETS/.gitkeep` exists and `init_campaign.py` copies the whole template into every new campaign.

Step 4 explicitly removed independent Secret truth/knowledge authority and states `WORLD/SECRETS` is legacy organization, not a required new-campaign root.

### Risk

The physical root advertises an apparently supported semantic owner:

```text
secret fact -> WORLD/SECRETS
```

which is exactly what Step 4 forbids.

### Recommendation

Remove the placeholder from the new campaign template. Existing legacy campaign data is migration input, not proof of current authority.

Owner: immediate 5.0 cleanup.

---

## F-03 — Undefined generic `STATE/TACTICAL` owner

### Verified state

The campaign template includes empty `STATE/TACTICAL/` and `scene.schema.yaml` contains `tactical_state_path`, but no typed tactical-state schema or accepted lifecycle owner exists.

Current accepted mechanics already distinguish:

- world/actor/scene/encounter state;
- Procedure operational state;
- Resolution execution state;
- Continuation suspension state;
- owner-local Effect/Resource/LifeState state.

### Risk

`TACTICAL` becomes a catch-all snapshot where implementations copy initiative, geometry, HP, Procedure budgets, pending actions or effects, creating a parallel writable authority.

### Strongest counterargument

Future exact tactical geometry might benefit from a separate record because large geometry can change independently from scene prose/state.

### Resolution

That future need does not justify an untyped current owner. If measured/mechanical requirements later prove independent tactical geometry needs its own lifecycle, admit a concrete typed owner then.

### Recommendation

Remove `STATE/TACTICAL/.gitkeep` and `scene.tactical_state_path` from active current contracts.

Owner: immediate 5.0 cleanup.

---

## F-04 — Old scalar-slot timeline survives current partial-order chronology

### Verified state

The current catalog still contains:

```text
world.timeline_marker
transition.timeline_place
event.timeline.placed
```

and `world.timeline_marker` requires `slot` and `summary`.

The historical catalog model explains the original semantics explicitly: numeric gameplay timeline slots allocated in steps of ten (e.g. `00430`, `00440`).

Current `CHRONOLOGY.md`, later Step-2 assurance and SemanticEvent schemas instead use a sparse partial order:

- causal edges;
- after edges;
- local scene order/frontiers;
- optional time only when material;
- globally reconciled sparse frontier;
- independent events may remain unordered.

### Risk

Leaving the marker class registered invites 5.9 to reconstruct a global sortable timeline and makes numeric slot order appear authoritative.

### Strongest counterargument

A named historical marker can be useful for lore (“before coronation”, “after siege”).

### Resolution

A useful named historical proposition/era does not require the old scalar gameplay ordering owner. Lore facts can carry chronology qualifiers; events carry ordering evidence. A future named chronology-anchor abstraction may be admitted only if a concrete need survives 5.9, without reusing `world.timeline_marker` semantics.

### Recommendation

Retire `world.timeline_marker`, `transition.timeline_place` and `event.timeline.placed` from the active catalog. Do not silently repurpose the old ID.

`transition.event_time_advance` / `event.event_time.advanced` are a different question and remain quarantined for 5.9 because event-local quantitative advancement still has concrete requirements.

Owner: immediate 5.0 catalog cleanup after approval.

---

## F-05 — `CURRENT.pending_global_consequences` is a generic pending-work bag

### Verified state

`current_state.schema.yaml` and template CURRENT contain:

```text
pending_global_consequences: array[object]
```

No lifecycle, identity, idempotency, trigger, owner, payload contract or consumer is defined in current CORE.

Accepted newer architecture has concrete owners for:

- owner-local scheduled triggers;
- delayed recovery;
- RuntimeCommand pending child descriptors;
- suspended Resolution/Continuation;
- world process/entity state;
- chronology causal links;
- noncanonical Dramaturg preparation.

Step 2 explicitly rejected a generic ScheduledJob/scheduler owner and Step 3 rejected a generic job/obligation runtime class.

### Strongest counterargument

The field might provide a convenient home for rare world-scale delayed consequences not naturally attached to a single Effect/Resource/Procedure.

### Resolution

Convenience is exactly the contamination risk. A concrete world-scale process with independent state deserves a real world/process owner or a future explicitly justified class. A generic array cannot safely decide recovery/idempotency.

### Recommendation

Remove `pending_global_consequences` from current-state schema/template. Later slices must represent proven pending work through actual owners.

Owner: immediate 5.0 cleanup.

---

# 5. Pointer/frontier duplication findings

## F-06 — latest checkpoint pointer is triplicated

Current active template/schema surfaces can contain:

```text
MANIFEST.last_checkpoint_id
STATE/CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml -> checkpoint_id/path/valid_through_event_id
```

`STORAGE.md` already speaks normatively about **MANIFEST checkpoint pointers** and tells runtime not to touch them unless a checkpoint changes. `SESSION.md`/bootstrap already read MANIFEST during campaign selection/startup.

Checkpoint records themselves are explicitly recovery projections, not current state.

### Options considered

A. `CHECKPOINTS/LATEST.yaml` sole owner.
- Pro: checkpoint-domain locality; can store path.
- Con: adds an extra mutable file/read even though MANIFEST is already mandatory; contradicts current STORAGE wording; duplicates campaign metadata.

B. `CURRENT.last_checkpoint_id` sole owner.
- Pro: CURRENT is already recovery/routing state.
- Con: checkpoint availability is campaign-level recovery metadata, not scene/current-world routing; bootstrap reads MANIFEST first; current STORAGE says MANIFEST.

C. **MANIFEST.last_checkpoint_id sole pointer** (recommended).
- Pro: matches current normative wording; always-loaded campaign metadata; one pointer; checkpoint path convention/index can be defined in 5.7.
- Con: MANIFEST remains mutable for recovery metadata, though this is already accepted current behavior.

### Recommendation

Keep `MANIFEST.last_checkpoint_id` as the one active latest-checkpoint pointer pending 5.7. Retire:

- `CURRENT.last_checkpoint_id`;
- `CHECKPOINTS/LATEST.yaml` from the new template.

5.7 must define deterministic checkpoint path lookup/index and migration for legacy pointer files.

This is an ownership cleanup, not the final checkpoint protocol.

---

## F-07 — current world chronology frontier is duplicated in MANIFEST and CURRENT

Current MANIFEST has:

```text
world_time:
    calendar_id
    frontier
```

CURRENT also has:

```text
world_time:
    frontier
    display
```

Current `CHRONOLOGY.md` explicitly identifies `CURRENT.world_time.frontier` as the sparse globally reconciled chronology frontier.

`MANIFEST.world_time.calendar_id` is configuration; the mutable frontier is current state/recovery routing.

### Recommendation

Retire `MANIFEST.world_time.frontier`; keep calendar configuration in MANIFEST and current chronology frontier in CURRENT. Step 5.1/5.9 will refine its exact semantics.

Owner: immediate 5.0 cleanup after approval.

---

## F-08 — global `last_event_id` is duplicated and semantically undernamed

Both MANIFEST and CURRENT currently contain `last_event_id`.

A global event cursor can be useful as storage/recovery metadata, but it must **not** imply fictional total chronology merely because event IDs allocate sequentially.

Current docs do not establish two independent meanings for the duplicate fields.

### Recommendation

For contamination control, treat `CURRENT.last_event_id` as the only provisional global LOG/recovery cursor because CURRENT already owns current routing/frontier metadata; retire `MANIFEST.last_event_id` from current new-campaign schema/template.

Step 5.1/5.9 must decide the final name/semantics (e.g. published semantic-log frontier versus chronology frontier). Until then, downstream design must not interpret this ID as “fictionally latest event.”

Confidence: **MEDIUM-HIGH**; final cursor naming/shape is intentionally deferred.

---

# 6. Registered Step-5 runtime classes that prematurely look canonical

## F-09 — `runtime.dirty_record`

### Origin

The historical mechanical runtime proposal introduced a physical SQLite `dirty_records` table tracking HOT/canonical divergence, reasons and dependency edges.

Current catalog still registers `runtime.dirty_record` with target-key identity and `CATALOG_CONTRACTS.md` calls it the owner of dirty/publication status.

There is no current dedicated machine-state schema for it.

### Architectural challenge

Does dirtiness need independently addressable identity/lifecycle?

Current accepted transport can derive a dirty set from:

- authoritative hot record state;
- pinned durable frontier;
- local mutation bookkeeping;
- publication closure.

A `dirty_record` may be useful implementation metadata, but that does not prove it is an independent `runtime.*` record under the catalog class-admission rule.

### Recommendation

Retire `runtime.dirty_record` from the active runtime-record catalog now. Step 5.5 may use an embedded/working-set dirty entry. Re-admit an independent runtime class only if 5.5 proves cross-boundary addressing/lifecycle that cannot be represented by the owning hot record + embedded bookkeeping.

This avoids designing 5.5 around an inherited SQLite table.

---

## F-10 — `runtime.publication_batch`

### Origin

The historical proposal introduced a SQLite `publication_batches` table for prepared/acknowledged/blocked batches and published event frontier.

Current PERSISTENCE semantics instead say:

```text
prepare complete transaction snapshot
-> build tree
-> ref check
-> commit
-> non-force ref advance
```

If the ref does not advance, no campaign canon changed. If it advances, Git commit/ref is durable evidence. An unreachable commit object after a race is acceptable and does not require a campaign record to explain it.

There is no current dedicated machine-state schema for `runtime.publication_batch`.

### Strongest counterargument

A stable batch ID could simplify retry diagnostics, host acknowledgements and crash recovery around publication.

### Resolution

That benefit must be proven by 5.6 against actual failure windows. Registering an independent lifecycle now biases the design before the failure analysis.

### Recommendation

Retire `runtime.publication_batch` from the active runtime-record catalog. Keep publication planning/manifest data as embedded transport state. Re-admit a record only if 5.6 proves independent durable identity is required.

`value.publication_manifest` is likewise not authority; its exact typed shape is quarantined to 5.6.

---

## F-11 — `runtime.id_allocator` is different and should remain

Although no dedicated state schema exists yet, its independent authority has already been accepted by ID/promotion contracts:

```text
campaign-allocator
    last_allocated by policy
```

Allocation and durable record creation are one atomic publication closure; concurrent unpublished conflicts can rekey local records, but published IDs never change/reuse.

This is a concrete independent campaign operational owner, not merely an inherited SQLite table.

### Recommendation

KEEP `runtime.id_allocator`. Step 5.2/5.6 owns its durable placement and recovery/atomic publication details.

---

## F-12 — `runtime.checkpoint`, `runtime.session`, `runtime.message`

These classes should not be removed merely because later contracts remain incomplete:

- checkpoint has a concrete GAME schema and independent recovery descriptor identity;
- session has a concrete coordination/recovery schema and campaign-scoped lifecycle;
- message has a concrete Step-3/Step-4 need for raw-message/transcript reference identity even though exact schema/retention remains 5.11.

Required quarantine semantics:

```text
runtime.session
    coordination/recovery evidence; never campaign HEAD authority

runtime.message
    retained discourse/evidence candidate; never truth/knowledge authority

runtime.checkpoint
    immutable recovery projection; never mutable world/runtime owner
```

---

# 7. Accepted owners with missing durable placement / recovery enumeration

This is the largest legitimate Step-5 carry-forward.

The repository currently has Step-3 machine-state schemas for Command, Resolution, Procedure and Continuation but the campaign template/manifest does not yet expose a dedicated, approved durable runtime-record storage route. `STATE/TACTICAL` is not a valid substitute.

Cold recovery must eventually discover the bounded set of active:

- commands/root closures as necessary;
- procedures;
- resolutions/continuations;
- pending mandatory children;
- fixed RNG and idempotency state;
- temporal owner bindings;
- live routing.

The audit deliberately does **not** choose whether those records ultimately live under a new runtime root, under structured STATE subroots, checkpoint-addressed paths, or another bounded placement.

Ownership is already settled; placement/enumeration belongs to:

- 5.2 Resumable Runtime Closure;
- 5.3 Temporal & pending-obligation continuity;
- 5.7 Checkpoint/recovery protocol.

Invariant for later slices:

> recovery placement may reference or enumerate these owners, but may not copy their mutable state into a second generic snapshot authority.

---

# 8. Live-scene Step-4 handoff contamination

`live_scene.schema.yaml` currently includes generic structures such as:

```text
live_facts[].known_by_pc_ids
observable_events[].perceived_by_pc_ids
pending_durable_events: array[object]
```

Step 4 has since established:

- `world.knowledge` as sole durable current fictional epistemic owner;
- `runtime.disclosure` as separate human exposure authority;
- SemanticEvent/Story separation.

Therefore:

- live perception/knowledge fields may be temporary operational evidence needed for concurrent Masters;
- they do not become alternate durable `world.knowledge` owners after compaction;
- `pending_durable_events` cannot become a generic durable pending-work queue.

Exact typed compaction belongs to 5.8 plus deferred Step-4 machine realization.

5.0 recommendation: preserve the fields only under explicit **operational/evidence quarantine**; later 5.8 must either type/route them to the accepted owners or remove them.

---

# 9. Session/preparation and context-loss findings

## 9.1 Maintenance continuation frame

`SESSION.md` already defines a minimal current-chat continuation frame for known maintenance interruptions. It is explicitly:

- current-chat working state;
- not campaign canon;
- not a checkpoint;
- not automatically a Git write reason.

This is not a second recovery authority. It is evidence used when the same chat survives maintenance.

The user requirement for restart/new-chat continuity is broader and belongs to 5.2/5.4: a durable semantic resume point must not rely on this ephemeral frame.

## 9.2 Preparation

`SESSION.md`/`CAMPAIGN_OPERATIONS.md` say to retain useful/plausible next-horizon prep, while `PREP.md` explicitly says unrevealed provisional preparation can be thrown away and only persisted objective world state is canon.

After Step 4, preparation is Dramaturg noncanonical output and retention/cache policy belongs to Step 6.

5.0 classification:

```text
Dramaturg preparation = noncanonical working/cache material
```

“retain” must never be interpreted as “promote to campaign current authority.” No new preparation owner is added in Step 5.

---

# 10. Scene-local generic facts

`scene.schema.yaml` includes:

```text
environment.transient_facts: array[object]
```

This may be intended for bounded non-independently-addressed scene-local facts, but its untyped semantics could also become a catch-all that duplicates assets/effects/lore/world state.

5.0 does not have enough evidence to delete it safely because concrete scene-local facts may legitimately belong to the Scene owner when they have no independent identity.

Disposition:

- mark as **AMBIGUOUS / NOT A GENERIC CANON ESCAPE HATCH**;
- 5.2 must classify what scene-local state is necessary for resumability;
- Step 6 catalog-gap/final holistic review must require typed semantics or retirement before implementation relies on it.

---

# 11. `transition.event_time_advance` and event-local time

Do not conflate this with obsolete scalar timeline markers.

The engine has concrete requirements for:

- `activity.wait`;
- `op.advance_local_time`;
- quantitative elapsed evidence;
- cross-scene reconciliation.

Therefore `transition.event_time_advance` / `event.event_time.advanced` may still represent a useful deterministic transition/event surface. Their exact scope is not established strongly enough for 5.0 to retire or canonize them.

Disposition: **QUARANTINE TO 5.9**. They may not be treated as permission for a universal campaign clock.

---

# 12. Analytical challenge

## 12.1 Strongest counterargument: leave all placeholders until their dedicated slices

Argument:

- deleting fields/classes now may create churn;
- later slices may discover a use for them;
- current architecture is still not implemented broadly, so placeholders cannot cause a production bug yet;
- preserving names gives later designers options.

Assessment:

This is attractive locally but weak globally. The project has already observed that an available registered entity can silently become a premise for later design. A placeholder in a closed catalog or copied campaign template is not neutral: it advertises legitimacy.

The correct distinction is not “delete everything undecided.” It is:

```text
accepted owner with later placement -> KEEP
untyped placeholder that claims an owner -> RETIRE
future concept with real requirement but unresolved shape -> QUARANTINE / named later slice
```

This preserves options without contaminating ownership.

## 12.2 Simplest alternative: documentation-only authority ledger

Alternative:

- write this audit;
- change no active machine/template/CORE surfaces;
- tell later slices to ignore bad fields/classes.

Why not recommended:

- `init_campaign.py` physically copies SECRETS/TACTICAL/LATEST into new campaigns;
- closed catalog IDs remain discoverable as accepted engine vocabulary;
- stale live paths are active runtime instructions;
- duplicate pointer fields remain writable by schemas.

A ledger alone does not remove the affordance that caused the earlier Chapter leak.

## 12.3 Risk of overreach

The opposite failure is deleting an abstraction merely because its final storage format is not designed.

This is why the audit explicitly retains:

- Procedure/Resolution/Continuation;
- id allocator;
- checkpoint/session/message identity;
- live epoch authority;
- chronology/event-local time requirements;
- scene-local fact question;
- Step-4 knowledge/disclosure owners.

5.0 must not decide their Step-5 wire format.

## 12.4 Restart with no chat memory

After removing generic placeholders, a cold recovery still has all accepted semantic owners. What is missing is an enumeration/placement contract — explicitly owned by 5.2/5.7.

Therefore retirement of `TACTICAL` and generic pending bags does not reduce a defined recovery guarantee; it prevents later recovery from using an undefined duplicate owner.

## 12.5 Stale campaign HEAD + live epoch

The live epoch remains legitimate operational authority. `runtime.session.base_head_sha` and local cached heads are evidence/caches, not authority; a stale session must refresh/adopt the actual live/campaign frontier according to live/multiplayer rules.

No new authority is required in 5.0.

## 12.6 Suspended command + RNG + due trigger

Accepted Step-3/Step-2 owners already exist. The audit confirms that a future recovery closure must reference/hydrate them; it must not reconstruct them from checkpoint prose, Agenda, TACTICAL snapshot or generic pending-consequence bag.

## 12.7 Story/transcript mismatch

Story remains projection. Message/transcript retention may preserve exact wording even when semantic state is elsewhere. This is a 5.10/5.11 retention/catch-up question, not a reason to give Story or session records current-state authority.

---

# 13. Proposed 5.0 cleanup set

Subject to architecture approval, the targeted active cleanup should be limited to already-proven contamination:

### Current runtime/docs/template

1. normalize current live path to `LIVE/LIVE_STATE.yaml` in active CORE docs;
2. remove `GAME/CAMPAIGN/WORLD/SECRETS/.gitkeep`;
3. remove `GAME/CAMPAIGN/STATE/TACTICAL/.gitkeep`;
4. remove `scene.tactical_state_path` from current scene schema;
5. remove `CURRENT.pending_global_consequences` from schema/template;
6. remove `CURRENT.last_checkpoint_id`;
7. remove `CHECKPOINTS/LATEST.yaml` from new template;
8. remove `MANIFEST.world_time.frontier` while retaining calendar config;
9. remove `MANIFEST.last_event_id`, retaining CURRENT's provisional LOG cursor until 5.1/5.9;

### Active catalog vocabulary

10. retire `world.timeline_marker`;
11. retire `transition.timeline_place`;
12. retire `event.timeline.placed`;
13. retire `runtime.dirty_record`;
14. retire `runtime.publication_batch`;
15. remove corresponding identifier policies/structure entries/schema requirements/tests and bump catalog version coherently;
16. update current normative inventory/contracts to make retirement and remaining class classifications explicit.

### Explicit quarantines, not deletions

17. `value.publication_manifest` -> 5.6;
18. `transition.event_time_advance` / `event.event_time.advanced` -> 5.9;
19. live knowledge/perception/pending-durable staging -> 5.8 / Step-4 implementation alignment;
20. scene `environment.transient_facts` -> 5.2 + Step-6 gap/final audit;
21. runtime.message schema/retention -> 5.11;
22. runtime operational storage placement/enumeration -> 5.2/5.7;
23. Dramaturg prep retention -> Step 6.

No new runtime class is introduced in 5.0.

---

# 14. Material decision analysis

Most cleanup items are direct consequences of already-approved architecture and do not require a new product semantic decision.

Two grouped changes are sufficiently structural to warrant explicit owner review before mutating the active closed catalog/template:

### Decision A — contamination retirement policy

Recommended principle:

> A registered/catalogued/template abstraction that claims semantic ownership but has no surviving accepted owner contract should be retired from the active surface now. A later slice may explicitly re-admit a new/old concept only after proving independent identity/lifecycle and defining its authority.

This principle supports retiring the old timeline marker, generic tactical/pending containers, Secret root, dirty-record and publication-batch classes rather than merely labeling them “ignore for now.”

### Decision B — single latest-checkpoint pointer

Recommended owner:

```text
MANIFEST.last_checkpoint_id
```

Retire CURRENT duplicate and `CHECKPOINTS/LATEST.yaml`; 5.7 defines deterministic path/index semantics.

Rationale: this matches current normative STORAGE wording and avoids a new mutable pointer file.

Neither decision selects Step-5 frontier/recovery wire formats.

---

# 15. Research verdict

Verified facts:

- current authority boundaries from Steps 2–4 are mostly coherent;
- the audit found real active leaks, not merely historical documentation;
- several leaks are copied into every new campaign by the init tool;
- the old scalar timeline model is still registered despite a newer partial-order chronology contract;
- two SQLite-era runtime record classes remain registered without current dedicated state schemas and before their Step-5 lifecycle has been designed;
- accepted Step-3 operational owners still lack durable placement/enumeration, exactly as Step 3 intended Step 5 to solve.

Recommendation:

1. adopt the contamination-retirement principle;
2. use MANIFEST as sole latest-checkpoint pointer pending 5.7;
3. retire only the proven obsolete/duplicate surfaces listed in §13;
4. quarantine later-slice concepts rather than guessing their final form;
5. after cleanup, run an independent adversarial review specifically against lost capability/recovery regressions;
6. stop after Step 5.0 summary/review; do not begin 5.1.

Confidence: **HIGH**.

Evidence that would change the recommendation:

- a current normative contract demonstrating an independent lifecycle/consumer for `STATE/TACTICAL`, `pending_global_consequences`, `runtime.dirty_record`, or `runtime.publication_batch` that cannot be expressed by accepted owners/embedded transport state;
- a current chronology requirement that materially requires global scalar timeline slots;
- a current bootstrap/recovery contract proving `CHECKPOINTS/LATEST.yaml` is authoritative rather than duplicate convenience;
- a recovery requirement that cannot discover required state without one of the proposed retirements and cannot be met by the explicitly assigned later slices.
