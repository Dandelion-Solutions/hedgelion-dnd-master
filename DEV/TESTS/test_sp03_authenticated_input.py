"""Trusted native source conformance only; no external authentication issuance."""

import hashlib
import unittest
from copy import deepcopy

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
    return {"segment_id": reference["segment_id"], "segment_sequence": 1,
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
            resolution_id = interaction["state"]["accepted_resume_ref"]["resolution_id"]
            repository.files[route_native_record("runtime.resolution", (resolution_id,)).relative_path] = {
                "kind": "runtime.resolution", "id": resolution_id, "state": {
                    "root_command_id": interaction["state"]["response_target"]["root_command_id"],
                    "segments": [deepcopy(segment)],
                },
            }
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
            repository.put({"kind": "runtime.resolution", "id": "resolution-1", "state": {
                "root_command_id": "command-1", "segments": [segment],
            }})
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
        from DEV.TESTS.test_rd07_recovery import FakeRepository
        from DEV.TESTS.test_rd12_collaboration import (
            _choice,
            _ordered_continuation,
            _ordered_resolution,
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
        for record in (_ordered_resolution(), _ordered_continuation(pending_response=_choice())):
            record["campaign_id"] = "campaign-1"
            repository.files[route_native_record(record["kind"], (record["id"],)).relative_path] = record
        _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)
        interaction["state"]["response_selection"]["option_id"] = "option.foreign"
        with self.assertRaises(RecoveryFailure):
            _hydrate_input_root_closure(repository, repository.pin_campaign("campaign-1"), interaction)


if __name__ == "__main__":
    unittest.main()
