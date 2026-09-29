# W04.T07E Dramaturg publication sizing — Implementation Impact Brief

Status: **T07E ACCEPTED/READ BACK — SENIOR IMPACT RESOLUTION REALIZED; T07-INTEGRATION PENDING**

Date: **2026-09-29**

## Trigger

W04.T07E publishes retained multiplayer Dramaturg horizons as mutable
campaign-tree YAML through the existing RuntimeHost/W02 publication boundary.
The current runtime mutable-artifact sizing owner requires the responsible
writer to measure the exact final serialized UTF-8 payload before publication
and apply its target/review/review-and-partition decision bands. The current
T07E direct write envelope admits `dramaturg.py`, the Dramaturg horizon schema
and RD13 only; the existing publication boundary accepts structured
`path_operations` mappings and does not expose the final emitted bytes or an
exact size result. A canonical-JSON measurement inside Dramaturg is not the
same as the final serialized `DRAMATURG/*.yaml` payload.

## Last safe public state

```text
LAST_SAFE_SHA: f60246abeca880b0d6c39c34feea99347a1be3e0
CURRENT_TASK: W04.T07E
T07E_ACCEPTANCE: NOT COMPLETE
```

The last safe public ref has accepted T07D and the T07E task envelope. Two
unpublished local T07E commits currently exist: implementation
`cd5c8a2ba78584ab0e1527d20b43db6ca443b417` and the corrupt-horizon fix
`20dd239d109cb2221b85ebd62f217fac509c7a1e`. They remain unpushed pending
resolution of this gate.

## Approved plan and controlling owner

The stable task row in
`DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`
authorizes T07E changes to `GAME/TOOLS/dramaturg.py`, Dramaturg schemas and
RD13 only, using the existing fixed retained-horizon routes and W02 publication
path.

The current sizing owner is
`DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`:

- §§2–4 require exact serialized UTF-8 measurement by the writer for mutable
  GitHub-backed text artifacts and use approximate 10–12 KiB preferred,
  13–16 KiB review, and above-approximately-16 KiB review/partition/rollover
  bands;
- these are decision bands, not a universal hard cutoff;
- truncation and semantically false splitting are forbidden;
- growth-bearing artifacts need an owner-valid bounded representation before
  becoming an operational dead end.

WP-18 requires the two fixed retained horizon families; the original accepted
T07E task did not authorize a new partition route, root selector, W02 serializer
API or other cross-owner interface. The 2026-09-29 Senior resolution below
amends only the narrow W02 exact-measurement capability and its tests. WP-24
rejects inventing universal numeric quotas.

## Discovered implementation pressure

The current writer calls `host.publication.publish_owner_delta(...)` with
structured mappings. `RuntimeHost.CampaignPublicationService.publish_owner_delta`
freezes the attempt, builds the publication plan and passes mapping-valued
`path_operations` to `CampaignPublicationTransport.create_tree`. The public
interface returns publication outcome/evidence, not the exact serialized bytes.
Repository search found no current `GAME/TOOLS` serializer or size-measurement
result for this path. Dramaturg's `_canonical_json` is an internal comparison
representation and does not prove the YAML bytes emitted by the transport.

Consequently T07E cannot claim the required exact measurement by measuring
canonical JSON, counting characters, or relying on the schema. Adding a hard
entry/text cap would substitute an unapproved quota for the sizing bands. Adding
partition/rollover or changing the serializer/publication API would cross the
approved direct write envelope.

## Affected owners and consumers

```text
CURRENT TASK OWNER / CONSUMER:
  GAME/TOOLS/dramaturg.py
  DEV/SCHEMAS/dramaturg-horizon.schema.json
  DEV/TESTS/test_rd13_story_t0_commentator.py

BOUNDARY THAT MAY REQUIRE AN AUTHORIZED CHANGE:
  GAME/TOOLS/runtime_host.py CampaignPublicationService
  CampaignPublicationTransport serialized-file boundary
  W02 campaign publication/versioning tests and owner evidence
```

## Protected invariants at risk

- exact final serialized size is measured before publication;
- sizing bands do not become a universal hard rejection cutoff;
- no truncation, arbitrary quota, false semantic split, or unowned partition
  is introduced;
