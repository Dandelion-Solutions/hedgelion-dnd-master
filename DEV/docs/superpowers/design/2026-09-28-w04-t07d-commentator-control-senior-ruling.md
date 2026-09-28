# W04.T07D Commentator Control Evidence — Senior System-Impact Ruling

Status: **ACCEPTED SENIOR / PRODUCT-SEMANTIC GATE OPEN**

Date: **2026-09-28**

Public basis reviewed:
`ece4ccd7f302f7a4aae2c37a55b4fea934edbcd5`

Current task:
`W04.T07D — Commentator self-contained control/snapshot and anti-oracle filtering`

Impact brief:
`DEV/docs/superpowers/design/2026-09-28-w04-t07d-commentator-control-system-impact-brief.md`

## 1. Disposition

```text
SENIOR_SYSTEM_IMPACT: RESOLVED
CLASSIFICATION: PRODUCT-SEMANTIC OWNER GAP + BOUNDED IMPLEMENTATION PREREQUISITE
PRODUCT_OWNER_DECISION_REQUIRED: YES
T07D: HELD BEFORE RED
T07A/T07B/T07C: RETAIN ACCEPTANCE
T08B: ACCEPTED / UNAFFECTED
CLS_HDM_PREFLIGHT: RETAIN PASS
VERSION_IMPACT FOR THIS RULING: NONE
```

The worker correctly stopped. The current Commentator implementation cannot
prove protected Story/T0 eligibility from a caller-supplied
`player_id -> story_ids` mapping or legacy `Story.availability.visible_to`.

The requested binary choice — “derive locally” versus “add a W03 evidence
interface” — is incomplete. A source-bound evidence interface can prove *what
the current owners say*, but it still cannot decide *which owner facts grant a
particular Commentator mode access* unless that product rule exists.

## 2. Owning evidence

This ruling composes:

- Step-4 truth / knowledge / disclosure / Story architecture;
- PO-009 self-contained Commentator corpus/control owner;
- current T07B/T07C Story/T0 machine contracts;
- current W03 principal/PLAYER and information owners;
- the stable Wave-04 T07D task;
- current Commentator consumer and RD13 tests;
- the recorded CLS↔HDM preflight and current CLS state.

No private CLS artifact requests a public semantic write for this issue.

## 3. What is already decided

The following are already authoritative:

1. `world.knowledge` owns current fictional subject epistemic state.
2. `runtime.disclosure` owns durable human-player exposure where future
   secrecy correctness depends on it.
3. Human PLAYER exposure does **not** imply that any controlled PC knows the
   same proposition.
4. Story is non-canonical, and Story presence/metadata does not grant knowledge,
   disclosure or access.
5. PO-009 requires the Commentator-importable corpus to carry a comprehensive,
   derived, self-contained control projection.
6. That projection is not a second ACL/knowledge/disclosure owner; native owner
   state determines it and Commentator may narrow but never widen it.
7. Missing/incompatible control evidence fails closed.
8. Ineligible IDs, titles, counts, refs and metadata must be removed before LLM
   materialization.
9. Story availability is dependency/reference based, not a scalar chronology.
10. Step-4 leaves the exact default Commentator spectator
    perspective/spoiler policy to the mode owner.

## 4. Missing semantic owner

Current accepted owners do not choose the baseline answer to questions such as:

- Is protected Commentator material available because the human PLAYER has
  already been exposed to it?
- Does current knowledge of a controlled PC also grant it to Commentator?
- If several PCs are controlled, is eligibility based on one explicitly
  selected PC or a union?
- Is a full-history/spoiler mode separately admissible, and under whose
  authorization?
- What is the fail-closed behavior when the session has no explicit perspective?

Those are product/mode semantics. They cannot be inferred from implementation
convenience.

`PUBLIC | PROTECTED` on retained T0 is intentionally insufficient to answer
the recipient-specific question. It tells Commentator that protection exists;
it does not identify who is allowed to cross it.

## 5. Rejected implementation direction

T07D SHALL NOT:

- construct eligibility from an arbitrary caller map;
- trust legacy `visible_to` as current owner evidence;
- invent an ad-hoc union/intersection of PLAYER disclosure and PC knowledge;
- make Story or Commentator a second access/knowledge/disclosure authority;
- infer PC knowledge from human exposure;
- infer human exposure from PC knowledge;
- use unrestricted native fallback to answer Commentator requests;
- expose protected IDs/counts/metadata to the model before deterministic
  filtering.

Therefore option 1 from the impact brief is rejected **as a semantic-owner
solution**.

## 6. Technical direction after Product Owner decision

Once the baseline mode/perspective rule is accepted, the intended machine shape
is:

```text
authenticated/current recipient identity
+ exact current PLAYER/control evidence
+ owner-native knowledge/disclosure/control evidence required by the selected mode
+ Story/T0 availability requirements
+ one coherent currentness basis
    ->
bounded source-bound Commentator control evidence
    ->
PO-009 self-contained control projection
    ->
deterministic anti-oracle filtering
    ->
eligible Story material only
    ->
Commentator model materialization
```

The source-bound evidence producer is a **projection/evidence boundary**, not a
new semantic authority.

Prefer the smallest owner-native evidence interface that can prove the accepted
mode rule. It should not emit caller-selected Story IDs as authority; Story/T0
requirements remain consumer-side nominations checked against owner evidence.

If the accepted mode can be realized by existing owner-issued values under one
coherent bound operation without changing W03 contracts, T07D may consume those
values read-only. If correctness requires a new W03-facing evidence producer,
instantiate a bounded prerequisite with W03 semantic ownership, focused tests
and normal Version Impact review. Do not broaden W03 merely for convenience.

That concrete implementation prerequisite is intentionally not started before
the Product Owner rule exists; otherwise its shape would encode an unowned
access policy.

## 7. Product Owner decision required

The Product Owner must define the baseline Commentator perspective/spoiler
semantics for protected Story/T0 material.

The decision must at minimum state:

1. the baseline served-human perspective;
2. whether human PLAYER disclosure and controlled-PC knowledge contribute to
   eligibility, and how;
3. behavior for multiple controlled PCs;
4. whether any wider/full-history profile exists and how it is explicitly
   selected/authorized;
5. fail-closed behavior when required perspective/control evidence is absent.

After that decision, Senior may classify the resulting implementation as either
an in-envelope read-only composition or a bounded W03-owned prerequisite. A new
architecture round is not required unless the Product Owner rule introduces a
new durable owner, authority domain or persistence lifecycle.

## 8. Downstream routing

```text
T08B: ACCEPTED / W04_SESSION_CONSUMER_DELTA_READY

T07D:
  PRODUCT_OWNER_DECISION_REQUIRED
  RED NOT AUTHORIZED

T07E:
  BLOCKED by T07D

T07-INTEGRATION:
  BLOCKED

T08A:
  BLOCKED by T07-INTEGRATION

T08C:
  BLOCKED by T08A

A26-02:
  separate mandatory repair/collection debt before W04 FINAL_REVIEW

W05:
  NOT AUTHORIZED
```

## 9. System and version impact

```text
THIS RULING:
  VERSION_IMPACT: NONE
  PRODUCTION_CODE_CHANGE: NONE

SYSTEM_IMPACT:
  SENIOR REVIEW COMPLETE

PRODUCT_OWNER_DECISION_REQUIRED:
  YES

PUBLIC_CLS_REOPEN:
  NO at this ruling
  fresh reconcile remains required if the eventual owner/interface changes the
  public Story/T0/control contract consumed by CLS
```
