# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: EXECUTING
CURRENT_TASK: restore rejected W04 task surfaces to accepted clean basis `80d1cedfce7f529df96ea2c4b2342ce466cc8806`, then execute W04.T00H runtime-host composition before T01A/T05A/T07A resume
LAST_COMPLETED_TASK: Wave-04 stable-plan decomposition, self-review/control synchronization and final pre-implementation baseline freeze
LAST_SAFE_SHA: 6cbde6a4845376ee55e8e9c10a17f354111a276d

## Execution policy

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after producer independent reviewer PASS is published/read back
SYSTEM_IMPACT: stops only affected lane; independent lanes continue
VERSION_SYNC: shared/global version owners are reserved and serialized before publication

The detailed execution decomposition, write sets, mandatory REDs and protected boundaries are owned by the stable Wave-04 plan. This cursor records scheduling/currentness only and does not override it.

## Lane graph

COLLABORATION:
T01A -> T01B -> T01C
T01C -> T02A -> T02B -> T02C -> T04A -> T04B
T01C -> T03A in parallel with T02A-T02C

CONTEXT / EMISSION:
T05A -> T05B
T05B + T04B -> T05C -> T06A -> T06B

STORY / COMMENTATOR:
T07-PREFLIGHT -> T07A -> T07B -> T07C -> T07D -> T07E -> T07-INTEGRATION
No T07A RED before the mandatory fresh cross-project preflight is recorded.

FINAL CONSUMERS:
T04B + T02C + T07-INTEGRATION -> T08A
T06B -> T08B
T08A + T08B + T03A -> T08C
T08C + all lane checkpoints -> FINAL_REVIEW

## Initial scheduler

READY_NOW: []

COORDINATOR_GATE_READY_NOW: []

NOT_READY:
- T01B through T04B wait a Senior ruling for W04.T01A System-Impact
- T05B through T06B wait a Senior ruling for W04.T05A System-Impact
- T07A waits fresh private CLS evidence after PREFLIGHT_UNAVAILABLE
- T03A/T02A wait T01C reviewer PASS
- T04A waits complete T02C
- T05C waits T05B + T04B
- T06A waits T05C
- T08A/T08B/T08C wait their named joins

No Wave-04 production subtask is currently eligible. The lane stops are independent: a Senior ruling may resume only its affected lane, and a restored private evidence route may independently unblock the Story preflight.

## Write-set reservations

COLLABORATION LANE:
- GAME/TOOLS/collaboration.py
- DEV/TESTS/test_rd12_collaboration.py
- collaboration obligation/closed-basis/handoff/frontier/catch-up schemas
- DEV/SCHEMAS/intent-clause.schema.json where owned by the subtask
Only one collaboration-lane worker at a time.

PLAYER DELTA:
- DEV/TESTS/test_rd16_world_family_machine_integration.py
- bounded Wave-05 player delta evidence only
No physical shared PLAYER schema write.

CONTEXT LANE:
- GAME/TOOLS/context_runtime.py
- GAME/TOOLS/context_budget.py when required
- DEV/TESTS/test_rd11_context_runtime.py
- Context owner-local schemas
Only one Context-lane worker at a time.

EMISSION LANE:
- GAME/TOOLS/turn_runtime.py
- GAME/TOOLS/emission.py
- DEV/TESTS/test_rd10_role_emission.py
- owner-local turn/handoff/narration schemas
Starts only after Context integration.

STORY LANE:
- GAME/TOOLS/history.py
- GAME/TOOLS/story.py
- GAME/TOOLS/commentator.py
- GAME/TOOLS/dramaturg.py
- DEV/TESTS/test_rd13_story_t0_commentator.py
- owner-local Story/T0/Commentator/Dramaturg schemas
Only one Story-lane implementation worker at a time because the primary test file is shared.

FINAL CONSUMERS:
T08A and T08B use disjoint focused test/delta surfaces and may execute in parallel after their inputs are GREEN. T08C is the convergence checkpoint.

## Pre-implementation risk controls learned from Wave 03

1. TYPED_OBJECT_IS_NOT_AUTHORITY
   - Every new collaboration/history/context/control carrier must prove its producer/currentness boundary.
   - Public constructor, Protocol, subclass, structural shape, token/registry or caller-provided validator cannot substitute for native owner admission.

2. CURRENTNESS_IS_FULL_BASIS
   - Same revision with changed relevant body/basis must fail closed.
   - Projection/current flags cannot substitute for exact source/owner currentness.

