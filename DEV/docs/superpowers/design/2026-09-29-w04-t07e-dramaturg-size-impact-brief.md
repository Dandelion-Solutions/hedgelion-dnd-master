# W04.T07E Dramaturg publication sizing — Implementation Impact Brief

Status: **SYSTEM-IMPACT REVIEW REQUIRED — T07E PAUSED BEFORE ACCEPTANCE**

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

WP-18 requires the two fixed retained horizon families; the accepted T07E task
does not authorize a new partition route, root selector, W02 serializer API or
other cross-owner interface. WP-24 rejects inventing universal numeric quotas.

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

## What can proceed without changing the boundary

The implementation and its local corrupt-horizon error-path repair are committed
locally and were reviewed. The reviewer confirmed the corrupt-horizon finding
was addressed and withdrew the mistaken SemanticEvent-source finding. The
candidate schema impact is `dramaturg-horizon.schema.json` 1 -> 2; under the
current pre-release clean-slate owner there is no migration or
`campaign_contract_generation` bump solely for replacing the unreleased
scaffold shape. The local candidate has focused/cross-owner test evidence, but
T07E cannot be accepted while the writer-size obligation lacks an authorized
measurement route.

## Safe options for Senior resolution

1. Authorize a narrow existing-W02/RuntimeHost capability that measures the
   exact final serialized bytes for the Dramaturg path operations and returns
   the owner-defined sizing classification before publication. This requires
   updating the T07E impact envelope and testing the W02 serialization boundary
   and Dramaturg behavior together.
2. Identify an already-approved exact serializer/measurement capability that
   the T07E writer can consume without changing W02/RuntimeHost contracts, with
   evidence that its measured bytes equal the actual emitted artifact.
3. Keep T07E stopped and the local candidate unpublished until a compliant
   bounded publication route is authorized.

No option is selected by this brief. Do not invent a serializer, numeric cap,
partition path, or compatibility/migration policy to continue implementation.

## Recommendation

Resolve the exact-byte measurement owner/interface before accepting or
publishing the T07E code candidate. Preserve the current stable two-route
Dramaturg semantics and keep T07D, T07A/B/C, the CLS↔HDM preflight and A26-02
unchanged.

## Cost / risk if this gate is wrong

Publishing without exact size evidence can create campaign artifacts outside
the accepted operational bands and make future reads/replacements unsafe.
Approximating with JSON or arbitrary byte/entry caps can misclassify actual
transport size, reject valid planning unnecessarily, or encode an unapproved
partition/migration policy.

```text
VERSION_IMPACT: NONE for this brief; it changes only development status/evidence.
T07E CANDIDATE VERSION IMPACT: dramaturg-horizon.schema.json 1 -> 2;
  campaign_contract_generation, storage/catalog/engine, migration and dual-read NONE.
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED
UNPUBLISHED_WORK: T07E commits `cd5c8a2ba78584ab0e1527d20b43db6ca443b417` and `20dd239d109cb2221b85ebd62f217fac509c7a1e` remain local and unpushed.
```
