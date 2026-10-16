"""Trusted native source conformance only; no external authentication issuance."""

import hashlib
import json
import tempfile
import unittest
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

from GAME.TOOLS import runtime_execution
from GAME.TOOLS.catalog_runtime import canonical_json, sha256
from GAME.TOOLS.durability import (
    DurabilityContractError,
    issue_durability_handoff_promise,
    route_serialized_operation,
)
from GAME.TOOLS.recovery_roots import enumerate_operational_root_page


def input_sources(*, kind="response_and_intent", creator=False):
    """Explicit retained bytes, never a verified/accepted authority fixture."""
    text = "Choose A; then move"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    authority = {
        "kind": "multiplayer", "player_id": "player-1",
        "accepted_subject_ids": ["actor-1"],
        "campaign_authority_revision": "access-1", "player_revision": 1,
        "route_evidence_revision": "route-1",
    }
    if creator:
        authority = {
            "kind": "creator_singleplayer", "accepted_subject_ids": ["actor-1"],
            "creator_history": {"author_login": "fixture-player",
                                "initialization_revision": "initial-1",
                                "parent_revision": "parent-1"},
        }
    state = {
        "schema_version": 1, "campaign_id": "campaign-1", "session_id": "session-1",
        "input_message_id": "message-9", "input_kind": kind,
        "accepted_input_basis": {
            "basis_generation": 1, "repository_identity": "fixture-repository",
            "adapter_profile_id": "fixture.input", "adapter_profile_generation": 1,
            "accepted_exchange_key": "exchange-1", "host_invocation_ref": "invocation-1",
            "principal": {"provider": "github", "stable_account_id": "123",
                          "login_at_acceptance": "fixture-player"},
            "representation": {"kind": "accepted_text", "digest_generation": 1,
                               "content_digest": digest},
            "authority_at_acceptance": authority,
        },
    }
    if not creator:
        state["player_id"] = "player-1"
    plan = None
    if kind == "intent":
        state["intent_plan_id"] = "plan-1"
        plan = {"kind": "runtime.intent_plan", "id": "plan-1", "state": {
            "schema_version": 1, "interaction_id": "interaction-1", "clauses": [
                {"schema_version": 1, "clause_kind": "intent", "clause_id": "clause-1",
                 "order": 1, "mapping_outcome": "exact", "execution_state": "intent.ready"},
            ],
        }}
    else:
        state["response_target"] = {
            "root_command_id": "command-1", "resolution_id": "resolution-1",
            "continuation_id": "continuation-1", "continuation_generation": 1,
            "offer_kind": "choice", "offer_id": "offer-1", "responder_id": "actor-1",
        }
        state["response_selection"] = {"kind": "choice", "option_id": "option-A"}
        if kind == "response_and_intent":
            state["planning_phase"] = "awaiting_response"
    interaction = {"kind": "runtime.interaction", "id": "interaction-1", "state": state}
    message = {"kind": "runtime.message", "id": "message-9", "state": {
        "schema_version": 1, "message_id": "message-9", "interaction_id": "interaction-1",
        "direction": "inbound", "input_basis_generation": 1,
        "representation_kind": "accepted_text", "payload_state": "message.exact_retained",
        "exact_text": text, "content_digest": digest,
    }}
    return interaction, message, plan


def response_survivor(interaction, message):
    """Construct a retained native marker for shape tests, not an issued consume."""
    state = interaction["state"]
    payload = {
        "response_interaction_id": interaction["id"], "response_message_id": message["id"],
        "input_kind": state["input_kind"], "accepted_input_basis": state["accepted_input_basis"],
        "target": state["response_target"], "selection": state["response_selection"],
    }
    reference = {"resolution_id": "resolution-1", "segment_id": "resolution-1:segment:1"}
    state["accepted_resume_ref"] = reference
    if state["input_kind"] == "response_and_intent":
        state["planning_phase"] = "ready_to_plan"
    marker = {"schema_version": 1, "resume_fingerprint_generation": 1,
              "resume_fingerprint": sha256(b"HDM_ACCEPTED_RESUME_INPUT/1\n" + canonical_json(payload)),
              **{key: payload[key] for key in ("response_interaction_id", "response_message_id", "target", "selection")}}
    return {"schema_version": 1, "segment_id": reference["segment_id"], "segment_sequence": 1,
            "commit_state": "committed", "resulting_execution_state": "COMPLETED",
            "event_ids": [], "pending_child_invocations": [], "receipt_exports": {}, "affected_revision_refs": [],
            "accepted_resume_input": marker}


def mixed_plan(interaction):
    state = interaction["state"]
    state["planning_phase"] = "materialized"
    state["intent_plan_id"] = "plan-1"
    return {"kind": "runtime.intent_plan", "id": "plan-1", "state": {
        "schema_version": 1, "interaction_id": interaction["id"], "clauses": [
            {"schema_version": 1, "clause_kind": "solicited_response", "clause_id": "clause.response",
             "order": 1, "mapping_outcome": "exact", "execution_state": "intent.executed",
             "accepted_resume_ref": deepcopy(state["accepted_resume_ref"])},
            {"schema_version": 1, "clause_kind": "intent", "clause_id": "clause.intent.1",
             "order": 2, "mapping_outcome": "narrative_only", "execution_state": "intent.pending",
             "collaboration_semantic_class": "OOC_COORDINATION", "normalized_semantics": {"request": "move later"}},
        ],
    }}


def retained_response_command(interaction):
    """Actual bound-source command preparation for the earlier response root.

    Its original I/exchange is distinct from the later responding I. No native
    input/consume producer or original-author reauthorization is claimed.
    """
    from DEV.TESTS.test_rd05_runtime_execution import (
        _bind_context,
        _candidate,
        _interpreter_result,
        _proposal,
    )
    from GAME.TOOLS.native_storage import route_native_record

    target = interaction["state"]["response_target"]
    proposal = _proposal()
    proposal.update(command_id=target["root_command_id"], root_resolution_id=target["resolution_id"],
        interaction_id=target["root_command_id"] + ".input", intent_plan_id=target["root_command_id"] + ".plan")
    with trusted_command_source(proposal, campaign_id=interaction["state"]["campaign_id"]) as (host, records):
        basis = records[route_native_record("runtime.interaction", (proposal["interaction_id"],)).relative_path]["state"]["accepted_input_basis"]
        basis.update(accepted_exchange_key=proposal["command_id"] + ":exchange",
            host_invocation_ref=proposal["command_id"] + ":invocation")
        mapping_path = host._accepted_input_capability.mapping_path
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
        mapping["key"][4] = basis["accepted_exchange_key"]
        mapping["host_invocation_ref"] = basis["host_invocation_ref"]
        mapping_path.write_text(json.dumps(mapping), encoding="utf-8")
        accepted = runtime_execution.accept_command(_interpreter_result(), _bind_context(), _candidate(), proposal,
            input_observation=host._current_owner._observe_command_input(proposal))
    return {"kind": "runtime.command", "id": accepted["command_id"], **accepted}


def retained_response_resolution(interaction, segment, *, command):
    """Complete existing R grammar and actual K binding; not native issuance."""
    from DEV.TESTS.test_rd05_runtime_execution import _resolution_source

    state = _resolution_source(command, segments=[deepcopy(segment)], next_segment_sequence=2)
    return {"kind": "runtime.resolution", "id": interaction["state"]["response_target"]["resolution_id"], "state": state}


def retained_eventless_segment(owner_id):
    return {"schema_version": 1, "segment_id": owner_id + ":segment:1", "segment_sequence": 1,
        "commit_state": "committed", "resulting_execution_state": "COMPLETED", "event_ids": [],
        "pending_child_invocations": [], "receipt_exports": {}, "affected_revision_refs": []}


