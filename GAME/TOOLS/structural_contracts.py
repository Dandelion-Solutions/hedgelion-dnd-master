"""Pure structural validation of the installed assertion-only ABI projection.

No source admission, native reads, execution, truth issuance or DEV access.
Unsupported assertion keywords fail closed. Successful composition branches
retain property annotations for draft-2020-12 unevaluatedProperties closure.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path

# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION = "1.0.2"


class StructuralContractError(ValueError):
    """A value does not match an exact installed structural contract."""


@lru_cache(maxsize=1)
def _projection():
    value = json.loads(Path(__file__).with_name("activity_contract_shapes.json").read_text(encoding="utf-8"))
    if set(value) != {"schema_version", "schemas", "named", "primitive_arguments"} or type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise StructuralContractError("unsupported structural projection")
    return value


def _equal(left, right):
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return set(left) == set(right) and all(_equal(left[key], right[key]) for key in left)
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(_equal(a, b) for a, b in zip(left, right, strict=True))
    return left == right


def _resolve(ref, root):
    base, _, fragment = ref.partition("#")
    target = root if not base else _projection()["schemas"].get(base)
    if target is None:
        raise StructuralContractError(f"unavailable installed contract reference: {ref}")
    node = target
    for part in fragment.lstrip("/").split("/") if fragment else ():
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node, target


_KEYWORDS = frozenset({"$id", "$schema", "$defs", "$ref", "type", "const", "enum", "allOf", "anyOf", "oneOf", "if", "then", "else", "not",
    "properties", "patternProperties", "additionalProperties", "unevaluatedProperties", "required", "dependentRequired", "dependentSchemas", "propertyNames", "minProperties", "maxProperties",
    "items", "prefixItems", "contains", "minContains", "maxContains", "minItems", "maxItems", "uniqueItems", "minLength", "maxLength", "pattern", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"})


def _validate(value, schema, root):
    if schema is False:
        raise StructuralContractError("forbidden contract branch")
    if schema is True:
        return set()
    if set(schema) - _KEYWORDS:
        raise StructuralContractError("unsupported structural assertion")
    evaluated = set()
    if "$ref" in schema:
        target, target_root = _resolve(schema["$ref"], root)
        evaluated |= _validate(value, target, target_root)
    for sub in schema.get("allOf", ()):
        evaluated |= _validate(value, sub, root)
    for keyword in ("anyOf", "oneOf"):
        if keyword in schema:
            successes = []
            for sub in schema[keyword]:
                try:
                    successes.append(_validate(value, sub, root))
                except StructuralContractError:
                    pass
            if not successes or keyword == "oneOf" and len(successes) != 1:
                raise StructuralContractError("closed union does not match")
            for keys in successes:
                evaluated |= keys
    if "if" in schema:
        try:
            conditional = _validate(value, schema["if"], root)
        except StructuralContractError:
            branch = "else"
        else:
            evaluated |= conditional
            branch = "then"
        if branch in schema:
            evaluated |= _validate(value, schema[branch], root)
    if "not" in schema:
        try:
            _validate(value, schema["not"], root)
        except StructuralContractError:
            pass
        else:
            raise StructuralContractError("forbidden matching branch")
    kinds = schema.get("type")
    if kinds is not None:
        kinds = (kinds,) if isinstance(kinds, str) else kinds
        matches = {"object": isinstance(value, Mapping), "array": isinstance(value, (tuple, list)), "string": isinstance(value, str),
                   "integer": type(value) is int, "number": type(value) in (int, float), "boolean": type(value) is bool, "null": value is None}
        if not any(matches.get(kind, False) for kind in kinds):
            raise StructuralContractError("wrong structural scalar/container type")
    if "const" in schema and not _equal(value, schema["const"]):
        raise StructuralContractError("wrong constant")
    if "enum" in schema and not any(_equal(value, option) for option in schema["enum"]):
        raise StructuralContractError("unknown structural enum")
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value) or set(schema.get("required", ())) - set(value):
            raise StructuralContractError("missing/invalid object keys")
        for key, required in schema.get("dependentRequired", {}).items():
            if key in value and set(required) - set(value):
                raise StructuralContractError("missing conditional members")
        for key, sub in schema.get("dependentSchemas", {}).items():
            if key in value:
                evaluated |= _validate(value, sub, root)
        properties = schema.get("properties", {})
        matched = set()
        for key, item in value.items():
            if key in properties:
                _validate(item, properties[key], root)
                matched.add(key)
            for pattern, sub in schema.get("patternProperties", {}).items():
                if re.search(pattern, key):
                    _validate(item, sub, root)
                    matched.add(key)
            if "propertyNames" in schema:
                _validate(key, schema["propertyNames"], root)
        if "additionalProperties" in schema:
            for key in set(value) - matched:
                _validate(value[key], schema["additionalProperties"], root)
            matched |= set(value)
        evaluated |= matched
        if "unevaluatedProperties" in schema:
            for key in set(value) - evaluated:
                _validate(value[key], schema["unevaluatedProperties"], root)
            evaluated |= set(value)
        if len(value) < schema.get("minProperties", 0) or len(value) > schema.get("maxProperties", len(value)):
            raise StructuralContractError("object cardinality")
    if isinstance(value, (list, tuple)):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", len(value)):
            raise StructuralContractError("array cardinality")
        if schema.get("uniqueItems") and any(_equal(item, prior) for index, item in enumerate(value) for prior in value[:index]):
            raise StructuralContractError("duplicate array member")
        prefix = schema.get("prefixItems", ())
        for index, sub in enumerate(prefix):
            if index < len(value):
                _validate(value[index], sub, root)
        if "items" in schema:
            for item in value[len(prefix):]:
                _validate(item, schema["items"], root)
        if "contains" in schema:
            count = 0
            for item in value:
                try:
                    _validate(item, schema["contains"], root)
                    count += 1
                except StructuralContractError:
                    pass
            if count < schema.get("minContains", 1) or count > schema.get("maxContains", len(value)):
                raise StructuralContractError("contains cardinality")
    if isinstance(value, str) and (len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", len(value)) or "pattern" in schema and re.search(schema["pattern"], value) is None):
        raise StructuralContractError("string shape")
    if type(value) in (int, float):
        if isinstance(value, float) and not math.isfinite(value):
            raise StructuralContractError("nonfinite scalar")
        for key, compare in (("minimum", lambda a, b: a >= b), ("maximum", lambda a, b: a <= b), ("exclusiveMinimum", lambda a, b: a > b), ("exclusiveMaximum", lambda a, b: a < b)):
            if key in schema and not compare(value, schema[key]):
                raise StructuralContractError("numeric bound")
        if "multipleOf" in schema and value % schema["multipleOf"] != 0:
            raise StructuralContractError("numeric multiple")
    return evaluated


def validate_contract(name: str, value: object) -> None:
    projection = _projection()
    if name in projection["named"]:
        schema = projection["named"][name]
        root = schema
    elif name.startswith("arguments:"):
        schema = projection["primitive_arguments"].get(name.removeprefix("arguments:"))
        if schema is None:
            raise StructuralContractError("unknown primitive contract")
        root = schema
    else:
        ref = name if name.startswith("https://") else "https://hedgelion.invalid/schemas/" + name + ".schema.json"
        schema, root = _resolve(ref, {})
    _validate(value, schema, root)
