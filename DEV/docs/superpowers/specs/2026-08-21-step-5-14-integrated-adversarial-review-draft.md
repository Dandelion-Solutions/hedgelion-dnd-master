# Step 5.14 — Full Recovery & Concurrency Adversarial Review — Integrated Review

Status: **INTEGRATED ADVERSARIAL REVIEW — RESOLUTION GATE PENDING**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-task-brief.md`

Primary navigation aid:

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`

This artifact attacks the accepted Steps 1–5 architecture as a composed system. It is not a new semantic owner/specification and does not silently modify earlier owner decisions.

---

# 1. Review method

For each case the review explicitly separates:

```text
PROSPECTIVE
ESTABLISHED
DURABLE
CURRENT AUTHORITY
PROJECTION
EVIDENCE
TRANSPORT STATE
```

and asks:

1. what native semantic owners exist;
2. what independently mutable source revisions exist;
3. what semantic edge has or has not been crossed;
4. what exact currentness/fencing rule applies;
5. what may lawfully be lost under the active durability promise;
6. what must survive in RRC;
7. what is rebuilt rather than recovered as authority;
8. whether retry can duplicate mechanics/RNG/temporal occurrence/disclosure;
9. whether transport order can leak into fictional chronology;
10. whether a projection/index/checkpoint/session/cleanup structure can become accidental authority;
11. whether the recovery/cleanup path remains bounded.

Primary classification:

```text
ARCHITECTURE BLOCKER
IMPLEMENTATION DEBT
STEP-6 FEASIBILITY DEPENDENCY
ACCEPTED PRODUCT LIMITATION / RISK
NO DEFECT
```

---

# 2. Thirty required integrated attacks

