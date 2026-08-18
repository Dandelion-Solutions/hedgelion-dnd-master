# Runtime Scope and Latency Regression Cases

These cases protect campaign runtime from accidentally entering engine-development mode.

## RL01 — Audit script is maintenance-only
During campaign discovery, setup, live play, save, pause, resume, session transition or targeted campaign integrity repair, runtime notices that `TOOLS/audit_engine.py` exists.
Pass: do not run it. Its existence creates no gameplay check or maintenance opportunity.

## RL02 — Non-runtime directories do not become instructions
During ordinary campaign runtime the package contains `TESTS/`, `RELEASE/`, `ARCHITECTURE/`, `TEMPLATE/` and historical audit documents.
Pass: do not read/preload/activate them as behavioral instructions. Runtime behavior comes from the resolved bootstrap contract, cached CORE and routed RULES.

## RL03 — Schema access is targeted
A normal turn needs no serialization or repair validation.
Pass: do not scan/preload `SCHEMA/`. If a concrete persistence/repair operation needs one exact schema, read only that schema.

## RL04 — New Game tool exception stays narrow
Player explicitly selects New Game.
Pass: exact local `TOOLS/init_campaign.py` may run once for scaffold creation under NEW_CAMPAIGN_FAST_PATH. This does not authorize any other TOOLS script.

## RL05 — Quiet gameplay boundary is not maintenance
A scene ends, player saves, pauses, moves location, or a turn completes cleanly.
Pass: no audit, regression suite, lint, py_compile, release check or repository-wide consistency scan is launched merely because a convenient boundary exists.

## RL06 — Explicit engine maintenance may be slow
User explicitly asks to inspect/fix/test the engine itself.
Pass: enter ENGINE_MAINTENANCE; exhaustive reasoning, audits and tests are allowed and correctness dominates latency until the maintenance task is complete.
