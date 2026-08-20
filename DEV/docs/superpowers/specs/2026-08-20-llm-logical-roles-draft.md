# HDM Logical LLM Roles — Cross-Cutting Architecture Draft

Status: **DRAFT — ROLE SET APPROVED IN PRINCIPLE / INDIVIDUAL CONTRACTS NOT YET CANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Related active work:

- `2026-08-20-step-4-lore-knowledge-story-task-brief.md`
- `2026-08-20-step-4-lore-knowledge-story-research-draft.md`
- `2026-08-20-step-4-lore-knowledge-disclosure-decision-brief.md`
- Step-3 canonical deterministic execution boundary

## 1. Purpose

HDM is a hybrid engine. The deterministic core owns authoritative state,
mechanics, validation, random-outcome integrity, execution and commit. LLMs are
not merely a prose layer: they are semantic and creative coprocessors for tasks
that are intentionally difficult or undesirable to reduce to a fixed formal
algorithm.

This draft records six logical LLM roles that should be designed independently
before physical call topology is chosen:

1. Interpreter;
2. Dramaturg;
3. Actor;
4. Narrator;
5. Chronicler;
6. Commentator.

A **logical role is not necessarily a separate long-lived agent, model, process
or model call**. The role defines responsibility, context eligibility, authority,
inputs, outputs and failure boundaries. Step 6 may later combine compatible
roles into one invocation or separate one role into several invocations when
quality, isolation, latency, cost or platform capabilities justify it.

The role model exists to prevent one general-purpose LLM context from silently
acquiring incompatible powers such as knowing all DM secrets while speaking to
a player, turning preparation into canon, or turning literary inference into a
world transition.

## 2. Global invariant

```text
LLM cognition / interpretation / creativity
                |
                | typed proposals / bounded semantic results
                v
       DETERMINISTIC CORE / AUTHORITIES
 truth / mechanics / validation / RNG / commit
                |
                | settled facts / authorized context
                v
      LLM presentation / reconstruction
```

No LLM role can make a proposition canonical merely by stating it.

No LLM role can mutate authoritative world state except through an accepted
runtime command or another explicit deterministic transition owned by the core.

No presentation role may treat narrative plausibility as evidence.

No role may receive broader hidden context merely because another role needed
that information earlier.

## 3. Role versus physical agent

The architecture separates two questions:

### 3.1 Logical role

A logical role answers:

- what problem is this LLM reasoning about?
- what information may enter its context?
- what information must not enter its context?
- what outputs may it propose?
- what outputs are authoritative, if any?
- what deterministic component validates or consumes the result?

These semantics belong primarily to Steps 4 and 6.

### 3.2 Physical invocation topology

A later implementation may decide, for example:

```text
Interpreter + Narrator
    -> one call with a strict phase boundary

Dramaturg
    -> occasional separate private call

Actor
    -> separate call only for important/nontrivial NPC decisions

Chronicler
    -> deferred/background-at-boundary call

Commentator
    -> independent spectator chat
```

or a different topology.

Such optimization must preserve the logical context and authority boundaries in
this document. Physical co-location never implies semantic authority merging.

## 4. Role 1 — Interpreter

### 4.1 Mission

Convert informal external language into bounded semantic candidates suitable for
deterministic binding and execution.

Examples:

- resolve what the player means by pronouns, nicknames and colloquial phrases;
- distinguish action, hypothesis, OOC correction, question and collaborative
  authorship request;
- identify intent, approach and mention spans;
- choose among host-supplied bounded candidates;
- provide only explicitly registered fiction-dependent invocation facts.

### 4.2 Typical context

May receive:

- current external message;
- recent discourse needed for reference resolution;
- authenticated player/PC/session identity;
- bounded visible scene/context candidates;
- relevant activity/entity candidate summaries;
- registered invocation-fact vocabulary.

Must not receive unrestricted campaign truth merely to improve language
understanding.

### 4.3 Output

Conceptually:

```text
InterpretationDraft
    message spans
    resolved/bounded mention candidates
    intent family
    approach
    material clauses
    optional invocation-adjudicated facts
    clarification requirement when genuinely blocking
```

