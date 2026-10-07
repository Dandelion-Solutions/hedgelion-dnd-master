"""SP03 membership preparation against a real immutable campaign Git tree."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path

CAMPAIGN_ID = "campaign-frostfall"
ACTOR_ID = "actor.sp03"


class GitCampaignRepository:
    """Small repository port backed by real Git commit/tree objects."""

    def __init__(self, root: Path) -> None:
        self.sp03_git_repository_path = root
        self.root = root
        self.read_paths: list[str] = []
        self.read_overrides: dict[str, object] = {}
        self.read_hook: Callable[[str], None] | None = None
        self.root.mkdir(parents=True, exist_ok=True)
        self._git("init", "-q")

    def _git(
        self, *arguments: str, check: bool = True
    ) -> subprocess.CompletedProcess[bytes]:
        result = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=False,
            capture_output=True,
        )
        if check and result.returncode != 0:
            raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
        return result

    def write(self, relative_path: str, value: object) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    def commit(self, message: str = "campaign fixture") -> tuple[str, str]:
        self._git("add", "--all")
        changed = self._git("diff", "--cached", "--quiet", check=False).returncode != 0
        has_head = (
            self._git("rev-parse", "--verify", "HEAD", check=False).returncode == 0
        )
        if changed or not has_head:
            self._git(
                "-c",
                "user.name=HDM test fixture",
                "-c",
                "user.email=hdm-test@example.invalid",
                "commit",
                "-m",
                message,
            )
        revision = self._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
        tree_sha = self._git("rev-parse", "HEAD^{tree}").stdout.decode("ascii").strip()
        return revision, tree_sha

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def pin_campaign(self, campaign_id: str):
        from GAME.TOOLS.policy_basis import PinnedCampaign

        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        revision = self._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
        tree_sha = self._git("rev-parse", "HEAD^{tree}").stdout.decode("ascii").strip()
        manifest = self.read_exact_path(
            PinnedCampaign(campaign_id, revision, tree_sha), "MANIFEST.yaml"
        )
        if not isinstance(manifest, dict) or manifest.get("campaign_id") != campaign_id:
            raise ValueError(
                "pinned Git tree does not contain the exact campaign identity"
            )
        return PinnedCampaign(campaign_id, revision, tree_sha)

    def read_exact_path(self, pinned, path: str) -> object:
        self.read_paths.append(path)
        if self.read_hook is not None:
            self.read_hook(path)
        result = self._git("cat-file", "blob", f"{pinned.revision}:{path}", check=False)
        if result.returncode != 0:
            raise KeyError(path)
        try:
            payload = json.loads(result.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"malformed fixture document: {path}") from error
        if path in self.read_overrides:
            return deepcopy(self.read_overrides[path])
        return payload

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        return {"campaign_id": campaign_id}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        return {"commit_sha": revision}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        return {
            "relation": "EQUAL"
            if ancestor_revision == descendant_revision
            else "DESCENDANT"
        }

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        return {"revision": revision}


def _effect(
    effect_id: str, target_id: str, lifecycle: str = "active"
) -> dict[str, object]:
    state: dict[str, object] = {
        "target_id": target_id,
        "lifecycle": (
            {"state_id": "effect_lifecycle.active"}
            if lifecycle == "active"
            else {
                "state_id": "effect_lifecycle.terminal",
                "terminal_reason_id": "effect_end.expired",
            }
        ),
    }
    return {
        "schema_version": 2,
        "id": effect_id,
        "kind": "world.effect",
        "definition_id": "effect.definition.sp03-test",
        "state": state,
    }


def _asset(
    asset_id: str,
    *,
    owner: str | None = None,
    container: str | None = None,
    access: str | None = None,
    equipment: str | None = None,
) -> dict[str, object]:
    state: dict[str, object] = {}
    if owner is not None:
        state["owner_actor_id"] = owner
    if container is not None:
        state["container_asset_id"] = container
    if access is not None:
        state["access"] = access
    if equipment is not None:
        state["equipment"] = {"mode": equipment}
    return {
        "id": asset_id,
        "kind": "world.asset",
        "definition_id": "asset.definition.sp03-test",
        "state": state,
    }


def _write_routed(
    repository: GitCampaignRepository, family: str, record: dict[str, object]
) -> None:
    from GAME.TOOLS.native_storage import route_native_record

    route = route_native_record(family, (record["id"],))
    repository.write(route.relative_path, record)


def _actor_record() -> dict[str, object]:
    from DEV.TESTS.test_w05_t06_p0_actor_producer import _actor

    actor = _actor()
    actor["id"] = ACTOR_ID
    return actor


def _accepted_command(catalog, compiled):
    from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
    from GAME.TOOLS.runtime_execution import accept_command

    proposal = _proposal(compiled.activity_id)
    proposal["action_request"]["actor_id"] = ACTOR_ID
    proposal["action_request"]["target_ids"] = []
    return accept_command(
        _interpreter_result(),
        catalog.catalog_context,
        {"definition_id": compiled.activity_id, "kind": "definition.activity"},
        proposal,
    )


def _context(catalog, compiled, host):
    accepted = _accepted_command(catalog, compiled)
    resolution = {
        "root_command_id": accepted["command_id"],
        "initiating_command_id": accepted["command_id"],
        "activity_id": compiled.activity_id,
        "actor_id": accepted["action_request"]["actor_id"],
        "target_ids": accepted["action_request"]["target_ids"],
        "parameter_bindings": accepted["action_request"].get("parameter_bindings", {}),
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": compiled.ruleset_set_sha256,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": catalog.catalog_context.fingerprint,
        "status": "RUNNING",
        "next_segment_sequence": 1,
        "invocation_facts": accepted["invocation_facts"],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "child_resolution_ids": [],
        "segments": [],
    }
    repository = host._repository
    command_record = {
        "kind": "runtime.command",
        "id": accepted["command_id"],
        **accepted,
    }
    resolution_record = {
        "kind": "runtime.resolution",
        "id": accepted["root_resolution_id"],
        "campaign_id": CAMPAIGN_ID,
        **resolution,
    }
    _write_routed(repository, "runtime.command", command_record)
    _write_routed(repository, "runtime.resolution", resolution_record)
    repository.commit("seed accepted root preparation inputs")
    return host._current_owner._prepare_root_context(
        catalog,
        compiled,
        command_id=accepted["command_id"],
        consumer_id=compiled.instructions[0].consumer_id,
    )


class InstalledMembershipTests(unittest.TestCase):
    def test_real_installed_compiler_discovers_records_omitted_from_indexes(self):
        if "HDM_INSTALLED_STRUCTURAL_TEST" in os.environ:
            self.skipTest("outer installation driver")
        from DEV.TESTS.sp02_installed_test_support import run_installed_structural_test

        result = run_installed_structural_test(
            "DEV.TESTS.test_sp03_native_membership.PinnedMembershipTests"
        )
        print(result.stdout + result.stderr)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless("HDM_INSTALLED_STRUCTURAL_TEST" in os.environ, "installed driver")
class PinnedMembershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from DEV.TESTS.sp02_installed_test_support import authentic_generic_catalog
        from GAME.TOOLS.activity_runtime import compile_activity

        cls.catalog = authentic_generic_catalog()
        cls.compiled = compile_activity(cls.catalog, "activity.check.generic")

    def test_real_installed_compiler_discovers_records_omitted_from_indexes(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
        from GAME.TOOLS import mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(prefix="sp03-membership-") as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            _write_routed(
                repository,
                "world.effect",
                _effect("effect.index-omitted", ACTOR_ID),
            )
            _write_routed(
                repository,
                "world.asset",
                _asset("asset.index-omitted", owner=ACTOR_ID, equipment="held"),
            )
            repository.commit("initial native source")

            with NativeHotStore(":memory:") as store:
                host, _ = _selected_host(store, repository=repository)
                context = _context(self.catalog, self.compiled, host)
                observation = mechanical_sources.prepare_membership(context)

            self.assertEqual(
                {item.owner_ref.identity[0] for item in observation.effects},
                {"effect.index-omitted"},
            )
            self.assertEqual(
                {item.owner_ref.identity[0] for item in observation.assets},
                {"asset.index-omitted"},
            )
            self.assertTrue(mechanical_sources.is_membership_issued(observation))
            from GAME.TOOLS.current_owner import CurrentOwnerSource

            for owner_ref in observation.p0_observation.key_union:
                read = observation.p0_observation.require(owner_ref)
                self.assertIs(read.source, CurrentOwnerSource.PINNED_CAMPAIGN)
                self.assertEqual(read.source_basis, observation.source_revision)
            self.assertNotIn("WORLD/EFFECTS/INDEX.yaml", repository.read_paths)
            self.assertNotIn("WORLD/ITEMS/INDEX.yaml", repository.read_paths)

    def test_p0_effect_body_must_equal_enumerated_git_blob(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-body-join-"
        ) as temporary:
            repository = self._repository(Path(temporary) / "campaign.git")
            path = route_native_record(
                "world.effect", ("effect.index-omitted",)
            ).relative_path
            altered = _effect("effect.index-omitted", "actor.other")
            repository.read_overrides[path] = altered

            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                with self.assertRaises(
                    activity_contracts.NativePreparationHold
                ) as raised:
                    mechanical_sources.prepare_membership(context)
                self.assertEqual(
                    raised.exception.operation_status, "AUTHORITY_UNAVAILABLE"
                )

    def test_new_selected_live_claim_invalidates_old_empty_membership(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            SelectedLive,
            _selected_host,
        )
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.live_state import (
            LiveClaim,
            LiveEnvelope,
            LiveRouting,
            build_live_ref,
            derive_live_epoch_id,
        )

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-live-change-"
        ) as temporary:
            repository = self._repository(
                Path(temporary) / "campaign.git", records=False
            )
            live = SelectedLive(route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()))
            with NativeHotStore(":memory:") as store:
                host, _ = _selected_host(store, repository=repository, live=live)
                context = _context(self.catalog, self.compiled, host)
                observation = mechanical_sources.prepare_membership(context)
                self.assertEqual(observation.effects, ())

                claim = LiveClaim.exact_owner("world.effect", "effect.added-live")
                opening_revision = "b" * 40
                epoch_id = derive_live_epoch_id(
                    CAMPAIGN_ID, "scene.sp03", opening_revision, (claim,)
                )
                live_source = LiveEnvelope(
                    campaign_id=CAMPAIGN_ID,
                    scene_id="scene.sp03",
                    epoch_id=epoch_id,
                    source_ref=build_live_ref(CAMPAIGN_ID, "scene.sp03", epoch_id),
                    source_revision="c" * 40,
                    opening_campaign_revision=opening_revision,
                    claims=(claim,),
                )
                live.route = LiveRouting(
                    campaign_id=CAMPAIGN_ID, entries=(live_source,)
                )
                with self.assertRaises(
                    activity_contracts.NativePreparationHold
                ) as raised:
                    mechanical_sources.revalidate_membership(observation, context)
                self.assertEqual(
                    raised.exception.operation_status, "AUTHORITY_UNAVAILABLE"
                )

    def test_source_advance_during_p0_reads_holds_before_issuance(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-read-race-"
        ) as temporary:
            repository = self._repository(Path(temporary) / "campaign.git")
            changed = False
            effect_path = route_native_record(
                "world.effect", ("effect.index-omitted",)
            ).relative_path

            def add_effect_during_p0_read(path: str) -> None:
                nonlocal changed
                if path == effect_path and not changed:
                    changed = True
                    _write_routed(
                        repository,
                        "world.effect",
                        _effect("effect.added-during-read", ACTOR_ID),
                    )
                    repository.commit("concurrent Effect membership advance")

            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                repository.read_hook = add_effect_during_p0_read
                with self.assertRaises(
                    activity_contracts.NativePreparationHold
                ) as raised:
                    mechanical_sources.prepare_membership(context)
                self.assertTrue(changed)
                self.assertEqual(
                    raised.exception.operation_status, "REVALIDATION_REQUIRED"
                )

    def test_new_live_family_claim_during_p0_reads_holds_before_issuance(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            SelectedLive,
            _selected_host,
        )
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.live_state import (
            LiveClaim,
            LiveEnvelope,
            LiveRouting,
            build_live_ref,
            derive_live_epoch_id,
        )
        from GAME.TOOLS.native_storage import route_native_record

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-live-race-"
        ) as temporary:
            repository = self._repository(Path(temporary) / "campaign.git")
            live = SelectedLive(route=LiveRouting(campaign_id=CAMPAIGN_ID, entries=()))
            effect_path = route_native_record(
                "world.effect", ("effect.index-omitted",)
            ).relative_path
            changed = False

            def select_live_claim_during_read(path: str) -> None:
                nonlocal changed
                if path != effect_path or changed:
                    return
                changed = True
                claim = LiveClaim.exact_owner("world.effect", "effect.added-live")
                opening_revision = "b" * 40
                epoch_id = derive_live_epoch_id(
                    CAMPAIGN_ID, "scene.sp03", opening_revision, (claim,)
                )
                source = LiveEnvelope(
                    campaign_id=CAMPAIGN_ID,
                    scene_id="scene.sp03",
                    epoch_id=epoch_id,
                    source_ref=build_live_ref(CAMPAIGN_ID, "scene.sp03", epoch_id),
                    source_revision="c" * 40,
                    opening_campaign_revision=opening_revision,
                    claims=(claim,),
                )
                live.route = LiveRouting(campaign_id=CAMPAIGN_ID, entries=(source,))

            with NativeHotStore(":memory:") as store:
                host, _ = _selected_host(store, repository=repository, live=live)
                context = _context(self.catalog, self.compiled, host)
                repository.read_hook = select_live_claim_during_read
                with self.assertRaises(
                    activity_contracts.NativePreparationHold
                ) as raised:
                    mechanical_sources.prepare_membership(context)
                self.assertTrue(changed)
                self.assertEqual(
                    raised.exception.operation_status, "AUTHORITY_UNAVAILABLE"
                )

    def test_asset_conversion_membership_requires_matching_profile_and_generation(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-conversion-"
        ) as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            _write_routed(
                repository,
                "world.effect",
                _effect("effect.index-omitted", ACTOR_ID),
            )
            converted = _asset("asset.converted", owner=ACTOR_ID)
            converted["state"]["conversion_membership"] = {
                "conversion_effect_id": "effect.index-omitted",
                "principal_subject_id": "actor.foreign",
                "binding_generation": 999,
                "mode": "active_object",
            }
            _write_routed(repository, "world.asset", converted)
            repository.commit("unqualified Asset conversion profile")

            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                with self.assertRaises(activity_contracts.NativePreparationHold):
                    mechanical_sources.prepare_membership(context)

    def test_transformed_equipment_without_exact_availability_profile_holds(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        for mode in ("merged", "resized"):
            with (
                self.subTest(mode=mode),
                tempfile.TemporaryDirectory(
                    prefix="sp03-membership-transform-"
                ) as temporary,
            ):
                repository = GitCampaignRepository(Path(temporary) / "campaign.git")
                repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
                repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
                repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
                _write_routed(repository, "world.actor", _actor_record())
                _write_routed(
                    repository,
                    "world.effect",
                    _effect("effect.transform", ACTOR_ID),
                )
                transformed = _asset(
                    "asset.transformed", owner=ACTOR_ID, equipment="held"
                )
                transformed["state"]["equipment_transform"] = {
                    "source_effect_id": "effect.transform",
                    "transition_occurrence_id": "occ.transform",
                    "mode": mode,
                }
                _write_routed(repository, "world.asset", transformed)
                repository.commit("unqualified equipment transformation")

                with NativeHotStore(":memory:") as store:
                    _host, context = self._host_context(repository, store)
                    with self.assertRaises(activity_contracts.NativePreparationHold):
                        mechanical_sources.prepare_membership(context)

    def _repository(self, root: Path, *, records: bool = True) -> GitCampaignRepository:
        repository = GitCampaignRepository(root)
        repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
        repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
        repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
        _write_routed(repository, "world.actor", _actor_record())
        if records:
            _write_routed(
                repository,
                "world.effect",
                _effect("effect.index-omitted", ACTOR_ID),
            )
            _write_routed(
                repository,
                "world.asset",
                _asset("asset.index-omitted", owner=ACTOR_ID, equipment="held"),
            )
        repository.commit("initial native source")
        return repository

    def _host_context(self, repository, store, *, live=None):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host

        host, _ = _selected_host(store, repository=repository, live=live)
        return host, _context(self.catalog, self.compiled, host)

    def test_absent_record_subtrees_are_proven_empty_and_issued(self):
        from GAME.TOOLS import mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(prefix="sp03-membership-empty-") as temporary:
            repository = self._repository(
                Path(temporary) / "campaign.git", records=False
            )
            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                observation = mechanical_sources.prepare_membership(context)
                self.assertEqual(observation.effects, ())
                self.assertEqual(observation.assets, ())
                self.assertTrue(mechanical_sources.is_membership_issued(observation))
                self.assertTrue(
                    mechanical_sources.revalidate_membership(observation, context)
                )
                self.assertEqual(
                    {coverage.absent_child for coverage in observation.family_coverage},
                    {"RECORDS"},
                )

    def test_source_addition_and_removal_invalidate_old_membership(self):
        from GAME.TOOLS import mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        with tempfile.TemporaryDirectory(prefix="sp03-membership-change-") as temporary:
            repository = self._repository(
                Path(temporary) / "campaign.git", records=False
            )
            with NativeHotStore(":memory:") as store:
                _host, first_context = self._host_context(repository, store)
                first = mechanical_sources.prepare_membership(first_context)
                self.assertEqual(first.effects, ())
                self.assertEqual(first.assets, ())
                self.assertTrue(
                    mechanical_sources.revalidate_membership(first, first_context)
                )

                effect = _effect("effect.added", ACTOR_ID)
                asset = _asset("asset.added", owner=ACTOR_ID)
                _write_routed(repository, "world.effect", effect)
                _write_routed(repository, "world.asset", asset)
                repository.commit("add native members without index updates")
                self.assertFalse(
                    mechanical_sources.revalidate_membership(first, first_context)
                )

                _host, added_context = self._host_context(repository, store)
                added = mechanical_sources.prepare_membership(added_context)
                self.assertEqual(
                    {item.owner_ref.identity[0] for item in added.effects},
                    {"effect.added"},
                )
                self.assertEqual(
                    {item.owner_ref.identity[0] for item in added.assets},
                    {"asset.added"},
                )

                for family, identity in (
                    ("world.effect", "effect.added"),
                    ("world.asset", "asset.added"),
                ):
                    route = route_native_record(family, (identity,))
                    (repository.root / route.relative_path).unlink()
                repository.commit("remove native members without index updates")
                self.assertFalse(
                    mechanical_sources.revalidate_membership(added, added_context)
                )
                _host, removed_context = self._host_context(repository, store)
                removed = mechanical_sources.prepare_membership(removed_context)
                self.assertEqual(removed.effects, ())
                self.assertEqual(removed.assets, ())

    def test_terminal_to_active_candidate_is_revalidated_and_retained(self):
        from GAME.TOOLS import mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-exclusion-"
        ) as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            _write_routed(
                repository,
                "world.effect",
                _effect("effect.terminal", ACTOR_ID, lifecycle="terminal"),
            )
            repository.commit("terminal Effect baseline")
            effect_path = route_native_record(
                "world.effect", ("effect.terminal",)
            ).relative_path

            with NativeHotStore(":memory:") as store:
                _host, terminal_context = self._host_context(repository, store)
                terminal = mechanical_sources.prepare_membership(terminal_context)
                self.assertEqual(terminal.effects, ())
                self.assertEqual(
                    [
                        (item.owner_ref.identity[0], item.reason)
                        for item in terminal.exclusions
                    ],
                    [("effect.terminal", "terminal")],
                )
                repository.write(effect_path, _effect("effect.terminal", ACTOR_ID))
                repository.commit("activate same native Effect")
                self.assertFalse(
                    mechanical_sources.revalidate_membership(terminal, terminal_context)
                )
                _host, active_context = self._host_context(repository, store)
                active = mechanical_sources.prepare_membership(active_context)
                self.assertEqual(
                    {item.owner_ref.identity[0] for item in active.effects},
                    {"effect.terminal"},
                )

    def test_container_closure_blocks_access_and_target_locality_is_preserved(self):
        from GAME.TOOLS import mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-container-"
        ) as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            for record in (
                _asset("asset.pack", owner=ACTOR_ID),
                _asset("asset.pouch", container="asset.pack"),
                _asset("asset.gem", container="asset.pouch"),
                _asset("asset.lockbox", container="asset.pack", access="blocked"),
                _asset("asset.potion", container="asset.lockbox"),
                _asset("asset.cloak", owner=ACTOR_ID, equipment="worn"),
                _asset("asset.other", owner="actor.other"),
            ):
                _write_routed(repository, "world.asset", record)
            for record in (
                _effect("effect.target-local", ACTOR_ID),
                _effect("effect.terminal", ACTOR_ID, lifecycle="terminal"),
                _effect("effect.source-only", "actor.other"),
                _effect("effect.support", "actor.other"),
            ):
                if record["id"] == "effect.source-only":
                    record["state"]["source_id"] = ACTOR_ID
                _write_routed(repository, "world.effect", record)
            supported = _effect("effect.supported", ACTOR_ID)
            supported["state"]["support_effect_id"] = "effect.support"
            supported["state"]["temporal_binding"] = {
                "basis_id": "temporal.metric_deadline",
                "context_id": "scene.sp03",
                "anchor_value": 0,
                "deadline_value": 72,
                "unit_id": "unit.hour",
            }
            _write_routed(repository, "world.effect", supported)
            wrong_subject = _effect("effect.wrong-subject", ACTOR_ID)
            wrong_subject["state"]["subject_binding"] = {
                "domain": "physical",
                "principal_subject_id": "actor.other",
                "physical_actor_id": "actor.other",
                "binding_generation": 2,
            }
            _write_routed(repository, "world.effect", wrong_subject)
            repository.commit("native nested Asset and Effect closure")

            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                observation = mechanical_sources.prepare_membership(context)
                assets = {
                    item.owner_ref.identity[0]: item for item in observation.assets
                }
                self.assertEqual(
                    set(assets),
                    {
                        "asset.pack",
                        "asset.pouch",
                        "asset.gem",
                        "asset.lockbox",
                        "asset.potion",
                        "asset.cloak",
                    },
                )
                self.assertTrue(assets["asset.gem"].accessible)
                self.assertFalse(assets["asset.lockbox"].accessible)
                self.assertEqual(
                    assets["asset.potion"].blocker_asset_id, "asset.lockbox"
                )
                self.assertEqual(assets["asset.cloak"].equipment_mode, "worn")
                self.assertEqual(
                    {item.owner_ref.identity[0] for item in observation.effects},
                    {"effect.target-local", "effect.supported"},
                )
                self.assertEqual(
                    {
                        item.owner_ref.identity[0]
                        for item in observation.effect_dependencies
                    },
                    {"effect.support"},
                )
                self.assertEqual(
                    {
                        item.owner_ref.identity[0]: item.reason
                        for item in observation.exclusions
                    },
                    {
                        "effect.terminal": "terminal",
                        "effect.source-only": "not_target_local",
                        "effect.wrong-subject": "wrong_subject_binding",
                    },
                )

                _write_routed(
                    repository,
                    "world.asset",
                    _asset("asset.gem", container="asset.other"),
                )
                repository.commit("move nested Asset out of the subject closure")
                self.assertFalse(
                    mechanical_sources.revalidate_membership(observation, context)
                )
                _host, moved_context = self._host_context(repository, store)
                moved = mechanical_sources.prepare_membership(moved_context)
                self.assertNotIn(
                    "asset.gem",
                    {item.owner_ref.identity[0] for item in moved.assets},
                )

    def test_missing_parent_and_container_cycle_hold(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        invalid_containers = (
            (_asset("asset.child", container="asset.missing"),),
            (
                _asset("asset.first", container="asset.second"),
                _asset("asset.second", container="asset.first"),
            ),
        )
        for invalid_assets in invalid_containers:
            with (
                self.subTest(invalid_assets=invalid_assets),
                tempfile.TemporaryDirectory(
                    prefix="sp03-membership-container-invalid-"
                ) as temporary,
            ):
                repository = GitCampaignRepository(Path(temporary) / "campaign.git")
                repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
                repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
                repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
                _write_routed(repository, "world.actor", _actor_record())
                _write_routed(
                    repository,
                    "world.asset",
                    _asset("asset.root", owner=ACTOR_ID),
                )
                for record in invalid_assets:
                    _write_routed(repository, "world.asset", record)
                repository.commit("invalid native container closure")

                with NativeHotStore(":memory:") as store:
                    _host, context = self._host_context(repository, store)
                    with self.assertRaises(activity_contracts.NativePreparationHold):
                        mechanical_sources.prepare_membership(context)

    def test_subject_generation_or_wrong_role_does_not_issue_membership(self):
        from dataclasses import replace

        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-subject-"
        ) as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            _write_routed(
                repository,
                "world.effect",
                _effect("effect.wrong-generation", ACTOR_ID),
            )
            record = _effect("effect.wrong-generation", ACTOR_ID)
            record["state"]["subject_binding"] = {
                "domain": "physical",
                "principal_subject_id": ACTOR_ID,
                "physical_actor_id": ACTOR_ID,
                "binding_generation": 2,
            }
            _write_routed(repository, "world.effect", record)
            repository.commit("subject-bound Effect needs unavailable binding issuer")

            with NativeHotStore(":memory:") as store:
                _host, context = self._host_context(repository, store)
                with self.assertRaises(activity_contracts.NativePreparationHold):
                    mechanical_sources.prepare_membership(context)
                with self.assertRaises(activity_contracts.ActivityContractError):
                    replace(
                        context,
                        role_bindings={
                            "actor": NativeOwnerRef("world.asset", ("asset.foreign",))
                        },
                    )

    def test_malformed_tree_and_missing_bounded_acquisition_hold(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-malformed-"
        ) as temporary:
            repository = GitCampaignRepository(Path(temporary) / "campaign.git")
            repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
            repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
            repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
            _write_routed(repository, "world.actor", _actor_record())
            repository.write("WORLD/EFFECTS/RECORDS/not-a-native-route.yaml", {})
            repository.commit("malformed membership path")

            with NativeHotStore(":memory:") as store:
                _host, malformed_context = self._host_context(repository, store)
                with self.assertRaises(activity_contracts.NativePreparationHold):
                    mechanical_sources.prepare_membership(malformed_context)

                repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
                (
                    repository.root / "WORLD/EFFECTS/RECORDS/not-a-native-route.yaml"
                ).unlink()
                repository.commit("restore source tree")
                _host, unavailable_context = self._host_context(repository, store)
                del repository.sp03_git_repository_path
                with self.assertRaises(activity_contracts.NativePreparationHold):
                    mechanical_sources.prepare_membership(unavailable_context)

    def test_malformed_native_payload_holds_instead_of_becoming_absence(self):
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore

        malformed_effects = (
            {
                "id": "effect.unknown-field",
                "mutate": lambda value: value["state"].__setitem__(
                    "unexpected_truth", True
                ),
            },
            {
                "id": "effect.bad-temporal",
                "mutate": lambda value: value["state"].__setitem__(
                    "temporal_binding", {}
                ),
            },
            {
                "id": "effect.executable-details",
                "mutate": lambda value: value["state"].__setitem__(
                    "details", {"subject_binding": "actor.sp03"}
                ),
            },
        )
        for malformed_spec in malformed_effects:
            with (
                self.subTest(effect_id=malformed_spec["id"]),
                tempfile.TemporaryDirectory(
                    prefix="sp03-membership-payload-"
                ) as temporary,
            ):
                repository = GitCampaignRepository(Path(temporary) / "campaign.git")
                repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
                repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
                repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
                _write_routed(repository, "world.actor", _actor_record())
                malformed = _effect(malformed_spec["id"], ACTOR_ID)
                malformed_spec["mutate"](malformed)
                _write_routed(repository, "world.effect", malformed)
                repository.commit("malformed native Effect payload")

                with NativeHotStore(":memory:") as store:
                    _host, context = self._host_context(repository, store)
                    with self.assertRaises(activity_contracts.NativePreparationHold):
                        mechanical_sources.prepare_membership(context)

    def test_raw_hot_rows_do_not_supply_membership_and_live_family_holds(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            SelectedLive,
            _selected_host,
        )
        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.hot_store import NativeHotStore, OwnerDocument
        from GAME.TOOLS.live_state import (
            LiveClaim,
            LiveEnvelope,
            LiveRouting,
            build_live_ref,
            derive_live_epoch_id,
        )

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-live-hot-"
        ) as temporary:
            repository = self._repository(
                Path(temporary) / "campaign.git", records=False
            )
            database_path = Path(temporary) / "working-state.sqlite"
            with NativeHotStore(str(database_path)) as store:
                revision, _tree = repository.commit()
                raw_effect = _effect("effect.raw-hot-only", ACTOR_ID)
                store.stage_owner_document(
                    OwnerDocument(
                        CAMPAIGN_ID,
                        "world.effect",
                        ("effect.raw-hot-only",),
                        raw_effect,
                        revision,
                        1,
                    )
                )
            with NativeHotStore(str(database_path)) as restarted_store:
                _host, context = self._host_context(repository, restarted_store)
                observation = mechanical_sources.prepare_membership(context)
                self.assertEqual(observation.effects, ())
                self.assertTrue(
                    mechanical_sources.revalidate_membership(observation, context)
                )

            claim = LiveClaim.exact_owner("world.effect", "effect.live")
            opening_revision = "b" * 40
            epoch_id = derive_live_epoch_id(
                CAMPAIGN_ID, "scene.sp03", opening_revision, (claim,)
            )
            live_source = LiveEnvelope(
                campaign_id=CAMPAIGN_ID,
                scene_id="scene.sp03",
                epoch_id=epoch_id,
                source_ref=build_live_ref(CAMPAIGN_ID, "scene.sp03", epoch_id),
                source_revision="c" * 40,
                opening_campaign_revision=opening_revision,
                claims=(claim,),
            )
            routing = LiveRouting(campaign_id=CAMPAIGN_ID, entries=(live_source,))
            with NativeHotStore(":memory:") as store:
                live_host, _ = _selected_host(
                    store,
                    repository=repository,
                    live=SelectedLive(route=routing),
                )
                live_context = _context(self.catalog, self.compiled, live_host)
                with self.assertRaises(activity_contracts.NativePreparationHold):
                    mechanical_sources.prepare_membership(live_context)

    def test_copied_mutated_and_rebound_evidence_rejects(self):
        import copy
        from dataclasses import replace

        from GAME.TOOLS import activity_contracts, mechanical_sources
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.hot_store import NativeHotStore

        with tempfile.TemporaryDirectory(
            prefix="sp03-membership-forgery-"
        ) as temporary:
            repository = self._repository(Path(temporary) / "campaign.git")
            with NativeHotStore(":memory:") as store:
                host, context = self._host_context(repository, store)
                self.assertTrue(
                    activity_contracts._preparation_context_is_issued(context)
                )
                unissued = replace(context)
                self.assertFalse(
                    activity_contracts._preparation_context_is_issued(unissued)
                )
                with self.assertRaisesRegex(
                    mechanical_sources.MechanicalSourceError, "source-bound"
                ):
                    mechanical_sources.prepare_membership(unissued)
                observation = mechanical_sources.prepare_membership(context)
                copied = copy.copy(observation)
                self.assertFalse(mechanical_sources.is_membership_issued(copied))
                with self.assertRaises(mechanical_sources.MechanicalSourceError):
                    mechanical_sources.revalidate_membership(copied, context)
                with self.assertRaises(mechanical_sources.MechanicalSourceError):
                    mechanical_sources.revalidate_membership(observation, unissued)

                mutated = copy.copy(observation)
                object.__setattr__(mutated, "effects", ())
                self.assertFalse(mechanical_sources.is_membership_issued(mutated))

                other_context = _context(self.catalog, self.compiled, host)
                with self.assertRaises(mechanical_sources.MechanicalSourceError):
                    mechanical_sources.revalidate_membership(observation, other_context)

                self.assertTrue(mechanical_sources.is_membership_issued(observation))
                self.assertEqual(
                    context.role_bindings["actor"],
                    NativeOwnerRef("world.actor", (ACTOR_ID,)),
                )


if __name__ == "__main__":
    unittest.main()