3. NO_REVERSE_AUTHORITY
   - Collaboration cannot authorize PLAYER/access.
   - Context cannot establish truth/knowledge/access.
   - Story/Commentator cannot establish native history/access.
   - Dramaturg cannot establish canon.
   - Session cannot establish campaign/LIVE/PLAYER authority.

4. NO_SHARED_FINAL_WRITER_THEFT
   - W04 emits deltas only for Wave-05-owned shipped CORE/shared schemas/catalogs.

5. NO_LATE_VERSION_SURPRISE
   - Persistent collaboration and Story/PO-009 schema impacts are evaluated at the first material row, not at wave end.
   - Durable Context/Turn control introduced for convenience is a System-Impact event.

## Story completeness gate

T07B is not allowed to close with an EVENTS-only implementation.

Required baseline registrations:
- T-MSG and T-ARC -> TRANSCRIPT
- E-EVT and E-REL -> EVENTS
- M-SEG and M-OUT -> MECHANICS
- N-EVT and N-REL -> NARRATIVE

The current owner-local schema set lacks a Story TRANSCRIPT unit schema; T07B owns the missing owner-local machine contract and the complete eight-registration coverage tests. Coverage/currentness remains per source-domain/generation/cardinality, never one global Story frontier.

## W04.T07 mandatory preflight

PREFLIGHT_DISPOSITION: PREFLIGHT_UNAVAILABLE

Fresh public HDM evidence was read at `6cbde6a4845376ee55e8e9c10a17f354111a276d`:

- `2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` blob `ea3dea6653c356c3be5529ff8c916740a0f39b6d`;
- `2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` blob `566f6d2e70087aa0abc93108c562d3b8e2d77023`;
- `2026-09-08-story-baseline-projection-source-contracts.md` blob `4e85a2899657f43c2bb812e9608d9d0c254b4a96`;
- `2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md` blob `3718ac404acade3bef84a655414258785bab5413`;
- `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` blob `5cd35b8f9782b53915591fd2967bff22edaf43fe`.

The required fresh private CLS paths could not be read:

- `audit/cls-project-audit-workspace` -> `CLS-AUDIT/CURRENT_AUDIT_STATE.md` and `CLS-AUDIT/graph/HDM_INTEGRATION_GRAPH.md`;
- `feature/commentator-language-stack` -> `HDM-CLS/docs/SENIOR_AUDITOR_HDM_INTEGRATION_HANDOFF.md` and `HDM-CLS/docs/CURRENT_PROGRESS.md`;
- `git ls-remote git@github-hdm:dkolyada/hedgelion-dnd-master-lab.git` returned `Repository not found` for both required refs;
- `git ls-remote git@github.com:dkolyada/hedgelion-dnd-master-lab.git` returned `Permission denied (publickey)`;
- the local runtime has no `gh` command for an authenticated GitHub read route.

The current W04 task Source Manifest is the stable Wave-04 plan execution section in `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`, blob `cdbc1d2bbc651ff6b087e22b8d502ec46bbc7386`. The historical WP-24 manifest is not substituted for this current W04 manifest.

No private ref/blob was inferred from planning-time evidence. Per the stable plan, only Story is stopped. Re-run the exact preflight after a current read-only private CLS route is available; do not begin W04.T07A RED first.

## System-Impact briefs

### W04.T01A - collaboration admission

TRIGGER: the current W03 owner exports owner-issued `PlayerResolution` for principal-to-PLAYER/control authorization, but no native coordination dependency/currentness/opportunity/durability/order result that W04.T01A can consume and revalidate.

CURRENT_TASK: Senior must rule whether an existing W03 owner-native participant/currentness result can be consumed and revalidated by T01A, or whether the missing coordination boundary must return to design; keep T01A-T04B stopped pending that ruling.

RECOMMENDATION: Do not resume with a local issuer, callback, token, registry or caller route; choose a native W03 route or return to design for an explicit owner boundary.

COST/RISK IF WRONG: Resuming without the owner boundary can mint participant authority and persist unauthorized or cross-scope collaboration; continuing the stop costs only collaboration-lane schedule time.

LAST_SAFE_SHA: `6cbde6a4845376ee55e8e9c10a17f354111a276d`

APPROVED EXPECTATION: T01A admits only exact native participant authority; caller-provided constructors, structural shapes, tokens, registries, callbacks and routes cannot mint it.

DISCOVERED PRESSURE: a local collaboration issuer or caller-provided route/loader inevitably mints or substitutes authority. The attempted W04 implementation and its repairs were restored: `a300b23774f9ed31dfbc991be73211c338976955`, `59b12a3075155c9f5984420691ff98be32562c6f`, and `de3254041b1126a5f46f53e1b8fcbee27153f968` are removed by `6cbde6a4845376ee55e8e9c10a17f354111a276d`.

