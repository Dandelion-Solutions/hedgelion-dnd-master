# Step 4 Rerun — Adversarial Architecture Review

Status: **ADVERSARIAL REVIEW COMPLETE — FIXES REQUIRED / NO NEW HUMAN DECISION REQUIRED**

Date: 2026-08-20

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-08-20-step-4-rerun-candidate-spec.md`

Review objective: attempt to falsify the Candidate rather than confirm it, with special attention to duplicate authority, hidden context inheritance, PC agency, partial chronology, Story spoiler behavior, migration and physical role co-location.

## 1. Summary

```text
BLOCKER requiring owner decision:     0
HIGH findings, mechanically fixable:  4
MEDIUM findings, mechanically fixable:5
LATER-OWNER / deferred:               4
REJECTED concerns:                    3
```

The core architecture survives review:

```text
world.lore_fact
world.knowledge
runtime.disclosure
Context Assembler
six logical LLM role contexts
STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}
```

No credible alternative became preferable and no new product-semantic trade-off was discovered.

However, Candidate wording is not yet safe to canonicalize. The most important fixes are:

1. replace ambiguous scalar Story `reveal_frontier` with dependency/reference-based availability so Step 4 does not reintroduce a global total chronology;
2. restore a distinct `known` fictional epistemic state so reliable factual knowledge is not collapsed into neutral awareness or voluntary belief;
3. strengthen physical role co-location rules: a logical phase boundary alone cannot make an LLM forget a broader earlier context;
4. make durable lore proposition statement/scope identity immutable once externally referenced; corrections use explicit truth transitions or supersession rather than silent rewriting.

## 2. Finding A — Scalar Story reveal frontier risks reintroducing global chronology

Severity: **HIGH / FIX REQUIRED**

### Attack

Candidate repeatedly names a `reveal_frontier` and says Commentator uses a spectator frontier.

Earlier canonical multiplayer/chronology architecture explicitly permits partially ordered independent scenes and rejects a mandatory global minute-by-minute total order. A single scalar frontier is therefore ambiguous and could accidentally force Story reveal eligibility onto a total timeline that does not exist.

Example:

```text
Scene A: E100 reveals secret X
Scene B: E200 is causally independent
```

If a spectator has consumed B but not A, a scalar `frontier=E200` must not imply X is available merely because E100 has a numerically smaller ID.

### Resolution

Replace scalar semantics with **dependency/reference-based Story availability**.

Conceptually:

```text
availability:
    requires_story_refs[]
    requires_source_refs[]?    # where needed for derivation/audit
