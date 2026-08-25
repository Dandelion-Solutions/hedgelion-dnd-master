# S6D-03 — Complete Calculation Selector Metadata — Decision Brief

Status: **STEP 3 COMPLETE — NO HUMAN DECISION REQUIRED**

Date: 2026-08-25

## Established facts

- Exact accounting covers 34 selectors and 26 operations.
- Only `health.maximum`, `resource.capacity`, `condition.applicability`, `rule.add_flat` and `rule.immunity` have current closed supported semantics.
- Structural tests and JSON-Schema examples are not catalog-aware executable consumers.
- Recovery/duration/cost/damage and other portable-shape pairs cannot be complete before S6D-05 semantics exist.
- Invocation fact allowlisting must name exact fact IDs; the current active selectors require none.
- Dependency kinds and dependency references are distinct.

## Recommendation

Adopt a three-selector/two-operation selectable surface with complete exact metadata. Demote two previously active selectors and five previously active operations to dormant; do not activate any example-driven ID.

Final catalog totals: 450 active, 35 embedded, 86 dormant, 0 stale.

## Human gate

None. This is the conservative technical consequence of current owners and evidence law. It avoids choosing unsupported rules semantics.
