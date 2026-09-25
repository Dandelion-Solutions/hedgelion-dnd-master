"""W04.T01A/T01C/T02A collaboration owner contract tests."""

from __future__ import annotations

import json
import unittest
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from unittest import mock

import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS import collaboration as collaboration_module
from GAME.TOOLS import live_state as live_state_module
from GAME.TOOLS.access_control import (
    AccessControlContractError,
    PlayerRecord,
    VerifiedPrincipal,
    advance_multi_live_freeze,
    authorize_operation,
    build_principal_player_route,
    freeze_access_policy_transition,
    freeze_multi_live_forward_plan,
    freeze_player_access_transition,
    publish_forward_transition,
    resolve_player,
)
from GAME.TOOLS.collaboration import (
    CollaborationAccessReconciliation,
    CollaborationAdmissionError,
    CollaborationCatchUp,
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
    join_participant,
    open_or_successor_obligation,
    reconcile_player_route_companions,
    required_route_holders,
    validate_visible_consequence,
)
from GAME.TOOLS.history import observe_first_initialization_history
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveLifecycle,
    LiveNativeStatePack,
    LiveRouting,
    build_live_ref,
    build_live_route,
    derive_live_epoch_id,
    freeze_campaign_absorption_delta,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign
from GAME.TOOLS.recovery_roots import OperationalRoot, OperationalRootHandoff
from GAME.TOOLS.runtime_execution import NativeOrderingEvidence
from GAME.TOOLS.runtime_host import compose_runtime_host

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


CAMPAIGN_ID = "campaign-frostfall"
CAMPAIGN_REVISION = "a" * 40
TREE_SHA = "b" * 40
CHANGED_CAMPAIGN_REVISION = "c" * 40
LIVE_SOURCE_REVISION = "7" * 40
LIVE_CLOSED_REVISION = "8" * 40


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
        self.pin_calls = 0
        self._snapshots: dict[str, tuple[str, dict[str, object]]] = {}
        self._parents: dict[str, str] = {}
        self._changed_paths: dict[str, tuple[str, ...]] = {}
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
        self.capture_current_revision()

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        self.pin_calls += 1
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        return PinnedCampaign(CAMPAIGN_ID, self.current_revision, self.current_tree)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if pinned.campaign_id != CAMPAIGN_ID:
            raise KeyError("stale campaign pin")
        if (
            pinned.revision == self.current_revision
            and pinned.tree_sha == self.current_tree
        ):
            self.reads.append(path)
            return deepcopy(self.records[path])
        snapshot = self._snapshots.get(pinned.revision)
        if snapshot is None or snapshot[0] != pinned.tree_sha:
            raise KeyError("unknown exact campaign snapshot")
        self.reads.append(path)
        return deepcopy(snapshot[1][path])

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        snapshot = self._snapshots.get(revision)
        if snapshot is None:
            raise KeyError("unknown exact campaign commit")
        return {
            "ref": campaign_ref,
            "revision": revision,
            "tree_sha": snapshot[0],
            "parent_revision": self._parents.get(revision),
            "changed_paths": list(self._changed_paths.get(revision, ())),
        }

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        del repository_ref
        if ancestor_revision == descendant_revision:
            return {"relation": "EQUAL"}
        current = descendant_revision
        while current in self._parents:
            current = self._parents[current]
            if current == ancestor_revision:
                return {"relation": "ANCESTOR"}
        return {"relation": "NOT_ANCESTOR"}

    def capture_current_revision(self, *, parent_revision: str | None = None) -> None:
        if parent_revision is not None:
            self._parents[self.current_revision] = parent_revision
        parent = self._parents.get(self.current_revision)
        previous = self._snapshots.get(parent) if parent is not None else None
        if previous is None:
            previous = self._snapshots.get(self.current_revision)
        prior_records = {} if previous is None else previous[1]
        missing = object()
        self._changed_paths[self.current_revision] = tuple(
            sorted(
                path
                for path in set(prior_records) | set(self.records)
                if prior_records.get(path, missing) != self.records.get(path, missing)
            )
        )
        self._snapshots[self.current_revision] = (
            self.current_tree,
            deepcopy(self.records),
        )


class CampaignPublicationTransport:
    """Host-bound W02 publication transport with controllable outcomes."""

    def __init__(self, repository: CampaignPublicationRepositoryFixture) -> None:
        self.repository = repository
        self.calls: list[tuple[str, object]] = []
        self.response_status = "accepted"
        self.next_head = "d" * 40
        self.reconciliation_head: str | None = None
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
            parent_revision = self.repository.current_revision
            self.repository.current_revision = new_commit_sha
            self.repository.current_tree = "e" * 40
            for path, payload in self._pending_operations.items():
                if payload is None:
                    self.repository.records.pop(path, None)
                else:
                    self.repository.records[path] = _thaw_for_test(payload)
            self.repository.capture_current_revision(parent_revision=parent_revision)
            if (
                self.response_status == "indeterminate"
                and self.reconciliation_head is not None
                and self.reconciliation_head != new_commit_sha
            ):
                self.repository.current_revision = self.reconciliation_head
                self.repository.capture_current_revision(parent_revision=new_commit_sha)
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


class MutableCampaignRepositoryFixture(RepositoryFixture):
    """Exact-read fixture whose pinned campaign revision advances on closure."""

    def __init__(self, clause: dict[str, object] | None = None) -> None:
        self.current_revision = CAMPAIGN_REVISION
        super().__init__(clause)
        self.records["MANIFEST.yaml"] = _campaign_manifest()

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        return PinnedCampaign(CAMPAIGN_ID, self.current_revision, TREE_SHA)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if (
            pinned.campaign_id != CAMPAIGN_ID
            or pinned.revision != self.current_revision
        ):
            raise KeyError("stale campaign pin")
        self.reads.append(path)
        return deepcopy(self.records[path])


class CreatorHistoryFixture:
    def read_exact_campaign_ref(self, campaign_id: str) -> dict[str, object]:
        return {
            "campaign_id": campaign_id,
            "campaign_ref": "refs/heads/campaign/frostfall",
            "campaign_head_revision": CHANGED_CAMPAIGN_REVISION,
            "default_ref": "refs/heads/main",
            "default_head_revision": TREE_SHA,
            "initialization_revision": CAMPAIGN_REVISION,
        }

    def read_exact_commit(self, campaign_ref: str, revision: str) -> dict[str, object]:
        return {
            "campaign_id": CAMPAIGN_ID,
            "revision": revision,
            "parent_revision": TREE_SHA,
            "campaign_specific": True,
        }

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> dict[str, str]:
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> dict[str, object]:
        return {
            "author": {"login": "creator"},
            "authenticated": True,
            "per_user": True,
        }


def _creator_provenance():
    observation = observe_first_initialization_history(
        CreatorHistoryFixture(), CAMPAIGN_ID
    )
    assert observation.evidence is not None
    return observation.evidence


class LiveFixture:
    def __init__(
        self,
        route: LiveRouting | None = None,
        *,
        source_packs: Mapping[tuple[str, str, str], LiveNativeStatePack] | None = None,
    ) -> None:
        self.route = route
        self.source_packs = dict(source_packs or {})
        self.source_pack_reads: list[tuple[str, str, str]] = []

    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        del pinned
        return (
            self.route
            if self.route is not None
            else LiveRouting(campaign_id=campaign_id, entries=())
        )

    def read_selected_live_source(
        self, route: LiveRouting, source: LiveEnvelope
    ) -> LiveNativeStatePack:
        if route.campaign_id != source.campaign_id:
            raise KeyError("foreign selected LIVE source")
        self.source_pack_reads.append(source.source_key)
        return self.source_packs[source.source_key]


class TransitioningLiveFixture:
    """Host fixture that follows the exact pre/post campaign route revisions."""

    def __init__(
        self,
        *,
        predecessor_revision: str,
        predecessor_route: LiveRouting,
        final_route: LiveRouting,
        source_packs: Mapping[tuple[str, str, str], LiveNativeStatePack] | None = None,
    ) -> None:
        self.predecessor_revision = predecessor_revision
        self.predecessor_route = predecessor_route
        self.final_route = final_route
        self.source_packs = dict(source_packs or {})
        self.source_pack_reads: list[tuple[str, str, str]] = []

    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        if campaign_id != self.predecessor_route.campaign_id:
            raise KeyError(campaign_id)
        return (
            self.predecessor_route
            if pinned.revision == self.predecessor_revision
            else self.final_route
        )

    def read_selected_live_source(
        self, route: LiveRouting, source: LiveEnvelope
    ) -> LiveNativeStatePack:
        if route.campaign_id != source.campaign_id:
            raise KeyError("foreign selected LIVE source")
        self.source_pack_reads.append(source.source_key)
        return self.source_packs[source.source_key]


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


def _access_campaign(
    *,
    revision: str = CAMPAIGN_REVISION,
    player_ids: tuple[str, ...] = ("player-alice", "player-bob"),
    join_policy: str = "invite_only",
) -> dict[str, object]:
    return {
        "schema_version": 4,
        "campaign_contract": {"created_with": 2, "current": 2},
        "campaign_id": CAMPAIGN_ID,
        "revision": revision,
        "campaign_name": "The Frostfall",
        "campaign_name_origin": "creator",
        "branch": "campaign/frostfall",
        "status": "active",
        "created_at": "2026-09-24T00:00:00Z",
        "mode": "multiplayer",
        "engine": {"update_policy": "ask"},
        "ruleset": {"baseline": "D&D 2024 / SRD 5.2.1"},
        "rules": {"baseline": "D&D 2024 / SRD 5.2.1"},
        "storage": {"state_root": "STATE", "index_root": "INDEX"},
        "sync": {"force_push_allowed": False, "persistence_policy": "batched"},
        "world_time": {"calendar_id": None},
        "players": {
            "join_policy": join_policy,
            "player_ids": list(player_ids),
        },
        "last_checkpoint_id": None,
    }


def _campaign_manifest(
    *,
    player_ids: tuple[str, ...] = ("player-alice", "player-bob"),
    join_policy: str = "invite_only",
    mode: str = "multiplayer",
) -> dict[str, object]:
    body = _access_campaign(player_ids=player_ids, join_policy=join_policy)
    body.pop("revision")
    body["mode"] = mode
    return body


