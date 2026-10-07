"""Bounded native Effect/Asset membership preparation from pinned Git trees.

This is a conformance-source adapter, not a production family-enumeration port.
It issues evidence only when the current-owner session is bound to a local
immutable campaign Git tree, P0 resolves every discovered record from that exact
campaign revision, and the relevant LIVE/HOT families have no unsupported
overrides. A normal repository without this bounded acquisition capability holds.
"""

from __future__ import annotations

import base64
import binascii
import json
import math
import re
import subprocess
import threading
import weakref
from collections.abc import Mapping
from dataclasses import dataclass, fields
from pathlib import Path
from types import MappingProxyType
from typing import Final

from . import activity_contracts as contracts
from . import mechanical_context
from .current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    CurrentOwnerSource,
    CurrentOwnerStatus,
    NativeOwnerRef,
)
from .hot_store import NativeHotStore
from .live_state import LiveRouting
from .native_storage import ROUTE_PREFIX, route_native_record
from .policy_basis import PinnedCampaign

# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"

_FAMILY_ROOTS: Final = MappingProxyType(
    {
        "world.effect": "WORLD/EFFECTS/RECORDS",
        "world.asset": "WORLD/ITEMS/RECORDS",
    }
)
_NATIVE_ID: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_OBJECT_ID: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_MAX_LISTING_BYTES: Final = 2 * 1024 * 1024
_MAX_TREE_ENTRIES: Final = 16_384
_MAX_NATIVE_RECORDS: Final = 4_096
_MAX_TREE_DEPTH: Final = 64
_ISSUANCE_LOCK = threading.RLock()
_ISSUED_MEMBERSHIPS: dict[
    int, tuple[weakref.ReferenceType[MembershipObservation], object]
] = {}


class MechanicalSourceError(ValueError):
    """A membership query or retained membership evidence is not authentic."""


@dataclass(frozen=True, slots=True)
class _TreeEntry:
    name: str
    mode: str
    object_type: str
    object_id: str


@dataclass(frozen=True, slots=True)
class _FamilyCoverage:
    family_key: str
    root_path: str
    subtree_id: str | None
    absence_parent_id: str | None
    absent_child: str | None
    files: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class MembershipEffect:
    """One target-local active Effect or a support dependency."""

    owner_ref: NativeOwnerRef
    target_id: str
    lifecycle: str
    source_id: str | None
    rules_origin_id: str | None
    support_effect_id: str | None
    source_basis: str
    fingerprint: str
    is_target_local: bool


@dataclass(frozen=True, slots=True)
class MembershipExclusion:
    """A retained native Effect candidate that does not join target membership."""

    owner_ref: NativeOwnerRef
    target_id: str
    reason: str
    source_basis: str
    fingerprint: str


@dataclass(frozen=True, slots=True)
class MembershipAsset:
    """One Asset in direct ownership, target, or containment closure."""

    owner_ref: NativeOwnerRef
    placement_owner_id: str | None
    container_path: tuple[str, ...]
    equipment_mode: str | None
    accessible: bool
    blocker_asset_id: str | None
    attuned_actor_id: str | None
    conversion_mode: str | None
    source_basis: str
    fingerprint: str


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class MembershipObservation:
    """Recursively immutable, process-local issued membership evidence."""

    campaign_id: str
    source_revision: str
    source_tree_sha: str
    activity_id: str
    consumer_id: str
    subject_actor_ids: tuple[str, ...]
    effects: tuple[MembershipEffect, ...]
    effect_dependencies: tuple[MembershipEffect, ...]
    exclusions: tuple[MembershipExclusion, ...]
    assets: tuple[MembershipAsset, ...]
    family_coverage: tuple[_FamilyCoverage, ...]
    p0_observation: CurrentOwnerObservation
    _context: contracts.NativePreparationContext
    _owner_session: CurrentOwnerReadSession
    _operation_token: object
    _issue_seal: object

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise MechanicalSourceError("membership evidence must be adapter-issued")


@dataclass(frozen=True, slots=True)
class _EffectData:
    owner_ref: NativeOwnerRef
    target_id: str
    lifecycle: str
    source_id: str | None
    rules_origin_id: str | None
    support_effect_id: str | None
    subject_binding: Mapping[str, object] | None
    conversion_state: Mapping[str, object] | None


@dataclass(frozen=True, slots=True)
class _AssetData:
    owner_ref: NativeOwnerRef
    state: Mapping[str, object]
    owner_actor_id: str | None
    container_asset_id: str | None
    location_id: str | None
    access_blocked: bool
    equipment_mode: str | None
    attuned_actor_id: str | None
    conversion_mode: str | None


