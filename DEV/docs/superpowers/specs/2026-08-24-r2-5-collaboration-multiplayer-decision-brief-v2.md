# R2.5 Decision Brief v2 — Agency-Safe Multiplayer Collaboration and Dramaturg Coordination

Status: **DECISION BRIEF — OWNER-APPROVED DIRECTION RECORDED SEPARATELY**

Date: 2026-08-24

Supersedes for owner decision:

- `2026-08-24-r2-5-collaboration-multiplayer-decision-brief.md`

Evidence basis:

- `../research/2026-08-24-r2-5-collaboration-multiplayer-evidence-ledger.md`
- `../research/2026-08-24-r2-5-agency-dramaturg-coordination-evidence-addendum.md`

---

## 1. Exact decision

R2.5 must solve two multiplayer-only/coordination deltas without redesigning existing live/currentness/chronology owners:

1. when asynchronous play must stop at a safe frontier so one player's earlier request does not consume another player's still-material voluntary decision opportunity;
2. how multiple independent Dramaturg phases working against one campaign repository retain compatible preparation without prewriting plot or loading all planning material every turn.

This decision does not choose schema fields, filenames, physical roots, timeout values, prompt text, polling or transport implementation.

---

## 2. Established facts

1. LIVE owns current mutable truth for one concurrently addressable shared scene; it is not campaign-wide planning coordination.
2. Chronology owns causal/order reconciliation across independent scopes; transport/Git order is not fictional order.
3. Step 4 already defines `PreparationDraft` as noncanonical conditional preparation with invalidation cues; prepared events have no entitlement to occur.
4. Step 4 already permits Dramaturg to consume relevant cross-player objective developments and retained noncanonical preparation.
5. R2.3 already provides lazy discovery/select/load/project and therefore can avoid preloading shared/local Dramaturg horizons every turn.
6. Authenticated player binding owns voluntary PC agency. Absence/presence/session metadata does not transfer it.
7. Strict mechanical responder/order semantics remain with Procedure/Continuation/Reaction/Choice/etc.
8. Independent scenes may progress independently until a material causal, resource, ownership, knowledge or agency bridge appears.

---

## 3. Alternative A — Immediate Progress + Canon/Story-Only Dramaturg Coordination

Ordinary free-form inputs resolve immediately except where existing mechanical owners already wait. Dramaturg phases coordinate only by reading current canon, Story and existing campaign premise/tone when relevant.

### Strengths

- minimal new retained planning state;
- simplest runtime;
- lowest coordination overhead.

### Weaknesses

- asynchronous arrival order can consume another player's still-open meaningful opportunity before their input arrives;
- no durable/recomputable way to collect genuinely joint free-form actions across host gaps;
- independent Dramaturg phases can remain factually consistent yet drift into incompatible campaign-level preparation/direction;
- Story is historical/presentational orientation, not a sufficient owner for current provisional preparation.

**Assessment:** too weak for proven multiplayer product requirements.

---

## 4. Alternative B3 — Agency-Safe Scoped Collaboration + Two-Level Dramaturg Coordination — RECOMMENDED

### 4.1 Coordination families

```text
INDEPENDENT / IMMEDIATE
    default; resolve now when no other human contribution remains materially relevant

COLLECTIVE / AGENCY-BLOCKED SCOPE
    resolve up to maximal safe frontier, then wait/collect only the dependent human contribution(s)

RULE-OWNED ORDERED
    Procedure / Continuation / Reaction / Choice / equivalent owner controls responder/order
```

No campaign-global `active_player` exists.

### 4.2 Maximal safe frontier

A scope may continue while player B is absent if resolving now does not materially remove, narrow or predetermine a decision B is still entitled to make under fiction/rules.

If it would, resolve only the independent portion and stop at the latest safe frontier before the dependent consequence.

Examples of material dependency classes include:

- joint action whose result depends on several voluntary declarations;
- shared commitment/negotiation where another PC can still intervene materially;
- scarce/common resource decision affecting another player's actionable choice;
- chronology convergence where transport order would otherwise arbitrarily erase an interception/reaction opportunity;
- a consequence that would seriously affect another PC when that PC has an applicable choice/reaction opportunity.

This is not universal protection from consequences. If no genuine player decision/reaction exists, native world/rules consequences may proceed normally.

### 4.3 External player coordination

Players may coordinate outside HDM through any channel. One player's statement that another agreed is a coordination hint only.

Each player's voluntary PC contribution must still be accepted through that player's authority unless explicit controller transfer exists.

### 4.4 Scoped collaboration owner

A durable/recoverable collaboration scope/window is admitted only when an unresolved human contribution obligation must survive across participant turns/host gaps and no native mechanical owner already owns it.

It owns only collection/agency coordination, conceptually including:

```text
scope/generation
required contributor set
optional contributor set
accepted contribution refs
current safe/blocked resolution boundary
OPEN -> CLOSED -> RESOLVED/OBSOLETE
source/currentness basis needed for safe continuation
```

It does not own world truth, PC intent semantics, mechanics, chronology, knowledge, disclosure or live mutation authority.

### 4.5 Input semantics

Incoming human material remains typed/separable:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

No class silently promotes into another.

### 4.6 Two-level Dramaturg coordination

#### Player-local horizon

Each player/chat may retain bounded noncanonical preparation for its own current/near horizon.

It may include relevant pressures, actors/goals, possible reactions/manifestations, opportunities, clue routes, likely unopposed developments, local pacing emphasis, assumptions and invalidation cues.

Local horizons may diverge substantially in focus while remaining compatible with canon and applicable shared planning basis.

#### Shared horizon — multiplayer only

When multiplayer is enabled, HDM admits one shared noncanonical planning projection used to coordinate multiple Dramaturg phases.

It may contain relevant campaign-level:

- premise/tone constraints by reference;
- shared pressures and important threads;
- material developments from one player line that may shape another;
- cross-player faction/antagonist directions;
- possible convergence points;
- mystery/revelation constraints;
- common assumptions and invalidation cues.

It distinguishes source-anchored constraints from provisional dramaturgic direction.

Singleplayer does not create this upper planning level merely for symmetry.

### 4.7 Preparation has no entitlement to occur

Canonical rule:

> **CANON INVALIDATES PREPARATION; PREPARATION DOES NOT CONSTRAIN CANONICAL PLAYER OR ACTOR FREEDOM.**

A player decision, Actor decision, mechanic, causal development or accepted owner transition may invalidate any shared/local preparation.

Dramaturg may reprepare from the new canon. It may not force, substitute, duplicate or contrive events solely to restore a discarded trajectory.

Shared coherence constrains preparation, not player freedom.

### 4.8 Lazy loading / shared generation awareness

Neither horizon is a mandatory per-turn preload.

Context Runtime may first use compact planning discovery/basis metadata. Full relevant shared/local planning slices are loaded only when the current Dramaturg task materially depends on them.

A local horizon may record which shared planning generation/basis it was prepared against. On later Dramaturg activation, relevant newer shared deltas trigger bounded revalidation/rebase; irrelevant changes do not force full reload/rewrite.

No background rewrite of all player-local horizons is required.

### 4.9 Catch-up and join/rejoin

Before mutable play after join/rejoin:

```text
authenticate/bind PLAYER
-> resolve controlled PC
-> acquire current campaign/live route
-> acquire collaboration/native-procedure admission
-> assemble recipient/PC eligible context + bounded catch-up
-> expose unresolved own obligations
-> accept mutable gameplay input
```

Catch-up remains a recipient-scoped R2.1/R2.3 projection, not read receipt or truth authority.

### 4.10 Split-party

Independent local scenes/horizons remain independently playable.

A bridge is required only when facts, entities, processes, chronology, agency obligations or material campaign planning relevance cross scopes.

LIVE/currentness resolves factual mutable ownership; chronology resolves causal order; collaboration protects still-open human agency; Dramaturg horizons coordinate noncanonical preparation.

---

## 5. Alternative C — Campaign Director / Global Plot and Turn Board

One durable campaign-level coordinator owns active player/readiness, pending input and global planned narrative direction.

### Strengths

- simple global overview;
- easy answer to who/what is pending;
- direct way to synchronize all Masters.

### Weaknesses

- becomes a second gameplay/turn authority;
- fights split-party independent scopes;
- duplicates rules-owned sequencing;
- strongly risks turning preparation into plot authority;
- pushes every local scene through a campaign-global coordination bottleneck;
- encourages global preload and overcentralized planning.

**Assessment:** reject.

---

## 6. Recommendation

Choose **B3 — Agency-Safe Scoped Collaboration + Two-Level Dramaturg Coordination**.

Confidence: **HIGH**.

B3 adds only the missing multiplayer semantics:

- protect still-open voluntary agency without globally freezing play;
- support bounded joint free-form input across async gaps;
- let multiple Dramaturg phases work as parts of one campaign while keeping all preparation provisional and lazy-loaded.

---

## 7. Proposed laws if B3 is approved

1. collaboration is coordination only, never a second gameplay authority;
2. immediate independent play is default;
3. resolve to the maximal safe frontier before waiting;
4. do not consume another player's still-material voluntary decision by transport order;
5. absence is neither consent nor immunity from automatic consequences;
6. external coordination does not authorize another player's PC;
7. collective obligations are bounded and scope-local;
8. native mechanical responder/order owner wins;
9. OOC/diegetic/action/control semantics remain distinct;
10. split-party independent scopes continue when not dependent;
11. join/rejoin acquires current route/admission/context before mutation;
12. catch-up is recipient projection, not read receipt/history authority;
13. multiplayer may retain player-local Dramaturg horizons;
14. multiplayer additionally retains one shared Dramaturg horizon;
15. singleplayer does not require the shared upper horizon;
16. both horizons are noncanonical and source-bounded;
17. shared horizon constrains local preparation coherence, not player/Actor freedom;
18. canon invalidates preparation, never vice versa;
19. invalidated preparation may be discarded/reworked without plot restoration;
20. horizons are lazy-loaded and revalidated only when materially relevant;
21. planning artifacts cannot self-promote provisional claims into facts;
22. no background global preparation rewrite/scheduler is required.

---

## 8. Diamond / Strong disposition delta

| Item | B3 disposition |
|---|---|
| **D21** | adopted: scoped durable/recomputable async collaboration semantics |
| **D22** | mostly inherited; agency/planning bridge delta added |
| **D23** | adopted: independent / agency-blocked collective / native ordered modes |
| **S43** | adopted: typed OOC/diegetic/action/control separation |
| **S44** | adopted: bounded recipient-specific catch-up |
| **S45** | adopted: current-frontier/admission/context acquisition before mutation |
| **S54** | adopted/refined: collective window is driven by material agency dependency, not generic batching timer |
| **S14** | **activated narrowly**: retained local + multiplayer-shared noncanonical planning horizons; no plot authority |

Inherited D20/D24/S41/S42/S46/S47/S50/S51/S52/S57 remain preserved and are not reopened.

---

## 9. Exact owner choice

- A — Immediate Progress + Canon/Story-Only Dramaturg Coordination
- **B3 — Agency-Safe Scoped Collaboration + Two-Level Dramaturg Coordination [recommended]**
- C — Campaign Director / Global Plot and Turn Board

Approval of B3 approves semantic direction only. Exact schema fields, files, persistence roots, IDs, generation encoding, prompt representation and host limits remain downstream mapping/assurance work.