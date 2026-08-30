# Step 5.10 — Story Projection Durability — Resolution Gate

Status: **RESOLUTION GATE — READY FOR CANONICALIZATION**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Inputs:

- `2026-08-21-step-5-10-story-projection-durability-task-brief.md`
- `2026-08-21-step-5-10-story-projection-durability-research-draft.md`
- `2026-08-21-step-5-10-story-projection-durability-analytical-challenge.md`
- `2026-08-21-step-5-10-story-projection-durability-candidate-spec.md`
- `2026-08-21-step-5-10-story-projection-durability-adversarial-review.md`

Candidate direction under gate:

> **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**

---

# 1. Gate question

Can Step 5.10 close Story projection durability without:

- background workers;
- durable projection jobs/claims;
- Story participation in gameplay SAVE/RRC;
- a global projection frontier;
- Story/canon duplicate authority;
- cross-layer all-or-nothing publication;
- model-call topology decisions belonging to Step 6?

**Answer: YES.**

---

# 2. Alternatives resolved

## A — Story inside canonical gameplay publication

Rejected because Story/Chronicler failure would block gameplay durability and violate explicit Step-5.10 isolation.

## B — mandatory post-canon Story projection every turn

Rejected as semantic requirement because it burns latency/tokens and still needs restart catch-up. May remain a Step-6 opportunistic activation policy.

## C — queue-free pull catch-up from durable typed coverage

Accepted as architecture direction.

## D — durable projection job queue

Rejected baseline as duplicate backlog/lifecycle machinery without a required background worker.

## E — source-keyed Story record IDs

Rejected as universal identity because Story projection is many-to-many and Step 4 already fixes layer-local human-facing IDs.

## F — rebuild Story on demand without progress state

Rejected because it is unbounded, expensive and cannot preserve fidelity after source compaction.

---

# 3. Required adversarial amendments — disposition

| Finding | Resolution |
|---|---|
| coverage policy can change retroactively | coverage is typed by semantic projection-contract generation |
| campaign HEAD can move from Story-only commit | campaign HEAD is transport pin only; source-domain basis/watermark owns projection progress |
| mutable Story progress in MANIFEST/CURRENT destroys disjointness | ordinary projection state remains under Story-owned surface; MANIFEST may carry static `story_root` only |
| source compaction can strand cursor | source-domain contract must preserve/migrate cursor continuity through 5.11/5.13 |
| concurrent workers may use incompatible semantic contracts | contract generation is frozen transaction dependency; incompatible movement requires migration/reassembly |
| contiguous cursor unsafe for late insertion | source projection enumeration must be append-monotonic or use typed sparse fallback |
| `MUST_MATERIALIZE` cardinality can vary | layer/source contract may impose additional mapping/cardinality validation |
| transcript candidate meaning depends on delivery/retention | explicit 5.11/5.12 handoff; 5.10 does not infer generated text as transcript |
| Story-to-Story prose could become authority | factual compatibility remains grounded in canonical/historical source refs; Story refs remain presentation dependencies |

All blocking findings are resolved without adding a new semantic owner or generic scheduler.

---

# 4. Final authority geometry

```text
CANONICAL / HISTORICAL SOURCE OWNERS
    own occurred facts/evidence/messages/mechanics

SOURCE PROJECTION DOMAIN CONTRACT
    owns candidate enumeration semantics
    owns projection-contract generation

STORY LAYER PROJECTION STATE
    durable non-canonical progress/identity metadata
    - source-domain coverage
    - layer allocator high-water
    - layer indexes/order metadata

CHRONICLER LOGICAL ROLE
    proposes editorial/generative projection only

DETERMINISTIC STORY CONTROL/PUBLISHER
    selects source work
    pins basis
    validates draft
    allocates final Story IDs
    validates availability/refs
    publishes Story closure through Step 5.6
```

No Story layer may become canonical source authority.

---

# 5. Final catch-up invariant

For each `(layer, source_domain, projection_contract_generation)`:

```text
coverage K
```

means all admitted candidates through K have reached a terminal disposition permitted by that exact semantic projection contract.

Backlog is derived from current source-domain basis minus compatible coverage.

No durable job object is required.

---

# 6. Final single-chat deployment statement

Step 5.10 correctness is deliberately stronger than current product convenience:

> Story projection remains correct even when HDM has only one ordinary sequential ChatGPT execution stream and no work continues after the current assistant turn ends.

Therefore:

- no Work dependency;
- no Pro/Enterprise dependency;
- no Scheduled Task dependency;
- no persistent background Chronicler dependency.

Step 6 may add isolated calls/workers/API orchestration as performance/quality deployment choices without changing the Step-5.10 persistence model.

---

# 7. Final same-ref concurrency statement

Story and canonical state remain on one campaign ref.

The architecture does not promise that Story can never cause one extra CAS retry. It promises the stronger semantic property that matters:

```text
canonical gameplay never waits for Story freshness/generation/lock
Story-only movement is proven-disjoint from ordinary gameplay authority
canonical gameplay preserves accepted mechanics/RNG/IDs across Story-only rebase
Story yields under repeated contention
```

No second Story branch or priority lock is required.

---

# 8. Final layer-independence statement

Ordinary catch-up has no required cross-layer atomicity.

Legal state:

```text
TRANSCRIPT = caught up to its basis
EVENTS = caught up to another basis
MECHANICS = lagging
NARRATIVE = heavily lagging
```

A layer transaction publishes its own record/index/availability/allocator/coverage closure.

Cross-layer Story maintenance may be atomic only when structural correction of already-published refs requires it.

---

# 9. Final retention handoff

Step 5.10 closes the projection side only.

Steps 5.11/5.13 must preserve:

1. any typed projection-before-delete requirement selected by retention policy;
2. interpretation/resume continuity of retained Story coverage cursors after source compaction.

`source_refs` promise stable source identity attribution, not permanent full-payload retention by themselves.

Transcript candidate admission additionally depends on the exact Step-5.11/5.12 participant-message/delivery contract.

---

# 10. Owner decision check

No material unresolved owner decision remains for core Step-5.10 architecture.

The baseline deliberately makes the weakest promises consistent with accepted requirements and owner constraints:

```text
Story freshness: eventual/opportunistic; no SLA
background processing: not required
stable external permalink across arbitrary structural rewrite: not promised
source identity provenance: preserved
permanent source payload dereferenceability: not promised by 5.10
Story SAVE/RRC participation: none
```

Stronger future product promises require explicit owner decisions and may add machinery later.

---

# 11. Canonicalization recommendation

**CANONICALIZE** the reviewed direction with all adversarial amendments incorporated.

No architecture blocker remains.

After canonicalization, update the roadmap to:

```text
5.10 CLOSED
5.11 NEXT / NOT STARTED
```

No Step-5.11 research begins before the Step-5.10 canonical/status verification gate completes.
