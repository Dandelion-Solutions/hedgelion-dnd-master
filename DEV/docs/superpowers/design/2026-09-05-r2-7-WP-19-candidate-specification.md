# R2.7 WP-19 — Step 5 Candidate Specification

Status: **STEP 5 CANDIDATE — PRE-ADVERSARIAL-REVIEW**

Date: 2026-09-05

## 1. Scope and ownership

This candidate owns the WP-19 **composition contract** for bootstrap / campaign creation / initial materialization and the immediately adjacent PO-001/PO-002/PO-003 consumer bindings.

It does not replace the owners it composes:

- Storage/runtime selection owner;
- Step-5 publication/durability/recovery owners;
- R2.2 Actor current continuity;
- Step-4 `world.knowledge`, disclosure, role/context and SemanticEvent history;
- R2.3 Context Runtime;
- R2.4 single-context logical-role execution;
- WP-10 durable record-family allocation;
- WP-13 durability/save/publication;
- WP-15 chronology;
- WP-16 multiplayer/access/live state;
- WP-18 Story/continuity.

No new gameplay mode, campaign lifecycle state, generic memory system, psychology-history owner, persistence owner or model-call owner is introduced.

## 2. Normative terminology

**Selection barrier** — no campaign-specific runtime/state/recovery resolution until one existing campaign or New Game is explicitly selected in the current chat.

**Creation envelope** — frozen technical inputs sufficient to deterministically materialize the first campaign-specific tree.

**Blank scaffold publication** — the first campaign-specific from-scratch generated tree/commit/ref update.

**PROVISIONAL_IDENTITY** — early durable stable protagonist identity anchor while mechanics remain incomplete.

**READY_PC** — current mechanical commitment frontier defined by the existing owner.

**PLAY_READY** — minimum durable starting/current-routing frontier required with READY_PC for lifecycle `active`.

**Historical decision basis** — bounded event-time evidence attached to/associated with a qualifying SemanticEvent so later retrospective consumers can recover the material T0 basis without substituting mutable T1 state.

**Exit-to-selection** — session/navigation composition after confirmed save; not a durable campaign lifecycle or membership transition.

## 3. Selection and campaign menu law

### WP19-L01 — Explicit choice

A fresh/current unselected chat SHALL NOT infer campaign identity from:

- one accessible campaign;
- most recent/active/paused campaign;
- generic play/start/continue language that is not unambiguous;
- cached prior-chat state.

The runtime SHALL obtain an explicit existing-campaign or New Game choice. Unambiguous explicit campaign/new-game intent supplied in the user's opening message satisfies the barrier without repeating the same question.

### WP19-L02 — Bounded discovery before selection

Before selection, runtime MAY inspect bounded storage/campaign discovery projections required for the menu, but SHALL NOT:

- pin/load a gameplay campaign working set;
- resolve exact campaign runtime package for play;
- load CONFIG/STATE/SCENE/PC/world history merely for menu presentation;
- run recovery or migration checks;
- prepare recap/gameplay context.

Campaign cards are preferred bounded projections with manifest fallback/revalidation under current owners.

## 4. New Game exact identity law

### WP19-L03 — Storage baseline is NEW-only

`DND_STORAGE.engine.baseline` selects the storage-owner-approved default runtime identity for a NEW campaign only. It SHALL NOT mutate, override or select an existing campaign runtime.

### WP19-L04 — Exact package admission

Before generation, the runtime SHALL have one exact validated local `RUNTIME_PACKAGE` compatible with the selected storage baseline. The creation identity set includes:

```text
engine_version
package_id
source_commit_sha | null   # truthful provenance only
package_sha256
ruleset_set_sha256
```

`ruleset_set_sha256` is the selected package's validated resolved-ruleset-set identity. Version/tag alone is insufficient.

### WP19-L05 — Frozen creation envelope

Before remote object mutation, freeze at least:

```text
storage repository identity
pinned storage default-branch HEAD H
creator authenticated login
authorized mode
neutral campaign branch
campaign_id
created_at
exact package identity set from L04
```

Branch naming remains `campaign/YYYYMMDD[-NN]`; branch name carries no lore/mode/owner authority.

## 5. Scaffold materialization/publication

### WP19-L06 — Exact generator is authoritative

Use the selected package's own `TOOLS/init_campaign.py` exactly once into a fresh local output root. Generator output is the complete authoritative blank scaffold.

Required generator identity inputs include all L04 identity members, including `ruleset_set_sha256`, plus campaign/branch/creator/time/mode inputs.

No schema reasoning or per-file GitHub creation may replace a failed/unavailable generator.

### WP19-L07 — First publication is from scratch

The first campaign-specific publication SHALL be:

```text
complete generator output
 -> one Git tree FROM SCRATCH
 -> one initialization commit parented to H
 -> one non-force campaign-ref create/update
```

Storage marker/README/default-branch contents are ancestry only and SHALL NOT leak into the resulting campaign tree.

All later ordinary campaign-tree publications use existing base-tree delta semantics under persistence owners.

### WP19-L08 — Creator authority

Campaign creator is derived from `author.login` of the first campaign-specific initialization commit. Card/manifest projections SHALL NOT become competing creator authority.

### WP19-L09 — Creation failure truthfulness

If generator, local completeness validation, publication or ref update cannot be safely completed, creation stops. Do not synthesize a partial campaign, report success, ask the player to continue into setup, or force-push.

Prepared/unpublished Git objects have no campaign authority.

### WP19-L10 — Infrastructure invisibility

After successful scaffold publication, technical initialization is normally invisible. Player-facing flow immediately becomes ordinary human setup; do not narrate YAML, branches, commits, internal stage names or repository progress absent an actionable failure.

## 6. Initial lifecycle / progressive onboarding

### WP19-L11 — Blank scaffold state

New scaffold lifecycle is `initializing`.

### WP19-L12 — Progressive onboarding, not hard pre-live/live split

HDM SHALL NOT model onboarding as a mandatory hard `pre-live -> true-live` transition.

While `initializing`, real player agency and fiction may occur with a provisional PC when each attempted interaction has sufficient committed local dependencies. Missing mechanics are blocked/resolved progressively; they are never invented merely to permit an uncertain mechanic.

### WP19-L13 — PROVISIONAL_IDENTITY

When a stable protagonist identity anchor is adopted and subsequent fiction would rely on that identity, the same stable PC identity MAY/SHALL be durably materialized according to the existing PROVISIONAL_IDENTITY boundary. It remains provisional and the campaign remains `initializing`.

Tentative alternatives do not trigger persistence.

### WP19-L14 — READY_PC

READY_PC is reached only when current material character-mechanical choices and dependencies required for ordinary mechanics-capable play are closed under its current owner. Presentation detail preferences never reduce mechanical completeness.

### WP19-L15 — PLAY_READY and activation

Lifecycle `active` requires both:

```text
READY_PC
AND
PLAY_READY durable frontier
```

PLAY_READY contains only the minimum durable launch/current-routing state necessary for reliable continuation. It does not require broad unused world generation.

Where no real decision/pause/recovery boundary intervenes, READY_PC-related state and minimal starting horizon/scene/current routing/card/lifecycle may share one coherent launch transaction.

### WP19-L16 — Save/stop during onboarding

Explicit save during unfinished onboarding persists established resumable state without manufacturing READY_PC/PLAY_READY and retains `initializing`.

Stopping an unfinished setup also remains `initializing`; `paused` is reserved for a campaign that previously reached PLAY_READY/normal active play and receives actual pause/stop intent.

### WP19-L17 — Low-friction question policy

For nonmaterial setup detail use, in order as applicable:

```text
explicit player choice
 -> deterministic rules/inheritance
 -> strong concept inference
 -> accepted campaign/rules defaults
 -> conservative Master default under player delegation
 -> one targeted question only when material alternatives remain
```

No broad mandatory Session Zero, mechanics questionnaire, distant-world preload, ceremonial acceptance phrase or extra `continue` is required.

When the last genuine blocker closes, complete minimum launch preparation silently and continue into the next playable scene in the same player-facing response.

## 7. Creation access / multiplayer

### WP19-L18 — Mode and join policy

Campaign mode is creator-controlled. Multiplayer creation defaults safely to `invite_only` unless creator intent selects another admitted policy.

### WP19-L19 — Gameplay write authority

Repository permission is not gameplay authority. Singleplayer gameplay publication is creator-only. Multiplayer gameplay publication requires the current active PLAYER binding and current access/live-owner rules.

Campaign card participant/login information is projection/hint only and SHALL be revalidated against current authority when used for access decisions.

## 8. PO-001 ordinary Master retrospective

### WP19-L20 — Active-player retrospective remains ordinary gameplay

An authorized active player may ask retrospective/history questions inside ordinary gameplay. This SHALL NOT require a Commentator-mode transition and need not advance fictional time.

### WP19-L21 — Registered bounded historical purpose

Retrospective handling SHALL use a registered R2.3-compatible purpose/need profile that binds current request, logical consumer role, principal/player/PC and disclosure eligibility.

Retrieval flow is progressive and bounded:

```text
request
 -> current entity/thread/Story orientation when useful
 -> bounded historical candidates
 -> exact/native current or SemanticEvent evidence for material/source-specific claims
 -> disclosure/no-spoiler eligibility
 -> visible answer
```

Failure of a coarse selector does not authorize whole-campaign history scanning.

