# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — 2 BLOCKING + 6 SIGNIFICANT FINDINGS / ALL MECHANICALLY RESOLVABLE**

Date: 2026-09-03

Candidate under review:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-step-5-candidate-spec.md`

Source graph:

- repaired Step-1 Source Manifest + SR15-01..03;
- Step-2 evidence + Source Manifest expansion;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest-step-6-expansion.md`.

---

## 1. Review method

The critic independently reconstructed and attacked the relevant whole-project subgraph across:

- Step-3 accepted execution/idempotency/RNG/firing identity;
- Steps 5.2/5.3 temporal roots, occurrence lifecycle and recovery reachability;
- Step-5.3/5.9 Agenda dependency enrollment/invalidation/rebuild;
- Step-5.9 sparse chronology, providers, late relation evidence and retention;
- Step-5.8 live authority/currentness/exact-source CAS;
- WP-12 local-vs-live establishment;
- WP-14 current-source recovery;
- Step-4 / Step-5.12 knowledge/disclosure separation;
- Step-5.11/5.13 history/retention/cleanup contracts;
- WP-10/WP-11 family allocation/routing;
- catalog class admission and exact-machine mismatch;
- current `PROCESSES.md`, `CHRONOLOGY.md`, thread schema, THREAD index/current summary and direct temporal/process consumers.

Reopen threshold remained: contradiction, newly unsatisfied consumer or material insufficiency in accepted upstream architecture. No upstream owner needs reopening; all findings below are mechanical qualification/propagation of already accepted laws.

---

# 2. Findings

## F01 — BLOCKING — Candidate does not make complete typed dependency enrollment a temporal-owner coherence invariant

### Attack

Candidate C14-C16 says Agenda is a rebuildable dependency index and cold recovery rebuilds it from current native owners. That is directionally correct but weaker than the controlling Step-5.3/5.9 integration contract.

The accepted integration law requires every independently-due armed owner to expose/deterministically derive a **complete bounded set of typed recheck dependencies**, and requires recovery to reconstruct enough enrollment for future accepted dependency changes to reach that owner. Merely hydrating the owner record and having some Agenda entry is not sufficient.

Without an explicit completeness invariant, healthy recovery could produce:

```text
owner O remains ARMED
+ O's current predicate depends on key K
+ O is not enrolled/reachable from K
+ K later changes
=> O is silently never reevaluated
```

That loses a gameplay-significant pending obligation without corrupting the owner record itself.

### Required repair

Final WP-15 must state:

1. every independently-due armed owner/binding family provides or deterministically derives all typed dependency keys whose accepted change can alter that occurrence's temporal predicate;
2. required enrollment is a correctness-critical **derivative** invariant, not semantic authority;
3. acknowledged healthy state may not contain an armed owner whose declared future reevaluation path is incomplete/unreconstructible;
4. `INDETERMINATE` owners remain enrolled when future accepted evidence can decide them;
5. provider move/rebase/rearm/unarm/claim/terminalization coherently rewrites or removes the derivative enrollment;
6. cold recovery is operationally complete only after this future-invalidatability path is reconstructed for recovered armed owners;
7. incomplete required enrollment => scoped derivative-routing/recovery defect, never permission to drop the obligation or scan the whole campaign as fallback.

**Severity:** BLOCKING.

---

## F02 — BLOCKING — Accepted materialization lacks an explicit native-owner occurrence closure at the acceptance edge

### Attack

Candidate C17-C18 correctly requires stable occurrence/execution identity and says a rebuilt Agenda cannot create the same occurrence again. It does not explicitly restate the controlling Step-5.3 source/execution closure that makes this true.

The critical invariant is not only "execution identity is stable after acceptance". At the semantic acceptance edge for occurrence G, current native owner state must cease exposing **that same G** as a fresh materialization candidate using one admitted lifecycle shape:

```text
direct finalization
safe immediate rearm to G+1
contingent CLAIMED(G,F)
```

Otherwise two hosts/retries can each evaluate G as DUE and allocate distinct accepted execution/firing identities before either observes the other's downstream execution record.

The risk is especially material for live-owned sources: WP-12 states pre-CAS local results are prospective only and Step-5.8 exact-source CAS is the authoritative live establishment edge.

### Required repair

