# HDM Rule Element Model

Status: **DESIGN BASELINE — pending focused mechanical examples**

This document defines passive mechanical contributions and bounded reactive
bindings. It supersedes the provisional standalone `definition.rule_element`
and `definition.trigger_binding` model.

## 1. Purpose and ownership

A Rule Element answers one question:

> What does this source contribute to this registered calculation when its
> explicit predicate is true?

It is a pure embedded value object. It does not perform an Activity, mutate
world state, spend resources, discover fiction, or call arbitrary code.

Rule Elements live inside the reusable definition that grants the mechanic,
normally a Feature, Effect, Asset, equipment property, or Feat. A named
Condition grants its mechanics through referenced Effects instead of copying
the same rules. The owning definition supplies identity and provenance. Runtime
state such as an active effect or equipped asset determines whether that owner
is currently available.

Consequently HDM does not create a standalone catalog file, canonical ID, or
allocator entry for every modifier. If reuse later requires a shared collection,
the reusable unit should be a Feature or Effect; a new rule-bundle entity is not
introduced without evidence.

## 2. Minimum structure

The minimum Rule Element is:

```json
{
  "operation_id": "rule.add_damage_component",
  "selector": "damage.weapon",
  "value": {
    "dice": "1d6",
    "damage_type_id": "damage.radiant"
  }
}
```

Only `operation_id`, `selector`, and `value` are required. Optional fields are:

```json
{
  "predicate": {
    "all": [
      {"fact": "source.equipped"},
      {"fact": "target.marked"}
    ]
  },
  "stacking_key": "artifact-radiant-rider",
  "priority": 100,
  "gate": {
    "resource_ref": "owner.radiant_rider_uses"
  }
}
```

The embedded object has no `id`, `source`, `phase`, recovery policy, or mutable
usage counter:

- provenance is derived from the owning definition and runtime instance;
- a registered selector denotes the calculation point and allowed contribution;
- the Resource owns current usage, capacity, spending, and recovery;
- resolver policy owns default ordering and stacking.

For diagnostics, runtime assigns an internal address from owner identity plus
the element's position in the validated definition. An optional local key may be
added later only if an external reference proves necessary.

## 3. Selectors, operations, and Contributions

`selector` identifies a registered calculation surface such as an attack bonus,
save DC, weapon damage, received damage, resource cost, range, or duration.

`operation_id` identifies the only transformation the element may contribute,
for example a flat modifier, advantage state, extra damage component,
resistance, cost adjustment, or bounded override.

At catalog compilation, runtime validates that:

1. both IDs exist in the selected engine/ruleset registry;
2. the operation is legal for the selector;
3. `value` matches that operation's exact JSON Schema;
4. predicate facts are exposed for that selector;
5. stacking, priority, and gate fields are valid for the operation.

When evaluated, a Rule Element returns a typed `value.contribution`. The
resolver accepts, combines, suppresses, or rejects Contributions according to
the selector's deterministic policy. Every result retains owner/source and
reason in the resolution trace.

No general `phase` field is stored. A selector such as `attack.roll.bonus` or
`damage.received` already identifies when it is evaluated. This prevents two
timing fields from disagreeing. Non-commutative overrides may use `priority`;
ordinary additive rules do not need it.

## 4. Predicates

Predicates are closed `all` / `any` / `not` trees over explicit typed facts, with
registered comparisons where required. They may inspect:

- actor, target, and source tags or conditions;
- equipped, held, accessible, attuned, and identified state;
- action, attack, damage, spell, weapon, and effect selectors;
- range, cover, visibility, and reachability facts already adjudicated;
- turn/round state and exposed Resource values;
- typed results from the current resolution.

Predicates cannot read arbitrary JSON paths, execute expressions, search all
lore, or infer a fact absent from the runtime context. The LLM must explicitly
adjudicate facts outside the engine's mathematical knowledge.

Missing facts make the predicate false or produce a typed validation issue when
the owning mechanic declares the fact mandatory. They never invite the runtime
to guess.

## 5. Stacking and limited use

