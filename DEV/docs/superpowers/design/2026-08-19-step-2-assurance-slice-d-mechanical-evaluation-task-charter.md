# Step 2 Retrospective Assurance — Slice D Task Charter: Mechanical Evaluation and Read Boundaries

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct the minimum architecture required for deterministic mechanical reads, derived calculations, declarative rule evaluation, bounded domain lookup, current/prospective state evaluation, and LLM-adjudicated context before judging the accepted Step-2 selector/accessor/query model.

This charter deliberately does not assume that the current Calculation Selector, MechanicalContext accessor, runtime Domain Query, pinned-view, or dependency-DAG design is correct. Those artifacts become evidence only after the problem framing is frozen.

## 2. System context

HDM combines:

- an LLM that interprets natural language and may adjudicate explicitly fiction-dependent facts;
- a deterministic runtime that owns engine-resolvable mechanics;
- canonical/HOT world records plus disposable SQLite indexes/caches;
- reusable definitions containing bounded declarative mechanics;
- prospective execution that must calculate effects before committing mutation;
- later checkpoint/recovery and multiplayer requirements;
- a catalog that is extensible in data but closed over executable engine capabilities.

The read/evaluation boundary is therefore security- and correctness-sensitive: a convenient generic read or context value can become an accidental second authority or an executable query language even when no mutation API is exposed.

## 3. Problem statement

Define the smallest coherent contract answering four distinct questions:

1. **What calculation is being resolved?**
2. **What authoritative or derived fact may that calculation read?**
3. **What bounded runtime lookup may infrastructure perform to locate relevant state owners?**
4. **Which input facts may be supplied by the LLM/host rather than derived by the engine?**

The architecture must prevent those surfaces from collapsing into arbitrary path/query/eval access while still supporting real D&D mechanics, efficient scoped evaluation, prospective state, effect/condition participation, temporal due execution, and later extensibility.

## 4. Goals

The architecture must support at minimum:

1. direct reads of authoritative state such as current HP or LifeState;
2. derived reads such as maximum HP, Resource capacity/availability, named Condition presence/value, and other registered calculations;
3. pure passive contributions from reusable Feature/Effect/Condition/Asset mechanics;
4. predicates over a closed typed set of values and explicitly admitted fiction-dependent invocation facts;
5. application-relative mechanics bound to source/target/declared application parameters;
6. current Effect/Condition effectiveness that can change when immunity/suppression/availability changes without rewriting lifecycle state;
7. prospective evaluation against a proposed mutation set before commit;
8. detection and rejection of dependency cycles introduced only by a concrete combination of otherwise-valid mechanics;
9. runtime lookups for relevant Effect, Resource, support, temporal, provenance, and owner state without granting declarative content a world-query DSL;
10. deterministic evaluation after retry/restart without silently mixing state revisions;
11. scoped caching/indexing that cannot become second authority;
12. efficient ordinary evaluation without full-campaign scans or a full-campaign dependency graph rebuild;
13. bounded context for due owner-local scheduled triggers without granting them more read authority than ordinary Activities/Rules;
14. clear failure behavior when exact engine-owned data is unavailable, stale, cyclic, invalidly bound, or improperly supplied by the LLM.

## 5. Non-goals

This slice does not finalize:

- exact Step-3 IntentPlan/Resolution/Signal/Event ordering;
- mutation transaction representation or receipt schema;
- full LLM referent-resolution workflow;
- lore/secret disclosure and prompt-context selection owned by Step 4;
- repository checkpoint publication or multiplayer revision reconciliation owned by Step 5;
- exhaustive selector/accessor seed enumeration owned by Step 6;
- physical cache/index implementation unless a correctness boundary requires it.

The slice must nevertheless leave later stages with an unambiguous authority contract rather than an unspecified `context` or `query` escape hatch.

## 6. Required conceptual separations to investigate

The assurance must determine whether the architecture needs distinct representations for:

### Calculation surface

A named deterministic calculation that accepts typed contributions or policy input, such as:

```text
maximum HP
Resource capacity
Condition applicability
damage received
Effect duration
attack roll
```

Questions:

- Does naming a calculation also authorize reading its result?
- Can one calculation recursively invoke another?
- What input classes can it depend on?
- Which calculation results may normalize or constrain authoritative stored state?

### State/context read

A typed value read from one logical state view, such as:

```text
current HP
resolved maximum HP
LifeState
Condition effective presence
Resource availability
bound Effect parameter
```

Questions:

- Is the read direct authority, derived engine fact, invocation-adjudicated fact, or something else?
- What arguments and subject kinds are legal?
- How is provenance retained for diagnostics/dependency analysis?
- Can reads enumerate collections, or only return bounded typed values?

