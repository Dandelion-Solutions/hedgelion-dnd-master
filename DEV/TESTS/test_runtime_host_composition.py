"""RuntimeHost composition and trust-boundary regression tests."""

from __future__ import annotations

import json
import pickle
import unittest
from collections.abc import Mapping, Sequence

import GAME.TOOLS.publication as publication_module
from GAME.TOOLS.durability import route_serialized_operation
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
    build_live_ref,
    derive_live_epoch_id,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.publication import (
    PublicationAcceptanceEvidence,
    PublicationOutcome,
    validate_owner_issued_accepted_publication,
)
from GAME.TOOLS.runtime_host import (
    FRAMEWORK_MODULE_VERSION,
    NativeOrderingStatus,
    RuntimeHostError,
    compose_runtime_host,
)

CAMPAIGN_ID = "campaign-frostfall"


def _validate_owner_publication(
    outcome: PublicationOutcome,
    *,
    campaign_id: str,
    expected_pinned_head_sha: str,
    required_operation_digests: Mapping[str, str] | None = None,
) -> PublicationAcceptanceEvidence:
    return validate_owner_issued_accepted_publication(
        outcome,
        campaign_id=campaign_id,
        expected_pinned_head_sha=expected_pinned_head_sha,
        required_operation_digests=required_operation_digests,
    )


def _candidate(candidate_id: str = "candidate-1") -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "channel": "EXPLICIT_REF",
        "owner_family": "world.scene",
        "owner_identity": [candidate_id],
        "dependencies": [],
        "payload": {"text": "bounded"},
    }


