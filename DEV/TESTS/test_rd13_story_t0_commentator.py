from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from GAME.TOOLS import story as story_module
from GAME.TOOLS.commentator import (
    CommentatorContractError,
    build_commentator_control_projection,
    build_commentator_snapshot,
    filter_commentator_request,
)
from GAME.TOOLS.dramaturg import (
    DramaturgContractError,
    admit_dramaturg_horizon,
    rebase_dramaturg_horizon,
    validate_dramaturg_horizon,
)
from GAME.TOOLS.history import (
    FRAMEWORK_MODULE_VERSION,
    HistoryContractError,
    NativeHistoryPublication,
    append_semantic_event,
    build_t0_basis,
    recover_native_history,
    validate_semantic_event_draft,
    validate_t0_basis,
)
from GAME.TOOLS.history import (
    _issue_native_history_from_window as _issue_native_history_from_adapter_window,
)
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
from GAME.TOOLS.runtime_host import EvtSourceWindow, compose_runtime_host
from GAME.TOOLS.story import (
    StoryContractError,
    build_story_source_bundle,
    project_story_window,
    select_story_root,
    story_record_path,
    validate_story_projection,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
_TEST_EVT_HOST_TOKENS: dict[int, object] = {}


def _issue_native_history_from_window(
    source_window: object, **kwargs: object
) -> NativeHistoryPublication:
    if "_expected_host_token" not in kwargs:
        kwargs["_expected_host_token"] = _TEST_EVT_HOST_TOKENS.get(
            id(source_window), object()
        )
    return _issue_native_history_from_adapter_window(source_window, **kwargs)  # type: ignore[arg-type]


def _semantic_event() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": "event.gate_opened",
        "semantic_order": 7,
        "kind": "event.action",
        "provenance_refs": ["resolution.gate"],
        "semantic_delta": {"gate": "opened"},
    }


def _t0_basis() -> dict[str, object]:
    return {
        "schema_version": 1,
        "event_id": "event.gate_opened",
        "actor_id": "actor.guard",
        "factors": [
            {
                "owner_family": "world.knowledge",
                "factor_id": "fact.party_authorized",
                "t0_value": "epistemic.known",
                "provenance_refs": ["fact.party_authorized"],
            }
        ],
    }


_HISTORY_REVISION = "a" * 40
_LIVE_ORIGIN = "LIVE:e1-" + ("0" * 64)


def _evt_window(
    *,
    campaign_id: str = "campaign.main",
    origin: str = "LOCAL",
    source_ref: str = "refs/heads/campaign/main",
    source_revision: str = _HISTORY_REVISION,
    event: dict[str, object] | None = None,
    lower_exclusive_ordinal: int | None = 6,
    upper_ordinal: int | None = 7,
) -> EvtSourceWindow:
    if origin != "LOCAL":
        raise ValueError("test helper supports only host-issued LOCAL windows")
    total = upper_ordinal or 0
    terminal_event = _semantic_event() if event is None else event
    source_events = [
        {
            **_semantic_event(),
            "event_id": f"event-{ordinal}",
            "semantic_order": ordinal,
        }
        for ordinal in range(1, total + 1)
    ]
    if source_events:
        source_events[-1] = terminal_event
    repository = _HistoryRepository(
        campaign_id=campaign_id,
        source_ref=source_ref,
        revision=source_revision,
        events=source_events,
    )
    host = compose_runtime_host(campaign_id, repository, _HistoryLiveTransport())
    window = host.semantic_events.read_local_evt_window(
        lower_exclusive_ordinal=lower_exclusive_ordinal,
        max_items=max(1, total - (lower_exclusive_ordinal or 0)),
    )
    _TEST_EVT_HOST_TOKENS[id(window)] = host._basis_token
    return window


class _HistoryRepository:
    def __init__(
        self,
        *,
        campaign_id: str = "campaign.main",
        source_ref: str = "refs/heads/campaign/main",
        revision: str = _HISTORY_REVISION,
        events: list[dict[str, object]] | None = None,
    ) -> None:
        self.campaign_id = campaign_id
        self.source_ref = source_ref
        self.revision = revision
        if events is None:
            events = [
                {**_semantic_event(), "event_id": "event-1", "semantic_order": 1},
                {**_semantic_event(), "event_id": "event-2", "semantic_order": 2},
            ]
        entries: list[dict[str, object]] = []
        self.records: dict[str, object] = {
            "MANIFEST.yaml": {
                "campaign_id": campaign_id,
                "branch": source_ref,
            }
        }
        for ordinal, event in enumerate(events, start=1):
            event_id = event["event_id"]
            if not isinstance(event_id, str):
                raise TypeError("history fixture event id must be text")
            path = route_native_record(
                "runtime.semantic_event", (event_id,)
            ).relative_path
            entries.append({"event_id": event_id, "ordinal": ordinal, "path": path})
            self.records[path] = event
        self.records["INDEX/EVENT_INDEX.yaml"] = {
            "schema_version": 1,
            "entity_type": "EVENT",
            "complete": True,
            "upper_ordinal": len(events) if events else None,
            "entries": entries,
        }
        self.read_paths: list[str] = []

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        return PinnedCampaign(campaign_id, self.revision, "b" * 40)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        del pinned
        self.read_paths.append(path)
        return self.records[path]

    def read_exact_campaign_ref(self, campaign_id: str) -> object:
        del campaign_id
        return {}

    def read_exact_commit(self, campaign_ref: str, revision: str) -> object:
        del campaign_ref, revision
        return {}

    def compare_ancestry(
        self, repository_ref: str, ancestor_revision: str, descendant_revision: str
    ) -> object:
        del repository_ref, ancestor_revision, descendant_revision
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(
        self, campaign_ref: str, revision: str
    ) -> object:
        del campaign_ref, revision
        return {}


class _HistoryLiveTransport:
    def __init__(self) -> None:
        opening_revision = "e" * 40
        claims = (LiveClaim.exact_owner("world.scene", "scene.main"),)
        epoch_id = derive_live_epoch_id(
            "campaign.main", "scene.main", opening_revision, claims
        )
        self.source = LiveEnvelope(
            campaign_id="campaign.main",
            scene_id="scene.main",
            epoch_id=epoch_id,
            source_ref=build_live_ref("campaign.main", "scene.main", epoch_id),
            source_revision="c" * 40,
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
                            "event_record": {
                                **_semantic_event(),
                                "event_id": "live-event-1",
                                "semantic_order": 1,
                            },
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
        del pinned
        return LiveRouting(campaign_id=campaign_id, entries=(self.source,))

    def read_selected_live_source(
        self, routing: LiveRouting, source: LiveEnvelope
    ) -> LiveNativeStatePack:
        del routing
        if source.source_key != self.source.source_key:
            raise KeyError(source.source_key)
        return self.pack


def _story_projection() -> dict[str, object]:
    return {
        "schema_version": 1,
        "story_id": "E000007",
        "content": {"body": "The guard opened the gate."},
        "sources": ["event.gate_opened"],
        "t0_basis": _t0_basis(),
        "availability": {"visible_to": ["player.aria"]},
    }


class NativeHistoryAuthorityTests(unittest.TestCase):
    def test_caller_shaped_semantic_events_cannot_mint_native_history(self) -> None:
        with self.assertRaises(HistoryContractError):
            append_semantic_event([], _semantic_event())
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "provenance_refs": []})


