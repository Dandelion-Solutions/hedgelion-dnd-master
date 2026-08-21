# HDM Activity Model

Status: **DESIGN BASELINE — STEP 2 ASSURANCE FACT-INPUT ALIGNMENT APPLIED**

This document defines the first executable contract for HDM Activities. It
supersedes the provisional Activity shapes in `CATALOG_MODEL.md` and
`MECHANICAL_RUNTIME_PROPOSAL.md` where they conflict.

## 1. Purpose and boundary

An Activity is a reusable, declarative recipe for one bounded mechanical
procedure. One invocation is a `runtime.resolution`.

An Activity is not:

- a player message;
- every fictional act described by the Master;
- necessarily one D&D Action, attack, roll, or state mutation;
- a general scripting language;
- a substitute for a deterministic `value.transition_request`.

The LLM first classifies every material clause in a player message. The host
routes each clause through the cheapest sufficient path:

| Clause | Runtime path |
|---|---|
| Fiction with no mechanically relevant state change | `narrative_only` |
| Already-adjudicated deterministic change | `value.transition_request` |
| Uncertainty, roll, resource, effect, reaction, or other rule procedure | `value.action_request` bound to an Activity |

`family_id` classifies player intent and helps routing. It does not select an
executor and does not force a runtime call. A communication or movement clause
may remain narrative-only when no tracked consequence exists.

## 2. Definition structure

The universal catalog-definition envelope owns `id`, `kind`, `name`, facets,
tags, and localization. Activity data does not repeat identity, provenance, or
schema-version fields.

The minimum valid Activity data is:

```json
{
  "family_id": "activity.attack",
  "steps": [
    {
      "op": "op.resolve_attack"
    }
  ]
}
```

Only `family_id` and a non-empty `steps` array are required. Expected fields are
added only when the procedure needs them:

```json
{
  "family_id": "activity.attack",
  "activation": {
    "economy_id": "resource.action",
    "amount": 1
  },
  "requirements": {
    "all": [
      {"fact": "fiction.target_reachable"}
    ]
  },
  "targeting": {
    "kind_id": "target.entity",
    "minimum": 1,
    "maximum": 1,
    "range_mode_id": "range.reachable"
  },
  "costs": [],
  "steps": []
}
```

The example fact is an invocation-adjudicated fiction input, not an engine-owned
mechanical claim. Engine-checkable requirements such as HP, Resource state,
Condition state, equipment state, or derived ability to act use registered
mechanical accessors/eligibility contracts instead of LLM facts.

The fields mean:

- `activation`: optional action-economy or procedure-time cost;
- `requirements`: closed predicate over registered accessors and explicitly
  registered invocation facts;
- `targeting`: target cardinality, kind, range, and area when relevant;
- `costs`: references to Resource state and the registered commitment point;
- `steps`: ordered typed operations.

Activity data has no top-level `uses`, `recovery`, `effect_ids`, or result
`duration`:

- uses and recovery belong to `definition.resource` and its state;
- an effect is created by `op.create_effect` and owns its duration;
- range and area are part of the single target contract;
- Activity-specific source and owner provenance come from the invocation.

This avoids two writable representations of the same mechanic.

## 3. Steps and registered operation contracts

The common step envelope is:

```json
{
  "op": "op.apply_damage",
  "args": {},
  "when": {
    "result": "attack.outcome",
    "in": ["hit", "critical"]
  },
  "export": "damage"
}
```

Only `op` is universally required. `args`, `when`, and `export` are optional.

The common JSON Schema validates the envelope. The operation registry maps every
`op.*` ID to an exact argument/result validator. Therefore `args` is not an
extension bag: an unknown parameter or an argument invalid for the selected
operation makes Activity compilation fail.

The first composition language permits only:

- a finite ordered sequence;
- a predicate over explicit registered context or typed prior results;
- bounded iteration over an explicit target list;
- a bounded branch over typed results;
- a player/GM choice request;
- a reaction window;
- named result exports consumed by later steps.

It forbids arbitrary Python, SQL, imports, file/network/GitHub access, `eval`,
unbounded loops, unrestricted recursion, arbitrary world queries, and runtime
creation of executable operation kinds. New numbers, dice, predicates, and
combinations are data; a new state-transition semantic requires a new registered
runtime capability.

Structural operations such as `op.branch` and `op.for_each_target` may compose
only finite child steps. Runtime configuration enforces maximum step count,
branch depth, target count, and trigger-chain depth. Exact limits will be chosen
from focused tests rather than guessed into the catalog.

## 4. ActionRequest and binding

The LLM supplies an Activity reference plus invocation-specific bindings.
Conceptually:

```json
{
  "activity_id": "srd.activity.longsword_attack",
  "actor_id": "actor-00001",
  "source_id": "asset-00001",
  "target_ids": ["actor-00014"],
  "context_facts": {
    "fiction.target_visible": {
      "value": true,
      "provenance": "llm_adjudicated"
    }
  }
}
```

This is a semantic example, not the final Step-3 RuntimeCommand schema.

The request does not copy the Activity definition, actor statistics, or active
Rule Elements. Runtime hydrates those records and rejects:

- unknown fact IDs;
- fact IDs not permitted by the consumer's input contract;
- attempts to supply engine-owned mechanical state as an adjudicated fact;
- unknown references;
- missing requirements/facts;
- illegal parameters or subject bindings.

Invocation facts are registered in `CATALOG/mechanical-surfaces.json`. The
initial fact channel is boolean and `INVOCATION_ADJUDICATED` only. Engine-owned
facts remain accessors/calculations resolved from the pinned MechanicalContext.

