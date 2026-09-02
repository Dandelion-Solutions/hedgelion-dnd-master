# R2.7 WP-13 — Durability / SAVE / Publication — Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRED — READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-02

Task-specific Source Manifest:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief-critic.md`

Global current-progress authority:

- `DEV/CURRENT_PROGRESS.md`

Task-local R2.7 cursor:

- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`

---

## 1. Task classification and current authorization

WP-13 is an **architectural / deep-work realization audit** because it joins persistence, durability promises, optimistic publication, concurrency/currentness, access control, multi-domain SAVE composition and crash/ambiguity behavior.

Current authorization is **Step 1 only**.

This Step-1 package may establish framing, evidence routes, current-machine debt and questions for Step 2. It may not:

- perform Step-2 evidence synthesis;
- select or canonicalize a new durability architecture;
- edit runtime/schema/catalog/test implementation;
- start WP-14, WP-16 or any later R2.7 domain;
- begin implementation planning.

After this package is published and verified, the required next action is the mandatory Senior review.

---

## 2. Problem statement

Accepted HDM architecture already defines the semantic durability and publication model:

- establishment and durability are separate facts;
- `SOFT` and `HARD` describe current durability obligation, not permanent semantic classes;
- durability policy is scope-owned rather than one campaign-global save clock/frontier;
- an explicit SAVE succeeds only when the promised established dirty roots and their required recovery dependencies are **actually durable** through the applicable compatible native durability domains;
- campaign publication uses one frozen single-ref CAS-style publication attempt with bounded semantic revalidation and exact-generation adoption;
- independent native durability domains compose but do not become one distributed transaction;
- live-claimed mutable consequences establish through exact-source live CAS, not through local SQLite or a campaign-tree commit;
- checkpoint is optional recovery evidence and does not prove SAVE success;
- native owner records and required derived indexes remain separate authority classes but must be publication-coherent where the index contract requires it.

The current shipped runtime/tests do not yet realize this model uniformly. Important surfaces still encode or imply:

- a campaign-global one-hour `durable_frontier_time`;
- a campaign-centric `SAVE_ALL_DIRTY` operation that can be read as the whole SAVE contract;
- unqualified dirty clearing after publication rather than frozen owner-generation adoption;
- current one-file live implementation details that are downstream debt relative to accepted Step-5.8/WP-12 authority;
- publication language whose exact relationship to native record/index closure, authorization basis, ambiguity, partial multi-domain success and named HARD-edge owners must be reconciled.

WP-13 must define the implementation-facing **machine realization contract** that closes that gap without reopening the accepted Step-5/WP-11/WP-12 architecture merely for implementation convenience.

---

## 3. Goals

WP-13 Steps 2–8, if authorized later, must be framed to produce a canonical realization that:

1. realizes `MAY_DEFER` versus `MUST_BE_DURABLE_BEFORE(edge)` without a persistent generic HARD queue, campaign-global dirty timer or universal durability frontier;
2. realizes scope-relative unpublished-exposure/durability policy over WP-12 owner generations and native owner scopes;
3. defines how an explicit SAVE selects its promised save scope, derives the required compatible native durable closure and acknowledges success only after the entire promised closure is actually durable;
4. preserves the rule that one campaign-domain publication is one coherent base-tree delta / one gameplay commit / one non-force single-ref transition, while overall SAVE may compose additional native durability domains;
5. maps frozen owner generations/roots to exact WP-11 native paths plus every required index/projection update that must share the publication closure;
6. carries exact repository/ref/source/currentness basis, acting-principal/authorization basis, dependency/read footprint, frozen generations/fingerprints and publication reason through the campaign publication attempt;
7. defines bounded stale-HEAD, rejection and indeterminate-publication handling without blind overwrite, gameplay replay, reroll or invented success;
8. makes successful publication generation-specific: confirmed durability of generation G cannot clear or overwrite a newer G+1;
9. maps named durability/HARD edges from their actual owning contracts rather than centralizing their semantics in `DURABILITY_GUARD.md`;
10. preserves local completeness and currentness checks as bounded operations over selected roots, native direct routes and directly relevant dependencies rather than campaign/WORLD/history scans;
11. keeps checkpoint creation/recovery selection, final live-machine realization, bootstrap/migration, implementation tests and performance work with their downstream owners;
12. supplies explicit later verification obligations for WP-22 and implementation planning without performing implementation during R2.7 architecture audit.

