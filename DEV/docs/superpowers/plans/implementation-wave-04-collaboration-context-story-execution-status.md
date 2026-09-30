# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: EXECUTING — W04.T08A/T08B/T08C and T07A-E integration accepted/read back; A26-02 repair published and exact-head verified; final Senior integration audit pending
CURRENT_TASK: complete final Wave-04 review/audit handoff from verified implementation head `7b652995398c08a327542ce8b9db25f254cf74f1`. A26-02 proof/collection repair is accepted at the implementation-review and local verification level; no runtime/schema/CI changes were made. Wave 05 remains unauthorized.
LAST_COMPLETED_TASK: W04.T08C -> `W04_MULTIPLAYER_SESSION_DELTAS_READY`, candidate `46ea4a472c6a8d403ad96f6b60867b31b23bf98b`, seven convergence tests, independent review PASS; final exact DEV at status HEAD `aec602a828ef399673b58d2ccd7cb804b3baa5c2`: 1424 passed, 5 skipped, four A26-02 failures reproduced sequentially; maintenance PASS; version/provenance/current-progress 18 passed; `VERSION_IMPACT: NONE`. Non-force publication/read-back at `aec602a828ef399673b58d2ccd7cb804b3baa5c2`. W04.T08A -> `W04_MULTIPLAYER_CONSUMER_DELTA_READY`, code `48cd790d93b8d7cbbf883f086fcbeab34a4235df`, independent PASS and read-back at `2720a6187d5919fb2ca8c8f3265604814510d69b`. T08B/T03A and W04.T07-INTEGRATION remain accepted/read back; T07E/T07D and earlier W04 checkpoints remain retained.
LAST_SAFE_SHA: `7b652995398c08a327542ce8b9db25f254cf74f1` — published A26-02 proof/collection repair checkpoint, independently reviewed and full local verification PASS.

## W04.T07D / PO-012 / P0 current disposition — 2026-09-28

OWNER: `DEV/docs/superpowers/specs/2026-09-28-commentator-player-selected-pc-perspective-owner-decision.md`

SENIOR RULING: `DEV/docs/superpowers/design/2026-09-28-w04-t07d-commentator-control-senior-ruling.md`

```text
PO-012: INCORPORATED
PRODUCT_OWNER_DECISION_REQUIRED: NO
T07D-P0: ACCEPTED — independent PASS and fresh remote read-back at `d37ed9c1994e78feb51fc147cd3e2e5225b5a548`
OUTPUT: W04_COMMENTATOR_CONTROL_CONTEXT_READY
T07D: RESUMED / RED AUTHORIZED
T07A/B/C: ACCEPTED / NOT REOPENED
```

P0 is the smallest sufficient prerequisite: existing ContextService already
exact-reloads current PLAYER, world.knowledge, runtime.disclosure and
world.lore_fact. P0 registers the missing COMMENTATOR control profile and binds
an optional selected-PC subject to exact current PLAYER.controlled_pc_ids. It
does not issue Story permissions or change W03 owners.

P0 Version Impact: Context Runtime 1.0.8 -> 1.0.9; the ContextNeedProfile enum
expansion is ephemeral and has no persistent schema/generation, migration or
dual-read impact. Independent review PASS; RD11 + RuntimeHost focused tests 96
passed; clean committed-source full DEV 1358 passed, 5 skipped and 4 known
out-of-scope S6D failures; version/provenance/current-progress 18 passed;
maintenance, scoped Ruff/format, and diff checks PASS.


## W04.T04B-P0R implementation impact envelope

SPEC / APPROVED DESIGN: `DEV/docs/superpowers/design/2026-09-25-w04-t04b-postpublication-recovery-evidence-senior-ruling.md`; stable task `W04.T04B-P0R` in `implementation-wave-04-collaboration-context-story.md`.
IMPLEMENTATION START HEAD: `cfa6c907189dd22741954303dae51d36f7bc4962`.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/publication.py`, `GAME/TOOLS/runtime_host.py`.

EXPECTED OWNERS TO CHANGE: W02 publication evidence and bound RuntimeHost read-side revalidation only.
EXPECTED CONSUMERS TO CHANGE: W02 publication and RuntimeHost primary tests; existing P1 owner validator remains the consumer contract.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: bounded `CampaignPublicationService.revalidate_published_owner_delta(...)`; ephemeral recovery-basis and exact-instance W02 evidence realization. No RepositoryPort protocol change.

PROTECTED ARCHITECTURE INVARIANTS: H/C remain nominations until exact repository proof; C is a direct single-parent child of H with exact changed-path closure; D retains every attempted after-image and, where D != C, exact C-to-D ancestry. No field-equality authority, historical-principal reconstruction, persistence, second repository authority, or Git write.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD06 publication suite, RuntimeHost composition suite, relevant cross-owner tests, maintenance audit, scoped Ruff/format, clean exact-tree full DEV suite.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: `live_state.py`, `collaboration.py`, `access_control.py`, `story.py`, `durability.py`, RepositoryPort protocol, persisted schemas, Wave-05 shared surfaces. The unpublished T04B candidate remains preserved locally and excluded from P0R.
VERSION IMPACT: expected `publication.py 1.0.5 -> 1.0.6`; `runtime_host.py 1.0.9 -> 1.0.10`; fresh verification required. Persisted schema, campaign contract, storage/catalog/engine generations, and migration expected NONE.
SCHEMA / CATALOG / CHECKPOINT IMPACT: NONE expected; no persisted receipt/evidence.
MIGRATION IMPACT: NONE expected.
CURRENTNESS RE-READ SET BEFORE WRITE: fresh remote HEAD, this cursor, stable Wave-04 plan, P0R Senior ruling, impact brief, current publication/RuntimeHost owners, W02 primary tests, Step-5.6 and versioning owners.

## W04.T04B implementation impact envelope

SPEC / APPROVED DESIGN: W04.T04B row in `implementation-wave-04-collaboration-context-story.md`, P0/P1 owner rulings, and P0R Senior ruling `DEV/docs/superpowers/design/2026-09-25-w04-t04b-postpublication-recovery-evidence-senior-ruling.md`.
IMPLEMENTATION START HEAD: `29289288798fb4ba71578610cd83676b878510b6`.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/collaboration.py`, `DEV/TESTS/test_rd12_collaboration.py`.

EXPECTED OWNERS TO CHANGE: Collaboration's already-admitted consumer/recovery path only; W03 LIVE and access remain read-only producers; W02 P0R remains a read-only accepted service.
EXPECTED CONSUMERS TO CHANGE: same-closure collaboration access publication/recovery tests; P0R and the existing P1 composed-absorption classifier are consumed unchanged.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: no new cross-owner API; T04B rederives the exact P1 delta and joined write set, calls existing `CampaignPublicationService.revalidate_published_owner_delta(...)`, then consumes the fresh W02 outcome through existing P1 classification.

PROTECTED ARCHITECTURE INVARIANTS: one initial W02 transaction; cold recovery issues no create_tree/create_commit/update_ref, no LIVE CAS, no mechanics/RNG replay, and no acting-principal reauthorization; only exact P1 final route/source members and all joined W03 + PLAYER/access + Collaboration after-images are accepted; reconstructed P0/P1 values remain non-authoritative; no reverse access-control dependency.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD12 T04B recovery suite; RD09 composed-absorption consumer suite; P0R RuntimeHost/publication suites; zero-write and exact-source/currentness checks; clean full DEV and maintenance audit.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: W02 publication/runtime-host, W03 live_state/access_control, story/history, RepositoryPort protocol, persisted schemas, and Wave-05 shared surfaces.
VERSION IMPACT: fresh baseline confirms Collaboration `1.0.18 -> 1.0.19` is the task's single module bump. P0R `publication.py 1.0.6` and `runtime_host.py 1.0.10` remain unchanged; no schema, campaign-contract, storage/catalog/engine generation, migration, or dual-read change.
SCHEMA / CATALOG / CHECKPOINT IMPACT: NONE expected.
MIGRATION IMPACT: NONE expected.
CURRENTNESS RE-READ SET BEFORE WRITE: fresh `v1/engine-rearchitecture` HEAD `292892...`; current collaboration.py/test_rd12 candidate and neighboring T04B consumers; current P1/P0R accepted owners; stable Wave-04 plan; P0R ruling and Step-5.8 recovery law; module versioning owner.

## W04.T05C implementation impact envelope

SPEC / APPROVED DESIGN: T05C row in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`; accepted Context law in `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`; T05B + T02C + accepted T04B inputs.
IMPLEMENTATION START HEAD: `2bf08089daccfe9eb9bdb9b31bc5af0c34f5a70e`.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/context_runtime.py`, `DEV/TESTS/test_rd11_context_runtime.py`.

EXPECTED OWNERS TO CHANGE: Context Runtime recipient-scoped consumer path only.
EXPECTED CONSUMERS TO CHANGE: T05C Context join and exact current collaboration-owner projection tests.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: one fixed Context candidate resolver for `runtime.collaboration_obligation`, exact request/candidate scope/frontier matching, and recipient-safe ephemeral summary; no RuntimeHost/Collaboration/Access/History API change.

PROTECTED ARCHITECTURE INVARIANTS: Context remains ephemeral projection; current exact PLAYER and collaboration obligation owners outrank stale candidate bytes; only exact current PLAYER route companions admit a current nonterminal obligation; no other participant's input identity/content is included; current profile/recipient/frontier mismatches fail closed; retrospective collaboration candidates re-read current permission before any result and do not promote old projection bytes.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: Context Runtime suite, collaboration/access consumer tests, full RD11, T04B/P0R/P1 regressions, maintenance audit and full DEV.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: `GAME/TOOLS/collaboration.py`, `access_control.py`, `history.py`, `live_state.py`, `runtime_host.py`, schemas, persisted state, RepositoryPort, and Wave-05 surfaces.
VERSION IMPACT: fresh baseline `context_runtime.py 1.0.7 -> 1.0.8`; persisted schemas, campaign contract, storage/catalog/engine generations, migration and dual-read expected NONE.
SCHEMA / CATALOG / CHECKPOINT IMPACT: NONE expected; request schema retains its existing `source_frontier` field; no new persisted record.
MIGRATION IMPACT: NONE expected.
CURRENTNESS RE-READ SET BEFORE WRITE: fresh branch HEAD, CURRENT_PROGRESS and this cursor, T05C plan row, Context Runtime canonical spec, current Context Runtime/tests, accepted T04B/T05B/T02C outputs, Collaboration/PLAYER access owners and Versioning owner.

## PO-011 response-language owner reconciliation

OWNER: `DEV/docs/superpowers/specs/2026-09-26-player-facing-response-language-owner-decision.md`

```text
PO-011: INCORPORATED
T06A: NOT AFFECTED / MAY CONTINUE
T06B: MUST CONSUME OWNER BEFORE RED
PERSISTENT PLAYER/SESSION LANGUAGE STATE: NOT AUTHORIZED / NOT REQUIRED
VISIBLE FALLBACK LANGUAGE ON MISSING OPTIONAL POLICY/ASSET: FORBIDDEN
INTERNAL/DIAGNOSTIC TECHNICAL LANGUAGE: SEPARATE SURFACE
VERSION_IMPACT FOR THIS CONTROL RECONCILIATION: NONE
SYSTEM_IMPACT: NONE — existing presentation/emission boundary only
```

T06B binds one transient current `ResolvedResponseLanguage` across accepted Narrator phase/result/protected emission, keeps fallback IDs internal until language realization, and rejects internal/diagnostic text as ordinary Master output. Exact/diegetic foreign-language content does not itself switch the Master carrier language.

## W04.T06A implementation impact envelope

SPEC / APPROVED DESIGN: T06A row in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`; R2.4 single-context turn/rebind laws; WP-08 role/context realization; Step-4 role-containment amendment; accepted W02.T07 `W02_PROTECTED_EXECUTION_HANDOFF_READY`.
IMPLEMENTATION START HEAD: `3113b43c345b10efacebcacb003eba98aa025b05`.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/turn_runtime.py`; `DEV/SCHEMAS/turn-envelope.schema.json`, `interpreter-result.schema.json`, `preparation-draft.schema.json`, `actor-proposal.schema.json`, `story-projection-draft.schema.json`, `narration-result.schema.json`; `DEV/TESTS/test_rd10_role_emission.py`.

EXPECTED OWNERS TO CHANGE: registered TurnRuntime phase-rebinding and accepted Context-basis controls only.
EXPECTED CONSUMERS TO CHANGE: T06A role/result contract tests in `test_rd10_role_emission.py` plus the mechanically synchronized W02 handoff consumer fixture in `test_rd05_runtime_execution.py`; `emission.py` and the W02 execution-handoff producer remain read-only.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: bind logical role/subject/purpose/profile/Context basis and minimum typed prior results; reject untyped/raw bundles, traces and private diagnostics; no generic result bus or persistent state.

