"""Closed immutable spell preparation ABI; no compiler, dispatcher or state issuer.

These values describe structure only. The compiler/native owners must validate
source admission and complete predecessor closure before issuing sealed values.
There is deliberately no public issuance function or production profile registry.
"""

from __future__ import annotations

import math
import re
import threading
import types
import weakref
from collections.abc import Mapping
from dataclasses import dataclass, field, fields, is_dataclass
from types import MappingProxyType
from typing import (
    ClassVar,
    Final,
    Literal,
    NewType,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from .catalog_runtime import ActivityCompilerContractSource, BoundCatalogContext
from .current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    NativeOwnerRef,
)
from .hot_store import OwnerDocument
from .policy_basis import AcceptedAdjudicationBasis
from .structural_contracts import StructuralContractError, validate_contract

# framework_module_version: 1.0.7
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.7"
PROFILE_CONTRACT_GENERATION: Final = 1
NativeId = NewType("NativeId", str)
Generation = NewType("Generation", int)
Ordinal = NewType("Ordinal", int)
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_CONTRACT_SEAL = object()
_COMPILER_ISSUANCE_LOCK = threading.RLock()
_COMPILER_ISSUANCES: dict[
    int,
    tuple[
        weakref.ReferenceType[object],
        str,
        tuple[object, ...],
        tuple[tuple[str, object, object], ...],
    ],
] = {}
NON_EXECUTABLE_DETAILS_FIELDS: Final = frozenset({
    "profile_bindings", "profile_args", "stochastic_state", "reconciliation_state", "cause", "geometry",
    "restoration_basis", "restoration_basis_ref", "progress", "spell_progress", "prospective_delta", "state_delta",
    "patch", "script", "code", "form_state", "identity_state", "conversion_state", "concentration_state",
    "control_state", "subject_binding", "return_adjudication_basis_ref", "object_suspension_basis", "spell_place",
    "portal_state", "equipment_transform",
})


class ActivityContractError(ValueError):
    """A value crosses its closed structural or issuance boundary."""


def _wire_contract(name: str, value: object) -> None:
    try:
        validate_contract(name, value)
    except StructuralContractError as error:
        raise ActivityContractError(str(error)) from error