AFFECTED OWNERS: W03 participant/currentness authority and the future collaboration admission consumer.

PROTECTED INVARIANTS: Collaboration never grants PLAYER/access authority; complete source basis, not a typed carrier/current flag, establishes currentness.

WHAT CAN PROCEED: no dependent collaboration subtask. Context and Story were independent but are separately stopped below.

SAFE OPTIONS: (1) Senior specifies an existing owner-native W03 result/admission route that T01A may consume; or (2) return to design for an explicit owner interface/boundary. No local bridge, callback, token or registry is authorized.

UNPUBLISHED_WORK: NONE.

### W04.T05A - Context admission

TRIGGER: the current W03 route accepts caller-constructible LIVE/projection carriers and callbacks but supplies no native reload or registered role/purpose eligibility binding for Context admission.

CURRENT_TASK: Senior must rule whether an existing W03 owner-native reload and registered role/purpose eligibility route can be consumed by Context, or whether the missing boundary must return to design; keep T05A-T06B stopped pending that ruling.

RECOMMENDATION: Require owner-routed LIVE/PLAYER/information eligibility and reject caller carriers, callbacks, registries and durable Context state.

COST/RISK IF WRONG: Resuming on shaped carriers can admit stale or forged currentness and disclose out-of-scope material; continuing the stop costs Context/emission schedule time.

LAST_SAFE_SHA: `6cbde6a4845376ee55e8e9c10a17f354111a276d`

APPROVED EXPECTATION: `current=True`/`eligible=True`, shaped carriers and physical/index/cache presence are only post-resolution data and never caller authority.

DISCOVERED PRESSURE: accepting those existing carriers permits internally consistent forged currentness/eligibility and loses role/purpose binding. The attempted implementation `e55cc560fee431460cdc5753abb94be9f5433008` was restored by `2c0a893f428e2e822d74c8fefc69f27f5b3f259a`.

AFFECTED OWNERS: W03 LIVE/PLAYER/information currentness and eligibility owners; Context admission consumer.

PROTECTED INVARIANTS: Context cannot establish truth, knowledge or access; currentness is a complete owner/source basis.

WHAT CAN PROCEED: no dependent Context or emission subtask.

SAFE OPTIONS: (1) Senior identifies an existing owner-native reload/role-profile route that T05A may consume; or (2) return to design for an explicit interface/boundary. No caller callback, registry, durable Context state or W03 interface change is authorized.

UNPUBLISHED_WORK: NONE.

## Verification / completion state

CURRENT_VERIFICATION_STATE:
- Wave 03 is globally CLOSED / Senior PASS; post-closure F63-F65 targeted repair is independently Senior PASS with hosted validation 992 passed / 6 skipped.
- Wave-04 stable plan decomposition is published.
- W04.T01A and W04.T05A attempted implementations were independently reviewed, restored to the pre-W04 owner tree, and await the two recorded Senior System-Impact rulings.
- W04.T07 mandatory preflight is `PREFLIGHT_UNAVAILABLE`; no W04.T07 RED or implementation occurred.
- No Wave-05 final-writer surface has been authorized for W04.

VERSION_IMPACT:
- This documentation-only repair is NONE; no current version-bearing owner or projection changes.
- Current W04 production-tree impact is NONE after restoration; this does not retrospectively classify either aborted implementation as a compliant NONE assessment.
- `a300b23774f9ed31dfbc991be73211c338976955` added optional but semantic collaboration fields to persisted `DEV/SCHEMAS/intent-clause.schema.json`, whose owner is the runtime Interaction/IntentPlan. It was never accepted and was restored; no bump is made now. A future reattempt must run the owner-specific persistent-contract Version Impact Gate before claiming an additive/compatible/no-bump result.
- `e55cc560fee431460cdc5753abb94be9f5433008` materially changed the Context runtime without a compliant version assessment and was restored. No current-tree version change exists; any reattempt must classify the actual module namespace before publication.
- Cursor evidence only: NONE.

SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED — W04.T01A and W04.T05A briefs above. W04.T07 is separately PREFLIGHT_UNAVAILABLE, not a System-Impact classification.
NEXT_EXACT_TASK: obtain a Senior ruling for the two System-Impact briefs and restore a read-only private CLS evidence route; then reschedule only the specifically unblocked lane.
KNOWN_BLOCKERS: T01A-T04B await T01A ruling; T05A-T06B await T05A ruling; T07A awaits fresh private CLS evidence. No Wave-04 production task is currently eligible.
UNPUBLISHED_WORK: NONE after publication/read-back.


