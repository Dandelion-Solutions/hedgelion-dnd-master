# W03.T08 LIVE consumer semantic deltas and shipped inputs

Status: **OWNER-LOCAL IMPLEMENTATION INPUT — NOT A WAVE-05 FINAL-WRITER PATCH**

## Scope

W03.T08 joins the accepted current LIVE source to the existing information and
scene consumers without creating a second information, disclosure, scene, or
currentness authority.

The implementation is limited to the owner-local runtime/test surfaces and this
bounded input record. W04 is not started.

## Owner-local realization

- `GAME/TOOLS/information.py` resolves the observed source through the selected
  complete `LiveRouting` entry, extracts only exact-source, recipient-bound LIVE
  information candidates, and passes only admitted extraction results through
  the existing native lore, knowledge, disclosure, and message normalizers.
- `GAME/TOOLS/live_state.py` resolves the observed source through the selected
  complete `LiveRouting` entry before providing an ephemeral material/current-
  scene bridge bound to `(campaign_id, scene_id, epoch_id)`, the exact LIVE ref,
  exact source revision, and exact source-native ID history.
- A LIVE physical projection is evidence/input only. It cannot mint knowledge,
  disclosure, message, scene, principal, or currentness authority.
- Missing, orphaned, superseded and stale sources, stale source revisions,
  stale source-native history, recipient mismatch, direct unadmitted candidate
  construction, forged admission markers, post-admission evidence mutation,
  legacy visibility/perception fields, and pre-v1 branch/revision shapes fail
  closed. The candidate carries no trusted admission or snapshot; module-owned
  identity-keyed extraction state carries the immutable evidence snapshot, and
  there is no latest-looking or campaign-base fallback.

## Wave-05 shipped inputs

The following files remain deferred to their single Wave-05 final writers and
are supplied only as semantic input/delta requirements here:

- `GAME/CORE/LIVE_SCENE.md` — replace scene-centric LIVE wording with the
  source-native exact-current route and owner-bound information normalization
  semantics.
- `GAME/CORE/MULTIPLAYER.md` — point shared-scene reads through the principal
  route and exact selected source; retain recipient-scoped knowledge/disclosure
  separation.
- `GAME/SCHEMA/live_scene.schema.yaml` — replace the retained pre-v1 physical
  shape with the final shared machine contract.
- `GAME/SCHEMA/scene.schema.yaml` — narrow the live pointer to the final
  owner-typed route/currentness contract.

No file above is edited by W03.T08. Their current bytes remain protected by the
named T08 cutover suites.

## Impact envelope and gates

Expected changed owners are the existing information and LIVE runtime owners,
their owner-local tests, this design input, and the LIVE runtime module
version. No shared schema, catalog, multiplayer/scene CORE file, persistent
family, or Wave-05 final-writer authority changes.

`VERSION_IMPACT` is classified against the actual changed owner set at the
checkpoint. The System-Impact result is `NONE` while the implementation remains
inside these boundaries; a new owner, source/currentness authority, persistence
field, or cross-wave writer would require escalation before implementation.