| # | Scenario | Failure/currentness attack | Result | Primary classification |
|---:|---|---|---|---|
| 1 | long singleplayer run with accumulated SOFT | destroy process after many established local mutations but before campaign publication | recovery returns to last actual compatible durable source set; unpublished SOFT is not invented; later natural/HARD boundary is what protects accumulated state | **NO DEFECT** |
| 2 | explicit SAVE | mix dirty campaign roots, already-durable dependencies, live sources and lagging Story | success only after every selected established dirty gameplay root plus required RRC/reference/interpretation closure is actually durable; Story freshness is irrelevant; partial native success remains real but SAVE remains unconfirmed until whole promise holds | **NO DEFECT** |
| 3 | controlled handoff | new gameplay arrives while source host is materializing recovery closure | scoped semantic-acceptance barrier prevents closure drift; pre-freeze accepted semantics materialize in native owners; acknowledgement occurs only after compatible durable RRC; no handoff snapshot becomes authority | **NO DEFECT** |
| 4 | abrupt crash before durability boundary | destroy all host/chat/HOT state with established deferrable local progress | only actual durable state recovers; newer SOFT may be lost by the owner-approved RPO contract; no plausible reconstruction/replay is permitted | **ACCEPTED PRODUCT LIMITATION / RISK** |
| 5 | crash/lost ACK during campaign publication | lose response after final ref operation; current HEAD may equal intended commit, descend from it, or exclude it | prepared objects remain nonauthority; bounded exact current/lineage evidence resolves what happened; no blind republish and no gameplay/RNG replay | **NO DEFECT** |
| 6 | suspended Resolution/Continuation crash | lose process after fixed inputs/RNG/choice state became required for unfinished execution | same Continuation generation and accepted interpretation/dependency evidence resume; missing required evidence blocks/suspects recovery rather than rebinding under ambient state | **NO DEFECT** |
| 7 | temporal trigger crash before/after materialization | crash at due discovery, owner claim, child creation or partial child execution | before acceptance current owner occurrence is reevaluated; after acceptance same occurrence is unavailable as fresh work and stable claim/execution identity resumes; invalid split visibility is integrity failure, not second firing | **NO DEFECT** |
| 8 | fixed RNG before suspension/restart | transport/recovery retry occurs after random result generated | accepted experiment/result identity survives and exact value is reused; no reroll/remap from traversal or repository conflict | **NO DEFECT** |
| 9 | two players in independent scenes | scene A and B advance independently and later one host observes different Git/live revisions | source/currentness and chronology remain domain typed; independent revisions are incomparable by default; no global vector, timestamp or event-ID order is required | **NO DEFECT** |
| 10 | two players in one live scene | concurrent actions prepare from same live revision | current route selects exactly one live truth source and exact-source CAS admits one transition; other writer refreshes/revalidates; shared consequence crosses write-before-reveal only after durable live publication | **NO DEFECT** |
| 11 | concurrent live CAS conflict | stale write loses to gameplay write or close | stale transition cannot overwrite; refresh determines ACTIVE/CLOSED and relevant dependencies; accepted gameplay is never replayed merely because source currentness changed | **NO DEFECT** |
| 12 | live close/rollover/failed absorption | close succeeds then campaign absorption conflicts/crashes | CLOSED_UNABSORBED remains current truth with zero ordinary writers; recovery resumes forward absorption; old epoch never reopens | **NO DEFECT** |
| 13 | entity crosses live ownership scopes | freeze several sources, crash after only subset closes | partial freeze is a valid technical mixed state, not partial fictional transfer; all affected owners/IDs remain native and recoverable; final campaign transfer occurs only after required closes are proven | **NO DEFECT** |
| 14 | global event touches multiple active scenes | attempt one fictional consequence across several independent live sources | architecture deliberately avoids distributed semantic commit: affected sources freeze first; partial freeze establishes no half-event; one campaign transition establishes the cross-scope consequence after all required final sources are known | **NO DEFECT** |
| 15 | campaign commit order conflicts with fictional chronology | later Git commit contains fictionally earlier calendar event or concurrent commits race | Git/ref/ID order has no implicit fictional meaning; typed chronology relations/metric evidence decide only when semantically established | **NO DEFECT** |
| 16 | cross-scene temporal dependency appears after independent advancement | armed owner is INDETERMINATE until late bridge relation arrives | relation evidence is append/forward-extensible; typed dependency invalidation selects only enrolled consumers; owner remains armed while indeterminate and is freshly reevaluated when evidence changes | **NO DEFECT** |
| 17 | Story lags; Chronicler restarts | delete model/process context after canon advanced far beyond Story | backlog derives from typed source basis minus compatible layer-local coverage; no queue/model memory/global Story frontier is required; current sources remain factual authority | **NO DEFECT** |
| 18 | Story publication fails while canon succeeds | Story draft loses same-ref CAS to canonical gameplay or NARRATIVE generation fails | canonical publication remains real; Story may abandon/yield/retry later; gameplay/SAVE/recovery never waits for Story freshness and no mechanics are replayed | **NO DEFECT** |
| 19 | transcript compaction while Story/history refs exist | attempt irreversible payload loss while exact/semantic/Story cursor consumers may survive | exact protection, semantic-content discharge, typed Story materialization when required, cursor/enumeration continuity and survivor/reference semantics must all hold before deletion; uncertainty retains | **NO DEFECT** |
| 20 | disclosure generation/emission/interruption/Retry | user interrupts after emission commit or retries old response; crash before disclosure durability | pre-emission eligibility/ref validation remains required; baseline may over-confirm full emission after interruption and may lose unpublished disclosure memory after crash; presentation retry never re-executes mechanics or creates a second fictional occurrence | **ACCEPTED PRODUCT LIMITATION / RISK** |
| 21 | checkpoint recovery with missing/corrupt dependency | checkpoint looks plausible but current native dependency is missing/incompatible | checkpoint is optional evidence only; current-authority-first recovery returns RETRY/BLOCKED/integrity as appropriate and never silently rolls back to checkpoint | **NO DEFECT** |
| 22 | stale multiplayer session after membership/authority change | old host uses cached binding/routing and tries to write or emit restricted content | semantic contract requires current application authorization, current route validation and recipient-scoped eligibility; stale session metadata grants nothing. Physical authenticated-principal/recipient/retry identity mapping must be proven by supported Step-6 host profile | **STEP-6 FEASIBILITY DEPENDENCY** |
| 23 | local entity/fact promotion forced by durable dependency | accepted durable knowledge/history/execution attempts to reference session/local-only identity or unowned proposition | durable canonical reference closure promotes/materializes the natural entity/fact owner and index/dependencies in the same required closure or rejects the reference; Story/message prose cannot become substitute authority | **NO DEFECT** |
| 24 | cleanup of obsolete artifact under concurrent/recovery dependencies | cleanup proves no blocker while campaign/live/operational sources may move | safe retirement requires compatible closed blocker vocabulary, complete current protection routing, coverage of every blocker-creating source, survivor-before-removal and currentness validation; inability to prove safe means retain/retry | **NO DEFECT** |
| 25 | engine/catalog upgrade changes cleanup blocker vocabulary while open execution exists | new runtime adds blocker class while old accepted execution remains pinned | cleanup contract generation participates in runtime/catalog compatibility; migration establishes new protection state before new cleanup rules activate; open execution keeps its accepted compatible interpretation | **NO DEFECT** |
| 26 | total LLM/chat loss with ACTIVE + CLOSED_UNABSORBED + Continuation + armed temporal owner + lagging Story | start from zero trusted host/model memory | current campaign route selects exact native live sources; RRC root routing recovers open execution/Procedure/Continuation and all independently-due temporal owners; Agenda/context/indexes rebuild; lagging Story is irrelevant to gameplay READY | **NO DEFECT** |
| 27 | Story-only commit races gameplay commit | Story advances same campaign ref between frozen gameplay base and final publication | if movement is proven Story-only/disjoint from gameplay dependencies, Step-5.6 transport-rebuilds the same accepted semantic transaction on new base; IDs/RNG/mechanics remain fixed; Story has lower contention priority | **NO DEFECT** |
| 28 | late chronology bridge makes owner DUE while live source moves | bridge evidence and FOLLOW/PRESERVE/SAFE_REBASE provider movement race Agenda state | Agenda is only candidate routing; current owner/binding/provider is reread before materialization; enrollment rewrites coherently with movement; accepted occurrence identity remains stable | **NO DEFECT** |
| 29 | exact Transcript is last text copy and source envelope retires | raw message payload/envelope is compacted/removed while Story retains exact quotation | retained exact claim requires surviving deterministic certification basis and appropriate cursor/provenance survivor; exact Transcript proves wording of communication only and never objective truth/current gameplay state | **NO DEFECT** |
| 30 | cleanup/protection-index generation changes during assessment | safe-retirement assessment pins old protection routing then successor generation becomes current | assessment is ephemeral and basis-sensitive; successor must be complete/durable/current before old routing retires; generation/currentness movement invalidates old negative proof and forces revalidation | **NO DEFECT** |

