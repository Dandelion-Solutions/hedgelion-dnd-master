# R2.5 Resolution Gate — Collaboration & Multiplayer Interaction Semantics

Status: **RESOLUTION GATE / R2.5 MAY CLOSE**

Date: 2026-08-24

Canonical candidate:

- `2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`

Adversarial review:

- `2026-08-24-r2-5-collaboration-multiplayer-adversarial-review.md`

Owner decision:

- `2026-08-24-r2-5-collaboration-multiplayer-owner-decision.md`

---

## 1. Verdict

> **R2.5 MAY CLOSE.**

No unresolved R2.5 owner-level product decision remains.

The owner-approved B3 direction survives adversarial review and is formalized canonically as:

> **AGENCY-SAFE SCOPED COLLABORATION + TWO-LEVEL DRAMATURG COORDINATION**

Broad implementation remains unauthorized.

---

## 2. Task-brief exit criteria

| # | Exit criterion | Closure evidence |
|---|---|---|
| 1 | collaboration authority bounded / no duplicate gameplay owner | Canonical §§1,5; Laws R2.5-1,13 |
| 2 | supported input semantic classes explicit | §6; Law R2.5-22 |
| 3 | mode-specific collection/resolution without global turn gate | §2; Laws R2.5-2,3 |
| 4 | absence/async preserves agency + independent progress | §§3–4; Laws R2.5-4..12 |
| 5 | join/rejoin frontier acquisition explicit/currentness-safe | §7; Laws R2.5-23..25 |
| 6 | recipient-specific bounded catch-up explicit | §7; Laws R2.5-24..26 |
| 7 | split-party uses independent frontiers/material bridges | §12; Laws R2.5-44..47 |
| 8 | per-participant R2.4 TurnEnvelope composition explicit | §13; Laws R2.5-48..49 |
| 9 | current live/shared synchronization owners remain authoritative | §§1,12; Law R2.5-1 plus responsibility matrix |
| 10 | D21/D22/D23/S43/S44/S45/S54 item-level disposition | §15; all individually dispositioned |
| 11 | inherited D20/D24/S41/S42/S46/S47/S50/S51/S52/S57 verified/narrowly extended | §15; inherited/preserved list |
| 12 | adversarial agency/secrecy/stale rejoin/batch/deadlock/cross-scene review | AR-1..AR-14 + integrated attack matrix |
| 13 | R2.6/R2.7 obligations explicit | §§16–17 |
| 14 | no broad implementation started | documentation/specification changes only |

All 14 criteria are satisfied.

---

## 3. Owner-clarified requirement closure

### 3.1 Natural async pausing without global serialization

Closed through:

- positive bounded agency-dependency requirement;
- currentness/chronology verification before contributor enrollment;
- maximal safe frontier;
- recipient-visible frontier matching semantic frontier;
- scope-local waiting;
- no silence-as-consent;
- absence not granting immunity from automatic consequences.

Result:

> one participant's earlier ChatGPT request cannot arbitrarily consume another participant's still-valid choice merely because it arrived first, while unrelated split-party play remains free to progress.

### 3.2 External player coordination

Closed through Law R2.5-12 and contribution identity/generation semantics.

Players may coordinate however they like outside HDM; each player's voluntary PC action still requires that player's accepted authority path.

### 3.3 Common campaign dramaturgy across independent Masters

Closed through multiplayer-only shared Dramaturg horizon + player-local horizons.

All horizons operate against one campaign repository/canon but are lazy-loaded through R2.3 rather than universally preloaded.

### 3.4 Story is not prewritten

Closed through Laws R2.5-30..35:

- preparation has no entitlement to occur;
- canon invalidates preparation;
- no plot restoration;
- common coherence constrains preparation rather than player/Actor agency;
- shared provisional direction is revisable;
- local independent development remains allowed.

---

## 4. Adversarial amendment closure

