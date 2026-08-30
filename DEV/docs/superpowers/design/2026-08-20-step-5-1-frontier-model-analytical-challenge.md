# Step 5.1 — Frontier Model — Analytical Challenge

Status: **CHALLENGE COMPLETE — RECOMMENDATION NARROWED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Challenged artifact:

- `2026-08-20-step-5-1-frontier-model-research-draft.md`

Preferred research alternative entering challenge:

- **Alternative B — small shared semantic vocabulary with domain-specific representations**.

This artifact deliberately attacks that recommendation before Decision Brief.

---

# 1. Strongest opposing case

The strongest case against Alternative B is **Alternative A/D: do not create a cross-domain frontier model at all**.

Every current HDM domain already has a concrete native concept:

```text
campaign Git commit/ref
live epoch/head/blob/revision
chronology event constraints
Continuation generation / dependency refs / RNG stream state
checkpoint ID/descriptor
Story source provenance
session observation SHAs
```

A critic can reasonably argue:

1. the domains have different ordering semantics;
2. therefore the common word `frontier` adds almost no executable behavior;
3. a conceptual `consistent cut` may become a premature generic recovery abstraction;
4. later slices can simply specify their own exact inputs and compatibility rules;
5. introducing common vocabulary now risks creating exactly the generic system the pre-research charter warned against.

This is not a strawman. If domain-local contracts can express every current consumer cleanly, Alternative A/D is simpler and should win.

---

# 2. Concrete-consumer test

The challenge requires at least two current cross-domain consumers before retaining shared semantics.

## 2.1 Consumer 1 — Context Assembler coherent source basis

Step 4 requires one coherent pinned source view per role invocation.

During ordinary campaign-only play this can be one campaign revision.

During an active live epoch, current truth for the live-owned scope is not present at current campaign HEAD; it is inherited campaign base + authoritative live state. A Narrator/Interpreter/Actor context that depends on that scene must therefore know which source revision governs each relevant scope.

Without any shared consistency vocabulary, every role/source adapter would need an ad hoc rule such as:

```text
campaign sources pinned at C
except scene X inherited from C0 and overlaid by live L
and only if campaign routing says L is authoritative
```

The common requirement is not a common data type. It is:

> every source set must declare its domain/scope and a compatible pinned revision/boundary; values from unrelated domains may not be compared or mixed implicitly.

**Result:** real cross-domain consumer exists.

## 2.2 Consumer 2 — checkpoint/cold-recovery composition

Step 3 requires exact recovery of active Procedure/Continuation/RNG/mandatory-work state. Live mode can independently own current scene scope. Campaign branch owns other durable state.

A checkpoint/recovery protocol cannot safely say merely “restore latest checkpoint” or “restore event N” without specifying which compatible authoritative roots/revisions the checkpoint describes.

Again, no generic Frontier value is required. But recovery needs the common invariant:

> a recovery basis is coherent only when every included marker is interpreted in its own domain/scope and the declared cross-domain compatibility/based-on relations hold.

**Result:** second real cross-domain consumer exists.

## 2.3 Consumer 3 — stale versus intentionally lagging classification

A session at old campaign HEAD may be stale for mutation. A Story projection behind current canon is intentionally lagging but valid. A checkpoint behind current campaign state may be a valid older recovery point. A closed unabsorbed live epoch is neither ordinary stale cache nor current campaign state.

Integrity/debugging needs a vocabulary that does not equate “behind” across these domains.

**Result:** useful third consumer, though less fundamental than the first two.

### Consumer-test verdict

Alternative A/D does not eliminate the cross-domain rules; it merely repeats them separately. A small shared semantic rule is therefore justified.

---

# 3. Challenge to the word `frontier`

## Objection

The repository already overuses `frontier` for:

- Git campaign state;
- chronology anchors;
- RNG position;
- dependency revisions;
- durable wall-clock guard metadata;
- Story projections.

Retaining the word may perpetuate confusion.

## Test

Can the model use only `revision`, `cursor`, `pointer`, `coverage` and concrete names, eliminating `frontier` entirely?

### Result

Not cleanly. Chronology and projection domains genuinely need a concept meaning “established/covered boundary in a possibly partial domain” that is neither one record revision nor one traversal cursor.

However, research recommendation was too broad if `frontier` is allowed to mean any progress marker.

### Narrowing

Retain `frontier` only under this strict rule:

> **Frontier = a domain-typed boundary of established progress, coverage, or constraint knowledge.**

Do **not** call these frontiers merely by habit:

