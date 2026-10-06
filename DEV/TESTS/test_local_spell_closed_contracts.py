"""Structural spell contracts do not confer native mutation permission."""

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.actor_continuity import (
    ActorContinuityError,
    validate_actor_delta,
    validate_actor_source,
)

ROOT = Path(__file__).resolve().parents[2]


def actor(state):
    return {"schema_version": 2, "id": "actor.carrier", "kind": "world.actor",
            "state_revision": 1, "state": state}


def validators():
    registry = Registry()
    for path in (ROOT / "DEV/SCHEMAS").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    schema = json.loads((ROOT / "DEV/SCHEMAS/world-actor-state.schema.json").read_text())
    return Draft202012Validator(schema, registry=registry)


def fragment_validator(name, fragment):
    registry = validators()._registry
    return Draft202012Validator(
        {"$ref": f"https://hedgelion.invalid/schemas/{name}.schema.json#/$defs/{fragment}"},
        registry=registry,
    )


class SpellClosedContractTests(unittest.TestCase):
    def test_typed_foundation_is_immutable_and_cannot_issue_execution_authority(self):
        self.assertIsNotNone(importlib.util.find_spec("GAME.TOOLS.activity_contracts"), "typed foundation is absent")
        from dataclasses import FrozenInstanceError

        from GAME.TOOLS import activity_contracts as contracts

        binding = contracts.SubjectBinding("actor.principal", "actor.body", 1)
        with self.assertRaises(FrozenInstanceError):
            binding.binding_generation = 2
        for values in (("bad id", "actor.body", 1), ("actor.principal", "actor.body", True)):
            with self.assertRaises(contracts.ActivityContractError):
                contracts.SubjectBinding(*values)
        for cls in (contracts.AdmittedActivityCatalog, contracts.CompiledActivity,
                    contracts.NativePreparationContext, contracts.PreparedNativeFragment,
                    contracts.NativeSegmentPlan, contracts.NativeSegmentEstablishment):
            with self.assertRaises((contracts.ActivityContractError, TypeError)):
                cls()
        for result in ("zero_original_policy", "principal_dead"):
            with self.assertRaises(contracts.ActivityContractError):
                contracts.TruePolymorphObjectReturnAdjudicationResult(
                    "entry_current_normalized", result, "terminal_damage_overflow_to_return"
                )
        state = contracts.PrismaticSprayRaysState(0, 2, "APPLY_RAYS", (1, 1), ("roll.one", "roll.two"))
        self.assertEqual(state.accepted_rays, (1, 1))
        with self.assertRaises(contracts.ActivityContractError):
            contracts.PrismaticSprayRaysState(0, 2, "APPLY_RAYS", (1, 8), ())

    def test_foundation_profile_check_requires_actual_inventory_and_occurrence(self):
        self.assertIsNotNone(importlib.util.find_spec("GAME.TOOLS.activity_contracts"))
        from GAME.TOOLS import activity_contracts as contracts

        binding = contracts.ProfileBinding("activity.cast.step.0", "execution.spell_cast.srd521", 1)
        with self.assertRaises(contracts.ActivityContractError):
            contracts.validate_profile_bindings((binding,), occurrence_ids=(binding.consumer_id,), admitted_contracts=())
        with self.assertRaises(contracts.ActivityContractError):
            contracts.validate_profile_bindings((binding,), occurrence_ids=(), admitted_contracts=((binding.profile_id, 1, binding.consumer_id),))
        contracts.validate_profile_bindings((binding,), occurrence_ids=(binding.consumer_id,), admitted_contracts=((binding.profile_id, 1, binding.consumer_id),))

    def test_source_bound_catalog_dto_detaches_nested_values_without_claiming_compilation(self):
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS import activity_contracts as contracts

        context = _bind_context()
        source = json.loads((ROOT / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json").read_text())
        record = next(record for record in source["activity_definitions"] if record["id"] == "activity.check.generic")
        data = copy.deepcopy(record["data"])
        data["details"] = {"notes": ["source.one"]}
        definitions = {record["id"]: {"id": record["id"], "kind": record["kind"], "name": {"en": record["id"]}, "data": data}}
        members = {("hdm.rules.dnd2024-srd52-core", "character-mvp-seed.json"): b"frozen source bytes"}
        value = contracts.AdmittedActivityCatalog(
            context, members, definitions, context.basis["engine_contract_inventory"], 1, "mode.conformance", {}, {}, {}, {},
            _issue_seal=contracts._CONTRACT_SEAL,
        )
        definitions["activity.check.generic"]["data"]["details"]["notes"].append("source.changed")
        members.clear()
        self.assertEqual(value.frozen_definitions["activity.check.generic"]["data"]["details"]["notes"], ("source.one",))
        self.assertTrue(value.frozen_semantic_members)
        with self.assertRaises(TypeError):
            value.frozen_definitions["activity.check.generic"]["data"]["details"]["notes"] = ()
        # This private trusted construction tests the DTO only, not SP02 compiler issuance.
        with self.assertRaises(contracts.ActivityContractError):
            contracts.ProfileBinding("activity.one", "execution.foreign", 1)

    def test_preparation_contract_uses_real_p0_observation_and_rejects_foreign_session_handles(self):
        from dataclasses import replace

        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
            _proposal,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            ACTOR_ID,
            ActorRepository,
            _actor,
            _selected_host,
        )
        from GAME.TOOLS import activity_contracts as contracts
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.runtime_execution import accept_command

        context = _bind_context()
        catalog = contracts.AdmittedActivityCatalog(context, {}, {}, context.basis["engine_contract_inventory"], 1, "mode.conformance", {}, {}, {}, {}, _issue_seal=contracts._CONTRACT_SEAL)
        with self.assertRaises(contracts.ActivityContractError):
            replace(catalog, engine_contract_inventory={})
        compiled = contracts.CompiledActivity(
            activity_id="activity.check.generic", definition_semantic_hash="a" * 64, definition_semantic_hash_generation=1,
            ruleset_set_sha256=context.basis["ruleset_lock"]["ruleset_set_sha256"], ruleset_set_digest_generation=1,
            catalog_context_fingerprint=context.fingerprint, catalog_context_fingerprint_generation=1,
            compiler_generation=1, engine_contract_inventory_sha256=context.basis["engine_contract_inventory_sha256"],
            mode_policy_profile_id="mode.conformance", instructions=(contracts.CompiledInstruction("activity.check.generic.step.0", "op.resolve_check", {"roll": {"export_ref": "roll.result", "value_kind": "prior_roll_result"}, "threshold": {"parameter_ref": "dc", "value_kind": "integer"}}, (), ()),), parameter_contracts={}, role_contracts={"actor": {"family_key": "world.actor", "required": True}}, export_contracts={},
            consumer_read_plan=(), dependency_ids=(), cost_contract_refs=(), native_transition_contract_refs=(), timing_contract_refs=(),
            profile_bindings=(), safe_recompute_phases=(), _issue_seal=contracts._CONTRACT_SEAL,
        )
        with NativeHotStore(":memory:") as store:
            child_actor_id = "actor.child"
            child_actor = copy.deepcopy(_actor())
            child_actor["id"] = child_actor_id

            class ChildActorRepository(ActorRepository):
                def read_exact_path(self, pinned, path):
                    child_path = route_native_record(
                        "world.actor", (child_actor_id,)
                    ).relative_path
                    if path == child_path:
                        return copy.deepcopy(child_actor)
                    return super().read_exact_path(pinned, path)

            host, _source = _selected_host(
                store, repository=ChildActorRepository()
            )
            session = host._current_owner.begin(host._begin_operation())
            owner = NativeOwnerRef("world.actor", (ACTOR_ID,))
            observation = session.require((owner,))
            token = object()
            handle = contracts.NativeAllocationHandle(owner, "occ.one", "allocation.one", token, _issue_seal=contracts._CONTRACT_SEAL)
            proposal = _proposal()
            proposal["action_request"]["actor_id"] = ACTOR_ID
            accepted = accept_command(_interpreter_result(), context, _candidate(), proposal)
            resolution = {"root_command_id": accepted["command_id"], "initiating_command_id": accepted["command_id"],
                "activity_id": compiled.activity_id, "actor_id": ACTOR_ID,
                "ruleset_set_digest_generation": 1, "ruleset_set_sha256": compiled.ruleset_set_sha256,
                "catalog_context_fingerprint_generation": 1, "catalog_context_fingerprint": context.fingerprint,
                "status": "RUNNING", "next_segment_sequence": 1, "invocation_facts": [], "fixed_rng_results": [],
                "prior_step_exports": {}, "child_resolution_ids": [], "segments": []}
            preparation = contracts.NativePreparationContext(
                catalog=catalog, compiled=compiled, consumer_id="activity.check.generic.step.0", occurrence_id="occ.one",
                execution_ref=contracts.ExecutionRef(accepted["command_id"], accepted["root_resolution_id"]), observation=observation, owner_session=session,
                role_bindings={"actor": owner}, accepted_command=accepted, resolution=resolution, accepted_fact_refs=(), accepted_adjudication=(),
                policy_refs=(), fixed_roll_refs=(), prospective_owner_documents=(), allocation_handles=(handle,),
                _builder_token=token, _issue_seal=contracts._CONTRACT_SEAL,
            )
            self.assertEqual(preparation.observation.observation_fingerprint, observation.observation_fingerprint)
            for change in ({"accepted_command": {}}, {"resolution": {}}, {"accepted_command": dict(accepted, hp=10)}, {"resolution": dict(resolution, patch={})}):
                with self.assertRaises(contracts.ActivityContractError):
                    replace(preparation, **change)
            with self.assertRaises(contracts.ActivityContractError):
                replace(preparation, resolution=dict(resolution, activity_id="activity.foreign"))
            with self.assertRaises(contracts.ActivityContractError):
                replace(preparation, owner_session=host._current_owner.begin(host._begin_operation()))
            with self.assertRaises(contracts.ActivityContractError):
                replace(preparation, allocation_handles=(replace(handle, _builder_token=object()),))
            with self.assertRaises(contracts.ActivityContractError):
                replace(preparation, consumer_id="activity.foreign.step.0")
            with self.assertRaises(contracts.ActivityContractError):
                replace(compiled, instructions=())

            child_owner = NativeOwnerRef("world.actor", (child_actor_id,))
            child_observation = session.require((child_owner,))
            child_compiled = replace(
                compiled,
                activity_id="activity.followup",
                instructions=(contracts.CompiledInstruction(
                    "activity.followup.step.0",
                    "op.resolve_check",
                    {
                        "roll": {"export_ref": "roll.result", "value_kind": "prior_roll_result"},
                        "threshold": {"parameter_ref": "dc", "value_kind": "integer"},
                    },
                    (),
                    (),
                ),),
            )
            child_handle = contracts.NativeAllocationHandle(
                child_owner,
                "occ.child",
                "allocation.child",
                token,
                _issue_seal=contracts._CONTRACT_SEAL,
            )
            child_resolution = dict(
                resolution,
                activity_id=child_compiled.activity_id,
                actor_id=child_actor_id,
                causal_invocation_key="resolution-1:segment:1:event:1",
            )
            child_resolution.pop("initiating_command_id")
            child_preparation = contracts.NativePreparationContext(
                catalog=catalog,
                compiled=child_compiled,
                consumer_id="activity.followup.step.0",
                occurrence_id="occ.child",
                execution_ref=contracts.ExecutionRef(
                    accepted["command_id"], "resolution.child"
                ),
                observation=child_observation,
                owner_session=session,
                role_bindings={"actor": child_owner},
                accepted_command=accepted,
                resolution=child_resolution,
                accepted_fact_refs=(),
                accepted_adjudication=(),
                policy_refs=(),
                fixed_roll_refs=(),
                prospective_owner_documents=(),
                allocation_handles=(child_handle,),
                _builder_token=token,
                _issue_seal=contracts._CONTRACT_SEAL,
            )
            self.assertEqual(child_preparation.execution_ref.resolution_id, "resolution.child")
            self.assertEqual(child_preparation.compiled.activity_id, "activity.followup")
            self.assertEqual(child_preparation.resolution["actor_id"], child_actor_id)
            for invalid_resolution in (
                {key: value for key, value in child_resolution.items() if key != "causal_invocation_key"},
                dict(child_resolution, root_command_id="command.foreign"),
                dict(child_resolution, activity_id="activity.foreign"),
                dict(child_resolution, actor_id=ACTOR_ID),
            ):
                with self.assertRaises(contracts.ActivityContractError):
                    replace(child_preparation, resolution=invalid_resolution)
        # No native mutation, RNG, compiler output or establishment was performed.

    def test_native_cause_and_object_basis_dtos_reject_amount_substitution(self):
        from GAME.TOOLS import activity_contracts as contracts

        common = {"cause_occurrence_id": "occ.cause", "principal_subject_id": "actor.one", "physical_actor_id": "actor.one",
                  "source_actor_id": "actor.source", "origin_subject_id": "actor.source", "health_policy_id": "health.srd521", "life_state_policy_id": "life_policy.dnd2024.character_like"}
        damage = contracts.DamageComponent(7, "damage.fire", "origin.spell")
        contracts.TypedHealthCause("damage", **common, damage_instance_id="damage.one", damage_components=(damage,))
        contracts.TypedHealthCause("healing", **common, healing_result_ref="result.heal")
        contracts.TypedHealthCause("maximum_change", **common, maximum_contribution_ref="contribution.max")
        contracts.TypedHealthCause("instant_death", **common, killing_profile_id="killing.source")
        with self.assertRaises(contracts.ActivityContractError):
            contracts.TypedHealthCause("instant_death", **common, killing_profile_id="killing.source", damage_instance_id="damage.one")
        with self.assertRaises((TypeError, contracts.ActivityContractError)):
            contracts.TypedObjectReturnCause("effect.convert", 1, "occ.end", "object_destruction", "observation.one", "basis.return", "basis.ruling", residual=10)
        with self.assertRaises(contracts.ActivityContractError):
            contracts.EntryHealth(10, 10, temporary=0, temporary_source=contracts.TemporaryHpSource("occ.grant"))
        with self.assertRaises(contracts.ActivityContractError):
            contracts.AssetDamageResult("occ.damage", "asset.object", 10, 5, 0, 6, "damage.one", "actor.one", "damage.fire", (), (), _issue_seal=contracts._CONTRACT_SEAL)

    def test_profile_and_schema_rosters_are_exactly_equal(self):
        from GAME.TOOLS import activity_contracts as contracts

        schema = json.loads((ROOT / "DEV/SCHEMAS/spell-native-profile-values.schema.json").read_text())
        self.assertEqual(set(schema["$defs"]["profileId"]["enum"]), contracts.SELECTED_PROFILE_IDS)
        self.assertEqual(set(contracts.StochasticState.__args__), {contracts.TeleportMishapState, contracts.PrismaticSprayRaysState, contracts.ReincarnateChoiceState})

    def test_progress_dto_decoder_and_details_validator_match_all_closed_profiles(self):
        from GAME.TOOLS import activity_contracts as contracts

        cases = json.loads((ROOT / "DEV/TESTS/fixtures/local-spells/SP01/branches.json").read_text())
        for case in cases:
            if case["fragment"] == "spellProgress":
                value = contracts.validate_spell_progress(case["value"])
                self.assertEqual(value.profile_id, case["value"]["profile_id"])
                with self.assertRaises(contracts.ActivityContractError):
                    contracts.validate_spell_progress(dict(case["value"], amount=10))
        contracts.validate_nonexecutable_details({"notes": ["descriptive", {"color": "red"}]})
        with self.assertRaises(contracts.ActivityContractError):
            contracts.validate_nonexecutable_details({"notes": [{"form_state": {}}]})

    def test_real_current_seed_validates_but_structural_profile_binding_does_not_activate_it(self):
        from DEV.TOOLS.activity_primitive_contracts import (
            load_activity_primitive_contracts,
        )
        from DEV.TOOLS.validate_character_mvp_seed import resolve_package

        package = ROOT / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
        primitive_catalog = load_activity_primitive_contracts(ROOT)
        resolve_package(package, primitive_catalog)
        with tempfile.TemporaryDirectory(prefix="sp01-source-") as directory:
            copied = Path(directory) / "package"
            shutil.copytree(package, copied)
            seed_path = copied / "character-mvp-seed.json"
            seed = json.loads(seed_path.read_text())
            activity = seed["activity_definitions"][0]
            activity["data"]["profile_bindings"] = [{"consumer_id": activity["id"], "profile_id": "execution.spell_cast.srd521", "profile_generation": 1}]
            seed_path.write_text(json.dumps(seed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "profile.*not admitted"):
                resolve_package(copied, primitive_catalog)

    def test_capability_relational_validator_rejects_foreign_duplicate_unsorted_and_mode_rosters(self):
        from GAME.TOOLS import activity_contracts as contracts

        value = {"schema_version": 1, "identity_source": "ruleset-package-manifest.json", "profile_id": "spell.srd52.local", "content_basis": "SRD_5_2_1", "coverage_stage": "PARTIAL", "supported_srd_spell_ids": ["spell.one"], "existing_extra_spell_ids": [], "mode_bindings": [{"spell_id": "spell.one", "mode_id": "mode.cast", "activity_id": "activity.one"}], "unsupported_content_policy": "ABSENT_NONSELECTABLE", "notice": "NOTICE.md"}
        inputs = {"supported_srd_ids": ("spell.one",), "existing_extra_ids": (), "mode_bindings": (("spell.one", "mode.cast", "activity.one"),)}
        contracts.validate_spell_capabilities(value, **inputs)
        for change in ({"supported_srd_spell_ids": ["spell.foreign"]}, {"supported_srd_spell_ids": ["spell.one", "spell.one"]}, {"mode_bindings": []}, {"existing_extra_spell_ids": ["spell.one"]}, {"coverage_stage": "MECHANICALLY_COMPLETE"}):
            with self.assertRaises(contracts.ActivityContractError):
                contracts.validate_spell_capabilities(dict(value, **change), **inputs)
        ambiguous = dict(value, mode_bindings=[value["mode_bindings"][0], {"spell_id": "spell.one", "mode_id": "mode.cast", "activity_id": "activity.other"}])
        with self.assertRaises(contracts.ActivityContractError):
            contracts.validate_spell_capabilities(ambiguous, **dict(inputs, mode_bindings=(("spell.one", "mode.cast", "activity.one"), ("spell.one", "mode.cast", "activity.other"))))

    def test_trigger_cutover_rejects_legacy_bindings_and_unknown_effect_schema(self):
        validator = fragment_validator("spell-native-profile-values", "temporalOccurrence")
        with self.assertRaises(ValidationError):
            validator.validate({"basis_id": "temporal.metric_deadline", "context_id": "scene.one", "anchor_value": 0, "deadline_value": 1, "unit_id": "unit.hour"})
        schema = json.loads((ROOT / "DEV/SCHEMAS/world-record.schema.json").read_text())
        validator = Draft202012Validator(schema, registry=validators()._registry)
        value = {"schema_version": 2, "id": "effect.one", "kind": "world.effect", "definition_id": "effect.one", "state": {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}}
        validator.validate(value)
        for version in (1, 3, True):
            with self.assertRaises(ValidationError):
                validator.validate(dict(value, schema_version=version))

    def test_revision_refs_preserve_native_source_basis_and_absent_local_ordinals(self):
        from GAME.TOOLS import activity_contracts as contracts
        from GAME.TOOLS.current_owner import NativeOwnerRef

        contracts.OwnerRevisionRef(NativeOwnerRef("world.asset", ("asset.one",)), "LIVE/scene-one@012345", None, "a" * 64)
        value = {"owner_ref": {"family_key": "world.asset", "identity": ["asset.one"]}, "source_basis": "LIVE/scene-one@012345", "generation": None, "fingerprint": "a" * 64}
        fragment_validator("spell-native-profile-values", "ownerRevisionRef").validate(value)
        with self.assertRaises(contracts.ActivityContractError):
            contracts.OwnerRevisionRef(NativeOwnerRef("world.actor", ("actor.one",)), "campaign@012345", None, "a" * 64)

    def test_roll_targets_can_reference_noncasting_execution_without_fictitious_cast_generation(self):
        from GAME.TOOLS import activity_contracts as contracts

        execution = contracts.ExecutionRef("command.attack", "resolution.attack")
        contracts.RollRef(execution, "roll.attack", "occ.attack", 1)
        reference = {"command_id": "command.attack", "resolution_id": "resolution.attack"}
        fragment_validator("spell-native-profile-values", "executionRef").validate(reference)
        with self.assertRaises(ValidationError):
            fragment_validator("spell-native-profile-values", "castExecutionRef").validate(reference)

    def test_holds_and_pending_source_preparation_carry_no_unaccepted_receipts(self):
        from GAME.TOOLS import activity_contracts as contracts
        from GAME.TOOLS.current_owner import NativeOwnerRef

        execution = contracts.ExecutionRef("command.one", "resolution.one")
        receipt = contracts.ReceiptRef(execution, "segment.one", "receipt.one")
        with self.assertRaises(contracts.ActivityContractError):
            contracts.WishSourcePreparationReceipt("live.one", "CLOSE_PENDING", "frontier.one", receipt)
        proof = contracts.OwnerRevisionRef(NativeOwnerRef("world.asset", ("asset.one",)), "campaign@0123", None, "a" * 64)
        with self.assertRaises(contracts.ActivityContractError):
            contracts.NativeSegmentEstablishment("CAPACITY_REQUIRED", "campaign.one", execution, "a" * 64,
                "segment.one", (proof,), (proof,), ("continuation.one",), _issue_seal=contracts._CONTRACT_SEAL)

    def test_optional_native_members_embed_exact_branch_shapes(self):
        cases = json.loads((ROOT / "DEV/TESTS/fixtures/local-spells/SP01/branches.json").read_text())
        bindings = {
            "effect-subject": ("world-effect-state", "subject_binding", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "form": ("world-effect-state", "form_state", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "concentration": ("world-effect-state", "concentration_state", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "jar-container": ("world-effect-state", "identity_state", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "creature-object": ("world-effect-state", "conversion_state", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "control": ("world-effect-state", "control_state", {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}}),
            "equipment": ("world-asset-state", "equipment_transform", {}),
            "replica": ("world-asset-state", "replica_origin", {}),
            "membership": ("world-asset-state", "conversion_membership", {}),
            "portal": ("world-connection-state", "portal_state", {"from_location_id": "location.one", "to_location_id": "location.two"}),
            "traversal": ("world-connection-state", "traversal_profile", {"from_location_id": "location.one", "to_location_id": "location.two"}),
            "place": ("world-location-state", "spell_place", {"name": "Pocket"}),
        }
        registry = validators()._registry
        for case in cases:
            if case["key"] not in bindings:
                continue
            name, member, base = bindings[case["key"]]
            validator = Draft202012Validator({"$ref": f"https://hedgelion.invalid/schemas/{name}.schema.json"}, registry=registry)
            with self.subTest(member=member):
                validator.validate(dict(base, **{member: case["value"]}))
                with self.assertRaises(ValidationError):
                    validator.validate(dict(base, **{member: dict(case["value"], amount=10)}))

    def test_runtime_states_keep_stochastic_and_wish_separate(self):
        registry = validators()._registry
        ray = {"profile_id": "execution.stochastic.prismatic_spray_rays", "profile_generation": 1,
               "target_ordinal": 0, "secondary_draw_ordinal": 0, "phase": "INITIAL_DRAW", "accepted_rays": [], "fixed_draw_refs": []}
        for name in ("runtime-resolution-state", "runtime-continuation-state"):
            schema = json.loads((ROOT / f"DEV/SCHEMAS/{name}.schema.json").read_text())
            base = schema["examples"][0]
            validator = Draft202012Validator(schema, registry=registry)
            validator.validate(dict(base, stochastic_state=ray))
            with self.assertRaises(ValidationError):
                validator.validate(dict(base, reconciliation_state=ray))
            with self.assertRaises(ValidationError):
                validator.validate(dict(base, details={"stochastic_state": ray}))

    def test_profile_bindings_are_closed_but_do_not_admit_production_consumers(self):
        schema = json.loads((ROOT / "DEV/SCHEMAS/activity-definition-data.schema.json").read_text())
        validator = Draft202012Validator(schema, registry=validators()._registry)
        base = {"family_id": "activity.spell", "steps": [{"op": "op.roll"}],
                "profile_bindings": [{"consumer_id": "activity.spell.step.0", "profile_id": "execution.spell_cast.srd521", "profile_generation": 1}]}
        validator.validate(base)
        for change in ({"profile_id": "execution.foreign"}, {"profile_generation": 2}, {"payload": {}}):
            bad = copy.deepcopy(base)
            bad["profile_bindings"][0].update(change)
            with self.assertRaises(ValidationError):
                validator.validate(bad)
        with self.assertRaises(ValidationError):
            validator.validate(dict(base, details={"profile_args": {"hp": 3}}))

    def test_casting_procedure_retains_native_resources_and_temporal_binding(self):
        schema = json.loads((ROOT / "DEV/SCHEMAS/runtime-procedure-state.schema.json").read_text())
        validator = Draft202012Validator(schema, registry=validators()._registry)
        cast = {"profile_id": "execution.spell_cast.long", "activity_id": "activity.cast",
                "execution_ref": {"command_id": "command.cast", "resolution_id": "resolution.cast", "cast_generation": 1},
                "subject_binding": {"principal_subject_id": "actor.one", "physical_actor_id": "actor.one", "binding_generation": 1},
                "phase": "CASTING", "temporal_binding": {"basis_id": "temporal.metric_deadline", "context_id": "scene.one", "anchor_value": 0, "deadline_value": 1, "unit_id": "unit.minute"},
                "concentration_effect_id": "effect.cast"}
        base = {"schema_version": 2, "lifecycle": "ACTIVE", "participant_resources": {}, "casting_state": cast}
        validator.validate(base)
        with self.assertRaises(ValidationError):
            validator.validate(dict(base, casting_state=dict(cast, resource_amounts={"slot": 1})))
        with self.assertRaises(ValidationError):
            validator.validate(dict(base, lifecycle="TERMINAL"))

    def test_spell_capability_and_support_projections_are_closed(self):
        registry = validators()._registry
        for name, value in (
            ("spell-capabilities", {"schema_version": 1, "identity_source": "ruleset-package-manifest.json", "profile_id": "spell.srd52.local", "content_basis": "SRD_5_2_1", "coverage_stage": "PARTIAL", "supported_srd_spell_ids": [], "existing_extra_spell_ids": [], "mode_bindings": [], "unsupported_content_policy": "ABSENT_NONSELECTABLE", "notice": "NOTICE.md"}),
            ("spell-support-row", {"spell_id": "spell.one", "mode_id": "mode.cast", "requirement_key": "requirement.cost", "source_witness_ref": "source.one", "activity_id": "activity.one", "compiled_consumer_ids": ["activity.one.step.0"], "dependency_ids": [], "contract_refs": [], **{key: {"status": "NOT_ESTABLISHED", "proof_refs": []} for key in ("source_closure", "definition_closure", "machine_admission", "production_realization", "scenario_verification", "target_performance")}}),
        ):
            path = ROOT / f"DEV/SCHEMAS/{name}.schema.json"
            self.assertTrue(path.is_file(), f"{name} is missing")
            validator = Draft202012Validator(json.loads(path.read_text()), registry=registry)
            validator.validate(value)
            with self.assertRaises(ValidationError):
                validator.validate(dict(value, supported=True))
            if name == "spell-support-row":
                with self.assertRaises(ValidationError):
                    validator.validate(dict(value, target_performance={"status": "PASS", "proof_refs": ["proof.one"]}))

    def test_all_new_native_branches_are_closed_and_reject_foreign_members(self):
        path = ROOT / "DEV/TESTS/fixtures/local-spells/SP01/branches.json"
        self.assertTrue(path.is_file(), "SP01 branch witnesses must exist")
        cases = json.loads(path.read_text(encoding="utf-8"))
        for case in cases:
            with self.subTest(branch=case["key"]):
                schema_path = ROOT / f"DEV/SCHEMAS/{case['schema']}.schema.json"
                self.assertTrue(schema_path.is_file(), "SP01 must materialize closed shapes")
                validator = fragment_validator(case["schema"], case["fragment"])
                validator.validate(case["value"])
                with self.assertRaises(ValidationError):
                    validator.validate(dict(case["value"], prospective_delta={"hp": 99}))
                for invalid in case.get("invalid", []):
                    with self.assertRaises(ValidationError):
                        validator.validate(invalid)
                for key in ("profile_id", "phase", "mode", "domain"):
                    if key in case["value"]:
                        with self.assertRaises(ValidationError):
                            validator.validate(dict(case["value"], **{key: "FOREIGN"}))
                for key in ("profile_generation", "generation", "binding_generation", "relation_generation"):
                    if key in case["value"]:
                        with self.assertRaises(ValidationError):
                            validator.validate(dict(case["value"], **{key: True}))

    def test_actor_progress_is_structural_and_remains_owner_local(self):
        state = {"spell_progress": {"progress.prayer": {"profile_id": "lifecycle.progress.rest_gate",
                  "consumed": True, "reset_boundary_id": "boundary.long_rest", "last_transition_occurrence": "occ.rest"}}}
        self.assert_actor_valid(state)
        for change in ({"amount": 1}, {"consumed": 1}, {"reset_boundary_id": "bad reference"},
                       {"profile_id": "lifecycle.progress.foreign"}):
            invalid = copy.deepcopy(state)
            invalid["spell_progress"]["progress.prayer"].update(change)
            self.assert_actor_invalid(invalid)

    def test_nested_details_cannot_smuggle_native_spell_state(self):
        self.assert_actor_invalid({"details": {"notes": [{"form_state": {"profile_id": "lifecycle.form.polymorph"}}]}})

    def test_wish_has_typed_phase_required_evidence_and_no_stochastic_discriminator(self):
        validator = fragment_validator("spell-native-profile-values", "wishReconciliationState")
        execution = {"command_id": "command.wish", "resolution_id": "resolution.wish", "cast_generation": 1}
        roll = {"execution_ref": execution, "request_id": "roll.old", "occurrence_id": "occ.old", "generation": 1}
        owner = {"owner_ref": {"family_key": "world.actor", "identity": ["actor.one"]}, "source_basis": "basis.one", "generation": 1, "fingerprint": "a" * 64}
        base = {"profile_id": "execution.wish_roll_redo", "profile_generation": 1,
                "wish_execution_ref": execution, "target_roll_ref": roll,
                "initiation_frontier": {"procedure_id": "procedure.one", "boundary_occurrence_id": "boundary.one", "chronology_bridge_ref": "bridge.one", "owner_revision_refs": [owner]},
                "recent_basis_ref": {"witness_id": "witness.one", "execution_ref": execution, "catalog_context_fingerprint_generation": 1, "catalog_context_fingerprint": "ctx"},
                "phase": "PREFLIGHT", "reroll_mode": "NORMAL", "reroll_request_refs": [],
                "closure_evidence_refs": [owner], "source_preparation_refs": [], "pending_work_refs": []}
        phases = ("PREFLIGHT", "CAST_ACCEPTED", "REROLL_FIXED", "SELECTION_PENDING", "SOURCES_PREPARED", "RECONCILIATION_STAGED", "ACCEPTED", "PUBLICATION_PENDING", "SETTLED")
        for index, phase in enumerate(phases):
            value = copy.deepcopy(base)
            value["phase"] = phase
            if index >= 2:
                value["reroll_request_refs"] = [dict(roll, request_id="roll.wish")]
            if index >= 4:
                value.update(selected_basis="ORIGINAL", accepted_choice_ref={"offer_id": "offer.one", "continuation_generation": 1, "responder_id": "actor.one", "selected_option_id": "option.original"})
            if index >= 6:
                value.update(replacement_relation_ref="relation.wish", reconciliation_receipt_ref={"execution_ref": execution, "segment_id": "segment.wish", "receipt_id": "receipt.wish"})
            validator.validate(value)
            with self.assertRaises(ValidationError):
                validator.validate(dict(value, target_roll_ref="roll.old"))
            with self.assertRaises(ValidationError):
                fragment_validator("spell-native-profile-values", "stochasticState").validate(value)
            if index >= 4:
                del value["accepted_choice_ref"]
                with self.assertRaises(ValidationError):
                    validator.validate(value)

    def test_geometry_shapes_are_closed_and_source_predicates_do_not_become_global_connectedness(self):
        validator = fragment_validator("spell-native-profile-values", "geometry")
        anchor = {"kind": "location_anchor", "location_id": "location.one", "anchor_basis_ref": "basis.anchor"}
        common = {"profile_id": "lifecycle.spatial.zone", "placement_generation": 1, "placement_fact_ref": "fact.place", "unit_id": "unit.foot"}
        branches = [
            dict(common, kind="radial", shape="sphere", origin_anchor=anchor, radius=10),
            dict(common, kind="radial", shape="cylinder", origin_anchor=anchor, radius=10, height=20),
            dict(common, kind="radial", shape="emanation", origin_anchor={"kind": "moving_anchor", "subject_kind": "actor", "subject_id": "actor.one", "offset_basis_ref": "basis.offset"}, radius=10),
            dict(common, kind="directional", shape="cone", origin_anchor=anchor, orientation_basis_ref="basis.orientation", length=10),
            dict(common, kind="directional", shape="line", origin_anchor=anchor, orientation_basis_ref="basis.orientation", length=10, width=5),
            dict(common, kind="cube_group", cells=[{"cell_key": "cell.one", "anchor": anchor, "edge_length": 10}], adjacent_pairs=[]),
            dict(common, kind="wall_panels", panels=[{"panel_key": "panel.one", "anchor": anchor, "width": 10, "height": 10, "thickness": 1}], adjacent_pairs=[], support_basis_ref="basis.support"),
            dict(common, kind="enclosure", boundary_refs=[{"kind": "zone", "id": "zone.one"}], interior_basis_ref="basis.interior", passage_profile_id="policy.passage"),
        ]
        for branch in branches:
            validator.validate(branch)
            with self.assertRaises(ValidationError):
                validator.validate(dict(branch, x=1))
            with self.assertRaises(ValidationError):
                validator.validate(dict(branch, unit_id="unit.foreign"))
        with self.assertRaises(ValidationError):
            validator.validate(dict(branches[0], height=20))
        invalid = dict(branches[1])
        del invalid["height"]
        with self.assertRaises(ValidationError):
            validator.validate(invalid)

    def test_geometry_member_references_are_finite_and_predicate_specific(self):
        from GAME.TOOLS import activity_contracts as contracts

        self.assertTrue(hasattr(contracts, "validate_geometry_membership"), "finite geometry reference checking is missing")
        value = {"kind": "cube_group", "cells": [{"cell_key": f"cell.{key}"} for key in ("a", "b", "c", "d")],
                 "adjacent_pairs": [{"left_cell_key": "cell.a", "right_cell_key": "cell.b"}, {"left_cell_key": "cell.c", "right_cell_key": "cell.d"}]}
        contracts.validate_geometry_membership(value, neighbor_predicate="EACH_HAS_NEIGHBOR")
        with self.assertRaises(contracts.ActivityContractError):
            contracts.validate_geometry_membership(value, neighbor_predicate="CONNECTED")
        for pairs in ([{"left_cell_key": "cell.a", "right_cell_key": "cell.foreign"}],
                      [{"left_cell_key": "cell.a", "right_cell_key": "cell.a"}]):
            with self.assertRaises(contracts.ActivityContractError):
                contracts.validate_geometry_membership(dict(value, adjacent_pairs=pairs), neighbor_predicate="NONE")


    def test_prismatic_secondary_rays_preserve_duplicates_and_reject_eight(self):
        schema_path = ROOT / "DEV/SCHEMAS/spell-native-profile-values.schema.json"
        self.assertTrue(schema_path.is_file(), "stochastic shape is missing")
        validator = fragment_validator("spell-native-profile-values", "stochasticState")
        value = {"profile_id": "execution.stochastic.prismatic_spray_rays", "profile_generation": 1,
                 "target_ordinal": 0, "secondary_draw_ordinal": 2, "phase": "APPLY_RAYS",
                 "accepted_rays": [1, 1], "fixed_draw_refs": ["roll.initial", "roll.red1", "roll.red2"]}
        validator.validate(value)
        for change in ({"accepted_rays": [1, 8]}, {"accepted_rays": [1, 1, 2]},
                       {"profile_generation": 2}, {"phase": "ARRIVED"},
                       {"profile_id": "execution.wish_roll_redo"}):
            with self.assertRaises(ValidationError):
                validator.validate(dict(value, **change))

    def test_finite_object_return_ruling_has_no_health_or_residual_input(self):
        schema_path = ROOT / "DEV/SCHEMAS/spell-native-profile-values.schema.json"
        self.assertTrue(schema_path.is_file(), "return ruling shape is missing")
        validator = fragment_validator("spell-native-profile-values", "objectReturnAdjudication")
        for result in ("restore_entry_health", "zero_original_policy", "principal_dead"):
            validator.validate({"ordinary_return_health": "entry_current_normalized",
                                "destruction_result": result, "overflow": "none"})
        for result in ("zero_original_policy", "principal_dead"):
            with self.assertRaises(ValidationError):
                validator.validate({"ordinary_return_health": "entry_current_normalized",
                                    "destruction_result": result, "overflow": "terminal_damage_overflow_to_return"})
        valid = {"ordinary_return_health": "entry_current_normalized", "destruction_result": "restore_entry_health",
                 "overflow": "terminal_damage_overflow_to_return"}
        validator.validate(valid)
        for key in ("current", "residual", "resource_amounts", "original_body_actor_id"):
            with self.assertRaises(ValidationError):
                validator.validate(dict(valid, **{key: 10}))

    def assert_actor_valid(self, state):
        validators().validate(state)
        self.assertEqual(validate_actor_source(actor(state))["state"], state)

    def assert_actor_invalid(self, state):
        with self.assertRaises(ValidationError):
            validators().validate(state)
        with self.assertRaises(ActorContinuityError):
            validate_actor_source(actor(state))

    def test_temporary_hp_has_one_amount_and_closed_positive_grant_provenance(self):
        state = {"hp": {"current": 8, "maximum_base": 10, "temporary": 5,
                        "temporary_source": {"grant_occurrence_id": "occurrence.grant",
                                             "source_effect_id": "effect.form"}},
                 "life_state_id": "life.active",
                 "life_state_policy_id": "life_policy.dnd2024.character_like"}
        self.assert_actor_valid(state)
        for change in ({"temporary": 0}, {"temporary": None},
                       {"temporary_source": {"grant_occurrence_id": "occurrence.grant", "amount": 5}},
                       {"temporary_source": {}},
                       {"temporary_source": {"grant_occurrence_id": "bad id"}}):
            with self.subTest(change=change):
                invalid = copy.deepcopy(state)
                invalid["hp"].update(change)
                self.assert_actor_invalid(invalid)
        invalid = copy.deepcopy(state)
        del invalid["hp"]["temporary"]
        self.assert_actor_invalid(invalid)

    def test_neutral_principal_variants_have_no_physical_health_or_location(self):
        for profile, policy in (
            ("actor.embodiment.principal", "life_policy.spell.magic_jar_principal"),
            ("actor.embodiment.principal", "life_policy.spell.astral_principal"),
            ("actor.embodiment.object_suspension", "life_policy.spell.true_polymorph_object_principal"),
        ):
            embodiment = {"profile_id": profile, "relation_effect_id": "effect.relation"}
            if profile.endswith("object_suspension"):
                embodiment.update(object_asset_id="asset.object", restoration_basis_ref="basis.return",
                                  binding_generation=1)
            state = {"embodiment": embodiment, "life_state_policy_id": policy,
                     "life_state_id": "life.active"}
            self.assert_actor_valid(state)
            for change in ({"hp": {"current": 1, "maximum_base": 10}},
                           {"location_id": "location.room"},
                           {"life_state_id": "life.dying", "life_state_progress": {"death_saves": {"successes": 0, "failures": 0}}},
                           {"life_state_policy_id": "life_policy.dnd2024.character_like"}):
                with self.subTest(profile=profile, change=change):
                    self.assert_actor_invalid(dict(state, **change))
            for extra in ("original_body_actor_id", "hp", "unknown"):
                invalid = copy.deepcopy(state)
                invalid["embodiment"][extra] = "actor.phantom"
                self.assert_actor_invalid(invalid)

    def test_body_and_astral_proxy_do_not_copy_build_or_private_continuity(self):
        for profile in ("actor.embodiment.body", "actor.embodiment.astral_proxy"):
            embodiment = {"profile_id": profile, "principal_subject_id": "actor.principal",
                          "relation_effect_id": "effect.relation", "construction_basis_ref": "basis.construction"}
            if profile.endswith("astral_proxy"):
                embodiment["replica_group_ref"] = "replica.group"
            state = {"embodiment": embodiment, "hp": {"current": 10, "maximum_base": 10},
                     "location_id": "location.room", "life_state_id": "life.active",
                     "life_state_policy_id": "life_policy.dnd2024.character_like"}
            self.assert_actor_valid(state)
            for extra in ("build", "continuity"):
                self.assert_actor_invalid(dict(state, **{extra: {}}))
            invalid = copy.deepcopy(state)
            invalid["embodiment"]["relation_effect_id"] = "not a native id"
            self.assert_actor_invalid(invalid)

    def test_principal_policies_cannot_be_used_by_an_ordinary_physical_actor(self):
        for policy in ("life_policy.spell.magic_jar_principal", "life_policy.spell.astral_principal",
                       "life_policy.spell.true_polymorph_object_principal"):
            self.assert_actor_invalid({"life_state_id": "life.active", "life_state_policy_id": policy})

    def test_malformed_policy_and_survival_values_raise_typed_errors(self):
        for bad in ([], {}, True):
            with self.subTest(value=bad):
                self.assert_actor_invalid({"life_state_policy_id": bad})
                self.assert_actor_invalid({"embodiment": {"profile_id": "actor.embodiment.principal",
                                                         "relation_effect_id": "effect.relation"},
                                           "life_state_policy_id": "life_policy.spell.magic_jar_principal",
                                           "life_state_id": bad})

    def test_continuity_delta_cannot_author_an_embodiment_transition(self):
        source = actor({"roles": ["actor.nonplayer_character"]})
        evidence = [{"ref": "evidence.phase", "accepted": True, "current": True,
                     "authorized_actor_ids": [source["id"]]}]
        delta = {"actor_id": source["id"], "expected_state_revision": 1,
                 "purpose": "assessment.react", "source_refs": ["evidence.phase"],
                 "changes": {"embodiment": {"profile_id": "actor.embodiment.principal",
                                            "relation_effect_id": "effect.relation"}}}
        with self.assertRaisesRegex(ActorContinuityError, "continuity"):
            validate_actor_delta(delta, source, evidence)

    def test_every_embodiment_required_member_and_generation_is_closed(self):
        branches = [
            {"profile_id": "actor.embodiment.principal", "relation_effect_id": "effect.relation"},
            {"profile_id": "actor.embodiment.body", "principal_subject_id": "actor.principal",
             "relation_effect_id": "effect.relation", "construction_basis_ref": "basis.body"},
            {"profile_id": "actor.embodiment.astral_proxy", "principal_subject_id": "actor.principal",
             "relation_effect_id": "effect.relation", "construction_basis_ref": "basis.body",
             "replica_group_ref": "replica.group"},
            {"profile_id": "actor.embodiment.object_suspension", "relation_effect_id": "effect.relation",
             "object_asset_id": "asset.object", "restoration_basis_ref": "basis.return",
             "binding_generation": 1},
        ]
        for branch in branches:
            profile = branch["profile_id"]
            policy = ("life_policy.spell.magic_jar_principal" if profile.endswith("principal")
                      else "life_policy.spell.true_polymorph_object_principal" if profile.endswith("object_suspension")
                      else "life_policy.dnd2024.character_like")
            state = {"embodiment": branch, "life_state_id": "life.active", "life_state_policy_id": policy}
            self.assert_actor_valid(state)
            for key in branch:
                invalid = copy.deepcopy(state)
                del invalid["embodiment"][key]
                self.assert_actor_invalid(invalid)
            invalid = copy.deepcopy(state)
            invalid["embodiment"]["profile_id"] = "actor.embodiment.foreign"
            self.assert_actor_invalid(invalid)
            if "binding_generation" in branch:
                for bad in (0, -1, True, "1"):
                    invalid = copy.deepcopy(state)
                    invalid["embodiment"]["binding_generation"] = bad
                    self.assert_actor_invalid(invalid)


if __name__ == "__main__":
    unittest.main()
