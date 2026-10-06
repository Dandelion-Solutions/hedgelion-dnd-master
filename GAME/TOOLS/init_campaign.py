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

if __package__:
    from .native_storage import FAMILY_ROOTS
else:
    from native_storage import FAMILY_ROOTS


_BLANK_COMPANION_TEMPLATES = {
    "STATE/CURRENT.yaml": (
        "schema_version: 3\n"
        "campaign_id: null\n"
        "world_time:\n"
        "  display: null\n"
        "active_scenes: []\n"
        "active_threads: []\n"
    ),
    "STATE/ID_ALLOCATOR.yaml": (
        "schema_version: 1\n"
        "kind: runtime.id_allocator\n"
        "campaign_id: null\n"
        "counters: {}\n"
    ),
    "STATE/RUNTIME/LIVE_ROUTING.yaml": (
        "schema_version: 4\n"
        "kind: runtime.live_routing\n"
        "campaign_id: null\n"
        "complete: true\n"
        "entries: []\n"
    ),
    "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml": (
        "schema_version: 1\n"
        "kind: runtime.principal_player_routing\n"
        "campaign_id: null\n"
        "complete: true\n"
        "entries: []\n"
    ),
    "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml": (
        "schema_version: 1\ncampaign_id: null\ncomplete: true\nroots: []\n"
    ),
}
_IDENTITY_COMPANIONS = tuple(_BLANK_COMPANION_TEMPLATES)
_BLANK_EVENT_INDEX = (
    "schema_version: 2\nentity_type: EVENT\ncomplete: true\n"
    "upper_ordinal: null\nentries: []\n"
)
_INDEX_FILES = frozenset(
    {
        "EVENT_INDEX.yaml",
        "FACTION_INDEX.yaml",
        "ITEM_INDEX.yaml",
        "LOCATION_INDEX.yaml",
        "LORE_INDEX.yaml",
        "NPC_INDEX.yaml",
        "PC_INDEX.yaml",
        "PLAYER_INDEX.yaml",
        "SCENE_INDEX.yaml",
        "THREAD_INDEX.yaml",
    }
)
_REQUIRED_CAMPAIGN_DIRECTORIES = frozenset(FAMILY_ROOTS.values()) | frozenset(
    {
        "INDEX",
        "LOG",
        "CHECKPOINTS",
        "SESSIONS",
        "RULES",
        "STORY/EVENTS",
        "STORY/MECHANICS",
        "STORY/NARRATIVE",
        "STORY/TRANSCRIPT",
        "DRAMATURG/PLAYERS",
        "STATE/RUNTIME/RECOVERY_ROOTS",
    }
)
_REQUIRED_CAMPAIGN_FILES = frozenset(
    {
        "README.md",
        "MANIFEST.yaml",
        "CAMPAIGN_CARD.yaml",
        "CONFIG.yaml",
        "STATE/ID_ALLOCATOR.yaml",
        "STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml",
        "LOG/_TEMPLATE.yaml",
        "CHECKPOINTS/_TEMPLATE.yaml",
        "SESSIONS/_TEMPLATE.yaml",
        "RULES/HOUSE_RULES.md",
        "RULES/HOUSE_RULES.yaml",
        "DRAMATURG/SHARED.yaml",
        *_IDENTITY_COMPANIONS,
        *(f"INDEX/{name}" for name in _INDEX_FILES),
    }
)
_STORAGE_MARKER_NAMES = frozenset({"DND_STORAGE", "DND_STORAGE.yaml"})


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def replace_once(text: str, old: str, new: str, path: Path) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one {old!r}, found {count}")
    return text.replace(old, new, 1)


def yaml_nullable_string(value: str | None) -> str:
    return "null" if value is None else yaml_string(value)


def _read_campaign_tree(
    campaign_root: Path,
) -> tuple[dict[str, bytes], frozenset[str]]:
    if campaign_root.is_symlink() or not campaign_root.is_dir():
        raise RuntimeError(
            f"CAMPAIGN template is not a regular directory: {campaign_root}"
        )

    files: dict[str, bytes] = {}
    directories: set[str] = set()
    for path in sorted(campaign_root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"CAMPAIGN template contains a symlink: {path}")
        if path.name in _STORAGE_MARKER_NAMES:
            raise RuntimeError(f"CAMPAIGN template contains a storage marker: {path}")
        relative_path = path.relative_to(campaign_root).as_posix()
        if path.is_dir():
            directories.add(relative_path)
        elif path.is_file():
            files[relative_path] = path.read_bytes()
        else:
            raise RuntimeError(
                f"CAMPAIGN template contains an unsupported path: {path}"
            )
    return files, frozenset(directories)


