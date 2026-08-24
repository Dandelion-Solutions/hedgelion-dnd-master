# R2.2 Task Brief — Actor Continuity, Cognition and Directed Relationships

Status: **ACTIVE TASK BRIEF — R2.2 IN PROGRESS**

Date: 2026-08-24

Roadmap authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Upstream canonical dependency:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`

Program evidence disposition:

- `DEV/docs/superpowers/research/2026-08-24-round-2-evidence-disposition-ledger.md`

---

## 1. Task classification

**Architectural / deep-work task.**

R2.2 defines the semantic ownership and lifecycle of Actor-local continuity that is not already owned by mechanical Actor state or Step-4 `world.knowledge`.

Its output becomes an upstream source contract for R2.3 Context Runtime.

No implementation is authorized.

---

## 2. Problem statement

HDM already defines:

- one progressively materialized `world.actor` mechanical/world identity;
- natural current mechanical/state ownership;
- `world.knowledge` as current subject-to-proposition epistemic authority;
- Actor logical role eligibility including identity/traits/values, goals/pressures, knowledge, observable facts, relationships, resources and commitments;
- Actor-generated cognition changes as non-authoritative proposals until validated/committed;
- player-agency restrictions on voluntary PC belief/emotion/interpretation;
- runtime doctrine for persistent NPC identity, goals, relationships, plans and bounded off-screen action.

What remains unresolved is the **canonical semantic model** for non-mechanical Actor continuity beyond proposition stance:

```text
stable identity / values
mutable goals / intentions / commitments
private plans
relationship state
transient affect/pressure where material
other bounded fictional cognition
```

R2.2 must decide which of these actually require durable typed ownership, which remain transient/derived, and how updates occur without creating a universal psychology database or duplicating `world.knowledge`.

---

## 3. Primary active research inputs

Current Round-2 disposition marks these as active for R2.2:

- D10 — stable foundation vs durable evolving continuity vs transient Actor state;
- D11-delta — distinguish truth/observation/knowledge/belief/suspicion/intention without reopening Step-4 epistemics;
- D12-delta — directed relationship state with player-agency protection;
- D13 — sparse/event-driven cognition and valid `NO_CHANGE`;
- S07 — explicit cognition modes rather than one generic Actor-think operation;
- S10 — `NO_CHANGE` as successful semantic assessment;
- S11 — transient private Actor state needs expiry/refresh semantics tied to appropriate fictional time.

Specialized candidates to reconsider only where R2.2 has a concrete consumer:

- D09 — evidence-bound durable mutation;
- S27 — possible one-assessment/one-bounded-mutation pattern.

Inherited/dormant research remains non-work unless its trigger becomes true.

---

## 4. Primary decision questions

### 4.1 Actor state taxonomy

Determine the minimum semantic classes required among:

- stable foundation/identity/values;
- durable evolving goals/objectives;
- intentions/commitments/promises;
- private plans;
- directed relationship state;
- transient stress/fear/anger/attention/urgency or equivalent short-lived cognition;
- proposition stance already owned by `world.knowledge`;
- ordinary current world/mechanical state already owned elsewhere.

Reject redundant classes.

### 4.2 Ownership geometry

For every admitted Actor-local class decide:

- natural semantic owner;
- whether it belongs inside `world.actor`, a separate relation/record, an existing owner, or no durable storage at all;
- durable vs transient;
- source/provenance requirements;
- whether history is event evidence rather than copied current state;
- whether a derived index/view is sufficient instead of a new authority.

Do not infer architecture merely from the current broad `world.actor.details` schema field.

### 4.3 `world.knowledge` boundary

Preserve Step-4 ownership for proposition stance:

```text
aware / known / believed / suspected / rejected
```

R2.2 must decide how intentions/goals/plans/relationships differ semantically from proposition stance and must not duplicate beliefs/suspicions in another Actor memory field.

### 4.4 Goals, intentions, commitments and plans

Decide which distinctions are materially useful and which can remain one simpler model.

Questions include:

- long-term goal versus current objective;
- intended next action versus private plan;
- promise/commitment as Actor cognition versus canonical social/world relation;
- reconsideration triggers;
- when a proposed intention becomes durable enough to matter to future behavior;
- when an abandoned plan can disappear without historical deletion.

### 4.5 Directed relationships

Determine whether material relationship state is modeled as directed `A -> B` Actor-local cognition/stance and which minimum dimensions, if any, deserve typed persistence.

Candidate dimensions from current runtime doctrine include trust, affinity, fear, respect, obligation/debt, hostility and leverage, but R2.2 must not adopt a catalog merely because examples exist.

Decide:

- one scalar vs sparse dimensions vs typed qualitative stance;
- source/evidence requirements;
- asymmetry;
- relation to organization membership/allegiance/current world facts;
- relation to player/PC agency;
- history/provenance without a relationship event-log duplicate.

### 4.6 Sparse/event-driven cognition

Define when Actor cognition assessment is warranted.

Default direction to challenge:

```text
material new evidence / pressure / commitment / elapsed-fiction trigger
    -> bounded Actor assessment
    -> NO_CHANGE or bounded proposal
