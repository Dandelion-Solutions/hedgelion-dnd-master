# General Architecture & Deep-Work Design Process

Status: **CANONICAL DEVELOPMENT PROCESS**

## 1. Purpose

This document defines the default process for architecture, system design,
fundamental subsystem work, deep technical research, and other decisions whose
cost of being wrong is materially higher than the cost of doing the analysis.

It is intentionally generic. Project-specific architecture documents may add
constraints, terminology, gates, or deliverables, but should not weaken the
reasoning, review, decision-rights, evidence-completeness, or source-traceability
requirements defined here.

The process is not intended for every small engineering task. A local function,
small validation rule, obvious schema correction, narrow endpoint, or similarly
bounded change should use a proportionate workflow rather than mechanically
running the full deep-design loop.

The governing rule is:

> Use the lightest process that is sufficient for the real complexity and risk,
> and upgrade immediately when hidden architectural complexity appears.

---

## 2. Superpowers is the process framework

For deep design and architecture work, use `@superpowers`.

Before substantive work:

1. invoke `superpowers:using-superpowers`;
2. for new systems, subsystems, architecture blocks, interfaces, or material
   behavior changes, use `superpowers:brainstorming`;
3. read the current versions of the applicable skills rather than relying on
   remembered behavior;
4. inspect the current project state before proposing changes;
5. complete and review architecture before implementation;
6. after an approved canonical specification exists, use
   `superpowers:writing-plans` for implementation planning.

Superpowers supplies the workflow discipline. This document strengthens it with
explicit decision rights, evidence discipline, repository-source completeness,
analytical challenge gates, traceability, risk handling, and agent/human
responsibility separation.

Using the correct workflow skill is not itself evidence that repository research
or architecture analysis was complete. The substantive gates below still apply.

---

## 3. Process classification

Classify the task before choosing the workflow.

### 3.1 Spike / Investigation

Use for questions such as:

- is an approach technically feasible;
- does a platform/library/protocol support a needed capability;
- what hard limit exists;
- which of a few candidate technologies is viable;
- can a risky assumption be tested cheaply.

The output is evidence and a recommendation, not production architecture or
production code.

A spike should be as cheap as correctness permits. Throwaway artifacts remain
explicitly throwaway unless a separate design decision promotes them.

### 3.2 Bounded task

Use for a well-scoped change in an already understood flow, for example:

- one local function;
- a small field;
- a narrow endpoint;
- a validation rule;
- a contained algorithm change;
- an implementation detail whose surrounding architecture is already settled.

Typical flow:

```text
context -> essential questions -> short design -> approval -> implementation
```

Do not impose the full eight-step process on a genuinely bounded task.

If hidden complexity appears, the classification ratchets upward. Do not keep a
bounded label merely to avoid architecture work.

### 3.3 Architectural / deep-work task

Use the full process when one or more of the following are true:

- a new subsystem is introduced;
- component boundaries or ownership change;
- interfaces used by multiple components are created or changed;
- the work creates a fundamental data/state model;
- persistence, transactions, concurrency, consistency, security, lifecycle,
  versioning, migration, replay, or distributed behavior is involved;
- multiple credible architecture alternatives exist;
- material unknowns remain;
- a wrong decision would be expensive to reverse;
- the decision constrains future subsystems;
- the work spans several architectural concerns;
- product semantics or important quality attributes are affected.

When uncertain between bounded and architectural, use the heavier path.

---

# Part I — Design Governance

## 4. Human and agent decision rights

The process separates **decision-making** from **technical evidence work**.

The human architect/owner should spend attention on decisions that require
judgment, priorities, risk acceptance, or product intent. The agent should do
research, repository/document inspection, analysis, formalization, consistency
work, documentation, examples, bookkeeping, implementation decomposition and
verification-oriented traceability.

### 4.1 Human Architect decides

Escalate a decision to the human architect when it materially involves one or
more of the following:

- project goals or non-goals;
- user/product semantics;
- business or domain priorities;
- trade-offs between significant quality attributes;
- acceptance of material risk;
- expensive or hard-to-reverse choices;
- scope expansion or contraction;
- fundamental component boundaries;
- authority or ownership of canonical state;
- architecture that constrains multiple future subsystems;
- compatibility or migration policy with meaningful external consequences;
- choosing between alternatives that remain genuinely reasonable after analysis.

The agent must provide decision-ready information before asking for such a
choice.

### 4.2 Agent recommends; Human decides

Most architectural choices belong here.

The agent must:

1. research what can be established mechanically;
2. identify relevant constraints and quality attributes;
3. narrow the choice to actual alternatives;
4. analyze trade-offs and second-order effects;
5. recommend one option;
6. state confidence and major uncertainty;
7. tell the human exactly what decision remains.

The human decides the unresolved architectural trade-off.

### 4.3 Agent decides and executes

The agent should independently handle mechanical or derivable technical work
when the governing decisions are already known, including:

- complete specification wording;
- schemas and structural details implied by accepted architecture;
- examples and edge-case examples;
- terminology normalization;
- cross-reference maintenance;
- consistency checking;
- Decision Log / ADR maintenance;
- TODO / deferred / debt / backlog maintenance;
- risk-register bookkeeping;
- traceability maintenance;
- implementation-plan decomposition;
- test and verification mapping;
- obvious fixes discovered during self-review that do not introduce a new
  architectural trade-off.

Do not ask the human architect to approve mechanical details one by one when
those details follow unambiguously from an accepted decision.

### 4.4 Do not outsource insufficient analysis to the human

This is a hard rule:

> Never ask the human architect to compensate for insufficient agent analysis.

Before escalating a question, the agent must first establish everything that
can be established by research, repository inspection, documentation, testing,
or logical consequence.

Questions such as "Which option do you prefer?" are insufficient when the agent
has not first explained why the options matter, how they differ, which one it
recommends, and what evidence supports the recommendation.