def _validate_campaign_structure(
    files: dict[str, bytes], directories: frozenset[str]
) -> None:
    missing_files = sorted(_REQUIRED_CAMPAIGN_FILES - files.keys())
    missing_directories = sorted(_REQUIRED_CAMPAIGN_DIRECTORIES - directories)
    missing_root_entries = sorted(
        root
        for root in _REQUIRED_CAMPAIGN_DIRECTORIES
        if not any(path.startswith(f"{root}/") for path in files)
    )
    if missing_files or missing_directories or missing_root_entries:
        raise RuntimeError(
            "CAMPAIGN template is incomplete: "
            f"missing files={missing_files}, "
            f"directories={missing_directories}, "
            f"root entries={missing_root_entries}"
        )


def _decode_campaign_file(files: dict[str, bytes], relative_path: str) -> str:
    try:
        return files[relative_path].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"CAMPAIGN template file is not UTF-8: {relative_path}"
        ) from exc


def _validate_campaign_template(
    files: dict[str, bytes], directories: frozenset[str]
) -> None:
    _validate_campaign_structure(files, directories)
    if _decode_campaign_file(files, "INDEX/EVENT_INDEX.yaml") != _BLANK_EVENT_INDEX:
        raise RuntimeError("EVENT_INDEX must remain complete empty native enrollment")

    manifest = _decode_campaign_file(files, "MANIFEST.yaml")
    if (
        not manifest.startswith("schema_version: 4\n")
        or "campaign_contract:\n  created_with: 2\n  current: 2\n" not in manifest
        or "players:\n  join_policy: invite_only\n  player_ids: []\n" not in manifest
    ):
        raise RuntimeError("MANIFEST template must remain schema v4 with player_ids")

    for relative_path, expected_template in _BLANK_COMPANION_TEMPLATES.items():
        content = _decode_campaign_file(files, relative_path)
        if content != expected_template:
            raise RuntimeError(
                f"campaign identity companion is not an exact blank template: {relative_path}"
            )


def _render_campaign_files(
    files: dict[str, bytes], *, args: argparse.Namespace
) -> dict[str, bytes]:
    rendered = dict(files)
    manifest_path = Path("MANIFEST.yaml")
    manifest = _decode_campaign_file(files, "MANIFEST.yaml")
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
        "\nruleset:\n"
        "  created_with:\n"
        "    ruleset_set_sha256: null\n"
        "    ruleset_set_digest_generation: 1\n"
        "  current:\n"
        "    ruleset_set_sha256: null\n"
        "    ruleset_set_digest_generation: 1\n"
        "    adopted_at: null"
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
        "\nruleset:\n"
        "  created_with:\n"
        f"    ruleset_set_sha256: {yaml_string(args.ruleset_set_sha256.lower())}\n"
        "    ruleset_set_digest_generation: 1\n"
        "  current:\n"
        f"    ruleset_set_sha256: {yaml_string(args.ruleset_set_sha256.lower())}\n"
        "    ruleset_set_digest_generation: 1\n"
        f"    adopted_at: {yaml_string(args.created_at)}"
    )
    manifest = replace_once(manifest, old_engine, new_engine, manifest_path)
    manifest_replacements = (
        ("campaign_id: null", f"campaign_id: {yaml_string(args.campaign_id)}"),
        ("branch: null", f"branch: {yaml_string(args.branch)}"),
        ("status: uninitialized", "status: initializing"),
        ("mode: singleplayer", f"mode: {args.mode}"),
        ("created_at: null", f"created_at: {yaml_string(args.created_at)}"),
    )
    for old, new in manifest_replacements:
        manifest = replace_once(manifest, old, new, manifest_path)
    rendered["MANIFEST.yaml"] = manifest.encode("utf-8")

    card_path = Path("CAMPAIGN_CARD.yaml")
    card = _decode_campaign_file(files, "CAMPAIGN_CARD.yaml")
    card_replacements = (
        ("campaign_id: null", f"campaign_id: {yaml_string(args.campaign_id)}"),
        ("mode: singleplayer", f"mode: {args.mode}"),
        ("engine_version: null", f"engine_version: {yaml_string(args.engine_version)}"),
        (
            "creator_github_login: null",
            f"creator_github_login: {yaml_string(args.creator_github_login)}",
        ),
    )
    for old, new in card_replacements:
        card = replace_once(card, old, new, card_path)
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
    rendered["CAMPAIGN_CARD.yaml"] = card.encode("utf-8")

    for relative_path in _IDENTITY_COMPANIONS:
        content = _decode_campaign_file(files, relative_path)
        updated = replace_once(
            content,
            "campaign_id: null",
            f"campaign_id: {yaml_string(args.campaign_id)}",
            Path(relative_path),
        )
        rendered[relative_path] = updated.encode("utf-8")
    return rendered


