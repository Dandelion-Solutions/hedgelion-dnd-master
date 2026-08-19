# HDM Engine Design Process

Status: **AGREED — PROJECT-SPECIFIC ADAPTER**

## Purpose and authority

The canonical generic architecture/deep-work procedure is:

`DEV/DESIGN_PROCESS.md`

That document governs task classification, human/agent decision rights,
research and evidence discipline, analytical challenge, the eight-step
deep-design loop, adversarial review, canonicalization, deferred work, risk,
traceability, and the transition from architecture into implementation planning.

This file adds HDM-specific constraints. It must not be interpreted as a weaker
alternative process.

## Superpowers requirement

Superpowers is a required development-process aid for HDM engine architecture.
It is not part of the game runtime, campaign bootstrap, release package, or
player environment. A campaign must never depend on the plugin being installed.

For architecture/deep-work blocks:

1. use the process in `DEV/DESIGN_PROCESS.md`;
2. invoke the applicable current Superpowers skills, beginning with
   `superpowers:using-superpowers` and using `superpowers:brainstorming` for
   architectural work;
3. use `superpowers:writing-plans` only after the relevant canonical design is
   approved;
4. keep Superpowers artifacts under the repository locations defined by
   `AGENTS.md`.

## HDM decision rights

Product requirements, gameplay semantics, project priorities, explicit risk
acceptance, and material architecture trade-offs remain owned by the project
owner/human architect.

The agent is responsible for the research, analytical challenge, recommendation,
mechanical formalization, detailed examples, consistency checking, critique
resolution, roadmap/status bookkeeping, and specification completeness required
by `DEV/DESIGN_PROCESS.md`.

Do not make the owner compensate for incomplete analysis by presenting raw
options without a recommendation, or by asking for manual validation of
mechanical documentation details that follow from already accepted decisions.

## HDM architecture sequencing gate

The active mechanical-architecture sequence is maintained in
`DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.

For that roadmap:

- exactly one numbered stage may be `IN PROGRESS`;
- a later stage may be examined when it exposes a dependency or contradiction
  relevant to the active stage, but it may not silently replace the active
  stage;
- a stage is complete only when its required artifacts exist, its exit checks
  pass, and unresolved work is explicitly owned, deferred, or recorded in the
  appropriate backlog/debt mechanism;
- architecture is reviewed before implementation;
- accepted decisions must remain compatible with existing canonical HDM
  architecture unless an explicit superseding decision is made;
- the roadmap and related architecture status must identify the exact next
  continuation point.

## HDM-specific analytical emphasis

In addition to the generic review gates, HDM architecture work must explicitly
look for risks created by the interaction between deterministic mechanics and
LLM-driven reasoning.

As relevant, challenge designs for:

- duplicate authority over canonical state;
- LLM output bypassing deterministic validation;
- narrative text becoming an accidental mechanical source of truth;
- inability to replay or recover committed mechanics deterministically;
- hidden coupling between GAME runtime contracts and DEV-only tooling/process;
- campaign/runtime dependence on development-only files;
- ambiguous state ownership across Actor, Asset, Effect, Resource, lifecycle,
  procedure-local state, and persistence layers;
- expensive campaign-wide scans or indexes where scoped ownership can provide a
  bounded query;
- cross-scene or multiplayer behavior that invalidates assumptions made by a
  single-scene design;
- hard-coded D&D rules where a registered policy/mechanic is required for
  extensibility;
- generic abstraction introduced without a concrete current requirement.

## Development/runtime separation

This process applies only to engine architecture and related development work.

It must not add calls, context, latency, workflow objects, schema fields, or
runtime dependencies to an ordinary HDM gameplay turn merely to represent the
development process.

Development process, architecture drafts, Superpowers artifacts, tests, and
maintenance tooling belong under `DEV/` as governed by `AGENTS.md`.

Runtime behavior shipped to players belongs under `GAME/`.

## Unavailable-Superpowers rule

If the required Superpowers capability is not exposed in the current work
environment after its connection is checked:

- report the observed limitation rather than claiming the skill was used;
- do not mark a deep architecture block canonical merely by silently replacing
  the required process with an improvised one;
- research and clearly labelled drafts may continue where useful;
- only an explicit project-owner decision, made after the limitation is stated,
  may authorize a documented fallback for that block;
- such an exception does not disable the process gate for later work.

## Evidence without runtime bureaucracy

The design process itself should be visible through development artifacts, not
through product/runtime state.

Normally it is sufficient that the roadmap/specification history shows:

- the workflow/review performed;
- the decisions made;
- material risks/findings and their disposition;
- intentionally deferred work;
- the exit-gate state and next continuation point.

Do not create runtime entities solely to prove that architecture review occurred.
