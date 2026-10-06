"""Bounded P2 campaign/LIVE preparation; HOT acceptance is dependency-held."""

from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from DEV.TESTS.test_runtime_host_composition import (
    LiveEventTransport,
    LocalEventRepository,
    PublicationTransport,
    _compose,
)
from GAME.TOOLS import history
from GAME.TOOLS.current_owner import NativeOwnerRef
from GAME.TOOLS.native_storage import route_native_record

ROOT = Path(__file__).resolve().parents[2]


def request(selector="RECENT_TAIL", **values):
    assert hasattr(history, "HistoryDiscoveryRequest"), "bounded History request is missing"
    return history.HistoryDiscoveryRequest(selector=selector, max_candidates=values.pop("max_candidates", 2), **values)


def discover(host, selector="RECENT_TAIL", **values):
    assert callable(getattr(host.history, "discover", None)), "bounded History discovery is missing"
    return host.history.discover(request(selector, **values))


def nominate(repository, event_id="event-1", ref=None):
    ref = ref or {"family_key": "world.actor", "identity": ["actor-1"]}
    for entry in repository.records["INDEX/EVENT_INDEX.yaml"]["entries"]:
        if entry["event_id"] == event_id:
            entry["discovery_refs"] = [ref]
    path = route_native_record("runtime.semantic_event", (event_id,)).relative_path
    repository.records[path]["semantic_delta"]["discovery_refs"] = [ref]


def test_scaffold_and_dedicated_schema_are_complete_empty_enrollment():
    scaffold = yaml.safe_load((ROOT / "GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml").read_text())
    assert scaffold == {"schema_version": 2, "entity_type": "EVENT", "complete": True, "upper_ordinal": None, "entries": []}
    schema_path = ROOT / "GAME/SCHEMA/event_index.schema.yaml"
    assert schema_path.exists(), "dedicated event-index schema is missing"
    schema = yaml.safe_load(schema_path.read_text())
    Draft202012Validator(schema).validate(scaffold)
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(scaffold | {"prose": "not routing metadata"})


def test_campaign_discovery_reads_index_only_and_bounds_recent_tail():
    repository = LocalEventRepository()
    host, _, _ = _compose(repository)
    result = discover(host, max_candidates=1)
    assert [c.event_id for c in result.candidates] == ["event-2"]
    assert result.limit_applied
    assert result.status == "TYPED_INCOMPLETE"  # no accepted HOT producer yet
    assert result.reason == "HOT_ACCEPTANCE_DEPENDENCY_HOLD"
    assert repository.read_paths == ["MANIFEST.yaml", "INDEX/EVENT_INDEX.yaml"]
    assert result.candidates[0].admission_ordinal == 2
    assert len(result.contributing_source_bases) == 1


def test_typed_owner_nominations_exact_load_native_event_without_prose_leak():
    repository = LocalEventRepository()
    nominate(repository)
    host, _, _ = _compose(repository)
    result = discover(host, "OWNER", owner_ref=NativeOwnerRef("world.actor", ("actor-1",)))
    assert [c.event_id for c in result.candidates] == ["event-1"]
    candidate = result.candidates[0]
    assert not hasattr(candidate, "event_record")
    event = host.history.read_candidate(result, candidate)
    assert event.event_id == "event-1"
    assert history._is_owner_issued_event(event)
    assert event.source_revision == repository.current_revision


def test_unknown_owner_metadata_is_not_absence_proof():
    host, _, _ = _compose(LocalEventRepository())
    result = discover(host, "OWNER", owner_ref=NativeOwnerRef("world.actor", ("actor-1",)))
    assert not result.candidates
    assert result.status == "TYPED_INCOMPLETE"


@pytest.mark.parametrize("bound", [0, -1, True, 1001, float("inf")])
def test_finite_positive_resource_bound_is_required(bound):
    with pytest.raises(ValueError):
        request(max_candidates=bound)


@pytest.mark.parametrize("selector", ["TEXT", "REGEX", "EMBEDDING", "PREDICATE"])
def test_generic_search_selectors_are_rejected(selector):
    with pytest.raises(ValueError):
        request(selector)


