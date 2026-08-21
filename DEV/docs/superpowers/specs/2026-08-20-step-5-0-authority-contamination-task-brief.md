# Step 5.0 — Authority / Contamination Audit Task Brief

Status: **ARCHITECTURAL RESEARCH BRIEF**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Parent agenda:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

Process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Classification: **Architectural / deep-work**.

This brief is solution-blind. Its purpose is to expose the actual current ownership graph and contamination risks before Step 5.1 or any later Step-5 design is allowed to rely on persistence/recovery abstractions inherited from early project phases.

---

## 1. Problem statement

Steps 1–4 materially changed HDM ownership, execution, temporal, knowledge and Story architecture. Several persistence/multiplayer/session contracts predate those decisions. A stale concept that remains active can leak into later architecture and acquire accidental authority even if nobody explicitly chooses it.

Recent examples include catalog/world concepts whose continued registration made them available as building blocks after their intended semantics had changed. Step 5.0 exists to prevent the same failure mode in durability, recovery, runtime continuity, multiplayer/live state, chronology, Story persistence and retention.

The audit must answer:

> Which current concepts are true semantic authorities, which are projections/evidence/caches/transport state, which are ambiguous or duplicated, which gameplay-significant state lacks an explicit durable owner, and which early abstractions must be retired or quarantined before Step 5.1?

---

## 2. Scope

Audit all active architecture/runtime concepts that can affect Step 5, including at least:

### 2.1 Canonical/current state

- campaign/world/entity state;
- `STATE/CURRENT`;
- current scene/thread/location routing;
- runtime operational records from Step 3;
- Procedure state;
- Continuation state;
- live scene operational state;
- Step-4 lore/knowledge/disclosure owners where persistence affects them.

### 2.2 Pending/future work

- Effect intrinsic TemporalBindings;
- Effect scheduled-trigger state;
- delayed Resource recovery;
- LifeState recovery;
- pending mandatory child invocations;
- suspended Resolution/Continuation state;
- Choice/Reaction state;
- pending global consequences;
- live compaction/rollover state;
- Story projection work;
- disclosure delivery/persistence work.

### 2.3 Frontiers/evidence/projections

- campaign Git HEAD/tree/known frontier;
- dirty HOT/SOFT state;
- checkpoints and checkpoint pointers;
- SemanticEvent/LOG;
- MechanicalEvent/receipts/traces;
- local/global chronology frontiers;
- live branch/head/blob/revision metadata;
- Story records/indexes/source refs;
- transcript/session records;
- maintenance/session continuation frame;
- ResolvedCatalogContext/runtime identity where recovery depends on it.

### 2.4 Derived/runtime-only structures

- Temporal Agenda;
- MechanicalContext;
- dependency DAG/cache;
- Condition/Effect arbitration/aggregation indexes;
- knowledge/reverse-reference indexes;
- Context Assembler bundles/source manifests;
- loaded-record caches;
- working-set frontier caches;
- ID allocator/reservation state.

### 2.5 Transport/authorization metadata

- campaign branch transaction state;
- live CAS state;
- authenticated PLAYER binding/routing evidence;
- campaign creator/access metadata where stale state may affect publication/recovery;
- storage/runtime package identity needed for exact recovery.

---

## 3. Out of scope

Step 5.0 SHALL NOT:

- choose the final unified frontier representation; that is Step 5.1;
- design the final Resumable Runtime Closure payload; that is Step 5.2;
- design final temporal/pending-work persistence; that is Step 5.3;
- redesign SOFT/HARD policy; that is Step 5.5;
- redesign Git publication transport; that is Step 5.6;
- redesign checkpoint format; that is Step 5.7;
- redesign multiplayer/live state machine; that is Step 5.8;
- redesign chronology representation; that is Step 5.9;
- design Story persistence formats; that is Step 5.10;
- design transcript retention; that is Step 5.11;
- design host delivery acknowledgement; that is Step 5.12;
- design GC policy; that is Step 5.13;
- decide physical LLM call topology; that remains Step 6;
- implement schemas/runtime code.

If an inconsistency cannot be corrected without making a later-slice design decision, 5.0 must identify it precisely and assign it to that slice rather than guessing the later solution.

---

## 4. Fixed constraints / accepted decisions

The audit treats these as constraints unless contradiction evidence forces an explicit superseding decision:

- exactly one long-lived durable campaign branch;
- temporary `live/*` branches only for shared-scene concurrency;
- no long-lived spectator/public branch;
- no force-push recovery;
- domain/world/runtime current-state owners remain current authority;
- checkpoints are sparse recovery frontiers, not alternate world snapshots;
- LOG/MechanicalEvents are history/evidence, not alternate current state;
- Temporal Agenda is a disposable derived index and owns no deadline;
- owner-local TemporalBindings/scheduled trigger state own temporal obligations;
- `runtime.procedure` owns procedure-local ResourceState;
- Continuation owns one suspended Resolution generation and cannot copy Procedure state or derived caches;
- RuntimeCommand/root chain and pending child identities preserve mandatory execution closure;
- fixed RNG already generated for a still-valid experiment cannot be rerolled because of retry/recovery;
- chronology is partial-order/adaptive and Git commit order is not fictional chronology;
- `world.lore_fact`, `world.knowledge`, `runtime.disclosure` are distinct Step-4 authorities;
- Story is durable non-canonical projection/read surface;
- Chapters have no world/runtime authority;
- six LLM roles do not create new canonical state authorities;
- Context Assembler bundle/context is working evidence, not canonical state;
- repository visibility is not character/player knowledge.

---

## 5. Quality attributes

The audit must prioritize:

1. **single authority** — one writable owner per semantic fact/lifetime;
2. **recoverability** — gameplay-significant current/pending state cannot depend only on dead process/chat memory after a promised durable frontier;
3. **determinism/idempotency** — restart/retry cannot duplicate or silently drop committed/pending mechanics;
4. **bounded recovery/read cost** — avoid requiring full campaign/world/log scans to discover active obligations;
5. **multiplayer consistency** — temporary live authority must not become a competing long-term canon;
6. **chronology correctness** — persistence metadata must not accidentally define fictional ordering;
7. **projection isolation** — checkpoint/LOG/Story/transcript/index/cache must not mutate semantic authority by implication;
8. **reversibility/YAGNI** — do not introduce new generic runtime entities merely to simplify the audit;
9. **testability/observability** — authority classification and recovery dependencies must be mechanically inspectable later;
10. **implementation neutrality** — 5.0 identifies ownership defects without prematurely selecting later Step-5 wire formats.

---

## 6. Required classification model

For every material concept, classify at least:

```text
concept
semantic responsibility
scope/lifetime
current writable owner?
authority_class:
    CURRENT_AUTHORITY
    OPERATIONAL_AUTHORITY
    PENDING_OBLIGATION_AUTHORITY
    HISTORICAL_EVIDENCE
    RECOVERY_PROJECTION
    PRESENTATION_PROJECTION
    DERIVED_INDEX_CACHE
    TRANSPORT_METADATA
    AUTHORIZATION_METADATA
    EPHEMERAL_WORKING_STATE
persistence location/form today
rebuild source if derived
invalid duplication / ambiguity?
downstream consumers
failure if lost/stale/duplicated
owning later Step-5 slice if unresolved
```

The exact labels may be refined during research, but the audit must preserve the distinctions.

---

## 7. Research targets

Inspect current active branch versions of at least:

### Process/status

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`

### Canonical Steps 1–4

- Step-1/2 retrospective assurance final;
- Step-2 temporal/recovery assurance resolution;
- Step-3 canonical spec and final review;
- Step-4 canonical spec and adversarial review;
- six-role LLM draft;
- Step-5 expanded agenda.

### Runtime durability/recovery/storage

- `GAME/CORE/STORAGE.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/DURABILITY_GUARD.md`
- `GAME/CORE/SAVE_CONTRACT.md`
- `GAME/CORE/SESSION.md`
- `GAME/CORE/RUNTIME.md`
- `GAME/CORE/INTEGRITY.md`
- campaign operations/identity/runtime-selection contracts as needed.

### Multiplayer/time

- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/CHRONOLOGY.md`

### Machine schemas/catalogs

- current state/checkpoint/live/event/session schemas;
- runtime command/resolution/procedure/continuation schemas;
- temporal binding/effect/resource/life-state related schemas;
- pending-child/receipt/mechanical-event schemas;
- relevant catalog/entity/field inventories and identifier policies.

### Step-4 / Story inputs

