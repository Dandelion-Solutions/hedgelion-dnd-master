# Global Current-Progress Authority

Status: **ACCEPTED PUBLIC MAINTENANCE DESIGN**

## Decision

`DEV/CURRENT_PROGRESS.md` is the single authoritative surface for HDM's
global current state, active work, next authorized unit and required gate.

It uses a compact Markdown record with a closed, human-readable field set.
It contains no transient branch identity or working SHA.

## Authority boundaries

- The current-progress authority owns global program state only.
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` owns intended sequence, scope and
  dependencies; it is not a mutable global cursor.
- A task-local execution/audit cursor may preserve bounded recovery state, but
  must state its local scope and defer global state/gates to the current-progress
  authority.
- Canonical indexes, reports and historical closure records remain navigation,
  semantic ownership or historical evidence according to their existing roles.

## Maintenance rule

Advance the compact current-progress record when global state or authorization
changes. Do not rewrite a roadmap, derivative index or history merely to copy
that movement. The maintenance audit guards the routing and identified
non-authority disclaimers.
