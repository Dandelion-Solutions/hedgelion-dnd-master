"""Bounded, host-bound and ephemeral Context Runtime admission.

Discovery is untrusted routing input.  A candidate is material only after the
fixed engine dispatch has reloaded and validated its native owner through the
trusted host repository (or, for selected LIVE material, the narrow read-only
Step-5.8 capability).  Context does not persist a basis or own truth,
currentness, knowledge, disclosure or access.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Final, Protocol

try:
    from .context_budget import allocate
    from .live_state import (
        LiveContractError,
        LiveEnvelope,
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
    from .policy_basis import PinnedCampaign, RepositoryPort
    from .access_control import PlayerRecord, AccessControlContractError
except ImportError:  # pragma: no cover - direct-path focused test imports.
    from context_budget import allocate  # type: ignore[no-redef]
    from GAME.TOOLS.live_state import (  # type: ignore[no-redef]
        LiveContractError,
        LiveEnvelope,
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
    from GAME.TOOLS.policy_basis import PinnedCampaign, RepositoryPort  # type: ignore[no-redef]
    from GAME.TOOLS.access_control import (  # type: ignore[no-redef]
        AccessControlContractError,
        PlayerRecord,
    )


class ContextContractError(ValueError):
    """A Context request, discovery hint or owner result is not admissible."""


class SelectedLiveReadCapability(Protocol):
    """Narrow read-only host capability for one already selected LIVE source."""

    def read_selected_live_source(self, route: LiveRouting, source: LiveEnvelope) -> object:
        """Return source-owned read evidence; never a semantic verdict."""


@dataclass(frozen=True, slots=True)
class _RegisteredProfile:
    profile_id: str
    role: str
    purposes: tuple[str, ...]
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
        "profile.interpreter": _RegisteredProfile(
            "profile.interpreter", "INTERPRETER", ("interpretation", "intent"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.intent": _RegisteredProfile(
            "profile.intent", "INTERPRETER", ("interpret", "interpretation", "intent"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.dramaturg": _RegisteredProfile(
            "profile.dramaturg", "DRAMATURG", ("planning", "dramaturgy"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.dramaturgy": _RegisteredProfile(
            "profile.dramaturgy", "DRAMATURG", ("prepare", "planning", "dramaturgy"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.actor": _RegisteredProfile(
            "profile.actor", "ACTOR", ("assessment", "actor"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.chronicler": _RegisteredProfile(
            "profile.chronicler", "CHRONICLER", ("chronicle", "story_projection"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.story": _RegisteredProfile(
            "profile.story", "CHRONICLER", ("story", "chronicle", "story_projection"), _DISCOVERY_CHANNELS, ("requires",)
        ),
        "profile.narrator": _RegisteredProfile(
            "profile.narrator", "NARRATOR", ("narration",), _DISCOVERY_CHANNELS, ("requires",)
        ),
        # Existing schema/examples use this name; it remains a fixed alias.
        "profile.narration": _RegisteredProfile(
            "profile.narration", "NARRATOR", ("narration",), _DISCOVERY_CHANNELS, ("requires",)
        ),
    }
)

_ROLE_ALIASES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "role.interpreter": "INTERPRETER",
        "role.dramaturg": "DRAMATURG",
        "role.actor": "ACTOR",
        "role.chronicler": "CHRONICLER",
        "role.narrator": "NARRATOR",
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
        "world.knowledge",
        "runtime.disclosure",
        "runtime.session",
        "runtime.checkpoint",
        "runtime.collaboration_obligation",
        "runtime.maintenance_audit",
        "runtime.catalog_gap_report",
    }
)


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ContextContractError(f"{label} must be an object")
    return value


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContextContractError(f"{label} must be a nonempty string")
    return value


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


def _scope(request: Mapping[str, object]) -> tuple[_RegisteredProfile, str, str, str, str, str]:
    if not isinstance(request, Mapping):
        raise ContextContractError("Context admission request must be an object")
    forbidden = _FORBIDDEN_AUTHORITY_FIELDS.intersection(request)
    if forbidden:
        raise ContextContractError(
            "caller authority fields are not accepted: " + ", ".join(sorted(forbidden))
        )
    registered = _profile(request.get("profile_id"))
    raw_role = request.get("role", request.get("role_id"))
    role = _ROLE_ALIASES.get(raw_role, raw_role) if isinstance(raw_role, str) else raw_role
    purpose = request.get("purpose")
    subject_id = request.get("subject_id")
    recipient_id = request.get("recipient_id")
    campaign_id = request.get("campaign_id")
    if any(
        not isinstance(value, str) or not value
        for value in (role, purpose, subject_id, recipient_id, campaign_id)
    ):
        raise ContextContractError(
            "owner-routed Context admission requires role, purpose, subject, recipient and campaign"
        )
    if role != registered.role or purpose not in registered.purposes:
        raise ContextContractError("request role/purpose is not admitted by the registered profile")
    channels = _string_list(request.get("allowed_channels"), "allowed_channels", allow_empty=False)
    if any(channel not in registered.channels for channel in channels):
        raise ContextContractError("request channel is not registered by the profile")
    relations = _string_list(request.get("allowed_relations"), "allowed_relations")
    if any(relation not in registered.relations for relation in relations):
        raise ContextContractError("request relation is not registered by the profile")
    limit = request.get("max_candidates")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 0 <= limit <= registered.max_candidates:
        raise ContextContractError("request candidate bound exceeds the registered profile")
    budget = request.get("budget")
    if isinstance(budget, bool) or not isinstance(budget, int) or not 0 <= budget <= registered.max_budget:
        raise ContextContractError("request budget exceeds the registered profile")
    required_ids = _string_list(request.get("required_ids"), "required_ids")
    if len(required_ids) != len(set(required_ids)):
        raise ContextContractError("required_ids must contain unique values")
    return registered, role, purpose, subject_id, recipient_id, campaign_id


def discover_candidates(request: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return only bounded discovery hints; no candidate field grants authority."""

    channels = request.get("allowed_channels")
    limit = request.get("max_candidates")
    if not isinstance(channels, list) or not channels:
        raise ContextContractError("request must name bounded registered discovery channels")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ContextContractError("request must name a nonnegative candidate bound")
    identities: set[str] = set()
    for item in candidates:
        candidate_id = item.get("candidate_id") if isinstance(item, dict) else None
        if not isinstance(candidate_id, str) or not candidate_id or candidate_id in identities:
            raise ContextContractError("candidate identities must be unique nonempty strings")
        identities.add(candidate_id)
    found = [item for item in candidates if isinstance(item, dict) and item.get("channel") in channels]
    return sorted(found, key=lambda item: item["candidate_id"])[:limit]


