#!/usr/bin/env python3
"""Build a deterministic repository-wide reference inventory for Superpowers corpus files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

CORPUS_DIRS = (
    Path("DEV/docs/superpowers/specs"),
    Path("DEV/docs/superpowers/research"),
)
EXCLUDED_DIR_NAMES = {".git", ".hdm-devtools", "__pycache__", ".pytest_cache"}


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _git_tracked_files(root: Path) -> list[Path] | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None

    files: list[Path] = []
    for raw in completed.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            relative = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        path = root / relative
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda path: _relative(root, path))


def _walk_repository_files(root: Path) -> list[Path]:
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


def _repository_files(root: Path) -> tuple[str, list[Path]]:
    tracked = _git_tracked_files(root)
    if tracked is not None:
        return "git_ls_files", tracked
    return "filesystem_walk", _walk_repository_files(root)


def _corpus_targets(root: Path, repository_files: list[Path]) -> list[dict[str, str]]:
    prefixes = tuple(f"{path.as_posix()}/" for path in CORPUS_DIRS)
    targets: list[dict[str, str]] = []
    for path in repository_files:
        relative = _relative(root, path)
        if relative.startswith(prefixes):
            targets.append({"path": relative, "basename": path.name})
    return sorted(targets, key=lambda row: row["path"])


def build_reference_report(root: Path | str) -> dict[str, object]:
    root = Path(root).resolve()
    scan_source, repository_files = _repository_files(root)
    targets = _corpus_targets(root, repository_files)

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

    for path in repository_files:
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
        "scan_source": scan_source,
        "tracked_file_count": len(repository_files) if scan_source == "git_ls_files" else None,
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