class NativeHistoryWindowTests(unittest.TestCase):
    def test_host_history_reads_only_the_bound_semantic_event_adapter_window(
        self,
    ) -> None:
        repository = _HistoryRepository()
        host = compose_runtime_host(
            "campaign.main", repository, _HistoryLiveTransport()
        )

        publication = host.history.read()

        self.assertEqual(publication.origin, "LOCAL")
        self.assertEqual(publication.events[0].event_id, "event-1")
        self.assertIn("INDEX/EVENT_INDEX.yaml", repository.read_paths)
        self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_bound_evt_window_issues_ephemeral_history_with_admission_provenance(
        self,
    ) -> None:
        repository = _HistoryRepository()
        host = compose_runtime_host(
            "campaign.main", repository, _HistoryLiveTransport()
        )
        publication = host.history.read()

        self.assertIsInstance(publication, NativeHistoryPublication)
        self.assertEqual(publication.campaign_id, "campaign.main")
        self.assertEqual(publication.origin, "LOCAL")
        self.assertEqual(publication.source_ref, "refs/heads/campaign/main")
        self.assertEqual(publication.source_revision, _HISTORY_REVISION)
        self.assertEqual(publication.events[0].event_id, "event-1")
        self.assertEqual(publication.events[0].admission_ordinal, 1)
        self.assertEqual(publication.events[0].semantic_order, 1)

    def test_history_rejects_aggregate_or_forged_window_shapes(self) -> None:
        aggregate = {
            "campaign_id": "campaign.main",
            "events": [_semantic_event()],
        }

        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                aggregate,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window().to_mapping(),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

        adapter_window = _evt_window()
        caller_window = EvtSourceWindow(
            campaign_id=adapter_window.campaign_id,
            origin=adapter_window.origin,
            source_ref=adapter_window.source_ref,
            source_revision=adapter_window.source_revision,
            lane=adapter_window.lane,
            lower_exclusive_ordinal=adapter_window.lower_exclusive_ordinal,
            upper_ordinal=adapter_window.upper_ordinal,
            interval_complete_through_upper=adapter_window.interval_complete_through_upper,
            entries=adapter_window.entries,
        )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                caller_window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

        forged = object.__new__(EvtSourceWindow)
        original = _evt_window()
        for name in (
            "campaign_id",
            "origin",
            "source_ref",
            "source_revision",
            "lane",
            "lower_exclusive_ordinal",
            "upper_ordinal",
            "interval_complete_through_upper",
            "entries",
        ):
            object.__setattr__(forged, name, getattr(original, name))
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                forged,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

    def test_evt_window_issuance_is_bound_to_its_runtime_host(self) -> None:
        first_host = compose_runtime_host(
            "campaign.main", _HistoryRepository(), _HistoryLiveTransport()
        )
        other_host = compose_runtime_host(
            "campaign.main", _HistoryRepository(), _HistoryLiveTransport()
        )
        window = first_host.semantic_events.read_local_evt_window(
            lower_exclusive_ordinal=None, max_items=1
        )

        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_adapter_window(
                window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
                _expected_host_token=other_host._basis_token,
            )

    def test_history_uses_exact_selected_live_source_and_preserves_origin(self) -> None:
        live = _HistoryLiveTransport()
        host = compose_runtime_host("campaign.main", _HistoryRepository(), live)

        publication = host.history.read(origin=f"LIVE:{live.source.epoch_id}")

        self.assertEqual(publication.origin, f"LIVE:{live.source.epoch_id}")
        self.assertEqual(publication.source_ref, live.source.source_ref)
        self.assertEqual(publication.source_revision, live.source.source_revision)
        self.assertEqual(publication.events[0].origin, f"LIVE:{live.source.epoch_id}")
        self.assertEqual(publication.events[0].semantic_order, 1)

    def test_history_rejects_live_pack_from_wrong_source_or_revision(self) -> None:
        for field, value in (
            ("source_key", ["campaign.main", "scene.other", "foreign-epoch"]),
            ("source_revision", "d" * 40),
        ):
            with self.subTest(field=field):
                live = _HistoryLiveTransport()
                live.pack = live.pack.as_mapping() | {field: value}
                repository = _HistoryRepository()
                host = compose_runtime_host("campaign.main", repository, live)

                with self.assertRaises(HistoryContractError):
                    host.history.read(origin=f"LIVE:{live.source.epoch_id}")

                self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_missing_selected_live_history_never_falls_back_to_local(self) -> None:
        class MissingLiveTransport(_HistoryLiveTransport):
            def read_selected_live(
                self, campaign_id: str, pinned: PinnedCampaign
            ) -> LiveRouting:
                del pinned
                return LiveRouting(campaign_id=campaign_id, entries=())

        live = MissingLiveTransport()
        repository = _HistoryRepository()
        host = compose_runtime_host("campaign.main", repository, live)

        with self.assertRaises(HistoryContractError):
            host.history.read(origin=f"LIVE:{live.source.epoch_id}")

        self.assertNotIn("INDEX/EVENT_INDEX.yaml", repository.read_paths)
        self.assertNotIn("LOG/SEMANTIC_EVENTS", repository.read_paths)

    def test_history_rejects_wrong_provenance_order_schema_and_interval(self) -> None:
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(event={**_semantic_event(), "semantic_order": 8}),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(),
                campaign_id="campaign.other",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )
        with self.assertRaises(HistoryContractError):
            _issue_native_history_from_window(
                _evt_window(event={**_semantic_event(), "schema_version": 2}),
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref="refs/heads/campaign/main",
                expected_source_revision=_HISTORY_REVISION,
            )

    def test_history_rechecks_forged_gap_duplicate_and_completeness_claims(
        self,
    ) -> None:
        original = _evt_window()
        forged_windows: list[EvtSourceWindow] = []
        for entries, complete in (
            (
                (
                    original.entries[0],
                    {
                        "ordinal": 8,
                        "event_id": "event.other",
                        "event_record": {
                            **_semantic_event(),
                            "event_id": "event.other",
                            "semantic_order": 8,
                        },
                    },
                ),
                True,
            ),
            (
                (
                    original.entries[0],
                    {
                        "ordinal": 7,
                        "event_id": "event.other",
                        "event_record": {
                            **_semantic_event(),
                            "event_id": "event.other",
                        },
                    },
                ),
                True,
            ),
        ):
            forged = object.__new__(EvtSourceWindow)
            for name in (
                "campaign_id",
                "origin",
                "source_ref",
                "source_revision",
                "lane",
                "lower_exclusive_ordinal",
                "upper_ordinal",
            ):
                object.__setattr__(forged, name, getattr(original, name))
            object.__setattr__(forged, "interval_complete_through_upper", complete)
            object.__setattr__(forged, "entries", entries)
            forged_windows.append(forged)

        incomplete = object.__new__(EvtSourceWindow)
        for name in (
            "campaign_id",
            "origin",
            "source_ref",
            "source_revision",
            "lane",
            "lower_exclusive_ordinal",
            "upper_ordinal",
            "entries",
        ):
            object.__setattr__(incomplete, name, getattr(original, name))
        object.__setattr__(incomplete, "interval_complete_through_upper", False)
        forged_windows.append(incomplete)

        for forged in forged_windows:
            with (
                self.subTest(
                    entries=forged.entries,
                    complete=forged.interval_complete_through_upper,
                ),
                self.assertRaises(HistoryContractError),
            ):
                _issue_native_history_from_window(
                    forged,
                    campaign_id="campaign.main",
                    expected_origin="LOCAL",
                    expected_source_ref=original.source_ref,
                    expected_source_revision=original.source_revision,
                )

    def test_history_recovery_revalidates_ephemeral_publication_provenance(
        self,
    ) -> None:
        window = _evt_window()
        publication = _issue_native_history_from_window(
            window,
            campaign_id="campaign.main",
            expected_origin="LOCAL",
            expected_source_ref=window.source_ref,
            expected_source_revision=window.source_revision,
        )

        recovered = recover_native_history(
            publication.to_mapping(), currentness=publication.currentness
        )

        self.assertEqual(recovered.to_mapping(), publication.to_mapping())
        forged = publication.to_mapping()
        forged["origin"] = "LOCAL"  # type: ignore[index]
        forged["events"] = []  # type: ignore[index]
        with self.assertRaises(HistoryContractError):
            recover_native_history(forged, currentness=publication.currentness)

    def test_history_api_has_no_caller_adapter_override(self) -> None:
        window = _evt_window()

        with self.assertRaises(TypeError):
            _issue_native_history_from_window(  # type: ignore[call-arg]
                window,
                campaign_id="campaign.main",
                expected_origin="LOCAL",
                expected_source_ref=window.source_ref,
                expected_source_revision=window.source_revision,
                source_adapter=object(),
            )


