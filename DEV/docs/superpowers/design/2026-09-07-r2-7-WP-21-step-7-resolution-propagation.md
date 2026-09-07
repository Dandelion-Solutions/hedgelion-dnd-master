# R2.7 WP-21 Step 7 — Resolution & Finding Propagation

Status: **STEP 7 COMPLETE — ALL STEP-6 FINDINGS CLOSED**

Date: 2026-09-07

Domain: **Diagnostics, observability, cleanup and retirement**

Inputs:

- Step-5 candidate specification;
- Step-6 whole-project adversarial review (`F21-201..F21-208`).

This step resolves and propagates every Step-6 finding. No finding requires a Product Owner decision, material redesign or semantic change to an upstream native owner.

---

## 1. Finding dispositions

### F21-201 — authorization vs disclosure

**CLOSED.** Final WP-21 law preserves two independent gates:

```text
operation authorization
!=
recipient information eligibility
```

Campaign creator authorization cannot expose otherwise ineligible player-local/private data. Redact/withhold/omit and disclose the limitation.

Propagation owner: final WP-21 canonical composition spec. Existing `ACCESS_CONTROL.md`, Step 5.12 and Step-1-repaired `MAINTENANCE_COMMANDS.md` already conform; no further owner edit required.

### F21-202 — false universal diagnostic frontier

**CLOSED.** Every material diagnostic claim remains owner-qualified. Independently writable owner evidence is never collapsed into one diagnostic revision/frontier; indeterminate cross-domain composition is reported as such.

Propagation owner: final WP-21 canonical spec. No new runtime/global currentness owner.

### F21-203 — generic physical removal vs PO-006

**CLOSED.** Git branch/ref is a hard exclusion from every physical-removal path. Native owners cannot opt a ref back into deletion through generic cleanup. Logical retirement/de-routing is final HDM action; physical residue may persist indefinitely.

Propagation owners: PO-006 + logical-ref amendment remain upstream; final WP-21 spec consumes them. No Connector capability probe or runtime edit.

### F21-204 — WP-17 terminal routing vs obligation retention

**CLOSED.** WP-17 terminal transition removes current PLAYER route companions as owned by WP-17, but obligation-record cleanup remains `RETAIN` until an explicit machine-realized enrollment proves protection/survivor obligations. Terminality alone is insufficient.

Propagation owner: final WP-21 composition spec. WP-17 semantics unchanged; exact schema/route machine debt remains deferred.

### F21-205 — WP-18 current retained horizon

**CLOSED.** Planning cleanup must use WP-18 current generation plus mode/membership/control/source/shared-basis validation. Current retained planning is not removable by age alone. Source invalidation causes invalidate/recompute under WP-18; planning cannot recreate canon.

Propagation owner: final WP-21 composition spec. WP-18 owner unchanged; exact horizon schema debt remains deferred.

### F21-206 — stale dry-run/report

**CLOSED.** A diagnostic/dry-run result is evidence bound to its observed currentness basis, not a reservation/authorization token. Any destructive cleanup rechecks current authority/currentness/protections/survivor conditions immediately under the owning transaction/publication law.

Propagation owner: final WP-21 composition spec.

### F21-207 — enrollment vs global registry

**CLOSED.** Late-family cleanup enrollment is a semantic completeness obligation, not a physical architecture choice. It may be realized in the native spec/schema/test/tool contract; no universal registry/database is required.

Propagation owner: final WP-21 composition spec.

### F21-208 — architecture coverage vs machine completion

**CLOSED.** Final artifacts explicitly preserve deferred realization:

- WP-17 obligation schema/fields + PLAYER collaboration route realization;
- WP-18 retained shared/player horizon schemas/value contracts;
- installed maintenance-command dispatcher/result enums;
- executable authorization/disclosure/redaction cases for that future command surface;
- family-specific automated cleanup tooling where absent;
- exact diagnostic serialization if later required.

No Step-7 action activates that debt.

---

## 2. Mandatory propagation sweep

| Surface | Finding relevance | Step-7 action |
|---|---|---|
| final WP-21 canonical spec | all findings | **CREATE as current WP-21 composition owner** |
| `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` | F21-201/F21-206/F21-208 | no edit — Step-1 recovery already says routing != auth, recipient-filtered, proposal/not-installed |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | F21-201 | no edit — current owner already requires creator authorization for explicit global maintenance |
| Step 5.12 canonical spec | F21-201 | no edit — current disclosure owner already forbids auxiliary leakage |
| Step 5.13 canonical + logical-ref amendment | F21-203/F21-206 | no edit — existing generic cleanup + superseding PO-006 ref law already sufficient |
| WP-17 canonical spec | F21-204/F21-208 | no edit — terminal routing and deferred machine debt preserved |
| WP-18 canonical spec | F21-205/F21-208 | no edit — retained planning currentness/recompute and deferred schemas preserved |
| WP-20 canonical spec | cleanup/migration boundary | no edit — migration remains separate and already forbids opportunistic cleanup transformation |
| `GAME/CORE/*` runtime consumers | composition consumers | no edit — no runtime implementation authorized |
| `GAME/SCHEMA/*` | machine debt | no edit — no schema realization authorized |
| tests/tooling | future realization | no edit — current tests remain valid; new runtime-specific tests wait for implementation authorization |
| `DEV/CURRENT_PROGRESS.md` | global cursor | synchronize at Step 8 |

Historical design artifacts remain provenance; they are not rewritten.

---

## 3. Final architecture delta from candidate

No selected alternative changed. Step 7 strengthens final wording around:

1. creator authorization vs recipient disclosure;
2. owner-qualified diagnostic currentness;
3. type-level Git-ref physical-delete exclusion;
4. WP-17 terminal routing vs record retention;
5. WP-18 current retained-horizon protection/recompute;
6. dry-run revalidation;
7. enrollment-as-contract, not registry;
8. explicit machine-debt status.

This is not material redesign, so a second Step-6 cycle is not required.

---

## 4. Resolution gate

```text
F21-201: CLOSED
F21-202: CLOSED
F21-203: CLOSED
F21-204: CLOSED
F21-205: CLOSED
F21-206: CLOSED
F21-207: CLOSED
F21-208: CLOSED

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
UNRESOLVED_MINOR: 0
MATERIAL_REDESIGN: NO
REPEAT_STEP_6_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_8_READY: YES
```
