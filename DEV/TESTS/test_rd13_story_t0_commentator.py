from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from GAME.TOOLS.commentator import (
    CommentatorContractError,
    build_commentator_control_projection,
    build_commentator_snapshot,
    filter_commentator_request,
)
from GAME.TOOLS.dramaturg import (
    DramaturgContractError,
    admit_dramaturg_horizon,
    rebase_dramaturg_horizon,
    validate_dramaturg_horizon,
)
from GAME.TOOLS.history import (
    FRAMEWORK_MODULE_VERSION,
    HistoryContractError,
    NativeHistoryPublication,
    _issue_native_history_from_window,
    append_semantic_event,
    build_t0_basis,
    recover_native_history,
    validate_semantic_event_draft,
    validate_t0_basis,
)
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
    build_live_ref,
    derive_live_epoch_id,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.runtime_host import EvtSourceWindow, compose_runtime_host
from GAME.TOOLS.story import (
    StoryContractError,
    build_story_source_bundle,
    project_story_window,
    select_story_root,
    story_record_path,
    validate_story_projection,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def _semantic_event() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": "event.gate_opened",
        "semantic_order": 7,
        "kind": "event.action",
        "provenance_refs": ["resolution.gate"],
        "semantic_delta": {"gate": "opened"},
    }


def _t0_basis() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": "event.gate_opened",
        "actor_id": "actor.guard",
        "factors": [
            {
                "owner_family": "world.knowledge",
                "factor_id": "fact.party_authorized",
                "t0_value": "epistemic.known",
                "provenance_refs": ["fact.party_authorized"],
            }
        ],
    }


_HISTORY_REVISION = "a" * 40
_LIVE_ORIGIN = "LIVE:e1-" + ("0" * 64)


def _evt_window(
    *,
    campaign_id: str = "campaign.main",
    origin: str = "LOCAL",
    source_ref: str = "refs/heads/campaign/main",
    source_revision: str = _HISTORY_REVISION,
    event: dict[str, object] | None = None,
    lower_exclusive_ordinal: int | None = 6,
    upper_ordinal: int | None = 7,
) -> EvtSourceWindow:
    if origin != "LOCAL":
        raise ValueError("test helper supports only host-issued LOCAL windows")
    total = upper_ordinal or 0
    terminal_event = _semantic_event() if event is None else event
    source_events = [
        {
            **_semantic_event(),
            "event_id": f"event-{ordinal}",
            "semantic_order": ordinal,
        }
        for ordinal in range(1, total + 1)
    ]
    if source_events:
        source_events[-1] = terminal_event
    repository = _HistoryRepository(
        campaign_id=campaign_id,
        source_ref=source_ref,
        revision=source_revision,
        events=source_events,
    )
    host = compose_runtime_host(campaign_id, repository, _HistoryLiveTransport())
    return host.semantic_events.read_local_evt_window(
        lower_exclusive_ordinal=lower_exclusive_ordinal,
        max_items=max(1, total - (lower_exclusive_ordinal or 0)),
    )


class _HistoryRepository:
    def __init__(
        self,
        *,
        campaign_id: str = "campaign.main",
        source_ref: str = "refs/heads/campaign/main",
        revision: str = _HISTORY_REVISION,
        events: list[dict[str, object]] | None = None,
    ) -> None:
        self.campaign_id = campaign_id
        self.source_ref = source_ref
        self.revision = revision
        if events is None:
            events = [
                {**_semantic_event(), "event_id": "event-1", "semantic_order": 1},
                {**_semantic_event(), "event_id": "event-2", "semantic_order": 2},
            ]
        entries: list[dict[str, object]] = []
        self.records: dict[str, object] = {
            "MANIFEST.yaml": {
                "campaign_id": campaign_id,
                "branch": source_ref,
            }
        }
        for ordinal, event in enumerate(events, start=1):
            event_id = event["event_id"]
            if not isinstance(event_id, str):
                raise TypeError("history fixture event id must be text")
            path = route_native_record(
                "runtime.semantic_event", (event_id,)
            ).relative_path
            entries.append({"event_id": event_id, "ordinal": ordinal, "path": path})
            self.records[path] = event
        self.records["INDEX/EVENT_INDEX.yaml"] = {
            "schema_version": 1,
            "entity_type": "EVENT",
            "complete": True,
            "upper_ordinal": len(events) if events else None,
            "entries": entries,
        }
        self.read_paths: list[str] = []

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        return PinnedCampaign(campaign_id, self.revision, "b" * 40)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        del pinned
        self.read_paths.append(path)
        return self.records[path]

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        del campaign_id
        return {}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        del campaign_ref, revision
        return {}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        del repository_ref, ancestor_revision, descendant_revision
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        del campaign_ref, revision
        return {}


