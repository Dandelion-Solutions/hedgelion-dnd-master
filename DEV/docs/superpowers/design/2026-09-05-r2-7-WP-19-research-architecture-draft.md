# R2.7 WP-19 — Step 2 Research & Architecture Draft

Status: **STEP 2 COMPLETE — READY FOR DECISION SYNTHESIS**

Date: 2026-09-05

Research basis: `aa9f23be5d7ee137bff107abc7199c3cf4236e66`

Source accounting:
- Step-1 Source Manifest;
- `2026-09-05-r2-7-WP-19-steps-2-8-source-manifest-refinement.md`;
- current owning artifacts and machine/test consumers listed there.

## 1. Research conclusion

WP-19 is not missing a monolithic bootstrap, lifecycle, persistence, access, history or LLM subsystem. The architecture already owns the relevant concerns separately. The required design is a **composition contract** that binds those owners at campaign creation and at three adjacent user-visible interactions: progressive initialization, retrospective/history discussion, and explicit save-and-exit.

The simplest viable design is therefore:

```text
EXPLICIT SELECTION
  -> EXACT CREATION ENVELOPE
  -> ONE GENERATED BLANK-SCAFFOLD PUBLICATION
  -> initializing
  -> PROGRESSIVE LOW-FRICTION ONBOARDING
       optional durable PROVISIONAL_IDENTITY
       locally sufficient provisional play allowed
       READY_PC when mechanical frontier closes
       PLAY_READY when durable launch/current routing closes
       active iff READY_PC + PLAY_READY

ordinary active gameplay
  -> ordinary Master retrospective consumer when requested

readable non-playable/completed campaign
  -> read-only Commentator retrospective consumer

material Actor decision
  -> bounded event-time basis as SemanticEvent historical evidence
  -> ordinary durability batching

explicit save-and-exit
  -> save succeeds
  -> clear only session-local selected-gameplay binding
  -> return to normal campaign-selection gate
```

No new current-state owner, gameplay mode, campaign lifecycle state, durable record family, psychology store, outbox or model-call topology is required.

## 2. Creation/materialization architecture

### 2.1 Selection is an agency and latency barrier

Campaign-specific state/runtime resolution begins only after explicit current-chat selection of an existing campaign or New Game. A sole/recent/active campaign and generic play wording are insufficient. Before selection, menu discovery stays card-first/manifest-fallback and does not preload campaign state, exact campaign runtime, recovery, migration or recap.

### 2.2 Exact New Game creation envelope

For a New Game, freeze one creation envelope before scaffold generation:

- selected storage repository and pinned default-branch HEAD for ancestry;
- authenticated creator login;
- neutral `campaign/YYYYMMDD[-NN]` branch;
- technical campaign ID and creation timestamp;
- selected mode;
- exact validated local package matching storage `engine.baseline`:
  - engine version;
  - package ID;
  - truthful `source_commit_sha | null`;
  - package SHA-256;
  - exact `ruleset_set_sha256` from RUNTIME_PACKAGE/resolved ruleset lock.

Storage baseline selects NEW campaigns only. Existing campaigns continue to use `MANIFEST.engine.current`.

### 2.3 Materialization/publication

Run the exact selected package's `TOOLS/init_campaign.py` once into a fresh local output directory. The output is the complete blank scaffold. Publish it as one from-scratch tree, one initialization commit parented to the pinned storage default HEAD, one non-force campaign-ref update. Storage marker/README do not enter the campaign tree. Generator failure or inability to bulk-publish is terminal for creation; no per-file semantic reconstruction fallback.

Creator authority derives from `author.login` of the first campaign-specific initialization commit. Card creator value is cache/projection only.

Successful technical scaffold publication is player-facing invisible infrastructure. Player setup starts after it, without YAML/branch/commit/stage narration.

## 3. Progressive initialization and readiness

The correct lifecycle is not `setup -> pre-live -> true live`.

```text
blank scaffold: initializing
    -> stable protagonist anchor may create durable PROVISIONAL_IDENTITY
    -> provisional play may occur when the attempted interaction has committed local dependencies
    -> unresolved mechanics remain blocked rather than invented
    -> READY_PC closes current material mechanical discretion
    -> PLAY_READY closes minimum durable starting/current-routing frontier
    -> active only when both READY_PC and PLAY_READY hold
```