def validate_nonexecutable_details(value: object) -> None:
    if isinstance(value, Mapping):
        if NON_EXECUTABLE_DETAILS_FIELDS.intersection(value):
            raise ActivityContractError("details cannot carry executable spell state")
        for item in value.values():
            validate_nonexecutable_details(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            validate_nonexecutable_details(item)
    elif not isinstance(value, (str, int, float, bool, type(None))) or isinstance(value, float) and not math.isfinite(value):
        raise ActivityContractError("details must remain descriptive portable JSON")


def _immutable(value: object) -> object:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) and not (isinstance(key, tuple) and len(key) == 2 and all(isinstance(part, str) for part in key)) for key in value):
            raise ActivityContractError("mapping keys must be strings or exact package/member pairs")
        return MappingProxyType({key: _immutable(item) for key, item in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_immutable(item) for item in value)
    if isinstance(value, float) and not math.isfinite(value):
        raise ActivityContractError("nonfinite values are not portable")
    if isinstance(value, (str, int, float, bool, type(None), bytes, ContractValue, NativeOwnerRef)):
        return value
    raise ActivityContractError("untyped mutable value is not portable")


def _check(value: object, annotation: object, label: str) -> None:
    if annotation is NativeId:
        if not isinstance(value, str) or _ID.fullmatch(value) is None:
            raise ActivityContractError(f"{label} must be a native reference")
        return
    if annotation in (Generation, Ordinal):
        minimum = 1 if annotation is Generation else 0
        if type(value) is not int or value < minimum:
            raise ActivityContractError(f"{label} has an invalid ordinal/generation")
        return
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (types.UnionType, Union):
        for option in args:
            try:
                _check(value, option, label)
                return
            except ActivityContractError:
                pass
        raise ActivityContractError(f"{label} does not match its closed union")
    if origin is Literal:
        if value not in args or any(type(value) is not type(item) for item in args[:1]):
            raise ActivityContractError(f"{label} has an unknown discriminator")
    elif origin is tuple:
        if not isinstance(value, tuple):
            raise ActivityContractError(f"{label} must be an immutable tuple")
        if len(args) == 2 and args[1] is Ellipsis:
            for item in value:
                _check(item, args[0], label)
        else:
            if len(value) != len(args):
                raise ActivityContractError(f"{label} has an invalid tuple arity")
            for item, item_type in zip(value, args, strict=True):
                _check(item, item_type, label)
    elif origin is Mapping:
        if not isinstance(value, Mapping):
            raise ActivityContractError(f"{label} must be a mapping")
        for key, item in value.items():
            _check(key, args[0], label)
            _check(item, args[1], label)
    elif annotation in (int, bool, float):
        if type(value) is not annotation:
            raise ActivityContractError(f"{label} has the wrong scalar type")
    elif annotation is str:
        if not isinstance(value, str) or not value:
            raise ActivityContractError(f"{label} must be a nonempty string")
    elif annotation is type(None):
        if value is not None:
            raise ActivityContractError(f"{label} must be absent")
    elif annotation is not object and not isinstance(value, annotation):
        raise ActivityContractError(f"{label} has the wrong native type")
    if annotation is NativeOwnerRef:
        expected = 2 if value.family_key in {"world.knowledge", "runtime.disclosure"} else 1
        if len(value.identity) != expected:
            raise ActivityContractError(f"{label} has a foreign family identity arity")


def _compiler_issuance_fields(value: object, kind: str) -> tuple[tuple[str, object], ...]:
    ignored = {"_issue_seal"}
    if kind == "catalog":
        # Compiled entries are a disposable process-local cache; all other catalog
        # fields are source/identity owners and stay frozen by the issuance record.
        ignored.add("compiled_activities")
    return tuple(
        (member.name, getattr(value, member.name))
        for member in fields(value)
        if member.name not in ignored
    )


def _compiler_value_snapshot(value: object, active: set[int] | None = None) -> object:
    """Capture recursively immutable DTO contents, rejecting object cycles."""
    if isinstance(value, (str, int, float, bool, type(None), bytes)):
        return ("scalar", type(value), value)
    if active is None:
        active = set()
    identity = id(value)
    if identity in active:
        raise ActivityContractError("compiler value contains a reference cycle")
    active.add(identity)
    try:
        if isinstance(value, Mapping):
            return (
                "mapping",
                type(value),
                identity,
                tuple(
                    (
                        _compiler_value_snapshot(key, active),
                        _compiler_value_snapshot(item, active),
                    )
                    for key, item in value.items()
                ),
            )
        if isinstance(value, (tuple, list)):
            return (
                "sequence",
                type(value),
                identity,
                tuple(_compiler_value_snapshot(item, active) for item in value),
            )
        if is_dataclass(value) and not isinstance(value, type):
            return (
                "dataclass",
                type(value),
                identity,
                tuple(
                    (member.name, _compiler_value_snapshot(getattr(value, member.name), active))
                    for member in fields(value)
                ),
            )
        return ("identity", type(value), identity)
    finally:
        active.remove(identity)


def _same_issued_field(current: object, issued: object) -> bool:
    if isinstance(issued, (Mapping, tuple, bytes)):
        return current is issued
    return type(current) is type(issued) and current == issued


def _register_compiler_value(
    value: object,
    *,
    kind: Literal["catalog", "compiled"],
    lineage: tuple[object, ...],
) -> None:
    """Record one exact compiler-issued object and its issuer lineage."""
    expected_type = {
        "catalog": AdmittedActivityCatalog,
        "compiled": CompiledActivity,
    }[kind]
    if type(value) is not expected_type or getattr(value, "_issue_seal", None) is not _CONTRACT_SEAL:
        raise ActivityContractError("compiler issuer attempted to register a foreign value")
    if kind == "catalog":
        if (
            len(lineage) != 1
            or lineage[0] is not value.catalog_context
            or not value.catalog_context._is_admitted()
        ):
            raise ActivityContractError("catalog compiler lineage is not admitted")
    else:
        if (
            len(lineage) != 4
            or not isinstance(lineage[0], BoundCatalogContext)
            or not lineage[0]._is_admitted()
            or lineage[0]._compiler_contract_source is not lineage[1]
            or type(lineage[1]) is not ActivityCompilerContractSource
            or not lineage[1]._is_admitted()
            or lineage[2] != value.activity_id
            or lineage[3] != value.definition_semantic_hash
        ):
            raise ActivityContractError(
                "compiled Activity source/context lineage is not admitted"
            )

    identity = id(value)

    def forget(reference: weakref.ReferenceType[object]) -> None:
        with _COMPILER_ISSUANCE_LOCK:
            current = _COMPILER_ISSUANCES.get(identity)
            if current is not None and current[0] is reference:
                del _COMPILER_ISSUANCES[identity]

    reference = weakref.ref(value, forget)
    fields_snapshot = tuple(
        (name, field_value, None if kind == "catalog" else _compiler_value_snapshot(field_value))
        for name, field_value in _compiler_issuance_fields(value, kind)
    )
    record = (reference, kind, lineage, fields_snapshot)
    with _COMPILER_ISSUANCE_LOCK:
        _COMPILER_ISSUANCES[identity] = record


def _compiler_value_is_issued(
    value: object,
    *,
    kind: Literal["catalog", "compiled"],
    parent: object | None = None,
) -> bool:
    expected_type = {
        "catalog": AdmittedActivityCatalog,
        "compiled": CompiledActivity,
    }[kind]
    if type(value) is not expected_type or getattr(value, "_issue_seal", None) is not _CONTRACT_SEAL:
        return False
    with _COMPILER_ISSUANCE_LOCK:
        record = _COMPILER_ISSUANCES.get(id(value))
    if record is None or record[0]() is not value or record[1] != kind:
        return False
    lineage = record[2]
    if (
        kind == "catalog"
        and parent is not None
        and (len(lineage) != 1 or lineage[0] is not parent)
    ):
        return False
    if kind == "catalog":
        if not value.catalog_context._is_admitted() or lineage[0] is not value.catalog_context:
            return False
    else:
        if (
            len(lineage) != 4
            or not isinstance(lineage[0], BoundCatalogContext)
            or not lineage[0]._is_admitted()
            or lineage[0]._compiler_contract_source is not lineage[1]
            or type(lineage[1]) is not ActivityCompilerContractSource
            or not lineage[1]._is_admitted()
            or lineage[2] != value.activity_id
            or lineage[3] != value.definition_semantic_hash
        ):
            return False
        if parent is not None and lineage[0] is not parent:
            return False
    try:
        current_fields = _compiler_issuance_fields(value, kind)
        current_snapshots = tuple(
            (name, field_value, None if kind == "catalog" else _compiler_value_snapshot(field_value))
            for name, field_value in current_fields
        )
    except (ActivityContractError, AttributeError, RecursionError, TypeError, ValueError):
        return False
    if len(current_snapshots) != len(record[3]):
        return False
    # Catalog source containers are recursively detached immutable JSON/bytes
    # at issue. Exact field identity plus the context/source issuers proves their
    # retention without walking the whole catalog again. Compiled instructions
    # retain recursive snapshots because frozen dataclass members can otherwise
    # be replaced through object.__setattr__.
    return all(
        current_name == issued_name
        and _same_issued_field(current_value, issued_value)
        and current_snapshot == issued_snapshot
        for (current_name, current_value, current_snapshot), (
            issued_name,
            issued_value,
            issued_snapshot,
        ) in zip(
            current_snapshots, record[3], strict=True
        )
    )


def _compiler_value_lineage(value: object, *, kind: Literal["catalog", "compiled"]) -> tuple[object, ...] | None:
    if not _compiler_value_is_issued(value, kind=kind):
        return None
    with _COMPILER_ISSUANCE_LOCK:
        record = _COMPILER_ISSUANCES.get(id(value))
    return None if record is None else record[2]


class ContractValue:
    """Frozen dataclasses validate all nested fields; unknown kwargs reject."""

    __slots__ = ()

    def __post_init__(self) -> None:
        hints = get_type_hints(type(self))
        for member in fields(self):
            value = getattr(self, member.name)
            if member.name.startswith("_"):
                continue
            _check(value, hints[member.name], member.name)
            if isinstance(value, Mapping):
                object.__setattr__(self, member.name, _immutable(value))
            elif isinstance(value, tuple):
                object.__setattr__(self, member.name, tuple(
                    OwnerDocument(item.campaign_id, item.family_key, item.identity, _immutable(item.payload), item.source_basis, item.generation)
                    if isinstance(item, OwnerDocument) else _immutable(item) if isinstance(item, Mapping) else item
                    for item in value
                ))


@dataclass(frozen=True, slots=True)
class _NativeClosedValue(ContractValue):
    value: Mapping[str, object]
    contract_fragment: ClassVar[str]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        _wire_contract("https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json#/$defs/" + self.contract_fragment, self.value)


@dataclass(frozen=True, slots=True)
class NativeFormState(_NativeClosedValue):
    contract_fragment = "formState"


@dataclass(frozen=True, slots=True)
class NativeIdentityState(_NativeClosedValue):
    contract_fragment = "identityState"


@dataclass(frozen=True, slots=True)
class NativeConversionState(_NativeClosedValue):
    contract_fragment = "conversionState"


@dataclass(frozen=True, slots=True)
class NativeControlState(_NativeClosedValue):
    contract_fragment = "controlState"


@dataclass(frozen=True, slots=True)
class NativeTemporalOccurrence(_NativeClosedValue):
    contract_fragment = "temporalOccurrence"


@dataclass(frozen=True, slots=True)
class NativeGeometry(_NativeClosedValue):
    contract_fragment = "geometry"


@dataclass(frozen=True, slots=True)
class NativeSpatialAnchor(_NativeClosedValue):
    contract_fragment = "spatialAnchor"


@dataclass(frozen=True, slots=True)
class NativePortalState(_NativeClosedValue):
    contract_fragment = "portalState"


@dataclass(frozen=True, slots=True)
class NativeSpellPlace(_NativeClosedValue):
    contract_fragment = "spellPlace"


class _SealedValue(ContractValue):
    __slots__ = ()

    def __post_init__(self) -> None:
        if getattr(self, "_issue_seal", None) is not _CONTRACT_SEAL:
            raise ActivityContractError("only the owning compiler/native issuer may issue this value")
        super().__post_init__()


@dataclass(frozen=True, slots=True)
class SubjectBinding(ContractValue):
    principal_subject_id: NativeId
    physical_actor_id: NativeId
    binding_generation: Generation
    relation_effect_id: NativeId | None = None
    control_effect_id: NativeId | None = None


@dataclass(frozen=True, slots=True)
class ObjectSubjectBinding(ContractValue):
    principal_subject_id: NativeId
    object_asset_id: NativeId
    relation_effect_id: NativeId
    binding_generation: Generation


@dataclass(frozen=True, slots=True)
class EffectSubjectBinding(ContractValue):
    domain: Literal["physical", "mental", "identity"]
    principal_subject_id: NativeId
    binding_generation: Generation
    physical_actor_id: NativeId | None = None
    relation_effect_id: NativeId | None = None
    rebind_event_id: NativeId | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.domain == "physical" and self.physical_actor_id is None:
            raise ActivityContractError("physical Effect requires its carrier")


@dataclass(frozen=True, slots=True)
class ProfileBinding(ContractValue):
    consumer_id: NativeId
    profile_id: NativeId
    profile_generation: Literal[1]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.profile_id not in SELECTED_PROFILE_IDS:
            raise ActivityContractError("unknown selected profile")


CALCULATION_PROFILE_IDS: Final = frozenset(
    {
        "calculation.roll_advantage_srd521",
        "calculation.damage_defense_srd521",
        "calculation.armor_class_srd521",
        "calculation.capability_projection_srd521",
    }
)
CAST_PROFILE_IDS: Final = frozenset(
    {
        "execution.spell_cast.srd521",
        "execution.spell_cast.ritual",
        "execution.spell_cast.long",
        "execution.spell_cast.invalid_target",
        "execution.spell_cast.countered",
    }
)


@dataclass(frozen=True, slots=True)
class CastProfileBinding(ContractValue):
    """One exact common-cast policy bound to its compiled Activity occurrence."""

    consumer_id: NativeId
    profile_id: Literal[
        "execution.spell_cast.srd521",
        "execution.spell_cast.ritual",
        "execution.spell_cast.long",
        "execution.spell_cast.invalid_target",
        "execution.spell_cast.countered",
    ]
    profile_generation: Literal[1]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        _wire_contract(
            "cast_profile_binding",
            {
                "consumer_id": self.consumer_id,
                "profile_id": self.profile_id,
                "profile_generation": self.profile_generation,
            },
        )


@dataclass(frozen=True, slots=True)
class SelectorOperationPair(ContractValue):
    selector_id: NativeId
    operation_ids: tuple[NativeId, ...]


@dataclass(frozen=True, slots=True)
class NativeRoleBinding(ContractValue):
    read_ref: NativeId
    role_names: tuple[NativeId, ...]


@dataclass(frozen=True, slots=True)
class ContextFactBinding(ContractValue):
    consumer_ref: NativeId
    fact_ids: tuple[NativeId, ...]


@dataclass(frozen=True, slots=True)
class CalculationPolicyBinding(ContractValue):
    """Exact occurrence and read/pair references; never a policy argument bag."""

    consumer_id: NativeId
    profile_id: Literal[
        "calculation.roll_advantage_srd521",
        "calculation.damage_defense_srd521",
        "calculation.armor_class_srd521",
        "calculation.capability_projection_srd521",
    ]
    profile_generation: Literal[1]
    reads: tuple[str, ...]
    selector_operation_pairs: tuple[SelectorOperationPair, ...]
    context_fact_bindings: tuple[ContextFactBinding, ...]
    native_role_bindings: tuple[NativeRoleBinding, ...]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        _wire_contract(
            "calculation_policy_binding",
            {
                "consumer_id": self.consumer_id,
                "profile_id": self.profile_id,
                "profile_generation": self.profile_generation,
                "reads": self.reads,
                "selector_operation_pairs": tuple(
                    {
                        "selector_id": pair.selector_id,
                        "operation_ids": pair.operation_ids,
                    }
                    for pair in self.selector_operation_pairs
                ),
                "context_fact_bindings": tuple(
                    {
                        "consumer_ref": binding.consumer_ref,
                        "fact_ids": binding.fact_ids,
                    }
                    for binding in self.context_fact_bindings
                ),
                "native_role_bindings": tuple(
                    {
                        "read_ref": binding.read_ref,
                        "role_names": binding.role_names,
                    }
                    for binding in self.native_role_bindings
                ),
            },
        )


@dataclass(frozen=True, slots=True)
class CompiledCalculationPolicy(ContractValue):
    """Retained exact policy binding plus the source contracts it closes over."""

    binding: CalculationPolicyBinding
    selector_contracts: Mapping[str, object]
    accessor_contracts: Mapping[str, object]
    derived_node_contracts: Mapping[str, object]
    context_fact_contracts: Mapping[str, object]
    role_contracts: Mapping[str, object]
    dependency_read_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        _wire_contract(
            "compiled_calculation_policy",
            {
                "binding": {
                    "consumer_id": self.binding.consumer_id,
                    "profile_id": self.binding.profile_id,
                    "profile_generation": self.binding.profile_generation,
                    "reads": self.binding.reads,
                    "selector_operation_pairs": tuple(
                        {
                            "selector_id": pair.selector_id,
                            "operation_ids": pair.operation_ids,
                        }
                        for pair in self.binding.selector_operation_pairs
                    ),
                    "context_fact_bindings": tuple(
                        {
                            "consumer_ref": binding.consumer_ref,
                            "fact_ids": binding.fact_ids,
                        }
                        for binding in self.binding.context_fact_bindings
                    ),
                    "native_role_bindings": tuple(
                        {
                            "read_ref": binding.read_ref,
                            "role_names": binding.role_names,
                        }
                        for binding in self.binding.native_role_bindings
                    ),
                },
                "selector_contracts": self.selector_contracts,
                "accessor_contracts": self.accessor_contracts,
                "derived_node_contracts": self.derived_node_contracts,
                "context_fact_contracts": self.context_fact_contracts,
                "role_contracts": self.role_contracts,
                "dependency_read_refs": self.dependency_read_refs,
            },
        )


SELECTED_PROFILE_IDS: Final = frozenset(
    {"execution.wish_roll_redo", "execution.adjudication.true_polymorph_creature_object_return",
     "lifecycle.concentration.srd521"}
    | {f"execution.spell_cast.{item}" for item in ("srd521", "ritual", "long", "invalid_target", "countered")}
    | {f"execution.stochastic.{item}" for item in ("teleport_mishap", "prismatic_spray_rays", "reincarnate_choice")}
    | {f"calculation.{item}_srd521" for item in ("roll_advantage", "damage_defense", "armor_class", "capability_projection")}
    | {f"lifecycle.{family}.{item}" for family, members in (
        ("form", ("polymorph", "shapechange", "true_polymorph_creature")),
        ("identity", ("magic_jar", "astral_projection", "clone", "simulacrum")),
        ("conversion", ("animate_objects", "true_polymorph_object_creature", "true_polymorph_creature_object")),
        ("actor", ("unseen_servant", "familiar", "steed", "summon")),
        ("health", ("death_ward", "aura_of_life", "mirror_image", "resistance", "contagion_removal")),
        ("successor", ("haste", "phantom_steed", "glyph", "wall_of_stone", "true_polymorph_persistence")),
        ("progress", ("turn_gate", "rest_gate", "day_gate", "progressive_save", "maturity", "repeated_place", "observable_release")),
        ("spatial", ("zone", "movement", "portal")),
        ("control", ("command", "domination_reaction", "enclosure_reaction")),
        ("information", ("sensory_link", "divination", "corpse_answers", "illusion_recognition", "memory_change")),
    ) for item in members}
)


def validate_profile_bindings(
    bindings: tuple[ProfileBinding, ...], *, occurrence_ids: tuple[str, ...],
    admitted_contracts: tuple[tuple[str, int, str], ...],
) -> None:
    """Check exact supplied occurrence/inventory edges, never create admission."""
    seen: set[tuple[str, str]] = set()
    for binding in bindings:
        if not isinstance(binding, ProfileBinding):
            raise ActivityContractError("untyped profile binding")
        key = (binding.consumer_id, binding.profile_id)
        edge = (binding.profile_id, binding.profile_generation, binding.consumer_id)
        if key in seen or binding.consumer_id not in occurrence_ids or edge not in admitted_contracts:
            raise ActivityContractError("profile occurrence/generation is not admitted")
        seen.add(key)


@dataclass(frozen=True, slots=True)
class ExecutionRef(ContractValue):
    command_id: str
    resolution_id: str


@dataclass(frozen=True, slots=True)
class CastExecutionRef(ExecutionRef):
    cast_generation: Generation


@dataclass(frozen=True, slots=True)
class RollRef(ContractValue):
    execution_ref: ExecutionRef
    request_id: NativeId
    occurrence_id: NativeId
    generation: Generation


@dataclass(frozen=True, slots=True)
class OwnerRevisionRef(ContractValue):
    owner_ref: NativeOwnerRef
    source_basis: str
    generation: Ordinal | None
    fingerprint: str

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if re.fullmatch(r"[a-f0-9]{64}", self.fingerprint) is None:
            raise ActivityContractError("native revision requires an exact fingerprint")
        if self.owner_ref.family_key == "world.actor" and self.generation is None:
            raise ActivityContractError("Actor revision cannot be absent")


@dataclass(frozen=True, slots=True)
class AcceptedChoiceRef(ContractValue):
    offer_id: NativeId
    continuation_generation: Generation
    responder_id: NativeId
    selected_option_id: NativeId


@dataclass(frozen=True, slots=True)
class ReceiptRef(ContractValue):
    execution_ref: ExecutionRef
    segment_id: NativeId
    receipt_id: NativeId


@dataclass(frozen=True, slots=True)
class TeleportMishapState(ContractValue):
    attempt_ordinal: Ordinal
    phase: Literal["TABLE_DRAW", "MISHAP_DAMAGE", "ARRIVAL"]
    destination_binding_key: NativeId
    table_definition_id: NativeId
    table_row_id: NativeId
    fixed_draw_refs: tuple[NativeId, ...]
    target_ids: tuple[NativeId, ...]
    committed_damage_segment_refs: tuple[NativeId, ...]
    profile_id: Literal["execution.stochastic.teleport_mishap"] = "execution.stochastic.teleport_mishap"
    profile_generation: Literal[1] = 1

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if re.fullmatch(r"[a-z][a-z0-9_]*", self.destination_binding_key) is None:
            raise ActivityContractError("destination must be an exact parameter binding key")
        if len(set(self.target_ids)) != len(self.target_ids):
            raise ActivityContractError("duplicate teleport target")


@dataclass(frozen=True, slots=True)
class PrismaticSprayRaysState(ContractValue):
    target_ordinal: Ordinal
    secondary_draw_ordinal: Ordinal
    phase: Literal["INITIAL_DRAW", "SECONDARY_DRAW", "APPLY_RAYS", "NEXT_TARGET", "DONE"]
    accepted_rays: tuple[int, ...]
    fixed_draw_refs: tuple[NativeId, ...]
    profile_id: Literal["execution.stochastic.prismatic_spray_rays"] = "execution.stochastic.prismatic_spray_rays"
    profile_generation: Literal[1] = 1

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if len(self.accepted_rays) > 2 or any(not 1 <= ray <= 7 for ray in self.accepted_rays):
            raise ActivityContractError("only zero to two accepted non-eight rays are portable")
        if self.phase == "APPLY_RAYS" and (not self.accepted_rays or not self.fixed_draw_refs):
            raise ActivityContractError("ray application requires accepted rays and fixed draws")
        if self.phase == "INITIAL_DRAW" and self.accepted_rays:
            raise ActivityContractError("initial draw cannot already have accepted rays")


@dataclass(frozen=True, slots=True)
class ReincarnateChoiceState(ContractValue):
    attempt_ordinal: Ordinal
    phase: Literal["ANCESTRY_DRAW", "AWAITING_REPEAT_CHOICE", "APPLY_BODY", "DONE"]
    fixed_draw_refs: tuple[NativeId, ...]
    consumed_choice_refs: tuple[AcceptedChoiceRef, ...]
    selected_ancestry_id: NativeId | None = None
    profile_id: Literal["execution.stochastic.reincarnate_choice"] = "execution.stochastic.reincarnate_choice"
    profile_generation: Literal[1] = 1

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if (self.attempt_ordinal > 0 or self.phase != "ANCESTRY_DRAW") and self.selected_ancestry_id is None:
            raise ActivityContractError("accepted ancestry must survive continuation")


StochasticState = TeleportMishapState | PrismaticSprayRaysState | ReincarnateChoiceState


@dataclass(frozen=True, slots=True)
class AcceptedCompiledReferences(ContractValue):
    """Supplied finite reference domains, not an admission or truth issuer."""
    roll_request_ids: tuple[NativeId, ...] = ()
    roll_refs: tuple[RollRef, ...] = ()
    target_ids: tuple[NativeId, ...] = ()
    parameter_keys: tuple[str, ...] = ()
    table_rows: Mapping[NativeId, tuple[NativeId, ...]] = field(default_factory=dict)
    ancestry_definition_ids: tuple[NativeId, ...] = ()
    committed_segment_ids: tuple[NativeId, ...] = ()
    accepted_choices: tuple[AcceptedChoiceRef, ...] = ()
    execution_refs: tuple[ExecutionRef, ...] = ()
    owner_revision_refs: tuple[OwnerRevisionRef, ...] = ()
    procedure_ids: tuple[NativeId, ...] = ()
    boundary_occurrence_ids: tuple[NativeId, ...] = ()
    chronology_bridge_refs: tuple[NativeId, ...] = ()
    witness_ids: tuple[NativeId, ...] = ()
    context_fingerprints: tuple[str, ...] = ()
    live_source_ids: tuple[NativeId, ...] = ()
    frontier_refs: tuple[NativeId, ...] = ()
    receipt_refs: tuple[ReceiptRef, ...] = ()
    replacement_relation_refs: tuple[NativeId, ...] = ()
    pending_owner_refs: tuple[NativeOwnerRef, ...] = ()


def validate_stochastic_references(state: StochasticState, references: AcceptedCompiledReferences) -> None:
    """Match causal references to supplied accepted domains without executing."""
    if not isinstance(state, (TeleportMishapState, PrismaticSprayRaysState, ReincarnateChoiceState)) or not isinstance(references, AcceptedCompiledReferences):
        raise ActivityContractError("untyped stochastic reference validation")
    if any(item not in references.roll_request_ids for item in state.fixed_draw_refs):
        raise ActivityContractError("foreign fixed draw reference")
    if isinstance(state, TeleportMishapState):
        if state.destination_binding_key not in references.parameter_keys or state.table_row_id not in references.table_rows.get(state.table_definition_id, ()):
            raise ActivityContractError("foreign Teleport parameter/table/row")
        if state.target_ids != references.target_ids or any(item not in references.committed_segment_ids for item in state.committed_damage_segment_refs):
            raise ActivityContractError("Teleport target/segment closure mismatch")
        if state.phase != "TABLE_DRAW" and not state.fixed_draw_refs:
            raise ActivityContractError("dependent Teleport phase needs its fixed draw")
    elif isinstance(state, PrismaticSprayRaysState):
        bound = len(references.target_ids)
        if state.target_ordinal >= bound and not (state.phase == "DONE" and state.target_ordinal == bound):
            raise ActivityContractError("foreign Prismatic target ordinal")
    else:
        if state.selected_ancestry_id is not None and state.selected_ancestry_id not in references.ancestry_definition_ids:
            raise ActivityContractError("foreign ancestry definition")
        if any(choice not in references.accepted_choices for choice in state.consumed_choice_refs):
            raise ActivityContractError("foreign consumed choice")
        if state.phase != "ANCESTRY_DRAW" and not state.fixed_draw_refs:
            raise ActivityContractError("ancestry-dependent phase needs its fixed draw")


@dataclass(frozen=True, slots=True)
class WishInitiationFrontier(ContractValue):
    procedure_id: NativeId
    boundary_occurrence_id: NativeId
    chronology_bridge_ref: NativeId
    owner_revision_refs: tuple[OwnerRevisionRef, ...]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if not self.owner_revision_refs:
            raise ActivityContractError("Wish initiation requires native revision evidence")


@dataclass(frozen=True, slots=True)
class RecentBasisRef(ContractValue):
    witness_id: NativeId
    execution_ref: ExecutionRef
    catalog_context_fingerprint: str
    catalog_context_fingerprint_generation: Literal[1] = 1


@dataclass(frozen=True, slots=True)
class WishSourcePreparationReceipt(ContractValue):
    live_source_id: NativeId
    phase: Literal["CLOSE_PENDING", "CLOSED", "ABSORBED"]
    final_frontier_ref: NativeId
    close_receipt_ref: ReceiptRef | None = None
    absorption_receipt_ref: ReceiptRef | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.phase != "CLOSE_PENDING" and self.close_receipt_ref is None:
            raise ActivityContractError("closed source requires its exact close receipt")
        if self.phase == "ABSORBED" and self.absorption_receipt_ref is None:
            raise ActivityContractError("absorbed source requires its exact receipt")
        if self.phase == "CLOSE_PENDING" and self.close_receipt_ref is not None or self.phase != "ABSORBED" and self.absorption_receipt_ref is not None:
            raise ActivityContractError("source preparation carries a premature receipt")


@dataclass(frozen=True, slots=True)
class WishReconciliationState(ContractValue):
    wish_execution_ref: CastExecutionRef
    target_roll_ref: RollRef
    initiation_frontier: WishInitiationFrontier
    recent_basis_ref: RecentBasisRef
    phase: Literal["PREFLIGHT", "CAST_ACCEPTED", "REROLL_FIXED", "SELECTION_PENDING", "SOURCES_PREPARED", "RECONCILIATION_STAGED", "ACCEPTED", "PUBLICATION_PENDING", "SETTLED"]
    reroll_mode: Literal["NORMAL", "ADVANTAGE", "DISADVANTAGE"]
    reroll_request_refs: tuple[RollRef, ...]
    closure_evidence_refs: tuple[OwnerRevisionRef, ...]
    source_preparation_refs: tuple[WishSourcePreparationReceipt, ...]
    pending_work_refs: tuple[NativeOwnerRef, ...]
    selected_basis: Literal["ORIGINAL", "REROLL"] | None = None
    accepted_choice_ref: AcceptedChoiceRef | None = None
    reconciliation_receipt_ref: ReceiptRef | None = None
    replacement_relation_ref: NativeId | None = None
    profile_id: Literal["execution.wish_roll_redo"] = "execution.wish_roll_redo"
    profile_generation: Literal[1] = 1

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        chosen = self.phase in {"SOURCES_PREPARED", "RECONCILIATION_STAGED", "ACCEPTED", "PUBLICATION_PENDING", "SETTLED"}
        accepted = self.phase in {"ACCEPTED", "PUBLICATION_PENDING", "SETTLED"}
        if chosen != (self.selected_basis is not None) or chosen != (self.accepted_choice_ref is not None):
            raise ActivityContractError("Wish selection provenance disagrees with phase")
        if accepted != (self.reconciliation_receipt_ref is not None) or accepted != (self.replacement_relation_ref is not None):
            raise ActivityContractError("Wish acceptance evidence disagrees with phase")
        if self.phase not in {"PREFLIGHT", "CAST_ACCEPTED"} and not self.reroll_request_refs:
            raise ActivityContractError("fixed reroll evidence is missing")
        if any(reference.execution_ref != self.wish_execution_ref for reference in self.reroll_request_refs):
            raise ActivityContractError("reroll references belong to another execution")


@dataclass(frozen=True, slots=True)
class TruePolymorphObjectReturnAdjudicationResult(ContractValue):
    ordinary_return_health: Literal["entry_current_normalized"]
    destruction_result: Literal["restore_entry_health", "zero_original_policy", "principal_dead"]
    overflow: Literal["none", "terminal_damage_overflow_to_return"]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.destruction_result != "restore_entry_health" and self.overflow != "none":
            raise ActivityContractError("zero/dead return cannot carry damage overflow")


def validate_wish_references(state: WishReconciliationState, references: AcceptedCompiledReferences) -> None:
    """Validate joins over supplied accepted references, never derive eligibility."""
    if not isinstance(state, WishReconciliationState) or not isinstance(references, AcceptedCompiledReferences):
        raise ActivityContractError("untyped Wish reference validation")
    execution_refs = (state.wish_execution_ref, state.target_roll_ref.execution_ref, state.recent_basis_ref.execution_ref)
    if any(item not in references.execution_refs for item in execution_refs):
        raise ActivityContractError("foreign Wish execution reference")
    if state.recent_basis_ref.execution_ref != state.target_roll_ref.execution_ref:
        raise ActivityContractError("recent basis belongs to another targeted execution")
    if any(item.request_id not in references.roll_request_ids for item in (state.target_roll_ref, *state.reroll_request_refs)):
        raise ActivityContractError("foreign Wish roll request")
    if any(item not in references.roll_refs for item in (state.target_roll_ref, *state.reroll_request_refs)):
        raise ActivityContractError("foreign Wish occurrence/generation/roll reference")
    frontier = state.initiation_frontier
    if frontier.procedure_id not in references.procedure_ids or frontier.boundary_occurrence_id not in references.boundary_occurrence_ids or frontier.chronology_bridge_ref not in references.chronology_bridge_refs:
        raise ActivityContractError("foreign Wish initiation frontier")
    if any(item not in references.owner_revision_refs for item in (*frontier.owner_revision_refs, *state.closure_evidence_refs)):
        raise ActivityContractError("foreign native revision evidence")
    if state.recent_basis_ref.witness_id not in references.witness_ids or state.recent_basis_ref.catalog_context_fingerprint not in references.context_fingerprints:
        raise ActivityContractError("foreign protected recent basis")
    if state.accepted_choice_ref is not None and state.accepted_choice_ref not in references.accepted_choices:
        raise ActivityContractError("foreign accepted Wish choice")
    if state.reconciliation_receipt_ref is not None and state.reconciliation_receipt_ref not in references.receipt_refs:
        raise ActivityContractError("foreign reconciliation receipt")
    if state.replacement_relation_ref is not None and state.replacement_relation_ref not in references.replacement_relation_refs:
        raise ActivityContractError("foreign replacement relation")
    if any(item not in references.pending_owner_refs for item in state.pending_work_refs):
        raise ActivityContractError("foreign pending owner reference")
    for preparation in state.source_preparation_refs:
        if preparation.live_source_id not in references.live_source_ids or preparation.final_frontier_ref not in references.frontier_refs:
            raise ActivityContractError("foreign source preparation frontier")
        if any(item is not None and item not in references.receipt_refs for item in (preparation.close_receipt_ref, preparation.absorption_receipt_ref)):
            raise ActivityContractError("foreign source preparation receipt")


def _validate_native_execution_envelope(value: Mapping[str, object]) -> None:
    """Validate mechanics output and its exact owner/evidence joins."""
    if not isinstance(value, Mapping):
        raise ActivityContractError("native execution envelope must be an object")
    resolution_value = value.get("resolution")
    if not isinstance(resolution_value, Mapping):
        raise ActivityContractError("execution Resolution state must be an object")

    # mechanics carries the resolution owner ID alongside the persisted state
    # only when an internal child Resolution ID is needed. The ID belongs to
    # the envelope, not to the persisted runtime.resolution record.
    resolution = dict(resolution_value)
    has_embedded_resolution_id = "resolution_id" in resolution
    embedded_resolution_id = resolution.pop("resolution_id", None)
    if has_embedded_resolution_id:
        _check(embedded_resolution_id, NativeId, "execution Resolution ID")
        if embedded_resolution_id != value.get("resolution_id"):
            raise ActivityContractError("execution Resolution ID differs from its envelope owner")
    normalized = dict(value)
    normalized["resolution"] = resolution
    _wire_contract("native_execution_envelope", normalized)

    resolution_id = value["resolution_id"]
    command_id = value["accepted_command_id"]
    fingerprint = value["accepted_input_fingerprint"]
    segment = value["segment"]
    event = value["event"]
    receipt = value["receipt"]
    if not all(isinstance(item, Mapping) for item in (segment, event, receipt)):
        raise ActivityContractError("execution envelope owner evidence must be objects")
    if (
        not isinstance(fingerprint, str)
        or re.fullmatch(r"[a-f0-9]{64}", fingerprint) is None
    ):
        raise ActivityContractError("execution envelope input fingerprint is not a SHA-256 digest")

    segment_id = segment["segment_id"]
    event_id = value["event_id"]
    segment_event_ids = tuple(segment["event_ids"])
    receipt_event_ids = tuple(receipt["event_ids"])
    event_ordinals: list[int] = []
    event_prefix = f"{segment_id}:event:"
    for member_event_id in segment_event_ids:
        if not isinstance(member_event_id, str) or not member_event_id.startswith(event_prefix):
            raise ActivityContractError("segment event ID is not bound to its stable ordinal")
        ordinal_text = member_event_id.removeprefix(event_prefix)
        if (
            not ordinal_text.isdigit()
            or int(ordinal_text) < 1
            or str(int(ordinal_text)) != ordinal_text
        ):
            raise ActivityContractError("segment event ID has a malformed stable ordinal")
        event_ordinals.append(int(ordinal_text))
    resolution_segments = [
        item
        for item in resolution["segments"]
        if isinstance(item, Mapping) and item.get("segment_id") == segment_id
    ]
    # Closing updates current Resolution/envelope status only; committed
    # segment and receipt statuses remain the historical acceptance values.
    if (
        value["execution_owner_id"] != resolution_id
        or resolution["root_command_id"] != command_id
        or resolution["status"] != value["status"]
        or segment["resulting_execution_state"] != receipt["status"]
        or event["root_command_id"] != command_id
        or event["causal_ref"] != resolution_id
        or event["segment_id"] != segment_id
        or event_id != f"{segment_id}:event:{event['event_ordinal']}"
        or event_id not in segment_event_ids
        or not segment_event_ids
        or event_ordinals != sorted(event_ordinals)
        or len(event_ordinals) != len(set(event_ordinals))
        or receipt_event_ids != segment_event_ids
        or tuple(receipt["segment_refs"]) != (segment_id,)
        or receipt["execution_owner_id"] != resolution_id
        or len(resolution_segments) != 1
        or resolution_segments[0] != segment
    ):
        raise ActivityContractError("execution envelope identities/evidence disagree")


@dataclass(frozen=True, slots=True)
class TemporaryHpSource(ContractValue):
    grant_occurrence_id: NativeId
    source_effect_id: NativeId | None = None


@dataclass(frozen=True, slots=True)
class EntryHealth(ContractValue):
    current: Ordinal
    maximum_base: Ordinal
    maximum_adjustment: int | None = None
    temporary: Ordinal | None = None
    temporary_source: TemporaryHpSource | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.temporary_source is not None and (self.temporary is None or self.temporary <= 0):
            raise ActivityContractError("grant provenance requires positive temporary HP")


@dataclass(frozen=True, slots=True)
class MetricDeadline(ContractValue):
    context_id: NativeId
    anchor_value: Ordinal
    deadline_value: Ordinal
    unit_id: Literal["unit.second", "unit.minute", "unit.hour", "unit.day"]
    basis_id: Literal["temporal.metric_deadline"] = "temporal.metric_deadline"


@dataclass(frozen=True, slots=True)
class ProcedureBoundary(ContractValue):
    boundary_id: NativeId
    procedure_id: NativeId
    anchor_id: NativeId
    subject_id: NativeId | None = None
    offset: Generation | None = None
    basis_id: Literal["temporal.procedure_boundary"] = "temporal.procedure_boundary"


@dataclass(frozen=True, slots=True)
class SemanticBoundary(ContractValue):
    boundary_id: NativeId
    anchor_id: NativeId
    subject_id: NativeId | None = None
    scope_id: NativeId | None = None
    basis_id: Literal["temporal.semantic_boundary"] = "temporal.semantic_boundary"


TemporalBinding = MetricDeadline | ProcedureBoundary | SemanticBoundary


@dataclass(frozen=True, slots=True)
class DeathSaves(ContractValue):
    successes: Ordinal
    failures: Ordinal

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.successes > 2 or self.failures > 2:
            raise ActivityContractError("third death save is a transition, not stored progress")


@dataclass(frozen=True, slots=True)
class DyingProgress(ContractValue):
    death_saves: DeathSaves


@dataclass(frozen=True, slots=True)
class StableProgress(ContractValue):
    recovery_binding: TemporalBinding


@dataclass(frozen=True, slots=True)
class ResourceOwnerRef(ContractValue):
    resource_definition_id: NativeId
    native_owner_ref: NativeOwnerRef
    availability_profile_id: NativeId


@dataclass(frozen=True, slots=True)
class GearEntry(ContractValue):
    asset_id: NativeId
    conversion_membership_ref: NativeId
    entry_equipment_mode: Literal["held", "worn"] | None = None


@dataclass(frozen=True, slots=True)
class EffectDispositionRef(ContractValue):
    effect_id: NativeId
    entry_binding_generation: Generation
    disposition_profile_id: NativeId


@dataclass(frozen=True, slots=True)
class ObjectSuspensionBasis(ContractValue):
    principal_subject_id: NativeId
    activation_occurrence_id: NativeId
    binding_generation: Generation
    rules_context_ref: NativeId
    entry_native_observation_ref: NativeId
    physical_policy_id: Literal["life_policy.dnd2024.character_like", "life_policy.dnd2024.monster_default"]
    entry_life_state_id: Literal["life.active", "life.dying", "life.stable", "life.dead"]
    entry_health: EntryHealth
    resource_owner_refs: tuple[ResourceOwnerRef, ...]
    gear_entries: tuple[GearEntry, ...]
    effect_disposition_refs: tuple[EffectDispositionRef, ...]
    entry_life_state_progress: DyingProgress | StableProgress | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if (self.entry_life_state_id in {"life.dying", "life.stable"}) != (self.entry_life_state_progress is not None):
            raise ActivityContractError("protected zero-state progress must match entry life state")
        if self.entry_life_state_id == "life.dying" and not isinstance(self.entry_life_state_progress, DyingProgress):
            raise ActivityContractError("dying entry requires death-save evidence")
        if self.entry_life_state_id == "life.stable" and not isinstance(self.entry_life_state_progress, StableProgress):
            raise ActivityContractError("stable entry requires absolute recovery binding")


@dataclass(frozen=True, slots=True)
class TypedObjectReturnCause(ContractValue):
    conversion_effect_id: NativeId
    binding_generation: Generation
    ending_occurrence_id: NativeId
    return_reason: Literal["ordinary_end", "dispel", "suppression", "object_destruction", "principal_death"]
    current_object_observation_ref: NativeId
    restoration_basis_ref: NativeId
    return_adjudication_basis_ref: NativeId
    asset_damage_cause_ref: NativeId | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.return_reason != "object_destruction" and self.asset_damage_cause_ref is not None:
            raise ActivityContractError("only actual destruction can reference terminal Asset damage")


@dataclass(frozen=True, slots=True)
class AssetDamageResult(_SealedValue):
    cause_occurrence_id: NativeId
    asset_id: NativeId
    received_damage: Ordinal
    prior_integrity: Ordinal
    final_integrity: Ordinal
    terminal_residual: Ordinal
    damage_instance_id: NativeId
    source_actor_id: NativeId
    damage_type_id: NativeId
    defense_basis_refs: tuple[NativeId, ...]
    fixed_roll_refs: tuple[NativeId, ...]
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if self.final_integrity != max(0, self.prior_integrity - self.received_damage) or self.terminal_residual != max(0, self.received_damage - self.prior_integrity):
            raise ActivityContractError("Asset damage result has invented integrity/residual")


@dataclass(frozen=True, slots=True)
class DamageComponent(ContractValue):
    amount: Ordinal
    damage_type_id: NativeId
    origin_id: NativeId
    bypass_ids: tuple[NativeId, ...] = ()


@dataclass(frozen=True, slots=True)
class TypedHealthCause(ContractValue):
    kind: Literal["damage", "healing", "maximum_change", "instant_death"]
    cause_occurrence_id: NativeId
    principal_subject_id: NativeId
    physical_actor_id: NativeId
    source_actor_id: NativeId
    origin_subject_id: NativeId
    health_policy_id: NativeId
    life_state_policy_id: NativeId
    damage_instance_id: NativeId | None = None
    simultaneous_group_id: NativeId | None = None
    damage_components: tuple[DamageComponent, ...] = ()
    fixed_roll_refs: tuple[NativeId, ...] = ()
    healing_result_ref: NativeId | None = None
    maximum_contribution_ref: NativeId | None = None
    killing_profile_id: NativeId | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.kind == "damage":
            if self.damage_instance_id is None or not self.damage_components:
                raise ActivityContractError("damage requires its instance and typed components")
        elif self.damage_instance_id is not None or self.simultaneous_group_id is not None or self.damage_components:
            raise ActivityContractError("nondamage cause cannot carry damage arithmetic")
        required = {"healing": self.healing_result_ref, "maximum_change": self.maximum_contribution_ref, "instant_death": self.killing_profile_id}
        if self.kind in required and required[self.kind] is None:
            raise ActivityContractError("typed native health cause evidence is missing")
        if any(value is not None for kind, value in required.items() if kind != self.kind):
            raise ActivityContractError("health cause has a foreign branch member")


@dataclass(frozen=True, slots=True)
class TypedEffectEndCause(ContractValue):
    kind: Literal["expiry", "dispel", "dismissal", "support_lost", "rule_transition"]
    cause_occurrence_id: NativeId
    effect_id: NativeId
    source_actor_id: NativeId
    scope_id: NativeId
    reason_id: NativeId


@dataclass(frozen=True, slots=True)
class AttackHitFrontierInput(ContractValue):
    consumer_id: NativeId
    attack_occurrence_id: NativeId
    frontier_id: NativeId
    source_binding: SubjectBinding
    target_binding: SubjectBinding
    attack_result_ref: NativeId
    fixed_roll_refs: tuple[NativeId, ...]
    sensory_exception_basis: OwnerRevisionRef | AcceptedAdjudicationBasis


@dataclass(frozen=True, slots=True)
class CastPreflightInput(ContractValue):
    consumer_id: NativeId
    subject_binding: SubjectBinding
    source_actor_id: NativeId
    origin_subject_id: NativeId
    cost_payer_actor_id: NativeId
    acquisition_binding_ref: NativeId
    component_owner_refs: tuple[NativeOwnerRef, ...]
    target_bindings: tuple[SubjectBinding | ObjectSubjectBinding, ...]
    slot_resource_definition_id: NativeId | None = None
    control_effect_id: NativeId | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)

        def subject_wire(value: SubjectBinding | ObjectSubjectBinding) -> dict[str, object]:
            if isinstance(value, SubjectBinding):
                wire: dict[str, object] = {
                    "principal_subject_id": value.principal_subject_id,
                    "physical_actor_id": value.physical_actor_id,
                    "binding_generation": value.binding_generation,
                }
                for name in ("relation_effect_id", "control_effect_id"):
                    member = getattr(value, name)
                    if member is not None:
                        wire[name] = member
                return wire
            return {
                "principal_subject_id": value.principal_subject_id,
                "object_asset_id": value.object_asset_id,
                "relation_effect_id": value.relation_effect_id,
                "binding_generation": value.binding_generation,
            }

        wire: dict[str, object] = {
            "consumer_id": self.consumer_id,
            "subject_binding": subject_wire(self.subject_binding),
            "source_actor_id": self.source_actor_id,
            "origin_subject_id": self.origin_subject_id,
            "cost_payer_actor_id": self.cost_payer_actor_id,
            "acquisition_binding_ref": self.acquisition_binding_ref,
            "component_owner_refs": tuple(
                {"family_key": owner.family_key, "identity": owner.identity}
                for owner in self.component_owner_refs
            ),
            "target_bindings": tuple(
                subject_wire(binding) for binding in self.target_bindings
            ),
        }
        if self.slot_resource_definition_id is not None:
            wire["slot_resource_definition_id"] = self.slot_resource_definition_id
        if self.control_effect_id is not None:
            wire["control_effect_id"] = self.control_effect_id
        _wire_contract("cast_preflight_input", wire)


