# Step 5.14 — Full Recovery & Concurrency Adversarial Review — Task Brief

Status: **IN PROGRESS — ARCHITECTURAL ADVERSARIAL REVIEW**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Problem statement

Steps 5.0–5.13 were designed and locally challenged as individual slices. Step 5.14 must attack the resulting architecture as one composed system and determine whether locally valid ownership, durability, recovery, live-authority, chronology, Story, transcript, disclosure and cleanup contracts remain mutually coherent under combined crash, retry, concurrency, source-movement and compaction failures.

The review is specifically intended to find cross-slice contradictions that local reviews could not expose.

## 2. Scope

Review the accepted architecture from Steps 1–5 where it participates in Step-5 continuity, with primary focus on:

- Step-3 accepted execution, idempotency, Procedure/Continuation and fixed-RNG boundaries;
- Step-4 truth, knowledge, disclosure and noncanonical Story ownership;
- Steps 5.0–5.13;
- campaign and live publication/currentness;
- cold recovery and controlled handoff;
- temporal/pending obligations and chronology;
- Story catch-up/publication;
- transcript/history retention and compaction;
- host disclosure/emission semantics;
- cleanup/retirement and compatibility/migration seams.

## 3. Non-goals

Step 5.14 SHALL NOT:

- design Step-6 physical LLM topology;
- choose deployment/model/token/cost topology;
- begin broad runtime/schema implementation;
- revive a rejected generic scheduler, global frontier, global clock, checkpoint snapshot authority, Story authority, delivery outbox/ACK subsystem or generic semantic GC merely to simplify review;
- reinterpret Git/ref/commit order as fictional chronology;
- treat current stale GAME prose/schemas as authority over accepted canonical architecture.

## 4. Governing evidence and precedence

Use:

1. current branch/ref and repository tree;
2. `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` for sequencing;
3. `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` as non-normative locator;
4. owning canonical Step-3/4/5 specifications and owner decisions;
5. current model/contracts and machine contracts where the canonical specs delegate details;
6. local critical/adversarial reviews for provenance;
7. expanded Step-5 agenda only where later canonical slices have not superseded its wording.

If the index or agenda conflicts with an owning source, the owning source wins.

## 5. Fixed architectural constraints to attack, not assume away

The review must preserve unless integrated evidence proves an actual contradiction requiring reopening:

- one semantic/current owner for each mutable concern;
- deterministic Step-3 accepted execution boundary;
- no raw LLM/chat/process memory as gameplay authority;
- domain-typed progress/frontier/order and no implicit cross-domain ordering;
- Resumable Runtime Closure over compatible native durable sources plus bounded typed routing;
- owner-local temporal authority, rebuildable Agenda and chronology-as-evidence;
- edge-obligation durability semantics;
- non-force single-ref CAS campaign publication;
- current-authority-first recovery;
- routed fixed-claim live epochs and exact-source CAS;
- sparse typed chronology and forward-extensible causal history baseline;
- noncanonical lagging Story with layer-local coverage;
- semantic continuity rather than universal verbatim transcript retention;
- validated emission-commit with no baseline durable delivery-ACK subsystem;
- owner-gated conservative cleanup with complete typed blocker/protection routing.

## 6. Quality attributes / fitness criteria

The integrated architecture must demonstrate:

- **correctness:** no accepted gameplay state, obligation or promised evidence is silently lost, duplicated, invented or assigned to a second authority;
- **determinism:** recovery/retry never depends on hidden model memory and never rerolls/re-executes already accepted mechanics because transport/projection failed;
- **currentness:** stale campaign/live/session/index/projection state cannot overwrite or impersonate current authority;
- **bounded recovery:** ordinary recovery uses current routes/native dependencies rather than campaign-wide scans or global reconstruction;
- **conservative irreversibility:** uncertain cleanup/compaction retains rather than destroys required evidence;
- **projection isolation:** Story/history/presentation failure cannot roll back or block gameplay authority except where an explicit canonical contract requires a gameplay-significant dependency;
- **chronology integrity:** storage/concurrency order never silently becomes fictional order;
- **testability/observability:** every material scenario has a deterministic expected authority/currentness/recovery outcome and a meaningful failure classification.

No new numerical performance target is invented by this review.

