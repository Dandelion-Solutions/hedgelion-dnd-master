# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Canonical Specification

Status: **CANONICALIZED ARCHITECTURE — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

This specification is the implementation-facing WP-19 owner after Steps 2–8. It composes existing owners; it does not replace their native semantics.

Design provenance:
- Step-1 Source Manifest / Task Brief / Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-steps-2-8-source-manifest-refinement.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-research-architecture-draft.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-decision-resolution.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-resolution-propagation.md`.

Product semantics:
- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`;
- immutable PO-003 latency/interactivity amendment in `DEV/PRODUCT_OWNER_INPUT.md`.

---

## 1. Scope and ownership

WP-19 owns the **composition contract** for:

1. campaign-selection barrier;
2. exact New Game identity/materialization/publication;
3. scaffold -> progressive initialization -> READY_PC -> PLAY_READY -> active composition;
4. creation-adjacent access/multiplayer authority;
5. PO-001 ordinary active-player retrospective behavior;
6. PO-002 save-and-exit back to campaign selection;
7. PO-003 event-time historical Actor decision basis and its performance boundary.

WP-19 does **not** become a new owner of current Actor cognition, knowledge, persistence, chronology, Story, access, live state, rulesets or migrations.

Existing owners remain controlling, including R2.2, Step-4, R2.3, R2.4, WP-10, WP-13, WP-15, WP-16, WP-18 and the existing storage/publication/runtime-package contracts.

No new gameplay mode, campaign lifecycle state, generic memory subsystem, psychology-history family, outbox, background worker or mandatory model-call topology is introduced.

---

## 2. Campaign selection and bounded discovery

### WP19-L01 — Explicit selection barrier

A chat with no selected campaign SHALL NOT infer campaign identity from a sole accessible campaign, recent/active/paused status, generic play/continue wording, or prior-chat cache.

Campaign-specific runtime/state/recovery work begins only after an explicit current-chat existing-campaign or New Game selection. Unambiguous explicit intent in the user's opening message satisfies the barrier without asking twice.

### WP19-L02 — Pre-selection work stays bounded

Before selection, runtime may read only bounded storage/campaign discovery projections required for the menu. It SHALL NOT eagerly load a gameplay working set, CONFIG/STATE/SCENE/PC/world history, exact campaign runtime for play, recovery/migration state or recap.

Card-first discovery with manifest fallback/revalidation remains the preferred current route. Menu numbering is presentation only.

---

## 3. Exact New Game identity

### WP19-L03 — Storage baseline is NEW-only

`DND_STORAGE.engine.baseline` selects the storage-owner-approved default runtime identity for **new campaigns only**. Existing campaigns resolve runtime from `MANIFEST.engine.current`; storage baseline never mutates or overrides them.

### WP19-L04 — Exact package identity

Before generation, resolve one exact validated local runtime package compatible with the selected baseline. The creation identity set is:

```text
engine_version
package_id
source_commit_sha | null   # truthful provenance only
package_sha256
ruleset_set_sha256
```

Version/tag alone is insufficient. `ruleset_set_sha256` is the validated resolved ruleset-set identity carried by the selected RUNTIME_PACKAGE.

### WP19-L05 — Frozen creation envelope

Before remote object mutation, freeze at least:

```text
storage repository identity
pinned storage default-branch HEAD H
authenticated creator login
authorized mode
neutral campaign/YYYYMMDD[-NN] branch
campaign_id
created_at
exact package identity from L04
```

Branch names do not encode lore, player count, mode or owner authority.

---

## 4. Scaffold materialization and first publication

### WP19-L06 — Exact generator is authoritative

Use the selected package's `TOOLS/init_campaign.py` once into a fresh local output root. Required identity inputs include all L04 fields, including `--ruleset-set-sha256`, plus campaign/branch/creator/time/mode inputs.

The complete generator output is the blank campaign scaffold. A failed/unavailable generator SHALL NOT be replaced by LLM reconstruction, per-file GitHub writes or schema-based improvisation.

Normative identity chain:

```text
validated RUNTIME_PACKAGE.ruleset_set_sha256
 -> init_campaign --ruleset-set-sha256
 -> MANIFEST.ruleset.created_with/current
```

### WP19-L07 — One from-scratch first publication

Initial campaign publication is:

```text
complete generated scaffold
 -> one Git tree FROM SCRATCH
 -> one initialization commit parented to H
 -> one non-force campaign-ref update/create
```

Storage marker/default-branch README/owner files are ancestry only and do not enter the campaign tree.

