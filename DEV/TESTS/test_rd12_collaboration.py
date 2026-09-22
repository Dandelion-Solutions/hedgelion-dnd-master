"""W04.T01A/T01C/T02A collaboration owner contract tests."""

from __future__ import annotations

import json
import unittest
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS import collaboration as collaboration_module
from GAME.TOOLS.access_control import (
    PlayerRecord,
    VerifiedPrincipal,
    build_principal_player_route,
)
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionError,
    CollaborationClosedBasis,
    CollaborationFrontier,
    CollaborationHandoff,
    CollaborationObligation,
    ContributorRef,
    CoordinationFamily,
    DependencyClass,
    HandoffDisposition,
    NativeBasisRef,
    apply_handoff,
    associate_input,
    build_handoff,
    build_join_frontier,
    classify_coordination_dependency,
    close_obligation,
    compute_maximal_safe_frontier,
    open_or_successor_obligation,
    reconcile_player_route_companions,
    required_route_holders,
    validate_visible_consequence,
)
from GAME.TOOLS.live_state import LiveRouting
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign
from GAME.TOOLS.runtime_execution import NativeOrderingEvidence
from GAME.TOOLS.runtime_host import compose_runtime_host

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


CAMPAIGN_ID = "campaign-frostfall"
CAMPAIGN_REVISION = "a" * 40
TREE_SHA = "b" * 40
CHANGED_CAMPAIGN_REVISION = "c" * 40


