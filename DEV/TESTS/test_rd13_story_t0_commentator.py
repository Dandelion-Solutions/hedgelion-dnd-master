from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

from GAME.TOOLS import context_runtime, history as history_module
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
    BoundNativeHistoryRuntime,
    FRAMEWORK_MODULE_VERSION,
    HistoryContractError,
    append_semantic_event,
    build_t0_basis,
    recover_native_history,
    read_native_history,
    validate_semantic_event_draft,
    validate_t0_basis,
)
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveRouting,
    build_live_ref,
    build_live_route,
    derive_live_epoch_id,
)
from GAME.TOOLS.policy_basis import PinnedCampaign
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


def _source_window(
    events: tuple[dict[str, object], ...] = (_semantic_event(),),
    *,
    campaign_id: str = "campaign.main",
    origin: str = "LOCAL",
    source_revision: str = "a" * 40,
    lower_exclusive: int | None = 6,
    upper: int | None = 7,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "source_domain": "campaign.semantic_events@S",
        "semantic_contract_generation": 1,
        "campaign_id": campaign_id,
        "origin": origin,
        "lane": "evt",
        "source_revision": source_revision,
        "lower_exclusive": f"evt:{lower_exclusive}" if lower_exclusive is not None else None,
        "upper": f"evt:{upper}" if upper is not None else None,
        "enumeration_representation": "runtime.semantic_event.evt.v1",
        "owner_contracts": [{"family": "runtime.semantic_event", "schema_version": 1}],
        "entries": [
            {
                "candidate_id": json.dumps([event["event_id"]], separators=(",", ":")),
                "ordinal": event["semantic_order"],
                "event": deepcopy(event),
            }
            for event in events
        ],
        "interval_complete": True,
    }


class _RepositoryForNativeHistory:
    def __init__(self, window: dict[str, object]) -> None:
        self.window = window
        self.paths: list[str] = []

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        return PinnedCampaign(campaign_id, "a" * 40, "b" * 40)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        del pinned
        self.paths.append(path)
        if path != "LOG/SEMANTIC_EVENTS":
            raise KeyError(path)
        return deepcopy(self.window)


def _live_source_for_native_history() -> LiveEnvelope:
    claims = (LiveClaim.exact_owner("world.actor", "actor.guard"),)
    opening_revision = "b" * 40
    campaign_id = "campaign.main"
    scene_id = "scene.gate"
    epoch_id = derive_live_epoch_id(campaign_id, scene_id, opening_revision, claims)
    return LiveEnvelope(
        campaign_id=campaign_id,
        scene_id=scene_id,
        epoch_id=epoch_id,
        source_ref=build_live_ref(campaign_id, scene_id, epoch_id),
        source_revision="c" * 40,
        claims=claims,
        opening_campaign_revision=opening_revision,
    )


def _history_from_context_runtime(
    repository: object,
    *,
    current_routing: LiveRouting | None,
    selected_live_reader: object | None = None,
) -> BoundNativeHistoryRuntime:
    """Use the existing host composition route in test fixtures only."""

    return context_runtime._compose_context_runtime(
        repository,
        live_route=current_routing,
        selected_live_reader=selected_live_reader,
    ).native_history_runtime