PROTECTED ARCHITECTURE INVARIANTS: TurnEnvelope remains transient control, not semantic or persistence authority; matching `bundle_id`/recipient or caller-shaped bundle alone cannot widen eligibility; Actor remains subject-local; Narrator freshly rebinds after Chronicler; only minimum accepted typed results cross phases; W02 accepted deterministic execution evidence remains owner-issued and mechanics/RNG are not replayed.
ARCHITECTURE-SENSITIVE SURFACES: ContextService/Context Runtime output as the accepted phase basis; TurnRuntime validation; protected emission consumer; all six registered turn/result schemas.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD10 role/emission suite; RD05 execution-handoff consumer tests; RD11 Context suite; relevant emission tests; maintenance audit and clean exact full DEV.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: `context_runtime.py`, `runtime_host.py`, `emission.py` implementation (T06B), `collaboration.py`, History/Story, GAME/CORE instruction files, persistent state, RepositoryPort, catalog, Wave-05. If T06A's required accepted-basis proof needs changing ContextService/Context Runtime ownership or another unplanned interface, stop at the System-Impact Gate before broadening the write set.
VERSION IMPACT: NONE — `turn_runtime.py` is unversioned GAME/TOOLS implementation support, not a versioned CORE instruction module; the six transient role/result schemas carry no HDM `schema_version` field and are not persistent record families. Campaign/storage/catalog/engine generations, migration and dual-read remain unchanged. Verify zero unclassified census hits at checkpoint.
SCHEMA / CATALOG / CHECKPOINT IMPACT: transient TurnEnvelope/result schema changes only; no persistent record, catalog, campaign checkpoint, or migration expected.
MIGRATION IMPACT: NONE expected.
CURRENTNESS RE-READ SET BEFORE WRITE: fresh branch HEAD, `CURRENT_PROGRESS` and this cursor, T06A plan row, current R2.3/R2.4/WP-08 and Step-4 role-containment owners, accepted W02.T07 and T05C outputs, current TurnRuntime/six schemas/RD10 tests, RD05 handoff consumer and `emission.py`, and Versioning owner.

## W04.T06B implementation impact envelope

SPEC / APPROVED DESIGN: T06B row in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`; accepted PO-011 owner `DEV/docs/superpowers/specs/2026-09-26-player-facing-response-language-owner-decision.md`; R2.3/R2.4 Context/TurnEnvelope/rebind law; WP-08 and Step-4 role-containment; accepted T06A `W04_ROLE_CONTEXT_HANDOFF_READY` + W02.T07.
IMPLEMENTATION START HEAD: `8174b41fcf8f6684d5c06acf2b0338fa894d6968`.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/turn_runtime.py`, `GAME/TOOLS/emission.py`, `DEV/SCHEMAS/turn-envelope.schema.json`, `DEV/SCHEMAS/narration-result.schema.json`, `DEV/TESTS/test_rd10_role_emission.py`; mechanically affected RD05 fixture `DEV/TESTS/test_rd05_runtime_execution.py`.

EXPECTED OWNERS TO CHANGE: transient Narrator language binding/currentness and protected emission validation/projection. Emission reads the existing accepted Context basis through TurnRuntime; ContextService/RuntimeHost producers remain unchanged.
EXPECTED CONSUMERS TO CHANGE: T06B RD10 role/emission tests and one mechanical RD05 handoff-fixture update; RD11 Context and RuntimeHost remain read-only regression consumers.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: bind one explicit nonempty opaque current `ResolvedResponseLanguage` to Narrator phase, typed narration result and protected emission; add a narrow current-phase accepted Context-basis read for emission; disclosure refs name only exact fact identities represented by eligible native information packets in that basis. No language registry, persistence, language inference or extra translation call.

PROTECTED ARCHITECTURE INVARIANTS: ordinary Master-to-human output uses current response language; missing optional policy/asset never authorizes another visible language; diagnostics remain separate; exact/diegetic foreign content does not switch the Master carrier language; no persistent player/session preference; no extra model call solely for translation; shaped bundle data cannot widen accepted Context/disclosure eligibility; W02 owner-verified handoff remains required where applicable.
ARCHITECTURE-SENSITIVE SURFACES: Narrator TurnRuntime binding/currentness, accepted Context basis at emission, disclosure source refs, narration-result schema, finite fallback identifier/text separation.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD10, RD05 handoff consumer, RD11 Context, RuntimeHost composition/data-plane override tests, full DEV, maintenance audit, version namespace/provenance tests.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: Context Runtime/RuntimeHost producer APIs, Collaboration/Access/History, persistent PLAYER/session schemas, language-detection algorithms, global language registry, language-specific assets, GAME/CORE shipped instructions (W05), disclosure-policy ownership, mechanics/RNG, diagnostic presentation realization, extra translation call. Any need to change these owners or semantics is a System-Impact Gate.
VERSION IMPACT: NONE expected — TurnRuntime/emission are unversioned support and turn/NarrationResult schemas are transient/non-persistent; perform exact Version Impact Gate and census before checkpoint.
SCHEMA / CATALOG / CHECKPOINT IMPACT: transient TurnEnvelope/NarrationResult shapes only; no persistent record, catalog, campaign checkpoint, migration, or dual-read.
MIGRATION IMPACT: NONE expected.
CURRENTNESS RE-READ SET BEFORE WRITE: fresh active-ref HEAD, CURRENT_PROGRESS/cursor, T06B plan row, accepted PO-011 owner, current R2.3/R2.4/WP-08/Step-4/emission owners, accepted T06A/W02 handoff, current turn_runtime/emission/two schemas/RD10 tests, RD05 if mechanically affected, and Versioning owner.

## W04.T06B implementation verification state

T06B_TDD_RED_GREEN: observed RED for missing current `ResolvedResponseLanguage`, caller-shaped disclosure widening, a sourced fact rejected when only the accepted Context basis carried it, and a registered `DEGRADED` status token embedded in prose. Current candidate closes those cases.
T06B_FOCUSED_VERIFICATION: RD10 + RD05 + RD11 + RuntimeHost composition: 170 passed. Scoped Ruff checks pass for TurnRuntime, emission, RD10, and the RD05 changed fixture (ignoring only the three recorded whole-file baseline codes for RD05); `git diff --check` passes.
T06B_FULL_DEV_DIAGNOSTIC: exact command `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto`, run in an uncommitted detached candidate verification copy: 1333 passed, 5 skipped, 5 failed. Four failures were known out-of-scope S6D tests; the fifth was expected dirty-worktree package provenance. This diagnostic is superseded by the clean committed-source evidence below.
T06B_CODE_COMMIT: `9bf679fa6b6b5ac560198448d50f932f08b808eb` (`feat(w04): protect Narrator emission`), published in the accepted active-ref chain.
T06B_CLEAN_EXACT_FULL_DEV: exact committed-source run at `9bf679fa6b6b5ac560198448d50f932f08b808eb`: 1334 passed, 5 skipped, 4 known out-of-scope S6D failures; package provenance reports `clean_head`. All four failures reproduced sequentially on this exact commit: `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`; `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`; `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`; `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`. Full command: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto`.
T06B_VERSION_AND_MAINTENANCE: version namespace policy suite 12 passed; combined package-provenance/current-progress suite on final status commit 18 passed; clean exact candidate census has no unrelated `.agents`, `.lavish`, `.entire`, nested-checkout or bytecode contamination; canonical maintenance audit PASS. `VERSION_IMPACT: NONE` — TurnRuntime/emission are unversioned support and both changed schemas are transient/non-persistent.
T06B_FORMAT_NOTE: scoped Ruff lint passes. Whole-file `ruff format --check` still reports existing formatting drift in RD05, RD10, TurnRuntime and emission; no broad reformat was applied. The new/changed hunks have no remaining Ruff formatting suggestions.
T06B_INDEPENDENT_REVIEW: **PASS** — final scoped hdm-reviewer reviewed the nine T06B files against base `8174b41fcf8f6684d5c06acf2b0338fa894d6968`, reran RD10 + RD05 + RD11 + RuntimeHost (170 passed), probed registered-token boundary behavior, and found no remaining findings or System-Impact concern. The reviewer confirmed the exact Context packet identity mapping and transient VERSION_IMPACT: NONE classification. The six pre-existing `.agents/skills/` edits and untracked `DEV/.lavish/` were excluded and left untouched.
T06B_PUBLICATION_READBACK: non-force push of the T06B implementation, verification and routing commits succeeded. Subsequent `git fetch --prune origin` confirmed local HEAD and `origin/v1/engine-rearchitecture` equal `9b7ac9825f90b1994fc33bf209834d1b0f2934ad`.

## W04.T07D implementation impact envelope

SPEC / APPROVED DESIGN: T07D row in the stable Wave-04 plan; PO-009 owner decision `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md`; WP-18 Story/Commentator spec; Story producer/persistence/retrospective contract; baseline Story projection source contracts; current W03 information/access owners; accepted T07A/T07B/T07C.
IMPLEMENTATION START CODE BASE: `b6b7e8925727394482a62ace335beb0a05ed733d` (freshly fetched published tree; subsequent cursor update is documentation-only).
CURRENT_RESUMPTION_BASE: `464a86ef687f5005274b9be8b6c00247ac07529a` — published P0 acceptance/cursor checkpoint before T07D RED.
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/commentator.py`, Commentator-owned schemas, `DEV/TESTS/test_rd13_story_t0_commentator.py`.

EXPECTED OWNERS TO CHANGE: Commentator's self-contained control/snapshot and deterministic pre-materialization filter only; Story/history and W03 information/access owners are read-only producers.
EXPECTED CONSUMERS TO CHANGE: T07D Commentator cases in RD13, with relevant T07C/Story and W03 access-information tests as regression consumers.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: the already admitted Commentator control/snapshot representation and its deterministic filter. No new ACL, knowledge, disclosure, Story, history, or currentness authority; no native-only fallback for qualifying retained T0 factors.

PROTECTED ARCHITECTURE INVARIANTS: arbitrary player-to-story-ID mappings cannot mint eligibility; `CONTENT_FINAL` is not `ACCESS_FINAL`; content and eligibility/control bases remain distinct; changed control refreshes filtering even with unchanged content; IDs/counts/titles/relations/pagination/navigation for ineligible material are removed before model materialization; required private/off-screen T0 basis is retained in the comprehensive corpus and availability-filtered, not omitted.
ARCHITECTURE-SENSITIVE SURFACES: snapshot/control basis identity and versioning, content/control currentness, recipient-safe pre-materialization filtering, retained T0 local recoverability.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD13 T07D witnesses, accepted T07C/Story consumer regressions, current W03 information/access consumers, full DEV, maintenance, schema/version/provenance checks.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: T07A/T07B/T07C producers/semantics, W03 information/access producers, Context Runtime, History/Story producer, T07E/Dramaturg, GAME/CORE and shared final-writer schemas (Wave 05), native Master fallback, unrestricted retrieval. Preserve the recorded CLS↔HDM preflight result and triggers; no rerun/reopen absent a concrete new public semantic trigger.
VERSION IMPACT: classify every actually changed Commentator schema against its persistence/local-version owner and aggregate campaign-generation rule. Do not infer NONE solely from filename; no bump is presumed before that assessment.
SYSTEM IMPACT: NONE expected inside the admitted Commentator consumer boundary; stop before any need to change T07A-C or W03 owner interfaces/semantics.

## W04.T07D implementation candidate, review and verification

```text
CANDIDATE_CODE_SHA: 3e80ecb187bd6474471ed53bc08424b5270f4dbb (published; fresh fetch/read-back confirmed in chain through `591791ef9242e2b4d5dc1d840e5b268dd78c0165`)
OUTPUT: W04_COMMENTATOR_CONTROL_READY
TDD: RED/GREEN reported and recorded by implementer
INDEPENDENT_REVIEW: PASS — spec compliance and task/code quality
```

Focused exact-candidate verification in the active checkout:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd11_context_runtime.py::CommentatorControlProfileTests
111 passed
```

Full DEV diagnostic in the current main worktree:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto
1368 passed, 5 skipped, 11 failed
```

Four are the known out-of-scope S6D cases; all four were reproduced sequentially on this candidate with the same contract mismatches. Seven are workspace-contamination failures: `test_runtime_package_provenance::{test_built_zip_contains_one_generated_root_provenance_member,test_clean_checkout_metadata_records_exact_head}`, `test_game_dev_layout::test_runtime_marker_is_unique`, `test_release_game_passthrough::test_new_game_root_file_and_directory_are_automatically_archived`, `test_release_integration::test_canonical_entry_point_builds_reproducible_flat_runtime_and_generator_smoke`, `test_s6d_11_ruleset_package_closure::test_transitional_identity_keys_are_absent_from_current_carriers`, and `test_versioning_namespace_policy::test_census_has_zero_unclassified_hits`. The release/package census reads preserved `.entire/tmp` session artifacts; root-marker census includes two pre-existing detached trees under `DEV/tmp`; the version scan also reads `.entire/` and `DEV/.lavish/`. No T07D/RD13/P0 test failed.

Main-worktree maintenance command `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py` returned FAIL with two workspace findings: duplicate `ENGINE_VERSION.yaml` under the two existing `DEV/tmp` checkouts and a `.entire/tmp` transitional-identity artifact. It did not report a T07D contract/owner defect.

