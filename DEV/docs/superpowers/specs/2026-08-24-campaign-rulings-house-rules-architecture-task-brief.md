# Campaign Rulings & House Rules Architecture — Task Brief

Status: **STEP 1 COMPLETE / STEP 2 RESEARCH NEXT / SOLUTION-BLIND**

Date: 2026-08-24

Target branch: `v1/engine-rearchitecture`

Repository recovery base HEAD:

```text
3674404a67589a2384cc8201a0d2d28e4057e91b
```

Governing process:

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Current sequencing authority:

- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

Durable handoff/status:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

Design input under review:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

No GAME/schema/runtime implementation is authorized by this step.

---

# 1. Classification

**Architectural / cross-cutting.**

The work defines a semantic and authority boundary spanning campaign policy, LLM adjudication, deterministic mechanics, persistence, retrieval, traceability and ruleset/catalog ownership. A wrong abstraction could create a second mechanics authority, over-formalize fiction-dependent judgment, or make durable campaign precedent undiscoverable/inconsistent.

The full eight-step deep-design loop is therefore mandatory.

---

# 2. One-sentence mission

Design the minimum coherent architecture by which HDM can make, preserve, discover, apply, supersede and trace campaign-specific rulings and deliberate house rules — including genuinely fiction-dependent LLM judgment — while preserving deterministic mechanical authority, bounded ordinary-turn latency, campaign ownership and historical consistency.

---

# 3. Problem statement

Current accepted HDM policy already requires local live adjudication, gives campaign house rules and established campaign rulings precedence, requires materially reusable precedent to be preserved, and forbids narration/LLM judgment from replacing required RNG, validation or engine-owned state mutation.

What is missing is one accepted architecture for the lifecycle and interaction of those responsibilities.

The investigation must determine, rather than assume:

- which distinct semantic kinds of ruling/policy actually need architecture-level identity;
- what is ephemeral versus durable and at what durability boundary;
- what belongs to LLM-readable campaign policy versus typed mechanics;
- how fiction-dependent judgment reaches deterministic execution through bounded legal interfaces;
- how applicable durable policy is discovered without an ordinary-turn repository/corpus scan;
- how precedence, conflict, correction and supersession work;
- what trace/provenance is required without storing chain-of-thought;
- whether existing files/owners suffice or a new owner/structure is justified.

---

# 4. Step-1 framing challenge — binding corrections to the input brief

The design brief is an input, not a candidate specification. Step 2 must remain able to invalidate its terminology, decomposition and proposed physical surfaces.

## 4.1 Sequencing correction

The design brief's Section 13 statement that independent S6D work may start before House Rules closes is stale and superseded.

Binding sequence:

```text
R2.7 WP-06 PAUSED
    -> House Rules Steps 1..8
    -> House Rules canonicalization
    -> S6D, one full eight-step cycle per numbered task/domain
    -> S6D integrated closure
    -> R2.7 WP-06 resume
```

Therefore:

- do not resume WP-06 during this cycle;
- do not execute or begin any S6D task before House Rules Step 8;
- S6D artifacts may be inspected only as downstream consumer/dependency evidence when needed to define the House Rules mechanical boundary.

## 4.2 Do not embed the proposed "two-channel architecture" as fact

The proposed formalized-mechanics vs bounded-LLM-adjudication split is a useful hypothesis, not the answer.

Research must test whether the problem is better described by independent axes such as:

```text
representation/execution form
    deterministic typed | adjudicative prose | hybrid

lifecycle/durability
    one-off | temporary | campaign precedent | deliberate house rule

authority/ownership
    framework/ruleset | campaign policy | engine-owned mechanical state
```

A sound result may keep two execution paths while rejecting a permanent two-class taxonomy for durable policy objects.

## 4.3 Do not assume `HOUSE_RULES.md` owns every durable ruling

The current `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` contract says it stores explicit campaign decisions that differ from Framework/base rules. Current `PLAY_POLICY.md` separately speaks of both campaign house rules and established campaign rulings.

