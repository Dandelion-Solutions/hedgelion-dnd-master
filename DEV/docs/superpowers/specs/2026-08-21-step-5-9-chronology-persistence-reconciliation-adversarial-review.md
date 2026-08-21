# Step 5.9 — Chronology Persistence & Reconciliation — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE NOT YET CANONICAL**

Date: 2026-08-21

Reviewed candidate:

- `2026-08-21-step-5-9-chronology-persistence-reconciliation-candidate-spec.md`

Owner boundary:

- `2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`

Review objective:

> Attempt to falsify the candidate under chronology-domain ambiguity, append-only late reconciliation, bounded recovery, frontier growth, metric-provider ambiguity, live-source movement, dense multi-scene interaction, compaction and the accepted forward-extensible/immutable-history temporal boundary.

---

# 1. Executive verdict

The candidate direction survives, but **five blocking clarifications** are required before canonicalization.

None requires a new owner/product decision or a second chronology model.

Blocking findings:

```text
F1  causal order vs calendar/metric order is not typed strongly enough
F2  metric deadline evaluation lacks exact deterministic position-provider routing
F3  late relation evidence needs explicit bounded dependency/discovery semantics
F4  local maximal-anchor frontier needs safe-retirement semantics, not only semantic joins
F5  baseline query/retention guarantee must be consumer-bounded, not arbitrary-history-complete
```

Additional nonblocking refinements:

```text
F6  local bounded metric constraint composition must be permitted without a global solver
F7  cross-live relation endpoints must survive source movement/absorption by stable identity
F8  same-coordinate evidence must remain positive/typed and must not be inferred from CAS simultaneity
F9  unsupported mutable-past semantics must be rejected before acceptance when recognizable
```

After these refinements, the architecture remains substantially simpler than global-clock, vector-clock, full temporal-CSP or branching-timeline alternatives.

---

# 2. Attack: immutable-history time travel breaks an untyped `STRICT_BEFORE`

## Scenario

Accepted fiction:

```text
A = PC departs from year 1250
B = PC arrives in year 1199

A CAUSES B
calendar(B) < calendar(A)
```

The owner-approved boundary explicitly permits immutable-history time travel when accepted causal history is not rewritten.

Candidate LAW 5.9-7/26 currently implies that causal relation plus reverse strict temporal order may be contradictory.

That is too strong if `STRICT_BEFORE` is not domain typed.

## Why this matters

There are at least two distinct orders:

```text
CAUSAL ORDER
    A causally precedes B

WORLD-CALENDAR / METRIC ORDER
    B is located earlier than A on calendar axis C
```

These statements are compatible.

The same issue appears in:

- visions/records that refer to earlier calendar positions;
- stasis/teleport/time-dilated crossings;
- any future chronology domain whose logical progression is not identical to world-calendar coordinate order.

Step 5.1 already requires domain typing and prohibits implicit cross-domain comparison.

## Finding F1 — BLOCKING

Every correctness-relevant precedence relation must identify its **chronology order domain/context**.

Required refinement:

```text
CAUSES(A,B)
    causal ancestry domain

PRECEDES(A,B,D)
    strict precedence in chronology order domain D

SAME_COORDINATE(A,B,C)
    equality in metric coordinate system C

ELAPSED(A,B,C,[lo,hi])
    metric relation in C
```

No implicit inference may equate causal order with calendar/metric order.

Baseline causal ancestry remains acyclic and forward-extensible even when calendar coordinates go backward.

A mutable-past causal loop remains unsupported; a backward calendar jump does not.

## Candidate impact

Material wording change required, but no architecture-direction change.

---

# 3. Attack: `TemporalBinding.context_id` still does not determine which current position to compare

## Scenario

Effect E has:

```text
metric_deadline:
    context_id = world_minutes
    deadline = 720
```

Actor owning E moves:

```text
Scene A -> transfer -> Scene B
```

Both scenes expose positions in `world_minutes`, but they are independent chronology scopes and may currently report different coordinates/ranges.

Which position determines E due-ness?

The candidate says "owner/applicable scope-position provider" but does not yet make provider selection machine-decidable.

## Failure modes

Without a precise provider contract, recovery/runtime may:

- choose the currently loaded scene by accident;
- compare against both and choose the more convenient answer;
- retain stale Scene-A position after transfer;
- silently treat the metric context itself as a global-current owner;
- disagree across hosts about which scope supplies `current position`.

## Finding F2 — BLOCKING

Every metric TemporalBinding family must have deterministic owner-specific **position-provider resolution**.

Conceptually:

```text
ResolveTemporalPosition(owner, binding, current ownership/routing basis)
    -> POSITION_PROVIDER(scope_ref, context_id)
     | INDETERMINATE_NO_COMPATIBLE_PROVIDER
     | INTEGRITY_CONFLICT
```