The original 24 expanded-agenda cases are all contained in this 30-case set; none were dropped.

---

# 3. Cross-front seam findings

## F1 — Accepted semantic state may be crash-volatile

**Challenge:** Step 3 calls a segment accepted/committed while Step 5.5 allows it to remain SOFT and Step 5.2/5.7 may later recover an older durable point.

**Resolution:** no contradiction. `ESTABLISHED` and `DURABLE` are intentionally orthogonal. Current runtime truth may be ahead of crash-recovery promise. A named HARD edge/SAVE/handoff converts the relevant scope into a durability obligation. Unexpected loss before that promise may lose SOFT and must never reconstruct it.

Classification: **NO DEFECT**.

Product implication: unexpected-loss RPO must remain explicit and must not be described as automatic crash-proof saving.

## F2 — Step-3 local segment atomicity versus cross-live global events

**Challenge:** one accepted action can affect several active live scopes; no distributed transaction exists.

**Resolution:** the global semantic transition is not established by independently writing half the final consequence into each live source. Required live sources are first closed/frozen independently; partial freeze is only technical currentness state. The actual cross-scope transfer/global consequence is established in the later campaign-domain transition after required final sources are known. Accepted root execution may remain open/recoverable across the process.

Classification: **NO DEFECT**.

Implementation obligation: machine realization must not map “one user action” mechanically to “one Step-3 segment spanning several refs.”

