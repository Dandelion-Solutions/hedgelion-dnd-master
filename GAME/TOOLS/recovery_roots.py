"""Owner-derived operational-root enrollment evidence.

Operational roots are a bounded routing projection.  This module deliberately
does not store lifecycle state and never treats a root carrier, index, or page
as proof that an owner is active.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import hashlib
import json
from typing import Final, Protocol

from .native_storage import route_native_record


# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final = "1.0.5"
OPERATIONAL_ROOT_SCHEMA_VERSION: Final = 1
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


@dataclass(frozen=True, slots=True)
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
    return OperationalRootDelta(
        campaign_id,
        action,
        root,
        reason,
        _native_state_fingerprint(native_owner),
    )


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
    if owner_kind not in _PROMISED_OWNER_KINDS:
        raise OperationalRootError("durability promise is only valid for unresolved input owners")
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
    if owner_kind == "runtime.interaction":
        owner_id = _nonempty(native_owner.get("input_message_id"), "interaction input_message_id")
    else:
        owner_id = _nonempty(
            native_owner.get("intent_plan_id", native_owner.get("id")), "intent plan id"
        )
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