The provider-selection rule belongs to the native owner/binding family, not to a generic global chronology service.

Examples:

- actor/effect deadline may use actor's current admitted temporal scope;
- process-local deadline may use process-owned temporal scope;
- procedure metric may use procedure-owned coordinate provider;
- a binding whose semantics deliberately remain anchored to source scope may pin/reference that provider until lawful rebase.

If several current providers are simultaneously claimed for one binding where the owner contract requires one, that is an ownership/integrity defect.

If no compatible provider/bridge is established, result is `INDETERMINATE`, not guessed time.

## Candidate impact

Technical contract refinement; no new mutable owner required.

---

# 4. Attack: late relation assertions are append-only but can become undiscoverable

## Scenario

Old anchors:

```text
A
B
```

Later event E establishes:

```text
PRECEDES(A,B,D)
```

The old A/B records remain immutable. E stores a chronology assertion.

Months later an active process P needs that exact relation after cold recovery.

How does P find E without scanning all LOG/history?

## Two bad extremes

### Bad option 1 — global chronology database

Create a universal mutable relation table/index as chronology authority.

Rejected: duplicate authority and unnecessary global subsystem.

### Bad option 2 — no discovery contract

Assume relation search can scan all chronology assertions whenever needed.

Rejected: violates bounded recovery/hot-path constraints.

## Finding F3 — BLOCKING

The architecture must distinguish **relation evidence identity** from **relation discovery/enrollment**.

For every still-live/promised consumer of a late relation, one bounded durable evidence path must exist.

Preferred forms:

```text
consumer/native owner directly references relation evidence
OR
owner/domain-native bounded chronology dependency index routes to it
```

If an endpoint-only relation lookup is a required runtime operation, a derivative typed endpoint index may be maintained, but:

- it is not semantic relation authority;
- it has explicit scope/coverage;
- assertion + required discovery enrollment become durable coherently enough that healthy state cannot expose an acknowledged live dependency with no bounded route;
- stale/lost index may be repaired from its bounded source contract, not by unconstrained campaign history scans.

No architecture promise is made that **arbitrary** old anchor pairs can always be answered from endpoint IDs alone after compaction.

## Candidate impact

Clarifies LAW 5.9-34/35 and late-assertion placement.

---

# 5. Attack: mathematical maximal frontier can grow forever

## Scenario

One large scene contains many independent ongoing processes/threads:

```text
A1 A2 A3 ...
B1 B2 B3 ...
C1 C2 C3 ...
```

No single accepted event is truly after every branch.

If `LocalFrontier(S)` literally means all mathematical maximal anchors in all retained scene history, its size can grow without bound.

A synthetic join purely to shrink metadata is forbidden correctly by the candidate.

## Finding F4 — BLOCKING

`LocalFrontier(S)` must mean the bounded set of maximal **active extension-basis anchors**, not every maximal historical anchor in the entire scope history.

An anchor remains in current local frontier only while future ordinary extension/recovery of S is required to treat it as a current predecessor/basis.

Safe removal from frontier occurs when either:

```text
A. semantic join/convergence J genuinely supersedes it as current extension basis
OR
B. owner lifecycle/relevance proves that branch is no longer part of current extension basis
   and every still-live direct consumer retains its own chronology dependency/evidence route
```

Removing A from current frontier does **not** delete A or assert an order relative to other branches.

If many genuinely independent activities must remain current simultaneously, they should normally be represented as separate typed chronology/process scopes rather than forcing one scene frontier to become a vector over the world.

## Candidate impact

Refines frontier meaning and boundedness. No vector clock required.

---

# 6. Attack: "bounded chronology" can secretly promise arbitrary historical analytics

## Scenario

After years of campaign play, user asks:

> Could NPC X have physically been in city Y between historical events A and B given every retained journey and appearance?

No active temporal owner, current process or promised recovery dependency has required that arbitrary query for years.

If Step 5.9 promises exact bounded answers for any historical pair/query forever, compaction becomes close to a permanent temporal database.

That conflicts with the stated "necessary and sufficient" scope.

## Finding F5 — BLOCKING

Baseline chronology guarantee is **consumer-bounded**, not arbitrary-history-complete.

Guarantee:

> Every still-live or explicitly promised canonical consumer retains a bounded path to sufficient temporal/causal evidence for its admitted predicates.

Not guaranteed:

> Every arbitrary future historical chronology query remains exactly decidable forever after lawful compaction.

An arbitrary historical question may still be answerable from retained lore/events/Story/evidence, but Step 5.9 does not require chronology retention to guarantee it unless another owning contract promises that capability.

