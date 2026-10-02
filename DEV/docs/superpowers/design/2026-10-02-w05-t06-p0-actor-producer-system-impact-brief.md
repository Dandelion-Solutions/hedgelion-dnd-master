# W05.T06-P0 Actor-Continuity Producer — System-Impact Brief

Status: **SENIOR_REVIEW_REQUIRED — P0 HELD AT PRODUCER WITNESS**
Date: 2026-10-02
Source-audit base: `4df0484790bbe54bbcf417483b871e0e8345380b`

## Trigger

The repaired P0 plan calls `actor_continuity.apply_actor_delta` an existing
accepted native Actor producer and requires its after-image as the positive HOT
admission witness. Current GAME source contains the pure transformation, but no
production caller or trusted accepted-evidence producer join. P0 cannot claim a
real accepted Actor-after-image witness from the current implementation.

This bounded finding does not reopen T06-A1 or the completed architecture loop.
It suspends P0 execution until the accepted-owner/source boundary is resolved.

## Approved plan expectation

The stable W05 plan's P0 says that `LOCAL_ESTABLISHED` follows native-owner
validation of the exact after-image and predecessor/current-source basis, and
that the P0 witness applies one accepted NPC Actor continuity delta before
SAVE. WP12 permits local SQLite establishment only for a semantic edge already
permitted by its native owner/durability contract. HOT itself cannot accept the
Actor mutation.

The final plan review at
`DEV/docs/superpowers/design/2026-10-02-w05-t06-repaired-plan-senior-review-final.md`
closed SP06-02 by naming `apply_actor_delta` as that witness. This brief records
new, direct source evidence that the function is not presently connected to an
accepted production path; the prior GO remains historical review evidence, not
resolution of this newly surfaced execution gate.

## Source evidence

| Source role | Evidence and applicability |
|---|---|
| Canonical Actor owner | `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md` states in its introduction (line 19) that it defines architecture only and implementation remains deferred; R2.2-16 requires bounded eligible evidence/current state, and R2.2-17 assigns deterministic control source membership/current revision/semantic eligibility validation before commit. |
| Accepted Actor phase contract | `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` provides material, subject-local Actor phases with a fresh logical rebind and conceptual `ActorProposal | NO_CHANGE` handoff (R2.4-14 and §7); exact schemas remain realization work. It establishes a semantic handoff, not a current GAME producer/callsite or evidence issuer. |
| Durable Actor owner | `DEV/ARCHITECTURE/ACTOR_MODEL.md` §§7, 8 and 11 places current continuity on the source Actor, keeps player agency separate, and distinguishes durable native authority from HOT/current-state representation. |
| Current continuation owner | `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` WP18-3 leaves current intentional continuity with the source Actor; Story/planning cannot produce or replace it. |
| Historical decision-basis owner | `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md` WP19-L29..L39 binds qualifying historical basis to the existing SemanticEvent family and the already-required Actor/Master decision work. WP19-L34 explicitly makes that basis retrospective, not a mutation path for current Actor state. It cannot by itself supply the P0 current-after-image witness. |
| Local establishment owner | `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` WP12-7/8 permits local establishment only where an existing native owner/durability contract permits that edge. It defines the transaction boundary, not Actor semantic acceptance. |
| Runtime implementation | `GAME/TOOLS/actor_continuity.py` `assess_actor` / `apply_actor_delta` validate shape and return a result/after-image. `_validated_evidence` receives ordinary mappings and checks caller-supplied `accepted`, `current`, and `authorized_actor_ids` fields; it does not resolve or revalidate those claims against native accepted evidence. |
| Existing tests | `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py::_accepted_evidence` constructs an in-memory fixture with `accepted: True`, `current: True`, and an Actor ID. These tests establish local transformation behavior, not an accepted production source path. |
| Consumer/callsite audit | GAME search finds no production call to `assess_actor` or `apply_actor_delta`; `continuity_projection.py` only validates continuity projections. `NativeHotStore` currently offers structural staging/mutation APIs without a trusted Actor producer caller. `bootstrap.compose_selected_runtime_host` currently composes repository/LIVE/publication capabilities and has no HOT/Actor producer join. |

