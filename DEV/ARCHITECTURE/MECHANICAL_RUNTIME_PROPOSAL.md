# Mechanical Runtime and Physical Hot State — Historical Proposal

Status: **HISTORICAL / NONCANONICAL PROPOSAL — SOURCE-NEUTRAL RETENTION**

Implementation status: **not activated by this document**

This file preserves the HDM-native architectural constraints that made the early mechanical-runtime proposal useful. Later accepted architecture/specifications and machine contracts supersede it. It is not an implementation plan and does not select libraries, products or external components.

## 1. Preserved HDM boundaries

1. Durable campaign authority and disposable/local HOT projection are distinct; a cache/database projection must be reconstructable from its owning durable inputs.
2. The LLM maps natural-language intent to bounded typed requests. It does not calculate authoritative mechanics, submit arbitrary record patches or execute arbitrary code.
3. An Activity is a declarative bounded mechanical procedure; one invocation is a Resolution.
4. Rule contributions are typed/pure with respect to authoritative mutation. They may influence registered calculations but do not become arbitrary callbacks.
5. Transient calculation signals are distinct from committed mechanical events.
6. State mutation occurs through validated atomic segments with revision/idempotency/currentness checks appropriate to the owning contracts.
7. Reactions/choices suspend explicit runtime state; no long-running transaction remains open across chat turns.
8. Dialogue is the control loop. No real-time daemon/background world clock is required for ordinary rules advancement.
9. Canonical/durable records may not depend on lost incidental local state; dependencies needed for durable publication must be promoted/materialized under current owners before publication.
10. Publication timing, durability classification and ref/currentness semantics belong to their current canonical owners. This proposal cannot override them.

## 2. DiceEngine boundary

HDM needs a deterministic/controlled dice boundary with at least these requirements:

- accepted dice syntax is finite and explicitly validated;
- RNG ownership is deterministic and compatible with current randomness/evidence contracts;
- execution limits prevent unbounded or hostile expressions;
- results are typed and can be retained/replayed where current owners require evidence;
- arbitrary LLM-provided code or unrestricted expression evaluation is forbidden.

No concrete dice library or external implementation is selected here. Component choice, adapter shape, maintenance/licensing review and performance trade-offs belong to future authorized implementation planning.

## 3. HOT/runtime realization constraints

A concrete implementation may use a local transactional store or another suitable projection, but physical design must preserve:

- one authoritative owner for each gameplay value;
- typed hydration/materialization boundaries;
- revision/currentness validation;
- no silent duplication of canonical state into writable cache authority;
- explicit suspension/recovery semantics;
- bounded deterministic execution;
- complete invalidation/rebuild when the owning source changes.

The original provisional module/file decomposition is not retained as architecture authority. Implementation structure should be chosen from the current canonical contracts and measured implementation needs.

## 4. Publication and transport

Current publication/currentness law is owned by the accepted persistence/publication specifications and the supported-ref monotonicity amendment. A transport implementation must preserve their exact-source, non-force, ambiguity/recovery and fail-closed semantics. Convenience APIs or local preparation success do not become publication authority.

## 5. Public provenance note

This historical proposal intentionally retains no prior-art table, development-source bibliography or external implementation preference. Required legal attribution and current operational/technical provenance remain in their dedicated owners.
