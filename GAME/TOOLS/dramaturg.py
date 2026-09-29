"""Noncanonical bounded Dramaturg horizon validation, admission, and safe rebase."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Final, NoReturn


class DramaturgContractError(ValueError):
    """Raised when prospective planning is treated as authority or is stale."""


class _CorruptDramaturgHorizonError(DramaturgContractError):
    """Stored fixed-route horizon bytes cannot represent the current contract."""


@dataclass(frozen=True, slots=True)
class DramaturgPreparation:
    """Ephemeral preparation result; a candidate is never a retained generation."""

    status: str
    path: str | None
    _candidate_json: str
    generation: int | None = None
    _plan: object | None = None

    @property
    def candidate(self) -> dict[str, object]:
        value = json.loads(self._candidate_json)
        if not isinstance(value, dict):
            raise DramaturgContractError("prepared candidate serialization is invalid")
        return value


@dataclass(frozen=True, slots=True)
class _PreparedDramaturgPublication:
    host_token: object
    basis: object
    candidate_json: str
    record_json: str
    player_id: str
    player_json: str
    path: str
    base_record_json: str | None
    base_generation: int


@dataclass(frozen=True, slots=True)
class _DramaturgSizeReviewOutcome:
    _issuer: object = field(repr=False, compare=False)
    plan: _PreparedDramaturgPublication = field(repr=False, compare=False)
    candidate_json: str = field(repr=False)
    fixed_path: str
    measured_size_bytes: int
    decision: str

    def __reduce__(self) -> NoReturn:
        raise TypeError("Dramaturg size review outcomes are ephemeral")

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError("Dramaturg size review outcomes are ephemeral")


@dataclass(frozen=True, slots=True)
class DramaturgPublicationResult:
    """Publication result; generation is present only after current proof."""

    status: str
    generation: int | None
    outcome: object | None
    preparation: DramaturgPreparation
    measured_sizes: Mapping[str, int] | None = None
    size_band: str | None = None
    _measurement_issuer: object | None = field(default=None, repr=False, compare=False)


_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_ENTRY_KINDS: Final[frozenset[str]] = frozenset(
    {"SOURCE_ANCHORED_CONSTRAINT", "PROVISIONAL_DRAMATURGIC_DIRECTION"}
)
_DRAMATURG_SIZE_REVIEW_ISSUER: Final[object] = object()
# Approximate owner-guidance transitions only; these values never reject a write.
_SIZE_TARGET_MAX_BYTES: Final[int] = 12 * 1024
_SIZE_REVIEW_MAX_BYTES: Final[int] = 16 * 1024


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise DramaturgContractError(f"{label} must be a nonempty string")
    return value


def _identifier(value: object, label: str) -> str:
    result = _nonempty_string(value, label)
    if _ID_PATTERN.fullmatch(result) is None:
        raise DramaturgContractError(f"{label} is not a stable native identifier")
    return result


def dramaturg_horizon_path(scope_kind: object, *, player_id: object = None) -> str:
    """Return one of the two fixed retained Dramaturg routes."""

    if scope_kind == "SHARED" and player_id is None:
        return "DRAMATURG/SHARED.yaml"
    if scope_kind == "PLAYER_LOCAL":
        stable_player_id = _identifier(player_id, "player_id")
        return f"DRAMATURG/PLAYERS/{stable_player_id}.yaml"
    raise DramaturgContractError(
        "only shared and stable-PLAYER-local routes are admitted"
    )


def _string_array(value: object, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise DramaturgContractError(f"{label} must be an array")
    result = [_nonempty_string(item, f"{label} item") for item in value]
    if len(result) != len(set(result)):
        raise DramaturgContractError(f"{label} must be unique")
    return result


def _source_basis_item(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping) or set(value) != {
        "owner_domain",
        "owner_type",
        "identity",
        "currentness",
    }:
        raise DramaturgContractError(
            "source basis must be a typed native-owner reference"
        )
    domain = _nonempty_string(value["owner_domain"], "source owner_domain")
    owner_type = _nonempty_string(value["owner_type"], "source owner_type")
    if domain not in {"CAMPAIGN", "LIVE"}:
        raise DramaturgContractError("unsupported source owner_domain")
    identity = [
        _identifier(item, "source owner identity")
        for item in _string_array(value["identity"], "source owner identity")
    ]
    currentness = value["currentness"]
    if not isinstance(currentness, Mapping) or set(currentness) != {"kind", "value"}:
        raise DramaturgContractError(
            "source currentness must use native-owner evidence"
        )
    currentness_kind = _nonempty_string(currentness["kind"], "source currentness kind")
    currentness_value = currentness["value"]
    if domain == "CAMPAIGN" and owner_type == "world.actor":
        if (
            len(identity) != 1
            or currentness_kind != "STATE_REVISION"
            or isinstance(currentness_value, bool)
            or not isinstance(currentness_value, int)
            or currentness_value < 0
        ):
            raise DramaturgContractError(
                "world.actor basis requires its native state_revision"
            )
    elif domain == "CAMPAIGN" and owner_type == "runtime.semantic_event":
        if (
            len(identity) != 1
            or currentness_kind != "SEMANTIC_ORDER"
            or isinstance(currentness_value, bool)
            or not isinstance(currentness_value, int)
            or currentness_value < 1
        ):
            raise DramaturgContractError(
                "semantic-event basis requires its immutable semantic_order"
            )
    elif domain == "LIVE" and owner_type == "LIVE":
        if (
            len(identity) != 3
            or currentness_kind != "SOURCE_REVISION"
            or not isinstance(currentness_value, str)
            or not currentness_value
        ):
            raise DramaturgContractError(
                "LIVE basis requires exact source identity and source_revision"
            )
        currentness_value = _identifier(currentness_value, "LIVE source_revision")
    else:
        raise DramaturgContractError(
            "source basis owner has no admitted currentness contract"
        )
    return {
        "owner_domain": domain,
        "owner_type": owner_type,
        "identity": identity,
        "currentness": {"kind": currentness_kind, "value": currentness_value},
    }


def _source_key(value: Mapping[str, object]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _source_basis(value: object) -> list[dict[str, object]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise DramaturgContractError("source_basis must be an array")
    basis = [_source_basis_item(item) for item in value]
    keys = [_source_key(item) for item in basis]
    if len(keys) != len(set(keys)):
        raise DramaturgContractError("source_basis must be unique")
    owner_keys = [
        _source_key(
            {
                "owner_domain": item["owner_domain"],
                "owner_type": item["owner_type"],
                "identity": item["identity"],
            }
        )
        for item in basis
    ]
    if len(owner_keys) != len(set(owner_keys)):
        raise DramaturgContractError(
            "one native owner cannot carry conflicting currentness evidence"
        )
    return [item for _key, item in sorted(zip(keys, basis, strict=True))]


def _scope(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise DramaturgContractError("Dramaturg scope must be an object")
    kind = value.get("kind")
    if kind == "SHARED" and set(value) == {"kind"}:
        return {"kind": "SHARED"}
    if kind == "PLAYER_LOCAL" and set(value) == {"kind", "player_id"}:
        return {
            "kind": "PLAYER_LOCAL",
            "player_id": _identifier(value["player_id"], "player_id"),
        }
    raise DramaturgContractError(
        "Dramaturg scope is not one of the two retained families"
    )


def _shared_basis(value: object, *, scope_id: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise DramaturgContractError("player-local shared_basis is required")
    kind = value.get("kind")
    if kind == "ABSENT" and set(value) == {"kind"}:
        return {"kind": "ABSENT"}
    if kind != "BOUND" or set(value) != {"kind", "scope_id", "generation"}:
        raise DramaturgContractError("shared_basis must be ABSENT or exact BOUND")
    shared_scope_id = _identifier(value["scope_id"], "shared basis scope_id")
    generation = value["generation"]
    if shared_scope_id != scope_id:
        raise DramaturgContractError("BOUND shared_basis belongs to another campaign")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
        raise DramaturgContractError("BOUND shared generation must be positive")
    return {"kind": "BOUND", "scope_id": shared_scope_id, "generation": generation}


def _entry(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping) or set(value) != {
        "kind",
        "text",
        "source_basis",
        "assumptions",
    }:
        raise DramaturgContractError(
            "Dramaturg entry has unsupported or missing fields"
        )
    kind = _nonempty_string(value["kind"], "Dramaturg entry kind")
    if kind not in _ENTRY_KINDS:
        raise DramaturgContractError("unsupported Dramaturg entry kind")
    basis = _source_basis(value["source_basis"])
    assumptions = _string_array(value["assumptions"], "Dramaturg assumptions")
    if kind == "SOURCE_ANCHORED_CONSTRAINT" and not basis:
        raise DramaturgContractError(
            "source-anchored constraints require typed source basis"
        )
    return {
        "kind": kind,
        "text": _nonempty_string(value["text"], "Dramaturg entry text"),
        "source_basis": basis,
        "assumptions": assumptions,
    }


def _entries(value: object) -> list[dict[str, object]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise DramaturgContractError("entries must be an array")
    return [_entry(item) for item in value]


def _entry_source_union(
    entries: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    unique: dict[str, dict[str, object]] = {}
    for entry in entries:
        entry_basis = entry["source_basis"]
        if not isinstance(entry_basis, Sequence):
            raise DramaturgContractError("entry source_basis is invalid")
        for item in entry_basis:
            if not isinstance(item, Mapping):
                raise DramaturgContractError("entry source_basis item is invalid")
            unique[_source_key(item)] = dict(item)
    return [unique[key] for key in sorted(unique)]


def _planning_base(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise DramaturgContractError("candidate planning_base must be explicit")
    kind = value.get("kind")
    if kind == "ABSENT" and set(value) == {"kind"}:
        return {"kind": "ABSENT"}
    if kind != "BOUND" or set(value) != {"kind", "generation"}:
        raise DramaturgContractError("planning_base must be ABSENT or exact BOUND")
    generation = value["generation"]
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
        raise DramaturgContractError("planning_base generation must be positive")
    return {"kind": "BOUND", "generation": generation}


def _candidate(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise DramaturgContractError("Dramaturg candidate must be an object")
    scope = _scope(value.get("scope"))
    required = {"scope_id", "scope", "planning_base", "source_basis", "entries"}
    expected = required | (
        {"shared_basis"} if scope["kind"] == "PLAYER_LOCAL" else set()
    )
    if set(value) != expected:
        raise DramaturgContractError(
            "candidate cannot carry generation or unsupported fields"
        )
    scope_id = _identifier(value["scope_id"], "candidate scope_id")
    entries = _entries(value["entries"])
    source_basis = _source_basis(value["source_basis"])
    if source_basis != _entry_source_union(entries):
        raise DramaturgContractError(
            "candidate source_basis must equal its entry-local bases"
        )
    result: dict[str, object] = {
        "scope_id": scope_id,
        "scope": scope,
        "planning_base": _planning_base(value["planning_base"]),
        "source_basis": source_basis,
        "entries": entries,
    }
    if scope["kind"] == "PLAYER_LOCAL":
        result["shared_basis"] = _shared_basis(value["shared_basis"], scope_id=scope_id)
    return result


def build_dramaturg_candidate(
    scope_id: object,
    scope: object,
    entries: object,
    *,
    shared_basis: object = None,
    planning_base: object = None,
) -> dict[str, object]:
    """Build an ephemeral candidate without a persisted schema or generation."""

    normalized_scope = _scope(scope)
    normalized_scope_id = _identifier(scope_id, "candidate scope_id")
    normalized_entries = _entries(entries)
    value: dict[str, object] = {
        "scope_id": normalized_scope_id,
        "scope": normalized_scope,
        "planning_base": _planning_base(
            {"kind": "ABSENT"} if planning_base is None else planning_base
        ),
        "source_basis": _entry_source_union(normalized_entries),
        "entries": normalized_entries,
    }
    if normalized_scope["kind"] == "PLAYER_LOCAL":
        if shared_basis is None:
            shared_basis = {"kind": "ABSENT"}
        value["shared_basis"] = _shared_basis(
            shared_basis, scope_id=normalized_scope_id
        )
    elif shared_basis is not None:
        raise DramaturgContractError("shared horizon cannot carry a shared_basis")
    return _candidate(value)


def _dramaturg_size_band(size_bytes: int) -> str:
    """Classify owner review bands; the result is guidance, never a hard cap."""

    if size_bytes <= _SIZE_TARGET_MAX_BYTES:
        return "PREFERRED_TARGET"
    if size_bytes <= _SIZE_REVIEW_MAX_BYTES:
        return "REVIEW"
    return "REVIEW_PARTITION"


def _issue_dramaturg_owner_size_review_outcome(
    result: DramaturgPublicationResult, *, decision: str
) -> _DramaturgSizeReviewOutcome:
    """Issue one ephemeral trusted owner outcome for an exact measured candidate."""

    if (
        not isinstance(result, DramaturgPublicationResult)
        or result.status != "SIZE_REVIEW_REQUIRED"
        or result._measurement_issuer is not _DRAMATURG_SIZE_REVIEW_ISSUER
    ):
        raise DramaturgContractError(
            "owner size review requires a measured review-band result"
        )
    if decision not in {"APPROVE_EXISTING_ROUTE", "REPREPARE"}:
        raise DramaturgContractError("Dramaturg size review decision is not admitted")
    plan = result.preparation._plan
    sizes = result.measured_sizes
    if not isinstance(plan, _PreparedDramaturgPublication) or not isinstance(
        sizes, Mapping
    ):
        raise DramaturgContractError("owner size review result is incomplete")
    measured_size = sizes.get(plan.path)
    if (
        type(measured_size) is not int
        or measured_size < 0
        or _dramaturg_size_band(measured_size) == "PREFERRED_TARGET"
        or result.size_band != _dramaturg_size_band(measured_size)
    ):
        raise DramaturgContractError("owner size review measurement is inconsistent")
    return _DramaturgSizeReviewOutcome(
        _issuer=_DRAMATURG_SIZE_REVIEW_ISSUER,
        plan=plan,
        candidate_json=plan.record_json,
        fixed_path=plan.path,
        measured_size_bytes=measured_size,
        decision=decision,
    )


def _validate_dramaturg_size_review_outcome(
    value: object,
    *,
    plan: _PreparedDramaturgPublication,
    size_bytes: int,
) -> _DramaturgSizeReviewOutcome:
    if (
        not isinstance(value, _DramaturgSizeReviewOutcome)
        or value._issuer is not _DRAMATURG_SIZE_REVIEW_ISSUER
        or value.plan is not plan
        or value.candidate_json != plan.record_json
        or value.fixed_path != plan.path
        or value.measured_size_bytes != size_bytes
        or value.decision not in {"APPROVE_EXISTING_ROUTE", "REPREPARE"}
    ):
        raise DramaturgContractError(
            "Dramaturg size review outcome is not bound to this exact candidate/path/size"
        )
    return value


def _runtime_host_basis(host: object) -> tuple[object, object]:
    try:
        from .runtime_host import RuntimeHost, _OperationBasis
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError(
            "RuntimeHost publication owners are unavailable"
        ) from exc
    if not isinstance(host, RuntimeHost):
        raise DramaturgContractError("Dramaturg requires the bound RuntimeHost")
    try:
        basis = host._begin_operation()
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError("Dramaturg campaign pin failed") from exc
    if (
        not isinstance(basis, _OperationBasis)
        or basis.host_token is not host._basis_token
        or basis.pinned_campaign.campaign_id != host.campaign_id
    ):
        raise DramaturgContractError("Dramaturg operation basis is not host-issued")
    return host, basis


def _exact_campaign_mapping(
    host: object, basis: object, path: str
) -> dict[str, object]:
    pinned = getattr(basis, "pinned_campaign", None)
    repository = getattr(host, "_repository", None)
    if pinned is None or repository is None:
        raise DramaturgContractError(
            "Dramaturg exact read requires a pinned host basis"
        )
    try:
        value = repository.read_exact_path(pinned, path)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            f"exact Dramaturg owner is unavailable: {path}"
        ) from exc
    if not isinstance(value, Mapping):
        raise DramaturgContractError(f"exact Dramaturg owner is not an object: {path}")
    try:
        normalized = json.loads(_canonical_json(value))
    except (TypeError, ValueError, RecursionError) as exc:
        raise DramaturgContractError(
            f"exact Dramaturg owner is not JSON-safe: {path}"
        ) from exc
    if not isinstance(normalized, dict):
        raise DramaturgContractError(f"exact Dramaturg owner is not an object: {path}")
    return normalized


def _canonical_json(value: object) -> str:
    def thaw(item: object) -> object:
        if isinstance(item, Mapping):
            if any(not isinstance(key, str) for key in item):
                raise DramaturgContractError("publication JSON keys must be strings")
            return {key: thaw(nested) for key, nested in item.items()}
        if isinstance(item, Sequence) and not isinstance(item, (str, bytes, bytearray)):
            return [thaw(nested) for nested in item]
        return item

    return json.dumps(
        thaw(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _read_optional_campaign_mapping(
    host: object, basis: object, path: str
) -> dict[str, object] | None:
    pinned = getattr(basis, "pinned_campaign", None)
    repository = getattr(host, "_repository", None)
    if pinned is None or repository is None:
        raise DramaturgContractError(
            "Dramaturg exact read requires a pinned host basis"
        )
    try:
        value = repository.read_exact_path(pinned, path)
    except KeyError:
        return None
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            f"exact Dramaturg owner read failed: {path}"
        ) from exc
    if not isinstance(value, Mapping):
        raise _CorruptDramaturgHorizonError(
            f"stored Dramaturg horizon is not an object: {path}"
        )
    try:
        normalized = json.loads(_canonical_json(value))
    except (TypeError, ValueError, RecursionError) as exc:
        raise _CorruptDramaturgHorizonError(
            f"stored Dramaturg horizon is not JSON-safe: {path}"
        ) from exc
    if not isinstance(normalized, dict):
        raise _CorruptDramaturgHorizonError(
            f"stored Dramaturg horizon is not an object: {path}"
        )
    return normalized


def _current_player_owner(
    host: object, basis: object, player_id: str
) -> tuple[dict[str, object], dict[str, object], object]:
    try:
        from .access_control import (
            PlayerRecord,
            PrincipalPlayerRoute,
            VerifiedPrincipal,
            resolve_player,
        )
        from .native_storage import route_native_record, validate_loaded_identity
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError("native PLAYER owners are unavailable") from exc
    campaign_id = _identifier(
        getattr(host, "campaign_id", None), "RuntimeHost campaign_id"
    )
    manifest = _exact_campaign_mapping(host, basis, "MANIFEST.yaml")
    if (
        manifest.get("campaign_id") != campaign_id
        or manifest.get("mode") != "multiplayer"
    ):
        raise DramaturgContractError(
            "retained planning requires current multiplayer MANIFEST"
        )
    players = manifest.get("players")
    if not isinstance(players, Mapping):
        raise DramaturgContractError("current MANIFEST has no PLAYER routing owner")
    player_ids = _string_array(players.get("player_ids"), "MANIFEST players.player_ids")
    if player_id not in player_ids:
        raise DramaturgContractError(
            "nominated PLAYER is not in current MANIFEST membership"
        )
    path = route_native_record("world.player", (player_id,)).relative_path
    payload = _exact_campaign_mapping(host, basis, path)
    try:
        validate_loaded_identity("world.player", (player_id,), payload)
        player = PlayerRecord.from_mapping(payload)
    except (TypeError, ValueError) as exc:
        raise DramaturgContractError("current PLAYER owner is invalid") from exc
    if payload.get("campaign_id") != campaign_id or player.player_id != player_id:
        raise DramaturgContractError("current PLAYER identity or campaign differs")
    if player.status != "active":
        raise DramaturgContractError("current PLAYER is inactive")
    pinned = getattr(basis, "pinned_campaign", None)
    transport = getattr(host, "_publication_transport", None)
    publication_service = getattr(host, "publication", None)
    try:
        principal = publication_service._resolve_principal(transport, pinned)
        principal_route = PrincipalPlayerRoute.from_mapping(
            _exact_campaign_mapping(
                host, basis, "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
            )
        )
        # W03 routing uses only the stable account ID. Login is a non-authoritative
        # display member of VerifiedPrincipal; when the current PLAYER omits it,
        # carry the authenticated stable ID rather than accepting caller text.
        verified_principal = VerifiedPrincipal(
            stable_account_id=principal.principal_id,
            login=player.login or principal.principal_id,
        )

        def load_route_candidate(candidate_id: str) -> dict[str, object]:
            candidate_path = route_native_record(
                "world.player", (candidate_id,)
            ).relative_path
            candidate = _exact_campaign_mapping(host, basis, candidate_path)
            validate_loaded_identity("world.player", (candidate_id,), candidate)
            if candidate.get("campaign_id") != campaign_id:
                raise DramaturgContractError(
                    "principal route candidate has foreign campaign scope"
                )
            return candidate

        resolution = resolve_player(
            verified_principal,
            principal_route,
            load_route_candidate,
            campaign_id=campaign_id,
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            "current authenticated PLAYER binding is unavailable"
        ) from exc
    if (
        resolution.status != "AUTHORIZED_PLAYER"
        or resolution.player is None
        or resolution.player != player
        or resolution.player_id != player_id
        or resolution.campaign_id != campaign_id
    ):
        raise DramaturgContractError(
            "nominated PLAYER differs from authenticated current binding"
        )
    return manifest, payload, player


def _read_horizon_owner(
    host: object,
    basis: object,
    path: str,
    *,
    scope_kind: str,
    player_id: str | None,
) -> dict[str, object] | None:
    value = _read_optional_campaign_mapping(host, basis, path)
    if value is None:
        return None
    try:
        horizon = validate_dramaturg_horizon(value)
    except DramaturgContractError as exc:
        raise _CorruptDramaturgHorizonError(
            f"stored Dramaturg horizon is corrupt or unsupported: {path}"
        ) from exc
    scope = horizon["scope"]
    if not isinstance(scope, Mapping) or horizon["scope_id"] != getattr(
        host, "campaign_id", None
    ):
        raise _CorruptDramaturgHorizonError(
            "retained horizon does not match its fixed campaign route"
        )
    if scope.get("kind") != scope_kind:
        raise _CorruptDramaturgHorizonError(
            "retained horizon scope differs from its fixed route"
        )
    if scope_kind == "PLAYER_LOCAL" and scope.get("player_id") != player_id:
        raise _CorruptDramaturgHorizonError(
            "retained local horizon belongs to another stable PLAYER"
        )
    return horizon


def _context_resolve_sources(
    host: object,
    player_id: str,
    source_basis: Sequence[Mapping[str, object]],
) -> tuple[dict[str, dict[str, object]], dict[str, object]]:
    context_service = getattr(host, "context", None)
    assemble = getattr(context_service, "assemble", None)
    if not callable(assemble):
        raise DramaturgContractError("RuntimeHost ContextService is unavailable")
    player_candidate_id = "dramaturg-current-player"
    subject_id = _identifier(
        getattr(host, "campaign_id", None), "Dramaturg campaign subject"
    )
    candidates: list[dict[str, object]] = [
        {
            "candidate_id": player_candidate_id,
            "channel": "EXPLICIT_REF",
            "role": "DRAMATURG",
            "purpose": "prepare",
            "subject_id": subject_id,
            "recipient_id": player_id,
            "owner_family": "world.player",
            "owner_identity": [player_id],
            "dependencies": [],
            "rank": 0,
        }
    ]
    channels = {"EXPLICIT_REF"}
    candidate_sources: dict[str, str] = {}
    for index, source in enumerate(source_basis):
        domain = source["owner_domain"]
        owner_type = source["owner_type"]
        identity = source["identity"]
        if not isinstance(identity, list):
            raise DramaturgContractError("typed source identity is invalid")
        if domain == "CAMPAIGN" and owner_type == "world.actor":
            candidate_id = f"dramaturg-source-{index:03d}"
            candidate = {
                "candidate_id": candidate_id,
                "channel": "EXPLICIT_REF",
                "role": "DRAMATURG",
                "purpose": "prepare",
                "subject_id": subject_id,
                "recipient_id": player_id,
                "owner_family": "world.actor",
                "owner_identity": list(identity),
                "dependencies": [],
                "rank": 0,
            }
        elif domain == "LIVE" and owner_type == "LIVE":
            candidate_id = f"dramaturg-source-{index:03d}"
            candidate = {
                "candidate_id": candidate_id,
                "channel": "LIVE_CURRENT",
                "role": "DRAMATURG",
                "purpose": "prepare",
                "subject_id": subject_id,
                "recipient_id": player_id,
                "owner_family": "LIVE",
                "owner_identity": list(identity),
                "source_key": list(identity),
                "dependencies": [],
                "rank": 0,
            }
            channels.add("LIVE_CURRENT")
        else:
            continue
        candidates.append(candidate)
        candidate_sources[candidate_id] = _source_key(source)

    request: dict[str, object] = {
        "profile_id": "profile.dramaturgy",
        "role": "DRAMATURG",
        "purpose": "prepare",
        "subject_id": subject_id,
        "recipient_id": player_id,
        "campaign_id": getattr(host, "campaign_id", None),
        "allowed_channels": sorted(channels),
        "max_candidates": len(candidates),
        "required_ids": [candidate["candidate_id"] for candidate in candidates],
        "allowed_relations": [],
        "budget": 1_000_000,
    }
    try:
        result = assemble(request, candidates)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            "registered Dramaturg Context admission failed"
        ) from exc
    if not isinstance(result, Mapping) or result.get("outcome") != "ASSEMBLED":
        raise DramaturgContractError(
            "registered Dramaturg Context admission is unsatisfiable"
        )
    bundle = result.get("bundle")
    if (
        not isinstance(bundle, Mapping)
        or bundle.get("profile_id") != "profile.dramaturgy"
        or bundle.get("role") != "DRAMATURG"
        or bundle.get("purpose") != "prepare"
        or bundle.get("recipient_id") != player_id
        or bundle.get("subject_id") != subject_id
        or not isinstance(bundle.get("required"), Sequence)
    ):
        raise DramaturgContractError("Context returned an unbound Dramaturg bundle")
    resolved: dict[str, dict[str, object]] = {}
    player_payload: dict[str, object] | None = None
    for item in bundle["required"]:
        if not isinstance(item, Mapping) or not isinstance(
            item.get("payload"), Mapping
        ):
            raise DramaturgContractError("Context required owner evidence is malformed")
        candidate_id = item.get("candidate_id")
        payload = deepcopy(dict(item["payload"]))
        if candidate_id == player_candidate_id:
            player_payload = payload
        elif isinstance(candidate_id, str) and candidate_id in candidate_sources:
            if item.get("owner_family") not in {"world.actor", "LIVE"}:
                raise DramaturgContractError(
                    "Context source family differs from its typed basis"
                )
            resolved[candidate_sources[candidate_id]] = payload
    if player_payload is None or len(resolved) != len(candidate_sources):
        raise DramaturgContractError("Context omitted a required owner source")
    return resolved, player_payload


def _validate_sources_at_basis(
    host: object,
    basis: object,
    source_basis: Sequence[Mapping[str, object]],
    context_sources: Mapping[str, Mapping[str, object]],
    context_player: Mapping[str, object],
    current_player: object,
    *,
    scope: Mapping[str, object],
) -> None:
    try:
        from .access_control import PlayerRecord
        from .history import validate_semantic_event_draft
        from .live_state import LiveRouting
        from .native_storage import route_native_record, validate_loaded_identity
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError(
            "native Dramaturg source validators are unavailable"
        ) from exc
    if not isinstance(current_player, PlayerRecord):
        raise DramaturgContractError("current authenticated PLAYER is not owner-typed")
    if dict(context_player) != _exact_campaign_mapping(
        host,
        basis,
        route_native_record("world.player", (current_player.player_id,)).relative_path,
    ):
        raise DramaturgContractError(
            "Context PLAYER evidence changed before exact owner recheck"
        )
    for source in source_basis:
        source_key = _source_key(source)
        domain = source["owner_domain"]
        owner_type = source["owner_type"]
        identity = source["identity"]
        currentness = source["currentness"]
        if not isinstance(identity, list) or not isinstance(currentness, Mapping):
            raise DramaturgContractError("typed source basis is malformed")
        if domain == "CAMPAIGN" and owner_type == "world.actor":
            path = route_native_record("world.actor", identity).relative_path
            payload = _exact_campaign_mapping(host, basis, path)
            try:
                validate_loaded_identity("world.actor", identity, payload)
            except ValueError as exc:
                raise DramaturgContractError(
                    "current Actor owner identity is invalid"
                ) from exc
            observed = context_sources.get(source_key)
            if observed is None or dict(observed) != payload:
                raise DramaturgContractError(
                    "Actor source changed after Context admission"
                )
            revision = payload.get("state_revision")
            if (
                isinstance(revision, bool)
                or not isinstance(revision, int)
                or revision != currentness.get("value")
            ):
                raise DramaturgContractError("Actor source revision is stale")
            if scope.get("kind") == "PLAYER_LOCAL":
                state = payload.get("state")
                roles = state.get("roles", []) if isinstance(state, Mapping) else []
                if (
                    isinstance(roles, Sequence)
                    and not isinstance(roles, (str, bytes))
                    and "actor.player_character" in roles
                    and identity[0] not in current_player.controlled_pc_ids
                ):
                    raise DramaturgContractError(
                        "PLAYER-local planning cannot retain another PLAYER's PC basis"
                    )
        elif domain == "CAMPAIGN" and owner_type == "runtime.semantic_event":
            payload = _exact_campaign_mapping(
                host,
                basis,
                route_native_record("runtime.semantic_event", identity).relative_path,
            )
            try:
                event = validate_semantic_event_draft(payload)
            except (TypeError, ValueError) as exc:
                raise DramaturgContractError(
                    "native semantic-event basis is invalid"
                ) from exc
            if event.get("event_id") != identity[0] or event.get(
                "semantic_order"
            ) != currentness.get("value"):
                raise DramaturgContractError("immutable semantic-event basis changed")
        elif domain == "LIVE" and owner_type == "LIVE":
            observed = context_sources.get(source_key)
            selected_live = getattr(basis, "selected_live", None)
            if observed is None or not isinstance(selected_live, LiveRouting):
                raise DramaturgContractError("selected LIVE source is unavailable")
            matching = [
                entry
                for entry in selected_live.entries
                if entry.source_key == tuple(identity)
            ]
            if len(matching) != 1:
                raise DramaturgContractError(
                    "LIVE basis is not selected by the current route"
                )
            selected_mapping = matching[0].as_mapping()
            if dict(observed) != selected_mapping or observed.get(
                "source_revision"
            ) != currentness.get("value"):
                raise DramaturgContractError("LIVE source basis is stale or changed")
        else:  # _source_basis_item already closes the admitted owner vocabulary.
            raise DramaturgContractError("source basis owner is not revalidatable")


def prepare_dramaturg_publication(
    host: object,
    candidate_value: object,
    *,
    player_id: object = None,
) -> DramaturgPreparation:
    """Prepare a host-checked multiplayer publication or leave single-player ephemeral."""

    host, basis = _runtime_host_basis(host)
    candidate = _candidate(candidate_value)
    campaign_id = _identifier(
        getattr(host, "campaign_id", None), "RuntimeHost campaign_id"
    )
    if candidate["scope_id"] != campaign_id:
        raise DramaturgContractError("candidate belongs to another campaign")
    manifest = _exact_campaign_mapping(host, basis, "MANIFEST.yaml")
    if manifest.get("campaign_id") != campaign_id:
        raise DramaturgContractError("current MANIFEST belongs to another campaign")
    mode = manifest.get("mode")
    if mode not in ("singleplayer", "multiplayer"):
        raise DramaturgContractError("current MANIFEST mode is unavailable or invalid")
    if mode == "singleplayer":
        return DramaturgPreparation(
            "EPHEMERAL", None, _canonical_json(candidate), None, None
        )
    stable_player_id = _identifier(player_id, "current PLAYER nomination")
    scope = candidate["scope"]
    if not isinstance(scope, Mapping):
        raise DramaturgContractError("candidate scope is invalid")
    if (
        scope.get("kind") == "PLAYER_LOCAL"
        and scope.get("player_id") != stable_player_id
    ):
        raise DramaturgContractError(
            "PLAYER-local candidate belongs to another stable PLAYER"
        )

    manifest_before, player_before, _player_record_before = _current_player_owner(
        host, basis, stable_player_id
    )
    scope_kind = str(scope["kind"])
    path = dramaturg_horizon_path(
        scope_kind,
        player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
    )
    base_horizon = _read_horizon_owner(
        host,
        basis,
        path,
        scope_kind=scope_kind,
        player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
    )
    base_generation = 0 if base_horizon is None else int(base_horizon["generation"])
    base_record_json = None if base_horizon is None else _canonical_json(base_horizon)
    current_planning_base: dict[str, object] = (
        {"kind": "ABSENT"}
        if base_horizon is None
        else {"kind": "BOUND", "generation": base_generation}
    )
    if candidate["planning_base"] != current_planning_base:
        raise DramaturgContractError(
            "candidate planning_base differs from the exact current horizon generation"
        )

    shared_horizon: dict[str, object] | None = None
    shared_basis = candidate.get("shared_basis")
    if (
        scope_kind == "PLAYER_LOCAL"
        and isinstance(shared_basis, Mapping)
        and shared_basis.get("kind") == "BOUND"
    ):
        shared_path = dramaturg_horizon_path("SHARED")
        shared_horizon = _read_horizon_owner(
            host, basis, shared_path, scope_kind="SHARED", player_id=None
        )
        if shared_horizon is None:
            raise DramaturgContractError(
                "BOUND shared basis is absent from its fixed current route"
            )
        if shared_horizon["scope_id"] != shared_basis.get("scope_id") or shared_horizon[
            "generation"
        ] != shared_basis.get("generation"):
            raise DramaturgContractError(
                "BOUND shared generation is not the exact current generation"
            )

    sources: list[object] = list(candidate["source_basis"])
    if shared_horizon is not None:
        shared_sources = shared_horizon["source_basis"]
        if not isinstance(shared_sources, Sequence):
            raise DramaturgContractError("current shared source basis is malformed")
        sources.extend(shared_sources)
    source_basis = _source_basis(sources)
    context_sources, context_player = _context_resolve_sources(
        host, stable_player_id, source_basis
    )

    host, final_basis = _runtime_host_basis(host)
    manifest_after, player_after, player_record_after = _current_player_owner(
        host, final_basis, stable_player_id
    )
    if manifest_before != manifest_after or player_before != player_after:
        raise DramaturgContractError(
            "current mode or PLAYER changed during planning admission"
        )
    current_after = _read_horizon_owner(
        host,
        final_basis,
        path,
        scope_kind=scope_kind,
        player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
    )
    if (
        None if current_after is None else _canonical_json(current_after)
    ) != base_record_json:
        raise DramaturgContractError("affected horizon moved during planning admission")
    if shared_horizon is not None:
        shared_after = _read_horizon_owner(
            host,
            final_basis,
            dramaturg_horizon_path("SHARED"),
            scope_kind="SHARED",
            player_id=None,
        )
        if shared_after is None or _canonical_json(shared_after) != _canonical_json(
            shared_horizon
        ):
            raise DramaturgContractError(
                "BOUND shared horizon moved during local admission"
            )

    _validate_sources_at_basis(
        host,
        final_basis,
        source_basis,
        context_sources,
        context_player,
        player_record_after,
        scope=scope,
    )
    record = {
        "schema_version": 2,
        "scope_id": campaign_id,
        "scope": dict(scope),
        "generation": base_generation + 1,
        "source_basis": candidate["source_basis"],
        "entries": candidate["entries"],
    }
    if scope_kind == "PLAYER_LOCAL":
        record["shared_basis"] = candidate["shared_basis"]
    record = validate_dramaturg_horizon(record)
    plan = _PreparedDramaturgPublication(
        host_token=getattr(host, "_basis_token", None),
        basis=final_basis,
        candidate_json=_canonical_json(candidate),
        record_json=_canonical_json(record),
        player_id=stable_player_id,
        player_json=_canonical_json(player_after),
        path=path,
        base_record_json=base_record_json,
        base_generation=base_generation,
    )
    return DramaturgPreparation(
        "READY", path, plan.record_json, int(record["generation"]), plan
    )


def _bound_shared_horizon(
    host: object, basis: object, record: Mapping[str, object]
) -> dict[str, object] | None:
    scope = record.get("scope")
    shared_basis = record.get("shared_basis")
    if (
        not isinstance(scope, Mapping)
        or scope.get("kind") != "PLAYER_LOCAL"
        or not isinstance(shared_basis, Mapping)
        or shared_basis.get("kind") != "BOUND"
    ):
        return None
    shared = _read_horizon_owner(
        host,
        basis,
        dramaturg_horizon_path("SHARED"),
        scope_kind="SHARED",
        player_id=None,
    )
    if shared is None:
        raise DramaturgContractError("BOUND shared horizon is absent")
    if shared.get("scope_id") != shared_basis.get("scope_id") or shared.get(
        "generation"
    ) != shared_basis.get("generation"):
        raise DramaturgContractError("BOUND shared generation is no longer current")
    return shared


def promote_accepted_dramaturg_generation(
    host: object,
    preparation: DramaturgPreparation,
    outcome: object,
) -> dict[str, object]:
    """Promote only an exact W02-accepted record still current with native owners."""

    if (
        not isinstance(preparation, DramaturgPreparation)
        or preparation.status != "READY"
    ):
        raise DramaturgContractError("a prepared multiplayer publication is required")
    plan = preparation._plan
    if not isinstance(plan, _PreparedDramaturgPublication):
        raise DramaturgContractError("publication plan is not Dramaturg-owner issued")
    host, _initial_basis = _runtime_host_basis(host)
    if plan.host_token is not getattr(host, "_basis_token", None):
        raise DramaturgContractError(
            "Dramaturg publication plan belongs to another host"
        )
    try:
        from .durability import route_serialized_operation
        from .publication import (
            PublicationOutcome,
            PublicationStatus,
            validate_owner_issued_accepted_publication,
        )
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError("W02 publication owner is unavailable") from exc
    if (
        not isinstance(outcome, PublicationOutcome)
        or outcome.status is not PublicationStatus.ACCEPTED
    ):
        raise DramaturgContractError(
            "W02 did not confirm ordinary campaign publication"
        )
    candidate_record = validate_dramaturg_horizon(json.loads(plan.record_json))
    player_payload = json.loads(plan.player_json)
    if not isinstance(player_payload, dict):
        raise DramaturgContractError("prepared PLAYER publication anchor is invalid")
    routed_operation = route_serialized_operation(
        "world.player", plan.player_id, player_payload
    )
    expected_generations = {plan.path: int(candidate_record["generation"])}
    expected_operations = {
        routed_operation.relative_path: player_payload,
        plan.path: candidate_record,
    }
    try:
        acceptance = validate_owner_issued_accepted_publication(
            outcome,
            campaign_id=getattr(host, "campaign_id", ""),
            expected_pinned_head_sha=getattr(
                getattr(plan.basis, "pinned_campaign", None), "revision", None
            ),
        )
    except (AttributeError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            "W02 acceptance evidence is not owner-issued"
        ) from exc
    attempt = acceptance.attempt
    if (
        _canonical_json(attempt.path_operations) != _canonical_json(expected_operations)
        or dict(attempt.owner_generations) != expected_generations
        or attempt.routed_operation != routed_operation
        or attempt.publication_reason != "dramaturg-horizon"
    ):
        raise DramaturgContractError(
            "W02 acceptance does not bind this exact Dramaturg delta"
        )

    candidate_sources = candidate_record["source_basis"]
    if not isinstance(candidate_sources, Sequence):
        raise DramaturgContractError("published source basis is invalid")
    host, first_basis = _runtime_host_basis(host)
    manifest_before, player_before, _player_before_record = _current_player_owner(
        host, first_basis, plan.player_id
    )
    current = _read_horizon_owner(
        host,
        first_basis,
        plan.path,
        scope_kind=str(candidate_record["scope"]["kind"]),  # type: ignore[index]
        player_id=plan.player_id
        if candidate_record["scope"]["kind"] == "PLAYER_LOCAL"  # type: ignore[index]
        else None,
    )
    if current is None or _canonical_json(current) != _canonical_json(candidate_record):
        raise DramaturgContractError(
            "published generation is not the exact current route record"
        )
    shared = _bound_shared_horizon(host, first_basis, candidate_record)
    source_union = list(candidate_sources)
    if shared is not None:
        shared_sources = shared["source_basis"]
        if not isinstance(shared_sources, Sequence):
            raise DramaturgContractError("BOUND shared source basis is invalid")
        source_union.extend(shared_sources)
    source_basis = _source_basis(source_union)
    context_sources, context_player = _context_resolve_sources(
        host, plan.player_id, source_basis
    )
    host, current_basis = _runtime_host_basis(host)
    manifest_after, player_after, player_record_after = _current_player_owner(
        host, current_basis, plan.player_id
    )
    if manifest_before != manifest_after or player_before != player_after:
        raise DramaturgContractError(
            "current mode or PLAYER changed before generation promotion"
        )
    confirmed_record = _read_horizon_owner(
        host,
        current_basis,
        plan.path,
        scope_kind=str(candidate_record["scope"]["kind"]),  # type: ignore[index]
        player_id=plan.player_id
        if candidate_record["scope"]["kind"] == "PLAYER_LOCAL"  # type: ignore[index]
        else None,
    )
    if confirmed_record is None or _canonical_json(confirmed_record) != _canonical_json(
        candidate_record
    ):
        raise DramaturgContractError(
            "published horizon changed before generation promotion"
        )
    if shared is not None:
        shared_after = _bound_shared_horizon(host, current_basis, confirmed_record)
        if shared_after is None or _canonical_json(shared_after) != _canonical_json(
            shared
        ):
            raise DramaturgContractError(
                "BOUND shared generation changed before promotion"
            )
    scope = candidate_record["scope"]
    if not isinstance(scope, Mapping):
        raise DramaturgContractError("published horizon scope is invalid")
    _validate_sources_at_basis(
        host,
        current_basis,
        source_basis,
        context_sources,
        context_player,
        player_record_after,
        scope=scope,
    )
    return confirmed_record


def publish_dramaturg_horizon(
    host: object,
    preparation: DramaturgPreparation,
    *,
    size_review_outcome: object | None = None,
) -> DramaturgPublicationResult:
    """Publish one fixed-route delta through the existing RuntimeHost/W02 service."""

    if (
        not isinstance(preparation, DramaturgPreparation)
        or preparation.status != "READY"
    ):
        raise DramaturgContractError(
            "a ready multiplayer Dramaturg preparation is required"
        )
    plan = preparation._plan
    if not isinstance(plan, _PreparedDramaturgPublication):
        raise DramaturgContractError("publication plan is not Dramaturg-owner issued")
    host, _basis = _runtime_host_basis(host)
    if plan.host_token is not getattr(host, "_basis_token", None):
        raise DramaturgContractError(
            "Dramaturg publication plan belongs to another host"
        )
    try:
        from .durability import route_serialized_operation
        from .publication import PublicationOutcome, PublicationStatus
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError("W02 publication owner is unavailable") from exc
    record = validate_dramaturg_horizon(json.loads(plan.record_json))
    player_payload = json.loads(plan.player_json)
    if not isinstance(player_payload, dict):
        raise DramaturgContractError("prepared PLAYER publication anchor is invalid")
    routed_operation = route_serialized_operation(
        "world.player", plan.player_id, player_payload
    )
    owner_generations = {plan.path: int(record["generation"])}
    path_operations: dict[str, object | None] = {
        routed_operation.relative_path: player_payload,
        plan.path: record,
    }
    publication_service = getattr(host, "publication", None)
    measure_path_operations = getattr(
        publication_service, "measure_path_operations", None
    )
    if not callable(measure_path_operations):
        raise DramaturgContractError(
            "exact W02 path-size measurement capability is unavailable"
        )
    try:
        raw_sizes = measure_path_operations(path_operations)
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError(
            "exact W02 path-size measurement failed closed"
        ) from exc
    if not isinstance(raw_sizes, Mapping) or set(raw_sizes) != set(path_operations):
        raise DramaturgContractError(
            "W02 path-size result does not bind the complete operation set"
        )
    measured_sizes: dict[str, int] = {}
    for path, measured_size in raw_sizes.items():
        if (
            not isinstance(path, str)
            or type(measured_size) is not int
            or measured_size < 0
        ):
            raise DramaturgContractError(
                "W02 path sizes are not exact non-negative bytes"
            )
        measured_sizes[path] = measured_size
    horizon_size = measured_sizes.get(plan.path)
    if type(horizon_size) is not int:
        raise DramaturgContractError("W02 did not measure the fixed Dramaturg path")
    size_band = _dramaturg_size_band(horizon_size)
    immutable_sizes = MappingProxyType(dict(measured_sizes))
    if size_band != "PREFERRED_TARGET":
        if size_review_outcome is None:
            return DramaturgPublicationResult(
                "SIZE_REVIEW_REQUIRED",
                None,
                None,
                preparation,
                immutable_sizes,
                size_band,
                _DRAMATURG_SIZE_REVIEW_ISSUER,
            )
        review = _validate_dramaturg_size_review_outcome(
            size_review_outcome,
            plan=plan,
            size_bytes=horizon_size,
        )
        if review.decision == "REPREPARE":
            return DramaturgPublicationResult(
                "REPREPARE_REQUIRED",
                None,
                None,
                preparation,
                immutable_sizes,
                size_band,
            )
    elif size_review_outcome is not None:
        raise DramaturgContractError(
            "size-review outcome is not applicable to a preferred-target candidate"
        )

    publish_owner_delta = getattr(publication_service, "publish_owner_delta", None)
    if not callable(publish_owner_delta):
        raise DramaturgContractError("RuntimeHost campaign publication is unavailable")
    try:
        outcome = publish_owner_delta(
            routed_operation=routed_operation,
            path_operations=path_operations,
            owner_generations=owner_generations,
            publication_reason="dramaturg-horizon",
            basis=plan.basis,
        )
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise DramaturgContractError("W02 Dramaturg publication failed closed") from exc
    if not isinstance(outcome, PublicationOutcome):
        raise DramaturgContractError("RuntimeHost returned an untyped W02 outcome")
    if outcome.status is not PublicationStatus.ACCEPTED:
        return DramaturgPublicationResult(
            "NOT_PUBLISHED",
            None,
            outcome,
            preparation,
            immutable_sizes,
            size_band,
        )
    try:
        promoted = promote_accepted_dramaturg_generation(host, preparation, outcome)
    except DramaturgContractError:
        return DramaturgPublicationResult(
            "PUBLISHED_NOT_RETAINABLE",
            None,
            outcome,
            preparation,
            immutable_sizes,
            size_band,
        )
    return DramaturgPublicationResult(
        "PUBLISHED",
        int(promoted["generation"]),
        outcome,
        preparation,
        immutable_sizes,
        size_band,
    )


def _project_dramaturg_horizon(
    host: object, *, scope_kind: str, player_id: object
) -> dict[str, object]:
    host, basis = _runtime_host_basis(host)
    campaign_id = _identifier(
        getattr(host, "campaign_id", None), "RuntimeHost campaign_id"
    )
    manifest = _exact_campaign_mapping(host, basis, "MANIFEST.yaml")
    if manifest.get("campaign_id") != campaign_id:
        raise DramaturgContractError("current MANIFEST belongs to another campaign")
    mode = manifest.get("mode")
    if mode == "singleplayer":
        return {"status": "INACTIVE_MODE", "horizon": None}
    if mode != "multiplayer":
        raise DramaturgContractError("current MANIFEST mode is unavailable or invalid")
    stable_player_id = _identifier(player_id, "current PLAYER nomination")
    try:
        manifest_before, player_before, _player_record = _current_player_owner(
            host, basis, stable_player_id
        )
    except DramaturgContractError:
        return {"status": "INACTIVE_PLAYER", "horizon": None}
    path = dramaturg_horizon_path(
        scope_kind,
        player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
    )
    try:
        horizon = _read_horizon_owner(
            host,
            basis,
            path,
            scope_kind=scope_kind,
            player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
        )
    except _CorruptDramaturgHorizonError:
        return {"status": "CORRUPT_OR_UNUSABLE", "horizon": None}
    if horizon is None:
        return {"status": "ABSENT", "horizon": None}
    sources = list(horizon["source_basis"])
    try:
        shared = _bound_shared_horizon(host, basis, horizon)
        if shared is not None:
            sources.extend(shared["source_basis"])
        source_basis = _source_basis(sources)
        context_sources, context_player = _context_resolve_sources(
            host, stable_player_id, source_basis
        )
        host, current_basis = _runtime_host_basis(host)
        manifest_after, player_after, current_player = _current_player_owner(
            host, current_basis, stable_player_id
        )
        if manifest_before != manifest_after or player_before != player_after:
            raise DramaturgContractError(
                "current MANIFEST or PLAYER changed during admission"
            )
        current = _read_horizon_owner(
            host,
            current_basis,
            path,
            scope_kind=scope_kind,
            player_id=stable_player_id if scope_kind == "PLAYER_LOCAL" else None,
        )
        if current is None or _canonical_json(current) != _canonical_json(horizon):
            raise DramaturgContractError(
                "affected retained horizon changed during admission"
            )
        if shared is not None:
            shared_after = _bound_shared_horizon(host, current_basis, current)
            if shared_after is None or _canonical_json(shared_after) != _canonical_json(
                shared
            ):
                raise DramaturgContractError(
                    "BOUND shared generation changed during admission"
                )
        scope = horizon["scope"]
        if not isinstance(scope, Mapping):
            raise DramaturgContractError("retained horizon scope is invalid")
        _validate_sources_at_basis(
            host,
            current_basis,
            source_basis,
            context_sources,
            context_player,
            current_player,
            scope=scope,
        )
    except _CorruptDramaturgHorizonError:
        return {"status": "CORRUPT_OR_UNUSABLE", "horizon": None}
    except DramaturgContractError:
        return {"status": "STALE_OR_INCOMPATIBLE", "horizon": None}
    return {"status": "CURRENT_COMPATIBLE", "horizon": deepcopy(horizon)}


def project_shared_dramaturg_horizon(
    host: object, *, player_id: object
) -> dict[str, object]:
    """Resolve only the fixed shared route under current multiplayer owner evidence."""

    return _project_dramaturg_horizon(host, scope_kind="SHARED", player_id=player_id)


def project_player_dramaturg_horizon(
    host: object, *, player_id: object
) -> dict[str, object]:
    """Resolve only the nominated stable PLAYER route after current eligibility."""

    return _project_dramaturg_horizon(
        host, scope_kind="PLAYER_LOCAL", player_id=player_id
    )


def classify_dramaturg_admission(
    host: object, *, scope_kind: str, player_id: object
) -> str:
    """Return current owner-derived status without trusting caller mode flags."""

    result = _project_dramaturg_horizon(
        host, scope_kind=scope_kind, player_id=player_id
    )
    return str(result["status"])


def admit_dramaturg_horizon(
    host: object, *, scope_kind: str, player_id: object
) -> dict[str, object]:
    """Return retained planning only after exact current-owner admission."""

    result = _project_dramaturg_horizon(
        host, scope_kind=scope_kind, player_id=player_id
    )
    horizon = result.get("horizon")
    if result.get("status") != "CURRENT_COMPATIBLE" or not isinstance(horizon, Mapping):
        raise DramaturgContractError(
            "retained Dramaturg horizon is not current and compatible"
        )
    return deepcopy(dict(horizon))


def rebase_dramaturg_horizon(
    host: object, *, scope_kind: str, player_id: object
) -> dict[str, object]:
    """Reread/revalidate the exact route; incompatible text is discarded, never merged."""

    return admit_dramaturg_horizon(host, scope_kind=scope_kind, player_id=player_id)


def invalidate_dramaturg_horizon(
    host: object, *, scope_kind: str, player_id: object
) -> dict[str, object]:
    """Derive owner-local usability without deleting bytes or restoring planning."""

    return _project_dramaturg_horizon(host, scope_kind=scope_kind, player_id=player_id)


def reconcile_dramaturg_publication(
    host: object,
    preparation: DramaturgPreparation,
    result: DramaturgPublicationResult,
) -> DramaturgPreparation | None:
    """Reprepare only when the exact affected horizon generation did not move.

    A changed planning generation is never text-merged or overwritten. A returned
    preparation is a new unretained candidate; this function performs no write.
    """

    if (
        not isinstance(preparation, DramaturgPreparation)
        or not isinstance(result, DramaturgPublicationResult)
        or result.preparation is not preparation
        or result.status != "NOT_PUBLISHED"
    ):
        return None
    plan = preparation._plan
    if not isinstance(plan, _PreparedDramaturgPublication):
        return None
    try:
        from .publication import PublicationOutcome, PublicationStatus
    except ImportError as exc:  # pragma: no cover - package wiring failure.
        raise DramaturgContractError("W02 publication owner is unavailable") from exc
    if (
        not isinstance(result.outcome, PublicationOutcome)
        or result.outcome.status is PublicationStatus.ACCEPTED
    ):
        return None
    record = validate_dramaturg_horizon(json.loads(plan.record_json))
    scope = record["scope"]
    if not isinstance(scope, Mapping):
        return None
    scope_kind = str(scope.get("kind"))
    current_view = _project_dramaturg_horizon(
        host, scope_kind=scope_kind, player_id=plan.player_id
    )
    if current_view.get("status") == "ABSENT":
        current_horizon = None
    elif current_view.get("status") == "CURRENT_COMPATIBLE":
        value = current_view.get("horizon")
        if not isinstance(value, Mapping):
            return None
        current_horizon = dict(value)
    else:
        return None
    if (
        None if current_horizon is None else int(current_horizon["generation"])
    ) != plan.base_generation or (
        None if current_horizon is None else _canonical_json(current_horizon)
    ) != plan.base_record_json:
        return None
    candidate = json.loads(plan.candidate_json)
    return prepare_dramaturg_publication(
        host,
        candidate,
        player_id=plan.player_id,
    )


def validate_dramaturg_horizon(value: object) -> dict[str, object]:
    """Validate noncanonical planning and exact retained-family identity."""

    if not isinstance(value, Mapping):
        raise DramaturgContractError("Dramaturg horizon must be an object")
    required = {
        "schema_version",
        "scope_id",
        "scope",
        "generation",
        "source_basis",
        "entries",
    }
    scope = _scope(value.get("scope"))
    expected = required | (
        {"shared_basis"} if scope["kind"] == "PLAYER_LOCAL" else set()
    )
    if set(value) != expected:
        raise DramaturgContractError(
            "Dramaturg horizon has unsupported or missing fields"
        )
    version = value["schema_version"]
    generation = value["generation"]
    if isinstance(version, bool) or not isinstance(version, int) or version != 2:
        raise DramaturgContractError("unsupported Dramaturg horizon schema_version")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
        raise DramaturgContractError("generation must be a positive integer")
    scope_id = _identifier(value["scope_id"], "scope_id")
    entries = _entries(value["entries"])
    source_basis = _source_basis(value["source_basis"])
    if source_basis != _entry_source_union(entries):
        raise DramaturgContractError(
            "horizon source_basis must equal its entry-local bases"
        )
    normalized: dict[str, object] = {
        "schema_version": version,
        "scope_id": scope_id,
        "scope": scope,
        "generation": generation,
        "source_basis": source_basis,
        "entries": entries,
    }
    if scope["kind"] == "PLAYER_LOCAL":
        normalized["shared_basis"] = _shared_basis(
            value["shared_basis"], scope_id=scope_id
        )
    return normalized