@dataclass(frozen=True, slots=True)
class CastTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    preflight: CastPreflightInput
    phase: Literal["START", "COMPLETE", "INTERRUPT", "COUNTERED", "INVALID_TARGET"]


@dataclass(frozen=True, slots=True)
class CastingProcedureTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    procedure_id: NativeId
    execution_ref: CastExecutionRef
    phase: Literal["START", "MAGIC_ACTION", "COMPLETE", "INTERRUPT", "COUNTERED"]
    temporal_binding_ref: NativeId
    participant_owner_refs: tuple[NativeOwnerRef, ...]


@dataclass(frozen=True, slots=True)
class ClosureTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    execution_ref: ExecutionRef
    mandatory_child_receipts: tuple[ReceiptRef, ...]


@dataclass(frozen=True, slots=True)
class StochasticTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    state: StochasticState
    fixed_roll_refs: tuple[RollRef, ...]


@dataclass(frozen=True, slots=True)
class ConcentrationTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    subject_binding: SubjectBinding
    concentration_effect_id: NativeId
    phase: Literal["START", "REPLACE", "DAMAGE_SAVE", "LOSS", "DISMISS"]
    cause: TypedHealthCause | TypedEffectEndCause | None = None


@dataclass(frozen=True, slots=True)
class SpellProgressTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    owner_ref: NativeOwnerRef
    progress_definition_id: NativeId
    profile_id: Literal["lifecycle.progress.turn_gate", "lifecycle.progress.rest_gate", "lifecycle.progress.day_gate", "lifecycle.progress.progressive_save", "lifecycle.progress.maturity", "lifecycle.progress.repeated_place", "lifecycle.progress.observable_release"]
    boundary_occurrence_ref: NativeId


