"""Source-bound Activity compiler catalog conformance tests."""

from __future__ import annotations

import copy
import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Mapping
from pathlib import Path

import pytest
import yaml

from DEV.TOOLS import validate_ruleset_package_closure as package_closure

ROOT = Path(__file__).resolve().parents[2]
_INSTALLED_RUNTIME_ROOT: Path | None = None


def _stage_clean_source_tree(destination: Path) -> None:
    """Copy current source files while excluding ignored checkout artifacts."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    for raw_relative_path in result.stdout.split(b"\0"):
        if not raw_relative_path:
            continue
        relative_path = Path(os.fsdecode(raw_relative_path))
        source = ROOT / relative_path
        if not source.exists() and not source.is_symlink():
            continue
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        elif source.is_file():
            shutil.copy2(source, target)


def test_activity_compiler_contract_projection_reuses_source_family_identity(
    installed_runtime_root: Path,
) -> None:
    producer = getattr(package_closure, "derive_activity_compiler_contracts", None)
    assert callable(producer), (
        "canonical Activity compiler projection producer is missing"
    )

    package = (
        installed_runtime_root
        / "RULES"
        / "packages"
        / "hdm.rules.dnd2024-srd52-core"
    )
    ruleset_package = _installed_tool(installed_runtime_root, "ruleset_package")

    manifest = ruleset_package.load_json_bytes(
        (package / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [package],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    inventory = package_closure.derive_engine_contract_inventory(
        ROOT,
        engine_version=manifest["engine_requirement"]["engine_version"],
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )

    projection = producer(
        ROOT,
        engine_version=manifest["engine_requirement"]["engine_version"],
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )

    source_hashes = {
        row["family"]: row["semantic_sha256"] for row in inventory["items"]
    }
    projection_hashes = {
        row["family"]: row["source_semantic_sha256"]
        for row in projection["source_identity"]["families"]
    }
    assert projection["schema_version"] == 1
    assert projection_hashes == source_hashes
    assert projection["source_identity"]["inventory_schema_version"] == 2
    assert "DEV/" not in repr(projection)

    primitive_source = package_closure.load_activity_primitive_contracts(ROOT)
    projected_primitives = projection["families"]["primitive"][
        "activity_primitive_contracts"
    ]
    for projected, original in zip(projected_primitives["contracts"], primitive_source["contracts"], strict=True):
        assert {key: value for key, value in projected.items() if key != "compiler_declarations"} == {
            key: value for key, value in original.items() if key != "compiler_declarations"}
    assert (
        projected_primitives["primitive_validation_matrix"]
        == primitive_source["primitive_validation_matrix"]
    )
    assert projected_primitives["read_contracts"] == primitive_source["read_contracts"]


def test_installed_activity_compiler_projection_matches_canonical_sources(
    installed_runtime_root: Path,
) -> None:
    validator = getattr(
        package_closure, "validate_activity_compiler_contracts_projection", None
    )
    assert callable(validator), "installed compiler projection validator is missing"

    package = (
        installed_runtime_root
        / "RULES"
        / "packages"
        / "hdm.rules.dnd2024-srd52-core"
    )
    ruleset_package = _installed_tool(installed_runtime_root, "ruleset_package")

    manifest = ruleset_package.load_json_bytes(
        (package / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [package],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )

    validator(
        ROOT,
        engine_version=manifest["engine_requirement"]["engine_version"],
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )


def test_runtime_package_metadata_binds_exact_compiler_projection_bytes(
    installed_runtime_root: Path,
    runtime_package_metadata: dict[str, object],
) -> None:
    ruleset_package = _installed_tool(installed_runtime_root, "ruleset_package")

    projection_bytes = (
        installed_runtime_root / "TOOLS" / "activity_compiler_contracts.json"
    ).read_bytes()
    assert runtime_package_metadata["schema_version"] == 4
    assert runtime_package_metadata["activity_compiler_contracts_sha256"] == (
        ruleset_package.sha256(projection_bytes)
    )


@pytest.fixture(scope="module")
def installed_runtime_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    global _INSTALLED_RUNTIME_ROOT
    from DEV.TOOLS import release_builder

    clean_source_root = tmp_path_factory.mktemp("sp02-clean-source")
    _stage_clean_source_tree(clean_source_root)
    build_dir = tmp_path_factory.mktemp("sp02-runtime-build")
    archive = release_builder.build_runtime_zip(
        clean_source_root, build_dir, intended_tag="v1.0-alpha"
    )
    installed_root = tmp_path_factory.mktemp("sp02-full-installed-runtime")
    with zipfile.ZipFile(archive) as runtime_zip:
        runtime_zip.extractall(installed_root)
    release_builder.validate_extracted_package_root(installed_root)
    _INSTALLED_RUNTIME_ROOT = installed_root
    return installed_root


@pytest.fixture(scope="module")
def runtime_package_metadata(installed_runtime_root: Path) -> dict[str, object]:
    metadata = yaml.safe_load(
        (installed_runtime_root / "RUNTIME_PACKAGE.yaml").read_text(encoding="utf-8")
    )
    assert isinstance(metadata, dict)
    return metadata


def _installed_tool(installed_runtime_root: Path, module_name: str):
    root = installed_runtime_root.resolve()
    tools = root / "TOOLS"
    package_name = "_sp02_installed_tools"
    loaded_package = sys.modules.get(package_name)
    if loaded_package is None:
        # TOOLS is shipped as a namespace package. Give this complete installed
        # package its own import namespace without changing any runtime root or
        # source-issuer input; every loaded module still has its real file origin.
        spec = importlib.machinery.ModuleSpec(package_name, loader=None, is_package=True)
        spec.submodule_search_locations = [str(tools)]
        loaded_package = importlib.util.module_from_spec(spec)
        sys.modules[package_name] = loaded_package
    package_paths = tuple(
        Path(item).resolve() for item in getattr(loaded_package, "__path__", ())
    )
    if package_paths != (tools,):
        raise RuntimeError("TOOLS imports do not resolve to this installed runtime root")
    module = importlib.import_module(f"{package_name}.{module_name}")
    module_path = Path(module.__file__).resolve()
    if tools not in module_path.parents:
        raise RuntimeError("runtime module import escaped the installed package root")
    return module


def test_installed_imports_keep_exact_origin_with_an_unrelated_tools_package(installed_runtime_root, monkeypatch):
    from types import ModuleType
    foreign = ModuleType("TOOLS")
    foreign.__path__ = [str(ROOT / "GAME/TOOLS")]
    monkeypatch.setitem(sys.modules, "TOOLS", foreign)
    module = _installed_tool(installed_runtime_root, "catalog_runtime")
    assert Path(module.__file__).resolve().parent == installed_runtime_root / "TOOLS"
    source = module.load_activity_compiler_contract_source()
    assert source.runtime_root == installed_runtime_root
    assert sys.modules["TOOLS"] is foreign


def _current_installed_runtime_root() -> Path:
    if _INSTALLED_RUNTIME_ROOT is None:
        raise RuntimeError("installed runtime package fixture has not been initialized")
    return _INSTALLED_RUNTIME_ROOT


def _request(*, frontier_revision: int = 4) -> dict[str, object]:
    from DEV.TESTS.test_rd15_catalog_runtime import _request as build_request

    return build_request(frontier_revision=frontier_revision)


def _package_snapshots():
    installed_root = _current_installed_runtime_root()
    ruleset_package = _installed_tool(installed_root, "ruleset_package")
    package_id = "hdm.rules.dnd2024-srd52-core"
    manifest = ruleset_package.load_json_bytes(
        (
            installed_root
            / "RULES"
            / "packages"
            / package_id
            / "ruleset-package-manifest.json"
        ).read_bytes()
    )
    _lock, snapshots = ruleset_package.build_resolved_lock(
        [installed_root / "RULES" / "packages" / package_id],
        root_package_ids=[package_id],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    return snapshots


def _natural_owner_sources(request: dict[str, object]) -> dict[str, object]:
    from DEV.TESTS.test_rd15_catalog_runtime import (
        _natural_owner_sources as build_sources,
    )

    return build_sources(request)


def _installed_package_context(
    installed_runtime_root: Path,
    source: object,
    definition_kinds: Mapping[str, str],
) -> tuple[dict[str, object], Mapping[str, object]]:
    ruleset_package = _installed_tool(installed_runtime_root, "ruleset_package")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    package_id = "hdm.rules.dnd2024-srd52-core"
    package_root = installed_runtime_root / "RULES" / "packages" / package_id
    manifest = ruleset_package.load_json_bytes(
        (package_root / "ruleset-package-manifest.json").read_bytes()
    )
    lock, snapshots = ruleset_package.build_resolved_lock(
        [package_root],
        root_package_ids=[package_id],
        engine_version=source.engine_contract_inventory["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    package_row = lock["packages"][0]
    definition_ids = sorted(definition_kinds)
    request = {
        "basis": {
            "catalog_generation": manifest["catalog_generation"],
            "engine_version": source.engine_contract_inventory["engine_version"],
            "engine_contract_inventory_sha256": source.engine_contract_inventory[
                "inventory_sha256"
            ],
            "engine_contract_inventory": catalog_runtime._thaw(
                source.engine_contract_inventory
            ),
            "ruleset_lock": lock,
            "campaign_definition_frontier": {
                "frontier_id": "campaign.definitions",
                "state_revision": 4,
                "definition_ids": definition_ids,
            },
            "natural_owner_evidence": [],
        },
        "definition_dependencies": [
            {
                "source_type": "ruleset_package",
                "definition_id": definition_id,
                "kind": definition_kinds[definition_id],
                "package_id": package_id,
                "package_content_sha256": package_row["content_sha256"],
            }
            for definition_id in definition_ids
        ],
    }
    return request, snapshots


def _run_installed_runtime_probe(
    installed_runtime_root: Path,
    script: str,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(installed_runtime_root.resolve())
    return subprocess.run(
        [sys.executable, "-c", script, *arguments],
        cwd=installed_runtime_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def _actual_check_catalog(
    installed_runtime_root: Path,
    *,
    include_save: bool = False,
    include_action_surge: bool = False,
    include_innate_sorcery: bool = False,
) -> object:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    source = catalog_runtime.load_activity_compiler_contract_source()
    request = _request()
    inventory = catalog_runtime._thaw(source.engine_contract_inventory)
    request["basis"]["engine_contract_inventory"] = inventory
    request["basis"]["engine_contract_inventory_sha256"] = inventory[
        "inventory_sha256"
    ]
    extra_definitions = []
    if include_save:
        extra_definitions.append(("activity.save.generic", "definition.activity"))
    if include_action_surge:
        extra_definitions.extend(
            (
                ("activity.feature.action_surge", "definition.activity"),
                ("resource.action_surge", "definition.resource"),
            )
        )
    if include_innate_sorcery:
        extra_definitions.extend(
            (
                ("activity.feature.innate_sorcery", "definition.activity"),
                ("resource.innate_sorcery", "definition.resource"),
                ("effect.innate_sorcery", "definition.effect"),
            )
        )
    if extra_definitions:
        package_row = request["basis"]["ruleset_lock"]["packages"][0]
        for identity, kind in extra_definitions:
            request["basis"]["campaign_definition_frontier"]["definition_ids"].append(
                identity
            )
            request["definition_dependencies"].append(
                {
                    "source_type": "ruleset_package",
                    "definition_id": identity,
                    "kind": kind,
                    "package_id": package_row["package_id"],
                    "package_content_sha256": package_row["content_sha256"],
                }
            )
    return activity_runtime.admit_activity_catalog(
        request,
        package_snapshots=_package_snapshots(),
        engine_contract_inventory_source=source,
        natural_owner_sources=_natural_owner_sources(request),
        compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521",
    )


def test_compiler_contract_source_loader_binds_installed_projection(
    runtime_package_metadata: dict[str, object],
    installed_runtime_root: Path,
    tmp_path: Path,
) -> None:
    foreign_root = tmp_path / "self-hashed-foreign-runtime"
    shutil.copytree(installed_runtime_root, foreign_root)
    foreign_projection_path = (
        foreign_root / "TOOLS" / "activity_compiler_contracts.json"
    )
    foreign_projection = json.loads(
        foreign_projection_path.read_text(encoding="utf-8")
    )
    compiler_primitives = foreign_projection["families"]["primitive"][
        "activity_primitive_contracts"
    ]["contracts"]
    roll_contract = next(
        row for row in compiler_primitives if row["primitive_id"] == "op.roll"
    )
    assert roll_contract["selection_state"] == "ACTIVE_ADMITTED"
    roll_contract["selection_state"] = "DORMANT_RESERVED"
    foreign_bytes = package_closure.canonical_json(foreign_projection) + b"\n"
    foreign_projection_path.write_bytes(foreign_bytes)
    foreign_marker = foreign_root / "RUNTIME_PACKAGE.yaml"
    foreign_metadata = yaml.safe_load(
        foreign_marker.read_text(encoding="utf-8")
    )
    foreign_metadata["activity_compiler_contracts_sha256"] = (
        package_closure.sha256(foreign_bytes)
    )
    foreign_marker.write_text(
        yaml.safe_dump(foreign_metadata, sort_keys=False), encoding="utf-8"
    )
    from DEV.TOOLS.release_builder import validate_extracted_package_root

    # Candidate-root package validation is data validation only; it must never
    # issue the runtime source authority consumed by the compiler.
    assert validate_extracted_package_root(foreign_root) == foreign_root.resolve()

    expected_inventory = json.dumps(
        runtime_package_metadata["ruleset_engine_contract_inventory"],
        sort_keys=True,
        separators=(",", ":"),
    )
    script = """
