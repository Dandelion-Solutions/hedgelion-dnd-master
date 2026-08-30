# R2.2 Actor Continuity / Cognition / Relationships — Evidence Ledger

Status: **RESEARCH EVIDENCE / PRE-DECISION SYNTHESIS**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-cognition-task-brief.md`

This ledger records source-derived constraints, research qualifiers and current architectural deltas. It is not an accepted design.

---

## 1. Established canonical / current-owner constraints

### C01 — `world.actor` is one progressively materialized Actor identity

Source: `DEV/ARCHITECTURE/ACTOR_MODEL.md`.

Actual claim:

- NPCs, PCs, companions and mechanically resolved creatures use one `world.actor` kind;
- Actor detail is materialized only when known/needed;
- instance state owns individual mutable values while reusable baseline values stay with definitions/archetypes;
- resolved/cache values are not copied back as alternate authority.

R2.2 consequence:

> Actor continuity should preserve progressive materialization and avoid creating a parallel “character profile” identity.

Interpretation: **BOUNDARY / NATURAL OWNER SIGNAL**.

---

### C02 — Current Actor schema has an open `details` object, but it is not a semantic decision

Source: `DEV/SCHEMAS/world-actor-state.schema.json`.

Actual claim:

- current machine schema contains `details: {type: object}`;
- no current typed cognition/relationship contract is defined there;
- schema existence does not establish semantic ownership for goals, plans, relationships or psychology.

R2.2 consequence:

> Do not treat `details` as permission to create an untyped Actor blob or as evidence that all cognition already belongs there.

Interpretation: **IMPLEMENTATION FACT / NOT ARCHITECTURE AUTHORITY**.

---

### C03 — `world.knowledge` already owns current proposition stance

Source: Step-4 canonical specification.

Actual claim:

- `(knower_id, fact_id)` current epistemic relation is owned by `world.knowledge`;
- initial stance semantics are `aware | known | believed | suspected | rejected`;
- full transition history belongs to LOG/SemanticEvents;
- Actor may propose `EpistemicDeltaDraft`, but validated owner transition commits the result.

R2.2 consequence:

> R2.2 must not create a second belief/suspicion store inside Actor continuity.

Interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C04 — Actor role already consumes goals, pressures, relationships and commitments

Source: Step-4 Actor role contract.

Actual claim:

Actor-eligible context may include relevant:

- identity/traits/values;
- goals/pressures;
- `world.knowledge`;
- observable scene facts;
- relationships/social position;
- resources/capabilities;
- commitments/recent known events.

R2.2 consequence:

> Goals/relationships/commitments are already real Context consumers, but their durable semantic ownership is not fully specified.

Interpretation: **NEW UNSATISFIED OWNER DELTA**.

---

### C05 — Actor cannot inherit DM truth/private plan unavailable to subject

Source: Step-4 canonical spec + single-context amendment.

Actual claim:

- Actor must reason from subject-local eligible cognition/evidence;
- physical co-presence of broader truth/private material does not make it eligible;
- public observable Actor-to-Actor transfer is distinct from private cognition inheritance.

R2.2 consequence:

> Actor continuity must be subject-owned/scoped and must not be reconstructable from global Story/DM preparation as current cognition merely because that material is available.

Interpretation: **BOUNDARY / NON-NEGOTIABLE**.

---

### C06 — R2.1 Story/continuity is not current Actor cognition

Source: R2.1 canonical specification.

Actual claim:

- Story may orient eligible gameplay roles;
- material decisions depending on current/source-specific correctness escalate to proper owners;
- source-bound does not mean current;
- entity continuity starts as a view;
- Actor current/private cognition requires proper owners in R2.2.

R2.2 consequence:

> Story/history can supply evidence or orientation for cognition assessment but cannot become the Actor's current mental state automatically.

Interpretation: **UPSTREAM BOUNDARY**.

---

### C07 — Current runtime doctrine already distinguishes stable and mutable NPC material

Source: `GAME/CORE/NPC.md`.

Actual claim:

Stable layer may include:

- core values;
- temperament;
- habitual style;
- long-term loyalties/aversions;
- important history;
- stable competencies/limitations.

Mutable layer may include:

- current goal;
- stress/fear/anger when material;
- recent experiences;
- current relationship stance;
- injuries/resources;
- new beliefs;
- active plans.

Changes should remain psychologically/causally traceable.

R2.2 consequence:

> Runtime behavior already requires the D10 distinction, but the architecture must narrow it into actual owners/lifecycles rather than copy the prose list wholesale.

Interpretation: **STRONG CURRENT CONSUMER EVIDENCE**.

---

### C08 — Current runtime rejects one universal relationship score

Source: `GAME/CORE/NPC.md`.

Actual claim:

- relationship should not be represented only by one universal scalar;
- examples of material dimensions include trust, affinity, fear, respect, obligation/debt, hostility and leverage;
- persist only dimensions that materially affect play;
- relationship changes require causal events rather than desired emotional beats.

R2.2 consequence:

> One scalar is already behaviorally inadequate, but the example dimension list is not yet a canonical schema/catalog.

Interpretation: **BEHAVIORAL REQUIREMENT / DIMENSION SET STILL OPEN**.

---

### C09 — Current runtime already uses sparse goals/plans and reconsideration trigger

Source: `GAME/CORE/NPC.md`.

Actual claim:

A significant NPC may have:

- long-term goal;
- current objective;
- next intended action;
- trigger/condition for reconsideration.

Off-screen action occurs when time/opportunity permits; every NPC is not continuously simulated.

R2.2 consequence:

> Goal/intention semantics have a real consumer. Continuous background cognition does not.

Interpretation: **STRONG CURRENT CONSUMER EVIDENCE**.

---

### C10 — Current runtime explicitly prevents assistant-style NPC cognition

Source: `GAME/CORE/AI_REASONING.md`.

Actual claim:

NPC behavior must be constrained by stable identity/values, goals/pressures, actual knowledge/beliefs, relationships/social position, resources/incentives/risk tolerance and recent events.

NPCs must not become unusually cooperative/explanatory/truth-revealing because the underlying model behaves like an assistant.

R2.2 consequence:

> Actor continuity is not decorative profile data; it is a correctness/quality input needed to prevent model-personality contamination.

Interpretation: **CURRENT BEHAVIORAL CONSUMER**.

---

### C11 — Objective truth and subjective understanding remain distinct

Sources: Step 4; `GAME/CORE/INFORMATION.md`.

Actual claim:

- character knowledge/belief can be incomplete, false or mutually incompatible;
- testimony/rumor/inference does not become objective truth merely because a character accepts it;
- later evidence updates character understanding without rewriting objective truth.

R2.2 consequence:

> Goals/intentions/relationships must be explicitly fictional-subject state; they cannot be used as objective-world truth without an independent owner/event.

Interpretation: **BOUNDARY**.

---

### C12 — Off-screen progression is causal and bounded

Source: `GAME/CORE/PROCESSES.md`.

Actual claim:

- active actors/processes advance only from cause/triggers/opportunity/time;
- dormant entities are not simulated every turn;
- temporal precision increases only when materially required.

R2.2 consequence:

> Sparse Actor cognition should reuse causal/event/time triggers and should not introduce its own always-on simulation scheduler.

Interpretation: **BOUNDARY / REUSE PRINCIPLE**.

---

### C13 — Player agency limits PC mental-state mutation

Sources: Step 4; `GAME/CORE/AI_REASONING.md`; `GAME/CORE/NARRATIVE.md`.

Actual claim:

The engine must not silently choose voluntary PC belief, suspicion, rejection, emotion, loyalty, interpretation, speech or decision merely because the model finds it plausible.

R2.2 consequence:

> NPC cognition machinery cannot be generalized to player-controlled PC voluntary mental state.

Interpretation: **PRODUCT LAW**.

---

## 2. Active research candidates

### D10 — Stable identity / mutable continuity / transient state

Research claim:

- biography, current emotion, long-term goal and temporary situation should not share one undifferentiated text blob;
- stable foundation changes only through explicit authority;
- durable evolving continuity changes more rarely from evidence;
- transient private state needs refresh/expiry;
- apply deep continuity only to Actors that need it.

Canonical reconciliation:

- progressive Actor materialization already exists;
- runtime NPC doctrine already distinguishes stable/mutable layers;
- no typed owner yet exists for the non-mechanical continuity delta.

R2.2 interpretation:

> **ACTIVE.** Preserve three lifetime semantics without requiring three independent stores.

---

### D11 — Truth / observation / knowledge / belief / suspicion / intention separation

Research claim:

- these are distinct entities and Actor-local state needs ownership/provenance;
- narrow typed model preferred over universal epistemic logic.

Canonical reconciliation:

- truth and `world.knowledge` stance separation is already Step-4 law;
- the unresolved delta is intention/plan and other Actor-private continuity, not another belief model.

R2.2 interpretation:

> **ACTIVE DELTA.** Preserve Step-4 epistemics; design only missing cognition classes.

---

### D12 — Directed relationships + player agency

Research claim:

- symmetric relationship state loses asymmetric feeling/trust/debt;
- `A -> B` and `B -> A` must be independent;
- NPC subsystem changes only its own relation view;
- player-owned mental/consent state is not inferred automatically;
- avoid universal social graph/over-numeric scoring.

R2.2 interpretation:

> **ACTIVE.** Directionality is strongly supported; storage shape and minimum facet vocabulary remain open.

---

### D13 — Sparse/event-driven cognition

Research claim:

- cognition runs for bounded focus Actors after material evidence/trigger;
- useful modes include react, update-belief, reflect, plan, reconsider;
- `NO_CHANGE` is legal;
- always-on multi-NPC simulation is rejected.

Canonical reconciliation:

- update-belief itself remains Step-4 `world.knowledge` mutation;
- other modes may assess Actor-local continuity;
- current runtime already bounds active cast/off-screen progression.

R2.2 interpretation:

> **ACTIVE, NARROWED.** Modes are assessment purposes, not separate persistent state machines.

---

### S07 — Explicit cognition modes

Research qualifier:

- one generic “think as NPC” operation mixes distinct tasks;
- risk is orchestration branching;
- original revisit: after basic Actor continuity.

Program disposition activated S07 for R2.2 because R2.2 is exactly the basic Actor-continuity stage.

R2.2 interpretation:

> Consider a small closed assessment-purpose vocabulary, not a new orchestration framework.

---

### S10 — `NO_CHANGE` is successful outcome

Research claim:

- cognition assessment may legitimately produce no mutation;
- forced changes create artificial character drift.

R2.2 interpretation:

> `NO_CHANGE` should produce no semantic write merely to prove assessment occurred. Optional diagnostics/history are separate concerns.

---

### S11 — Transient private-state expiry

Research claim:

- temporary emotion/tension/short goal should expire without refresh;
- turn-count TTL may not correspond to fictional time.

R2.2 interpretation:

> Transient state should be ephemeral by default; durable transient state needs explicit event/time invalidation only when future correctness/continuity requires survival.

---

### D09 — Evidence-bound durable mutation

Research claim:

- bounded evidence -> proposed mutation/NO_CHANGE -> deterministic identity/current-revision/shape validation -> commit;
- validator validates structure better than meaning.

Canonical reconciliation:

- generic proposer/commit boundary already exists;
- Actor cognition is fictional judgment and cannot be made fully deterministic by schema validation.

R2.2 interpretation:

> Apply the inherited boundary to Actor-local state: bounded eligible source basis and target/current-revision checks are mandatory; semantic judgment remains bounded nondeterminism rather than objective truth.

---

### S27 — One durable mutation per assessment

Research qualifier:

- can bound drift but may create update backlog.

R2.1 already rejected it as a generic projection rule.

R2.2 interpretation:

> Do not require one field/record mutation. Prefer **one bounded Actor + one assessment-purpose delta**, which may update a small coherent set of mutually dependent Actor-local fields if evidence justifies them.

This remains a candidate, not yet accepted.

---

## 3. Negative / adversarial evidence

### N01 — Biography / psychology blob

Failure mode:

- stable traits, current emotions, goals and history live in one prose field;
- transient detail becomes permanent and updates overwrite stable identity.

Guardrail candidate:

> Admit explicit lifetime semantics; do not use `world.actor.details` as untyped universal cognition authority.

---

### N02 — Duplicate epistemics

Failure mode:

- Actor profile stores beliefs/suspicions already owned by `world.knowledge`.

Guardrail candidate:

> Proposition stance remains exclusively in `world.knowledge`; Actor continuity may reference it but not copy it as writable state.

---

### N03 — Symmetric relationship

Failure mode:

- one relation object/score silently represents both directions.

Guardrail candidate:

> Actor-local relationship view is directed; B's view is independent.

---

### N04 — Universal relationship scalar

Failure mode:

- one number cannot distinguish trust, fear, affection, respect or felt obligation.

Guardrail candidate:

> If durable relationship facets are admitted, keep them sparse and typed; do not compress all material relationship semantics into one score.

---

### N05 — Dimension explosion / false precision

Failure mode:

- dozens of numeric psychology/social axes create a simulation ontology without gameplay consumer need.

Guardrail candidate:

> Admit the smallest facet vocabulary justified by actual Actor decision consumers; qualitative/sparse representation is preferred over false numeric precision unless mechanics require numbers.

---

### N06 — Every thought retained

Failure mode:

- model deliberation becomes durable biography/history.

Guardrail candidate:

> Persist only material current cognition that must affect future play; hidden chain-of-thought/private reasoning text is not Actor state.

---

### N07 — Forced mutation

Failure mode:

- every assessment changes personality/goal/relationship simply because a cognition call ran.

Guardrail candidate:

> `NO_CHANGE` is normal and creates no semantic write.

---

### N08 — Story/evidence laundering

Failure mode:

- historical/derived prose is treated as proof that Actor currently believes/wants something.

Guardrail candidate:

> Durable cognition updates require eligible evidence/current Actor source basis; Story may orient but not establish current cognition automatically.

---

### N09 — Permanent transient emotion

Failure mode:

- fear/anger/current short objective survives indefinitely because nothing clears it.

Guardrail candidate:

> Transient state is non-durable by default; if persisted, it carries explicit event/time invalidation semantics appropriate to fiction.

---

### N10 — Always-on cognition

Failure mode:

- every NPC rethinks every turn, causing cost, noise and uncaused character drift.

Guardrail candidate:

> Sparse material triggers/focus Actors only; no per-turn/background correctness loop.

---

### N11 — PC mind takeover

Failure mode:

- NPC cognition machinery is reused to infer/persist a PC's voluntary belief/emotion/goal.

Guardrail candidate:

> Player-authored mental/consent/goal state remains player/rules-owned; no implicit Actor-assessment mutation.

---

## 4. Ownership analysis

### 4.1 Strong natural-owner signal: source Actor

The evidence favors making current Actor-private continuity semantically **owned by the source Actor identity** rather than introducing a global cognition authority.

Reasons:

- state answers “what does Actor A currently want/intend/feel toward B?”;
- directionality is naturally `A -> target`;
- Actor progressive materialization already bounds detail;
- current Actor record already owns other individual mutable state;
- R2.3 can build derived indexes/views without moving writable authority.

This does **not** yet decide exact physical field layout.

### 4.2 Relationship owner candidate

A directed relation `A -> B` can be represented semantically as part of A's Actor-private state even if a later machine layout chooses a separate record for cardinality/performance.

Important distinction:

> **semantic owner = source Actor A** does not necessarily require **physical storage = same JSON file**.

Therefore architecture can decide semantic ownership now and defer physical normalization to R2.7 unless independent lifecycle/concurrency requirements force a separate owner earlier.

### 4.3 Objective social facts remain elsewhere

Actor-local relationship/cognition must not steal objective facts such as:

- organization membership/allegiance when independently canonical;
- contractual/legal debt or promise occurrence where another world owner exists;
- physical possession/location;
- actual event occurrence;
- another Actor's cognition.

Actor A may have a **felt obligation**, belief or intention about an objective relation; that subjective state remains distinct from the objective relation itself.

---

## 5. Emerging state taxonomy

Current evidence supports testing a minimal three-lifetime model without three separate stores:

```text
FOUNDATION
    stable identity/values/temperament/long-lived commitments
    changes only through explicit material authority/event