def prepare_membership(
    context: contracts.NativePreparationContext,
) -> MembershipObservation:
    """Acquire complete pinned Effect/Asset membership for compiled role subjects.

    The only query semantics are the exact accepted root Actor, accepted
    target_ids that have a same-family compiled role binding, directly owned
    Assets, their reverse container descendants and required ancestors. Family
    paths, traversal, target tests and selection rules are fixed here; no caller
    may supply IDs, predicates, a backend, or a completeness assertion.
    """

    compiled, consumer_id, session, pinned, roles, subject_actor_ids, target_assets = (
        _validate_context(context)
    )
    repo_path = _conformance_repository_path(session, context)
    initial_live_basis = _live_family_basis(session._selected_live)
    current_pin, current_live = _fresh_source_basis(session, context)
    if current_pin != pinned:
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "campaign source changed before membership acquisition",
        )
    current_live_basis = _live_family_basis(current_live)
    if current_live_basis != initial_live_basis:
        if current_live_basis:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "selected LIVE Effect/Asset coverage changed before acquisition",
            )
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "selected LIVE source basis changed before membership acquisition",
        )
    _require_pinned_only_current_sources(
        session, context, pinned, selected_live=current_live
    )
    _verify_git_pin(repo_path, pinned, context)

    coverage = tuple(
        _enumerate_family(repo_path, pinned.tree_sha, family, context)
        for family in _FAMILY_ROOTS
    )
    effect_routes = _routes_from_coverage("world.effect", coverage[0], context)
    asset_routes = _routes_from_coverage("world.asset", coverage[1], context)
    all_routes = (*effect_routes, *asset_routes)
    if len(all_routes) > _MAX_NATIVE_RECORDS:
        _hold(
            context,
            "CAPACITY_REQUIRED",
            "native membership source exceeds its bounded record capacity",
        )

    initial_refs = tuple(
        sorted(
            set(roles) | {route_ref for route_ref, _path, _blob_id in all_routes},
            key=_owner_key,
        )
    )
    p0_observation = _require_p0_reads(session, initial_refs, pinned, context)

    effects_by_id: dict[str, _EffectData] = {}
    effect_reads: dict[str, object] = {}
    for owner_ref, _path, blob_id in effect_routes:
        read = p0_observation.require(owner_ref)
        payload = read.payload
        if payload is None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "enumerated Effect payload is unavailable",
            )
        _require_blob_payload_matches(repo_path, blob_id, payload, "Effect", context)
        effect = _validate_effect(owner_ref, payload, context)
        effects_by_id[owner_ref.identity[0]] = effect
        effect_reads[owner_ref.identity[0]] = read

    assets_by_id: dict[str, _AssetData] = {}
    asset_reads: dict[str, object] = {}
    for owner_ref, _path, blob_id in asset_routes:
        read = p0_observation.require(owner_ref)
        payload = read.payload
        if payload is None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "enumerated Asset payload is unavailable",
            )
        _require_blob_payload_matches(repo_path, blob_id, payload, "Asset", context)
        asset = _validate_asset(owner_ref, payload, context)
        assets_by_id[owner_ref.identity[0]] = asset
        asset_reads[owner_ref.identity[0]] = read

    _validate_native_references(effects_by_id, assets_by_id, context)
    asset_closure = _asset_closure(
        assets_by_id,
        subject_actor_ids,
        target_assets,
        context,
    )
    target_ids = set(subject_actor_ids) | set(asset_closure)
    _hold_unqualified_asset_profiles(
        subject_actor_ids=subject_actor_ids,
        target_ids=target_ids,
        asset_closure=asset_closure,
        assets=assets_by_id,
        effects=effects_by_id,
        p0_observation=p0_observation,
        context=context,
    )

    effects: list[MembershipEffect] = []
    exclusions: list[MembershipExclusion] = []
    target_effect_ids: set[str] = set()
    for effect_id, effect in effects_by_id.items():
        if effect.target_id not in target_ids:
            if effect.source_id in target_ids or _binding_mentions(
                effect.subject_binding, target_ids
            ):
                exclusions.append(
                    _effect_exclusion(
                        effect,
                        effect_reads[effect_id],
                        "not_target_local",
                    )
                )
            continue
        if effect.lifecycle == "effect_lifecycle.terminal":
            exclusions.append(
                _effect_exclusion(effect, effect_reads[effect_id], "terminal")
            )
            continue
        if effect.subject_binding is not None:
            if effect.target_id in subject_actor_ids and _binding_is_definitely_foreign(
                effect.subject_binding, effect.target_id
            ):
                exclusions.append(
                    _effect_exclusion(
                        effect,
                        effect_reads[effect_id],
                        "wrong_subject_binding",
                    )
                )
                continue
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "target-local Effect has a subject generation not bound by this compiled preparation",
            )
        target_effect_ids.add(effect_id)
        effects.append(_effect_member(effect, effect_reads[effect_id], True))

    dependency_ids: set[str] = set()
    pending = list(target_effect_ids)
    while pending:
        effect_id = pending.pop()
        parent_id = effects_by_id[effect_id].support_effect_id
        if (
            parent_id is None
            or parent_id in dependency_ids
            or parent_id in target_effect_ids
        ):
            continue
        parent = effects_by_id.get(parent_id)
        if parent is None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Effect support parent is absent from the complete family tree",
            )
        if parent.lifecycle != "effect_lifecycle.active":
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "active Effect has a terminal support parent",
            )
        if parent.subject_binding is not None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Effect support dependency has an unbound subject generation",
            )
        dependency_ids.add(parent_id)
        pending.append(parent_id)

    dependencies = [
        _effect_member(effects_by_id[item], effect_reads[item], False)
        for item in sorted(dependency_ids)
    ]
    assets = [
        _asset_member(
            assets_by_id[asset_id],
            asset_reads[asset_id],
            assets_by_id,
            subject_actor_ids,
            context,
        )
        for asset_id in sorted(asset_closure)
    ]

    # Assets can name source Effects; they are references, not permission to
    # synthesize a duplicate Effect or its mechanical contribution.
    for asset_id in asset_closure:
        asset = assets_by_id[asset_id]
        if not _asset_effect_reference_present(asset.state, effects_by_id):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset conversion/equipment Effect reference is unresolved",
            )

    _confirm_acquisition_currentness(
        session=session,
        p0_observation=p0_observation,
        repository=repo_path,
        pinned=pinned,
        family_coverage=coverage,
        initial_live_basis=initial_live_basis,
        context=context,
    )

    return _issue_membership(
        campaign_id=pinned.campaign_id,
        source_revision=pinned.revision,
        source_tree_sha=pinned.tree_sha,
        activity_id=compiled.activity_id,
        consumer_id=consumer_id,
        subject_actor_ids=tuple(sorted(subject_actor_ids)),
        effects=tuple(sorted(effects, key=lambda item: _owner_key(item.owner_ref))),
        effect_dependencies=tuple(
            sorted(dependencies, key=lambda item: _owner_key(item.owner_ref))
        ),
        exclusions=tuple(
            sorted(
                exclusions, key=lambda item: (_owner_key(item.owner_ref), item.reason)
            )
        ),
        assets=tuple(assets),
        family_coverage=coverage,
        p0_observation=p0_observation,
        context=context,
        owner_session=session,
        operation_token=session.operation_token,
    )


def is_membership_issued(value: object) -> bool:
    """Return whether this exact immutable membership object has valid issuance."""

    if type(value) is not MembershipObservation:
        return False
    with _ISSUANCE_LOCK:
        record = _ISSUED_MEMBERSHIPS.get(id(value))
    if record is None or record[0]() is not value:
        return False
    try:
        return record[1] == _membership_snapshot(value)
    except (AttributeError, RecursionError, TypeError, ValueError):
        return False


def revalidate_membership(
    observation: MembershipObservation,
    context: contracts.NativePreparationContext,
) -> bool:
    """Reacquire the same bounded family coverage and all exact P0 reads."""

    if not is_membership_issued(observation):
        raise MechanicalSourceError(
            "membership observation is copied, forged, or mutated"
        )
    if (
        type(context) is not contracts.NativePreparationContext
        or context is not observation._context
    ):
        raise MechanicalSourceError(
            "membership observation is rebound to another preparation context"
        )
    if (
        context.owner_session is not observation._owner_session
        or context.owner_session.operation_token is not observation._operation_token
        or context.compiled.activity_id != observation.activity_id
        or context.consumer_id != observation.consumer_id
    ):
        raise MechanicalSourceError(
            "membership observation has foreign operation or compiler lineage"
        )
    try:
        fresh_pin, fresh_live = _fresh_source_basis(observation._owner_session, context)
        if (
            fresh_pin.campaign_id != observation.campaign_id
            or fresh_pin.revision != observation.source_revision
            or fresh_pin.tree_sha != observation.source_tree_sha
        ):
            return False
        _require_pinned_only_current_sources(
            observation._owner_session,
            context,
            fresh_pin,
            selected_live=fresh_live,
        )
        if not observation._owner_session.revalidate(observation.p0_observation):
            return False
        repo_path = _conformance_repository_path(observation._owner_session, context)
        pinned = observation._owner_session._pinned_campaign
        if type(pinned) is not PinnedCampaign or (
            pinned.campaign_id != observation.campaign_id
            or pinned.revision != observation.source_revision
            or pinned.tree_sha != observation.source_tree_sha
        ):
            return False
        _verify_git_pin(repo_path, pinned, context)
        fresh_coverage = tuple(
            _enumerate_family(repo_path, pinned.tree_sha, family, context)
            for family in _FAMILY_ROOTS
        )
        if fresh_coverage != observation.family_coverage:
            return False
        confirmed_pin, confirmed_live = _fresh_source_basis(
            observation._owner_session, context
        )
        if confirmed_pin != fresh_pin:
            return False
        _require_pinned_only_current_sources(
            observation._owner_session,
            context,
            confirmed_pin,
            selected_live=confirmed_live,
        )
    except (OSError, TypeError, ValueError, subprocess.SubprocessError):
        return False
    return True


