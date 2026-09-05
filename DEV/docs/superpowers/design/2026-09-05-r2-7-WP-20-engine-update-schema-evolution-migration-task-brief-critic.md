# R2.7 WP-20 Step 1 — Whole-Project Task-Brief Critic

Status: **COMPLETE — ALL BLOCKING/SIGNIFICANT FRAMING FINDINGS REPAIRED / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

Reviewed brief:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-architecture-task-brief.md`

Source Manifest:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-20-source-manifest.md`

## 1. Critic method and independently reconstructed dependency graph

The critic did not restrict itself to the draft Brief or `GAME/MIGRATIONS/`.

It reconstructed the WP-20 dependency subgraph from `DEV/PROJECT_MAP.md` and checked actual current owners/consumers along these routes:

```text
PO-004 clean-slate authority
    -> R2.7 WP-20 scope

WP-19 creation/runtime identity
    -> MANIFEST engine/ruleset created/current
    -> ENGINE_UPDATES / package provenance
    -> ruleset package identity/compatibility

engine/ruleset update
    -> release/version metadata
    -> RUNTIME_PACKAGE / exact ZIP provenance
    -> persistent campaign/storage schema identities
    -> MIGRATIONS scaffold

migration publication
    -> WP-13 / PERSISTENCE pinned-head base-tree non-force publication
    -> failure epistemics / indeterminate authority

migration recovery
    -> WP-14 current-source recovery / checkpoint nonauthority
    -> WP-12 HOT/SQLite derived-state boundary
    -> accepted execution interpretation continuity

semantic preservation
    -> stable native owners/IDs
    -> WP-15 chronology/history
    -> ruleset exact interpretation context

multiplayer/live migration
    -> ACCESS_CONTROL
    -> WP-16 campaign/LIVE/HOT currentness
    -> exact-source LIVE authority/CAS

machine reverse audit
    -> bootstrap/update prose
    -> MANIFEST/DND_STORAGE schemas
    -> release builder/version files
    -> migration scaffold
    -> update/release/persistence/live tests
    -> audit/release consumers
```

WP-21+ were considered only as downstream constraints; they were not started.

## 2. Existing-owner / reopen check

The critic found no basis to reopen WP-19. Its creation-side exact identity and first-publication boundary are accepted and sufficient as input to WP-20.

The critic also found several responsibilities already settled upstream and therefore not open WP-20 choices by default:

- storage baseline is NEW-campaign-only;
- existing campaign runtime authority is `MANIFEST.engine.current`;
- exact package provenance cannot be inferred from mutable tag/main;
- engine/ruleset identity axes are distinct;
- same-version compatible forward refresh already has accepted narrow rules;
- ordinary existing-campaign publication is base-tree/pinned-HEAD/non-force;
- checkpoint is not current authority or guaranteed rollback slot;
- HOT/SQLite and indexes are derived/non-authoritative;
- campaign/LIVE/HOT currentness dimensions are distinct;
- accepted execution cannot be replayed/rerolled merely because representation changes.

WP-20 must conform to these unless later Step-2 evidence proves a genuine insufficiency requiring an explicit superseding decision.

## 3. Findings and repairs

### F20-S1-01 — SIGNIFICANT — pre-release compatibility could be accidentally resurrected

**Failure mode:** legacy bootstrap paths, old 0.8 design examples, migration scaffold or U17 legacy-layout test could be treated as compatibility requirements merely because they are tracked.

**Evidence:** PO-004 explicitly removes all pre-release compatibility obligations and structural freeze.

**Repair:** Brief section 2 now makes the compatibility horizon explicit and requires all legacy/pre-release machine artifacts to be classified, not preserved by default.

**Disposition:** `CLOSED`.

---

### F20-S1-02 — SIGNIFICANT — hidden single-axis assumption around semantic `engine_version`

**Failure mode:** a runtime with a “compatible” engine version could still carry incompatible ruleset set, schema/format, or accepted-open-work interpretation semantics.

**Evidence:** ruleset package identity explicitly separates engine, package, ruleset and catalog axes; MANIFEST separately stores engine/ruleset identity; release policy says schema/format revisions are independent.

**Repair:** Brief Q20-01..Q20-03 require a minimum sufficient multi-axis compatibility envelope and prohibit a universal version scalar without evidence.

**Disposition:** `CLOSED`.

---

### F20-S1-03 — SIGNIFICANT — migration path could be selected from mutable tag/current `main`/“latest”

**Failure mode:** a historical campaign or migration edge is reclassified after a tag moves or current repository state changes; path selection becomes non-reproducible.