DURABLE EVOLVING COGNITION
    current goals/objectives
    current intentions/active plans
    material directed relationship facets
    other current Actor-private state proven necessary
    evidence/currentness-bound updates

TRANSIENT PRIVATE STATE
    short-lived affect/attention/urgency/local intention
    ephemeral by default
    persist only when it must survive interruption and has explicit invalidation
```

`world.knowledge` remains separate proposition stance and is not copied into this taxonomy.

---

## 6. Emerging relationship model

Evidence strongly rejects:

- symmetric relation authority;
- one universal scalar;
- large numeric psychological ontology.

Credible minimal direction:

```text
source_actor -> target_subject
    sparse material relationship facets
```

Potential facet families from current consumers:

- trust;
- affinity;
- fear;
- respect;
- hostility;
- felt obligation.

`leverage` is not yet clearly a pure relationship facet: it may instead be knowledge/resource/objective-world state. It should not be adopted without a clearer semantic consumer.

The exact facet vocabulary/value scale remains a Decision Brief question.

---

## 7. Emerging cognition-assessment model

A small assessment-purpose vocabulary appears justified:

```text
REACT
    choose immediate Actor response/action from current eligible state

UPDATE_EPISTEMIC
    Step-4 world.knowledge proposal path

RECONSIDER_GOAL
    assess goal/objective change after material evidence/pressure

