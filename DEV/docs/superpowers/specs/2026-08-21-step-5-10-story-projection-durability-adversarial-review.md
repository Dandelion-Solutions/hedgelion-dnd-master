# Step 5.10 — Story Projection Durability — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE NOT YET CANONICAL**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed candidate:

- `2026-08-21-step-5-10-story-projection-durability-candidate-spec.md`

Review goal:

> Attack the candidate for hidden authority, hidden global ordering, policy-version traps, source-compaction breakage, same-ref contention, role-topology leakage and restart duplication before any resolution gate/canonicalization.

---

# 1. Verdict

The core candidate survives, but the review found **five blocking specification gaps** and four strengthening clarifications.

All five blockers are mechanically resolvable without changing owner product semantics or requiring a new human architecture decision.

Required direction after fixes remains:

> **LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS**

with stronger source-domain and projection-contract typing.

---

# 2. BLOCKER A — coverage cursor can silently skip retroactively admitted candidates

## Attack

Candidate says:

```text
coverage(D) = K
```

means all candidates through K were considered.

But what if the **candidate-admission/disposition policy itself changes**?

Example:

```text
contract generation G1:
    source items 1..100
    only player-visible utterances of class A are transcript candidates
    coverage = 100

later contract generation G2:
    class B utterances are now also required transcript candidates
```

Some old class-B items may exist at source positions `< 100`. Reusing G1 coverage under G2 would falsely claim those newly admitted candidates were considered.

This is not the same as changing model/prompt wording. It changes the semantic projection candidate set.

## Required fix

Coverage must be interpreted under an explicit **Story projection contract generation** for the layer/source-domain pair.

Conceptually:

```text
ProjectionContractRef
    layer
    source_domain
    semantic contract generation/version

Coverage
    contract_ref
    source cursor/evidence
```

A semantic contract change that can alter:

- candidate admission behind existing coverage;
- `MUST_MATERIALIZE` versus `MAY_OMIT` disposition;
- source enumeration interpretation;
- output cardinality required for terminal disposition;

requires an explicit migration/reprojection decision for affected coverage.

A model/prompt/style/projector implementation change that does **not** alter those semantics does not invalidate coverage.

## Resolution

**BLOCKER RESOLVED TECHNICALLY.** Add contract-generation typing to canonical coverage semantics. No generic projector-version replay.

---

# 3. BLOCKER B — campaign HEAD is not a Story source watermark

## Attack

Candidate frequently says “pinned campaign/source basis”. Since Story and canon share one campaign ref, HEAD can advance solely because Story was edited.

Example:

```text
H1 canonical sources unchanged
H2 = Story-only commit
```

If `H2 > H1` were treated as new projection source progress, Story could invent backlog from its own publication.

Likewise Git commit order must not become a source-event or fictional chronology frontier.

## Required fix

Separate:

```text
CAMPAIGN HEAD
    transport/current-tree pin for one transaction

SOURCE-DOMAIN BASIS / WATERMARK
    owner-defined projection enumeration boundary
```

A `StorySourceBundle` may be read from a tree pinned at campaign HEAD H, but catch-up coverage is compared only against typed source-domain basis/watermarks defined by source owners.

Story-only HEAD movement does not advance any canonical source-domain watermark unless it actually changes that source domain.

## Resolution

**BLOCKER RESOLVED TECHNICALLY.** Canonical spec must forbid campaign HEAD/Git order from acting as Story source coverage frontier.

---

# 4. BLOCKER C — mutable Story progress in MANIFEST/CURRENT would destroy proven-disjoint Story movement

## Attack

Machine realization still needs a `story_root`. A tempting implementation is to place Story progress such as:

```text
MANIFEST.story_frontier
CURRENT.story_projection_cursor
```

Then every Story-only commit touches MANIFEST/CURRENT, which are canonical routing/current-state surfaces used by gameplay.

That would make “Story-only movement is semantically disjoint from ordinary gameplay” harder or false at the physical dependency level.

It would also repeat Step-5.0 contamination mistakes.

## Required fix

`MANIFEST.storage.story_root` or equivalent **static routing/configuration** may be introduced during scaffold/migration.

But mutable projection state must live under the Story-owned projection surface itself.

Prohibit ordinary Story progress fields in:

```text
MANIFEST
STATE/CURRENT
checkpoint/RRC state
canonical runtime allocator
```

Ordinary Story catch-up should therefore change Story paths only.

## Resolution