class T0BasisTests(unittest.TestCase):
    def test_t0_basis_is_explicit_and_reconstructible_without_current_actor_state(
        self,
    ) -> None:
        basis = build_t0_basis(_semantic_event(), _t0_basis())

        self.assertEqual(basis["factors"][0]["t0_value"], "epistemic.known")
        with self.assertRaises(HistoryContractError):
            validate_t0_basis(
                {**_t0_basis(), "factors": [{"factor_id": "fact.party_authorized"}]}
            )


class StoryProjectionTests(unittest.TestCase):
    def test_story_is_a_projection_of_a_bounded_native_source_bundle(self) -> None:
        bundle = build_story_source_bundle([_semantic_event()], layer="EVENTS")
        projection = project_story_window(bundle, [_story_projection()])

        self.assertEqual(projection[0]["sources"], ["event.gate_opened"])
        self.assertEqual(bundle["events"][0]["event_id"], "event.gate_opened")

    def test_story_window_revalidates_and_rejects_forged_malformed_or_duplicate_bundle_events(
        self,
    ) -> None:
        forged_event = {**_semantic_event(), "provenance_refs": []}
        malformed_event = {"event_id": "event.gate_opened"}

        for events in (
            [forged_event],
            [malformed_event],
            [_semantic_event(), _semantic_event()],
        ):
            with self.subTest(events=events):
                with self.assertRaises(StoryContractError):
                    project_story_window({"layer": "EVENTS", "events": events}, [])


