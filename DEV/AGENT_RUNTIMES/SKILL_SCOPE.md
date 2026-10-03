# HDM development skill scope and workflow overrides

This is the repository-owned detailed skill adapter, extracted without semantic change from `AGENTS.md`. Read it when selecting an applicable skill or resolving a workflow/scope conflict; it is development-only and is not shipped GAME context.

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

