# S6D-08 Step 5 — Candidate Specification

Status: **CANDIDATE REALIZED RED→GREEN**

Date: 2026-08-26

## Candidate

Adopt DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md as the single integration owner while retaining domain authority in Actor, ResourceDefinition/owner state, world.effect, derived Condition aggregation, chronology and Step-3 execution.

Machine realization:

1. materialized Actor hp requires current and maximum_base;
2. unused definition.resource resource.hit_points is removed from the S6D-07 package and its content identity is updated;
3. health-effects-recovery-seed.json records exact supported owner routes, complete character-like zero-HP/death/stable-recovery transitions, S6D-07 recovery responders, Effect/Condition/temporal cases, durability reconstruction and negative space;
4. the package binds a closed two-file content set through per-file and aggregate digests;
5. strict schema and reference validation cover transitions, retry, boundaries, Effect replacement/expiry/support, derivative rebuilding and negative states while forbidding duplicate owners, scheduler/queue/global scan, RestPolicy mutation authority and new primitive activation.

## TDD evidence

RED: the focused test failed because health-effects-recovery-seed.json did not exist.

First GREEN: ten focused assertions passed. Independent review exposed missing executable closure; the repair cycle added ten behavioral/negative tests. Current GREEN is twenty focused assertions.

## Compatibility and activation

No released campaign migration exists. Package content identity changes because an invalid unused support definition is removed and the S6D-08 machine seed joins the exact content set. Existing active primitive consumer sets do not change. Periodic content, generic concentration and partial Exhaustion remain nonselectable.

## Acceptance walkthroughs

1. Damage uses the reviewed op.apply_damage consumer, consumes temp HP then HP, proposes LifeState in the same segment, commits once, emits event/receipt.
2. Second Wind consumes its Actor use pool and heals Actor hp; a short-rest occurrence later invokes only the named Resource responders.
3. Sorcerer spell slots and Innate Sorcery recover on long-rest completion; RestPolicy only qualifies/emits.
4. Innate Sorcery creates/replaces one target-source-definition Effect with its local one-minute binding; due index loss is repaired from the Effect.
5. Unconscious is derived from applicable Effect sources; Exhaustion aggregates per-unit sources and removes one at the long-rest boundary.
6. Support-root termination ends dependent Effects; the conformance case activates no new package content.
7. Crash/retry restores owner state and fixed causal inputs, rebuilds derivatives, and deduplicates by occurrence/responder or Resolution identity.

## Candidate exit

The candidate closes the stated S6D-08 scope without a second lifecycle, scheduler, query engine, generic mutation channel or content-breadth expansion.