def _decode_record(value: object, label: str) -> Mapping[str, object]:
    if isinstance(value, (bytes, bytearray)):
        try:
            value = json.loads(bytes(value).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContextContractError(f"{label} is not a JSON owner record") from error
    return _mapping(value, label)


def _identity(value: object, label: str, *, length: int | None = None) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not value:
        raise ContextContractError(f"{label} must be a native identity tuple")
    result = tuple(_nonempty(item, f"{label} item") for item in value)
    if length is not None and len(result) != length:
        raise ContextContractError(f"{label} has the wrong arity")
    return result


def _read_campaign_record(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    family: str,
    identity: tuple[str, ...],
) -> dict[str, object]:
    try:
        route = route_native_record(family, identity)
        raw = repository.read_exact_path(pinned, route.relative_path)
        record = dict(_decode_record(raw, f"{family} owner record"))
        validate_loaded_identity(family, identity, record)
    except (AttributeError, KeyError, OSError, TypeError, ValueError, NativeStorageError) as error:
        raise ContextContractError(f"exact {family} owner record is unavailable or invalid") from error
    record_campaign = record.get("campaign_id")
    if record_campaign is not None and record_campaign != pinned.campaign_id:
        raise ContextContractError("owner record belongs to another campaign")
    return record


def _native_payload(record: Mapping[str, object]) -> dict[str, object]:
    """Keep the owner record as payload without copying discovery authority."""

    return deepcopy(dict(record))


def _public_candidate(candidate: Mapping[str, object]) -> dict[str, object]:
    """Remove internal admission flags before material reaches the role bundle."""

    return {
        "candidate_id": candidate["candidate_id"],
        "owner_family": candidate["owner_family"],
        "owner_identity": deepcopy(candidate["owner_identity"]),
        "payload": deepcopy(candidate["payload"]),
    }


def _candidate_family(candidate: Mapping[str, object]) -> str:
    family = candidate.get("owner_family", candidate.get("family"))
    return _nonempty(family, "candidate owner_family")


def _candidate_scope(candidate: Mapping[str, object], scope: tuple[str, str, str, str, str, str]) -> None:
    _profile_value, role, purpose, subject_id, recipient_id, _campaign_id = scope
    for field_name, expected in (
        ("role", role),
        ("role_id", role),
        ("purpose", purpose),
        ("subject_id", subject_id),
        ("recipient_id", recipient_id),
    ):
        if field_name in candidate:
            supplied = candidate[field_name]
            if field_name in {"role", "role_id"} and isinstance(supplied, str):
                supplied = _ROLE_ALIASES.get(supplied, supplied)
            if supplied != expected:
                raise ContextContractError(f"candidate {field_name} is outside the registered scope")


def _resolve_player(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.player", identity)
    try:
        player = PlayerRecord.from_mapping(record)
    except (AccessControlContractError, AttributeError, TypeError, ValueError) as error:
        raise ContextContractError("native PLAYER record is invalid") from error
    if player.player_id != recipient_id or player.status != "active":
        raise ContextContractError("native PLAYER is not the current eligible recipient")
    return _native_payload(record)


def _resolve_information(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.lore_fact", identity)
    for field_name in ("recipient_player_id", "player_id"):
        if field_name in record and record[field_name] != recipient_id:
            raise ContextContractError("native information is outside the requested recipient scope")
    authorized_recipients = record.get("authorized_recipient_ids")
    if authorized_recipients is not None:
        if not isinstance(authorized_recipients, Sequence) or isinstance(
            authorized_recipients, (str, bytes)
        ) or recipient_id not in authorized_recipients:
            raise ContextContractError("native information recipient eligibility is not admitted")
    return _native_payload(record)


def _resolve_knowledge(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    identity: tuple[str, ...],
    subject_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "world.knowledge", identity)
    if record.get("knower_id") != subject_id:
        raise ContextContractError("native knowledge is outside the requested subject scope")
    authorized_knowers = record.get("authorized_knower_ids")
    if authorized_knowers is not None:
        if not isinstance(authorized_knowers, Sequence) or isinstance(
            authorized_knowers, (str, bytes)
        ) or subject_id not in authorized_knowers:
            raise ContextContractError("native knowledge subject eligibility is not admitted")
    return _native_payload(record)


def _resolve_disclosure(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    identity: tuple[str, ...],
    recipient_id: str,
) -> dict[str, object]:
    record = _read_campaign_record(repository, pinned, "runtime.disclosure", identity)
    if record.get("player_id") != recipient_id:
        raise ContextContractError("native disclosure is outside the requested recipient scope")
    return _native_payload(record)


def _resolve_campaign(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    family: str,
    identity: tuple[str, ...],
) -> dict[str, object]:
    if family not in _CAMPAIGN_FAMILIES:
        raise ContextContractError("candidate family is not a registered native owner")
    return _native_payload(_read_campaign_record(repository, pinned, family, identity))


def _resolve_live(
    route: LiveRouting | None,
    reader: SelectedLiveReadCapability | None,
    pinned: PinnedCampaign,
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
        selected = select_live_source(route, source_key)
        if selected is None:
            raise ContextContractError("LIVE source is not selected by the current route")
        source = require_selected_live_source(route, selected)
        raw = _decode_record(reader.read_selected_live_source(route, source), "LIVE source read")
    except (LiveContractError, ContextContractError, AttributeError, KeyError, OSError, TypeError, ValueError) as error:
        if isinstance(error, ContextContractError):
            raise
        raise ContextContractError("selected LIVE source is stale or invalid") from error
    if (
        raw.get("source_key") != list(source.source_key)
        or raw.get("source_ref") != source.source_ref
        or raw.get("source_revision") != source.source_revision
        or raw.get("source_native_ids") != list(source.source_native_ids)
    ):
        raise ContextContractError("LIVE source read does not match the selected source")
    return deepcopy(dict(raw))


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
        seen: set[tuple[str, str]] = set()
        for dependency in dependencies:
            if not isinstance(dependency, Mapping) or set(dependency) != {"relation", "candidate_id"}:
                raise ContextContractError("dependency must be a typed relation")
            relation = dependency.get("relation")
            target = dependency.get("candidate_id")
            if not isinstance(relation, str) or relation not in allowed_relations:
                raise ContextContractError("dependency relation is not registered by the profile")
            if not isinstance(target, str) or not target:
                raise ContextContractError("dependency candidate identity is invalid")
            key = (relation, target)
            if key in seen:
                raise ContextContractError("duplicate dependency relation")
            seen.add(key)
            pending.append(target)
    return [resolved[key] for key in sorted(resolved)]


@dataclass(frozen=True, slots=True, init=False)
class BoundContextRuntime:
    """Host-composed Context service with no durable per-request state."""

    _repository: RepositoryPort
    _live_route: LiveRouting | None
    _selected_live_reader: SelectedLiveReadCapability | None

    def __init__(self, **_values: object) -> None:
        raise ContextContractError("Context Runtime must be host-bound")

    def resolve_candidate_basis(
        self,
        request: Mapping[str, object],
        candidate: Mapping[str, object],
        *,
        pinned: PinnedCampaign | None = None,
    ) -> dict[str, object]:
        """Resolve one discovery hint through fixed owner dispatch."""

        scope = _scope(request)
        if not isinstance(candidate, Mapping) or not isinstance(candidate, dict):
            raise ContextContractError("Context candidate must be a native discovery mapping")
        forbidden = _FORBIDDEN_AUTHORITY_FIELDS.intersection(candidate)
        if forbidden:
            raise ContextContractError(
                "candidate authority fields are not accepted: " + ", ".join(sorted(forbidden))
            )
        candidate_id = _nonempty(candidate.get("candidate_id"), "candidate identity")
        _candidate_scope(candidate, scope)
        registered, _role, _purpose, subject_id, recipient_id, campaign_id = scope
        if pinned is None:
            try:
                pinned_value = self._repository.pin_campaign(campaign_id)
            except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
                raise ContextContractError("exact campaign currentness is unavailable") from error
            pinned = pinned_value
        if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
            raise ContextContractError("repository did not return the exact campaign pin")
        family = _candidate_family(candidate)
        raw_identity = candidate.get("owner_identity")
        if family in _LIVE_FAMILIES:
            payload = _resolve_live(self._live_route, self._selected_live_reader, pinned, candidate)
        elif family in _PLAYER_FAMILIES:
            payload = _resolve_player(
                self._repository,
                pinned,
                _identity(raw_identity, "PLAYER owner_identity", length=1),
                recipient_id,
            )
        elif family in _INFORMATION_FAMILIES:
            payload = _resolve_information(
                self._repository,
                pinned,
                _identity(raw_identity, "information owner_identity", length=1),
                recipient_id,
            )
        elif family in _KNOWLEDGE_FAMILIES:
            payload = _resolve_knowledge(
                self._repository,
                pinned,
                _identity(raw_identity, "knowledge owner_identity", length=2),
                subject_id,
            )
        elif family in _DISCLOSURE_FAMILIES:
            payload = _resolve_disclosure(
                self._repository,
                pinned,
                _identity(raw_identity, "disclosure owner_identity", length=2),
                recipient_id,
            )
        else:
            payload = _resolve_campaign(
                self._repository,
                pinned,
                family,
                _identity(raw_identity, "campaign owner_identity"),
            )
        # These booleans are an internal post-resolution carrier only.
        admitted: dict[str, object] = {
            "candidate_id": candidate_id,
            "channel": candidate.get("channel"),
            "rank": candidate.get("rank", 0),
            "dependencies": deepcopy(candidate.get("dependencies", [])),
            "owner_family": family,
            "owner_identity": list(candidate.get("owner_identity", candidate.get("source_key", ()))),
            "payload": payload,
            "current": True,
            "eligible": True,
            "profile_id": registered.profile_id,
        }
        return admitted

    def assemble(self, request: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
        """Assemble one bounded ephemeral result from native owner reads."""

        scope = _scope(request)
        registered, role, purpose, subject_id, recipient_id, campaign_id = scope
        try:
            pinned = self._repository.pin_campaign(campaign_id)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
            raise ContextContractError("exact campaign currentness is unavailable") from error
        if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
            raise ContextContractError("repository did not return the exact campaign pin")
        discovered = discover_candidates(request, candidates)
        available: dict[str, dict[str, object]] = {}
        excluded: list[str] = []
        for item in discovered:
            candidate_id = item["candidate_id"]
            try:
                available[candidate_id] = self.resolve_candidate_basis(
                    request,
                    item,
                    pinned=pinned,
                )
            except ContextContractError:
                excluded.append(candidate_id)
        required_ids = request["required_ids"]
        relations = set(request["allowed_relations"])
        trace: dict[str, object] = {
            "profile_id": registered.profile_id,
            "discovered_ids": [item["candidate_id"] for item in discovered],
            "included_ids": [],
            "excluded_ids": sorted(set(excluded)),
        }
        required = _required_closure(required_ids, available, relations)
        if required is None:
            return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
        required_set = {item["candidate_id"] for item in required}
        optional = [
            available[item["candidate_id"]]
            for item in discovered
            if item["candidate_id"] not in required_set and item["candidate_id"] in available
        ]
        allocation = allocate(required, optional, request["budget"])
        if allocation["outcome"] == "UNSATISFIABLE":
            return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
        outcome = allocation["outcome"]
        if excluded and outcome == "ASSEMBLED":
            outcome = "ASSEMBLED_DEGRADED"
        included = [item["candidate_id"] for item in allocation["required"] + allocation["optional"]]
        trace["included_ids"] = included
        bundle = {
            "profile_id": registered.profile_id,
            "role": role,
            "purpose": purpose,
            "subject_id": subject_id,
            "source_frontier": request.get("source_frontier", ""),
            "recipient_id": recipient_id,
            "required": [_public_candidate(item) for item in allocation["required"]],
            "optional": [_public_candidate(item) for item in allocation["optional"]],
            "retrospective_projection": request.get("retrospective", False) is True,
        }
        return {"outcome": outcome, "bundle": bundle, "trace": trace}


def bind_context_runtime(
    repository: RepositoryPort,
    *,
    live_route: LiveRouting | None = None,
    selected_live_reader: SelectedLiveReadCapability | None = None,
) -> BoundContextRuntime:
    """Compose Context once from trusted host capabilities."""

    if not hasattr(repository, "pin_campaign") or not hasattr(repository, "read_exact_path"):
        raise ContextContractError("Context Runtime requires the trusted RepositoryPort")
    if live_route is not None and not isinstance(live_route, LiveRouting):
        raise ContextContractError("Context LIVE route must be owner-typed")
    if selected_live_reader is not None and not hasattr(
        selected_live_reader, "read_selected_live_source"
    ):
        raise ContextContractError("Context LIVE reader must be the narrow read capability")
    if selected_live_reader is not None and live_route is None:
        raise ContextContractError("Context LIVE reader requires its selected route")
    runtime = object.__new__(BoundContextRuntime)
    object.__setattr__(runtime, "_repository", repository)
    object.__setattr__(runtime, "_live_route", live_route)
    object.__setattr__(runtime, "_selected_live_reader", selected_live_reader)
    return runtime


def resolve_candidate_basis(
    candidate: dict[str, Any],
    *,
    request: Mapping[str, object] | None = None,
    runtime: BoundContextRuntime | None = None,
) -> dict[str, object]:
    """Resolve only through a host-bound runtime; caller carriers are rejected."""

    if runtime is None or not isinstance(runtime, BoundContextRuntime):
        raise ContextContractError("candidate requires a host-bound Context Runtime")
    if request is None:
        raise ContextContractError("candidate requires an owner-routed Context request")
    return runtime.resolve_candidate_basis(request, candidate)


def assemble_context(
    request: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    runtime: BoundContextRuntime | None = None,
) -> dict[str, Any]:
    """Compatibility entry point that refuses unbound Context admission."""

    if runtime is None or not isinstance(runtime, BoundContextRuntime):
        raise ContextContractError("Context assembly requires a host-bound Context Runtime")
    return runtime.assemble(request, candidates)


def scoped_context_join(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Join only bundles with one identical registered scope."""

    keys = ("profile_id", "role", "purpose", "subject_id", "source_frontier", "recipient_id")
    if any(left.get(key) != right.get(key) for key in keys):
        raise ContextContractError("context join requires one scoped profile/role/purpose/recipient basis")
    return {key: left.get(key) for key in keys}
