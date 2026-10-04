"""Reproduce design-only requirement routing; never compile or activate spells.

Input paths are explicit. The published input is checked after LF normalization;
the official-text extraction and independent full-body reviews remain qualified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT.parent / "hdm_srd_spell_research"
SOURCE_SHA = "05576261665280c3f424d791c19d8c4080343c6a"
INPUT_SHA = "cd894d28ef8693352c2a80c01e062a058358ef3734ff6f813e42c934fb84e4c3"
INPUT_PATH = "DEV/docs/superpowers/research/2026-10-04-spell-coverage/spell-inventory.json"

GROUP_ROUTES = {
    "DAMAGE": ["SP-05", "SP-06", "SP-07", "SP-12"],
    "HEALTH": ["SP-05", "SP-06", "SP-07", "SP-08", "SP-12"],
    "EFFECT": ["SP-05", "SP-06", "SP-08", "SP-12"],
    "ZONE": ["SP-05", "SP-06", "SP-08", "SP-09", "SP-12", "SP-16"],
    "MOVEMENT": ["SP-05", "SP-06", "SP-09"],
    "TRANSFORM": ["SP-05", "SP-06", "SP-08", "SP-10"],
    "SUMMON": ["SP-05", "SP-06", "SP-08", "SP-10", "SP-16"],
    "WORLD": ["SP-05", "SP-06", "SP-09", "SP-10"],
    "INFORMATION": ["SP-05", "SP-06", "SP-11"],
    "ILLUSION": ["SP-05", "SP-06", "SP-08", "SP-11"],
    "CONTROL": ["SP-05", "SP-06", "SP-08", "SP-11"],
    "COUNTER": ["SP-05", "SP-06", "SP-07", "SP-08", "SP-12"],
    "SPECIAL": ["SP-05", "SP-06", "SP-07", "SP-08", "SP-13"],
}
EXACT_ROUTES = {
    "Wish": ["SP-10", "SP-11", "SP-12", "SP-13", "SP-14"],
    "Time Stop": ["SP-09", "SP-13"],
    "Magic Jar": ["SP-10", "SP-11", "SP-22"],
    "Clone": ["SP-10", "SP-11", "SP-22"],
    "Astral Projection": ["SP-09", "SP-10", "SP-11", "SP-22"],
    "Glyph of Warding": ["SP-09", "SP-13"],
    "Contingency": ["SP-13"],
    "Teleport": ["SP-21"],
    "Prismatic Spray": ["SP-21"],
    "Reincarnate": ["SP-21"],
}

def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def rows_from_review(doc: object) -> list[dict]:
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for key in ("rows", "spells", "entries", "reviews", "spell_reviews"):
            if isinstance(doc.get(key), list):
                return doc[key]
    raise ValueError("Independent review has no recognized row list")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, help="Pinned research spell-inventory.json")
    parser.add_argument("--extracted-sources", type=Path, help="Optional original extraction to recheck body witnesses")
    args = parser.parse_args()
    inventory_path = args.inventory
    if inventory_path is None:
        inventory_path = next((p / INPUT_PATH for p in ROOT.parents if (p / INPUT_PATH).is_file()), RESEARCH / "spell-inventory.json")
    text = inventory_path.read_text(encoding="utf-8")
    assert sha(text) == INPUT_SHA, "Input differs from fresh Connector-read source"
    inventory = json.loads(text)
    witness_path = ROOT / "source-body-witnesses.json"
    if args.extracted_sources is not None:
        raw_text = args.extracted_sources.read_text(encoding="utf-8")
        raw = json.loads(raw_text)
        witness = {"status": "FROZEN_EXTRACTION_WITNESS_NOT_CANONICAL_RULE_TEXT",
                   "source": "https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf",
                   "extraction_lf_utf8_sha256": sha(raw_text),
                   "qualification": "Hash covers the exact extracted span, including recorded contamination/tail qualifiers. Reproduction from witnesses does not reverify primary text or recipe semantics.",
                   "rows": [{"name": row["name"], "level": row["level"], "page": row["page"], "line": row["line"], "body_sha256": sha(row["body"])} for row in raw]}
        witness_path.write_text(json.dumps(witness, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    else:
        witness = json.loads(witness_path.read_text(encoding="utf-8"))
    source_by_name = {row["name"]: row for row in witness["rows"]}
    assert len(source_by_name) == len(witness["rows"]) == 339
    reviews: dict[str, dict] = {}
    review_manifest = []
    for suffix, expected in (("0-2", 141), ("3-5", 114), ("6-9", 84)):
        path = ROOT / f"source-pass-{suffix}.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        selected = rows_from_review(doc)
        assert len(selected) == expected, (path.name, len(selected))
        for row in selected:
            name = row.get("source_exact_name", row.get("name", row.get("spell", row.get("spell_name"))))
            assert isinstance(name, str) and name in source_by_name, (path.name, name)
            assert name not in reviews, name
            assert row["body_sha256"] == source_by_name[name]["body_sha256"], (path.name, name, "body hash mismatch")
            # The independently authored fields and qualifiers survive unchanged.
            reviews[name] = {"row": row, "artifact": path.name}
        review_manifest.append({"artifact": path.name, "entries": expected,
                                "utf8_sha256": sha(path.read_text(encoding="utf-8")),
                                "qualification": "Full extracted-body design review; not licensed-source recipe verification"})
    assert set(reviews) == set(source_by_name)
    rows = []
    for item in inventory["spells"]:
        name = item["name"]
        source = source_by_name[name]
        routes = set(GROUP_ROUTES[item["primary_group"]]) | set(EXACT_ROUTES.get(name, []))
        if item["primary_group"] in {"HEALTH", "EFFECT", "ZONE", "SUMMON", "SPECIAL", "CONTROL"}:
            routes.update({"SP-23", "SP-24"})
        for tag in item["tags"]:
            if any(word in tag for word in ("concentration", "duration", "recurring", "trigger", "repeat", "long-lived", "persistence", "permanen")):
                routes.add("SP-08")
            if any(word in tag for word in ("area", "target", "object", "travel", "plane", "portal", "sense", "fall")):
                routes.add("SP-09")
            if any(word in tag for word in ("material", "component", "ritual", "long-cast", "upcast", "bonus-action", "reaction")):
                routes.add("SP-05")
            if any(word in tag for word in ("agency", "belief", "knowledge", "information", "epistemic", "disclosure", "communication", "sensor", "language")):
                routes.add("SP-11")
            if any(word in tag for word in ("reaction", "counter", "suppression", "intercept", "dispel", "defense")):
                routes.add("SP-12")
            if any(word in tag for word in ("form", "statblock", "identity", "equipment", "summon", "resurrection", "restoration")):
                routes.add("SP-10")
            if "composed" in tag or "triggered-cast" in tag:
                routes.add("SP-13")
        review = reviews[name]["row"]
        reviewed_routes = review.get("candidate_routes", review.get("routes", []))
        for route in reviewed_routes if isinstance(reviewed_routes, list) else []:
            if isinstance(route, str) and route.startswith("SP-"):
                routes.add(route)
        rows.append({
            "name": name, "level": item["level"], "source_page": item["source_page"],
            "research_group": item["primary_group"],
            "research_evidence_ref": {"artifact": INPUT_PATH, "exact_name": name},
            "extracted_body_sha256": source["body_sha256"],
            "architecture_routes": sorted(routes, key=lambda value: int(value[3:])),
            "independent_full_body_review_ref": {"artifact": reviews[name]["artifact"], "exact_name": name},
            "common_contracts_ref": "document.common_contracts",
            "architecture_disposition": "NEEDS_PO_SP14_FOR_ROLL_REDO" if name == "Wish" else "ROUTED_CANDIDATE",
            "rule_mode_recipe_proof": "NOT_PERFORMED_BY_DESIGN_ROUTING",
            "machine_admission": "UNCHANGED_EXACT_BASELINE_ONLY",
            "production_support": "NOT_ESTABLISHED_BY_THIS_DESIGN",
            "required_proof": "source/mode equality + dependency/admission/consumer equality + native execution/recovery/eligible receipt + target performance",
        })
    assert len(rows) == len({row["name"] for row in rows}) == 339
    assert {row["name"] for row in rows} == set(reviews)
    levels = Counter(row["level"] for row in rows)
    assert dict(levels) == {0:27, 1:57, 2:57, 3:42, 4:34, 5:38, 6:31, 7:20, 8:17, 9:16}
    doc = {"status": "ARCHITECTURE_REQUIREMENT_ROUTING_CANDIDATE_NOT_SUPPORT_ADMISSION",
           "source_ref": "v1/engine-rearchitecture", "source_commit": SOURCE_SHA,
           "research_input": INPUT_PATH, "research_lf_normalized_utf8_sha256": INPUT_SHA,
           "source_body_witness": {"artifact": witness_path.name, "lf_utf8_sha256": sha(witness_path.read_text(encoding="utf-8"))},
           "source_review_manifest": review_manifest,
           "item_evidence_rule": "Research evidence and every independent row, mode, negative evidence, confidence and qualifier remain authoritative only within their stated evidence role in the exact linked artifact, qualified by this manifest hash. Compact references remove duplicate payload, not item semantics.",
           "common_contracts": ["SP-01", "SP-02", "SP-03", "SP-04", "SP-07", "SP-15", "SP-16", "SP-17", "SP-18", "SP-19", "SP-20"],
           "required_attribution": inventory["required_attribution"],
           "coverage_limits": ["339 unique entry routing, every extracted body independently read",
                               "Mode count is not a tag count; exact source/mode requirement equality awaits recipe materialization",
                               "Source-parser contamination/table/tail qualifications retained per referenced row; verified Unicode signs are not corruption",
                               "Full spell support does not mean full class acquisition; Wish SP14 remains decision-gated"],
           "counts": {"entries":339, "reviewed_extracted_bodies":339, "by_level":dict(sorted(levels.items())),
                      "by_group":dict(sorted(Counter(row["research_group"] for row in rows).items()))},
           "spells": rows}
    (ROOT / "requirement-matrix.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (ROOT / "requirement-matrix.csv").open("w", encoding="utf-8", newline="") as stream:
        columns = ["name", "level", "source_page", "research_group", "architecture_routes", "architecture_disposition", "rule_mode_recipe_proof", "production_support"]
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: " | ".join(row[key]) if isinstance(row[key], list) else row[key] for key in columns})
    print(json.dumps({"entries":339, "reviewed_bodies":339, "input_source_equal":True,
                      "primary_extraction_rechecked": args.extracted_sources is not None,
                      "json_lf_utf8_sha256": sha((ROOT/"requirement-matrix.json").read_text(encoding="utf-8"))}))

if __name__ == "__main__":
    main()