This is not a ban on historical investigation gameplay: when a historical relation becomes materially established/needed, the relevant accepted lore/event/process/chronology evidence becomes a live/retained consumer and is then protected accordingly.

## Candidate impact

Clarifies retention/compaction semantics and prevents accidental temporal-database scope expansion.

---

# 7. Attack: range-only metric evidence may require bounded local constraint composition

## Scenario

Accepted evidence:

```text
ELAPSED(A,B,C,[5,10])
ELAPSED(B,D,C,[7,12])
```

A current consumer asks whether D is at least 15 minutes after A.

Direct edge does not exist.

A simple bounded composition derives:

```text
ELAPSED(A,D,C,[12,22])
```

and therefore the predicate may remain indeterminate.

## Risk

If the architecture forbids any temporal constraint composition, useful retained interval evidence becomes much less valuable.

If it admits a campaign-wide solver, complexity explodes.

## Finding F6 — NONBLOCKING REFINEMENT

Permit deterministic **bounded component-local metric constraint composition** for a concrete predicate.

Baseline needs only simple ordered difference/bound reasoning over loaded relevant anchors/relations; no global temporal CSP service is authorized.

If the touched component is not bounded under the consumer's dependency contract, the operation must use explicit maintenance/reconciliation/degradation rather than scan all campaign history.

Derived composed bounds need not be persisted unless a concrete future-consumer/performance requirement justifies a derivative summary.

---

# 8. Attack: cross-live bridge endpoint moves during close/absorption

## Scenario

Live epoch EA accepts anchor A3.

Live epoch EB accepts B4 referencing A3 causally.

EA then closes and absorbs into campaign while EB remains active.

Can EB's relation still resolve?

## Finding F7 — NONBLOCKING REFINEMENT

Yes, only if chronology endpoints use stable accepted identities independent of current physical source placement.

Step 5.8 already requires accepted live-born IDs/evidence to survive close/absorption. Step 5.9 must state explicitly:

```text
anchor identity survives native source movement
routing resolves current retained evidence location
physical source revision is not chronology identity
```

B4 must never bind its causal relation to "whatever event is at live branch HEAD L" as chronology identity.

If an endpoint is accepted only in volatile/unpublished state, it is not a legal durable cross-scope chronology anchor.

No freeze of EA is required merely because EB references an already accepted immutable A3; freeze remains necessary only when the cross-scope semantic transition mutates/fences affected writable scopes under Step 5.8.

---

# 9. Attack: CAS-near-simultaneous actions masquerade as `SAME_COORDINATE`

## Scenario

Two live writers prepare actions from the same live revision. One CAS wins, then the other refreshes and its action is adjudicated as fictionally simultaneous with the first.

## Risk

Implementation may infer simultaneity from:

- same prior source revision;
- near-equal commit time;
- same user-message window;
- same combat round.

None is sufficient by itself.

## Finding F8 — NONBLOCKING REFINEMENT

`SAME_COORDINATE(A,B,C)` is accepted positive semantic/mechanical evidence only.

It may be established by:

- registered initiative/turn/contest mechanics;
- accepted shared boundary occurrence;
- explicit chronology reconciliation with adequate evidence;
- exact shared metric coordinate where semantics warrant equality.

Transport concurrency never establishes it.

---

# 10. Attack: unsupported mutable-past request is accepted first and rejected only after contradiction

## Scenario

Dramaturg/player interaction produces an action explicitly intended to alter already-established past fact A.

If the runtime first commits replacement facts and only later notices a chronology contradiction, baseline history has already been contaminated.

## Finding F9 — NONBLOCKING BUT REQUIRED BOUNDARY HANDLING

Where unsupported temporal semantics are explicit in the requested/validated action, capability validation should reject/defer **before** accepting canonical mutation that depends on mutable-past/branching/causal-loop semantics.

If the unsupported nature becomes knowable only after resolving new evidence, no silent rewrite occurs; affected operation remains unaccepted or enters typed boundary/integrity handling.

Dramaturg carry-forward reduces spontaneous preparation of such premises but is not the enforcement authority.

---

# 11. Attack: causal relation can be objectively uncertain/disputed

## Scenario

NPC believes A caused B, but objective canon has not established that causal relation.

## Review result

No candidate change required.

`CAUSES` is canonical objective causal evidence only when established through normal deterministic/adjudicated promotion.

Believed/suspected causality belongs to Step-4 lore/knowledge propositions and does not become chronology relation merely because an NPC or Narrator states it.

---

# 12. Attack: global countdown

## Scenario

Five independent parties race against one 24-hour deadline.

## Review result

Candidate survives.

Use one common metric coordinate system if established by campaign/ruleset, but retain independent scope positions.

More actions require metric evidence; no one mutable global `now` is necessary.

