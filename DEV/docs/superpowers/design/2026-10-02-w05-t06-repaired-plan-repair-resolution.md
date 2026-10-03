# W05.T06 Repaired Plan — Targeted Repair Resolution

Status: **HISTORICAL REPAIR RESOLUTION — CURRENT P0 BOUNDED PRODUCER GO**

Historical final plan disposition: `DEV/docs/superpowers/design/2026-10-02-w05-t06-final-plan-senior-rereview.md`.
Current P0 disposition: `DEV/docs/superpowers/design/2026-10-03-w05-t06-p0-actor-producer-senior-ruling.md`.

Date: 2026-10-02
Repair basis: `5830fcca01fa4f2bc2231ed50254e4b6f680dad8`

This is planning provenance, not a second executable plan. The only executable
route remains the stable Wave-05 plan plus implementation-plan index.

## Senior findings

### SP06-01 — ordinary Master / Commentator eligibility

Resolved. P3 no longer imports PO-012's Commentator formula. Ordinary Master
uses current gameplay subject + active PLAYER/control and source/aspect-specific
native knowledge/disclosure/access eligibility. Epistemic stance is preserved;
belief/suspicion never becomes objective fact. PO-012 remains separate
Commentator regression coverage.

### SP06-02 — accepted HOT producer/admission join

Resolved by making the WP12 establishment/adoption boundary explicit.

NativeHotStore/CurrentOwnerView trusts no raw row from gameplay/model input.
Rows are current only after trusted native-owner code reaches LOCAL_ESTABLISHED
or post-CAS LIVE_ADOPTED through the infrastructure-only HOT establishment
entry. Admission is process-local operational evidence; cold restart discards
it until current native sources are revalidated. P0 uses an existing real
owner-validated Actor continuity after-image as its producer witness; P1A and P2
supply the T06-specific PC-character and SemanticEvent producers later.

This does not make HOT a semantic acceptance authority: native owner code
validates meaning first; WP12's local transaction establishes the already
accepted after-image.

Historical/currentness note: the source audit recorded in
`2026-10-02-w05-t06-p0-actor-producer-system-impact-brief.md` later found that
the cited `actor_continuity.apply_actor_delta` is not connected to a production
caller and receives accepted/current evidence claims as ordinary input. The
earlier disposition above is retained as review provenance; SP06-02 is currently
open only for confirmation of the accepted producer/source-evidence join. P0 is
held until the bounded Senior ruling.

### SP06-03 — expanding read coherence

Resolved. P0 now defines a finite operation-scoped read session. Any dependency
expansion rereads the full accumulated key union from one closed SQLite
snapshot, invalidates earlier derivations, includes explicit absences and
per-owner source bases, and performs final union revalidation. Movement yields
REVALIDATION_REQUIRED rather than mixed state. No remote I/O occurs inside the
SQLite transaction.

### SP06-04 — P1 issuer/catalog path

Resolved by splitting the lane:

- P1A binds the already-admitted BoundCatalogContext into RuntimeHost and
  implements the S6D-07 production character materialization resolver;
- P1B ReadinessService is the sole issuer of BoundMechanicalDependencySet from
  exact admitted executable/invocation bindings and current owner closure.

Wrong-host/stale catalog and forged dependency carriers fail closed.

## Additional Senior current-consumer findings found during repair

### SP06-05 — actual selected product host lacked HOT wiring

Resolved. P0 now includes bootstrap.compose_selected_runtime_host and RD14.
Trusted HOT capability is supplied at infrastructure composition and is not a
gameplay/model argument. Missing capability cannot mean “HOT is empty”.

### SP06-06 — READY_PC signature lacked PLAYER binding

Resolved. P1B assess_ready_pc takes explicit Actor and PLAYER refs, resolves
both current owners and proves active PLAYER controls that Actor. No reverse
PLAYER scan/index inference is admitted.

### SP06-07 — generic index schema was the wrong EVENT_INDEX contract

Resolved. P2 leaves GAME/SCHEMA/index.schema.yaml on native_family_index
responsibility and creates/finalizes a dedicated strict event_index.schema.yaml
for the already-existing EVENT_INDEX artifact. Template/generator/RuntimeHost/
tests use that event-specific contract. No second history index/owner is added.

