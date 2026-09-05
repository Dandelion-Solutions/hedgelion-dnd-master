# R2.7 WP-19 — Step 3 Decision Brief

Status: **STEP 3 COMPLETE — NO HUMAN DECISION REQUIRED**

Date: 2026-09-05

Research source:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-research-architecture-draft.md`.

## Decision summary

WP-19 needs one implementation-facing composition architecture over already accepted owners. Product semantics are already fixed by PO-001/PO-002/PO-003; evidence does not expose a remaining product trade-off or owner ambiguity.

Recommendation: **Alternative A — composition-first existing-owner contract**.

Recommendation confidence: **HIGH**.

Human decision required: **NO**.

## D19-01 — Campaign selection barrier

Decision: campaign-specific runtime/state resolution requires explicit current-chat existing-campaign or New Game selection. Menu discovery remains bounded and noncommittal before selection.

Why now: it is the entry boundary for all WP-19 creation/runtime work and a material agency/latency guarantee.

Alternatives rejected: implicit sole/recent campaign selection; eager campaign preload.

## D19-02 — Exact New Game identity envelope

Decision: freeze exact selected package identity before generation, including `version`, `package_id`, truthful `source_commit_sha|null`, `package_sha256`, and `ruleset_set_sha256`, plus storage ancestry HEAD, creator login, campaign ID/branch/time/mode.

`ruleset_set_sha256` comes from the validated RUNTIME_PACKAGE/resolved ruleset lock and is passed to the generator, then projected to MANIFEST ruleset created/current identity.

Alternative rejected: version/tag-only identity.

## D19-03 — Initial scaffold and publication

Decision: exact selected package generator once; complete generator output; one from-scratch campaign tree; one init commit parented to pinned storage default HEAD; one non-force ref update. No semantic/per-file reconstruction fallback.

Technical scaffold completion precedes player questions and remains normally invisible.

## D19-04 — Progressive readiness/lifecycle

Decision: retain the existing sequence:

```text
initializing scaffold
 -> optional durable PROVISIONAL_IDENTITY
 -> progressive locally-sufficient play
 -> READY_PC
 -> PLAY_READY
 -> active iff READY_PC + PLAY_READY
```

No hard `pre-live` versus `true live` state is admitted. Explicit save during unfinished setup preserves `initializing`; `paused` requires prior PLAY_READY/normal active play plus a real pause/stop intent.

## D19-05 — Creation authority and multiplayer

Decision: creator is first campaign-specific init-commit `author.login`; singleplayer writes creator-only; multiplayer gameplay writes require active PLAYER binding; mode creator-controlled; `invite_only` default/safe. Card identity/participant fields are projections/hints.

No new access subsystem.

## D19-06 — PO-001 ordinary Master retrospective

Decision: register/realize retrospective/history as an ordinary active-gameplay Master consumer under existing R2.3 purpose/need-profile and Step-4 disclosure boundaries. Story is orientation only; material claims escalate to exact/native historical evidence. No Commentator transition for an authorized active player.

Read-only Commentator consumes the same historical owners only under its own eligible read-only context.

## D19-07 — PO-002 save-and-exit

Decision: compose existing save + session-context termination + campaign-menu re-entry.

Ordering:

```text
SAVE succeeds
 -> clear campaign-specific session-local gameplay binding/hot context
 -> preserve durable lifecycle/membership/control
 -> re-enter normal bounded campaign-selection state
```

On save failure/indeterminate publication, no combined success and no destructive context clearing.

Exit is not pause/completion/archive/membership leave/PLAYER deactivation/control transfer/global live stop.

## D19-08 — PO-003 historical decision basis

Decision: extend existing Step-4 `LOG/runtime.semantic_event` / WP-10 SemanticEvent history family with a **logical bounded event-time decision-basis contract** for qualifying material Actor decisions/transitions.

The situation-specific material subset may be proposed in the already-required Actor/Master reasoning phase. Deterministic validation owns eligibility/source-class/stable identity/then-value-or-immutable-evidence/boundedness/provenance/no-COT checks.

Physical field names/layout/index projection are intentionally deferred to realization.

No new historical psychology owner/family.

## D19-09 — PO-003 durability and retrieval

Decision: accepted basis follows ordinary SemanticEvent SOFT/HARD/save/live durability. Capture alone creates no new remote publication boundary. Retrospective retrieval is dependency-specific and bounded; any needed physical discovery projection is derived/index-only and cannot become authority.

Insufficient T0 evidence yields an explicit supported-limit answer, never exact motive inferred from T1.

## D19-10 — Mandatory latency/interactivity law

Decision: preserve Product Owner latency amendment as a hard design criterion.

Baseline:

```text
extra sequential LLM call solely for capture = 0
extra serial remote/tool read solely for capture when data already bound = 0
separate remote publication solely for basis = 0
irrelevant-turn basis work = 0
additional context/output = bounded typed material items only
```

Any future requirement for a serial extra critical-path round-trip is a material architecture/performance problem, not an implementation detail.

## D19-11 — Realization and compatibility boundary

Decision: WP-19 canonical architecture owns clean creation and adjacent consumer composition. Current runtime/schema/test mismatches are downstream realization obligations. WP-20 alone owns future released-campaign evolution/migration/compatibility.

No runtime/schema/test implementation in this design loop.

## Strongest weakness of recommendation

The composition contract spans many owners and therefore requires careful implementation traceability. This is preferable to creating a duplicate orchestrator owner: the complexity already exists in the domain boundaries, and centralizing it would hide rather than remove it.

## Residual uncertainty

Only physical realization choices remain: exact schema representation for decision basis, minimum index projection needed for bounded retrieval, exact runtime instruction placement, and direct acceptance-test form. None changes current product semantics or owner allocation.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```