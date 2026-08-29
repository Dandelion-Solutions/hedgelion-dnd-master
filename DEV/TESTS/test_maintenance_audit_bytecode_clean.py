from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class MaintenanceAuditBytecodeCleanTests(unittest.TestCase):
    def test_audit_and_nested_validators_do_not_create_game_bytecode(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tools = root / "DEV/TOOLS"
            game_tools = root / "GAME/TOOLS"
            tools.mkdir(parents=True)
            game_tools.mkdir(parents=True)
            shutil.copy2(ROOT / "DEV/TOOLS/run_maintenance_audit", tools / "run_maintenance_audit")
            (tools / "dev_tool_environment.py").write_text(
                "import sys\nfrom pathlib import Path\n"
                "class PreparationError(Exception):\n    exit_code = 1\n"
                "def ensure_environment(_root): return Path(sys.executable)\n",
                encoding="utf-8",
            )
            (tools / "audit_engine.py").write_text(
                "import subprocess, sys\nfrom pathlib import Path\n"
                "sys.path.insert(0, str(Path(__file__).resolve().parents[2]))\n"
                "import GAME.TOOLS.audit_probe\n"
                "subprocess.run([sys.executable, '-c', 'import GAME.TOOLS.validator_probe'], "
                "cwd=Path(__file__).resolve().parents[2], check=True)\n",
                encoding="utf-8",
            )
            (game_tools / "audit_probe.py").write_text("VALUE = 1\n", encoding="utf-8")
            (game_tools / "validator_probe.py").write_text("VALUE = 2\n", encoding="utf-8")
            env = os.environ.copy()
            env.pop("PYTHONDONTWRITEBYTECODE", None)
            completed = subprocess.run(
                [sys.executable, str(tools / "run_maintenance_audit")],
                cwd=root, env=env, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = [
                path.relative_to(root).as_posix()
                for path in (root / "GAME").rglob("*")
                if path.name == "__pycache__" or path.suffix == ".pyc"
            ]
            self.assertEqual(generated, [])


if __name__ == "__main__":
    unittest.main()
