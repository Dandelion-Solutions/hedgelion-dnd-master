# HDM Engine Design Process

Status: **AGREED — PROJECT-SPECIFIC ADAPTER**

## Purpose and authority

The canonical generic architecture/deep-work procedure is:

`DEV/DESIGN_PROCESS.md`

That document governs task classification, human/agent decision rights,
research and evidence discipline, repository evidence completeness, analytical
challenge, the eight-step deep-design loop, adversarial review,
canonicalization, deferred work, risk, traceability, and the transition from
architecture into implementation planning.

This file adds HDM-specific constraints. It must not be interpreted as a weaker
alternative process.

## Fresh-session architecture bootstrap

A fresh HDM architecture/deep-work chat must recover its working state from the
repository before it starts substantive synthesis or asks the project owner to
restate previous work.

Follow the repository bootstrap in `AGENTS.md`, then establish at least:

1. the current remote ref and repository state;
2. the current versions of `AGENTS.md`, `DEV/DESIGN_PROCESS.md`, this file and
   `DEV/PROJECT_MAP.md`;
3. the global current-progress authority in `DEV/CURRENT_PROGRESS.md`;
4. the roadmap in `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` when sequencing,
   scope or dependencies need detail;
5. the current canonical/derivative locator state needed for the task, including
   `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` where applicable;
6. the task-specific owning artifacts, neighboring schemas/tests/runtime
   contracts and research inputs identified through the project map.

Conversation summaries, previous-chat handoffs, model memory and remembered
filenames may help orientation only. They do not establish current architecture
state when repository sources are available.

Do not ask the project owner questions such as "what did we decide about X?" or
"which file owns Y?" until repository research has shown that the answer is not
recoverable from the current project sources.

## Superpowers requirement

Superpowers is a required development-process aid for HDM engine architecture.
It is not part of the game runtime, campaign bootstrap, release package, or
player environment. A campaign must never depend on the plugin being installed.

For architecture/deep-work blocks:

1. use the process in `DEV/DESIGN_PROCESS.md`;
2. invoke the applicable current Superpowers skills, beginning with
   `superpowers:using-superpowers` and using `superpowers:brainstorming` for
   architectural work;
3. use `superpowers:writing-plans` only after the relevant canonical design is
   approved;
4. keep Superpowers artifacts under the repository locations defined by
   `AGENTS.md`.

Superpowers is workflow discipline, not a substitute for repository research.
Invoking the correct skill does not satisfy the evidence or completeness gates
unless the required source discovery, extraction, reconciliation and review are
actually performed.

## Repository project-map / discovery requirement

HDM maintains `DEV/PROJECT_MAP.md` as a **non-normative navigation and dependency
index** for the repository. Its purpose is to prevent architecture research from
being scoped only by remembered filenames or keyword-search hits as the project
grows.

Before substantive repository research:

1. inspect the current remote branch/ref and current repository tree;
2. consult `DEV/PROJECT_MAP.md` to identify likely owners, neighboring surfaces,
   schemas, tests, support contracts, research inputs and historical derivation
   that may matter;
3. construct the task-specific **Source Manifest** required by
   `DEV/DESIGN_PROCESS.md` rather than treating one located file as the whole
   evidence set;
4. read the actual owning files before making correctness-sensitive claims;
5. follow relevant references into schemas, tests, runtime consumers and later
   amendments/owner decisions when they can change the conclusion;
6. search concrete symbols/paths for consumers and stale references after the
   structural pass;
7. treat an empty keyword search as non-evidence of absence until the relevant
   directory/tree and local indexes have also been checked.

`DEV/PROJECT_MAP.md` is never a semantic source of truth and must not repeat full
contracts merely for convenience. If it disagrees with an owning contract,
schema, machine catalog, canonical specification, roadmap/status document or the
actual current tree, that source wins and the map must be repaired.

Update the project map when a file/directory/responsibility change would make
future discovery materially misleading. Homogeneous families such as schemas,
tests and dated design artifacts may be covered by path/pattern rather than by a
manual entry for every member; the goal is reliable navigation and dependency
discovery, not a second copy of repository contents.

### Mandatory whole-project scope for both critics

**THIS IS A HARD HDM PROCESS GATE.** Both the Step-1 Task-Brief critic and the
Step-6 adversarial/candidate critic must use the current `DEV/PROJECT_MAP.md`
to reconstruct everything directly or indirectly relevant to the active block.
They must locate actual canonical owners, accepted and superseding decisions,
neighboring modules, schemas, tests, runtime consumers and cross-stage
dependencies rather than reviewing the block as an isolated component.