Every later ordinary campaign-tree publication uses existing base-tree delta semantics.

### WP19-L08 — Creator authority

Campaign creator is `author.login` of the first campaign-specific initialization commit. Card or manifest creator projections are caches/hints only and cannot become competing authority.

### WP19-L09 — Truthful failure

Generator/completeness/publication/ref-update failure stops creation. Do not report success, begin player setup against a partial scaffold, or force-push. Prepared/unpublished Git objects have no campaign authority.

### WP19-L10 — Infrastructure is normally invisible

After successful technical scaffold publication, player-facing flow begins ordinary human setup without narrating YAML, branches, commits, generator phases or internal status unless an actionable failure requires it.

---

## 5. Progressive initialization and readiness

### WP19-L11 — Blank scaffold lifecycle

A new scaffold starts as `initializing`.

### WP19-L12 — No hard pre-live / true-live phase

Onboarding SHALL NOT introduce a mandatory hard gameplay phase boundary named `pre-live`, `true live` or equivalent.

While lifecycle remains `initializing`, real agency and fiction may occur with a provisional PC when the attempted interaction has committed local dependencies. Missing mechanics remain blocked or are resolved progressively; the Master does not invent unresolved modifiers/resources to force a mechanic through.

### WP19-L13 — PROVISIONAL_IDENTITY

When a stable protagonist identity anchor is adopted and subsequent fiction would rely on it, persist the same stable PC identity under the existing PROVISIONAL_IDENTITY durability boundary. Tentative alternatives do not create a write.

The PC remains provisional and lifecycle remains `initializing`.

### WP19-L14 — READY_PC

READY_PC is reached only when current material character-mechanical choices/dependencies required for ordinary mechanics-capable play are closed under its existing owner. Low mechanics-presentation preference never reduces actual mechanical completeness.

### WP19-L15 — PLAY_READY and activation

Lifecycle `active` requires both:

```text
READY_PC
AND
PLAY_READY durable frontier
```

PLAY_READY is the minimum durable launch/current-routing frontier, not permission for broad unused world generation.

When no real player/recovery boundary intervenes, READY_PC state and the minimal starting horizon/scene/current routing/card/lifecycle transition may share one coherent launch transaction.

### WP19-L16 — Save/stop during unfinished onboarding

Explicit save preserves established resumable setup state but does not manufacture readiness. Unfinished onboarding remains `initializing`.

Stopping unfinished onboarding also remains `initializing`; `paused` requires a campaign that had already reached PLAY_READY/normal active play plus actual pause/stop intent.

### WP19-L17 — Low-friction setup

For setup detail, prefer in order where applicable:

```text
explicit player choice
 -> deterministic rule/inheritance
 -> strong concept inference
 -> accepted defaults
 -> conservative delegated Master default
 -> one targeted question only when material alternatives remain
```

No broad mandatory Session Zero, full mechanics questionnaire, distant-world preload, ceremonial acceptance phrase or extra `continue` is required. Once the last genuine blocker closes, complete the minimum launch preparation silently and continue into playable fiction in the same player-facing response.

---

## 6. Creation access and multiplayer

### WP19-L18 — Mode / join policy

Mode is creator-controlled. Multiplayer creation uses `invite_only` as the safe/default join policy unless creator intent selects another admitted policy.

### WP19-L19 — Gameplay publication authority

Repository permission is necessary infrastructure capability, never sufficient gameplay authority. Singleplayer gameplay publication is creator-only. Multiplayer gameplay publication requires current active PLAYER binding under WP-16/access/live rules.

Card participant/login values are projections/hints and must be revalidated for authority-sensitive decisions.

---

## 7. PO-001 — ordinary active-player retrospective

### WP19-L20 — Retrospective stays ordinary gameplay

An authorized active player may ask retrospective/history questions inside ordinary D&D Master interaction. No Commentator transition is required, and the question alone need not advance fictional time.

### WP19-L21 — Bounded registered historical context

Retrospective handling SHALL use an R2.3-compatible registered purpose/need profile binding request, logical consumer role, principal/player/PC and disclosure eligibility.

```text
request
 -> entity/thread/Story orientation when useful
 -> bounded historical candidate set
 -> exact/native/SemanticEvent evidence for material/source-specific claims
 -> current disclosure/no-spoiler eligibility
 -> visible answer
```

Failure of a coarse selector never authorizes an ordinary whole-campaign history scan.

### WP19-L22 — Story and disclosure remain separate

