"""Owner-neutral evidence bindings shared by bounded handoff adapters.

This module intentionally knows neither LIVE state nor operational-root
semantics.  An owning producer registers an accepted proof after validating its
own contract; consumers can then verify object identity and exact source
binding without importing that producer's module.
"""

from __future__ import annotations

from collections.abc import Sequence
import re
import weakref


_SOURCE_REVISION = re.compile(
    r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$"
)
_ISSUED_ABSORPTION_EVIDENCE: dict[
    int,
    tuple[weakref.ReferenceType[object], tuple[str, str, str], str],
] = {}


def mark_accepted_absorption_evidence(
    evidence: object,
    *,
    source_key: Sequence[str],
    source_revision: str,
) -> object:
    """Register one owner-validated accepted proof at its exact source."""

    key = _source_key(source_key)
    revision = _source_revision(source_revision)
    evidence_id = id(evidence)

    def remove(reference: weakref.ReferenceType[object]) -> None:
        current = _ISSUED_ABSORPTION_EVIDENCE.get(evidence_id)
        if current is not None and current[0] is reference:
            _ISSUED_ABSORPTION_EVIDENCE.pop(evidence_id, None)

    try:
        evidence_ref = weakref.ref(evidence, remove)
    except TypeError as exc:
        raise ValueError("accepted absorption evidence must be weak-referenceable") from exc
    _ISSUED_ABSORPTION_EVIDENCE[evidence_id] = (evidence_ref, key, revision)
    return evidence


def validate_accepted_absorption_evidence(
    evidence: object,
    *,
    source_key: Sequence[str],
    source_revision: str,
) -> None:
    """Require an owning producer's accepted proof for one exact source."""

    record = _ISSUED_ABSORPTION_EVIDENCE.get(id(evidence))
    if record is None or record[0]() is not evidence:
        raise ValueError("accepted absorption evidence is not owner-issued")
    expected_key = _source_key(source_key)
    expected_revision = _source_revision(source_revision)
    if record[1] != expected_key or record[2] != expected_revision:
        raise ValueError("accepted absorption evidence is bound to another source")


def _source_key(value: Sequence[str]) -> tuple[str, str, str]:
    if isinstance(value, (str, bytes)) or len(value) != 3:
        raise ValueError("accepted absorption source key must have three components")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError("accepted absorption source key must be non-empty strings")
    return tuple(value)  # type: ignore[return-value]


def _source_revision(value: object) -> str:
    if not isinstance(value, str) or _SOURCE_REVISION.fullmatch(value) is None:
        raise ValueError("accepted absorption source revision is not exact")
    return value
