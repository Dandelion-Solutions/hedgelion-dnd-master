# W04.T07A Implementation Impact Brief — Native Owner Boundary Stop

**DATE:** 2026-09-21
**TASK:** W04.T07A — accepted native history publication/recovery
**LAST_SAFE_SHA:** `6fc280dda6afbf4e62ed620ef74642ddd82e5df4`
**STATUS:** **SYSTEM-IMPACT STOP / SENIOR REVIEW REQUIRED**

## Trigger

Re-review established that `NativeHistoryOwnerPort` is only a structural
`typing.Protocol`. No admitted W02 native-history adapter or composition-root
boundary exists. A caller can therefore provide a conforming object and mint
accepted native-history authority.

This brief records the stop. It does not authorize another production repair.

## Approved expectation

T07A may admit accepted native history only through an already admitted W02 or
native owner-read boundary. Caller-shaped `SemanticEvent` data, structural
protocol conformance, projections, tokens, registries, callbacks or other
caller-provided carriers must never mint currentness, accepted events or
publication state. Story, Commentator and Dramaturg remain projections and
cannot establish native history or access.

## Exact forged-port evidence

- `GAME/TOOLS/history.py:79-83` defines `NativeHistoryOwnerPort` as a one-method
  structural protocol; it has no nominal identity or admitted producer.
- `GAME/TOOLS/history.py:278-323` obtains the method with `getattr`, calls it,
  validates only the returned mapping shape, and then directly calls the
  private issuers to construct and register `NativeHistoryCurrentness`,
  `NativeSemanticEvent` and `NativeHistoryPublication`.
- `DEV/TESTS/test_rd13_story_t0_commentator.py:79-106` demonstrates the issue:
  `_NativeHistoryOwner` is an ordinary class with no inheritance, registration,
  token or composition-root provenance. Its caller-selected payload is
  accepted by `read_native_history` and becomes owner-issued publication state.

Thus a caller can supply the equivalent of:

```python
class ForgedOwner:
    def read_accepted_native_history(self, campaign_id: str) -> object:
        return {
            "campaign_id": campaign_id,
            "origin": "LOCAL",
            "source_revision": "0" * 40,
            "events": [valid_event_mapping],
        }

read_native_history(ForgedOwner(), "campaign.main")
```

The result is accepted publication material despite the absence of an admitted
W02/native owner.

## Affected owners and consumers

- W04.T07A native-history issuance, publication and recovery in
  `GAME/TOOLS/history.py`.
- The missing W02/native owner-read adapter and its composition root.
- Native-history currentness/publication contract consumers and their existing
  `DEV/SCHEMAS/` representations; no schema edit is authorized by this brief.
- W04 Story, Commentator and Dramaturg consumers that must read native history
  without becoming a second authority.
- `DEV/TESTS/test_rd13_story_t0_commentator.py`, whose current plain test owner
  is evidence of the structural seam, not evidence of trusted production
  ownership.
- Wave-05 shared/final-writer surfaces are out of scope and remain
  unauthorized.

## Protected invariants

- Only an admitted native/W02 owner can establish native-history currentness,
  accepted event identity and publication state.
- Currentness is the complete owner/source basis, not a typed carrier or
  structural method match.
- Publication and recovery cannot accept caller-shaped or stale authority.
- Story/Commentator/Dramaturg cannot establish native history, access or canon.
- No ad-hoc trust marker, registry, capability, private CLS implementation or
  Wave-05 write is introduced to bypass the missing owner boundary.

## What can proceed

- This documentation, Senior/design review and owner/consumer evidence work.
- Independent work that does not consume T07A native-history authority, subject
  to its own gates.

T07A production implementation, T07B–T07E and T07 integration cannot proceed
until the owner boundary is resolved. Wave-05 remains unauthorized.

## Safe options

1. Senior identifies an existing admitted W02/native owner and composition-root
   route that T07A can consume without accepting structural caller authority.
2. Return to design to specify an owner-owned read boundary, including producer,
   construction/composition, currentness proof, persistence implications,
   consumers, tests and versioning.
3. Defer native-history read/issuance work until one of those routes exists;
   preserve the stop rather than adding a local bridge.

No option authorizes an ad-hoc trust marker, registry, caller capability or
private CLS dependency.

## Recommendation

Keep W04.T07A at the System-Impact stop. Resolve the W02/native owner and
composition-root boundary through the Senior/design route, then revise the
implementation impact envelope and rerun TDD and integration review from the
newly accepted boundary.

## Risk if the stop is bypassed

A caller can choose a valid campaign, origin, source revision and event set and
obtain an apparently owner-issued publication. Downstream append/recovery sees
the forged object as current, creating a second currentness authority and
allowing false provenance, replay/recovery divergence or cross-scope accepted
history to reach Story consumers.

## Version Impact Gate

`VERSION_IMPACT: NONE` — this checkpoint adds only a development design brief
under `DEV/docs/superpowers/design/`. It changes no runtime module, serialized
schema, campaign/storage generation, catalog, digest generation, projection or
version-bearing owner. The existing `GAME/TOOLS/history.py` module revision is
unchanged at `1.0.7`.

## Checkpoint state

`SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED`
`UNPUBLISHED_WORK: NONE after commit, publication and remote read-back.`