CLEAN_EXACT_SOURCE_FULL_DEV_AND_MAINTENANCE: SATISFIED BY COMPOSED EXACT-HEAD EVIDENCE. No literal clean `pytest -n auto` rerun was available because the shell denied the existing detached worktree. Instead:
- dirty-worktree full pytest on the exact candidate produced 1368 passed, 5 skipped, 11 failed;
- four failures are the separately reproduced known A26-02 pytest-only S6D REDs;
- the other seven failures were all workspace-artifact-sensitive `unittest.TestCase` tests;
- exact remote HEAD `c963ff15af22c79581441f63afd59e5cb8ea4c5b` then ran hosted `Validate engine source` run `36558943551` in a fresh GitHub checkout;
- hosted `Run full maintenance audit`: PASS;
- hosted canonical `.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v`: PASS;
- all seven dirty-only artifact-sensitive tests are part of that unittest discovery surface and therefore passed clean at the exact published head.

This closes the task-local clean verification gap without reclassifying the four pytest-only S6D REDs; those remain A26-02.

VERSION_IMPACT: `commentator-control-projection.schema.json` 1 -> 2; `commentator-snapshot.schema.json` 1 -> 2. `campaign_contract_generation`, `storage_format_generation`, `catalog_generation`, engine release, any existing Commentator module-version namespace, migration and dual-read: NONE. The changed schemas define local Commentator consumer-cache contracts; no campaign-persistent family or storage writer changed.

CURRENT_DISPOSITION: **ACCEPTED / W04_COMMENTATOR_CONTROL_READY** — implementation/review PASS, publication/read-back PASS, composed clean exact-head verification PASS. T07E is authorized.

T07D_PUBLICATION_READBACK: `git fetch --prune origin` confirmed local HEAD and `origin/v1/engine-rearchitecture` at `591791ef9242e2b4d5dc1d840e5b268dd78c0165`, containing candidate code `3e80ecb187bd6474471ed53bc08424b5270f4dbb`.

## W04.T07E implementation impact envelope

SPEC / APPROVED DESIGN: W04.T07E row in the stable Wave-04 plan; R2.5 two-level multiplayer Dramaturg coordination; WP-18 Story/Dramaturg canonical specification, especially §§5–10 and §§13–15; accepted Story/T0 source contracts; existing R2.3 `profile.dramaturgy` and RuntimeHost/W02 publication owners.
IMPLEMENTATION START HEAD: `b97610d00b41c274742cc5ec57c94463e34b1811` (freshly fetched accepted T07D status/read-back head).
PRIMARY OWNER ARTIFACTS: `GAME/TOOLS/dramaturg.py`, `DEV/SCHEMAS/dramaturg-horizon.schema.json`, `GAME/TOOLS/runtime_host.py` (narrow W02 measurement), `DEV/TESTS/test_rd13_story_t0_commentator.py`, `DEV/TESTS/test_runtime_host_composition.py`.

EXPECTED OWNERS TO CHANGE: Dramaturg retained-horizon value validation, current admission, bounded publication, owner-local generation and safe rebase; one generic, side-effect-free exact serialized-byte measurement capability at the W02/RuntimeHost publication boundary.
EXPECTED CONSUMERS TO CHANGE: T07E Dramaturg horizon/publication/admission/rebase/size-review tests in RD13; W02/RuntimeHost measurement contract tests. The capability is reusable across similar W02 path-operation writers; T07E is the current consumer, not an automatic retrofit of unrelated owner lanes.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: Dramaturg horizon schema/value and owner-local functions; add exact per-path UTF-8 measurement using the same serializer as `create_tree`, callable through the bound RuntimeHost/W02 service. W02 accepted publication outcome/transaction semantics remain unchanged. T07E measures before publication; review/partition-band candidates require an ephemeral trusted owner outcome bound to exact candidate, fixed route and byte count, never persisted or caller/model/campaign supplied. No root selector/catalog/Context/W03/Story/Commentator/TurnRuntime change.

PROTECTED ARCHITECTURE INVARIANTS: exactly shared + stable-PLAYER-local retained families are active only in multiplayer; single-player preparation is ephemeral; route identity is stable `player_id`; player-local shared basis is exactly ABSENT or BOUND and BOUND retains the exact generation/bounded identity; entries use only accepted planning classes; native owners outrank planning; source basis stays owner-typed with no universal revision scalar; generation is monotonic owner-local metadata and only a successfully published generation is retainable; candidates cannot self-authorize; incompatible/stale state is discarded/reprepared, never text-merged/LWW; no planning-as-canon, chronology, PC agency, knowledge/disclosure, Actor, gameplay, native-history, catch-up or raw-Narrator authority; no global planning scans.
ARCHITECTURE-SENSITIVE SURFACES: current mode/PLAYER/role admission, owner-typed source basis, horizon scope/shared-generation identity, exact pinned base and successful non-force publication outcome, rebase conflict handling, retention/privacy containment.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD13 T07E cases plus relevant existing RuntimeHost/W02 publication, Context `profile.dramaturgy`, PLAYER/mode and T07C/T07D regressions; schema validation, Version Impact/provenance, full DEV, maintenance and scoped Ruff/format.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: T07A/B/C/D implementations and semantics; W02 publication/transaction behavior beyond exact measurement; W03/PLAYER/access/Context producers; Story/T0/history writers; T06 Narrator, Commentator, catch-up/session, Actor/mechanics/RNG; catalogs, `GAME/CORE`, campaign templates/scaffolds, Wave-05 final writers, A26-02 and T07-INTEGRATION. No persisted single-player planning owner, global planning registry/index/scheduler, root selector, universal freshness vector, hard size cap or new partition route.
VERSION IMPACT: classify the actual Dramaturg horizon schema and any persistent generation contract independently; do not infer NONE from scope/file location. `dramaturg.py` has no current module-version field. Determine whether local schema and campaign-contract/storage/catalog/engine/migration/dual-read changes are required under the current versioning owners.
SYSTEM IMPACT AT TRIGGER: TRIGGERED — the current W02/RuntimeHost campaign publication path did not expose the exact emitted serialized UTF-8 bytes required by the current mutable-artifact sizing owner. The T07E Senior resolution below authorizes only a bounded exact-measurement capability.

## W04.T07E historical System-Impact trigger — exact published-byte measurement (resolved below)

IMPACT_BRIEF: `DEV/docs/superpowers/design/2026-09-29-w04-t07e-dramaturg-size-impact-brief.md`.
TRIGGER: T07E publishes mutable campaign-tree `DRAMATURG/*.yaml` artifacts, while the current runtime mutable GitHub-artifact sizing owner requires the writer to measure exact final serialized UTF-8 bytes before publication and apply target/review/partition bands. T07E receives only mapping-valued `path_operations` through `RuntimeHost.CampaignPublicationService`; its transport interface does not expose emitted file bytes or exact byte-size evidence. Dramaturg's internal canonical JSON is not the transport YAML serialization. T07E's direct write envelope excludes W02/RuntimeHost changes.
LAST_SAFE_SHA: `f60246abeca880b0d6c39c34feea99347a1be3e0` — accepted T07D plus published T07E task-envelope checkpoint.
CURRENT_TASK_AT_TRIGGER: W04.T07E; local candidate commits were not published/accepted at the original measurement boundary stop.
APPROVED SPEC / PLAN EXPECTATION: stable W04.T07E row plus R2.5/WP-18 fixed two-family noncanonical horizon contract; exact size policy `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` §§2–4.
DISCOVERED IMPLEMENTATION PRESSURE AT TRIGGER: no in-scope exact serializer/measurement capability existed; JSON canonicalization, estimated size or arbitrary entry caps would not satisfy SIZE-5 and must not be presented as exact. The Senior resolution below authorizes only the bounded W02/RuntimeHost measurement extension.
AFFECTED OWNERS / CONSUMERS: `GAME/TOOLS/dramaturg.py`, `DEV/SCHEMAS/dramaturg-horizon.schema.json`, RD13; potential required extension is at `GAME/TOOLS/runtime_host.py` / W02 `CampaignPublicationService` or the existing host transport serialization boundary.
PROTECTED INVARIANTS AT RISK: exact final size measurement; no false hard cap/truncation; no unapproved partition/root selector; no persisted candidate treated as retained before accepted publication; noncanonical planning remains below native truth/authorization.
WHAT CAN PROCEED WITHOUT THE CHANGE: corrupt-horizon fail-closed repair is addressed locally; prior T07D remains accepted. No T07E code acceptance, publication or T07-INTEGRATION can safely proceed until the measurement boundary is resolved.
SAFE OPTIONS AT TRIGGER: Senior may authorize a narrow W02/RuntimeHost exact serialized-byte measurement capability and revise T07E's Impact Envelope, identify an already-approved exact serializer output usable within the existing interface, or keep T07E stopped. The first option was selected by the 2026-09-29 Senior/PO resolution below.
RECOMMENDATION AT TRIGGER: stop before T07E acceptance/publication and obtain Senior disposition on the exact-size measurement boundary and any required scope expansion. This stop was resolved by the ruling below.
COST / RISK IF WRONG: an unmeasured mutable horizon may exceed accepted operational bands; an estimate can undercount transport bytes, while a hard cap or invented split can deny valid planning or silently alter its contract.

```text
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED
T07E candidate code: `cd5c8a2ba78584ab0e1527d20b43db6ca443b417` + local corrupt-horizon fix `20dd239d109cb2221b85ebd62f217fac509c7a1e`; not published.
VERSION_IMPACT for candidate: `dramaturg-horizon.schema.json` 1 -> 2; pre-release campaign/storage/catalog/engine generations, migration and dual-read NONE under current clean-slate owner.
```

## W04.T07E Senior resolution — exact-size measurement scope

RULING: On 2026-09-29 the Product Owner/Senior authorized a narrow W02 exact serialized-byte measurement capability for all similar W02 path-operation cases and the required W02/RuntimeHost tests. This resolves the sizing System-Impact trigger to a bounded implementation prerequisite; it does not close T07E acceptance.

AUTHORIZED_SCOPE_DELTA: T07E may add one generic, side-effect-free exact per-path UTF-8 measurement capability in `GAME/TOOLS/runtime_host.py` and the necessary W02/RuntimeHost tests, with T07E using it before publication. The measurement must use the same serializer as `CampaignPublicationTransport.create_tree`. W02 publication outcome, transaction and accepted-evidence semantics remain unchanged; no unrelated W02 writers are automatically pulled into this task.

SIZE_REVIEW_DISPOSITION: review/partition-band Dramaturg payloads remain unpublished until a trusted ephemeral Dramaturg-owner review outcome is supplied, bound to the exact candidate, fixed route and measured byte count. The outcome is not persisted and cannot be supplied by model, request or campaign data. No hard byte cap or new partition route is authorized.

VERSION_IMPACT_EXPECTATION: Dramaturg horizon schema `1 -> 2`; RuntimeHost `1.0.10 -> 1.0.11` if the measurement capability is a material module edit. Fresh task-local Version Impact Gate is required. Campaign/storage/catalog/engine generations, migration and dual-read remain NONE unless the actual delta changes their owning semantics.

CURRENT_DISPOSITION: `W04_COMMENTATOR_DRAMATURG_READY` ACCEPTED — exact measurement, size-review defer, tests, independent task review, local verification and publication/read-back PASS. T07-INTEGRATION is PASS; T08A inputs are satisfied.

## W04.T07E implementation/review checkpoint

```text
OUTPUT: W04_COMMENTATOR_DRAMATURG_READY — ACCEPTED
CODE: `cd5c8a2ba78584ab0e1527d20b43db6ca443b417` + fix `20dd239d109cb2221b85ebd62f217fac509c7a1e` + W02 measurement/review integration `421516689e6ed766eadf1045571eff3078971328` + trusted-outcome TCB fix `c34c5b20f0657052e4a152bd21abe5fe11202f2d`
INDEPENDENT_REVIEW: PASS for spec compliance/task quality after corrupt-horizon repair and value-bound ephemeral review outcome; no remaining task-local finding.
PUBLICATION/READBACK: PASS — T07E code candidate `c34c5b20f0657052e4a152bd21abe5fe11202f2d` and synchronized status checkpoint `1e3ddfa71e285513ce0d86e6a16096fcf527eeaf`; fresh fetch confirmed local HEAD and `origin/v1/engine-rearchitecture` equal `1e3ddfa71e285513ce0d86e6a16096fcf527eeaf`.
```

Controller focused exact-candidate run: RuntimeHost composition + RD13 + RD11 + RD09 — **418 passed**, two existing `RefResolver` deprecation warnings. Scoped Ruff/format and diff checks PASS. The earlier current-worktree DEV diagnostic was **1400 passed, 5 skipped, 11 failed**; four are the known A26-02/S6D failures and seven were preserved-workspace contamination checks. On 2026-09-30, the clean exact-candidate full DEV run at `c34c5b20f0657052e4a152bd21abe5fe11202f2d` reported **1411 passed, 5 skipped, 4 failed**; all four are the separately tracked A26-02/S6D cases and each reproduced sequentially with the same failure. Clean package provenance passed. Version namespace + package provenance + current-progress suite: **18 passed**. Canonical maintenance audit: PASS. No preserved artifacts were cleaned. Hosted CI is unavailable in this local-machine runtime; no hosted result is claimed for T07E.

VERSION_IMPACT: RuntimeHost `1.0.10 -> 1.0.11`; Dramaturg horizon schema `1 -> 2`; campaign contract generation 2, storage generation 3, catalog generation 2, engine release, migration and dual-read NONE under the current clean-slate owner. No DEV bookkeeping revision.
T07E_STATUS_SYNCHRONIZATION_VERSION_IMPACT: NONE — this progress, cursor and impact-brief synchronization changes no HDM-owned version/revision/schema/generation namespace; the T07E runtime/schema transitions are recorded above.

