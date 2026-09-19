"""W03.T08 owner-local LIVE information and scene-consumer witnesses."""

from __future__ import annotations

import hashlib
from pathlib import Path
import unittest

from GAME.TOOLS.information import (
    InformationContractError,
    LiveInformationCandidate,
    apply_normalization_candidates_under_native_owners,
    extract_material_live_information,
)
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveContractError,
    LiveEnvelope,
    build_live_ref,
    build_material_current_scene_bridge,
    derive_live_epoch_id,
)


ROOT = Path(__file__).resolve().parents[2]
LIVE_SCENE_CORE_SHA256 = "faf9b1be0bb023570d93f3e2f26decef36da518060b4753926331de360b59dbf"
MULTIPLAYER_CORE_SHA256 = "45b65daa63d9c4cab02b39216bbe94baf3c3ee4d902ecca854a45401d1b33f7f"
SCENE_SCHEMA_SHA256 = "85237b5b76cd847c1db5d66d105f310c5a3a115add37bff6c229c6126d7fc5e1"
LIVE_SCENE_SCHEMA_SHA256 = "0e5cceac5b29d1bcad1fcfe5779905092402d1c8b00d9c3d04157a822ceb5638"


def _live_source(*, revision: str = "a" * 40) -> LiveEnvelope:
    claims = (LiveClaim.exact_owner("world.actor", "actor.aria"),)
    opening_revision = "0" * 40
    epoch_id = derive_live_epoch_id(
        "campaign-frostfall", "scene-market", opening_revision, claims
    )
    return LiveEnvelope(
        campaign_id="campaign-frostfall",
        scene_id="scene-market",
        epoch_id=epoch_id,
        source_ref=build_live_ref("campaign-frostfall", "scene-market", epoch_id),
        source_revision=revision,
        claims=claims,
        opening_campaign_revision=opening_revision,
    )


def _native_information(*, recipient: str = "player.aria") -> dict[str, object]:
    return {
        "fact": {
            "fact_id": "fact.hidden_passage",
            "statement": "A hidden passage opens behind the tapestry.",
            "truth_status": "truth.established",
            "record_status": "lore_record.active",
            "provenance_refs": ["semantic.live.001"],
        },
        "knowledge": {
            "knower_id": "actor.aria",
            "fact_id": "fact.hidden_passage",
            "stance": "epistemic.known",
            "supporting_source_refs": ["semantic.live.001"],
            "source_evidence": [
                {
                    "ref": "semantic.live.001",
                    "accepted": True,
                    "current": True,
                    "authorized_knower_ids": ["actor.aria"],
                }
            ],
        },
        "emission": {
            "message_id": "message.live.001",
            "interaction_id": "turn.live.001",
            "recipient_player_id": recipient,
            "text": "You notice the hidden passage.",
            "source_evidence": [
                {
                    "ref": "semantic.live.001",
                    "accepted": True,
                    "current": True,
                    "fact_id": "fact.hidden_passage",
                }
            ],
            "disclosure_refs": [
                {
                    "fact_id": "fact.hidden_passage",
                    "aspect": "disclosure.statement",
                    "source_ref": "semantic.live.001",
                }
            ],
        },
    }


def _projection(source: LiveEnvelope, *candidates: dict[str, object]) -> dict[str, object]:
    return {
        "source_key": list(source.source_key),
        "source_ref": source.source_ref,
        "source_revision": source.source_revision,
        "source_native_ids": list(source.source_native_ids),
        "information_candidates": list(candidates),
    }


class LiveInformationNormalizationIntegrationTests(unittest.TestCase):
    def test_current_source_candidates_normalize_under_native_information_owners(self) -> None:
        source = _live_source()
        candidates = extract_material_live_information(
            source,
            _projection(
                source,
                {"recipient_player_id": "player.aria", "evidence": _native_information()},
            ),
            recipient_player_id="player.aria",
        )

        result = apply_normalization_candidates_under_native_owners(
            candidates, source, recipient_player_id="player.aria"
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["lore_fact"]["fact_id"], "fact.hidden_passage")
        self.assertEqual(result[0]["message"]["recipient_player_id"], "player.aria")
        self.assertEqual(result[0]["disclosure"]["player_id"], "player.aria")
        self.assertNotIn("live_facts", result[0])
        self.assertNotIn("known_by_pc_ids", result[0])

    def test_stale_source_projection_is_rejected_before_normalization(self) -> None:
        source = _live_source(revision="b" * 40)
        stale = _projection(_live_source(revision="a" * 40), {
            "recipient_player_id": "player.aria", "evidence": _native_information()
        })

        with self.assertRaisesRegex(InformationContractError, "current|stale"):
            extract_material_live_information(source, stale, recipient_player_id="player.aria")

    def test_recipient_leakage_is_rejected_instead_of_projected(self) -> None:
        source = _live_source()
        leaked = _projection(
            source,
            {"recipient_player_id": "player.borin", "evidence": _native_information(recipient="player.borin")},
        )

        with self.assertRaisesRegex(InformationContractError, "recipient"):
            extract_material_live_information(source, leaked, recipient_player_id="player.aria")

    def test_legacy_visibility_and_live_arrays_are_not_information_fallbacks(self) -> None:
        source = _live_source()
        legacy = _projection(
            source,
            {
                "recipient_player_id": "player.aria",
                "evidence": {
                    "known_by_pc_ids": ["pc.aria"],
                    "visible_to": ["player.aria"],
                    "narration": "The passage is obvious.",
                },
            },
        )

        with self.assertRaisesRegex(InformationContractError, "legacy|native|evidence"):
            extract_material_live_information(source, legacy, recipient_player_id="player.aria")

    def test_apply_rejects_caller_forged_or_stale_candidate(self) -> None:
        source = _live_source(revision="b" * 40)
        forged = LiveInformationCandidate(
            source_key=source.source_key,
            source_ref=source.source_ref,
            source_revision="a" * 40,
            source_native_ids=source.source_native_ids,
            recipient_player_id="player.aria",
            evidence=_native_information(),
        )

        with self.assertRaisesRegex(InformationContractError, "current|stale"):
            apply_normalization_candidates_under_native_owners(
                (forged,), source, recipient_player_id="player.aria"
            )


