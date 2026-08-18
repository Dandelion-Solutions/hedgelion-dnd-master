from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import struct
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

import yaml


class BuildError(RuntimeError):
    pass


GAME_FIELDS = {
    'engine_version',
    'release_status',
    'repository',
    'engine_owner_login',
    'rules_baseline',
    'schema_version',
    'campaign_update',
    'recommended_tag',
}
SHARED_FIELDS = (
    'engine_version',
    'release_status',
    'repository',
    'engine_owner_login',
    'rules_baseline',
    'schema_version',
    'recommended_tag',
)
RUNTIME_PACKAGE_FIELDS = {
    'schema_version',
    'engine_version',
    'package_id',
    'source_state',
    'source_ref',
    'source_commit_sha',
}
RUNTIME_PACKAGE_STATES = {'tagged', 'clean_head', 'dirty_worktree', 'non_git'}
# Presence checks only. Package composition recursively includes every valid file under GAME/.
REQUIRED_RUNTIME_ROOT_DIRS = ('CORE', 'INSTALL', 'RULES', 'SCHEMA', 'CAMPAIGN', 'TEMPLATE', 'MIGRATIONS', 'TOOLS')
LEGAL_TOP_LEVEL = ('LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md')
FORBIDDEN_JUNK_NAMES = {'.DS_Store'}
FORBIDDEN_JUNK_SUFFIXES = ('.pyc', '.pyo')


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_output_dir(repo_root: Path, output_dir: Path) -> Path:
    repo_root = repo_root.resolve()
    game_root = (repo_root / 'GAME').resolve()
    output_dir = output_dir.resolve()
    if _is_relative_to(output_dir, game_root):
        raise BuildError('release output directory must not be inside GAME')
    return output_dir


def validate_game_manifest_shape(data: dict) -> None:
    if not isinstance(data, dict):
        raise BuildError('GAME manifest must be a mapping')
    keys = set(data)
    if keys != GAME_FIELDS:
        extra = sorted(keys - GAME_FIELDS)
        missing = sorted(GAME_FIELDS - keys)
        raise BuildError(f'invalid GAME manifest fields; extra={extra} missing={missing}')
    campaign_update = data.get('campaign_update')
    if not isinstance(campaign_update, dict) or set(campaign_update) != {'compatibility'}:
        raise BuildError('GAME campaign_update must contain only compatibility')


def validate_runtime_package_metadata(data: dict) -> None:
    if not isinstance(data, dict):
        raise BuildError('RUNTIME_PACKAGE manifest must be a mapping')
    if set(data) != RUNTIME_PACKAGE_FIELDS:
        extra = sorted(set(data) - RUNTIME_PACKAGE_FIELDS)
        missing = sorted(RUNTIME_PACKAGE_FIELDS - set(data))
        raise BuildError(f'invalid RUNTIME_PACKAGE fields; extra={extra} missing={missing}')
    if data.get('schema_version') != 1:
        raise BuildError('RUNTIME_PACKAGE schema_version must be 1')
    state = data.get('source_state')
    if state not in RUNTIME_PACKAGE_STATES:
        raise BuildError(f'invalid RUNTIME_PACKAGE source_state: {state!r}')
    if not isinstance(data.get('engine_version'), str) or not data['engine_version']:
        raise BuildError('RUNTIME_PACKAGE engine_version must be a non-empty string')
    if not isinstance(data.get('package_id'), str) or not data['package_id']:
        raise BuildError('RUNTIME_PACKAGE package_id must be a non-empty string')
    source_ref = data.get('source_ref')
    source_sha = data.get('source_commit_sha')
    if state == 'tagged':
        if not isinstance(source_ref, str) or not source_ref:
            raise BuildError('tagged RUNTIME_PACKAGE requires source_ref')
        if not isinstance(source_sha, str) or not source_sha:
            raise BuildError('tagged RUNTIME_PACKAGE requires source_commit_sha')
    elif state == 'clean_head':
        if source_ref != 'HEAD':
            raise BuildError('clean_head RUNTIME_PACKAGE source_ref must be HEAD')
        if not isinstance(source_sha, str) or not source_sha:
            raise BuildError('clean_head RUNTIME_PACKAGE requires source_commit_sha')
    else:
        if source_sha is not None:
            raise BuildError(f'{state} RUNTIME_PACKAGE must not claim source_commit_sha')
        if source_ref is not None:
            raise BuildError(f'{state} RUNTIME_PACKAGE source_ref must be null')


