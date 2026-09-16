from __future__ import annotations

import copy
import json
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
from GAME.TOOLS.ruleset_package import build_resolved_lock


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
PACKAGE_ID = "hdm.rules.dnd2024-srd52-core"
PACKAGE = ROOT / "GAME" / "RULES" / "packages" / PACKAGE_ID


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
    return {
        "basis": {
            "catalog_generation": 2,
            "engine_contract_inventory_sha256": "a" * 64,
            "ruleset_lock": lock,
            "campaign_definition_frontier": {
                "frontier_id": "campaign.definitions",
                "state_revision": frontier_revision,
                "definition_ids": ["activity.check.generic"],
            },
        },
        "definition_dependencies": [
            {
                "definition_id": "activity.check.generic",
                "kind": "definition.activity",
                "package_id": package["package_id"],
                "package_content_sha256": package["content_sha256"],
            }
        ],
    }


def _package_snapshots():
    _lock, snapshots = build_resolved_lock(
        [PACKAGE],
        root_package_ids=[PACKAGE_ID],
        engine_version="1.0-alpha",
        catalog_generation=2,
    )
    return snapshots


def _bind_context(request: dict[str, object] | None = None):
    return bind_catalog_context(
        _request() if request is None else request,
        package_snapshots=_package_snapshots(),
    )


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

    def test_definition_outside_the_declared_frontier_cannot_be_bound(self) -> None:
        request = _request()
        request["basis"]["campaign_definition_frontier"]["definition_ids"] = []

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
            _bind_context({"default_catalog": "dnd"})


class CatalogBackedAcceptanceIntegrationTests(unittest.TestCase):
    def test_binding_result_requires_revalidation_before_a_consumer_can_accept_it(self) -> None:
        context = _bind_context()
        result = bind_executable_catalog(
            context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"},
        )

        self.assertEqual(result["status"], "bound")
        validate_executable_binding(context, result["binding"])


if __name__ == "__main__":
    unittest.main()