## Senior gate resolution — 2026-09-21

SENIOR_REVIEWED_PUBLIC_HEAD: `5b3841ffe17bbea0e0663342eab1278427d6b07c`
OUTCOME: **TARGETED_REPAIR_REQUIRED / NO ARCHITECTURE REOPEN**
AFFECTED_LANES: W04.T01A, W04.T05A
W04.T07_PREFLIGHT: **PASS**

### SR-W04-T01A — coordination admission stays Collaboration-owned

RULING: **TARGETED_REPAIR_REQUIRED / SYSTEM_IMPACT RESOLVED**

No new W03 `coordination authority` result, local issuer, callback-authority, token registry or second currentness owner is required or permitted.

The accepted owner split already supplies the machine route:

1. `runtime.interaction` and `runtime.intent_plan` are existing accepted native owners with known-ID physical routes under WP-11 and existing schemas `runtime-interaction-state.schema.json`, `runtime-intent-plan-state.schema.json` and embedded `intent-clause.schema.json`.
2. W03 owns current principal -> exact current PLAYER/control authorization. Use its owner-native route/revalidation; do not accept caller-minted PLAYER/currentness carriers.
3. R2.5/WP-17 **itself owns coordination-family admission and material-dependency classification**. W03 does not and must not mint that result.
4. An accepted Interaction/IntentClause may nominate a bounded dependency candidate, scope and referenced participants/native owners; it is discovery/input evidence, not final authority.
5. Before choosing a coordination family or enrolling a required contributor, Collaboration must re-read/revalidate the smallest applicable native currentness/ownership/chronology basis required by the dependency class.
6. Existing native Procedure/Continuation/Choice/Reaction ordering wins and produces `RULE_OWNED_ORDERED`; Collaboration does not mirror it.
7. Only a positive bounded current material dependency may produce `AGENCY_DEPENDENT_COLLECTIVE`; failure to prove independence is not sufficient. Otherwise use `INDEPENDENT_IMMEDIATE`.
8. Exact known-ID native loads may use the existing host/storage transport boundary, but loaded identity/schema/currentness must be owner-validated. A callback returning `is_current`, `required_players`, `coordination_family` or equivalent semantic verdict is forbidden.
9. The W04 owner-local admission result may be a derived typed result minted by `collaboration.py` **after** those validations. It owns only collaboration admission/collection semantics and carries references/evidence identities; it does not become PLAYER, LIVE, chronology, Procedure or Interaction authority.

Required REDs remain those in stable T01A plus explicit rejection of:
- caller-selected coordination family;
- caller-selected required-contributor set without native revalidation;
- caller-supplied boolean/callback currentness;
- stale/foreign Interaction/IntentPlan/PLAYER/native-opportunity basis;
- generic collaboration when an admitted native ordered owner applies.

The prior restored attempts are non-precedential. Re-run the persistent-contract Version Impact Gate for any actual `intent-clause.schema.json` change.

### SR-W04-T05A — Context currentness/eligibility is owner-routed resolution, not carrier trust

RULING: **TARGETED_REPAIR_REQUIRED / SYSTEM_IMPACT RESOLVED**

No new W03 Context carrier, currentness token, eligibility issuer or durable Context authority is required or permitted.

R2.3 + WP08 + WP09 already require T05A to realize:

```text
registered RoleContextRequest + registered ContextNeedProfile
-> bounded candidate discovery/routing hints
-> exact routed native-owner reload
-> native currentness + role/purpose/recipient eligibility validation
-> internal post-resolution candidate basis
-> packet closure/allocation
```

Implementation constraints:

1. Caller-shaped candidate objects, `current=true`, `eligible=true`, scene/index/cache presence and physical prompt presence are discovery hints only.
2. Before semantic use, T05A must resolve the candidate through its routed current native owner. Use existing owner routes:
   - current PLAYER/control through W03 access-control resolution;
   - selected LIVE/currentness through W03 LIVE owner validation;
   - information/knowledge/disclosure through their native owners and recipient eligibility;
   - other candidate families through their existing known-ID native routes/validators.