**BLOCKER RESOLVED TECHNICALLY.** Add explicit placement/authority prohibition to canonical spec and machine debt.

---

# 5. BLOCKER D — source compaction can invalidate the meaning of an old cursor

## Attack

Step 5.11/5.13 may compact exact source records/segments. If a layer stores cursor K that only makes sense by dereferencing a deleted source item/segment, later enumeration cannot resume boundedly.

This would turn a valid Story projection into a full-history recovery problem.

## Required fix

Every source projection-domain contract must define cursor continuity across lawful source compaction.

One of these must hold:

```text
A. cursor token remains interpretable after compaction
B. retention keeps a compact source enumeration anchor/index
C. compaction atomically migrates Story coverage to a successor compatible cursor
```

Step 5.10 defines the requirement. Step 5.11/5.13 own the physical retained artifact/migration.

Do not retain full source payload merely to preserve cursor continuity when a smaller enumeration anchor suffices.

## Resolution

**BLOCKER RESOLVED TECHNICALLY.** Add a typed cursor-continuity handoff to 5.11/5.13.

---

# 6. BLOCKER E — concurrent workers can use incompatible projection-contract generations

## Attack

Future Step-6 worker A may still run G1 while worker B runs G2. Both can observe the same Story layer state and attempt to advance coverage.

If G1/G2 have different candidate/disposition semantics, accepting either writer blindly may make current coverage uninterpretable.

## Required fix

A Story publication attempt freezes the exact active projection contract generation(s) used to interpret every coverage entry it advances.

Before publication, deterministic core validates that current target Story layer state still accepts those contract generations.

Incompatible generation movement is not a remappable allocator-only conflict. It requires typed projection-state migration/reassembly rather than advancing old coverage.

## Resolution

**BLOCKER RESOLVED TECHNICALLY.** Treat semantic projection-contract generation as part of the Story transaction dependency footprint.

---

# 7. Strengthening finding F — source-domain enumeration must be append-monotonic with respect to projection work

A contiguous cursor is safe only if the source contract guarantees that ordinary new candidates do not later appear “behind” a previously accepted cursor.

Late historical facts/relations are still allowed: they enter as **newly accepted source evidence at a later projection-enumeration position**, even when they concern old fictional time.

If a source cannot provide append-monotonic projection enumeration, it must use typed sparse coverage or another owner-defined bounded mechanism.

No Story layer may fake monotonicity by sorting on fictional chronology, ID lexicography or Git timestamp.

---

# 8. Strengthening finding G — `MUST_MATERIALIZE` may need layer-specific cardinality

“At least one Story record” is not universally sufficient.

For example, an exact retained transcript candidate may require exactly one corresponding Transcript record; another source family may permit one-to-many mapping.

Therefore the projection contract may define candidate-specific terminal mapping constraints beyond the base classes:

```text
MUST_MATERIALIZE
MAY_OMIT
+ owner-defined cardinality/shape validation where needed
```

Do not create a universal mapping algebra until concrete layer requirements require it.

---

# 9. Strengthening finding H — TRANSCRIPT candidate admission depends on 5.11/5.12 boundaries

Step 5.10 cannot safely decide that a generated Narrator string is a participant transcript candidate merely because text exists.

The exact participant-message/utterance source and delivered/emitted boundary interact with:

- Step 5.11 exact transcript retention;
- Step 5.12 host delivery/disclosure acknowledgement.

Therefore Step 5.10 defines only the projection protocol once a transcript source-domain candidate is admitted by those contracts.

A generated-but-never-emitted player-facing narration must not become retained transcript merely through projection.

This is a named handoff, not a reason to block 5.10 closure.

---

# 10. Strengthening finding I — Story-to-Story refs cannot become factual source authority

NARRATIVE may reference EVENTS/MECHANICS/TRANSCRIPT, but a lower Story record is still non-canonical projection.

If NARRATIVE factual correctness depended solely on mutable lower-layer prose, correcting that lower layer could require a complex automatic downstream invalidation system.

The simpler inherited Step-4 rule is stronger:

> Material factual claims in Story remain traceable to authoritative/historical `source_refs`; Story-to-Story refs are presentation/navigation/editorial dependencies, not promotion of lower Story prose to factual authority.

Therefore a lower-layer editorial wording correction does not automatically invalidate all dependent NARRATIVE records merely because they reference its Story ID.

A structural edit must still preserve no-dangling Story refs. A newly established canonical/source correction enters its own source projection domain and may trigger explicit Story correction/regeneration.