def test_invalid_index_does_not_scan_bodies_but_exact_known_id_bypasses_it():
    repository = LocalEventRepository()
    repository.records["INDEX/EVENT_INDEX.yaml"]["complete"] = False
    host, _, _ = _compose(repository)
    result = discover(host)
    assert result.status == "TYPED_INCOMPLETE"
    assert not result.candidates
    assert all(not p.startswith("LOG/") for p in repository.read_paths)
    exact = discover(host, "EXACT_EVENT", event_id="event-1", origin="LOCAL")
    assert [c.event_id for c in exact.candidates] == ["event-1"]
    assert host.history.read_candidate(exact, exact.candidates[0]).event_id == "event-1"


def test_selected_live_candidates_keep_their_exact_source_basis():
    live = LiveEventTransport()
    host, _, _ = _compose(LocalEventRepository(), live)
    result = discover(host, max_candidates=3)
    assert len(result.candidates) == 3
    assert len(result.contributing_source_bases) == 2
    candidate = next(c for c in result.candidates if c.origin.startswith("LIVE:"))
    assert candidate.admission_ordinal == 1
    assert candidate.source_revision == live.source.source_revision
    event = host.history.read_candidate(result, candidate)
    assert event.event_id == "live-event-1"
    assert event.origin == candidate.origin


def test_selected_live_missing_enrollment_is_typed_incomplete_not_campaign_fallback():
    live = LiveEventTransport()
    live.pack = live.pack.as_mapping() | {"native_owner_states": {}}
    host, _, _ = _compose(LocalEventRepository(), live)
    result = discover(host, origin=f"LIVE:{live.source.epoch_id}")
    assert result.status == "TYPED_INCOMPLETE"
    assert not result.candidates


def test_exact_load_rejects_changed_pin_foreign_candidate_and_forged_nomination():
    repository = LocalEventRepository()
    nominate(repository)
    host, _, _ = _compose(repository)
    result = discover(host, "OWNER", owner_ref=NativeOwnerRef("world.actor", ("actor-1",)))
    candidate = result.candidates[0]
    foreign, _, _ = _compose(repository)
    with pytest.raises(ValueError):
        foreign.history.read_candidate(result, candidate)
    path = candidate.path
    repository.records[path]["semantic_delta"].pop("discovery_refs")
    with pytest.raises(ValueError):
        host.history.read_candidate(result, candidate)
    nominate(repository)
    repository.current_revision = "d" * 40
    with pytest.raises(ValueError):
        host.history.read_candidate(result, candidate)


def test_optional_discovery_refs_are_strict_structural_routing_metadata():
    event = LocalEventRepository().records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
    assert history.validate_semantic_event_draft(event) == event
    event["semantic_delta"]["discovery_refs"] = [{"family_key": "world.actor", "identity": ["actor-1"], "motive": "private"}]
    with pytest.raises(ValueError):
        history.validate_semantic_event_draft(event)


def test_campaign_publication_copies_event_and_index_in_same_existing_closure():
    repository = LocalEventRepository()
    transport = PublicationTransport(repository)
    host, _, _ = _compose(repository, publication=transport)
    from GAME.TOOLS.durability import route_serialized_operation
    event = deepcopy(repository.records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path])
    event.update(event_id="event-3", semantic_order=3)
    event["semantic_delta"]["discovery_refs"] = [{"family_key": "world.actor", "identity": ["actor-1"]}]
    operation = route_serialized_operation("runtime.semantic_event", "event-3", event)
    host.publication.publish_owner_delta(routed_operation=operation, path_operations={operation.relative_path: event}, owner_generations={}, publication_reason="save")
    tree_ops = next(value for name, value in transport.calls if name == "create_tree")
    assert operation.relative_path in tree_ops
    assert tree_ops["INDEX/EVENT_INDEX.yaml"]["upper_ordinal"] == 3
    serialized_index = yaml.safe_load(transport.serialized_path_bytes["INDEX/EVENT_INDEX.yaml"])
    assert serialized_index["entries"][-1]["discovery_refs"] == event["semantic_delta"]["discovery_refs"]


def test_generator_rejects_incomplete_blank_event_enrollment():
    from GAME.TOOLS import init_campaign
    files, directories = init_campaign._read_campaign_tree(ROOT / "GAME/CAMPAIGN")
    init_campaign._validate_campaign_template(files, directories)
    files["INDEX/EVENT_INDEX.yaml"] = b"schema_version: 2\nentity_type: EVENT\nentries: []\n"
    with pytest.raises(RuntimeError, match="EVENT_INDEX"):
        init_campaign._validate_campaign_template(files, directories)


