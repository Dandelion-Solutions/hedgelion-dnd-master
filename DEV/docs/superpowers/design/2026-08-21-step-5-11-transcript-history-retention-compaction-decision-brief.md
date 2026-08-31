# Step 5.11 — Transcript / History Retention & Compaction — Decision Brief

Status: **OWNER DECISION REQUIRED — STEP 5.11 REMAINS OPEN**

Date: 2026-08-21

Basis:

- Step-5.11 task brief;
- Step-5.11 research draft;
- Step-5.11 analytical challenge;
- canonical Steps 3, 4 and 5.1–5.10;
- current runtime/catalog/schema audit;
- current official ChatGPT platform research.

---

# 1. Decision requested

Choose the baseline **historical exact-text promise** HDM makes when no active gameplay/canonical correctness dependency independently requires exact wording.

This is a product/architecture decision because deletion is irreversible and changes what users can expect the engine to remember exactly years later.

It is **not** a choice about schema fields, file sharding, hash algorithm, cursor representation or compaction implementation. Those follow mechanically after the semantic promise is fixed.

---

# 2. Fixed facts regardless of choice

The following do not depend on the owner decision:

1. visible ChatGPT history is not immutable campaign authority;
2. host messages can be edited, assistant responses retried, conversations branched and chats deleted;
3. Project/chat memory is not exact durable campaign storage;
4. Step 3 already owns accepted external exchange identity through `runtime.interaction` and raw message linkage;
5. `runtime.message` is already admitted with campaign-scoped stable identity but lacks finalized structure;
6. exactness for normal text means exact text accepted by the HDM runtime, not raw UI/HTTP bytes;
7. ChatGPT Voice transcript is not a guaranteed verbatim audio record;
8. transcript text does not prove the claims inside it are objectively true;
9. message/source order does not become fictional chronology;
10. correctness-critical exact wording must remain protected or be promoted to a proper semantic/historical owner;
11. SemanticEvents remain compact semantic history, not exact transcript;
12. Story may be the last exact copy for historical/presentation purposes without becoming objective truth authority;
13. no LLM importance judgment may by itself authorize irreversible deletion;
14. compaction eligibility must be bounded and typed;
15. physical cross-artifact GC remains Step 5.13;
16. exact outbound host delivery qualification remains Step 5.12;
17. stable host Retry/edit revision identity feasibility remains a Step-6 deployment concern.

---

# 3. Recommended choice — S: Selective Exact / Semantic Continuity

## Promise

> **HDM guarantees exact wording when exact wording is materially protected by gameplay/canonical semantics, and may retain selected qualified Transcript material for historical quality. HDM does not promise verbatim recovery of every arbitrary old message forever. If exact wording was not protected/retained and is gone, HDM reports that fact and uses surviving semantic evidence without inventing a quote.**

### Practical examples

Guaranteed exact or exact-equivalent owner protection:

```text
Wish-like wording that affects adjudication
contract/oath exact terms
password/passphrase
riddle/inscription/code
player-authored in-fiction document
exact quote deliberately made a durable evidence dependency
```

Not universally guaranteed forever:

```text
ordinary flavor banter
mundane action declaration wording
routine Narrator prose
ordinary OOC rules chatter
arbitrary old host message with no retained/protected exact dependency
```

Story/Transcript can still retain valuable dialogue exactly. The guarantee is simply not “every line forever.”

## Why this is recommended

### A. It matches existing HDM behavior

Current `SESSION.md` already says that when an exact old utterance is not available, HDM should use durable semantic evidence and summarize rather than fabricate a quote.

Current `DIALOGUE.md` says to persist socially consequential dialogue facts rather than archive every casual line into permanent state.

Choosing S formalizes the existing product posture rather than silently expanding it.

### B. It best matches necessary-and-sufficient persistence

Correctness keeps exactly the text it actually needs.

Long-lived exact semantic objects move into their natural owner instead of keeping the original chat message forever merely as a container.

### C. It minimizes irreversible data retention

Campaign repositories do not automatically accumulate every piece of player-authored/OOC text forever.

This matters even if raw storage bytes are cheap: retention itself is a product/privacy promise.

### D. It avoids transcript machinery on every ordinary turn

A normal mundane message does not require a permanent exact Story materialization or an LLM classification merely to remain correct.

### E. It is forward-extensible

HDM can later broaden archival policy prospectively if users demonstrate strong demand.

The reverse decision is harder: after promising/storing everything forever, reducing retention changes user expectations and does not undo already accumulated data.

---

# 4. Strongest alternative — B: Broad Qualified Long-Term Transcript

## Promise

> **HDM normally preserves an exact long-term `STORY/TRANSCRIPT` archive of a defined class of player-facing gameplay discourse even when exact wording has no active correctness dependency.**

This is not necessarily every host token. A plausible qualified set could include:

- accepted gameplay player messages;
- delivered player-facing Narrator/NPC responses;
- or a narrower defined in-fiction discourse subset.

Exact qualification would be formalized after the owner chooses this product direction.

## Strengths

### A. Better campaign-memory experience

Late questions such as:

```text
“What exactly did the witch say?”
“Did I promise to return it or merely say I would try?”
“What joke did we make in session three?”
```

are far more likely to have exact answers.

### B. Better Chronicler/Commentator source fidelity

Long-term retrospective storytelling has richer primary material.

### C. Protects against unanticipated future importance

A line that looked mundane when spoken may later become significant.

Broad archival avoids most irreversible regret in this class.

### D. Raw runtime payload still need not live forever

The design can copy qualified exact text into Story, verify the copy, then compact the raw `runtime.message` payload to a provenance envelope.

So B does **not** require duplicate permanent raw + Story copies.

## Costs

### A. Stronger permanent data-retention promise

More player-authored text lives in campaign storage for the long term.

### B. More storage/files/history churn

Step 4's sharding helps bounded access, but campaign size remains proportional to conversation volume.

### C. Qualification becomes architecture

If the promise is “in-fiction discourse,” the engine must distinguish exact spoken text from action gist/paraphrase.

If instead the promise is “whole player-facing gameplay messages,” implementation is simpler but archives more OOC/action/narrative text.

### D. Delivery boundary becomes part of completeness

Outbound Transcript cannot be complete until Step 5.12 can establish what was actually emitted/delivered rather than merely generated.

### E. Legacy campaigns cannot satisfy the promise retroactively

Old exact text that was never durably retained cannot be recreated honestly.

---

# 5. Rejected baselines

## Full host-visible archive

Retain all visible user/assistant messages exactly forever.

Rejected recommendation because it over-retains OOC/meta/narrative material and is broader than any current HDM requirement.

## TTL/rolling exact window

Rejected as semantic authority because age does not determine whether wording remains important.

## SemanticEvents only

Rejected because exact wording is sometimes a real gameplay/history requirement.

## Chronicler-decides-importance

Rejected for deletion authority because LLM editorial judgment cannot prove no future correctness dependency exists.

---

# 6. Irreversible consequence of choosing S

This must be explicit.

Under S, a line may eventually reach:

```text
exact runtime payload gone
no exact Story copy retained
semantic event/current effects survive
compact provenance may survive
```

If the user later asks for the exact quote, HDM may legitimately answer:

```text
exact wording is no longer retained
```

It must not reconstruct likely wording and present it as verbatim.

This is the principal cost of S.

---

# 7. Irreversible consequence of choosing B

Under B, campaign storage intentionally becomes a durable historical archive of a substantial portion of player-facing discourse.

That means:

- more long-term personal/player-authored text retention;
- more files/storage;
- stronger expectations around export/correction/deletion/history;
- future attempts to reduce archival scope become a product-policy change rather than a mere optimization.

This is the principal cost of B.

---

# 8. Storage/token distinction

Neither option requires putting old transcript into ordinary LLM context.

The architecture will preserve the four separate questions:

```text
physically retained?
indexed/discoverable?
eligible for this role?
loaded into this invocation?
```

Therefore B costs repository/history storage, but it does **not** automatically cost gameplay tokens.

Likewise S does not require deleting recent/available chat text from the host; it only defines what HDM itself promises durably.

---

# 9. Recommendation

**Choose S — Selective Exact / Semantic Continuity.**

Confidence: **MEDIUM-HIGH**.

Why not HIGH: broad dialogue memory is genuinely valuable in a long-form D&D product, and Step 4's existing Transcript design makes B plausible rather than extravagant.

The deciding project value is therefore:

> Is broad exact historical conversation itself a baseline HDM product feature, or is the baseline promise correct persistent world/history with exact wording only where materially retained?

Current repository behavior and the owner's stated “necessary and sufficient / avoid complexity bombs” direction favor **S**.

---

# 10. What would change the recommendation

Recommend B instead if the owner considers any of these baseline requirements:

- “The Master should normally be able to quote any old gameplay conversation exactly.”
- “A durable campaign transcript is itself a core user-facing artifact.”
- “Long-term callbacks from exact dialogue matter enough to justify permanent transcript growth.”
- “We explicitly accept broader long-term player-text retention in campaign storage.”

If none of these is a baseline promise, S remains the smaller architecture.

---

# 11. Owner response required

Approve one direction:

```text
S — SELECTIVE EXACT / SEMANTIC CONTINUITY   [recommended]

B — BROAD QUALIFIED LONG-TERM TRANSCRIPT
```

A modified owner direction is also valid if it specifies the intended user-facing historical promise.

After this decision, the agent owns the mechanical continuation:

```text
owner-decision artifact
-> candidate specification
-> full adversarial scenario review
-> resolution gate
-> canonical Step-5.11 spec
-> roadmap update
```
