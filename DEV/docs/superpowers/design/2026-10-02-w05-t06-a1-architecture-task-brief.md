# W05.T06-A1 — Architecture Task Brief

Status: **STEP-1 COMPLETE / MANDATORY REVIEW STOP 1 CANDIDATE — NOT ARCHITECTURE AUTHORITY**

Architecture block: `W05.T06-A1 — current-readiness and ordinary Master retrospective consumer architecture`

Target architecture checkpoint: `W05_T06_READINESS_RETROSPECTIVE_ARCHITECTURE_READY`

Current evidence basis: `5b7db90a36f9d5771c392f2e5119fbcd29893c03`

Source Manifest and evidence extraction: `DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-source-manifest.md`

## 1. Problem statement

W05.T06 is authorized to integrate progressive onboarding/readiness and ordinary active-player retrospective paths over already accepted HDM owners. Execution of the other T06 paths has produced two safe, published slices, but readiness and ordinary Master retrospective reached a System-Impact Gate because their current consumer composition is not represented by an admitted GAME runtime route.

Accepted product semantics and owner boundaries exist. `CHARACTER_READINESS.md`, the S6D-07 READY_PC seed, WP-19, Step-5.1, WP-12/WP-14 and the Step-4/R2.3/R2.4/WP-18 owners already constrain the result. S6D-03/04/06 also close the admitted MechanicalContext, selector and Activity-primitive surfaces. The design task is to determine the missing runtime consumer boundaries and exact current evidence routes without duplicating those owners.

Two connected concerns are in scope:

1. A deterministic, ephemeral READY_PC/local-mechanical-sufficiency assessment over the coherent current native-owner view, including accepted unpublished HOT/SOFT and currently routed LIVE where they own the relevant scope.
2. A bounded ordinary Master retrospective use case that resolves historical intent to native/current evidence and current recipient eligibility without a Commentator transition, caller-supplied historical authority, a broad history scan, or a Story dependency.

The concerns share current owner composition, Context/role eligibility, provenance and bounded-read constraints, but remain separate use cases and acceptance surfaces. The architecture investigation must keep those boundaries visible and determine whether they have a sufficient common current-source/context path.

## 2. Scope

### In scope for the architecture investigation

- Establish the trusted coherent read basis required to evaluate onboarding when current accepted state may be newer than durable campaign Git.
- Reconcile `CHARACTER_READINESS.md` and S6D-07 readiness evidence with actual Actor, PLAYER, Asset, Effect, definition/ruleset, MechanicalContext/accessor, selector/primitive, Context, RuntimeHost, HOT and recovery owners.
- Determine an ephemeral owner-issued machine assessment contract for READY_PC and local mechanical sufficiency, including exact typed unresolved/blocking dependencies, currentness and post-resume/rejoin validity.
- Define how a successful readiness assessment reaches the existing coherent durability/PLAY_READY boundary without a new lifecycle state or duplicated canonical readiness field/owner.
- Define a bounded ordinary Master retrospective consumer for the PO-001/WP-19-supported history use over registered Context/role-purpose binding, native History, current owners, and current PLAYER/`world.knowledge`/`runtime.disclosure` eligibility. It consumes evidence available under current native/retention contracts and introduces no new retention or exact-quotation guarantee.
- Determine the minimum bounded native History discovery route for the WP-19 query classes (e.g. NPC, place, earlier event/session, causal motive), using existing indexes/identity routes where sufficient and examining minimum additional derived discovery support under existing index ownership only where necessary.
- Treat Story only as an optional nomination/orientation source. Include it only if evidence establishes a material bounded-discovery benefit; any Story candidate remains nonauthoritative and native evidence remains the proof path.
- Preserve exact, typed failure/insufficiency semantics and recipient-safe answer context.
- Map the architecture to downstream implementation/test/version boundaries without starting them.

### Out of scope

