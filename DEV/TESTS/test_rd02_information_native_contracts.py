from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.information import (
    InformationContractError,
    normalize_embedded_epistemic_input,
    normalize_information_evidence,
    normalize_live_material_evidence,
    validate_knowledge_transition,
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


class NativeInformationSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_owner_native_schemas_are_strict_and_preserve_distinct_authorities(self) -> None:
        schema_names = (
            "information-normalization-result.schema.json",
            "world-lore-fact-state.schema.json",
            "world-knowledge-state.schema.json",
            "runtime-disclosure-state.schema.json",
            "runtime-message-state.schema.json",
        )
        schemas = {
            name: json.loads((ROOT / "DEV" / "SCHEMAS" / name).read_text(encoding="utf-8"))
            for name in schema_names
        }

        self.assertTrue(all(schema["additionalProperties"] is False for schema in schemas.values()))
        self.assertEqual(
            schemas["world-lore-fact-state.schema.json"]["required"],
            ["fact_id", "statement", "truth_status", "record_status"],
        )
        self.assertEqual(
            schemas["world-knowledge-state.schema.json"]["required"],
            ["knower_id", "fact_id", "stance", "supporting_source_refs"],
        )
        self.assertEqual(
            schemas["runtime-disclosure-state.schema.json"]["required"],
            ["player_id", "fact_id", "statement_exposed", "source_refs"],
        )
        self.assertEqual(
            schemas["runtime-message-state.schema.json"]["required"],
            ["message_id", "interaction_id", "direction", "recipient_player_id", "payload_state", "content_digest"],
        )

    def test_normalizer_output_satisfies_strict_draft_2020_12_result_schema(self) -> None:
        result = normalize_information_evidence(_native_information_input())

        Draft202012Validator(
            self.schemas["information-normalization-result.schema.json"],
            registry=self.registry,
        ).validate(result)

    def test_schemas_reject_missing_provenance_and_invalid_native_ids(self) -> None:
        lore_validator = Draft202012Validator(
            self.schemas["world-lore-fact-state.schema.json"], registry=self.registry
        )
        knowledge_validator = Draft202012Validator(
            self.schemas["world-knowledge-state.schema.json"], registry=self.registry
        )

        with self.assertRaises(ValidationError):
            lore_validator.validate(
                {
                    "statement": "The duke is a vampire.",
                    "truth_status": "truth.established",
                    "record_status": "lore_record.active",
                }
            )
        with self.assertRaises(ValidationError):
            knowledge_validator.validate(
                {
                    "knower_id": "actor.aria",
                    "fact_id": "fact.duke_vampire",
                    "stance": "epistemic.known",
                    "supporting_source_refs": [],
                }
            )
        with self.assertRaises(ValidationError):
            knowledge_validator.validate(
                {
                    "knower_id": "actor.aria",
                    "fact_id": "1-not-a-native-id",
                    "stance": "epistemic.known",
                    "supporting_source_refs": ["semantic.001"],
                }
            )


def _native_information_input() -> dict[str, object]:
    return {
        "fact": {
            "fact_id": "fact.duke_vampire",
            "statement": "The duke is a vampire.",
            "truth_status": "truth.established",
            "record_status": "lore_record.active",
            "provenance_refs": ["semantic.001"],
            "last_truth_transition_ref": "semantic.001",
        },
        "knowledge": {
            "knower_id": "actor.aria",
            "fact_id": "fact.duke_vampire",
            "stance": "epistemic.known",
            "supporting_source_refs": ["semantic.001"],
            "source_evidence": [
                {
                    "ref": "semantic.001",
                    "accepted": True,
                    "current": True,
                    "authorized_knower_ids": ["actor.aria"],
                }
            ],
        },
        "emission": {
            "message_id": "message.scene.001",
            "interaction_id": "turn.001",
            "recipient_player_id": "player.aria",
            "text": "You confirm the duke is a vampire.",
            "source_evidence": [
                {
                    "ref": "semantic.001",
                    "accepted": True,
                    "current": True,
                    "fact_id": "fact.duke_vampire",
                    "truth_transition_ref": "semantic.001",
                }
            ],
            "disclosure_refs": [
                {
                    "fact_id": "fact.duke_vampire",
                    "aspect": "disclosure.statement",
                    "source_ref": "semantic.001",
                },
                {
                    "fact_id": "fact.duke_vampire",
                    "aspect": "disclosure.objective_status",
                    "truth_transition_ref": "semantic.001",
                    "source_ref": "semantic.001",
                },
            ],
        },
    }


class InformationNormalizationTests(unittest.TestCase):
    def test_normalizes_accepted_evidence_into_lore_knowledge_disclosure_and_message(self) -> None:
        result = normalize_information_evidence(_native_information_input())

        self.assertEqual(result["lore_fact"]["fact_id"], "fact.duke_vampire")
        self.assertEqual(result["knowledge"]["stance"], "epistemic.known")
        self.assertEqual(result["disclosure"]["player_id"], "player.aria")
        self.assertTrue(result["disclosure"]["statement_exposed"])
        self.assertEqual(result["disclosure"]["latest_exposed_truth_transition_ref"], "semantic.001")
        self.assertEqual(result["message"]["recipient_player_id"], "player.aria")

    def test_rejects_visibility_as_knowledge_evidence(self) -> None:
        with self.assertRaisesRegex(InformationContractError, "accepted native evidence"):
            normalize_embedded_epistemic_input(
                {
                    "knower_id": "actor.aria",
                    "fact_id": "fact.duke_vampire",
                    "stance": "epistemic.known",
                    "supporting_source_refs": ["cache:scene-001"],
                }
            )

    def test_rejects_stale_unauthorized_or_ambiguous_evidence(self) -> None:
        cases = (
            (["semantic.001", "semantic.001"], []),
            (["semantic.001"], [{"ref": "semantic.001", "accepted": True, "current": False, "authorized_knower_ids": ["actor.aria"]}]),
            (["semantic.001"], [{"ref": "semantic.001", "accepted": True, "current": True, "authorized_knower_ids": ["actor.borin"]}]),
            (["semantic.001"], [{"ref": "semantic.001", "accepted": False, "current": True, "authorized_knower_ids": ["actor.aria"]}]),
        )
        for source_refs, source_evidence in cases:
            with self.subTest(source_refs=source_refs, source_evidence=source_evidence):
                with self.assertRaises(InformationContractError):
                    validate_knowledge_transition(
                        {
                            "knower_id": "actor.aria",
                            "fact_id": "fact.duke_vampire",
                            "stance": "epistemic.known",
                            "supporting_source_refs": source_refs,
                            "source_evidence": source_evidence,
                        }
                    )

    def test_rejects_unrelated_or_stale_truth_transition_evidence(self) -> None:
        cases = (
            ("fact.other", "semantic.001", True),
            ("fact.duke_vampire", "semantic.other", True),
            ("fact.duke_vampire", "semantic.001", False),
        )
        for evidence_fact_id, evidence_transition_ref, current in cases:
            with self.subTest(
                evidence_fact_id=evidence_fact_id,
                evidence_transition_ref=evidence_transition_ref,
                current=current,
            ):
                value = _native_information_input()
                evidence = value["emission"]["source_evidence"][0]
                evidence["fact_id"] = evidence_fact_id
                evidence["truth_transition_ref"] = evidence_transition_ref
                evidence["current"] = current
                with self.assertRaisesRegex(
                    InformationContractError, "truth-transition evidence|accepted native evidence"
                ):
                    normalize_information_evidence(value)


class LegacyInformationProjectionTests(unittest.TestCase):
    def test_legacy_lore_schema_is_not_the_native_information_contract(self) -> None:
        legacy_lore = (ROOT / "GAME" / "SCHEMA" / "lore.schema.yaml").read_text(encoding="utf-8")
        information = (ROOT / "GAME" / "CORE" / "INFORMATION.md").read_text(encoding="utf-8")

        self.assertIn("disputed_in_world", legacy_lore)
        self.assertIn("legacy embedded pc/npc/faction knowledge arrays", information.lower())
        self.assertIn("world.lore_fact", information)
        self.assertIn("world.knowledge", information)


class RecipientIsolationTests(unittest.TestCase):
    def test_normalization_does_not_leak_another_recipients_disclosure(self) -> None:
        result = normalize_live_material_evidence(
            {
                "message_id": "message.scene.002",
                "interaction_id": "turn.002",
                "recipient_player_id": "player.aria",
                "text": "Only Aria receives this clue.",
                "source_evidence": [
                    {"ref": "semantic.002", "accepted": True, "current": True}
                ],
                "disclosure_refs": [
                    {
                        "fact_id": "fact.hidden_passage",
                        "aspect": "disclosure.statement",
                        "source_ref": "semantic.002",
                    }
                ],
            }
        )

        self.assertEqual(result["disclosure"]["player_id"], "player.aria")
        self.assertNotIn("player.borin", result["disclosure"].values())

    def test_rejects_unaccepted_disclosure_source_evidence(self) -> None:
        with self.assertRaisesRegex(InformationContractError, "accepted native evidence"):
            normalize_live_material_evidence(
                {
                    "message_id": "message.scene.003",
                    "interaction_id": "turn.003",
                    "recipient_player_id": "player.aria",
                    "text": "Only accepted evidence may be disclosed.",
                    "source_evidence": [{"ref": "semantic.003", "accepted": False, "current": True}],
                    "disclosure_refs": [
                        {
                            "fact_id": "fact.hidden_passage",
                            "aspect": "disclosure.statement",
                            "source_ref": "semantic.003",
                        }
                    ],
                }
            )

    def test_rejects_disclosure_for_a_different_recipient(self) -> None:
        with self.assertRaisesRegex(InformationContractError, "recipient"):
            normalize_live_material_evidence(
                {
                    "message_id": "message.scene.002",
                    "interaction_id": "turn.002",
                    "recipient_player_id": "player.aria",
                    "text": "Only Aria receives this clue.",
                    "source_evidence": [
                        {"ref": "semantic.002", "accepted": True, "current": True}
                    ],
                    "disclosure_refs": [
                        {
                            "fact_id": "fact.hidden_passage",
                            "aspect": "disclosure.statement",
                            "source_ref": "semantic.002",
                            "player_id": "player.borin",
                        }
                    ],
                }
            )


if __name__ == "__main__":
    unittest.main()