def _validate_context(
    context: contracts.NativePreparationContext,
) -> tuple[
    contracts.CompiledActivity,
    str,
    CurrentOwnerReadSession,
    PinnedCampaign,
    tuple[NativeOwnerRef, ...],
    set[str],
    set[str],
]:
    if type(context) is not contracts.NativePreparationContext:
        raise MechanicalSourceError(
            "membership requires a typed native preparation context"
        )
    compiled = context.compiled
    if (
        not contracts._compiler_value_is_issued(
            compiled, kind="compiled", parent=context.catalog.catalog_context
        )
        or not contracts._compiler_value_is_issued(context.catalog, kind="catalog")
        or context.catalog.compiled_activities.get(compiled.activity_id) is not compiled
    ):
        raise MechanicalSourceError(
            "membership requires the exact compiler-issued catalog and Activity"
        )
    consumer_id = context.consumer_id
    mechanical_context._instruction(compiled, consumer_id)
    session = context.owner_session
    if type(session) is not CurrentOwnerReadSession:
        raise MechanicalSourceError(
            "membership requires the operation-scoped P0 current-owner session"
        )
    if session.operation_token is not context.observation.operation_token:
        raise MechanicalSourceError(
            "membership context observation belongs to another operation"
        )
    try:
        roles = mechanical_context._roles(compiled, context.role_bindings)
        command = mechanical_context._accepted_command(
            compiled, context.accepted_command
        )
    except (KeyError, TypeError, ValueError) as error:
        raise MechanicalSourceError(
            "membership context has invalid compiled role/command bindings"
        ) from error
    request = command.get("action_request")
    if (
        not isinstance(request, Mapping)
        or request.get("activity_id") != compiled.activity_id
    ):
        raise MechanicalSourceError(
            "membership command differs from its compiled Activity"
        )
    actor = context.role_bindings.get("actor")
    if (
        type(actor) is not NativeOwnerRef
        or actor.family_key != "world.actor"
        or actor.identity != (request.get("actor_id"),)
    ):
        raise MechanicalSourceError(
            "membership root Actor role differs from accepted command"
        )
    target_value = request.get("target_ids", ())
    if not isinstance(target_value, (list, tuple)) or any(
        not isinstance(item, str) or not item for item in target_value
    ):
        raise MechanicalSourceError("membership accepted targets are malformed")
    target_ids = tuple(target_value)
    if len(target_ids) != len(set(target_ids)):
        raise MechanicalSourceError("membership accepted targets are not unique")
    actor_ids = {actor.identity[0]}
    asset_ids = {
        owner.identity[0] for owner in roles if owner.family_key == "world.asset"
    }
    owners_by_identity = {
        (owner.family_key, owner.identity[0]): owner
        for owner in roles
        if owner.family_key in {"world.actor", "world.asset"}
        and len(owner.identity) == 1
    }
    for target_id in target_ids:
        matches = [
            owner
            for (family, identity), owner in owners_by_identity.items()
            if identity == target_id and family in {"world.actor", "world.asset"}
        ]
        if len(matches) != 1:
            raise MechanicalSourceError(
                "accepted target lacks one exact compiled Actor/Asset role"
            )
        if matches[0].family_key == "world.actor":
            actor_ids.add(target_id)
        else:
            asset_ids.add(target_id)
    pinned = session._pinned_campaign
    if type(pinned) is not PinnedCampaign or pinned.campaign_id != session._campaign_id:
        raise MechanicalSourceError("membership operation has no exact pinned campaign")
    if not session.revalidate(context.observation):
        _hold(context, "REVALIDATION_REQUIRED", "preparation P0 observation is stale")
    return compiled, consumer_id, session, pinned, roles, actor_ids, asset_ids


def _conformance_repository_path(
    session: CurrentOwnerReadSession,
    context: contracts.NativePreparationContext,
) -> Path:
    reader = session._reader
    reader_owner = getattr(reader, "__self__", None)
    repository = getattr(reader_owner, "_repository", reader_owner)
    raw_path = getattr(repository, "sp03_git_repository_path", None)
    if not isinstance(raw_path, (str, Path)) or not raw_path:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "current-owner repository has no bounded Git-tree acquisition",
        )
    try:
        path = Path(raw_path).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise _hold_error(
            context, "AUTHORITY_UNAVAILABLE", "conformance Git source is unavailable"
        ) from error
    if not path.is_dir():
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "conformance Git source is not a repository directory",
        )
    return path


def _fresh_source_basis(
    session: CurrentOwnerReadSession,
    context: contracts.NativePreparationContext,
) -> tuple[PinnedCampaign, LiveRouting | None]:
    try:
        pinned, selected_live = session._source_basis_reader(session._pinned_campaign)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
        raise _hold_error(
            context,
            "AUTHORITY_UNAVAILABLE",
            "fresh campaign/LIVE source basis is unavailable",
        ) from error
    if (
        type(pinned) is not PinnedCampaign
        or pinned.campaign_id != session._campaign_id
        or selected_live is not None
        and type(selected_live) is not LiveRouting
    ):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "fresh campaign/LIVE source basis has a foreign identity or shape",
        )
    return pinned, selected_live


def _live_family_basis(routing: LiveRouting | None) -> tuple[object, ...]:
    if routing is None:
        return ()
    basis: list[tuple[object, ...]] = []
    for source in routing.entries:
        relevant_claims = tuple(
            sorted(
                claim.identity_key
                for claim in source.claims
                if claim.native_family in _FAMILY_ROOTS
            )
        )
        if relevant_claims:
            basis.append(
                (
                    source.source_key,
                    source.source_revision,
                    source.status.value,
                    relevant_claims,
                )
            )
    return tuple(sorted(basis))


def _require_pinned_only_current_sources(
    session: CurrentOwnerReadSession,
    context: contracts.NativePreparationContext,
    pinned: PinnedCampaign,
    *,
    selected_live: LiveRouting | None,
) -> None:
    if _live_family_basis(selected_live):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "LIVE Effect/Asset membership lacks complete family coverage",
        )
    store = session._hot_store
    if type(store) is not NativeHotStore:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "HOT membership coverage is not available for this conformance source",
        )
    with store._lock:
        if any(
            campaign_id == pinned.campaign_id and family_key in _FAMILY_ROOTS
            for campaign_id, family_key, _identity in store._admitted_rows
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "admitted HOT Effect/Asset membership has no complete roster",
            )


def _confirm_acquisition_currentness(
    *,
    session: CurrentOwnerReadSession,
    p0_observation: CurrentOwnerObservation,
    repository: Path,
    pinned: PinnedCampaign,
    family_coverage: tuple[_FamilyCoverage, ...],
    initial_live_basis: tuple[object, ...],
    context: contracts.NativePreparationContext,
) -> None:
    if not session.revalidate(p0_observation):
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "P0 current-owner source advanced during membership acquisition",
        )
    confirmed_pin, confirmed_live = _fresh_source_basis(session, context)
    if confirmed_pin != pinned:
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "campaign pin advanced during membership acquisition",
        )
    confirmed_live_basis = _live_family_basis(confirmed_live)
    if confirmed_live_basis != initial_live_basis:
        if confirmed_live_basis:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "LIVE Effect/Asset coverage changed during membership acquisition",
            )
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "LIVE source basis changed during membership acquisition",
        )
    _require_pinned_only_current_sources(
        session, context, confirmed_pin, selected_live=confirmed_live
    )
    _verify_git_pin(repository, confirmed_pin, context)
    confirmed_coverage = tuple(
        _enumerate_family(repository, confirmed_pin.tree_sha, family, context)
        for family in _FAMILY_ROOTS
    )
    if confirmed_coverage != family_coverage:
        _hold(
            context,
            "REVALIDATION_REQUIRED",
            "native family coverage changed during membership acquisition",
        )


