# HDM Role-Context Validation Protocol 2 — Collapsed Multi-Role Execution

Status: **COMPLETED VALIDATION EVIDENCE — NON-CANONICAL ARCHITECTURE INPUT**

Date: 2026-08-23

## Purpose

Protocol 2 tested a stronger topology than Protocol 1.

Several logically incompatible HDM role phases were executed inside one physical model generation:

```text
Dramaturg -> Actor(s) -> Narrator -> player-facing response
```

All role frames were physically co-located. The validation therefore tested **controlled non-isolation** rather than physical secrecy.

The core question was:

> Can one physical generation execute multiple HDM logical roles while keeping their observable decisions aligned with role-local eligibility rather than with the union of all physically visible information?

## Setup

The completed run contained 96 Subject turns.

The strongest channels deliberately paired hidden and lawfully eligible states:

- a hidden canonical fact was physically present to a broader role but ineligible to the active Actor;
- a matched positive control later made the relevant fact lawfully eligible;
- historical controls tested whether a role could use previously disclosed information correctly;
- same-generation probes tested whether a fresh private Dramaturg branch would steer an Actor that did not receive that branch;
- multi-role turns exercised Actor and Narrator separation inside one response.

A compact witness channel recorded selected turn-local role states. Larger factor-attribution telemetry was also tested but proved unreliable and is not treated as primary evidence.

## Primary behavioral result

Independent semantic review found no convincing material role-boundary leak in ordinary collapsed-role gameplay turns.

The strongest objective channels were:

- hidden semantic canonical-target selections: **0/11**;
- matched eligible controls after lawful eligibility: **4/4**;
- dynamic historical eligible controls: **4/4**;
- same-generation private-branch affinity: **0/12**.

The combined hidden/eligible pattern is the most important result:

```text
hidden truth physically present -> Actor does not use it
lawful disclosure/eligibility -> Actor uses it
```

This is substantially stronger than a low hidden-target rate by itself because it shows that the Subject was capable of selecting the canonical information when the receiving role actually became entitled to it.

## Hidden-to-disclosed transitions

Several semantic domains followed the same pattern:

- identity;
- cause;
- location;
- route;
- evidence source.

The relevant Actor first operated from its own evidence or belief while the objective answer remained physically present elsewhere in the generation/history. After ordinary in-fiction evidence lawfully disclosed the answer, the same Actor updated.

This supports a role-local epistemic model rather than simple lexical avoidance.

## Same-generation result and limitation

The same-generation channel was directionally favorable: Actor behavior did not align with a freshly selected private Dramaturg branch on the 12 tested turns.

However, the option mapping used an overly obvious positional relationship between private branches and Actor choices. A Subject that recognized the experiment could deliberately avoid the corresponding index.

Therefore:

- the 0/12 result is supporting evidence;
- it is not sufficient standalone proof of same-generation containment;
- later validation must use opaque turn-local IDs and non-positional affinity mappings.

## Witness findings

### Turn-local state IDs — useful

Selected role-state IDs correlated well with visible decisions on reviewed turns.

This makes a short state/decision witness useful as a diagnostic channel.

### Factor masks — not suitable for causal attribution

Factor masks were highly saturated:

- about 91.8% of available role factors were selected on average;
- roughly three quarters of parsed records selected every available factor.

The Subject appeared to interpret the mask more like "relevant/in-frame information" than "the exact causal factors that determined this decision".

Consequently factor-mask over-report or under-report must not be interpreted as role leakage by itself.

### Confidence — not informative

Reviewed records reported maximum confidence throughout, so the confidence field produced no useful calibration signal.

### Boundary self-report — weakly validated

Boundary flags were consistent with visible behavior but lacked a positive-control case that required a boundary violation. They are supporting telemetry, not primary evidence.

## No-witness observations

Ordinary no-witness turns did not show an obvious degradation in role discipline or response quality.

This weakens the explanation that good containment existed only because a telemetry footer reminded the Subject that it was being tested.

The no-witness controls were not perfectly matched hidden-probe pairs, so later validation improved this design.

## Automated semantic-judge limitation

An automated semantic-judge path proved unsuitable as the primary evidence source.

It sometimes classified a turn as failed because it disagreed with witness factor attribution even while observable role behavior remained contained. That conflated two different questions:

1. did the visible Actor/Narrator cross a role boundary;
2. did an auxiliary self-report match an assessor's causal interpretation?

The second question cannot substitute for the first.

The generated aggregate report also mis-combined assessment fields and produced a misleading failure headline that was inconsistent with the underlying behavioral channels.

Durable lesson:

> behavioral containment, witness diagnostics and assessor interpretation must remain separate evidence channels.

## Transport/instrument limitations

The validation exposed avoidable transport risk when the model was asked to produce large structured envelopes:

- malformed structured responses;
- manual repair before acceptance;
- stricter-than-necessary final envelopes;
- retry/submission provenance gaps;
- unreliable factor-attribution telemetry;
- defective aggregate reporting.

These defects do not explain the positive semantic containment observations, but they prevent treating the run as pristine confirmatory evidence.

Engineering consequence:

> deterministic Python should own serialization, validation and experiment bookkeeping; the model should not be responsible for large transport JSON in the hot loop.

## Engineering inference

Protocol 2 provides strong evidence that one physical generation can execute multiple logically incompatible HDM roles with useful **behavioral containment** even when all role frames are physically co-located.

The evidence supports:

- explicit role rebinding inside one generation;
- role-local epistemic state;
- lawful typed/observable information transfer rather than raw-frame inheritance;
- Actor and Narrator separation without one persistent physical agent per role.

It does **not** establish:

- physical or cognitive isolation;
- universal safety across reasoning configurations;
- unlimited-campaign stability;
- final production prompt topology;
- final player-facing quality.

Those remaining questions are addressed more directly by Protocol 3 and the subsequent Step-6 architecture design.

## Step-6 relevance

Protocol 2 removes the need to treat separate physical role calls as an untested default assumption.

It supports considering a collapsed single-turn pipeline as a real baseline candidate, provided Step 6 preserves the existing logical eligibility, disclosure, authority and persistence semantics.
