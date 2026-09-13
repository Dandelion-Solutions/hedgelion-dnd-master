# HDM Implementation Planning — Author Second-Pass Repair Addendum

Status: **CURRENT MANDATORY SECOND-PASS ADDENDUM — EXECUTION NOT AUTHORIZED**
Date: 2026-09-13
Baseline: `db23d097abfb9a2cfdbeb88b115689566a575bed`
Production implementation authorized: **NO**.

This addendum repairs ASR-004 and ASR-005. Current route precedence is:

```text
base RD plan
+ SIRR repair addendum where applicable
+ first author self-review repair addendum where applicable
+ this second-pass addendum where applicable
```

This file supersedes only conflicting Story topology/bootstrap-coupling details from earlier overlays. It creates no new owner, readiness identity, RD unit or product semantic.

---

## A. ASR-004 — exact Story physical routing

### A1. Canonical route contract

RD-13 Task 4 MUST use the exact WP-11/WP-18 exceptional Story routes selected by `MANIFEST.storage.story_root`:

```text
<story_root>/TRANSCRIPT/PROJECTION_STATE.yaml
<story_root>/EVENTS/PROJECTION_STATE.yaml
<story_root>/MECHANICS/PROJECTION_STATE.yaml
<story_root>/NARRATIVE/PROJECTION_STATE.yaml

<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

where:
- `<story_root>` is the static campaign-root-relative selector from WP-11/RD-04, expected value `STORY` in the v1 campaign template;
- `<layer>` is exactly one of `TRANSCRIPT | EVENTS | MECHANICS | NARRATIVE`;
- `sequence` is the accepted layer-local Story sequence allocated by that layer's Story projection state;
- bucket is the decimal value `floor(sequence/1000)` under the canonical route; workers may not substitute hash sharding, global sequence, arbitrary padding or another partition scheme unless a later owner decision explicitly supersedes WP-11/WP-18;
- `<story_id>` is the accepted layer-local Story ID represented under the Story owner contract.

Route/bucket/sequence are Story-local addressing. None establishes fictional chronology, native history order, gameplay currentness, source authority or cross-layer priority.

### A2. RD-13 Task 4 file/action replacement

The vague base-plan phrase:

```text
layer-local projection-state location selected by existing Story owner/scaffold convention
```

is superseded.

Future implementation file actions are exact:

```text
Create on first materialization for each materialized layer:
  <resolved story_root>/<layer>/PROJECTION_STATE.yaml

Create each Story unit at:
  <resolved story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

No generic `STORY/INDEX`, global projection state, global Story allocator, campaign-wide Story frontier or alternate partition is admitted.

The implementation may use helper functions, but their public contract must preserve:

```text
resolve_story_projection_state_path(story_root, layer)
    -> <story_root>/<layer>/PROJECTION_STATE.yaml

resolve_story_unit_path(story_root, layer, sequence, story_id)
    -> <story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

These helpers perform deterministic path construction only; they do not own semantic identity or currentness.

### A3. Focused RED/GREEN tests

Add to `DEV/TESTS/test_rd13_story_t0_commentator.py`:

```text
StoryPhysicalRouteTests.test_projection_state_path_is_exact_owner_route
StoryPhysicalRouteTests.test_story_unit_uses_exact_layer_local_thousand_bucket
StoryPhysicalRouteTests.test_all_four_layers_use_separate_projection_state
StoryPhysicalRouteTests.test_story_sequence_does_not_define_fictional_chronology
StoryPhysicalRouteTests.test_manifest_story_root_is_static_route_only
StoryPhysicalRouteTests.test_no_global_story_index_allocator_or_frontier
```

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryPhysicalRouteTests -v
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator.StoryProjectionTests -v
```

`R016.STORY` and `R018.STORY` cannot close until these exact routes and Story projection behavior are green.

---

## B. ASR-005 — static Story selector without bootstrap Story prerequisite

### B1. Correction to first self-review ASR-001 repair