### 4.5 AI-architect / human-architect operating contract

The architecture partnership is intentionally asymmetric in workload.

The **agent owns evidence work**. This includes discovering relevant sources,
reading them to the depth required by the question, extracting material claims
and qualifiers, reconciling source roles and supersession, checking consumers and
cross-system effects, maintaining traceability, detecting omissions and producing
a decision-ready synthesis.

The **human architect owns human judgment**. This includes product meaning,
priorities, material trade-offs, explicit risk acceptance, hard-to-reverse choices
and other decisions that remain genuinely reasonable after the technical evidence
has been exhausted.

Repository or documentation volume does not move evidence responsibility from
the agent to the human. A large corpus requires better routing, source selection,
structured extraction and completeness checks; it does not justify asking the
human to read the corpus to determine what the agent missed.

The intended interface is:

```text
Agent:
  repository state
  -> relevant evidence set
  -> extraction / reconciliation
  -> alternatives / consequences
  -> recommendation
  -> exact residual human decision

Human architect:
  product intent / priorities / risk judgment
  -> architectural decision

Agent:
  formalization / consistency / traceability / verification mapping
```

Human review is a decision gate, not a substitute for agent research completeness.

---

## 5. Information layers

Keep these categories explicit during deep work:

- **FACT** — externally or internally verifiable information;
- **CONSTRAINT** — a requirement or limitation that must be respected;
- **ASSUMPTION** — an unverified premise currently used by the design;
- **INFERENCE** — a reasoned conclusion derived from facts/constraints;
- **DECISION** — an accepted architectural choice;
- **OPEN QUESTION** — a material unresolved issue;
- **DEFERRED** — a deliberately postponed issue whose postponement is safe;
- **DEBT** — a knowingly suboptimal choice accepted for a stated reason.

Do not silently promote an assumption or inference into a fact.

---

## 6. Assumption and Evidence Ledger

Material assumptions must be inspectable.

For each assumption that could change the architecture, record as applicable:

```text
Assumption:
Confidence: HIGH | MEDIUM | LOW
Evidence:
Impact if false:
How to verify:
Revisit trigger:
```

Evidence must be evaluated for applicability, not merely existence.

For external sources consider:

- authority of the source;
- version;
- publication/currentness date when relevant;
- environment and jurisdiction where relevant;
- whether the source describes the same workload or problem class;
- whether a cited best practice depends on assumptions absent from this project.

"A source recommends X" and "X is appropriate here" are separate claims.

### 6.1 Repository Source Manifest

Before correctness-sensitive deep synthesis, construct a task-specific **Source
Manifest** from current project state and the repository's navigation/ownership
information.

The manifest exists to answer:

- which sources are relevant to this question;
- what authority role each source has;
- why it is included;
- which part must be inspected;
- which neighboring owners/consumers may change the conclusion;
- whether the source has been inspected deeply enough for the claim being made.

A practical form is:

```text
Source:
Authority role: CANONICAL | AMENDMENT/DECISION | DERIVATIVE | RESEARCH | HISTORICAL | IMPLEMENTATION/TEST
Why relevant:
Required scope:
Important neighbors/dependencies:
Inspection status:
```

The manifest need not become a permanent standalone artifact for every task. It
may live in the Architecture Task Brief, research notes or another inspectable
working artifact. The required property is auditable source selection, not
ceremony.

Do not read the entire repository merely to claim completeness. Use project
indexes and ownership routes to discover the relevant dependency subgraph, then
inspect that task-specific set to the depth required by the decision.

### 6.2 Evidence extraction and synthesis completeness gate

**NO ROADMAP, DECISION BRIEF, CANDIDATE SPECIFICATION, COVERAGE CLAIM OR
CANONICALIZATION CLAIM may rely on undocumented thematic sampling when the
relevant source material is available.**

Before synthesis, extract enough structured evidence from the Source Manifest to
preserve the semantics that can affect the conclusion.

For material source items, record as applicable:

```text
Source/item:
Actual claim:
Authority/classification:
Qualifiers / applicability conditions:
Exceptions / negative findings:
Revisit/defer trigger:
Related accepted decision/owner:
Current interpretation/disposition:
Rationale:
```

This is an evidence ledger, not private chain-of-thought. It records source facts,
qualifiers, relationships and dispositions necessary to audit the result.

Hard requirements:

1. **Owning sources beat summaries.** Navigation indexes, executive summaries,
   roadmaps, derivative indexes, prior-chat summaries, remembered content and
   search snippets are discovery/compression aids, not substitutes for owning
   artifacts when a correctness-sensitive claim depends on them.
2. **Qualifiers survive compression.** Scope conditions, `only if`, `revisit
   when`, defer triggers, exceptions, confidence, non-goals and negative findings
   are part of the evidence. Dropping them can reverse the meaning of a finding.
3. **Enumerated sets require accounting.** If a source contains enumerated
   requirements, findings, risks, review issues, candidates, test cases, schema
   members, deferred items or similar records, a claim of coverage requires
   item-level accounting or an equally strong mechanically verifiable mapping.
   Broad thematic similarity is not coverage evidence.
4. **Coverage does not imply activation.** An accounted item may be already
   satisfied, conditional/dormant, safely deferred, out of current scope or
   rejected. Completeness means the item is understood and correctly dispositioned,
   not that it becomes current architecture work.
5. **Research is not authority.** A detailed research artifact remains research
   until the architecture process evaluates and adopts its relevant principle.
6. **Closed decisions are not reopened by keyword overlap.** New evidence should
   first be classified as confirming, extending, contradicting, serving a new
   consumer, or exposing insufficiency in the accepted design.
7. **Human proofreading is not the gate.** The agent must run the completeness
   check itself before asking for architectural judgment.

