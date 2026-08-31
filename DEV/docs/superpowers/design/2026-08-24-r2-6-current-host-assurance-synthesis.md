# R2.6 Current-Host Assurance Synthesis

Status: **RESEARCH SYNTHESIS / PRE-PROBE CONTRACT CANDIDATE**

Date: 2026-08-24

Purpose:

> Narrow the current ChatGPT Plus assurance problem after Source-Manifest/evidence extraction, identify what follows mechanically from existing architecture, and isolate the remaining empirical blockers before any R2.6 Decision Brief/canonicalization.

This artifact is not canonical architecture and does not claim that Protocol 4 has executed.

---

# 1. Established baseline — not reopened

The following are inherited decisions, not R2.6 alternatives:

```text
host                         ChatGPT Plus / ordinary chat
physical LLM topology        one model / one physical chat context
ordinary gameplay turn       one user request / one assistant turn
role containment             logical/behavioral; physical presence != eligibility
campaign authority           repository/native semantic owners, not host memory
repository transport         deterministic Python/core preparation + fixed GitHub Connector remote path
campaign publication         create_tree -> ref check -> create_commit -> update_ref(force=false)
private/API orchestration     out of current public baseline
```

No R2.6 evidence currently justifies reopening these decisions.

---

# 2. The actual remaining assurance problem

R2.6 does not need to discover a new host architecture. It must determine whether the accepted architecture is supportable on the current product surface without overstating guarantees.

The remaining questions divide into four classes:

```text
A. BEHAVIORAL CONTAINMENT
   do final R2.4/R2.5 roles stay inside logical eligibility?

B. HOST BOUNDARY / VISIBLE SURFACES
   can secret-bearing gameplay avoid bypassing Narrator through final response/tool/app surfaces?

C. RESOURCE / DEGRADATION
   does the system fail/degrade safely without exact context telemetry?

D. MULTI-CHAT / CONCURRENCY
   do agency, catch-up and shared planning compose correctly across independent participant chats?
```

Repository transport **selection** is not a fifth class. Only fixed-path assurance remains.

---

# 3. Narrator / `EMISSION_COMMIT` interpretation

## 3.1 What Step 5.12 actually requires

Canonical Step 5.12 defines:

```text
resolved state
-> NarrationResult
-> validate eligible content
-> validate material disclosure refs
-> validate intended recipient
-> freeze supported player-visible response representation
-> EMISSION_COMMIT
-> host output path
```

It also explicitly states:

- `EMISSION_COMMIT` is a **logical semantic boundary**, not a required serialized state machine;
- normal uninterrupted responses are the supported baseline;
- no delivery outbox, token-prefix ledger or completed-message ACK subsystem is required;
- auxiliary visible surfaces must not intentionally carry Narrator-ineligible campaign material;
- Step 6/R2.6 must determine whether the selected physical host provides an equivalent safe boundary.

Therefore R2.6 must **not silently strengthen** Step 5.12 into a byte-exact post-render interception requirement that the owner never selected.

## 3.2 Equally important: R2.6 may not weaken it either

The fact that Step 5.12 does not require a byte-exact outbox does not authorize:

```text
all secret-bearing context
-> free-form final answer
-> hope sanitization catches mistakes
```

The supported physical realization still needs evidence that:

- Narrator is freshly rebound to recipient/role eligibility;
- material reveal basis is established before intentional output;
- private Dramaturg/Actor/Chronicler/planning content does not become Narrator evidence;
- no mandatory auxiliary surface exposes secret-bearing intermediate data;
- the final ordinary response behavior respects the approved recipient bundle.

## 3.3 Recommended interpretation to test

The current architecture strongly points to:

> **PRE-NARRATOR SEMANTIC ADMISSION + FRESH NARRATOR RENDERING**, not post-render byte policing.

Conceptually:

```text
accepted gameplay/current frontier
    |
    v
DETERMINISTIC / TYPED PRE-NARRATOR ADMISSION
    recipient identity
    current source basis
    allowed material reveal refs
    exact-protected eligible slices
    required pending gameplay obligations
    forbidden/ineligible source classes remain non-admitted
    |
    v
FRESH NARRATOR ROLE REBIND
    RoleContextBundle + legal typed handoffs only
    |
    v
NARRATION RESULT / PLAYER-VISIBLE RESPONSE
    |
    v
EMISSION_COMMIT
```

