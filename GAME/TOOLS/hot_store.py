"""Local typed HOT owner state, subordinate to native owner authority."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .native_storage import (
    IdentityMismatch,
    NativeFamilyIndex,
    NativeStorageError,
    rebuild_family_index,
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


class NativeHotStore:
    """SQLite working-state store with campaign/family/identity owner uniqueness."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
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

    def __enter__(self) -> NativeHotStore:
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def stage_owner_document(self, document: OwnerDocument) -> None:
        """Establish one validated owner row as local dirty working state."""
        document.validate()
        with self._connection:
            self._stage(document)

    def atomic_owner_mutation(self, documents: Iterable[OwnerDocument]) -> None:
        """Commit a local owner mutation atomically, without any external transaction."""
        staged = tuple(documents)
        for document in staged:
            document.validate()
        with self._connection:
            for document in staged:
                self._stage(document)

    def load_current_owner(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
    ) -> OwnerDocument | None:
        """Load one current local owner only by its complete semantic key."""
        identity_json = _canonical_identity(identity)
        row = self._connection.execute(
            """
            SELECT payload_json, source_basis, generation
            FROM current_native_owner
            WHERE campaign_id = ? AND family_key = ? AND identity_json = ?
            """,
            (campaign_id, family_key, identity_json),
        ).fetchone()
        if row is None:
            return None
        payload = json.loads(row[0])
        if not isinstance(payload, dict):
            raise IdentityMismatch("stored HOT payload is not an owner object")
        document = OwnerDocument(
            campaign_id=campaign_id,
            family_key=family_key,
            identity=tuple(identity),
            payload=payload,
            source_basis=row[1],
            generation=row[2],
        )
        document.validate()
        return document

    def clear_published_generation(
        self,
        campaign_id: str,
        family_key: str,
        identity: Sequence[str],
        published_generation: int,
    ) -> int:
        """Clear dirty state only when publication confirms this exact generation."""
        with self._connection:
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
