"""Bounded, ephemeral Context Runtime discovery and assembly primitives."""

from __future__ import annotations

from typing import Any

from context_budget import allocate


class ContextContractError(ValueError):
    """A context candidate or scoped join violates the registered request."""


def discover_candidates(request: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    channels = request.get("allowed_channels")
    limit = request.get("max_candidates")
    if not isinstance(channels, list) or not channels or isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ContextContractError("request must name bounded registered discovery channels")
    found = [item for item in candidates if item.get("channel") in channels]
    return sorted(found, key=lambda item: item.get("candidate_id", ""))[:limit]


def resolve_candidate_basis(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict) or not candidate.get("candidate_id"):
        raise ContextContractError("candidate identity is required")
    if candidate.get("current") is not True:
        raise ContextContractError("candidate is not current at its native owner")
    if candidate.get("eligible") is not True:
        raise ContextContractError("candidate is not eligible role evidence")
    return candidate


def _required_closure(required_ids: list[str], available: dict[str, dict[str, Any]]) -> list[dict[str, Any]] | None:
    pending = list(required_ids)
    resolved: dict[str, dict[str, Any]] = {}
    while pending:
        candidate_id = pending.pop()
        if candidate_id in resolved:
            continue
        candidate = available.get(candidate_id)
        if candidate is None:
            return None
        try:
            resolved[candidate_id] = resolve_candidate_basis(candidate)
        except ContextContractError:
            return None
        dependencies = candidate.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            return None
        pending.extend(dependencies)
    return [resolved[key] for key in sorted(resolved)]


def assemble_context(request: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    profile_id = request.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id:
        raise ContextContractError("profile_id is required")
    discovered = discover_candidates(request, candidates)
    available = {item.get("candidate_id"): item for item in discovered if isinstance(item.get("candidate_id"), str)}
    required_ids = request.get("required_ids", [])
    if not isinstance(required_ids, list) or any(not isinstance(item, str) for item in required_ids):
        raise ContextContractError("required_ids must be strings")
    required = _required_closure(required_ids, available)
    trace = {"profile_id": profile_id, "discovered_ids": sorted(available), "included_ids": [], "excluded_ids": []}
    if required is None:
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    required_set = {item["candidate_id"] for item in required}
    optional: list[dict[str, Any]] = []
    for item in discovered:
        if item["candidate_id"] in required_set:
            continue
        try:
            optional.append(resolve_candidate_basis(item))
        except ContextContractError:
            trace["excluded_ids"].append(item["candidate_id"])
    allocation = allocate(required, optional, request.get("budget", 0))
    if allocation["outcome"] == "UNSATISFIABLE":
        return {"outcome": "UNSATISFIABLE", "bundle": None, "trace": trace}
    trace["included_ids"] = [item["candidate_id"] for item in allocation["required"] + allocation["optional"]]
    bundle = {
        "profile_id": profile_id,
        "source_frontier": request.get("source_frontier", ""),
        "recipient_id": request.get("recipient_id", ""),
        "required": allocation["required"],
        "optional": allocation["optional"],
        "retrospective_projection": request.get("retrospective", False) is True,
    }
    return {"outcome": allocation["outcome"], "bundle": bundle, "trace": trace}


def scoped_context_join(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    keys = ("profile_id", "source_frontier", "recipient_id")
    if any(left.get(key) != right.get(key) for key in keys):
        raise ContextContractError("context join requires one scoped profile/frontier/recipient basis")
    return {key: left.get(key) for key in keys}