- Production GAME or DEV-tool implementation, tests, schemas, catalog entries, runtime profile changes, indexes, adapters or CORE/install text.
- Reopening or re-implementing published T06-S1 save/exit and exact-size measurement, or T06-S2 selection/RuntimeHost/creator/join/rejoin. Revisit only if a concrete contradiction is proved.
- Changing accepted READY_PC, local sufficiency, T0, retrospective, Context, access, Story, HOT/SOFT, durability, publication, LIVE or chronology semantics.
- Adding a new persistent readiness field, history database, generic memory/search authority, global history/chronology index, campaign scan, Story authority, or a seventh logical `MASTER` LLM role.
- Making Story a mandatory ordinary Master retrospective dependency or importing Commentator-only PO-009/PO-012 consumer rules into ordinary Master.
- Editing T07 manifest-v5/membership retirement, T08 shipped CORE/install/module/control-plane bytes, W06 proof, or root README.
- Provider-specific Git/API design, external vendor research, real campaign writes, or production/empirical performance acceptance.
- A new MechanicalContext accessor, selector, Activity primitive or executable mechanics authority; unsupported readiness dependencies must remain under the current owner/architecture gate.
- Updating the implementation plan/envelope before final architecture GO; that is a downstream reconciliation gate.

## 3. Goals and success criteria

The completed architecture must be implementable without reconstructing current meaning from chat history or this investigation's prose. It must specify or precisely defer with a safe trigger:

- the current-source/read basis and how valid HOT/SOFT, campaign, selected LIVE and necessary operational owners compose without merging writable authority;
- owner inputs, validation/currentness and derived mechanics needed for READY_PC, tied to `actor_id`, `actor_state_revision`, current PLAYER binding, `catalog_generation`, `ruleset_set_digest_generation`, `ruleset_set_sha256` and required native Assets/Effects/definitions;
- the difference between READY_PC, per-action local mechanical sufficiency and durable PLAY_READY/`active` transition;
- the assessment's transient owner-issued result, exact blockers and re-evaluation after resume/rejoin;
- a bounded request-to-candidate-to-native-evidence route for ordinary Master retrospective, including query scope, exact source proof, current eligibility, representation floor, response handoff and finite failure/degradation;
- where native/index discovery suffices, and if it does not, the smallest owner-valid discovery projection/capability and its lifecycle/currentness/Version Impact consequences;
- whether any optional Story navigation is materially justified, its nomination-only contract, safe no-Story behavior and the explicit revisit trigger;
- existing-role/profile binding with no new logical role, one-turn/context constraints, and no raw private context handoff;
- compatibility with current semantics, schemas/catalogs, native index contracts, live-source origin/currentness, recovery and the relevant executable/scenario tests;
- a traceable downstream verification map and an exact review/implementation gate sequence.

Step-1 success is narrower: Source Manifest complete; Task Brief solution-blind enough to be falsifiable; whole-project critic independently reconstructs the dependency graph; all mechanically repairable BLOCKING/SIGNIFICANT framing findings are resolved; genuine later human trade-offs are visible; a review-ready Step-1 package is published. Step 2 must not begin before Review Stop 1 GO.

## 4. Accepted constraints and non-negotiable invariants

### Readiness

- `READY_PC` is the existing deterministic semantic predicate over the same current PC Actor and required binding/Asset/Effect/definition/rules dependencies. It is neither a first-play gate nor a 100%-filled dossier test.
- Before READY_PC, each mechanically relevant outcome is resolved only from its complete locally committed dependency set. This local-sufficiency result is not READY_PC.
- Initial material choices are fixed without situational hindsight; accepted player intent, deterministic inheritance, valid concept inference, adopted defaults and delegated defaults retain the current precedence. Ask only where a material legal choice remains unresolved.
- Provisional gameplay and durable `PROVISIONAL_IDENTITY` may precede READY_PC. Preserve the same stable Actor ID and current PLAYER binding.
- Readiness must use a coherent current-owner view; campaign HEAD alone is not all current truth. Do not ignore accepted HOT/SOFT or selected LIVE-owned scope, infer from a cache/index, or force a save merely to inspect readiness.
- Readiness output is ephemeral owner-issued evidence, not a caller/bootstrap boolean or persisted duplicate truth owner. Exact package/catalog identity and Actor state revision are part of existing S6D-07 readiness evidence semantics.
- S6D-07 evidence identity includes `actor_id`, `actor_state_revision`, `catalog_generation`, `ruleset_set_digest_generation` and `ruleset_set_sha256`; the DEV-only `evaluate_ready_pc()` conformance function is not a GAME runtime resolver.
- Mechanical reads remain within current admitted ENGINE_STATE accessors/selectors, the exact active selector/primitive consumers and their pinned-view contracts. Missing/dormant capability is a typed blocker, not an invocation-fact or query fallback.
- READY_PC does not itself set lifecycle `active`. Existing durability rules publish the accepted character frontier before it crosses a player-turn boundary; READY_PC and PLAY_READY may share one coherent launch transaction. `active` still requires confirmed READY_PC plus durable PLAY_READY.
- Re-evaluate after resume/rejoin from a fresh admitted current-owner basis. Lost unpublished HOT is not reconstructed from plausible dialogue, old chat or the last Story projection.