def _thaw_for_test(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_for_test(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_thaw_for_test(item) for item in value]
    return value


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


class CampaignPublicationRepositoryFixture(RepositoryFixture):
    """Exact-read fixture whose writes are applied only by the host transport."""

    def __init__(self, clause: dict[str, object] | None = None) -> None:
        self.current_revision = CAMPAIGN_REVISION
        self.current_tree = TREE_SHA
        super().__init__(clause)
        self.records["MANIFEST.yaml"] = {
            "campaign_id": CAMPAIGN_ID,
            "campaign_name": "The Frostfall",
            "branch": "campaign/frostfall",
            "created_at": "2026-09-22T00:00:00Z",
        }
        self.records["CAMPAIGN_CARD.yaml"] = {
            "campaign_id": CAMPAIGN_ID,
            "campaign_name": "The Frostfall",
        }

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        return PinnedCampaign(CAMPAIGN_ID, self.current_revision, self.current_tree)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if path in {"MANIFEST.yaml", "CAMPAIGN_CARD.yaml"}:
            return deepcopy(self.records[path])
        if (
            pinned.campaign_id != CAMPAIGN_ID
            or pinned.revision != self.current_revision
        ):
            raise KeyError("stale campaign pin")
        self.reads.append(path)
        return deepcopy(self.records[path])

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        return {
            "ref": campaign_ref,
            "revision": revision,
            "tree_sha": self.current_tree,
        }


class CampaignPublicationTransport:
    """Host-bound W02 publication transport with controllable outcomes."""

    def __init__(self, repository: CampaignPublicationRepositoryFixture) -> None:
        self.repository = repository
        self.calls: list[tuple[str, object]] = []
        self.response_status = "accepted"
        self.next_head = "d" * 40
        self.ref_revision_override: str | None = None
        self._pending_operations: dict[str, object | None] = {}

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def resolve_authenticated_acting_principal(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> AuthenticatedPrincipalEvidence:
        return AuthenticatedPrincipalEvidence("principal-1")

    def read_ref(self, target_ref: str) -> object:
        self.calls.append(("read_ref", target_ref))
        return {
            "head_sha": self.ref_revision_override or self.repository.current_revision
        }

    def create_tree(self, base_tree_sha: str, path_operations: object) -> object:
        self.calls.append(("create_tree", path_operations))
        if not isinstance(path_operations, Mapping):
            raise TypeError("path operations must be a mapping")
        self._pending_operations = dict(path_operations)
        return "e" * 40

    def create_commit(self, parent_sha: str, tree_sha: str, target_ref: str) -> object:
        self.calls.append(("create_commit", (parent_sha, tree_sha, target_ref)))
        return self.next_head

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        self.calls.append(("update_ref", (target_ref, new_commit_sha, force)))
        if self.response_status in {"accepted", "indeterminate"}:
            self.repository.current_revision = new_commit_sha
            self.repository.current_tree = "e" * 40
            for path, payload in self._pending_operations.items():
                if payload is None:
                    self.repository.records.pop(path, None)
                else:
                    self.repository.records[path] = _thaw_for_test(payload)
        return {
            "status": self.response_status,
            "head_sha": (
                new_commit_sha if self.response_status != "rejected" else None
            ),
            "dispatched": True,
            "reason": "non_fast_forward"
            if self.response_status == "rejected"
            else None,
        }


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


def _host(
    repository: RepositoryFixture,
    publication: CampaignPublicationTransport | None = None,
) -> object:
    return compose_runtime_host(CAMPAIGN_ID, repository, LiveFixture(), publication)


def _classify(repository: RepositoryFixture):
    host = _host(repository)
    return classify_coordination_dependency(
        host,
        "interaction-1",
        "clause-1",
        principal=_principal(),
        player_route=_route(),
    )


def _add_persisted_input(
    repository: RepositoryFixture,
    *,
    interaction_id: str,
    clause_id: str,
    player_id: str,
    pc_id: str | None = None,
) -> None:
    plan_id = f"plan-{interaction_id.removeprefix('interaction-')}"
    repository.put(
        "runtime.interaction",
        interaction_id,
        {
            "kind": "runtime.interaction",
            "id": interaction_id,
            "campaign_id": CAMPAIGN_ID,
            "session_id": "session-secondary",
            "player_id": player_id,
            "input_message_id": f"message-{interaction_id}",
            "intent_plan_id": plan_id,
        },
    )
    repository.put(
        "runtime.intent_plan",
        plan_id,
        {
            "kind": "runtime.intent_plan",
            "id": plan_id,
            "campaign_id": CAMPAIGN_ID,
            "interaction_id": interaction_id,
            "clauses": [
                {
                    "clause_id": clause_id,
                    "order": 1,
                    "mapping_outcome": "exact",
                    "execution_state": "intent.pending",
                    "collaboration_semantic_class": "ACTIONABLE_INTENT",
                    "normalized_semantics": {"action": "wait"},
                }
            ],
        },
    )


def _persist_obligation(
    repository: RepositoryFixture, obligation: CollaborationObligation
) -> None:
    repository.put(
        "runtime.collaboration_obligation",
        obligation.obligation_id,
        obligation.to_mapping(),
    )


def _append_persisted_input(
    value: dict[str, object],
    *,
    interaction_id: str,
    clause_id: str,
    player_id: str,
    pc_id: str | None = None,
) -> None:
    value["accepted_input_uses"].append(  # type: ignore[union-attr]
        {"interaction_id": interaction_id, "clause_id": clause_id}
    )
    contributor: dict[str, str] = {
        "interaction_id": interaction_id,
        "clause_id": clause_id,
        "player_id": player_id,
    }
    if pc_id is not None:
        contributor["pc_id"] = pc_id
    value["accepted_input_contributors"].append(  # type: ignore[union-attr]
        contributor
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

        terminal = replace(
            obligation,
            lifecycle="RESOLVED",
            closed_input_set_fingerprint="a" * 64,
        )
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
    def _load_obligation(self, value: object, repository: RepositoryFixture):
        parser = getattr(CollaborationObligation, "from_mapping", None)
        self.assertTrue(callable(parser), "serialized obligation parser is required")
        assert callable(parser)
        return parser(value, host=_host(repository))

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

    def test_obligation_schema_requires_new_lineage_and_input_fields(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-required"
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)

        for field in (
            "predecessor_generation",
            "collaboration_semantic_class",
            "accepted_input_contributors",
        ):
            value = obligation.to_mapping()
            del value[field]
            with self.subTest(field=field), self.assertRaises(ValidationError):
                validator.validate(value)

    def test_obligation_schema_uses_v3_and_rejects_legacy_schema(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-version"
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        game_schema = yaml.safe_load(
            (
                ROOT / "GAME" / "SCHEMA" / "collaboration_obligation.schema.yaml"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(schema["properties"]["schema_version"]["const"], 3)
        self.assertEqual(game_schema["schema_version"], 3)

        legacy = obligation.to_mapping()
        legacy["schema_version"] = 1
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(legacy)

    def test_obligation_schema_enforces_v3_fingerprint_lifecycle_matrix(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()),
            obligation_id="obligation-fingerprint-matrix",
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)
        open_value = obligation.to_mapping()
        open_value["closed_input_set_fingerprint"] = None
        self.assertIsNone(open_value["closed_input_set_fingerprint"])
        self.assertTrue(validator.is_valid(open_value))

        closed_value = open_value | {
            "lifecycle": "CLOSED",
            "closed_input_set_fingerprint": "a" * 64,
        }
        self.assertTrue(validator.is_valid(closed_value))
        resolved_value = closed_value | {"lifecycle": "RESOLVED"}
        self.assertTrue(validator.is_valid(resolved_value))
        obsolete_open_value = open_value | {"lifecycle": "OBSOLETE"}
        self.assertTrue(validator.is_valid(obsolete_open_value))
        obsolete_closed_value = closed_value | {"lifecycle": "OBSOLETE"}
        self.assertTrue(validator.is_valid(obsolete_closed_value))

        for lifecycle in ("OPEN", "CLOSED", "RESOLVED"):
            invalid = open_value | {
                "lifecycle": lifecycle,
                "closed_input_set_fingerprint": (
                    None if lifecycle != "OPEN" else "b" * 64
                ),
            }
            with self.subTest(lifecycle=lifecycle), self.assertRaises(ValidationError):
                validator.validate(invalid)

    def test_runtime_state_rejects_v2_after_v3_cutover_and_preserves_fingerprint_rules(
        self,
    ) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-v3-cutover"
        )
        assert obligation is not None
        with self.assertRaisesRegex(CollaborationAdmissionError, "unsupported"):
            CollaborationObligation.from_mapping(
                obligation.to_mapping() | {"schema_version": 2},
                host=_host(RepositoryFixture()),
            )

        with self.assertRaisesRegex(CollaborationAdmissionError, "fingerprint"):
            replace(
                obligation,
                lifecycle="OPEN",
                closed_input_set_fingerprint="a" * 64,
            )
        with self.assertRaisesRegex(CollaborationAdmissionError, "fingerprint"):
            replace(obligation, lifecycle="CLOSED")

    def test_obligation_schema_rejects_duplicate_serialized_identities(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-unique"
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)

        duplicate_use = obligation.to_mapping()
        duplicate_use["accepted_input_uses"].append(
            duplicate_use["accepted_input_uses"][0]
        )
        with self.assertRaises(ValidationError):
            validator.validate(duplicate_use)

        duplicate_contributor = obligation.to_mapping()
        duplicate_contributor["accepted_input_contributors"].append(
            duplicate_contributor["accepted_input_contributors"][0]
        )
        with self.assertRaises(ValidationError):
            validator.validate(duplicate_contributor)

    def test_obligation_schema_correlates_generation_and_predecessor_shape(
        self,
    ) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-generation-shape"
        )
        assert obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)

        initial_with_predecessor = obligation.to_mapping()
        initial_with_predecessor["predecessor_generation"] = 1
        with self.assertRaises(ValidationError):
            validator.validate(initial_with_predecessor)

        successor_without_predecessor = obligation.to_mapping()
        successor_without_predecessor["generation"] = 2
        successor_without_predecessor["predecessor_generation"] = None
        with self.assertRaises(ValidationError):
            validator.validate(successor_without_predecessor)

    def test_runtime_state_rejects_unanchored_successor_lineage(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-lineage-state"
        )
        assert obligation is not None

        with self.assertRaisesRegex(CollaborationAdmissionError, "predecessor"):
            replace(obligation, generation=2, predecessor_generation=None)

    def test_runtime_state_rejects_mismatched_input_identity_correlation(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-correlation"
        )
        assert obligation is not None

        with self.assertRaisesRegex(CollaborationAdmissionError, "input"):
            replace(
                obligation,
                accepted_input_uses=(
                    ("interaction-1", "clause-1"),
                    ("interaction-2", "clause-2"),
                ),
            )

    def test_runtime_state_rejects_duplicate_input_identity(self) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-duplicate"
        )
        assert obligation is not None
        identity = ("interaction-1", "clause-1")

        with self.assertRaisesRegex(CollaborationAdmissionError, "duplicate"):
            replace(
                obligation,
                accepted_input_uses=(identity, identity),
                accepted_input_contributors=(
                    (identity, ContributorRef("player-alice")),
                    (identity, ContributorRef("player-alice")),
                ),
            )

    def test_duplicate_input_revalidates_native_owner_before_idempotent_ack(
        self,
    ) -> None:
        obligation = open_or_successor_obligation(
            _classify(RepositoryFixture()), obligation_id="obligation-forged-input"
        )

        assert obligation is not None
        with self.assertRaisesRegex(CollaborationAdmissionError, "PLAYER"):
            associate_input(
                obligation,
                _host(RepositoryFixture()),
                "interaction-1",
                "clause-1",
                principal=_bob_principal(),
                player_route=_route(),
            )

    def test_runtime_state_round_trip_validates_new_schema_and_native_input_owner(
        self,
    ) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-round-trip"
        )
        assert obligation is not None

        restored = self._load_obligation(obligation.to_mapping(), repository)

        self.assertEqual(restored, obligation)

    def test_runtime_state_rejects_restore_from_inactive_origin_player(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-inactive-origin"
        )
        assert obligation is not None
        inactive_alice = _player_record("player-alice", "42", "alice", "pc-alice")
        inactive_alice["status"] = "inactive"
        inactive_alice["deactivated_by"] = "self"
        repository.put("world.player", "player-alice", inactive_alice)

        with self.assertRaisesRegex(CollaborationAdmissionError, "active"):
            self._load_obligation(obligation.to_mapping(), repository)

    def test_runtime_state_rejects_legacy_schema_mapping(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-legacy"
        )
        assert obligation is not None
        value = obligation.to_mapping()
        value["schema_version"] = 1

        with self.assertRaisesRegex(CollaborationAdmissionError, "schema"):
            self._load_obligation(value, repository)

    def test_runtime_state_rejects_input_contributor_not_owned_by_input(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-forged-owner"
        )
        assert obligation is not None
        value = obligation.to_mapping()
        value["accepted_input_contributors"][0]["player_id"] = "player-bob"

        with self.assertRaisesRegex(CollaborationAdmissionError, "contributor"):
            self._load_obligation(value, repository)

    def test_runtime_state_rejects_valid_non_holder_input_contributor(self) -> None:
        repository = RepositoryFixture()
        repository.put(
            "world.player",
            "player-carol",
            _player_record("player-carol", "44", "carol", "pc-carol"),
        )
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-carol",
            pc_id="pc-carol",
        )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-non-holder"
        )
        assert obligation is not None
        value = obligation.to_mapping()
        _append_persisted_input(
            value,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-carol",
            pc_id="pc-carol",
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "contributor"):
            self._load_obligation(value, repository)

    def test_runtime_state_rejects_input_from_inactive_player(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-inactive-input"
        )
        assert obligation is not None
        inactive_bob = _player_record("player-bob", "43", "bob", "pc-bob")
        inactive_bob["status"] = "inactive"
        inactive_bob["deactivated_by"] = "self"
        repository.put("world.player", "player-bob", inactive_bob)
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        value = obligation.to_mapping()
        _append_persisted_input(
            value,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "active"):
            self._load_obligation(value, repository)

    def test_runtime_state_rejects_input_with_invalid_controlled_pc(self) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-not-controlled",
        )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-invalid-input-pc"
        )
        assert obligation is not None
        value = obligation.to_mapping()
        _append_persisted_input(
            value,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-not-controlled",
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "PC"):
            self._load_obligation(value, repository)

    def test_runtime_state_rejects_duplicate_input_contributor_identity(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-forged-duplicate"
        )
        assert obligation is not None
        value = obligation.to_mapping()
        value["accepted_input_contributors"].append(
            {
                "interaction_id": "interaction-1",
                "clause_id": "clause-1",
                "player_id": "player-bob",
            }
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "duplicate"):
            self._load_obligation(value, repository)