- existing message/session/event storage contracts;
- manifest storage roots;
- any active Story-related current docs/schemas (expected mostly deferred at Step-4 closure);
- knowledge/disclosure migration obligations relevant to persistence.

External research is optional in 5.0 and should be used only if repository ambiguity cannot be resolved internally. The primary goal is consistency with HDM's own accepted architecture, not importing a persistence framework.

---

## 8. Required questions

The audit must answer at least:

1. Are there any current semantic facts with two writable owners?
2. Are there any records called `state`, `current`, `checkpoint`, `live`, `pending`, `frontier`, `event`, `session`, `cache` or `index` whose real authority differs from their apparent semantics?
3. Does `STATE/CURRENT` own anything that should live in a domain/runtime owner, or is it correctly only compact routing/hot state?
4. Does checkpoint metadata duplicate current state or runtime owners?
5. Are current runtime.command/resolution/procedure/continuation/pending-child responsibilities persistence-consistent?
6. Can mandatory pending work be discovered after restart without a full world/log scan?
7. Which gameplay-significant concepts currently survive only in process/chat memory?
8. Is Temporal Agenda correctly derivable from durable owner-local state, and are all its source obligations actually persisted somewhere?
9. Is RNG/idempotency continuity represented by an authority that survives the necessary external boundaries?
10. Does live-scene state create any ambiguous authority with campaign state or multiple live epochs?
11. Do chronology/frontier fields accidentally imply a total order or duplicate event authority?
12. Do LOG/session/transcript concepts overlap or conflict with Step-4 Story responsibilities?
13. Does any Story/Chapter legacy remain active after Chapter retirement?
14. Are Step-4 disclosure/context concepts likely to be incorrectly persisted as transcript/narration rather than their own authority?
15. Is ID allocation/reservation state safe across process loss/concurrency, or is there an unidentified durability owner?
16. Does the maintenance continuation frame represent a hidden second recovery model?
17. Are known-head/tree/dirty caches being mistaken for canonical campaign state?
18. Is runtime/package/catalog identity recoverable without environment-local paths becoming durable state?
19. Which active concepts should be explicitly retired/quarantined now?
20. Which defects must be carried to named later Step-5 slices rather than fixed in 5.0?

---

## 9. Analytical challenge requirements

Before recommendation, explicitly test:

- strongest case for leaving early runtime/storage abstractions alone until their dedicated later slice;
- simplest viable alternative: a documentation-only authority ledger with zero active-contract cleanup;
- risk that 5.0 overreaches and accidentally designs 5.1–5.13;
- risk that an apparently derived cache is actually the only place a gameplay-significant obligation survives;
- risk that a projection/frontier becomes an accidental write authority after recovery;
- restart with no chat memory;
- stale campaign HEAD + active live epoch;
- suspended command/procedure/continuation after process loss;
- due scheduled trigger across restart;
- Story/log/transcript mismatch;
- stale/missing checkpoint pointer;
- ID reserved only in RAM;
- known maintenance handoff versus abrupt crash.

State recommendation confidence and evidence that would change it.

---

## 10. Deliverables

The 5.0 cycle should produce, as warranted:

1. this Task Brief;
2. Research & Authority Inventory Draft;
3. Decision Brief only for genuinely material ownership/retirement choices not already implied by accepted architecture;
4. Candidate 5.0 Audit Resolution / authority ledger;
5. Adversarial Review;
6. Resolution Gate / final 5.0 disposition;
7. targeted active-document cleanup only where an identified abstraction is already proven wrong and its retirement does not require a later-slice design decision;
8. roadmap/status update identifying the exact Step-5 continuation point.

Historical derivation documents should not be rewritten merely because their old terminology is historically accurate.

---

## 11. Exit criteria

Step 5.0 is ready to close only when:

- every material Step-5-relevant active concept has an explicit authority classification;
- duplicate/ambiguous owners are either removed or assigned to an exact later slice with no permission for downstream designs to treat them as resolved authority;
- every gameplay-significant in-memory-only state candidate is identified and assigned to 5.2/5.3/5.4 or another exact slice;
- no old Chapter/Secret/catalog-style contamination is silently available as a valid persistence abstraction;
- no recommendation depends on unverified generic best practice;
- analytical challenge and adversarial review have been completed;
- no unresolved 5.0 architecture blocker remains;
- the owner receives a concise result summary;
- **Step 5.1 has not begun.**
