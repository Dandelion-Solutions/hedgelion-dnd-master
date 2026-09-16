from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.bootstrap import (
    BootstrapContractError,
    CampaignSelection,
    CreatorIdentity,
    authorize_creator,
    build_scaffold_input,
    create_bootstrap_result,
    require_campaign_selection,
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


class CampaignSelectionBarrierTests(unittest.TestCase):
    def test_missing_selection_fails_closed_without_inferring_a_sole_candidate(self) -> None:
        with self.assertRaisesRegex(BootstrapContractError, "selection"):
            require_campaign_selection(None)

    def test_explicit_existing_or_new_selection_is_typed_and_unambiguous(self) -> None:
        self.assertEqual(CampaignSelection.existing("campaign.frostfall").kind, "existing")
        self.assertEqual(CampaignSelection.new().kind, "new")
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="existing", campaign_id=None)
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="new", campaign_id="campaign.frostfall")
        with self.assertRaises(BootstrapContractError):
            CampaignSelection(kind="implicit", campaign_id=None)  # type: ignore[arg-type]


class CreationIdentityTests(unittest.TestCase):
    def test_creation_allocates_one_canonical_campaign_identity_before_scaffold_input(self) -> None:
        scaffold_input = _scaffold_input()

        self.assertRegex(str(scaffold_input["campaign_id"]), r"^campaign\.[0-9a-f]{32}$")
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

    def test_scaffold_input_is_bounded_and_contains_every_generator_identity_input(self) -> None:
        scaffold_input = _scaffold_input()

        Draft202012Validator(
            self.schemas["bootstrap-request.schema.json"], registry=self.registry
        ).validate(scaffold_input)
        self.assertEqual(
            set(scaffold_input),
            {
                "campaign_id", "campaign_branch", "created_at", "creator_github_login", "mode",
                "engine_version", "package_id", "source_commit_sha", "package_sha256", "ruleset_set_sha256",
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

    def test_scaffold_input_rejects_an_incompatible_ruleset_digest_generation(self) -> None:
        invalid = _scaffold_input() | {"ruleset_set_digest_generation": 2}
        validator = Draft202012Validator(
            self.schemas["bootstrap-request.schema.json"], registry=self.registry
        )

        with self.assertRaises(ValidationError):
            validator.validate(invalid)


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
                stable_github_user_id="U_kgDOBootstrap", login="lina", email="lina@example.test"
            )

    def test_login_rename_cannot_transfer_creator_authority_even_with_same_stable_id(self) -> None:
        authority = authorize_creator(
            creator_login="lina",
            current_principal=CreatorIdentity(
                stable_github_user_id="U_kgDOBootstrap", login="lina-renamed"
            ),
        )

        self.assertEqual(authority, "read_only")

    def test_result_contract_carries_selection_and_creator_identity_without_email_authority(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