### WP19-L22 — Story and disclosure

Story/continuity may orient retrospective retrieval but is not authoritative for objective/current truth, private Actor cognition, exact historical motive or player eligibility.

Physical availability of hidden historical evidence never grants disclosure. Current player/principal/PC eligibility and Step-4 disclosure law remain controlling.

### WP19-L23 — Commentator boundary

Visible active campaigns where the user lacks gameplay participation and completed readable campaigns use read-only Commentator under existing eligibility rules. Commentator consumes current/historical owners; it does not own a second history or truth state.

## 9. PO-002 save-and-exit to campaign selection

### WP19-L24 — Intent composition

`save-and-exit-to-campaign-selection` is composition of existing save/durability + session/context navigation + campaign-selection owners. It is not a new campaign lifecycle enum/event by itself.

### WP19-L25 — Success ordering

Required order:

```text
existing SAVE_ALL_DIRTY/native save boundary
 -> confirmed successful required campaign/live durability
 -> clear this chat's selected gameplay context
 -> re-enter normal campaign-selection gate
```

Do not clear selected gameplay context or report combined success before the applicable durability result is known successful.

If publication is rejected/indeterminate/fails, retain the strongest truthful recovery-safe context/frontier and report only the actual save/exit result.

### WP19-L26 — Session-local clear/preserve boundary

After successful save, clear session-local state that could cause subsequent user input to act as if the just-exited campaign were still selected, including as applicable:

- selected campaign ID/branch/campaign-root gameplay binding;
- pinned campaign gameplay HEAD/native source working-set bindings;
- hot campaign working set and dirty-set ownership for this chat after successful flush;
- active gameplay role-context/player/PC binding;
- this chat's current live participation handle.

Preserve:

- authenticated principal/session identity;
- selected storage repository sufficient to return to its campaign menu;
- inert local runtime-package caches;
- durable campaign lifecycle, PLAYER membership, PC-control ownership and canonical world state exactly as persisted.

A future implementation may retain benign read caches only if they cannot bypass the selection barrier/currentness revalidation.

### WP19-L27 — No implicit durable side effects

Exit-to-selection does not by itself mean:

```text
paused
completed
archived
multiplayer membership leave
PLAYER deactivation
PC-control transfer
campaign-wide stop
```

If a native save boundary requires live consolidation, perform only that existing-owner work. Ending one user's chat does not close a still-shared live epoch solely because that chat exits.

### WP19-L28 — Same-chat menu re-entry

After successful clear, use the normal bounded campaign-selection/menu rules in the same chat. The previous campaign receives no implicit selection priority.

## 10. PO-003 historical Actor decision basis

### WP19-L29 — Existing historical owner

Historical Actor decision basis belongs to existing Step-4 `LOG/runtime.semantic_event` and WP-10 SemanticEvent/history record family. It is a conditional historical-evidence extension, not a new current Actor/knowledge owner or record family.

### WP19-L30 — Qualifying capture boundary

Capture is required for an accepted **material Actor decision or material cognitive transition** when later faithful continuity/explanation/replay may depend on one or more mutable event-time factors whose T0 semantics would otherwise be lost.

Capture is not required merely for:

- every NPC/turn;
- transient thought;
- trivial/incidental choice;
- `NO_CHANGE` assessment with no material historical decision evidence to retain;
- information already fully recoverable from admitted immutable evidence without ambiguity.

The trigger is semantic/event-driven, not time/count based.

### WP19-L31 — Situation-specific minimal basis

The already-required Actor/Master decision work MAY propose the smallest eligible material subset needed for the particular decision. The field set is not globally fixed.

Potential factor classes include current T0:

- `world.knowledge` stance for specific fact identities;
- source-Actor objective/goal/next intention/commitment;
- directed relationship facets `(source Actor -> target)`;
- relevant resource/constraint/circumstance state;
- admitted causal/source event/fact references;
- other owner-recognized Actor-private factors material to that decision.

### WP19-L32 — Logical basis-item contract

Physical schema spelling/layout is deferred, but each retained material factor SHALL provide logically sufficient evidence to recover:

1. source semantic owner/family;
2. stable subject/fact/relationship/resource identity;
3. the materially relevant T0 value/stance **or** an immutable historical evidence reference that deterministically recovers that T0 meaning;
4. required source/provenance refs under the source owner;
5. association with the accepted decision/transition SemanticEvent.

A reference only to a mutable current record is invalid when later mutation could change the referenced meaning.

### WP19-L33 — Deterministic admission boundary

The LLM may propose material-factor selection only from the already admitted decision context. Deterministic validation SHALL reject basis items that fail any applicable condition:

- factor/source was not eligible in the Actor's T0 context;
- unsupported owner/source class;
- missing stable identity;
- missing recoverable T0 value/evidence semantics;
- unbounded/raw context capture;
- hidden chain-of-thought/reasoning trace/private prompt state;
- malformed/provenance-invalid shape.

The validator guarantees admissibility, provenance and bounded representation. It does not claim to independently reproduce the model's semantic judgment of which among multiple eligible factors mattered; that selection remains part of the accepted Actor-decision proposal subject to deterministic constraints.

### WP19-L34 — No current-state mutation from history

Historical decision basis SHALL NOT become a writable current cognition/relationship/knowledge owner, restore T0 state into current owners, or imply reciprocity for directed relationships.

R2.2 and `world.knowledge` remain current-state owners.

### WP19-L35 — Durability

Once accepted, required basis is SemanticEvent/history state and follows existing SOFT/HARD/save/live durability law. Basis capture itself SHALL NOT create a separate per-decision Git publication boundary.

At explicit save, established dirty required history participates in the same coherent native campaign transaction as other applicable dirty state.

### WP19-L36 — Bounded retrieval and discovery

A retrospective consumer SHALL locate basis through current bounded R2.3/history discovery. Existing event/entity/Story/index projections may guide discovery, but indexes remain derived/non-authoritative.

If machine realization lacks enough discovery metadata for bounded decision-event lookup, add the minimum derived projection under existing index ownership. Do not introduce a second history authority or ordinary campaign-wide scan.

### WP19-L37 — Insufficient historical evidence

When admitted T0 evidence cannot establish the exact historical motive/basis requested, the visible answer SHALL distinguish known evidence from inference and SHALL NOT present a newly inferred exact motive from current T1 Actor state as established history.

## 11. Mandatory latency/interactivity law

### WP19-L38 — Zero-extra-serial capture baseline

For PO-003 capture on the ordinary gameplay critical path, baseline architecture requires:

```text
additional sequential LLM calls solely for basis capture = 0
additional serial remote/tool reads solely for capture when required T0 data is already in admitted decision context = 0
additional separate remote publications solely for basis = 0
basis work on irrelevant/trivial/NO_CHANGE turns = 0
additional context/output = bounded typed material items only
```

Decision basis is an in-band typed byproduct of already-required Actor/Master decision work and existing persistence batching.

### WP19-L39 — Serial-cost escalation

If later concrete realization evidence proves that correctness requires an additional serial LLM/tool round-trip on ordinary gameplay critical path, that is a material architecture/performance issue. It SHALL be surfaced through the applicable architecture/Product Owner process before becoming baseline.

No implementation may silently convert PO-003 into a dedicated post-decision rationale pass.

## 12. Recovery / failure / concurrency

- Creation uses exact pinned storage ancestry and non-force publication; branch/ref races follow existing publication law.
- Prepared scaffold objects do not establish campaign authority before the campaign ref selects the commit.
- Save-and-exit never reports saved/exited on partial or ambiguous publication success.
- Existing live-source currentness and membership revocation rules remain controlling; exit navigation creates no stale write authority.
- Recovery after lost SOFT decision-basis state returns to actual durable sources and does not invent history.
- Chronology may establish event order/time/causal evidence but cannot establish Actor motive/knowledge by itself.

## 13. Machine realization obligations — not implemented here

Later authorized realization must align at least:

1. `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/CORE/CAMPAIGN_SETUP.md` generator call documentation with required `ruleset_set_sha256` chain.
2. `CAMPAIGN_SETUP.md`, `NEW_CAMPAIGN_FAST_PATH.md`, campaign manifest wording and affected test prose away from a hard `pre-live/true-live` phase model while preserving initializing/READY_PC/PLAY_READY law.
3. ordinary `GAME/CORE/RUNTIME.md`/information/context consumer instructions for PO-001 retrospective behavior.
4. explicit save-and-exit-to-selection runtime/session/menu composition for PO-002.
5. SemanticEvent schema/serialization/validation and, only if required for bounded lookup, derived event-index projection for PO-003.
6. direct acceptance cases for PO-001, PO-002 and PO-003, including T0 -> T1 mutation -> retrospective T0 basis.
7. direct performance verification for L38: no dedicated model call, no redundant serial read, no separate publication, no irrelevant-turn work.
8. stale legacy scenario expectations already classified in the Source Manifest.

These are realization obligations, not authorization to modify runtime/schema/tests in this architecture assignment.

## 14. WP-20 boundary

WP-19 defines clean creation-side identity/materialization and adjacent consumers. Future released-campaign engine/ruleset/schema evolution, compatibility and migration belong to WP-20 and are not activated here.

## 15. Candidate state

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
WP20_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO
```

This candidate requires whole-project Step-6 adversarial review before canonicalization.