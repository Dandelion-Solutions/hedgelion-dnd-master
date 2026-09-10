# HDM Development Agent Instructions

## Scope

This file governs **development work on the HDM engine repository**. It is not part of gameplay/runtime instructions and is never shipped in the runtime release asset.

## Runtime instruction overlays

This repository supports more than one agent runtime. The core rules in this file apply everywhere; a runtime overlay supplies the transport, tool and verification mechanics that are actually available.

Before external repository communication or execution work, identify the current runtime and load its overlay:

- **ChatGPT Work / Codex with GitHub Connector:** `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`;
- **OpenCode:** `DEV/AGENT_RUNTIMES/OPENCODE.md` and `DEV/AGENT_RUNTIMES/LOCAL_MACHINE.md`;
- **Claude Code:** `DEV/AGENT_RUNTIMES/CLAUDE_CODE.md` and `DEV/AGENT_RUNTIMES/LOCAL_MACHINE.md`;
- **another runtime:** stop before remote writes or verification claims unless an equivalent runtime policy has been explicitly supplied.

An overlay adapts process to its environment. It may not weaken the HDM authority hierarchy, source/evidence requirements, branch guardrails, public-material rules, approval gates, or prohibition on force-pushing live refs.

## Project skill stack

HDM development uses **Superpowers as the process-owner skill layer** plus four specialized domain/evidence skills:

```text
Product Owner / HDM authoritative repository owners
                    |
                    v
             Superpowers
           (process authority)
                    |
        +-----------+-----------+----------------+----------------+
        |                       |                |                |
        v                       v                v                v
Clean Architecture        SOTA Python      Prompt Optimizer   OpenAI Docs
(architecture)          (Python code)      (LLM prompts)     (OpenAI facts)
```

This diagram is a **scope/authority model, not a pipeline that requires every skill on every task**. `Clean Architecture`, `SOTA Python`, `Prompt Optimizer`, and `OpenAI Docs` are sibling specialists under the Superpowers process frame. They do not have a general total ordering among themselves; when scopes overlap, the ownership rules below determine which skill is primary for the specific decision.

The active skill set is:

- **Superpowers** — development-process authority. It owns skill selection/invocation order and the applicable workflows for brainstorming/design, implementation planning, TDD, systematic debugging, execution, review, verification, and completion discipline. It does **not** own HDM product semantics, architectural decisions already owned by canonical repository artifacts, Python language semantics, prompt content semantics, or OpenAI platform facts.
- **Clean Architecture** — project-local architectural skill at `.agents/skills/clean-architecture/SKILL.md`. It owns the architectural review/design lens for dependency direction, boundary placement, entities/use cases/adapters/framework details, persistence isolation, component coupling/cohesion, composition roots, and SOLID-level structural concerns. It may advise architecture but is subordinate to accepted HDM architecture owners and decisions.
- **SOTA Python** — project-local Python implementation skill at `.agents/skills/sota-python/SKILL.md`. It owns Python-language realization guidance: typing, data-modeling idioms, stdlib/tooling choices, resource/error handling, Python-specific security, async mechanics when applicable, measured performance practice, lint/type-check/test-runner mechanics, and Python code audit guidance. It does **not** own architecture, product semantics, TDD/test strategy, repository dependency/toolchain policy, persistence or other product-technology choices already made by HDM, runtime/package boundaries, or provider/model semantics.
- **Prompt Optimizer** — project-local prompt/instruction skill at `.agents/skills/prompt-optimizer/SKILL.md`. It owns prompt-quality methodology: instruction ownership/layering, prompt structure, reusable prompt templates, tool-policy wording, examples, output-contract expression, prompt-specific eval design, optimization loops, model-family portability, and prompt failure analysis. It does **not** own HDM product semantics, accepted contracts, architecture, or current vendor facts.
- **OpenAI Docs** — the current runtime-provided `openai-docs` skill/capability and official OpenAI developer-documentation route. It is the primary **factual evidence source** for current OpenAI model/API/Codex/tool/prompting behavior and model-specific guidance. It does **not** own HDM product semantics, architecture, process, Python implementation style, or prompt methodology. If the runtime does not expose the skill directly, use the runtime's permitted route to current official OpenAI documentation rather than substituting model memory for current facts.

### Authority hierarchy

For every task, resolve authority in this order:

```text
1. Explicit Product Owner instructions
2. AGENTS.md + applicable runtime overlay + current canonical/accepted HDM process, architecture, specification and owner decisions
3. Superpowers process rules
4. Applicable specialist skill guidance within that specialist's delegated scope
5. Generic model knowledge/defaults
```

A lower level MUST NOT silently override a higher level. A skill's own words such as `mandatory`, `non-negotiable`, `must`, scoring targets, default toolchains, or recommended companion skills remain subordinate to this hierarchy.