def response_binding_mutations():
    return {
        "actor_id": "foreign-root-actor",
        "activity_id": "activity.foreign",
        "initiating_command_id": "foreign-command",
        "catalog_context_fingerprint": "wrong-context",
        "ruleset_set_sha256": "1" * 64,
        "invocation_facts": [{"fact_id": "fiction.target_reachable", "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED", "provenance_ref": "retained:foreign-fact",
            "consumer_id": "activity.check.generic", "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64, "policy_basis_refs": []}],
        "target_ids": ["foreign-target"],
    }


class TrustedInputAdapterFixture:
    """Constructor-only TC infrastructure with restart-stable exchange mapping.

    This implements the source contract, not a deployed supported issuer. No
    gameplay verdict, private acceptance seal, RNG or native producer is faked.
    """

    adapter_profile_id = "fixture.input"
    adapter_profile_generation = 1

    def __init__(self, mapping_path):
        from GAME.TOOLS.access_control import VerifiedPrincipal

        self.mapping_path = mapping_path
        self.principal = VerifiedPrincipal("123", "fixture-player")
        self.calls = []

    def lookup_exchange(self, *, repository_identity, campaign_id,
                        adapter_profile_id, adapter_profile_generation, accepted_exchange_key):
        self.calls.append("lookup")
        record = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        key = [repository_identity, campaign_id, adapter_profile_id,
               adapter_profile_generation, accepted_exchange_key]
        return record["interaction_id"] if record["key"] == key else None

    def accepted_representation(self, *, repository_identity, campaign_id,
                                adapter_profile_id, adapter_profile_generation,
                                accepted_exchange_key, host_invocation_ref):
        self.calls.append("representation")
        record = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        key = [repository_identity, campaign_id, adapter_profile_id,
               adapter_profile_generation, accepted_exchange_key]
        if record["key"] != key or record["host_invocation_ref"] != host_invocation_ref:
            raise ValueError("exchange/invocation mapping conflict")
        return record["principal_at_acceptance"], record["exact_text"]

    def current_principal(self, *, repository_identity, campaign_id):
        self.calls.append("principal")
        record = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        if [repository_identity, campaign_id] != record["key"][:2]:
            raise ValueError("principal scope differs")
        return self.principal


def trusted_input_source_records(proposal, *, repository_identity, campaign_id):
    """One retained-source producer for Git and in-memory P0 conformance fixtures."""
    from GAME.TOOLS.native_storage import route_native_record

    interaction, message, plan = input_sources(kind="intent")
    interaction["id"] = proposal["interaction_id"]
    message["id"] = f'{proposal["interaction_id"]}.message'
    plan["id"] = proposal["intent_plan_id"]
    state = interaction["state"]
    state.update(campaign_id=campaign_id, input_message_id=message["id"], intent_plan_id=plan["id"])
    basis = state["accepted_input_basis"]
    basis["repository_identity"] = repository_identity
    basis["authority_at_acceptance"]["accepted_subject_ids"] = [proposal["action_request"]["actor_id"]]
    message["state"].update(message_id=message["id"], interaction_id=interaction["id"])
    plan["state"]["interaction_id"] = interaction["id"]
    plan["state"]["clauses"][0].update(clause_id=proposal["clause_id"], command_id=proposal["command_id"])
    player = {"schema_version": 2, "kind": "world.player", "id": "player-1", "state": {
        "player_id": "player-1", "status": "active", "github_binding": {"user_id": "123", "login": "fixture-player"},
        "controlled_pc_ids": [proposal["action_request"]["actor_id"]], "collaboration_route_refs": [],
    }}
    sources = (interaction, message, plan, player)
    records = {route_native_record(source["kind"], (source["id"],)).relative_path: source
               for source in sources}
    route_path = "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
    records[route_path] = {"schema_version": 1, "kind": "runtime.principal_player_routing",
        "campaign_id": campaign_id, "complete": True,
        "entries": [{"stable_account_id": "123", "candidate_player_ids": ["player-1"]}]}
    records["MANIFEST.yaml"] = {"campaign_id": campaign_id, "mode": "multiplayer",
        "players": {"player_ids": ["player-1"], "join_policy": "invite_only"}}
    mapping = {
        "key": [repository_identity, campaign_id, "fixture.input", 1, "exchange-1"],
        "interaction_id": interaction["id"], "host_invocation_ref": "invocation-1",
        "principal_at_acceptance": {"provider": "github", "stable_account_id": "123", "login": "fixture-player"},
        "exact_text": message["state"]["exact_text"],
    }
    return records, mapping


def seed_trusted_input_sources(repository, proposal, mapping_path, *, campaign_id="campaign-frostfall"):
    """Write retained TC sources through Git; never issue a native acceptance."""
    records, mapping = trusted_input_source_records(proposal,
        repository_identity=repository.repository_identity(), campaign_id=campaign_id)
    for path, record in records.items():
        repository.write(path, record)
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")
    repository.commit("retained trusted-input conformance sources")
    return TrustedInputAdapterFixture(mapping_path), tuple(path for path in records if path != "MANIFEST.yaml")


@contextmanager
def trusted_command_source(proposal, *, repository=None, campaign_id="campaign-frostfall"):
    """Bound Host/P0 source fixture, with retained native bytes and no native issuer.

    Callers retain successful preparation explicitly in ``records`` before asking
    for an execution observation. Negative proposals never replace those bytes.
    """
    from DEV.TESTS.test_w05_t06_p0_actor_producer import (
        ActorRepository,
        PublicationTransport,
        SelectedLive,
    )
    from GAME.TOOLS.bootstrap import CampaignSelection, compose_selected_runtime_host
    from GAME.TOOLS.hot_store import NativeHotStore
    from GAME.TOOLS.live_state import LiveRouting
    from GAME.TOOLS.native_storage import route_native_record

    class Repository(ActorRepository):
        def read_exact_path(self, pin, path):
            if path in self.records:
                self.path_reads.append((pin.revision, path))
                return deepcopy(self.records[path])
            return super().read_exact_path(pin, path)

    repository = Repository() if repository is None else repository
    records, mapping = trusted_input_source_records(proposal,
        repository_identity=repository.repository_identity(), campaign_id=campaign_id)
    if hasattr(repository, "files"):
        repository.files.update(records)
        records = repository.files
    else:
        repository.records = records
    actor = deepcopy(repository.actor)
    actor["id"] = proposal["action_request"]["actor_id"]
    records[route_native_record("world.actor", (actor["id"],)).relative_path] = actor
    with tempfile.TemporaryDirectory(prefix="s2-command-", dir="/tmp/hdm-dev/spell-recovery") as temporary:
        mapping_path = Path(temporary) / "exchange.json"
        mapping_path.write_text(json.dumps(mapping), encoding="utf-8")
        store = NativeHotStore(":memory:")
        try:
            host = compose_selected_runtime_host(CampaignSelection.existing(campaign_id),
                repository, SelectedLive(route=LiveRouting(campaign_id=campaign_id, entries=())), PublicationTransport(), hot_owner_store=store,
                accepted_input_capability=TrustedInputAdapterFixture(mapping_path))
            yield host, records
        finally:
            store.close()


def prepare_trusted_git_command(repository, proposal, context, *, adjudication_basis=None):
    """Prepare against the actual fixture Git sources and constructor-bound TC.

    The caller still writes retained K/R bytes separately. This never establishes
    input, command or execution state through a native producer.
    """
    from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result
    from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
    from GAME.TOOLS.hot_store import NativeHotStore

    mapping_path = repository.root.with_name(repository.root.name + ".exchange.json")
    adapter, _paths = seed_trusted_input_sources(repository, proposal, mapping_path)
    with NativeHotStore(":memory:") as store:
        host, _ = _selected_host(store, repository=repository, accepted_input_capability=adapter)
        accepted = runtime_execution.accept_command(_interpreter_result(), context,
            {"definition_id": proposal["action_request"]["activity_id"], "kind": "definition.activity"},
            proposal, input_observation=host._current_owner._observe_command_input(proposal),
            adjudication_basis=adjudication_basis)
    return accepted, adapter


class AuthenticatedHostSourceTests(unittest.TestCase):
    """Actual bound Host, P0 establishment, native reads and current-control TC."""

    def setUp(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            ACTOR_ID,
            CAMPAIGN_ID,
            ActorRepository,
            PublicationTransport,
            SelectedLive,
            _actor_phase,
        )
        from GAME.TOOLS.bootstrap import (
            CampaignSelection,
            compose_selected_runtime_host,
        )
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        self.campaign_id = CAMPAIGN_ID
        self.actor_id = ACTOR_ID
        temporary = tempfile.TemporaryDirectory(prefix="s2-input-", dir="/tmp/hdm-dev/spell-recovery")
        self.addCleanup(temporary.cleanup)
        self.mapping_path = Path(temporary.name) / "exchange.json"
        self.adapter = TrustedInputAdapterFixture(self.mapping_path)
        self.repository = ActorRepository()
        if hasattr(self, "make_repository"):
            self.repository = self.make_repository(self.repository)
        self.repository.revision_records[self.repository.revision] = {}
        self.records = self.repository.revision_records[self.repository.revision]
        # ActorRepository normally serves this exact native source directly;
        # the revision-record branch is used for all the additional input owners.
        self.records[route_native_record("world.actor", (ACTOR_ID,)).relative_path] = deepcopy(self.repository.actor)
        self.interaction, self.message, self.plan = input_sources(kind="intent")
        state = self.interaction["state"]
        state["campaign_id"] = CAMPAIGN_ID
        basis = state["accepted_input_basis"]
        basis["repository_identity"] = self.repository.repository_identity()
        basis["authority_at_acceptance"]["accepted_subject_ids"] = [ACTOR_ID]
        self.plan["state"]["clauses"][0]["command_id"] = "command-1"
        self.player = {"schema_version": 2, "kind": "world.player", "id": "player-1", "state": {
            "player_id": "player-1", "status": "active", "github_binding": {"user_id": "123", "login": "fixture-player"},
            "controlled_pc_ids": [ACTOR_ID], "collaboration_route_refs": [],
        }}
        for source in (self.interaction, self.message, self.plan, self.player):
            self.records[route_native_record(source["kind"], (source["id"],)).relative_path] = deepcopy(source)
        self.records["MANIFEST.yaml"] = {
            "campaign_id": CAMPAIGN_ID, "mode": "multiplayer",
            "players": {"player_ids": ["player-1"], "join_policy": "invite_only"},
        }
        self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"] = {
            "schema_version": 1, "kind": "runtime.principal_player_routing", "campaign_id": CAMPAIGN_ID,
            "complete": True, "entries": [{"stable_account_id": "123", "candidate_player_ids": ["player-1"]}],
        }
        self.mapping_path.write_text(json.dumps({
            "key": [self.repository.repository_identity(), CAMPAIGN_ID, "fixture.input", 1, "exchange-1"],
            "interaction_id": self.interaction["id"], "host_invocation_ref": "invocation-1",
            "principal_at_acceptance": {"provider": "github", "stable_account_id": "123", "login": "fixture-player"},
            "exact_text": self.message["state"]["exact_text"],
        }), encoding="utf-8")
        self.store = NativeHotStore(":memory:")
        self.addCleanup(self.store.close)
        self.compose = lambda adapter: compose_selected_runtime_host(
            CampaignSelection.existing(CAMPAIGN_ID), self.repository, SelectedLive(), PublicationTransport(),
            hot_owner_store=self.store, accepted_input_capability=adapter,
        )
        self.host = self.compose(self.adapter)
        envelope, phase_result = _actor_phase(self.host, self.repository.actor)
        result = self.host.actor_continuity.establish_from_phase(envelope, phase_result)
        self.assertEqual(result.status.value, "ESTABLISHED")
        self.assertEqual(result.after_state_revision, 5)
        self.command = {
            "command_id": "command-1", "interaction_id": self.interaction["id"], "intent_plan_id": self.plan["id"],
            "clause_id": "clause-1", "command_kind": "action", "root_resolution_id": "resolution-1",
            "action_request": {"activity_id": "activity.check.generic", "actor_id": ACTOR_ID, "target_ids": []},
        }

    def _observe(self, host=None):
        return (host or self.host)._current_owner._observe_command_input(self.command)

    def test_bound_adapter_native_p0_observation_and_retry_mapping(self):
        from GAME.TOOLS.current_owner import CurrentOwnerSource, NativeOwnerRef

        observation = self._observe()
        actor = observation.require(NativeOwnerRef("world.actor", (self.actor_id,)))
        self.assertIs(actor.source, CurrentOwnerSource.ACCEPTED_HOT)
        self.assertEqual(actor.payload["state_revision"], 5)
        self.assertEqual(self.adapter.calls[0], "lookup")
        self.assertLess(self.adapter.calls.index("lookup"), self.adapter.calls.index("principal"))
        self.host._current_owner._validate_command_input_observation(observation, self.command)
        # A restarted TC adapter recovers exactly the same exchange->I mapping.
        fresh_host = self.compose(TrustedInputAdapterFixture(self.mapping_path))
        fresh = self._observe(fresh_host)
        self.assertIsNot(fresh.operation_token, observation.operation_token)
        fresh_host._current_owner._validate_command_input_observation(fresh, self.command)

    def test_missing_capability_dto_and_copied_or_foreign_session_do_not_authorize(self):
        from dataclasses import replace

        from GAME.TOOLS.runtime_host import RuntimeHostError

        with self.assertRaises(RuntimeHostError):
            self._observe(self.compose(None))
        with self.assertRaises((RuntimeHostError, TypeError)):
            self.compose({"verified": True, "principal": "123"})
        observation = self._observe()
        with self.assertRaises(RuntimeHostError):
            self.host._current_owner._validate_command_input_observation(replace(observation), self.command)
        with self.assertRaises(RuntimeHostError):
            self.compose(self.adapter)._current_owner._validate_command_input_observation(observation, self.command)

    def test_action_acceptance_requires_exact_source_observation_and_uses_codec3(self):
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.runtime_execution import (
            accept_command,
            validate_execution_proposal,
        )

        context = _bind_context()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        candidate = {"definition_id": "activity.check.generic", "kind": "definition.activity"}
        with self.assertRaises(TypeError):
            accept_command(_interpreter_result(), context, candidate, proposal)
        observation = self._observe()
        accepted = accept_command(_interpreter_result(), context, candidate, proposal, input_observation=observation)
        self.assertEqual(accepted["schema_version"], 4)
        self.assertEqual(accepted["input_fingerprint_generation"], 3)
        self.assertNotIn("accepted_input_origin", accepted)
        # Source conformance deliberately writes retained native K/C bytes here;
        # it does not claim the SP04 native command-acceptance producer exists.
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.native_storage import route_native_record

        with self.assertRaises(ValueError):
            validate_execution_proposal(accepted, context, candidate, input_observation=observation)
        command_ref = NativeOwnerRef("runtime.command", (accepted["command_id"],))
        self.records[route_native_record("runtime.command", command_ref.identity).relative_path] = {
            "kind": "runtime.command", "id": accepted["command_id"], **deepcopy(accepted)}
        native_observation = self.host._current_owner._observe_command_input(accepted, required_owner_refs=(command_ref,))
        validate_execution_proposal(accepted, context, candidate, input_observation=native_observation)
        for field, value in (("target_ids", ["foreign-target"]), ("actor_id", "foreign-actor")):
            forged = deepcopy(accepted)
            forged["action_request"][field] = value
            origin = self.host._current_owner._input_origin(accepted, native_observation)
            forged["input_fingerprint"] = runtime_execution.command_input_fingerprint(forged, origin=origin)
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_execution_proposal(forged, context, candidate, input_observation=native_observation)
        with self.assertRaises(ValueError):
            accept_command(_interpreter_result(), context, candidate, proposal, input_observation=object())

    def test_current_control_route_and_source_mutations_fail_before_preparation(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import RuntimeHostError

        player_path = route_native_record("world.player", ("player-1",)).relative_path
        interaction_path = route_native_record("runtime.interaction", (self.interaction["id"],)).relative_path
        for label, path, mutate in (
            ("inactive", player_path, lambda x: x["state"].update(status="inactive", deactivated_by="creator")),
            ("control lost", player_path, lambda x: x["state"].update(controlled_pc_ids=[])),
            ("rebound", player_path, lambda x: x["state"]["github_binding"].update(user_id="999")),
            ("foreign envelope", player_path, lambda x: x.update(id="foreign-player")),
            ("invalid state", player_path, lambda x: x["state"].update(unknown=True)),
            ("wrong invocation", interaction_path, lambda x: x["state"]["accepted_input_basis"].update(host_invocation_ref="foreign")),
            ("wrong repository", interaction_path, lambda x: x["state"]["accepted_input_basis"].update(repository_identity="foreign")),
            ("historical login rewritten", interaction_path, lambda x: x["state"]["accepted_input_basis"]["principal"].update(login_at_acceptance="forged-login")),
            ("omitted route", "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml", lambda x: x.update(entries=[])),
        ):
            original = deepcopy(self.records[path])
            mutate(self.records[path])
            try:
                with self.subTest(label=label), self.assertRaises(RuntimeHostError):
                    self._observe()
            finally:
                self.records[path] = original

    def test_current_source_or_control_change_invalidates_prospective_observation(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import RuntimeHostError

        observation = self._observe()
        path = route_native_record("world.player", ("player-1",)).relative_path
        self.records[path]["state"]["controlled_pc_ids"] = []
        with self.assertRaises(RuntimeHostError):
            self.host._current_owner._validate_command_input_observation(observation, self.command)

    def test_review_f1_same_host_stale_reader_cannot_bypass_public_acceptance(self):
        from types import MethodType

        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.native_storage import route_native_record

        observation = self._observe()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        context = _bind_context()
        runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
            input_observation=observation)
        retained = deepcopy(self.records)
        player_path = route_native_record("world.player", ("player-1",)).relative_path
        self.records[player_path]["state"]["controlled_pc_ids"] = []
        with self.assertRaises(ValueError):
            runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                input_observation=observation)
        original = observation.operation_token.session._reader

        def stale_reader(host, pin, path):
            return deepcopy(retained[path]) if path in retained else original(pin, path)

        observation.operation_token.session._reader = MethodType(stale_reader, self.host)
        with self.assertRaises(ValueError):
            runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                input_observation=observation)

    def test_review_f1_public_acceptance_rejects_substituted_session_configuration(self):
        from copy import copy
        from dataclasses import replace
        from types import MethodType

        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.hot_store import NativeHotStore

        context = _bind_context()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        other_store = NativeHotStore(":memory:")
        self.addCleanup(other_store.close)
        for field in ("_reader", "_source_basis_reader", "_live_reader", "_hot_store",
                      "_pinned_campaign", "_selected_live", "_campaign_id", "copied_session"):
            observation = self._observe()
            session = observation.operation_token.session
            runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                input_observation=observation)
            original = getattr(session, field, None)
            if field in {"_reader", "_source_basis_reader", "_live_reader"}:
                def substituted(host, *args, callback=original):
                    return callback(*args)
                replacement = MethodType(substituted, self.host)
            elif field == "_hot_store":
                replacement = other_store
            elif field in {"_pinned_campaign", "_selected_live"}:
                replacement = replace(original)
            elif field == "copied_session":
                replacement = copy(session)
            else:
                replacement = "foreign-campaign"
            if field == "copied_session":
                observation.operation_token.session = replacement
            else:
                setattr(session, field, replacement)
            with self.subTest(field=field), self.assertRaises(ValueError):
                runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                    input_observation=observation)

    def test_historical_origin_survives_revocation_but_new_work_requires_current_control(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import RuntimeHostError

        observation = self._observe()
        original = self.host._current_owner._input_origin(self.command, observation)
        path = route_native_record("world.player", ("player-1",)).relative_path
        self.records[path]["state"].update(status="inactive", deactivated_by="creator")
        with self.assertRaises(RuntimeHostError):
            self._observe()
        historical = self.host._current_owner._observe_command_input(self.command, current_authority=False)
        self.assertEqual(original, self.host._current_owner._validate_command_input_observation(
            historical, self.command, current_authority=False))
        with self.assertRaises(RuntimeHostError):
            self.host._current_owner._validate_command_input_observation(historical, self.command)

    def test_duplicate_complete_account_route_reads_all_nominated_players_and_denies(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import RuntimeHostError

        duplicate = deepcopy(self.player)
        duplicate["id"] = "player-2"
        duplicate["state"]["player_id"] = "player-2"
        self.records[route_native_record("world.player", ("player-2",)).relative_path] = duplicate
        self.records["MANIFEST.yaml"]["players"]["player_ids"].append("player-2")
        route = self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"]
        route["entries"][0]["candidate_player_ids"].append("player-2")
        with self.assertRaises(RuntimeHostError):
            self._observe()
        paths = {path for _, path in self.repository.path_reads}
        self.assertIn(route_native_record("world.player", ("player-1",)).relative_path, paths)
        self.assertIn(route_native_record("world.player", ("player-2",)).relative_path, paths)

    def test_review_f2_all_route_accounts_require_exact_player_body_associations(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.native_storage import route_native_record

        other = deepcopy(self.player)
        other["id"] = other["state"]["player_id"] = "player-2"
        other["state"]["github_binding"]["user_id"] = "999"
        path = route_native_record("world.player", ("player-2",)).relative_path
        self.records[path] = deepcopy(other)
        self.records["MANIFEST.yaml"]["players"]["player_ids"].append("player-2")
        self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"]["entries"].append({
            "stable_account_id": "999", "candidate_player_ids": ["player-2"]})
        context = _bind_context()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        observation = self._observe()
        runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
            input_observation=observation)
        normal_union = observation.key_union
        for label, mutation in (
            ("duplicate account hidden in another row", lambda p: p["state"]["github_binding"].update(user_id="123")),
            ("foreign unrelated account", lambda p: p["state"]["github_binding"].update(user_id="888")),
            ("invalid unrelated state", lambda p: p["state"].update(unknown=True)),
            ("foreign envelope", lambda p: p.update(id="foreign-player")),
        ):
            self.records[path] = deepcopy(other)
            observation = self._observe()
            mutation(self.records[path])
            with self.subTest(case=label, boundary="read"), self.assertRaises(ValueError):
                self._observe()
            with self.subTest(case=label, boundary="public"), self.assertRaises(ValueError):
                runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                    input_observation=observation)
        self.records.pop(path)
        with self.assertRaises(ValueError):
            self._observe()
        self.assertIn(NativeOwnerRef("world.player", ("player-2",)), normal_union)

    def test_review_f4_mixed_prior_resolution_uses_strict_observed_source_validator(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.native_storage import route_native_record

        interaction, message, _plan = input_sources()
        interaction["state"]["campaign_id"] = self.campaign_id
        interaction["state"]["accepted_input_basis"] = deepcopy(self.interaction["state"]["accepted_input_basis"])
        interaction["state"]["response_target"]["root_command_id"] = "prior-command"
        interaction["state"]["response_target"]["responder_id"] = self.actor_id
        segment = response_survivor(interaction, message)
        plan = mixed_plan(interaction)
        plan["state"]["clauses"][1].update(mapping_outcome="exact", execution_state="intent.ready",
            collaboration_semantic_class="ACTIONABLE_INTENT", command_id=self.command["command_id"])
        self.command.update(clause_id="clause.intent.1", root_resolution_id="resolution-extra")
        prior = {"kind": "runtime.resolution", "id": "resolution-1", "campaign_id": self.campaign_id,
            "state": {"schema_version": 1, "root_command_id": "prior-command", "segments": [segment]}}
        for owner in (interaction, message, plan, prior):
            self.records[route_native_record(owner["kind"], (owner["id"],)).relative_path] = deepcopy(owner)
        context = _bind_context()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        prior_path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
        for purpose in (True, False):
            self.records[prior_path] = deepcopy(prior)
            observed = self.host._current_owner._observe_command_input(self.command, current_authority=purpose)
            runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                input_observation=observed)
            for label, mutate in (
                ("foreign campaign", lambda r: r.update(campaign_id="foreign")),
                ("flattened root conflict", lambda r: r.update(root_command_id="forged-root")),
                ("unsupported schema", lambda r: r["state"].update(schema_version=999)),
            ):
                self.records[prior_path] = deepcopy(prior)
                mutate(self.records[prior_path])
                with self.subTest(case=label, current_authority=purpose), self.assertRaises(ValueError):
                    wrong = self.host._current_owner._observe_command_input(self.command, current_authority=purpose)
                    runtime_execution.accept_command(_interpreter_result(), context, _candidate(), proposal,
                        input_observation=wrong)

    def test_creator_uses_real_history_service_without_a_player_or_session_lease(self):
        from DEV.TESTS.test_rd09_access_live import _HistoryRepository
        from GAME.TOOLS.access_control import VerifiedPrincipal
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import RuntimeHostError

        history_source = _HistoryRepository(author_login="fixture-player")
        for name in ("read_exact_campaign_ref", "read_exact_commit", "compare_ancestry", "read_authenticated_commit_author"):
            setattr(self.repository, name, getattr(history_source, name))
        self.records["MANIFEST.yaml"]["mode"] = "singleplayer"
        self.records.pop("STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml")
        self.records.pop(route_native_record("world.player", ("player-1",)).relative_path)
        path = route_native_record("runtime.interaction", (self.interaction["id"],)).relative_path
        state = self.records[path]["state"]
        state.pop("player_id")
        state["accepted_input_basis"]["authority_at_acceptance"] = {
            "kind": "creator_singleplayer", "accepted_subject_ids": [self.actor_id],
            "creator_history": {"author_login": "fixture-player",
                "initialization_revision": history_source.initialization_revision,
                "parent_revision": history_source.parent_revision},
        }
        # A historical session remains a native link; no current session owner is
        # invented as a lease, and no Player is needed to authorize this creator.
        state["session_id"] = "historical-session"
        observation = self._observe()
        self.assertFalse(any(ref.family_key == "world.player" for ref in observation.key_union))
        self.assertTrue(history_source.calls)
        self.adapter.principal = VerifiedPrincipal("123", "renamed-creator")
        with self.assertRaises(RuntimeHostError):
            self._observe()


