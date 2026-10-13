"""Native Sorcerer source-basis preparation over the installed compiler path."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)


def _run_installed_source_basis_case(
    runtime_root: Path,
    recipe: dict[str, object],
    dependency_kinds: dict[str, str],
    scratch: Path,
    *,
    test_name: str = "PinnedNativeSourceBasisTests",
    route_activity_in_package: bool = False,
    expected_route: bool = True,
    expected_disposition: str | None = None,
) -> subprocess.CompletedProcess[str]:
    scratch.mkdir()
    installed_root = scratch / "GAME"
    shutil.copytree(runtime_root, installed_root)
    case_path = scratch / "source-basis-case.json"
    case_path.write_text(
        json.dumps(
            {
                "recipe": recipe,
                "dependency_kinds": dependency_kinds,
                "route_activity_in_package": route_activity_in_package,
                "expected_route": expected_route,
                "expected_disposition": expected_disposition,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["HDM_INSTALLED_STRUCTURAL_TEST"] = str(installed_root)
    environment["HDM_SP03_SOURCE_BASIS_CASE"] = str(case_path)
    environment["HDM_SP03_SOURCE_BASIS_TEST_SCRATCH"] = str(scratch)
    environment["PYTHONPATH"] = os.pathsep.join((str(scratch), str(ROOT)))
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            f"DEV.TESTS.test_sp03_native_source_basis.{test_name}",
            "-q",
        ],
        cwd=installed_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


@unittest.skipUnless(
    "HDM_INSTALLED_STRUCTURAL_TEST" in os.environ, "installed runtime driver"
)
class PinnedNativeSourceBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from GAME.TOOLS import activity_runtime, catalog_runtime, ruleset_package

        cls.runtime_root = Path(os.environ["HDM_INSTALLED_STRUCTURAL_TEST"]).resolve()
        if Path.cwd().resolve() != cls.runtime_root:
            raise AssertionError(
                "compiler probe did not run from the installed package root"
            )
        case = json.loads(
            Path(os.environ["HDM_SP03_SOURCE_BASIS_CASE"]).read_text(encoding="utf-8")
        )
        cls.case = case
        cls.recipe = case["recipe"]
        dependency_kinds = case["dependency_kinds"]
        source = catalog_runtime.load_activity_compiler_contract_source()
        package_id = "hdm.rules.dnd2024-srd52-core"
        package_root = cls.runtime_root / "RULES/packages" / package_id
        manifest = ruleset_package.load_json_bytes(
            (package_root / "ruleset-package-manifest.json").read_bytes()
        )
        lock, snapshots = ruleset_package.build_resolved_lock(
            [package_root],
            root_package_ids=[package_id],
            engine_version=manifest["engine_requirement"]["engine_version"],
            catalog_generation=manifest["catalog_generation"],
        )
        recipe = cls.recipe
        frontier = {
            "frontier_id": "campaign.definitions",
            "state_revision": 5,
            "definition_ids": sorted({recipe["id"], *dependency_kinds}),
        }
        raw = ruleset_package.canonical_json(recipe)
        evidence = {
            "definition_id": recipe["id"],
            "kind": recipe["kind"],
            "owner_domain": "campaign",
            "scope": "campaign.definition_frontier",
            "route": f"campaign/definitions/{recipe['id']}.json",
            "pinned_revision": 5,
            "content_sha256": ruleset_package.sha256(raw),
        }
        package_content_sha256 = lock["packages"][0]["content_sha256"]
        route_activity_in_package = case.get("route_activity_in_package") is True
        natural_owner_evidence: list[dict[str, object]] = (
            [] if route_activity_in_package else [evidence]
        )
        natural_owner_sources: dict[str, object] = (
            {}
            if route_activity_in_package
            else {
                "campaign": {
                    "selected_frontier": frontier,
                    "members": [evidence],
                    "immutable_member_bytes": {evidence["route"]: raw},
                }
            }
        )
        definition_dependencies = [
            {
                "source_type": "ruleset_package",
                "definition_id": identity,
                "kind": kind,
                "package_id": package_id,
                "package_content_sha256": package_content_sha256,
            }
            for identity, kind in dependency_kinds.items()
        ]
        if not route_activity_in_package:
            definition_dependencies.append(
                {
                    "source_type": "natural_owner",
                    **{
                        key: value
                        for key, value in evidence.items()
                        if key != "content_sha256"
                    },
                    "evidence_sha256": ruleset_package.sha256(
                        catalog_runtime.NATURAL_OWNER_EVIDENCE_DOMAIN
                        + ruleset_package.canonical_json(evidence)
                    ),
                }
            )
        request = {
            "basis": {
                "catalog_generation": manifest["catalog_generation"],
                "engine_version": manifest["engine_requirement"]["engine_version"],
                "engine_contract_inventory": catalog_runtime._thaw(
                    source.engine_contract_inventory
                ),
                "engine_contract_inventory_sha256": source.engine_contract_inventory[
                    "inventory_sha256"
                ],
                "ruleset_lock": lock,
                "campaign_definition_frontier": frontier,
                "natural_owner_evidence": natural_owner_evidence,
            },
            "definition_dependencies": definition_dependencies,
        }
        cls.catalog = activity_runtime.admit_activity_catalog(
            request,
            package_snapshots=snapshots,
            engine_contract_inventory_source=source,
            natural_owner_sources=natural_owner_sources,
            compiler_generation=1,
            mode_policy_profile_id="execution.spell_cast.srd521",
        )
        cls.compiled = activity_runtime.compile_activity(cls.catalog, str(recipe["id"]))
        cls.cast_source = next(
            row
            for row in cls.compiled.cast_source_bindings
            if row.binding.consumer_id.endswith(".step.0")
        )

    def test_actor_reference_inventory_matches_current_closed_schemas(self) -> None:
        from GAME.TOOLS import spell_cast

        spell_schema = json.loads(
            (ROOT / "DEV/SCHEMAS/spell-native-profile-values.schema.json").read_text(
                encoding="utf-8"
            )
        )
        actor_schema = json.loads(
            (ROOT / "DEV/SCHEMAS/world-actor-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        effect_schema = json.loads(
            (ROOT / "DEV/SCHEMAS/world-effect-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        asset_schema = json.loads(
            (ROOT / "DEV/SCHEMAS/world-asset-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        spell_defs = spell_schema["$defs"]

        self.assertEqual(
            set(spell_cast._EFFECT_DIRECT_ACTOR_REFERENCE_FIELDS),
            {"target_id", "source_id"},
        )
        self.assertTrue(
            set(spell_cast._EFFECT_DIRECT_ACTOR_REFERENCE_FIELDS)
            <= set(effect_schema["properties"])
        )
        self.assertEqual(
            set(spell_cast._SUBJECT_BINDING_ACTOR_REFERENCE_FIELDS),
            {"principal_subject_id", "physical_actor_id"},
        )
        self.assertEqual(
            set(spell_cast._SUBJECT_BINDING_ACTOR_REFERENCE_FIELDS)
            | {"domain", "relation_effect_id", "binding_generation", "rebind_event_id"},
            set(spell_defs["effectSubjectBinding"]["properties"]),
        )
        self.assertEqual(
            set(spell_cast._CONTROL_ACTOR_REFERENCE_FIELDS),
            {"controller_principal_subject_id", "controlled_physical_actor_id"},
        )
        self.assertEqual(
            set(spell_cast._CONTROL_ACTOR_REFERENCE_FIELDS)
            | {"command_generation", "command_ref", "phase"},
            set(spell_defs["controlState"]["properties"]),
        )

        identity_profiles = {
            "lifecycle.identity.magic_jar": (
                "jarState",
                {
                    "profile_id",
                    "relation_generation",
                    "principal_subject_id",
                    "activation_occurrence_id",
                    "restoration_policy_id",
                    "phase",
                    "original_body_actor_id",
                    "receptacle_asset_id",
                    "host_body_actor_id",
                    "displaced_principal_subject_id",
                    "active_body_actor_id",
                },
                {
                    "principal_subject_id",
                    "original_body_actor_id",
                    "host_body_actor_id",
                    "displaced_principal_subject_id",
                    "active_body_actor_id",
                },
            ),
            "lifecycle.identity.astral_projection": (
                "astralState",
                {
                    "profile_id",
                    "relation_generation",
                    "principal_subject_id",
                    "activation_occurrence_id",
                    "restoration_policy_id",
                    "phase",
                    "original_body_actor_id",
                    "astral_proxy_actor_id",
                    "tether_ref",
                    "replica_group_ref",
                },
                {
                    "principal_subject_id",
                    "original_body_actor_id",
                    "astral_proxy_actor_id",
                },
            ),
            "lifecycle.identity.clone": (
                "cloneState",
                {
                    "profile_id",
                    "relation_generation",
                    "principal_subject_id",
                    "activation_occurrence_id",
                    "restoration_policy_id",
                    "phase",
                    "replica_asset_id",
                    "vessel_asset_id",
                    "maturity_occurrence_ref",
                    "death_occurrence_ref",
                    "transfer_occurrence_ref",
                    "original_remains_asset_id",
                },
                {"principal_subject_id"},
            ),
            "lifecycle.identity.simulacrum": (
                "simulacrumState",
                {
                    "profile_id",
                    "relation_generation",
                    "principal_subject_id",
                    "activation_occurrence_id",
                    "restoration_policy_id",
                    "phase",
                    "replica_actor_id",
                    "construction_basis_ref",
                    "creation_occurrence_id",
                },
                {"principal_subject_id", "replica_actor_id"},
            ),
        }
        common_properties = set(spell_defs["identityCommon"]["properties"])
        identity_actor_reference_fields = dict(
            spell_cast._IDENTITY_ACTOR_REFERENCE_FIELDS_BY_PROFILE
        )
        for profile_id, (
            definition_name,
            expected_properties,
            expected_actor_fields,
        ) in identity_profiles.items():
            definition = spell_defs[definition_name]
            variant_properties = {
                key
                for clause in definition["allOf"]
                for key in clause.get("properties", {})
            }
            self.assertEqual(
                common_properties | variant_properties, expected_properties
            )
            self.assertEqual(
                set(identity_actor_reference_fields[profile_id]), expected_actor_fields
            )
        self.assertEqual(set(identity_actor_reference_fields), set(identity_profiles))

        conversion_profiles = {
            "lifecycle.conversion.animate_objects": (
                {
                    "profile_id",
                    "asset_id",
                    "animated_actor_id",
                    "activation_occurrence_id",
                    "phase",
                },
                {"animated_actor_id"},
                {"asset_id"},
            ),
            "lifecycle.conversion.true_polymorph_object_creature": (
                {
                    "profile_id",
                    "asset_id",
                    "creature_actor_id",
                    "activation_occurrence_id",
                    "phase",
                },
                {"creature_actor_id"},
                {"asset_id"},
            ),
            "lifecycle.conversion.true_polymorph_creature_object": (
                {
                    "profile_id",
                    "principal_subject_id",
                    "object_asset_id",
                    "activation_occurrence_id",
                    "binding_generation",
                    "restoration_basis_ref",
                    "return_adjudication_basis_ref",
                    "phase",
                    "lifetime_stage",
                    "object_experience_scope_ref",
                    "merged_asset_ids",
                    "independent_body_relation_ref",
                    "original_body_actor_id",
                },
                {"principal_subject_id", "original_body_actor_id"},
                {"object_asset_id", "merged_asset_ids"},
            ),
        }
        conversion_rows = {
            row["properties"]["profile_id"]["const"]: row["properties"]
            for row in spell_defs["conversionState"]["oneOf"]
        }
        self.assertEqual(set(conversion_rows), set(conversion_profiles))
        for profile_id, (
            expected_properties,
            expected_actor_fields,
            expected_asset_fields,
        ) in conversion_profiles.items():
            self.assertEqual(set(conversion_rows[profile_id]), expected_properties)
            self.assertEqual(
                set(
                    dict(spell_cast._CONVERSION_ACTOR_REFERENCE_FIELDS_BY_PROFILE)[
                        profile_id
                    ]
                ),
                expected_actor_fields,
            )
            self.assertEqual(
                set(
                    dict(spell_cast._CONVERSION_ASSET_REFERENCE_FIELDS_BY_PROFILE)[
                        profile_id
                    ]
                ),
                expected_asset_fields,
            )
        identity_asset_reference_fields = dict(
            spell_cast._IDENTITY_ASSET_REFERENCE_FIELDS_BY_PROFILE
        )
        expected_identity_asset_fields = {
            "lifecycle.identity.magic_jar": {"receptacle_asset_id"},
            "lifecycle.identity.astral_projection": set(),
            "lifecycle.identity.clone": {
                "replica_asset_id",
                "vessel_asset_id",
                "original_remains_asset_id",
            },
            "lifecycle.identity.simulacrum": set(),
        }
        self.assertEqual(
            set(identity_asset_reference_fields), set(expected_identity_asset_fields)
        )
        for profile_id, asset_fields in expected_identity_asset_fields.items():
            self.assertEqual(
                set(identity_asset_reference_fields[profile_id]), asset_fields
            )
        self.assertEqual(
            spell_defs["conversionState"]["oneOf"][2]["properties"][
                "independent_body_relation_ref"
            ]["$ref"],
            "#/$defs/ownerRevisionRef",
        )
        self.assertEqual(
            spell_defs["ownerRevisionRef"]["properties"]["owner_ref"]["$ref"],
            "#/$defs/ownerRef",
        )
        self.assertIn(
            "world.actor",
            spell_defs["ownerRef"]["properties"]["family_key"]["enum"],
        )

        form_properties = set(spell_defs["formState"]["properties"])
        self.assertEqual(
            form_properties,
            {
                "profile_id",
                "form_archetype_id",
                "activation_occurrence_id",
                "form_generation",
            },
        )
        self.assertEqual(
            getattr(spell_cast, "_FORM_STATE_ACTOR_REFERENCE_FIELDS", None), ()
        )
        self.assertEqual(
            getattr(spell_cast, "_INDEPENDENT_BODY_RELATION_REFERENCE_FIELD", None),
            "independent_body_relation_ref",
        )

        asset_state_properties = set(asset_schema["properties"])
        self.assertEqual(
            set(spell_cast._ASSET_ACTOR_REFERENCE_FIELDS),
            {"owner_actor_id", "attuned_actor_id"},
        )
        self.assertTrue(
            set(spell_cast._ASSET_ACTOR_REFERENCE_FIELDS) <= asset_state_properties
        )
        self.assertEqual(
            set(spell_cast._ASSET_CONVERSION_ACTOR_REFERENCE_FIELDS),
            {"principal_subject_id"},
        )
        self.assertEqual(
            set(spell_defs["conversionMembership"]["properties"]),
            {
                "conversion_effect_id",
                "principal_subject_id",
                "binding_generation",
                "mode",
            },
        )
        self.assertEqual(
            set(spell_defs["equipmentTransform"]["properties"]),
            {"source_effect_id", "transition_occurrence_id", "mode"},
        )
        self.assertEqual(
            set(spell_defs["replicaOrigin"]["properties"]),
            {"source_asset_id", "relation_effect_id", "creation_occurrence_id"},
        )
        self.assertEqual(
            set(asset_state_properties),
            {
                "owner_actor_id",
                "container_asset_id",
                "location_id",
                "quantity",
                "equipment",
                "attuned_actor_id",
                "resources",
                "durability",
                "access",
                "equipment_transform",
                "replica_origin",
                "conversion_membership",
                "spell_progress",
                "details",
            },
        )

        embodiment_profiles = {
            "actor.embodiment.principal": (
                {"profile_id", "relation_effect_id"},
                set(),
            ),
            "actor.embodiment.body": (
                {
                    "profile_id",
                    "principal_subject_id",
                    "relation_effect_id",
                    "construction_basis_ref",
                },
                {"principal_subject_id"},
            ),
            "actor.embodiment.astral_proxy": (
                {
                    "profile_id",
                    "principal_subject_id",
                    "relation_effect_id",
                    "construction_basis_ref",
                    "replica_group_ref",
                },
                {"principal_subject_id"},
            ),
            "actor.embodiment.object_suspension": (
                {
                    "profile_id",
                    "relation_effect_id",
                    "object_asset_id",
                    "restoration_basis_ref",
                    "binding_generation",
                },
                set(),
            ),
        }
        actual_embodiments = {
            row["properties"]["profile_id"]["const"]: set(row["properties"])
            for row in actor_schema["$defs"]["embodiment"]["oneOf"]
        }
        self.assertEqual(set(actual_embodiments), set(embodiment_profiles))
        production_embodiment_fields = dict(
            spell_cast._ACTOR_EMBODIMENT_ACTOR_REFERENCE_FIELDS_BY_PROFILE
        )
        self.assertEqual(set(production_embodiment_fields), set(embodiment_profiles))
        for profile_id, (schema_fields, actor_fields) in embodiment_profiles.items():
            self.assertEqual(actual_embodiments[profile_id], schema_fields)
            self.assertEqual(
                set(production_embodiment_fields[profile_id]), actor_fields
            )

    def test_each_closed_relation_actor_reference_field_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        identity_bases = {
            "lifecycle.identity.magic_jar": {
                "profile_id": "lifecycle.identity.magic_jar",
                "relation_generation": 1,
                "principal_subject_id": "actor.other",
                "activation_occurrence_id": "resolution.identity",
                "restoration_policy_id": "policy.restore",
                "phase": "possessed",
                "original_body_actor_id": "actor.other",
                "receptacle_asset_id": "asset.receptacle",
                "host_body_actor_id": "actor.other",
                "displaced_principal_subject_id": "actor.other",
                "active_body_actor_id": "actor.other",
            },
            "lifecycle.identity.astral_projection": {
                "profile_id": "lifecycle.identity.astral_projection",
                "relation_generation": 1,
                "principal_subject_id": "actor.other",
                "activation_occurrence_id": "resolution.identity",
                "restoration_policy_id": "policy.restore",
                "phase": "projected",
                "original_body_actor_id": "actor.other",
                "astral_proxy_actor_id": "actor.other",
                "tether_ref": "relation.tether",
                "replica_group_ref": "group.replica",
            },
            "lifecycle.identity.clone": {
                "profile_id": "lifecycle.identity.clone",
                "relation_generation": 1,
                "principal_subject_id": "actor.other",
                "activation_occurrence_id": "resolution.identity",
                "restoration_policy_id": "policy.restore",
                "phase": "growing",
                "replica_asset_id": "asset.replica",
                "vessel_asset_id": "asset.vessel",
                "maturity_occurrence_ref": "resolution.maturity",
            },
            "lifecycle.identity.simulacrum": {
                "profile_id": "lifecycle.identity.simulacrum",
                "relation_generation": 1,
                "principal_subject_id": "actor.other",
                "activation_occurrence_id": "resolution.identity",
                "restoration_policy_id": "policy.restore",
                "phase": "active",
                "replica_actor_id": "actor.other",
                "construction_basis_ref": "basis.simulacrum",
                "creation_occurrence_id": "resolution.simulacrum",
            },
        }
        conversion_bases = {
            "lifecycle.conversion.animate_objects": {
                "profile_id": "lifecycle.conversion.animate_objects",
                "asset_id": "asset.object",
                "animated_actor_id": "actor.other",
                "activation_occurrence_id": "resolution.convert",
                "phase": "animated",
            },
            "lifecycle.conversion.true_polymorph_object_creature": {
                "profile_id": "lifecycle.conversion.true_polymorph_object_creature",
                "asset_id": "asset.object",
                "creature_actor_id": "actor.other",
                "activation_occurrence_id": "resolution.convert",
                "phase": "temporary",
            },
            "lifecycle.conversion.true_polymorph_creature_object": {
                "profile_id": "lifecycle.conversion.true_polymorph_creature_object",
                "principal_subject_id": "actor.other",
                "object_asset_id": "asset.object",
                "activation_occurrence_id": "resolution.convert",
                "binding_generation": 1,
                "restoration_basis_ref": "basis.restore",
                "return_adjudication_basis_ref": "basis.return",
                "phase": "object",
                "lifetime_stage": "concentration",
                "object_experience_scope_ref": "scope.object",
                "merged_asset_ids": [],
                "original_body_actor_id": "actor.other",
                "independent_body_relation_ref": {
                    "owner_ref": {
                        "family_key": "world.effect",
                        "identity": ["effect.other-relation"],
                    },
                    "source_basis": "revision.other",
                    "generation": 1,
                    "fingerprint": "0" * 64,
                },
            },
        }
        states: list[tuple[str, dict[str, object]]] = []
        for field_name in spell_cast._SUBJECT_BINDING_ACTOR_REFERENCE_FIELDS:
            binding: dict[str, object] = {
                "domain": "physical",
                "principal_subject_id": "actor.other",
                "physical_actor_id": "actor.other",
                "binding_generation": 1,
            }
            binding[field_name] = "actor.mara"
            states.append(
                (f"subject_binding.{field_name}", {"subject_binding": binding})
            )
        for (
            profile_id,
            fields,
        ) in spell_cast._IDENTITY_ACTOR_REFERENCE_FIELDS_BY_PROFILE:
            for field_name in fields:
                state = deepcopy(identity_bases[profile_id])
                state[field_name] = "actor.mara"
                states.append(
                    (
                        f"identity_state.{profile_id}.{field_name}",
                        {"identity_state": state},
                    )
                )
        for field_name in spell_cast._CONTROL_ACTOR_REFERENCE_FIELDS:
            state = {
                "controller_principal_subject_id": "actor.other",
                "controlled_physical_actor_id": "actor.other",
                "command_generation": 1,
                "phase": "controlled",
            }
            state[field_name] = "actor.mara"
            states.append((f"control_state.{field_name}", {"control_state": state}))
        for (
            profile_id,
            fields,
        ) in spell_cast._CONVERSION_ACTOR_REFERENCE_FIELDS_BY_PROFILE:
            for field_name in fields:
                state = deepcopy(conversion_bases[profile_id])
                state[field_name] = "actor.mara"
                states.append(
                    (
                        f"conversion_state.{profile_id}.{field_name}",
                        {"conversion_state": state},
                    )
                )

        for index, (label, relation_state) in enumerate(states):
            effect = self._effect_record(
                f"effect.schema-actor-reference-{index}",
                additional_state=relation_state,
            )
            context, _repository, _store, _host, _accepted = self._prepare(
                effect_records=(effect,)
            )
            with (
                self.subTest(actor_reference=label),
                self.assertRaises(NativePreparationHold),
            ):
                spell_cast._prepare_cast_source_basis(context)

    def test_foreign_source_field_alone_is_not_a_caster_relation(self) -> None:
        from GAME.TOOLS import spell_cast

        effect = self._effect_record(
            "effect.source-only",
            target_id="actor.other",
            source_id="actor.mara",
        )
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        prepared = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(
            prepared.source_basis.value["source_disposition"],
            "SELECTED_PREPARED_LEVEL1",
        )

    def test_foreign_magic_jar_asset_reference_is_relevant_after_binding_exclusion(
        self,
    ) -> None:
        from GAME.TOOLS import mechanical_sources, spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold
        from GAME.TOOLS.current_owner import CurrentOwnerStatus, NativeOwnerRef

        for asset_owner_id, should_hold in (
            ("actor.mara", True),
            ("actor.other", False),
        ):
            asset_id = f"asset.receptacle-{asset_owner_id.rsplit('.', 1)[-1]}"
            effect = self._effect_record(
                f"effect.magic-jar-{asset_owner_id.rsplit('.', 1)[-1]}",
                target_id="actor.mara",
                source_id="actor.other",
                additional_state={
                    "subject_binding": {
                        "domain": "physical",
                        "principal_subject_id": "actor.other",
                        "physical_actor_id": "actor.other",
                        "binding_generation": 1,
                    },
                    "identity_state": {
                        "profile_id": "lifecycle.identity.magic_jar",
                        "relation_generation": 1,
                        "principal_subject_id": "actor.other",
                        "activation_occurrence_id": "resolution.identity",
                        "restoration_policy_id": "policy.restore",
                        "phase": "container",
                        "original_body_actor_id": "actor.other",
                        "receptacle_asset_id": asset_id,
                    },
                },
            )
            asset = {
                "id": asset_id,
                "kind": "world.asset",
                "definition_id": "asset.arcane_focus",
                "state": {"owner_actor_id": asset_owner_id},
            }
            context, _repository, _store, _host, _accepted = self._prepare(
                effect_records=(effect,), asset_records=(asset,)
            )
            membership = mechanical_sources.prepare_membership(context)
            self.assertTrue(mechanical_sources.is_membership_issued(membership))
            asset_read = membership.p0_observation.require(
                NativeOwnerRef("world.asset", (asset_id,))
            )
            self.assertIs(asset_read.status, CurrentOwnerStatus.RESOLVED)
            self.assertEqual(
                asset_read.payload["state"]["owner_actor_id"], asset_owner_id
            )
            self.assertEqual(
                [
                    exclusion.reason
                    for exclusion in membership.exclusions
                    if exclusion.owner_ref.identity == (effect["id"],)
                ],
                ["wrong_subject_binding"],
            )

            with self.subTest(asset_owner_id=asset_owner_id):
                if should_hold:
                    with self.assertRaises(NativePreparationHold):
                        spell_cast._require_current_subject_sources(
                            self.cast_source, membership, "actor.mara", context
                        )
                else:
                    spell_cast._require_current_subject_sources(
                        self.cast_source, membership, "actor.mara", context
                    )
                    fresh_context, *_ = self._prepare(
                        effect_records=(effect,), asset_records=(asset,)
                    )
                    prepared = spell_cast._prepare_cast_source_basis(fresh_context)
                    self.assertEqual(
                        prepared.source_basis.value["source_disposition"],
                        "SELECTED_PREPARED_LEVEL1",
                    )

    def test_asset_actor_reference_fields_remain_in_full_membership(self) -> None:
        from GAME.TOOLS import mechanical_sources, spell_cast

        assets = (
            {
                "id": "asset.caster-owned",
                "kind": "world.asset",
                "definition_id": "asset.arcane_focus",
                "state": {"owner_actor_id": "actor.mara"},
            },
            {
                "id": "asset.caster-attuned",
                "kind": "world.asset",
                "definition_id": "asset.arcane_focus",
                "state": {
                    "owner_actor_id": "actor.other",
                    "attuned_actor_id": "actor.mara",
                },
            },
        )
        context, _repository, _store, _host, _accepted = self._prepare(
            asset_records=assets
        )
        prepared = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(
            prepared.source_basis.value["facets"]["equipment"], "NOT_EVALUATED"
        )
        asset_reads = {
            owner.identity[0]
            for owner in prepared.membership.p0_observation.key_union
            if owner.family_key == "world.asset"
        }
        self.assertEqual(asset_reads, {"asset.caster-owned", "asset.caster-attuned"})
        self.assertTrue(mechanical_sources.is_membership_issued(prepared.membership))

    def test_effect_asset_reference_array_reaching_caster_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        asset = {
            "id": "asset.caster-merged",
            "kind": "world.asset",
            "definition_id": "asset.arcane_focus",
            "state": {"owner_actor_id": "actor.mara"},
        }
        conversion = {
            "profile_id": "lifecycle.conversion.true_polymorph_creature_object",
            "principal_subject_id": "actor.other",
            "object_asset_id": "asset.object",
            "activation_occurrence_id": "resolution.convert",
            "binding_generation": 1,
            "restoration_basis_ref": "basis.restore",
            "return_adjudication_basis_ref": "basis.return",
            "phase": "object",
            "lifetime_stage": "concentration",
            "object_experience_scope_ref": "scope.object",
            "merged_asset_ids": ["asset.caster-merged"],
        }
        effect = self._effect_record(
            "effect.merged-caster-asset",
            additional_state={"conversion_state": conversion},
        )
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,), asset_records=(asset,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_owner_revision_actor_reference_in_conversion_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        conversion = {
            "profile_id": "lifecycle.conversion.true_polymorph_creature_object",
            "principal_subject_id": "actor.other",
            "object_asset_id": "asset.object",
            "activation_occurrence_id": "resolution.convert",
            "binding_generation": 1,
            "restoration_basis_ref": "basis.restore",
            "return_adjudication_basis_ref": "basis.return",
            "phase": "object",
            "lifetime_stage": "concentration",
            "object_experience_scope_ref": "scope.object",
            "merged_asset_ids": [],
            "original_body_actor_id": "actor.mara",
            "independent_body_relation_ref": {
                "owner_ref": {
                    "family_key": "world.actor",
                    "identity": ["actor.mara"],
                },
                "source_basis": "actor.revision",
                "generation": 4,
                "fingerprint": "0" * 64,
            },
        }
        effect = self._effect_record(
            "effect.owner-revision-actor-relation",
            additional_state={"conversion_state": conversion},
        )
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def _actor_state(self, **changes: object) -> dict[str, object]:
        from DEV.TESTS.test_sp03_cast_source_contracts import (
            CANTRIP_IDS,
            CANTRIP_SLOT_ID,
            KNOWN_IDS,
            LEVEL1_IDS,
            PREPARED_SLOT_ID,
        )

        cantrips = list(CANTRIP_IDS)
        level1 = list(LEVEL1_IDS)
        state: dict[str, object] = {
            "roles": ["actor.player_character"],
            "abilities": {"ability.charisma": {"base": 16, "adjustment": 0}},
            "resources": {
                "resource.spell_slot.level_1": {"current": 2},
                "resource.innate_sorcery": {"current": 2},
            },
            "build": {
                "species_id": "species.human",
                "background_id": "background.criminal",
                "class_progression": [{"class_id": "class.sorcerer", "level": 1}],
                "choice_bindings": {
                    CANTRIP_SLOT_ID: {
                        "selected_option_ids": [
                            f"option.{identity}" for identity in cantrips
                        ],
                        "selection_basis": "choice_basis.player_explicit",
                    },
                    PREPARED_SLOT_ID: {
                        "selected_option_ids": [
                            f"option.{identity}" for identity in level1
                        ],
                        "selection_basis": "choice_basis.player_explicit",
                    },
                },
                "spellcasting": {
                    "known_spell_ids": sorted(KNOWN_IDS),
                    "prepared_spell_ids": sorted(level1),
                },
            },
        }
        for key, value in changes.items():
            state[key] = value
        return state

    def _prepare(
        self,
        *,
        actor_state: dict[str, object] | None = None,
        effect_records: tuple[dict[str, object], ...] = (),
        asset_records: tuple[dict[str, object], ...] = (),
    ):
        from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
        from DEV.TESTS.test_sp03_native_membership import (
            GitCampaignRepository,
            _write_routed,
        )
        from DEV.TESTS.test_w05_t06_p0_actor_producer import (
            ACTOR_ID,
            _selected_host,
        )
        from GAME.TOOLS.hot_store import NativeHotStore
        from GAME.TOOLS.native_storage import route_native_record
        from GAME.TOOLS.policy_basis import AcceptedAdjudicationBasis
        from GAME.TOOLS.runtime_execution import accept_command

        state = self._actor_state() if actor_state is None else actor_state
        actor = {
            "schema_version": 2,
            "id": ACTOR_ID,
            "kind": "world.actor",
            "definition_id": "actor_archetype.sorcerer",
            "state_revision": 4,
            "state": state,
        }
        temporary = tempfile.TemporaryDirectory(
            prefix="sp03-source-basis-campaign-",
            dir=os.environ["HDM_SP03_SOURCE_BASIS_TEST_SCRATCH"],
        )
        self.addCleanup(temporary.cleanup)
        repository = GitCampaignRepository(Path(temporary.name) / "campaign.git")
        repository.write("MANIFEST.yaml", {"campaign_id": "campaign-frostfall"})
        repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
        repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
        _write_routed(repository, "world.actor", actor)
        for effect in effect_records:
            _write_routed(repository, "world.effect", effect)
        for asset in asset_records:
            _write_routed(repository, "world.asset", asset)
        repository.commit("initial source-basis native owner")
        repository.actor = deepcopy(actor)

        proposal = _proposal(str(self.recipe["id"]))
        proposal["action_request"]["actor_id"] = ACTOR_ID
        proposal["action_request"]["target_ids"] = (
            [ACTOR_ID] if "target" in self.compiled.role_contracts else []
        )
        invocation_facts: list[dict[str, object]] = []
        pending = list(self.recipe["data"].get("steps", ()))
        while pending:
            step = pending.pop()
            if not isinstance(step, dict):
                continue
            arguments = step.get("args")
            if isinstance(arguments, dict):
                raw_facts = arguments.get("applicability_facts", ())
                if isinstance(raw_facts, (list, tuple)):
                    invocation_facts.extend(
                        fact
                        for fact in raw_facts
                        if isinstance(fact, dict)
                        and fact.get("fact_id") == "fiction.target_reachable"
                    )
                child_steps = arguments.get("steps", ())
                if isinstance(child_steps, (list, tuple)):
                    pending.extend(child_steps)
        adjudication_basis = (
            AcceptedAdjudicationBasis(
                parameter_bindings={},
                invocation_facts=tuple(invocation_facts),
                verified_policies=(),
            )
            if invocation_facts
            else None
        )
        acceptance_arguments = (
            {}
            if adjudication_basis is None
            else {"adjudication_basis": adjudication_basis}
        )
        accepted = accept_command(
            _interpreter_result(),
            self.catalog.catalog_context,
            {"definition_id": self.compiled.activity_id, "kind": "definition.activity"},
            proposal,
            **acceptance_arguments,
        )

        resolution = {
            "root_command_id": accepted["command_id"],
            "initiating_command_id": accepted["command_id"],
            "activity_id": self.compiled.activity_id,
            "actor_id": ACTOR_ID,
            "target_ids": accepted["action_request"]["target_ids"],
            "parameter_bindings": accepted["action_request"].get(
                "parameter_bindings", {}
            ),
            "ruleset_set_digest_generation": self.compiled.ruleset_set_digest_generation,
            "ruleset_set_sha256": self.compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": self.compiled.catalog_context_fingerprint_generation,
            "catalog_context_fingerprint": self.compiled.catalog_context_fingerprint,
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": accepted["invocation_facts"],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        repository.write(
            route_native_record(
                "runtime.command", (accepted["command_id"],)
            ).relative_path,
            {"kind": "runtime.command", "id": accepted["command_id"], **accepted},
        )
        repository.write(
            route_native_record(
                "runtime.resolution", (accepted["root_resolution_id"],)
            ).relative_path,
            {
                "kind": "runtime.resolution",
                "id": accepted["root_resolution_id"],
                "campaign_id": "campaign-frostfall",
                **resolution,
            },
        )
        repository.commit("accepted source-basis root inputs")
        store = NativeHotStore(":memory:")
        self.addCleanup(store.close)
        host, _ = _selected_host(store, repository=repository)
        context = host._current_owner._prepare_root_context(
            self.catalog,
            self.compiled,
            command_id=accepted["command_id"],
            consumer_id=self.cast_source.binding.consumer_id,
            adjudication_basis=adjudication_basis,
        )
        return context, repository, store, host, accepted

    def _effect_record(
        self,
        effect_id: str,
        *,
        target_id: str = "actor.other",
        source_id: str = "actor.other",
        additional_state: dict[str, object] | None = None,
    ) -> dict[str, object]:
        state: dict[str, object] = {
            "target_id": target_id,
            "source_id": source_id,
            "lifecycle": {"state_id": "effect_lifecycle.active"},
        }
        if additional_state is not None:
            state.update(additional_state)
        return {
            "schema_version": 2,
            "id": effect_id,
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": state,
        }

    def test_compiler_native_actor_source_basis(self) -> None:
        import copy

        from GAME.TOOLS import activity_contracts, spell_cast
        from GAME.TOOLS.mechanical_context import (
            MechanicalContextError,
            _source_binding_identity,
        )

        context, repository, store, _host, accepted = self._prepare()
        actor_before = deepcopy(repository.actor)
        hot_changes_before = store._connection.total_changes
        result = spell_cast._prepare_cast_source_basis(context)

        self.assertTrue(activity_contracts._preparation_context_is_issued(context))
        self.assertEqual(result.value["source_disposition"], "SELECTED_PREPARED_LEVEL1")
        self.assertEqual(
            result.value["source_spell_id"], self.cast_source.binding.source_spell_id
        )
        acquisition = result.value["acquisition"]
        self.assertEqual(len(acquisition["cantrip_spell_ids"]), 4)
        self.assertEqual(len(acquisition["level1_spell_ids"]), 2)
        self.assertFalse(
            set(acquisition["cantrip_spell_ids"]) & set(acquisition["level1_spell_ids"])
        )
        self.assertEqual(
            set(acquisition["known_spell_ids"]),
            set(acquisition["cantrip_spell_ids"])
            | set(acquisition["level1_spell_ids"]),
        )
        self.assertEqual(
            set(acquisition["prepared_spell_ids"]), set(acquisition["level1_spell_ids"])
        )
        self.assertEqual(result.value["ability_basis"]["base_spell_save_dc"], 13)
        self.assertEqual(result.value["ability_basis"]["base_spell_attack_bonus"], 5)
        self.assertEqual(
            result.value["ability_basis"]["modifier_source_definition_ids"],
            ("effect.innate_sorcery",),
        )
        self.assertEqual(
            result.value["facets"]["final_modifier_closure"], "NOT_EVALUATED"
        )
        self.assertEqual(result.value["facets"]["source_mode"], "NOT_EVALUATED")
        self.assertEqual(result.value["facets"]["form"], "NOT_EVALUATED")
        self.assertEqual(
            set(result.value["activity_closure_ids"]),
            {
                activity_id
                for spell_id in acquisition["known_spell_ids"]
                for activity_id in self.cast_source.definition_contracts[spell_id][
                    "data"
                ]["activity_ids"]
            },
        )
        self.assertEqual(
            result.value["read_refs"], self.cast_source.dependency_read_refs
        )
        self.assertEqual(
            {
                (item["definition_id"], item["kind"])
                for item in result.value["source_definition_refs"]
            },
            {
                (item.definition_id, item.kind)
                for item in self.cast_source.binding.source_definition_refs
            },
        )
        self.assertEqual(result.value["context_facts"], ())
        bound_identity = _source_binding_identity(context.compiled, context.consumer_id)
        cast_identity = tuple(
            row for row in bound_identity if row[0] == "CastSourceBinding"
        )
        self.assertEqual(len(cast_identity), 1)
        self.assertIn(
            ("profile_id", ("str", "execution.spell_cast.srd521")),
            cast_identity[0][1],
        )
        self.assertIn("bound_definition:class.sorcerer", cast_identity[0][9])
        self.assertEqual(
            repository.actor["state"]["build"]["class_progression"],
            [{"class_id": "class.sorcerer", "level": 1}],
        )
        self.assertEqual(repository.actor, actor_before)
        self.assertEqual(store._connection.total_changes, hot_changes_before)
        self.assertEqual(context.resolution["segments"], ())
        self.assertEqual(context.resolution["fixed_rng_results"], ())
        self.assertEqual(accepted["disposition"], "command.accepted")
        with self.assertRaises(MechanicalContextError):
            spell_cast._prepare_cast_source_basis(copy.copy(result))

    def test_selected_source_route_proof(self) -> None:
        from types import MappingProxyType

        from GAME.TOOLS import (
            activity_contracts,
            activity_runtime,
            mechanical_context,
            spell_cast,
        )

        if self.case.get("route_activity_in_package") is not True:
            self.skipTest("actual installed spell Activity route fixture only")
        object.__setattr__(self.catalog, "compiled_activities", MappingProxyType({}))
        self.compiled = activity_runtime.compile_activity(
            self.catalog, str(self.recipe["id"])
        )
        self.cast_source = next(
            row
            for row in self.compiled.cast_source_bindings
            if row.binding.consumer_id.endswith(".step.0")
        )
        context, repository, store, _host, accepted = self._prepare()
        if self.case.get("expected_route") is False:
            with self.assertRaises(activity_contracts.NativePreparationHold):
                spell_cast._prove_selected_source_route(context)
            return

        expected_context_identity = mechanical_context.context_cache_identity(context)
        actor_before = deepcopy(repository.actor)
        repository_revision_before = repository._git("rev-parse", "HEAD").stdout
        hot_changes_before = store._connection.total_changes
        route = spell_cast._prove_selected_source_route(context)
        binding = self.cast_source.binding
        source_spell = self.cast_source.definition_contracts[binding.source_spell_id]
        expected_activity_ids = tuple(source_spell["data"]["activity_ids"])
        self.assertIs(type(route), spell_cast._SelectedCastSourceRouteEvidence)
        self.assertFalse(hasattr(route, "_issue_seal"))
        self.assertTrue(activity_contracts._preparation_context_is_issued(context))
        self.assertEqual(
            accepted["action_request"]["activity_id"], context.compiled.activity_id
        )
        self.assertEqual(
            context.resolution["activity_id"], context.compiled.activity_id
        )
        self.assertEqual(route.activity_id, context.compiled.activity_id)
        self.assertEqual(route.consumer_id, context.consumer_id)
        self.assertEqual(route.source_spell_id, binding.source_spell_id)
        self.assertEqual(route.profile_id, binding.profile_id)
        self.assertEqual(route.profile_generation, binding.profile_generation)
        self.assertEqual(route.source_activity_ids, expected_activity_ids)
        self.assertEqual(route.command_id, context.execution_ref.command_id)
        self.assertEqual(route.root_resolution_id, context.execution_ref.resolution_id)
        self.assertEqual(route.source_read_refs, self.cast_source.dependency_read_refs)
        self.assertEqual(route.source_disposition, self.case["expected_disposition"])
        self.assertEqual(route.source_mode, "NOT_EVALUATED")
        self.assertIsNone(route.mode_id)
        self.assertEqual(
            route.catalog_context_fingerprint,
            context.catalog.catalog_context.fingerprint,
        )
        self.assertEqual(route.context_identity, expected_context_identity)
        self.assertIsInstance(route.membership_identity, tuple)
        self.assertRegex(route.read_fingerprint, r"^[a-f0-9]{64}$")
        self.assertIn(route.activity_id, route.source_activity_ids)

        if context.compiled.activity_id == "activity.spell.magic_missile":
            pending = list(context.compiled.instructions)
            compiled_primitives: list[str] = []
            selected_targets = None
            while pending:
                instruction = pending.pop(0)
                compiled_primitives.append(instruction.primitive_id)
                if instruction.primitive_id == "op.select_targets":
                    selected_targets = instruction
                pending.extend(instruction.children)
            self.assertEqual(
                compiled_primitives,
                [
                    "op.consume_resource",
                    "op.select_targets",
                    "op.for_each_target",
                    "op.apply_damage",
                ],
            )
            self.assertIsNotNone(selected_targets)
            self.assertIn(
                "fact:fiction.target_reachable", selected_targets.read_contract_refs
            )
            fact = selected_targets.arguments["applicability_facts"][0]
            self.assertEqual(fact["fact_id"], "fiction.target_reachable")
            self.assertFalse(fact["value"])
            self.assertEqual(
                tuple(context.accepted_command["invocation_facts"]), (fact,)
            )

        self.assertEqual(
            repository.actor["state"]["abilities"]["ability.charisma"]["base"], 16
        )
        self.assertEqual(repository.actor, actor_before)
        self.assertEqual(
            repository._git("rev-parse", "HEAD").stdout, repository_revision_before
        )
        self.assertEqual(store._connection.total_changes, hot_changes_before)
        self.assertEqual(context.resolution["segments"], ())
        self.assertEqual(context.resolution["fixed_rng_results"], ())

    def _valid_alternative_source_basis(
        self,
        context: object,
        source_basis: object,
    ) -> object:
        from GAME.TOOLS import activity_contracts as contracts

        basis_result = source_basis.source_basis
        value = contracts._thaw(basis_result.value)
        acquisition = value["acquisition"]
        prepared_spell_ids = sorted(("spell.fixture_unselected", "spell.magic_missile"))
        acquisition["level1_spell_ids"] = prepared_spell_ids
        acquisition["prepared_spell_ids"] = prepared_spell_ids
        acquisition["prepared_option_ids"] = [
            f"option.{spell_id}" for spell_id in prepared_spell_ids
        ]
        known_spell_ids = sorted(
            (*acquisition["cantrip_spell_ids"], *prepared_spell_ids)
        )
        acquisition["known_spell_ids"] = known_spell_ids
        value["activity_closure_ids"] = sorted(
            {
                activity_id
                for spell_id in known_spell_ids
                for activity_id in self.cast_source.definition_contracts[spell_id][
                    "data"
                ]["activity_ids"]
            }
        )
        value["source_disposition"] = "SELECTED_PREPARED_LEVEL1"
        value["facets"]["source_spell"] = "RESOLVED"
        return contracts.validate_source_basis_result(value, compiled=context.compiled)

    def _valid_foreign_actor_ability_source_basis(
        self,
        context: object,
        source_basis: object,
    ) -> object:
        from GAME.TOOLS import activity_contracts as contracts

        value = contracts._thaw(source_basis.source_basis.value)
        foreign_actor_ref = {
            "family_key": "world.actor",
            "identity": ["actor.foreign"],
        }
        value["source_actor_ref"] = foreign_actor_ref
        ability = value["ability_basis"]
        ability["base_source_ref"]["source_actor_ref"] = foreign_actor_ref
        ability["base_score"] = 18
        ability["score"] = 18
        ability["modifier"] = 4
        ability["base_spell_save_dc"] = 14
        ability["base_spell_attack_bonus"] = 6
        return contracts.validate_source_basis_result(value, compiled=context.compiled)

    def test_selected_route_does_not_trust_a_valid_alternative_native_basis(
        self,
    ) -> None:
        import copy
        from dataclasses import replace

        from GAME.TOOLS import spell_cast

        if self.case.get("route_activity_in_package") is not True:
            self.skipTest("actual installed spell Activity route fixture only")
        counterfeit_context, _repository, _store, _host, _accepted = self._prepare()
        source_basis = spell_cast._prepare_cast_source_basis(counterfeit_context)
        self.assertEqual(
            source_basis.source_basis.value["source_disposition"], "UNAVAILABLE"
        )
        alternative = self._valid_alternative_source_basis(
            counterfeit_context, source_basis
        )
        self.assertEqual(
            alternative.value["source_disposition"], "SELECTED_PREPARED_LEVEL1"
        )
        replacement = replace(copy.copy(source_basis), source_basis=alternative)

        route_context, _repository, _store, _host, _accepted = self._prepare()
        route = spell_cast._prove_selected_source_route(route_context)
        self.assertEqual(route.source_disposition, "UNAVAILABLE")
        with self.assertRaises(TypeError):
            spell_cast._prove_selected_source_route(route_context, replacement)

    def test_selected_route_rejects_a_caller_supplied_context_identity_prefix(
        self,
    ) -> None:
        from dataclasses import replace

        from GAME.TOOLS import mechanical_context, spell_cast

        if self.case.get("route_activity_in_package") is not True:
            self.skipTest("actual installed spell Activity route fixture only")
        counterfeit_context, _repository, _store, _host, _accepted = self._prepare()
        mechanical_context.context_cache_identity(counterfeit_context)
        source_basis = spell_cast._prepare_cast_source_basis(counterfeit_context)
        counterfeit = replace(
            source_basis,
            cache_identity=(
                ("counterfeit-context-identity",),
                source_basis.cache_identity[1],
            ),
        )

        context, _repository, _store, _host, _accepted = self._prepare()
        expected_identity = mechanical_context.context_cache_identity(context)
        route = spell_cast._prove_selected_source_route(context)

        self.assertEqual(route.context_identity, expected_identity)
        with self.assertRaises(TypeError):
            spell_cast._prove_selected_source_route(context, counterfeit)

    def test_selected_route_does_not_accept_foreign_actor_or_ability_basis_values(
        self,
    ) -> None:
        from dataclasses import replace

        from GAME.TOOLS import spell_cast

        if self.case.get("route_activity_in_package") is not True:
            self.skipTest("actual installed spell Activity route fixture only")
        basis_context, _repository, _store, _host, _accepted = self._prepare()
        source_basis = spell_cast._prepare_cast_source_basis(basis_context)
        self.assertEqual(
            source_basis.source_basis.value["source_disposition"], "UNAVAILABLE"
        )
        foreign_source_basis = self._valid_foreign_actor_ability_source_basis(
            basis_context, source_basis
        )

        route_context, _repository, _store, _host, _accepted = self._prepare()
        route = spell_cast._prove_selected_source_route(route_context)

        self.assertEqual(route.source_disposition, "UNAVAILABLE")
        with self.assertRaises(TypeError):
            spell_cast._prove_selected_source_route(
                route_context,
                replace(source_basis, source_basis=foreign_source_basis),
            )

    def test_selected_source_route_rejects_copied_foreign_and_stale_inputs(
        self,
    ) -> None:
        import copy
        from dataclasses import replace

        from GAME.TOOLS import activity_contracts, spell_cast
        from GAME.TOOLS.mechanical_context import MechanicalContextError
        from GAME.TOOLS.native_storage import route_native_record

        if self.case.get("route_activity_in_package") is not True:
            self.skipTest("actual installed spell Activity route fixture only")
        context, repository, _store, _host, _accepted = self._prepare()

        with self.assertRaises(MechanicalContextError):
            spell_cast._prove_selected_source_route(copy.copy(context))

        replaced_context = replace(context)
        with self.assertRaises(MechanicalContextError):
            spell_cast._prove_selected_source_route(replaced_context)
        replaced_consumer = replace(
            context, consumer_id=f"{context.compiled.activity_id}.step.1"
        )
        with self.assertRaises(MechanicalContextError):
            spell_cast._prove_selected_source_route(replaced_consumer)
        with self.assertRaises(activity_contracts.ActivityContractError):
            replace(context, compiled=copy.copy(context.compiled))
        with self.assertRaises(activity_contracts.ActivityContractError):
            replace(context, catalog=copy.copy(context.catalog))

        mismatched_request = dict(context.accepted_command)
        mismatched_request["action_request"] = dict(
            context.accepted_command["action_request"],
            activity_id="activity.spell.fire_bolt",
        )
        with self.assertRaises(activity_contracts.ActivityContractError):
            replace(context, accepted_command=mismatched_request)
        mismatched_resolution = dict(
            context.resolution, activity_id="activity.spell.fire_bolt"
        )
        with self.assertRaises(activity_contracts.ActivityContractError):
            replace(context, resolution=mismatched_resolution)

        repository.actor["state"]["abilities"]["ability.charisma"]["base"] = 17
        actor_path = route_native_record(
            "world.actor", (repository.actor["id"],)
        ).relative_path
        repository.write(actor_path, repository.actor)
        repository.commit("change Actor after selected-route source basis")
        with self.assertRaises(activity_contracts.NativePreparationHold) as raised:
            spell_cast._prove_selected_source_route(context)
        self.assertEqual(raised.exception.operation_status, "REVALIDATION_REQUIRED")

    def test_only_an_authentic_native_context_is_accepted(self) -> None:
        import copy

        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.mechanical_context import MechanicalContextError

        context, _repository, _store, _host, _accepted = self._prepare()
        with self.assertRaises(MechanicalContextError):
            spell_cast._prepare_cast_source_basis(copy.copy(context))

    def test_compiled_source_node_removal_invalidates_the_issued_context(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.mechanical_context import MechanicalContextError

        context, _repository, _store, _host, _accepted = self._prepare()
        compiled = context.compiled
        original = compiled.cast_source_bindings
        try:
            object.__setattr__(compiled, "cast_source_bindings", ())
            with self.assertRaises(MechanicalContextError):
                spell_cast._prepare_cast_source_basis(context)
        finally:
            object.__setattr__(compiled, "cast_source_bindings", original)

    def test_compiled_source_role_mutation_invalidates_the_issued_context(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.mechanical_context import MechanicalContextError

        context, _repository, _store, _host, _accepted = self._prepare()
        binding = self.cast_source.binding
        original = binding.native_role_bindings
        try:
            object.__setattr__(binding, "native_role_bindings", ())
            with self.assertRaises(MechanicalContextError):
                spell_cast._prepare_cast_source_basis(context)
        finally:
            object.__setattr__(binding, "native_role_bindings", original)

    def test_source_node_role_cannot_be_rebound_to_an_unrelated_actor(self) -> None:
        from dataclasses import replace

        from GAME.TOOLS.current_owner import CurrentOwnerError, NativeOwnerRef

        context, _repository, _store, _host, _accepted = self._prepare()
        foreign = dict(context.role_bindings)
        foreign["actor"] = NativeOwnerRef("world.actor", ("actor.foreign",))
        with self.assertRaises(CurrentOwnerError):
            replace(context, role_bindings=foreign)

    def test_actor_base_and_adjustment_have_native_precedence(self) -> None:
        from GAME.TOOLS import spell_cast

        state = self._actor_state()
        state["abilities"]["ability.charisma"] = {"base": 16, "adjustment": 1}
        context, _repository, _store, _host, _accepted = self._prepare(
            actor_state=state
        )
        result = spell_cast._prepare_cast_source_basis(context)
        ability = result.value["ability_basis"]
        self.assertEqual(ability["base_source"], "ACTOR")
        self.assertEqual(ability["base_score"], 16)
        self.assertEqual(ability["adjustment"], 1)
        self.assertEqual(ability["score"], 17)
        self.assertEqual(ability["base_spell_save_dc"], 13)

        actor_override = self._actor_state()
        actor_override["abilities"]["ability.charisma"] = {
            "base": 15,
            "adjustment": 1,
        }
        actor_context, _repository, _store, _host, _accepted = self._prepare(
            actor_state=actor_override
        )
        actor_result = spell_cast._prepare_cast_source_basis(actor_context)
        self.assertEqual(actor_result.value["ability_basis"]["base_source"], "ACTOR")
        self.assertEqual(actor_result.value["ability_basis"]["score"], 16)
        self.assertEqual(ability["base_spell_attack_bonus"], 5)

    def test_invalid_acquisition_state_fails_closed(self) -> None:
        from GAME.TOOLS import activity_contracts, spell_cast

        states: list[dict[str, object]] = []
        wrong_class = self._actor_state()
        wrong_class["build"]["class_progression"] = [
            {"class_id": "class.fighter", "level": 1}
        ]
        states.append(wrong_class)
        wrong_level = self._actor_state()
        wrong_level["build"]["class_progression"][0]["level"] = 2
        states.append(wrong_level)
        cross_slot_choice = self._actor_state()
        cross_slot_choice["build"]["choice_bindings"][
            "advancement.sorcerer.level_1.prepared_spells"
        ]["selected_option_ids"][0] = "option.spell.fire_bolt"
        states.append(cross_slot_choice)
        omitted_choice = self._actor_state()
        omitted_choice["build"]["choice_bindings"].pop(
            "advancement.sorcerer.level_1.cantrips"
        )
        states.append(omitted_choice)
        extra_choice = self._actor_state()
        extra_choice["build"]["choice_bindings"][
            "advancement.sorcerer.level_1.cantrips"
        ]["selected_option_ids"].append("option.spell.foreign")
        states.append(extra_choice)
        known_conflict = self._actor_state()
        known_conflict["build"]["spellcasting"]["known_spell_ids"].pop()
        states.append(known_conflict)
        prepared_conflict = self._actor_state()
        prepared_conflict["build"]["spellcasting"]["prepared_spell_ids"] = [
            "spell.shield",
            "spell.magic_missile",
        ]
        states.append(prepared_conflict)
        body_form = self._actor_state()
        body_form["embodiment"] = {
            "profile_id": "actor.embodiment.principal",
            "relation_effect_id": "effect.form_relation",
        }
        body_form["life_state_id"] = "life.active"
        body_form["life_state_policy_id"] = "life_policy.spell.magic_jar_principal"
        states.append(body_form)

        for state in states:
            context, _repository, _store, _host, _accepted = self._prepare(
                actor_state=state
            )
            with (
                self.subTest(state=state),
                self.assertRaises(activity_contracts.NativePreparationHold),
            ):
                spell_cast._prepare_cast_source_basis(context)

    def test_missing_native_charisma_source_holds_instead_of_guessing(self) -> None:
        from GAME.TOOLS import activity_contracts, spell_cast

        state = self._actor_state()
        state.pop("abilities")
        context, _repository, _store, _host, _accepted = self._prepare(
            actor_state=state
        )
        with self.assertRaises(activity_contracts.NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_untyped_build_score_is_not_a_native_base_source(self) -> None:
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        state = self._actor_state()
        state["build"]["abilities"] = {"ability.charisma": 30}
        with self.assertRaises(NativePreparationHold):
            self._prepare(actor_state=state)

    def test_stale_native_actor_invalidates_the_source_result(self) -> None:
        from GAME.TOOLS import activity_contracts, spell_cast
        from GAME.TOOLS.native_storage import route_native_record

        context, repository, _store, _host, _accepted = self._prepare()
        repository.actor["state"]["abilities"]["ability.charisma"]["base"] = 17
        repository.actor["state_revision"] += 1
        actor_path = route_native_record(
            "world.actor", (repository.actor["id"],)
        ).relative_path
        repository.write(actor_path, repository.actor)
        repository.commit("change Actor after source context issue")
        with self.assertRaises(activity_contracts.NativePreparationHold) as raised:
            spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(raised.exception.operation_status, "REVALIDATION_REQUIRED")

    def test_selected_cantrip_source_is_resolved(self) -> None:
        if self.cast_source.binding.source_spell_id != "spell.fire_bolt":
            self.skipTest("fixture is not the selected-cantrip case")
        from GAME.TOOLS import spell_cast

        context, _repository, _store, _host, _accepted = self._prepare()
        result = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(result.value["source_disposition"], "SELECTED_KNOWN_CANTRIP")
        self.assertEqual(result.value["facets"]["source_spell"], "RESOLVED")

    def test_legal_unselected_cast_source_is_unavailable(self) -> None:
        if self.cast_source.binding.source_spell_id != "spell.fixture_unselected":
            self.skipTest("fixture is not the legal-unselected case")
        from GAME.TOOLS import spell_cast

        context, _repository, _store, _host, _accepted = self._prepare()
        result = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(result.value["source_disposition"], "UNAVAILABLE")
        self.assertEqual(result.value["facets"]["source_spell"], "UNAVAILABLE")
        self.assertEqual(result.value["facets"]["activity_closure"], "RESOLVED")

    def test_native_selected_options_not_defaults_determine_the_result(self) -> None:
        if self.cast_source.binding.source_spell_id != "spell.fixture_unselected":
            self.skipTest("fixture has no additional legal Sorcerer option")
        from DEV.TESTS.test_sp03_cast_source_contracts import (
            CANTRIP_IDS,
            CANTRIP_SLOT_ID,
            PREPARED_SLOT_ID,
        )
        from GAME.TOOLS import spell_cast

        state = self._actor_state()
        selected_prepared = ("spell.fixture_unselected", "spell.magic_missile")
        state["build"]["choice_bindings"][PREPARED_SLOT_ID]["selected_option_ids"] = [
            f"option.{identity}" for identity in selected_prepared
        ]
        selected_known = sorted((*CANTRIP_IDS, *selected_prepared))
        state["build"]["spellcasting"]["known_spell_ids"] = selected_known
        state["build"]["spellcasting"]["prepared_spell_ids"] = sorted(selected_prepared)
        context, _repository, _store, _host, _accepted = self._prepare(
            actor_state=state
        )
        result = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(result.value["source_disposition"], "SELECTED_PREPARED_LEVEL1")
        self.assertEqual(
            set(result.value["acquisition"]["level1_spell_ids"]),
            set(selected_prepared),
        )
        self.assertEqual(
            result.value["acquisition"]["cantrip_choice_slot_id"], CANTRIP_SLOT_ID
        )

    def test_spell_beyond_sorcerer_one_is_prohibited(self) -> None:
        if self.cast_source.binding.source_spell_id != "spell.fixture_level3":
            self.skipTest("fixture is not the higher-level case")
        from GAME.TOOLS import spell_cast

        context, _repository, _store, _host, _accepted = self._prepare()
        result = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(result.value["source_disposition"], "PROHIBITED")
        self.assertEqual(result.value["facets"]["source_spell"], "PROHIBITED")

    def test_archetype_base_is_used_only_from_the_bound_definition(self) -> None:
        if "actor_archetype.sorcerer" not in self.cast_source.definition_contracts:
            self.skipTest("fixture has no compiler-bound actor archetype")
        from GAME.TOOLS import spell_cast

        state = self._actor_state()
        state.pop("abilities")
        state["abilities"] = {"ability.charisma": {"adjustment": 1}}
        context, _repository, _store, _host, _accepted = self._prepare(
            actor_state=state
        )
        result = spell_cast._prepare_cast_source_basis(context)
        ability = result.value["ability_basis"]
        self.assertEqual(ability["base_source"], "ARCHETYPE")
        self.assertEqual(ability["base_score"], 16)
        self.assertEqual(ability["adjustment"], 1)
        self.assertEqual(ability["score"], 17)
        self.assertEqual(ability["base_spell_save_dc"], 13)

    def test_source_basis_retains_same_operation_native_membership(self) -> None:
        from GAME.TOOLS import mechanical_context, mechanical_sources, spell_cast

        context, _repository, _store, _host, _accepted = self._prepare()
        prepared = spell_cast._prepare_cast_source_basis(context)
        membership = prepared.membership
        self.assertIs(prepared.context, context)
        self.assertIs(membership._context, context)
        self.assertIs(membership._owner_session, context.owner_session)
        self.assertIs(
            membership._operation_token, context.owner_session.operation_token
        )
        self.assertTrue(mechanical_sources.is_membership_issued(membership))
        self.assertTrue(mechanical_sources.revalidate_membership(membership, context))
        self.assertEqual(
            {item.family_key for item in membership.family_coverage},
            {"world.effect", "world.asset"},
        )
        self.assertEqual(
            {item.absent_child for item in membership.family_coverage}, {"RECORDS"}
        )
        self.assertTrue(
            all(
                read.payload is not None
                for read in membership.p0_observation.reads.values()
            )
        )
        expected_membership_identity = mechanical_context._value_identity(
            {
                "activity_id": membership.activity_id,
                "consumer_id": membership.consumer_id,
                "subject_actor_ids": membership.subject_actor_ids,
                "membership": mechanical_context._membership_wire(membership),
                "p0_observation_fingerprint": membership.p0_observation.observation_fingerprint,
            }
        )
        self.assertEqual(prepared.cache_identity[1], expected_membership_identity)
        self.assertEqual(
            prepared.source_basis.value["facets"]["final_modifier_closure"],
            "NOT_EVALUATED",
        )

    def test_active_modifier_effect_is_retained_without_claiming_final_values(
        self,
    ) -> None:
        from GAME.TOOLS import spell_cast

        effect = {
            "schema_version": 2,
            "id": "effect.innate-sorcery-current",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        prepared = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(
            prepared.source_basis.value["facets"]["final_modifier_closure"],
            "NOT_EVALUATED",
        )
        self.assertIn(
            "effect.innate-sorcery-current",
            {item.owner_ref.identity[0] for item in prepared.membership.effects},
        )
        self.assertEqual(
            prepared.source_basis.value["ability_basis"]["base_spell_save_dc"], 13
        )

    def test_effect_form_without_actor_embodiment_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.form-without-actor-embodiment",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "form_state": {
                    "profile_id": "lifecycle.form.polymorph",
                    "form_archetype_id": "actor_archetype.beast",
                    "activation_occurrence_id": "resolution.form",
                    "form_generation": 1,
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_current_control_relation_without_actor_embodiment_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.control-without-actor-embodiment",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "control_state": {
                    "controller_principal_subject_id": "actor.other",
                    "controlled_physical_actor_id": "actor.mara",
                    "command_generation": 1,
                    "phase": "controlled",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_root_target_with_foreign_source_relation_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.root-target-foreign-source-control",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "control_state": {
                    "controller_principal_subject_id": "actor.other",
                    "controlled_physical_actor_id": "actor.mara",
                    "command_generation": 1,
                    "phase": "controlled",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_physical_and_principal_subject_refs_to_caster_hold(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        subject_bindings = (
            {
                "domain": "physical",
                "principal_subject_id": "actor.other",
                "physical_actor_id": "actor.mara",
                "binding_generation": 1,
            },
            {
                "domain": "identity",
                "principal_subject_id": "actor.mara",
                "binding_generation": 1,
            },
        )
        for index, subject_binding in enumerate(subject_bindings):
            effect = {
                "schema_version": 2,
                "id": f"effect.subject-reference-{index}",
                "kind": "world.effect",
                "definition_id": "effect.innate_sorcery",
                "state": {
                    "target_id": "actor.other",
                    "source_id": "actor.other",
                    "lifecycle": {"state_id": "effect_lifecycle.active"},
                    "subject_binding": subject_binding,
                },
            }
            context, _repository, _store, _host, _accepted = self._prepare(
                effect_records=(effect,)
            )
            with (
                self.subTest(subject_binding=subject_binding),
                self.assertRaises(NativePreparationHold),
            ):
                spell_cast._prepare_cast_source_basis(context)

    def test_missing_subject_generation_holds_before_basis_resolution(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.missing-subject-generation",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "subject_binding": {
                    "domain": "physical",
                    "principal_subject_id": "actor.other",
                    "physical_actor_id": "actor.mara",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_conversion_relation_to_caster_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.foreign-conversion-relation",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "conversion_state": {
                    "profile_id": "lifecycle.conversion.animate_objects",
                    "asset_id": "asset.object",
                    "animated_actor_id": "actor.mara",
                    "activation_occurrence_id": "resolution.convert",
                    "phase": "animated",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_foreign_creature_object_original_body_reference_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.foreign-conversion-original-body",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "conversion_state": {
                    "profile_id": "lifecycle.conversion.true_polymorph_creature_object",
                    "principal_subject_id": "actor.other",
                    "object_asset_id": "asset.object",
                    "activation_occurrence_id": "resolution.convert",
                    "binding_generation": 1,
                    "restoration_basis_ref": "basis.restore",
                    "return_adjudication_basis_ref": "basis.return",
                    "phase": "object",
                    "lifetime_stage": "concentration",
                    "object_experience_scope_ref": "scope.object",
                    "merged_asset_ids": [],
                    "original_body_actor_id": "actor.mara",
                    "independent_body_relation_ref": {
                        "owner_ref": {
                            "family_key": "world.actor",
                            "identity": ["actor.mara"],
                        },
                        "source_basis": "campaign-source",
                        "generation": 4,
                        "fingerprint": "a" * 64,
                    },
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_full_effect_universe_relation_to_caster_is_not_filtered_by_target_source(
        self,
    ) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.review-control-nontarget",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "control_state": {
                    "controller_principal_subject_id": "actor.other",
                    "controlled_physical_actor_id": "actor.mara",
                    "command_generation": 1,
                    "phase": "controlled",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_foreign_effect_identity_replica_reference_to_caster_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.review-identity-replica",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "identity_state": {
                    "profile_id": "lifecycle.identity.simulacrum",
                    "relation_generation": 1,
                    "principal_subject_id": "actor.other",
                    "activation_occurrence_id": "resolution.identity",
                    "restoration_policy_id": "restoration.identity",
                    "phase": "active",
                    "replica_actor_id": "actor.mara",
                    "construction_basis_ref": "basis.simulacrum",
                    "creation_occurrence_id": "resolution.simulacrum",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_unrelated_and_ended_relations_do_not_overhold(self) -> None:
        from GAME.TOOLS import spell_cast

        unrelated = {
            "schema_version": 2,
            "id": "effect.unrelated-control",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.other",
                "source_id": "actor.other",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "control_state": {
                    "controller_principal_subject_id": "actor.other",
                    "controlled_physical_actor_id": "actor.other",
                    "command_generation": 1,
                    "phase": "controlled",
                },
            },
        }
        ended = {
            "schema_version": 2,
            "id": "effect.ended-control",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.other",
                "lifecycle": {
                    "state_id": "effect_lifecycle.terminal",
                    "terminal_reason_id": "effect_end.removed",
                },
                "control_state": {
                    "controller_principal_subject_id": "actor.other",
                    "controlled_physical_actor_id": "actor.mara",
                    "command_generation": 1,
                    "phase": "expired",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(unrelated, ended)
        )
        prepared = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(
            prepared.source_basis.value["facets"]["class_progression"], "RESOLVED"
        )

    def test_expired_typed_relations_and_unrelated_sources_do_not_overhold(
        self,
    ) -> None:
        from GAME.TOOLS import spell_cast

        effects = (
            {
                "schema_version": 2,
                "id": "effect.expired-control-relation",
                "kind": "world.effect",
                "definition_id": "effect.innate_sorcery",
                "state": {
                    "target_id": "actor.other",
                    "source_id": "actor.other",
                    "lifecycle": {"state_id": "effect_lifecycle.active"},
                    "control_state": {
                        "controller_principal_subject_id": "actor.other",
                        "controlled_physical_actor_id": "actor.mara",
                        "command_generation": 1,
                        "phase": "expired",
                    },
                },
            },
            {
                "schema_version": 2,
                "id": "effect.ended-simulacrum-relation",
                "kind": "world.effect",
                "definition_id": "effect.innate_sorcery",
                "state": {
                    "target_id": "actor.other",
                    "source_id": "actor.other",
                    "lifecycle": {"state_id": "effect_lifecycle.active"},
                    "identity_state": {
                        "profile_id": "lifecycle.identity.simulacrum",
                        "relation_generation": 1,
                        "principal_subject_id": "actor.other",
                        "activation_occurrence_id": "resolution.identity",
                        "restoration_policy_id": "restoration.identity",
                        "phase": "ended",
                        "replica_actor_id": "actor.mara",
                        "construction_basis_ref": "basis.simulacrum",
                        "creation_occurrence_id": "resolution.simulacrum",
                    },
                },
            },
            {
                "schema_version": 2,
                "id": "effect.reverted-conversion-relation",
                "kind": "world.effect",
                "definition_id": "effect.innate_sorcery",
                "state": {
                    "target_id": "actor.other",
                    "source_id": "actor.other",
                    "lifecycle": {"state_id": "effect_lifecycle.active"},
                    "conversion_state": {
                        "profile_id": "lifecycle.conversion.animate_objects",
                        "asset_id": "asset.object",
                        "animated_actor_id": "actor.mara",
                        "activation_occurrence_id": "resolution.convert",
                        "phase": "reverted",
                    },
                },
            },
        )
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=effects
        )
        prepared = spell_cast._prepare_cast_source_basis(context)
        self.assertEqual(
            prepared.source_basis.value["facets"]["class_progression"], "RESOLVED"
        )

    def test_asset_transform_holds_before_source_basis_resolution(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.innate-sorcery-transform-source",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }
        asset = {
            "id": "asset.transformed-focus",
            "kind": "world.asset",
            "definition_id": "asset.arcane_focus",
            "state": {
                "owner_actor_id": "actor.mara",
                "equipment_transform": {
                    "source_effect_id": "effect.innate-sorcery-transform-source",
                    "transition_occurrence_id": "resolution.transform",
                    "mode": "merged",
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,), asset_records=(asset,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_unqualified_subject_generation_holds_membership(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.stale-subject-generation",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
                "subject_binding": {
                    "domain": "physical",
                    "principal_subject_id": "actor.mara",
                    "physical_actor_id": "actor.mara",
                    "binding_generation": 2,
                },
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_unbound_current_effect_definition_holds_modifier_closure(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        effect = {
            "schema_version": 2,
            "id": "effect.unbound-current-source",
            "kind": "world.effect",
            "definition_id": "effect.unbound_current_source",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }
        context, _repository, _store, _host, _accepted = self._prepare(
            effect_records=(effect,)
        )
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_missing_membership_acquisition_holds(self) -> None:
        from GAME.TOOLS import spell_cast
        from GAME.TOOLS.activity_contracts import NativePreparationHold

        context, repository, _store, _host, _accepted = self._prepare()
        del repository.sp03_git_repository_path
        with self.assertRaises(NativePreparationHold):
            spell_cast._prepare_cast_source_basis(context)

    def test_membership_copy_and_source_add_remove_do_not_retain_currentness(
        self,
    ) -> None:
        import copy

        from DEV.TESTS.test_sp03_native_membership import _write_routed
        from GAME.TOOLS import mechanical_sources, spell_cast
        from GAME.TOOLS.mechanical_sources import MechanicalSourceError
        from GAME.TOOLS.native_storage import route_native_record

        context, repository, _store, host, accepted = self._prepare()
        prepared = spell_cast._prepare_cast_source_basis(context)
        membership = prepared.membership
        with self.assertRaises(MechanicalSourceError):
            mechanical_sources.revalidate_membership(copy.copy(membership), context)

        effect = {
            "schema_version": 2,
            "id": "effect.innate-sorcery-added",
            "kind": "world.effect",
            "definition_id": "effect.innate_sorcery",
            "state": {
                "target_id": "actor.mara",
                "source_id": "actor.mara",
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }
        _write_routed(repository, "world.effect", effect)
        repository.commit("add current source Effect")
        self.assertFalse(mechanical_sources.revalidate_membership(membership, context))

        new_context = host._current_owner._prepare_root_context(
            self.catalog,
            self.compiled,
            command_id=accepted["command_id"],
            consumer_id=self.cast_source.binding.consumer_id,
        )
        new_prepared = spell_cast._prepare_cast_source_basis(new_context)
        self.assertNotEqual(prepared.cache_identity, new_prepared.cache_identity)
        self.assertIn(
            "effect.innate-sorcery-added",
            {item.owner_ref.identity[0] for item in new_prepared.membership.effects},
        )

        effect_path = route_native_record(
            "world.effect", ("effect.innate-sorcery-added",)
        ).relative_path
        (repository.root / effect_path).unlink()
        repository.commit("remove current source Effect")
        self.assertFalse(
            mechanical_sources.revalidate_membership(
                new_prepared.membership, new_context
            )
        )


@pytest.mark.parametrize(
    ("mutation", "test_name"),
    (
        (
            "cast_selected_cantrip",
            "PinnedNativeSourceBasisTests.test_selected_cantrip_source_is_resolved",
        ),
        (
            "unselected_legal_spell",
            "PinnedNativeSourceBasisTests.test_legal_unselected_cast_source_is_unavailable",
        ),
        (
            "unselected_legal_spell",
            "PinnedNativeSourceBasisTests.test_native_selected_options_not_defaults_determine_the_result",
        ),
        (
            "source_prohibited_spell",
            "PinnedNativeSourceBasisTests.test_spell_beyond_sorcerer_one_is_prohibited",
        ),
        (
            "actor_archetype_ability",
            "PinnedNativeSourceBasisTests.test_archetype_base_is_used_only_from_the_bound_definition",
        ),
    ),
)
def test_installed_source_basis_source_statuses(
    conformance_runtime_root: Path,
    tmp_path: Path,
    mutation: str,
    test_name: str,
) -> None:
    from DEV.TESTS.test_sp03_cast_source_contracts import (
        _cold_source_compiler_fixture,
    )

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        mutation=mutation,
        root_roles={"actor": "world.actor", "target": "world.actor"},
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "installed-test",
        test_name=test_name,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_foreign_magic_jar_asset_relation(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_cast_source_contracts import (
        _cold_source_compiler_fixture,
    )

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        mutation="distinct_consumers",
        root_roles={"actor": "world.actor", "target": "world.actor"},
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "installed-magic-jar-test",
        test_name=(
            "PinnedNativeSourceBasisTests."
            "test_foreign_magic_jar_asset_reference_is_relevant_after_binding_exclusion"
        ),
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_compiler_issues_native_sorcerer_source_basis(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_cast_source_contracts import (
        _cold_source_compiler_fixture,
    )

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        mutation="distinct_consumers",
        root_roles={"actor": "world.actor", "target": "world.actor"},
    )
    result = _run_installed_source_basis_case(
        runtime_root, recipe, dependency_kinds, tmp_path / "installed-test"
    )
    assert result.returncode == 0, result.stdout + result.stderr