## F3 — Cleanup proof versus a new cross-source consumer

**Challenge:** cleanup pins campaign state proving no consumer, while an independently writable live/operational source creates a new dependency without moving campaign HEAD.

**Resolution:** Step 5.13 admits automatic cleanup only when every blocker-creating source class uses one of:

```text
SELF-CONTAINED CONSUMER
CROSS-SOURCE PROTECTION REGISTRATION
SOURCE FENCE / SYNCHRONIZATION
```

For cross-source registration, the safe baseline ordering is conservative:

```text
register/protect target durably first
-> accept external consumer

consumer ends/becomes self-contained
-> release external need
-> remove protection later
```

Crash in either direction creates temporary over-retention, not use-after-delete. A live writer that creates a representation-dependent consumer without the declared protection/fence is an integrity/implementation defect and makes automatic cleanup invalid for that contract.

Classification: **NO DEFECT**, with **SIGNIFICANT implementation debt**.

## F4 — Story lag versus source compaction

**Challenge:** Step 5.10 allows indefinite Story lag; Step 5.11/5.13 allow source payload/envelope retirement.

**Resolution:** there is deliberately no promise that future Story can reproduce every lawfully deleted old payload. `MUST_MATERIALIZE`/explicit archival protection blocks deletion until required Story output exists. `MAY_OMIT` material may lawfully lose exact/fidelity source after semantic discharge, while source candidate/cursor continuity remains sufficient for currently supported coverage/migration. Future projection contracts cannot invent deleted source.

Classification: **NO DEFECT**.

Product implication: Story is durable but not universally regenerable at full historical fidelity.

## F5 — Verified exact Transcript as sole exact copy versus Story nonauthority

**Challenge:** after source compaction, noncanonical Story may be the only exact textual copy.

**Resolution:** this does not promote Story into objective/gameplay truth. The retained Story record may be authoritative only for the narrow **certified textual-equality claim** under its archive contract. Gameplay correctness-critical exact semantics must already have moved to a canonical/natural owner and may not depend solely on Story. Exact transcript proves what was communicated, not whether its proposition is true.

Classification: **NO DEFECT**.

## F6 — Concurrent disclosure updates without immediate publication

**Challenge:** `runtime.disclosure` is one semantic owner while outbound disclosure changes are normally SOFT. Concurrent host/session work could create overlapping unpublished updates.

**Resolution:** repeated exposure is intentionally monotonic under the fact owner's semantic truth-transition relation. When overlapping campaign publication occurs, Step 5.6 requires native-owner reconciliation rather than last-writer-wins. Therefore compatible disclosure updates can join deterministically; contradictory/incomparable evidence where a linear relation is required is not resolved by transport order.

For non-monotonic owners such as `world.knowledge`, independent live/source writers may not assume this merge property: Step 5.8 containment/synchronization rules require one native writable partition or an explicit synchronization/repartition boundary.

Classification: **NO DEFECT**, with **SIGNIFICANT implementation/test debt**.

## F7 — Same-ref Story/gameplay/cleanup contention

**Challenge:** Story and cleanup share campaign ref with canonical gameplay; transport conflict might induce semantic replay or clear wrong dirty generations.

