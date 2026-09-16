from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.actor_continuity import (
    ActorContinuityError,
    apply_actor_delta,
    assess_actor,
    validate_actor_delta,
)
from GAME.TOOLS.continuity_projection import (
    ContinuityProjectionError,
    build_continuity_source_bundle,
    classify_projection_compatibility,
    validate_continuity_projection,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def _schema_registry() -> tuple[Registry, dict[str, object]]:
    registry = Registry()
    schemas: dict[str, object] = {}
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry, schemas


def _actor() -> dict[str, object]:
    return {
        "id": "actor.mara",
        "kind": "world.actor",
        "state_revision": 4,
        "state": {
            "roles": ["actor.nonplayer_character"],
            "continuity": {
                "evolving": {
                    "current_objective": {"statement": "Find who poisoned the well"}
                }
            },
        },
    }


def _accepted_evidence() -> list[dict[str, object]]:
    return [
        {
            "ref": "event.well.001",
            "accepted": True,
            "current": True,
            "authorized_actor_ids": ["actor.mara"],
        }
    ]


def _delta() -> dict[str, object]:
    return {
        "actor_id": "actor.mara",
        "expected_state_revision": 4,
        "purpose": "assessment.react",
        "source_refs": ["event.well.001"],
        "changes": {
            "continuity": {
                "evolving": {
                    "next_intention": {"statement": "Question the miller"}
                }
            }
        },
    }


class NativeActorShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_native_state_and_execution_schemas_are_strict(self) -> None:
        names = (
            "actor-assessment-request.schema.json",
            "actor-delta-draft.schema.json",
            "continuity-projection-candidate.schema.json",
            "world-actor-state.schema.json",
            "world-actor-group-state.schema.json",
            "world-asset-state.schema.json",
            "world-effect-state.schema.json",
        )
        schemas = {name: self.schemas[name] for name in names}

        self.assertTrue(all(schema["additionalProperties"] is False for schema in schemas.values()))
        self.assertEqual(
            schemas["world-effect-state.schema.json"]["required"],
            ["target_id", "lifecycle"],
        )
        self.assertIn("continuity", schemas["world-actor-state.schema.json"]["properties"])
        self.assertNotIn("knowledge", schemas["world-actor-state.schema.json"]["properties"])

    def test_native_shapes_reject_duplicate_authority_and_ambiguous_placement(self) -> None:
        actor_validator = Draft202012Validator(
            self.schemas["world-actor-state.schema.json"], registry=self.registry
        )
        asset_validator = Draft202012Validator(
            self.schemas["world-asset-state.schema.json"], registry=self.registry
        )
        effect_validator = Draft202012Validator(
            self.schemas["world-effect-state.schema.json"], registry=self.registry
        )

        with self.assertRaises(ValidationError):
            actor_validator.validate({"knowledge": {"fact.hidden": "epistemic.known"}})
        with self.assertRaises(ValidationError):
            asset_validator.validate(
                {"owner_actor_id": "actor.mara", "location_id": "location.well"}
            )
        with self.assertRaises(ValidationError):
            effect_validator.validate(
                {
                    "target_id": "actor.mara",
                    "lifecycle": {"state_id": "effect_lifecycle.terminal", "terminal_reason_id": "effect_end.expired"},
                    "scheduled_trigger_state": {"daily_save": {"basis_id": "temporal.metric_deadline"}},
                }
            )

    def test_delta_and_projection_schemas_reject_unmodelled_nested_continuity(self) -> None:
        delta_validator = Draft202012Validator(
            self.schemas["actor-delta-draft.schema.json"], registry=self.registry
        )
        projection_validator = Draft202012Validator(
            self.schemas["continuity-projection-candidate.schema.json"], registry=self.registry
        )
        invalid_delta = _delta()
        invalid_delta["changes"]["continuity"]["evolving"]["hidden_reasoning"] = {
            "statement": "Not a native continuity field"
        }
        with self.assertRaises(ValidationError):
            delta_validator.validate(invalid_delta)

        invalid_projection = {
            "actor_id": "actor.mara",
            "expected_state_revision": 4,
            "source_refs": ["event.well.001"],
            "projection_kind": "continuity.derived",
            "continuity": {"evolving": {"hidden_reasoning": {"statement": "No"}}},
        }
        with self.assertRaises(ValidationError):
            projection_validator.validate(invalid_projection)

    def test_installed_schema_projections_name_only_native_actor_asset_effect_families(self) -> None:
        for name, schema_name in (
            ("actor.schema.yaml", "world_actor"),
            ("asset.schema.yaml", "world_asset"),
            ("effect.schema.yaml", "world_effect"),
        ):
            text = (ROOT / "GAME" / "SCHEMA" / name).read_text(encoding="utf-8")
            self.assertIn(f"schema_name: {schema_name}", text)
            self.assertIn("schema_version: 1", text)
            self.assertIn("strict: true", text)


class ActorAssessmentBehaviorTests(unittest.TestCase):
    def test_assessment_accepts_current_authorized_actor_evidence(self) -> None:
        assessment = assess_actor(
            {
                "actor": _actor(),
                "purpose": "assessment.react",
                "source_evidence": _accepted_evidence(),
                "delta": _delta(),
            }
        )

        self.assertEqual(assessment["disposition"], "assessment.delta")
        self.assertEqual(assessment["actor_id"], "actor.mara")
        self.assertEqual(assessment["source_refs"], ["event.well.001"])

    def test_assessment_accepts_no_change_without_creating_a_delta(self) -> None:
        assessment = assess_actor(
            {
                "actor": _actor(),
                "purpose": "assessment.reflect",
                "source_evidence": _accepted_evidence(),
                "delta": None,
            }
        )

        self.assertEqual(assessment["disposition"], "assessment.no_change")
        self.assertNotIn("delta", assessment)

    def test_assessment_rejects_stale_or_conflicting_identity(self) -> None:
        stale = _accepted_evidence()
        stale[0]["current"] = False
        with self.assertRaisesRegex(ActorContinuityError, "stale"):
            assess_actor(
                {
                    "actor": _actor(),
                    "purpose": "assessment.react",
                    "source_evidence": stale,
                    "delta": _delta(),
                }
            )

        conflict = _delta()
        conflict["actor_id"] = "actor.other"
        with self.assertRaisesRegex(ActorContinuityError, "identity"):
            validate_actor_delta(conflict, _actor(), _accepted_evidence())

    def test_assessment_rejects_unmodelled_native_state_and_malformed_player_role(self) -> None:
        unmodelled = _actor()
        unmodelled["state"]["hidden_authority"] = {"statement": "Do not persist this"}
        with self.assertRaisesRegex(ActorContinuityError, "unsupported field"):
            assess_actor(
                {
                    "actor": unmodelled,
                    "purpose": "assessment.reflect",
                    "source_evidence": _accepted_evidence(),
                    "delta": None,
                }
            )

        malformed_role = _actor()
        malformed_role["state"]["roles"] = "actor.player_character"
        with self.assertRaisesRegex(ActorContinuityError, "roles"):
            assess_actor(
                {
                    "actor": malformed_role,
                    "purpose": "assessment.reflect",
                    "source_evidence": _accepted_evidence(),
                    "delta": None,
                }
            )

    def test_assessment_rejects_malformed_declared_hp_state(self) -> None:
        malformed_hp = _actor()
        malformed_hp["state"].update(
            {
                "hp": {"current": 5},
                "life_state_id": "life.active",
                "life_state_policy_id": "life_policy.dnd2024.character_like",
            }
        )

        with self.assertRaisesRegex(ActorContinuityError, "hp"):
            assess_actor(
                {
                    "actor": malformed_hp,
                    "purpose": "assessment.reflect",
                    "source_evidence": _accepted_evidence(),
                    "delta": None,
                }
            )

    def test_assessment_validates_each_declared_native_state_field(self) -> None:
        malformed_states = (
            {"name": {"en": ""}},
            {"concept": ""},
            {"location_id": "not a native id"},
            {"build": {"class_progression": []}},
            {"abilities": {"ability.strength": {"base": -1}}},
            {
                "hp": {"current": "five", "maximum_base": 5},
                "life_state_id": "life.active",
                "life_state_policy_id": "life_policy.dnd2024.character_like",
            },
            {"life_state_id": "life.unknown", "life_state_policy_id": "life_policy.dnd2024.character_like"},
            {"life_state_id": [], "life_state_policy_id": "life_policy.dnd2024.character_like"},
            {"life_state_id": "life.active", "life_state_policy_id": "life_policy.invalid"},
            {
                "hp": {"current": 0, "maximum_base": 5},
                "life_state_id": "life.dying",
                "life_state_policy_id": "life_policy.dnd2024.character_like",
                "life_state_progress": {"death_saves": {"successes": 3, "failures": 0}},
            },
            {"resources": {"resource.inspiration": {"current": -1}}},
            {
                "resources": {
                    "resource.inspiration": {
                        "current": 1,
                        "recovery_binding": {"basis_id": []},
                    }
                }
            },
            {"details": []},
        )
        for changes in malformed_states:
            with self.subTest(changes=changes):
                actor = _actor()
                actor["state"].update(changes)
                with self.assertRaises(ActorContinuityError):
                    assess_actor(
                        {
                            "actor": actor,
                            "purpose": "assessment.reflect",
                            "source_evidence": _accepted_evidence(),
                            "delta": None,
                        }
                    )

    def test_assessment_accepts_complete_declared_native_state(self) -> None:
        actor = _actor()
        actor["state"].update(
            {
                "name": {"en": "Mara"},
                "concept": "Village guardian",
                "location_id": "location.well",
                "build": {"class_progression": [{"class_id": "class.fighter", "level": 1}]},
                "abilities": {"ability.strength": {"base": 15, "adjustment": 1}},
                "hp": {"current": 12, "maximum_base": 12},
                "life_state_id": "life.active",
                "life_state_policy_id": "life_policy.dnd2024.character_like",
                "resources": {
                    "resource.inspiration": {
                        "current": 1,
                        "recovery_binding": {
                            "basis_id": "temporal.semantic_boundary",
                            "boundary_id": "boundary.long_rest",
                            "anchor_id": "rest.001",
                        },
                    }
                },
                "details": {"description": "A watchful villager."},
            }
        )

        result = assess_actor(
            {
                "actor": actor,
                "purpose": "assessment.reflect",
                "source_evidence": _accepted_evidence(),
                "delta": None,
            }
        )

        self.assertEqual(result["disposition"], "assessment.no_change")

class ActorMutationIntegrationTests(unittest.TestCase):
    def test_accepted_delta_advances_only_the_native_actor_state(self) -> None:
        mutated = apply_actor_delta(_actor(), _delta(), _accepted_evidence())

        self.assertEqual(mutated["state_revision"], 5)
        evolving = mutated["state"]["continuity"]["evolving"]
        self.assertEqual(evolving["next_intention"]["statement"], "Question the miller")
        self.assertNotIn("knowledge", mutated["state"])

    def test_mutation_rejects_stale_input_and_knowledge_or_inventory_aliases(self) -> None:
        stale = _delta()
        stale["expected_state_revision"] = 3
        with self.assertRaisesRegex(ActorContinuityError, "stale"):
            apply_actor_delta(_actor(), stale, _accepted_evidence())

        forbidden = _delta()
        forbidden["changes"] = {"knowledge": {"fact.hidden": "epistemic.known"}}
        with self.assertRaisesRegex(ActorContinuityError, "native Actor continuity"):
            apply_actor_delta(_actor(), forbidden, _accepted_evidence())

    def test_mutation_does_not_author_player_controlled_actor_continuity(self) -> None:
        player_actor = _actor()
        player_actor["state"]["roles"] = ["actor.player_character"]

        with self.assertRaisesRegex(ActorContinuityError, "player-controlled"):
            apply_actor_delta(player_actor, _delta(), _accepted_evidence())

    def test_mutation_rejects_unmodelled_nested_continuity_fields(self) -> None:
        unmodelled = _delta()
        unmodelled["changes"]["continuity"]["evolving"]["hidden_reasoning"] = {
            "statement": "Invent a private plan graph"
        }

        with self.assertRaisesRegex(ActorContinuityError, "unsupported field"):
            apply_actor_delta(_actor(), unmodelled, _accepted_evidence())

    def test_mutation_rejects_unmodelled_delta_envelope_fields(self) -> None:
        unmodelled = _delta()
        unmodelled["replacement_state"] = {"roles": ["actor.player_character"]}

        with self.assertRaisesRegex(ActorContinuityError, "unsupported field"):
            apply_actor_delta(_actor(), unmodelled, _accepted_evidence())

    def test_mutation_rejects_unused_invalid_foundation_transition(self) -> None:
        invalid_transition = _delta()
        invalid_transition["foundation_transition"] = "foundation.implicit"

        with self.assertRaisesRegex(ActorContinuityError, "foundation_transition"):
            apply_actor_delta(_actor(), invalid_transition, _accepted_evidence())


class ContinuitySourceAdmissionTests(unittest.TestCase):
    def test_source_bundle_rejects_sparse_actor_without_continuity(self) -> None:
        for continuity in (None, {}):
            with self.subTest(continuity=continuity):
                actor = _actor()
                if continuity is None:
                    del actor["state"]["continuity"]
                else:
                    actor["state"]["continuity"] = continuity

                with self.assertRaisesRegex(ContinuityProjectionError, "continuity"):
                    build_continuity_source_bundle(actor, _accepted_evidence())

    def test_projection_requires_current_native_actor_sources(self) -> None:
        bundle = build_continuity_source_bundle(_actor(), _accepted_evidence())
        candidate = {
            "actor_id": "actor.mara",
            "expected_state_revision": 4,
            "source_refs": ["event.well.001"],
            "projection_kind": "continuity.derived",
            "continuity": _actor()["state"]["continuity"],
        }

        projection = validate_continuity_projection(candidate, bundle)
        self.assertEqual(classify_projection_compatibility(projection, bundle), "compatible")

    def test_projection_accepts_only_retained_native_values_and_native_ids(self) -> None:
        actor = _actor()
        actor["state"]["continuity"]["foundation"] = {
            "values": [{"statement": "Protect the village"}]
        }
        bundle = build_continuity_source_bundle(actor, _accepted_evidence())
        retained_subset = {
            "actor_id": "actor.mara",
            "expected_state_revision": 4,
            "source_refs": ["event.well.001"],
            "projection_kind": "continuity.derived",
            "continuity": {
                "evolving": {
                    "current_objective": {"statement": "Find who poisoned the well"}
                }
            },
        }
        self.assertEqual(
            classify_projection_compatibility(retained_subset, bundle), "compatible"
        )

        divergent = deepcopy(retained_subset)
        divergent["continuity"]["evolving"]["current_objective"]["statement"] = "Invent a new goal"
        with self.assertRaisesRegex(ContinuityProjectionError, "diverges"):
            validate_continuity_projection(divergent, bundle)

        invalid_ref = deepcopy(retained_subset)
        invalid_ref["source_refs"] = ["not a native id"]
        with self.assertRaisesRegex(ContinuityProjectionError, "native id"):
            validate_continuity_projection(invalid_ref, bundle)

        invalid_evidence = _accepted_evidence()
        invalid_evidence[0]["ref"] = "not a native id"
        with self.assertRaisesRegex(ContinuityProjectionError, "native id"):
            build_continuity_source_bundle(actor, invalid_evidence)

    def test_projection_rejects_provisional_or_non_native_authority(self) -> None:
        provisional = _actor()
        provisional["state_revision"] = 4
        provisional["provisional"] = True
        with self.assertRaisesRegex(ContinuityProjectionError, "provisional"):
            build_continuity_source_bundle(provisional, _accepted_evidence())

        bundle = build_continuity_source_bundle(_actor(), _accepted_evidence())
        candidate = {
            "actor_id": "actor.mara",
            "expected_state_revision": 4,
            "source_refs": ["event.well.001"],
            "projection_kind": "continuity.derived",
            "continuity": {"knowledge": {"fact.hidden": "epistemic.known"}},
        }
        with self.assertRaisesRegex(ContinuityProjectionError, "knowledge"):
            validate_continuity_projection(candidate, bundle)

    def test_projection_rejects_unmodelled_source_bundle_continuity(self) -> None:
        bundle = build_continuity_source_bundle(_actor(), _accepted_evidence())
        bundle["continuity"]["evolving"]["hidden_reasoning"] = {
            "statement": "This must not become projection authority"
        }
        candidate = {
            "actor_id": "actor.mara",
            "expected_state_revision": 4,
            "source_refs": ["event.well.001"],
            "projection_kind": "continuity.derived",
            "continuity": _actor()["state"]["continuity"],
        }

        with self.assertRaisesRegex(ContinuityProjectionError, "unsupported field"):
            validate_continuity_projection(candidate, bundle)


class LegacyEntityProjectionTests(unittest.TestCase):
    def test_legacy_entity_shapes_remain_rejected_as_native_inputs_while_t02_evidence_survives(self) -> None:
        information = (ROOT / "GAME" / "CORE" / "INFORMATION.md").read_text(encoding="utf-8")
        self.assertIn("legacy embedded PC/NPC/Faction knowledge arrays", information)

        legacy_actor = {
            "id": "actor.mara",
            "kind": "player_character",
            "state_revision": 4,
            "knowledge": {"known_fact_ids": ["fact.hidden"]},
        }
        with self.assertRaisesRegex(ActorContinuityError, "world.actor"):
            assess_actor(
                {
                    "actor": legacy_actor,
                    "purpose": "assessment.react",
                    "source_evidence": _accepted_evidence(),
                    "delta": _delta(),
                }
            )


class ProvisionalActorConsumerTests(unittest.TestCase):
    def test_provisional_actor_cannot_be_promoted_by_continuity_projection(self) -> None:
        actor = _actor()
        actor["provisional"] = True
        with self.assertRaisesRegex(ContinuityProjectionError, "provisional"):
            build_continuity_source_bundle(actor, _accepted_evidence())


if __name__ == "__main__":
    unittest.main()
