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
    HistoryContractError,
    append_semantic_event,
    build_t0_basis,
    validate_semantic_event_draft,
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
    def test_only_validated_semantic_events_enter_native_history(self) -> None:
        history = append_semantic_event([], _semantic_event())

        self.assertEqual(history, [_semantic_event()])
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
        history = append_semantic_event([], _semantic_event())
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