**Resolution:** all use Step-5.6 exact-base single-parent non-force publication. Disjoint movement may cause transport-only rebuild; overlapping semantic dependencies require current native revalidation. Dirty clearing is generation-specific. Story yields under sustained contention. Cleanup final proof includes blocker/currentness footprint, so relevant movement invalidates retirement proof.

Classification: **NO DEFECT**.

## F8 — Recovery composes several native sources rather than one snapshot

**Challenge:** campaign H, live LA/LB and operational sources may have different revision domains and may move while hydration occurs.

**Resolution:** Step 5.7 pins exact revisions per source for one attempt and proves a coherent owner-defined source composition rather than a scalar global cut. Final current-routing/root-membership validation detects material basis movement and returns retry/block as appropriate. A coherent read composition never merges writable authority.

Classification: **NO DEFECT**.

## F9 — Controlled handoff cannot stop other legitimate writers

**Challenge:** handoff barrier is host-local; another valid live writer may advance current state while handoff is running.

**Resolution:** handoff does not claim a global lock. External relevant movement invalidates/reselects the source composition. Shared live changes are already durable at their own write-before-reveal edge. Handoff acknowledgement requires the final compatible durable composition, not the source host's stale frozen view.

Classification: **NO DEFECT**.

## F10 — Git history still physically contains lawfully compacted secrets/text

**Challenge:** current-tree cleanup deletes a payload but append-only Git history still contains bytes; ordinary retrieval could “resurrect” exact text and undermine retention semantics.

**Resolution:** Step 5.13 explicitly separates transport/audit history from semantic retained memory. Ordinary Master/Story/history retrieval may not mine old Git commits to restore lawfully compacted exact text. Forensic/integrity history access is a separate authorized mode and does not change semantic retention status. Current-tree cleanup is not secure erasure.

Classification: **NO DEFECT**, with implementation guard and documentation debt.

---

# 4. Step-6 feasibility dependencies exposed by Step 5.14

These are not Step-5 semantic blockers, but Step 6 must treat them as real feasibility gates rather than routine implementation details.

## SD-1 — Deterministic RepositoryPort transport

Canonical Step 5.6 requires Python-owned repository publication semantics. Existing feasibility work demonstrates exact hash-verifiable Git tree construction and real non-force ref race protection, but the current built-in connector is still a model/tool relay rather than the intended deterministic Python transport boundary.

Step 6 must select/prove a supported profile or explicitly refine the compatibility profile without silently moving repository protocol authority into an LLM role.

Severity: **BLOCKING for a persistence-capable deployment profile**.

## SD-2 — Pre-player-visible Narrator validation boundary

Step 4/5.12 require material Narrator output and disclosure refs to be eligible/validated before the material content becomes player-visible. Streaming host behavior may make same-call generation directly visible.

Step 6 must prove staging/buffering/separate invocation or an equivalent topology.

Severity: **BLOCKING for any profile that may expose secret-bearing output**.

## SD-3 — Stable invocation/retry/edit/branch identity

Step 3 and Steps 5.11/5.12 require accepted Interaction/message identity and no gameplay replay on Retry/edit/branch. Host products may expose weaker revision ancestry than the semantic model desires.

Step 6 must determine what identity is available, what application identity can be minted reliably, and which host behaviors belong to unsupported/degraded profile semantics.

Severity: **SIGNIFICANT / potentially blocking for strong retry idempotency guarantees**.

## SD-4 — Authenticated acting-principal and recipient/audience mapping

Repository credentials are not gameplay authority, and disclosure is recipient scoped. Step 6 must prove trustworthy mapping from physical host user/session to application principal/player and intended audience, including shared-surface limitations.

Severity: **BLOCKING for secure multiplayer write/disclosure profiles**.

## SD-5 — Real role-context isolation/reset

Step 4 forbids a narrower role from running in a physical invocation that still contains ineligible source material. Prompting a model to “forget” is not isolation.

Step 6 must prove context reset/isolation or separate calls compatible with the six logical roles.