### Specialist ownership matrix

| Decision / concern | Primary skill owner | Secondary role(s) |
|---|---|---|
| Development/design workflow, implementation planning, TDD cycle, debugging process, execution/review/verification discipline | **Superpowers** | HDM process owners constrain/adapt the workflow; other skills provide domain-specific checks |
| Architecture boundaries, dependency direction, component placement/coupling, persistence/framework isolation, composition structure | **Clean Architecture** | SOTA Python may advise idiomatic realization after the architectural decision |
| Python types, idioms, data carriers, error/resource handling, Python tooling, Python-specific security/performance, pytest/Hypothesis mechanics | **SOTA Python** | Clean Architecture constrains boundary/dependency placement; Superpowers and HDM execution owners control test/process obligations |
| Prompt/instruction structure, layer ownership, prompt contracts, examples/tool-policy wording, prompt-specific eval cases and optimization | **Prompt Optimizer** | OpenAI Docs supplies current OpenAI facts; Superpowers/HDM owners control project process and acceptance gates |
| Current OpenAI API/model/tool/Codex behavior, supported features, provider-specific prompting facts and recommendations | **OpenAI Docs** | Prompt Optimizer applies those facts to prompt design; SOTA Python applies API facts to Python realization |
| HDM product/gameplay semantics, accepted architecture/contracts, canonical state ownership, scope and Product-Owner choices | **No skill owns this** | Controlled only by Product Owner and current canonical HDM repository authorities |

### Cross-skill conflict and composition rules

1. **Superpowers frames the generic development process, but HDM process owners adapt and constrain it.** Specialist skills execute inside that process and cannot replace or weaken `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`, runtime overlays, approval/review gates, source/evidence requirements, Version Impact Gate, System-Impact Gate, checkpoint/publication rules or other canonical HDM process owners.
2. **Clean Architecture vs SOTA Python:** Clean Architecture is primary for *where responsibilities and dependencies belong*; SOTA Python is primary for *how the accepted structure is expressed idiomatically and safely in Python*. SOTA Python must not move boundaries, introduce framework/persistence coupling, or change architectural ownership merely because a Python pattern/tool would be convenient.
3. **Superpowers/HDM process vs SOTA Python testing:** Superpowers owns the TDD cycle/process and `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` owns HDM implementation/test/review gates. SOTA Python owns Python-specific test mechanics such as pytest usage, Hypothesis mechanics, type/lint integration, and Python test hygiene. `sota-python` references `sota-testing`, but **`sota-testing` is not part of the active HDM skill stack and MUST NOT be auto-loaded or treated as authority unless the Product Owner explicitly adds it later**.
4. **Superpowers/HDM process vs Prompt Optimizer evals:** HDM process owners control when work is researched, designed, planned, criticized, executed, reviewed and accepted. Prompt Optimizer may define prompt-specific eval cases, baselines, candidate comparisons, holdouts and optimization loops *inside* those gates; it cannot create a parallel acceptance process or bypass current HDM evidence/evaluation governance.
5. **Clean Architecture vs Prompt Optimizer:** Clean Architecture is primary for architectural placement and dependency boundaries of prompt/LLM subsystems; Prompt Optimizer is primary for the content structure and evaluation of the instructions carried by those subsystems. Prompt convenience must not collapse an accepted architecture boundary.
6. **Prompt Optimizer vs OpenAI Docs:** OpenAI Docs wins on current factual claims about OpenAI models/APIs/tools and provider-specific behavior. Prompt Optimizer owns how those facts are translated into prompt structure/evals. Vendor recommendations are evidence, not automatic HDM product decisions.
7. **SOTA Python vs OpenAI Docs:** OpenAI Docs wins on OpenAI API/model/tool facts; SOTA Python owns idiomatic Python implementation around those facts, subject to accepted HDM architecture/contracts and runtime/tooling policy.
8. **Clean Architecture scoring is diagnostic only.** It must not reopen or redesign already-authorized HDM architecture merely to improve a Clean Architecture score, satisfy a textbook pattern, or introduce additional ports/DTOs/interactors/abstractions. Report meaningful conflicts and consequences; change accepted architecture only through the controlling HDM process.
9. **SOTA Python defaults are defaults, not project mandates.** Its preferences for `uv`, `pyproject.toml`, lockfiles, a particular type checker, Pydantic, project layout, Python-version features, async patterns, tooling or test setup apply only where consistent with accepted HDM specs/configuration, runtime constraints and repository toolchain owners. In particular, it must not replace the repository-owned `.hdm-devtools/` + `DEV/TOOLS/requirements-dev-tools.txt` development-tool environment or violate the standard-library-only requirement for `GAME/TOOLS/init_campaign.py` merely to satisfy the skill.
10. **Prompt Optimizer cannot alter owned semantics silently.** It may improve wording, layering, model adaptation, examples and evals, but material changes to HDM gameplay behavior, product semantics, evaluation meaning, tool authority, output semantics, prompt/contract ownership or canonical runtime contracts require the owning HDM design/change route.
11. **OpenAI Docs is evidence, not product authority.** Current vendor documentation may invalidate a technical assumption and therefore trigger reconciliation, but it never silently overrides Product-Owner intent or accepted HDM semantics/architecture.
12. If a conflict spans domains, decompose it by decision type using the matrix above. If that still leaves a material unresolved conflict, surface it explicitly through the normal HDM process; do not invent a hidden precedence rule.
13. A skill being active means it is available and mandatory **when its declared scope is relevant**. Do not force irrelevant skills into unrelated work, and do not let one skill's broad trigger wording manufacture scope that the current Task/WP/plan does not authorize.

