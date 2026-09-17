from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from DEV.TOOLS.validate_domain_rules_coverage import initialize_combat_procedure
from GAME.TOOLS.recovery_roots import (
    AcceptedUnresolvedInputPromise,
    OperationalRoot,
    OperationalRootCompletenessError,
    OperationalRootError,
    OperationalRootDelta,
    derive_operational_root_delta,
    enumerate_operational_root_page,
    validate_operational_root_delta,
)
from GAME.TOOLS.native_storage import route_native_record


ROOT = Path(__file__).resolve().parents[2]


def _procedure_owner(*, procedure_id: str = "procedure-000001", lifecycle: str = "ACTIVE") -> dict[str, object]:
    state = initialize_combat_procedure(["actor-1"], ["actor-1"])
    state["lifecycle"] = lifecycle
    if lifecycle == "TERMINAL":
        state["lifecycle_state"] = "terminated"
    return {"kind": "runtime.procedure", "id": procedure_id, "revision": 1, "state": state}


def _command_owner(*, command_id: str = "command-000001") -> dict[str, object]:
    return {
        "kind": "runtime.command",
        "schema_version": 3,
        "command_id": command_id,
        "disposition": "command.accepted",
        "pending_child_invocations": [
            {
                "firing_key": "event-1:binding-1",
                "root_command_id": command_id,
                "activity_id": "activity.followup",
                "trigger_ref": "event-1",
                "reason": "mandatory_followup",
            }
        ],
    }


class OperationalRootEnrollmentTests(unittest.TestCase):
    def test_active_procedure_enrollment_is_idempotent(self) -> None:
        owner = _procedure_owner()

        first = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=owner,
        )
        again = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=owner,
            existing_roots=(first.root,),
        )

        self.assertEqual(first.action, "ENROLL")
        self.assertEqual(again.action, "NOOP")
        self.assertEqual(first.root.owner_kind, "runtime.procedure")
        self.assertEqual(first.root.owner_id, "procedure-000001")

    def test_exact_kind_and_identity_rejects_same_kind_different_id(self) -> None:
        owner = _procedure_owner()
        delta = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=owner,
        )
        different_owner = _procedure_owner(procedure_id="procedure-000002")

        with self.assertRaisesRegex(OperationalRootError, "identity"):
            validate_operational_root_delta(delta, native_owner=different_owner)

    def test_forged_carrier_cannot_supply_native_lifecycle_or_removal(self) -> None:
        owner = _procedure_owner()
        delta = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=owner,
        )
        forged_root = OperationalRoot(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            owner_id="procedure-000001",
            relative_path=delta.root.relative_path,
        )
        with self.assertRaisesRegex(OperationalRootError, "native owner"):
            derive_operational_root_delta(
                campaign_id="campaign-1",
                owner_kind="runtime.procedure",
                native_owner=forged_root,
            )

        forged_removal = OperationalRootDelta(
            campaign_id="campaign-1",
            action="REMOVE",
            root=delta.root,
            reason="caller_asserted_terminal",
        )
        with self.assertRaisesRegex(OperationalRootError, "eligible"):
            validate_operational_root_delta(forged_removal, native_owner=owner)

    def test_terminal_procedure_prepares_removal_delta_without_publication(self) -> None:
        active = _procedure_owner()
        enrolled = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=active,
        )
        terminal = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=_procedure_owner(lifecycle="TERMINAL"),
            existing_roots=(enrolled.root,),
        )

        self.assertEqual(terminal.action, "REMOVE")
        self.assertEqual(terminal.root, enrolled.root)
        self.assertEqual(terminal.reason, "native_lifecycle_terminal")

    def test_caller_built_terminal_removal_lacks_native_state_evidence(self) -> None:
        terminal_owner = _procedure_owner(lifecycle="TERMINAL")
        root = OperationalRoot(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            owner_id="procedure-000001",
            relative_path=route_native_record(
                "runtime.procedure", ("procedure-000001",)
            ).relative_path,
        )
        forged_removal = OperationalRootDelta(
            campaign_id="campaign-1",
            action="REMOVE",
            root=root,
            reason="caller_asserted_terminal",
        )
        with self.assertRaisesRegex(OperationalRootError, "state evidence"):
            validate_operational_root_delta(forged_removal, native_owner=terminal_owner)

    def test_runtime_command_requires_unfinished_mandatory_closure(self) -> None:
        accepted = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.command",
            native_owner=_command_owner(),
        )
        settled_owner = _command_owner(command_id="command-000002")
        settled_owner["disposition"] = "command.settled"
        settled_owner["pending_child_invocations"] = []
        settled = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.command",
            native_owner=settled_owner,
        )

        self.assertEqual(accepted.action, "ENROLL")
        self.assertEqual(settled.action, "NOOP")

    def test_unresolved_input_requires_later_owner_promise(self) -> None:
        interaction = {
            "kind": "runtime.interaction",
            "campaign_id": "campaign-1",
            "session_id": "session-1",
            "player_id": "player-1",
            "input_message_id": "message-1",
            "intent_plan_id": "plan-1",
        }
        with self.assertRaisesRegex(OperationalRootError, "promise"):
            derive_operational_root_delta(
                campaign_id="campaign-1",
                owner_kind="runtime.interaction",
                native_owner=interaction,
            )

        promise = AcceptedUnresolvedInputPromise(
            campaign_id="campaign-1",
            owner_kind="runtime.interaction",
            owner_id="message-1",
            promise_id="promise-1",
        )
        delta = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.interaction",
            native_owner=interaction,
            accepted_promise=promise,
        )
        self.assertEqual(delta.action, "ENROLL")
        validate_operational_root_delta(delta, native_owner=interaction, accepted_promise=promise)

    def test_enumeration_requires_complete_native_input_and_never_scans(self) -> None:
        with self.assertRaises(OperationalRootError):
            enumerate_operational_root_page("campaign-1", None)
        with self.assertRaises(OperationalRootCompletenessError):
            enumerate_operational_root_page(
                "campaign-1", [_procedure_owner()], complete=False
            )

        page = enumerate_operational_root_page(
            "campaign-1", [_procedure_owner()], complete=True
        )
        self.assertTrue(page.complete)
        self.assertEqual(len(page.roots), 1)
        schema = json.loads(
            (ROOT / "DEV" / "SCHEMAS" / "operational-root-routing.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(page.to_dict())

    def test_delta_validation_rejects_tampered_identity(self) -> None:
        owner = _procedure_owner()
        delta = derive_operational_root_delta(
            campaign_id="campaign-1",
            owner_kind="runtime.procedure",
            native_owner=owner,
        )
        tampered = replace(
            delta,
            root=OperationalRoot(
                campaign_id="campaign-1",
                owner_kind="runtime.procedure",
                owner_id="procedure-other",
                relative_path=route_native_record(
                    "runtime.procedure", ("procedure-other",)
                ).relative_path,
            ),
        )
        with self.assertRaises(OperationalRootError):
            validate_operational_root_delta(tampered, native_owner=owner)


if __name__ == "__main__":
    unittest.main()