class StorySourceRegistrationTests(unittest.TestCase):
    def test_closed_registry_has_all_eight_layer_domain_lanes(self) -> None:
        registrations = story_module.STORY_SOURCE_REGISTRATIONS

        self.assertEqual(
            {
                key: (
                    value.layer,
                    value.source_domain_prefix,
                    value.lane,
                    value.requirement_policy,
                    value.cardinality_policy,
                )
                for key, value in registrations.items()
            },
            {
                "T-MSG": (
                    "TRANSCRIPT",
                    "campaign.participant_messages@",
                    "msg",
                    "MAY_OMIT",
                    "ZERO_OR_ONE_PER_CANDIDATE",
                ),
                "T-ARC": (
                    "TRANSCRIPT",
                    "campaign.transcript_archival_requests@",
                    "arc",
                    "MUST_MATERIALIZE",
                    "EXACTLY_ONE_PER_CANDIDATE",
                ),
                "E-EVT": (
                    "EVENTS",
                    "campaign.semantic_events@",
                    "evt",
                    "SOURCE_CLASSIFIED",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
                "E-REL": (
                    "EVENTS",
                    "campaign.semantic_relations@",
                    "rel",
                    "MUST_MATERIALIZE",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
                "M-SEG": (
                    "MECHANICS",
                    "campaign.mechanical_segments@",
                    "seg",
                    "SOURCE_CLASSIFIED",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
                "M-OUT": (
                    "MECHANICS",
                    "campaign.mechanical_outcomes@",
                    "out",
                    "SOURCE_CLASSIFIED",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
                "N-EVT": (
                    "NARRATIVE",
                    "campaign.semantic_events@",
                    "evt",
                    "SOURCE_CLASSIFIED",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
                "N-REL": (
                    "NARRATIVE",
                    "campaign.semantic_relations@",
                    "rel",
                    "MUST_MATERIALIZE",
                    "ONE_OR_MORE_PER_CANDIDATE",
                ),
            },
        )
        self.assertEqual(len(registrations), 8)
        self.assertTrue(
            all(
                registration.semantic_contract_generation == 1
                for registration in registrations.values()
            )
        )

    def test_candidate_identity_codecs_round_trip_and_reject_noncanonical_forms(
        self,
    ) -> None:
        examples = {
            "T-MSG": ["message-1"],
            "T-ARC": ["interaction-1", "clause-1", 2],
            "E-EVT": ["event-1"],
            "E-REL": ["runtime.semantic_event", "event-1", "assertion-1"],
            "M-SEG": ["runtime.resolution", "resolution-1", 3],
            "M-OUT": ["runtime.command", "command-1", "terminal"],
            "N-EVT": ["event-1"],
            "N-REL": ["runtime.semantic_event", "event-1", "assertion-1"],
        }
        for registration_id, identity in examples.items():
            with self.subTest(registration=registration_id):
                encoded = story_module.encode_candidate_id(registration_id, identity)
                self.assertEqual(
                    story_module.decode_candidate_id(registration_id, encoded),
                    tuple(identity),
                )

        escaped = story_module.encode_candidate_id("E-EVT", ['quote" slash/é\n\u0001'])
        self.assertEqual(escaped, '["quote\\" slash/é\\n\\u0001"]')
        self.assertEqual(
            story_module.decode_candidate_id("E-EVT", escaped),
            ('quote" slash/é\n\u0001',),
        )

        with self.assertRaises(StoryContractError):
            story_module.decode_candidate_id("E-EVT", '["event-1" ]')
        with self.assertRaises(StoryContractError):
            story_module.encode_candidate_id(
                "T-ARC", ["interaction-1", "clause-1", True]
            )

    def test_native_origin_scopes_are_byte_escaped_without_case_folding(self) -> None:
        self.assertEqual(
            story_module.story_source_domain("E-EVT", "LOCAL"),
            "campaign.semantic_events@LOCAL",
        )
        self.assertEqual(
            story_module.story_source_domain("E-EVT", "LIVE:e1-abc"),
            "campaign.semantic_events@LIVE%3Ae1-abc",
        )
        with self.assertRaises(StoryContractError):
            story_module.story_source_domain("E-EVT", "LIVE:bad space")

    def test_registration_requiredness_and_omission_codes_are_closed(self) -> None:
        registrations = story_module.STORY_SOURCE_REGISTRATIONS
        self.assertEqual(
            registrations["T-MSG"].omission_codes, ("OPTIONAL_TRANSCRIPT",)
        )
        self.assertEqual(registrations["T-ARC"].requirement_policy, "MUST_MATERIALIZE")
        self.assertEqual(registrations["E-REL"].requirement_policy, "MUST_MATERIALIZE")
        self.assertEqual(registrations["N-REL"].requirement_policy, "MUST_MATERIALIZE")
        self.assertEqual(
            registrations["E-EVT"].omission_codes, ("TECHNICAL_ONLY_EVENT",)
        )
        self.assertEqual(
            registrations["M-SEG"].omission_codes,
            ("EXECUTION_BOOKKEEPING_ONLY",),
        )
        self.assertEqual(
            registrations["M-OUT"].omission_codes, ("NO_GAMEPLAY_OUTCOME",)
        )

    def test_candidate_results_cannot_omit_required_or_rank_candidates(self) -> None:
        relation_id = story_module.encode_candidate_id(
            "E-REL", ["runtime.semantic_event", "event-1", "assertion-1"]
        )
        relation_candidate = {
            "candidate_id": relation_id,
            "requirement": "MUST_MATERIALIZE",
            "source_keys": ["relation"],
        }
        with self.assertRaises(StoryContractError):
            story_module.validate_story_candidate_result(
                "E-REL",
                "campaign.semantic_relations@LOCAL",
                relation_candidate,
                {
                    "source_domain": "campaign.semantic_relations@LOCAL",
                    "candidate_id": relation_id,
                    "outcome": "OMITTED",
                    "reason_code": "low_importance",
                },
            )

        outcome_id = story_module.encode_candidate_id(
            "M-OUT", ["runtime.resolution", "resolution-1", "terminal"]
        )
        outcome_candidate = {
            "candidate_id": outcome_id,
            "requirement": "MAY_OMIT",
            "source_keys": ["outcome"],
        }
        with self.assertRaises(StoryContractError):
            story_module.validate_story_candidate_result(
                "M-OUT",
                "campaign.mechanical_outcomes@LOCAL",
                outcome_candidate,
                {
                    "source_domain": "campaign.mechanical_outcomes@LOCAL",
                    "candidate_id": outcome_id,
                    "outcome": "OMITTED",
                    "reason_code": "uninteresting",
                },
            )
        with self.assertRaises(StoryContractError):
            story_module.validate_story_candidate_result(
                "M-OUT",
                "campaign.mechanical_outcomes@LOCAL",
                outcome_candidate,
                {
                    "source_domain": "campaign.mechanical_outcomes@LOCAL",
                    "candidate_id": outcome_id,
                    "outcome": "OMITTED",
                    "reason_code": "NO_GAMEPLAY_OUTCOME",
                },
            )
        adjudicated_zero_change = outcome_candidate | {
            "requirement": "MUST_MATERIALIZE"
        }
        self.assertEqual(
            story_module.validate_story_candidate_result(
                "M-OUT",
                "campaign.mechanical_outcomes@LOCAL",
                adjudicated_zero_change,
                {
                    "source_domain": "campaign.mechanical_outcomes@LOCAL",
                    "candidate_id": outcome_id,
                    "outcome": "MATERIALIZED",
                    "record_keys": ["miss-or-failure"],
                },
            )["outcome"],
            "MATERIALIZED",
        )

    def test_candidate_result_enforces_registration_cardinality(self) -> None:
        cases = (
            (
                "T-MSG",
                "campaign.participant_messages@LOCAL",
                story_module.encode_candidate_id("T-MSG", ["message-1"]),
                "MAY_OMIT",
            ),
            (
                "T-ARC",
                "campaign.transcript_archival_requests@LOCAL",
                story_module.encode_candidate_id(
                    "T-ARC", ["interaction-1", "clause-1", 2]
                ),
                "MUST_MATERIALIZE",
            ),
            (
                "E-EVT",
                "campaign.semantic_events@LOCAL",
                story_module.encode_candidate_id("E-EVT", ["event-1"]),
                "MUST_MATERIALIZE",
            ),
        )
        for registration_id, domain, candidate_id, requirement in cases:
            candidate = {
                "candidate_id": candidate_id,
                "requirement": requirement,
                "source_keys": ["source"],
            }
            with self.subTest(registration=registration_id, record_keys=1):
                validated = story_module.validate_story_candidate_result(
                    registration_id,
                    domain,
                    candidate,
                    {
                        "source_domain": domain,
                        "candidate_id": candidate_id,
                        "outcome": "MATERIALIZED",
                        "record_keys": ["record-1"],
                    },
                )
                self.assertEqual(validated["record_keys"], ["record-1"])

        for registration_id, domain, candidate_id, requirement in cases[:2]:
            candidate = {
                "candidate_id": candidate_id,
                "requirement": requirement,
                "source_keys": ["source"],
            }
            with (
                self.subTest(registration=registration_id, record_keys=2),
                self.assertRaises(StoryContractError),
            ):
                story_module.validate_story_candidate_result(
                    registration_id,
                    domain,
                    candidate,
                    {
                        "source_domain": domain,
                        "candidate_id": candidate_id,
                        "outcome": "MATERIALIZED",
                        "record_keys": ["record-1", "record-2"],
                    },
                )

        registration_id, domain, candidate_id, requirement = cases[2]
        self.assertEqual(
            story_module.validate_story_candidate_result(
                registration_id,
                domain,
                {
                    "candidate_id": candidate_id,
                    "requirement": requirement,
                    "source_keys": ["source"],
                },
                {
                    "source_domain": domain,
                    "candidate_id": candidate_id,
                    "outcome": "MATERIALIZED",
                    "record_keys": ["record-1", "record-2"],
                },
            )["record_keys"],
            ["record-1", "record-2"],
        )

    def test_native_identity_bindings_are_exact_for_all_registrations(self) -> None:
        transcript = _registered_story_unit("TRANSCRIPT")
        transcript["sources"]["native"]["ref"]["identity"] = [
            "message-1",
            "extra",
        ]
        transcript_selector = _registered_story_unit("TRANSCRIPT")
        transcript_selector["sources"]["native"]["ref"]["selector"] = {
            "slice": "not-a-message-owner-selector"
        }

        archive = _registered_story_unit("TRANSCRIPT")
        archive["projection_basis"] = [
            {
                "source_domain": "campaign.transcript_archival_requests@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "T-ARC", ["interaction-1", "clause-1", 2]
                    )
                ],
            }
        ]
        archive_request_ref = {
            "family": "runtime.interaction",
            "identity": ["clause-1", "interaction-1"],
            "selector": {"clause_id": "clause-1", "target_ordinal": 2},
        }
        archive["sources"]["request"] = {"ref": archive_request_ref}
        archive["payload"]["interaction_ref"] = archive_request_ref
        archive["payload"]["exact_text_ref"] = archive["sources"]["native"]["ref"]

        event = _registered_story_unit("EVENTS")
        event["sources"]["native"]["ref"]["identity"] = [
            "event.gate_opened",
            "extra",
        ]

        event_relation = _registered_story_unit("EVENTS")
        event_relation["projection_basis"] = [
            {
                "source_domain": "campaign.semantic_relations@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "E-REL", ["runtime.semantic_event", "event-1", "assertion-1"]
                    )
                ],
            }
        ]
        event_relation["sources"]["native"] = {
            "ref": {
                "family": "runtime.semantic_event",
                "identity": ["event-1", "assertion-1", "extra"],
            }
        }
        event_relation["payload"] = {"relation_source_keys": ["native"]}

        segment = _registered_story_unit("MECHANICS")
        segment["sources"]["owner"]["ref"]["identity"] = [
            "extra",
            "resolution-1",
        ]
        segment["payload"]["resolution_refs"][0]["identity"] = [
            "extra",
            "resolution-1",
        ]

        outcome = _registered_story_unit("MECHANICS")
        outcome["projection_basis"] = [
            {
                "source_domain": "campaign.mechanical_outcomes@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "M-OUT", ["runtime.resolution", "resolution-1", "terminal"]
                    )
                ],
            }
        ]
        outcome["sources"] = {
            "native": {
                "ref": {
                    "family": "runtime.resolution",
                    "identity": ["resolution-1", "extra"],
                }
            }
        }
        outcome["payload"] = {"mechanical_source_keys": ["native"]}

        narrative_event = _registered_story_unit("NARRATIVE")
        narrative_event["sources"]["native"]["ref"]["identity"] = [
            "event.gate_opened",
            "extra",
        ]

        narrative_relation = _registered_story_unit("NARRATIVE")
        narrative_relation["projection_basis"] = [
            {
                "source_domain": "campaign.semantic_relations@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "N-REL", ["runtime.semantic_event", "event-1", "assertion-1"]
                    )
                ],
            }
        ]
        narrative_relation["sources"]["native"] = {
            "ref": {
                "family": "runtime.semantic_event",
                "identity": ["event-1", "assertion-1", "extra"],
            }
        }
        narrative_relation["payload"] = {"factual_source_keys": ["native"]}

        cases = (
            ("T-MSG", transcript, "TRANSCRIPT"),
            ("T-MSG-selector", transcript_selector, "TRANSCRIPT"),
            ("T-ARC", archive, "TRANSCRIPT"),
            ("E-EVT", event, "EVENTS"),
            ("E-REL", event_relation, "EVENTS"),
            ("M-SEG", segment, "MECHANICS"),
            ("M-OUT", outcome, "MECHANICS"),
            ("N-EVT", narrative_event, "NARRATIVE"),
            ("N-REL", narrative_relation, "NARRATIVE"),
        )
        for registration_id, unit, layer in cases:
            with (
                self.subTest(registration=registration_id),
                self.assertRaises(StoryContractError),
            ):
                story_module.validate_story_unit(unit, layer=layer)

    def test_source_window_uses_domain_local_contiguous_coverage_and_cardinality(
        self,
    ) -> None:
        event_one = story_module.encode_candidate_id("E-EVT", ["event-1"])
        event_two = story_module.encode_candidate_id("E-EVT", ["event-2"])
        window = {
            "source_domain": "campaign.semantic_events@LOCAL",
            "semantic_contract_generation": 1,
            "source_basis": {
                "origin": "LOCAL",
                "lane": "evt",
                "upper": "evt:2",
                "enumeration_representation": "native-event-index-v1",
                "owner_contracts": [
                    {"family": "runtime.semantic_event", "schema_version": 1}
                ],
            },
            "expected_coverage": {"kind": "CONTIGUOUS", "through": None},
            "proposed_coverage": {"kind": "CONTIGUOUS", "through": "evt:2"},
            "candidates": [
                {
                    "candidate_id": event_one,
                    "requirement": "MUST_MATERIALIZE",
                    "source_keys": ["event_one"],
                },
                {
                    "candidate_id": event_two,
                    "requirement": "MUST_MATERIALIZE",
                    "source_keys": ["event_two"],
                },
            ],
        }

        validated = story_module.validate_story_source_window("E-EVT", window)

        self.assertEqual(len(validated["candidates"]), 2)
        self.assertEqual(validated["proposed_coverage"]["through"], "evt:2")
        duplicate = dict(window)
        duplicate["candidates"] = [window["candidates"][0], window["candidates"][0]]
        with self.assertRaises(StoryContractError):
            story_module.validate_story_source_window("E-EVT", duplicate)
        with self.assertRaises(StoryContractError):
            story_module.validate_story_source_window(
                "E-EVT",
                window | {"semantic_contract_generation": 2},
            )
        with self.assertRaises(StoryContractError):
            story_module.validate_story_source_window(
                "E-EVT",
                window
                | {"proposed_coverage": {"kind": "CONTIGUOUS", "through": "evt:3"}},
            )
        extra_field = deepcopy(window)
        extra_field["candidates"][0]["importance"] = "low"
        with self.assertRaises(StoryContractError):
            story_module.validate_story_source_window("E-EVT", extra_field)
        empty_window = window | {
            "expected_coverage": {"kind": "CONTIGUOUS", "through": "evt:2"},
            "proposed_coverage": {"kind": "CONTIGUOUS", "through": "evt:2"},
            "candidates": [],
        }
        with self.assertRaises(StoryContractError):
            story_module.validate_story_source_window("E-EVT", empty_window)


