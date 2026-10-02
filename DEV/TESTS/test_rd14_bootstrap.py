from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS import bootstrap, init_campaign, native_storage
from GAME.TOOLS.bootstrap import (
    BootstrapContractError,
    CampaignSelection,
    CreatorIdentity,
    authorize_creator,
    build_scaffold_input,
    create_bootstrap_result,
    require_campaign_selection,
)
from GAME.TOOLS.durability import (
    DurabilityPromiseResult,
    NativeDurabilityResult,
    complete_save_promise,
    evaluate_durability,
    freeze_save_promise,
    route_serialized_operation,
)
from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence
from GAME.TOOLS.publication import PublicationOutcome, PublicationStatus

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


def _creator(login: str = "lina") -> CreatorIdentity:
    return CreatorIdentity(stable_github_user_id="U_kgDOBootstrap", login=login)


def _scaffold_input(campaign_branch: str = "campaign/20260916") -> dict[str, object]:
    creation = create_bootstrap_result(
        selection=CampaignSelection.new(),
        storage_repository="github.com/example/campaign-storage",
        pinned_storage_head="a" * 40,
        creator=_creator(),
        mode="multiplayer",
        campaign_branch=campaign_branch,
        created_at="2026-09-16T12:00:00Z",
        engine_version="1.0-alpha",
        package_id="dev-v1.0-alpha",
        source_commit_sha="b" * 40,
        package_sha256="c" * 64,
        ruleset_set_sha256="d" * 64,
        ruleset_set_digest_generation=1,
    )
    return build_scaffold_input(creation)


def _bootstrap_result() -> bootstrap.BootstrapResult:
    return create_bootstrap_result(
        selection=CampaignSelection.new(),
        storage_repository="github.com/example/campaign-storage",
        pinned_storage_head="a" * 40,
        creator=_creator(),
        mode="multiplayer",
        campaign_branch="campaign/20260916",
        created_at="2026-09-16T12:00:00Z",
        engine_version="1.0-alpha",
        package_id="dev-v1.0-alpha",
        source_commit_sha="b" * 40,
        package_sha256="c" * 64,
        ruleset_set_sha256="d" * 64,
        ruleset_set_digest_generation=1,
    )


def _generated_initial_files(
    result: bootstrap.BootstrapResult,
) -> dict[str, bytes]:
    return {
        "MANIFEST.yaml": f"campaign_id: {result.campaign_id}\n".encode(),
        "CAMPAIGN_CARD.yaml": f"campaign_id: {result.campaign_id}\n".encode(),
        "README.md": (ROOT / "GAME" / "CAMPAIGN" / "README.md").read_bytes(),
        "STATE/CURRENT.yaml": b"schema_version: 3\n",
    }


def _run_campaign_generator(
    output: Path,
    result: bootstrap.BootstrapResult,
    *,
    source_root: Path = ROOT / "GAME",
) -> subprocess.CompletedProcess[str]:
    generator = source_root / "TOOLS" / "init_campaign.py"
    if not generator.is_file():
        generator = ROOT / "GAME" / "TOOLS" / "init_campaign.py"
    arguments = [
        sys.executable,
        str(generator),
        "--output",
        str(output),
        "--campaign-id",
        result.campaign_id,
        "--branch",
        result.campaign_branch,
        "--engine-version",
        result.engine_version,
        "--package-id",
        result.package_id,
        "--package-sha256",
        result.package_sha256,
        "--ruleset-set-sha256",
        result.ruleset_set_sha256,
        "--created-at",
        result.created_at,
        "--creator-github-login",
        result.creator.login,
        "--mode",
        result.mode,
        "--source-root",
        str(source_root),
    ]
    if result.source_commit_sha is not None:
        arguments.extend(["--source-commit-sha", result.source_commit_sha])
    return subprocess.run(arguments, capture_output=True, text=True, check=False)


def _copy_campaign_package(destination: Path) -> tuple[Path, Path]:
    source_root = destination / "selected-package"
    source_campaign = source_root / "CAMPAIGN"
    source_campaign.parent.mkdir(parents=True)
    shutil.copytree(ROOT / "GAME" / "CAMPAIGN", source_campaign)
    tools = source_root / "TOOLS"
    tools.mkdir()
    for relative_path in ("init_campaign.py", "native_storage.py"):
        shutil.copy2(ROOT / "GAME" / "TOOLS" / relative_path, tools / relative_path)
    return source_root, source_campaign


def _campaign_file_map(campaign_root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(campaign_root).as_posix(): path.read_bytes()
        for path in sorted(campaign_root.rglob("*"))
        if path.is_file()
    }


def _generate_campaign(
    output: Path,
    result: bootstrap.BootstrapResult | None = None,
    *,
    source_root: Path = ROOT / "GAME",
) -> tuple[bootstrap.BootstrapResult, subprocess.CompletedProcess[str]]:
    frozen_identity = _bootstrap_result() if result is None else result
    completed = _run_campaign_generator(
        output, frozen_identity, source_root=source_root
    )
    return frozen_identity, completed


class CampaignSelectionBarrierTests(unittest.TestCase):
    def test_missing_selection_fails_closed_without_inferring_a_sole_candidate(
        self,
    ) -> None:
        with self.assertRaisesRegex(BootstrapContractError, "selection"):
            require_campaign_selection(None)

    def test_explicit_existing_or_new_selection_is_typed_and_unambiguous(self) -> None:
        self.assertEqual(
            CampaignSelection.existing("campaign.frostfall").kind, "existing"
        )
        self.assertEqual(CampaignSelection.new().kind, "new")
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="existing", campaign_id=None)
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="new", campaign_id="campaign.frostfall")
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="implicit", campaign_id=None)  # type: ignore[arg-type]