The deterministic binder revalidates every executable identity and state
constraint.

### 4.4 Explicit non-authority

Interpreter does not:

- create world facts because the player asserted them;
- decide HP/resources/effects/eligibility when engine-checkable;
- commit actions;
- choose outcomes;
- narrate hidden information.

## 5. Role 2 — Dramaturg

### 5.1 Mission

Perform private GM preparation: construct useful **situations, pressures,
possibilities and causal preparation**, not a mandatory future plot.

The Dramaturg is the role most naturally allowed to reason across broad DM-only
context because its output remains non-canonical preparation until play causes
something to become real.

### 5.2 Typical context

May receive, when relevant:

- objective established and undetermined world/lore truth;
- DM-only secrets and proposition status;
- active threads, faction pressures, deadlines and processes;
- NPC/faction goals, resources and constraints;
- recent player interests and actions;
- consequences across multiple players/scenes where cross-scene awareness helps
  preparation;
- campaign premise, tone and boundaries;
- unresolved clues and existing credible discovery routes.

It should still receive the smallest useful preparation horizon rather than the
entire repository by default.

### 5.3 Output

Preferred output is a structured preparation proposal such as:

```text
PreparationDraft
    active pressure / problem
    involved actors and their goals
    likely reactions if conditions arise
    possible manifestations
    clue/evidence routes
    opportunities and constraints
    likely near-horizon developments if unopposed
    preparation dependencies / assumptions
    expiry or invalidation conditions
```

### 5.4 Critical invariant — prepare situations, not plot

The Dramaturg must not emit future events as guaranteed canon.

Bad:

```text
next_event = assassin attacks PC tonight
```

Better:

```text
pressure:
    assassin is searching for an opportunity
constraints:
    does not know room number
    avoids city guards
possible manifestations:
    follow party
    bribe servant
    wait near exit
opportunities:
    target becomes isolated
    credible location information is acquired
```

Prepared scenes have no right to occur. Player choices, NPC choices, mechanics,
randomness and actual opportunity determine what becomes real.

### 5.5 Explicit non-authority

Dramaturg does not:

- commit world state;
- pre-author player actions;
- force prepared scenes;
- alter truth to preserve drama;
- change mechanical stakes after seeing outcomes;
- directly speak to the player from its DM-secret context.

## 6. Role 3 — Actor

### 6.1 Mission

Reason about non-formalizable decisions of an NPC, faction or other intentional
world subject **from that subject's own cognition and circumstances**.

The Actor exists to prevent both deterministic-core overreach into human-like
judgment and Dramaturg/Narrator contamination of NPC agency.

### 6.2 Typical context

For the represented subject, receive only relevant:

- stable identity, traits and values;
- current goals and pressures;
- known/believed/suspected/rejected propositions;
- current perception/observable scene facts;
- relationships and social position;
- resources/capabilities known to the subject;
- prior commitments and recent events known to the subject;
- risk tolerance and immediate constraints.

Actor should **not** receive unrestricted objective truth or Dramaturg-only
planning that the subject cannot know.

### 6.3 Output

Conceptually:

```text
ActorIntentDraft
    intended goal
    chosen approach
    optional speech intent / communicative content
    assumptions based on subject knowledge
    confidence/ambiguity where relevant
```

When the intent has mechanical consequences it returns to Interpreter/binder/
RuntimeCommand machinery like any other world action.

### 6.4 Dramaturg versus Actor

Dramaturg may identify an interesting possibility:

```text
betrayal by the count would create pressure
```

Actor(count) may still conclude:

```text
do not betray now;
lie and buy time instead
```

because the count's actual goals, knowledge, constraints and incentives do not
support betrayal yet.

This separation is essential to emergent rather than scripted play.

### 6.5 Explicit non-authority

Actor does not:

- know facts unavailable to the represented subject;
- optimize for narrative excitement over subject motivation;
- alter deterministic mechanics;
- commit its own proposed action;
- rewrite objective truth to justify its choice.

## 7. Role 4 — Narrator

### 7.1 Mission

Serve as the player-facing Master/frontman for **current gameplay**.