def test_hot_helper_preparation_cannot_admit_raw_events_and_rollback_is_atomic():
    from GAME.TOOLS.hot_store import NativeHotStore
    with NativeHotStore(":memory:") as store:
        assert callable(getattr(store, "_stage_event_discovery_helper", None)), "derived HOT event helper preparation is missing"
        event = LocalEventRepository().records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
        with pytest.raises(ValueError, match="transaction"):
            store._stage_event_discovery_helper("campaign-frostfall", event, "a" * 40)
        with pytest.raises(RuntimeError, match="rollback probe"), store._lock, store._connection:
            store._connection.execute("BEGIN IMMEDIATE")
            store._stage_event_discovery_helper("campaign-frostfall", event, "a" * 40)
            assert store._connection.execute("SELECT count(*) FROM derived_event_discovery").fetchone()[0] == 1
            raise RuntimeError("rollback probe")
        assert store._connection.execute("SELECT count(*) FROM derived_event_discovery").fetchone()[0] == 0
        with store._lock, store._connection:
            store._connection.execute("BEGIN IMMEDIATE")
            store._stage_event_discovery_helper("campaign-frostfall", event, "a" * 40)
        snapshot = store.read_admitted_event_discovery("campaign-frostfall", 2)
        assert snapshot.entries == ()
        assert not snapshot.acceptance_integrated


@pytest.mark.parametrize("family,identity", [("world.faction", ["f"]), ("unknown", ["x"]), ("world.knowledge", ["actor-1"]), ("world.actor", ["actor-1", "extra"])])
def test_runtime_and_schema_reject_unknown_or_incomplete_discovery_ref(family, identity):
    import json
    event = LocalEventRepository().records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
    event["semantic_delta"]["discovery_refs"] = [{"family_key": family, "identity": identity}]
    with pytest.raises(ValueError):
        history.validate_semantic_event_draft(event)
    schema = json.loads((ROOT / "DEV/SCHEMAS/runtime-semantic-event-state.schema.json").read_text())
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(event)


def test_session_and_provenance_ref_selectors_are_typed_nominations_only():
    repository = LocalEventRepository()
    ref = {"family_key": "runtime.session", "identity": ["session-1"]}
    nominate(repository, ref=ref)
    host, _, _ = _compose(repository)
    for selector in ("SESSION", "SOURCE_REF"):
        result = discover(host, selector, owner_ref=NativeOwnerRef("runtime.session", ("session-1",)))
        assert [c.event_id for c in result.candidates] == ["event-1"]
        assert result.status == "TYPED_INCOMPLETE"


def test_changed_live_pin_and_prospective_pack_are_not_accepted_history():
    from dataclasses import replace
    live = LiveEventTransport()
    host, _, _ = _compose(LocalEventRepository(), live)
    result = discover(host, origin=f"LIVE:{live.source.epoch_id}")
    assert len(result.candidates) == 1
    live.source = replace(live.source, source_revision="c" * 40)
    with pytest.raises(ValueError):
        host.history.read_candidate(result, result.candidates[0])
    # The old pack cannot nominate accepted current events under the new CAS pin.
    result = discover(host, origin=f"LIVE:{live.source.epoch_id}")
    assert not result.candidates


def test_existing_event_anchor_requires_exact_body_and_bad_companion_writes_nothing():
    from GAME.TOOLS.durability import route_serialized_operation
    repository = LocalEventRepository()
    transport = PublicationTransport(repository)
    host, _, _ = _compose(repository, publication=transport)
    path = route_native_record("runtime.semantic_event", ("event-1",)).relative_path
    event = deepcopy(repository.records[path])
    event["semantic_delta"]["state"] = "forged"
    operation = route_serialized_operation("runtime.semantic_event", "event-1", event)
    with pytest.raises(ValueError):
        host.publication.publish_owner_delta(routed_operation=operation, path_operations={path: event}, owner_generations={}, publication_reason="save")
    assert transport.calls == []