Each registered rule operation defines its default combination policy. D&D
advantage/disadvantage, resistance, replacement, minimum/maximum, and additive
bonuses therefore remain resolver behavior rather than ad-hoc instructions
copied into every Rule Element.

`stacking_key` exists only when named-source or once-only behavior cannot be
derived from the operation and owner. `priority` is limited to operations whose
order changes the result. Runtime uses a deterministic tie-breaker and reports
conflicting incompatible overrides instead of depending on JSON array order.

`gate.resource_ref` may require an available limited-use Resource. The Rule
Element itself remains pure: it requests a gate as part of its Contribution.
The resolver validates and consumes the Resource atomically with the owning
mechanical result. Capacity and recovery are never duplicated in the element.

## 6. Trigger Bindings

A Trigger Binding represents a reactive mechanic that cannot be expressed as a
passive Contribution. It is also an embedded value object owned by the Feature,
Effect, Asset, or other definition that grants it.

Minimum shape:

```json
{
  "on": "signal.attack.hit.pending",
  "activity_id": "srd.activity.shield_reaction"
}
```

Expected optional fields are:

```json
{
  "mode": "offer",
  "actor": "owner",
  "targets": "signal.source",
  "predicate": {"fact": "owner.can_react"},
  "gate": {"resource_ref": "owner.reaction"},
  "priority": 100
}
```

The binding names a registered Signal or Event and a registered Activity. It
contains no callback, child steps, arbitrary payload mutation, or embedded
Activity definition.

`mode` is one of:

- `automatic`: invoke when the binding is eligible;
- `offer`: suspend and request an eligible player's/GM's decision;
- `schedule`: enqueue a mandatory post-commit child Resolution.

The registry restricts which modes are legal for each Signal/Event.

## 7. Signals and Events

A Signal is transient calculation/timing context exposed before a mutation is
irreversible. A pre-commit Trigger Binding may offer or automatically apply a
reaction that changes the pending result. Declining or completing the reaction
resumes the same Resolution without rerolling completed rolls.

An Event is an immutable committed fact. A post-commit binding may schedule a
new child Resolution with its own `resolution_id`, the same causal chain, and
the Event as `caused_by`. That child may add new facts; it cannot delete or
rewrite the triggering Event.

Runtime enforces deterministic ordering, per-binding/per-signal idempotency,
Resource gates, and a bounded trigger-chain depth. There is no background event
loop: turn changes, duration ticks, rests, and local-time advancement require an
explicit typed runtime command.

## 8. Fast evaluation

On hydration/definition load, runtime compiles and indexes embedded Rule Elements
by selector and Trigger Bindings by Signal/Event ID. A resolution evaluates only
the entries supplied by the actor, source, targets, their active effects, and the
current procedure state. It never scans the whole catalog or asks the LLM to
recalculate modifiers.

Changing a relevant working object invalidates its compiled cache entry through
the existing coarse `state_revision` policy. The cache stores complete compiled
objects and is disposable; canonical definitions and state remain recoverable
from GitHub.

## 9. Forbidden behavior

Rule Elements and Trigger Bindings cannot:

- mutate state directly;
- invoke Python, SQL, shell, network, GitHub, or arbitrary expressions;
- invent selectors, facts, operations, Signals, Events, or Activities;
- iterate or recurse;
- rewrite committed Events;
- own mutable counters or recovery schedules;
- create undocumented action-economy costs;
- silently disclose or search narrative secrets.

The remaining work is limited to the exact selector/fact registry, operation
value schemas, Contribution combination tables, and focused examples for
advantage, resistance, once-per-turn damage, reactions, and post-damage
follow-ups.

## 10. Design basis

- [PF2e Rule Elements](https://github.com/foundryvtt/pf2e/wiki/Quickstart-guide-for-rule-elements):
  typed operation keys, selectors, predicates, values, provenance, and stacking;
- [D&D SRD 5.2.1](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf):
  advantage/disadvantage, attack/save/damage timing, reactions, resistance,
  vulnerability, immunity, resources, and effect durations.

HDM deliberately omits arbitrary data paths, expression evaluation, and the
full PF2e actor-preparation pipeline.
