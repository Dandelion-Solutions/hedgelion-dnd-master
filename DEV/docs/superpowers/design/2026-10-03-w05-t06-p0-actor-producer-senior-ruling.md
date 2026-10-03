# W05.T06-P0 Actor Producer — Bounded Senior System-Impact Ruling

Status: **GO — REVISED P0 ENVELOPE AUTHORIZED**
Date: 2026-10-03
Reviewed remote HEAD: `29ee6bcb5fa7180ba5c1d940b17c19dc9e685253`
Process: DEV/DEVELOPMENT_EXECUTION_PROCESS.md §§6–7; bounded review of implementation allocation, not a new architecture loop.

## Disposition

SP06-02 source-capability finding is CONFIRMED. The previous review mistook an
owner-local transformation for an existing connected accepted producer.
`apply_actor_delta` and synthetic RD03 evidence alone cannot authorize HOT.

R2.2/R2.3/R2.4 and WP12 already settle a bounded native Actor assessment ->
deterministic validation -> local SOFT establishment. A separate product/owner
decision is not required to implement that accepted path. **P0 GO** is restored
only for the concrete self-state reconsideration join now specified in the
stable Wave-05 plan. Broader evidence classes are not authorized by this ruling.

No production change or producer acceptance is claimed here. P0's output
remains unproduced pending TDD, independent task review and required verification.

## Bounded dependency graph and Source Manifest

All sources below were Connector-read at the reviewed HEAD. Indexes were used
for discovery only; private Lab and release packages were not inspected.

