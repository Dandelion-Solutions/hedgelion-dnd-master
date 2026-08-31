# Current-Progress Authority Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`[ ]`) syntax for tracking.

**Goal:** Consolidate HDM global progress into one compact authority without erasing roadmap, task-local or historical roles.

**Architecture:** `DEV/CURRENT_PROGRESS.md` owns global state/gates. Roadmap and index retain sequencing/navigation; the R2.7 cursor remains task-local. A maintenance-audit check and focused unit test prevent the identified duplicate-authority regression.

**Tech Stack:** Markdown, Python standard-library `unittest`, existing `DEV/TOOLS/audit_engine.py`.

**Spec:** `DEV/docs/superpowers/specs/2026-08-31-current-progress-authority-refactor.md`

## Global Constraints

- No public HDM file may mention the private audit workspace.
- Global progress must have one authority; task-local cursors remain subordinate.
- Branch/ref identity is not durable progress semantics.
- Local VPS verification is required before the refactor can be closed.

---

### Task 1: Add the global owner and regression guardrail

**Files:**

- Create: `DEV/CURRENT_PROGRESS.md`
- Create: `DEV/TESTS/test_current_progress_authority.py`
- Modify: `DEV/TOOLS/audit_engine.py`

- [ ] Define the closed global-progress record and its authority boundary.
- [ ] Add a focused test that requires the owner, required fields, bootstrap routes and non-authority disclaimers.
- [ ] Add the same targeted assertions to the maintenance audit.
- [ ] Run locally on the VPS: `python -m unittest discover -s DEV/TESTS -p 'test_current_progress_authority.py' -v` and `DEV/TOOLS/run_maintenance_audit`.

### Task 2: Migrate competing current claims and bootstrap routes

**Files:**

- Modify: `AGENTS.md`, `DEV/PROJECT_MAP.md`, `DEV/DESIGN_PROCESS.md`, `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- Modify: `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`, `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`
- Modify: `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`

- [ ] Route fresh architecture bootstrap through `DEV/CURRENT_PROGRESS.md`.
- [ ] Remove global current-state claims from roadmap and derivative index.
- [ ] Retain the R2.7 record as an explicitly task-local cursor.
- [ ] Run the focused unit test and maintenance audit locally.
- [ ] Perform an independent local audit in a fresh OpenCode session before Senior closure.
