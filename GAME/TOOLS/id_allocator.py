"""Campaign-scoped sequential allocator state for owner-approved identities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


@dataclass(frozen=True, slots=True)
class AllocatorState:
    campaign_id: str
    counters: Mapping[str, int]

    def require_campaign(self, campaign_id: str) -> None:
        if self.campaign_id != campaign_id:
            raise ValueError("allocator state belongs to another campaign")


def load_campaign_allocator(payload: Mapping[str, object]) -> AllocatorState:
    """Validate the operational allocator singleton without creating a registry."""
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported campaign allocator schema")
    if payload.get("kind") != "runtime.id_allocator":
        raise ValueError("allocator payload has an invalid kind")
    campaign_id = payload.get("campaign_id")
    counters = payload.get("counters")
    if not isinstance(campaign_id, str) or not campaign_id:
        raise ValueError("allocator payload has no campaign id")
    if not isinstance(counters, Mapping):
        raise ValueError("allocator payload has invalid counters")
    typed_counters: dict[str, int] = {}
    for family_key, counter in counters.items():
        if not isinstance(family_key, str) or not isinstance(counter, int) or counter < 0:
            raise ValueError("allocator counter is invalid")
        typed_counters[family_key] = counter
    return AllocatorState(campaign_id=campaign_id, counters=typed_counters)


def allocate_and_stage_record(
    state: AllocatorState,
    *,
    family_key: str,
    prefix: str,
    minimum_width: int,
    collision_check: Callable[[str], bool],
) -> tuple[str, AllocatorState]:
    """Allocate one collision-free campaign ID and return a new staged owner state."""
    if not family_key or not prefix or minimum_width < 1:
        raise ValueError("invalid allocator request")
    next_counter = state.counters.get(family_key, 0)
    while True:
        next_counter += 1
        candidate = f"{prefix}-{next_counter:0{minimum_width}d}"
        if not collision_check(candidate):
            break
    counters = dict(state.counters)
    counters[family_key] = next_counter
    return candidate, AllocatorState(campaign_id=state.campaign_id, counters=counters)


def stage_allocator_state(state: AllocatorState) -> dict[str, object]:
    """Produce the owner-native serialization payload for one allocator singleton."""
    return {
        "schema_version": 1,
        "kind": "runtime.id_allocator",
        "campaign_id": state.campaign_id,
        "counters": dict(state.counters),
    }
