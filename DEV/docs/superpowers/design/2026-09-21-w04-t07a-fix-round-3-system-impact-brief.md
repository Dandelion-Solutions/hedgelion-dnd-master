# W04.T07A Fix Round 3 — Host Composition Boundary Stop

**DATE:** 2026-09-21
**TASK:** W04.T07A native-history composition / T05A Context host boundary
**REVIEWED HEAD:** `b6065ea0679fa8b4aff77ba0d531be8c5597f662`
**STATUS:** **SYSTEM-IMPACT STOP / SENIOR ROUTE REQUIRED**

## Trigger

Round-3 re-review required a mechanically non-replaceable host boundary. The
published round-1/round-2 repairs bind History through Context, but the
construction route and the resulting host object remain caller-forgeable.

The accepted Senior ruling still requires:

- T05A §2: `BoundContextRuntime` consumes an existing trusted
  `RepositoryPort`, selected-LIVE read capability, and fixed owner dispatch;
- T07A §3: native History is created at trusted host composition and per-call
  callers cannot replace the repository, routing, LIVE reader, or evt-window
  adapter.

## Actual admitted-route trace

Repository inspection found no separate runtime host/composition root or
production entry point that supplies these capabilities. The only GAME
construction route is:

```text
GAME/TOOLS/context_runtime.py::_compose_context_runtime(
    repository,
    live_route,
    selected_live_reader,
)
```

At the current head:

1. `_compose_context_runtime` accepts all three construction parts from its
   caller and stores them into a freshly allocated `BoundContextRuntime`.
2. It creates `BoundNativeHistoryRuntime(runtime)` from that object.
3. `BoundNativeHistoryRuntime.__init__` accepts any `BoundContextRuntime` and
   reads its private `_repository`, `_live_route`, and `_selected_live_reader`
   fields.
4. `resolve_candidate_basis` and `assemble_context` accept a caller-provided
   `BoundContextRuntime` and check only `isinstance`.
5. `object.__new__(BoundContextRuntime)` plus `object.__setattr__` can create a
   nominally valid forged host without any existing owner, producer, or
   composition provenance.

`GAME/TOOLS/policy_basis.py::RepositoryPort` is the accepted host capability
contract, but it is only a structural `Protocol` in this runtime tree. No
authenticated concrete provider is composed into Context or History. The
existing `PolicyBasisResolver` consumes a caller-injected repository for its
own resolver use; it is not a Context/History composition root.

No other `GAME/**/*.py` production consumer or composition root was found.
The current test consumers call the private Context composer directly:

- `DEV/TESTS/test_rd11_context_runtime.py` supplies repository/LIVE fixtures;
- `DEV/TESTS/test_rd13_story_t0_commentator.py` obtains History through that
  private composer.

## Reproduction evidence

Using the published code and test fixtures, a one-off bytecode-disabled probe
produced:

```text
FORGED_LOCAL_HISTORY_MINTED True
FORGED_LIVE_HISTORY_MINTED True
FORGED_CONTEXT_PUBLIC_API_ACCEPTED True
```

The first result used a forged `BoundContextRuntime` carrying a caller-created
repository and minted an accepted LOCAL publication. The second used the same
forged host shape with caller-created `LiveRouting` and LIVE reader material
and minted an accepted LIVE publication. The third passed the forged host to
the public Context assembly API and received `ASSEMBLED`.

## Why this task cannot safely implement locally

The required fix cannot be achieved by:

- renaming the composer with an underscore;
- adding a local trust marker, token, registry, or identity table;
- adding a new semantic owner or structural Protocol;
- merely hiding the History constructor while Context remains forgeable.

Those are expressly forbidden by the Senior ruling and task brief. Without an
existing concrete host producer, there is no accepted non-replaceable value
from which Context and History can be safely constructed. A local nominal
check is bypassed by the demonstrated `object.__new__` path; a local issuer or
registry would create the prohibited new trust mechanism.

## Scope and consumer impact

No GAME production consumer, Story path, Wave-05 writer, schema, persistence
surface, or Context semantic behavior was changed. T05 current behavior is
therefore preserved, but it remains dependent on the unresolved host boundary.
No TDD RED/GREEN production cycle was started because the accepted composition
route is absent; adding a test-only workaround would not establish authority.

## Version Impact Gate

`VERSION_IMPACT: NONE` — this is a development-only stop-evidence document.
No runtime module, serialized schema, campaign/storage generation, catalog,
projection, or version-bearing owner changed.

## Resolution required

Senior must identify or authorize the concrete host composition/deployment
boundary that supplies authenticated `RepositoryPort`, selected-LIVE read
capability, current routing, and the bound Context/History services without
caller replacement. Until that route exists, W04.T07A round 3 remains stopped.

`SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED`
`UNPUBLISHED_WORK: NONE after this evidence checkpoint`
