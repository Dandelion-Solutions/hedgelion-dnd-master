# Independent re-review — W04.T07C targeted repairs

Status: **PASS / GO**

Date: 2026-09-25.

## Exact review basis

Public repository:
- reviewed remote HEAD: `df83bc7c37e1f1d0fdeebd583350bf377a4c8f37`;
- T07C repair implementation: `f114eb6a38c50d755cf71094d078c1d362f08bb4`;
- later commits through the reviewed HEAD modify only CURRENT_PROGRESS / Wave-04 execution-status evidence; production/schema/test bytes are unchanged from the repair checkpoint.

Prior findings:
- IRR-T07C-01 — retained T0 lacked historical protection/availability classification;
- IRR-T07C-02 — an exact already-covered older page was rejected after later coverage advancement.

Role: independent reviewer. This review modifies only review/control artifacts.

## Source Manifest

Current public machine evidence:
- `GAME/TOOLS/history.py` — T0 schema/version validation and exact native-event binding;
- `GAME/TOOLS/story.py` — E-EVT generation, Story EVENTS materialization, coverage/idempotency and W02 publication;
- `DEV/TESTS/test_rd13_story_t0_commentator.py` — repair regressions;
- `DEV/SCHEMAS/semantic-event-t0-basis.schema.json`;
- `DEV/SCHEMAS/story-event-unit.schema.json`;
- `DEV/SCHEMAS/story-projection-state.schema.json`;
- `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`;
- stable Wave-04 T07C/T07D plan;
- Step-5.10 Story projection durability owner;
- 2026-09-08 Story baseline projection-source contracts;
- 2026-09-09 self-contained Commentator corpus owner;
- 2026-09-05 versioning/compatibility policy.

Current cross-project evidence, freshly read because the public persisted Story/T0 contract changed:

Audit branch:
`dkolyada/hedgelion-dnd-master-lab@audit/cls-project-audit-workspace`
- head: `3bd4ffb1db0451d0079568d4ad58709372ef3a4d`;
- `CLS-AUDIT/CURRENT_AUDIT_STATE.md` blob `30ef4eea12a051ebe91929670a63eeb5a66aa453`;
- `CLS-AUDIT/graph/HDM_INTEGRATION_GRAPH.md` blob `6e2f44f2c3345f0d4a515cf303033dd07a52d890`.

Feature branch:
`dkolyada/hedgelion-dnd-master-lab@feature/commentator-language-stack`
- head: `2c5dc9f6a4f1c8a23b070e7520e7854491af5282`;
- `HDM-CLS/docs/CURRENT_PROGRESS.md` blob `0e086d69cf1ce48987aaf01aec5b0037d279f01b`;
- WP12-05 framing Source Manifest blob `58d8a60eb7ec1f245581dff5e1345dbaef554a8b`;
- WP12-05 executable package blob `35c8d958c2ef5c523e7a49765d4433f55283d497`;
- WP12-05 architecture acceptance blob `021325bfceceae6711463fe5ab575657ff17bea2`;
- WP12-05 implementation release blob `54538c29b8618fe07103dbf06db90cc761438d69`;
- Senior integration mailbox blob `0fc0ca7ef1072d6fd9614efe92e62f0807da838e`.

## Verification

Exact repair commit hosted run:
- run `36076362491`;
- job `107888337524`;
- head `f114eb6a38c50d755cf71094d078c1d362f08bb4`;
- conclusion SUCCESS;
- maintenance audit PASS;
- 1218 tests, 5 skipped;
- `VERSION_UNCLASSIFIED=[]`;
- `VERSION_LEGACY_HITS=[]`.

Exact current reviewed-head hosted run:
- run `36078547787`;
- job `107895116534`;
- head `df83bc7c37e1f1d0fdeebd583350bf377a4c8f37`;
- conclusion SUCCESS;
- maintenance audit PASS;
- 1218 tests, 5 skipped;
- `VERSION_UNCLASSIFIED=[]`;
- `VERSION_LEGACY_HITS=[]`.

The ordinary worker checkout's protected `.entire/` census contamination did not reproduce in hosted clean checkout. This review does not claim that environment issue repaired.

## IRR-T07C-01 — CLOSED

The retained T0 basis is now explicitly versioned as schema 2.

Every retained factor must contain exactly:
- `owner_family`;
- `factor_id`;
- `t0_value`;
- `provenance_refs`;
- `availability_classification`.

