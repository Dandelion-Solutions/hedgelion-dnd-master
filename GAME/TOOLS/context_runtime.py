"""Bounded Context admission through the RuntimeHost composition boundary.

Discovery data is untrusted routing input.  A candidate becomes material only
after fixed engine dispatch reloads and validates its native owner through the
operation basis supplied by the trusted RuntimeHost.  Context remains an
ephemeral projection and owns no campaign, LIVE, access or knowledge truth.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final

try:
    from .access_control import AccessControlContractError, PlayerRecord
    from .context_budget import allocate
    from .live_state import (
        LiveContractError,
        LiveRouting,
        require_selected_live_source,
        select_live_source,
    )
    from .native_storage import (
        FAMILY_ROOTS,
        NativeStorageError,
        route_native_record,
        validate_loaded_identity,
    )
    from .policy_basis import PinnedCampaign as _PinnedCampaign
except ImportError:  # pragma: no cover - direct-path focused test imports.
    from GAME.TOOLS.access_control import (  # type: ignore[no-redef]
        AccessControlContractError,
        PlayerRecord,
    )
    from GAME.TOOLS.context_budget import allocate  # type: ignore[no-redef]
    from GAME.TOOLS.live_state import (  # type: ignore[no-redef]
        LiveContractError,
        LiveRouting,
        require_selected_live_source,
        select_live_source,
    )
    from GAME.TOOLS.native_storage import (  # type: ignore[no-redef]
        FAMILY_ROOTS,
        NativeStorageError,
        route_native_record,
        validate_loaded_identity,
    )
    from GAME.TOOLS.policy_basis import (
        PinnedCampaign as _PinnedCampaign,  # type: ignore[no-redef]
    )


# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"


class ContextContractError(ValueError):
    """A Context request, discovery hint or owner result is not admissible."""


@dataclass(frozen=True, slots=True)
class _RegisteredProfile:
    profile_id: str
    role: str
    purpose: str
    channels: tuple[str, ...]
    relations: tuple[str, ...]
    max_candidates: int = 256
    max_budget: int = 1_000_000


_DISCOVERY_CHANNELS: Final[tuple[str, ...]] = (
    "CURRENT_SCOPE",
    "SCENE_MANIFEST",
    "EXPLICIT_REF",
    "ACTIVE_DEPENDENCY",
    "LIVE_CURRENT",
    "INDEX_LOOKUP",
    "HISTORY_HINT",
)

_PROFILE_TABLE: Final[Mapping[str, _RegisteredProfile]] = MappingProxyType(
    {
        "profile.intent": _RegisteredProfile(
            "profile.intent",
            "INTERPRETER",
            "interpret",
            _DISCOVERY_CHANNELS,
            ("requires",),
        ),
        "profile.dramaturgy": _RegisteredProfile(
            "profile.dramaturgy",
            "DRAMATURG",
            "prepare",
            _DISCOVERY_CHANNELS,
            ("requires",),
        ),
        "profile.actor": _RegisteredProfile(
            "profile.actor", "ACTOR", "assess", _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.story": _RegisteredProfile(
            "profile.story",
            "CHRONICLER",
            "chronicle",
            _DISCOVERY_CHANNELS,
            ("requires",),
        ),
        "profile.narration": _RegisteredProfile(
            "profile.narration",
            "NARRATOR",
            "narrate",
            _DISCOVERY_CHANNELS,
            ("requires",),
        ),
    }
)

REGISTERED_PROFILE_IDS: Final[tuple[str, ...]] = tuple(_PROFILE_TABLE)
_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")

_REQUEST_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "profile_id",
        "role",
        "purpose",
        "subject_id",
        "recipient_id",
        "campaign_id",
        "allowed_channels",
        "max_candidates",
        "required_ids",
        "allowed_relations",
        "budget",
        "source_frontier",
        "retrospective",
    }
)
_FORBIDDEN_AUTHORITY_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "current",
        "eligible",
        "exact_load",
        "validator",
        "resolver",
        "semantic_resolver",
        "callback",
        "repository_port",
        "live_transport",
        "runtime_host",
        "context_service",
        "need_profile",
        "profile",
    }
)

_LIVE_FAMILIES: Final[frozenset[str]] = frozenset(
    {"LIVE", "runtime.live", "runtime.live_source", "world.live"}
)
_PLAYER_FAMILIES: Final[frozenset[str]] = frozenset({"PLAYER", "world.player"})
_INFORMATION_FAMILIES: Final[frozenset[str]] = frozenset(
    {"information", "world.information", "world.lore_fact"}
)
_KNOWLEDGE_FAMILIES: Final[frozenset[str]] = frozenset({"knowledge", "world.knowledge"})
_DISCLOSURE_FAMILIES: Final[frozenset[str]] = frozenset(
    {"disclosure", "runtime.disclosure"}
)
_CAMPAIGN_FAMILIES: Final[frozenset[str]] = frozenset(
    family
    for family in FAMILY_ROOTS
    if family
    not in {
        "world.player",
        "world.lore_fact",
        "world.knowledge",
        "runtime.disclosure",
        "runtime.session",
        "runtime.checkpoint",
        "runtime.collaboration_obligation",
        "runtime.maintenance_audit",
        "runtime.catalog_gap_report",
    }
)


@dataclass(frozen=True, slots=True)
class _RequestScope:
    profile: _RegisteredProfile
    role: str
    purpose: str
    subject_id: str
    recipient_id: str
    campaign_id: str


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContextContractError(f"{label} must be a nonempty string")
    return value


def _scope_id(value: object, label: str) -> str:
    result = _nonempty(value, label)
    if _ID_PATTERN.fullmatch(result) is None:
        raise ContextContractError(f"{label} must be a native identifier")
    return result


def _string_list(value: object, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ContextContractError(f"{label} must be a bounded string list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ContextContractError(f"{label} must contain only nonempty strings")
    if len(value) != len(set(value)):
        raise ContextContractError(f"{label} must contain unique values")
    return value


def _profile(value: object) -> _RegisteredProfile:
    try:
        return _PROFILE_TABLE[value]  # type: ignore[index]
    except (KeyError, TypeError) as error:
        raise ContextContractError("ContextNeedProfile is not registered") from error


def _scope(request: Mapping[str, object]) -> _RequestScope:
    if not isinstance(request, Mapping):
        raise ContextContractError("Context admission request must be an object")
    unknown = set(request).difference(_REQUEST_FIELDS)
    if unknown:
        raise ContextContractError(
            "request fields are not registered: " + ", ".join(sorted(unknown))
        )
    forbidden = _FORBIDDEN_AUTHORITY_FIELDS.intersection(request)
    if forbidden:
        raise ContextContractError(
            "caller authority fields are not accepted: " + ", ".join(sorted(forbidden))
        )

    profile = _profile(request.get("profile_id"))
    role = _scope_id(request.get("role"), "role")
    purpose = _scope_id(request.get("purpose"), "purpose")
    subject_id = _scope_id(request.get("subject_id"), "subject_id")
    recipient_id = _scope_id(request.get("recipient_id"), "recipient_id")
    campaign_id = _scope_id(request.get("campaign_id"), "campaign_id")
    if role != profile.role or purpose != profile.purpose:
        raise ContextContractError(
            "request role/purpose is not admitted by the registered profile"
        )

    channels = _string_list(
        request.get("allowed_channels"), "allowed_channels", allow_empty=False
    )
    if any(channel not in profile.channels for channel in channels):
        raise ContextContractError("request channel is not registered by the profile")
    relations = _string_list(request.get("allowed_relations"), "allowed_relations")
    if any(relation not in profile.relations for relation in relations):
        raise ContextContractError("request relation is not registered by the profile")

    limit = request.get("max_candidates")
    if (
        isinstance(limit, bool)
        or not isinstance(limit, int)
        or not 0 <= limit <= profile.max_candidates
    ):
        raise ContextContractError(
            "request candidate bound exceeds the registered profile"
        )
    required_ids = _string_list(request.get("required_ids"), "required_ids")
    for required_id in required_ids:
        _scope_id(required_id, "required_id")
    budget = request.get("budget")
    if (
        isinstance(budget, bool)
        or not isinstance(budget, int)
        or not 0 <= budget <= profile.max_budget
    ):
        raise ContextContractError("request budget exceeds the registered profile")
    if "source_frontier" in request:
        _scope_id(request["source_frontier"], "source_frontier")
    if "retrospective" in request and type(request["retrospective"]) is not bool:
        raise ContextContractError("retrospective must be boolean")
    return _RequestScope(profile, role, purpose, subject_id, recipient_id, campaign_id)


def discover_candidates(
    request: dict[str, Any], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return only bounded discovery hints; no hint field grants authority."""

    channels = request.get("allowed_channels")
    limit = request.get("max_candidates")
    if not isinstance(channels, list) or not channels:
        raise ContextContractError(
            "request must name bounded registered discovery channels"
        )
    if any(channel not in _DISCOVERY_CHANNELS for channel in channels):
        raise ContextContractError("request channel is not registered")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ContextContractError("request must name a nonnegative candidate bound")
    identities: set[str] = set()
    for item in candidates:
        candidate_id = item.get("candidate_id") if isinstance(item, dict) else None
        if (
            not isinstance(candidate_id, str)
            or not candidate_id
            or candidate_id in identities
        ):
            raise ContextContractError(
                "candidate identities must be unique nonempty strings"
            )
        identities.add(candidate_id)
    found = [
        item
        for item in candidates
        if isinstance(item, dict) and item.get("channel") in channels
    ]
    return sorted(found, key=lambda item: item["candidate_id"])[:limit]


