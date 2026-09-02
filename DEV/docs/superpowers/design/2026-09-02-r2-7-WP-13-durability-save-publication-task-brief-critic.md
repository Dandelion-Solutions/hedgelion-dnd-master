# R2.7 WP-13 — Durability / SAVE / Publication — Whole-Project Task-Brief Critic

Status: **STEP-1 WHOLE-PROJECT CRITIC COMPLETE — ALL BLOCKING/SIGNIFICANT FRAMING FINDINGS REPAIRED**

Date: 2026-09-02

Reviewed Task Brief:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief.md`

Reviewed Source Manifest:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest.md`

---

## 1. Critic method

This critic does not review WP-13 as an isolated persistence module.

It reconstructed the current dependency subgraph from `DEV/PROJECT_MAP.md` and inspected actual current sources across:

- Step-3 accepted execution/identity/RNG boundaries;
- Step-5.2 native Resumable Runtime Closure;
- Step-5.4 controlled host handoff;
- Step-5.5 SOFT/HARD/SAVE durability semantics;
- Step-5.6 campaign publication/currentness/crash consistency;
- Step-5.7 checkpoint/recovery boundary;
- Step-5.8 live authority/exact-source CAS;
- Step-5.14 integrated concurrency/recovery closure;
- WP-10 native durable record families;
- WP-11 route/index topology and F02 forward obligation;
- closed WP-12 owner-generation/dirty/publication and repaired live-CAS boundary;
- `ACCESS_CONTROL.md`, `BRANCH_MODEL.md` and campaign House-Rules adoption authority;
- current GAME runtime durability/save/publication/session/live/integrity/randomness consumers;
- current campaign/current/session schemas;
- current durability/save/persistence regression suites and the executable hourly-durability contract;
- current maintenance-audit entry point.

The critic asks whether the Step-1 framing could accidentally:

- reopen closed architecture because current code is more concrete;
- turn one campaign commit into a distributed/global SAVE transaction;
- preserve a superseded global one-hour frontier;
- lose a newer local owner generation after an older publication succeeds;
- require broad campaign scans to prove save completeness;
- promote checkpoint, index, SQLite, session metadata or prepared Git objects into authority;
- weaken live exact-source CAS or access-control requirements;
- claim `saved` after partial/ambiguous durability;
- omit an actual named durability-edge owner.

---

## 2. Findings

### C01 — campaign-only SAVE framing cannot represent the accepted multi-native-domain promise

Severity: **BLOCKING**  
Agree: **YES**

Failure mechanism:

Current `GAME/CORE/SAVE_CONTRACT.md` and `DEV/TESTS/EXPLICIT_SAVE_CASES.md` describe explicit save primarily as `SAVE_ALL_DIRTY` and one `CAMPAIGN_TREE_TXN`. If the WP-13 brief copied that concrete shape as the architecture problem, it would contradict Step-5.5/5.6, which allow one explicit SAVE promise to require compatible durability across multiple independent native domains. A live-owned required consequence, for example, cannot become durable merely because a campaign-tree commit succeeds.

Required repair:

- distinguish **campaign-domain transaction** from **overall explicit SAVE composition**;
- preserve one coherent campaign commit for one campaign-domain publication;
- allow overall SAVE to compose campaign/live/other native durability outcomes under their native protocols;
- prohibit a distributed rollback/transaction across those domains;
- acknowledge `saved` only after the full promised closure is confirmed durable;
- treat already-durable native components as satisfied without heartbeat writes.

Propagation:

- Task Brief Goals 3–4, accepted constraints 5.3–5.4, core questions, critical flow 11.4 and scenarios repaired;
- Source Manifest classifies `SAVE_CONTRACT`/explicit-save tests as current partial machine framing rather than semantic authority.

Resolved: **YES**

---

### C02 — current one-hour/global frontier could be accidentally preserved as architecture

Severity: **BLOCKING**  
Agree: **YES**

Failure mechanism:

`DURABILITY_GUARD.md`, `STORAGE.md`, `RUNTIME.md`, `SESSION.md` and `test_hourly_durability_contract.py` currently encode `durable_frontier_time` / a one-hour dirty ceiling. Step-5.5 and WP-12 explicitly reject that campaign-global timer/frontier as canonical architecture. A machine-realization brief framed around “fix the hourly save implementation” could silently make stale implementation debt the design premise.

Required repair:

- classify the one-hour/global frontier surfaces explicitly as current machine/test debt;
- frame realization around scope-owned policy and named `MUST_BE_DURABLE_BEFORE(edge)` obligations;
- do not choose a replacement global cadence/timer/constant in Step 1;
- require Step 2 to derive exact operational metadata/policies from accepted owners and actual named edges.