class InitialCampaignPublicationTests(unittest.TestCase):
    def test_bootstrap_module_version_tracks_material_publication_contract(
        self,
    ) -> None:
        self.assertEqual(getattr(bootstrap, "FRAMEWORK_MODULE_VERSION", None), "1.0.3")

    def test_freeze_initial_publication_copies_exact_generated_file_identity(
        self,
    ) -> None:
        freeze = getattr(bootstrap, "freeze_initial_campaign_publication", None)
        self.assertTrue(
            callable(freeze),
            "bootstrap must expose its initial campaign publication freeze",
        )
        if not callable(freeze):
            return

        result = _bootstrap_result()
        generated_files = _generated_initial_files(result)
        attempt = freeze(result, generated_files)
        generated_files["STATE/CURRENT.yaml"] = b"changed after freeze"

        self.assertIs(attempt.bootstrap_result, result)
        self.assertEqual(
            attempt.generated_files["STATE/CURRENT.yaml"], b"schema_version: 3\n"
        )
        self.assertEqual(
            attempt.generated_files_fingerprint,
            (
                ("CAMPAIGN_CARD.yaml", f"campaign_id: {result.campaign_id}\n".encode()),
                ("MANIFEST.yaml", f"campaign_id: {result.campaign_id}\n".encode()),
                (
                    "README.md",
                    (ROOT / "GAME" / "CAMPAIGN" / "README.md").read_bytes(),
                ),
                ("STATE/CURRENT.yaml", b"schema_version: 3\n"),
            ),
        )

    def test_absent_ref_creates_one_scratch_tree_one_parented_commit_and_ref(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment()

        bootstrap.discover_campaign_page(deployment)
        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(
            deployment.list_calls, [(None, bootstrap.MAX_CAMPAIGN_REFS_PER_PAGE)]
        )
        self.assertEqual(
            deployment.resolved_storage_basis,
            (result.storage_repository, result.pinned_storage_head),
        )
        self.assertEqual(
            deployment.principal.principal_id, result.creator.stable_github_user_id
        )
        self.assertEqual(
            deployment.operations,
            [
                "repository_identity",
                "resolve_authenticated_storage_principal",
                "read_ref_state",
                "create_tree_from_scratch",
                "create_single_parent_commit",
                "create_ref_if_absent",
            ],
        )
        self.assertEqual(len(deployment.tree_calls), 1)
        self.assertEqual(len(deployment.commit_calls), 1)
        self.assertEqual(len(deployment.create_ref_calls), 1)
        self.assertEqual(
            deployment.create_ref_calls,
            [(result.campaign_branch, deployment.commit_sha)],
        )

    def test_initialization_commit_has_only_the_pinned_storage_head_as_parent(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment()

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(
            publication.attempt.initialization_commit_sha, deployment.commit_sha
        )
        self.assertEqual(
            deployment.commit_calls,
            [(result.pinned_storage_head, deployment.tree_sha, result.campaign_branch)],
        )
        self.assertEqual(
            deployment.commits[deployment.commit_sha]["parents"],
            [result.pinned_storage_head],
        )

    def test_scratch_tree_passes_campaign_readme_unchanged_without_storage_marker(
        self,
    ) -> None:
        result = _bootstrap_result()
        generated_files = _generated_initial_files(result)
        attempt = bootstrap.freeze_initial_campaign_publication(result, generated_files)
        deployment = _InitialPublicationDeployment()

        bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(deployment.tree_files, [generated_files])
        self.assertEqual(
            deployment.tree_files[0]["README.md"],
            (ROOT / "GAME" / "CAMPAIGN" / "README.md").read_bytes(),
        )
        self.assertNotIn("DND_STORAGE.yaml", deployment.tree_files[0])
        self.assertFalse(
            any(
                path == "DND_STORAGE" or path.startswith("DND_STORAGE/")
                for path in deployment.tree_files[0]
            )
        )

    def test_freeze_rejects_storage_marker_file_and_directory_paths(self) -> None:
        result = _bootstrap_result()
        files = _generated_initial_files(result)

        for path in ("DND_STORAGE.yaml", "DND_STORAGE/owner.yaml"):
            with (
                self.subTest(path=path),
                self.assertRaisesRegex(BootstrapContractError, "storage-root files"),
            ):
                bootstrap.freeze_initial_campaign_publication(
                    result, files | {path: b"storage marker"}
                )

    def test_preexisting_target_conflicts_without_any_write(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(bootstrap.InitialCampaignRefState.present("e" * 40),)
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.CONFLICT)
        self.assertEqual(deployment.tree_calls, [])
        self.assertEqual(deployment.commit_calls, [])
        self.assertEqual(deployment.create_ref_calls, [])

    def test_existing_target_without_exact_initialization_proof_conflicts(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(bootstrap.InitialCampaignRefState.present("f" * 40),),
            existing_commit_sha="f" * 40,
            existing_tree_files=attempt.generated_files,
            existing_parent_sha=result.pinned_storage_head,
        )
        deployment.commits["f" * 40] = {
            "revision": "f" * 40,
            "tree_sha": deployment.existing_tree_sha,
        }

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertIs(publication.outcome.status, PublicationStatus.CONFLICT)
        self.assertEqual(deployment.tree_calls, [])
        self.assertEqual(deployment.commit_calls, [])
        self.assertEqual(deployment.create_ref_calls, [])

    def test_exact_existing_initialization_can_be_adopted_without_writes(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(bootstrap.InitialCampaignRefState.present("f" * 40),),
            existing_commit_sha="f" * 40,
            existing_tree_files=attempt.generated_files,
            existing_parent_sha=result.pinned_storage_head,
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(publication.outcome.observed_head_sha, "f" * 40)
        self.assertEqual(deployment.tree_calls, [])
        self.assertEqual(deployment.commit_calls, [])
        self.assertEqual(deployment.create_ref_calls, [])

    def test_existing_initialization_with_different_commit_tree_or_identity_conflicts(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        prepared = bootstrap.publish_initial_campaign(
            _InitialPublicationDeployment(), attempt
        ).attempt
        files = dict(prepared.generated_files)
        wrong_identity = dict(files)
        wrong_identity["MANIFEST.yaml"] = b"campaign_id: campaign.other\n"
        wrong_tree = dict(files)
        wrong_tree["STATE/CURRENT.yaml"] = b"schema_version: 2\n"

        cases = (
            (
                "different commit",
                _InitialPublicationDeployment(
                    ref_states=(bootstrap.InitialCampaignRefState.present("9" * 40),),
                    existing_commit_sha="9" * 40,
                    existing_tree_files=files,
                    existing_parent_sha=result.pinned_storage_head,
                ),
            ),
            (
                "different tree",
                _InitialPublicationDeployment(
                    ref_states=(
                        bootstrap.InitialCampaignRefState.present(
                            prepared.initialization_commit_sha
                        ),
                    ),
                    existing_commit_sha=prepared.initialization_commit_sha,
                    existing_tree_files=wrong_tree,
                    existing_parent_sha=result.pinned_storage_head,
                    existing_tree_sha="8" * 40,
                ),
            ),
            (
                "different campaign identity",
                _InitialPublicationDeployment(
                    ref_states=(
                        bootstrap.InitialCampaignRefState.present(
                            prepared.initialization_commit_sha
                        ),
                    ),
                    existing_commit_sha=prepared.initialization_commit_sha,
                    existing_tree_files=wrong_identity,
                    existing_parent_sha=result.pinned_storage_head,
                ),
            ),
        )
        for label, deployment in cases:
            with self.subTest(label=label):
                publication = bootstrap.publish_initial_campaign(deployment, prepared)
                self.assertEqual(publication.outcome.status, PublicationStatus.CONFLICT)
                self.assertEqual(deployment.tree_calls, [])
                self.assertEqual(deployment.commit_calls, [])
                self.assertEqual(deployment.create_ref_calls, [])

    def test_create_if_absent_race_loss_never_overwrites_or_uses_force(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.CONFLICT,
                    "2" * 40,
                    "3" * 40,
                    "INITIAL_REF_ALREADY_EXISTS",
                    True,
                ),
            )
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.CONFLICT)
        self.assertEqual(
            deployment.create_ref_calls,
            [(result.campaign_branch, deployment.commit_sha)],
        )
        self.assertEqual(deployment.update_ref_calls, [])

    def test_indeterminate_result_reconciles_exact_target_to_accepted(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.present("2" * 40),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.INDETERMINATE,
                    "2" * 40,
                    None,
                    "INDETERMINATE",
                    True,
                ),
            ),
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(publication.outcome.observed_head_sha, "2" * 40)
        self.assertEqual(deployment.ref_read_count, 2)
        self.assertEqual(
            deployment.exact_commit_reads, [(result.campaign_branch, "2" * 40)]
        )

    def test_indeterminate_result_with_authoritative_absence_is_not_acknowledged(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.INDETERMINATE,
                    "2" * 40,
                    None,
                    "INDETERMINATE",
                    True,
                ),
            ),
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(publication.outcome.cause, "CONFIRMED_NOT_PUBLISHED")
        self.assertFalse(publication.outcome.acknowledged)
        self.assertEqual(deployment.ref_read_count, 2)

    def test_indeterminate_result_with_different_target_head_is_conflict(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.present("4" * 40),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.INDETERMINATE,
                    "2" * 40,
                    None,
                    "INDETERMINATE",
                    True,
                ),
            ),
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.CONFLICT)
        self.assertEqual(deployment.exact_commit_reads, [])

    def test_malformed_transport_outcome_is_reconciled_not_acknowledged(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    "accepted",  # type: ignore[arg-type]
                    "2" * 40,
                    "2" * 40,
                    "UNTRUSTED_ACCEPTANCE",
                    True,
                ),
            ),
        )

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertIs(publication.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(publication.outcome.cause, "CONFIRMED_NOT_PUBLISHED")
        self.assertEqual(deployment.ref_read_count, 2)

    def test_missing_create_if_absent_capability_fails_closed_without_update_ref(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment()
        deployment.create_ref_if_absent = None

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(
            publication.outcome.cause, "INITIAL_PUBLICATION_CAPABILITY_UNAVAILABLE"
        )
        self.assertEqual(deployment.operations, [])
        self.assertEqual(deployment.update_ref_calls, [])

    def test_ordinary_update_ref_is_not_used_as_initial_ref_creation(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment()
        deployment.create_ref_if_absent = None

        publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(deployment.update_ref_calls, [])
        self.assertEqual(deployment.create_ref_calls, [])

    def test_repository_or_authenticated_principal_mismatch_rejects_before_write(
        self,
    ) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        mismatches = (
            _InitialPublicationDeployment(repository_id="github.com/example/other"),
            _InitialPublicationDeployment(
                principal=AuthenticatedPrincipalEvidence("U_other")
            ),
        )
        for deployment in mismatches:
            with self.subTest(
                repository=deployment.repo_id, principal=deployment.principal
            ):
                publication = bootstrap.publish_initial_campaign(deployment, attempt)
                self.assertEqual(publication.outcome.status, PublicationStatus.REJECTED)
                self.assertEqual(deployment.tree_calls, [])
                self.assertEqual(deployment.commit_calls, [])
                self.assertEqual(deployment.create_ref_calls, [])

    def test_retry_reuses_frozen_identity_tree_and_initialization_commit(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.INDETERMINATE,
                    "2" * 40,
                    None,
                    "INDETERMINATE",
                    True,
                ),
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    "2" * 40,
                    "2" * 40,
                    "CONFIRMED_ACCEPTED",
                    True,
                ),
            ),
        )

        first = bootstrap.publish_initial_campaign(deployment, attempt)
        retry = bootstrap.publish_initial_campaign(deployment, first.attempt)

        self.assertEqual(first.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(retry.outcome.status, PublicationStatus.ACCEPTED)
        self.assertIs(first.attempt.bootstrap_result, result)
        self.assertIs(retry.attempt.bootstrap_result, result)
        self.assertEqual(
            first.attempt.generated_files_fingerprint,
            attempt.generated_files_fingerprint,
        )
        self.assertEqual(
            retry.attempt.initialization_commit_sha,
            first.attempt.initialization_commit_sha,
        )
        self.assertEqual(len(deployment.tree_calls), 1)
        self.assertEqual(len(deployment.commit_calls), 1)
        self.assertEqual(
            deployment.create_ref_calls,
            [
                (result.campaign_branch, first.attempt.initialization_commit_sha),
                (result.campaign_branch, first.attempt.initialization_commit_sha),
            ],
        )

    def test_unproven_prepared_commit_cannot_be_published(self) -> None:
        result = _bootstrap_result()
        attempt = bootstrap.freeze_initial_campaign_publication(
            result, _generated_initial_files(result)
        )
        forged = replace(
            attempt,
            tree_sha="1" * 40,
            initialization_commit_sha="2" * 40,
        )
        deployment = _InitialPublicationDeployment()

        publication = bootstrap.publish_initial_campaign(deployment, forged)

        self.assertIsNot(publication.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(deployment.create_ref_calls, [])


class CreationIdentityTests(unittest.TestCase):
    def test_creation_allocates_one_canonical_campaign_identity_before_scaffold_input(
        self,
    ) -> None:
        scaffold_input = _scaffold_input()

        self.assertRegex(
            str(scaffold_input["campaign_id"]), r"^campaign\.[0-9a-f]{32}$"
        )
        self.assertEqual(scaffold_input["creator_github_login"], "lina")
        self.assertEqual(scaffold_input["campaign_branch"], "campaign/20260916")
        self.assertEqual(scaffold_input.get("ruleset_set_digest_generation"), 1)

    def test_creation_accepts_the_first_admitted_collision_suffix(self) -> None:
        self.assertEqual(
            _scaffold_input("campaign/20260916-02")["campaign_branch"],
            "campaign/20260916-02",
        )

    def test_creation_rejects_missing_or_ambiguous_identity_material(self) -> None:
        with self.assertRaises(BootstrapContractError):
            create_bootstrap_result(
                selection=CampaignSelection.new(),
                storage_repository="github.com/example/campaign-storage",
                pinned_storage_head="not-a-sha",
                creator=_creator(),
                mode="singleplayer",
                campaign_branch="campaign/20260916",
                created_at="2026-09-16T12:00:00Z",
                engine_version="1.0-alpha",
                package_id="dev-v1.0-alpha",
                source_commit_sha=None,
                package_sha256="c" * 64,
                ruleset_set_sha256="d" * 64,
                ruleset_set_digest_generation=1,
            )
        with self.assertRaisesRegex(BootstrapContractError, "digest generation"):
            create_bootstrap_result(
                selection=CampaignSelection.new(),
                storage_repository="github.com/example/campaign-storage",
                pinned_storage_head="a" * 40,
                creator=_creator(),
                mode="singleplayer",
                campaign_branch="campaign/20260916-02",
                created_at="2026-09-16T12:00:00Z",
                engine_version="1.0-alpha",
                package_id="dev-v1.0-alpha",
                source_commit_sha=None,
                package_sha256="c" * 64,
                ruleset_set_sha256="d" * 64,
                ruleset_set_digest_generation=2,
            )
        for invalid_generation in (True, 1.0):
            with self.subTest(invalid_generation=invalid_generation):
                with self.assertRaisesRegex(
                    BootstrapContractError, "digest generation"
                ):
                    create_bootstrap_result(
                        selection=CampaignSelection.new(),
                        storage_repository="github.com/example/campaign-storage",
                        pinned_storage_head="a" * 40,
                        creator=_creator(),
                        mode="singleplayer",
                        campaign_branch="campaign/20260916-02",
                        created_at="2026-09-16T12:00:00Z",
                        engine_version="1.0-alpha",
                        package_id="dev-v1.0-alpha",
                        source_commit_sha=None,
                        package_sha256="c" * 64,
                        ruleset_set_sha256="d" * 64,
                        ruleset_set_digest_generation=invalid_generation,  # type: ignore[arg-type]
                    )
        with self.assertRaises(BootstrapContractError):
            create_bootstrap_result(
                selection=CampaignSelection.new(),
                storage_repository="github.com/example/campaign-storage",
                pinned_storage_head="a" * 40,
                creator=_creator(),
                mode="singleplayer",
                campaign_branch="campaign/20260916",
                created_at="2026-09-16",
                engine_version="1.0-alpha",
                package_id="dev-v1.0-alpha",
                source_commit_sha=None,
                package_sha256="c" * 64,
                ruleset_set_sha256="d" * 64,
                ruleset_set_digest_generation=1,
            )
        with self.assertRaises(BootstrapContractError):
            create_bootstrap_result(
                selection=CampaignSelection.new(),
                storage_repository="github.com/example/campaign-storage",
                pinned_storage_head="a" * 40,
                creator=_creator(),
                mode="singleplayer",
                campaign_branch="campaign/20260916-01",
                created_at="2026-09-16T12:00:00Z",
                engine_version="1.0-alpha",
                package_id="dev-v1.0-alpha",
                source_commit_sha=None,
                package_sha256="c" * 64,
                ruleset_set_sha256="d" * 64,
                ruleset_set_digest_generation=1,
            )


class GeneratorScaffoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_scaffold_input_is_bounded_and_contains_every_generator_identity_input(
        self,
    ) -> None:
        scaffold_input = _scaffold_input()

        Draft202012Validator(
            self.schemas["bootstrap-request.schema.json"], registry=self.registry
        ).validate(scaffold_input)
        self.assertEqual(
            set(scaffold_input),
            {
                "campaign_id",
                "campaign_branch",
                "created_at",
                "creator_github_login",
                "mode",
                "engine_version",
                "package_id",
                "source_commit_sha",
                "package_sha256",
                "ruleset_set_sha256",
                "ruleset_set_digest_generation",
            },
        )

    def test_scaffold_input_rejects_unknown_fields(self) -> None:
        invalid = _scaffold_input() | {"creator_email": "lina@example.test"}
        validator = Draft202012Validator(
            self.schemas["bootstrap-request.schema.json"], registry=self.registry
        )

        with self.assertRaises(ValidationError):
            validator.validate(invalid)

    def test_scaffold_input_rejects_an_incompatible_ruleset_digest_generation(
        self,
    ) -> None:
        invalid = _scaffold_input() | {"ruleset_set_digest_generation": 2}
        validator = Draft202012Validator(
            self.schemas["bootstrap-request.schema.json"], registry=self.registry
        )

        with self.assertRaises(ValidationError):
            validator.validate(invalid)

    def test_generator_writes_current_v3_and_exact_identity_to_all_five_companions(
        self,
    ) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "campaign"
            campaign, completed = _generate_campaign(output, result)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(output.is_dir())
            self.assertEqual(campaign.campaign_id, result.campaign_id)

            current = yaml.safe_load(
                (output / "STATE" / "CURRENT.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(current["schema_version"], 3)
            self.assertEqual(current["campaign_id"], result.campaign_id)
            self.assertEqual(current["world_time"], {"display": None})
            self.assertEqual(current["active_scenes"], [])
            self.assertEqual(current["active_threads"], [])

            companion_paths = (
                "STATE/CURRENT.yaml",
                "STATE/ID_ALLOCATOR.yaml",
                "STATE/RUNTIME/LIVE_ROUTING.yaml",
                "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml",
                "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml",
            )
            for relative_path in companion_paths:
                with self.subTest(relative_path=relative_path):
                    value = yaml.safe_load(
                        (output / relative_path).read_text(encoding="utf-8")
                    )
                    self.assertEqual(value["campaign_id"], result.campaign_id)
                    if relative_path == "STATE/ID_ALLOCATOR.yaml":
                        self.assertEqual(value["counters"], {})
                    if relative_path in {
                        "STATE/RUNTIME/LIVE_ROUTING.yaml",
                        "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml",
                    }:
                        self.assertTrue(value["complete"])
                        self.assertEqual(value["entries"], [])

            manifest = yaml.safe_load(
                (output / "MANIFEST.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], 4)
            self.assertEqual(manifest["players"]["player_ids"], [])

    def test_generator_copies_only_selected_package_campaign_bytes_and_readme(
        self,
    ) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_root, source_campaign = _copy_campaign_package(
                Path(temporary_directory)
            )
            expected_readme = b"Selected campaign README\n"
            (source_campaign / "README.md").write_bytes(expected_readme)
            (source_root / "README.md").write_text(
                "Storage-root README must not be copied\n", encoding="utf-8"
            )
            (source_root / "DND_STORAGE.yaml").write_text(
                "storage marker must not be copied\n", encoding="utf-8"
            )
            engine_file = source_root / "CORE" / "ENGINE_SENTINEL.md"
            engine_file.parent.mkdir()
            engine_file.write_text("engine file", encoding="utf-8")

            output = Path(temporary_directory) / "campaign"
            _, completed = _generate_campaign(output, result, source_root=source_root)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual((output / "README.md").read_bytes(), expected_readme)
            self.assertFalse((output / "DND_STORAGE.yaml").exists())
            self.assertFalse((output / "CORE").exists())
            self.assertNotEqual(
                (output / "README.md").read_bytes(),
                (source_root / "README.md").read_bytes(),
            )


class GeneratorConsumerProjectionTests(unittest.TestCase):
    def test_generated_current_record_matches_current_state_v3_owner(self) -> None:
        schema = yaml.safe_load(
            (ROOT / "GAME" / "SCHEMA" / "current_state.schema.yaml").read_text(
                encoding="utf-8"
            )
        )
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "campaign"
            _, completed = _generate_campaign(output, result)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            current = yaml.safe_load(
                (output / "STATE" / "CURRENT.yaml").read_text(encoding="utf-8")
            )

        self.assertEqual(current["schema_version"], schema["schema_version"])
        self.assertEqual(set(current), set(schema["required"]))
        self.assertEqual(set(current["world_time"]), {"display"})
        self.assertEqual(current["campaign_id"], result.campaign_id)

    def test_catalog_census_and_current_native_root_owner_map_are_exact(self) -> None:
        catalog = json.loads(
            (ROOT / "DEV" / "CATALOG" / "core-catalog.json").read_text(encoding="utf-8")
        )
        registries = catalog["registries"]
        world_families = set(registries["world_record_kinds"])
        runtime_families = set(registries["runtime_record_kinds"])

        self.assertEqual(len(world_families), 17)
        self.assertEqual(len(runtime_families), 17)
        self.assertEqual(
            world_families | runtime_families,
            (set(native_storage.FAMILY_ROOTS) - {"world.faction"})
            | {"runtime.id_allocator"},
        )
        self.assertNotIn("world.faction", world_families)
        self.assertIn("organization.faction", registries["organization_facets"])


class BlankScaffoldCompletenessTests(unittest.TestCase):
    def test_generated_blank_campaign_has_every_native_root_and_companion(self) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "campaign"
            _, completed = _generate_campaign(output, result)

            self.assertEqual(completed.returncode, 0, completed.stderr)

            missing_roots = sorted(
                root
                for root in set(native_storage.FAMILY_ROOTS.values())
                if not (output / root).is_dir()
            )
            self.assertEqual(missing_roots, [])
            self.assertTrue((output / "STATE" / "ID_ALLOCATOR.yaml").is_file())

            index_files = {
                "EVENT_INDEX.yaml",
                "FACTION_INDEX.yaml",
                "ITEM_INDEX.yaml",
                "LOCATION_INDEX.yaml",
                "LORE_INDEX.yaml",
                "NPC_INDEX.yaml",
                "PC_INDEX.yaml",
                "PLAYER_INDEX.yaml",
                "SCENE_INDEX.yaml",
                "THREAD_INDEX.yaml",
            }
            self.assertEqual(
                {path.name for path in (output / "INDEX").iterdir()}, index_files
            )
            for root in (
                "STORY/EVENTS",
                "STORY/MECHANICS",
                "STORY/NARRATIVE",
                "STORY/TRANSCRIPT",
                "DRAMATURG/PLAYERS",
            ):
                self.assertTrue((output / root).is_dir(), root)
            self.assertTrue((output / "DRAMATURG" / "SHARED.yaml").is_file())

            routing = yaml.safe_load(
                (
                    output / "STATE" / "RUNTIME" / "RECOVERY_ROOTS" / "ROUTING.yaml"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(routing["campaign_id"], result.campaign_id)
            self.assertTrue(routing["complete"])
            self.assertEqual(routing["roots"], [])

            manifest = yaml.safe_load(
                (output / "MANIFEST.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], 4)
            self.assertEqual(manifest["players"]["player_ids"], [])


class _FakeCampaignDiscoveryProvider:
    def __init__(
        self,
        *,
        refs: tuple[object, ...],
        more_available: bool,
        continuation: str | None,
        files: dict[tuple[str, str], object],
        exact: dict[str, object],
        limitation: object | None,
    ) -> None:
        self.refs = refs
        self.more_available = more_available
        self.continuation = continuation
        self.files = files
        self.exact = exact
        self.limitation = limitation
        self.list_calls: list[tuple[str | None, int]] = []
        self.exact_lookups: list[str] = []
        self.file_reads: list[tuple[str, str]] = []

    def list_campaign_refs(self, *, continuation: str | None, limit: int) -> object:
        self.list_calls.append((continuation, limit))
        return bootstrap.CampaignRefPage(
            references=self.refs,
            more_available=self.more_available,
            continuation=self.continuation,
            inability=self.limitation,
        )

    def resolve_campaign_ref(self, *, campaign_id: str) -> object | None:
        self.exact_lookups.append(campaign_id)
        return self.exact.get(campaign_id)

    def read_campaign_file(self, *, ref: object, path: str) -> object | None:
        branch = ref.branch
        self.file_reads.append((branch, path))
        return self.files.get((branch, path))


class _InitialPublicationDeployment(_FakeCampaignDiscoveryProvider):
    """One fake discovery/storage/publication adapter with exact call evidence."""

    def __init__(
        self,
        *,
        repository_id: str = "github.com/example/campaign-storage",
        principal: AuthenticatedPrincipalEvidence | None = None,
        ref_states: tuple[object, ...] = (),
        create_ref_outcomes: tuple[PublicationOutcome, ...] = (),
        existing_commit_sha: str | None = None,
        existing_tree_files: object | None = None,
        existing_parent_sha: str = "a" * 40,
        existing_tree_sha: str = "1" * 40,
    ) -> None:
        super().__init__(
            refs=(),
            more_available=False,
            continuation=None,
            files={},
            exact={},
            limitation=None,
        )
        self.repo_id = repository_id
        self.principal = principal or AuthenticatedPrincipalEvidence("U_kgDOBootstrap")
        self.ref_states = list(ref_states)
        self.create_ref_outcomes = list(create_ref_outcomes)
        self.existing_commit_sha = existing_commit_sha
        self.existing_tree_files = existing_tree_files
        self.existing_parent_sha = existing_parent_sha
        self.existing_tree_sha = existing_tree_sha
        self.operations: list[str] = []
        self.tree_calls: list[dict[str, bytes]] = []
        self.tree_files: list[dict[str, bytes]] = []
        self.commit_calls: list[tuple[str, str, str]] = []
        self.create_ref_calls: list[tuple[str, str]] = []
        self.update_ref_calls: list[tuple[str, str, bool]] = []
        self.exact_commit_reads: list[tuple[str, str]] = []
        self.ref_read_count = 0
        self.tree_sha = "1" * 40
        self.commit_sha = "2" * 40
        self.commits: dict[str, dict[str, object]] = {}
        if existing_commit_sha is not None:
            self.commits[existing_commit_sha] = {
                "revision": existing_commit_sha,
                "tree_sha": existing_tree_sha,
                "parents": [existing_parent_sha],
                "files": dict(existing_tree_files or {}),
            }

    def repository_identity(self) -> str:
        self.operations.append("repository_identity")
        return self.repo_id

    def resolve_authenticated_storage_principal(
        self, storage_repository: str, pinned_storage_head: str
    ) -> AuthenticatedPrincipalEvidence:
        self.operations.append("resolve_authenticated_storage_principal")
        self.resolved_storage_basis = (storage_repository, pinned_storage_head)
        return self.principal

    def read_ref_state(self, target_campaign_ref: str) -> object:
        self.operations.append("read_ref_state")
        self.ref_read_count += 1
        if self.ref_states:
            return self.ref_states.pop(0)
        return bootstrap.InitialCampaignRefState.absent()

    def create_tree_from_scratch(self, exact_generated_files: object) -> str:
        self.operations.append("create_tree_from_scratch")
        copied = dict(exact_generated_files)
        self.tree_calls.append(copied)
        self.tree_files.append(copied)
        return self.tree_sha

    def create_single_parent_commit(
        self, parent_sha: str, tree_sha: str, target_ref: str
    ) -> str:
        self.operations.append("create_single_parent_commit")
        self.commit_calls.append((parent_sha, tree_sha, target_ref))
        self.commits[self.commit_sha] = {
            "revision": self.commit_sha,
            "tree_sha": tree_sha,
            "parents": [parent_sha],
            "files": dict(self.tree_files[-1]),
        }
        return self.commit_sha

    def create_ref_if_absent(
        self, target_campaign_ref: str, exact_commit_sha: str
    ) -> PublicationOutcome:
        self.operations.append("create_ref_if_absent")
        self.create_ref_calls.append((target_campaign_ref, exact_commit_sha))
        if self.create_ref_outcomes:
            return self.create_ref_outcomes.pop(0)
        return PublicationOutcome(
            PublicationStatus.ACCEPTED,
            exact_commit_sha,
            exact_commit_sha,
            "CONFIRMED_ACCEPTED",
            True,
        )

    def read_exact_commit(
        self, target_campaign_ref: str, exact_commit_sha: str
    ) -> object:
        self.exact_commit_reads.append((target_campaign_ref, exact_commit_sha))
        return self.commits[exact_commit_sha]

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        self.update_ref_calls.append((target_ref, new_commit_sha, force))
        raise AssertionError("ordinary update_ref must never publish an initial ref")


class InitialPublicationTests(unittest.TestCase):
    def test_exact_generated_file_map_is_published_through_accepted_p1_capability(
        self,
    ) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "campaign"
            _, completed = _generate_campaign(output, result)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated_files = init_campaign.validate_generated_scaffold(
                output, result.campaign_id
            )

            attempt = bootstrap.freeze_initial_campaign_publication(
                result, generated_files
            )
            deployment = _InitialPublicationDeployment()
            publication = bootstrap.publish_initial_campaign(deployment, attempt)

        self.assertEqual(publication.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(dict(publication.attempt.generated_files), generated_files)
        self.assertEqual(deployment.tree_files, [generated_files])
        self.assertEqual(
            deployment.tree_files[0]["README.md"],
            (ROOT / "GAME" / "CAMPAIGN" / "README.md").read_bytes(),
        )
        self.assertNotIn("DND_STORAGE.yaml", generated_files)
        self.assertIn("STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml", generated_files)


class FailureRetryTests(unittest.TestCase):
    def test_missing_identity_companion_fails_before_output_and_can_retry_same_root(
        self,
    ) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_root, source_campaign = _copy_campaign_package(
                Path(temporary_directory)
            )
            allocator = source_campaign / "STATE" / "ID_ALLOCATOR.yaml"
            original_allocator = allocator.read_bytes()
            allocator.write_bytes(
                original_allocator.replace(b"campaign_id: null", b"campaign_id: stale")
            )
            output = Path(temporary_directory) / "campaign"

            invalid = _run_campaign_generator(output, result, source_root=source_root)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertFalse(output.exists())

            allocator.write_bytes(original_allocator)
            retry = _run_campaign_generator(output, result, source_root=source_root)
            self.assertEqual(retry.returncode, 0, retry.stderr)
            self.assertTrue((output / "STATE" / "ID_ALLOCATOR.yaml").is_file())

    def test_populated_blank_routing_companion_fails_before_output(self) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_root, source_campaign = _copy_campaign_package(
                Path(temporary_directory)
            )
            live_routing = source_campaign / "STATE" / "RUNTIME" / "LIVE_ROUTING.yaml"
            live_routing.write_bytes(
                live_routing.read_bytes().replace(
                    b"entries: []", b"entries: [unexpected]"
                )
            )
            output = Path(temporary_directory) / "campaign"

            completed = _run_campaign_generator(output, result, source_root=source_root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    def test_indeterminate_p1_retry_reuses_generated_file_map_and_commit(self) -> None:
        result = _bootstrap_result()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "campaign"
            _, completed = _generate_campaign(output, result)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated_files = _campaign_file_map(output)

        deployment = _InitialPublicationDeployment(
            ref_states=(
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
                bootstrap.InitialCampaignRefState.absent(),
            ),
            create_ref_outcomes=(
                PublicationOutcome(
                    PublicationStatus.INDETERMINATE,
                    "2" * 40,
                    None,
                    "INDETERMINATE",
                    True,
                ),
                PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    "2" * 40,
                    "2" * 40,
                    "CONFIRMED_ACCEPTED",
                    True,
                ),
            ),
        )
        attempt = bootstrap.freeze_initial_campaign_publication(result, generated_files)

        first = bootstrap.publish_initial_campaign(deployment, attempt)
        retry = bootstrap.publish_initial_campaign(deployment, first.attempt)

        self.assertEqual(first.outcome.status, PublicationStatus.REJECTED)
        self.assertEqual(retry.outcome.status, PublicationStatus.ACCEPTED)
        self.assertEqual(
            retry.attempt.generated_files_fingerprint,
            attempt.generated_files_fingerprint,
        )
        self.assertEqual(
            retry.attempt.initialization_commit_sha,
            first.attempt.initialization_commit_sha,
        )
        self.assertEqual(len(deployment.tree_calls), 1)
        self.assertEqual(len(deployment.commit_calls), 1)
        self.assertEqual(
            deployment.create_ref_calls,
            [
                (result.campaign_branch, first.attempt.initialization_commit_sha),
                (result.campaign_branch, first.attempt.initialization_commit_sha),
            ],
        )
        self.assertEqual(deployment.update_ref_calls, [])


class BoundedCampaignDiscoveryTests(unittest.TestCase):
    def _ref(self, branch: str) -> bootstrap.CampaignRef:
        return bootstrap.CampaignRef(branch=branch)

    def _card(self, campaign_id: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "campaign_id": campaign_id,
            "campaign_name": f"Name for {campaign_id}",
            "mode": "singleplayer",
            "status": "active",
            "engine_version": "1.0-alpha",
            "protagonist": {"name": None, "role_race": None},
            "multiplayer": None,
        }

    def _manifest(self, branch: str, campaign_id: str) -> dict[str, object]:
        return {
            "schema_version": 4,
            "campaign_id": campaign_id,
            "campaign_name": f"Manifest name for {campaign_id}",
            "branch": branch,
            "mode": "singleplayer",
            "status": "paused",
        }

    def _provider(
        self,
        refs: tuple[bootstrap.CampaignRef, ...],
        *,
        more_available: bool = False,
        continuation: str | None = None,
        files: dict[tuple[str, str], object] | None = None,
        exact: dict[str, bootstrap.CampaignRef] | None = None,
        limitation: bootstrap.CampaignDiscoveryInability | None = None,
    ) -> _FakeCampaignDiscoveryProvider:
        return _FakeCampaignDiscoveryProvider(
            refs=refs,
            more_available=more_available,
            continuation=continuation,
            files={} if files is None else files,
            exact={} if exact is None else exact,
            limitation=limitation,
        )

    def test_discovery_returns_one_bounded_page_and_exposes_continuation(self) -> None:
        refs = (self._ref("campaign/20261001"), self._ref("campaign/20261002"))
        provider = self._provider(
            refs,
            more_available=True,
            continuation="opaque-next-page",
            files={
                (ref.branch, "CAMPAIGN_CARD.yaml"): self._card(f"id-{index}")
                for index, ref in enumerate(refs)
            },
        )

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(
            provider.list_calls, [(None, bootstrap.MAX_CAMPAIGN_REFS_PER_PAGE)]
        )
        self.assertEqual(
            tuple(item.branch for item in page.candidates),
            tuple(ref.branch for ref in refs),
        )
        self.assertEqual(page.continuation, "opaque-next-page")
        self.assertIsNone(page.inability)
        self.assertEqual(
            provider.file_reads,
            [(ref.branch, "CAMPAIGN_CARD.yaml") for ref in refs],
        )
        self.assertFalse(hasattr(page, "selection"))

    def test_continuation_is_explicitly_requested_and_only_that_page_is_hydrated(
        self,
    ) -> None:
        ref = self._ref("campaign/20261003")
        provider = self._provider(
            (ref,),
            more_available=True,
            continuation="page-two",
            files={(ref.branch, "CAMPAIGN_CARD.yaml"): self._card("id-one")},
        )

        page = bootstrap.discover_campaign_page(provider, continuation="page-one")

        self.assertEqual(
            provider.list_calls, [("page-one", bootstrap.MAX_CAMPAIGN_REFS_PER_PAGE)]
        )
        self.assertEqual(len(page.candidates), 1)
        self.assertEqual(page.continuation, "page-two")
        self.assertEqual(len(provider.file_reads), 1)

    def test_exact_campaign_selection_routes_without_listing_campaign_refs(
        self,
    ) -> None:
        ref = self._ref("campaign/20261004")
        selection = CampaignSelection.existing("campaign.exact")
        provider = self._provider(
            (),
            exact={selection.campaign_id: ref},
            files={(ref.branch, "CAMPAIGN_CARD.yaml"): self._card("campaign.exact")},
        )

        page = bootstrap.discover_campaign_page(provider, selection=selection)

        self.assertEqual(provider.list_calls, [])
        self.assertEqual(provider.exact_lookups, ["campaign.exact"])
        self.assertEqual(tuple(item.branch for item in page.candidates), (ref.branch,))
        self.assertIsNone(page.inability)
        self.assertIs(require_campaign_selection(selection), selection)

    def test_provider_without_exact_resolver_returns_inability_without_list_fallback(
        self,
    ) -> None:
        class ProviderWithoutExactResolver:
            def __init__(self) -> None:
                self.list_calls = 0

            def list_campaign_refs(
                self, *, continuation: str | None, limit: int
            ) -> bootstrap.CampaignRefPage:
                self.list_calls += 1
                return bootstrap.CampaignRefPage(references=(), more_available=False)

            def read_campaign_file(
                self,
                *,
                ref: bootstrap.CampaignRef,
                path: str,
            ) -> object | None:
                return None

        provider = ProviderWithoutExactResolver()

        page = bootstrap.discover_campaign_page(
            provider,
            selection=CampaignSelection.existing("campaign.unresolved"),
        )

        self.assertEqual(page.inability.reason, "provider_limited")
        self.assertEqual(provider.list_calls, 0)

    def test_provider_limit_without_continuation_is_returned_as_typed_inability(
        self,
    ) -> None:
        ref = self._ref("campaign/20261005")
        provider = self._provider(
            (ref,),
            more_available=True,
            files={(ref.branch, "CAMPAIGN_CARD.yaml"): self._card("id-one")},
        )

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(len(page.candidates), 1)
        self.assertIsNone(page.continuation)
        self.assertEqual(page.inability.reason, "continuation_unavailable")
        self.assertEqual(len(provider.list_calls), 1)

    def test_provider_can_report_bounded_discovery_limitation_without_fallback_scan(
        self,
    ) -> None:
        limitation = bootstrap.CampaignDiscoveryInability(reason="provider_limited")
        provider = self._provider((), limitation=limitation)

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(page.inability, limitation)
        self.assertEqual(
            provider.list_calls, [(None, bootstrap.MAX_CAMPAIGN_REFS_PER_PAGE)]
        )
        self.assertEqual(provider.file_reads, [])

    def test_provider_over_returning_beyond_page_bound_fails_without_hydration(
        self,
    ) -> None:
        refs = tuple(self._ref(f"campaign/202610{day:02d}") for day in range(1, 22))
        provider = self._provider(refs)

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(page.inability.reason, "page_limit_exceeded")
        self.assertEqual(page.candidates, ())
        self.assertEqual(
            provider.list_calls, [(None, bootstrap.MAX_CAMPAIGN_REFS_PER_PAGE)]
        )
        self.assertEqual(provider.file_reads, [])

    def test_duplicate_refs_fail_closed_before_card_reads(self) -> None:
        ref = self._ref("campaign/20261006")
        provider = self._provider((ref, ref))

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(page.inability.reason, "duplicate_campaign_ref")
        self.assertEqual(page.candidates, ())
        self.assertEqual(provider.file_reads, [])

    def test_distinct_refs_with_duplicate_campaign_ids_are_ambiguous(self) -> None:
        refs = (self._ref("campaign/20261007"), self._ref("campaign/20261008"))
        provider = self._provider(
            refs,
            files={
                (ref.branch, "CAMPAIGN_CARD.yaml"): self._card("same-id")
                for ref in refs
            },
        )

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(page.inability.reason, "ambiguous_campaign_id")
        self.assertEqual(page.candidates, ())

    def test_hydration_is_card_first_and_manifest_is_only_missing_or_invalid_fallback(
        self,
    ) -> None:
        valid = self._ref("campaign/20261009")
        missing = self._ref("campaign/20261010")
        invalid = self._ref("campaign/20261011")
        provider = self._provider(
            (valid, missing, invalid),
            files={
                (valid.branch, "CAMPAIGN_CARD.yaml"): self._card("card-id"),
                (missing.branch, "CAMPAIGN_CARD.yaml"): None,
                (missing.branch, "MANIFEST.yaml"): self._manifest(
                    missing.branch, "missing-card-id"
                ),
                (invalid.branch, "CAMPAIGN_CARD.yaml"): {
                    "schema_version": 1,
                    "campaign_id": "",
                },
                (invalid.branch, "MANIFEST.yaml"): self._manifest(
                    invalid.branch, "invalid-card-id"
                ),
            },
        )

        page = bootstrap.discover_campaign_page(provider)

        self.assertIsNone(page.inability)
        self.assertEqual(
            provider.file_reads,
            [
                (valid.branch, "CAMPAIGN_CARD.yaml"),
                (missing.branch, "CAMPAIGN_CARD.yaml"),
                (missing.branch, "MANIFEST.yaml"),
                (invalid.branch, "CAMPAIGN_CARD.yaml"),
                (invalid.branch, "MANIFEST.yaml"),
            ],
        )
        self.assertEqual(
            tuple(candidate.projection.source for candidate in page.candidates),
            ("card", "manifest", "manifest"),
        )
        self.assertEqual(page.candidates[1].projection.campaign_id, "missing-card-id")
        self.assertIsNone(page.candidates[1].projection.engine_version)
        self.assertIsNone(page.candidates[1].projection.creator_github_login)
        self.assertIsNone(page.candidates[1].projection.current_location)

    def test_single_candidate_does_not_create_implicit_selection(self) -> None:
        ref = self._ref("campaign/20261012")
        provider = self._provider(
            (ref,),
            files={(ref.branch, "CAMPAIGN_CARD.yaml"): self._card("only-candidate")},
        )

        page = bootstrap.discover_campaign_page(provider)

        self.assertEqual(len(page.candidates), 1)
        self.assertFalse(hasattr(page, "selection"))
        candidate = page.candidates[0]
        for authority_field in (
            "selection",
            "access",
            "creator_authority",
            "gameplay",
            "currentness",
        ):
            self.assertFalse(hasattr(candidate, authority_field))
        with self.assertRaisesRegex(BootstrapContractError, "selection"):
            require_campaign_selection(None)


class CreatorAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_stable_account_id_and_current_login_are_separate_inputs(self) -> None:
        creator = _creator()

        self.assertEqual(creator.stable_github_user_id, "U_kgDOBootstrap")
        self.assertEqual(creator.login, "lina")
        with self.assertRaises(TypeError):
            CreatorIdentity(  # type: ignore[call-arg]
                stable_github_user_id="U_kgDOBootstrap",
                login="lina",
                email="lina@example.test",
            )

    def test_login_rename_cannot_transfer_creator_authority_even_with_same_stable_id(
        self,
    ) -> None:
        authority = authorize_creator(
            creator_login="lina",
            current_principal=CreatorIdentity(
                stable_github_user_id="U_kgDOBootstrap", login="lina-renamed"
            ),
        )

        self.assertEqual(authority, "read_only")

    def test_result_contract_carries_selection_and_creator_identity_without_email_authority(
        self,
    ) -> None:
        result = create_bootstrap_result(
            selection=CampaignSelection.new(),
            storage_repository="github.com/example/campaign-storage",
            pinned_storage_head="a" * 40,
            creator=_creator(),
            mode="singleplayer",
            campaign_branch="campaign/20260916",
            created_at="2026-09-16T12:00:00Z",
            engine_version="1.0-alpha",
            package_id="dev-v1.0-alpha",
            source_commit_sha=None,
            package_sha256="c" * 64,
            ruleset_set_sha256="d" * 64,
            ruleset_set_digest_generation=1,
        )
        result_value = result.as_dict()

        Draft202012Validator(
            self.schemas["bootstrap-result.schema.json"], registry=self.registry
        ).validate(result_value)
        self.assertNotIn("email", json.dumps(result_value))
        self.assertEqual(result_value.get("ruleset_set_digest_generation"), 1)


class SaveExitMenuTests(unittest.TestCase):
    @staticmethod
    def _durability_result(
        status: str, *, scope: str = "SAVE_ALL_DIRTY"
    ) -> DurabilityPromiseResult:
        evaluation = evaluate_durability(
            campaign_id="campaign.frostfall",
            scope=scope,
            dirty_roots=("CAMPAIGN_TREE",),
            currentness_evidence={"campaign_revision": "a" * 40},
        )
        promise = freeze_save_promise(evaluation, owner_generations={"campaign": 1})
        return complete_save_promise(
            promise,
            (NativeDurabilityResult("campaign", status),),
            currentness_evidence={"campaign_revision": "b" * 40},
        )

    def test_only_confirmed_required_save_clears_selection_and_returns_to_menu(
        self,
    ) -> None:
        compose_exit = getattr(bootstrap, "compose_save_exit", None)
        self.assertTrue(callable(compose_exit), "T06 save/exit composition is required")
        if not callable(compose_exit):
            return

        current = CampaignSelection.existing("campaign.frostfall")
        session_context = object()
        result = compose_exit(
            current,
            self._durability_result("CONFIRMED_ACCEPTED"),
            session_context=session_context,
        )

        self.assertTrue(result.saved)
        self.assertTrue(result.return_to_selection)
        self.assertIsNone(result.selection)
        self.assertIsNone(result.session_context)

    def test_rejected_conflict_and_indeterminate_save_retain_selected_context(
        self,
    ) -> None:
        compose_exit = getattr(bootstrap, "compose_save_exit", None)
        self.assertTrue(callable(compose_exit), "T06 save/exit composition is required")
        if not callable(compose_exit):
            return

        current = CampaignSelection.existing("campaign.frostfall")
        for native_status in (
            "CONFIRMED_REJECTED",
            "CONFLICT",
            "INDETERMINATE",
        ):
            with self.subTest(native_status=native_status):
                outcome = self._durability_result(native_status)
                session_context = object()
                result = compose_exit(current, outcome, session_context=session_context)

                self.assertFalse(result.saved)
                self.assertFalse(result.return_to_selection)
                self.assertIs(result.selection, current)
                self.assertIs(result.session_context, session_context)

    def test_save_scope_must_cover_save_all_dirty_before_exit(self) -> None:
        compose_exit = getattr(bootstrap, "compose_save_exit", None)
        self.assertTrue(callable(compose_exit), "T06 save/exit composition is required")
        if not callable(compose_exit):
            return

        with self.assertRaises(bootstrap.BootstrapContractError):
            compose_exit(
                CampaignSelection.existing("campaign.frostfall"),
                self._durability_result(
                    "CONFIRMED_ACCEPTED", scope="CAMPAIGN_TREE_ONLY"
                ),
                session_context=object(),
            )

    def test_untyped_or_inconsistent_save_result_fails_closed(self) -> None:
        compose_exit = getattr(bootstrap, "compose_save_exit", None)
        self.assertTrue(callable(compose_exit), "T06 save/exit composition is required")
        if not callable(compose_exit):
            return

        current = CampaignSelection.existing("campaign.frostfall")
        with self.assertRaises(bootstrap.BootstrapContractError):
            compose_exit(current, object(), session_context=object())


class ShippedBootstrapProjectionTests(unittest.TestCase):
    def test_size_governed_publication_measures_exact_path_operations_first(
        self,
    ) -> None:
        publish = getattr(bootstrap, "publish_measured_owner_delta", None)
        self.assertTrue(callable(publish), "T06 exact-measurement gate is required")
        if not callable(publish):
            return

        class Publication:
            def __init__(self) -> None:
                self.calls: list[str] = []
                self.measured_operations: object | None = None
                self.published_operations: object | None = None

            def measure_path_operations(self, operations: object) -> dict[str, int]:
                self.calls.append("measure")
                self.measured_operations = operations
                return {"STATE/CURRENT.yaml": 12}

            def publish_owner_delta(self, **_kwargs: object) -> PublicationOutcome:
                self.calls.append("publish")
                self.published_operations = _kwargs["path_operations"]
                return PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    "a" * 40,
                    "a" * 40,
                    "CONFIRMED_ACCEPTED",
                    True,
                )

        publication = Publication()
        host = type("BoundHost", (), {"publication": publication})()
        operations = {"STATE/CURRENT.yaml": {"state": "current"}}

        measured, result = publish(
            host,
            routed_operation=route_serialized_operation(
                "world.actor",
                "actor-1",
                {"kind": "world.actor", "id": "actor-1", "state": "current"},
            ),
            path_operations=operations,
            owner_generations={"campaign": 1},
            publication_reason="test.size_governed_write",
        )

        self.assertEqual(publication.calls, ["measure", "publish"])
        self.assertIs(publication.measured_operations, operations)
        self.assertIs(publication.published_operations, operations)
        self.assertEqual(dict(measured), {"STATE/CURRENT.yaml": 12})
        self.assertIs(result.status, PublicationStatus.ACCEPTED)

    def test_missing_or_inexact_measurement_fails_before_publication(self) -> None:
        publish = getattr(bootstrap, "publish_measured_owner_delta", None)
        self.assertTrue(callable(publish), "T06 exact-measurement gate is required")
        if not callable(publish):
            return

        class Publication:
            def __init__(self, measurement: object) -> None:
                self.measurement = measurement
                self.publish_calls = 0

            def publish_owner_delta(self, **_kwargs: object) -> PublicationOutcome:
                self.publish_calls += 1
                return PublicationOutcome(
                    PublicationStatus.ACCEPTED,
                    "a" * 40,
                    "a" * 40,
                    "CONFIRMED_ACCEPTED",
                    True,
                )

        for measurement in (None, {}, {"other.yaml": 12}, {"STATE/CURRENT.yaml": True}):
            with self.subTest(measurement=measurement):
                publication = Publication(measurement)
                if measurement is not None:
                    publication.measure_path_operations = (
                        lambda _ops, exact_result=measurement: exact_result
                    )
                host = type("BoundHost", (), {"publication": publication})()
                with self.assertRaises(bootstrap.BootstrapContractError):
                    publish(
                        host,
                        routed_operation=route_serialized_operation(
                            "world.actor",
                            "actor-1",
                            {
                                "kind": "world.actor",
                                "id": "actor-1",
                                "state": "current",
                            },
                        ),
                        path_operations={"STATE/CURRENT.yaml": {"state": "current"}},
                        owner_generations={"campaign": 1},
                        publication_reason="test.size_governed_write",
                    )
                self.assertEqual(publication.publish_calls, 0)


if __name__ == "__main__":
    unittest.main()
