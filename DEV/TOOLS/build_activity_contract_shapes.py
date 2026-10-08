"""Build the runtime structural projection; never admission or rule content.

Owning DEV schemas/catalog contracts remain the maintenance sources. The
installed ABI reads only this deterministic assertion-only GAME projection.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV/TOOLS"))
from activity_primitive_contracts import load_activity_primitive_contracts

DESTINATION = ROOT / "GAME/TOOLS/activity_contract_shapes.json"
BASE = "https://hedgelion.invalid/schemas/"
COMPILED_VALUES = BASE + "compiled-activity-values.schema.json"
ROOTS = ("spell-native-profile-values", "mechanical-surfaces", "runtime-command-state", "runtime-resolution-state",
         "resolution-receipt", "execution-segment", "activity-parameter-spec", "catalog-definition",
         "roll-result", "activity-primitive-values", "runtime-mechanical-event-state",
          "runtime-procedure-state", "runtime-continuation-state", "activity-compiler-declaration")
ID = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_.:-]*$"}
SCALAR = {"type": ["string", "number", "boolean"]}


def assertions(value):
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in {"description", "title", "$comment", "examples", "default"}:
            continue
        if key in {"properties", "patternProperties", "$defs", "dependentSchemas"}:
            result[key] = {name: assertions(schema) for name, schema in item.items()}
        elif key in {"allOf", "anyOf", "oneOf", "prefixItems"}:
            result[key] = [assertions(schema) for schema in item]
        elif key in {"additionalProperties", "unevaluatedProperties", "propertyNames", "items", "contains", "if", "then", "else", "not"}:
            result[key] = assertions(item)
        else:
            result[key] = item
    return result


def build_projection(root=ROOT):
    schemas = {}
    pending = list(ROOTS)
    catalog = load_activity_primitive_contracts(root)
    registries = json.loads((root / "DEV/CATALOG/core-catalog.json").read_text())["registries"]

    def reference(ref):
        if ref.startswith("DEV/SCHEMAS/"):
            ref = BASE + ref.removeprefix("DEV/SCHEMAS/")
        elif not ref.startswith("https://"):
            ref = BASE + ref
        if ref.split("#")[0] != COMPILED_VALUES:
            pending.append(ref.split("#")[0].removeprefix(BASE).removesuffix(".schema.json"))
        return {"$ref": ref}

    def value_shape(kind):
        contract = catalog["value_contracts"][kind]
        if "schema_ref" in contract:
            return reference(contract["schema_ref"])
        if "enum" in contract:
            return {"enum": contract["enum"]}
        if "type" in contract:
            return {"type": contract["type"]}
        if "catalog_ref" in contract:
            registry = contract["catalog_ref"]
            return {"enum": registries[registry]} if registry in registries else ID
        compiler = contract.get("compiler_ref")
        known = {
            "stable_target_source_definition_tuple": {"type": "array", "minItems": 3, "maxItems": 3, "items": ID},
            "bounded_compiled_activity_steps": {"type": "array", "minItems": 1, "items": reference(COMPILED_VALUES + "#/$defs/step")},
            "bounded_ordered_typed_result_list": {"type": "array", "items": {"anyOf": [ID, reference(COMPILED_VALUES + "#/$defs/typedResult")]}},
            "typed_prior_export_symbol": {"type": "string", "pattern": "^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)*$"},
        }
        if compiler not in known:
            raise ValueError(f"unclosed value contract: {kind}")
        return known[compiler]

    value_shapes = {kind: value_shape(kind) for kind in catalog["value_contracts"]}
    argument_shapes = {}
    for row in catalog["contracts"]:
        props, required = {}, []
        for name, spec in row["arguments"].items():
            kind = spec["value_kind"]
            shape = value_shapes[kind]
            if spec["cardinality"] == "many":
                shape = {"type": "array", "items": shape}
            refs = [{"type": "object", "additionalProperties": False,
                     "required": [key, "value_kind"],
                      "properties": {key: {"type": "string", "pattern": "^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)*(?::[a-z][a-z0-9_]*)?$" if key == "symbol_ref" else "^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)*$"},
                                     "value_kind": {"const": kind}}}
                     for key in ("export_ref", "parameter_ref", "scope_ref", "symbol_ref")]
            props[name] = {"anyOf": [shape, *refs]}
            if spec["required"]:
                required.append(name)
        argument_shapes[row["primitive_id"]] = {"type": "object", "additionalProperties": False,
                                                "required": required, "properties": props}

    while pending:
        name = pending.pop()
        identifier = BASE + name + ".schema.json"
        if identifier in schemas:
            continue
        schema = assertions(json.loads((root / f"DEV/SCHEMAS/{name}.schema.json").read_text()))
        schemas[identifier] = schema
        def visit(node):
            if isinstance(node, dict):
                ref = node.get("$ref", "")
                if ref and not ref.startswith("#"):
                    node["$ref"] = reference(ref)["$ref"]
                for child in node.values():
                    visit(child)
            elif isinstance(node, list):
                for child in node:
                    visit(child)
        visit(schema)

    value_descriptor = {"type": "object", "additionalProperties": False,
                        "required": ["value_kind", "cardinality", "required", "source"],
                        "properties": {"value_kind": {"enum": sorted(catalog["value_contracts"])},
                                       "cardinality": {"enum": ["single", "many"]}, "required": {"type": "boolean"},
                                       "source": {"const": "PRIMITIVE_RESULT"}}}
    scope_binding = {"type": "object", "additionalProperties": False,
                     "required": ["source_export", "value_kind"],
                      "properties": {"source_export": ID,
                                     "value_kind": {"enum": sorted(catalog["value_contracts"])},
                                     "family_key": {"enum": ["world.actor", "world.asset", "runtime.procedure"]}}}
    named = {
        "calculation_policy_binding": reference(BASE + "spell-native-profile-values.schema.json#/$defs/calculationPolicyBinding"),
        "roll_policy_result": reference(BASE + "spell-native-profile-values.schema.json#/$defs/rollPolicyResult"),
        "cast_profile_binding": reference(BASE + "spell-native-profile-values.schema.json#/$defs/castProfileBinding"),
        "cast_preflight_input": reference(BASE + "spell-native-profile-values.schema.json#/$defs/castPreflightInput"),
        "compiled_calculation_policy": reference(BASE + "spell-native-profile-values.schema.json#/$defs/compiledCalculationPolicy"),
        "compiler_context_fact_metadata": reference(BASE + "spell-native-profile-values.schema.json#/$defs/compilerContextFactMetadata"),
        "definition_dependency_graph": {"type": "object", "propertyNames": ID,
            "additionalProperties": {"type": "array", "uniqueItems": True, "items": ID}},
        "compiler_symbol_contracts": {"type": "object", "additionalProperties": reference(BASE + "activity-compiler-declaration.schema.json#/$defs/symbol")},
        "capability_card": {"type": "object", "additionalProperties": False,
            "required": ["definition_id", "name", "summary", "activity_ids"], "properties": {
                "definition_id": ID, "name": {"type": "object", "minProperties": 1, "additionalProperties": {"type": "string", "minLength": 1}},
                "summary": {"type": "string", "minLength": 1}, "activity_ids": {"type": "array", "uniqueItems": True, "items": ID}}},
        "exports": {"type": "object", "propertyNames": ID, "additionalProperties": SCALAR},
        "typed_export_value": {"oneOf": [{"type": "object", "additionalProperties": False,
            "required": ["value_kind", "value"], "properties": {"value_kind": {"const": kind}, "value": value_shapes[kind]}}
            for kind in sorted(catalog["value_contracts"])]},
        "parameters": {"type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"},
                       "additionalProperties": {"$ref": BASE + "activity-parameter-spec.schema.json"}},
        "roles": {"type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"},
                  "additionalProperties": {"type": "object", "additionalProperties": False,
                    "required": ["family_key", "required"], "properties": {
                        "family_key": schemas[BASE + "spell-native-profile-values.schema.json"]["$defs"]["ownerRef"]["properties"]["family_key"],
                        "required": {"type": "boolean"}, "subject_domain": {"enum": ["physical", "mental", "identity", "object"]}}}},
        "export_contracts": {"type": "object", "propertyNames": ID, "additionalProperties": {
            "type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"}, "minProperties": 1,
            "additionalProperties": value_descriptor}},
        "compiled_instruction": {"$ref": COMPILED_VALUES + "#/$defs/instruction"},
        "activity_unavailable_reasons": {
            "type": "object", "propertyNames": ID,
            "additionalProperties": {"type": "string", "minLength": 1},
        },
        "native_execution_envelope": {
            "type": "object", "additionalProperties": False,
            "required": ["accepted_command_id", "accepted_input_fingerprint", "execution_owner_id",
                         "resolution_id", "status", "segment", "event", "event_id", "receipt", "resolution"],
            "properties": {
                "accepted_command_id": ID,
                "accepted_input_fingerprint": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "execution_owner_id": ID,
                "resolution_id": ID,
                "status": schemas[BASE + "runtime-resolution-state.schema.json"]["properties"]["status"],
                "segment": reference(BASE + "execution-segment.schema.json"),
                "event": reference(BASE + "runtime-mechanical-event-state.schema.json"),
                "event_id": ID,
                "receipt": reference(BASE + "resolution-receipt.schema.json"),
                "resolution": reference(BASE + "runtime-resolution-state.schema.json"),
                "roll_result": reference(BASE + "roll-result.schema.json"),
                "procedure_state": reference(BASE + "runtime-procedure-state.schema.json"),
                "continuation_state": reference(BASE + "runtime-continuation-state.schema.json"),
            },
        },
    }
    named["fragment_exports"] = {"type": "object", "propertyNames": ID,
        "additionalProperties": {"anyOf": [SCALAR, named["typed_export_value"]]}}
    instruction_shape = {
        "type": "object", "additionalProperties": False,
        "required": ["consumer_id", "primitive_id", "arguments", "result_contract_refs",
                     "read_contract_refs", "children", "guard", "result_contracts", "scope_bindings", "export_name"],
        "properties": {
            "consumer_id": ID,
            "primitive_id": {"enum": sorted(argument_shapes)},
            "arguments": {"type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"}},
            "result_contract_refs": {"type": "array", "items": ID},
            "read_contract_refs": {"type": "array", "items": ID},
            "children": {"type": "array", "items": {"$ref": "#/$defs/instruction"}},
            "guard": {"anyOf": [{"type": "null"},
                                 reference(BASE + "activity-definition-data.schema.json#/$defs/step/properties/when")]},
            "result_contracts": {"type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"},
                                 "additionalProperties": value_descriptor},
            "scope_bindings": {"type": "object", "propertyNames": {"pattern": "^[a-z][a-z0-9_]*$"},
                               "additionalProperties": scope_binding},
            "export_name": {"anyOf": [{"type": "null"}, {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"}]},
        },
        "allOf": [
            {"if": {"properties": {"primitive_id": {"const": operation}}, "required": ["primitive_id"]},
             "then": {"properties": {"arguments": {
                 **arguments, "properties": {
                     name: {"type": "array", "minItems": 1, "items": ID}
                     if catalog_row["arguments"][name]["value_kind"] == "compiled_step_list" else shape
                     for name, shape in arguments["properties"].items()
                 }}}}}
            for catalog_row in catalog["contracts"]
            for operation, arguments in [(catalog_row["primitive_id"], argument_shapes[catalog_row["primitive_id"]])]
        ],
    }
    schemas[COMPILED_VALUES] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": COMPILED_VALUES,
        "$defs": {"typedResult": named["typed_export_value"], "instruction": instruction_shape, "step": {
            "allOf": [{"$ref": BASE + "activity-definition-data.schema.json#/$defs/step"},
                      {"properties": {"op": {"enum": sorted(argument_shapes)}}}],
            "dependentSchemas": {"op": {"allOf": [
                {"if": {"properties": {"op": {"const": operation}}}, "then": {
                    "required": ["args"] if arguments["required"] else [], "properties": {"args": arguments}}}
                for operation, arguments in argument_shapes.items()]}}}}}
    # Named contracts must use the same explicitly closed schema projection;
    # references cannot silently add a root after the closure pass.
    if any(BASE + name + ".schema.json" not in schemas for name in pending):
        raise ValueError("result contract introduced an unjoined schema root")
    return {"schema_version": 1, "schemas": schemas, "named": named, "primitive_arguments": argument_shapes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(build_projection(), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not DESTINATION.is_file() or DESTINATION.read_text(encoding="utf-8") != encoded:
            raise SystemExit("runtime structural projection differs from owning sources")
    else:
        DESTINATION.write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