class MaterialBridgeCurrentnessTests(unittest.TestCase):
    def test_exact_current_source_builds_material_scene_bridge(self) -> None:
        source = _live_source()
        bridge = build_material_current_scene_bridge(
            source,
            {
                "source_key": list(source.source_key),
                "source_ref": source.source_ref,
                "source_revision": source.source_revision,
                "source_native_ids": [],
                "scene_id": source.scene_id,
                "material": {"summary": "The market square is crowded."},
            },
        )

        self.assertEqual(bridge.source_key, source.source_key)
        self.assertEqual(bridge.source_revision, source.source_revision)
        self.assertEqual(bridge.material["summary"], "The market square is crowded.")
        self.assertEqual(bridge.as_mapping()["authority"], "LIVE_SOURCE_CURRENT")

    def test_stale_material_projection_cannot_bridge_to_current_scene(self) -> None:
        source = _live_source(revision="b" * 40)
        stale = {
            "source_key": list(source.source_key),
            "source_ref": source.source_ref,
            "source_revision": "a" * 40,
            "source_native_ids": [],
            "scene_id": source.scene_id,
            "material": {},
        }

        with self.assertRaisesRegex(LiveContractError, "current|stale"):
            build_material_current_scene_bridge(source, stale)

    def test_projection_cannot_supply_source_native_authority(self) -> None:
        source = _live_source()
        forged = {
            "source_key": list(source.source_key),
            "source_ref": source.source_ref,
            "source_revision": source.source_revision,
            "source_native_ids": ["actor:live1:forged"],
            "scene_id": source.scene_id,
            "material": {},
        }

        with self.assertRaisesRegex(LiveContractError, "source-native|current"):
            build_material_current_scene_bridge(source, forged)

    def test_legacy_live_branch_revision_shape_has_no_fallback(self) -> None:
        source = _live_source()
        legacy = {
            "epoch_id": source.epoch_id,
            "live_branch": "live/old-name",
            "revision": 7,
            "scene_id": source.scene_id,
            "material": {},
        }

        with self.assertRaisesRegex(LiveContractError, "source-native|current|projection"):
            build_material_current_scene_bridge(source, legacy)


class SourceNativeLiveSchemaCutoverTests(unittest.TestCase):
    def test_bridge_preserves_strict_source_native_identity_fields(self) -> None:
        source = _live_source()
        mapping = source.as_mapping()

        self.assertIn("source_revision", mapping)
        self.assertIn("source_native_ids", mapping)
        self.assertNotIn("revision", mapping)
        self.assertNotIn("live_branch", mapping)
        self.assertNotIn("base_campaign_sha", mapping)

    def test_bridge_requires_all_exact_source_fields(self) -> None:
        source = _live_source()
        projection = _projection(source)
        projection.pop("source_revision")

        with self.assertRaisesRegex(LiveContractError, "source_revision|projection"):
            build_material_current_scene_bridge(source, projection)


class ShippedLiveCoreCutoverTests(unittest.TestCase):
    def test_live_scene_core_remains_deferred_to_wave05_final_writer(self) -> None:
        path = ROOT / "GAME" / "CORE" / "LIVE_SCENE.md"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(digest, LIVE_SCENE_CORE_SHA256)

    def test_shared_scene_schemas_remain_deferred_to_wave05(self) -> None:
        for relative, expected in (
            ("GAME/SCHEMA/scene.schema.yaml", SCENE_SCHEMA_SHA256),
            ("GAME/SCHEMA/live_scene.schema.yaml", LIVE_SCENE_SCHEMA_SHA256),
        ):
            with self.subTest(relative=relative):
                self.assertEqual(
                    hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected
                )


class MultiplayerCoreCutoverTests(unittest.TestCase):
    def test_multiplayer_core_remains_deferred_to_wave05_final_writer(self) -> None:
        path = ROOT / "GAME" / "CORE" / "MULTIPLAYER.md"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), MULTIPLAYER_CORE_SHA256)

    def test_owner_local_delta_names_the_deferred_shared_inputs(self) -> None:
        delta = (
            ROOT
            / "DEV"
            / "docs"
            / "superpowers"
            / "design"
            / "2026-09-19-w03-t08-live-consumer-deltas.md"
        ).read_text(encoding="utf-8")
        self.assertIn("GAME/CORE/LIVE_SCENE.md", delta)
        self.assertIn("GAME/CORE/MULTIPLAYER.md", delta)
        self.assertIn("Wave-05", delta)
        self.assertIn("source-native", delta)


if __name__ == "__main__":
    unittest.main()