@dataclass(frozen=True, slots=True)
class FormTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    subject_binding: SubjectBinding
    profile_id: Literal["lifecycle.form.polymorph", "lifecycle.form.shapechange", "lifecycle.form.true_polymorph_creature"]
    phase: Literal["START", "CHANGE", "SUPPRESS", "RESUME", "END"]
    form_archetype_id: NativeId
    gear_choice_ref: AcceptedChoiceRef | None = None


@dataclass(frozen=True, slots=True)
class ActorConstructionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.actor.unseen_servant", "lifecycle.actor.familiar", "lifecycle.actor.steed", "lifecycle.actor.summon"]
    principal_subject_id: NativeId
    archetype_id: NativeId
    construction_basis_ref: NativeId
    source_effect_id: NativeId


@dataclass(frozen=True, slots=True)
class IdentityTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.identity.magic_jar", "lifecycle.identity.astral_projection", "lifecycle.identity.clone", "lifecycle.identity.simulacrum"]
    principal_subject_id: NativeId
    relation_effect_id: NativeId
    relation_generation: Generation
    transition_basis_ref: NativeId
    participant_owner_refs: tuple[NativeOwnerRef, ...]


@dataclass(frozen=True, slots=True)
class ConversionTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.conversion.animate_objects", "lifecycle.conversion.true_polymorph_object_creature", "lifecycle.conversion.true_polymorph_creature_object"]
    subject_binding: SubjectBinding | ObjectSubjectBinding
    relation_effect_id: NativeId
    phase: Literal["START", "PERSIST", "RETURN", "SUPPRESS", "RESUME", "END"]
    return_cause: TypedObjectReturnCause | None = None