Severity: **BLOCKING for any topology that combines differently privileged logical roles**.

## SD-6 — Optional live-ref deletion

Current connector lacks ref deletion. Step 5.13 already makes this capability optional and classifies its absence as cleanup deferral rather than gameplay failure.

Severity: **MINOR / nonblocking capability dependency**.

---

# 5. Accepted product limitations carried through the review

These remain explicit and are not disguised as architecture defects:

1. **Unexpected-loss RPO for unpublished SOFT.** Established deferrable local state can be lost before a durability promise.
2. **Emission interruption ambiguity.** After `EMISSION_COMMIT`, interruption may leave only a prefix visible while HDM records the full committed representation/disclosure.
3. **Unsaved disclosure under-memory.** Crash may lose SOFT exposure metadata and cause later repetition of otherwise eligible information.
4. **No exactly-once visible prose/read receipt guarantee.** Presentation reliability is intentionally weaker than gameplay semantic idempotency.
5. **Story fidelity can degrade after lawful source compaction.** Story remains noncanonical and not universally byte-regenerable.
6. **Live close/revocation safety does not guarantee starvation-freedom under unbounded valid contention.** Safety is preserved; coordination/maintenance may be needed.
7. **Current-tree cleanup is not secure erasure.** Historical Git objects may continue to contain old bytes.
8. **Lawful compaction may reduce later forensic richness.** Explicit audit/repair contracts, not hypothetical future usefulness, determine retention.

---

# 6. Consolidated implementation-debt clusters

The review did not discover a new semantic subsystem requirement. It did sharpen implementation debt into these cross-slice clusters.

## ID-A — Native source/routing/currentness framework

- exact current source pinning and coherent source-composition validation;
- typed bounded RRC/root routing and lifecycle coherence;
- campaign/live write-authority lookup;
- no implicit cross-domain comparison;
- generation/currentness footprints for publication and cleanup.

## ID-B — Execution/temporal continuity

- RuntimeCommand/Resolution/Procedure/Continuation persistence;
- stable firing/occurrence IDs;
- fixed RNG binding;
- source claim/finalize/rearm closure;
- temporal dependency-key extraction/reverse enrollment;
- stale Agenda validation;
- provider move/rebase integration.

## ID-C — Publication and live CAS

- Python RepositoryPort interface;
- exact-base campaign transactions;
- accepted/rejected/indeterminate outcomes;
- bounded ambiguity verification;
- live exact-source CAS;
- close/absorption/transfer protocols;
- transport-only rebuild versus semantic-overlap classification;
- generation-specific dirty clearing.

## ID-D — Story/history/disclosure

- Story layer projection state/coverage/allocators;
- source contract generations and cursor migration;
- `runtime.message` stable source-native identity;
- exact/slice protection and semantic discharge;
- verified Transcript certification;
- recipient-scoped disclosure and monotonic semantic merge;
- pre-emission validation hooks;
- no mechanics replay on presentation retry.

## ID-E — Cleanup/retention

- closed CleanupContracts by target kind/generation;
- completeness-typed protection routing;
- cross-source protection registration/fencing;
- survivor/reference semantics;
- checkpoint/message/Story/chronology/live cleanup cases;
- Git-history semantic exclusion;
- conservative compatibility migration;
- no generic GC/refcount/frontier.

## ID-F — Tests/observability

Implementation tests must include the thirty scenarios above plus the stronger composite cases in Section 7. Diagnostics must explain routing/currentness/protection decisions without turning diagnostic state into authority.

---

# 7. Stronger composite worst-case attacks

## C1 — Total host amnesia during mixed live/recovery state

Initial state:

```text
campaign H
live A ACTIVE @ LA
live B CLOSED_UNABSORBED @ LBf
RuntimeCommand C non-SETTLED
Resolution R suspended through Continuation K
fixed RNG already accepted
armed temporal owner T in live A
another temporal owner U = CLAIMED(G,F)
Story EVENTS caught up, NARRATIVE far behind
one outbound disclosure still SOFT only
```

