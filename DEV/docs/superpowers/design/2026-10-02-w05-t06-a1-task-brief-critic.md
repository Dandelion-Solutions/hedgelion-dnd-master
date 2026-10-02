# W05.T06-A1 — Whole-Project Task-Brief Critic

Status: **STEP-1 CRITIC COMPLETE / FRAMING FINDINGS RESOLVED / REVIEW STOP 1 CANDIDATE**

Reviewed source basis: `5b7db90a36f9d5771c392f2e5119fbcd29893c03`

Task Brief: `DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-architecture-task-brief.md`

Source Manifest: `DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-source-manifest.md`

This was a distinct read-only whole-project critic pass. The critic reconstructed the dependency routes through `DEV/PROJECT_MAP.md` and read actual owners/consumers rather than treating the draft Manifest as a completeness proof. This record does not grant GO, start Step 2, or authorize implementation.

## 1. Independently reconstructed routes and owners

### Readiness/current-state route

```text
CHARACTER_READINESS + DIEGETIC_ONBOARDING + WP-19
  -> S6D-07 character progression/READY_PC seed and exact current ruleset identity
  -> Actor / PLAYER / Asset / Effect / MechanicalContext / selectors / Activity primitives
  -> Step-5.1 current composed owner view
  -> WP-12 local HOT owner establishment/currentness
  -> WP-14 exact current-source recovery/rebuild after resume
  -> WP-13 durability + PLAY_READY boundary
  -> RuntimeHost / TurnRuntime consumer composition and current T06 code/tests
```

### Ordinary Master retrospective route

```text
PO-001 / WP-19 / PO-003
  -> Step-4 truth, knowledge, disclosure, roles, Story boundaries
  -> R2.1 continuity/history and R2.3 / WP-09 bounded candidate/profile rules
  -> R2.4 single-context phase rebinding / typed handoff
  -> WP-10 SemanticEvent family + WP-11 native routes/indexes
  -> WP-15 chronology / WP-16 selected LIVE and PLAYER currentness
  -> WP-18 Story / Chronicler consumer boundaries + PO-009 / PO-012 Commentator-only amendments
  -> WP-24 bounded operation and Class A/B/C performance evidence
  -> RuntimeHost History + Context Runtime + Story/Commentator code and RD11/RD13/RD14 tests
```

The critic also checked `DEV/PRODUCT_OWNER_INPUT.md` active routing and the exact PO-001/002/003/009/011/012 entries, current progress, T06 ruling/plan/cursor, and the versioning owner.

## 2. Findings and dispositions

### F-A1-01 — SIGNIFICANT — missing current-view/recovery and exact mechanical-input owners

**Finding.** The first draft did not list the canonical WP-12 HOT and WP-14 recovery specifications or the exact `MECHANICAL_CONTEXT.md`, `CALCULATION_SELECTOR_METADATA.md`, and `ACTIVITY_PRIMITIVE_CONTRACTS.md` owners/tests. These sources constrain whether a local HOT row is current, how a selected LIVE source remains non-current before CAS, how cold recovery selects/rebuilds current owners, and which mechanical read capabilities are actually admitted.

**Independent evidence.** WP-12 Laws 1–8, 13–18 and 22–27; WP-14 Laws 1–13 and 21–24; MechanicalContext §§2–9; selector metadata §§2–7; primitive contract §§1–6. `recovery.py::recover_current_runtime` ignores `hot_state`, returns `hot_authoritative=false`, and rebuilds current sources. `NativeHotStore` has no GAME runtime call site. Exact selector/primitive tests enforce closed active sets, ENGINE_STATE-only inputs and pinned view identity.

**Disposition.** ACCEPTED / REPAIRED. The Source Manifest now includes WP-12, WP-14, S6D-03/04/06, their relevant test suites, and the Brief’s dependency route and questions explicitly preserve those contracts. The frame identifies the missing runtime composition boundary without assuming HOT is already wired or authorizing a new selector/primitive.

### F-A1-02 — SIGNIFICANT — Commentator-only PO-012 test leaked into ordinary Master criteria

**Finding.** A draft ordinary-Master acceptance line demanded “no multi-PC union leakage.” The exact `PUBLIC + PLAYER disclosure + at-most-one selected controlled PC` rule belongs to baseline Commentator under PO-009/PO-012, not ordinary active-player Master retrospective.

**Independent evidence.** PO-012 §§1, 5, 8 and the T06 plan’s explicit separation of ordinary Master and Commentator paths. WP-19 L20–L23 defines the Master consumer using its own current eligibility contract.

**Disposition.** ACCEPTED / REPAIRED. The ordinary Master test scope now covers its accepted native/player/recipient eligibility without importing PO-012’s formula. The brief explicitly routes multi-PC-union coverage to the separate Commentator regression surface.

### F-A1-03 — SIGNIFICANT — historical query examples needed explicit retention/exactness bounds

**Finding.** PO-001/WP-19's example questions could be read as guaranteeing exact or exhaustive answers for every historical query, even after owner-lawful compaction or when the native source never retained the requested fact. That would expand product retention and query promises.