3. A host-injected exact-load transport may provide bytes/records; it may not return semantic `current`/`eligible` verdicts. Context performs/dispatches owner validation.
4. `ContextNeedProfile` registration and role/purpose/subject/recipient binding are Context/consumer-contract responsibilities already accepted by R2.3/R2.4/WP08/WP09. T05A may realize the finite registered profile table/contracts in its allowed Context scope; the caller/LLM cannot invent a profile or widen it.
5. The existing `current` / `eligible` fields may remain only on an internal owner-resolved result after successful validation. They are never accepted as authority-bearing input.
6. If a discovered family lacks an admitted exact owner route/eligibility resolver, that candidate fails closed or yields the registered terminal/degraded outcome; do not invent a generic callback or broaden into a scan.
7. Context remains an ephemeral projection and cannot establish truth, PLAYER/access, knowledge/disclosure or LIVE authority.

Mandatory REDs include forged booleans/carriers, stale PLAYER/LIVE, wrong role/purpose/profile/recipient, scene/index/cache-only admission, and a fake semantic callback that claims current/eligible without native reload.

The prior restored attempt is non-precedential. Re-run module/version impact against the actual accepted implementation.

### SR-W04-T07 — mandatory CLS↔HDM preflight

RESULT: **PREFLIGHT_PASS / SYSTEM_IMPACT NONE**

Private refs were read directly through GitHub Connector:

- audit workspace `6273260c55107bc769d355875da749c9ef3c9296`;
- feature CLS `0f88185966aed937852824db7417f83487beef23`.

Exact required artifacts/blobs:

- audit state `c5fe22947ec6e573c15f686c3840579f9a3e19d2`;
- HDM integration graph `1665618d0276c7a150956d6f4664b085f8bfdac2`;
- Senior-Auditor handoff `0fc0ca7ef1072d6fd9614efe92e62f0807da838e`;
- feature current progress `0eae6d528f606caa1721bdb433270755aad2d9a1`;
- WP12-04 Source Manifest `4caa601d5c43cbdfb51ff121a21b2b63a5df5cee`;
- WP12-04 canonical design `96ba235d535a9088ef8d808c40b0b92e18cbdc53`;
- architect wide-angle PASS `9e7500e8cd0cc9011fae6c1b8bb13eedc38a5ed6`.

Public bytes at the reviewed head:
- SCC owner `ea3dea6653c356c3be5529ff8c916740a0f39b6d`;
- stable W04 plan `cdbc1d2bbc651ff6b087e22b8d502ec46bbc7386`.

Those public owner bytes are unchanged from the current CLS WP12-04 consumed basis. Current private WP12-04 explicitly reports no public HDM write, no public semantic reopen, no REAL integration claim, and keeps REAL source integration downstream. Post-manifest private changes only frame/design/activate the private retrieval package and do not create a new W04.T07 public contract.

Therefore W04.T07A may begin. The implementation still must obey the public SCC/Story/T0 owners and may not import private CLS implementation as public architecture.

## Resumption state

```text
W04.T01A: AUTHORIZED_FOR_TARGETED_REIMPLEMENTATION
W04.T05A: AUTHORIZED_FOR_TARGETED_REIMPLEMENTATION
W04.T07A: PREFLIGHT_PASS / AUTHORIZED
W04.T01B+: DEPENDENCY_GATED
W04.T05B+: DEPENDENCY_GATED
W04.T07B+: DEPENDENCY_GATED
WAVE_05: NOT AUTHORIZED
```

VERSION_IMPACT: NONE for this ruling/preflight documentation checkpoint.
SYSTEM_IMPACT: RESOLVED / NONE CURRENT.


## Current execution override after Senior resolution

STATUS: EXECUTING
CURRENT_TASK: W04.T01A / W04.T05A / W04.T07A may execute in parallel when write sets remain isolated.
LAST_SAFE_SHA: `5b3841ffe17bbea0e0663342eab1278427d6b07c` product tree before this documentation-only ruling.
CURRENT_VERIFICATION_STATE: restored pre-attempt production tree; three gates resolved above; normal task TDD/review/Version Impact applies.
VERSION_IMPACT: NONE for the Senior ruling checkpoint.
SYSTEM_IMPACT: NONE CURRENT; prior T01A/T05A events are resolved by SR-W04-T01A/SR-W04-T05A.
NEXT_EXACT_TASK: coordinator reschedules T01A, T05A and T07A; each publishes only after its own hdm-reviewer PASS/read-back. Dependent tasks wait for named checkpoints.
KNOWN_BLOCKERS: NONE for T01A/T05A/T07A start.
UNPUBLISHED_WORK: NONE after publication/read-back.

## Execution stop after targeted reimplementation review

