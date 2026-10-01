from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS import bootstrap
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


if __name__ == "__main__":
    unittest.main()