### Project-specific overrides of generic skill workflows

Local HDM governance controls how generic skill workflows are instantiated. Repository structure, accepted architecture/contracts, runtime overlays, artifact taxonomy, role boundaries, branch/publication rules, design/implementation authorization and current owning process always override generic workflow mechanics.

1. **Bootstrap order is project-owned.** On a fresh HDM session, establish the current remote ref/state, read `AGENTS.md`, and load the applicable runtime overlay before relying on any skill workflow. Superpowers' generic "invoke skills before any action" rule begins after the repository authority needed to select and constrain those skills has been loaded; it does not invert the mandatory HDM bootstrap order.
2. **Do not manufacture duplicate Product-Owner or Senior approval gates.** An explicit Product-Owner authorization or a completed/accepted HDM design, architecture, plan or Senior gate satisfies a generic skill approval requirement for the same already-authorized scope. Continue mechanically inside that scope. A generic skill also cannot waive an HDM-required gate. New product semantics, material architecture choices, scope expansion, explicit risk acceptance, System-Impact Gate events, or other decisions that current HDM owners genuinely reserve for Product Owner/Senior review still follow the owning HDM process.
3. **Generic worktree/branch workflows are subordinate to HDM branch policy and runtime overlays.** No skill may create or require a branch unless the exact branch name and exact base ref have received the approval required by the HDM branch-creation guardrail. No skill may use branch creation as an automatic worktree setup step. Branch/ref deletion remains absolutely prohibited regardless of generic cleanup instructions. Existing/externally managed isolated workspaces may be used only when compatible with the active runtime overlay and current task; otherwise remain on the authorized current ref/workspace.
4. **HDM artifact taxonomy and owner paths override generic skill defaults.** A generic skill may inform plan/design content, but it must not redirect durable HDM artifacts into its own default directories when current HDM owners require `DEV/docs/superpowers/research/`, `design/`, `specs/`, `plans/` or another declared owner path. Repository-root `docs/` or `docs/superpowers/` must not be created for this work.
5. **`DEV/DEVELOPMENT_EXECUTION_PROCESS.md` owns implementation execution.** Generic Superpowers execution menus or handoffs are used only where that process and the applicable runtime overlay leave the choice open. For substantial implementation, the HDM sequence of approved architecture/spec -> implementation plan -> Senior plan review/GO -> autonomous execution -> final Senior integration audit remains controlling; do not introduce extra user-choice menus or alternative acceptance paths unless the current HDM owner requires them.
6. **HDM publication/closure rules override generic branch-finishing workflows.** Generic merge/PR/keep-branch menus, branch cleanup/deletion, worktree cleanup and `finishing-a-development-branch` mechanics apply only where explicitly compatible with the current HDM publication/closure owner and branch policy. They must never delete a branch/ref, bypass coherent checkpoint publication/read-back, replace a required Senior gate, or move work to another ref without authorization.
7. **Mechanical repair follows HDM autonomous execution rules.** In-scope RED/GREEN iterations, test failures, lint/type failures, bounded plan corrections, ordinary debugging, review findings and mechanically resolvable verification defects are handled autonomously when the current role/task/process authorizes the repair. A generic skill instruction to stop and ask does not by itself create a Product-Owner/Senior stop. Stop/escalate when `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`, another controlling HDM process, a human/safety gate, or insufficient accepted architecture/specification requires it.
8. **Testing examples do not become competing test strategy.** Superpowers owns the TDD process; accepted HDM specs and `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` own required behavior, verification scope and escalation. Clean Architecture test examples and SOTA Python pytest/Hypothesis guidance are secondary domain mechanics. Generic advice to mock ports, prefer fakes, choose integration boundaries, randomize tests, add property tests, add a new test dependency, or restructure the suite must be reconciled with the owning HDM test/verification plan rather than treated as an independent mandate.
9. **Specialist scores and severities are diagnostic, not gate authority.** Clean Architecture scores and SOTA Python `CRITICAL/HIGH/MEDIUM/LOW/INFO` labels may be preserved as source-skill diagnostics, but any finding affecting HDM execution must be reconciled into the current HDM critic/review/Senior severity, disposition and gate semantics. A specialist label never advances, blocks, reopens or closes HDM work by itself.
10. **Prompt deduplication is not permission to remove deliberate defense-in-depth.** Prompt Optimizer's "one owner per behavior rule" and deduplication guidance is the default for accidental duplication. Repeated enforcement may remain when independent runtime layers, GAME boundaries, tool boundaries, degraded/fallback paths, safety/fail-closed behavior, or independently consumed artifacts require local protection. Do not remove such redundancy without proving behavioral equivalence through the owning HDM contract and appropriate evals/tests.
11. **Skill command examples do not grant mutation authority.** Commands or recommendations inside a skill do not by themselves authorize installing/upgrading dependencies, replacing the repository toolchain, changing requirements/lock/configuration files, running broad auto-fix operations, modifying unrelated files, adding infrastructure, changing runtime dependencies, using destructive commands, or widening network/tool access. Such mutations require authorization from the current HDM task/plan/owner and must stay inside its write scope and runtime overlay. Read-only diagnostics may be used only where the current runtime/role permits them.
12. **Vendored skills are not authoritative sources for mutable external facts.** Version numbers, release status, library/framework behavior, tool capabilities, performance claims, provider behavior and other time-sensitive assertions embedded in a vendored skill must be fresh-verified against current primary documentation before they drive architecture, implementation, compatibility or tooling decisions. Use OpenAI Docs for current OpenAI-specific facts; use the relevant official/primary source for Python, SQLite and third-party tooling. If a mutable claim cannot be verified, record that limitation rather than promoting it to HDM fact.
13. **Companion-skill recommendations do not expand the active stack.** A skill may mention another skill, but that mention does not install, activate or grant authority to the companion. The active skill stack changes only through this file and explicit Product-Owner/project-governance changes.