```text
STATUS: SENIOR_REVIEW_REQUIRED
CURRENT_TASK: resolve the three W04 System-Impact briefs before resuming T01A, T05A or T07A.
LAST_SAFE_SHA: `0bd665860386e04ecd2efb589e58069a4d6da033` restored product tree before the targeted reimplementation attempts.
LAST_PUBLISHED_SHA: `86138093021095fa24ec611314fa9482749c5afa`

CURRENT_VERIFICATION_STATE:
- T01A focused regression passed, but independent review rejected its unadmitted generic native opportunity contract.
- T05A focused regression and maintenance audit passed, but independent re-review rejected its caller-controlled exact-load boundary and missing native role/purpose eligibility binding.
- T07A focused regression and malformed-provenance repair passed, but independent re-review rejected its structural caller-provided NativeHistoryOwnerPort boundary.
- No rejected T01A/T05A/T07A implementation checkpoint authorizes a dependent task.

VERSION_IMPACT:
- T01A final task classification is pending the Senior resolution because the rejected implementation introduced a new module/schema and IntentClause semantic fields without accepted task-completion evidence.
- T05A repair commit `22e24951358bca8b3636a3c80fcbfa510e01d614` records `NONE` for unchanged existing version-bearing namespaces.
- T07A repair commits record `GAME/TOOLS/history.py` module revision `1.0.7`; native-history schemas remain at `1`; no engine, campaign, storage, catalog or shared projection bump was required.
- This cursor checkpoint: VERSION_IMPACT: NONE.

SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED
- T01A: no finite owner-defined, schema-validated native opportunity route exists for AGENCY_DEPENDENT_COLLECTIVE. Brief: `DEV/docs/superpowers/design/2026-09-21-w04-t01a-fix-round-1-system-impact-brief.md`.
- T05A: no approved trusted exact-load boundary or native role/purpose eligibility route exists. Brief: `DEV/docs/superpowers/design/2026-09-21-w04-t05a-fix-round-1-implementation-impact-brief.md`.
- T07A: no admitted W02/native owner adapter or composition-root boundary exists; structural port conformance is forgeable. Brief: `DEV/docs/superpowers/design/2026-09-21-w04-t07a-implementation-impact-brief.md`.

NEXT_EXACT_TASK: Senior/design resolution of the three recorded owner-boundary choices; do not run T01B+, T05B+, T07B+, or any Wave-05 task.
KNOWN_BLOCKERS: the three System-Impact briefs above.
UNPUBLISHED_WORK: NONE after publication/read-back.
```


## Final Senior/design ruling — 2026-09-21

AUTHORITATIVE_RULING:
`DEV/docs/superpowers/design/2026-09-21-w04-t01a-t05a-t07a-senior-design-rulings.md`

REVIEWED_STOP_HEAD: `35f979b3e05e10cc759f01361e7271d36941ff4e`

Fresh GitHub comparison proved rejected implementation residue remains. Before
new RED, restore the exact task production/schema/test paths listed in the ruling
to `0bd665860386e04ecd2efb589e58069a4d6da033`, preserving current design/control
artifacts.

After restore reviewer PASS/read-back:

```text
T01A: AUTHORIZED — accepted IntentClause is finite opportunity identity;
      Collaboration owns family classification after native revalidation.

T05A: AUTHORIZED — RepositoryPort + read-only Step-5.8 LIVE source read;
      registered ContextNeedProfile/RoleContextRequest owns role-purpose eligibility.

T07A: AUTHORIZED — fixed Step-5.10 campaign.semantic_events@S evt-lane adapter;
      no NativeHistoryOwnerPort.
```

CLS↔HDM preflight remains PASS unless its explicit trigger fires.

STATUS: EXECUTING
NEXT_EXACT_TASK: clean-basis restore -> local reviewer PASS -> publish/read-back
-> parallel T01A/T05A/T07A fresh TDD where write sets allow.
KNOWN_BLOCKERS: restore checkpoint only; no unresolved design decision.
SYSTEM_IMPACT: RESOLVED / NONE CURRENT.
VERSION_IMPACT: NONE for ruling/restore; each fresh task performs its own gate.

## Clean-basis restore acceptance — 2026-09-21

