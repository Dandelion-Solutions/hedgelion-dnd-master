from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "GAME"
SCHEMA = GAME / "SCHEMA"
CAMPAIGN = GAME / "CAMPAIGN"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class HouseRulesPolicyAuthorityContractTests(unittest.TestCase):
    def test_creator_authority_is_not_moved_into_manifest(self):
        schema = load_yaml(SCHEMA / "campaign_manifest.schema.yaml")
        self.assertNotIn("creator", schema["fields"])
        self.assertTrue(
            any("creator" in value and "MUST NOT be duplicated" in value for value in schema["invariants"])
        )

    def test_player_binding_has_only_narrow_mechanical_override_grant(self):
        schema = load_yaml(SCHEMA / "player.schema.yaml")
        policy_authority = schema["fields"]["policy_authority"]
        self.assertEqual(policy_authority["mechanical_override_policy"], "boolean|null")
        self.assertNotIn("interpretive_policy", policy_authority)
        joined = "\n".join(schema["invariants"])
        self.assertIn("missing/null mechanical_override_policy means false", joined)
        self.assertIn("campaign creator", joined)
        self.assertIn("active PLAYER", joined)
        self.assertIn("self-grant", joined)
        self.assertIn("HARD access-control", joined)

    def test_structured_sidecar_is_narrow_identity_currentness_evidence(self):
        schema = load_yaml(SCHEMA / "house_rules_policy.schema.yaml")
        self.assertEqual(schema["schema_name"], "house_rules_policy")
        self.assertEqual(schema["required"], ["schema_version", "source_path", "policies"])
        item = schema["fields"]["policies"]["item"]
        self.assertEqual(item["policy_id"], "string")
        self.assertEqual(
            item["authority_class"],
            "enum[INTERPRETIVE_POLICY, MECHANICAL_OVERRIDE_POLICY]",
        )
        self.assertEqual(item["kind"], "enum[house_rule, ruling]")
        self.assertEqual(item["lifecycle"], "enum[active, superseded, retired]")
        self.assertEqual(item["source_anchor"], "string")
        self.assertEqual(
            item["adoption_basis"],
            "enum[campaign_creator, active_player_interpretive, creator_delegated_mechanical_override]",
        )
        self.assertEqual(item["adopted_by_player_id"], "string|null")
        self.assertEqual(item["realization_refs"], "array[string]")
        self.assertNotIn("capability_refs", item)
        self.assertNotIn("normative_text", item)
        joined = "\n".join(schema["invariants"])
        self.assertIn("campaign revision", joined)
        self.assertIn("not a global policy epoch", joined)
        self.assertIn("routing-only", joined)
        self.assertIn("exactly one current sidecar entry", joined)
        self.assertIn("unindexed normative prose", joined)

    def test_campaign_template_contains_empty_sidecar_without_manifest_rewrite(self):
        template = load_yaml(CAMPAIGN / "RULES" / "HOUSE_RULES.yaml")
        self.assertEqual(template["schema_version"], 1)
        self.assertEqual(template["source_path"], "RULES/HOUSE_RULES.md")
        self.assertEqual(template["policies"], [])

        manifest = load_yaml(CAMPAIGN / "MANIFEST.yaml")
        self.assertEqual(manifest["rules"]["house_rules_path"], "RULES/HOUSE_RULES.md")
        self.assertNotIn("creator", manifest)

    def test_runtime_policy_laws_distinguish_adoption_and_refresh_notification(self):
        access = (ROOT / "DEV" / "ARCHITECTURE" / "ACCESS_CONTROL.md").read_text(encoding="utf-8")
        house_rules = (CAMPAIGN / "RULES" / "HOUSE_RULES.md").read_text(encoding="utf-8")
        session_schema = load_yaml(SCHEMA / "session.schema.yaml")

        for text in (access, house_rules):
            self.assertIn("INTERPRETIVE_POLICY", text)
            self.assertIn("MECHANICAL_OVERRIDE_POLICY", text)

        self.assertIn("policy_authority.mechanical_override_policy", access)
        self.assertIn("changed-path", house_rules)
        self.assertIn("realization_refs", house_rules)
        self.assertIn("unindexed", house_rules.lower())
        self.assertIn("конец", house_rules.lower())
        self.assertIn("background", house_rules.lower())
        self.assertIn("base_head_sha", session_schema["fields"])
        self.assertNotIn("policy_notification_cursor", session_schema["fields"])


if __name__ == "__main__":
    unittest.main()