### SP06-08 — multi-source History result had singular source basis

Resolved. P2 result is bound to one RuntimeHost operation token and a bounded
collection of contributing source bases; every candidate retains its exact
origin/ref/revision and is exact-revalidated.

### SP06-09 — progressive onboarding had no production materialization resolver

Resolved by P1A. GAME runtime currently has no producer of PC
class_progression/choice_bindings/spellcasting; S6D-07 explicitly deferred the
future production resolver and DIEGETIC_ONBOARDING requires validated native
materialization. P1A implements that already-accepted obligation from typed
accepted anchors/selections plus deterministic inheritance/defaults. It does
not infer rules from prose, create new content, publish or declare READY_PC.

### SP06-10 — native Actor state_revision envelope mismatch

Resolved in P1A planning. Current Actor Continuity machine input and S6D-07
READY_PC evidence require outer native Actor `state_revision`, while the
installed `GAME/SCHEMA/actor.schema.yaml` and generic world-record envelope do
not currently represent that field and no RuntimeHost/native-storage adapter
derives it.

P1A therefore includes the minimum native Actor envelope schema alignment under
the already-accepted Actor/S6D owners. The implementation Version Impact Gate
must classify the exact local schema/campaign-contract consequence under the
current pre-release compatibility policy; the plan does not invent a second
revision field or silently synthesize one from Git/HOT generation.

### SP06-11 — initial Asset allocation and repeat/resume establishment join

Final Senior review found that P1A creates starting Assets but did not explicitly
map their campaign-native allocation or repeated initial materialization.
Step-5.1 §10, WP12-8 and the current id_allocator producer already settle this:
new campaign Assets + allocator after-image + Actor update share the same local
establishment transaction. Existing grants retain identities. Repeat/resume
cannot reallocate, reset current resources or reopen accepted choices.

Resolved directly in the stable P1A file set, producer join, acceptance witnesses
and Impact Envelope. This is an executable-plan omission, not new character,
allocation, persistence or idempotency architecture. No production code changed.

## Gate

```text
PRODUCT_OWNER_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
T06_A1_ARCHITECTURE: ACCEPTED
PLAN_FINDINGS_REPAIRED: SP06-01..SP06-11
FINAL_SENIOR_PLAN_REVIEW: GO
PRODUCTION_IMPLEMENTATION: P0 AUTHORIZED; LATER TASKS DEPENDENCY-GATED
NEXT: W05.T06-P0
```

The final Senior review compared those owners and current consumer contracts;
the linked ruling grants P0 RED/GREEN. This resolution remains provenance,
not a second executable plan.

## Current P0 producer-capability follow-up

The final GO above is a historical plan-review disposition. Direct source
inspection at `4df0484790bbe54bbcf417483b871e0e8345380b` found no production GAME
call to `assess_actor` / `apply_actor_delta`; RD03 supplies a test-only evidence
fixture, while WP12 specifies local establishment only for an already-permitted
native owner edge. The bounded System-Impact brief links the exact owner/code
evidence and holds P0 without reopening T06-A1.

```text
SP06_02: SENIOR_SYSTEM_IMPACT_REVIEW_REQUIRED
FINAL_PLAN_GO: HISTORICAL / P0 EXECUTION HELD
T06_A1_ARCHITECTURE: ACCEPTED / NOT REOPENED
PRODUCT_OWNER_DECISION_REQUIRED: NO UNLESS THE SENIOR FINDS SEMANTICS OR AUTHORITY MUST CHANGE
VERSION_IMPACT: NONE
NEXT: Senior ruling on the exact accepted Actor producer/source join
```

## Senior disposition — 2026-10-03

`DEV/docs/superpowers/design/2026-10-03-w05-t06-p0-actor-producer-senior-ruling.md` confirms the missing trusted caller and resolves the execution hold as bounded realization of accepted R2.2/R2.3/R2.4/WP12 laws. The stable Wave-05 plan now owns the concrete self-state NPC reconsideration join and P0-first Actor revision alignment. No universal evidence issuer or new semantic owner is authorized. SP06-02 is resolved in planning; P0 production proof remains pending. Earlier hold wording is preserved as provenance, not current scheduling. P0 GO; later tasks dependency-gated; PO decision not required.