---

## 4. Non-goals

WP-13 does **not** own or reopen:

- Step-3 ExecutionSegment semantics or runtime owner topology;
- Step-5.2 Resumable Runtime Closure semantics;
- Step-5.4 host-handoff semantics;
- Step-5.5 SOFT/HARD/SAVE semantic architecture;
- Step-5.6 campaign publication/crash-consistency semantic architecture;
- Step-5.7 checkpoint/recovery selection semantics;
- Step-5.8 live-epoch authority, claim or exact-source-CAS semantics;
- Step-5.9 fictional chronology;
- WP-10 durable record-family allocation;
- WP-11 physical route/identity/index laws;
- WP-12 HOT/SQLite transaction architecture, including the repaired local-HOT versus live-CAS establishment split;
- exact SQLite DDL/API or local database lifecycle;
- final checkpoint schema/recovery machine repair (`WP-14`);
- final live-machine realization and source-native live identity (`WP-16`);
- campaign bootstrap/scaffolding (`WP-19`);
- migration compatibility realization (`WP-20`);
- executable conformance/failure-injection implementation (`WP-22`);
- performance/index partitioning (`WP-24`);
- stale Storage-v2 prose cleanup (`WP-26`);
- release packaging or deployment transport.

Current implementation wording may be classified as debt without becoming architecture authority.

---

## 5. Accepted upstream constraints

### 5.1 Native authority and recovery closure

Step 5.2 owns Resumable Runtime Closure as a correctness property over compatible native durable sources. Required recovery closure is bounded and native-routed; it is not a global snapshot, root registry, scalar frontier or checkpoint identity.

Lost unpublished HOT/SOFT state is not invented after process/context loss.

### 5.2 Durability obligation model

Step 5.5 owns the durability semantics:

```text
established semantic state
    != necessarily durable state

SOFT
    = established + currently allowed to remain volatile/dirty

HARD for edge E
    = applicable state MUST_BE_DURABLE_BEFORE(E)
```

Durability policy is scope-owned. The accepted architecture explicitly rejects the current global `durable_frontier_time` / one-hour ceiling as canonical architecture.

A required durable closure may contain native sources that are already durable and therefore absent from the physical write set.

### 5.3 Explicit SAVE

An explicit SAVE promises actual durability of every established gameplay-significant dirty root in the selected SAVE scope plus correctness-required dependencies.

SAVE may compose multiple native durability domains. It does not imply a distributed transaction and cannot roll back an already accepted native publication merely because a later participating domain fails.

The runtime may acknowledge `saved` only when the whole promised closure is confirmed durable. A clean/equivalent scope requires no heartbeat/no-op publication.

### 5.4 Campaign publication

Step 5.6 owns campaign publication as Python-owned, frozen, single-ref CAS-style publication:

```text
pin campaign HEAD/tree
-> freeze exact owner generations + closure + authorization/currentness/dependency basis
-> derive exact path operations
-> construct resulting tree from pinned base
-> locally prove planned closure/invariants
-> revalidate ref/currentness as required
-> create one single-parent gameplay commit
-> non-force ref transition
-> classify outcome
-> adopt only confirmed exact generations
```

Publication results must distinguish confirmed acceptance, rejection and indeterminate transport. An indeterminate result is not safe to acknowledge or blindly retry.

Prepared objects/commits are not campaign authority until the ref transition is established.

### 5.5 Currentness and accepted gameplay

HEAD movement is classified against the frozen dependency/touch footprint. Proven-disjoint movement may preserve accepted IDs, RNG and semantic result while rebuilding transport/source basis. Relevant overlap requires owner-specific revalidation/re-resolution.

Publication retry is not gameplay replay.

### 5.6 Physical paths and indexes