When a party's current position interval crosses the deadline, result is lawfully `INDETERMINATE` until a material operation establishes more precision or adjudicates the boundary.

No architecture blocker.

---

# 13. Attack: strong planar time dilation

## Scenario

Plane A and Plane B have nonconstant/unknown conversion. Actor carries a 60-minute Effect across boundary.

## Review result

Candidate survives if F2 position-provider routing and candidate rebasing law are strengthened.

Safe cases:

- retain source-context deadline + exact/bounded bridge evidence;
- deterministic safe rebase;
- otherwise `INDETERMINATE` for affected temporal predicate.

No generic rate engine is required.

---

# 14. Attack: dense synchronized multi-scene campaign

## Scenario

Four groups continuously exchange state every few actions.

## Review result

Candidate correctness survives, but cost approaches a denser affected relation component.

Required discipline:

- operations declare concrete chronology dependencies;
- relation evidence remains stable/direct where possible;
- consumer-specific summaries/indexes may optimize repeated predicates;
- no automatic vector clock/global frontier solely because interaction is frequent.

Revisit trigger:

> measured real workloads show repeated arbitrary cross-scope chronology comparisons dominate latency/context/storage enough that derivative summary maintenance is cheaper.

This is performance debt trigger, not current semantic blocker.

---

# 15. Attack: compaction widens interval while preserving today's answer

## Scenario

Current retained evidence says:

```text
ELAPSED(A,B) = [47,53]
```

Today one deadline at 100 minutes remains NOT_DUE even if summary widens to `[0,60]`.

Tomorrow another still-live mechanic tests `>= 50`.

## Review result

Candidate LAW 5.9-38 is correct: compaction must preserve the feasible relation set required by every still-live promised consumer, not one current answer.

No blocker.

---

# 16. Attack: historical discovery adds relation that conflicts with existing canon

## Scenario

Current accepted chronology contains:

```text
PRECEDES(B,A,D)
```

New discovered document appears to prove:

```text
PRECEDES(A,B,D)
```

## Review result

The new evidence does not automatically become a second contradictory chronology assertion.

The accepted transition must distinguish:

- document/proposition exists and says X;
- objective chronology X is established.

Step-4 truth/knowledge can represent disputed/false evidence without polluting chronology.

Only validated objective relation enters chronology. If authoritative evidence still conflicts, use scoped integrity/adjudication policy rather than accepting both silently.

No blocker.

---

# 17. Attack: local frontier retirement hides a causal prerequisite

## Scenario

Frontier currently `{A,B}`. B becomes inactive and is removed from frontier. Later new event J relies on a state that in fact required B.

## Review result

This is exactly why F4 needs explicit safe-retirement semantics.

Frontier retirement cannot discard direct consumer dependencies or current-state causal prerequisites. If J's accepted legality/state depends on B, B remains reachable through native state/provenance/chronology dependency even if it is no longer a current extension-frontier member.

Frontier is not the only history/provenance route.

---

# 18. Blocking resolution requirements

Canonicalization is blocked until the resolution gate incorporates all five:

```text
R1. domain-type every chronology precedence/metric relation;
    causal order and calendar/metric order are distinct.

R2. define deterministic native owner-specific temporal position-provider resolution.

R3. require bounded durable consumer->relation evidence routing/enrollment for late assertions;
    endpoint indexes remain derivative/typed if required.

R4. redefine local frontier as maximal active extension-basis anchors with safe retirement,
    not all historical maxima.

R5. state explicitly that retention/query guarantees are consumer-bounded,
    not arbitrary-history-complete.
```

Required nonblocking refinements:

```text
R6. permit bounded component-local metric constraint composition.
R7. anchor identity survives live source movement/absorption.
R8. SAME_COORDINATE is positive accepted evidence only.
R9. unsupported mutable-past capability is rejected before accepted mutation where recognizable.
```

---

# 19. Owner-decision assessment

No new human decision is required by this review.

The most material finding, F1, does not reopen the owner-approved temporal boundary. It is required **to honor** it: immutable-history time travel is allowed only if causal progression and calendar/metric coordinate order are not conflated.

F5 narrows baseline retention to the already intended "necessary and sufficient" promise: protect active/promised consumers, do not silently promise a permanent arbitrary historical temporal database.

No reviewed failure demonstrates need for:

- global current clock;
- vector clocks;
- full temporal CSP;
- branching-timeline engine;
- second compensation chronology model.

---

# 20. Review verdict

```text
architecture direction     SURVIVES
candidate as written       NOT READY TO CANONICALIZE
blocking findings          5
new owner decision         NONE
second chronology model    NOT JUSTIFIED
```

Proceed to a resolution gate that mechanically incorporates R1–R9, then write a consolidated canonical specification and run fresh closure verification.