def runtime_asset_name(tag: str) -> str:
    if not tag.startswith('v') or len(tag) < 2:
        raise BuildError(f'invalid release tag: {tag}')
    return f'hedgelion-dnd-master-runtime-{tag}.zip'


def _load_yaml(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise BuildError(f'cannot parse YAML {path}: {exc}') from exc
    if not isinstance(value, dict):
        raise BuildError(f'YAML root must be a mapping: {path}')
    return value


def load_and_validate_manifests(
    repo_root: Path,
    intended_tag: str | None = None,
    tag_mode: bool = False,
) -> tuple[dict, dict]:
    repo_root = repo_root.resolve()
    dev = _load_yaml(repo_root / 'DEV' / 'ENGINE_DEVELOPMENT.yaml')
    game = _load_yaml(repo_root / 'GAME' / 'ENGINE_VERSION.yaml')
    validate_game_manifest_shape(game)
    for key in SHARED_FIELDS:
        if dev.get(key) != game.get(key):
            raise BuildError(f'shared manifest field differs: {key}')
    if dev.get('campaign_update') != game.get('campaign_update'):
        raise BuildError('shared manifest field differs: campaign_update')
    if str(game.get('engine_version')) != '0.8' or game.get('recommended_tag') != 'v0.8':
        raise BuildError('engine 0.8 migration requires version 0.8 / tag v0.8')
    if intended_tag is not None and intended_tag != game.get('recommended_tag'):
        raise BuildError('intended tag differs from recommended_tag')
    if tag_mode and game.get('release_status') != 'ready-for-tag':
        raise BuildError('tag build requires release_status ready-for-tag')
    return dev, game


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ['git', *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _git_rev_parse(repo_root: Path, revision: str) -> str:
    cp = _run_git(repo_root, 'rev-parse', revision)
    if cp.returncode != 0:
        detail = cp.stderr.strip() or cp.stdout.strip() or f'exit {cp.returncode}'
        raise BuildError(f'cannot resolve Git revision {revision}: {detail}')
    value = cp.stdout.strip()
    if not value:
        raise BuildError(f'empty Git revision for {revision}')
    return value


def build_runtime_package_metadata(repo_root: Path, intended_tag: str, tag_mode: bool = False) -> dict:
    repo_root = repo_root.resolve()
    _dev, game = load_and_validate_manifests(
        repo_root,
        intended_tag=intended_tag,
        tag_mode=tag_mode,
    )
    version = str(game['engine_version'])
    release_status = game.get('release_status')
    development_package_id = f'dev-v{version}'

    if not (repo_root / '.git').exists():
        data = {
            'schema_version': 1,
            'engine_version': version,
            'package_id': development_package_id if release_status == 'development' else intended_tag,
            'source_state': 'non_git',
            'source_ref': None,
            'source_commit_sha': None,
        }
        validate_runtime_package_metadata(data)
        return data

    if tag_mode:
        tag_ref = f'refs/tags/{intended_tag}'
        tag_commit = _git_rev_parse(repo_root, f'{tag_ref}^{{commit}}')
        head_commit = _git_rev_parse(repo_root, 'HEAD')
        if tag_commit != head_commit:
            raise BuildError(
                f'tag-mode package must be built from exact tagged commit: '
                f'{intended_tag}={tag_commit} HEAD={head_commit}'
            )
        data = {
            'schema_version': 1,
            'engine_version': version,
            'package_id': intended_tag,
            'source_state': 'tagged',
            'source_ref': intended_tag,
            'source_commit_sha': tag_commit,
        }
        validate_runtime_package_metadata(data)
        return data

    status = _run_git(repo_root, 'status', '--porcelain', '--untracked-files=normal')
    if status.returncode != 0:
        detail = status.stderr.strip() or status.stdout.strip() or f'exit {status.returncode}'
        raise BuildError(f'cannot inspect Git worktree state: {detail}')
    package_id = development_package_id if release_status == 'development' else intended_tag
    if status.stdout.strip():
        data = {
            'schema_version': 1,
            'engine_version': version,
            'package_id': package_id,
            'source_state': 'dirty_worktree',
            'source_ref': None,
            'source_commit_sha': None,
        }
    else:
        data = {
            'schema_version': 1,
            'engine_version': version,
            'package_id': package_id,
            'source_state': 'clean_head',
            'source_ref': 'HEAD',
            'source_commit_sha': _git_rev_parse(repo_root, 'HEAD'),
        }
    validate_runtime_package_metadata(data)
    return data


def _runtime_package_yaml_bytes(data: dict) -> bytes:
    validate_runtime_package_metadata(data)
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).encode('utf-8')


def validate_tag_lineage(repo_root: Path) -> None:
    repo_root = repo_root.resolve()
    if not (repo_root / ".git").exists():
        raise BuildError("tag-mode release build requires a Git checkout for lineage validation")
    cp = subprocess.run(
        ["git", "merge-base", "--is-ancestor", "HEAD", "origin/main"],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if cp.returncode != 0:
        raise BuildError("tagged commit is not on the approved main release lineage")


def _git_commit_datetime(repo_root: Path, revision: str) -> datetime:
    cp = subprocess.run(
        ["git", "show", "-s", "--format=%cI", revision],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if cp.returncode != 0:
        detail = cp.stderr.strip() or cp.stdout.strip() or f'exit {cp.returncode}'
        raise BuildError(f'cannot read Git commit date for {revision}: {detail}')
    raw = cp.stdout.strip()
    try:
        value = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise BuildError(f'invalid Git commit date for {revision}: {raw!r}') from exc
    if value.tzinfo is None:
        raise BuildError(f'Git commit date has no timezone for {revision}: {raw!r}')
    return value


def resolve_archive_datetime(repo_root: Path, intended_tag: str) -> datetime:
    """Choose stable human-meaningful ZIP time: tagged commit when present, otherwise HEAD."""
    repo_root = repo_root.resolve()
    if (repo_root / '.git').exists():
        tag_ref = f'refs/tags/{intended_tag}'
        probe = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", tag_ref],
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if probe.returncode == 0:
            return _git_commit_datetime(repo_root, f'{tag_ref}^{{commit}}')
        if probe.returncode != 1:
            detail = probe.stderr.strip() or probe.stdout.strip() or f'exit {probe.returncode}'
            raise BuildError(f'cannot inspect Git tag {intended_tag}: {detail}')
        return _git_commit_datetime(repo_root, 'HEAD')

    # Direct unit-test/minimal-fixture builds may not be Git checkouts. Production CLI builds are.
    game_root = repo_root / 'GAME'
    mtimes = [path.stat().st_mtime for path, _rel in _iter_game_files(game_root)]
    if not mtimes:
        raise BuildError('cannot derive archive timestamp outside Git: GAME contains no files')
    return datetime.fromtimestamp(max(mtimes)).astimezone()


def _zip_timestamp_fields(value: datetime) -> tuple[tuple[int, int, int, int, int, int], bytes]:
    if value.tzinfo is None:
        raise BuildError('archive timestamp must include timezone information')
    if value.year < 1980 or value.year > 2107:
        raise BuildError(f'archive timestamp is outside ZIP date range: {value.isoformat()}')

    # Classic ZIP/DOS timestamp has two-second precision. Preserve it for broad reader
    # compatibility and also write the standard Extended Timestamp extra field with the
    # full one-second Unix mtime so a one-second commit-date change still changes ZIP bytes.
    dos_time = (
        value.year,
        value.month,
        value.day,
        value.hour,
        value.minute,
        value.second - (value.second % 2),
    )
    epoch = int(value.timestamp())
    if epoch < 0 or epoch > 0xFFFFFFFF:
        raise BuildError(f'archive timestamp cannot be represented as Unix ZIP mtime: {value.isoformat()}')
    extended = struct.pack('<HHBI', 0x5455, 5, 0x01, epoch)
    return dos_time, extended


def validate_extracted_package_root(root: Path) -> Path:
    root = root.resolve()
    if not (root / 'ENGINE_VERSION.yaml').is_file():
        raise BuildError('not a flattened HDM runtime package root')
    if not (root / 'RUNTIME_PACKAGE.yaml').is_file():
        raise BuildError('runtime package provenance marker is missing')
    try:
        validate_runtime_package_metadata(_load_yaml(root / 'RUNTIME_PACKAGE.yaml'))
    except BuildError as exc:
        raise BuildError(f'invalid runtime package provenance: {exc}') from exc
    if not all((root / p).is_dir() for p in REQUIRED_RUNTIME_ROOT_DIRS):
        raise BuildError('not a flattened HDM runtime package root')
    if (root / 'GAME').exists() or (root / 'DEV').exists():
        raise BuildError('source repository layout is not an installable runtime package')
    return root


def _iter_game_files(game_root: Path):
    casefold_seen: dict[str, str] = {}
    for path in sorted(game_root.rglob('*'), key=lambda p: p.relative_to(game_root).as_posix()):
        rel = path.relative_to(game_root).as_posix()
        folded = rel.casefold()
        previous = casefold_seen.setdefault(folded, rel)
        if previous != rel:
            raise BuildError(f'case-insensitive path collision: {previous} vs {rel}')
        if path.is_symlink():
            raise BuildError(f'symlink is not allowed in GAME: {rel}')
        if path.is_dir():
            if path.name in {'__pycache__', '.pytest_cache'}:
                raise BuildError(f'build/test cache is not allowed in GAME: {rel}')
            continue
        if path.name in FORBIDDEN_JUNK_NAMES or path.suffix in FORBIDDEN_JUNK_SUFFIXES or path.suffix == '.zip':
            raise BuildError(f'build junk is not allowed in GAME: {rel}')
        yield path, rel


def _relative_file_set(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob('*')
        if path.is_file()
    }


def validate_legal_copies(repo_root: Path) -> None:
    repo_root = repo_root.resolve()
    game_root = repo_root / 'GAME'

    observed_legal = (
        (repo_root / '.git').exists()
        or (repo_root / 'AGENTS.md').is_file()
        or any((repo_root / name).exists() or (game_root / name).exists() for name in LEGAL_TOP_LEVEL)
        or (repo_root / 'LICENSES').exists()
        or (game_root / 'LICENSES').exists()
    )
    if not observed_legal:
        # Minimal unit-test fixtures may intentionally omit distribution metadata.
        return

    for name in LEGAL_TOP_LEVEL:
        canonical = repo_root / name
        distribution = game_root / name
        if not canonical.is_file() or not distribution.is_file():
            raise BuildError(f'missing canonical/distribution legal file: {name}')
        if canonical.read_bytes() != distribution.read_bytes():
            raise BuildError(f'GAME/{name} differs from root canonical copy')

    canonical_licenses = repo_root / 'LICENSES'
    distribution_licenses = game_root / 'LICENSES'
    if not canonical_licenses.is_dir() or not distribution_licenses.is_dir():
        raise BuildError('root LICENSES/ and GAME/LICENSES/ must both exist')

    canonical_files = _relative_file_set(canonical_licenses)
    distribution_files = _relative_file_set(distribution_licenses)
    if canonical_files != distribution_files:
        raise BuildError(
            'GAME/LICENSES file set differs from root canonical LICENSES; '
            f'root_only={sorted(canonical_files - distribution_files)} '
            f'game_only={sorted(distribution_files - canonical_files)}'
        )
    for rel in sorted(canonical_files):
        if (canonical_licenses / rel).read_bytes() != (distribution_licenses / rel).read_bytes():
            raise BuildError(f'GAME/LICENSES/{rel} differs from root canonical copy')


def validate_package_markdown(source_path: Path, game_root: Path) -> None:
    src = source_path.read_text(encoding='utf-8')
    game_root = game_root.resolve()
    for raw in MARKDOWN_LINK_RE.findall(src):
        raw = raw.strip()
        if not raw or _is_external_link(raw):
            continue
        target = raw.split('#', 1)[0].strip()
        if not target:
            continue
        if target.startswith('<') and target.endswith('>'):
            target = target[1:-1]
        target = target.replace('\\', '/')
        candidate = (source_path.parent / target).resolve()
        if not _is_relative_to(candidate, game_root):
            raise BuildError(f'{source_path}: package link escapes GAME root: {target}')
        if not candidate.exists():
            raise BuildError(f'{source_path}: unresolved package link: {target}')


def validate_source_tree(repo_root: Path) -> None:
    repo_root = repo_root.resolve()
    game_root = repo_root / 'GAME'
    for d in REQUIRED_RUNTIME_ROOT_DIRS:
        if not (game_root / d).is_dir():
            raise BuildError(f'missing required GAME directory: {d}')
    if (game_root / 'TEMPLATE/CAMPAIGN_MANIFEST.yaml').exists():
        raise BuildError('deprecated TEMPLATE/CAMPAIGN_MANIFEST.yaml must be absent')
    if (game_root / 'RUNTIME_PACKAGE.yaml').exists():
        raise BuildError('RUNTIME_PACKAGE.yaml is builder-generated and must not be tracked under GAME')
    validate_legal_copies(repo_root)
    validate_project_instructions_parity(game_root / 'INSTALL')

    campaign_files = {
        p.relative_to(game_root / 'CAMPAIGN').as_posix()
        for p in (game_root / 'CAMPAIGN').rglob('*') if p.is_file()
    }
    campaign_readme = game_root / 'CAMPAIGN/README.md'
    if campaign_readme.is_file():
        validate_destination_markdown(
            campaign_readme,
            destination_root_files=campaign_files,
            destination_rel='README.md',
        )
    storage_readme = game_root / 'TEMPLATE/STORAGE_README.md'
    if storage_readme.is_file():
        validate_destination_markdown(
            storage_readme,
            destination_root_files={'README.md', 'DND_STORAGE.yaml'},
            destination_rel='README.md',
        )

    destination_sources = {campaign_readme.resolve(), storage_readme.resolve()}
    for path in sorted(game_root.rglob('*.md')):
        if path.resolve() in destination_sources:
            continue
        validate_package_markdown(path, game_root)


def _write_zip_member(
    zf: zipfile.ZipFile,
    *,
    name: str,
    data: bytes,
    zip_time: tuple[int, int, int, int, int, int],
    zip_extra: bytes,
    mode: int,
) -> None:
    info = zipfile.ZipInfo(name, date_time=zip_time)
    info.create_system = 3
    info.extra = zip_extra
    info.external_attr = (stat.S_IFREG | mode) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_runtime_zip(
    repo_root: Path,
    output_dir: Path,
    intended_tag: str,
    tag_mode: bool = False,
) -> Path:
    repo_root = repo_root.resolve()
    game_root = repo_root / 'GAME'
    output_dir = validate_output_dir(repo_root, output_dir)
    load_and_validate_manifests(
        repo_root,
        intended_tag=intended_tag,
        tag_mode=tag_mode,
    )
    validate_source_tree(repo_root)
    package_metadata = build_runtime_package_metadata(repo_root, intended_tag, tag_mode=tag_mode)
    package_metadata_bytes = _runtime_package_yaml_bytes(package_metadata)
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / runtime_asset_name(intended_tag)
    tmp = target.with_suffix(target.suffix + '.tmp')
    files = list(_iter_game_files(game_root))
    archive_datetime = resolve_archive_datetime(repo_root, intended_tag)
    zip_time, zip_extra = _zip_timestamp_fields(archive_datetime)
    with zipfile.ZipFile(tmp, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in files:
            _write_zip_member(
                zf,
                name=rel,
                data=path.read_bytes(),
                zip_time=zip_time,
                zip_extra=zip_extra,
                mode=0o755 if os.access(path, os.X_OK) else 0o644,
            )
        _write_zip_member(
            zf,
            name='RUNTIME_PACKAGE.yaml',
            data=package_metadata_bytes,
            zip_time=zip_time,
            zip_extra=zip_extra,
            mode=0o644,
        )
    tmp.replace(target)
    return target


def write_sha256(path: Path) -> Path:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    sidecar = path.with_suffix(path.suffix + '.sha256')
    sidecar.write_text(f'{digest}  {path.name}\n', encoding='utf-8')
    return sidecar


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _normalize_text(value: str) -> str:
    return value.replace('\r\n', '\n').replace('\r', '\n').strip() + '\n'


def validate_project_instructions_parity(install_dir: Path) -> None:
    canonical_path = install_dir / 'PROJECT_INSTRUCTIONS.txt'
    readme_path = install_dir / 'README.md'
    canonical = _normalize_text(canonical_path.read_text(encoding='utf-8'))
    readme = readme_path.read_text(encoding='utf-8')
    blocks = re.findall(r"```text\n(.*?)\n```", readme, flags=re.S)
    if len(blocks) != 1:
        raise BuildError('INSTALL/README.md must contain exactly one text Project Instructions block')
    embedded = _normalize_text(blocks[0])
    if canonical != embedded:
        raise BuildError('embedded Project Instructions differ from PROJECT_INSTRUCTIONS.txt')


def _is_external_link(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(('http://', 'https://', 'mailto:', 'tel:')) or target.startswith('#')


def validate_destination_markdown(
    source_path: Path,
    *,
    destination_root_files: set[str],
    destination_rel: str,
) -> None:
    src = source_path.read_text(encoding='utf-8')
    for source_prefix in ('GAME/', 'DEV/', 'TEMPLATE/'):
        if source_prefix in src:
            raise BuildError(
                f'{source_path}: destination text leaks source prefix: {source_prefix}'
            )
    base = Path(destination_rel).parent
    for raw in MARKDOWN_LINK_RE.findall(src):
        target = raw.strip().split('#', 1)[0]
        if not target or _is_external_link(raw.strip()):
            continue
        target = target.replace('\\', '/')
        if target.startswith(('GAME/', 'DEV/')):
            raise BuildError(f'{source_path}: destination link leaks source prefix: {target}')
        candidate = (base / target).as_posix()
        normalized = Path(candidate)
        if normalized.is_absolute() or '..' in normalized.parts:
            raise BuildError(f'{source_path}: destination link escapes root: {target}')
        normalized_rel = normalized.as_posix().lstrip('./')
        if normalized_rel not in destination_root_files:
            raise BuildError(f'{source_path}: unresolved destination link: {target}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--tag")
    parser.add_argument("--output", required=True)
    parser.add_argument("--tag-mode", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    dev, _game = load_and_validate_manifests(
        repo_root,
        intended_tag=args.tag,
        tag_mode=args.tag_mode,
    )
    intended_tag = args.tag if args.tag is not None else dev.get('recommended_tag')
    if not isinstance(intended_tag, str) or not intended_tag:
        raise BuildError('DEV/ENGINE_DEVELOPMENT.yaml must define recommended_tag')
    if args.tag_mode:
        validate_tag_lineage(repo_root)
    runtime_zip = build_runtime_zip(
        repo_root,
        Path(args.output),
        intended_tag,
        tag_mode=args.tag_mode,
    )
    sha256_file = write_sha256(runtime_zip)
    print(json.dumps({
        "asset_name": runtime_zip.name,
        "runtime_zip": str(runtime_zip),
        "sha256_file": str(sha256_file),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
