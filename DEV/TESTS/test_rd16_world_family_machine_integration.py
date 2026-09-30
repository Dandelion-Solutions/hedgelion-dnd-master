import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
PLAYER_COLLABORATION_DELTA = (
    ROOT / "DEV" / "TESTS" / "fixtures" / "w04_player_collaboration_delta.json"
)
W05_WORLD_MACHINE_INPUTS = (
    ROOT / "DEV" / "TESTS" / "fixtures" / "w05_world_machine_owner_inputs.json"
)
PLAYER_WORLD_SCHEMA_NAME = "world-player-state.schema.json"
PLAYER_WORLD_SCHEMA = SCHEMAS / PLAYER_WORLD_SCHEMA_NAME

QUIET_WORLD_SCHEMA_NAMES = {
    "world.location": "world-location-state.schema.json",
    "world.connection": "world-connection-state.schema.json",
    "world.zone": "world-zone-state.schema.json",
    "world.organization": "world-organization-state.schema.json",
    "world.contract": "world-contract-state.schema.json",
    "world.mission": "world-mission-state.schema.json",
    "world.scene": "world-scene-state.schema.json",
    "world.encounter": "world-encounter-state.schema.json",
    "world.hazard": "world-hazard-state.schema.json",
}

CONSUMED_OWNER_SCHEMA_NAMES = {
    "world.actor": "world-actor-state.schema.json",
    "world.actor_group": "world-actor-group-state.schema.json",
    "world.asset": "world-asset-state.schema.json",
    "world.effect": "world-effect-state.schema.json",
    "world.lore_fact": "world-lore-fact-state.schema.json",
    "world.knowledge": "world-knowledge-state.schema.json",
    "world.thread": "world-thread-state.schema.json",
}

CANONICAL_WORLD_FAMILIES = frozenset(
    {
        *QUIET_WORLD_SCHEMA_NAMES,
        *CONSUMED_OWNER_SCHEMA_NAMES,
        "world.player",
    }
)

CANONICAL_RUNTIME_FAMILIES = frozenset(
    {
        "runtime.session",
        "runtime.message",
        "runtime.interaction",
        "runtime.procedure",
        "runtime.intent_plan",
        "runtime.command",
        "runtime.resolution",
        "runtime.continuation",
        "runtime.mechanical_event",
        "runtime.semantic_event",
        "runtime.resolution_trace",
        "runtime.disclosure",
        "runtime.collaboration_obligation",
        "runtime.checkpoint",
        "runtime.id_allocator",
        "runtime.maintenance_audit",
        "runtime.catalog_gap_report",
    }
)

EXPECTED_WORLD_SCHEMA_DISPATCH = {
    **QUIET_WORLD_SCHEMA_NAMES,
    **CONSUMED_OWNER_SCHEMA_NAMES,
    "world.player": PLAYER_WORLD_SCHEMA_NAME,
}

VALID_QUIET_STATES = {
    "world.location": {"name": "Market square"},
    "world.connection": {
        "from_location_id": "location.market",
        "to_location_id": "location.bridge",
    },
    "world.zone": {"location_id": "location.market", "name": "Fountain plaza"},
    "world.organization": {"name": "Merchants guild"},
    "world.contract": {
        "party_ids": ["actor.mara", "organization.guild"],
        "terms": {},
        "status": {},
    },
    "world.mission": {"name": "Find the courier", "status": {}},
    "world.scene": {"name": "Market morning"},
    "world.encounter": {"participant_ids": ["actor.mara"], "status": {}},
    "world.hazard": {"status": {}},
}

VALID_CONTRACT_DEADLINE = {
    "basis_id": "temporal.metric_deadline",
    "context_id": "scene.market",
    "anchor_value": 12,
    "deadline_value": 15,
    "unit_id": "unit.day",
}