The `.agents/` tree is development-only repository infrastructure. Runtime GAME content must not depend on it or ship it as gameplay context.

## Fresh development-session bootstrap

A fresh development chat/session must recover current project state from the repository before doing substantive analysis, proposing architecture, or asking the repository owner to restate information that is already recoverable from project sources.

For architecture/deep-work activity, use this bootstrap order:

```text
current remote ref/state
-> AGENTS.md
-> applicable runtime overlay
-> applicable Superpowers process skill(s)
-> applicable specialist skill(s): Clean Architecture / SOTA Python / Prompt Optimizer / OpenAI Docs
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> DEV/CURRENT_PROGRESS.md
-> DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md when sequencing/scope detail is needed
-> task-specific owning artifacts and relevant evidence
```

At minimum:

1. determine the active branch/ref and current repository state using the applicable runtime overlay;
2. read the current `AGENTS.md` and applicable runtime overlay on that state;
3. after the project-owned bootstrap has established the applicable repository authority, load the applicable Superpowers process skill(s) and every specialist skill whose declared scope is relevant to the authorized task; a runtime that does not auto-discover `.agents/skills/` must read the relevant project-local `SKILL.md` explicitly; for OpenAI-specific work use the runtime's supported official-documentation route;
4. read the current applicable design-process files rather than relying on remembered versions;
5. read `DEV/PROJECT_MAP.md` and use it to identify the task-specific ownership/dependency route;
6. read `DEV/CURRENT_PROGRESS.md` for global current state and the next authorized unit when the task is architectural;
7. read `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` when sequencing, scope or dependencies need detail;
8. inspect the actual owning artifacts and relevant neighboring consumers before making correctness-sensitive claims.

Conversation history, model memory, handoff summaries, prior-agent summaries, search snippets and derivative indexes may accelerate orientation, but they are not substitutes for current repository evidence when the owning source is available.

Do not make the repository owner reconstruct repository topology, previous decisions, document contents, accepted constraints, or current stage state that the agent can establish from the repository itself.

## Development design process

Before architecture, system design, deep technical research, or other development work whose scope may affect architecture:

1. read and follow `DEV/DESIGN_PROCESS.md`;
2. for HDM architecture work, also read and follow `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

`DEV/DESIGN_PROCESS.md` is the canonical general development/design process. `DEV/ARCHITECTURE/DESIGN_PROCESS.md` is the project-specific HDM adapter and adds constraints; it does not replace or weaken the general process.

Do not rely on remembered versions of these rules. Read the current files on the active branch before substantive architecture/deep-work activity.

## Implementation execution process

For implementation after an approved architecture/specification or approved bounded design, read and follow `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` before production-code changes.

That file is the canonical HDM implementation-execution process. It owns the additional project rules for:

- `superpowers:writing-plans`-based implementation planning for substantial work;
- the Implementation Impact Envelope and its Senior plan-review gate;
- autonomous TDD/task execution after GO;
- task/code-review automation when subagents are available;
- coherent checkpoint publication and durable execution cursors;
- the System-Impact Gate and its exact escalation triggers;
- final verification and Senior integration audit.

Do not paste this entire process into delegated worker prompts. Workers are expected to bootstrap from the repository and read the current process owner. Delegated prompts should contain only the task-specific delta, expected current ref/cursor when useful, task-local constraints that are not already owned by repository process, and required return evidence.

A normal test failure, local bug or mechanically resolvable implementation detail is not a reason to stop for Senior approval. A worker stops during approved execution when `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` identifies a real system-impact escalation, when another existing mandatory human/safety gate fires, or when the approved plan/spec no longer provides a trustworthy path forward.

## Documentation evidence and synthesis discipline

Repository documentation volume is an **agent workload problem**, not a human proofreading obligation.

The agent is responsible for discovering the relevant source set, reading it to the depth required by the claim, preserving material qualifiers, reconciling it with current owners, and checking completeness before synthesis. The repository owner should receive decision-ready conclusions and genuine architectural trade-offs, not a request to manually verify whether the agent missed something in a large document corpus.

Hard rules:

- `DEV/PROJECT_MAP.md`, `CANONICAL_ARCHITECTURE_INDEX.md`, roadmaps, summaries, executive syntheses, search results and conversation summaries are routing/compression aids. They do not replace actual owning artifacts for correctness-sensitive conclusions.
- Do not claim architecture, roadmap, requirement, research or review coverage from thematic overlap, representative sampling, remembered content, headings, or an executive summary when the underlying relevant source material is available.
- When a source contains individually enumerated requirements, findings, risks, review issues, candidates, test cases, schema members, deferred items or similar records, preserve item-level semantics where the task depends on coverage. A broad statement such as "the themes are covered" is not evidence that the set is accounted for.
- Qualifiers are part of the evidence. Conditions such as scope limits, confidence, exceptions, non-goals, `revisit when`, defer triggers, negative findings and applicability constraints must survive extraction and synthesis.
- For deep work, use the source-manifest / evidence-extraction / completeness gates defined by `DEV/DESIGN_PROCESS.md` and the HDM-specific rules in `DEV/ARCHITECTURE/DESIGN_PROCESS.md` before producing a roadmap, Decision Brief, candidate specification, coverage claim or canonicalization result.
- A large repository does **not** imply preloading or rereading the entire repository for every task. Use `DEV/PROJECT_MAP.md` to identify the relevant dependency subgraph, then exhaust that task-specific source set to the degree necessary for the claims being made.
- Do not ask the human architect to compensate for incomplete document research. Escalate only the residual product semantics, priorities, material trade-offs, risk acceptance or other decisions that genuinely require human judgment.

## Repository ownership geometry

The source repository has two product ownership trees:

- `GAME/` — exact source tree of the installed runtime distribution. The release builder archives the **contents** of this directory.
- `DEV/` — architecture, tests, release policy, development catalogs/schemas, Superpowers artifacts and developer tooling.

Repository root is reserved for repository infrastructure/metadata such as `.github/`, `.agents/`, this `AGENTS.md`, root `README.md`, `.gitignore` and canonical legal files.

Do not recreate old repository-root product/development directories such as `CORE/`, `TESTS/`, `TOOLS/`, `ARCHITECTURE/`, `RELEASE/`, `CATALOG/`, `SCHEMA/`, `SCHEMAS/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/`, `INSTALL/` or `docs/`.

## Root README editorial contract

The repository-root `README.md` is a **manually curated public-facing document owned by the repository owner**. It is not ordinary development documentation and must not be treated as a convenient place to dump technical state.

### Do not modify it opportunistically

Do **not** rewrite, reorganize, condense, expand, modernize, clean up, normalize, re-template or otherwise reshape the root `README.md` as a side effect of architecture work, repository moves, release/version changes, refactors, path migrations, tooling changes, audits or other unrelated implementation work.

Do not perform broad/global path replacements in the root README. Do not replace the whole file merely because one link, path or statement became stale.

Treat the existing wording, tone, jokes, pacing, whitespace, visual separators, section ordering, legal framing and closing text as intentional editorial choices.

### Required editorial structure

Preserve this high-level structure unless the repository owner explicitly asks to change it:

1. **Legal/disclaimer header** — project independence / Wizards of the Coast and trademark framing at the top.
2. **Friendly human-facing section** — approachable explanation of what the project is, why it is interesting and how it feels to use; this is the primary public face of the repository.
3. **Quick start** — concise installation/start instructions written for a normal user.
4. **Intentional visual separation** before the technical-interest section.
5. **`Подробности для нёрдов` section** — conceptual architecture and implementation-relevant explanation for technically interested readers, but still written as readable public documentation rather than internal engineering notes.
6. **License / third-party legal footer and friendly closing sign-off**.

The nerd section may explain concepts such as GAME/DEV separation, storage, releases and high-level architecture, but it must not become a dump of internal technical debris: no audit logs, CI minutiae, debugging history, temporary implementation details, maintenance-process chatter, low-level agent workflow, internal checklists or other material that belongs under `DEV/`.

### Technical changes do not automatically authorize README edits

If a technical change makes a README statement, path or link inaccurate, **report the exact mismatch to the repository owner instead of silently rewriting the README**.

Only edit the root README when the repository owner explicitly asks for, or explicitly approves, a README change as part of the current task. When such an edit is authorized:

- make the **smallest targeted patch** needed;
- preserve the surrounding voice, structure, formatting and editorial rhythm;
- do not use the opportunity to rewrite adjacent text;
- keep the friendly section friendly and the nerd section readable;
- do not introduce internal implementation clutter merely because it is technically accurate.

Direct edits made by the repository owner to `README.md` are authoritative. Do not revert them to an older version, regenerate them from another source or "restore" a previous agent-authored variant unless explicitly asked.

The root README is **not machine-authoritative metadata**. Detailed architecture, release policy, tests, implementation plans and maintenance procedures belong under `DEV/`; runtime contracts belong under `GAME/`. The README should summarize only what is useful to human readers.

## Superpowers artifacts

All Superpowers research, design and implementation artifacts for this repository are development-only.

Use only:

```text
DEV/docs/superpowers/research/
DEV/docs/superpowers/design/
DEV/docs/superpowers/specs/
DEV/docs/superpowers/plans/
```

Placement semantics:

- `research/` — durable research findings, experiment results, measurements, feasibility/comparative investigations, exploratory ideas/dossiers and other standalone evidence whose value is primarily **what was learned, measured or discovered**. Research remains evidence, not architecture authority merely because it is retained here.
- `design/` — design-process and provenance history: Task Briefs, scope discovery, Source Manifests and evidence-working artifacts, pre-acceptance Decision Briefs, critics, collaborative reviews, candidate specs, resolution gates, intermediate Step-1…8 artifacts, process-history closure/canonicalization evidence, audit mini-reports/status/cursors, rejected or superseded proposals, and other records whose value is primarily **how the accepted result was reached**.
- `specs/` — the compact final implementation-facing corpus: final approved specifications, accepted canonical amendments, final accepted owner decisions and other final documents actually needed by downstream planning/implementation to know what is accepted, required, forbidden, deferred or excluded. `specs/` is not an archive of the whole design workflow.
- `plans/` — implementation plans produced after approved designs.

Eight-step design output routing follows the semantic role of the artifact, not its filename or Step number:

```text
standalone research / experiment result
    -> research/

