# S6D-02 — Catalog Admission and Gap Closure — Whole-Project Brief Critic

Status: **CRITIQUE COMPLETE — PASS AFTER REPAIR**

Date: 2026-08-25

Reviewed ref: `v1/engine-rearchitecture@eee4683b2b270a555105c19fc293d2bf4467530d`

Reviewed artifact: draft `2026-08-25-s6d-02-catalog-admission-gap-closure-task-brief.md`

Reviewer stance: independent Step-1 whole-project critic under `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

No Step-2 research, catalog decision, file edit or publication was performed by the critic.

---

## 1. Whole-project routes checked

The critic reconstructed the dependency subgraph from current remote sources rather than accepting the draft's source list as complete:

- bootstrap/process: `AGENTS.md` -> `DEV/DESIGN_PROCESS.md` -> `DEV/ARCHITECTURE/DESIGN_PROCESS.md` -> `DEV/PROJECT_MAP.md` -> `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- S6D sequencing decision, owner decision and parent task brief;
- S6D-01 canonical `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`;
- catalog owners: `CATALOG_CONTRACTS.md`, `CATALOG_INVENTORY.md`, `CATALOG_RESOLUTION.md`, `CATALOG_MODEL.md`;
- machine catalogs: `core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, `mechanical-surfaces.json`;
- Step-1 catalog meta-model resolution and Steps-1/2 retrospective assurance;
- Activity/Rule Element owners;
- Step-3 execution canonical owner and catalog tests;
- current House Rules owner;
- R2.7 durable cursor and accepted Round-2 ownership;
- engine/rules baseline metadata;
- runtime `MECHANICS_INTEGRITY.md`, `ADJUDICATION.md`, `GAME/RULES/README.md`;
- focused searches for registry consumers, removed IDs, gap reports, selectors and primitives, followed by ref-pinned owner reads.

---

## 2. Findings

### BC-01 — Admission was conflated with full realization

Severity: **BLOCKING**

The draft required every ID to finish S6D-02 as “supported and realized,” while explicitly assigning selector metadata to S6D-03, accessor/dependency metadata to S6D-04, value contracts to S6D-05, primitive contracts to S6D-06 and supported seed/domain proof to S6D-07–09.

Current evidence makes the contradiction concrete: the catalog registers substantially more selectors than `mechanical-surfaces.json` currently describes, and many `op.*` primitives do not receive exact contracts until S6D-06. An ID can therefore be validly admitted for the supported profile while still having an explicit downstream realization obligation.

Required repair:

- use one axis for S6D-02 admission: `ACTIVE_ADMITTED`, `EMBEDDED_NONOWNER`, `DORMANT_NONSELECTABLE(trigger)`, `STALE_REMOVE`;
- use a separate axis for realization: `COMPLETE` or exact downstream owner plus missing contract;
- state that S6D-02 proves admission and destination, not downstream completeness;
- require integrated S6D closure to complete or remove every active entry.

Risk if unfixed: false S6D-02 closure, deletion of valid IDs, or scope theft from S6D-03–11.

### BC-02 — Accepted catalog class boundaries were framed as open alternatives

Severity: **SIGNIFICANT**

The draft treated definition/world/runtime/value boundaries and a minimal direct-flow catalog as peer alternatives. Current canonical owners already settle the minimum-sufficient class model and Catalog 2.0 class-admission semantics. Later work may change an individual entry only on concrete contradictory evidence, an unsatisfied consumer or an explicit superseding decision.

Required repair:

- inherit the accepted class model as an invariant;
- recast boundary checks as challenge hypotheses against concrete entries;
- remove wholesale minimal direct-flow replacement as a peer alternative unless evidence first proves accepted architecture insufficient.

Risk if unfixed: unnecessary reopening of Steps 1–2 and accidental loss of indirect recovery/collaboration/package owners.

### BC-03 — The registry scope could pull closed Round-2 work into S6D

Severity: **SIGNIFICANT**

The parent S6D-02 scope emphasizes definition/world/runtime/value/selector/accessor/operation IDs. The shared catalog also contains role/context/collaboration/Story/chronology/durability vocabularies whose semantic admission is already owned by accepted Round-2 architecture and whose physical realization belongs to paused later R2.7 work.

Required repair: stratify the census:

1. S6D-primary families receive full admission decisions;
2. cross-surface referenced engine enums/policies receive set-equality and stale-reference checks while inheriting current owners;
3. later Round-2 vocabulary receives consistency and named future-WP routing only unless a real contradiction is found.

Risk if unfixed: S6D-02 silently reopens R2.1–R2.6 or starts WP-07+ out of sequence.

### BC-04 — “Real supported consumer” lacked an evidence hierarchy

Severity: **SIGNIFICANT**

`engine_version: 1.0-alpha` and `rules_baseline: D&D 2024 / SRD 5.2.1` do not enumerate the exact supported MVP seed. `GAME/RULES/README.md` also permits bounded local rulings when exact RAW is absent, while S6D-09 owns full mechanics-surface coverage.

Required repair: accept admission evidence in this order:

1. current canonical owner plus active machine/runtime consumer;
2. accepted supported-profile requirement plus exact downstream S6D owner;
3. accepted-work/package/recovery/retention dependency;
4. otherwise owner-approved dormant trigger or stale removal.

Rules-baseline metadata, generic D&D familiarity, prose mention, historical inventory presence or hypothetical later use cannot alone prove active admission.

Risk if unfixed: placeholders survive on vague thematic relevance or valid future seed needs are deleted prematurely.

### BC-05 — Recovery and retention owners were routed too broadly

Severity: **SIGNIFICANT**

The draft mentioned Step-3 and durability/recovery generically, but S6D-01 requires exact accepted Resolution/Continuation ruleset identity and dependency retention, finite failure on missing context and integration with Step-5.13 retention.

Required repair: name and inspect:

- Step-3 execution canonical owner;
- Resolution/Continuation/receipt schemas and tests;
- Step-5.2 resumable-runtime canonical owner;
- Step-5.7 checkpoint canonical owner;
- Step-5.13 cleanup/retention canonical owner and resolution;
- S6D-01 §§6, 8, 10–12.

S6D-02 must preserve IDs/content required by reachable accepted work but must not redesign recovery, checkpoints or garbage collection.

Risk if unfixed: apparently stale vocabulary can be removed while still protected by accepted-work recovery.

### BC-06 — Namespace field was overgeneralized

Severity: **MINOR**

Package namespace claims apply to reusable definition content. Engine capability/protocol IDs remain closed engine-owned vocabulary; world/runtime instance identities are not package namespace claims.

Required repair: use `identity/namespace owner (N/A with reason where not package-scoped)`.

### BC-07 — Step-1 exit and domain closure were mixed

Severity: **MINOR**

The draft placed the complete census, set equality and every-ID disposition beside the instruction to stop before Step 2.

Required repair: separate Step-1 exit criteria from full S6D-02 loop exit criteria.

---

## 3. Critic verdict before repair

**NOT READY FOR STEP 2.**

BC-01 blocks execution. BC-02 through BC-05 are significant framing/ownership gaps. Step 2 must not begin until they are repaired. BC-06 and BC-07 should be repaired in the same pass.

The repair must not perform the census, decide individual ID dispositions, remove IDs, alter catalogs/schemas/tests, build package content or prove S6D-09 coverage. Those are later-step activities.

---

## 4. Resolution record

The final brief repair addresses the findings as follows:

| Finding | Resolution |
|---|---|
| BC-01 | Separate admission and realization axes added throughout problem, ledger and exits. |
| BC-02 | Accepted class model made inherited invariant; alternatives/questions narrowed to evidence-triggered challenge. |
| BC-03 | Three registry census strata added; later Round-2 ownership and sequencing preserved. |
| BC-04 | Explicit admission-evidence hierarchy and forbidden weak evidence added; S6D-09 boundary preserved. |
| BC-05 | Exact Step-3/Step-5.2/5.7/5.13/S6D-01 routes and narrow retention duty added. |
| BC-06 | Ledger field corrected to identity/namespace owner with scoped applicability. |
| BC-07 | Step-1 and full-loop exit criteria separated. |

Final post-repair verdict is recorded after the independent re-review.


## 5. Post-repair re-review

The first repair pass resolved BC-01 through BC-07 but left one significant qualification: it required integrated S6D to complete or remove inherited Round-2 vocabulary whose realization intentionally belongs to paused WP-07+.

The brief was corrected again:

- `COMPLETE-or-remove` applies only to S6D-primary active IDs and residual Step-6 obligations;
- inherited Round-2 vocabulary terminates S6D-02 as `INHERITED_ACTIVE` with exact accepted R2.x/WP owner, consistency checked and no S6D realization obligation;
- an inherited item enters S6D-primary scope only on concrete contradiction or an unsatisfied S6D consumer;
- zero-unclassified coverage means every ID has a census stratum plus its stratum-appropriate disposition.

Final verdict: **PASS — zero unresolved BLOCKING or SIGNIFICANT findings.**

Step 2 remains not started.