class _HistoryLiveTransport:
    def __init__(self) -> None:
        opening_revision = "e" * 40
        claims = (LiveClaim.exact_owner("world.scene", "scene.main"),)
        epoch_id = derive_live_epoch_id(
            "campaign.main", "scene.main", opening_revision, claims
        )
        self.source = LiveEnvelope(
            campaign_id="campaign.main",
            scene_id="scene.main",
            epoch_id=epoch_id,
            source_ref=build_live_ref("campaign.main", "scene.main", epoch_id),
            source_revision="c" * 40,
            claims=claims,
            opening_campaign_revision=opening_revision,
        )
        self.pack = LiveNativeStatePack(
            source_key=self.source.source_key,
            source_revision=self.source.source_revision,
            next_source_native_creation_ordinal=1,
            source_native_ids=(),
            native_owner_states={
                "runtime.semantic_event": {
                    "complete": True,
                    "upper_ordinal": 1,
                    "entries": [
                        {
                            "event_id": "live-event-1",
                            "ordinal": 1,
                            "event_record": {
                                **_semantic_event(),
                                "event_id": "live-event-1",
                                "semantic_order": 1,
                            },
                        }
                    ],
                }
            },
            provenance={},
            privacy={},
            chronology={},
            unresolved_work={},
        )

    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        del pinned
        return LiveRouting(campaign_id=campaign_id, entries=(self.source,))

    def read_selected_live_source(
        self, routing: LiveRouting, source: LiveEnvelope
    ) -> LiveNativeStatePack:
        del routing
        if source.source_key != self.source.source_key:
            raise KeyError(source.source_key)
        return self.pack


def _story_projection() -> dict[str, object]:
    return {
        "schema_version": 1,
        "story_id": "E000007",
        "content": {"body": "The guard opened the gate."},
        "sources": ["event.gate_opened"],
        "t0_basis": _t0_basis(),
        "availability": {"visible_to": ["player.aria"]},
    }


class NativeHistoryAuthorityTests(unittest.TestCase):
    def test_caller_shaped_semantic_events_cannot_mint_native_history(self) -> None:
        with self.assertRaises(HistoryContractError):
            append_semantic_event([], _semantic_event())
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "provenance_refs": []})


