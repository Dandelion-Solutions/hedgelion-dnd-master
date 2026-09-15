# Implementation Planning — Install / Bootstrap Shared-Writer Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-15
Finding: **AUTHOR GRAPH FINDING 39 — SIGNIFICANT**
Later runtime-performance repair: **AUTHOR FINDING 52 — SIGNIFICANT**

## Finding

RD-01 and RD-14 independently plan writes to the same shipped installation/bootstrap projection files:

```text
GAME/INSTALL/README.md
GAME/INSTALL/PROJECT_INSTRUCTIONS.txt
GAME/INSTALL/00_DND_BOOTSTRAP.md
```

RD-01 owns stale-projection cleanup for accepted v1 transport/product/currentness laws. RD-14 owns the final bootstrap/New-Game/campaign-selection/product flow projected into the same shipped surfaces.

The current execution graph has explicit shared-file checkpoints for scene routing, catalog-binding prose, multiplayer/session prose, historical GAME schema overlaps, `PROJECT_MAP` and `audit_engine.py`, but no checkpoint for these three install/bootstrap files.

Therefore both RDs may be locally correct while a legal implementation order still overwrites the other's admitted semantics. A worker would have to invent merge/order policy. Because these are shipped operational instructions, this is not cosmetic documentation drift: stale guidance can direct incorrect bootstrap/currentness/transport behavior.

No semantic owner changes. This is a physical shared-writer / shipped-consumer cutover defect.

---

# 1. Ownership split

Semantic ownership remains unchanged:

- RD-01 owns only the stale/current projection deltas required by `R001,R003,R033,R043,R047,R048,R050` and WP-26 documentation-routing closure;
- RD-14 owns bootstrap/product flow semantics from WP-19 and its accepted downstream joins;
- install files remain projections and gain no semantic authority.

Physical final-writer responsibility for the three overlapping install files is assigned to the RD-14 **final install/bootstrap projection checkpoint**, because RD-14 necessarily composes the later product flow after its runtime/bootstrap joins are known.

This physical assignment does not transfer RD-01 semantic duties to RD-14.

---

# 2. Required checkpoint split

RD-01 Task 2/3 produces a named local projection checkpoint:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
```

It means the RD-01-required v1 transport/currentness/stale-projection assertions have a coherent candidate delta and focused tests are GREEN. RD-01 may publish owner-local changes to non-overlapping files independently.

For the three overlapping install files, RD-14 final product documentation integration produces:

```text
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

Required edge:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
+ RD14 bootstrap/product semantic checkpoints required by the touched text
  SHARED_FILE_CHECKPOINT / JOIN_BEFORE_INTEGRATION
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

The final writer fresh-reads current bytes at its exact execution checkpoint and composes both admitted requirement sets.

---

# 3. File-specific merge law

For each overlapping path:

## `GAME/INSTALL/README.md`

Final content must preserve simultaneously:

- RD-01 accepted ordinary Project-capable ChatGPT / transport projection and no persisted model/plan identity;
- RD-14 campaign selection/New Game/resume/bootstrap product entry behavior;
- no stale path resurrection or v0.8 compatibility fiction.

## `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`

Final content must preserve simultaneously:

- RD-01 fixed Connector/no-probe/no-fallback transport instructions and current v1 routing constraints;
- RD-14 explicit selection/bootstrap/product flow and exact package/campaign identity handling;
- no shorter alternate bootstrap path that bypasses current selection/currentness/creator checks.

## `GAME/INSTALL/00_DND_BOOTSTRAP.md`

RD-14 remains the final structural replacement owner, but the result must satisfy every applicable RD-01 shipped-projection assertion. Replacement does not erase RD-01's accepted transport/currentness requirements.

No file may be accepted by taking one RD's complete version and then replaying the other RD's stale pre-integration version.

---

# 4. TDD / proof requirements

RD-14 final install/bootstrap integration must run both focused suites:

```text
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.InstallProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap -v
```

and the final package verification required by checkpoint law.

Add an exact cross-RD witness conceptually:

```text
InstallBootstrapSharedWriterTests
```

Required cases:

1. final `README.md` satisfies RD-01 transport/current-product projection and RD-14 selection/bootstrap semantics together;
2. final `PROJECT_INSTRUCTIONS.txt` contains no stale transport fallback and no bootstrap/currentness bypass;
3. final `00_DND_BOOTSTRAP.md` replacement preserves every applicable RD-01 accepted invariant;
4. reversing the stale writer order cannot silently remove the other RD's requirement set because final integration always rereads current bytes;
5. no removed `GAME/AGENTS.md` or `GAME/CORE/START.md` path is recreated;
6. install docs remain non-authoritative projections and point to current runtime owners.

A single-RD focused test suite is insufficient to close the shared-writer checkpoint.

---

# 5. Execution graph amendment

Add to Tier D shared shipped-consumer checkpoints:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
  CONSTRAINS_WITHOUT_ORDERING RD14 owner-local bootstrap work

RD01_INSTALL_PROJECTION_LOCAL_READY
+ RD14 final bootstrap/product semantics ready
  SHARED_FILE_CHECKPOINT
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

RD-14 final product closure may not claim shipped install/bootstrap readiness before this checkpoint.

This does not require all of RD-01 to precede all of RD-14. Only the physical shared-file integration checkpoint is ordered.

---

# 6. Non-goals

This repair does not:

- make install docs semantic authority;
- serialize unrelated RD-01/RD-14 tasks;
- reopen WP-19 or WP-26 architecture;
- introduce a generated documentation system;
- preserve obsolete v0.8 paths;
- authorize production implementation.

---

# 7. Later runtime-performance repair — F52 bounded campaign-menu discovery

## 7.1 Finding

The accepted owners already require bounded campaign discovery:

```text
WP24-11 bounded campaign discovery per menu operation
+ WP19-L02 bounded pre-selection discovery
  -> RD-14 select_campaign(request, bounded_campaign_cards)
```

However, RD-14 currently consumes `bounded_campaign_cards` without assigning a producer/currentness/continuation contract for that bounded set, while shipped `GAME/CORE/BOOTSTRAP_RUNTIME.md` instructs the runtime to enumerate `campaign/*` and probe `CAMPAIGN_CARD.yaml` for each campaign branch.

Therefore a conforming worker has no executable bridge from the current shipped `O(N)` card-read loop to the accepted bounded-discovery law. The missing producer is material on the cold/menu critical path: repository work can grow linearly with total campaign refs before the user can select one.

This is not permission to invent a particular REST/GraphQL primitive. The repair binds an implementation-facing bounded producer contract while preserving provider/transport choice under the existing transport owner.

Broken chain:

```text
WP24-11 / WP19-L02
  -> bounded campaign-discovery requirement
  -> RD-14 bounded_campaign_cards consumer
  -X-> bounded candidate/page producer
  -> shipped for-each-campaign card probe
  -> N-dependent remote-read fan-out
```

## 7.2 Required RD-14 producer contract

RD-14 Task 2 bootstrap implementation MUST own or bind one explicit provider-independent bounded discovery interface before `select_campaign(...)` is called.

Logical interface:

```text
discover_campaign_candidates(storage_basis, selector?, continuation?)
  -> BoundedCampaignPage

hydrate_campaign_cards(candidate_page)
  -> BoundedCampaignCards
```

`BoundedCampaignPage` MUST carry enough information to enforce, not merely describe:

```text
candidate refs/identities limited to one admitted finite menu window
continuation token/cursor or equivalent bounded continuation when more candidates remain
exhausted / more-available disposition
selector/narrowing basis when exact-name or prefix routing is used
```

The exact spelling/type may follow the final bootstrap request/result schema, but these semantics are mandatory and may not be left to worker invention.

## 7.3 Runtime laws

The final implementation and shipped projections MUST satisfy all of the following:

1. one normal menu operation does not traverse every physical `campaign/*` ref merely because more campaigns exist than the admitted finite retrieval window;
2. card hydration is limited to candidates already admitted by that bounded page/window;
3. missing/invalid `CAMPAIGN_CARD.yaml` may trigger the accepted minimum-authoritative-metadata fallback only for candidates already inside the admitted bounded set; fallback does not expand the candidate set;
4. known exact campaign identity/ref/name uses the shortest admitted exact/narrowed route and does not first enumerate the complete campaign namespace;
5. when more candidates exist, expose/use bounded continuation, paging or owner-permitted narrowing rather than silently reading the remainder;
6. when the provider cannot supply a bounded listing primitive for the current situation, ask for an exact/narrowing selector or return a typed bounded inability/continuation state; never fall back to exhaustive traversal;
7. campaign selection remains a pre-gameplay barrier: bounded discovery still must not preload PC/PLAYER/STATE/WORLD/SCENE/LOG gameplay working sets;
8. save-and-exit re-entry uses the same bounded discovery producer and does not reintroduce the shipped all-ref card loop;
9. transport/provider mechanics remain beneath the existing owner; this amendment does not prescribe REST, GraphQL or another provider API.

## 7.4 File actions / integration

Use the already-planned RD-14 implementation surfaces; do not create a second campaign-discovery subsystem.

```text
GAME/TOOLS/bootstrap.py                         RD-14 Task 2: implement/bind bounded producer before select_campaign
RD-14 bootstrap request/result schemas          carry continuation/narrowing disposition as required by the concrete interface
GAME/CORE/BOOTSTRAP_RUNTIME.md                  final shared RD-01/RD-14 CORE integration: retire for-each-ref card loop wording
GAME/INSTALL/README.md                          final RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION projection
GAME/INSTALL/PROJECT_INSTRUCTIONS.txt            final RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION projection
GAME/INSTALL/00_DND_BOOTSTRAP.md                 final RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION projection
DEV/TESTS/test_rd14_bootstrap.py                 add exact bounded-discovery behavioral witnesses
```

F52 extends the existing unpublished final RD-14/BOOTSTRAP integration; it adds no second final writer.

Under F46, `GAME/CORE/BOOTSTRAP_RUNTIME.md` remains one coherent final material edit at target `framework_module_version: 1.0.9`. F52 does not create a second module bump.

## 7.5 Exact proof

Add an exact class to `DEV/TESTS/test_rd14_bootstrap.py`:

```text
BoundedCampaignDiscoveryTests
```

It MUST prove at least:

1. a repository with more campaign refs than one admitted menu window does not issue a card read for every physical campaign ref;
2. the returned menu/page is finite and exposes a bounded continuation/narrowing disposition when additional campaigns remain;
3. the number of `CAMPAIGN_CARD` hydrations cannot exceed the admitted candidate page size;
4. an exact known campaign selector does not enumerate the full campaign namespace first;
5. missing/invalid cards use fallback only inside the current bounded candidate set and do not trigger broad expansion;
6. unsupported/unavailable bounded listing fails/degrades to exact narrowing or typed bounded continuation/inability rather than exhaustive scan;
7. save-and-exit menu re-entry uses the same bounded discovery law;
8. final `GAME/CORE/BOOTSTRAP_RUNTIME.md` and install/bootstrap projections no longer prescribe `one card read per campaign` / complete `campaign/*` traversal as the normal menu algorithm.

The existing `InstallBootstrapSharedWriterTests` final-byte witness also MUST preserve this bounded-discovery projection together with the previously required RD-01 and RD-14 semantics.

## 7.6 Graph / package consequence

No new cross-RD semantic edge is required. F52 strengthens the acceptance of the existing RD-14 bootstrap and final integration checkpoints:

```text
RD14 bounded discovery producer GREEN
  -> RD14 campaign-selection consumer GREEN
  -> RD14 bootstrap/product semantics ready
  -> existing RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

The package overlay count remains unchanged because F52 is folded into this already-mandatory overlay.

---

## Disposition

```text
AUTHOR_GRAPH_FINDING_39: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING

AUTHOR_FINDING_52: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ROOT_CAUSE: accepted bounded campaign-menu law reached an RD-14 bounded-card consumer but no executable bounded candidate/card producer, leaving shipped O(N) per-campaign remote reads as the only concrete route
REPAIR: bind provider-independent bounded campaign candidate/page + card hydration producer into RD-14; cut shipped/install projections over to bounded continuation/narrowing semantics; add exact behavioral proof
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
NEW_OVERLAY: NO — folded into mandatory overlay 28
NEW_EXECUTION_EDGE: NO — strengthens existing RD-14/bootstrap final integration acceptance
NEW_MODULE_BUMP: NO — F46 final BOOTSTRAP_RUNTIME target remains 1.0.9
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```