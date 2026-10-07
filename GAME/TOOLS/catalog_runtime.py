#!/usr/bin/env python3
"""Exact, caller-supplied catalog-context binding for HDM execution.

This module neither discovers catalog content nor supplies a default context. A
consumer must bind an exact resolved ruleset lock, definition frontier,
definition dependencies, and admitted immutable engine/campaign/session source
evidence before it can use an interpreter candidate.
"""

from __future__ import annotations

import copy
import threading
import weakref
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .ruleset_package import (
    INVENTORY_DOMAIN,
    REQUIRED_ENGINE_CONTRACT_FAMILIES,
    RULESET_SET_DIGEST_GENERATION,
    PackageSnapshot,
    RulesetContractError,
    _validated_engine_contract_entries,
    build_resolved_lock,
    canonical_json,
    load_json_bytes,
    semantic_entries,
    sha256,
    validate_resolved_lock,
)

# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.2"
CATALOG_CONTEXT_FINGERPRINT_GENERATION: Final = 1
CATALOG_CONTEXT_DOMAIN: Final = b"HDM_CATALOG_CONTEXT/1\n"
NATURAL_OWNER_EVIDENCE_DOMAIN: Final = b"HDM_CATALOG_NATURAL_OWNER_EVIDENCE/1\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")
_NATURAL_OWNER_SCOPES: Final = {
    "campaign": "campaign.definition_frontier",
    "session": "session.overlay_frontier",
}
_NATURAL_OWNER_ROUTE_PREFIXES: Final = {
    "campaign": "campaign/definitions/",
    "session": "session/overlays/",
}
_ADMITTED_CONTEXT_SEAL: Final = object()
_COMPILER_CONTRACT_SOURCE_SEAL: Final = object()


class CatalogBindingError(ValueError):
    """Raised when an exact catalog context or executable binding is invalid."""


@dataclass(frozen=True)
class ActivityCompilerContractSource:
    """Installed, package-bound compiler contracts; never caller-authored proof."""

    runtime_root: Path
    engine_contract_inventory: Mapping[str, object]
    compiler_contracts: Mapping[str, object]
    compiler_contracts_bytes: bytes
    compiler_contracts_sha256: str
    _source_seal: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._source_seal is not _COMPILER_CONTRACT_SOURCE_SEAL:
            raise CatalogBindingError(
                "compiler contract source is not package-authenticated"
            )

    def _is_admitted(self) -> bool:
        if self._source_seal is not _COMPILER_CONTRACT_SOURCE_SEAL:
            return False
        with _COMPILER_SOURCE_LOCK:
            entry = _COMPILER_SOURCE_ISSUANCES.get(id(self))
        if entry is None or entry[0]() is not self:
            return False
        issued_fields = entry[1]
        try:
            return (
                self.runtime_root == _current_runtime_package_root()
                and self.runtime_root == issued_fields[0]
                and self.engine_contract_inventory is issued_fields[1]
                and self.compiler_contracts is issued_fields[2]
                and self.compiler_contracts_bytes is issued_fields[3]
                and self.compiler_contracts_sha256 == issued_fields[4]
            )
        except CatalogBindingError:
            return False

    def inventory_matches(self, value: object) -> bool:
        return self._is_admitted() and _thaw(self.engine_contract_inventory) == value


_COMPILER_SOURCE_LOCK = threading.RLock()
_COMPILER_SOURCE_ISSUANCES: dict[
    int,
    tuple[
        weakref.ReferenceType[ActivityCompilerContractSource],
        tuple[object, ...],
    ],
] = {}


def _remember_compiler_source(source: ActivityCompilerContractSource) -> None:
    identity = id(source)

    def forget(reference: weakref.ReferenceType[ActivityCompilerContractSource]) -> None:
        with _COMPILER_SOURCE_LOCK:
            current = _COMPILER_SOURCE_ISSUANCES.get(identity)
            if current is not None and current[0] is reference:
                del _COMPILER_SOURCE_ISSUANCES[identity]

    reference = weakref.ref(source, forget)
    fields_snapshot = (
        source.runtime_root,
        source.engine_contract_inventory,
        source.compiler_contracts,
        source.compiler_contracts_bytes,
        source.compiler_contracts_sha256,
    )
    with _COMPILER_SOURCE_LOCK:
        _COMPILER_SOURCE_ISSUANCES[identity] = (reference, fields_snapshot)


@dataclass(frozen=True)
class BoundCatalogContext:
    """One immutable logical context with reconstructive input evidence."""

    basis: Mapping[str, object]
    definition_dependencies: tuple[Mapping[str, object], ...]
    fingerprint: str
    _admission_seal: object = field(default=None, repr=False, compare=False)
    _compiler_contract_source: ActivityCompilerContractSource | None = field(
        default=None, repr=False, compare=False
    )
    _definition_semantic_hashes: Mapping[str, str] = field(
        default_factory=lambda: MappingProxyType({}), repr=False, compare=False
    )

    def _is_admitted(self) -> bool:
        if self._admission_seal is not _ADMITTED_CONTEXT_SEAL:
            return False
        with _CONTEXT_LOCK:
            entry = _CONTEXT_ISSUANCES.get(id(self))
        if entry is None or entry[0]() is not self:
            return False
        issued_fields = entry[1]
        return (
            self.basis is issued_fields[0]
            and self.definition_dependencies is issued_fields[1]
            and self.fingerprint == issued_fields[2]
            and self._compiler_contract_source is issued_fields[3]
            and self._definition_semantic_hashes is issued_fields[4]
            and (
                self._compiler_contract_source is None
                or type(self._compiler_contract_source) is ActivityCompilerContractSource
                and self._compiler_contract_source._is_admitted()
            )
        )

    def to_dict(self) -> dict[str, object]:
        """Return a serializable carrier without exposing mutable internal state."""

        if not self._is_admitted():
            raise CatalogBindingError("catalog context is not issuer-owned")
        return {
            "basis": _thaw(self.basis),
            "definition_dependencies": [
                dict(row) for row in self.definition_dependencies
            ],
            "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
            "catalog_context_fingerprint": self.fingerprint,
        }