Narrator turns resolved, knowledge-safe state into clear, vivid and responsive
player-facing language while preserving pacing, tone, humor, player agency and
mechanical explanation preferences.

### 7.2 Typical context

May receive:

- what the current PC can perceive and legitimately know;
- what the current human player has been disclosed;
- newly settled observable consequences;
- authorized NPC speech/action outputs;
- settled mechanical receipts and selected explanation detail;
- current narrative/tone context;
- only those contextual facts eligible for player narration.

It should not receive DM-only truth merely because adjudication used it.

### 7.3 Output

Player-facing response, potentially including:

- scene description;
- NPC dialogue;
- immediate consequence narration;
- concise or detailed mechanics explanation;
- pacing/transition prose;
- one genuinely blocking question when required;
- an actionable endpoint that returns voluntary control to the player.

### 7.4 Critical invariant — narration is projection

Narration may embellish presentation but may not establish a material fact that
was not already resolved/authorized.

Narrative desirability does not feed backward into STATE/RULES/RANDOMNESS/
CONSEQUENCES.

### 7.5 Explicit non-authority

Narrator does not:

- choose voluntary player actions, beliefs, emotions or speech;
- expose private truth not eligible for the current context;
- turn stylistic connective tissue into new factual history;
- overwrite committed outcomes for pacing;
- treat its own prior prose as stronger authority than structured state.

## 8. Role 5 — Chronicler

### 8.1 Mission

Transform already occurred campaign evidence into the non-canonical durable
`STORY` read/presentation model.

Chronicler is an **archive author/editor**, not a live-game authority.

### 8.2 Primary sources

Depending on Story layer, it may use:

- retained runtime messages / visible discourse;
- LOG / SemanticEvents;
- selected MechanicalEvents/receipts;
- canonical entity/lore references needed to make the record coherent;
- existing Story records for continuity/editing.

### 8.3 Outputs

```text
STORY/
    TRANSCRIPT/
    EVENTS/
    MECHANICS/
    NARRATIVE/
```

The four layers are non-canonical projections with explicit source/cross-layer
references.

Chronicler may also maintain narrative grouping/index metadata such as chapter
order/title and ordered NARRATIVE refs. Chapter grouping is not a world entity.

### 8.4 Layer responsibilities

`TRANSCRIPT`:
- retained participant discourse useful for reconstruction;
- not raw hidden reasoning/tool plumbing;
- not world truth merely because someone said it.

`EVENTS`:
- story-facing adaptation of durable semantic history;
- may merge/split source events for readability;
- retains provenance refs;
- not current-state authority.

`MECHANICS`:
- curated player/spectator-relevant mechanics;
- e.g. important rolls, HP changes, resources, effects/conditions, durations,
  LifeState and tactically material facts;
- not a duplicate state/checkpoint/trace dump.

`NARRATIVE`:
- editable literary prose;
- optimized for coherent reading and later interactive retelling;
- independent from chapter grouping;
- may be rewritten for quality without changing canon.

### 8.5 Explicit non-authority

Chronicler does not:

- adjudicate current gameplay from STORY;
- silently change canon to improve prose;
- invent missing historical events;
- copy entire authoritative state into Story;
- turn Story indexes/chapters into world entities.

## 9. Role 6 — Commentator

### 9.1 Mission

Provide an **interactive spectator-facing retelling over `STORY`**.

Commentator is analogous to a sports commentator or interactive documentary
host. It does not write the campaign and normally does not write STORY; it reads
and navigates already prepared Story material in response to a guest/spectator.

### 9.2 Typical interactions

A guest may ask:

- continue the story;
- rewind to an earlier event;
- jump to the first meeting with an NPC;
- explain why a later event happened;
- quote/reconstruct what someone actually said;
- show the mechanics of a battle;
- skip combat and continue afterward;
- retell a segment as noir, comedy, tragedy, epic fantasy or another style;
- focus only on one character or plot thread;
- compare two moments in the campaign.

### 9.3 Primary context

Normal Commentator mode should be **STORY-first / STORY-only by default**:

```text
NARRATIVE
    main readable retelling

EVENTS
    factual story spine

TRANSCRIPT
    exact/reconstructed dialogue evidence

MECHANICS
    optional technical commentary
```

