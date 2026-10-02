# W05.T06-A1 — Step 3 Decision Brief

Status: COMPLETE

## What is being decided

How to realize two already accepted T06 consumers:

1. current deterministic READY_PC/local mechanical sufficiency;
2. ordinary active-player Master retrospective over current and historical game evidence.

This is machine architecture, not a new product-semantics choice.

## Why now

T06 implementation is correctly held because neither consumer has an admitted production boundary. Existing Context Runtime also reads pinned campaign state while accepted unpublished HOT/SOFT may be current, so a local patch would preserve a correctness defect.

## Distinguishing requirements

- current truth must include accepted HOT/SOFT and selected LIVE where owned;
- Story may not become current truth, History replacement or disclosure authority;
- History retrieval must remain bounded and exact evidence must terminate material historical claims;
- ordinary Master stays in the existing Interpreter/Narrator role model;
- current PLAYER/PC/knowledge/disclosure controls visible retrospective material;
- no whole-campaign event-body scan;
- no extra serial LLM call solely for retrospective evidence;
- no generic memory/search subsystem.

## Recommendation

Adopt the four-part repair:

1. RuntimeHost-internal CurrentOwnerView used by Context, readiness and retrospective/current exact event reads.
2. Production ReadinessService with deterministic READY_PC/local-sufficiency evaluator over CurrentOwnerView + BoundCatalogContext.
3. Extend the existing EVENT_INDEX with minimum typed discovery refs, plus atomic HOT/current LIVE discovery companions; add bounded History discovery/exact-event APIs.
4. Add RetrospectiveService that orchestrates native discovery/evidence/current eligibility and issues a sealed retrospective evidence carrier to existing profile.narration with retrospective=True.

Story public Master access is deferred.

## Why

This is the only considered design that:

- satisfies currentness for unpublished accepted state;
- provides a correct native baseline when Story is stale/absent;
- preserves History, Context and knowledge/disclosure authority boundaries;
- fixes the existing Context stale-read seam once rather than duplicating it;
- remains bounded and product-specific.

## Strongest weakness

The repair crosses RuntimeHost, HOT, Context and History and therefore has wider implementation impact than a Story-reader patch. That width is caused by an existing shared currentness gap, not by speculative abstraction.

## Alternatives and trade-offs

Story-first:
- less new discovery work initially;
- still cannot prove current truth/eligibility and fails when Story lags.

Context-does-everything:
- fewer service names;
- creates a search/storage orchestration owner inside Context.

Per-feature current reads:
- smaller local diffs;
- duplicates source-selection authority and leaves Context inconsistent.

## Remaining uncertainty

Exact production field spelling and module factoring may change during TDD as long as canonical contracts remain intact. No material semantic uncertainty remains.

Recommendation confidence: HIGH
Human decision required: NO

The accepted owners already decide the material trade-offs. No Product Owner gate is created here.
