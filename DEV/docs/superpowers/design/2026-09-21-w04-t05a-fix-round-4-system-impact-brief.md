# W04.T05A fix round 4 — forged host composition System-Impact Brief

STATUS: **STOP / SENIOR-DESIGN REVIEW REQUIRED**

This is a bounded re-review brief for W04.T05A. It records an unresolved
composition/trust-boundary defect only. It does not authorize a production
repair, a local token or registry workaround, a cursor update, or downstream
Wave-04/Wave-05 work.

## Trigger

TRIGGER: `BoundContextRuntime` remains caller-composable; a forged host can
mint Context and accepted `LOCAL` history, and no concrete non-replaceable
trusted composition route is identified by the final ruling.

Independent re-review after the final W04.T01A/T05A/T07A ruling found that
`BoundContextRuntime` still accepts caller-supplied host capabilities in
practice. A caller can create a nominal `BoundContextRuntime` with
`object.__new__`, replace its private repository/LIVE capability fields, and
construct `BoundNativeHistoryRuntime` from that forged host. The final ruling
describes a trusted composition root conceptually, but does not identify a
concrete non-replaceable trusted composition route that proves the host and its
capabilities are authoritative.

The defect is therefore a system-boundary gap, not a local candidate-field
validation defect. No local token, weak registry, marker, or equivalent
workaround is authorized to stand in for the missing composition authority.

## Last safe published state

```text
LAST_SAFE_PUBLISHED_SHA: 58444e0fcd08ba7dce651cfb2c0799345b227591
CURRENT_TASK: W04.T05A owner-routed Context currentness and eligibility,
              fix round 4 re-review
```

This SHA is the last published/read-back basis before this documentation-only
stop. It must not be interpreted as a W04.T05A acceptance checkpoint: the
published implementation still has the composition defect described here.

## Approved expectation versus discovered pressure

The final ruling requires:

```text
registered RoleContextRequest + registered ContextNeedProfile
-> bounded discovery/routing hints
-> exact routed native-owner reload
-> native currentness and role/purpose/recipient eligibility validation
-> internal post-resolution basis
```

It also requires the Context and native-history services to consume trusted
host-composed `RepositoryPort` and selected-LIVE capabilities, with callers
unable to replace those capabilities.

The implementation currently relies on nominal Python object shape and private
attribute access instead:

- `_compose_context_runtime` accepts a repository by method presence and stores
  supplied capabilities with `object.__setattr__`;
- `BoundNativeHistoryRuntime.__init__` accepts any `BoundContextRuntime` and
  reads its private capability fields after an `isinstance` check;
- `object.__new__(BoundContextRuntime)` plus `object.__setattr__` bypasses the
  constructor and permits caller-created host state;
- the resulting host can issue Context and native `LOCAL` history through the
  ordinary public service methods.

## Evidence and probes

### Baseline verification

At the last published head:

```text
.hdm-devtools/venv/bin/python -m unittest \
  DEV.TESTS.test_rd11_context_runtime \
  DEV.TESTS.test_rd13_story_t0_commentator

Ran 70 tests in 0.034s
OK
```

The existing forged-runtime regression only forges a bare
`BoundNativeHistoryRuntime` and expects it to lack its service-issued window
adapter. It does not test a forged `BoundContextRuntime` carrying caller-made
capabilities.

### Probe A — forged Context host admits caller-created material

The probe created a `BoundContextRuntime` with `object.__new__`, installed a
caller-created repository containing a caller-created `world.scene` record,
installed a `BoundNativeHistoryRuntime` from that host, and called
`BoundContextRuntime.assemble` with a registered request and discovery hint.

Observed output:

```text
FORGED_CONTEXT_OUTCOME ASSEMBLED
FORGED_CONTEXT_INCLUDED ['scene-forged']
```

The Context result therefore carries `current=True` and `eligible=True` in its
post-resolution basis even though no trusted composition route issued the host
or its repository.

### Probe B — the same forged host mints accepted LOCAL history

The probe created another nominal `BoundContextRuntime`, installed a
caller-created repository returning a caller-created valid-looking semantic
event window, constructed `BoundNativeHistoryRuntime(forged_host)`, and called
`read_native_history`.

Observed output:

```text
FORGED_LOCAL_HISTORY_ORIGIN LOCAL
FORGED_LOCAL_HISTORY_EVENT event.gate_opened
```

The history validator proves the shape and interval of the supplied window,
but the host boundary does not prove that the repository/capability was issued
by the native composition authority. A forged host can consequently mint
accepted Context/`LOCAL` history from caller-supplied material.

## Affected owners and consumers

