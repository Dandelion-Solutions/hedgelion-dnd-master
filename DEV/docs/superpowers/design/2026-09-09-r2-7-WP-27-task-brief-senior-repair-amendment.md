# R2.7 WP-27 Step 1 — Task-Brief Senior Repair Amendment

Status: **CURRENT STEP-1 FRAMING AMENDMENT / CLOSES SENIOR SELF-REVIEW FINDINGS SR27-S1-01..04**

Date: 2026-09-09

Amends:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-task-brief-source-manifest.md`.

Review source:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-step-1-senior-self-review.md`.

This amendment changes only WP-27 audit framing/process/source coverage. It introduces no runtime/product semantics, no implementation authorization and no new semantic owner.

Where this amendment conflicts with the earlier Task Brief wording for the four scopes below, this amendment controls.

---

# 1. SR27-S1-01 — Round-2 item-level disposition continuity

Add the following mandatory Step-2 evidence obligation after `R27-E06`.

## R27-E07 — Round-2 DIAMOND/STRONG disposition continuity

WP-27 shall preserve and reconcile the mandatory Round-2 sub-ledger at **item level**:

```text
all 82 R2.1-R2.6 DIAMOND / STRONG dispositions
+ later S14 / S53 / D15 changes
```

For every item retain, where applicable:

```text
item ID
accepted current disposition
owning current source / later supersession
activation state
implementation consequence
verification/scenario/empirical consequence
dormant/revisit trigger
rejected/negative constraint
whether current machine realization already satisfies any part
```

The DIAMOND/STRONG ledger is completeness evidence, not architecture authority. Current owning canonical sources and later accepted amendments/owner decisions remain controlling.

WP-27 must not collapse the 82-item set into a thematic statement such as “Round 2 covered”.

The WP-27 mini-report and later readiness synthesis shall explicitly state the current accounting/delta for this mandatory sub-ledger.

---

# 2. SR27-S1-02 — Current machine/source family expansion

Amend Task Brief section `6.11 Current machine/runtime realization families` so the open-world machine/reverse-conformance family includes, in addition to the already listed paths:

```text
GAME/TEMPLATE/*
GAME/ENGINE_VERSION.yaml
DEV/ENGINE_DEVELOPMENT.yaml
```

The complete current discovery family is therefore at least:

```text
GAME/CORE/*.md
GAME/SCHEMA/*
GAME/CAMPAIGN/*
GAME/TEMPLATE/*
GAME/INSTALL/*
GAME/RULES/*
GAME/MIGRATIONS/*
GAME/TOOLS/*
GAME/ENGINE_VERSION.yaml

DEV/ARCHITECTURE/*
DEV/CATALOG/*
DEV/SCHEMAS/*
DEV/TESTS/*
DEV/TOOLS/*
DEV/RELEASE/*
DEV/ENGINE_DEVELOPMENT.yaml
.github/workflows/*
```

This remains a discovery family, not a demand to read every file front-to-back. Step 2 expands through owner/dependency evidence and current machine responsibilities.

Top-level legal/runtime publication surfaces remain in the existing release/version/legal family and are inspected when their owner/consumer route is implicated.

---

# 3. SR27-S1-03 — WP-27 durable mini-report/control plane

The active WP-27 domain shall maintain:

- `DEV/docs/superpowers/research/2026-09-09-r2-7-WP-27-final-implementation-planning-readiness-mini-report.md`.

It is the domain-local durable execution/evidence checkpoint required by the R2.7 execution protocol. It does not replace the Task Brief, canonical owners, `DEV/CURRENT_PROGRESS.md`, or the task-local R2.7 cursor.

Fresh-session WP-27 recovery shall include the current mini-report after loading the R2.7 audit cursor.

The mini-report must preserve at least:

```text
status / current slice
Source Manifest delta
established facts
architecture -> machine accounting
machine -> architecture accounting
conflicts / stale / negative findings
automatically resolved technical decisions
implementation obligations
verification / scenario / empirical / release forward obligations
Round-2 DIAMOND/STRONG delta
human decision
closure verdict
exact continuation point
```

---

# 4. SR27-S1-04 — Post-Senior continuation semantics

The earlier Task Brief sentence that makes Steps 2–8 eligible for **separate authorization** after Step-1 Senior PASS/GO is superseded.

Current governing process is:

```text
Product Owner WP-27 stage-entry authorization
-> Step 1 complete
-> mandatory Step-1 Senior review

if PASS / GO and no genuine human-owned decision remains:
    existing WP-27 stage authorization resumes
    -> AUTO_CONTINUE through Steps 2–8 under the normal deep-work loop

if a genuine human-owned decision appears:
    -> stop only at that actual decision gate
```

Genuine human-owned gates remain limited to the current process classes, including:

```text
PRODUCT_SEMANTICS
ARCHITECTURE_TRADEOFF
AUTHORITY_CHANGE
COMPATIBILITY_POLICY
RISK_ACCEPTANCE
SCOPE_CHANGE
SUPERSESSION
```

Do not manufacture another approval pause for mechanical mapping, schema detail implied by accepted owners, test mapping, traceability, dependency decomposition or implementation-neutral representation choices.

This continuation law does **not** bypass:

```text
WP-27 final Step-8 Senior stop
R2.7 final reconciliation
implementation-planning entry resolution
explicit implementation execution process/gates
```

Implementation planning remains blocked until R2.7 final reconciliation passes.

---

# 5. Repaired Step-1 package disposition

After publication of the required WP-27 mini-report and successful Senior re-review, the Step-1 package shall be interpreted as:

```text
SOURCE_MANIFEST_OPEN_WORLD: YES
TASK_BRIEF_OWNER_DERIVED: YES
WORKER_WIDE_ANGLE_CRITIC_CLOSED: YES
SENIOR_SELF_REVIEW_FINDINGS: 4 SIGNIFICANT
SENIOR_SELF_REVIEW_FINDINGS_REPAIRED: 4 / 4
HUMAN_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
PRODUCT_OWNER_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
WP27_STEP2_STARTED_DURING_REPAIR: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

The final Step-1 PASS/GO remains contingent on the documented Senior self-re-review and fresh verification evidence.