```

Do not simulate every NPC every turn or create cognition records merely because a turn occurred.

### 4.7 Mutation validation

For any durable Actor-local cognition mutation evaluate:

```text
bounded eligible evidence
    -> Actor/cognition proposal
    -> deterministic source/current-owner/shape validation
    -> admitted state mutation + history evidence where material
```

Determine what semantic conditions can be structurally validated and what remains non-deterministic fictional judgment under bounded authority.

### 4.8 Transient state and fictional time

Decide whether short-lived Actor state needs explicit expiry/refresh semantics and which clock owns expiration.

Do not use arbitrary turn-count TTL when fictional elapsed time or event triggers are the actual cause.

Do not introduce a generic scheduler if existing temporal/process machinery or simple event-driven refresh is sufficient.

### 4.9 Actor depth / materialization

Preserve progressive materialization:

- incidental Actors stay sparse;
- supporting/significant Actors acquire only continuity that future play needs;
- deep cognition remains bounded to active/relevant Actors;
- absence of a cognition record must have explicit semantics and must not force speculative filling.

### 4.10 PC agency boundary

R2.2 must explicitly distinguish NPC/faction Actor cognition from player-controlled PCs.

The engine SHALL NOT silently choose voluntary PC:

- belief;
- suspicion/rejection;
- emotion;
- loyalty;
- interpretation;
- private plan/goal where player agency owns it;

unless an explicit rules/world mechanism legitimately constrains cognition.

---

## 5. Explicit non-goals

R2.2 does **not** design:

- generic continuity/history projection — closed by R2.1;
- context retrieval/ranking/token budgets — R2.3;
- single-context role sequencing/instruction machinery — R2.4;
- multiplayer collaboration protocol — R2.5;
- final host evaluation/security envelope — R2.6;
- concrete schema/catalog migrations/runtime implementation — R2.7 mapping and later implementation planning;
- universal psychological simulation;
- every-NPC background thinking loop;
- personality trait ontology;
- generic social graph/knowledge graph;
- authored character-arc progression system unless a dormant trigger becomes real.

---

## 6. Inherited constraints

R2.2 must preserve:

- one mutable semantic owner per concern;
- `world.actor` current mechanical/world identity semantics;
- `world.knowledge` as current proposition-stance owner;
- objective truth / fictional knowledge / human disclosure separation;
- R2.1 continuity/Story is orientation/history, not current Actor cognition;
- Story mention does not automatically establish Actor belief, goal or relationship;
- material role decisions depending on current/source-specific claims must obtain proper-source evidence;
- Actor LLM output is proposal, not authority;
- current world/mechanical facts remain deterministic-owner facts;
- player agency boundaries;
- recovery cannot depend on hidden chain-of-thought/model memory;
- no per-turn/background cognition worker correctness dependency.

---

## 7. Source Manifest

### 7.1 Process / sequencing

| Source | Role | Inspection purpose |
|---|---|---|
| `AGENTS.md` | governance | evidence/transport/documentation rules |
| `DEV/DESIGN_PROCESS.md` | canonical process | Source Manifest, decision/synthesis/completeness gates |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | Round-1 preservation and item-level research handling |
| `DEV/PROJECT_MAP.md` | derivative locator | Actor/LLM/runtime/schema/test dependency subgraph |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing authority | R2.2 scope/exit/downstream boundary |
| R2.1 canonical spec + resolution gate | upstream canonical | continuity/history/Story boundary handed to Actor state |

### 7.2 Canonical / owning architecture

| Source | Why required |
|---|---|
| `DEV/ARCHITECTURE/ACTOR_MODEL.md` | current `world.actor` identity/materialization/mechanical ownership |
| `DEV/SCHEMAS/world-actor-state.schema.json` | current machine realization; exposes existing fields but does not decide new semantics |
| Step-3 deterministic execution canonical spec | inherited proposal/validation/commit boundary |
| Step-4 truth/knowledge/role-context/Story canonical spec | `world.knowledge`, Actor role contract, PC agency, relationship/goal context eligibility |
| Step-4 single-context role-containment amendment | current logical-role containment and Actor-to-Actor transfer boundary |
| relevant Step-5 history/chronology specs as needed | provenance/history/fictional-time dependencies without duplicate history ownership |

### 7.3 Runtime semantic neighbors

| Source | Why required |
|---|---|
| `GAME/CORE/NPC.md` | current runtime doctrine for layered personality, relationships, goals/plans, sparse NPC depth |
| `GAME/CORE/AI_REASONING.md` | Actor-vs-assistant behavior, evidence/agency/knowledge discipline |
| `GAME/CORE/INFORMATION.md` | truth/knowledge/belief/testimony distinctions |
| `GAME/CORE/PROCESSES.md` | off-screen actors/processes and causal/fictive-time advancement |
| `GAME/CORE/NARRATIVE.md` | player agency and world/NPC initiative boundary where relevant |

Inspect additional campaign schemas/catalog contracts/tests only when a proposed semantic owner would overlap or contradict them.

### 7.4 Research input

Primary Dossier items:

- D10, D11, D12, D13;
- S07, S10, S11;
- D09/S27 specialized mutation question.

Relevant negative/reserve evidence must include at least failure modes around:

- symmetric relationship scores;
- all-NPC cognition every turn;
- every thought persisted;
- assistant/helpfulness leaking into NPC behavior;
- hidden DM truth entering Actor cognition;
- generated cognition becoming canon without evidence;
- player-character autonomy being overwritten.

---

## 8. Required R2.2 evidence ledger

Before a Decision Brief, create an inspectable R2.2 ledger containing for every material source/finding:

```text
Source/item
Actual claim
Authority/classification
Qualifier/applicability
Existing owner
Conflict / extension / new consumer / no delta
Candidate disposition
Reason
Downstream R2.3 source consequence
```

For current runtime doctrine, distinguish desirable behavior from already-canonical storage/authority semantics.

For research findings, preserve applicability and revisit conditions rather than promoting examples into mandatory schema.

---

## 9. Required analytical challenges

At minimum attack candidate designs for:

1. **Duplicate epistemics** — belief/suspicion copied outside `world.knowledge`.
2. **Actor blob** — `world.actor.details` becomes an untyped universal psychology store.
3. **Relationship symmetry** — A's view of B silently forces B's view of A.
4. **Scalar overfitting** — one relationship score cannot represent materially different fear/trust/obligation states.
5. **Dimension explosion** — typed relationship dimensions become a universal social ontology without consumer need.
6. **Thought logging** — every internal thought becomes durable state/history.
7. **No-change bureaucracy** — cognition assessment creates writes merely to record that nothing changed.
8. **Evidence laundering** — Story/model speculation becomes durable Actor cognition without an eligible causal basis.
9. **Temporal drift** — transient emotions/plans never expire or use turn count unrelated to fictional time.
10. **Background simulation cost** — every NPC is reconsidered every turn.
11. **Player agency** — PC beliefs/emotions/goals are inferred and persisted without player/rules authority.
12. **Current/history confusion** — an old Actor plan/event is treated as current intention.
13. **Recovery** — Actor continuity depends on hidden prior-chat reasoning rather than durable owners/evidence.
14. **R2.3 leakage** — R2.2 starts designing ranking/token context algorithms instead of source semantics.

---

## 10. Alternatives requirement

The Decision Brief must compare at least credible forms of:

### A. Actor-embedded sparse cognition

Store admitted durable Actor-local cognition directly in `world.actor` under a narrow typed structure, with separate relation representation only where identity/cardinality requires it.

### B. Separate typed Actor-cognition / relationship owners

Keep mechanical Actor state narrower and create explicit cognition/relation records keyed by Actor/target/concern.

### C. Minimal persistent cognition

Persist only `world.knowledge` plus a very small goal/commitment surface; synthesize most plans/relationships transiently from history/context.

A hybrid may be recommended, but the analysis must justify every durable class by a real consumer and ownership need.

---

## 11. Exit criteria

R2.2 may close only when canonical design defines:

- admitted Actor continuity classes and rejected alternatives;
- stable vs durable evolving vs transient semantics;
- exact boundary with `world.knowledge` and mechanical `world.actor` state;
- ownership/cardinality for goals/plans/commitments/relationships where admitted;
- directed relationship semantics and minimum dimensions/representation;
- evidence/provenance/currentness rules for durable mutation;
- `NO_CHANGE` semantics without mandatory writes;
- sparse/event-driven activation and Actor-depth/materialization policy;
- transient expiry/refresh semantics;
- PC agency restrictions;
- recovery/history behavior without hidden model memory;
- explicit R2.3 source/eligibility handoff;
- no duplicate semantic authority;
- adversarial review closure;
- unresolved work explicitly owned/deferred/dormant/debt.

---

## 12. Current continuation point

```text
R2.2 status: IN PROGRESS
task brief: established
next activity: source extraction / R2.2 evidence ledger
broad implementation: BLOCKED
```