Failure: all host/model/chat memory disappears.

Expected recovery:

1. current campaign H selects A/B routes;
2. exact current live sources are resolved/pinned;
3. RRC root routing finds C/Procedure/K plus all independently-due temporal owners;
4. fixed RNG and accepted execution context hydrate from native execution evidence;
5. claimed U resolves F rather than rematerializing G;
6. Agenda/provider dependency indexes rebuild from current owners;
7. B remains CLOSED current truth and recovery resumes absorption as appropriate;
8. lagging Story is ignored for gameplay READY;
9. unpublished disclosure may be lost under accepted RPO and never drives gameplay replay.

Result: **NO DEFECT**.

## C2 — Explicit SAVE races Story, live advance and ambiguous campaign ACK

Initial state: dirty campaign-local SOFT, active live source already durable through each accepted shared transition, Story writer preparing a same-ref commit.

Attack:

1. Story wins campaign ref first;
2. gameplay SAVE rebuilds on proven Story-only movement;
3. campaign ref update returns INDETERMINATE;
4. live source advances again before SAVE final validation.

Expected result:

- accepted local mechanics/IDs/RNG are not replayed due Story movement;
- ambiguous campaign result is verified against current lineage/closure;
- live movement is not a problem if final current live generation is itself durably established and compatible;
- SAVE is acknowledged only when current selected composed source closure satisfies the save promise;
- otherwise SAVE stays unconfirmed without pretending successful native publications disappeared.

Result: **NO DEFECT**.

## C3 — Cleanup target races new live consumer

Initial state: target X appears terminal and cleanup assessment finds no current blockers.

Attack: live source L can create new accepted consumer Y that would require current X.

Safe outcomes permitted by the cleanup contract:

```text
A. Y self-contains everything needed -> X may retire
B. durable protection for X is registered before Y acceptance -> cleanup sees/proof-invalidates
C. L is fenced/synchronized through cleanup -> no new Y can appear during proof
```

Any implementation allowing Y to commit first and protection to appear later is nonconforming and unsafe.

Result: **NO DEFECT in architecture; SIGNIFICANT implementation/test obligation**.

## C4 — Late chronology bridge + owner transfer + temporal firing

Initial state: temporal owner T is armed and INDETERMINATE, depends on cross-scope bridge; owner/provider then moves from source scope to destination while late bridge evidence arrives.

Expected result:

- owner/provider transfer preserves FOLLOW/PRESERVE/SAFE_REBASE semantics;
- derivative enrollment rewrites coherently;
- bridge change selects T only through typed dependency path;
- materialization rereads current owner occurrence/provider;
- stale old-scope Agenda entry cannot fire;
- once accepted, occurrence identity prevents duplicate firing across source movement.

Result: **NO DEFECT**.

## C5 — Engine adoption + open Continuation + cleanup generation change

Initial state: open accepted execution pinned to runtime/catalog generation G; new generation G2 expands cleanup blocker vocabulary and changes representation eligibility.

Attack: host adopts G2 and maintenance immediately attempts cleanup of an artifact still needed by G execution.

Expected result:

- open execution continues under compatible pinned G interpretation/dependencies;
- G2 cleanup rules remain retain-only for unmigrated targets/protection state;
- compatible migration establishes new cleanup/protection contract before automatic G2 cleanup activates;
- no ambient reinterpretation of the open Continuation.

Result: **NO DEFECT**.

## C6 — Stale host after revocation attempts gameplay and secret emission

Initial state: Player P is removed; affected live epoch closes and campaign absorption/revocation transaction becomes current. Old host retains cached ACTIVE source/player binding and private context.

Attack: old host attempts another write and emits a secret-bearing response.

Semantic expectation:

