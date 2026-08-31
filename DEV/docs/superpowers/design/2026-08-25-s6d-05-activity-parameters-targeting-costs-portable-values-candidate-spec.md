# S6D-05 — Candidate Specification

Status: **STEP 5 CANDIDATE — ACCEPTED BY STEP 6/7 REVIEW**

Canonical owner candidate: `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md`.

Material decisions:

- all portable values remain embedded nonowners;
- declaration/binding, target/area/cost/duration, rolls and Choice/Reaction use canonical roots and parent execution identity;
- Signal has kind+bindings only and no lifecycle/disposition/identity;
- StateDelta is a parent-relative prospective instruction with no lifecycle/disposition and is never trusted through Continuation;
- commit/outcome authority stays with ExecutionSegment/MechanicalEvent/receipt;
- exact active StateDelta payloads remain S6D-06-owned;
- no seed content is activated.

Machine candidate adds rejecting Signal/StateDelta roots without status fields, exact portable-value route and catalog contracts, strengthened canonical schemas, and focused binding/catalog/recovery tests. Catalog-aware compilation owns cross-field compatibility where JSON Schema alone is insufficient.