```text
working state
SOFT/HARD
pointer
cursor
session observation SHA
dirty set
live blob CAS token
Continuation generation
```

A campaign commit may be described as a **durable campaign revision** and, where a consumer speaks specifically about publication progress, as the marker of that campaign publication frontier. The revision identity is primary; “frontier” is the semantic role, not a new object.

**Verdict:** retain but narrow terminology.

---

# 4. Challenge to `consistent cut`

## Objection

A named “consistent cut” is one conceptual step away from a new `runtime.recovery_cut` class. It may prematurely design 5.2/5.7.

## Simplest alternative

Describe each consumer with explicit source tuples instead:

```text
campaign revision C
live epoch E at L based on C0
Continuation generation G
```

without naming a common composition concept.

## Failure test

The same compatibility requirement appears independently in:

- RoleContext source assembly;
- cold recovery/checkpoint hydration;
- live/campaign cross-scope reads;
- later Story source pinning.

A common phrase is useful, but no record/value identity is needed.

## Narrowing

Use **coherent source cut** only as a conceptual term meaning:

> a scope-indexed selection of source markers that are jointly valid for one read/recovery operation.

Hard restrictions:

- no independent ID;
- no runtime catalog class in 5.1;
- no universal schema in 5.1;
- no implication that every component is a frontier;
- later slices may rename/remove the term if their concrete contracts make it unnecessary.

**Verdict:** keep as conceptual relation, not architecture object.

---

# 5. Challenge to `CURRENT.last_event_id` retirement

## Strongest case for retaining it

A global semantic-event anchor could make bounded LOG retrieval and Chronicler catch-up cheap. It does not need to mean fictional chronology or dense event coverage; it could simply mean “most recently published semantic event known to CURRENT”.

## Counteranalysis

That interpretation still has no current correctness consumer:

- exact campaign revision identifies the durable LOG tree;
- session start can use bounded current-state/entity provenance rather than one global event;
- Story catch-up belongs to 5.10 and may need a different source-coverage scheme;
- checkpoints already require more than one event anchor once live/operational state matters;
- event IDs are allocation identities, not a proven dense log prefix;
- multiple events can be published in one campaign transaction, and a transaction can contain no semantic event at all;
- per-record `last_event_id` already provides local causal provenance where useful.

Keeping the field “for cheap retrieval later” is speculative extensibility — exactly the Step-5.0 contamination pattern.

## Reversal cost

Low. A later slice can introduce a dedicated projection/log cursor if it proves a concrete consumer and semantics.

**Verdict:** retirement recommendation survives challenge with HIGH confidence.

---

# 6. Challenge to checkpoint event frontier conclusion

## Objection

`checkpoint.valid_through_event_id` may intentionally identify the semantic event whose transaction established the recovery point. It need not claim a dense event prefix.

## Result

This is plausible. Therefore 5.1 should **not declare the field itself invalid solely because event IDs are not dense**.

The stronger, justified conclusion is narrower:

> one semantic-event ID cannot be assumed to be a complete universal recovery frontier for campaign + live + operational state.

Step 5.7 must determine whether `valid_through_event_id` remains useful as one provenance/recovery anchor, becomes optional, is supplemented, or is retired.

**Verdict:** research wording is narrowed; defer field fate to 5.7.

---

# 7. Challenge to campaign SHA as durable frontier

## Objection

An active live epoch contains durable operational truth outside the campaign branch, so “campaign SHA = durable frontier” is incomplete.

## Resolution

Correct. The recommendation must say:

```text
campaign durable revision = exact published revision of campaign-owned state
```

not:

```text
campaign SHA = entire game's durable current state
```

Live-owned scope has its own operational durable revision. Overall recoverability may require both.

**Verdict:** campaign revision concept survives with scope qualification.

---

# 8. Challenge to live revision representation

## Objection

`LIVE_STATE.revision` might be redundant with live branch HEAD/blob SHA and should not be promoted into frontier semantics.

## Result

Agreed. `revision` is an epoch-local logical generation/counter useful for inspection/protocol checks. The live branch HEAD/blob token are storage/CAS identities. None should be generalized in 5.1.

**Verdict:** no generic live Frontier object; later 5.8 decides exact live protocol fields.

---

# 9. Assumption attack

## A1 — Context Assembler really needs live-aware source composition

If false: shared vocabulary loses one major consumer.

Attempt to falsify: could live state be normalized into campaign state before every LLM context?

Rejected by existing live design: that would eliminate live hot-path ownership and reintroduce expensive campaign writes/coordination.