class DirectInputCompositionTests(unittest.TestCase):
    setUp = AuthenticatedHostSourceTests.setUp
    _observe = AuthenticatedHostSourceTests._observe

    @staticmethod
    def make_repository(native_repository):
        class RecoveryCatalogRepository:
            def __getattr__(self, name):
                return getattr(native_repository, name)

            def resolve_recovery_catalog_context(self, pinned, command, catalog_basis):
                from DEV.TESTS.sp02_installed_test_support import (
                    authentic_generic_catalog,
                )

                context = authentic_generic_catalog().catalog_context
                if context.to_dict() != catalog_basis:
                    raise ValueError("native recovery catalog differs")
                return context, None

        return RecoveryCatalogRepository()

    def test_installed_direct_profile_source_and_command_cutover(self):
        import os

        if "HDM_INSTALLED_STRUCTURAL_TEST" not in os.environ:
            from DEV.TESTS.sp02_installed_test_support import (
                run_installed_structural_test,
            )

            result = run_installed_structural_test(
                "DEV.TESTS.test_sp03_authenticated_input.DirectInputCompositionTests."
                "test_installed_direct_profile_source_and_command_cutover")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return

        from DEV.TESTS.sp02_installed_test_support import authentic_generic_catalog
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.native_storage import route_native_record

        context = authentic_generic_catalog().catalog_context
        self.command = {key: value for key, value in self.command.items()
            if key not in {"action_request", "root_resolution_id"}}
        self.command.update(command_kind="transition", transition_request={
            "transition_kind": "transition.location_change", "payload": {
                "transition_kind": "transition.location_change",
                "profile_id": "location_change.outside_procedure", "idempotency_key": "move-1",
                "catalog_generation": 2, "actor_id": self.actor_id, "actor_revision": 5,
                "destination_location_id": "location-2", "destination_location_revision": 1,
                "movement_cost": "NOT_APPLICABLE_OUTSIDE_PROCEDURE"}},
            transition_binding={"profile_id": "location_change.outside_procedure", "profile_generation": 1,
                "payload_schema_id": "https://hedgelion.invalid/schemas/gameplay-spine-transition-request.schema.json#/$defs/outsideProcedureMovement",
                "payload_schema_version": 1})
        destination_ref = NativeOwnerRef("world.location", ("location-2",))
        self.records[route_native_record(destination_ref.family_key, destination_ref.identity).relative_path] = {
            "kind": "world.location", "id": "location-2", "state_revision": 1, "state": {}}
        observation = self._observe()
        self.assertIn(destination_ref, observation.key_union)
        accepted = runtime_execution.accept_command(None, context, None, self.command, input_observation=observation)
        self.assertEqual(accepted["schema_version"], 4)
        self.assertNotIn("root_resolution_id", accepted)
        self.assertNotIn("interpreter_result", accepted)
        command_ref = NativeOwnerRef("runtime.command", (accepted["command_id"],))
        self.records[route_native_record(command_ref.family_key, command_ref.identity).relative_path] = {
            "kind": "runtime.command", "id": accepted["command_id"], **deepcopy(accepted)}
        observed = self.host._current_owner._observe_command_input(accepted, required_owner_refs=(command_ref,))
        runtime_execution.validate_execution_proposal(accepted, context, None, input_observation=observed)
        from GAME.TOOLS.durability import (
            evaluate_durability,
            freeze_save_promise,
            join_execution_durability,
        )
        from GAME.TOOLS.publication import _accepted_identity

        segment_id = accepted["command_id"] + ":segment:1"
        event_id = segment_id + ":event:1"
        segment = {"schema_version": 1, "segment_id": segment_id, "segment_sequence": 1,
            "event_ids": [event_id], "commit_state": "committed", "resulting_execution_state": "COMPLETED",
            "pending_child_invocations": [], "receipt_exports": {}, "affected_revision_refs": []}
        receipt = {"execution_owner_id": accepted["command_id"], "segment_refs": [segment_id],
            "event_ids": [event_id], "status": "COMPLETED", "exports": {}, "pending_child_refs": []}
        # Retained native-source conformance bytes, not a native producer claim.
        direct = {"accepted_command_id": accepted["command_id"],
            "accepted_input_fingerprint": accepted["input_fingerprint"],
            "status": "COMPLETED",
            "execution_owner_id": accepted["command_id"], "segment": segment, "receipt": receipt,
            "events": [{"segment_id": segment_id, "event_ordinal": 1,
                "root_command_id": accepted["command_id"], "causal_ref": accepted["command_id"],
                "event_kind": "event.entity.moved", "payload": {}}]}
        promise = freeze_save_promise(evaluate_durability(campaign_id=self.campaign_id,
            scope="accepted_execution", dirty_roots=("runtime.command:command-1",),
            currentness_evidence={"head_sha": "a" * 40}), owner_generations={})
        retained = dict(accepted, direct_transition_segments=[segment], direct_transition_receipt=receipt)
        joined = join_execution_durability(retained, direct, promise,
            routed_operation=route_serialized_operation("runtime.command", retained["command_id"], retained))
        identity, _, _ = _accepted_identity(retained, direct)
        self.assertEqual(identity.to_dict(), joined.to_dict()["execution_identity"])
        self.assertEqual(identity.execution_owner_kind, "runtime.command")
        self.assertNotIn("resolution_id", joined.to_dict())
        self.assertNotIn("action_request", joined.to_dict()["policy_basis"])
        from GAME.TOOLS.recovery import (
            _hydrate_execution_result,
            validate_recovered_basis,
        )

        pin = self.repository.pin_campaign(self.campaign_id)
        self.assertIsNone(_hydrate_execution_result(self.repository, pin, accepted, None))
        from GAME.TOOLS.recovery import _validate_recovered_root_closures

        root = self.records[route_native_record(command_ref.family_key, command_ref.identity).relative_path]
        _validate_recovered_root_closures(self.repository, pin, (root,), input_observation=observed)
        self.records[route_native_record("runtime.mechanical_event", (event_id,)).relative_path] = {
            "kind": "runtime.mechanical_event", "id": event_id, **direct["events"][0]}
        hydrated = _hydrate_execution_result(self.repository, pin, retained, None)
        self.assertNotIn("resolution_id", hydrated)
        recovered = validate_recovered_basis(retained, hydrated, catalog_basis=context.to_dict(),
            policy_basis=joined.to_dict()["policy_basis"])
        self.assertEqual(recovered.execution_identity, identity.to_dict())
        eventless_segment = dict(segment, event_ids=[])
        eventless_receipt = dict(receipt, event_ids=[])
        eventless_owner = dict(retained, direct_transition_segments=[eventless_segment],
            direct_transition_receipt=eventless_receipt)
        eventless_result = dict(direct, segment=eventless_segment, receipt=eventless_receipt, events=[])

        def consume_direct(owner, result):
            projected = _accepted_identity(owner, result)[0].to_dict()
            durable = join_execution_durability(owner, result, promise,
                routed_operation=route_serialized_operation("runtime.command", owner["command_id"], owner))
            recovered_result = validate_recovered_basis(owner, result, catalog_basis=context.to_dict(),
                policy_basis=durable.to_dict()["policy_basis"])
            self.assertEqual(projected, recovered_result.execution_identity)
            return projected

        self.assertEqual(consume_direct(eventless_owner, eventless_result)["event_ids"], [])
        eventless_without_carrier = dict(eventless_result)
        eventless_without_carrier.pop("events")
        self.assertEqual(consume_direct(eventless_owner, eventless_without_carrier)["event_ids"], [])
        for label, owner, result in (
            ("unsupported direct segment", retained, dict(direct, segment=dict(segment, schema_version=999))),
            ("prospective direct segment", retained, dict(direct, segment=dict(segment, commit_state="prospective"))),
            ("missing K embedding", dict(retained, direct_transition_segments=[]), direct),
            ("foreign K receipt", dict(retained, direct_transition_receipt=dict(receipt, execution_owner_id="foreign")), direct),
        ):
            for name, consumer in (
                ("publication", lambda owner=owner, result=result: _accepted_identity(owner, result)),
                ("durability", lambda owner=owner, result=result: join_execution_durability(owner, result, promise,
                    routed_operation=route_serialized_operation("runtime.command", owner["command_id"], owner))),
                ("recovery", lambda owner=owner, result=result: validate_recovered_basis(owner, result, catalog_basis=context.to_dict(),
                    policy_basis=joined.to_dict()["policy_basis"])),
            ):
                with self.subTest(case=label, boundary=name), self.assertRaises(ValueError):
                    consumer()
        retained_root = {"kind": "runtime.command", "id": retained["command_id"], **retained}
        self.records[route_native_record(command_ref.family_key, command_ref.identity).relative_path] = retained_root
        retained_observation = self.host._current_owner._observe_command_input(retained,
            required_owner_refs=(command_ref,))
        _validate_recovered_root_closures(self.repository, pin, (retained_root,),
            input_observation=retained_observation)
        with self.assertRaises(ValueError):
            _validate_recovered_root_closures(self.repository, pin, (retained_root,))
        for wrong in (dict(direct, resolution_id=accepted["command_id"]),
                      dict(direct, execution_owner_id="foreign"),
                      dict(direct, receipt=dict(receipt, execution_owner_id="foreign"))):
            with self.subTest(result=wrong), self.assertRaises(ValueError):
                _accepted_identity(retained, wrong)
        for path, value in ((('transition_binding', 'profile_generation'), True),
                            (('transition_binding', 'payload_schema_id'), 'foreign'),
                            (('transition_request', 'payload', 'actor_revision'), 4),
                            (('transition_request', 'payload', 'movement_cost'), 0),
                            (('transition_request', 'payload', 'patch'), {})):
            wrong = deepcopy(self.command)
            parent = wrong
            for key in path[:-1]:
                parent = parent[key]
            parent[path[-1]] = value
            with self.subTest(path=path), self.assertRaises(ValueError):
                candidate_observation = self.host._current_owner._observe_command_input(wrong)
                runtime_execution.accept_command(None, context, None, wrong, input_observation=candidate_observation)

        # Every other admitted S2 direct source mapping uses its actual finite
        # request/profile and native refs. These remain preparation conformance.
        asset_ref = NativeOwnerRef("world.asset", ("asset-1",))
        self.records[route_native_record(asset_ref.family_key, asset_ref.identity).relative_path] = {
            "kind": "world.asset", "id": "asset-1", "state_revision": 1,
            "state": {"owner_actor_id": self.actor_id, "quantity": 1}}
        procedure_ref = NativeOwnerRef("runtime.procedure", ("procedure-1",))
        self.records[route_native_record(procedure_ref.family_key, procedure_ref.identity).relative_path] = {
            "kind": "runtime.procedure", "id": "procedure-1", "revision": 1,
            "state": {"schema_version": 2, "procedure_kind": "procedure.combat_minimal", "lifecycle": "ACTIVE",
                "lifecycle_state": "turn_active", "participant_ids": [self.actor_id],
                "initiative_order": [self.actor_id], "round_number": 1, "active_turn_index": 0,
                "round_advance_pending": False, "participant_resources": {self.actor_id: {
                    "resource.action_budget": {"capacity": 1, "spent": 0}}}}}
        movement = deepcopy(self.command["transition_request"]["payload"])
        movement.update(profile_id="location_change.procedure_movement", procedure_id="procedure-1",
            procedure_revision=1, movement_cost=2)
        for profile, kind, fragment, payload, refs in (
            ("location_change.procedure_movement", "transition.location_change", "procedureMovement", movement,
             {procedure_ref, destination_ref}),
            ("asset.equip", "transition.asset_status", "assetEquip",
             {"asset_id": "asset-1", "asset_revision": 1, "owner_actor_id": self.actor_id, "mode": "held"}, {asset_ref}),
            ("asset.transfer", "transition.asset_transfer", "assetTransfer",
             {"asset_id": "asset-1", "asset_revision": 1, "from_placement": {"owner_actor_id": self.actor_id},
              "to_placement": {"location_id": "location-2"}}, {asset_ref, destination_ref}),
        ):
            with self.subTest(profile=profile):
                candidate_command = deepcopy(self.command)
                candidate_command["transition_request"] = {"transition_kind": kind,
                    "payload": {**payload, "transition_kind": kind, "profile_id": profile,
                        "idempotency_key": "native-profile-1", "catalog_generation": 2}}
                candidate_command["transition_binding"].update(profile_id=profile,
                    payload_schema_id="https://hedgelion.invalid/schemas/gameplay-spine-transition-request.schema.json#/$defs/" + fragment)
                observed_profile = self.host._current_owner._observe_command_input(candidate_command)
                self.assertTrue(refs <= set(observed_profile.key_union))
                prepared = runtime_execution.accept_command(None, context, None, candidate_command,
                    input_observation=observed_profile)
                self.assertEqual(prepared["command_kind"], "transition")
                self.assertNotIn("root_resolution_id", prepared)
                for forbidden_interpreter, forbidden_candidate in (({}, None), (None, {})):
                    with self.assertRaises(ValueError):
                        runtime_execution.accept_command(forbidden_interpreter, context, forbidden_candidate,
                            candidate_command, input_observation=observed_profile)