```

A Story record is eligible only when the active spectator mode/session considers all required reveal anchors available.

A simple linear NARRATIVE mode may maintain an editorial cursor for UX, but editorial sequence is presentation order, not objective world chronology.

No total chronology is introduced.

Human decision: **not required**; this follows from existing chronology architecture.

## 3. Finding B — `aware | believed | suspected | rejected` cannot represent reliable factual knowledge cleanly

Severity: **HIGH / FIX REQUIRED**

### Attack

The Candidate removed `known` to protect PC voluntary belief and introduced neutral `aware`.

This creates the opposite problem: a PC who directly and reliably perceives an established fact has no state meaning "this information is legitimately part of what the PC knows" unless the engine chooses `believed`, which is framed as voluntary commitment.

Existing INFORMATION policy explicitly distinguishes what each PC/NPC **knows** from beliefs and false beliefs.

### Resolution

Use the minimal closed stance vocabulary:

```text
epistemic.aware
epistemic.known
epistemic.believed
epistemic.suspected
epistemic.rejected
```

Semantics:

- `aware` — aware of the claim/proposition without durable commitment;
- `known` — information is legitimately available to the subject as an established in-fiction fact from a qualifying source;
- `believed` — subject treats proposition as true without the engine claiming objective/reliable knowledge;
- `suspected` — plausible/material possibility;
- `rejected` — subject treats proposition as false/unreliable.

`known` does not mean the human player voluntarily chose an emotion/opinion. The engine may establish PC `known` from resolved reliable observation/information channels. Voluntary transitions among belief/suspicion/rejection remain player-controlled unless a real rule forces cognition.

A proposition can later be corrected objectively; historical source/provenance explains why a subject previously had `known` state under the then-established world model.

Human decision: **not required**; this restores semantics already required by INFORMATION.md and the accepted player-agency boundary.

## 4. Finding C — Logical phase boundary is insufficient if broader private tokens remain in the same model context

Severity: **HIGH / FIX REQUIRED**

### Attack

Candidate correctly says physical co-location cannot merge eligibility, but wording could be implemented as one model conversation with a "now act as Narrator" phase after the same model has already seen Dramaturg secrets.

An LLM cannot be required to literally forget earlier tokens by role label alone.

### Resolution

Canonical rule must be stronger:

> A narrower-context logical role SHALL NOT execute in a physical invocation that still contains source material ineligible for that role.

Therefore Step 6 may co-locate roles only when one of these is true:

1. their effective source eligibility is compatible for that invocation; or
2. the platform provides a genuine context reset/isolation boundary so ineligible prior source material is not present in the narrower phase.

Otherwise the roles require separate physical invocations.

Typed handoffs may cross the isolation boundary; raw source bundles may not.

This remains a Step-4 semantic constraint and a Step-6 physical implementation decision.

Human decision: **not required**; it is necessary to make the already-approved context boundary real.

## 5. Finding D — Proposition text/scope can be silently repurposed under one fact ID

Severity: **HIGH / FIX REQUIRED**

### Attack

Candidate has supersession links but does not explicitly make the proposition's identity-defining statement/scope immutable after durable references exist.

If `fact0042.statement` is rewritten from:

```text
"The duke ordered the murder"
```

to:

```text
"The duke knew about the murder"
```

all existing knowledge/disclosure/history refs silently change meaning.

This violates Step-1 ID non-repurposing.

### Resolution

Once a lore fact is durably referenced, its **identity-defining proposition payload** (statement + material scope/subject/chronology qualifiers) SHALL NOT be semantically rewritten in place.

Allowed in-place changes:

- truth-status transition for the same proposition;
- lifecycle/provenance metadata;
- nonsemantic presentation metadata.

A materially different proposition receives a new fact ID and may supersede/reference the old one.

Human decision: **not required**; direct consequence of stable-ID architecture.

## 6. Finding E — Player disclosure delivery cannot mean "human definitely read it"

Severity: **MEDIUM / FIX REQUIRED**

### Attack

Candidate says disclosure updates after "successful user-visible delivery". The engine cannot know whether a human actually read/rendered a response, and transport acknowledgement semantics may vary.

### Resolution

Define disclosure delivery boundary as **host emission/acceptance onto the player-facing response surface**, not proof of human cognition.

Conceptually:

```text
response accepted by host for player-visible delivery
    -> disclosure may advance
