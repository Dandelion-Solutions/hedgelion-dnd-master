"""Campaign-bound runtime composition for the deterministic GAME engine.

The deployment host supplies the authenticated repository capability and the
selected-LIVE reader exactly once at this infrastructure boundary.  Gameplay
services receive only domain requests and candidate data; they never receive a
transport, repository, route resolver or replaceable sibling service.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, NoReturn, Protocol

from .live_state import LiveRouting, validate_live_route_completeness
from .policy_basis import PinnedCampaign, RepositoryPort

# framework_module_version: 1.0.3
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.3"

_REPOSITORY_OPERATIONS: Final[tuple[str, ...]] = (
    "pin_campaign",
    "read_exact_path",
    "read_exact_campaign_ref",
    "read_exact_commit",
    "compare_ancestry",
    "read_authenticated_commit_author",
)
_LIVE_OPERATION: Final[str] = "read_selected_live"
_NATIVE_ORDERING_ROUTE: Final[str] = "runtime_execution"


class SelectedLiveTransport(Protocol):
    """Selected-LIVE source reader supplied by the deployment host."""

    def read_selected_live(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> LiveRouting | None:
        """Return the exact selected route for the current campaign pin."""


class RuntimeHostError(ValueError):
    """Raised when a campaign-bound runtime operation cannot be admitted."""


class NativeOrderingStatus(StrEnum):
    """Bounded result when no native ordered owner is currently admitted."""

    NO_ORDERED_OWNER = "NO_ORDERED_OWNER"


@dataclass(frozen=True, slots=True)
class NativeOrderingResult:
    """Ephemeral result of the fixed native-ordering dispatch route."""

    status: NativeOrderingStatus
    campaign_id: str
    route: str = _NATIVE_ORDERING_ROUTE


@dataclass(frozen=True, slots=True)
class _OperationBasis:
    """Fresh source basis for one host operation."""

    pinned_campaign: PinnedCampaign
    selected_live: LiveRouting | None


def _require_nonempty_campaign_id(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeHostError("selected campaign identity is required")
    return value


def _require_operations(value: object, operations: tuple[str, ...], label: str) -> None:
    for operation in operations:
        if not callable(getattr(value, operation, None)):
            raise RuntimeHostError(f"{label} is missing required operation {operation}")


def _validate_pinned_campaign(
    value: object, expected_campaign_id: str
) -> PinnedCampaign:
    if not isinstance(value, PinnedCampaign):
        raise RuntimeHostError("repository did not return an owner-typed campaign pin")
    if value.campaign_id != expected_campaign_id:
        raise RuntimeHostError("repository pin belongs to another campaign")
    return value


def _validate_selected_live(
    value: object, expected_campaign_id: str
) -> LiveRouting | None:
    if value is None:
        return None
    if not isinstance(value, LiveRouting):
        raise RuntimeHostError(
            "selected-LIVE transport did not return an owner-typed route"
        )
    if value.campaign_id != expected_campaign_id:
        raise RuntimeHostError("selected-LIVE route belongs to another campaign")
    try:
        validate_live_route_completeness(value)
    except ValueError as exc:
        raise RuntimeHostError(
            "selected-LIVE route is not current and complete"
        ) from exc
    return value


class _BoundService:
    """Immutable handle to the one composition root that owns the service."""

    __slots__ = ("_host",)

    def __init__(self, host: RuntimeHost) -> None:
        object.__setattr__(self, "_host", host)

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise AttributeError(f"bound service attribute {name!r} is immutable")

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError(f"bound service attribute {name!r} cannot be deleted")


class ContextService(_BoundService):
    """Fixed route to the owner-native ephemeral Context Runtime."""

    __slots__ = ()

    def assemble(
        self,
        request: dict[str, object],
        candidates: list[dict[str, object]],
    ) -> dict[str, object]:
        basis = self._host._begin_operation()
        try:
            from . import context_runtime
        except ModuleNotFoundError as exc:
            raise RuntimeHostError("Context Runtime owner is unavailable") from exc
        return context_runtime._assemble_bound_context(
            request,
            candidates,
            repository=self._host._repository,
            pinned_campaign=basis.pinned_campaign,
            selected_live=basis.selected_live,
            selected_live_reader=self._host._live_transport,
        )


class HistoryService(_BoundService):
    """Fixed route to native history; it is a sibling of ContextService."""

    __slots__ = ()

    def read(self, *, origin: str = "LOCAL") -> object:
        """Read a bounded native evt window through this host's fresh basis."""

        basis = self._host._begin_operation()
        from .history import _read_bound_native_history

        return _read_bound_native_history(
            self._host._repository,
            campaign_id=self._host._campaign_id,
            campaign_pin=basis.pinned_campaign,
            current_routing=basis.selected_live,
            selected_live_reader=self._host._live_transport,
            origin=origin,
        )

    def recover(self, *, origin: str = "LOCAL") -> object:
        """Recover by re-reading the same bound native source route."""

        return self.read(origin=origin)

    def observe_first_initialization_history(self):
        self._host._begin_operation()
        from .history import observe_first_initialization_history

        return observe_first_initialization_history(
            self._host._repository, self._host._campaign_id
        )


