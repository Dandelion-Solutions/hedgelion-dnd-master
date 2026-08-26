# S6D-08 Step 1 — Whole-Project Architecture Task Brief Critic

Status: **INITIAL REVIEW — FAIL — 1 BLOCKING, 2 SIGNIFICANT, 1 MINOR; RE-REVIEW REQUIRED**

Date: 2026-08-26

Authoritative review ref: `v1/engine-rearchitecture@5533e0195cde94d318b5751cb02354270db02e5a`

## Review scope

The critique reconstructed the relevant graph through `DEV/PROJECT_MAP.md` and checked the brief against the accepted Step-2 ownership/assurance route, Step-3 execution boundary, Step-5 temporal/currentness/recovery owners, House Rules, S6D-03–07 contracts, machine catalogs/schemas/tests and downstream S6D-09/S6D-11/R2.7 obligations. A routing/index statement was not treated as a substitute for an owning source.

## BLOCKING

### B1 — The eight-step loop is misnumbered and replaces the mandatory independent Step-6 review

**Brief location:** §5 items 4–8 and the paragraph following them.

The current process sequence is inconsistent with the governing design process and the completed S6D loops. It labels Step 4 “Research/architecture draft,” Step 6 “Collaborative review,” Step 7 “Adversarial review,” and omits the distinct Resolution Gate. The accepted sequence is: Step 2 Research & Architecture Draft; Step 3 Decision Brief; Step 4 Collaborative Review; Step 5 Candidate Specification/TDD realization; Step 6 independent whole-project adversarial solution review; Step 7 Resolution Gate; Step 8 canonicalization/publication. As written, the brief could let the candidate reach Step 7 without the required independent Step-6 gate and provides no explicit resolution authority before canonicalization.

**Required repair:** replace §5 with the governing sequence and corresponding artifacts. State that Step 6 is independent and must not be performed by the candidate author/reviewer acting as collaborative co-designer; Step 7 resolves every finding and records the final architecture gate; Step 8 canonicalizes only after zero unresolved BLOCKING/SIGNIFICANT findings. Update every later reference to “Steps 1, 6 and 7” so the Step-1 brief critic and Step-6 adversarial critic are mandatory, while Step 7 is the resolution gate rather than another critic.

## SIGNIFICANT

### S1 — The mandatory source manifest names owner categories instead of the exact accepted assurance/temporal/recovery artifacts

**Brief location:** §2 items 2, 4 and 6.

The brief correctly identifies the subject areas, but “accepted Step-2 mechanical-state ownership design and assurance resolutions” and “applicable accepted Step-5 contracts” are not sufficient source routes for correctness-sensitive work. The current graph contains exact superseding artifacts whose qualifiers materially constrain Effect/Condition evaluation, resumability, pending temporal work, checkpoints and orphan cleanup. Without naming them, Step 2 can accidentally rely on a historical proposal, skip a resolution amendment, or invent a recovery test path.

**Required repair:** add exact mandatory anchors, at minimum:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`, followed to every exact Resource/HP/LifeState/Effect/Condition owner and assurance resolution it routes;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` and its actual execution/resume/event/receipt tests;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` and the forward-extensible time-boundary owner decision;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` plus its resolution gate.

Require the Source Manifest to follow each anchor to actual current schemas/tests and to mark `MECHANICAL_RUNTIME_PROPOSAL.md` and other superseded derivations provenance-only. Do not invent executable test filenames when an owner provides canonical scenarios only.

### S2 — S6D-07's already accepted narrow contracts are treated only as generic predecessor debt

**Brief location:** §§2.5, 3, 4.1, 6 and 7.

S6D-07 did more than defer health/resource/effect work: it activated exact primitive/selector pairs and closed a deliberately narrow `effect.innate_sorcery` identity, one-minute TemporalBinding, same-key replacement, recovery/expiry boundary; Action Surge current-turn procedure state; Second Wind/Tactical Mind/resource consumers; and READY_PC evidence dependencies. S6D-08 owns the generic domain closure but must not silently redesign, broaden or contradict those accepted slice contracts. Conversely, their narrow activation cannot be cited as proof of generic Effect/Duration/Resource sufficiency.

