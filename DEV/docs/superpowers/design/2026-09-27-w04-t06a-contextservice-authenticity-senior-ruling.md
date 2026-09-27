# W04.T06A ContextService Authenticity — Senior Ruling

Status: **ACCEPTED SENIOR / SYSTEM-IMPACT RESOLUTION**

Date: **2026-09-27**

Public basis reviewed:
`5136fdae83663dad43a45c8c58c8b38f989b1a90`

Current task:
`W04.T06A — phase rebind and accepted Context basis`

## 1. Trigger

Independent review of the unpublished T06A candidate found that its
`ContextAssembler` structural port can be satisfied by any in-process Python
object exposing `assemble`. The review classified that as HIGH because a test
double can return matching assembled fields and the TurnRuntime-local seal then
cannot prove that the exact `RuntimeHost.context` instance produced them.

The observation about the structural port is factual. The requested
exact-object authentication must, however, be evaluated against the already
accepted runtime-host trust model rather than against a stronger attacker model.

## 2. Owning evidence

This ruling composes:

- `DEV/docs/superpowers/design/2026-09-21-w04-runtime-host-ordering-route-owner-decision.md`;
- `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`;
- current `GAME/TOOLS/runtime_host.py` and `DEV/TESTS/test_runtime_host_composition.py`;
- `DEV/docs/superpowers/design/2026-09-26-w04-t06a-accepted-context-basis-system-impact-brief.md`.

No wider repository preload is required for this bounded ruling.

## 3. Controlling trust model

T00H already settles the disputed boundary.

Its trusted computing base is tracked deterministic HDM Python, runtime
host/bootstrap composition and authenticated deployment adapters. Player/model
text, model-shaped objects, unvalidated repository bytes and objects/callbacks
that cross gameplay/domain data-plane APIs remain untrusted.

T00H explicitly states that arbitrary in-process Python capable of importing
private issuers, mutating private attributes or supplying test fixtures is a TCB
compromise/test-harness concern rather than an ordinary gameplay attacker. It
also explicitly forbids inventing token/weak-registry/marker schemes merely to
authenticate the host root.

The current RuntimeHost already supplies the relevant composition invariant:

```text
compose_runtime_host(...)
  -> immutable campaign-bound RuntimeHost
  -> fixed RuntimeHost.context ContextService
  -> ContextService.assemble(...)
  -> fresh host operation basis
  -> owner-native Context assembly
```

Existing T00H negatives already reject repository/LIVE/service replacement
through gameplay request/candidate data and reject mutation of the root's bound
service attributes.

## 4. Disposition of the independent HIGH finding

The review is **correct** that structural Protocol conformance is not
cryptographic or nominal proof that an arbitrary Python object is the exact
`ContextService` instance.

That proof is not required at this boundary.

Treating a directly injected Python test double as an admitted hostile caller
would contradict the accepted T00H attacker model and would drive the design
toward exactly the in-process pseudo-security token/registry/identity machinery
that T00H rejected.

The relevant machine invariant is instead:

```text
untrusted gameplay/model/data-plane material
  MUST NOT choose / replace / serialize / reconstruct
  the Context assembler capability

tracked deterministic composition
  supplies the assembler dependency

T06A
  calls that dependency exactly once for the phase
  validates returned role/purpose/profile/subject/recipient/frontier
  mints only transient phase-local basis
  rejects raw/caller-shaped bundle data as provenance
```

A test-defined assembler is permitted when the test harness is intentionally
acting as trusted composition. Its existence is not a negative witness for the
gameplay authority boundary.

## 5. T06A implementation ruling

T06A may resume **inside its existing direct owner envelope**.

The implementation SHALL preserve all of the following:

1. the assembler capability is an ephemeral dependency supplied by tracked
   deterministic composition code, never a field/value selected from
   TurnEnvelope, Context request/candidates, model output, prior result or
   serialized state;
2. one phase assembly invokes the injected assembler exactly once;
3. before minting the transient accepted phase basis, T06A validates the
   assembled role, purpose, profile, subject/recipient and accepted source
   frontier required by that phase;
4. a raw mapping, matching `bundle_id`, matching recipient or other
   caller-shaped bundle data cannot mint or substitute the accepted basis;
5. Context trace/private diagnostics never become role evidence or ordinary
   output;
6. the assembler capability and any phase-local basis are ephemeral and not
   serializable/persistent authority;
7. test doubles may implement the narrow structural assembler port, but tests
   MUST separately prove that admitted gameplay/data-plane carriers cannot
   choose or replace that port.

Do not add, solely for this concern:

- a ContextService authenticity token;
- a weak registry/object-identity registry;
- a private marker presented as security authority;
- a reverse `turn_runtime -> runtime_host` dependency merely to perform
  nominal exact-instance checking;
- a new ContextService/RuntimeHost producer contract.

If implementation actually discovers that an admitted gameplay/data-plane path
can select or replace the service, or that a ContextService/RuntimeHost contract
must change for correctness, stop and reopen the System-Impact Gate with that
concrete evidence.

## 6. Review interpretation

The earlier independent review remains valid evidence that the candidate must
not claim arbitrary Python object identity as provenance. Its HIGH blocking
disposition is superseded **only in the exact threat-model point above**.

The next independent review SHALL evaluate the candidate against this ruling:

- attack raw/model/request/envelope/candidate substitution;
- verify one assembly call and scope/frontier checks;
- verify no raw basis promotion or diagnostic transport;
- do not reject a test-harness assembler solely because it is not the concrete
  RuntimeHost class;
- confirm no new producer/interface/dependency direction was introduced.

This ruling does not grant T06A PASS. The unpublished candidate remains
NOT_ACCEPTED until its required verification and independent task review pass.

## 7. Downstream routing

```text
T06A Senior System-Impact gate: RESOLVED
T06A implementation/re-review: CURRENT / NOT YET PASS
T06B: BLOCKED until T06A PASS
T07D: independently authorized
PO-011: unchanged; mandatory T06B input
W05: NOT AUTHORIZED
```

Final product/deployment wiring that ensures the production path uses the fixed
`RuntimeHost.context` service remains under the already accepted RuntimeHost /
Wave-05 bootstrap composition owners. T06A does not claim REAL deployment
integration.

## 8. Version and System Impact

```text
THIS RULING / CONTROL SYNCHRONIZATION:
  VERSION_IMPACT: NONE

T06A CURRENT EXPECTATION:
  turn_runtime.py remains unversioned support
  transient turn/result schemas remain non-persistent
  no Context Runtime / RuntimeHost module change is authorized by this ruling

SYSTEM_IMPACT:
  RESOLVED
  CLASSIFICATION: NO ARCHITECTURE DELTA / TARGETED IMPLEMENTATION RULING

PRODUCT_OWNER_DECISION_REQUIRED:
  NO
```
