# Steps 1–2 Retrospective Assurance — Slice E Task Charter: Whole-System Integration

Status: **SOLUTION-BLIND INTEGRATION CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently test whether the accepted Step-1 catalog/class model and Step-2 mechanical-state/evaluation model compose into one coherent engine boundary when definitions evolve, live state survives, execution suspends, caches disappear, campaigns promote local state, and later durability/multiplayer work is introduced.

Slices 0A–D have already tested local subsystems. Slice E is not another local redesign. It asks whether their joins create duplicate authority, missing lifetime owners, unrecoverable references, incompatible migration semantics, hidden event-history requirements, or accidental LLM/canonical-state coupling.

## 2. System invariant under test

For every mechanically meaningful fact or obligation there must be exactly one current authority.

Other representations may be:

```text
reusable definition
reference/provenance
prospective plan
immutable receipt/event
continuity serialization of a runtime owner
rebuildable index/cache/projection
migration input/output
```

but must not become a second independently writable truth.

The complete chain must remain interpretable across:

```text
Resolved catalog context
    -> live world/procedure state
    -> pinned mechanical evaluation
    -> prospective execution / suspension
    -> committed event/provenance
    -> continuity checkpoint / publication
    -> migration / later hydration
```

## 3. Integration questions

### Catalog identity and definition evolution

- What exact context makes a durable `definition_id` semantically interpretable?
- Does a campaign resolve exactly one coherent definition set at a time?
- Can two layers silently shadow the same ID?
- What happens to live Actor/Resource/Effect state when an engine/ruleset/campaign definition changes incompatibly?
- Are active instances migrated to the adopted catalog context, or can they remain pinned to old definition semantics?
- Can a scheduled-trigger local key, Effect parameter schema, Resource recovery rule, or support/provenance relation become orphaned by definition evolution?
- Which exact packaging/version shape may remain Step 6 without leaving the logical ownership rule ambiguous now?

### World/application provenance and event compaction

- Which live facts needed for current mechanics may depend on historical Event/Trace records?
- Can Effect arbitration using mechanical recency survive compaction of old Events/Traces?
- Is `rules_origin_id` distinguishable from concrete causal creation identity?
- Does a live application need an immutable causal reference/order token, or can it safely require historical lookup?
- What history must remain when terminal Effect records themselves may be garbage-collected?

### Procedure-local Resource ownership

- What object is the actual lifetime owner when a Resource definition says `lifetime_owner = procedure`?
- Is that owner an Encounter, generic Procedure, Resolution, turn scope, or another runtime object?
- May Resolution/Continuation/checkpoint each serialize procedure-local `spent` without creating several mutable copies?
- How does a suspended parent + child reaction observe and mutate the same procedure-local action/reaction budgets?
- Can the owner survive process/chat loss without being confused with one Activity invocation?

### Temporal, chronology, and checkpoint composition

- Are Effect intrinsic lifetime, Effect scheduled-trigger next-due state, Resource recovery bindings, LifeState recovery bindings, procedure-local temporal obligations, and retained chronology evidence distinct owners?
- Does the checkpoint preserve only continuity-critical source authority, or copy canonical/HOT owner state into another writable truth?
- Can Temporal Agenda always rebuild after loss from those authorities?
- Can a future elapsed-time query be answered or explicitly return insufficient evidence without replaying all campaign history?

### Promotion and reference closure

- Can a canonical/durable record point to a local-only support parent, source, definition, procedure, or scheduled-trigger dependency?
- What must be promoted together when one record becomes durable?
- Which runtime-only identities may appear in immutable receipts but not durable world references?
- Do session-local definitions referenced by durable world state require definition promotion before publication?

### LLM/core/lore composition

- Can an invocation-adjudicated fact influence a committed outcome without silently becoming canonical truth?
- If the outcome must be replayed/resumed, is fact value/provenance preserved as causal execution input rather than world authority?
- Can Step 4 later promote a fact to lore without rewriting the original mechanical receipt semantics?
- Can secret/knowledge-scoped context remain outside deterministic state while still satisfying a registered fact request safely?

### Recovery of derived state

After loss of SQLite/index/cache state, can runtime reconstruct without guessing:

- effective Conditions;
- Effect arbitration groups/winners;
- support reverse indexes;
- Resource capacities/availability;
- scoped mechanical dependency DAG;
- Temporal Agenda;
- scheduled-trigger due entries;
- pinned definition semantics;
- suspended execution inputs/frontier where checkpointed?

If any answer requires an old cache, arbitrary event replay, LLM prose reconstruction, or mutable duplicate snapshot, the integration fails.

## 4. Required multi-system scenarios

The assurance must attack at least these cases.

### E1 — long-lived periodic Condition across catalog update and restart