Before moving from research to Decision Brief, explicitly check:

```text
[ ] Source Manifest covers the relevant ownership/dependency subgraph.
[ ] Actual owning sources were inspected where available.
[ ] Material enumerated items are accounted for where coverage is claimed.
[ ] Qualifiers, exceptions and revisit triggers were preserved.
[ ] Current accepted decisions and superseding amendments were reconciled.
[ ] Consumers/tests/schemas relevant to the claim were checked.
[ ] No conclusion depends only on a summary, search snippet or remembered state.
[ ] Remaining questions genuinely require human judgment or new evidence.
```

If any required check fails, synthesis is premature.

---

## 7. Quality attributes and measurable constraints

Architecture must be evaluated against project-relevant qualities rather than
against generic elegance.

Before selecting a fundamental design, identify the quality attributes that can
actually distinguish alternatives. Examples include:

- correctness;
- determinism;
- latency;
- throughput;
- consistency;
- availability;
- durability;
- recovery;
- observability;
- debuggability;
- security;
- privacy;
- maintainability;
- extensibility;
- operational complexity;
- deployment complexity;
- storage growth;
- cost;
- migration cost;
- interoperability;
- testability.

Where practical, express these as concrete constraints or fitness criteria rather
than adjectives.

Examples:

```text
State mutation must be deterministic.
Replay must reconstruct the same canonical state.
No probabilistic model output may mutate canonical state without validation.
RPO = 0 for committed ledger entries.
p95 command latency <= 200 ms at the target workload.
```

Do not invent numerical targets when the project has not established them.
Mark them as open decisions if the number itself matters.

---

# Part II — Project-Level Architecture Map

## 8. Create a development/architecture roadmap first

If the project does not yet have a high-level architecture/development map,
create one before deep-diving into individual fundamental blocks.

The number of stages is not fixed. It must follow the actual logical structure
and dependencies of the project.

The roadmap should capture:

### 8.1 Goals

What the project must achieve and what success means.

### 8.2 Non-goals

What the project intentionally does not attempt to solve.

### 8.3 Fundamental blocks

Decompose the system into meaningful areas or capabilities.

Example only:

```text
Project
├── Domain Model
│   ├── Actors
│   ├── Resources
│   └── State
├── Persistence
├── Execution Runtime
├── External Interfaces
├── Security
└── Observability
```

Never force a project into this shape.

### 8.4 Dependencies and sequencing

For each block identify:

- prerequisites;
- downstream consumers;
- decisions that must precede it;
- decisions that can safely wait;
- known cross-cutting constraints.

### 8.5 Architectural invariants

Record rules that all later designs must preserve.

### 8.6 Known unknowns

Record material questions that still require research.

### 8.7 Status

Use project-appropriate states such as:

```text
PLANNED
RESEARCH
DESIGN
REVIEW
CANONICAL
IMPLEMENTATION
DONE
```

The exact vocabulary may vary.

### 8.8 Repository navigation index for growing projects

As a repository grows, consider maintaining a compact **non-normative project
navigation index** that records where major responsibilities live and which
neighboring surfaces are commonly affected together. The filename and exact
format are project-specific.

There is no universal file-count threshold for when such an index becomes
necessary. Raw repository size is only a proxy for discovery difficulty. Create
or strengthen the index when one or more of these signals appears:

- a complete structural inspection of the relevant project area is no longer
  cheap enough to perform reliably at the start of ordinary substantive work;
- several ownership domains, layers, packages, or source trees coexist and a
  filename/keyword search does not reveal their relationships;
- important concerns are cross-cutting and routinely require checking several
  contracts, schemas, tests, tools, or operational surfaces together;
- large homogeneous families such as schemas, migrations, tests, generated
  contracts, plugins, or dated design artifacts make manual filename memory
  unreliable;
- agents or maintainers have already missed relevant files, stale references,
  duplicate authority, or consumers because discovery started from remembered
  names or one search query;
- the cost of omitting a relevant dependency is materially higher than the cost
  of maintaining a small navigation map;
- onboarding, handoff, context loss, or a fresh agent/session repeatedly requires
  reconstructing the same repository topology and dependency routes.

Prefer creating the index slightly **before** repeated misses become normal. The
purpose is to reduce discovery risk, not to prove that the project has crossed
an arbitrary size boundary.

A useful navigation index should normally capture:

- major responsibility/ownership areas and their primary entry points;
- source-of-truth status where confusion is likely;
- common cross-system dependency routes or "check these together" surfaces;
- links to existing local indexes rather than duplicating them;
- patterns for large homogeneous families instead of manually enumerating every
  member;
- known historical/legacy surfaces that are useful for provenance but must not
  override current owners.

The navigation index must **not** become another semantic source of truth. It
should summarize responsibilities and direct research to owning artifacts; full
rules, schemas, contracts, enums, and architecture decisions remain in their
actual owners. If the index conflicts with the current repository tree or an
owning artifact, the tree/owner wins and the index is stale.

For repository research, use the index as part of a structural discovery pass,
not as a substitute for it:

```text
current tree/ref
    -> navigation index, if present
    -> task-specific Source Manifest
    -> actual owning artifacts
    -> concrete symbol/path search for consumers and stale references
```

An empty keyword search is not evidence that a concept or dependency is absent
when the relevant repository area or local indexes have not yet been inspected.

Update the navigation index when structural or responsibility changes would make
future discovery materially misleading. Do not require an edit for every new
file that already belongs to a clearly covered homogeneous family.

---

## 9. The roadmap is a living model

The roadmap is not a promise that the first decomposition was correct.

Deep work may reveal that:

- a new fundamental block is required;
- two blocks should merge;
- one block should split;
- dependency direction was wrong;
- a supposed requirement is unnecessary;
- a decision must move earlier or later;
- an entire planned subsystem is YAGNI.