## 7. Review fronts

### A. Durability / publication / recovery

Attack Step-3 + 5.2 + 5.4–5.7 seams: accumulated SOFT, SAVE, controlled handoff, crash before/inside publication, ambiguous ACK, suspended execution, corrupt/missing recovery dependencies.

### B. Live / concurrency / temporal / chronology

Attack 5.1 + 5.3 + 5.7–5.9 seams: independent scenes, same-scene CAS, close/absorption/rollover, source transfer, global events, late chronology bridges, due-state changes, fixed RNG and source movement.

### C. Story / transcript / disclosure

Attack Step-4 + 5.10–5.12 seams: layer-local lag, projection races, source compaction, exact-text protection, stable message evidence, emission interruption/edit/Retry and recipient-scoped disclosure.

### D. Cleanup / retention / migration

Attack 5.2 + 5.7–5.13 seams: currentness races during retirement, protection-index generation changes, live refs, checkpoint retirement, compact message/source envelopes, Story/chronology provenance and compatibility vocabulary changes.

### E. Cross-front contamination

Construct scenarios combining at least three fronts, especially fresh-process recovery with mixed ACTIVE/CLOSED_UNABSORBED live state, suspended execution, armed temporal owner, lagging Story, partially compacted transcript and concurrent cleanup/publication.

## 8. Minimum scenario set

The review SHALL cover the 24 scenarios from the expanded Step-5 agenda and the 30-route matrix in `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`. It may consolidate equivalent cases only when the stronger combined case subsumes their failure mechanism and expected result.

## 9. Analytical challenge questions

For every scenario ask:

1. What semantic owners exist before failure?
2. What independently mutable durable/current sources exist?
3. Which facts are prospective, ESTABLISHED, DURABLE, current authority, projection, evidence or transport-only state?
4. Where is the acceptance edge?
5. What exact currentness fence applies?
6. What can be lost without violating the declared durability contract?
7. What must be recovered and from which native source?
8. What must be rebuilt rather than recovered as authority?
9. Can retry duplicate accepted execution/RNG/temporal occurrence/disclosure?
10. Can transport order leak into fictional order?
11. Can Story/checkpoint/index/cleanup metadata become accidental authority?
12. Can a stale session/source/index make a valid-looking but wrong decision?
13. Can compaction destroy the only surviving promised semantic/exact/chronology evidence?
14. Does the recovery path remain bounded?
15. Would the obvious fix introduce a second authority or speculative subsystem?

## 10. Finding classification

Every material finding must be classified as exactly one primary class:

```text
ARCHITECTURE BLOCKER
IMPLEMENTATION DEBT
STEP-6 FEASIBILITY DEPENDENCY
ACCEPTED PRODUCT LIMITATION / RISK
NO DEFECT
```

Severity for review findings:

```text
BLOCKING
SIGNIFICANT
MINOR
```

An earlier canonical slice reopens only when integrated evidence proves a real contradiction or unsatisfied correctness invariant. Implementation inconvenience is not enough.

## 11. Required outputs

Step 5.14 must produce:

- integrated scenario results with explicit failure mechanisms and expected recovery/currentness outcome;
- final authority/contamination sweep of Step-5 abstractions;
- cross-system contradiction ledger;
- resolution/disposition of every material finding;
- explicit Step-6/implementation carry-forward ledger;
- closure recommendation with confidence and falsifiability statement;
- canonical final review artifact if and only if all blockers are closed;
- roadmap update only after the resolution gate.

## 12. Exit criteria

Step 5 may close only if:

1. every required integrated scenario has a coherent deterministic outcome;
2. no unresolved Step-5 architecture blocker remains;
3. no projection/cache/index/evidence/transport abstraction has become accidental gameplay authority;
4. recovery remains native-owner/current-authority-first and bounded;
5. publication/live-source races cannot duplicate or invent accepted mechanics;
6. chronology remains independent of Git/host concurrency order;
7. Story/transcript/disclosure/cleanup semantics do not contradict gameplay durability or each other;
8. unresolved implementation obligations and Step-6 feasibility questions have explicit owners;
9. any accepted product limitation remains explicit rather than disguised as correctness;
10. the final roadmap identifies the exact next continuation point.

If any blocker remains unresolved, Step 5 stays open.