def _self_deactivation_transition(
    repository: MutableCampaignRepositoryFixture,
    *,
    player_id: str = "player-bob",
    player_ids: tuple[str, ...] = ("player-alice", "player-bob"),
):
    player_path = route_native_record("world.player", (player_id,)).relative_path
    current_player = deepcopy(repository.records[player_path])
    principal = _bob_principal()
    resolution = resolve_player(
        principal,
        _route(),
        lambda candidate_id: repository.records[
            route_native_record("world.player", (candidate_id,)).relative_path
        ],
        campaign_id=CAMPAIGN_ID,
    )
    proposed_player = deepcopy(current_player)
    proposed_player["status"] = "inactive"
    proposed_player["deactivated_by"] = "self"
    return freeze_player_access_transition(
        principal,
        resolution,
        operation="deactivate_self",
        current_player=current_player,
        proposed_player=proposed_player,
        current_campaign=_access_campaign(player_ids=player_ids),
        proposed_campaign=_access_campaign(
            revision=CHANGED_CAMPAIGN_REVISION,
            player_ids=player_ids,
        ),
        expected_campaign_revision=CAMPAIGN_REVISION,
        proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
        live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
    )


def _self_reactivation_transition(
    repository: MutableCampaignRepositoryFixture,
):
    player_path = route_native_record("world.player", ("player-bob",)).relative_path
    current_player = deepcopy(repository.records[player_path])
    current_player["status"] = "inactive"
    current_player["deactivated_by"] = "self"
    repository.put("world.player", "player-bob", current_player)
    principal = _bob_principal()
    resolution = resolve_player(
        principal,
        _route(),
        lambda candidate_id: repository.records[
            route_native_record("world.player", (candidate_id,)).relative_path
        ],
        campaign_id=CAMPAIGN_ID,
    )
    proposed_player = deepcopy(current_player)
    proposed_player["status"] = "active"
    proposed_player["deactivated_by"] = None
    return freeze_player_access_transition(
        principal,
        resolution,
        operation="reactivate",
        current_player=current_player,
        proposed_player=proposed_player,
        current_campaign=_access_campaign(),
        proposed_campaign=_access_campaign(revision=CHANGED_CAMPAIGN_REVISION),
        expected_campaign_revision=CAMPAIGN_REVISION,
        proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
        live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
    )


def _join_policy_transition(
    *,
    player_ids: tuple[str, ...] = ("player-alice", "player-bob"),
):
    return freeze_access_policy_transition(
        VerifiedPrincipal(stable_account_id="99", login="creator"),
        current_campaign=_access_campaign(player_ids=player_ids),
        proposed_campaign=_access_campaign(
            revision=CHANGED_CAMPAIGN_REVISION,
            player_ids=player_ids,
            join_policy="open_contributors",
        ),
        creator_provenance=_creator_provenance(),
        expected_campaign_revision=CAMPAIGN_REVISION,
        proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
        live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
    )


def _singleplayer_transition(
    *,
    player_ids: tuple[str, ...] = ("player-alice", "player-bob"),
):
    return freeze_access_policy_transition(
        VerifiedPrincipal(stable_account_id="99", login="creator"),
        current_campaign=_access_campaign(player_ids=player_ids),
        proposed_campaign={
            **_access_campaign(
                revision=CHANGED_CAMPAIGN_REVISION,
                player_ids=player_ids,
            ),
            "mode": "singleplayer",
        },
        creator_provenance=_creator_provenance(),
        expected_campaign_revision=CAMPAIGN_REVISION,
        proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
        live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
    )


def _mechanical_grant_revocation_transition(
    repository: MutableCampaignRepositoryFixture,
):
    player_path = route_native_record("world.player", ("player-bob",)).relative_path
    current_player = deepcopy(repository.records[player_path])
    current_player["policy_authority"] = {"mechanical_override_policy": True}
    repository.put("world.player", "player-bob", current_player)
    resolution = resolve_player(
        _bob_principal(),
        _route(),
        lambda candidate_id: repository.records[
            route_native_record("world.player", (candidate_id,)).relative_path
        ],
        campaign_id=CAMPAIGN_ID,
    )
    proposed_player = deepcopy(current_player)
    proposed_player["policy_authority"] = {"mechanical_override_policy": False}
    return freeze_player_access_transition(
        VerifiedPrincipal(stable_account_id="99", login="creator"),
        resolution,
        operation="revoke_mechanical_override",
        current_player=current_player,
        proposed_player=proposed_player,
        current_campaign=_access_campaign(),
        proposed_campaign=_access_campaign(revision=CHANGED_CAMPAIGN_REVISION),
        creator_provenance=_creator_provenance(),
        expected_campaign_revision=CAMPAIGN_REVISION,
        proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
        live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
    )


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
    live: LiveFixture | None = None,
) -> object:
    return compose_runtime_host(
        CAMPAIGN_ID, repository, live or LiveFixture(), publication
    )


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
    semantic_class: str = "ACTIONABLE_INTENT",
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
                    "collaboration_semantic_class": semantic_class,
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


def _attach_route_ref(
    repository: RepositoryFixture,
    obligation: CollaborationObligation,
    *player_ids: str,
) -> None:
    for player_id in player_ids:
        path = route_native_record("world.player", (player_id,)).relative_path
        player = repository.records[path]
        refs = {
            (ref["obligation_id"], ref["generation"])
            for ref in player.get("collaboration_route_refs", ())
        }
        refs.add((obligation.obligation_id, obligation.generation))
        player["collaboration_route_refs"] = [
            {"obligation_id": obligation_id, "generation": generation}
            for obligation_id, generation in sorted(refs)
        ]


def _live_source(scene_id: str) -> LiveEnvelope:
    claims = (LiveClaim.exact_owner("world.actor", f"actor-{scene_id}"),)
    epoch_id = derive_live_epoch_id(CAMPAIGN_ID, scene_id, CAMPAIGN_REVISION, claims)
    return LiveEnvelope(
        campaign_id=CAMPAIGN_ID,
        scene_id=scene_id,
        epoch_id=epoch_id,
        opening_campaign_revision=CAMPAIGN_REVISION,
        source_ref=build_live_ref(CAMPAIGN_ID, scene_id, epoch_id),
        source_revision=LIVE_SOURCE_REVISION,
        claims=claims,
    )


def _live_absorption_delta(
    route: LiveRouting,
    *,
    expected_campaign_revision: str,
    proposed_campaign_revision: str,
    event_index: Mapping[str, object] | None = None,
    operational_roots: Mapping[str, object] | None = None,
) -> live_state_module.FrozenCampaignAbsorptionDelta:
    sources = tuple(route.entries)
    packed_states: dict[tuple[str, str, str], LiveNativeStatePack] = {}
    for source in sources:
        actor_id = f"actor-{source.scene_id}"
        native_owner_states: dict[str, object] = {
            "world.actor": {
                "schema_version": 1,
                "kind": "world.actor",
                "id": actor_id,
                "state": {"concept": source.scene_id},
            }
        }
        if event_index is not None:
            event_id = f"live-event-{source.scene_id}"
            event_record = {
                "schema_version": 1,
                "event_id": event_id,
                "semantic_order": 1,
                "kind": "event.action",
                "provenance_refs": ["source.live"],
                "semantic_delta": {"scene_id": source.scene_id},
            }
            native_owner_states["runtime.semantic_event"] = {
                "complete": True,
                "upper_ordinal": 1,
                "entries": [
                    {
                        "ordinal": 1,
                        "event_id": event_id,
                        "event_record": event_record,
                    }
                ],
            }
        unresolved_work: dict[str, object] = {}
        if operational_roots is not None:
            absorbed_root = OperationalRoot(
                CAMPAIGN_ID,
                "runtime.procedure",
                "procedure-live-absorption",
                route_native_record(
                    "runtime.procedure", ("procedure-live-absorption",)
                ).relative_path,
            )
            handoff = OperationalRootHandoff(
                campaign_id=CAMPAIGN_ID,
                source_scope="LIVE",
                source_revision=source.source_revision,
                roots=(absorbed_root,),
                source_key=source.source_key,
                source_lifecycle=source.status.value,
                complete=True,
            )
            unresolved_work = {
                "runtime.procedure": {
                    "schema_version": 1,
                    "kind": "runtime.procedure",
                    "id": "procedure-live-absorption",
                    "state": {"concept": source.scene_id},
                },
                "runtime.operational_root_handoff": handoff.to_dict(),
            }
        packed_states[source.source_key] = LiveNativeStatePack(
            source_key=source.source_key,
            source_revision=source.source_revision,
            next_source_native_creation_ordinal=source.next_source_native_creation_ordinal,
            source_native_ids=source.source_native_ids,
            native_owner_states=native_owner_states,
            provenance={},
            privacy={},
            chronology={},
            unresolved_work=unresolved_work,
        )
    campaign_state = _access_campaign(revision=expected_campaign_revision)
    if event_index is not None:
        campaign_state["path_snapshots"] = {
            "INDEX/EVENT_INDEX.yaml": deepcopy(dict(event_index))
        }
    if operational_roots is not None:
        path_snapshots = dict(campaign_state.get("path_snapshots", {}))
        path_snapshots["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"] = deepcopy(
            dict(operational_roots)
        )
        campaign_state["path_snapshots"] = path_snapshots
    return freeze_campaign_absorption_delta(
        sources,
        route=route,
        packed_states=packed_states,
        campaign_state=campaign_state,
        expected_campaign_revision=expected_campaign_revision,
        proposed_campaign_revision=proposed_campaign_revision,
    )


def _live_delta_packs(
    delta: live_state_module.FrozenCampaignAbsorptionDelta,
) -> dict[tuple[str, str, str], LiveNativeStatePack]:
    return {
        attempt.source_key: attempt.packed_state for attempt in delta.source_attempts
    }


