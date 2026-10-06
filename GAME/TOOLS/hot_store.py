"""Local typed HOT owner state, subordinate to native owner authority."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import weakref
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from types import MappingProxyType
from typing import Protocol, Self

from .native_storage import (
    IdentityMismatch,
    NativeFamilyIndex,
    NativeStorageError,
    rebuild_family_index,
    route_native_record,
    validate_loaded_identity,
)


class StaleOwnerGeneration(NativeStorageError):
    """A local update would replace an equal or newer accepted HOT generation."""


@dataclass(frozen=True, slots=True)
class OwnerDocument:
    campaign_id: str
    family_key: str
    identity: tuple[str, ...]
    payload: Mapping[str, object]
    source_basis: str
    generation: int

    def validate(self) -> None:
        if not self.campaign_id or not self.source_basis or self.generation < 0:
            raise ValueError("owner document has invalid campaign, basis, or generation")
        validate_loaded_identity(self.family_key, self.identity, self.payload)


@dataclass(frozen=True, slots=True)
class HotOwnerReadSnapshot:
    """Detached admitted HOT rows and explicit absences from one SQLite read."""

    campaign_id: str
    requested_keys: tuple[tuple[str, tuple[str, ...]], ...]
    rows: Mapping[tuple[str, tuple[str, ...]], OwnerDocument]
    absent_keys: tuple[tuple[str, tuple[str, ...]], ...]
    row_fingerprints: Mapping[tuple[str, tuple[str, ...]], str]
    admission_bases: Mapping[tuple[str, tuple[str, ...]], HotOwnerAdmissionBasis]
    snapshot_fingerprint: str
    _store_token: object


@dataclass(frozen=True, slots=True)
class HotOwnerAdmissionBasis:
    """Process-local proof tying one accepted HOT row to its exact predecessor."""

    source_revision: str
    source_fingerprint: str


@dataclass(frozen=True, slots=True)
class HotEventDiscoverySnapshot:
    """Derived nominations only; native kernel acceptance integration is pending."""

    entries: tuple[Mapping[str, object], ...]
    snapshot_fingerprint: str
    acceptance_integrated: bool = False


class HotOwnerStorePort(Protocol):
    """Infrastructure-only HOT read and native Actor establishment capability."""

    def read_admitted_snapshot(
        self,
        campaign_id: str,
        owner_keys: tuple[tuple[str, Sequence[str]], ...],
    ) -> HotOwnerReadSnapshot: ...

    def _lookup_actor_phase_consumption(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
        phase_result: object,
        host_token: object,
    ) -> tuple[object, str | None] | None: ...

    def _establish_actor_owner(
        self,
        document: OwnerDocument,
        expected_snapshot: HotOwnerReadSnapshot,
        *,
        phase_result: object,
        host_token: object,
        establishment_result: object,
        source_fingerprint: str,
    ) -> None: ...

    def _consume_actor_no_change(
        self,
        *,
        campaign_id: str,
        identity: Sequence[str],
        expected_snapshot: HotOwnerReadSnapshot,
        phase_result: object,
        host_token: object,
        result: object,
        source_fingerprint: str,
    ) -> None: ...


class NativeHotStore:
    """SQLite working-state store with campaign/family/identity owner uniqueness."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._lock = RLock()
        self._snapshot_token = object()
        self._admitted_rows: dict[
            tuple[str, str, str], tuple[str, HotOwnerAdmissionBasis]
        ] = {}
        self._actor_phase_consumption: weakref.WeakKeyDictionary[
            object, tuple[tuple[str, str, str], object, object, str | None]
        ] = weakref.WeakKeyDictionary()
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS current_native_owner (
                campaign_id TEXT NOT NULL,
                family_key TEXT NOT NULL,
                identity_json TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                source_basis TEXT NOT NULL,
                generation INTEGER NOT NULL,
                dirty INTEGER NOT NULL,
                PRIMARY KEY (campaign_id, family_key, identity_json)
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS derived_event_discovery (
                campaign_id TEXT NOT NULL,
                event_id TEXT NOT NULL,
                source_basis TEXT NOT NULL,
                ordinal INTEGER NOT NULL,
                refs_json TEXT NOT NULL,
                event_fingerprint TEXT NOT NULL,
                PRIMARY KEY (campaign_id, event_id)
            )
            """
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def _stage_event_discovery_helper(
        self, campaign_id: str, event: Mapping[str, object], source_basis: str
    ) -> None:
        """Stage derived metadata in an existing local transaction, never acceptance.

        The SP04 kernel join must later call this from its accepted event edge.
        This helper neither stages a native owner nor issues an admission marker.
        """
        from .history import _semantic_event_fingerprint, validate_semantic_event_draft

        if (
            not isinstance(campaign_id, str)
            or not campaign_id
            or not isinstance(source_basis, str)
            or not re.fullmatch(r"[a-f0-9]{40}(?:[a-f0-9]{24})?", source_basis)
        ):
            raise NativeStorageError("event helper requires exact campaign/source basis")
        record = validate_semantic_event_draft(event)
        with self._lock:
            if not self._connection.in_transaction:
                raise NativeStorageError("event helper requires the existing owner transaction")
            self._connection.execute(
                """INSERT INTO derived_event_discovery
                    (campaign_id, event_id, source_basis, ordinal, refs_json, event_fingerprint)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(campaign_id, event_id) DO UPDATE SET
                      source_basis=excluded.source_basis, ordinal=excluded.ordinal,
                      refs_json=excluded.refs_json, event_fingerprint=excluded.event_fingerprint""",
                (campaign_id, record["event_id"], source_basis, record["semantic_order"],
                 json.dumps(record["semantic_delta"].get("discovery_refs", []), sort_keys=True),
                 _semantic_event_fingerprint(record)),
            )

    def read_admitted_event_discovery(
        self, campaign_id: str, max_candidates: int
    ) -> HotEventDiscoverySnapshot:
        """Read a finite helper snapshot; raw/stale surviving rows are excluded.

        No SemanticEvent acceptance producer exists here. Until the native SP04
        join is integrated the result explicitly cannot prove discovery completeness.
        """
        from .history import _semantic_event_fingerprint, validate_semantic_event_draft

        if not isinstance(campaign_id, str) or not campaign_id:
            raise NativeStorageError("event discovery campaign is required")
        if type(max_candidates) is not int or not 1 <= max_candidates <= 1000:
            raise NativeStorageError("event discovery requires a finite positive bound")
        entries: list[Mapping[str, object]] = []
        with self._lock:
            self._connection.execute("BEGIN")
            try:
                # Query only a bounded narrow helper, never the owner table or
                # the complete admitted-owner set. Each nomination must still
                # match a native producer's process-local admission marker.
                rows = self._connection.execute(
                    "SELECT event_id, source_basis, ordinal, refs_json, event_fingerprint "
                    "FROM derived_event_discovery WHERE campaign_id=? LIMIT ?",
                    (campaign_id, max_candidates),
                ).fetchall()
                for event_id, source_basis, ordinal, refs_json, event_fingerprint in rows:
                    identity = (event_id,)
                    family = "runtime.semantic_event"
                    admission = self._admitted_rows.get(
                        _store_key(campaign_id, family, identity)
                    )
                    if admission is None:
                        continue
                    native_row = self._connection.execute(
                        "SELECT payload_json, source_basis, generation FROM current_native_owner "
                        "WHERE campaign_id=? AND family_key=? AND identity_json=?",
                        (campaign_id, family, _canonical_identity(identity)),
                    ).fetchone()
                    if native_row is None:
                        continue
                    # Same native adapter convention as the History source reader:
                    # event_id + semantic kind, never synthetic generic id/kind.
                    payload = validate_semantic_event_draft(json.loads(native_row[0]))
                    if payload["event_id"] != event_id:
                        raise IdentityMismatch("HOT event identity differs from helper route")
                    document = OwnerDocument(
                        campaign_id, family, identity, payload,
                        native_row[1], native_row[2],
                    )
                    if (
                        _owner_fingerprint(document) != admission[0]
                        or source_basis != document.source_basis
                        or event_fingerprint != _semantic_event_fingerprint(document.payload)
                    ):
                        continue
                    entries.append(MappingProxyType({
                        "event_id": event_id,
                        "source_basis": source_basis,
                        "ordinal": ordinal,
                        "discovery_refs": tuple(
                            _freeze_helper_ref(ref) for ref in json.loads(refs_json)
                        ),
                    }))
                self._connection.execute("COMMIT")
            except BaseException:
                self._connection.execute("ROLLBACK")
                raise
        fingerprint = _semantic_event_fingerprint({"entries": entries})
        return HotEventDiscoverySnapshot(tuple(entries), fingerprint)

    def stage_owner_document(self, document: OwnerDocument) -> None:
        """Establish one validated owner row as local dirty working state."""
        document.validate()
        with self._lock, self._connection:
            self._stage(document)

    def atomic_owner_mutation(self, documents: Iterable[OwnerDocument]) -> None:
        """Commit a local owner mutation atomically, without any external transaction."""
        staged = tuple(documents)
        for document in staged:
            document.validate()
        with self._lock, self._connection:
            for document in staged:
                self._stage(document)

    def load_current_owner(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
    ) -> OwnerDocument | None:
        """Load one current local owner only by its complete semantic key."""
        with self._lock:
            document = self._load_document(campaign_id, family_key, tuple(identity))
            return _detach_document(document) if document is not None else None

    def read_admitted_snapshot(
        self,
        campaign_id: str,
        owner_keys: tuple[tuple[str, Sequence[str]], ...],
    ) -> HotOwnerReadSnapshot:
        """Read exact requested keys in one closed SQLite snapshot.

        Persisted dirty rows do not become current merely by surviving restart;
        only this store instance's successful native-owner establishment markers
        can admit them.
        """

        if not isinstance(campaign_id, str) or not campaign_id:
            raise ValueError("HOT snapshot campaign id is required")
        requested: list[tuple[str, tuple[str, ...]]] = []
        for family_key, identity_value in owner_keys:
            identity = tuple(identity_value)
            if not identity or any(not isinstance(part, str) or not part for part in identity):
                raise ValueError("HOT snapshot identity must be complete")
            route_native_record(family_key, identity)
            requested.append((family_key, identity))
        if len(requested) != len(set(requested)):
            raise ValueError("HOT snapshot owner keys must be unique")
        requested_keys = tuple(requested)

        with self._lock:
            rows: dict[tuple[str, tuple[str, ...]], OwnerDocument] = {}
            fingerprints: dict[tuple[str, tuple[str, ...]], str] = {}
            admission_bases: dict[
                tuple[str, tuple[str, ...]], HotOwnerAdmissionBasis
            ] = {}
            absent: list[tuple[str, tuple[str, ...]]] = []
            self._connection.execute("BEGIN")
            try:
                for family_key, identity in requested_keys:
                    document = self._load_document(campaign_id, family_key, identity)
                    key = (family_key, identity)
                    if document is None:
                        absent.append(key)
                        continue
                    fingerprint = _owner_fingerprint(document)
                    admission = self._admitted_rows.get(
                        _store_key(campaign_id, family_key, identity)
                    )
                    if admission is None or admission[0] != fingerprint:
                        absent.append(key)
                        continue
                    rows[key] = _detach_document(document)
                    fingerprints[key] = fingerprint
                    admission_bases[key] = admission[1]
                self._connection.execute("COMMIT")
            except BaseException:
                self._connection.execute("ROLLBACK")
                raise

            snapshot_fingerprint = _snapshot_fingerprint(
                requested_keys, fingerprints
            )
            return HotOwnerReadSnapshot(
                campaign_id=campaign_id,
                requested_keys=requested_keys,
                rows=MappingProxyType(rows),
                absent_keys=tuple(absent),
                row_fingerprints=MappingProxyType(fingerprints),
                admission_bases=MappingProxyType(admission_bases),
                snapshot_fingerprint=snapshot_fingerprint,
                _store_token=self._snapshot_token,
            )

    def clear_published_generation(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
        published_generation: int,
    ) -> int:
        """Clear dirty state only when publication confirms this exact generation."""
        with self._lock, self._connection:
            cursor = self._connection.execute(
                """
                UPDATE current_native_owner
                SET dirty = 0
                WHERE campaign_id = ? AND family_key = ? AND identity_json = ?
                  AND generation = ? AND dirty = 1
                """,
                (campaign_id, family_key, _canonical_identity(identity), published_generation),
            )
        return cursor.rowcount

    def _stage(self, document: OwnerDocument) -> None:
        identity_json = _canonical_identity(document.identity)
        existing = self._connection.execute(
            """
            SELECT payload_json, source_basis, generation
            FROM current_native_owner
            WHERE campaign_id = ? AND family_key = ? AND identity_json = ?
            """,
            (document.campaign_id, document.family_key, identity_json),
        ).fetchone()
        if existing is not None:
            existing_payload, existing_basis, existing_generation = existing
            candidate_payload = json.dumps(document.payload, sort_keys=True, separators=(",", ":"))
            if document.generation < existing_generation:
                raise StaleOwnerGeneration("stale HOT generation requires reconciliation from current owner state")
            if document.generation == existing_generation:
                if existing_payload != candidate_payload or existing_basis != document.source_basis:
                    raise StaleOwnerGeneration("conflicting HOT generation requires reconciliation")
                return
        self._connection.execute(
            """
            INSERT INTO current_native_owner (
                campaign_id, family_key, identity_json, payload_json, source_basis, generation, dirty
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(campaign_id, family_key, identity_json) DO UPDATE SET
                payload_json = excluded.payload_json,
                source_basis = excluded.source_basis,
                generation = excluded.generation,
                dirty = 1
            """,
            (
                document.campaign_id,
                document.family_key,
                identity_json,
                json.dumps(document.payload, sort_keys=True, separators=(",", ":")),
                document.source_basis,
                document.generation,
            ),
        )

    def _lookup_actor_phase_consumption(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
        phase_result: object,
        host_token: object,
    ) -> tuple[object, str | None] | None:
        key = _store_key(campaign_id, family_key, tuple(identity))
        with self._lock:
            consumption = self._actor_phase_consumption.get(phase_result)
            if (
                consumption is None
                or consumption[0] != key
                or consumption[1] is not host_token
            ):
                return None
            return consumption[2], consumption[3]

    def _establish_actor_owner(
        self,
        document: OwnerDocument,
        expected_snapshot: HotOwnerReadSnapshot,
        *,
        phase_result: object,
        host_token: object,
        establishment_result: object,
        source_fingerprint: str,
    ) -> None:
        """Atomically establish a native Actor row and its process-local receipt."""

        document.validate()
        if document.family_key != "world.actor":
            raise NativeStorageError("Actor establishment requires world.actor")
        if (
            not isinstance(source_fingerprint, str)
            or len(source_fingerprint) != 64
            or any(character not in "0123456789abcdef" for character in source_fingerprint)
            or not re.fullmatch(r"[a-f0-9]{40}(?:[a-f0-9]{24})?", document.source_basis)
        ):
            raise NativeStorageError("Actor establishment requires an exact source basis")
        if (
            not isinstance(expected_snapshot, HotOwnerReadSnapshot)
            or expected_snapshot._store_token is not self._snapshot_token
            or expected_snapshot.campaign_id != document.campaign_id
            or (document.family_key, document.identity) not in expected_snapshot.requested_keys
        ):
            raise NativeStorageError("Actor establishment basis is not this store's snapshot")
        key = _store_key(document.campaign_id, document.family_key, document.identity)
        with self._lock:
            if self._snapshot_fingerprint_locked(
                expected_snapshot.campaign_id, expected_snapshot.requested_keys
            ) != expected_snapshot.snapshot_fingerprint:
                raise StaleOwnerGeneration("HOT predecessor changed before Actor establishment")
            self._connection.execute("BEGIN IMMEDIATE")
            try:
                if self._snapshot_fingerprint_in_transaction(
                    expected_snapshot.campaign_id, expected_snapshot.requested_keys
                ) != expected_snapshot.snapshot_fingerprint:
                    raise StaleOwnerGeneration("HOT predecessor changed during Actor establishment")
                # Existing non-admitted rows are cache residue, not authority. The
                # caller has revalidated the exact current native predecessor.
                if (document.family_key, document.identity) in expected_snapshot.absent_keys:
                    self._connection.execute(
                        "DELETE FROM current_native_owner WHERE campaign_id = ? AND family_key = ? AND identity_json = ?",
                        (document.campaign_id, document.family_key, _canonical_identity(document.identity)),
                    )
                self._stage(document)
                self._connection.execute("COMMIT")
            except BaseException:
                if self._connection.in_transaction:
                    self._connection.execute("ROLLBACK")
                raise
            self._admitted_rows[key] = (
                _owner_fingerprint(document),
                HotOwnerAdmissionBasis(
                    source_revision=document.source_basis,
                    source_fingerprint=source_fingerprint,
                ),
            )
            self._actor_phase_consumption[phase_result] = (
                key,
                host_token,
                establishment_result,
                _owner_fingerprint(document),
            )

    def _consume_actor_no_change(
        self,
        *,
        campaign_id: str,
        identity: Sequence[str],
        expected_snapshot: HotOwnerReadSnapshot,
        phase_result: object,
        host_token: object,
        result: object,
        source_fingerprint: str,
    ) -> None:
        key = _store_key(campaign_id, "world.actor", tuple(identity))
        if (
            expected_snapshot._store_token is not self._snapshot_token
            or expected_snapshot.campaign_id != campaign_id
            or ("world.actor", tuple(identity)) not in expected_snapshot.requested_keys
        ):
            raise NativeStorageError("NO_CHANGE basis is not this store's snapshot")
        if not isinstance(source_fingerprint, str) or not source_fingerprint:
            raise NativeStorageError("NO_CHANGE requires an exact owner fingerprint")
        with self._lock:
            self._connection.execute("BEGIN IMMEDIATE")
            try:
                if self._snapshot_fingerprint_in_transaction(
                    campaign_id, expected_snapshot.requested_keys
                ) != expected_snapshot.snapshot_fingerprint:
                    raise StaleOwnerGeneration("HOT predecessor changed before NO_CHANGE")
                self._connection.execute("COMMIT")
            except BaseException:
                if self._connection.in_transaction:
                    self._connection.execute("ROLLBACK")
                raise
            self._actor_phase_consumption[phase_result] = (
                key,
                host_token,
                result,
                source_fingerprint,
            )

    def _snapshot_fingerprint_locked(
        self,
        campaign_id: str,
        requested_keys: Sequence[tuple[str, tuple[str, ...]]],
    ) -> str:
        self._connection.execute("BEGIN")
        try:
            fingerprint = self._snapshot_fingerprint_in_transaction(
                campaign_id, requested_keys
            )
            self._connection.execute("COMMIT")
        except BaseException:
            self._connection.execute("ROLLBACK")
            raise
        return fingerprint

    def _snapshot_fingerprint_in_transaction(
        self,
        campaign_id: str,
        requested_keys: Sequence[tuple[str, tuple[str, ...]]],
    ) -> str:
        fingerprints: dict[tuple[str, tuple[str, ...]], str] = {}
        for family_key, identity in requested_keys:
            document = self._load_document(campaign_id, family_key, identity)
            if document is None:
                continue
            fingerprint = _owner_fingerprint(document)
            admission = self._admitted_rows.get(
                _store_key(campaign_id, family_key, identity)
            )
            if admission is not None and admission[0] == fingerprint:
                fingerprints[(family_key, identity)] = fingerprint
        return _snapshot_fingerprint(requested_keys, fingerprints)

    def _load_document(
        self, campaign_id: str, family_key: str, identity: tuple[str, ...]
    ) -> OwnerDocument | None:
        row = self._connection.execute(
            """
            SELECT payload_json, source_basis, generation
            FROM current_native_owner
            WHERE campaign_id = ? AND family_key = ? AND identity_json = ?
            """,
            (campaign_id, family_key, _canonical_identity(identity)),
        ).fetchone()
        if row is None:
            return None
        payload = json.loads(row[0])
        if not isinstance(payload, dict):
            raise IdentityMismatch("stored HOT payload is not an owner object")
        document = OwnerDocument(
            campaign_id=campaign_id,
            family_key=family_key,
            identity=identity,
            payload=payload,
            source_basis=row[1],
            generation=row[2],
        )
        document.validate()
        return document


def stage_owner_document(document: OwnerDocument) -> OwnerDocument:
    """Validate a staged document before it enters an owner-local HOT mutation."""
    document.validate()
    return document


def stage_index_delta(index: Mapping[str, object]) -> Mapping[str, object]:
    """Keep index material explicitly derived and free of owner payloads."""
    if "entries" not in index:
        raise ValueError("index delta has no entries")
    return index


def clear_published_generation(
    store: NativeHotStore,
    campaign_id: str,
    family_key: str,
    identity: Sequence[str],
    published_generation: int,
) -> int:
    """Expose generation-specific dirty clearing without adding publication authority."""
    return store.clear_published_generation(campaign_id, family_key, identity, published_generation)


def rebuild_helper(
    family_key: str,
    records: Iterable[Mapping[str, object]],
) -> NativeFamilyIndex:
    """Make derived rebuild behavior explicit rather than an ordinary owner read path."""
    return rebuild_family_index(family_key, records)


def _canonical_identity(identity: Sequence[str]) -> str:
    if not identity or any(not isinstance(component, str) or not component for component in identity):
        raise ValueError("owner identity must contain non-empty strings")
    return json.dumps(list(identity), ensure_ascii=False, separators=(",", ":"))


def _freeze_helper_ref(ref: Mapping[str, object]) -> Mapping[str, object]:
    return MappingProxyType({"family_key": ref["family_key"], "identity": tuple(ref["identity"])})


def _store_key(
    campaign_id: str, family_key: str, identity: Sequence[str]
) -> tuple[str, str, str]:
    return campaign_id, family_key, _canonical_identity(identity)


def _owner_fingerprint(document: OwnerDocument) -> str:
    encoded = json.dumps(
        {
            "campaign_id": document.campaign_id,
            "family_key": document.family_key,
            "identity": list(document.identity),
            "payload": document.payload,
            "source_basis": document.source_basis,
            "generation": document.generation,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _snapshot_fingerprint(
    requested_keys: Sequence[tuple[str, tuple[str, ...]]],
    row_fingerprints: Mapping[tuple[str, tuple[str, ...]], str],
) -> str:
    projection = [
        {
            "family_key": family_key,
            "identity": list(identity),
            "row_fingerprint": row_fingerprints.get((family_key, identity)),
        }
        for family_key, identity in sorted(requested_keys)
    ]
    encoded = json.dumps(
        projection,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _detach_document(document: OwnerDocument) -> OwnerDocument:
    return OwnerDocument(
        campaign_id=document.campaign_id,
        family_key=document.family_key,
        identity=tuple(document.identity),
        payload=deepcopy(dict(document.payload)),
        source_basis=document.source_basis,
        generation=document.generation,
    )
