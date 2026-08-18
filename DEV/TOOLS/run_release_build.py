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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag")
    parser.add_argument("--output", default=str(REPO_ROOT / "builds"))
    parser.add_argument("--tag-mode", action="store_true")
    args = parser.parse_args()
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