def _verify_git_pin(
    repository: Path,
    pinned: PinnedCampaign,
    context: contracts.NativePreparationContext,
) -> None:
    if not _OBJECT_ID.fullmatch(pinned.revision) or not _OBJECT_ID.fullmatch(
        pinned.tree_sha
    ):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "current-owner pin is not an exact Git commit/tree identity",
        )
    commit = _git_output(
        repository, ("rev-parse", "--verify", f"{pinned.revision}^{{commit}}"), context
    )
    tree = _git_output(
        repository, ("rev-parse", "--verify", f"{pinned.revision}^{{tree}}"), context
    )
    if commit != pinned.revision or tree != pinned.tree_sha:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "current-owner pin does not match the immutable campaign Git tree",
        )


def _enumerate_family(
    repository: Path,
    root_tree_sha: str,
    family: str,
    context: contracts.NativePreparationContext,
) -> _FamilyCoverage:
    root_path = _FAMILY_ROOTS[family]
    parent_id = root_tree_sha
    components = root_path.split("/")
    for component in components:
        entries = _list_tree(repository, parent_id, context)
        matches = [entry for entry in entries if entry.name == component]
        if not matches:
            return _FamilyCoverage(
                family,
                root_path,
                None,
                parent_id,
                component,
                (),
            )
        if (
            len(matches) != 1
            or matches[0].mode != "040000"
            or matches[0].object_type != "tree"
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native membership path has a duplicate or non-tree parent",
            )
        parent_id = matches[0].object_id

    pending: list[tuple[str, str, int]] = [("", parent_id, 0)]
    files: list[tuple[str, str]] = []
    entry_count = 0
    while pending:
        relative, tree_id, depth = pending.pop()
        if depth > _MAX_TREE_DEPTH:
            _hold(
                context,
                "CAPACITY_REQUIRED",
                "native membership tree exceeds the bounded traversal depth",
            )
        entries = _list_tree(repository, tree_id, context)
        if relative and not entries:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native record subtree contains an empty non-route directory",
            )
        entry_count += len(entries)
        if entry_count > _MAX_TREE_ENTRIES:
            _hold(
                context,
                "CAPACITY_REQUIRED",
                "native membership tree exceeds the bounded traversal capacity",
            )
        for entry in entries:
            child = f"{relative}/{entry.name}" if relative else entry.name
            if entry.mode == "040000" and entry.object_type == "tree":
                pending.append((child, entry.object_id, depth + 1))
            elif entry.mode == "100644" and entry.object_type == "blob":
                files.append((child, entry.object_id))
            else:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native membership tree contains a symlink, submodule, or malformed object",
                )
            if len(files) > _MAX_NATIVE_RECORDS:
                _hold(
                    context,
                    "CAPACITY_REQUIRED",
                    "native membership family exceeds its bounded record capacity",
                )
    return _FamilyCoverage(
        family,
        root_path,
        parent_id,
        None,
        None,
        tuple(sorted(files)),
    )


def _list_tree(
    repository: Path,
    tree_id: str,
    context: contracts.NativePreparationContext,
) -> tuple[_TreeEntry, ...]:
    if not _OBJECT_ID.fullmatch(tree_id):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Git tree object identity is malformed")
    result = _run_git(repository, ("ls-tree", "-z", tree_id), context)
    if len(result) > _MAX_LISTING_BYTES:
        _hold(
            context,
            "CAPACITY_REQUIRED",
            "one native Git tree listing exceeds its byte capacity",
        )
    if not result:
        return ()
    if not result.endswith(b"\0"):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Git tree listing is truncated")
    parsed: list[_TreeEntry] = []
    names: set[str] = set()
    for raw_entry in result[:-1].split(b"\0"):
        try:
            raw_metadata, raw_name = raw_entry.split(b"\t", 1)
            raw_mode, raw_type, raw_object_id = raw_metadata.split(b" ", 2)
            name = raw_name.decode("utf-8")
            mode = raw_mode.decode("ascii")
            object_type = raw_type.decode("ascii")
            object_id = raw_object_id.decode("ascii")
        except (UnicodeDecodeError, ValueError) as error:
            raise _hold_error(
                context, "AUTHORITY_UNAVAILABLE", "Git tree entry is malformed"
            ) from error
        if (
            not name
            or "/" in name
            or "\x00" in name
            or name in {".", ".."}
            or name in names
            or not _OBJECT_ID.fullmatch(object_id)
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Git tree entry has invalid or duplicate identity",
            )
        names.add(name)
        parsed.append(_TreeEntry(name, mode, object_type, object_id))
    return tuple(parsed)


def _run_git(
    repository: Path,
    arguments: tuple[str, ...],
    context: contracts.NativePreparationContext,
) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=False,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise _hold_error(
            context, "AUTHORITY_UNAVAILABLE", "pinned native Git object read failed"
        ) from error
    if result.returncode != 0:
        _hold(
            context, "AUTHORITY_UNAVAILABLE", "pinned native Git object is unavailable"
        )
    if len(result.stdout) > _MAX_LISTING_BYTES:
        _hold(
            context,
            "CAPACITY_REQUIRED",
            "native Git object output exceeds its byte capacity",
        )
    return result.stdout


def _git_output(
    repository: Path,
    arguments: tuple[str, ...],
    context: contracts.NativePreparationContext,
) -> str:
    output = _run_git(repository, arguments, context)
    try:
        return output.decode("ascii").strip()
    except UnicodeDecodeError as error:
        raise _hold_error(
            context, "AUTHORITY_UNAVAILABLE", "Git pin output is malformed"
        ) from error


def _routes_from_coverage(
    family: str,
    coverage: _FamilyCoverage,
    context: contracts.NativePreparationContext,
) -> tuple[tuple[NativeOwnerRef, str, str], ...]:
    routes: list[tuple[NativeOwnerRef, str, str]] = []
    seen: set[tuple[str, ...]] = set()
    prefix = f"{coverage.root_path}/"
    for relative_path, object_id in coverage.files:
        full_path = prefix + relative_path
        identity = _decode_route(family, full_path, context)
        if identity in seen:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native family tree duplicates a full native identity",
            )
        seen.add(identity)
        owner_ref = NativeOwnerRef(family, identity)
        route = route_native_record(family, identity)
        if route.relative_path != full_path:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native record path differs from WP-11 route",
            )
        routes.append((owner_ref, full_path, object_id))
    return tuple(sorted(routes, key=lambda item: _owner_key(item[0])))


def _require_blob_payload_matches(
    repository: Path,
    blob_id: str,
    p0_payload: Mapping[str, object],
    family_label: str,
    context: contracts.NativePreparationContext,
) -> None:
    raw_blob = _run_git(repository, ("cat-file", "blob", blob_id), context)
    try:
        parsed_blob = json.loads(
            raw_blob.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
        p0_canonical = json.dumps(
            dict(p0_payload),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        blob_canonical = json.dumps(
            parsed_blob,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError, UnicodeDecodeError) as error:
        raise _hold_error(
            context,
            "AUTHORITY_UNAVAILABLE",
            f"{family_label} Git blob cannot be matched to the P0 parser value",
        ) from error
    if not isinstance(parsed_blob, Mapping) or p0_canonical != blob_canonical:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            f"{family_label} P0 payload differs from its enumerated immutable Git blob",
        )


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Git JSON blob repeats an object key")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Git JSON blob uses nonstandard constant {value}")


