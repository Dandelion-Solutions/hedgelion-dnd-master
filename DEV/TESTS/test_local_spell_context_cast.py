"""SP03 exact compiled-read slice, using actual installed SP02 and P0 owners.

This slice establishes no selector result, cast, RNG or native consequence.
"""

from __future__ import annotations

import copy
import importlib.util
import os
import unittest
from dataclasses import replace


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

            def read_exact_path(inner, pinned, path):
                if inner.actor_missing and path == route_native_record("world.actor", (ACTOR_ID,)).relative_path:
                    raise KeyError(path)
                if path == route_native_record("world.actor", ("actor.other",)).relative_path:
                    inner.path_reads.append((pinned.revision, path))
                    return copy.deepcopy(inner.other)
                return super().read_exact_path(pinned, path)

        self.repository = Repository()
        self.store = NativeHotStore(":memory:")
        self.addCleanup(self.store.close)
        host, _source = _selected_host(self.store, repository=self.repository)
        self.session = host._current_owner.begin(host._begin_operation())
        self.roles = {"actor": self.owner}
        self.consumer = "activity.check.generic.step.0"
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
        from GAME.TOOLS.runtime_execution import accept_command

        proposal = _proposal()
        proposal["action_request"]["actor_id"] = self.owner.identity[0]
        self.accepted = accept_command(_interpreter_result(), self.catalog.catalog_context,
            {"definition_id": self.compiled.activity_id, "kind": "definition.activity"}, proposal)

    def acquire(self, **changes):
        arguments = {"consumer_id": self.consumer, "owner_session": self.session,
                     "role_bindings": self.roles, "accepted_command": self.accepted}
        arguments.update(changes)
        return self.mechanical.acquire_observation(self.compiled, **arguments)

    def preparation(self):
        """SP01 trusted issuer over actual observations and authentic compiled handles."""
        from GAME.TOOLS import activity_contracts as contracts
        accepted = self.accepted
        resolution = {
            "root_command_id": accepted["command_id"], "initiating_command_id": accepted["command_id"],
            "activity_id": self.compiled.activity_id, "actor_id": self.owner.identity[0],
            "ruleset_set_digest_generation": 1, "ruleset_set_sha256": self.compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": self.catalog.catalog_context.fingerprint,
            "status": "RUNNING", "next_segment_sequence": 1, "invocation_facts": [],
            "fixed_rng_results": [], "prior_step_exports": {}, "child_resolution_ids": [], "segments": [],
        }
        return contracts.NativePreparationContext(
            catalog=self.catalog, compiled=self.compiled, consumer_id=self.consumer,
            occurrence_id="occ.read", execution_ref=contracts.ExecutionRef(accepted["command_id"], accepted["root_resolution_id"]),
            observation=self.acquire(), owner_session=self.session, role_bindings=self.roles,
            accepted_command=accepted, resolution=resolution, accepted_fact_refs=(), accepted_adjudication=(),
            policy_refs=(), fixed_roll_refs=(), prospective_owner_documents=(), allocation_handles=(),
            _builder_token=object(), _issue_seal=contracts._CONTRACT_SEAL,
        )

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

    def test_material_policy_order_is_canonical_and_affects_identity(self):
        context = self.preparation()
        before = self.mechanical.context_cache_identity(context)
        changed = replace(context, policy_refs=("policy.one", "policy.two"))
        self.assertNotEqual(self.mechanical.context_cache_identity(changed), before)
        for refs in (("policy.two", "policy.one"), ("policy.one", "policy.one")):
            with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "canonical"):
                self.mechanical.context_cache_identity(replace(context, policy_refs=refs))

    def test_post_issuance_command_mutation_and_state_substitution_reject(self):
        from GAME.TOOLS.activity_contracts import ActivityContractError

        context = self.preparation()
        with self.assertRaises(ActivityContractError):
            replace(context, accepted_command=dict(context.accepted_command, hp=100))
        forged = dict(context.accepted_command)
        forged["input_fingerprint"] = "0" * 64
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "accepted command"):
            self.mechanical.context_cache_identity(replace(context, accepted_command=forged))

    def test_prospective_documents_require_future_same_builder_issuance(self):
        from GAME.TOOLS.hot_store import OwnerDocument

        context = self.preparation()
        read = context.observation.require(self.owner)
        document = OwnerDocument(self.session._campaign_id, self.owner.family_key,
            self.owner.identity, read.payload, read.source_basis, read.generation)
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "prospective"):
            self.mechanical.context_cache_identity(replace(context, prospective_owner_documents=(document,)))

    def test_fake_context_and_stale_observation_are_not_cache_authority(self):
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        with self.assertRaises(self.mechanical.MechanicalContextError):
            self.mechanical.context_cache_identity({"hp": 8})
        context = self.preparation()
        self.session.require((self.other,))
        with self.assertRaises(NativePreparationHold):
            self.mechanical.context_cache_identity(context)

    def test_read_roles_cannot_rebind_the_accepted_root_actor(self):
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "root Actor"):
            self.acquire(role_bindings={"actor": self.other})

    def test_adjudication_cache_join_uses_actual_frozen_basis_members(self):
        from GAME.TOOLS.policy_basis import AcceptedAdjudicationBasis

        context = self.preparation()
        basis = AcceptedAdjudicationBasis({}, (), ())
        joined = replace(context, accepted_adjudication=(basis,))
        self.assertNotEqual(self.mechanical.context_cache_identity(joined),
                            self.mechanical.context_cache_identity(context))
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "adjudication"):
            self.mechanical.context_cache_identity(replace(context, accepted_adjudication=(copy.copy(basis),)))

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
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
        from GAME.TOOLS.runtime_execution import accept_command

        basis = self.policy_basis()
        proposal = _proposal()
        proposal["action_request"]["actor_id"] = self.owner.identity[0]
        proposal["action_request"]["parameter_bindings"] = basis.runtime_parameter_bindings()
        self.accepted = accept_command(_interpreter_result(), self.catalog.catalog_context,
            {"definition_id": self.compiled.activity_id, "kind": "definition.activity"},
            proposal, adjudication_basis=basis)
        context = self.preparation()
        resolution = dict(context.resolution, parameter_bindings=basis.runtime_parameter_bindings())
        context = replace(context, resolution=resolution, accepted_adjudication=(basis,))
        self.assertEqual(self.accepted["action_request"]["parameter_bindings"], basis.runtime_parameter_bindings())
        self.assertEqual(basis.verified_policies[0].consumer_id, self.compiled.activity_id)
        identity = self.mechanical.context_cache_identity(context)
        self.assertEqual(identity, self.mechanical.context_cache_identity(context))

    def test_policy_for_wrong_activity_consumer_rejects_at_cache_seam(self):
        context = self.preparation()
        basis = self.policy_basis(consumer_id="activity.save.generic")
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "adjudication") as raised:
            self.mechanical.context_cache_identity(replace(context, accepted_adjudication=(basis,)))
        self.assertIn("policy applicability witness", str(raised.exception.__cause__))

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
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "adjudication") as raised:
            self.mechanical.context_cache_identity(replace(self.preparation(), accepted_adjudication=(basis,)))
        self.assertIn("resolver-selected catalog context", str(raised.exception.__cause__))

    def test_cache_cannot_rebind_root_actor_when_both_actors_are_observed(self):
        context = self.preparation()
        observation = self.session.require((self.other,))
        context = replace(context, observation=observation)
        self.mechanical.context_cache_identity(context)
        rebound = replace(context, role_bindings={"actor": self.other})
        self.assertEqual(set(rebound.observation.key_union), {self.owner, self.other})
        with self.assertRaisesRegex(self.mechanical.MechanicalContextError, "root Actor"):
            self.mechanical.context_cache_identity(rebound)

    def test_cache_preserves_real_child_activity_and_actor_binding(self):
        from GAME.TOOLS import activity_contracts as contracts
        from GAME.TOOLS.activity_runtime import compile_activity

        root = self.preparation()
        child = compile_activity(self.catalog, "activity.save.generic")
        observation = self.session.require((self.other,))
        resolution = dict(root.resolution, activity_id=child.activity_id,
                          actor_id=self.other.identity[0], causal_invocation_key="resolution-1:segment:1:event:1")
        resolution.pop("initiating_command_id")
        context = replace(root, compiled=child, consumer_id="activity.save.generic.step.0",
            occurrence_id="occ.child", execution_ref=contracts.ExecutionRef(root.execution_ref.command_id, "resolution.child"),
            observation=observation, role_bindings={"actor": self.other}, resolution=resolution)
        self.assertEqual(context.accepted_command["action_request"]["actor_id"], self.owner.identity[0])
        self.assertNotEqual(context.compiled.activity_id, root.compiled.activity_id)
        self.mechanical.context_cache_identity(context)