def _registered_story_unit(layer: str) -> dict[str, object]:
    story_id = {
        "TRANSCRIPT": "T000001",
        "EVENTS": "E000001",
        "MECHANICS": "M000001",
        "NARRATIVE": "N000001",
    }[layer]
    source_family, source_id = {
        "TRANSCRIPT": ("runtime.message", "message-1"),
        "EVENTS": ("runtime.semantic_event", "event.gate_opened"),
        "MECHANICS": ("runtime.mechanical_event", "mechanical-1"),
        "NARRATIVE": ("runtime.semantic_event", "event.gate_opened"),
    }[layer]
    source_domain = {
        "TRANSCRIPT": "campaign.participant_messages@LOCAL",
        "EVENTS": "campaign.semantic_events@LOCAL",
        "MECHANICS": "campaign.mechanical_segments@LOCAL",
        "NARRATIVE": "campaign.semantic_events@LOCAL",
    }[layer]
    registration_id, candidate_identity = {
        "TRANSCRIPT": ("T-MSG", [source_id]),
        "EVENTS": ("E-EVT", [source_id]),
        "MECHANICS": ("M-SEG", ["runtime.resolution", "resolution-1", 1]),
        "NARRATIVE": ("N-EVT", [source_id]),
    }[layer]
    candidate_id = story_module.encode_candidate_id(registration_id, candidate_identity)
    payload: dict[str, object]
    if layer == "TRANSCRIPT":
        payload = {
            "message_source_key": "native",
            "speaker": {"kind": "ROLE", "role": "PLAYER"},
        }
    elif layer == "EVENTS":
        payload = {
            "event_source_keys": ["native"],
            "t0_basis": _t0_basis(),
        }
    elif layer == "MECHANICS":
        segment_selector = {
            "segment_id": "resolution-1:segment:1",
            "segment_sequence": 1,
        }
        payload = {
            "mechanical_source_keys": ["native"],
            "resolution_refs": [
                {
                    "family": "runtime.resolution",
                    "identity": ["resolution-1"],
                    "selector": segment_selector,
                }
            ],
        }
    else:
        payload = {"factual_source_keys": ["native"]}
    sources = {"native": {"ref": {"family": source_family, "identity": [source_id]}}}
    if layer == "MECHANICS":
        sources["owner"] = {
            "ref": {
                "family": "runtime.resolution",
                "identity": ["resolution-1"],
                "selector": {
                    "segment_id": "resolution-1:segment:1",
                    "segment_sequence": 1,
                },
            }
        }
    return {
        "schema_version": story_module.STORY_UNIT_SCHEMA_VERSIONS[layer],
        "story_id": story_id,
        "content": {"body": "A source-bound Story account."},
        "sources": sources,
        "projection_basis": [
            {
                "source_domain": source_domain,
                "semantic_contract_generation": 1,
                "candidate_ids": [candidate_id],
            }
        ],
        "availability": {"requires_story_refs": []},
        "payload": payload,
    }