class NativeHistoryWindowTests(unittest.TestCase):
    def test_host_history_reads_only_the_bound_semantic_event_adapter_window(self) -> None:
        repository = _HistoryRepository()
        host = compose_runtime_host(
            "campaign.main", repository, _HistoryLiveTransport()
        )

        publication = host.history.read()

        self.assertEqual(publication.origin, "LOCAL")
        self.assertEqual(publication.events[0].event_id, "event-1")
        self.assertIn("INDEX/EVENT_INDEX.yaml", repository.read_paths)
        self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_bound_evt_window_issues_ephemeral_history_with_admission_provenance(self) -> None:
        repository = _HistoryRepository()
        host = compose_runtime_host(
            "campaign.main", repository, _HistoryLiveTransport()
        )
        publication = host.history.read()

        self.assertIsInstance(publication, NativeHistoryPublication)
        self.assertEqual(publication.campaign_id, "campaign.main")
        self.assertEqual(publication.origin, "LOCAL")
        self.assertEqual(publication.source_ref, "refs/heads/campaign/main")
        self.assertEqual(publication.source_revision, _HISTORY_REVISION)
        self.assertEqual(publication.events[0].event_id, "event-1")
        self.assertEqual(publication.events[0].admission_ordinal, 1)
        self.assertEqual(publication.events[0].semantic_order, 1)

    def test_history_rejects_aggregate_or_forged_window_shapes(self) -> None:
        aggregate = {
            "campaign_id": "campaign.main",
            "events": [_semantic_event()],
        }

        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                aggregate,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window().to_mapping(),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

        adapter_window = _evt_window()
        caller_window = EvtSourceWindow(
            campaign_id=adapter_window.campaign_id,
            origin=adapter_window.origin,
            source_ref=adapter_window.source_ref,
            source_revision=adapter_window.source_revision,
            lane=adapter_window.lane,
            lower_exclusive_ordinal=adapter_window.lower_exclusive_ordinal,
            upper_ordinal=adapter_window.upper_ordinal,
            interval_complete_through_upper=adapter_window.interval_complete_through_upper,
            entries=adapter_window.entries,
        )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                caller_window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

        forged = object.__new__(EvtSourceWindow)
        original = _evt_window()
        for name in (
            "campaign_id",
            "origin",
            "source_ref",
            "source_revision",
            "lane",
            "lower_exclusive_ordinal",
            "upper_ordinal",
            "interval_complete_through_upper",
            "entries",
        ):
            object.__setattr__(forged, name, getattr(original, name))
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                forged,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

    def test_evt_window_issuance_is_bound_to_its_runtime_host(self) -> None:
        first_host = compose_runtime_host(
            "campaign.main", _HistoryRepository(), _HistoryLiveTransport()
        )
        other_host = compose_runtime_host(
            "campaign.main", _HistoryRepository(), _HistoryLiveTransport()
        )
        window = first_host.semantic_events.read_local_evt_window(
            lower_exclusive_ordinal=None, max_items=1
        )

        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
                _expected_host_token=other_host._basis_token,
            )

    def test_history_uses_exact_selected_live_source_and_preserves_origin(self) -> None:
        live = _HistoryLiveTransport()
        host = compose_runtime_host("campaign.main", _HistoryRepository(), live)

        publication = host.history.read(origin=f"LIVE:{live.source.epoch_id}")

        self.assertEqual(publication.origin, f"LIVE:{live.source.epoch_id}")
        self.assertEqual(publication.source_ref, live.source.source_ref)
        self.assertEqual(publication.source_revision, live.source.source_revision)
        self.assertEqual(publication.events[0].origin, f"LIVE:{live.source.epoch_id}")
        self.assertEqual(publication.events[0].semantic_order, 1)

    def test_history_rejects_live_pack_from_wrong_source_or_revision(self) -> None:
        for field, value in (
            ("source_key", ["campaign.main", "scene.other", "foreign-epoch"]),
            ("source_revision", "d" * 40),
        ):
            with self.subTest(field=field):
                live = _HistoryLiveTransport()
                live.pack = live.pack.as_mapping() | {field: value}
                repository = _HistoryRepository()
                host = compose_runtime_host("campaign.main", repository, live)

                with self.assertRaises(HistoryContractError):
                    host.history.read(origin=f"LIVE:{live.source.epoch_id}")

                self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_missing_selected_live_history_never_falls_back_to_local(self) -> None:
        class MissingLiveTransport(_HistoryLiveTransport):
            def read_selected_live(
                self, campaign_id: str, pinned: PinnedCampaign
            ) -> LiveRouting:
                del pinned
                return LiveRouting(campaign_id=campaign_id, entries=())

        live = MissingLiveTransport()
        repository = _HistoryRepository()
        host = compose_runtime_host("campaign.main", repository, live)

        with self.assertRaises(HistoryContractError):
            host.history.read(origin=f"LIVE:{live.source.epoch_id}")

        self.assertNotIn("INDEX/EVENT_INDEX.yaml", repository.read_paths)
        self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_history_rejects_wrong_provenance_order_schema_and_interval(self) -> None:
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(event={**_semantic_event(), "semantic_order": 8}),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(),
                campaign_id="campaign.other",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(event={**_semantic_event(), "schema_version": 2}),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

    def test_history_rechecks_forged_gap_duplicate_and_completeness_claims(self) -> None:
        original = _evt_window()
        forged_windows: list[EvtSourceWindow] = []
        for entries, complete in (
            (
                (
                    original.entries[0],
                    {
                        "ordinal": 8,
                        "event_id": "event.other",
                        "event_record": {
                            **_semantic_event(),
                            "event_id": "event.other",
                            "semantic_order": 8,
                        },
                    },
                ),
                True,
            ),
            (
                (
                    original.entries[0],
                    {
                        "ordinal": 7,
                        "event_id": "event.other",
                        "event_record": {
                            **_semantic_event(),
                            "event_id": "event.other",
                        },
                    },
                ),
                True,
            ),
        ):
            forged = object.__new__(EvtSourceWindow)
            for name in (
                "campaign_id",
                "origin",
                "source_ref",
                "source_revision",
                "lane",
                "lower_exclusive_ordinal",
                "upper_ordinal",
            ):
                object.__setattr__(forged, name, getattr(original, name))
            object.__setattr__(forged, "interval_complete_through_upper", complete)
            object.__setattr__(forged, "entries", entries)
            forged_windows.append(forged)

        incomplete = object.__new__(EvtSourceWindow)
        for name in (
            "campaign_id",
            "origin",
            "source_ref",
            "source_revision",
            "lane",
            "lower_exclusive_ordinal",
            "upper_ordinal",
            "entries",
        ):
            object.__setattr__(incomplete, name, getattr(original, name))
        object.__setattr__(incomplete, "interval_complete_through_upper", False)
        forged_windows.append(incomplete)

        for forged in forged_windows:
            with self.subTest(
                entries=forged.entries, complete=forged.interval_complete_through_upper
            ), self.assertRaises(HistoryContractError):
                _issue_native_history_from_window(
                    forged,
                    campaign_id="campaign.main",
                    expected_origin="LOCAL",
                    expected_source_ref=original.source_ref,
                    expected_source_revision=original.source_revision,
                )

    def test_history_recovery_revalidates_ephemeral_publication_provenance(self) -> None:
        window = _evt_window()
        publication = _issue_native_history_from_window(
            window,
            campaign_id="campaign.main",
            expected_origin="LOCAL",
            expected_source_ref=window.source_ref,
            expected_source_revision=window.source_revision,
        )

        recovered = recover_native_history(
            publication.to_mapping(), currentness=publication.currentness
        )

        self.assertEqual(recovered.to_mapping(), publication.to_mapping())
        forged = publication.to_mapping()
        forged["origin"] = "LOCAL"  # type: ignore[index]
        forged["events"] = []  # type: ignore[index]
        with self.assertRaises(HistoryContractError):
            recover_native_history(forged, currentness=publication.currentness)

    def test_history_api_has_no_caller_adapter_override(self) -> None:
        window = _evt_window()

        with self.assertRaises(TypeError):
            _issue_native_history_from_window(  # type: ignore[call-arg]
                window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref=window.source_ref,
                expected_source_revision=window.source_revision,
                source_adapter=object(),
            )


