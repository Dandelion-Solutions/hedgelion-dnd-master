from __future__ import annotations

import copy
from collections.abc import Mapping
from dataclasses import fields
import unittest

from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
from GAME.TOOLS.policy_basis import (
    ApplicabilityEvidence,
    AuthenticatedPrincipalEvidence,
    AdoptionEvidence,
    CreatorEvidence,
    PolicyBasisResolutionError,
    PolicyBasisResolver,
    PolicySelection,
    PinnedCampaign,
    PlayerEvidence,
)
from GAME.TOOLS.runtime_execution import accept_command
from GAME.TOOLS.recovery import (
    CheckpointDescriptorError,
    CurrentNativeSource,
    HistoricalRepairCandidate,
    MaintenanceAudit,
    RecoveryFailure,
    RecoveryFailureCode,
    RecoveredExecution,
    RecoverySourceError,
    export_checkpoint_diagnostics,
    hydrate_operational_roots,
    promote_historical_repair,
    record_maintenance_audit,
    recover_current_runtime,
    reset_last_checkpoint_reference,
    select_current_native_sources,
    validate_checkpoint_descriptor,
    validate_repair_candidate,
    validate_recovered_basis,
)


H = "0123456789abcdef0123456789abcdef01234567"
TREE = "abcdef0123456789abcdef0123456789abcdef01"


def _sidecar(*, source_path: str = "RULES/HOUSE_RULES.md") -> dict[str, object]:
    return {
        "schema_version": 1,
        "source_path": source_path,
        "policies": [
            {
                "policy_id": "policy.social_leverage",
                "kind": "house_rule",
                "authority_class": "INTERPRETIVE_POLICY",
                "lifecycle": "active",
                "source_anchor": "#social-leverage",
                "routing_keys": ["social"],
                "adoption_basis": "active_player_interpretive",
                "adopted_by_player_id": "player-1",
                "supersedes_policy_ids": [],
                "realization_refs": ["activity.check.generic"],
            }
        ],
    }


def _normative() -> str:
    return "# Правила\n\n## Social Leverage\n\nThe adopted ruling applies to social leverage.\n"


class FakeRepository:
    def __init__(self) -> None:
        self.reads: list[tuple[str, str]] = []
        self.files: dict[str, object] = {
            "MANIFEST.yaml": {"rules": {"house_rules_path": "RULES/HOUSE_RULES.md"}},
            "RULES/HOUSE_RULES.yaml": _sidecar(),
            "RULES/HOUSE_RULES.md": _normative(),
        }

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        return PinnedCampaign(campaign_id=campaign_id, revision=H, tree_sha=TREE)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        self.reads.append((pinned.revision, path))
        return copy.deepcopy(self.files[path])


class FakeAccess:
    def resolve_principal(self, pinned: PinnedCampaign) -> AuthenticatedPrincipalEvidence:
        return AuthenticatedPrincipalEvidence(principal_id="principal-1")

    def resolve_creator(self, pinned: PinnedCampaign) -> CreatorEvidence:
        return CreatorEvidence(principal_id="creator-1")

    def resolve_active_player(
        self, pinned: PinnedCampaign, principal: AuthenticatedPrincipalEvidence
    ) -> PlayerEvidence:
        return PlayerEvidence(player_id="player-1", mechanical_override_policy=False)

    def prove_policy_adoption(
        self,
        pinned: PinnedCampaign,
        policy: dict[str, object],
        principal: AuthenticatedPrincipalEvidence,
        creator: CreatorEvidence,
        player: PlayerEvidence,
    ) -> AdoptionEvidence:
        return AdoptionEvidence(
            authority_class="INTERPRETIVE_POLICY",
            adoption_basis="active_player_interpretive",
            adopted_by_player_id="player-1",
        )


class FakeApplicability:
    def prove_policy_applicability(
        self,
        pinned: PinnedCampaign,
        policy: dict[str, object],
        consumer_id: str,
    ) -> ApplicabilityEvidence:
        return ApplicabilityEvidence(policy_id=str(policy["policy_id"]), consumer_id=consumer_id)