@dataclass(frozen=True, slots=True)
class SpatialTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.spatial.zone", "lifecycle.spatial.movement", "lifecycle.spatial.portal"]
    source_owner_refs: tuple[NativeOwnerRef, ...]
    destination_owner_refs: tuple[NativeOwnerRef, ...]
    placement_basis_ref: NativeId
    roster_basis_ref: NativeId
    movement_fact_ref: NativeId | None = None


@dataclass(frozen=True, slots=True)
class ControlTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.control.command", "lifecycle.control.domination_reaction", "lifecycle.control.enclosure_reaction"]
    controller_binding: SubjectBinding
    performer_binding: SubjectBinding
    cost_payer_owner_refs: tuple[NativeOwnerRef, ...]
    accepted_command_ref: NativeId


@dataclass(frozen=True, slots=True)
class InformationTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    profile_id: Literal["lifecycle.information.sensory_link", "lifecycle.information.divination", "lifecycle.information.corpse_answers", "lifecycle.information.illusion_recognition", "lifecycle.information.memory_change"]
    principal_subject_id: NativeId
    recipient_subject_ids: tuple[NativeId, ...]
    scope_basis_ref: NativeId
    source_owner_refs: tuple[NativeOwnerRef, ...]
    accepted_content_basis: AcceptedAdjudicationBasis | None = None