```text
Actor has disease Condition/Effect
    intrinsic lifetime
    daily scheduled save

later Actor gains immunity
campaign adopts compatible/incompatible definition update
next trigger becomes due
chat/process dies before/after due handling
campaign resumes elsewhere
```

Verify definition interpretation, current applicability, trigger key migration, temporal authority, causal execution, and no scheduler/cache authority.

### E2 — procedure budgets with reaction and suspension

```text
Actor spends Action-like procedure Resource
parent Resolution opens reaction
child reaction spends Reaction-like procedure Resource
parent suspends/resumes
process is lost and restored
```

Verify exactly one procedure-local mutable Resource authority and idempotent recovery/resume.

### E3 — overlapping Effects requiring recency after history compaction

```text
same rules-origin Effect A and B coexist
potency tie requires mechanical recency
old Event/Trace history compacts
winner ends
fallback must be derived deterministically
```

Verify current arbitration does not depend on disposable history or SQL row order.

### E4 — capacity/lifecycle/effect mutation in one prospective segment

```text
Effect ends
Resource capacity falls
stored current must normalize
HP maximum changes
Condition applicability changes
LifeState consequence may also occur
```

Verify one pinned prospective view, one DAG, state-owner normalization, no intermediate mutation-order semantics.

### E5 — durable dependent Effect with local dependencies

```text
child Effect is promoted/durable
support parent or source/rules definition is still local/session-only
```

Verify publication closure either promotes required dependencies or rejects the durable reference.

### E6 — invocation fact affects one execution only

```text
LLM adjudicates target visible
attack resolves and commits
same world state later has target not visible
```

Verify original receipt remains reproducible while no persistent capacity/Condition/lifecycle fact depended on the ephemeral input and the fact did not become lore merely by use.

### E7 — definition removes active scheduled-trigger declaration

```text
live Effect has scheduled_trigger_state.daily_save
new catalog definition removes/renames daily_save
```

Verify migration is explicit; runtime cannot silently load an orphan key or keep old semantics invisibly.

## 5. Quality attributes / exit tests

### Single authority

For every state/obligation in scenarios E1–E7, identify exactly one mutable owner.

### Interpretability

Every durable reference and continuity record must be interpretable under an exact resolved engine/catalog/campaign context after restart.

### Reconstructability

All derived indexes/graphs/Agenda results must rebuild from source owners and accepted continuity inputs.

### Migration safety

An adopted catalog/runtime change cannot silently reinterpret live durable state under an incompatible definition contract.

### Causal sufficiency

Live mechanics that need recency/provenance cannot require disposable history to remain un-compacted forever.

### Bounded execution

No integration fix may introduce a global scheduler, generic workflow/query language, campaign-wide per-action scan, or event-sourced replacement for current-state authority.

### LLM isolation

Invocation adjudication remains explicit input; it does not become engine-owned state or durable truth by accident.

## 6. Non-goals

Slice E does not finalize:

- exact Step-3 ExecutionSegment/Event/Continuation schemas;
- exact repository checkpoint publication format (Step 5);
- exact ruleset package manifest/version format (Step 6);
- final lore/disclosure/context-selection model (Step 4);
- full seed migration tooling (Step 6);
- multiplayer reconciliation algorithm (Step 5).

It must, however, define enough ownership constraints that those later stages cannot choose mutually incompatible semantics.

## 7. Human-decision threshold

Do not escalate mere field naming, schema alignment, validation gaps, or mechanically forced ownership clarifications.

Escalate only if evidence leaves multiple materially different viable choices involving, for example:

- whether active live instances migrate to a newly adopted catalog context or retain old definition semantics;
- introduction of a new persistent owner/class rather than reuse of an existing owner;
- durable retention versus compaction of causal history where both materially affect performance/semantics;
- another product-level compatibility or lifecycle tradeoff not already decided.

Any escalation must include recommendation, simplest alternative, strongest counterargument, risks, reversibility, and what evidence would change the recommendation.

## 8. Exit criteria

Slice E closes only when:

1. a cross-system ownership matrix covers catalog → live state → evaluation → execution → history → checkpoint → migration;
2. scenarios E1–E7 have explicit dispositions;
3. procedure-local Resource ownership is unambiguous;
4. live Effect causal/recency requirements survive history compaction;
5. catalog-context evolution semantics for active state are explicit enough for later migration design;
6. temporal/checkpoint/promotion boundaries contain no duplicate authority;
7. LLM invocation facts remain isolated from canonical truth;
8. all derived state is rebuildable;
9. an independent adversarial pass attacks the integration result;
10. every finding is fixed, assigned to a later owner with a sufficient current constraint, or escalated to the human architect;
11. the result states `KEEP`, `AMEND`, or `REOPEN` with confidence.