@pytest.mark.parametrize(
    "json_lookalike",
    [pytest.param(True, id="integer-vs-boolean"), pytest.param(1.0, id="integer-vs-float")],
)
def test_existing_event_anchor_uses_json_typed_fingerprint_not_python_mapping_equality(
    json_lookalike,
):
    from GAME.TOOLS.durability import route_serialized_operation

    repository = LocalEventRepository()
    transport = PublicationTransport(repository)
    host, _, _ = _compose(repository, publication=transport)
    path = route_native_record("runtime.semantic_event", ("event-1",)).relative_path
    existing = deepcopy(repository.records[path])
    existing["semantic_delta"]["numeric"] = 1
    repository.records[path] = existing
    incoming = deepcopy(existing)
    incoming["semantic_delta"]["numeric"] = json_lookalike
    assert existing == incoming
    assert history._semantic_event_fingerprint(existing) != history._semantic_event_fingerprint(
        incoming
    )
    operation = route_serialized_operation("runtime.semantic_event", "event-1", incoming)

    with pytest.raises(ValueError):
        host.publication.publish_owner_delta(
            routed_operation=operation,
            path_operations={path: incoming},
            owner_generations={},
            publication_reason="save",
        )

    assert not any(
        name in {"create_tree", "create_commit", "update_ref"}
        for name, _payload in transport.calls
    )


@pytest.mark.parametrize("mutation", ["duplicate", "ordinal", "path", "upper", "body", "private-ref"])
def test_invalid_campaign_routing_metadata_is_typed_incomplete_without_body_scan(mutation):
    repository = LocalEventRepository()
    index = repository.records["INDEX/EVENT_INDEX.yaml"]
    if mutation == "duplicate":
        index["entries"][1]["event_id"] = "event-1"
    elif mutation == "ordinal":
        index["entries"][0]["ordinal"] = True
    elif mutation == "path":
        index["entries"][0]["path"] = "arbitrary/private.yaml"
    elif mutation == "upper":
        index["upper_ordinal"] = 100
    elif mutation == "body":
        index["entries"][0]["event_record"] = {"private": "not routing metadata"}
    else:
        index["entries"][0]["discovery_refs"] = [{"family_key": "world.actor", "identity": ["actor-1"], "t0_value": "private"}]
    host, _, _ = _compose(repository)
    result = discover(host)
    assert not result.candidates
    assert result.status == "TYPED_INCOMPLETE"
    assert all(not path.startswith("LOG/") for path in repository.read_paths)


def test_event_ref_family_vocabulary_and_arity_are_synchronized_between_schemas():
    import json

    from GAME.TOOLS.native_storage import FAMILY_ROOTS
    event_schema = json.loads((ROOT / "DEV/SCHEMAS/runtime-semantic-event-state.schema.json").read_text())
    event_ref = event_schema["properties"]["semantic_delta"]["properties"]["discovery_refs"]["items"]
    index_schema = yaml.safe_load((ROOT / "GAME/SCHEMA/event_index.schema.yaml").read_text())
    index_ref = index_schema["properties"]["entries"]["items"]["properties"]["discovery_refs"]["items"]
    assert event_ref == index_ref
    assert set(event_ref["properties"]["family_key"]["enum"]) == set(FAMILY_ROOTS) - {"world.faction"}


def test_surviving_helper_bytes_do_not_become_accepted_hot_history(tmp_path):
    from GAME.TOOLS.hot_store import NativeHotStore
    database = str(tmp_path / "helper.db")
    event = LocalEventRepository().records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
    with NativeHotStore(database) as store, store._lock, store._connection:
        store._connection.execute("BEGIN IMMEDIATE")
        store._stage_event_discovery_helper("campaign-frostfall", event, "a" * 40)
    with NativeHotStore(database) as restarted:
        assert restarted.read_admitted_event_discovery("campaign-frostfall", 1).entries == ()
        assert restarted.read_admitted_event_discovery("campaign-other", 1).entries == ()


def test_batch_event_publication_enrolls_every_exact_route_without_id_sorting():
    from GAME.TOOLS.durability import route_serialized_operation
    repository = LocalEventRepository()
    transport = PublicationTransport(repository)
    host, _, _ = _compose(repository, publication=transport)
    base = repository.records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
    third = deepcopy(base) | {"event_id": "z-event", "semantic_order": 3}
    fourth = deepcopy(base) | {"event_id": "a-event", "semantic_order": 4}
    anchor = route_serialized_operation("runtime.semantic_event", "z-event", third)
    fourth_path = route_native_record("runtime.semantic_event", ("a-event",)).relative_path
    host.publication.publish_owner_delta(routed_operation=anchor, path_operations={fourth_path: fourth, anchor.relative_path: third}, owner_generations={}, publication_reason="save")
    index = yaml.safe_load(transport.serialized_path_bytes["INDEX/EVENT_INDEX.yaml"])
    assert index["upper_ordinal"] == 4
    assert [entry["event_id"] for entry in index["entries"]][-2:] == ["z-event", "a-event"]