- only fixed Dramaturg routes and accepted non-force W02 publication remain;
- publication failure never promotes a candidate generation;
- planning remains noncanonical and never mutates native history or overrides
  current owners.

## Pre-resolution disposition (historical)

The implementation and its local corrupt-horizon error-path repair are committed
locally and were reviewed. At this brief's initial disposition, the reviewer
confirmed the corrupt-horizon finding was addressed and withdrew the mistaken
SemanticEvent-source finding, but T07E remained stopped pending measurement
authorization. That stop was later resolved by the Senior authorization below.
The candidate schema impact is `dramaturg-horizon.schema.json` 1 -> 2; under
the current pre-release clean-slate owner there is no migration or
`campaign_contract_generation` bump solely for replacing the unreleased
scaffold shape.

## Senior resolution — 2026-09-29

Senior / Product Owner disposition: **AUTHORIZE NARROW W02 MEASUREMENT FOR ALL SIMILAR CASES**.

The T07E impact envelope is amended to allow one generic, side-effect-free
RuntimeHost/W02 capability that reports the exact serialized UTF-8 byte size
for supplied campaign path operations using the same serializer as
`CampaignPublicationTransport.create_tree`, plus its RuntimeHost/W02 tests.
T07E is the current adopter; the measurement capability is reusable by
similar W02 writers without automatically changing unrelated owners' direct
write scopes.

For review/partition-band Dramaturg candidates, publication remains withheld
until an **ephemeral trusted owner review outcome** is present and bound to the
exact candidate, fixed route, and measured byte count. No review outcome or
review artifact is persisted. It cannot be supplied by model, request or
campaign data. The accepted sizing bands remain decision guidance, not a hard
validity cutoff; no hard byte cap or new partition route is authorized.

The resolution authorizes measurement and review-defer behavior only. It does
not change W02 publication acceptance/transaction semantics, add a general
registry or alter campaign/storage version policy. The RuntimeHost module
version must be reconciled under its current version owner if the implementation
materially changes that module.

## Recommendation

Implement the authorized exact-byte measurement capability and T07E integration
inside the amended impact envelope, then re-review and verify before accepting
or publishing the T07E candidate. Preserve the stable two-route Dramaturg
semantics and keep T07D, T07A/B/C, the CLS↔HDM preflight and A26-02 unchanged.

## Cost / risk if this gate is wrong

Publishing without exact size evidence can create campaign artifacts outside
the accepted operational bands and make future reads/replacements unsafe.
Approximating with JSON or arbitrary byte/entry caps can misclassify actual
transport size, reject valid planning unnecessarily, or encode an unapproved
partition/migration policy.

```text
VERSION_IMPACT: NONE for this brief; it changes only development status/evidence.
T07E CANDIDATE VERSION IMPACT: dramaturg-horizon.schema.json 1 -> 2;
  RuntimeHost module 1.0.10 -> 1.0.11; campaign_contract_generation,
  storage/catalog/engine, migration and dual-read NONE.
SYSTEM_IMPACT: RESOLVED TO BOUNDED W02 MEASUREMENT / T07E IMPLEMENTATION RESUMED
UNPUBLISHED_WORK_AT_INITIAL_BRIEF: T07E commits `cd5c8a2ba78584ab0e1527d20b43db6ca443b417` and `20dd239d109cb2221b85ebd62f217fac509c7a1e` were local and unpushed when this impact brief was first recorded.
```

```text
SYSTEM_IMPACT_RESOLUTION: RESOLVED TO BOUNDED W02 MEASUREMENT PREREQUISITE
AUTHORIZED_EXTENDED_SCOPE: one exact serialized-byte measurement capability in RuntimeHost/W02 plus its tests; T07E consumes it before publication
REVIEW_BAND_DISPOSITION: withhold until ephemeral trusted owner outcome tied to candidate/route/byte count
HARD_CAP_OR_NEW_PARTITION: NOT AUTHORIZED
T07E_ACCEPTANCE_AT_RULING: PENDING IMPLEMENTATION, VERIFICATION, REVIEW AND REMOTE READ-BACK
```