For a registered boolean invocation fact:

```text
explicit true  != explicit false != missing
```

Missing is not coerced to false. If compiled mechanics reference an invocation
fact that was not accepted for the request, runtime returns a typed missing-input
or adjudication requirement.

Fictional facts that the mathematical engine cannot infer — for example whether
a target is visible through an unusual fictional obstruction, or whether an
improvised support can bear weight — may be adjudicated first and passed as
registered typed context. An Activity cannot discover unstated fiction by
querying all lore.

Accepted invocation facts are explicit in the trace and, when execution may
suspend/retry, become fixed causal execution inputs with provenance. They do not
automatically become canonical world/lore facts.

Ad-hoc play should normally bind a standard parameterized Activity such as an
improvised attack or generic test. It does not create a persistent Activity ID
for every unique sentence. A campaign Activity is created only when the mechanic
is reusable and all of its operations already exist in the engine registry.

## 5. D&D action economy and natural turns

Engine Activity and D&D Action are different concepts:

- one D&D Action may contain several attacks or steps;
- movement may occur around an Action;
- a single player message may contain movement, an Action, a free interaction,
  and purely narrative speech;
- narrative and quick-run modes may choose not to enforce action economy.

`activation` is therefore optional. The active mode profile decides whether it
is enforced. An Activity never invents additional microscopic actions for
routine handling.

For assets, preflight applies the accepted handling contract:

- an accessible potion can be retrieved and consumed as one use Activity;
- ordinary drawing, stowing, or exchanging held items is implicit and spends no
  separate player turn;
- runtime asks for a replacement choice before committing only when the requested
  held configuration exceeds available hands;
- an unarmed attack never requires a weapon and the mere presence of a weapon
  never creates an unnecessary choice.

These engine-checkable facts are resolved from authoritative state/contracts,
not supplied through the invocation fact channel.

## 6. Multiple intents in one message

The host builds one ordered `runtime.intent_plan` containing every material
clause and submits it in one runtime call where possible. Each clause keeps its
own mapping and execution state.

The normal plan is sequential, not globally atomic. If a hero takes a sword,
moves into a corridor, and then fails to close a jammed door, the first two
committed results remain true. Later clauses may be skipped when an earlier
result makes them impossible. The receipt must report each executed, skipped,
failed, or suspended clause so narration cannot silently omit part of the
player's intent.

`activity.composite` is reserved for a reusable rules-defined procedure such as
Multiattack or a spell with several coupled effects. The host does not create a
new permanent composite Activity merely to wrap a long natural-language turn.

An Activity may define an atomic mutation segment. Once that segment commits, a
later failure produces partial completion; it does not invoke a general rollback
or fictional compensation mechanism.

## 7. Suspension and deterministic resumption

`op.request_choice` and `op.open_reaction_window` may suspend the same
Resolution. The continuation persists:

- Activity and bound entity references;
- completed step position;
- already generated authoritative rolls;
- accepted invocation facts + provenance required for deterministic resumption;
- typed exports;
- relevant record revisions;
- the pending choice or reaction contract;
- idempotency token.

SQLite transactions never remain open across chat messages. Resumption validates
the stored revisions and never rerolls or repeats a committed mutation.

Derived MechanicalContext values are not blindly trusted across suspension.
Step 3 owns the safe recompute frontier and re-pinning rules; fixed accepted
invocation facts remain fixed inputs to the resumed Resolution unless the
contract explicitly requires new adjudication.

## 8. Efficient execution in ChatGPT

The runtime compiles Activity definitions when loaded and caches the complete
compiled object. A normal call hydrates only the acting actor, explicit targets,
the source, their relevant effects/resources, and the current procedure state.

One host call should normally process the whole IntentPlan until it completes,
fails, or requires a genuine human choice/adjudication. The LLM is not invoked
between deterministic mechanical steps and does not maintain a separate
reasoning context for every NPC. It receives one compact, typed receipt and
produces one coherent narrative answer.

A due owner-local scheduled Effect trigger uses the same Activity binding/read
contract. It does not gain arbitrary world-query access merely because its
invocation was initiated by the Temporal Agenda.

Meta and maintenance commands bypass Activity routing and must never be logged
as fictional actions.

## 9. Known limitations and later ownership

This model does not guarantee that the LLM maps prose correctly. It reduces the
failure surface through a closed Activity/operation registry, strict schemas,
registered invocation facts, typed accessors, and typed runtime rejection. It
also does not provide a tactical map, simulate wall-clock time, or make
arbitrary homebrew executable.

Step 3 owns the exact RuntimeCommand/ActionRequest schema for fact values and
provenance, binder failure types, idempotency fingerprinting, and Continuation
persistence. Step 4 owns durable lore/knowledge promotion and broader context
selection. Step 6 owns full selector/fact seed closure.

The remaining Activity work is deliberately narrow:

1. exact `args` and result schema for every registered primitive;
2. exact cost commitment points;
3. focused examples covering branch, multiple targets, suspension, and partial
   completion;
4. measured composition limits.

## 10. Design basis

- D&D SRD 5.2.1: action, Bonus Action, Reaction, movement, tests, attacks, and
  GM adjudication;
- Foundry D&D5e Activities: multiple activities per source plus activation,
  consumption, targeting, and effect separation;
- Avrae Automation Reference: typed mechanical nodes, target scopes, and
  result-dependent branches.

These are design references. HDM does not copy their UI, command language,
document model, recursive automation surface, or implementation code.
