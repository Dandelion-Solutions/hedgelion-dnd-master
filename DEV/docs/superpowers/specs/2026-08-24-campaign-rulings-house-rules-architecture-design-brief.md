# Campaign Rulings & House Rules Architecture — Design Brief

Status: **DESIGN BRIEF / OWNER DIRECTION APPROVED / NOT YET CANONICAL**

Date: 2026-08-24

Purpose:

> Consolidate the currently scattered HDM rules for LLM adjudication, temporary rulings, reusable campaign precedents and formalized house mechanics into one explicit architecture before S6D mechanical-boundary closure and before R2.7 resumes.

This document does not yet modify `GAME/CORE` or campaign machine schemas. It is the basis for the next owner discussion/design decision.

## 1. Existing accepted foundation

Current HDM already establishes the following pieces across `PLAY_POLICY.md`, `ADJUDICATION.md`, `RULES/README.md`, `MECHANICS_INTEGRITY.md`, Step-1 catalog evolution and the Activity/Rule-Element architecture:

1. live adjudication is local-first;
2. external RAW lookup is not an automatic live-turn dependency;
3. campaign house rules and established rulings precede baseline local rules knowledge;
4. the model may use established fiction, character capability, rules knowledge and common-sense causal reasoning to make the smallest fair local ruling;
5. a temporary ruling need not trigger later web research;
6. a materially reusable precedent should be persisted;
7. house mechanics expressible through existing typed policy/Feature/Rule Element/Activity machinery should use those mechanisms;
8. campaign content may add new stable IDs but may not silently same-ID override shipped definitions;
9. true replacement of shipped reusable rules belongs to an explicit ruleset package/profile change/fork boundary;
10. whatever ruling is chosen still passes `MECHANICS_INTEGRITY`: required RNG/math/state mutation cannot be replaced by narration;
11. engine-owned state such as HP, Resource state and deterministic capability cannot be supplied by the LLM as if it were authoritative engine state.

These principles are individually strong, but no single current owner defines their lifecycle and interaction.

## 2. Missing architecture

Current documentation does not fully define:

- the difference between one-off adjudication, temporary ruling, durable campaign precedent and deliberate house rule;
- when a ruling should become durable;
- what exactly `HOUSE_RULES.md` is allowed to own;
- whether a durable nonformalizable ruling needs stable identity/scope/supersession metadata;
- how an LLM-only judgment becomes a typed execution input without gaining direct mutation authority;
- when repeated prose policy should be formalized into catalog mechanics;
- when formalization is inappropriate because the rule genuinely depends on rich fiction/context;
- how deterministic execution cites or traces the ruling basis without persisting chain-of-thought;
- how contradictions between house rules, campaign rulings and typed mechanics are detected/resolved;
- how a ruling is superseded/corrected without rewriting already accepted historical outcomes;
- how this policy remains fast enough for ordinary play.

## 3. Proposed two-channel rules architecture

HDM should explicitly recognize two legal channels that converge before accepted gameplay consequence.

### Channel A — formalized deterministic mechanics

Use when the mechanic can be represented reliably through existing typed machinery:

```text
registered policy / definition
    -> Rule Elements / Activities / Resources / Effects / other typed owners
    -> Step-3 deterministic execution
    -> accepted state/events
```

Examples include recurring numerical modifiers, resource costs, action-economy changes, deterministic recovery rules, reusable spell/feature behavior and other mechanics whose relevant semantics can be stated as closed machine contracts.

### Channel B — bounded LLM adjudication

Use when material judgment depends on open-ended fiction, intent, causal reasoning or circumstances that are not sensibly reducible to a static catalog expression:

```text
current authoritative state + eligible fiction + applicable ruling policy
    -> LLM adjudication
    -> bounded typed adjudication result/input
    -> deterministic validation/execution where mechanics apply
    -> accepted state/events
```

Examples may include:

- selecting a fair DC for an unusual improvised attempt;
- deciding whether a fictional support is strong enough to attempt a maneuver;
- interpreting whether a broad player declaration maps to one available capability or needs clarification;
- judging social leverage/risk/feasibility from current NPC goals and circumstances;
- deciding whether an improvised magical interaction is possible under established campaign physics before any required roll/cost is executed.

