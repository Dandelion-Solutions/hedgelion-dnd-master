#!/usr/bin/env python3
"""Derive the Documentation Corpus Refactor migration map from durable census owners."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DESIGN_DIR = Path("DEV/docs/superpowers/design")
RESEARCH_CENSUS = DESIGN_DIR / "2026-08-29-documentation-corpus-refactor-census.md"
SPECS_CENSUS_GLOB = "2026-08-29-documentation-corpus-refactor-specs-census-part-*.md"
ENTRY_HEADING_RE = re.compile(r"^(?P<marks>#{2,3}) (?P<source_id>[RS]-\d{3}) — `(?P<basename>[^`]+)`\s*$", re.MULTILINE)
FINAL_DESTINATION_RE = re.compile(
    r"^- \*\*(?:FINAL(?:_| )DESTINATION(?:_| )FILES?|FINAL(?:_| )DESTINATION):\*\*\s*(?P<value>.*)$",
    re.MULTILINE,
)
FULL_PATH_RE = re.compile(r"`(?P<path>DEV/docs/superpowers/(?:design|research|specs)/[^`]+)`")
SHORT_PATH_RE = re.compile(r"`(?P<path>(?:design|research|specs)/[^`]+)`")
PART_NUMBER_RE = re.compile(r"part-(\d+)\.md$")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _entry_blocks(text: str) -> list[tuple[str, str, str]]:
    matches = list(ENTRY_HEADING_RE.finditer(text))
    result: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group("source_id"), match.group("basename"), text[match.end() : end]))
    return result


def _destination_line(block: str) -> str | None:
    match = FINAL_DESTINATION_RE.search(block)
    return match.group("value").strip() if match else None


def _explicit_paths(value: str) -> list[str]:
    paths = [match.group("path") for match in FULL_PATH_RE.finditer(value)]
    for match in SHORT_PATH_RE.finditer(value):
        short = match.group("path")
        full = f"DEV/docs/superpowers/{short}"
        if full not in paths:
            paths.append(full)
    return paths


def _same_basename_path(paths: list[str], basename: str, kind: str) -> str | None:
    prefix = f"DEV/docs/superpowers/{kind}/"
    for path in paths:
        if path.startswith(prefix) and Path(path).name == basename:
            return path
    return None


def _resolve_destination(source_root: str, basename: str, value: str) -> tuple[str | None, list[str]]:
    if "PENDING_FINAL_SUPERSESSION_CHECK" in value:
        return None, []

    explicit = _explicit_paths(value)
    lowered = value.lower()

    design_path = _same_basename_path(explicit, basename, "design")
    research_path = _same_basename_path(explicit, basename, "research")
    specs_path = _same_basename_path(explicit, basename, "specs")

    if design_path or "`design/`" in value or "corresponding `design/` path" in lowered:
        destination = design_path or f"DEV/docs/superpowers/design/{basename}"
    elif source_root == "specs" and (research_path or "`research/`" in value):
        destination = research_path or f"DEV/docs/superpowers/research/{basename}"
    elif source_root == "research" and (
        research_path
        or "same research artifact" in lowered
        or "unchanged `research/" in lowered
        or "unchanged research" in lowered
    ):
        destination = research_path or f"DEV/docs/superpowers/research/{basename}"
    elif source_root == "specs" and (
        specs_path
        or "unchanged" in lowered
        or "retain" in lowered
        or "remain in `specs/`" in lowered
        or "remain `specs/`" in lowered
    ):
        destination = specs_path or f"DEV/docs/superpowers/specs/{basename}"
    elif source_root == "research" and research_path:
        destination = research_path
    else:
        return None, []

    extra_outputs = sorted(path for path in explicit if path != destination and Path(path).name != basename)
    return destination, extra_outputs


def _part_number(path: Path) -> int:
    match = PART_NUMBER_RE.search(path.name)
    if not match:
        raise ValueError(f"invalid specs census part name: {path}")
    return int(match.group(1))


def _parse_census_file(path: Path, source_root: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, basename, block in _entry_blocks(_read(path)):
        if not source_id.startswith("R-" if source_root == "research" else "S-"):
            continue
        value = _destination_line(block)
        destination = None
        extra_outputs: list[str] = []
        if value is not None:
            destination, extra_outputs = _resolve_destination(source_root, basename, value)
        rows.append(
            {
                "source_id": source_id,
                "basename": basename,
                "old_path": f"DEV/docs/superpowers/{source_root}/{basename}",
                "destination_path": destination,
                "extra_outputs": extra_outputs,
                "census_file": path.as_posix(),
                "destination_evidence": value,
            }
        )
    return rows


def _load_dispositions(root: Path) -> dict[str, dict[str, object]]:
    dispositions: dict[str, dict[str, object]] = {}

    research_path = root / RESEARCH_CENSUS
    for row in _parse_census_file(research_path, "research"):
        dispositions[row["old_path"]] = row

    parts = sorted((root / DESIGN_DIR).glob(SPECS_CENSUS_GLOB), key=_part_number)
    for part in parts:
        for row in _parse_census_file(part, "specs"):
            # Later census parts intentionally override earlier pending/supersession entries.
            dispositions[row["old_path"]] = row

    return dispositions


def build_migration_map(root: Path | str, *, targets: list[dict[str, str]]) -> dict[str, object]:
    root = Path(root).resolve()
    dispositions = _load_dispositions(root)

    rows: list[dict[str, object]] = []
    unresolved: list[str] = []
    extractions: list[dict[str, str]] = []

    for target in sorted(targets, key=lambda row: row["target_path"]):
        old_path = target["target_path"]
        disposition = dispositions.get(old_path)
        if disposition is None or disposition["destination_path"] is None:
            unresolved.append(old_path)
            continue

        destination_path = str(disposition["destination_path"])
        row = {
            "source_id": disposition["source_id"],
            "old_path": old_path,
            "destination_path": destination_path,
            "action": "RETAIN" if destination_path == old_path else "MOVE",
            "census_file": disposition["census_file"],
        }
        rows.append(row)

        for output in disposition["extra_outputs"]:
            extractions.append(
                {
                    "source_id": str(disposition["source_id"]),
                    "source_path": old_path,
                    "destination_path": output,
                }
            )

    rows.sort(key=lambda row: row["old_path"])
    extractions.sort(key=lambda row: (row["source_path"], row["destination_path"]))

    counts = {
        "target_count": len(targets),
        "resolved_target_count": len(rows),
        "unresolved_target_count": len(unresolved),
        "move_count": sum(row["action"] == "MOVE" for row in rows),
        "retain_count": sum(row["action"] == "RETAIN" for row in rows),
        "specs_to_design": sum(
            row["old_path"].startswith("DEV/docs/superpowers/specs/")
            and row["destination_path"].startswith("DEV/docs/superpowers/design/")
            for row in rows
        ),
        "specs_to_research": sum(
            row["old_path"].startswith("DEV/docs/superpowers/specs/")
            and row["destination_path"].startswith("DEV/docs/superpowers/research/")
            for row in rows
        ),
        "retained_specs": sum(
            row["action"] == "RETAIN" and row["old_path"].startswith("DEV/docs/superpowers/specs/")
            for row in rows
        ),
        "research_to_design": sum(
            row["old_path"].startswith("DEV/docs/superpowers/research/")
            and row["destination_path"].startswith("DEV/docs/superpowers/design/")
            for row in rows
        ),
        "retained_research": sum(
            row["action"] == "RETAIN" and row["old_path"].startswith("DEV/docs/superpowers/research/")
            for row in rows
        ),
        "extraction_count": len(extractions),
    }

    return {
        "counts": counts,
        "rows": rows,
        "extractions": extractions,
        "unresolved_targets": sorted(unresolved),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--targets-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.targets_manifest.read_text(encoding="utf-8"))
    result = build_migration_map(args.root, targets=manifest["targets"])
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    return 1 if result["unresolved_targets"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
