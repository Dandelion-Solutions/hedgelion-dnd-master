# Step 5.2 — Resumable Runtime Closure — Resolution Gate

Status: **RESOLVED — CANONICALIZATION AUTHORIZED**

Date: 2026-08-20

Basis:

- fixed pre-research charter;
- architecture task brief;
- research & architecture draft;
- analytical challenge;
- decision brief;
- candidate specification;
- adversarial review.

---

# 1. Gate question

Does Step 5.2 contain any unresolved product-semantic, state-owner, concurrency,
recovery-risk or architectural trade-off that requires a new human architect
decision before canonicalization?

Answer:

> **NO.**

The remaining physical choices are representation/protocol decisions explicitly
owned by later Step-5 slices. The semantic owner model follows from already
accepted Steps 2–5.1 constraints and survives analytical/adversarial challenge.

---

# 2. Resolved architecture

Step 5.2 shall canonicalize:

> **Resumable Runtime Closure is a correctness property over a compatible set of
> domain-native durable sources and the transitive closure of gameplay-significant
> native owners reachable from bounded typed recovery-routing evidence. It is not
> a new semantic owner, universal snapshot, scalar frontier/cut, transcript/model
> memory image or mandatory first-class runtime record.**

The system preserves native state authority, persists irreducible execution
continuity where required, rebuilds derived state, and provides bounded discovery
for active owners that are not already transitively reachable from another
admitted root.

---

# 3. Accepted laws

The candidate laws 5.2-1 through 5.2-8 are accepted with the adversarial
refinements below.

## LAW 5.2-1 — NATIVE OWNER PRESERVATION

Recovery metadata/routing never replaces or duplicates native writable state
authority.

## LAW 5.2-2 — BOUNDED ROOT DISCOVERY

Normal cold recovery must find every independently recovery-relevant active owner
or armed due-capable temporal source from bounded typed routing/native indexes;
no campaign/history/world-wide semantic scan is required.

## LAW 5.2-3 — ROUTING IS EVIDENCE, NOT AUTHORITY

Routing answers only what typed owner/reference to load and validate. Owner state
and lifecycle come from the native owner.

## LAW 5.2-4 — PARTITIONABLE RECOVERY ROUTING

Recovery routing must be partitionable by existing semantic/writable scope. No
single globally hot mutable registry is required.

## LAW 5.2-5 — TRANSITIVE REQUIRED-DEPENDENCY CLOSURE

A promised recovery source set is valid only when every **semantically required
recovery dependency** of its recoverable owners is durable/reachable in the
appropriate native domain, optional, or deterministically rebuildable.

This does not mean recursively materializing every informational edge in the
world graph.

## LAW 5.2-6 — DERIVED STATE REBUILDS

Agenda, MechanicalContext, aggregation/reverse indexes, DAG/cache state, loaded
record caches and other derived views never become recovery authority merely to
avoid recomputation.

## LAW 5.2-7 — NO INVENTED LOST HOT STATE

If volatile HOT/SOFT state is destroyed before an applicable durability protocol
successfully includes it in a promised durable source set, recovery returns to
the last actual durable source set and never fabricates the lost delta.

## LAW 5.2-8 — DOMAIN-NATIVE RECOVERY SOURCES

One recovery operation may compose several compatible native revisions. Their
participation does not make them scalar-comparable, totally ordered or one merged
writable authority.

## LAW 5.2-9 — PINNED NATIVE HYDRATION

One hydration attempt resolves every participating mutable source to an exact
native revision before consuming dependent state from it. A source revision
change that affects compatibility invalidates/restarts the affected selection;
recovery does not assemble mixed branch-relative revisions accidentally.

## LAW 5.2-10 — OWNING-SCOPE RESOLUTION

A required identity/state is resolved through its current native ownership/routing
contract. A stale representation in another domain is not fallback authority.

In particular, live-owned mutable truth is loaded through the live epoch. Missing
or incompatible live state blocks/suspects that scope rather than silently using
an older campaign representation.

## LAW 5.2-11 — ROOT MEMBERSHIP COHERENCE

Whenever a native owner transition changes independent recovery-root eligibility,
the corresponding routing-membership mutation is a required derivative of that
native lifecycle transition and must join the applicable durability closure.

Routing membership reflects lifecycle; it does not decide lifecycle.

Publication/root completeness is therefore correctness-critical secondary-index
maintenance, not a second semantic owner.

## LAW 5.2-12 — INTERPRETABILITY CLOSURE