Final WP-15 must bind materialization to Step-5.3's owner-claim shapes:

- an accepted transition for G simultaneously/coherently makes G unavailable as a fresh owner occurrence and establishes the accepted consequence identity required by the selected shape;
- a contingent `CLAIMED(G,F)` relation contains only source occurrence -> accepted execution identity, not duplicated execution state;
- immediate rearm is legal only under the already accepted schedule-independence + overlap/order-safety conditions;
- two distinct accepted firing identities for one owner occurrence generation are an integrity defect;
- local campaign HOT may establish the source/execution closure only at the already admitted local atomic edge;
- for live-owned state, the pre-CAS proposal remains non-current and the authoritative owner/execution establishment occurs at the exact-source live CAS edge; a stale contender cannot accept a second F from the old G;
- retries/recovery resolve or resume the already accepted identity and never reopen G by reconstructing Agenda state.

No new firing ledger or distributed transaction is introduced.

**Severity:** BLOCKING.

---

## F03 — SIGNIFICANT — Off-screen simulation-budget wording can be misread as permission to suppress correctness-required invalidation

### Attack

Candidate C33 inherits useful CORE language about considering only relevant/active/scheduled/soon-affecting processes. But the controlling Agenda integration contract is stronger: when accepted evidence changes typed dependency key K, every currently enrolled armed owner whose declared predicate depends on K must be reachable for required invalidation/recheck according to its owner contract.

Narrative relevance, current working-set membership, Dramaturg interest or "soon affecting" judgment cannot veto a correctness dependency already declared by the owner.

### Required repair

Separate two concepts:

- **speculative simulation budget** may avoid loading/updating unrelated dormant processes;
- **correctness invalidation** follows declared dependency enrollment and cannot be filtered by narrative relevance.

A process with no affected dependency need not be touched. A process with an affected admitted dependency cannot be skipped merely because it is off-screen or not currently interesting.

**Severity:** SIGNIFICANT.

---

## F04 — SIGNIFICANT — `world.thread` family provenance needs explicit semantic-admission versus physical-route separation

### Attack

Candidate C05 correctly notices the catalog-2.0 mismatch and WP-11 route. The whole-project reconstruction found a subtle provenance risk:

- WP-10's compact durable-family canonical allocation does not enumerate `world.thread`;
- WP-11 later explicitly routes `world.thread` as a native family;
- `CATALOG_CONTRACTS.md` says semantic class admission is responsibility/lifecycle driven and physical serialization/path does not create ownership;
- current exact catalog 2.0 still omits the kind/structure/identifier realization.

If final WP-15 says "WP-11 routes it, therefore it is semantically admitted", physical topology would accidentally become class authority. If it instead treats the catalog omission as proof the family is invalid, it would discard the independently persistent process lifecycle that WP-15 is specifically responsible for reconciling.

### Required repair

Final WP-15 must say explicitly:

1. WP-15 performs the current semantic reconciliation/admission for the **narrow independent generic process** owner under the already accepted class-admission rule;
2. WP-11 supplies the already accepted physical native route for that family; it does not create semantic ownership by itself;
3. WP-10's compact allocation omission is not an authority to force this independently persistent process into another owner; WP-15 adds the previously unsatisfied process-family consumer without reopening unrelated WP-10 decisions;
4. exact catalog/schema/identifier/admission-ledger/conformance realization remains coordinated unreleased machine-alignment debt and must become internally consistent before release;
5. no duplicate/alternate process family is introduced.

**Severity:** SIGNIFICANT.

---

## F05 — SIGNIFICANT — Current thread lifecycle labels do not yet define safe temporal arming/terminal behavior

### Attack

Current `thread.schema.yaml` exposes:

```text
status = active | paused | resolved | failed | obsolete
```

Candidate C06-C13 constrains stage/progress/deadline semantics but does not explicitly reconcile these lifecycle labels with owner occurrence arming.

Two bad implementations remain possible:

- a terminal `resolved|failed|obsolete` thread keeps an old deadline enrolled and materializes a new advancement;
- setting `paused` silently freezes/rebases fictional time or resets a deadline merely because the label changed.

The second is particularly dangerous because "pause process advancement" and "fictional time stops for this deadline/provider" are different semantics.

### Required repair

