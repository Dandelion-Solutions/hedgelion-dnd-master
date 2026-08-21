from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


class PreparationError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code


def venv_python_path(venv_dir: Path) -> Path:
    return venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def compute_fingerprint(requirements_path: Path, python_version: tuple[int, int]) -> dict[str, str]:
    return {
        "requirements_sha256": hashlib.sha256(requirements_path.read_bytes()).hexdigest(),
        "python": f"{python_version[0]}.{python_version[1]}",
    }


def load_fingerprint(path: Path) -> dict[str, str] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
        return None
    return value


def cache_is_current(venv_dir: Path, fingerprint_path: Path, expected: dict[str, str]) -> bool:
    py = venv_python_path(venv_dir)
    return py.is_file() and os.access(py, os.X_OK) and load_fingerprint(fingerprint_path) == expected


def ensure_environment(
    repo_root: Path,
    *,
    python_version: tuple[int, int] | None = None,
    builder_factory=venv.EnvBuilder,
    runner=subprocess.run,
) -> Path:
    repo_root = repo_root.resolve()
    requirements = repo_root / "DEV/TOOLS/requirements-dev-tools.txt"
    version = python_version or (sys.version_info.major, sys.version_info.minor)
    try:
        expected = compute_fingerprint(requirements, version)
    except OSError as exc:
        raise PreparationError(f"cannot read DEV/TOOLS/requirements-dev-tools.txt: {exc}") from exc
    cache = repo_root / ".hdm-devtools"
    venv_dir = cache / "venv"
    fingerprint_path = cache / "fingerprint.json"
    if cache_is_current(venv_dir, fingerprint_path, expected):
        return venv_python_path(venv_dir)
    cache.mkdir(parents=True, exist_ok=True)
    fingerprint_path.unlink(missing_ok=True)
    if venv_dir.exists(): shutil.rmtree(venv_dir)
    try:
        builder_factory(with_pip=True, clear=True).create(venv_dir)
    except Exception as exc:
        raise PreparationError(f"virtual environment creation failed: {exc}") from exc
    python = venv_python_path(venv_dir)
    env = os.environ.copy()
    env.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PIP_RETRIES": "1",
        "PIP_CACHE_DIR": str(cache / "pip-cache"),
    })
    cp = runner([str(python), "-m", "pip", "install", "-r", str(requirements)], cwd=repo_root, env=env)
    if cp.returncode != 0:
        raise PreparationError(f"DEV tool dependency installation failed (exit {cp.returncode})", cp.returncode)
    tmp = fingerprint_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(expected, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(fingerprint_path)
    return python
