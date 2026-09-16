import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"

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
            with self.subTest(family=family, invalid="missing-required-state"):
                with self.assertRaises(ValidationError):
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


class WorldFamilyCensusTests(unittest.TestCase):
    def test_owner_local_inputs_cover_the_exact_final_world_census_except_deferred_player(self) -> None:
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
        self.assertNotIn("world.player", QUIET_WORLD_SCHEMA_NAMES)
        self.assertNotIn("world.player", CONSUMED_OWNER_SCHEMA_NAMES)


@unittest.skip("Wave 05 owns final world-record wrapper dispatch.")
class WorldEnvelopeDispatchTests(unittest.TestCase):
    def test_final_wrapper_dispatch_is_deferred(self) -> None:
        self.fail("Wave 05 must provide the shared world-record dispatch.")


@unittest.skip("Wave 05 owns shared definition-binding catalog integration.")
class DefinitionBindingModeTests(unittest.TestCase):
    def test_final_definition_binding_integration_is_deferred(self) -> None:
        self.fail("Wave 05 must integrate shared definition-binding modes.")


@unittest.skip("Wave 05 owns shared catalog integration.")
class SharedCatalogIntegrationTests(unittest.TestCase):
    def test_shared_catalog_integration_is_deferred(self) -> None:
        self.fail("Wave 05 must integrate the shared catalog.")


@unittest.skip("Wave 05 owns strict PLAYER collaboration state integration.")
class PlayerCollaborationStrictStateIntegrationTests(unittest.TestCase):
    def test_player_collaboration_state_is_deferred(self) -> None:
        self.fail("Wave 05 must provide PLAYER collaboration state.")


@unittest.skip("Wave 05 owns native PLAYER identity integration.")
class WorldPlayerNativeIdentityTests(unittest.TestCase):
    def test_player_native_identity_is_deferred(self) -> None:
        self.fail("Wave 05 must provide native PLAYER identity integration.")


@unittest.skip("Wave 05 owns source-native identifier-policy integration.")
class SourceNativeIdentifierPolicyIntegrationTests(unittest.TestCase):
    def test_source_native_identifier_policy_is_deferred(self) -> None:
        self.fail("Wave 05 must integrate source-native identifier policy.")


if __name__ == "__main__":
    unittest.main()