def test_exact_bypass_revalidates_the_retained_native_event_fingerprint():
    repository = LocalEventRepository()
    host, _, _ = _compose(repository)
    result = discover(host, "EXACT_EVENT", event_id="event-1", origin="LOCAL")
    candidate = result.candidates[0]
    repository.records[candidate.path]["semantic_delta"]["state"] = "changed-under-pin"
    with pytest.raises(ValueError, match="fingerprint"):
        host.history.read_candidate(result, candidate)


def test_helper_storage_requires_typed_campaign_namespace():
    from GAME.TOOLS.hot_store import NativeHotStore
    event = LocalEventRepository().records[route_native_record("runtime.semantic_event", ("event-1",)).relative_path]
    with NativeHotStore(":memory:") as store, store._lock, store._connection:
        store._connection.execute("BEGIN IMMEDIATE")
        with pytest.raises(ValueError, match="campaign"):
            store._stage_event_discovery_helper(1, event, "a" * 40)
        assert store._connection.execute("SELECT count(*) FROM derived_event_discovery").fetchone()[0] == 0


def _mixed_event_repository(entries):
    from GAME.TOOLS.live_state import LiveClaim, build_live_ref, derive_live_epoch_id

    repository = LocalEventRepository()
    template = deepcopy(
        repository.records[
            route_native_record("runtime.semantic_event", ("event-1",)).relative_path
        ]
    )
    index_entries = []
    for campaign_position, (event_id, source_origin, admission_ordinal) in enumerate(
        entries, start=1
    ):
        event = deepcopy(template)
        event["event_id"] = event_id
        event["semantic_order"] = admission_ordinal
        path = route_native_record("runtime.semantic_event", (event_id,)).relative_path
        repository.records[path] = event
        index_entry = {
            "ordinal": campaign_position,
            "event_id": event_id,
            "path": path,
            "source_origin": source_origin,
            "admission_ordinal": admission_ordinal,
        }
        if source_origin.startswith("LIVE:"):
            scene_id = f"scene-{source_origin.removeprefix('LIVE:')}"
            claims = (LiveClaim.exact_owner("world.scene", scene_id),)
            epoch_id = derive_live_epoch_id(
                repository.campaign_id, scene_id, "e" * 40, claims
            )
            source_origin = f"LIVE:{epoch_id}"
            index_entry["source_origin"] = source_origin
            source_key = [repository.campaign_id, scene_id, epoch_id]
            index_entry["native_source_binding"] = {
                "source_key": source_key,
                "source_ref": build_live_ref(*source_key),
                "source_revision": "f" * 40,
            }
        index_entries.append(index_entry)
    repository.records["INDEX/EVENT_INDEX.yaml"] = {
        "schema_version": 2,
        "entity_type": "EVENT",
        "complete": True,
        "upper_ordinal": len(index_entries) if index_entries else None,
        "entries": index_entries,
    }
    return repository


