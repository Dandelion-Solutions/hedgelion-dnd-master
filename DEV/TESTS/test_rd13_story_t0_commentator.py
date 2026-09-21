from __future__ import annotations

import json
import unittest
from copy import deepcopy
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
    HistoryContractError,
    NativeHistoryCurrentness,
    NativeHistoryPublication,
    NativeSemanticEvent,
    append_semantic_event,
    build_t0_basis,
    issue_native_history_currentness,
    issue_native_semantic_event,
    publish_native_history,
    read_native_history,
    recover_native_history,
    validate_semantic_event_draft,
    validate_native_history,
    validate_t0_basis,
)
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


class _NativeHistoryOwner:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def read_accepted_native_history(self, campaign_id: str) -> object:
        if campaign_id != self._payload["campaign_id"]:
            raise AssertionError("test owner received the wrong campaign")
        return deepcopy(self._payload)


def _native_history(
    events: tuple[dict[str, object], ...] | None = None,
    *,
    origin: str = "LOCAL",
    source_revision: str = "0" * 40,
) -> object:
    source_events = events if events is not None else (_semantic_event(),)
    return read_native_history(
        _NativeHistoryOwner(
            {
                "campaign_id": "campaign.main",
                "origin": origin,
                "source_revision": source_revision,
                "events": list(source_events),
            }
        ),
        "campaign.main",
    )


def _native_currentness(
    events: tuple[dict[str, object], ...] | None = None,
    *,
    origin: str = "LOCAL",
    source_revision: str = "0" * 40,
) -> object:
    return _native_history(events, origin=origin, source_revision=source_revision).currentness  # type: ignore[attr-defined]