Task Brief / Source Manifest / working evidence / pre-acceptance Decision Brief /
critic / collaborative review / candidate / resolution / process-history closure
    -> design/

final accepted implementation-facing specification / canonical amendment /
final accepted owner decision
    -> specs/

implementation plan
    -> plans/
```

One source file need not remain one destination file. If an artifact mixes reusable research findings, design provenance and final accepted law, split it when that materially improves taxonomy or downstream discoverability. Before demoting an intermediate/research artifact that is the only current carrier of accepted implementation-relevant semantics, promote/consolidate those exact semantics into the appropriate final spec or durable architecture owner. Do not leave hidden current authority stranded only in `design/` or `research/`, and do not create duplicate normative copies.

Implementation planning should normally begin from current durable architecture owners plus `DEV/docs/superpowers/specs/`. Read `design/` or `research/` when provenance, reopening, unresolved evidence, applicability or audit requires it; do not bulk-read those histories merely to reconstruct already accepted architecture.

`DEV/docs/superpowers/README.md` is the short non-authoritative navigation entry point for this taxonomy.

Do **not** create repository-root `docs/superpowers/` or repository-root `docs/` for Superpowers work. Historical paths that are accurate parts of a historical statement need not be mechanically rewritten, but every current live routing/reference must point to the current location.

## Transient development branches in documentation

The active development branch/ref is session-specific repository state, not architecture semantics.

Do not write transient feature/research branch names into durable architecture, status, roadmap, contract, research, specification or implementation-plan documents as `Target`, `Target branch`, `Target development branch`, or equivalent working metadata. Determine the active ref from the repository at work time instead.

Record an exact branch/ref only when that identity is itself material evidence needed to reproduce or interpret a historical experiment, Git operation, release/provenance event, migration, comparison or failure. Accurate historical provenance must not be rewritten merely because later work moved to another branch.

## Branch creation guardrail

Remote branch creation is **prohibited by default**.

Never create a branch for probing, discovery, existence checks, temporary work, no-op operations, tool testing, recovery, uncertainty resolution, or as a substitute for a read-only ref query.

Never create disposable or placeholder branches with names such as `temp-*`, `do-not-use`, `noop`, `no-op`, `stop`, `scratch`, `test`, `ignore-me`, or equivalent variants.

A remote branch may be created only when the repository owner has explicitly requested a new branch or has explicitly approved the **exact branch name and exact base ref** for the current task.

Before any remote branch-creation action, the agent must state the exact intended branch name and base ref and obtain explicit owner approval. A general request to modify files, continue development, work on the current branch, or inspect repository state is not branch-creation approval.

Branch creation is effectively irreversible for HDM automation because branch/ref deletion is prohibited by policy, independent of tool availability. This makes branch creation an especially high-risk write and never an acceptable experiment or discovery operation.

### Absolute branch/ref deletion prohibition

Branch/ref deletion is **prohibited absolutely** for all HDM development agents and automation.

Never invoke a branch/ref-delete command, API, Connector action, native Git operation, script, wrapper or equivalent capability. This prohibition applies to cleanup, testing, migration, repair, stale/orphan refs, absorbed live refs, repository maintenance and every other HDM-controlled operation, regardless of repository permissions or technical tool availability.

A later task instruction, write authorization, branch ownership or repository Admin/Write permission does not override this prohibition. Only a later explicit Product Owner policy decision that supersedes `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md` may change it.

Use routing/currentness to make a branch non-authoritative; leave the ref physically present. Out-of-band human repository administration is outside HDM automation.

Use read-only operations for branch/ref discovery and verification, including branch search, current-file reads on a named ref, commit/ref comparison, and other Connector read surfaces. A create/write operation must never be used to answer a read-only question.

When an active development branch/ref is already specified, all ordinary reads and writes remain on that ref unless the repository owner explicitly changes the target.

For the current HDM rearchitecture program, the active development target is `v1/engine-rearchitecture`. Do not create another branch unless the repository owner explicitly requests or approves it under the rule above.

## Runtime-specific remote transport and verification

The required outcome is environment-independent: a correctness-sensitive repository write starts from verified current remote state, publishes without force, and is followed by an independent read-back. The applicable runtime overlay owns the exact transport commands/tools.

- A local tracking ref, stale checkout, cached API response or unrefreshed branch is not evidence of current remote state.
- A local commit is not evidence of remote publication.
- A verification result is valid only for the execution surface that actually ran it. Do not claim a hosted-CI, local-test or remote-read-back result that the current runtime could not obtain.
- When a required transport or execution surface is unavailable, report that as unavailable evidence; do not silently substitute a weaker source or fabricate PASS.

## Version metadata and mandatory Version Impact Gate

`DEV/RELEASE/VERSIONING.md` is the compact canonical versioning policy projection; its detailed semantic owner is the versioning specification it references.

- `DEV/ENGINE_DEVELOPMENT.yaml` is the complete development/release bookkeeping record.
- `GAME/ENGINE_VERSION.yaml` is the minimal installed-package/runtime projection.
- Shared fields must stay equal; builder/audit enforce this.
- `ENGINE_VERSION.yaml` must remain unique in the tracked repository so runtime package-root discovery is unambiguous.

Runtime GAME files read package metadata only from package-root `ENGINE_VERSION.yaml`; they never read DEV metadata.

**Every repository change MUST perform a Version Impact Gate before the change is treated as checkpoint-ready or complete.** This applies even when the final result is `VERSION_IMPACT: NONE`.

For the actual changed owner/consumer set, the worker must:

1. identify every changed current semantic/machine/runtime/schema/catalog/protocol/module owner or projection that belongs to, carries, or consumes an HDM-owned version/revision/schema/generation namespace;
2. classify the change under the owning bump rule in `DEV/RELEASE/VERSIONING.md` and its detailed canonical owner;
3. determine whether a bump is required for each affected namespace;
4. when a bump is required, update the owning value and every required projection/consumer atomically in the same coherent checkpoint;
5. when no bump is required, verify that the edit is non-material under that namespace's bump rule rather than assuming "no version change" from file type or diff size;
6. include the result in review/completion evidence as `VERSION_IMPACT: NONE` or a concise list of affected namespaces and old -> new values.

A version-bearing change is **not complete** while a required version/revision/schema/generation bump or required projection synchronization is stale. Updating a version header/value is part of the same logical change and does not itself create an additional bump.

Machine validation is a backstop, not a substitute for this semantic assessment: CI can detect many stale/mixed projections but cannot reliably infer whether every human-authored semantic edit was material.

## Development tools

Canonical DEV entry points:

```text
DEV/TOOLS/run_maintenance_audit.py
DEV/TOOLS/run_release_build.py
```

Both own/reuse the isolated repository-local `.hdm-devtools/` environment declared by `DEV/TOOLS/requirements-dev-tools.txt`. Do not install DEV dependencies into system Python and do not make GAME/runtime depend on them.

`GAME/TOOLS/init_campaign.py` is runtime support and remains Python-standard-library-only.

## Release boundary

`DEV/TOOLS/run_release_build.py` is the single authority for runtime package validation/composition, deterministic ZIP creation, asset naming and checksum creation. GitHub Actions must not maintain a second include/exclude list or duplicate builder dependency logic.

The supported install artifact is `hedgelion-dnd-master-runtime-v<version>.zip`. GitHub-generated source archives are repository snapshots and are not gameplay packages.

## Execution and verification surfaces

Runtime overlays define the available local tools, remote transport and hosted-CI visibility. Use the strongest verification available in the current runtime and record the actual surface. Hosted CI is an additional acceptance surface when it is available; it is not an excuse to skip required local validation, and unavailable hosted CI is not a passing result.

## Development versus gameplay

Development instructions, tests, release policy, catalogs under DEV and maintenance tooling must never be copied into gameplay prompts or runtime CORE context. GAME runtime behavior is defined only by the installed package and campaign storage contracts.

## Delegated-task prompt discipline

Standing project rules belong in repository instructions and process owners, not in every delegated task prompt.

When one development agent delegates work to another agent/chat/session:

- assume the worker will perform the required fresh-session bootstrap and read the current `AGENTS.md` plus applicable process files;
- do **not** repeatedly paste transport policy, branch-creation rules, evidence/completeness rules, decision-rights rules, repository ownership geometry, Superpowers requirements, the generic checkpoint protocol, or `DEV/DEVELOPMENT_EXECUTION_PROCESS.md` when the repository already owns them;
- make the delegated message carry the **task-specific delta**: exact goal, expected current ref/cursor when useful, task-specific owning artifacts, concrete task-local constraints, material stop conditions, and required return evidence;
- restate a standing rule only when the current task introduces an exception, a narrower task-specific interpretation, or a known failure mode that makes the generic rule insufficiently precise;
- use concrete public repository terminology. Do not depend on private audit shorthand, metaphors, or labels that the worker cannot recover from the public repository sources.

A delegated prompt must remain sufficient to identify the requested work, but it should not become a second copy of `AGENTS.md`, the design-process documents, or the implementation-execution process. Repository-owned standing instructions are the durable/canonical place for recurring agent behavior.

## Coherent checkpoint commit discipline

For any large or interruption-prone development/implementation task, **do not wait until the entire assignment is finished before publishing progress** when a coherent verified slice is already complete.

The required pattern is:

```text
fresh current remote state
-> complete one coherent slice
-> run the focused verification that proves that slice
-> inspect the delta for partial migration / scope creep
-> commit
-> publish on the active ref without force
-> remote read-back
-> continue from the published HEAD
```

A slice is checkpoint-ready only when:

1. it is internally coherent and follows current owners;
2. its relevant focused tests/validation pass, or any unavailable verification is explicitly recorded rather than silently treated as PASS;
3. the published repository is not intentionally left in a broken or half-migrated contract state;
4. the checkpoint does not leave parallel old/new authority, partially synchronized identity carriers, producer/generated-artifact disagreement, or another state that necessarily requires hidden uncommitted work to be valid;
5. another agent could safely continue from that published HEAD without reconstructing hidden conversation-local work.

Good checkpoint boundaries include a complete schema+producer+test change, one fully synchronized migration, one independently complete implementation-plan task, one reconciled failure class, one coherent machine-contract realization, one completed evidence slice, or one status/canonicalization synchronization.

Do **not** create artificial micro-commits after arbitrary file counts or time intervals. Coherence and recoverability define the boundary.

### Interruption / exhaustion behavior

If context, message, credit, execution-time, or other practical limits are approaching:

```text
finish the nearest safe coherent slice
-> verify
-> publish
-> remote read-back
-> record exact continuation state
```

The continuation state should identify at least:

```text
LAST_PUBLISHED_SHA
COMPLETED_SLICES
CURRENT_VERIFICATION_STATE
NEXT_EXACT_TASK_OR_SLICE
KNOWN_BLOCKERS
UNPUBLISHED_WORK: NONE | exact description
```

If unfinished local work is in an unsafe midpoint and cannot be published coherently, explicitly identify the last safe published SHA and the unpublished state. Do not imply that uncommitted/chat-local work is durable project state.

Durability of completed work is part of execution quality. A long task may therefore produce several good commits before its final task-level completion claim.