class StoryUnitLayerTests(unittest.TestCase):
    def test_all_four_unit_contracts_validate_their_payload_and_prefix(self) -> None:
        for layer in ("TRANSCRIPT", "EVENTS", "MECHANICS", "NARRATIVE"):
            with self.subTest(layer=layer):
                unit = _registered_story_unit(layer)
                validated = story_module.validate_story_unit(unit, layer=layer)
                self.assertEqual(validated["story_id"], unit["story_id"])
                self.assertEqual(validated["payload"], unit["payload"])

    def test_payload_source_keys_must_resolve_and_layers_cannot_cross_use_ids(
        self,
    ) -> None:
        event = _registered_story_unit("EVENTS")
        event["payload"] = {"event_source_keys": ["missing"]}
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(event, layer="EVENTS")

        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(
                _registered_story_unit("EVENTS"), layer="NARRATIVE"
            )

    def test_payload_source_keys_are_bound_to_registered_native_families(self) -> None:
        wrong_families = {
            "TRANSCRIPT": "runtime.semantic_event",
            "EVENTS": "runtime.message",
            "MECHANICS": "runtime.message",
            "NARRATIVE": "runtime.message",
        }
        for layer, family in wrong_families.items():
            with self.subTest(layer=layer):
                unit = _registered_story_unit(layer)
                unit["sources"]["native"]["ref"]["family"] = family
                with self.assertRaises(StoryContractError):
                    story_module.validate_story_unit(unit, layer=layer)

    def test_archive_and_relation_registrations_bind_candidate_owner_source(
        self,
    ) -> None:
        archive = _registered_story_unit("TRANSCRIPT")
        archive["projection_basis"] = [
            {
                "source_domain": "campaign.transcript_archival_requests@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "T-ARC", ["interaction-1", "clause-1", 2]
                    )
                ],
            }
        ]
        interaction_ref = {
            "family": "runtime.interaction",
            "identity": ["interaction-1"],
            "selector": {"clause_id": "clause-1", "target_ordinal": 2},
        }
        archive["sources"]["request"] = {"ref": interaction_ref}
        archive["payload"]["interaction_ref"] = interaction_ref
        archive["payload"]["exact_text_ref"] = archive["sources"]["native"]["ref"]
        story_module.validate_story_unit(archive, layer="TRANSCRIPT")

        relation = _registered_story_unit("EVENTS")
        relation["projection_basis"] = [
            {
                "source_domain": "campaign.semantic_relations@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "E-REL", ["runtime.semantic_event", "event-1", "assertion-1"]
                    )
                ],
            }
        ]
        relation["sources"]["native"] = {
            "ref": {
                "family": "runtime.semantic_event",
                "identity": ["event-1", "assertion-1"],
            }
        }
        relation["payload"] = {"relation_source_keys": ["native"]}
        story_module.validate_story_unit(relation, layer="EVENTS")

        wrong_relation = deepcopy(relation)
        wrong_relation["sources"]["native"]["ref"]["family"] = "runtime.message"
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(wrong_relation, layer="EVENTS")

        wrong_archive = deepcopy(archive)
        wrong_archive["payload"]["interaction_ref"]["selector"]["target_ordinal"] = True
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(wrong_archive, layer="TRANSCRIPT")

    def test_event_source_family_is_checked_independently_of_optional_t0(self) -> None:
        event = _registered_story_unit("EVENTS")
        event["payload"].pop("t0_basis")
        event["sources"]["native"]["ref"]["family"] = "runtime.message"

        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(event, layer="EVENTS")

    def test_terminal_outcome_candidate_binds_its_resolution_or_command_owner(
        self,
    ) -> None:
        outcome = _registered_story_unit("MECHANICS")
        outcome["projection_basis"] = [
            {
                "source_domain": "campaign.mechanical_outcomes@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id(
                        "M-OUT", ["runtime.resolution", "resolution-1", "terminal"]
                    )
                ],
            }
        ]
        outcome["sources"] = {
            "native": {
                "ref": {
                    "family": "runtime.resolution",
                    "identity": ["resolution-1"],
                }
            }
        }
        outcome["payload"] = {"mechanical_source_keys": ["native"]}
        story_module.validate_story_unit(outcome, layer="MECHANICS")

        outcome["sources"]["native"]["ref"]["family"] = "runtime.message"
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(outcome, layer="MECHANICS")

    def test_segment_candidate_binds_exact_segment_sequence_selector(self) -> None:
        segment = _registered_story_unit("MECHANICS")
        story_module.validate_story_unit(segment, layer="MECHANICS")

        wrong_segment = deepcopy(segment)
        wrong_selector = {
            "segment_id": "resolution-1:segment:2",
            "segment_sequence": 2,
        }
        wrong_segment["sources"]["owner"]["ref"]["selector"] = wrong_selector
        wrong_segment["payload"]["resolution_refs"][0]["selector"] = wrong_selector
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(wrong_segment, layer="MECHANICS")

    def test_transcript_units_do_not_merge_distinct_message_candidates(self) -> None:
        unit = _registered_story_unit("TRANSCRIPT")
        unit["projection_basis"][0]["candidate_ids"].append(
            story_module.encode_candidate_id("T-MSG", ["message-2"])
        )

        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(unit, layer="TRANSCRIPT")

        separate_contributions = _registered_story_unit("TRANSCRIPT")
        separate_contributions["projection_basis"].append(
            {
                "source_domain": "campaign.participant_messages@LOCAL",
                "semantic_contract_generation": 1,
                "candidate_ids": [
                    story_module.encode_candidate_id("T-MSG", ["message-2"])
                ],
            }
        )
        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(separate_contributions, layer="TRANSCRIPT")

    def test_replaced_story_unit_shapes_fail_closed_after_schema_cutover(self) -> None:
        for layer in ("TRANSCRIPT", "EVENTS", "MECHANICS", "NARRATIVE"):
            old_versions = range(1, story_module.STORY_UNIT_SCHEMA_VERSIONS[layer])
            for old_version in old_versions:
                with self.subTest(layer=layer, schema_version=old_version):
                    old_unit = _registered_story_unit(layer) | {
                        "schema_version": old_version
                    }
                    with self.assertRaises(StoryContractError):
                        story_module.validate_story_unit(old_unit, layer=layer)

    def test_story_refs_use_minimum_width_canonical_decimal_encoding(self) -> None:
        noncanonical = _registered_story_unit("EVENTS") | {"story_id": "E0000001"}

        with self.assertRaises(StoryContractError):
            story_module.validate_story_unit(noncanonical, layer="EVENTS")


class StoryT0MaterializationTests(unittest.TestCase):
    def test_story_event_retains_story_local_t0_basis(self) -> None:
        projection = validate_story_projection(_story_projection(), layer="EVENTS")

        self.assertEqual(projection["t0_basis"]["event_id"], "event.gate_opened")
        self.assertNotIn("current_actor_state", projection)


class CommentatorSelfContainedTests(unittest.TestCase):
    def test_commentator_filters_hidden_story_material_before_request_materialization(
        self,
    ) -> None:
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )
        snapshot = build_commentator_snapshot([_story_projection()], control)

        self.assertEqual(
            filter_commentator_request(snapshot, "player.aria"), [_story_projection()]
        )
        self.assertEqual(filter_commentator_request(snapshot, "player.borin"), [])

    def test_commentator_rejects_an_invalid_control_projection(self) -> None:
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {
                    "schema_version": 0,
                    "controls": {"player.aria": {"story_ids": ["E000007"]}},
                },
            )

    def test_commentator_control_cannot_widen_story_availability_for_another_player(
        self,
    ) -> None:
        private_projection = _story_projection()
        private_projection["story_id"] = "E000008"
        private_projection["availability"] = {"visible_to": ["player.borin"]}
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007", "E000008"]}}
        )
        snapshot = build_commentator_snapshot(
            [_story_projection(), private_projection], control
        )

        self.assertEqual(
            filter_commentator_request(snapshot, "player.aria"), [_story_projection()]
        )


class DramaturgHorizonTests(unittest.TestCase):
    def test_dramaturg_horizon_is_provisional_and_has_no_future_fact_field(
        self,
    ) -> None:
        horizon = validate_dramaturg_horizon(
            {
                "schema_version": 1,
                "scope_id": "campaign.main",
                "generation": 1,
                "source_basis": ["event.gate_opened"],
                "entries": [
                    {
                        "kind": "PROVISIONAL_DRAMATURGIC_DIRECTION",
                        "text": "Prepare a guarded route.",
                    }
                ],
            }
        )

        self.assertEqual(horizon["generation"], 1)
        self.assertNotIn("future_fact", horizon)


class HistoryProjectionSeparationTests(unittest.TestCase):
    def test_story_validation_never_mutates_native_history(self) -> None:
        history = [_semantic_event()]
        validate_story_projection(_story_projection(), layer="EVENTS")

        self.assertEqual(history, [_semantic_event()])


class CompositeIntegrationTests(unittest.TestCase):
    def test_owner_local_chain_preserves_native_event_and_reader_safe_projection(
        self,
    ) -> None:
        history = [_semantic_event()]
        bundle = build_story_source_bundle(history, layer="EVENTS")
        projection = project_story_window(bundle, [_story_projection()])
        control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )

        self.assertEqual(
            filter_commentator_request(
                build_commentator_snapshot(projection, control), "player.aria"
            ),
            projection,
        )


class StoryStorageSelectorTests(unittest.TestCase):
    def test_story_selector_is_static_and_rejects_noncanonical_or_traversal_roots(
        self,
    ) -> None:
        self.assertEqual(select_story_root("STORY"), "STORY")
        for root in ("../STORY", "STORY/other", "ARCHIVE"):
            with self.subTest(root=root):
                with self.assertRaises(StoryContractError):
                    select_story_root(root)