No generic Story dependency invalidation engine is required baseline.

---

# 11. Race matrix after blocker fixes

## 11.1 Story writer vs canonical writer

```text
Story wins ref first
    -> gameplay sees verified Story-only movement
    -> transport-only rebuild on newer base
    -> no gameplay semantic replay

Gameplay wins ref first
    -> Story checks frozen source/layer/availability footprint
    -> reuse draft if compatible
    -> otherwise discard/reassemble
```

## 11.2 Story writer vs same-layer Story writer

```text
winner advances allocator/coverage atomically
loser refreshes
    if source window now covered -> discard draft
    if compatible uncovered remainder exists -> revalidate/remap or regenerate later
```

## 11.3 Story writer vs different-layer Story writer

Target layer state is normally disjoint. Loser may mechanically rebase if cross-layer refs/dependencies remain valid.

## 11.4 Contract-generation movement

Never treat incompatible semantic projection-contract movement as disjoint merely because record paths differ.

---

# 12. Ambiguous-ack attack after contract typing

Coverage-only idempotency remains valid only when interpreted under the same compatible contract generation.

Recovery checks conceptually:

```text
current coverage.contract_ref compatible with intended contract_ref?
    no -> migration/reassembly path
    yes -> compare source-domain coverage
```

If compatible current coverage already passes the intended source window, duplicate publication is suppressed.

No durable job/run identity becomes necessary.

---

# 13. Compaction attack: Story is caught up, then source cursor anchor is removed

The stronger rule is now:

> A retention/GC operation that preserves Story coverage but destroys the ability to interpret/resume that coverage is not safe compaction.

This feeds Step 5.11/5.13 alongside source-fidelity obligations.

Story coverage itself is compact projection evidence and should normally be retained while the layer remains active even if many old Story records are editorially deleted.

---

# 14. Plain-ChatGPT deployment attack

Current product constraints do not justify any new persistent scheduler:

- no required background worker;
- Work excluded by owner for ordinary HDM;
- Pro/Enterprise assumptions excluded;
- Scheduled Tasks are not a per-turn repository/project Story worker contract;
- Step 6 may later provide separate invocations/API orchestration.

Candidate remains viable because **absence of projection execution only increases lag**. It does not create pending gameplay work.

This is a major success criterion of the candidate.

---

# 15. YAGNI sweep

After review, remove/defer all of the following from baseline 5.10:

```text
StoryProjectionJob entity
worker lease/claim
background polling loop
projection-run durable receipt
cross-layer global frontier
per-source skip records for cursor-capable domains
model/prompt version as replay authority
campaign HEAD as projection source watermark
CURRENT/MANIFEST mutable Story progress
automatic downstream invalidation graph over Story prose
mandatory Story tombstones
stable external permalink guarantee
Story catch-up in gameplay SAVE/RRC
```

Retain only contract generation, source-domain coverage, Story-local allocator/indexes, typed source bundles/drafts and deterministic publication control.

---

# 16. Required candidate amendments before canonicalization

Canonical spec must add/strengthen:

1. source projection contract generation identity;
2. semantic-versus-cosmetic projector-change distinction;
3. append-monotonic source projection enumeration requirement;
4. campaign HEAD is transport pin, never source coverage watermark;
5. mutable Story progress is forbidden in MANIFEST/CURRENT/RRC/checkpoint state;
6. source cursor continuity through 5.11/5.13 compaction;
7. incompatible contract-generation concurrency handling;
8. layer-specific terminal mapping/cardinality validation;
9. Transcript admission handoff to 5.11/5.12;
10. Story-to-Story refs remain non-authoritative presentation dependencies.

---

# 17. Owner-decision check

None of the blockers creates a material product/semantic choice requiring owner arbitration.

The surviving baseline promises remain deliberately minimal and already aligned with owner constraints:

- Story is eventually/opportunistically fresh, not freshness-SLA-bound;
- no Work/background/Pro/Enterprise dependency;
- no permanent source-payload dereference promise from 5.10 alone;
- no stable external Story permalink promise across arbitrary structural rewriting;
- Story cannot participate in gameplay authority.

No new owner decision is requested at this gate.

---

# 18. Review disposition

**PASS WITH REQUIRED TECHNICAL AMENDMENTS.**

The candidate direction survives adversarial review.

Confidence after blocker resolution: **HIGH**.

Next step: resolution gate that incorporates these amendments, then canonical specification if the gate finds no new material trade-off.
