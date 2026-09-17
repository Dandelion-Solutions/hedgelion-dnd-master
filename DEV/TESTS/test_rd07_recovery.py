from __future__ import annotations

import copy
from dataclasses import fields
import unittest

from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
from GAME.TOOLS.policy_basis import (
    ApplicabilityEvidence,
    AuthenticatedPrincipalEvidence,
    AdoptionEvidence,
    CreatorEvidence,
    PolicyBasisResolutionError,
    PolicyBasisResolver,
    PolicySelection,
    PinnedCampaign,
    PlayerEvidence,
)


H = "0123456789abcdef0123456789abcdef01234567"
TREE = "abcdef0123456789abcdef0123456789abcdef01"


def _sidecar(*, source_path: str = "RULES/HOUSE_RULES.md") -> dict[str, object]:
    return {
        "schema_version": 1,
        "source_path": source_path,
        "policies": [
            {
                "policy_id": "policy.social_leverage",
                "kind": "house_rule",
                "authority_class": "INTERPRETIVE_POLICY",
                "lifecycle": "active",
                "source_anchor": "#social-leverage",
                "routing_keys": ["social"],
                "adoption_basis": "active_player_interpretive",
                "adopted_by_player_id": "player-1",
                "supersedes_policy_ids": [],
                "realization_refs": ["activity.check.generic"],
            }
        ],
    }


def _normative() -> str:
    return "# Правила\n\n## Social Leverage\n\nThe adopted ruling applies to social leverage.\n"


class FakeRepository:
    def __init__(self) -> None:
        self.reads: list[tuple[str, str]] = []
        self.files: dict[str, object] = {
            "MANIFEST.yaml": {"rules": {"house_rules_path": "RULES/HOUSE_RULES.md"}},
            "RULES/HOUSE_RULES.yaml": _sidecar(),
            "RULES/HOUSE_RULES.md": _normative(),
        }

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        return PinnedCampaign(campaign_id=campaign_id, revision=H, tree_sha=TREE)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        self.reads.append((pinned.revision, path))
        return copy.deepcopy(self.files[path])


class FakeAccess:
    def resolve_principal(self, pinned: PinnedCampaign) -> AuthenticatedPrincipalEvidence:
        return AuthenticatedPrincipalEvidence(principal_id="principal-1")

    def resolve_creator(self, pinned: PinnedCampaign) -> CreatorEvidence:
        return CreatorEvidence(principal_id="creator-1")

    def resolve_active_player(
        self, pinned: PinnedCampaign, principal: AuthenticatedPrincipalEvidence
    ) -> PlayerEvidence:
        return PlayerEvidence(player_id="player-1", mechanical_override_policy=False)

    def prove_policy_adoption(
        self,
        pinned: PinnedCampaign,
        policy: dict[str, object],
        principal: AuthenticatedPrincipalEvidence,
        creator: CreatorEvidence,
        player: PlayerEvidence,
    ) -> AdoptionEvidence:
        return AdoptionEvidence(
            authority_class="INTERPRETIVE_POLICY",
            adoption_basis="active_player_interpretive",
            adopted_by_player_id="player-1",
        )


class FakeApplicability:
    def prove_policy_applicability(
        self,
        pinned: PinnedCampaign,
        policy: dict[str, object],
        consumer_id: str,
    ) -> ApplicabilityEvidence:
        return ApplicabilityEvidence(policy_id=str(policy["policy_id"]), consumer_id=consumer_id)