**Required repair:** add an inherited S6D-07 contract ledger to the mandatory evidence products. Itemize every active S6D-07 resource/effect/health/temporal/primitive/selector dependency and classify it `accepted narrow contract`, `requires generic S6D-08 completion`, `unsupported outside exact consumer`, or `conflict requiring amendment`. Explicitly preserve the `effect.innate_sorcery` no-generic-authority boundary and Action Surge procedure-state/non-Actor-state boundary. Require bidirectional tests: generic S6D-08 machinery must realize the accepted exact cases, while unrelated Effect/Resource/temporal content remains nonselectable until independently admitted.

## MINOR

### M1 — “Recovery” is used for two different concepts without a naming rule

**Brief location:** title and §§1, 4.1–4.4, 6.

Rules recovery (rest/resource/condition/effect response) and durability recovery (retry, reload, crash/checkpoint/orphan cleanup) are both in scope. The text usually distinguishes them by context, but ledgers and failure names can become ambiguous.

**Suggested repair:** establish the terms `mechanical recovery` and `durability recovery`, and require every matrix row to identify which one applies (or both).

## Findings that pass

- Scope correctly separates mutable Actor/Effect state from declarative definitions and derived Condition aggregation.
- LifeState policy remains distinct from HP arithmetic.
- ExecutionSegment/MechanicalEvent/receipt ownership is preserved; no independent Signal/StateDelta lifecycle is introduced.
- RestPolicy is an owner-local boundary producer, not a global mutation coordinator.
- Chronology is fail-closed against background scheduling, global scans and a general event queue.
- House Rules are routed as typed authority, not prose mutation.
- Supported breadth is bounded by the S6D-07 profile and additional minimal proof cases; coverage is not activation.
- Downstream S6D-09, S6D-11 and R2.7 consistency checks and the stop-before-S6D-09 boundary are explicit.

## Verdict

**FAIL — 1 BLOCKING, 2 SIGNIFICANT remain.** Repair the process sequence, exact source routes and S6D-07 inherited-contract framing, then rerun the whole-project Step-1 gate. No Step-2 work is authorized by this critic.

---

## Re-review after Step-1 repairs

Status: **PASS — 0 BLOCKING, 0 SIGNIFICANT**

The current brief closes every prior finding without introducing a new authority or scope regression:

- §5 now follows the governing eight-step loop exactly: Step 2 research/architecture draft, Step 3 decision, Step 4 collaborative review, Step 5 candidate/TDD realization, independent Step 6 adversarial review, Step 7 Resolution Gate and Step 8 canonicalization/publication. Independence and zero-unresolved-finding rules are explicit.
- §2 names the exact Step-1/2 assurance, Step-3, Step-5.2v2, Step-5.3 temporal continuity/integration, Step-5.7 checkpoint, Step-5.9 chronology and Step-5.13 GC canonical/resolution anchors. It requires following them to actual schemas/tests/scenarios and marks superseded proposals provenance-only.
- §§3–4 add the inherited S6D-07 ledger and preserve the exact narrow Innate Sorcery Effect/TemporalBinding/reapplication/expiry contract, Action Surge procedure-state boundary, and reviewed consumer-limited resource/selector/primitive authority. The bidirectional proof prevents narrow accepted cases from being lost while forbidding their use as generic S6D-08 activation evidence.
- §1 distinguishes mechanical recovery from durability recovery and requires every matrix row to identify the applicable meaning.

The remainder of the brief continues to preserve Actor/LifeState/Effect/Condition ownership, ExecutionSegment/Event/receipt authority, owner-local RestPolicy response, scan-free chronology, House-Rules typed authority, bounded S6D-07 content scope and downstream S6D-09/S6D-11/R2.7 consistency.

## Final Step-1 verdict

**PASS — 0 BLOCKING, 0 SIGNIFICANT.** The repaired brief is fit for Step-1 publication and read-back. This verdict does not authorize Step-2 work before the Step-1 publication/status gate is completed.