Update the roadmap when evidence changes the architecture map.

Do not preserve a bad decomposition merely because it existed first.

A roadmap rebaseline that claims to derive its problem horizon from prior
requirements, research or review findings must pass the evidence and synthesis
completeness gate before the coverage claim is treated as established.

---

# Part III — The Eight-Step Deep-Design Loop

## 10. Step 1 — Architecture Task Brief

Before researching a deep-design block, write a focused assignment for the
agent itself.

The Task Brief should define:

- problem statement;
- scope;
- goals;
- non-goals;
- existing constraints;
- applicable architecture invariants;
- relevant existing components;
- known dependencies;
- quality attributes that may distinguish solutions;
- unknowns that require investigation;
- repository/docs/code that must be inspected;
- initial Source Manifest / discovery route for repository evidence;
- external evidence that may be required;
- questions the result must answer;
- success/exit criteria.

As relevant, include:

- official documentation;
- standards and RFCs;
- primary technical sources;
- scientific literature;
- vendor documentation;
- analysis of comparable systems;
- best-practice research;
- source-code inspection;
- focused feasibility experiments.

The brief exists to make the investigation purposeful rather than an open-ended
search for interesting information.

### 10.1 Problem-Framing / Task-Brief Quality Gate

The formulation of the Task Brief is itself part of the architecture work. A
well-executed investigation can still produce a convincing but wrong answer if
the question was framed incorrectly, assumed the wrong abstraction boundary, or
silently embedded the desired solution.

Before substantive research begins, give explicit attention to the quality of
the research/draft assignment and revise it when necessary. There is no
universal template for a correct research prompt: its framing must follow the
specific project, stage, goals, unknowns, evidence state, failure model and cost
of error.

At minimum, challenge the framing for:

- a proposed solution, architecture, technology, record type or terminology
  already embedded in the question as if it were established;
- stale or unverified assumptions being treated as facts;
- a scope or abstraction boundary inherited from an earlier project stage that
  current evidence may no longer justify;
- a question so narrow that it can optimize one subsystem while missing the
  actual cross-system problem;
- a question so broad that research cannot distinguish decision-relevant
  evidence from interesting background;
- missing counterexamples, negative outcomes or simpler alternatives that the
  investigation must remain able to discover;
- wording that makes deletion, derivation, deferral, dormancy or rejection of the
  proposed abstraction impossible as a valid research result.

Ask explicitly:

> If the initial framing is wrong, could a competent and honest investigation
> still follow this assignment and return a persuasive but architecturally wrong
> answer?

If yes, improve the Task Brief before research. The brief should constrain the
investigation enough to make it purposeful while remaining solution-blind enough
that evidence can invalidate its initial terminology, assumptions, decomposition
or candidate approach.

The required depth of this framing review is proportional to the architectural
risk. Fundamental, cross-cutting, hard-to-reverse or poorly understood work
requires substantially more attention to the research prompt than a narrow,
well-bounded investigation.

### 10.2 Mandatory whole-project Task-Brief Critic

For deep-design work, the Task Brief quality gate SHALL include a distinct critic
pass before Step 2. The critic is not allowed to evaluate only the proposed
module or the files named by the draft brief.

**MANDATORY WHOLE-PROJECT RULE:** use `DEV/PROJECT_MAP.md` to construct the
task-specific dependency subgraph; locate and read the actual canonical owners,
accepted/superseding decisions, neighboring modules, schemas, tests, runtime
consumers and historical derivation that can change the framing. Follow direct
and indirect dependencies until the evidence is sufficient to detect an
incorrect boundary, an already-settled rule, a duplicate owner or a conflict
with accepted architecture.

The critic must ask:

- Which existing owner already governs each claimed responsibility or authority?
- Which upstream/downstream or sibling contracts can constrain the task?
- Is the brief treating an existing project rule as an unanswered question?
- Would the proposed scope optimize an isolated component while breaking an
  established cross-system invariant?
- If a conflict exists, is the task expected to change the current module, or
  does it expose a material trade-off that requires an explicit proposal to
  supersede accepted architecture?

A zero-result keyword search, remembered topology or the brief's initial source
list is insufficient. Blocking/significant omissions are repaired in the brief
before Step 2. The critic record must identify the dependency routes and owners
checked, not merely state that a whole-project review occurred.

---

## 11. Step 2 — Research & Architecture Draft

Execute the Task Brief.

### 11.1 Preferred evidence order

Use, as applicable:

1. current project requirements, architecture and code;
2. canonical project specifications and accepted decisions;
3. official documentation/specifications;
4. standards/RFCs;
5. primary research or controlled experiments;
6. established practice in comparable systems;
7. secondary sources.

Within the project, distinguish owning/canonical sources from derivative indexes,
research inputs, historical derivation and implementation/test evidence.

### 11.2 Repository/document research execution

Before drafting the recommendation:

1. refine the Source Manifest as references and dependency routes are discovered;
2. inspect the actual owning artifacts rather than stopping at routing indexes or
   summaries;
3. extract material claims and qualifiers into inspectable working evidence;
4. reconcile later amendments, superseding decisions and current consumers;
5. account for enumerated source items when the result claims coverage;
6. run the synthesis-completeness checklist in section 6.2.

Do not begin architecture synthesis merely because the high-level themes look
familiar. Extraction precedes synthesis.

A large source corpus should be processed selectively through ownership and
dependency routing. The goal is not to hold the entire repository in working
context; it is to avoid unsupported conclusions about the relevant subset.

### 11.3 Draft contents

Include only relevant sections, but consider:

- conceptual model;
- data/state structures;
- entities and value objects;
- relationships;
- ownership and authority;
- interfaces and contracts;
- lifecycle and state transitions;
- invariants;
- persistence;
- consistency and transaction boundaries;
- concurrency;
- error semantics;
- recovery behavior;
- security boundaries;
- observability;
- versioning and migration;
- performance implications;
- extension points;
- examples;
- counterexamples;
- edge cases;
- integration effects.

