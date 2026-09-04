# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Step-3 Decision Brief

Status: **STEP 3 COMPLETE — RECOMMENDED DIRECTION ESTABLISHED / NO HUMAN-OWNED MATERIAL DECISION REQUIRED**

Date: 2026-09-04

Evidence basis:

- approved Step-1 Architecture Task Brief and Source Manifest at `1db145712632aca7b2e89c655d468192e1004a86`;
- `...-step-2-research-architecture-draft.md`.

This Decision Brief evaluates architecture alternatives. It does not authorize implementation.

---

## 1. Decision to make

Choose the minimum sufficient physical/runtime realization that simultaneously preserves:

- accepted layer-local Story projection durability;
- Story/continuity nonauthority;
- R2.2 source-Actor intentional-state ownership;
- single-player prep recomputability;
- the proven R2.5 multiplayer retained-planning consumer;
- bounded discovery/currentness/eligibility;
- non-force publication and recovery laws;
- `preparation has no entitlement to occur; canon invalidates preparation`;
- no global plot/planning/chronology authority.

The decision is primarily technical owner/topology allocation. Current evidence does not expose a product-semantics tradeoff requiring human judgment.

---

## 2. Alternatives

### Alternative A — Ephemeral Dramaturg planning everywhere

**Shape**

- preserve Story as accepted;
- all Dramaturg prep remains TurnEnvelope/current-chat only;
- no retained multiplayer horizon.

**Strengths**

- smallest persistence surface;
- strongest anti-authority property by construction;
- no planning CAS/lifecycle/schema work.

**Failure**

R2.5 already establishes an independently useful retained-planning consumer across isolated multiplayer participant sessions. Purely ephemeral planning loses shared/local preparation coherence and makes every independent chat reconstruct a different provisional horizon from partial context.

This would contradict accepted R2.5 rather than simplify it.

**Disposition:** reject.

---

### Alternative B — Generic durable planning registry / graph

**Shape**

- independent planning-entry IDs;
- campaign-wide registry/index;
- arbitrary links among players/actors/threads/scenes;
- one planning lifecycle/currentness service.

**Strengths**

- flexible querying;
- easy future feature accretion;
- fine-grained entry mutation.

**Costs and risks**

- invents independent identity/lifecycle where no consumer requires it;
- creates a new global index/registry and potential recovery/currentness authority;
- encourages plot graph semantics;
- requires orphan cleanup/backlinks/history semantics;
- makes privacy/authorization and cross-entry CAS much harder;
- invites generation/order to become campaign-wide frontier/chronology;
- expands persistence/query/runtime complexity far beyond the two proven bounded consumers.

**Disposition:** reject as YAGNI and authority-expanding.

---

### Alternative C — Scoped noncanonical Dramaturg horizon documents + accepted Story projection topology

**Shape**

Story keeps the already accepted layer-local route. Continuity remains derived retrieval. Single-player planning stays ephemeral. Multiplayer uses exactly two bounded retained horizon families:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

Planning entries are embedded typed values rather than independent records. There is no planning registry/index/scheduler/global frontier.

**Strengths**

- satisfies the proven isolated-session multiplayer consumer;
- preserves no durable single-player owner;
- direct deterministic routing by known campaign/PLAYER identity;
- bounded CAS scope;
- privacy aligns naturally with player-local files;
- source/currentness revalidation remains owner-relative;
- loss/rebuild is simple because planning is noncanonical;
- does not create new chronology/recovery/truth authority.

**Costs**

- shared document contention is possible, but current scope is small and R2.5 already requires exact-base CAS/rebase;
- selective entry rebase may rewrite one bounded horizon document;
- future measured scale may require partitioning, but no current trigger exists.

**Disposition:** recommended.

---

## 3. Story alternatives are already constrained

WP-18 does not have a legitimate choice between a legacy monolithic Story store and Step-5.10 layer-local projection state. Step-4/5.10/WP-11 already establish the controlling architecture.

Therefore:

- do not restore `world.chapter`;
- do not create one global Story file/index/frontier;
- do not create a Chronicler queue/service record;
- realize accepted layer-local Story projection contracts and preserve their nonauthority.

This is reconciliation, not reopening.

---

## 4. Recommended direction

> **LAYER-LOCAL STORY PROJECTIONS / DERIVED CONTINUITY / EPHEMERAL SINGLE-PLAYER PREP / SCOPED MULTIPLAYER DRAMATURG HORIZONS / NATIVE-OWNER-FIRST INVALIDATION**

The minimum physical direction is:

```text
Story:
    STORY/<layer>/PROJECTION_STATE.yaml
    STORY/<layer>/<shard>/<story_id>.yaml

Continuity:
    no generic record; bounded derived retrieval

Single-player Dramaturg:
    ephemeral PreparationDraft/current working context only

Multiplayer Dramaturg:
    DRAMATURG/SHARED.yaml
    DRAMATURG/PLAYERS/<player_id>.yaml
```