The LLM owns the bounded judgment, **not** the resulting engine state.

## 4. Authority boundary

Proposed law:

> A ruling may establish an adjudication decision or reusable adjudication policy within its declared scope. It may not directly establish engine-owned mechanical state, fabricate RNG, mutate records, invent unavailable character capability, or bypass a typed execution/acceptance boundary when the outcome is mechanical.

Therefore legal examples include:

```text
ruling decides DC = 15
    -> accepted Activity parameter
    -> DiceEngine + deterministic comparison

ruling decides fiction.target_reachable = true
    -> authorized invocation-adjudicated fact
    -> deterministic Activity predicate/execution

ruling decides the attempt is impossible under established fiction
    -> typed IMPOSSIBLE adjudication outcome
```

Illegal examples include:

```text
ruling says actor now has 37 HP
ruling declares the die rolled 19
ruling silently grants an unknown spell
ruling directly edits canonical state because the prose says so
ruling invents an arbitrary Python/query operation
```

## 5. Proposed ruling lifecycle

Use a small lifecycle rather than treating every judgment as a house rule.

### 5.1 Situational adjudication

One bounded judgment for the current case.

Default durability: **ephemeral as policy**.

Its accepted gameplay consequence may of course become durable through normal owner state/events.

Do not persist the rationale merely because a check happened.

### 5.2 Temporary ruling

A current-case or short-horizon interpretation used because exact local rules are unavailable/ambiguous.

Default durability: only when necessary to preserve consistency across an unresolved/repeating local situation.

No automatic web follow-up is required.

### 5.3 Campaign ruling / precedent

A reusable adjudication decision that should constrain future analogous cases in this campaign.

This is the main missing durable semantic layer.

A campaign ruling should have enough stable metadata to support:

- stable ruling identity;
- scope/applicability;
- active/superseded lifecycle;
- concise decision text;
- relevant constraints/exceptions;
- optional basis/source references without chain-of-thought;
- optional typed mechanic references when part of the ruling is formalized;
- supersedes/superseded-by relation where needed.

### 5.4 Deliberate house rule

A campaign policy intentionally adopted to differ from or extend the baseline rules.

House rule semantics may be:

- **formalized** — executable through typed HDM mechanics;
- **adjudicative** — a durable LLM-interpreted policy because the material semantics depend on rich fiction/context;
- **hybrid** — prose policy defines applicability/intent while typed mechanics define the deterministic consequence once applicability is adjudicated.

### 5.5 Ruleset/package fork boundary

If a change is a true reusable replacement of shipped ruleset definitions/capabilities and cannot remain a campaign-owned additive rule with unique IDs, it belongs to explicit ruleset package/profile fork/evolution semantics rather than an implicit campaign override.

## 6. Proposed role of `HOUSE_RULES.md`

`GAME/CAMPAIGN/RULES/HOUSE_RULES.md` should remain valuable precisely because not all useful campaign rules are naturally executable machine data.

Proposed role:

> durable campaign-specific adjudication policy and precedent surface intended primarily for the LLM/human-readable rules layer, with stable lightweight structure sufficient for routing, scope, supersession and traceability.

It should **not** become:

- an arbitrary scripting language;
- a replacement for typed catalog mechanics;
- a writable copy of Actor/Asset/Effect/Resource state;
- a place to store every one-off DC/check;
- a dump of external rulebook text;
- a hidden second ruleset package.

A future design decision should choose whether this remains one Markdown file with stable entry conventions or becomes a small `RULES/RULINGS/` family plus an index. YAGNI favors one file until measured volume/discovery pressure proves otherwise.

## 7. Proposed promotion rule

Do **not** require every recurring ruling to become Python/catalog mechanics.

Instead:

```text
reusable ruling observed
    -> persist concise campaign precedent
    -> ask: is deterministic formalization beneficial and semantically faithful?
        yes -> formalize typed consequence/policy where appropriate
        no  -> keep adjudicative ruling in LLM-readable policy layer
```

