import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class CurrentProgressAuthorityTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding='utf-8')

    def test_single_global_authority_has_closed_shape_and_bootstrap_routes(self):
        progress = self.read('DEV/CURRENT_PROGRESS.md')
        for marker in (
            'Status: **CANONICAL GLOBAL CURRENT-PROGRESS AUTHORITY**',
            'GLOBAL_PROGRAM:', 'GLOBAL_STATE:', 'CURRENT_WORKSTREAM:',
            'CURRENT_SLICE:', 'LAST_CLOSED_UNIT:', 'NEXT_AUTHORIZED_UNIT:',
            'REQUIRED_GATE:', 'TASK_LOCAL_CURSOR:', 'KNOWN_BLOCKERS:',
        ):
            self.assertIn(marker, progress)

        for relative in (
            'AGENTS.md', 'DEV/PROJECT_MAP.md', 'DEV/DESIGN_PROCESS.md',
            'DEV/ARCHITECTURE/DESIGN_PROCESS.md',
            'DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md',
            'DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md',
        ):
            self.assertIn('DEV/CURRENT_PROGRESS.md', self.read(relative))

    def test_old_live_surfaces_do_not_claim_global_current_progress(self):
        roadmap = self.read('DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md')
        index = self.read('DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md')
        cursor = self.read('DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md')

        self.assertIn('NOT CURRENT-PROGRESS AUTHORITY', roadmap)
        self.assertNotIn('This file is the sequencing/status authority', roadmap)
        self.assertNotIn('## 8. R2.7 current status', roadmap)
        self.assertNotIn('## 9. Current continuation point', roadmap)
        self.assertNotIn('Architecture state:', index)
        self.assertIn('TASK-LOCAL R2.7 AUDIT CURSOR — NOT GLOBAL CURRENT-PROGRESS AUTHORITY', cursor)


if __name__ == '__main__':
    unittest.main()