import json
from pathlib import Path
import sys
from TOOLS.catalog_runtime import load_activity_compiler_contract_source

source = load_activity_compiler_contract_source()
assert source.runtime_root == Path.cwd().resolve()
assert source._is_admitted()
assert source.compiler_contracts_sha256 == sys.argv[1]
assert source.inventory_matches(json.loads(sys.argv[2]))
roll_contract = next(row for row in source.compiler_contracts["families"]["primitive"]["activity_primitive_contracts"]["contracts"] if row["primitive_id"] == "op.roll")
assert roll_contract["selection_state"] == "ACTIVE_ADMITTED"
try:
    load_activity_compiler_contract_source(Path(sys.argv[3]))
except TypeError:
    pass
else:
    raise AssertionError("caller-selected package root was accepted")
print(json.dumps({"runtime_root": str(source.runtime_root), "digest": source.compiler_contracts_sha256}))
"""
    result = _run_installed_runtime_probe(
        installed_runtime_root,
        script,
        str(runtime_package_metadata["activity_compiler_contracts_sha256"]),
        expected_inventory,
        str(foreign_root),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    evidence = json.loads(result.stdout)
    assert evidence["runtime_root"] == str(installed_runtime_root.resolve())
    assert (
        evidence["digest"]
        == runtime_package_metadata["activity_compiler_contracts_sha256"]
    )


def test_runtime_compiler_issuer_has_no_caller_selected_root() -> None:
    from inspect import signature

    from GAME.TOOLS.catalog_runtime import load_activity_compiler_contract_source

    assert tuple(signature(load_activity_compiler_contract_source).parameters) == ()


def test_compiled_instruction_abi_retains_guards_results_and_child_scope() -> None:
    from dataclasses import fields

    from GAME.TOOLS.activity_contracts import CompiledInstruction

    instruction_fields = {item.name for item in fields(CompiledInstruction)}
    assert {"guard", "result_contracts", "scope_bindings"} <= instruction_fields


def test_admitted_catalog_abi_retains_activity_specific_rejection_diagnostics() -> None:
    from dataclasses import fields

    from GAME.TOOLS.activity_contracts import AdmittedActivityCatalog

    catalog_fields = {item.name for item in fields(AdmittedActivityCatalog)}
    assert "unavailable_activity_reasons" in catalog_fields


def test_source_and_context_issuance_are_bound_to_the_exact_object() -> None:
    from dataclasses import replace
    from inspect import signature
    from types import MappingProxyType

    from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
    from GAME.TOOLS import catalog_runtime

    source_fields = signature(
        catalog_runtime.ActivityCompilerContractSource
    ).parameters
    source_values: dict[str, object] = {
        "engine_contract_inventory": MappingProxyType({}),
        "compiler_contracts": MappingProxyType({}),
        "compiler_contracts_bytes": b"{}\n",
        "compiler_contracts_sha256": "0" * 64,
    }
    if "runtime_root" in source_fields:
        source_values["runtime_root"] = ROOT / "GAME"
    source_values["_source_seal"] = catalog_runtime._COMPILER_CONTRACT_SOURCE_SEAL
    forged_source = catalog_runtime.ActivityCompilerContractSource(**source_values)
    assert not forged_source._is_admitted()

    context = _bind_context()
    assert context._is_admitted()
    assert not copy.copy(context)._is_admitted()
    assert not replace(context)._is_admitted()


def test_compiler_package_snapshots_must_originate_under_the_runtime_root(
    installed_runtime_root: Path,
    tmp_path: Path,
) -> None:
    from dataclasses import replace

    installed_root = installed_runtime_root
    catalog_runtime = _installed_tool(installed_root, "catalog_runtime")
    source = catalog_runtime.load_activity_compiler_contract_source()
    request, snapshots = _installed_package_context(
        installed_root, source, {"activity.check.generic": "definition.activity"}
    )

    catalog_runtime._validate_compiler_package_snapshot_origins(
        source, snapshots, request["basis"]
    )

    package_id, snapshot = next(iter(snapshots.items()))
    foreign_package = tmp_path / package_id
    shutil.copytree(snapshot.package_dir, foreign_package)
    foreign_snapshots = {
        package_id: replace(snapshot, package_dir=foreign_package)
    }
    with pytest.raises(catalog_runtime.CatalogBindingError, match="selected runtime"):
        catalog_runtime._validate_compiler_package_snapshot_origins(
            source, foreign_snapshots, request["basis"]
        )


def test_compiler_contract_source_rejects_absent_and_tampered_projection(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    CatalogBindingError = catalog_runtime.CatalogBindingError
    validate_package_root = (
        catalog_runtime.validate_activity_compiler_contracts_package_root
    )

    missing_root = tmp_path / "missing-runtime"
    shutil.copytree(installed_runtime_root, missing_root)
    (missing_root / "TOOLS" / "activity_compiler_contracts.json").unlink()
    with pytest.raises(CatalogBindingError, match="projection is unavailable"):
        validate_package_root(missing_root)

    tampered_root = tmp_path / "tampered-runtime"
    shutil.copytree(installed_runtime_root, tampered_root)
    tools = tampered_root / "TOOLS"
    projection_path = tools / "activity_compiler_contracts.json"
    canonical_bytes = projection_path.read_bytes()
    projection_path.write_bytes(canonical_bytes + b" ")
    with pytest.raises(CatalogBindingError, match="projection digest mismatch"):
        validate_package_root(tampered_root)


def test_compiler_source_rejects_runtime_inventory_claim_mismatch(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    CatalogBindingError = catalog_runtime.CatalogBindingError
    validate_package_root = (
        catalog_runtime.validate_activity_compiler_contracts_package_root
    )

    tampered_root = tmp_path / "inventory-mismatch-runtime"
    shutil.copytree(installed_runtime_root, tampered_root)
    manifest = tampered_root / "RUNTIME_PACKAGE.yaml"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    in_inventory = False
    changed = False
    for index, line in enumerate(lines):
        if line == "ruleset_engine_contract_inventory:":
            in_inventory = True
            continue
        if in_inventory and line and not line[0].isspace():
            in_inventory = False
        if in_inventory and line.lstrip().startswith("inventory_sha256:"):
            lines[index] = "  inventory_sha256: " + "0" * 64
            changed = True
    assert changed, "test did not locate the installed inventory digest"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(CatalogBindingError, match="inventory digest differs"):
        validate_package_root(tampered_root)


def test_compiler_source_rejects_runtime_attestation_claim_mismatch(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    CatalogBindingError = catalog_runtime.CatalogBindingError
    validate_package_root = (
        catalog_runtime.validate_activity_compiler_contracts_package_root
    )

    tampered_root = tmp_path / "attestation-mismatch-runtime"
    shutil.copytree(installed_runtime_root, tampered_root)
    manifest = tampered_root / "RUNTIME_PACKAGE.yaml"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    in_attestation = False
    changed = False
    for index, line in enumerate(lines):
        if line == "ruleset_conformance_attestation:":
            in_attestation = True
            continue
        if in_attestation and line and not line[0].isspace():
            in_attestation = False
        if in_attestation and line.lstrip().startswith(
            "engine_contract_inventory_sha256:"
        ):
            lines[index] = "  engine_contract_inventory_sha256: " + "0" * 64
            changed = True
    assert changed, "test did not locate the installed attestation digest"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(CatalogBindingError, match="attestation differs"):
        validate_package_root(tampered_root)


def test_compiler_projection_requires_integer_inventory_schema_version(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ruleset_package = _installed_tool(installed_runtime_root, "ruleset_package")
    CatalogBindingError = catalog_runtime.CatalogBindingError
    validate_package_root = (
        catalog_runtime.validate_activity_compiler_contracts_package_root
    )

    malformed_root = tmp_path / "float-inventory-schema-runtime"
    shutil.copytree(installed_runtime_root, malformed_root)
    projection_path = malformed_root / "TOOLS" / "activity_compiler_contracts.json"
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    projection["source_identity"]["inventory_schema_version"] = 2.0
    projection_bytes = ruleset_package.canonical_json(projection) + b"\n"
    projection_path.write_bytes(projection_bytes)

    manifest = malformed_root / "RUNTIME_PACKAGE.yaml"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith("activity_compiler_contracts_sha256:"):
            lines[index] = (
                "activity_compiler_contracts_sha256: "
                f"{ruleset_package.sha256(projection_bytes)}"
            )
            changed = True
    assert changed, "test did not locate the installed projection digest"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(CatalogBindingError, match="inventory schema version"):
        validate_package_root(malformed_root)


def test_real_source_binder_compiler_and_accept_command_route(
    installed_runtime_root: Path,
) -> None:
    script = """
