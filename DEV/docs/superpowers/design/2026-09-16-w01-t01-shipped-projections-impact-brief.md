# W01.T01 shipped projections - implementation impact brief

TRIGGER: W01.T01 RED witnesses identify active contradictions only in physical files reserved for Wave-05 final writers.
LAST_SAFE_SHA: `a63deadf1e24d92eefe1d0fd82f3912744482f69`
CURRENT_TASK: W01.T01 - Current shipped projections and negative reconciliation

## Approved expectation

W01.T01 requires a RED-to-GREEN repair of a current shipped contradiction while its file-action manifest defers `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/CORE/RANDOMNESS.md`, and `GAME/CORE/EXPLORATION.md` to the Wave-05 final writers. It forbids creating the absent historical `GAME/CORE/DOMAIN_RULES_COVERAGE.md` path or an obsolete compatibility alias.

## Discovered pressure

The W01.T01 RED suite identifies four required current-projection repairs in the deferred Wave-05-only physical files: Plus profile, closed Connector transport, fixed-RNG recovery, and spatial-record wording. The permitted W01.T01 direct write set contains only its new test module. No allowed W01.T01 write can turn those expected failures GREEN without changing deferred final-writer bytes.

## Affected owners and invariants

Affected owner lanes are shipped instructions and the Wave-05 bootstrap/install final writers. The protected invariants at risk are one physical final writer per shared target, no duplicate authority, no obsolete v0.8 compatibility layer, and no intentional future-task RED test publication.

## Safe continuation

All owner-local Wave-01 lanes other than W01.T01 may continue. W01.T01 has no implementation delta to publish. Its safe checkpoint is the current published coordinator state.

## Required decision

Senior review must choose one approved route before W01.T01 resumes:

1. admit the exact named shipped-byte repairs to W01.T01's write set, with Wave-05 final-writer coordination preserved; or
2. move the W01.T01 repair/Green obligation to the named Wave-05 final-writer tasks and redefine W01.T01 as a static negative-reconciliation checkpoint without future-task failing tests.

RECOMMENDATION: route 2, because it retains the explicit one-final-writer rule and prevents W01.T01 from making Wave-05-only bytes a parallel writer surface.

COST / RISK IF RECOMMENDATION IS WRONG: delaying a required owner-local precondition could hide a genuine early cross-owner consistency requirement; route 1 would instead require an explicit accepted exception to the shared-writer discipline.

UNPUBLISHED_WORK: NONE
