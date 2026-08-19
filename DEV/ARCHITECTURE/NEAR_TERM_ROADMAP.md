# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes only after required artifacts/review/verification pass and every
  unresolved item has a later owner or explicit deferred/debt/backlog record.
- Step closure updates this roadmap and
  `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`.
- After all major modules have designs, run one holistic architecture review over
  the complete ownership graph, schemas, logic, and cross-module relationships.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Owned audit ledger + retrospective assurance | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases + retrospective assurance | No unresolved Step-2 blocker; maintenance/schema/unit-test validation passes |
| 3 | **COMPLETE — FINAL SAME-HEAD CI REQUIRED FOR CLAIMED CLOSURE** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary, Procedure ownership and checkpointable continuation | Canonical Alternative-C execution contract + machine schemas/catalogs + A–N cases + adversarial/final critical review | Final documentation/status HEAD passes maintenance audit, full DEV unit suite and `Validate engine source` |
| 4 | **IN PROGRESS** | Lore, chapters, knowledge, secrets, disclosure, narrative projections, minimum promotion interface | One durable truth/disclosure model + knowledge-safe LLM context + transcript/SemanticEvent/Chapter projection contract | Public/restricted knowledge has one authority; durable references cannot depend on unpromoted local entities; narrative projections cannot become alternate truth; spectator/public projection has a safe visibility boundary |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, event-local time | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model | Publication/live-scene ownership, cross-scene recovery, chronology, local time, continuity restoration, public/private projection transport, and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, LLM execution budget, migration, catalog gaps, full seed, final closure | Mode profiles + final cross-cutting consistency pass | Mode isolation enforceable; migration/gap/seed ownership complete; full audit passes |

## Steps 1–2 retrospective assurance

The non-numbered retrospective assurance overlay is complete. Final resolution:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Steps 1–2 remain closed and assured.

## Step 3 closure chain

Owner-approved architecture: **Alternative C**.

Canonical/review artifacts:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- `DEV/docs/superpowers/plans/2026-08-19-step-3-execution-boundary-machine-contract.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Current Step-3 machine baseline:

```text
catalog_version = 1.4.0

Interaction
    -> IntentPlan
        -> RuntimeCommand
            -> ActionRequest -> Resolution(Activity)
            OR
            -> TransitionRequest -> direct deterministic execution

RuntimeCommand
    root mandatory execution-chain closure owner

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded ExecutionSegment(s)
        -> committed MechanicalEvents
        -> receipts / idempotency
        -> mandatory child descriptors

Continuation
    portable suspended Resolution generation
```

Key Step-3 closure points:

- IntentPlan is ordered message orchestration, not a transaction;
- Resolution means exactly one Activity invocation;
- deterministic transitions do not require fake Activities;
- RuntimeCommand owns root mandatory descendant closure; no
  `runtime.resolution_chain` exists;
- ExecutionSegment is embedded under an independent execution owner; no
  `runtime.execution_segment` exists;
- `runtime.procedure` exclusively owns procedure-local spent ResourceState;
- reaction children share Procedure by reference and parent recomputes from a
  safe phase after expected child commits;
- mandatory post-commit child identity is representable in the same committed
  segment as the triggering Event;
- MechanicalEvent identity is segment + stable ordinal;
- invocation facts are explicit registered booleans with provenance; missing is
  distinct from false and engine-owned facts cannot enter this channel;
- incompatible ResolvedCatalogContext adoption cannot silently reinterpret an
  in-flight command/continuation;
- Effect recency uses compact target/application-family-local immutable episode
  order evidence rather than wall time or retained trace bodies;
- same-coordinate advancement cannot pass unresolved mandatory due work;
- scheduled owner-local triggers enter ordinary child Resolution execution;
- final narration is normally based on mechanically settled receipt closure and
  never becomes mechanical authority.

Focused integrated cases A–N cover ordinary action, reactions, post-commit
follow-ups, partial multi-intent completion, direct transitions, clarification,
retry identity, suspended recovery, boundary occurrence, scheduled due work,
Procedure sharing, incompatible catalog contexts, execution-chain limits, and
Effect recency after trace compaction.

The final critical review reports zero unresolved Step-3 blockers. The only
remaining closure condition is fresh `Validate engine source` success on the
final roadmap/status/documentation HEAD.

## Step 4 — active architecture stage

Step 4 now owns the boundary among objective truth, disclosure/knowledge,
conversation history, semantic campaign history and authored narrative.

Primary problem graph:

```text
world/lore truth authority
    -> knowledge/disclosure authority
    -> knowledge-safe LLM context

runtime.message / retained transcript
    + committed MechanicalEvents/world/lore truth
        -> runtime.semantic_event
            -> world.chapter
                -> optional spectator/public projection
```

The layers are not alternate truths:

- transcript preserves what participants actually said when retained;
- MechanicalEvents are technical committed mechanics facts;
- SemanticEvents are compact campaign-history facts/projections;
- Chapters are authored human-readable narrative/history projections.

Step 4 must determine which claims each projection may make, how they anchor to
truth/knowledge authority, how secrets remain inaccessible to unauthorized
contexts, and when a situational invocation-adjudicated fact may be promoted to
durable lore.

### Mandatory Step-4 questions

1. What is the sole authority for objective propositions, disputed claims and
   unknown/unresolved truth?
2. What is the sole authority for who knows what and what a given player/LLM
   context may see?
3. How do SemanticEvents compact MechanicalEvents/world changes without becoming
   a second writable world state?
4. How do Chapters cite/cover SemanticEvents/lore while remaining editable
   narration rather than canon authority?
5. What transcript subset, if any, is retained durably, and which layer owns
   dialogue fidelity versus story truth?
6. How are public/spectator projections generated so private secrets never leak
   merely because the private campaign Git repository contains them?
7. What promotion closure is required before a durable lore/event/chapter
   reference can point to a currently local entity/definition?
8. How are LLM discovery/context candidates filtered by knowledge/disclosure
   without forcing full campaign state into model context?

## Step 5 carry-forward

Step 5 will own physical repository publication/restoration and shared-state
behavior after Step 4 fixes the semantic visibility boundary, including:

- checkpoint publication/restoration;
- SOFT/HARD durability;
- multiplayer/shared Procedure conflicts;
- chronology evidence and cross-scene reconciliation;
- private canonical versus public/spectator Git projection transport;
- transcript/history retention/compaction mechanics;
- checkpoint cleanup/expiry.

## Step 6 carry-forward

Step 6 retains:

- exact engine/ruleset/package/catalog snapshot metadata;
- full D&D seed and migration/catalog-gap closure;
- complete selector/input/dependency metadata coverage;
- proven specialized simultaneous/scheduled ordering rules;
- modes and LLM execution budget;
- final holistic architecture/catalog/seed audit.

## Documentation debt

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and
`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` are historical derivation
material with examples/version labels predating current canonical Step-2/3
contracts. They are non-authoritative relative to `CATALOG_INVENTORY.md`, machine
catalogs/schemas and the canonical specs. Add/strengthen supersession warnings
before implementation work relies on those examples.

## Exact continuation point

**Step 4 / Lore, Knowledge, Disclosure, Narrative Projection, and Promotion.**

Begin with a solution-blind Task Brief over truth/knowledge/projection ownership,
including the spectator-safe transcript → SemanticEvent → Chapter requirement.