class CollaborationFrontierTests(unittest.TestCase):
    def test_caller_empty_pending_cannot_erase_missing_required_holder(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository),
            obligation_id="obligation-frontier-pending-override",
        )
        assert obligation is not None

        frontier = compute_maximal_safe_frontier(
            obligation,
            host=_host(repository),
            pending_required_contributors=(),
        )

        self.assertEqual(
            frontier.pending_required_contributors,
            (ContributorRef("player-bob", "pc-bob"),),
        )

    def test_post_admission_native_basis_drift_is_rejected(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository),
            obligation_id="obligation-frontier-drift",
        )
        assert obligation is not None
        scene_path = route_native_record("world.scene", ("scene-market",)).relative_path
        repository.records[scene_path]["revision"] = CHANGED_CAMPAIGN_REVISION  # type: ignore[index]

        with self.assertRaisesRegex(CollaborationAdmissionError, "current"):
            compute_maximal_safe_frontier(
                obligation,
                host=_host(repository),
                current_basis_refs=obligation.native_basis_refs,
            )

    def test_forged_foreign_frontier_cannot_authorize_visible_consequence(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository),
            obligation_id="obligation-frontier-foreign",
        )
        assert obligation is not None
        host = _host(repository)
        frontier = compute_maximal_safe_frontier(obligation, host=host)
        forged = replace(frontier, campaign_id="campaign-foreign")

        with self.assertRaisesRegex(CollaborationAdmissionError, "authoritative"):
            validate_visible_consequence(
                forged,
                obligation=obligation,
                host=host,
                evidence_refs=forged.safe_prefix_refs,
            )

    def test_frontier_stops_at_missing_required_input_and_keeps_scope_local(
        self,
    ) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-frontier"
        )
        assert obligation is not None

        frontier = compute_maximal_safe_frontier(obligation, host=_host(repository))

        self.assertEqual(frontier.obligation_id, obligation.obligation_id)
        self.assertEqual(frontier.generation, obligation.generation)
        self.assertEqual(frontier.campaign_id, obligation.campaign_id)
        self.assertEqual(frontier.dependency_scope, obligation.dependency_scope)
        self.assertEqual(frontier.safe_prefix_refs, obligation.native_basis_refs)
        self.assertEqual(
            frontier.pending_required_contributors,
            (ContributorRef("player-bob", "pc-bob"),),
        )
        self.assertEqual(obligation.lifecycle, "OPEN")

    def test_optional_silence_is_not_a_pending_frontier_requirement(self) -> None:
        clause = _collective_clause() | {
            "optional_contributors": [{"player_id": "player-carol"}]
        }
        repository = RepositoryFixture(clause)
        obligation = open_or_successor_obligation(
            _classify(repository),
            obligation_id="obligation-optional-frontier",
        )
        assert obligation is not None

        frontier = build_join_frontier(obligation, host=_host(repository))

        self.assertEqual(
            frontier.pending_required_contributors,
            (ContributorRef("player-bob", "pc-bob"),),
        )
        self.assertNotIn(
            ContributorRef("player-carol"), frontier.pending_required_contributors
        )
        self.assertEqual(obligation.lifecycle, "OPEN")

    def test_visible_consequence_must_use_the_same_safe_frontier(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-visible-frontier"
        )
        assert obligation is not None
        host = _host(repository)
        frontier = compute_maximal_safe_frontier(obligation, host=host)

        validate_visible_consequence(
            frontier,
            obligation=obligation,
            host=host,
            evidence_refs=frontier.safe_prefix_refs,
        )
        with self.assertRaisesRegex(CollaborationAdmissionError, "frontier"):
            validate_visible_consequence(
                frontier,
                obligation=obligation,
                host=host,
                evidence_refs=(
                    NativeBasisRef("world.scene", "scene-other", CAMPAIGN_REVISION),
                ),
            )

    def test_frontier_ignores_replayed_scope_basis_without_global_fallback(
        self,
    ) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-scope-currentness"
        )
        assert obligation is not None

        frontier = compute_maximal_safe_frontier(
            obligation,
            host=_host(repository),
            current_basis_refs=(
                NativeBasisRef("world.scene", "scene-other", CAMPAIGN_REVISION),
            ),
        )

        self.assertEqual(frontier.safe_prefix_refs, obligation.native_basis_refs)

    def test_unrelated_scope_builds_without_waiting_on_this_frontier(self) -> None:
        repository = RepositoryFixture()
        repository.put(
            "world.scene",
            "scene-other",
            {
                "kind": "world.scene",
                "id": "scene-other",
                "campaign_id": CAMPAIGN_ID,
                "revision": CAMPAIGN_REVISION,
                "state": {"name": "Other scene"},
            },
        )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-scope-one"
        )
        assert obligation is not None
        unrelated = replace(
            obligation,
            obligation_id="obligation-scope-two",
            dependency_scope={"scene_id": "scene-other"},
            native_basis_refs=(
                NativeBasisRef("world.scene", "scene-other", CAMPAIGN_REVISION),
            ),
        )

        host = _host(repository)
        first = compute_maximal_safe_frontier(obligation, host=host)
        second = compute_maximal_safe_frontier(unrelated, host=host)

        self.assertNotEqual(first.obligation_id, second.obligation_id)
        self.assertNotEqual(first.dependency_scope, second.dependency_scope)
        self.assertEqual(second.safe_prefix_refs, unrelated.native_basis_refs)

    def test_frontier_schema_has_no_technical_order_or_chronology_authority(
        self,
    ) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-technical-order"
        )
        assert obligation is not None
        frontier = compute_maximal_safe_frontier(obligation, host=_host(repository))
        value = frontier.to_mapping()

        self.assertNotIn("arrival_order", value)
        self.assertNotIn("cas_order", value)
        self.assertNotIn("generation_order", value)
        self.assertNotIn("chronology", value)
        value["arrival_order"] = 1

        with self.assertRaisesRegex(CollaborationAdmissionError, "frontier"):
            CollaborationFrontier.from_mapping(value)

    def test_frontier_round_trip_preserves_scope_and_pending_requirements(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository),
            obligation_id="obligation-frontier-round-trip",
        )
        assert obligation is not None
        frontier = compute_maximal_safe_frontier(obligation, host=_host(repository))

        restored = CollaborationFrontier.from_mapping(frontier.to_mapping())

        self.assertEqual(restored, frontier)

    def test_frontier_schema_projection_accepts_owner_evidence_only(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-frontier-schema"
        )
        assert obligation is not None
        value = compute_maximal_safe_frontier(
            obligation, host=_host(repository)
        ).to_mapping()

        schema = json.loads(
            (SCHEMAS / "collaboration-frontier.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(schema).validate(value)
        self.assertEqual(schema["properties"]["schema_version"]["const"], 1)


class CollaborationCloseHandoffTests(unittest.TestCase):
    def _closed_obligation(
        self, repository: RepositoryFixture, *, obligation_id: str
    ) -> tuple[CollaborationObligation, RepositoryFixture]:
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id=obligation_id
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
        _persist_obligation(repository, associated)
        closed = close_obligation(associated, host=_host(repository))
        _persist_obligation(repository, closed)
        return closed, repository

    def test_close_requires_current_generation_and_all_required_inputs(self) -> None:
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-close-required"
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)

        with self.assertRaisesRegex(CollaborationAdmissionError, "required"):
            close_obligation(obligation, host=_host(repository))

        with self.assertRaisesRegex(CollaborationAdmissionError, "generation"):
            close_obligation(obligation, host=_host(repository), generation=2)

    def test_predecessor_cannot_close_after_successor_is_current(self) -> None:
        repository = RepositoryFixture()
        predecessor = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-current-generation"
        )
        assert predecessor is not None
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        predecessor = associate_input(
            predecessor,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )
        _persist_obligation(repository, predecessor)

        successor = open_or_successor_obligation(
            _classify(repository),
            obligation_id=predecessor.obligation_id,
            generation=2,
            predecessor=predecessor,
        )
        assert successor is not None
        _persist_obligation(repository, successor)

        with self.assertRaisesRegex(CollaborationAdmissionError, "current"):
            close_obligation(predecessor, host=_host(repository))

    def test_closed_input_fingerprint_is_order_independent_and_round_trips_basis(
        self,
    ) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-close-fingerprint"
        )
        basis = closed.closed_basis

        reordered = replace(
            closed,
            accepted_input_uses=tuple(reversed(closed.accepted_input_uses)),
            accepted_input_contributors=tuple(
                reversed(closed.accepted_input_contributors)
            ),
        )
        self.assertEqual(
            closed.closed_input_set_fingerprint,
            reordered.closed_basis.closed_input_set_fingerprint,
        )
        self.assertEqual(
            basis, CollaborationClosedBasis.from_mapping(basis.to_mapping())
        )

    def test_duplicate_close_is_idempotent(self) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-close-idempotent"
        )

        self.assertIs(close_obligation(closed, host=_host(repository)), closed)

    def test_actionable_clause_is_pre_command_until_handoff(self) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-handoff"
        )
        original_clause = repository.records[
            route_native_record("runtime.intent_plan", ("plan-1",)).relative_path
        ]["clauses"][0]
        self.assertEqual(original_clause["execution_state"], "intent.pending")
        self.assertNotIn("command_id", original_clause)

        handoff = build_handoff(closed, host=_host(repository))

        self.assertIsInstance(handoff, CollaborationHandoff)
        self.assertEqual(
            handoff.entries[0].disposition,
            HandoffDisposition.RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH,
        )
        self.assertNotIn("command_id", handoff.to_mapping())
        self.assertNotIn("runtime.command", repr(handoff.to_mapping()))

    def test_handoff_does_not_resolve_before_native_clause_is_ready(
        self,
    ) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-apply-handoff"
        )
        handoff = build_handoff(closed, host=_host(repository))

        resolved = apply_handoff(closed, handoff, host=_host(repository))

        self.assertEqual(resolved.lifecycle, "CLOSED")
        self.assertEqual(
            resolved.closed_input_set_fingerprint, closed.closed_input_set_fingerprint
        )
        self.assertEqual(handoff.entries[0].execution_state, "intent.ready")
        self.assertIsNone(handoff.entries[0].command_id)
        original_clause = repository.records[
            route_native_record("runtime.intent_plan", ("plan-1",)).relative_path
        ]["clauses"][0]
        self.assertEqual(original_clause["execution_state"], "intent.pending")
        self.assertNotIn("command_id", original_clause)

    def test_closed_basis_and_handoff_match_owner_schemas(self) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-schema-close"
        )
        handoff = build_handoff(closed, host=_host(repository))
        closed_schema = json.loads(
            (SCHEMAS / "collaboration-closed-basis.schema.json").read_text(
                encoding="utf-8"
            )
        )
        handoff_schema = json.loads(
            (SCHEMAS / "collaboration-handoff.schema.json").read_text(encoding="utf-8")
        )

        Draft202012Validator(closed_schema).validate(closed.closed_basis.to_mapping())
        registry = Registry().with_resource(
            closed_schema["$id"], Resource.from_contents(closed_schema)
        )
        Draft202012Validator(handoff_schema, registry=registry).validate(
            handoff.to_mapping()
        )
        self.assertEqual(
            CollaborationHandoff.from_mapping(handoff.to_mapping()), handoff
        )
        self.assertEqual(handoff_schema["properties"]["schema_version"]["const"], 1)

    def test_closed_generation_rejects_late_input_without_replaying_mechanics(
        self,
    ) -> None:
        repository = RepositoryFixture()
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        closed, _ = self._closed_obligation(
            repository, obligation_id="obligation-late-input"
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "open"):
            associate_input(
                closed,
                _host(repository),
                "interaction-2",
                "clause-2",
                principal=_bob_principal(),
                player_route=_route(),
            )