If the required answer is absent from Story, Commentator should say that the
retained story does not establish it rather than search hidden authoritative
state and fill the gap.

A future explicit debug/deep-source mode may traverse provenance into canonical
sources, but that is a distinct later capability and not the default spectator
role.

### 9.4 Narrative freedom versus factual freedom

Commentator has broad **presentation freedom**:

- style;
- tone;
- pacing;
- emphasis;
- ordering/navigation;
- compression and expansion;
- explanatory commentary;
- perspective/focus.

It has no factual freedom to invent events, motives, dialogue, mechanics or
causal links that Story does not support.

Useful internal distinction:

```text
RECONSTRUCTION
    what Story establishes happened

COMMENTARY
    interpretation/analysis of those facts
```

Interpretation must be marked as interpretation when it goes beyond explicit
recorded causality.

### 9.5 Spectator session state

Navigation/presentation state such as:

```text
current_story_cursor
current_focus
preferred_style
requested_detail
mechanics_detail
```

is spectator-session state, not campaign canon.

### 9.6 Explicit non-authority

Commentator does not:

- alter WORLD/STATE/LOG;
- create events;
- promote Story statements to canon;
- treat style as evidence;
- fill unsupported gaps with plausible fiction;
- participate in current gameplay unless explicitly entering a different role.

## 10. Role topology

The conceptual flow is:

```text
                          +------------------+
                          |    DRAMATURG      |
                          | private GM prep  |
                          +--------+---------+
                                   |
                               PREPARATION
                                   |
                                   v
Player --> INTERPRETER --> deterministic CORE/BINDER
                                   ^          |
                                   |          | settled facts / receipts
                              ACTOR ----------+
                                              |
                                      disclosure/context
                                           filtering
                                              |
                                              v
                                          NARRATOR
                                              |
                                              v
                                            Player

Committed history / transcript / mechanics
                   |
                   v
               CHRONICLER
                   |
                   v
                 STORY
                   |
                   v
              COMMENTATOR
                   |
                   v
            Guest / Spectator
```

This diagram is logical, not a required synchronous invocation graph.

## 11. Context-envelope principle

Each role must have an explicit context envelope.

The envelope is more important than a general instruction such as "do not reveal
secrets" because an LLM cannot leak material that was never supplied to that
invocation/context.

Illustrative envelopes:

```text
INTERPRETER
    external language + bounded visible candidates

DRAMATURG
    broad DM truth + preparation horizon

ACTOR
    one subject's cognition + perceptions + goals

NARRATOR
    player/PC-eligible facts + settled results

CHRONICLER
    historical source evidence needed for Story projection

COMMENTATOR
    Story retrieval surface + spectator conversation
```

Physical repository readability is not the security boundary. These envelopes
exist to prevent accidental semantic leakage and authority confusion during LLM
reasoning/output.

## 12. Cross-role handoff discipline

Roles should exchange the **smallest stable product** required by the consumer,
not inherited opaque conversational context.

Examples:

```text
Interpreter -> core
    InterpretationDraft

Dramaturg -> preparation store/current GM workset
    PreparationDraft

Actor -> core
    ActorIntentDraft

core -> Narrator
    settled observable consequence bundle

history -> Chronicler
    source refs + authorized projection payload

STORY -> Commentator
    retrieved Story records + indexes
```

This reduces secret/context contamination and makes role behavior testable.

## 13. Preparation is not canon

Dramaturg output deserves an explicit non-canonical lifecycle.

Preparation may be:

- used;
- invalidated by player action;
- revised;
- discarded;
- promoted only when a later world decision/event actually establishes something.

A prepared clue route, scene possibility, NPC likely reaction or potential
complication is not a future fact.

Exact persistence and retention of preparation is not decided in this draft.

## 14. Relationship to Step 4

Step 4 should define the semantic context boundaries required by the roles,
especially:

- objective proposition authority (`world.lore_fact`);
- in-fiction epistemic state (`world.knowledge`);
- human-player disclosure state;
- context eligibility for adjudication, NPC cognition, player narration and
  Story/spectator reconstruction;