import json
from pathlib import Path
from TOOLS.activity_runtime import admit_activity_catalog, compile_activity
from TOOLS.catalog_runtime import load_activity_compiler_contract_source, _thaw
from TOOLS.ruleset_package import build_resolved_lock, load_json_bytes
from TOOLS.runtime_execution import accept_command

root = Path.cwd().resolve()
assert not (root / "DEV").exists() and not (root / "GAME").exists()
source = load_activity_compiler_contract_source()
package_id = "hdm.rules.dnd2024-srd52-core"
package_root = root / "RULES" / "packages" / package_id
manifest = load_json_bytes((package_root / "ruleset-package-manifest.json").read_bytes())
lock, snapshots = build_resolved_lock(
    [package_root],
    root_package_ids=[package_id],
    engine_version=source.engine_contract_inventory["engine_version"],
    catalog_generation=manifest["catalog_generation"],
)
package_row = lock["packages"][0]
activity_id = "activity.feature.innate_sorcery"
resource_id = "resource.innate_sorcery"
effect_id = "effect.innate_sorcery"
definition_ids = sorted((activity_id, resource_id, effect_id))
request = {
    "basis": {
        "catalog_generation": manifest["catalog_generation"],
        "engine_version": source.engine_contract_inventory["engine_version"],
        "engine_contract_inventory_sha256": source.engine_contract_inventory["inventory_sha256"],
        "engine_contract_inventory": _thaw(source.engine_contract_inventory),
        "ruleset_lock": lock,
        "campaign_definition_frontier": {
            "frontier_id": "campaign.definitions",
            "state_revision": 4,
            "definition_ids": definition_ids,
        },
        "natural_owner_evidence": [],
    },
    "definition_dependencies": [
        {
            "source_type": "ruleset_package",
            "definition_id": identity,
            "kind": kind,
            "package_id": package_id,
            "package_content_sha256": package_row["content_sha256"],
        }
        for identity, kind in (
            (activity_id, "definition.activity"),
            (resource_id, "definition.resource"),
            (effect_id, "definition.effect"),
        )
    ],
}
catalog = admit_activity_catalog(
    request,
    package_snapshots=snapshots,
    engine_contract_inventory_source=source,
    natural_owner_sources={},
    compiler_generation=1,
    mode_policy_profile_id="execution.spell_cast.srd521",
)
compiled = compile_activity(catalog, activity_id)
accepted = accept_command(
    {"kind": "interpreter_result", "purpose": "interpret", "bundle_id": "bundle-sp02",
     "source_generation": "frontier-sp02", "intent": "use Innate Sorcery"},
    catalog.catalog_context,
    {"definition_id": activity_id, "kind": "definition.activity"},
    {"command_id": "turn-sp02-command", "interaction_id": "turn-sp02",
     "intent_plan_id": "turn-sp02-plan", "clause_id": "clause-action-surge",
     "action_request": {"activity_id": activity_id, "actor_id": "actor.sp02"},
     "root_resolution_id": "resolution.sp02"},
)
assert compiled.activity_id == activity_id
assert accepted["action_request"]["activity_id"] == activity_id
print(json.dumps({"runtime_root": str(source.runtime_root), "activity_id": compiled.activity_id,
                  "instruction_count": len(compiled.instructions), "accepted_command_id": accepted["command_id"]}))
