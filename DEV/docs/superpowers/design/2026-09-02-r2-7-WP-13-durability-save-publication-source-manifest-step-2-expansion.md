# R2.7 WP-13 — Source Manifest — Step-2 Expansion

Status: **CURRENT TASK-SPECIFIC SOURCE-MANIFEST EXPANSION — STEP 2 COMPLETE**

Date: 2026-09-02

Base Source Manifest:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest.md`

Step-2 evidence record:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-2-evidence-extraction.md`

This addendum is part of the current WP-13 task-specific Source Manifest. It extends rather than replaces the repaired Step-1 manifest. The manifest remains open to further real owners/consumers discovered before synthesis/canonicalization.

---

## 1. New direct consumer activated by Step 2

| Source | Role | Why newly required | Disposition |
|---|---|---|---|
| `GAME/CORE/ENGINE_UPDATES.md` | IMPLEMENTATION / MACHINE CONTRACT / DIRECT PUBLICATION CONSUMER | Creator-authorized campaign runtime/rules provenance refresh may join a normal coherent campaign transaction; semantic-version adoption requires required durability/concurrency gates and campaign publication; storage baseline remains a separate storage-owner transaction; update success is not established before publication success. | **REQUIRED EVIDENCE / INSPECTED**; consume in Step 3–8 only as a downstream publication consumer, not as authority to start WP-20 migration design. |
| `DEV/TESTS/ENGINE_UPDATE_CASES.md` | IMPLEMENTATION / TEST | U14 requires dirty state durable before maintenance; U19 requires optimistic rebuild/non-force behavior; U21 preserves independent storage/campaign transaction success. | **REQUIRED TEST EVIDENCE / INSPECTED**; later executable alignment belongs to implementation/WP-22/WP-20 as appropriate. |

No new semantic owner is created by this activation.

---

## 2. Conditional canonical routes promoted to inspected evidence

| Source | Trigger | Extracted constraint | Final role in WP-13 |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` | current `durable_frontier_time` / frontier terminology | progress/revision/frontier claims are domain typed; no implicit cross-domain order; dirty set is not a frontier; campaign ref order is publication evidence only. | **CANONICAL / OWNING CONSTRAINT — INSPECTED**; prevents replacement global frontier. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` | multiplayer/persistence conflict paths observe Git order | Git/ref/ID/storage order cannot establish fictional chronology. | **CANONICAL / OWNING CONSTRAINT — INSPECTED**; preserve prohibition only, chronology design remains out of scope. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | prepared/unreachable commit objects may occur after races | prepared/unreachable objects are not authority; object reclamation/cleanup is owner-gated/host-GC concern. | **CANONICAL / OWNING CONSTRAINT — INSPECTED**; no WP-13 GC protocol. |

Step-5.10/5.11/5.12 remain conditional/downstream for WP-13 because current Step-5.5/5.6/5.8 authority already supplies the required SAVE/projection/write-before-reveal constraints; no candidate wording may expand into their owned semantics without reinspection.

---

## 3. Required source-set disposition after Step 2

The current Step-3 synthesis basis is:

```text
PROCESS / CURRENT STATE
    AGENTS.md
    DEV/DESIGN_PROCESS.md
    DEV/ARCHITECTURE/DESIGN_PROCESS.md
    DEV/PROJECT_MAP.md
    DEV/CURRENT_PROGRESS.md
    R2.7 execution protocol + task-local cursor

CROSS-STAGE SHIPPED TRANSPORT AUTHORITY
    R2.6 MVP Host Assurance canonical spec
    R2.6 fixed gameplay repository-transport owner clarification

CORE SEMANTIC / PUBLICATION AUTHORITY
    Step 3 execution boundary
    Step 5.1 frontier discipline
    Step 5.2 RRC
    Step 5.3 temporal/pending continuity
    Step 5.4 handoff
    Step 5.5 durability/SAVE
    Step 5.6 campaign publication
    Step 5.7 checkpoint/recovery boundary
    Step 5.8 live exact-source CAS
    Step 5.9 chronology prohibition
    Step 5.13 prepared-object cleanup boundary
    Step 5.14 integrated closure

R2.7 UPSTREAM REALIZATION
    WP-10 record families
    WP-11 routes/indexes + F02
    WP-12 HOT/generation/publication handoff + Senior recovery

AUTHORITY / CONSUMERS
    ACCESS_CONTROL
    BRANCH_MODEL
    CAMPAIGN_HOUSE_RULES
    DIEGETIC_ONBOARDING
    CHARACTER_READINESS
    MULTIPLAYER
    ENGINE_UPDATES

CURRENT MACHINE / TEST EVIDENCE
    PERSISTENCE
    SAVE_CONTRACT
    DURABILITY_GUARD
    STORAGE
    SESSION / RUNTIME / CAMPAIGN_OPERATIONS / LIVE_SCENE / INTEGRITY as routed
    current campaign/current/session/live schemas as applicable
    EXPLICIT_SAVE_CASES
    PERSISTENCE_TRANSACTION_CASES
    test_hourly_durability_contract.py
    readiness/onboarding/access/membership/live/integrity tests as routed
    ENGINE_UPDATE_CASES
```

---

## 4. Step-2 manifest gate

```text
NEW_DIRECT_CONSUMERS_ADDED:          2
CONDITIONAL_CANONICAL_ROUTES_OPENED: 3
UNRESOLVED_SOURCE_GAPS:              0
UPSTREAM_REOPEN_REQUIRED:            NO
HUMAN_DECISION_REQUIRED:             NO
```

This base manifest plus this expansion is the current WP-13 Source Manifest for Steps 3–8.