"""Production-path witnesses for the bounded W05.T06-P0 Actor producer."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Callable
from copy import deepcopy
from typing import Any

import pytest

from GAME.TOOLS import context_runtime, turn_runtime
from GAME.TOOLS.bootstrap import CampaignSelection, compose_selected_runtime_host
from GAME.TOOLS.current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    CurrentOwnerSource,
    NativeOwnerRef,
)
from GAME.TOOLS.hot_store import NativeHotStore, OwnerDocument
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
    build_live_ref,
    derive_live_epoch_id,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign

CAMPAIGN_ID = "campaign-frostfall"
CAMPAIGN_REVISION = "a" * 40
ACTOR_ID = "actor.mara"
PLAYER_ID = "player.lina"
_DEFAULT_DELTA = object()


def _actor(
    *,
    state_revision: int | None = 4,
    cue: dict[str, object] | None = None,
    cues: list[dict[str, object]] | None = None,
    roles: list[str] | None = None,
) -> dict[str, object]:
    record: dict[str, object] = {
        "schema_version": 2,
        "id": ACTOR_ID,
        "kind": "world.actor",
        "definition_id": "definition.npc_villager",
        "state": {
            "roles": ["actor.nonplayer_character"] if roles is None else roles,
            "continuity": {
                "evolving": {
                    "current_objective": {"statement": "Protect the spring"},
                    "reconsideration_cues": (
                        cues
                        if cues is not None
                        else [
                            {"statement": "The spring is already poisoned"}
                            if cue is None
                            else cue
                        ]
                    ),
                }
            },
        },
    }
    if state_revision is not None:
        record["state_revision"] = state_revision
    return record


def _delta(
    actor: dict[str, object], *, source_refs: list[str] | None = None
) -> dict[str, object]:
    return {
        "actor_id": actor["id"],
        "expected_state_revision": actor.get("state_revision"),
        "purpose": "assessment.reconsider",
        "source_refs": [actor["id"]] if source_refs is None else source_refs,
        "changes": {
            "continuity": {
                "evolving": {"next_intention": {"statement": "Warn the miller"}}
            }
        },
    }


def _phase_proposal(
    actor: dict[str, object],
    *,
    delta: object = _DEFAULT_DELTA,
    cue: dict[str, object] | None = None,
    extra: dict[str, object] | None = None,
) -> str:
    evolving = actor["state"]["continuity"]["evolving"]
    exact_cue = evolving["reconsideration_cues"][0] if cue is None else cue
    proposal: dict[str, object] = {
        "assessment_purpose": "assessment.reconsider",
        "reconsideration_cue": exact_cue,
        "delta": _delta(actor) if delta is _DEFAULT_DELTA else delta,
    }
    if extra:
        proposal.update(extra)
    return json.dumps(proposal, sort_keys=True, separators=(",", ":"))


class ActorRepository:
    def __init__(self, actor: dict[str, object] | None = None) -> None:
        self.actor = _actor() if actor is None else deepcopy(actor)
        self.revision = CAMPAIGN_REVISION
        self.pin_count = 0
        self.path_reads: list[tuple[str, str]] = []
        self.revision_records: dict[str, dict[str, object]] = {}
        self.read_hook: Callable[[PinnedCampaign, str], None] | None = None
        self.scene: dict[str, object] | None = None

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        self.pin_count += 1
        return PinnedCampaign(
            campaign_id=campaign_id,
            revision=self.revision,
            tree_sha="b" * 40,
        )

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        self.path_reads.append((pinned.revision, path))
        if self.read_hook is not None:
            self.read_hook(pinned, path)
        if pinned.revision in self.revision_records:
            try:
                return deepcopy(self.revision_records[pinned.revision][path])
            except KeyError as exc:
                raise KeyError(path) from exc
        if path == route_native_record("world.actor", (ACTOR_ID,)).relative_path:
            return deepcopy(self.actor)
        if path == route_native_record("world.scene", ("scene.spring",)).relative_path:
            if self.scene is None:
                raise KeyError(path)
            return deepcopy(self.scene)
        raise KeyError(path)

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        return {}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        return {}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        return {}


class SelectedLive:
    def __init__(
        self,
        route: LiveRouting | None = None,
        *,
        pack: LiveNativeStatePack | None = None,
    ) -> None:
        self.route = route or LiveRouting(campaign_id=CAMPAIGN_ID, entries=())
        self.pack = pack
        self.source_reads = 0
        self.route_pin_reads: list[str] = []

    def read_selected_live(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> LiveRouting:
        self.route_pin_reads.append(pinned_campaign.revision)
        return self.route

    def read_selected_live_source(
        self, routing: LiveRouting, source: LiveEnvelope
    ) -> LiveNativeStatePack:
        self.source_reads += 1
        if self.pack is None:
            raise KeyError(source.source_key)
        return self.pack


class PublicationTransport:
    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def resolve_authenticated_acting_principal(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> AuthenticatedPrincipalEvidence:
        return AuthenticatedPrincipalEvidence("principal.lina")

    def read_ref(self, target_ref: str) -> object:
        return {"head_sha": CAMPAIGN_REVISION}

    def create_tree(self, base_tree_sha: str, path_operations: object) -> object:
        return {}

    def create_commit(self, parent_sha: str, tree_sha: str, target_ref: str) -> object:
        return {}

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        return {}


def _selected_host(
    store: NativeHotStore,
    *,
    repository: ActorRepository | None = None,
    live: SelectedLive | None = None,
):
    source = repository or ActorRepository()
    host = compose_selected_runtime_host(
        CampaignSelection.existing(CAMPAIGN_ID),
        source,
        live or SelectedLive(),
        PublicationTransport(),
        hot_owner_store=store,
    )
    return host, source


def _actor_phase(
    host: object,
    actor: dict[str, object],
    *,
    proposal: str | None = None,
    turn_id: str = "turn-actor-1",
) -> tuple[dict[str, Any], object]:
    source_revision = host._repository.revision
    envelope = turn_runtime.start_turn(turn_id, source_revision, 120)
    request: dict[str, object] = {
        "profile_id": "profile.actor",
        "role": "ACTOR",
        "purpose": "assess",
        "subject_id": ACTOR_ID,
        "recipient_id": PLAYER_ID,
        "campaign_id": CAMPAIGN_ID,
        "allowed_channels": ["CURRENT_SCOPE"],
        "max_candidates": 1,
        "required_ids": ["actor-source"],
        "allowed_relations": [],
        "budget": 10_000,
        "source_frontier": source_revision,
    }
    candidates: list[dict[str, object]] = [
        {
            "candidate_id": "actor-source",
            "channel": "CURRENT_SCOPE",
            "rank": 0,
            "role": "ACTOR",
            "purpose": "assess",
            "subject_id": ACTOR_ID,
            "recipient_id": PLAYER_ID,
            "owner_family": "world.actor",
            "owner_identity": [ACTOR_ID],
            "dependencies": [],
        }
    ]
    binding = turn_runtime.bind_phase_from_context(
        envelope,
        "ACTOR",
        "assess",
        "profile.actor",
        host.context,
        request,
        candidates,
        ("actor_proposal",),
        subject_id=ACTOR_ID,
        recipient_id=PLAYER_ID,
    )
    turn_runtime.accept_phase_result(
        envelope,
        {
            "kind": "actor_proposal",
            "purpose": "assess",
            "bundle_id": binding["bundle_id"],
            "source_generation": source_revision,
            "subject_id": ACTOR_ID,
            "proposal": _phase_proposal(actor) if proposal is None else proposal,
        },
    )
    return envelope, binding["accepted_phase_result"]


def _live_claiming_actor() -> LiveRouting:
    claim = LiveClaim.exact_owner("world.actor", ACTOR_ID)
    opening_revision = "b" * 40
    epoch_id = derive_live_epoch_id(
        CAMPAIGN_ID, "scene.spring", opening_revision, (claim,)
    )
    source = LiveEnvelope(
        campaign_id=CAMPAIGN_ID,
        scene_id="scene.spring",
        epoch_id=epoch_id,
        source_ref=build_live_ref(CAMPAIGN_ID, "scene.spring", epoch_id),
        source_revision="c" * 40,
        opening_campaign_revision=opening_revision,
        claims=(claim,),
    )
    return LiveRouting(campaign_id=CAMPAIGN_ID, entries=(source,))


def _live_actor_pack(
    route: LiveRouting, actor: dict[str, object]
) -> LiveNativeStatePack:
    source = route.entries[0]
    return LiveNativeStatePack(
        source_key=source.source_key,
        source_revision=source.source_revision,
        next_source_native_creation_ordinal=1,
        source_native_ids=(),
        native_owner_states={"world.actor": actor},
        provenance={},
        privacy={},
        chronology={},
        unresolved_work={},
    )


def test_selected_host_establishes_trusted_npc_reconsideration_before_save() -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        actor = _actor()
        envelope, phase_result = _actor_phase(host, actor)

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value == "ESTABLISHED"
        assert result.before_state_revision == 4
        assert result.after_state_revision == 5
        assert result.owner_ref.family_key == "world.actor"
        assert result.owner_ref.identity == (ACTOR_ID,)
        staged = store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,))
        assert staged is not None
        snapshot = store.read_admitted_snapshot(
            CAMPAIGN_ID, (("world.actor", (ACTOR_ID,)),)
        )
        assert len(snapshot.row_fingerprints[("world.actor", (ACTOR_ID,))]) == 64
        admission_basis = snapshot.admission_bases[("world.actor", (ACTOR_ID,))]
        assert staged.source_basis == CAMPAIGN_REVISION
        assert admission_basis.source_revision == CAMPAIGN_REVISION
        assert len(admission_basis.source_fingerprint) == 64
        snapshot.rows[("world.actor", (ACTOR_ID,))].payload["state"]["continuity"] = {}
        other_campaign = store.read_admitted_snapshot(
            "campaign-other", (("world.actor", (ACTOR_ID,)),)
        )
        assert other_campaign.rows == {}
        assert other_campaign.absent_keys == (("world.actor", (ACTOR_ID,)),)
        staged_after_detached_mutation = store.load_current_owner(
            CAMPAIGN_ID, "world.actor", (ACTOR_ID,)
        )
        assert staged_after_detached_mutation == staged
        assert staged.payload == {
            **actor,
            "state_revision": 5,
            "state": {
                **actor["state"],
                "continuity": {
                    "evolving": {
                        **actor["state"]["continuity"]["evolving"],
                        "next_intention": {"statement": "Warn the miller"},
                    }
                },
            },
        }

        followup = host.context.assemble(
            {
                "profile_id": "profile.actor",
                "role": "ACTOR",
                "purpose": "assess",
                "subject_id": ACTOR_ID,
                "recipient_id": PLAYER_ID,
                "campaign_id": CAMPAIGN_ID,
                "allowed_channels": ["CURRENT_SCOPE"],
                "max_candidates": 1,
                "required_ids": ["actor-source"],
                "allowed_relations": [],
                "budget": 10_000,
                "source_frontier": CAMPAIGN_REVISION,
            },
            [
                {
                    "candidate_id": "actor-source",
                    "channel": "CURRENT_SCOPE",
                    "rank": 0,
                    "role": "ACTOR",
                    "purpose": "assess",
                    "subject_id": ACTOR_ID,
                    "recipient_id": PLAYER_ID,
                    "owner_family": "world.actor",
                    "owner_identity": [ACTOR_ID],
                    "dependencies": [],
                }
            ],
        )
        payload = followup["bundle"]["required"][0]["payload"]
        assert payload["schema_version"] == actor["schema_version"]
        assert payload["definition_id"] == actor["definition_id"]
        assert payload["state_revision"] == 5
        assert payload["state"]["continuity"]["evolving"]["next_intention"] == {
            "statement": "Warn the miller"
        }
        assert not hasattr(result, "after_image")


def test_read_session_expansion_reacquires_the_complete_union_after_hot_movement() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        envelope, phase_result = _actor_phase(host, _actor())
        established = host.actor_continuity.establish_from_phase(envelope, phase_result)
        assert established.status.value == "ESTABLISHED"

        session = host._current_owner.begin(host._begin_operation())
        actor_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        scene_ref = NativeOwnerRef("world.scene", ("scene.spring",))
        first = session.require((actor_ref,))
        first_actor = first.require(actor_ref)
        assert first_actor.source is CurrentOwnerSource.ACCEPTED_HOT
        assert first_actor.generation == 5

        staged = store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,))
        assert staged is not None
        moved_payload = deepcopy(dict(staged.payload))
        moved_payload["state_revision"] = 6
        store.stage_owner_document(
            OwnerDocument(
                campaign_id=CAMPAIGN_ID,
                family_key="world.actor",
                identity=(ACTOR_ID,),
                payload=moved_payload,
                source_basis=staged.source_basis,
                generation=6,
            )
        )
        assert not session.revalidate(first)

        expanded = session.require((scene_ref,))

        assert expanded.key_union == (actor_ref, scene_ref)
        recomputed_actor = expanded.require(actor_ref)
        assert recomputed_actor.source is CurrentOwnerSource.PINNED_CAMPAIGN
        assert recomputed_actor.generation == 4
        assert expanded.require(scene_ref).status.value == "ABSENT"
        assert session.revalidate(expanded)


def test_context_expansion_rejects_a_retained_actor_from_an_older_observation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        host, _repository = _selected_host(store, repository=repository)
        initial_actor = _actor()
        first_envelope, first_phase = _actor_phase(host, initial_actor)
        first = host.actor_continuity.establish_from_phase(first_envelope, first_phase)
        assert first.status.value == "ESTABLISHED"
        assert first.after_state_revision == 5

        current_actor = dict(
            store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)).payload
        )
        next_delta = _delta(current_actor)
        next_delta["changes"]["continuity"]["evolving"]["next_intention"][
            "statement"
        ] = "Seek a healer"
        next_envelope, next_phase = _actor_phase(
            host,
            current_actor,
            proposal=_phase_proposal(current_actor, delta=next_delta),
            turn_id="turn-actor-context-expansion",
        )
        repository.scene = {
            "id": "scene.spring",
            "kind": "world.scene",
            "state": {"name": "The spring"},
        }
        original_resolve_candidate = context_runtime._resolve_candidate
        producer_ran = False

        def advance_actor_after_actor_resolution(
            *args: Any, **kwargs: Any
        ) -> dict[str, object]:
            nonlocal producer_ran
            resolved = original_resolve_candidate(*args, **kwargs)
            if not producer_ran and resolved["owner_family"] == "world.actor":
                producer_ran = True
                assert not store._connection.in_transaction
                moved = host.actor_continuity.establish_from_phase(
                    next_envelope, next_phase
                )
                assert moved.status.value == "ESTABLISHED"
                assert moved.after_state_revision == 6
            return resolved

        monkeypatch.setattr(
            context_runtime, "_resolve_candidate", advance_actor_after_actor_resolution
        )
        result = host.context.assemble(
            {
                "profile_id": "profile.actor",
                "role": "ACTOR",
                "purpose": "assess",
                "subject_id": ACTOR_ID,
                "recipient_id": PLAYER_ID,
                "campaign_id": CAMPAIGN_ID,
                "allowed_channels": ["CURRENT_SCOPE"],
                "max_candidates": 2,
                "required_ids": ["actor-source"],
                "allowed_relations": ["requires"],
                "budget": 10_000,
                "source_frontier": CAMPAIGN_REVISION,
            },
            [
                {
                    "candidate_id": "actor-source",
                    "channel": "CURRENT_SCOPE",
                    "rank": 0,
                    "role": "ACTOR",
                    "purpose": "assess",
                    "subject_id": ACTOR_ID,
                    "recipient_id": PLAYER_ID,
                    "owner_family": "world.actor",
                    "owner_identity": [ACTOR_ID],
                    "dependencies": [
                        {"relation": "requires", "candidate_id": "scene-source"}
                    ],
                },
                {
                    "candidate_id": "scene-source",
                    "channel": "CURRENT_SCOPE",
                    "rank": 0,
                    "role": "ACTOR",
                    "purpose": "assess",
                    "subject_id": ACTOR_ID,
                    "recipient_id": PLAYER_ID,
                    "owner_family": "world.scene",
                    "owner_identity": ["scene.spring"],
                    "dependencies": [],
                },
            ],
        )

        assert result["outcome"] == "REVALIDATION_REQUIRED"
        assert producer_ran
        assert result["bundle"] is None
        staged = store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,))
        assert staged is not None and staged.payload["state_revision"] == 6


def test_actor_route_opening_during_predecessor_read_prevents_local_establishment() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        live = SelectedLive()
        host, _repository = _selected_host(store, repository=repository, live=live)
        actor = _actor()
        envelope, phase_result = _actor_phase(
            host, actor, turn_id="turn-actor-route-opening"
        )
        actor_path = route_native_record("world.actor", (ACTOR_ID,)).relative_path

        def open_live_route_during_predecessor_read(
            _pinned: PinnedCampaign, path: str
        ) -> None:
            if path != actor_path:
                return
            assert not store._connection.in_transaction
            repository.read_hook = None
            live.route = _live_claiming_actor()
            live.pack = _live_actor_pack(live.route, actor)

        repository.read_hook = open_live_route_during_predecessor_read

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value in {"UNSUPPORTED", "REVALIDATION_REQUIRED"}
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_read_session_revalidation_rejects_live_route_movement() -> None:
    with NativeHotStore(":memory:") as store:
        route = _live_claiming_actor()
        live = SelectedLive(route, pack=_live_actor_pack(route, _actor()))
        host, _repository = _selected_host(store, live=live)
        owner_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        session = host._current_owner.begin(host._begin_operation())

        observation = session.require((owner_ref,))

        assert observation.require(owner_ref).source is CurrentOwnerSource.SELECTED_LIVE
        live.route = LiveRouting(campaign_id=CAMPAIGN_ID, entries=())

        assert not session.revalidate(observation)


def test_read_session_revalidation_rereads_the_current_campaign_owner_source() -> None:
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        host, _repository = _selected_host(store, repository=repository)
        owner_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        operation = host._begin_operation()
        session = host._current_owner.begin(operation)
        observation = session.require((owner_ref,))
        initial_source_read_count = len(repository.path_reads)

        successor_revision = "d" * 40
        repository.revision = successor_revision
        repository.actor["state"]["continuity"]["evolving"]["current_objective"] = {
            "statement": "A current-source change after observation"
        }

        assert not store._connection.in_transaction
        assert not session.revalidate(observation)
        assert len(repository.path_reads) == initial_source_read_count + 1
        assert repository.path_reads[-1][0] == successor_revision


def test_read_session_revalidation_refreshes_immutable_campaign_revision() -> None:
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        live = SelectedLive()
        host, _repository = _selected_host(store, repository=repository, live=live)
        actor_path = route_native_record("world.actor", (ACTOR_ID,)).relative_path
        owner_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        operation = host._begin_operation()
        session = host._current_owner.begin(operation)
        observation = session.require((owner_ref,))

        moved_actor = deepcopy(repository.actor)
        moved_actor["state"]["continuity"]["evolving"]["current_objective"] = {
            "statement": "The immutable successor revision"
        }
        successor_revision = "d" * 40
        repository.revision_records = {
            operation.pinned_campaign.revision: {
                actor_path: deepcopy(repository.actor)
            },
            successor_revision: {actor_path: moved_actor},
        }
        repository.revision = successor_revision

        assert not session.revalidate(observation)
        assert repository.path_reads[-1] == (successor_revision, actor_path)
        assert live.route_pin_reads[-1] == successor_revision


def test_read_session_revalidation_rejects_revision_movement_during_last_owner_read() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        live = SelectedLive()
        host, _repository = _selected_host(store, repository=repository, live=live)
        actor_path = route_native_record("world.actor", (ACTOR_ID,)).relative_path
        owner_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        operation = host._begin_operation()
        session = host._current_owner.begin(operation)
        observation = session.require((owner_ref,))
        successor_revision = "d" * 40
        repository.revision_records = {
            operation.pinned_campaign.revision: {
                actor_path: deepcopy(repository.actor)
            },
            successor_revision: {actor_path: deepcopy(repository.actor)},
        }
        moved = False

        def advance_head_during_owner_read(_pinned: PinnedCampaign, path: str) -> None:
            nonlocal moved
            if path == actor_path and not moved:
                moved = True
                assert not store._connection.in_transaction
                repository.revision = successor_revision
                live.route = _live_claiming_actor()

        repository.read_hook = advance_head_during_owner_read

        assert not session.revalidate(observation)
        assert moved
        assert repository.path_reads[-1] == (
            operation.pinned_campaign.revision,
            actor_path,
        )
        assert live.route_pin_reads[-1] == successor_revision


def test_actor_source_movement_after_operation_revalidation_blocks_establishment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with NativeHotStore(":memory:") as store:
        repository = ActorRepository()
        host, _repository = _selected_host(store, repository=repository)
        actor = _actor()
        envelope, phase_result = _actor_phase(
            host, actor, turn_id="turn-actor-source-movement"
        )
        original_revalidate = CurrentOwnerReadSession.revalidate
        source_moved = False

        def move_source_after_revalidation(
            session: CurrentOwnerReadSession,
            observation: CurrentOwnerObservation | None = None,
        ) -> bool:
            nonlocal source_moved
            valid = original_revalidate(session, observation)
            if valid and not source_moved:
                source_moved = True
                assert not store._connection.in_transaction
                repository.revision = "d" * 40
                repository.actor["state"]["continuity"]["evolving"][
                    "current_objective"
                ] = {"statement": "A new campaign predecessor"}
            return valid

        monkeypatch.setattr(
            CurrentOwnerReadSession, "revalidate", move_source_after_revalidation
        )

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert source_moved
        assert result.status.value == "REVALIDATION_REQUIRED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_current_owner_observation_payload_does_not_retain_nested_mutations() -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        owner_ref = NativeOwnerRef("world.actor", (ACTOR_ID,))
        session = host._current_owner.begin(host._begin_operation())
        observation = session.require((owner_ref,))
        owner_read = observation.require(owner_ref)
        original = owner_read.payload["state"]["continuity"]["evolving"][
            "reconsideration_cues"
        ][0]["statement"]
        fingerprint = observation.observation_fingerprint

        owner_read.payload["state"]["continuity"]["evolving"]["reconsideration_cues"][
            0
        ]["statement"] = "tampered outside the retained evidence"

        assert (
            observation.require(owner_ref).payload["state"]["continuity"]["evolving"][
                "reconsideration_cues"
            ][0]["statement"]
            == original
        )
        assert observation.observation_fingerprint == fingerprint
        assert session.revalidate(observation)


def test_same_phase_consumption_is_idempotent_and_no_change_writes_nothing() -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        envelope, phase_result = _actor_phase(host, _actor())

        first = host.actor_continuity.establish_from_phase(envelope, phase_result)
        repeated = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert repeated == first
        assert (
            store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)).payload[
                "state_revision"
            ]
            == 5
        )

    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        actor = _actor()
        new_envelope, new_phase = _actor_phase(
            host,
            actor,
            proposal=_phase_proposal(actor, delta=None),
            turn_id="turn-actor-no-change",
        )
        no_change = host.actor_continuity.establish_from_phase(new_envelope, new_phase)
        no_change_again = host.actor_continuity.establish_from_phase(
            new_envelope, new_phase
        )
        assert no_change.status.value == "NO_CHANGE"
        assert no_change == no_change_again
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


@pytest.mark.parametrize(
    "proposal_kwargs",
    [
        {"cue": {"statement": "not a current cue"}},
        {"extra": {"source_evidence": [{"accepted": True, "current": True}]}},
        {"extra": {"replacement_state": {"state_revision": 500}}},
        {"delta": _delta(_actor(), source_refs=["event.foreign"])},
        {"extra": {"native_after_image": _actor()}},
    ],
)
def test_untrusted_or_out_of_scope_proposals_fail_without_hot_establishment(
    proposal_kwargs: dict[str, object],
) -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        actor = _actor()
        proposal = _phase_proposal(actor, **proposal_kwargs)
        envelope, phase_result = _actor_phase(
            host,
            actor,
            proposal=proposal,
            turn_id="turn-actor-invalid",
        )

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value == "UNSUPPORTED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_raw_native_actor_after_image_is_not_an_accepted_actor_delta() -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        actor = _actor()
        envelope, phase_result = _actor_phase(
            host,
            actor,
            proposal=json.dumps(_actor(state_revision=100)),
            turn_id="turn-actor-raw-after-image",
        )

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value == "UNSUPPORTED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_source_movement_and_missing_native_revision_fail_closed() -> None:
    with NativeHotStore(":memory:") as store:
        host, repository = _selected_host(store)
        envelope, phase_result = _actor_phase(host, _actor())
        repository.revision = "d" * 40
        repository.actor["state"]["continuity"]["evolving"]["current_objective"] = {
            "statement": "The current objective moved with the durable source"
        }

        moved = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert moved.status.value == "REVALIDATION_REQUIRED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None

    with NativeHotStore(":memory:") as store:
        host, repository = _selected_host(store)
        envelope, phase_result = _actor_phase(host, _actor())
        repository.actor["state_revision"] = 5

        moved_owner = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert moved_owner.status.value == "REVALIDATION_REQUIRED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None

    with NativeHotStore(":memory:") as store:
        actor = _actor(state_revision=None)
        host, _repository = _selected_host(store, repository=ActorRepository(actor))
        with pytest.raises(turn_runtime.TurnContractError):
            _actor_phase(host, actor)
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_admitted_hot_survives_disjoint_pin_movement_but_not_actor_source_movement() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        host, repository = _selected_host(store)
        first_envelope, first_phase = _actor_phase(host, _actor())
        first = host.actor_continuity.establish_from_phase(first_envelope, first_phase)
        assert first.status.value == "ESTABLISHED"
        repository.revision = "d" * 40
        hot_actor = dict(
            store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)).payload
        )
        next_delta = _delta(hot_actor)
        next_delta["changes"]["continuity"]["evolving"]["next_intention"][
            "statement"
        ] = "Seek a healer"

        second_envelope, second_phase = _actor_phase(
            host,
            hot_actor,
            proposal=_phase_proposal(hot_actor, delta=next_delta),
            turn_id="turn-actor-after-disjoint-move",
        )
        second = host.actor_continuity.establish_from_phase(
            second_envelope, second_phase
        )

        assert second.status.value == "ESTABLISHED"
        assert second.before_state_revision == 5
        assert second.after_state_revision == 6

    with NativeHotStore(":memory:") as store:
        host, repository = _selected_host(store)
        first_envelope, first_phase = _actor_phase(host, _actor())
        first = host.actor_continuity.establish_from_phase(first_envelope, first_phase)
        assert first.status.value == "ESTABLISHED"
        repository.revision = "d" * 40
        repository.actor["state_revision"] = 5
        repository.actor["state"]["continuity"]["evolving"]["current_objective"] = {
            "statement": "A conflicting durable objective"
        }

        with pytest.raises(turn_runtime.TurnContractError):
            _actor_phase(
                host,
                dict(
                    store.load_current_owner(
                        CAMPAIGN_ID, "world.actor", (ACTOR_ID,)
                    ).payload
                ),
                turn_id="turn-actor-after-overlap-move",
            )
        current = store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,))
        assert current is not None and current.payload["state_revision"] == 5


def test_published_hot_after_image_is_an_exact_current_basis_for_the_next_local_delta() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        host, repository = _selected_host(store)
        first_envelope, first_phase = _actor_phase(host, _actor())
        first = host.actor_continuity.establish_from_phase(first_envelope, first_phase)
        assert first.status.value == "ESTABLISHED"
        published_after_image = dict(
            store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)).payload
        )
        repository.revision = "d" * 40
        repository.actor = deepcopy(published_after_image)
        next_delta = _delta(published_after_image)
        next_delta["changes"]["continuity"]["evolving"]["next_intention"][
            "statement"
        ] = "Seek a healer"

        next_envelope, next_phase = _actor_phase(
            host,
            published_after_image,
            proposal=_phase_proposal(published_after_image, delta=next_delta),
            turn_id="turn-actor-after-publication",
        )
        next_result = host.actor_continuity.establish_from_phase(
            next_envelope, next_phase
        )

        assert next_result.status.value == "ESTABLISHED"
        assert next_result.before_state_revision == 5
        assert next_result.after_state_revision == 6
        current = store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,))
        assert current is not None
        assert current.source_basis == repository.revision


def test_context_from_another_host_or_rebound_actor_phase_cannot_be_consumed() -> None:
    with NativeHotStore(":memory:") as store:
        first_host, repository = _selected_host(store)
        second_host, _ = _selected_host(store, repository=repository)
        envelope, phase_result = _actor_phase(first_host, _actor())

        foreign = second_host.actor_continuity.establish_from_phase(
            envelope, phase_result
        )

        assert foreign.status.value == "REVALIDATION_REQUIRED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None

    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        envelope, old_phase = _actor_phase(host, _actor())
        request: dict[str, object] = {
            "profile_id": "profile.actor",
            "role": "ACTOR",
            "purpose": "assess",
            "subject_id": ACTOR_ID,
            "recipient_id": PLAYER_ID,
            "campaign_id": CAMPAIGN_ID,
            "allowed_channels": ["CURRENT_SCOPE"],
            "max_candidates": 1,
            "required_ids": ["actor-source"],
            "allowed_relations": [],
            "budget": 10_000,
            "source_frontier": CAMPAIGN_REVISION,
        }
        candidate = {
            "candidate_id": "actor-source",
            "channel": "CURRENT_SCOPE",
            "rank": 0,
            "role": "ACTOR",
            "purpose": "assess",
            "subject_id": ACTOR_ID,
            "recipient_id": PLAYER_ID,
            "owner_family": "world.actor",
            "owner_identity": [ACTOR_ID],
            "dependencies": [],
        }
        turn_runtime.bind_phase_from_context(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            host.context,
            request,
            [candidate],
            ("actor_proposal",),
            subject_id=ACTOR_ID,
            recipient_id=PLAYER_ID,
        )

        rebound = host.actor_continuity.establish_from_phase(envelope, old_phase)

        assert rebound.status.value == "REVALIDATION_REQUIRED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_actor_without_a_current_reconsideration_cue_is_unsupported() -> None:
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(
            store, repository=ActorRepository(_actor(cues=[]))
        )
        actor = _actor(cues=[])
        with pytest.raises(turn_runtime.TurnContractError):
            _actor_phase(
                host,
                actor,
                proposal=json.dumps(
                    {
                        "assessment_purpose": "assessment.reconsider",
                        "reconsideration_cue": {},
                        "delta": _delta(actor),
                    }
                ),
            )
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_player_controlled_actor_and_selected_live_actor_cannot_be_locally_changed() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        actor = _actor(roles=["actor.player_character"])
        host, _repository = _selected_host(store, repository=ActorRepository(actor))
        envelope, phase_result = _actor_phase(host, actor)

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value == "UNSUPPORTED"
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None

    with NativeHotStore(":memory:") as store:
        route = _live_claiming_actor()
        actor = _actor()
        live = SelectedLive(route, pack=_live_actor_pack(route, actor))
        host, _repository = _selected_host(store, live=live)
        envelope, phase_result = _actor_phase(host, actor)
        context_actor = envelope["phase_bindings"]["ACTOR"]["context_basis"].bundle[
            "required"
        ][0]["payload"]
        assert context_actor == actor

        result = host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert result.status.value == "UNSUPPORTED"
        assert live.source_reads >= 1
        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None


def test_failed_sqlite_establishment_rolls_back_row_admission_and_phase_receipt() -> (
    None
):
    with NativeHotStore(":memory:") as store:
        host, _repository = _selected_host(store)
        envelope, phase_result = _actor_phase(host, _actor())
        store._connection.execute(
            """
            CREATE TRIGGER fail_actor_insert BEFORE INSERT ON current_native_owner
            WHEN NEW.family_key = 'world.actor'
            BEGIN SELECT RAISE(ABORT, 'test rollback'); END
            """
        )

        with pytest.raises(sqlite3.IntegrityError, match="test rollback"):
            host.actor_continuity.establish_from_phase(envelope, phase_result)

        assert store.load_current_owner(CAMPAIGN_ID, "world.actor", (ACTOR_ID,)) is None
        snapshot = store.read_admitted_snapshot(
            CAMPAIGN_ID, (("world.actor", (ACTOR_ID,)),)
        )
        assert snapshot.rows == {}
        assert snapshot.absent_keys == (("world.actor", (ACTOR_ID,)),)

        store._connection.execute("DROP TRIGGER fail_actor_insert")
        retried = host.actor_continuity.establish_from_phase(envelope, phase_result)
        assert retried.status.value == "ESTABLISHED"


def test_cold_restart_does_not_admit_a_surviving_dirty_actor_row(tmp_path) -> None:
    database = str(tmp_path / "hot.sqlite")
    first_store = NativeHotStore(database)
    first_host, _repository = _selected_host(first_store)
    envelope, phase_result = _actor_phase(first_host, _actor())

    established = first_host.actor_continuity.establish_from_phase(
        envelope, phase_result
    )
    assert established.status.value == "ESTABLISHED"
    first_store.close()

    recovered_store = NativeHotStore(database)
    try:
        snapshot = recovered_store.read_admitted_snapshot(
            CAMPAIGN_ID, (("world.actor", (ACTOR_ID,)),)
        )
        assert snapshot.rows == {}
        assert snapshot.absent_keys == (("world.actor", (ACTOR_ID,)),)
    finally:
        recovered_store.close()
