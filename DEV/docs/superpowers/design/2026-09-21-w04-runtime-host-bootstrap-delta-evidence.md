# W04 RuntimeHost Bootstrap Delta Evidence

Status: **BOUNDED WAVE-05 INPUT — NOT A FINAL WRITER**

Producer: **W04.T00H**

Outputs:

```text
W04_RUNTIME_HOST_COMPOSITION_READY
W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY
```

## Delta for the Wave-05 bootstrap owner

After explicit campaign selection, the deployment host supplies:

1. an authenticated Step-5.6 `RepositoryPort`; and
2. the selected-LIVE Step-5.8 transport.

`GAME/TOOLS/runtime_host.py` composes those capabilities into one ephemeral,
campaign-bound `RuntimeHost`. The root owns fixed sibling routes for:

- Context Runtime;
- native History; and
- Step-3 native ordering evidence.

Each service operation obtains a fresh exact campaign pin and selected-LIVE
route. The root is not a lease and exposes no repository, LIVE transport,
route-resolver or service replacement API. Domain/gameplay calls provide only
requests and candidate data; capability-shaped values in those inputs are not
used for routing or currentness.

The host and its capabilities are in-process ephemeral state. They are not
serialized or persisted in campaign state. Arbitrary object fabrication or
mutation inside tracked deterministic Python remains a trusted-computing-base
compromise, not an ordinary gameplay authority path; an unsupported deployment
that permits untrusted Python in that TCB requires process/tool isolation.

## Wave-05 ownership boundary

W05.T08 is the sole final writer for `GAME/CORE/BOOTSTRAP_RUNTIME.md`. It must
fresh-read this delta and integrate the deployment-wiring law at its admitted
`BOOTSTRAP_RUNTIME` checkpoint (`1.0.9`). This artifact does not edit shipped
CORE/bootstrap bytes, install writers, product paths, schemas or campaign
scaffolds.

## Evidence

`DEV/TESTS/test_runtime_host_composition.py` covers composition, sibling
service separation, per-operation re-pin/revalidation, cross-campaign rejection,
capability/service override rejection, untrusted input containment,
non-serialization and adapter-shape validation. The focused host suite is
GREEN at 8 tests.

## Version and system impact

```text
VERSION_IMPACT:
  GAME/TOOLS/runtime_host.py framework_module_version: new module -> 1.0.1
  persistent schema: none
  campaign/storage/catalog/protocol generation: none
  Wave-05 CORE projection: deferred to W05.T08 final writer

SYSTEM_IMPACT: NONE
```
