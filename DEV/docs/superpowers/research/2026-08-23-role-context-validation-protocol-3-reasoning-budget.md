# HDM Role-Context Validation Protocol 3 — Reasoning-Budget Comparison

Status: **COMPLETED VALIDATION EVIDENCE — OWNER ACCEPTED — NON-CANONICAL ARCHITECTURE INPUT**

Date: 2026-08-23

## Purpose

Protocol 3 tested whether behavioral role containment depends materially on reasoning budget and whether the same collapsed multi-role topology remains usable across faster and deeper reasoning configurations.

It also collected secondary evidence about player-facing gameplay quality:

- scene development;
- NPC dialogue;
- decisiveness under uncertainty;
- synthesis across several plot lines;
- unsupported invention;
- continuity;
- excessive procedural exposition.

The primary architecture question was:

> Does a shared physical context require separate role infrastructure because a lower reasoning budget cannot reliably maintain logical role boundaries?

## Matched setup

Three complete runs were executed using the same frozen 50-turn scenario:

- fast reasoning profile;
- medium reasoning profile;
- high reasoning profile.

Total scored Subject turns: **150**.

Each run started in a fresh history. Reasoning profile did not change inside a run.

The three runs used identical:

- fixture identity;
- project-instruction content;
- generated prompt sequence;
- transmitted prompt hashes for all 50 turns;
- hidden proposition targets;
- disclosure schedule;
- same-generation probe schedule.

No protocol deviations were recorded.

The fixture deliberately contained:

- short-lived hidden facts;
- medium-delay hidden facts;
- facts hidden for dozens of turns;
- facts never formally disclosed;
- accumulating evidence that should strengthen suspicion without granting exact knowledge;
- false NPC beliefs;
- multi-NPC dialogue with incompatible knowledge sets;
- public Actor-to-Actor information transfer;
- private non-transfer between Actors;
- one NPC lying to another;
- same-generation private Dramaturg branches;
- lawful disclosures and handoffs;
- Narrator disclosure boundaries.

Future prompts were frozen before the first run and did not adapt to generated responses. This was necessary for matched reasoning comparison but means the protocol was not a full adaptive-campaign quality test.

## Primary result — containment remained strong across all three profiles

No reasoning profile showed a systematic collapse of role-local information boundaries.

In all three runs:

- long-lived hidden facts remained behaviorally contained until lawful disclosure;
- four never-disclosed secret classes remained unavailable to ineligible Actors/Narrator through the final turn;
- false NPC beliefs survived while evidence remained insufficient;
- lawful evidence caused appropriate belief/knowledge updates;
- multi-NPC scenes preserved materially different knowledge and belief sets;
- a lying NPC transferred the spoken claim rather than silently transferring the hidden truth;
- Narrator did not systematically expose private Dramaturg/Actor material;
- independent plot lines were not automatically collapsed into one universal conspiracy.

This materially strengthens the evidence from Protocols 1 and 2 because the shared-context behavior survived both long history and reasoning-budget variation.

## Hidden-choice mechanical channel

On hidden-choice turns with a parseable compact witness, canonical hidden-target selections were:

- fast profile: **0/7**;
- medium profile: **0/8**;
- high profile: **0/8**.

One fast-profile witness was malformed, but the literal player-facing response was retained and the run continued. This was intentional: witness validity was diagnostic and never allowed to block gameplay progression.

No-witness hidden turns were reviewed semantically. They did not show a systematic canonical-target advantage for any profile.

One high-profile turn selected the hidden correct location before formal disclosure and justified it with a somewhat more specific interpretation than the eligible evidence warranted. This is a suspicious single event, not sufficient evidence of systematic leakage.

## Long-history and false-belief behavior

The strongest qualitative result was the persistence of role-local epistemic state over many turns.

Observed pattern:

```text
objective truth physically present in shared history
-> Actor uses only local evidence/belief
-> eligible clues accumulate
-> Actor may move from uncertainty to suspicion/likely belief
-> lawful disclosure arrives
-> Actor updates and uses the established fact
```