T07E_CLEAN_EXACT_FAILURES: `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`; `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`; `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`; `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`. All four are outside T07E scope and remain A26-02; the focused sequential rerun reproduced all four. No T07E/RD13/RD11/RuntimeHost-focused test failed.

The external deployment transport implementation is not in this repository. It must implement the new measurement capability using the same serializer as `create_tree`; when missing, RuntimeHost fails closed. This is a rollout dependency, not an estimated measurement.

## W04.T07-INTEGRATION independent review — 2026-09-30

REVIEWED_HEAD: `3c61f636257f5febbfd47339e25a6be420852be9`
REVIEW: PASS — every T07A–T07E plan RED mapped to current owner/test evidence; no reverse authority edge or unaccounted version/migration impact.
REPORT: `DEV/docs/superpowers/design/2026-09-30-w04-t07-integration-independent-review.md`
VERIFICATION: declared repository environment, RD13 + RD11 + RuntimeHost composition unittest command, **224 passed**. No full DEV rerun was claimed by reviewer; latest exact T07E full DEV result and A26-02 disposition remain recorded above.
VERSION_IMPACT: NONE for review/status artifacts. T07E runtime/schema transitions remain as recorded above.
QUALIFICATIONS: no dedicated same-payload LOCAL/LIVE duplicate assertion; no positive source-classified omission-admission path; no distinct process-kill test for every T07A interruption point; no separate test attempting to persist a P0 result. The report records these as coverage limits, not T07 integration findings.
CLS↔HDM: recorded preflight preserved; not rerun and not reopened because no triggering semantic change was found.

## W04.T08A implementation impact envelope

SPEC / APPROVED DESIGN: W04.T08A row in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md:444–452`; accepted T04B and T02C inputs; T07-INTEGRATION PASS report above.
BASE_SHA: `3c61f636257f5febbfd47339e25a6be420852be9` (published T07-INTEGRATION-reviewed source).
EXPECTED OWNERS TO CHANGE: `DEV/TESTS/test_w04_t08_multiplayer_consumer_delta.py` and `DEV/TESTS/fixtures/w04_multiplayer_consumer_delta.json` only.
EXPECTED CONSUMERS TO CHANGE: the new T08A consumer-contract tests and bounded MULTIPLAYER delta; no runtime producer or shared final-writer bytes.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: describe/verify the admitted consumer delta only. Do not edit `GAME/CORE/MULTIPLAYER.md`, PLAYER/LIVE shared schemas, runtime authority owners or catalogs. Do not implement invitation, account-resolution, or login UI behavior; PO-005 runtime realization is deferred outside this T08A consumer-delta scope.
PROTECTED INVARIANTS: principal route -> candidate PLAYER IDs -> exact current PLAYER reload; no PLAYER_INDEX/scan authorization; catch-up reads current collaboration/history/access only; planning/private input excluded; login remains human selection/display while stable account ID is the binding.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: T08A mandatory REDs, exact delta fixture contract, T02C/T04B/T07 integration consumers, current-progress/version/provenance checks and maintenance as required by the approved plan.
VERSION IMPACT: NONE expected for DEV tests and the bounded DEV consumer-delta record; classify the actual changed set under the version owner before checkpoint.
SYSTEM IMPACT: NONE expected. If correct evidence requires a runtime/shared-schema/final-writer change, stop before broadening scope.

T08A_TDD: six consumer-delta assertions first failed because the bounded fixture was absent; after fixture creation all six pass. A reviewer finding that had scoped the scan prohibition to unbounded scans was repaired by changing the contract/test to forbid repository/directory scans as authorization; the targeted failure was observed before the fixture update.
T08A_FOCUSED_VERIFICATION: canonical RD12 + RD16 + T08A + T08B unittest set — 170 passed, 5 skipped. Focused T08A + T08B + T03A + T02C join/catch-up + RD09 principal authorization pytest selection — 38 passed, 2 existing `jsonschema.RefResolver` deprecation warnings. Scoped Ruff check/format and JSON parse: PASS.
T08A_INDEPENDENT_REVIEW: PASS after scan-scope repair. All five plan REDs represented; no runtime/shared-schema change; PO-005 runtime realization remains deferred.
T08A_CLEAN_EXACT_FULL_DEV: candidate commit `48cd790d93b8d7cbbf883f086fcbeab34a4235df` — **1417 passed, 5 skipped, 4 failed**. All four are the separately tracked A26-02/S6D nodes and were reproduced sequentially with the same failures; no T08A/T02C/T03A/T08B/RD09 regression failed. Clean package provenance and version/progress tests passed.
T08A_A26_FAILURES: `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`; `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`; `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`; `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`.
T08A_CLEAN_MAINTENANCE: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py` — PASS (`OK: engine consistency audit passed`).
T08A_VERSION_IMPACT: NONE — only DEV tests and a bounded DEV consumer-delta fixture changed; no HDM-owned runtime/module/schema/generation namespace changed.
T08A_SYSTEM_IMPACT: NONE — task remains inside the approved consumer-delta boundary.
T08A_CURRENT_DISPOSITION: **ACCEPTED / W04_MULTIPLAYER_CONSUMER_DELTA_READY** — test/delta implementation, independent review, clean exact local verification and maintenance PASS.
T08A_PUBLICATION_READBACK: PASS — code candidate `48cd790d93b8d7cbbf883f086fcbeab34a4235df` and verification/status checkpoint `2720a6187d5919fb2ca8c8f3265604814510d69b`; fresh fetch confirmed local HEAD and `origin/v1/engine-rearchitecture` equal `2720a6187d5919fb2ca8c8f3265604814510d69b`.

## W04.T08C implementation impact envelope

SPEC / APPROVED DESIGN: W04.T08C row in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md:464–472`; accepted inputs T08A, T08B and T03A.
INPUT_ACCEPTANCE: T08A code/read-back `48cd790d93b8d7cbbf883f086fcbeab34a4235df` / `2720a6187d5919fb2ca8c8f3265604814510d69b`; T08B read-back `468bd3400183ada85b76cd93737005aa1e1e64a7`; T03A reviewer-PASS code `ca3efa3c7750cffc2eef228b4b8666b75828cea9` and acceptance-status commit `b737555b9d9a1c404576dc173dfdaf34cd023e13`.
BASE_SHA: `2720a6187d5919fb2ca8c8f3265604814510d69b` (published T08A checkpoint).
EXPECTED OWNERS TO CHANGE: `DEV/TESTS/test_w04_t08_consumer_convergence.py` and `DEV/TESTS/fixtures/w04_multiplayer_session_deltas.json` only.
EXPECTED CONSUMERS TO CHANGE: T08C convergence tests and the bounded task-local MULTIPLAYER/SESSION/PLAYER consumer-delta evidence; no runtime producer or physical final-writer bytes.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: a development-only convergence delta and its tests. Do not edit `GAME/CORE/MULTIPLAYER.md`, `GAME/CORE/SESSION.md`, PLAYER/LIVE/session schemas, runtime authority owners or catalogs.
PROTECTED INVARIANTS: no shared final-writer bytes changed; no scan/index authorization; no Dramaturg/planning leakage; campaign, LIVE, PLAYER and currentness fields each retain one native owner with no universal cross-domain currentness scalar.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: T08C assertions over accepted T03A/T08A/T08B delta fixtures; relevant T02C/T04B/T07 source/consumer tests; version/provenance/current-progress checks; clean exact full DEV and maintenance audit.
VERSION IMPACT: NONE expected for DEV tests/evidence only; classify the actual changed set before checkpoint.
SYSTEM IMPACT: NONE expected. Any need for runtime, shared-schema or final-writer changes is outside this plan row.
T08C_TDD: six convergence assertions first failed because the bounded convergence delta was absent; after fixture creation the suite was GREEN. The independent review repair added explicit T03A/T08A PLAYER_INDEX fallback and stable-ID/login assertions; the final T08C suite has seven passing tests.
T08C_FOCUSED_VERIFICATION: canonical T08A/T08B/T03A/RD12/RD16/T08C unittest set — 177 passed, 5 skipped. T08C-specific pytest suite — 7 passed. Scoped Ruff check/format and JSON parse: PASS.
T08C_INDEPENDENT_REVIEW: PASS after repair. First review's targeted repair required explicit T03A/T08A PLAYER_INDEX and stable-ID/login assertions; those are now asserted against the accepted input fixtures. No runtime/shared-schema changes.
T08C_VERSION_IMPACT: NONE expected — DEV test and bounded consumer-delta fixture only; no HDM-owned runtime/module/schema/generation namespace.
T08C_SYSTEM_IMPACT: NONE — no owner boundary or final-writer scope changed.
T08C_CLEAN_EXACT_FULL_DEV: candidate commit `46ea4a472c6a8d403ad96f6b60867b31b23bf98b` — **1424 passed, 5 skipped, 4 failed**. The exact four A26-02/S6D failures from the T07E/T08A diagnostics were reproduced sequentially; no T08C/T08A/T08B/T03A/RD12/RD16 regression failed. Clean package provenance, version namespace and current-progress checks passed.
T08C_A26_FAILURES: `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`; `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`; `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`; `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`.
T08C_CLEAN_MAINTENANCE: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py` — PASS (`OK: engine consistency audit passed`).
T08C_FINAL_STATUS_HEAD_FULL_DEV: `aec602a828ef399673b58d2ccd7cb804b3baa5c2` — 1424 passed, 5 skipped, the same four A26-02 failures; no T08C failure. Fresh run on this exact HEAD.
T08C_FINAL_STATUS_HEAD_VERSION_AND_MAINTENANCE: version-namespace + package-provenance + current-progress suite 18 passed; canonical maintenance audit PASS.
T08C_CURRENT_DISPOSITION: **ACCEPTED / W04_MULTIPLAYER_SESSION_DELTAS_READY** — implementation, review, clean exact verification and non-force publication/read-back PASS; `VERSION_IMPACT: NONE`.
T08C_PUBLICATION_READBACK: PASS — code candidate `46ea4a472c6a8d403ad96f6b60867b31b23bf98b` and synchronized status `aec602a828ef399673b58d2ccd7cb804b3baa5c2`; fresh fetch confirmed local HEAD and `origin/v1/engine-rearchitecture` equal `aec602a828ef399673b58d2ccd7cb804b3baa5c2`.
T08C_STATUS_SYNCHRONIZATION_VERSION_IMPACT: NONE — this progress/cursor/impact-brief acceptance/read-back synchronization changes no HDM-owned version/revision/schema/generation namespace.

## A26-02 S6D proof/collection repair impact envelope

STATUS: required separate repair before final Wave-04 review; implementation, independent review and exact-head local verification PASS; no production/runtime behavior change was made.
BASE_SHA: `b081e6eeaeb6919c7d3dc01576171b532526e2df` (freshly fetched published T08C acceptance/status checkpoint).
SPEC / OWNER ROUTE: `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` §§3.2, 5 and 6; `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` §§2, 5 and 10 plus its S6D-09 amendment; `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` (“Builder and loader”; “Projections and durability”); four A26-02 test nodes listed below. A26-02 keeps these owner repairs separate from T07A–T08C.

ROOT-CAUSE DISPOSITION:
- S6D-04 fact test includes `fiction.target_reachable` in an all-dormant loop and supplies unauthorized `activity:def:1`; current owner admits `fiction.target_reachable` for seven exact S6D-09 consumers and keeps only `fiction.target_visible` dormant. Test active authorized false-vs-missing behavior separately; do not change runtime fact admission.
- S6D-05 embedding test infers edges from arbitrary filename text. The manifest is stale relative to actual direct schema `$ref` edges introduced by accepted later consumers. Repair the test to traverse exact `$ref` values and synchronize `DEV/CATALOG/portable-value-routes.json` with all current direct embedding consumers, without adding new values or consumers.
- Two S6D-05 continuation examples predate the currently required `ruleset_set_digest_generation`, `ruleset_set_sha256`, and `catalog_context_fingerprint_generation`; update only test examples using the current typed identities.
- The four affected tests are top-level pytest functions and `unittest discover -s DEV/TESTS` collected **0 tests** from the two modules. Add standard `unittest` `load_tests` collection adapters for the existing `test_*` functions in these two modules; do not change the canonical CI runner or add dependencies.
- `expect_rejected` catches its own deliberate assertion on success. Repair the helper so unexpected acceptance fails the test, and add a guard test for that helper.