Therefore Step 2 must research whether:

- one file can legitimately own both concepts after an explicit contract change;
- campaign precedents need a separate surface/family;
- the distinction is semantic but not physical;
- some durable rulings belong in existing campaign/canon structures instead.

Do not decide the filename/shape in Step 1.

## 4.4 Do not assume a new `GAME/CORE/RULINGS.md`

A new CORE owner is only one candidate. Existing `PLAY_POLICY.md`, `ADJUDICATION.md`, `MECHANICS_INTEGRITY.md`, rules-routing owners or another existing owner may be sufficient after amendment/delegation.

The investigation must prefer reuse if responsibility can be made unambiguous without creating duplicate authority.

## 4.5 Do not assume a generic executable `ruling` record or DSL

No generic ruling interpreter, scripting language, arbitrary expression engine, query mechanism or direct prose-to-state mutation path is authorized.

If structured durable metadata or machine indexes are proposed, each field and machine representation must be justified by current routing, scope, supersession, trace, recovery or validation needs.

## 4.6 Stable IDs are a requirement candidate, not an axiom

Durable identity may be useful for reference, supersession and trace, but Step 2 must establish what actually requires stable identity and at what granularity. Markdown anchors, structured records, typed mechanic references or another representation remain alternatives.

## 4.7 Examples in the design brief are illustrative only

Names such as `fiction.target_reachable`, `invocation-adjudicated fact`, a typed `IMPOSSIBLE` outcome, or a particular parameter carrier must not be treated as existing canonical schemas/types merely because they appear in examples.

Step 2 must inspect the actual invocation/execution/input contracts before proposing receiving surfaces.

## 4.8 Recurrence does not automatically imply formalization

A recurring policy should be formalized only when typed representation is semantically faithful and materially improves correctness, validation, accounting, repeatability or latency. Rich fiction/context dependence may make deliberate LLM interpretation the correct durable representation.

The inverse must also be challenged: prose persistence must not become an excuse to leave closed deterministic mechanics outside canonical typed machinery.

## 4.9 Temporary-ruling durability is underspecified

"Temporary" may mean current adjudication only, encounter/session-local policy, unresolved short-horizon campaign policy, or durable policy with an expiry/revisit condition. Those have different persistence/recovery implications.

Step 2 must define the semantic distinction before choosing storage.

## 4.10 Retrieval is part of correctness

A durable precedent that exists but is not discoverable when applicable cannot guarantee consistency.

The architecture must explain how relevant campaign policy enters the bounded working set while preserving the accepted rule that campaign data remains lazily/targetedly retrieved and ordinary turns do not gain full-corpus scans, GitHub round-trips or extra LLM passes without a concrete trigger.

---

# 5. In scope

Step 2 and the subsequent House Rules cycle SHALL cover:

1. semantic taxonomy/lifecycle of one-off adjudication, temporary ruling, reusable campaign precedent and deliberate house rule, while allowing evidence to merge/split/rename these categories;
2. authority and precedence relative to Framework/ruleset mechanics, exact stored character/entity mechanics and engine-owned state;
3. formalized, adjudicative and hybrid representations where each is justified;
4. the legal LLM -> typed/deterministic receiving boundary for mechanically consequential judgments;
5. durable identity, scope/applicability, status, correction/supersession and provenance only to the degree required;
6. discovery/routing/loading of applicable campaign policy;
7. persistence and recovery semantics for durable/temporary policy;
8. historical non-retroactivity and explicit correction/repair boundaries;
9. traceability/audit basis without chain-of-thought persistence;
10. interaction with existing Activity, Rule Element, catalog/ruleset and adjudication owners;
11. exact responsibilities of `HOUSE_RULES.md` and whether another physical campaign/CORE surface is necessary;
12. the contract that later S6D must consume, without starting S6D itself.

---

# 6. Explicit non-goals

This House Rules cycle does not:

