# OpenCode runtime overlay

OpenCode loads this file and `LOCAL_MACHINE.md` through the project `opencode.json`; `AGENTS.md` remains the repository-wide core.

- Use the native local-machine transport and verification procedure from `LOCAL_MACHINE.md`.
- Superpowers is installed in this environment. Use the applicable available Superpowers skill before relevant work; do not assume ChatGPT Work-only skills, Connector tools or hosted-CI visibility exist.
- Do not run OpenCode `/init` against this repository: `AGENTS.md` is maintained deliberately and is not a generated summary.
- Select models/effort appropriate to the task, but do not allow a lower-cost model to bypass the repository's evidence, design, approval or verification gates.

## Coordinator, delegation and model selection

The coordinator owns the dependency graph, accepted checkpoint applicability, task assignments, integration, durable cursor and publication. Execute every currently eligible task in the authorized continuation scope until completion or a real gate; a checkpoint is a recovery boundary, not a request to continue. A held lane does not block a semantically independent lane whose own inputs and permissions are satisfied.

Use native OpenCode subagents when they reduce serial work: bounded source extraction, disjoint eligible implementation tasks, and independent review of a frozen candidate. Do not create an agent for a trivial edit or make every logical role a separate model call. Default profiles are capability preferences, not claims about models enabled on this VPS:

| Work | Preferred starting profile | Escalation |
|---|---|---|
| Bounded read-only extraction, exact source inventory, mechanical checking | Luna, low/medium | Sol when semantic synthesis or ambiguity is material |
| Accepted implementation, TDD and local repair | Sol, medium | Sol high for difficult interacting contracts |
| Independent spec/quality review | Sol, high | Astra for cross-owner authority/System-Impact review |
| Senior technical review or genuinely difficult architecture synthesis | Astra, high | Higher effort only when a concrete unresolved risk justifies it |

Inspect actual provider/model/variant availability at session bootstrap. If a preferred profile is absent, choose an available capability-equivalent profile; record material limitations. Do not persist a cheaper replacement that weakens accepted verification. Conversely, do not default every task to maximum effort. Fixed profile choices are overridable by the coordinator within available capabilities.

Each assignment contains: task/role; pinned base; bounded primary-source manifest; allowed paths and workspace; expected result/proof; accepted dependency inputs; escalation conditions. Do not copy the full repository/process corpus into each prompt. Reuse a task agent for bounded repair/follow-up when its provenance is still current; use a different agent for independent review. Review only a frozen candidate, record its exact SHA/byte identity, and invalidate the affected review if later changes alter its scope.

Parallelism follows semantic dependencies and physical ownership. Read-only independent work may run together. Production preparation may run together only with disjoint physical writers or isolated task workspaces; overlapping shared files have one final integrator. Serialize shared-index operations, final integration and publication. Bound concurrency to measured CPU/memory/tool/provider capacity and task value; retry/rate-limit contention is a reason to reduce it. Do not nest delegation mechanically.

Technical Senior gates may be routed to an independent qualified agent when the current process authorizes that role; preserve its evidence/ruling and required publication/read-back. Neither implementer self-review nor a profile name constitutes Senior approval. A real product-semantics, priority, material trade-off or explicit risk-acceptance question belongs to the human. If an indispensable technical reviewer/tool is unavailable, record that capability blocker without fabricating acceptance; continue only independent permitted work.

## Verification economy

Use focused tests in the RED/GREEN loop. Run every exact owning acceptance command on the final coherent candidate; share unchanged proof where scope and source identity make it applicable. Parallel independent spec and quality reviews of the same frozen bytes are allowed. After repair, rerun/review the affected scope and required integration, rather than restarting unrelated completed research. Full suites/builds remain mandatory at the boundaries named by owners, not after each local command.

External-directory access is limited by opencode.json; the task scratch exception is not general access to the VPS. Shell pattern guards supplement repository policy, not a security proof against arbitrary scripts. Do not read secrets or bypass a denied operation.
