from __future__ import annotations

import json
import unittest
from pathlib import Path

from GAME.TOOLS.information import (
    InformationContractError,
    normalize_embedded_epistemic_input,
    normalize_information_evidence,
    normalize_live_material_evidence,
    validate_knowledge_transition,
)


ROOT = Path(__file__).resolve().parents[2]


class NativeInformationSchemaTests(unittest.TestCase):
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
            ["statement", "truth_status", "record_status"],
        )
        self.assertEqual(
            schemas["world-knowledge-state.schema.json"]["required"],
            ["knower_id", "fact_id", "stance"],
        )
        self.assertEqual(
            schemas["runtime-disclosure-state.schema.json"]["required"],
            ["player_id", "fact_id", "statement_exposed", "source_refs"],
        )
        self.assertEqual(
            schemas["runtime-message-state.schema.json"]["required"],
            ["message_id", "interaction_id", "direction", "recipient_player_id", "payload_state", "content_digest"],
        )


class InformationNormalizationTests(unittest.TestCase):
    def test_normalizes_accepted_evidence_into_lore_knowledge_disclosure_and_message(self) -> None:
        result = normalize_information_evidence(
            {
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
                        {"ref": "semantic.001", "accepted": True, "current": True}
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
        )

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