class NativeOrderingService(_BoundService):
    """Fixed route to the Step-3 runtime-execution ordered-owner producer."""

    __slots__ = ()

    def resolve(self, request: object) -> NativeOrderingResult | object:
        basis = self._host._begin_operation()
        try:
            from . import runtime_execution
        except ModuleNotFoundError as exc:
            raise RuntimeHostError("runtime execution owner is unavailable") from exc

        resolver = getattr(runtime_execution, "resolve_native_ordering_evidence", None)
        if not callable(resolver):
            return NativeOrderingResult(
                status=NativeOrderingStatus.NO_ORDERED_OWNER,
                campaign_id=basis.pinned_campaign.campaign_id,
            )
        return resolver(
            request,
            repository=self._host._repository,
            campaign_pin=basis.pinned_campaign,
            selected_live=basis.selected_live,
        )


class RuntimeHost:
    """Ephemeral root for exactly one selected campaign.

    Construction is an infrastructure operation.  Once constructed, every
    normal attribute assignment and deletion is rejected; callers cannot
    replace the repository, selected-LIVE transport or sibling services.
    """

    __slots__ = (
        "_campaign_id",
        "_context",
        "_history",
        "_live_transport",
        "_native_ordering",
        "_repository",
    )

    def __init__(
        self,
        selected_campaign_id: str,
        authenticated_repository_port: RepositoryPort,
        selected_live_transport: SelectedLiveTransport,
    ) -> None:
        campaign_id = _require_nonempty_campaign_id(selected_campaign_id)
        _require_operations(
            authenticated_repository_port,
            _REPOSITORY_OPERATIONS,
            "authenticated RepositoryPort",
        )
        _require_operations(
            selected_live_transport, (_LIVE_OPERATION,), "selected-LIVE transport"
        )
        object.__setattr__(self, "_campaign_id", campaign_id)
        object.__setattr__(self, "_repository", authenticated_repository_port)
        object.__setattr__(self, "_live_transport", selected_live_transport)
        object.__setattr__(self, "_context", ContextService(self))
        object.__setattr__(self, "_history", HistoryService(self))
        object.__setattr__(self, "_native_ordering", NativeOrderingService(self))

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise AttributeError(f"runtime host binding {name!r} is immutable")

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError(f"runtime host binding {name!r} cannot be deleted")

    def __reduce__(self) -> NoReturn:
        raise TypeError("RuntimeHost is ephemeral and cannot be serialized")

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError("RuntimeHost is ephemeral and cannot be serialized")

    @property
    def campaign_id(self) -> str:
        return self._campaign_id

    @property
    def context(self) -> ContextService:
        return self._context

    @property
    def history(self) -> HistoryService:
        return self._history

    @property
    def native_ordering(self) -> NativeOrderingService:
        return self._native_ordering

    def _begin_operation(self) -> _OperationBasis:
        try:
            pinned = self._repository.pin_campaign(self._campaign_id)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("campaign pinning failed") from exc
        pinned_campaign = _validate_pinned_campaign(pinned, self._campaign_id)
        try:
            selected_live = self._live_transport.read_selected_live(
                self._campaign_id, pinned_campaign
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("selected-LIVE currentness read failed") from exc
        return _OperationBasis(
            pinned_campaign=pinned_campaign,
            selected_live=_validate_selected_live(selected_live, self._campaign_id),
        )


def compose_runtime_host(
    selected_campaign_id: str,
    authenticated_repository_port: RepositoryPort,
    selected_live_transport: SelectedLiveTransport,
) -> RuntimeHost:
    """Compose one immutable, campaign-bound ephemeral runtime root."""

    return RuntimeHost(
        selected_campaign_id,
        authenticated_repository_port,
        selected_live_transport,
    )