MALFORMED_CONTRACT_DEADLINE = {
    **VALID_CONTRACT_DEADLINE,
    "anchor_value": "twelve",
}


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def load_w05_world_machine_inputs(test_case: unittest.TestCase) -> dict[str, object]:
    test_case.assertTrue(
        W05_WORLD_MACHINE_INPUTS.is_file(),
        "W05.T01 must publish owner-local schema dispatch inputs",
    )
    return json.loads(W05_WORLD_MACHINE_INPUTS.read_text(encoding="utf-8"))


def local_schema_registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


class WorldStateSchemaCoverageTests(unittest.TestCase):
    def test_quiet_world_family_schemas_are_present_and_strict(self) -> None:
        for family, name in QUIET_WORLD_SCHEMA_NAMES.items():
            with self.subTest(family=family):
                schema = load_schema(name)
                self.assertEqual(schema["title"], f"HDM {family} state")
                self.assertIs(schema["additionalProperties"], False)
                Draft202012Validator(schema).validate(VALID_QUIET_STATES[family])

    def test_quiet_world_family_schemas_reject_missing_state_and_new_authority(self) -> None:
        for family, name in QUIET_WORLD_SCHEMA_NAMES.items():
            with self.subTest(
                family=family, invalid="missing-required-state"
            ), self.assertRaises(ValidationError):
                Draft202012Validator(load_schema(name)).validate({})
            with self.subTest(family=family, invalid="unmodelled-state-authority"):
                invalid = dict(VALID_QUIET_STATES[family], knowledge={"fact.secret": "known"})
                with self.assertRaises(ValidationError):
                    Draft202012Validator(load_schema(name)).validate(invalid)

    def test_contract_deadlines_resolve_and_enforce_t05_temporal_bindings(self) -> None:
        validator = Draft202012Validator(
            load_schema("world-contract-state.schema.json"), registry=local_schema_registry()
        )
        valid = dict(
            VALID_QUIET_STATES["world.contract"],
            deadlines={"deadline.delivery": VALID_CONTRACT_DEADLINE},
        )
        validator.validate(valid)

        malformed = dict(
            valid,
            deadlines={"deadline.delivery": MALFORMED_CONTRACT_DEADLINE},
        )
        with self.assertRaises(ValidationError):
            validator.validate(malformed)

    def test_information_and_thread_schemas_remain_owner_supplied_inputs(self) -> None:
        for family, name in CONSUMED_OWNER_SCHEMA_NAMES.items():
            with self.subTest(family=family):
                schema = load_schema(name)
                self.assertIs(schema["additionalProperties"], False)

    def test_player_state_schema_is_present_and_strict(self) -> None:
        self.assertTrue(
            PLAYER_WORLD_SCHEMA.is_file(),
            "W05.T01 must provide the owner-local world.player state schema",
        )
        schema = load_schema(PLAYER_WORLD_SCHEMA_NAME)
        self.assertEqual(schema["$id"], "https://hedgelion.invalid/schemas/world-player-state.schema.json")
        self.assertEqual(schema["title"], "HDM world.player state")
        self.assertIs(schema["additionalProperties"], False)
        self.assertIn("collaboration_route_refs", schema["required"])


class WorldFamilyCensusTests(unittest.TestCase):
    def test_owner_local_inputs_cover_the_exact_final_world_census(self) -> None:
        self.assertEqual(
            CANONICAL_WORLD_FAMILIES,
            {
                "world.actor",
                "world.actor_group",
                "world.asset",
                "world.location",
                "world.connection",
                "world.zone",
                "world.organization",
                "world.contract",
                "world.mission",
                "world.scene",
                "world.encounter",
                "world.hazard",
                "world.effect",
                "world.lore_fact",
                "world.knowledge",
                "world.thread",
                "world.player",
            },
        )
        self.assertNotIn("world.faction", CANONICAL_WORLD_FAMILIES)
        self.assertEqual(set(EXPECTED_WORLD_SCHEMA_DISPATCH), CANONICAL_WORLD_FAMILIES)

    def test_final_runtime_family_census_remains_exact(self) -> None:
        self.assertEqual(
            CANONICAL_RUNTIME_FAMILIES,
            {
                "runtime.session",
                "runtime.message",
                "runtime.interaction",
                "runtime.procedure",
                "runtime.intent_plan",
                "runtime.command",
                "runtime.resolution",
                "runtime.continuation",
                "runtime.mechanical_event",
                "runtime.semantic_event",
                "runtime.resolution_trace",
                "runtime.disclosure",
                "runtime.collaboration_obligation",
                "runtime.checkpoint",
                "runtime.id_allocator",
                "runtime.maintenance_audit",
                "runtime.catalog_gap_report",
            },
        )
        self.assertEqual(len(CANONICAL_RUNTIME_FAMILIES), 17)


