"""Real installed compiler setup for structural consumers; no issuer bypass."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_installed_structural_test(test_id: str) -> subprocess.CompletedProcess[str]:
    from DEV.TESTS.test_local_spell_catalog import _stage_clean_source_tree
    from DEV.TOOLS.release_builder import (
        build_runtime_zip,
        validate_extracted_package_root,
    )

    with tempfile.TemporaryDirectory(prefix="sp02-structural-installed-") as temporary:
        parent = Path(temporary)
        source = parent / "source"
        source.mkdir()
        _stage_clean_source_tree(source)
        archive = build_runtime_zip(source, parent / "build", intended_tag="v1.0-alpha")
        installed = parent / "GAME"
        installed.mkdir()
        with zipfile.ZipFile(archive) as runtime_zip:
            runtime_zip.extractall(installed)
        validate_extracted_package_root(installed)
        environment = os.environ.copy()
        environment["HDM_INSTALLED_STRUCTURAL_TEST"] = str(installed)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONPATH"] = os.pathsep.join((str(parent), str(ROOT)))
        return subprocess.run([sys.executable, "-m", "unittest", test_id, "-q"],
            cwd=parent, env=environment, text=True, capture_output=True, check=False)


def authentic_generic_catalog():
    """Use the loaded complete package's actual public binder/compiler route."""
    from GAME.TOOLS import activity_runtime, catalog_runtime, ruleset_package

    source = catalog_runtime.load_activity_compiler_contract_source()
    expected_root = Path(os.environ["HDM_INSTALLED_STRUCTURAL_TEST"]).resolve()
    assert source.runtime_root == expected_root
    assert Path(activity_runtime.__file__).resolve().parent == expected_root / "TOOLS"
    package_id = "hdm.rules.dnd2024-srd52-core"
    package_root = expected_root / "RULES/packages" / package_id
    lock, snapshots = ruleset_package.build_resolved_lock([package_root],
        root_package_ids=[package_id], engine_version="1.0-alpha", catalog_generation=2)
    identities = ("activity.check.generic", "activity.save.generic")
    request = {
        "basis": {"catalog_generation": 2, "engine_version": "1.0-alpha",
            "engine_contract_inventory": catalog_runtime._thaw(source.engine_contract_inventory),
            "engine_contract_inventory_sha256": source.engine_contract_inventory["inventory_sha256"],
            "ruleset_lock": lock, "natural_owner_evidence": [],
            "campaign_definition_frontier": {"frontier_id": "campaign.definitions",
                "state_revision": 1, "definition_ids": list(identities)}},
        "definition_dependencies": [{"source_type": "ruleset_package", "definition_id": identity,
            "kind": "definition.activity", "package_id": package_id,
            "package_content_sha256": lock["packages"][0]["content_sha256"]} for identity in identities],
    }
    return activity_runtime.admit_activity_catalog(request, package_snapshots=snapshots,
        engine_contract_inventory_source=source, natural_owner_sources={}, compiler_generation=1,
        mode_policy_profile_id="execution.spell_cast.srd521")