WP-11 owns native physical routes. Known native IDs derive one deterministic route; paths/indexes never create semantic identity or currentness.

Where a current discoverable record requires an index entry, the native record and required index update share a publication closure. Index absence cannot prove semantic absence and no ordinary save may require broad directory enumeration to discover a known owner.

### 5.7 HOT generation contract

WP-12 owns local owner-generation and dirty support. Dirty bookkeeping is owner-generation-specific and scope-relative. There is no accepted campaign-global dirty generation, universal HARD queue, global save clock or persistent generic publication journal.

A frozen publication attempt is ephemeral operation state. Confirmed publication of G clears only G; G+1 remains dirty.

### 5.8 Live establishment boundary

For live-claimed mutable consequences, Step-5.8 exact-source live CAS is the authoritative establishment/durability edge. Pre-CAS state is prospective/non-current; post-CAS SQLite only adopts already accepted live authority.

WP-13 may define how an overall SAVE/HARD promise composes such a native live edge with other durability domains. It may not replace that edge with a campaign commit, local SQLite transaction or SQLite+live distributed transaction.

### 5.9 Checkpoint boundary

Step 5.7 states that checkpoint is optional immutable recovery/maintenance evidence. It may be absent from ordinary SAVE. Checkpoint existence/publication does not prove SAVE or handoff success.

WP-14 owns final checkpoint/recovery machine realization.

### 5.10 Authorization

`ACCESS_CONTROL.md` and Step 5.6 require application-level acting-principal authorization in addition to technical repository write ability. A frozen attempt must retain the required authorization basis and revalidate mutable authorization dependencies at the owning boundary.

---

## 6. Current machine-debt perimeter established during Step 1

These are **current implementation/test observations**, not new architectural decisions.

### D1 — global one-hour durability frontier

`GAME/CORE/DURABILITY_GUARD.md`, `GAME/CORE/STORAGE.md`, `GAME/CORE/RUNTIME.md`, `GAME/CORE/SESSION.md` and `DEV/TESTS/test_hourly_durability_contract.py` currently encode or enforce a campaign-global one-hour dirty durability ceiling / `durable_frontier_time`.

This conflicts with the accepted Step-5.5/WP-12 scope-relative model and is in WP-13 realization scope.

Step 1 does **not** select a replacement global timer, cadence or constant.

### D2 — campaign-centric explicit SAVE wording

`GAME/CORE/SAVE_CONTRACT.md` and `DEV/TESTS/EXPLICIT_SAVE_CASES.md` currently frame explicit SAVE primarily as `SAVE_ALL_DIRTY` followed by one campaign `CAMPAIGN_TREE_TXN`.

That is a valid description of the campaign-domain publication portion when the promise contains only campaign-domain work, but it is insufficient as the general SAVE contract because accepted Step 5.5 allows a promised closure to compose several native durability domains.

### D3 — unqualified dirty clearing

Current persistence/runtime tests and prose use phrases equivalent to “clear published dirty state.” WP-12 requires generation-specific adoption. Step 2 must locate every current machine/test surface that could incorrectly clear G+1 after publication of frozen G.

### D4 — older live implementation surfaces

`GAME/CORE/LIVE_SCENE.md` and tests such as `PERSISTENCE_TRANSACTION_CASES.md` still describe the current one-file live implementation. They are concrete consumers/debt surfaces, not permission for WP-13 to replace accepted Step-5.8/WP-12 authority with the old machine shape.

Final live realization remains WP-16.

### D5 — named edge owners are distributed

Durability semantics are not owned solely by `DURABILITY_GUARD.md`. Current named owners include at least:

- `DIEGETIC_ONBOARDING.md` — `PROVISIONAL_IDENTITY`;
- `CHARACTER_READINESS.md` — READY_PC / PLAY_READY persistence barrier;
- `SESSION.md` / Step 5.4 — controlled handoff and session/lifecycle durability;
- `MULTIPLAYER.md` / `ACCESS_CONTROL.md` — membership/authorization boundaries;
- `CAMPAIGN_HOUSE_RULES.md` — policy/grant adoption boundaries;
- explicit SAVE itself;
- current live claim/visibility edges under Step 5.8.