PLAN
    assess current intention/next plan where future continuity requires it

REFLECT
    not yet proven as separate persistent-state operation;
    may be omitted or folded into goal/relation assessment
```

The vocabulary should describe **purpose of bounded assessment**, not persistent state-machine phases.

`NO_CHANGE` is legal for every assessment that permits mutation.

---

## 8. Emerging mutation boundary

Credible narrow form:

```text
one source Actor
+ one assessment purpose
+ bounded eligible evidence/current state
    -> ActorCognitionDelta | EpistemicDeltaDraft | NO_CHANGE
    -> deterministic identity/current-revision/source/shape validation
    -> native-owner mutation if accepted
    -> SemanticEvent/history evidence where materially required
```

A single bounded Actor delta may update a small coherent set of mutually dependent fields. It is not an arbitrary whole-Actor rewrite.

This preserves the useful boundedness of S27 without artificial one-field update backlog.

---

## 9. Open architectural decisions after extraction

The evidence leaves three material design choices for the R2.2 Decision Brief:

1. **Semantic owner/layout boundary:** source-Actor-owned sparse continuity versus separate cognition/relation semantic owners versus minimal persistence.
2. **Minimum relationship representation:** which sparse facets/value semantics are actually baseline-worthy without false precision.
3. **Transient persistence rule:** ephemeral-by-default with explicit persistence trigger/invalidation versus durable transient entries with generic TTL machinery.

Current evidence favors:

- source-Actor semantic ownership;
- sparse directed relation facets rather than a separate global relation authority;
- ephemeral transient cognition by default;
- event/time invalidation only when transient state must survive interruption;
- no generic TTL scheduler;
- no universal psychology model.

These are recommendations-in-formation, not accepted architecture.
