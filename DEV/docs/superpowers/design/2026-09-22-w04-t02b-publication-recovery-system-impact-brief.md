# W04.T02B — Publication/recovery system-impact brief

**DATE:** 2026-09-22
**TASK:** W04.T02B — publication/recovery and route-companion closure
**PUBLISHED REVIEW BASIS:** `ae424f32cc785f940f7740355924aa259d8895c6`
**STATUS:** **SENIOR_REVIEW_REQUIRED — T02B UNACCEPTED**

## Review scope

The published candidate was reviewed against the accepted W02 durability and
publication owner, the stable W04 plan, and the collaboration obligation
schema/runtime contract. This brief records findings only; it does not choose
or implement a publisher, migration, or compatibility alias.

## Independent review findings

### 1. Unadmitted publication capability and owner bypass

`GAME/TOOLS/collaboration.py::resolve_waiting` introduces a local
`CollaborationPublicationClosure`/publisher protocol and calls
`host._repository.publish_campaign_closure(...)` directly. That repository
publication capability is not admitted by the W04 impact envelope. The call
bypasses the accepted W02 publication owner in `GAME/TOOLS/publication.py`,
including its immutable `FrozenCampaignPublicationAttempt`, pinned currentness,
owner-issued durability/join validation, exact path envelope, non-force
publication plan, typed `PublicationOutcome`, and indeterminate reconciliation
contract.

This is a new repository publication/authority boundary and a material
transaction/currentness ownership decision. T02B cannot be accepted by keeping
the local capability as an implementation detail.

### 2. Breaking obligation schema change lacks compatibility disposition

The candidate changes the collaboration obligation persistent schema from v2 to
v3 and makes `closed_input_set_fingerprint` required for CLOSED/RESOLVED
records. Existing v2 persisted obligations therefore need an explicit
disposition: an admitted migration edge, an explicit unsupported/reject rule,
or another accepted compatibility policy. The candidate supplies none. It also
does not state whether the breaking persistent-family change requires a
`campaign_contract_generation` transition under the versioning owner.

This brief does not select a migration or compatibility policy. The schema and
campaign-contract consequences require Senior/design resolution before any
implementation resumes.

### 3. Schema lifecycle conditional mismatch

The candidate's three representations are not semantically equivalent:

- Python validation rejects a non-null `closed_input_set_fingerprint` on OPEN
  and requires a non-null fingerprint on CLOSED/RESOLVED.
- `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json` requires the
  field and conditionally requires a non-null value for CLOSED/RESOLVED, but
  permits a non-null value on OPEN.
- `GAME/SCHEMA/collaboration_obligation.schema.yaml` requires the field but
  permits `null` for every lifecycle and does not express the CLOSED/RESOLVED
  non-null condition.

The development schema, shipped projection and runtime validator therefore do
not describe one lifecycle contract. This must be reconciled as part of the
Senior disposition; it is not repaired in this checkpoint.

## Required Senior disposition and gates

Senior must either identify an already-admitted W02 publication/composition
route that can carry the exact collaboration closure through the accepted
`FrozenCampaignPublicationAttempt`/publisher contract, or return that boundary
to design. Senior/design must separately settle the v2-to-v3 persisted-schema
compatibility and campaign-contract disposition, then align the lifecycle
conditions across the DEV schema, GAME projection and runtime.

Until those findings are resolved:

- W04.T02B is **UNACCEPTED / SENIOR_REVIEW_REQUIRED**;
- W04.T02C and W04.T04A/T04B remain gated;
- W04.T05C remains gated on T05B + T04B + T02C;
- Wave 05 remains unauthorized;
- W04.T07A's selected-LIVE reader stop remains separate and unchanged.

No publisher or migration is selected or implemented here.

```text
VERSION_IMPACT: NONE — documentation-only checkpoint; no namespace value changed
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED — W04.T02B
UNPUBLISHED_WORK: NONE after publication/read-back
```