Step 2 must map each applicable trigger to its owner rather than inventing a centralized semantic trigger table.

---

## 7. Core questions for Step 2

If Senior authorizes Step 2, evidence extraction must answer at least:

1. Which current owner/edge contracts may defer durability, and which require durability before a named edge?
2. What exact operational metadata is necessary to evaluate those obligations over WP-12 owner generations without creating new semantic owners?
3. How are dirty roots selected for one scope, and how is correctness-required dependency closure derived without broad campaign scans?
4. For explicit SAVE, what is the selected promise scope and which native durability domains participate?
5. How does SAVE handle a participating native domain that is already durable and therefore requires no physical write?
6. How does an overall SAVE freeze/quiesce only the required scopes strongly enough to prevent promise drift while avoiding a distributed/global lock?
7. How do already-accepted native publications survive partial multi-domain SAVE failure?
8. What exact campaign publication attempt fields are required by Step 5.6, WP-11 and WP-12?
9. How are WP-11 record paths, DELETE/UPSERT operations and required index updates derived from frozen roots/generations?
10. What local completeness/integrity assertions can prove the planned resulting tree without repository-wide traversal?
11. How are acting-principal authorization and mutable authorization dependencies represented/revalidated?
12. What exact stale-HEAD cases are safely disjoint, which require owner-specific revalidation, and which make the publication attempt fail/retry?
13. What evidence distinguishes `CONFIRMED_ACCEPTED`, `REJECTED` and `INDETERMINATE` after ref-update transport ambiguity?
14. How does bounded verification determine whether an indeterminate attempt actually became current without treating an unreachable prepared commit as authority?
15. How does confirmed campaign publication adopt the new known frontier and clear only frozen owner generation G while preserving G+1?
16. How are explicit save success, HARD-edge success and ordinary deferred publication surfaced to player/host behavior without technical chatter on healthy success?
17. Which current GAME/schema/test/tool surfaces directly implement each law, which are stale pre-realization debt, and which belong to WP-14/WP-16/later work?

---

## 8. Required Step-2 evidence matrix

Step 2 must produce item-level evidence at least in this form for every applicable named durability trigger/save scope/native publication domain:

```text
trigger / named edge
-> owning semantic contract
-> established owner generation(s) / dirty roots
-> selected durability-policy scope
-> required native durable closure
-> currentness/authority source(s)
-> native publication domain / partition
-> freeze/quiescence requirement
-> frozen generation/fingerprint + auth/source/dependency basis
-> exact native path delta + required-index closure
-> publication protocol/outcome classes
-> disjoint/overlap/ambiguity handling
-> success / partial-success / failure postcondition
-> generation-specific local adoption/dirty clearing
-> player-visible acknowledgement rule
-> current implementation/schema/test evidence or debt
-> downstream owner when outside WP-13
```

A coverage claim requires item-level accounting or an equally strong mechanically verifiable mapping.

---

## 9. Components and ownership boundaries

| Concern | Existing owner | WP-13 relationship |
|---|---|---|
| ExecutionSegment / accepted mechanics | Step 3 | consume only; no replay/redefinition |
| Recovery closure semantics | Step 5.2 | consume bounded closure law |
| Controlled handoff | Step 5.4 | consume durability-success promise |
| SOFT/HARD/SAVE semantics | Step 5.5 | machine realization target; semantics closed |
| Campaign publication/crash consistency | Step 5.6 | machine realization target; semantics closed |
| Checkpoint/recovery | Step 5.7 / WP-14 | preserve boundary; defer machine repair |
| Live claims/CAS | Step 5.8 / WP-16 | compose native durability edge; do not redesign |
| Native record families | WP-10 | consume owner allocation |
| Native routes/indexes | WP-11 | realize publication closure/path delta |
| HOT owner generations | WP-12 | consume dirty/frozen-generation/adoption laws |
| Access/acting principal | `ACCESS_CONTROL.md` | carry/revalidate existing authorization basis |
| Publication transport machine | `PERSISTENCE.md` + later implementation | reconcile against closed architecture |
| Boundary classification runtime | owner modules + `DURABILITY_GUARD.md` | realize routing/evaluation without centralizing semantics |
| Explicit save runtime | `SAVE_CONTRACT.md` | reconcile campaign-only wording with native-domain composition |
| Integrity preflight | `INTEGRITY.md` | preserve bounded directly-touched validation |
| Tests/maintenance audit | `DEV/TESTS/`, `DEV/TOOLS/` | evidence/debt now; implementation later WP-22 |