| AR | Canonical closure |
|---|---|
| AR-1 false-positive waiting | Law R2.5-4 positive bounded dependency required |
| AR-2 stale/impossible dependency | Law R2.5-5 currentness/chronology before enrollment |
| AR-3 provisional outcome leak | Law R2.5-8 visible frontier matches semantic safe frontier |
| AR-4 ambiguous contribution reuse | Law R2.5-19 purpose/scope/generation binding |
| AR-5 stale collaboration generation | Laws R2.5-20..21 |
| AR-6 lost-update shared planning | Law R2.5-41 current generation/CAS/rebase |
| AR-7 soft railroad through shared provisional direction | Laws R2.5-33..34 |
| AR-8 multiplayer mode lifecycle | Law R2.5-27 |
| AR-9 catch-up planning leak | Law R2.5-26 |
| AR-10 planning as recovery authority | Law R2.5-42 |
| AR-11 Story/planning lifecycle collapse | Law R2.5-43 |
| AR-12 cross-player planning leak in single physical context | Law R2.5-49 + R2.6 assurance handoff |
| AR-13 global consistency scan | Laws R2.5-36..39,47 |
| AR-14 planning relation invents causal bridge | Laws R2.5-45..46 |

All required adversarial amendments are canonicalized.

---

## 5. Diamond / Strong disposition

### Adopted / active result

- **D21** — adopted narrowly as scoped persistent async collaboration semantics.
- **D22** — existing independent scene/context/chronology frontiers retained; agency/planning bridge delta added.
- **D23** — adopted as three coordination families; global active-player rejected.
- **S43** — typed OOC/diegetic/action/control separation adopted.
- **S44** — bounded recipient-specific catch-up adopted.
- **S45** — join/rejoin current-frontier/admission/context acquisition adopted.
- **S54** — refined/adopted as material agency-dependent collective scope, not timer/debounce batching authority.
- **S14** — **trigger fired and activated narrowly** for player-local plus multiplayer-shared noncanonical Dramaturg horizons.

### Inherited / preserved

**D20, D24, S41, S42, S46, S47, S50, S51, S52, S57** remain inherited constraints. R2.5 composes with them and does not reopen their owners.

### Dormant / rejected expansion

No other Narrative Dynamics candidate is activated. No campaign director, authored plot state machine, generic planning graph, world-pressure ladder, background planning scheduler, AI-PC control framework or spectator system is introduced.

---

## 6. Authority/contamination check

Confirmed:

```text
collaboration window        != PC intent/world/mechanics authority
safe frontier               != chronology owner
timeout/presence             != agency authority
external coordination       != PC controller authorization
shared Dramaturg horizon    != canon/plot authority
player-local horizon        != canon/plot authority
planning generation         != factual currentness
planning convergence        != causal bridge
Story                       != prospective planning owner
catch-up                    != read receipt/truth authority
shared planning             != player-visible context
```

No new duplicate gameplay authority is accepted.

---

## 7. R2.6 mandatory assurance handoff

R2.6 must validate the ChatGPT-Plus/common-repository profile for:

- false-positive vs false-negative agency gating;
- maximal-safe-frontier visible-output behavior;
- stale collaboration generations;
- external-consent impersonation;
- shared-horizon concurrent update/rebase feasibility;
- shared/local planning -> Narrator leakage containment;
- catch-up planning exclusion;
- planning-text prompt injection/role confusion;
- lazy shared-planning retrieval under realistic context pressure;
- anti-railroad/no-plot-restoration scenarios;
- split-party coherence without global scans;
- host/product limitations affecting multi-chat synchronization.

These are assurance obligations, not reasons to reopen R2.5 absent contradictory evidence.

---

## 8. R2.7 mandatory machine mapping

R2.7 owns exact physical/schema/runtime realization for:

- collaboration identity/generation/lifecycle;
- local/shared Dramaturg horizons;
- planning discovery/basis metadata;
- shared-horizon exact-base/CAS/rebase realization;
- persistence roots/retention/migrations;
- Context Runtime and TurnEnvelope integration;
- tests/evaluations/tooling.

---

## 9. Closure statement

R2.5 architecture is internally complete under the current approved product envelope.

Reopen only if later evidence shows, for example:

- no bounded positive dependency test can protect agency without global serialization;
- the selected host cannot maintain shared planning currentness without introducing a conflicting authority;
- recipient containment cannot prevent planning leakage in the supported host profile;
- a real supported multiplayer mode requires a fundamentally different coordination owner.

Implementation difficulty alone is not enough to reopen the architecture.

**R2.5 may transition to COMPLETE / ARCHITECTURE CLOSED after fresh remote verification.**