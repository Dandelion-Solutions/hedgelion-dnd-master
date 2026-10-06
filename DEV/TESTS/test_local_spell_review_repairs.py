"""Regression witnesses for independent frozen SP01 review findings."""

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from GAME.TOOLS import activity_contracts as c

ROOT = Path(__file__).resolve().parents[2]


class FrozenReviewRepairTests(unittest.TestCase):
    def test_runtime_checker_operates_without_a_dev_tree(self):
        with tempfile.TemporaryDirectory(prefix="sp01-runtime-contract-") as directory:
            target = Path(directory)
            for name in ("structural_contracts.py", "activity_contract_shapes.json"):
                shutil.copy2(ROOT / "GAME/TOOLS" / name, target / name)
            spec = importlib.util.spec_from_file_location("isolated_sp01_structural", target / "structural_contracts.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.validate_contract("exports", {"hit": True})
            with self.assertRaises(ValueError):
                module.validate_contract("exports", {"hit": {"patch": {"hp": 10}}})
    def test_runtime_projection_reproduces_sources_and_preserves_assertion_field_names(self):
        from DEV.TOOLS.build_activity_contract_shapes import build_projection

        projected = json.loads((ROOT / "GAME/TOOLS/activity_contract_shapes.json").read_text())
        self.assertEqual(projected, build_projection(ROOT))
        schema = projected["schemas"]["https://hedgelion.invalid/schemas/activity-parameter-spec.schema.json"]
        self.assertIn("default", schema["properties"])

    def test_wish_reference_validator_checks_all_supplied_domains_without_issuing_truth(self):
        from dataclasses import replace

        from GAME.TOOLS.current_owner import NativeOwnerRef

        original = c.ExecutionRef("command.old", "resolution.old")
        wish = c.CastExecutionRef("command.wish", "resolution.wish", 1)
        owner = c.OwnerRevisionRef(NativeOwnerRef("world.actor", ("actor.one",)), "source", 1, "a" * 64)
        state = c.WishReconciliationState(wish, c.RollRef(original, "roll.old", "occ.old", 1),
            c.WishInitiationFrontier("procedure.one", "boundary.one", "bridge.one", (owner,)),
            c.RecentBasisRef("witness.one", original, "context"), "REROLL_FIXED", "NORMAL",
            (c.RollRef(wish, "roll.new", "occ.new", 1),), (owner,), (), ())
        references = c.AcceptedCompiledReferences(roll_request_ids=("roll.old", "roll.new"), roll_refs=(state.target_roll_ref, *state.reroll_request_refs),
            execution_refs=(original, wish), owner_revision_refs=(owner,), procedure_ids=("procedure.one",),
            boundary_occurrence_ids=("boundary.one",), chronology_bridge_refs=("bridge.one",), witness_ids=("witness.one",), context_fingerprints=("context",))
        c.validate_wish_references(state, references)
        for field in ("roll_request_ids", "roll_refs", "execution_refs", "owner_revision_refs", "procedure_ids", "boundary_occurrence_ids", "chronology_bridge_refs", "witness_ids", "context_fingerprints"):
            with self.assertRaises(c.ActivityContractError):
                c.validate_wish_references(state, replace(references, **{field: ()}))

    def test_native_geometry_union_and_current_effect_consumer_have_full_branch_closure(self):
        from DEV.TOOLS.validate_character_mvp_seed import (
            CanonicalSchemaValidator,
            SchemaViolation,
        )
        from GAME.TOOLS.structural_contracts import validate_contract

        schema = CanonicalSchemaValidator(ROOT / "DEV/SCHEMAS")
        owner = schema.schemas["https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json"]
        anchor = {"kind": "location_anchor", "location_id": "location.one", "anchor_basis_ref": "basis.anchor"}
        common = {"profile_id": "lifecycle.spatial.zone", "placement_generation": 1, "placement_fact_ref": "fact.place", "unit_id": "unit.foot"}
        values = [dict(common, kind="radial", shape="sphere", origin_anchor=anchor, radius=10),
            dict(common, kind="radial", shape="cylinder", origin_anchor=anchor, radius=10, height=10),
            dict(common, kind="radial", shape="emanation", origin_anchor=anchor, radius=10),
            dict(common, kind="directional", shape="cone", origin_anchor=anchor, orientation_basis_ref="basis.face", length=10),
            dict(common, kind="directional", shape="line", origin_anchor=anchor, orientation_basis_ref="basis.face", length=10, width=5),
            dict(common, kind="cube_group", cells=[{"cell_key": "cell.one", "anchor": anchor, "edge_length": 10}], adjacent_pairs=[]),
            dict(common, kind="wall_panels", panels=[{"panel_key": "panel.one", "anchor": anchor, "width": 10, "height": 10, "thickness": 1}], adjacent_pairs=[], support_basis_ref="basis.support"),
            dict(common, kind="enclosure", boundary_refs=[{"kind": "zone", "id": "zone.one"}], interior_basis_ref="basis.interior", passage_profile_id="policy.passage")]
        for value in values:
            c.NativeGeometry(value)
            schema.validate(value, owner["$defs"]["geometry"], root=owner)
            with self.assertRaises(c.ActivityContractError):
                c.NativeGeometry(dict(value, x=1))
            with self.assertRaises(SchemaViolation):
                schema.validate(dict(value, x=1), owner["$defs"]["geometry"], root=owner)
        validate_contract("parameters", {"amount": {"source_class": "ENGINE_BOUND", "value_type": "integer", "cardinality": "single", "required": True, "default": 1}})
        for name, invalid in (("parameters", {"amount": {"hp": 10}}), ("roles", {"actor": "world.actor"}),
                              ("export_contracts", {"result": {"hp": {"value_kind": "foreign", "cardinality": "single", "required": True, "source": "PRIMITIVE_RESULT"}}})):
            with self.assertRaises(ValueError):
                validate_contract(name, invalid)
    def test_runtime_native_unions_are_closed_for_every_branch(self):
        self.assertTrue(hasattr(c, "NativeFormState"), "runtime-native closed unions are absent")
        classes = {"formState": c.NativeFormState, "identityState": c.NativeIdentityState,
                   "conversionState": c.NativeConversionState, "controlState": c.NativeControlState,
                   "temporalOccurrence": c.NativeTemporalOccurrence, "portalState": c.NativePortalState,
                   "spellPlace": c.NativeSpellPlace}
        cases = json.loads((ROOT / "DEV/TESTS/fixtures/local-spells/SP01/branches.json").read_text())
        for case in cases:
            if case["fragment"] not in classes:
                continue
            cls = classes[case["fragment"]]
            cls(case["value"])
            with self.assertRaises(c.ActivityContractError):
                cls(dict(case["value"], hp=10))

    def test_instruction_arguments_use_registered_runtime_shapes(self):
        with self.assertRaises(c.ActivityContractError):
            c.CompiledInstruction("activity.one.step.0", "op.resolve_check", {"hp": 10}, (), ())
        valid = {"roll": {"roll_id": "roll.one", "request_id": "roll.one", "expression": "1d20",
                           "raw_values": [10], "source_kind": "rng.system", "provenance_ref": "rng.one"}, "threshold": 10}
        c.CompiledInstruction("activity.one.step.0", "op.resolve_check", valid, (), ())

    def test_fragment_exports_cannot_be_an_opaque_mutation_bag(self):
        with self.assertRaises(c.ActivityContractError):
            c.PreparedNativeFragment("activity.one", "occ.one", "a" * 64, (), (),
                {"result": {"patch": {"hp": 10}}}, (), (), object(), _issue_seal=c._CONTRACT_SEAL)
    def test_stochastic_phase_consistency_and_supplied_reference_sets(self):
        with self.assertRaises(c.ActivityContractError):
            c.PrismaticSprayRaysState(0, 0, "APPLY_RAYS", (), ())
        self.assertTrue(hasattr(c, "AcceptedCompiledReferences"))
        references = c.AcceptedCompiledReferences(
            roll_request_ids=("roll.red",), target_ids=("actor.one",),
            parameter_keys=("destination",), table_rows={"table.teleport": ("row.mishap",)},
            ancestry_definition_ids=("species.human",),
        )
        valid = c.PrismaticSprayRaysState(0, 1, "APPLY_RAYS", (1, 1), ("roll.red",))
        c.validate_stochastic_references(valid, references)
        for bad in (c.PrismaticSprayRaysState(1, 1, "APPLY_RAYS", (1,), ("roll.red",)),
                    c.PrismaticSprayRaysState(0, 1, "APPLY_RAYS", (1,), ("roll.foreign",))):
            with self.assertRaises(c.ActivityContractError):
                c.validate_stochastic_references(bad, references)
        teleport = c.TeleportMishapState(0, "TABLE_DRAW", "destination", "table.teleport", "row.foreign", (), ("actor.one",), ())
        with self.assertRaises(c.ActivityContractError):
            c.validate_stochastic_references(teleport, references)

    def test_owner_reference_arity_is_family_specific(self):
        from GAME.TOOLS.current_owner import NativeOwnerRef

        with self.assertRaises(c.ActivityContractError):
            c.OwnerRevisionRef(NativeOwnerRef("world.actor", ("actor.one", "actor.two")), "source", 1, "a" * 64)
        with self.assertRaises(c.ActivityContractError):
            c.OwnerRevisionRef(NativeOwnerRef("world.knowledge", ("actor.one",)), "source", None, "a" * 64)

    def test_wish_reroll_is_owned_by_wish_execution(self):
        from GAME.TOOLS.current_owner import NativeOwnerRef

        original = c.ExecutionRef("command.old", "resolution.old")
        wish = c.CastExecutionRef("command.wish", "resolution.wish", 1)
        owner = c.OwnerRevisionRef(NativeOwnerRef("world.actor", ("actor.one",)), "source", 1, "a" * 64)
        with self.assertRaises(c.ActivityContractError):
            c.WishReconciliationState(wish, c.RollRef(original, "roll.old", "occ.old", 1),
                c.WishInitiationFrontier("procedure.one", "boundary.one", "bridge.one", (owner,)),
                c.RecentBasisRef("witness.one", original, "context"), "REROLL_FIXED", "NORMAL",
                (c.RollRef(original, "roll.new", "occ.new", 1),), (owner,), (), ())
    def test_native_preparation_hold_is_a_typed_raise_catch_exception(self):
        hold = c.NativePreparationHold("CAPACITY_REQUIRED", c.ExecutionRef("command.one", "resolution.one"), ("continuation.one",))
        self.assertIsInstance(hold, Exception)
        try:
            raise hold
        except c.NativePreparationHold as caught:
            self.assertIs(caught, hold)
            self.assertEqual(caught.operation_status, "CAPACITY_REQUIRED")
        for status in ("FAILED", "COMPLETED", True):
            with self.assertRaises(c.ActivityContractError):
                c.NativePreparationHold(status, hold.execution_ref, ())

    def test_actual_effect_consumer_rejects_identity_extra_health(self):
        from DEV.TOOLS.validate_health_effects_recovery_seed import (
            validate_world_effect_records,
        )

        cases = json.loads((ROOT / "DEV/TESTS/fixtures/local-spells/SP01/branches.json").read_text())
        for case in cases:
            if case["fragment"] != "identityState":
                continue
            value = {"schema_version": 2, "id": "effect.one", "kind": "world.effect", "definition_id": "effect.one",
                     "state": {"target_id": "actor.one", "lifecycle": {"state_id": "effect_lifecycle.active"}, "identity_state": case["value"]}}
            validate_world_effect_records({"effect.one": value})
            bad = copy.deepcopy(value)
            bad["state"]["identity_state"]["hp"] = {"current": 10}
            with self.assertRaises(ValueError):
                validate_world_effect_records({"effect.one": bad})

    def test_native_establishment_uses_actual_execution_envelope_for_established_and_replay(self):
        from DEV.TESTS.test_rd05_runtime_execution import (
            _candidate,
            _interpreter_result,
            _proposal,
        )
        from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
        from GAME.TOOLS.mechanics import (
            ExecutionStore,
            FixedRng,
            close_resolution,
            execute_segment,
        )
        from GAME.TOOLS.runtime_execution import accept_command

        accepted = accept_command(
            _interpreter_result(), _bind_context(), _candidate(), _proposal()
        )
        resolution = {
            "root_command_id": accepted["command_id"],
            "initiating_command_id": accepted["command_id"],
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "context.one",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": "a" * 64,
            "procedure_id": "procedure.one",
            "safe_recompute_phase": "determine",
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        continuation = {
            "generation": 1,
            "root_command_id": accepted["command_id"],
            "resolution_id": accepted["root_resolution_id"],
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": "a" * 64,
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "context.one",
            "procedure_id": "procedure.one",
            "execution_cursor": "step.check.resolve",
            "safe_recompute_phase": "determine",
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "committed_segment_refs": [],
            "dependency_frontier_refs": [],
            "expected_child_resolution_ids": [],
            "future_rng_frontier": "rng:one",
        }
        procedure_state = {
            "schema_version": 2,
            "lifecycle": "ACTIVE",
            "participant_resources": {},
        }
        store = ExecutionStore()
        execution = execute_segment(
            accepted,
            resolution,
            rng=FixedRng([17]),
            event_payload={"result": 17},
            procedure_state=procedure_state,
            continuation_state=continuation,
            store=store,
        )
        replay = execute_segment(
            accepted,
            resolution,
            rng=FixedRng([3]),
            target_segment_id=execution["segment"]["segment_id"],
            event_payload={"result": 17},
            procedure_state=procedure_state,
            continuation_state=continuation,
            store=store,
        )
        child_resolution = dict(
            resolution,
            resolution_id="resolution.child",
            activity_id="activity.followup",
            actor_id="actor-2",
            causal_invocation_key="resolution-1:segment:1:event:1",
        )
        child_execution = execute_segment(
            accepted,
            child_resolution,
            event_payload={"followup": True},
            store=ExecutionStore(),
        )

        def establish(status, result, receipt=None, *, resolution_id=None):
            return c.NativeSegmentEstablishment(
                status,
                "campaign.one",
                c.ExecutionRef(
                    accepted["command_id"],
                    accepted["root_resolution_id"] if resolution_id is None else resolution_id,
                ),
                accepted["input_fingerprint"],
                result.get("segment", {}).get(
                    "segment_id", execution["segment"]["segment_id"]
                ),
                (),
                (),
                (),
                accepted_execution=result,
                receipt=(
                    receipt
                    if receipt is not None
                    else result.get("receipt", execution["receipt"])
                ),
                _issue_seal=c._CONTRACT_SEAL,
            )

        established = establish("ESTABLISHED", execution)
        replayed = establish("REPLAY", replay)
        closed_execution = close_resolution(execution, store=store)
        closed_establishment = establish("ESTABLISHED", closed_execution)
        child_established = establish(
            "ESTABLISHED", child_execution, resolution_id="resolution.child"
        )
        self.assertEqual(established.status, "ESTABLISHED")
        self.assertEqual(replayed.status, "REPLAY")
        self.assertEqual(closed_execution["status"], "COMPLETED")
        self.assertEqual(closed_execution["resolution"]["status"], "COMPLETED")
        self.assertEqual(
            closed_execution["segment"]["resulting_execution_state"], "RUNNING"
        )
        self.assertEqual(closed_execution["receipt"]["status"], "RUNNING")
        self.assertEqual(closed_establishment.status, "ESTABLISHED")
        self.assertEqual(
            child_established.execution_ref.resolution_id, "resolution.child"
        )
        for field in ("roll_result", "procedure_state", "continuation_state"):
            self.assertIn(field, established.accepted_execution)
        for establishment, result in (
            (established, execution),
            (replayed, replay),
            (closed_establishment, closed_execution),
            (child_established, child_execution),
        ):
            self.assertEqual(
                establishment.accepted_execution["accepted_command_id"],
                result["accepted_command_id"],
            )
            self.assertEqual(
                establishment.accepted_execution["segment"]["segment_id"],
                result["segment"]["segment_id"],
            )
            self.assertEqual(
                establishment.accepted_execution["event_id"], result["event_id"]
            )
            self.assertEqual(
                establishment.receipt["execution_owner_id"], result["receipt"]["execution_owner_id"]
            )

        # Structural witness only: mechanics currently emits one event, while
        # the accepted segment/receipt owners permit a complete stable-ID batch.
        multi_event = copy.deepcopy(execution)
        second_event_id = f"{execution['segment']['segment_id']}:event:2"
        multi_event["segment"]["event_ids"].append(second_event_id)
        multi_event["receipt"]["event_ids"].append(second_event_id)
        multi_event["resolution"]["segments"][-1]["event_ids"].append(second_event_id)
        multi_established = establish("ESTABLISHED", multi_event)
        self.assertEqual(
            tuple(multi_established.accepted_execution["segment"]["event_ids"]),
            (execution["event_id"], second_event_id),
        )
        with self.assertRaises(c.ActivityContractError):
            establish(
                "ESTABLISHED",
                dict(
                    multi_event,
                    receipt=dict(
                        multi_event["receipt"], event_ids=[execution["event_id"]]
                    ),
                ),
            )
        with self.assertRaises(c.ActivityContractError):
            establish(
                "ESTABLISHED",
                dict(multi_event, event_id=second_event_id),
            )

        for invalid in (
            accepted,
            dict(execution, unauthorized_extra=True),
            dict(execution, accepted_command_id="command.foreign"),
            dict(execution, receipt=dict(execution["receipt"], event_ids=[])),
            dict(execution, receipt=dict(execution["receipt"], status="COMPLETED")),
        ):
            with self.subTest(
                invalid_keys=set(invalid) - set(execution)
            ), self.assertRaises(c.ActivityContractError):
                establish("ESTABLISHED", invalid)
        with self.assertRaises(c.ActivityContractError):
            establish(
                "ESTABLISHED",
                dict(
                    closed_execution,
                    resolution=dict(closed_execution["resolution"], status="RUNNING"),
                ),
            )
        with self.assertRaises(c.ActivityContractError):
            establish(
                "ESTABLISHED",
                dict(
                    child_execution,
                    resolution=dict(
                        child_execution["resolution"],
                        resolution_id="resolution.foreign",
                    ),
                ),
                resolution_id="resolution.child",
            )
        with self.assertRaises(c.ActivityContractError):
            establish(
                "ESTABLISHED",
                execution,
                dict(execution["receipt"], exports={"foreign": True}),
            )
        for field in ("procedure_state", "continuation_state", "resolution"):
            with self.subTest(nested_field=field), self.assertRaises(
                c.ActivityContractError
            ):
                establish(
                    "ESTABLISHED",
                    dict(execution, **{field: dict(execution[field], extra=True)}),
                )


if __name__ == "__main__":
    unittest.main()