"""
    result = _run_installed_runtime_probe(installed_runtime_root, script)
    assert result.returncode == 0, result.stderr or result.stdout
    evidence = json.loads(result.stdout)
    assert evidence["runtime_root"] == str(installed_runtime_root.resolve())
    assert evidence["activity_id"] == "activity.feature.innate_sorcery"
    assert evidence["instruction_count"] == 2
    assert evidence["accepted_command_id"] == "turn-sp02-command"


def _add_natural_activity_source(
    request: dict[str, object], record: dict[str, object]
) -> dict[str, object]:
    return _add_natural_activity_sources(request, [record])


def _add_natural_activity_sources(
    request: dict[str, object], records: list[dict[str, object]]
) -> dict[str, object]:
    runtime_root = _current_installed_runtime_root()
    catalog_runtime = _installed_tool(runtime_root, "catalog_runtime")
    ruleset_package = _installed_tool(runtime_root, "ruleset_package")
    natural_owner_evidence_domain = catalog_runtime.NATURAL_OWNER_EVIDENCE_DOMAIN

    frontier = request["basis"]["campaign_definition_frontier"]
    frontier["state_revision"] = 5
    evidence_rows = []
    immutable_member_bytes = {}
    for record in records:
        identity = str(record["id"])
        raw = ruleset_package.canonical_json(record)
        evidence = {
            "definition_id": identity,
            "kind": record["kind"],
            "owner_domain": "campaign",
            "scope": "campaign.definition_frontier",
            "route": f"campaign/definitions/{identity}.json",
            "pinned_revision": 5,
            "content_sha256": ruleset_package.sha256(raw),
        }
        frontier["definition_ids"].append(identity)
        request["basis"]["natural_owner_evidence"].append(evidence)
        request["definition_dependencies"].append(
            {
                "source_type": "natural_owner",
                "definition_id": identity,
                "kind": evidence["kind"],
                "owner_domain": evidence["owner_domain"],
                "scope": evidence["scope"],
                "route": evidence["route"],
                "pinned_revision": evidence["pinned_revision"],
                "evidence_sha256": ruleset_package.sha256(
                    natural_owner_evidence_domain
                    + ruleset_package.canonical_json(evidence)
                ),
            }
        )
        evidence_rows.append(copy.deepcopy(evidence))
        immutable_member_bytes[evidence["route"]] = raw
    return {
        "campaign": {
            "selected_frontier": copy.deepcopy(frontier),
            "members": evidence_rows,
            "immutable_member_bytes": immutable_member_bytes,
        }
    }


def test_dormant_primitive_source_is_retained_but_never_compiled(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityRuntimeError = activity_runtime.ActivityRuntimeError

    request = _request()
    source = catalog_runtime.load_activity_compiler_contract_source()
    inventory = catalog_runtime._thaw(source.engine_contract_inventory)
    request["basis"]["engine_contract_inventory"] = inventory
    request["basis"]["engine_contract_inventory_sha256"] = inventory["inventory_sha256"]
    activity_id = "campaign.dormant_branch"
    natural_sources = _add_natural_activity_source(
        request,
        {
            "id": activity_id,
            "kind": "definition.activity",
            "data": {
                "family_id": "activity.test",
                "steps": [{"op": "op.branch", "args": {}}],
            },
        },
    )

    catalog = activity_runtime.admit_activity_catalog(
        request,
        package_snapshots=_package_snapshots(),
        engine_contract_inventory_source=source,
        natural_owner_sources=natural_sources,
        compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521",
    )

    assert "activity.check.generic" in catalog.compiled_activities
    assert activity_id in catalog.frozen_definitions
    assert activity_id not in catalog.compiled_activities
    with pytest.raises(ActivityRuntimeError, match="dormant primitive"):
        activity_runtime.compile_activity(catalog, activity_id)


def test_primitive_activation_requires_transitive_active_primitive_closure(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityNotSelectable = activity_runtime.ActivityNotSelectable

    source = catalog_runtime.load_activity_compiler_contract_source()
    maps = activity_runtime._runtime_contract_maps(source)
    core, ledger_rows, primitive_rows, matrices, values = (
        maps[3],
        maps[5],
        dict(maps[6]),
        maps[7],
        maps[8],
    )
    primitive_rows.pop("op.consume_resource")

    with pytest.raises(ActivityNotSelectable, match="op.consume_resource"):
        activity_runtime._validate_active_primitive(
            "op.emit_fact",
            "activity.feature.action_surge",
            primitive_rows=primitive_rows,
            matrices=matrices,
            value_contracts=values,
            core=core,
            ledger_rows=ledger_rows,
        )

    cyclic_matrices = catalog_runtime._thaw(matrices)
    for primitive_id, dependency_id in (
        ("op.emit_fact", "op.consume_resource"),
        ("op.consume_resource", "op.emit_fact"),
    ):
        cyclic_matrices[primitive_id]["activation_dependencies"][
            "required_active_primitive_ids"
        ] = [dependency_id]
    with pytest.raises(ActivityNotSelectable, match="activation dependency cycle"):
        activity_runtime._validate_active_primitive(
            "op.emit_fact",
            "activity.feature.action_surge",
            primitive_rows=maps[6],
            matrices=cyclic_matrices,
            value_contracts=values,
            core=core,
            ledger_rows=ledger_rows,
        )


def test_card_lookup_is_narrowed_by_actual_actor_availability_source(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")

    actor_projection = json.loads(
        (
            ROOT / "DEV" / "TESTS" / "fixtures" / "s6d-07-character-mvp-actors.json"
        ).read_text(encoding="utf-8")
    )
    eligible_activity_ids = tuple(
        actor_projection["readiness_evidence"]["sorcerer"]["admitted_activity_ids"]
    )
    request = _request()
    package_id = "hdm.rules.dnd2024-srd52-core"
    package_row = request["basis"]["ruleset_lock"]["packages"][0]
    request["basis"]["campaign_definition_frontier"]["definition_ids"].append(
        "activity.spell.fire_bolt"
    )
    request["definition_dependencies"].append(
        {
            "source_type": "ruleset_package",
            "definition_id": "activity.spell.fire_bolt",
            "kind": "definition.activity",
            "package_id": package_id,
            "package_content_sha256": package_row["content_sha256"],
        }
    )
    natural_sources = _add_natural_activity_sources(
        request,
        [
            {
                "id": "campaign.card.fire_bolt",
                "kind": "definition.activity",
                "data": {
                    "family_id": "activity.cast",
                    "details": {
                        "capability_card": {
                            "definition_id": "campaign.card.fire_bolt",
                            "name": {"en": "Fire Bolt"},
                            "summary": "A supported cantrip card.",
                            "activity_ids": ["activity.spell.fire_bolt"],
                        }
                    },
                    "steps": [{"op": "op.branch", "args": {}}],
                },
            },
            {
                "id": "campaign.hidden_npc_spell",
                "kind": "definition.activity",
                "data": {
                    "family_id": "activity.cast",
                    "details": {
                        "capability_card": {
                            "definition_id": "campaign.hidden_npc_spell",
                            "name": {"en": "Hidden NPC Option"},
                            "summary": "A noneligible hidden card.",
                            "activity_ids": ["campaign.hidden_npc_spell"],
                        }
                    },
                    "steps": [{"op": "op.branch", "args": {}}],
                },
            },
        ],
    )
    source = catalog_runtime.load_activity_compiler_contract_source()
    inventory = catalog_runtime._thaw(source.engine_contract_inventory)
    request["basis"]["engine_contract_inventory"] = inventory
    request["basis"]["engine_contract_inventory_sha256"] = inventory["inventory_sha256"]
    catalog = activity_runtime.admit_activity_catalog(
        request,
        package_snapshots=_package_snapshots(),
        engine_contract_inventory_source=source,
        natural_owner_sources=natural_sources,
        compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521",
    )
    compiled_before = dict(catalog.compiled_activities)

    cards = activity_runtime.lookup_capability_cards(
        catalog,
        eligible_activity_ids=eligible_activity_ids,
        query="fire bolt",
        maximum_candidates=1,
    )
    broad_query = activity_runtime.lookup_capability_cards(
        catalog,
        eligible_activity_ids=eligible_activity_ids,
        query="hidden npc option",
        maximum_candidates=10,
    )

    assert [card["definition_id"] for card in cards] == ["campaign.card.fire_bolt"]
    assert broad_query == ()
    assert dict(catalog.compiled_activities) == compiled_before


def test_dormant_fact_and_unpermitted_consumer_are_rejected(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityNotSelectable = activity_runtime.ActivityNotSelectable

    source = catalog_runtime.load_activity_compiler_contract_source()
    contract_maps = activity_runtime._runtime_contract_maps(source)
    mechanical = contract_maps[1]

    with pytest.raises(
        ActivityNotSelectable, match="unknown, dormant, or unauthorized"
    ):
        activity_runtime._validate_fact_read(
            "fiction.target_visible",
            "activity.spell.fire_bolt",
            mechanical,
        )
    with pytest.raises(
        ActivityNotSelectable, match="unknown, dormant, or unauthorized"
    ):
        activity_runtime._validate_fact_read(
            "fiction.target_reachable",
            "activity.check.generic",
            mechanical,
        )
    activity_runtime._validate_fact_read(
        "fiction.target_reachable",
        "activity.spell.fire_bolt",
        mechanical,
    )


def test_dormant_and_unpermitted_accessor_reads_are_rejected(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityRuntimeError = activity_runtime.ActivityRuntimeError

    source = catalog_runtime.load_activity_compiler_contract_source()
    _admission, mechanical, _primitives, core, _portable, ledger_rows, *_ = (
        activity_runtime._runtime_contract_maps(source)
    )
    for accessor_ref in (
        {
            "accessor_id": "condition.value",
            "subject": "target",
            "condition_id": "condition.poisoned",
        },
        {"accessor_id": "health.current", "subject": "target"},
    ):
        reads: list[str] = []
        with pytest.raises(
            ActivityRuntimeError,
            match="accessor is unknown, dormant, or unauthorized",
        ):
            activity_runtime._compile_predicate_reads(
                {
                    "compare": {
                        "left": accessor_ref,
                        "operator": "eq",
                        "right": True,
                    }
                },
                activity_id="activity.spell.fire_bolt",
                mechanical=mechanical,
                core=core,
                ledger_rows=ledger_rows,
                reads=reads,
            )


def test_missing_transitive_definition_edge_and_cycle_reject_cold_catalog(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityRuntimeError = activity_runtime.ActivityRuntimeError

    source = catalog_runtime.load_activity_compiler_contract_source()

    inventory = catalog_runtime._thaw(source.engine_contract_inventory)
    snapshots = _package_snapshots()

    missing_request = _request()
    missing_request["basis"]["engine_contract_inventory"] = inventory
    missing_request["basis"]["engine_contract_inventory_sha256"] = inventory[
        "inventory_sha256"
    ]
    missing_sources = _add_natural_activity_source(
        missing_request,
        {
            "id": "campaign.missing_edge",
            "kind": "definition.activity",
            "references": ["campaign.unavailable_dependency"],
            "data": {
                "family_id": "activity.test",
                "steps": [{"op": "op.branch", "args": {}}],
            },
        },
    )
    with pytest.raises(
        ActivityRuntimeError, match="unavailable transitive dependencies"
    ):
        activity_runtime.admit_activity_catalog(
            missing_request,
            package_snapshots=snapshots,
            engine_contract_inventory_source=source,
            natural_owner_sources=missing_sources,
            compiler_generation=1,
            mode_policy_profile_id="execution.spell_cast.srd521",
        )

    cycle_request = _request()
    cycle_request["basis"]["engine_contract_inventory"] = inventory
    cycle_request["basis"]["engine_contract_inventory_sha256"] = inventory[
        "inventory_sha256"
    ]
    cycle_sources = _add_natural_activity_sources(
        cycle_request,
        [
            {
                "id": "campaign.cycle_a",
                "kind": "definition.activity",
                "references": ["campaign.cycle_b"],
                "data": {
                    "family_id": "activity.test",
                    "steps": [{"op": "op.branch", "args": {}}],
                },
            },
            {
                "id": "campaign.cycle_b",
                "kind": "definition.activity",
                "references": ["campaign.cycle_a"],
                "data": {
                    "family_id": "activity.test",
                    "steps": [{"op": "op.branch", "args": {}}],
                },
            },
        ],
    )
    with pytest.raises(ActivityRuntimeError, match="definition dependency cycle"):
        activity_runtime.admit_activity_catalog(
            cycle_request,
            package_snapshots=snapshots,
            engine_contract_inventory_source=source,
            natural_owner_sources=cycle_sources,
            compiler_generation=1,
            mode_policy_profile_id="execution.spell_cast.srd521",
        )


def test_dependency_graph_walk_handles_deep_finite_source_closure(
    installed_runtime_root: Path,
) -> None:
    _definition_graph = _installed_tool(
        installed_runtime_root, "activity_runtime"
    )._definition_graph

    dependency_ids = {f"campaign.node_{index}" for index in range(1500)}
    ordered_ids = sorted(dependency_ids)
    source_records = {
        identity: {
            "references": (ordered_ids[index + 1],)
            if index + 1 < len(ordered_ids)
            else ()
        }
        for index, identity in enumerate(ordered_ids)
    }

    graph = _definition_graph(dependency_ids, source_records)

    assert len(graph) == len(dependency_ids)
    assert graph[ordered_ids[0]] == (ordered_ids[1],)
    assert graph[ordered_ids[-1]] == ()


def test_selected_profile_registration_does_not_admit_an_occurrence(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")
    ActivityRuntimeError = activity_runtime.ActivityRuntimeError

    request = _request()
    source = catalog_runtime.load_activity_compiler_contract_source()
    inventory = catalog_runtime._thaw(source.engine_contract_inventory)
    request["basis"]["engine_contract_inventory"] = inventory
    request["basis"]["engine_contract_inventory_sha256"] = inventory["inventory_sha256"]
    natural_sources = _add_natural_activity_source(
        request,
        {
            "id": "campaign.unadmitted_profile",
            "kind": "definition.activity",
            "data": {
                "family_id": "activity.test",
                "profile_bindings": [
                    {
                        "consumer_id": "campaign.unadmitted_profile.step.0",
                        "profile_id": "execution.spell_cast.srd521",
                        "profile_generation": 1,
                    }
                ],
                "steps": [{"op": "op.branch", "args": {}}],
            },
        },
    )

    catalog = activity_runtime.admit_activity_catalog(
        request,
        package_snapshots=_package_snapshots(),
        engine_contract_inventory_source=source,
        natural_owner_sources=natural_sources,
        compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521",
    )

    assert "campaign.unadmitted_profile" in catalog.frozen_definitions
    assert "campaign.unadmitted_profile" not in catalog.compiled_activities
    with pytest.raises(ActivityRuntimeError, match="profile binding is not admitted"):
        activity_runtime.compile_activity(catalog, "campaign.unadmitted_profile")


def test_warm_compiled_handle_survives_path_mutation_but_cold_load_revalidates(
    installed_runtime_root: Path,
    tmp_path: Path,
) -> None:
    package_copy = tmp_path / "runtime-copy"
    shutil.copytree(installed_runtime_root, package_copy)
    script = """
import json
import sys
from pathlib import Path
from TOOLS.catalog_runtime import load_activity_compiler_contract_source, _thaw
from TOOLS.ruleset_package import build_resolved_lock, load_json_bytes
from TOOLS.activity_runtime import ActivityRuntimeError, admit_activity_catalog, compile_activity

