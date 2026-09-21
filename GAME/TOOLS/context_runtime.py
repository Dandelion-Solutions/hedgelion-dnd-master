"""Bounded, ephemeral Context Runtime discovery and assembly primitives.

Discovery inputs are routing hints only.  A candidate becomes usable Context
material only after this module re-runs the fixed native LIVE, information and
PLAYER owner checks for the registered role/purpose scope.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
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
    )
    from GAME.TOOLS.live_state import (  # type: ignore[no-redef]
        LiveContractError,
        LiveEnvelope,
        LiveRouting,
        require_selected_live_source,
    )


class ContextContractError(ValueError):
    """A context candidate or scoped join violates the registered request."""


@dataclass(frozen=True, slots=True)
class ContextOwnerInput:
    """Untrusted transport for native owner inputs needed by one candidate.

    Constructing this carrier does not establish currentness or eligibility.
    Admission always re-runs the fixed native owner validators below, and
    owner-issued PLAYER resolution is checked against its private issuer mark.
    """

    candidate_id: str
    live_route: object
    live_source: object
    live_projection: object
    information_candidate: object
    player_resolution: object

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id:
            raise ContextContractError("owner input candidate identity is required")


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


def _request_scope(request: Mapping[str, object]) -> tuple[_RegisteredProfile, str, str, str]:
    if type(request) is not dict:
        raise ContextContractError("Context admission request must be a native mapping")
    profile = _registered_profile(request.get("profile_id"))
    role_id = request.get("role_id")
    purpose = request.get("purpose")
    recipient_id = request.get("recipient_id")
    if any(not isinstance(value, str) or not value for value in (role_id, purpose, recipient_id)):
        raise ContextContractError("owner-routed Context admission requires role, purpose and recipient")
    if role_id != profile.role_id or purpose not in profile.purposes:
        raise ContextContractError("request role/purpose is not admitted by the registered ContextNeedProfile")
    if "need_profile" in request or "profile" in request:
        raise ContextContractError("caller cannot supply or replace a registered ContextNeedProfile")
    _validate_request_limits(dict(request), profile)
    return profile, role_id, purpose, recipient_id


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
    profile, _role_id, _purpose, _recipient_id = _request_scope(request)
    required = ("allowed_channels", "max_candidates", "allowed_relations", "budget")
    if any(field not in request for field in required):
        raise ContextContractError("registered ContextNeedProfile limits are required")
    return profile


def _owner_input_for_candidate(owner_input: object, candidate_id: str) -> ContextOwnerInput:
    if type(owner_input) is not ContextOwnerInput:
        raise ContextContractError("candidate requires the nominal Context owner input")
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
    _profile, role_id, purpose, recipient_id = _request_scope(request)
    for field, expected in (("role_id", role_id), ("purpose", purpose), ("recipient_id", recipient_id)):
        if field in candidate and candidate[field] != expected:
            raise ContextContractError(f"candidate {field} is outside the registered request scope")

    try:
        current_source = require_selected_live_source(owner.live_route, owner.live_source)
    except (LiveContractError, TypeError, ValueError) as error:
        raise ContextContractError(f"candidate LIVE source is stale or incomplete: {error}") from error

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
    owner_input: ContextOwnerInput | None = None,
    request: Mapping[str, object] | None = None,
) -> dict[str, Any]:
    """Admit a candidate only after complete native owner/source resolution."""

    if request is None:
        raise ContextContractError("candidate requires an owner-routed Context request")
    return _resolve_owner_admitted_candidate(candidate, owner_input, request)


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
) -> dict[str, Any]:
    profile = _validate_registered_request(request)
    discovered = discover_candidates(request, candidates)
    owner_by_id: dict[str, ContextOwnerInput] = {}
    for owner_input in owner_inputs:
        if type(owner_input) is not ContextOwnerInput:
            raise ContextContractError("Context owner inputs must be nominal typed carriers")
        if owner_input.candidate_id in owner_by_id:
            raise ContextContractError("Context owner inputs must have unique candidate identities")
        owner_by_id[owner_input.candidate_id] = owner_input

    available: dict[str, dict[str, Any]] = {}
    for item in discovered:
        candidate_id = item["candidate_id"]
        try:
            available[candidate_id] = resolve_candidate_basis(
                item,
                owner_input=owner_by_id.get(candidate_id),
                request=request,
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
    _profile, role_id, purpose, recipient_id = _request_scope(request)
    bundle = {
        "profile_id": profile.profile_id,
        "role_id": role_id,
        "purpose": purpose,
        "source_frontier": request.get("source_frontier", ""),
        "recipient_id": recipient_id,
        "required": allocation["required"],
        "optional": allocation["optional"],
        "retrospective_projection": request.get("retrospective", False) is True,
    }
    return {"outcome": allocation["outcome"], "bundle": bundle, "trace": trace}


def scoped_context_join(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    keys = ("profile_id", "source_frontier", "recipient_id")
    if any(left.get(key) != right.get(key) for key in keys):
        raise ContextContractError("context join requires one scoped profile/frontier/recipient basis")
    return {key: left.get(key) for key in keys}