def _accepted_live_close_ack(attempt: object) -> dict[str, object]:
    return {
        "accepted": True,
        "source_key": attempt.source_key,  # type: ignore[attr-defined]
        "target_ref": attempt.target_ref,  # type: ignore[attr-defined]
        "expected_source_revision": attempt.expected_source_revision,  # type: ignore[attr-defined]
        "new_source_revision": attempt.proposed_source_revision,  # type: ignore[attr-defined]
        "selected_route": attempt.selected_route.as_mapping(),  # type: ignore[attr-defined]
        "successor": attempt.successor_route.as_mapping(),  # type: ignore[attr-defined]
    }


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
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")

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
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")

        with self.assertRaisesRegex(CollaborationAdmissionError, "semantic class"):
            associate_input(
                obligation,
                _host(repository),
                "interaction-2",
                "clause-2",
                principal=_bob_principal(),
                player_route=_route(),
            )

    def test_association_reloads_current_obligation_generation_before_mutation(
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
        predecessor = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-current-input"
        )
        assert predecessor is not None
        successor = open_or_successor_obligation(
            _classify(repository),
            obligation_id=predecessor.obligation_id,
            generation=2,
            predecessor=predecessor,
        )
        assert successor is not None
        _persist_obligation(repository, successor)
        _attach_route_ref(repository, successor, "player-alice", "player-bob")

        with self.assertRaisesRegex(CollaborationAdmissionError, "current"):
            associate_input(
                predecessor,
                _host(repository),
                "interaction-2",
                "clause-2",
                principal=_bob_principal(),
                player_route=_route(),
            )

    def test_association_requires_the_callers_current_obligation_route_ref(
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
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-route-current"
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        repository.records[bob_path]["collaboration_route_refs"] = []  # type: ignore[index]

        with self.assertRaisesRegex(CollaborationAdmissionError, "route"):
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
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
        first = associate_input(
            obligation,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )
        _persist_obligation(repository, first)
        second = associate_input(
            first,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )

        self.assertEqual(second, first)
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
        _persist_obligation(repository, successor)
        _attach_route_ref(repository, successor, "player-alice", "player-bob")

        self.assertEqual(successor.predecessor_generation, 1)
        self.assertEqual(predecessor.generation, 1)

        with self.assertRaisesRegex(CollaborationAdmissionError, "current"):
            associate_input(
                predecessor,
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
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")

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
        repository = RepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-forged-input"
        )

        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
        with self.assertRaisesRegex(CollaborationAdmissionError, "PLAYER"):
            associate_input(
                obligation,
                _host(repository),
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
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
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
        _persist_obligation(repository, predecessor)
        _attach_route_ref(repository, predecessor, "player-alice", "player-bob")
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


class CollaborationJoinCatchUpTests(unittest.TestCase):
    def _open_with_current_route(
        self, repository: RepositoryFixture, obligation_id: str
    ) -> CollaborationObligation:
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id=obligation_id
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
        return obligation

    def test_join_revalidates_current_binding_and_routing_before_mutable_input(
        self,
    ) -> None:
        repository = RepositoryFixture()
        obligation = self._open_with_current_route(repository, "obligation-join")

        catch_up = join_participant(
            _host(repository), principal=_principal(), player_route=_route()
        )

        self.assertIsInstance(catch_up, CollaborationCatchUp)
        self.assertEqual(catch_up.player_id, "player-alice")
        self.assertEqual(
            catch_up.obligations[0].obligation_id, obligation.obligation_id
        )
        self.assertEqual(catch_up.obligations[0].participant_role, "ORIGINATING")

    def test_catch_up_exposes_only_the_recipient_obligation_projection(self) -> None:
        repository = RepositoryFixture(
            _collective_clause() | {"purpose": "planning-private-secret"}
        )
        obligation = self._open_with_current_route(
            repository, "obligation-recipient-safe"
        )
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
        _attach_route_ref(repository, associated, "player-alice", "player-bob")

        catch_up = join_participant(
            _host(repository), principal=_principal(), player_route=_route()
        )
        serialized = json.dumps(catch_up.to_mapping(), sort_keys=True)

        self.assertEqual(catch_up.obligations[0].contribution_status, "RECEIVED")
        self.assertNotIn("purpose", catch_up.obligations[0].to_mapping())
        self.assertNotIn("normalized_semantics", serialized)
        self.assertNotIn("enter", serialized)
        self.assertNotIn("player-bob", serialized)
        self.assertNotIn("planning", serialized)
        self.assertNotIn("private", serialized)
        schema = json.loads(
            (SCHEMAS / "collaboration-catch-up.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(schema).validate(catch_up.to_mapping())
        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)

    def test_stale_or_deactivated_access_fails_closed(self) -> None:
        repository = RepositoryFixture()
        self._open_with_current_route(repository, "obligation-access")
        player_path = route_native_record(
            "world.player", ("player-alice",)
        ).relative_path
        repository.records[player_path]["status"] = "inactive"

        with self.assertRaisesRegex(CollaborationAdmissionError, "active"):
            join_participant(
                _host(repository), principal=_principal(), player_route=_route()
            )

    def test_changed_campaign_basis_fails_before_catch_up_projection(self) -> None:
        repository = ChangingPinRepositoryFixture()
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-stale-basis"
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice")
        repository.pin_calls = 0

        with self.assertRaisesRegex(CollaborationAdmissionError, "basis"):
            join_participant(
                _host(repository), principal=_principal(), player_route=_route()
            )

    def test_changed_native_obligation_basis_revision_fails_closed_before_catch_up(
        self,
    ) -> None:
        repository = RepositoryFixture()
        self._open_with_current_route(repository, "obligation-stale-native-basis")
        scene_path = route_native_record("world.scene", ("scene-market",)).relative_path
        repository.records[scene_path]["revision"] = CHANGED_CAMPAIGN_REVISION  # type: ignore[index]

        with self.assertRaisesRegex(CollaborationAdmissionError, "basis"):
            join_participant(
                _host(repository), principal=_principal(), player_route=_route()
            )

    def test_cursor_hint_is_not_a_consumption_receipt_or_filter(self) -> None:
        repository = RepositoryFixture()
        self._open_with_current_route(repository, "obligation-cursor")

        catch_up = join_participant(
            _host(repository),
            principal=_principal(),
            player_route=_route(),
            cursor_hint="session-cursor-7",
        )
        serialized = catch_up.to_mapping()

        self.assertEqual(serialized["cursor_hint"], "session-cursor-7")
        self.assertNotIn("human_consumed", serialized)
        self.assertNotIn("consumed", serialized)
        self.assertEqual(len(catch_up.obligations), 1)

    def test_join_reads_only_exact_obligation_ids_from_current_player_route(
        self,
    ) -> None:
        repository = RepositoryFixture()
        self._open_with_current_route(repository, "obligation-known-id")
        rogue = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-not-routed"
        )
        assert rogue is not None
        _persist_obligation(repository, rogue)
        repository.reads.clear()

        join_participant(
            _host(repository), principal=_principal(), player_route=_route()
        )

        known_path = route_native_record(
            "runtime.collaboration_obligation", ("obligation-known-id",)
        ).relative_path
        rogue_path = route_native_record(
            "runtime.collaboration_obligation", ("obligation-not-routed",)
        ).relative_path
        self.assertIn(known_path, repository.reads)
        self.assertNotIn(rogue_path, repository.reads)


class CollaborationPublicationRecoveryTests(unittest.TestCase):
    def _open_with_all_inputs(
        self,
        repository: CampaignPublicationRepositoryFixture,
        obligation_id: str,
        *,
        input_semantic_class: str = "ACTIONABLE_INTENT",
    ) -> CollaborationObligation:
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id=obligation_id
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(repository, obligation, "player-alice", "player-bob")
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
            semantic_class=input_semantic_class,
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

    def test_persisted_obligation_validation_reuses_prepared_host_basis(self) -> None:
        repository = CampaignPublicationRepositoryFixture()
        obligation = self._open_with_all_inputs(repository, "obligation-basis-reuse")
        host = _host(repository)
        basis = host._begin_operation()
        persisted = obligation.to_mapping()
        repository.pin_calls = 0

        restored = CollaborationObligation.from_mapping(
            persisted, host=host, basis=basis
        )

        self.assertEqual(restored, obligation)
        # One fresh pin verifies that the original basis did not move after
        # native owner reads; parsing must not acquire a second basis of its own.
        self.assertEqual(repository.pin_calls, 1)

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

    def test_non_actionable_handoff_does_not_publish_an_intent_plan_operation(
        self,
    ) -> None:
        repository = CampaignPublicationRepositoryFixture(
            _collective_clause() | {"collaboration_semantic_class": "OOC_COORDINATION"}
        )
        transport = CampaignPublicationTransport(repository)
        opening = self._open_with_all_inputs(
            repository,
            "obligation-non-actionable",
            input_semantic_class="OOC_COORDINATION",
        )
        host = _host(repository, transport)

        closed = collaboration_module.publish_closed(opening, host=host)
        handoff = build_handoff(closed, host=host)
        self.assertEqual(
            handoff.entries[0].disposition,
            HandoffDisposition.CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT,
        )

        collaboration_module.resolve_waiting(closed, handoff, host=host)

        intent_plan_path = route_native_record(
            "runtime.intent_plan", ("plan-1",)
        ).relative_path
        resolution_operations = [
            operations for name, operations in transport.calls if name == "create_tree"
        ][-1]
        self.assertNotIn(intent_plan_path, resolution_operations)

    def test_persisted_obsolete_recovery_preserves_prior_holders_for_route_removal(
        self,
    ) -> None:
        repository = CampaignPublicationRepositoryFixture()
        transport = CampaignPublicationTransport(repository)
        opening = self._open_with_all_inputs(repository, "obligation-obsolete")
        host = _host(repository, transport)

        closed = collaboration_module.publish_closed(opening, host=host)
        obsolete = collaboration_module.obsolete_generation(closed, host=host)

        self.assertEqual(obsolete.lifecycle, "OBSOLETE")
        self.assertEqual(
            obsolete.closed_input_set_fingerprint,
            closed.closed_input_set_fingerprint,
        )
        recovered = collaboration_module.recover_obligation(host, opening.obligation_id)
        self.assertEqual(recovered, obsolete)
        self.assertEqual(recovered.closed_basis, closed.closed_basis)
        self.assertEqual(
            tuple(
                companion.player_id
                for companion in collaboration_module.reconcile_player_route_companions(
                    recovered
                )
            ),
            ("player-alice", "player-bob"),
        )
        for player_id in ("player-alice", "player-bob"):
            player = repository.records[
                route_native_record("world.player", (player_id,)).relative_path
            ]
            self.assertEqual(player["collaboration_route_refs"], [])

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


class CollaborationAccessReconciliationTests(unittest.TestCase):
    def test_module_revision_changes_without_changing_persisted_schema(self) -> None:
        self.assertEqual(collaboration_module.FRAMEWORK_MODULE_VERSION, "1.0.19")
        self.assertEqual(collaboration_module.COLLABORATION_SCHEMA_VERSION, 3)

    def _open_pending(
        self, *, required: tuple[dict[str, str], ...] | None = None
    ) -> tuple[MutableCampaignRepositoryFixture, CollaborationObligation]:
        clause = _collective_clause()
        if required is not None:
            clause["required_contributors"] = list(required)
        repository = MutableCampaignRepositoryFixture(clause)
        if required is not None and any(
            ref["player_id"] == "player-carol" for ref in required
        ):
            repository.put(
                "world.player",
                "player-carol",
                _player_record("player-carol", "44", "carol", "pc-carol"),
            )
            repository.records["MANIFEST.yaml"] = _campaign_manifest(
                player_ids=("player-alice", "player-bob", "player-carol")
            )
        obligation = open_or_successor_obligation(
            _classify(repository), obligation_id="obligation-access-reconcile"
        )
        assert obligation is not None
        _persist_obligation(repository, obligation)
        _attach_route_ref(
            repository,
            obligation,
            *tuple(
                sorted(
                    {
                        "player-alice",
                        *(ref.player_id for ref in obligation.required_contributors),
                    }
                )
            ),
        )
        return repository, obligation

    def _accept_bob_input(
        self,
        repository: MutableCampaignRepositoryFixture,
        obligation: CollaborationObligation,
    ) -> CollaborationObligation:
        _add_persisted_input(
            repository,
            interaction_id="interaction-2",
            clause_id="clause-2",
            player_id="player-bob",
            pc_id="pc-bob",
        )
        accepted = associate_input(
            obligation,
            _host(repository),
            "interaction-2",
            "clause-2",
            principal=_bob_principal(),
            player_route=_route(),
        )
        _persist_obligation(repository, accepted)
        return accepted

    def test_pending_required_player_deactivation_obsoletes_exact_generation(
        self,
    ) -> None:
        repository, obligation = self._open_pending()
        transition = _self_deactivation_transition(repository)
        before = deepcopy(repository.records)

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )

        self.assertEqual(
            reconciliation.after_authority_view["player"]["status"], "inactive"
        )
        self.assertIn("MANIFEST.yaml", repository.reads)
        self.assertEqual(
            tuple(
                (item.obligation_id, item.generation)
                for item in reconciliation.obligations
            ),
            ((obligation.obligation_id, obligation.generation),),
        )
        obsolete = reconciliation.obligations[0]
        self.assertEqual(obsolete.lifecycle, "OBSOLETE")
        self.assertEqual(obsolete.accepted_input_uses, obligation.accepted_input_uses)
        self.assertEqual(
            obsolete.accepted_input_contributors,
            obligation.accepted_input_contributors,
        )
        self.assertEqual(repository.records, before)
        repeated = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )
        self.assertEqual(repeated, reconciliation)
        self.assertEqual(repository.records, before)

    def test_w03_full_body_guard_uses_loaded_manifest_and_rejects_body_drift(
        self,
    ) -> None:
        for mutation in ("changed", "missing", "added"):
            with self.subTest(mutation=mutation):
                repository, _obligation = self._open_pending()
                transition = _self_deactivation_transition(repository)
                current_manifest = deepcopy(repository.records["MANIFEST.yaml"])
                if mutation == "changed":
                    current_manifest["campaign_name"] = "Changed name"
                elif mutation == "missing":
                    current_manifest.pop("created_at")
                else:
                    current_manifest["unmodeled_owner_field"] = "changed"
                repository.records["MANIFEST.yaml"] = current_manifest

                with self.assertRaises(CollaborationAdmissionError):
                    collaboration_module.reconcile_collaboration_for_player_access_transition(
                        transition, host=_host(repository)
                    )

    def test_reactivation_restores_only_prospective_pending_eligibility(self) -> None:
        repository, obligation = self._open_pending()
        transition = _self_reactivation_transition(repository)

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )

        self.assertEqual(
            reconciliation.after_authority_view["player"]["status"], "active"
        )
        self.assertEqual(len(reconciliation.obligations), 1)
        self.assertEqual(reconciliation.obligations[0].lifecycle, "OPEN")
        self.assertEqual(
            reconciliation.obligations[0].accepted_input_uses,
            obligation.accepted_input_uses,
        )

    def test_satisfied_requirement_keeps_valid_generation_and_history_prospectively(
        self,
    ) -> None:
        repository, obligation = self._open_pending(
            required=(
                {"player_id": "player-bob", "pc_id": "pc-bob"},
                {"player_id": "player-carol", "pc_id": "pc-carol"},
            )
        )
        accepted = self._accept_bob_input(repository, obligation)
        transition = _self_deactivation_transition(
            repository,
            player_ids=("player-alice", "player-bob", "player-carol"),
        )

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )

        current = reconciliation.obligations[0]
        self.assertEqual(current.lifecycle, "OPEN")
        self.assertEqual(current.accepted_input_uses, accepted.accepted_input_uses)
        self.assertEqual(
            current.accepted_input_contributors,
            accepted.accepted_input_contributors,
        )
        self.assertEqual(
            tuple(
                ref.player_id
                for ref in collaboration_module._pending_required_contributors(current)
            ),
            ("player-carol",),
        )

        # Simulate T04B's same-closure publication so the exact-recovery path sees
        # the prospective PLAYER state and unchanged accepted collaboration data.
        repository.put(
            "world.player",
            "player-bob",
            _thaw_for_test(transition.proposed_player),
        )
        _persist_obligation(repository, current)
        repository.current_revision = CHANGED_CAMPAIGN_REVISION
        host = _host(repository)

        recovered = collaboration_module.recover_obligation(
            host, obligation.obligation_id
        )
        self.assertEqual(recovered.accepted_input_uses, accepted.accepted_input_uses)
        self.assertEqual(
            recovered.accepted_input_contributors, accepted.accepted_input_contributors
        )
        with self.assertRaisesRegex(CollaborationAdmissionError, "active|join"):
            associate_input(
                recovered,
                host,
                "interaction-3",
                "clause-3",
                principal=_bob_principal(),
                player_route=_route(),
            )
        with self.assertRaisesRegex(CollaborationAdmissionError, "active|join"):
            join_participant(host, principal=_bob_principal(), player_route=_route())
        with self.assertRaisesRegex(CollaborationAdmissionError, "active"):
            CollaborationObligation.from_mapping(
                repository.records[
                    route_native_record(
                        "runtime.collaboration_obligation",
                        (obligation.obligation_id,),
                    ).relative_path
                ],
                host=host,
            )

    def test_exact_hydration_rejects_forged_historical_author_or_pc(self) -> None:
        repository, obligation = self._open_pending(
            required=(
                {"player_id": "player-bob", "pc_id": "pc-bob"},
                {"player_id": "player-carol", "pc_id": "pc-carol"},
            )
        )
        self._accept_bob_input(repository, obligation)
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        inactive_bob = deepcopy(repository.records[bob_path])
        inactive_bob["status"] = "inactive"
        inactive_bob["deactivated_by"] = "self"
        repository.put("world.player", "player-bob", inactive_bob)
        repository.current_revision = CHANGED_CAMPAIGN_REVISION
        host = _host(repository)
        obligation_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        current = deepcopy(repository.records[obligation_path])

        for forged_value, expected_error in (
            (
                current
                | {
                    "accepted_input_contributors": [
                        current["accepted_input_contributors"][0],
                        current["accepted_input_contributors"][1]
                        | {"player_id": "player-alice"},
                    ]
                },
                "author|holder",
            ),
            (
                current
                | {
                    "accepted_input_contributors": [
                        current["accepted_input_contributors"][0],
                        current["accepted_input_contributors"][1]
                        | {"pc_id": "pc-not-controlled"},
                    ]
                },
                "PC association",
            ),
        ):
            with self.subTest(expected_error=expected_error):
                repository.put(
                    "runtime.collaboration_obligation",
                    obligation.obligation_id,
                    forged_value,
                )
                with self.assertRaisesRegex(
                    CollaborationAdmissionError, expected_error
                ):
                    collaboration_module.recover_obligation(
                        host, obligation.obligation_id
                    )
        repository.put(
            "runtime.collaboration_obligation", obligation.obligation_id, current
        )

    def test_remaining_active_contributor_can_close_and_handoff_retained_history(
        self,
    ) -> None:
        repository, obligation = self._open_pending(
            required=(
                {"player_id": "player-bob", "pc_id": "pc-bob"},
                {"player_id": "player-carol", "pc_id": "pc-carol"},
            )
        )
        self._accept_bob_input(repository, obligation)
        transition = _self_deactivation_transition(
            repository,
            player_ids=("player-alice", "player-bob", "player-carol"),
        )
        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )
        current = reconciliation.obligations[0]
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        repository.put(
            "world.player",
            "player-bob",
            _thaw_for_test(transition.proposed_player),
        )
        _persist_obligation(repository, current)
        repository.current_revision = CHANGED_CAMPAIGN_REVISION
        host = _host(repository)

        _add_persisted_input(
            repository,
            interaction_id="interaction-3",
            clause_id="clause-3",
            player_id="player-carol",
            pc_id="pc-carol",
        )
        carol = VerifiedPrincipal(stable_account_id="44", login="carol")
        carol_route = build_principal_player_route(
            CAMPAIGN_ID,
            (
                PlayerRecord(
                    "player-carol",
                    "44",
                    "carol",
                    "active",
                    None,
                    controlled_pc_ids=("pc-carol",),
                ),
            ),
        )
        associated = associate_input(
            current,
            host,
            "interaction-3",
            "clause-3",
            principal=carol,
            player_route=carol_route,
        )
        _persist_obligation(repository, associated)

        closed = collaboration_module.close_obligation(associated, host=host)
        self.assertEqual(closed.lifecycle, "CLOSED")
        self.assertEqual(
            closed.accepted_input_uses,
            (
                ("interaction-1", "clause-1"),
                ("interaction-2", "clause-2"),
                ("interaction-3", "clause-3"),
            ),
        )
        _persist_obligation(repository, closed)
        handoff = build_handoff(closed, host=host)
        self.assertEqual(len(handoff.entries), 3)
        self.assertEqual(
            repository.records[bob_path]["status"],
            "inactive",
        )

    def test_campaign_join_policy_change_preserves_existing_obligation(self) -> None:
        repository, _obligation = self._open_pending()
        transition = _join_policy_transition(player_ids=("player-alice", "player-bob"))

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_access_policy_transition(
                transition, host=_host(repository)
            )
        )

        self.assertEqual(
            reconciliation.after_authority_view["campaign"]["players"]["join_policy"],
            "open_contributors",
        )
        self.assertEqual(len(reconciliation.obligations), 1)
        self.assertEqual(reconciliation.obligations[0].lifecycle, "OPEN")

    def test_singleplayer_transition_fails_closed_for_unverified_pending_agency(
        self,
    ) -> None:
        repository, _obligation = self._open_pending()
        transition = _singleplayer_transition()
        before = deepcopy(repository.records)

        with self.assertRaisesRegex(CollaborationAdmissionError, "creator|agency"):
            collaboration_module.reconcile_collaboration_for_access_policy_transition(
                transition, host=_host(repository)
            )
        self.assertEqual(repository.records, before)

    def test_singleplayer_uncertainty_does_not_obsolete_closed_generation(self) -> None:
        repository, obligation = self._open_pending()
        accepted = self._accept_bob_input(repository, obligation)
        closed = collaboration_module.close_obligation(accepted, host=_host(repository))
        _persist_obligation(repository, closed)
        transition = _singleplayer_transition()
        before = deepcopy(repository.records)

        with self.assertRaisesRegex(CollaborationAdmissionError, "creator|agency"):
            collaboration_module.reconcile_collaboration_for_access_policy_transition(
                transition, host=_host(repository)
            )

        current_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        self.assertEqual(repository.records[current_path]["lifecycle"], "CLOSED")
        self.assertEqual(
            repository.records[current_path]["closed_input_set_fingerprint"],
            closed.closed_input_set_fingerprint,
        )
        self.assertEqual(repository.records, before)

    def test_campaign_policy_mutation_without_creator_provenance_fails_closed(
        self,
    ) -> None:
        with self.assertRaises(AccessControlContractError):
            freeze_access_policy_transition(
                VerifiedPrincipal(stable_account_id="99", login="creator"),
                current_campaign=_access_campaign(),
                proposed_campaign=_access_campaign(
                    revision=CHANGED_CAMPAIGN_REVISION,
                    join_policy="open_contributors",
                ),
                expected_campaign_revision=CAMPAIGN_REVISION,
                proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
                live_route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()),
            )

    def test_grant_revocation_is_prospective_for_existing_collaboration_requirement(
        self,
    ) -> None:
        repository, _obligation = self._open_pending()
        transition = _mechanical_grant_revocation_transition(repository)

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )

        self.assertEqual(reconciliation.obligations[0].lifecycle, "OPEN")
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        repository.put(
            "world.player",
            "player-bob",
            _thaw_for_test(transition.proposed_player),
        )
        repository.current_revision = CHANGED_CAMPAIGN_REVISION
        resolution = resolve_player(
            _bob_principal(),
            _route(),
            lambda candidate_id: repository.records[
                route_native_record("world.player", (candidate_id,)).relative_path
            ],
            campaign_id=CAMPAIGN_ID,
        )
        decision = authorize_operation(
            _bob_principal(),
            resolution,
            operation="mechanical_override_policy",
            campaign_id=CAMPAIGN_ID,
        )
        self.assertFalse(decision.authorized)
        self.assertFalse(
            repository.records[bob_path]["policy_authority"][
                "mechanical_override_policy"
            ]
        )

    def test_reconciliation_reads_only_route_bounded_obligation_ids(self) -> None:
        repository, obligation = self._open_pending()
        rogue = replace(obligation, obligation_id="obligation-not-routed")
        _persist_obligation(repository, rogue)
        repository.reads.clear()
        transition = _self_deactivation_transition(repository)

        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )

        expected_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        rogue_path = route_native_record(
            "runtime.collaboration_obligation", (rogue.obligation_id,)
        ).relative_path
        self.assertEqual(len(reconciliation.obligations), 1)
        self.assertIn(expected_path, repository.reads)
        self.assertNotIn(rogue_path, repository.reads)

    def test_terminal_generation_remains_known_id_recoverable_but_leaves_routes(
        self,
    ) -> None:
        repository, obligation = self._open_pending()
        transition = _self_deactivation_transition(repository)
        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        )
        obsolete = reconciliation.obligations[0]
        self.assertEqual(obsolete.lifecycle, "OBSOLETE")
        _persist_obligation(repository, obsolete)
        repository.put(
            "world.player",
            "player-bob",
            _thaw_for_test(transition.proposed_player),
        )
        for companion in collaboration_module.reconcile_player_route_companions(
            obsolete
        ):
            player_path = route_native_record(
                "world.player", (companion.player_id,)
            ).relative_path
            player = deepcopy(repository.records[player_path])
            player["collaboration_route_refs"] = [
                ref
                for ref in player.get("collaboration_route_refs", ())
                if (ref["obligation_id"], ref["generation"])
                != (obsolete.obligation_id, obsolete.generation)
            ]
            repository.put("world.player", companion.player_id, player)
        repository.current_revision = CHANGED_CAMPAIGN_REVISION
        host = _host(repository)

        recovered = collaboration_module.recover_obligation(
            host, obligation.obligation_id
        )
        self.assertEqual(recovered.lifecycle, "OBSOLETE")
        self.assertEqual(required_route_holders(recovered), ())
        repository.reads.clear()
        catch_up = join_participant(host, principal=_principal(), player_route=_route())
        self.assertEqual(catch_up.obligations, ())
        self.assertNotIn(
            route_native_record(
                "runtime.collaboration_obligation", (obligation.obligation_id,)
            ).relative_path,
            repository.reads,
        )

    def test_stale_access_transition_fails_closed_before_reconciliation(self) -> None:
        repository, _obligation = self._open_pending()
        transition = _self_deactivation_transition(repository)
        repository.current_revision = CHANGED_CAMPAIGN_REVISION

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )


