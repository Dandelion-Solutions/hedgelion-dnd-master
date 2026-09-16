"""Central deterministic size estimation and packet-first allocation."""

from __future__ import annotations

import json
from typing import Any


class ContextBudgetError(ValueError):
    """A context allocation request has no legal bounded allocation."""


def estimate_size(value: Any) -> int:
    """Return a centralized conservative UTF-8 byte estimate for one candidate."""
    if isinstance(value, dict) and isinstance(value.get("size"), int) and not isinstance(value["size"], bool):
        return value["size"]
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def allocate(required: list[dict[str, Any]], optional: list[dict[str, Any]], budget: int) -> dict[str, Any]:
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ContextBudgetError("budget must be a nonnegative integer")
    required_size = sum(estimate_size(item) for item in required)
    if required_size > budget:
        return {"outcome": "UNSATISFIABLE", "required": [], "optional": [], "used": 0}
    used = required_size
    selected: list[dict[str, Any]] = []
    for item in sorted(optional, key=lambda value: (-value.get("rank", 0), value["candidate_id"])):
        size = estimate_size(item)
        if used + size <= budget:
            selected.append(item)
            used += size
    outcome = "ASSEMBLED" if len(selected) == len(optional) else "ASSEMBLED_DEGRADED"
    return {"outcome": outcome, "required": required, "optional": selected, "used": used}