Propagation:

- Task Brief problem, Goals 1–2, debt D1, questions and risks repaired;
- Source Manifest marks the affected GAME/test surfaces as required debt routes.

Resolved: **YES**

---

### C03 — publication success/dirty clearing must be generation-specific

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

Current runtime/tests use broad language such as clearing the published dirty state. Without the WP-12 generation qualifier, generation G may be frozen/published while G+1 is established locally, after which a path-level or boolean dirty clear can lose G+1.

Required repair:

- every frozen publication attempt identifies exact owner generation/fingerprint;
- confirmed publication of G may only adopt/clear G;
- current G+1 remains dirty and current locally under its owning contract;
- Step 2 must locate current prose/test/API surfaces that clear by path/scope without generation identity.

Propagation:

- Task Brief Goals 6/8, debt D3, questions, campaign flow and scenario 9 repaired;
- Source Manifest carries WP-12 generation law and flags `PERSISTENCE`/tests.

Resolved: **YES**

---

### C04 — “save completeness” could turn into a campaign/WORLD/history scan

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

`SAVE_ALL_DIRTY`, “all established state” and resulting-tree completeness can be misread as “discover all campaign truth before saving.” That would contradict Step-5.2 bounded recovery closure, WP-11 direct routing/index non-authority and `INTEGRITY.md` scope-local preflight.

Required repair:

- begin from known established dirty native roots/generations in the selected policy/SAVE scope;
- derive only correctness-required recovery/reference/interpretation dependencies;
- use WP-11 direct routes for known IDs;
- validate planned dirty/directly touched invariants locally;
- never use index/directory/history absence as the generic completeness algorithm;
- never invent missing state from summary/narration to make a SAVE look complete.

Propagation:

- Task Brief Goals 5/10, questions 3/9/10, scenarios and risk R4 repaired;
- Source Manifest adds `INTEGRITY.md`, WP-11 route/index rules and native-family conditional inspection.

Resolved: **YES**

---

### C05 — current one-file live machine could override accepted Step-5.8/WP-12 authority

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

`GAME/CORE/LIVE_SCENE.md` and current persistence/live tests are concrete and executable-looking, while accepted Step-5.8/WP-12 is more abstract. Treating the current one-file implementation as the WP-13 live publication owner would reopen/replace the already closed exact-source-CAS/live-claim architecture and could reintroduce the pre-Senior WP12-8 ambiguity.

Required repair:

- Step-5.8 and final WP-12 remain controlling live authority/currentness/durability law;
- pre-CAS live state remains prospective/non-current;
- exact-source live CAS remains the authoritative native durability edge;
- WP-13 may define SAVE/HARD composition with that edge and classify current machine debt;
- WP-16 owns final live schema/ref/CAS machine realization.

Propagation:

- Task Brief non-goals, constraints 5.8, debt D4, flows/scenarios and ownership table repaired;
- Source Manifest classifies `LIVE_SCENE.md`/live tests as implementation/debt consumers with WP-16 boundary.

Resolved: **YES**

---

### C06 — frozen publication attempt must retain application authorization/currentness basis

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

A purely Git-shaped attempt containing only repo/ref/HEAD/tree/path delta could remain technically publishable after creator/player/policy authorization changed. GitHub permission and CAS success do not establish HDM application authority.

Required repair:

- include acting principal and required authorization evidence/basis in the frozen attempt;
- include source/currentness/dependency basis needed by the native write contract;
- revalidate mutable authorization dependencies at the owning required pre-mutation boundary;
- include `ACCESS_CONTROL.md`, House-Rules and multiplayer membership consumers in Step-2 edge mapping.

Propagation:

- Task Brief Goals 6, constraints 5.10, questions 8/11 and risk R5 repaired;
- Source Manifest authority section expanded.

Resolved: **YES**

---

### C07 — treating `DURABILITY_GUARD.md` as the semantic trigger owner would erase distributed owner semantics

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

The current runtime describes `DURABILITY_GUARD.md` as authoritative for WHEN to publish. But actual reasons/promises are owned by semantic modules: `PROVISIONAL_IDENTITY`, READY_PC/PLAY_READY, host handoff, membership/access changes, House-Rule grant/adoption, explicit SAVE and live visibility/CAS. If WP-13 moves these reasons into a central guard registry/state machine, it creates a new semantic owner and generic HARD queue.

Required repair:

- semantic owner defines the named edge and required promise;
- shared WP-13 machinery evaluates/satisfies the obligation over current native generations/scopes;
- Source Manifest must include actual named owners/tests;
- Step 2 must produce an item-level edge-owner mapping before synthesis.

Propagation:

- Task Brief Goals 9, debt D5, Questions 1/8, named-edge flow and scenarios 12–14 repaired;
- Source Manifest includes onboarding/readiness/multiplayer/House-Rules owners and relevant tests.

Resolved: **YES**

---

### C08 — checkpoint adjacency could be mistaken for SAVE proof or mandatory SAVE payload

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

Current session/save prose mentions checkpoint around session/save boundaries. Without an explicit boundary, WP-13 could require a checkpoint whenever SAVE occurs or infer success from checkpoint creation, contradicting Step 5.7.

Required repair:

- explicit SAVE can succeed with zero checkpoint publication when native durable sources are sufficient;
- checkpoint joins a publication only when an independent recovery/session owner actually requires that checkpoint as its own native dirty record;
- checkpoint never proves whole SAVE/handoff durability;
- final checkpoint/currentness/schema realization remains WP-14.

Propagation:

- Task Brief non-goals, constraints 5.9, questions/scenario 15 repaired;
- Source Manifest makes Step5.7/checkpoint schemas a boundary/deferred route.

Resolved: **YES**

---

### C09 — storage-default metadata publication must not join campaign gameplay SAVE

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

Current `STORAGE.md`/`PERSISTENCE.md` expose both storage default-branch metadata publication and campaign publication. A generic multi-domain SAVE implementation could incorrectly treat storage baseline metadata as another component of campaign gameplay durability, mixing repository-role/authorization domains and reviving stale Storage-v2 assumptions.

Required repair:

- storage-default metadata remains a distinct storage-owner operation;
- it does not join ordinary campaign gameplay SAVE merely because both use Git transport;
- existing Storage-v2 wording debt remains WP-26;
- WP-13 only consumes storage metadata when a concrete accepted native owner operation independently requires it.

Propagation:

- Task Brief non-goals/ownership constraints and Source Manifest debt O09/boundaries repaired.

Resolved: **YES**

---

### C10 — partial or indeterminate native publication could be falsely acknowledged or “rolled back”

Severity: **SIGNIFICANT**  
Agree: **YES**

Failure mechanism:

A multi-domain SAVE may publish one native domain successfully and then reject/lose transport certainty in another. Treating overall SAVE as one all-or-nothing logical transaction causes one of two invalid behaviors: falsely saying nothing became durable, or trying to replay/rollback already accepted gameplay. Conversely, acknowledging SAVE after only a prepared/ambiguous publication violates the durability promise.

Required repair:

- preserve every confirmed accepted native publication as real durability;
- no cross-domain rollback/distributed transaction;
- overall SAVE stays incomplete until every promised native closure component is confirmed durable;
- indeterminate publication enters bounded exact source/lineage/current-closure verification;
- no blind retry, duplicate gameplay commit, reroll or false `saved` message;
- success/partial/failure postconditions must appear in the Step-2 evidence matrix.

Propagation:

- Task Brief constraints 5.3–5.5, questions 6/7/13/14/16, flow 11.4, scenario 16 and risk R3 repaired;
- Source Manifest explicitly routes Step5.6 ambiguity and SAVE tests.

Resolved: **YES**

---

## 3. Findings that were considered but do not require Step-1 repair

### N01 — exact SQL/SQLite realization

No finding. WP-12 already owns local HOT transaction semantics and exact DDL/API remains implementation planning. WP-13 only consumes owner generations/dirty metadata/publication handoff.

### N02 — persistent generic publication journal

No finding. Step5.6/WP12 already prohibit it; the repaired Task Brief keeps publication/SAVE composition values ephemeral.

### N03 — commit order as fictional chronology

No new finding. Step3/Step5 already forbid Git/SQL order from becoming fictional chronology. Step-5.9 is conditional Step-2 inspection if a concrete publication reconciliation path needs it.

### N04 — broad canonical owner reopening because current runtime disagrees

No finding. Current GAME/tests are explicitly classified as implementation/debt evidence where they conflict with closed canonical specs.

### N05 — Storage-v2 wording cleanup

No WP-13 finding. Existing stale wording in `BRANCH_MODEL.md` / `ACCESS_CONTROL.md` is already a bounded WP-26 documentation-consistency route and does not affect WP-13 semantics.

### N06 — WP-10 local status header

No WP-13 finding. Global current state is owned by `DEV/CURRENT_PROGRESS.md`; closed upstream spec-local historical audit wording is not a reason to expand WP-13.

---

## 4. Whole-project source/dependency challenge after repairs

The repaired framing was rechecked against the current ownership graph.

### Existing owners already settle the main architecture choices

Confirmed:

- Step 5.5 settles durability obligation/SAVE semantics;
- Step 5.6 settles campaign publication/currentness/crash-consistency architecture;
- Step 5.8 settles live exact-source CAS authority;
- WP-11 settles path/index ownership;
- WP-12 settles local generation/dirty/frozen-attempt/adoption law;
- Access Control settles application authorization;
- Step 5.7 settles checkpoint non-authority.

Therefore Step 2 is a realization/evidence problem, not a blank-sheet alternatives exercise.

### No current contradiction requiring architecture reopening was found

The current one-hour/global frontier, campaign-only SAVE wording and one-file live machine are current implementation/test debt relative to later accepted architecture. They do not invalidate the accepted architecture merely because they remain in GAME/tests.

### No new consumer requires a new semantic owner

Named durability edges remain owned by their domain modules. They can consume common WP-13 operational evaluation/publication machinery without creating a central semantic “durability job”, SAVE journal or global transaction owner.

### Current downstream boundaries remain sufficient

- checkpoint/recovery machine -> WP-14;
- live machine -> WP-16;
- bootstrap/migration -> WP-19/WP-20;
- executable implementation coverage -> WP-22;
- performance -> WP-24;
- Storage-v2 docs -> WP-26.

No roadmap rebaseline is required by Step 1.

---

## 5. Required Step-2 adversarial questions preserved by the repaired brief

Before a Decision Brief/candidate, Step 2 must have evidence capable of answering:

1. Can one local owner generation become dirty without any global durability timestamp changing?
2. Can two scopes have independent durability/exposure policy without introducing one universal frontier?
3. Can a named HARD edge identify the minimum native closure without a full campaign scan?
4. Can an explicit SAVE promise cross campaign/live native domains without a distributed transaction?
5. Can one native domain be already durable and participate with zero write?
6. Can one campaign publication update a native record plus required derived index coherently while preserving unrelated blobs byte-for-byte?
7. Can G publish while G+1 is established and remain dirty afterward?
8. Can a stale/disjoint HEAD preserve accepted IDs/RNG/semantics while transport basis is rebuilt?
9. Can an overlapping HEAD movement force owner-specific revalidation without blind merge/replay?
10. Can an indeterminate ref transition be classified with bounded evidence and no blind duplicate commit?
11. Can a membership/policy authorization change invalidate a prepared publication despite technical Git permission?
12. Can an explicit SAVE succeed without a checkpoint?
13. Can a partial multi-domain SAVE preserve accepted native durability while withholding overall `saved` acknowledgement?
14. Can current one-hour tests be replaced later without leaving an unowned durability-policy gap?
15. Can current live-machine tests be updated later without WP-13 specifying the final WP-16 live schema/protocol?

A Step-2 evidence package that cannot answer these has not reached the synthesis completeness gate.

---

## 6. Decision-rights review

All Step-1 findings are mechanically resolvable by applying current accepted authority. None requires choosing between still-credible product semantics or accepting new material risk.

No new choice is made about:

- how long SOFT state may remain unpublished in every future scope;
- a universal autosave cadence;
- exact database/API implementation;
- final live file/ref shape;
- checkpoint schema;
- migration/bootstrap policy.

If Step 2 discovers that a concrete product scope needs a new default exposure policy or another material unresolved durability promise not settled by current owners, it must produce a decision-ready escalation then.

**Human decision required at Step 1: NO.**

---

## 7. Critic closure

Initial findings:

```text
C01  BLOCKING     campaign-only SAVE framing
C02  BLOCKING     stale global one-hour/frontier treated as architecture
C03  SIGNIFICANT  non-generation-specific dirty clearing
C04  SIGNIFICANT  broad completeness scan risk
C05  SIGNIFICANT  old live implementation could override Step-5.8/WP-12
C06  SIGNIFICANT  missing acting-principal/authorization basis
C07  SIGNIFICANT  Durability Guard could become central semantic trigger owner
C08  SIGNIFICANT  checkpoint could become SAVE proof/mandatory payload
C09  SIGNIFICANT  storage metadata could join campaign SAVE incorrectly
C10  SIGNIFICANT  partial/indeterminate multi-domain outcome mishandling
```

After repairs:

```text
UNRESOLVED BLOCKING:     0
UNRESOLVED SIGNIFICANT:  0
UNRESOLVED MINOR:        0 REQUIRED FOR STEP-1 GATE
HUMAN DECISION REQUIRED: NO
```

The Step-1 package is review-ready.

---

## 8. Mandatory gate

WP-13 Step 1 may be published and presented for mandatory Senior review.

**Do not begin Step 2 before explicit Senior GO.**

Also blocked:

- WP-14;
- implementation planning;
- runtime/schema/catalog/test implementation changes.