class _SelectedLiveReaderForNativeHistory:
    def __init__(self, window: dict[str, object]) -> None:
        self.window = window
        self.calls = 0

    def read_selected_live_source(self, route: LiveRouting, source: LiveEnvelope) -> object:
        del route, source
        self.calls += 1
        return deepcopy(self.window)


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
    def test_history_composition_is_owned_by_the_bound_context_runtime(self) -> None:
        repository = _RepositoryForNativeHistory(_source_window())
        context = context_runtime._compose_context_runtime(repository)

        self.assertIsInstance(context.native_history_runtime, BoundNativeHistoryRuntime)

    def test_history_does_not_expose_a_caller_replaceable_composition_factory(self) -> None:
        self.assertNotIn("_compose_native_history_runtime", vars(history_module))

    def test_public_composition_and_forged_runtime_cannot_mint_history(self) -> None:
        self.assertNotIn("bind_native_history_runtime", vars(history_module))
        forged_runtime = object.__new__(BoundNativeHistoryRuntime)

        with self.assertRaises(HistoryContractError):
            read_native_history(forged_runtime, "campaign.main")

    def test_trusted_host_binding_reads_a_bounded_local_window(self) -> None:
        repository = _RepositoryForNativeHistory(_source_window())
        runtime = _history_from_context_runtime(repository, current_routing=None)

        self.assertIsInstance(runtime, BoundNativeHistoryRuntime)
        publication = runtime.read("campaign.main")

        self.assertEqual(publication.source_domain, "campaign.semantic_events@S")
        self.assertEqual(publication.lane, "evt")
        self.assertEqual(publication.origin, "LOCAL")
        self.assertEqual(publication.events[0].admission_ordinal, 7)
        self.assertEqual(publication.events[0].candidate_id, '["event.gate_opened"]')
        self.assertEqual(repository.paths, ["LOG/SEMANTIC_EVENTS"])

    def test_caller_shaped_event_and_history_list_cannot_mint_accepted_history(self) -> None:
        with self.assertRaises(HistoryContractError):
            append_semantic_event([], _semantic_event())
        with self.assertRaises(HistoryContractError):
            recover_native_history([_semantic_event()])

    def test_history_rejects_duplicate_or_noncontiguous_window_evidence(self) -> None:
        duplicate = _source_window(
            (
                _semantic_event(),
                dict(_semantic_event(), event_id="event.other", semantic_order=7),
            ),
            upper=7,
        )
        noncontiguous = _source_window(
            (dict(_semantic_event(), semantic_order=8),),
            lower_exclusive=6,
            upper=8,
        )

        for window in (duplicate, noncontiguous):
            with self.subTest(window=window):
                with self.assertRaises(HistoryContractError):
                    _history_from_context_runtime(
                        _RepositoryForNativeHistory(window), current_routing=None
                    ).read("campaign.main")

    def test_empty_evt_window_is_bounded_without_a_dummy_event(self) -> None:
        publication = _history_from_context_runtime(
            _RepositoryForNativeHistory(_source_window(events=(), lower_exclusive=None, upper=None)),
            current_routing=None,
        ).read("campaign.main")

        self.assertEqual(publication.events, ())
        self.assertIsNone(publication.currentness.upper)

    def test_history_rejects_wrong_origin_revision_and_provenance(self) -> None:
        cases = (
            _source_window(origin="LIVE:epoch-1"),
            _source_window(source_revision="d" * 40),
            {
                **_source_window(),
                "entries": [
                    {
                        "candidate_id": '["event.other"]',
                        "ordinal": 7,
                        "event": _semantic_event(),
                    }
                ],
            },
        )
        for window in cases:
            with self.subTest(window=window):
                with self.assertRaises(HistoryContractError):
                    _history_from_context_runtime(
                        _RepositoryForNativeHistory(window), current_routing=None
                    ).read("campaign.main")

    def test_selected_live_read_is_route_bound_and_never_falls_back_to_campaign(self) -> None:
        source = _live_source_for_native_history()
        route = build_live_route(source.campaign_id, (source,))
        live_reader = _SelectedLiveReaderForNativeHistory(
            _source_window(
                origin=f"LIVE:{source.epoch_id}",
                source_revision=source.source_revision,
            )
        )
        runtime = _history_from_context_runtime(
            _RepositoryForNativeHistory(_source_window()),
            current_routing=route,
            selected_live_reader=live_reader,
        )

        publication = runtime.read("campaign.main", origin=f"LIVE:{source.epoch_id}")

        self.assertEqual(publication.origin, f"LIVE:{source.epoch_id}")
        self.assertEqual(publication.source_revision, source.source_revision)
        self.assertEqual(live_reader.calls, 1)

        with self.assertRaises(HistoryContractError):
            runtime.read("campaign.main", origin="LIVE:missing-epoch")
        self.assertEqual(live_reader.calls, 1)

    def test_recovery_reloads_the_bound_window_without_story_or_narration_fallback(self) -> None:
        repository = _RepositoryForNativeHistory(_source_window())
        runtime = _history_from_context_runtime(repository, current_routing=None)

        recovered = recover_native_history(runtime, "campaign.main")

        self.assertEqual(recovered.to_mapping(), runtime.read("campaign.main").to_mapping())
        story_window = _source_window()
        story_window["entries"] = [{"story_id": "E000007", "content": {"body": "fiction"}}]
        with self.assertRaises(HistoryContractError):
            _history_from_context_runtime(
                _RepositoryForNativeHistory(story_window), current_routing=None
            ).read("campaign.main")

    def test_only_validated_semantic_events_enter_native_history(self) -> None:
        history = _history_from_context_runtime(
            _RepositoryForNativeHistory(_source_window()), current_routing=None
        ).read("campaign.main")

        self.assertEqual(history.events[0].as_mapping(), _semantic_event())
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "provenance_refs": []})


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
        publication = _history_from_context_runtime(
            _RepositoryForNativeHistory(_source_window()), current_routing=None
        ).read("campaign.main")
        history = [event.as_mapping() for event in publication.events]
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
    def test_history_module_uses_current_framework_revision(self) -> None:
        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.8")

    def test_native_history_schemas_validate_only_the_bound_evidence_shape(self) -> None:
        publication = _history_from_context_runtime(
            _RepositoryForNativeHistory(_source_window()), current_routing=None
        ).read("campaign.main")
        currentness_schema = json.loads(
            (SCHEMAS / "native-history-currentness.schema.json").read_text(encoding="utf-8")
        )
        publication_schema = json.loads(
            (SCHEMAS / "native-history-publication.schema.json").read_text(encoding="utf-8")
        )

        self.assertTrue(Draft202012Validator(currentness_schema).is_valid(publication.currentness.as_mapping()))
        self.assertTrue(Draft202012Validator(publication_schema).is_valid(publication.to_mapping()))
        forged = publication.to_mapping()
        forged["events"][0]["provenance"]["origin"] = "FORGED"
        self.assertFalse(Draft202012Validator(publication_schema).is_valid(forged))

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
