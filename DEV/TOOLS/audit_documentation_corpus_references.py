#!/usr/bin/env python3
"""Build a deterministic repository-wide reference inventory for Superpowers corpus files."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

CORPUS_DIRS = (
    Path("DEV/docs/superpowers/specs"),
    Path("DEV/docs/superpowers/research"),
)
EXCLUDED_DIR_NAMES = {".git", ".hdm-devtools", "__pycache__", ".pytest_cache"}


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _corpus_targets(root: Path) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    for rel_dir in CORPUS_DIRS:
        directory = root / rel_dir
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                targets.append({"path": _relative(root, path), "basename": path.name})
    return sorted(targets, key=lambda row: row["path"])


def _repository_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in EXCLUDED_DIR_NAMES for part in relative_parts):
            continue
        files.append(path)
    return sorted(files, key=lambda path: _relative(root, path))


def build_reference_report(root: Path | str) -> dict[str, object]:
    root = Path(root).resolve()
    targets = _corpus_targets(root)

    by_basename: dict[str, list[str]] = defaultdict(list)
    for row in targets:
        by_basename[row["basename"]].append(row["path"])

    ambiguous = {
        basename: sorted(paths)
        for basename, paths in sorted(by_basename.items())
        if len(paths) > 1
    }
    unique_targets = {
        basename: paths[0]
        for basename, paths in by_basename.items()
        if len(paths) == 1
    }

    pattern = None
    if unique_targets:
        alternatives = "|".join(
            re.escape(name) for name in sorted(unique_targets, key=lambda value: (-len(value), value))
        )
        pattern = re.compile(alternatives)

    references: list[dict[str, object]] = []
    binary_or_non_utf8_files: list[str] = []

    for path in _repository_files(root):
        source_path = _relative(root, path)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            binary_or_non_utf8_files.append(source_path)
            continue
        except OSError:
            binary_or_non_utf8_files.append(source_path)
            continue

        if pattern is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            matched = sorted({match.group(0) for match in pattern.finditer(line)})
            for basename in matched:
                references.append(
                    {
                        "source_path": source_path,
                        "line": line_number,
                        "target_path": unique_targets[basename],
                        "matched_basename": basename,
                    }
                )

    references.sort(
        key=lambda row: (
            row["source_path"],
            row["line"],
            row["target_path"],
            row["matched_basename"],
        )
    )

    return {
        "target_count": len(targets),
        "targets": [
            {"target_path": row["path"], "basename": row["basename"]}
            for row in targets
        ],
        "ambiguous_target_basenames": ambiguous,
        "binary_or_non_utf8_files": sorted(binary_or_non_utf8_files),
        "reference_count": len(references),
        "references": references,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_reference_report(args.root)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