class ExactPolicyBasisResolutionTests(unittest.TestCase):
    def test_resolves_one_policy_from_exact_pinned_sidecar_and_normative_anchor(self) -> None:
        repository = FakeRepository()
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        result = resolver.resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )

        self.assertEqual(result.policy_ref, f"policy.social_leverage@{H}")
        self.assertEqual(result.campaign_revision, H)
        self.assertEqual(
            repository.reads,
            [
                (H, "MANIFEST.yaml"),
                (H, "RULES/HOUSE_RULES.yaml"),
                (H, "RULES/HOUSE_RULES.md"),
            ],
        )
        self.assertEqual(result.realization_refs, ("activity.check.generic",))

    def test_untrusted_mapping_cannot_supply_authority_applicability_path_or_revision(self) -> None:
        resolver = PolicyBasisResolver(FakeRepository(), FakeAccess(), FakeApplicability())
        forged = {
            "policy_id": "policy.social_leverage",
            "consumer_id": "activity.check.generic",
            "campaign_revision": H,
            "source_path": "RULES/HOUSE_RULES.md",
            "authority_validated": True,
            "applicable": True,
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "typed policy selection"):
            resolver.resolve("campaign-1", forged, catalog_context=_bind_context())

    def test_missing_normative_anchor_fails_before_realization(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["source_anchor"] = "#missing"
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "normative anchor"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )


    def test_missing_realization_is_a_typed_gap(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["realization_refs"] = ["activity.not_admitted"]
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "realization gap"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )


    def test_owner_evidence_must_be_typed_and_is_not_a_caller_boolean(self) -> None:
        class UntrustedAccess(FakeAccess):
            def resolve_principal(self, pinned: PinnedCampaign) -> dict[str, object]:
                return {"principal_id": "principal-1", "authenticated": True}

        resolver = PolicyBasisResolver(FakeRepository(), UntrustedAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "owner-typed evidence"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )


    def test_sidecar_duplicate_policy_identity_is_rejected(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"].append(copy.deepcopy(sidecar["policies"][0]))
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "policy IDs must be unique"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_untrusted_repository_pin_cannot_select_a_revision(self) -> None:
        class UntrustedRepository(FakeRepository):
            def pin_campaign(self, campaign_id: str) -> dict[str, str]:
                return {"campaign_id": campaign_id, "revision": H, "tree_sha": TREE}

        resolver = PolicyBasisResolver(UntrustedRepository(), FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "trusted exact campaign pin"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_sidecar_authority_class_and_adoption_basis_must_obey_access_law(self) -> None:
        class InvalidShapeAccess(FakeAccess):
            def prove_policy_adoption(
                self,
                pinned: PinnedCampaign,
                policy: dict[str, object],
                principal: AuthenticatedPrincipalEvidence,
                creator: CreatorEvidence,
                player: PlayerEvidence,
            ) -> AdoptionEvidence:
                return AdoptionEvidence(
                    authority_class="INTERPRETIVE_POLICY",
                    adoption_basis="campaign_creator",
                    adopted_by_player_id=None,
                )

        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["adoption_basis"] = "campaign_creator"
        sidecar["policies"][0]["adopted_by_player_id"] = None
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, InvalidShapeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "adoption basis is not admitted"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_sidecar_and_manifest_house_rules_paths_must_match(self) -> None:
        repository = FakeRepository()
        repository.files["RULES/HOUSE_RULES.yaml"] = _sidecar(source_path="RULES/OTHER_RULES.md")
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "paths differ"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_policy_selection_rejects_consumer_outside_active_adjudication_surface(self) -> None:
        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted adjudication consumer"):
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.not_admitted")

    def test_direct_resolved_policy_basis_construction_is_not_a_provenance_source(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        values = {
            item.name: getattr(resolved, item.name)
            for item in fields(resolved)
            if not item.name.startswith("_")
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "resolver-issued"):
            type(resolved)(**values)

    def test_object_new_forged_policy_basis_cannot_bind_accepted_inputs(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        forged = object.__new__(type(resolved))
        for item in fields(resolved):
            object.__setattr__(forged, item.name, getattr(resolved, item.name))
        object.__setattr__(forged, "policy_ref", "policy.forged@" + "f" * 40)

        with self.assertRaisesRegex(PolicyBasisResolutionError, "resolver-issued"):
            PolicyBasisResolver.bind_accepted_basis(
                {
                    "dc": {
                        "source_class": "INVOCATION_ADJUDICATED",
                        "value": 15,
                        "provenance_ref": "turn-1:dc",
                        "eligibility_basis_fingerprint": "eligibility-A",
                        "rules_context_fingerprint": "rules-A",
                        "policy_basis_refs": [forged.policy_ref],
                    }
                },
                (),
                (forged,),
            )

    def test_invocation_fact_must_use_the_exact_admitted_fact_edge(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.spell.fire_bolt"),
            catalog_context=_bind_context(),
        )
        fact = {
            "fact_id": "fiction.target_visible",
            "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "turn-1:reachable",
            "consumer_id": "activity.spell.fire_bolt",
            "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64,
            "policy_basis_refs": [resolved.policy_ref],
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted fact edge"):
            PolicyBasisResolver.bind_accepted_basis({}, (fact,), (resolved,))

    def test_invocation_fact_consumer_must_be_one_of_the_seven_compiled_edges(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        fact = {
            "fact_id": "fiction.target_reachable",
            "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "turn-1:reachable",
            "consumer_id": "activity.not_admitted",
            "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64,
            "policy_basis_refs": [resolved.policy_ref],
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted fact consumer"):
            PolicyBasisResolver.bind_accepted_basis({}, (fact,), (resolved,))

    def test_applicability_witness_must_match_the_selected_consumer(self) -> None:
        class CrossConsumerApplicability(FakeApplicability):
            def prove_policy_applicability(
                self,
                pinned: PinnedCampaign,
                policy: dict[str, object],
                consumer_id: str,
            ) -> ApplicabilityEvidence:
                return ApplicabilityEvidence(
                    policy_id=str(policy["policy_id"]), consumer_id="activity.save.generic"
                )

        resolver = PolicyBasisResolver(FakeRepository(), FakeAccess(), CrossConsumerApplicability())
        with self.assertRaisesRegex(PolicyBasisResolutionError, "applicability evidence identity mismatch"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )



class CurrentSourceSelectionTests(unittest.TestCase):
    def test_selects_owner_native_current_source_not_checkpoint_or_lexical_latest(self) -> None:
        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (
                    CurrentNativeSource(
                        campaign_id=pinned.campaign_id,
                        domain="campaign",
                        source_id="campaign/current",
                        revision=pinned.revision,
                        relative_path="MANIFEST.yaml",
                    ),
                )

        repository = Repository()
        selected = select_current_native_sources(
            repository,
            "campaign-1",
            checkpoint_hint={"revision": "f" * 40},
        )

        self.assertEqual(selected[0].revision, H)
        self.assertEqual(selected[0].source_id, "campaign/current")
        self.assertEqual(repository.reads, [])

    def test_missing_owner_native_route_is_typed_incomplete_failure(self) -> None:
        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return ()

        with self.assertRaises(RecoverySourceError) as raised:
            select_current_native_sources(Repository(), "campaign-1")

        self.assertEqual(raised.exception.code, RecoveryFailureCode.INCOMPLETE)


def _accepted_command_for_recovery() -> dict[str, object]:
    return {
        "command_id": "command-000001",
        "input_fingerprint": "a" * 64,
        "catalog_context": {
            "catalog_generation": 2,
            "catalog_context_fingerprint": "b" * 64,
            "ruleset_set_sha256": "c" * 64,
        },
        "action_request": {
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
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
        "invocation_facts": [],
    }


def _execution_for_recovery() -> dict[str, object]:
    return {
        "accepted_command_id": "command-000001",
        "accepted_input_fingerprint": "a" * 64,
        "resolution_id": "resolution-000001",
        "segment": {"segment_id": "resolution-000001:segment:1", "segment_sequence": 1},
        "event": {
            "segment_id": "resolution-000001:segment:1",
            "event_ordinal": 1,
            "event_id": "resolution-000001:segment:1:event:1",
        },
        "event_id": "resolution-000001:segment:1:event:1",
        "roll_result": {
            "roll_id": "resolution-000001:roll:1",
            "request_id": "resolution-000001:roll:1",
            "expression": "fixed",
            "raw_values": [17],
            "source_kind": "rng.system",
            "provenance_ref": "resolution-000001:rng:1",
        },
    }


def _policy_basis_for_recovery(
    command: Mapping[str, object], refs: list[str] | None = None, *, source_revision: str = H
) -> dict[str, object]:
    return {
        "policy_refs": [f"policy.social_leverage@{source_revision}"] if refs is None else refs,
        "source_revision": source_revision,
        "action_request": copy.deepcopy(command["action_request"]),
        "invocation_facts": copy.deepcopy(command["invocation_facts"]),
    }


def _validated_command_closure(
    *, include_policy: bool = False
) -> tuple[dict[str, object], dict[str, object], dict[str, object], object, dict[str, str]]:
    context = _bind_context()
    accepted_basis = None
    resolved_policy = None
    if include_policy:
        resolved_policy = PolicyBasisResolver(FakeRepository(), FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=context,
        )
        accepted_basis = PolicyBasisResolver.bind_accepted_basis(
            {
                "dc": {
                    "source_class": "INVOCATION_ADJUDICATED",
                    "value": 15,
                    "provenance_ref": "turn-1:dc",
                    "eligibility_basis_fingerprint": "eligibility-A",
                    "rules_context_fingerprint": "rules-A",
                    "policy_basis_refs": [resolved_policy.policy_ref],
                }
            },
            (),
            (resolved_policy,),
        )
    action_request: dict[str, object] = {
        "activity_id": "activity.check.generic",
        "actor_id": "actor-1",
        "target_ids": ["actor-2"],
    }
    if accepted_basis is not None:
        action_request["parameter_bindings"] = accepted_basis.runtime_parameter_bindings()
    accepted = accept_command(
        {
            "kind": "interpreter_result",
            "purpose": "interpret",
            "bundle_id": "bundle-1",
            "source_generation": "frontier-7",
            "intent": "make a check",
        },
        context,
        {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        {
            "command_id": "turn-1-cmd-01",
            "interaction_id": "turn-1",
            "intent_plan_id": "turn-1-plan",
            "clause_id": "c1",
            "action_request": action_request,
            "root_resolution_id": "resolution-1",
        },
        adjudication_basis=accepted_basis,
    )
    if not isinstance(accepted, dict):
        raise AssertionError("test command must be accepted")
    segment_id = "resolution-1:segment:1"
    event_id = f"{segment_id}:event:1"
    roll = {
        "roll_id": "resolution-1:roll:1",
        "request_id": "resolution-1:roll:1",
        "expression": "fixed",
        "raw_values": [17],
        "source_kind": "rng.system",
        "provenance_ref": "resolution-1:rng:1",
    }
    segment = {
        "segment_id": segment_id,
        "segment_sequence": 1,
        "commit_state": "committed",
        "event_ids": [event_id],
    }
    execution = {
        "accepted_command_id": accepted["command_id"],
        "accepted_input_fingerprint": accepted["input_fingerprint"],
        "execution_owner_id": "resolution-1",
        "resolution_id": "resolution-1",
        "segment": segment,
        "event": {
            "segment_id": segment_id,
            "event_ordinal": 1,
            "event_id": event_id,
        },
        "event_id": event_id,
        "roll_result": roll,
    }
    resolution = {
        "resolution_id": "resolution-1",
        "root_command_id": accepted["command_id"],
        "segments": [segment],
        "fixed_rng_results": [roll],
    }
    policy = _policy_basis_for_recovery(
        accepted,
        [] if resolved_policy is None else [resolved_policy.policy_ref],
        source_revision=H,
    )
    closure = {
        "accepted_command": accepted,
        "execution": execution,
        "resolution": resolution,
        "catalog_basis": accepted["catalog_context"],
        "policy_basis": policy,
        "candidate": {"definition_id": "activity.check.generic", "kind": "definition.activity"},
    }
    return accepted, execution, closure, context, {"command_id": str(accepted["command_id"]), "path": ""}


class CheckpointDescriptorTests(unittest.TestCase):
    def test_descriptor_has_narrow_identity_and_campaign_association(self) -> None:
        descriptor = validate_checkpoint_descriptor(
            {
                "schema_version": 4,
                "id": "checkpoint-1",
                "campaign_id": "campaign-1",
                "created_at": "2026-09-18T00:00:00Z",
            },
            campaign_id="campaign-1",
            selected_id="checkpoint-1",
        )

        self.assertEqual(descriptor.id, "checkpoint-1")
        self.assertFalse(hasattr(descriptor, "valid_through_event_id"))

    def test_retired_or_stale_descriptor_fails_typed(self) -> None:
        base = {
            "schema_version": 4,
            "id": "checkpoint-1",
            "campaign_id": "campaign-1",
        }
        with self.assertRaises(CheckpointDescriptorError) as retired:
            validate_checkpoint_descriptor(base | {"valid_through_event_id": "event-1"}, campaign_id="campaign-1")
        self.assertEqual(retired.exception.code, RecoveryFailureCode.CORRUPT)

        with self.assertRaises(CheckpointDescriptorError) as stale:
            validate_checkpoint_descriptor(base, campaign_id="campaign-1", selected_id="checkpoint-2")
        self.assertEqual(stale.exception.code, RecoveryFailureCode.STALE)


class AcceptedExecutionRecoveryTests(unittest.TestCase):
    def test_recovery_preserves_command_event_and_fixed_rng_identity(self) -> None:
        command = _accepted_command_for_recovery()
        execution = _execution_for_recovery()
        recovered = validate_recovered_basis(
            command,
            execution,
            catalog_basis=command["catalog_context"],
            policy_basis=_policy_basis_for_recovery(command),
        )

        self.assertIsInstance(recovered, RecoveredExecution)
        self.assertEqual(recovered.command_id, command["command_id"])
        self.assertEqual(recovered.event_id, execution["event_id"])
        self.assertEqual(recovered.fixed_rng_values, (17,))
        self.assertEqual(recovered.catalog_basis, command["catalog_context"])

    def test_recovery_rejects_identity_or_basis_replacement_before_replay(self) -> None:
        command = _accepted_command_for_recovery()
        execution = _execution_for_recovery()
        with self.assertRaises(RecoveryFailure) as identity:
            validate_recovered_basis(
                command,
                execution | {"accepted_command_id": "command-other"},
                catalog_basis=command["catalog_context"],
                policy_basis=_policy_basis_for_recovery(command),
            )
        self.assertEqual(identity.exception.code, RecoveryFailureCode.CORRUPT)

        with self.assertRaises(RecoveryFailure) as policy:
            validate_recovered_basis(
                command,
                execution,
                catalog_basis=command["catalog_context"],
                policy_basis=_policy_basis_for_recovery(
                    command, [f"policy.social_leverage@{'f' * 40}"], source_revision="f" * 40
                ),
            )
        self.assertEqual(policy.exception.code, RecoveryFailureCode.STALE)

    def test_recovery_rejects_arbitrary_event_ordinal_and_derived_event_id(self) -> None:
        command = _accepted_command_for_recovery()
        execution = _execution_for_recovery()
        forged_event_id = "resolution-000001:segment:1:event:99"
        forged_event = dict(execution["event"])
        forged_event["event_ordinal"] = 99
        forged_event["event_id"] = forged_event_id
        forged = execution | {"event": forged_event, "event_id": forged_event_id}

        with self.assertRaises(RecoveryFailure) as raised:
            validate_recovered_basis(
                command,
                forged,
                catalog_basis=command["catalog_context"],
                policy_basis=_policy_basis_for_recovery(command),
            )
        self.assertEqual(raised.exception.code, RecoveryFailureCode.CORRUPT)

    def test_recovery_accepts_owner_derived_later_segment_and_roll_identity(self) -> None:
        command = _accepted_command_for_recovery()
        execution = _execution_for_recovery()
        segment_id = "resolution-000001:segment:2"
        event_id = f"{segment_id}:event:3"
        roll_id = "resolution-000001:roll:7"
        later_segment = {
            "segment_id": segment_id,
            "segment_sequence": 2,
            "event_ids": [event_id],
        }
        later_event = {
            "segment_id": segment_id,
            "event_ordinal": 3,
            "event_id": event_id,
        }
        later_roll = {
            "roll_id": roll_id,
            "request_id": roll_id,
            "expression": "fixed",
            "raw_values": [19],
            "source_kind": "rng.system",
            "provenance_ref": "resolution-000001:rng:7",
        }
        later_execution = execution | {
            "segment": later_segment,
            "event": later_event,
            "event_id": event_id,
            "roll_result": later_roll,
        }
        resolution = {
            "resolution_id": "resolution-000001",
            "root_command_id": command["command_id"],
            "segments": [later_segment],
            "fixed_rng_results": [later_roll],
        }

        recovered = validate_recovered_basis(
            command,
            later_execution,
            catalog_basis=command["catalog_context"],
            policy_basis=_policy_basis_for_recovery(command),
            resolution=resolution,
        )

        self.assertEqual(recovered.segment_id, segment_id)
        self.assertEqual(recovered.event_id, event_id)
        self.assertEqual(recovered.fixed_rng_values, (19,))

    def test_recovery_rejects_mutually_forged_policy_refs(self) -> None:
        command = _accepted_command_for_recovery()
        action_request = copy.deepcopy(command["action_request"])
        action_request["parameter_bindings"]["dc"]["policy_basis_refs"] = [f"policy.forged@{H}"]
        forged_command = command | {"action_request": action_request}
        forged_policy = {
            "policy_refs": [f"policy.forged@{H}"],
            "source_revision": H,
            "action_request": command["action_request"],
            "invocation_facts": [],
        }

        with self.assertRaises(RecoveryFailure) as raised:
            validate_recovered_basis(
                forged_command,
                _execution_for_recovery(),
                catalog_basis=command["catalog_context"],
                policy_basis=forged_policy,
            )
        self.assertEqual(raised.exception.code, RecoveryFailureCode.CORRUPT)


class OperationalRootRecoveryTests(unittest.TestCase):
    def test_hydrates_each_complete_root_through_its_exact_native_route(self) -> None:
        root = {
            "owner_kind": "runtime.command",
            "owner_id": "command-000001",
            "route": {
                "family_key": "runtime.command",
                "identity": ["command-000001"],
                "relative_path": "",
            },
        }
        from GAME.TOOLS.native_storage import route_native_record

        root["route"]["relative_path"] = route_native_record(
            "runtime.command", ("command-000001",)
        ).relative_path
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [root],
        }

        class Repository(FakeRepository):
            def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
                if path == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return page
                if path == root["route"]["relative_path"]:
                    return {
                        "kind": "runtime.command",
                        "command_id": "command-000001",
                        "disposition": "command.accepted",
                        "pending_child_invocations": [],
                        "direct_transition_receipt": {"status": "PUBLISH_REQUIRED"},
                    }
                return super().read_exact_path(pinned, path)

        hydrated = hydrate_operational_roots(
            Repository(),
            PinnedCampaign("campaign-1", H, TREE),
            page,
        )
        self.assertEqual(hydrated[0]["command_id"], "command-000001")

    def test_terminal_root_is_not_hydrated_as_active_recovery_work(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        path = route_native_record("runtime.command", ("command-000001",)).relative_path
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [
                {
                    "owner_kind": "runtime.command",
                    "owner_id": "command-000001",
                    "route": {
                        "family_key": "runtime.command",
                        "identity": ["command-000001"],
                        "relative_path": path,
                    },
                }
            ],
        }

        class Repository(FakeRepository):
            def read_exact_path(self, pinned: PinnedCampaign, requested: str) -> object:
                if requested == path:
                    return {
                        "kind": "runtime.command",
                        "command_id": "command-000001",
                        "disposition": "command.settled",
                        "pending_child_invocations": [],
                        "direct_transition_receipt": {"status": "CONFIRMED"},
                    }
                return super().read_exact_path(pinned, requested)

        with self.assertRaises(RecoveryFailure) as raised:
            hydrate_operational_roots(Repository(), PinnedCampaign("campaign-1", H, TREE), page)
        self.assertEqual(raised.exception.code, RecoveryFailureCode.STALE)

    def test_incomplete_root_page_cannot_fall_back_to_a_directory_scan(self) -> None:
        with self.assertRaises(RecoveryFailure) as raised:
            hydrate_operational_roots(
                FakeRepository(),
                PinnedCampaign("campaign-1", H, TREE),
                {"schema_version": 1, "campaign_id": "campaign-1", "complete": False, "roots": []},
            )
        self.assertEqual(raised.exception.code, RecoveryFailureCode.INCOMPLETE)


class RecoveryCurrentRuntimeTests(unittest.TestCase):
    def test_current_runtime_recovery_does_not_require_checkpoint_or_hot_authority(self) -> None:
        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (
                    CurrentNativeSource(
                        pinned.campaign_id, "campaign", "campaign/current", pinned.revision, "MANIFEST.yaml"
                    ),
                )

            def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
                if path == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return {"schema_version": 1, "campaign_id": pinned.campaign_id, "complete": True, "roots": []}
                return super().read_exact_path(pinned, path)

        result = recover_current_runtime(
            Repository(),
            "campaign-1",
            checkpoint={"schema_version": 4, "id": "old", "campaign_id": "campaign-1"},
            hot_state={"source_basis": {"campaign": "f" * 40}, "owners": {"invented": True}},
        )

        self.assertEqual(result.disposition, "READY")
        self.assertFalse(result.hot_authoritative)
        self.assertEqual(result.sources[0].revision, H)

    def test_current_runtime_does_not_return_ready_before_command_closure_validation(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        path = route_native_record("runtime.command", ("command-000001",)).relative_path
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [
                {
                    "owner_kind": "runtime.command",
                    "owner_id": "command-000001",
                    "route": {
                        "family_key": "runtime.command",
                        "identity": ["command-000001"],
                        "relative_path": path,
                    },
                }
            ],
        }

        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (CurrentNativeSource(pinned.campaign_id, "campaign", "campaign/current", H, "MANIFEST.yaml"),)

            def read_exact_path(self, pinned: PinnedCampaign, requested: str) -> object:
                if requested == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return page
                if requested == path:
                    return {
                        "kind": "runtime.command",
                        "command_id": "command-000001",
                        "disposition": "command.accepted",
                        "pending_child_invocations": [],
                        "direct_transition_receipt": {"status": "PUBLISH_REQUIRED"},
                        "closure": {},
                    }
                return super().read_exact_path(pinned, requested)

        with self.assertRaises(RecoveryFailure) as raised:
            recover_current_runtime(Repository(), "campaign-1")
        self.assertEqual(raised.exception.code, RecoveryFailureCode.INCOMPLETE)

    def test_current_runtime_hydrates_t05_command_and_execution_sources_before_ready(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        accepted, execution, closure, context, identity = _validated_command_closure(include_policy=True)
        path = route_native_record("runtime.command", (identity["command_id"],)).relative_path
        resolution = copy.deepcopy(closure["resolution"])
        resolution_path = route_native_record(
            "runtime.resolution", (str(accepted["root_resolution_id"]),)
        ).relative_path
        event = copy.deepcopy(execution["event"])
        event["root_command_id"] = accepted["command_id"]
        event["causal_ref"] = accepted["root_resolution_id"]
        event_path = route_native_record(
            "runtime.mechanical_event", (str(execution["event_id"]),)
        ).relative_path
        root = {
            "owner_kind": "runtime.command",
            "owner_id": identity["command_id"],
            "route": {
                "family_key": "runtime.command",
                "identity": [identity["command_id"]],
                "relative_path": path,
            },
        }
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [root],
        }

        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (CurrentNativeSource(pinned.campaign_id, "campaign", "campaign/current", H, "MANIFEST.yaml"),)

            def read_exact_path(self, pinned: PinnedCampaign, requested: str) -> object:
                self.reads.append((pinned.revision, requested))
                if requested == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return page
                if requested == path:
                    return accepted
                if requested == resolution_path:
                    return resolution
                if requested == event_path:
                    return event
                return super().read_exact_path(pinned, requested)

            def resolve_recovery_catalog_context(
                self,
                pinned: PinnedCampaign,
                accepted_command: Mapping[str, object],
                catalog_basis: Mapping[str, object],
            ) -> tuple[object, Mapping[str, str]]:
                return context, {"definition_id": "activity.check.generic", "kind": "definition.activity"}

            def resolve_recovery_policy_basis(
                self,
                pinned: PinnedCampaign,
                accepted_command: Mapping[str, object],
                policy_refs: tuple[str, ...],
            ) -> Mapping[str, object]:
                self.read_exact_path(pinned, "MANIFEST.yaml")
                self.read_exact_path(pinned, "RULES/HOUSE_RULES.yaml")
                self.read_exact_path(pinned, "RULES/HOUSE_RULES.md")
                return {"source_revision": pinned.revision}

        repository = Repository()
        result = recover_current_runtime(repository, "campaign-1")
        self.assertEqual(result.disposition, "READY")
        self.assertEqual(result.hydrated_owners[0]["command_id"], identity["command_id"])
        reads = [path for _revision, path in repository.reads]
        self.assertIn(path, reads)
        self.assertIn(resolution_path, reads)
        self.assertIn(event_path, reads)
        self.assertIn("MANIFEST.yaml", reads)
        self.assertIn("RULES/HOUSE_RULES.yaml", reads)
        self.assertIn("RULES/HOUSE_RULES.md", reads)

    def test_current_runtime_rejects_missing_resolution_root_command_id(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        accepted, execution, closure, context, identity = _validated_command_closure()
        command_path = route_native_record("runtime.command", (identity["command_id"],)).relative_path
        resolution_path = route_native_record(
            "runtime.resolution", (str(accepted["root_resolution_id"]),)
        ).relative_path
        event_path = route_native_record(
            "runtime.mechanical_event", (str(execution["event_id"]),)
        ).relative_path
        resolution = copy.deepcopy(closure["resolution"])
        del resolution["root_command_id"]
        command_owner = copy.deepcopy(accepted)
        command_owner["kind"] = "runtime.command"
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [
                {
                    "owner_kind": "runtime.command",
                    "owner_id": identity["command_id"],
                    "route": {
                        "family_key": "runtime.command",
                        "identity": [identity["command_id"]],
                        "relative_path": command_path,
                    },
                }
            ],
        }

        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (CurrentNativeSource(pinned.campaign_id, "campaign", "campaign/current", H, "MANIFEST.yaml"),)

            def read_exact_path(self, pinned: PinnedCampaign, requested: str) -> object:
                if requested == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return page
                if requested == command_path:
                    return command_owner
                if requested == resolution_path:
                    return resolution
                if requested == event_path:
                    return execution["event"]
                return super().read_exact_path(pinned, requested)

            def resolve_recovery_catalog_context(
                self,
                pinned: PinnedCampaign,
                accepted_command: Mapping[str, object],
                catalog_basis: Mapping[str, object],
            ) -> tuple[object, Mapping[str, str]]:
                return context, {"definition_id": "activity.check.generic", "kind": "definition.activity"}

        with self.assertRaises(RecoveryFailure) as raised:
            recover_current_runtime(Repository(), "campaign-1")
        self.assertEqual(raised.exception.code, RecoveryFailureCode.INCOMPLETE)

    def test_current_runtime_rejects_mismatched_resolution_root_command_id(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        accepted, execution, closure, context, identity = _validated_command_closure()
        command_path = route_native_record("runtime.command", (identity["command_id"],)).relative_path
        resolution_path = route_native_record(
            "runtime.resolution", (str(accepted["root_resolution_id"]),)
        ).relative_path
        event_path = route_native_record(
            "runtime.mechanical_event", (str(execution["event_id"]),)
        ).relative_path
        resolution = copy.deepcopy(closure["resolution"])
        resolution["root_command_id"] = "command-forged"
        command_owner = copy.deepcopy(accepted)
        command_owner["kind"] = "runtime.command"
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [
                {
                    "owner_kind": "runtime.command",
                    "owner_id": identity["command_id"],
                    "route": {
                        "family_key": "runtime.command",
                        "identity": [identity["command_id"]],
                        "relative_path": command_path,
                    },
                }
            ],
        }

        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (CurrentNativeSource(pinned.campaign_id, "campaign", "campaign/current", H, "MANIFEST.yaml"),)

            def read_exact_path(self, pinned: PinnedCampaign, requested: str) -> object:
                if requested == "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml":
                    return page
                if requested == command_path:
                    return command_owner
                if requested == resolution_path:
                    return resolution
                if requested == event_path:
                    return execution["event"]
                return super().read_exact_path(pinned, requested)

            def resolve_recovery_catalog_context(
                self,
                pinned: PinnedCampaign,
                accepted_command: Mapping[str, object],
                catalog_basis: Mapping[str, object],
            ) -> tuple[object, Mapping[str, str]]:
                return context, {"definition_id": "activity.check.generic", "kind": "definition.activity"}

        with self.assertRaises(RecoveryFailure) as raised:
            recover_current_runtime(Repository(), "campaign-1")
        self.assertEqual(raised.exception.code, RecoveryFailureCode.CORRUPT)


class SourceNativeLiveRecoveryTests(unittest.TestCase):
    def test_selected_live_source_without_native_reader_is_typed_missing_not_campaign_fallback(self) -> None:
        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                return (CurrentNativeSource(pinned.campaign_id, "live", "scene-1/epoch-1", H, "LIVE/LIVE_STATE.yaml"),)

            def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
                self.reads.append((pinned.revision, path))
                return {"campaign_id": pinned.campaign_id}

        with self.assertRaises(RecoverySourceError) as raised:
            recover_current_runtime(Repository(), "campaign-1")
        self.assertEqual(raised.exception.code, RecoveryFailureCode.MISSING)


class CurrentSourceFailureTests(unittest.TestCase):
    def test_duplicate_current_source_owners_are_ambiguous(self) -> None:
        class Repository(FakeRepository):
            def select_current_native_sources(
                self, pinned: PinnedCampaign
            ) -> tuple[CurrentNativeSource, ...]:
                source = CurrentNativeSource(
                    pinned.campaign_id, "campaign", "campaign/current", pinned.revision, "MANIFEST.yaml"
                )
                return source, source

        with self.assertRaises(RecoverySourceError) as raised:
            select_current_native_sources(Repository(), "campaign-1")
        self.assertEqual(raised.exception.code, RecoveryFailureCode.AMBIGUOUS)

    def test_invalid_native_root_kind_is_typed_corrupt_recovery_failure(self) -> None:
        page = {
            "schema_version": 1,
            "campaign_id": "campaign-1",
            "complete": True,
            "roots": [
                {
                    "owner_kind": "runtime.unknown",
                    "owner_id": "unknown-000001",
                    "route": {
                        "family_key": "runtime.unknown",
                        "identity": ["unknown-000001"],
                        "relative_path": "STATE/RUNTIME/UNKNOWN/owner.yaml",
                    },
                }
            ],
        }

        with self.assertRaises(RecoveryFailure) as raised:
            hydrate_operational_roots(FakeRepository(), PinnedCampaign("campaign-1", H, TREE), page)
        self.assertEqual(raised.exception.code, RecoveryFailureCode.CORRUPT)


class SessionHotAuthorityTests(unittest.TestCase):
    def test_checkpoint_and_hot_are_diagnostics_not_current_authority(self) -> None:
        diagnostics = export_checkpoint_diagnostics(
            {"schema_version": 4, "id": "checkpoint-1", "campaign_id": "campaign-1"},
            campaign_id="campaign-1",
            observed_revision=H,
        )
        self.assertFalse(diagnostics["authoritative"])
        self.assertTrue(diagnostics["ephemeral"])


class StorageProjectionTests(unittest.TestCase):
    def test_empty_checkpoint_pointer_is_healthy_and_non_authoritative(self) -> None:
        diagnostics = export_checkpoint_diagnostics(None, campaign_id="campaign-1")
        self.assertEqual(diagnostics["status"], "NO_CHECKPOINT")
        self.assertFalse(diagnostics["authoritative"])

    def test_reset_only_clears_the_exact_selected_pointer(self) -> None:
        manifest = {"campaign_id": "campaign-1", "last_checkpoint_id": "checkpoint-1"}
        reset = reset_last_checkpoint_reference(manifest, selected_checkpoint_id="checkpoint-1")
        self.assertIsNone(reset["last_checkpoint_id"])
        self.assertEqual(manifest["last_checkpoint_id"], "checkpoint-1")

    def test_export_pins_manifest_and_reads_only_the_selected_descriptor(self) -> None:
        from GAME.TOOLS.native_storage import route_native_record

        checkpoint_path = route_native_record("runtime.checkpoint", ("checkpoint-1",)).relative_path

        class Repository(FakeRepository):
            def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
                if path == "MANIFEST.yaml":
                    return {"last_checkpoint_id": "checkpoint-1"}
                if path == checkpoint_path:
                    return {
                        "schema_version": 4,
                        "id": "checkpoint-1",
                        "campaign_id": pinned.campaign_id,
                    }
                raise KeyError(path)

        diagnostics = export_checkpoint_diagnostics(Repository(), campaign_id="campaign-1")
        self.assertEqual(diagnostics["checkpoint_id"], "checkpoint-1")
        self.assertEqual(diagnostics["observed_revision"], H)


class HistoricalMaintenanceTests(unittest.TestCase):
    def test_historical_candidate_is_maintenance_isolated(self) -> None:
        candidate = validate_repair_candidate(
            {
                "schema_version": 1,
                "campaign_id": "campaign-1",
                "operation_id": "repair-1",
                "historical_revision": H,
                "source_paths": ["STATE/CURRENT.yaml"],
                "evidence": {"checkpoint_id": "checkpoint-1"},
            },
            campaign_id="campaign-1",
            historical_revision=H,
        )
        self.assertIsInstance(candidate, HistoricalRepairCandidate)
        promotion = promote_historical_repair(candidate, current_revision=TREE, authorized=True)
        self.assertEqual(promotion["status"], "FORWARD_PUBLICATION_REQUIRED")
        self.assertFalse(promotion["ref_rewind"])
        self.assertFalse(promotion["current_authority"])

    def test_incomplete_historical_composition_is_typed(self) -> None:
        with self.assertRaises(RecoveryFailure) as raised:
            validate_repair_candidate(
                {
                    "schema_version": 1,
                    "campaign_id": "campaign-1",
                    "operation_id": "repair-1",
                    "historical_revision": H,
                    "source_paths": [],
                    "evidence": {"checkpoint_id": "checkpoint-1"},
                },
                campaign_id="campaign-1",
            )
        self.assertEqual(raised.exception.code, RecoveryFailureCode.INCOMPLETE)


class MaintenanceAuditMachineTests(unittest.TestCase):
    def test_audit_is_narrow_support_evidence_not_authority(self) -> None:
        audit = record_maintenance_audit(
            campaign_id="campaign-1",
            audit_id="audit-0001",
            operation="HDM_EXPORT_CHECKPOINT_LOG",
            scope="checkpoint-1",
            outcome="CONFIRMED",
            observed_basis={"revision": H},
        )
        self.assertIsInstance(audit, MaintenanceAudit)
        self.assertEqual(audit.to_dict()["authority"], "SUPPORT_AUDIT_ONLY")

    def test_audit_identity_must_use_the_native_campaign_policy(self) -> None:
        with self.assertRaises(RecoveryFailure) as raised:
            record_maintenance_audit(
                campaign_id="campaign-1",
                audit_id="maintenance-1",
                operation="HDM_EXPORT_CHECKPOINT_LOG",
                scope="checkpoint-1",
                outcome="CONFIRMED",
                observed_basis={"revision": H},
            )
        self.assertEqual(raised.exception.code, RecoveryFailureCode.CORRUPT)


if __name__ == "__main__":
    unittest.main()
