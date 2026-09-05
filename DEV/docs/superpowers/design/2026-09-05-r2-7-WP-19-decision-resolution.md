# R2.7 WP-19 — Step 4 Decision Resolution

Status: **STEP 4 COMPLETE — TECHNICAL RESOLUTION / NO HUMAN GATE**

Date: 2026-09-05

Decision Brief:
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-decision-brief.md`.

## Resolution rule

The mandatory Step-1 Senior GO authorized Steps 2–8. `DEV/ARCHITECTURE/DESIGN_PROCESS.md` forbids manufacturing routine approval pauses when evidence and accepted decisions settle the next action. PO-001/PO-002/PO-003 already own the relevant product semantics, so this review resolves only technical composition.

| Decision | Resolution | Basis | Human decision? |
|---|---|---|---|
| D19-01 explicit selection barrier | ACCEPT | current bootstrap owners + agency/latency law | NO |
| D19-02 exact creation identity envelope | ACCEPT | Storage v3 + RUNTIME_PACKAGE + materializer contracts | NO |
| D19-03 one generated from-scratch scaffold publication | ACCEPT | new-campaign fast path + Step-5.6 publication owner | NO |
| D19-04 progressive readiness, no hard pre-live/live split | ACCEPT | WP-04 owner clarification + readiness/durability owners | NO |
| D19-05 creator/PLAYER/mode authority | ACCEPT | access/WP-16 owners | NO |
| D19-06 ordinary Master retrospective | ACCEPT | PO-001 + R2.3/Step-4/WP-18 | NO |
| D19-07 save-and-exit composition | ACCEPT | PO-002 + save/session/live/multiplayer owners | NO |
| D19-08 SemanticEvent historical decision basis | ACCEPT | PO-003 + Step-4/WP-10 sufficiency evidence | NO |
| D19-09 ordinary durability/bounded retrieval | ACCEPT | WP-13/R2.3/WP-15/WP-11 | NO |
| D19-10 zero-extra-serial latency law | ACCEPT | PO-003 amendment + PLAY_POLICY/R2.4 | NO |
| D19-11 realization/WP-20 boundary | ACCEPT | R2.7 sequencing + no implementation authorization | NO |

## Focused resolution notes

### Event-time materiality

The model may select the situation-specific *material subset* only inside an already authorized Actor/Master decision phase. This does not grant model authority over persistence or schema. Deterministic admission checks source eligibility, stable identity, value/evidence recoverability, bounded shape, provenance and no-COT constraints.

### Save-and-exit session clearing

The design must distinguish durable campaign semantics from this chat's selected-gameplay binding. Clearing a chat-local campaign working set after a confirmed save is navigation, not a durable membership/lifecycle transition. A later implementation must make that separation explicit.

### Progressive onboarding terminology

Any existing `pre-live` / `first true live scene` phrasing is treated as stale realization vocabulary. The normative distinction is `initializing` versus `active`, plus per-interaction dependency sufficiency before READY_PC.

### Physical representation

Exact PO-003 schema/index field names remain intentionally undecided at this architecture layer because the evidence supports multiple compatible physical encodings under the same logical SemanticEvent owner. Deferring the encoding preserves option value without leaving a correctness hole.

## Product Owner gate

No new requirement, material quality trade-off, lifecycle choice, compatibility policy or risk acceptance remains for the Product Owner.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

Proceed to Step 5 candidate specification.