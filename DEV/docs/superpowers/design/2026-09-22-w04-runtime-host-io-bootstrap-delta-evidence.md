# W04 RuntimeHost I/O Bootstrap Delta Evidence

Status: **BOUNDED WAVE-05 INPUT — NOT A FINAL WRITER**

Producer: **W04.T00P**

Outputs:

```text
W04_RUNTIME_HOST_IO_EXTENSIONS_READY
W04_RUNTIME_HOST_IO_BOOTSTRAP_DELTA_READY
```

## Delta for downstream Wave-05 owners

After campaign selection, the deployment host may additionally bind one
campaign-write capability to the existing ephemeral `RuntimeHost`:

1. authenticated Step-5.6 `RepositoryPort`;
2. selected-LIVE Step-5.8 transport; and
3. optional `CampaignPublicationTransport` for profiles that publish campaign
   state.

The host now exposes two fixed, immutable sibling routes in addition to the
accepted Context, History and native-ordering services:

- `CampaignPublicationService` receives an owner-routed
  `RoutedSerializedOperation`, freezes the W02 publication attempt, builds the
  connector plan, performs one non-force ref transition, classifies the
  `PublicationOutcome`, and performs only typed bounded reconciliation when
  acknowledgement is indeterminate;
- `SemanticEventSourceAdapter` returns strict bounded raw `evt` windows. LOCAL
  reads use the accepted event enrollment/index plus exact known-ID native
  records. Selected LIVE reads use the exact route-selected source revision
  and packed native enrollment/event evidence.

Neither sibling returns accepted history, Story material, eligibility or
fictional chronology. `history.py` remains the authority that validates raw
windows and issues native-history objects. Missing or stale LIVE sources do
not fall back to LOCAL/campaign aggregate reads. No aggregate
`LOG/SEMANTIC_EVENTS` read or invented LIVE tree index is admitted.

Publication-capable composition requires the read-side repository and
publication transport to expose and match the same selected repository
identity. The transport is never a gameplay argument, and no RuntimeHost or
service replacement/serialization surface is exposed.

## Verification evidence

`DEV/TESTS/test_runtime_host_composition.py` contains 14 focused tests covering
the existing composition boundary plus publication routing, one non-force
write, typed indeterminate reconciliation without a second write, LOCAL exact
known-ID reads, selected-LIVE source-pack reads, and missing-LIVE fail-closed
behavior.

Focused result:

```text
14 passed
```

Neighboring owner regression result:

```text
DEV/TESTS/test_rd06_durability_publication.py
DEV/TESTS/test_publication_ref_fence_contract.py
DEV/TESTS/test_rd11_context_runtime.py
DEV/TESTS/test_rd12_collaboration.py
156 passed
```

## Version and system impact

```text
VERSION_IMPACT:
  GAME/TOOLS/runtime_host.py framework_module_version: 1.0.5 -> 1.0.6
  persistent schema: none
  campaign/storage/catalog/protocol generation: none
  Wave-05 CORE projections/final writes: deferred to their owning W05.T08 writer

SYSTEM_IMPACT: NONE — accepted W04.T00P boundary only
```

W05.T06 consumes `W04_RUNTIME_HOST_IO_EXTENSIONS_READY` for product paths.
W05.T08 remains the sole final writer for shipped CORE/bootstrap projections;
this evidence does not edit shipped CORE bytes, install writers, schemas or
campaign scaffolds.
