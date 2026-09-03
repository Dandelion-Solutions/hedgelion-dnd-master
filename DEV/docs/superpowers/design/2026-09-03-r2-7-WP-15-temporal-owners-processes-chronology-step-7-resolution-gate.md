# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Step 7 Resolution Gate

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-03

Inputs:

- Step-5 candidate specification;
- Step-6 Source Manifest expansion;
- Step-6 whole-project adversarial review (`F01..F08`).

This resolution mechanically tightens the selected Step-3 direction from already accepted owner contracts. It introduces no new product trade-off, semantic mega-owner, scheduler, global fictional clock, firing ledger, distributed transaction or historical rewind guarantee.

---

# 1. Resolution summary

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       6
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_8_MAY_PROCEED:       YES
```

---

# 2. Binding resolutions

## F01 — CLOSED — Complete typed dependency enrollment is a correctness-critical derivative invariant

Binding repair:

1. Every independently-due `ARMED` native owner occurrence SHALL provide or deterministically derive the complete bounded set of typed dependency keys whose accepted change can alter its temporal predicate.
2. Dependency enrollment/routing remains derivative. It owns neither obligation, occurrence, DUE truth, chronology nor execution.
3. Healthy acknowledged state SHALL NOT contain an armed occurrence that is missing a required future-reevaluation route.
4. `INDETERMINATE` does not remove an occurrence from enrollment when later lawful evidence can decide it.
5. Provider move/rebase, rearm, unarm, claim and terminalization SHALL coherently recompute/remove enrollment so no acknowledged gap leaves an armed occurrence reachable only through obsolete dependency state.
6. Cold recovery is operationally complete for an armed occurrence only after the owner/binding/provider basis and sufficient future invalidation routing are reconstructed.
7. Missing/incompatible completeness-required enrollment is a typed routing/recovery coherence defect. It does not erase the obligation and does not authorize campaign-wide scanning.

Result: **CLOSED**.

---

## F02 — CLOSED — Accepted materialization includes native-owner occurrence closure

Binding repair:

For current occurrence `G`, acceptance follows the controlling Step-5.3 lifecycle shapes:

```text
ARMED(G)
    -> FINALIZED

OR

ARMED(G)
    -> ARMED(G+1) + accepted F(G)
       only when schedule-independence + overlap/order-safety are proven

OR

ARMED(G)
    -> CLAIMED(G,F) + accepted F
       while F controls source-owner settlement
```

Additional binding rules:

- At acceptance, the current owner ceases exposing the same `G` as a distinct fresh materialization candidate.
- `CLAIMED(G,F)` records only the source-occurrence-to-accepted-execution relation; Step-3 remains execution-progress authority.
- Two distinct accepted firing/execution identities for one occurrence generation are an integrity defect.
- Campaign-local establishment uses the already admitted owner/ExecutionSegment local atomic boundary where applicable.
- For live-owned state, pre-CAS local material is prospective/non-current; the exact-source live CAS is the authoritative establishment edge. A stale CAS contender cannot accept a second consequence from old `G`.
- Retry/recovery resumes the accepted identity or re-evaluates still-unaccepted current owner state; it never recreates an accepted occurrence from Agenda reconstruction.

Result: **CLOSED**.

---

## F03 — CLOSED — Simulation budget cannot suppress declared dependency invalidation

Binding repair:

Two operations are explicitly separate:

```text
SPECULATIVE / DORMANT SIMULATION BUDGET
    may omit unrelated processes and avoid continuous world simulation

CORRECTNESS-REQUIRED TEMPORAL INVALIDATION
    follows complete typed dependency enrollment
