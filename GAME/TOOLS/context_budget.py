"""Central deterministic size estimation and packet-first allocation."""

from __future__ import annotations

import json
from typing import Any


class ContextBudgetError(ValueError):
    """A context allocation request has no legal bounded allocation."""


def estimate_size(value: Any) -> int:
    """Return a centralized conservative UTF-8 byte estimate for one candidate."""
    try:
        return len(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        )
    except (TypeError, ValueError) as exc:
        raise ContextBudgetError(
            "payload is not a valid canonical context value"
        ) from exc


def _candidate_size(candidate: dict[str, Any]) -> int:
    if (
        not isinstance(candidate, dict)
        or "size" in candidate
        or "payload" not in candidate
    ):
        raise ContextBudgetError(
            "candidate must carry a payload, not a caller-supplied size"
        )
    return estimate_size(candidate["payload"])


def _candidate_rank(candidate: dict[str, Any]) -> int:
    rank = candidate.get("rank", 0)
    if isinstance(rank, bool) or not isinstance(rank, int):
        raise ContextBudgetError("candidate rank must be an integer")
    return rank


def allocate(
    required: list[dict[str, Any]], optional: list[dict[str, Any]], budget: int
) -> dict[str, Any]:
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ContextBudgetError("budget must be a nonnegative integer")
    required_size = sum(_candidate_size(item) for item in required)
    if required_size > budget:
        return {"outcome": "UNSATISFIABLE", "required": [], "optional": [], "used": 0}
    used = required_size
    selected: list[dict[str, Any]] = []
    for item in sorted(
        optional, key=lambda value: (-_candidate_rank(value), value["candidate_id"])
    ):
        size = _candidate_size(item)
        if used + size <= budget:
            selected.append(item)
            used += size
    outcome = "ASSEMBLED" if len(selected) == len(optional) else "ASSEMBLED_DEGRADED"
    return {
        "outcome": outcome,
        "required": required,
        "optional": selected,
        "used": used,
    }