EXPECTED OWNERS TO CHANGE: `DEV/TESTS/test_s6d_04_mechanical_context_contract.py`, `DEV/TESTS/test_s6d_05_portable_value_contract.py`, and `DEV/CATALOG/portable-value-routes.json` only. No GAME runtime/schema, workflow, toolchain, package manifest or lock file is directly edited.
EXPECTED CONSUMERS TO CHANGE: the canonical unittest test collector, local pytest suite, maintenance/package-closure validator, and build-time engine-contract inventory derivation that consumes `portable-value-routes.json`. The release builder recomputes that inventory in generated package metadata; no derived hash is hand-edited.
PROTECTED INVARIANTS: preserve exact active S6D-09 `fiction.target_reachable` consumers, dormant `fiction.target_visible`, false-vs-missing distinction, exact direct `$ref` consumer edges, the current continuation identity fields, and the existing ruleset/package identity algorithm. Do not weaken assertions or alter runtime code to satisfy stale test assumptions.
ALLOWED CHANGE: test evidence/collection and the existing consumer-edge inventory values needed to match actual current schema `$ref`s. The release builder/closure validator recomputes the path-neutral engine-contract inventory digest from this input; no hand-edited derived hash or package-identity alias is authorized.
VERSION_IMPACT: NONE expected — `portable-value-routes.json` retains `schema_version: 1` and identical shape; mechanical catalog generation, ruleset package revision/family/generation, engine release, runtime modules/schemas, campaign/storage generations, migration and dual-read remain unchanged. The derived engine-contract inventory content hash is recomputed under its existing generation and is not a version namespace.
SYSTEM_IMPACT: NONE expected. If the direct consumer edges require a new capability, schema, runtime owner or executable vocabulary, stop before broadening scope.

A26-02 TEST NODES:
- `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`
- `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`
- `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`
- `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`

A26-02 IMPLEMENTATION / FOCUSED VERIFICATION:
- Scoped repair is implemented in the three expected owners above; the current pytest modules pass **31 tests** and the same two modules pass **31 tests** through standard `unittest` `load_tests` collection.
- Independent `hdm-reviewer` review: **PASS / no findings** after cursor reconciliation; reviewer also confirmed all 19 portable-value route rows match current direct schema `$ref` edges.
- Direct build-time inventory reconstruction: PASS — inventory schema `2`, five families, ruleset-set identity `0700d3ccf367ade9ff56f620c4330bd5b4544fb9e22031f9d1eac3718a88ef2d`, inventory digest `c17a0cddc21720ac7bd97ce413ed519b122d9c5f55ac8718bb1a151fab298678`.
- Scoped Ruff check and `git diff --check`: PASS. `ruff format --check` reports pre-existing whole-file formatting drift in both modules; no broad reformat was applied.
- `VERSION_IMPACT: NONE` — the route manifest keeps `schema_version: 1` and the same shape; the corrected rows name existing direct schema `$ref` edges, changing only the derived portable-value semantic hash and enclosing engine-contract inventory hash under their existing schema/digest generations. No incompatible coordinated vocabulary, package identity algorithm, runtime/module/schema namespace, or persistence contract changes.
- `SYSTEM_IMPACT: NONE` — no new capability, runtime owner, schema or executable vocabulary is introduced.