class T0BasisTests(unittest.TestCase):
    def test_t0_basis_is_explicit_and_reconstructible_without_current_actor_state(self) -> None:
        basis = build_t0_basis(_semantic_event(), _t0_basis())

        self.assertEqual(basis["factors"][0]["t0_value"], "epistemic.known")
        with self.assertRaises(HistoryContractError):
            validate_t0_basis({**_t0_basis(), "factors": [{"factor_id": "fact.party_authorized"}]})


class StoryProjectionTests(unittest.TestCase):
    def test_story_is_a_projection_of_a_bounded_native_source_bundle(self) -> None:
        bundle = build_story_source_bundle([_semantic_event()], layer="EVENTS")
        projection = project_story_window(bundle, [_story_projection()])

        self.assertEqual(projection[0]["sources"], ["event.gate_opened"])
        self.assertEqual(bundle["events"][0]["event_id"], "event.gate_opened")

    def test_story_window_revalidates_and_rejects_forged_malformed_or_duplicate_bundle_events(
        self,
    ) -> None:
        forged_event = {**_semantic_event(), "provenance_refs": []}
        malformed_event = {"event_id": "event.gate_opened"}

        for events in (
            [forged_event],
            [malformed_event],
            [_semantic_event(), _semantic_event()],
        ):
            with self.subTest(events=events):
                with self.assertRaises(StoryContractError):
                    project_story_window({"layer": "EVENTS", "events": events}, [])