class StoryPhysicalRouteTests(unittest.TestCase):
    def test_story_event_route_is_prefix_and_thousand_shard_bound(self) -> None:
        self.assertEqual(
            story_record_path("STORY", "E000007"),
            Path("STORY/EVENTS/000/E000007.yaml"),
        )
        self.assertEqual(
            story_record_path("STORY", "N003562"),
            Path("STORY/NARRATIVE/003/N003562.yaml"),
        )

        with self.assertRaises(StoryContractError):
            story_record_path("STORY", "E0000001")


class DramaturgPublicationTests(unittest.TestCase):
    def test_unadmitted_dramaturg_candidate_cannot_enter_native_history(self) -> None:
        history = [_semantic_event()]
        horizon = validate_dramaturg_horizon(
            {
                "schema_version": 1,
                "scope_id": "campaign.main",
                "generation": 1,
                "source_basis": ["event.gate_opened"],
                "entries": [],
            }
        )

        with self.assertRaises(DramaturgContractError):
            admit_dramaturg_horizon(horizon, mode="singleplayer")
        self.assertEqual(history, [_semantic_event()])


class DramaturgAdmissionTests(unittest.TestCase):
    def test_retained_horizon_requires_multiplayer_and_current_source_basis(
        self,
    ) -> None:
        horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }

        with self.assertRaises(DramaturgContractError):
            admit_dramaturg_horizon(horizon, mode="singleplayer")
        self.assertEqual(admit_dramaturg_horizon(horizon, mode="multiplayer"), horizon)


class DramaturgRebaseTests(unittest.TestCase):
    def test_rebase_rejects_incompatible_native_source_without_silent_merge(
        self,
    ) -> None:
        horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }

        with self.assertRaises(DramaturgContractError):
            rebase_dramaturg_horizon(
                horizon, current_source_basis=["event.gate_closed"]
            )