Each critic must explicitly test whether:

- an existing owner already settles a purported open question;
- the proposed block duplicates, contradicts or leaks another owner's authority;
- indirect consumers or invariants change the conclusion;
- a detected conflict should be repaired in the current block; or
- changing accepted architecture is materially justified and therefore requires
  a decision-ready superseding proposal to the human architect.

A critic that reads only the brief/candidate and its explicitly listed files has
not completed the gate. Blocking/significant dependency or owner omissions must
be resolved before proceeding. Keeping `DEV/PROJECT_MAP.md` accurate enough
for this discovery is part of the same process obligation.

### Mandatory Senior review stops in the eight-step loop

For HDM architecture/deep-work blocks, the generic eight-step loop has exactly
two **mandatory Senior review stops** independent of ordinary evidence work.
These stops exist so an independent Senior Auditor/project-owner review can
inspect the framing and the final result before the worker crosses the next major
boundary.

#### Review stop 1 — completed Step 1, after the Task-Brief critic

A draft or partially researched Task Brief is **not** a review checkpoint. Do not
bring a raw brief to the Senior Auditor/project owner merely to ask whether the
agent should finish framing it.

Before this mandatory stop, the worker must complete Step 1 as a whole:

1. construct the task-specific Source Manifest/discovery route deeply enough to
   frame the block correctly;
2. produce the complete Architecture Task Brief;
3. run the mandatory whole-project Step-1 Task-Brief critic;
4. inspect the actual owners/dependencies exposed by that critic;
5. repair all mechanically resolvable `BLOCKING`/`SIGNIFICANT` framing defects,
   omissions and stale assumptions;
6. record any genuine material human decision that remains rather than hiding it
   inside an unfinished brief;
7. leave a coherent, review-ready Step-1 artifact/checkpoint.

Only then stop and return the completed Step-1 package for Senior review and
possible intervention. **Step 2 must not begin until this review stop receives a
GO.**

The intent is explicit: the Senior review judges a finished, criticised framing;
it is not a substitute for the worker completing the framing or critic itself.

#### Review stop 2 — completed Step 8

After the Step-1 review gives GO, the worker may proceed through the remaining
cycle without artificial Senior pauses, subject to the material human-decision
rule below.

At Step 8, finish the complete canonicalization before stopping. This includes,
as applicable:

- candidate/spec critic findings resolved through Step 7;
- final Step-8 self-review complete;
- canonical artifacts and accepted decision summary synchronized;
- roadmap/status/traceability/deferred/debt state synchronized;
- required verification complete;
- coherent publication/checkpoint complete;
- remote read-back/currentness evidence obtained where repository process
  requires it;
- mandatory finding-propagation sweep complete.

#### Mandatory finding-propagation sweep

A `BLOCKING` or `SIGNIFICANT` Step-6 finding that changes, rejects or
materially qualifies a candidate law must be propagated before Step 7 is
complete. This is evidence/traceability work within the existing eight-step
loop; it creates neither a ninth step nor another routine human pause.

For each such finding, the Step-7 resolution record (or a directly linked
resolution ledger) must account for:

- the finding ID and repaired/current disposition;
- each affected Task Brief, Decision Brief, review, candidate, critic,
  canonical artifact, status/current-progress record, roadmap/index or deferred
  obligation;
- whether that artifact was updated, explicitly superseded, retained as safely
  historical/non-current, or shown not applicable;
- the one current final owner for every changed or rejected normative statement.

An artifact that preserves a rejected formulation as history must say so
explicitly and route readers to the finding/resolution and current final owner.
Do not rewrite historical analysis as though it originally made the later
correction. Update global status and derivative navigation only when their
current-state or routing claims are affected.

Then **stop for the second mandatory Senior review**. Do not automatically begin
the next architecture block or implementation-planning work until that review
receives a GO.

#### Additional stops only for genuine human decisions

The two stops above are mandatory process checkpoints; they do not remove the
human/agent decision-rights contract in `DEV/DESIGN_PROCESS.md`.

Between them, do not manufacture approval pauses for mechanically derivable
work. Continue automatically when the current evidence and accepted decisions
settle the next action. In particular, Step 3/4 does not require an extra stop
when its Decision Brief concludes `Human decision required: NO`.