class StoryT0MaterializationTests(unittest.TestCase):
    def test_story_event_retains_story_local_t0_basis(self) -> None:
        projection = validate_story_projection(_story_projection(), layer="EVENTS")

        self.assertEqual(projection["t0_basis"]["event_id"], "event.gate_opened")
        self.assertNotIn("current_actor_state", projection)


class CommentatorSelfContainedTests(unittest.TestCase):
    def test_commentator_filters_hidden_story_material_before_request_materialization(self) -> None:
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )
        snapshot = build_commentator_snapshot([_story_projection()], control)

        self.assertEqual(filter_commentator_request(snapshot, "player.aria"), [_story_projection()])
        self.assertEqual(filter_commentator_request(snapshot, "player.borin"), [])

    def test_commentator_rejects_an_invalid_control_projection(self) -> None:
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {"schema_version": 0, "controls": {"player.aria": {"story_ids": ["E000007"]}}},
            )

    def test_commentator_control_cannot_widen_story_availability_for_another_player(self) -> None:
        private_projection = _story_projection()
        private_projection["story_id"] = "E000008"
        private_projection["availability"] = {"visible_to": ["player.borin"]}
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007", "E000008"]}}
        )
        snapshot = build_commentator_snapshot([_story_projection(), private_projection], control)

        self.assertEqual(filter_commentator_request(snapshot, "player.aria"), [_story_projection()])


class DramaturgHorizonTests(unittest.TestCase):
    def test_dramaturg_horizon_is_provisional_and_has_no_future_fact_field(self) -> None:
        horizon = validate_dramaturg_horizon(
            {
                "schema_version": 1,
                "scope_id": "campaign.main",
                "generation": 1,
                "source_basis": ["event.gate_opened"],
                "entries": [{"kind": "PROVISIONAL_DRAMATURGIC_DIRECTION", "text": "Prepare a guarded route."}],
            }
        )

        self.assertEqual(horizon["generation"], 1)
        self.assertNotIn("future_fact", horizon)


class HistoryProjectionSeparationTests(unittest.TestCase):
    def test_story_validation_never_mutates_native_history(self) -> None:
        history = [_semantic_event()]
        validate_story_projection(_story_projection(), layer="EVENTS")

        self.assertEqual(history, [_semantic_event()])


class CompositeIntegrationTests(unittest.TestCase):
    def test_owner_local_chain_preserves_native_event_and_reader_safe_projection(self) -> None:
        history = [_semantic_event()]
        bundle = build_story_source_bundle(history, layer="EVENTS")
        projection = project_story_window(bundle, [_story_projection()])
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )

        self.assertEqual(
            filter_commentator_request(build_commentator_snapshot(projection, control), "player.aria"),
            projection,
        )


class StoryStorageSelectorTests(unittest.TestCase):
    def test_story_selector_is_static_and_rejects_noncanonical_or_traversal_roots(self) -> None:
        self.assertEqual(select_story_root("STORY"), "STORY")
        for root in ("../STORY", "STORY/other", "ARCHIVE"):
            with self.subTest(root=root):
                with self.assertRaises(StoryContractError):
                    select_story_root(root)