def _plain_json(value):
    from collections.abc import Mapping, Sequence

    if isinstance(value, Mapping):
        return {key: _plain_json(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_plain_json(item) for item in value]
    return value


def _revalidation_repository_state(repository, predecessor, predecessor_tree, intended, intended_tree, operations):
    predecessor_records = deepcopy(repository.records)
    repository.current_revision = intended
    repository.current_tree = intended_tree
    repository.revision_records = {
        predecessor: predecessor_records,
        intended: predecessor_records | _plain_json(operations),
    }
    repository.exact_commit_evidence = {
        predecessor: {
            "revision": predecessor,
            "tree_sha": predecessor_tree,
            "changed_paths": [],
        },
        intended: {
            "revision": intended,
            "tree_sha": intended_tree,
            "parent_revision": predecessor,
            "changed_paths": sorted(operations),
        },
    }


class RevalidationEventRepository(LocalEventRepository):
    def __init__(self):
        super().__init__()
        self.revision_records = {}

    def read_exact_path(self, pinned, path):
        self.read_paths.append(path)
        if pinned.revision in self.revision_records:
            return self.revision_records[pinned.revision][path]
        return self.records[path]


def test_batch_event_only_recovery_reconstructs_exact_companion_and_rejects_altered_one():
    from GAME.TOOLS.durability import route_serialized_operation
    from GAME.TOOLS.publication import PublicationStatus

    repository = RevalidationEventRepository()
    transport = PublicationTransport(repository)
    host, _, _ = _compose(repository, publication=transport)
    predecessor = repository.current_revision
    predecessor_tree = repository.current_tree
    base = deepcopy(
        repository.records[
            route_native_record("runtime.semantic_event", ("event-1",)).relative_path
        ]
    )
    first = deepcopy(base) | {"event_id": "z-event", "semantic_order": 3}
    second = deepcopy(base) | {"event_id": "a-event", "semantic_order": 4}
    first_path = route_native_record("runtime.semantic_event", ("z-event",)).relative_path
    second_path = route_native_record("runtime.semantic_event", ("a-event",)).relative_path
    caller_operations = {second_path: second, first_path: first}
    routed_operation = route_serialized_operation(
        "runtime.semantic_event", "z-event", first
    )

    publication = host.publication.publish_owner_delta(
        routed_operation=routed_operation,
        path_operations=caller_operations,
        owner_generations={},
        publication_reason="save",
    )

    assert publication.status is PublicationStatus.ACCEPTED
    published_operations = _plain_json(
        next(value for name, value in transport.calls if name == "create_tree")
    )
    index_path = "INDEX/EVENT_INDEX.yaml"
    assert set(published_operations) == {*caller_operations, index_path}
    intended = transport.next_head
    intended_tree = "d" * 40
    _revalidation_repository_state(
        repository,
        predecessor,
        predecessor_tree,
        intended,
        intended_tree,
        published_operations,
    )
    writes_before_recovery = [
        name
        for name, _value in transport.calls
        if name in {"create_tree", "create_commit", "update_ref"}
    ]

    recovered = host.publication.revalidate_published_owner_delta(
        routed_operation=routed_operation,
        path_operations=caller_operations,
        owner_generations={},
        publication_reason="save",
        expected_pinned_head_sha=predecessor,
        intended_commit_sha=intended,
    )

    assert recovered.status is PublicationStatus.ACCEPTED
    assert recovered.cause == "RECONCILED_CURRENT_CLOSURE"
    assert [entry["event_id"] for entry in published_operations[index_path]["entries"]][-2:] == [
        "z-event",
        "a-event",
    ]

    altered_index = deepcopy(published_operations[index_path])
    altered_index["entries"][-1]["event_id"] = "forged-event"
    altered = host.publication.revalidate_published_owner_delta(
        routed_operation=routed_operation,
        path_operations=caller_operations | {index_path: altered_index},
        owner_generations={},
        publication_reason="save",
        expected_pinned_head_sha=predecessor,
        intended_commit_sha=intended,
    )
    assert altered.status is not PublicationStatus.ACCEPTED
    assert [
        name
        for name, _value in transport.calls
        if name in {"create_tree", "create_commit", "update_ref"}
    ] == writes_before_recovery


def test_selected_live_metadata_fingerprint_is_rechecked_before_exact_issue():
    live = LiveEventTransport()
    host, _, _ = _compose(LocalEventRepository(), live)
    origin = f"LIVE:{live.source.epoch_id}"
    result = discover(host, "EXACT_EVENT", event_id="live-event-1", origin=origin)
    candidate = result.candidates[0]

    packed = deepcopy(live.pack.as_mapping())
    owner_states = packed["native_owner_states"]
    enrollment = owner_states["runtime.semantic_event"]
    second_event = {
        "schema_version": 1,
        "event_id": "live-event-2",
        "semantic_order": 2,
        "kind": "event.context",
        "provenance_refs": ["source.live"],
        "semantic_delta": {"state": "changed enrollment"},
    }
    enrollment["upper_ordinal"] = 2
    enrollment["entries"].append(
        {"ordinal": 2, "event_id": "live-event-2", "event_record": second_event}
    )
    live.pack = packed

    with pytest.raises(ValueError, match="metadata|nomination|fingerprint|revalidation"):
        host.history.read_candidate(result, candidate)


def test_copied_candidate_cannot_replace_host_issued_shortlist_carrier():
    repository = LocalEventRepository()
    nominate(repository)
    host, _, _ = _compose(repository)
    result = discover(host, "OWNER", owner_ref=NativeOwnerRef("world.actor", ("actor-1",)))
    forged_candidate = deepcopy(result.candidates[0])
    object.__setattr__(result, "candidates", (forged_candidate,))

    with pytest.raises(ValueError, match="issued|shortlist|carrier"):
        host.history.read_candidate(result, forged_candidate)


def test_replaced_data_plane_event_adapter_cannot_issue_nominated_payload():
    repository = LocalEventRepository()
    nominate(repository)
    host, _, _ = _compose(repository)
    result = discover(host, "OWNER", owner_ref=NativeOwnerRef("world.actor", ("actor-1",)))
    candidate = result.candidates[0]
    bound_adapter = host.semantic_events

    class ReplacedAdapter:
        def _read_exact_path(self, pinned, path):
            value = deepcopy(bound_adapter._read_exact_path(pinned, path))
            if path == candidate.path:
                value["semantic_delta"]["state"] = "forged by replacement"
            return value

    object.__setattr__(host, "_semantic_events", ReplacedAdapter())

    with pytest.raises(ValueError, match="adapter|bound|source|Host"):
        host.history.read_candidate(result, candidate)


def test_replaced_selected_live_transport_cannot_issue_nominated_payload():
    live = LiveEventTransport()
    host, _, _ = _compose(LocalEventRepository(), live)
    origin = f"LIVE:{live.source.epoch_id}"
    result = discover(host, "EXACT_EVENT", event_id="live-event-1", origin=origin)
    candidate = result.candidates[0]

    class ReplacedLiveTransport:
        def read_selected_live(self, campaign_id, pinned):
            return live.read_selected_live(campaign_id, pinned)

        def read_selected_live_source(self, route, source):
            return live.read_selected_live_source(route, source)

    object.__setattr__(host, "_live_transport", ReplacedLiveTransport())

    with pytest.raises(ValueError, match="transport|bound|binding|source"):
        host.history.read_candidate(result, candidate)


def test_selected_live_revalidation_detects_growth_past_complete_source_bound():
    live = LiveEventTransport()
    pack = deepcopy(live.pack.as_mapping())
    owner_states = pack["native_owner_states"]
    base_record = live.pack.native_owner_states["runtime.semantic_event"]["entries"][0][
        "event_record"
    ]
    entries = []
    for ordinal in range(1, 1001):
        event = deepcopy(base_record)
        event["event_id"] = f"live-event-{ordinal}"
        event["semantic_order"] = ordinal
        entries.append(
            {"ordinal": ordinal, "event_id": event["event_id"], "event_record": event}
        )
    owner_states["runtime.semantic_event"] = {
        "complete": True,
        "upper_ordinal": 1000,
        "entries": entries,
    }
    live.pack = pack
    host, _, _ = _compose(LocalEventRepository(), live)
    origin = f"LIVE:{live.source.epoch_id}"
    result = discover(host, "EXACT_EVENT", event_id="live-event-1", origin=origin)
    candidate = result.candidates[0]

    entries.append(
        {
            "ordinal": 1001,
            "event_id": "live-event-1001",
            "event_record": deepcopy(base_record)
            | {"event_id": "live-event-1001", "semantic_order": 1001},
        }
    )
    owner_states["runtime.semantic_event"]["upper_ordinal"] = 1001

    with pytest.raises(ValueError, match="bound|limit|metadata|nomination"):
        host.history.read_candidate(result, candidate)


def test_exact_known_id_without_surviving_origin_anchor_does_not_become_local():
    repository = LocalEventRepository()
    repository.records["INDEX/EVENT_INDEX.yaml"]["entries"] = []
    repository.records["INDEX/EVENT_INDEX.yaml"]["upper_ordinal"] = None
    host, _, _ = _compose(repository)

    result = discover(host, "EXACT_EVENT", event_id="event-1", origin="LOCAL")

    assert not result.candidates
    assert result.status == "TYPED_INCOMPLETE"


def test_local_lane_append_uses_admission_ordinal_after_absorbed_live_position():
    repository = _mixed_event_repository(
        [("local-1", "LOCAL", 1), ("live-a-1", "LIVE:epoch-a", 1)]
    )
    local_event = deepcopy(
        repository.records[
            route_native_record("runtime.semantic_event", ("local-1",)).relative_path
        ]
    )
    local_event["event_id"] = "local-2"
    local_event["semantic_order"] = 2

    after_image = history.event_index_after_image(
        repository.records["INDEX/EVENT_INDEX.yaml"], local_event
    )

    assert after_image["upper_ordinal"] == 3
    assert after_image["entries"][-1]["ordinal"] == 3
    assert after_image["entries"][-1]["source_origin"] == "LOCAL"
    assert after_image["entries"][-1]["admission_ordinal"] == 2


def test_two_absorbed_live_origins_and_local_windows_use_native_lane_coordinates():
    from GAME.TOOLS.history import read_native_history_window

    repository = _mixed_event_repository(
        [
            ("local-1", "LOCAL", 1),
            ("live-a-1", "LIVE:epoch-a", 1),
            ("local-2", "LOCAL", 2),
            ("live-b-1", "LIVE:epoch-b", 1),
        ]
    )
    host, _, _ = _compose(repository)
    index = repository.records["INDEX/EVENT_INDEX.yaml"]
    index_schema = yaml.safe_load((ROOT / "GAME/SCHEMA/event_index.schema.yaml").read_text())
    Draft202012Validator(index_schema).validate(index)
    source_origins = {
        entry["event_id"]: entry["source_origin"]
        for entry in index["entries"]
        if entry["source_origin"].startswith("LIVE:")
    }
    for event_id, origin, campaign_position in (
        ("live-a-1", source_origins["live-a-1"], 2),
        ("live-b-1", source_origins["live-b-1"], 4),
    ):
        result = discover(host, "EXACT_EVENT", event_id=event_id, origin=origin)
        assert [candidate.event_id for candidate in result.candidates] == [event_id]
        candidate = result.candidates[0]
        anchor = next(entry for entry in index["entries"] if entry["event_id"] == event_id)
        binding = anchor["native_source_binding"]
        assert candidate.origin == origin
        assert candidate.admission_ordinal == 1
        assert candidate.serving_ordinal == campaign_position
        assert candidate.source_basis.origin == "LOCAL"
        assert candidate.source_basis.campaign_revision == repository.current_revision
        assert candidate.source_ref == binding["source_ref"]
        assert candidate.source_revision == binding["source_revision"]
        exact = host.history.read_candidate(result, candidate)
        assert exact.origin == origin
        assert exact.source_ref == binding["source_ref"]
        assert exact.source_revision == binding["source_revision"]

    local_window = read_native_history_window(
        host, origin="LOCAL", lower_exclusive_ordinal=None, max_items=2
    )
    assert [event.event_id for event in local_window.events] == ["local-1", "local-2"]
    assert [event.admission_ordinal for event in local_window.events] == [1, 2]
    local_tail = read_native_history_window(
        host, origin="LOCAL", lower_exclusive_ordinal=1, max_items=1
    )
    assert [event.event_id for event in local_tail.events] == ["local-2"]
    archived_live_window = read_native_history_window(
        host, origin=source_origins["live-a-1"], lower_exclusive_ordinal=None, max_items=1
    )
    assert [event.event_id for event in archived_live_window.events] == ["live-a-1"]
    assert archived_live_window.events[0].admission_ordinal == 1


def test_absorbed_live_source_binding_must_belong_to_serving_campaign():
    from GAME.TOOLS.live_state import build_live_ref

    repository = _mixed_event_repository(
        [("live-a-1", "LIVE:epoch-a", 1)]
    )
    entry = repository.records["INDEX/EVENT_INDEX.yaml"]["entries"][0]
    binding = entry["native_source_binding"]
    foreign_source_key = ["campaign-other", *binding["source_key"][1:]]
    binding["source_key"] = foreign_source_key
    binding["source_ref"] = build_live_ref(*foreign_source_key)
    host, _, _ = _compose(repository)

    result = discover(
        host,
        "EXACT_EVENT",
        event_id="live-a-1",
        origin=entry["source_origin"],
    )

    assert not result.candidates
    assert result.status == "TYPED_INCOMPLETE"


@pytest.mark.parametrize(
    "mutation",
    ["missing-live-binding", "live-epoch-mismatch", "binding-on-local"],
)
def test_event_index_rejects_forged_or_contradictory_origin_anchors(mutation):
    repository = _mixed_event_repository(
        [("local-1", "LOCAL", 1), ("live-a-1", "LIVE:epoch-a", 1)]
    )
    index = deepcopy(repository.records["INDEX/EVENT_INDEX.yaml"])
    live_entry = index["entries"][1]
    if mutation == "missing-live-binding":
        del live_entry["native_source_binding"]
    elif mutation == "live-epoch-mismatch":
        live_entry["native_source_binding"]["source_key"][2] = "epoch-b"
    else:
        index["entries"][0]["native_source_binding"] = live_entry[
            "native_source_binding"
        ]

    with pytest.raises(ValueError, match="binding|origin|epoch"):
        history.validate_event_index(index)