root = Path.cwd().resolve()
package_id = "hdm.rules.dnd2024-srd52-core"
package_root = root / "RULES" / "packages" / package_id
manifest = load_json_bytes((package_root / "ruleset-package-manifest.json").read_bytes())
source = load_activity_compiler_contract_source()
activity_id = "activity.feature.innate_sorcery"
resource_id = "resource.innate_sorcery"
effect_id = "effect.innate_sorcery"
lock, snapshots = build_resolved_lock(
    [package_root], root_package_ids=[package_id],
    engine_version=source.engine_contract_inventory["engine_version"],
    catalog_generation=manifest["catalog_generation"],
)
package_row = lock["packages"][0]
definition_ids = sorted((activity_id, resource_id, effect_id))
request = {
    "basis": {
        "catalog_generation": manifest["catalog_generation"],
        "engine_version": source.engine_contract_inventory["engine_version"],
        "engine_contract_inventory_sha256": source.engine_contract_inventory["inventory_sha256"],
        "engine_contract_inventory": _thaw(source.engine_contract_inventory),
        "ruleset_lock": lock,
        "campaign_definition_frontier": {"frontier_id": "campaign.definitions", "state_revision": 4, "definition_ids": definition_ids},
        "natural_owner_evidence": [],
    },
    "definition_dependencies": [
        {"source_type": "ruleset_package", "definition_id": identity,
         "kind": kind, "package_id": package_id,
         "package_content_sha256": package_row["content_sha256"]}
        for identity, kind in (
            (activity_id, "definition.activity"),
            (resource_id, "definition.resource"),
            (effect_id, "definition.effect"),
        )
    ],
}
catalog = admit_activity_catalog(
    request, package_snapshots=snapshots,
    engine_contract_inventory_source=source, natural_owner_sources={},
    compiler_generation=1, mode_policy_profile_id="execution.spell_cast.srd521",
)
compiled = compile_activity(catalog, activity_id)
member = package_root / "character-mvp-seed.json"
original_bytes = member.read_bytes()
member.write_bytes(original_bytes + b" ")
observed = []
def audit(event, args):
    if event in {"open", "socket.connect"}:
        observed.append((event, args))
sys.addaudithook(audit)
warm = compile_activity(catalog, activity_id)
warm_reads = len(observed)
assert warm is compiled
assert warm_reads == 0, observed
try:
    admit_activity_catalog(
        request, package_snapshots=snapshots,
        engine_contract_inventory_source=source, natural_owner_sources={},
        compiler_generation=1, mode_policy_profile_id="execution.spell_cast.srd521",
    )
except ActivityRuntimeError as error:
    assert "catalog source binding failed" in str(error), str(error)
else:
    raise AssertionError("cold admission accepted mutated installed package bytes")