def _accepted_semantic_event(
    event: dict[str, object] | None = None, *, currentness: object | None = None
) -> object:
    del currentness
    source = _native_history((event or _semantic_event(),))
    return source.events[0]  # type: ignore[attr-defined]


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
    def test_public_raw_issuance_paths_cannot_mint_owner_accepted_history(self) -> None:
        with self.assertRaises(HistoryContractError):
            issue_native_history_currentness(
                campaign_id="campaign.main", origin="LOCAL", source_revision="0" * 40
            )
        with self.assertRaises(HistoryContractError):
            issue_native_semantic_event(_semantic_event(), currentness=_native_currentness())
        with self.assertRaises(HistoryContractError):
            read_native_history({"campaign_id": "campaign.main"}, "campaign.main")  # type: ignore[arg-type]

        owner_publication = _native_history((_semantic_event(),))
        currentness = owner_publication.currentness
        self.assertEqual(owner_publication.events[0].as_mapping(), _semantic_event())
        with self.assertRaises(HistoryContractError):
            NativeHistoryCurrentness(
                campaign_id="campaign.main",
                origin="LOCAL",
                source_revision="0" * 40,
                accepted_event_fingerprints={},
            )
        with self.assertRaises(HistoryContractError):
            NativeSemanticEvent(event=_semantic_event(), currentness=currentness)
        with self.assertRaises(HistoryContractError):
            NativeHistoryPublication(currentness=currentness, events=())
        with self.assertRaises(HistoryContractError):
            publish_native_history((), _semantic_event(), currentness=currentness)
        with self.assertRaises(HistoryContractError):
            recover_native_history({}, currentness={})  # type: ignore[arg-type]
        with self.assertRaises(HistoryContractError):
            validate_native_history({}, currentness={})  # type: ignore[arg-type]

    def test_only_validated_semantic_events_enter_native_history(self) -> None:
        currentness = _native_currentness()
        history = append_semantic_event(
            (), _accepted_semantic_event(currentness=currentness), currentness=currentness  # type: ignore[arg-type]
        )

        self.assertEqual(history.events[0].as_mapping(), _semantic_event())
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "provenance_refs": []})

    def test_caller_shaped_semantic_event_cannot_mint_accepted_history(self) -> None:
        currentness = _native_currentness()

        with self.assertRaises(HistoryContractError):
            append_semantic_event((), _semantic_event(), currentness=currentness)

    def test_native_publication_rejects_duplicate_identity_order_and_currentness(self) -> None:
        source = _native_history(
            (_semantic_event(), dict(_semantic_event(), event_id="event.other", semantic_order=8))
        )
        currentness = source.currentness
        accepted = source.events[0]
        publication = append_semantic_event((), accepted, currentness=currentness)

        with self.assertRaises(HistoryContractError):
            append_semantic_event(publication, accepted, currentness=currentness)

        order_publication = append_semantic_event((), source.events[1], currentness=currentness)
        with self.assertRaises(HistoryContractError):
            append_semantic_event(order_publication, accepted, currentness=currentness)

        other_source = _native_history(
            (dict(_semantic_event(), event_id="event.foreign"),), source_revision="1" * 40
        )
        with self.assertRaises(HistoryContractError):
            append_semantic_event(
                publication,
                other_source.events[0],
                currentness=currentness,
            )

        same_revision_source = _native_history(
            (
                dict(
                    _semantic_event(), event_id="event.same_revision_foreign", semantic_order=8
                ),
            )
        )
        with self.assertRaises(HistoryContractError):
            append_semantic_event(
                publication,
                same_revision_source.events[0],
                currentness=currentness,
            )

    def test_interruption_recovery_preserves_identity_provenance_and_semantic_order(self) -> None:
        source = _native_history(
            (
                _semantic_event(),
                dict(_semantic_event(), event_id="event.gate_closed", semantic_order=8),
            ),
            origin="LIVE:epoch-1",
        )
        currentness = source.currentness
        first, second = source.events
        publication = append_semantic_event(
            append_semantic_event((), first, currentness=currentness),
            second,
            currentness=currentness,
        )

        recovered = recover_native_history(publication.to_mapping(), currentness=currentness)

        self.assertEqual(recovered.to_mapping(), publication.to_mapping())
        self.assertEqual(
            [event["event_id"] for event in recovered.events],
            ["event.gate_opened", "event.gate_closed"],
        )
        self.assertEqual(recovered.origin, "LIVE:epoch-1")

    def test_native_history_recovery_cannot_reconstruct_from_story_or_narration(self) -> None:
        currentness = _native_currentness()

        for candidate in (_story_projection(), {"body": "The guard opened the gate."}):
            with self.subTest(candidate=candidate):
                with self.assertRaises(HistoryContractError):
                    recover_native_history(candidate, currentness=currentness)

    def test_recovery_rejects_a_caller_forged_event_under_the_same_currentness(self) -> None:
        currentness = _native_currentness((_semantic_event(),))
        publication = append_semantic_event(
            (), _accepted_semantic_event(currentness=currentness), currentness=currentness
        )
        forged = publication.to_mapping()
        forged_event = forged["events"][0]["event"]
        forged_event["semantic_delta"] = {"gate": "forged"}

        with self.assertRaises(HistoryContractError):
            recover_native_history(forged, currentness=currentness)

    def test_recovery_rejects_malformed_provenance_ref_shapes(self) -> None:
        event = dict(_semantic_event(), provenance_refs=["x"])
        publication = _native_history((event,))
        currentness = publication.currentness

        malformed_values: tuple[object, ...] = (
            "x",
            None,
            1,
            {"x": 1},
            ("x",),
            ["x", "x"],
            [1],
        )
        for location in ("event", "provenance"):
            for malformed in malformed_values:
                with self.subTest(location=location, malformed=malformed):
                    candidate = publication.to_mapping()
                    candidate["events"][0][location]["provenance_refs"] = malformed
                    with self.assertRaises(HistoryContractError):
                        recover_native_history(candidate, currentness=currentness)

    def test_recovery_rejects_reordered_provenance_refs(self) -> None:
        event = dict(_semantic_event(), provenance_refs=["first", "second"])
        publication = _native_history((event,))
        currentness = publication.currentness
        candidate = publication.to_mapping()
        candidate["events"][0]["provenance"]["provenance_refs"] = ["second", "first"]

        with self.assertRaises(HistoryContractError):
            recover_native_history(candidate, currentness=currentness)

    def test_recovery_rejects_campaign_origin_and_source_revision_mismatch(self) -> None:
        currentness = _native_currentness()
        publication = append_semantic_event(
            (), _accepted_semantic_event(currentness=currentness), currentness=currentness  # type: ignore[arg-type]
        )
        for field, value in (
            ("campaign_id", "campaign.other"),
            ("origin", "LIVE:epoch-2"),
            ("source_revision", "1" * 40),
        ):
            with self.subTest(field=field):
                candidate = publication.to_mapping()
                candidate[field] = value
                with self.assertRaises(HistoryContractError):
                    recover_native_history(candidate, currentness=currentness)


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
        currentness = _native_currentness()
        history = append_semantic_event(
            (), _accepted_semantic_event(currentness=currentness), currentness=currentness  # type: ignore[arg-type]
        )
        bundle = build_story_source_bundle(
            [event.as_mapping() for event in history.events], layer="EVENTS"
        )
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
            "native-history-currentness.schema.json",
            "native-history-publication.schema.json",
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

    def test_native_history_publication_mapping_is_structurally_valid(self) -> None:
        currentness = _native_currentness()
        publication = append_semantic_event(
            (), _accepted_semantic_event(currentness=currentness), currentness=currentness  # type: ignore[arg-type]
        )
        currentness_schema = json.loads(
            (SCHEMAS / "native-history-currentness.schema.json").read_text(encoding="utf-8")
        )
        schema = json.loads((SCHEMAS / "native-history-publication.schema.json").read_text(encoding="utf-8"))

        self.assertTrue(Draft202012Validator(currentness_schema).is_valid(currentness.as_mapping()))  # type: ignore[attr-defined]
        self.assertTrue(Draft202012Validator(schema).is_valid(publication.to_mapping()))


class SchemaVersionTests(unittest.TestCase):
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