class ExactPolicyBasisResolutionTests(unittest.TestCase):
    def test_resolves_one_policy_from_exact_pinned_sidecar_and_normative_anchor(self) -> None:
        repository = FakeRepository()
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        result = resolver.resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )

        self.assertEqual(result.policy_ref, f"policy.social_leverage@{H}")
        self.assertEqual(result.campaign_revision, H)
        self.assertEqual(
            repository.reads,
            [
                (H, "MANIFEST.yaml"),
                (H, "RULES/HOUSE_RULES.yaml"),
                (H, "RULES/HOUSE_RULES.md"),
            ],
        )
        self.assertEqual(result.realization_refs, ("activity.check.generic",))

    def test_untrusted_mapping_cannot_supply_authority_applicability_path_or_revision(self) -> None:
        resolver = PolicyBasisResolver(FakeRepository(), FakeAccess(), FakeApplicability())
        forged = {
            "policy_id": "policy.social_leverage",
            "consumer_id": "activity.check.generic",
            "campaign_revision": H,
            "source_path": "RULES/HOUSE_RULES.md",
            "authority_validated": True,
            "applicable": True,
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "typed policy selection"):
            resolver.resolve("campaign-1", forged, catalog_context=_bind_context())

    def test_missing_normative_anchor_fails_before_realization(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["source_anchor"] = "#missing"
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "normative anchor"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_missing_realization_is_a_typed_gap(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["realization_refs"] = ["activity.not_admitted"]
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "realization gap"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_owner_evidence_must_be_typed_and_is_not_a_caller_boolean(self) -> None:
        class UntrustedAccess(FakeAccess):
            def resolve_principal(self, pinned: PinnedCampaign) -> dict[str, object]:
                return {"principal_id": "principal-1", "authenticated": True}

        resolver = PolicyBasisResolver(FakeRepository(), UntrustedAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "owner-typed evidence"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_sidecar_duplicate_policy_identity_is_rejected(self) -> None:
        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"].append(copy.deepcopy(sidecar["policies"][0]))
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "policy IDs must be unique"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_untrusted_repository_pin_cannot_select_a_revision(self) -> None:
        class UntrustedRepository(FakeRepository):
            def pin_campaign(self, campaign_id: str) -> dict[str, str]:
                return {"campaign_id": campaign_id, "revision": H, "tree_sha": TREE}

        resolver = PolicyBasisResolver(UntrustedRepository(), FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "trusted exact campaign pin"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_sidecar_authority_class_and_adoption_basis_must_obey_access_law(self) -> None:
        class InvalidShapeAccess(FakeAccess):
            def prove_policy_adoption(
                self,
                pinned: PinnedCampaign,
                policy: dict[str, object],
                principal: AuthenticatedPrincipalEvidence,
                creator: CreatorEvidence,
                player: PlayerEvidence,
            ) -> AdoptionEvidence:
                return AdoptionEvidence(
                    authority_class="INTERPRETIVE_POLICY",
                    adoption_basis="campaign_creator",
                    adopted_by_player_id=None,
                )

        repository = FakeRepository()
        sidecar = _sidecar()
        sidecar["policies"][0]["adoption_basis"] = "campaign_creator"
        sidecar["policies"][0]["adopted_by_player_id"] = None
        repository.files["RULES/HOUSE_RULES.yaml"] = sidecar
        resolver = PolicyBasisResolver(repository, InvalidShapeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "adoption basis is not admitted"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_sidecar_and_manifest_house_rules_paths_must_match(self) -> None:
        repository = FakeRepository()
        repository.files["RULES/HOUSE_RULES.yaml"] = _sidecar(source_path="RULES/OTHER_RULES.md")
        resolver = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability())

        with self.assertRaisesRegex(PolicyBasisResolutionError, "paths differ"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )

    def test_policy_selection_rejects_consumer_outside_active_adjudication_surface(self) -> None:
        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted adjudication consumer"):
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.not_admitted")

    def test_direct_resolved_policy_basis_construction_is_not_a_provenance_source(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        values = {
            item.name: getattr(resolved, item.name)
            for item in fields(resolved)
            if not item.name.startswith("_")
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "resolver-issued"):
            type(resolved)(**values)

    def test_object_new_forged_policy_basis_cannot_bind_accepted_inputs(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        forged = object.__new__(type(resolved))
        for item in fields(resolved):
            object.__setattr__(forged, item.name, getattr(resolved, item.name))
        object.__setattr__(forged, "policy_ref", "policy.forged@" + "f" * 40)

        with self.assertRaisesRegex(PolicyBasisResolutionError, "resolver-issued"):
            PolicyBasisResolver.bind_accepted_basis(
                {
                    "dc": {
                        "source_class": "INVOCATION_ADJUDICATED",
                        "value": 15,
                        "provenance_ref": "turn-1:dc",
                        "eligibility_basis_fingerprint": "eligibility-A",
                        "rules_context_fingerprint": "rules-A",
                        "policy_basis_refs": [forged.policy_ref],
                    }
                },
                (),
                (forged,),
            )

    def test_invocation_fact_must_use_the_exact_admitted_fact_edge(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.spell.fire_bolt"),
            catalog_context=_bind_context(),
        )
        fact = {
            "fact_id": "fiction.target_visible",
            "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "turn-1:reachable",
            "consumer_id": "activity.spell.fire_bolt",
            "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64,
            "policy_basis_refs": [resolved.policy_ref],
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted fact edge"):
            PolicyBasisResolver.bind_accepted_basis({}, (fact,), (resolved,))

    def test_invocation_fact_consumer_must_be_one_of_the_seven_compiled_edges(self) -> None:
        repository = FakeRepository()
        resolved = PolicyBasisResolver(repository, FakeAccess(), FakeApplicability()).resolve(
            "campaign-1",
            PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
            catalog_context=_bind_context(),
        )
        fact = {
            "fact_id": "fiction.target_reachable",
            "value": True,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "turn-1:reachable",
            "consumer_id": "activity.not_admitted",
            "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64,
            "policy_basis_refs": [resolved.policy_ref],
        }

        with self.assertRaisesRegex(PolicyBasisResolutionError, "admitted fact consumer"):
            PolicyBasisResolver.bind_accepted_basis({}, (fact,), (resolved,))

    def test_applicability_witness_must_match_the_selected_consumer(self) -> None:
        class CrossConsumerApplicability(FakeApplicability):
            def prove_policy_applicability(
                self,
                pinned: PinnedCampaign,
                policy: dict[str, object],
                consumer_id: str,
            ) -> ApplicabilityEvidence:
                return ApplicabilityEvidence(
                    policy_id=str(policy["policy_id"]), consumer_id="activity.save.generic"
                )

        resolver = PolicyBasisResolver(FakeRepository(), FakeAccess(), CrossConsumerApplicability())
        with self.assertRaisesRegex(PolicyBasisResolutionError, "applicability evidence identity mismatch"):
            resolver.resolve(
                "campaign-1",
                PolicySelection(policy_id="policy.social_leverage", consumer_id="activity.check.generic"),
                catalog_context=_bind_context(),
            )


if __name__ == "__main__":
    unittest.main()