```

If generation/host publication fails before that boundary, do not advance disclosure.

Exact transport acknowledgement mechanics belong to Step 5/host integration.

## 7. Finding F — Disclosure of truth status needs exact revision identity, not only current fact ID

Severity: **MEDIUM / FIX REQUIRED**

### Attack

Candidate introduces `latest_exposed_truth_revision_ref` but leaves revision identity vague.

A correction/supersession must not make a prior disclosure appear to expose the new objective status.

### Resolution

Use an existing causal revision identity rather than introducing a generic revision object.

Conceptually, objective-status disclosure references the exact committed lore truth-transition/correction evidence, such as:

```text
truth_event_id / semantic_event_id
```

or another stable committed transition receipt defined by the eventual lore transition contract.

No disclosure is inferred transitively across:

- later truth-status transition;
- supersession to a different fact ID;
- changed replacement proposition.

## 8. Finding G — Story metadata and indexes can themselves leak spoilers into Commentator context

Severity: **MEDIUM / FIX REQUIRED**

### Attack

Candidate focuses eligibility on Story record content. But names/refs/index entries may themselves reveal hidden entities or later events.

Examples:

```text
chapter title: "The Vampire Duke"
entity_ref: vampire_form_004
cross_ref: E009991_DEATH_OF_KING
```

Even if body content is withheld, metadata can spoil the story.

### Resolution

Availability applies to the **whole retrieval unit**, including material metadata, titles, refs and index entries.

Story indexes used by Commentator SHALL themselves be eligibility-filtered presentation structures.

If a reference identity is materially spoiler-bearing, the containing record/index entry is unavailable until its availability requirements are satisfied.

Repository files remain physically readable; this is only context assembly correctness.

## 9. Finding H — Story availability metadata can become stale after literary edits

Severity: **MEDIUM / FIX REQUIRED**

### Attack

NARRATIVE is editable. A rewrite may add a later-known motive or identity while leaving old availability metadata untouched.

### Resolution

Any material Story content/source edit SHALL recompute/revalidate the record's availability requirements before the edited record is publishable through normal Story tooling.

Story record content and its availability metadata form one coherent projection update even though Story remains non-canonical.

Exact Git atomic publication belongs to Step 5.

## 10. Finding I — Context Assembler needs inspectable source manifests for testability

Severity: **MEDIUM / FIX REQUIRED**

### Attack

Without inspectable source identities, failures such as "Actor somehow knew the secret" become difficult to distinguish from model hallucination versus assembler leakage.

### Resolution

Each RoleContextBundle SHALL expose an inspectable bounded `source_manifest` / source-ref list sufficient for tests/debugging.

This manifest is working/trace evidence, not a new canonical authority and need not be retained indefinitely in production.

Step 6 may define retention/observability policy; Step 4 requires the bundle to be mechanically inspectable.

## 11. Finding J — `world.knowledge.source_refs[]` could grow into history duplication

Severity: **MEDIUM / FIX REQUIRED**

### Attack

If every historical source is retained forever on the current relation, `world.knowledge` becomes a second history log.

### Resolution

Current relation source evidence SHALL be bounded to provenance needed to explain/support the current stance (for example the decisive/current source set). Full historical transition sequence belongs to SemanticEvents/LOG.

No unbounded source accumulation requirement.

## 12. Later-owner finding L1 — Exact Story publication atomicity

Owner: **Step 5**

Need to ensure Story body/index/availability changes cannot publish partially in ways that break normal Commentator retrieval.

Not a Step-4 authority blocker because Story is non-canonical and Step 5 already owns tree transaction semantics.

## 13. Later-owner finding L2 — Story ID allocation under concurrent Chroniclers

Owner: **Step 5**

Layer-local sequential IDs require collision-safe allocation/publication in multiplayer/concurrent maintenance. Existing ID allocator/persistence mechanisms should be evaluated rather than inventing a Story-specific lock now.

## 14. Later-owner finding L3 — Which roles physically require isolated calls

Owner: **Step 6**

Step 4 now gives the compatibility rule. Step 6 must derive the physical role-call matrix based on actual model/context capabilities, cost and latency.

Dramaturg -> Narrator is the obvious incompatible same-context sequence unless true reset/isolation exists.

## 15. Later-owner finding L4 — Default Commentator spoiler/perspective mode

Owner: **Step 6 / mode profiles**

Step 4 supplies dependency-based availability metadata. Product mode chooses whether a guest starts:

- no-spoiler chronological/editorial progression;
- full completed history;
- a particular PC/player perspective;
- another explicit mode.

No need to decide this to establish storage/authority semantics.

## 16. Rejected concern R1 — "Story should be canonical because it may become the only exact transcript copy"

Reject.

Irreplaceable presentation fidelity does not imply world/mechanical authority. Losing an old photograph does not change the event it depicted. Story can be durable and valuable without becoming recovery truth.

## 17. Rejected concern R2 — "Use one universal knowledge record to simplify Context Assembler"

Reject.

Six roles make the human-player versus fictional-subject distinction more important, not less. Combining player exposure with fictional cognition would make Actor/Narrator/Interpreter eligibility easier to confuse.

## 18. Rejected concern R3 — "Add an LLM verifier role for Narrator factuality"

Reject for Step 4.

A seventh role would not create deterministic proof of free-form prose correctness and would add latency/complexity. The stronger guarantees are:

- narrow eligible Narrator context;
- typed settled inputs;
- structured disclosure refs;
- Narrator prose never becomes canonical authority;
- optional quality verification may be considered under Step-6 orchestration if evidence later justifies it.

## 19. Residual generative limitation

Even with perfect context assembly, an LLM can hallucinate an unsupported factual sentence from its priors.

Step 4 can prevent **context-derived secret leakage** and prevent prose from becoming canon; it cannot mathematically prove arbitrary natural-language output contains no coincidental unsupported claim without turning narration into a fully formal language.

Therefore the canonical spec should state this boundary explicitly:

- material narration must be grounded in eligible structured inputs;
- unsupported prose is a correctness error;
- no later core operation may treat Narrator prose as authority;
- optional semantic output checking is a Step-6 quality mechanism, not canonical-state authority.

This is a residual model-quality risk, not a reason to abandon role-specific contexts.

## 20. Recommendation after challenge

Apply Findings A–J mechanically and proceed to canonical consolidation.

No finding changes the owner-approved product semantics or requires a new human architecture decision.

Recommendation confidence after adversarial review: **HIGH**.

What would change the recommendation:

- proof that role-specific source isolation cannot be implemented even with separate model calls;
- a product requirement that Story must become recovery/canonical authority;
- a requirement that all spectator modes directly query unrestricted live world state;
- a requirement that fictional PC belief be automatically chosen by the engine rather than controlled by the player;
- a real lifecycle for Secret that remains independent after truth/knowledge/preparation decomposition.

None is present.
