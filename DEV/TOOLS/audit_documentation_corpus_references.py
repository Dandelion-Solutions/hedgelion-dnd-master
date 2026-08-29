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
TARGET_MANIFEST_VERSION = 1


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
            targets.append({"target_path": relative, "basename": path.name})
    return sorted(targets, key=lambda row: row["target_path"])


def _normalize_targets(targets: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for row in targets:
        target_path = str(row["target_path"])
        basename = str(row["basename"])
        if not target_path or not basename:
            raise ValueError("target rows require non-empty target_path and basename")
        if Path(target_path).name != basename:
            raise ValueError(f"target basename mismatch: {target_path} != {basename}")
        if target_path in seen_paths:
            raise ValueError(f"duplicate target path: {target_path}")
        seen_paths.add(target_path)
        normalized.append({"target_path": target_path, "basename": basename})
    return sorted(normalized, key=lambda row: row["target_path"])


def build_target_manifest(root: Path | str) -> dict[str, object]:
    root = Path(root).resolve()
    scan_source, repository_files = _repository_files(root)
    targets = _corpus_targets(root, repository_files)
    return {
        "manifest_version": TARGET_MANIFEST_VERSION,
        "scan_source": scan_source,
        "tracked_file_count": len(repository_files) if scan_source == "git_ls_files" else None,
        "target_count": len(targets),
        "targets": targets,
    }


def build_reference_report(
    root: Path | str,
    *,
    targets: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    root = Path(root).resolve()
    scan_source, repository_files = _repository_files(root)
    effective_targets = (
        _corpus_targets(root, repository_files)
        if targets is None
        else _normalize_targets(targets)
    )

    by_basename: dict[str, list[str]] = defaultdict(list)
    for row in effective_targets:
        by_basename[row["basename"]].append(row["target_path"])

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
        "target_source": "current_corpus" if targets is None else "frozen_manifest",
        "target_count": len(effective_targets),
        "targets": effective_targets,
        "ambiguous_target_basenames": ambiguous,
        "binary_or_non_utf8_files": sorted(binary_or_non_utf8_files),
        "reference_count": len(references),
        "references": references,
    }


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_target_manifest(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("manifest_version") != TARGET_MANIFEST_VERSION:
        raise ValueError("unsupported target manifest version")
    return _normalize_targets(payload["targets"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--targets-manifest", type=Path)
    parser.add_argument("--write-targets-manifest", type=Path)
    args = parser.parse_args()

    frozen_targets = None
    if args.targets_manifest:
        frozen_targets = _load_target_manifest(args.targets_manifest)

    if args.write_targets_manifest:
        _write_json(args.write_targets_manifest, build_target_manifest(args.root))

    report = build_reference_report(args.root, targets=frozen_targets)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