Physical co-presence of other information in model history is handled by the already-approved role-containment law and must be empirically assured, not pretended absent.

This interpretation is compatible with Step 5.12 **if** Protocol 4 demonstrates equivalent material disclosure containment on the supported host.

## 3.4 Why a post-render validator is not the baseline recommendation

A design that requires:

```text
model creates exact final prose
-> external deterministic system receives exact prose
-> external system rejects/edits exact bytes
-> host renders only approved exact bytes
```

would be stronger, but current ordinary-Chat documentation does not expose such a programmable rendering hook as a stable Plus contract.

Making it mandatory would therefore:

- introduce a host primitive not evidenced for the selected baseline;
- effectively reopen the owner-approved one-turn ordinary-chat topology;
- risk driving HDM toward an API/custom-host design already out of scope;
- exceed Step 5.12's accepted normal-response/YAGNI contract.

Keep it as a possible future defense-in-depth mechanism on a richer host, not the current baseline.

## 3.5 Blocking condition

If Protocol 4B shows a material forbidden reveal under realistic final-topology conditions that cannot be corrected by role/context/admission/output-contract design, then the pre-Narrator interpretation is insufficient.

At that point R2.6 must explicitly classify the secret-bearing ordinary-Chat profile as unsupported/restricted or reopen the relevant architecture decision.

Do not paper over such a result with string filtering.

---

# 4. Auxiliary visible-surface policy

Step 5.12 already prohibits intentional leakage through tool/debug/connector surfaces.

For the current Plus host, app documentation adds a practical concern: an approval card may appear before an app action and contains information about the app/proposed action.

The exact visible fields for the current GitHub Connector are an empirical UI question.

Therefore the recommended supported-profile rule is:

```text
ordinary secret-bearing gameplay
    MUST NOT require a visible approval/tool surface
    that exposes raw Narrator-ineligible campaign payload
```

Possible conforming outcomes:

1. the current Connector card exposes only safe metadata/status -> supported;
2. persistent `Always allow` / equivalent permission suppresses routine approval cards and is available/configured -> supported with deployment prerequisite;
3. the mandatory card exposes raw secret-bearing payload and cannot be suppressed safely -> secret-bearing persistence-capable profile is unsupported until the host changes.

This is not transport selection. The Connector remains fixed in all three cases.

Do not pass a deliberately secret-bearing rejected Narrator draft through a player-visible app/tool surface merely to validate it.

Use synthetic canaries for UI-surface testing.

---

# 5. Project memory / ambient context contract

Current Projects documentation means previous project chats may be physically available as context. With default memory on non-Enterprise plans, outside-project chats may also be referenced depending on settings.

HDM therefore needs the following deployment interpretation:

## 5.1 Memory is never an authority path

```text
ChatGPT saved memory / chat-history retrieval / Project memory
    = ambient host context only
    != campaign canon
    != currentness evidence
    != Actor knowledge
    != human disclosure evidence
    != collaboration generation
    != Story coverage
```

Current routed owners always win.

## 5.2 Project-only memory is a useful narrowing option, not a semantic dependency

When available, `project-only memory` is a reasonable recommended HDM Project setting because it prevents unrelated outside-project chat context from entering the physical context.

However:

- chats inside the same Project can still be referenced;
- multiple campaigns or stale prior sessions may therefore remain physically available;
- correctness must still rely on role/currentness containment, not on memory configuration.

A supported HDM profile should not become incorrect merely because Project memory is enabled.

If Protocol 4 shows ambient-memory leakage that cannot be contained, memory-mode restrictions may become an explicit deployment prerequisite.

---

# 6. Context/resource contract

No current consumer-ChatGPT documentation provides an exact stable remaining-context telemetry contract for HDM.

Therefore the R2.3 physical realization should be assured against the following interpretation:

```text
one central conservative estimator
+ versioned host/profile assumptions where useful
+ empirical calibration
+ required representation floors
+ ASSEMBLED_DEGRADED
+ UNSATISFIABLE
```

Not:

```text
hard-code API model max context
or
assume hidden exact remaining tokens are known
```

An estimator miss is allowed to hurt quality/efficiency. It must not authorize silent omission of required evidence.

---

# 7. S53 — shared serving/model/safety profile

## 7.1 Evidence

Current Plus documentation allows Medium/High reasoning and documents that a reasoning allowance may fall back to another available reasoning model.

Protocol 3 already showed strong containment across multiple tested reasoning profiles, with differences mainly in style/decision quality rather than campaign semantics.