class StoryPhysicalRouteTests(unittest.TestCase):
    def test_story_event_route_is_prefix_and_thousand_shard_bound(self) -> None:
        self.assertEqual(
            story_record_path("STORY", "E000007"),
            Path("STORY/EVENTS/000/E000007.yaml"),
        )
        self.assertEqual(
            story_record_path("STORY", "N003562"),
            Path("STORY/NARRATIVE/003/N003562.yaml"),
        )


class DramaturgPublicationTests(unittest.TestCase):
    def test_unadmitted_dramaturg_candidate_cannot_enter_native_history(self) -> None:
        history = [_semantic_event()]
        horizon = validate_dramaturg_horizon(
            {
                "schema_version": 1,
                "scope_id": "campaign.main",
                "generation": 1,
                "source_basis": ["event.gate_opened"],
                "entries": [],
            }
        )

        with self.assertRaises(DramaturgContractError):
            admit_dramaturg_horizon(horizon, mode="singleplayer")
        self.assertEqual(history, [_semantic_event()])


class DramaturgAdmissionTests(unittest.TestCase):
    def test_retained_horizon_requires_multiplayer_and_current_source_basis(self) -> None:
        horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }

        with self.assertRaises(DramaturgContractError):
            admit_dramaturg_horizon(horizon, mode="singleplayer")
        self.assertEqual(admit_dramaturg_horizon(horizon, mode="multiplayer"), horizon)


class DramaturgRebaseTests(unittest.TestCase):
    def test_rebase_rejects_incompatible_native_source_without_silent_merge(self) -> None:
        horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }

        with self.assertRaises(DramaturgContractError):
            rebase_dramaturg_horizon(horizon, current_source_basis=["event.gate_closed"])


class StorySchemaTests(unittest.TestCase):
    def test_owner_local_schemas_are_strict_and_use_initial_local_versions(self) -> None:
        schema_names = (
            "runtime-semantic-event-state.schema.json",
            "native-history-currentness.schema.json",
            "native-history-publication.schema.json",
            "story-projection-state.schema.json",
            "story-event-unit.schema.json",
            "story-narrative-unit.schema.json",
            "story-mechanics-unit.schema.json",
            "semantic-event-t0-basis.schema.json",
            "commentator-snapshot.schema.json",
            "commentator-control-projection.schema.json",
            "commentator-view.schema.json",
            "dramaturg-horizon.schema.json",
        )

        schemas = [json.loads((SCHEMAS / name).read_text(encoding="utf-8")) for name in schema_names]
        self.assertTrue(all(schema["additionalProperties"] is False for schema in schemas))
        self.assertTrue(all("schema_version" in schema["properties"] for schema in schemas))
        self.assertTrue(all(schema["properties"]["schema_version"].get("type") == "integer" for schema in schemas))
        self.assertTrue(all(schema["properties"]["schema_version"].get("const") == 1 for schema in schemas))