class SourceBoundMechanicsTests(unittest.TestCase):
    setUp = AuthenticatedHostSourceTests.setUp
    _observe = AuthenticatedHostSourceTests._observe

    def test_codec3_native_source_retry_survives_revocation_but_new_segment_holds(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            _interpreter_result,
            _resolution_source,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.mechanics import ExecutionStore, FixedRng, resolve_mechanic
        from GAME.TOOLS.native_storage import route_native_record

        context = _bind_context()
        proposal = {key: value for key, value in self.command.items() if key != "command_kind"}
        accepted = runtime_execution.accept_command(_interpreter_result(), context,
            {"definition_id": "activity.check.generic", "kind": "definition.activity"}, proposal,
            input_observation=self._observe())
        command_ref = NativeOwnerRef("runtime.command", (accepted["command_id"],))
        self.records[route_native_record(command_ref.family_key, command_ref.identity).relative_path] = {
            "kind": "runtime.command", "id": accepted["command_id"], **deepcopy(accepted)}
        observed = self.host._current_owner._observe_command_input(accepted, required_owner_refs=(command_ref,))
        resolution = _resolution_source(accepted)
        store, rng = ExecutionStore(), FixedRng([11, 12])
        result = resolve_mechanic(accepted, resolution, input_observation=observed, store=store, rng=rng)
        self.assertEqual(result["execution_identity"]["input_fingerprint_generation"], 3)
        from GAME.TOOLS.durability import (
            evaluate_durability,
            freeze_save_promise,
            join_execution_durability,
            route_serialized_operation,
        )
        from GAME.TOOLS.publication import _accepted_identity

        promise = freeze_save_promise(evaluate_durability(campaign_id=self.campaign_id,
            scope="accepted_execution", dirty_roots=("runtime.command:command-1",),
            currentness_evidence={"head_sha": "a" * 40}), owner_generations={})
        joined = join_execution_durability(accepted, result, promise,
            routed_operation=route_serialized_operation("runtime.command", "command-1", accepted))
        self.assertEqual(joined.to_dict()["execution_identity"], result["execution_identity"])
        published_identity, _, catalog_basis = _accepted_identity(accepted, result)
        self.assertEqual(published_identity.to_dict(), result["execution_identity"])
        self.assertEqual(catalog_basis, context.to_dict())
        self.assertEqual(rng.draw_count, 1)
        self.player["state"]["status"] = "inactive"
        self.records[route_native_record("world.player", ("player-1",)).relative_path] = deepcopy(self.player)
        historical = self.host._current_owner._observe_command_input(accepted,
            required_owner_refs=(command_ref,), current_authority=False)
        self.assertEqual(result, resolve_mechanic(accepted, resolution,
            input_observation=historical, store=store, rng=rng))
        with self.assertRaises(ValueError):
            resolve_mechanic(accepted, dict(resolution, next_segment_sequence=2),
                input_observation=historical, store=store, rng=rng)
        self.assertEqual(rng.draw_count, 1)


class AuthenticatedCommandCodecTests(unittest.TestCase):
    """Initial S2 pure-source RED cases, not Host/current-authority conformance."""

    def test_schema_source_members_and_input_infrastructure_are_exact(self):
        from DEV.TOOLS.validate_ruleset_package_closure import (
            ENGINE_CONTRACT_SOURCE_GROUPS,
        )
        from GAME.TOOLS import catalog_runtime

        projection = json.loads((Path(__file__).resolve().parents[2] /
            "GAME/TOOLS/activity_compiler_contracts.json").read_text(encoding="utf-8"))
        members = projection["families"]["schema_contract"]
        self.assertEqual(set(members), {key for key, _path in ENGINE_CONTRACT_SOURCE_GROUPS["schema_contract"]})
        validator = getattr(catalog_runtime, "_validate_schema_contract_members", None)
        self.assertTrue(callable(validator), "strict installed schema source member loader is missing")
        validator(members)
        for key in members:
            wrong = deepcopy(members)
            wrong.pop(key)
            with self.subTest(missing=key), self.assertRaises(ValueError):
                validator(wrong)
        with self.assertRaises(ValueError):
            validator(dict(members, invented_auth_registry={}))
        descriptor = members["activity_compiler_declaration_schema"]["$defs"]["acceptedInputOriginInfrastructure"]["const"]
        self.assertEqual(descriptor, {"contract_id": "infrastructure.accepted_input_origin", "contract_generation": 1})
        wrong = deepcopy(members)
        wrong["activity_compiler_declaration_schema"]["$defs"]["acceptedInputOriginInfrastructure"]["const"]["contract_generation"] = True
        with self.assertRaises(ValueError):
            validator(wrong)

    def test_previous_compiler_generation_cannot_admit_new_input_contract(self):
        from GAME.TOOLS.activity_runtime import (
            ActivityRuntimeError,
            admit_activity_catalog,
        )

        for generation in (True, 1, 3):
            with self.subTest(generation=generation), self.assertRaisesRegex(ActivityRuntimeError, "generation.*2"):
                admit_activity_catalog({}, package_snapshots={}, engine_contract_inventory_source=None,
                    natural_owner_sources={}, compiler_generation=generation,
                    mode_policy_profile_id="execution.spell_cast.srd521")

    def test_mechanics_output_qualifies_resolution_and_embedded_segment_initial_schema(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            SourceCommandFixture,
            _candidate,
            _interpreter_result,
            _proposal,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.mechanics import ExecutionStore

        source = SourceCommandFixture()
        self.addCleanup(source.doCleanups)
        context = _bind_context()
        command = source.accept_from_sources(_interpreter_result(), context, _candidate(), _proposal())
        resolution = {"root_command_id": command["command_id"], "initiating_command_id": command["command_id"],
            "activity_id": "activity.check.generic", "actor_id": "actor-1",
            "ruleset_set_digest_generation": 1, "ruleset_set_sha256": context.basis["ruleset_lock"]["ruleset_set_sha256"],
            "catalog_context_fingerprint_generation": 1, "catalog_context_fingerprint": context.fingerprint,
            "status": "COMPLETED", "next_segment_sequence": 1, "invocation_facts": [],
            "fixed_rng_results": [], "prior_step_exports": {}, "child_resolution_ids": [], "segments": []}
        result = source.execute_from_sources(command, resolution, event_payload={}, store=ExecutionStore())
        for name, value in (("runtime-resolution-state", result["resolution"]), ("execution-segment", result["segment"])):
            self.assertEqual(value.get("schema_version"), 1, name + " lacks initial schema qualification")
            runtime_execution._input_wire(name, value)
            for wrong in (dict(value, schema_version=True), dict(value, schema_version=2),
                          {key: item for key, item in value.items() if key != "schema_version"}):
                with self.subTest(schema=name, value=wrong), self.assertRaises(ValueError):
                    runtime_execution._input_wire(name, wrong)

    def _origin(self, interaction, message, plan, clause_id="clause-1"):
        self.assertTrue(
            callable(getattr(runtime_execution, "accepted_input_origin", None)),
            "S2 native-source origin derivation is not implemented",
        )
        return runtime_execution.accepted_input_origin(
            campaign_id="campaign-1", interaction=interaction, message=message,
            plan=plan, clause_id=clause_id,
        )

    def test_origin_requires_exact_native_input_plan_and_intent_clause(self):
        interaction, message, plan = input_sources(kind="intent")
        origin = self._origin(interaction, message, plan)
        self.assertEqual(origin, {
            "interaction_id": interaction["id"], "intent_plan_id": plan["id"],
            "clause_id": "clause-1", "input_kind": "intent",
            "accepted_input_basis": interaction["state"]["accepted_input_basis"],
        })
        for label, mutate in (
            ("campaign", lambda i, m, p: i["state"].update(campaign_id="foreign")),
            ("message", lambda i, m, p: m.update(id="foreign")),
            ("content", lambda i, m, p: m["state"].update(exact_text="changed")),
            ("plan", lambda i, m, p: p.update(id="foreign")),
            ("parent", lambda i, m, p: p["state"].update(interaction_id="foreign")),
            ("missing clause", lambda i, m, p: p["state"].update(clauses=[])),
            ("duplicate clause", lambda i, m, p: p["state"]["clauses"].append(deepcopy(p["state"]["clauses"][0]))),
        ):
            i, m, p = deepcopy((interaction, message, plan))
            mutate(i, m, p)
            with self.subTest(label=label), self.assertRaises(ValueError):
                runtime_execution.accepted_input_origin(
                    campaign_id="campaign-1", interaction=i, message=m, plan=p,
                    clause_id="clause-1",
                )

    def test_mixed_origin_retains_prior_resume_but_nonexecuting_units_cannot_create_commands(self):
        interaction, message, _ = input_sources()
        segment = response_survivor(interaction, message)
        plan = mixed_plan(interaction)
        extra = plan["state"]["clauses"][1]
        extra.update(mapping_outcome="exact", execution_state="intent.ready")
        arguments = {"campaign_id": "campaign-1", "interaction": interaction, "message": message,
            "plan": plan, "accepted_response_segment": segment}
        with self.assertRaises(ValueError):
            runtime_execution.accepted_input_origin(**arguments, clause_id="clause.intent.1")
        extra["collaboration_semantic_class"] = "ACTIONABLE_INTENT"
        origin = runtime_execution.accepted_input_origin(**arguments, clause_id="clause.intent.1")
        self.assertEqual(origin["accepted_resume_ref"], interaction["state"]["accepted_resume_ref"])
        with self.assertRaises(ValueError):
            runtime_execution.accepted_input_origin(**arguments, clause_id="clause.response")

    def test_direct_codec_hashes_complete_payload_binding_and_origin(self):
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context

        interaction, message, plan = input_sources(kind="intent")
        origin = self._origin(interaction, message, plan)
        context = _bind_context()
        command = {
            "command_kind": "transition", "catalog_context_fingerprint": context.fingerprint,
            "catalog_context": context.to_dict(),
            "invocation_facts": [],
            "transition_request": {"transition_kind": "transition.location_change", "payload": {
                "transition_kind": "transition.location_change",
                "profile_id": "location_change.procedure_movement",
                "idempotency_key": "movement-1", "catalog_generation": 2,
                "procedure_id": "procedure-1", "procedure_revision": 1,
                "actor_id": "actor-1", "actor_revision": 1,
                "destination_location_id": "location-2", "destination_location_revision": 1,
                "movement_cost": 1,
            }},
            "transition_binding": {"profile_id": "location_change.procedure_movement",
                "profile_generation": 1,
                "payload_schema_id": "https://hedgelion.invalid/schemas/gameplay-spine-transition-request.schema.json#/$defs/procedureMovement",
                "payload_schema_version": 1},
        }
        # The payload uses the existing source-owned finite movement contract.
        # This pure codec test does not claim inventory admission or native issue.
        from jsonschema import Draft202012Validator

        from DEV.TESTS.test_rd15_catalog_runtime import _schema_registry

        registry, schemas = _schema_registry()
        Draft202012Validator(
            schemas["gameplay-spine-transition-request.schema.json"], registry=registry,
        ).validate(command["transition_request"]["payload"])
        self.assertTrue(
            callable(getattr(runtime_execution, "command_input_fingerprint", None)),
            "S2 single command codec3 is not implemented",
        )
        fingerprint = runtime_execution.command_input_fingerprint(command, origin=origin)
        material = dict(command, accepted_input_origin=origin)
        self.assertEqual(fingerprint, sha256(b"HDM_RUNTIME_COMMAND_INPUT/3\n" + canonical_json(material)))
        for key in command["transition_request"]["payload"]:
            wrong = deepcopy(command)
            current = wrong["transition_request"]["payload"][key]
            wrong["transition_request"]["payload"][key] = current + 1 if type(current) is int else "foreign"
            self.assertNotEqual(fingerprint, runtime_execution.command_input_fingerprint(wrong, origin=origin))
        for key in command["transition_binding"]:
            wrong = deepcopy(command)
            wrong["transition_binding"][key] = 2 if key.endswith(("generation", "version")) else "foreign"
            self.assertNotEqual(fingerprint, runtime_execution.command_input_fingerprint(wrong, origin=origin))
        def leaves(value, prefix=()):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield from leaves(item, (*prefix, key))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    yield from leaves(item, (*prefix, index))
            else:
                yield prefix, value

        for path, value in leaves(origin):
            altered = deepcopy(origin)
            parent = altered
            for member in path[:-1]:
                parent = parent[member]
            parent[path[-1]] = value + 1 if type(value) is int else value + ".changed"
            with self.subTest(origin_member=path):
                try:
                    changed = runtime_execution.command_input_fingerprint(command, origin=altered)
                except runtime_execution.CommandAcceptanceError:
                    continue
                self.assertNotEqual(fingerprint, changed)
        self.assertEqual(fingerprint, runtime_execution.command_input_fingerprint(
            dict(command, disposition="command.settled", details={"diagnostic": "ignored"}), origin=origin))

    def test_execution_projection_dispatches_actual_action_and_direct_owner_without_fake_event(self):
        self.assertTrue(callable(getattr(runtime_execution, "execution_identity", None)),
                        "S2 branch-aware execution projection is not implemented")
        command = {"command_id": "command-1", "command_kind": "transition",
            "input_fingerprint_generation": 3, "input_fingerprint": "a" * 64}
        segment = {"segment_id": "command-1:segment:1", "segment_sequence": 1, "event_ids": []}
        identity = runtime_execution.execution_identity(command, execution_owner_kind="runtime.command",
            execution_owner_id="command-1", segment=segment)
        self.assertEqual(identity, {"identity_generation": 1, "command_id": "command-1",
            "input_fingerprint_generation": 3, "input_fingerprint": "a" * 64,
            "execution_owner_kind": "runtime.command", "execution_owner_id": "command-1",
            "segment_id": "command-1:segment:1", "event_ids": []})
        action = dict(command, command_kind="action", root_resolution_id="resolution-1")
        action_segment = dict(segment, segment_id="resolution-1:segment:1", event_ids=["event-1"])
        projected = runtime_execution.execution_identity(action, execution_owner_kind="runtime.resolution",
            execution_owner_id="resolution-1", segment=action_segment)
        self.assertEqual(projected["event_ids"], ["event-1"])
        self.assertNotIn("resolution_id", projected)
        for owner_kind, owner_id, source in (
            ("runtime.resolution", "command-1", segment),
            ("runtime.command", "foreign", segment),
            ("runtime.command", "command-1", dict(segment, segment_id="resolution-1:segment:1")),
            ("runtime.command", "command-1", dict(segment, segment_sequence=True)),
            ("runtime.command", "command-1", dict(segment, event_ids=["event-1", "event-1"])),
        ):
            with self.subTest(owner_kind=owner_kind, owner_id=owner_id, source=source), self.assertRaises(ValueError):
                runtime_execution.execution_identity(command, execution_owner_kind=owner_kind,
                    execution_owner_id=owner_id, segment=source)


class CollaborationInputAuthorityTests(unittest.TestCase):
    """Clause-use TC over the established P0 source fixture, never native issue."""

    def setUp(self):
        AuthenticatedHostSourceTests.setUp(self)
        from GAME.TOOLS.native_storage import route_native_record

        self.plan["state"]["clauses"][0].pop("command_id")
        self.plan["state"]["clauses"][0].update(
            collaboration_semantic_class="OOC_COORDINATION",
            normalized_semantics={"request": "move later"},
        )
        self.records[route_native_record("runtime.intent_plan", (self.plan["id"],)).relative_path] = deepcopy(self.plan)

    def observe(self, **kwargs):
        from GAME.TOOLS.access_control import PrincipalPlayerRoute

        method = getattr(self.host._current_owner, "_observe_collaboration_input", None)
        self.assertTrue(callable(method), "trusted no-K collaboration observation is missing")
        arguments = {"principal": self.adapter.principal,
            "player_route": kwargs.get("player_route") or PrincipalPlayerRoute.from_mapping(self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"])}
        arguments.update(kwargs)
        return method(self.interaction["id"], "clause-1", **arguments)

    def test_no_k_clause_uses_complete_native_source_union(self):
        observation, player = self.observe()
        self.assertEqual(player.player_id, "player-1")
        self.assertEqual({ref.family_key for ref in observation.key_union},
                         {"runtime.interaction", "runtime.message", "runtime.intent_plan", "world.player"})
        self.assertNotIn("command_id", self.plan["state"]["clauses"][0])

    def test_caller_principal_cannot_replace_trusted_current_principal(self):
        from GAME.TOOLS.access_control import VerifiedPrincipal
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        self.adapter.principal = VerifiedPrincipal("other-account", "other-login")
        with self.assertRaises(InputAuthorityUnavailable):
            self.observe(principal=VerifiedPrincipal("123", "fixture-player"))

    def test_caller_route_cannot_replace_complete_native_account_route(self):
        from GAME.TOOLS.access_control import PrincipalPlayerRoute
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        claimed = PrincipalPlayerRoute.from_mapping(self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"])
        self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"]["complete"] = False
        with self.assertRaises(InputAuthorityUnavailable):
            self.observe(player_route=claimed)

    def test_missing_bound_issuer_holds_before_association(self):
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        self.host = self.compose(None)
        with self.assertRaises(InputAuthorityUnavailable):
            self.observe()

    def _obligation(self, clause_id="clause-1"):
        from GAME.TOOLS.access_control import PrincipalPlayerRoute
        from GAME.TOOLS.collaboration import (
            classify_coordination_dependency,
            open_or_successor_obligation,
        )
        from GAME.TOOLS.native_storage import route_native_record

        clause = next(clause for clause in self.plan["state"]["clauses"] if clause["clause_id"] == clause_id)
        clause.update(execution_state="intent.pending", dependency_kind="JOINT_VOLUNTARY_ACTION",
            purpose="move-later", dependency_scope={"scene_id": "scene-1"},
            required_contributors=[{"player_id": "player-1"}],
            native_basis_refs=[{"family": "world.scene", "id": "scene-1", "revision": self.repository.revision}])
        self.records[route_native_record("runtime.intent_plan", (self.plan["id"],)).relative_path] = deepcopy(self.plan)
        self.records[route_native_record("world.scene", ("scene-1",)).relative_path] = {
            "kind": "world.scene", "id": "scene-1", "revision": self.repository.revision, "state": {}}
        self.player.update(deepcopy(self.player["state"]))
        self.records[route_native_record("world.player", ("player-1",)).relative_path] = deepcopy(self.player)
        self.route = PrincipalPlayerRoute.from_mapping(self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"])
        admission = classify_coordination_dependency(self.host, self.interaction["id"], clause_id,
            principal=self.adapter.principal, player_route=self.route)
        obligation = open_or_successor_obligation(admission, obligation_id="obligation-1")
        self.assertIsNotNone(obligation)
        self.records[route_native_record("runtime.collaboration_obligation", (obligation.obligation_id,)).relative_path] = obligation.to_mapping()
        self.player["state"]["collaboration_route_refs"] = [{"obligation_id": "obligation-1", "generation": 1}]
        self.player["collaboration_route_refs"] = deepcopy(self.player["state"]["collaboration_route_refs"])
        self.records[route_native_record("world.player", ("player-1",)).relative_path] = deepcopy(self.player)
        return obligation

    def test_public_association_rejects_caller_principal_after_trusted_account_switch(self):
        from GAME.TOOLS.access_control import VerifiedPrincipal
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )

        obligation = self._obligation()
        self.assertEqual(associate_input(obligation, self.host, self.interaction["id"], "clause-1",
            principal=self.adapter.principal, player_route=self.route), obligation)
        self.adapter.principal = VerifiedPrincipal("other-account", "other-login")
        with self.assertRaises(CollaborationAdmissionError):
            associate_input(obligation, self.host, self.interaction["id"], "clause-1",
                principal=VerifiedPrincipal("123", "fixture-player"), player_route=self.route)

    def test_public_association_rejects_callback_host_replaying_an_old_observation(self):
        from types import SimpleNamespace

        from GAME.TOOLS.access_control import VerifiedPrincipal
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )

        obligation = self._obligation()
        captured = self.observe(player_route=self.route)
        real_host = self.host

        class CallbackHost:
            _current_owner = SimpleNamespace(
                _observe_collaboration_input=lambda *args, **kwargs: captured,
                _input_payload=real_host._current_owner._input_payload,
            )

            def __getattr__(proxy, name):
                return getattr(real_host, name)

        self.adapter.principal = VerifiedPrincipal("other-account", "other-login")
        with self.assertRaises(CollaborationAdmissionError):
            associate_input(obligation, CallbackHost(), self.interaction["id"], "clause-1",
                principal=VerifiedPrincipal("123", "fixture-player"), player_route=self.route)

    def test_public_association_generation_is_not_boolean(self):
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )

        obligation = self._obligation()
        with self.assertRaises(CollaborationAdmissionError):
            associate_input(obligation, self.host, self.interaction["id"], "clause-1",
                principal=self.adapter.principal, player_route=self.route, generation=True)

    def test_inactive_duplicate_rebound_and_omitted_native_players_hold(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        route_path = "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
        player_path = route_native_record("world.player", ("player-1",)).relative_path
        original = deepcopy(self.records)
        for label in ("inactive", "duplicate", "rebound", "omitted", "invalid envelope"):
            self.records.clear()
            self.records.update(deepcopy(original))
            if label == "inactive":
                self.records[player_path]["state"]["status"] = "inactive"
            elif label == "rebound":
                self.records[player_path]["state"]["github_binding"]["user_id"] = "other"
            elif label == "invalid envelope":
                self.records[player_path]["id"] = "foreign"
            else:
                other = deepcopy(self.records[player_path])
                other["id"] = other["state"]["player_id"] = "player-2"
                self.records[route_native_record("world.player", ("player-2",)).relative_path] = other
                self.records["MANIFEST.yaml"]["players"]["player_ids"].append("player-2")
                if label == "duplicate":
                    self.records[route_path]["entries"][0]["candidate_player_ids"].append("player-2")
            with self.subTest(label=label), self.assertRaises(InputAuthorityUnavailable):
                self.observe()

    def test_mixed_ooc_uses_prior_marker_without_current_old_offer_or_command(self):
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        interaction = self.interaction
        state = interaction["state"]
        state.pop("intent_plan_id")
        state.update(input_kind="response_and_intent", planning_phase="awaiting_response",
            response_target={"root_command_id": "old-command", "resolution_id": "old-resolution",
                "continuation_id": "old-continuation", "continuation_generation": 7,
                "offer_kind": "choice", "offer_id": "offer-7", "responder_id": self.actor_id},
            response_selection={"kind": "choice", "option_id": "option-A"})
        text = "Choose A; let's move later"
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        state["accepted_input_basis"]["representation"]["content_digest"] = digest
        self.message["state"].update(exact_text=text, content_digest=digest)
        mapping = json.loads(self.mapping_path.read_text(encoding="utf-8"))
        mapping["exact_text"] = text
        self.mapping_path.write_text(json.dumps(mapping), encoding="utf-8")
        segment = response_survivor(interaction, self.message)
        # Use the actual fixed old R address; no current Continuation is needed
        # to validate retained historical response evidence for a new clause use.
        state["accepted_resume_ref"]["resolution_id"] = "old-resolution"
        state["accepted_resume_ref"]["segment_id"] = "old-resolution:segment:1"
        segment["segment_id"] = "old-resolution:segment:1"
        self.plan = mixed_plan(interaction)
        for owner in (interaction, self.message, self.plan):
            self.records[route_native_record(owner["kind"], (owner["id"],)).relative_path] = deepcopy(owner)
        root_command = retained_response_command(interaction)
        self.records[route_native_record("runtime.command", (root_command["id"],)).relative_path] = root_command
        self.records[route_native_record("runtime.resolution", ("old-resolution",)).relative_path] = retained_response_resolution(
            interaction, segment, command=root_command)
        method = self.host._current_owner._observe_collaboration_input
        observation, player = method(interaction["id"], "clause.intent.1", principal=self.adapter.principal,
                                     player_route=self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"])
        self.assertEqual(player.player_id, "player-1")
        self.assertIn("runtime.resolution", {ref.family_key for ref in observation.key_union})
        self.assertFalse({ref.identity[0] for ref in observation.key_union if ref.family_key == "runtime.command"} - {"old-command"})
        self.assertNotEqual(root_command["action_request"]["actor_id"], state["response_target"]["responder_id"])
        obligation = self._obligation("clause.intent.1")
        associated = associate_input(obligation, self.host, interaction["id"], "clause.intent.1",
            principal=self.adapter.principal, player_route=self.route, generation=obligation.generation)
        self.assertIn((interaction["id"], "clause.intent.1"), associated.accepted_input_uses)
        self.assertNotIn((interaction["id"], "clause.response"), associated.accepted_input_uses)
        with self.assertRaises(CollaborationAdmissionError):
            associate_input(obligation, self.host, interaction["id"], "clause.response",
                principal=self.adapter.principal, player_route=self.route)
        with self.assertRaises(InputAuthorityUnavailable):
            method(interaction["id"], "clause.response", principal=self.adapter.principal,
                   player_route=self.records["STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"])

    def test_public_mixed_association_rejects_incomplete_or_malformed_retained_result(self):
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )
        from GAME.TOOLS.native_storage import route_native_record

        self.test_mixed_ooc_uses_prior_marker_without_current_old_offer_or_command()
        obligation = self._obligation("clause.intent.1")
        path = route_native_record("runtime.resolution", ("old-resolution",)).relative_path
        valid = deepcopy(self.records[path])
        for case in ("truncated", "status", "rng", "frontier", "suspension", "child"):
            self.records[path] = deepcopy(valid)
            state = self.records[path]["state"]
            if case == "truncated":
                self.records[path]["state"] = {key: state[key] for key in ("schema_version", "root_command_id", "segments")}
            elif case == "status":
                state["status"] = "NOT_A_NATIVE_STATUS"
            elif case == "rng":
                state["fixed_rng_results"] = [{"digest": "a" * 64}]
            elif case == "frontier":
                state["next_segment_sequence"] = 1
            elif case == "suspension":
                state["status"] = "AWAITING_CHOICE"
            else:
                state["child_resolution_ids"] = ["missing-child"]
                state["segments"][0]["pending_child_invocations"] = [{"firing_key": "fixed-child",
                    "root_command_id": state["root_command_id"], "activity_id": state["activity_id"],
                    "trigger_ref": state["segments"][0]["segment_id"], "reason": "mandatory_followup",
                    "child_resolution_id": "missing-child"}]
            with self.subTest(case=case), self.assertRaises(CollaborationAdmissionError):
                associate_input(obligation, self.host, self.interaction["id"], "clause.intent.1",
                    principal=self.adapter.principal, player_route=self.route)

    def test_r3_public_mixed_association_binds_response_r_to_actual_original_k(self):
        from GAME.TOOLS.collaboration import (
            CollaborationAdmissionError,
            associate_input,
        )
        from GAME.TOOLS.native_storage import route_native_record

        self.test_mixed_ooc_uses_prior_marker_without_current_old_offer_or_command()
        obligation = self._obligation("clause.intent.1")
        path = route_native_record("runtime.resolution", ("old-resolution",)).relative_path
        valid = deepcopy(self.records[path])
        for field, value in response_binding_mutations().items():
            self.records[path] = deepcopy(valid)
            associate_input(obligation, self.host, self.interaction["id"], "clause.intent.1",
                principal=self.adapter.principal, player_route=self.route)
            self.records[path]["state"][field] = value
            with self.subTest(field=field), self.assertRaises(CollaborationAdmissionError):
                associate_input(obligation, self.host, self.interaction["id"], "clause.intent.1",
                    principal=self.adapter.principal, player_route=self.route)

    def test_creator_without_player_is_scoped_hold_without_fake_multiplayer_reads(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        source = self.records[route_native_record("runtime.interaction", (self.interaction["id"],)).relative_path]
        source["state"].pop("player_id")
        source["state"]["accepted_input_basis"]["authority_at_acceptance"] = input_sources(
            kind="intent", creator=True)[0]["state"]["accepted_input_basis"]["authority_at_acceptance"]
        self.records["MANIFEST.yaml"]["mode"] = "singleplayer"
        self.records.pop(route_native_record("world.player", ("player-1",)).relative_path)
        self.records.pop("STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml")
        before = len(self.repository.path_reads)
        with self.assertRaisesRegex(InputAuthorityUnavailable, "multiplayer participation"):
            self.host._current_owner._observe_collaboration_input(self.interaction["id"], "clause-1",
                principal=self.adapter.principal, player_route=None)
        self.assertFalse(any("PLAYER" in path for _, path in self.repository.path_reads[before:]))

    def test_relevant_source_movement_invalidates_clause_observation(self):
        from GAME.TOOLS.runtime_host import InputAuthorityUnavailable

        repository = self.repository

        class MovingTrustedAdapter(TrustedInputAdapterFixture):
            def current_principal(adapter, **scope):
                principal = super().current_principal(**scope)
                if adapter.calls.count("principal") == 2:
                    repository.revision_records["c" * 40] = deepcopy(repository.revision_records[repository.revision])
                    repository.revision = "c" * 40
                return principal

        adapter = MovingTrustedAdapter(self.mapping_path)
        self.host = self.compose(adapter)
        with self.assertRaisesRegex(InputAuthorityUnavailable, "REVALIDATION_REQUIRED"):
            self.observe()


class InputRootClosureTests(unittest.TestCase):
    def validate(self, interaction, message, plan=None, segment=None):
        runtime_execution.validate_input_closure(
            campaign_id="campaign-1", interaction=interaction, message=message,
            plan=plan, accepted_response_segment=segment,
        )

    def _cold_repository(self, interaction, message, plan=None, segment=None):
        from DEV.TESTS.test_rd07_recovery import FakeRepository
        from GAME.TOOLS.native_storage import route_native_record

        repository = FakeRepository()
        for source in (interaction, message, plan):
            if source is not None:
                repository.files[route_native_record(source["kind"], (source["id"],)).relative_path] = deepcopy(source)
        if segment is not None:
            command = retained_response_command(interaction)
            resolution = retained_response_resolution(interaction, segment, command=command)
            for source in (command, resolution):
                repository.files[route_native_record(source["kind"], (source["id"],)).relative_path] = source
        return repository

    def test_review_f1_cold_response_requires_native_resolution_identity(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import RecoveryFailure, _hydrate_input_root_closure

        for materialized in (False, True):
            interaction, message, _ = input_sources()
            segment = response_survivor(interaction, message)
            plan = mixed_plan(interaction) if materialized else None
            repository = self._cold_repository(interaction, message, plan, segment)
            pin = repository.pin_campaign("campaign-1")
            _hydrate_input_root_closure(repository, pin, interaction)
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            valid = deepcopy(repository.files[path])
            for label, mutate in (
                ("foreign envelope", lambda r: r.update(id="foreign-resolution")),
                ("missing envelope ID", lambda r: r.pop("id")),
                ("missing envelope kind", lambda r: r.pop("kind")),
                ("foreign flat projection", lambda r: r.update(resolution_id="foreign-resolution")),
                ("foreign state projection", lambda r: r["state"].update(resolution_id="foreign-resolution")),
                ("conflicting root projection", lambda r: r.update(root_command_id="foreign-command")),
            ):
                wrong = deepcopy(valid)
                mutate(wrong)
                repository.files[path] = wrong
                with self.subTest(materialized=materialized, mutation=label), self.assertRaises(RecoveryFailure):
                    _hydrate_input_root_closure(repository, pin, interaction)
            valid["resolution_id"] = "resolution-1"
            valid["state"]["resolution_id"] = "resolution-1"
            repository.files[path] = valid
            _hydrate_input_root_closure(repository, pin, interaction)

    def test_review_f2_marker_nested_types_do_not_equal_valid_source(self):
        for kind in ("response", "response_and_intent"):
            interaction, message, _ = input_sources(kind=kind)
            segment = response_survivor(interaction, message)
            self.validate(interaction, message, segment=segment)
            fingerprint = segment["accepted_resume_input"]["resume_fingerprint"]
            for value in (True, 1.0):
                wrong = deepcopy(segment)
                wrong["accepted_resume_input"]["target"]["continuation_generation"] = value
                self.assertIs(type(interaction["state"]["response_target"]["continuation_generation"]), int)
                self.assertEqual(wrong["accepted_resume_input"]["resume_fingerprint"], fingerprint)
                with self.subTest(kind=kind, value=value), self.assertRaises(ValueError):
                    self.validate(interaction, message, segment=wrong)
            for field in ("root_command_id", "resolution_id", "continuation_id", "offer_id", "responder_id"):
                for value in (True, 1.0, "foreign-id"):
                    wrong = deepcopy(segment)
                    wrong["accepted_resume_input"]["target"][field] = value
                    with self.subTest(kind=kind, field=field, value=value), self.assertRaises(ValueError):
                        self.validate(interaction, message, segment=wrong)
            for selection in ({"kind": "choice", "option_id": True},
                              {"kind": "choice", "option_id": "foreign-option"},
                              {"kind": "choice", "option_id": "option-A", "extra": None}):
                wrong = deepcopy(segment)
                wrong["accepted_resume_input"]["selection"] = selection
                with self.subTest(kind=kind, selection=selection), self.assertRaises(ValueError):
                    self.validate(interaction, message, segment=wrong)

    def test_review_f3_message_and_plan_campaign_projections_are_bound(self):
        from GAME.TOOLS.recovery import RecoveryFailure, _hydrate_input_root_closure

        for source_kind in ("message", "plan"):
            for value in ("campaign-foreign", True, 1.0, None):
                interaction, message, plan = input_sources(kind="intent")
                source = message if source_kind == "message" else plan
                source["campaign_id"] = value
                with self.subTest(source=source_kind, value=value, consumer="pure"), self.assertRaises(ValueError):
                    self.validate(interaction, message, plan)
                repository = self._cold_repository(interaction, message, plan)
                with self.subTest(source=source_kind, value=value, consumer="cold"), self.assertRaises(RecoveryFailure):
                    _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)
        for explicit in (False, True):
            interaction, message, plan = input_sources(kind="intent")
            if explicit:
                message["campaign_id"] = plan["campaign_id"] = "campaign-1"
            self.validate(interaction, message, plan)
            repository = self._cold_repository(interaction, message, plan)
            _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)

    def test_review_f4_standalone_plan_parent_is_a_native_interaction_id(self):
        import json
        from pathlib import Path

        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        from GAME.TOOLS.structural_contracts import validate_contract

        root = Path(__file__).resolve().parents[2]
        names = ("runtime-intent-plan-state", "intent-clause", "runtime-interaction-state")
        schemas = {name: json.loads((root / "DEV/SCHEMAS" / (name + ".schema.json")).read_text(encoding="utf-8")) for name in names}
        registry = Registry().with_resources((schema["$id"], Resource.from_contents(schema)) for schema in schemas.values())
        validator = Draft202012Validator(schemas["runtime-intent-plan-state"], registry=registry)
        _, _, plan = input_sources(kind="intent")
        for parent in ("not/a/native/id", "", None, True, 1.0):
            wrong = deepcopy(plan)
            wrong["state"]["interaction_id"] = parent
            with self.subTest(parent=parent, consumer="DEV"):
                self.assertFalse(validator.is_valid(wrong["state"]))
            with self.subTest(parent=parent, consumer="installed"), self.assertRaises(ValueError):
                validate_contract("runtime-intent-plan-state", wrong["state"])
            with self.subTest(parent=parent, consumer="standalone"), self.assertRaises(ValueError):
                runtime_execution.validate_input_plan(wrong)
            with self.subTest(parent=parent, consumer="promise"), self.assertRaises(DurabilityContractError):
                issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.intent_plan",
                                                 native_owner=wrong, scope="handoff")
            with self.subTest(parent=parent, consumer="serialized"), self.assertRaises(DurabilityContractError):
                route_serialized_operation("runtime.intent_plan", wrong["id"], wrong)
        validator.validate(plan["state"])
        validate_contract("runtime-intent-plan-state", plan["state"])
        runtime_execution.validate_input_plan(plan)
        promise = issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.intent_plan",
                                                  native_owner=plan, scope="handoff")
        self.assertEqual(promise.required_dependencies, (("runtime.interaction", "interaction-1"),))
        route_serialized_operation("runtime.intent_plan", plan["id"], plan)

    def test_promised_root_and_serialized_route_use_own_interaction_id(self):
        # Equal flattened projections expose the old M-as-I predicate directly.
        interaction, _, _ = input_sources(kind="intent")
        interaction.update(interaction["state"])
        promise = issue_durability_handoff_promise(
            campaign_id="campaign-1", owner_kind="runtime.interaction",
            native_owner=interaction, scope="handoff",
        )
        page = enumerate_operational_root_page(
            "campaign-1", [("runtime.interaction", interaction, promise)],
        )
        self.assertEqual(page.roots[0].owner_id, "interaction-1")
        for creator in (False, True):
            with self.subTest(creator=creator):
                interaction, _, _ = input_sources(creator=creator)
                promise = issue_durability_handoff_promise(
                    campaign_id="campaign-1", owner_kind="runtime.interaction",
                    native_owner=interaction, scope="handoff",
                )
                page = enumerate_operational_root_page(
                    "campaign-1", [("runtime.interaction", interaction, promise)],
                )
                self.assertEqual(page.roots[0].owner_id, "interaction-1")
                route_serialized_operation("runtime.interaction", "interaction-1", interaction)
                with self.assertRaises(DurabilityContractError):
                    route_serialized_operation("runtime.interaction", "message-9", interaction)

    def test_native_input_phase_and_reciprocal_source_links(self):
        for kind in ("intent", "response", "response_and_intent"):
            interaction, message, plan = input_sources(kind=kind)
            self.validate(interaction, message, plan)
            wrong = deepcopy(message)
            wrong["state"]["interaction_id"] = "other-I"
            with self.assertRaises(ValueError):
                self.validate(interaction, wrong, plan)
            if plan is not None:
                with self.assertRaises(ValueError):
                    self.validate(interaction, message)
            else:
                foreign_plan = input_sources(kind="intent")[2]
                with self.assertRaises(ValueError):
                    self.validate(interaction, message, foreign_plan)

    def test_collaboration_loads_only_schema1_intent_units(self):
        from GAME.TOOLS.collaboration import CollaborationAdmissionError, _load_clause
        _, _, plan = input_sources(kind="intent")
        self.assertEqual(_load_clause(plan["state"], "clause-1")["clause_kind"], "intent")
        wrong = deepcopy(plan["state"])
        wrong["clauses"][0]["schema_version"] = True
        with self.assertRaises(CollaborationAdmissionError):
            _load_clause(wrong, "clause-1")

    def test_ready_and_materialized_require_exact_structural_marker_and_phase_links(self):
        interaction, message, _ = input_sources()
        segment = response_survivor(interaction, message)
        self.validate(interaction, message, segment=segment)
        interaction["state"]["response_message_id"] = "outbound-1"
        promise = issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.interaction",
                                                  native_owner=interaction, scope="handoff")
        self.assertEqual(enumerate_operational_root_page("campaign-1", [("runtime.interaction", interaction, promise)]).roots[0].owner_id,
                         interaction["id"])
        with self.assertRaises(ValueError):
            self.validate(interaction, message)
        wrong = deepcopy(segment)
        wrong["accepted_resume_input"]["response_message_id"] = "other-M"
        with self.assertRaises(ValueError):
            self.validate(interaction, message, segment=wrong)
        wrong = deepcopy(segment)
        wrong["accepted"] = True
        with self.assertRaises(ValueError):
            self.validate(interaction, message, segment=wrong)
        plan = mixed_plan(interaction)
        self.validate(interaction, message, plan, segment)
        with self.assertRaises(ValueError):
            self.validate(interaction, message, segment=segment)
        for mutation in (lambda p: p["state"].update(interaction_id="other-I"),
                         lambda p: p["state"]["clauses"].pop(),
                         lambda p: p["state"]["clauses"][1].update(clause_id="clause.response"),
                         lambda p: p["state"]["clauses"][1].update(order=1),
                         lambda p: p["state"]["clauses"][0].update(command_id="command-fake"),
                         lambda p: p["state"]["clauses"][0]["accepted_resume_ref"].update(segment_id="foreign")):
            wrong_plan = deepcopy(plan)
            mutation(wrong_plan)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.validate(interaction, message, wrong_plan, segment)

    def test_source_digest_private_content_and_alias_negatives(self):
        interaction, message, plan = input_sources(kind="intent")
        for mutation in (lambda m: m["state"].update(exact_text="substituted"),
                         lambda m: m["state"].update(exact_text="\ud800"),
                         lambda m: m["state"].update(content_digest="a" * 64),
                         lambda m: m["state"].update(recipient_player_id="private-player"),
                         lambda m: m["state"].update(delivery_evidence_ref="delivery-1"),
                         lambda m: m["state"].update(private_body="secret"),
                         lambda m: m.update(private_body="secret"),
                         lambda m: m.update(message_id="foreign-M"),
                         lambda m: m.update(schema_version=True)):
            wrong = deepcopy(message)
            mutation(wrong)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.validate(interaction, wrong, plan)
        compact = deepcopy(message)
        compact["state"]["payload_state"] = "message.compacted"
        with self.assertRaises(ValueError):
            self.validate(interaction, compact, plan)
        del compact["state"]["exact_text"]
        with self.assertRaises(ValueError):
            self.validate(interaction, compact, plan)

    def test_phase_forbidden_missing_null_and_boolean_fields(self):
        for kind in ("intent", "response", "response_and_intent"):
            interaction, message, plan = input_sources(kind=kind)
            fields = ("schema_version", "input_kind", "accepted_input_basis", "input_message_id")
            for field in fields:
                for value in (None, True, "", {}):
                    wrong = deepcopy(interaction)
                    wrong["state"][field] = value
                    with self.subTest(kind=kind, field=field, value=value), self.assertRaises(ValueError):
                        self.validate(wrong, message, plan)
            wrong = deepcopy(interaction)
            wrong["state"]["accepted_input_basis"]["authority_at_acceptance"]["player_revision"] = True
            with self.assertRaises(ValueError):
                self.validate(wrong, message, plan)
            if kind != "intent":
                wrong = deepcopy(interaction)
                wrong["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = []
                with self.assertRaises(ValueError):
                    self.validate(wrong, message, plan)
        interaction, message, _ = input_sources(creator=True)
        interaction["state"]["player_id"] = "player-fake"
        with self.assertRaises(ValueError):
            self.validate(interaction, message)

    def test_cold_ready_and_materialized_input_closure_is_not_emission_resolution(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.policy_basis import PinnedCampaign
        from GAME.TOOLS.recovery import (
            CurrentNativeSource,
            RecoveryFailure,
            RecoveryFailureCode,
            recover_current_runtime,
        )

        class Repository:
            def __init__(self):
                self.records = {"MANIFEST.yaml": {"campaign_id": "campaign-1"}}
                self.reads = []

            def pin_campaign(self, campaign_id):
                return PinnedCampaign(campaign_id, "a" * 40, "b" * 40)

            def select_current_native_sources(self, pinned):
                return (CurrentNativeSource("campaign-1", "campaign", "campaign-1", "a" * 40, "MANIFEST.yaml"),)

            def read_exact_path(self, pinned, path):
                self.reads.append(path)
                return deepcopy(self.records[path])

            def put(self, value):
                self.records[route_native_record(value["kind"], (value["id"],)).relative_path] = deepcopy(value)

        for creator in (False, True):
            interaction, message, _ = input_sources(creator=creator)
            segment = response_survivor(interaction, message)
            interaction["state"]["response_message_id"] = "outbound-1"
            repository = Repository()
            repository.put(interaction)
            repository.put(message)
            command = retained_response_command(interaction)
            repository.put(command)
            repository.put(retained_response_resolution(interaction, segment, command=command))
            promise = issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.interaction",
                                                      native_owner=interaction, scope="handoff")
            repository.records["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"] = enumerate_operational_root_page(
                "campaign-1", [("runtime.interaction", interaction, promise)],
            ).to_dict()
            result = recover_current_runtime(repository, "campaign-1")
            self.assertEqual(result.disposition.value, "READY")
            self.assertFalse(any("PLAYERS" in path for path in repository.reads))
            self.assertFalse(any("INTENT_PLANS" in path for path in repository.reads))
            message_path = route_native_record("runtime.message", ("message-9",)).relative_path
            saved = repository.records.pop(message_path)
            with self.assertRaises(RecoveryFailure) as raised:
                recover_current_runtime(repository, "campaign-1")
            self.assertEqual(raised.exception.code, RecoveryFailureCode.MISSING)
            repository.records[message_path] = saved
            plan = mixed_plan(interaction)
            repository.put(interaction)
            with self.assertRaises(RecoveryFailure) as raised:
                recover_current_runtime(repository, "campaign-1")
            self.assertEqual(raised.exception.code, RecoveryFailureCode.MISSING)
            repository.put(plan)
            self.assertEqual(recover_current_runtime(repository, "campaign-1").disposition.value, "READY")
            plan["state"]["clauses"][1]["command_id"] = "command-extra"
            plan["state"]["clauses"][1]["mapping_outcome"] = "exact"
            repository.put(plan)
            repository.records[route_native_record("runtime.command", ("command-extra",)).relative_path] = {
                "kind": "runtime.command", "command_id": "command-extra", "interaction_id": "foreign-I",
                "intent_plan_id": "plan-1", "clause_id": "clause.intent.1",
            }
            with self.assertRaises(RecoveryFailure):
                recover_current_runtime(repository, "campaign-1")

    def test_dev_and_installed_phase_schema_agreement(self):
        import json
        from pathlib import Path

        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        from GAME.TOOLS.structural_contracts import validate_contract

        root = Path(__file__).resolve().parents[2]
        names = ("runtime-interaction-state", "runtime-message-state", "runtime-intent-plan-state", "intent-clause")
        schemas = {name: json.loads((root / "DEV/SCHEMAS" / (name + ".schema.json")).read_text()) for name in names}
        registry = Registry().with_resources((schema["$id"], Resource.from_contents(schema)) for schema in schemas.values())
        for kind in ("intent", "response", "response_and_intent"):
            interaction, message, plan = input_sources(kind=kind)
            variants = [(interaction, message, plan)]
            if kind == "response_and_intent":
                response_survivor(interaction, message)
                variants.append((deepcopy(interaction), message, None))
                plan = mixed_plan(interaction)
                variants.append((interaction, message, plan))
            for i, m, p in variants:
                for name, source in zip(names, (i, m, p), strict=False):
                    if source is None:
                        continue
                    state = source["state"]
                    validator = Draft202012Validator(schemas[name], registry=registry)
                    validator.validate(state)
                    validate_contract(name, state)
                    for field in schemas[name]["required"]:
                        for change in ("missing", "null", "extra"):
                            wrong = deepcopy(state)
                            if change == "missing":
                                wrong.pop(field)
                            elif change == "null":
                                wrong[field] = None
                            else:
                                wrong["caller_verified"] = True
                            self.assertFalse(validator.is_valid(wrong))
                            with self.assertRaises(ValueError):
                                validate_contract(name, wrong)

    def test_unpromised_arrival_and_copied_promise_cannot_enroll(self):
        from GAME.TOOLS.recovery_roots import OperationalRootError
        interaction, _, _ = input_sources()
        with self.assertRaises(OperationalRootError):
            enumerate_operational_root_page("campaign-1", [("runtime.interaction", interaction)])
        promise = issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.interaction",
                                                  native_owner=interaction, scope="handoff")
        with self.assertRaises(OperationalRootError):
            enumerate_operational_root_page("campaign-1", [("runtime.interaction", interaction, deepcopy(promise))])
        interaction["state"]["input_message_id"] = "changed-M"
        with self.assertRaises(OperationalRootError):
            enumerate_operational_root_page("campaign-1", [("runtime.interaction", interaction, promise)])

    def test_plan_root_rejects_duplicate_units_and_forward_guard(self):
        _, _, plan = input_sources(kind="intent")
        duplicate = deepcopy(plan["state"]["clauses"][0])
        duplicate["order"] = 2
        plan["state"]["clauses"].append(duplicate)
        with self.assertRaises(DurabilityContractError):
            issue_durability_handoff_promise(campaign_id="campaign-1", owner_kind="runtime.intent_plan",
                                             native_owner=plan, scope="handoff")

    def test_unconsumed_response_root_requires_exact_offer_source(self):
        from DEV.TESTS.test_rd05_runtime_execution import _resolution_source
        from DEV.TESTS.test_rd07_recovery import FakeRepository
        from DEV.TESTS.test_rd12_collaboration import (
            _choice,
            _ordered_continuation,
        )
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import RecoveryFailure, _hydrate_input_root_closure

        interaction, message, _ = input_sources(kind="response")
        repository = FakeRepository()
        repository.files[route_native_record("runtime.message", (message["id"],)).relative_path] = message
        with self.assertRaises(RecoveryFailure):
            _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)
        target = interaction["state"]["response_target"]
        target.update(continuation_generation=3, offer_id="choice-1", responder_id="actor-bob")
        interaction["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = ["actor-bob"]
        interaction["state"]["response_selection"]["option_id"] = "option.left"
        command = retained_response_command(interaction)
        state = _resolution_source(command, status="AWAITING_CHOICE", continuation_id=target["continuation_id"])
        resolution = {"kind": "runtime.resolution", "id": target["resolution_id"], "state": state}
        continuation = _ordered_continuation(pending_response=_choice())
        for key in ("root_command_id", "activity_id", "actor_id", "target_ids", "parameter_bindings",
                    "ruleset_set_digest_generation", "ruleset_set_sha256", "catalog_context_fingerprint_generation",
                    "catalog_context_fingerprint", "invocation_facts", "fixed_rng_results", "prior_step_exports"):
            if key in state:
                continuation[key] = deepcopy(state[key])
        for record in (command, resolution, continuation):
            record["campaign_id"] = "campaign-1"
            repository.files[route_native_record(record["kind"], (record["id"],)).relative_path] = record
        _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)
        interaction["state"]["response_selection"]["option_id"] = "option.foreign"
        with self.assertRaises(RecoveryFailure):
            _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)