- `GAME/TOOLS/context_runtime.py` — `BoundContextRuntime`, host composition,
  Context candidate resolution and Context assembly.
- `GAME/TOOLS/history.py` — `BoundNativeHistoryRuntime`, native-history window
  adapter and `LOCAL` history publication/recovery.
- `GAME/TOOLS/live_state.py` — selected-LIVE read capability and LIVE
  currentness boundary relied on by Context and History; this boundary is not
  sufficient to authenticate the enclosing host composition.
- W03 LIVE/currentness, PLAYER/access and information/knowledge/disclosure
  owners, whose native evidence must not be reached through a forged Context
  host.
- W04.T05A Context consumers and dependent T05B/T05C/T06 Context/emission
  consumers; no dependent task may consume this admission basis.
- W04.T07A native-history consumers, because the same host shape can mint
  `LOCAL` history even when no LIVE capability is present.

## Protected invariants

- Caller-created objects, mappings, private attribute assignments, booleans,
  routes, repositories and capabilities cannot mint native currentness,
  eligibility or accepted history.
- Native LIVE, PLAYER/access, information, knowledge and disclosure owners
  remain the sole authorities for their domains.
- `LOCAL` history binds to accepted native campaign publication/currentness, not
  merely to a caller-supplied repository response that matches the schema.
- Context remains a bounded ephemeral projection and cannot establish truth,
  PLAYER/access, knowledge/disclosure, LIVE authority or history authority.
- History and Context have one trusted composition authority; structural
  `isinstance` checks and caller-replaceable host fields are not that authority.
- No second authority, local token/registry, generic callback authority,
  durable Context state or unapproved protocol is introduced as a workaround.

## What can proceed without the disputed change

- Preserve this brief and the existing fail-closed tests as evidence.
- Perform read-only Senior/design resolution of the missing non-replaceable
  composition route.
- Continue only unrelated work with isolated owner/write sets.
- Do not claim `W04_CONTEXT_CURRENTNESS_ELIGIBILITY_READY` or advance T05B,
  T05C or T06 from this basis.
- Do not normalize the forged-host result by adding a local token, weak registry,
  constructor marker, or equivalent caller-visible capability test.

## Safe options

1. **Specify a concrete trusted composition route.** The owning design must name
   the actual composition root/entry point, its authority boundary, how the
   trusted `RepositoryPort` and selected-LIVE capability are obtained, and why
   a gameplay caller cannot replace the host or its capabilities. Context and
   History may then be repaired within that accepted route.
2. **Narrow the current implementation to fail closed.** Remove or disable the
   caller-replaceable host path until the concrete route is accepted. This
   preserves safety but does not complete T05A.
3. **Return the owner boundary to architecture/design.** If the repository has
   no existing non-replaceable composition route, resolve that missing boundary
   before changing Context, LIVE or History authority. A local marker, token,
   weak registry or registry-backed issuer is explicitly not an option.

## Recommendation

Keep W04.T05A stopped and return the missing composition boundary to
Senior/design. Prefer option 1 only after the route is concrete and
non-replaceable; otherwise use option 2 and fail closed. Do not accept nominal
`BoundContextRuntime`/`BoundNativeHistoryRuntime` instances as trusted merely
because they pass `isinstance`, expose private fields, or contain owner-shaped
records.

## Cost / risk if the recommendation is wrong

Resuming on the current boundary permits caller-controlled repositories,
selected-source material and host fields to produce apparently native Context
and `LOCAL` history. That can admit stale, forged, cross-campaign or
cross-role material, undermine replay/recovery provenance, and create duplicate
authority across Context, LIVE and History. Continuing the stop costs only the
Context/history implementation schedule; the missing composition decision is
not safely reversible after accepted material has been emitted.

## Version Impact Gate

```text
VERSION_IMPACT: NONE
```

This checkpoint changes only a development design/provenance document under
`DEV/docs/superpowers/design/`. No engine release, CORE/module revision,
persistent schema, campaign generation, storage/catalog/ruleset namespace,
protocol, or runtime projection changes. Any future production repair must
classify the actual Context, LIVE and History owner/consumer set from the
restored basis and must not reuse this documentation-only `NONE` result.

## System-Impact disposition and unpublished state

```text
SYSTEM_IMPACT: STOP / SENIOR-DESIGN REVIEW REQUIRED
UNPUBLISHED_WORK: NONE
```

No production, schema, test, cursor, `DEV/CURRENT_PROGRESS.md`, Wave-05, or
`.entire/` content was changed in this checkpoint. The forged-host defect
remains unresolved and is intentionally unpublished as a production repair
pending the named composition-boundary decision.
