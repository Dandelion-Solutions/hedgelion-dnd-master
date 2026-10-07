"""Source-bound cold Activity compilation and process-local lookup.

This module issues no native execution or mutation authority. It consumes the
existing sealed catalog binder, package byte identities and the installed
path-neutral compiler-contract projection. Only exact currently admitted source
consumers produce CompiledActivity values.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Final

from . import activity_contracts as contracts
from .catalog_runtime import (
    ActivityCompilerContractSource,
    BoundCatalogContext,
    CatalogBindingError,
    bind_catalog_context,
)
from .ruleset_package import (
    PACKAGE_DOMAIN,
    SEMANTIC_ENTRY_DIGEST_GENERATION,
    PackageSnapshot,
    RulesetContractError,
    canonical_json,
    load_json_bytes,
    sha256,
)
from .structural_contracts import StructuralContractError, validate_contract

# framework_module_version: 1.0.3
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.3"
_ID: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


class ActivityRuntimeError(ValueError):
    """Raised when a source Activity cannot be admitted or compiled exactly."""


class ActivityNotSelectable(ActivityRuntimeError):
    """Raised for structurally loaded content without an admitted compiler edge."""


@dataclass(frozen=True, slots=True)
class _PackageDefinition:
    package_id: str
    member_path: str
    record: Mapping[str, object]
    semantic_sha256: str


@dataclass(frozen=True, slots=True)
class _LoweredSteps:
    instructions: tuple[contracts.CompiledInstruction, ...]
    roles: Mapping[str, Mapping[str, object]]
    exports: Mapping[str, object]
    reads: tuple[str, ...]
    dependencies: tuple[str, ...]
    transitions: tuple[str, ...]
    symbols: Mapping[str, object]


def _validate_bound_definition_reference(
    value_kind: str, value: object, *, values: Mapping[str, object],
    source_definitions: Mapping[str, Mapping[str, object]], core: Mapping[str, object],
) -> None:
    contract = _mapping(values.get(value_kind), "value contract")
    registry = contract.get("catalog_ref")
    if not isinstance(registry, str) or not (registry == "content_definition_kinds" or registry.startswith("content_definition_kinds:")):
        return
    record = source_definitions.get(value) if isinstance(value, str) else None
    if not isinstance(record, Mapping):
        raise ActivityNotSelectable(f"unavailable source definition dependency: {value}")
    _, _, expected_kind = registry.partition(":")
    if expected_kind and expected_kind not in core["registries"]["content_definition_kinds"]:
        raise ActivityNotSelectable(f"unknown source definition-kind contract: {expected_kind}")
    if (expected_kind and record.get("kind") != expected_kind
        or not expected_kind and record.get("kind") not in core["registries"]["content_definition_kinds"]):
        raise ActivityRuntimeError(f"definition dependency has wrong kind for {value_kind}: {value}")


def _resolve_compiler_symbol(
    symbol_id: str, *, expected_kind: str, cardinality: str, occurrence_id: str,
    activity_id: str, declarations: Mapping[str, object], values: Mapping[str, object],
    mechanical: Mapping[str, object], core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
    reads: list[str], retained: dict[str, object],
    parameters: Mapping[str, object] = MappingProxyType({}),
    scopes: Mapping[str, object] = MappingProxyType({}),
    scope_name: str | None = None,
    source_definitions: Mapping[str, Mapping[str, object]] = MappingProxyType({}),
) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()
    pending = [(symbol_id, False)]
    while pending:
        current, leaving = pending.pop()
        if leaving:
            visiting.remove(current)
            visited.add(current)
            continue
        if current in visiting:
            raise ActivityRuntimeError(f"compiled producer dependency cycle: {current}")
        if current in visited:
            continue
        descriptor = declarations.get(current)
        if not isinstance(descriptor, Mapping):
            raise ActivityNotSelectable(f"compiled symbol has unavailable source producer contract: {current}")
        _validate_shape("https://hedgelion.invalid/schemas/activity-compiler-declaration.schema.json#/$defs/symbol", descriptor)
        if occurrence_id not in descriptor["permitted_occurrence_ids"]:
            raise ActivityNotSelectable(f"compiled producer is unauthorized for {occurrence_id}: {current}")
        scope_contract = descriptor.get("scope")
        if scope_contract is not None:
            actual_scope = scopes.get(scope_name)
            if (not isinstance(actual_scope, Mapping) or scope_contract["name"] != scope_name
                or actual_scope.get("value_kind") != scope_contract["value_kind"]
                or actual_scope.get("family_key") != scope_contract["family_key"]):
                raise ActivityRuntimeError(f"producer scope is unavailable or incompatible: {current}")
        elif current == symbol_id and scope_name is not None:
            raise ActivityRuntimeError(f"producer scope is unavailable or incompatible: {current}")
        kind = descriptor["value_kind"]
        if kind not in values:
            raise ActivityRuntimeError(f"compiled producer has unknown value kind: {current}")
        if current == symbol_id and (kind != expected_kind or descriptor["cardinality"] != cardinality):
            raise ActivityRuntimeError(f"compiled producer has wrong type/cardinality: {current}")
        if "template" in descriptor:
            is_half_damage = descriptor["template"]["kind"] == "HALF_DAMAGE_FLOOR_MIN_ZERO"
            expected_template_kind = "damage_components" if is_half_damage else "roll_request"
            if kind != expected_template_kind or descriptor["cardinality"] != "single":
                raise ActivityRuntimeError("compiler template has wrong result type/cardinality")
            if is_half_damage:
                dependency = descriptor["template"]["source_symbol"]
                if tuple(descriptor["dependencies"]) != (dependency,):
                    raise ActivityRuntimeError("half-damage template must retain its same full-result dependency")
                input_contract = declarations.get(dependency)
                if input_contract is not None and (input_contract.get("value_kind") != "damage_components" or input_contract.get("cardinality") != "single"):
                    raise ActivityRuntimeError("half-damage input producer has wrong type/cardinality")
            for parameter_key in ("ability_parameter", "proficiency_parameter"):
                parameter_name = descriptor["template"].get(parameter_key)
                if parameter_name is None:
                    continue
                parameter = parameters.get(parameter_name)
                if (not isinstance(parameter, Mapping) or parameter.get("source_class") != "ENGINE_BOUND"
                    or parameter.get("value_type") != "machine_id" or parameter.get("cardinality") != "single"):
                    raise ActivityRuntimeError(f"compiled producer lacks authoritative parameter contract: {parameter_name}")
            if descriptor["template"]["kind"] == "D10_FIXED_FAILED_CHECK":
                parameter = parameters.get(descriptor["template"]["original_dc_parameter"])
                if not isinstance(parameter, Mapping) or parameter != {"source_class": "ENGINE_BOUND", "value_type": "integer", "cardinality": "single", "required": True}:
                    raise ActivityRuntimeError("Tactical Mind original DC must be fixed from its accepted prior check")
        else:
            raw_values = descriptor["value"] if descriptor["cardinality"] == "many" else (descriptor["value"],)
            for value in _sequence(raw_values, "compiled producer values"):
                _validate_shape("typed_export_value", {"value_kind": kind, "value": value})
                _validate_bound_definition_reference(kind, value, values=values,
                    source_definitions=source_definitions, core=core)
        for reference in descriptor["reads"]:
            read_kind, read_id = reference.split(":", 1)
            if read_kind == "selector":
                _validate_selector_read(read_id, activity_id, mechanical=mechanical, core=core, ledger_rows=ledger_rows)
            elif read_kind == "fact":
                _validate_fact_read(read_id, activity_id, mechanical)
            else:
                _validate_accessor_read(read_id, activity_id, mechanical, ledger_rows)
            reads.append(reference)
        if current in retained and retained[current] != descriptor:
            raise ActivityRuntimeError(f"conflicting source producer contracts: {current}")
        retained[current] = descriptor
        visiting.add(current)
        pending.append((current, True))
        for dependency in reversed(descriptor["dependencies"]):
            if dependency in visiting:
                raise ActivityRuntimeError(f"compiled producer dependency cycle: {dependency}")
            pending.append((dependency, False))


def _validate_accessor_read(
    accessor_id: str, activity_id: str, mechanical: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
) -> None:
    accessor = _mapping(mechanical.get("accessors"), "accessors").get(accessor_id)
    admission = ledger_rows.get(("mechanical_accessors", accessor_id))
    if (not isinstance(accessor, Mapping) or accessor.get("disposition") != "ACTIVE_ADMITTED"
        or admission is None or admission.get("admission_disposition") != "ACTIVE_ADMITTED"
        or admission.get("realization_state") != "COMPLETE"
        or not _contains_id(accessor.get("permitted_consumer_ids"), activity_id)):
        raise ActivityRuntimeError(f"accessor is unknown, dormant, or unauthorized: {accessor_id}")


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ActivityRuntimeError(f"{label} must be an object")
    return value


def _sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ActivityRuntimeError(f"{label} must be an array")
    return value


def _require_id(value: object, label: str) -> str:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise ActivityRuntimeError(f"{label} must be a native identifier")
    return value


def _validate_shape(name: str, value: object) -> None:
    try:
        validate_contract(name, value)
    except StructuralContractError as exc:
        raise ActivityRuntimeError(f"{name} is not admitted: {exc}") from exc


def _package_member_path(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ActivityRuntimeError("package member path is invalid")
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != value:
        raise ActivityRuntimeError("package member path is not normalized")
    return value


def _definition_envelope(
    identity: str,
    kind: str,
    record: Mapping[str, object],
) -> dict[str, object]:
    if record.get("id") != identity or record.get("kind") != kind:
        raise ActivityRuntimeError(
            "source definition identity differs from its binding"
        )
    data = _mapping(record.get("data"), f"{identity}.data")
    name = record.get("name", {"en": identity})
    envelope = {"id": identity, "kind": kind, "name": name, "data": data}
    for qualifier in ("facets", "tags"):
        if qualifier in record:
            envelope[qualifier] = record[qualifier]
    _validate_shape("catalog-definition", envelope)
    return envelope


def _definition_graph(
    dependency_ids: set[str],
    source_records: Mapping[str, Mapping[str, object]],
) -> dict[str, tuple[str, ...]]:
    graph: dict[str, tuple[str, ...]] = {}
    for identity in dependency_ids:
        record = source_records[identity]
        raw_references = record.get("references", ())
        references = tuple(
            _require_id(item, f"{identity} reference")
            for item in _sequence(raw_references, f"{identity}.references")
        )
        if len(references) != len(set(references)):
            raise ActivityRuntimeError(
                f"{identity} has duplicate definition references"
            )
        missing = set(references) - dependency_ids
        if missing:
            raise ActivityRuntimeError(
                f"{identity} has unavailable transitive dependencies: {sorted(missing)}"
            )
        graph[identity] = references

    visited: set[str] = set()
    for identity in sorted(graph):
        if identity in visited:
            continue
        visiting: set[str] = set()
        stack: list[tuple[str, bool]] = [(identity, False)]
        while stack:
            current, leaving = stack.pop()
            if leaving:
                visiting.remove(current)
                visited.add(current)
                continue
            if current in visited:
                continue
            if current in visiting:
                raise ActivityRuntimeError(f"definition dependency cycle at {current}")
            visiting.add(current)
            stack.append((current, True))
            for dependency_id in reversed(graph[current]):
                if dependency_id in visiting:
                    raise ActivityRuntimeError(
                        f"definition dependency cycle at {dependency_id}"
                    )
                if dependency_id not in visited:
                    stack.append((dependency_id, False))
    return graph


def _contains_id(values: object, identity: str) -> bool:
    return isinstance(values, (list, tuple, set, frozenset)) and identity in values


def _package_member_bytes(
    context: BoundCatalogContext,
    package_snapshots: Mapping[str, PackageSnapshot],
) -> dict[tuple[str, str], bytes]:
    lock = _mapping(context.basis["ruleset_lock"], "ruleset lock")
    package_rows = _sequence(lock["packages"], "resolved packages")
    packages = {str(row["package_id"]): row for row in package_rows}
    if set(package_snapshots) != set(packages):
        raise ActivityRuntimeError(
            "package snapshots differ from admitted ruleset lock"
        )
    frozen: dict[tuple[str, str], bytes] = {}
    for package_id, raw_package in packages.items():
        package = _mapping(raw_package, "resolved package")
        snapshot = package_snapshots[package_id]
        if not isinstance(snapshot, PackageSnapshot):
            raise ActivityRuntimeError("package snapshot has an invalid source")
        package_root = Path(snapshot.package_dir).resolve()
        if not package_root.is_dir():
            raise ActivityRuntimeError("package source directory is unavailable")
        members = _sequence(package["members"], "resolved package member set")
        observed: list[dict[str, str]] = []
        for raw_member in members:
            member = _mapping(raw_member, "resolved package member")
            relative_path = _package_member_path(member.get("path"))
            target = package_root.joinpath(*PurePosixPath(relative_path).parts)
            resolved = target.resolve()
            if (
                not target.is_file()
                or target.is_symlink()
                or package_root not in resolved.parents
            ):
                raise ActivityRuntimeError(
                    "package member is unavailable or escapes its source"
                )
            raw = target.read_bytes()
            digest = sha256(raw)
            if digest != member.get("sha256"):
                raise ActivityRuntimeError(
                    "package member changed after source binding"
                )
            observed.append({"path": relative_path, "sha256": digest})
            frozen[(package_id, relative_path)] = raw
        content_sha256 = sha256(
            PACKAGE_DOMAIN + canonical_json({"content_files": observed})
        )
        if content_sha256 != package.get("content_sha256"):
            raise ActivityRuntimeError("frozen package bytes differ from admitted lock")
    return frozen


def _package_definition_records(
    frozen_members: Mapping[tuple[str, str], bytes],
    context: BoundCatalogContext,
) -> dict[str, _PackageDefinition]:
    selected_ids = {
        str(row["definition_id"])
        for row in context.definition_dependencies
        if row["source_type"] == "ruleset_package"
    }
    definitions: dict[str, _PackageDefinition] = {}
    for (package_id, member_path), raw in frozen_members.items():
        if (
            not member_path.endswith(".json")
            or member_path == "ruleset-package-manifest.json"
        ):
            continue
        try:
            payload = load_json_bytes(raw)
        except RulesetContractError as exc:
            raise ActivityRuntimeError(
                f"package member is not valid JSON: {member_path}"
            ) from exc
        if not isinstance(payload, Mapping):
            continue
        for raw_records in payload.values():
            if not isinstance(raw_records, (list, tuple)):
                continue
            for raw_record in raw_records:
                if not isinstance(raw_record, Mapping):
                    continue
                identity = raw_record.get("id")
                kind = raw_record.get("kind")
                if (
                    not isinstance(identity, str)
                    or not isinstance(kind, str)
                    or not kind.startswith("definition.")
                    or not isinstance(raw_record.get("data"), Mapping)
                    or identity not in selected_ids
                ):
                    continue
                if identity in definitions:
                    raise ActivityRuntimeError("package has duplicate definition IDs")
                semantic_hash = context._definition_semantic_hashes.get(identity)
                if semantic_hash is None:
                    raise ActivityRuntimeError(
                        f"definition {identity} has no exact package semantic identity"
                    )
                definitions[identity] = _PackageDefinition(
                    package_id,
                    member_path,
                    raw_record,
                    semantic_hash,
                )
    if selected_ids - set(definitions):
        raise ActivityRuntimeError(
            f"package definitions are unavailable: {sorted(selected_ids - set(definitions))}"
        )
    return definitions


def _validate_active_primitive(
    primitive_id: str,
    activity_id: str,
    *,
    primitive_rows: Mapping[str, Mapping[str, object]],
    matrices: Mapping[str, object],
    value_contracts: Mapping[str, object],
    core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
) -> Mapping[str, object]:
    registries = _mapping(core.get("registries"), "core catalog registries")
    registry_ids = _sequence(registries.get("activity_primitives"), "primitive IDs")
    visiting: set[str] = set()
    visited: set[str] = set()
    pending: list[tuple[str, bool]] = [(primitive_id, False)]
    while pending:
        current_id, leaving = pending.pop()
        if leaving:
            visiting.remove(current_id)
            visited.add(current_id)
            continue
        if current_id in visited:
            continue
        if current_id in visiting:
            raise ActivityNotSelectable(
                f"primitive activation dependency cycle at {current_id}"
            )

        primitive = primitive_rows.get(current_id)
        ledger = ledger_rows.get(("activity_primitives", current_id))
        if (
            primitive is None
            or ledger is None
            or primitive.get("realization_state") != "COMPLETE"
            or primitive.get("selection_state") != "ACTIVE_ADMITTED"
            or ledger.get("realization_state") != "COMPLETE"
            or ledger.get("admission_disposition") != "ACTIVE_ADMITTED"
        ):
            raise ActivityNotSelectable(f"unknown or dormant primitive: {current_id}")
        declarations = _mapping(primitive.get("compiler_declarations", {}), "compiler declarations")
        declaration = declarations.get(activity_id)
        if declaration is not None:
            _validate_shape("activity-compiler-declaration", declaration)
        if not _contains_id(primitive.get("exact_seed_consumer_ids"), activity_id) and declaration is None:
            raise ActivityNotSelectable(
                f"primitive {current_id} has no exact consumer {activity_id}"
            )
        if current_id not in registry_ids:
            raise ActivityRuntimeError(
                f"primitive is absent from core catalog: {current_id}"
            )

        matrix = _mapping(matrices.get(current_id), f"{current_id} validation matrix")
        activation = _mapping(
            matrix.get("activation_dependencies"), "activation dependencies"
        )
        required_values = {
            _require_id(value, "required active value kind")
            for value in _sequence(
                activation.get("required_active_value_kinds"), "required values"
            )
        }
        if required_values - set(value_contracts):
            raise ActivityRuntimeError(
                f"{current_id} has an unavailable value dependency"
            )
        required_primitives = tuple(
            _require_id(value, "required active primitive ID")
            for value in _sequence(
                activation.get("required_active_primitive_ids"),
                "required primitives",
            )
        )
        if len(required_primitives) != len(set(required_primitives)):
            raise ActivityRuntimeError(
                f"{current_id} has ambiguous primitive activation dependencies"
            )
        visiting.add(current_id)
        pending.append((current_id, True))
        for dependency_id in reversed(required_primitives):
            if dependency_id in visiting:
                raise ActivityNotSelectable(
                    f"primitive activation dependency cycle at {dependency_id}"
                )
            if dependency_id not in visited:
                pending.append((dependency_id, False))

    return primitive_rows[primitive_id]


def _validate_selector_read(
    selector_id: str,
    activity_id: str,
    *,
    mechanical: Mapping[str, object],
    core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
) -> None:
    selector = _mapping(mechanical.get("selectors"), "selectors").get(selector_id)
    registries = _mapping(core.get("registries"), "core registries")
    if not isinstance(selector, Mapping) or selector_id not in _sequence(
        registries.get("rule_selectors"), "rule selectors"
    ):
        raise ActivityNotSelectable(f"unknown selector read: {selector_id}")
    for operation_id in _sequence(
        selector.get("allowed_operations"), f"{selector_id} allowed operations"
    ):
        _selector_operation_pair_is_admitted(
            selector_id,
            _require_id(operation_id, "selector operation ID"),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
        )
    admission = ledger_rows.get(("rule_selectors", selector_id))
    if (
        admission is None
        or admission.get("admission_disposition") != "ACTIVE_ADMITTED"
        or admission.get("realization_state") != "COMPLETE"
    ):
        raise ActivityNotSelectable(f"selector is dormant: {selector_id}")
    consumer_text = admission.get("consumer_or_dependency")
    consumers = (
        set(re.findall(r"\bactivity\.[A-Za-z0-9_.:-]+\b", consumer_text))
        if isinstance(consumer_text, str)
        else set()
    )
    if activity_id not in consumers:
        raise ActivityNotSelectable(
            f"selector {selector_id} is not admitted for {activity_id}"
        )


def _selector_operation_pair_is_admitted(
    selector_id: str,
    operation_id: str,
    *,
    mechanical: Mapping[str, object],
    core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
) -> None:
    selectors = _mapping(mechanical.get("selectors"), "mechanical selectors")
    selector = selectors.get(selector_id)
    registries = _mapping(core.get("registries"), "core registries")
    operations = _sequence(registries.get("rule_operations"), "rule operations")
    operation_contracts = (
        _mapping(selector.get("operation_contracts"), "selector operation contracts")
        if isinstance(selector, Mapping)
        else {}
    )
    allowed = (
        _sequence(selector.get("allowed_operations"), "selector allowed operations")
        if isinstance(selector, Mapping)
        else ()
    )
    ledger = ledger_rows.get(("rule_operations", operation_id))
    if (
        not isinstance(selector, Mapping)
        or operation_id not in allowed
        or operation_id not in operation_contracts
        or operation_id not in operations
        or ledger is None
        or ledger.get("admission_disposition") != "ACTIVE_ADMITTED"
        or ledger.get("realization_state") != "COMPLETE"
    ):
        raise ActivityNotSelectable(
            f"selector-operation pair is unknown, dormant, or unadmitted: "
            f"{selector_id}+{operation_id}"
        )


def _validate_fact_read(
    fact_id: str,
    activity_id: str,
    mechanical: Mapping[str, object],
) -> None:
    fact = _mapping(mechanical.get("context_facts"), "context facts").get(fact_id)
    if (
        not isinstance(fact, Mapping)
        or fact.get("disposition") != "ACTIVE_ADMITTED"
        or not _contains_id(fact.get("permitted_consumer_ids"), activity_id)
    ):
        raise ActivityNotSelectable(
            f"invocation fact is unknown, dormant, or unauthorized: {fact_id}"
        )


def _reject_source_lowered_references(value: object) -> None:
    """Compiler reference wrappers are output DTOs, never source literals."""
    pending = [value]
    reference_keys = {"symbol_ref", "parameter_ref", "export_ref", "scope_ref"}
    while pending:
        current = pending.pop()
        if isinstance(current, Mapping):
            if isinstance(current.get("value_kind"), str) and any(
                isinstance(current.get(key), str) for key in reference_keys
            ):
                raise ActivityRuntimeError("source-authored lowered reference object is not admitted")
            pending.extend(current.values())
        elif isinstance(current, (list, tuple)):
            pending.extend(current)


def _normalize_value_reference(
    raw: object,
    *,
    value_kind: str,
    activity_id: str,
    parameters: Mapping[str, object],
    exports: Mapping[str, Mapping[str, object]],
    previous_results: Mapping[str, object],
    value_contracts: Mapping[str, object],
    mechanical: Mapping[str, object],
    core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
    read_refs: list[str],
    symbols: Mapping[str, object] = MappingProxyType({}),
    retained_symbols: dict[str, object] | None = None,
    occurrence_id: str = "",
    scopes: Mapping[str, object] = MappingProxyType({}),
    cardinality: str = "single",
    export_guards: Mapping[str, tuple[Mapping[str, object], ...]] = MappingProxyType({}),
    active_guards: tuple[Mapping[str, object], ...] = (),
    source_definitions: Mapping[str, Mapping[str, object]] = MappingProxyType({}),
) -> object:
    if not isinstance(raw, str):
        _reject_source_lowered_references(raw)
        return raw
    if raw.startswith("$"):
        scope = raw.removeprefix("$")
        descriptor = scopes.get(scope)
        if not isinstance(descriptor, Mapping):
            raise ActivityRuntimeError(f"unavailable child scope: {raw}")
        if descriptor["value_kind"] != value_kind and not (value_kind == "role" and descriptor["value_kind"] == "entity_ref"):
            raise ActivityRuntimeError(f"child scope has wrong value kind: {raw}")
        return {"scope_ref": scope, "value_kind": value_kind}
    if raw.startswith("compiled."):
        symbol_id, separator, raw_scope = raw.partition(":")
        scope_name = raw_scope.removeprefix("$") if separator else None
        if separator and (not raw_scope.startswith("$") or ":" in raw_scope):
            raise ActivityRuntimeError(f"producer scope is unavailable or incompatible: {raw}")
        if symbol_id not in symbols:
            raise ActivityNotSelectable(f"compiled symbol has unavailable source producer contract: {raw} at {occurrence_id}")
        _resolve_compiler_symbol(
            symbol_id, expected_kind=value_kind, cardinality=cardinality, occurrence_id=occurrence_id,
            activity_id=activity_id, declarations=symbols, values=value_contracts,
            mechanical=mechanical, core=core, ledger_rows=ledger_rows,
            reads=read_refs, retained=retained_symbols if retained_symbols is not None else {},
            parameters=parameters,
            scopes=scopes, scope_name=scope_name,
            source_definitions=source_definitions,
        )
        return {"symbol_ref": symbol_id + (f":{scope_name}" if scope_name is not None else ""), "value_kind": value_kind}
    if raw.startswith("invocation."):
        reference = raw.removeprefix("invocation.")
        if value_kind == "invocation_fact":
            _validate_fact_read(reference, activity_id, mechanical)
            read_refs.append(f"fact:{reference}")
            return {"parameter_ref": raw, "value_kind": value_kind}
        parameter = parameters.get(reference)
        if not isinstance(parameter, Mapping):
            raise ActivityRuntimeError(f"unknown invocation parameter: {reference}")
        if parameter.get("value_type") != value_kind:
            raise ActivityRuntimeError(
                f"invocation parameter {reference} has the wrong compiled value kind"
            )
        return {"parameter_ref": reference, "value_kind": value_kind}
    if raw.startswith("selector."):
        selector_id = raw.removeprefix("selector.")
        _validate_selector_read(
            selector_id,
            activity_id,
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
        )
        selector = mechanical["selectors"][selector_id]
        if selector["result_type"] != value_kind and not (selector["result_type"] == "integer" and value_kind == "number"):
            raise ActivityRuntimeError(f"selector result has wrong value kind: {selector_id}")
        read_refs.append(f"selector:{selector_id}")
        return {"parameter_ref": raw, "value_kind": value_kind}
    if value_kind in {
        "activity_definition_ref",
        "effect_definition_ref",
        "entity_definition_ref",
        "resource_definition_ref",
        "zone_definition_ref",
    }:
        _validate_bound_definition_reference(value_kind, raw, values=value_contracts,
            source_definitions=source_definitions, core=core)
        return raw
    value_contract = _mapping(value_contracts.get(value_kind), "compiled value contract")
    enum_values = value_contract.get("enum")
    if isinstance(enum_values, (list, tuple)) and any(
        type(raw) is type(candidate) and raw == candidate for candidate in enum_values
    ):
        return raw
    catalog_ref = value_contract.get("catalog_ref")
    registries = _mapping(core.get("registries"), "core registries")
    if isinstance(catalog_ref, str) and catalog_ref in registries:
        if raw in _sequence(registries[catalog_ref], f"{catalog_ref} registry"):
            return raw
        raise ActivityNotSelectable(
            f"catalog reference is not admitted for {value_kind}: {raw}"
        )
    if "." in raw:
        export_name, _, result_name = raw.partition(".")
        if any(guard not in active_guards for guard in export_guards.get(export_name, ())):
            raise ActivityRuntimeError(f"guarded export is unavailable in this scope: {raw}")
        result_contracts = (
            previous_results if export_name == "result" else exports.get(export_name)
        )
        if result_contracts is None or result_name not in result_contracts:
            raise ActivityRuntimeError(f"unavailable Activity export reference: {raw}")
        result = _mapping(result_contracts[result_name], "primitive result contract")
        if result.get("cardinality") != cardinality:
            raise ActivityRuntimeError(f"Activity export has wrong cardinality: {raw}")
        produced_kind = str(result.get("value_kind"))
        if produced_kind != value_kind:
            produced_contract = _mapping(
                value_contracts.get(produced_kind), "produced value contract"
            )
            consumed_contract = _mapping(
                value_contracts.get(value_kind), "consumed value contract"
            )
            if not (
                produced_kind == "roll_result"
                and value_kind == "prior_roll_result"
                and produced_contract.get("schema_ref")
                == consumed_contract.get("schema_ref")
            ):
                raise ActivityRuntimeError(
                    f"Activity export has the wrong value kind: {raw}"
                )
        return {"export_ref": raw, "value_kind": value_kind}
    return raw


def _resource_owner_family(
    resource_id: str,
    source_definitions: Mapping[str, Mapping[str, object]],
) -> str:
    record = source_definitions.get(resource_id)
    if (
        not isinstance(record, Mapping)
        or record.get("kind") != "definition.resource"
        or not isinstance(record.get("data"), Mapping)
    ):
        raise ActivityNotSelectable(
            f"resource owner binding is unavailable for {resource_id}"
        )
    lifetime_owner = record["data"].get("lifetime_owner")
    family_by_owner = {
        "actor": "world.actor",
        "asset": "world.asset",
        "procedure": "runtime.procedure",
    }
    family = family_by_owner.get(lifetime_owner)
    if family is None:
        raise ActivityNotSelectable(
            f"resource {resource_id} has no admitted native owner family"
        )
    return family


def _bound_role_family(
    primitive_id: str,
    argument_name: str,
    primitive_matrix: Mapping[str, object],
    raw_arguments: Mapping[str, object],
    source_definitions: Mapping[str, Mapping[str, object]],
) -> str:
    subject_policy = primitive_matrix.get("subject_policy")
    storage_policy = primitive_matrix.get("storage_policy")
    if primitive_id == "op.consume_resource" and argument_name == "owner_role":
        resource_id = _require_id(raw_arguments.get("resource_ref"), "resource_ref")
        return _resource_owner_family(resource_id, source_definitions)
    if subject_policy in {
        "BOUND_ACTOR_CURRENT_TURN_ONLY",
        "BOUND_ACTOR_IS_BOTH_SOURCE_AND_TARGET",
    }:
        return "world.actor"
    if storage_policy == "WORLD_ACTOR_OWNER_ONLY":
        return "world.actor"
    raise ActivityNotSelectable(
        f"{primitive_id}.{argument_name} has no source-specific native role-family mapping"
    )


def _register_role_contract(
    role_contracts: dict[str, Mapping[str, object]],
    role_name: str,
    family_key: str,
) -> None:
    contract = {"family_key": family_key, "required": True}
    previous = role_contracts.get(role_name)
    if previous is not None and previous != contract:
        raise ActivityNotSelectable(
            f"native role {role_name} has conflicting owner-family requirements"
        )
    role_contracts[role_name] = contract


def _compile_predicate_reads(
    predicate: object,
    *,
    activity_id: str,
    mechanical: Mapping[str, object],
    core: Mapping[str, object],
    ledger_rows: Mapping[tuple[str, str], Mapping[str, object]],
    reads: list[str],
) -> None:
    _validate_shape("mechanical-predicate", predicate)
    node = _mapping(predicate, "mechanical predicate")
    if "fact" in node:
        fact_id = _require_id(node["fact"], "predicate fact")
        _validate_fact_read(fact_id, activity_id, mechanical)
        reads.append(f"fact:{fact_id}")
    elif "all" in node or "any" in node:
        key = "all" if "all" in node else "any"
        for child in _sequence(node[key], "predicate children"):
            _compile_predicate_reads(
                child,
                activity_id=activity_id,
                mechanical=mechanical,
                core=core,
                ledger_rows=ledger_rows,
                reads=reads,
            )
    elif "not" in node:
        _compile_predicate_reads(
            node["not"],
            activity_id=activity_id,
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            reads=reads,
        )
    elif "compare" in node:
        compare = _mapping(node["compare"], "predicate comparison")
        for side in ("left", "right"):
            operand = compare.get(side)
            if isinstance(operand, Mapping) and "accessor_id" in operand:
                accessor_id = _require_id(operand["accessor_id"], "predicate accessor")
                accessors = _mapping(mechanical.get("accessors"), "accessors")
                accessor = accessors.get(accessor_id)
                admission = ledger_rows.get(("mechanical_accessors", accessor_id))
                if (
                    not isinstance(accessor, Mapping)
                    or accessor.get("disposition") != "ACTIVE_ADMITTED"
                    or admission is None
                    or admission.get("admission_disposition") != "ACTIVE_ADMITTED"
                    or not _contains_id(
                        accessor.get("permitted_consumer_ids"), activity_id
                    )
                ):
                    raise ActivityRuntimeError(
                        f"accessor is unknown, dormant, or unauthorized: {accessor_id}"
                    )
                reads.append(f"accessor:{accessor_id}")
        operand_kinds = []
        for side in ("left", "right"):
            operand = compare[side]
            if isinstance(operand, Mapping):
                kind = mechanical["accessors"][operand["accessor_id"]]["value_type"]
                operand_kinds.append("number" if kind in {"integer", "number"} else kind)
            else:
                operand_kinds.append("number" if type(operand) in {int, float} else "boolean" if type(operand) is bool else "string")
        if operand_kinds[0] != operand_kinds[1] or (compare["operator"] not in {"eq", "ne"} and operand_kinds[0] != "number"):
            raise ActivityRuntimeError("predicate operands have incompatible comparison types")


def _compile_activity_definition(
    activity_id: str,
    definition: Mapping[str, object],
    source_record: Mapping[str, object],
    *,
    catalog_context: BoundCatalogContext,
    source: ActivityCompilerContractSource,
    source_definitions: Mapping[str, Mapping[str, object]],
    compiler_generation: int,
    mode_policy_profile_id: str,
    _occurrence_prefix: str | None = None,
    _inherited_exports: Mapping[str, Mapping[str, object]] | None = None,
    _scopes: Mapping[str, object] | None = None,
    _inherited_export_guards: Mapping[str, tuple[Mapping[str, object], ...]] | None = None,
    _enclosing_guards: tuple[Mapping[str, object], ...] = (),
    _definition_dependency_graph: Mapping[str, tuple[str, ...]] | None = None,
) -> contracts.CompiledActivity | _LoweredSteps:
    (
        _admission,
        mechanical,
        _primitive_data,
        core,
        _portable,
        ledger_rows,
        primitive_rows,
        matrices,
        values,
    ) = _runtime_contract_maps(source)
    data = _mapping(definition["data"], f"{activity_id}.data")
    if (
        source_record.get("id") != activity_id
        or source_record.get("kind") != definition.get("kind")
        or source_record.get("data") != data
    ):
        raise ActivityRuntimeError(
            "compiled Activity differs from its frozen source record"
        )
    _validate_shape("activity-definition-data", data)
    if data.get("targeting") is not None and data["targeting"]["minimum"] > data["targeting"]["maximum"]:
        raise ActivityRuntimeError("target minimum exceeds maximum")
    contracts.validate_nonexecutable_details(data.get("details", {}))
    if definition.get("kind") != "definition.activity":
        raise ActivityRuntimeError(f"{activity_id} is not an Activity definition")
    # family_id is a routing/classification label, not an executable registry.
    _require_id(data.get("family_id"), "Activity family_id")

    raw_profile_bindings = data.get("profile_bindings", ())
    profile_binding_values = _sequence(raw_profile_bindings, "profile_bindings")
    if profile_binding_values:
        try:
            bindings = tuple(
                contracts.ProfileBinding(
                    str(_mapping(item, "profile binding")["consumer_id"]),
                    str(_mapping(item, "profile binding")["profile_id"]),
                    _mapping(item, "profile binding")["profile_generation"],
                )
                for item in profile_binding_values
            )
            declared_edges = tuple(
                (profile["profile_id"], profile["profile_generation"], profile["consumer_id"])
                for primitive in primitive_rows.values()
                for declaration in (primitive.get("compiler_declarations", {}).get(activity_id),)
                if declaration is not None
                for profile in declaration["profiles"]
            )
            contracts.validate_profile_bindings(bindings,
                occurrence_ids=tuple(edge[2] for edge in declared_edges), admitted_contracts=declared_edges)
        except contracts.ActivityContractError as exc:
            raise ActivityNotSelectable(
                f"Activity profile binding is not admitted: {exc}"
            ) from exc

    parameters = dict(_mapping(data.get("parameters", {}), "Activity parameters"))
    _validate_shape("parameters", parameters)
    steps = _sequence(data.get("steps"), "Activity steps")
    exports: dict[str, Mapping[str, object]] = dict(_inherited_exports or {})
    instructions: list[contracts.CompiledInstruction] = []
    read_plan: list[str] = []
    dependency_ids: set[str] = set()
    cost_refs: list[str] = []
    transition_refs: list[str] = []
    role_contracts: dict[str, Mapping[str, object]] = {}
    profile_bindings: list[contracts.ProfileBinding] = []
    export_contracts: dict[str, object] = {}
    prior_results: Mapping[str, object] = {}
    retained_symbols: dict[str, object] = {}
    scopes = _scopes or {}
    export_guards = dict(_inherited_export_guards or {})
    local_exports: set[str] = set()

    for index, raw_step in enumerate(steps):
        step = _mapping(raw_step, f"Activity step {index}")
        primitive_id = _require_id(step.get("op"), "Activity primitive ID")
        occurrence_id = f"{_occurrence_prefix or activity_id}.step.{index}"
        active_guards = _enclosing_guards + ((step["when"],) if step.get("when") is not None else ())
        primitive = _validate_active_primitive(
            primitive_id,
            activity_id,
            primitive_rows=primitive_rows,
            matrices=matrices,
            value_contracts=values,
            core=core,
            ledger_rows=ledger_rows,
        )
        declaration = _mapping(primitive.get("compiler_declarations", {}), "compiler declarations").get(activity_id)
        if declaration is not None:
            for parameter_name, parameter in declaration.get("parameters", {}).items():
                if parameter_name in parameters and parameters[parameter_name] != parameter:
                    raise ActivityRuntimeError(f"conflicting compiler parameter contract: {parameter_name}")
                parameters[parameter_name] = parameter
            _validate_shape("parameters", parameters)
            for role, family in _mapping(declaration["roles"], "declared roles").items():
                _register_role_contract(role_contracts, role, family)
        raw_args = _mapping(step.get("args", {}), "primitive arguments")
        _reject_source_lowered_references(raw_args)
        argument_specs = _mapping(
            primitive.get("arguments"), "primitive argument contracts"
        )
        required = {
            name
            for name, spec in argument_specs.items()
            if _mapping(spec, "primitive argument contract").get("required") is True
        }
        if required - set(raw_args):
            raise ActivityRuntimeError(f"{primitive_id} has missing required arguments")
        if set(raw_args) - set(argument_specs):
            raise ActivityRuntimeError(f"{primitive_id} has unknown arguments")

        compiled_args: dict[str, object] = {}
        step_reads: list[str] = []
        children: list[contracts.CompiledInstruction] = []
        child_scopes = dict(scopes)
        symbols = declaration["symbols"] if declaration is not None else {}
        role_arguments = dict(raw_args)
        if primitive_id == "op.consume_resource":
            resource_reference = raw_args.get("resource_ref")
            if isinstance(resource_reference, str) and resource_reference.startswith("compiled."):
                _resolve_compiler_symbol(resource_reference, expected_kind="resource_definition_ref", cardinality="single",
                    occurrence_id=occurrence_id, activity_id=activity_id, declarations=symbols, values=values,
                    mechanical=mechanical, core=core, ledger_rows=ledger_rows,
                    reads=step_reads, retained=retained_symbols, parameters=parameters, source_definitions=source_definitions)
                role_arguments["resource_ref"] = symbols[resource_reference]["value"]
            _validate_bound_definition_reference("resource_definition_ref", role_arguments.get("resource_ref"),
                values=values, source_definitions=source_definitions, core=core)
        if primitive_id == "op.for_each_target":
            target_export = raw_args.get("targets")
            if isinstance(target_export, str) and target_export.startswith("compiled."):
                _resolve_compiler_symbol(target_export, expected_kind="entity_ref", cardinality="many",
                    occurrence_id=occurrence_id, activity_id=activity_id, declarations=symbols, values=values,
                    mechanical=mechanical, core=core, ledger_rows=ledger_rows,
                    reads=step_reads, retained=retained_symbols)
            elif isinstance(target_export, str):
                export_name, dot, result_name = target_export.partition(".")
                if any(guard not in active_guards for guard in export_guards.get(export_name, ())):
                    raise ActivityRuntimeError("guarded export is unavailable in this scope")
                result_name = result_name if dot else "targets"
                target_contract = exports.get(export_name, {}).get(result_name)
                if not isinstance(target_contract, Mapping) or target_contract.get("value_kind") != "entity_ref" or target_contract.get("cardinality") != "many":
                    raise ActivityRuntimeError("target iteration requires a prior many entity_ref export")
                target_export = f"{export_name}.{result_name}"
            else:
                raise ActivityRuntimeError("target iteration requires an exact typed producer/export")
            target_family = role_contracts.get("target", {}).get("family_key")
            if target_family is None:
                raise ActivityNotSelectable("target iteration has unavailable native subject-family source contract")
            child_scopes["target"] = {"source_export": target_export, "value_kind": "entity_ref", "family_key": target_family}
        for argument_name, raw_value in raw_args.items():
            argument_spec = _mapping(
                argument_specs[argument_name], "primitive argument contract"
            )
            value_kind = _require_id(
                argument_spec.get("value_kind"), "primitive value kind"
            )
            if value_kind not in values:
                raise ActivityRuntimeError(
                    f"{primitive_id} uses unknown value kind {value_kind}"
                )
            if value_kind == "compiled_step_list":
                if _mapping(matrices[primitive_id], "primitive matrix").get("compiler_form_propagation") != "CHILD_STEPS_ONLY_WITH_ENCLOSING_SEGMENT_INHERITANCE":
                    raise ActivityRuntimeError("child steps have no admitted propagation contract")
                if isinstance(raw_value, str) and raw_value.startswith("compiled."):
                    _resolve_compiler_symbol(raw_value, expected_kind="compiled_step_list", cardinality="single",
                        occurrence_id=occurrence_id, activity_id=activity_id, declarations=symbols, values=values,
                        mechanical=mechanical, core=core, ledger_rows=ledger_rows,
                        reads=step_reads, retained=retained_symbols, parameters=parameters)
                    raw_value = symbols[raw_value]["value"]
                child_data = {"family_id": data["family_id"], "parameters": parameters, "steps": raw_value}
                child_record = {"id": activity_id, "kind": "definition.activity", "data": child_data}
                lowered = _compile_activity_definition(activity_id, child_record, child_record,
                    catalog_context=catalog_context, source=source, source_definitions=source_definitions,
                    compiler_generation=compiler_generation, mode_policy_profile_id=mode_policy_profile_id,
                    _occurrence_prefix=f"{occurrence_id}.{argument_name}", _inherited_exports=exports, _scopes=child_scopes,
                    _inherited_export_guards=export_guards, _enclosing_guards=active_guards)
                children.extend(lowered.instructions)
                compiled_args[argument_name] = tuple(child.consumer_id for child in lowered.instructions)
                read_plan.extend(lowered.reads)
                dependency_ids.update(lowered.dependencies)
                transition_refs.extend(lowered.transitions)
                export_contracts.update(lowered.exports)
                for role_name, role_spec in lowered.roles.items():
                    _register_role_contract(role_contracts, role_name, role_spec["family_key"])
                for symbol_id, descriptor in lowered.symbols.items():
                    if symbol_id in retained_symbols and retained_symbols[symbol_id] != descriptor:
                        raise ActivityRuntimeError(f"conflicting source producer contracts: {symbol_id}")
                    retained_symbols[symbol_id] = descriptor
                continue
            if value_kind == "mechanical_predicate" and isinstance(raw_value, Mapping):
                _compile_predicate_reads(raw_value, activity_id=activity_id,
                    mechanical=mechanical, core=core, ledger_rows=ledger_rows, reads=step_reads)
            if primitive_id == "op.for_each_target" and argument_name == "targets":
                compiled_args[argument_name] = {"symbol_ref" if str(raw_value).startswith("compiled.") else "export_ref": target_export, "value_kind": "prior_export_ref"}
                continue
            if raw_value == "activity.targeting" and value_kind == "target_spec":
                if data.get("targeting") is None:
                    raise ActivityRuntimeError("Activity targeting is unavailable")
                compiled_args[argument_name] = data["targeting"]
                continue
            if argument_spec.get("source") == "BOUND_ROLE":
                role_values = _sequence(raw_value, "bound roles") if argument_spec.get("cardinality") == "many" else (raw_value,)
                for role_name in role_values:
                    if isinstance(role_name, str) and role_name.startswith("$"):
                        scope = scopes.get(role_name.removeprefix("$"))
                        if not isinstance(scope, Mapping):
                            raise ActivityRuntimeError(f"unavailable child scope: {role_name}")
                        expected_family = _bound_role_family(primitive_id, argument_name,
                            matrices[primitive_id], role_arguments, source_definitions)
                        if scope.get("family_key") != expected_family:
                            raise ActivityRuntimeError("child scope has conflicting owner-family requirements")
                        continue
                    if not isinstance(role_name, str) or re.fullmatch(
                        r"^[a-z][a-z0-9_]*$", role_name
                    ) is None:
                        raise ActivityNotSelectable(
                            f"{primitive_id}.{argument_name} has an invalid bound role"
                        )
                    declared_family = role_contracts.get(role_name, {}).get("family_key")
                    try:
                        role_family = _bound_role_family(primitive_id, argument_name,
                            matrices[primitive_id], role_arguments, source_definitions)
                    except ActivityNotSelectable:
                        if declared_family is None:
                            raise
                        role_family = declared_family
                    if declared_family is not None and declared_family != role_family:
                        raise ActivityRuntimeError("native role has conflicting owner-family requirements")
                    _register_role_contract(role_contracts, role_name, role_family)
            if argument_spec.get("cardinality") == "many":
                compiled_args[argument_name] = tuple(
                    _normalize_value_reference(
                        item,
                        value_kind=value_kind,
                        activity_id=activity_id,
                        parameters=parameters,
                        exports=exports,
                        previous_results=prior_results,
                        value_contracts=values,
                        mechanical=mechanical,
                        core=core,
                        ledger_rows=ledger_rows,
                        read_refs=step_reads,
                        symbols=symbols, retained_symbols=retained_symbols, occurrence_id=occurrence_id, scopes=scopes,
                        export_guards=export_guards, active_guards=active_guards,
                        source_definitions=source_definitions,
                    )
                    for item in _sequence(raw_value, f"{primitive_id}.{argument_name}")
                )
            else:
                compiled_args[argument_name] = _normalize_value_reference(
                    raw_value,
                    value_kind=value_kind,
                    activity_id=activity_id,
                    parameters=parameters,
                    exports=exports,
                    previous_results=prior_results,
                    value_contracts=values,
                    mechanical=mechanical,
                    core=core,
                    ledger_rows=ledger_rows,
                    read_refs=step_reads,
                    symbols=symbols, retained_symbols=retained_symbols, occurrence_id=occurrence_id, scopes=scopes,
                    export_guards=export_guards, active_guards=active_guards,
                    source_definitions=source_definitions,
                )
            if value_kind in {
                "activity_definition_ref",
                "effect_definition_ref",
                "entity_definition_ref",
                "resource_definition_ref",
                "zone_definition_ref",
            } and isinstance(raw_value, str) and not raw_value.startswith(("compiled.", "invocation.")):
                if raw_value not in catalog_context._definition_semantic_hashes:
                    raise ActivityRuntimeError(
                        f"{primitive_id} has an unavailable definition dependency: {raw_value}"
                    )
                dependency_ids.add(raw_value)
            elif isinstance(raw_value, str) and raw_value in source_definitions:
                # Fixed enum members can also be exact content references (for
                # example the innate-sorcery Effect). Retain that bound source
                # edge even when its value kind has a specialized enum contract.
                dependency_ids.add(raw_value)

        for raw_read in _sequence(primitive.get("reads"), f"{primitive_id} reads"):
            read = _mapping(raw_read, "primitive read contract")
            read_kind = str(read.get("kind"))
            read_id = _require_id(read.get("id"), "primitive read ID")
            if read_kind == "SELECTOR":
                _validate_selector_read(read_id, activity_id, mechanical=mechanical,
                    core=core, ledger_rows=ledger_rows)
                step_reads.append(f"selector:{read_id}")
            elif read_kind == "ACCESSOR":
                # This exact active primitive's source read contract is the
                # consumer edge. Predicate/symbol reads instead need their own
                # mechanical-surface permission; an accessor's availability
                # alone never authorizes those unrelated consumers.
                accessor = _mapping(mechanical["accessors"].get(read_id), "primitive accessor")
                admission = ledger_rows.get(("mechanical_accessors", read_id))
                if (accessor.get("disposition") != "ACTIVE_ADMITTED" or admission is None
                    or admission.get("realization_state") != "COMPLETE"
                    or admission.get("admission_disposition") != "ACTIVE_ADMITTED"):
                    raise ActivityNotSelectable(f"primitive read accessor is unknown or dormant: {read_id}")
                step_reads.append(f"accessor:{read_id}")
            elif read_kind == "INVOCATION_FACT":
                _validate_fact_read(read_id, activity_id, mechanical)
                step_reads.append(f"fact:{read_id}")
            elif read_kind == "BINDING":
                if read_id not in raw_args:
                    raise ActivityRuntimeError(f"{primitive_id} omits bound read {read_id}")
                step_reads.append(f"binding:{read_id}")
            elif read_kind in {"DOMAIN_OWNER", "INFRASTRUCTURE"}:
                read_contracts = _mapping(_primitive_data.get("read_contracts"), "read contracts")
                if read_id not in _sequence(read_contracts.get(read_kind), "source read contracts"):
                    raise ActivityNotSelectable(f"primitive names an unknown {read_kind} read: {read_id}")
                step_reads.append(f"{read_kind.lower()}:{read_id}")
            else:
                raise ActivityRuntimeError(f"{primitive_id} has an unsupported read contract: {read_kind}:{read_id}")

        when = step.get("when")
        if when is not None:
            if isinstance(when, Mapping) and "result" in when:
                reference = when["result"]
                if not isinstance(reference, str) or "." not in reference:
                    raise ActivityRuntimeError(
                        "result condition has an invalid export reference"
                    )
                export_name, result_name = reference.split(".", 1)
                if any(guard not in active_guards for guard in export_guards.get(export_name, ())):
                    raise ActivityRuntimeError(f"guarded export is unavailable in this scope: {reference}")
                result_contracts = exports.get(export_name)
                if result_contracts is None or result_name not in result_contracts:
                    raise ActivityRuntimeError(
                        f"result condition uses an unavailable export: {reference}"
                    )
                result_spec = _mapping(result_contracts[result_name], "result contract")
                result_kind = str(result_spec.get("value_kind"))
                value_spec = _mapping(
                    values.get(result_kind), f"{result_kind} value contract"
                )
                allowed = value_spec.get("enum")
                if result_spec.get("cardinality") != "single":
                    raise ActivityRuntimeError("result condition requires a single typed result")
                for candidate in when["in"]:
                    _validate_shape("typed_export_value", {"value_kind": result_kind, "value": candidate})
                if isinstance(allowed, (list, tuple)) and not set(when["in"]) <= set(
                    allowed
                ):
                    raise ActivityRuntimeError(
                        f"result condition has invalid values for {reference}"
                    )
            else:
                _compile_predicate_reads(
                    when,
                    activity_id=activity_id,
                    mechanical=mechanical,
                    core=core,
                    ledger_rows=ledger_rows,
                    reads=step_reads,
                )

        results = _mapping(primitive.get("results"), "primitive result contracts")
        result_contract_refs = tuple(
            f"value.{_require_id(_mapping(spec, 'result contract').get('value_kind'), 'result value kind')}"
            for spec in results.values()
        )
        instruction = contracts.CompiledInstruction(
            consumer_id=occurrence_id,
            primitive_id=primitive_id,
            arguments=compiled_args,
            result_contract_refs=result_contract_refs,
            read_contract_refs=tuple(dict.fromkeys(step_reads)),
            guard=when,
            result_contracts=results,
            children=tuple(children),
            scope_bindings=child_scopes,
            export_name=step.get("export"),
        )
        instructions.append(instruction)
        read_plan.append(occurrence_id)
        if step_reads:
            dependency_ids.update(
                ref.split(":", 1)[1]
                for ref in step_reads
                if ref.startswith(("selector:", "accessor:", "fact:"))
            )
        export_name = step.get("export")
        if export_name is not None:
            export_name = _require_id(export_name, "Activity export")
            if export_name in local_exports:
                raise ActivityRuntimeError(f"duplicate Activity export: {export_name}")
            local_exports.add(export_name)
            exports[export_name] = results
            export_guards[export_name] = active_guards
            export_contracts[occurrence_id] = {
                name: {
                    "value_kind": spec["value_kind"],
                    "cardinality": spec["cardinality"],
                    "required": spec["required"],
                    "source": spec["source"],
                }
                for name, spec in results.items()
            }
        prior_results = results
        export_guards["result"] = active_guards
        for transition_kind in _sequence(
            _mapping(primitive.get("prospective_outputs"), "prospective outputs").get(
                "transition_kinds"
            ),
            "transition kinds",
        ):
            transition_refs.append(_require_id(transition_kind, "transition kind"))

    for descriptor in retained_symbols.values():
        if "value" not in descriptor:
            continue
        value_contract = values[descriptor["value_kind"]]
        registry = value_contract.get("catalog_ref", "")
        if isinstance(registry, str) and (registry == "content_definition_kinds" or registry.startswith("content_definition_kinds:")):
            references = descriptor["value"] if descriptor["cardinality"] == "many" else (descriptor["value"],)
            dependency_ids.update(references)

    if _occurrence_prefix is not None:
        return _LoweredSteps(tuple(instructions), role_contracts, export_contracts, tuple(read_plan),
            tuple(sorted(dependency_ids)), tuple(dict.fromkeys(transition_refs)), retained_symbols)
    pending = list(instructions)
    occurrences: list[str] = []
    admitted_profiles: list[tuple[str, int, str]] = []
    while pending:
        instruction = pending.pop()
        occurrences.append(instruction.consumer_id)
        pending.extend(instruction.children)
        declaration = primitive_rows[instruction.primitive_id].get("compiler_declarations", {}).get(activity_id)
        if declaration is not None:
            for profile in declaration["profiles"]:
                if profile["consumer_id"] == instruction.consumer_id:
                    admitted_profiles.append((profile["profile_id"], profile["profile_generation"], profile["consumer_id"]))
    try:
        contracts.validate_profile_bindings(
            bindings if profile_binding_values else (), occurrence_ids=tuple(occurrences),
            admitted_contracts=tuple(admitted_profiles))
    except contracts.ActivityContractError as exc:
        raise ActivityNotSelectable(f"Activity profile binding is not admitted: {exc}") from exc
    profile_bindings.extend(bindings if profile_binding_values else ())
    activation = data.get("activation")
    timing_refs: list[str] = []
    if activation is not None and "economy_id" in activation:
        _validate_shape("typed_export_value", {"value_kind": "action_economy_id", "value": activation["economy_id"]})
        timing_refs.append(activation["economy_id"])
    duration = data.get("duration")
    if duration is not None:
        timing_refs.append(duration["kind_id"])
        if "unit_id" in duration:
            timing_refs.append(duration["unit_id"])
        if "boundary_id" in duration:
            registry = _mapping(core["registries"], "core registries")
            if duration["boundary_id"] not in registry["boundary_kinds"]:
                raise ActivityNotSelectable(f"unavailable timing boundary: {duration['boundary_id']}")
            timing_refs.append(duration["boundary_id"])
        if "subject_role" in duration and duration["subject_role"] not in role_contracts:
            raise ActivityRuntimeError("duration subject role has no admitted native family")
    if data.get("targeting") is not None and not any(
        instruction.primitive_id == "op.select_targets" for instruction in instructions
    ):
        raise ActivityNotSelectable(
            "Activity declares targeting without an admitted selection consumer"
        )
    for raw_cost in _sequence(data.get("costs", ()), "Activity costs"):
        _validate_shape("cost-spec", raw_cost)
        cost = _mapping(raw_cost, "CostSpec")
        resource_id = _require_id(cost["resource_ref"], "CostSpec resource_ref")
        if (
            resource_id not in catalog_context._definition_semantic_hashes
            or resource_id not in source_definitions
        ):
            raise ActivityRuntimeError(
                f"CostSpec resource dependency is unavailable: {resource_id}"
            )
        cost_refs.append(resource_id)
        dependency_ids.add(resource_id)
        payer_role = _require_id(cost["payer_role"], "CostSpec payer_role")
        _register_role_contract(
            role_contracts,
            payer_role,
            _resource_owner_family(resource_id, source_definitions),
        )
    if data.get("requirements") is not None:
        _compile_predicate_reads(
            data["requirements"],
            activity_id=activity_id,
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            reads=read_plan,
        )
        dependency_ids.update(reference.split(":", 1)[1] for reference in read_plan
            if reference.startswith(("selector:", "accessor:", "fact:")))
    source_graph = _definition_dependency_graph or {}
    pending_dependencies = [activity_id, *(identity for identity in dependency_ids if identity in source_graph)]
    visited_dependencies: set[str] = set()
    while pending_dependencies:
        identity = pending_dependencies.pop()
        if identity in visited_dependencies:
            continue
        visited_dependencies.add(identity)
        for reference in source_graph.get(identity, ()):
            dependency_ids.add(reference)
            pending_dependencies.append(reference)

    lock = _mapping(catalog_context.basis["ruleset_lock"], "ruleset lock")
    inventory = _mapping(
        catalog_context.basis["engine_contract_inventory"], "engine inventory"
    )
    semantic_hash = catalog_context._definition_semantic_hashes.get(activity_id)
    if semantic_hash is None:
        raise ActivityRuntimeError(
            f"Activity has no bound semantic source hash: {activity_id}"
        )
    try:
        return contracts.CompiledActivity(
            activity_id=activity_id,
            definition_semantic_hash=semantic_hash,
            definition_semantic_hash_generation=SEMANTIC_ENTRY_DIGEST_GENERATION,
            ruleset_set_sha256=str(lock["ruleset_set_sha256"]),
            ruleset_set_digest_generation=lock["ruleset_set_digest_generation"],
            catalog_context_fingerprint=catalog_context.fingerprint,
            catalog_context_fingerprint_generation=1,
            compiler_generation=compiler_generation,
            engine_contract_inventory_sha256=str(inventory["inventory_sha256"]),
            mode_policy_profile_id=mode_policy_profile_id,
            instructions=tuple(instructions),
            parameter_contracts=parameters,
            role_contracts=role_contracts,
            export_contracts=export_contracts,
            consumer_read_plan=tuple(read_plan),
            dependency_ids=tuple(sorted(dependency_ids)),
            cost_contract_refs=tuple(cost_refs),
            native_transition_contract_refs=tuple(dict.fromkeys(transition_refs)),
            timing_contract_refs=tuple(dict.fromkeys(timing_refs)),
            profile_bindings=tuple(profile_bindings),
            safe_recompute_phases=(),
            requirements=data.get("requirements"),
            activation_contract=data.get("activation"),
            cost_contracts=tuple(data.get("costs", ())),
            duration_contract=data.get("duration"),
            targeting_contract=data.get("targeting"),
            symbol_contracts=retained_symbols,
            _issue_seal=contracts._CONTRACT_SEAL,
        )
    except contracts.ActivityContractError as exc:
        raise ActivityRuntimeError(
            f"compiled Activity contract is invalid: {exc}"
        ) from exc


def _runtime_contract_maps(
    source: ActivityCompilerContractSource,
) -> tuple[
    Mapping[str, object],
    Mapping[str, object],
    Mapping[str, object],
    Mapping[str, object],
    Mapping[str, object],
    dict[tuple[str, str], Mapping[str, object]],
    dict[str, Mapping[str, object]],
    Mapping[str, object],
    Mapping[str, object],
]:
    families = _mapping(source.compiler_contracts.get("families"), "compiler families")
    try:
        admission = _mapping(
            _mapping(families["catalog_admission"], "admission family")[
                "catalog_admission_ledger"
            ],
            "catalog admission ledger",
        )
        mechanical = _mapping(
            _mapping(families["mechanical_surface"], "mechanical family")[
                "mechanical_surfaces"
            ],
            "mechanical surfaces",
        )
        primitives = _mapping(
            _mapping(families["primitive"], "primitive family")[
                "activity_primitive_contracts"
            ],
            "Activity primitive contracts",
        )
        core = _mapping(
            _mapping(families["mechanical_surface"], "mechanical family")[
                "core_catalog"
            ],
            "core catalog",
        )
        portable = _mapping(
            _mapping(families["portable_value"], "portable family")[
                "portable_value_contracts"
            ],
            "portable value contracts",
        )
    except KeyError as exc:
        raise ActivityRuntimeError("compiler projection member is missing") from exc
    ledger_rows: dict[tuple[str, str], Mapping[str, object]] = {}
    for raw in _sequence(admission.get("entries"), "catalog admission entries"):
        entry = _mapping(raw, "catalog admission entry")
        key = (str(entry.get("registry_family")), str(entry.get("id")))
        if key in ledger_rows:
            raise ActivityRuntimeError("catalog admission ledger has duplicate IDs")
        ledger_rows[key] = entry
    primitive_rows: dict[str, Mapping[str, object]] = {}
    for raw in _sequence(primitives.get("contracts"), "primitive contracts"):
        entry = _mapping(raw, "primitive contract")
        primitive_id = _require_id(entry.get("primitive_id"), "primitive_id")
        if primitive_id in primitive_rows:
            raise ActivityRuntimeError("primitive contracts have duplicate IDs")
        primitive_rows[primitive_id] = entry
    matrices = _mapping(
        primitives.get("primitive_validation_matrix"), "primitive validation matrix"
    )
    values = _mapping(primitives.get("value_contracts"), "primitive value contracts")
    return (
        admission,
        mechanical,
        primitives,
        core,
        portable,
        ledger_rows,
        primitive_rows,
        matrices,
        values,
    )


def _freeze_natural_owner_definitions(
    dependencies: tuple[Mapping[str, object], ...],
    natural_owner_sources: object,
    context: BoundCatalogContext,
) -> dict[str, Mapping[str, object]]:
    evidence = {
        str(row["definition_id"]): row
        for row in context.basis["natural_owner_evidence"]
    }
    source_map = _mapping(natural_owner_sources, "natural owner sources")
    frozen: dict[str, Mapping[str, object]] = {}
    for dependency in dependencies:
        if dependency["source_type"] != "natural_owner":
            continue
        identity = str(dependency["definition_id"])
        row = evidence.get(identity)
        if row is None:
            raise ActivityRuntimeError("natural owner dependency is not pinned")
        source = _mapping(
            source_map.get(str(row["owner_domain"])), "natural owner source"
        )
        contents = _mapping(source.get("immutable_member_bytes"), "natural owner bytes")
        raw = contents.get(str(row["route"]))
        if not isinstance(raw, bytes) or sha256(raw) != row["content_sha256"]:
            raise ActivityRuntimeError(
                "natural owner bytes differ from pinned source identity"
            )
        try:
            record = load_json_bytes(raw)
        except RulesetContractError as exc:
            raise ActivityRuntimeError(
                "natural owner definition is not valid JSON"
            ) from exc
        if (
            not isinstance(record, Mapping)
            or record.get("id") != identity
            or record.get("kind") != row["kind"]
            or not isinstance(record.get("data"), Mapping)
        ):
            raise ActivityRuntimeError(
                "natural owner definition envelope is not closed"
            )
        frozen[identity] = record
    return frozen


def _build_cards(
    definitions: Mapping[str, Mapping[str, object]],
) -> tuple[
    dict[str, object],
    dict[str, tuple[str, ...]],
    dict[str, tuple[str, ...]],
]:
    cards: dict[str, object] = {}
    activity_to_cards: dict[str, list[str]] = {}
    aliases: dict[str, list[str]] = {}
    for identity, definition in definitions.items():
        data = _mapping(definition.get("data"), f"{identity}.data")
        details = data.get("details", {})
        if not isinstance(details, Mapping) or "capability_card" not in details:
            continue
        card = _mapping(details["capability_card"], "capability card")
        _validate_shape("capability_card", card)
        card_id = _require_id(
            card.get("definition_id"), "capability card definition_id"
        )
        if card_id in cards:
            raise ActivityRuntimeError("duplicate capability card identity")
        activity_ids = tuple(
            _require_id(item, "capability card Activity ID")
            for item in _sequence(
                card.get("activity_ids"), "capability card Activity IDs"
            )
        )
        if any(activity_id not in definitions for activity_id in activity_ids):
            raise ActivityRuntimeError(
                "capability card references an unavailable Activity"
            )
        cards[card_id] = dict(card)
        for activity_id in activity_ids:
            activity_to_cards.setdefault(activity_id, []).append(card_id)
        for label in _mapping(card["name"], "capability card names").values():
            if not isinstance(label, str):
                raise ActivityRuntimeError("capability card name is invalid")
            alias = " ".join(label.casefold().split())
            aliases.setdefault(alias, []).append(card_id)
    return (
        cards,
        {key: tuple(values) for key, values in activity_to_cards.items()},
        {key: tuple(values) for key, values in aliases.items()},
    )


def admit_activity_catalog(
    context_request: object,
    *,
    package_snapshots: Mapping[str, PackageSnapshot],
    engine_contract_inventory_source: object,
    natural_owner_sources: object,
    compiler_generation: int,
    mode_policy_profile_id: str,
) -> contracts.AdmittedActivityCatalog:
    """Validate exact sources, freeze package bytes and issue a conformance catalog."""
    if type(compiler_generation) is not int or compiler_generation < 1:
        raise ActivityRuntimeError("compiler_generation must be a positive integer")
    mode_policy_profile_id = _require_id(
        mode_policy_profile_id, "mode_policy_profile_id"
    )
    if mode_policy_profile_id not in contracts.SELECTED_PROFILE_IDS:
        raise ActivityRuntimeError(
            f"unknown mode/policy profile: {mode_policy_profile_id}"
        )
    if type(engine_contract_inventory_source) is not ActivityCompilerContractSource:
        raise ActivityRuntimeError(
            "compiler admission requires an authenticated package source"
        )

    try:
        context = bind_catalog_context(
            context_request,
            package_snapshots=package_snapshots,
            engine_contract_inventory_source=engine_contract_inventory_source,
            natural_owner_sources=natural_owner_sources,
        )
    except CatalogBindingError as exc:
        raise ActivityRuntimeError(f"catalog source binding failed: {exc}") from exc
    compiler_source = context._compiler_contract_source
    if compiler_source is None:
        raise ActivityRuntimeError("bound catalog has no compiler source carrier")

    frozen_members = _package_member_bytes(context, package_snapshots)
    package_records = _package_definition_records(frozen_members, context)
    records: dict[str, Mapping[str, object]] = {
        identity: source.record for identity, source in package_records.items()
    }
    records.update(
        _freeze_natural_owner_definitions(
            context.definition_dependencies, natural_owner_sources, context
        )
    )
    dependency_ids = {
        str(row["definition_id"]) for row in context.definition_dependencies
    }
    missing_records = dependency_ids - set(records)
    if missing_records:
        raise ActivityRuntimeError(
            f"bound definitions are absent from frozen source bytes: {sorted(missing_records)}"
        )
    graph = _definition_graph(dependency_ids, records)

    frozen_definitions: dict[str, object] = {}
    source_records: dict[str, Mapping[str, object]] = {}
    for dependency in context.definition_dependencies:
        identity = str(dependency["definition_id"])
        record = records[identity]
        frozen_definitions[identity] = _definition_envelope(
            identity, str(dependency["kind"]), record
        )
        source_records[identity] = record

    compiled: dict[str, contracts.CompiledActivity] = {}
    unavailable_activity_reasons: dict[str, str] = {}
    for identity, definition in frozen_definitions.items():
        if definition["kind"] != "definition.activity":
            continue
        source_hash = context._definition_semantic_hashes.get(identity)
        if source_hash is None:
            raise ActivityRuntimeError(
                f"Activity source hash is unavailable: {identity}"
            )
        try:
            compiled_activity = _compile_activity_definition(
                identity,
                _mapping(definition, "frozen Activity definition"),
                source_records[identity],
                catalog_context=context,
                source=compiler_source,
                source_definitions=source_records,
                compiler_generation=compiler_generation,
                mode_policy_profile_id=mode_policy_profile_id,
                _definition_dependency_graph=graph,
            )
            contracts._register_compiler_value(
                compiled_activity,
                kind="compiled",
                lineage=(context, compiler_source, identity, source_hash),
            )
            compiled[identity] = compiled_activity
        except ActivityNotSelectable as exc:
            unavailable_activity_reasons[identity] = str(exc)
            continue
        except ActivityRuntimeError:
            raise
        except contracts.ActivityContractError as exc:
            raise ActivityRuntimeError(
                f"Activity {identity} is not compilable: {exc}"
            ) from exc
    cards, capability_index, alias_index = _build_cards(
        {
            identity: _mapping(definition, "frozen definition")
            for identity, definition in frozen_definitions.items()
        }
    )
    inventory = context.basis["engine_contract_inventory"]
    try:
        admitted_catalog = contracts.AdmittedActivityCatalog(
            catalog_context=context,
            frozen_semantic_members=frozen_members,
            frozen_definitions=frozen_definitions,
            engine_contract_inventory=inventory,
            compiler_generation=compiler_generation,
            mode_policy_profile_id=mode_policy_profile_id,
            compiled_activities=compiled,
            alias_index=alias_index,
            capability_index=capability_index,
            card_index=cards,
            unavailable_activity_reasons=unavailable_activity_reasons,
            definition_dependency_graph=graph,
            _issue_seal=contracts._CONTRACT_SEAL,
        )
        contracts._register_compiler_value(
            admitted_catalog,
            kind="catalog",
            lineage=(context,),
        )
        return admitted_catalog
    except contracts.ActivityContractError as exc:
        raise ActivityRuntimeError(
            f"sealed Activity catalog is invalid: {exc}"
        ) from exc


def _compiled_identity_matches(
    catalog: contracts.AdmittedActivityCatalog,
    activity_id: str,
    compiled: object,
) -> bool:
    if (
        not contracts._compiler_value_is_issued(catalog, kind="catalog")
        or not contracts._compiler_value_is_issued(
            compiled,
            kind="compiled",
            parent=catalog.catalog_context,
        )
    ):
        return False
    if (
        compiled._issue_seal is not contracts._CONTRACT_SEAL
        or compiled.activity_id != activity_id
    ):
        return False
    context = catalog.catalog_context
    basis = context.basis
    lock = _mapping(basis["ruleset_lock"], "ruleset lock")
    inventory = _mapping(basis["engine_contract_inventory"], "engine inventory")
    semantic_hash = context._definition_semantic_hashes.get(activity_id)
    if semantic_hash is None:
        return False
    cached_key = _compiled_cache_key(
        {
            "activity_id": compiled.activity_id,
            "definition_semantic_hash_generation": compiled.definition_semantic_hash_generation,
            "definition_semantic_hash": compiled.definition_semantic_hash,
            "ruleset_set_digest_generation": compiled.ruleset_set_digest_generation,
            "ruleset_set_sha256": compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": compiled.catalog_context_fingerprint_generation,
            "catalog_context_fingerprint": compiled.catalog_context_fingerprint,
            "engine_contract_inventory_sha256": compiled.engine_contract_inventory_sha256,
            "compiler_generation": compiled.compiler_generation,
            "mode_policy_profile_id": compiled.mode_policy_profile_id,
        }
    )
    expected_key = _compiled_cache_key(
        {
            "activity_id": activity_id,
            "definition_semantic_hash_generation": SEMANTIC_ENTRY_DIGEST_GENERATION,
            "definition_semantic_hash": semantic_hash,
            "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
            "ruleset_set_sha256": lock["ruleset_set_sha256"],
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": context.fingerprint,
            "engine_contract_inventory_sha256": inventory["inventory_sha256"],
            "compiler_generation": catalog.compiler_generation,
            "mode_policy_profile_id": catalog.mode_policy_profile_id,
        }
    )
    return cached_key == expected_key


_COMPILED_CACHE_IDENTITY_FIELDS: Final[tuple[str, ...]] = (
    "activity_id",
    "definition_semantic_hash_generation",
    "definition_semantic_hash",
    "ruleset_set_digest_generation",
    "ruleset_set_sha256",
    "catalog_context_fingerprint_generation",
    "catalog_context_fingerprint",
    "engine_contract_inventory_sha256",
    "compiler_generation",
    "mode_policy_profile_id",
)


def _compiled_cache_key(identity: Mapping[str, object]) -> tuple[object, ...]:
    if set(identity) != set(_COMPILED_CACHE_IDENTITY_FIELDS):
        raise ActivityRuntimeError("compiled cache identity is incomplete or ambiguous")
    return tuple(identity[field] for field in _COMPILED_CACHE_IDENTITY_FIELDS)


def compile_activity(
    catalog: contracts.AdmittedActivityCatalog,
    activity_id: str,
) -> contracts.CompiledActivity:
    """Return a compiled cache entry or rebuild a stale derived value from frozen data."""
    if (
        not isinstance(catalog, contracts.AdmittedActivityCatalog)
        or not contracts._compiler_value_is_issued(catalog, kind="catalog")
        or catalog.catalog_context._compiler_contract_source is None
    ):
        raise ActivityRuntimeError("Activity catalog is not compiler-issued")
    activity_id = _require_id(activity_id, "activity_id")
    definition = catalog.frozen_definitions.get(activity_id)
    if (
        not isinstance(definition, Mapping)
        or definition.get("kind") != "definition.activity"
    ):
        raise ActivityRuntimeError(
            f"Activity is not admitted in this catalog: {activity_id}"
        )
    unavailable_reason = catalog.unavailable_activity_reasons.get(activity_id)
    if unavailable_reason is not None:
        raise ActivityNotSelectable(unavailable_reason)
    cached = (
        catalog.compiled_activities.get(activity_id)
        if isinstance(catalog.compiled_activities, Mapping)
        else None
    )
    if _compiled_identity_matches(catalog, activity_id, cached):
        return cached
    record = _mapping(definition, "frozen Activity definition")
    rebuilt = _compile_activity_definition(
        activity_id,
        record,
        record,
        catalog_context=catalog.catalog_context,
        source=catalog.catalog_context._compiler_contract_source,
        _definition_dependency_graph=catalog.definition_dependency_graph,
            compiler_generation=catalog.compiler_generation,
            mode_policy_profile_id=catalog.mode_policy_profile_id,
            source_definitions={
                identity: _mapping(definition, "frozen source definition")
                for identity, definition in catalog.frozen_definitions.items()
            },
        )
    contracts._register_compiler_value(
        rebuilt,
        kind="compiled",
        lineage=(
            catalog.catalog_context,
            catalog.catalog_context._compiler_contract_source,
            activity_id,
            rebuilt.definition_semantic_hash,
        ),
    )
    repaired_cache = (
        dict(catalog.compiled_activities)
        if isinstance(catalog.compiled_activities, Mapping)
        else {}
    )
    repaired_cache[activity_id] = rebuilt
    object.__setattr__(catalog, "compiled_activities", MappingProxyType(repaired_cache))
    return rebuilt


def lookup_activity(
    catalog: contracts.AdmittedActivityCatalog,
    activity_id: str,
) -> contracts.CompiledActivity:
    """Resolve a known Activity ID by direct index; names never grant capability."""
    return compile_activity(catalog, activity_id)


def lookup_capability_cards(
    catalog: contracts.AdmittedActivityCatalog,
    *,
    eligible_activity_ids: tuple[str, ...],
    query: str,
    maximum_candidates: int,
) -> tuple[Mapping[str, object], ...]:
    """Hydrate only source-owned cards reachable from supplied Actor eligibility."""
    if (
        not isinstance(catalog, contracts.AdmittedActivityCatalog)
        or not contracts._compiler_value_is_issued(catalog, kind="catalog")
    ):
        raise ActivityRuntimeError(
            "capability lookup requires a compiler-issued catalog"
        )
    if not isinstance(eligible_activity_ids, tuple):
        raise ActivityRuntimeError(
            "eligible Activity IDs must be an immutable source projection"
        )
    if len(eligible_activity_ids) != len(set(eligible_activity_ids)):
        raise ActivityRuntimeError("eligible Activity IDs are ambiguous")
    if not isinstance(query, str) or not query.strip():
        raise ActivityRuntimeError("catalog query must be non-empty")
    if type(maximum_candidates) is not int or maximum_candidates < 1:
        raise ActivityRuntimeError("maximum_candidates must be positive")
    query_key = " ".join(query.casefold().split())
    results: list[Mapping[str, object]] = []
    seen: set[str] = set()
    for activity_id in eligible_activity_ids:
        cards = catalog.capability_index.get(activity_id, ())
        for card_id in cards:
            if card_id in seen:
                continue
            card = catalog.card_index.get(card_id)
            if not isinstance(card, Mapping):
                continue
            names = _mapping(card.get("name"), "capability card names")
            alias_match = any(
                query_key in " ".join(str(label).casefold().split())
                for label in names.values()
            )
            direct_match = (
                query_key == activity_id.casefold() or query_key == card_id.casefold()
            )
            if not (alias_match or direct_match):
                continue
            results.append(card)
            seen.add(card_id)
            if len(results) >= maximum_candidates:
                return tuple(results)
    return tuple(results)
