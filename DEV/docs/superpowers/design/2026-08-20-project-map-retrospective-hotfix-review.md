# HDM Project-Map Retrospective Hot-Fix Review

Status: **BOUNDED RETROSPECTIVE AUDIT — CLOSED**

Date: 2026-08-20

Scope: Steps 1 through 5.1, reviewed after introducing `DEV/PROJECT_MAP.md` and the repository-discovery discipline. Step 5.2 remains paused and was not started by this review.

## 1. Purpose

This review asks two bounded questions:

1. If the repository navigation/dependency map had existed earlier, what would materially have changed in the development process?
2. Do the already-closed Steps 1–5.1 contain obvious active-surface drift that can be corrected without reopening accepted architectural decisions?

This is not a redesign of Steps 1–5.1. Accepted ownership, product semantics and architecture decisions remain closed unless a genuine contradiction is discovered.

## 2. Counterfactual process finding

The principal benefit of an earlier project map would have been **better evidence coverage and dependency discovery**, not a different architectural philosophy.

The earlier process often began from the known/current design artifact plus remembered neighboring files and targeted searches. With the current discipline it would instead begin:

```text
current ref/tree
    -> project responsibility/dependency map
    -> actual owning contracts/schemas/tests
    -> symbol/path search for consumers and stale references
```

That structural pass would have made missed neighboring consumers substantially less likely.

## 3. What would likely have changed by stage

### Steps 1–2

The catalog/mechanical conclusions remain supported. An earlier map would mainly have made the assurance pass more systematic by forcing the catalog, machine schemas, runtime CORE consumers and tests into one initial dependency set rather than discovering some relationships incrementally.

No retrospective evidence requires reopening the accepted Resource, HP/LifeState, Effect, Condition, TemporalBinding, recovery, selector or query ownership decisions.

### Step 3

The recommended/accepted Alternative C remains supported. The main process improvement would have been to include recovery/session/randomness/support consumers in the first repository-surface map around Continuation/Procedure/Resolution rather than relying primarily on execution-model files and later recovery carry-forward checks.

No retrospective evidence requires changing the Step-3 execution boundary or owner model.

### Step 4

A structural retirement sweep would have followed Chapter/Secret retirement through runtime support and campaign-template surfaces as well as the primary catalog/schema surfaces. That would likely have caught the stale maintenance-command `chapter entry` wording and the orphan `INDEX/SECRET_INDEX.yaml` immediately.

The truth / fictional knowledge / disclosure / Story architecture itself remains unchanged.

### Step 5.0

This is the stage most directly affected. The contamination audit correctly retired independent Secret authority, but the campaign-template index family was not completely traversed. `GAME/CAMPAIGN/INDEX/SECRET_INDEX.yaml` survived and therefore continued to be copied by the generic campaign scaffold generator.

With the current project-map discipline, `GAME/CAMPAIGN/` plus all template/index/schema/generator neighbors are an explicit campaign-creation dependency route; the orphan would have been visible during the original cleanup.

### Step 5.1

B-NARROW remains supported. A dependency-first pass would have included `SESSION.md`, `STORAGE.md` and the internal maintenance contract among the consumers of the pointer/descriptor/frontier terminology. Their stale checkpoint wording would therefore likely have been aligned during 5.1 instead of after it.

The same support-contract review would also have exposed the unrelated stale native-Git transport proposal while reconnect/recovery semantics were being examined.

### Before Step 5.2

`MAINTENANCE_COMMANDS.md` would have been found from the support/recovery dependency route without requiring the project owner to point to it manually. Its diagnostic/export/reset commands would therefore have entered the 5.2 framing inputs from the start.

## 4. Hot fixes applied

### HF-1 — remove orphan Secret template index

Removed:

```text
GAME/CAMPAIGN/INDEX/SECRET_INDEX.yaml
```

Reason: independent generic Secret authority was retired in Step 5.0. The orphan routing index had no surviving entity family and was still emitted into every new campaign because `init_campaign.py` copies the campaign template tree generically.

This is cleanup of an already-decided retirement, not a new Step-4/5 semantic decision.

### HF-2 — align checkpoint terminology with Step 5.1

Updated:

- `GAME/CORE/SESSION.md`
- `GAME/CORE/STORAGE.md`
- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`

Current distinction is explicit:

```text
MANIFEST.last_checkpoint_id
    -> pointer

checkpoint
    -> sparse recovery descriptor / evidence

recovery boundary/frontier
    -> semantic boundary described by applicable recovery evidence
```

No final Step-5.7 checkpoint representation or hydration protocol was selected.

### HF-3 — remove stale native-Git maintenance transport model

`MAINTENANCE_COMMANDS.md` no longer defines:

```text
runtime.session.transport_mode
native_git
connector_fallback
native-Git probe-first behavior
```

Maintenance commands now use the selected/authorized GitHub Connector path and the applicable current storage/persistence contract. Diagnostic exports may report observable Connector operation/provenance/error evidence without creating a second transport authority.

This aligns the internal support proposal with current runtime transport policy and the active session schema.

### HF-4 — remove retired Chapter wording from maintenance routing

The maintenance routing invariant no longer names a `chapter entry` as a runtime artifact. Chapter world/runtime authority was retired in Step 4; literary grouping remains a Story concern.

### HF-5 — narrow turn-counter wording

The maintenance proposal previously said:

```text
Runtime state stores one counter only
```

That statement became false after the accepted runtime architecture. It now explicitly describes only maintenance-command **turn-number bookkeeping** and does not claim that runtime state lacks other counters, revisions, execution owners or recovery state.

The eventual owner/durability semantics of turn-number continuity remain available for the appropriate Step-5 research rather than being silently decided here.

## 5. Deliberate non-fixes

The review did **not** mechanically rewrite every historical occurrence of retired terminology.

In particular:

- dated research/proposal artifacts remain provenance unless they incorrectly claim current authority;
- `CATALOG_MODEL.md` and `MECHANICAL_RUNTIME_PROPOSAL.md` remain explicitly historical/derivation material;
- deferred Step-4 machine realization (including normalized truth/knowledge/disclosure machine surfaces) remains deferred as already recorded;
- `checkpoint.valid_through_event_id` remains a Step-5.7 question;
- final Resumable Runtime Closure, temporal pending-work continuity, publication, live recovery and chronology representation were not designed here.

The map is a navigation aid, not a reason to perform broad opportunistic refactoring.

## 6. TDD / verification evidence

A focused regression suite was added:

`DEV/TESTS/test_project_map_retrospective_hotfixes.py`

RED run:

- maintenance audit passed;
- DEV suite ran 174 tests;
- exactly the five new retrospective tests failed;
- failures corresponded to the orphan Secret index, checkpoint terminology, stale maintenance transport, retired Chapter wording and over-broad turn-counter claim.

After the minimal hot fixes, the same validation workflow passed maintenance audit and the full DEV unit suite.

## 7. Architectural disposition

No accepted architectural decision from Steps 1–5.1 is reopened by this audit.

The retrospective result is:

```text
core architecture decisions     unchanged
repository discovery discipline strengthened
missed active-surface drift      repaired
new architecture trade-off      none
Step 5.2                         paused / not started
```

The strongest lesson is procedural: repository research must establish the relevant structural and dependency surface **before** treating targeted search results as adequate coverage.