class WorldEnvelopeDispatchTests(unittest.TestCase):
    def _load_inputs(self) -> dict[str, object]:
        return load_w05_world_machine_inputs(self)

    def test_dispatch_inputs_cover_each_world_family_once(self) -> None:
        inputs = self._load_inputs()
        dispatch = inputs["world_family_schema_dispatch"]
        self.assertIsInstance(dispatch, list)
        families = [entry["family"] for entry in dispatch]
        self.assertEqual(len(families), len(set(families)))
        self.assertEqual(set(families), CANONICAL_WORLD_FAMILIES)
        self.assertNotIn("world.faction", families)

        schema_paths: list[str] = []
        for family, expected_schema in EXPECTED_WORLD_SCHEMA_DISPATCH.items():
            with self.subTest(family=family):
                entry = next(row for row in dispatch if row["family"] == family)
                self.assertEqual(entry["schema_path"], f"DEV/SCHEMAS/{expected_schema}")
                schema_paths.append(entry["schema_path"])
                schema = load_schema(expected_schema)
                self.assertIs(schema["additionalProperties"], False)

        self.assertEqual(len(schema_paths), len(set(schema_paths)))

    def test_owner_inputs_reference_information_collaboration_and_source_identity_owners(self) -> None:
        inputs = self._load_inputs()
        self.assertEqual(
            inputs["information_schema_inputs"],
            {
                "world.lore_fact": "DEV/SCHEMAS/world-lore-fact-state.schema.json",
                "world.knowledge": "DEV/SCHEMAS/world-knowledge-state.schema.json",
            },
        )
        self.assertEqual(
            inputs["collaboration_state_input"],
            {
                "owner_checkpoint": "W04_PLAYER_COLLABORATION_DELTA_READY",
                "owner_path": "DEV/TESTS/fixtures/w04_player_collaboration_delta.json",
                "schema_pointer": "/player_fragment_schema",
            },
        )
        self.assertEqual(
            inputs["source_native_identity_input"],
            {
                "owner_checkpoint": "W03_SOURCE_NATIVE_LIVE_ID_READY",
                "owner_path": "DEV/docs/superpowers/plans/implementation-wave-03-principal-live-temporal.md",
            },
        )

    def test_dispatch_has_no_generic_or_latest_fallback(self) -> None:
        inputs = self._load_inputs()
        self.assertNotIn("fallback_schema", inputs)
        self.assertNotIn("default_schema", inputs)
        self.assertNotIn("latest_schema", inputs)
        self.assertNotIn("additionalProperties", inputs)