def _decode_route(
    family: str,
    path: str,
    context: contracts.NativePreparationContext,
) -> tuple[str, ...]:
    parts = path.split("/")
    prefix = _FAMILY_ROOTS[family].split("/")
    if (
        len(parts) < len(prefix) + 3
        or parts[: len(prefix)] != prefix
        or not re.fullmatch(r"[0-9a-f]{2}", parts[len(prefix)])
        or not re.fullmatch(r"[0-9a-f]{2}", parts[len(prefix) + 1])
        or not parts[-1].endswith(".yaml")
    ):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "native family contains a non-WP-11 document path",
        )
    chunks = [*parts[len(prefix) + 2 : -1], parts[-1][:-5]]
    encoded = "".join(chunks)
    if not encoded or any(
        character not in "0123456789ABCDEFGHIJKLMNOPQRSTUV" for character in encoded
    ):
        _hold(context, "AUTHORITY_UNAVAILABLE", "native route encoding is malformed")
    padded = encoded + "=" * ((8 - len(encoded) % 8) % 8)
    try:
        framed = base64.b32hexdecode(padded)
    except (binascii.Error, ValueError) as error:
        raise _hold_error(
            context, "AUTHORITY_UNAVAILABLE", "native route encoding cannot be decoded"
        ) from error
    family_prefix = ROUTE_PREFIX + b"\x00" + family.encode("utf-8") + b"\x00"
    if not framed.startswith(family_prefix) or len(framed) < len(family_prefix) + 4:
        _hold(context, "AUTHORITY_UNAVAILABLE", "native route encodes a foreign family")
    offset = len(family_prefix)
    count = int.from_bytes(framed[offset : offset + 4], "big")
    offset += 4
    if not 1 <= count <= 8:
        _hold(
            context, "AUTHORITY_UNAVAILABLE", "native route identity arity is invalid"
        )
    identity: list[str] = []
    for _ in range(count):
        if offset + 4 > len(framed):
            _hold(
                context, "AUTHORITY_UNAVAILABLE", "native route identity is truncated"
            )
        size = int.from_bytes(framed[offset : offset + 4], "big")
        offset += 4
        if size < 1 or offset + size > len(framed):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native route identity component is truncated",
            )
        try:
            component = framed[offset : offset + size].decode("utf-8")
        except UnicodeDecodeError as error:
            raise _hold_error(
                context, "AUTHORITY_UNAVAILABLE", "native route identity is not UTF-8"
            ) from error
        if _NATIVE_ID.fullmatch(component) is None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native route identity component is not canonical",
            )
        identity.append(component)
        offset += size
    if offset != len(framed):
        _hold(context, "AUTHORITY_UNAVAILABLE", "native route has trailing bytes")
    return tuple(identity)


def _require_p0_reads(
    session: CurrentOwnerReadSession,
    owner_refs: tuple[NativeOwnerRef, ...],
    pinned: PinnedCampaign,
    context: contracts.NativePreparationContext,
) -> CurrentOwnerObservation:
    if not owner_refs:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "membership query has no P0 owner bindings",
        )
    try:
        observation = session.require(owner_refs)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
        raise _hold_error(
            context, "AUTHORITY_UNAVAILABLE", "P0 membership reads are unavailable"
        ) from error
    for owner_ref in observation.key_union:
        read = observation.require(owner_ref)
        if (
            read.status is not CurrentOwnerStatus.RESOLVED
            or read.source is not CurrentOwnerSource.PINNED_CAMPAIGN
            or read.source_basis != pinned.revision
            or read.payload is None
            or not read.fingerprint
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "membership requires complete exact pinned-campaign P0 reads",
            )
    return observation


def _validate_effect(
    owner_ref: NativeOwnerRef,
    payload: Mapping[str, object],
    context: contracts.NativePreparationContext,
) -> _EffectData:
    _strict_fields(
        payload,
        {"schema_version", "id", "kind", "definition_id", "state"},
        {"schema_version", "id", "kind", "definition_id", "state"},
        "Effect envelope",
        context,
    )
    if (
        type(payload["schema_version"]) is not int
        or payload["schema_version"] != 2
        or payload["kind"] != "world.effect"
        or payload["id"] != owner_ref.identity[0]
        or not _is_id(payload["definition_id"])
        or not isinstance(payload["state"], Mapping)
    ):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "native Effect envelope identity or schema is malformed",
        )
    state = payload["state"]
    allowed = {
        "target_id",
        "source_id",
        "rules_origin_id",
        "application_order_key",
        "parameters",
        "support_effect_id",
        "temporal_binding",
        "scheduled_trigger_state",
        "lifecycle",
        "subject_binding",
        "form_state",
        "concentration_state",
        "identity_state",
        "conversion_state",
        "control_state",
        "spell_progress",
        "duplicate_count",
        "details",
    }
    _strict_fields(state, allowed, {"target_id", "lifecycle"}, "Effect state", context)
    target_id = _require_id(state["target_id"], "Effect target_id", context)
    lifecycle = state["lifecycle"]
    if not isinstance(lifecycle, Mapping):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Effect lifecycle is malformed")
    state_id = lifecycle.get("state_id")
    if state_id == "effect_lifecycle.active":
        if set(lifecycle) != {"state_id"}:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "active Effect lifecycle has foreign fields",
            )
    elif state_id == "effect_lifecycle.terminal":
        if set(lifecycle) != {"state_id", "terminal_reason_id"} or lifecycle.get(
            "terminal_reason_id"
        ) not in {
            "effect_end.expired",
            "effect_end.removed",
            "effect_end.replaced",
            "effect_end.support_lost",
        }:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "terminal Effect lifecycle is malformed",
            )
    else:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "Effect lifecycle discriminator is unsupported",
        )
    source_id = _optional_id(state, "source_id", context)
    rules_origin_id = _optional_id(state, "rules_origin_id", context)
    support_effect_id = _optional_id(state, "support_effect_id", context)
    if "application_order_key" in state and (
        type(state["application_order_key"]) is not int
        or state["application_order_key"] < 1
    ):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Effect application order is malformed")
    if "parameters" in state:
        parameters = state["parameters"]
        if not isinstance(parameters, Mapping) or any(
            not _is_id(key) or not _is_scalar(value)
            for key, value in parameters.items()
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Effect parameters are not native scalar values",
            )
    if "duplicate_count" in state and (
        type(state["duplicate_count"]) is not int
        or not 0 <= state["duplicate_count"] <= 3
    ):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Effect duplicate_count is malformed")
    subject_binding = state.get("subject_binding")
    if subject_binding is not None:
        _validate_effect_subject_binding(subject_binding, context)
    for name in (
        "temporal_binding",
        "scheduled_trigger_state",
        "form_state",
        "concentration_state",
        "identity_state",
        "conversion_state",
        "control_state",
        "spell_progress",
        "details",
    ):
        if name in state and not isinstance(state[name], Mapping):
            _hold(context, "AUTHORITY_UNAVAILABLE", f"Effect {name} is malformed")
    if "temporal_binding" in state:
        _validate_schema(
            "https://hedgelion.invalid/schemas/temporal-binding.schema.json",
            state["temporal_binding"],
            "Effect temporal binding",
            context,
        )
    if "scheduled_trigger_state" in state:
        trigger_state = state["scheduled_trigger_state"]
        if not trigger_state:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Effect scheduled trigger state is empty",
            )
        for trigger_key, occurrence in trigger_state.items():
            if (
                not isinstance(trigger_key, str)
                or re.fullmatch(r"[a-z][a-z0-9_]*", trigger_key) is None
            ):
                _hold(
                    context, "AUTHORITY_UNAVAILABLE", "Effect trigger key is malformed"
                )
            _validate_schema(
                "https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json#/$defs/temporalOccurrence",
                occurrence,
                "Effect scheduled trigger occurrence",
                context,
            )
    profile_contracts = {
        "form_state": "formState",
        "concentration_state": "concentrationState",
        "identity_state": "identityState",
        "conversion_state": "conversionState",
        "control_state": "controlState",
        "spell_progress": "progressMap",
    }
    for name, contract_name in profile_contracts.items():
        if name in state:
            _validate_schema(
                "https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json#/$defs/"
                + contract_name,
                state[name],
                f"Effect {name}",
                context,
            )
    if "details" in state:
        try:
            contracts.validate_nonexecutable_details(state["details"])
        except contracts.ActivityContractError as error:
            raise _hold_error(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Effect details are not descriptive-only",
            ) from error
    if state_id == "effect_lifecycle.terminal" and "scheduled_trigger_state" in state:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "terminal Effect retains scheduled trigger state",
        )
    return _EffectData(
        owner_ref,
        target_id,
        state_id,
        source_id,
        rules_origin_id,
        support_effect_id,
        subject_binding,
        state.get("conversion_state"),
    )