### Ordinary Master retrospective

- PO-001/WP-19 ordinary active-player retrospective is a normal Master interaction, not a Commentator mode transition; the question itself does not create an event, advance time or mutate truth/knowledge by fiat.
- Current native owners and native History remain authoritative. Event-time T0 evidence is distinct from mutable current T1 state; exact historical motive claims need sufficient admitted T0/evidence and otherwise remain qualified/insufficient.
- The query classes/examples in PO-001/WP-19 are consumer requirements, not a guarantee of every possible historical question or exact verbatim text after lawful compaction. Use all available admitted evidence under current owner/retention contracts; where necessary evidence is absent, provide the strongest supported semantic account or state the specific insufficiency.
- Use a bounded registered profile/purpose and role/subject/recipient basis. D&D Master is a product-facing composition, not a seventh logical role. Determine the narrowest existing role/profile binding during design; do not guess in implementation.
- Natural entity/thread/Story orientation may nominate only. Exact current/native/SemanticEvent evidence proves material claims; current PLAYER/knowledge/disclosure owners decide recipient eligibility before role-visible material is assembled.
- No broad campaign/whole-history/all-LIVE scan, generic memory/search service, caller Story-ID/content authority, legacy `visible_to`, cache-as-truth, session-meta authority, or physical-repository access outside fixed owner services.
- Story remains optional, durable noncanonical, possibly lagging and non-blocking. A read does not trigger Story catch-up/publication. A Story path is designed only if the existing native/index route cannot meet a concrete bounded discovery need without broad scans or unacceptable measured operation cost.
- PO-009’s Story-local T0 and self-contained Commentator control requirements and PO-012’s `PUBLIC + PLAYER disclosure + at-most-one selected controlled-PC known` formula remain specific to Commentator. They do not constrain ordinary Master by substitution. PO-012's multi-PC-union check remains on the separate Commentator regression surface, not ordinary Master acceptance.
- WP-24 admits no universal numerical latency, file, record, token or repository-call SLA. Structural boundedness, actual Class-B benchmark and supported-target Class-C response evaluation are separate evidence classes. Preserve the exact PO-003 zero-extra-serial **capture** law without misapplying it to every user-requested read.

### Shared protected boundaries

- Preserve one semantic owner per native value, one controlled composition boundary, domain-specific currentness and exact native revalidation.
- A composed current view is not a merged writable authority; one operation's mutations continue to route to the existing natural owner and publication boundary.
- Indexes/caches/Story/turn bundles/attestations are not independent truth, authorization, chronology or currentness owners.
- No historical Event ID, Story ID, source ordinal, commit/ref order or physical path is a fictional timeline.
- Missing/incomplete source evidence fails closed or yields the registered bounded unresolved result; omission is not semantic absence.

## 5. Relevant existing components and dependency route

The Source Manifest contains the actual owners and current consumers. The central route is:

```text
W05.T06-A1 gate/current plan + Product Owner ledger
  -> READY_PC + diegetic onboarding owners
      -> Actor / PLAYER / Asset / Effect / Rule Element / Activity / package identity
      -> current HOT/SOFT (WP-12) + campaign pin + routed selected LIVE + exact-source recovery (WP-14)
      -> pinned MechanicalContext / selector / primitive contracts (S6D-03..06)
      -> existing durability + PLAY_READY transition
  -> PO-001 + WP-19 ordinary Master retrospective
      -> Step-4 truth/knowledge/disclosure + PO-003 event-time T0 basis
      -> R2.3 registered Context profile/current eligibility
      -> RuntimeHost native History + exact EVENT enrollment + WP-11 indexes
      -> optional Story orientation (PO-009/PO-012 remain Commentator-specific)
      -> ordinary TurnEnvelope/rebinding/recipient-safe answer path
  -> RD04 / RD07 / RD09 / RD11 / RD13 / RD14 and named S6D package tests
  -> Version Impact owner
```

This is a discovery route, not a proposed dependency architecture. The design must refine it based on actual owner contracts and the whole-project critic.

## 6. Questions the architecture work must answer

### A — READY_PC / progressive readiness

1. What one trustworthy coherent current-owner read basis supports a deterministic readiness assessment while accepted onboarding facts may exist as unpublished HOT/SOFT and applicable LIVE scope, under WP-12 local owner establishment/currentness and WP-14 current-source recovery?
2. Which exact owner-issued records/results provide current Actor, PLAYER binding/control, Asset, Effect, package/definition/rules and admitted MechanicalContext/selector evidence? How are currentness, provenance, catalog/ruleset identity, revisions and transitive dependency closure verified without making the bootstrap orchestrator a new authority or broadening the exact S6D-03..06 selector/primitive set?
3. How does the existing S6D-07 typed derivation-attestation contract relate to an ephemeral runtime-issued assessment and the DEV-only `evaluate_ready_pc()` conformance tool?
4. What typed result distinguishes READY_PC, per-action local sufficiency, required dependency closure, material unresolved choices, stale/missing owner evidence and unsupported package content? Which outcomes are terminal, retryable or safe provisional continuation under existing owners?
5. How does assessment reacquire and revalidate a fresh current basis after durable resume, post-selection RuntimeHost recreation, and multiplayer rejoin/current PLAYER + controlled-PC reacquisition? The loss rule is settled: lost unpublished HOT/SOFT is not reconstructed. The open question is obtaining an accepted current HOT/SOFT basis while it survives and handling stale/moved surviving evidence.
6. How does a true assessment compose with semantic choice acceptance and the existing coherent READY_PC/PLAY_READY durability boundary, avoiding both an eager commit and a new readiness field/lifecycle owner?
7. How will concrete examples (provisional dialogue; one locally sufficient mechanic; open material choice; stale Actor revision; missing Asset/Effect/definition; package/catalog mismatch; ready but not yet durably launched; cold resume after HOT loss) distinguish the design's correctness behavior without testing or reimplementing an unadmitted mechanical primitive?

### B — ordinary Master retrospective