- old live source is CLOSED/non-writable and stale CAS cannot succeed;
- session metadata cannot grant authority;
- application authorization must be refreshed/revalidated on current route/binding;
- response eligibility requires current authenticated recipient/audience and supported pre-visible validation surface.

Repository/currentness laws are sufficient to reject stale gameplay write. Whether the physical host can reliably fence the player-visible response before leakage depends on Step-6 principal/audience/staging capabilities.

Result: **STEP-6 FEASIBILITY DEPENDENCY**, not permission to weaken disclosure semantics.

## C7 — Lawfully compacted exact message remains in old Git history

Initial state: exact text has been semantically discharged; current source payload/envelope retires; no exact archive promise survives; ancestor Git commit still stores bytes.

Attack: later user asks for the exact quote and a naive repair/search routine can technically find the old blob.

Expected result:

- ordinary historical query returns semantic-only/unavailable exact wording according to current retention contract;
- normal runtime does not mine transport history to resurrect exact memory;
- an explicitly authorized forensic mode may inspect old Git evidence but does not mutate semantic retained-memory status.

Result: **NO DEFECT**, implementation guard required.

---

# 8. Final authority/contamination sweep

| Structure | Correct role | Forbidden promotion checked by 5.14 |
|---|---|---|
| campaign ref/commit | campaign publication/current durable selection | fictional chronology, universal recovery cut |
| live source revision | scope-local currentness/CAS fence | global order/time |
| HOT dirty state | current owner-relative unpublished state | independent durable owner |
| RRC | property over native durable sources | snapshot/mega-owner |
| recovery routing | bounded native owner discovery evidence | lifecycle/current payload authority |
| checkpoint | optional immutable recovery/maintenance evidence | current state / SAVE proof / rollback authority |
| session metadata | coordination/observability | write authority / liveness lease |
| Temporal Agenda | rebuildable candidate/dependency selector | obligation/scheduler/time authority |
| chronology evidence | typed causal/order/metric evidence | scheduler/current world owner/global clock |
| RuntimeCommand/Resolution/Procedure/Continuation | accepted execution native owners | checkpoint/Story/session replacement |
| Story | durable noncanonical read/presentation model | world/history truth/current-state recovery authority |
| Story coverage/allocator | projection-local progress/identity state | campaign frontier / source authority |
| runtime.message | accepted communication evidence identity | truth/knowledge/disclosure by itself |
| runtime.disclosure | human exposure owner | PC knowledge / objective truth |
| Transcript exact certification | narrow textual equality evidence | objective truth / gameplay exact owner when canonical consumer still requires text |
| protection routing | completeness-typed blocker discovery evidence | forward consumer semantic owner |
| SafeRetirementAssessment | ephemeral proof working state | persistent liveness/GC authority |
| CleanupContract | closed validation vocabulary | target lifecycle owner |
| prepared Git objects | transport candidates | gameplay/history authority |
| Git ancestor bytes | transport/audit history | ordinary exact semantic memory after lawful compaction |

No contamination path survived the review as a new authority.

---

# 9. Preliminary review verdict

After the thirty required attacks and seven stronger composite cases:

```text
unresolved Step-5 architecture blockers found: 0
new owner-level product decisions required: 0
accepted product limitations reaffirmed: 8
Step-6 feasibility dependencies requiring explicit proof: 6
cross-slice implementation-debt clusters: 6
```

This is **not yet the Step-5 closure claim**. The next action is an analytical challenge of this preliminary verdict itself, followed by a resolution gate. In particular, the challenge must attempt to falsify:

1. the claim that cross-source cleanup registration can always avoid a distributed transaction;
2. the claim that multi-source recovery compatibility is sufficient without a scalar snapshot;
3. the claim that disclosure concurrency remains owner-safe under SOFT accumulation;
4. the claim that global multi-live semantic transitions can remain forward-only and recoverable;
5. the claim that all remaining host limitations can safely be deferred to Step 6 without weakening Step-5 semantics.