def _validate_effect_subject_binding(
    value: object,
    context: contracts.NativePreparationContext,
) -> None:
    if not isinstance(value, Mapping):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Effect subject binding is malformed")
    allowed = {
        "domain",
        "principal_subject_id",
        "physical_actor_id",
        "relation_effect_id",
        "binding_generation",
        "rebind_event_id",
    }
    _strict_fields(
        value,
        allowed,
        {"domain", "principal_subject_id", "binding_generation"},
        "Effect subject binding",
        context,
    )
    if value["domain"] not in {"physical", "mental", "identity"}:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "Effect subject binding domain is unsupported",
        )
    _require_id(value["principal_subject_id"], "Effect principal subject", context)
    if type(value["binding_generation"]) is not int or value["binding_generation"] < 1:
        _hold(
            context, "AUTHORITY_UNAVAILABLE", "Effect subject generation is malformed"
        )
    if value["domain"] == "physical" and "physical_actor_id" not in value:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "physical Effect subject lacks its carrier",
        )
    for name in ("physical_actor_id", "relation_effect_id", "rebind_event_id"):
        if name in value:
            _require_id(value[name], f"Effect {name}", context)


def _binding_is_definitely_foreign(
    binding: Mapping[str, object], target_id: str
) -> bool:
    principal = binding.get("principal_subject_id")
    carrier = binding.get("physical_actor_id")
    if binding.get("domain") == "physical":
        return carrier != target_id and principal != target_id
    return principal != target_id and carrier != target_id


def _binding_mentions(
    binding: Mapping[str, object] | None,
    target_ids: set[str],
) -> bool:
    return binding is not None and bool(
        target_ids.intersection(
            value
            for name, value in binding.items()
            if name in {"principal_subject_id", "physical_actor_id"}
            and isinstance(value, str)
        )
    )


def _validate_asset(
    owner_ref: NativeOwnerRef,
    payload: Mapping[str, object],
    context: contracts.NativePreparationContext,
) -> _AssetData:
    _strict_fields(
        payload,
        {"id", "kind", "definition_id", "state"},
        {"id", "kind", "definition_id", "state"},
        "Asset envelope",
        context,
    )
    if (
        payload["kind"] != "world.asset"
        or payload["id"] != owner_ref.identity[0]
        or not _is_id(payload["definition_id"])
        or not isinstance(payload["state"], Mapping)
    ):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "native Asset envelope identity or schema is malformed",
        )
    state = payload["state"]
    allowed = {
        "owner_actor_id",
        "container_asset_id",
        "location_id",
        "quantity",
        "equipment",
        "attuned_actor_id",
        "resources",
        "durability",
        "access",
        "equipment_transform",
        "replica_origin",
        "conversion_membership",
        "spell_progress",
        "details",
    }
    _strict_fields(state, allowed, set(), "Asset state", context)
    placements = [
        name
        for name in ("owner_actor_id", "container_asset_id", "location_id")
        if name in state
    ]
    if len(placements) > 1:
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "Asset has mutually exclusive native placements",
        )
    owner_actor_id = _optional_id(state, "owner_actor_id", context)
    container_asset_id = _optional_id(state, "container_asset_id", context)
    location_id = _optional_id(state, "location_id", context)
    if "quantity" in state and (
        type(state["quantity"]) is not int or state["quantity"] < 1
    ):
        _hold(context, "AUTHORITY_UNAVAILABLE", "Asset quantity is malformed")
    equipment_mode: str | None = None
    if "equipment" in state:
        equipment = state["equipment"]
        if (
            not isinstance(equipment, Mapping)
            or set(equipment) != {"mode"}
            or equipment.get("mode") not in {"held", "worn"}
        ):
            _hold(
                context, "AUTHORITY_UNAVAILABLE", "Asset equipment state is malformed"
            )
        equipment_mode = str(equipment["mode"])
    attuned_actor_id = _optional_id(state, "attuned_actor_id", context)
    if "resources" in state:
        resources = state["resources"]
        if not isinstance(resources, Mapping):
            _hold(context, "AUTHORITY_UNAVAILABLE", "Asset resources are malformed")
        for key, value in resources.items():
            if (
                not _is_id(key)
                or not isinstance(value, Mapping)
                or set(value) - {"current", "recovery_binding"}
                or "current" not in value
            ):
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "Asset resource state is malformed",
                )
            current = value["current"]
            if (
                type(current) not in (int, float)
                or current < 0
                or not math.isfinite(current)
            ):
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "Asset resource current value is malformed",
                )
            if "recovery_binding" in value:
                _validate_schema(
                    "https://hedgelion.invalid/schemas/temporal-binding.schema.json",
                    value["recovery_binding"],
                    "Asset resource recovery binding",
                    context,
                )
    if "durability" in state:
        durability = state["durability"]
        if (
            not isinstance(durability, Mapping)
            or set(durability) != {"hp_current"}
            or type(durability.get("hp_current")) is not int
            or durability["hp_current"] < 0
        ):
            _hold(
                context, "AUTHORITY_UNAVAILABLE", "Asset durability state is malformed"
            )
    if "access" in state and state["access"] != "blocked":
        _hold(context, "AUTHORITY_UNAVAILABLE", "Asset access obstacle is unsupported")
    conversion_mode: str | None = None
    if "equipment_transform" in state:
        transform = state["equipment_transform"]
        if (
            not isinstance(transform, Mapping)
            or set(transform)
            != {"source_effect_id", "transition_occurrence_id", "mode"}
            or transform.get("mode") not in {"merged", "resized"}
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset equipment transform is malformed",
            )
        for field in ("source_effect_id", "transition_occurrence_id"):
            _require_id(transform[field], f"Asset transform {field}", context)
    if "replica_origin" in state:
        replica = state["replica_origin"]
        if not isinstance(replica, Mapping) or set(replica) != {
            "source_asset_id",
            "relation_effect_id",
            "creation_occurrence_id",
        }:
            _hold(context, "AUTHORITY_UNAVAILABLE", "Asset replica origin is malformed")
        for field in replica:
            _require_id(replica[field], f"Asset replica {field}", context)
    if "conversion_membership" in state:
        membership = state["conversion_membership"]
        if (
            not isinstance(membership, Mapping)
            or set(membership)
            != {
                "conversion_effect_id",
                "principal_subject_id",
                "binding_generation",
                "mode",
            }
            or membership.get("mode")
            not in {"active_object", "suspended_gear", "dormant_object"}
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset conversion membership is malformed",
            )
        _require_id(
            membership["conversion_effect_id"], "Asset conversion Effect", context
        )
        _require_id(
            membership["principal_subject_id"], "Asset conversion principal", context
        )
        if (
            type(membership["binding_generation"]) is not int
            or membership["binding_generation"] < 1
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset conversion generation is malformed",
            )
        conversion_mode = str(membership["mode"])
    if "spell_progress" in state:
        _validate_schema(
            "https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json#/$defs/progressMap",
            state["spell_progress"],
            "Asset spell progress",
            context,
        )
    if "details" in state:
        if not isinstance(state["details"], Mapping):
            _hold(context, "AUTHORITY_UNAVAILABLE", "Asset details are malformed")
        try:
            contracts.validate_nonexecutable_details(state["details"])
        except contracts.ActivityContractError as error:
            raise _hold_error(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset details are not descriptive-only",
            ) from error
    return _AssetData(
        owner_ref,
        state,
        owner_actor_id,
        container_asset_id,
        location_id,
        state.get("access") == "blocked",
        equipment_mode,
        attuned_actor_id,
        conversion_mode,
    )