**Evidence:** exact runtime package provenance owner already rejects mutable-tag inference for candidate bytes.

**Repair:** Q20-04 requires immutable source/target predicates, migration implementation identity/provenance, deterministic edge ordering and explicit ambiguity/gap/cycle behavior. Mutable tags/main/latest are named invalid selectors.

**Disposition:** `CLOSED`.

---

### F20-S1-04 — SIGNIFICANT — local transformation could be confused with authoritative migration success

**Failure mode:** migration writes target-form local bytes, publication rejects or becomes indeterminate, yet runtime adopts/announces target identity or retries blindly.

**Evidence:** WP-13 owns immutable publication attempts and tri-state final ref epistemics; existing PERSISTENCE requires pinned-head, base-tree, non-force CAS.

**Repair:** Q20-08..Q20-10 explicitly separate local transform from authority-changing publication, require rejection/indeterminate semantics and prohibit blind retry/force/alternate publication authority.

**Disposition:** `CLOSED`.

---

### F20-S1-05 — SIGNIFICANT — active multiplayer/LIVE state was not sufficiently part of migration framing

**Failure mode:** campaign migration transforms campaign-base copies while selected LIVE remains current authority for some owners, losing shared mutations or creating duplicate truth.

**Evidence:** WP-16 makes campaign/LIVE/HOT currentness separate and preserves ACTIVE/CLOSED-unabsorbed LIVE truth with exact-source CAS.

**Repair:** Q20-11 and inherited constraints require explicit LIVE routing/claim/quiescence/absorption/blocking analysis and prohibit campaign fallback over live-owned truth.

**Disposition:** `CLOSED`.

---

### F20-S1-06 — SIGNIFICANT — rollback/checkpoint language could embed an unsupported promise

**Failure mode:** `GAME/MIGRATIONS/README.md` says each migration should define rollback/checkpoint requirement; a design could infer that every migration must be reversible or that checkpoint guarantees rewind.

**Evidence:** WP-14 states checkpoint is optional non-authoritative evidence and not a guaranteed rewind slot.

**Repair:** Brief Q20-14 decomposes abort/rejection/indeterminate/reverse-migration cases and requires evidence for any real rollback promise. The migration README is classified as scaffold, not owner.

**Disposition:** `CLOSED`.

---

### F20-S1-07 — SIGNIFICANT — stable identity/history/currentness preservation was too implicit

**Failure mode:** a schema migration regenerates IDs, rebinds accepted open work to newer mechanics, rebuilds chronology from storage order, or loses recovery/currentness evidence while preserving superficially similar data.

**Evidence:** WP-12 stable native identity/open-work interpretation; WP-14 no replay; WP-15 native chronology; ruleset exact-set interpretation.

**Repair:** Brief Q20-06 enumerates semantic invariants and Step-2 requires owner-family/path/schema mapping rather than file-only transformation analysis.

**Disposition:** `CLOSED`.

---

### F20-S1-08 — SIGNIFICANT — update authorization source graph contains unresolved wording tension

**Failure mode:** migration is silently treated as storage-owner maintenance, campaign-creator adoption, or ordinary PLAYER mutation depending on which paragraph a worker reads.

**Evidence:** `ACCESS_CONTROL.md` includes a broad “campaign engine maintenance is storage-owner maintenance” sentence while later owner-only operation wording and `ENGINE_UPDATES.md` identify creator-controlled explicit engine/ruleset adoption; storage baseline itself is separately storage-owner-only and NEW-only.

**Repair:** Q20-07 makes this an explicit existing-owner reconciliation task. Step 2 must separate storage baseline maintenance from existing-campaign mutation and derive authority from current accepted owners.

**Human decision:** not yet required. The conflict is first a repository-owner reconciliation question. Escalation is warranted only if Step-2 evidence leaves genuinely reasonable product/authority alternatives after accepted-owner reconciliation.

**Disposition:** `CLOSED AS FRAMING DEFECT`.

---

### F20-S1-09 — SIGNIFICANT — current scaffold/tests could be treated as architecture authority

**Failure mode:** tests and legacy paths constrain final architecture, including old UI vocabulary, old storage field names and mandatory legacy-layout preservation.

**Evidence:** current `ENGINE_UPDATE_CASES.md` contains stale or superseded details (`U04`, `U06`, `U08`, `U17`), while current owners have moved.

**Repair:** Source Manifest assigns test/scaffold sources `IMPLEMENTATION/TEST` or `SCAFFOLD` roles; Q20-16 requires machine→architecture classification. Existing tests have no correctness presumption.

**Disposition:** `CLOSED`.

---