```

When accepted evidence changes dependency key `K`, every currently enrolled armed occurrence whose declared predicate can be changed by `K` remains reachable for the owner-required invalidation/recheck path. Narrative interest, loaded working-set membership, Dramaturg preference or “soon affecting” heuristics cannot veto that dependency.

No affected dependency => no required reevaluation. Affected admitted dependency => optimization cannot silently skip it.

Result: **CLOSED**.

---

## F04 — CLOSED — `world.thread` semantic admission is separated from physical route and historical omissions

Binding repair:

- WP-15 canonically reconciles/adopts `world.thread` as the narrow independent generic process owner because the process has independent world identity/lifecycle and satisfies the accepted `world.*` class-admission rule.
- WP-11 supplies the accepted physical native route (`WORLD/THREADS` + discovery-only `THREAD_INDEX`) for that family. Physical route existence does not create semantic ownership by itself.
- WP-10's compact allocation omission does not force an independently persistent process into another owner and does not reopen unrelated WP-10 allocations. WP-15 closes the previously unsatisfied generic-process consumer.
- Current catalog-2.0 omission of `world.thread` kind/structure/identifier/admission/conformance realization is coordinated unreleased machine-alignment debt.
- Later realization must align catalog classification/admission ledger, exact structure, identifier policy, schema/scaffold and conformance tests as one coherent generation.
- No alternate/duplicate generic process family is authorized.

Result: **CLOSED**.

---

## F05 — CLOSED — Process status and temporal arming are distinct owner-local dimensions

Binding repair:

- `thread.status` is owner lifecycle state; it is not itself a metric provider, chronology coordinate, TemporalBinding or DUE flag.
- `resolved`, `failed`, `obsolete` (or future equivalent terminal process states) expose no new ordinary thread-advancement occurrence unless a separate explicit reactivation/new-generation owner transition exists.
- `paused` does not by itself freeze fictional time, rewrite a deadline, change provider, SAFE_REBASE, erase elapsed evidence or allocate a new occurrence.
- Whether a particular temporal obligation remains armed while a process is paused is defined explicitly by that process/binding mechanic; it is not inferred from the label alone.
- Resume/reactivation preserves or changes occurrence/binding identity only through an explicit native-owner transition.
- Machine realization must represent/derive the actual arming lifecycle sufficiently to satisfy Step-5.3; broad status labels cannot substitute for occurrence state.

Result: **CLOSED**.

---

## F06 — CLOSED — Thread association/subtype fields grant no semantic authority

Binding repair:

- `world.thread` is the semantic record family for admitted independent generic processes.
- `owner_entity_id`, if retained, is an in-fiction sponsor/controller/responsible-entity association only. It does not transfer HDM persistence ownership, write authority or current-state responsibility to the referenced entity.
- current thread subtype `kind = threat|goal|project|countdown|investigation|pursuit|custom` is owner-local process classification, not a `world.*` catalog record kind and not an owner-precedence mechanism.
- subtype names cannot shadow or duplicate specific owners such as `world.mission`, `world.contract`, `world.effect`, ResourceState or `runtime.procedure`.

Result: **CLOSED**.

---

## F07 — CLOSED — Forward-extensible history carries no arbitrary historical-retention promise

Binding repair:

- Late accepted relation/bridge evidence may extend chronology over stable old anchors without rewriting their accepted identity/meaning.
- This capability does not imply indefinite retention of every old event, transcript, metric sample or arbitrary pairwise chronology answer.
- Still-live or explicitly promised consumers retain bounded sufficient evidence under their owner/retention contracts.
- After lawful compaction, an unpromised historical query may remain `INDETERMINATE`/unavailable when required evidence is no longer retained.
- New accepted historical evidence may establish a new relation prospectively when it independently supplies/addresses adequate stable support; technical Git/history bytes, host memory or arbitrary scans do not recreate semantic authority.
- Immutable-history time travel remains supported only within forward-extensible causal semantics and available owner evidence. It is not a generic rewind/historical-state reconstruction guarantee.

Result: **CLOSED**.

---

## F08 — CLOSED — Discovery/summary indexes are not temporal-root completeness authority

Binding repair:

- known `world.thread` reads use WP-11 exact native routing;
- `THREAD_INDEX.yaml`, `CURRENT.active_threads`, Agenda lists and other discovery/current-summary projections may provide positive routing hints/candidates but cannot prove absence of an armed independently-due owner;
- temporal-root recovery and dependency invalidation use a typed completeness-required temporal-source routing/enrollment contract derived from native owner lifecycle, reusing the existing Step-5.2/5.3 model where applicable;
- required derivative routing may rebuild/repair, but acknowledged healthy state cannot omit a protected armed occurrence from the declared complete route;
- no ordinary fallback scans all `WORLD/THREADS`, all world records, LOG/history or repository directories.

Exact machine index/schema/table realization remains downstream.

Result: **CLOSED**.

---

# 3. Resolution interaction / second-order adversarial check

The combined repairs were challenged for new authority or atomicity leakage.

### No new semantic owner

Completeness-typed enrollment remains derivative; `world.thread` remains narrow; Step-3 remains accepted execution owner; chronology remains evidence.

### No scheduler/firing ledger

Dependency routing nominates/rechecks current native occurrences. It does not own a due time, queue item or firing truth.

### No distributed transaction

Source/execution closure uses already accepted native establishment boundaries:

- local owner/ExecutionSegment atomicity where admitted;
- exact-source live CAS for live-owned establishment;
- ordinary later publication under existing durability contracts.

It does not require SQLite+Git/live atomic commit.

### No hidden global scan

Completeness is provided by typed owner/dependency routing, not directory/history enumeration.

### No replay/reroll

Once accepted, stable execution/firing identity and fixed RNG remain authoritative. Routing repair/rebuild cannot reopen accepted `G`.

### No information-owner regression

Thread lifecycle/association/subtype repairs do not restore `known_by_pc_ids` or `public` as knowledge/disclosure authority.

### No historical over-promise

Forward-extensible chronology remains bounded by retained owner evidence and consumer contracts.

No new BLOCKING or SIGNIFICANT finding is introduced by the combined resolution.

---

# 4. Mandatory finding-propagation sweep

Current artifact disposition after these repairs:

| Artifact | Disposition |
|---|---|
| Step-1 Task Brief / Source Manifest / critics / Senior recovery | historical task/evidence provenance; no selected direction changes required |
| Step-2 evidence + manifest expansion | historical evidence provenance; findings refine synthesis, not extracted facts |
| Step-3 Decision Brief | selected direction remains valid; final canonical adds mechanical qualifications only |
| Step-4 collaborative review | remains historical review provenance; no accepted product trade-off changes |
| Step-5 candidate | **historical noncanonical candidate**; F01-F08 repaired wording supersedes candidate where different |
| Step-6 critic | authoritative finding record for this cycle |
| Step-7 resolution | authoritative resolution/propagation record until Step-8 final canonical publication |
| final WP-15 canonical spec | must become current implementation-facing WP-15 owner and contain all F01-F08 repairs |
| `DEV/CURRENT_PROGRESS.md` | update only at coherent Step-8 final checkpoint |
| task-local R2.7 audit cursor | update only at coherent Step-8 final checkpoint |
| roadmap | no sequencing/scope change; no update required |
| downstream obligations | propagate to WP-16/WP-19/WP-20/WP-22/WP-24/WP-26 in final canonical/cursors as applicable |

No historical derivation artifact is silently rewritten into a false record of what Step 5 originally said.

---

# 5. Required final-canonical additions

Step 8 final canonical must include, at minimum:

1. four-way owner/Agenda/chronology/Step-3 separation;
2. explicit narrow `world.thread` semantic admission and physical/catalog distinction;
3. specific-owner precedence;
4. thread status/subtype/owner-entity field dispositions;
5. typed deadlines/provider semantics;
6. complete bounded dependency enrollment and future-invalidatability recovery invariant;
7. discovery-index/current-summary non-completeness;
8. DUE derived only;
9. Step-5.3 accepted occurrence closure shapes;
10. local/live establishment and duplicate-firing race law;
11. simulation-budget versus correctness-invalidation separation;
12. fixed accepted RNG/no replay;
13. sparse owner-anchored chronology and multi-anchor frontier;
14. no technical-order chronology;
15. knowledge/disclosure owner separation;
16. Procedure timing ownership;
17. current-owner recovery/Agenda rebuild;
18. consumer-bounded chronology retention / no arbitrary historical guarantee;
19. forward-extensible capability boundary;
20. boundedness/no broad scans;
21. coordinated downstream machine/test obligations.

---

# 6. Step-7 gate

```text
F01: CLOSED
F02: CLOSED
F03: CLOSED
F04: CLOSED
F05: CLOSED
F06: CLOSED
F07: CLOSED
F08: CLOSED

UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
NEW_MATERIAL_FINDINGS:    0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
READY_FOR_STEP_8:         YES
```
