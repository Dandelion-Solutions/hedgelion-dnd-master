"""Bounded, ephemeral Context Runtime discovery and assembly primitives.

Discovery inputs are routing hints only.  A candidate becomes usable Context
material only after this module re-runs the fixed native LIVE, information and
PLAYER owner checks for the registered role/purpose scope.
"""

from __future__ import annotations

import json
import weakref
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

try:
    from .access_control import (
        PlayerRecord,
        PlayerResolution,
        _is_owner_issued_resolution,
    )
    from .context_budget import allocate
    from .information import (
        InformationContractError,
        LiveInformationCandidate,
        apply_normalization_candidates_under_native_owners,
        extract_material_live_information,
    )
    from .live_state import LiveContractError, LiveEnvelope, LiveRouting, require_selected_live_source
except ImportError:  # pragma: no cover - direct-path focused test imports.
    from GAME.TOOLS.access_control import (  # type: ignore[no-redef]
        PlayerRecord,
        PlayerResolution,
        _is_owner_issued_resolution,
    )
    from GAME.TOOLS.context_budget import allocate  # type: ignore[no-redef]
    from GAME.TOOLS.information import (  # type: ignore[no-redef]
        InformationContractError,
        LiveInformationCandidate,
        apply_normalization_candidates_under_native_owners,
        extract_material_live_information,
    )
    from GAME.TOOLS.live_state import (  # type: ignore[no-redef]
        LiveContractError,
        LiveEnvelope,
        LiveRouting,
        require_selected_live_source,
    )


class ContextContractError(ValueError):
    """A context candidate or scoped join violates the registered request."""


ExactLoadTransport = Callable[[str, tuple[str, ...]], object]

_LIVE_ROUTE_LOAD = "context.live_route"
_LIVE_SOURCE_LOAD = "context.live_source"
_LIVE_PROJECTION_LOAD = "context.live_projection"
_PLAYER_RESOLUTION_LOAD = "context.player_resolution"
_CONTEXT_OWNER_INPUT_TOKEN = object()


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class ContextOwnerInput:
    """Opaque internal post-resolution carrier for one admitted candidate.

    The public constructor is deliberately disabled.  Context creates this
    carrier only after exact-load transport has supplied route/source records,
    Context has rebuilt the native LIVE types, and the PLAYER owner has supplied
    its owner-issued resolution.  It is never an authority-bearing input.
    """

    candidate_id: str
    live_route: object
    live_source: object
    live_projection: object
    information_candidate: object
    player_resolution: object
    _issuer: object = field(default=None, repr=False, compare=False)

    def __init__(self, **_values: object) -> None:
        raise ContextContractError(
            "Context owner inputs are internal; use fixed exact native-load transport"
        )


_OWNER_ISSUED_CONTEXT_INPUTS: dict[
    int, weakref.ReferenceType[ContextOwnerInput]
] = {}


def _issue_context_owner_input(**values: object) -> ContextOwnerInput:
    owner_input = object.__new__(ContextOwnerInput)
    for field_name, value in values.items():
        object.__setattr__(owner_input, field_name, value)
    object.__setattr__(owner_input, "_issuer", _CONTEXT_OWNER_INPUT_TOKEN)
    owner_input_id = id(owner_input)

    def remove(reference: weakref.ReferenceType[ContextOwnerInput]) -> None:
        if _OWNER_ISSUED_CONTEXT_INPUTS.get(owner_input_id) is reference:
            _OWNER_ISSUED_CONTEXT_INPUTS.pop(owner_input_id, None)

    _OWNER_ISSUED_CONTEXT_INPUTS[owner_input_id] = weakref.ref(owner_input, remove)
    return owner_input


def _is_owner_issued_context_input(value: object) -> bool:
    reference = _OWNER_ISSUED_CONTEXT_INPUTS.get(id(value))
    return (
        type(value) is ContextOwnerInput
        and value._issuer is _CONTEXT_OWNER_INPUT_TOKEN
        and reference is not None
        and reference() is value
    )


@dataclass(frozen=True, slots=True)
class _RegisteredProfile:
    profile_id: str
    role_id: str
    purposes: tuple[str, ...]
    channels: tuple[str, ...]
    relations: tuple[str, ...]
    max_candidates: int
    max_budget: int