STATUS: EXECUTING
CURRENT_TASK: W04.T01A / W04.T05A / W04.T07A are authorized for fresh parallel TDD under the final Senior/design ruling.
LAST_SAFE_SHA: `ce05e58e9f398e779dcdda68cb9aec53e82cfe7a`
LAST_COMPLETED_TASK: mandatory clean-basis restore of the eleven ruled task production/schema/test paths to `0bd665860386e04ecd2efb589e58069a4d6da033`.
CURRENT_VERIFICATION_STATE: exact staged/worktree comparison to `0bd665860386e04ecd2efb589e58069a4d6da033` passed; independent local `hdm-reviewer` re-review PASS; diff check passed; non-force publication and remote read-back matched `ce05e58e9f398e779dcdda68cb9aec53e82cfe7a`. Full local DEV suite recorded 1006 passed, 6 skipped and 9 failures: five are generated GAME cache / `.entire/` contamination and four are unchanged S6D owner tests; exact-head hosted CI `35610456548` is SUCCESS.
VERSION_IMPACT: NONE for the restore and this execution-state checkpoint.
SYSTEM_IMPACT: NONE CURRENT; final Senior/design rulings resolve the prior T01A/T05A/T07A stops without architecture reopen.
NEXT_EXACT_TASK: dispatch W04.T01A, W04.T05A and W04.T07A with disjoint write sets; T07 CLS↔HDM preflight remains PASS unless its explicit semantic-change trigger fires.
KNOWN_BLOCKERS: none for the three root tasks; all downstream tasks remain dependency-gated; Wave 05 remains unauthorized.
UNPUBLISHED_WORK: NONE after restore publication/read-back.

## Runtime host composition acceptance — 2026-09-21

STATUS: EXECUTING
CURRENT_TASK: W04.T01A / W04.T05A / W04.T07A may execute in parallel with isolated write sets.
LAST_SAFE_SHA: `a7432515e500cc2caf21fe55db17f64a7fd0ed47`
LAST_COMPLETED_TASK: W04.T00H -> W04_RUNTIME_HOST_COMPOSITION_READY / W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY.
CURRENT_VERIFICATION_STATE: T00H RED/GREEN, host focused suite, cross-owner regression, direct Context tests, ruff, compile, diff check and maintenance audit passed; independent scoped re-review PASS; non-force publication/read-back at `a7432515e500cc2caf21fe55db17f64a7fd0ed47`.
VERSION_IMPACT: `GAME/TOOLS/runtime_host.py` new module `framework_module_version: 1.0.1`; no persistent schema, campaign/storage/catalog generation or Wave-05 projection change. Context import-resolution repair: NONE.
SYSTEM_IMPACT: NONE CURRENT; RuntimeHost and runtime_execution ordering producer routes are accepted by the owner decision.
NEXT_EXACT_TASK: dispatch T01A, T05A and T07A; T07 CLS↔HDM preflight remains PASS unless its explicit semantic-change trigger fires before RED.
KNOWN_BLOCKERS: none for the three root tasks; all downstream tasks and Wave 05 remain dependency-gated/unauthorized.
UNPUBLISHED_WORK: NONE after publication/read-back.

## Targeted reimplementation stop after final ruling

STATUS: SENIOR_REVIEW_REQUIRED
CURRENT_TASK: resolve the two recorded owner-boundary gaps before resuming W04.T01A, W04.T05A or W04.T07A.
LAST_SAFE_SHA: `ce05e58e9f398e779dcdda68cb9aec53e82cfe7a` clean task-surface restoration; `80d1cedfce7f529df96ea2c4b2342ce466cc8806` records its acceptance without changing product bytes.
LAST_PUBLISHED_SHA: `2eb3c28f480932db984240d5ea9f41954d744eaf`
CURRENT_VERIFICATION_STATE: targeted focused suites and maintenance audits passed at several rejected checkpoints, but independent reviewers found that no accepted producer validates native ordered-owner authority for T01A and that forged host construction mints Context/LOCAL history for T05A/T07A. No rejected checkpoint may unlock a dependent task.
VERSION_IMPACT: documentation checkpoint NONE. Rejected fresh-attempt module/schema transitions are recorded in `2026-09-21-w04-t01a-fix-round-4-system-impact-brief.md`; they are non-precedential and must not be reused as an accepted basis.
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED
- T01A: `DEV/docs/superpowers/design/2026-09-21-w04-t01a-fix-round-4-system-impact-brief.md` records that the only discovered complete ordering validator is a new manual/public mirror, not an admitted native owner route.
- T05A: `DEV/docs/superpowers/design/2026-09-21-w04-t05a-fix-round-4-system-impact-brief.md` records that caller-forged hosts mint Context and LOCAL history.
- T07A: `DEV/docs/superpowers/design/2026-09-21-w04-t07a-fix-round-3-system-impact-brief.md` records the same missing host composition route; T07A remains dependency-gated on its resolution.
NEXT_EXACT_TASK: Senior/design identifies the complete T01A native ordering-validator producer/composition/currentness route and the T05A/T07A non-replaceable host composition route, or returns the affected boundary to design. Do not run T01B+, T05B+, T07B+, or Wave-05.
KNOWN_BLOCKERS: the two System-Impact gaps above.
UNPUBLISHED_WORK: NONE after publication/read-back.