### Runtime domain lookup

Infrastructure may need to locate:

```text
nonterminal Effect applications for one target/family
ResourceState for one owner/resource definition
support descendants
Temporal Agenda due entries
Condition applications by typed origin
resolved definitions
```

Questions:

- Which consumers may invoke these lookups?
- Are arguments closed per operation/domain?
- Can results escape into declarative content as arbitrary collections?
- How are lookup scope and deterministic ordering defined?

### Invocation-adjudicated fact

Some mechanics depend on facts the deterministic engine may not own directly, for example a fiction-dependent visibility/reachability judgment.

Questions:

- How is such a fact registered?
- Which calculations may consume it?
- Can it influence stored-state normalization, durable capacity, Effect lifecycle, or other facts that must remain reconstructable without the original LLM invocation?
- What happens on replay/recovery when the original adjudicated fact is no longer present?

## 7. State-view consistency questions

The accepted architecture must be tested against:

- one calculation reading direct and derived values from incompatible revisions;
- a committed-view cache reused inside a prospective view;
- a prospective Effect application changing the very predicates/capacities used to validate the application;
- lazy hydration occurring while the underlying committed frontier changes;
- a suspended Resolution resuming after other state changed;
- a current Condition effectiveness calculation reading the prospective immunity that caused its own reevaluation;
- due scheduled-trigger execution reading owner/source/target state at the wrong revision.

The architecture must define logical immutability/pinning strongly enough to make such mixing mechanically detectable rather than relying on caller discipline.

## 8. Dependency and cycle questions

The assurance must reconstruct what participates in dependency analysis, including at least plausible nodes for:

```text
calculation result
registered accessor/derived fact
Effect availability
Effect arbitration
Condition aggregation
Condition intrinsic mechanics
Condition applicability/current effectiveness
Resource capacity
scheduled-trigger eligibility/binding where mechanically dependent
```

Questions:

- Which dependencies are statically known from definitions?
- Which only appear after concrete source/target/application binding?
- Can a cycle be introduced by two valid Effects applied together?
- At what transition must a newly introduced cycle be rejected?
- Are fixed-point/repeated-until-stable semantics ever permitted implicitly?
- Can dependency evaluation remain scoped to the hydrated mechanical component rather than campaign-global state?

## 9. State-stability and reconstruction questions

Some derived calculations only affect one invocation. Others constrain authoritative state.

Examples:

```text
attack bonus this roll
    invocation-local result

persistent Resource capacity
    may require current-state normalization when capacity truly shrinks

maximum HP
    affects legal current HP and lifecycle-related prospective calculations
```

The assurance must determine:

- whether every calculation may depend on invocation-adjudicated facts;
- whether a distinct restriction is needed for state-normalizing/state-stable calculations;
- what evidence must be persisted if an adjudicated fact is allowed to influence a durable state change;
- whether a calculation that cannot be reconstructed from durable/pinned mechanical state may safely define an invariant over stored state.

This is a direct carry-forward from Slice A and must be explicitly resolved.

## 10. Conditions and Effects

Test these cases:

1. Poisoned application exists; target later gains Poisoned immunity; the application remains nonterminal but named Condition effectiveness becomes false.
2. Immunity later ends before the Poisoned application expires; effectiveness returns without lifecycle resurrection.
3. Frightened from two sources evaluates source-relative mechanics without a general source enumeration query inside declarative content.
4. One Effect changes a fact used by another Effect's availability predicate.
5. Prospective activation would create a dependency cycle only for one concrete target.
6. A shadowed Effect remains structurally supported and timed while not currently contributing.
7. An Effect's scheduled trigger becomes due while the Effect is still live; the child Activity receives only closed owner/source/target/application context and normal typed reads.
8. The Effect becomes terminal at the same temporal boundary as its scheduled trigger would become due; exact ordering is Step 3, but no read/query authority may decide the result by incidental index order.

## 11. LLM/core authority failure scenarios

The architecture must survive:

1. LLM supplies `current_hp=17` even though authoritative state says 9.
2. LLM supplies `resource_capacity=4` as a convenient adjudicated fact.
3. LLM supplies a fiction-dependent fact that is registered for one selector but tries to use it in another.
4. A predicate attempts to read arbitrary JSON path `target.state.foo.bar`.
5. A content definition attempts a generic `where` query over all Effects.
6. A scheduled trigger declaration attempts to embed an arbitrary predicate/query/callback with world access.
7. A runtime domain query accepts a free-form filter object that can encode SQL/query semantics indirectly.
8. A cache result computed from an LLM-adjudicated fact is reused in a later invocation that did not provide that fact.
9. An invocation-adjudicated fact becomes the hidden reason a durable ResourceState was clamped, but the fact is absent on recovery.
10. The LLM invents a selector/accessor/operation ID that looks plausible.