A promised recoverable operational owner is resumable only when the compatible
runtime/catalog/rules interpretation context accepted by that execution can be
resolved through the campaign engine/package compatibility contract.

Missing required runtime/catalog interpretation context blocks recovery or
requires explicit compatible migration/adoption; arbitrary ambient rebinding is
forbidden.

---

# 4. Procedure lifecycle resolution

Adversarial review exposed an important implementation gap: the current Procedure
machine shape does not yet expose explicit active/terminal lifecycle state.

Step 5.2 resolves the semantics without prematurely choosing a wire enum:

```text
Procedure ACTIVE
    from accepted creation/open semantics
    through intervals between participating Commands/Resolutions

Procedure TERMINAL
    only after explicit typed Procedure-closing/reset/terminal semantics commit
```

Therefore:

- no open Command is required for Procedure to remain active;
- absence of a Command does not terminate Procedure;
- Encounter/Scene status alone does not define Procedure lifetime;
- routing/index membership is not the sole evidence of Procedure lifecycle;
- later machine realization must make active/terminal state/evidence
  deterministic enough to validate membership.

This is a mechanical consequence of accepted Step-3 Procedure ownership, not a
new product choice.

---

# 5. Root classes and admission

Current minimum independently rootable classes are:

```text
non-settled RuntimeCommand
active Procedure
materially unresolved accepted Interaction/IntentPlan when a durability/handoff
    protocol promises that semantic point
otherwise-unreachable armed due-capable temporal source owner
```

Common descendants such as Resolution, Continuation, child Resolution, pending
child descriptor and receipts need not be redundantly rooted when durably
reachable from another admitted root.

This list is not a forever-closed enumeration. General admission rule:

> Any later native operational owner with independently active recoverable
> lifetime that is not guaranteed boundedly reachable from another admitted root
> must receive typed recovery routing under the ordinary architecture/catalog
> admission process.

No untyped generic pending bucket is admitted.

---

# 6. Temporal resolution

Temporal Agenda remains derived.

Required cold-recovery semantics are:

1. bounded discovery of otherwise-unreachable armed due-capable temporal source
   owners;
2. load each native owner/TemporalBinding from its pinned owning scope;
3. load applicable Procedure/chronology/context evidence;
4. rebuild Agenda/due projection;
5. once a due firing crosses the selected/committed execution boundary, continue
   from Step-3 stable firing/pending-child/Resolution identity rather than
   reselecting it from Agenda.

Required temporal routing stores only owner/scope retrieval evidence. It does not
own or require duplicated deadline, next-due, priority, due/not-due decision,
selected trigger, firing generation or chronology-order result.

Step 5.3 owns exact due-selection/no-lost/no-double semantics and any explicitly
disposable acceleration projection.

---

# 7. RNG resolution

Step 5.2 requires survival of:

- already generated/fixed RNG values whose accepted execution remains unfinished;
- already committed/reserved future RNG identity/state only when that reservation
  itself has entered accepted execution semantics.

Step 5.2 does **not** require:

- a campaign-global deterministic RNG stream;
- all genuinely future random experiments to reproduce the same sequence after
  restart;
- ResolutionTrace to become continuity authority.

Step 5.3 must reconcile exact future-RNG representation with the accepted Step-3
fixed-input guarantees.

---

# 8. Interaction / semantic resume resolution

No new generic durable `resume_point` or `pending_prompt` class is admitted.

Cases:

```text
settled/open scene
    -> recover semantic current state; regenerate equivalent presentation

pending mechanical Choice/Reaction
    -> Continuation owns the fixed response contract

material accepted declaration awaiting clarification before Command
    -> Interaction/IntentPlan owns sufficient semantic pending-input state when
       the applicable durability/handoff policy promises that point

same-context maintenance convenience
    -> ephemeral maintenance continuation frame may assist but is not cold
       authority
```

Verbatim transcript is not universally required. If exact message evidence is
still the only way to preserve a materially accepted intent, that specific
message/Interaction evidence remains irreducible until sufficient semantic state
has been materialized.

---

# 9. Live and multiplayer resolution

Recovery source composition preserves native live routing:

```text
campaign scene pointer
    -> exact live epoch/head/state for live-owned scope
```

Rules:

- campaign copies are not fallback truth while live scope owns current mutation;
- independent live epochs remain independent native sources;
- root routing may be live-local/partitioned;
- no global root enrollment barrier/count/generation/digest is required for every
  independent local mutation;
- closed-unabsorbed live epoch is a valid recovery condition but not ordinary
  writable gameplay state;
