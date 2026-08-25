# Canonical Architecture Index — Campaign House Rules Addendum

Status: **DERIVATIVE / NON-NORMATIVE NAVIGATION ADDENDUM**

Date: 2026-08-25

This addendum extends `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` for the House Rules design closure without rewriting the older Steps-1–5 navigation index.

It creates no semantic authority. Primary owning sources always win.

---

## Campaign House Rules / established Rulings

**Architecture status:** CANONICAL / CLOSED.

Primary owner:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

Design-cycle evidence:

- Step 1 — `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
- Step 2 — `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`
- Step 3 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief.md`
- Step 4 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review.md`
- Step 5 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec.md`
- Step 6 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review.md`
- Step 7 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate.md`
- Step 8 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization.md`

Runtime-facing campaign policy surface:

- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

### Locator summary

| Concern | Primary owner / inherited owner |
|---|---|
| Campaign semantic game-rule/adjudication policy | `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` |
| Truth/knowledge/disclosure + role context | Step-4 canonical spec + 2026-08-23 single-context containment amendment |
| Bounded retrieval/currentness/eligibility | `2026-08-24-r2-3-context-runtime-canonical-spec.md` |
| One-context role rebinding + instruction/data fencing | `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` |
| Campaign publication/CAS | Step 5.6 canonical spec |
| Recovery / accepted frozen inputs | Step 5.7 canonical spec |
| Multiplayer live/currentness | Step 5.8 canonical spec + R2.5 canonical spec |
| Deterministic mechanical execution | Activity / Rule Element / Step-3 execution owners |

### Integrated invariant summary

```text
LLM semantic applicability
    != deterministic execution authority

current published campaign policy
    != local file existence / remembered chat

physical context presence
    != role/consumer information eligibility

policy prose
    != system/engine instruction tier

new affected Resolution
    -> current policy basis required before acceptance

accepted Resolution generation
    -> frozen historical policy basis survives later publication

multiplayer propagation
    = authoritative publication/currentness + bounded context assembly
    != copying Markdown among chats
```

No House-Rules-specific global frontier/synchronization subsystem exists.

### Residual navigation debt

R2.3 canonical semantics are owned by:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`.

The convenience path `DEV/ARCHITECTURE/CONTEXT_RUNTIME.md` named in some planning material is absent at the House-Rules canonicalization HEAD. Treat this as nonblocking navigation/documentation debt, not as missing House-Rules semantics.