1. Which existing logical role/purpose/profile accepts a retrospective request, and does it require a new registered profile/purpose or only a new admitted consumer route?
2. What bounded semantic selection contract maps entity/place/thread/session/cause/motive questions to selector nominations without giving natural-language/caller refs authority?
3. Are current entity/thread/event indexes sufficient to find candidate SemanticEvents for PO-001/WP-19 query examples within existing WP-11/WP-24 bounds? The rule is settled: incomplete index proof is not semantic absence and cannot trigger a broad scan. Determine whether the exact EVENT enrollment source establishes a complete requested interval/scope, including the blank-template/current-reader discrepancy, and what bounded unresolved result applies otherwise.
4. If native indexes are insufficient, what minimum derived history-discovery data can be admitted under existing index ownership, and what exact candidates, current owner bodies and SemanticEvent facts must be re-read?
5. How do existing evidence classes map to supported query claims: current native state, exact event-time T0, typed chronology/causal evidence, selectively retained exact transcript, or eligible Story orientation? Owners already settle that current T1 cannot replace T0 and exact wording needs surviving exact evidence; determine the native route and truthful fallback when support is absent without adding retention promises.
6. How is ordinary Master recipient/player/PC disclosure/no-spoiler eligibility acquired and enforced before LLM-visible assembly without importing the Commentator-only PO-012 formula or duplicating access/knowledge/disclosure owners?
7. Apply the already-settled Story revisit trigger: does current evidence show native/index discovery cannot meet required navigation quality or responsiveness without broad scans, or that empirical use materially benefits from Story lookup? If not, keep Story navigation deferred. Only if a trigger is established, frame a read-only hint adapter that avoids Story truth/currentness, caller repository access, broad Story-state scans, Commentator-only cache reuse and physical shard coupling.
8. How does one selected LIVE origin/route participate in historical search when material, without falling back to local campaign History if the selected LIVE source is unavailable or stale?
9. What are finite outcomes for selector miss, incomplete source/index scope, exact evidence missing, current authorization failure, stale current owner, unsupported historical claim and inability to satisfy a required context floor?
10. What test vectors prove ordinary Master eligibility under existing owners, non-time-advancing reads, exact/current and T0 evidence separation, no `visible_to`/caller-ID/caller-content authority, no Story requirement, and bounded discovery under retained-history growth? Route PO-012 multi-PC-union cases to the separate Commentator regression surface.

## 7. Quality attributes and falsifiability

Decision-distinguishing qualities are correctness/currentness, no duplicate authority, disclosure safety, determinism/replay, bounded per-operation reads, responsive ordinary turns, resume correctness, fail-closed behavior and low operational complexity. Do not create numeric budgets absent an owning source.

The framing is solution-blind: a correct investigation may find existing owner APIs sufficient after deeper inspection; a native/index-only path sufficient with Story deferred; a narrowly needed index projection; or a need to revise accepted consumer/interface boundaries. It must also be able to conclude that a proposed callable/adapter/new profile is unnecessary. It must not presuppose any of these outcomes.

Representative counterexamples to preserve in later research include: a blank campaign with no admitted events; an unindexed old NPC event; incomplete event-index completion evidence; a newly accepted event past an ordinal page; concurrent campaign movement; selected LIVE history with missing routing; T0 goal changed at T1; a stale/missing knowledge/disclosure relation; an active PC with one open material initial choice; a post-ready value that is safely derivable; an unresolved choice that affects only a later advancement boundary; a player rejoining after their PC-control relation changed; a durable READY_PC that has not yet crossed PLAY_READY; and loss of unpublished HOT across a cold restart. These are representative failure vectors, not a universal exact-history guarantee; retention/exactness follows current owners.

## 8. External evidence

No external vendor or standards fact is needed to frame this block. The relevant accepted behavior, owner boundaries, failure model and current runtime code are internal HDM sources. If Step 2 discovers a material external platform/API dependency, its primary-source evidence must be added to the Source Manifest before it affects a recommendation.

## 9. Human decision and gate

```text
PRODUCT_OWNER_DECISION_REQUIRED_AT_ENTRY: NO
SYSTEM_IMPACT: REAL / BOUNDED (already ruled)
PRODUCTION_IMPLEMENTATION: HELD for A and B
T06-S1 / T06-S2: PRESERVED
T07 / T08 / W06: NOT STARTED
```

The accepted ruling settles product semantics and authorizes this design investigation. Step 1 must surface only any genuine new human-owned decision discovered by evidence; it must not re-ask settled product questions. After manifest and framing critic repairs are complete, return the package for mandatory Senior Review Stop 1. No Step 2 research/draft, implementation, or implementation-plan reconciliation begins before GO.

## 10. Step-1 exit check

- Source Manifest and item-level evidence extraction exist at the exact current source basis.
- The Brief separates established facts/constraints from open architecture questions.
- Every direct/indirect owner route that can change the framing is represented.
- A distinct whole-project critic records reconstructed dependency routes, findings and dispositions.
- Any BLOCKING/SIGNIFICANT framing defects are repaired in the brief before the stop.
- The package does not claim architecture selection, behavioral acceptance or implementation readiness.
- Mandatory Review Stop 1 is the next exact action; after GO, Step 2 is still required.