@dataclass(frozen=True, slots=True)
class ReconciliationDependencyEdge(ContractValue):
    edge_id: NativeId
    cause_roll_ref: RollRef
    consumer_id: NativeId
    consequence_owner_ref: NativeOwnerRef
    classification: Literal["INVALIDATE", "RECOMPUTE", "PRESERVE", "RECONCILE"]
    before_revision: OwnerRevisionRef
    after_revision: OwnerRevisionRef
    basis_ref: NativeId


@dataclass(frozen=True, slots=True)
class RecentRollWitness(ContractValue):
    witness_id: NativeId
    roll_ref: RollRef
    segment_ref: NativeId
    activity_id: NativeId
    mode_id: NativeId
    catalog_context: BoundCatalogContext
    accepted_input_refs: tuple[NativeId, ...]
    fixed_raw_draws: tuple[int, ...]
    interpretation_ref: NativeId
    dependency_edges: tuple[ReconciliationDependencyEdge, ...]


@dataclass(frozen=True, slots=True)
class AcceptedWishRetentionFrontier(ContractValue):
    procedure_id: NativeId
    boundary_occurrence_ref: NativeId
    chronology_bridge_ref: NativeId
    owner_revision_refs: tuple[OwnerRevisionRef, ...]


@dataclass(frozen=True, slots=True)
class WitnessRetentionPlan(ContractValue):
    frontier: AcceptedWishRetentionFrontier
    protected_witness_ids: tuple[NativeId, ...]
    expired_witness_ids: tuple[NativeId, ...]
    pending_execution_refs: tuple[ExecutionRef, ...]


@dataclass(frozen=True, slots=True)
class WishRollRedoRequest(ContractValue):
    consumer_id: NativeId
    target_roll_ref: RollRef
    reroll_mode: Literal["NORMAL", "ADVANTAGE", "DISADVANTAGE"]
    initiation_frontier: WishInitiationFrontier


@dataclass(frozen=True, slots=True)
class WishRecentBasis(ContractValue):
    witness: RecentRollWitness
    retention_frontier: AcceptedWishRetentionFrontier
    closure_evidence_refs: tuple[OwnerRevisionRef, ...]


@dataclass(frozen=True, slots=True)
class WishTransitionInput(ContractValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    state: WishReconciliationState
    recent_basis: WishRecentBasis


@dataclass(frozen=True, slots=True)
class WishSourcePreparationPlan(ContractValue):
    wish_execution_ref: CastExecutionRef
    required_live_source_ids: tuple[NativeId, ...]
    accepted_preparation_receipts: tuple[WishSourcePreparationReceipt, ...]
    target_owner_ref: NativeOwnerRef


@dataclass(frozen=True, slots=True)
class WishReplacementRelation(ContractValue):
    relation_id: NativeId
    wish_event_id: NativeId
    target_roll_ref: RollRef
    selected_basis: Literal["ORIGINAL", "REROLL"]
    old_consequence_refs: tuple[NativeId, ...]
    current_consequence_refs: tuple[NativeId, ...]
    reconciliation_receipt_ref: ReceiptRef


@dataclass(frozen=True, slots=True)
class ConsequenceValidityProjection(ContractValue):
    consequence_ref: NativeId
    validity: Literal["CURRENT", "REPLACED", "PRESERVED"]
    replacement_relation_ref: NativeId


NativeTransitionInput = (
    TypedHealthCause | TypedEffectEndCause | CastTransitionInput | CastingProcedureTransitionInput
    | ClosureTransitionInput | StochasticTransitionInput | ConcentrationTransitionInput
    | SpellProgressTransitionInput | FormTransitionInput | ActorConstructionInput
    | IdentityTransitionInput | ConversionTransitionInput | SpatialTransitionInput
    | ControlTransitionInput | InformationTransitionInput | WishTransitionInput
)


@dataclass(frozen=True, slots=True)
class TurnGateProgress(ContractValue):
    turn_occurrence_key: NativeId
    consumed: bool
    profile_id: Literal["lifecycle.progress.turn_gate"] = "lifecycle.progress.turn_gate"


@dataclass(frozen=True, slots=True)
class RestGateProgress(ContractValue):
    consumed: bool
    reset_boundary_id: NativeId
    last_transition_occurrence: NativeId
    profile_id: Literal["lifecycle.progress.rest_gate"] = "lifecycle.progress.rest_gate"


@dataclass(frozen=True, slots=True)
class DayGateProgress(ContractValue):
    window_ref: NativeId
    count: Ordinal
    last_transition_occurrence: NativeId
    profile_id: Literal["lifecycle.progress.day_gate"] = "lifecycle.progress.day_gate"


@dataclass(frozen=True, slots=True)
class ProgressiveSaveProgress(ContractValue):
    phase: Literal["testing", "established"]
    successes: Ordinal
    failures: Ordinal
    last_transition_occurrence: NativeId
    profile_id: Literal["lifecycle.progress.progressive_save"] = "lifecycle.progress.progressive_save"

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        if self.successes > 2 or self.failures > 2:
            raise ActivityContractError("terminal threshold is not stored as testing progress")


@dataclass(frozen=True, slots=True)
class MaturityProgress(ContractValue):
    phase: Literal["growing", "ready", "consumed", "invalid"]
    maturity_occurrence_ref: NativeId
    profile_id: Literal["lifecycle.progress.maturity"] = "lifecycle.progress.maturity"


@dataclass(frozen=True, slots=True)
class RepeatedPlaceProgress(ContractValue):
    series_key: NativeId
    qualifying_count: Ordinal
    last_qualifying_period_ref: NativeId
    last_transition_occurrence: NativeId
    profile_id: Literal["lifecycle.progress.repeated_place"] = "lifecycle.progress.repeated_place"


@dataclass(frozen=True, slots=True)
class ObservableReleaseProgress(ContractValue):
    predicate_id: NativeId
    accepted_predicate_basis_ref: NativeId
    enrollment_generation: Generation
    phase: Literal["armed", "claimed", "released"]
    profile_id: Literal["lifecycle.progress.observable_release"] = "lifecycle.progress.observable_release"


SpellProgress = TurnGateProgress | RestGateProgress | DayGateProgress | ProgressiveSaveProgress | MaturityProgress | RepeatedPlaceProgress | ObservableReleaseProgress


def validate_spell_progress(value: Mapping[str, object]) -> SpellProgress:
    """Validate the finite native value only; no owner/transition permission."""
    classes = {
        "lifecycle.progress.turn_gate": TurnGateProgress,
        "lifecycle.progress.rest_gate": RestGateProgress,
        "lifecycle.progress.day_gate": DayGateProgress,
        "lifecycle.progress.progressive_save": ProgressiveSaveProgress,
        "lifecycle.progress.maturity": MaturityProgress,
        "lifecycle.progress.repeated_place": RepeatedPlaceProgress,
        "lifecycle.progress.observable_release": ObservableReleaseProgress,
    }
    profile = value.get("profile_id")
    if not isinstance(profile, str) or profile not in classes:
        raise ActivityContractError("unknown progress profile")
    try:
        return classes[profile](**value)
    except TypeError as exc:
        raise ActivityContractError("progress has missing/foreign fields") from exc


def _compiled_instruction_wire(value: CompiledInstruction) -> dict[str, object]:
    return {
        "consumer_id": value.consumer_id,
        "primitive_id": value.primitive_id,
        "arguments": value.arguments,
        "result_contract_refs": value.result_contract_refs,
        "read_contract_refs": value.read_contract_refs,
        "children": tuple(_compiled_instruction_wire(child) for child in value.children),
        "guard": value.guard,
        "result_contracts": value.result_contracts,
        "scope_bindings": value.scope_bindings,
        "export_name": value.export_name,
    }


@dataclass(frozen=True, slots=True)
class CompiledInstruction(ContractValue):
    consumer_id: NativeId
    primitive_id: NativeId
    arguments: Mapping[str, object]
    result_contract_refs: tuple[NativeId, ...]
    read_contract_refs: tuple[NativeId, ...]
    children: tuple[CompiledInstruction, ...] = ()
    guard: Mapping[str, object] | None = None
    result_contracts: Mapping[str, object] = field(default_factory=dict)
    scope_bindings: Mapping[str, object] = field(default_factory=dict)
    export_name: str | None = None

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        _wire_contract("compiled_instruction", _compiled_instruction_wire(self))


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CompiledActivity(_SealedValue):
    activity_id: NativeId
    definition_semantic_hash: str
    definition_semantic_hash_generation: Generation
    ruleset_set_sha256: str
    ruleset_set_digest_generation: Literal[1]
    catalog_context_fingerprint: str
    catalog_context_fingerprint_generation: Literal[1]
    compiler_generation: Generation
    engine_contract_inventory_sha256: str
    mode_policy_profile_id: NativeId
    instructions: tuple[CompiledInstruction, ...]
    parameter_contracts: Mapping[str, object]
    role_contracts: Mapping[str, object]
    export_contracts: Mapping[str, object]
    consumer_read_plan: tuple[NativeId, ...]
    dependency_ids: tuple[NativeId, ...]
    cost_contract_refs: tuple[NativeId, ...]
    native_transition_contract_refs: tuple[NativeId, ...]
    timing_contract_refs: tuple[NativeId, ...]
    profile_bindings: tuple[ProfileBinding, ...]
    safe_recompute_phases: tuple[NativeId, ...]
    requirements: Mapping[str, object] | None = None
    activation_contract: Mapping[str, object] | None = None
    cost_contracts: tuple[Mapping[str, object], ...] = ()
    duration_contract: Mapping[str, object] | None = None
    targeting_contract: Mapping[str, object] | None = None
    symbol_contracts: Mapping[str, object] = field(default_factory=dict)
    calculation_policy_bindings: tuple[CompiledCalculationPolicy, ...] = ()
    cast_profile_bindings: tuple[CastProfileBinding, ...] = ()
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if not self.instructions:
            raise ActivityContractError("compiled Activity requires a finite instruction tree")
        _wire_contract("parameters", self.parameter_contracts)
        _wire_contract("roles", self.role_contracts)
        _wire_contract("export_contracts", self.export_contracts)
        _wire_contract("compiler_symbol_contracts", self.symbol_contracts)
        for policy in self.calculation_policy_bindings:
            if not isinstance(policy, CompiledCalculationPolicy):
                raise ActivityContractError("compiled calculation policy is untyped")
        for binding in self.cast_profile_bindings:
            if not isinstance(binding, CastProfileBinding):
                raise ActivityContractError("compiled cast profile is untyped")
        for name, value in (("mechanical-predicate", self.requirements),
                            ("duration-spec", self.duration_contract),
                            ("target-spec", self.targeting_contract)):
            if value is not None:
                _wire_contract(name, value)
        if self.activation_contract is not None:
            _wire_contract("https://hedgelion.invalid/schemas/activity-definition-data.schema.json#/$defs/activation", self.activation_contract)
        for cost in self.cost_contracts:
            _wire_contract("cost-spec", cost)
        pending, consumers = list(self.instructions), set()
        while pending:
            instruction = pending.pop()
            if instruction.consumer_id in consumers:
                raise ActivityContractError("duplicate instruction occurrence")
            consumers.add(instruction.consumer_id)
            pending.extend(instruction.children)
        if any(binding.consumer_id not in consumers for binding in self.profile_bindings):
            raise ActivityContractError("profile binding references a foreign instruction occurrence")
        policy_keys: set[tuple[str, str]] = set()
        profile_keys = {
            (binding.consumer_id, binding.profile_id, binding.profile_generation)
            for binding in self.profile_bindings
        }
        for policy in self.calculation_policy_bindings:
            binding = policy.binding
            key = (binding.consumer_id, binding.profile_id)
            if key in policy_keys or binding.consumer_id not in consumers:
                raise ActivityContractError("calculation policy references a duplicate/foreign occurrence")
            if (binding.consumer_id, binding.profile_id, binding.profile_generation) not in profile_keys:
                raise ActivityContractError("calculation policy has no exact profile binding")
            if any(
                self.role_contracts.get(role_name) != role_contract
                for role_name, role_contract in policy.role_contracts.items()
            ):
                raise ActivityContractError("calculation policy role contract differs from the compiled Activity")
            policy_keys.add(key)
        cast_keys: set[tuple[str, str]] = set()
        for binding in self.cast_profile_bindings:
            key = (binding.consumer_id, binding.profile_id)
            if key in cast_keys or binding.consumer_id not in consumers:
                raise ActivityContractError("cast profile references a duplicate/foreign occurrence")
            if (binding.consumer_id, binding.profile_id, binding.profile_generation) not in profile_keys:
                raise ActivityContractError("cast profile has no exact profile binding")
            cast_keys.add(key)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class AdmittedActivityCatalog(_SealedValue):
    catalog_context: BoundCatalogContext
    frozen_semantic_members: Mapping[tuple[str, str], bytes]
    frozen_definitions: Mapping[str, object]
    engine_contract_inventory: Mapping[str, object]
    compiler_generation: Generation
    mode_policy_profile_id: NativeId
    compiled_activities: Mapping[str, CompiledActivity]
    alias_index: Mapping[str, tuple[NativeId, ...]]
    capability_index: Mapping[str, tuple[NativeId, ...]]
    card_index: Mapping[str, object]
    unavailable_activity_reasons: Mapping[str, str] = field(default_factory=dict)
    definition_dependency_graph: Mapping[str, tuple[NativeId, ...]] = field(default_factory=dict)
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if not self.catalog_context._is_admitted():
            raise ActivityContractError("catalog requires an admitted source context")
        if self.engine_contract_inventory != self.catalog_context.basis["engine_contract_inventory"]:
            raise ActivityContractError("catalog inventory differs from its admitted context")
        for identity, definition in self.frozen_definitions.items():
            _wire_contract("catalog-definition", definition)
            if definition["id"] != identity:
                raise ActivityContractError("definition map key differs from its closed source envelope")
        for identity, card in self.card_index.items():
            _wire_contract("capability_card", card)
            if card["definition_id"] != identity:
                raise ActivityContractError("card map key differs from its definition")
        _wire_contract(
            "activity_unavailable_reasons", self.unavailable_activity_reasons
        )
        _wire_contract("definition_dependency_graph", self.definition_dependency_graph)
        if self.definition_dependency_graph and (
            set(self.definition_dependency_graph) != set(self.frozen_definitions)
            or any(reference not in self.frozen_definitions
                for references in self.definition_dependency_graph.values() for reference in references)
        ):
            raise ActivityContractError("definition dependency graph differs from its frozen source set")
        if any(
            identity not in self.frozen_definitions
            or self.frozen_definitions[identity]["kind"] != "definition.activity"
            for identity in self.unavailable_activity_reasons
        ):
            raise ActivityContractError(
                "unavailable Activity diagnostics reference a foreign definition"
            )


@dataclass(frozen=True, slots=True)
class NativeAllocationHandle(_SealedValue):
    owner_ref: NativeOwnerRef
    occurrence_id: NativeId
    local_key: NativeId
    _builder_token: object = field(repr=False, compare=False)
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)