class CollaborationAccessPublicationClosureTests(unittest.TestCase):
    def _open_reconciliation(
        self,
        *,
        transition_kind: str = "deactivate",
        obligation_count: int = 1,
        unrelated_obligation: bool = False,
    ) -> tuple[
        CampaignPublicationRepositoryFixture,
        CampaignPublicationTransport,
        CollaborationObligation,
        object,
        CollaborationAccessReconciliation,
    ]:
        repository = CampaignPublicationRepositoryFixture(_collective_clause())
        repository.records["MANIFEST.yaml"] = _campaign_manifest()
        admission = _classify(repository)
        obligations: list[CollaborationObligation] = []
        for index in range(obligation_count):
            obligation_id = (
                "obligation-access-closure"
                if index == 0
                else f"obligation-access-closure-{index + 1}"
            )
            obligation = open_or_successor_obligation(
                admission, obligation_id=obligation_id
            )
            assert obligation is not None
            _persist_obligation(repository, obligation)
            _attach_route_ref(repository, obligation, "player-alice", "player-bob")
            obligations.append(obligation)
        if unrelated_obligation:
            unrelated = replace(
                obligations[0],
                obligation_id="obligation-unaffected",
                required_contributors=(
                    ContributorRef(player_id="player-alice", pc_id="pc-alice"),
                ),
            )
            _persist_obligation(repository, unrelated)
            _attach_route_ref(repository, unrelated, "player-alice")
        repository.capture_current_revision()
        obligation = obligations[0]
        if transition_kind == "deactivate":
            transition = _self_deactivation_transition(repository)
            reconciliation = collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition, host=_host(repository)
            )
        elif transition_kind == "join-policy":
            transition = _join_policy_transition()
            reconciliation = collaboration_module.reconcile_collaboration_for_access_policy_transition(
                transition, host=_host(repository)
            )
        else:
            raise AssertionError(f"unknown test transition {transition_kind}")
        return (
            repository,
            CampaignPublicationTransport(repository),
            obligation,
            transition,
            reconciliation,
        )

    def _advance_deactivation_after_state(
        self,
        repository: CampaignPublicationRepositoryFixture,
        transport: CampaignPublicationTransport,
        *,
        obsolete_ids: tuple[str, ...] = (),
        cleanup_ids: tuple[str, ...] = (),
    ) -> None:
        """Publish a controlled post-W03 fixture, optionally only partly applied."""
        operations: dict[str, object | None] = {}
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        bob = deepcopy(repository.records[bob_path])
        bob["status"] = "inactive"
        bob["deactivated_by"] = "self"
        operations[bob_path] = bob
        for obligation_id in obsolete_ids:
            obligation_path = route_native_record(
                "runtime.collaboration_obligation", (obligation_id,)
            ).relative_path
            obligation = deepcopy(repository.records[obligation_path])
            obligation["lifecycle"] = "OBSOLETE"
            operations[obligation_path] = obligation
        for player_id in ("player-alice", "player-bob"):
            player_path = route_native_record(
                "world.player", (player_id,)
            ).relative_path
            player = deepcopy(
                operations.get(player_path, repository.records[player_path])
            )
            player["collaboration_route_refs"] = [
                ref
                for ref in player.get("collaboration_route_refs", ())
                if ref["obligation_id"] not in cleanup_ids
            ]
            operations[player_path] = player
        transport._pending_operations = operations
        transport.update_ref("campaign/frostfall", transport.next_head, force=False)

    def _live_reconciliation(
        self,
        *,
        source_count: int = 1,
        complete_forward: bool,
    ) -> tuple[
        CampaignPublicationRepositoryFixture,
        CampaignPublicationTransport,
        object,
        CollaborationAccessReconciliation,
        LiveRouting,
        LiveRouting,
        object,
        object,
    ]:
        repository, transport, _obligation, _old_transition, _old_reconciliation = (
            self._open_reconciliation()
        )
        sources = tuple(
            _live_source(f"scene-live-{index}") for index in range(source_count)
        )
        active_route = build_live_route(CAMPAIGN_ID, sources)
        repository.capture_current_revision()
        current_campaign = _access_campaign()
        proposed_source_revisions = {
            source.source_key: LIVE_CLOSED_REVISION for source in sources
        }
        plan = freeze_multi_live_forward_plan(
            active_route,
            current_campaign=current_campaign,
            expected_campaign_revision=repository.current_revision,
            proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
            proposed_source_revisions=proposed_source_revisions,
        )
        if complete_forward:
            progress = advance_multi_live_freeze(
                plan,
                acknowledgements={
                    attempt.source_key: _accepted_live_close_ack(attempt)
                    for attempt in plan.attempts
                },
            )
            forward = publish_forward_transition(
                plan,
                progress,
                current_campaign_revision=repository.current_revision,
                campaign_state=current_campaign,
            )
            proposed_campaign = deepcopy(dict(forward.campaign_state))
            proposed_campaign.pop("access_transition", None)
            proposed_campaign.pop("live_routing", None)
            proposed_route = forward.route
        else:
            acknowledgements: dict[object, object] = {}
            current_sources: dict[object, object] = {}
            if source_count > 1:
                acknowledgements[sources[0].source_key] = _accepted_live_close_ack(
                    plan.attempts[0]
                )
                acknowledgements[sources[1].source_key] = None
                current_sources[sources[1].source_key] = sources[1]
            progress = advance_multi_live_freeze(
                plan,
                acknowledgements=acknowledgements,
                current_sources=current_sources,
            )
            route_entries = {source.source_key: source for source in sources}
            route_entries.update(
                {source.source_key: source for source in progress.final_sources}
            )
            proposed_route = build_live_route(
                CAMPAIGN_ID, tuple(route_entries.values())
            )
            proposed_campaign = current_campaign | {
                "revision": CHANGED_CAMPAIGN_REVISION,
            }

        player_path = route_native_record("world.player", ("player-bob",)).relative_path
        current_player = deepcopy(repository.records[player_path])
        proposed_player = deepcopy(current_player)
        proposed_player["status"] = "inactive"
        proposed_player["deactivated_by"] = "self"
        principal = _bob_principal()
        resolution = resolve_player(
            principal,
            _route(),
            lambda candidate_id: repository.records[
                route_native_record("world.player", (candidate_id,)).relative_path
            ],
            campaign_id=CAMPAIGN_ID,
        )
        transition = freeze_player_access_transition(
            principal,
            resolution,
            operation="deactivate_self",
            current_player=current_player,
            proposed_player=proposed_player,
            current_campaign=current_campaign,
            proposed_campaign=proposed_campaign,
            expected_campaign_revision=repository.current_revision,
            proposed_campaign_revision=CHANGED_CAMPAIGN_REVISION,
            current_live_route=active_route,
            proposed_live_route=proposed_route,
        )
        reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                transition,
                host=_host(repository, live=LiveFixture(active_route)),
            )
        )
        return (
            repository,
            transport,
            transition,
            reconciliation,
            active_route,
            proposed_route,
            plan,
            progress,
        )

    def _publish_live_closure_for_cold_recovery(self):
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            predecessor_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        delta = _live_absorption_delta(
            predecessor_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=predecessor_route,
            final_route=delta.final_route,
            source_packs=_live_delta_packs(delta),
        )
        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=delta,
        )
        if published.composed_absorption is None:
            raise AssertionError("LIVE publication did not retain composed evidence")
        return (
            repository,
            transport,
            transition,
            predecessor_route,
            delta,
            live,
            published,
        )

    def test_live_w03_delta_is_joined_once_and_bound_to_actual_w02_revision(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
            source_packs=_live_delta_packs(absorption_delta),
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        composed = published.composed_absorption
        self.assertIsNotNone(composed)
        assert composed is not None
        self.assertEqual(composed.status.value, "ACCEPTED")
        self.assertEqual(composed.delta.proposed_campaign_revision, transport.next_head)
        self.assertEqual(
            dict(composed.delta.path_operations), dict(absorption_delta.path_operations)
        )
        self.assertEqual(
            dict(composed.delta.operation_digests),
            dict(absorption_delta.operation_digests),
        )
        for attempt in composed.delta.source_attempts:
            self.assertIs(
                live_state_module.validate_accepted_absorption_evidence(
                    composed,
                    source_key=attempt.source_key,
                    source_revision=attempt.source_revision,
                    selected_route=composed.delta.selected_route,
                ),
                composed,
            )

        operations = next(
            payload for name, payload in transport.calls if name == "create_tree"
        )
        self.assertIsInstance(operations, Mapping)
        self.assertEqual(
            {name for name, _payload in transport.calls}.intersection(
                {"create_tree", "create_commit", "update_ref"}
            ),
            {"create_tree", "create_commit", "update_ref"},
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "create_tree"]),
            1,
        )
        self.assertEqual(
            len(
                [name for name, _payload in transport.calls if name == "create_commit"]
            ),
            1,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )
        for path, payload in absorption_delta.path_operations.items():
            self.assertEqual(operations[path], payload)
        self.assertIn(
            route_native_record("world.player", ("player-bob",)).relative_path,
            operations,
        )
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation",
                (reconciliation.obligations[0].obligation_id,),
            ).relative_path,
            operations,
        )
        self.assertEqual(
            repository.records["STATE/RUNTIME/LIVE_ROUTING.yaml"],
            absorption_delta.final_route.as_mapping(),
        )
        duplicate = collaboration_module.publish_collaboration_access_reconciliation(
            published,
            host=_host(
                repository,
                transport,
                LiveFixture(absorption_delta.final_route),
            ),
        )
        self.assertEqual(duplicate, published)
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )

    def test_live_event_index_snapshot_is_reused_for_actual_revision_binding(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        previous_event_id = "campaign-event-before-live"
        previous_event_path = route_native_record(
            "runtime.semantic_event", (previous_event_id,)
        ).relative_path
        event_index: dict[str, object] = {
            "schema_version": 1,
            "entity_type": "EVENT",
            "complete": True,
            "upper_ordinal": 1,
            "entries": [
                {
                    "ordinal": 1,
                    "event_id": previous_event_id,
                    "path": previous_event_path,
                }
            ],
        }
        repository.records["INDEX/EVENT_INDEX.yaml"] = event_index
        repository.capture_current_revision()
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
            event_index=event_index,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
            source_packs=_live_delta_packs(absorption_delta),
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        assert published.composed_absorption is not None
        rebound = published.composed_absorption.delta
        self.assertEqual(rebound.proposed_campaign_revision, transport.next_head)
        self.assertEqual(
            dict(rebound.operation_digests), dict(absorption_delta.operation_digests)
        )
        event_id = "live-event-scene-live-0"
        event_path = route_native_record(
            "runtime.semantic_event", (event_id,)
        ).relative_path
        operations = next(
            payload for name, payload in transport.calls if name == "create_tree"
        )
        self.assertEqual(operations[event_path]["event_id"], event_id)
        self.assertEqual(operations["INDEX/EVENT_INDEX.yaml"]["upper_ordinal"], 2)
        cold = replace(
            published,
            transition=replace(published.transition),
            composed_absorption=None,
        )
        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            cold, host=_host(repository, transport, live)
        )
        self.assertIsNotNone(recovered.composed_absorption)
        assert recovered.composed_absorption is not None
        self.assertEqual(
            recovered.composed_absorption.delta.path_operations[
                "INDEX/EVENT_INDEX.yaml"
            ]["upper_ordinal"],
            2,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )

    def test_live_operational_root_snapshot_is_reused_for_actual_revision_binding(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        retained_root = OperationalRoot(
            CAMPAIGN_ID,
            "runtime.command",
            "command-unaffected",
            route_native_record(
                "runtime.command", ("command-unaffected",)
            ).relative_path,
        )
        root_page: dict[str, object] = {
            "schema_version": 1,
            "campaign_id": CAMPAIGN_ID,
            "complete": True,
            "roots": [retained_root.to_dict()],
        }
        root_path = "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"
        repository.records[root_path] = root_page
        repository.capture_current_revision()
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
            operational_roots=root_page,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
            source_packs=_live_delta_packs(absorption_delta),
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        assert published.composed_absorption is not None
        self.assertEqual(
            published.composed_absorption.delta.proposed_campaign_revision,
            transport.next_head,
        )
        self.assertEqual(
            dict(published.composed_absorption.delta.operation_digests),
            dict(absorption_delta.operation_digests),
        )
        expected_roots = tuple(
            sorted(
                (
                    retained_root.to_dict(),
                    OperationalRoot(
                        CAMPAIGN_ID,
                        "runtime.procedure",
                        "procedure-live-absorption",
                        route_native_record(
                            "runtime.procedure",
                            ("procedure-live-absorption",),
                        ).relative_path,
                    ).to_dict(),
                ),
                key=lambda item: (item["owner_kind"], item["owner_id"]),
            )
        )
        self.assertEqual(repository.records[root_path]["roots"], list(expected_roots))
        cold = replace(
            published,
            transition=replace(published.transition),
            composed_absorption=None,
        )
        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            cold, host=_host(repository, transport, live)
        )
        self.assertIsNotNone(recovered.composed_absorption)
        assert recovered.composed_absorption is not None
        self.assertEqual(
            _thaw_for_test(
                recovered.composed_absorption.delta.path_operations[root_path]["roots"]
            ),
            list(expected_roots),
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )

    def test_live_transition_without_owner_issued_p1_delta_fails_before_w02(
        self,
    ) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "create_tree"], []
        )
        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"], []
        )
        self.assertEqual(transport.calls, [])

    def test_non_owner_p1_delta_is_rejected_before_w02_dispatch(self) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        issued_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        reconstructed_delta = live_state_module.FrozenCampaignAbsorptionDelta(
            campaign_id=issued_delta.campaign_id,
            expected_campaign_revision=issued_delta.expected_campaign_revision,
            proposed_campaign_revision=issued_delta.proposed_campaign_revision,
            selected_route=issued_delta.selected_route,
            final_route=issued_delta.final_route,
            source_attempts=issued_delta.source_attempts,
            path_operations=_thaw_for_test(issued_delta.path_operations),
            operation_digests=dict(issued_delta.operation_digests),
            delta_digest=issued_delta.delta_digest,
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
                absorption_delta=reconstructed_delta,
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "create_tree"], []
        )
        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"], []
        )
        self.assertEqual(transport.calls, [])

    def test_tampered_owner_p1_delta_is_rejected_before_w02_dispatch(self) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        tampered_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        object.__setattr__(tampered_delta, "delta_digest", "0" * 64)

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
                absorption_delta=tampered_delta,
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "create_tree"], []
        )
        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"], []
        )
        self.assertEqual(transport.calls, [])

    def test_closed_unabsorbed_only_state_is_not_live_absorption_recovery(
        self,
    ) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active_route,
            closed_route,
            _plan,
            _progress,
        ) = self._live_reconciliation(complete_forward=True)
        self._advance_deactivation_after_state(
            repository,
            transport,
            obsolete_ids=tuple(
                obligation.obligation_id for obligation in reconciliation.obligations
            ),
            cleanup_ids=tuple(
                obligation.obligation_id for obligation in reconciliation.obligations
            ),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"],
            ["update_ref"],
        )

    def test_indeterminate_w02_acknowledgement_uses_same_closure_without_second_write(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        transport.response_status = "indeterminate"
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        assert published.composed_absorption is not None
        self.assertEqual(
            published.composed_absorption.delta.proposed_campaign_revision,
            transport.next_head,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "read_ref"]),
            2,
        )
        self.assertEqual(
            repository.records["STATE/RUNTIME/LIVE_ROUTING.yaml"],
            published.composed_absorption.delta.final_route.as_mapping(),
        )

    def test_ancestor_w02_reconciliation_binds_p1_to_intended_not_observed_head(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        transport.response_status = "indeterminate"
        transport.reconciliation_head = "9" * 40
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        assert published.composed_absorption is not None
        self.assertEqual(
            published.composed_absorption.delta.proposed_campaign_revision,
            transport.next_head,
        )
        self.assertEqual(
            published.composed_absorption.accepted_campaign_revision,
            transport.reconciliation_head,
        )
        self.assertNotEqual(
            published.composed_absorption.delta.proposed_campaign_revision,
            published.composed_absorption.accepted_campaign_revision,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )

    def test_w02_conflict_never_becomes_p1_accepted_absorption(self) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        transport.ref_revision_override = "f" * 40
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
                absorption_delta=absorption_delta,
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"], []
        )
        self.assertEqual(
            [name for name, _payload in transport.calls if name == "create_commit"],
            [],
        )

    def test_conflict_retry_rebases_same_final_live_sources_without_reclosing(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        original_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        transport.ref_revision_override = "f" * 40

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(closed_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
                absorption_delta=original_delta,
            )

        self.assertEqual(
            [name for name, _payload in transport.calls if name == "create_commit"],
            [],
        )
        self.assertEqual(
            [name for name, _payload in transport.calls if name == "update_ref"], []
        )

        unrelated_path = route_native_record(
            "world.scene", ("scene-unrelated",)
        ).relative_path
        external_revision = "e" * 40
        transport.ref_revision_override = None
        transport.next_head = external_revision
        transport._pending_operations = {
            unrelated_path: {
                "schema_version": 1,
                "kind": "world.scene",
                "id": "scene-unrelated",
                "state": {"marker": "disjoint"},
            }
        }
        transport.update_ref("campaign/frostfall", external_revision, force=False)
        transport.calls.clear()
        retry_proposed_revision = "9" * 40
        current_campaign = _access_campaign(revision=external_revision)
        retry_plan = freeze_multi_live_forward_plan(
            closed_route,
            current_campaign=current_campaign,
            expected_campaign_revision=external_revision,
            proposed_campaign_revision=retry_proposed_revision,
            proposed_source_revisions={
                source.source_key: source.source_revision
                for source in closed_route.entries
            },
        )
        retry_progress = advance_multi_live_freeze(retry_plan)
        forward = publish_forward_transition(
            retry_plan,
            retry_progress,
            current_campaign_revision=external_revision,
            campaign_state=current_campaign,
        )
        proposed_campaign = deepcopy(dict(forward.campaign_state))
        proposed_campaign.pop("access_transition", None)
        proposed_campaign.pop("live_routing", None)
        player_path = route_native_record("world.player", ("player-bob",)).relative_path
        current_player = deepcopy(repository.records[player_path])
        proposed_player = deepcopy(current_player)
        proposed_player["status"] = "inactive"
        proposed_player["deactivated_by"] = "self"
        principal = _bob_principal()
        resolution = resolve_player(
            principal,
            _route(),
            lambda player_id: repository.records[
                route_native_record("world.player", (player_id,)).relative_path
            ],
            campaign_id=CAMPAIGN_ID,
        )
        retry_transition = freeze_player_access_transition(
            principal,
            resolution,
            operation="deactivate_self",
            current_player=current_player,
            proposed_player=proposed_player,
            current_campaign=current_campaign,
            proposed_campaign=proposed_campaign,
            expected_campaign_revision=external_revision,
            proposed_campaign_revision=retry_proposed_revision,
            current_live_route=closed_route,
            proposed_live_route=forward.route,
        )
        retry_reconciliation = (
            collaboration_module.reconcile_collaboration_for_player_access_transition(
                retry_transition,
                host=_host(repository, transport, LiveFixture(closed_route)),
            )
        )
        retry_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=external_revision,
            proposed_campaign_revision=retry_proposed_revision,
        )
        transport.next_head = "a" * 40
        published = collaboration_module.publish_collaboration_access_reconciliation(
            retry_reconciliation,
            host=_host(
                repository,
                transport,
                TransitioningLiveFixture(
                    predecessor_revision=external_revision,
                    predecessor_route=closed_route,
                    final_route=retry_delta.final_route,
                ),
            ),
            live_forward_plan=retry_plan,
            live_freeze_progress=retry_progress,
            absorption_delta=retry_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        assert published.composed_absorption is not None
        self.assertEqual(
            tuple(
                (attempt.source_key, attempt.source_revision)
                for attempt in published.composed_absorption.delta.source_attempts
            ),
            tuple(
                (attempt.source_key, attempt.source_revision)
                for attempt in original_delta.source_attempts
            ),
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )

    def test_live_process_loss_rederives_p1_and_revalidates_exact_final_route(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        live = TransitioningLiveFixture(
            predecessor_revision=transition.expected_campaign_revision,
            predecessor_route=closed_route,
            final_route=absorption_delta.final_route,
            source_packs=_live_delta_packs(absorption_delta),
        )
        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(repository, transport, live),
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertIsNotNone(published.composed_absorption)
        cold_reconciliation = replace(
            published,
            transition=replace(published.transition),
            composed_absorption=None,
        )
        recovered_after_process_loss = (
            collaboration_module.recover_collaboration_access_reconciliation(
                cold_reconciliation,
                host=_host(repository, transport, live),
            )
        )
        self.assertIsNotNone(recovered_after_process_loss.composed_absorption)
        assert recovered_after_process_loss.composed_absorption is not None
        self.assertEqual(
            recovered_after_process_loss.composed_absorption.delta,
            published.composed_absorption.delta,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "create_tree"]),
            1,
        )
        self.assertEqual(
            len(
                [name for name, _payload in transport.calls if name == "create_commit"]
            ),
            1,
        )
        self.assertEqual(
            set(live.source_pack_reads),
            set(transition.impact.live_source_keys),
        )
        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                published,
                host=_host(repository, transport, LiveFixture(closed_route)),
            )
        assert published.composed_absorption is not None
        reconstructed_composed = replace(published.composed_absorption)
        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                replace(published, composed_absorption=reconstructed_composed),
                host=_host(
                    repository,
                    transport,
                    LiveFixture(absorption_delta.final_route),
                ),
            )
        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            published,
            host=_host(
                repository,
                transport,
                LiveFixture(absorption_delta.final_route),
            ),
        )

        self.assertEqual(recovered, published)
        self.assertEqual(
            len([name for name, _payload in transport.calls if name == "update_ref"]),
            1,
        )
        actor_path = route_native_record(
            "world.actor", ("actor-scene-live-0",)
        ).relative_path
        actor_after = deepcopy(repository.records[actor_path])
        actor_after["state"]["concept"] = "tampered"  # type: ignore[index]
        repository.records[actor_path] = actor_after
        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                published,
                host=_host(
                    repository,
                    transport,
                    LiveFixture(absorption_delta.final_route),
                ),
            )

    def test_cold_p1_revalidation_accepts_compatible_disjoint_descendant(self) -> None:
        (
            repository,
            transport,
            _transition,
            _predecessor_route,
            delta,
            live,
            published,
        ) = self._publish_live_closure_for_cold_recovery()
        intended = published.transition.proposed_campaign_revision
        descendant = "9" * 40
        repository.current_revision = descendant
        repository.current_tree = "f" * 40
        repository.records["STATE/RUNTIME/P0R_DISJOINT.yaml"] = {
            "kind": "runtime.p0r_disjoint",
            "revision": 1,
        }
        repository.capture_current_revision(parent_revision=intended)
        transport.calls.clear()
        cold_reconciliation = replace(
            published,
            transition=replace(published.transition),
            composed_absorption=None,
        )

        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            cold_reconciliation,
            host=_host(repository, transport, live),
        )

        self.assertIsNotNone(recovered.composed_absorption)
        assert recovered.composed_absorption is not None
        self.assertEqual(recovered.composed_absorption.status.value, "ACCEPTED")
        self.assertEqual(
            recovered.composed_absorption.accepted_campaign_revision, descendant
        )
        self.assertEqual(
            dict(recovered.composed_absorption.delta.path_operations),
            dict(delta.path_operations),
        )
        writes = [
            name
            for name, _payload in transport.calls
            if name in {"create_tree", "create_commit", "update_ref"}
        ]
        self.assertEqual(writes, [])
        self.assertEqual(
            set(live.source_pack_reads),
            {attempt.source_key for attempt in delta.source_attempts},
        )

    def test_cold_p1_revalidation_rejects_overlapping_descendant_without_writes(
        self,
    ) -> None:
        (
            repository,
            transport,
            _transition,
            _predecessor_route,
            delta,
            live,
            published,
        ) = self._publish_live_closure_for_cold_recovery()
        intended = published.transition.proposed_campaign_revision
        descendant = "9" * 40
        overlapping_path = next(iter(delta.path_operations))
        repository.current_revision = descendant
        repository.current_tree = "f" * 40
        repository.records[overlapping_path] = {
            "kind": "runtime.p0r_overlap",
            "revision": 2,
        }
        repository.capture_current_revision(parent_revision=intended)
        transport.calls.clear()
        cold_reconciliation = replace(
            published,
            transition=replace(published.transition),
            composed_absorption=None,
        )

        with self.assertRaisesRegex(
            CollaborationAdmissionError, "W02 did not revalidate"
        ):
            collaboration_module.recover_collaboration_access_reconciliation(
                cold_reconciliation,
                host=_host(repository, transport, live),
            )

        writes = [
            name
            for name, _payload in transport.calls
            if name in {"create_tree", "create_commit", "update_ref"}
        ]
        self.assertEqual(writes, [])

    def test_owner_operation_collision_fails_closed(self) -> None:
        with self.assertRaisesRegex(CollaborationAdmissionError, "collision"):
            collaboration_module._join_campaign_path_operations(
                {"same/path.yaml": {"owner": "W03"}},
                {"same/path.yaml": {"owner": "access"}},
            )

    def test_live_path_collision_fails_before_w02_dispatch(self) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        collision_path = next(iter(absorption_delta.path_operations))

        with (
            mock.patch.object(
                collaboration_module,
                "_build_access_reconciliation_operations",
                return_value=(
                    {collision_path: {"owner": "access/Collaboration"}},
                    None,
                    {},
                ),
            ),
            self.assertRaisesRegex(CollaborationAdmissionError, "collision"),
        ):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(
                    repository,
                    transport,
                    TransitioningLiveFixture(
                        predecessor_revision=transition.expected_campaign_revision,
                        predecessor_route=closed_route,
                        final_route=absorption_delta.final_route,
                    ),
                ),
                live_forward_plan=plan,
                live_freeze_progress=progress,
                absorption_delta=absorption_delta,
            )

        self.assertEqual(transport.calls, [])

    def test_access_and_obsolete_obligation_publish_in_one_campaign_closure(
        self,
    ) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        host = _host(repository, transport)

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )

        update_ref_calls = [
            payload for name, payload in transport.calls if name == "update_ref"
        ]
        self.assertEqual(len(update_ref_calls), 1)
        self.assertFalse(update_ref_calls[0][2])
        self.assertEqual(repository.current_revision, transport.next_head)
        bob_path = route_native_record("world.player", ("player-bob",)).relative_path
        alice_path = route_native_record(
            "world.player", ("player-alice",)
        ).relative_path
        obligation_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        self.assertEqual(repository.records[bob_path]["status"], "inactive")
        self.assertEqual(repository.records[bob_path]["collaboration_route_refs"], [])
        self.assertEqual(repository.records[alice_path]["collaboration_route_refs"], [])
        self.assertEqual(repository.records[obligation_path]["lifecycle"], "OBSOLETE")
        self.assertEqual(published.obligations[0].lifecycle, "OBSOLETE")
        self.assertIsNone(published.composed_absorption)
        self.assertEqual(
            published.after_authority_view["campaign"]["revision"],
            repository.current_revision,
        )

    def test_campaign_access_policy_and_collaboration_close_together(self) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation(transition_kind="join-policy")
        )
        host = _host(repository, transport)

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )

        manifest = repository.records["MANIFEST.yaml"]
        obligation_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        self.assertEqual(manifest["players"]["join_policy"], "open_contributors")
        self.assertEqual(repository.records[obligation_path]["lifecycle"], "OPEN")
        self.assertEqual(published.obligations[0].lifecycle, "OPEN")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_duplicate_publish_and_after_commit_recovery_do_not_dispatch_again(
        self,
    ) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        host = _host(repository, transport)
        first = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )
        writes_after_first = len(
            [name for name, _ in transport.calls if name == "update_ref"]
        )

        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            reconciliation, host=host
        )
        retried = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )

        self.assertEqual(recovered, first)
        self.assertEqual(retried, first)
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]),
            writes_after_first,
        )

    def test_recovery_before_publication_fails_without_mutation(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        before = deepcopy(repository.records)

        with self.assertRaisesRegex(
            CollaborationAdmissionError, "not.*published|predecessor"
        ):
            collaboration_module.recover_collaboration_access_reconciliation(
                reconciliation, host=_host(repository, transport)
            )

        self.assertEqual(repository.records, before)
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_recovery_and_advanced_publish_reject_empty_effect_set(self) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        self._advance_deactivation_after_state(repository, transport)
        empty = replace(
            reconciliation,
            affected_obligation_ids=(),
            obligations=(),
        )
        host = _host(repository, transport)

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                empty, host=host
            )
        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                empty, host=host
            )

        obligation_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        self.assertEqual(repository.records[obligation_path]["lifecycle"], "OPEN")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_empty_carrier_does_not_hide_effects_in_a_complete_published_closure(
        self,
    ) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        host = _host(repository, transport)
        collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )
        empty = replace(
            reconciliation,
            affected_obligation_ids=(),
            obligations=(),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                empty, host=_host(repository, transport)
            )
        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                empty, host=_host(repository, transport)
            )

        obligation_path = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        ).relative_path
        self.assertEqual(repository.records[obligation_path]["lifecycle"], "OBSOLETE")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_subset_carrier_cannot_hide_a_second_affected_obligation(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation(obligation_count=2)
        )
        first_id = reconciliation.affected_obligation_ids[0]
        self._advance_deactivation_after_state(
            repository,
            transport,
            obsolete_ids=(first_id[0],),
            cleanup_ids=(first_id[0],),
        )
        subset = replace(
            reconciliation,
            affected_obligation_ids=(first_id,),
            obligations=tuple(
                item
                for item in reconciliation.obligations
                if (item.obligation_id, item.generation) == first_id
            ),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                subset, host=_host(repository, transport)
            )

        second_id = reconciliation.affected_obligation_ids[1][0]
        second_path = route_native_record(
            "runtime.collaboration_obligation", (second_id,)
        ).relative_path
        self.assertEqual(repository.records[second_path]["lifecycle"], "OPEN")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_extra_effect_identity_is_rejected_after_publication(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation(unrelated_obligation=True)
        )
        collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=_host(repository, transport)
        )
        unrelated_path = route_native_record(
            "runtime.collaboration_obligation", ("obligation-unaffected",)
        ).relative_path
        extra_obligation = CollaborationObligation.from_mapping(
            repository.records[unrelated_path], host=_host(repository, transport)
        )
        extra_ids = tuple(
            sorted(
                (
                    *reconciliation.affected_obligation_ids,
                    (extra_obligation.obligation_id, extra_obligation.generation),
                )
            )
        )
        extra_effects = replace(
            reconciliation,
            affected_obligation_ids=extra_ids,
            obligations=tuple(
                sorted(
                    (*reconciliation.obligations, extra_obligation),
                    key=lambda item: (item.obligation_id, item.generation),
                )
            ),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                extra_effects, host=_host(repository, transport)
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_recovery_rejects_partially_applied_complete_effect_set(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation(obligation_count=2)
        )
        first_id = reconciliation.affected_obligation_ids[0][0]
        self._advance_deactivation_after_state(
            repository,
            transport,
            obsolete_ids=(first_id,),
            cleanup_ids=(first_id,),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                reconciliation, host=_host(repository, transport)
            )

        second_id = reconciliation.affected_obligation_ids[1][0]
        second_path = route_native_record(
            "runtime.collaboration_obligation", (second_id,)
        ).relative_path
        self.assertEqual(repository.records[second_path]["lifecycle"], "OPEN")

    def test_active_affected_live_source_blocks_campaign_write(self) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            active_route,
            _proposed,
            _plan,
            _progress,
        ) = self._live_reconciliation(complete_forward=False)

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(active_route)),
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_partial_indeterminate_multi_live_close_blocks_campaign_write(self) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active_route,
            partial_route,
            _plan,
            progress,
        ) = self._live_reconciliation(source_count=2, complete_forward=False)
        self.assertEqual(progress.status, "INDETERMINATE")
        self.assertEqual(
            sum(
                source.status is LiveLifecycle.CLOSED_UNABSORBED
                for source in partial_route.entries
            ),
            1,
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(partial_route)),
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_stale_closed_live_revision_does_not_match_w03_forward_proof(self) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        stale_source = replace(closed_route.entries[0], source_revision="9" * 40)
        stale_route = build_live_route(CAMPAIGN_ID, (stale_source,))

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(stale_route)),
                live_forward_plan=plan,
                live_freeze_progress=progress,
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_recovery_rejects_partially_closed_w03_live_boundary(self) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active_route,
            partial_route,
            _plan,
            progress,
        ) = self._live_reconciliation(source_count=2, complete_forward=False)
        self.assertEqual(progress.status, "INDETERMINATE")
        obligation_id = reconciliation.affected_obligation_ids[0][0]
        self._advance_deactivation_after_state(
            repository,
            transport,
            obsolete_ids=(obligation_id,),
            cleanup_ids=(obligation_id,),
        )

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture(partial_route)),
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )

    def test_completed_w03_forward_closure_joins_access_publication_and_recovers(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            active_route,
            closed_route,
            plan,
            progress,
        ) = self._live_reconciliation(complete_forward=True)
        self.assertEqual(progress.status, "READY_TO_PUBLISH")
        self.assertTrue(
            all(
                source.status is LiveLifecycle.CLOSED_UNABSORBED
                for source in closed_route.entries
            )
        )

        absorption_delta = _live_absorption_delta(
            closed_route,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )
        host = _host(
            repository,
            transport,
            TransitioningLiveFixture(
                predecessor_revision=transition.expected_campaign_revision,
                predecessor_route=closed_route,
                final_route=absorption_delta.final_route,
            ),
        )
        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=host,
            live_forward_plan=plan,
            live_freeze_progress=progress,
            absorption_delta=absorption_delta,
        )

        self.assertNotEqual(active_route.as_mapping(), closed_route.as_mapping())
        self.assertNotIn("live_routing", repository.records["MANIFEST.yaml"])
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )
        operations = next(
            payload for name, payload in transport.calls if name == "create_tree"
        )
        self.assertNotIn("MANIFEST.yaml", operations)
        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            published,
            host=_host(
                repository, transport, LiveFixture(absorption_delta.final_route)
            ),
        )
        self.assertEqual(recovered, published)

    def test_closed_live_route_reestablishes_bounded_w03_forward_proof(
        self,
    ) -> None:
        (
            repository,
            transport,
            transition,
            reconciliation,
            _active,
            closed,
            _plan,
            _progress,
        ) = self._live_reconciliation(complete_forward=True)
        absorption_delta = _live_absorption_delta(
            closed,
            expected_campaign_revision=transition.expected_campaign_revision,
            proposed_campaign_revision=transition.proposed_campaign_revision,
        )

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation,
            host=_host(
                repository,
                transport,
                TransitioningLiveFixture(
                    predecessor_revision=transition.expected_campaign_revision,
                    predecessor_route=closed,
                    final_route=absorption_delta.final_route,
                ),
            ),
            absorption_delta=absorption_delta,
        )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )
        self.assertEqual(published.obligations[0].lifecycle, "OBSOLETE")

    def test_missing_selected_live_route_blocks_required_forward_boundary(self) -> None:
        (
            repository,
            transport,
            _transition,
            reconciliation,
            _active,
            _closed,
            _plan,
            _progress,
        ) = self._live_reconciliation(complete_forward=True)

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation,
                host=_host(repository, transport, LiveFixture()),
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_body_drift_after_prepare_stops_before_w02_dispatch(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        repository.records["MANIFEST.yaml"]["campaign_name"] = "Drifted"

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation, host=_host(repository, transport)
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_recovery_rejects_after_authority_manifest_body_drift(self) -> None:
        repository, transport, _obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        host = _host(repository, transport)
        collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )
        repository.records["MANIFEST.yaml"]["campaign_name"] = "Drifted after commit"

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.recover_collaboration_access_reconciliation(
                reconciliation, host=host
            )

    def test_stale_obligation_generation_stops_before_w02_dispatch(self) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        successor = replace(obligation, generation=2, predecessor_generation=1)
        _persist_obligation(repository, successor)
        _attach_route_ref(repository, successor, "player-alice", "player-bob")

        with self.assertRaises(CollaborationAdmissionError):
            collaboration_module.publish_collaboration_access_reconciliation(
                reconciliation, host=_host(repository, transport)
            )

        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 0
        )

    def test_indeterminate_ack_reconciles_same_closure_without_second_write(
        self,
    ) -> None:
        repository, transport, obligation, _transition, reconciliation = (
            self._open_reconciliation()
        )
        transport.response_status = "indeterminate"
        host = _host(repository, transport)

        published = collaboration_module.publish_collaboration_access_reconciliation(
            reconciliation, host=host
        )

        self.assertEqual(published.obligations[0].lifecycle, "OBSOLETE")
        self.assertEqual(
            len([name for name, _ in transport.calls if name == "update_ref"]), 1
        )
        recovered = collaboration_module.recover_collaboration_access_reconciliation(
            reconciliation, host=host
        )
        self.assertEqual(recovered, published)
        self.assertEqual(
            repository.records[
                route_native_record(
                    "runtime.collaboration_obligation", (obligation.obligation_id,)
                ).relative_path
            ]["lifecycle"],
            "OBSOLETE",
        )


if __name__ == "__main__":
    unittest.main()
