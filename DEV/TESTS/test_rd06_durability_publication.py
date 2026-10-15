from __future__ import annotations

import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import GAME.TOOLS.publication as publication_module
from GAME.TOOLS.durability import (
    DurabilityContractError,
    ExecutionDurabilityJoin,
    NativeDurabilityResult,
    RoutedSerializedOperation,
    complete_save_promise,
    evaluate_durability,
    freeze_save_promise,
    is_execution_durability_join,
    issue_durability_handoff_promise,
    join_execution_durability,
    project_durable_generations,
    route_serialized_operation,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign
from GAME.TOOLS.publication import (
    CommitAncestryEvidence,
    PublicationAcceptanceEvidence,
    PublicationContractError,
    PublicationCurrentClosureEvidence,
    PublicationOutcome,
    PublicationStatus,
    build_connector_git_plan,
    classify_ref_transition,
    freeze_campaign_publication_attempt,
    reconcile_indeterminate_publication,
    validate_owner_issued_accepted_publication,
)
from GAME.TOOLS.recovery_roots import (
    OperationalRootDelta,
    derive_operational_root_delta,
)

ROOT = Path(__file__).resolve().parents[2]
H = "0123456789abcdef0123456789abcdef01234567"
T = "abcdef0123456789abcdef0123456789abcdef01"
C = "fedcba9876543210fedcba9876543210fedcba98"


def _validate_owner_publication(
    outcome: PublicationOutcome,
    *,
    campaign_id: str,
    expected_pinned_head_sha: str,
) -> PublicationAcceptanceEvidence:
    return validate_owner_issued_accepted_publication(
        outcome,
        campaign_id=campaign_id,
        expected_pinned_head_sha=expected_pinned_head_sha,
    )


def _accepted_command() -> dict[str, object]:
    from DEV.TESTS.test_rd05_runtime_execution import _candidate, _interpreter_result
    from DEV.TESTS.test_rd07_recovery import (
        FakeAccess,
        FakeApplicability,
        FakeRepository,
    )
    from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
    from DEV.TESTS.test_sp03_authenticated_input import trusted_command_source
    from GAME.TOOLS.policy_basis import (
        AcceptedAdjudicationBasis,
        PolicyBasisResolver,
        PolicySelection,
    )
    from GAME.TOOLS.runtime_execution import accept_command

    context = _bind_context()
    policy = PolicyBasisResolver(FakeRepository(), FakeAccess(), FakeApplicability()).resolve(
        "campaign-1", PolicySelection("policy.social_leverage", "activity.check.generic"),
        catalog_context=context)
    proposal = {
        "command_id": "command-000001",
        "interaction_id": "interaction-000001",
        "intent_plan_id": "plan-000001",
        "clause_id": "clause-1",
        "action_request": {
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "target_ids": [],
            "parameter_bindings": {
                "dc": {
                    "source_class": "INVOCATION_ADJUDICATED",
                    "value": 15,
                    "provenance_ref": "turn-1:dc",
                    "eligibility_basis_fingerprint": "eligibility-A",
                    "rules_context_fingerprint": "rules-A",
                    "policy_basis_refs": [f"policy.social_leverage@{H}"],
                }
            },
        },
        "root_resolution_id": "resolution-000001",
    }
    basis = AcceptedAdjudicationBasis(
        parameter_bindings=proposal["action_request"]["parameter_bindings"],
        invocation_facts=(), verified_policies=(policy,))
    with trusted_command_source(proposal) as (host, _records):
        return accept_command(_interpreter_result(), context, _candidate(), proposal,
            input_observation=host._current_owner._observe_command_input(proposal),
            adjudication_basis=basis)


def _execution() -> dict[str, object]:
    from DEV.TESTS.test_rd05_runtime_execution import _resolution_source
    from DEV.TESTS.test_sp03_authenticated_input import trusted_command_source
    from GAME.TOOLS.current_owner import NativeOwnerRef
    from GAME.TOOLS.mechanics import ExecutionStore, FixedRng, execute_segment

    command = _accepted_command()
    with trusted_command_source(command) as (host, records):
        ref = NativeOwnerRef("runtime.command", (command["command_id"],))
        records[route_native_record(ref.family_key, ref.identity).relative_path] = {
            "kind": ref.family_key, "id": command["command_id"], **deepcopy(command)}
        observation = host._current_owner._observe_command_input(command, required_owner_refs=(ref,))
        return execute_segment(command, _resolution_source(command), input_observation=observation,
            rng=FixedRng([17]), event_payload={"result": 17}, store=ExecutionStore())


def _command_operation() -> RoutedSerializedOperation:
    return route_serialized_operation(
        "runtime.command", "command-000001", _accepted_command()
    )


def _execution_join() -> ExecutionDurabilityJoin:
    evaluation = evaluate_durability(
        campaign_id="campaign-000001",
        scope="accepted_execution",
        dirty_roots=("runtime.command:command-000001",),
        currentness_evidence={"head_sha": H},
    )
    promise = freeze_save_promise(evaluation, owner_generations={})
    return join_execution_durability(
        _accepted_command(),
        _execution(),
        promise,
        routed_operation=_command_operation(),
    )


def _procedure(*, lifecycle: str, revision: int = 1) -> dict[str, object]:
    state: dict[str, object] = {
        "schema_version": 2,
        "procedure_kind": "procedure.combat_minimal",
        "lifecycle": lifecycle,
        "lifecycle_state": "terminated" if lifecycle == "TERMINAL" else "turn_active",
        "participant_ids": ["actor-1"],
        "initiative_order": ["actor-1"],
        "round_number": 1,
        "round_advance_pending": False,
        "active_turn_index": 0,
        "participant_resources": {"actor-1": {"resource.action_budget": {"spent": 0}}},
    }
    return {
        "kind": "runtime.procedure",
        "id": "procedure-000001",
        "revision": revision,
        "state": state,
    }


def _root_delta() -> tuple[OperationalRootDelta, dict[str, object], dict[str, object]]:
    active = _procedure(lifecycle="ACTIVE")
    terminal = _procedure(lifecycle="TERMINAL", revision=2)
    enrolled = derive_operational_root_delta(
        "campaign-000001", "runtime.procedure", active
    )
    removed = derive_operational_root_delta(
        "campaign-000001",
        "runtime.procedure",
        terminal,
        existing_roots=(enrolled.root,),
    )
    page = {
        "schema_version": 1,
        "campaign_id": "campaign-000001",
        "complete": True,
        "roots": [enrolled.root.to_dict()],
    }
    return removed, terminal, page


def _attempt(**overrides: object):
    removed, terminal, page = _root_delta()
    values: dict[str, object] = {
        "repository_id": "github.com/example/campaigns",
        "target_ref": "campaign/20260916",
        "campaign_id": "campaign-000001",
        "acting_principal": AuthenticatedPrincipalEvidence("principal-1"),
        "pinned_head_sha": H,
        "base_tree_sha": T,
        "manifest": {
            "campaign_id": "campaign-000001",
            "campaign_name": "The Frostfall",
            "branch": "campaign/20260916",
            "created_at": "2026-09-16T12:00:00Z",
        },
        "campaign_card": {
            "campaign_id": "campaign-000001",
            "campaign_name": "The Frostfall",
        },
        "path_operations": {_command_operation().relative_path: _accepted_command()},
        "owner_generations": {"runtime.procedure:procedure-000001": 2},
        "currentness_evidence": PinnedCampaign("campaign-000001", H, T),
        "accepted_command": _accepted_command(),
        "execution": _execution(),
        "execution_durability_join": _execution_join(),
        "routed_operation": _command_operation(),
        "procedure_before": _procedure(lifecycle="ACTIVE"),
        "procedure_after": terminal,
        "root_delta": removed,
        "root_membership_before": page,
        "policy_basis": {"policy_refs": [f"policy.social_leverage@{H}"], "source_revision": H},
        "catalog_basis": _accepted_command()["catalog_context"],
        "publication_reason": "accepted_execution_closure",
    }
    values.update(overrides)
    return freeze_campaign_publication_attempt(**values)


def _procedure_attempt():
    removed, terminal, page = _root_delta()
    operation = route_serialized_operation("runtime.procedure", "procedure-000001", terminal)
    return freeze_campaign_publication_attempt(
        repository_id="github.com/example/campaigns",
        target_ref="campaign/20260916",
        campaign_id="campaign-000001",
        acting_principal=AuthenticatedPrincipalEvidence("principal-1"),
        pinned_head_sha=H,
        base_tree_sha=T,
        currentness_evidence=PinnedCampaign("campaign-000001", H, T),
        manifest={
            "campaign_id": "campaign-000001",
            "campaign_name": "The Frostfall",
            "branch": "campaign/20260916",
            "created_at": "2026-09-16T12:00:00Z",
        },
        campaign_card={"campaign_id": "campaign-000001", "campaign_name": "The Frostfall"},
        path_operations={operation.relative_path: terminal},
        owner_generations={"runtime.procedure:procedure-000001": 2},
        procedure_before=_procedure(lifecycle="ACTIVE"),
        procedure_after=terminal,
        root_delta=removed,
        root_membership_before=page,
        routed_operation=operation,
        publication_reason="procedure_terminal_closure",
    )


def _current_closure(attempt, *, head_sha: str, operation_digests=None):
    return PublicationCurrentClosureEvidence(
        base_revision=H,
        head_sha=head_sha,
        tree_sha=T,
        operation_digests=operation_digests or attempt.publication_operation_digests(),
    )


class DurabilityPromiseContractTests(unittest.TestCase):
    def test_explicit_save_freezes_one_ephemeral_scope_and_currentness_basis(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="explicit_save",
            dirty_roots=("runtime.command:command-000001",),
            required_dependencies=("runtime.procedure:procedure-000001",),
            currentness_evidence={"head_sha": H},
        )
        promise = freeze_save_promise(
            evaluation,
            owner_generations={"runtime.command:command-000001": 4},
        )

        self.assertEqual(promise.scope, "explicit_save")
        self.assertTrue(promise.ephemeral)
        self.assertEqual(promise.required_dependencies, ("runtime.procedure:procedure-000001",))
        self.assertEqual(promise.currentness_evidence["head_sha"], H)
        self.assertFalse(hasattr(promise, "journal_id"))

    def test_no_write_requires_operation_current_evidence_not_empty_dirty_state(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="explicit_save",
            dirty_roots=(),
            currentness_evidence=None,
        )

        self.assertEqual(evaluation.status, "REVALIDATION_REQUIRED")
        with self.assertRaisesRegex(DurabilityContractError, "currentness|current"):
            freeze_save_promise(evaluation, owner_generations={})

    def test_partial_native_success_does_not_acknowledge_save(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="explicit_save",
            dirty_roots=("runtime.command:command-000001",),
            currentness_evidence={"head_sha": H},
        )
        promise = freeze_save_promise(evaluation, owner_generations={})

        result = complete_save_promise(
            promise,
            (
                NativeDurabilityResult("campaign", "CONFIRMED_ACCEPTED"),
                NativeDurabilityResult("storage", "INDETERMINATE"),
            ),
            currentness_evidence={"head_sha": H},
        )

        self.assertEqual(result.status, "INDETERMINATE")
        self.assertFalse(result.acknowledged)


class PublicationPlanTests(unittest.TestCase):
    def test_publication_requires_captured_currentness_evidence(self) -> None:
        values = {
            "repository_id": "github.com/example/campaigns",
            "target_ref": "campaign/20260916",
            "campaign_id": "campaign-000001",
            "acting_principal": AuthenticatedPrincipalEvidence("principal-1"),
            "pinned_head_sha": H,
            "base_tree_sha": T,
            "manifest": {
                "campaign_id": "campaign-000001",
                "campaign_name": "The Frostfall",
                "branch": "campaign/20260916",
                "created_at": "2026-09-16T12:00:00Z",
            },
            "campaign_card": {"campaign_id": "campaign-000001", "campaign_name": "The Frostfall"},
            "path_operations": {_command_operation().relative_path: _accepted_command()},
            "owner_generations": {},
        }

        with self.assertRaisesRegex(PublicationContractError, "currentness"):
            freeze_campaign_publication_attempt(**values)

    def test_publication_rejects_forged_mapping_principal_evidence(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "owner-typed|Access"):
            _attempt(acting_principal={"principal_id": "principal-1", "authorization": "campaign_write"})

    def test_publication_rejects_currentness_head_or_tree_mismatch(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "currentness"):
            _attempt(currentness_evidence=PinnedCampaign("campaign-000001", C, T))
        with self.assertRaisesRegex(PublicationContractError, "currentness"):
            _attempt(currentness_evidence=PinnedCampaign("campaign-000001", H, C))

    def test_publication_rejects_missing_or_mismatched_typed_join_and_route(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "join"):
            _attempt(execution_durability_join=None)
        with self.assertRaisesRegex(PublicationContractError, "route|operation"):
            _attempt(routed_operation=None)
        with self.assertRaisesRegex(PublicationContractError, "join"):
            _attempt(
                execution_durability_join=_execution_join(),
                execution=_execution() | {"event_id": "other"},
            )

    def test_runtime_command_route_rejects_missing_join_without_raw_execution_arguments(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "join"):
            _attempt(
                accepted_command=None,
                execution=None,
                execution_durability_join=None,
            )

    def test_immutable_command_attempt_rejects_missing_join(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "join"):
            replace(_attempt(), execution_durability_join=None)

    def test_freeze_and_plan_use_one_parent_tree_and_non_force_ref_transition(self) -> None:
        attempt = _attempt()
        plan = build_connector_git_plan(attempt)

        self.assertEqual(plan.parent_sha, H)
        self.assertEqual(plan.base_tree_sha, T)
        self.assertEqual(
            tuple(operation.kind for operation in plan.operations),
            ("create_tree", "read_ref", "create_commit", "update_ref"),
        )
        self.assertFalse(plan.force)
        self.assertEqual(plan.commit_parent_sha, H)
        self.assertNotIn("create_file", {operation.kind for operation in plan.operations})

    def test_plan_preserves_execution_catalog_and_policy_bases(self) -> None:
        attempt = _attempt()

        self.assertEqual(attempt.accepted_identity.command_id, "command-000001")
        self.assertEqual(attempt.accepted_identity.input_fingerprint, _accepted_command()["input_fingerprint"])
        self.assertEqual(attempt.fixed_rng_values, (17,))
        self.assertEqual(attempt.catalog_basis["basis"]["catalog_generation"], 2)
        self.assertEqual(attempt.policy_basis["policy_refs"], (f"policy.social_leverage@{H}",))

    def test_frozen_attempt_cannot_be_mutated_through_nested_inputs(self) -> None:
        attempt = _attempt()

        with self.assertRaises(TypeError):
            attempt.path_operations[_command_operation().relative_path]["command_id"] = "other"  # type: ignore[index]
        with self.assertRaises(TypeError):
            attempt.catalog_basis["basis"]["catalog_generation"] = 3  # type: ignore[index]

    def test_campaign_publication_has_no_storage_or_repository_spanning_transaction(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "storage"):
            _attempt(
                path_operations={
                    _command_operation().relative_path: _accepted_command(),
                    "DND_STORAGE.yaml": {"storage": "metadata"},
                }
            )


class PublicationOutcomeTests(unittest.TestCase):
    def test_revalidated_recovery_basis_issues_exact_instance_w02_evidence(
        self,
    ) -> None:
        freeze_recovery_basis = getattr(
            publication_module, "freeze_campaign_publication_recovery_basis", None
        )
        self.assertTrue(callable(freeze_recovery_basis))
        if not callable(freeze_recovery_basis):
            return
        operation = route_serialized_operation(
            "runtime.collaboration_obligation",
            "obligation-000001",
            {"id": "obligation-000001", "kind": "runtime.collaboration_obligation"},
        )
        recovery_basis = freeze_recovery_basis(
            repository_id="github.com/example/campaigns",
            target_ref="campaign/20260916",
            campaign_id="campaign-000001",
            pinned_head_sha=H,
            base_tree_sha=T,
            intended_commit_sha=C,
            manifest={
                "campaign_id": "campaign-000001",
                "campaign_name": "The Frostfall",
                "branch": "campaign/20260916",
                "created_at": "2026-09-16T12:00:00Z",
            },
            campaign_card={
                "campaign_id": "campaign-000001",
                "campaign_name": "The Frostfall",
            },
            path_operations={operation.relative_path: operation.payload},
            owner_generations={"runtime.collaboration_obligation:obligation-000001": 4},
            routed_operation=operation,
            publication_reason="collaboration-close",
        )
        outcome = PublicationOutcome(
            PublicationStatus.ACCEPTED,
            C,
            C,
            "RECONCILED_CURRENT_CLOSURE",
            False,
        )
        closure = PublicationCurrentClosureEvidence(
            base_revision=H,
            head_sha=C,
            tree_sha=T,
            operation_digests=recovery_basis.publication_operation_digests(),
        )

        issued = publication_module._issue_owner_issued_accepted_publication(
            outcome,
            recovery_basis,
            intended_commit_sha=C,
            current_closure=closure,
        )

        evidence = _validate_owner_publication(
            outcome,
            campaign_id="campaign-000001",
            expected_pinned_head_sha=H,
        )
        self.assertIs(evidence, issued)
        recovery_basis_type = getattr(
            publication_module, "FrozenCampaignPublicationRecoveryBasis", None
        )
        self.assertIsInstance(
            evidence.attempt,
            recovery_basis_type,
        )
        self.assertFalse(hasattr(evidence.attempt, "acting_principal"))
        path, digest = next(
            iter(recovery_basis.publication_operation_digests().items())
        )
        self.assertIs(
            validate_owner_issued_accepted_publication(
                outcome,
                campaign_id="campaign-000001",
                expected_pinned_head_sha=H,
                required_operation_digests={path: digest},
            ),
            evidence,
        )
        copied = PublicationOutcome(
            outcome.status,
            outcome.intended_commit_sha,
            outcome.observed_head_sha,
            outcome.cause,
            outcome.dispatched,
            outcome.retry_with_force,
        )
        with self.assertRaises(PublicationContractError):
            _validate_owner_publication(
                copied,
                campaign_id="campaign-000001",
                expected_pinned_head_sha=H,
            )
        other_intended = "a" * 40
        other_outcome = PublicationOutcome(
            PublicationStatus.ACCEPTED,
            other_intended,
            other_intended,
            "RECONCILED_CURRENT_CLOSURE",
            False,
        )
        other_closure = PublicationCurrentClosureEvidence(
            base_revision=H,
            head_sha=other_intended,
            tree_sha=T,
            operation_digests=recovery_basis.publication_operation_digests(),
        )
        with self.assertRaisesRegex(PublicationContractError, "intended commit"):
            publication_module._issue_owner_issued_accepted_publication(
                other_outcome,
                recovery_basis,
                intended_commit_sha=other_intended,
                current_closure=other_closure,
            )

    def test_constructible_accepted_outcome_is_not_owner_issued(self) -> None:
        outcome = PublicationOutcome(
            PublicationStatus.ACCEPTED,
            C,
            C,
            "CONFIRMED_ACCEPTED",
            True,
        )

        self.assertTrue(outcome.acknowledge())
        with self.assertRaises(PublicationContractError):
            _validate_owner_publication(
                outcome,
                campaign_id="campaign-000001",
                expected_pinned_head_sha=H,
            )

    def test_direct_classifier_result_is_not_owner_issued(self) -> None:
        attempt = _attempt()
        outcome = classify_ref_transition(
            {"dispatched": True, "status": "accepted", "head_sha": C},
            intended_commit_sha=C,
        )

        with self.assertRaises(PublicationContractError):
            _validate_owner_publication(
                outcome,
                campaign_id=attempt.campaign_id,
                expected_pinned_head_sha=attempt.pinned_head_sha,
            )

    def test_direct_reconciliation_result_with_constructible_proofs_is_not_owner_issued(
        self,
    ) -> None:
        attempt = _attempt()
        closure = _current_closure(attempt, head_sha=C)
        outcome = reconcile_indeterminate_publication(
            attempt,
            lambda: {"closure": closure},
            intended_commit_sha=C,
        )

        self.assertEqual(outcome.status, PublicationStatus.ACCEPTED)
        with self.assertRaises(PublicationContractError):
            _validate_owner_publication(
                outcome,
                campaign_id=attempt.campaign_id,
                expected_pinned_head_sha=attempt.pinned_head_sha,
            )

        descendant = "a" * 40
        ancestor_outcome = reconcile_indeterminate_publication(
            attempt,
            lambda: {
                "closure": _current_closure(attempt, head_sha=descendant),
                "ancestry": CommitAncestryEvidence(
                    ancestor_sha=C, descendant_sha=descendant
                ),
            },
            intended_commit_sha=C,
        )
        self.assertEqual(ancestor_outcome.status, PublicationStatus.ACCEPTED)
        with self.assertRaises(PublicationContractError):
            _validate_owner_publication(
                ancestor_outcome,
                campaign_id=attempt.campaign_id,
                expected_pinned_head_sha=attempt.pinned_head_sha,
            )

    def test_owner_issuance_rejects_mismatched_closure_and_ancestry_proofs(
        self,
    ) -> None:
        attempt = _attempt()
        digests = attempt.publication_operation_digests()
        intended = C
        descendant = "a" * 40

        invalid_proofs = (
            (
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    intended,
                    intended,
                    "RECONCILED_CURRENT_CLOSURE",
                    False,
                ),
                PublicationCurrentClosureEvidence(
                    base_revision=T,
                    head_sha=intended,
                    tree_sha=T,
                    operation_digests=digests,
                ),
                None,
            ),
            (
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    intended,
                    intended,
                    "RECONCILED_CURRENT_CLOSURE",
                    False,
                ),
                PublicationCurrentClosureEvidence(
                    base_revision=H,
                    head_sha=descendant,
                    tree_sha=T,
                    operation_digests=digests,
                ),
                None,
            ),
            (
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    intended,
                    intended,
                    "RECONCILED_CURRENT_CLOSURE",
                    False,
                ),
                PublicationCurrentClosureEvidence(
                    base_revision=H,
                    head_sha=intended,
                    tree_sha=T,
                    operation_digests={
                        path: digest
                        for index, (path, digest) in enumerate(digests.items())
                        if index > 0
                    },
                ),
                None,
            ),
            (
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    intended,
                    intended,
                    "RECONCILED_CURRENT_CLOSURE",
                    False,
                ),
                PublicationCurrentClosureEvidence(
                    base_revision=H,
                    head_sha=intended,
                    tree_sha=T,
                    operation_digests=digests | {next(iter(digests)): "0" * 64},
                ),
                None,
            ),
            (
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    intended,
                    descendant,
                    "RECONCILED_ANCESTOR_CURRENT_CLOSURE",
                    False,
                ),
                PublicationCurrentClosureEvidence(
                    base_revision=H,
                    head_sha=descendant,
                    tree_sha=T,
                    operation_digests=digests,
                ),
                CommitAncestryEvidence(ancestor_sha=H, descendant_sha=descendant),
            ),
        )

        for outcome, closure, ancestry in invalid_proofs:
            with self.subTest(cause=outcome.cause, closure=closure.to_dict()):
                with self.assertRaises(PublicationContractError):
                    publication_module._issue_owner_issued_accepted_publication(
                        outcome,
                        attempt,
                        intended_commit_sha=intended,
                        current_closure=closure,
                        ancestry=ancestry,
                    )
                with self.assertRaises(PublicationContractError):
                    _validate_owner_publication(
                        outcome,
                        campaign_id=attempt.campaign_id,
                        expected_pinned_head_sha=attempt.pinned_head_sha,
                    )

    def test_owner_issued_ancestor_evidence_preserves_additional_disjoint_paths(
        self,
    ) -> None:
        attempt = _attempt()
        intended = C
        descendant = "a" * 40
        extra_path = "independent/owner.yaml"
        closure = PublicationCurrentClosureEvidence(
            base_revision=attempt.pinned_head_sha,
            head_sha=descendant,
            tree_sha=T,
            operation_digests={
                **attempt.publication_operation_digests(),
                extra_path: "d" * 64,
            },
        )
        outcome = PublicationOutcome(
            PublicationStatus.ACCEPTED,
            intended,
            descendant,
            "RECONCILED_ANCESTOR_CURRENT_CLOSURE",
            False,
        )

        issued = publication_module._issue_owner_issued_accepted_publication(
            outcome,
            attempt,
            intended_commit_sha=intended,
            current_closure=closure,
            ancestry=CommitAncestryEvidence(
                ancestor_sha=intended, descendant_sha=descendant
            ),
        )

        validated = _validate_owner_publication(
            outcome,
            campaign_id=attempt.campaign_id,
            expected_pinned_head_sha=attempt.pinned_head_sha,
        )
        self.assertIs(validated, issued)
        self.assertEqual(
            validated.current_closure.operation_digests[extra_path], "d" * 64
        )

    def test_acceptance_is_typed_and_acknowledgeable(self) -> None:
        outcome = classify_ref_transition(
            {"dispatched": True, "status": "accepted", "head_sha": C},
            intended_commit_sha=C,
        )

        self.assertEqual(outcome.status, PublicationStatus.ACCEPTED)
        self.assertTrue(outcome.acknowledge())

    def test_non_fast_forward_is_conflict_and_never_force_retried(self) -> None:
        outcome = classify_ref_transition(
            {
                "dispatched": True,
                "status": "rejected",
                "reason": "non_fast_forward",
                "head_sha": C,
            },
            intended_commit_sha=C,
        )

        self.assertEqual(outcome.status, PublicationStatus.CONFLICT)
        self.assertEqual(outcome.cause, "STALE_OR_NON_FAST_FORWARD")
        self.assertFalse(outcome.retry_with_force)

    def test_indeterminate_acknowledgement_requires_exact_authoritative_read(self) -> None:
        attempt = _attempt()
        outcome = classify_ref_transition(
            {"dispatched": True, "status": "indeterminate"},
            intended_commit_sha=C,
        )

        self.assertEqual(outcome.status, PublicationStatus.INDETERMINATE)
        with self.assertRaisesRegex(PublicationContractError, "indeterminate"):
            outcome.acknowledge()

        reads: list[str] = []

        def read_current() -> dict[str, object]:
            reads.append("current-ref")
            return {
                "closure": _current_closure(attempt, head_sha=C),
            }

        reconciled = reconcile_indeterminate_publication(
            attempt, read_current, intended_commit_sha=C
        )
        self.assertEqual(reconciled.status, PublicationStatus.ACCEPTED)
        self.assertEqual(reads, ["current-ref"])

    def test_indeterminate_without_compatible_current_closure_stays_unresolved(self) -> None:
        attempt = _attempt()

        result = reconcile_indeterminate_publication(
            attempt,
            lambda: {
                "closure": _current_closure(
                    attempt,
                    head_sha=C,
                    operation_digests={"unrelated/path": "0" * 64},
                ),
            },
            intended_commit_sha=C,
        )

        self.assertEqual(result.status, PublicationStatus.INDETERMINATE)
        self.assertFalse(result.acknowledged)

    def test_indeterminate_reconciliation_rejects_omitted_commit_or_unbound_boolean(self) -> None:
        attempt = _attempt()
        with self.assertRaisesRegex(PublicationContractError, "intended commit"):
            reconcile_indeterminate_publication(
                attempt,
                lambda: {"head_sha": C, "lineage_contains_intended": True},
            )

        with self.assertRaisesRegex(PublicationContractError, "boolean"):
            reconcile_indeterminate_publication(
                attempt,
                lambda: {
                    "head_sha": C,
                    "tree_sha": T,
                    "parent_sha": H,
                    "operation_paths": sorted(attempt.path_operations),
                    "closure_digest": "not-the-attempt-closure",
                    "lineage_contains_intended": True,
                },
                intended_commit_sha=C,
            )

    def test_descendant_head_accepts_only_typed_ancestor_and_compatible_closure(self) -> None:
        attempt = _attempt()
        descendant = "a" * 40
        reconciled = reconcile_indeterminate_publication(
            attempt,
            lambda: {
                "ancestry": CommitAncestryEvidence(ancestor_sha=C, descendant_sha=descendant),
                "closure": _current_closure(attempt, head_sha=descendant),
            },
            intended_commit_sha=C,
        )

        self.assertEqual(reconciled.status, PublicationStatus.ACCEPTED)
        self.assertEqual(reconciled.observed_head_sha, descendant)

    def test_descendant_head_rejects_overlapping_or_incompatible_closure(self) -> None:
        attempt = _attempt()
        descendant = "a" * 40
        digests = attempt.publication_operation_digests()
        overlapping_path = next(iter(digests))
        digests[overlapping_path] = "0" * 64
        result = reconcile_indeterminate_publication(
            attempt,
            lambda: {
                "ancestry": CommitAncestryEvidence(ancestor_sha=C, descendant_sha=descendant),
                "closure": _current_closure(
                    attempt, head_sha=descendant, operation_digests=digests
                ),
            },
            intended_commit_sha=C,
        )

        self.assertEqual(result.status, PublicationStatus.CONFLICT)

    def test_descendant_head_without_typed_ancestry_stays_indeterminate(self) -> None:
        attempt = _attempt()
        descendant = "a" * 40
        result = reconcile_indeterminate_publication(
            attempt,
            lambda: {"closure": _current_closure(attempt, head_sha=descendant)},
            intended_commit_sha=C,
        )

        self.assertEqual(result.status, PublicationStatus.INDETERMINATE)