def _write_campaign_tree(
    output: Path,
    files: dict[str, bytes],
    directories: frozenset[str],
) -> None:
    if output.exists() or output.is_symlink():
        raise RuntimeError(f"Output already exists: {output}")
    created = False
    try:
        output.mkdir()
        created = True
        for relative_path in sorted(directories):
            (output / relative_path).mkdir(parents=True, exist_ok=True)
        for relative_path, content in sorted(files.items()):
            destination = output / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    except OSError:
        if created:
            shutil.rmtree(output)
        raise


def validate_generated_scaffold(
    output_root: Path, campaign_id: str
) -> dict[str, bytes]:
    """Validate a generated campaign and return its exact path-to-bytes map."""

    files, directories = _read_campaign_tree(output_root)
    _validate_campaign_structure(files, directories)

    manifest = _decode_campaign_file(files, "MANIFEST.yaml")
    if (
        not manifest.startswith("schema_version: 4\n")
        or f"campaign_id: {yaml_string(campaign_id)}\n" not in manifest
        or "players:\n  join_policy: invite_only\n  player_ids: []\n" not in manifest
    ):
        raise RuntimeError(
            "generated MANIFEST does not match the frozen campaign identity"
        )

    for relative_path, blank_template in _BLANK_COMPANION_TEMPLATES.items():
        content = _decode_campaign_file(files, relative_path)
        expected_content = replace_once(
            blank_template,
            "campaign_id: null",
            f"campaign_id: {yaml_string(campaign_id)}",
            Path(relative_path),
        )
        if content != expected_content:
            raise RuntimeError(
                f"generated campaign identity differs in {relative_path}"
            )
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--engine-version", required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--source-commit-sha", required=False)
    parser.add_argument("--package-sha256", required=True)
    parser.add_argument("--ruleset-set-sha256", required=True)
    parser.add_argument("--created-at", required=True)
    parser.add_argument("--creator-github-login", required=True)
    parser.add_argument(
        "--mode", choices=("singleplayer", "multiplayer"), default="singleplayer"
    )
    parser.add_argument(
        "--source-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Extracted engine root; defaults to parent of TOOLS/",
    )
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    source_campaign = source_root / "CAMPAIGN"
    output = Path(args.output).resolve()

    if output == source_campaign or source_campaign in output.parents:
        raise RuntimeError("Output must be outside the selected CAMPAIGN template")
    if len(args.package_sha256) != 64 or any(
        ch not in "0123456789abcdefABCDEF" for ch in args.package_sha256
    ):
        raise RuntimeError(
            "--package-sha256 must be a 64-character hexadecimal SHA-256"
        )
    if len(args.ruleset_set_sha256) != 64 or any(
        ch not in "0123456789abcdefABCDEF" for ch in args.ruleset_set_sha256
    ):
        raise RuntimeError(
            "--ruleset-set-sha256 must be a 64-character hexadecimal SHA-256"
        )

    template_files, template_directories = _read_campaign_tree(source_campaign)
    _validate_campaign_template(template_files, template_directories)
    rendered_files = _render_campaign_files(template_files, args=args)
    _write_campaign_tree(output, rendered_files, template_directories)
    try:
        generated_files = validate_generated_scaffold(output, args.campaign_id)
    except (OSError, RuntimeError):
        shutil.rmtree(output)
        raise

    for relative_path in sorted(generated_files):
        print(relative_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