Confidence remains HIGH.

## A2 — recovery really needs more than campaign revision

If false: coherent-cut vocabulary may be unnecessary for recovery.

Attempt to falsify: could all active operational state always be published into the campaign tree before any recoverable boundary?

Step 3 explicitly allows suspended Procedure/Continuation and requires recovery roots; Step 5.2 exists to define their durable representation. Active live scope is also separate. Collapsing everything into one campaign snapshot would pre-decide later persistence and could duplicate owner state.

Confidence remains HIGH that semantics must support composition, even though representation is open.

## A3 — campaign source revision can substitute for global semantic-log cursor

Attempt to falsify: Story/Chronicler may need an efficient event cursor.

Correctness does not require `CURRENT.last_event_id`. Efficiency may later justify a projection-local cursor. Step 5.10 is the right owner.

Confidence remains HIGH for current retirement; MEDIUM that no future cursor will be introduced.

---

# 10. Local-versus-global optimization check

Alternative B could make architecture documentation elegant while pushing complexity into every subsystem if it required each value to implement generic comparison/composition.

Therefore the recommendation is explicitly narrowed:

- **no common runtime interface**;
- **no common JSON schema**;
- **no generic comparison function**;
- **no global frontier registry**;
- **no global monotonic counter**;
- **no generic persistence record**.

The shared layer contains only semantic definitions and two enforceable laws:

```text
LAW 1 — DOMAIN TYPING
Every frontier/progress claim must identify its semantic domain/scope.

LAW 2 — NO IMPLICIT CROSS-DOMAIN ORDER
No ordering/comparison is valid across different domains unless a specific
contract defines that relation.
```

Everything else remains domain-local unless a later concrete consumer proves common behavior.

This converts Alternative B from a framework into a small architecture invariant.

---

# 11. Reversibility / option value

The narrowed B is highly reversible because it creates no runtime entity/schema.

Later slices may:

- introduce typed schemas for concrete domains;
- eliminate a conceptual term;
- add a common helper only after repeated identical behavior is demonstrated.

Alternative C would be expensive to reverse because machine contracts would depend on a generic value system.

Alternative A is easy to reverse but leaves current cross-domain consistency language ungoverned.

Narrowed B preserves the most option value at low cost.

---

# 12. Final challenged recommendation

Recommend **Alternative B-NARROW**:

1. retain a small shared semantic vocabulary only;
2. define frontier strictly as a **domain-typed boundary of established progress/coverage/constraint knowledge**;
3. add no generic Frontier machine type, record, schema, registry or comparison API;
4. make domain/scope identity mandatory in every frontier interpretation;
5. forbid implicit ordering/comparison across different domains;
6. keep native domain representations and relations;
7. treat coherent source cut only as a conceptual scope-indexed compatibility notion, not a new record;
8. classify HOT/dirty/SOFT/HARD/pointers/cursors/revisions correctly rather than calling all of them frontiers;
9. retire `CURRENT.last_event_id` as a speculative global cursor;
10. defer the exact role of checkpoint `valid_through_event_id` to 5.7, with the hard constraint that it cannot be the universal recovery frontier by itself;
11. require later Story projection coverage to prove its own concrete cursor/coverage representation rather than inheriting `CURRENT.last_event_id`.

Recommendation confidence: **HIGH**.

---

# 13. What would change the recommendation

Move toward domain-local A/D if later analysis proves both:

- recovery/checkpoint and Context Assembler can operate correctly without any common source-domain/scope compatibility invariant; and
- repeated misuse of pointers/revisions/frontiers can be prevented entirely by local naming alone.

Move toward unified C only if concrete implementation produces multiple consumers needing the **same** heterogeneous marker interface/comparison/composition semantics, not merely similar nouns.

Reconsider `CURRENT.last_event_id` if a named current consumer proves a required semantic-log traversal contract that cannot be adequately represented by campaign source revision plus bounded source/index discovery.

---

# 14. Challenge gate verdict

```text
Strongest opposing case considered:       YES
Simplest viable alternative compared:     YES
Assumptions attacked:                     YES
Failure/counterexamples exercised:        YES
Local/global optimization checked:        YES
Reversibility assessed:                   YES
Recommendation narrowed materially:       YES
Human decision still material:            YES
```

The remaining decision is architectural rather than mechanical because the chosen vocabulary/invariant will constrain every later Step-5 persistence/recovery/concurrency slice.

Next process artifact: Decision Brief for the human architect.