_DISCOVERY_CHANNELS = (
    "CURRENT_SCOPE",
    "SCENE_MANIFEST",
    "EXPLICIT_REF",
    "ACTIVE_DEPENDENCY",
    "LIVE_CURRENT",
    "INDEX_LOOKUP",
    "HISTORY_HINT",
)


def _registered_profile(profile_id: object) -> _RegisteredProfile:
    """Return one fixed Context consumer contract; callers cannot register one."""

    if profile_id == "profile.narration":
        return _RegisteredProfile(
            profile_id="profile.narration",
            role_id="role.narrator",
            purposes=("narration", "context-test"),
            channels=_DISCOVERY_CHANNELS,
            relations=("requires",),
            max_candidates=256,
            max_budget=1_000_000,
        )
    if profile_id == "profile.commentator":
        return _RegisteredProfile(
            profile_id="profile.commentator",
            role_id="role.commentator",
            purposes=("commentary", "context-test"),
            channels=_DISCOVERY_CHANNELS,
            relations=("requires",),
            max_candidates=256,
            max_budget=1_000_000,
        )
    if profile_id == "profile.actor":
        return _RegisteredProfile(
            profile_id="profile.actor",
            role_id="role.actor",
            purposes=("actor", "context-test"),
            channels=_DISCOVERY_CHANNELS,
            relations=("requires",),
            max_candidates=256,
            max_budget=1_000_000,
        )
    raise ContextContractError("ContextNeedProfile is not registered")


def _request_scope(
    request: Mapping[str, object],
) -> tuple[_RegisteredProfile, str, str, str, str]:
    if type(request) is not dict:
        raise ContextContractError("Context admission request must be a native mapping")
    profile = _registered_profile(request.get("profile_id"))
    role_id = request.get("role_id")
    purpose = request.get("purpose")
    subject_id = request.get("subject_id")
    recipient_id = request.get("recipient_id")
    if any(
        not isinstance(value, str) or not value
        for value in (role_id, purpose, subject_id, recipient_id)
    ):
        raise ContextContractError(
            "owner-routed Context admission requires role, purpose, subject and recipient"
        )
    if role_id != profile.role_id or purpose not in profile.purposes:
        raise ContextContractError("request role/purpose is not admitted by the registered ContextNeedProfile")
    if "need_profile" in request or "profile" in request:
        raise ContextContractError("caller cannot supply or replace a registered ContextNeedProfile")
    _validate_request_limits(dict(request), profile)
    return profile, role_id, purpose, subject_id, recipient_id