_CONTEXT_LOCK = threading.RLock()
_CONTEXT_ISSUANCES: dict[
    int,
    tuple[
        weakref.ReferenceType[BoundCatalogContext],
        tuple[object, ...],
    ],
] = {}


def _remember_bound_catalog_context(context: BoundCatalogContext) -> None:
    if (
        context._admission_seal is not _ADMITTED_CONTEXT_SEAL
        or context._compiler_contract_source is not None
        and not context._compiler_contract_source._is_admitted()
    ):
        raise CatalogBindingError("catalog context inputs are not issuer-owned")
    identity = id(context)

    def forget(reference: weakref.ReferenceType[BoundCatalogContext]) -> None:
        with _CONTEXT_LOCK:
            current = _CONTEXT_ISSUANCES.get(identity)
            if current is not None and current[0] is reference:
                del _CONTEXT_ISSUANCES[identity]

    reference = weakref.ref(context, forget)
    fields_snapshot = (
        context.basis,
        context.definition_dependencies,
        context.fingerprint,
        context._compiler_contract_source,
        context._definition_semantic_hashes,
    )
    with _CONTEXT_LOCK:
        _CONTEXT_ISSUANCES[identity] = (reference, fields_snapshot)


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_thaw(item) for item in value]
    return value


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CatalogBindingError(f"{label} must be an object")
    return value


def _require_exact_keys(
    value: object, expected: set[str], label: str, *, optional: set[str] | None = None
) -> Mapping[str, object]:
    mapping = _require_mapping(value, label)
    allowed = expected | (optional or set())
    if set(mapping) - allowed or not expected.issubset(mapping):
        raise CatalogBindingError(f"{label} has unexpected or missing fields")
    return mapping


def _require_id(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or not value[0].isalpha()
        or not all(character.isalnum() or character in "_.:-" for character in value)
    ):
        raise CatalogBindingError(f"{label} must be a native identifier")
    return value