class CollaborationPublicationRecoveryTests(unittest.TestCase):
    def _open_with_all_inputs(
        self, repository: CampaignPublicationRepositoryFixture, obligation_id: str
    ) -> CollaborationObligation:
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id=obligation_id
        )
        assert obligation is not None
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        associated = associate_input(
            obligation,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )
        _persist_obligation(repository, associated)
        return associated

    def test_t02b_publication_entry_point_is_runtime_host_routed(self) -> None:
        self.assertTrue(callable(getattr(collaboration_module, "publish_closed", None)))
        source = (ROOT / "GAME" / "TOOLS" / "collaboration.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("CollaborationPublicationClosure", source)
        self.assertNotIn("CollaborationPublicationResult", source)
        self.assertNotIn("publish_campaign_closure", source)

    def test_open_to_closed_publishes_obligation_and_retains_route_companions(
        self,
    ) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        opening = self._open_with_all_inputs(repository, "obligation-close-publish")

        closed = collaboration_module.publish_closed(
            opening, host=_host(repository, transport)
        )

        self.assertEqual(closed.lifecycle, "CLOSED")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )
        retried = collaboration_module.publish_closed(
            opening, host=_host(repository, transport)
        )
        self.assertEqual(retried, closed)
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )
        self.assertFalse(hasattr(repository, "publish_campaign_closure"))
        persisted = repository.records[
            route_native_record(
                "runtime.collaboration_obligation", (opening.obligation_id,)
            ).relative_path
        ]
        self.assertEqual(persisted["lifecycle"], "CLOSED")
        self.assertIsNotNone(persisted["closed_input_set_fingerprint"])
        for player_id in ("player-alice", "player-bob"):
            player = repository.records[
                route_native_record("world.player", (player_id,)).relative_path
            ]
            self.assertEqual(
                player["collaboration_route_refs"],
                [{"obligation_id": opening.obligation_id, "generation": 1}],
            )

    def test_stale_non_fast_forward_fails_closed_without_owner_mutation(self) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        transport.ref_revision_override = CHANGED_CAMPAIGN_REVISION
        opening = self._open_with_all_inputs(repository, "obligation-stale-close")
        before = deepcopy(
            repository.records[
                route_native_record(
                    "runtime.collaboration_obligation", (opening.obligation_id,)
                ).relative_path
            ]
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "publication"):
            collaboration_module.publish_closed(
                opening, host=_host(repository, transport)
            )

        self.assertEqual(
            repository.records[
                route_native_record(
                    "runtime.collaboration_obligation", (opening.obligation_id,)
                ).relative_path
            ],
            before,
        )
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_indeterminate_ack_reconciles_without_a_second_write(self) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        transport.response_status = "indeterminate"
        opening = self._open_with_all_inputs(repository, "obligation-indeterminate")

        closed = collaboration_module.publish_closed(
            opening, host=_host(repository, transport)
        )

        self.assertEqual(closed.lifecycle, "CLOSED")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_closed_recovery_reconstructs_fingerprint_and_resolved_recovery_is_idempotent(
        self,
    ) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        opening = self._open_with_all_inputs(repository, "obligation-recovery")
        host = _host(repository, transport)
        closed = collaboration_module.publish_closed(opening, host=host)
        writes_after_close = len(
            [name for name, _ in transport.calls if name == "update_ref"]
        )
        self.assertEqual(
            collaboration_module.publish_closed(opening, host=host), closed
        )
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]),
            writes_after_close,
        )

        recovered_closed = collaboration_module.recover_obligation(
            host, opening.obligation_id
        )
        self.assertEqual(recovered_closed, closed)
        handoff = build_handoff(recovered_closed, host=host)

        resolved = collaboration_module.resolve_waiting(closed, handoff, host=host)
        self.assertEqual(resolved.lifecycle, "RESOLVED")
        plan = repository.records[
            route_native_record("runtime.intent_plan", ("plan-1",)).relative_path
        ]
        self.assertEqual(plan["clauses"][0]["execution_state"], "intent.ready")
        for player_id in ("player-alice", "player-bob"):
            player = repository.records[
                route_native_record("world.player", (player_id,)).relative_path
            ]
            self.assertEqual(player["collaboration_route_refs"], [])

        resolution_operations = [
            operations for name, operations in transport.calls if name == "create_tree"
        ][-1]
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation", (opening.obligation_id,)
            ).relative_path,
            resolution_operations,
        )
        self.assertIn(
            route_native_record("runtime.intent_plan", ("plan-1",)).relative_path,
            resolution_operations,
        )
        for player_id in ("player-alice", "player-bob"):
            self.assertIn(
                route_native_record("world.player", (player_id,)).relative_path,
                resolution_operations,
            )

        writes_after_resolution = len(
            [name for name, _ in transport.calls if name == "update_ref"]
        )
        retried = collaboration_module.resolve_waiting(closed, handoff, host=host)
        recovered_resolved = collaboration_module.recover_obligation(
            host, opening.obligation_id
        )
        self.assertEqual(retried.lifecycle, "RESOLVED")
        self.assertEqual(recovered_resolved.lifecycle, "RESOLVED")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]),
            writes_after_resolution,
        )

    def test_resolve_rejects_a_changed_closed_fingerprint_and_obsolete_preserves_it(
        self,
    ) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        opening = self._open_with_all_inputs(
            repository, "obligation-fingerprint-closure"
        )
        host = _host(repository, transport)
        closed = collaboration_module.publish_closed(opening, host=host)
        handoff = build_handoff(closed, host=host)

        with self.assertRaisesRegex(CollaborationAdmissionError, "fingerprint"):
            collaboration_module.resolve_waiting(
                replace(closed, closed_input_set_fingerprint="b" * 64),
                handoff,
                host=host,
            )

        obsolete = replace(closed, lifecycle="OBSOLETE")
        self.assertEqual(
            obsolete.closed_input_set_fingerprint,
            closed.closed_input_set_fingerprint,
        )


if __name__ == "__main__":
    unittest.main()
