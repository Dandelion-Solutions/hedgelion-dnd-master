"""W04.T01A collaboration admission and native ordering evidence tests."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from GAME.TOOLS.access_control import (
    PlayerRecord,
    VerifiedPrincipal,
    build_principal_player_route,
)
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionError,
    CoordinationFamily,
    DependencyClass,
    classify_coordination_dependency,
    open_or_successor_obligation,
)
from GAME.TOOLS.live_state import LiveRouting
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.runtime_execution import NativeOrderingEvidence
from GAME.TOOLS.runtime_host import compose_runtime_host

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


CAMPAIGN_ID = "campaign-frostfall"
CAMPAIGN_REVISION = "a" * 40
TREE_SHA = "b" * 40
CHANGED_CAMPAIGN_REVISION = "c" * 40


class RepositoryFixture:
    """Trusted host fixture exposing only exact pinned repository reads."""

    def __init__(self, clause: dict[str, object] | None = None) -> None:
        self.records: dict[str, object] = {}
        self.reads: list[str] = []
        self._install_records(clause or _collective_clause())

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        return PinnedCampaign(CAMPAIGN_ID, CAMPAIGN_REVISION, TREE_SHA)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if pinned.campaign_id != CAMPAIGN_ID or pinned.revision != CAMPAIGN_REVISION:
            raise KeyError("stale campaign pin")
        self.reads.append(path)
        return deepcopy(self.records[path])

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        return {"campaign_id": campaign_id}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        return {"ref": campaign_ref, "revision": revision}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        return {"ref": campaign_ref, "revision": revision}

    def put(self, family: str, record_id: str, value: dict[str, object]) -> None:
        self.records[route_native_record(family, (record_id,)).relative_path] = value

    def _install_records(self, clause: dict[str, object]) -> None:
        self.put(
            "runtime.interaction",
            "interaction-1",
            {
                "kind": "runtime.interaction",
                "id": "interaction-1",
                "campaign_id": CAMPAIGN_ID,
                "session_id": "session-1",
                "player_id": "player-alice",
                "input_message_id": "message-1",
                "intent_plan_id": "plan-1",
            },
        )
        self.put(
            "runtime.intent_plan",
            "plan-1",
            {
                "kind": "runtime.intent_plan",
                "id": "plan-1",
                "campaign_id": CAMPAIGN_ID,
                "interaction_id": "interaction-1",
                "clauses": [clause],
            },
        )
        self.put(
            "world.player",
            "player-alice",
            _player_record("player-alice", "42", "alice", "pc-alice"),
        )
        self.put(
            "world.player",
            "player-bob",
            _player_record("player-bob", "43", "bob", "pc-bob"),
        )
        self.put(
            "world.scene",
            "scene-market",
            {
                "kind": "world.scene",
                "id": "scene-market",
                "campaign_id": CAMPAIGN_ID,
                "revision": CAMPAIGN_REVISION,
                "state": {"name": "Market morning"},
            },
        )


class ChangingPinRepositoryFixture(RepositoryFixture):
    """Fixture that changes the campaign pin before the ordering read."""

    def __init__(self, clause: dict[str, object] | None = None) -> None:
        self.pin_calls = 0
        super().__init__(clause)

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        self.pin_calls += 1
        revision = (
            CAMPAIGN_REVISION if self.pin_calls == 1 else CHANGED_CAMPAIGN_REVISION
        )
        return PinnedCampaign(CAMPAIGN_ID, revision, TREE_SHA)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if pinned.campaign_id != CAMPAIGN_ID:
            raise KeyError("wrong campaign pin")
        self.reads.append(path)
        return deepcopy(self.records[path])


class LiveFixture:
    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        return LiveRouting(campaign_id=campaign_id, entries=())


def _player_record(
    player_id: str, account_id: str, login: str, pc_id: str
) -> dict[str, object]:
    return {
        "kind": "world.player",
        "id": player_id,
        "player_id": player_id,
        "campaign_id": CAMPAIGN_ID,
        "state": {},
        "github_binding": {"user_id": account_id, "login": login},
        "status": "active",
        "deactivated_by": None,
        "controlled_pc_ids": [pc_id],
    }


def _collective_clause() -> dict[str, object]:
    return {
        "clause_id": "clause-1",
        "order": 1,
        "mapping_outcome": "exact",
        "execution_state": "intent.pending",
        "collaboration_semantic_class": "ACTIONABLE_INTENT",
        "normalized_semantics": {"action": "enter", "target": "market"},
        "dependency_kind": DependencyClass.JOINT_VOLUNTARY_ACTION.value,
        "purpose": "joint-entry",
        "dependency_scope": {"scene_id": "scene-market"},
        "required_contributors": [{"player_id": "player-bob", "pc_id": "pc-bob"}],
        "native_basis_refs": [
            {
                "family": "world.scene",
                "id": "scene-market",
                "revision": CAMPAIGN_REVISION,
            }
        ],
    }


def _route() -> object:
    return build_principal_player_route(
        CAMPAIGN_ID,
        (
            PlayerRecord(
                "player-alice",
                "42",
                "alice",
                "active",
                None,
                controlled_pc_ids=("pc-alice",),
            ),
            PlayerRecord(
                "player-bob", "43", "bob", "active", None, controlled_pc_ids=("pc-bob",)
            ),
        ),
    )


def _principal() -> VerifiedPrincipal:
    return VerifiedPrincipal(stable_account_id="42", login="alice")


def _host(repository: RepositoryFixture) -> object:
    return compose_runtime_host(CAMPAIGN_ID, repository, LiveFixture())


def _classify(repository: RepositoryFixture):
    host = _host(repository)
    return classify_coordination_dependency(
        host,
        "interaction-1",
        "clause-1",
        principal=_principal(),
        player_route=_route(),
    )


def _ordered_resolution(
    *, status: str = "AWAITING_CHOICE", procedure_id: str | None = None
) -> dict[str, object]:
    resolution: dict[str, object] = {
        "kind": "runtime.resolution",
        "id": "resolution-1",
        "campaign_id": CAMPAIGN_ID,
        "root_command_id": "command-1",
        "initiating_command_id": "command-1",
        "activity_id": "activity.test",
        "actor_id": "actor-bob",
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": "d" * 64,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": "catalog-context-1",
        "status": status,
        "continuation_id": "continuation-1",
        "next_segment_sequence": 1,
        "invocation_facts": [],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "child_resolution_ids": [],
        "segments": [],
    }
    if procedure_id is not None:
        resolution["procedure_id"] = procedure_id
    return resolution


def _ordered_continuation(
    *,
    pending_response: dict[str, object] | None = None,
    procedure_id: str | None = None,
) -> dict[str, object]:
    continuation: dict[str, object] = {
        "kind": "runtime.continuation",
        "id": "continuation-1",
        "campaign_id": CAMPAIGN_ID,
        "generation": 3,
        "resolution_id": "resolution-1",
        "root_command_id": "command-1",
        "activity_id": "activity.test",
        "actor_id": "actor-bob",
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": "d" * 64,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": "catalog-context-1",
        "execution_cursor": "step.test",
        "safe_recompute_phase": "determine",
        "invocation_facts": [],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "committed_segment_refs": [],
        "dependency_frontier_refs": [],
        "expected_child_resolution_ids": [],
        "future_rng_frontier": "rng:test",
    }
    if pending_response is not None:
        continuation["pending_response"] = pending_response
    if procedure_id is not None:
        continuation["procedure_id"] = procedure_id
    return continuation


def _choice() -> dict[str, object]:
    return {
        "kind": "choice",
        "offer_id": "choice-1",
        "parent_resolution_id": "resolution-1",
        "continuation_generation": 3,
        "responder_id": "actor-bob",
        "option_ids": ["option.left", "option.right"],
    }


class CollaborationAdmissionTests(unittest.TestCase):
    def test_finite_collective_dependency_is_derived_from_current_native_records(
        self,
    ) -> None:
        admission = _classify(RepositoryFixture())

        self.assertEqual(
            admission.family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
        )
        self.assertEqual(admission.opportunity_identity, ("interaction-1", "clause-1"))
        self.assertEqual(admission.required_contributors[0].player_id, "player-bob")
        obligation = open_or_successor_obligation(
            admission, obligation_id="obligation-1"
        )
        self.assertIsNotNone(obligation)

    def test_ordered_evidence_is_produced_by_step3_through_bound_host(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)
        self.assertIsNone(open_or_successor_obligation(admission))

    def test_reaction_offer_is_also_a_positive_ordered_owner(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(status="AWAITING_REACTION"),
        )
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(
                pending_response={
                    "kind": "reaction",
                    "offer_id": "reaction-1",
                    "parent_resolution_id": "resolution-1",
                    "continuation_generation": 3,
                    "responder_id": "actor-bob",
                    "candidate_activity_ids": ["activity.shield"],
                }
            ),
        )

        self.assertEqual(
            _classify(repository).family, CoordinationFamily.RULE_OWNED_ORDERED
        )

    def test_ordering_ref_without_exact_current_pending_offer_fails_closed(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        repository.put(
            "runtime.continuation", "continuation-1", _ordered_continuation()
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_resolution_missing_required_owner_schema_field_fails_closed(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        resolution = _ordered_resolution()
        del resolution["fixed_rng_results"]
        repository.put("runtime.resolution", "resolution-1", resolution)
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_continuation_missing_required_owner_schema_field_fails_closed(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        continuation = _ordered_continuation(pending_response=_choice())
        del continuation["future_rng_frontier"]
        repository.put("runtime.continuation", "continuation-1", continuation)

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_changing_campaign_pin_fails_closed_before_ordered_evidence(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = ChangingPinRepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_active_procedure_alone_never_proves_order(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(procedure_id="procedure-1"),
        )
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(
                procedure_id="procedure-1", pending_response=_choice()
            ),
        )
        repository.put(
            "runtime.procedure",
            "procedure-1",
            {
                "kind": "runtime.procedure",
                "id": "procedure-1",
                "campaign_id": CAMPAIGN_ID,
                "schema_version": 2,
                "lifecycle": "ACTIVE",
                "participant_resources": {},
            },
        )

        self.assertEqual(
            _classify(repository).family, CoordinationFamily.RULE_OWNED_ORDERED
        )

    def test_procedure_reference_without_ordering_resolution_does_not_infer_order(
        self,
    ) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {
                "family": "runtime.procedure",
                "id": "procedure-1",
                "revision": CAMPAIGN_REVISION,
            }
        ]

        with self.assertRaises(CollaborationAdmissionError):
            _classify(RepositoryFixture(clause))

    def test_non_awaiting_resolution_cannot_be_reclassified_as_collective_or_independent(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(status="RUNNING"),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_resolution_status_must_match_pending_offer_kind_and_generation(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(status="AWAITING_REACTION"),
        )
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_caller_cannot_supply_ordering_owner_body_or_family(self) -> None:
        clause = _collective_clause() | {
            "coordination_family": "RULE_OWNED_ORDERED",
            "continuation": _ordered_continuation(pending_response=_choice()),
            "status": "AWAITING_CHOICE",
        }
        with self.assertRaises(CollaborationAdmissionError):
            _classify(RepositoryFixture(clause))

    def test_collaboration_semantics_must_be_nonempty_when_declared(self) -> None:
        clause = _collective_clause() | {"normalized_semantics": {}}

        with self.assertRaises(CollaborationAdmissionError):
            _classify(RepositoryFixture(clause))

    def test_inactive_or_mismatched_linked_procedure_fails_closed(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(procedure_id="procedure-1"),
        )
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(
                procedure_id="procedure-1", pending_response=_choice()
            ),
        )
        repository.put(
            "runtime.procedure",
            "procedure-1",
            {
                "kind": "runtime.procedure",
                "id": "procedure-1",
                "campaign_id": CAMPAIGN_ID,
                "schema_version": 2,
                "lifecycle": "TERMINAL",
                "participant_resources": {},
            },
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_linked_procedure_identity_cannot_disagree_with_its_native_route(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put(
            "runtime.resolution",
            "resolution-1",
            _ordered_resolution(procedure_id="procedure-1"),
        )
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(
                procedure_id="procedure-1", pending_response=_choice()
            ),
        )
        repository.put(
            "runtime.procedure",
            "procedure-1",
            {
                "kind": "runtime.procedure",
                "id": "procedure-1",
                "procedure_id": "procedure-other",
                "campaign_id": CAMPAIGN_ID,
                "schema_version": 2,
                "lifecycle": "ACTIVE",
                "participant_resources": {},
            },
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_ordered_result_contains_only_ephemeral_owner_evidence(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        admission = _classify(repository)

        self.assertIsInstance(admission.ordered_evidence, NativeOrderingEvidence)
        assert admission.ordered_evidence is not None
        self.assertEqual(admission.ordered_evidence.resolution_id, "resolution-1")
        self.assertEqual(admission.ordered_evidence.continuation_generation, 3)
        self.assertEqual(admission.ordered_evidence.offer_kind, "choice")
        self.assertNotIn("status", admission.normalized_semantics)

    def test_former_mechanics_ordering_helper_is_not_an_authority_surface(self) -> None:
        from GAME.TOOLS import mechanics

        self.assertFalse(hasattr(mechanics, "validate_native_ordering_owner"))


class CollaborationSchemaTests(unittest.TestCase):
    def test_intent_clause_schema_accepts_finite_dependency_and_ordering_reference(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        schema = json.loads(
            (SCHEMAS / "intent-clause.schema.json").read_text(encoding="utf-8")
        )

        Draft202012Validator(schema).validate(clause)

    def test_intent_clause_schema_rejects_caller_selected_family_or_owner_body(
        self,
    ) -> None:
        clause = _collective_clause() | {
            "coordination_family": "RULE_OWNED_ORDERED",
            "continuation": _ordered_continuation(pending_response=_choice()),
        }
        schema = json.loads(
            (SCHEMAS / "intent-clause.schema.json").read_text(encoding="utf-8")
        )

        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(clause)

    def test_obligation_schema_preserves_exact_input_identity(self) -> None:
        admission = _classify(RepositoryFixture())
        obligation = open_or_successor_obligation(
            admission, obligation_id="obligation-1"
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )

        value = obligation.to_mapping()
        Draft202012Validator(schema).validate(value)
        self.assertEqual(
            value["accepted_input_uses"],
            [{"interaction_id": "interaction-1", "clause_id": "clause-1"}],
        )


if __name__ == "__main__":
    unittest.main()
