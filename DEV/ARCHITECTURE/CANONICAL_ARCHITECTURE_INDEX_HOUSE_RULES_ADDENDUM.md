# Canonical Architecture Index — Campaign House Rules Addendum

Status: **DERIVATIVE / NON-NORMATIVE / HOUSE RULES CURRENTLY ON STEP 2–3 HOLD**

Date: 2026-08-25

This addendum is navigation only. It creates no semantic authority and currently records a **reopened design gate**, not canonical House-Rules closure.

Current gate/status owner:

- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-senior-audit-reopen-hold.md`

Current design sources:

- Step 1 — `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md` — PRESERVED;
- Step 2 audit delta — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md` — COMPLETE;
- Step 3 amended Decision Brief — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md` — HUMAN DECISION REQUIRED.

The earlier Step-4..8 artifacts and `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` are attempted-closure/candidate material while the HOLD is active. Do not route from their old `CANONICAL/CLOSED` labels without first reading the current HOLD and amended Step-3 gate.

Runtime-facing campaign policy surface:

- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` — retained only as the shipped purpose/limit projection; it does not establish adoption authority or implementation completeness.

Current richer adjudication machine-contract surfaces:

- `DEV/CATALOG/mechanical-surfaces.json` — boolean registered invocation facts remain unchanged;
- `DEV/SCHEMAS/activity-parameter-spec.schema.json` — bounded richer adjudicated parameter declarations;
- `DEV/SCHEMAS/activity-parameter-binding.schema.json` — accepted richer adjudication evidence;
- `DEV/SCHEMAS/action-request.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
- `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
- `DEV/SCHEMAS/resolution-receipt.schema.json`;
- `DEV/TESTS/test_house_rules_adjudicated_input_contract.py`.

Preserved inherited owners still include:

- Step-4 truth/knowledge/disclosure + role-context contracts;
- R2.3 bounded Context Runtime;
- R2.4 role rebinding/instruction-data fencing;
- Step-5.6/5.7/5.8 publication/recovery/currentness;
- R2.5 multiplayer collaboration/current-frontier rules;
- Activity / Rule Element / Step-3 deterministic execution owners.

Current program routing:

```text
HOUSE RULES STEP 1  PRESERVED
HOUSE RULES STEP 2  REPAIRED
HOUSE RULES STEP 3  HUMAN DECISION GATE
STEP 4..8           BLOCKED
S6D                 BLOCKED / NOT STARTED
R2.7 WP-06          PAUSED
```

Residual R2.3 navigation debt remains unchanged: the semantic owner exists at `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`; the convenience path `DEV/ARCHITECTURE/CONTEXT_RUNTIME.md` is absent.
