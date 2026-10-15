"""Bounded Sorcerer1 source preparation; no cast or mutation authority."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, Literal, NoReturn

from . import activity_contracts as contracts
from . import mechanical_context, mechanical_sources
from .current_owner import CurrentOwnerStatus, NativeOwnerRef

# framework_module_version: 1.0.4
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.4"

_CLASS_ID: Final[str] = "class.sorcerer"
_ADVANCEMENT_ID: Final[str] = "advancement.sorcerer.mvp_1"
_SPELLCASTING_FEATURE_ID: Final[str] = "feature.sorcerer.spellcasting"
_INNATE_SORCERY_FEATURE_ID: Final[str] = "feature.sorcerer.innate_sorcery"
_INNATE_SORCERY_EFFECT_ID: Final[str] = "effect.innate_sorcery"
_CANTRIP_SLOT_ID: Final[str] = "advancement.sorcerer.level_1.cantrips"
_PREPARED_SLOT_ID: Final[str] = "advancement.sorcerer.level_1.prepared_spells"
_SOURCE_ABILITY_ID: Final[str] = "ability.charisma"
_FORM_STATE_ACTOR_REFERENCE_FIELDS: Final[tuple[str, ...]] = ()
_EFFECT_DIRECT_ACTOR_REFERENCE_FIELDS: Final[tuple[str, str]] = (
    "target_id",
    "source_id",
)
_SUBJECT_BINDING_ACTOR_REFERENCE_FIELDS: Final[tuple[str, str]] = (
    "principal_subject_id",
    "physical_actor_id",
)
_IDENTITY_ACTOR_REFERENCE_FIELDS_BY_PROFILE: Final = (
    (
        "lifecycle.identity.magic_jar",
        (
            "principal_subject_id",
            "original_body_actor_id",
            "host_body_actor_id",
            "displaced_principal_subject_id",
            "active_body_actor_id",
        ),
    ),
    (
        "lifecycle.identity.astral_projection",
        (
            "principal_subject_id",
            "original_body_actor_id",
            "astral_proxy_actor_id",
        ),
    ),
    ("lifecycle.identity.clone", ("principal_subject_id",)),
    (
        "lifecycle.identity.simulacrum",
        ("principal_subject_id", "replica_actor_id"),
    ),
)
_CONTROL_ACTOR_REFERENCE_FIELDS: Final[tuple[str, str]] = (
    "controller_principal_subject_id",
    "controlled_physical_actor_id",
)
_CONVERSION_ACTOR_REFERENCE_FIELDS_BY_PROFILE: Final = (
    ("lifecycle.conversion.animate_objects", ("animated_actor_id",)),
    (
        "lifecycle.conversion.true_polymorph_object_creature",
        ("creature_actor_id",),
    ),
    (
        "lifecycle.conversion.true_polymorph_creature_object",
        ("principal_subject_id", "original_body_actor_id"),
    ),
)
_ASSET_ACTOR_REFERENCE_FIELDS: Final[tuple[str, str]] = (
    "owner_actor_id",
    "attuned_actor_id",
)
_ASSET_CONVERSION_ACTOR_REFERENCE_FIELDS: Final[tuple[str, ...]] = (
    "principal_subject_id",
)
_INDEPENDENT_BODY_RELATION_REFERENCE_FIELD: Final[str] = "independent_body_relation_ref"
_IDENTITY_ASSET_REFERENCE_FIELDS_BY_PROFILE: Final = (
    ("lifecycle.identity.magic_jar", ("receptacle_asset_id",)),
    ("lifecycle.identity.astral_projection", ()),
    (
        "lifecycle.identity.clone",
        ("replica_asset_id", "vessel_asset_id", "original_remains_asset_id"),
    ),
    ("lifecycle.identity.simulacrum", ()),
)
_CONVERSION_ASSET_REFERENCE_FIELDS_BY_PROFILE: Final = (
    ("lifecycle.conversion.animate_objects", ("asset_id",)),
    ("lifecycle.conversion.true_polymorph_object_creature", ("asset_id",)),
    (
        "lifecycle.conversion.true_polymorph_creature_object",
        ("object_asset_id", "merged_asset_ids"),
    ),
)
_ACTOR_EMBODIMENT_ACTOR_REFERENCE_FIELDS_BY_PROFILE: Final = (
    ("actor.embodiment.principal", ()),
    ("actor.embodiment.body", ("principal_subject_id",)),
    ("actor.embodiment.astral_proxy", ("principal_subject_id",)),
    ("actor.embodiment.object_suspension", ()),
)


@dataclass(frozen=True, slots=True)
class _CastSourceBasisEvidence:
    """Unissued evidence bundle; its components retain their exact issuers.

    Reusing this cache identity requires revalidating ``membership`` with the
    exact ``context``. The wrapper itself is never permission or authority.
    """

    source_basis: contracts.SourceBasisResult
    context: contracts.NativePreparationContext
    membership: mechanical_sources.MembershipObservation
    cache_identity: tuple[object, ...]

    @property
    def value(self) -> Mapping[str, object]:
        """Expose the structural result without turning it into permission."""
        return self.source_basis.value


@dataclass(frozen=True, slots=True)
class _SelectedCastSourceRouteEvidence:
    """Unissued structural proof of one exact source-spell Activity route.

    This descriptor records an edge from a bound spell to the selected compiled
    Activity. It is not spell availability, named-mode resolution, execution or
    cast permission.
    """

    consumer_id: str
    profile_id: str
    profile_generation: int
    source_spell_id: str
    activity_id: str
    source_activity_ids: tuple[str, ...]
    source_read_refs: tuple[str, ...]
    source_disposition: Literal[
        "SELECTED_KNOWN_CANTRIP",
        "SELECTED_PREPARED_LEVEL1",
        "UNAVAILABLE",
        "PROHIBITED",
        "NOT_EVALUATED",
    ]
    mode_id: None
    source_mode: Literal["NOT_EVALUATED"]
    catalog_context_fingerprint: str
    command_id: str
    root_resolution_id: str
    context_identity: tuple[object, ...]
    membership_identity: tuple[object, ...]
    read_fingerprint: str


def _hold(
    context: contracts.NativePreparationContext,
    status: Literal[
        "REVALIDATION_REQUIRED", "CAPACITY_REQUIRED", "AUTHORITY_UNAVAILABLE"
    ] = "AUTHORITY_UNAVAILABLE",
) -> NoReturn:
    raise contracts.NativePreparationHold(status, context.execution_ref, ())


def _record(
    source: contracts.CompiledSourceBinding,
    identity: str,
    expected_kind: str,
    context: contracts.NativePreparationContext,
) -> Mapping[str, object]:
    value = source.definition_contracts.get(identity)
    if (
        not isinstance(value, Mapping)
        or value.get("id") != identity
        or value.get("kind") != expected_kind
        or not isinstance(value.get("data"), Mapping)
    ):
        _hold(context)
    return value


def _validate_membership_frame(
    context: contracts.NativePreparationContext,
    membership: mechanical_sources.MembershipObservation,
    actor_ref: NativeOwnerRef,
) -> Mapping[str, object]:
    if (
        type(membership) is not mechanical_sources.MembershipObservation
        or not mechanical_sources.is_membership_issued(membership)
        or membership._context is not context
        or membership._owner_session is not context.owner_session
        or membership._operation_token is not context.owner_session.operation_token
        or membership.p0_observation.operation_token
        is not context.owner_session.operation_token
        or membership.activity_id != context.compiled.activity_id
        or membership.consumer_id != context.consumer_id
        or membership.campaign_id != context.owner_session._campaign_id
        or membership.source_revision != context.owner_session._pinned_campaign.revision
        or membership.source_tree_sha != context.owner_session._pinned_campaign.tree_sha
        or actor_ref.identity[0] not in membership.subject_actor_ids
    ):
        _hold(context, "REVALIDATION_REQUIRED")

    coverage_by_family = {item.family_key: item for item in membership.family_coverage}
    if len(membership.family_coverage) != 2 or set(coverage_by_family) != {
        "world.effect",
        "world.asset",
    }:
        _hold(context)

    expected_refs = {
        *context.role_bindings.values(),
        NativeOwnerRef("runtime.command", (context.execution_ref.command_id,)),
        NativeOwnerRef("runtime.resolution", (context.execution_ref.resolution_id,)),
    }
    from .runtime_execution import _bound_input_origin, input_source_owner_refs

    observation = membership.p0_observation
    try:
        _bound_input_origin(context.accepted_command, observation)
        expected_refs.update(input_source_owner_refs(context.accepted_command, observation,
            authority_sources=observation.operation_token.authority_sources))
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", context.execution_ref, ()) from error
    for family, coverage in coverage_by_family.items():
        if not isinstance(coverage.files, tuple):
            _hold(context)
        expected_refs.update(
            owner_ref
            for owner_ref, _relative_path, _blob_id in (
                mechanical_sources._routes_from_coverage(family, coverage, context)
            )
        )
        if coverage.subtree_id is None and (
            coverage.absence_parent_id is None or coverage.absent_child is None
        ):
            _hold(context)

    observation = membership.p0_observation
    if set(observation.key_union) != expected_refs:
        _hold(context, "REVALIDATION_REQUIRED")
    for owner_ref in expected_refs:
        read = observation.require(owner_ref)
        if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
            _hold(
                context,
                "REVALIDATION_REQUIRED"
                if read.status is CurrentOwnerStatus.REVALIDATION_REQUIRED
                else "AUTHORITY_UNAVAILABLE",
            )

    command_ref = NativeOwnerRef("runtime.command", (context.execution_ref.command_id,))
    resolution_ref = NativeOwnerRef(
        "runtime.resolution", (context.execution_ref.resolution_id,)
    )
    command_payload = observation.require(command_ref).payload
    resolution_payload = observation.require(resolution_ref).payload
    if not isinstance(command_payload, Mapping) or not isinstance(
        resolution_payload, Mapping
    ):
        _hold(context)
    try:
        command_state = contracts._preparation_owner_state(
            command_payload,
            family="runtime.command",
            owner_id=context.execution_ref.command_id,
            campaign_id=membership.campaign_id,
        )
        resolution_state = contracts._preparation_owner_state(
            resolution_payload,
            family="runtime.resolution",
            owner_id=context.execution_ref.resolution_id,
            campaign_id=membership.campaign_id,
        )
    except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        ) from error
    if command_state != contracts._thaw(
        context.accepted_command
    ) or resolution_state != contracts._thaw(context.resolution):
        _hold(context, "REVALIDATION_REQUIRED")

    actor_read = observation.require(actor_ref)
    actor_payload = actor_read.payload
    if (
        actor_read.status is not CurrentOwnerStatus.RESOLVED
        or not isinstance(actor_payload, Mapping)
        or actor_payload.get("kind") != "world.actor"
        or actor_payload.get("id") != actor_ref.identity[0]
        or not isinstance(actor_payload.get("definition_id"), str)
        or not isinstance(actor_payload.get("state"), Mapping)
    ):
        _hold(context)
    return actor_payload


def _active_relation_state_names(state: Mapping[str, object]) -> frozenset[str]:
    active: set[str] = set()
    if "form_state" in state:
        active.add("form_state")
    if "subject_binding" in state:
        active.add("subject_binding")
    identity = state.get("identity_state")
    if isinstance(identity, Mapping) and not (
        identity.get("profile_id") == "lifecycle.identity.simulacrum"
        and identity.get("phase") == "ended"
    ):
        active.add("identity_state")
    control = state.get("control_state")
    if isinstance(control, Mapping) and control.get("phase") != "expired":
        active.add("control_state")
    conversion = state.get("conversion_state")
    if isinstance(conversion, Mapping) and not (
        conversion.get("profile_id")
        in {
            "lifecycle.conversion.animate_objects",
            "lifecycle.conversion.true_polymorph_object_creature",
        }
        and conversion.get("phase") == "reverted"
    ):
        active.add("conversion_state")
    return frozenset(active)


def _profile_reference_fields(
    value: object,
    inventory: tuple[tuple[str, tuple[str, ...]], ...],
    context: contracts.NativePreparationContext,
) -> tuple[str, ...]:
    if not isinstance(value, Mapping):
        _hold(context)
    profile_id = value.get("profile_id")
    for expected_profile, fields in inventory:
        if profile_id == expected_profile:
            return fields
    _hold(context)


def _owner_revision_reference_matches(
    relation: Mapping[str, object],
    family_key: str,
    identities: set[str],
    context: contracts.NativePreparationContext,
) -> bool:
    revision = relation.get(_INDEPENDENT_BODY_RELATION_REFERENCE_FIELD)
    if revision is None:
        return False
    if not isinstance(revision, Mapping):
        _hold(context)
    owner_ref = revision.get("owner_ref")
    if not isinstance(owner_ref, Mapping):
        _hold(context)
    if owner_ref.get("family_key") != family_key:
        return False
    identity = owner_ref.get("identity")
    if not isinstance(identity, (tuple, list)) or any(
        not isinstance(item, str) for item in identity
    ):
        _hold(context)
    return bool(set(identity) & identities)


def _state_relation_mentions_actor(
    state: Mapping[str, object],
    actor_id: str,
    context: contracts.NativePreparationContext,
) -> bool:
    binding = state.get("subject_binding")
    if isinstance(binding, Mapping) and any(
        binding.get(field_name) == actor_id
        for field_name in _SUBJECT_BINDING_ACTOR_REFERENCE_FIELDS
    ):
        return True
    active_relations = _active_relation_state_names(state)
    for member, inventory in (
        ("identity_state", _IDENTITY_ACTOR_REFERENCE_FIELDS_BY_PROFILE),
        ("conversion_state", _CONVERSION_ACTOR_REFERENCE_FIELDS_BY_PROFILE),
    ):
        if member not in active_relations:
            continue
        value = state.get(member)
        fields = _profile_reference_fields(value, inventory, context)
        if any(value.get(field_name) == actor_id for field_name in fields):
            return True
        if (
            member == "conversion_state"
            and value.get("profile_id")
            == "lifecycle.conversion.true_polymorph_creature_object"
            and _owner_revision_reference_matches(
                value, "world.actor", {actor_id}, context
            )
        ):
            return True
    if "control_state" in active_relations:
        control = state.get("control_state")
        if not isinstance(control, Mapping):
            _hold(context)
        if any(
            control.get(field_name) == actor_id
            for field_name in _CONTROL_ACTOR_REFERENCE_FIELDS
        ):
            return True
    return False


def _state_mentions_caster_asset(
    state: Mapping[str, object],
    caster_asset_ids: set[str],
    context: contracts.NativePreparationContext,
) -> bool:
    active_relations = _active_relation_state_names(state)
    for member, inventory in (
        ("identity_state", _IDENTITY_ASSET_REFERENCE_FIELDS_BY_PROFILE),
        ("conversion_state", _CONVERSION_ASSET_REFERENCE_FIELDS_BY_PROFILE),
    ):
        if member not in active_relations:
            continue
        value = state.get(member)
        if not isinstance(value, Mapping):
            _hold(context)
        fields = _profile_reference_fields(value, inventory, context)
        for field_name in fields:
            reference = value.get(field_name)
            if field_name == "merged_asset_ids":
                if not isinstance(reference, (tuple, list)) or any(
                    not isinstance(item, str) for item in reference
                ):
                    _hold(context)
                if set(reference) & caster_asset_ids:
                    return True
            elif reference is not None:
                if not isinstance(reference, str):
                    _hold(context)
                if reference in caster_asset_ids:
                    return True
        if (
            member == "conversion_state"
            and value.get("profile_id")
            == "lifecycle.conversion.true_polymorph_creature_object"
            and _owner_revision_reference_matches(
                value, "world.asset", caster_asset_ids, context
            )
        ):
            return True
    return False


def _caster_asset_sources(
    membership: mechanical_sources.MembershipObservation,
    actor_id: str,
    context: contracts.NativePreparationContext,
) -> tuple[set[str], dict[str, Mapping[str, object]]]:
    states: dict[str, Mapping[str, object]] = {}
    caster_asset_ids = {
        asset.owner_ref.identity[0]
        for asset in membership.assets
        if asset.placement_owner_id == actor_id
    }
    for owner_ref in membership.p0_observation.key_union:
        if owner_ref.family_key != "world.asset":
            continue
        asset_id = owner_ref.identity[0]
        read = membership.p0_observation.require(owner_ref)
        payload = read.payload
        if (
            read.status is not CurrentOwnerStatus.RESOLVED
            or not isinstance(payload, Mapping)
            or payload.get("id") != asset_id
            or payload.get("kind") != "world.asset"
            or not isinstance(payload.get("state"), Mapping)
        ):
            _hold(context)
        state = payload["state"]
        states[asset_id] = state
        if any(
            state.get(field_name) == actor_id
            for field_name in _ASSET_ACTOR_REFERENCE_FIELDS
        ):
            caster_asset_ids.add(asset_id)
        conversion = state.get("conversion_membership")
        if isinstance(conversion, Mapping) and any(
            conversion.get(field_name) == actor_id
            for field_name in _ASSET_CONVERSION_ACTOR_REFERENCE_FIELDS
        ):
            caster_asset_ids.add(asset_id)
    return caster_asset_ids, states


def _require_current_subject_sources(
    source: contracts.CompiledSourceBinding,
    membership: mechanical_sources.MembershipObservation,
    actor_id: str,
    context: contracts.NativePreparationContext,
) -> None:
    """Inspect relation relevance over the complete P0-covered Effect universe."""
    support_effect_refs = {item.owner_ref for item in membership.effect_dependencies}
    exclusion_reasons = {item.owner_ref: item.reason for item in membership.exclusions}
    caster_asset_ids, asset_states = _caster_asset_sources(
        membership, actor_id, context
    )
    membership_assets = {
        asset.owner_ref.identity[0]: asset for asset in membership.assets
    }
    relevant_effect_ids: set[str] = set()
    for owner_ref in membership.p0_observation.key_union:
        if owner_ref.family_key != "world.effect":
            continue
        effect_id = owner_ref.identity[0]
        read = membership.p0_observation.require(owner_ref)
        payload = read.payload
        if (
            read.status is not CurrentOwnerStatus.RESOLVED
            or not isinstance(payload, Mapping)
            or payload.get("id") != effect_id
            or payload.get("kind") != "world.effect"
            or not isinstance(payload.get("state"), Mapping)
        ):
            _hold(context)
        state = payload["state"]
        lifecycle = state.get("lifecycle")
        if not isinstance(lifecycle, Mapping):
            _hold(context)
        lifecycle_id = lifecycle.get("state_id")
        if lifecycle_id == "effect_lifecycle.terminal":
            continue
        if lifecycle_id != "effect_lifecycle.active":
            _hold(context)
        relation_state = bool(_active_relation_state_names(state))
        relation_mentions_actor = _state_relation_mentions_actor(
            state, actor_id, context
        )
        relation_mentions_caster_asset = _state_mentions_caster_asset(
            state, caster_asset_ids, context
        )
        exclusion_reason = exclusion_reasons.get(owner_ref)
        if (
            exclusion_reason == "wrong_subject_binding"
            and not relation_mentions_actor
            and not relation_mentions_caster_asset
        ):
            continue
        relevant = (
            state.get(_EFFECT_DIRECT_ACTOR_REFERENCE_FIELDS[0]) == actor_id
            or relation_mentions_actor
            or relation_mentions_caster_asset
            or owner_ref in support_effect_refs
        )
        if not relevant:
            continue
        relevant_effect_ids.add(effect_id)
        if relation_state:
            _hold(context)
        definition_id = payload.get("definition_id")
        definition = (
            source.definition_contracts.get(definition_id)
            if isinstance(definition_id, str)
            else None
        )
        data = definition.get("data") if isinstance(definition, Mapping) else None
        if (
            not isinstance(definition, Mapping)
            or definition.get("id") != definition_id
            or definition.get("kind") != "definition.effect"
            or not isinstance(data, Mapping)
        ):
            _hold(context)
        elements = data.get("rule_elements", ())
        if not isinstance(elements, (tuple, list)):
            _hold(context)
        for element in elements:
            if not isinstance(element, Mapping):
                _hold(context)
            if (
                element.get("selector")
                in {
                    "ability.charisma",
                    "spell.dc",
                    "attack.roll",
                }
                and definition_id != _INNATE_SORCERY_EFFECT_ID
            ):
                _hold(context)

    for asset_id, state in asset_states.items():
        owner_actor_id = state.get("owner_actor_id")
        attuned_actor_id = state.get("attuned_actor_id")
        container_asset_id = state.get("container_asset_id")
        transform = state.get("equipment_transform")
        replica = state.get("replica_origin")
        conversion = state.get("conversion_membership")
        relevant = (
            asset_id in caster_asset_ids
            or owner_actor_id == actor_id
            or attuned_actor_id == actor_id
            or container_asset_id in caster_asset_ids
            or (
                isinstance(transform, Mapping)
                and transform.get("source_effect_id") in relevant_effect_ids
            )
            or (
                isinstance(replica, Mapping)
                and (
                    replica.get("source_asset_id") in caster_asset_ids
                    or replica.get("relation_effect_id") in relevant_effect_ids
                )
            )
            or (
                isinstance(conversion, Mapping)
                and any(
                    conversion.get(field_name) == actor_id
                    for field_name in _ASSET_CONVERSION_ACTOR_REFERENCE_FIELDS
                )
            )
        )
        if not relevant:
            continue
        membership_asset = membership_assets.get(asset_id)
        if (
            (
                membership_asset is not None
                and membership_asset.conversion_mode is not None
            )
            or transform is not None
            or replica is not None
            or conversion is not None
        ):
            _hold(context)


def _direct_definition_dependencies(
    source: contracts.CompiledSourceBinding, identity: str
) -> frozenset[str]:
    source_ref = f"bound_definition:{identity}"
    return frozenset(
        edge.dependency_ref.removeprefix("bound_definition:")
        for edge in source.dependency_edges
        if edge.source_ref == source_ref
        and edge.dependency_ref.startswith("bound_definition:")
    )


def _one_spell_grant(
    option: object,
    *,
    prepared: bool,
    source: contracts.CompiledSourceBinding,
    context: contracts.NativePreparationContext,
) -> tuple[str, str]:
    if not isinstance(option, Mapping):
        _hold(context)
    option_id = option.get("option_id")
    grants = option.get("grant_definition_ids")
    spell_bindings = option.get("spell_bindings")
    if (
        not isinstance(option_id, str)
        or not isinstance(grants, (list, tuple))
        or len(grants) != 1
        or not isinstance(grants[0], str)
        or not isinstance(spell_bindings, Mapping)
        or tuple(spell_bindings.get("known_spell_ids", ())) != (grants[0],)
        or (
            prepared
            and tuple(spell_bindings.get("prepared_spell_ids", ())) != (grants[0],)
        )
        or (not prepared and "prepared_spell_ids" in spell_bindings)
        or option_id != f"option.{grants[0]}"
    ):
        _hold(context)
    spell = _record(source, grants[0], "definition.spell", context)
    data = spell["data"]
    expected_level = 1 if prepared else 0
    if type(data.get("level")) is not int or data["level"] != expected_level:
        _hold(context)
    return option_id, grants[0]


def _slot_options(
    source: contracts.CompiledSourceBinding,
    slot_id: str,
    *,
    expected_count: int,
    prepared: bool,
    context: contracts.NativePreparationContext,
) -> Mapping[str, str]:
    slot = source.choice_slot_contracts.get(slot_id)
    if (
        not isinstance(slot, Mapping)
        or slot.get("choice_id") != slot_id
        or slot.get("minimum") != expected_count
        or slot.get("maximum") != expected_count
        or not isinstance(slot.get("options"), (tuple, list))
    ):
        _hold(context)
    options: dict[str, str] = {}
    for option in slot["options"]:
        option_id, spell_id = _one_spell_grant(
            option,
            prepared=prepared,
            source=source,
            context=context,
        )
        if option_id in options:
            _hold(context)
        options[option_id] = spell_id
    if len(options) < expected_count:
        _hold(context)
    return options


def _selected_options(
    build: Mapping[str, object],
    slot_id: str,
    legal_options: Mapping[str, str],
    *,
    expected_count: int,
    context: contracts.NativePreparationContext,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    choice_bindings = build.get("choice_bindings")
    selected = (
        choice_bindings.get(slot_id) if isinstance(choice_bindings, Mapping) else None
    )
    option_ids = (
        selected.get("selected_option_ids") if isinstance(selected, Mapping) else None
    )
    if (
        not isinstance(option_ids, (tuple, list))
        or len(option_ids) != expected_count
        or any(not isinstance(item, str) for item in option_ids)
        or len(set(option_ids)) != len(option_ids)
        or any(item not in legal_options for item in option_ids)
    ):
        _hold(context)
    ordered_options = tuple(sorted(option_ids, key=lambda item: legal_options[item]))
    spells = tuple(legal_options[item] for item in ordered_options)
    return ordered_options, spells


def _require_sorcerer1_definitions(
    source: contracts.CompiledSourceBinding,
    context: contracts.NativePreparationContext,
) -> None:
    class_definition = _record(source, _CLASS_ID, "definition.class", context)
    class_data = class_definition["data"]
    primary_abilities = class_data.get("primary_ability_ids")
    if (
        set(class_data) != {"hit_die", "primary_ability_ids", "advancement_id"}
        or class_data.get("advancement_id") != _ADVANCEMENT_ID
        or not isinstance(primary_abilities, (tuple, list))
        or tuple(primary_abilities) != (_SOURCE_ABILITY_ID,)
        or _ADVANCEMENT_ID not in _direct_definition_dependencies(source, _CLASS_ID)
    ):
        _hold(context)

    advancement = _record(source, _ADVANCEMENT_ID, "definition.advancement", context)
    advancement_data = advancement["data"]
    levels = advancement_data.get("levels")
    if set(advancement_data) != {"levels"} or not isinstance(levels, (tuple, list)):
        _hold(context)
    level_one = tuple(
        row
        for row in levels
        if isinstance(row, Mapping)
        and type(row.get("level")) is int
        and row["level"] == 1
    )
    if (
        len(levels) != 1
        or len(level_one) != 1
        or set(level_one[0]) != {"level", "automatic_grant_definition_ids"}
    ):
        _hold(context)
    feature_grants = level_one[0].get("automatic_grant_definition_ids")
    if (
        not isinstance(feature_grants, (tuple, list))
        or any(not isinstance(item, str) for item in feature_grants)
        or set(feature_grants) != {_SPELLCASTING_FEATURE_ID, _INNATE_SORCERY_FEATURE_ID}
        or len(feature_grants) != 2
    ):
        _hold(context)

    spellcasting = _record(
        source, _SPELLCASTING_FEATURE_ID, "definition.feature", context
    )
    spellcasting_refs = _direct_definition_dependencies(
        source, _SPELLCASTING_FEATURE_ID
    )
    if (
        set(spellcasting["data"]) != {"resource_ids"}
        or tuple(spellcasting["data"].get("resource_ids", ()))
        != ("resource.spell_slot.level_1",)
        or not {
            "resource.spell_slot.level_1",
            "asset.arcane_focus",
        }
        <= spellcasting_refs
    ):
        _hold(context)
    _record(source, "resource.spell_slot.level_1", "definition.resource", context)
    _record(source, "asset.arcane_focus", "definition.asset", context)

    innate_feature = _record(
        source, _INNATE_SORCERY_FEATURE_ID, "definition.feature", context
    )
    innate_refs = _direct_definition_dependencies(source, _INNATE_SORCERY_FEATURE_ID)
    if (
        set(innate_feature["data"]) != {"activity_ids", "resource_ids", "effect_ids"}
        or tuple(innate_feature["data"].get("activity_ids", ()))
        != ("activity.feature.innate_sorcery",)
        or tuple(innate_feature["data"].get("resource_ids", ()))
        != ("resource.innate_sorcery",)
        or tuple(innate_feature["data"].get("effect_ids", ()))
        != (_INNATE_SORCERY_EFFECT_ID,)
        or not {
            _INNATE_SORCERY_EFFECT_ID,
            "resource.innate_sorcery",
            "activity.feature.innate_sorcery",
        }
        <= innate_refs
    ):
        _hold(context)
    _record(source, "resource.innate_sorcery", "definition.resource", context)
    _record(source, "activity.feature.innate_sorcery", "definition.activity", context)

    effect = _record(source, _INNATE_SORCERY_EFFECT_ID, "definition.effect", context)
    elements = effect["data"].get("rule_elements")
    expected_elements = (
        {"selector": "spell.dc", "operation_id": "rule.add_flat", "value": 1},
        {
            "selector": "attack.roll",
            "operation_id": "rule.grant_advantage",
            "value": True,
        },
    )
    if (
        not isinstance(elements, (tuple, list))
        or len(elements) != len(expected_elements)
        or tuple(dict(item) for item in elements if isinstance(item, Mapping))
        != expected_elements
    ):
        _hold(context)


def _acquisition(
    source: contracts.CompiledSourceBinding,
    actor_state: Mapping[str, object],
    context: contracts.NativePreparationContext,
) -> tuple[dict[str, object], frozenset[str], frozenset[str]]:
    build = actor_state.get("build")
    if not isinstance(build, Mapping) or set(build) - {
        "species_id",
        "background_id",
        "class_progression",
        "choice_bindings",
        "spellcasting",
    }:
        _hold(context)
    progression = build.get("class_progression")
    if (
        not isinstance(progression, (tuple, list))
        or len(progression) != 1
        or not isinstance(progression[0], Mapping)
        or set(progression[0]) != {"class_id", "level"}
        or progression[0].get("class_id") != _CLASS_ID
        or type(progression[0].get("level")) is not int
        or progression[0]["level"] != 1
    ):
        _hold(context)

    slots = source.binding.choice_slots
    slot_specs = {slot.slot_id: slot for slot in slots}
    if (
        set(slot_specs) != {_CANTRIP_SLOT_ID, _PREPARED_SLOT_ID}
        or slot_specs[_CANTRIP_SLOT_ID].minimum != 4
        or slot_specs[_CANTRIP_SLOT_ID].maximum != 4
        or slot_specs[_PREPARED_SLOT_ID].minimum != 2
        or slot_specs[_PREPARED_SLOT_ID].maximum != 2
    ):
        _hold(context)
    cantrip_options = _slot_options(
        source,
        _CANTRIP_SLOT_ID,
        expected_count=4,
        prepared=False,
        context=context,
    )
    prepared_options = _slot_options(
        source,
        _PREPARED_SLOT_ID,
        expected_count=2,
        prepared=True,
        context=context,
    )
    cantrip_option_ids, cantrips = _selected_options(
        build,
        _CANTRIP_SLOT_ID,
        cantrip_options,
        expected_count=4,
        context=context,
    )
    prepared_option_ids, prepared = _selected_options(
        build,
        _PREPARED_SLOT_ID,
        prepared_options,
        expected_count=2,
        context=context,
    )
    if set(cantrips) & set(prepared):
        _hold(context)

    spellcasting = build.get("spellcasting")
    if not isinstance(spellcasting, Mapping) or set(spellcasting) != {
        "known_spell_ids",
        "prepared_spell_ids",
    }:
        _hold(context)

    def membership(member: str, expected: set[str]) -> tuple[str, ...]:
        value = spellcasting.get(member)
        if (
            not isinstance(value, (tuple, list))
            or any(not isinstance(identity, str) for identity in value)
            or len(value) != len(set(value))
            or set(value) != expected
        ):
            _hold(context)
        return tuple(sorted(value))

    known_ids = membership("known_spell_ids", set(cantrips) | set(prepared))
    prepared_ids = membership("prepared_spell_ids", set(prepared))
    choice_bindings = build.get("choice_bindings")
    if not isinstance(choice_bindings, Mapping) or any(
        key.startswith("advancement.sorcerer.")
        and key not in {_CANTRIP_SLOT_ID, _PREPARED_SLOT_ID}
        for key in choice_bindings
        if isinstance(key, str)
    ):
        _hold(context)

    legal_cantrips = frozenset(cantrip_options.values())
    legal_prepared = frozenset(prepared_options.values())

    activity_ids: set[str] = set()
    edges = {(edge.source_ref, edge.dependency_ref) for edge in source.dependency_edges}
    for spell_id in (*cantrips, *prepared):
        spell = _record(source, spell_id, "definition.spell", context)
        level = 0 if spell_id in cantrips else 1
        if spell["data"].get("level") != level:
            _hold(context)
        declared_activities = spell["data"].get("activity_ids")
        if (
            not isinstance(declared_activities, (tuple, list))
            or not declared_activities
            or len(declared_activities) != len(set(declared_activities))
        ):
            _hold(context)
        for activity_id in declared_activities:
            _record(source, activity_id, "definition.activity", context)
            if (
                f"bound_definition:{spell_id}",
                f"bound_definition:{activity_id}",
            ) not in edges:
                _hold(context)
            activity_ids.add(activity_id)

    acquisition: dict[str, object] = {
        "class_progression": [{"class_id": _CLASS_ID, "level": 1}],
        "advancement_id": _ADVANCEMENT_ID,
        "spellcasting_feature_id": _SPELLCASTING_FEATURE_ID,
        "cantrip_choice_slot_id": _CANTRIP_SLOT_ID,
        "cantrip_spell_ids": tuple(sorted(cantrips)),
        "cantrip_option_ids": tuple(
            f"option.{identity}" for identity in sorted(cantrips)
        ),
        "prepared_choice_slot_id": _PREPARED_SLOT_ID,
        "level1_spell_ids": tuple(sorted(prepared)),
        "prepared_option_ids": tuple(
            f"option.{identity}" for identity in sorted(prepared)
        ),
        "known_spell_ids": known_ids,
        "prepared_spell_ids": prepared_ids,
    }
    # Keep selection order irrelevant while preserving exact owner-relative
    # binding identity in the reconstructed equations above.
    if tuple(sorted(cantrip_option_ids)) != tuple(
        sorted(acquisition["cantrip_option_ids"])
    ):
        _hold(context)
    if tuple(sorted(prepared_option_ids)) != tuple(
        sorted(acquisition["prepared_option_ids"])
    ):
        _hold(context)
    return acquisition, legal_cantrips, legal_prepared


def _ability_basis(
    source: contracts.CompiledSourceBinding,
    actor_payload: Mapping[str, object],
    actor_state: Mapping[str, object],
    context: contracts.NativePreparationContext,
) -> dict[str, object]:
    abilities = actor_state.get("abilities", {})
    if not isinstance(abilities, Mapping):
        _hold(context)
    components = abilities.get(_SOURCE_ABILITY_ID)
    base_score: int | None = None
    adjustment = 0
    if components is not None:
        if (
            not isinstance(components, Mapping)
            or not components
            or set(components) - {"base", "adjustment"}
        ):
            _hold(context)
        raw_adjustment = components.get("adjustment", 0)
        if type(raw_adjustment) is not int:
            _hold(context)
        adjustment = raw_adjustment
        if "base" in components:
            raw_base = components["base"]
            if type(raw_base) is not int or raw_base < 1:
                _hold(context)
            base_score = raw_base

    source_actor_ref = {
        "family_key": "world.actor",
        "identity": [actor_payload["id"]],
    }
    base_source = "ACTOR"
    base_source_ref: dict[str, object]
    if base_score is not None:
        base_source_ref = {"kind": "ACTOR", "source_actor_ref": source_actor_ref}
    else:
        actor_definition_id = actor_payload.get("definition_id")
        archetype = (
            source.definition_contracts.get(actor_definition_id)
            if isinstance(actor_definition_id, str)
            else None
        )
        data = archetype.get("data") if isinstance(archetype, Mapping) else None
        archetype_abilities = (
            data.get("abilities") if isinstance(data, Mapping) else None
        )
        raw_base = (
            archetype_abilities.get(_SOURCE_ABILITY_ID)
            if isinstance(archetype_abilities, Mapping)
            else None
        )
        if (
            not isinstance(archetype, Mapping)
            or archetype.get("id") != actor_definition_id
            or archetype.get("kind") != "definition.actor_archetype"
            or type(raw_base) is not int
            or raw_base < 1
        ):
            # The current Actor build schema does not define an ability-score
            # base member. Do not infer one from prose or an untyped build field.
            _hold(context)
        base_score = raw_base
        base_source = "ARCHETYPE"
        base_source_ref = {
            "kind": "ARCHETYPE",
            "source_definition_ref": {
                "definition_id": actor_definition_id,
                "kind": "definition.actor_archetype",
            },
        }

    score = base_score + adjustment
    if not 1 <= score <= 30:
        _hold(context)
    modifier = (score - 10) // 2
    return {
        "ability_id": _SOURCE_ABILITY_ID,
        "base_source": base_source,
        "base_source_ref": base_source_ref,
        "base_score": base_score,
        "adjustment": adjustment,
        "score": score,
        "modifier": modifier,
        "proficiency_bonus": 2,
        "base_spell_save_dc": 8 + modifier + 2,
        "base_spell_attack_bonus": modifier + 2,
        "modifier_source_definition_ids": (_INNATE_SORCERY_EFFECT_ID,),
    }


def _prepare_cast_source_basis(
    context: contracts.NativePreparationContext,
) -> _CastSourceBasisEvidence:
    """Derive partial Sorcerer1 source evidence from one authentic native context.

    This result is not cast permission, a final modifier result, or an execution
    fragment. Inputs are recovered only from the exact compiler and context.
    """
    if (
        type(context) is not contracts.NativePreparationContext
        or not contracts._preparation_context_is_issued(context)
    ):
        raise mechanical_context.MechanicalContextError(
            "source basis requires an authentic source-bound preparation context"
        )
    initial_identity = mechanical_context.context_cache_identity(context)
    if (
        not contracts._compiler_value_is_issued(context.compiled, kind="compiled")
        or context.catalog.compiled_activities.get(context.compiled.activity_id)
        is not context.compiled
    ):
        _hold(context)
    rows = tuple(
        row
        for row in context.compiled.cast_source_bindings
        if row.binding.consumer_id == context.consumer_id
    )
    if (
        len(rows) != 1
        or type(rows[0].binding) is not contracts.CastSourceBinding
        or rows[0].binding.profile_id != "execution.spell_cast.srd521"
        or rows[0].binding.profile_generation != 1
        or rows[0].binding.context_fact_ids
    ):
        _hold(context)
    source = rows[0]
    binding = source.binding
    actor_ref = context.role_bindings.get("actor")
    request = context.accepted_command.get("action_request")
    if (
        type(actor_ref) is not NativeOwnerRef
        or actor_ref.family_key != "world.actor"
        or not isinstance(request, Mapping)
        or actor_ref.identity != (request.get("actor_id"),)
    ):
        _hold(context)

    class_role_bindings = tuple(
        role_binding
        for role_binding in binding.native_role_bindings
        if role_binding.read_ref == f"bound_definition:{_CLASS_ID}"
    )
    if (
        len(binding.native_role_bindings) != 1
        or len(class_role_bindings) != 1
        or class_role_bindings[0].role_names != ("actor",)
        or any(
            role_name not in context.role_bindings
            for role_binding in binding.native_role_bindings
            for role_name in role_binding.role_names
        )
        or any(
            role_name != "actor"
            for role_binding in binding.native_role_bindings
            for role_name in role_binding.role_names
        )
    ):
        _hold(context)

    membership = mechanical_sources.prepare_membership(context)
    actor_payload = _validate_membership_frame(context, membership, actor_ref)
    _require_current_subject_sources(source, membership, actor_ref.identity[0], context)

    actor_state = actor_payload["state"]
    if "embodiment" in actor_state:
        _hold(context)

    _require_sorcerer1_definitions(source, context)
    acquisition, legal_cantrips, legal_prepared = _acquisition(
        source, actor_state, context
    )
    ability_basis = _ability_basis(source, actor_payload, actor_state, context)

    source_spell = _record(source, binding.source_spell_id, "definition.spell", context)
    source_spell_level = source_spell["data"].get("level")
    if type(source_spell_level) is not int or source_spell_level < 0:
        _hold(context)
    cantrips = set(acquisition["cantrip_spell_ids"])
    prepared = set(acquisition["level1_spell_ids"])
    if source_spell_level == 0 and binding.source_spell_id in cantrips:
        disposition = "SELECTED_KNOWN_CANTRIP"
    elif source_spell_level == 1 and binding.source_spell_id in prepared:
        disposition = "SELECTED_PREPARED_LEVEL1"
    elif (source_spell_level == 0 and binding.source_spell_id in legal_cantrips) or (
        source_spell_level == 1 and binding.source_spell_id in legal_prepared
    ):
        disposition = "UNAVAILABLE"
    elif source_spell_level > 1:
        disposition = "PROHIBITED"
    else:
        disposition = "NOT_EVALUATED"

    source_definition_refs = tuple(
        {
            "definition_id": reference.definition_id,
            "kind": reference.kind,
        }
        for reference in binding.source_definition_refs
    )
    activity_closure = tuple(
        sorted(
            {
                activity_id
                for spell_id in (
                    *acquisition["cantrip_spell_ids"],
                    *acquisition["level1_spell_ids"],
                )
                for activity_id in source.definition_contracts[spell_id]["data"][
                    "activity_ids"
                ]
            }
        )
    )
    facet_values = {
        "class_progression": "RESOLVED",
        "acquisition": "RESOLVED",
        "source_spell": {
            "NOT_EVALUATED": "NOT_EVALUATED",
            "SELECTED_KNOWN_CANTRIP": "RESOLVED",
            "SELECTED_PREPARED_LEVEL1": "RESOLVED",
            "UNAVAILABLE": "UNAVAILABLE",
            "PROHIBITED": "PROHIBITED",
        }[disposition],
        "source_mode": "NOT_EVALUATED",
        "activity_closure": "RESOLVED",
        "source_ability": "RESOLVED",
        "proficiency": "RESOLVED",
        "base_spell_values": "RESOLVED",
        "final_modifier_closure": "NOT_EVALUATED",
        "movement": "NOT_EVALUATED",
        "senses": "NOT_EVALUATED",
        "anatomy": "NOT_EVALUATED",
        "equipment": "NOT_EVALUATED",
        "form": "NOT_EVALUATED",
    }
    result_value: dict[str, object] = {
        "consumer_id": context.consumer_id,
        "profile_id": binding.profile_id,
        "profile_generation": binding.profile_generation,
        "activity_id": context.compiled.activity_id,
        "source_actor_ref": {
            "family_key": actor_ref.family_key,
            "identity": actor_ref.identity,
        },
        "source_spell_id": binding.source_spell_id,
        "source_spell_level": source_spell_level,
        "mode_id": None,
        "activity_closure_ids": activity_closure,
        "source_definition_refs": source_definition_refs,
        "read_refs": source.dependency_read_refs,
        "context_facts": (),
        "source_disposition": disposition,
        "acquisition": acquisition,
        "ability_basis": ability_basis,
        "facets": facet_values,
    }
    try:
        result = contracts.validate_source_basis_result(
            result_value, compiled=context.compiled
        )
    except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        ) from error
    if not mechanical_sources.revalidate_membership(membership, context):
        _hold(context, "REVALIDATION_REQUIRED")
    membership_identity = mechanical_context._value_identity(
        {
            "activity_id": membership.activity_id,
            "consumer_id": membership.consumer_id,
            "subject_actor_ids": membership.subject_actor_ids,
            "membership": mechanical_context._membership_wire(membership),
            "p0_observation_fingerprint": membership.p0_observation.observation_fingerprint,
        }
    )
    return _CastSourceBasisEvidence(
        source_basis=result,
        context=context,
        membership=membership,
        cache_identity=(initial_identity, membership_identity),
    )


def _prove_selected_source_route(
    context: contracts.NativePreparationContext,
) -> _SelectedCastSourceRouteEvidence:
    """Derive native source evidence, then prove its selected Activity edge.

    The basis is derived internally from the authentic context and current native
    Actor, never accepted as caller-supplied structural truth. The result remains
    unissued; source availability, named mode, target success and execution are
    outside this proof.
    """
    if (
        type(context) is not contracts.NativePreparationContext
        or not contracts._preparation_context_is_issued(context)
    ):
        raise mechanical_context.MechanicalContextError(
            "selected route requires an authentic source-bound preparation context"
        )
    context_identity = mechanical_context.context_cache_identity(context)
    evidence = _prepare_cast_source_basis(context)
    if (
        type(evidence) is not _CastSourceBasisEvidence
        or evidence.context is not context
        or type(evidence.source_basis) is not contracts.SourceBasisResult
        or type(evidence.membership) is not mechanical_sources.MembershipObservation
    ):
        _hold(context, "REVALIDATION_REQUIRED")

    compiled = context.compiled
    if (
        not contracts._compiler_value_is_issued(compiled, kind="compiled")
        or context.catalog.compiled_activities.get(compiled.activity_id) is not compiled
    ):
        _hold(context)

    source_basis = evidence.source_basis
    try:
        validated_basis = contracts.validate_source_basis_result(
            source_basis, compiled=compiled
        )
    except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        ) from error
    basis_value = validated_basis.value
    if (
        basis_value["activity_id"] != compiled.activity_id
        or basis_value["consumer_id"] != context.consumer_id
        or basis_value["mode_id"] is not None
        or basis_value["facets"]["source_mode"] != "NOT_EVALUATED"
    ):
        _hold(context)

    membership = evidence.membership
    cache_identity = evidence.cache_identity
    if not isinstance(cache_identity, tuple) or len(cache_identity) != 2:
        _hold(context, "REVALIDATION_REQUIRED")
    initial_identity = cache_identity[0]
    if (
        not mechanical_sources.is_membership_issued(membership)
        or membership._context is not context
        or membership._owner_session is not context.owner_session
        or membership._operation_token is not context.owner_session.operation_token
        or membership.p0_observation.operation_token
        is not context.owner_session.operation_token
        or membership.activity_id != compiled.activity_id
        or membership.consumer_id != context.consumer_id
    ):
        _hold(context, "REVALIDATION_REQUIRED")

    membership_identity = mechanical_context._value_identity(
        {
            "activity_id": membership.activity_id,
            "consumer_id": membership.consumer_id,
            "subject_actor_ids": membership.subject_actor_ids,
            "membership": mechanical_context._membership_wire(membership),
            "p0_observation_fingerprint": membership.p0_observation.observation_fingerprint,
        }
    )
    if cache_identity != (context_identity, membership_identity):
        _hold(context, "REVALIDATION_REQUIRED")
    actor_ref = context.role_bindings.get("actor")
    if type(actor_ref) is not NativeOwnerRef or actor_ref.family_key != "world.actor":
        _hold(context)
    if not mechanical_sources.revalidate_membership(membership, context):
        _hold(context, "REVALIDATION_REQUIRED")
    _validate_membership_frame(context, membership, actor_ref)

    accepted_command = context.accepted_command
    request = accepted_command.get("action_request")
    resolution = context.resolution
    command_id = context.execution_ref.command_id
    resolution_id = context.execution_ref.resolution_id
    if (
        accepted_command.get("command_kind") != "action"
        or accepted_command.get("disposition") != "command.accepted"
        or accepted_command.get("command_id") != command_id
        or accepted_command.get("root_resolution_id") != resolution_id
        or not isinstance(request, Mapping)
        or request.get("activity_id") != compiled.activity_id
        or resolution.get("root_command_id") != command_id
        or resolution.get("initiating_command_id") != command_id
        or resolution.get("activity_id") != compiled.activity_id
    ):
        _hold(context, "REVALIDATION_REQUIRED")

    rows = tuple(
        row
        for row in compiled.cast_source_bindings
        if row.binding.consumer_id == context.consumer_id
    )
    if (
        len(rows) != 1
        or type(rows[0].binding) is not contracts.CastSourceBinding
        or rows[0].binding.profile_id != "execution.spell_cast.srd521"
        or rows[0].binding.profile_generation != 1
        or rows[0].binding.source_spell_id != basis_value["source_spell_id"]
    ):
        _hold(context)
    source = rows[0]
    source_spell_id = source.binding.source_spell_id
    spell_definition = source.definition_contracts.get(source_spell_id)
    if (
        not isinstance(spell_definition, Mapping)
        or spell_definition.get("id") != source_spell_id
        or spell_definition.get("kind") != "definition.spell"
        or not isinstance(spell_definition.get("data"), Mapping)
    ):
        _hold(context)
    raw_activity_ids = spell_definition["data"].get("activity_ids")
    if (
        not isinstance(raw_activity_ids, (tuple, list))
        or not raw_activity_ids
        or any(not isinstance(activity_id, str) for activity_id in raw_activity_ids)
        or len(raw_activity_ids) != len(set(raw_activity_ids))
    ):
        _hold(context)
    source_activity_ids = tuple(raw_activity_ids)
    activity_id = compiled.activity_id
    activity_definition = source.definition_contracts.get(activity_id)
    definition_edges = {
        (edge.source_ref, edge.dependency_ref) for edge in source.dependency_edges
    }
    if (
        activity_id not in source_activity_ids
        or not isinstance(activity_definition, Mapping)
        or activity_definition.get("id") != activity_id
        or activity_definition.get("kind") != "definition.activity"
        or (
            f"bound_definition:{source_spell_id}",
            f"bound_definition:{activity_id}",
        )
        not in definition_edges
    ):
        _hold(context)

    return _SelectedCastSourceRouteEvidence(
        consumer_id=context.consumer_id,
        profile_id=source.binding.profile_id,
        profile_generation=source.binding.profile_generation,
        source_spell_id=source_spell_id,
        activity_id=activity_id,
        source_activity_ids=source_activity_ids,
        source_read_refs=source.dependency_read_refs,
        source_disposition=basis_value["source_disposition"],
        mode_id=None,
        source_mode="NOT_EVALUATED",
        catalog_context_fingerprint=context.catalog.catalog_context.fingerprint,
        command_id=command_id,
        root_resolution_id=resolution_id,
        context_identity=initial_identity,
        membership_identity=membership_identity,
        read_fingerprint=membership.p0_observation.observation_fingerprint,
    )


def _prove_named_source_mode(
    context: contracts.NativePreparationContext,
) -> contracts.NamedSourceRouteResult:
    """Resolve one explicit source mode for the exact selected spell Activity.

    The existing selected-route proof establishes the authentic context, current
    native membership, bound spell, and exact Activity edge first. This result is
    still structural evidence: source availability is copied unchanged and no
    casting, execution, cost, or mutation authority is issued.
    """
    selected_route = _prove_selected_source_route(context)
    rows = tuple(
        row
        for row in context.compiled.cast_source_bindings
        if row.binding.consumer_id == context.consumer_id
        and row.binding.profile_id == selected_route.profile_id
        and row.binding.profile_generation == selected_route.profile_generation
    )
    if (
        len(rows) != 1
        or type(rows[0].binding) is not contracts.CastSourceBinding
        or rows[0].binding.source_spell_id != selected_route.source_spell_id
    ):
        _hold(context)
    source = rows[0]
    spell_definition = source.definition_contracts.get(selected_route.source_spell_id)
    if (
        not isinstance(spell_definition, Mapping)
        or spell_definition.get("id") != selected_route.source_spell_id
        or spell_definition.get("kind") != "definition.spell"
    ):
        _hold(context)
    spell_data = spell_definition.get("data")
    if not isinstance(spell_data, Mapping):
        _hold(context)
    raw_modes = spell_data.get("source_modes")
    if not isinstance(raw_modes, (tuple, list)) or not raw_modes:
        _hold(context)

    source_modes: list[contracts.SourceMode] = []
    seen_mode_ids: set[str] = set()
    for raw_mode in raw_modes:
        if not isinstance(raw_mode, Mapping):
            _hold(context)
        try:
            mode = contracts.SourceMode(**dict(raw_mode))
        except (contracts.ActivityContractError, TypeError):
            _hold(context)
        if mode.mode_id in seen_mode_ids:
            _hold(context)
        seen_mode_ids.add(mode.mode_id)
        source_modes.append(mode)

    matching_modes = tuple(
        mode for mode in source_modes if mode.activity_id == selected_route.activity_id
    )
    if len(matching_modes) != 1:
        _hold(context)
    mode = matching_modes[0]
    activity_definition = source.definition_contracts.get(mode.activity_id)
    source_activity_ids = selected_route.source_activity_ids
    dependency_edge = {
        "source_ref": f"bound_definition:{selected_route.source_spell_id}",
        "dependency_ref": f"bound_definition:{mode.activity_id}",
    }
    definition_edges = {
        (edge.source_ref, edge.dependency_ref) for edge in source.dependency_edges
    }
    if (
        not isinstance(activity_definition, Mapping)
        or activity_definition.get("id") != mode.activity_id
        or activity_definition.get("kind") != "definition.activity"
        or mode.activity_id not in source_activity_ids
        or (dependency_edge["source_ref"], dependency_edge["dependency_ref"])
        not in definition_edges
    ):
        _hold(context)

    context_identity = selected_route.context_identity
    result_value: dict[str, object] = {
        "consumer_id": selected_route.consumer_id,
        "profile_id": selected_route.profile_id,
        "profile_generation": selected_route.profile_generation,
        "source_spell_id": selected_route.source_spell_id,
        "mode_id": mode.mode_id,
        "activity_id": selected_route.activity_id,
        "source_mode_status": "NAMED_ROUTE_RESOLVED",
        "source_disposition": selected_route.source_disposition,
        "source_activity_ids": selected_route.source_activity_ids,
        "mode_declaration": {
            "mode_id": mode.mode_id,
            "activity_id": mode.activity_id,
        },
        "source_spell_definition": spell_definition,
        "selected_activity_definition": activity_definition,
        "source_dependency_edge": dependency_edge,
        "source_read_refs": selected_route.source_read_refs,
        "compiler_generation": context.compiled.compiler_generation,
        "definition_semantic_hash_generation": context.compiled.definition_semantic_hash_generation,
        "definition_semantic_hash": context.compiled.definition_semantic_hash,
        "ruleset_set_digest_generation": context.compiled.ruleset_set_digest_generation,
        "ruleset_set_sha256": context.compiled.ruleset_set_sha256,
        "catalog_context_fingerprint_generation": context.compiled.catalog_context_fingerprint_generation,
        "catalog_context_fingerprint": context.compiled.catalog_context_fingerprint,
        "engine_contract_inventory_sha256": context.compiled.engine_contract_inventory_sha256,
        "command_id": selected_route.command_id,
        "root_resolution_id": selected_route.root_resolution_id,
        "occurrence_id": context.occurrence_id,
        "context_identity": context_identity,
        "membership_identity": selected_route.membership_identity,
        "native_read_fingerprint": selected_route.read_fingerprint,
    }
    try:
        result = contracts.validate_named_source_route_result(
            result_value, context=context
        )
    except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
        raise contracts.NativePreparationHold(
            "AUTHORITY_UNAVAILABLE", context.execution_ref, ()
        ) from error
    if (
        result.value["source_disposition"] != selected_route.source_disposition
        or result.value["context_identity"] != selected_route.context_identity
        or result.value["membership_identity"] != selected_route.membership_identity
        or result.value["native_read_fingerprint"] != selected_route.read_fingerprint
    ):
        _hold(context, "REVALIDATION_REQUIRED")
    return result
