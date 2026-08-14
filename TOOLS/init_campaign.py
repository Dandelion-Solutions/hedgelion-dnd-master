#!/usr/bin/env python3
"""Generate a root-layout campaign scaffold from the local D&D Master release.

The local engine directory CAMPAIGN/ is a TEMPLATE SOURCE. Its contents become
the root of the generated campaign tree. Standard-library only. No GitHub access.
No base64.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def replace_once(text: str, old: str, new: str, path: Path) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one {old!r}, found {count}")
    return text.replace(old, new, 1)


def yaml_nullable_string(value: str | None) -> str:
    return "null" if value is None else yaml_string(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--engine-tag", required=True)
    parser.add_argument("--engine-sha", required=False)
    parser.add_argument("--created-at", required=True)
    parser.add_argument("--mode", choices=("singleplayer", "multiplayer"), default="singleplayer")
    parser.add_argument(
        "--source-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Extracted engine root; defaults to parent of TOOLS/",
    )
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    source_campaign = source_root / "CAMPAIGN"
    output = Path(args.output).resolve()

    if not source_campaign.is_dir():
        raise RuntimeError(f"CAMPAIGN template not found: {source_campaign}")
    if output.exists():
        raise RuntimeError(f"Output already exists: {output}")

    # copytree copies CONTENTS into output. `output` itself is the future branch root.
    shutil.copytree(source_campaign, output)

    manifest_path = output / "MANIFEST.yaml"
    manifest = manifest_path.read_text(encoding="utf-8")
    engine_sha = yaml_nullable_string(args.engine_sha)
    replacements = [
        ("campaign_id: null", f"campaign_id: {yaml_string(args.campaign_id)}"),
        ("branch: null", f"branch: {yaml_string(args.branch)}"),
        ("status: uninitialized", "status: initializing"),
        ("mode: singleplayer", f"mode: {args.mode}"),
        ("  base_tag: null", f"  base_tag: {yaml_string(args.engine_tag)}"),
        ("  base_sha: null", f"  base_sha: {engine_sha}"),
        ("  integrated_tag: null", f"  integrated_tag: {yaml_string(args.engine_tag)}"),
        ("  integrated_main_sha: null", f"  integrated_main_sha: {engine_sha}"),
        ("created_at: null", f"created_at: {yaml_string(args.created_at)}"),
    ]
    for old, new in replacements:
        manifest = replace_once(manifest, old, new, manifest_path)
    manifest_path.write_text(manifest, encoding="utf-8")

    current_path = output / "STATE" / "CURRENT.yaml"
    current = current_path.read_text(encoding="utf-8")
    current = replace_once(
        current,
        "campaign_id: null",
        f"campaign_id: {yaml_string(args.campaign_id)}",
        current_path,
    )
    current_path.write_text(current, encoding="utf-8")

    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        print(path.relative_to(output).as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