A26-02 MAIN-WORKTREE DIAGNOSTIC:
- Full DEV pytest command: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto` — **1423 passed, 5 skipped, 7 failed**. All four historical A26-02/S6D failures now pass; the remaining failures are workspace-sensitive: `test_game_dev_layout::test_runtime_marker_is_unique`, `test_s6d_11_ruleset_package_closure::test_transitional_identity_keys_are_absent_from_current_carriers`, `test_runtime_package_provenance::{test_built_zip_contains_one_generated_root_provenance_member,test_clean_checkout_metadata_records_exact_head}`, `test_release_game_passthrough::test_new_game_root_file_and_directory_are_automatically_archived`, `test_release_integration::test_canonical_entry_point_builds_reproducible_flat_runtime_and_generator_smoke`, and `test_versioning_namespace_policy::test_census_has_zero_unclassified_hits`.
- Maintenance audit reports duplicate `GAME/ENGINE_VERSION.yaml` markers under existing `DEV/tmp/` verification worktrees and one transitional-identity token in preserved `.entire/tmp/` data; no preserved artifact was cleaned.
- Full unittest discovery in this checkout exceeded its 120-second limit while reaching the version-census test. Focused unittest collection is green; rerun the full canonical collector in a clean exact-head verification checkout.
- The above dirty-worktree diagnostic is superseded by the clean exact-head verification below; preserved user artifacts remain untouched.

A26-02 CLEAN EXACT-HEAD VERIFICATION — `7b652995398c08a327542ce8b9db25f254cf74f1`:
- Clean detached verification checkout at the exact published commit, outside the source tree.
- Canonical unittest discovery: **1435 tests passed, 5 skipped**; version census reported `VERSION_UNCLASSIFIED=[]` and `VERSION_LEGACY_HITS=[]`.
- Full DEV pytest: **1430 passed, 5 skipped**, 24 existing `jsonschema.RefResolver` deprecation warnings; exact command `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto` executed in the clean checkout.
- Canonical maintenance audit: **PASS** (`OK: engine consistency audit passed`).
- Canonical release builder: **PASS**; it reconstructed engine-contract inventory schema `2` with five families, ran registered package validators, and generated `/tmp/opencode/a26-02-build-7b652995/hedgelion-dnd-master-runtime-v1.0-alpha.zip` plus its SHA-256 sidecar.
- `VERSION_IMPACT: NONE`; `SYSTEM_IMPACT: NONE`. No hosted-CI result is claimed in this local-machine runtime.
- Independent task review: **PASS / no findings**. Code checkpoint commit `7b652995398c08a327542ce8b9db25f254cf74f1` was pushed non-force; fresh `git fetch --prune origin` confirmed local and `origin/v1/engine-rearchitecture` both at that SHA.
- A26-02 disposition: **IMPLEMENTATION / REVIEW / LOCAL VERIFICATION PASS**. Wave 04 remains open solely for the mandatory final Senior integration audit and closure decision.
- `A26-02_STATUS_SYNCHRONIZATION_VERSION_IMPACT: NONE` — execution cursor and `DEV/CURRENT_PROGRESS.md` record task state/evidence only; no version, revision, schema or generation namespace changes.

## W04.T07D System-Impact stop and accepted resolution

T07D_STATUS: `SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED` — stopped before RED; no T07D code/schema/test changes.
IMPACT_BRIEF: `DEV/docs/superpowers/design/2026-09-28-w04-t07d-commentator-control-system-impact-brief.md`.
TRIGGER: current Commentator `player_id -> story_ids` control is caller-shaped and only intersects Story-carried `visible_to`; neither is bound to an independently current W03 information/access basis. The accepted PO-009/T07D contract requires a comprehensive, source-bound Commentator eligibility/control projection and distinct content/control bases. The existing W03 read surfaces validate principal/PLAYER and individual knowledge/disclosure records but do not issue the required Story/T0-to-recipient control basis. A safe implementation may therefore require a newly chosen mapping contract or a broader producer/interface boundary, neither admitted by the current task envelope.
LAST_SAFE_SHA: `b6b7e8925727394482a62ace335beb0a05ed733d`.
DISPOSITION: preserve T07A/T07B/T07C and the recorded CLS↔HDM preflight result/trigger conditions. Do not implement guessed access semantics or modify W03 owners. W04.T08B is independent and continues under its own envelope.
INDEPENDENT_REVIEW: hdm-reviewer confirmed no complete T07D-only path was established by current owners and validated this as a genuine System-Impact trigger. This historical stop was resolved by PO-012, the Senior ruling and accepted T07D-P0; the independent P0 PASS/read-back gate is complete.

CURRENT_DISPOSITION: `SYSTEM_IMPACT: RESOLVED`; PO-012 supplies the baseline reader rule and T07D-P0 supplies exact-current owner evidence. T07D may resume inside the existing Commentator consumer boundary. No T07A/B/C, CLS↔HDM, W03 producer, Context Runtime, Story/T0, persistent-schema or shared-writer scope is reopened.

## W04.T08B implementation impact envelope

SPEC / APPROVED DESIGN: T08B row in the stable Wave-04 plan; accepted T06B `W04_PROTECTED_EMISSION_READY`; current W03 principal-to-PLAYER, LIVE-currentness and access-policy transition owners. W03 execution status is `COMPLETE` / Senior PASS; the Product Owner confirms its T08B currentness input is satisfied, with no new W03 task.
IMPLEMENTATION START CODE BASE: `b6b7e8925727394482a62ace335beb0a05ed733d` (freshly fetched published tree; subsequent cursor update is documentation-only).
PRIMARY OWNER ARTIFACTS: session-focused DEV test `DEV/TESTS/test_w04_t08_session_consumer_delta.py` and bounded Wave-05 SESSION delta fixture `DEV/TESTS/fixtures/w04_session_consumer_delta.json`, following the accepted T03A owner-local delta pattern.

EXPECTED OWNERS TO CHANGE: test/evidence-only consumer delta for the future Wave-05 SESSION final writer; no GAME runtime producer, schema, or CORE writer changes.
EXPECTED CONSUMERS TO CHANGE: the new T08B session-handoff contract tests and Wave-05 SESSION delta consumer.
ALLOWED INTERFACES / CONTRACTS TO CHANGE: only the bounded SESSION consumer delta and focused tests. No physical `GAME/CORE/SESSION.md`, `GAME/SCHEMA/session.schema.yaml`, runtime/session producer or shared schema change.

PROTECTED ARCHITECTURE INVARIANTS: session metadata never becomes campaign/LIVE/PLAYER authority; stale/relinquished host revalidates native sources; controlled handoff names the exact durable/current source basis; no heartbeat/lease/no-op publication.
ARCHITECTURE-SENSITIVE SURFACES: exact campaign/LIVE/PLAYER identity and currentness stated in the downstream SESSION consumer delta.
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: focused T08B session tests, delta-fixture contract, T06B and accepted W03 currentness-consumer regressions, full DEV, maintenance and version/provenance checks.
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: `GAME/CORE/SESSION.md`, `GAME/SCHEMA/session.schema.yaml`, session runtime production code, shared PLAYER/LIVE schemas, W03 producers, GAME/CORE final-writer bytes, heartbeat/lease infrastructure and publication behavior.
VERSION IMPACT: NONE expected for test/delta-only changes; perform the normal owner/consumer classification before checkpoint.
SYSTEM IMPACT: NONE expected; if a correct handoff delta appears to require a session authority/schema/runtime producer change, stop before expanding the write set.

## W04.T08B implementation verification state

T08B_TDD_RED_GREEN: five new focused contract tests failed before the bounded SESSION delta fixture existed; after adding the fixture and correcting the task-local assertion to the exact no-op-only publication vocabulary, the focused suite is green. Review fix round 1 added an assertion that the universal cross-domain currentness scalar stays false; toggling the fixture true produced the expected RED, restoring false produced GREEN.
T08B_FOCUSED_VERIFICATION: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_w04_t08_session_consumer_delta.py DEV/TESTS/test_house_rules_policy_authority_contract.py DEV/TESTS/test_maintenance_continuation_contract.py` — 14 passed. Scoped Ruff check and format pass for the new session test; `json.tool` parses the delta fixture.
T08B_REVIEW: initial independent review finding that the delta test omitted the `universal_cross_domain_currentness_scalar: false` guard was repaired test-first; the RED was observed with the fixture temporarily set true, then restored false. Scoped re-review marked the finding ADDRESSED with no new concerns.
T08B_INDEPENDENT_REVIEW: **PASS** — the bounded delta and test now enforce all T08B mandatory REDs, including no universal cross-domain currentness scalar. Reviewer found no remaining task-local findings; no runtime/session schema or authority changed.
T08B_VERSION_IMPACT: NONE — only DEV tests and an owner-local bounded Wave-05 SESSION delta fixture changed; `GAME/CORE/SESSION.md`, the persistent SESSION schema and runtime producers remain unchanged.
T08B_SYSTEM_IMPACT: NONE — no new authority, session lease/heartbeat or no-op publication behavior.
T08B_CODE_COMMIT: `356357a5c05e16d704bebfe11e8a3df542321694` (`test(w04): add session consumer delta`), published in the accepted active-ref chain.
T08B_CLEAN_EXACT_FULL_DEV: exact committed-source run at `356357a5c05e16d704bebfe11e8a3df542321694`: 1339 passed, 5 skipped, 4 known out-of-scope S6D failures; package provenance reports `clean_head`. All four named S6D failures reproduced sequentially on this exact commit. Full command: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto`.
T08B_VERSION_AND_MAINTENANCE: combined version namespace/package-provenance/current-progress suite 18 passed; clean candidate census has no unrelated `.agents`, `.lavish`, `.entire`, nested-checkout or bytecode contamination; canonical maintenance audit PASS. `VERSION_IMPACT: NONE`.
T08B_INDEPENDENT_REVIEW: **PASS** — reviewer approved the scoped delta/test; the missing negative for `universal_cross_domain_currentness_scalar` was added test-first and scoped re-review marked it ADDRESSED with no new concerns.
T08B_PUBLICATION_READBACK: non-force push succeeded. Fresh `git fetch --prune origin` confirmed local HEAD and `origin/v1/engine-rearchitecture` equal `468bd3400183ada85b76cd93737005aa1e1e64a7`.

## W04.T06A mechanical fixture synchronization — RD05 handoff consumer

IMPACT ENVELOPE CORRECTION: include the single W02 handoff consumer test fixture `DEV/TESTS/test_rd05_runtime_execution.py::DeterministicExecutionTests.test_committed_execution_crosses_only_a_registered_narrator_handoff` alongside RD10 as a mechanical consumer synchronization. The test now obtains its Narrator binding through `turn_runtime.bind_phase_from_context` with a test ContextService capability and verifies one assembly call. Its accepted-execution/W02 handoff assertions remain unchanged.

CLASSIFICATION: test-fixture synchronization only. No new product owner, owner/interface, runtime producer, or persistence boundary; `runtime_execution.py`, `mechanics.py`, and W02 producer behavior are unchanged.

SYSTEM_IMPACT: NONE. The one-file consumer fixture now uses the T06A accepted-basis contract already in the Impact Envelope; no implementation owner or interface changed.


## T04B Senior System-Impact resolution

RULING: DEV/docs/superpowers/design/2026-09-25-w04-t04b-irr-t04b-02-senior-ruling.md
RULING_BASE: 186da5a81a9bc760ebf7cc87ccbf629cf0f630aa
RULING_PUBLICATION: 2128702e1c1a257f825b4b5b2f70dd3dc3c33dd2
PLAN_SYNC: bf7fdfcae43e43588d16579b50f92c2d6027d762

IRR-T04B-02 disposition: **RESOLVED TO BOUNDED PREREQUISITE / NO PRODUCT-SEMANTIC CHANGE**.

The accepted Step-5.8 law already requires exact final LIVE close -> absorption/final routing -> PLAYER/access + Collaboration transition -> one same-campaign W02 transaction. The missing W03 producer boundary is therefore an implementation-boundary prerequisite, not a new product/authority decision.

W04.T04B-P1 is authorized with W03 LIVE semantic ownership. Its production write surface is limited to `GAME/TOOLS/live_state.py`; it must issue a complete owner-authenticated `FrozenCampaignAbsorptionDelta` plus group-aware accepted-publication evidence, using only existing admitted campaign owner paths. If any required packed/handoff contribution cannot be represented losslessly without a new persistent owner/schema or broader runtime/repository API, P1 stops at a new System-Impact event.

T04B may resume immediately after P1 implementation + independent PASS/read-back. No PO or second Senior gate is required unless P1 discovers a new trigger. T04A/T07B/T07C remain closed; T07D is unaffected.

## T04B-P1 W02 ancestry-evidence Senior resolution

RULING: `DEV/docs/superpowers/design/2026-09-25-w04-t04b-p1-w02-publication-evidence-senior-ruling.md`

Disposition: **RESOLVED TO BOUNDED W02 PREREQUISITE / NO PRODUCT-SEMANTIC CHANGE**.

New prerequisite:

```text
W04.T04B-P0 — W02 verified campaign-publication acceptance evidence
OUTPUT: W02_VERIFIED_CAMPAIGN_PUBLICATION_EVIDENCE_READY
```

P0 preserves `PublicationOutcome` as the ordinary constructible result value but adds exact-instance W02 owner-issued acceptance evidence bound to the exact `FrozenCampaignPublicationAttempt`. Direct acceptance binds the actual trusted ref result; reconciled current closure retains the trusted closure proof; reconciled ancestor closure retains both trusted closure and ancestry evidence. Raw/directly constructed/copied/equal-field outcomes are not owner evidence.

Allowed P0 production writes: `GAME/TOOLS/publication.py`, `GAME/TOOLS/runtime_host.py`. Primary tests: `DEV/TESTS/test_rd06_durability_publication.py`, `DEV/TESTS/test_runtime_host_composition.py`.

After P0 independent PASS/read-back, P1 resumes and must consume the W02 owner validator using its campaign/predecessor and W03 operation-digest subset. W03 does not re-run Git ancestry.

Expected fresh Version Impact if baseline remains current: publication `1.0.4 -> 1.0.5`, runtime_host `1.0.8 -> 1.0.9`. No persistent schema/generation/migration change expected.

No PO gate. T07D remains independent.

## T04B post-publication recovery evidence Senior resolution

RULING: DEV/docs/superpowers/design/2026-09-25-w04-t04b-postpublication-recovery-evidence-senior-ruling.md

Disposition: **RESOLVED TO BOUNDED W02 READ-ONLY PREREQUISITE / NO PRODUCT-SEMANTIC CHANGE**.

New prerequisite:

    W04.T04B-P0R — W02 read-only post-publication acceptance revalidation
    OUTPUT: W02_POSTPUBLICATION_REVALIDATION_READY

P0R re-proves an already-published H -> C closure from repository authority after process loss, then issues a fresh exact-instance P0-style PublicationOutcome/acceptance evidence pair. It performs no create_tree/create_commit/update_ref and persists no receipt.

The nominated predecessor H and intended commit C are not trusted inputs. W02 must prove exact predecessor tree, direct single-parent C, exact changed-path/write closure, current D closure and C->D ancestry where applicable. Existing Step-5.6 RepositoryPort exact commit/tree/path and bounded changed-path/ancestry capability is sufficient; no new RepositoryPort method or authority is authorized.

Same-process-only recovery is rejected because it violates the accepted Step-5.6 cold-recovery law. Durable evidence persistence is not authorized because repository authority can re-prove the closure without adding a journal/schema.

After P0R independent PASS/read-back, the existing T04B candidate may resume. It rederives P1 delta + full joined W02 operations, calls P0R, passes the fresh W02-issued outcome through unchanged P1 composed-absorption classification, and validates final after-images without a second W02 write or LIVE replay.

Expected fresh P0R Version Impact if baselines remain current: publication 1.0.5 -> 1.0.6; runtime_host 1.0.9 -> 1.0.10. No persistent schema/generation/migration change.

No PO gate. T07D remains independent.

## Current independent review

REPORT: DEV/docs/superpowers/design/2026-09-25-w04-t07c-independent-rereview.md
REVIEWED_HEAD: df83bc7c37e1f1d0fdeebd583350bf377a4c8f37

| Task | Candidate / repair | Independent disposition |
|---|---|---|
| W04.T04A | accepted prior chain | Prior PASS preserved |
| W04.T04B | 6bb8723ff5ef8f3508d53303ba614d42222393d3 | NOT ACCEPTED; IRR-T04B-01 CLOSED; IRR-T04B-02 Senior gate resolved to T04B-P1 W03 prerequisite |
| W04.T07B | 55fb0a52a933b90a15ad2bc8b0af624635edaf26 | Prior PASS preserved |
| W04.T07C | f114eb6a38c50d755cf71094d078c1d362f08bb4 | PASS / GO; IRR-T07C-01/02 CLOSED |

T07C retains complete T0 factor values plus PUBLIC/PROTECTED historical classification from exact native SemanticEvent evidence, without consulting later Actor/knowledge/disclosure state. Exact older pages at/below compatible coverage are idempotently acknowledged only after exact native revalidation.

Hosted evidence: repair run 36076362491/job 107888337524 SUCCESS and current run 36078547787/job 107895116534 SUCCESS; maintenance PASS, 1218 tests / 5 skipped, zero version unclassified/legacy hits.

## T04B-P1 ancestry-evidence finding — resolved by P0; P1 accepted

IMPACT_BRIEF: `DEV/docs/superpowers/design/2026-09-25-w04-t04b-p1-w02-ancestry-evidence-impact-brief.md`

This records the pre-P0 review trigger. The earlier unpublished P1 candidate accepted a constructible W02 `PublicationOutcome` claiming `RECONCILED_ANCESTOR_CURRENT_CLOSURE` without owner-issued closure/ancestry provenance. P0 resolved the evidence boundary: W02 owns exact-outcome-instance acceptance evidence; P1 consumes that validator and does not validate Git ancestry independently.

P0 output `W02_VERIFIED_CAMPAIGN_PUBLICATION_EVIDENCE_READY` passed independent review and remote read-back at `d1a10f8bf6ec16d34ecb3ffa58b0a48c6527a31a`. P1 resumed only after that gate and remains within its existing W03 write scope.

P1 OUTPUT: `W03_COMPOSABLE_CAMPAIGN_ABSORPTION_DELTA_READY`

P1_CODE_COMMIT: `a792d14894dcc3ba123191883e5647cc06808e85`

P1_INDEPENDENT_REVIEW: **PASS** — W03 validates exact P0 owner-issued acceptance evidence with its W03 operation subset; caller-constructed direct and ancestor outcomes are rejected; genuine RuntimeHost direct/current/ancestor evidence is accepted; no second ref transition is added.

P1_REMOTE_READBACK: fresh fetch confirmed `origin/v1/engine-rearchitecture == a792d14894dcc3ba123191883e5647cc06808e85`.

P1_VERIFICATION: P1 class 23 passed; RD09 194 passed; clean exact P1 full DEV suite 1268 passed, 5 skipped, 4 sequentially reproduced S6D catalog/contract failures outside P1 scope; clean exact maintenance audit PASS; scoped Ruff/format PASS. Hosted CI unavailable.

VERSION_IMPACT — P1: `GAME/TOOLS/live_state.py 1.0.20 -> 1.0.21`; LIVE routing v4, native-state-pack v2, absorption-attempt v1, campaign-contract generation and storage generation unchanged. No migration or dual-read.

## W04.T04B-P0 accepted checkpoint — 2026-09-25

OUTPUT: `W02_VERIFIED_CAMPAIGN_PUBLICATION_EVIDENCE_READY`

CODE_COMMIT: `d1a10f8bf6ec16d34ecb3ffa58b0a48c6527a31a`

INDEPENDENT_REVIEW: **PASS** — exact outcome-instance binding, proof/attempt/currentness validation, operation-subset checking, RuntimeHost direct/current/ancestor issuance, non-acceptance behavior, and no second ref update.

REMOTE_READBACK: fresh fetch confirmed `origin/v1/engine-rearchitecture == d1a10f8bf6ec16d34ecb3ffa58b0a48c6527a31a`.

VERSION_IMPACT: `GAME/TOOLS/publication.py 1.0.4 -> 1.0.5`; `GAME/TOOLS/runtime_host.py 1.0.8 -> 1.0.9`. No persistent schema, campaign-contract/storage/catalog generation, engine release, migration, or dual-read change.

VERIFICATION:
- W02 publication + RuntimeHost unit suites: 68 passed;
- affected Collaboration, Story/T0, and publication-ref-fence suites: 211 passed;
- maintenance audit from the clean exact P0 worktree: PASS;
- P0-range Ruff format and scoped Ruff checks: PASS;
- full canonical DEV suite from clean exact P0 commit: 1245 passed, 5 skipped, 4 failed. The four reproducible failures are outside P0 scope: `test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`, `test_real_activity_action_request_binding_matrix_and_freeze`, `test_roll_retry_is_single_fixed_result_and-offers-reject-stale-owner`, and `test_route_rows_ids_and_embedding_edges_are_machine_verified` (S6D catalog/contract owners). Hosted CI is unavailable.

The full-suite failures are recorded, not repaired under P0’s write scope. The P0 code commit contains only its two authorized W02 production files and two primary test files.

Exact failing node IDs (correcting the hyphenated shorthand above): `test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`; `test_real_activity_action_request_binding_matrix_and_freeze`; `test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`; `test_route_rows_ids_and_embedding_edges_are_machine_verified`.

## T04B post-publication recovery System-Impact stop — 2026-09-25

IMPACT_BRIEF: `DEV/docs/superpowers/design/2026-09-25-w04-t04b-postpublication-recovery-evidence-impact-brief.md`

The uncommitted T04B candidate validates same-process recovery when the exact W03 composed-absorption object is retained. That result and the W02 exact-outcome proof are ephemeral. After process loss, a newly reconstructed reconciliation has no composed result, and current W02 exposes no read-only owner path to reissue exact closure/ancestry evidence without another publication. The accepted crash-after-publication/recovery case is therefore not complete.

Disposition: stop T04B production changes pending Senior resolution of whether/how W02 may reissue owner-authenticated evidence for an existing commit through bounded current-ref/closure/ancestry reads. Do not persist a receipt or broaden W02/RuntimeHost within the current T04B write scope without that ruling. T05C remains blocked; T07D remains independent.

Evidence: RD12 focused suite: 142 passed; worker combined relevant suites: 404 passed; independent review: TARGETED_REPAIR_REQUIRED for post-process-loss recovery evidence; maintenance audit was blocked by the ignored `GAME/TOOLS/__pycache__` release-boundary finding. P0/P1 remain independently accepted/published; no T04B checkpoint exists.

VERSION_IMPACT: T04B candidate Collaboration module `1.0.18 -> 1.0.19` if baseline remains current; schema v3 and other namespaces unchanged. This candidate impact is provisional while the gate is open.

Fresh CLS reconciliation: audit head 3bd4ffb1db0451d0079568d4ad58709372ef3a4d, feature head 2c5dc9f6a4f1c8a23b070e7520e7854491af5282. Current WP12-05 remains synthetic/normalized and REAL wire normalization remains WP12-08-owned. No public semantic reopen/write or current private WP12-05 repair is required; future REAL integration must consume T0 schema 2 / EVENTS schema 4 / E-EVT generation 2.

## Accepted producer checkpoints retained

| Task | Accepted checkpoint / evidence route |
|---|---|
| W04.T00H | Accepted host-composition chain retained in the historical ledger identified below |
| W04.T01A | b50f490cf8dc1d5448cf3ee3c84ce4112e5f8772 |
| W04.T05A | 995924b2a5448dbf9ae4a52555f64de69f7fd699 |
| W04.T01B | 856abcbd6621da33b9ca5ff59413ae7aeb8b3d20 |
| W04.T05B | a1a4d204fbeec9f8a24e681289e0e530e5b91b75 |
| W04.T01C | 7b66ac881aa8a60dd6d03bd97d1ab74e1a96da62 |
| W04.T02A | 5c77aced9dafd9a7f26177090b3e62466b8ec561 |
| W04.T03A | ca3efa3c7750cffc2eef228b4b8666b75828cea9 |
| W04.T00P | 606cf87caeee427622680f8898a6ba1998fb1a9e — accepted coherent host/History bridge; earlier 595ff95f10d3d48de5748ae32a60d4839106ea2b chain retained |
| W04.T02B | 711738ce20d449a330313f5e51292408d311a616 |
| W04.T07A | 534653babd788d85663dfc2006fbc921ad1577bd |
| W04.T02C | dd0783c4eca20a94431b17844ca09ac64f8ba2cf |
| W04.T04A | 0d190a9db11129a02f07c71a812996c78a8d33cf — independently accepted at combined reviewed HEAD 3c1a9ca1e31e46f8101944ee668a52bd3d3678ff |
| W04.T07B | 55fb0a52a933b90a15ad2bc8b0af624635edaf26 — independently accepted at combined reviewed HEAD a5cd9c517913bcf04d7acfbe895be49cdf941111; prior source-contract repair chain retained |
| W04.T07C | f114eb6a38c50d755cf71094d078c1d362f08bb4 — independently accepted at reviewed HEAD df83bc7c37e1f1d0fdeebd583350bf377a4c8f37 |

W04_AUTHORITY_COLLAB_RECONCILIATION_READY: ACCEPTED
W04_AUTHORITY_COLLABORATION_RECONCILED: NOT ACCEPTED
W04_STORY_SOURCE_CONTRACTS_READY: ACCEPTED
W04_T0_STORY_READY: ACCEPTED

No earlier accepted task is reopened. T07C is independently accepted. T04B-P1 is a new bounded W03-owned prerequisite for the still-unaccepted T04B candidate, not a Wave-03 reopen.


## Scheduling and gates

```text
READY IN PARALLEL:
  T07D
  T04B-P0R  (W02 read-only recovery owner)
  T04B-P0  (W02 publication semantic owner)