class ExecutionDurabilityJoinTests(unittest.TestCase):
    def _event_carrier_consumers(self, command):
        from GAME.TOOLS.recovery import validate_recovered_basis
        from GAME.TOOLS.runtime_execution import command_policy_basis

        promise = freeze_save_promise(evaluate_durability(campaign_id="campaign-000001",
            scope="accepted_execution", dirty_roots=("runtime.command:" + command["command_id"],),
            currentness_evidence={"head_sha": H}), owner_generations={})
        return {
            "publication": lambda value: publication_module._accepted_identity(command, value),
            "join": lambda value: join_execution_durability(command, value, promise,
                routed_operation=route_serialized_operation("runtime.command", command["command_id"], command)),
            "recovery": lambda value: validate_recovered_basis(command, value,
                catalog_basis=command["catalog_context"], policy_basis=command_policy_basis(command)),
        }

    def test_review_r3_producer_event_carrier_forms_and_actual_cold_dual_are_preserved(self):
        from DEV.TESTS.test_rd07_recovery import FakeRepository
        from GAME.TOOLS.recovery import _hydrate_execution_result

        command, singular = _accepted_command(), _execution()
        dual = dict(deepcopy(singular), events=[deepcopy(singular["event"])])
        plural = deepcopy(dual)
        plural.pop("event")
        plural.pop("event_id")
        repository = FakeRepository()
        event_id = singular["event_id"]
        repository.files[route_native_record("runtime.mechanical_event", (event_id,)).relative_path] = {
            "kind": "runtime.mechanical_event", "id": event_id, **deepcopy(singular["event"])}
        cold = _hydrate_execution_result(repository, repository.pin_campaign("campaign-1"),
            command, singular["resolution"])
        self.assertEqual(cold["events"], [cold["event"]])
        self.assertEqual(cold["event_id"], event_id)
        consumers = self._event_carrier_consumers(command)
        for label, value in (("singular producer", singular), ("plural only", plural),
                             ("equal dual", dual), ("actual cold dual producer", cold)):
            for name, consumer in consumers.items():
                with self.subTest(form=label, boundary=name):
                    recovered_or_joined = consumer(value)
                    if name == "recovery":
                        self.assertEqual(recovered_or_joined.execution, value)
                        self.assertEqual(recovered_or_joined.execution_identity, singular["execution_identity"])

    def test_review_r3_conflicting_or_malformed_event_carriers_reject_at_all_consumers(self):
        command, result = _accepted_command(), _execution()
        dual = dict(deepcopy(result), events=[deepcopy(result["event"])])
        consumers = self._event_carrier_consumers(command)
        for consumer in consumers.values():
            consumer(dual)
        for label, mutate in (
            ("review forged singular", lambda r: r.update(event={"event_kind": "forged",
                "segment_id": "foreign", "event_ordinal": True})),
            ("null singular", lambda r: r.update(event=None)),
            ("empty singular", lambda r: r.update(event={})),
            ("list singular", lambda r: r.update(event=[])),
            ("bool ordinal alias", lambda r: r["event"].update(event_ordinal=True)),
            ("float ordinal alias", lambda r: r["event"].update(event_ordinal=1.0)),
            ("Python equal payload differs canonically", lambda r: r["event"]["payload"].update(result=17.0)),
            ("null plural must not fall back", lambda r: r.update(events=None)),
            ("empty plural must not fall back", lambda r: r.update(events=[])),
            ("object plural", lambda r: r.update(events={})),
            ("null plural member", lambda r: r.update(events=[None])),
            ("null singular ID", lambda r: r.update(event_id=None)),
            ("foreign singular ID", lambda r: r.update(event_id="foreign")),
        ):
            wrong = deepcopy(dual)
            mutate(wrong)
            self.assertEqual(wrong["execution_identity"], result["execution_identity"])
            for name, consumer in consumers.items():
                with self.subTest(case=label, boundary=name), self.assertRaises(ValueError):
                    consumer(wrong)

    def test_review_r3_plural_batch_cannot_acquire_an_ambiguous_singular_alias(self):
        command, result = _accepted_command(), _execution()
        # Retained multi-event contract witness derived from the real producer's
        # complete edge; not a claim that mechanics emits a second native event.
        first = deepcopy(result.pop("event"))
        result.pop("event_id")
        later = dict(deepcopy(first), event_ordinal=3)
        later_id = result["segment"]["segment_id"] + ":event:3"
        result["events"] = [first, later]
        result["segment"]["event_ids"].append(later_id)
        result["resolution"]["segments"][-1]["event_ids"].append(later_id)
        result["receipt"]["event_ids"].append(later_id)
        result["execution_identity"]["event_ids"].append(later_id)
        for name, consumer in self._event_carrier_consumers(command).items():
            with self.subTest(form="plural batch", boundary=name):
                consumer(result)
            with self.subTest(form="ambiguous singular", boundary=name), self.assertRaises(ValueError):
                consumer(dict(result, event=deepcopy(first)))

    def test_review_f3_cumulative_receipts_and_exact_child_mapping_use_producer_edges(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            SourceCommandFixture,
            _candidate,
            _interpreter_result,
            _proposal,
            _resolution_source,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.mechanics import ExecutionStore
        from GAME.TOOLS.publication import _accepted_identity
        from GAME.TOOLS.recovery import validate_recovered_basis
        from GAME.TOOLS.runtime_execution import command_policy_basis

        source = SourceCommandFixture()
        self.addCleanup(source.doCleanups)
        command = source.accept_from_sources(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        store = ExecutionStore()
        first = source.execute_from_sources(command, _resolution_source(command), event_payload={"result": 1}, store=store)
        second = source.execute_from_sources(command, first["resolution"], event_payload={"result": 2}, store=store)
        cumulative = deepcopy(second)
        cumulative["receipt"]["segment_refs"] = [first["segment"]["segment_id"], second["segment"]["segment_id"]]
        cumulative["receipt"]["event_ids"] = first["segment"]["event_ids"] + second["segment"]["event_ids"]
        promise = freeze_save_promise(evaluate_durability(campaign_id="campaign-000001", scope="accepted_execution",
            dirty_roots=("runtime.command:" + command["command_id"],), currentness_evidence={"head_sha": H}),
            owner_generations={})

        def consume(value):
            identity = _accepted_identity(command, value)[0].to_dict()
            joined = join_execution_durability(command, value, promise,
                routed_operation=route_serialized_operation("runtime.command", command["command_id"], command))
            recovered = validate_recovered_basis(command, value, catalog_basis=command["catalog_context"],
                policy_basis=command_policy_basis(command))
            self.assertEqual(identity, joined.to_dict()["execution_identity"])
            self.assertEqual(identity, recovered.execution_identity)

        consume(cumulative)
        bad = deepcopy(cumulative)
        bad["receipt"]["event_ids"] = second["segment"]["event_ids"]
        with self.assertRaises(ValueError):
            consume(bad)
        command = deepcopy(command)
        command["pending_child_invocations"] = [{"firing_key": first["event_id"] + ":binding.child",
            "root_command_id": command["command_id"], "activity_id": "activity.check.generic",
            "child_resolution_id": "resolution-child", "trigger_ref": first["event_id"], "reason": "mandatory_followup"}]
        source.retain_lifecycle(command)
        child_state = _resolution_source(command, resolution_id="resolution-child",
            causal_invocation_key=command["pending_child_invocations"][0]["firing_key"])
        child_state.pop("initiating_command_id")
        child = source.execute_from_sources(command, child_state, event_payload={}, store=store)
        consume(child)
        forged_state = dict(child_state, resolution_id="foreign-child", causal_invocation_key="invented-cause")
        forged = source.execute_from_sources(command, forged_state, event_payload={}, store=store)
        for name, consumer in (
            ("publication", lambda: _accepted_identity(command, forged)),
            ("durability", lambda: join_execution_durability(command, forged, promise,
                routed_operation=route_serialized_operation("runtime.command", command["command_id"], command))),
            ("recovery", lambda: validate_recovered_basis(command, forged,
                catalog_basis=command["catalog_context"], policy_basis=command_policy_basis(command))),
        ):
            with self.subTest(boundary=name), self.assertRaises(ValueError):
                consumer()

    def test_review_f3_producer_result_rejects_corrupt_owner_edge_at_all_consumers(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            SourceCommandFixture,
            _candidate,
            _interpreter_result,
            _proposal,
            _resolution_source,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.mechanics import ExecutionStore
        from GAME.TOOLS.publication import _accepted_identity
        from GAME.TOOLS.recovery import validate_recovered_basis
        from GAME.TOOLS.runtime_execution import command_policy_basis

        source = SourceCommandFixture()
        self.addCleanup(source.doCleanups)
        command = source.accept_from_sources(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        result = source.execute_from_sources(command, _resolution_source(command), event_payload={}, store=ExecutionStore())
        promise = freeze_save_promise(evaluate_durability(campaign_id="campaign-000001", scope="accepted_execution",
            dirty_roots=("runtime.command:" + command["command_id"],), currentness_evidence={"head_sha": H}),
            owner_generations={})
        consumers = {
            "publication": lambda value: _accepted_identity(command, value),
            "durability": lambda value: join_execution_durability(command, value, promise,
                routed_operation=route_serialized_operation("runtime.command", command["command_id"], command)),
            "recovery": lambda value: validate_recovered_basis(command, value,
                catalog_basis=command["catalog_context"], policy_basis=command_policy_basis(command)),
        }
        for consumer in consumers.values():
            consumer(result)
        validate_recovered_basis(command, result, catalog_basis=command["catalog_context"],
            policy_basis=command_policy_basis(command), resolution=result["resolution"])
        with self.assertRaises(ValueError):
            validate_recovered_basis(command, result, catalog_basis=command["catalog_context"],
                policy_basis=command_policy_basis(command), resolution=dict(result["resolution"], schema_version=999))
        for label, mutate in (
            ("foreign native R", lambda r: r["resolution"].update(resolution_id="foreign")),
            ("prospective segment", lambda r: r["segment"].update(commit_state="prospective")),
            ("missing embedded segment", lambda r: r["resolution"].update(segments=[])),
            ("unsupported segment schema", lambda r: r["segment"].update(schema_version=999)),
            ("unsupported R schema", lambda r: r["resolution"].update(schema_version=999)),
            ("unsupported receipt shape", lambda r: r["receipt"].update(schema_version=999)),
            ("foreign receipt segment", lambda r: r["receipt"].update(segment_refs=["foreign:segment:1"])),
            ("different embedded segment", lambda r: r["resolution"]["segments"][0].update(receipt_exports={"invented": 1})),
        ):
            wrong = deepcopy(result)
            mutate(wrong)
            self.assertEqual(wrong["execution_identity"], result["execution_identity"])
            for name, consumer in consumers.items():
                with self.subTest(case=label, boundary=name), self.assertRaises(ValueError):
                    consumer(wrong)

    def test_join_rejects_stale_command_schema_and_mixed_variant_before_identity_escape(self):
        command = _accepted_command()
        promise = freeze_save_promise(evaluate_durability(campaign_id="campaign-000001",
            scope="accepted_execution", dirty_roots=("runtime.command:command-000001",),
            currentness_evidence={"head_sha": H}), owner_generations={})
        for wrong in (dict(command, schema_version=3), dict(command, schema_version=True),
                      dict(command, input_fingerprint_generation=2),
                      dict(command, transition_request={})):
            with self.subTest(command=wrong), self.assertRaises(DurabilityContractError):
                join_execution_durability(wrong, _execution(), promise,
                    routed_operation=route_serialized_operation("runtime.command", "command-000001", wrong))

    def test_exact_join_policy_projection_recovers_without_flattened_revision_alias(self):
        from GAME.TOOLS.recovery import validate_recovered_basis

        joined = _execution_join()
        recovered = validate_recovered_basis(_accepted_command(), _execution(),
            catalog_basis=joined.to_dict()["catalog_basis"], policy_basis=joined.to_dict()["policy_basis"])
        self.assertEqual(recovered.execution_identity, joined.to_dict()["execution_identity"])
        self.assertEqual(recovered.fixed_rng_values, (17,))

    def test_join_keeps_accepted_identity_fixed_rng_catalog_and_policy_basis(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="accepted_execution",
            dirty_roots=("runtime.command:command-000001",),
            currentness_evidence={"head_sha": H},
        )
        promise = freeze_save_promise(evaluation, owner_generations={})
        joined = _execution_join()

        self.assertEqual(joined.execution_identity["command_id"], "command-000001")
        self.assertEqual(joined.execution_identity["input_fingerprint"], _accepted_command()["input_fingerprint"])
        self.assertEqual(joined.fixed_rng_values, (17,))
        self.assertEqual(joined.catalog_basis["basis"]["catalog_generation"], 2)
        self.assertEqual(joined.policy_basis_refs, (f"policy.social_leverage@{H}",))
        self.assertTrue(is_execution_durability_join(joined))
        self.assertEqual(joined.accepted_command["command_id"], "command-000001")
        self.assertEqual(joined.routed_operation.relative_path, _command_operation().relative_path)

    def test_join_rejects_execution_identity_replacement(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="accepted_execution",
            dirty_roots=("runtime.command:command-000001",),
            currentness_evidence={"head_sha": H},
        )
        promise = freeze_save_promise(evaluation, owner_generations={})
        execution = _execution()
        execution["accepted_command_id"] = "command-other"

        with self.assertRaisesRegex(DurabilityContractError, "identity"):
            join_execution_durability(
                _accepted_command(), execution, promise, routed_operation=_command_operation()
            )


class DurabilityProjectionTests(unittest.TestCase):
    def test_only_the_published_generation_is_cleared(self) -> None:
        projected = project_durable_generations(
            current={"runtime.command:command-000001": 5},
            published={"runtime.command:command-000001": 4},
        )

        self.assertEqual(projected.durable, {"runtime.command:command-000001": 4})
        self.assertEqual(projected.dirty, {"runtime.command:command-000001": 5})


class Wp13ProofTests(unittest.TestCase):
    def test_shipped_sources_preserve_bounded_non_force_publication_laws(self) -> None:
        persistence = (ROOT / "GAME/CORE/PERSISTENCE.md").read_text(encoding="utf-8")
        save = (ROOT / "GAME/CORE/SAVE_CONTRACT.md").read_text(encoding="utf-8")

        self.assertIn("create_tree(base pinned tree", persistence)
        self.assertIn("update_ref(force=false)", persistence)
        self.assertNotIn("durable_frontier_time", persistence)
        self.assertIn("SAME coherent save transaction", save)
        self.assertIn("checkpoint", save)


class SaveContractCutoverTests(unittest.TestCase):
    def test_save_promise_does_not_create_summary_note_or_checkpoint_authority(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="explicit_save",
            dirty_roots=("world.actor:actor-1",),
            currentness_evidence={"head_sha": H},
        )
        promise = freeze_save_promise(evaluation, owner_generations={})

        self.assertNotIn("summary", promise.required_roots)
        self.assertNotIn("checkpoint", promise.required_roots)


class PersistencePublicationContractTests(unittest.TestCase):
    def test_publication_plan_contains_exact_delta_and_no_immediate_confirmation_read(self) -> None:
        plan = build_connector_git_plan(_attempt())

        self.assertEqual(
            plan.path_operations[_command_operation().relative_path]["command_id"], "command-000001"
        )
        self.assertEqual(plan.confirmation_reads, 0)
        self.assertTrue(plan.requires_currentness_probe)


class ShippedPersistenceDispositionTests(unittest.TestCase):
    def test_storage_metadata_is_not_in_campaign_closure(self) -> None:
        attempt = _attempt()

        self.assertNotIn("DND_STORAGE.yaml", attempt.path_operations)
        self.assertEqual(attempt.native_domains, ("campaign",))


class OperationalRootPublicationTests(unittest.TestCase):
    def test_procedure_publication_does_not_require_execution_join(self) -> None:
        attempt = _procedure_attempt()
        plan = build_connector_git_plan(attempt)

        self.assertIsNone(attempt.execution_durability_join)
        self.assertIsNone(attempt.accepted_identity)
        self.assertIn(
            route_native_record("runtime.procedure", ("procedure-000001",)).relative_path,
            plan.path_operations,
        )
        self.assertIn("STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml", plan.path_operations)

    def test_terminal_procedure_and_root_removal_are_one_campaign_delta(self) -> None:
        attempt = _attempt()
        plan = build_connector_git_plan(attempt)
        operation_paths = set(plan.path_operations)

        self.assertIn(route_native_record("runtime.procedure", ("procedure-000001",)).relative_path, operation_paths)
        self.assertIn("STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml", operation_paths)
        self.assertNotIn(
            route_native_record("runtime.procedure", ("procedure-000001",)).relative_path,
            attempt.deleted_paths,
        )
        self.assertEqual(attempt.root_delta.action, "REMOVE")

    def test_frozen_publication_serializes_terminal_and_root_closure_evidence(self) -> None:
        serialized = _attempt().to_dict()

        self.assertEqual(serialized["procedure_before"]["state"]["lifecycle"], "ACTIVE")
        self.assertEqual(serialized["procedure_after"]["state"]["lifecycle"], "TERMINAL")
        self.assertEqual(serialized["root_delta"]["action"], "REMOVE")
        self.assertTrue(serialized["root_membership_before"]["complete"])


class AcceptedAdjudicationPublicationTests(unittest.TestCase):
    def test_publication_carries_t03_policy_basis_without_resolving_current_policy_again(self) -> None:
        attempt = _attempt()

        self.assertEqual(attempt.policy_basis["source_revision"], H)
        self.assertEqual(attempt.policy_basis["policy_refs"], (f"policy.social_leverage@{H}",))
        self.assertNotIn("current_policy", attempt.policy_basis)


class CatalogDependencyDurabilityTests(unittest.TestCase):
    def test_catalog_dependency_is_explicit_and_not_a_global_frontier(self) -> None:
        evaluation = evaluate_durability(
            campaign_id="campaign-000001",
            scope="accepted_execution",
            dirty_roots=("runtime.command:command-000001",),
            required_dependencies=("catalog.context:b" * 1,),
            currentness_evidence={"head_sha": H},
        )

        self.assertEqual(evaluation.required_dependencies, ("catalog.context:b",))
        self.assertFalse(hasattr(evaluation, "global_frontier"))


class CampaignIdentityImmutabilityTests(unittest.TestCase):
    def test_campaign_id_and_manifest_card_identity_must_remain_canonical(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "campaign identity"):
            _attempt(campaign_id="campaign-other")

        with self.assertRaisesRegex(PublicationContractError, "campaign name"):
            _attempt(campaign_card={"campaign_id": "campaign-000001", "campaign_name": "Other"})

    def test_campaign_name_change_is_a_synchronized_projection_not_card_authority(self) -> None:
        attempt = _attempt(
            manifest={
                "campaign_id": "campaign-000001",
                "campaign_name": "New Name",
                "branch": "campaign/20260916",
                "created_at": "2026-09-16T12:00:00Z",
            },
            campaign_card={"campaign_id": "campaign-000001", "campaign_name": "New Name"},
        )

        self.assertEqual(attempt.campaign_identity.campaign_id, "campaign-000001")
        self.assertEqual(attempt.campaign_identity.campaign_name, "New Name")

    def test_campaign_id_mutation_is_rejected_even_when_card_is_also_changed(self) -> None:
        with self.assertRaisesRegex(PublicationContractError, "immutable"):
            _attempt(
                path_operations={
                    "MANIFEST.yaml": {"campaign_id": "campaign-other", "campaign_name": "The Frostfall"},
                    "CAMPAIGN_CARD.yaml": {"campaign_id": "campaign-other", "campaign_name": "The Frostfall"},
                    _command_operation().relative_path: _accepted_command(),
                }
            )

    def test_manifest_branch_and_created_at_are_immutable_result_fields(self) -> None:
        manifest = {
            "campaign_id": "campaign-000001",
            "campaign_name": "The Frostfall",
            "branch": "campaign/other",
            "created_at": "2026-09-16T12:00:00Z",
        }
        with self.assertRaisesRegex(PublicationContractError, "immutable"):
            _attempt(
                path_operations={
                    "MANIFEST.yaml": manifest,
                    _command_operation().relative_path: _accepted_command(),
                }
            )

        manifest["branch"] = "campaign/20260916"
        manifest["created_at"] = "2026-09-17T12:00:00Z"
        with self.assertRaisesRegex(PublicationContractError, "immutable"):
            _attempt(
                path_operations={
                    "MANIFEST.yaml": manifest,
                    _command_operation().relative_path: _accepted_command(),
                }
            )


class AuthorizedDurabilityHandoffTests(unittest.TestCase):
    def test_only_owner_issued_handoff_promise_may_enroll_unresolved_interaction(self) -> None:
        from DEV.TESTS.test_sp03_authenticated_input import input_sources
        interaction, _, _ = input_sources(kind="intent")
        interaction["state"]["campaign_id"] = "campaign-000001"
        promise = issue_durability_handoff_promise(
            campaign_id="campaign-000001",
            owner_kind="runtime.interaction",
            native_owner=interaction,
            scope="accepted_handoff",
        )

        delta = derive_operational_root_delta(
            "campaign-000001", "runtime.interaction", interaction, accepted_promise=promise
        )
        self.assertEqual(delta.action, "ENROLL")

    def test_handoff_issuance_rejects_cross_campaign_and_resolved_or_fabricated_owner(self) -> None:
        from DEV.TESTS.test_sp03_authenticated_input import input_sources
        interaction, _, _ = input_sources(kind="intent")
        interaction["state"]["campaign_id"] = "campaign-000001"
        with self.assertRaisesRegex(DurabilityContractError, "campaign"):
            issue_durability_handoff_promise(
                campaign_id="campaign-other",
                owner_kind="runtime.interaction",
                native_owner=interaction,
                scope="accepted_handoff",
            )

        # Emission alone cannot discharge promised semantic meaning.
        interaction["state"]["response_message_id"] = "message-2"
        issued = issue_durability_handoff_promise(
            campaign_id="campaign-000001", owner_kind="runtime.interaction",
            native_owner=interaction, scope="accepted_handoff",
        )
        self.assertEqual(issued.owner_id, interaction["id"])

        with self.assertRaisesRegex(DurabilityContractError, "native owner"):
            issue_durability_handoff_promise(
                campaign_id="campaign-000001",
                owner_kind="runtime.interaction",
                native_owner={"kind": "runtime.interaction", "input_message_id": "message-1"},
                scope="accepted_handoff",
            )

    def test_arbitrary_promise_shape_is_not_an_authority_boundary(self) -> None:
        interaction = {
            "kind": "runtime.interaction",
            "campaign_id": "campaign-000001",
            "input_message_id": "message-1",
        }

        class ArbitraryPromise:
            def validate(self, **_kwargs: object) -> bool:
                return True

        with self.assertRaisesRegex(Exception, "authorized|native owner|session_id"):
            derive_operational_root_delta(
                "campaign-000001",
                "runtime.interaction",
                interaction,
                accepted_promise=ArbitraryPromise(),
            )


if __name__ == "__main__":
    unittest.main()