Formalization is preferred when it materially improves:

- mechanical honesty;
- repeatability;
- latency;
- validation;
- resource/state accounting;
- reduced ambiguity.

Formalization is not preferred when it would require a brittle pseudo-language for rich fiction or merely move a judgment from the LLM into an unreadable maze of special cases.

## 8. Hybrid rule pattern

A particularly important supported shape should be:

```text
HOUSE RULE / CAMPAIGN RULING
    prose: when this fictional condition applies
        -> LLM adjudicates applicability

TYPED MECHANIC
    exact deterministic consequence once applicable
```

Example pattern, without making any concrete campaign rule normative:

```text
ruling applicability judgment
    -> typed boolean / enum / bounded numeric parameter
    -> registered Activity/Rule Element/policy
    -> deterministic RNG/math/state mutation
```

This allows HDM to use LLM strengths without giving the LLM direct mechanical authority.

## 9. Trace and persistence principle

Accepted execution should retain only the compact basis needed for reproducibility/audit, for example:

- ruling ID when a durable precedent was applied;
- accepted typed adjudication inputs;
- relevant source/state revision references where required by execution semantics.

Do not persist hidden reasoning or full internal deliberation.

A later change to a ruling does not retroactively rewrite already accepted historical mechanics unless an explicit repair/correction operation is authorized.

## 10. Latency principle

Rulings are intended to preserve play flow, not create bureaucracy.

Normal path:

```text
already-loaded house rules / current precedent
    -> one local LLM adjudication as part of the current reasoning pass
    -> typed execution input
    -> deterministic resolution
```

Do not add an ordinary-turn repository search, web lookup, second LLM pass or full ruling-corpus scan when the relevant current policy is already in the loaded/assembled working set.

Persistence of a new reusable precedent happens at normal durability boundaries rather than forcing a GitHub commit after every ruling.

## 11. Candidate owning surfaces

Recommended design direction for owner review:

### `GAME/CORE/RULINGS.md`

One new CORE module owning:

- ruling lifecycle;
- LLM vs deterministic authority boundary;
- promotion/formalization policy;
- contradiction/supersession semantics;
- latency discipline;
- interaction with `ADJUDICATION.md`, `PLAY_POLICY.md`, `MECHANICS_INTEGRITY.md` and `RULES/README.md`.

Likely activation:

```text
load_when: local ruling, house rule, campaign precedent, improvised/adjudicated mechanics, rule ambiguity
```

It probably should not join the always-active guard set unless later analysis proves the boundary must apply to every turn through delegation from an always-active owner.

### `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

Campaign instance policy/precedent store, initially retained as Markdown.

### Machine interfaces

Do not create a generic executable `ruling` record merely because the prose layer exists.

S6D should provide only the typed mechanical receiving surfaces actually required: declared Activity parameters, invocation facts, mapping outcomes and other bounded accepted inputs.

A small machine index/schema for durable ruling identity may be justified later only if routing/scale/traceability requires it.

## 12. Required owner decisions before canonicalization

The current direction is owner-approved at the conceptual level, but the following exact design points should be discussed before editing shipped CORE:

1. Should durable campaign precedents and deliberate house rules share `HOUSE_RULES.md`, or be separated into two files/families?
2. Should every durable entry require a stable ruling ID and explicit scope/status metadata?
3. Should `RULINGS.md` be situational or part of the always-active guard set through a narrow invariant?
4. What is the threshold for mandatory formalization of a recurring ruling versus leaving it intentionally LLM-adjudicated?
5. Should a player-visible rules correction automatically create/supersede a durable ruling, or only when explicitly adopted as precedent?

## 13. Relationship to S6D and R2.7

S6D consumes only the mechanical-boundary result of this design:

```text
LLM judgment
    -> authorized typed input/proposal
    -> deterministic execution/acceptance
```

R2.7 later owns final persistence/root/index/instruction/test realization across the whole project.

The House Rules architecture should be canonicalized before S6D closes its Domain S6D-10, but S6D can begin earlier on independent selectors/seed/package tasks once the owner starts it.