Story/continuity may orient retrieval but is not authority for objective/current truth, private Actor cognition, exact historical motive or player eligibility. Physical ability to retrieve private historical evidence does not widen disclosure.

### WP19-L23 — Commentator boundary

Visible active campaigns without gameplay participation and completed readable campaigns use read-only Commentator under existing eligibility rules. Commentator consumes existing current/historical owners; it owns no second history/truth state.

---

## 8. PO-002 — save and exit to campaign selection

### WP19-L24 — Composition, not lifecycle enum

`save-and-exit-to-campaign-selection` composes existing save/durability, session-context termination and campaign-menu owners. It is not itself a new campaign lifecycle state or membership transition.

### WP19-L25 — Save success precedes clear

Required order:

```text
existing SAVE_ALL_DIRTY/native durability boundary
 -> confirmed required campaign/live save success
 -> clear this chat's selected gameplay context
 -> re-enter normal campaign-selection gate
```

Rejected/failed/indeterminate persistence SHALL NOT be reported as combined success, and the strongest truthful recovery-safe selected-campaign context/frontier must not be discarded.

### WP19-L26 — Session-local clear/preserve contract

After successful save, clear session-local state capable of making later input operate as though the just-exited campaign remained selected, including as applicable:

- selected campaign/branch/campaign-root gameplay binding;
- pinned campaign gameplay/native working-set bindings;
- flushed hot campaign working set/dirty ownership for this chat;
- active gameplay role-context/player/PC binding;
- this chat's current live participation handle.

Preserve:

- authenticated principal/session identity;
- selected storage repository sufficient for its menu;
- inert local runtime-package caches;
- durable campaign lifecycle, PLAYER membership, PC-control ownership and world state exactly as canonically persisted.

Benign caches may survive only if they cannot bypass explicit selection/currentness revalidation.

### WP19-L27 — Exit has no implicit durable side effects

Exit-to-selection alone does not mean:

```text
paused
completed
archived
membership leave
PLAYER deactivation
PC-control transfer
campaign-wide stop
```

If the native save boundary itself requires live consolidation, only that existing-owner work occurs. Ending one player's chat does not close a still-shared live epoch solely because the chat exited.

### WP19-L28 — Same-chat menu

After successful clear, re-enter the normal bounded campaign-selection flow in the same chat. The exited campaign receives no implicit reselection priority.

---

## 9. PO-003 — historical Actor decision basis

### WP19-L29 — Existing owner/family

Historical Actor decision basis belongs to Step-4 `LOG/runtime.semantic_event` and the existing WP-10 SemanticEvent/history family. This is a conditional historical-evidence extension, not a second Actor/knowledge owner or new durable record family.

### WP19-L30 — Qualifying capture boundary

Capture is required for an accepted **material Actor decision or material cognitive transition** when later faithful continuity/explanation/replay may depend on mutable T0 factors whose meaning would otherwise be lost.

Capture is not required merely for every NPC, every turn, every transient thought, trivial/incidental choice, `NO_CHANGE`, or information already unambiguously recoverable from admitted immutable evidence.

The trigger is semantic/event-driven, not time/count based.

### WP19-L31 — Situation-specific minimal subset

The already-required Actor/Master decision work may propose the smallest eligible material subset relevant to the particular decision. No fixed universal field list is required.

Potential classes include T0:

- specific `world.knowledge` fact stance;
- source-Actor objective/goal/intention/commitment;
- directed relationship facet `(source Actor -> target)`;
- relevant resource/constraint/circumstance state;
- admitted causal/source event/fact refs;
- other owner-recognized Actor-private factors material to that decision.

### WP19-L32 — Logical basis-item contract

Physical field spelling/layout remains realization work, but each retained factor SHALL provide logically sufficient evidence to recover:

1. source semantic owner/family;
2. stable subject/fact/relationship/resource identity;
3. material T0 value/stance **or** immutable historical evidence that deterministically recovers the same T0 meaning;
4. source/provenance refs required by the source owner;
5. association with the accepted decision/transition SemanticEvent.

A pointer only to a mutable current record is invalid when later mutation could change the referenced meaning.

### WP19-L33 — Deterministic admission boundary

The LLM may propose material-factor selection only from the already admitted decision context. Deterministic validation rejects basis items with any applicable defect:

- source/factor was not eligible at T0;
- unsupported owner/source class;
- missing stable identity;
- missing recoverable T0 value/evidence semantics;
- unbounded/raw context capture;
- hidden chain-of-thought/reasoning trace/private prompt state;
- malformed or invalid provenance.

