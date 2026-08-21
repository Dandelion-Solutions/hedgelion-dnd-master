# Step 4 Rerun — Adversarial Resolution Gate

Status: **RESOLVED — READY FOR CANONICAL CONSOLIDATION**

Date: 2026-08-20

Inputs:

- `2026-08-20-step-4-rerun-candidate-spec.md`
- `2026-08-20-step-4-rerun-adversarial-review.md`

## 1. Gate result

All adversarial findings are either:

- accepted as mechanical amendments to the canonical consolidation;
- assigned to Step 5 or Step 6 without weakening Step-4 semantics; or
- rejected with rationale.

No finding introduced a new material product/authority trade-off.

```text
unresolved owner blockers: 0
accepted Step-4 amendments: 10
later-owner findings:       4
architecture debt created:  0
```

Proceed to canonical consolidation.

## 2. Accepted amendments

### R4.1 Dependency-based Story availability

Replace ambiguous scalar `reveal_frontier` semantics with dependency/reference-based availability requirements.

A Story record/index entry may be exposed to Commentator only when its required reveal anchors are satisfied by the active spectator mode/session state.

Editorial sequence may guide UX but is not objective world chronology.

### R4.2 Restore `epistemic.known`

Initial fictional stance vocabulary becomes:

```text
epistemic.aware
epistemic.known
epistemic.believed
epistemic.suspected
epistemic.rejected
```

`known` covers information legitimately available to a subject as established in-fiction knowledge through a qualifying source. Voluntary belief/suspicion/rejection remain subject/player agency where applicable.

### R4.3 Physical context incompatibility rule

A narrower role cannot execute in a physical model invocation that still contains source material ineligible for that role.

Role co-location is permitted only if source eligibility is compatible or the platform provides genuine context reset/isolation. Otherwise Step 6 must use separate invocations.

### R4.4 Lore proposition identity immutability

After durable external reference, identity-defining statement and material scope/subject/chronology qualifiers cannot be semantically rewritten in place.

Truth-status transition for the same proposition is allowed. A materially different proposition receives a new ID and explicit supersession/reference.

### R4.5 Disclosure delivery boundary

Disclosure means emitted/accepted onto the player-facing host surface, not proof the human actually read the message.

Transport acknowledgement details remain Step 5/host implementation.

### R4.6 Exact truth-revision exposure

Objective-status disclosure references the exact committed lore truth-transition/correction evidence. Later truth changes or supersession do not become disclosed transitively.

No new generic revision record is introduced.

### R4.7 Story metadata/index eligibility

Availability applies to the full retrieved presentation unit, including titles, refs, entity identities and index entries that may themselves be spoilers.

### R4.8 Availability recomputation on Story edits

A material Story edit must recompute/revalidate its availability requirements before publishable Story output is accepted.

### R4.9 Inspectable RoleContext source manifest

RoleContextBundle includes bounded source identities sufficient for test/debug attribution. It is working/trace evidence, not canonical authority.

### R4.10 Bounded current knowledge provenance

`world.knowledge` stores only provenance needed to support/explain the current stance. Full transition history remains in LOG/SemanticEvents.

## 3. Later-owner assignments

### Step 5

- atomic/coherent Story body/index/availability publication;
- concurrent Story ID allocation/publication;
- exact host response-delivery acknowledgement;
- Story/transcript retention/compaction transport.

### Step 6

- physical role-call compatibility matrix;
- required model-call isolation where context eligibility differs;
- default Commentator spoiler/perspective mode;
- optional semantic narration verification/evaluation;
- token/cost/latency/model selection.

## 4. Residual generative limitation accepted

Role-specific context selection cannot mathematically prove that free-form LLM prose will never hallucinate an unsupported factual sentence from model priors.

The architecture instead guarantees:

- hidden source data is not deliberately supplied to ineligible roles;
- material role inputs are typed/grounded;
- unsupported narration is a correctness error;
- Narrator/Commentator prose is never canonical authority;
- optional semantic output checking may be added as Step-6 quality machinery without becoming truth authority.

This residual model-quality risk does not alter the accepted authority architecture.

## 5. Gate decision

**READY FOR CANONICAL CONSOLIDATION.**

Confidence: **HIGH**.
