# R2.5 Adversarial Review — Agency-Safe Collaboration and Two-Level Dramaturg Coordination

Status: **ADVERSARIAL REVIEW / CANDIDATE SURVIVES WITH REQUIRED AMENDMENTS**

Date: 2026-08-24

Reviewed candidate:

- `2026-08-24-r2-5-collaboration-multiplayer-candidate-spec.md`

Owner-approved direction remains:

> **B3 — AGENCY-SAFE SCOPED COLLABORATION + TWO-LEVEL DRAMATURG COORDINATION**

Verdict:

> **B3 survives. No new owner-level product decision is required.**

The review identifies required clarifications/amendments AR-1..AR-14 below. They narrow false waiting, prevent collaboration-generation ambiguity, protect shared-planning currentness and ensure planning coherence never becomes plot authority.

---

## AR-1 — Negative proof of independence would freeze too much play

### Attack

Candidate wording could be misread as: if the system cannot prove another player is irrelevant, it should wait.

In an open world there are always hypothetical ways another player might care. This would turn uncertainty into campaign-wide serialization and violate split-party independence.

### Required amendment

A human contributor may become **required** only after a **positive bounded material dependency** is identified through an admitted dependency class and current evidence.

Failure to prove universal independence is not enough.

Conservative stopping applies only after a concrete dependency candidate exists whose unresolved branch can materially consume a still-valid decision opportunity.

### Result

False-positive waiting is bounded without weakening agency protection.

---

## AR-2 — Agency dependency can be stale or fictionally impossible

### Attack

A candidate dependency may be discovered from stale location, old scene state or a planning hint. Example: B appears to be near the bridge in stale campaign state but has already moved under another current owner/frontier.

Waiting for B would be wrong; resolving without current verification could also steal agency.

### Required amendment

Before enrolling a required contributor for a material dependency, verify the smallest applicable currentness/chronology/ownership basis needed to establish that the decision opportunity actually exists.

Planning metadata may discover the possibility but cannot establish it.

Where the decision opportunity depends on cross-scene temporal relation, use bounded Step-5.9 reconciliation before classifying the human dependency.

### Result

Agency protection composes with currentness/chronology rather than bypassing them.

---

## AR-3 — A dependent provisional consequence must not leak through narration

### Attack

The engine may stop canonical resolution at the maximal safe frontier but narrate a likely dependent consequence anyway. Another human can observe that prose externally; observational finality then makes the supposedly provisional branch practically irreversible.

### Required amendment

The maximal safe frontier applies to **visible established consequence** as well as semantic mutation.

Narrator may describe only facts/consequences already established at or before the safe frontier plus recipient-safe OOC waiting/status explanation. It must not expose a dependent unresolved outcome as if it happened.

### Result

Agency barrier protects both state and shared observable history.

---

## AR-4 — One input could be reused ambiguously across collaboration windows

### Attack

Player B says one sentence while two overlapping collaborative scopes are open. If the same contribution is implicitly consumed by both, the engine can invent consent/action in a second context.

### Required amendment

A contribution reference must bind to a typed purpose/scope/generation when admitted to a collaboration obligation.

Reuse across multiple obligations is allowed only when deterministic interpretation establishes that the same accepted contribution explicitly and compatibly satisfies each obligation. No transitive/default reuse.

### Result

Contribution identity does not become blanket authorization.

---

## AR-5 — Overlapping/superseded collaboration scopes need deterministic generation semantics

### Attack

A scope may be replaced while a participant is away. Their later answer may target the obsolete generation and accidentally resolve the successor.

### Required amendment

Collective scopes have stable identity/generation and explicit currentness/supersession.

Input aimed at an obsolete/superseded generation cannot mutate the successor merely by similarity. Rejoin/catch-up must expose the current obligation and reinterpret/reconfirm stale input only through the normal Interpreter/authority boundary.

### Result

Async stale contributions cannot cross generations silently.

---

## AR-6 — Shared Dramaturg horizon can suffer lost-update divergence

### Attack

Two Dramaturg phases in independent chats concurrently update one shared noncanonical horizon. Blind last-writer-wins can silently delete one line's coordination information, recreating the divergence the horizon was introduced to prevent.

### Required amendment

The shared horizon has one current projection generation/source basis and updates through existing exact-base/CAS publication discipline or equivalent current-source fencing.

On conflict, fetch/revalidate and perform semantic rebase. Do not blind text-merge.

Compatible independent planning deltas may coexist. Incompatible provisional directions are reconciled as planning alternatives/revision; neither becomes fact by winning transport order.

### Result

Shared planning continuity is concurrency-safe without becoming gameplay authority.

---

## AR-7 — Shared provisional direction could become a soft railroad

### Attack

If local preparation must always conform to the current shared provisional direction, a stale/mediocre planning choice can suppress better emergent development even when canon has not yet changed.

### Required amendment

Shared **source-anchored constraints** constrain local preparation because their referenced owners do.

Shared **provisional directions** are coordination baselines, not immutable constraints. A local Dramaturg may explore an incompatible alternative as explicitly local/provisional and may propose a shared planning revision. Until the shared basis changes, it must not silently treat that alternative as common campaign preparation.

No player/Actor choice is blocked while planning coordination is revised.

### Result

Coherence does not become plot preservation.

---

## AR-8 — Multiplayer mode transition can leave a stale shared horizon active

### Attack

Campaign changes multiplayer -> singleplayer -> multiplayer. A retained old shared horizon may be mistaken for current common planning on re-enable.