A provisional PC uses the same stable identity later promoted to READY_PC. Explicit save during onboarding preserves truthful resumable state but does not manufacture readiness or `paused`. `paused` requires a campaign that had already reached PLAY_READY/normal active play and a real pause/stop intent.

Player questions are minimized: explicit choice -> deterministic rule/inheritance -> strong concept inference -> accepted defaults -> one targeted question only when material alternatives remain. No broad Session Zero, broad catalog/world pre-generation or ceremonial `continue` confirmation is required.

## 4. Access and multiplayer at creation

Mode is creator-controlled. `invite_only` is the safe/default multiplayer join policy. Repository write capability is necessary infrastructure permission but never gameplay authority. A multiplayer gameplay write requires the current active PLAYER binding under WP-16/access-control law. Campaign card participant information is a hint/cache and must be revalidated.

Creation itself does not grant new engine/storage-main authority. One user's later exit from a multiplayer gameplay chat is not membership leave, PLAYER deactivation, PC-control transfer or campaign stop.

## 5. PO-001 retrospective consumer

Retrospective/history discussion for an authorized active player is ordinary D&D Master interaction, not Commentator mode. Register/use a bounded retrospective purpose/need profile under R2.3:

```text
current request + principal/player/PC + purpose
    -> Story/entity/thread hint when useful
    -> bounded historical candidate set
    -> exact current/native or SemanticEvent evidence when the claim is material
    -> current knowledge/disclosure/no-spoiler eligibility
    -> Narrator-visible Master answer
```

A question itself does not advance fictional time or make facts/PC knowledge canonical. Story may orient retrieval but cannot establish a material historical motive or widen disclosure.

Read-only Commentator uses the same admitted historical owners through its own eligible role context for visible-but-nonplayable active campaigns and completed readable campaigns.

## 6. PO-002 save-and-exit composition

Define `save-and-exit-to-campaign-selection` as one user intent composed from existing owners, not a new lifecycle transition.

Required order:

1. invoke the existing truthful save/durability boundary over all established dirty state required by the current campaign/live owners;
2. if save/publication is not confirmed successful, do not report combined success and do not discard the strongest recovery-safe selected-campaign context;
3. after success, terminate this chat's gameplay interaction binding and clear campaign-specific session-local working state that could make subsequent input act as if the campaign were still selected;
4. preserve authenticated principal, selected storage repository and inert local runtime-package caches as ordinary environment/session resources; preserve durable PLAYER membership/PC control/campaign lifecycle exactly as canonical state says;
5. re-enter the normal bounded campaign-selection/menu gate in the same chat.

Clear at least the session-local selected campaign/branch/current campaign pin, campaign-specific runtime binding as active gameplay authority, hot campaign working set, role-context/gameplay bindings and current live participation handle for this chat. Cached package bytes may remain inert; durable membership is not changed.

A native save boundary may perform live consolidation required by existing live ownership. Exit itself does not close a still-shared live epoch solely because one player's chat ended.

## 7. PO-003 historical Actor decision basis

### 7.1 Owner and trigger

Use existing Step-4 `LOG/runtime.semantic_event` / WP-10 SemanticEvent history family. Capture a basis when an accepted **material Actor decision or material cognitive transition** may later require explanation/replay and at least one material factor is mutable current Actor-private/epistemic/relationship/circumstance state whose T0 meaning could otherwise be lost.

Do not capture merely because an NPC existed, a turn occurred, a `NO_CHANGE` assessment ran or a trivial choice happened.

### 7.2 Logical basis item contract

No physical schema layout is selected in Step 2. Logically, retained basis must make each admitted item inspectable enough to identify:

- the current owner/family from which the factor came at T0;
- stable subject/fact/relationship/resource identity sufficient to understand the factor;
- the relevant T0 value/stance **or** an immutable historical evidence reference sufficient to recover it;
- source/provenance references required by the owning contract;
- its association with the accepted decision/transition event.

Examples: `world.knowledge` fact stance at T0; source-Actor `A -> B` trust/fear facet at T0; objective/commitment/intention identity/value; a constraint/resource state; causal event/fact refs.

A pointer only to a mutable current record is insufficient when later mutation changes its meaning.

### 7.3 LLM/deterministic split

The existing Actor/Master decision phase may propose the situation-specific minimal material subset because semantic relevance is contextual. Deterministic control admits only basis items that:

- were eligible/admitted in the Actor decision context at T0;
- identify an allowed current owner/source class;
- are bounded and serializable;
- contain/resolve stable identity and then-value semantics;
- contain no hidden chain-of-thought, raw prompt/context bundle or generic free-form rationale trace.

The validator does not pretend to independently prove human-like motive relevance; it verifies source eligibility, identity, shape, boundedness and provenance around the model-proposed material subset.

### 7.4 Durability and retrieval

Decision-basis evidence becomes part of accepted SemanticEvent/history state and follows existing SOFT/HARD/save/live durability law. Capturing it alone does not create a new remote publication boundary. On a later explicit save it is included if established dirty durable history requires materialization.

Retrospective retrieval remains bounded: use existing Story/entity/event/index orientation and dependency-specific historical escalation. If current physical indexes cannot locate qualifying decision events efficiently, realization must add the minimum derived discovery projection under existing index ownership rather than create a new history authority.

If historical basis is missing/insufficient, visible output states the supported limit; it must not infer an exact old motive from T1 current state.

## 8. Mandatory live-turn performance contract

Preferred candidate cost target:

```text
additional sequential LLM calls solely for basis capture: 0
additional serial remote/tool reads solely for basis capture: 0 when T0 factors are already in admitted decision context
additional separate remote publications solely for basis: 0
work on irrelevant/trivial/NO_CHANGE turns: 0
additional model output/context: bounded typed basis items only
```

This composes with `PLAY_POLICY`, R2.3 and R2.4. A separate post-decision “why did you do that?” model pass is not baseline. Full Actor snapshots are not baseline. Campaign-wide history scans are not baseline.

If later implementation evidence proves correctness cannot be achieved without an extra serial LLM/tool round-trip on the ordinary gameplay critical path, that is a material architecture/performance problem requiring explicit re-evaluation; it cannot be silently introduced.

## 9. Alternatives

### A — Composition-first existing-owner contract — RECOMMENDED

Bind existing storage/package/materializer/readiness/persistence/access/context/history owners and add only the missing cross-owner composition laws. PO-003 uses SemanticEvent with a logical typed decision-basis extension.

Benefits: minimum new authority, lowest migration/implementation surface, aligns with current machine structure, preserves zero-extra-serial target, easy to reverse/refine physical layout later.

Weakness: implementation must align several currently stale prose/schema/test surfaces; no single monolithic object describes the entire flow.

### B — New monolithic bootstrap/session orchestrator owner — REJECT

Would centralize campaign creation, readiness, save/exit and retrospective state.

Benefit: superficially simple control flow.

Failure: duplicates existing lifecycle/persistence/access/context owners and creates a new cross-domain authority; higher coupling and migration burden.

### C — New historical NPC-psychology/snapshot store — REJECT

Would snapshot Actor/knowledge state or create a separate psychology history family.

Failure: contradicts PO-003, R2.2, WP-10 and latency/storage constraints; duplicates current owners and stores irrelevant state.

### D — Reconstruct old motive later from current state/Story — REJECT

Lowest capture work but fails the defining T0-vs-T1 correctness requirement and encourages broad retrospective search/inference.

### E — Dedicated post-decision LLM rationale call — REJECT AS BASELINE

Could produce a readable explanation immediately but adds serial critical-path latency, duplicates Actor reasoning and pressures hidden-reasoning retention. Revisit only if future measured correctness evidence proves typed in-band capture insufficient.

### F — Broad upfront Session Zero/world materialization — REJECT

Conflicts with low-friction startup, progressive readiness and latency. Optional world/detail work remains lazy.

## 10. Analytical challenge

Strongest case against Alternative A: composition across many owners can be harder to implement and test than one centralized workflow, and a minimal SemanticEvent extension may initially feel less convenient than a full historical snapshot.

Response: the apparent simplicity of centralization comes from duplicating authority. Current owners already encode failure, concurrency, eligibility and durability semantics. Reusing them removes semantic special cases. Typed in-band basis capture retains only information that would otherwise be lost while preserving physical-layout option value.

Recommendation confidence: **HIGH**.

Evidence that would change the recommendation:
- proof that existing SemanticEvent/history cannot represent or durably route required event-time basis without violating its owner contract;
- measured evidence that correct basis extraction cannot be obtained from the already-required decision context and necessarily requires a serial extra model/tool round-trip;
- a demonstrated Product Owner requirement for exhaustive historical psychology or a new lifecycle/mode authority.

No such evidence was found.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```