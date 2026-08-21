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
    parser.add_argument("--engine-version", required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--source-commit-sha", required=False)
    parser.add_argument("--package-sha256", required=True)
    parser.add_argument("--created-at", required=True)
    parser.add_argument("--creator-github-login", required=True)
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
    if len(args.package_sha256) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in args.package_sha256):
        raise RuntimeError("--package-sha256 must be a 64-character hexadecimal SHA-256")

    # copytree copies CONTENTS into output. `output` itself is the future branch root.
    shutil.copytree(source_campaign, output)

    manifest_path = output / "MANIFEST.yaml"
    manifest = manifest_path.read_text(encoding="utf-8")
    source_sha = yaml_nullable_string(args.source_commit_sha)
    old_engine = (
        "engine:\n"
        "  created_with:\n"
        "    version: null\n"
        "    package_id: null\n"
        "    source_commit_sha: null\n"
        "  current:\n"
        "    version: null\n"
        "    package_id: null\n"
        "    source_commit_sha: null\n"
        "    package_sha256: null\n"
        "    adopted_at: null\n"
        "  update_policy: ask"
    )
    new_engine = (
        "engine:\n"
        "  created_with:\n"
        f"    version: {yaml_string(args.engine_version)}\n"
        f"    package_id: {yaml_string(args.package_id)}\n"
        f"    source_commit_sha: {source_sha}\n"
        "  current:\n"
        f"    version: {yaml_string(args.engine_version)}\n"
        f"    package_id: {yaml_string(args.package_id)}\n"
        f"    source_commit_sha: {source_sha}\n"
        f"    package_sha256: {yaml_string(args.package_sha256.lower())}\n"
        f"    adopted_at: {yaml_string(args.created_at)}\n"
        "  update_policy: ask"
    )
    manifest = replace_once(manifest, old_engine, new_engine, manifest_path)
    replacements = [
        ("campaign_id: null", f"campaign_id: {yaml_string(args.campaign_id)}"),
        ("branch: null", f"branch: {yaml_string(args.branch)}"),
        ("status: uninitialized", "status: initializing"),
        ("mode: singleplayer", f"mode: {args.mode}"),
        ("created_at: null", f"created_at: {yaml_string(args.created_at)}"),
    ]
    for old, new in replacements:
        manifest = replace_once(manifest, old, new, manifest_path)
    manifest_path.write_text(manifest, encoding="utf-8")

    card_path = output / "CAMPAIGN_CARD.yaml"
    card = card_path.read_text(encoding="utf-8")
    card = replace_once(card, "campaign_id: null", f"campaign_id: {yaml_string(args.campaign_id)}", card_path)
    card = replace_once(card, "mode: singleplayer", f"mode: {args.mode}", card_path)
    card = replace_once(
        card,
        "engine_version: null",
        f"engine_version: {yaml_string(args.engine_version)}",
        card_path,
    )
    card = replace_once(
        card,
        "creator_github_login: null",
        f"creator_github_login: {yaml_string(args.creator_github_login)}",
        card_path,
    )
    if args.mode == "multiplayer":
        card = replace_once(
            card,
            "protagonist:\n  name: null\n  role_race: null",
            "protagonist: null",
            card_path,
        )
        card = replace_once(
            card,
            "multiplayer: null",
            "multiplayer:\n  join_policy: invite_only\n  participant_github_logins: []",
            card_path,
        )
    card_path.write_text(card, encoding="utf-8")

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
