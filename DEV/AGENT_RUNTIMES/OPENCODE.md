# OpenCode runtime overlay

OpenCode loads this file and `LOCAL_MACHINE.md` through the project `opencode.json`; `AGENTS.md` remains the repository-wide core.

- Use the native local-machine transport and verification procedure from `LOCAL_MACHINE.md`.
- Superpowers is installed in this environment. Use the applicable available Superpowers skill before relevant work; do not assume ChatGPT Work-only skills, Connector tools or hosted-CI visibility exist.
- Do not run OpenCode `/init` against this repository: `AGENTS.md` is maintained deliberately and is not a generated summary.
- Select models/effort appropriate to the task, but do not allow a lower-cost model to bypass the repository's evidence, design, approval or verification gates.