### 11.4 Alternatives

When multiple credible solutions exist, present normally two or three real
alternatives or a justified hybrid.

For each alternative assess:

- what it optimizes;
- benefits;
- weaknesses;
- constraints;
- failure modes;
- operational consequences;
- future constraints;
- migration/reversal cost;
- interaction with project quality attributes.

Do not manufacture weak alternatives merely to reach a count.

Always consider the **simplest viable design**. When applicable, also consider
**defer / do nothing yet** as a legitimate alternative.

End with the agent's current recommendation, not just a menu of options.

---

## 12. Analytical Quality Gate — challenge the recommendation before presenting it

Before producing the Decision Brief, the agent must run a deliberate challenge
pass against its own preferred solution.

This is mandatory for deep-design work.

### 12.1 Strongest opposing case

State the strongest credible argument against the preferred solution.

Do not use a strawman objection.

### 12.2 Simplest viable comparison

Compare the preferred solution against the least complex design that still
satisfies the known requirements.

Ask:

- Which complexity is actually required?
- Which complexity is speculative?
- What can safely be delayed?
- Is an abstraction solving a current problem or a hypothetical future one?

### 12.3 Assumption attack

Identify assumptions on which the preferred design depends.

For each material assumption ask what happens if it is false.

### 12.4 Counterexample and failure-scenario construction

Try concrete scenarios intended to break the design.

Relevant examples may include:

- partial failure;
- retry;
- duplicate request;
- stale state;
- concurrent mutation;
- restart/recovery;
- missing dependency;
- invalid external input;
- migration from older state;
- long-running accumulation;
- unusual but valid domain state;
- multiple interacting features;
- resource exhaustion.

The scenarios should follow from the actual system rather than from a generic
checklist.

### 12.5 Local-versus-global optimization check

Ask whether the design makes one subsystem elegant by making the whole system
harder.

Check for:

- duplicated authority;
- leaked abstractions;
- cross-module special cases;
- downstream coupling;
- hidden operational burden;
- complexity displaced rather than removed.

### 12.6 Best-practice applicability check

For each influential external pattern or "best practice", ask:

- what assumptions make that practice successful;
- whether those assumptions hold here;
- whether the project has a different workload, scale, failure model, or
  deployment model;
- whether a simpler project-specific design is stronger.

### 12.7 Reversibility and option-value check

Assess:

- how costly the decision is to reverse;
- whether uncertainty justifies preserving options;
- whether preserving options itself adds unjustified complexity.

### 12.8 Recommendation falsifiability

State:

```text
Recommendation confidence: HIGH | MEDIUM | LOW
What evidence would change this recommendation:
```

A recommendation that cannot name plausible disconfirming evidence has probably
not been challenged enough.

Only after this gate should the recommendation be presented for human decision.

---

## 13. Step 3 — Decision Brief

Convert the research into concise decision-ready information for the human
architect.

The Decision Brief is an interface between agent analysis and human judgment.
It should normally answer:

1. **What are we deciding?**
2. **Why does it need to be decided now?**
3. **Which requirements/quality attributes actually distinguish the options?**
4. **What does the agent recommend?**
5. **Why?**
6. **What is the strongest weakness of that recommendation?**
7. **What do we gain and lose versus the credible alternatives?**
8. **What assumptions or uncertainty remain?**
9. **What would change the recommendation?**
10. **What exact human decision is required?**

Include:

```text
Recommendation confidence: HIGH | MEDIUM | LOW
Human decision required: YES | NO
```

Do not bury the actual decision under documentation detail.

Do not ask the architect to review structures that are mechanically implied by
an already accepted decision unless a structural choice itself changes the
trade-off.

Do not present a large source corpus to the human as a substitute for synthesis.
The Decision Brief should expose traceable evidence and uncertainty while keeping
the human's task focused on judgment, not completeness checking.

---

## 14. Step 4 — Collaborative Architecture Review

Discuss the Decision Brief with the human architect.

The review may:

- clarify requirements;
- correct assumptions;
- choose between alternatives;
- introduce constraints;
- reject the recommendation;
- expose new unknowns.

When a material unknown appears, do not fill the gap with a plausible guess.
Run a focused nested loop:

```text
QUESTION
  -> TARGETED RESEARCH
  -> FINDING
  -> RECOMMENDATION
  -> DECISION
  -> return to main design
```

The nested loop should be as small as the question permits.

Continue only after the unknown no longer materially prevents the design choice.

---

## 15. Step 5 — Candidate Specification

After the significant choices are settled, produce a complete candidate
specification.

At this point the document should describe one concrete architecture, not a list
of unresolved A/B/C options for decisions that were already made.

The specification should contain enough detail that a future engineer or agent
can understand the design without reconstructing it from chat history.

As relevant, include:

- goals and scope;
- normative terminology;
- architecture and components;
- responsibilities and boundaries;
- ownership/authority;
- interfaces/contracts;
- schemas and structures;
- catalogs/enums/registries;
- relationships;
- lifecycle/state machines;
- invariants;
- dependency direction;
- transaction boundaries;
- consistency/concurrency rules;
- error semantics;
- recovery;
- persistence;
- security;
- observability;
- versioning/migration;
- examples;
- invalid examples;
- integration points;
- quality-attribute consequences;
- intentionally deferred scope.

### 15.1 Agent responsibility for completeness

The agent owns the mechanical and documentary completeness of this document.

The human architect should not be required to proofread hundreds or thousands
of lines merely to ensure that:

- a previously agreed field was copied correctly;
- examples match the normative rule;
- terminology is consistent;
- an enum was fully listed;
- cross-references were updated;
- a decision was recorded in the correct section;
- a relevant source qualifier or already accepted decision was silently dropped;
- an enumerated finding was forgotten during synthesis.

Those are agent responsibilities and should be checked mechanically, through
structured source accounting, or by self-review where possible.

---

## 16. Cross-System Impact Analysis

Before adversarial review, explicitly evaluate what the candidate decision does
to the rest of the system.

For the block record, as applicable:

```text
Depends on:
Constrains:
Owns:
May mutate:
May observe:
Consumers:
Future decisions affected:
Migration effects:
Operational effects:
```

Ask:

> What does this decision make easier, harder, or impossible elsewhere in the
> system?

Pay special attention to internal implementation details that have leaked into
other components and become de facto global architecture.

---

## 17. Step 6 — Adversarial Architecture Review

Run a separate critical review before canonicalization.

The critic's objective is not to confirm the design.

Use the stance:

> Assume the candidate architecture contains hidden weaknesses. Find concrete
> ways it can fail, conflict, over-constrain, duplicate authority, or create
> unnecessary complexity.

Where tools/process allow, prefer a reviewer that approaches the candidate with
a fresh context rather than merely continuing the same line of reasoning.

**MANDATORY WHOLE-PROJECT RULE:** the adversarial critic SHALL independently
reconstruct the relevant dependency subgraph through `DEV/PROJECT_MAP.md`,
then inspect the actual upstream, downstream and sibling owners/consumers whose
contracts can constrain the candidate. It must search for already accepted
rules, hidden cross-owner conflicts, duplicate authority and consequences
outside the candidate's local module. Reviewing only the candidate artifact,
its stated Source Manifest or its immediate directory is invalid.

When a conflict is found, the critic must determine whether the candidate should
conform to existing architecture or whether the evidence exposes a real material
trade-off requiring an explicit superseding human decision. It must not silently
overwrite accepted architecture, invent a new authority, or escalate a question
that an existing canonical owner already answers.

Review only categories relevant to the design, including as applicable:

- requirement mismatch;
- contradiction with accepted architecture;
- incorrect abstraction boundaries;
- duplicate or unclear authority;
- leaked abstractions;
- hidden coupling;
- invalid or ambiguous states;
- invariant violations;
- transaction boundaries;
- data consistency;
- concurrency and races;
- retry/idempotency behavior;
- partial failure and recovery;
- security/authorization;
- performance and scalability;
- storage/memory growth;
- migration;
- compatibility/versioning;
- observability;
- debuggability;
- testability;
- maintainability;
- extensibility;
- operational complexity;
- vendor/platform lock-in;
- irreversible decisions;
- premature abstraction;
- overengineering;
- YAGNI violations;
- missing failure semantics;
- missing ownership/authority;
- requirements that are only implicit;
- evidence-set omissions or source-role confusion;
- dropped qualifiers, revisit triggers or negative findings;
- coverage claims unsupported by item-level accounting where required.

For AI/LLM systems also consider when relevant:

- deterministic versus probabilistic authority;
- validation boundaries;
- hallucination containment;
- provenance;
- replayability;
- state mutation authority;
- prompt/context trust boundaries;
- model-output schema enforcement.

### 17.1 Finding classification

Classify findings at least as:

```text
BLOCKING
SIGNIFICANT
MINOR
```

For material findings record where useful:

```text
Probability:
Impact:
Reversibility:
Detection difficulty:
Mitigation:
```

A vague statement such as "this may not scale" is insufficient without a
credible failure scenario or mechanism.

---

## 18. Step 7 — Resolution Gate

Do not blindly copy critic comments into the architecture.

Evaluate each material finding:

```text
Issue:
Severity:
Do we agree?:
Reasoning:
Proposed resolution:
Architectural consequences:
Human decision required?:
```

The agent should fix obvious defects directly when no new architectural
trade-off is introduced.

Return genuine trade-offs to the human architect with a recommendation.

After changes, determine whether the changes themselves created material new
risk.

If yes, repeat:

```text
Candidate Spec
  -> Adversarial Review
  -> Resolution
  -> Candidate Spec
```

Repeat until all `BLOCKING` findings are closed and `SIGNIFICANT` findings are
resolved, accepted as explicit risk/debt, or intentionally deferred with a safe
boundary.

Do not run endless review cycles because of cosmetic `MINOR` comments.

The goal is robust architecture, not zero comments.

---

## 19. Step 8 — Canonicalization

Before marking the design canonical, the agent performs a final self-review.

Check:

1. no accidental TBD/TODO remains in normative required behavior;
2. terminology is consistent;
3. no internal contradictions remain;
4. examples match normative rules;
5. accepted decisions are represented completely;
6. assumptions are still valid or explicitly recorded;
7. ownership and dependency direction are clear;
8. cross-system effects are reflected where required;
9. unresolved work is classified correctly;
10. Decision Log / ADR is updated;
11. Risk Register is updated;
12. Deferred / Debt / Backlog is updated;
13. the global current-progress authority is updated, and the roadmap is updated only when sequencing or scope changed;
14. traceability is sufficient for material requirements/decisions;
15. Source Manifest coverage is sufficient for the claims made;
16. material enumerated source items and qualifiers were accounted for where
    coverage was claimed;
17. no correctness-sensitive conclusion depends only on a derivative summary,
    search snippet or remembered state.

Then save the architecture as the canonical project artifact.

The human architect approves the significant architectural decisions and the
final decision summary. The human is not required to manually revalidate every
line of mechanical formalization or re-read the underlying source corpus if those
decisions were already reviewed and the agent completed the evidence and
consistency gates.

---

# Part IV — Project Memory and Traceability

## 20. Decision Log / ADR discipline

Maintain history for material architecture decisions.

A compact record may use:

```text
Decision ID:
Context:
Constraints:
Alternatives:
Chosen:
Reason:
Consequences:
Status:
Date:
```

Suggested statuses:

```text
PROPOSED
ACCEPTED
REJECTED
SUPERSEDED
```

Do not erase old decisions merely because they changed. Mark them superseded and
link the replacement so future readers can understand why the architecture
evolved.

---

## 21. TODO, TOBIDONE / Deferred, Backlog, and Architecture Debt

These categories are different and should not be conflated.

### 21.1 TODO

Work required to complete the current block or an immediately required stage.

A TODO that affects correctness of the current canonical design cannot be
silently deferred.

### 21.2 TOBIDONE / Deferred

A known item intentionally postponed because it is not required by current
scope and postponement is safe.

Record where useful:

```text
Item:
Reason deferred:
Related component:
Dependencies:
Revisit trigger:
```

Example:

```text
Item: introduce distributed locking
Reason deferred: current deployment is single-node
Revisit trigger: before multi-node execution is introduced
```

### 21.3 Conditional / Dormant

A known candidate or concern whose own applicability condition has not occurred.
It is preserved so the project can return to it when the condition becomes true,
but it does not create current architecture work merely because it is known.

Record where useful:

```text
Item:
Why dormant:
Revisit trigger:
Current owner/context:
```

Do not promote `revisit when X` into an immediate TODO unless `X` is now true or
new evidence creates an independent current requirement.

### 21.4 Backlog

An idea, enhancement, optional direction, or future investigation without a
current commitment to implement it.

### 21.5 Architecture Debt

A knowingly suboptimal architecture choice accepted because of time, cost,
compatibility, delivery pressure, or another explicit reason.

Record:

```text
Debt:
Why accepted:
Consequence:
Risk:
Revisit trigger:
Expected migration path:
Maximum acceptable lifetime:  # if meaningful
```

Do not label a critical unresolved correctness question as "debt" to bypass the
design gate.

---

## 22. Deferred/dormant is not unresolved architecture

Deferral or dormancy is valid only if:

- the current scope remains correct without resolving the item;
- a safe boundary exists;
- future resolution will not invalidate current invariants unexpectedly;
- the trigger for revisiting is known or the backlog status is explicit.

A canonical specification must not contain critical holes such as:

```text
TODO: decide later how consistency works.
```

if consistency is necessary for correctness of the current design.

---

## 23. Risk Register

For material risks record, as applicable:

```text
Risk:
Probability:
Impact:
Reversibility:
Detection difficulty:
Mitigation:
Trigger:
Owner:
Status:
```

Pay particular attention to risks that are:

- low probability but catastrophic;
- hard to reverse;
- discovered only late;
- cross-cutting;
- dependent on external vendors/platforms;
- capable of corrupting canonical state;
- capable of silently producing incorrect results.

Risk acceptance that changes project trade-offs belongs to the human architect.

---

## 24. Traceability

For material requirements and decisions, preserve a navigable chain such as:

```text
Requirement / Constraint / Research Finding
  -> Applicability / Disposition
  -> Invariant / Architecture Decision
  -> Canonical Specification
  -> Implementation Plan
  -> Verification / Test
```

Use identifiers such as `REQ-*`, `INV-*`, or `ADR-*` when the project benefits
from them. Do not create ceremony for trivial requirements.

Traceability should allow an agent to detect questions such as:

- Which decision caused this structure to exist?
- Which implementation task satisfies this requirement?
- Is an accepted requirement missing from the plan?
- Does a superseded decision still appear in the spec?
- Is there a schema field with no current architectural rationale?
- Which test verifies a critical invariant?
- Which research finding was adopted, rejected, deferred or left dormant, and
  under what trigger?
- Is a coverage claim missing an enumerated source item or qualifier?

---

# Part V — Analytical Principles

## 25. Invariants before structures

Determine rules the system must preserve before optimizing tables, classes,
messages, or files.

Structures should express the invariants rather than becoming accidental
architecture because they were easy to implement first.

---

## 26. Boundaries and authority before implementation

For every important component, be able to answer:

- what does it do;
- what does it not do;
- what does it own;
- what may it mutate;
- what may it observe;
- what does it consume;
- what does it produce;
- what does it depend on;
- who may change its canonical state.

If these answers are unclear, the design is not yet ready for implementation.

---

## 27. Prefer explicit contracts

Important agreements between components should be represented by explicit
interfaces, schemas, types, state transitions, validations, invariants, or
normative documentation.

Avoid architecture that depends on hidden shared assumptions.

---

## 28. Make trade-offs explicit

Every significant recommendation should state what is gained and what is paid.

If a proposal lists only benefits, analysis is incomplete.

---

## 29. Prefer reversibility under uncertainty, but do not abstract speculatively

When evidence is weak, avoid unnecessarily irreversible commitments.

However, do not add adapter layers, plugin systems, indirection, or generic
abstractions solely to preserve hypothetical future options.

Option value itself has complexity cost.

---

## 30. YAGNI aggressively

Do not build infrastructure for requirements that do not exist and are not
credibly expected.

Extensibility should be directional: easy in expected directions, not universal
for every imaginable future.

Known research candidates with unmet revisit triggers are not current
requirements merely because they are documented.

---

## 31. Architecture must survive concrete examples

Validate important models with concrete scenarios.

Depending on the subsystem, include examples such as:

```text
create
read
modify
delete
retry
duplicate
partial failure
concurrent modification
restart/recovery
migration
version mismatch
invalid state
long-running accumulation
```

Use scenarios that reveal the actual design's weak points rather than blindly
running a generic checklist.

---

## 32. Architecture must survive failure

For important behavior ask:

- what can fail;
- what state remains after failure;
- whether a retry is safe;
- whether recovery is deterministic;
- who detects the failure;
- who has authority to repair state;
- whether partial progress is visible;
- whether failure can silently violate an invariant.