T04B-P0 implementation -> independent PASS/read-back
  -> T04B-P1 resumes immediately
T04B-P1 implementation -> independent PASS/read-back
  -> T04B resumes immediately
  -> T04B repair/recovery verification -> independent PASS

T05B + T02C + T04B PASS -> T05C -> T06A -> T06B

T07C PASS -> T07D -> independent PASS -> T07E
T07A..T07E -> T07-INTEGRATION independent review

T04B PASS + T02C + T07-INTEGRATION -> T08A
T06B + accepted W03 currentness -> T08B
T08A + T08B + T03A -> T08C
T08C + all lane checkpoints -> Wave-04 FINAL_REVIEW
mandatory Senior Wave-04 integration audit -> closure decision
```

T07D and T04B-P0 may begin independently. T04B-P1 remains stopped until exact P0 independent PASS/read-back; T04B remains stopped until P1 PASS/read-back; T05C remains blocked until T04B PASS.

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE; reviewers do not consume worker slots
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after exact producer independent PASS is published/read back

## Preserved T04A clarification and T04B obligations

Historical hydration and current admission are distinct. Exact durable accepted associations, authorship, PC association and frozen fingerprints survive author deactivation. An inactive historical author is not by itself a reason to reject historical hydration or cancel an otherwise valid satisfied requirement.

A positively established invalid outstanding required agency or decision opportunity may obsolete the affected generation. Do not remove requirements, synthesize consent/PASS, create an automatic successor, or reinterpret accepted mechanics. Unknown authority/opportunity is a bounded failure, not proof of obsolescence. In the accepted T04A implementation, unavailable singleplayer creator/agency validity raises without producing an OBSOLETE candidate, including for CLOSED state.

The unchanged W03 full-body guard consumes an independently read pinned MANIFEST. Keep that exact-body check; do not substitute the frozen predecessor, a projected access subset or a caller currentness flag.

T04A remains read-only preparation. T04B owns the physical same-campaign-closure authority/obligation/PLAYER-route publication and its complete recovery. Agreement between a carrier's affected IDs and its candidate tuple does not prove effect-set completeness. Repeated/advanced-head recovery must not skip omitted effects.

T04B must preserve Step-5.8 revocation law. The current repair proves source close but omits positive W03 absorption/final-routing from its W02 write-set and accepts CLOSED_UNABSORBED during recovery. The Senior ruling resolves the producer gap by requiring T04B-P1 to add the W03-owned composable delta/evidence boundary first. T04B then only consumes that owner-issued delta in the same W02 closure; Collaboration still may not create LIVE authority. CLOSED_UNABSORBED remains pending absorption, not a successful recovery state.

## Preserved Story and cross-project limits

All four Story layers and eight source registrations remain mandatory. No baseline SPARSE coverage, false omission of required material, source substitution, reconstruction of native history from Story, or current T1 substitute for retained T0 is authorized.

Accepted M-SEG validation keeps explicit payload owner links, strict positive non-boolean ordinals and exact candidate/segment binding. Structural schema admission need not itself prove cross-field candidate equality; a well-shaped wrong segment remains rejected by Python.

T07B's unconditional rejection of source-classified OMITTED results is not positive proof of native-proven omission support. Preserve that qualification in subsequent source/materialization evidence. A caller MAY_OMIT/reason flag cannot authorize omission. T07B PASS is not whole-Story or whole-Wave integration acceptance.

T07C must preserve retained T0 values together with the historical availability/protection classification needed for later self-contained filtering. Coverage is the idempotency owner: after exact native revalidation, a compatible page wholly at or below persisted coverage is already covered, not a source rewind.

The mandatory pre-T07 CLS-HDM preflight retains its recorded PASS and explicit semantic-change/unavailable-evidence trigger conditions. This review does not repeat it or waive a future genuine trigger. Its exact original refs/blobs remain in CURRENT_PROGRESS and the historical ledger.


## Wave-04 independent-review verification and Version Impact

```text
REVIEWED_HEAD: df83bc7c37e1f1d0fdeebd583350bf377a4c8f37
T07C_REPAIR: f114eb6a38c50d755cf71094d078c1d362f08bb4
HOSTED_REPAIR_RUN: 36076362491
HOSTED_REPAIR_JOB: 107888337524
HOSTED_CURRENT_RUN: 36078547787
HOSTED_CURRENT_JOB: 107895116534
```

CURRENT_VERIFICATION_STATE:
- repair commit exact-head maintenance PASS and 1218 tests/5 skipped PASS;
- current reviewed-head maintenance PASS and 1218 tests/5 skipped PASS;
- VERSION_UNCLASSIFIED=[] and VERSION_LEGACY_HITS=[] on both hosted verification points;
- IRR-T07C-01/02 independently CLOSED;
- IRR-T04B-02 main producer gap remains assigned to T04B-P1; the nested ancestry-authenticity gate was resolved by T04B-P0. P0 and P1 outputs are independently accepted/read back.

VERSION_IMPACT — T07C ACCEPTED:
- History module 1.0.5;
- embedded T0 basis schema 2;
- Story module 1.0.8;
- Story EVENTS unit schema 4;
- E-EVT semantic contract generation 2;
- runtime.semantic_event outer schema 1 unchanged;
- Story projection-state schema 4 unchanged;
- durability 1.0.4 unchanged;
- campaign_contract_generation 2 unchanged;
- migration/dual-read NONE under the current pre-release clean-slate policy.

CLS_HDM_RECONCILIATION:
- audit current head 3bd4ffb1db0451d0079568d4ad58709372ef3a4d;
- private feature current head 2c5dc9f6a4f1c8a23b070e7520e7854491af5282;
- current WP12-05 synthetic/normalized implementation does not hard-bind REAL public wire versions;
- WP12-08 remains owner of REAL source/content/control normalization;
- PUBLIC_HDM_SEMANTIC_REOPEN_REQUIRED=NO;
- PUBLIC_HDM_WRITE_REQUIRED_BY_CLS=NO;
- CURRENT_PRIVATE_WP12_05_REPAIR_REQUIRED=NO;
- FUTURE_REAL_NORMALIZATION_OBLIGATION=YES.

SYSTEM_IMPACT:
- T07C NONE / accepted;
- IRR-T04B-02 RESOLVED TO BOUNDED PREREQUISITES;
- T04B-P0: PASS / independently reviewed / published / read back;
- T04B-P1: PASS / independently reviewed / published / read back under existing W03 scope using the P0 validator.
- T04B-P0R: ACCEPTED W02 read-only recovery prerequisite; independent PASS and exact remote read-back complete.
- T04B: `W04_AUTHORITY_COLLAB_RECONCILIATION_READY` independently PASS, clean exact full DEV evidence recorded, and remote read-back complete; no new System-Impact trigger.

P0R_IMPLEMENTATION_STATE: PASS — implementation, focused and clean exact-tree verification, independent review, publication and remote read-back complete.
P0R_OUTPUT: `W02_POSTPUBLICATION_REVALIDATION_READY` — ACCEPTED / independent PASS / remote read-back.
P0R_CODE_COMMIT: `d053dbbc01351c0ef5a356110542b0a86d3f923c`.
P0R_REMOTE_READBACK: fresh fetch confirmed `origin/v1/engine-rearchitecture == 94bfddf475cd5ffa21049e6333188aa32126635b`; P0R code and cursor files match local HEAD.
P0R_INDEPENDENT_REVIEW: **PASS** — repository-identity mismatch negative witness was added and scoped re-review marked it ADDRESSED.
P0R_FOCUSED_VERIFICATION: RD06 + RuntimeHost + LiveComposedCampaignAbsorptionDelta + publication-ref-fence suites: 112 passed; maintenance audit: PASS.
P0R_CLEAN_EXACT_FULL_DEV: 1281 passed, 5 skipped, 4 known S6D failures outside P0R scope; clean exact maintenance audit PASS; version census zero unclassified hits; clean package provenance PASS. Ran from detached clean worktree at code commit `d053dbbc01351c0ef5a356110542b0a86d3f923c`.
P0R_RUFF: all changed-range format checks PASS. Whole-file Ruff reports only three findings confirmed present at implementation BASE_SHA: RD06 unused `promise`, `publication.py` NaN self-compare and nested immutable-campaign identity condition. Whole-file formatting remains non-clean in pre-existing sections of `publication.py` and RD06 tests; P0R changed ranges are formatted.
P0R_DIRTY_WORKTREE_FULL_DEV: diagnostic run before the final reviewer-only test addition: 1277 passed, 5 skipped, 6 failed. Four failures are known S6D cases; the other two were traced to local `.entire/`/`DEV/.lavish/` version-census contamination and expected dirty-worktree package provenance, and disappeared in the clean exact-tree run.
P0R_VERSION_IMPACT: `publication.py 1.0.5 -> 1.0.6`; `runtime_host.py 1.0.9 -> 1.0.10`; schema, campaign-contract, storage/catalog/engine generations, migration, and dual-read: NONE.

T04B_TDD_RED: cold recovery with `composed_absorption=None` failed at the missing owner-issued P1 evidence guard before P0R consumption; after the bounded P0R rederivation path, the current-closure case is GREEN.
T04B_FOCUSED_VERIFICATION: RD12 collaboration suite 144 passed; combined RD12 + RD06 + RuntimeHost + W03 composed-absorption + ref-fence suites 256 passed.
T04B_MAINTENANCE: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py` — PASS.
T04B_RUFF: `ruff check` and `ruff format --check` for `collaboration.py` and `test_rd12_collaboration.py` — PASS.
T04B_VERSION_IMPACT: Collaboration `1.0.18 -> 1.0.19`; schema v3 unchanged; P0R `publication.py 1.0.6` and `runtime_host.py 1.0.10` unchanged; campaign, storage/catalog/engine generations, migration and dual-read: NONE.
T04B_INDEPENDENT_REVIEW: **PASS** for spec compliance and code quality; no findings; reviewer verified no new System-Impact trigger.
T04B_CLEAN_FULL_DEV: 1297 passed, 5 skipped, 4 known S6D failures outside T04B scope; version census zero unclassified hits and clean package provenance PASS. Run from detached clean worktree at T04B candidate commit `a04cc825bb8cfdfb965d9ffec9fdb0cae1ea37ad`, excluding main-worktree `.entire/` and `DEV/.lavish/`.
T05C_TDD_RED: collaboration owner candidate is currently unregistered; the new required-collaboration-context witness fails `UNSATISFIABLE` before the Context resolver is added.
T05C_FOCUSED_VERIFICATION: RD11 Context suite: 42 passed; combined RD11 + RD12 + W03 composed-absorption suites: 209 passed, including recipient-safe projection, no purpose/dependency-scope projection, malformed-lifecycle fail-closed behavior, independent obsolete/route/generation negatives, retrospective current-permission revalidation, and profile/recipient/frontier mismatch checks.
T05C_RUFF: `ruff check` and `ruff format --check` for `context_runtime.py` and `test_rd11_context_runtime.py` — PASS.
T05C_MAINTENANCE: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python DEV/TOOLS/run_maintenance_audit.py` — PASS after clearing generated GAME bytecode cache.
T05C_DIRTY_FULL_DEV_DIAGNOSTIC: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto` in the active checkout — 1302 passed, 5 skipped, 6 failed. Four failures are the known out-of-scope S6D cases; `test_runtime_package_provenance::test_clean_checkout_metadata_records_exact_head` observes `dirty_worktree`; `test_versioning_namespace_policy::test_census_has_zero_unclassified_hits` observes 128858 hits from `.entire/` and `DEV/.lavish/`. This dirty-checkout diagnostic is not clean exact-tree evidence; both directories remain untouched.
T05C_VERSION_IMPACT: Context Runtime `1.0.7 -> 1.0.8`; persistent schema, campaign-contract, storage/catalog/engine generations, migration and dual-read: NONE.
T05C_CLEAN_FULL_DEV: full clean exact-tree suite at candidate `c373d1cd7d71455a62cbfa2e7d993e0b1a97c34a`: 1304 passed, 5 skipped, 4 known out-of-scope S6D failures; version census zero unclassified hits; runtime package provenance reports `clean_head`; maintenance audit PASS. The four known failures are `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`, `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`, `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`, and `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and-offers-reject-stale-owner`. Run from a clean detached-HEAD repository under ignored `DEV/tmp/`; `.entire/`, `DEV/.lavish/`, and unrelated `.agents/` edits were excluded without modifying them. Fresh remote read-back confirmed the T05C code and status commits at `95c898ce62fc947436cd386198c182ea98510925`.
T05C_CLEAN_FULL_DEV_FAILURE_ID_CORRECTION: The fourth exact failing node ID is `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner`; the preceding summary's hyphenated spelling is a typographical error.
T05C_INDEPENDENT_REVIEW: **PASS** — spec/code PASS; prior HIGH recipient-scope disclosure and MEDIUM malformed-lifecycle findings CLOSED; the independent status-focused re-review confirmed the reconciled verification counts and task-state bookkeeping.
T05C_REVIEW_BOOKKEEPING_RECONCILIATION: **PASS** — focused verification 42/209 and review state independently confirmed consistent across this cursor and `DEV/CURRENT_PROGRESS.md`.