The first self-review addendum correctly requires seven MANIFEST selectors and local campaign manifest schema `4 -> 5`, but the following earlier statements are superseded:
- the selector checkpoint does **not** require RD-13 Story files/root contents to exist;
- no `ROOT_SELECTOR_CUTOVER` may force Story materialization before New Game/bootstrap can be valid;
- RD-14 generated-root validation must **not** require physical `STORY/**` at blank-campaign creation.

WP-11 topology ownership and WP-18 Story materialization are separate.

### B2. RD-04 selector/schema checkpoint — corrected acceptance

RD-04 `R064-FIXED-ROOTS` remains the owner of MANIFEST/schema static selectors.

Files remain:
```text
GAME/CAMPAIGN/MANIFEST.yaml
GAME/SCHEMA/campaign_manifest.schema.yaml
GAME/CORE/STORAGE.md
DEV/TESTS/test_rd04_native_routing_index_hot.py
DEV/TOOLS/audit_engine.py
```

Required selector set remains exactly:
```text
state_root: STATE
index_root: INDEX
world_root: WORLD
event_log_root: LOG
checkpoints_root: CHECKPOINTS
sessions_root: SESSIONS
story_root: STORY
```

Corrected RED/GREEN assertions:
1. template + schema require all seven selectors exactly once;
2. schema/template values agree with WP-11 static routes;
3. selector fields own no mutable Story/session/currentness/coverage state;
4. `sessions_root` points to the already generated `SESSIONS` template root;
5. `story_root` is a legal static route even when no `STORY/**` file has yet been materialized;
6. absence of current Story files is not an integrity error and cannot block campaign creation/gameplay;
7. once Story materializes, RD-13 resolves only below the selected static root through the exact ASR-004 routes.

Future version consequences remain:
- campaign manifest local schema `4 -> 5`;
- no campaign-contract generation bump solely for the pre-release clean-slate change;
- no storage-format generation bump;
- no compatibility migration solely for obsolete pre-release manifest shapes;
- `GAME/CORE/STORAGE.md` material edit `1.0.1 -> 1.0.2`.

The RD-04 selector/schema checkpoint may become green independently of Story projection creation.

### B3. RD-13 Story materialization lifecycle

RD-13 consumes `MANIFEST.storage.story_root` but materializes Story only when its source/candidate contract actually requires Story projection work.

A blank campaign requires no Story unit, T0 materialization, projection-state file, Story layer directory, Story backlog or Chronicler service state merely to become playable.

On first materialization of a layer:
1. resolve current static `story_root`;
2. create/load that exact layer's `PROJECTION_STATE.yaml` under ASR-004;
3. enumerate only admitted source candidates;
4. write legal Story units under the exact bucket route;
5. publish through ordinary RD-06 campaign publication;
6. advance that layer/source-domain coverage only after legal terminal disposition and accepted publication.

Story loss/absence/lag remains non-blocking for gameplay except for a consumer that explicitly requires an already promised Story-derived capability under its owner.

### B4. RD-14 generated-scaffold/bootstrap consumer correction

RD-14 must distinguish **manifest routes** from **physically pre-materialized roots**.

Future shipped consumer edits:

`GAME/CORE/BOOTSTRAP_RUNTIME.md`
- synchronize ruleset-set digest wording from SIRR repair;
- generated physical root examples may add existing `SESSIONS/`;
- do **not** claim `STORY/` or Story files are mandatory blank-scaffold output;
- existing campaign path resolution recognizes MANIFEST `story_root` when/if Story is later consumed.

`GAME/CORE/CAMPAIGN_SETUP.md`
- replace stale manifest schema wording with current post-cutover local schema `5`;
- initial MANIFEST description names all seven static selectors;
- generated physical root list includes the actually materialized blank-template roots such as `SESSIONS/`, but does not require `STORY/`;
- explicitly preserve: no Story/T0 file is a first-play/PLAY_READY prerequisite.

