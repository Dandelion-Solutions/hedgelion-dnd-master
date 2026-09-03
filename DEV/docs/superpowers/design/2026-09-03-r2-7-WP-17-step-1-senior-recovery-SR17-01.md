# R2.7 WP-17 Step-1 — Senior Recovery SR17-01

Status: **SENIOR REPAIR COMPLETE — MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Domain: `WP-17 — async collaboration / agency-safe progression`

Repair basis public HEAD:

- `d72662d827049b39612386bb236fa14c83fc9ef8`

This artifact records a narrow Senior recovery of the completed WP-17 Step-1 package. It does not start Step 2, does not start WP-18, does not begin implementation planning, and does not alter runtime/schema/template/catalog/test implementation.

Historical whole-project Task-Brief critic findings `B01-B05` / `S01-S11` and their original counts remain historical evidence and are not renumbered, recomputed or rewritten by this repair.

---

## 1. Senior finding

### SR17-01 — BLOCKING — existing `value.contribution` semantic collision

The Step-1 package used generic human-collaboration language such as “typed semantic contribution” without directly enrolling the already-existing `value.contribution` owner into the mandatory Step-2 Source Manifest route.

Current repository evidence establishes a collision that must be impossible to interpret as one shared semantic surface:

- `DEV/CATALOG/core-catalog.json` already registers `value.contribution` under `protocol_value_kinds`;
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` owns its meaning: a Rule Element is a pure embedded mechanical value object and, when evaluated, returns a typed `value.contribution` to a deterministic Calculation Selector resolver.

Mandatory distinction:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != collaboration-obligation contribution lifecycle
```

The existing kind is therefore not available for automatic reinterpretation merely because R2.5 calls human collaboration inputs “contributions”.

Disposition: **CLOSED** by the repaired Task Brief and open-world Source Manifest.

---

## 2. Mandatory Step-2 evidence route after repair

If and only if Senior GO later authorizes Step 2, the open-world Source Manifest requires direct inspection of:

- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/CATALOG/core-catalog.json`, including the existing `value.contribution` protocol surface;
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`, especially LAW R2.5-18;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` for Interaction/input identity and idempotency owners;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` for accepted `runtime.message` evidence;
- current runtime/catalog/input consumers reached from that owner graph.

Step 2 must determine the exact representation of **human async collaboration input** through the current Interaction/message/input owners and evidence. It must not assume that `runtime.interaction`, `runtime.message`, `value.contribution`, a collaboration-obligation field, or any new protocol kind is automatically the answer before evidence synthesis.

This repair deliberately does **not** introduce a replacement protocol kind/name/schema.

---

## 3. R2.5 accepted-input reference law preserved

R2.5 LAW R2.5-18 remains controlling:

```text
collaboration obligation lifecycle
    -> references accepted Interaction/input identities
    -> does not copy transcript prose
    -> does not become a second message store
```

Therefore any later admitted `runtime.collaboration_obligation` owner may retain only the references/currentness/lifecycle information required by the accepted collaboration semantics. The exact referenced human-input representation remains a later evidence/design result.

The repair also preserves:

- collaboration owns collection only, never gameplay consequence;
- human input representation does not establish fictional chronology;
- duplicate/late input still composes through accepted Interaction/idempotency owners;
- message presence does not establish truth, knowledge or disclosure;
- recipient catch-up remains bounded and recipient-safe.

---

## 4. Historical critic preservation

The completed Step-1 whole-project critic remains historical evidence:

```text
B01-B05 BLOCKING:      5
S01-S11 SIGNIFICANT:  11
```

Those counts are unchanged by Senior review.

SR17-01 is a later Senior finding and is recorded only in this recovery artifact plus the repaired Task Brief/Source Manifest/cursors. It is not inserted into or renumbered within the historical B/S register.

---

## 5. Reopen and downstream boundaries

This Senior repair found no:

- contradiction requiring R2.5 reopening;
- contradiction requiring Rule Element mechanics reopening;
- product-semantic decision requiring human arbitration;
- new unsatisfied consumer requiring Step 3, Step 5.11, WP-13, WP-14, WP-15 or WP-16 reopening.

The collision is resolved by semantic separation and mandatory source routing, not by changing the existing mechanical kind.

WP-18 remains downstream and not started.

No implementation planning is authorized.

---

## 6. Repair disposition

```text
SR17-01:                       CLOSED
HISTORICAL_B01_B05:            PRESERVED
HISTORICAL_S01_S11:            PRESERVED
HISTORICAL_CRITIC_BLOCKING:    5
HISTORICAL_CRITIC_SIGNIFICANT: 11
UNRESOLVED_BLOCKING:           0
UNRESOLVED_SIGNIFICANT:        0
HUMAN_DECISION_REQUIRED:       NO
UPSTREAM_REOPEN_REQUIRED:      NO
STEP_2_AUTHORIZED:             NO
WP18_STARTED:                  NO
IMPLEMENTATION_PLANNING:       NO
IMPLEMENTATION_CHANGED:        NO
SOURCE_MANIFEST_CLOSED_WORLD:  NO
NEXT_GATE:                     MANDATORY SENIOR REVIEW
```