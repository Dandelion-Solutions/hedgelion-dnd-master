# HDM Implementation Planning Package — Impact/TDD Contract

Status: **PB-01 PACKAGE PROTOCOL**
Date: 2026-09-13

This file defines the mandatory implementation-task structure used by every RD plan in the current package.

## TDD task shape

Each task uses RED -> GREEN -> REFACTOR -> VERIFY.

1. **Files** — exact create/modify/replace/retire/test paths.
2. **Interfaces** — inputs, outputs, schema members, IDs, transitions or callable contracts affected.
3. **RED** — exact failing test/scenario/static assertion and why it must fail before implementation.
4. **GREEN** — minimal owner-correct implementation needed to pass, with unrelated cleanup excluded.
5. **REFACTOR** — allowed cleanup while behavior and authority boundaries remain unchanged.
6. **VERIFY** — focused command plus applicable broader suite/audit and expected evidence.
7. **Commit boundary** — coherent recoverable checkpoint; multiple microsteps may share one commit.

Tests must cover positive behavior and material negative laws. Deterministic/static evidence cannot substitute for future empirical/release evidence owned by another trigger.

## HDM Impact Envelope

Every task or tightly coupled task group states:

```text
Primary owner artifacts:
GAME runtime/projection surfaces:
DEV schemas/catalogs/machine contracts:
Direct runtime consumers:
Persistence/recovery/currentness consumers:
Validators/tests/audits:
Documentation/install/package projections:
Cross-RD joins:
Explicit exclusions / authority not transferred:
Version Impact: NONE | PATCH | MINOR | MAJOR | DEFERRED-TRIGGER
Schema/catalog/checkpoint impact:
Migration impact:
HG-01 constraints affected:
Currentness/re-read set before write:
```

The envelope follows actual ownership/dependency impact, not directory adjacency. Rename/restructure tasks include transitive stale-reference consumers. `Version Impact: NONE` needs a reason when a touched contract could plausibly affect version/checkpoint semantics.

## Negative-law proof

Every RD plan contains a `Forbidden outcomes / negative-law proof` section. Each material forbidden outcome gets a test, scenario or inspectable static proof route.

Typical forbidden classes include:

- second canonical/state/knowledge/history/currentness authority;
- narrative or model prose becoming direct mechanics authority;
- cache/index/derived projection becoming authoritative;
- chronology/currentness inferred from IDs, SQL order or transport order;
- visibility implying player knowledge;
- retry/recovery replaying accepted mechanics or rerolling fixed RNG;
- role/diagnostic/tool output bypassing protected emission;
- cross-scope collaboration creating a global active-player/frontier/synchronization owner.

Only RD-specific applicable laws are copied into an individual plan.

## Version, migration and checkpoint routing

Every task records version impact against the current version owner. Schema/catalog changes must keep coherent owner-family version/checkpoint rules.

Migration execution is not authorized by this planning package. Plans distinguish:

- implementation required in the current future execution wave;
- migration design/proof required by that implementation;
- migration execution deferred to its authorized stage/trigger.

The 12 trigger-gated readiness routes remain dormant until their exact release/real-target/writer/focus-risk trigger exists.

## Completion evidence

An RD plan is worker-ready only when every task has executable evidence instructions and the RD ending contains:

```text
focused tests: specified
applicable broader audit/suite: specified
readiness obligations: fully mapped
composite contribution: explicit
pure-proof target/routes: explicit
version/checkpoint impact: explicit
stale-reference search: specified where structural changes occur
next dependent joins: explicit
recommended implementation checkpoint boundaries: explicit
```

No production worker may execute these plans before the complete package receives independent Senior PASS / GO.
