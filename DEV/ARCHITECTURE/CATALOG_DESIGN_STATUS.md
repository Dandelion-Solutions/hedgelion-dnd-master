# HDM Catalog Design Status

Status: **STEPS 1–4 ARCHITECTURE CLOSED / STEP 5.0 COMPLETE — AWAITING OWNER REVIEW / STEP 5.1 NOT STARTED**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in linked architecture/spec documents and Git
history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Current checkpoint

Steps 1–2 are complete and retrospectively assured.

Step 3 is closed: owner decision, candidate, adversarial review, canonical spec,
machine-contract TDD alignment, integrated A–N cases, final critical review and
same-head validation completed successfully.

Step 4 completed its full architecture rerun after adoption of six logical LLM
roles. Its architecture is closed. The obsolete literary Chapter world surface
has been removed from the active machine catalog and current normative catalog
documents.

Step 5 remains the sole active numbered architecture stage. Its first bounded
architecture slice, **5.0 Authority / Contamination Audit**, completed the full
design cycle and approved cleanup. Step 5.1 has not started and must not start
until the owner reviews the 5.0 result.

Per owner direction, broad implementation planning for the remaining Step-4/5/6
contracts waits until the remaining architecture sequence is complete.

## 2. Current machine baseline

Active catalog version: `1.6.0`.

Catalog `1.5.0` retired the old literary Chapter world vocabulary. Step 5.0 then
advanced the coherent machine catalog to `1.6.0` to retire additional early
abstractions that had no surviving accepted independent owner contract:

```text
world.timeline_marker          removed
transition.timeline_place      removed
event.timeline.placed          removed
runtime.dirty_record           removed
runtime.publication_batch      removed
```

Numeric/local sparse ordering remains available as an ordering value rather
than an independently identified world record. Dirty bookkeeping and publication
transactions remain required operational concepts; Step 5.5/5.6 must prove an
independent lifecycle before any corresponding runtime record can be re-admitted.

All four coordinated machine catalog files are `1.6.0`:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

Step 5.0 also removed active storage/schema affordances that could have leaked
obsolete ownership into later design:

```text
GAME/CAMPAIGN/WORLD/SECRETS/
GAME/SCHEMA/secret.schema.yaml

GAME/CAMPAIGN/STATE/TACTICAL/
scene.tactical_state_path

STATE/CURRENT.pending_global_consequences

STATE/CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml

MANIFEST.world_time.frontier
MANIFEST.last_event_id
```

The resulting active routing rules are:

- `MANIFEST.last_checkpoint_id` is the sole latest-checkpoint pointer;
- `CURRENT.world_time.frontier` remains the compact globally reconciled
  chronology frontier pending Step 5.1/5.9;
- `CURRENT.last_event_id` remains a provisional semantic-log/recovery cursor,
  not fictional total-order authority;
- current campaign paths are branch-root-relative (`STATE/`, `WORLD/`, `LIVE/`,
  `LOG/`, `CHECKPOINTS/`); obsolete campaign-storage `CAMPAIGN/...` wrapper
  spelling is not current runtime routing;
- `GAME/CAMPAIGN/` remains only the engine-source template directory whose
  contents are copied into a new campaign branch root.

This catalog/version cleanup does **not** claim that deferred Step-4/5 machine
realization already exists.

## 3. Current accepted execution/runtime owners

The Step-3 owner graph remains intact:

```text
Interaction
    -> IntentPlan
        -> RuntimeCommand
            -> ActionRequest -> Resolution(Activity)
            OR
            -> TransitionRequest -> direct deterministic execution

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded ExecutionSegment(s)
        -> MechanicalEvents
        -> receipts/idempotency
        -> mandatory child descriptors

Continuation
    one portable suspended Resolution generation
```

Accepted runtime records retained through Step 5.0 include:

```text
runtime.session
runtime.message
runtime.interaction
runtime.intent_plan
runtime.command
runtime.resolution
runtime.procedure
runtime.continuation
runtime.mechanical_event
runtime.semantic_event
runtime.resolution_trace
runtime.checkpoint
runtime.id_allocator
runtime.maintenance_audit
runtime.catalog_gap_report
```

Their eventual durable placement/recovery enumeration is a Step-5 concern; it is
not permission to create a generic runtime snapshot owner.

## 4. Step-4 information architecture remains authoritative

Canonical Step-4 specification:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`

Authority remains:

```text
OBJECTIVE / CURRENT
    ordinary world state owners
    world.lore_fact

FICTIONAL CURRENT PERSPECTIVE
    world.knowledge

HUMAN PLAYER EXPOSURE
    runtime.disclosure

HISTORICAL EVIDENCE
    runtime.semantic_event / LOG
    runtime.mechanical_event

ROLE CONTEXT
    deterministic Context Assembler
        -> Interpreter
        -> Dramaturg
        -> Actor
        -> Narrator
        -> Chronicler
        -> Commentator

NON-CANONICAL PRESENTATION HISTORY
    STORY/
        TRANSCRIPT/
        EVENTS/
        MECHANICS/
        NARRATIVE/
```

No generic Secret authority survives. Removal of the old Secret schema/template
slot in Step 5.0 enforces that already-accepted semantic result; it does not yet
perform the broader Step-4 migration of embedded legacy knowledge fields.

## 5. Step 5.0 full-cycle artifacts

Expanded Step-5 agenda:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-expanded-architecture-agenda.md`

Step 5.0 design chain:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-research-draft.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-adversarial-review.md`

Accepted 5.0 rule:

> an active catalog/template abstraction that appears to own semantics but has
> no surviving accepted independent owner/lifecycle contract is removed rather
> than left as a machine-visible placeholder. A later slice may re-admit a
> suitable abstraction only after proving the need.

The audit intentionally distinguishes this from accepted owners whose durable
placement is merely not yet designed.

## 6. Explicit carry-forward after 5.0

Step 5.0 does not decide:

- exact frontier/recovery-cut representation;
- durable placement/enumeration of active RuntimeCommand/Resolution/Procedure/
  Continuation roots;
- exact dirty-set representation;
- whether publication preparation ever needs independent durable identity;
- publication-manifest final wire shape;
- pending-work no-lost/no-double recovery protocol;
- exact multiplayer/live-epoch reconciliation redesign;
- chronology persistence representation;
- whether sparse numeric sequence keys are useful inside specific chronology
  domains;
- Story publication/catch-up/retention;
- transcript retention;
- host delivery/disclosure acknowledgement;
- GC/orphan cleanup frontiers.

These remain owned by the corresponding later Step-5 slices in the expanded
agenda.

## 7. Deferred Step-4 machine realization

The integrated implementation program after Steps 5–6 must still realize, test
and migrate at least:

- `world.lore_fact` truth/lifecycle normalization;
- `world.knowledge` stance/current-owner normalization;
- `runtime.disclosure` record/schema/provenance;
- knowledge/disclosure transition and event contracts;
- Context Assembler request/bundle/source-manifest contracts;
- role-specific eligibility and disclosure-delivery tests;
- Story root/layout/IDs/shards/index/four-layer schemas;
- dependency-based Story availability;
- legacy embedded-knowledge migration;
- live-scene knowledge/disclosure compaction alignment.

These are explicit deferred implementation obligations, not unresolved Step-4
architecture questions.

## 8. Exact continuation

Current review point:

> **Step 5.0 / Authority & Contamination Audit — COMPLETE, awaiting owner review.**

**Step 5.1 / Frontier Model is NOT STARTED.**

Do not begin Step 5.1 or broad implementation planning until the owner reviews
this 5.0 result and explicitly continues the architecture sequence.
