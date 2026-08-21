# Step 5.9 — Forward-Extensible Time Boundary — Owner Decision

Status: **OWNER-APPROVED ARCHITECTURE BOUNDARY — INPUT TO STEP 5.9**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

## Decision

Baseline HDM chronology is **forward-extensible**.

Accepted fictional history may be extended by later events, later-established causal/temporal relations, bounded elapsed evidence, and corrections handled through explicit integrity/repair semantics. Ordinary baseline gameplay does **not** rewrite already-established causal history as a normal chronology operation.

Canonical baseline assumptions:

```text
accepted history extends forward

later canon MAY:
    add new events
    add newly established relations between existing anchors
    refine previously unknown/indeterminate chronology with valid evidence
    preserve exact or bounded elapsed evidence when materially required

later canon SHALL NOT, as ordinary baseline chronology semantics:
    make an already-established cause never have happened
    replace one accepted past with another mutable past
    maintain several simultaneously authoritative branching timelines
    require causal loops / retrocausal cycles to be represented as normal chronology
```

## Supported difficult cases

The boundary does **not** prohibit complex time handling that remains compatible with forward-extensible history.

Baseline architecture may support, subject to ordinary Step-5.9 evidence rules:

- exact or approximate deadlines;
- global countdowns;
- independently advancing scenes;
- tightly synchronized multi-scene operations via more expensive reconciliation;
- different temporal rates or coordinate systems across scopes/planes;
- large jumps forward in fictional time;
- visits to, visions of, records from, or simulations of past periods when they do not mutate already-established causal history;
- newly discovered evidence that establishes previously unknown historical ordering without rewriting accepted facts.

These cases may increase metric/reconciliation cost but do not by themselves require another chronology authority model.

## Outside baseline chronology contract

The following are intentionally **not supported as baseline engine semantics**:

- mutable-past time travel where player actions rewrite already-established history;
- branching/multiple authoritative timelines or worldlines;
- routine retrocausality where later actions become causes of already-established earlier events;
- causal-loop mechanics that require strict temporal precedence to cycle;
- arbitrary timeline replacement/merge semantics.

Supporting one of these in the future requires an explicit architecture extension rather than implicit interpretation through baseline chronology fields.

This is a complexity boundary, not a claim that fictional stories may never mention time travel. A campaign may contain immutable-history time travel, visions, prophecies, temporal anomalies, records, stasis, time dilation, or similar fiction when their mechanics remain representable by the baseline forward-extensible model.

## Dramaturg / campaign-preparation policy

Step 4 defines Dramaturg as the private noncanonical preparation role. This decision therefore creates the following carry-forward constraint for Dramaturg policy and its eventual Context/role realization:

> Dramaturg SHALL NOT deliberately prepare a baseline campaign premise, pressure, mystery solution, planned development, or near-horizon mechanic whose correctness requires mutable past, branching authoritative timelines, or causal-loop chronology unless a future explicit chronology extension has been selected for that campaign/runtime profile.

Dramaturg MAY prepare temporal themes and difficult chronology that stay inside baseline semantics, including forward jumps, deadlines, time dilation, independent scene timing, immutable-history time travel, historical mysteries, prophecies, and temporal anomalies whose accepted history remains forward-extensible.

This is a preparation/capability guard. It does not make Dramaturg chronology authority and does not authorize prepared temporal events to occur.

## Engine/runtime behavior at the boundary

Baseline runtime SHALL NOT silently fake unsupported temporal semantics by:

- rewriting old SemanticEvents in place;
- deleting accepted causal history to make a new past fit;
- treating Git history rewrite as fictional timeline rewrite;
- inventing hidden worldline IDs;
- treating contradictions as evidence that time travel occurred;
- converting a causal cycle into arbitrary total order.

If play nevertheless reaches a state that genuinely requires unsupported semantics, the engine should surface a typed capability/architecture boundary rather than pretending the baseline chronology model can represent it correctly. Exact user-facing handling belongs to later runtime/design work.

## Why this boundary is accepted

The baseline HDM objective is the minimum sufficient chronology architecture for normal D&D campaigns and complex but forward-extensible multiplayer fiction.

Designing mutable history, worldline identity, branching authority, retrocausal provenance and timeline merge semantics now would create a disproportionate complexity bomb with no demonstrated baseline consumer.

The accepted boundary preserves extensibility: a future dedicated temporal-branching architecture may be added explicitly if a real campaign/product requirement justifies it.

## Step 5.9 consequence

The Step-5.9 candidate/adversarial/canonical chain SHALL treat **forward-extensible accepted history** as an explicit governing assumption and SHALL test difficult supported cases for graceful cost degradation rather than introducing a second chronology model pre-emptively.

No compensation model is designed in Step 5.9 unless later evidence demonstrates a typical baseline HDM scenario that cannot be represented safely under this assumption.
