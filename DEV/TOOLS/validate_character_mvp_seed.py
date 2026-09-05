"""Fail-closed S6D-07 package compiler/readiness/advancement conformance tool."""

from copy import deepcopy
import json
from pathlib import Path
import re
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from DEV.TOOLS.validate_ruleset_package_closure import build_resolved_lock


CHARACTER_KINDS = {
    "definition.species", "definition.background", "definition.class",
    "definition.advancement", "definition.feat", "definition.feature", "definition.spell",
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_primitive_argument(primitive_catalog, primitive_id, argument_name, value):
    contract = next(row for row in primitive_catalog["contracts"] if row["primitive_id"] == primitive_id)
    if argument_name not in contract["arguments"]:
        raise ValueError("unknown primitive argument")
    value_kind = contract["arguments"][argument_name]["value_kind"]
    value_contract = primitive_catalog["value_contracts"][value_kind]
    if "enum" in value_contract and value not in value_contract["enum"]:
        raise ValueError(f"argument {argument_name} violates {value_kind}")
    return True


def create_innate_sorcery_effect_candidate(actor_id, causing_idempotency_key, local_chronology_id, existing=None):
    existing = existing if existing is not None else {}
    replay_key = (actor_id, causing_idempotency_key)
    if replay_key in existing:
        return existing[replay_key]
    instance_key = (actor_id, actor_id, "effect.innate_sorcery")
    candidate = {
        "instance_key": instance_key,
        "definition_id": "effect.innate_sorcery",
        "target_actor_id": actor_id,
        "source_actor_id": actor_id,
        "temporal_binding": {
            "start_owner": "CAUSING_EXECUTION_SEGMENT_COMMIT",
            "local_chronology_id": local_chronology_id,
            "duration": {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.minute"},
        },
        "reapplication": "ATOMIC_REPLACE_SAME_INSTANCE_KEY",
        "expiry": "IDEMPOTENT_TEMPORAL_AGENDA_TRANSITION",
    }
    existing[replay_key] = candidate
    return candidate


class SchemaViolation(ValueError):
    pass


class CanonicalSchemaValidator:
    """Small fail-closed Draft-2020-12 subset used by the conformance compiler.

    It resolves the repository's real schema IDs/$refs and implements every
    assertion keyword used by the definition schemas exercised by this seed.
    Unsupported assertion keywords fail rather than being silently ignored.
    """

    def __init__(self, schema_dir):
        self.schemas = {}
        for path in Path(schema_dir).glob("*.schema.json"):
            schema = load_json(path)
            if "$id" in schema:
                self.schemas[schema["$id"]] = schema

    @staticmethod
    def _type_matches(value, expected):
        types = expected if isinstance(expected, list) else [expected]
        checks = {
            "object": lambda: isinstance(value, dict), "array": lambda: isinstance(value, list),
            "string": lambda: isinstance(value, str), "boolean": lambda: isinstance(value, bool),
            "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
            "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
            "null": lambda: value is None,
        }
        return any(checks[k]() for k in types)

    def _resolve(self, ref, root):
        if ref.startswith("#/"):
            node = root
            for token in ref[2:].split("/"):
                node = node[token.replace("~1", "/").replace("~0", "~")]
            return node, root
        base, _, fragment = ref.partition("#")
        if base not in self.schemas:
            raise SchemaViolation(f"unresolved canonical $ref {ref}")
        target = self.schemas[base]
        if fragment:
            node = target
            for token in fragment.lstrip("/").split("/"):
                node = node[token.replace("~1", "/").replace("~0", "~")]
            return node, target
        return target, target

    def validate(self, value, schema, root=None, path="$", probe=False):
        root = root or schema
        try:
            if "$ref" in schema:
                target, target_root = self._resolve(schema["$ref"], root)
                self.validate(value, target, target_root, path)
            for sub in schema.get("allOf", []): self.validate(value, sub, root, path)
            if "anyOf" in schema and not any(self.validate(value, sub, root, path, True) for sub in schema["anyOf"]):
                raise SchemaViolation(f"{path}: no anyOf branch matched")
            if "oneOf" in schema and sum(bool(self.validate(value, sub, root, path, True)) for sub in schema["oneOf"]) != 1:
                raise SchemaViolation(f"{path}: expected exactly one oneOf branch")
            if "if" in schema:
                branch = "then" if self.validate(value, schema["if"], root, path, True) else "else"
                if branch in schema: self.validate(value, schema[branch], root, path)
            if "not" in schema and self.validate(value, schema["not"], root, path, True):
                raise SchemaViolation(f"{path}: forbidden schema matched")
            if "type" in schema and not self._type_matches(value, schema["type"]): raise SchemaViolation(f"{path}: wrong type")
            if "const" in schema and value != schema["const"]: raise SchemaViolation(f"{path}: const mismatch")
            if "enum" in schema and value not in schema["enum"]: raise SchemaViolation(f"{path}: enum mismatch")
            if isinstance(value, dict):
                missing = set(schema.get("required", [])) - set(value)
                if missing: raise SchemaViolation(f"{path}: missing {sorted(missing)}")
                for trigger, dependencies in schema.get("dependentRequired", {}).items():
                    if trigger in value:
                        dependency_missing = set(dependencies) - set(value)
                        if dependency_missing: raise SchemaViolation(f"{path}: {trigger} requires {sorted(dependency_missing)}")
                props = schema.get("properties", {})
                if schema.get("additionalProperties") is False:
                    extra = set(value) - set(props)
                    if extra: raise SchemaViolation(f"{path}: additional properties {sorted(extra)}")
                for key, item in value.items():
                    if key in props: self.validate(item, props[key], root, f"{path}.{key}")
                    elif isinstance(schema.get("additionalProperties"), dict):
                        self.validate(item, schema["additionalProperties"], root, f"{path}.{key}")
                    if "propertyNames" in schema: self.validate(key, schema["propertyNames"], root, f"{path}.<key>")
                if len(value) < schema.get("minProperties", 0): raise SchemaViolation(f"{path}: too few properties")
                if "maxProperties" in schema and len(value) > schema["maxProperties"]: raise SchemaViolation(f"{path}: too many properties")
            if isinstance(value, list):
                if len(value) < schema.get("minItems", 0): raise SchemaViolation(f"{path}: too few items")
                if "maxItems" in schema and len(value) > schema["maxItems"]: raise SchemaViolation(f"{path}: too many items")
                if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value): raise SchemaViolation(f"{path}: duplicate items")
                if "items" in schema:
                    for index, item in enumerate(value): self.validate(item, schema["items"], root, f"{path}[{index}]")
                if "contains" in schema:
                    count = sum(bool(self.validate(item, schema["contains"], root, path, True)) for item in value)
                    if count < schema.get("minContains", 1) or count > schema.get("maxContains", len(value)): raise SchemaViolation(f"{path}: contains cardinality")
            if isinstance(value, str):
                if len(value) < schema.get("minLength", 0): raise SchemaViolation(f"{path}: string too short")
                if "pattern" in schema and not re.search(schema["pattern"], value): raise SchemaViolation(f"{path}: pattern mismatch")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                if "minimum" in schema and value < schema["minimum"]: raise SchemaViolation(f"{path}: below minimum")
                if "maximum" in schema and value > schema["maximum"]: raise SchemaViolation(f"{path}: above maximum")
                if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]: raise SchemaViolation(f"{path}: below exclusive minimum")
            return True
        except (SchemaViolation, KeyError):
            if probe: return False
            raise


