"""Bounded native-record routes and non-authoritative discovery helpers."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


ROUTE_PREFIX = b"HDM-WP11-ROUTE-V1"

FAMILY_ROOTS: dict[str, str] = {
    "world.scene": "STATE/SCENES",
    "world.actor": "WORLD/ACTORS",
    "world.actor_group": "WORLD/ACTOR_GROUPS",
    "world.faction": "WORLD/FACTIONS",
    "world.asset": "WORLD/ITEMS",
    "world.location": "WORLD/LOCATIONS",
    "world.lore_fact": "WORLD/LORE",
    "world.player": "WORLD/PLAYERS",
    "world.thread": "WORLD/THREADS",
    "world.effect": "WORLD/EFFECTS",
    "world.connection": "WORLD/CONNECTIONS",
    "world.zone": "WORLD/ZONES",
    "world.organization": "WORLD/ORGANIZATIONS",
    "world.contract": "WORLD/CONTRACTS",
    "world.mission": "WORLD/MISSIONS",
    "world.encounter": "WORLD/ENCOUNTERS",
    "world.hazard": "WORLD/HAZARDS",
    "world.knowledge": "WORLD/KNOWLEDGE",
    "runtime.interaction": "STATE/RUNTIME/INTERACTIONS",
    "runtime.intent_plan": "STATE/RUNTIME/INTENT_PLANS",
    "runtime.command": "STATE/RUNTIME/COMMANDS",
    "runtime.procedure": "STATE/RUNTIME/PROCEDURES",
    "runtime.resolution": "STATE/RUNTIME/RESOLUTIONS",
    "runtime.continuation": "STATE/RUNTIME/CONTINUATIONS",
    "runtime.resolution_trace": "STATE/RUNTIME/RESOLUTION_TRACES",
    "runtime.disclosure": "STATE/RUNTIME/DISCLOSURES",
    "runtime.collaboration_obligation": "STATE/RUNTIME/COLLABORATION",
    "runtime.maintenance_audit": "STATE/RUNTIME/MAINTENANCE_AUDITS",
    "runtime.catalog_gap_report": "STATE/RUNTIME/CATALOG_GAP_REPORTS",
    "runtime.semantic_event": "LOG/SEMANTIC_EVENTS",
    "runtime.mechanical_event": "LOG/MECHANICAL_EVENTS",
    "runtime.message": "LOG/MESSAGES",
    "runtime.checkpoint": "CHECKPOINTS",
    "runtime.session": "SESSIONS",
}


class NativeStorageError(ValueError):
    """Base class for typed native-storage contract failures."""


class IdentityMismatch(NativeStorageError):
    """A loaded record does not match the requested native owner identity."""


class MissingCampaignRoot(NativeStorageError):
    """No candidate exists for the requested campaign root."""


class StaleCampaignRoot(NativeStorageError):
    """The only campaign-root candidate does not have the requested revision."""


class AmbiguousCampaignRoot(NativeStorageError):
    """More than one candidate claims the requested campaign root."""


class AmbiguousDiscoveryCandidate(NativeStorageError):
    """A derived index presents more than one entry for one identity."""


@dataclass(frozen=True, slots=True)
class NativeRoute:
    family_key: str
    identity: tuple[str, ...]
    relative_path: str


@dataclass(frozen=True, slots=True)
class CampaignRootCandidate:
    campaign_id: str
    root: str
    revision: str


@dataclass(frozen=True, slots=True)
class NativeFamilyIndex:
    family_key: str
    entries: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        if self.family_key not in FAMILY_ROOTS:
            raise NativeStorageError(f"unknown native family: {self.family_key}")
        for entry in self.entries:
            _validate_index_entry(self.family_key, entry)


def route_native_record(family_key: str, identity: Sequence[str]) -> NativeRoute:
    """Derive the one WP-11 route for a known native identity."""
    root = FAMILY_ROOTS.get(family_key)
    components = tuple(identity)
    if root is None:
        raise NativeStorageError(f"unknown native family: {family_key}")
    if not components or any(not isinstance(component, str) or not component for component in components):
        raise NativeStorageError("native route identity must contain non-empty components")

    framed = _frame_route_input(family_key, components)
    digest = hashlib.sha256(framed).hexdigest()
    encoded = base64.b32hexencode(framed).decode("ascii").rstrip("=")
    chunks = [encoded[offset : offset + 100] for offset in range(0, len(encoded), 100)]
    filename = f"{chunks[-1]}.yaml"
    relative_path = "/".join((root, "RECORDS", digest[:2], digest[2:4], *chunks[:-1], filename))
    return NativeRoute(family_key=family_key, identity=components, relative_path=relative_path)


def validate_loaded_identity(
    family_key: str,
    requested_identity: Sequence[str],
    payload: Mapping[str, object],
) -> None:
    """Reject a route/index result whose actual owner identity differs."""
    if family_key not in FAMILY_ROOTS:
        raise NativeStorageError(f"unknown native family: {family_key}")
    if not isinstance(payload, Mapping):
        raise IdentityMismatch("loaded owner payload is not an object")
    if payload.get("kind") != family_key:
        raise IdentityMismatch("loaded record family does not match requested family")
    actual_identity = native_identity_from_record(family_key, payload)
    if actual_identity != tuple(requested_identity):
        raise IdentityMismatch("loaded record identity does not match requested identity")
    if family_key.startswith("world.") and not isinstance(payload.get("state"), Mapping):
        raise IdentityMismatch("loaded world owner payload has no object state")


def native_identity_from_record(family_key: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    """Extract only the owner-defined identity needed to validate a loaded record."""
    composite_fields = {
        "world.knowledge": ("knower_id", "fact_id"),
        "runtime.disclosure": ("player_id", "fact_id"),
    }
    fields = composite_fields.get(family_key)
    if fields is not None:
        if "id" in payload:
            raise IdentityMismatch("loaded composite record must not carry a surrogate id")
        values: list[str] = []
        for field in fields:
            value = payload.get(field)
            if not isinstance(value, str) or not value:
                raise IdentityMismatch("loaded composite record has incomplete native identity")
            values.append(value)
        return tuple(values)
    record_id = payload.get("id")
    if not isinstance(record_id, str) or not record_id:
        raise IdentityMismatch("loaded record has no valid native id")
    return (record_id,)


def rebuild_family_index(
    family_key: str,
    records: Iterable[Mapping[str, object]],
) -> NativeFamilyIndex:
    """Build a compact, derived family index; use only in an explicit rebuild flow."""
    entries: list[Mapping[str, object]] = []
    seen: set[tuple[str, ...]] = set()
    for record in records:
        identity = native_identity_from_record(family_key, record)
        validate_loaded_identity(family_key, identity, record)
        if identity in seen:
            raise AmbiguousDiscoveryCandidate("family index cannot contain duplicate owner identities")
        seen.add(identity)
        route = route_native_record(family_key, identity)
        entry: dict[str, object] = {"id": identity[0], "path": route.relative_path}
        for field in ("name", "aliases", "status", "parent_id", "tags", "last_event_id"):
            if field in record:
                entry[field] = record[field]
        entries.append(entry)
    return NativeFamilyIndex(family_key=family_key, entries=tuple(entries))


def resolve_discovery_candidate(
    index: NativeFamilyIndex,
    record_id: str,
    read_exact_path: Callable[[str], Mapping[str, object]],
) -> Mapping[str, object] | None:
    """Use an index only to nominate one candidate, then revalidate its owner body."""
    candidates = [entry for entry in index.entries if entry.get("id") == record_id]
    if not candidates:
        return None
    if len(candidates) != 1:
        raise AmbiguousDiscoveryCandidate("index has multiple candidates for one record id")
    path = candidates[0].get("path")
    if not isinstance(path, str):
        raise NativeStorageError("index candidate has no exact record path")
    payload = read_exact_path(path)
    validate_loaded_identity(index.family_key, (record_id,), payload)
    return payload


def select_campaign_root(
    candidates: Iterable[CampaignRootCandidate],
    *,
    campaign_id: str,
    expected_revision: str,
) -> Path:
    """Select one fixed root or return a typed missing/stale/ambiguous outcome."""
    matches = [candidate for candidate in candidates if candidate.campaign_id == campaign_id]
    if not matches:
        raise MissingCampaignRoot(f"campaign root is missing: {campaign_id}")
    if len(matches) != 1:
        raise AmbiguousCampaignRoot(f"campaign root is ambiguous: {campaign_id}")
    candidate = matches[0]
    if candidate.revision != expected_revision:
        raise StaleCampaignRoot(f"campaign root is stale: {campaign_id}")
    return Path(candidate.root)


def _frame_route_input(family_key: str, identity: tuple[str, ...]) -> bytes:
    family_bytes = family_key.encode("utf-8")
    parts = [ROUTE_PREFIX, b"\x00", family_bytes, b"\x00", len(identity).to_bytes(4, "big")]
    for component in identity:
        component_bytes = component.encode("utf-8")
        parts.extend((len(component_bytes).to_bytes(4, "big"), component_bytes))
    return b"".join(parts)


def _validate_index_entry(family_key: str, entry: Mapping[str, object]) -> None:
    allowed_fields = {"id", "name", "aliases", "status", "path", "parent_id", "tags", "last_event_id"}
    if not isinstance(entry, Mapping) or set(entry) - allowed_fields:
        raise NativeStorageError("index entry is not compact routing metadata")
    record_id = entry.get("id")
    path = entry.get("path")
    if not isinstance(record_id, str) or not record_id or not isinstance(path, str):
        raise NativeStorageError("index entry has an invalid id or path")
    if path != route_native_record(family_key, (record_id,)).relative_path:
        raise NativeStorageError("index entry path does not match the deterministic native route")
    for field in ("name", "status", "parent_id", "last_event_id"):
        value = entry.get(field)
        if value is not None and not isinstance(value, str):
            raise NativeStorageError(f"index entry {field} is not compact scalar metadata")
    for field in ("aliases", "tags"):
        value = entry.get(field)
        if value is not None and (
            not isinstance(value, (list, tuple)) or any(not isinstance(item, str) for item in value)
        ):
            raise NativeStorageError(f"index entry {field} is not compact string metadata")