def _registered_string_list(
    value: object,
    *,
    label: str,
    allowed: tuple[str, ...],
    require_nonempty: bool,
) -> list[str]:
    if not isinstance(value, list) or (require_nonempty and not value):
        raise ContextContractError(f"{label} must be a bounded registered string list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ContextContractError(f"{label} must contain only nonempty strings")
    if len(value) != len(set(value)) or any(item not in allowed for item in value):
        raise ContextContractError(f"{label} exceeds the registered profile")
    return value


def _validate_request_limits(request: dict[str, Any], profile: _RegisteredProfile) -> None:
    if "allowed_channels" in request:
        _registered_string_list(
            request["allowed_channels"],
            label="request channels",
            allowed=profile.channels,
            require_nonempty=True,
        )
    if "max_candidates" in request:
        limit = request["max_candidates"]
        if isinstance(limit, bool) or not isinstance(limit, int) or not 0 <= limit <= profile.max_candidates:
            raise ContextContractError("request candidate bound exceeds the registered profile")
    if "allowed_relations" in request:
        _registered_string_list(
            request["allowed_relations"],
            label="request relations",
            allowed=profile.relations,
            require_nonempty=False,
        )
    if "budget" in request:
        budget = request["budget"]
        if isinstance(budget, bool) or not isinstance(budget, int) or not 0 <= budget <= profile.max_budget:
            raise ContextContractError("request budget exceeds the registered profile")


def _validate_registered_request(request: dict[str, Any]) -> _RegisteredProfile:
    profile, _role_id, _purpose, _subject_id, _recipient_id = _request_scope(request)
    required = ("allowed_channels", "max_candidates", "allowed_relations", "budget")
    if any(field not in request for field in required):
        raise ContextContractError("registered ContextNeedProfile limits are required")
    return profile


def _call_exact_load(
    exact_load: ExactLoadTransport | object,
    family: str,
    identity: tuple[str, ...],
) -> object:
    loader = getattr(exact_load, "load_exact", None)
    if loader is None:
        loader = exact_load
    if not callable(loader):
        raise ContextContractError("fixed exact native-load transport is required")
    try:
        value = loader(family, identity)
    except (KeyError, OSError, TypeError, ValueError) as error:
        raise ContextContractError(
            f"exact native load failed for {family}",
        ) from error
    if value is None:
        raise ContextContractError(f"exact native load is missing for {family}:{identity[0]}")
    if isinstance(value, (bytes, bytearray)):
        try:
            value = json.loads(bytes(value).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContextContractError(
                f"exact native load for {family} is not a JSON record",
            ) from error
    return value


def _load_owner_input(
    candidate_id: str,
    request: Mapping[str, object],
    exact_load: ExactLoadTransport | object | None,
) -> ContextOwnerInput:
    if exact_load is None:
        raise ContextContractError(
            "candidate requires owner-routed fixed exact native-load transport"
        )
    _profile, _role_id, _purpose, _subject_id, recipient_id = _request_scope(request)
    raw_route = _call_exact_load(exact_load, _LIVE_ROUTE_LOAD, (candidate_id,))
    raw_source = _call_exact_load(exact_load, _LIVE_SOURCE_LOAD, (candidate_id,))
    raw_projection = _call_exact_load(exact_load, _LIVE_PROJECTION_LOAD, (candidate_id,))
    resolution = _call_exact_load(exact_load, _PLAYER_RESOLUTION_LOAD, (recipient_id,))
    try:
        route = LiveRouting.from_mapping(raw_route)
        source = LiveEnvelope.from_mapping(raw_source)
    except (LiveContractError, TypeError, ValueError) as error:
        raise ContextContractError(f"exact native LIVE load is invalid: {error}") from error
    if not isinstance(raw_projection, Mapping) or callable(raw_projection):
        raise ContextContractError("exact native LIVE projection load is invalid")
    if not isinstance(resolution, PlayerResolution):
        raise ContextContractError("exact native PLAYER resolution load is not owner-issued")
    try:
        extracted = extract_material_live_information(
            route,
            source,
            raw_projection,
            recipient_player_id=recipient_id,
        )
    except (InformationContractError, LiveContractError, TypeError, ValueError) as error:
        raise ContextContractError(f"exact native information load is invalid: {error}") from error
    if len(extracted) != 1:
        raise ContextContractError("exact native information load is ambiguous")
    return _issue_context_owner_input(
        candidate_id=candidate_id,
        live_route=route,
        live_source=source,
        live_projection=deepcopy(dict(raw_projection)),
        information_candidate=extracted[0],
        player_resolution=resolution,
    )


def _owner_input_for_candidate(owner_input: object, candidate_id: str) -> ContextOwnerInput:
    if not _is_owner_issued_context_input(owner_input):
        raise ContextContractError("candidate requires an owner-issued exact-load result")
    if owner_input.candidate_id != candidate_id:
        raise ContextContractError("Context owner input identity differs from candidate")
    if type(owner_input.live_route) is not LiveRouting:
        raise ContextContractError("Context LIVE route must be native owner-typed")
    if type(owner_input.live_source) is not LiveEnvelope:
        raise ContextContractError("Context LIVE source must be native owner-typed")
    if type(owner_input.information_candidate) is not LiveInformationCandidate:
        raise ContextContractError("Context information candidate must be native owner-typed")
    if type(owner_input.player_resolution) is not PlayerResolution:
        raise ContextContractError("Context PLAYER resolution must be native owner-typed")
    if not isinstance(owner_input.live_projection, Mapping) or callable(owner_input.live_projection):
        raise ContextContractError("Context LIVE projection must be an owner source mapping")
    return owner_input


def _resolve_owner_admitted_candidate(
    candidate: dict[str, Any],
    owner_input: object,
    request: Mapping[str, object],
) -> dict[str, Any]:
    """Resolve one discovery hint through fixed native owner routes."""

    if type(candidate) is not dict:
        raise ContextContractError("Context candidate must be a native discovery mapping")
    if "current" in candidate or "eligible" in candidate:
        raise ContextContractError("caller current/eligible flags are not owner evidence")
    candidate_id = candidate.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ContextContractError("candidate identity is required")
    owner = _owner_input_for_candidate(owner_input, candidate_id)
    _profile, role_id, purpose, subject_id, recipient_id = _request_scope(request)
    for field, expected in (("role_id", role_id), ("purpose", purpose), ("recipient_id", recipient_id)):
        if field in candidate and candidate[field] != expected:
            raise ContextContractError(f"candidate {field} is outside the registered request scope")
    if "subject_id" in candidate and candidate["subject_id"] != subject_id:
        raise ContextContractError("candidate subject is outside the registered request scope")

    try:
        current_source = require_selected_live_source(owner.live_route, owner.live_source)
    except (LiveContractError, TypeError, ValueError) as error:
        raise ContextContractError(f"candidate LIVE source is stale or incomplete: {error}") from error
    if not current_source.claims_contain("world.actor", subject_id):
        raise ContextContractError("candidate LIVE source is not current for the requested subject")

    resolution = owner.player_resolution
    if not _is_owner_issued_resolution(resolution):
        raise ContextContractError("candidate PLAYER resolution is not owner-issued")
    if resolution.status != "AUTHORIZED_PLAYER" or resolution.player is None:
        raise ContextContractError("candidate PLAYER resolution is not active")
    if type(resolution.player) is not PlayerRecord:
        raise ContextContractError("candidate PLAYER record is not native owner state")
    if resolution.campaign_id != current_source.campaign_id:
        raise ContextContractError("candidate PLAYER resolution is bound to another campaign")
    if resolution.player.player_id != recipient_id:
        raise ContextContractError("candidate recipient is not the current PLAYER")

    information_candidate = owner.information_candidate
    if information_candidate.recipient_player_id != recipient_id:
        raise ContextContractError("candidate information is outside the current recipient scope")
    try:
        normalized_values = apply_normalization_candidates_under_native_owners(
            (information_candidate,),
            owner.live_route,
            current_source,
            owner.live_projection,
            recipient_player_id=recipient_id,
        )
    except (InformationContractError, LiveContractError, TypeError, ValueError) as error:
        raise ContextContractError(
            f"candidate information is stale or not eligible for the current {role_id}/{purpose} scope: {error}"
        ) from error
    if len(normalized_values) != 1:
        raise ContextContractError("candidate information owner returned an ambiguous result")
    normalized = normalized_values[0]
    if normalized["knowledge"]["knower_id"] != subject_id:
        raise ContextContractError("candidate native information is outside the requested subject scope")
    native_ids = {
        normalized["lore_fact"]["fact_id"],
        normalized["message"]["message_id"],
    }
    if candidate_id not in native_ids:
        raise ContextContractError("candidate identity is not bound to native information")

    admitted = deepcopy(candidate)
    admitted["current"] = True
    admitted["eligible"] = True
    admitted["payload"] = deepcopy(normalized)
    return admitted


def discover_candidates(request: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    channels = request.get("allowed_channels")
    limit = request.get("max_candidates")
    if not isinstance(channels, list) or not channels or isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ContextContractError("request must name bounded registered discovery channels")
    identities: set[str] = set()
    for item in candidates:
        candidate_id = item.get("candidate_id") if isinstance(item, dict) else None
        if not isinstance(candidate_id, str) or not candidate_id or candidate_id in identities:
            raise ContextContractError("candidate identities must be unique nonempty strings")
        identities.add(candidate_id)
    found = [item for item in candidates if isinstance(item, dict) and item.get("channel") in channels]
    return sorted(found, key=lambda item: item.get("candidate_id", ""))[:limit]


def resolve_candidate_basis(
    candidate: dict[str, Any],
    *,
    owner_input: object | None = None,
    request: Mapping[str, object] | None = None,
    exact_load: ExactLoadTransport | object | None = None,
) -> dict[str, Any]:
    """Admit a candidate only after complete native owner/source resolution."""

    if request is None:
        raise ContextContractError("candidate requires an owner-routed Context request")
    if owner_input is not None:
        raise ContextContractError(
            "caller-constructed Context owner carriers are not admitted; use exact native load"
        )
    candidate_id = candidate.get("candidate_id") if isinstance(candidate, dict) else None
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ContextContractError("candidate identity is required")
    loaded_owner_input = _load_owner_input(candidate_id, request, exact_load)
    return _resolve_owner_admitted_candidate(candidate, loaded_owner_input, request)


def _required_closure(
    required_ids: list[str],
    available: dict[str, dict[str, Any]],
    allowed_relations: set[str],
) -> list[dict[str, Any]] | None:
    pending = list(required_ids)
    resolved: dict[str, dict[str, Any]] = {}
    while pending:
        candidate_id = pending.pop()
        if candidate_id in resolved:
            continue
        candidate = available.get(candidate_id)
        if candidate is None:
            return None
        if candidate.get("current") is not True or candidate.get("eligible") is not True:
            return None
        resolved[candidate_id] = candidate
        dependencies = candidate.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise ContextContractError("dependencies must be a typed list")
        dependency_keys: set[tuple[str, str]] = set()
        for dependency in dependencies:
            if not isinstance(dependency, dict) or set(dependency) != {"relation", "candidate_id"}:
                raise ContextContractError("dependency must be a typed relation")
            relation, target = dependency["relation"], dependency["candidate_id"]
            if not isinstance(relation, str) or relation not in allowed_relations or not isinstance(target, str) or not target:
                raise ContextContractError("dependency relation is not registered by the profile")
            key = (relation, target)
            if key in dependency_keys:
                raise ContextContractError("duplicate dependency relation")
            dependency_keys.add(key)
            pending.append(target)
    return [resolved[key] for key in sorted(resolved)]


def assemble_context(
    request: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    owner_inputs: Sequence[ContextOwnerInput] = (),
    exact_load: ExactLoadTransport | object | None = None,
) -> dict[str, Any]:
    profile = _validate_registered_request(request)
    discovered = discover_candidates(request, candidates)
    if owner_inputs:
        raise ContextContractError(
            "caller-provided Context owner carriers are not admitted; use exact native load"
        )

    available: dict[str, dict[str, Any]] = {}
    for item in discovered:
        candidate_id = item["candidate_id"]
        try:
            available[candidate_id] = resolve_candidate_basis(
                item,
                request=request,
                exact_load=exact_load,
            )
        except ContextContractError:
            continue

    required_ids = request.get("required_ids", [])
    relations = request.get("allowed_relations")
    if not isinstance(required_ids, list) or len(required_ids) != len(set(required_ids)) or any(not isinstance(item, str) for item in required_ids):
        raise ContextContractError("required_ids must be strings")
    if not isinstance(relations, list) or len(relations) != len(set(relations)) or any(not isinstance(item, str) or not item for item in relations):
        raise ContextContractError("allowed_relations must be registered unique strings")
    discovered_ids = sorted(item["candidate_id"] for item in discovered)
    trace = {
        "profile_id": profile.profile_id,
        "discovered_ids": discovered_ids,
        "included_ids": [],
        "excluded_ids": sorted(set(discovered_ids) - set(available)),
    }
    required = _required_closure(required_ids, available, set(relations))
    if required is None:
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    required_set = {item["candidate_id"] for item in required}
    optional = [available[item["candidate_id"]] for item in discovered if item["candidate_id"] not in required_set and item["candidate_id"] in available]
    allocation = allocate(required, optional, request["budget"])
    if allocation["outcome"] == "UNSATISFIABLE":
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    trace["included_ids"] = [item["candidate_id"] for item in allocation["required"] + allocation["optional"]]
    _profile, role_id, purpose, subject_id, recipient_id = _request_scope(request)
    bundle = {
        "profile_id": profile.profile_id,
        "role_id": role_id,
        "purpose": purpose,
        "subject_id": subject_id,
        "source_frontier": request.get("source_frontier", ""),
        "recipient_id": recipient_id,
        "required": allocation["required"],
        "optional": allocation["optional"],
        "retrospective_projection": request.get("retrospective", False) is True,
    }
    return {"outcome": allocation["outcome"], "bundle": bundle, "trace": trace}


def scoped_context_join(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    keys = ("profile_id", "role_id", "purpose", "subject_id", "source_frontier", "recipient_id")
    if any(left.get(key) != right.get(key) for key in keys):
        raise ContextContractError("context join requires one scoped profile/frontier/recipient basis")
    return {key: left.get(key) for key in keys}