### F20-S1-10 — SIGNIFICANT — runtime/migration implementation availability and older-runtime rejection were underframed

**Failure mode:** missing exact runtime causes fuzzy substitution; older runtime tolerates unknown newer data; missing migration edge is guessed from nearest versions.

**Evidence:** current bootstrap/update contracts require exact package recovery and forbid silent semantic-version substitution; accepted open work requires exact compatible interpretation context.

**Repair:** Q20-12/Q20-13 require finite unavailable/unsupported outcomes and fail-closed older-runtime behavior, with no main/latest/sibling-runtime borrowing.

**Disposition:** `CLOSED`.

---

### F20-S1-11 — SIGNIFICANT — architecture questions and realization work could be misclassified

**Failure mode A:** compatibility/path/authority/failure semantics are deferred as “implementation details”, leaving no architecture from which safe implementation can follow.

**Failure mode B:** exact Python APIs, DDL or scripts are prematurely frozen as architecture and duplicate current owners.

**Repair:** Q20-17, architecture↔machine audit and hard boundaries now separate required canonical semantics from later WP-22/23/26 and implementation-plan realization.

**Disposition:** `CLOSED`.

## 4. Required assignment-specific challenge checks

| Challenge | Critic result |
|---|---|
| accidental pre-release compatibility resurrection | Prevented by PO-004 hard horizon + reverse-audit classification. |
| semantic engine version treated as complete compatibility | Rejected; multi-axis envelope required. |
| migration selected from mutable tags/current main | Rejected; immutable exact provenance/path identity required. |
| partial/in-place authoritative mutation | Rejected as architecture assumption; final authority must follow existing coherent publication/CAS law. |
| stable identity loss/reassignment | Explicit invariant and failure scenario. |
| history/currentness/recovery evidence loss | Explicit invariant and owner routes included. |
| unsafe active multiplayer/live interaction | Explicit WP-16 route and migration/live questions included. |
| bypass of normal publication/CAS | Explicitly forbidden by inherited WP-13/PERSISTENCE boundary. |
| unsupported rollback promise | Removed; rollback decomposed and evidence-gated. |
| silent forward/backward tolerance | Directionality/older-runtime rejection questions explicit. |
| stale migration/schema/tests treated as authority | Role-classified; reverse audit mandatory. |
| duplicate compatibility/version owners | Minimum sufficient envelope required; no universal duplicate scalar by convenience. |
| architecture deferred as implementation detail | Q20-17 prevents deferral of semantic laws. |
| realization promoted into architecture | Hard boundary retains exact APIs/DDL/scripts for later unless semantically material. |

## 5. Product Owner / human-decision test

No genuine Product Owner decision is required to complete Step 1.

In particular:

- **pre-release compatibility** is already decided by PO-004;
- **forward-only vs another migration direction** is not decided here because Step 2 must first establish which ordering axes and retained artifacts make each policy technically coherent;
- **rollback** is not presented as a product preference before feasibility/authority evidence exists;
- **creator vs storage-owner wording** is first an accepted-owner reconciliation problem, not a new product choice;
- **exact compatibility record shape** is agent-owned technical architecture unless analysis exposes a material product trade-off.

If Step 2 demonstrates that two materially different released-campaign support policies remain reasonable after evidence — for example, a real product choice about the duration/scope of support for released old versions — that future Decision Brief must set `NEEDS_PO`. No such residual decision is established by Step-1 evidence.

## 6. Critic final state

```text
TASK_BRIEF_CRITIC: COMPLETE

BLOCKING_FOUND: 0
SIGNIFICANT_FOUND: 11
MINOR_FOUND: 0

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0

F20-S1-01: CLOSED
F20-S1-02: CLOSED
F20-S1-03: CLOSED
F20-S1-04: CLOSED
F20-S1-05: CLOSED
F20-S1-06: CLOSED
F20-S1-07: CLOSED
F20-S1-08: CLOSED AS FRAMING DEFECT / STEP-2 OWNER RECONCILIATION REQUIRED
F20-S1-09: CLOSED
F20-S1-10: CLOSED
F20-S1-11: CLOSED

HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO

WP20_STEP1: COMPLETE — MANDATORY SENIOR REVIEW
WP20_STEP2_AUTHORIZED: NO
WP20_STEP2_STARTED: NO
WP21_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
RUNTIME_MIGRATION_EXECUTED: NO
REAL_CAMPAIGN_MIGRATED: NO

NEXT_AUTHORIZED_UNIT: NONE — MANDATORY SENIOR REVIEW
```

The package is review-ready. The critic authorizes no Step 2 work; only the mandatory Senior gate can do so.
