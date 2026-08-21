#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "DEV/TOOLS"
sys.path.insert(0, str(TOOLS))
from dev_tool_environment import PreparationError, ensure_environment


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_release_build.py",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            "Build the deterministic HDM runtime ZIP and SHA-256 sidecar. "
            "Development dependencies are prepared in the isolated .hdm-devtools environment."
        ),
    )
    parser.add_argument(
        "-h", "-?", "--h", "--help",
        action="help",
        help="show this usage/help text and exit",
    )
    parser.add_argument(
        "--tag",
        metavar="TAG",
        help=(
            "release tag, for example v0.8; when omitted, use recommended_tag "
            "from DEV/ENGINE_DEVELOPMENT.yaml"
        ),
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        default=str(REPO_ROOT / "builds"),
        help="directory for the generated runtime ZIP and .sha256 file",
    )
    parser.add_argument(
        "--tag-mode",
        action="store_true",
        help=(
            "enforce tagged-release checks (ready-for-tag status and approved Git lineage); "
            "intended for the release workflow"
        ),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        py = ensure_environment(REPO_ROOT)
    except PreparationError as exc:
        print(f"ERROR: DEV tool environment preparation failed: {exc}", file=sys.stderr)
        return exc.exit_code
    cmd = [str(py), str(TOOLS / "release_builder.py"), "--output", args.output]
    if args.tag is not None:
        cmd.extend(["--tag", args.tag])
    if args.tag_mode:
        cmd.append("--tag-mode")
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
