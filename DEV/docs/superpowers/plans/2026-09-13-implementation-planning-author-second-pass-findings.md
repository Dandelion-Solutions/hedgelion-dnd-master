# HDM Implementation Planning — Author Second-Pass Findings

Status: **AUTHOR SECOND-PASS SELF-REVIEW — REPAIR REQUIRED BEFORE INDEPENDENT RE-REVIEW #2**
Date: 2026-09-13
Reviewed repair checkpoint: `db23d097abfb9a2cfdbeb88b115689566a575bed`
Production implementation authorized: **NO**.

## 1. Method

The second author pass did not trust the first self-review repair. It fresh-read the published `db23d097...` checkpoint, verified its exact six-file planning-only delta, verified hosted maintenance audit + DEV tests, then re-ran owner and reverse-consumer checks against WP-11, WP-18, WP-19, current RD-13/RD-14 routes and the independent re-review #2 criteria.

The pass also inspected likely neighboring layout consumers (`GAME/CAMPAIGN/README.md`, `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`) rather than assuming every install surface encoded the same root list. Those three do not create an additional root-list repair obligation.

## 2. Result

ASR-001..ASR-003 are directionally repaired, but the second pass found two additional material author defects in the first self-review repair. Therefore no author closure or independent handoff is allowed yet.

### ASR-004 — SIGNIFICANT — RD-13 leaves canonical Story physical routing to worker inference

WP-11 and WP-18 already fix Story physical topology:

```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

with baseline layers:

```text
TRANSCRIPT
EVENTS
MECHANICS
NARRATIVE
```

Current RD-13 Task 4 instead says the layer-local projection-state location is "selected by the existing Story owner/scaffold convention" and lists layer directories without pinning the complete record path/bucket formula in the executable task.

That leaves a worker free to choose a different projection-state filename/location or Story record partitioning even though the canonical owner already decided both. This is a worker design choice and directly affects `R016.STORY` / `R018.STORY` route/body integration.

**Required repair:** the current execution overlay must state the exact WP-11/WP-18 Story path formula, layer set, bucket computation, source of `story_root`, and focused route tests. Story sequence remains layer-local routing/allocator evidence and never fictional chronology.

### ASR-005 — SIGNIFICANT — first self-review repair over-couples static `story_root` selector to bootstrap Story materialization

The first self-review addendum correctly moved MANIFEST selector ownership to WP-11/RD-04, but then incorrectly required a claimed-green selector checkpoint to contain a physically realized Story root/scaffold and made RD-14 expected generated roots include STORY.

This is stronger than the canonical owners and conflicts with WP-19/RD-14 protected behavior:
- `MANIFEST.storage.story_root` is static routing metadata;
- Story is noncanonical derived projection;
- Story/T0 is **not** an unconditional bootstrap/gameplay-start prerequisite;
- a new campaign can be valid/playable before any Story projection has materialized.

A static selector may lawfully name `STORY` before any Story file exists. Physical Story topology becomes real when RD-13 first materializes Story. No Story file or projection-state file is required merely to create the blank campaign.

`SESSIONS/`, by contrast, already exists in the template (`SESSIONS/_TEMPLATE.yaml`) and may be named in generated-root documentation after the selector repair.

**Required repair:**
1. RD-04 fixed-selector/schema cutover must be independently green without Story content files.
2. Remove the artificial RD-04+RD-13 coherent physical-root checkpoint.
3. RD-14 must validate all seven MANIFEST selectors while proving **no Story file/path is required at New Game bootstrap**.
4. Bootstrap/root-list prose may add physically generated `SESSIONS/`; it must not claim STORY is physically generated unless the implementation deliberately adds nonsemantic scaffold bytes under an owner-approved requirement. No such requirement is currently established, so the plan must not add them.
5. RD-13 later consumes `story_root` and materializes exact WP-18 routes on demand.

## 3. Rechecked non-findings

The second pass additionally confirmed:
- `GAME/CAMPAIGN/README.md` does not encode campaign root topology;
- `GAME/INSTALL/README.md` and `PROJECT_INSTRUCTIONS.txt` define package/install/bootstrap entry behavior but do not enumerate the campaign-root set requiring ASR-001 synchronization;
- generic `init_campaign.py` remains suitable for copying the template and does not hard-code Story/SESSIONS root lists;
- local campaign manifest schema `4 -> 5` remains the correct future implementation consequence for adding required `sessions_root` + `story_root` fields;
- clean-slate v1 policy still rejects manufacturing pre-release compatibility migrations solely for the old schema shape;
- `ABSENT | BOUND` Dramaturg repair remains owner-correct;
- WP12/WP13 proof-owner corrections from ASR-003 remain owner-correct;
- no human Product Owner decision or architecture reopen is required.

## 4. Gate

```text
AUTHOR_SECOND_PASS_VERDICT: FAIL / REPAIR REQUIRED
OPEN_AUTHOR_FINDINGS: ASR-004 SIGNIFICANT; ASR-005 SIGNIFICANT
INDEPENDENT_RE_REVIEW_2_READY: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

After ASR-004/005 repair, the author must perform another fresh exact-head pass rather than treating this finding publication as closure.
