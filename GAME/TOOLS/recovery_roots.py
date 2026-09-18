"""Owner-derived operational-root enrollment evidence.

Operational roots are a bounded routing projection.  This module deliberately
does not store lifecycle state and never treats a root carrier, index, or page
as proof that an owner is active.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Final, Protocol
import weakref

from .live_state import validate_accepted_absorption_evidence
from .native_storage import route_native_record


# framework_module_version: 1.0.8
FRAMEWORK_MODULE_VERSION: Final = "1.0.8"
OPERATIONAL_ROOT_SCHEMA_VERSION: Final = 1
OPERATIONAL_ROOT_HANDOFF_SCHEMA_VERSION: Final = 1
_OWNER_KINDS: Final = frozenset(
    {
        "runtime.command",
        "runtime.procedure",
        "runtime.interaction",
        "runtime.intent_plan",
    }
)
_PROMISED_OWNER_KINDS: Final = frozenset({"runtime.interaction", "runtime.intent_plan"})
_ACTIONS: Final = frozenset({"ENROLL", "REMOVE", "NOOP"})
_LIFECYCLES: Final = frozenset({"ACTIVE", "TERMINAL"})
_PROCEDURE_SCHEMA_VERSION: Final = 2
_SOURCE_REVISION = re.compile(r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$")
_HANDOFF_SCOPES: Final = frozenset({"CAMPAIGN", "LIVE"})


class OperationalRootError(ValueError):
    """Raised when native-root evidence is malformed or inconsistent."""


class OperationalRootCompletenessError(OperationalRootError):
    """Raised when a root page was not built from a complete native set."""


@dataclass(frozen=True, slots=True)
class OperationalRoot:
    """A routing-only identity and its deterministic native route."""

    campaign_id: str
    owner_kind: str
    owner_id: str
    relative_path: str

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "root campaign_id")
        if self.owner_kind not in _OWNER_KINDS:
            raise OperationalRootError("root owner_kind is not an admitted operational owner")
        _nonempty(self.owner_id, "root owner_id")
        expected = route_native_record(self.owner_kind, (self.owner_id,)).relative_path
        if self.relative_path != expected:
            raise OperationalRootError("root route does not match exact native owner identity")

    @property
    def key(self) -> tuple[str, str, str]:
        return self.campaign_id, self.owner_kind, self.owner_id

    def to_dict(self) -> dict[str, object]:
        return {
            "owner_kind": self.owner_kind,
            "owner_id": self.owner_id,
            "route": {
                "family_key": self.owner_kind,
                "identity": [self.owner_id],
                "relative_path": self.relative_path,
            },
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class OperationalRootDelta:
    """A derivative membership change prepared from one native owner."""

    campaign_id: str
    action: str
    root: OperationalRoot
    reason: str
    owner_state_fingerprint: str = ""

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "delta campaign_id")
        if self.action not in _ACTIONS:
            raise OperationalRootError("operational-root delta action is not registered")
        if self.root.campaign_id != self.campaign_id:
            raise OperationalRootError("delta root campaign differs from delta campaign")
        _nonempty(self.reason, "delta reason")
        if self.owner_state_fingerprint and (
            len(self.owner_state_fingerprint) != 64
            or any(char not in "0123456789abcdef" for char in self.owner_state_fingerprint)
        ):
            raise OperationalRootError("delta owner state evidence must be a SHA-256 fingerprint")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": OPERATIONAL_ROOT_SCHEMA_VERSION,
            "campaign_id": self.campaign_id,
            "action": self.action,
            "root": self.root.to_dict(),
            "reason": self.reason,
            "owner_state_fingerprint": self.owner_state_fingerprint,
        }


_OWNER_ISSUED_ROOT_DELTAS: dict[int, weakref.ReferenceType[OperationalRootDelta]] = {}


def _mark_owner_issued_root_delta(delta: OperationalRootDelta) -> OperationalRootDelta:
    delta_id = id(delta)

    def remove(reference: weakref.ReferenceType[OperationalRootDelta]) -> None:
        if _OWNER_ISSUED_ROOT_DELTAS.get(delta_id) is reference:
            _OWNER_ISSUED_ROOT_DELTAS.pop(delta_id, None)

    _OWNER_ISSUED_ROOT_DELTAS[delta_id] = weakref.ref(delta, remove)
    return delta


def _is_owner_issued_root_delta(delta: OperationalRootDelta) -> bool:
    reference = _OWNER_ISSUED_ROOT_DELTAS.get(id(delta))
    return reference is not None and reference() is delta


@dataclass(frozen=True, slots=True)
class OperationalRootPage:
    """A complete, bounded routing page derived from native owners."""

    campaign_id: str
    roots: tuple[OperationalRoot, ...]
    complete: bool

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "page campaign_id")
        if not self.complete:
            raise OperationalRootCompletenessError("operational-root page is incomplete")
        seen: set[tuple[str, str, str]] = set()
        for root in self.roots:
            if root.campaign_id != self.campaign_id:
                raise OperationalRootError("page root campaign differs from page campaign")
            if root.key in seen:
                raise OperationalRootError("operational-root page contains duplicate owner identity")
            seen.add(root.key)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": OPERATIONAL_ROOT_SCHEMA_VERSION,
            "campaign_id": self.campaign_id,
            "complete": self.complete,
            "roots": [root.to_dict() for root in self.roots],
        }


@dataclass(frozen=True, slots=True)
class OperationalRootHandoff:
    """Ephemeral root-routing evidence pinned to one exact source."""

    campaign_id: str
    source_scope: str
    source_revision: str
    roots: tuple[OperationalRoot, ...]
    source_key: tuple[str, str, str] | None = None
    source_lifecycle: str = "ACTIVE"
    complete: bool = True

    def __post_init__(self) -> None:
        campaign_id = _nonempty(self.campaign_id, "handoff campaign_id")
        scope = _handoff_scope(self.source_scope)
        revision = _source_revision(self.source_revision)
        if self.complete is not True:
            raise OperationalRootCompletenessError("operational-root handoff is incomplete")
        source_key = _handoff_source_key(self.source_key, campaign_id, scope)
        if self.source_lifecycle not in {"ACTIVE", "CLOSED", "CLOSED_UNABSORBED", "ABSORBED"}:
            raise OperationalRootError("operational-root handoff lifecycle is unsupported")
        roots = tuple(self.roots)
        seen: set[tuple[str, str, str]] = set()
        for root in roots:
            if not isinstance(root, OperationalRoot):
                raise OperationalRootError("operational-root handoff roots must be typed")
            if root.campaign_id != campaign_id:
                raise OperationalRootError("handoff root campaign differs from handoff campaign")
            if root.key in seen:
                raise OperationalRootError("operational-root handoff contains duplicate owner identity")
            seen.add(root.key)
        object.__setattr__(self, "campaign_id", campaign_id)
        object.__setattr__(self, "source_scope", scope)
        object.__setattr__(self, "source_revision", revision)
        object.__setattr__(self, "source_key", source_key)
        object.__setattr__(self, "roots", roots)

    def to_page(self) -> OperationalRootPage:
        return OperationalRootPage(self.campaign_id, self.roots, complete=True)

    def to_dict(self) -> dict[str, object]:
        """Return handoff evidence without claiming it is the persistent page schema."""

        return {
            "schema_version": OPERATIONAL_ROOT_HANDOFF_SCHEMA_VERSION,
            "kind": "runtime.operational_root_handoff",
            "campaign_id": self.campaign_id,
            "source_scope": self.source_scope,
            "source_revision": self.source_revision,
            "source_key": list(self.source_key) if self.source_key is not None else None,
            "source_lifecycle": self.source_lifecycle,
            "complete": True,
            "roots": [root.to_dict() for root in self.roots],
            "ephemeral": True,
        }

    @classmethod
    def from_mapping(cls, value: object) -> "OperationalRootHandoff":
        if not isinstance(value, Mapping):
            raise OperationalRootError("operational-root handoff must be an object")
        expected = {
            "schema_version",
            "kind",
            "campaign_id",
            "source_scope",
            "source_revision",
            "source_key",
            "source_lifecycle",
            "complete",
            "roots",
            "ephemeral",
        }
        if set(value) != expected:
            raise OperationalRootError("operational-root handoff fields are not strict")
        if (
            value["schema_version"] != OPERATIONAL_ROOT_HANDOFF_SCHEMA_VERSION
            or value["kind"] != "runtime.operational_root_handoff"
            or value["ephemeral"] is not True
        ):
            raise OperationalRootError("unsupported operational-root handoff")
        raw_roots = value["roots"]
        if not isinstance(raw_roots, Sequence) or isinstance(raw_roots, (str, bytes)):
            raise OperationalRootError("operational-root handoff roots must be an array")
        campaign_id = value["campaign_id"]
        if not isinstance(campaign_id, str):
            raise OperationalRootError("operational-root handoff campaign is malformed")
        return cls(
            campaign_id=campaign_id,
            source_scope=value["source_scope"],  # type: ignore[arg-type]
            source_revision=value["source_revision"],  # type: ignore[arg-type]
            source_key=value["source_key"],  # type: ignore[arg-type]
            source_lifecycle=value["source_lifecycle"],  # type: ignore[arg-type]
            complete=value["complete"],  # type: ignore[arg-type]
            roots=tuple(_root_from_mapping(raw, campaign_id) for raw in raw_roots),
        )


class AcceptedUnresolvedInputPromise(Protocol):
    """Later-owner promise boundary interface reserved for the later owner.

    W02.T04 defines the typed input/derivation port but has no authorized
    durability/handoff issuer.  Until that later owner supplies its boundary,
    every unresolved-input candidate fails closed.
    """

    def validate(
        self,
        *,
        campaign_id: str,
        owner_kind: str,
        owner_id: str,
        native_owner: Mapping[str, object],
    ) -> bool:
        """Return exactly ``True`` only for matching owner-validated evidence."""


def derive_operational_root_delta(
    campaign_id: str,
    owner_kind: str,
    native_owner: Mapping[str, object],
    existing_roots: Iterable[OperationalRoot | Mapping[str, object]] = (),
    accepted_promise: AcceptedUnresolvedInputPromise | None = None,
) -> OperationalRootDelta:
    """Derive one idempotent membership delta from validated native owner state.

    ``existing_roots`` is only the prior routing membership projection.  It is
    never consulted to decide owner lifecycle or eligibility.
    """

    _nonempty(campaign_id, "campaign_id")
    if owner_kind in _PROMISED_OWNER_KINDS:
        identity, eligible, reason = _validate_promised_input(
            campaign_id, owner_kind, native_owner, accepted_promise
        )
    else:
        identity, eligible, reason = _validate_native_owner(owner_kind, native_owner)
    root = OperationalRoot(
        campaign_id=campaign_id,
        owner_kind=owner_kind,
        owner_id=identity,
        relative_path=route_native_record(owner_kind, (identity,)).relative_path,
    )
    current = _normalize_existing_roots(campaign_id, existing_roots)
    present = root.key in current
    if eligible and not present:
        action = "ENROLL"
    elif eligible:
        action = "NOOP"
    elif present:
        action = "REMOVE"
    else:
        action = "NOOP"
    return _mark_owner_issued_root_delta(OperationalRootDelta(
        campaign_id,
        action,
        root,
        reason,
        _native_state_fingerprint(native_owner),
    ))


def validate_operational_root_delta(
    delta: OperationalRootDelta,
    native_owner: Mapping[str, object],
    accepted_promise: AcceptedUnresolvedInputPromise | None = None,
) -> None:
    """Validate a derivative delta against the exact current native owner."""

    if not isinstance(delta, OperationalRootDelta):
        raise OperationalRootError("operational-root delta must be owner-derived typed evidence")
    if delta.root.owner_kind in _PROMISED_OWNER_KINDS:
        identity, eligible, _reason = _validate_promised_input(
            delta.campaign_id, delta.root.owner_kind, native_owner, accepted_promise
        )
    else:
        identity, eligible, _reason = _validate_native_owner(delta.root.owner_kind, native_owner)
    if identity != delta.root.owner_id:
        raise OperationalRootError("delta owner identity differs from native owner identity")
    expected_path = route_native_record(delta.root.owner_kind, (identity,)).relative_path
    if delta.root.relative_path != expected_path:
        raise OperationalRootError("delta route differs from native owner identity")
    if delta.action == "ENROLL" and not eligible:
        raise OperationalRootError("enrollment delta is not eligible from native owner state")
    if delta.action == "REMOVE" and eligible:
        raise OperationalRootError("removal delta is not eligible from native owner state")
    if delta.owner_state_fingerprint != _native_state_fingerprint(native_owner):
        raise OperationalRootError("delta lacks matching native owner state evidence")


def _handoff_scope(value: object) -> str:
    if not isinstance(value, str) or value.upper() not in _HANDOFF_SCOPES:
        raise OperationalRootError("operational-root handoff source scope is unsupported")
    return value.upper()


def _source_revision(value: object) -> str:
    if not isinstance(value, str) or _SOURCE_REVISION.fullmatch(value) is None:
        raise OperationalRootError("operational-root handoff source revision is not exact")
    return value


def _handoff_source_key(
    value: object,
    campaign_id: str,
    scope: str,
) -> tuple[str, str, str] | None:
    if scope == "CAMPAIGN":
        if value is not None:
            raise OperationalRootError("campaign operational roots cannot carry a LIVE source key")
        return None
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise OperationalRootError("LIVE operational roots require an exact source key")
    key = tuple(_nonempty(item, "operational-root source key") for item in value)
    if key[0] != campaign_id:
        raise OperationalRootError("operational-root source key belongs to another campaign")
    return key  # type: ignore[return-value]


def _owner_key(value: object, campaign_id: str, label: str) -> tuple[str, str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise OperationalRootError(f"{label} identity is malformed")
    if len(value) == 2:
        kind, owner_id = value
    elif len(value) == 3:
        source_campaign, kind, owner_id = value
        if source_campaign != campaign_id:
            raise OperationalRootError(f"{label} belongs to another campaign")
    else:
        raise OperationalRootError(f"{label} identity is malformed")
    return _nonempty(kind, f"{label} owner kind"), _nonempty(owner_id, f"{label} owner ID")


def _coerce_handoff(
    value: OperationalRootHandoff | OperationalRootPage | Mapping[str, object],
    *,
    campaign_id: str,
    source_scope: str,
    source_revision: str,
    source_key: Sequence[str] | None,
    source_lifecycle: str,
) -> OperationalRootHandoff:
    if isinstance(value, OperationalRootHandoff):
        handoff = value
    elif isinstance(value, OperationalRootPage):
        handoff = OperationalRootHandoff(
            campaign_id=value.campaign_id,
            source_scope=source_scope,
            source_revision=source_revision,
            source_key=source_key,
            source_lifecycle=source_lifecycle or "ACTIVE",
            roots=value.roots,
            complete=value.complete,
        )
    elif isinstance(value, Mapping):
        handoff = OperationalRootHandoff.from_mapping(value)
    else:
        raise OperationalRootError("operational-root handoff must be typed evidence")
    if handoff.campaign_id != campaign_id:
        raise OperationalRootError("operational-root handoff belongs to another campaign")
    return handoff


def _validate_terminal_roots(
    handoff: OperationalRootHandoff,
    terminal_owner_keys: Sequence[tuple[str, str] | tuple[str, str, str]],
    terminal_native_owners: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None,
) -> set[tuple[str, str, str]]:
    requested = {
        _owner_key(raw_key, handoff.campaign_id, "terminal root")
        for raw_key in terminal_owner_keys
    }
    root_map = {(root.owner_kind, root.owner_id): root for root in handoff.roots}
    if not requested.issubset(root_map):
        raise OperationalRootError("terminal root identity is not in the exact handoff page")
    if requested and terminal_native_owners is None:
        raise OperationalRootError("terminal roots require native owner evidence")
    for key in requested:
        owner = None
        if terminal_native_owners is not None:
            owner = terminal_native_owners.get(key)
            if owner is None:
                owner = terminal_native_owners.get((handoff.campaign_id, *key))
        if not isinstance(owner, OperationalRootDelta) or not _is_owner_issued_root_delta(owner):
            raise OperationalRootError("terminal roots require owner-issued native removal proof")
        if owner.campaign_id != handoff.campaign_id or owner.root != root_map[key]:
            raise OperationalRootError("terminal root proof is not bound to the exact root")
        if owner.action != "REMOVE":
            raise OperationalRootError("terminal root owner proof is not a removal delta")
    return {(kind, owner_id, root_map[(kind, owner_id)].relative_path) for kind, owner_id in requested}


def reconcile_operational_root_handoff(
    page: OperationalRootHandoff | OperationalRootPage | Mapping[str, object],
    *,
    campaign_id: str,
    expected_source_scope: str,
    expected_source_revision: str,
    target_source_scope: str,
    target_source_revision: str,
    expected_source_key: Sequence[str] | None = None,
    target_source_key: Sequence[str] | None = None,
    source_lifecycle: str | None = None,
    absorption_acknowledged: bool | None = None,
    absorption_evidence: object | None = None,
    terminal_owner_keys: Sequence[tuple[str, str] | tuple[str, str, str]] = (),
    terminal_native_owners: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None = None,
    superseded_owner_keys: Sequence[tuple[str, str] | tuple[str, str, str]] = (),
    superseded_native_deltas: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None = None,
) -> OperationalRootHandoff:
    """Move root references without moving native owner state or authority."""

    current = _coerce_handoff(
        page,
        campaign_id=campaign_id,
        source_scope=expected_source_scope,
        source_revision=expected_source_revision,
        source_key=expected_source_key,
        source_lifecycle=source_lifecycle,
    )
    expected_scope = _handoff_scope(expected_source_scope)
    target_scope = _handoff_scope(target_source_scope)
    target_revision = _source_revision(target_source_revision)
    target_key = _handoff_source_key(target_source_key, campaign_id, target_scope)
    expected_revision = _source_revision(expected_source_revision)
    expected_key = _handoff_source_key(expected_source_key, campaign_id, expected_scope)
    if (
        current.source_scope == target_scope
        and current.source_revision == target_revision
        and current.source_key == target_key
    ):
        if terminal_owner_keys or superseded_owner_keys:
            raise OperationalRootError("idempotent operational-root retry cannot add a removal claim")
        if target_scope == "CAMPAIGN" and expected_scope == "LIVE":
            if source_lifecycle is not None or absorption_acknowledged is not None:
                raise OperationalRootError(
                    "campaign recovery requires owner-issued absorption evidence; "
                    "caller assertions are not accepted"
                )
            if absorption_evidence is None:
                raise OperationalRootError("campaign recovery requires owner-issued absorption evidence")
            try:
                validate_accepted_absorption_evidence(
                    absorption_evidence,
                    source_key=expected_key,  # type: ignore[arg-type]
                    source_revision=expected_revision,
                )
            except ValueError as exc:
                raise OperationalRootError("campaign recovery absorption evidence is not exact") from exc
            return current
        return current
    if current.source_scope != expected_scope or current.source_revision != expected_revision:
        raise OperationalRootError("operational-root handoff source scope or revision is stale")
    if current.source_key != expected_key:
        raise OperationalRootError("operational-root handoff source key is stale")
    if target_scope == "CAMPAIGN" and expected_scope == "LIVE":
        if source_lifecycle is not None:
            raise OperationalRootError(
                "campaign recovery requires owner-issued absorption evidence; "
                "caller lifecycle assertions are not accepted"
            )
        if absorption_acknowledged is not None:
            raise OperationalRootError("campaign recovery requires owner-issued absorption evidence")
        if absorption_evidence is None:
            raise OperationalRootError("campaign recovery requires owner-issued absorption evidence")
        try:
            validate_accepted_absorption_evidence(
                absorption_evidence,
                source_key=current.source_key,  # type: ignore[arg-type]
                source_revision=current.source_revision,
            )
        except ValueError as exc:
            raise OperationalRootError("campaign recovery absorption evidence is not exact") from exc
    elif target_scope == "LIVE" and expected_scope != "CAMPAIGN":
        raise OperationalRootError("LIVE root handoff must begin from campaign roots")
    terminal = _validate_terminal_roots(current, terminal_owner_keys, terminal_native_owners)
    superseded = {
        _owner_key(raw_key, campaign_id, "superseded root")
        for raw_key in superseded_owner_keys
    }
    root_keys = {(root.owner_kind, root.owner_id) for root in current.roots}
    if not superseded.issubset(root_keys):
        raise OperationalRootError("superseded root identity is not in the exact handoff page")
    _validate_superseded_roots(current, superseded, superseded_native_deltas)
    if superseded and not (
        expected_scope == "LIVE"
        and target_scope == "CAMPAIGN"
        and absorption_evidence is not None
    ):
        raise OperationalRootError("superseded roots require exact closed-source absorption")
    removed = {(kind, owner_id) for kind, owner_id, _path in terminal}
    removed.update(superseded)
    roots = tuple(root for root in current.roots if (root.owner_kind, root.owner_id) not in removed)
    return OperationalRootHandoff(
        campaign_id=campaign_id,
        source_scope=target_scope,
        source_revision=target_revision,
        source_key=target_key,
        source_lifecycle="ACTIVE" if target_scope == "LIVE" else "ABSORBED",
        roots=roots,
        complete=True,
    )


def _validate_superseded_roots(
    handoff: OperationalRootHandoff,
    requested: set[tuple[str, str]],
    proofs: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None,
) -> None:
    if not requested:
        return
    if proofs is None:
        raise OperationalRootError("superseded roots require owner-issued replacement proof")
    root_map = {(root.owner_kind, root.owner_id): root for root in handoff.roots}
    for key in requested:
        proof = proofs.get(key)
        if proof is None:
            proof = proofs.get((handoff.campaign_id, *key))
        if not isinstance(proof, OperationalRootDelta) or not _is_owner_issued_root_delta(proof):
            raise OperationalRootError("superseded roots require owner-issued replacement proof")
        if proof.campaign_id != handoff.campaign_id or proof.root != root_map[key]:
            raise OperationalRootError("superseded root proof is not bound to the exact root")


def handoff_operational_roots_to_live(
    page: OperationalRootPage | OperationalRootHandoff | Mapping[str, object],
    *,
    campaign_id: str,
    campaign_revision: str,
    live_source_key: Sequence[str],
    live_source_revision: str,
) -> OperationalRootHandoff:
    """Route active campaign roots into one exact selected LIVE source."""

    return reconcile_operational_root_handoff(
        page,
        campaign_id=campaign_id,
        expected_source_scope="CAMPAIGN",
        expected_source_revision=campaign_revision,
        target_source_scope="LIVE",
        target_source_revision=live_source_revision,
        target_source_key=live_source_key,
    )


def recover_operational_roots_to_campaign(
    page: OperationalRootHandoff | Mapping[str, object],
    *,
    campaign_id: str,
    live_source_key: Sequence[str],
    live_source_revision: str,
    campaign_revision: str,
    source_lifecycle: str | None = None,
    absorption_acknowledged: bool | None = None,
    absorption_evidence: object | None = None,
    terminal_owner_keys: Sequence[tuple[str, str] | tuple[str, str, str]] = (),
    terminal_native_owners: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None = None,
    superseded_owner_keys: Sequence[tuple[str, str] | tuple[str, str, str]] = (),
    superseded_native_deltas: Mapping[
        tuple[str, str] | tuple[str, str, str], OperationalRootDelta
    ]
    | None = None,
) -> OperationalRootHandoff:
    """Return live roots to campaign recovery only after exact absorption."""

    return reconcile_operational_root_handoff(
        page,
        campaign_id=campaign_id,
        expected_source_scope="LIVE",
        expected_source_revision=live_source_revision,
        expected_source_key=live_source_key,
        target_source_scope="CAMPAIGN",
        target_source_revision=campaign_revision,
        source_lifecycle=source_lifecycle,
        absorption_acknowledged=absorption_acknowledged,
        absorption_evidence=absorption_evidence,
        terminal_owner_keys=terminal_owner_keys,
        terminal_native_owners=terminal_native_owners,
        superseded_owner_keys=superseded_owner_keys,
        superseded_native_deltas=superseded_native_deltas,
    )


def enumerate_operational_root_page(
    campaign_id: str,
    native_owners: Iterable[
        Mapping[str, object]
        | tuple[str, Mapping[str, object]]
        | tuple[str, Mapping[str, object], AcceptedUnresolvedInputPromise]
    ]
    | None,
    *,
    complete: bool = True,
) -> OperationalRootPage:
    """Build a page from an explicit complete native-owner enumeration.

    Directory scans, indexes, checkpoints, and callables are intentionally not
    accepted as a fallback source for current root membership.
    """

    if native_owners is None or callable(native_owners):
        raise OperationalRootError("operational roots require explicit native owners; scan fallback is forbidden")
    if not complete:
        raise OperationalRootCompletenessError("native operational-root enumeration is incomplete")
    if isinstance(native_owners, Mapping) or isinstance(native_owners, (str, bytes)):
        raise OperationalRootError("native operational owners must be an explicit iterable")
    roots: dict[tuple[str, str, str], OperationalRoot] = {}
    for item in native_owners:
        owner_kind, owner, promise = _owner_item(item)
        if owner_kind in _PROMISED_OWNER_KINDS:
            identity, eligible, _reason = _validate_promised_input(
                campaign_id, owner_kind, owner, promise
            )
        else:
            if promise is not None:
                raise OperationalRootError(
                    "promise evidence is only valid for unresolved input owners"
                )
            identity, eligible, _reason = _validate_native_owner(owner_kind, owner)
        if not eligible:
            continue
        root = OperationalRoot(
            campaign_id=campaign_id,
            owner_kind=owner_kind,
            owner_id=identity,
            relative_path=route_native_record(owner_kind, (identity,)).relative_path,
        )
        if root.key in roots:
            raise OperationalRootError("native operational-root enumeration contains duplicate owner identity")
        roots[root.key] = root
    return OperationalRootPage(
        campaign_id=campaign_id,
        roots=tuple(roots[key] for key in sorted(roots)),
        complete=True,
    )


def _validate_native_owner(owner_kind: str, owner: Mapping[str, object]) -> tuple[str, bool, str]:
    if owner_kind not in _OWNER_KINDS:
        raise OperationalRootError("native owner kind is not an admitted operational owner")
    if not isinstance(owner, Mapping) or isinstance(owner, OperationalRoot):
        raise OperationalRootError("operational-root evidence must be a native owner mapping")
    declared_kind = owner.get("kind")
    if declared_kind is not None and declared_kind != owner_kind:
        raise OperationalRootError("native owner kind differs from requested owner kind")
    if owner_kind in _PROMISED_OWNER_KINDS:
        raise OperationalRootError("unresolved input requires an accepted durability promise")
    if owner_kind == "runtime.procedure":
        owner_id = _nonempty(owner.get("id"), "native Procedure id")
        revision = owner.get("revision")
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            raise OperationalRootError("native Procedure revision is invalid")
        state = owner.get("state")
        if not isinstance(state, Mapping) or isinstance(state, OperationalRoot):
            raise OperationalRootError("native Procedure state is required")
        if state.get("schema_version") != _PROCEDURE_SCHEMA_VERSION:
            raise OperationalRootError("native Procedure schema_version is unsupported")
        if not isinstance(state.get("participant_resources"), Mapping):
            raise OperationalRootError("native Procedure resource state is required")
        lifecycle = state.get("lifecycle")
        if lifecycle not in _LIFECYCLES:
            raise OperationalRootError("native Procedure lifecycle must be ACTIVE or TERMINAL")
        if lifecycle == "TERMINAL":
            if state.get("lifecycle_state") != "terminated":
                raise OperationalRootError("terminal Procedure requires explicit terminal phase")
            return owner_id, False, "native_lifecycle_terminal"
        if state.get("lifecycle_state") == "terminated":
            raise OperationalRootError("ACTIVE Procedure cannot use terminal phase")
        return owner_id, True, "native_lifecycle_active"

    owner_id = _nonempty(owner.get("command_id"), "native RuntimeCommand id")
    disposition = owner.get("disposition")
    if disposition not in {"command.accepted", "command.settled"}:
        raise OperationalRootError("native RuntimeCommand disposition is not accepted or settled")
    pending = owner.get("pending_child_invocations")
    if not isinstance(pending, list):
        raise OperationalRootError("native RuntimeCommand mandatory closure is not typed")
    if disposition == "command.settled" and pending:
        raise OperationalRootError("settled RuntimeCommand retains mandatory closure")
    receipt = owner.get("direct_transition_receipt")
    publish_required = isinstance(receipt, Mapping) and receipt.get("status") == "PUBLISH_REQUIRED"
    unfinished = disposition == "command.accepted" or bool(pending) or publish_required
    if unfinished:
        return owner_id, True, "native_command_unfinished_closure"
    return owner_id, False, "native_command_settled"


def _validate_promised_input(
    campaign_id: str,
    owner_kind: str,
    native_owner: Mapping[str, object],
    promise: AcceptedUnresolvedInputPromise | None,
) -> tuple[str, bool, str]:
    try:
        owner_id = validate_unresolved_input_owner(campaign_id, owner_kind, native_owner)
    except OperationalRootError as exc:
        raise OperationalRootError(
            f"authorized durability/handoff promise boundary does not match native owner: {exc}"
        ) from exc
    if promise is None:
        raise OperationalRootError(
            "unresolved input enrollment is deferred until an authorized durability/handoff promise boundary"
        )
    try:
        from .durability import is_authorized_handoff_promise
    except ImportError as exc:  # pragma: no cover - package import is stable in runtime
        raise OperationalRootError("authorized durability/handoff boundary is unavailable") from exc
    if not is_authorized_handoff_promise(promise):
        raise OperationalRootError("unresolved input requires an authorized durability/handoff promise boundary")
    try:
        valid = promise.validate(
            campaign_id=campaign_id,
            owner_kind=owner_kind,
            owner_id=owner_id,
            native_owner=native_owner,
        )
    except (AttributeError, TypeError, ValueError) as exc:
        raise OperationalRootError("authorized durability/handoff promise evidence is invalid") from exc
    if valid is not True:
        raise OperationalRootError("authorized durability/handoff promise does not match native owner")
    return owner_id, True, "owner_issued_durability_handoff_promise"


def validate_unresolved_input_owner(
    campaign_id: str, owner_kind: str, native_owner: Mapping[str, object]
) -> str:
    """Validate one exact native unresolved-input owner before handoff issuance."""

    _nonempty(campaign_id, "campaign_id")
    if owner_kind not in _PROMISED_OWNER_KINDS:
        raise OperationalRootError("durability promise is only valid for unresolved input owners")
    if not isinstance(native_owner, Mapping):
        raise OperationalRootError("unresolved input owner must be a native mapping")
    if native_owner.get("kind") != owner_kind:
        raise OperationalRootError("native unresolved owner kind differs from requested owner kind")
    if native_owner.get("campaign_id") != campaign_id:
        raise OperationalRootError("native unresolved owner campaign differs from promise campaign")
    if owner_kind == "runtime.interaction":
        required = ("session_id", "player_id", "input_message_id", "intent_plan_id")
        for field in required:
            _nonempty(native_owner.get(field), f"interaction {field}")
        if native_owner.get("response_message_id") is not None:
            raise OperationalRootError("native interaction is resolved, not unresolved")
        return _nonempty(native_owner.get("input_message_id"), "interaction input_message_id")

    owner_id = _nonempty(
        native_owner.get("intent_plan_id", native_owner.get("id")), "intent plan id"
    )
    _nonempty(native_owner.get("interaction_id"), "intent plan interaction_id")
    clauses = native_owner.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        raise OperationalRootError("native intent plan clauses are required")
    if not any(
        isinstance(clause, Mapping)
        and clause.get("execution_state") in {"intent.pending", "intent.ready"}
        for clause in clauses
    ):
        raise OperationalRootError("native intent plan is resolved, not unresolved")
    return owner_id


def _owner_item(
    item: Mapping[str, object]
    | tuple[str, Mapping[str, object]]
    | tuple[str, Mapping[str, object], AcceptedUnresolvedInputPromise],
) -> tuple[str, Mapping[str, object], AcceptedUnresolvedInputPromise | None]:
    if isinstance(item, tuple) and len(item) == 2:
        owner_kind, owner = item
        if not isinstance(owner_kind, str) or not isinstance(owner, Mapping):
            raise OperationalRootError("native owner tuple is malformed")
        return owner_kind, owner, None
    if isinstance(item, tuple) and len(item) == 3:
        owner_kind, owner, promise = item
        if not isinstance(owner_kind, str) or not isinstance(owner, Mapping):
            raise OperationalRootError("native owner tuple is malformed")
        return owner_kind, owner, promise
    if isinstance(item, Mapping):
        owner_kind = item.get("kind")
        if not isinstance(owner_kind, str):
            raise OperationalRootError("native owner enumeration requires owner kind")
        return owner_kind, item, None
    raise OperationalRootError("native owner enumeration item is malformed")


def _normalize_existing_roots(
    campaign_id: str,
    roots: Iterable[OperationalRoot | Mapping[str, object]],
) -> set[tuple[str, str, str]]:
    if isinstance(roots, (str, bytes, Mapping)):
        raise OperationalRootError("existing roots must be an explicit iterable of routing carriers")
    result: set[tuple[str, str, str]] = set()
    for value in roots:
        root = value if isinstance(value, OperationalRoot) else _root_from_mapping(value, campaign_id)
        if root.campaign_id != campaign_id:
            raise OperationalRootError("existing root campaign differs from native owner campaign")
        if root.key in result:
            raise OperationalRootError("existing roots contain duplicate owner identity")
        result.add(root.key)
    return result


def _root_from_mapping(value: Mapping[str, object], campaign_id: str) -> OperationalRoot:
    if not isinstance(value, Mapping):
        raise OperationalRootError("existing root is not a routing carrier")
    route = value.get("route")
    if not isinstance(route, Mapping):
        raise OperationalRootError("existing root has no typed native route")
    owner_kind = value.get("owner_kind")
    owner_id = value.get("owner_id")
    relative_path = route.get("relative_path")
    if not isinstance(owner_kind, str) or not isinstance(owner_id, str) or not isinstance(relative_path, str):
        raise OperationalRootError("existing root identity is incomplete")
    if route.get("family_key") != owner_kind or route.get("identity") != [owner_id]:
        raise OperationalRootError("existing root route identity is inconsistent")
    return OperationalRoot(campaign_id, owner_kind, owner_id, relative_path)


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise OperationalRootError(f"{label} must be a nonempty string")
    return value


def _native_state_fingerprint(native_owner: Mapping[str, object]) -> str:
    try:
        encoded = json.dumps(
            dict(native_owner),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise OperationalRootError("native owner state is not canonical evidence") from exc
    return hashlib.sha256(encoded).hexdigest()
