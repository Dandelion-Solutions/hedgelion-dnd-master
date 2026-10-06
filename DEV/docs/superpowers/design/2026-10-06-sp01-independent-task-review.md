# SP01 independent task review — recovered candidate

Status: **SPEC PASS / QUALITY PASS — STRUCTURAL FOUNDATION ONLY**
Date: 2026-10-06
Original base: `565b7625c2f04e937cfca4425507af61a366bc01`
Final frozen candidate: `1cea6ddb3be82d47eff0b807bd048255b949374e`
Final tree: `aaf19482e304c0d94320ae0353b56b1017dfaa2e`

The independent reviewer inspected the initial SP01 candidate and scoped repairs
at `651c70d5`, `9fd7523c` and `1cea6ddb`. All task-review findings are closed:

| Finding | Final disposition |
|---|---|
| NativePreparationHold was not an exception | Typed Exception with actual raise/catch witness and closed status/continuity fields. |
| DEV consumer ignored unevaluatedProperties | Declared Draft-2020-12 validation uses local registered resources; actual Effect consumer closure parity tested. |
| Stochastic/Wish/reference relations | Pure accepted-reference-set validators, phase consistency, Wish-owned reroll references and family-specific identity arity. Admission truth remains downstream. |
| Opaque compiled/preparation/native mappings | Runtime-owned closed structural projection, no GAME-to-DEV dependency; installed projection reproducible by DEV producer. |
| Root-only preparation rejected child Resolutions | Root equality preserved; child causal/invocation binding and observed Actor role checked without equating child Activity/Actor to root. |
| Execution slot used command schema | Existing mechanics execution envelope and segment/event/Resolution/receipt/roll/Procedure/Continuation components validated separately from command. |
| Current closure status equated to historical receipt | Current Resolution/envelope status separate from immutable segment/receipt status; actual close_resolution witness preserved. |
| Universal singleton event restriction | Ordered batch membership and exact segment/receipt/Resolution joins; multi-event witness is structural, not native-establishment proof. |

Final scoped review changed only Activity contracts and its repair tests. The
other closed findings remained unchanged. Reviewer verified frozen byte identity
and diff checks; broad executable results below are implementer evidence, not
claimed independently rerun by the reviewer.

Implementer exact clean-source proof: 130 focused, 209 expanded, 1597 pytest,
1572 canonical unittest tests; maintenance, generated projection check, scoped
Ruff and runtime build PASS. Coordinator integration checks final identical
SP01 owner bytes again before publication. No hosted CI is claimed here.

Version Impact across the task: new Activity contracts 1.0.1 then material
review repairs through 1.0.4; new structural_contracts 1.0.1 then 1.0.2;
Effect schema 1 -> 2 with producer/projection/test synchronization. New installed
structural projection and capability protocol begin schema 1. Actor/Asset/
Location/Procedure additions are optional; geometry/details restrictions close
reserved non-authoritative bags, not admitted old mechanics. No released
compatibility or migration claim follows from pre-release clean-slate permission.

This PASS is SP01 structural-foundation task review. It does not approve native
spell execution, profile activation, source339 closure, gameplay latency,
package support or the future Senior integration gate.
