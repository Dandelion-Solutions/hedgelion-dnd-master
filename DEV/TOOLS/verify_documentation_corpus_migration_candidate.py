#!/usr/bin/env python3
"""Build and verify the one-shot Documentation Corpus Refactor migration candidate."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath

from apply_documentation_corpus_migration import apply_migration
from plan_documentation_corpus_path_repairs import build_path_repair_plan

EXPECTED_COUNTS = {
    "target_count": 419,
    "resolved_target_count": 419,
    "unresolved_target_count": 0,
    "move_count": 370,
    "retain_count": 49,
    "specs_to_design": 333,
    "specs_to_research": 1,
    "retained_specs": 41,
    "research_to_design": 36,
    "retained_research": 8,
    "extraction_count": 1,
}
EXPECTED_MECHANICAL_REPAIRS = 365
EXPECTED_PLANNER_REPAIRS = 503
EXPECTED_TOTAL_REPAIRS = 504
EXPECTED_HISTORICAL_EXCEPTIONS = 2
PART13 = (
    "DEV/docs/superpowers/design/"
    "2026-08-29-documentation-corpus-refactor-specs-census-part-13.md"
)
RESEARCH_DIR = "DEV/docs/superpowers/research"
RELEASE_FIXTURE = "DEV/TESTS/test_release_game_passthrough.py"
DERIVED_FIXTURE_OLD = (
    "owner_target = dev / 'docs' / 'superpowers' / 'specs' / owner.name"
)
DERIVED_FIXTURE_NEW = (
    "owner_target = dev / 'docs' / 'superpowers' / 'design' / owner.name"
)
TEMPORARY_PATHS = (
    ".github/workflows/dcr-reference-audit.yml",
    ".github/workflows/dcr-migration-candidate.yml",
    "DEV/TOOLS/verify_documentation_corpus_migration_candidate.py",
    "DEV/TESTS/test_documentation_corpus_candidate_verifier.py",
)


def _run(args: list[str], *, root: Path, capture: bool = False) -> subprocess.CompletedProcess[bytes]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        args,
        cwd=root,
        check=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=None,
        env=env,
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_historical_exception(source_path: str, target_final: str) -> bool:
    return (
        source_path == PART13
        and PurePosixPath(target_final).parent.as_posix() == RESEARCH_DIR
    )


def _append_derived_path_repairs(root: Path, repairs: list[dict[str, object]]) -> None:
    """Add the one path construction that cannot contain a target basename.

    The release fixture reconstructs the destination directory using ``owner.name``.
    Filename-oriented inbound-reference scans therefore cannot discover this path.
    Post-move candidate verification exposed it; keep it explicit and fail closed.
    """

    fixture = Path(root) / RELEASE_FIXTURE
    if not fixture.is_file():
        raise RuntimeError("release fixture required for derived DCR repair is missing")
    lines = fixture.read_text(encoding="utf-8").splitlines()
    matches = [
        line_number
        for line_number, line in enumerate(lines, start=1)
        if DERIVED_FIXTURE_OLD in line
    ]
    if len(matches) != 1:
        raise RuntimeError(
            "derived release-fixture DCR path must occur exactly once; "
            f"observed={len(matches)}"
        )
    repairs.append(
        {
            "source_path": RELEASE_FIXTURE,
            "line": matches[0],
            "old_literal": DERIVED_FIXTURE_OLD,
            "new_literal": DERIVED_FIXTURE_NEW,
        }
    )


def _tracked_files(root: Path) -> list[Path]:
    raw = _run(["git", "ls-files", "-z"], root=root, capture=True).stdout.decode("utf-8")
    return [root / path for path in raw.split("\0") if path and (root / path).is_file()]


def _build_inputs(root: Path, out: Path) -> tuple[dict[str, object], dict[str, object]]:
    python = sys.executable
    _run(
        [
            python,
            "DEV/TOOLS/audit_documentation_corpus_references.py",
            "--write-targets-manifest",
            str(out / "pre-migration-targets.json"),
            "--output",
            str(out / "pre-migration-reference-report.json"),
        ],
        root=root,
    )
    _run(
        [
            python,
            "DEV/TOOLS/build_documentation_corpus_migration_map.py",
            "--targets-manifest",
            str(out / "pre-migration-targets.json"),
            "--output",
            str(out / "migration-map.json"),
        ],
        root=root,
    )
    migration = json.loads((out / "migration-map.json").read_text(encoding="utf-8"))
    if migration["counts"] != EXPECTED_COUNTS or migration["unresolved_targets"]:
        raise RuntimeError("migration-map accounting changed before candidate application")

    plan = build_path_repair_plan(root, migration, repository_files=_tracked_files(root))
    _write_json(out / "pre-migration-path-repair-plan.json", plan)
    return migration, plan


def _review_repairs(
    migration: dict[str, object],
    plan: dict[str, object],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    mmap = {row["old_path"]: row for row in migration["rows"]}
    repairs = [
        {
            "source_path": row["source_path"],
            "line": row["line"],
            "old_literal": row["old_literal"],
            "new_literal": row["new_literal"],
        }
        for row in plan["mechanical_repairs"]
    ]
    exceptions: list[dict[str, object]] = []

    for row in plan["basename_only_review"]:
        source = row["source_path"]
        target = row["target_path"]
        source_final = mmap[source]["destination_path"] if source in mmap else source
        target_final = mmap[target]["destination_path"]
        if PurePosixPath(source_final).parent == PurePosixPath(target_final).parent:
            continue

        basename = PurePosixPath(target).name
        if _is_historical_exception(source, target_final):
            exceptions.append(row)
            continue

        if (
            source.startswith("DEV/docs/superpowers/specs/")
            and mmap[source]["action"] == "RETAIN"
            and PurePosixPath(target_final).parent.as_posix()
            == "DEV/docs/superpowers/design"
        ):
            repairs.append(
                {
                    "source_path": source,
                    "line": row["line"],
                    "old_literal": basename,
                    "new_literal": "../design/" + basename,
                }
            )
            continue

        if source == "DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md":
            repairs.append(
                {
                    "source_path": source,
                    "line": row["line"],
                    "old_literal": basename,
                    "new_literal": target_final,
                }
            )
            continue

        if source == RELEASE_FIXTURE:
            repairs.append(
                {
                    "source_path": source,
                    "line": row["line"],
                    "old_literal": "'specs' / '" + basename + "'",
                    "new_literal": "'design' / '" + basename + "'",
                }
            )
            continue

        raise RuntimeError(
            "unresolved cross-directory basename occurrence: "
            + json.dumps(row, sort_keys=True)
        )

    if len(plan["mechanical_repairs"]) != EXPECTED_MECHANICAL_REPAIRS:
        raise RuntimeError(
            f"mechanical repair count drifted: {len(plan['mechanical_repairs'])}"
        )
    if len(repairs) != EXPECTED_PLANNER_REPAIRS:
        raise RuntimeError(f"reviewed planner repair count drifted: {len(repairs)}")
    if len(exceptions) != EXPECTED_HISTORICAL_EXCEPTIONS:
        raise RuntimeError(f"historical exception count drifted: {len(exceptions)}")
    return repairs, exceptions


def _verify_physical_result(
    root: Path,
    migration: dict[str, object],
    repairs: list[dict[str, object]],
    exceptions: list[dict[str, object]],
) -> None:
    mmap = {row["old_path"]: row for row in migration["rows"]}
    for item in migration["rows"]:
        old = root / item["old_path"]
        destination = root / item["destination_path"]
        if item["action"] == "MOVE":
            if old.exists() or not destination.is_file():
                raise RuntimeError("physical move verification failed: " + item["old_path"])
        elif item["action"] == "RETAIN":
            if not old.is_file() or destination != old:
                raise RuntimeError("retained-source verification failed: " + item["old_path"])

    extraction = root / RESEARCH_DIR / "2026-08-24-chatgpt-plus-host-evidence.md"
    if not extraction.is_file():
        raise RuntimeError("R-015 extraction missing")

    for repair in repairs:
        source = repair["source_path"]
        source_final = mmap[source]["destination_path"] if source in mmap else source
        lines = (root / source_final).read_text(encoding="utf-8").splitlines()
        line = lines[int(repair["line"]) - 1]
        if repair["new_literal"] not in line:
            raise RuntimeError(
                "post-move repair verification failed: "
                + json.dumps(repair, sort_keys=True)
            )

    for exception in exceptions:
        lines = (root / exception["source_path"]).read_text(encoding="utf-8").splitlines()
        target_name = PurePosixPath(exception["target_path"]).name
        if target_name not in lines[int(exception["line"]) - 1]:
            raise RuntimeError("historical exception was not preserved")


def _run_repository_verification(root: Path) -> None:
    shutil.rmtree(root / ".hdm-devtools", ignore_errors=True)
    for cache in root.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache, ignore_errors=True)
    _run([str(root / "DEV/TOOLS/run_maintenance_audit")], root=root)
    _run(
        [
            str(root / ".hdm-devtools/venv/bin/python"),
            "-m",
            "unittest",
            "discover",
            "-s",
            "DEV/TESTS",
            "-v",
        ],
        root=root,
    )


def _remove_temporary_paths(root: Path) -> None:
    for relative in TEMPORARY_PATHS:
        path = root / relative
        if path.exists():
            path.unlink()


def _index_sha(root: Path, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD:" + path],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _head_bytes(root: Path, path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "show", "HEAD:" + path],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return completed.stdout if completed.returncode == 0 else None


def _build_candidate_metadata(root: Path, out: Path, head_sha: str) -> dict[str, object]:
    _run(["git", "diff", "--check"], root=root)
    _run(["git", "add", "-A"], root=root)

    raw = _run(
        ["git", "diff", "--cached", "--name-status", "-z"],
        root=root,
        capture=True,
    ).stdout.decode("utf-8")
    fields = raw.split("\0")
    ops: list[dict[str, str]] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index]
        index += 1
        if status.startswith("R"):
            old = fields[index]
            new = fields[index + 1]
            index += 2
            ops.append({"status": status, "old_path": old, "path": new})
        else:
            path = fields[index]
            index += 1
            ops.append({"status": status, "path": path})

    candidate_files = out / "candidate-files"
    candidate_files.mkdir(parents=True, exist_ok=True)
    tree_ops: list[dict[str, object]] = []
    payload_paths: list[str] = []

    for op in ops:
        status = op["status"][0]
        if status == "D":
            tree_ops.append(
                {"path": op["path"], "mode": "100644", "type": "blob", "sha": None}
            )
            continue

        if status == "R":
            old = op["old_path"]
            new = op["path"]
            tree_ops.append(
                {"path": old, "mode": "100644", "type": "blob", "sha": None}
            )
            old_bytes = _head_bytes(root, old)
            new_bytes = (root / new).read_bytes()
            old_sha = _index_sha(root, old)
            if old_bytes is not None and old_sha and new_bytes == old_bytes:
                tree_ops.append(
                    {
                        "path": new,
                        "mode": "100644",
                        "type": "blob",
                        "sha": old_sha,
                        "requires_content": False,
                    }
                )
            else:
                tree_ops.append(
                    {
                        "path": new,
                        "mode": "100644",
                        "type": "blob",
                        "sha": None,
                        "requires_content": True,
                    }
                )
                payload_paths.append(new)
            continue

        if status in {"A", "M"}:
            path = op["path"]
            tree_ops.append(
                {
                    "path": path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": None,
                    "requires_content": True,
                }
            )
            payload_paths.append(path)
            continue

        raise RuntimeError("unsupported candidate status: " + op["status"])

    for path in sorted(set(payload_paths)):
        destination = candidate_files / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / path, destination)

    candidate_tree_sha = _run(["git", "write-tree"], root=root, capture=True).stdout.decode().strip()
    summary = {
        "head_sha": head_sha,
        "changed_entry_count": len(ops),
        "tree_operation_count": len(tree_ops),
        "changed_payload_file_count": len(set(payload_paths)),
        "candidate_tree_sha_local": candidate_tree_sha,
    }
    _write_json(out / "candidate-tree-ops.json", tree_ops)
    _write_json(out / "candidate-summary.json", summary)
    (out / "candidate.patch").write_bytes(
        _run(["git", "diff", "--cached", "--binary"], root=root, capture=True).stdout
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def _assert_no_stale_full_or_short_references(
    root: Path,
    migration: dict[str, object],
    report: dict[str, object],
) -> None:
    by_target = {row["old_path"]: row for row in migration["rows"] if row["action"] == "MOVE"}
    stale: list[dict[str, object]] = []
    marker = "DEV/docs/superpowers/"
    for reference in report["references"]:
        target = reference["target_path"]
        if target not in by_target:
            continue
        source = root / reference["source_path"]
        if not source.is_file():
            continue
        lines = source.read_text(encoding="utf-8").splitlines()
        line_number = int(reference["line"])
        if line_number < 1 or line_number > len(lines):
            continue
        line = lines[line_number - 1]
        old_short = target[len(marker) :] if target.startswith(marker) else target
        if target in line or old_short in line:
            stale.append(reference)
    if stale:
        raise RuntimeError(
            "post-move frozen replay found stale full/short paths: "
            + json.dumps(stale[:20], sort_keys=True)
        )


def _commit_candidate_locally(root: Path, expected_tree_sha: str, source_head: str) -> str:
    observed_source = _run(["git", "rev-parse", "HEAD"], root=root, capture=True).stdout.decode().strip()
    if observed_source != source_head:
        raise RuntimeError(
            f"candidate source HEAD drifted: expected={source_head} observed={observed_source}"
        )
    _run(
        [
            "git",
            "-c",
            "user.name=HDM DCR Candidate",
            "-c",
            "user.email=hdm-dcr-candidate@invalid",
            "commit",
            "--no-gpg-sign",
            "-m",
            "DCR candidate verification",
        ],
        root=root,
    )
    candidate_commit = _run(["git", "rev-parse", "HEAD"], root=root, capture=True).stdout.decode().strip()
    observed_tree = _run(["git", "rev-parse", "HEAD^{tree}"], root=root, capture=True).stdout.decode().strip()
    if observed_tree != expected_tree_sha:
        raise RuntimeError(
            f"candidate local commit tree mismatch: expected={expected_tree_sha} observed={observed_tree}"
        )
    parent = _run(["git", "rev-parse", "HEAD^"], root=root, capture=True).stdout.decode().strip()
    if parent != source_head:
        raise RuntimeError(f"candidate local commit parent mismatch: {parent}")
    return candidate_commit


def _assert_clean_candidate(root: Path) -> None:
    status = _run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        root=root,
        capture=True,
    ).stdout.decode().strip()
    if status:
        raise RuntimeError("candidate verification dirtied tracked tree: " + status)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--head-sha", required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    observed_head = _run(["git", "rev-parse", "HEAD"], root=root, capture=True).stdout.decode().strip()
    if observed_head != args.head_sha:
        raise RuntimeError(
            f"workflow checkout is not exact source HEAD: expected={args.head_sha} observed={observed_head}"
        )

    out = root / ".hdm-maintenance" / "dcr-migration-candidate"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    migration, plan = _build_inputs(root, out)
    repairs, exceptions = _review_repairs(migration, plan)
    _append_derived_path_repairs(root, repairs)
    if len(repairs) != EXPECTED_TOTAL_REPAIRS:
        raise RuntimeError(f"total repair count drifted: {len(repairs)}")
    _write_json(out / "repairs.json", repairs)
    _write_json(out / "historical-exceptions.json", exceptions)

    result = apply_migration(root, migration=migration, repairs=repairs)
    expected_result = {
        "move_count": 370,
        "repair_count": EXPECTED_TOTAL_REPAIRS,
        "extraction_count": 1,
    }
    if result != expected_result:
        raise RuntimeError(
            "candidate application accounting mismatch: " + json.dumps(result, sort_keys=True)
        )

    _verify_physical_result(root, migration, repairs, exceptions)

    # DCR-only orchestration is deliberately absent from the durable post-refactor tree.
    _remove_temporary_paths(root)
    for cache in root.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache, ignore_errors=True)

    # Freeze the exact final tree while the source HEAD still identifies the pre-migration parent.
    summary = _build_candidate_metadata(root, out, args.head_sha)

    # Replay the frozen target manifest against the staged final tree.  Basenames may remain
    # in valid new relative links/provenance, but no full or old-root path may survive.
    _run(
        [
            sys.executable,
            "DEV/TOOLS/audit_documentation_corpus_references.py",
            "--targets-manifest",
            str(out / "pre-migration-targets.json"),
            "--output",
            str(out / "post-migration-frozen-reference-report.json"),
        ],
        root=root,
    )
    post_report = json.loads(
        (out / "post-migration-frozen-reference-report.json").read_text(encoding="utf-8")
    )
    if post_report["binary_or_non_utf8_files"]:
        raise RuntimeError("post-move frozen replay encountered non-UTF8 tracked files")
    _assert_no_stale_full_or_short_references(root, migration, post_report)

    # Release/provenance tests intentionally require clean HEAD.  Create a local-only commit
    # in this disposable Actions checkout, prove it has the exact frozen candidate tree, then
    # run the complete repository verification on that clean tree.  No remote ref is mutated.
    candidate_commit = _commit_candidate_locally(
        root,
        str(summary["candidate_tree_sha_local"]),
        args.head_sha,
    )
    summary["candidate_local_verification_commit"] = candidate_commit
    _write_json(out / "candidate-summary.json", summary)

    _run_repository_verification(root)
    _assert_clean_candidate(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
