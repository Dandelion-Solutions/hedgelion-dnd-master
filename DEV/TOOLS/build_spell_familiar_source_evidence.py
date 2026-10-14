"""Cold, explicit derivation of the accepted R2 Familiar evidence (stdlib only).

Historical inputs are required only to regenerate, never to validate or recover
the durable ledger. This producer carries no gameplay or acceptance authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS_SHA256 = "f3671f452d6d382abdae3f89318da03ac79743ba60bfa0a159c24dafac4eec0d"
PREREQUISITES_SHA256 = (
    "5869ec71cf99487e28c6d0400e3583ceee80daafc300559e9483818c7dd7800f"
)
OUTPUT_PATH = "DEV/TESTS/fixtures/spell-familiar-source-prerequisites.json"
ENTRY_KEYS = frozenset(
    {
        "prerequisite_id",
        "review_register_line",
        "review_root",
        "classification",
        "subject_role",
        "applicable_member_source_keys",
        "source_refs",
        "member_body_refs",
        "predicates_and_outcomes",
        "permitted_conditional_contexts",
        "non_goals",
        "native_consumer_admission_status",
        "attack_relay_classification",
    }
)
CENSUS_KEYS = frozenset(
    {
        "status",
        "pinned_commit",
        "source_path",
        "source_raw_sha256",
        "hash_basis",
        "domain_bounds",
        "index_span",
        "domain_spans",
        "coverage",
        "spell_body",
        "records",
        "support_clauses",
        "fixture_route_file",
        "source_key_boundary",
        "named_spell_examples",
        "additional_qualifying_forms",
        "negative_partitions",
        "source_manifest",
        "candidate_revision",
        "prerequisite_source_clauses",
        "source_prerequisite_ledger",
        "prior_review",
    }
)
PREREQUISITE_KEYS = frozenset(
    {
        "candidate_revision",
        "classification",
        "pinned_commit",
        "review_path",
        "review_sha256",
        "scope",
        "terminal_boundary",
        "general_nonattack_action_count",
        "general_nonattack_actions",
        "source_prerequisite_records",
        "entries",
        "parameterized_inputs",
        "finding_dispositions",
        "native_consumer_edges",
        "native_consumer_admission_status",
        "independent_R2_review",
    }
)


def closed_object(value: object, keys: set[str] | frozenset[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"closed shape differs: {label}")
    return value


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode_json(data: bytes) -> dict:
    value = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_pairs)
    if not isinstance(value, dict):
        raise TypeError("JSON root shape must be an object")
    return value


def load_accepted_input(path: Path, expected_sha256: str) -> dict:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        raise ValueError(f"accepted input identity differs: {path}")
    return decode_json(data)


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def reference_tuples(entries: list[dict]) -> list[list]:
    return [
        [
            entry["prerequisite_id"],
            ref["collection"],
            ref.get("index"),
            ref["line_start"],
            ref["line_end"],
            ref["raw_utf8_sha256"],
        ]
        for entry in entries
        for ref in entry["source_refs"]
    ]


def build_prerequisites(census: dict, prerequisites: dict) -> dict:
    closed_object(census, CENSUS_KEYS, "accepted census")
    closed_object(prerequisites, PREREQUISITE_KEYS, "accepted prerequisites")
    if census["source_prerequisite_ledger"] != prerequisites:
        raise ValueError("accepted census/ledger equality differs")
    if (
        census["candidate_revision"] != "R2"
        or prerequisites["candidate_revision"] != "R2"
    ):
        raise ValueError("accepted R2 revision differs")
    entries = prerequisites["entries"]
    for entry in entries:
        closed_object(entry, ENTRY_KEYS, "prerequisite entry")
        for ref in entry["source_refs"]:
            keys = {
                "kind",
                "collection",
                "source_path",
                "line_start",
                "line_end",
                "raw_utf8_sha256",
            }
            if ref["collection"] != "spell_body":
                keys.add("index")
            closed_object(ref, keys, "source reference")
        for ref in entry["member_body_refs"]:
            closed_object(ref, {"source_key", "record_index", "span"}, "member join")
            closed_object(
                ref["span"],
                {"line_start", "line_end", "raw_utf8_sha256"},
                "member span",
            )
    rows = reference_tuples(entries)
    clauses = [
        [r["source_key"], r["line_start"], r["line_end"], r["raw_utf8_sha256"]]
        for r in prerequisites["source_prerequisite_records"]
    ]
    if (
        len(entries),
        len(rows),
        sum(len(e["member_body_refs"]) for e in entries),
        len(clauses),
    ) != (37, 151, 673, 33):
        raise ValueError("accepted item completeness differs")
    # Preserve all root semantics verbatim, including applicability and exclusions.
    return {
        "artifact_kind": "SP00_FIND_FAMILIAR_SOURCE_PREREQUISITES",
        "candidate_revision": "R2",
        "pinned_commit": prerequisites["pinned_commit"],
        "source_identity_owner": {
            "path": census["source_path"],
            "identity_fixture_path": "DEV/TESTS/fixtures/spell-familiar-source-census.json",
        },
        "accepted_input": {
            "path": "/tmp/hdm-dev/spell-recovery/SP00-familiar-prerequisites-20261014.json",
            "sha256": PREREQUISITES_SHA256,
            "r2_manifest_sha256": "44d8c10b03f1e3276bf11ad0fc0f29dd9761d91decbcfaf7010fb50a3a51f0c7",
            "independent_r2_review_sha256": "bd878a6746e71705db8d2d7c0947cb2ed8239086a93d932a275832e57d6a6405",
        },
        "classification": prerequisites["classification"],
        "source_reference_tuple_sha256": canonical_sha256(rows),
        "new_source_clause_tuple_sha256": canonical_sha256(clauses),
        "completeness": {
            "review_register_root_count": len(entries),
            "source_reference_count": len(rows),
            "new_source_clause_count": len(clauses),
            "parameterized_input_category_count": len(
                prerequisites["parameterized_inputs"]
            ),
            "general_nonattack_action_count": prerequisites[
                "general_nonattack_action_count"
            ],
        },
        "review_register_roots": [
            [
                e["prerequisite_id"],
                e["review_register_line"],
                e["classification"],
                len(e["source_refs"]),
            ]
            for e in entries
        ],
        "entries": entries,
        "source_reference_tuples": rows,
        "parameterized_inputs": prerequisites["parameterized_inputs"],
        "accepted_scope": prerequisites["scope"],
        "accepted_terminal_boundary": prerequisites["terminal_boundary"],
        "finding_dispositions": prerequisites["finding_dispositions"],
        "general_nonattack_actions": prerequisites["general_nonattack_actions"],
        "new_source_clauses": clauses,
        "parameterized_input_categories": [
            [r["input_id"], r["required_by"]]
            for r in prerequisites["parameterized_inputs"]
        ],
        "help_first_aid": {
            "stabilization_source_key": "source.srd521.prerequisite.help.stabilize",
            "stabilization_target_hp": 0,
            "stabilization_check": "DC 10 Wisdom (Medicine)",
            "medicine_proficiency_required": False,
            "stable_remains_unconscious": True,
            "knockout_first_aid_source_key": "source.srd521.prerequisite.help.knockout_first_aid",
            "knockout_first_aid_uses_action": True,
            "knockout_creation_requires_melee_attack": True,
            "knockout_creation_granted_to_familiar": False,
            "familiar_at_zero_hp": "DISAPPEARS; NO_ON_SCENE_STABILIZATION_OVERRIDE",
        },
        "source_boundary": {
            "terminal_boundary": "Finite shared source clauses for the registered roots; actual selected spells, grants, objects/tasks, incoming effects and environmental states remain parameterized inputs.",
            "native_dependency_graph": "NOT_ESTABLISHED",
            "native_consumer_admission": "NOT_ESTABLISHED",
            "touch_spell_attack_save_statistic_classification": "NOT_DECIDED_HERE",
            "form_hands_voice_language_proficiency_spellcasting_defaults": "NONE",
            "general_action_labels_create_executor_entitlement": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", required=True, type=Path)
    parser.add_argument("--prerequisites", required=True, type=Path)
    parser.add_argument(
        "--check", action="store_true", help="compare generated bytes without writing"
    )
    args = parser.parse_args()
    payload = build_prerequisites(
        load_accepted_input(args.census, CENSUS_SHA256),
        load_accepted_input(args.prerequisites, PREREQUISITES_SHA256),
    )
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target = ROOT / OUTPUT_PATH
    if args.check:
        if target.read_bytes() != data:
            raise ValueError("derived fixture drift")
    else:
        target.write_bytes(data)
    print(
        f"{OUTPUT_PATH}: 37 roots, 151 references, 673 member joins; sha256={hashlib.sha256(data).hexdigest()}"
    )


if __name__ == "__main__":
    main()