class StorySchemaTests(unittest.TestCase):
    def test_owner_local_schemas_are_strict_and_use_initial_local_versions(
        self,
    ) -> None:
        self.assertEqual(story_module.FRAMEWORK_MODULE_VERSION, "1.0.4")
        schema_names = (
            "runtime-semantic-event-state.schema.json",
            "native-history-currentness.schema.json",
            "native-history-publication.schema.json",
            "story-projection-state.schema.json",
            "story-transcript-unit.schema.json",
            "story-event-unit.schema.json",
            "story-narrative-unit.schema.json",
            "story-mechanics-unit.schema.json",
            "story-source-window.schema.json",
            "semantic-event-t0-basis.schema.json",
            "commentator-snapshot.schema.json",
            "commentator-control-projection.schema.json",
            "commentator-view.schema.json",
            "dramaturg-horizon.schema.json",
        )

        versioned_schema_names = tuple(
            name for name in schema_names if name != "story-source-window.schema.json"
        )
        schemas = [
            json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            for name in versioned_schema_names
        ]
        unit_schema_names = {
            "story-transcript-unit.schema.json",
            "story-event-unit.schema.json",
            "story-narrative-unit.schema.json",
            "story-mechanics-unit.schema.json",
        }
        for name, schema in zip(versioned_schema_names, schemas, strict=True):
            if name in unit_schema_names:
                self.assertEqual(
                    schema["allOf"][0]["$ref"],
                    "story-unit-common.schema.json#/$defs/storyUnit",
                )
            else:
                self.assertIs(schema["additionalProperties"], False)
        version_properties = {
            name: (
                schema["allOf"][1]["properties"]
                if name in unit_schema_names
                else schema["properties"]
            )
            for name, schema in zip(versioned_schema_names, schemas, strict=True)
        }
        self.assertTrue(
            all("schema_version" in props for props in version_properties.values())
        )
        common_schema = json.loads(
            (SCHEMAS / "story-unit-common.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            common_schema["$defs"]["storyUnit"]["properties"]["schema_version"]["type"],
            "integer",
        )
        for name, props in version_properties.items():
            if name not in unit_schema_names:
                self.assertEqual(props["schema_version"].get("type"), "integer")
        expected_versions = {
            "runtime-semantic-event-state.schema.json": 1,
            "native-history-currentness.schema.json": 1,
            "native-history-publication.schema.json": 1,
            "story-projection-state.schema.json": 4,
            "story-transcript-unit.schema.json": 2,
            "story-event-unit.schema.json": 3,
            "story-narrative-unit.schema.json": 3,
            "story-mechanics-unit.schema.json": 4,
            "semantic-event-t0-basis.schema.json": 1,
            "commentator-snapshot.schema.json": 1,
            "commentator-control-projection.schema.json": 1,
            "commentator-view.schema.json": 1,
            "dramaturg-horizon.schema.json": 1,
        }
        self.assertEqual(
            {
                name: props["schema_version"].get("const")
                for name, props in version_properties.items()
            },
            expected_versions,
        )

    def test_all_four_story_unit_schemas_accept_registered_envelopes(self) -> None:
        resources = Registry()
        for schema_name in (
            "story-unit-common.schema.json",
            "semantic-event-t0-basis.schema.json",
        ):
            schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
            resources = resources.with_resource(
                schema["$id"], Resource.from_contents(schema)
            )
        schema_names = {
            "TRANSCRIPT": "story-transcript-unit.schema.json",
            "EVENTS": "story-event-unit.schema.json",
            "MECHANICS": "story-mechanics-unit.schema.json",
            "NARRATIVE": "story-narrative-unit.schema.json",
        }
        for layer, schema_name in schema_names.items():
            with self.subTest(layer=layer):
                schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
                validator = Draft202012Validator(schema, registry=resources)
                unit = _registered_story_unit(layer)
                self.assertTrue(validator.is_valid(unit))
                self.assertFalse(validator.is_valid(unit | {"unregistered": True}))
                if layer == "EVENTS":
                    self.assertFalse(
                        validator.is_valid(unit | {"story_id": "E0000001"})
                    )
                if layer == "MECHANICS":
                    missing_segment_binding = deepcopy(unit)
                    missing_segment_binding["payload"].pop("resolution_refs")
                    self.assertFalse(validator.is_valid(missing_segment_binding))
                if layer == "TRANSCRIPT":
                    merged = deepcopy(unit)
                    merged["projection_basis"][0]["candidate_ids"].append(
                        story_module.encode_candidate_id("T-MSG", ["message-2"])
                    )
                    self.assertFalse(validator.is_valid(merged))
                    archive = _registered_story_unit("TRANSCRIPT")
                    archive["projection_basis"] = [
                        {
                            "source_domain": "campaign.transcript_archival_requests@LOCAL",
                            "semantic_contract_generation": 1,
                            "candidate_ids": [
                                story_module.encode_candidate_id(
                                    "T-ARC", ["interaction-1", "clause-1", 2]
                                )
                            ],
                        }
                    ]
                    archive["sources"]["request"] = {
                        "ref": {
                            "family": "runtime.interaction",
                            "identity": ["interaction-1"],
                            "selector": {
                                "clause_id": "clause-1",
                                "target_ordinal": 2,
                            },
                        }
                    }
                    archive["payload"]["interaction_ref"] = archive["sources"][
                        "request"
                    ]["ref"]
                    archive["payload"]["exact_text_ref"] = archive["sources"]["native"][
                        "ref"
                    ]
                    self.assertTrue(validator.is_valid(archive))
                    del archive["payload"]["exact_text_ref"]
                    self.assertFalse(validator.is_valid(archive))

    def test_story_source_window_schema_rejects_unknown_candidate_fields(self) -> None:
        schema = json.loads(
            (SCHEMAS / "story-source-window.schema.json").read_text(encoding="utf-8")
        )
        candidate_id = story_module.encode_candidate_id("E-EVT", ["event-1"])
        value = {
            "source_domain": "campaign.semantic_events@LOCAL",
            "semantic_contract_generation": 1,
            "source_basis": {
                "origin": "LOCAL",
                "lane": "evt",
                "upper": "evt:1",
                "enumeration_representation": "native-event-index-v1",
                "owner_contracts": [
                    {"family": "runtime.semantic_event", "schema_version": 1}
                ],
            },
            "expected_coverage": {"kind": "CONTIGUOUS", "through": None},
            "proposed_coverage": {"kind": "CONTIGUOUS", "through": "evt:1"},
            "candidates": [
                {
                    "candidate_id": candidate_id,
                    "requirement": "MUST_MATERIALIZE",
                    "source_keys": ["event"],
                }
            ],
        }
        self.assertTrue(Draft202012Validator(schema).is_valid(value))
        invalid = deepcopy(value)
        invalid["candidates"][0]["importance"] = "low"
        self.assertFalse(Draft202012Validator(schema).is_valid(invalid))

    def test_projection_state_is_layer_local_and_has_no_global_coverage_scalar(
        self,
    ) -> None:
        schema = json.loads(
            (SCHEMAS / "story-projection-state.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        state = {
            "schema_version": 4,
            "layer": "EVENTS",
            "story_id_allocator_high_water": 0,
            "coverage_by_source_domain": {},
            "lookup": {},
        }
        self.assertTrue(validator.is_valid(state))
        self.assertFalse(validator.is_valid(state | {"schema_version": 1}))
        self.assertFalse(validator.is_valid(state | {"schema_version": 2}))
        self.assertFalse(validator.is_valid(state | {"schema_version": 3}))
        self.assertFalse(validator.is_valid(state | {"global_coverage": "evt:0"}))
        self.assertFalse(
            validator.is_valid(
                state
                | {
                    "lookup": {
                        "E0000001": {
                            "entity_refs": [],
                            "source_refs": [],
                            "story_refs": [],
                        }
                    }
                }
            )
        )
        sparse_state = state | {
            "coverage_by_source_domain": {
                "campaign.semantic_events@LOCAL": {
                    "semantic_contract_generation": 1,
                    "terminal_coverage": {
                        "kind": "SPARSE",
                        "evidence": {"uncovered": ["evt:2"]},
                    },
                }
            }
        }
        self.assertFalse(validator.is_valid(sparse_state))


class SchemaVersionTests(unittest.TestCase):
    def test_history_module_starts_at_its_first_material_revision(self) -> None:
        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.3")

    def test_owner_native_python_ingress_accepts_only_actual_integer_one(self) -> None:
        valid_horizon = {
            "schema_version": 1,
            "scope_id": "campaign.main",
            "generation": 1,
            "source_basis": ["event.gate_opened"],
            "entries": [],
        }
        valid_control = build_commentator_control_projection(
            {"player.aria": {"story_ids": ["E000007"]}}
        )
        valid_snapshot = build_commentator_snapshot(
            [_story_projection()], valid_control
        )

        self.assertEqual(
            validate_semantic_event_draft(_semantic_event())["schema_version"], 1
        )
        self.assertEqual(validate_t0_basis(_t0_basis())["schema_version"], 1)
        self.assertEqual(
            validate_story_projection(_story_projection(), layer="EVENTS")[
                "schema_version"
            ],
            1,
        )
        self.assertEqual(
            build_commentator_snapshot([_story_projection()], valid_control)[
                "schema_version"
            ],
            1,
        )
        self.assertEqual(
            filter_commentator_request(valid_snapshot, "player.aria"),
            [_story_projection()],
        )
        self.assertEqual(validate_dramaturg_horizon(valid_horizon)["schema_version"], 1)

        invalid_versions: tuple[object, ...] = (1.0, True, "1", None, 2)
        for version in invalid_versions:
            with self.subTest(version=version, ingress="semantic event"):
                with self.assertRaises(HistoryContractError):
                    validate_semantic_event_draft(
                        {**_semantic_event(), "schema_version": version}
                    )
            with self.subTest(version=version, ingress="T0 basis"):
                with self.assertRaises(HistoryContractError):
                    validate_t0_basis({**_t0_basis(), "schema_version": version})
            with self.subTest(version=version, ingress="Story projection"):
                with self.assertRaises(StoryContractError):
                    validate_story_projection(
                        {**_story_projection(), "schema_version": version},
                        layer="EVENTS",
                    )
            with self.subTest(version=version, ingress="Commentator control"):
                with self.assertRaises(CommentatorContractError):
                    build_commentator_snapshot(
                        [_story_projection()],
                        {
                            "schema_version": version,
                            "controls": {"player.aria": {"story_ids": []}},
                        },
                    )
            with self.subTest(version=version, ingress="Commentator snapshot"):
                with self.assertRaises(CommentatorContractError):
                    filter_commentator_request(
                        {**valid_snapshot, "schema_version": version}, "player.aria"
                    )
            with self.subTest(version=version, ingress="Dramaturg horizon"):
                with self.assertRaises(DramaturgContractError):
                    validate_dramaturg_horizon(
                        {**valid_horizon, "schema_version": version}
                    )

    def test_draft_2020_12_structural_validation_accepts_numeric_one_point_zero(
        self,
    ) -> None:
        schema = json.loads(
            (SCHEMAS / "runtime-semantic-event-state.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertTrue(
            Draft202012Validator(schema).is_valid(
                {**_semantic_event(), "schema_version": 1.0}
            )
        )

    def test_owner_local_validators_reject_noninteger_schema_version_one_point_zero(
        self,
    ) -> None:
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "schema_version": 1.0})
        with self.assertRaises(HistoryContractError):
            validate_t0_basis({**_t0_basis(), "schema_version": 1.0})
        with self.assertRaises(StoryContractError):
            validate_story_projection(
                {**_story_projection(), "schema_version": 1.0}, layer="EVENTS"
            )
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {
                    "schema_version": 1.0,
                    "controls": {"player.aria": {"story_ids": ["E000007"]}},
                },
            )
        snapshot = build_commentator_snapshot(
            [_story_projection()],
            build_commentator_control_projection(
                {"player.aria": {"story_ids": ["E000007"]}}
            ),
        )
        with self.assertRaises(CommentatorContractError):
            filter_commentator_request(
                {**snapshot, "schema_version": 1.0}, "player.aria"
            )
        with self.assertRaises(DramaturgContractError):
            validate_dramaturg_horizon(
                {
                    "schema_version": 1.0,
                    "scope_id": "campaign.main",
                    "generation": 1,
                    "source_basis": ["event.gate_opened"],
                    "entries": [],
                }
            )

    def test_owner_local_validators_reject_unsupported_schema_version_two(self) -> None:
        with self.assertRaises(HistoryContractError):
            validate_semantic_event_draft({**_semantic_event(), "schema_version": 2})
        with self.assertRaises(HistoryContractError):
            validate_t0_basis({**_t0_basis(), "schema_version": 2})
        with self.assertRaises(StoryContractError):
            validate_story_projection(
                {**_story_projection(), "schema_version": 2}, layer="EVENTS"
            )
        with self.assertRaises(CommentatorContractError):
            build_commentator_snapshot(
                [_story_projection()],
                {
                    "schema_version": 2,
                    "controls": {"player.aria": {"story_ids": ["E000007"]}},
                },
            )
        snapshot = build_commentator_snapshot(
            [_story_projection()],
            build_commentator_control_projection(
                {"player.aria": {"story_ids": ["E000007"]}}
            ),
        )
        with self.assertRaises(CommentatorContractError):
            filter_commentator_request({**snapshot, "schema_version": 2}, "player.aria")
        with self.assertRaises(DramaturgContractError):
            validate_dramaturg_horizon(
                {
                    "schema_version": 2,
                    "scope_id": "campaign.main",
                    "generation": 1,
                    "source_basis": ["event.gate_opened"],
                    "entries": [],
                }
            )


if __name__ == "__main__":
    unittest.main()