The validator owns admissibility/provenance/bounded representation, not an independent simulation of subjective semantic relevance.

### WP19-L34 — Historical evidence cannot mutate current owners

Decision basis is retrospective evidence. It SHALL NOT become writable current cognition/relationship/knowledge state, restore T0 state into current owners, or imply relationship reciprocity. R2.2 and `world.knowledge` remain current-state owners.

### WP19-L35 — Ordinary durability

Accepted required basis follows existing SemanticEvent/history SOFT/HARD/save/live durability law. Basis capture alone creates no separate per-decision publication. At explicit save, dirty required history joins the same coherent native transaction as other applicable state.

### WP19-L36 — Bounded retrieval/discovery

Retrospective consumers locate basis through bounded R2.3/history discovery. Story/entity/event/index projections may orient discovery but are non-authoritative.

If physical realization lacks enough metadata for bounded qualifying-event lookup, add the **minimum derived discovery projection** under existing index ownership. Do not create a second history authority or an ordinary campaign-wide scan.

### WP19-L37 — Insufficient evidence remains insufficient

If admitted T0 evidence cannot establish the requested exact historical motive/basis, visible output distinguishes supported evidence from inference and SHALL NOT present a motive reconstructed from current T1 state as established history.

---

## 10. Mandatory latency / interactivity law

### WP19-L38 — Zero-extra-serial baseline

For PO-003 capture on ordinary gameplay critical path:

```text
additional sequential LLM calls solely for basis capture = 0
additional serial remote/tool reads solely for capture when required T0 data is already admitted = 0
additional separate remote publications solely for basis = 0
basis work on irrelevant/trivial/NO_CHANGE turns = 0
additional context/output = bounded typed material items only
```

Decision basis is an in-band typed byproduct of already-required Actor/Master decision work and existing persistence batching.

### WP19-L39 — Serial-cost escalation is material

If later realization evidence proves correctness requires an extra serial LLM/tool round-trip on the ordinary gameplay critical path, treat that as a material architecture/performance issue and route it through the applicable architecture/Product Owner process before adopting it.

A dedicated post-decision rationale model call SHALL NOT be introduced silently.

---

## 11. Failure / recovery / chronology rules

- creation publication uses pinned ancestry and non-force ref semantics;
- prepared scaffold objects have no authority before ref publication;
- save-and-exit never acknowledges saved/exited on partial/ambiguous durability;
- membership/currentness/live-source owners remain controlling after navigation changes;
- loss of unpublished SOFT decision basis does not authorize invented historical motive;
- chronology may prove typed order/time/causal evidence, never Actor motive/knowledge by itself;
- retry/presentation/history work never replays already accepted gameplay mechanics solely to regenerate retrospective evidence.

---

## 12. Deferred realization obligations

Architecture is complete; the following are **not** implementation authorization:

1. align `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `BOOTSTRAP_RUNTIME.md`, `CAMPAIGN_SETUP.md` generator-call prose with exact `ruleset_set_sha256` propagation;
2. align `CAMPAIGN_SETUP.md`, `NEW_CAMPAIGN_FAST_PATH.md`, campaign-manifest schema wording and affected test prose away from hard `pre-live/true-live` vocabulary;
3. realize PO-001 ordinary Master retrospective instruction/context consumer;
4. realize PO-002 save/session/menu clear-preserve composition;
5. realize PO-003 SemanticEvent schema/serialization/validation and only the minimum derived discovery index support actually required;
6. add direct PO-001 acceptance;
7. add direct PO-002 save-success -> clear -> same-chat-menu acceptance with multiplayer non-interference;
8. add direct PO-003 T0 basis -> T1 current mutation -> retrospective T0 evidence acceptance;
9. add direct PO-003 L38 performance verification;
10. repair/remove/qualify stale scenario expectations already classified in WP-19 evidence.

These items activate only after final architecture Senior approval and the normal implementation-planning/execution gates.

---

## 13. Compatibility / WP-20 boundary

WP-19 owns clean creation-side identity/materialization and adjacent consumers. It establishes no compatibility obligation for obsolete unreleased scaffold state.

Future **released-campaign** engine/ruleset/schema evolution, compatibility and migration remain WP-20 and are not started or authorized here.

---

## 14. Final architecture result

```text
WP19_STEPS_2_8: COMPLETE
WP19_CANONICALIZATION: COMPLETE

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0

HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE

UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO

WP20_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO

NEXT_AUTHORIZED_UNIT: NONE — MANDATORY SENIOR REVIEW
```

No final Senior PASS is implied by canonicalization.