- resume or complete R2.7 WP-06;
- start any S6D numbered task/domain;
- close residual selector/seed/package/catalog coverage;
- invent concrete S6D machine types merely to satisfy examples in the design brief;
- redesign the whole Context Runtime, role topology, Story system, persistence stack or catalog architecture;
- choose model/provider/API/Work deployment topology;
- perform external RAW research for ordinary D&D rules unless a specific architecture question demonstrably requires it;
- build a generic policy language, generic expression interpreter, arbitrary script hook or second mechanics engine;
- persist hidden reasoning/chain-of-thought;
- define migration compatibility for nonexistent current user campaigns beyond already accepted clean-slate constraints;
- implement GAME/schema/runtime changes before the later approval/implementation gates.

Neighboring systems may be inspected as consumers or invariant owners without reopening their closed architecture absent contradictory evidence or a genuinely new consumer requirement.

---

# 7. Fixed constraints and architecture invariants

The solution must preserve at least:

1. **Deterministic mechanical authority.** Required RNG, math, validation, resource accounting and engine-owned mutation remain in canonical deterministic owners.
2. **LLM judgment is bounded.** An LLM may decide an eligible fiction-dependent fact/classification/parameter/policy application, but cannot directly fabricate RNG, HP/resources/capability or canonical mutation.
3. **No parallel mechanics authority.** Formalized house mechanics must reuse canonical catalog/ruleset/Activity/Rule-Element execution/validation surfaces rather than a second interpreter.
4. **Campaign ownership.** Campaign-specific policy must not silently same-ID override shipped definitions or masquerade as a global ruleset replacement.
5. **Local-first gameplay.** External RAW/web research is not an automatic dependency of live adjudication.
6. **Bounded latency/retrieval.** Normal play remains local/bounded from the current working set; no default repository/web/full-corpus scan or extra LLM pass.
7. **Consistency.** Material reusable precedent must be representable/discoverable strongly enough to constrain analogous future cases.
8. **Historical stability.** Later policy change does not silently rewrite accepted historical outcomes; repair/correction is explicit.
9. **Minimal auditable basis.** Persist identifiers/accepted inputs/source references where needed, not hidden deliberation.
10. **YAGNI/reuse-first.** New owners, registries, schemas, indexes and record families require a demonstrated current responsibility.
11. **Clean-slate current scaffold.** No current user campaign requires backward-compatible migration; future released-campaign evolution remains a later R2.7 responsibility.
12. **House Rules before S6D.** Step 8 canonicalization is the S6D start gate.

---

# 8. Quality attributes that may distinguish alternatives

Evaluate alternatives against:

- authority correctness / mechanical honesty;
- semantic fidelity for rich fiction-dependent judgment;
- deterministic reproducibility of mechanical consequences once adjudication inputs are accepted;
- consistency across analogous future cases;
- ordinary-turn latency and bounded retrieval cost;
- durability/recovery where policy is intended to survive;
- traceability/debuggability without chain-of-thought;
- correction/supersession clarity;
- discoverability/routing at campaign scale;
- simplicity/YAGNI and number of new authorities;
- compatibility with existing catalog/Activity/Rule Element contracts;
- testability of authority violations and policy application;
- extensibility without turning campaign Markdown into an executable DSL.

Do not invent numeric latency or scale targets unless an owning source establishes them.

---

# 9. Initial Source Manifest / discovery route for Step 2

Owning sources beat this Task Brief and the earlier design brief where they conflict.

## 9.1 Governance, sequencing and durable state

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`
- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

## 9.2 Existing gameplay/adjudication/rules authorities

Inspect at minimum:

- `GAME/CORE/PLAY_POLICY.md`
- `GAME/CORE/ADJUDICATION.md`
- `GAME/CORE/MECHANICS_INTEGRITY.md`
- `GAME/RULES/README.md`
- `GAME/RULES/INDEX.md`
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

Follow their explicit delegation/consumer links to any additional owning CORE/rules sources implicated by ruling applicability, intent mapping, state ownership, persistence or campaign retrieval.

## 9.3 Formal mechanics owners

Inspect at minimum:

- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`

