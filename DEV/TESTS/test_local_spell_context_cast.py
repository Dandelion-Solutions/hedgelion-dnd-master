"""SP03 exact compiled-read slice, using actual installed SP02 and P0 owners.

This slice establishes no selector result, cast, RNG or native consequence.
"""

from __future__ import annotations

import copy
import importlib.util
import os
import unittest
from dataclasses import fields, replace


class InstalledMechanicalReadTests(unittest.TestCase):
    def test_real_installed_compiler_and_p0_read_consumers(self):
        if "HDM_INSTALLED_STRUCTURAL_TEST" in os.environ:
            self.skipTest("outer installation driver")
        from DEV.TESTS.sp02_installed_test_support import run_installed_structural_test

        result = run_installed_structural_test(
            "DEV.TESTS.test_local_spell_context_cast.PinnedMechanicalReadTests"
        )
        print(result.stdout + result.stderr)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless("HDM_INSTALLED_STRUCTURAL_TEST" in os.environ, "installed driver")
class PinnedMechanicalReadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from DEV.TESTS.sp02_installed_test_support import authentic_generic_catalog
        from GAME.TOOLS.activity_runtime import compile_activity

        cls.catalog = authentic_generic_catalog()
        cls.compiled = compile_activity(cls.catalog, "activity.check.generic")

    def setUp(self):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            ACTOR_ID,
            CAMPAIGN_ID,
            ActorRepository,
            _actor,
            _selected_host,
        )
        self.assertIsNotNone(importlib.util.find_spec("GAME.TOOLS.mechanical_context"),
                             "SP03 compiled-read consumer module is missing")
        from GAME.TOOLS import mechanical_context
        from GAME.TOOLS.current_owner import NativeOwnerRef
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record

        self.mechanical = mechanical_context
        self.owner = NativeOwnerRef("world.actor", (ACTOR_ID,))
        self.other = NativeOwnerRef("world.actor", ("actor.other",))

        class Repository(ActorRepository):
            def __init__(inner):
                super().__init__()
                inner.other = copy.deepcopy(_actor())
                inner.other["id"] = "actor.other"
                inner.actor_missing = False
                inner.native_records = {}

            def read_exact_path(inner, pinned, path):
                if path in inner.native_records:
                    inner.path_reads.append((pinned.revision, path))
                    return copy.deepcopy(inner.native_records[path])
                if inner.actor_missing and path == route_native_record("world.actor", (ACTOR_ID,)).relative_path:
                    raise KeyError(path)
                if path == route_native_record("world.actor", ("actor.other",)).relative_path:
                    inner.path_reads.append((pinned.revision, path))
                    return copy.deepcopy(inner.other)
                return super().read_exact_path(pinned, path)

        self.consumer = "activity.check.generic.step.0"
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
        from GAME.TOOLS.runtime_execution import accept_command

        proposal = _proposal()
        proposal["action_request"]["actor_id"] = self.owner.identity[0]
        proposal["action_request"]["target_ids"] = []
        self.accepted = accept_command(
            _interpreter_result(),
            self.catalog.catalog_context,
            {"definition_id": self.compiled.activity_id, "kind": "definition.activity"},
            proposal,
        )
        self.repository = Repository()
        command_record = {
            "kind": "runtime.command",
            "id": self.accepted["command_id"],
            **self.accepted,
        }
        resolution = {
            "root_command_id": self.accepted["command_id"],
            "initiating_command_id": self.accepted["command_id"],
            "activity_id": self.compiled.activity_id,
            "actor_id": self.owner.identity[0],
            "target_ids": self.accepted["action_request"]["target_ids"],
            "parameter_bindings": self.accepted["action_request"].get(
                "parameter_bindings", {}
            ),
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": self.compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": self.catalog.catalog_context.fingerprint,
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": self.accepted["invocation_facts"],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        resolution_record = {
            "kind": "runtime.resolution",
            "id": self.accepted["root_resolution_id"],
            "campaign_id": CAMPAIGN_ID,
            **resolution,
        }
        self.repository.native_records.update(
            {
                route_native_record(
                    "runtime.command", (self.accepted["command_id"],)
                ).relative_path: command_record,
                route_native_record(
                    "runtime.resolution", (self.accepted["root_resolution_id"],)
                ).relative_path: resolution_record,
            }
        )
        self.store = NativeHotStore(":memory:")
        self.addCleanup(self.store.close)
        self.host, _source = _selected_host(
            self.store, repository=self.repository
        )
        self.session = self.host._current_owner.begin(self.host._begin_operation())
        self.roles = {"actor": self.owner}

    def acquire(self, **changes):
        arguments = {"consumer_id": self.consumer, "owner_session": self.session,
                     "role_bindings": self.roles, "accepted_command": self.accepted}
        arguments.update(changes)
        return self.mechanical.acquire_observation(self.compiled, **arguments)

    def preparation(self, *, adjudication_basis=None):
        """Use the runtime-host source-bound root read/preparation issuer."""
        return self.host._current_owner._prepare_root_context(
            self.catalog,
            self.compiled,
            command_id=self.accepted["command_id"],
            consumer_id=self.consumer,
            adjudication_basis=adjudication_basis,
        )

    def _store_root_source(self, accepted):
        from DEV.TESTS.test_w05_t06_p0_actor_producer import CAMPAIGN_ID
        from GAME.TOOLS.native_storage import route_native_record

        request = accepted["action_request"]
        resolution = {
            "root_command_id": accepted["command_id"],
            "initiating_command_id": accepted["command_id"],
            "activity_id": self.compiled.activity_id,
            "actor_id": request["actor_id"],
            "target_ids": request["target_ids"],
            "parameter_bindings": request.get("parameter_bindings", {}),
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": self.compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": self.catalog.catalog_context.fingerprint,
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": accepted["invocation_facts"],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        self.repository.native_records.update(
            {
                route_native_record(
                    "runtime.command", (accepted["command_id"],)
                ).relative_path: {
                    "kind": "runtime.command",
                    "id": accepted["command_id"],
                    **accepted,
                },
                route_native_record(
                    "runtime.resolution", (accepted["root_resolution_id"],)
                ).relative_path: {
                    "kind": "runtime.resolution",
                    "id": accepted["root_resolution_id"],
                    "campaign_id": CAMPAIGN_ID,
                    **resolution,
                },
            }
        )

    def _accepted_with_basis(self, basis):
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
        from GAME.TOOLS.runtime_execution import accept_command

        proposal = _proposal()
        proposal["action_request"]["actor_id"] = self.owner.identity[0]
        proposal["action_request"]["target_ids"] = []
        proposal["action_request"]["parameter_bindings"] = (
            basis.runtime_parameter_bindings()
        )
        self.accepted = accept_command(
            _interpreter_result(),
            self.catalog.catalog_context,
            {"definition_id": self.compiled.activity_id, "kind": "definition.activity"},
            proposal,
            adjudication_basis=basis,
        )
        self._store_root_source(self.accepted)
        return self.preparation(adjudication_basis=basis)

    def test_exact_read_plan_is_retained_from_real_compiler(self):
        self.assertEqual(self.mechanical.compiled_read_plan(self.compiled, self.consumer),
                         ("selector:check.roll",))

    def test_forged_or_copied_compiled_handle_rejects(self):
        for forged in (copy.copy(self.compiled), replace(self.compiled)):
            with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "compiler-issued"):
                self.mechanical.compiled_read_plan(forged, self.consumer)

    def test_foreign_occurrence_rejects(self):
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "consumer"):
            self.acquire(consumer_id="activity.foreign.step.0")

    def test_native_role_family_and_unknown_role_reject_before_read(self):
        from GAME.TOOLS.current_owner import NativeOwnerRef

        for roles in ({"actor": NativeOwnerRef("world.asset", ("asset.one",))},
                      {"actor": self.owner, "extra": self.other}, {}):
            with self.assertRaises(self.mechanical.MechanicalContextError):
                self.acquire(role_bindings=roles)
        self.assertEqual(self.repository.path_reads, [])

    def test_complete_accumulated_union_is_reacquired_on_expansion(self):
        first = self.acquire()
        self.repository.actor["state_revision"] += 1
        expanded = self.session.require((self.other,))
        self.assertEqual(set(expanded.key_union), {self.owner, self.other})
        self.assertEqual(expanded.require(self.owner).generation, 5)
        self.assertFalse(self.session.revalidate(first))
        self.assertTrue(self.session.revalidate(expanded))

    def test_missing_actor_is_typed_hold_never_index_absence_or_empty_set(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold
        self.repository.actor_missing = True
        with self.assertRaises(NativePreparationHold) as raised:
            self.acquire()
        self.assertEqual(raised.exception.operation_status, "AUTHORITY_UNAVAILABLE")

    def test_currentness_relevant_owner_change_rejects_cache_use(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        context = self.preparation()
        self.mechanical.context_cache_identity(context)
        self.repository.actor["state_revision"] += 1
        with self.assertRaises(NativePreparationHold) as raised:
            self.mechanical.context_cache_identity(context)
        self.assertEqual(raised.exception.operation_status, "REVALIDATION_REQUIRED")

    def test_unrelated_owner_change_does_not_invalidate_read_identity(self):
        context = self.preparation()
        before = self.mechanical.context_cache_identity(context)
        self.repository.other["state_revision"] += 1
        self.assertEqual(self.mechanical.context_cache_identity(context), before)

    def test_repin_recomputes_relevant_identity(self):
        before = self.mechanical.context_cache_identity(self.preparation())
        self.repository.actor["state_revision"] += 1
        after = self.mechanical.context_cache_identity(self.preparation())
        self.assertNotEqual(before, after)

    def test_resolver_issued_policy_changes_cache_identity(self):
        unadjudicated_context = self.preparation()
        unadjudicated_identity = self.mechanical.context_cache_identity(
            unadjudicated_context
        )
        basis = self.policy_basis()
        context = self._accepted_with_basis(basis)
        before = self.mechanical.context_cache_identity(context)
        self.assertNotEqual(unadjudicated_identity, before)
        self.assertEqual(
            context.policy_refs,
            tuple(sorted(policy.policy_id for policy in basis.verified_policies)),
        )
        self.assertEqual(self.mechanical.context_cache_identity(context), before)
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(
                replace(context, policy_refs=("policy.one", "policy.two"))
            )

    def test_post_issuance_command_mutation_and_state_substitution_reject(self):
        from GAME.TOOLS.activity_contracts import ActivityContractError

        context = self.preparation()
        with self.assertRaises(ActivityContractError):
            replace(context, accepted_command=dict(context.accepted_command, hp=100))
        forged = dict(context.accepted_command)
        forged["input_fingerprint"] = "0" * 64
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(replace(context, accepted_command=forged))

    def test_prospective_documents_require_future_same_builder_issuance(self):
        from GAME.TOOLS.hot_store import OwnerDocument

        context = self.preparation()
        read = context.observation.require(self.owner)
        document = OwnerDocument(self.session._campaign_id, self.owner.family_key,
            self.owner.identity, read.payload, read.source_basis, read.generation)
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(replace(context, prospective_owner_documents=(document,)))

    def test_fake_context_and_stale_observation_are_not_cache_authority(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        with self.assertRaises(self.mechanical.MechanicalContextError):
            self.mechanical.context_cache_identity({"hp": 8})
        context = self.preparation()
        context.owner_session.require((self.other,))
        with self.assertRaises(NativePreparationHold):
            self.mechanical.context_cache_identity(context)

    def test_source_bound_issuer_binds_exact_native_root_and_consumer(self):
        from GAME.TOOLS import activity_contracts as contracts

        context = self.preparation()

        self.assertTrue(contracts._preparation_context_is_issued(context))
        from GAME.TOOLS.catalog_runtime import _thaw

        self.assertEqual(_thaw(context.accepted_command), self.accepted)
        self.assertEqual(context.execution_ref.command_id, self.accepted["command_id"])
        self.assertEqual(
            context.execution_ref.resolution_id,
            self.accepted["root_resolution_id"],
        )
        self.assertEqual(
            context.occurrence_id,
            f"{self.accepted['root_resolution_id']}:{self.consumer}",
        )
        self.assertEqual(dict(context.role_bindings), self.roles)
        self.assertEqual(context.resolution["root_command_id"], self.accepted["command_id"])
        self.assertEqual(context.resolution["segments"], ())
        self.assertIs(context._builder_token, context.owner_session.operation_token)

    def test_constructor_copy_replace_mutation_and_forged_child_do_not_issue(self):
        from GAME.TOOLS import activity_contracts as contracts

        context = self.preparation()
        registry_count = sum(
            record.reference() is not None
            for records in contracts._PREPARATION_CONTEXTS.values()
            for record in records
        )
        self.mechanical.context_cache_identity(context)
        self.assertEqual(
            sum(
                record.reference() is not None
                for records in contracts._PREPARATION_CONTEXTS.values()
                for record in records
            ),
            registry_count,
        )
        direct_fields = {
            member.name: getattr(context, member.name)
            for member in fields(context)
            if member.init and member.name != "_issue_seal"
        }
        directly_constructed = contracts.NativePreparationContext(
            **direct_fields, _issue_seal=context._issue_seal
        )
        forged_child_resolution = dict(context.resolution)
        forged_child_resolution["causal_invocation_key"] = "invented:segment:event"
        forged_child = replace(
            context,
            occurrence_id="occ.invented.child",
            execution_ref=contracts.ExecutionRef(
                context.execution_ref.command_id, "resolution.invented.child"
            ),
            resolution=forged_child_resolution,
        )

        for unissued in (
            copy.copy(context),
            replace(context),
            replace(context, occurrence_id="occ.invented"),
            directly_constructed,
            forged_child,
        ):
            self.assertFalse(contracts._preparation_context_is_issued(unissued))
            with self.assertRaisesRegex(
                self.mechanical.MechanicalContextError, "authentic source-bound"
            ):
                self.mechanical.context_cache_identity(unissued)

        other_session = self.host._current_owner.begin(self.host._begin_operation())
        other_observation = other_session.require((self.owner,))
        rebound = replace(
            context,
            owner_session=other_session,
            observation=other_observation,
        )
        self.assertFalse(contracts._preparation_context_is_issued(rebound))
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(rebound)

        with self.assertRaises(contracts.ActivityContractError):
            replace(context, consumer_id="activity.foreign.step.0")
        with self.assertRaises(contracts.ActivityContractError):
            replace(context, catalog=copy.copy(context.catalog))

        original_occurrence = context.occurrence_id
        object.__setattr__(context, "occurrence_id", "occ.mutated.after.issue")
        self.assertFalse(contracts._preparation_context_is_issued(context))
        object.__setattr__(context, "occurrence_id", original_occurrence)
        self.assertTrue(contracts._preparation_context_is_issued(context))

    def test_unrelated_compiled_cache_rebuild_preserves_root_issuance(self):
        from types import MappingProxyType

        from GAME.TOOLS import activity_contracts as contracts
        from GAME.TOOLS.activity_runtime import compile_activity

        context = self.preparation()
        before = self.mechanical.context_cache_identity(context)
        self.assertTrue(contracts._preparation_context_is_issued(context))
        selected_compiled = self.compiled

        unrelated_before = compile_activity(self.catalog, "activity.save.generic")
        cache_without_unrelated = dict(self.catalog.compiled_activities)
        cache_without_unrelated.pop("activity.save.generic")
        object.__setattr__(
            self.catalog,
            "compiled_activities",
            MappingProxyType(cache_without_unrelated),
        )
        unrelated_after = compile_activity(self.catalog, "activity.save.generic")

        self.assertIsNot(unrelated_after, unrelated_before)
        self.assertTrue(contracts._compiler_value_is_issued(self.catalog, kind="catalog"))
        self.assertTrue(contracts._compiler_value_is_issued(selected_compiled, kind="compiled"))
        self.assertIs(
            self.catalog.compiled_activities[self.compiled.activity_id],
            selected_compiled,
        )
        self.assertTrue(contracts._preparation_context_is_issued(context))
        self.assertEqual(self.mechanical.context_cache_identity(context), before)

        selected_cache = self.catalog.compiled_activities
        replaced_cache = dict(selected_cache)
        replaced_cache[self.compiled.activity_id] = copy.copy(self.compiled)
        try:
            object.__setattr__(
                self.catalog, "compiled_activities", MappingProxyType(replaced_cache)
            )
            self.assertFalse(contracts._preparation_context_is_issued(context))
        finally:
            object.__setattr__(self.catalog, "compiled_activities", selected_cache)
        self.assertTrue(contracts._preparation_context_is_issued(context))

        accepted_definitions = self.catalog.frozen_definitions
        changed_definitions = dict(accepted_definitions)
        changed_definitions.pop(self.compiled.activity_id)
        try:
            object.__setattr__(
                self.catalog,
                "frozen_definitions",
                MappingProxyType(changed_definitions),
            )
            self.assertFalse(contracts._preparation_context_is_issued(context))
        finally:
            object.__setattr__(self.catalog, "frozen_definitions", accepted_definitions)
        self.assertTrue(contracts._preparation_context_is_issued(context))

    def test_native_root_issuer_holds_missing_foreign_or_advanced_sources(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold
        from GAME.TOOLS.native_storage import route_native_record

        with self.assertRaises(NativePreparationHold) as missing_command:
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id="command.missing",
                consumer_id=self.consumer,
            )
        self.assertEqual(
            missing_command.exception.operation_status, "AUTHORITY_UNAVAILABLE"
        )

        command_path = route_native_record(
            "runtime.command", (self.accepted["command_id"],)
        ).relative_path
        original_command = self.repository.native_records[command_path]
        foreign_command = dict(original_command, command_id="command.foreign")
        self.repository.native_records[command_path] = foreign_command
        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        stale_command = dict(original_command, input_fingerprint="0" * 64)
        self.repository.native_records[command_path] = stale_command
        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        self.repository.native_records[command_path] = original_command

        resolution_path = route_native_record(
            "runtime.resolution", (self.accepted["root_resolution_id"],)
        ).relative_path
        original_resolution = self.repository.native_records[resolution_path]
        self.repository.native_records.pop(resolution_path)
        with self.assertRaises(NativePreparationHold) as missing_resolution:
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        self.assertEqual(
            missing_resolution.exception.operation_status, "AUTHORITY_UNAVAILABLE"
        )
        self.repository.native_records[resolution_path] = original_resolution

        foreign_resolution = dict(original_resolution, campaign_id="campaign.other")
        self.repository.native_records[resolution_path] = foreign_resolution
        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        self.repository.native_records[resolution_path] = original_resolution

        foreign_root = dict(original_resolution, root_command_id="command.foreign")
        self.repository.native_records[resolution_path] = foreign_root
        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        self.repository.native_records[resolution_path] = original_resolution

        advanced_resolution = dict(
            original_resolution
        )
        advanced_resolution["segments"] = [{"segment_id": "invented"}]
        self.repository.native_records[resolution_path] = advanced_resolution
        with self.assertRaises(NativePreparationHold) as advanced_root:
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
            )
        self.assertEqual(
            advanced_root.exception.operation_status, "AUTHORITY_UNAVAILABLE"
        )
        self.repository.native_records[resolution_path] = original_resolution
        from GAME.TOOLS import activity_contracts as contracts

        fresh = self.preparation()
        self.assertTrue(contracts._preparation_context_is_issued(fresh))

    def test_read_roles_cannot_rebind_the_accepted_root_actor(self):
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "root Actor"):
            self.acquire(role_bindings={"actor": self.other})

    def test_adjudication_cache_join_uses_actual_frozen_basis_members(self):
        from GAME.TOOLS import activity_contracts as contracts

        basis = self.policy_basis()
        context = self._accepted_with_basis(basis)
        self.assertTrue(contracts._preparation_context_is_issued(context))
        identity = self.mechanical.context_cache_identity(context)
        self.assertEqual(self.mechanical.context_cache_identity(context), identity)
        copied_basis_context = replace(
            context, accepted_adjudication=(copy.copy(basis),)
        )
        self.assertFalse(
            contracts._preparation_context_is_issued(copied_basis_context)
        )
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(copied_basis_context)

    def policy_basis(self, *, consumer_id=None, catalog_context=None):
        from DEV.TESTS.test_rd07_recovery import (
            FakeAccess,
            FakeApplicability,
            FakeRepository,
        )
        from GAME.TOOLS.policy_basis import PolicyBasisResolver, PolicySelection

        catalog_context = self.catalog.catalog_context if catalog_context is None else catalog_context
        resolver = PolicyBasisResolver(FakeRepository(), FakeAccess(), FakeApplicability())
        policy = resolver.resolve(self.session._campaign_id,
            PolicySelection("policy.social_leverage", consumer_id or self.compiled.activity_id),
            catalog_context=catalog_context)
        binding = {"source_class": "INVOCATION_ADJUDICATED", "value": 15,
                   "provenance_ref": "sp03:adjudication:dc",
                   "eligibility_basis_fingerprint": "sp03:eligibility",
                   "rules_context_fingerprint": catalog_context.fingerprint,
                   "policy_basis_refs": [policy.policy_ref]}
        return resolver.bind_accepted_basis({"dc": binding}, (), (policy,))

    def test_nonempty_policy_used_by_actual_accepted_command_is_cache_eligible(self):
        basis = self.policy_basis()
        context = self._accepted_with_basis(basis)
        self.assertEqual(self.accepted["action_request"]["parameter_bindings"], basis.runtime_parameter_bindings())
        self.assertEqual(basis.verified_policies[0].consumer_id, self.compiled.activity_id)
        identity = self.mechanical.context_cache_identity(context)
        self.assertEqual(identity, self.mechanical.context_cache_identity(context))

    def test_policy_for_wrong_activity_consumer_rejects_at_cache_seam(self):
        basis = self.policy_basis(consumer_id="activity.save.generic")
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
                adjudication_basis=basis,
            )

    def test_policy_for_other_admitted_catalog_context_rejects_at_cache_seam(self):
        from pathlib import Path

        from GAME.TOOLS import catalog_runtime, ruleset_package

        source = catalog_runtime.load_activity_compiler_contract_source()
        package_id = "hdm.rules.dnd2024-srd52-core"
        _, snapshots = ruleset_package.build_resolved_lock(
            [Path(os.environ["HDM_INSTALLED_STRUCTURAL_TEST"]) / "RULES/packages" / package_id],
            root_package_ids=[package_id], engine_version="1.0-alpha", catalog_generation=2)
        request = self.catalog.catalog_context.to_dict()
        request = {"basis": request["basis"], "definition_dependencies": request["definition_dependencies"]}
        request["basis"]["campaign_definition_frontier"]["state_revision"] += 1
        foreign = catalog_runtime.bind_catalog_context(request, package_snapshots=snapshots,
            engine_contract_inventory_source=source, natural_owner_sources={})
        self.assertNotEqual(foreign.fingerprint, self.catalog.catalog_context.fingerprint)
        basis = self.policy_basis(catalog_context=foreign)
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                self.compiled,
                command_id=self.accepted["command_id"],
                consumer_id=self.consumer,
                adjudication_basis=basis,
            )

    def test_cache_cannot_rebind_root_actor_when_both_actors_are_observed(self):
        context = self.preparation()
        from GAME.TOOLS import activity_contracts as contracts

        observation = context.owner_session.require((self.other,))
        rebound = replace(
            context,
            observation=observation,
            role_bindings={"actor": self.other},
        )
        self.assertFalse(contracts._preparation_context_is_issued(rebound))
        with self.assertRaisesRegex(
            self.mechanical.MechanicalContextError, "authentic source-bound"
        ):
            self.mechanical.context_cache_identity(rebound)

    def test_root_issuer_does_not_invent_a_distinct_child_resolution(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold
        from GAME.TOOLS.activity_runtime import compile_activity

        child = compile_activity(self.catalog, "activity.save.generic")
        with self.assertRaises(NativePreparationHold):
            self.host._current_owner._prepare_root_context(
                self.catalog,
                child,
                command_id=self.accepted["command_id"],
                consumer_id="activity.save.generic.step.0",
            )