@dataclass(frozen=True, slots=True)
class MandatoryWorkDescriptor(ContractValue):
    occurrence_id: NativeId
    activity_id: NativeId
    expected_resolution_id: NativeId
    source_owner_ref: NativeOwnerRef


@dataclass(frozen=True, slots=True)
class PlannedEventBasis(ContractValue):
    stable_ordinal: Generation
    event_kind_id: NativeId
    cause_occurrence_id: NativeId
    transition_refs: tuple[NativeId, ...]


@dataclass(frozen=True, slots=True)
class NativePreparationContext(_SealedValue):
    catalog: AdmittedActivityCatalog
    compiled: CompiledActivity
    consumer_id: NativeId
    occurrence_id: NativeId
    execution_ref: ExecutionRef
    observation: CurrentOwnerObservation
    owner_session: CurrentOwnerReadSession
    role_bindings: Mapping[str, NativeOwnerRef]
    accepted_command: Mapping[str, object]
    resolution: Mapping[str, object]
    accepted_fact_refs: tuple[NativeId, ...]
    accepted_adjudication: tuple[AcceptedAdjudicationBasis, ...]
    policy_refs: tuple[NativeId, ...]
    fixed_roll_refs: tuple[RollRef, ...]
    prospective_owner_documents: tuple[OwnerDocument, ...]
    allocation_handles: tuple[NativeAllocationHandle, ...]
    _builder_token: object = field(repr=False, compare=False)
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if (
            not _compiler_value_is_issued(self.catalog, kind="catalog")
            or not _compiler_value_is_issued(
                self.compiled,
                kind="compiled",
                parent=self.catalog.catalog_context,
            )
            or self.catalog.compiled_activities.get(self.compiled.activity_id)
            is not self.compiled
        ):
            raise ActivityContractError(
                "preparation requires exact compiler-issued catalog and Activity"
            )
        _wire_contract("runtime-command-state", self.accepted_command)
        _wire_contract("runtime-resolution-state", self.resolution)
        if self._builder_token is None or self.compiled.catalog_context_fingerprint != self.catalog.catalog_context.fingerprint:
            raise ActivityContractError("context is not bound to its builder/catalog")
        if self.owner_session._operation_token is not self.observation.operation_token:
            raise ActivityContractError("context observation belongs to another owner session")
        pending, consumers = list(self.compiled.instructions), set()
        while pending:
            instruction = pending.pop()
            consumers.add(instruction.consumer_id)
            pending.extend(instruction.children)
        if self.consumer_id not in consumers or set(self.role_bindings) - set(self.compiled.role_contracts):
            raise ActivityContractError("context has a foreign instruction or role")
        for role, contract in self.compiled.role_contracts.items():
            if contract["required"] and role not in self.role_bindings:
                raise ActivityContractError("missing required native role")
            if role in self.role_bindings and self.role_bindings[role].family_key != contract["family_key"]:
                raise ActivityContractError("native role has the wrong owner family")
        if self.accepted_command["command_id"] != self.execution_ref.command_id or self.resolution["root_command_id"] != self.execution_ref.command_id:
            raise ActivityContractError("context execution references do not match accepted owners")
        if self.resolution["activity_id"] != self.compiled.activity_id:
            raise ActivityContractError("Resolution belongs to another Activity")
        if self.accepted_command["command_kind"] == "action":
            request = self.accepted_command["action_request"]
            root_resolution_id = self.accepted_command["root_resolution_id"]
            if self.execution_ref.resolution_id == root_resolution_id:
                if (
                    request["activity_id"] != self.compiled.activity_id
                    or request["actor_id"] != self.resolution["actor_id"]
                    or self.resolution.get("initiating_command_id")
                    != self.execution_ref.command_id
                ):
                    raise ActivityContractError("root command/Resolution invocation bindings disagree")
            else:
                causal_invocation_key = self.resolution.get("causal_invocation_key")
                if not isinstance(causal_invocation_key, str) or not causal_invocation_key:
                    raise ActivityContractError("child Resolution requires its causal invocation key")
                initiating_command_id = self.resolution.get("initiating_command_id")
                if initiating_command_id is not None and initiating_command_id != self.execution_ref.command_id:
                    raise ActivityContractError("child Resolution has a foreign initiating command")
                actor_id = self.resolution["actor_id"]
                if not any(
                    owner_ref.family_key == "world.actor" and owner_ref.identity == (actor_id,)
                    for owner_ref in self.role_bindings.values()
                ):
                    raise ActivityContractError("child Resolution Actor has no exact native role binding")
        if any(handle._builder_token is not self._builder_token for handle in self.allocation_handles):
            raise ActivityContractError("foreign allocation handle")
        for owner_ref in self.role_bindings.values():
            self.observation.require(owner_ref)