The admitted classification is `PUBLIC | PROTECTED`; missing, malformed or unregistered values fail closed.

The exact native SemanticEvent remains the owner of the retained basis. Story copies the validated basis unchanged. The repair tests prove that later Actor, knowledge and disclosure state are not read to reconstruct or rewrite historical factor protection.

This is sufficient for the T07C boundary:
- T07C retains comprehensive historical material and its protection class;
- T07D still owns the self-contained current eligibility/control projection and reader-specific anti-oracle filtering;
- a protected factor is retained in the Story corpus rather than omitted because a current reader is ineligible.

No Story/Commentator ACL authority is created.

## IRR-T07C-02 — CLOSED

Story publication revalidates the exact native page before consulting coverage.

After that exact source validation, a compatible page whose terminal upper ordinal is at or below current compatible Story coverage returns `ALREADY_COVERED` with:
- no Story ID allocation;
- no tree creation;
- no ref update.

Regressions cover:
- page 1 -> page 2 -> retry exact page 1;
- mutation of the old page after coverage advancement, which still fails before idempotent acknowledgement;
- incompatible coverage generation;
- uncovered/gapped page rejection.

This preserves Step-5.10's rule that coverage is catch-up idempotency evidence without weakening native currentness.

## Version Impact disposition

Accepted T07C realization:

```text
History module:                    1.0.4 -> 1.0.5
embedded T0 basis schema:          1 -> 2
Story module:                      1.0.7 -> 1.0.8
Story EVENTS unit schema:          3 -> 4
E-EVT semantic contract generation 1 -> 2

runtime.semantic_event outer schema: 1 unchanged
Story projection-state schema:       4 unchanged
durability module:                    1.0.4 unchanged
campaign_contract_generation:         2 unchanged
storage/catalog/engine generations:   unchanged
migration / dual read:                NONE
```

The unchanged outer SemanticEvent schema is acceptable because the retained T0 basis is an explicitly self-typed nested contract carrying its own schema version; the SemanticEvent envelope/identity fields did not change. E-EVT generation 2 prevents old generation-1 Story coverage from being silently reused under the new required projection semantics.

The Story projection-state family remains schema 4 because it already carries per-source `semantic_contract_generation`; incompatible generation-1 E-EVT coverage fails closed through that existing typed axis rather than changing the projection-state shape.

The pre-v1 clean-slate policy does not require a migration or aggregate campaign-contract bump solely to preserve unshipped obsolete candidate shapes. If released/adopted data requiring conversion is later discovered, that is a new explicit migration/adoption gate.

## Fresh CLS↔HDM reconciliation

The public change does fire the recorded "fresh reconciliation" trigger because persisted Story/T0 realization and E-EVT generation changed.

Fresh current private evidence does **not** require a public semantic reopen or public write:

- current WP12-05 remains a private normalized/synthetic host package;
- it does not claim REAL public-HDM wire acceptance;
- its current package explicitly leaves independent source/content/control freshness and REAL source normalization to WP12-08;
- current feature state does not make public Story/T0 schema numbers a WP12-05 authority;
- the current private audit graph is therefore stale with respect to the newly accepted public machine versions, but it already records NO REAL ACCEPTANCE and a bounded future re-entry trigger.

Disposition:

```text
T07C_CLS_HDM_RECONCILIATION: PASS
PUBLIC_HDM_SEMANTIC_REOPEN_REQUIRED: NO
PUBLIC_HDM_WRITE_REQUIRED_BY_CLS: NO
CURRENT_PRIVATE_WP12_05_REPAIR_REQUIRED: NO
FUTURE_REAL_NORMALIZATION_OBLIGATION: YES
```

Before private CLS claims REAL integration/normalization, its own current process must reconcile the accepted public T0 schema 2 / Story EVENTS schema 4 / E-EVT generation 2. This is not a blocker for public T07D.

## Final disposition

```text
W04.T07C: PASS / GO
IRR-T07C-01: CLOSED
IRR-T07C-02: CLOSED
W04_T0_STORY_READY: ACCEPTED
W04.T07D: AUTHORIZED

T04B: still SYSTEM_IMPACT / SENIOR_DESIGN_REQUIRED
W04.T05C: BLOCKED by T04B
WAVE_05: NOT AUTHORIZED
```

The previous T04B finding and System-Impact producer-interface gap are not resolved or weakened by this review.