## Discovered capability gap

There is no current end-to-end production path that:

1. obtains a current native `world.actor` predecessor and exact `state_revision`;
2. sources and verifies accepted/current evidence and Actor eligibility from its
   existing native owner, rather than accepting caller-provided boolean claims;
3. passes a bounded continuity delta through deterministic Actor validation;
4. joins the resulting exact Actor after-image to WP12 `LOCAL_ESTABLISHED` in
   the required local atomic edge before SAVE.

`apply_actor_delta` can be used by a future trusted caller as the owner-local
transformation. Its existence alone does not supply steps 1, 2, or 4 and does
not prove an accepted gameplay mutation. RD03 fixture success is not a
substitute for that producer/consumer join.

## Affected owners and protected invariants

- Owners: R2.2 / `ACTOR_MODEL.md`, WP18 source-Actor ownership, WP12 local
  establishment, T06-A1 P0 CurrentOwnerView/HOT admission.
- Consumers: RuntimeHost, selected campaign bootstrap, CurrentOwnerView/Context,
  SAVE, and P0's focused Actor/HOT integration tests.
- Preserve: one source-Actor semantic owner; current source/revision and accepted
  evidence are established before HOT; HOT is not semantic acceptance; no
  caller/test/HOT row can authorize a continuity mutation; PC agency and
  epistemic separation remain unchanged; no remote I/O occurs in the SQLite
  transaction.

## Safe boundary and Senior ruling requested

No P0 production RED/GREEN work or `W05_T06_CURRENT_OWNER_VIEW_READY` acceptance
may proceed while its required positive witness is represented only by the
current pure function plus synthetic evidence fixture. HOT snapshot/session
plumbing must not use a fabricated `OwnerDocument` to claim that the owner join
works.

Senior review is requested to determine whether the accepted R2.2/R2.4 Actor
proposal + deterministic-control contract, together with existing current-owner
evidence, is sufficient to authorize a bounded P0 implementation adapter and
producer/establishment join under the current architecture, or whether the
missing current-runtime capability needs a separately bounded owner/design
decision. The review should distinguish the accepted conceptual Actor phase
from the absent implementation call path; it should not treat WP19 historical
decision-basis evidence as current Actor mutation authority.

Until that ruling, do not add an Actor acceptance authority, evidence issuer,
producer interface, or mutation path by inference. No Product Owner decision
about gameplay semantics is presumed; escalate to the Product Owner only if the
Senior finds that closing the gap requires such a decision.

### Safe options

1. Confirm that the current accepted R2.2/R2.4 native Actor phase and its
   deterministic owner validation authorize a bounded P0 adapter, then specify
   the exact current-evidence input and test the end-to-end owner-to-HOT join
   within the existing P0 envelope.
2. If those owners do not supply the required current evidence/acceptance
   boundary, keep P0 held and route only that missing capability through the
   applicable owner/design decision path before implementation.

What can proceed without that ruling: no P0 production change or P0 completion
claim in this checkpoint. The current package remains safely at the published
pre-P0 plan boundary.

**Recommendation:** retain the P0 task and accepted T06-A1 architecture, but
hold P0 at this bounded System-Impact gate. Do not classify
`apply_actor_delta` itself as an accepted producer; it is an owner-local
validator/transformation awaiting a trusted current-evidence caller and
establishment join.

Cost/risk if this recommendation is wrong: treating the pure transformation or
synthetic evidence fixture as a connected producer could admit Actor state into
HOT without proving the accepted source/eligibility edge; holding when the
accepted phase contract already authorizes the exact adapter would delay P0 but
would not change gameplay behavior or create a conflicting owner.

```text
VERSION_IMPACT: NONE — development planning/provenance only.
PRODUCTION_CODE_CHANGED: NO
UNPUBLISHED_WORK: NONE after this brief and synchronized cursor are published.
```