The exact manifest selector/schema naming is implementation-facing downstream realization. The architecture requires deterministic campaign-root-relative routing and may permit a static manifest root selector; the selector cannot own planning currentness/generation.

---

## 5. Planning semantic contract

A retained horizon is a dedicated noncanonical projection document, not `world.*`, not `runtime.*`, not a checkpoint and not an index.

Each document minimally carries:

```text
scope identity
planning contract/version identity where required
generation
source_basis / assumptions
entries[]
invalidation/revalidation cues
shared_generation_hint?  # local horizon only
```

Entries use only accepted classes:

```text
SOURCE_ANCHORED_CONSTRAINT
PROVISIONAL_DRAMATURGIC_DIRECTION
```

No entry acquires canon status through retention, repetition, shared visibility, generation advancement or Chronicler/Dramaturg output.

---

## 6. Currentness / CAS decision

### Shared horizon

A shared mutation must establish:

- multiplayer currently enabled;
- writer currently authorized for the applicable planning operation under campaign/PLAYER policy;
- exact current shared planning generation/base;
- material referenced source basis still compatible;
- no current native owner invalidates the proposed retained direction.

Publish with ordinary non-force campaign-tree semantics. Conflict requires bounded reread/revalidation/rebase or discard. No LWW/blind merge.

### Player-local horizon

Route by stable `player_id`. Player-local content is not automatically eligible to another participant or shared planning. Where a local horizon records a shared generation hint, that hint is routing/revalidation metadata only.

### Native currentness wins

Campaign/LIVE/HOT currentness, Actor state, world truth, knowledge/disclosure and Step-3 execution owners remain independent and stronger for their scopes. Planning generation never substitutes for them.

---

## 7. Lifecycle decision

No generic durable planning lifecycle record is needed.

A retained horizon is usable only when its scope/mode/source basis passes current revalidation. Conceptual states are therefore derived:

```text
ABSENT
CURRENT_COMPATIBLE
STALE_OR_INCOMPATIBLE
INACTIVE_MODE
CORRUPT_OR_UNUSABLE
```

These are interpretation outcomes, not necessarily stored enum fields.

Transitions:

```text
ABSENT -> create generation
CURRENT_COMPATIBLE -> successor generation on accepted update
STALE_OR_INCOMPATIBLE -> selective rebase or replacement generation
INACTIVE_MODE -> ignore bytes
CORRUPT_OR_UNUSABLE -> discard/rebuild
```

No tombstone service or planning history index is required for correctness.

---

## 8. Invalidation / source reference decision

`SOURCE_ANCHORED_CONSTRAINT` references native source identity/basis; it does not clone mutable authoritative facts into planning as a replacement owner.

Material use revalidates the relevant bounded source. If source movement makes the planning claim incompatible, planning yields.

Planning references do not by default enroll sources as GC retention blockers. If later a specific planning feature truly requires an explicit retention promise, that would need a separate owner/lifecycle proof.

---

## 9. Recovery decision

Recovery order remains native-owner-first:

```text
campaign/mode/PLAYER/current native owners
-> applicable Story/retained planning discovery
-> compatibility/eligibility validation
-> use as projection/preparation only
```

Lost or corrupt Story reduces history/presentation quality according to its source contracts. Lost or corrupt planning causes re-preparation. Neither permits reconstruction of canon, Actor state, accepted PC choice, mechanics, RNG or fictional chronology.

---

## 10. Instruction / host assurance decision

Architecture must propagate obligations to current instruction/runtime/test realization so that later implementation can prove:

- Narrator cannot consume raw Dramaturg/private/Chronicler material outside typed eligible handoff;
- same-envelope newly produced Story cannot feed back into gameplay/narration;
- ambient/stale context never outranks current owner;
- Actor current cognition cannot be inferred from planning/Story;
- current canon invalidates preparation;
- shared/local planning remains privacy-scoped and bounded;
- conflict/rebase has no plot restoration;
- no global scan/scheduler is introduced.

R2.6 production-like integrated acceptance remains post-implementation.

---

## 11. Machine alignment obligations

Later approved implementation must reconcile at least:

- Story/planning schemas;
- campaign manifest/static root routing as required by WP-11;
- catalog/admission-ledger provenance for planning semantics;
- runtime instruction mapping in existing owner modules rather than parallel role system files;
- executable tests for authority separation, mode/currentness/CAS/rebase/privacy/recovery and Story containment.

These are implementation obligations, not changes authorized by this Decision Brief.

---

## 12. Human decision / reopen gate

Current alternatives are not materially equivalent product choices. A is incompatible with an accepted consumer; B violates minimum-sufficient owner/topology principles; C satisfies accepted semantics with the smallest new retained surface.

```text
RECOMMENDATION:                    ALTERNATIVE C
HUMAN_DECISION_REQUIRED:           NO
UPSTREAM_REOPEN_REQUIRED:          NO
MATERIAL_RISK_ACCEPTANCE_REQUIRED: NO
IMPLEMENTATION_AUTHORIZED:         NO
```

Step 4 should attack Alternative C and its exact boundaries rather than revisit rejected alternatives without new evidence.