If Step 2–7 exposes a genuine unresolved matter involving product semantics,
material architecture trade-offs, canonical authority/ownership, meaningful
compatibility policy, explicit risk acceptance, hard-to-reverse scope, or another
human-owned judgment under the generic process, stop at that actual decision
gate with a decision-ready brief and recommendation. Such a stop is substantive,
not a routine process checkpoint.

## HDM repository-evidence and synthesis gate

HDM architecture work must satisfy the generic repository-evidence completeness
gate in `DEV/DESIGN_PROCESS.md` before producing correctness-sensitive synthesis.
The project-specific interpretation is below.

### Task-specific evidence set

The Source Manifest should include, where relevant:

- current requirements and product constraints;
- canonical owning architecture/specifications;
- later canonical amendments and explicit owner decisions;
- current roadmap/status authority;
- derivative indexes used only to locate owners;
- relevant research dossiers, experiments and feasibility studies;
- affected `GAME/` runtime contracts;
- affected DEV catalogs/schemas/machine contracts;
- executable and scenario/adversarial tests;
- historical/derivation artifacts only when provenance, supersession or a
  previous assumption materially affects the current question.

The manifest is task-specific. HDM does **not** require reading the entire
repository for every architecture question. The agent must instead discover the
relevant dependency subgraph and read that subgraph deeply enough to support the
claims being made.

### Source roles must stay distinct

During research and synthesis, explicitly distinguish at least:

```text
CANONICAL / OWNING
CANONICAL AMENDMENT / OWNER DECISION
DERIVATIVE LOCATOR / INDEX
RESEARCH INPUT
HISTORICAL / SUPERSEDED DERIVATION
IMPLEMENTATION / MACHINE CONTRACT / TEST EVIDENCE
```

A research artifact does not become architecture because it is detailed or
persuasive. A derivative index does not override its linked owner. A historical
artifact does not regain authority because a current question resembles it.

### Enumerated findings and qualifiers

When an HDM source contains individually enumerated findings, candidates,
requirements, risks, review issues, test cases, deferred items or similar
records, item-level semantics must be preserved whenever the work claims
coverage or derives sequencing from that corpus.

For each relevant item record enough structured evidence to recover:

```text
Source/item:
Actual claim:
Classification/authority:
Qualifiers / applicability conditions:
Revisit/defer trigger, if any:
Existing HDM owner/decision, if any:
Conflict / extension / new consumer / no delta:
Current disposition:
Rationale:
```

Qualifiers are not editorial decoration. `revisit when`, `only if`, scope limits,
non-goals, exceptions, confidence, negative findings and explicit defer
conditions are part of the finding and must survive compression.

For research candidates, useful dispositions include:

```text
ACTIVE — current architecture work must consider it
INHERITED / ALREADY SATISFIED — current accepted architecture already covers it
CONDITIONAL / DORMANT — no current work; preserve the explicit revisit trigger
OUT OF CURRENT SCOPE — excluded by current product/deployment scope
REJECTED — consciously not adopted after analysis
```

`CONDITIONAL / DORMANT` is not an instruction to study the item immediately. If
the source itself says to return only when a trigger occurs and that trigger has
not occurred, preserving the trigger is normally sufficient.

The External Architecture Idea Dossier is one example of this rule, not the
reason for it. The same discipline applies to any enumerated research corpus,
review finding set, requirement list, schema contract, test inventory, migration
set or other correctness-sensitive collection.

### No thematic-coverage shortcut

A roadmap or architecture document must not claim that a source set is covered
merely because its broad themes resemble roadmap headings.

Before claiming coverage of an enumerated corpus, the agent must account for the
relevant items individually or through an equally strong mechanically verifiable
mapping. The output may be compact, but the underlying accounting must exist.

A synthesis may classify items as inherited, dormant, out-of-scope or rejected;
coverage does **not** mean every item becomes a roadmap stage or current task.

### Round-1 preservation rule

Round-1 architecture is a strong accepted base. A new research item or later
stage does not reopen a closed Round-1 topic merely because it discusses the same
subject.

Before reopening, classify whether the new work:

1. materially extends the accepted decision;
2. exposes a real contradiction or invalid assumption;
3. introduces a new consumer the accepted decision cannot satisfy;
4. makes the accepted decision insufficient for a current requirement.

If none apply, the new evidence is confirmation/context rather than new
architecture work.

### Human review is not the completeness mechanism

The project owner is not the final parser, proofreader or memory system for the
document corpus.

Before escalating a decision, the agent must independently establish everything
that can be established through repository inspection, source reconciliation,
structured evidence extraction, tests and logical consequence. The owner should
receive the decision-ready delta: what is established, what changed, what
remains genuinely ambiguous, the credible alternatives, the recommendation and
the exact human decision required.