### Required amendment

The shared horizon is **active only while multiplayer mode requires it**.

When multiplayer is disabled it becomes inactive planning material, not a singleplayer correctness dependency. If multiplayer is later re-enabled, retained shared planning must be revalidated against current canon/currentness before reuse; rebuilding/discarding it is always legal.

### Result

“Shared level exists only in multiplayer” gains lifecycle semantics without requiring deletion.

---

## AR-9 — Catch-up can leak private planning

### Attack

Returning-player catch-up discovers a shared/local Dramaturg artifact and summarizes it because it appears relevant. This reveals future possibilities, secrets or GM preparation to the human.

### Required amendment

Dramaturg horizons are never player-facing catch-up evidence merely because they exist or were loaded by a GM role.

A fact described in planning may reach Narrator/catch-up only through an independently eligible canonical/Story/disclosure source under Step 4/R2.3.

### Result

Planning coordination does not weaken recipient secrecy.

---

## AR-10 — Planning loss/recovery must not become canon loss

### Attack

Because horizons are retained across chats, implementation may start treating them as required recovery state for gameplay truth.

### Required amendment

Loss/corruption of local/shared Dramaturg planning may degrade preparation quality and require bounded repreparation, but cannot erase or rewrite accepted world/history/mechanics.

No gameplay recovery guarantee depends on reconstructing exact prior provisional preparation.

### Result

S14 remains noncanonical planning continuity, not a hidden authority promotion.

---

## AR-11 — Story and Dramaturg horizon can accidentally merge lifecycles

### Attack

Both are noncanonical retained prose/projections. An implementation may reuse Story as the shared planning owner or publish future preparation through Chronicler coverage.

### Required amendment

Story is retrospective/history/presentation projection under Chronicler/Step-5.10. Dramaturg horizons are prospective conditional preparation.

Story may orient Dramaturg when eligible, but Story coverage does not prove planning currency and planning generations do not advance Story coverage.

No common lifecycle/authority is implied by both being noncanonical.

### Result

Retrospective continuity and prospective preparation remain distinct.

---

## AR-12 — Single-context physical coexistence increases cross-player planning leak risk

### Attack

A Dramaturg phase may load hidden cross-player plans/secrets, then the same physical chat proceeds to Narrator. Logical eligibility rules exist, but R2.5 adds a new high-value leak channel.

### Required amendment

R2.4 fresh role rebinding and Step-4/R2.3 recipient eligibility remain mandatory.

R2.6 must explicitly test:

- shared-horizon -> Narrator containment;
- other-player local-horizon -> Narrator containment;
- catch-up projection exclusion of planning-only information;
- injection attempts embedded inside retained planning text.

### Result

No new semantic boundary is needed, but assurance scope expands.

---

## AR-13 — Full-campaign planning consistency scans would defeat lazy loading

### Attack

“Every part of the story must be coherent” could be implemented as reading all local horizons and all campaign state before every Dramaturg turn.

### Required amendment

Consistency is enforced through bounded current source constraints, shared planning generation/basis metadata and material dependency discovery.

No per-turn all-player/all-horizon consistency scan is authorized.

When a latent contradiction is discovered later, stale provisional preparation is revised/discarded; this is a planning correction, not evidence that gameplay canon was inconsistent.

### Result

Global coherence remains compatible with R2.3 lazy loading.

---

## AR-14 — Planning relevance must not invent factual/causal bridges

### Attack

Shared horizon notes that two storylines “may converge”. A Dramaturg could treat this planning relevance as proof that remote actions currently affect each other, triggering waiting or world mutation.

### Required amendment

A planning relation may activate discovery/preparation only.

Any material factual, causal, temporal, ownership/resource or agency bridge must be established through its native currentness/chronology/collaboration evidence before affecting resolution.

### Result

Shared planning coordinates possibility without creating causality.

---

# Integrated attack matrix

| Attack | Outcome after amendments |
|---|---|
| false wait on hypothetical remote relevance | AR-1/2: no required contributor without positive bounded current dependency |
| premature bridge explosion kills absent PC by message order | AR-2/3 + Step 5.9: reconcile actual opportunity/order before dependent consequence |
| absent PC exploited as permanent invulnerability | R2.5-7 preserved: automatic consequences still proceed when no decision exists |
| player A claims external consent for B | R2.5-8 + contribution binding: hint only, no B authority |
| one answer accidentally satisfies two windows | AR-4: scope/generation-purpose binding |
| stale reply mutates successor window | AR-5: generation currentness + re-interpret/reconfirm |
| concurrent Dramaturg writes lose one player's prep | AR-6: exact-base/CAS + semantic rebase |
| shared plan railroads emergent local direction | AR-7 + no-entitlement laws |
| multiplayer re-enabled with ancient shared plan | AR-8: inactive/revalidate/rebuild |
| returning player sees hidden future preparation | AR-9/12: planning excluded from recipient projection |
| lost shared plan treated as canon loss | AR-10: quality-only degradation |
| Story becomes future-plan database | AR-11: separate retrospective/prospective lifecycle |
| coherence requires full campaign scan | AR-13: bounded generation/source discovery |
| planned convergence becomes causal fact | AR-14: planning can only discover, never establish bridge |

---

# Required canonical amendments

The canonical specification must incorporate AR-1..AR-14 explicitly or semantically equivalently.

No exact schema/file representation is approved by this review.

No standalone Narrative Dynamics stage is introduced.

No new owner decision is required.

Confidence after review: **HIGH**.