def _context_request() -> dict[str, object]:
    return {
        "profile_id": "profile.narration",
        "role": "NARRATOR",
        "purpose": "narrate",
        "subject_id": "actor.context",
        "recipient_id": "player-1",
        "campaign_id": CAMPAIGN_ID,
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
        return {
            "kind": "world.scene",
            "id": "candidate-1",
            "state": {"text": "bounded"},
        }

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


class PublicationRepository(DeploymentRepository):
    """Fixture for exact campaign publication reads."""

    def __init__(self, campaign_id: str = CAMPAIGN_ID) -> None:
        super().__init__(campaign_id)
        self.current_revision = "a" * 40
        self.current_tree = "b" * 40
        self.pin_revision_override: str | None = None
        self.records: dict[str, object] = {
            "MANIFEST.yaml": {
                "campaign_id": campaign_id,
                "campaign_name": "The Frostfall",
                "branch": "campaign/frostfall",
                "created_at": "2026-09-22T00:00:00Z",
            },
            "CAMPAIGN_CARD.yaml": {
                "campaign_id": campaign_id,
                "campaign_name": "The Frostfall",
            },
        }
        self.path_overrides: dict[str, object] = {}
        self.ancestry_relation = "EQUAL"
        self.read_exact_commit_calls: list[tuple[str, str]] = []
        self.ancestry_calls: list[tuple[str, str, str]] = []

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        self.pin_calls.append(campaign_id)
        return PinnedCampaign(
            campaign_id=self.campaign_id,
            revision=self.pin_revision_override or self.current_revision,
            tree_sha=self.current_tree,
        )

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if path in self.path_overrides:
            return self.path_overrides[path]
        if path in self.records:
            return self.records[path]
        return {"id": "obligation-1", "kind": "runtime.collaboration_obligation"}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        self.read_exact_commit_calls.append((campaign_ref, revision))
        return {"revision": revision}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        self.ancestry_calls.append(
            (repository_ref, ancestor_revision, descendant_revision)
        )
        return {"relation": self.ancestry_relation}


class PublicationTransport:
    """Fixture for the host-bound Connector Git-data publication capability."""

    def __init__(self, repository: PublicationRepository) -> None:
        self.repository = repository
        self.calls: list[tuple[str, object]] = []
        self.response_status = "accepted"
        self.next_head = "c" * 40
        self.reconciliation_head: str | None = None
        self.reconciliation_pin_revision: str | None = None

    def repository_identity(self) -> str:
        return "github.com/example/campaigns"

    def resolve_authenticated_acting_principal(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> object:
        from GAME.TOOLS.policy_basis import AuthenticatedPrincipalEvidence

        return AuthenticatedPrincipalEvidence("principal-1")

    def read_ref(self, target_ref: str) -> object:
        self.calls.append(("read_ref", target_ref))
        return {"head_sha": self.repository.current_revision}

    def create_tree(self, base_tree_sha: str, path_operations: object) -> object:
        self.calls.append(("create_tree", path_operations))
        return "d" * 40

    def create_commit(self, parent_sha: str, tree_sha: str, target_ref: str) -> object:
        self.calls.append(("create_commit", (parent_sha, tree_sha, target_ref)))
        return self.next_head

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        self.calls.append(("update_ref", (target_ref, new_commit_sha, force)))
        if self.response_status == "indeterminate":
            self.repository.current_revision = (
                self.reconciliation_head or new_commit_sha
            )
            self.repository.pin_revision_override = self.reconciliation_pin_revision
        return {
            "status": self.response_status,
            "head_sha": new_commit_sha if self.response_status != "rejected" else None,
            "dispatched": True,
        }


def _publication_payload() -> dict[str, object]:
    return {"id": "obligation-1", "kind": "runtime.collaboration_obligation"}


def _publication_delta() -> tuple[dict[str, object], dict[str, object]]:
    payload = _publication_payload()
    route = route_native_record("runtime.collaboration_obligation", ("obligation-1",))
    return payload, {route.relative_path: payload}


def _semantic_event(event_id: str, ordinal: int) -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": event_id,
        "semantic_order": ordinal,
        "kind": "event.context",
        "provenance_refs": ["resolution.context"],
        "semantic_delta": {"state": "native"},
    }


class LocalEventRepository(PublicationRepository):
    def __init__(self) -> None:
        super().__init__()
        first_route = route_native_record("runtime.semantic_event", ("event-1",))
        second_route = route_native_record("runtime.semantic_event", ("event-2",))
        self.records.update(
            {
                "MANIFEST.yaml": {
                    "campaign_id": CAMPAIGN_ID,
                    "campaign_name": "The Frostfall",
                    "branch": "campaign/frostfall",
                    "created_at": "2026-09-22T00:00:00Z",
                },
                "INDEX/EVENT_INDEX.yaml": {
                    "schema_version": 1,
                    "entity_type": "EVENT",
                    "complete": True,
                    "upper_ordinal": 2,
                    "entries": [
                        {
                            "event_id": "event-1",
                            "ordinal": 1,
                            "path": first_route.relative_path,
                        },
                        {
                            "event_id": "event-2",
                            "ordinal": 2,
                            "path": second_route.relative_path,
                        },
                    ],
                },
                first_route.relative_path: _semantic_event("event-1", 1),
                second_route.relative_path: _semantic_event("event-2", 2),
            }
        )
        self.read_paths: list[str] = []

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        self.read_paths.append(path)
        return self.records[path]


class LiveEventTransport(DeploymentLiveTransport):
    def __init__(self) -> None:
        super().__init__()
        opening_revision = "e" * 40
        claims = (LiveClaim.exact_owner("world.scene", "scene-1"),)
        epoch_id = derive_live_epoch_id(
            CAMPAIGN_ID, "scene-1", opening_revision, claims
        )
        source_ref = build_live_ref(CAMPAIGN_ID, "scene-1", epoch_id)
        self.source = LiveEnvelope(
            campaign_id=CAMPAIGN_ID,
            scene_id="scene-1",
            epoch_id=epoch_id,
            source_ref=source_ref,
            source_revision="f" * 40,
            claims=claims,
            opening_campaign_revision=opening_revision,
        )
        self.pack = LiveNativeStatePack(
            source_key=self.source.source_key,
            source_revision=self.source.source_revision,
            next_source_native_creation_ordinal=1,
            source_native_ids=(),
            native_owner_states={
                "runtime.semantic_event": {
                    "complete": True,
                    "upper_ordinal": 1,
                    "entries": [
                        {
                            "event_id": "live-event-1",
                            "ordinal": 1,
                            "event_record": _semantic_event("live-event-1", 1),
                        }
                    ],
                }
            },
            provenance={},
            privacy={},
            chronology={},
            unresolved_work={},
        )

    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        self.read_calls.append((campaign_id, pinned))
        return LiveRouting(campaign_id=CAMPAIGN_ID, entries=(self.source,))

    def read_selected_live_source(
        self, route: LiveRouting, source: LiveEnvelope
    ) -> object:
        self.read_calls.append(("source", source))  # type: ignore[arg-type]
        return self.pack


class CountingSequence(Sequence[object]):
    """Sequence fixture that exposes unbounded enrollment enumeration."""

    def __init__(self, values: list[object]) -> None:
        self._values = values
        self.accesses = 0

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> object:
        self.accesses += 1
        return self._values[index]


class OversizedLiveEventTransport(LiveEventTransport):
    def __init__(self) -> None:
        super().__init__()
        entries = CountingSequence(
            [
                {
                    "event_id": f"live-event-{ordinal}",
                    "ordinal": ordinal,
                    "event_record": _semantic_event(f"live-event-{ordinal}", ordinal),
                }
                for ordinal in range(1, 1002)
            ]
        )
        self.oversized_entries = entries
        owner_states = dict(self.pack.native_owner_states)
        owner_states["runtime.semantic_event"] = {
            "complete": True,
            "upper_ordinal": 1001,
            "entries": entries,
        }
        self.pack = self.pack.as_mapping() | {"native_owner_states": owner_states}


class StaleLiveTransport(DeploymentLiveTransport):
    def read_selected_live(
        self, campaign_id: str, pinned: PinnedCampaign
    ) -> LiveRouting:
        self.read_calls.append((campaign_id, pinned))
        return LiveRouting(campaign_id="campaign-other", entries=())


def _compose(
    repository: DeploymentRepository | None = None,
    live: DeploymentLiveTransport | None = None,
    publication: PublicationTransport | None = None,
):
    repository = repository or DeploymentRepository()
    live = live or DeploymentLiveTransport()
    return (
        compose_runtime_host(
            CAMPAIGN_ID,
            repository,
            live,
            campaign_publication_transport=publication,
        ),
        repository,
        live,
    )


class RuntimeHostCompositionTests(unittest.TestCase):
    def test_new_runtime_host_starts_at_current_engine_module_line(self) -> None:
        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.9")

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
            host.history.read(repository=repository)
        with self.assertRaises(TypeError):
            host.history.read(live_transport=live)
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

    def test_publication_requires_the_same_read_and_write_repository_identity(
        self,
    ) -> None:
        class MismatchedRepository(PublicationRepository):
            def repository_identity(self) -> str:
                return "github.com/example/other-campaigns"

        repository = MismatchedRepository()
        with self.assertRaises(RuntimeHostError):
            _compose(repository, publication=PublicationTransport(repository))

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

        with self.assertRaises(ValueError):
            host.context.assemble(request, [candidate])
        self.assertEqual(repository.pin_calls, [CAMPAIGN_ID])
        self.assertEqual(len(live.read_calls), 1)

    def test_host_capabilities_are_not_serializable_or_persistable(self) -> None:
        host, _repository, _live = _compose()

        with self.assertRaises(TypeError):
            pickle.dumps(host)
        with self.assertRaises(TypeError):
            json.dumps(host)

    def test_campaign_publication_is_a_bound_sibling_and_uses_one_non_force_write(
        self,
    ) -> None:
        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        host, _repository, _live = _compose(repository, publication=transport)
        payload, path_operations = _publication_delta()
        publication = getattr(host, "publication", None)
        self.assertIsNotNone(publication)
        if publication is None:
            return

        outcome = publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )

        self.assertEqual(outcome.kind, "accepted")
        self.assertIsInstance(outcome, publication_module.PublicationOutcome)
        evidence = _validate_owner_publication(
            outcome,
            campaign_id=CAMPAIGN_ID,
            expected_pinned_head_sha="a" * 40,
        )
        self.assertEqual(evidence.kind.value, "CONFIRMED_REF")
        self.assertEqual(evidence.attempt.campaign_id, CAMPAIGN_ID)
        self.assertEqual(evidence.attempt.pinned_head_sha, "a" * 40)
        self.assertIsNone(evidence.current_closure)
        self.assertIsNone(evidence.ancestry)
        digests = evidence.attempt.publication_operation_digests()
        path, digest = next(iter(digests.items()))
        self.assertIs(
            _validate_owner_publication(
                outcome,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
                required_operation_digests={path: digest},
            ),
            evidence,
        )
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                outcome,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
                required_operation_digests={path: "0" * 64},
            )
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                outcome,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
                required_operation_digests={"unowned/path": digest},
            )
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                outcome,
                campaign_id="campaign-other",
                expected_pinned_head_sha="a" * 40,
            )
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                outcome,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="f" * 40,
            )
        copied_outcome = publication_module.PublicationOutcome(
            outcome.status,
            outcome.intended_commit_sha,
            outcome.observed_head_sha,
            outcome.cause,
            outcome.dispatched,
            outcome.retry_with_force,
        )
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                copied_outcome,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
            )
        self.assertEqual(
            [name for name, _value in transport.calls],
            ["create_tree", "read_ref", "create_commit", "update_ref"],
        )
        self.assertEqual(transport.calls[-1][1][2], False)  # type: ignore[index]
        self.assertFalse(hasattr(host, "campaign_publication_transport"))
        self.assertFalse(hasattr(publication, "publish_campaign_closure"))

    def test_indeterminate_publication_reconciles_without_a_second_write(self) -> None:
        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        transport.response_status = "indeterminate"
        host, _repository, _live = _compose(repository, publication=transport)
        payload, path_operations = _publication_delta()
        publication = getattr(host, "publication", None)
        self.assertIsNotNone(publication)
        if publication is None:
            return

        outcome = publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )

        self.assertEqual(outcome.kind, "accepted")
        evidence = _validate_owner_publication(
            outcome,
            campaign_id=CAMPAIGN_ID,
            expected_pinned_head_sha="a" * 40,
        )
        self.assertEqual(evidence.kind.value, "RECONCILED_CURRENT_CLOSURE")
        self.assertEqual(evidence.current_closure.base_revision, "a" * 40)
        self.assertEqual(evidence.current_closure.head_sha, outcome.intended_commit_sha)
        self.assertIsNone(evidence.ancestry)
        self.assertEqual(
            dict(evidence.current_closure.operation_digests),
            evidence.attempt.publication_operation_digests(),
        )
        self.assertEqual(
            [name for name, _value in transport.calls].count("update_ref"), 1
        )
        self.assertEqual(
            [name for name, _value in transport.calls].count("read_ref"), 2
        )

    def test_ancestor_reconciliation_retains_the_bound_closure_and_ancestry_proofs(
        self,
    ) -> None:
        repository = PublicationRepository()
        repository.ancestry_relation = "ANCESTOR"
        transport = PublicationTransport(repository)
        transport.response_status = "indeterminate"
        transport.reconciliation_head = "e" * 40
        host, _repository, _live = _compose(repository, publication=transport)
        payload, path_operations = _publication_delta()

        outcome = host.publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )

        evidence = _validate_owner_publication(
            outcome,
            campaign_id=CAMPAIGN_ID,
            expected_pinned_head_sha="a" * 40,
        )
        self.assertEqual(outcome.kind, "accepted")
        self.assertEqual(outcome.observed_head_sha, "e" * 40)
        self.assertEqual(evidence.kind.value, "RECONCILED_ANCESTOR_CURRENT_CLOSURE")
        self.assertEqual(evidence.current_closure.base_revision, "a" * 40)
        self.assertEqual(evidence.current_closure.head_sha, "e" * 40)
        self.assertEqual(evidence.ancestry.ancestor_sha, outcome.intended_commit_sha)
        self.assertEqual(evidence.ancestry.descendant_sha, "e" * 40)
        self.assertEqual(
            evidence.attempt.campaign_id,
            CAMPAIGN_ID,
        )
        self.assertEqual(repository.pin_calls, [CAMPAIGN_ID, CAMPAIGN_ID])
        self.assertEqual(
            repository.read_exact_commit_calls,
            [("campaign/frostfall", "e" * 40)],
        )
        self.assertEqual(
            repository.ancestry_calls,
            [("campaign/frostfall", outcome.intended_commit_sha, "e" * 40)],
        )
        self.assertEqual(
            [name for name, _value in transport.calls].count("update_ref"), 1
        )
        self.assertEqual(
            [name for name, _value in transport.calls].count("read_ref"), 2
        )

    def test_nonaccepted_publication_results_do_not_have_owner_issued_evidence(
        self,
    ) -> None:
        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        transport.response_status = "rejected"
        host, _repository, _live = _compose(repository, publication=transport)
        payload, path_operations = _publication_delta()
        rejected = host.publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )
        self.assertEqual(rejected.kind, "rejected")
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                rejected,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
            )

        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        transport.response_status = "indeterminate"
        route = route_native_record(
            "runtime.collaboration_obligation", ("obligation-1",)
        ).relative_path
        repository.path_overrides[route] = {
            "id": "obligation-1",
            "kind": "runtime.collaboration_obligation",
            "changed": True,
        }
        host, _repository, _live = _compose(repository, publication=transport)
        conflicting = host.publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )
        self.assertEqual(conflicting.kind, "conflict")
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                conflicting,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
            )

        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        transport.response_status = "indeterminate"
        transport.reconciliation_pin_revision = "f" * 40
        host, _repository, _live = _compose(repository, publication=transport)
        unresolved = host.publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
        )
        self.assertEqual(unresolved.kind, "indeterminate")
        with self.assertRaises(ValueError):
            _validate_owner_publication(
                unresolved,
                campaign_id=CAMPAIGN_ID,
                expected_pinned_head_sha="a" * 40,
            )

    def test_publication_rejects_an_intervening_ref_against_prepared_host_basis(
        self,
    ) -> None:
        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        host, _repository, _live = _compose(repository, publication=transport)
        payload, path_operations = _publication_delta()
        prepared_basis = host._begin_operation()
        repository.current_revision = "f" * 40

        outcome = host.publication.publish_owner_delta(
            routed_operation=route_serialized_operation(
                "runtime.collaboration_obligation", "obligation-1", payload
            ),
            path_operations=path_operations,
            owner_generations={"runtime.collaboration_obligation": 1},
            publication_reason="collaboration-close",
            basis=prepared_basis,
        )

        self.assertEqual(outcome.kind, "conflict")
        self.assertEqual(
            [name for name, _value in transport.calls].count("update_ref"), 0
        )

    def test_publication_rejects_a_basis_from_another_runtime_host(self) -> None:
        repository = PublicationRepository()
        transport = PublicationTransport(repository)
        host, _repository, _live = _compose(repository, publication=transport)
        other_repository = PublicationRepository()
        other_transport = PublicationTransport(other_repository)
        other_host, _other_repository, _other_live = _compose(
            other_repository, publication=other_transport
        )
        payload, path_operations = _publication_delta()

        with self.assertRaises(RuntimeHostError):
            host.publication.publish_owner_delta(
                routed_operation=route_serialized_operation(
                    "runtime.collaboration_obligation", "obligation-1", payload
                ),
                path_operations=path_operations,
                owner_generations={"runtime.collaboration_obligation": 1},
                publication_reason="collaboration-close",
                basis=other_host._begin_operation(),
            )

    def test_local_semantic_events_use_index_and_exact_known_ids_not_aggregate_log(
        self,
    ) -> None:
        repository = LocalEventRepository()
        host, _repository, _live = _compose(repository)
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        window = semantic_events.read_local_evt_window(
            lower_exclusive_ordinal=None, max_items=2
        )

        self.assertEqual(window.__class__.__name__, "EvtSourceWindow")
        self.assertEqual(window.origin, "LOCAL")
        self.assertEqual(
            [entry["event_id"] for entry in window.entries], ["event-1", "event-2"]
        )
        self.assertIn("INDEX/EVENT_INDEX.yaml", repository.read_paths)
        self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)
        self.assertEqual(
            repository.read_paths,
            [
                "MANIFEST.yaml",
                "INDEX/EVENT_INDEX.yaml",
                route_native_record(
                    "runtime.semantic_event", ("event-1",)
                ).relative_path,
                route_native_record(
                    "runtime.semantic_event", ("event-2",)
                ).relative_path,
            ],
        )

    def test_local_semantic_events_reject_missing_enrollment_completion_proof(
        self,
    ) -> None:
        repository = LocalEventRepository()
        index = repository.records["INDEX/EVENT_INDEX.yaml"]
        self.assertIsInstance(index, dict)
        if not isinstance(index, dict):
            return
        incomplete_index = dict(index)
        incomplete_index.pop("complete", None)
        incomplete_index.pop("upper_ordinal", None)
        repository.records["INDEX/EVENT_INDEX.yaml"] = incomplete_index
        host, _repository, _live = _compose(repository)
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        with self.assertRaises(RuntimeHostError):
            semantic_events.read_local_evt_window(
                lower_exclusive_ordinal=None, max_items=2
            )

    def test_local_semantic_events_reject_explicitly_incomplete_enrollment(
        self,
    ) -> None:
        repository = LocalEventRepository()
        index = repository.records["INDEX/EVENT_INDEX.yaml"]
        self.assertIsInstance(index, dict)
        if not isinstance(index, dict):
            return
        repository.records["INDEX/EVENT_INDEX.yaml"] = index | {"complete": False}
        host, _repository, _live = _compose(repository)
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        with self.assertRaises(RuntimeHostError):
            semantic_events.read_local_evt_window(
                lower_exclusive_ordinal=None, max_items=2
            )

    def test_local_semantic_events_reject_false_bounded_completion_claim(self) -> None:
        repository = LocalEventRepository()
        index = repository.records["INDEX/EVENT_INDEX.yaml"]
        self.assertIsInstance(index, dict)
        if not isinstance(index, dict):
            return
        repository.records["INDEX/EVENT_INDEX.yaml"] = index | {
            "complete": True,
            "upper_ordinal": 1,
        }
        host, _repository, _live = _compose(repository)
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        with self.assertRaises(RuntimeHostError):
            semantic_events.read_local_evt_window(
                lower_exclusive_ordinal=None, max_items=2
            )

    def test_selected_live_semantic_events_use_exact_source_pack_without_campaign_fallback(
        self,
    ) -> None:
        repository = PublicationRepository()
        live = LiveEventTransport()
        host, _repository, _live = _compose(repository, live)
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        window = semantic_events.read_selected_live_evt_window(
            origin=f"LIVE:{live.source.epoch_id}",
            lower_exclusive_ordinal=None,
            max_items=1,
        )

        self.assertEqual(window.source_ref, live.source.source_ref)
        self.assertEqual(window.source_revision, live.source.source_revision)
        self.assertEqual(window.entries[0]["event_id"], "live-event-1")
        self.assertFalse(hasattr(semantic_events, "read_exact_path"))

    def test_missing_selected_live_source_does_not_fall_back_to_local(self) -> None:
        host, _repository, _live = _compose()
        semantic_events = getattr(host, "semantic_events", None)
        self.assertIsNotNone(semantic_events)
        if semantic_events is None:
            return

        with self.assertRaises(RuntimeHostError):
            semantic_events.read_selected_live_evt_window(
                origin="LIVE:e1-" + "0" * 64,
                lower_exclusive_ordinal=None,
                max_items=1,
            )

    def test_oversized_local_enrollment_reads_only_the_requested_bounded_window(
        self,
    ) -> None:
        repository = LocalEventRepository()
        index = repository.records["INDEX/EVENT_INDEX.yaml"]
        self.assertIsInstance(index, dict)
        if not isinstance(index, dict):
            return
        oversized_entries = CountingSequence(
            [
                {
                    "event_id": f"event-{ordinal}",
                    "ordinal": ordinal,
                    "path": route_native_record(
                        "runtime.semantic_event", (f"event-{ordinal}",)
                    ).relative_path,
                }
                for ordinal in range(1, 1002)
            ]
        )
        repository.records["INDEX/EVENT_INDEX.yaml"] = index | {
            "upper_ordinal": 1001,
            "entries": oversized_entries,
        }
        host, _repository, _live = _compose(repository)

        window = host.semantic_events.read_local_evt_window(
            lower_exclusive_ordinal=None, max_items=1
        )

        self.assertEqual(len(window.entries), 1)
        self.assertEqual(window.entries[0]["event_id"], "event-1")
        self.assertEqual(oversized_entries.accesses, 1)
        self.assertEqual(
            repository.read_paths,
            [
                "MANIFEST.yaml",
                "INDEX/EVENT_INDEX.yaml",
                route_native_record(
                    "runtime.semantic_event", ("event-1",)
                ).relative_path,
            ],
        )

    def test_oversized_live_pack_reads_only_the_requested_bounded_window(
        self,
    ) -> None:
        live = OversizedLiveEventTransport()
        host, _repository, _live = _compose(live=live)

        window = host.semantic_events.read_selected_live_evt_window(
            origin=f"LIVE:{live.source.epoch_id}",
            lower_exclusive_ordinal=None,
            max_items=1,
        )

        self.assertEqual(len(window.entries), 1)
        self.assertEqual(window.entries[0]["event_id"], "live-event-1")
        self.assertEqual(live.oversized_entries.accesses, 1)


if __name__ == "__main__":
    unittest.main()
