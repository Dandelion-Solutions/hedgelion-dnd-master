#!/usr/bin/env python3
"""Plan deterministic documentation-corpus path repairs.

This module is intentionally read-only.  It classifies references to corpus
sources that are scheduled to move, separating mechanically repairable path
literals from basename-only occurrences that require review.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def _relative_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _old_root_literal(path: str) -> str:
    marker = "DEV/docs/superpowers/"
    if not path.startswith(marker):
        raise ValueError(f"unsupported corpus path: {path}")
    return path[len(marker) :]


def _new_root_literal(path: str) -> str:
    marker = "DEV/docs/superpowers/"
    if not path.startswith(marker):
        raise ValueError(f"unsupported corpus destination: {path}")
    return path[len(marker) :]


def build_path_repair_plan(
    root: Path,
    migration: dict,
    *,
    repository_files: Iterable[Path],
) -> dict:
    """Classify inbound references for moved corpus targets.

    Full old paths and old-root-relative paths are mechanical repairs.
    Bare basenames are preserved as a separate review set.  Retained targets
    are deliberately ignored because they require no path repair.
    """

    root = Path(root)
    moved_rows = [row for row in migration.get("rows", []) if row.get("action") == "MOVE"]
    moved_rows.sort(key=lambda row: row["old_path"])

    mechanical_repairs: list[dict] = []
    basename_only_review: list[dict] = []
    non_utf8_files: list[str] = []

    for file_path in sorted((Path(path) for path in repository_files), key=lambda p: _relative_posix(root, p)):
        source_path = _relative_posix(root, file_path)
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            non_utf8_files.append(source_path)
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            for row in moved_rows:
                old_path = row["old_path"]
                destination_path = row["destination_path"]
                old_short = _old_root_literal(old_path)
                new_short = _new_root_literal(destination_path)
                basename = Path(old_path).name

                full_count = line.count(old_path)
                if full_count:
                    for _ in range(full_count):
                        mechanical_repairs.append(
                            {
                                "source_path": source_path,
                                "line": line_number,
                                "target_path": old_path,
                                "kind": "FULL_OLD_PATH",
                                "old_literal": old_path,
                                "new_literal": destination_path,
                            }
                        )
                    continue

                short_count = line.count(old_short)
                if short_count:
                    for _ in range(short_count):
                        mechanical_repairs.append(
                            {
                                "source_path": source_path,
                                "line": line_number,
                                "target_path": old_path,
                                "kind": "SHORT_OLD_ROOT_PATH",
                                "old_literal": old_short,
                                "new_literal": new_short,
                            }
                        )
                    continue

                basename_count = line.count(basename)
                if basename_count:
                    for _ in range(basename_count):
                        basename_only_review.append(
                            {
                                "source_path": source_path,
                                "line": line_number,
                                "target_path": old_path,
                                "basename": basename,
                            }
                        )

    mechanical_repairs.sort(
        key=lambda row: (row["source_path"], row["line"], row["target_path"], row["kind"])
    )
    basename_only_review.sort(
        key=lambda row: (row["source_path"], row["line"], row["target_path"])
    )
    non_utf8_files.sort()

    full_count = sum(row["kind"] == "FULL_OLD_PATH" for row in mechanical_repairs)
    short_count = sum(row["kind"] == "SHORT_OLD_ROOT_PATH" for row in mechanical_repairs)

    return {
        "counts": {
            "full_old_path_occurrences": full_count,
            "short_old_root_occurrences": short_count,
            "basename_only_occurrences": len(basename_only_review),
            "mechanical_repair_occurrences": len(mechanical_repairs),
            "mechanical_repair_source_files": len({row["source_path"] for row in mechanical_repairs}),
        },
        "mechanical_repairs": mechanical_repairs,
        "basename_only_review": basename_only_review,
        "non_utf8_files": non_utf8_files,
    }