class DefinitionBindingModeTests(unittest.TestCase):
    def test_owner_local_binding_deltas_complete_the_exact_world_census(self) -> None:
        inputs = load_w05_world_machine_inputs(self)
        binding_inputs = inputs["definition_binding_inputs"]
        self.assertEqual(
            binding_inputs["base_entity_structures"],
            "DEV/CATALOG/entity-structures.json",
        )
        self.assertEqual(
            binding_inputs["entity_structures_schema"],
            "DEV/SCHEMAS/entity-structures.schema.json",
        )

        base_structures = json.loads(
            (ROOT / binding_inputs["base_entity_structures"]).read_text(encoding="utf-8")
        )
        Draft202012Validator(
            load_schema("entity-structures.schema.json")
        ).validate(base_structures)
        base_world = base_structures["world_records"]
        deltas = binding_inputs["owner_local_deltas"]
        self.assertEqual(set(base_world) & set(deltas), set())
        self.assertEqual(set(base_world) | set(deltas), CANONICAL_WORLD_FAMILIES)
        self.assertEqual(set(deltas), {"world.thread", "world.player"})

        for family, delta in deltas.items():
            with self.subTest(family=family):
                self.assertEqual(delta, {"definition_binding": {"mode": "forbidden"}})

        core_catalog = json.loads(
            (ROOT / "DEV" / "CATALOG" / "core-catalog.json").read_text(encoding="utf-8")
        )
        registered_definitions = set(core_catalog["registries"]["content_definition_kinds"])
        for family, spec in base_world.items():
            binding = spec["definition_binding"]
            with self.subTest(family=family):
                if binding["mode"] == "forbidden":
                    self.assertEqual(binding, {"mode": "forbidden"})
                else:
                    self.assertIn(binding["mode"], {"optional", "required"})
                    self.assertTrue(set(binding["allowed_definition_kinds"]))
                    self.assertLessEqual(
                        set(binding["allowed_definition_kinds"]), registered_definitions
                    )


@unittest.skip("Wave 05 owns shared catalog integration.")
class SharedCatalogIntegrationTests(unittest.TestCase):
    def test_shared_catalog_integration_is_deferred(self) -> None:
        self.fail("Wave 05 must integrate the shared catalog.")


class PlayerCollaborationStrictStateIntegrationTests(unittest.TestCase):
    def _load_delta(self) -> dict[str, object]:
        self.assertTrue(
            PLAYER_COLLABORATION_DELTA.is_file(),
            "W04.T03A must publish its bounded PLAYER collaboration delta",
        )
        return json.loads(PLAYER_COLLABORATION_DELTA.read_text(encoding="utf-8"))

    def _fragment_validator(self) -> Draft202012Validator:
        delta = self._load_delta()
        fragment = delta["player_fragment_schema"]
        self.assertIsInstance(fragment, dict)
        return Draft202012Validator(fragment)

    def test_delta_declares_exact_scoped_route_reference_fragment(self) -> None:
        delta = self._load_delta()

        self.assertEqual(delta["kind"], "w04.player_collaboration_delta")
        self.assertEqual(delta["output"], "W04_PLAYER_COLLABORATION_DELTA_READY")
        self.assertEqual(delta["route_reference_authority"], "routing_only")
        self.assertEqual(
            delta["forbidden_authorization_fallbacks"],
            ["MANIFEST.players.player_ids", "GAME/CAMPAIGN/INDEX/PLAYER_INDEX.yaml"],
        )
        self.assertIn("authorization_fallbacks", delta)
        self.assertEqual(delta["authorization_fallbacks"], [])
        self.assertEqual(
            delta["player_fragment_schema"]["required"],
            ["collaboration_route_refs"],
        )

    def test_collaboration_owner_has_no_generic_player_index_fallback(self) -> None:
        source = (ROOT / "GAME" / "TOOLS" / "collaboration.py").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("MANIFEST.players.player_ids", source)
        self.assertNotIn("PLAYER_INDEX.yaml", source)

    def test_missing_route_references_fail_closed(self) -> None:
        with self.assertRaises(ValidationError):
            self._fragment_validator().validate({})

    def test_duplicate_route_references_fail_closed(self) -> None:
        ref = {"obligation_id": "obligation-1", "generation": 2}
        with self.assertRaises(ValidationError):
            self._fragment_validator().validate(
                {"collaboration_route_refs": [ref, dict(ref)]}
            )

    def test_route_references_are_scoped_and_non_authoritative(self) -> None:
        validator = self._fragment_validator()
        validator.validate(
            {
                "collaboration_route_refs": [
                    {"obligation_id": "obligation-1", "generation": 2}
                ]
            }
        )

        for forbidden_field in (
            "authorized",
            "authorization",
            "controlled_pc_ids",
            "lifecycle",
            "status",
        ):
            with self.subTest(forbidden_field=forbidden_field), self.assertRaises(
                ValidationError
            ):
                validator.validate(
                    {
                        "collaboration_route_refs": [
                            {
                                "obligation_id": "obligation-1",
                                "generation": 2,
                                forbidden_field: True,
                            }
                        ]
                    }
                )

    def test_player_state_schema_accepts_only_the_owner_collaboration_fragment(self) -> None:
        self.assertTrue(
            PLAYER_WORLD_SCHEMA.is_file(),
            "W05.T01 must join the W04 collaboration fragment into strict PLAYER state",
        )
        schema = load_schema(PLAYER_WORLD_SCHEMA_NAME)
        state = {
            "player_id": "player.aria",
            "status": "active",
            "github_binding": {"user_id": "account.42", "login": "aria"},
            "controlled_pc_ids": ["pc.aria"],
            "collaboration_route_refs": [
                {"obligation_id": "obligation-1", "generation": 2}
            ],
        }
        Draft202012Validator(schema).validate(state)
        fragment = self._fragment_validator()
        fragment.validate(
            {"collaboration_route_refs": state["collaboration_route_refs"]}
        )

        for forbidden_field in ("authorization", "authorized", "membership_registry"):
            with self.subTest(forbidden_field=forbidden_field), self.assertRaises(
                ValidationError
            ):
                Draft202012Validator(schema).validate({**state, forbidden_field: True})