def _require_sha256(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in _SHA256_HEX for character in value)
    ):
        raise CatalogBindingError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _require_revision(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise CatalogBindingError(f"{label} must be a non-negative integer")
    return value


def _contains_dev_path(value: object) -> bool:
    if isinstance(value, str):
        return "DEV/" in value
    if isinstance(value, Mapping):
        return any(
            _contains_dev_path(key) or _contains_dev_path(item)
            for key, item in value.items()
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(_contains_dev_path(item) for item in value)
    return False


def _runtime_package_lines(runtime_root: Path) -> tuple[str, ...]:
    package_root = Path(runtime_root).resolve()
    marker = package_root / "RUNTIME_PACKAGE.yaml"
    if not marker.is_file() or marker.is_symlink():
        raise CatalogBindingError("selected runtime package marker is unavailable")
    try:
        return tuple(marker.read_text(encoding="utf-8").splitlines())
    except (OSError, UnicodeDecodeError) as exc:
        raise CatalogBindingError(
            "selected runtime package marker is unreadable"
        ) from exc


def _current_runtime_package_root() -> Path:
    module_path = Path(__file__).resolve()
    tools_root = module_path.parent
    if module_path.name != "catalog_runtime.py" or tools_root.name != "TOOLS":
        raise CatalogBindingError(
            "catalog runtime module is not loaded from a flattened runtime package"
        )
    return tools_root.parent


def _read_runtime_package_scalar(lines: Sequence[str], key: str) -> str:
    prefix = f"{key}:"
    values = [line[len(prefix) :].strip() for line in lines if line.startswith(prefix)]
    if len(values) != 1 or not values[0]:
        raise CatalogBindingError(
            f"RUNTIME_PACKAGE {key} field is missing or ambiguous"
        )
    value = values[0]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def _read_runtime_package_section_scalar(
    lines: Sequence[str], section: str, key: str
) -> str:
    section_indexes = [
        index for index, line in enumerate(lines) if line == f"{section}:"
    ]
    if len(section_indexes) != 1:
        raise CatalogBindingError(
            f"RUNTIME_PACKAGE {section} section is missing or ambiguous"
        )
    values: list[str] = []
    for line in lines[section_indexes[0] + 1 :]:
        if line and not line[0].isspace():
            break
        if line.startswith(f"  {key}:") and not line.startswith("   "):
            values.append(line[len(key) + 3 :].strip())
    if len(values) != 1 or not values[0]:
        raise CatalogBindingError(
            f"RUNTIME_PACKAGE {section}.{key} field is missing or ambiguous"
        )
    value = values[0]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def _validate_compiler_contracts_package_root(
    runtime_root: Path,
) -> tuple[Path, Mapping[str, object], Mapping[str, object], bytes, str]:
    """Validate one package root without issuing a runtime source capability.

    This pure validator is also used by the DEV release builder on an extracted
    candidate root. Its return value is reconstruction data only and never carries
    the module-owned source-issuance seal.
    """
    package_root = Path(runtime_root).resolve()
    package_lines = _runtime_package_lines(package_root)
    engine_marker = package_root / "ENGINE_VERSION.yaml"
    if not engine_marker.is_file() or engine_marker.is_symlink():
        raise CatalogBindingError("selected runtime engine marker is unavailable")
    try:
        engine_lines = tuple(engine_marker.read_text(encoding="utf-8").splitlines())
    except (OSError, UnicodeDecodeError) as exc:
        raise CatalogBindingError("selected runtime engine marker is unreadable") from exc
    manifest_engine_version = _require_nonempty_string(
        _read_runtime_package_scalar(engine_lines, "engine_version"),
        "ENGINE_VERSION.engine_version",
    )
    if _read_runtime_package_scalar(package_lines, "schema_version") != "4":
        raise CatalogBindingError(
            "runtime package does not bind the compiler projection"
        )
    expected_projection_sha256 = _require_sha256(
        _read_runtime_package_scalar(
            package_lines, "activity_compiler_contracts_sha256"
        ),
        "activity_compiler_contracts_sha256",
    )
    tools_root = package_root / "TOOLS"
    projection_path = tools_root / "activity_compiler_contracts.json"
    if (
        not package_root.is_dir()
        or not tools_root.is_dir()
        or tools_root.is_symlink()
        or not projection_path.is_file()
        or projection_path.is_symlink()
        or package_root not in projection_path.resolve().parents
    ):
        raise CatalogBindingError("installed compiler projection is unavailable")
    raw_projection = projection_path.read_bytes()
    actual_projection_sha256 = sha256(raw_projection)
    if actual_projection_sha256 != expected_projection_sha256:
        raise CatalogBindingError("installed compiler projection digest mismatch")
    try:
        projection = load_json_bytes(
            raw_projection, failure_reason="unreconstructable_context"
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"installed compiler projection is invalid: {exc.detail}"
        ) from exc
    if canonical_json(projection) + b"\n" != raw_projection:
        raise CatalogBindingError("installed compiler projection is not canonical JSON")

    projection = _require_exact_keys(
        projection,
        {"schema_version", "source_identity", "families"},
        "activity compiler projection",
    )
    if (
        type(projection["schema_version"]) is not int
        or projection["schema_version"] != 1
    ):
        raise CatalogBindingError("unsupported Activity compiler projection schema")
    identity = _require_exact_keys(
        projection["source_identity"],
        {
            "inventory_schema_version",
            "engine_version",
            "ruleset_set_digest_generation",
            "ruleset_set_sha256",
            "inventory_sha256",
            "families",
        },
        "activity compiler source identity",
    )
    engine_version = _require_nonempty_string(
        identity["engine_version"], "engine_version"
    )
    if (
        _read_runtime_package_scalar(package_lines, "engine_version") != engine_version
        or manifest_engine_version != engine_version
    ):
        raise CatalogBindingError(
            "runtime engine manifests differ from compiler source"
        )
    ruleset_set_digest_generation = _require_revision(
        identity["ruleset_set_digest_generation"], "ruleset_set_digest_generation"
    )
    ruleset_set_sha256 = _require_sha256(
        identity["ruleset_set_sha256"], "ruleset_set_sha256"
    )
    if ruleset_set_digest_generation != RULESET_SET_DIGEST_GENERATION:
        raise CatalogBindingError(
            "compiler projection has an unsupported ruleset digest generation"
        )
    if (
        type(identity["inventory_schema_version"]) is not int
        or identity["inventory_schema_version"] != 2
    ):
        raise CatalogBindingError(
            "compiler projection inventory schema version is invalid"
        )
    raw_family_identities = identity["families"]
    if not isinstance(raw_family_identities, Sequence) or isinstance(
        raw_family_identities, (str, bytes)
    ):
        raise CatalogBindingError("compiler source families must be an array")
    source_items: list[dict[str, str]] = []
    seen_families: set[str] = set()
    for raw_family in raw_family_identities:
        family_identity = _require_exact_keys(
            raw_family,
            {"family", "contract_id", "source_semantic_sha256"},
            "compiler source family identity",
        )
        family = _require_nonempty_string(family_identity["family"], "source family")
        if family in seen_families:
            raise CatalogBindingError("compiler source family identity is ambiguous")
        seen_families.add(family)
        if family_identity["contract_id"] != f"engine_contract.{family}.v1":
            raise CatalogBindingError("compiler source family contract ID is invalid")
        source_items.append(
            {
                "family": family,
                "contract_id": str(family_identity["contract_id"]),
                "semantic_sha256": _require_sha256(
                    family_identity["source_semantic_sha256"],
                    "source family semantic hash",
                ),
            }
        )
    if seen_families != REQUIRED_ENGINE_CONTRACT_FAMILIES:
        raise CatalogBindingError(
            "compiler source family set is incomplete or ambiguous"
        )
    inventory_core: dict[str, object] = {
        "inventory_schema_version": 2,
        "engine_version": engine_version,
        "ruleset_set_digest_generation": ruleset_set_digest_generation,
        "ruleset_set_sha256": ruleset_set_sha256,
        "items": source_items,
    }
    inventory_sha256 = sha256(INVENTORY_DOMAIN + canonical_json(inventory_core))
    if identity["inventory_sha256"] != inventory_sha256:
        raise CatalogBindingError(
            "compiler projection does not reconstruct inventory schema 2"
        )
    inventory = {**inventory_core, "inventory_sha256": inventory_sha256}
    if (
        _read_runtime_package_scalar(package_lines, "engine_version") != engine_version
        or _read_runtime_package_scalar(package_lines, "ruleset_set_digest_generation")
        != str(ruleset_set_digest_generation)
        or _read_runtime_package_scalar(package_lines, "ruleset_set_sha256")
        != ruleset_set_sha256
    ):
        raise CatalogBindingError(
            "RUNTIME_PACKAGE identity differs from compiler source"
        )
    if (
        _read_runtime_package_section_scalar(
            package_lines,
            "ruleset_engine_contract_inventory",
            "inventory_sha256",
        )
        != inventory_sha256
    ):
        raise CatalogBindingError(
            "RUNTIME_PACKAGE inventory digest differs from compiler source"
        )
    if (
        _read_runtime_package_section_scalar(
            package_lines,
            "ruleset_conformance_attestation",
            "engine_contract_inventory_sha256",
        )
        != inventory_sha256
    ):
        raise CatalogBindingError(
            "RUNTIME_PACKAGE attestation differs from compiler source"
        )
    try:
        _validated_engine_contract_entries(
            inventory,
            engine_version=engine_version,
            ruleset_set_sha256=ruleset_set_sha256,
            ruleset_set_digest_generation=ruleset_set_digest_generation,
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"compiler source inventory is invalid: {exc.detail}"
        ) from exc
    expected_families = [
        {
            "family": item["family"],
            "contract_id": item["contract_id"],
            "source_semantic_sha256": item["semantic_sha256"],
        }
        for item in inventory["items"]
    ]
    if identity != {
        "inventory_schema_version": 2,
        "engine_version": engine_version,
        "ruleset_set_digest_generation": ruleset_set_digest_generation,
        "ruleset_set_sha256": ruleset_set_sha256,
        "inventory_sha256": inventory["inventory_sha256"],
        "families": expected_families,
    }:
        raise CatalogBindingError(
            "compiler projection source identity differs from package inventory"
        )
    projected_families = _require_mapping(
        projection["families"], "activity compiler family projection"
    )
    if set(projected_families) != REQUIRED_ENGINE_CONTRACT_FAMILIES or any(
        not isinstance(projected_families[family], Mapping)
        for family in REQUIRED_ENGINE_CONTRACT_FAMILIES
    ):
        raise CatalogBindingError(
            "compiler projection family set is incomplete or ambiguous"
        )
    if _contains_dev_path(projection):
        raise CatalogBindingError(
            "compiler projection contains a development source path"
        )

    frozen_inventory = _freeze(inventory)
    frozen_projection = _freeze(projection)
    if not isinstance(frozen_inventory, Mapping) or not isinstance(
        frozen_projection, Mapping
    ):
        raise CatalogBindingError("compiler source freezing changed its mapping shape")
    return (
        package_root,
        frozen_inventory,
        frozen_projection,
        raw_projection,
        actual_projection_sha256,
    )


def validate_activity_compiler_contracts_package_root(
    runtime_root: Path,
) -> Mapping[str, object]:
    """Validate a candidate package root without issuing a runtime capability."""
    _root, inventory, _projection, _projection_bytes, _projection_sha256 = (
        _validate_compiler_contracts_package_root(runtime_root)
    )
    return _thaw(inventory)


def _validate_compiler_package_snapshot_origins(
    source: ActivityCompilerContractSource,
    package_snapshots: Mapping[str, PackageSnapshot],
    basis: Mapping[str, object],
) -> None:
    lock = _require_mapping(basis.get("ruleset_lock"), "ruleset lock")
    packages = lock.get("packages")
    if not isinstance(packages, Sequence) or isinstance(packages, (str, bytes)):
        raise CatalogBindingError("resolved packages must be an array")
    expected_ids = {
        _require_id(_require_mapping(row, "resolved package").get("package_id"), "package_id")
        for row in packages
    }
    if set(package_snapshots) != expected_ids:
        raise CatalogBindingError(
            "compiler source package snapshots differ from the exact lock"
        )
    package_root = source.runtime_root
    rules_root = package_root / "RULES"
    packages_root = rules_root / "packages"
    if (
        package_root != _current_runtime_package_root()
        or rules_root.is_symlink()
        or packages_root.is_symlink()
        or not packages_root.is_dir()
    ):
        raise CatalogBindingError(
            "compiler source package root differs from the selected runtime"
        )
    for package_id, snapshot in package_snapshots.items():
        if not isinstance(snapshot, PackageSnapshot):
            raise CatalogBindingError("compiler source package snapshot is invalid")
        expected_path = packages_root / package_id
        actual_path = Path(snapshot.package_dir)
        if (
            expected_path.is_symlink()
            or actual_path.is_symlink()
            or actual_path != expected_path
            or not expected_path.is_dir()
        ):
            raise CatalogBindingError(
                f"package snapshot {package_id} does not originate in the selected runtime"
            )


def load_activity_compiler_contract_source() -> ActivityCompilerContractSource:
    """Issue compiler contracts only from the package containing this module.

    The selected runtime root is the executing module's package root. A caller
    cannot nominate another directory, adjacent marker or projection as an
    issuer. Candidate-root validation for release tooling returns no authority.
    """
    (
        package_root,
        inventory,
        projection,
        projection_bytes,
        projection_sha256,
    ) = _validate_compiler_contracts_package_root(_current_runtime_package_root())
    source = ActivityCompilerContractSource(
        runtime_root=package_root,
        engine_contract_inventory=inventory,
        compiler_contracts=projection,
        compiler_contracts_bytes=projection_bytes,
        compiler_contracts_sha256=projection_sha256,
        _source_seal=_COMPILER_CONTRACT_SOURCE_SEAL,
    )
    _remember_compiler_source(source)
    if not source._is_admitted():
        raise CatalogBindingError("installed compiler source issuance failed")
    return source


def _normalize_frontier(value: object, label: str) -> dict[str, object]:
    frontier = _require_exact_keys(
        value, {"frontier_id", "state_revision", "definition_ids"}, label
    )
    definition_ids = frontier["definition_ids"]
    if not isinstance(definition_ids, Sequence) or isinstance(definition_ids, str):
        raise CatalogBindingError(f"{label}.definition_ids must be an array")
    normalized_ids = [
        _require_id(item, f"{label}.definition_id") for item in definition_ids
    ]
    if len(normalized_ids) != len(set(normalized_ids)):
        raise CatalogBindingError(f"{label}.definition_ids are ambiguous")
    return {
        "frontier_id": _require_id(frontier["frontier_id"], f"{label}.frontier_id"),
        "state_revision": _require_revision(
            frontier["state_revision"], f"{label}.state_revision"
        ),
        "definition_ids": sorted(normalized_ids),
    }


def _normalize_basis(value: object) -> dict[str, object]:
    basis = _require_exact_keys(
        value,
        {
            "catalog_generation",
            "engine_version",
            "engine_contract_inventory_sha256",
            "engine_contract_inventory",
            "ruleset_lock",
            "campaign_definition_frontier",
            "natural_owner_evidence",
        },
        "catalog context basis",
        optional={"session_overlay_frontier"},
    )
    catalog_generation = _require_revision(
        basis["catalog_generation"], "catalog_generation"
    )
    if catalog_generation < 1:
        raise CatalogBindingError("catalog_generation must be positive")
    lock = copy.deepcopy(_require_mapping(basis["ruleset_lock"], "ruleset_lock"))
    try:
        validated_lock = validate_resolved_lock(lock)
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"ruleset_lock is not reconstructive: {exc.detail}"
        ) from exc
    if validated_lock["ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION:
        raise CatalogBindingError("unsupported ruleset set digest generation")
    package_ids: set[str] = set()
    for package in validated_lock["packages"]:
        package_id = package["package_id"]
        if package_id in package_ids:
            raise CatalogBindingError("ruleset_lock package identities are ambiguous")
        package_ids.add(package_id)
        if package["catalog_generation"] != catalog_generation:
            raise CatalogBindingError("ruleset_lock has a mixed catalog generation")
    engine_version = _require_nonempty_string(basis["engine_version"], "engine_version")
    inventory = copy.deepcopy(
        _require_mapping(
            basis["engine_contract_inventory"], "engine_contract_inventory"
        )
    )
    inventory_sha256 = _require_sha256(
        basis["engine_contract_inventory_sha256"], "engine_contract_inventory_sha256"
    )
    if inventory.get("inventory_sha256") != inventory_sha256:
        raise CatalogBindingError(
            "engine contract inventory digest does not match its basis"
        )
    try:
        _validated_engine_contract_entries(
            inventory,
            engine_version=engine_version,
            ruleset_set_sha256=validated_lock["ruleset_set_sha256"],
            ruleset_set_digest_generation=validated_lock[
                "ruleset_set_digest_generation"
            ],
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"engine contract inventory is not admitted evidence: {exc.detail}"
        ) from exc
    normalized: dict[str, object] = {
        "catalog_generation": catalog_generation,
        "engine_version": engine_version,
        "engine_contract_inventory_sha256": inventory_sha256,
        "engine_contract_inventory": inventory,
        "ruleset_lock": validated_lock,
        "campaign_definition_frontier": _normalize_frontier(
            basis["campaign_definition_frontier"], "campaign_definition_frontier"
        ),
        "natural_owner_evidence": _normalize_natural_owner_evidence(
            basis["natural_owner_evidence"]
        ),
    }
    if "session_overlay_frontier" in basis:
        normalized["session_overlay_frontier"] = _normalize_frontier(
            basis["session_overlay_frontier"], "session_overlay_frontier"
        )
    return normalized


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CatalogBindingError(f"{label} must be a nonempty string")
    return value


def _require_route(value: object, label: str) -> str:
    route = _require_nonempty_string(value, label)
    components = route.split("/")
    if any(
        not component or component.casefold() == "latest" for component in components
    ):
        raise CatalogBindingError(
            f"{label} must be an exact route, not an ambient/latest selector"
        )
    return route


def _require_canonical_natural_owner_route(
    value: object, *, owner_domain: str, definition_id: str
) -> str:
    route = _require_route(value, "natural owner route")
    expected = f"{_NATURAL_OWNER_ROUTE_PREFIXES[owner_domain]}{definition_id}.json"
    if route != expected:
        raise CatalogBindingError("natural owner route is not canonical")
    return route


def _normalize_natural_owner_evidence(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise CatalogBindingError("natural_owner_evidence must be an array")
    evidence_rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for raw_row in value:
        row = _require_exact_keys(
            raw_row,
            {
                "definition_id",
                "kind",
                "owner_domain",
                "scope",
                "route",
                "pinned_revision",
                "content_sha256",
            },
            "natural owner evidence",
        )
        definition_id = _require_id(row["definition_id"], "natural owner definition_id")
        owner_domain = _require_nonempty_string(row["owner_domain"], "owner_domain")
        scope = _require_nonempty_string(row["scope"], "scope")
        if _NATURAL_OWNER_SCOPES.get(owner_domain) != scope:
            raise CatalogBindingError("natural owner domain and scope do not match")
        if definition_id in seen_ids:
            raise CatalogBindingError("natural owner evidence is ambiguous")
        seen_ids.add(definition_id)
        evidence_rows.append(
            {
                "definition_id": definition_id,
                "kind": _require_id(row["kind"], "natural owner kind"),
                "owner_domain": owner_domain,
                "scope": scope,
                "route": _require_canonical_natural_owner_route(
                    row["route"], owner_domain=owner_domain, definition_id=definition_id
                ),
                "pinned_revision": _require_revision(
                    row["pinned_revision"], "natural owner pinned_revision"
                ),
                "content_sha256": _require_sha256(
                    row["content_sha256"], "natural owner content_sha256"
                ),
            }
        )
    return tuple(sorted(evidence_rows, key=lambda row: str(row["definition_id"])))


def _validate_admitted_source_evidence(
    basis: Mapping[str, object],
    *,
    engine_contract_inventory_source: object,
    natural_owner_sources: object,
) -> None:
    source_inventory = copy.deepcopy(
        _require_mapping(
            engine_contract_inventory_source, "engine contract inventory source"
        )
    )
    try:
        _validated_engine_contract_entries(
            source_inventory,
            engine_version=str(basis["engine_version"]),
            ruleset_set_sha256=str(basis["ruleset_lock"]["ruleset_set_sha256"]),
            ruleset_set_digest_generation=int(
                basis["ruleset_lock"]["ruleset_set_digest_generation"]
            ),
        )
    except (RulesetContractError, KeyError, TypeError, ValueError) as exc:
        detail = exc.detail if isinstance(exc, RulesetContractError) else str(exc)
        raise CatalogBindingError(
            f"engine contract inventory source is not admitted evidence: {detail}"
        ) from exc
    if source_inventory != basis["engine_contract_inventory"]:
        raise CatalogBindingError(
            "engine contract inventory differs from admitted source evidence"
        )

    sources = _require_mapping(natural_owner_sources, "natural owner sources")
    evidence_by_domain = {
        owner_domain: tuple(
            row
            for row in basis["natural_owner_evidence"]
            if row["owner_domain"] == owner_domain
        )
        for owner_domain in _NATURAL_OWNER_SCOPES
    }
    expected_domains = {
        owner_domain for owner_domain, rows in evidence_by_domain.items() if rows
    }
    if set(sources) != expected_domains:
        raise CatalogBindingError(
            "natural owner sources do not match admitted owner domains"
        )
    for owner_domain in sorted(expected_domains):
        source = _require_exact_keys(
            sources[owner_domain],
            {"selected_frontier", "members", "immutable_member_bytes"},
            "natural owner source",
        )
        frontier_key = (
            "campaign_definition_frontier"
            if owner_domain == "campaign"
            else "session_overlay_frontier"
        )
        if frontier_key not in basis:
            raise CatalogBindingError(
                "natural owner source has no selected context frontier"
            )
        selected_frontier = _normalize_frontier(
            source["selected_frontier"], f"{owner_domain} source selected_frontier"
        )
        if selected_frontier != basis[frontier_key]:
            raise CatalogBindingError(
                "natural owner selected frontier differs from context basis"
            )
        admitted_members = _normalize_natural_owner_evidence(source["members"])
        if any(row["owner_domain"] != owner_domain for row in admitted_members):
            raise CatalogBindingError(
                "natural owner source member has the wrong domain"
            )
        if admitted_members != evidence_by_domain[owner_domain]:
            raise CatalogBindingError(
                "natural owner evidence differs from admitted source membership"
            )
        if not {str(row["definition_id"]) for row in admitted_members}.issubset(
            set(selected_frontier["definition_ids"])
        ):
            raise CatalogBindingError(
                "natural owner member is absent from its selected frontier"
            )
        immutable_member_bytes = _require_mapping(
            source["immutable_member_bytes"], "natural owner immutable member bytes"
        )
        expected_routes = {str(row["route"]) for row in admitted_members}
        if set(immutable_member_bytes) != expected_routes:
            raise CatalogBindingError(
                "natural owner immutable member bytes are incomplete"
            )
        for row in admitted_members:
            raw_content = immutable_member_bytes[row["route"]]
            if not isinstance(raw_content, bytes):
                raise CatalogBindingError(
                    "natural owner immutable member content must be bytes"
                )
            if sha256(raw_content) != row["content_sha256"]:
                raise CatalogBindingError(
                    "natural owner content digest differs from immutable owner bytes"
                )


def _rebuild_definition_sources(
    basis: Mapping[str, object], package_snapshots: Mapping[str, PackageSnapshot]
) -> dict[str, dict[str, str]]:
    packages = {row["package_id"]: row for row in basis["ruleset_lock"]["packages"]}
    if set(package_snapshots) != set(packages):
        raise CatalogBindingError(
            "package snapshot evidence is incomplete or ambiguous"
        )
    source_dirs = []
    for snapshot in package_snapshots.values():
        if not isinstance(snapshot, PackageSnapshot):
            raise CatalogBindingError("package snapshot evidence has an invalid source")
        source_dirs.append(snapshot.package_dir)
    try:
        rebuilt_lock, rebuilt_snapshots = build_resolved_lock(
            source_dirs,
            root_package_ids=basis["ruleset_lock"]["root_package_ids"],
            engine_version=basis["engine_version"],
            catalog_generation=basis["catalog_generation"],
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"package snapshot source cannot rebuild an admitted lock: {exc.detail}"
        ) from exc
    if rebuilt_lock != basis["ruleset_lock"]:
        raise CatalogBindingError("rebuilt admitted lock does not match ruleset_lock")

    definitions: dict[str, dict[str, str]] = {}
    for package_id, rebuilt in rebuilt_snapshots.items():
        lock_package = packages[package_id]
        for entry_key, entry in rebuilt.semantic_entries.items():
            _prefix, marker, definition_id = entry_key.rpartition("|id:")
            kind = entry.get("kind")
            if (
                not marker
                or not isinstance(kind, str)
                or not kind.startswith("definition.")
            ):
                continue
            namespace = f"{definition_id.partition('.')[0]}.*"
            if namespace not in lock_package["owned_namespaces"]:
                raise CatalogBindingError(
                    "source definition is outside its package namespace"
                )
            if definition_id in definitions:
                raise CatalogBindingError("cross-source definition collision")
            definitions[definition_id] = {
                "package_id": package_id,
                "kind": kind,
                "package_content_sha256": rebuilt.content_sha256,
                "semantic_sha256": entry["semantic_sha256"],
            }
    return definitions


def _normalize_dependencies(
    value: object,
    basis: Mapping[str, object],
    package_snapshots: Mapping[str, PackageSnapshot],
    natural_owner_sources: object,
) -> tuple[tuple[dict[str, str], ...], dict[str, str]]:
    if not isinstance(value, Sequence) or isinstance(value, str) or not value:
        raise CatalogBindingError("definition_dependencies must be a nonempty array")
    source_definitions = _rebuild_definition_sources(basis, package_snapshots)
    natural_evidence = {
        str(row["definition_id"]): row for row in basis["natural_owner_evidence"]
    }
    dependencies: list[dict[str, object]] = []
    semantic_hashes: dict[str, str] = {}
    seen_ids: set[str] = set()
    for value_row in value:
        row = _require_mapping(value_row, "catalog definition dependency")
        source_type = _require_nonempty_string(
            row.get("source_type"), "dependency source_type"
        )
        if source_type == "ruleset_package":
            row = _require_exact_keys(
                row,
                {
                    "source_type",
                    "definition_id",
                    "kind",
                    "package_id",
                    "package_content_sha256",
                },
                "ruleset package definition dependency",
            )
            definition_id = _require_id(row["definition_id"], "definition_id")
            kind = _require_id(row["kind"], "kind")
            if definition_id in seen_ids:
                raise CatalogBindingError(
                    "definition_dependencies contain duplicate definition_id"
                )
            package_id = _require_id(row["package_id"], "package_id")
            content_sha256 = _require_sha256(
                row["package_content_sha256"], "package_content_sha256"
            )
            source_definition = source_definitions.get(definition_id)
            if source_definition is None:
                raise CatalogBindingError(
                    "definition dependency is absent from rebuilt source evidence"
                )
            if (
                source_definition["package_id"] != package_id
                or source_definition["package_content_sha256"] != content_sha256
            ):
                raise CatalogBindingError(
                    "definition dependency source does not match rebuilt evidence"
                )
            if source_definition["kind"] != kind:
                raise CatalogBindingError(
                    "definition dependency kind differs from rebuilt evidence"
                )
            semantic_hashes[definition_id] = source_definition["semantic_sha256"]
            normalized_dependency: dict[str, object] = {
                "source_type": source_type,
                "definition_id": definition_id,
                "kind": kind,
                "package_id": package_id,
                "package_content_sha256": content_sha256,
            }
        elif source_type == "natural_owner":
            row = _require_exact_keys(
                row,
                {
                    "source_type",
                    "definition_id",
                    "kind",
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                    "evidence_sha256",
                },
                "natural owner definition dependency",
            )
            definition_id = _require_id(row["definition_id"], "definition_id")
            kind = _require_id(row["kind"], "kind")
            if definition_id in seen_ids:
                raise CatalogBindingError(
                    "definition_dependencies contain duplicate definition_id"
                )
            if definition_id in source_definitions:
                raise CatalogBindingError(
                    "natural owner definition collides with a package definition"
                )
            evidence = natural_evidence.get(definition_id)
            if evidence is None:
                raise CatalogBindingError("natural owner evidence is missing")
            expected = {
                key: evidence[key]
                for key in (
                    "definition_id",
                    "kind",
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                )
            }
            actual = {key: row[key] for key in expected}
            if actual != expected:
                raise CatalogBindingError(
                    "natural owner dependency does not match pinned evidence"
                )
            evidence_sha256 = _require_sha256(row["evidence_sha256"], "evidence_sha256")
            if evidence_sha256 != sha256(
                NATURAL_OWNER_EVIDENCE_DOMAIN + canonical_json(evidence)
            ):
                raise CatalogBindingError("natural owner evidence digest mismatch")
            normalized_dependency = {
                "source_type": source_type,
                **expected,
                "evidence_sha256": evidence_sha256,
            }
            owner_sources = _require_mapping(
                natural_owner_sources, "natural owner sources"
            )
            owner_source = _require_mapping(
                owner_sources.get(str(expected["owner_domain"])),
                "natural owner source",
            )
            immutable_member_bytes = _require_mapping(
                owner_source["immutable_member_bytes"],
                "natural owner immutable member bytes",
            )
            raw_definition = immutable_member_bytes.get(str(expected["route"]))
            if isinstance(raw_definition, bytes):
                try:
                    definition_value = load_json_bytes(raw_definition)
                except RulesetContractError:
                    definition_value = None
                if (
                    isinstance(definition_value, Mapping)
                    and definition_value.get("id") == definition_id
                    and definition_value.get("kind") == kind
                    and isinstance(definition_value.get("data"), Mapping)
                ):
                    rows = semantic_entries(
                        str(expected["owner_domain"]),
                        "natural-owner-definitions.json",
                        {"definitions": [dict(definition_value)]},
                    )
                    semantic_hashes[definition_id] = next(iter(rows.values()))[
                        "semantic_sha256"
                    ]
        else:
            raise CatalogBindingError("unsupported dependency source_type")
        seen_ids.add(definition_id)
        dependencies.append(normalized_dependency)
    return (
        tuple(sorted(dependencies, key=lambda row: row["definition_id"])),
        semantic_hashes,
    )


def bind_catalog_context(
    value: object,
    *,
    package_snapshots: Mapping[str, PackageSnapshot],
    engine_contract_inventory_source: object,
    natural_owner_sources: object,
) -> BoundCatalogContext:
    """Bind exact reconstruction inputs; this function never chooses a default."""

    request = _require_exact_keys(
        value, {"basis", "definition_dependencies"}, "catalog binding request"
    )
    basis = _normalize_basis(request["basis"])
    compiler_source: ActivityCompilerContractSource | None = None
    inventory_source = engine_contract_inventory_source
    if isinstance(engine_contract_inventory_source, ActivityCompilerContractSource):
        if type(engine_contract_inventory_source) is not ActivityCompilerContractSource or not engine_contract_inventory_source._is_admitted():
            raise CatalogBindingError(
                "compiler contract source is not package-authenticated"
            )
        compiler_source = engine_contract_inventory_source
        _validate_compiler_package_snapshot_origins(
            compiler_source, package_snapshots, basis
        )
        inventory_source = _thaw(compiler_source.engine_contract_inventory)
    _validate_admitted_source_evidence(
        basis,
        engine_contract_inventory_source=inventory_source,
        natural_owner_sources=natural_owner_sources,
    )
    dependencies, semantic_hashes = _normalize_dependencies(
        request["definition_dependencies"],
        basis,
        package_snapshots,
        natural_owner_sources,
    )
    fingerprint_payload = {
        "basis": basis,
        "definition_dependencies": list(dependencies),
    }
    fingerprint = sha256(CATALOG_CONTEXT_DOMAIN + canonical_json(fingerprint_payload))
    frozen_basis = _freeze(basis)
    frozen_dependencies = _freeze(dependencies)
    frozen_semantic_hashes = _freeze(semantic_hashes)
    if (
        not isinstance(frozen_basis, Mapping)
        or not isinstance(frozen_dependencies, tuple)
        or not isinstance(frozen_semantic_hashes, Mapping)
    ):
        raise CatalogBindingError(
            "catalog context freezing changed the expected carrier shape"
        )
    context = BoundCatalogContext(
        frozen_basis,
        frozen_dependencies,
        fingerprint,
        _ADMITTED_CONTEXT_SEAL,
        compiler_source,
        frozen_semantic_hashes,
    )
    _remember_bound_catalog_context(context)
    return context


def _candidate(value: object) -> tuple[str, str]:
    candidate = _require_exact_keys(value, {"definition_id", "kind"}, "candidate")
    return (
        _require_id(candidate["definition_id"], "candidate definition_id"),
        _require_id(candidate["kind"], "candidate kind"),
    )


def _find_dependency(
    context: BoundCatalogContext, definition_id: str
) -> Mapping[str, object] | None:
    return next(
        (
            row
            for row in context.definition_dependencies
            if row["definition_id"] == definition_id
        ),
        None,
    )


def bind_interpreter_candidate(
    context: BoundCatalogContext, candidate: object
) -> dict[str, object]:
    """Pin one exact interpreter candidate to its already-bound catalog context."""

    definition_id, kind = _candidate(candidate)
    dependency = _find_dependency(context, definition_id)
    if dependency is None:
        raise CatalogBindingError("definition_not_found")
    if dependency["kind"] != kind:
        raise CatalogBindingError("definition_kind_mismatch")
    lock = context.basis["ruleset_lock"]
    binding: dict[str, object] = {
        "definition_id": definition_id,
        "kind": kind,
        "source_type": dependency["source_type"],
        "catalog_generation": context.basis["catalog_generation"],
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
        "catalog_context_fingerprint": context.fingerprint,
    }
    if dependency["source_type"] == "ruleset_package":
        binding.update(
            {
                "source_package_id": dependency["package_id"],
                "source_package_content_sha256": dependency["package_content_sha256"],
            }
        )
    else:
        binding.update(
            {
                key: dependency[key]
                for key in (
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                    "evidence_sha256",
                )
            }
        )
    return binding


def validate_executable_binding(context: BoundCatalogContext, binding: object) -> None:
    """Reject bindings that were selected under another or forged context."""

    raw_binding = _require_mapping(binding, "executable binding")
    source_type = _require_nonempty_string(
        raw_binding.get("source_type"), "source_type"
    )
    common_fields = {
        "definition_id",
        "kind",
        "source_type",
        "catalog_generation",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
    }
    if source_type == "ruleset_package":
        value = _require_exact_keys(
            raw_binding,
            common_fields | {"source_package_id", "source_package_content_sha256"},
            "ruleset package executable binding",
        )
    elif source_type == "natural_owner":
        value = _require_exact_keys(
            raw_binding,
            common_fields
            | {"owner_domain", "scope", "route", "pinned_revision", "evidence_sha256"},
            "natural owner executable binding",
        )
    else:
        raise CatalogBindingError("unsupported binding source_type")
    if (
        value["catalog_context_fingerprint_generation"]
        != CATALOG_CONTEXT_FINGERPRINT_GENERATION
        or value["catalog_context_fingerprint"] != context.fingerprint
    ):
        raise CatalogBindingError("stale catalog context")
    lock = context.basis["ruleset_lock"]
    if (
        value["catalog_generation"] != context.basis["catalog_generation"]
        or value["ruleset_set_digest_generation"]
        != lock["ruleset_set_digest_generation"]
        or value["ruleset_set_sha256"] != lock["ruleset_set_sha256"]
    ):
        raise CatalogBindingError("stale catalog context")
    definition_id, kind = _candidate(
        {"definition_id": value["definition_id"], "kind": value["kind"]}
    )
    dependency = _find_dependency(context, definition_id)
    if dependency is None or dependency["kind"] != kind:
        raise CatalogBindingError("binding definition is no longer pinned")
    if value["source_type"] != dependency["source_type"]:
        raise CatalogBindingError("binding source does not match the pinned definition")
    if value["source_type"] == "ruleset_package":
        source_fields = ("package_id", "package_content_sha256")
        binding_fields = ("source_package_id", "source_package_content_sha256")
    else:
        source_fields = (
            "owner_domain",
            "scope",
            "route",
            "pinned_revision",
            "evidence_sha256",
        )
        binding_fields = source_fields
    if any(
        value[binding_key] != dependency[source_key]
        for binding_key, source_key in zip(binding_fields, source_fields, strict=True)
    ):
        raise CatalogBindingError("binding source does not match the pinned definition")


def bind_executable_catalog(
    context: BoundCatalogContext, candidate: object
) -> dict[str, object]:
    """Return either an exact executable binding or typed unsupported-gap evidence."""

    try:
        return {
            "status": "bound",
            "binding": bind_interpreter_candidate(context, candidate),
        }
    except CatalogBindingError as exc:
        if str(exc) not in {"definition_not_found", "definition_kind_mismatch"}:
            raise
        definition_id, kind = _candidate(candidate)
        lock = context.basis["ruleset_lock"]
        return {
            "status": "gap",
            "gap_report": {
                "requested_identity": {"definition_id": definition_id, "kind": kind},
                "context_basis": _thaw(context.basis),
                "catalog_generation": context.basis["catalog_generation"],
                "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
                "ruleset_set_sha256": lock["ruleset_set_sha256"],
                "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
                "catalog_context_fingerprint": context.fingerprint,
                "reason": str(exc),
            },
        }
