# W04.T05A fix round 1 — Implementation Impact Brief

TRIGGER: Re-review of the Context repair established that the arbitrary
caller-supplied `exact_load` callable/object has no approved trusted transport
boundary. The current native checks also validate subject/recipient and the
registered profile table, but do not obtain native role/purpose eligibility.
This is a system-boundary gap, not a local validation defect.

LAST_SAFE_SHA: `98d3875ba1ab9780835819d70f627440a4bb9bd5`

CURRENT_TASK: W04.T05A owner-routed Context currentness and eligibility,
fix round 1. The pressure probe used evidence tree
`6fc280dda6afbf4e62ed620ef74642ddd82e5df4`; subsequent T07A documentation
publication is unrelated to this stop.

## Approved expectation

Context may consume a host-injected exact-load route only when that transport
boundary is explicitly trusted and owner-approved. The transport may provide
records, but it may not mint semantic `current` or `eligible` verdicts.
Role, subject, purpose and recipient must be freshly bound before semantic use;
Context remains an ephemeral projection and does not become an authority owner.

## Exact demonstrated pressure

Against the published repair, a caller-created loader returning self-consistent
LIVE route/source/projection records plus an owner-issued PLAYER resolution
produced:

```text
FORGED_LOADER_ADMITTED=True
ROLE_PURPOSE_NATIVE_REBIND_ADMITTED=True
```

The first result proves that rejecting a callback which returns boolean
verdicts is insufficient: an untrusted loader can still supply records that
pass every local exact-owner check. The second uses the same native evidence
under the registered Actor role/purpose and shows that no native owner binds
role/purpose eligibility.

## Affected owners and consumers

- W04 Context Runtime admission and its `assemble_context` consumers.
- W03 LIVE/currentness, information/knowledge/disclosure, and PLAYER/access
  owners.
- Registered ContextNeedProfile / RoleContextRequest role, subject, purpose and
  recipient contracts.
- The host/native exact-load transport boundary and its known-ID routing owner.
- Downstream T05B/T05C/T06 Context, Story and protected-emission consumers,
  which must not consume an untrusted admission basis.

## Protected invariants

- Caller records, mappings, callbacks, booleans and physical presence cannot
  mint currentness or eligibility.
- Native LIVE, PLAYER, information, knowledge and disclosure owners remain the
  sole authorities for their domains.
- Role/subject/purpose/recipient rebinding is required before semantic use.
- Context remains bounded, ephemeral and non-authoritative.
- No adapter, registry, capability, generic callback authority, second
  currentness owner or new persistent protocol is introduced locally.

## What can proceed

- Preserve this stop evidence and perform read-only Senior/Product-Owner design
  resolution of the missing boundary.
- Continue only unrelated already-authorized work with isolated owner/write
  sets; no dependent T05B/T05C/T06 implementation may proceed from this basis.
- Retain fail-closed behavior and existing negative verification; do not claim
  W04_CONTEXT_CURRENTNESS_ELIGIBILITY_READY.

## Safe options

1. Senior designates an existing trusted host exact-load boundary and an
   existing/native role-purpose eligibility route, then updates the accepted
   T05A contract and impact envelope.
2. Return to architecture/design to authorize an explicit boundary if no such
   existing route exists; this brief is not authorization to create it.
3. Narrow T05A to fail closed for candidates until both bindings are supplied
   through an approved owner route.

RECOMMENDATION: Keep T05A stopped and choose option 1 or 3. Do not treat an
arbitrary caller-supplied `exact_load` as trusted and do not promote the
registered profile table into native role/purpose eligibility.

COST / RISK IF WRONG: A local-looking repair could admit forged or stale
material, cross role/purpose boundaries, disclose ineligible information, and
leave replay/recovery without a reproducible native authority basis.

VERSION_IMPACT: NONE — documentation-only design checkpoint; no version,
revision, schema, generation or projection namespace changed.

SYSTEM_IMPACT: STOP / SENIOR REVIEW REQUIRED — approved boundary and native
role/purpose eligibility route are unresolved.

UNPUBLISHED_WORK: NONE. No production, schema, test, cursor, Wave-05, adapter,
registry or capability files were changed in this stop slice.
