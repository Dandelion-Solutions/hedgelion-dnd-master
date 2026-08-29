#!/usr/bin/env python3
"""Apply a pre-verified Documentation Corpus Refactor migration to a checkout.

The applier does not discover policy.  It consumes an already-proven migration
map plus explicit line-scoped repair decisions, validates the entire operation
first, then mutates the checkout in one deterministic phase.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

EXTRACTION_START = "# 3. Current first-party ChatGPT evidence"
EXTRACTION_END = "# 4. Preliminary assurance disposition matrix"


def _extract_r015(source_path: str, text: str) -> str:
    start = text.find(EXTRACTION_START)
    end = text.find(EXTRACTION_END)
    if start < 0 or end < 0 or end <= start:
        raise ValueError("R-015 H1-H8 extraction boundaries not found")
    section = text[start:end].rstrip() + "\n"
    return (
        "# ChatGPT Plus Host Evidence — Extracted R2.6 Research Evidence\n\n"
        "Status: **RESEARCH EVIDENCE — NON-NORMATIVE**\n\n"
        f"SPLIT_FROM: `{source_path}`\n\n"
        "SEMANTIC_SOURCE_RANGE: `# 3. Current first-party ChatGPT evidence` — H1 through H8, ending before section 4.\n\n"
        "CURRENT_AUTHORITY: NONE — EVIDENCE ONLY\n\n"
        "This extraction preserves the point-in-time host evidence and its qualifications. "
        "Implementation-facing R2.6 law remains in the current canonical owners.\n\n"
        "---\n\n"
        + section
    )


def _prepare_repaired_texts(root: Path, repairs: list[dict]) -> dict[str, str]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in repairs:
        grouped[str(row["source_path"])].append(row)

    prepared: dict[str, str] = {}
    for source_path in sorted(grouped):
        path = root / source_path
        if not path.is_file():
            raise ValueError(f"repair source missing: {source_path}")
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        for row in sorted(
            grouped[source_path],
            key=lambda item: (int(item["line"]), str(item["old_literal"]), str(item["new_literal"])),
        ):
            line_number = int(row["line"])
            if line_number < 1 or line_number > len(lines):
                raise ValueError(f"repair line out of range: {source_path}:{line_number}")
            old = str(row["old_literal"])
            new = str(row["new_literal"])
            line = lines[line_number - 1]
            if old not in line:
                raise ValueError(
                    f"repair literal missing: {source_path}:{line_number}: {old!r}"
                )
            lines[line_number - 1] = line.replace(old, new, 1)
        prepared[source_path] = "".join(lines)
    return prepared


def apply_migration(root: Path | str, *, migration: dict, repairs: list[dict]) -> dict:
    root = Path(root).resolve()

    move_rows = sorted(
        (row for row in migration.get("rows", []) if row.get("action") == "MOVE"),
        key=lambda row: str(row["old_path"]),
    )
    extractions = list(migration.get("extractions", []))

    # Phase 1: validate and prepare every mutation before touching the checkout.
    repaired_texts = _prepare_repaired_texts(root, repairs)

    for row in move_rows:
        old_path = str(row["old_path"])
        destination_path = str(row["destination_path"])
        source = root / old_path
        destination = root / destination_path
        if not source.is_file():
            raise ValueError(f"move source missing: {old_path}")
        if destination.exists():
            raise ValueError(f"move destination already exists: {destination_path}")

    prepared_extractions: list[tuple[str, str]] = []
    for row in extractions:
        source_id = str(row["source_id"])
        source_path = str(row["source_path"])
        destination_path = str(row["destination_path"])
        source = root / source_path
        destination = root / destination_path
        if source_id != "R-015":
            raise ValueError(f"unsupported extraction source: {source_id}")
        if not source.is_file():
            raise ValueError(f"extraction source missing: {source_path}")
        if destination.exists():
            raise ValueError(f"extraction destination already exists: {destination_path}")
        original_text = source.read_text(encoding="utf-8")
        prepared_extractions.append(
            (destination_path, _extract_r015(source_path, original_text))
        )

    # Phase 2: deterministic mutation after complete validation.
    for source_path in sorted(repaired_texts):
        (root / source_path).write_text(repaired_texts[source_path], encoding="utf-8")

    for row in move_rows:
        source = root / str(row["old_path"])
        destination = root / str(row["destination_path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.replace(destination)

    for destination_path, content in prepared_extractions:
        destination = root / destination_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    return {
        "move_count": len(move_rows),
        "repair_count": len(repairs),
        "extraction_count": len(prepared_extractions),
    }
