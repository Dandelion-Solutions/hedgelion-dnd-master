# Step 5.11 — Selective Exact / Semantic Continuity — Owner Decision

Status: **OWNER-APPROVED PRODUCT / ARCHITECTURE DECISION**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Decision context:

- `2026-08-21-step-5-11-transcript-history-retention-compaction-task-brief.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-research-draft.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-analytical-challenge.md`
- `2026-08-21-step-5-11-transcript-history-retention-compaction-decision-brief.md`

## Decision

The owner selects:

> **S — SELECTIVE EXACT / SEMANTIC CONTINUITY**

Baseline HDM does **not** promise to act as a permanent verbatim recorder of every arbitrary historical conversation item.

Baseline HDM **does** promise durable semantic continuity of materially established campaign history and durable exact wording wherever exact wording is materially protected by gameplay/canonical semantics or deliberately retained by an applicable historical/presentation policy.

If exact wording is no longer retained, HDM must say so and use the strongest surviving semantic evidence. It must not reconstruct plausible wording and present it as a verbatim quote.

## Product rationale

Owner rationale:

> The Master is living and conversational. It may have excellent, effectively permanent memory in the human sense, but it is not a tape recorder.

Architectural interpretation:

```text
excellent durable memory
    = established world/state/history meaning remains available
      through its proper owners and bounded historical evidence

verbatim recall
    = a separate retained capability
      present only where exact form is protected or deliberately archived
```

This distinction is intentional product semantics, not a storage accident.

## Baseline exactness promise

Exact or exact-equivalent wording must survive when material semantics require it, including examples such as:

- wording whose exact form affects adjudication;
- contract/oath/bargain terms where exact terms remain material;
- passwords/passphrases;
- riddles, inscriptions, codes, poems or clues whose form is part of the game object;
- player-authored in-fiction documents where the document text itself is established content;
- a historical quote explicitly promoted into a durable exact-evidence dependency;
- another owner-defined exact-text requirement.

Exact wording is **not** guaranteed forever merely because a line once appeared in the host conversation. Examples that may lawfully lose verbatim form when no retained policy/dependency protects them include:

- ordinary flavor banter;
- mundane action-declaration phrasing after accepted intent/semantic consequences are durably represented;
- routine Narrator prose;
- ordinary OOC rules chatter;
- arbitrary old host messages with no retained exact-text obligation.

## Semantic continuity promise

Loss of non-protected exact prose must not imply loss of materially established campaign memory.

Where relevant, the proper durable owners continue to preserve meaning, for example:

```text
world/current owner
world.contract / world.asset document / lore owner
world.knowledge
runtime.disclosure
runtime.semantic_event / LOG
runtime.mechanical_event / receipts
runtime.interaction / compact message provenance
Story records where deliberately retained
```

No transcript/read-model record becomes objective truth authority merely because it is the last surviving textual copy.

## Irreversible consequence accepted by owner

The owner explicitly accepts that under this baseline a future historical request may lawfully receive:

```text
"The exact wording is no longer retained. The surviving evidence establishes that ..."
```

rather than an exact quotation.

This is an intended product boundary, not a recovery failure, provided the deleted wording was not protected by a correctness or explicit retention obligation.

## Rejected stronger baseline

The owner does not select a baseline promise of broad qualified long-term exact Transcript for ordinary player-facing discourse.

HDM may still retain selected `STORY/TRANSCRIPT` material for dialogue fidelity, reconstruction, Story quality or explicit historical value. Such retention does not upgrade the global product promise to "all gameplay conversation is permanently verbatim recoverable."

A future product extension may broaden prospective archival policy without changing the meaning of older evidence. It must not invent exact text for historical periods where exact payload was already lawfully compacted.

## Design consequences for Step 5.11

The agent now owns mechanical formalization of at least:

1. `runtime.message` historical/evidence semantics;
2. exactness definition for accepted text;
3. exact-text protection ownership and bounded discovery;
4. semantic/provenance survivor requirements;
5. raw-payload compaction eligibility;
6. Story/Transcript optional archival and required transfer cases;
7. correction/retraction/host-edit semantics;
8. source-enumeration/cursor continuity;
9. multiplayer visibility separation;
10. 5.12 delivery and 5.13 physical-GC handoffs;
11. migration/integrity behavior when historical exact text is unavailable;
12. adversarial/regression requirements.

No further owner decision is required unless candidate/adversarial review exposes a materially different product promise or irreversible trade-off.