Then use `CANONICAL_ARCHITECTURE_INDEX.md`, project routing and concrete identifier/catalog searches to locate the accepted owners for:

- ruleset/package/catalog composition and identity;
- campaign-added definitions / same-ID override prohibition;
- Activity parameters/targets/predicates/costs/results;
- Rule Element composition;
- invocation/trigger/input facts if they are real current concepts;
- provenance/trace surfaces used by deterministic execution.

Do not infer these contracts from the design brief's examples.

## 9.4 Persistence, retrieval and recovery consumers

Follow project routing to the accepted owners for:

- campaign branch/root layout and current campaign RULES materialization;
- campaign lazy retrieval / Context Runtime assembly;
- save/durability boundaries;
- recovery/currentness/index behavior;
- audit/trace/history boundaries relevant to applied rulings.

Inspect only the dependency subgraph implicated by the proposed semantics; do not reopen unrelated persistence architecture.

## 9.5 Downstream consumers — inspect, do not execute

- current R2.7 WP-06 durable status/forward obligations where House Rules changes its eventual audit surface;
- S6D owner/task/plan only to enumerate the mechanical-boundary inputs it expects from House Rules;
- current schemas/catalog/tests only where they expose real receiving interfaces or prove a proposed type does not exist.

S6D remains blocked.

## 9.6 External evidence

Presumption: **no external web research is required to settle the internal HDM ownership model.**

Use external primary/official technical evidence only if Step 2 discovers a material question that cannot be answered from current project authorities and whose answer can change the architecture. Do not browse merely to collect generic rule-engine or RPG design patterns.

---

# 10. Required Step-2 research questions

The Research & Architecture Draft must answer, with source-backed evidence:

1. What semantic distinction is actually required between situational adjudication, temporary ruling, campaign precedent and deliberate house rule?
2. Are those categories a lifecycle, orthogonal attributes, distinct record kinds, or merely policy states?
3. What current owner establishes precedence, and what precedence/conflict model is missing?
4. Which decisions must become durable, and what makes durability necessary?
5. What does "temporary" mean across turn/session/recovery boundaries?
6. What minimum identity/scope/status/supersession metadata is required, if any?
7. Can existing `HOUSE_RULES.md` legitimately absorb established precedents, or would that contradict its current responsibility?
8. Is a new CORE owner necessary, or can existing owners be amended/delegated cleanly?
9. How is an applicable durable policy discovered and loaded without scanning all campaign policy on ordinary turns?
10. Which LLM outputs may legally become typed deterministic inputs under existing execution contracts?
11. Which candidate receiving types/interfaces already exist, and which examples in the design brief are currently fictional?
12. How are hybrid rules represented without making prose executable or duplicating deterministic consequence semantics?
13. When is formalization mandatory, preferred, optional or semantically wrong?
14. How does formalized campaign mechanics composition avoid forbidden shipped same-ID override and hidden ruleset forks?
15. What compact execution trace/provenance is required when a ruling affects a mechanical outcome?
16. How are correction, supersession and explicit repair distinguished from retroactive rewrite?
17. What are the exact persistence/recovery semantics when a durable ruling is created, changed or temporarily scoped?
18. What failure modes arise if policy text and typed mechanic references change independently?
19. Which architecture responsibilities belong to House Rules now versus S6D later versus resumed R2.7?
20. What is the smallest design that satisfies these responsibilities without a new generic subsystem?

---

# 11. Alternatives that must receive genuine consideration

Step 2 must compare distinct families before hybridizing them:

A. **Minimal existing-owner amendment** — keep campaign policy primarily in the existing `HOUSE_RULES.md`/current CORE owners, add only explicit conventions/delegation required for precedent and typed handoff.

B. **Separated campaign policy surfaces** — deliberate house rules and reusable campaign rulings have distinct physical surfaces but share common authority/lifecycle law.

C. **Unified structured campaign policy entries** — one durable family with explicit kind/scope/status/provenance, potentially human-readable but more structured.