Do not ask the owner to read large source sets merely to discover whether the
agent omitted a dependency, qualifier, prior decision or enumerated finding.

## HDM decision rights

Product requirements, gameplay semantics, project priorities, explicit risk
acceptance, and material architecture trade-offs remain owned by the project
owner/human architect.

The agent is responsible for the research, analytical challenge, recommendation,
mechanical formalization, detailed examples, consistency checking, source
coverage, critique resolution, roadmap/status bookkeeping, traceability and
specification completeness required by `DEV/DESIGN_PROCESS.md`.

Do not make the owner compensate for incomplete analysis by presenting raw
options without a recommendation, by asking for manual validation of mechanical
documentation details that follow from already accepted decisions, or by asking
the owner to reconstruct evidence that exists in repository sources.

## HDM architecture sequencing gate

Global current progress and the next authorized unit are owned only by
`DEV/CURRENT_PROGRESS.md`. `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` owns
the mechanical-architecture sequence, scope and dependencies; it is not a
second progress cursor.

Architecture work must:

- consult the global current-progress authority before choosing a stage;
- examine a later stage only when it exposes a dependency or contradiction
  relevant to the authorized work, without silently replacing that work;
- treat a stage as complete only when its required artifacts exist, its exit
  checks pass, and unresolved work is explicitly owned, deferred, dormant with
  a meaningful trigger, or recorded in the appropriate backlog/debt mechanism;
- review architecture before implementation;
- keep accepted decisions compatible with existing canonical HDM architecture
  unless an explicit superseding decision is made;
- update `DEV/CURRENT_PROGRESS.md` when global state or the next authorized
  unit changes, and update the roadmap only when sequence, scope or dependency
  content changes;
- require any roadmap rebaseline that derives a problem horizon from a research
  corpus to pass the repository-evidence and synthesis gate above before that
  coverage claim is treated as assured.

## HDM-specific analytical emphasis

In addition to the generic review gates, HDM architecture work must explicitly
look for risks created by the interaction between deterministic mechanics and
LLM-driven reasoning.

As relevant, challenge designs for:

- duplicate authority over canonical state;
- LLM output bypassing deterministic validation;
- narrative text becoming an accidental mechanical source of truth;
- inability to replay or recover committed mechanics deterministically;
- hidden coupling between GAME runtime contracts and DEV-only tooling/process;
- campaign/runtime dependence on development-only files;
- ambiguous state ownership across Actor, Asset, Effect, Resource, lifecycle,
  procedure-local state, and persistence layers;
- expensive campaign-wide scans or indexes where scoped ownership can provide a
  bounded query;
- cross-scene or multiplayer behavior that invalidates assumptions made by a
  single-scene design;
- hard-coded D&D rules where a registered policy/mechanic is required for
  extensibility;
- generic abstraction introduced without a concrete current requirement;
- research compression that drops qualifiers, revisit triggers or negative
  evidence;
- roadmap/spec synthesis that assumes broad thematic overlap proves source
  coverage.

## Development/runtime separation

This process applies only to engine architecture and related development work.

It must not add calls, context, latency, workflow objects, schema fields, or
runtime dependencies to an ordinary HDM gameplay turn merely to represent the
development process.

Development process, architecture drafts, Superpowers artifacts, tests, and
maintenance tooling belong under `DEV/` as governed by `AGENTS.md`.

Runtime behavior shipped to players belongs under `GAME/`.

## Unavailable-Superpowers rule

If the required Superpowers capability is not exposed in the current work
environment after its connection is checked:

- report the observed limitation rather than claiming the skill was used;
- do not mark a deep architecture block canonical merely by silently replacing
  the required process with an improvised one;
- research and clearly labelled drafts may continue where useful;
- only an explicit project-owner decision, made after the limitation is stated,
  may authorize a documented fallback for that block;
- such an exception does not disable the process gate for later work.

## Evidence without runtime bureaucracy

The design process itself should be visible through development artifacts, not
through product/runtime state.

Normally it is sufficient that the task brief, research/specification history
and roadmap show, at proportional depth:

- the relevant Source Manifest or otherwise auditable source coverage;
- the workflow/review performed;
- the decisions made;
- material risks/findings and their disposition;
- applicability qualifiers and revisit triggers that matter to future work;
- intentionally deferred/dormant work;
- the exit-gate state and next continuation point.

Do not create runtime entities solely to prove that architecture review or
document research occurred.