---

## 10. Conceptual operation values — no new semantic owners

Step 2 may evaluate implementation-facing typed **ephemeral operation values** such as the following, but Step 1 does not authorize persistent generic records:

### Durability evaluation

May conceptually carry:

```text
edge/reason
policy scope
selected owner generations
required durable roots/dependencies
native domain disposition
```

It is an evaluation/result, not a semantic owner or queue.

### Frozen campaign publication attempt

Already required by Step 5.6/WP-12 and may conceptually carry:

```text
repository/ref
acting principal + authorization basis
pinned HEAD/tree/source basis
frozen owner generations/fingerprints
durability roots / dependency footprint
exact path UPSERT/DELETE operations
publication reason/edge
```

It remains ephemeral and immutable for one attempt.

### SAVE operation composition

An explicit SAVE may require ephemeral composition state describing participating native domains and whether each promised closure component is already durable, confirmed accepted, rejected or still indeterminate.

Such composition state is not a distributed transaction, recovery frontier, gameplay owner or persistent publication journal.

---

## 11. Critical flows to preserve

### 11.1 Ordinary local SOFT accumulation

```text
accepted local semantic edge
-> local HOT establishment allowed by owner contract
-> owner generation becomes dirty/exposed in its policy scope
-> no applicable durability obligation fires
-> continue without repository I/O
```

No global elapsed-time scalar is assumed by architecture.

### 11.2 Named HARD edge

```text
owning module establishes MUST_BE_DURABLE_BEFORE(edge)
-> select only implicated policy scope / owner generations
-> derive required compatible native durable closure
-> publish/verify required native domain(s)
-> edge may cross only after required durability is confirmed
```

The owner defines **why/when** the edge is HARD; WP-13 realizes the shared machinery for evaluating and satisfying the obligation.

### 11.3 Campaign-domain publication

```text
frozen generation/closure
-> derive WP-11 native path delta + required indexes
-> local bounded integrity/result-tree proof
-> exact currentness/auth revalidation
-> one single-parent campaign commit
-> non-force ref transition
-> classify result
-> adopt confirmed source basis / exact frozen generations only
```

### 11.4 Explicit SAVE across native domains

```text
explicit SAVE promise
-> freeze selected SAVE scope
-> derive required native durable closure
-> classify each participating native domain
-> satisfy/verify each domain under its own publication protocol
-> preserve every independently accepted native publication
-> overall SAVE succeeds only when complete promised closure is confirmed durable
```

No distributed rollback is introduced.

### 11.5 Live-owned mutable consequence

```text
prospective live consequence
-> exact-source live CAS native durability edge
-> confirmed accepted live authority
-> local HOT adoption
```

A campaign save may later compact/absorb live state only through the accepted live/campaign lifecycle. WP-13 cannot substitute a campaign-tree write for live authority.

---

## 12. Required scenarios

Step 2 and later candidate review must preserve at least these scenarios:

1. several ordinary singleplayer turns accumulate SOFT owner generations with zero GitHub writes;
2. one named HARD edge flushes only the required scope plus required recovery dependencies, not every dirty campaign fact by default;
3. explicit SAVE with only campaign-domain dirty state uses one coherent campaign publication and no forced checkpoint;
4. explicit SAVE with campaign + independent native live/other durability participation composes native outcomes and acknowledges only complete promised durability;
5. one participating native domain is already durable and causes no heartbeat/no-op write;
6. campaign HEAD moves disjointly after preparation; accepted IDs/RNG/semantics survive while publication basis is rebuilt;
7. campaign HEAD moves over a relevant dependency; the attempt is revalidated/re-resolved under the owning contract rather than blindly merged;
8. ref update succeeds remotely but response is indeterminate; bounded verification prevents duplicate gameplay publication and false `saved` acknowledgement;
9. frozen generation G publishes while local G+1 is created; G+1 remains dirty;
10. required native record and its WP-11 discovery index update remain publication-coherent;
11. current index is stale/malformed but native records are valid; save does not treat index absence as semantic absence and rebuild/repair follows the derived-index contract;
12. `PROVISIONAL_IDENTITY` durability succeeds while campaign remains `initializing`;
13. READY_PC/PLAY_READY edge cannot cross until the required committed character closure is actually durable;
14. membership or House-Rule authorization changes are not accepted merely because repository write permission exists;
15. checkpoint is absent during an otherwise valid explicit SAVE; SAVE may still succeed;
16. partial multi-domain SAVE publishes one native domain and then another domain rejects; accepted first-domain durability remains real, overall SAVE remains incomplete and no rollback/replay occurs;
17. lost unpublished local state after context destruction is not invented from narration, Story or expected player intent;
18. current old one-hour test/runtime policy is classified and removed/replaced only through accepted scope policy, not preserved as an accidental global architecture law.

---

## 13. Quality attributes / fitness criteria

The eventual WP-13 result must optimize for:

- **correctness** — never acknowledge durability that was not actually established;
- **determinism/idempotency** — publication retry cannot duplicate accepted mechanics, IDs, events or RNG;
- **boundedness** — ordinary save/publication preflight scales with selected dirty/required closure, not total campaign/history size;
- **concurrency safety** — stale/ambiguous ref outcomes are classified without force overwrite;
- **authority preservation** — storage/SQLite/index/checkpoint/session metadata do not become semantic owners;
- **latency** — ordinary SOFT turns remain zero-I/O when no durability obligation fires;
- **recoverability** — promised durable closure is sufficient for honest native recovery;
- **authorization** — technical repository capability never substitutes for HDM application authority;
- **testability** — each publication/result/dirty-generation invariant admits focused deterministic/failure-injection verification;
- **evolvability** — no global timer/frontier/journal schema is introduced merely to simplify current implementation.

No new numerical latency/cadence target is invented by this Step-1 package.

---

## 14. Risks and challenge points

### R1 — central durability scheduler accidentally becomes semantic authority

A generic timer/queue/frontier can erase owner-local policy and reintroduce the rejected global model.

Mitigation: machine values remain scope-relative operational metadata/evaluation; trigger semantics stay with owning contracts.

### R2 — campaign transaction mistaken for whole SAVE

One campaign publication is atomic only inside its native campaign ref; explicit SAVE may promise multiple native durability domains.

Mitigation: distinguish campaign-domain transaction from overall SAVE composition and acknowledgement.

### R3 — partial multi-domain success mishandled as rollback

Already accepted native state cannot be undone by a later domain failure.

Mitigation: record/verify native outcome independently; overall promise fails incomplete without gameplay rollback/replay.

### R4 — broad completeness scan destroys boundedness

“Save all state” can be misimplemented as repository/world traversal.

Mitigation: begin from established dirty/native roots, WP-11 direct routes and correctness-required dependency closure only.

### R5 — stale authorization survives preparation

Publication could be technically valid but application-unauthorized.

Mitigation: freeze authorization basis and revalidate mutable authorization dependencies at the owner-required pre-mutation boundary.

### R6 — prepared/unreachable Git objects treated as canon

Commit/tree creation is not authority before the ref transition.

Mitigation: result classification and bounded lineage/current-state verification.

### R7 — G publication clears G+1

Asynchronous local progress can be lost if dirty state is cleared by path rather than frozen generation.

Mitigation: exact generation/fingerprint adoption law from WP-12.

### R8 — old live implementation reopens closed authority

Current one-file live prose/tests may appear more concrete than Step-5.8.

Mitigation: classify it as implementation/debt evidence; final live realization stays WP-16.

### R9 — checkpoint sneaks into SAVE proof

Current session prose can make checkpoint appear adjacent to save/session boundary.

