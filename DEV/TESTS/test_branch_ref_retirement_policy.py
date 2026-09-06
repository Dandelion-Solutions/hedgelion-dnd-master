from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
AMENDMENT = ROOT / "DEV/docs/superpowers/specs/2026-09-06-step-5-13-logical-ref-retirement-canonical-amendment.md"
OWNER = ROOT / "DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md"


class BranchRefRetirementPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amendment = AMENDMENT.read_text(encoding="utf-8")
        cls.owner = OWNER.read_text(encoding="utf-8")

    def test_current_amendment_excludes_physical_ref_deletion_automation(self):
        self.assertIn("HDM AUTOMATION NEVER DELETES GIT BRANCHES/REFS", self.amendment)
        self.assertIn("MUST NOT design, capability-probe, invoke, retry", self.amendment)
        self.assertIn("There is no `RepositoryPort.DeleteRef` debt", self.amendment)
        self.assertNotIn("CAPABILITY_DEFERRED because DeleteRef is missing", self.owner)

    def test_retirement_is_logical_and_physical_ref_is_nonauthoritative(self):
        self.assertIn("REF RETIREMENT IS LOGICAL RETIREMENT", self.amendment)
        self.assertIn("Physical ref existence does not imply authority", self.amendment)
        self.assertIn("may remain physically present indefinitely", self.amendment)

    def test_no_manual_or_out_of_band_delete_fallback(self):
        self.assertIn("manual operator action or any out-of-band deletion fallback", self.amendment)
        self.assertIn("no manual/native-Git/private-HTTP/out-of-band deletion fallback", self.amendment)

    def test_physical_presence_cannot_reactivate_old_authority(self):
        self.assertIn("STALE HOST CANNOT RECREATE OLD AUTHORITY", self.amendment)
        self.assertIn("may not adopt or recreate the old epoch", self.amendment)


if __name__ == "__main__":
    unittest.main()