**Independent evidence.** PO-001 authorizes natural-language retrospective over available admitted history/continuity and forbids disclosure leakage. WP-19 L36–L37 requires bounded retrieval and says insufficient evidence stays insufficient. R2.1 Laws 2, 5, 9, 11 and 13 distinguish current/native evidence, derived orientation and selective exact recall. Step 5.11 Laws 1 and 5 say semantic continuity is not a universal verbatim archive and prohibit exact claims without exact evidence. WP-15 §7 Laws WP15-34/35 explicitly state that there is no guarantee of indefinite retention of every old event/detail or arbitrary historical pair query, and that an unpromised query may remain `INDETERMINATE`/unavailable after lawful compaction.

**Disposition.** ACCEPTED / REPAIRED. The Brief now states that the PO-001/WP-19 examples are supported consumer requirements over available admitted evidence, not a universal exact-quotation or unbounded-query guarantee. It requires the strongest supported semantic account or a truthful insufficiency result when the necessary evidence is unavailable, without narrowing supported PO-001 behavior or adding a new retention rule.

### F-A1-04 — MINOR — S6D-07 exact evidence identity fields were too generic

**Finding.** “Exact package/catalog identity” could leave room to revive superseded digest terminology.

**Independent evidence.** `CHARACTER_PROGRESSION_READY_PC_SEED.md` and its machine/conformance consumer use Actor identity/revision, catalog generation, and typed resolved ruleset-set digest generation/hash.

**Disposition.** ACCEPTED / REPAIRED. Both Brief and Manifest name `actor_id`, `actor_state_revision`, `catalog_generation`, `ruleset_set_digest_generation`, and `ruleset_set_sha256`.

### F-A1-05 — MINOR — settled loss/index/Story outcomes were partly phrased as open design questions

**Finding.** The source set already settles that lost unpublished HOT is not reconstructed, missing/incomplete indexes do not prove semantic absence or authorize scans, and Story is optional subject to an explicit revisit trigger. Those settled outcomes must be framing constraints, not reopen questions.

**Independent evidence.** Step-5.1, WP-12, WP-14, WP-11, WP-15, WP-19, the System-Impact Senior ruling and WP-24.

**Disposition.** ACCEPTED / REPAIRED. The Brief now treats HOT loss recovery and incomplete-index behavior as settled laws; open questions concern current-view acquisition while evidence exists, the exact complete-empty Event-index source, and whether the already accepted Story revisit trigger is met. Story is not presumed necessary.

## 3. Reconciled owner/open-issue matrix

| Concern | Already settled by accepted owner | Still genuinely open for A1 research |
|---|---|---|
| READY_PC meaning and local sufficiency | `CHARACTER_READINESS.md`, S6D-07 and WP-19; same Actor, no situational retrofit, not a begin-play gate | Runtime current-owner view, owner-issued assessment route, exact blocker outputs, re-evaluation after fresh recovery/rejoin, and integration to existing launch durability |
| HOT/recovery | Step-5.1/WP-12/WP-14; current owner composition is domain-specific; local bytes are not independent authority; lost unpublished HOT is not reconstructed | How accepted HOT/SOFT reaches a trusted assessment while it remains current, given actual code composition |
| Mechanical evidence | S6D-03/04/06 and package identity owners; exact closed selector/accessor/primitive admissions and typed failure semantics | Which existing evidence route can compose required owners without adding authority or capability |
| Ordinary Master product behavior | PO-001/WP-19/PO-003; normal gameplay, bounded/native evidence, current eligibility, no T1-as-T0, no invention on insufficiency | Registered profile/candidate discovery implementation boundary and testable exact evidence route |
| Context/history | R2.3/WP-09 and native History; finite profile/closure, terminal failures, exact pinned ordinal/origin windows | Semantic query nomination and minimum bounded lookup across NPC/place/thread/session/event cases |
| Story/Commentator | Story remains noncanonical/optional for Master; PO-009/PO-012 are Commentator-specific; explicit Story revisit trigger already exists | Whether current native/index route satisfies the revisit trigger; if not, narrow nomination-only hint adapter design |
| Retention/exactness | R2.1, Step 5.11, WP-19 and WP-15; semantic continuity is distinct from exact transcript, no arbitrary historical query guarantee | Map each supported question/evidence class to current retained owners and truthful missing-evidence behavior |
| Performance | WP-19 capture law is scoped to capture; WP-24 admits no universal SLA and separates structural/class-B/class-C evidence | Bounded source fan-out and later required realized/supported-target measurements after implementation is authorized |

No current owner asks A1 to decide a new product policy. Any material architecture trade-off discovered in Step 2–7 remains subject to the existing decision-rights process.

## 4. Final critic gate

```text
CRITIC_SCOPE: WHOLE-PROJECT / PROJECT-MAP RECONSTRUCTED
BLOCKING: 0
SIGNIFICANT: 3 FOUND / 3 REPAIRED
MINOR: 2 FOUND / 2 REPAIRED
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
PRODUCT_OWNER_DECISION_REQUIRED_AT_ENTRY: NO
SENIOR_GO: NOT GRANTED BY CRITIC
NEXT: MANDATORY ARCHITECTURE REVIEW STOP 1
STEP_2_STARTED: NO
PRODUCTION_IMPLEMENTATION: HELD
VERSION_IMPACT: NONE — design evidence/Task Brief/critic/cursor only
```

The Step-1 package is ready to return for Review Stop 1. This critic does not grant Senior GO. Step 2 and production implementation remain unauthorized until the mandatory review receives GO.