def _validate_native_references(
    effects: Mapping[str, _EffectData],
    assets: Mapping[str, _AssetData],
    context: contracts.NativePreparationContext,
) -> None:
    for effect in effects.values():
        if (
            effect.support_effect_id is not None
            and effect.support_effect_id not in effects
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native Effect support edge points outside the complete family tree",
            )
    for asset in assets.values():
        state = asset.state
        if (
            asset.container_asset_id is not None
            and asset.container_asset_id not in assets
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native Asset container parent is absent from the complete family tree",
            )
        references: list[str] = []
        transform = state.get("equipment_transform")
        if isinstance(transform, Mapping):
            references.append(str(transform["source_effect_id"]))
        replica = state.get("replica_origin")
        if isinstance(replica, Mapping):
            references.append(str(replica["relation_effect_id"]))
            if replica["source_asset_id"] not in assets:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native Asset replica source is missing",
                )
        conversion = state.get("conversion_membership")
        if isinstance(conversion, Mapping):
            references.append(str(conversion["conversion_effect_id"]))
        if any(reference not in effects for reference in references):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native Asset refers to an absent Effect",
            )
    for asset_id in assets:
        seen_assets: set[str] = set()
        current_asset_id = asset_id
        while True:
            if current_asset_id in seen_assets:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native Asset container graph contains a cycle",
                )
            seen_assets.add(current_asset_id)
            current_asset = assets[current_asset_id]
            parent_id = current_asset.container_asset_id
            if parent_id is None:
                break
            current_asset_id = parent_id
    for effect_id in effects:
        seen: set[str] = set()
        current = effect_id
        while True:
            if current in seen:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native Effect support graph contains a cycle",
                )
            seen.add(current)
            parent = effects[current].support_effect_id
            if parent is None:
                break
            current = parent


def _asset_closure(
    assets: Mapping[str, _AssetData],
    subject_actor_ids: set[str],
    target_asset_ids: set[str],
    context: contracts.NativePreparationContext,
) -> set[str]:
    seeds = set(target_asset_ids)
    seeds.update(
        asset_id
        for asset_id, asset in assets.items()
        if asset.owner_actor_id in subject_actor_ids
    )
    if not seeds.issubset(assets):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            "compiled Asset role is absent from the complete native Asset tree",
        )

    closure: set[str] = set()
    for seed in seeds:
        current = seed
        chain: set[str] = set()
        while True:
            if current in chain:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native Asset container chain contains a cycle",
                )
            chain.add(current)
            asset = assets.get(current)
            if asset is None:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "native Asset container parent is missing",
                )
            closure.add(current)
            if asset.container_asset_id is None:
                break
            current = asset.container_asset_id

    children: dict[str, list[str]] = {}
    for asset_id, asset in assets.items():
        if asset.container_asset_id is not None:
            children.setdefault(asset.container_asset_id, []).append(asset_id)
    pending = list(closure)
    while pending:
        parent = pending.pop()
        for child in children.get(parent, ()):
            if child not in closure:
                closure.add(child)
                pending.append(child)

    # Native Asset relation fields carry references, not duplicated Effects.
    for asset_id in tuple(closure):
        asset = assets[asset_id]
        replica = asset.state.get("replica_origin")
        if isinstance(replica, Mapping):
            source_id = str(replica["source_asset_id"])
            current = source_id
            while current not in closure:
                source = assets.get(current)
                if source is None:
                    _hold(
                        context,
                        "AUTHORITY_UNAVAILABLE",
                        "Asset replica source closure is missing",
                    )
                closure.add(current)
                if source.container_asset_id is None:
                    break
                current = source.container_asset_id
    return closure


def _hold_unqualified_asset_profiles(
    *,
    subject_actor_ids: set[str],
    target_ids: set[str],
    asset_closure: set[str],
    assets: Mapping[str, _AssetData],
    effects: Mapping[str, _EffectData],
    p0_observation: CurrentOwnerObservation,
    context: contracts.NativePreparationContext,
) -> None:
    for actor_id in subject_actor_ids:
        actor_ref = NativeOwnerRef("world.actor", (actor_id,))
        payload = p0_observation.require(actor_ref).payload
        if payload is None or not isinstance(payload.get("state"), Mapping):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "compiled Actor subject has no current native profile state",
            )
        if payload["state"].get("embodiment") is not None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "nonordinary Actor embodiment lacks a compiled subject/profile binding in this slice",
            )

    for asset_id, asset in assets.items():
        state = asset.state
        conversion = state.get("conversion_membership")
        if isinstance(conversion, Mapping) and (
            asset_id in asset_closure
            or conversion.get("principal_subject_id") in subject_actor_ids
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "Asset conversion membership lacks this consumer's exact profile/principal/generation join",
            )
        if asset_id in asset_closure and "equipment_transform" in state:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "transformed Asset availability lacks its exact current source-profile qualification",
            )
        replica = state.get("replica_origin")
        if isinstance(replica, Mapping):
            relation = effects.get(str(replica["relation_effect_id"]))
            replica_is_relevant = (
                asset_id in asset_closure
                or replica.get("source_asset_id") in asset_closure
                or relation is not None
                and (
                    relation.target_id in target_ids
                    or relation.source_id in subject_actor_ids
                    or _binding_mentions(relation.subject_binding, subject_actor_ids)
                )
            )
            if replica_is_relevant:
                _hold(
                    context,
                    "AUTHORITY_UNAVAILABLE",
                    "replica Asset relation lacks its exact current source-profile qualification",
                )

    for effect in effects.values():
        conversion_state = effect.conversion_state
        if not isinstance(conversion_state, Mapping):
            continue
        if (
            effect.target_id in target_ids
            or conversion_state.get("principal_subject_id") in subject_actor_ids
        ):
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "conversion Effect lacks an admitted consumer/profile binding in this slice",
            )