- Story projection records and provenance;
- retirement of old `Secret` and `world.chapter` ownership mistakes;
- promotion rules when local/adjudicated material must become durable canon.

Step 4 does **not** need to fix exact model-call orchestration.

## 15. Relationship to Step 6

Step 6 should revisit the six roles as an explicit LLM execution architecture
problem and decide, using actual runtime/model constraints:

- which logical roles require physically isolated calls;
- which roles may safely share a call with a hard phase/context boundary;
- when Dramaturg is invoked and how far ahead it prepares;
- when Actor deserves a separate call versus bounded reasoning inside another
  call;
- whether Chronicler is eager at persistence boundaries or lazily generated;
- Commentator retrieval/tool topology;
- model choice by role;
- token/context budgets;
- latency and cost budgets;
- caching/reuse;
- observability and evaluation;
- failure/fallback behavior;
- role-specific prompt/schema contracts;
- mode isolation;
- prevention of private-context carry-over across logically isolated roles.

## 16. Role-specific evaluation questions

### Interpreter

- Does colloquial intent map to the right bounded candidate?
- Does the role ask clarification only when materially necessary?
- Does it refrain from inventing unchecked entities/facts?

### Dramaturg

- Does preparation create useful pressure without scripting player outcomes?
- Are future developments causally constrained by actual actor goals/resources?
- Does unused prep remain discardable?

### Actor

- Does the decision follow the subject's knowledge/goals rather than DM truth?
- Does the subject avoid assistant-like omniscience/helpfulness?
- Are proposed intents mechanically legal after core validation?

### Narrator

- Does output reveal only eligible information?
- Does it preserve player agency?
- Does it project settled state rather than generate facts?
- Does it stop at meaningful voluntary decision points?

### Chronicler

- Can every material Story claim be traced to source evidence?
- Can Story be regenerated without affecting canon?
- Is MECHANICS curated rather than a state dump?
- Can NARRATIVE be edited without changing factual authority?

### Commentator

- Can a guest navigate by event/entity/chapter/thread?
- Can style change without factual drift?
- Does mechanics Q&A use Story MECHANICS rather than invent numbers?
- Does unsupported information return "not established in Story" rather than a
  plausible fabrication?

## 17. Open questions requiring later dedicated work

The six-role set is intentionally a draft boundary, not a complete subsystem
specification. Dedicated follow-up design should answer at least:

1. exact typed input/output contracts for every role;
2. how Dramaturg preparation is represented, retained and invalidated;
3. whether Actor reasoning applies only to NPCs or also organizations/collective
   actors and how their cognition differs;
4. exact context-assembler request classes and eligibility policy;
5. how player disclosure and PC knowledge combine for Narrator eligibility;
6. how much source truth Chronicler may access when building Story records;
7. Story indexing/retrieval contract needed by Commentator;
8. whether Commentator supports explicit provenance/debug traversal outside
   ordinary spectator mode;
9. role-specific error/fallback behavior when an LLM output is malformed or
   low-confidence;
10. physical call topology, model selection, budget and isolation in Step 6;
11. evaluation corpus and regression tests for each role;
12. whether any later proven use-case justifies a seventh role rather than an
    extension of these six.

## 18. Non-goals of this draft

This document does not define:

- specific model vendors or model names;
- one-agent-per-role deployment;
- autonomous background agents;
- long-lived agent memory as campaign authority;
- a generic multi-agent message bus;
- prompt wording;
- token budgets;
- scheduler behavior;
- Story schemas;
- preparation schemas;
- implementation code.

Those decisions belong to the appropriate later design stage.

## 19. Current recommendation

Treat the six roles as the accepted initial logical decomposition:

```text
INTERPRETER
DRAMATURG
ACTOR
NARRATOR
CHRONICLER
COMMENTATOR
```

The deterministic core remains authority for truth/mechanics/validation/commit.
The LLM roles remain first-class cognitive/creative components with explicitly
bounded authority rather than an undifferentiated assistant wrapped around the
core.

The most important design requirement is not "six agents". It is:

> six distinct responsibility/context contracts that remain valid regardless of
> how many physical model calls later implement them.
