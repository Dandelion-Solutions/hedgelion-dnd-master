# HDM Implementation Planning — Independent Senior Review Brief

Status: READY FOR GENUINELY INDEPENDENT SENIOR PLAN REVIEW
Author package head at brief creation: `e33d0ad2a1d735a114cdfaf39c50decc3f9279af`.
Production implementation authorized: NO.

## Reviewer role

Act as independent HDM Senior Plan Reviewer. Do not repair the author package while reviewing. Recompute material claims from authoritative repository sources. Author coverage/closure documents are evidence to challenge, not authority.

The review must be rigorous **and context-efficient**. Do not load the whole repository or recursively follow every cross-reference. Build the smallest evidence subgraph that can prove or disprove the package claims, and expand it only when a concrete uncertainty, contradiction, drift signal or finding requires more source evidence.

## Hard context-budget policy

Treat context as a scarce review resource.

1. **Never bulk-read the project.** Do not recursively open directories, all architecture docs, all GAME files, all historical audits or all source manifests “for completeness”.
2. **Use `DEV/PROJECT_MAP.md` as a router, not as an instruction to load every linked artifact.** Follow only edges required by the current review question.
3. **Prefer exact-path and exact-ID retrieval.** For large specs/ledgers, retrieve only the sections for the readiness IDs, owner claims, dependencies or findings currently being checked when the connector/runtime supports bounded reads.
4. **Do not keep provenance documents in the mandatory working set.** PB source manifests, PB closure documents, older candidates, repair overlays and earlier critic rounds are escalation evidence only unless a discrepancy requires them.
5. **Do not read semantic/runtime/persistence owners merely because they exist.** Open a current owner only when:
   - the canonical readiness ledger/spec and the plan disagree or are ambiguous;
   - a plan appears to invent/transfer authority;
   - currentness comparison shows that owner changed after authoring;
   - an E1-E15 dependency cannot be validated from the accepted decomposition/package;
   - a suspected finding needs primary-owner confirmation.
6. **Do not inspect runtime release packages** unless a concrete finding concerns packaging, compatibility, installation or release validation.
7. **Do not inspect GAME/runtime implementation bodies** merely to understand planned semantics. For file-action validation, first verify path/existence/classification. Read file contents only when the plan’s claim depends on current contents.
8. **Do not use external/web research** for this review unless a current HDM owner explicitly makes an external mutable fact material to a finding.
9. **Escalate evidence incrementally.** One unresolved question -> the smallest next authoritative artifact/excerpt. Never respond to one uncertainty by loading an entire subsystem corpus.
10. **Stop expanding a branch once the review claim is proved or disproved.** Additional corroboration is not useful if it cannot change the verdict or severity.

A good working-set target for any single question is:

```text
current control/gate
+ current RD plan or integration artifact
+ exact readiness/spec/ledger excerpt
+ at most the directly implicated owner artifact(s)
```

This is a review discipline, not a weakening of evidence requirements. If a material claim genuinely requires broader evidence, load it and record why the escalation was necessary.

## Fresh bootstrap — minimal form

Use GitHub Connector authoritative remote state only.

Bootstrap in this order:

1. fresh-check branch `v1/engine-rearchitecture` HEAD;
2. read the current review/gate state from `DEV/CURRENT_PROGRESS.md`;
3. read the current `AGENTS.md` sections governing authority hierarchy, fresh bootstrap, review independence, publication/write guardrails and skill/runtime selection; do not load unrelated sections if bounded retrieval is available;
4. read the applicable runtime overlay sections needed for GitHub transport/publication/verification;
5. use required Superpowers/review discipline and specialist skills only where their declared scope is relevant;
6. use `DEV/PROJECT_MAP.md` only to resolve paths/owners when an exact path is not already supplied by this brief;
7. read broader design/process documents only if the current gate or a disputed process claim actually depends on them.

Do not perform a generic architecture bootstrap that loads the whole architecture corpus. This task is an independent review of an already-authored implementation-planning package, not a new architecture-design session.

## Review corpus — staged, not bulk

### Tier 0 — always load

These define the review gate and current package surface:

1. `DEV/CURRENT_PROGRESS.md`.
2. this brief.
3. critic-approved `DEV/docs/superpowers/design/2026-09-13-implementation-planning-candidate-bounded-decomposition-v2.md`.
4. final decomposition critic PASS result referenced by current progress/package control.
5. `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-package-conventions.md`.
6. `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-package-impact-tdd-contract.md`.
7. package master/index.
8. `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-execution-waves.md`.
9. `DEV/docs/superpowers/plans/2026-09-13-implementation-planning-bidirectional-coverage.md`.

Where a Tier-0 document is large, read its relevant sections in bounded chunks rather than loading the entire file in one call when the connector permits.

### Tier 1 — canonical readiness evidence, queried by need

Use the WP-27 final readiness spec and Step-2 evidence ledger as canonical leaf-level evidence, but **do not sequentially ingest the entire ledger unless bounded exact-ID retrieval is unavailable**.

Start by extracting/reconfirming only:

- exact active set and counts;
- 12 trigger-gated identities;
- 79 no-work terminals;
- absent R004;
- direct/pure-proof/composite classification;
- exact records for any readiness IDs currently under review.

When auditing a plan or finding, retrieve that plan’s readiness IDs from the ledger/spec on demand.

### Tier 2 — executable plans, reviewed sequentially

Review all RD-01..RD-14 plans, but do not load all fourteen into context at once.

Process one RD (or one tightly coupled join) at a time:

```text
RD plan
-> its direct readiness IDs / composite slices from Tier 1
-> relevant package conventions / Impact-TDD rule
-> only if needed, exact semantic owner evidence
-> record compact review result
-> move to next RD
```

For each RD retain only a compact audit note: readiness/slices, file-action concerns, dependency concerns, TDD/verification concerns, owner/authority concerns, unresolved evidence needs and finding IDs.

### Tier 3 — provenance / owner escalation only

Open these only when a Tier-0/1/2 check creates a concrete reason:

- PB-02..PB-05 source manifests and closure docs;
- earlier decomposition candidates/repair overlays/critic rounds;
- current semantic/runtime/persistence/version owner documents;
- current GAME/schema/tool bodies;
- HG-01 research details;
- historical roadmap/audit material.

Record the reason for every Tier-3 escalation in the review notes/result so expensive context has an explicit causal purpose.

## Review workflow

Perform the review in this order because it maximizes evidence value per token.

### Phase 1 — currentness first

Fresh-compare the author package/review baseline to review HEAD before deep reading.

- If changes are planning/control-only, record `NO_SEMANTIC_OWNER_DRIFT` and do not reread unaffected owners.
- If canonical readiness/decomposition/semantic/runtime/persistence/version owners changed, identify exactly which changed files/owners can affect the package and load only that dependency subgraph.
- If material drift invalidates the package globally, stop deep review and issue the appropriate finding rather than auditing a stale package exhaustively.

### Phase 2 — canonical accounting

Independently reconstruct active 133, trigger-gated 12, no-work 79 and absent R004. Verify active set partitions exactly into 116 direct + 9 pure proof + 8 composite parents with no overlap/missing/extra identity.

This phase should rely primarily on WP-27 canonical readiness evidence plus decomposition v2, not on author coverage claims.

### Phase 3 — leaf/slice fidelity and plan quality

For every active readiness identity, verify its planning route. Do this by walking RD plans sequentially against exact Tier-1 records rather than loading the complete ledger and all plans together.

Verify exact owner/disposition/qualifiers/negative laws/scenarios/defer-revisit semantics where they are material to execution planning. Composite slices must preserve parent semantics without becoming new readiness IDs.

Pay special attention to author-repaired PB-05 routes:

- RD-12: `R016.COLLAB`, `R018.COLLAB`, `R122.COLLABORATION_BRIDGE`;
- RD-13: `R016.STORY`, `R018.STORY`, `R062.SEMANTIC_EVENT_HISTORY`, `R087.SEMANTIC_EVENT_T0`;
- RD-14: `R029.ONBOARDING`, `R087.SAVE_SESSION_MENU`.

For every RD plan check:

- exact file actions and owner boundaries;
- bounded worker tasks;
- TDD RED/GREEN/REFACTOR/VERIFY;
- Impact Envelope;
- negative-law tests;
- Version Impact/schema/catalog/checkpoint/migration/HG-01 handling where applicable;
- coherent commit boundaries;
- currentness fence;
- no conditional architecture/design choice improperly delegated to implementation workers.

Do not inspect target file bodies unless a file-action/owner claim cannot be validated without them.

### Phase 4 — dependency graph / execution waves

Independently recompute/validate owner-derived E1-E15 from decomposition v2 plus only the exact owner evidence needed for disputed edges.

Verify PB-06 neither serializes independent owners unnecessarily nor closes joins too early. Specifically test:

- RD-11/RD-12 cycle handling;
- R124;
- R122;
- R029;
- R062;
- R087;
- selected-LIVE recovery;
- protected emission;
- T0/Commentator;
- save-and-exit;
- creator fail-closed joins.

Do not reread every owner behind every valid edge. Escalate only edges that are ambiguous, contradictory or high-risk after decomposition/plan comparison.

### Phase 5 — reverse coverage

Inspect implementation/proof/integration tasks in the plans and waves. Every task must trace to an admitted readiness leaf/slice, required owner integration, proof route, Version Impact projection or required test/audit evidence.

Report orphan work or architecture invention. PB source manifests are not needed unless an orphan/ownership dispute requires provenance.

### Phase 6 — protected-invariant adversarial pass

Adversarially check:

- no second gameplay/knowledge/history/currentness authority;
- eligibility before semantic use;
- optional ranking cannot override authority/eligibility/requiredness;
- TurnEnvelope control is not authority;
- physical presence is not eligibility;
- late steering is non-authoritative;
- only validated Narrator payload crosses `EMISSION_COMMIT`;
- no global active player;
- positive dependency before waiting;
- scope-local waiting;
- join/rejoin current frontier before mutation;
- catch-up is recipient projection;
- Story is noncanonical;
- T0 is not parallel history;
- Context Runtime is ephemeral.

Use targeted owner escalation only if the package/decomposition evidence leaves an invariant genuinely uncertain.

## Context-escalation stop rules

Do **not** broaden the corpus merely because:

- a document links to another document;
- an RD touches the same subsystem as historical work;
- a source manifest lists additional evidence;
- an old critic mentioned a now-resolved issue;
- a file exists under GAME/DEV;
- another owner could provide redundant confirmation.

Broaden only for one of these explicit reasons:

```text
DRIFT
DISAGREEMENT
AMBIGUITY
AUTHORITY_TRANSFER_RISK
UNTRACEABLE_TASK
UNPROVEN_DEPENDENCY
FILE_ACTION_DEPENDS_ON_CURRENT_BODY
FINDING_CONFIRMATION
```

If none applies, do not load more context.

## Finding severity / verdict

Report itemized `BLOCKING`, `SIGNIFICANT`, `MINOR` findings with exact source/plan evidence and affected readiness/tasks. Do not silently repair.

Final verdict must be exactly one:

- `PASS / GO FOR PRODUCTION IMPLEMENTATION PLANNING GATE` only if no unresolved blocking/significant defect and package is execution-ready;
- `FAIL / REPAIR REQUIRED` otherwise.

Even on PASS, this review authorizes the next repository gate only; it does not itself execute production implementation, migration, release or gameplay bootstrap.

## Expected result artifact

Publish an independent review result under `DEV/docs/superpowers/plans/` (or the current repository-mandated review location if owners changed), recording:

- reviewed HEAD and author-package baseline;
- currentness result and any targeted drift subgraph loaded;
- independent canonical accounting;
- RD-by-RD compact review status;
- E1-E15/dependency result;
- reverse-coverage result;
- every Tier-3 escalation and why it was needed;
- findings and severity;
- final verdict;
- exact next authorized unit.

Update `DEV/CURRENT_PROGRESS.md` only according to the resulting gate and repository process.

## Review completion condition

The review is complete when every required claim above has been proved or disproved with the smallest sufficient authoritative evidence set. **Reading more repository material is not a completion criterion.** Evidence sufficiency, traceability, currentness and independence are.