class SchemaVersionTests(unittest.TestCase):
    def test_history_module_starts_at_its_first_material_revision(self) -> None:
        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.2")

    def test_owner_native_python_ingress_accepts_only_actual_integer_one(self) -> None:
        valid_horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }
        valid_control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )
        valid_snapshot = build_commentator_snapshot([_story_projection()], valid_control)

        self.assertEqual(validate_semantic_event_draft(_semantic_event())["schema_version"], 1)
        self.assertEqual(validate_t0_basis(_t0_basis())["schema_version"], 1)
        self.assertEqual(
            validate_story_projection(_story_projection(), layer="EVENTS")["schema_version"], 1
        )
        self.assertEqual(
            build_commentator_snapshot([_story_projection()], valid_control)["schema_version"], 1
        )
        self.assertEqual(
            filter_commentator_request(valid_snapshot, "player.aria"), [_story_projection()]
        )
        self.assertEqual(validate_dramaturg_horizon(valid_horizon)["schema_version"], 1)

        invalid_versions: tuple[object, ...] = (1.0, True, "1", None, 2)
        for version in invalid_versions:
            with self.subTest(version=version, ingress="semantic event"):
                with self.assertRaises(HistoryContractError):
                    validate_semantic_event_draft({**_semantic_event(), "schema_version": version})
            with self.subTest(version=version, ingress="T0 basis"):
                with self.assertRaises(HistoryContractError):
                    validate_t0_basis({**_t0_basis(), "schema_version": version})
            with self.subTest(version=version, ingress="Story projection"):
                with self.assertRaises(StoryContractError):
                    validate_story_projection(
                        {**_story_projection(), "schema_version": version}, layer="EVENTS"
                    )
            with self.subTest(version=version, ingress="Commentator control"):
                with self.assertRaises(CommentatorContractError):
                    build_commentator_snapshot(
                        [_story_projection()],
                        {"schema_version": version, "controls": {"player.aria": {"story_ids": []}}},
                    )
            with self.subTest(version=version, ingress="Commentator snapshot"):
                with self.assertRaises(CommentatorContractError):
                    filter_commentator_request(
                        {**valid_snapshot, "schema_version": version}, "player.aria"
                    )
            with self.subTest(version=version, ingress="Dramaturg horizon"):
                with self.assertRaises(DramaturgContractError):
                    validate_dramaturg_horizon({**valid_horizon, "schema_version": version})

    def test_draft_2020_12_structural_validation_accepts_numeric_one_point_zero(self) -> None:
        schema = json.loads(
            (SCHEMAS / "runtime-semantic-event-state.schema.json").read_text(encoding="utf-8")
        )

        self.assertTrue(
            Draft202012Validator(schema).is_valid({**_semantic_event(), "schema_version": 1.0})
        )

    def test_owner_local_validators_reject_noninteger_schema_version_one_point_zero(self) -> None:
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "schema_version": 1.0})
        with self.assertRaises(HistoryContractError):
            validate_t0_basis({**_t0_basis(), "schema_version": 1.0})
        with self.assertRaises(StoryContractError):
            validate_story_projection({**_story_projection(), "schema_version": 1.0}, layer="EVENTS")
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {"schema_version": 1.0, "controls": {"player.aria": {"story_ids": ["E000007"]}}},
            )
        snapshot = build_commentator_snapshot(
            [_story_projection()],
            build_commentator_control_projection({"player.aria": {"story_ids": ["E000007"]}}),
        )
        with self.assertRaises(CommentatorContractError):
            filter_commentator_request({**snapshot, "schema_version": 1.0}, "player.aria")
        with self.assertRaises(DramaturgContractError):
            validate_dramaturg_horizon(
                {
                    "schema_version": 1.0,
                    "scope_id": "campaign.main",
                    "generation": 1,
                    "source_basis": ["event.gate_opened"],
                    "entries": [],
                }
            )

    def test_owner_local_validators_reject_unsupported_schema_version_two(self) -> None:
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "schema_version": 2})
        with self.assertRaises(HistoryContractError):
            validate_t0_basis({**_t0_basis(), "schema_version": 2})
        with self.assertRaises(StoryContractError):
            validate_story_projection({**_story_projection(), "schema_version": 2}, layer="EVENTS")
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {"schema_version": 2, "controls": {"player.aria": {"story_ids": ["E000007"]}}},
            )
        snapshot = build_commentator_snapshot(
            [_story_projection()],
            build_commentator_control_projection({"player.aria": {"story_ids": ["E000007"]}}),
        )
        with self.assertRaises(CommentatorContractError):
            filter_commentator_request({**snapshot, "schema_version": 2}, "player.aria")
        with self.assertRaises(DramaturgContractError):
            validate_dramaturg_horizon(
                {
                    "schema_version": 2,
                    "scope_id": "campaign.main",
                    "generation": 1,
                    "source_basis": ["event.gate_opened"],
                    "entries": [],
                }
            )


if __name__ == "__main__":
    unittest.main()
