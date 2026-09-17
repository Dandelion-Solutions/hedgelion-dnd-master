from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.catalog_runtime import (
    CatalogBindingError,
    bind_catalog_context,
    bind_executable_catalog,
    bind_interpreter_candidate,
    validate_executable_binding,
)
from GAME.TOOLS.ruleset_package import (
    INVENTORY_DOMAIN,
    REQUIRED_ENGINE_CONTRACT_FAMILIES,
    RULESET_SET_DIGEST_GENERATION,
    SET_DOMAIN,
    build_resolved_lock,
    build_snapshot,
    canonical_json,
    sha256,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
PACKAGE_ID = "hdm.rules.dnd2024-srd52-core"
PACKAGE = ROOT / "GAME" / "RULES" / "packages" / PACKAGE_ID
NATURAL_OWNER_EVIDENCE_DOMAIN = b"HDM_CATALOG_NATURAL_OWNER_EVIDENCE/1\n"


def _schema_registry() -> tuple[Registry, dict[str, object]]:
    registry = Registry()
    schemas: dict[str, object] = {}
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry, schemas


def _request(*, frontier_revision: int = 4) -> dict[str, object]:
    lock, _ = build_resolved_lock(
        [PACKAGE],
        root_package_ids=[PACKAGE_ID],
        engine_version="1.0-alpha",
        catalog_generation=2,
    )
    package = lock["packages"][0]
    inventory = _engine_contract_inventory(lock)
    return {
        "basis": {
            "catalog_generation": 2,
            "engine_version": "1.0-alpha",
            "engine_contract_inventory_sha256": inventory["inventory_sha256"],
            "engine_contract_inventory": inventory,
            "ruleset_lock": lock,
            "campaign_definition_frontier": {
                "frontier_id": "campaign.definitions",
                "state_revision": frontier_revision,
                "definition_ids": ["activity.check.generic"],
            },
            "natural_owner_evidence": [],
        },
        "definition_dependencies": [
            {
                "definition_id": "activity.check.generic",
                "kind": "definition.activity",
                "source_type": "ruleset_package",
                "package_id": package["package_id"],
                "package_content_sha256": package["content_sha256"],
            }
        ],
    }


def _engine_contract_inventory(lock: dict[str, object]) -> dict[str, object]:
    core = {
        "inventory_schema_version": 2,
        "engine_version": "1.0-alpha",
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "items": [
            {
                "family": family,
                "contract_id": f"engine_contract.{family}.v1",
                "semantic_sha256": "a" * 64,
            }
            for family in sorted(REQUIRED_ENGINE_CONTRACT_FAMILIES)
        ],
    }
    return {**core, "inventory_sha256": sha256(INVENTORY_DOMAIN + canonical_json(core))}


def _natural_owner_evidence(*, owner_domain: str = "campaign") -> dict[str, object]:
    scope = (
        f"{owner_domain}.definition_frontier"
        if owner_domain == "campaign"
        else "session.overlay_frontier"
    )
    definition_id = f"{owner_domain}.local_attack"
    return {
        "definition_id": definition_id,
        "kind": "definition.activity",
        "owner_domain": owner_domain,
        "scope": scope,
        "route": (
            f"campaign/definitions/{definition_id}.json"
            if owner_domain == "campaign"
            else f"session/overlays/{definition_id}.json"
        ),
        "pinned_revision": 4,
        "content_sha256": sha256(_natural_owner_content(owner_domain=owner_domain)),
    }


def _natural_owner_content(*, owner_domain: str) -> bytes:
    return canonical_json(
        {
            "definition_id": f"{owner_domain}.local_attack",
            "kind": "definition.activity",
            "owner_domain": owner_domain,
            "pinned_revision": 4,
            "effect": "local attack",
        }
    )


def _natural_owner_dependency(evidence: dict[str, object]) -> dict[str, object]:
    return {
        "source_type": "natural_owner",
        "definition_id": evidence["definition_id"],
        "kind": evidence["kind"],
        "owner_domain": evidence["owner_domain"],
        "scope": evidence["scope"],
        "route": evidence["route"],
        "pinned_revision": evidence["pinned_revision"],
        "evidence_sha256": sha256(
            NATURAL_OWNER_EVIDENCE_DOMAIN + canonical_json(evidence)
        ),
    }


def _natural_owner_sources(request: dict[str, object]) -> dict[str, object]:
    basis = request["basis"]
    evidence = basis["natural_owner_evidence"]
    sources: dict[str, object] = {}
    for owner_domain in ("campaign", "session"):
        rows = [row for row in evidence if row["owner_domain"] == owner_domain]
        if not rows:
            continue
        frontier_key = (
            "campaign_definition_frontier"
            if owner_domain == "campaign"
            else "session_overlay_frontier"
        )
        sources[owner_domain] = {
            "selected_frontier": copy.deepcopy(basis[frontier_key]),
            "members": copy.deepcopy(rows),
            "immutable_member_bytes": {
                row["route"]: _natural_owner_content(owner_domain=owner_domain)
                for row in rows
            },
        }
    return sources


def _package_snapshots():
    _lock, snapshots = build_resolved_lock(
        [PACKAGE],
        root_package_ids=[PACKAGE_ID],
        engine_version="1.0-alpha",
        catalog_generation=2,
    )
    return snapshots


def _bind_context(
    request: dict[str, object] | None = None, *, package_snapshots=None
):
    request = _request() if request is None else request
    return bind_catalog_context(
        request,
        package_snapshots=_package_snapshots() if package_snapshots is None else package_snapshots,
        engine_contract_inventory_source=copy.deepcopy(
            request["basis"]["engine_contract_inventory"]
        ),
        natural_owner_sources=_natural_owner_sources(request),
    )


def _lock_from_snapshots(snapshots):
    packages = []
    for package_id, snapshot in sorted(snapshots.items()):
        manifest = snapshot.manifest
        packages.append(
            {
                "package_id": package_id,
                "package_revision": manifest["package_revision"],
                "compatibility_family": manifest["compatibility_family"],
                "compatibility_generation": manifest["compatibility_generation"],
                "content_sha256": snapshot.content_sha256,
                "catalog_generation": manifest["catalog_generation"],
                "owned_namespaces": sorted(manifest["owned_namespaces"]),
                "dependencies": sorted(
                    manifest["dependencies"], key=lambda row: row["package_id"]
                ),
                "members": list(snapshot.members),
            }
        )
    core = {
        "lock_schema_version": 2,
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "root_package_ids": sorted(snapshots),
        "packages": packages,
    }
    return {**core, "ruleset_set_sha256": sha256(SET_DOMAIN + canonical_json(core))}


def _rehash_lock(lock):
    core = {
        key: lock[key]
        for key in (
            "lock_schema_version",
            "ruleset_set_digest_generation",
            "root_package_ids",
            "packages",
        )
    }
    lock["ruleset_set_sha256"] = sha256(SET_DOMAIN + canonical_json(core))


class CatalogContextBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_bound_context_carries_exact_reconstructive_basis(self) -> None:
        context = _bind_context()
        payload = context.to_dict()

        self.assertEqual(payload["basis"]["catalog_generation"], 2)
        self.assertEqual(
            payload["basis"]["ruleset_lock"]["ruleset_set_digest_generation"], 1
        )
        self.assertEqual(payload["catalog_context_fingerprint_generation"], 1)
        Draft202012Validator(
            self.schemas["catalog-binding-result.schema.json"], registry=self.registry
        ).validate(payload)

    def test_bound_context_does_not_expose_mutable_reconstruction_inputs(self) -> None:
        context = _bind_context()

        with self.assertRaises(TypeError):
            context.basis["catalog_generation"] = 3


class CatalogCandidateValidationTests(unittest.TestCase):
    def test_candidate_is_bound_only_when_its_exact_id_and_kind_are_pinned(self) -> None:
        context = _bind_context()

        binding = bind_interpreter_candidate(
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )

        self.assertEqual(binding["definition_id"], "activity.check.generic")
        self.assertEqual(binding["catalog_context_fingerprint"], context.fingerprint)

    def test_name_only_candidate_cannot_become_an_executable_binding(self) -> None:
        context = _bind_context()

        with self.assertRaises(CatalogBindingError):
            bind_interpreter_candidate(context, {"name": "Basic attack"})


class CatalogDefinitionAdmissionTests(unittest.TestCase):
    def _request_with_natural_evidence(
        self, *, owner_domain: str = "campaign"
    ) -> dict[str, object]:
        request = _request()
        evidence = _natural_owner_evidence(owner_domain=owner_domain)
        request["basis"]["natural_owner_evidence"] = [evidence]
        request["definition_dependencies"].append(_natural_owner_dependency(evidence))
        if owner_domain == "campaign":
            request["basis"]["campaign_definition_frontier"]["definition_ids"].append(
                evidence["definition_id"]
            )
        else:
            request["basis"]["session_overlay_frontier"] = {
                "frontier_id": "session.overlay",
                "state_revision": 4,
                "definition_ids": [evidence["definition_id"]],
            }
        return request

    def test_pinned_campaign_owner_evidence_is_admitted_with_the_exact_package_context(self) -> None:
        request = self._request_with_natural_evidence()

        context = _bind_context(request)

        self.assertEqual(
            {row["definition_id"] for row in context.definition_dependencies},
            {"activity.check.generic", "campaign.local_attack"},
        )
        registry, schemas = _schema_registry()
        Draft202012Validator(
            schemas["catalog-binding-result.schema.json"], registry=registry
        ).validate(context.to_dict())

    def test_pinned_session_owner_evidence_is_admitted(self) -> None:
        request = self._request_with_natural_evidence(owner_domain="session")
        context = _bind_context(request)

        self.assertEqual(context.definition_dependencies[-1]["owner_domain"], "session")

    def test_natural_owner_evidence_cannot_be_missing_changed_or_ambient(self) -> None:
        missing = self._request_with_natural_evidence()
        missing["basis"]["natural_owner_evidence"] = []
        changed = self._request_with_natural_evidence()
        changed["basis"]["natural_owner_evidence"][0]["content_sha256"] = "c" * 64
        ambient = self._request_with_natural_evidence()
        ambient["basis"]["natural_owner_evidence"][0]["route"] = "campaign/latest/local_attack.json"

        for request in (missing, changed, ambient):
            with self.subTest(request=request):
                with self.assertRaises(CatalogBindingError):
                    _bind_context(request)

    def test_natural_owner_dependency_cannot_change_its_pinned_revision(self) -> None:
        request = self._request_with_natural_evidence()
        request["definition_dependencies"][1]["pinned_revision"] = 5

        with self.assertRaises(CatalogBindingError):
            _bind_context(request)

    def test_coordinated_caller_claims_cannot_forge_immutable_engine_inventory(self) -> None:
        request = _request()
        immutable_inventory = copy.deepcopy(request["basis"]["engine_contract_inventory"])
        forged_inventory = copy.deepcopy(immutable_inventory)
        forged_inventory["items"][0]["semantic_sha256"] = "b" * 64
        forged_core = {
            key: forged_inventory[key]
            for key in (
                "inventory_schema_version",
                "engine_version",
                "ruleset_set_digest_generation",
                "ruleset_set_sha256",
                "items",
            )
        }
        forged_inventory["inventory_sha256"] = sha256(
            INVENTORY_DOMAIN + canonical_json(forged_core)
        )
        request["basis"]["engine_contract_inventory"] = forged_inventory
        request["basis"]["engine_contract_inventory_sha256"] = forged_inventory[
            "inventory_sha256"
        ]

        with self.assertRaises(CatalogBindingError):
            bind_catalog_context(
                request,
                package_snapshots=_package_snapshots(),
                engine_contract_inventory_source=immutable_inventory,
                natural_owner_sources={},
            )

    def test_coordinated_caller_claims_cannot_forge_natural_owner_source_evidence(self) -> None:
        request = self._request_with_natural_evidence()
        natural_owner_sources = _natural_owner_sources(request)
        forged = request["basis"]["natural_owner_evidence"][0]
        forged["content_sha256"] = "c" * 64
        request["definition_dependencies"][1] = _natural_owner_dependency(forged)

        with self.assertRaises(CatalogBindingError):
            bind_catalog_context(
                request,
                package_snapshots=_package_snapshots(),
                engine_contract_inventory_source=request["basis"]["engine_contract_inventory"],
                natural_owner_sources=natural_owner_sources,
            )

    def test_synchronized_natural_owner_claims_cannot_forge_owner_content_digest(self) -> None:
        request = self._request_with_natural_evidence()
        natural_owner_sources = _natural_owner_sources(request)
        forged = request["basis"]["natural_owner_evidence"][0]
        forged["content_sha256"] = "c" * 64
        natural_owner_sources["campaign"]["members"][0]["content_sha256"] = "c" * 64
        request["definition_dependencies"][1] = _natural_owner_dependency(forged)

        with self.assertRaises(CatalogBindingError):
            bind_catalog_context(
                request,
                package_snapshots=_package_snapshots(),
                engine_contract_inventory_source=request["basis"]["engine_contract_inventory"],
                natural_owner_sources=natural_owner_sources,
            )

    def test_natural_owner_source_requires_selected_frontier_and_member(self) -> None:
        request = self._request_with_natural_evidence()
        for missing_key, source in (
            ("selected_frontier", {"members": request["basis"]["natural_owner_evidence"]}),
            (
                "members",
                {
                    "selected_frontier": request["basis"]["campaign_definition_frontier"],
                    "members": [],
                },
            ),
        ):
            with self.subTest(missing_key=missing_key):
                with self.assertRaises(CatalogBindingError):
                    bind_catalog_context(
                        request,
                        package_snapshots=_package_snapshots(),
                        engine_contract_inventory_source=request["basis"][
                            "engine_contract_inventory"
                        ],
                        natural_owner_sources={"campaign": source},
                    )

    def test_noncanonical_natural_owner_source_route_is_rejected(self) -> None:
        request = self._request_with_natural_evidence()
        source = _natural_owner_sources(request)
        source["campaign"]["members"][0]["route"] = "campaign/archive/local_attack.json"
        request["basis"]["natural_owner_evidence"][0]["route"] = (
            "campaign/archive/local_attack.json"
        )
        request["definition_dependencies"][1] = _natural_owner_dependency(
            request["basis"]["natural_owner_evidence"][0]
        )

        with self.assertRaises(CatalogBindingError):
            bind_catalog_context(
                request,
                package_snapshots=_package_snapshots(),
                engine_contract_inventory_source=request["basis"]["engine_contract_inventory"],
                natural_owner_sources=source,
            )

    def test_malformed_source_specific_dependency_raises_catalog_binding_error(self) -> None:
        malformed_dependencies = (
            {"source_type": "ruleset_package", "definition_id": "activity.check.generic"},
            {
                "source_type": "natural_owner",
                "definition_id": "campaign.local_attack",
                "kind": "definition.activity",
            },
        )
        for dependency in malformed_dependencies:
            request = _request()
            request["definition_dependencies"] = [dependency]
            with self.subTest(dependency=dependency):
                with self.assertRaises(CatalogBindingError):
                    _bind_context(request)

    def test_engine_contract_inventory_requires_its_admitted_evidence(self) -> None:
        request = _request()
        request["basis"]["engine_contract_inventory"]["items"][0]["semantic_sha256"] = "b" * 64

        with self.assertRaises(CatalogBindingError):
            _bind_context(request)

    def test_natural_owner_executable_binding_retains_its_pinned_source(self) -> None:
        context = _bind_context(self._request_with_natural_evidence())

        binding = bind_interpreter_candidate(
            context,
            {"definition_id": "campaign.local_attack", "kind": "definition.activity"},
        )

        self.assertEqual(binding["source_type"], "natural_owner")
        validate_executable_binding(context, binding)
        forged = dict(binding)
        forged["pinned_revision"] = 5
        with self.assertRaises(CatalogBindingError):
            validate_executable_binding(context, forged)

    def test_absent_definition_cannot_be_declared_into_a_context(self) -> None:
        request = _request()
        request["basis"]["campaign_definition_frontier"]["definition_ids"] = [
            "activity.unknown"
        ]
        request["definition_dependencies"][0]["definition_id"] = "activity.unknown"

        with self.assertRaises(CatalogBindingError):
            _bind_context(request)

    def test_unowned_namespace_cannot_be_declared_into_a_context(self) -> None:
        request = _request()
        request["basis"]["campaign_definition_frontier"]["definition_ids"] = [
            "unowned.attack"
        ]
        request["definition_dependencies"][0]["definition_id"] = "unowned.attack"

        with self.assertRaises(CatalogBindingError):
            _bind_context(request)

    def test_package_definition_admission_does_not_use_campaign_session_frontiers(self) -> None:
        request = _request()
        request["basis"]["campaign_definition_frontier"]["definition_ids"] = []

        self.assertEqual(
            _bind_context(request).definition_dependencies[0]["definition_id"],
            "activity.check.generic",
        )

    def test_forged_mutable_semantic_entry_cannot_admit_an_absent_definition(self) -> None:
        request = _request()
        request["basis"]["campaign_definition_frontier"]["definition_ids"] = [
            "activity.forged"
        ]
        request["definition_dependencies"][0]["definition_id"] = "activity.forged"
        snapshots = _package_snapshots()
        snapshots[PACKAGE_ID].semantic_entries[
            f"{PACKAGE_ID}|activity_definitions|id:activity.forged"
        ] = {"kind": "definition.activity", "semantic_sha256": "f" * 64}

        with self.assertRaises(CatalogBindingError):
            _bind_context(request, package_snapshots=snapshots)

    def test_changed_package_bytes_cannot_reuse_a_snapshot_self_reported_digest(self) -> None:
        request = _request()
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / PACKAGE_ID
            shutil.copytree(PACKAGE, package)
            _lock, snapshots = build_resolved_lock(
                [package],
                root_package_ids=[PACKAGE_ID],
                engine_version="1.0-alpha",
                catalog_generation=2,
            )
            source = package / "gameplay-spine-seed.json"
            source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")

            with self.assertRaises(CatalogBindingError):
                _bind_context(request, package_snapshots=snapshots)

    def test_cross_source_definition_collision_rejects_the_catalog_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            duplicate_dir = Path(directory) / "duplicate"
            shutil.copytree(PACKAGE, duplicate_dir)
            manifest_path = duplicate_dir / "ruleset-package-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            duplicate_id = "hdm.rules.duplicate"
            manifest["package_id"] = duplicate_id
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            duplicate = build_snapshot(
                duplicate_dir, engine_version="1.0-alpha", catalog_generation=2
            )
            snapshots = _package_snapshots()
            snapshots[duplicate_id] = duplicate
            request = _request()
            request["basis"]["ruleset_lock"] = _lock_from_snapshots(snapshots)

            with self.assertRaises(CatalogBindingError):
                _bind_context(request, package_snapshots=snapshots)

    def test_rehashed_lock_cannot_forge_a_package_identity_line(self) -> None:
        request = _request()
        request["basis"]["ruleset_lock"]["packages"][0]["package_revision"] = 99
        _rehash_lock(request["basis"]["ruleset_lock"])

        with self.assertRaises(CatalogBindingError):
            _bind_context(request)


class CatalogGapReportTests(unittest.TestCase):
    def test_unavailable_exact_candidate_returns_context_bound_gap_evidence(self) -> None:
        context = _bind_context()

        result = bind_executable_catalog(
            context,
            {"definition_id": "activity.unknown", "kind": "definition.activity"},
        )

        self.assertEqual(result["status"], "gap")
        self.assertEqual(result["gap_report"]["reason"], "definition_not_found")
        self.assertEqual(
            result["gap_report"]["catalog_context_fingerprint"], context.fingerprint
        )
        self.assertEqual(
            result["gap_report"]["context_basis"]["ruleset_lock"]["ruleset_set_sha256"],
            context.basis["ruleset_lock"]["ruleset_set_sha256"],
        )

    def test_wrong_kind_is_a_gap_not_a_name_based_substitution(self) -> None:
        context = _bind_context()

        result = bind_executable_catalog(
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.spell"},
        )

        self.assertEqual(result["status"], "gap")
        self.assertEqual(result["gap_report"]["reason"], "definition_kind_mismatch")


class CatalogBindingCurrentnessTests(unittest.TestCase):
    def test_binding_from_an_older_frontier_is_rejected_against_the_current_context(self) -> None:
        old_context = _bind_context(_request(frontier_revision=4))
        old_binding = bind_interpreter_candidate(
            old_context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )
        current_context = _bind_context(_request(frontier_revision=5))

        with self.assertRaisesRegex(CatalogBindingError, "stale catalog context"):
            validate_executable_binding(current_context, old_binding)


class CatalogBindingIntegrationTests(unittest.TestCase):
    def test_executable_binding_remains_pinned_to_the_context_that_selected_it(self) -> None:
        context = _bind_context()
        binding = bind_interpreter_candidate(
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )

        validate_executable_binding(context, binding)

        forged = copy.deepcopy(binding)
        forged["source_package_id"] = "hdm.rules.other"
        with self.assertRaises(CatalogBindingError):
            validate_executable_binding(context, forged)


class CatalogContextBasisContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_basis_schema_is_strict_and_rejects_a_mixed_catalog_generation(self) -> None:
        basis = _request()["basis"]
        validator = Draft202012Validator(
            self.schemas["catalog-context-basis.schema.json"], registry=self.registry
        )
        validator.validate(basis)

        mixed = copy.deepcopy(basis)
        mixed["ruleset_lock"]["packages"][0]["catalog_generation"] = 3
        with self.assertRaises(ValidationError):
            validator.validate(mixed)


class CatalogGapContextEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = _schema_registry()

    def test_gap_report_schema_requires_pinned_context_and_requested_identity(self) -> None:
        context = _bind_context()
        result = bind_executable_catalog(
            context,
            {"definition_id": "activity.unknown", "kind": "definition.activity"},
        )
        validator = Draft202012Validator(
            self.schemas["runtime-catalog-gap-report-state.schema.json"], registry=self.registry
        )
        validator.validate(result["gap_report"])

        missing_context = copy.deepcopy(result["gap_report"])
        missing_context.pop("catalog_context_fingerprint")
        with self.assertRaises(ValidationError):
            validator.validate(missing_context)


class CatalogBindingInstructionCutoverTests(unittest.TestCase):
    def test_default_or_ambient_catalog_selection_is_not_accepted(self) -> None:
        with self.assertRaises(CatalogBindingError):
            bind_catalog_context(
                {"default_catalog": "dnd"},
                package_snapshots=_package_snapshots(),
                engine_contract_inventory_source={},
                natural_owner_sources={},
            )


class CatalogBackedAcceptanceIntegrationTests(unittest.TestCase):
    def test_binding_result_requires_revalidation_before_a_consumer_can_accept_it(self) -> None:
        from GAME.TOOLS.runtime_execution import (
            CatalogGap,
            accept_command,
            validate_execution_proposal,
        )

        context = _bind_context()
        result = bind_executable_catalog(
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )

        self.assertEqual(result["status"], "bound")
        validate_executable_binding(context, result["binding"])
        accepted = accept_command(
            {
                "kind": "interpreter_result",
                "purpose": "interpret",
                "bundle_id": "bundle-1",
                "source_generation": "frontier-7",
                "intent": "make a check",
            },
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
            {
                "command_id": "turn-1-cmd-01",
                "interaction_id": "turn-1",
                "intent_plan_id": "turn-1-plan",
                "clause_id": "c1",
                "action_request": {
                    "activity_id": "activity.check.generic",
                    "actor_id": "actor-1",
                },
                "root_resolution_id": "resolution-1",
            },
        )
        self.assertNotIsInstance(accepted, CatalogGap)
        validate_execution_proposal(
            accepted,
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )


if __name__ == "__main__":
    unittest.main()
