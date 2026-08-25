# S6D-03 — Complete Calculation Selector Metadata — Adversarial Review

Status: **STEP 6 COMPLETE — PASS AFTER REPAIR**

Date: 2026-08-25

Base ref: `v1/engine-rearchitecture@4f951d242eb87bcfc42c744b2fe541862dc0cede`

## Review scope

The independent critic inspected the exact research, candidate, machine surfaces, schema, 571-row admission ledger and focused verification against the whole-project dependency graph.

## Findings and resolution

### AR-01 — Example-driven activation was circular

Severity: **BLOCKING**

Tests/schema examples and proposed metadata were used as support for several promotions without an independent current semantic owner.

Resolution: all structural/example-only IDs remain dormant. The final active surface is reduced to three selectors/two operations with accepted closed semantics. Structural examples are explicitly labeled non-executable.

### AR-02 — Input-class contradiction

Severity: **BLOCKING**

The first artifact admitted invocation-adjudicated input to a selector not allowed by candidate/test.

Resolution: every active selector is `ENGINE_STATE` only.

### AR-03 — Provenance class was not an exact fact allowlist

Severity: **SIGNIFICANT**

Class membership could have admitted any future invocation fact.

Resolution: every selector now has exact `permitted_context_fact_ids=[]`. Exact fact/binding/transitive graph work remains S6D-04.

### AR-04 — Resolver semantics were invented or false-complete

Severity: **SIGNIFICANT**

Recovery/duration/cost/damage and numeric ordering policies lacked closed current evidence or depended on unresolved S6D-05 shapes.

Resolution: affected selectors/pairs are dormant. Active semantics reduce to commutative finite-integer addition with selector minimum and literal-true condition immunity veto.

### AR-05 — Derived-node IDs remained in dependency-kind sets

Severity: **SIGNIFICANT**

The first repair corrected selectors but left derived-node names encoded as kinds.

Resolution: all selector and derived-node kind sets use only `selector|accessor|derived`; exact identities remain prefixed references. Focused tests cover both sections. `condition_intrinsic` invocation input remains an explicit S6D-04 obligation.

## Final verdict

**PASS — zero unresolved BLOCKING or SIGNIFICANT findings.**

The critic did not edit or publish artifacts.
