"""Owner-local routing, allocator, index, and HOT contract witnesses."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GAME_ROOT = ROOT / "GAME"
if str(GAME_ROOT) not in sys.path:
    sys.path.insert(0, str(GAME_ROOT))

from TOOLS.hot_store import NativeHotStore, OwnerDocument, StaleOwnerGeneration, rebuild_helper
from TOOLS.id_allocator import AllocatorState, allocate_and_stage_record, load_campaign_allocator
from TOOLS.native_storage import (
    AmbiguousCampaignRoot,
    CampaignRootCandidate,
    IdentityMismatch,
    MissingCampaignRoot,
    StaleCampaignRoot,
    NativeStorageError,
    route_native_record,
    select_campaign_root,
    validate_loaded_identity,
)
from TOOLS.native_storage import NativeFamilyIndex, rebuild_family_index, resolve_discovery_candidate


class NativeRouteTests(unittest.TestCase):
    def test_known_actor_id_uses_framed_exact_route_without_index_lookup(self) -> None:
        route = route_native_record("world.actor", ("actor-0001",))

        self.assertEqual(
            route.relative_path,
            "WORLD/ACTORS/RECORDS/a7/02/"
            "9124QBANA0OJ2BAI9TAL8H9DAOOG0TRFE9M68BJ1CDQ6USG0000000800000KOB3EHNN4B9G60O32.yaml",
        )
        self.assertEqual(route.identity, ("actor-0001",))

    def test_loaded_body_must_match_requested_family_and_complete_identity(self) -> None:
        with self.assertRaises(IdentityMismatch):
            validate_loaded_identity(
                "world.actor",
                ("actor-0001",),
                {"kind": "world.actor", "id": "actor-0002"},
            )


class CampaignAllocatorTests(unittest.TestCase):
    def test_campaign_allocator_skips_collision_and_advances_monotonically(self) -> None:
        state = load_campaign_allocator(
            {
                "schema_version": 1,
                "kind": "runtime.id_allocator",
                "campaign_id": "campaign-a",
                "counters": {"world.actor": 1},
            }
        )

        record_id, staged = allocate_and_stage_record(
            state,
            family_key="world.actor",
            prefix="actor",
            minimum_width=4,
            collision_check=lambda candidate: candidate == "actor-0002",
        )

        self.assertEqual(record_id, "actor-0003")
        self.assertEqual(staged.counters["world.actor"], 3)
        self.assertEqual(state.counters["world.actor"], 1)

    def test_allocator_is_campaign_scoped(self) -> None:
        state = AllocatorState(campaign_id="campaign-a", counters={})
        with self.assertRaises(ValueError):
            state.require_campaign("campaign-b")


class PresenceAuthorityTests(unittest.TestCase):
    def test_index_membership_does_not_prove_presence(self) -> None:
        index = NativeFamilyIndex(
            family_key="world.actor",
            entries=(
                {
                    "id": "actor-0001",
                    "path": route_native_record("world.actor", ("actor-0001",)).relative_path,
                    "name": "Ari",
                },
            ),
        )

        record = resolve_discovery_candidate(
            index,
            "actor-0001",
            lambda _path: {
                "id": "actor-0001",
                "kind": "world.actor",
                "state": {"location_id": "location-0001"},
            },
        )

        self.assertEqual(record["state"]["location_id"], "location-0001")
        self.assertNotIn("presence", index.entries[0])


class NativeIndexTests(unittest.TestCase):
    def test_rebuilds_compact_index_from_owner_records_and_revalidates_candidates(self) -> None:
        index = rebuild_family_index(
            "world.actor",
            [
                {
                    "id": "actor-0002",
                    "kind": "world.actor",
                    "state": {},
                    "name": "Bryn",
                    "aliases": ["B"],
                    "status": "active",
                    "tags": ["guide"],
                }
            ],
        )

        self.assertEqual(index.entries[0]["id"], "actor-0002")
        self.assertNotIn("state", index.entries[0])
        with self.assertRaises(IdentityMismatch):
            resolve_discovery_candidate(
                index,
                "actor-0002",
                lambda _path: {"id": "actor-9999", "kind": "world.actor"},
            )

    def test_rebuild_helper_delegates_only_to_the_explicit_family_rebuild(self) -> None:
        index = rebuild_helper(
            "world.actor",
            [{"id": "actor-0001", "kind": "world.actor", "state": {}, "name": "Ari"}],
        )

        self.assertEqual(index.family_key, "world.actor")
        self.assertEqual(index.entries[0]["id"], "actor-0001")

    def test_rejects_index_entry_with_non_deterministic_path(self) -> None:
        with self.assertRaises(NativeStorageError):
            NativeFamilyIndex(
                family_key="world.actor",
                entries=({"id": "actor-0001", "path": "WORLD/ACTORS/RECORDS/wrong.yaml"},),
            )

    def test_rejects_noncompact_index_entry_with_owner_body(self) -> None:
        with self.assertRaises(NativeStorageError):
            NativeFamilyIndex(
                family_key="world.actor",
                entries=(
                    {
                        "id": "actor-0001",
                        "path": route_native_record("world.actor", ("actor-0001",)).relative_path,
                        "state": {"location_id": "location-0001"},
                    },
                ),
            )


class NativeHotStoreTests(unittest.TestCase):
    def test_current_owner_is_unique_by_campaign_family_and_complete_identity(self) -> None:
        with NativeHotStore(":memory:") as store:
            store.stage_owner_document(
                OwnerDocument(
                    campaign_id="campaign-a",
                    family_key="world.actor",
                    identity=("actor-0001",),
                    payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                    source_basis="commit-a",
                    generation=1,
                )
            )
            store.stage_owner_document(
                OwnerDocument(
                    campaign_id="campaign-a",
                    family_key="world.actor",
                    identity=("actor-0001",),
                    payload={"id": "actor-0001", "kind": "world.actor", "state": {}, "name": "Ari"},
                    source_basis="commit-b",
                    generation=2,
                )
            )

            loaded = store.load_current_owner("campaign-a", "world.actor", ("actor-0001",))

        self.assertEqual(loaded.generation, 2)
        self.assertEqual(loaded.payload["name"], "Ari")

    def test_rejects_stale_generation_without_replacing_newer_hot_owner(self) -> None:
        with NativeHotStore(":memory:") as store:
            current = OwnerDocument(
                campaign_id="campaign-a",
                family_key="world.actor",
                identity=("actor-0001",),
                payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                source_basis="commit-new",
                generation=2,
            )
            store.stage_owner_document(current)

            with self.assertRaises(StaleOwnerGeneration):
                store.stage_owner_document(
                    OwnerDocument(
                        campaign_id="campaign-a",
                        family_key="world.actor",
                        identity=("actor-0001",),
                        payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                        source_basis="commit-old",
                        generation=1,
                    )
                )

            self.assertEqual(store.load_current_owner("campaign-a", "world.actor", ("actor-0001",)).generation, 2)

    def test_rejects_unadmitted_family_and_invalid_world_payload(self) -> None:
        with NativeHotStore(":memory:") as store:
            with self.assertRaises(NativeStorageError):
                store.stage_owner_document(
                    OwnerDocument(
                        campaign_id="campaign-a",
                        family_key="world.unadmitted",
                        identity=("unadmitted-0001",),
                        payload={"id": "unadmitted-0001", "kind": "world.unadmitted", "state": {}},
                        source_basis="commit-a",
                        generation=1,
                    )
                )
            with self.assertRaises(IdentityMismatch):
                store.stage_owner_document(
                    OwnerDocument(
                        campaign_id="campaign-a",
                        family_key="world.actor",
                        identity=("actor-0001",),
                        payload={"id": "actor-0001", "kind": "world.actor", "state": []},
                        source_basis="commit-a",
                        generation=1,
                    )
                )


class NativeAtomicityTests(unittest.TestCase):
    def test_failed_atomic_batch_leaves_no_partial_owner_state(self) -> None:
        with NativeHotStore(":memory:") as store:
            valid = OwnerDocument(
                campaign_id="campaign-a",
                family_key="world.actor",
                identity=("actor-0001",),
                payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                source_basis="commit-a",
                generation=1,
            )
            invalid = OwnerDocument(
                campaign_id="campaign-a",
                family_key="world.actor",
                identity=("actor-0002",),
                payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                source_basis="commit-a",
                generation=1,
            )

            with self.assertRaises(IdentityMismatch):
                store.atomic_owner_mutation((valid, invalid))

            self.assertIsNone(store.load_current_owner("campaign-a", "world.actor", ("actor-0001",)))

    def test_publication_clears_only_the_exact_published_generation(self) -> None:
        with NativeHotStore(":memory:") as store:
            store.stage_owner_document(
                OwnerDocument(
                    campaign_id="campaign-a",
                    family_key="world.actor",
                    identity=("actor-0001",),
                    payload={"id": "actor-0001", "kind": "world.actor", "state": {}},
                    source_basis="commit-a",
                    generation=2,
                )
            )

            self.assertEqual(store.clear_published_generation("campaign-a", "world.actor", ("actor-0001",), 1), 0)
            self.assertEqual(store.clear_published_generation("campaign-a", "world.actor", ("actor-0001",), 2), 1)


class FixedCampaignRootSelectorTests(unittest.TestCase):
    def test_selector_returns_only_exact_current_campaign_root(self) -> None:
        root = select_campaign_root(
            (CampaignRootCandidate("campaign-a", "/campaigns/a", "commit-a"),),
            campaign_id="campaign-a",
            expected_revision="commit-a",
        )
        self.assertEqual(root, Path("/campaigns/a"))

    def test_selector_returns_typed_missing_stale_and_ambiguous_outcomes(self) -> None:
        with self.assertRaises(MissingCampaignRoot):
            select_campaign_root((), campaign_id="campaign-a", expected_revision="commit-a")
        with self.assertRaises(StaleCampaignRoot):
            select_campaign_root(
                (CampaignRootCandidate("campaign-a", "/campaigns/a", "commit-old"),),
                campaign_id="campaign-a",
                expected_revision="commit-a",
            )
        with self.assertRaises(AmbiguousCampaignRoot):
            select_campaign_root(
                (
                    CampaignRootCandidate("campaign-a", "/campaigns/a", "commit-a"),
                    CampaignRootCandidate("campaign-a", "/campaigns/a-copy", "commit-a"),
                ),
                campaign_id="campaign-a",
                expected_revision="commit-a",
            )


class NativeContractSchemaTests(unittest.TestCase):
    def test_owner_contract_schemas_and_allocator_template_are_machine_readable(self) -> None:
        schema_names = (
            "native-route.schema.json",
            "campaign-id-allocator-state.schema.json",
            "native-family-index.schema.json",
            "native-owner-hot-envelope.schema.json",
        )
        for schema_name in schema_names:
            with self.subTest(schema_name=schema_name):
                schema = json.loads((ROOT / "DEV/SCHEMAS" / schema_name).read_text(encoding="utf-8"))
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")

        route_schema = json.loads((ROOT / "DEV/SCHEMAS/native-route.schema.json").read_text(encoding="utf-8"))
        self.assertIn("route_companion_inputs", route_schema["properties"])

        allocator_template = (ROOT / "GAME/CAMPAIGN/STATE/ID_ALLOCATOR.yaml").read_text(encoding="utf-8")
        self.assertIn("kind: runtime.id_allocator", allocator_template)
        self.assertIn("campaign_id: null", allocator_template)


if __name__ == "__main__":
    unittest.main()
