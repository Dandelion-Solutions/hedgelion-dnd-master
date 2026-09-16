# W01.T07 schema lexical validation - implementation impact brief

TRIGGER: generic Draft 2020-12 validation accepts JSON `1.0` for a schema field declared as integer constant `1`, while the W01.T07 Python ingress validators reject it.
LAST_SAFE_SHA: `e9c71885e14ebdfc2119d8950cd6eddf464818d3`
CURRENT_TASK: W01.T07 - Native history, Story root and static selection

## Approved expectation

W01.T07 creates owner-local v1 schemas and validators that fail closed on unsupported newer schemas. The task does not admit a generic schema-validation capability, a lexical JSON-number policy, or a dependency on the existing S6D compiler validator.

## Discovered pressure

Under standard Draft 2020-12 numeric semantics, `{"type": "integer", "const": 1}` accepts `1.0` because JSON Schema validates numeric values rather than their lexical spelling. W01.T07 Python ingress validators enforce a non-boolean integer exactly equal to `1`, but the generic maintenance schema validator cannot distinguish `1` from `1.0`.

## Affected owners and invariants

Affected surfaces are the generic schema-validation authority, W01 Story/history schemas, and their Python ingress validators. The protected invariants are exact schema-version admission, no new cross-owner validation authority, and no unplanned dependency direction from W01 Story owners to the S6D compiler validator.

## Safe continuation

The W01.T07 owner-local implementation remains unpublished. Its Python ingress rejects booleans, floats, strings, nulls, and unsupported integer versions. No generic lexical enforcement is added without a decision.

## Required decision

Senior review must decide whether current canonical strict schema-version law requires a repository-wide lexical-number validation capability for these new schemas, or whether Draft 2020-12 value semantics plus owner-native ingress validation is the accepted enforcement boundary.

RECOMMENDATION: accept the owner-native ingress boundary for W01.T07 because generic JSON Schema cannot represent the requested lexical distinction, and any generic pre-parse/custom-type capability is a new validation authority outside the task envelope.

COST / RISK IF RECOMMENDATION IS WRONG: accepting the boundary may leave generic static schema checks less strict than a future cross-project lexical policy requires; adding the capability without a decision would silently create that cross-project policy.

UNPUBLISHED_WORK: W01.T07 local commits remain unintegrated pending the ruling.