print(json.dumps({"activity_id": warm.activity_id, "warm_reads": warm_reads, "cold_reload_rejected": True}))
"""
    result = _run_installed_runtime_probe(package_copy, script)
    assert result.returncode == 0, result.stderr or result.stdout
    evidence = json.loads(result.stdout)
    assert evidence == {
        "activity_id": "activity.feature.innate_sorcery",
        "warm_reads": 0,
        "cold_reload_rejected": True,
    }


def test_copy_or_replace_cannot_reissue_catalog_or_compiled_activity(
    installed_runtime_root: Path,
) -> None:
    from copy import copy
    from dataclasses import replace

    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog = _actual_check_catalog(
        installed_runtime_root, include_innate_sorcery=True
    )
    activity_id = "activity.feature.innate_sorcery"
    compiled = activity_runtime.compile_activity(catalog, activity_id)

    for clone in (copy(catalog), replace(catalog)):
        with pytest.raises(
            activity_runtime.ActivityRuntimeError, match="compiler-issued"
        ):
            activity_runtime.compile_activity(clone, activity_id)

    assert not activity_runtime._compiled_identity_matches(
        catalog, activity_id, copy(compiled)
    )


def test_nested_compiled_mutation_invalidates_cache_and_repairs_from_admitted_bytes(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog = _actual_check_catalog(
        installed_runtime_root, include_innate_sorcery=True
    )
    activity_id = "activity.feature.innate_sorcery"
    compiled = activity_runtime.compile_activity(catalog, activity_id)
    original_primitive_id = compiled.instructions[0].primitive_id

    object.__setattr__(compiled.instructions[0], "primitive_id", "op.roll")

    repaired = activity_runtime.compile_activity(catalog, activity_id)

    assert repaired is not compiled
    assert repaired.instructions[0].primitive_id == original_primitive_id
    assert catalog.compiled_activities[activity_id] is repaired


def test_compiled_cache_identity_separates_every_typed_source_axis(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")

    key_builder = getattr(activity_runtime, "_compiled_cache_key", None)
    assert callable(key_builder), "compiled Activity cache identity builder is missing"
    identity = {
        "activity_id": "activity.check.generic",
        "definition_semantic_hash_generation": 1,
        "definition_semantic_hash": "a" * 64,
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": "b" * 64,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": "c" * 64,
        "engine_contract_inventory_sha256": "d" * 64,
        "compiler_generation": 1,
        "mode_policy_profile_id": "execution.spell_cast.srd521",
    }
    baseline = key_builder(identity)
    changed_axes = {
        "activity_id": "activity.save.generic",
        "definition_semantic_hash_generation": 2,
        "definition_semantic_hash": "e" * 64,
        "ruleset_set_digest_generation": 2,
        "ruleset_set_sha256": "f" * 64,
        "catalog_context_fingerprint_generation": 2,
        "catalog_context_fingerprint": "0" * 64,
        "engine_contract_inventory_sha256": "1" * 64,
        "compiler_generation": 2,
        "mode_policy_profile_id": "execution.spell_cast.ritual",
    }
    for field_name, changed_value in changed_axes.items():
        changed = dict(identity)
        changed[field_name] = changed_value
        assert key_builder(changed) != baseline, field_name


def test_corrupt_compiled_cache_entry_rebuilds_from_admitted_definition_bytes(
    installed_runtime_root: Path,
) -> None:
    from dataclasses import replace
    from types import MappingProxyType

    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    ActivityRuntimeError = activity_runtime.ActivityRuntimeError

    catalog = _actual_check_catalog(
        installed_runtime_root, include_innate_sorcery=True
    )
    activity_id = "activity.feature.innate_sorcery"
    compiled = activity_runtime.compile_activity(catalog, activity_id)
    corrupted_entry = replace(compiled, definition_semantic_hash="0" * 64)
    cache = dict(catalog.compiled_activities)
    cache[activity_id] = corrupted_entry
    object.__setattr__(catalog, "compiled_activities", MappingProxyType(cache))

    repaired = activity_runtime.compile_activity(catalog, activity_id)

    assert repaired is not corrupted_entry
    assert repaired.definition_semantic_hash == compiled.definition_semantic_hash
    assert repaired.instructions == compiled.instructions

    forged_catalog = replace(catalog, frozen_definitions=dict(catalog.frozen_definitions))
    with pytest.raises(ActivityRuntimeError, match="compiler-issued"):
        activity_runtime.compile_activity(forged_catalog, activity_id)


def test_explicit_generic_check_and_save_owner_templates_compile_without_evaluation(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog = _actual_check_catalog(installed_runtime_root, include_save=True)
    for family in ("check", "save"):
        compiled = activity_runtime.lookup_activity(catalog, f"activity.{family}.generic")
        symbol = compiled.symbol_contracts[f"compiled.generic_{family}_roll"]
        assert symbol["value_kind"] == "roll_request"
        assert symbol["template"]["kind"] == "D20_ABILITY_BASIS"
        assert symbol["template"]["modifier_basis"] == "AUTHORITATIVE_ABILITY_AND_PROFICIENCY"
        assert symbol["template"]["ability_parameter"] == "ability_id"
        assert compiled.parameter_contracts["dc"]["minimum"] == 1
        assert compiled.parameter_contracts["dc"]["maximum"] == 30
        assert compiled.role_contracts["actor"]["family_key"] == "world.actor"


def test_half_fire_damage_source_template_requires_the_same_full_damage_dependency(installed_runtime_root):
    source = _installed_tool(installed_runtime_root, "catalog_runtime").load_activity_compiler_contract_source()
    primitives = source.compiler_contracts["families"]["primitive"]["activity_primitive_contracts"]["contracts"]
    damage = next(row for row in primitives if row["primitive_id"] == "op.apply_damage")
    symbol = damage["compiler_declarations"]["activity.spell.burning_hands"]["symbols"]["compiled.half_fire_damage_floor"]
    assert symbol["value_kind"] == "damage_components"
    assert symbol["dependencies"] == ("compiled.full_fire_damage",)
    assert symbol["template"]["kind"] == "HALF_DAMAGE_FLOOR_MIN_ZERO"
    assert symbol["template"]["input_contract"] == "SAME_FIXED_FULL_DAMAGE_RESULT"


def test_unregistered_activity_family_is_an_activity_specific_diagnostic(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    catalog = _actual_check_catalog(
        installed_runtime_root, include_action_surge=True
    )

    diagnostic = catalog.unavailable_activity_reasons.get(
        "activity.feature.action_surge"
    )
    assert isinstance(diagnostic, str)
    assert "activity.magic" in diagnostic
    with pytest.raises(activity_runtime.ActivityNotSelectable, match="activity.magic"):
        activity_runtime.lookup_activity(catalog, "activity.feature.action_surge")


def test_selector_operation_pair_requires_source_and_active_ledger_edge(
    installed_runtime_root: Path,
) -> None:
    activity_runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    ActivityNotSelectable = activity_runtime.ActivityNotSelectable
    catalog_runtime = _installed_tool(installed_runtime_root, "catalog_runtime")

    source = catalog_runtime.load_activity_compiler_contract_source()
    maps = activity_runtime._runtime_contract_maps(source)
    mechanical, core, ledger_rows = maps[1], maps[3], maps[5]
    validate_pair = getattr(
        activity_runtime, "_selector_operation_pair_is_admitted", None
    )
    assert callable(validate_pair), "selector-operation pair validator is missing"

    validate_pair(
        "check.roll",
        "rule.add_flat",
        mechanical=mechanical,
        core=core,
        ledger_rows=ledger_rows,
    )
    with pytest.raises(ActivityNotSelectable, match="selector-operation pair"):
        validate_pair(
            "check.roll",
            "rule.grant_advantage",
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
        )


def _recipe_catalog(installed_root, record, dependencies=None):
    """Admit exact natural-owner recipe bytes against the installed source issuer."""
    runtime = _installed_tool(installed_root, "activity_runtime")
    binder = _installed_tool(installed_root, "catalog_runtime")
    source = binder.load_activity_compiler_contract_source()
    request, snapshots = _installed_package_context(
        installed_root, source, dependencies or {}
    )
    sources = _add_natural_activity_source(request, record)
    return runtime.admit_activity_catalog(
        request, package_snapshots=snapshots,
        engine_contract_inventory_source=source, natural_owner_sources=sources,
        compiler_generation=1, mode_policy_profile_id="execution.spell_cast.srd521",
    )


@pytest.fixture(scope="module")
def conformance_runtime_root(tmp_path_factory):
    """Build a complete installed package from bounded canonical conformance inputs."""
    from DEV.TOOLS import release_builder
    source_root = tmp_path_factory.mktemp("sp02-conformance-source")
    _stage_clean_source_tree(source_root)
    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    for path in primitive_root.glob("*.json"):
        row = json.loads(path.read_text())
        if row["contract"]["selection_state"] == "ACTIVE_ADMITTED":
            row["contract"]["compiler_declarations"] = {
                "activity.conformance.compiler": {"roles": {"actor": "world.actor", "target": "world.actor", "asset_owner": "world.asset"},
                    "symbols": {}, "profiles": [{"consumer_id": "activity.conformance.compiler.step.0",
                        "profile_id": "calculation.roll_advantage_srd521", "profile_generation": 1}] if path.name == "op.roll.json" else []}
            }
            path.write_text(json.dumps(row))
    loop_path = primitive_root / "op.for_each_target.json"
    loop = json.loads(loop_path.read_text())
    loop["contract"]["compiler_declarations"]["activity.conformance.compiler"]["symbols"] = {
        "compiled.targets": {"value_kind": "entity_ref", "cardinality": "many", "value": ["actor.target"],
            "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.1"]},
        "compiled.child_steps": {"value_kind": "compiled_step_list", "cardinality": "single", "value": [
            {"op": "op.roll", "args": {"request": {"roll_id": "roll.child", "expression": "1d20", "purpose_id": "roll.check", "roller_role": "actor"}}}],
            "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.1"]}}
    for reference_key in ("symbol_ref", "parameter_ref", "export_ref", "scope_ref"):
        loop["contract"]["compiler_declarations"]["activity.conformance.compiler"]["symbols"]["compiled.lowered_children_" + reference_key] = {
            "value_kind": "compiled_step_list", "cardinality": "single", "value": [{"op": "op.roll", "args": {
                "request": {reference_key: "compiled.nonexistent", "value_kind": "roll_request"}}}],
            "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.1"]}
    loop_path.write_text(json.dumps(loop))
    selector_path = source_root / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
    selectors = json.loads(selector_path.read_text())
    for entry in selectors["entries"]:
        if entry["id"] in {"check.roll", "damage.received"}:
            entry["consumer_or_dependency"] += "; activity.conformance.compiler"
    selector_path.write_text(json.dumps(selectors))
    roll_path = primitive_root / "op.roll.json"
    roll = json.loads(roll_path.read_text())
    symbol = {"value_kind": "roll_request", "cardinality": "single", "value": {
        "roll_id": "roll.symbol", "expression": "1d20", "purpose_id": "roll.check", "roller_role": "actor"},
        "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.0"]}
    symbols = {"compiled.request": copy.deepcopy(symbol), "compiled.dep": copy.deepcopy(symbol)}
    symbols["compiled.request"]["dependencies"] = ["compiled.dep"]
    for name in ("cycle_a", "cycle_b", "foreign_occurrence", "wrong_type", "unknown_dependency", "unknown_read"):
        symbols["compiled." + name] = copy.deepcopy(symbol)
    symbols["compiled.cycle_a"]["dependencies"] = ["compiled.cycle_b"]
    symbols["compiled.cycle_b"]["dependencies"] = ["compiled.cycle_a"]
    symbols["compiled.foreign_occurrence"]["permitted_occurrence_ids"] = ["activity.foreign.step.0"]
    symbols["compiled.wrong_type"]["value_kind"] = "integer"
    symbols["compiled.wrong_type"]["value"] = 1
    symbols["compiled.unknown_dependency"]["dependencies"] = ["compiled.absent"]
    symbols["compiled.unknown_read"]["reads"] = ["fact:fiction.foreign"]
    symbols["compiled.scoped_request"] = copy.deepcopy(symbol)
    symbols["compiled.scoped_request"]["scope"] = {"name": "target", "value_kind": "entity_ref", "family_key": "world.actor"}
    symbols["compiled.scoped_request"]["permitted_occurrence_ids"] = ["activity.conformance.compiler.step.1.steps.step.0"]
    symbols["compiled.scoped_request"]["value"]["roller_role"] = "target"
    roll["contract"]["compiler_declarations"]["activity.conformance.compiler"]["symbols"] = symbols
    roll_path.write_text(json.dumps(roll))
    damage_path = primitive_root / "op.apply_damage.json"
    damage = json.loads(damage_path.read_text())
    declaration = damage["contract"]["compiler_declarations"]["activity.conformance.compiler"]
    full = {"value_kind": "damage_components", "cardinality": "single", "value": [{"amount": 7, "damage_type_ref": "damage.fire"}],
        "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.0"]}
    half = {"value_kind": "damage_components", "cardinality": "single", "template": {
        "kind": "HALF_DAMAGE_FLOOR_MIN_ZERO", "source_symbol": "compiled.full", "input_contract": "SAME_FIXED_FULL_DAMAGE_RESULT"},
        "dependencies": ["compiled.full"], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.0"]}
    declaration["symbols"] = {"compiled.full": full, "compiled.half": half, "compiled.half_unavailable": copy.deepcopy(half)}
    declaration["symbols"]["compiled.half_unavailable"]["dependencies"] = ["compiled.unavailable"]
    declaration["symbols"]["compiled.half_unavailable"]["template"]["source_symbol"] = "compiled.unavailable"
    damage_path.write_text(json.dumps(damage))
    resource_path = primitive_root / "op.consume_resource.json"
    resource = json.loads(resource_path.read_text())
    resource["contract"]["compiler_declarations"]["activity.conformance.compiler"]["symbols"] = {
        "compiled.resource": {"value_kind": "resource_definition_ref", "cardinality": "single", "value": "resource.innate_sorcery",
            "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.0"]},
        "compiled.foreign_resource": {"value_kind": "resource_definition_ref", "cardinality": "single", "value": "effect.innate_sorcery",
            "dependencies": [], "reads": [], "permitted_occurrence_ids": ["activity.conformance.compiler.step.0"]}}
    resource_path.write_text(json.dumps(resource))
    rules = source_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
    lock, _ = package_closure.build_resolved_lock(
        [rules], root_package_ids=[rules.name], engine_version="1.0-alpha", catalog_generation=2,
    )
    package_closure.write_activity_compiler_contracts_projection(
        source_root, engine_version="1.0-alpha", ruleset_set_sha256=lock["ruleset_set_sha256"],
    )
    archive = release_builder.build_runtime_zip(
        source_root, tmp_path_factory.mktemp("sp02-conformance-build"), intended_tag="v1.0-alpha",
    )
    root = tmp_path_factory.mktemp("sp02-conformance-installed")
    with zipfile.ZipFile(archive) as runtime_zip:
        runtime_zip.extractall(root)
    release_builder.validate_extracted_package_root(root)
    return root


_RECIPE_PROBE = '''
import json, sys
from pathlib import Path
from TOOLS.catalog_runtime import load_activity_compiler_contract_source, _thaw, NATURAL_OWNER_EVIDENCE_DOMAIN
from TOOLS.ruleset_package import build_resolved_lock, canonical_json, sha256
from TOOLS.activity_runtime import admit_activity_catalog, compile_activity, ActivityRuntimeError
source = load_activity_compiler_contract_source()
assert source.runtime_root == Path.cwd().resolve()
import TOOLS.activity_runtime as runtime
assert Path(runtime.__file__).resolve().parent == Path.cwd().resolve() / "TOOLS"
package_id = "hdm.rules.dnd2024-srd52-core"
lock, snapshots = build_resolved_lock([Path.cwd()/"RULES/packages"/package_id], root_package_ids=[package_id], engine_version="1.0-alpha", catalog_generation=2)
record = json.loads(sys.argv[1])
dependency_kinds = json.loads(sys.argv[2])
identity = record["id"]
records = [record] + (json.loads(sys.argv[3]) if len(sys.argv) > 3 else [])
frontier = {"frontier_id":"campaign.definitions", "state_revision":5, "definition_ids":sorted([row["id"] for row in records] + list(dependency_kinds))}
evidence_rows, members = [], {}
for row in records:
    raw = canonical_json(row)
    evidence = {"definition_id":row["id"],"kind":row["kind"],"owner_domain":"campaign","scope":"campaign.definition_frontier","route":f"campaign/definitions/{row['id']}.json","pinned_revision":5,"content_sha256":sha256(raw)}
    evidence_rows.append(evidence)
    members[evidence["route"]] = raw
request = {"basis":{"catalog_generation":2,"engine_version":"1.0-alpha","engine_contract_inventory":_thaw(source.engine_contract_inventory),"engine_contract_inventory_sha256":source.engine_contract_inventory["inventory_sha256"],"ruleset_lock":lock,"campaign_definition_frontier":frontier,"natural_owner_evidence":evidence_rows},"definition_dependencies":[{"source_type":"ruleset_package","definition_id":key,"kind":kind,"package_id":package_id,"package_content_sha256":lock["packages"][0]["content_sha256"]} for key,kind in dependency_kinds.items()] + [{"source_type":"natural_owner",**{key:value for key,value in evidence.items() if key != "content_sha256"},"evidence_sha256":sha256(NATURAL_OWNER_EVIDENCE_DOMAIN+canonical_json(evidence))} for evidence in evidence_rows]}
sources = {"campaign":{"selected_frontier":frontier,"members":evidence_rows,"immutable_member_bytes":members}}
catalog = admit_activity_catalog(request, package_snapshots=snapshots,engine_contract_inventory_source=source,natural_owner_sources=sources,compiler_generation=1,mode_policy_profile_id="execution.spell_cast.srd521")
compiled = compile_activity(catalog,identity)
'''


def test_source_recipe_retains_requirements_activation_cost_and_timing(conformance_runtime_root):
    data = {
        "family_id": "activity.feature",
        "activation": {"economy_id": "resource.action", "amount": 1},
        "duration": {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.minute"},
        "requirements": {"compare": {"left": 1, "operator": "eq", "right": 1}},
        "costs": [{"resource_ref": "resource.innate_sorcery", "payer_role": "actor",
                   "amount": 1, "commitment_id": "cost_commit.on_accept"}],
        "steps": [{"op": "op.consume_resource", "args": {
            "resource_ref": "resource.innate_sorcery", "owner_role": "actor",
            "amount": 1, "commitment_id": "cost_commit.on_accept"}}],
    }
    script = _RECIPE_PROBE + '''
assert compiled.requirements == record["data"]["requirements"]
assert compiled.activation_contract == record["data"]["activation"]
assert compiled.cost_contracts == tuple(record["data"]["costs"])
assert compiled.duration_contract == record["data"]["duration"]
assert "resource.innate_sorcery" in compiled.dependency_ids
assert compiled.role_contracts["actor"]["family_key"] == "world.actor"
record["data"]["costs"][0]["amount"] = 9
assert compiled.cost_contracts[0]["amount"] == 1
'''
    result = _run_installed_runtime_probe(conformance_runtime_root, script,
        json.dumps({"id": "activity.conformance.compiler", "kind": "definition.activity", "data": data}),
        json.dumps({"resource.innate_sorcery": "definition.resource"}))
    assert result.returncode == 0, result.stderr


def test_source_recipe_profile_requires_exact_declared_occurrence(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["profile_bindings"] = [{"consumer_id": "activity.conformance.compiler.step.0",
        "profile_id": "calculation.roll_advantage_srd521", "profile_generation": 1}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
assert len(compiled.profile_bindings) == 1
assert compiled.profile_bindings[0].consumer_id == identity + ".step.0"
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr
    recipe["data"]["profile_bindings"][0]["consumer_id"] = "activity.conformance.compiler.step.1.steps.step.0"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "profile binding is not admitted" in result.stderr


@pytest.mark.parametrize("change, diagnostic", [
    ("child_export_escape", "unavailable Activity export"),
    ("invalid_guard_type", "typed_export_value"),
    ("unknown_child", "unknown or dormant primitive"),
    ("unknown_activation", "action_economy_id"),
    ("unknown_symbol", "unavailable source producer contract"),
])
def test_source_recipe_rejects_scope_type_and_permission_faults(conformance_runtime_root, change, diagnostic):
    recipe = _nested_recipe()
    if change == "child_export_escape":
        recipe["data"]["steps"].append({"op": "op.resolve_check", "args": {"roll": "roll.result", "threshold": 10}})
    elif change == "invalid_guard_type":
        recipe["data"]["steps"][1]["args"]["steps"][2]["when"] = {"result": "roll.result", "in": ["success"]}
    elif change == "unknown_child":
        recipe["data"]["steps"][1]["args"]["steps"][0]["op"] = "op.foreign"
    elif change == "unknown_activation":
        recipe["data"]["activation"] = {"economy_id": "resource.foreign", "amount": 1}
    else:
        recipe["data"]["steps"][1]["args"]["targets"] = "compiled.foreign"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert diagnostic in result.stderr


def _nested_recipe():
    return {"id": "activity.conformance.compiler", "kind": "definition.activity", "data": {
        "family_id": "activity.test",
        "steps": [
            {"op": "op.roll", "args": {"request": {"roll_id": "roll.outer", "expression": "1d20", "purpose_id": "roll.check", "roller_role": "actor"}}, "export": "outer"},
            {"op": "op.for_each_target", "args": {"targets": "compiled.targets", "steps": [
                {"op": "op.roll", "args": {"request": {"roll_id": "roll.conformance", "expression": "1d20", "purpose_id": "roll.check", "roller_role": "actor"}}, "export": "roll"},
                {"op": "op.resolve_check", "args": {"roll": "roll.result", "threshold": 10}, "export": "check"},
                {"op": "op.roll", "when": {"result": "check.outcome", "in": ["failure"]}, "args": {"request": {"roll_id": "roll.retry", "expression": "1d20", "purpose_id": "roll.check", "roller_role": "actor"}}}
            ]}, "export": "per_target"}
        ]}}


def test_admitted_source_recipe_recursively_lowers_children_and_retains_guards(conformance_runtime_root):
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
loop = compiled.instructions[1]
assert len(loop.children) == 3
assert loop.arguments["steps"] == tuple(child.consumer_id for child in loop.children)
assert loop.children[0].consumer_id == identity + ".step.1.steps.step.0"
assert loop.children[2].guard == {"result":"check.outcome","in":("failure",)}
assert loop.scope_bindings["target"] == {"source_export":"compiled.targets","value_kind":"entity_ref","family_key":"world.actor"}
assert loop.children[1].arguments["roll"] == {"export_ref":"roll.result","value_kind":"prior_roll_result"}
assert loop.children[0].consumer_id in compiled.consumer_read_plan
assert "binding:targets" in loop.read_contract_refs
''', json.dumps(_nested_recipe()), "{}")
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("symbol, diagnostic", [
    ("cycle_a", "producer dependency cycle"),
    ("foreign_occurrence", "producer is unauthorized"),
    ("wrong_type", "wrong type/cardinality"),
    ("unknown_dependency", "unavailable source producer contract: compiled.absent"),
    ("unknown_read", "unknown, dormant, or unauthorized"),
])
def test_typed_source_producer_rejects_cycles_types_and_unknown_permissions(conformance_runtime_root, symbol, diagnostic):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.roll", "args": {"request": "compiled." + symbol}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_typed_source_producer_retains_transitive_contracts(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.roll", "args": {"request": "compiled.request"}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
assert set(compiled.symbol_contracts) == {"compiled.request", "compiled.dep"}
assert compiled.instructions[0].arguments["request"] == {"symbol_ref":"compiled.request", "value_kind":"roll_request"}
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def test_tactical_mind_explicit_owner_template_preserves_fixed_prior_and_success_spend(installed_runtime_root):
    binder = _installed_tool(installed_runtime_root, "catalog_runtime")
    runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    source = binder.load_activity_compiler_contract_source()
    request, snapshots = _installed_package_context(installed_runtime_root, source, {
        "activity.feature.tactical_mind": "definition.activity", "resource.second_wind": "definition.resource"})
    catalog = runtime.admit_activity_catalog(request, package_snapshots=snapshots,
        engine_contract_inventory_source=source, natural_owner_sources={}, compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521")
    compiled = runtime.compile_activity(catalog, "activity.feature.tactical_mind")
    template = compiled.symbol_contracts["compiled.d10_plus_prior_check_total"]["template"]
    assert template["kind"] == "D10_FIXED_FAILED_CHECK"
    assert template["prior_result_source"] == "ACCEPTED_FAILED_ABILITY_CHECK"
    assert template["modifier_basis"] == "FIXED_PRIOR_TOTAL"
    assert compiled.parameter_contracts["prior_check_dc"]["source_class"] == "ENGINE_BOUND"
    assert compiled.instructions[2].guard == {"result": "augmented_check.outcome", "in": ("success",)}


def test_source_branch_remains_dormant_under_current_source_admission(conformance_runtime_root):
    recipe = _nested_recipe()
    first = recipe["data"]["steps"][0]
    recipe["data"]["steps"] = [{"op": "op.branch", "args": {
        "when": {"compare": {"left": 1, "operator": "eq", "right": 1}},
        "then_steps": [dict(first, export="branch_roll")],
        "else_steps": [dict(first, export="branch_roll")],
    }}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "unknown or dormant primitive: op.branch" in result.stderr


@pytest.mark.parametrize("change, diagnostic", [
    ("predicate_types", "predicate operands"),
    ("selector_type", "selector result has wrong value kind"),
    ("target_bound", "target minimum exceeds maximum"),
    ("cost_amount", "numeric bound"),
])
def test_source_recipe_rejects_predicate_selector_target_and_cost_types(conformance_runtime_root, change, diagnostic):
    recipe = _nested_recipe()
    if change == "predicate_types":
        recipe["data"]["requirements"] = {"compare": {"left": 1, "operator": "eq", "right": True}}
    elif change == "selector_type":
        recipe["data"]["steps"][0]["args"]["request"] = "selector.check.roll"
    elif change == "target_bound":
        recipe["data"]["targeting"] = {"kind_id": "target.entities", "minimum": 3, "maximum": 2}
    else:
        recipe["data"]["costs"] = [{"resource_ref": "resource.innate_sorcery", "payer_role": "actor", "amount": -1, "commitment_id": "cost_commit.on_accept"}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_declared_role_cannot_relabel_a_resources_native_owner_family(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.consume_resource", "args": {
        "owner_role": "asset_owner", "resource_ref": "resource.innate_sorcery", "amount": 1}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe),
        json.dumps({"resource.innate_sorcery": "definition.resource"}))
    assert result.returncode != 0
    assert "conflicting owner-family" in result.stderr


def test_typed_source_child_list_producer_is_lowered_not_left_as_raw_grammar(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"][1]["args"]["steps"] = "compiled.child_steps"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
loop = compiled.instructions[1]
assert len(loop.children) == 1
assert loop.arguments["steps"] == (loop.children[0].consumer_id,)
assert compiled.symbol_contracts["compiled.child_steps"]["value_kind"] == "compiled_step_list"
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def test_source_producer_scope_suffix_requires_an_exact_typed_child_binding(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"][1]["args"]["steps"][0]["args"]["request"] = "compiled.scoped_request:$target"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
request = compiled.instructions[1].children[0].arguments["request"]
assert request == {"symbol_ref":"compiled.scoped_request:target", "value_kind":"roll_request"}
assert compiled.symbol_contracts["compiled.scoped_request"]["scope"]["family_key"] == "world.actor"
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr
    recipe["data"]["steps"][1]["args"]["steps"][0]["args"]["request"] = "compiled.scoped_request:$foreign"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "producer scope is unavailable or incompatible" in result.stderr


def test_half_damage_producer_retains_same_input_and_requires_dependency_closure(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.apply_damage", "args": {"target_role": "target", "components": "compiled.half"}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
assert set(compiled.symbol_contracts) == {"compiled.half", "compiled.full"}
assert compiled.symbol_contracts["compiled.half"]["template"]["source_symbol"] == "compiled.full"
assert compiled.instructions[0].arguments["components"] == {"symbol_ref":"compiled.half", "value_kind":"damage_components"}
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr
    recipe["data"]["steps"][0]["args"]["components"] = "compiled.half_unavailable"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "unavailable source producer contract: compiled.unavailable" in result.stderr


def test_guarded_export_requires_its_source_guard_in_the_consuming_scope(conformance_runtime_root):
    recipe = _nested_recipe()
    children = recipe["data"]["steps"][1]["args"]["steps"]
    children[2]["export"] = "conditional_roll"
    children.append({"op": "op.resolve_check", "args": {"roll": "conditional_roll.result", "threshold": 10}})
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "guarded export is unavailable in this scope" in result.stderr
    children[3]["when"] = children[2]["when"]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def test_child_may_shadow_an_outer_export_once_but_not_duplicate_it(conformance_runtime_root):
    recipe = _nested_recipe()
    children = recipe["data"]["steps"][1]["args"]["steps"]
    children[0]["export"] = "outer"
    children[1]["args"]["roll"] = "outer.result"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr
    children[2]["export"] = "outer"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "duplicate Activity export: outer" in result.stderr


def test_source_definition_closure_is_retained_and_survives_compiled_cache_repair(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["references"] = ["campaign.dep_one"]
    dormant = {"family_id": "activity.test", "steps": [{"op": "op.branch", "args": {}}]}
    dependencies = [{"id": "campaign.dep_one", "kind": "definition.activity", "references": ["campaign.dep_two"], "data": dormant},
        {"id": "campaign.dep_two", "kind": "definition.activity", "data": dormant}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
from types import MappingProxyType
assert {"campaign.dep_one", "campaign.dep_two"} <= set(compiled.dependency_ids)
assert catalog.definition_dependency_graph[identity] == ("campaign.dep_one",)
object.__setattr__(catalog, "compiled_activities", MappingProxyType({}))
rebuilt = compile_activity(catalog, identity)
assert rebuilt is not compiled
assert rebuilt.dependency_ids == compiled.dependency_ids
''', json.dumps(recipe), "{}", json.dumps(dependencies))
    assert result.returncode == 0, result.stderr


def test_warm_lookup_does_not_recensus_immutable_catalog_or_engine_sources(installed_runtime_root):
    runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    contracts = _installed_tool(installed_runtime_root, "activity_contracts")
    catalog = _actual_check_catalog(installed_runtime_root, include_innate_sorcery=True)
    activity_id = "activity.feature.innate_sorcery"
    compiled = runtime.compile_activity(catalog, activity_id)
    forbidden = {id(catalog.frozen_definitions), id(catalog.frozen_semantic_members),
        id(catalog.engine_contract_inventory), id(catalog.definition_dependency_graph),
        id(catalog.catalog_context._compiler_contract_source.compiler_contracts)}
    observed = []
    def profile(frame, event, _arg):
        if (event == "call" and frame.f_code is contracts._compiler_value_snapshot.__code__
            and id(frame.f_locals.get("value")) in forbidden):
            observed.append(id(frame.f_locals["value"]))
    previous = sys.getprofile()
    try:
        sys.setprofile(profile)
        assert runtime.compile_activity(catalog, activity_id) is compiled
    finally:
        sys.setprofile(previous)
    assert observed == []


def test_source_subclass_cannot_override_exact_source_issuance(installed_runtime_root):
    from dataclasses import fields
    runtime = _installed_tool(installed_runtime_root, "activity_runtime")
    binder = _installed_tool(installed_runtime_root, "catalog_runtime")
    source = binder.load_activity_compiler_contract_source()
    class SpoofedSource(type(source)):
        def _is_admitted(self):
            return True
    spoofed = SpoofedSource(**{field.name: getattr(source, field.name) for field in fields(source)})
    request, snapshots = _installed_package_context(installed_runtime_root, source, {
        "activity.check.generic": "definition.activity"})
    with pytest.raises(runtime.ActivityRuntimeError, match="authenticated package source"):
        runtime.admit_activity_catalog(request, package_snapshots=snapshots,
            engine_contract_inventory_source=spoofed, natural_owner_sources={}, compiler_generation=1,
            mode_policy_profile_id="execution.spell_cast.srd521")


@pytest.mark.parametrize("reference", ["effect.innate_sorcery", "compiled.foreign_resource"])
def test_definition_reference_uses_actual_bound_kind_not_an_identifier_shape(conformance_runtime_root, reference):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.consume_resource", "args": {"owner_role": "actor", "resource_ref": reference, "amount": 1}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe),
        json.dumps({"effect.innate_sorcery": "definition.effect"}))
    assert result.returncode != 0
    assert "definition dependency has wrong kind" in result.stderr


def test_source_resource_producer_retains_actual_definition_and_owner_contract(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["steps"] = [{"op": "op.consume_resource", "args": {"owner_role": "actor", "resource_ref": "compiled.resource", "amount": 1}}]
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
assert "resource.innate_sorcery" in compiled.dependency_ids
assert compiled.instructions[0].arguments["resource_ref"] == {"symbol_ref":"compiled.resource","value_kind":"resource_definition_ref"}
assert compiled.role_contracts["actor"]["family_key"] == "world.actor"
''', json.dumps(recipe), json.dumps({"resource.innate_sorcery": "definition.resource"}))
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("reference_key", ["symbol_ref", "parameter_ref", "export_ref", "scope_ref"])
@pytest.mark.parametrize("site", ["top", "child", "literal_member", "producer_children"])
def test_source_authored_lowered_reference_objects_reject_before_issuance(conformance_runtime_root, reference_key, site):
    recipe = _nested_recipe()
    wrapper = {reference_key: "compiled.nonexistent", "value_kind": "roll_request"}
    if site == "producer_children":
        recipe["data"]["steps"][1]["args"]["steps"] = "compiled.lowered_children_" + reference_key
    else:
        target = recipe["data"]["steps"][0] if site in {"top", "literal_member"} else recipe["data"]["steps"][1]["args"]["steps"][0]
        if site == "literal_member":
            target["args"]["request"]["expression"] = wrapper
        else:
            target["args"]["request"] = wrapper
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "source-authored lowered reference object" in result.stderr


def test_portable_literal_requests_still_compile_with_descriptive_reference_text(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["details"] = {"symbol_ref": "description", "value_kind": "description"}
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
assert compiled.instructions[0].arguments["request"]["expression"] == "1d20"
assert compiled.instructions[1].children[0].arguments["request"]["roll_id"] == "roll.conformance"
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def _named_roll_recipe():
    first = _nested_recipe()["data"]["steps"][0]
    first["export"] = "a"
    second = copy.deepcopy(first)
    second["export"] = "b"
    second["args"]["request"]["roll_id"] = "roll.second"
    second["args"]["request"]["expression"] = "1d6"
    return {"id": "activity.conformance.compiler", "kind": "definition.activity", "data": {
        "family_id": "activity.test", "steps": [first, second,
            {"op": "op.resolve_check", "args": {"roll": "a.result", "threshold": 10}, "export": "check"}]}}


def test_swapping_named_exports_changes_the_actual_compiled_tree_association(conformance_runtime_root):
    recipe = _named_roll_recipe()
    script = _RECIPE_PROBE + '''
original = compiled
swapped = json.loads(sys.argv[1])
swapped["data"]["steps"][0]["export"], swapped["data"]["steps"][1]["export"] = "b", "a"
sys.argv[1] = json.dumps(swapped)
''' + _RECIPE_PROBE + '''
assert original.instructions != compiled.instructions, "export swap disappeared from compiled tree"
assert tuple(step.export_name for step in original.instructions) == ("a", "b", "check")
assert tuple(step.export_name for step in compiled.instructions) == ("b", "a", "check")
assert original.instructions[2].arguments["roll"] == compiled.instructions[2].arguments["roll"]
assert next(step.consumer_id for step in original.instructions if step.export_name == "a") == identity + ".step.0"
assert next(step.consumer_id for step in compiled.instructions if step.export_name == "a") == identity + ".step.1"
'''
    result = _run_installed_runtime_probe(conformance_runtime_root, script, json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def test_named_export_declarations_survive_child_shadow_guards_requirements_and_cache_repair(conformance_runtime_root):
    recipe = _nested_recipe()
    recipe["data"]["requirements"] = {"compare": {"left": 1, "operator": "eq", "right": 1}}
    children = recipe["data"]["steps"][1]["args"]["steps"]
    children[0]["export"] = "outer"
    children[1]["args"]["roll"] = "outer.result"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE + '''
root, loop = compiled.instructions
assert root.export_name == "outer" and loop.export_name == "per_target"
assert tuple(child.export_name for child in loop.children) == ("outer", "check", None)
assert loop.children[1].arguments["roll"]["export_ref"] == "outer.result"
assert loop.children[2].guard["result"] == "check.outcome"
assert compiled.requirements == record["data"]["requirements"]
object.__setattr__(loop.children[0], "export_name", "foreign")
repaired = compile_activity(catalog, identity)
assert repaired is not compiled
assert repaired.instructions[1].children[0].export_name == "outer"
assert repaired.instructions[1].children[1].export_name == "check"
''', json.dumps(recipe), "{}")
    assert result.returncode == 0, result.stderr


def test_swapped_export_with_wrong_result_member_rejects_in_its_lexical_scope(conformance_runtime_root):
    recipe = _named_roll_recipe()
    recipe["data"]["steps"][2]["args"]["roll"] = "a.outcome"
    result = _run_installed_runtime_probe(conformance_runtime_root, _RECIPE_PROBE, json.dumps(recipe), "{}")
    assert result.returncode != 0
    assert "unavailable Activity export reference: a.outcome" in result.stderr