def resolve_package(package_dir, primitive_catalog):
    package_dir = Path(package_dir)
    capability = load_json(package_dir / "character-capabilities.json")
    manifest = load_json(package_dir / "ruleset-package-manifest.json")
    lock, _ = build_resolved_lock(
        [package_dir], root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    seed = load_json(package_dir / "character-mvp-seed.json")
    if seed["profile_id"] != capability["profile_id"]:
        raise ValueError("profile identity mismatch")

    gameplay_path = package_dir / "gameplay-spine-seed.json"
    gameplay_seed = load_json(gameplay_path) if gameplay_path.exists() else {"activity_definitions": []}
    gameplay_activities = gameplay_seed["activity_definitions"]
    records = seed["definitions"] + seed["support_definitions"] + seed["activity_definitions"] + gameplay_activities
    ids = [record["id"] for record in records]
    value_ids = seed["value_registrations"]
    if len(ids) != len(set(ids)) or len(value_ids) != len(set(value_ids)):
        raise ValueError("duplicate catalog identity")
    resolved = {}
    validator = CanonicalSchemaValidator(Path(__file__).resolve().parents[1] / "SCHEMAS")
    catalog_schema_id = "https://hedgelion.invalid/schemas/catalog-definition.schema.json"
    if catalog_schema_id not in validator.schemas:
        raise ValueError("canonical catalog definition schema unavailable")
    for record in records:
        if "data" not in record:
            raise ValueError(f"definition data missing for {record['id']}")
        envelope = {"id": record["id"], "kind": record["kind"], "name": {"en": record["id"]}, "data": deepcopy(record["data"])}
        if record.get("choice_slots"):
            if record["kind"] == "definition.advancement":
                first_level = envelope["data"]["levels"][0]
                first_level["choice_slots"] = deepcopy(record["choice_slots"])
            else:
                envelope["data"]["choice_slots"] = deepcopy(record["choice_slots"])
        validator.validate(envelope, validator.schemas[catalog_schema_id])
        resolved[record["id"]] = envelope
    admitted = set(resolved) | set(value_ids)
    base_record_ids = {record["id"] for record in seed["definitions"] + seed["support_definitions"] + seed["activity_definitions"]}
    if set(seed["external_dependency_ids"]) != (base_record_ids | set(value_ids)) - {record["id"] for record in seed["definitions"]}:
        raise ValueError("external dependency inventory mismatch")
    for record in seed["definitions"]:
        if record["kind"] not in CHARACTER_KINDS:
            raise ValueError("unsupported character definition kind")
        for ref in record.get("references", []):
            if ref not in admitted:
                raise ValueError(f"unresolved reference {ref}")
        data = resolved[record["id"]]["data"]
        if record["kind"] == "definition.species" and not {"size_options", "speed"} <= set(data):
            raise ValueError("species schema requirements missing")
        if record["kind"] == "definition.class" and not {"hit_die", "advancement_id"} <= set(data):
            raise ValueError("class schema requirements missing")
        if record["kind"] == "definition.advancement" and "levels" not in data:
            raise ValueError("advancement schema requirements missing")
        if record["kind"] == "definition.spell" and not {"level", "school_id", "activity_ids"} <= set(data):
            raise ValueError("spell schema requirements missing")

    contracts = {row["primitive_id"]: row for row in primitive_catalog["contracts"]}
    actual_consumers = {}
    outcome_enums = {
        "check_outcome": {"success", "failure"}, "save_outcome": {"success", "failure"},
        "attack_outcome": {"miss", "hit", "critical"},
    }
    def compile_steps(steps, activity_id, available_exports=None, depth=0):
        if depth > 3:
            raise ValueError("compiled step nesting exceeds bound")
        available_exports = dict(available_exports or {})
        previous_results = {}
        for step in steps:
            contract = contracts.get(step["op"])
            if not contract or contract["realization_state"] != "COMPLETE" or contract["selection_state"] != "ACTIVE_ADMITTED":
                raise ValueError(f"nonselectable primitive {step['op']}")
            supplied = set(step.get("args", {}))
            if supplied - set(contract["arguments"]):
                raise ValueError("unknown primitive argument")
            required = {name for name, spec in contract["arguments"].items() if spec["required"]}
            if not required <= supplied:
                raise ValueError("missing primitive argument")
            for argument_name, argument in step.get("args", {}).items():
                validate_primitive_argument(primitive_catalog, step["op"], argument_name, argument)
                if isinstance(argument, str) and "." in argument:
                    export, member = argument.split(".", 1)
                    result_contract = previous_results if export == "result" else available_exports.get(export)
                    if result_contract is not None and member not in result_contract:
                        raise ValueError(f"unknown result member {argument}")
            actual_consumers.setdefault(step["op"], set()).add(activity_id)
            if step["op"] == "op.for_each_target":
                target_export = step["args"]["targets"]
                if target_export not in available_exports:
                    raise ValueError("for_each targets must reference prior export")
                child_steps = step["args"]["steps"]
                if not isinstance(child_steps, list) or not child_steps:
                    raise ValueError("for_each child steps missing")
                nested_exports = dict(available_exports)
                nested_exports["$target"] = {"entity_ref": {"value_kind": "entity_ref"}}
                compile_steps(child_steps, activity_id, nested_exports, depth + 1)
            if "when" in step:
                condition = step["when"]
                result_ref = condition.get("result")
                if not result_ref or "." not in result_ref:
                    raise ValueError("typed result condition missing")
                export, member = result_ref.split(".", 1)
                result_contract = available_exports.get(export)
                if not result_contract or member not in result_contract:
                    raise ValueError(f"unresolved condition result {result_ref}")
                allowed = outcome_enums.get(result_contract[member]["value_kind"])
                if allowed is not None and not set(condition.get("in", [])) <= allowed:
                    raise ValueError(f"illegal condition enum for {result_ref}")
            if step.get("export"):
                if step["export"] in available_exports:
                    raise ValueError("duplicate Activity export")
                available_exports[step["export"]] = contract["results"]
            previous_results = contract["results"]
        return available_exports

    for record in seed["activity_definitions"] + gameplay_activities:
        if record["kind"] != "definition.activity" or not record["data"].get("steps"):
            raise ValueError("invalid Activity definition")
        compile_steps(record["data"]["steps"], record["id"])
    for primitive_id, consumers in actual_consumers.items():
        if set(contracts[primitive_id]["exact_seed_consumer_ids"]) != consumers:
            raise ValueError(f"primitive consumer closure mismatch for {primitive_id}: catalog={sorted(contracts[primitive_id]['exact_seed_consumer_ids'])} actual={sorted(consumers)}")
    return {
        "capability": capability,
        "manifest": manifest,
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "seed": seed,
        "gameplay_seed": gameplay_seed,
        "resolved_catalog": resolved,
        "value_ids": set(value_ids),
    }


def evaluate_ready_pc(actor, resolved_package, evidence=None):
    seed = resolved_package["seed"]
    build = actor.get("build", {})
    progression = build.get("class_progression", [])
    blockers = []
    if not build.get("species_id") or not build.get("background_id") or len(progression) != 1:
        blockers.append("actor_build_anchors")
        return {"ready": False, "blockers": blockers, "provisional_gameplay_allowed": True}
    class_id = progression[0]["class_id"]
    evidence = evidence or {}
    manifest = resolved_package["manifest"]
    required_provenance = {"assets": "ASSET_STATE", "proficiencies": "RESOLVED_DEFINITION_GRANTS", "selectors": "MECHANICAL_CONTEXT", "activities": "CATALOG_ADMISSION_LEDGER"}
    if evidence.get("actor_id") != actor.get("id") or evidence.get("actor_state_revision") != actor.get("state_revision"):
        blockers.append("readiness_actor_identity_or_revision")
    if (
        evidence.get("catalog_generation") != manifest["catalog_generation"]
        or evidence.get("ruleset_set_digest_generation") != resolved_package["ruleset_set_digest_generation"]
        or evidence.get("ruleset_set_sha256") != resolved_package["ruleset_set_sha256"]
    ):
        blockers.append("readiness_catalog_identity")
    if evidence.get("provenance") != required_provenance:
        blockers.append("readiness_evidence_provenance")
    required = {"species.human.size", "species.human.origin_feat"}
    required.add("advancement.fighter.level_1.style" if class_id == "class.fighter" else "advancement.sorcerer.level_1.spells")
    bindings = build.get("choice_bindings", {})
    blockers.extend(sorted(required - set(bindings)))
    if "hp" not in actor or "life_state_id" not in actor:
        blockers.append("derived_health_and_life_state")
    required_assets = {"asset.shortbow", "asset.thieves_tools"} if class_id == "class.fighter" else {"asset.arcane_focus", "asset.thieves_tools"}
    if required_assets != set(evidence.get("owned_asset_definition_ids", [])) or not required_assets <= set(resolved_package["resolved_catalog"]):
        blockers.append("owned_assets")
    background_proficiencies = set(resolved_package["resolved_catalog"][build["background_id"]]["data"].get("proficiency_ids", []))
    class_proficiencies = {ref for ref in resolved_package["seed"]["definitions"][[x["id"] for x in resolved_package["seed"]["definitions"]].index(class_id)].get("references", []) if ref.startswith("proficiency.")}
    required_proficiencies = background_proficiencies | class_proficiencies
    if required_proficiencies != set(evidence.get("derived_proficiency_ids", [])):
        blockers.append("derived_proficiencies")
    dexterity = actor.get("abilities", {}).get("ability.dexterity", {}).get("base")
    expected_defense = 10 + ((dexterity - 10) // 2) if isinstance(dexterity, int) else None
    if evidence.get("selector_results", {}).get("defense.armor_class") != expected_defense:
        blockers.append("derived_defense")
    if class_id == "class.sorcerer":
        selected = set(build.get("spellcasting", {}).get("known_spell_ids", []))
        advancement = resolved_package["resolved_catalog"]["advancement.sorcerer.mvp_1"]
        granted = set(advancement["data"]["levels"][0]["choice_slots"][0]["options"][0]["grant_definition_ids"])
        if selected != granted:
            blockers.append("spell_selection_binding_mismatch")
        required_activities = {resolved_package["resolved_catalog"][spell_id]["data"]["activity_ids"][0] for spell_id in granted}
        required_activities.add("activity.feature.innate_sorcery")
        if required_activities != set(evidence.get("admitted_activity_ids", [])) or not required_activities <= set(resolved_package["resolved_catalog"]):
            blockers.append("admitted_spell_activities")
        if "spell.dc" not in evidence.get("selector_results", {}):
            blockers.append("derived_spell_dc")
        charisma = actor.get("abilities", {}).get("ability.charisma", {}).get("base")
        expected_dc = 10 + ((charisma - 10) // 2) if isinstance(charisma, int) else None
        if evidence.get("selector_results", {}).get("spell.dc") != expected_dc:
            blockers.append("derived_spell_dc")
        required_resources = {"resource.spell_slot.level_1", "resource.innate_sorcery"}
    else:
        required_activities = {"activity.attack.ranged_weapon", "activity.feature.resourceful", "activity.feature.second_wind"}
        if required_activities != set(evidence.get("admitted_activity_ids", [])) or not required_activities <= set(resolved_package["resolved_catalog"]):
            blockers.append("admitted_martial_activities")
        required_resources = {"resource.second_wind"}
    if not required_resources <= set(actor.get("resources", {})) or not required_resources <= set(resolved_package["resolved_catalog"]):
        blockers.append("owned_resources")
    return {"ready": not blockers, "blockers": blockers, "provisional_gameplay_allowed": True}


def advance_fighter_to_level_2(actor, command_id, idempotency_key, existing_receipts=None):
    existing_receipts = existing_receipts if existing_receipts is not None else {}
    if idempotency_key in existing_receipts:
        return existing_receipts[idempotency_key]
    before = actor["build"]["class_progression"][0]
    if before != {"class_id": "class.fighter", "level": 1}:
        raise ValueError("advancement prerequisite mismatch")
    after = deepcopy(actor)
    after["build"]["class_progression"][0]["level"] = 2
    after.setdefault("resources", {})["resource.action_surge"] = {"current": 1}
    receipt = {
        "command_id": command_id,
        "idempotency_key": idempotency_key,
        "after_actor": after,
        "execution_segment": {"disposition": "COMMITTED", "transition_kind": "transition.actor_state"},
        "mechanical_event": {"kind": "event.character.advanced"},
        "receipt": {"outcome": "COMPLETED", "evidence": ["feature.fighter.action_surge", "feature.fighter.tactical_mind"]},
        "continuation": None,
    }
    existing_receipts[idempotency_key] = receipt
    return receipt