## 12. Query and performance failure scenarios

1. `condition.present` scans every Effect in the campaign.
2. `resource.available` scans all Resources owned by all actors.
3. an Effect-family arbitration lookup depends on SQL row order.
4. source-scoped Condition removal uses a generic callback/filter rather than a closed provenance key.
5. dependency validation rebuilds the entire campaign graph for every application.
6. cache invalidation is so broad that ordinary single-target resolution becomes effectively campaign-global.
7. a derived cache becomes necessary for correctness after restart because the source inputs are not recoverable.
8. query result ordering leaks into mechanical tie-breaking where the rules did not define an order.

## 13. Quality attributes / fitness criteria

### Authority

- no selector/accessor/query/cache becomes a second writable authority;
- engine-owned mechanical facts cannot be overridden by LLM invocation data;
- declarative content has no arbitrary world-query or executable expression capability.

### Determinism

- same pinned state view + same registered invocation-adjudicated inputs + same fixed RNG yields the same reads/calculations;
- result does not depend on hydration, cache, SQL, map, or list order;
- missing/stale/cyclic inputs fail explicitly rather than being guessed.

### Reconstruction

- a durable state invariant can be re-established after restart from authoritative state plus explicitly durable evidence;
- disposable caches/indexes/DAG projections can be rebuilt;
- invocation-only facts are not silently required to reconstruct canonical state unless their causal evidence is deliberately persisted by a later-stage contract.

### Extensibility

- adding a new calculation/read normally requires registered typed metadata, not arbitrary code or paths;
- a future ruleset can add bounded accessors/selectors without exposing general database structure;
- new derived stages must declare dependency contracts before participating.

### Performance

- ordinary evaluation scope is actor/source/target/procedure-local plus relevant Effects/Resources/definitions;
- no full-campaign scan or graph rebuild is architecturally required for the common path;
- indexes/caches remain optional accelerators, not hidden authority.

### Testability / observability

- each read/calculation exposes enough typed provenance/reason to diagnose its inputs;
- invalid subject/argument/input-class/dependency bindings are mechanically testable;
- committed/prospective cache separation and cycle failures can be fixture-tested;
- domain-query surface can be exhaustively audited for forbidden generic filters.

## 14. Known unknowns requiring investigation

- Whether current selector metadata distinguishes invocation-only permissible inputs from state-stable/reconstructable inputs.
- Whether current predicate `fact` support is sufficiently registered/typed or is an under-specified escape hatch.
- Whether `resource.capacity` can currently depend on invocation-adjudicated facts despite Slice-A normalization semantics.
- Whether current `condition.applicability` metadata and dependency nodes fully support reevaluating already-existing applications under later immunity.
- Whether scheduled-trigger due execution needs any additional owner-bound accessor or can use ordinary Activity context without adding a new read surface.
- Whether current scoped dependency-DAG identity is concrete enough for per-application source-relative rules.
- Whether domain-query contracts are represented anywhere machine-readably or exist only as prose implementation constraints.
- Whether deterministic ordering requirements for multi-result runtime queries are explicit enough before Step 3.
- Whether lazy hydration/revision pinning has a sufficient failure contract or only a conceptual statement.

These are questions, not findings.

## 15. Evidence to inspect after this charter is frozen

Project evidence:

- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- mechanical surface/accessor/predicate/Rule Element schemas;
- selector/query design, adversarial review, and resolution;
- Effect/Condition and Resource assurance amendments;
- Slice-C scheduled-trigger resolution;
- relevant Step-2 focused tests;
- Step-3 Task Brief/Research only to expose downstream requirements after baseline coverage is understood.

External/primary evidence only if a concrete gap warrants it:

- official D&D/SRD rules proving a needed relational/context-dependent read;
- primary comparable-engine contracts where they illuminate a specific read/dependency/query design question;
- database snapshot/transaction documentation only if needed to resolve logical pinning semantics.

## 16. Exit criteria

Slice D closes only when:

1. calculation, read, runtime-query, and invocation-adjudicated input responsibilities are explicit;
2. every charter requirement is mapped to the accepted baseline;
3. the Slice-A state-stability carry-forward is resolved;
4. current Condition applicability and scheduled-trigger read boundaries are covered;
5. concrete dependency-cycle and revision-mixing attacks are attempted;
6. generic query/path/eval escape hatches are ruled out or fixed;
7. an independent critic attacks the resulting model;
8. every finding is fixed, consciously deferred with a later owner, or escalated to a human architecture gate;
9. the result states `KEEP`, `AMEND`, or `REOPEN` with confidence and evidence.
