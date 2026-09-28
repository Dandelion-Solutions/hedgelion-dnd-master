# Commentator Player + Selected-PC Perspective — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT / CONSUMER SEMANTICS**

Date: **2026-09-28**

Product Owner input:
- `DEV/PRODUCT_OWNER_INPUT.md` — `PO-012`.

This decision refines PO-009 only for baseline Commentator reader perspective
and protected-material eligibility. It does not change native truth,
`world.knowledge`, `runtime.disclosure`, PLAYER/control, Story non-authority
or Commentator-cache ownership.

## 1. Baseline perspective

Baseline Commentator uses one served-human perspective in one Commentator
session/chat. It does not require one chat per PC and does not duplicate the
same commentary across multiple chats merely because the engine can represent
more than one controlled PC.

```text
campaign-admitted Commentator reader
  -> PUBLIC Story material

+ current active PLAYER binding, when one exists
  -> material eligible through that PLAYER's runtime.disclosure

+ at most one selected PC currently controlled by that PLAYER
  -> material eligible through that PC's current world.knowledge
```

No automatic union across several controlled PCs exists.

## 2. Commentator-only reader before PLAYER participation

PO-009 permits a user to enter a campaign read-only through Commentator before
later becoming a gameplay participant.

For a campaign-admitted Commentator reader with no current PLAYER binding:

```text
PUBLIC Story material: eligible
PLAYER disclosure contribution: absent
selected-PC knowledge contribution: absent
protected material without another accepted eligibility basis: fail closed
```

Campaign/read-only admission itself remains externally owned. This decision does
not create a public campaign or bypass campaign admission.

## 3. PLAYER disclosure contribution

When the served human has one current active PLAYER binding, current
`runtime.disclosure` for that exact PLAYER may expand Commentator eligibility.

The contribution is bound to the current PLAYER, an exact fact/control anchor
and a sufficient disclosure aspect. Statement-only exposure does not silently
authorize stronger objective-status or other protected semantics. Missing,
stale, mismatched or insufficient disclosure fails closed.

Commentator does not infer disclosure from chat text, Story presence,
`visible_to`, caller Story-ID lists or PC knowledge.

## 4. Selected-PC knowledge contribution

A PLAYER may additionally use the current knowledge perspective of **one**
selected PC that the PLAYER currently controls.

For baseline protected factual Story/T0 material:

```text
selected PC
+ exact current world.knowledge relation
+ stance == epistemic.known
+ exact fact/control anchor match
  -> may satisfy that protected eligibility requirement
```

`aware`, `believed`, `suspected` and `rejected` do not by themselves
authorize factual protected Story as established knowledge.

Human PLAYER exposure and fictional PC knowledge remain distinct owners. Either
may satisfy an explicitly matching Commentator control requirement under this
decision, but neither is rewritten into the other.

## 5. PC selection and multiple controlled PCs

The normal baseline assumes one active character perspective at a time.

If the current PLAYER controls exactly one PC, host/session UX may select it
automatically. The engine still treats that identity as an untrusted nomination
and revalidates current control.

If several controlled PCs exist:

- do not union their knowledge;
- do not run duplicate Commentator chats;
- do not repeat the same material once per PC;
- use one explicitly selected currently controlled PC for the optional PC contribution;
- if no valid PC is selected, fall back to PLAYER-only eligibility.

Selection is transient Commentator/session perspective state. It is not a new
durable PLAYER field, gameplay authority or PC-control owner.

## 6. Protected Story/T0 material without an exact anchor

`PUBLIC | PROTECTED` is protection classification, not recipient authority.

Protected material is admitted only when Commentator control metadata binds it
to an exact owner-native fact/control requirement evaluable under this decision.
Do not guess from factor names, arbitrary string `provenance_refs`, legacy
`visible_to`, Story IDs or co-location in one record.

If no exact admitted control anchor exists, retain the material in the
comprehensive Story corpus but exclude the affected whole retrieval unit from
baseline model materialization. No field-level secret redaction is introduced.

## 7. Currentness and anti-oracle behavior

Content basis and control basis remain independent. PLAYER binding/control,
selected PC, `world.knowledge` or `runtime.disclosure` changes refresh the
control basis even when Story content is unchanged.

Filtering occurs before model materialization and covers body/title, IDs,
entity/cross refs, counts, chapter/search membership, labels, T0 factors and
navigation/pagination metadata. Missing/incompatible control evidence fails closed.

## 8. Technical realization boundary

No second ACL, knowledge owner, disclosure owner or persistent global
Commentator permission database is authorized.

Current Context Runtime already exact-reloads `world.player`,
`world.knowledge`, `runtime.disclosure` and `world.lore_fact` through the
bound RuntimeHost. The minimal realization direction is:

```text
Story/T0 exact control nominations
+ current reader / optional selected-PC nomination
  -> registered Commentator-control Context profile
  -> exact native owner reload + scope validation
  -> bounded source-bound control evidence
  -> PO-009 Commentator control projection
  -> deterministic anti-oracle filter
```

The evidence layer proves owner state; T07D applies this decision and Story
availability. Neither may mint new access semantics.

## 9. Full-history / spoiler mode

A wider full-history/spoiler profile is **not baseline-authorized**. A future
requirement needs explicit selection/authorization semantics.

## 10. Impact

```text
PO-009: REFINED, NOT REOPENED WHOLESALE
STEP-4 KNOWLEDGE/DISCLOSURE OWNERS: PRESERVED
PLAYER/CONTROL OWNER: PRESERVED
STORY AUTHORITY: UNCHANGED / NONCANONICAL
NEW PERSISTENT PLAYER FIELD: NO
SEPARATE CHAT PER PC: NO
AUTO UNION MULTIPLE PCS: NO
FULL_HISTORY BASELINE: NO
VERSION_IMPACT FOR OWNER PUBLICATION: NONE
```