class ResponseMixedClosureTests(unittest.TestCase):
    """S3 deterministic source conformance; not a native consume/issuer proof."""

    def test_mixed_materialization_cannot_replace_extra_meaning_with_dummy_unit(self):
        interaction, message, _ = input_sources()
        segment = response_survivor(interaction, message)
        plan = mixed_plan(interaction)
        extra = plan["state"]["clauses"][1]
        del extra["normalized_semantics"]
        with self.assertRaises(ValueError):
            runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=interaction,
                message=message, plan=plan, accepted_response_segment=segment)

    def test_mixed_preserves_all_semantic_classes_guards_and_collection_metadata(self):
        from GAME.TOOLS.collaboration import CollaborationAdmissionError, _load_clause

        for semantic_class in ("OOC_COORDINATION", "DIEGETIC_COMMUNICATION", "CONTROL_SIGNAL", "ACTIONABLE_INTENT"):
            interaction, message, _ = input_sources()
            segment = response_survivor(interaction, message)
            plan = mixed_plan(interaction)
            extra = plan["state"]["clauses"][1]
            extra.update(collaboration_semantic_class=semantic_class,
                dependency_kind="JOINT_VOLUNTARY_ACTION", purpose="joint-entry",
                dependency_scope={"scene_id": "scene-market"},
                required_contributors=[{"player_id": "player-1", "pc_id": "actor-1"}],
                optional_contributors=[{"player_id": "player-2"}],
                native_basis_refs=[{"family": "world.scene", "id": "scene-market", "revision": "r1"}])
            later = deepcopy(extra)
            later.update(clause_id="clause.intent.2", order=3,
                guard={"prior_clause_id": "clause.intent.1", "source": "export", "export_id": "outcome",
                       "operator": "in", "literal_values": ["done", False, 0]})
            plan["state"]["clauses"].append(later)
            expected = deepcopy(plan)
            runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=interaction,
                message=message, plan=plan, accepted_response_segment=segment)
            self.assertEqual(plan, expected)
            self.assertEqual(_load_clause(plan["state"], "clause.intent.1"), extra)
            self.assertNotIn("command_id", extra)
            with self.assertRaises(CollaborationAdmissionError):
                _load_clause(plan["state"], "clause.response")

    def test_pure_response_and_swapped_mixed_sources_never_become_extra_commands(self):
        interaction, message, _ = input_sources(kind="response")
        segment = response_survivor(interaction, message)
        runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=interaction,
            message=message, plan=None, accepted_response_segment=segment)
        foreign_plan = input_sources(kind="intent")[2]
        with self.assertRaises(ValueError):
            runtime_execution.accepted_input_origin(campaign_id="campaign-1", interaction=interaction,
                message=message, plan=foreign_plan, clause_id="clause-1", accepted_response_segment=segment)
        interaction, message, _ = input_sources()
        segment = response_survivor(interaction, message)
        plan = mixed_plan(interaction)
        for mutate in (
            lambda i, p, s: i.update(id="another-I"),
            lambda i, p, s: i["state"].update(input_kind="response"),
            lambda i, p, s: p["state"].update(interaction_id="another-I"),
            lambda i, p, s: p["state"]["clauses"][0].update(command_id="synthetic-K"),
            lambda i, p, s: p["state"]["clauses"][0].update(normalized_semantics={"new": "response"}),
            lambda i, p, s: p["state"]["clauses"][1].update(clause_id="clause.intent.01"),
            lambda i, p, s: s["accepted_resume_input"].update(response_interaction_id="another-I"),
        ):
            wrong_i, wrong_p, wrong_s = deepcopy(interaction), deepcopy(plan), deepcopy(segment)
            mutate(wrong_i, wrong_p, wrong_s)
            with self.assertRaises(ValueError):
                runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=wrong_i,
                    message=message, plan=wrong_p, accepted_response_segment=wrong_s)

    def test_resume_codec_is_public_and_stable_across_same_i_planning(self):
        codec = getattr(runtime_execution, "resume_input_fingerprint", None)
        self.assertTrue(callable(codec), "S3 requires the single public resume codec")
        interaction, message, _ = input_sources()
        before = codec(interaction=interaction, message=message)
        segment = response_survivor(interaction, message)
        self.assertEqual(before, segment["accepted_resume_input"]["resume_fingerprint"])
        self.assertEqual(before, codec(interaction=interaction, message=message))
        plan = mixed_plan(interaction)
        self.assertEqual(before, codec(interaction=interaction, message=message))
        runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=interaction,
            message=message, plan=plan, accepted_response_segment=segment)

    def test_resume_codec_hashes_all_fixed_origin_target_selection_fields(self):
        codec = getattr(runtime_execution, "resume_input_fingerprint", None)
        self.assertTrue(callable(codec), "S3 requires the single public resume codec")
        interaction, message, _ = input_sources()
        before = codec(interaction=interaction, message=message)
        for field in interaction["state"]["response_target"]:
            if field == "offer_kind":
                continue
            wrong = deepcopy(interaction)
            wrong["state"]["response_target"][field] = 2 if field == "continuation_generation" else "foreign-id"
            if field == "responder_id":
                wrong["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = ["foreign-id"]
            with self.subTest(field=field):
                self.assertNotEqual(before, codec(interaction=wrong, message=message))
        for mutate in (
            lambda i: i["state"]["response_selection"].update(option_id="option-B"),
            lambda i: i["state"]["accepted_input_basis"].update(accepted_exchange_key="exchange-2"),
            lambda i: i["state"].update(input_kind="response"),
        ):
            wrong = deepcopy(interaction)
            mutate(wrong)
            if wrong["state"]["input_kind"] == "response":
                wrong["state"].pop("planning_phase")
            self.assertNotEqual(before, codec(interaction=wrong, message=message))
        for mutate in (
            lambda m: m.update(id="foreign-M"),
            lambda m: m["state"].update(exact_text="changed"),
            lambda m: m["state"].update(exact_text="\ud800"),
        ):
            wrong = deepcopy(message)
            mutate(wrong)
            with self.assertRaises(ValueError):
                codec(interaction=interaction, message=wrong)

    def test_marker_is_admitted_by_strict_dev_and_installed_segment_wire(self):
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        from GAME.TOOLS.structural_contracts import validate_contract

        root = Path(__file__).resolve().parents[2]
        schemas = [json.loads(path.read_text(encoding="utf-8")) for path in (root / "DEV/SCHEMAS").glob("*.json")]
        registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas if "$id" in s)
        schema = next(s for s in schemas if s.get("$id", "").endswith("/execution-segment.schema.json"))
        validator = Draft202012Validator(schema, registry=registry)
        interaction, message, _ = input_sources(kind="response")
        segment = response_survivor(interaction, message)
        self.assertTrue(validator.is_valid(segment), "W09 must admit the genuine embedded marker")
        validate_contract("execution-segment", segment)
        for field in segment["accepted_resume_input"]:
            wrong = deepcopy(segment)
            del wrong["accepted_resume_input"][field]
            self.assertFalse(validator.is_valid(wrong))
            with self.assertRaises(ValueError):
                validate_contract("execution-segment", wrong)
        for value in (True, 1.0, None):
            wrong = deepcopy(segment)
            wrong["accepted_resume_input"]["target"]["continuation_generation"] = value
            with self.assertRaises(ValueError):
                runtime_execution.validate_input_closure(campaign_id="campaign-1", interaction=interaction,
                    message=message, plan=None, accepted_response_segment=wrong)

    def test_later_pending_offer_can_retain_old_response_marker_without_replay(self):
        from DEV.TESTS.test_rd12_collaboration import _ordered_resolution

        interaction, message, _ = input_sources(kind="response")
        segment = response_survivor(interaction, message)
        resolution = _ordered_resolution()
        resolution.update(segments=[segment], next_segment_sequence=2)
        # A different current suspension is not the consumed offer or a retry.
        runtime_execution._ordering_resolution_schema(resolution)

    def test_direct_command_segment_cannot_carry_synthetic_response_marker(self):
        from GAME.TOOLS.structural_contracts import validate_contract

        interaction, message, _ = input_sources(kind="response")
        segment = response_survivor(interaction, message)
        segment["segment_id"] = "command-direct:segment:1"
        command = {"command_id": "command-direct", "command_kind": "transition",
                   "input_fingerprint_generation": 3, "input_fingerprint": "a" * 64}
        with self.assertRaises(ValueError):
            runtime_execution.execution_identity(command, execution_owner_kind="runtime.command",
                execution_owner_id="command-direct", segment=segment)
        contract = "https://hedgelion.invalid/schemas/runtime-command-state.schema.json#/properties/direct_transition_segments"
        with self.assertRaises(ValueError):
            validate_contract(contract, [segment])
        del segment["accepted_resume_input"]
        validate_contract(contract, [segment])