Existing architecture also requires campaign semantics/persistence to remain model-profile independent.

## 7.2 Derived result

Exact model equality across multiplayer participants is neither reliably enforceable nor architecturally necessary.

The only baseline compatible with current evidence is:

```text
SHARED EXACT MODEL ID           NO
SHARED EXACT REASONING LEVEL    NO
CAMPAIGN-PERSISTED MODEL ID     NO

SUPPORTED HOST REQUIREMENT      each participant host satisfies the minimum tested HDM capability/behavior envelope
RECOMMENDED PLUS PROFILE        High reasoning when available
FALLBACK                         acceptable only while the supported correctness envelope remains satisfied
```

This is a technical consequence, not currently a material owner trade-off.

If later evaluation shows one supported reasoning/profile class fails a correctness-critical channel, classify that class as degraded/unsupported. Do not change campaign semantics or force every participant to persist identical model metadata.

### S53 disposition

**ACTIVE -> RESOLVABLE BY ASSURANCE:** adopt an explicit minimum capability/behavior envelope; reject exact shared serving identity as baseline requirement.

---

# 8. D15 — Retry sibling advisory

Current Retry/regeneration feature existence does not fire the D15 trigger.

D15 remains:

**CONDITIONAL / DORMANT**

Revisit only if Protocol 4I demonstrates a repetitive supported-product Retry failure where bounded rejected-sibling advisory information would materially help and can remain non-authoritative.

Do not create rejected-response memory merely because Retry exists.

---

# 9. Diamond / Strong disposition at this R2.6 point

| Item | R2.6 state | Human-readable disposition |
|---|---|---|
| **S53** | ACTIVE / near-resolution | Use minimum tested host capability/behavior envelope; High recommended; exact cross-player model equality rejected as unnecessary/unreliable. |
| **D15** | DORMANT | Retry exists, but its exact trigger has not fired. No rejected-sibling memory. |
| **S14** | INHERITED ACTIVE from R2.5 | Local/shared Dramaturg horizons stay noncanonical and need containment/concurrency assurance; R2.6 does not redesign them. |
| **S39** | DORMANT | No reliable measurable prompt-cache contract has been established that justifies cache-specific architecture. |
| **D16/S21/S28** | INHERITED from R2.4 | Invisible logical phases, non-authoritative steering and structural visible-output fencing are regression requirements. |

No other dormant candidate is activated by current host documentation.

---

# 10. What is already sufficiently established vs still empirical

## Established strongly enough to carry as baseline evidence

- one physical context does not inherently require one physical role per call; Protocols 1-3 strongly support behavioral role containment;
- High can remain recommended but cannot be campaign semantics;
- exact cross-player serving equality is not a robust Plus requirement;
- exact remaining-context telemetry cannot be assumed;
- host Retry/history mutation is not campaign rewind;
- fixed Python-prepared + Connector transport remains the selected path;
- Project memory is ambient context, not authority;
- no baseline outbox/ACK subsystem is required by Step 5.12.

## Still requires production-like evidence before R2.6 closure

1. Chronicler -> Narrator containment;
2. shared/local Dramaturg planning -> Narrator/catch-up containment;
3. Project-memory stale/foreign-context containment;
4. data/instruction/role-switch injection corpus;
5. realistic long-chat/context degradation behavior;
6. first-safe-opportunity Chronicler anti-starvation;
7. agency barrier false-positive/false-negative rates and maximal-safe-frontier narration;
8. shared-horizon conflict/rebase behavior on the fixed path;
9. final player-visible/approval/tool surface inventory with synthetic canary;
10. exact supported guarantee for pre-Narrator/`EMISSION_COMMIT` boundary after those observations.

---

# 11. Current Decision-Brief gate

A human owner decision is **not yet justified**.

The main potentially material choice — whether ordinary ChatGPT behavioral/pre-Narrator containment is an acceptable realization of Step-5.12 — depends on Protocol 4 evidence that has not yet been collected for the final topology.

Presenting A/B/C now would outsource an evidence question to the owner.

Correct continuation:

```text
execute / collect Protocol-4 assurance evidence where the current target host allows
-> classify failures/limitations
-> determine whether the pre-Narrator interpretation passes unchanged
-> only if material viable alternatives remain, produce Decision Brief
```

If no material failure appears, R2.6 can likely canonicalize the current direction without reopening Step 5.12.