A happy-path-only architecture is incomplete.

---

## 33. Detect complexity displacement

When a design simplifies one component, check where the complexity moved.

Common forms include:

- a simple writer creating a complex reader;
- a simple domain model requiring many runtime special cases;
- a generic abstraction forcing every consumer to branch;
- duplicated cached state creating synchronization work;
- an elegant schema requiring expensive operational reconciliation.

Complexity that moved is not complexity that disappeared.

---

## 34. Distinguish expected scale from imaginary scale

Do not justify present complexity with unbounded phrases such as "for scale".

Use the project's expected workload, growth model, failure domain, and operating
environment.

If scale is genuinely uncertain and architecture depends on it, elevate the
uncertainty as an assumption or human decision rather than inventing a target.

---

## 35. Stop research when it stops changing decisions — after coverage is sound

Research is complete when both are true:

1. the task-specific evidence set and required completeness checks are sound for
   the claims being made; and
2. additional evidence no longer materially changes:
   - constraints;
   - credible alternatives;
   - risk assessment;
   - recommendation;
   - confidence;
   - required architecture decisions.

Do not continue research merely to accumulate citations or appear thorough.

Do not use diminishing returns as an excuse to stop before the relevant owners,
material qualifiers or enumerated items required for a coverage claim have been
accounted for.

---

# Part VI — Transition to Implementation

## 36. Architecture and implementation planning are separate artifacts

The canonical architecture specification answers:

> What are we building, how is it conceptually structured, what invariants and
> contracts govern it, and why was this design chosen?

The implementation plan answers:

> How will this architecture be realized in the current codebase, in what order,
> in which files, with which tests and verification steps?

Do not prematurely hard-code implementation structure into early architecture
unless the implementation choice is itself architecturally significant.

After canonical design approval, use `superpowers:writing-plans`.

The implementation plan should define concrete, independently testable work with
explicit files, interfaces, dependencies, tests, verification, and sequencing.

---

## 37. Discovery during implementation

Implementation may reveal that an architectural assumption was wrong.

Do not hide a material architecture problem behind a local workaround.

Return to design when a discovery:

- changes a contract;
- violates an invariant;
- changes canonical ownership;
- materially affects another component;
- introduces a new architecture trade-off;
- invalidates a quality-attribute assumption;
- creates a new significant risk.

Use the smallest sufficient return path:

```text
focused research -> finding -> decision -> spec amendment
```

or, when necessary, a full new deep-design loop.

Update the canonical specification and implementation plan before continuing the
affected implementation.

---

# Part VII — Definition of Done

## 38. Definition of Architecture Done

A deep-design block is architecture-complete when:

- scope and non-goals are explicit;
- material requirements and constraints are known;
- relevant quality attributes are identified;
- material assumptions are visible;
- the task-specific Source Manifest/evidence set is sufficient for the claims made;
- actual owning sources were inspected where available;
- material source qualifiers and enumerated items were accounted for when required;
- invariants are defined;
- credible alternatives were considered;
- the chosen approach is explicit;
- trade-offs are understood;
- ownership and component boundaries are clear;
- dependencies and cross-system effects are clear;
- contracts and structures are documented sufficiently;
- critical edge/failure cases were exercised conceptually;
- analytical self-challenge was completed;
- adversarial review was completed;
- all `BLOCKING` findings are closed;
- `SIGNIFICANT` findings are resolved or explicitly accepted/deferred;
- significant risks are mitigated or consciously accepted;
- unresolved work is correctly classified as TODO, Deferred, Conditional/Dormant,
  Backlog, or Debt;
- Decision Log / ADR is updated;
- Risk Register is updated when needed;
- roadmap is updated;
- traceability is sufficient for material decisions;
- the canonical specification is stored;
- the exact next continuation point is known.

Only then should the block move into implementation planning.

---

# Part VIII — Process Overview

## 39. End-to-end flow

```text
PROJECT CONTEXT / CURRENT REPOSITORY STATE
      |
      v
Navigation / Ownership Discovery
      |
      v
Task-specific Source Manifest
      |
      v
Architecture Task Brief
      |
      v
Evidence Extraction / Reconciliation
      |
      v
Repository Evidence & Synthesis Completeness Gate
      |
      v
Research + Architecture Draft
      |
      v
Analytical Quality Gate
      |
      v
Decision Brief
      |
      v
Human Architecture Review
      |
      +---- material unknown ----> focused research loop ----+
      |                                                       |
      <-------------------------------------------------------+
      |
      v
Candidate Specification
      |
      v
Cross-System Impact Analysis
      |
      v
Adversarial Review
      |
      v
Resolution Gate
      |
      +---- material redesign ----> review/resolution loop ---+
      |                                                       |
      <-------------------------------------------------------+
      |
      v
Canonicalization
      |
      +--> Decision Log / ADR
      +--> Assumption/Evidence Ledger
      +--> Source/Disposition Traceability
      +--> Risk Register
      +--> TODO / Deferred / Dormant / Backlog / Debt
      +--> Roadmap update
      |
      v
Implementation Planning (`superpowers:writing-plans`)
      |
      v
Implementation / Verification
```

---

## 40. Governing principle

The human architect should receive **necessary and sufficient information for
judgment**.

The agent should perform **the maximum amount of repository research, evidence
extraction, challenge, formalization, verification, bookkeeping, consistency
checking and technical detail work that does not require human judgment**.

Documentation volume is an agent workload problem, not a human review problem.
Completeness does not mean reading everything for every task; it means correctly
discovering the relevant source set, exhausting that set to the degree required
by the claims being made, and preserving the semantics that affect the decision.

The process succeeds when the human spends time choosing goals and meaningful
trade-offs rather than reconstructing repository state, catching preventable
analytical omissions or manually checking documentary consistency.