`GAME/INSTALL/00_DND_BOOTSTRAP.md`
- generated blank-root example adds current physical `SESSIONS/` where the template includes it;
- does not require `STORY/` physical materialization at New Game;
- exact MANIFEST selector validation still requires `story_root: STORY` after schema cutover.

`GAME/TOOLS/init_campaign.py`
- remains `PROTECT_CURRENT_CONFORMING` for generic template copy and ruleset-set propagation unless fresh implementation evidence changes its body;
- must not synthesize Story files merely to satisfy `story_root`.

Future module/revision consequences from the first self-review remain one logical increment per materially edited shipped file:
```text
BOOTSTRAP_RUNTIME.md 0.8.8 -> 1.0.9
CAMPAIGN_SETUP.md    1.0.3 -> 1.0.4
00_DND_BOOTSTRAP.md launcher_revision 19 -> 20
```
No second increment is added for this correction because these ASR-001/ASR-005 changes belong to the same future implementation edit per file.

### B5. RD-14 focused tests — corrected set

Add/retain:
```text
GeneratorConsumerProjectionTests.test_manifest_has_all_seven_static_root_selectors
GeneratorConsumerProjectionTests.test_sessions_root_exists_in_blank_generated_scaffold
GeneratorConsumerProjectionTests.test_story_root_selector_does_not_require_story_files_at_bootstrap
GeneratorConsumerProjectionTests.test_blank_scaffold_can_be_playable_without_story_projection_state
GeneratorConsumerProjectionTests.test_current_manifest_schema_is_5
GeneratorConsumerProjectionTests.test_ruleset_set_digest_reaches_manifest
```

Remove/supersede any test from the first self-review addendum that requires physical `STORY/**` to survive blank scaffold generation.

### B6. Scheduling correction

Delete/supersede the first self-review `ROOT_SELECTOR_CUTOVER` requirement that made RD-04 selector/schema completion wait for RD-13 physical Story realization.

Correct edge semantics:

```text
RD-04 WP-11 selector/schema owner
  -> independently produces static story_root/sessions_root contract

RD-13 Story owner
  consumes story_root when Story materializes

RD-14 bootstrap/product
  consumes the selector/schema contract for generated MANIFEST validation
  but does not wait for Story materialization

R018 package integration
  joins RD-04 ROUTE/ROOT + RD-13 STORY behavior later
```

This is owner consumption + later composite integration, not a shared-file semantic prerequisite between RD-04 and RD-13.

---

## C. Reverse coverage after ASR-004/005

```text
R064 -> RD-04 seven static selectors + manifest schema + STORAGE projection
R018.ROUTE/ROOT -> RD-04 static route contract
R016.STORY -> RD-13 exact Story physical/lifecycle projection behavior
R018.STORY -> RD-13 exact Story route/body/load behavior consuming RD-04 selector
R030/R086 -> RD-14 generated MANIFEST/bootstrap consumer validation without Story startup prerequisite
R087/T0 -> remains conditional; no startup activation
```

No new readiness identity is created. No trigger-gated/no-work item is activated.

## D. Author third-pass checklist

Before independent re-review #2 the author must fresh-check the published repair SHA and prove:

```text
[ ] all seven MANIFEST selectors are owner-correct and no physical Story file is required by selector validity
[ ] exact Story projection-state path matches WP-11/WP-18
[ ] exact Story unit bucket/path matches WP-11/WP-18
[ ] Story layer-local sequence has no chronology meaning
[ ] RD-14 preserves no-Story/T0 bootstrap prerequisite
[ ] SESSIONS physical-root documentation is synchronized without inventing Story scaffold
[ ] first self-review artificial ROOT_SELECTOR_CUTOVER is explicitly superseded
[ ] ASR-001..ASR-005 have no remaining conflicting current route
[ ] current package index/brief route every overlay in precedence order
[ ] exact-head hosted maintenance audit and DEV unit tests pass
```

Until a third-pass closure records this with no open author finding, independent re-review #2 is not authorized.