D. **Prose-first policy + typed mechanic binding** — durable adjudicative policy remains readable prose while deterministic mechanics are referenced through existing typed owners.

E. **Predominantly formalized campaign mechanics** — use catalog/ruleset composition wherever possible, leaving only irreducibly fiction-dependent applicability to adjudication.

F. **No new durable ruling abstraction** — test whether existing campaign canon/house-rule policy plus normal accepted outcome history can satisfy consistency without a separate precedent object/family.

For every family, challenge what it cannot represent cleanly and what new authority/latency/maintenance cost it introduces.

---

# 12. Required adversarial scenarios during research

At minimum challenge candidate directions against:

- same unusual situation appears ten turns later after context compaction/retrieval;
- temporary ruling must survive one session boundary but should not become permanent campaign law;
- a durable precedent is later corrected/superseded;
- a house rule intentionally differs from baseline mechanics;
- a recurring rule is fully numerical and should not remain prose-only;
- a recurring rule depends on nuanced NPC goals/fiction and becomes brittle if encoded mechanically;
- prose applicability and deterministic consequence are split across hybrid owners;
- relevant precedent exists but is not currently loaded;
- two applicable rulings conflict or one is more specific;
- a ruling references a typed mechanic that is later replaced/renamed during pre-release canonicalization;
- an LLM attempts to output HP/resource/RNG/capability as if authoritative;
- a judgment legitimately supplies a bounded parameter/fact, but deterministic validation rejects it;
- player asks for a correction after a prior outcome was already committed;
- campaign policy grows large enough that full-file/full-corpus loading is no longer cheap;
- ordinary gameplay must still avoid repository/web/extra-LLM round trips;
- replay/audit must explain the accepted mechanical basis without hidden reasoning;
- no new ruling record/schema/index is added: identify precisely what fails, if anything;
- a proposed new ruling registry exists: prove why existing ownership/routing is insufficient.

---

# 13. Expected Step-2 deliverables

Step 2 must produce a **Research & Architecture Draft**, not a canonical spec.

It must include:

1. refined Source Manifest;
2. inspectable evidence ledger with source authority, qualifiers, amendments and dispositions;
3. current-state ownership/lifecycle/flow reconstruction;
4. contradictions/gaps proven from owning sources;
5. evaluation of the alternative families above plus any evidence-driven alternative discovered during research;
6. recommended conceptual architecture and authority boundaries;
7. explicit reuse/new-surface justification;
8. latency/retrieval/persistence/recovery analysis;
9. downstream House-Rules -> S6D contract at semantic level only;
10. unresolved questions classified into agent-resolvable evidence gaps versus genuine owner decisions;
11. challenge against counterexamples and simpler/deletion alternatives;
12. readiness assessment for Step 3 Decision Brief.

The Source Manifest/evidence-extraction/synthesis-completeness gates must pass before Step 3.

---

# 14. Step-1 success / exit criteria

Step 1 is complete when:

- the assignment is explicitly architectural and bounded;
- stale sequencing is removed from the active framing;
- the design brief's proposed two-channel model, lifecycle names, `RULINGS.md`, `HOUSE_RULES.md` shape and generic ruling metadata are treated as hypotheses rather than accepted architecture;
- current authority/determinism/latency/YAGNI constraints are preserved;
- the investigation can validly conclude that an initially proposed file/type/category is unnecessary;
- initial repository evidence routes cover governance, existing adjudication/rules policy, formal mechanics, campaign storage/retrieval and downstream consumers;
- WP-06 and S6D are explicitly fenced off from execution;
- Step 2 has concrete research questions, alternatives, challenge cases and exit deliverables.

**Step-1 disposition: PASS WITH MATERIAL REFRAMING.**

Next allowed action:

```text
House Rules Step 2 — Research & Architecture Draft
```

Blocked actions remain:

```text
R2.7 WP-06 RESUME: NO
S6D START: NO
GAME/SCHEMA/RUNTIME IMPLEMENTATION: NO
```