def _asset_member(
    asset: _AssetData,
    read: object,
    assets: Mapping[str, _AssetData],
    actor_ids: set[str],
    context: contracts.NativePreparationContext,
) -> MembershipAsset:
    asset_id = asset.owner_ref.identity[0]
    path: list[str] = []
    current = asset_id
    blocker: str | None = None
    visited: set[str] = set()
    while True:
        if current in visited:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native Asset containment closure contains a cycle",
            )
        visited.add(current)
        parent = assets.get(current)
        if parent is None:
            _hold(
                context,
                "AUTHORITY_UNAVAILABLE",
                "native Asset containment ancestor is missing",
            )
        path.append(current)
        if parent.access_blocked and blocker is None:
            blocker = current
        if parent.container_asset_id is None:
            root_owner = parent.owner_actor_id
            break
        current = parent.container_asset_id
    if asset.location_id is not None or root_owner not in actor_ids:
        accessible = False
    else:
        accessible = blocker is None and asset.conversion_mode not in {
            "suspended_gear",
            "dormant_object",
        }
    return MembershipAsset(
        owner_ref=asset.owner_ref,
        placement_owner_id=asset.owner_actor_id or root_owner,
        container_path=tuple(reversed(path)),
        equipment_mode=asset.equipment_mode,
        accessible=accessible,
        blocker_asset_id=blocker,
        attuned_actor_id=asset.attuned_actor_id,
        conversion_mode=asset.conversion_mode,
        source_basis=read.source_basis or "",
        fingerprint=read.fingerprint or "",
    )


def _asset_effect_reference_present(
    state: Mapping[str, object], effects: Mapping[str, _EffectData]
) -> bool:
    for name in ("equipment_transform", "replica_origin", "conversion_membership"):
        value = state.get(name)
        if not isinstance(value, Mapping):
            continue
        field_name = {
            "equipment_transform": "source_effect_id",
            "replica_origin": "relation_effect_id",
            "conversion_membership": "conversion_effect_id",
        }[name]
        effect = effects.get(str(value[field_name]))
        if effect is None or effect.lifecycle != "effect_lifecycle.active":
            return False
    return True


def _effect_member(
    effect: _EffectData, read: object, is_target_local: bool
) -> MembershipEffect:
    return MembershipEffect(
        owner_ref=effect.owner_ref,
        target_id=effect.target_id,
        lifecycle=effect.lifecycle,
        source_id=effect.source_id,
        rules_origin_id=effect.rules_origin_id,
        support_effect_id=effect.support_effect_id,
        source_basis=read.source_basis or "",
        fingerprint=read.fingerprint or "",
        is_target_local=is_target_local,
    )


def _effect_exclusion(
    effect: _EffectData,
    read: object,
    reason: str,
) -> MembershipExclusion:
    return MembershipExclusion(
        effect.owner_ref,
        effect.target_id,
        reason,
        read.source_basis or "",
        read.fingerprint or "",
    )


def _issue_membership(
    *,
    campaign_id: str,
    source_revision: str,
    source_tree_sha: str,
    activity_id: str,
    consumer_id: str,
    subject_actor_ids: tuple[str, ...],
    effects: tuple[MembershipEffect, ...],
    effect_dependencies: tuple[MembershipEffect, ...],
    exclusions: tuple[MembershipExclusion, ...],
    assets: tuple[MembershipAsset, ...],
    family_coverage: tuple[_FamilyCoverage, ...],
    p0_observation: CurrentOwnerObservation,
    context: contracts.NativePreparationContext,
    owner_session: CurrentOwnerReadSession,
    operation_token: object,
) -> MembershipObservation:
    value = object.__new__(MembershipObservation)
    for name, item in {
        "campaign_id": campaign_id,
        "source_revision": source_revision,
        "source_tree_sha": source_tree_sha,
        "activity_id": activity_id,
        "consumer_id": consumer_id,
        "subject_actor_ids": subject_actor_ids,
        "effects": effects,
        "effect_dependencies": effect_dependencies,
        "exclusions": exclusions,
        "assets": assets,
        "family_coverage": family_coverage,
        "p0_observation": p0_observation,
        "_context": context,
        "_owner_session": owner_session,
        "_operation_token": operation_token,
        "_issue_seal": _ISSUANCE_LOCK,
    }.items():
        object.__setattr__(value, name, item)
    identity = id(value)

    def forget(reference: weakref.ReferenceType[MembershipObservation]) -> None:
        with _ISSUANCE_LOCK:
            current = _ISSUED_MEMBERSHIPS.get(identity)
            if current is not None and current[0] is reference:
                del _ISSUED_MEMBERSHIPS[identity]

    reference = weakref.ref(value, forget)
    snapshot = _membership_snapshot(value)
    with _ISSUANCE_LOCK:
        _ISSUED_MEMBERSHIPS[identity] = (reference, snapshot)
    return value


def _membership_snapshot(value: MembershipObservation) -> object:
    return tuple(
        (member.name, _snapshot_value(getattr(value, member.name)))
        for member in fields(value)
    )


def _snapshot_value(value: object, active: set[int] | None = None) -> object:
    if isinstance(value, (str, int, float, bool, type(None), bytes)):
        return ("scalar", type(value), value)
    if active is None:
        active = set()
    identity = id(value)
    if identity in active:
        raise MechanicalSourceError("membership evidence contains a reference cycle")
    active.add(identity)
    try:
        if isinstance(value, Mapping):
            return (
                "mapping",
                type(value),
                identity,
                tuple(
                    (_snapshot_value(key, active), _snapshot_value(item, active))
                    for key, item in value.items()
                ),
            )
        if isinstance(value, (tuple, list)):
            return (
                "sequence",
                type(value),
                identity,
                tuple(_snapshot_value(item, active) for item in value),
            )
        if hasattr(type(value), "__dataclass_fields__"):
            return (
                "dataclass",
                type(value),
                identity,
                tuple(
                    (member.name, _snapshot_value(getattr(value, member.name), active))
                    for member in fields(value)
                ),
            )
        return ("identity", type(value), identity)
    finally:
        active.remove(identity)


def _strict_fields(
    value: Mapping[str, object],
    allowed: set[str],
    required: set[str],
    label: str,
    context: contracts.NativePreparationContext,
) -> None:
    if set(value) - allowed or required - set(value):
        _hold(
            context,
            "AUTHORITY_UNAVAILABLE",
            f"{label} has unsupported or missing fields",
        )


def _validate_schema(
    schema_ref: str,
    value: object,
    label: str,
    context: contracts.NativePreparationContext,
) -> None:
    try:
        contracts._wire_contract(schema_ref, value)
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise _hold_error(
            context,
            "AUTHORITY_UNAVAILABLE",
            f"{label} does not match its installed native schema",
        ) from error


def _optional_id(
    mapping: Mapping[str, object],
    key: str,
    context: contracts.NativePreparationContext,
) -> str | None:
    if key not in mapping:
        return None
    return _require_id(mapping[key], key, context)


def _require_id(
    value: object, label: str, context: contracts.NativePreparationContext
) -> str:
    if not isinstance(value, str) or _NATIVE_ID.fullmatch(value) is None:
        _hold(context, "AUTHORITY_UNAVAILABLE", f"{label} is not a native identifier")
    return value


def _is_id(value: object) -> bool:
    return isinstance(value, str) and _NATIVE_ID.fullmatch(value) is not None


def _is_scalar(value: object) -> bool:
    return (
        type(value) in (str, int, bool) or type(value) is float and math.isfinite(value)
    )


def _owner_key(owner_ref: NativeOwnerRef) -> tuple[str, tuple[str, ...]]:
    return owner_ref.family_key, owner_ref.identity


def _hold(
    context: contracts.NativePreparationContext,
    status: str,
    message: str,
) -> None:
    raise contracts.NativePreparationHold(
        status, context.execution_ref, ()
    ) from MechanicalSourceError(message)


def _hold_error(
    context: contracts.NativePreparationContext,
    status: str,
    message: str,
) -> contracts.NativePreparationHold:
    return contracts.NativePreparationHold(status, context.execution_ref, ())
