"""RuntimeHost composition and trust-boundary regression tests."""

from __future__ import annotations

import json
import pickle
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from GAME.TOOLS.live_state import LiveRouting  # noqa: I001
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.runtime_host import (
    FRAMEWORK_MODULE_VERSION,
    NativeOrderingStatus,
    RuntimeHostError,
    compose_runtime_host,
)


CAMPAIGN_ID = "campaign-frostfall"


def _candidate(candidate_id: str = "candidate-1") -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "channel": "EXPLICIT_REF",
        "current": True,
        "eligible": True,
        "dependencies": [],
        "payload": {"text": "bounded"},
    }


def _context_request() -> dict[str, object]:
    return {
        "profile_id": "profile.narration",
        "allowed_channels": ["EXPLICIT_REF"],
        "max_candidates": 2,
        "required_ids": [],
        "allowed_relations": [],
        "budget": 100,
    }


class DeploymentRepository:
    """Fixture for the authenticated deployment-supplied RepositoryPort."""

    def __init__(self, campaign_id: str = CAMPAIGN_ID) -> None:
        self.campaign_id = campaign_id
        self.pin_calls: list[str] = []

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        self.pin_calls.append(campaign_id)
        ordinal = len(self.pin_calls)
        return PinnedCampaign(
            campaign_id=self.campaign_id,
            revision=f"{ordinal:040x}",
            tree_sha=f"{ordinal + 100:040x}",
        )

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        return {"campaign_id": pinned.campaign_id, "path": path}

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        return {}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        return {}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        return {}


class DeploymentLiveTransport:
    """Fixture for the selected-LIVE reader supplied by the deployment host."""

    def __init__(self, campaign_id: str = CAMPAIGN_ID) -> None:
        self.campaign_id = campaign_id
        self.read_calls: list[tuple[str, PinnedCampaign]] = []

    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        self.read_calls.append((campaign_id, pinned))
        return LiveRouting(campaign_id=self.campaign_id, entries=())


class StaleLiveTransport(DeploymentLiveTransport):
    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        self.read_calls.append((campaign_id, pinned))
        return LiveRouting(campaign_id="campaign-other", entries=())


def _compose(
    repository: DeploymentRepository | None = None,
    live: DeploymentLiveTransport | None = None,
):
    repository = repository or DeploymentRepository()
    live = live or DeploymentLiveTransport()
    return compose_runtime_host(CAMPAIGN_ID, repository, live), repository, live


class RuntimeHostCompositionTests(unittest.TestCase):
    def test_new_runtime_host_starts_at_current_engine_module_line(self) -> None:
        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.1")

    def test_composition_binds_one_campaign_and_creates_sibling_services(self) -> None:
        host, _repository, _live = _compose()

        self.assertEqual(host.campaign_id, CAMPAIGN_ID)
        self.assertIsNot(host.context, host.history)
        self.assertIsNot(host.context, host.native_ordering)
        self.assertIsNot(host.history, host.native_ordering)
        self.assertNotIn("_context", dir(host.history))

    def test_each_operation_repins_campaign_and_rereads_selected_live(self) -> None:
        host, repository, live = _compose()

        host.context.assemble(_context_request(), [_candidate()])
        host.context.assemble(_context_request(), [_candidate("candidate-2")])
        observation = host.history.observe_first_initialization_history()
        ordering = host.native_ordering.resolve({"candidate": "untrusted"})

        self.assertIn(observation.status.value, {"UNAVAILABLE", "AMBIGUOUS"})
        self.assertEqual(ordering.status, NativeOrderingStatus.NO_ORDERED_OWNER)
        self.assertEqual(repository.pin_calls, [CAMPAIGN_ID] * 4)
        self.assertEqual(len(live.read_calls), 4)
        self.assertEqual(
            [pinned.revision for _campaign, pinned in live.read_calls],
            [f"{ordinal:040x}" for ordinal in range(1, 5)],
        )

    def test_cross_campaign_pin_or_selected_live_route_is_rejected(self) -> None:
        repository = DeploymentRepository(campaign_id="campaign-other")
        host, _repository, _live = _compose(repository=repository)

        with self.assertRaises(RuntimeHostError):
            host.native_ordering.resolve({})

        host, _repository, _live = _compose(live=StaleLiveTransport())
        with self.assertRaises(RuntimeHostError):
            host.native_ordering.resolve({})

    def test_gameplay_methods_reject_capability_and_service_overrides(self) -> None:
        host, repository, live = _compose()

        with self.assertRaises(AttributeError):
            _ = host.repository
        with self.assertRaises(AttributeError):
            _ = host.live_transport
        with self.assertRaises(AttributeError):
            _ = host.route_resolver
        with self.assertRaises(TypeError):
            host.context.assemble(
                _context_request(), [_candidate()], repository=repository
            )
        with self.assertRaises(TypeError):
            host.history.observe_first_initialization_history(repository=repository)
        with self.assertRaises(TypeError):
            host.native_ordering.resolve({}, live_transport=live)
        with self.assertRaises(AttributeError):
            host.context = object()
        with self.assertRaises(AttributeError):
            host._repository = repository

    def test_composition_requires_the_authenticated_adapter_operations(self) -> None:
        with self.assertRaises(RuntimeHostError):
            compose_runtime_host(CAMPAIGN_ID, object(), DeploymentLiveTransport())
        with self.assertRaises(RuntimeHostError):
            compose_runtime_host(CAMPAIGN_ID, DeploymentRepository(), object())

    def test_untrusted_request_data_cannot_select_or_replace_transport(self) -> None:
        host, repository, live = _compose()
        evil = object()
        request = _context_request() | {
            "repository_port": evil,
            "live_transport": evil,
            "runtime_host": evil,
            "context_service": evil,
        }
        candidate = _candidate() | {
            "repository_port": evil,
            "live_transport": evil,
            "history_service": evil,
        }

        result = host.context.assemble(request, [candidate])

        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(repository.pin_calls, [CAMPAIGN_ID])
        self.assertEqual(len(live.read_calls), 1)

    def test_host_capabilities_are_not_serializable_or_persistable(self) -> None:
        host, _repository, _live = _compose()

        with self.assertRaises(TypeError):
            pickle.dumps(host)
        with self.assertRaises(TypeError):
            json.dumps(host)


if __name__ == "__main__":
    unittest.main()