class InputRetentionSourceTests(unittest.TestCase):
    """S3 retained-source sufficiency, not native protection establishment."""

    @contextmanager
    def retained(self, *, materialized=False, kind="response_and_intent"):
        from DEV.TESTS.test_rd05_runtime_execution import (
            _bind_context,
            _candidate,
            _interpreter_result,
            _proposal,
            _resolution_source,
        )
        from GAME.TOOLS.native_storage import route_native_record

        proposal = _proposal()
        with trusted_command_source(proposal) as (host, records):
            command = runtime_execution.accept_command(_interpreter_result(), _bind_context(),
                _candidate(), proposal, input_observation=host._current_owner._observe_command_input(proposal))
            interaction, message, _ = input_sources(kind=kind)
            interaction["state"]["campaign_id"] = host._campaign_id
            interaction["state"]["accepted_input_basis"]["repository_identity"] = host._repository.repository_identity()
            interaction["state"]["accepted_input_basis"].update(
                accepted_exchange_key="response-exchange", host_invocation_ref="response-invocation")
            interaction["state"]["response_target"]["root_command_id"] = command["command_id"]
            segment = response_survivor(interaction, message)
            plan = mixed_plan(interaction) if materialized else None
            resolution = {"kind": "runtime.resolution", "id": "resolution-1",
                "state": _resolution_source(command, segments=[segment], next_segment_sequence=2)}
            def put(record):
                records[route_native_record(record["kind"], (record["id"],)).relative_path] = deepcopy(record)
            for record in (interaction, message, resolution,
                           {"kind": "runtime.command", "id": command["command_id"], **command}):
                put(record)
            if plan is not None:
                put(plan)
            promise = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=interaction, scope="handoff")
            records["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"] = enumerate_operational_root_page(
                host._campaign_id, [("runtime.interaction", interaction, promise)]).to_dict()
            adapter_path = host._accepted_input_capability.mapping_path
            mapping = json.loads(adapter_path.read_text(encoding="utf-8"))
            mapping.update(interaction_id=interaction["id"], exact_text=message["state"]["exact_text"],
                host_invocation_ref=interaction["state"]["accepted_input_basis"]["host_invocation_ref"])
            mapping["key"][4] = interaction["state"]["accepted_input_basis"]["accepted_exchange_key"]
            adapter_path.write_text(json.dumps(mapping), encoding="utf-8")

            def resolve_catalog(pin, accepted, catalog_basis):
                # Existing recovery source port returns a real owner-admitted
                # context. The production reader independently checks it and all
                # native input/codec bindings; this is not a callback verdict.
                if accepted["command_kind"] == "transition":
                    from DEV.TESTS.sp02_installed_test_support import (
                        authentic_generic_catalog,
                    )

                    context, candidate = authentic_generic_catalog().catalog_context, None
                else:
                    context, candidate = _bind_context(), _candidate()
                if pin != host._repository.pin_campaign(host._campaign_id) or context.to_dict() != catalog_basis:
                    raise ValueError("accepted catalog interpretation source differs")
                return context, candidate
            host._repository.resolve_recovery_catalog_context = resolve_catalog
            yield host, records, interaction, message, plan, promise, put

    def validator(self):
        validator = getattr(__import__("GAME.TOOLS.durability", fromlist=["validate_input_handoff_sources"]),
                            "validate_input_handoff_sources", None)
        self.assertTrue(callable(validator), "S3 needs actual retained-source sufficiency validation")
        return validator

    def check_response_binding_mutations(self, fields):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, i, _m, _p, promise, _put):
            target = i["state"]["response_target"]
            path = route_native_record("runtime.resolution", (target["resolution_id"],)).relative_path
            command = runtime_execution.native_command_state(
                records[route_native_record("runtime.command", (target["root_command_id"],)).relative_path],
                command_id=target["root_command_id"], campaign_id=host._campaign_id)
            valid = deepcopy(records[path])
            for field in fields:
                records[path] = deepcopy(valid)
                validate(promise, host=host)
                state = records[path]["state"]
                runtime_execution._validate_action_resolution_binding(command, target["resolution_id"], state)
                state[field] = response_binding_mutations()[field]
                runtime_execution.validate_retained_resolution(resolution_id=target["resolution_id"], resolution=records[path])
                with self.assertRaises(ValueError):
                    runtime_execution._validate_action_resolution_binding(command, target["resolution_id"], state)
                with self.subTest(field=field), self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_r3_response_root_actor_must_match_its_actual_k_request(self):
        self.check_response_binding_mutations(("actor_id",))

    def test_r3_response_root_activity_must_match_its_actual_k_request(self):
        self.check_response_binding_mutations(("activity_id",))

    def test_r3_response_root_initiating_command_must_match_actual_k(self):
        self.check_response_binding_mutations(("initiating_command_id",))

    def test_r3_response_root_catalog_facts_and_roles_must_match_actual_k(self):
        self.check_response_binding_mutations(("catalog_context_fingerprint", "ruleset_set_sha256", "invocation_facts", "target_ids"))

    @contextmanager
    def cold_response_sources(self):
        from GAME.TOOLS.recovery import CurrentNativeSource

        with self.retained() as (host, records, interaction, _m, _p, _promise, put):
            class ColdRepository:
                def __init__(self):
                    self.reads = []

                def pin_campaign(self, campaign_id):
                    return host._repository.pin_campaign(campaign_id)

                def read_exact_path(self, pinned, path):
                    self.reads.append(path)
                    return host._repository.read_exact_path(pinned, path)

                def select_current_native_sources(self, pinned):
                    return (CurrentNativeSource(pinned.campaign_id, "campaign", pinned.campaign_id,
                        pinned.revision, "MANIFEST.yaml"),)

            yield ColdRepository(), host._campaign_id, records, interaction, put

    def test_r3_cold_response_root_binding_rejects_shape_valid_contradictions(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import recover_current_runtime

        with self.cold_response_sources() as (repository, campaign_id, records, _i, _put):
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            valid = deepcopy(records[path])
            for field, value in response_binding_mutations().items():
                records[path] = deepcopy(valid)
                self.assertEqual(recover_current_runtime(repository, campaign_id).disposition.value, "READY")
                records[path]["state"][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    recover_current_runtime(repository, campaign_id)

    def check_cold_missing_response_dependency(self, kind):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import (
            RecoveryFailure,
            RecoveryFailureCode,
            recover_current_runtime,
        )

        with self.cold_response_sources() as (repository, campaign_id, records, _i, _put):
            self.assertEqual(recover_current_runtime(repository, campaign_id).disposition.value, "READY")
            state = records[route_native_record("runtime.resolution", ("resolution-1",)).relative_path]["state"]
            segment = state["segments"][0]
            if kind == "event":
                segment["event_ids"] = ["resolution-1:segment:1:event:1"]
            elif kind == "child":
                state["child_resolution_ids"] = ["missing-child"]
                segment["pending_child_invocations"] = [{"firing_key": "fixed-child",
                    "root_command_id": state["root_command_id"], "activity_id": state["activity_id"],
                    "trigger_ref": segment["segment_id"], "reason": "mandatory_followup",
                    "child_resolution_id": "missing-child"}]
            else:
                state.update(status="AWAITING_CHOICE", continuation_id="continuation-next")
                segment.update(resulting_execution_state="AWAITING_CHOICE", continuation_id="continuation-next")
            runtime_execution.validate_retained_resolution(resolution_id="resolution-1", resolution={
                "kind": "runtime.resolution", "id": "resolution-1", "state": state})
            with self.assertRaises(RecoveryFailure) as raised:
                recover_current_runtime(repository, campaign_id)
            self.assertEqual(raised.exception.code, RecoveryFailureCode.MISSING)

    def test_cold_ready_response_requires_its_declared_native_event(self):
        self.check_cold_missing_response_dependency("event")

    def test_cold_ready_response_requires_its_declared_native_child(self):
        self.check_cold_missing_response_dependency("child")

    def test_cold_ready_response_requires_current_next_continuation(self):
        self.check_cold_missing_response_dependency("continuation")

    def test_cold_ready_response_loads_cumulative_results_child_and_next_offer_without_old_offer(self):
        from DEV.TESTS.test_rd12_collaboration import _choice, _ordered_continuation
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import (
            RecoveryFailure,
            RecoveryFailureCode,
            recover_current_runtime,
        )

        with self.cold_response_sources() as (repository, campaign_id, records, interaction, put):
            target = interaction["state"]["response_target"]
            root_id = target["root_command_id"]
            message = records[route_native_record("runtime.message", (interaction["state"]["input_message_id"],)).relative_path]
            target["responder_id"] = "actor-other"
            interaction["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = ["actor-other"]
            consumed = response_survivor(interaction, message)
            put(interaction)
            state = records[route_native_record("runtime.resolution", ("resolution-1",)).relative_path]["state"]
            self.assertNotEqual(state["actor_id"], target["responder_id"])
            next_segment = retained_eventless_segment("resolution-1")
            next_segment.update(segment_id="resolution-1:segment:2", segment_sequence=2,
                resulting_execution_state="AWAITING_CHOICE", continuation_id="continuation-next")
            next_segment["pending_child_invocations"] = [{"firing_key": "response-child-key",
                "root_command_id": root_id, "activity_id": state["activity_id"],
                "trigger_ref": next_segment["segment_id"], "reason": "mandatory_followup",
                "child_resolution_id": "response-child"}]
            state.update(segments=[consumed, next_segment], next_segment_sequence=3,
                child_resolution_ids=["response-child"], status="AWAITING_CHOICE", continuation_id="continuation-next")
            event_paths = []
            for segment in state["segments"]:
                event_id = segment["segment_id"] + ":event:1"
                segment["event_ids"] = [event_id]
                put({"kind": "runtime.mechanical_event", "id": event_id, "state": {
                    "segment_id": segment["segment_id"], "event_ordinal": 1, "event_kind": "event.test.response",
                    "root_command_id": root_id, "causal_ref": "resolution-1", "payload": {"segment": segment["segment_sequence"]}}})
                event_paths.append(route_native_record("runtime.mechanical_event", (event_id,)).relative_path)
            child = deepcopy(state)
            child.pop("initiating_command_id")
            child.pop("continuation_id")
            child.update(resolution_id="response-child", causal_invocation_key="response-child-key", status="COMPLETED",
                segments=[retained_eventless_segment("response-child")], next_segment_sequence=2, child_resolution_ids=[])
            put({"kind": "runtime.resolution", "id": "response-child", "state": child})
            offer = _choice()
            offer.update(offer_id="offer-next", continuation_generation=2, responder_id="actor-next")
            continuation = _ordered_continuation(pending_response=offer)
            continuation.update(id="continuation-next", campaign_id=campaign_id, generation=2,
                expected_child_resolution_ids=["response-child"],
                committed_segment_refs=[segment["segment_id"] for segment in state["segments"]])
            for key in ("root_command_id", "activity_id", "actor_id", "target_ids", "parameter_bindings",
                        "ruleset_set_digest_generation", "ruleset_set_sha256", "catalog_context_fingerprint_generation",
                        "catalog_context_fingerprint", "invocation_facts", "fixed_rng_results", "prior_step_exports"):
                if key in state:
                    continuation[key] = deepcopy(state[key])
            put(continuation)
            paths = event_paths + [route_native_record("runtime.resolution", ("response-child",)).relative_path,
                route_native_record("runtime.continuation", ("continuation-next",)).relative_path]
            old_offer_path = route_native_record("runtime.continuation", (target["continuation_id"],)).relative_path
            self.assertNotIn(old_offer_path, records)
            self.assertNotIn("intent_plan_id", interaction["state"])
            self.assertEqual(recover_current_runtime(repository, campaign_id).disposition.value, "READY")
            self.assertTrue(set(paths) <= set(repository.reads))
            self.assertNotIn(old_offer_path, repository.reads)
            self.assertFalse(any("INTENT_PLANS" in path or "PLAYERS" in path for path in repository.reads))
            for path in paths:
                saved = records.pop(path)
                with self.subTest(path=path), self.assertRaises(RecoveryFailure) as raised:
                    recover_current_runtime(repository, campaign_id)
                self.assertEqual(raised.exception.code, RecoveryFailureCode.MISSING)
                records[path] = saved
                self.assertEqual(recover_current_runtime(repository, campaign_id).disposition.value, "READY")
            for path, container, field, wrong in (
                (event_paths[0], "state", "root_command_id", "foreign-command"),
                (route_native_record("runtime.resolution", ("response-child",)).relative_path,
                 "state", "causal_invocation_key", "foreign-child-key"),
                (route_native_record("runtime.continuation", ("continuation-next",)).relative_path,
                 None, "generation", True),
            ):
                saved = deepcopy(records[path])
                target_state = records[path] if container is None else records[path][container]
                target_state[field] = wrong
                with self.subTest(path=path, field=field), self.assertRaises(ValueError):
                    recover_current_runtime(repository, campaign_id)
                records[path] = saved
                self.assertEqual(recover_current_runtime(repository, campaign_id).disposition.value, "READY")

    @contextmanager
    def retained_extra(self, *, direct=False, pending=False):
        from DEV.TESTS.test_rd05_runtime_execution import _resolution_source
        from GAME.TOOLS.native_storage import route_native_record

        with self.retained(materialized=True) as (host, records, i, m, p, promise, put):
            command = deepcopy(next(v for v in records.values() if v.get("kind") == "runtime.command"))
            command.update(id="extra-command", command_id="extra-command", interaction_id=i["id"],
                intent_plan_id=p["id"], clause_id="clause.intent.1", disposition="command.accepted" if pending else "command.settled")
            clause = p["state"]["clauses"][1]
            clause.update(command_id=command["command_id"], collaboration_semantic_class="ACTIONABLE_INTENT",
                mapping_outcome="exact", execution_state="intent.ready" if pending else "intent.executed",
                normalized_semantics={"request": "move"})
            segment = {"schema_version": 1, "segment_id": "resolution-extra:segment:1", "segment_sequence": 1,
                "commit_state": "committed", "resulting_execution_state": "COMPLETED", "event_ids": [],
                "pending_child_invocations": [], "receipt_exports": {}, "affected_revision_refs": []}
            if direct:
                from DEV.TESTS.sp02_installed_test_support import (
                    authentic_generic_catalog,
                )

                context = authentic_generic_catalog().catalog_context
                for field in ("action_request", "root_resolution_id", "interpreter_result", "interpreter_result_fingerprint_generation",
                              "interpreter_result_fingerprint", "candidate_binding"):
                    command.pop(field, None)
                actor = records[route_native_record("world.actor", ("actor-1",)).relative_path]
                command.update(command_kind="transition", catalog_context=context.to_dict(), catalog_context_fingerprint=context.fingerprint,
                    transition_request={"transition_kind": "transition.location_change", "payload": {
                        "transition_kind": "transition.location_change", "profile_id": "location_change.outside_procedure",
                        "idempotency_key": "retained-extra-move", "catalog_generation": 2, "actor_id": "actor-1",
                        "actor_revision": actor["state_revision"], "destination_location_id": "location-2",
                        "destination_location_revision": 1, "movement_cost": "NOT_APPLICABLE_OUTSIDE_PROCEDURE"}},
                    transition_binding={"profile_id": "location_change.outside_procedure", "profile_generation": 1,
                        "payload_schema_id": "https://hedgelion.invalid/schemas/gameplay-spine-transition-request.schema.json#/$defs/outsideProcedureMovement",
                        "payload_schema_version": 1})
                put({"kind": "world.location", "id": "location-2", "state_revision": 1, "state": {}})
                if not pending:
                    segment["segment_id"] = "extra-command:segment:1"
                    command.update(direct_transition_segments=[segment], direct_transition_receipt={"execution_owner_id": "extra-command",
                        "segment_refs": [segment["segment_id"]], "status": "COMPLETED", "event_ids": [], "exports": {}, "pending_child_refs": []})
            else:
                command["root_resolution_id"] = "resolution-extra"
                put({"kind": "runtime.resolution", "id": "resolution-extra", "state": _resolution_source(command,
                    segments=[segment], next_segment_sequence=2)})
            put(p)
            prior = records[route_native_record("runtime.resolution", ("resolution-1",)).relative_path]["state"]["segments"][0]
            origin = runtime_execution.accepted_input_origin(campaign_id=host._campaign_id, interaction=i,
                message=m, plan=p, clause_id=clause["clause_id"], accepted_response_segment=prior)
            command["input_fingerprint"] = runtime_execution.command_input_fingerprint(command, origin=origin)
            put(command)
            yield host, records, promise, put, command

    def test_r2_complete_extra_action_root_is_distinct_and_missing_result_holds(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained_extra() as (host, records, promise, _put, _command):
            validate(promise, host=host)
            actual_resolver = host._repository.resolve_recovery_catalog_context
            host._repository.resolve_recovery_catalog_context = None
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            host._repository.resolve_recovery_catalog_context = lambda *_args: (True, None)
            with self.assertRaises(ValueError):
                validate(promise, host=host)  # Existing port cannot substitute a callback verdict for admitted context.
            host._repository.resolve_recovery_catalog_context = actual_resolver
            validate(promise, host=host)
            records.pop(route_native_record("runtime.resolution", ("resolution-extra",)).relative_path)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_r2_direct_pending_eventless_and_required_event_receipt_sources(self):
        import os

        from GAME.TOOLS.native_storage import route_native_record

        if "HDM_INSTALLED_STRUCTURAL_TEST" not in os.environ:
            from DEV.TESTS.sp02_installed_test_support import (
                run_installed_structural_test,
            )

            result = run_installed_structural_test("DEV.TESTS.test_sp03_authenticated_input.InputRetentionSourceTests."
                "test_r2_direct_pending_eventless_and_required_event_receipt_sources")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return
        validate = self.validator()
        with self.retained_extra(direct=True, pending=True) as (host, _records, promise, put, command):
            validate(promise, host=host)
            command["disposition"] = "command.settled"
            put(command)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
        with self.retained_extra(direct=True) as (host, records, promise, put, command):
            validate(promise, host=host)
            valid = deepcopy(command)
            command.pop("direct_transition_receipt")
            put(command)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            command = valid
            segment = command["direct_transition_segments"][0]
            event_id = segment["segment_id"] + ":event:1"
            segment["event_ids"] = [event_id]
            command["direct_transition_receipt"]["event_ids"] = [event_id]
            put(command)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            event = {"kind": "runtime.mechanical_event", "id": event_id, "state": {
                "segment_id": segment["segment_id"], "event_ordinal": 1, "event_kind": "event.test.transition",
                "root_command_id": command["command_id"], "causal_ref": command["command_id"], "payload": {}}}
            put(event)
            validate(promise, host=host)
            records[route_native_record("runtime.mechanical_event", (event_id,)).relative_path]["state"]["causal_ref"] = "foreign"
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_r2_executed_extra_unit_requires_settled_native_mandatory_closure(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained_extra() as (host, records, promise, put, command):
            validate(promise, host=host)
            command["disposition"] = "command.accepted"
            put(command)
            with self.assertRaises(ValueError):
                validate(promise, host=host)  # Executed clause cannot be a settlement assertion.
            command["disposition"] = "command.settled"
            put(command)
            path = route_native_record("runtime.resolution", ("resolution-extra",)).relative_path
            parent = records[path]["state"]
            parent["child_resolution_ids"] = ["extra-child"]
            parent["segments"][0]["pending_child_invocations"] = [{"firing_key": "extra-child-key",
                "root_command_id": command["command_id"], "activity_id": parent["activity_id"],
                "trigger_ref": parent["segments"][0]["segment_id"], "reason": "mandatory_followup",
                "child_resolution_id": "extra-child"}]
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            child = deepcopy(records[path])
            child.update(id="extra-child")
            child["state"].pop("initiating_command_id")
            child["state"].update(resolution_id="extra-child", causal_invocation_key="extra-child-key",
                child_resolution_ids=[], segments=[retained_eventless_segment("extra-child")], next_segment_sequence=2)
            put(child)
            validate(promise, host=host)
            child_event_id = "extra-child:segment:1:event:1"
            child["state"]["segments"][0]["event_ids"] = [child_event_id]
            put(child)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            child_event = {"kind": "runtime.mechanical_event", "id": child_event_id, "state": {
                "segment_id": "extra-child:segment:1", "event_ordinal": 1, "event_kind": "event.test.child",
                "root_command_id": command["command_id"], "causal_ref": "extra-child", "payload": {}}}
            put(child_event)
            validate(promise, host=host)
            from GAME.TOOLS.recovery import _hydrate_input_root_closure

            interaction = records[route_native_record("runtime.interaction", ("interaction-1",)).relative_path]
            _hydrate_input_root_closure(host._repository, host._repository.pin_campaign(host._campaign_id), interaction)
            records[route_native_record("runtime.mechanical_event", (child_event_id,)).relative_path]["id"] = "foreign-event"
            with self.assertRaises(ValueError):
                _hydrate_input_root_closure(host._repository, host._repository.pin_campaign(host._campaign_id), interaction)
            put(child_event)
            child["state"]["status"] = "RUNNING"
            put(child)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            child["state"].update(status="COMPLETED", segments=[], next_segment_sequence=1)
            put(child)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_r2_cold_input_reader_cannot_skip_populated_extra_action_result(self):
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.recovery import _hydrate_input_root_closure

        with self.retained_extra() as (host, records, _promise, _put, _command):
            interaction = records[route_native_record("runtime.interaction", ("interaction-1",)).relative_path]
            pin = host._repository.pin_campaign(host._campaign_id)
            _hydrate_input_root_closure(host._repository, pin, interaction)
            records.pop(route_native_record("runtime.resolution", ("resolution-extra",)).relative_path)
            with self.assertRaises(ValueError):
                _hydrate_input_root_closure(host._repository, pin, interaction)

    def test_r1_open_normalized_shape_is_not_positive_content_survivor_evidence(self):
        validate = self.validator()
        for meaning in ({"opaque": "a" * 64}, {"content_digest": {"sha256": "a" * 64}},
                        {"request": "move later"}):
            with self.retained(materialized=True) as (host, _records, _i, m, p, promise, put):
                p["state"]["clauses"][1]["normalized_semantics"] = meaning
                put(p)
                validate(promise, host=host)  # Exact M is actual retained content.
                m["state"].pop("exact_text")
                m["state"]["payload_state"] = "message.compacted"
                put(m)
                with self.subTest(meaning=meaning), self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_r2_settled_extra_action_requires_its_distinct_native_result(self):
        validate = self.validator()
        with self.retained(materialized=True) as (host, records, i, m, p, promise, put):
            validate(promise, host=host)
            command = deepcopy(next(v for v in records.values() if v.get("kind") == "runtime.command"))
            command.update(id="extra-command", command_id="extra-command", interaction_id=i["id"],
                intent_plan_id=p["id"], clause_id="clause.intent.1", root_resolution_id="missing-extra-resolution",
                disposition="command.settled")
            p["state"]["clauses"][1].update(command_id=command["id"], collaboration_semantic_class="ACTIONABLE_INTENT",
                mapping_outcome="exact", execution_state="intent.executed", normalized_semantics={"request": "move"})
            put(p)
            segment = next(v for v in records.values() if v.get("kind") == "runtime.resolution")["state"]["segments"][0]
            origin = runtime_execution.accepted_input_origin(campaign_id=host._campaign_id, interaction=i,
                message=m, plan=p, clause_id="clause.intent.1", accepted_response_segment=segment)
            command["input_fingerprint"] = runtime_execution.command_input_fingerprint(command, origin=origin)
            put(command)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_r3_response_relational_closure_rejects_missing_current_forward_sources(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        for case in ("awaiting", "frontier", "declared-child"):
            with self.retained() as (host, records, _i, _m, _p, promise, _put):
                validate(promise, host=host)
                state = records[route_native_record("runtime.resolution", ("resolution-1",)).relative_path]["state"]
                if case == "awaiting":
                    state["status"] = "AWAITING_CHOICE"
                elif case == "frontier":
                    state["next_segment_sequence"] = 1
                else:
                    state["segments"][0]["pending_child_invocations"] = [{"firing_key": "fixed-child",
                        "root_command_id": state["root_command_id"], "activity_id": state["activity_id"],
                        "trigger_ref": state["segments"][0]["segment_id"], "reason": "mandatory_followup",
                        "child_resolution_id": "missing-declared-child"}]
                with self.subTest(case=case), self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_r3_old_segment_continuation_can_retire_only_after_its_actual_consume(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, i, _m, _p, _promise, put):
            state = records[route_native_record("runtime.resolution", ("resolution-1",)).relative_path]["state"]
            consume = state["segments"][0]
            consume.update(segment_id="resolution-1:segment:2", segment_sequence=2)
            i["state"]["accepted_resume_ref"]["segment_id"] = consume["segment_id"]
            put(i)
            offered = retained_eventless_segment("resolution-1")
            offered.update(resulting_execution_state="AWAITING_CHOICE", continuation_id="continuation-1")
            state.update(segments=[offered, consume], next_segment_sequence=3)
            promise = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            validate(promise, host=host)
            offered["continuation_id"] = "missing-unconsumed-continuation"
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_ready_exact_same_source_root_and_response_closure_is_sufficient(self):
        validate = self.validator()
        with self.retained() as (host, _records, i, m, p, promise, put):
            self.assertIsNone(p)
            validate(promise, host=host)
            # An outbound acknowledgement has no effect on remaining input.
            i["state"]["response_message_id"] = "outbound-1"
            put(i)
            changed = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            validate(changed, host=host)
            m["state"].pop("exact_text")
            m["state"]["payload_state"] = "message.compacted"
            put(m)
            with self.assertRaises(ValueError):
                validate(changed, host=host)

    def test_bool_hash_copied_promise_and_callback_host_never_prove_protection(self):
        from types import SimpleNamespace

        validate = self.validator()
        with self.retained() as (host, _records, _i, _m, _p, promise, _put):
            validate(promise, host=host)
            for evidence in (True, "a" * 64, deepcopy(promise), SimpleNamespace(validate=lambda **kw: True)):
                with self.subTest(evidence=type(evidence).__name__), self.assertRaises(ValueError):
                    validate(evidence, host=host)
            with self.assertRaises(ValueError):
                validate(promise, host=SimpleNamespace(_current_owner=host._current_owner))

    def test_unknown_root_protection_and_missing_response_survivor_hold(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, _i, _m, _p, promise, _put):
            root_path = "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"
            page = records.pop(root_path)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            records[root_path] = dict(page, roots=[])
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            records[root_path] = page
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            records[path]["state"]["segments"][0].pop("accepted_resume_input")
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_selected_live_input_does_not_fall_back_to_campaign_protection(self):
        from GAME.TOOLS.live_state import (
            LiveClaim,
            LiveEnvelope,
            LiveNativeStatePack,
            LiveRouting,
            build_live_ref,
            derive_live_epoch_id,
        )

        validate = self.validator()
        with self.retained() as (host, _records, i, _m, _p, promise, _put):
            claim = LiveClaim.exact_owner("runtime.interaction", i["id"])
            opening = "b" * 40
            epoch = derive_live_epoch_id(host._campaign_id, "scene.test", opening, (claim,))
            source = LiveEnvelope(campaign_id=host._campaign_id, scene_id="scene.test", epoch_id=epoch,
                source_ref=build_live_ref(host._campaign_id, "scene.test", epoch), source_revision="c" * 40,
                opening_campaign_revision=opening, claims=(claim,))
            host._live_transport.route = LiveRouting(campaign_id=host._campaign_id, entries=(source,))
            host._live_transport.pack = LiveNativeStatePack(source_key=source.source_key,
                source_revision=source.source_revision, next_source_native_creation_ordinal=1, source_native_ids=(),
                native_owner_states={"runtime.interaction": deepcopy(i)}, provenance={}, privacy={}, chronology={}, unresolved_work={})
            with self.assertRaisesRegex(ValueError, "cross-source protection/freeze is unavailable"):
                validate(promise, host=host)

    def test_plan_root_survivor_covers_every_no_k_unit_before_i_root_release(self):
        validate = self.validator()
        with self.retained(materialized=True) as (host, records, _i, m, p, promise, put):
            for n, semantic_class in enumerate(("DIEGETIC_COMMUNICATION", "CONTROL_SIGNAL", "ACTIONABLE_INTENT"), 2):
                clause = deepcopy(p["state"]["clauses"][1])
                clause.update(clause_id=f"clause.intent.{n}", order=n + 1,
                    collaboration_semantic_class=semantic_class,
                    normalized_semantics={"request": f"retained unit {n}"})
                p["state"]["clauses"].append(clause)
            put(p)
            pp = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.intent_plan", native_owner=p, scope="handoff")
            records["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"] = enumerate_operational_root_page(
                host._campaign_id, [("runtime.intent_plan", p, pp)]).to_dict()
            validate(promise, host=host)
            # Each unit, including held/nonexecutable, must retain its meaning.
            for index in range(1, len(p["state"]["clauses"])):
                wrong = deepcopy(p)
                wrong["state"]["clauses"][index].pop("normalized_semantics")
                put(wrong)
                with self.assertRaises(ValueError):
                    validate(promise, host=host)
            put(p)
            m["state"].pop("exact_text")
            m["state"]["payload_state"] = "message.compacted"
            put(m)
            with self.assertRaises(ValueError):
                validate(promise, host=host)  # Open normalized shape is not a sufficient survivor.

    def test_exact_refs_and_opaque_digest_are_not_content_discharge(self):
        validate = self.validator()
        with self.retained(materialized=True) as (host, _records, _i, m, p, promise, put):
            validate(promise, host=host)
            p["state"]["clauses"][1]["material_exact_text_refs"] = ["unknown-natural-owner"]
            put(p)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

            p["state"]["clauses"][1].pop("material_exact_text_refs")
            p["state"]["clauses"][1]["normalized_semantics"] = {"content_digest": "a" * 64}
            put(p)
            m["state"].pop("exact_text")
            m["state"]["payload_state"] = "message.compacted"
            put(m)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_declared_native_basis_is_required_even_for_a_no_k_held_unit(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained(materialized=True) as (host, records, _i, _m, p, promise, put):
            p["state"]["clauses"][1]["native_basis_refs"] = [{"family": "world.scene", "id": "scene-1", "revision": "scene-r1"}]
            put(p)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            scene = {"kind": "world.scene", "id": "scene-1", "revision": "scene-r1", "state": {}}
            put(scene)
            validate(promise, host=host)
            records.pop(route_native_record("world.scene", ("scene-1",)).relative_path)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_native_result_children_and_fixed_cause_cannot_be_omitted(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, _i, _m, _p, promise, _put):
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            source = deepcopy(records[path])
            for field, value in (("child_resolution_ids", ["missing-child"]),
                                 ("fixed_rng_results", [{"digest": "b" * 64}])):
                records[path] = deepcopy(source)
                records[path]["state"][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_actual_child_and_event_survivors_are_read_before_sufficiency(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, _i, _m, _p, promise, put):
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            state = records[path]["state"]
            child = deepcopy(records[path])
            child["id"] = "resolution-child"
            child["state"].update(resolution_id="resolution-child",
                segments=[retained_eventless_segment("resolution-child")], next_segment_sequence=2)
            child["state"].pop("initiating_command_id")
            child["state"]["causal_invocation_key"] = "fixed-child-key"
            state["child_resolution_ids"] = [child["id"]]
            put(child)
            segment = state["segments"][0]
            segment["pending_child_invocations"] = [{"firing_key": "fixed-child-key",
                "root_command_id": state["root_command_id"], "activity_id": child["state"]["activity_id"],
                "trigger_ref": segment["segment_id"], "reason": "mandatory_followup",
                "child_resolution_id": child["id"]}]
            event_id = segment["segment_id"] + ":event:1"
            segment["event_ids"] = [event_id]
            event = {"kind": "runtime.mechanical_event", "id": event_id, "state": {
                "segment_id": segment["segment_id"], "event_ordinal": 1,
                "event_kind": "event.test.response", "root_command_id": state["root_command_id"],
                "causal_ref": "resolution-1", "payload": {"selected_option_id": "option-A"}}}
            put(event)
            validate(promise, host=host)
            put({"kind": event["kind"], "id": event["id"], **deepcopy(event["state"])})
            validate(promise, host=host)
            child["state"]["causal_invocation_key"] = "foreign-child-key"
            put(child)
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            child["state"]["causal_invocation_key"] = "fixed-child-key"
            put(child)
            event["state"]["causal_ref"] = "foreign-resolution"
            put(event)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_settled_response_k_root_does_not_discover_unplanned_or_no_k_extras(self):
        validate = self.validator()
        for materialized in (False, True):
            with self.retained(materialized=materialized) as (host, records, i, _m, _p, promise, _put):
                root_page = records["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"]
                root = root_page["roots"][0]
                from GAME.TOOLS.native_storage import route_native_record

                command_id = i["state"]["response_target"]["root_command_id"]
                records[route_native_record("runtime.command", (command_id,)).relative_path]["disposition"] = "command.settled"
                root.update(owner_kind="runtime.command", owner_id=command_id,
                    route={"family_key": "runtime.command", "identity": [command_id],
                           "relative_path": route_native_record("runtime.command", (command_id,)).relative_path})
                with self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_relevant_input_and_root_movement_during_source_window_hold(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        for changed in ("interaction", "roots"):
            with self.retained() as (host, records, i, m, _p, promise, put):
                repository = host._repository
                original = repository.read_exact_path
                message_path = route_native_record("runtime.message", (m["id"],)).relative_path
                triggered = False
                def moving(pin, path, *, original=original, message_path=message_path, changed=changed):
                    nonlocal triggered
                    result = original(pin, path)
                    if path == message_path and not triggered:
                        triggered = True
                        if changed == "interaction":
                            i["state"]["response_message_id"] = "new-outbound"
                            put(i)
                        else:
                            records["STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"]["roots"] = []
                    return result
                repository.read_exact_path = moving
                with self.subTest(changed=changed), self.assertRaises(ValueError):
                    validate(promise, host=host)

    def test_expanding_source_union_cannot_accept_an_unvisited_new_child(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, _i, m, _p, promise, _put):
            repository = host._repository
            original = repository.read_exact_path
            message_path = route_native_record("runtime.message", (m["id"],)).relative_path
            resolution_path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            message_reads = 0
            def moving(pin, path):
                nonlocal message_reads
                if path == message_path:
                    message_reads += 1
                    if message_reads == 2:
                        records[resolution_path]["state"]["child_resolution_ids"] = ["new-unvisited-child"]
                return original(pin, path)
            repository.read_exact_path = moving
            with self.assertRaisesRegex(ValueError, "REVALIDATION_REQUIRED"):
                validate(promise, host=host)

    def test_cold_ready_keeps_old_marker_after_offer_retirement_without_plan(self):
        from GAME.TOOLS.recovery import _hydrate_input_root_closure

        validate = self.validator()
        for kind in ("response", "response_and_intent"):
            with self.retained(kind=kind) as (host, _records, i, m, p, promise, put):
                validate(promise, host=host)
                _hydrate_input_root_closure(host._repository,
                    host._repository.pin_campaign(host._campaign_id), i)
                # No current/old Continuation or Player is needed for historical
                # retrieval; no P is allocated for either retained pre-plan case.
                self.assertIsNone(p)
                source = deepcopy(i)
                source["id"] = "different-I"
                m["state"]["interaction_id"] = source["id"]
                put(m)
                with self.assertRaises(ValueError):
                    _hydrate_input_root_closure(host._repository,
                        host._repository.pin_campaign(host._campaign_id), source)

    def test_new_suspension_keeps_old_marker_but_requires_its_current_native_source(self):
        from DEV.TESTS.test_rd12_collaboration import _choice, _ordered_continuation
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained() as (host, records, i, _m, _p, promise, put):
            continuation = _ordered_continuation()
            continuation.update(id="continuation-next", campaign_id=host._campaign_id,
                generation=2, root_command_id=i["state"]["response_target"]["root_command_id"])
            offer = _choice()
            offer.update(continuation_generation=2, offer_id="choice-next")
            continuation["pending_response"] = offer
            put(continuation)
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            records[path]["state"].update(continuation_id=continuation["id"], status="AWAITING_CHOICE")
            validate(promise, host=host)
            continuation["generation"] = True
            put(continuation)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

            continuation["generation"] = 2
            continuation.pop("pending_response")
            put(continuation)
            with self.assertRaises(ValueError):
                validate(promise, host=host)

    def test_unconsumed_native_envelope_offer_retains_exact_candidate_without_fake_p(self):
        from DEV.TESTS.test_rd12_collaboration import _ordered_continuation
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained(kind="response") as (host, records, i, _m, _p, _promise, put):
            i["state"].pop("accepted_resume_ref")
            put(i)
            target = i["state"]["response_target"]
            path = route_native_record("runtime.resolution", (target["resolution_id"],)).relative_path
            state = records[path]["state"]
            state.update(status="AWAITING_CHOICE", continuation_id=target["continuation_id"],
                segments=[], next_segment_sequence=1)
            continuation = _ordered_continuation()
            continuation.update(campaign_id=host._campaign_id, generation=target["continuation_generation"])
            for key in ("root_command_id", "activity_id", "actor_id", "target_ids", "parameter_bindings",
                        "ruleset_set_digest_generation", "ruleset_set_sha256", "catalog_context_fingerprint_generation",
                        "catalog_context_fingerprint", "invocation_facts", "fixed_rng_results", "prior_step_exports"):
                if key in state:
                    continuation[key] = deepcopy(state[key])
            continuation["pending_response"] = {"kind": "choice", "offer_id": target["offer_id"],
                "parent_resolution_id": target["resolution_id"], "continuation_generation": target["continuation_generation"],
                "responder_id": target["responder_id"], "option_ids": ["option-A", "option-B"]}
            put(continuation)
            promise = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            validate(promise, host=host)
            i["state"]["response_selection"]["option_id"] = "foreign-option"
            put(i)
            wrong = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            with self.assertRaises(ValueError):
                validate(wrong, host=host)

    def test_response_root_author_and_responder_need_not_be_the_same_actor(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained(kind="response") as (host, records, i, m, _p, promise, put):
            i["state"]["response_target"]["responder_id"] = "actor-other"
            i["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = ["actor-other"]
            segment = response_survivor(i, m)
            put(i)
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            records[path]["state"]["segments"] = [segment]
            promise = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            validate(promise, host=host)

    def test_reaction_selected_native_child_survives_with_different_root_actor(self):
        from GAME.TOOLS.native_storage import route_native_record

        validate = self.validator()
        with self.retained(kind="response") as (host, records, i, m, _p, promise, put):
            i["state"]["response_target"].update(offer_kind="reaction", responder_id="actor-other")
            i["state"]["response_selection"] = {"kind": "reaction", "activity_id": "activity.check.generic"}
            i["state"]["accepted_input_basis"]["authority_at_acceptance"]["accepted_subject_ids"] = ["actor-other"]
            segment = response_survivor(i, m)
            put(i)
            path = route_native_record("runtime.resolution", ("resolution-1",)).relative_path
            state = records[path]["state"]
            state["segments"] = [segment]
            state["child_resolution_ids"] = ["reaction-child"]
            promise = issue_durability_handoff_promise(campaign_id=host._campaign_id,
                owner_kind="runtime.interaction", native_owner=i, scope="handoff")
            with self.assertRaises(ValueError):
                validate(promise, host=host)
            child = deepcopy(records[path])
            child["id"] = "reaction-child"
            child["state"].pop("initiating_command_id")
            child["state"].update(resolution_id="reaction-child", actor_id="actor-other",
                segments=[retained_eventless_segment("reaction-child")], child_resolution_ids=[],
                next_segment_sequence=2, causal_invocation_key="fixed-reaction")
            put(child)
            state["child_resolution_ids"] = [child["id"]]
            segment["pending_child_invocations"] = [{"firing_key": "fixed-reaction",
                "root_command_id": state["root_command_id"], "activity_id": "activity.check.generic",
                "trigger_ref": segment["segment_id"], "reason": "mandatory_followup",
                "child_resolution_id": child["id"]}]
            validate(promise, host=host)

    def test_mixed_extra_action_and_direct_move_bind_same_i_and_fixed_resume(self):
        import os

        from DEV.TESTS.test_rd05_runtime_execution import (
            _bind_context,
            _candidate,
            _interpreter_result,
        )
        from GAME.TOOLS.native_storage import route_native_record

        if "HDM_INSTALLED_STRUCTURAL_TEST" not in os.environ:
            from DEV.TESTS.sp02_installed_test_support import (
                run_installed_structural_test,
            )

            result = run_installed_structural_test(
                "DEV.TESTS.test_sp03_authenticated_input.InputRetentionSourceTests."
                "test_mixed_extra_action_and_direct_move_bind_same_i_and_fixed_resume")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return

        for direct in (False, True):
            with self.retained(materialized=True) as (host, records, i, m, p, _promise, put):
                basis = i["state"]["accepted_input_basis"]
                adapter_path = host._accepted_input_capability.mapping_path
                mapping = json.loads(adapter_path.read_text(encoding="utf-8"))
                mapping.update(interaction_id=i["id"], exact_text=m["state"]["exact_text"])
                mapping["key"][4] = basis["accepted_exchange_key"]
                mapping["host_invocation_ref"] = basis["host_invocation_ref"]
                adapter_path.write_text(json.dumps(mapping), encoding="utf-8")
                p["state"]["clauses"][1].update(mapping_outcome="exact", execution_state="intent.ready",
                    collaboration_semantic_class="ACTIONABLE_INTENT", normalized_semantics={"request": "move"})
                put(p)
                command = {"command_id": "extra-command", "interaction_id": i["id"],
                    "intent_plan_id": p["id"], "clause_id": "clause.intent.1"}
                if direct:
                    records[route_native_record("world.location", ("location-2",)).relative_path] = {
                        "kind": "world.location", "id": "location-2", "state_revision": 1, "state": {}}
                    command.update(command_kind="transition", transition_request={
                        "transition_kind": "transition.location_change", "payload": {
                            "transition_kind": "transition.location_change", "profile_id": "location_change.outside_procedure",
                            "idempotency_key": "move-extra", "catalog_generation": 2, "actor_id": "actor-1",
                            "actor_revision": records[route_native_record("world.actor", ("actor-1",)).relative_path]["state_revision"],
                            "destination_location_id": "location-2", "destination_location_revision": 1,
                            "movement_cost": "NOT_APPLICABLE_OUTSIDE_PROCEDURE"}},
                        transition_binding={"profile_id": "location_change.outside_procedure", "profile_generation": 1,
                            "payload_schema_id": "https://hedgelion.invalid/schemas/gameplay-spine-transition-request.schema.json#/$defs/outsideProcedureMovement",
                            "payload_schema_version": 1})
                else:
                    command.update(action_request={"activity_id": "activity.check.generic", "actor_id": "actor-1", "target_ids": ["actor-2"]},
                        root_resolution_id="resolution-extra")
                observed = host._current_owner._observe_command_input(command)
                from DEV.TESTS.sp02_installed_test_support import (
                    authentic_generic_catalog,
                )

                accepted = runtime_execution.accept_command(None if direct else _interpreter_result(),
                    authentic_generic_catalog().catalog_context if direct else _bind_context(),
                    None if direct else _candidate(), command, input_observation=observed)
                self.assertEqual(accepted["interaction_id"], i["id"])
                self.assertEqual(accepted["intent_plan_id"], p["id"])
                self.assertEqual(basis["principal"]["stable_account_id"], "123")
                fixed = runtime_execution.resume_input_fingerprint(interaction=i, message=m)
                origin = runtime_execution.accepted_input_origin(campaign_id=host._campaign_id,
                    interaction=i, message=m, plan=p, clause_id="clause.intent.1",
                    accepted_response_segment=records[next(path for path in records if path.endswith(".yaml")
                        and records[path].get("kind") == "runtime.resolution")]["state"]["segments"][0])
                self.assertEqual(origin["accepted_resume_ref"], i["state"]["accepted_resume_ref"])
                self.assertEqual(accepted["input_fingerprint"], runtime_execution.command_input_fingerprint(accepted, origin=origin))
                self.assertEqual(fixed, runtime_execution.resume_input_fingerprint(interaction=i, message=m))


if __name__ == "__main__":
    unittest.main()
