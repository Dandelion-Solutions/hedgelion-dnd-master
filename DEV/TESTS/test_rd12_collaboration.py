"""W04.T01A collaboration admission and native ordering evidence tests."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from GAME.TOOLS.access_control import (
    PlayerRecord,
    VerifiedPrincipal,
    build_principal_player_route,
)
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionError,
    ContributorRef,
    CoordinationFamily,
    DependencyClass,
    associate_input,
    classify_coordination_dependency,
    open_or_successor_obligation,
    reconcile_player_route_companions,
    required_route_holders,
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


def _bob_principal() -> VerifiedPrincipal:
    return VerifiedPrincipal(stable_account_id="43", login="bob")


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

    def test_optional_contributors_are_preserved_but_do_not_become_required(
        self,
    ) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [
                {"player_id": "player-alice", "pc_id": "pc-alice"}
            ]
        }

        admission = _classify(RepositoryFixture(clause))
        obligation = open_or_successor_obligation(
            admission, obligation_id="obligation-optional"
        )

        assert obligation is not None
        self.assertEqual(
            obligation.optional_contributors,
            (ContributorRef("player-alice", "pc-alice"),),
        )
        self.assertNotIn(
            ContributorRef("player-alice", "pc-alice"),
            obligation.required_contributors,
        )

    def test_optional_contributors_require_a_positive_dependency(self) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [{"player_id": "player-alice"}]
        }
        for field in (
            "collaboration_semantic_class",
            "dependency_kind",
            "purpose",
            "dependency_scope",
            "required_contributors",
            "native_basis_refs",
        ):
            clause.pop(field)

        with self.assertRaisesRegex(CollaborationAdmissionError, "dependency"):
            _classify(RepositoryFixture(clause))

    def test_one_player_cannot_be_both_required_and_optional(self) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [{"player_id": "player-bob"}]
        }

        with self.assertRaisesRegex(CollaborationAdmissionError, "both"):
            _classify(RepositoryFixture(clause))

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

    def test_association_uses_exact_interaction_clause_reference_without_copying_input_body(
        self,
    ) -> None:
        repository = RepositoryFixture()
        repository.put(
            "runtime.interaction",
            "interaction-2",
            {
                "kind": "runtime.interaction",
                "id": "interaction-2",
                "campaign_id": CAMPAIGN_ID,
                "session_id": "session-2",
                "player_id": "player-bob",
                "input_message_id": "message-2",
                "intent_plan_id": "plan-2",
            },
        )
        repository.put(
            "runtime.intent_plan",
            "plan-2",
            {
                "kind": "runtime.intent_plan",
                "id": "plan-2",
                "campaign_id": CAMPAIGN_ID,
                "interaction_id": "interaction-2",
                "clauses": [
                    {
                        "clause_id": "clause-2",
                        "order": 1,
                        "mapping_outcome": "exact",
                        "execution_state": "intent.pending",
                        "collaboration_semantic_class": "ACTIONABLE_INTENT",
                        "normalized_semantics": {
                            "action": "wait",
                            "private": "must-not-be-copied",
                        },
                    }
                ],
            },
        )
        admission = _classify(repository)
        obligation = open_or_successor_obligation(
            admission, obligation_id="obligation-input"
        )
        assert obligation is not None

        associated = associate_input(
            obligation,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )

        self.assertEqual(
            associated.accepted_input_uses,
            (
                ("interaction-1", "clause-1"),
                ("interaction-2", "clause-2"),
            ),
        )
        serialized = associated.to_mapping()
        self.assertNotIn("normalized_semantics", serialized)
        self.assertNotIn("private", serialized)

    def test_association_rejects_a_different_human_semantic_class(self) -> None:
        repository = RepositoryFixture()
        repository.put(
            "runtime.interaction",
            "interaction-2",
            {
                "kind": "runtime.interaction",
                "id": "interaction-2",
                "campaign_id": CAMPAIGN_ID,
                "session_id": "session-2",
                "player_id": "player-bob",
                "input_message_id": "message-2",
                "intent_plan_id": "plan-2",
            },
        )
        repository.put(
            "runtime.intent_plan",
            "plan-2",
            {
                "kind": "runtime.intent_plan",
                "id": "plan-2",
                "campaign_id": CAMPAIGN_ID,
                "interaction_id": "interaction-2",
                "clauses": [
                    {
                        "clause_id": "clause-2",
                        "order": 1,
                        "mapping_outcome": "exact",
                        "execution_state": "intent.pending",
                        "collaboration_semantic_class": "OOC_COORDINATION",
                        "normalized_semantics": {"note": "coordinate"},
                    }
                ],
            },
        )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-class"
        )
        assert obligation is not None

        with self.assertRaisesRegex(CollaborationAdmissionError, "semantic class"):
            associate_input(
                obligation,
                _host(repository),
                "interaction-2",
                "clause-2",
                principal=_bob_principal(),
                player_route=_route(),
            )

    def test_duplicate_input_association_is_idempotent(self) -> None:
        repository = RepositoryFixture()
        repository.put(
            "runtime.interaction",
            "interaction-2",
            {
                "kind": "runtime.interaction",
                "id": "interaction-2",
                "campaign_id": CAMPAIGN_ID,
                "session_id": "session-2",
                "player_id": "player-bob",
                "input_message_id": "message-2",
                "intent_plan_id": "plan-2",
            },
        )
        repository.put(
            "runtime.intent_plan",
            "plan-2",
            {
                "kind": "runtime.intent_plan",
                "id": "plan-2",
                "campaign_id": CAMPAIGN_ID,
                "interaction_id": "interaction-2",
                "clauses": [
                    {
                        "clause_id": "clause-2",
                        "order": 1,
                        "mapping_outcome": "exact",
                        "execution_state": "intent.pending",
                        "collaboration_semantic_class": "ACTIONABLE_INTENT",
                        "normalized_semantics": {"action": "enter"},
                    }
                ],
            },
        )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-idempotent"
        )
        assert obligation is not None
        first = associate_input(
            obligation,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )
        second = associate_input(
            first,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )

        self.assertIs(second, first)
        self.assertEqual(len(second.accepted_input_uses), 2)

    def test_old_generation_input_cannot_mutate_a_successor(self) -> None:
        repository = RepositoryFixture()
        admission = _classify(repository)
        predecessor = open_or_successor_obligation(
            admission, obligation_id="obligation-lineage"
        )
        assert predecessor is not None
        successor = open_or_successor_obligation(
            admission,
            obligation_id="obligation-lineage",
            generation=2,
            predecessor=predecessor,
        )
        assert successor is not None

        self.assertEqual(successor.predecessor_generation, 1)
        self.assertEqual(predecessor.generation, 1)

        with self.assertRaisesRegex(CollaborationAdmissionError, "stale"):
            associate_input(
                successor,
                _host(repository),
                "interaction-1",
                "clause-1",
                principal=_principal(),
                player_route=_route(),
                generation=1,
            )

    def test_generation_identity_is_not_rewritable_by_input_association(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-immutable"
        )
        assert obligation is not None

        with self.assertRaisesRegex(CollaborationAdmissionError, "stale"):
            associate_input(
                obligation,
                _host(repository),
                "interaction-1",
                "clause-1",
                principal=_principal(),
                player_route=_route(),
                generation=2,
            )

    def test_generation_above_one_requires_explicit_predecessor_lineage(self) -> None:
        with self.assertRaisesRegex(CollaborationAdmissionError, "predecessor"):
            open_or_successor_obligation(
                _classify(RepositoryFixture()),
                obligation_id="obligation-unanchored",
                generation=2,
            )

    def test_successor_cannot_repurpose_an_obligation_id_for_a_new_lineage(
        self,
    ) -> None:
        admission = _classify(RepositoryFixture())
        predecessor = open_or_successor_obligation(
            admission, obligation_id="obligation-stable"
        )
        assert predecessor is not None
        unrelated = replace(admission, interaction_id="interaction-new")

        with self.assertRaisesRegex(CollaborationAdmissionError, "lineage"):
            open_or_successor_obligation(
                unrelated,
                obligation_id="obligation-stable",
                generation=2,
                predecessor=predecessor,
            )

    def test_route_holders_include_required_and_input_players_but_not_optional_silence(
        self,
    ) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [{"player_id": "player-carol"}]
        }
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture(clause)), obligation_id="obligation-routes"
        )
        assert obligation is not None

        self.assertEqual(
            required_route_holders(obligation),
            ("player-alice", "player-bob"),
        )

    def test_player_route_companions_are_complete_references_and_terminal_removal_is_explicit(
        self,
    ) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-companion"
        )
        assert obligation is not None

        companions = reconcile_player_route_companions(obligation)
        self.assertEqual(
            tuple(companion.player_id for companion in companions),
            ("player-alice", "player-bob"),
        )
        self.assertTrue(all(companion.complete for companion in companions))
        self.assertEqual(
            companions[0].to_mapping()["collaboration_route_refs"],
            [{"obligation_id": "obligation-companion", "generation": 1}],
        )
        self.assertNotIn("authorized", companions[0].to_mapping())

        terminal = replace(obligation, lifecycle="RESOLVED")
        terminal_companions = reconcile_player_route_companions(terminal)
        self.assertEqual(
            [
                companion.to_mapping()["collaboration_route_refs"]
                for companion in terminal_companions
            ],
            [[], []],
        )

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

    def test_resolution_malformed_owner_schema_constraint_fails_closed(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        resolution = _ordered_resolution()
        resolution["ruleset_set_sha256"] = "not-a-sha256"
        repository.put("runtime.resolution", "resolution-1", resolution)
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_resolution_failure_code_must_match_owner_status_conditional(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        resolution = _ordered_resolution() | {
            "failure_code": "failure.order_adjudication_required"
        }
        repository.put("runtime.resolution", "resolution-1", resolution)
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_resolution_rejects_non_schema_resolution_id_alias(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        resolution = _ordered_resolution() | {"resolution_id": "resolution-1"}
        repository.put("runtime.resolution", "resolution-1", resolution)
        repository.put(
            "runtime.continuation",
            "continuation-1",
            _ordered_continuation(pending_response=_choice()),
        )

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_continuation_rejects_non_schema_continuation_id_alias(self) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        continuation = _ordered_continuation(pending_response=_choice()) | {
            "continuation_id": "continuation-1"
        }
        repository.put("runtime.continuation", "continuation-1", continuation)

        with self.assertRaises(CollaborationAdmissionError):
            _classify(repository)

    def test_continuation_malformed_owner_schema_constraint_fails_closed(
        self,
    ) -> None:
        clause = _collective_clause() | {"ordering_resolution_id": "resolution-1"}
        repository = RepositoryFixture(clause)
        repository.put("runtime.resolution", "resolution-1", _ordered_resolution())
        continuation = _ordered_continuation(pending_response=_choice())
        continuation["ruleset_set_sha256"] = "not-a-sha256"
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
    def test_intent_clause_schema_accepts_optional_contributors(self) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [{"player_id": "player-alice"}]
        }
        schema = json.loads(
            (SCHEMAS / "intent-clause.schema.json").read_text(encoding="utf-8")
        )

        Draft202012Validator(schema).validate(clause)

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
