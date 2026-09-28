# W04.T07D Commentator control evidence — Implementation Impact Brief

Status: **SENIOR REVIEW COMPLETE — PO-012 INCORPORATED / T07D-P0 ACCEPTED / T07D RESUMED**

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

## Senior resolution

The two implementation options above are not semantically equivalent and cannot
be selected safely before one upstream product question is closed.

Accepted Step-4 architecture says that Story availability is evaluated by the
active Commentator mode/session and explicitly leaves the exact default
spectator perspective/spoiler policy to the mode owner. PO-009 requires the
control projection to be derived from current native owners but does not choose
whether protected eligibility is based on human PLAYER disclosure, one
controlled PC's `world.knowledge`, several controlled PCs, a full-history
spectator profile, or another explicitly admitted mode.

Accordingly:

1. **Reject T07D-local semantic derivation.** Commentator may not invent the
   join rule or turn caller values into access authority.
2. **Require Product Owner semantics first.** The baseline Commentator
   perspective/spoiler rule must define what protected material a served human
   may receive and how PLAYER exposure differs from PC knowledge.
3. **Then use a bounded native-owner evidence prerequisite.** The implementation
   should issue source-bound current PLAYER/control and information/disclosure
   evidence sufficient to build the PO-009 control projection, without creating
   a second ACL/knowledge/disclosure owner. Story/T0 availability requirements
   are nominations to be checked against that evidence, not authority.
4. No T07A/B/C reopen, no native-only fallback and no T07D RED until the owner
   decision is incorporated.

Full disposition:
`DEV/docs/superpowers/design/2026-09-28-w04-t07d-commentator-control-senior-ruling.md`.

A26-02 remains a separate mandatory proof/collection repair before Wave-04
FINAL_REVIEW; do not weaken accepted semantics to satisfy stale tests.

COST / RISK IF WRONG: trusting a caller map can leak protected Story/T0
existence or content; an invented restrictive rule can incorrectly withhold
eligible material or silently alter product access semantics.

UNPUBLISHED_WORK: NONE for T07D-P0 code/schema/tests. W04.T08B completed and was
published/read back at `W04_SESSION_CONSUMER_DELTA_READY`; its code commit is
`356357a5c05e16d704bebfe11e8a3df542321694`, with the final status/read-back
checkpoint at `468bd3400183ada85b76cd93737005aa1e1e64a7`. T07D-P0 is published
at `d37ed9c1994e78feb51fc147cd3e2e5225b5a548`; independent PASS and fresh
remote read-back are complete, so T07D may resume within its existing
Commentator consumer envelope.

```text
VERSION_IMPACT: NONE for this brief; no production or version-bearing owner changed.
SYSTEM_IMPACT: SENIOR_REVIEW_RESOLVED / PO-012 INCORPORATED / T07D-P0 ACCEPTED; T07D is cleared to resume within its existing consumer envelope.
```

## T07D-P0 verification and acceptance

P0 code commit: `d37ed9c1994e78feb51fc147cd3e2e5225b5a548`.

- RD11 Context + RuntimeHost focused tests: 96 passed.
- Clean committed-source full DEV: 1358 passed, 5 skipped, 4 known out-of-scope S6D failures; package provenance reports `clean_head`.
- Version/provenance/current-progress suite: 18 passed; maintenance audit: PASS.
- Scoped Ruff check/format and `git diff --check`: PASS.
- Independent task review: PASS; no findings/System-Impact concern.
- A fresh fetch confirmed `origin/v1/engine-rearchitecture` at `d37ed9c1994e78feb51fc147cd3e2e5225b5a548` after review.

`VERSION_IMPACT: GAME/TOOLS/context_runtime.py 1.0.8 -> 1.0.9`; no persistent schema/generation, campaign/storage/catalog/engine generation, migration, or dual-read change.


## PO-012 incorporation / exact continuation

PO-012:
`DEV/docs/superpowers/specs/2026-09-28-commentator-player-selected-pc-perspective-owner-decision.md`.

The product-semantic question is closed. Fresh machine inspection narrows the
implementation prerequisite: Context Runtime already owns exact current
PLAYER/knowledge/disclosure/lore reloads through RuntimeHost. Therefore use
T07D-P0 to register a COMMENTATOR control profile rather than adding a new W03
permission service.

```text
T07D-P0 -> W04_COMMENTATOR_CONTROL_CONTEXT_READY
  -> independent PASS/read-back
  -> T07D RED / implementation
```

No T07A/B/C reopen. No caller map, visible_to, provenance-string heuristic,
multiple-PC union or native-only Commentator fallback is authorized.