Final WP-15 must define the architecture boundary, not invent game-specific pause mechanics:

- terminal process lifecycle (`resolved|failed|obsolete` or future equivalent terminal state) exposes no new ordinary thread advancement occurrence unless a separate explicit reactivation/new-generation transition exists;
- `paused` means ordinary owner-defined process advancement is not accepted merely from the paused record, but it does **not** by itself freeze a metric provider, rewrite TemporalBinding, erase chronology, move a deadline or create a rebase;
- whether a particular obligation remains armed while the process is paused is an explicit owner/binding mechanic, not inferred from the word `paused`;
- resume/reactivation preserves or changes occurrence/binding identity only through an explicit owner transition.

Exact wire status vocabulary may be tightened later; these authority semantics are binding.

**Severity:** SIGNIFICANT.

---

## F06 — SIGNIFICANT — Thread `owner_entity_id` and process subtype `kind` can be mistaken for authority/classification mechanisms

### Attack

Current thread schema has both:

```text
kind = threat | goal | project | countdown | investigation | pursuit | custom
owner_entity_id
```

The field names invite two false interpretations:

1. `owner_entity_id` makes the referenced Actor/Faction/etc. the HDM semantic persistence owner of the thread state;
2. thread subtype `kind` creates separate catalog record families/classes or permits generic "goal" to shadow `world.mission`.

Both would violate candidate C02/C04 and the catalog owner/class rule.

### Required repair

- `world.thread` remains the semantic record family for admitted independent generic processes;
- `owner_entity_id`, if retained, is an in-fiction sponsor/controller/responsible-entity association only and grants neither repository write authority nor semantic state ownership;
- thread subtype `kind` is an owner-local process classification/value, not a `world.*` catalog kind and not a precedence rule over more specific owners;
- subtype labels cannot cause mission/contract/effect/procedure/resource state to be copied into thread.

**Severity:** SIGNIFICANT.

---

## F07 — SIGNIFICANT — Late-relation/time-travel wording can over-promise historical chronology after lawful compaction

### Attack

Candidate C24/C40 correctly preserves forward-extensible history and immutable-history time travel. Read without the Step-5.9/5.11/5.13 retention boundary, however, it could be interpreted as a promise that arbitrary old anchors/relations can always be reconstructed later.

The accepted chronology contract explicitly does **not** promise permanent temporal analytics over every historical pair. Retention is consumer-bounded. New evidence may establish a relation between old anchors only when stable identities/evidence required by the admitted operation remain lawfully available or are independently established by the new accepted evidence.

Old Git bytes, compacted transcript, host memory or arbitrary history scans do not automatically restore semantic evidence authority.

### Required repair

Final WP-15 must qualify late relation capability:

- forward-extensible relation establishment does not imply indefinite retention of all historical detail;
- still-live/promised consumers retain bounded evidence required by their owner contracts;
- arbitrary historical pair queries after lawful compaction may remain unanswerable/INDETERMINATE;
- newly accepted historical evidence can establish a new relation prospectively without rewriting old accepted identities, but cannot fabricate missing support from technical history;
- immutable-history time travel support is a semantic capability boundary, not a guarantee of unrestricted historical-state reconstruction or rewind.

**Severity:** SIGNIFICANT.

---

## F08 — SIGNIFICANT — `THREAD_INDEX` / `CURRENT.active_threads` cannot be repurposed as complete temporal-root authority

### Attack

WP-11 makes `INDEX/THREAD_INDEX.yaml` discovery-only and states index omission does not prove semantic absence. Step-2 also classifies `CURRENT.active_threads` as routing/current-summary evidence, not a temporal root registry.

Candidate C16 says recovery rebuilds Agenda from current native owner routes and admitted armed obligations but does not explicitly forbid an implementation from treating either current thread list as exhaustive temporal-source membership. That would silently lose an armed thread when a discovery projection is stale/incomplete.

### Required repair

- ordinary known thread reads continue through the WP-11 direct route;
- process discovery indexes/current summaries may nominate positive candidates but cannot prove that no armed temporal owner exists;
- independently-due temporal-root recovery/invalidation uses a typed **completeness-required temporal-source routing/enrollment contract** derived from native owner lifecycle, reusing existing Step-5.2/5.3 machinery where applicable;
- such routing remains derivative and may be rebuilt/repaired, but a healthy acknowledged state may not omit a protected armed occurrence from a completeness-required route;
- no full `WORLD/THREADS`, LOG or campaign directory scan becomes the ordinary fallback.