def _decode_record(value: object, label: str) -> Mapping[str, object]:
    if isinstance(value, (bytes, bytearray)):
        try:
            value = json.loads(bytes(value).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContextContractError(f"{label} is not a JSON owner record") from error
    if not isinstance(value, Mapping):
        raise ContextContractError(f"{label} must be an owner mapping")
    return value


def _identity(
    value: object, label: str, *, length: int | None = None
) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not value:
        raise ContextContractError(f"{label} must be a native identity tuple")
    result = tuple(_scope_id(item, f"{label} item") for item in value)
    if length is not None and len(result) != length:
        raise ContextContractError(f"{label} has the wrong arity")
    return result


def _read_campaign_record(
    repository: object,
    pinned: _PinnedCampaign,
    family: str,
    identity: tuple[str, ...],
) -> dict[str, object]:
    try:
        route = route_native_record(family, identity)
        raw = repository.read_exact_path(pinned, route.relative_path)  # type: ignore[attr-defined]
        record = dict(_decode_record(raw, f"{family} owner record"))
        validate_loaded_identity(family, identity, record)
    except (
        AttributeError,
        KeyError,
        OSError,
        TypeError,
        ValueError,
        NativeStorageError,
    ) as error:
        raise ContextContractError(
            f"exact {family} owner record is unavailable or invalid"
        ) from error
    record_campaign = record.get("campaign_id")
    if record_campaign is not None and record_campaign != pinned.campaign_id:
        raise ContextContractError("owner record belongs to another campaign")
    return record


def _candidate_family(candidate: Mapping[str, object]) -> str:
    return _nonempty(
        candidate.get("owner_family", candidate.get("family")), "candidate owner_family"
    )


def _candidate_scope(candidate: Mapping[str, object], scope: _RequestScope) -> None:
    for field_name, expected in (
        ("role", scope.role),
        ("purpose", scope.purpose),
        ("subject_id", scope.subject_id),
        ("recipient_id", scope.recipient_id),
    ):
        if field_name in candidate and candidate[field_name] != expected:
            raise ContextContractError(
                f"candidate {field_name} is outside the registered scope"
            )


def _resolve_player(
    repository: object,
    pinned: _PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.player", identity)
    try:
        player = PlayerRecord.from_mapping(record)
    except (AccessControlContractError, AttributeError, TypeError, ValueError) as error:
        raise ContextContractError("native PLAYER record is invalid") from error
    if player.player_id != recipient_id or player.status != "active":
        raise ContextContractError(
            "native PLAYER is not the current eligible recipient"
        )
    return record


def _resolve_information(
    repository: object,
    pinned: _PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.lore_fact", identity)
    for field_name in ("recipient_player_id", "player_id"):
        if field_name in record and record[field_name] != recipient_id:
            raise ContextContractError(
                "native information is outside the requested recipient scope"
            )
    authorized_recipients = record.get("authorized_recipient_ids")
    if authorized_recipients is not None and (
        not isinstance(authorized_recipients, Sequence)
        or isinstance(authorized_recipients, (str, bytes))
        or recipient_id not in authorized_recipients
    ):
        raise ContextContractError(
            "native information recipient eligibility is not admitted"
        )
    return record


def _resolve_knowledge(
    repository: object,
    pinned: _PinnedCampaign,
    identity: tuple[str, ...],
    subject_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.knowledge", identity)
    if record.get("knower_id") != subject_id:
        raise ContextContractError(
            "native knowledge is outside the requested subject scope"
        )
    authorized_knowers = record.get("authorized_knower_ids")
    if authorized_knowers is not None and (
        not isinstance(authorized_knowers, Sequence)
        or isinstance(authorized_knowers, (str, bytes))
        or subject_id not in authorized_knowers
    ):
        raise ContextContractError(
            "native knowledge subject eligibility is not admitted"
        )
    return record


def _resolve_disclosure(
    repository: object,
    pinned: _PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "runtime.disclosure", identity)
    if record.get("player_id") != recipient_id:
        raise ContextContractError(
            "native disclosure is outside the requested recipient scope"
        )
    return record


def _resolve_live(
    route: LiveRouting | None,
    reader: object | None,
    pinned: _PinnedCampaign,
    candidate: Mapping[str, object],
) -> dict[str, object]:
    if route is None or reader is None:
        raise ContextContractError("selected LIVE read capability is unavailable")
    if route.campaign_id != pinned.campaign_id:
        raise ContextContractError("selected LIVE route belongs to another campaign")
    source_key = candidate.get("source_key", candidate.get("owner_identity"))
    if not isinstance(source_key, (list, tuple)) or len(source_key) != 3:
        raise ContextContractError("LIVE candidate requires one exact source key")
    try:
        selected = select_live_source(route, tuple(source_key))
        if selected is None:
            raise ContextContractError(
                "LIVE source is not selected by the current route"
            )
        source = require_selected_live_source(route, selected)
        raw = _decode_record(
            reader.read_selected_live_source(route, source),  # type: ignore[attr-defined]
            "LIVE source read",
        )
    except ContextContractError:
        raise
    except (
        LiveContractError,
        AttributeError,
        KeyError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise ContextContractError(
            "selected LIVE source is stale or invalid"
        ) from error
    if (
        raw.get("source_key") != list(source.source_key)
        or raw.get("source_ref") != source.source_ref
        or raw.get("source_revision") != source.source_revision
    ):
        raise ContextContractError(
            "LIVE source read does not match the selected source"
        )
    return dict(raw)


def _resolve_candidate(
    repository: object,
    pinned: _PinnedCampaign,
    selected_live: LiveRouting | None,
    selected_live_reader: object | None,
    scope: _RequestScope,
    candidate: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(candidate, dict):
        raise ContextContractError(
            "Context candidate must be a native discovery mapping"
        )
    forbidden = _FORBIDDEN_AUTHORITY_FIELDS.intersection(candidate)
    if forbidden:
        raise ContextContractError(
            "candidate authority fields are not accepted: "
            + ", ".join(sorted(forbidden))
        )
    candidate_id = _scope_id(candidate.get("candidate_id"), "candidate identity")
    _candidate_scope(candidate, scope)
    family = _candidate_family(candidate)
    raw_identity = candidate.get("owner_identity")
    if family in _LIVE_FAMILIES:
        payload = _resolve_live(selected_live, selected_live_reader, pinned, candidate)
        owner_identity = list(candidate.get("source_key", raw_identity))
    elif family in _PLAYER_FAMILIES:
        owner_identity = list(
            _identity(raw_identity, "PLAYER owner_identity", length=1)
        )
        payload = _resolve_player(
            repository, pinned, tuple(owner_identity), scope.recipient_id
        )
    elif family in _INFORMATION_FAMILIES:
        owner_identity = list(
            _identity(raw_identity, "information owner_identity", length=1)
        )
        payload = _resolve_information(
            repository, pinned, tuple(owner_identity), scope.recipient_id
        )
    elif family in _KNOWLEDGE_FAMILIES:
        owner_identity = list(
            _identity(raw_identity, "knowledge owner_identity", length=2)
        )
        payload = _resolve_knowledge(
            repository, pinned, tuple(owner_identity), scope.subject_id
        )
    elif family in _DISCLOSURE_FAMILIES:
        owner_identity = list(
            _identity(raw_identity, "disclosure owner_identity", length=2)
        )
        payload = _resolve_disclosure(
            repository, pinned, tuple(owner_identity), scope.recipient_id
        )
    elif family in _CAMPAIGN_FAMILIES:
        owner_identity = list(_identity(raw_identity, "campaign owner_identity"))
        payload = _read_campaign_record(
            repository, pinned, family, tuple(owner_identity)
        )
    else:
        raise ContextContractError("candidate family is not a registered native owner")

    # current/eligible are deliberately internal post-resolution markers only.
    return {
        "candidate_id": candidate_id,
        "channel": candidate.get("channel"),
        "rank": candidate.get("rank", 0),
        "dependencies": deepcopy(candidate.get("dependencies", [])),
        "owner_family": family,
        "owner_identity": owner_identity,
        "payload": deepcopy(payload),
        "current": True,
        "eligible": True,
    }


def _required_closure(
    required_ids: list[str],
    available: dict[str, dict[str, object]],
    allowed_relations: set[str],
) -> list[dict[str, object]] | None:
    pending = list(required_ids)
    resolved: dict[str, dict[str, object]] = {}
    while pending:
        candidate_id = pending.pop()
        if candidate_id in resolved:
            continue
        candidate = available.get(candidate_id)
        if candidate is None:
            return None
        resolved[candidate_id] = candidate
        dependencies = candidate.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise ContextContractError("dependencies must be a typed list")
        dependency_keys: set[tuple[str, str]] = set()
        for dependency in dependencies:
            if not isinstance(dependency, Mapping) or set(dependency) != {
                "relation",
                "candidate_id",
            }:
                raise ContextContractError("dependency must be a typed relation")
            relation, target = (
                dependency.get("relation"),
                dependency.get("candidate_id"),
            )
            if not isinstance(relation, str) or relation not in allowed_relations:
                raise ContextContractError(
                    "dependency relation is not registered by the profile"
                )
            if not isinstance(target, str) or not target:
                raise ContextContractError("dependency candidate identity is invalid")
            key = (relation, target)
            if key in dependency_keys:
                raise ContextContractError("duplicate dependency relation")
            dependency_keys.add(key)
            pending.append(target)
    return [resolved[key] for key in sorted(resolved)]


def _public_candidate(candidate: Mapping[str, object]) -> dict[str, object]:
    return {
        "candidate_id": candidate["candidate_id"],
        "owner_family": candidate["owner_family"],
        "owner_identity": deepcopy(candidate["owner_identity"]),
        "payload": deepcopy(candidate["payload"]),
    }


def _assemble_bound_context(
    request: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    repository: object,
    pinned_campaign: object,
    selected_live: LiveRouting | None,
    selected_live_reader: object | None,
) -> dict[str, Any]:
    """Internal RuntimeHost route; callers cannot supply this operation basis."""

    scope = _scope(request)
    if (
        not isinstance(pinned_campaign, _PinnedCampaign)
        or pinned_campaign.campaign_id != scope.campaign_id
    ):
        raise ContextContractError(
            "operation basis does not match the Context campaign"
        )
    discovered = discover_candidates(request, candidates)
    available: dict[str, dict[str, object]] = {}
    excluded: list[str] = []
    for item in discovered:
        candidate_id = item["candidate_id"]
        try:
            available[candidate_id] = _resolve_candidate(
                repository,
                pinned_campaign,
                selected_live,
                selected_live_reader,
                scope,
                item,
            )
        except ContextContractError:
            excluded.append(candidate_id)

    trace: dict[str, object] = {
        "profile_id": scope.profile.profile_id,
        "discovered_ids": [item["candidate_id"] for item in discovered],
        "included_ids": [],
        "excluded_ids": sorted(set(excluded)),
    }
    required = _required_closure(
        request["required_ids"], available, set(request["allowed_relations"])
    )
    if required is None:
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    required_set = {item["candidate_id"] for item in required}
    optional = [
        available[item["candidate_id"]]
        for item in discovered
        if item["candidate_id"] not in required_set
        and item["candidate_id"] in available
    ]
    allocation = allocate(required, optional, request["budget"])
    if allocation["outcome"] == "UNSATISFIABLE":
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    outcome = allocation["outcome"]
    if excluded and outcome == "ASSEMBLED":
        outcome = "ASSEMBLED_DEGRADED"
    included = [
        item["candidate_id"] for item in allocation["required"] + allocation["optional"]
    ]
    trace["included_ids"] = included
    bundle = {
        "profile_id": scope.profile.profile_id,
        "role": scope.role,
        "purpose": scope.purpose,
        "subject_id": scope.subject_id,
        "source_frontier": request.get("source_frontier", ""),
        "recipient_id": scope.recipient_id,
        "required": [_public_candidate(item) for item in allocation["required"]],
        "optional": [_public_candidate(item) for item in allocation["optional"]],
        "retrospective_projection": request.get("retrospective", False) is True,
    }
    return {"outcome": outcome, "bundle": bundle, "trace": trace}


def assemble_context(
    request: dict[str, Any], candidates: list[dict[str, Any]]
) -> dict[str, Any]:
    """Reject unbound direct calls; Context is a RuntimeHost sibling service."""

    raise ContextContractError("Context assembly requires the RuntimeHost service")


def resolve_candidate_basis(candidate: dict[str, Any]) -> dict[str, object]:
    """Reject carrier-only resolution; owner validation is host-routed."""

    raise ContextContractError("candidate resolution requires the RuntimeHost service")


def scoped_context_join(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Join only bundles with one identical registered scope."""

    keys = (
        "profile_id",
        "role",
        "purpose",
        "subject_id",
        "source_frontier",
        "recipient_id",
    )
    if any(left.get(key) != right.get(key) for key in keys):
        raise ContextContractError(
            "context join requires one scoped profile/role/purpose basis"
        )
    return {key: left.get(key) for key in keys}
