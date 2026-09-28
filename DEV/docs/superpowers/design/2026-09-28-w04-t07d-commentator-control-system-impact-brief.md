# W04.T07D Commentator control evidence — Implementation Impact Brief

Status: **SENIOR REVIEW REQUIRED — T07D HELD BEFORE RED**

Date: 2026-09-28

## Trigger

T07D's mandatory anti-oracle RED cannot be implemented safely from the existing
Commentator input contract without either treating caller-provided
`player_id -> story_ids` data as eligibility authority or deciding how current
W03 access, knowledge, disclosure and Story/T0 evidence combine into one
source-bound Commentator control basis. The current T07D write envelope keeps
W03 producers read-only and does not supply that joined evidence contract.

## Last safe state

```text
LAST_SAFE_SHA: b6b7e8925727394482a62ace335beb0a05ed733d
CURRENT_TASK: W04.T07D
T07D_RED: NOT STARTED
T07D_CODE/SCHEMA/TEST_CHANGES: NONE
```

## Approved plan expectation

The stable T07D row in
`DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`
admits `GAME/TOOLS/commentator.py`, Commentator schemas and RD13 tests. It
requires that arbitrary player-to-story-ID mappings cannot mint eligibility,
that content-finality is separate from access-finality, that changed control
basis refreshes filtering despite unchanged content, and that ineligible IDs,
counts and metadata are removed before LLM materialization. T07A/T07B/T07C and
W03 information/access producers are read-only inputs.

PO-009's accepted Commentator decision
(`DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md`)
requires a comprehensive, derived, self-contained eligibility/control
projection, preserves native knowledge/disclosure/access ownership, separates
content and control bases, and fails closed when control evidence is absent or
incompatible. Its exact physical representation is a downstream realization
decision; it does not itself define a Story/T0-to-recipient eligibility rule.

## Discovered implementation pressure

- `GAME/TOOLS/commentator.py::build_commentator_control_projection` currently
  accepts an arbitrary `player_id -> story_ids` mapping; the filter trusts that
  list and intersects it with `Story.availability.visible_to`.
- `GAME/TOOLS/story.py::validate_story_projection` validates the legacy
  Commentator carrier's `visible_to` list, but does not bind that list to the
  current W03 information/access basis. T07C's canonical StoryUnit availability
  instead carries source/story prerequisites and retained T0 values; it is not
  a per-player eligibility result.
- W03 `access_control.resolve_player(...)` resolves a verified principal to
  exact current PLAYER records, but it does not issue Story/T0 eligibility.
  W03 `information.py` validates native fact, knowledge and disclosure
  structures but does not expose a Commentator snapshot-level control basis.
- Implementing the required mapping therefore appears to require either a new
  W03-owned source-bound control-evidence interface or an additional
  Commentator eligibility rule joining native player/PC, knowledge/disclosure,
  Story availability and separate content/control bases. Neither is explicitly
  admitted by the current T07D row; guessing risks creating new access semantics
  or trusting the caller mapping.

Independent hdm-reviewer inspection of the T07D plan, PO-009, current Commentator
consumer, Story/T0 carrier and W03 access/information interfaces reached the same
conclusion: no mechanically complete T07D-only path was evident from the
current public owners. This finding does not reopen T07A, T07B, T07C or the
recorded CLS↔HDM preflight.

## Affected owners and protected invariants

```text
AFFECTED OWNERS / CONSUMERS:
  GAME/TOOLS/commentator.py
  Commentator-owned schemas
  DEV/TESTS/test_rd13_story_t0_commentator.py
  potential W03 access/information evidence boundary

PROTECTED INVARIANTS AT RISK:
  arbitrary caller mappings cannot mint eligibility
  content-final is not access-final
  IDs/counts/metadata of ineligible material remain absent before model materialization
  no second ACL, knowledge, disclosure, Story, History or currentness authority
  qualifying retained T0 remains Story-local and has no native-only fallback
```

## What can proceed without the disputed change

W04.T08B is independently dependency-eligible from accepted T06B plus the
closed Wave-03 principal/PLAYER, LIVE-currentness and access-policy chain, as
confirmed by the Product Owner. It remains within its test-and-bounded-SESSION-
delta write envelope and can be completed while T07D is held.

## Safe options for Senior resolution

1. Confirm that T07D may derive its Commentator-local source-bound control basis
   directly from existing read-only W03 owner values, and identify the exact
   already-authorized evidence/currentness composition that prevents caller
   mappings from becoming authority; or
2. expand the T07D Implementation Impact Envelope to admit the smallest needed
   W03 source-evidence interface/producer and its tests/version impact, without
   reopening T07A/B/C semantics or changing their accepted outputs.

RECOMMENDATION: keep T07D stopped before RED until the control-evidence boundary
and exact access semantics are resolved. Continue T08B independently. Keep
A26-02 as a separate mandatory proof/collection repair before
Wave-04 FINAL_REVIEW; do not weaken the accepted semantics to satisfy stale tests.

COST / RISK IF WRONG: trusting a caller map can leak protected Story/T0
existence or content; an invented restrictive rule can incorrectly withhold
eligible material or silently alter product access semantics.

UNPUBLISHED_WORK: NONE for T07D code/schema/tests. W04.T08B candidate remains
local and awaits its independent review/checkpoint.

```text
VERSION_IMPACT: NONE for this brief; no production or version-bearing owner changed.
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED for W04.T07D only.
```