## Senior route owner decision — 2026-09-21

AUTHORITATIVE_DECISION:
`DEV/docs/superpowers/design/2026-09-21-w04-runtime-host-ordering-route-owner-decision.md`

REVIEWED_STOP_HEAD: `256c4916fecaf38c40c890570f65815cae4df2bb`

```text
SYSTEM_IMPACT: RESOLVED
ARCHITECTURE_REVIEW_REQUIRED: NO

NEW PREREQUISITE:
  W04.T00H runtime host composition
  -> W04_RUNTIME_HOST_COMPOSITION_READY
  -> W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY

T01A:
  ordered producer = Step-3 runtime_execution owner
  positive proof = exact current Resolution(AWAITING_CHOICE/REACTION)
                   -> exact Continuation generation
                   -> pending ChoiceRequest/ReactionOffer
                   -> ACTIVE Procedure if linked
  Procedure existence alone != ordered proof
  mechanics.py helper forbidden

T05A:
  no caller BoundContextRuntime/repository/live override
  Context is a sibling service under campaign-bound RuntimeHost

T07A:
  no caller History service/repository/live override
  History is a sibling service under the same RuntimeHost
  Step-5.10 evt source-domain route remains authority geometry
```

Threat-model clarification: arbitrary Python object fabrication/mutation inside
tracked deterministic runtime is TCB compromise, not a gameplay caller path.
Negative review targets admitted model/player/data/API surfaces. A deployment
that permits untrusted Python execution inside this TCB is unsupported and must
supply process/tool isolation rather than an in-process token.

### Mandatory clean restore before T00H

Restore exactly to `80d1cedfce7f529df96ea2c4b2342ce466cc8806`:

```text
DEV/SCHEMAS/context-need-profile.schema.json
DEV/SCHEMAS/context-trace.schema.json
DEV/SCHEMAS/intent-clause.schema.json
DEV/SCHEMAS/native-history-currentness.schema.json
DEV/SCHEMAS/native-history-publication.schema.json
DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json
DEV/TESTS/test_rd09_access_live.py
DEV/TESTS/test_rd11_context_runtime.py
DEV/TESTS/test_rd12_collaboration.py
DEV/TESTS/test_rd13_story_t0_commentator.py
GAME/SCHEMA/collaboration_obligation.schema.yaml
GAME/TOOLS/collaboration.py
GAME/TOOLS/context_runtime.py
GAME/TOOLS/history.py
GAME/TOOLS/live_state.py
GAME/TOOLS/mechanics.py
```

Delete paths absent at the clean basis. Preserve current design/version evidence,
cursor/current-progress and unrelated accepted build/tool-discovery changes.

Restore -> baseline verification -> local hdm-reviewer -> publish/read-back ->
T00H -> reviewer PASS -> T01A/T05A/T07A.

The existing T07 CLS↔HDM preflight remains PASS unless its explicit semantic
trigger fires before T07A RED.

VERSION_IMPACT: NONE for this decision/restore; fresh task-local gates apply.
KNOWN_BLOCKERS: clean restore + T00H checkpoint only.

## Runtime-host restore acceptance — 2026-09-21

STATUS: EXECUTING
CURRENT_TASK: W04.T00H runtime-host composition only.
LAST_SAFE_SHA: `e7909df857e79d181dca5527609754def4248cc4`
LAST_COMPLETED_TASK: mandatory 16-path clean restore to `80d1cedfce7f529df96ea2c4b2342ce466cc8806` under the runtime-host/ordering route owner decision.
CURRENT_VERIFICATION_STATE: exact restore comparison, diff check, focused RD09/RD11/RD13 suite (208 passed), maintenance audit and independent local `hdm-reviewer` PASS completed before non-force publication/read-back at `e7909df857e79d181dca5527609754def4248cc4`.
VERSION_IMPACT: NONE for restore and this cursor checkpoint.
SYSTEM_IMPACT: NONE CURRENT; the owner decision supplies T00H and the native ordered-evidence route.
NEXT_EXACT_TASK: W04.T00H -> reviewer PASS/publish/read-back -> W04.T01A/W04.T05A/W04.T07A in parallel.
KNOWN_BLOCKERS: T01A/T05A/T07A wait `W04_RUNTIME_HOST_COMPOSITION_READY`; all downstream tasks and Wave 05 remain dependency-gated/unauthorized.
UNPUBLISHED_WORK: NONE after restore publication/read-back.