| Source / role | Extracted evidence / qualifier | Consequence |
|---|---|---|
| AGENTS.md; CHATGPT_WORK overlay; DEV/DESIGN_PROCESS.md; DEV/ARCHITECTURE/DESIGN_PROCESS.md; DEVELOPMENT_EXECUTION_PROCESS §§6–7 — process owners | Derivable realization and envelope repair are Senior work; real owner/authority changes return to design | This ruling authorizes implementation of accepted semantics only |
| DEV/PROJECT_MAP.md; implementation-plan-index; current progress + Wave-05 cursor — routing/scheduling | P0 held; downstream P1A/P1B/P2/P3 gated | Synchronize current route; preserve downstream gates |
| R2.2 canonical spec Laws 13–17,20–21 — semantic owner | Material reconsideration cue/current-state conflict is a legitimate sparse trigger; one Actor/purpose/bounded eligible state; deterministic source/revision/agency validation; NO_CHANGE writes nothing | Exact own current cue is sufficient for the bounded witness; no made-up external event required |
| ACTOR_MODEL §§7,8,11 — semantic owner | Actor owns sparse evolving continuity and cues; PC agency/control separate; accepted SOFT may precede Git durability | Self-state evidence changes intention only, not truth/knowledge |
| R2.3 canonical spec Laws 11–12; R2.4 Laws 14,17–20; WP08-3/4; WP09-5 — context/phase owners | Currentness and subject eligibility before role evidence; phase handoff is minimum scoped proposal, not semantic acceptance | Consume issued phase/basis; exact native revalidation still required |
| WP12 Laws 6–9,15–16,22–25 — local/currentness/recovery owner | Local establishment only for admitted native edge; no external transaction; LIVE pre-CAS not current; cold survival not authority | Local producer fails closed on LIVE selection; read/adoption plumbing preserves LIVE-first rules |
| T06-A1 §§2–4,17–20 — accepted composition owner | CurrentOwnerView read-only; HOT accepted-owner observation; no extra LLM/publication edge | Fixed native join composed by RuntimeHost |
| WP18-3/9/17; history.py T0 validation — owner/implementation | Story/planning/history cannot establish current Actor intentions; T0 is historical evidence | No Story, CLS or historical-basis shortcut |
| actor_continuity.py — implementation | Validator consumes caller booleans; after-image increments native revision, PC role rejected; reduced mapping is not full envelope | Keep native transformation; trusted caller derives checks and preserves wrapper |
| All current GAME/TOOLS/*.py from exact recursive tree — implementation/callsite census | Only actor_continuity.py defines/references assess_actor/apply_actor_delta | Absence of connected production caller confirmed for this bounded directory |
| turn_runtime.py; context_runtime.py; runtime_host.py; bootstrap.py; hot_store.py — implementation | Existing issued AcceptedContextBasis/AcceptedPhaseResult and Host Context service; pure structural HOT staging; repository-backed Context | Reuse existing provenance machinery; implement producer/current-owner join, no generic issuer |
| RD03 test + Actor assessment/delta schemas; world-actor-state schema — machine/tests | Synthetic accepted/current fixture proves transformation only; explicit assessment purpose and revision already required | Test production path, retain unit coverage |
| GAME/SCHEMA/actor.schema.yaml; DEV/SCHEMAS/world-record.schema.json — strict machine envelopes | Native envelope omits/rejects state_revision while transformation requires it | Move existing SP06-10 alignment from P1A to P0 before the witness |
| Prior final Senior review + source brief + repair resolution — provenance | Earlier GO did not discharge connected producer evidence | Retain history, explicitly supersede source-witness assumption |
| PRODUCT_OWNER_INPUT applicable PO-001/003/005/008 and separate PO-009/012 routes — requirements | Ordinary Master/native continuity distinct from Commentator; access/failure laws preserved | No new PO choice; no private dependency |
| VERSIONING.md + detailed namespace policy — version owners | Actual material serialized/runtime changes need owning bumps; planning provenance owns no numbered namespace | This checkpoint NONE; P0 schema realization must classify/synchronize |

Graph:
`native NPC current Actor/cue -> Host CurrentOwnerView -> Context ACTOR basis
-> TurnRuntime issued proposal -> native Actor validation -> WP12 local atomic
establishment -> admitted HOT -> fresh Context`.
RuntimeHost composes dependencies; Actor remains semantic owner. Access and
selected LIVE/currentness constrain every applicable edge. SAVE/recovery consume
accepted owners; P1A consumes the P0 Actor revision envelope.

## Senior allocation and scope

The stable Wave-05 P0 section is the sole executable plan. It now specifies:
one fixed internal Actor phase-consumption service; own exact current NPC cue
with assessment.reconsider; issued same-Host/current-phase provenance; exact
predecessor/source/eligibility revalidation; internally derived transformation
evidence; validated full envelope; atomic local admission and repeat consumption;
NO_CHANGE; typed rejection of unsupported sources and LIVE mutation.

An accepted phase seal does not certify evidence truth or accept the semantic
write. Role Context contains only eligible proposal inputs; deterministic Actor
code validates native semantics and the local transaction establishes the result.
No universal boolean-to-authority adapter is allowed.

SP06-10 revision alignment moves to P0 because P0 cannot test a real strict
Actor after-image without it. No second revision axis, guessed missing revision,
migration or automatic catalog/campaign-generation bump is admitted. The actual
schema/projection bump belongs to implementation's Version Impact Gate. P1A
consumes GREEN P0 and must not repeat the logical bump.

## Challenge / completeness checks

- Existing-owner sufficiency: current self reconsideration is expressly admitted;
  generic external event-evidence issuance is unnecessary for this witness.
- Trust: phase carrier alone is insufficient; exact current native predecessor,
  cue membership and applicable subject/write authority remain required.
- Concurrency: operation basis and predecessor compare before local establishment;
  related movement fails boundedly. No network/model operation inside SQLite.
- Retry: consumed issued result cannot apply twice; bookkeeping and row admission
  advance together. NO_CHANGE and failed establishment create no state advance.
- Recovery: consumption/admission markers are process-local; cold restart
  recovers compatible durable source, not surviving dirty bytes.
- LIVE: local join cannot stage a live-owned prospective mutation; post-CAS
  adoption remains independently evidenced.
- Privacy/agency: one NPC's own continuity; no private-role transport to Narrator,
  PC voluntary-state authorship or external knowledge laundering.
- Performance: finite same-subject reads/validation only for material assessment;
  no additional mandatory physical model invocation, scan, scheduler or save.
  No measured latency claim.
- Indirect consumers: full wrapper/schema preservation, selected Host composition,
  Context fresh reads, SAVE generation clearing, P1A revision dependency and
  downstream task gates remain covered by required P0 verification.

Rejected alternatives: pretending RD03 fixtures are production evidence;
introducing a generic evidence issuer; deferring the entire accepted Actor
semantics to a new product decision; placing revision alignment after its first
consumer. These either fail the trust boundary or add unnecessary scope.

## Verification and continuation

Fresh source/callsite/envelope checks support this review. Prepared-document
checks verify references, synchronized current statuses, producer scope and
P0/P1A ownership transfer before publication. No local production tests,
maintenance PASS or hosted-CI PASS is inferred from the worker's report; that
report's 21 focused checks, timeout and contaminated-workspace audit apply only
to its recorded execution surface. Source-checkpoint hosted workflow 37063174902 at exact reviewed HEAD completed
successfully (fresh Connector read); this does not prove the not-yet-implemented
producer. Exact new published-head CI is checked separately.

```text
SENIOR_SYSTEM_IMPACT_RULING: GO / ACCEPTED-ARCHITECTURE REALIZATION
SP06_02: RESOLVED IN PLAN; PRODUCTION PROOF PENDING P0
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
NEXT_EXACT_TASK: implementation worker W05.T06-P0 under revised stable Envelope
W05_T06_CURRENT_OWNER_VIEW_READY: NOT YET PRODUCED
P1A/P1B/P2/P3: DEPENDENCY-GATED
T06 S1/S2 AND T06-A1: PRESERVED
STORY: DORMANT
PRODUCTION_CODE_CHANGED: NO
VERSION_IMPACT: NONE — no versioned semantic/machine/runtime owner changes; implementation allocation and review/status only
UNPUBLISHED_WORK: NONE after successful publication/read-back
```
