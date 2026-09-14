# HDM Implementation Planning — Checkpoint / TDD Coherence Repair Addendum

Status: **CURRENT MANDATORY EXECUTION OVERLAY**
Date: 2026-09-14
Production implementation authorized: **NO**.

This overlay repairs publication/checkpoint choreography only. It preserves all accepted RD semantics, interfaces, ownership, readiness routing and test intent.

## Global publication law

A RED test/group is created immediately before the task or tightly coupled task group that is responsible for making it GREEN.

Local RED observation is required by TDD, but a named coherent checkpoint is publication-eligible only when all of the following are true:

```text
all committed tests in the affected RD test module: GREEN
focused owner tests for the checkpoint: GREEN
python3 DEV/TOOLS/run_maintenance_audit.py: GREEN
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py': GREEN
no future-task intentionally failing group already committed: TRUE
```

After publication, hosted CI on the exact checkpoint HEAD must also be GREEN before that checkpoint is reused as completion evidence.

Focused GREEN never overrides broader committed-module or branch-discovery RED. Do not hide a planned RED through skip, expected-failure, discovery-name tricks or temporary suppression.

This law is package-wide. The explicit replacement choreography below covers the seven current base plans where the present text otherwise permits or strongly implies future-task RED groups in an earlier publishable checkpoint.

## RD-01 replacement choreography

Base Task 1 currently declares four test classes even though `CoreCurrentProjectionTests` is owned by Task 3 while Task 2 declares an earlier coherent checkpoint.

Replace that timing with:

- Before Task 2, create `InstallProjectionTests`, `RandomnessProjectionTests` and `DomainExplorationTests`; observe the exact current projection REDs; Task 2 makes those groups GREEN.
- Create `CoreCurrentProjectionTests` only at Task 3, immediately before the bounded R033/R050 scan/repair that owns it; observe RED only for confirmed current in-scope prose debt, then make the group GREEN.
- Task 2 is publication-eligible only when the complete committed RD-01 test module, maintenance audit and full DEV discovery are GREEN.

The base requirement to test R033/R050 is preserved; only premature materialization of its RED group is superseded.

## RD-02 replacement choreography

Base Task 1 no longer creates every future group at once.

- Before Task 2, create only `NativeInformationSchemaTests`; observe RED; Task 2 makes it GREEN. Publish only after full current RD-02 module + maintenance + discovery are GREEN.
- At Task 3 start, create `InformationNormalizationTests` and `RecipientIsolationTests`; observe RED; implement the normalizer; make both GREEN before publication.
- At Task 4 start, create `LegacyInformationProjectionTests`; observe RED; perform legacy projection cutover; make it GREEN before publication.
- Cross-RD LIVE normalization tests are created only when the RD-09 producer/consumer join is ready to be realized in that same joined checkpoint.

Any base wording allowing later RD-02 groups to remain RED in a published Task-2 checkpoint is superseded.

## RD-03 replacement choreography

Create each group only at its owning task boundary:

```text
Task 2 -> NativeActorShapeTests
Task 3 -> ActorAssessmentBehaviorTests
Task 4 -> ContinuitySourceAdmissionTests
Task 5 -> LegacyEntityProjectionTests
Task 6 -> ActorMutationIntegrationTests
Task 7 -> ProvisionalActorConsumerTests
```

Each task first proves its newly introduced group RED, then makes it GREEN. No earlier checkpoint contains a later intentionally failing group.

## RD-05 replacement choreography

- Before Task 2, create `FixedRngTests` and `ProposalValidationTests`; prove RED; Task 2 makes them GREEN.
- Before Task 3, create `AcceptedIdentityTests`, `LifecycleEvidenceTests`, `ProcedureTemporalStateTests` and `ContinuationTemporalStateTests`; prove the task-specific debt RED; Task 3 makes the complete set GREEN before publication.
- Create `ExecutionAtomicityTests` only in Task 4.
- Create `DownstreamExecutionEvidenceTests` only in Task 5.

A Task-2 mechanics checkpoint cannot contain Task-3 lifecycle/Procedure/Continuation groups in intentional RED state.

## RD-12 replacement choreography

- Before Task 2, create only `CoordinationAdmissionTests` and `ObligationLineageTests`; prove RED; Task 2 makes both GREEN.
- Create `IntentClauseCollaborationTests` only at Task 3.
- Create `PlayerRouteCompanionTests` only at Task 4.
- Create input-association, scope-local progression, close/handoff, publication/recovery and catch-up groups only in the task that realizes each respective behavior.

The native-obligation checkpoint cannot contain future IntentClause/PLAYER-route RED groups.

## RD-13 replacement choreography

Create test groups at their owning realization boundary:

```text
Task 2 -> NativeHistoryAuthorityTests
Task 3 -> T0BasisTests
Task 4 -> StoryProjectionTests
Task 5 -> StoryT0MaterializationTests
Task 6 -> CommentatorSelfContainedTests
retained Dramaturg task -> Dramaturg publication/admission/rebase/horizon groups
Story selector/storage checkpoint -> StoryStorageSelectorTests
```

The native-history checkpoint cannot contain future Story, Commentator or Dramaturg RED groups.

## RD-14 replacement choreography

```text
Task 2 -> CampaignSelectionBarrierTests + CreationIdentityTests
Task 3 -> GeneratorScaffoldTests
Task 4 -> InitialPublicationTests
Task 5 -> ProgressiveOnboardingTests
Task 6 -> MultiplayerJoinRejoinTests
Task 7 -> OrdinaryRetrospectiveRoutingTests
Task 8 -> save/clear/menu focused group(s)
Task 9 -> CreatorAuthorityTests
Task 10 -> ShippedBootstrapProjectionTests
```

The earlier umbrella `ProductExitCreatorTests` is not pre-created in Task 1. Its required save/exit and creator-fail-closed behavior remains mandatory through the task-local groups at Tasks 8 and 9.

## Checkpoint verification rule for all seven explicitly repaired RDs

For every named coherent checkpoint in RD-01, RD-02, RD-03, RD-05, RD-12, RD-13 and RD-14, append this verification before publication:

```bash
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Expected: PASS. A failed broader suite means the checkpoint is not publication-eligible even if its focused class is GREEN.

For RD-04, RD-06, RD-07, RD-08, RD-09, RD-10 and RD-11, the current reviewed plan text does not pre-create a future-task RED group before an earlier coherent checkpoint. The same global publication law still applies if execution-time currentness later exposes such a conflict.

## Scope

This overlay supersedes only conflicting RED-group creation timing and checkpoint publication eligibility. It does not remove any required test, change accepted behavior, transfer semantic authority, change readiness accounting or authorize runtime implementation.

```text
VERSION_IMPACT: NONE — planning/control only
MIGRATION_IMPACT: NONE
READINESS_ID_CHANGE: NONE
SEMANTIC_OWNER_CHANGE: NONE
```