@dataclass(frozen=True, slots=True)
class PreparedNativeFragment(_SealedValue):
    consumer_id: NativeId
    occurrence_id: NativeId
    observation_fingerprint: str
    transitions: tuple[NativeTransitionInput, ...]
    read_refs: tuple[NativeOwnerRef, ...]
    exports: Mapping[str, object]
    event_basis_refs: tuple[NativeId, ...]
    mandatory_work: tuple[MandatoryWorkDescriptor, ...]
    _builder_token: object = field(repr=False, compare=False)
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if self._builder_token is None:
            raise ActivityContractError("fragment has no issuing builder")
        _wire_contract("fragment_exports", self.exports)


@dataclass(slots=True)
class NativePreparationHold(Exception, ContractValue):
    operation_status: Literal["REVALIDATION_REQUIRED", "CAPACITY_REQUIRED", "AUTHORITY_UNAVAILABLE"]
    execution_ref: ExecutionRef
    continuity_refs: tuple[NativeId, ...]

    def __post_init__(self) -> None:
        ContractValue.__post_init__(self)
        Exception.__init__(self, self.operation_status, self.execution_ref, self.continuity_refs)


@dataclass(frozen=True, slots=True)
class NativeSegmentPlan(_SealedValue):
    campaign_id: NativeId
    execution_ref: ExecutionRef
    input_fingerprint: str
    root_command_id: NativeId
    segment_id: NativeId
    catalog: AdmittedActivityCatalog
    compiled: CompiledActivity
    observation: CurrentOwnerObservation
    owner_documents: tuple[OwnerDocument, ...]
    document_profile_bindings: tuple[ProfileBinding, ...]
    fixed_roll_refs: tuple[RollRef, ...]
    fixed_roll_results: tuple[Mapping[str, object], ...]
    future_rng_frontier: str
    runtime_owner_documents: tuple[OwnerDocument, ...]
    event_basis_refs: tuple[NativeId, ...]
    event_batch: tuple[PlannedEventBasis, ...]
    receipt_exports: Mapping[str, object]
    mandatory_work: tuple[MandatoryWorkDescriptor, ...]
    owner_generation_refs: tuple[OwnerRevisionRef, ...]
    dirty_owner_refs: tuple[NativeOwnerRef, ...]
    _operation_token: object = field(repr=False, compare=False)
    _builder_token: object = field(repr=False, compare=False)
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        if self._operation_token is not self.observation.operation_token or self._builder_token is None:
            raise ActivityContractError("plan is foreign to its native observation/builder")
        _wire_contract("exports", self.receipt_exports)
        for result in self.fixed_roll_results:
            _wire_contract("roll-result", result)


@dataclass(frozen=True, slots=True)
class NativeSegmentEstablishment(_SealedValue):
    status: Literal["ESTABLISHED", "REPLAY", "REVALIDATION_REQUIRED", "CAPACITY_REQUIRED", "AUTHORITY_UNAVAILABLE", "INDETERMINATE"]
    campaign_id: NativeId
    execution_ref: ExecutionRef
    input_fingerprint: str
    segment_id: NativeId
    accepted_owner_revisions: tuple[OwnerRevisionRef, ...]
    current_native_source_proof: tuple[OwnerRevisionRef, ...]
    pending_continuity_refs: tuple[NativeId, ...]
    accepted_execution: Mapping[str, object] | None = None
    receipt: Mapping[str, object] | None = None
    dispatched_attempt_ref: NativeId | None = None
    _issue_seal: object = field(default=None, repr=False, compare=False, kw_only=True)

    def __post_init__(self) -> None:
        _SealedValue.__post_init__(self)
        accepted = self.status in {"ESTABLISHED", "REPLAY"}
        if accepted != (self.accepted_execution is not None) or accepted != (self.receipt is not None):
            raise ActivityContractError("hold/accepted establishment evidence is mixed")
        if not accepted and self.accepted_owner_revisions:
            raise ActivityContractError("a hold cannot claim newly accepted owner revisions")
        if self.status == "INDETERMINATE" and self.dispatched_attempt_ref is None:
            raise ActivityContractError("indeterminate dispatch requires its exact attempt")
        if self.accepted_execution is not None:
            _validate_native_execution_envelope(self.accepted_execution)
            if (
                self.accepted_execution["accepted_command_id"] != self.execution_ref.command_id
                or self.accepted_execution["resolution_id"] != self.execution_ref.resolution_id
                or self.accepted_execution["accepted_input_fingerprint"] != self.input_fingerprint
                or self.accepted_execution["segment"]["segment_id"] != self.segment_id
            ):
                raise ActivityContractError("execution envelope differs from establishment identity")
            _wire_contract("resolution-receipt", self.receipt)
            if self.receipt != self.accepted_execution["receipt"]:
                raise ActivityContractError("establishment receipt differs from execution envelope")


def validate_spell_capabilities(
    value: Mapping[str, object], *, supported_srd_ids: tuple[str, ...],
    existing_extra_ids: tuple[str, ...], mode_bindings: tuple[tuple[str, str, str], ...],
) -> None:
    """Relational projection check against exact supplied proved inputs; no grant."""
    expected = {"schema_version", "identity_source", "profile_id", "content_basis", "coverage_stage", "supported_srd_spell_ids", "existing_extra_spell_ids", "mode_bindings", "unsupported_content_policy", "notice"}
    if not isinstance(value, Mapping) or set(value) != expected or value["schema_version"] != 1 or type(value["schema_version"]) is not int:
        raise ActivityContractError("capability projection has unexpected fields/schema")
    literals = {"identity_source": "ruleset-package-manifest.json", "profile_id": "spell.srd52.local", "content_basis": "SRD_5_2_1", "unsupported_content_policy": "ABSENT_NONSELECTABLE", "notice": "NOTICE.md"}
    if any(value[key] != literal for key, literal in literals.items()) or not isinstance(value["coverage_stage"], str) or value["coverage_stage"] not in {"PARTIAL", "MECHANICALLY_COMPLETE"}:
        raise ActivityContractError("capability projection has foreign semantics")
    rosters = []
    for key, supplied in (("supported_srd_spell_ids", supported_srd_ids), ("existing_extra_spell_ids", existing_extra_ids)):
        actual = value[key]
        if not isinstance(actual, (tuple, list)) or any(not isinstance(item, str) or not item.startswith("spell.") or _ID.fullmatch(item) is None for item in actual):
            raise ActivityContractError("invalid spell roster")
        if list(actual) != sorted(set(actual)) or tuple(actual) != supplied:
            raise ActivityContractError("spell roster is unsorted/duplicate/foreign")
        rosters.append(set(actual))
    if rosters[0] & rosters[1]:
        raise ActivityContractError("SRD and existing-extra rosters must be disjoint")
    actual_modes = value["mode_bindings"]
    if not isinstance(actual_modes, (tuple, list)):
        raise ActivityContractError("mode bindings must be a finite array")
    normalized = []
    for row in actual_modes:
        if not isinstance(row, Mapping) or set(row) != {"spell_id", "mode_id", "activity_id"}:
            raise ActivityContractError("mode binding is not closed")
        for item in row.values():
            _check(item, NativeId, "mode reference")
        if not row["activity_id"].startswith("activity."):
            raise ActivityContractError("mode binding requires an exact Activity definition")
        normalized.append((row["spell_id"], row["mode_id"], row["activity_id"]))
    if normalized != sorted(set(normalized)) or tuple(normalized) != mode_bindings:
        raise ActivityContractError("mode roster is unsorted/duplicate/foreign")
    if len({(row[0], row[1]) for row in normalized}) != len(normalized):
        raise ActivityContractError("one spell mode cannot bind two Activities")
    if {row[0] for row in normalized} != rosters[0] | rosters[1]:
        raise ActivityContractError("spell/mode roster mismatch")
    if value["coverage_stage"] == "MECHANICALLY_COMPLETE" and len(rosters[0]) != 339:
        raise ActivityContractError("full coverage requires the exact proved SRD roster")


def validate_geometry_membership(
    value: Mapping[str, object], *, neighbor_predicate: Literal["NONE", "EACH_HAS_NEIGHBOR", "CONNECTED"],
) -> None:
    """Check finite local keys after shape validation, not native/source admission.

    The caller here is the compiled profile consumer, not a gameplay surface.
    Choosing a predicate does not authorize geometry or widen a source rule.
    """
    if not isinstance(neighbor_predicate, str) or neighbor_predicate not in {"NONE", "EACH_HAS_NEIGHBOR", "CONNECTED"}:
        raise ActivityContractError("unknown geometry predicate")
    kind = value.get("kind")
    if not isinstance(kind, str) or kind not in {"cube_group", "wall_panels"}:
        raise ActivityContractError("membership predicate requires a finite cube/panel group")
    member_field, key_field = ("cells", "cell_key") if kind == "cube_group" else ("panels", "panel_key")
    members = value.get(member_field)
    pairs = value.get("adjacent_pairs")
    if not isinstance(members, (tuple, list)) or not members or not isinstance(pairs, (tuple, list)):
        raise ActivityContractError("geometry member/edge arrays are missing")
    keys: list[str] = []
    for member in members:
        if not isinstance(member, Mapping):
            raise ActivityContractError("geometry member is not a closed record")
        key = member.get(key_field)
        _check(key, NativeId, "geometry member key")
        keys.append(key)
    if len(keys) != len(set(keys)):
        raise ActivityContractError("duplicate geometry member key")
    graph = {key: set() for key in keys}
    seen: set[frozenset[str]] = set()
    left_key, right_key = ("left_cell_key", "right_cell_key") if kind == "cube_group" else ("left_panel_key", "right_panel_key")
    for pair in pairs:
        if not isinstance(pair, Mapping) or set(pair) != {left_key, right_key}:
            raise ActivityContractError("geometry edge is not closed")
        left, right = pair[left_key], pair[right_key]
        _check(left, NativeId, "geometry edge")
        _check(right, NativeId, "geometry edge")
        edge = frozenset((left, right))
        if left not in graph or right not in graph or left == right or edge in seen:
            raise ActivityContractError("foreign/self/duplicate geometry edge")
        seen.add(edge)
        graph[left].add(right)
        graph[right].add(left)
    if neighbor_predicate == "EACH_HAS_NEIGHBOR" and any(not neighbors for neighbors in graph.values()):
        raise ActivityContractError("source requires each member to have a neighbor")
    if neighbor_predicate == "CONNECTED":
        visited, pending = set(), [keys[0]]
        while pending:
            key = pending.pop()
            if key not in visited:
                visited.add(key)
                pending.extend(graph[key] - visited)
        if visited != set(keys):
            raise ActivityContractError("source requires one connected component")