Mitigation: Step-5.7 boundary is explicit: checkpoint optional, separate purpose, never SAVE proof.

---

## 15. Research / spikes

No external research or technology-selection spike is currently required for Step 2.

Reason: current HDM canonical architecture already determines the authority, concurrency and durability semantics strongly enough. The present work is primarily repository evidence extraction, machine-contract reconciliation and bounded implementation-facing formalization.

A later spike is justified only if Step-2 repository evidence exposes an implementation feasibility uncertainty not answerable from current Git/host contracts. Such a spike would produce evidence, not silently reopen accepted architecture.

---

## 16. Decision rights

### Already settled; agent must not escalate merely for convenience

- native owners and RRC;
- SOFT/HARD/SAVE semantic model;
- no global durability frontier/timer as architecture;
- campaign single-ref non-force publication architecture;
- native multi-domain composition without distributed transaction;
- exact-source live CAS authority;
- generation-specific dirty adoption;
- checkpoint optionality/non-authority;
- WP-11 path/index authority rules;
- WP-12 local-HOT/live-CAS split.

### Agent-owned mechanical work

- complete source discovery/extraction;
- current-machine debt classification;
- exact field/flow/verification formalization implied by closed architecture;
- traceability and downstream routing;
- repair of wording/coverage omissions that introduce no new product or authority choice.

### Human-owned only if Step 2 exposes a genuine residual choice

Escalate only if evidence leaves a material unresolved choice involving product semantics, durability promise, compatibility policy, authority ownership, hard-to-reverse scope or explicit material risk acceptance.

At Step-1 completion:

**Human decision required: NO.**

---

## 17. Source Manifest and evidence-completeness gate

The task-specific Source Manifest is the companion artifact listed at the top of this brief.

Before any Step-2 synthesis/Decision Brief, the worker must:

```text
[ ] inspect every REQUIRED STEP-2 source to the stated depth;
[ ] preserve every relevant enumerated law/finding/qualifier;
[ ] classify current GAME/schema/test surfaces as conforming, stale debt, supporting evidence or downstream-owned;
[ ] map every named durability edge to its actual owner;
[ ] account for WP-11/F02 and WP-12 -> WP-13 forward obligations explicitly;
[ ] prove that no conclusion depends only on summaries/roadmaps/search snippets;
[ ] keep checkpoint/live/bootstrap/migration/test/performance boundaries with their owners;
[ ] identify any genuine contradiction/new consumer/insufficiency before proposing to reopen a closed decision.
```

Step 2 must not assume that the manifest is a closed-world list; newly discovered direct/indirect consumers must be added before synthesis.

---

## 18. Step-1 whole-project critic outcome

The mandatory critic found two `BLOCKING` and eight `SIGNIFICANT` framing defects in the initial framing. All were mechanically repairable from existing accepted architecture and actual repository evidence.

Repairs now incorporated into this Task Brief / Source Manifest include:

- explicit multi-native-domain SAVE composition rather than campaign-only SAVE;
- explicit rejection/classification of the current global one-hour/frontier machine as debt;
- generation-specific G/G+1 publication adoption;
- bounded native-root/direct-route completeness rather than broad scans;
- Step-5.8/WP-16 authority over final live realization;
- acting-principal/authorization basis in frozen publication attempts;
- actual named durability-edge owner mapping;
- checkpoint optionality and WP-14 boundary;
- storage metadata/default-branch publication separation;
- partial/indeterminate multi-domain result semantics.

Final critic state:

```text
UNRESOLVED BLOCKING:     0
UNRESOLVED SIGNIFICANT:  0
HUMAN DECISION REQUIRED: NO
STEP 2 AUTHORIZED:       NO — MANDATORY SENIOR REVIEW PENDING
```

---

## 19. Step-1 completion gate

This Task Brief is complete only together with the current Source Manifest and whole-project critic.

After publication/read-back of the coherent Step-1 package:

- stop for mandatory Senior review;
- do not begin Step 2;
- do not begin WP-14;
- do not begin implementation planning;
- do not modify runtime/schema/catalog/test implementation under this Step-1 authorization.