Exact physical index/table/schema realization remains downstream.

**Severity:** SIGNIFICANT.

---

# 3. Explicit non-findings

The independent review found **no** need to:

- make `world.thread` a universal process or temporal owner;
- create a generic scheduler/job queue/firing ledger;
- introduce one campaign-global fictional clock/frontier;
- turn Agenda or chronology into an execution owner;
- make thread public/visibility fields a parallel knowledge/disclosure owner;
- move Procedure timing into Encounter/thread;
- infer chronology from Git/CAS/SQLite/ID/host/session order;
- permit background fictional advancement from real time or recovery;
- replay/reroll accepted execution;
- create a global chronology database/temporal CSP;
- promise arbitrary historical temporal analytics or rewind;
- reopen Step-3, Step-4, Step-5.3, Step-5.8, Step-5.9, WP-10, WP-11, WP-12 or WP-14;
- start WP-16 or implementation planning.

---

# 4. Finding-propagation targets

Every material finding changes/qualifies candidate wording but does not alter the selected Step-3 direction. Step 7 must propagate as follows:

| Finding | Candidate area | Required current-final propagation |
|---|---|---|
| F01 | C14-C16, C35, C41 | Add complete typed enrollment/recovery-coherence law + downstream machine/test obligation. |
| F02 | C17-C18, C34-C35 | Add Step-5.3 materialization-shape/source-execution closure and local/live establishment law. |
| F03 | C33 | Separate speculative simulation budget from correctness-required dependency invalidation. |
| F04 | C03-C05 | Clarify WP-15 semantic admission, WP-11 physical route, WP-10 omission and catalog machine debt. |
| F05 | C06-C13 | Add process lifecycle/paused/terminal temporal-arming boundary. |
| F06 | C03-C10 | Add `owner_entity_id` and subtype `kind` nonauthority dispositions. |
| F07 | C24, C37, C40 | Add consumer-bounded retention/no historical reconstruction guarantee. |
| F08 | C14-C16, C35, C41 | Add discovery-index/current-summary non-completeness and completeness-typed temporal-source routing. |

Historical Task Brief, Decision Brief, collaborative review and candidate remain derivation/provenance. Step 7 and the final canonical artifact must identify the final canonical spec as the current implementation-facing owner where repaired wording differs.

No roadmap sequencing change is required.

---

# 5. Downstream impact review

After mechanical resolution:

- **WP-16** must preserve source-native occurrence closure/currentness for live-owned process materialization and cannot use CAS order as fiction;
- **WP-19/WP-20** must realize the reconciled thread/catalog/schema/scaffold and migration/bootstrap shape only after final architecture approval;
- **WP-22** must test dependency-enrollment completeness, stale routing/index behavior, duplicate firing/CAS races, pause/terminal lifecycle, Agenda rebuild, INDETERMINATE enrollment, no-scan recovery, no-reroll and historical-retention limits;
- **WP-24** measures temporal routing/fanout/index costs before repartition/optimization;
- **WP-26** repairs stale CORE/schema/document wording including global/singleton chronology frontiers and process visibility/status semantics.

---

# 6. Finding counts and gate

```text
F01 BLOCKING     complete typed dependency enrollment / recovery invalidatability
F02 BLOCKING     native-owner occurrence closure at accepted materialization edge
F03 SIGNIFICANT  simulation budget cannot suppress correctness invalidation
F04 SIGNIFICANT  world.thread semantic admission vs physical route / WP10/catalog provenance
F05 SIGNIFICANT  thread lifecycle pause/terminal temporal semantics
F06 SIGNIFICANT  owner_entity_id + process subtype nonauthority
F07 SIGNIFICANT  late-relation capability vs consumer-bounded retention
F08 SIGNIFICANT  discovery indexes/current summary are not complete temporal-root authority
```

Counts:

```text
STEP_6_BLOCKING:            2
STEP_6_SIGNIFICANT:         6
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
```

All eight findings are mechanically resolvable from already accepted architecture. Step 7 is authorized to resolve and propagate them without human escalation.