NEXT_EXACT_TASK: complete the mandatory Senior Wave-04 integration audit/closure decision against verified implementation head `7b652995398c08a327542ce8b9db25f254cf74f1`, using the A26-02 review and clean exact-head evidence above plus the accepted T07-INTEGRATION/T08C records. Then synchronize final Wave-04 status. Wave 05 remains unauthorized.
KNOWN_BLOCKERS: no Senior System-Impact gate remains open for T07A-E, T08A-C or A26-02. A26-02 implementation/review/local verification PASS and publication/read-back PASS. Wave 04 is not complete pending the mandatory final Senior integration audit/closure decision; hosted CI is unavailable in this local-machine runtime. Wave 05 is not authorized.
UNPUBLISHED_WORK: NONE for A26-02; the repair is published and exact-head verified. No runtime/schema implementation remains unpublished. Preserve unrelated `.agents/skills/`, `.entire/`, and `DEV/.lavish/` workspace material without staging or modifying it.

## W04.T06A accepted Context-basis gate adjudication

IMPACT_BRIEF: `DEV/docs/superpowers/design/2026-09-26-w04-t06a-accepted-context-basis-system-impact-brief.md`

HISTORICAL_LAST_SAFE_SHA_AT_FIRST_RULING: `e428084382a84ce87ef1e8123a1c9b2d97e7cb2d` (the then-current PO-011-integrated basis; retained only as historical gate evidence)
HISTORICAL_REMOTE_HEAD_AT_FIRST_RULING: `e428084382a84ce87ef1e8123a1c9b2d97e7cb2d` — retained as the first-ruling evidence basis; current public routing is owned by the top cursor and the 2026-09-27 Senior ruling.
INITIAL_STOP_VERIFICATION_STATE: the supplied RD10 baseline observed the expected forged-basis RED: 1 failed, 24 passed. This was the pre-ruling diagnostic; the current post-sync verification is recorded below.

INITIAL_VERSION_IMPACT_AT_STOP: NONE for the partial T06A code/test delta at the time of the initial gate; TurnRuntime is unversioned implementation support and no version-bearing or persistent schema was changed.

RULING: The T06A scope may consume Context through the already-accepted injected RuntimeHost `ContextService.assemble(request, candidates)` capability. TurnRuntime must invoke it exactly once per phase and mint a sealed transient basis only from that invocation's result; binding rejects raw mappings even when `bundle_id` and scope fields match. This adds no ContextService/RuntimeHost producer/interface change and no new authority. Full rationale and cost if wrong are recorded in the Impact Brief above.
T06A_RULING_ENFORCEMENT_STATUS: SUPERSEDED BY 2026-09-27 SENIOR RULING — the independent review correctly identified that the candidate accepts a structural assembler port, but T00H explicitly places tracked deterministic Python/test-fixture injection inside the trusted computing base and forbids inventing an in-process token/registry/marker merely to authenticate arbitrary Python objects. The relevant enforcement boundary is that gameplay/model/request/envelope/candidate data cannot choose or replace the assembler capability.

SYSTEM_IMPACT: RESOLVED / NO ARCHITECTURE DELTA — resume inside the original T06A owner envelope under `2026-09-27-w04-t06a-contextservice-authenticity-senior-ruling.md`; no ContextService/RuntimeHost producer or interface change is authorized by this resolution.

## W04.T06A implementation candidate and verification

IMPLEMENTATION_STATE: CODE/TEST REVIEW PASS; CLEAN EXACT VERIFICATION PASS at `5550d30cb2e53f4e309725cf4a69f510c57f7af6` — the candidate remains NOT_ACCEPTED until publication/read-back.

CURRENT_TDD_EVIDENCE: the supplied forged-basis RED was observed; additional REDs covered missing basis assembly, Actor subject crossing, unselected typed prior transport, stale Narrator binding after Chronicler, same-envelope Story transfer, trace/private diagnostics, token serialization, handoff reprojection after fresh Narrator rebind, and consumed-basis replay. The mechanical RD05 raw-bundle fixture failure was also observed before the one-file API synchronization. All listed focused witnesses are GREEN in the combined current module run.

VERSION_IMPACT: NONE — `turn_runtime.py` is unversioned implementation support; changed TurnEnvelope and NarrationResult JSON schemas are transient, carry no HDM `schema_version`, and are not persistent record families. Campaign/storage/catalog/engine generations, migration, and dual-read remain unchanged.

SYSTEM_IMPACT: RESOLVED / NO ARCHITECTURE DELTA — the 2026-09-27 Senior T00H ruling supersedes exact-object authentication. Tracked composition supplies the capability; untrusted data-plane carriers cannot select or replace it. The focused tests reuse the existing T00H request/service override witnesses. No out-of-envelope producer/interface change is authorized; review, clean verification and maintenance PASS, publication/read-back pending.

INDEPENDENT_REVIEW_AT_GATE: **PASS** — fresh T06A review against `0d39b0122d71948a6940076b306eb881f447f8cb` confirms the Senior ruling resolves the prior exact-object-authentication finding; no remaining spec/code findings. Reviewer relied on controller-run focused test evidence and did not rerun tests. Code candidate `5550d30cb2e53f4e309725cf4a69f510c57f7af6` is local-only pending status synchronization/publication.
T06A_LATEST_VERIFICATION: RD10 + RuntimeHost composition + RD05 + RD11 focused modules: 156 passed; current-progress authority: 2 passed. Clean exact full DEV at candidate `5550d30cb2e53f4e309725cf4a69f510c57f7af6`: 1320 passed, 5 skipped, 4 known out-of-scope S6D failures; clean-head package provenance and zero-unclassified version census; maintenance audit PASS. Exact suite command: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto`. Four known failures: `test_s6d_04_mechanical_context_contract::test_dormant_ids_rejected_before_input_class_and_false_is_not_missing`, `test_s6d_05_portable_value_contract::test_route_rows_ids_and_embedding_edges_are_machine_verified`, `test_s6d_05_portable_value_contract::test_real_activity_action_request_binding_matrix_and_freeze`, `test_s6d_05_portable_value_contract::test_roll_retry_is_single_fixed_result_and-offers-reject-stale-owner`. Targeted version/provenance/current-progress suite: 18 passed. Hosted CI unavailable.
T06A_T00H_EVIDENCE: reused `RuntimeHostCompositionTests.test_untrusted_request_data_cannot_select_or_replace_transport` and `test_gameplay_methods_reject_capability_and_service_overrides`; both are included in the passing RuntimeHost composition module.
T06A_FINAL_STATUS_HEAD_VERIFICATION: after evidence/cursor commit `32c10ea902b769f0122da3d1c66d3090587e0d85`, clean detached exact suite repeated with the same result: 1320 passed, 5 skipped, four named S6D failures; maintenance audit PASS; version/provenance/current-progress targeted suite 18 passed; scratch tree clean.
T06A_REVIEW_FINDING: historical HIGH observation — `ContextAssembler` is structural. The 2026-09-27 Senior T00H ruling supersedes exact-object authentication under the accepted TCB model; independent re-review must evaluate data-plane selection/replacement negatives and must not reject a trusted structural test harness solely for not being concrete RuntimeHost.ContextService.
T06A_RUFF_BASELINE_NOTE: scoped Ruff check passes on TurnRuntime and RD10. Full-file RD05 Ruff reports eight existing I001/F841/SIM117 findings outside the changed fixture hunk; the explicit scoped check ignoring only those baseline codes passes across the three changed Python files. `git diff --check` passes.
T06A_ADDITIONAL_RED_GREEN: basis reuse after its phase binding was replaced failed the new negative witness before the per-turn bound-basis-ID guard; the final RD10 suite passes it.
T06A_RD05_FIXTURE_RED_GREEN: the RD05 consumer's baseline raw-`bundle_id` call failed; its one-file fixture synchronization now invokes `bind_phase_from_context` with one test ContextService capability and preserves the W02 accepted-execution/idempotency assertions. No W02 producer change was made.

UNPUBLISHED_WORK: T06A code candidate `5550d30cb2e53f4e309725cf4a69f510c57f7af6` is committed locally; progress/cursor status synchronization and non-force publication/read-back remain pending. T06B remains blocked until T06A is accepted and PO-011 is consumed.

## W04.T06A capability-authenticity Senior resolution — 2026-09-27

RULING: `DEV/docs/superpowers/design/2026-09-27-w04-t06a-contextservice-authenticity-senior-ruling.md`

DISPOSITION: **NO ARCHITECTURE DELTA / TARGETED IMPLEMENTATION RULING**.

The independent HIGH observation is retained as useful evidence about the structural port, but its requested exact-object authentication is outside the accepted T00H threat model. Tracked deterministic HDM Python, runtime-host/bootstrap composition and test-harness fixture injection are inside the trusted computing base. A fake Python assembler passed directly by test code is therefore not by itself an admitted gameplay authority bypass.

T06A may retain a narrow structural Context assembler port only as a trusted composition dependency. It must never be selected, reconstructed, serialized or replaced through TurnEnvelope, request/candidate/model data, prior results or another gameplay/data-plane carrier. The operation invokes that injected port exactly once and validates role/purpose/profile/subject/recipient/current frontier before minting the phase-local transient basis. Raw mappings and caller-shaped bundle fields remain non-provenance and fail closed.

Do **not** add a local token/registry/marker, nominal RuntimeHost identity test, reverse dependency or new producer evidence solely to authenticate arbitrary in-process Python objects. The accepted T00H owner already assigns exact product composition to the fixed `RuntimeHost.context` service and Wave-05 bootstrap wiring. If implementation discovers an admitted data-plane service override or truly needs to change ContextService/RuntimeHost contracts, the System-Impact Gate reopens.

This resolution authorizes implementation/re-review only; it does not accept the unpublished T06A candidate and does not authorize T06B.


## Historical evidence retention

Earlier review/candidate evidence is retained verbatim at this cursor path:

- Commit `df83bc7c37e1f1d0fdeebd583350bf377a4c8f37`, blob `bf2f796710c6c6892588687b57e543e1f30a6bb2`: submitted T07C repair verification and T04B System-Impact gate state.
- Commit `959de8e2d91e46ff326b046ee39045afa04b952d`, blob `d12e3bc60a4feb6ba7067526f12f4cf0c86b9236`: submitted T04B/T07C candidates and worker verification evidence.
- Commit `a5cd9c517913bcf04d7acfbe895be49cdf941111`, blob `be512b4f01e745c62b44fdd719b68672749dbe1a`: submitted T04B/T07B candidates, author verification and pre-review gates.
- Commit `3c1a9ca1e31e46f8101944ee668a52bd3d3678ff`, blob `7485d887226b93896c03c71fe64aa6177524afe7`: earlier repair candidates, local verification limitations and previous findings.
- Commit `b13496b19bc8a7f11b82a24e11508036e815596f`, blob `82560dd4b321a91c9f438401b964bcd6904f6ed3`: complete earlier Source Manifests, System-Impact rulings, rejected attempts/restores, version chains, original CLS preflight and author verification.

Those snapshots are historical evidence, not competing current cursors or planning authorities. No whole-wave restore, new host prerequisite, production implementation by the reviewer, migration, release, gameplay bootstrap, new branch/ref or force update is authorized here.