- 5.8 owns exact root movement/adoption across compaction/rollover.

---

# 10. Identity/promotion closure

A promised recoverable owner cannot require an identity/state whose lifetime is
shorter than the recovery promise.

Therefore:

- a session-local `local-*` dependency must be promoted/rekeyed/materialized
  before a durable owner can depend on it across cold recovery;
- campaign allocator remains its known singleton authority;
- live-epoch provisional identities may remain valid only inside that durable
  authoritative live-epoch lifetime until promotion/compaction;
- a durable root may not point to RAM-only owner state.

This is the recovery consequence of existing promotion/publication closure, not a
new allocator authority.

---

# 11. Integrity and verification resolution

Expected cases:

```text
missing derived cache
    -> rebuild

stale session/coordination pointer
    -> refresh/rebind through native routing

malformed recovery-routing projection
    -> scoped recovery/integrity mode

required root target missing/incompatible
    -> recovery blocked / CANON_SUSPECT
    -> targeted validation/repair

stale root lists terminal owner
    -> native terminal owner wins; repair routing; do not replay

active owner omitted from required routing
    -> publication/root-enrollment completeness defect
```

Because omission may be invisible to normal cold recovery, implementation/testing
must assert enrollment obligations on native activation/terminality paths and at
publication completeness boundaries. Maintenance audit may use broader structural
enumeration specifically to detect latent orphan-active/stale-root drift; normal
recovery remains bounded.

Active cold-start enumeration is distinct from direct addressability/retention of
settled records needed for idempotent retry or audit.

---

# 12. Host-delivery carry-forward

Step 5.2 deliberately does not decide whether a generated player-facing response
was emitted or durably acknowledged.

A crash may occur after mechanics/disclosure state commits but before host output
is known to have reached the player. Step 5.2 establishes only these constraints:

- never roll back or replay committed mechanics merely to reproduce narration;
- transcript text does not become mechanical authority;
- if emitted/acknowledged delivery state changes what may safely be re-emitted or
  what a human player is known to have received, Step 5.12 must represent that
  state through an admitted owner/evidence and make it recoverable when required;
- until then, `delivery state unknown` is a host-layer recovery condition, not a
  license to invent whether output was seen.

Owner: **Step 5.12 / Host Delivery & Disclosure Boundary**.

---

# 13. Explicit later ownership

## Step 5.3

Due-work transition, Agenda rebuild algorithm, temporal no-lost/no-double,
selected-firing boundary and exact RNG continuity.

## Step 5.4

Controlled restart/new-chat/context-expiration policy and when volatile current
closure must be forced durable before intentional context destruction.

## Step 5.5

SOFT/HARD/SAVE semantics for when active owner/root changes become promised
cross-session durability.

## Step 5.6

Crash-consistent publication/idempotency of owner state + required routing
membership/dependency promotion.

## Step 5.7

Physical recovery-routing/checkpoint representation, hydration order, source
pinning/validation, repair behavior and historical checkpoint source selection.

## Step 5.8

Live/campaign partition placement and root movement across epoch lifecycle.

## Step 5.9

Chronology evidence required to interpret recovered temporal bindings.

## Step 5.12

Generated/emitted/acknowledged host output/disclosure recovery semantics.

## Step 5.13

Retention/GC of terminal runtime owners, receipts, root projections and direct
idempotency evidence after active membership ends.

---

# 14. Gate checklist

```text
solution-blind framing executed                         YES
current repository ownership researched                YES
verified facts separated from inference                YES
strongest simpler alternatives challenged              YES
new semantic owner avoided                             YES
checkpoint-as-authority avoided                        YES
Agenda-as-authority avoided                            YES
unbounded normal recovery avoided                      YES
global multiplayer enrollment hotspot avoided          YES
mixed native-revision hydration prohibited             YES
stale wrong-scope fallback prohibited                  YES
interpretation/runtime context closure handled          YES
Procedure between-Command lifetime handled             YES
pending-input recovery bounded                         YES
lost HOT state policy preserved                        YES
cross-slice obligations explicitly assigned            YES
blocking human decision                                NO
```

---

# 15. Resolution

```text
Step 5.2 architecture recommendation: APPROVED FOR CANONICALIZATION
owner decision required:               NO
candidate owner model changed:         NO
adversarial refinements incorporated:  YES
next artifact:                         canonical specification
```

Canonicalization must preserve all laws and carry-forward constraints above. It
must not silently select the later physical root-index/checkpoint/live layout.