## T07E measurement implementation and task-review evidence

Local code checkpoints:

```text
T07E horizon implementation: `cd5c8a2ba78584ab0e1527d20b43db6ca443b417`
corrupt-horizon repair: `20dd239d109cb2221b85ebd62f217fac509c7a1e`
W02 measurement + T07E size review: `421516689e6ed766eadf1045571eff3078971328`
T07E review-outcome TCB fix: `c34c5b20f0657052e4a152bd21abe5fe11202f2d`
```

The W02 measurement addition is one generic side-effect-free
`CampaignPublicationTransport.measure_path_operations` capability, surfaced
through bound `RuntimeHost.publication`. It returns per-path exact UTF-8 byte
lengths using the same adapter serializer contract as `create_tree`; missing,
incomplete or invalid measurement fails closed. RuntimeHost/W02 publication
transaction, accepted-outcome and create_tree signatures remain unchanged.
T07E measures the exact operation before W02 publication; review/partition-band
candidate writes remain unpublished until a nonpersistent typed trusted-owner
outcome is bound by value to that candidate, route, base and measured size. No
hard cap or new route was added.

The independent reviewer initially found the review-outcome issuer marker
could be used as pseudo-authentication. The fix removes issuer markers and
object-identity proof; the outcome is a plain ephemeral value and tracked
deterministic composition is its trusted source under T00H. The same reviewer
scoped re-review marked that finding ADDRESSED and found no new breakage.
Review verdicts: spec compliance PASS for the implementation range and
task/code quality PASS, with local broad-verification concerns below.

Verification evidence:

- controller combined RuntimeHost composition + RD13 + RD11 + RD09: **418
  passed**, with two pre-existing `jsonschema.RefResolver` warnings;
- scoped Ruff checks and format checks: **PASS**;
- full local DEV diagnostic: **1404 passed, 5 skipped, 11 failed**; the four
  known A26-02/S6D REDs were separately reproduced, and the remaining seven
  failures are preserved workspace-artifact contamination (`.entire/`,
  `DEV/tmp`, `DEV/.lavish/`/generated GAME cache);
- maintenance audit: existing duplicate `ENGINE_VERSION.yaml` under
  `DEV/tmp` plus `.entire/tmp` identity artifact; no workspace material was
  cleaned;
- hosted CI unavailable in the local-machine runtime; no hosted result is
  claimed for this T07E candidate.

`VERSION_IMPACT`: Dramaturg horizon schema `1 -> 2`; RuntimeHost `1.0.10 ->
1.0.11`; campaign/storage/catalog/engine generations, migration, dual-read
and DEV bookkeeping revisions: NONE. The pre-release clean-slate owner remains
the basis for no campaign migration/aggregate-generation bump.

T07E code candidate `c34c5b20f0657052e4a152bd21abe5fe11202f2d` and synchronized
verification/status checkpoint `1e3ddfa71e285513ce0d86e6a16096fcf527eeaf` were
published non-force. A fresh fetch confirmed local HEAD and
`origin/v1/engine-rearchitecture` both at `1e3ddfa71e285513ce0d86e6a16096fcf527eeaf`.
T07E is accepted/read back as `W04_COMMENTATOR_DRAMATURG_READY`. Next is the
independent T07-INTEGRATION review; A26-02 remains separate.

## Clean exact-candidate verification — 2026-09-30

The clean detached source at `c34c5b20f0657052e4a152bd21abe5fe11202f2d`
passed the canonical full DEV diagnostic with **1411 passed, 5 skipped, 4
failed**. All four failures are the exact known S6D/A26-02 nodes listed in the
execution cursor; a sequential rerun reproduced each failure. No T07E/RD13,
RuntimeHost, or related regression test failed. The package-provenance tests
reported a clean HEAD. The combined version-namespace, package-provenance, and
current-progress suite passed **18 tests**; the canonical maintenance audit
passed (`OK: engine consistency audit passed`).

This is local verification only. Hosted CI is unavailable in the current
runtime. T07E code and synchronized status remain pending non-force publication
and fresh remote read-back; T07-INTEGRATION is not started until that gate.
