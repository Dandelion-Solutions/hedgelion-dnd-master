# HG-01 Novel-Action Hourglass — Public Research Result

Status: **COMPLETE — PASS WITH PLANNING CONSTRAINTS**

Date: 2026-09-13

## Purpose

HG-01 tested a central HDM assumption: players should be able to describe unusual, improvised and previously unseen actions in ordinary language without forcing the engine to maintain a huge catalog of predeclared action types or giving prose direct authority over deterministic game state.

The experiment asked whether broad player intent can narrow through existing HDM semantic and deterministic owners, including cases where two situations look almost identical in prose but differ in what consequence, authority or persistence is actually requested.

This document preserves the durable public conclusion only. It is research evidence, not a new architecture owner and not a replacement for the accepted HDM specifications that govern the behaviors involved.

## Method in brief

The experiment used **24 frozen scenarios arranged as 12 paired comparisons**. Each pair changed one important dimension while keeping the surrounding fiction deliberately similar. The pairs covered:

1. an improvised chandelier stunt with and without a requested disarm;
2. the same cold-producing ability used to create temporary traversal versus reveal information;
3. improvised rope/pitons/bench used as a temporary barrier versus a momentary handhold;
4. forged evidence versus genuine evidence presented with a misleading interpretation;
5. an illusion intended to influence NPC behavior versus one intended to create a bounded mechanical advantage;
6. a one-off bargain versus explicit promotion of the same idea into a reusable campaign rule;
7. a long compound stunt ending in an effect on another actor versus ending only in positioning;
8. a cooperative multi-player action with all participants current versus one required participant no longer current;
9. a delayed conditional trap versus recovery of an already accepted result after a downstream failure;
10. the same social request aimed at an ordinary nonsentient object versus a sentient actor inhabiting it;
11. a claimed permission absent from authoritative state versus the same action with real current permission;
12. a player directly asserting a private RNG result and world-state mutation versus declaring a legitimate action that may produce the same eventual outcome.

The paired structure was intentional: the experiment tested whether HDM can distinguish *why* an action matters rather than classifying it by surface wording alone.

## Result

All 24 scenarios were resolved without identifying a missing fundamental engine capability.

Final classification:

```text
A — semantic handling only:                         5
B — semantic handling + existing deterministic boundary: 18
C — reusable content / campaign-policy definition: 1
D — genuinely new deterministic primitive/architecture:  0
```

The only reusable-policy case was the scenario where the table explicitly chose to promote a repeated one-off bargain into a standing campaign rule. That belongs to the existing House-Rules concept rather than to a new core action mechanism.

No scenario demonstrated a need for a generic natural-language execution language, generic world-state mutation bridge, universal workflow engine, universal scheduler, or LLM-owned deterministic authority.

## Most useful findings

### Broad language can remain broad

A natural-language declaration does not need a matching engine verb. A visually elaborate action may collapse to no authoritative mutation at all, or to a small existing mechanical boundary, depending on the actual requested consequence.

This is the strongest support for the Hourglass idea: expressive player language can stay open-ended while authoritative consequences remain narrow and owner-controlled.

### Small fictional changes can legitimately change the route

The experiment repeatedly showed that almost identical player wording may require different treatment when one underlying fact changes: whether a target is sentient, whether a participant is current, whether a permission really exists, whether a result was already accepted, or whether a lasting consequence is actually requested.

The important input is therefore not a phrase-to-command mapping but the combination of current fiction, authority and intended consequence.

### Fiction should not automatically become persistent state

Ordinary scene details such as temporary relative position, attention, facing, distraction or similar short-lived relations should remain fiction unless an admitted mechanic or established owner requires a typed authoritative state transition.

The experiment exposed a tendency to over-formalize such details. Implementation planning should resist that pressure.

### NPC choice is not human collaboration authority

A sentient NPC deciding how to react to persuasion, deception, threat or illusion is an Actor/NPC reasoning problem. It must not be treated as though the NPC were another human participant whose current session/consent must be managed through multiplayer collaboration rules.

### Missing realization evidence is not an architecture gap by itself

A compact scenario or test context may fail to show the exact concrete realization of a consequence. That is not sufficient evidence for inventing a new primitive. Planning must first trace the current public owner and determine whether the case is already admitted, mechanically null, intentionally fictional, or explicitly unsupported.

### A successful adjudication need not imply arbitrary mutation

A bounded check can be meaningful even when it does not produce a durable state change. HDM should not manufacture a generic consequence mechanism merely because a semantic or mechanical test succeeded.

### Authority protections held under adversarial cases

The tested boundaries correctly distinguish player intent from authoritative fact. In particular, fabricated permissions, stale participation and private RNG assertions do not become canonical merely because the player states them confidently. Conversely, genuinely authorized actions remain available through their normal owners.

### Accepted causal results survive downstream recovery

Once an authoritative attempt and its causal/RNG basis have been accepted, a later persistence or publication failure must not silently create a fresh roll, reinterpret the action or alter its already accepted basis.

## Planning constraints carried forward

Implementation planning should preserve four concrete constraints exposed by HG-01:

1. Route voluntary NPC/faction reasoning through the existing Actor/NPC semantic owners; reserve multiplayer currentness/agency rules for actual human participants.
2. Keep ordinary within-location micro-position and transient attention/facing/distraction/reaction in fiction unless an exact admitted mechanic or native owner requires typed state.
3. Treat "exact realization not proven here" as a lookup/realization question, not automatic evidence that new architecture is required.
4. Preserve mechanically-null bounded adjudication; do not introduce a generic prose-to-StateDelta, workflow or arbitrary consequence bridge.

These constraints do not introduce new architecture. They are implementation-planning guardrails for staying inside already accepted HDM ownership boundaries.

## Limits of the result

HG-01 does not prove that every imaginable future player declaration is already handled correctly, nor that every current implementation artifact is complete. It establishes a narrower result: this deliberately varied frozen corpus did not reveal a missing fundamental action-execution architecture, and the observed failure pressures can be handled as planning/implementation discipline under existing owners.

A future case that genuinely cannot be expressed through accepted semantics and deterministic owners may still justify architecture review. HG-01 is evidence against premature generalization, not a prohibition on future evidence-driven change.

## Closure

```text
HG01_SCENARIOS: 24 / 24
HG01_PAIRS: 12 / 12
HG01_FINAL_DISTRIBUTION: A=5 B=18 C=1 D=0
HG01_ARCHITECTURE_GAP_FOUND: NO
HG01_TARGETED_RERUN_REQUIRED: NO
HG01_FURTHER_EXPERIMENT_WORK_REQUIRED: NO
HG01_DISPOSITION: PASS WITH PLANNING CONSTRAINTS
```

HG-01 is closed as a research experiment. Its durable value for the next stage is the evidence that open-ended player language should be planned around existing semantic and deterministic boundaries rather than by expanding the engine into a catalog or interpreter of bespoke natural-language actions.