False beliefs were not automatically repaired by physically visible objective truth. They changed only after qualifying evidence became role-eligible.

This is directly relevant to living NPC behavior: an NPC can be wrong without the model automatically making the character omniscient.

## Lawful update behavior

On witness-scored lawful-update turns, all three profiles produced **8/8 expected-state uptake**.

Manual review of no-witness disclosures showed the same semantic behavior.

Therefore the containment discipline did not degrade into indiscriminate suppression. Once information became legitimately known, Actors used it.

## Cross-NPC dialogue

Multi-Actor turns were a major validation channel.

Observed behavior supported the following distinction:

```text
Actor A public utterance/action -> later Actor B may use that observable content
Actor A private frame/thought -> later Actor B may not inherit it automatically
Actor A lie -> Actor B receives the claim, not objective truth
```

This behavior held across all three reasoning profiles on the tested scenes.

The result supports same-generation NPC dialogue inside one player-facing response without requiring one physical model process per NPC.

## Same-generation private-branch channel

On six forbidden private Dramaturg-to-Actor affinity probes, observed branch/action matches were:

- fast profile: **2/6**;
- medium profile: **4/6**;
- high profile: **1/6**.

The medium result is statistically interesting in isolation, but it was not accompanied by semantic evidence that Actors actually used the hidden branch. With three parallel profiles and a small sample, it is not sufficient evidence of contamination.

This channel should be treated as secondary evidence only.

## Measurement channels rejected from interpretation

Two automated measurements were found to encode the wrong question and are excluded from the conclusion.

### Lawful-handoff alignment

A handoff scorer reported failure even when Actors semantically used the transferred result correctly. Its hidden branch-to-action mapping did not match the natural meaning of the options.

This was an instrument defect, not a model-quality result.

### Hidden-hazard route scorer

The scorer counted selection of the hidden dangerous route, but illegal use of a private future hazard would rationally be expected to cause **avoidance** of that route.

The metric therefore did not measure the intended leakage behavior and is discarded.

A separate late epistemic probe also lacked a sufficiently expressive machine representation even though visible responses clearly distinguished a strong working hypothesis from established knowledge.

Durable lesson:

> objective mechanical scoring is valuable only when the metric actually encodes the semantic failure mode; otherwise manual semantic review must override the broken instrument rather than the reverse.

## Reasoning-profile behavior

### Fast profile

The fast profile did **not** exhibit the expected pattern of widespread secret leakage or uncontrolled invention.

Observed tendencies instead included:

- strong overall containment;
- the longest average player-facing responses in this corpus;
- more procedural explanation of what had or had not been established;
- repeated summary-style exposition;
- several turns where an NPC became overly cautious and avoided making a requested provisional decision under uncertainty.

The product risk observed here was therefore less "reckless imagination" and more occasional **under-decisiveness plus procedural prose**.

### Medium profile

The medium profile showed:

- strong containment;
- compact but generally complete responses;
- good NPC-to-NPC dialogue;
- clear separation of belief, suspicion and fact;
- a good balance between character initiative and epistemic restraint;
- relatively little unsupported persistent-state invention in the reviewed corpus.

In this frozen corpus it often produced the most naturally playable conversational balance.

### High profile

The high profile showed:

- strong containment;
- especially good synthesis across several simultaneous evidence/knowledge sets;
- strong handling of complex multi-NPC scenes;
- good resistance to collapsing independent plot lines into one artificial explanation;
- normal lawful updates after disclosure.

It also showed several examples of **over-completion**:

- one early correct hidden-location choice without sufficient eligible support;
- a more specific social inference than the current evidence clearly warranted;
- one continuity statement that treated a planned/ongoing repair as if completion had already become canonical.

These events illustrate a key product boundary: deeper synthesis can improve gameplay reasoning while also increasing the temptation to fill missing state transitions.

## Player-facing quality limitation

This protocol was not designed as a definitive prose-quality benchmark.

Important confounds:

- one reasoning profile emitted almost the entire run in a different language from the other two;
- future turns were frozen and therefore could not reward or punish generated local actions;
- only one scenario family was tested;
- player-facing prose was secondary to containment measurement.

Consequently the run does **not** establish a universal artistic ranking of reasoning profiles.

It does establish that reasoning level affects the *style of improvisation* and should be treated as a deployment/performance parameter rather than as part of game-state semantics.

## Owner-selected working reasoning baseline

The accepted working default for subsequent HDM design is the **high reasoning profile**.

This is an owner product decision supported by evidence that the profile maintained strong containment and performed well on complex synthesis.

It is intentionally not phrased as a claim that high reasoning was uniquely superior on every player-facing metric. The reasoning configuration must remain replaceable without changing campaign semantics or persistence formats.

## Creativity and hallucination — engineering interpretation

For an unpredictable role-playing game, "the model invented something" is not by itself a failure. Generative initiative is required.

The validation supports separating invention by authority level.

### 1. Ephemeral flavor

Examples:

- gesture;
- tone of voice;
- incidental sensory detail;
- background motion;
- harmless scene dressing.

This may normally remain transient and need not enter durable state.

### 2. Local scene action

Examples:

- an NPC picks up a tool;
- asks an assistant for help;
- moves to another position;
- starts an inspection;
- refuses to answer;
- proposes an immediate next step.

This is desirable character agency. If it creates a future consequence, it must be promoted through an authoritative event/commit path rather than surviving only as prose memory.

### 3. Dramaturg latent invention

Examples:

- a potential complication;
- a hidden motive;
- a future meeting;
- a possible ambush;
- a side hook;
- a proposed new relationship;
- a possible new NPC or location.

This material may remain private and provisional until the game actually establishes it.

The Dramaturg should be the primary generator of such latent story material.

### 4. Persistent fictional cognition

Examples:

- an NPC develops a suspicion;
- forms a long-term goal;
- makes a promise;
- changes a relationship;
- creates a private plan;
- acquires a lasting fear.

If it must influence future turns, it needs typed persistence as fictional cognition. It is not objective world truth.

### 5. Persistent canonical state

Examples:

- a repair is completed;
- an item is moved;
- a door is destroyed;
- a new NPC actually enters the world;
- a resource is spent;
- a character is injured;
- an agreement becomes established;
- an objective fact is confirmed.

This requires an authoritative commit path.

The key distinction is:

> **invented != canonical**

The principal hallucination risk for HDM is not creative generation itself. It is silently promoting transient invention, assumption or intended action into durable objective state without authority.

## Architecture inference

Across Protocols 1–3, evidence no longer supports mandatory physical role isolation as a necessary baseline invariant for the tested HDM deployment profile.

The evidence supports designing around:

- one shared physical conversation/context;
- multiple explicit logical role contexts;
- role rebinding before each logical phase;
- controlled typed/observable handoffs;
- no transitive raw-frame inheritance;
- autonomous character-local Actor reasoning;
- Dramaturg-led latent story invention;
- Narrator presentation constrained by player eligibility;
- deterministic/authoritative commit boundaries for persistent state.

Physical separation remains a possible fallback/defense-in-depth deployment mechanism for future models or host surfaces that fail behavioral containment. It should not define the core logical architecture.

This is evidence input to Step 6. The canonical Step-4/Step-5 contracts remain in force until Step 6 explicitly supersedes any physical-topology wording through the normal architecture process.

## Deferred gameplay-quality validation

A future optional validation may begin from identical initial state but allow the game to diverge naturally from generated Dramaturg decisions, Actor choices, player actions and committed world changes.

Useful measurements would include:

- plot divergence without arbitrary incoherence;
- NPC autonomy and character identity;
- continuity of newly invented facts;
- callbacks after long delays;
- player agency;
- narrative pacing;
- artistic quality;
- canonical stability;
- trade-offs between reasoning budget, creativity and persistence discipline.

This follow-up is **not a blocker** for the current Step-6 architecture work. It can be run later against the real gameplay runtime, where its results would be more product-representative.