class WorldPlayerNativeIdentityTests(unittest.TestCase):
    def test_optional_display_name_preserves_owner_string_shape(self) -> None:
        schema = load_schema(PLAYER_WORLD_SCHEMA_NAME)
        state = {
            "player_id": "player.aria",
            "status": "active",
            "github_binding": {"user_id": "account.42", "login": "aria"},
            "controlled_pc_ids": ["pc.aria"],
            "collaboration_route_refs": [],
        }
        validator = Draft202012Validator(schema)
        for display_name in ("", None):
            with self.subTest(display_name=display_name):
                validator.validate({**state, "display_name": display_name})

    def test_player_identity_is_stable_and_separate_from_mutable_login(self) -> None:
        self.assertTrue(
            PLAYER_WORLD_SCHEMA.is_file(),
            "W05.T01 must provide strict owner-local PLAYER identity inputs",
        )
        schema = load_schema(PLAYER_WORLD_SCHEMA_NAME)
        validator = Draft202012Validator(schema)
        state = {
            "player_id": "player.aria",
            "status": "active",
            "github_binding": {"user_id": "account.42", "login": "aria"},
            "controlled_pc_ids": ["pc.aria"],
            "collaboration_route_refs": [],
        }
        validator.validate(state)
        renamed = {
            **state,
            "github_binding": {"user_id": "account.42", "login": "aria-renamed"},
        }
        validator.validate(renamed)
        self.assertEqual(state["player_id"], renamed["player_id"])
        self.assertEqual(
            state["github_binding"]["user_id"],
            renamed["github_binding"]["user_id"],
        )

    def test_native_identity_inputs_retain_the_w03_live_birth_owner(self) -> None:
        inputs = load_w05_world_machine_inputs(self)
        identity_input = inputs["source_native_identity_input"]
        self.assertEqual(
            identity_input["owner_checkpoint"], "W03_SOURCE_NATIVE_LIVE_ID_READY"
        )
        self.assertEqual(
            identity_input["owner_path"],
            "DEV/docs/superpowers/plans/implementation-wave-03-principal-live-temporal.md",
        )
        w03_owner = (ROOT / identity_input["owner_path"]).read_text(encoding="utf-8")
        self.assertIn("| world.player | FORBIDDEN |", w03_owner)


@unittest.skip("Wave 05 owns source-native identifier-policy integration.")
class SourceNativeIdentifierPolicyIntegrationTests(unittest.TestCase):
    def test_source_native_identifier_policy_is_deferred(self) -> None:
        self.fail("Wave 05 must integrate source-native identifier policy.")


if __name__ == "__main__":
    unittest.main()
