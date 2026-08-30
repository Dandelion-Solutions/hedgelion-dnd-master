# Campaign House Rules — Step 3 Decision Brief — Amended After Senior Audit

Status: **STEP 3 REOPENED / MATERIAL HUMAN DECISIONS REQUIRED / STEP 4 BLOCKED**

Date: 2026-08-25

Supersedes for the current decision gate:

- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-3-decision-brief.md`

Evidence basis:

- Step-1 Task Brief;
- original Step-2 research;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`;
- current machine contracts/tests inspected and materialized there.

Governance correction:

> The earlier Senior Auditor `GO FOR STEP 2–8` authorized continuation of the design process. It did **not** constitute approval of material architecture alternatives discovered later. The previous Step-3 statement that the owner gate was satisfied by that GO is withdrawn.

No Step-4 collaborative review or later closure gate may proceed until the decisions below are made by the human architect.

---

# 1. FACT / inherited architecture

The following are already accepted or directly established by current owning sources and are **not** being reopened:

1. LLM/Master semantic judgment is separate from deterministic execution authority.
2. LLM/prose does not own RNG, direct canonical state mutation or native owner bypass.
3. Current authorized campaign policy may make a stale baseline mechanical realization insufficient; stale code/definition text is not constitutional authority.
4. If no admitted deterministic realization exists, execution stops with a finite gap rather than granting prose execution authority.
5. Physical information availability does not create role/consumer information eligibility.
6. House Rules content is scoped gameplay-policy data below host/project/CORE constitutional instruction authority.
7. Context Runtime owns bounded discovery/currentness/eligibility/allocation; indexes/caches remain routing-only.
8. House Rules introduces no global policy epoch/frontier.
9. Multiplayer propagation is authoritative publication/currentness plus context assembly, not chat-copy synchronization.
10. Accepted policy-dependent causal inputs remain frozen across retry/recovery; later policy publication is forward-looking.
11. Structured promotion is optional and may not duplicate deterministic ownership.
12. ACCESS_CONTROL determines write/identity authorization but does not currently define semantic campaign-policy adoption authority.
13. ADJUDICATION distinguishes temporary/local rulings from table-adopted permanent rules but does not define who may perform that adoption.
14. Current registered `INVOCATION_ADJUDICATED` context facts are boolean and remain intentionally so.
15. Current WP-06 Activity parameter declarations already provide a distinct richer invocation-specific value surface.

These facts constrain the decision space.

---

# 2. DERIVABLE mechanical detail

The following does not require a new product-semantic decision and has been materialized under the owner's clean-slate pre-release structural authorization.

## 2.1 Richer semantic-value channel

Use the existing Activity parameter declaration as the only initial richer adjudicated-value consumer.

Initial admitted `INVOCATION_ADJUDICATED` values:

- boolean;
- bounded integer;
- bounded number;
- bounded/admitted `machine_id` selection.

Do not widen boolean Rule Element/context-fact predicates into a general typed variable language.

## 2.2 Accepted evidence shape

A richer accepted adjudicated binding carries:

```text
value
provenance_ref
eligibility_basis_fingerprint
rules_context_fingerprint
policy_basis_refs[]
candidate_set_fingerprint? when dynamic bounded selection applies
```

The full accepted binding participates in existing RuntimeCommand input identity and is preserved by Resolution/Continuation.

## 2.3 Deterministic validation

The binder validates the selected Activity declaration, type/range/domain/candidate set, consumer eligibility, current rules/policy basis and admitted deterministic realization before command acceptance.

## 2.4 Finite failure outcomes

The current machine vocabulary now includes:

- missing adjudicated input;
- unauthorized input;
- invalid type/range/domain/candidate;
- stale adjudication context;
- unresolved policy conflict;
- policy realization gap.

No arbitrary JSON path, eval/expression/query DSL, free-form object/state injection or prose mutation path is introduced.

## 2.5 Current materialization

Machine-contract commits:

- `c8ed8c1059b5391597e9fb74eaa4311128cfe4ad` — failing contract tests first;
- `dcd19c60796825af79baa3e3b8de4227e018dfd0` — current schema repair.

These details remain valid under any reasonable policy-adoption authority choice below.

---

# 3. MATERIAL HUMAN DECISION H1 — responsibility shape

Step 1 required explicit disposition of responsibility shapes A–E. Evidence narrows the viable choices but does not give the agent authority to choose a subsystem/owner boundary unilaterally.

## A — existing-owner runtime contract + minimal policy conventions

Use existing PLAY_POLICY/ADJUDICATION, Context Runtime, R2.4 role/instruction law, Step-5 publication/currentness and Step-3 deterministic owners. Add only the minimum campaign-policy identity/currentness data needed by those owners.

## B — dedicated narrow runtime policy owner

Introduce a new shipped runtime module/owner specifically for House Rule/Ruling semantics and adoption/application behavior.

## C — structured identity/currentness sidecar

Keep semantic policy human/LLM-readable but add narrow structured identity/revision/currentness/adoption-basis data used by existing runtime owners.

## D — predominantly structured campaign policy

Represent most policy applicability/content structurally, with prose secondary.

## E — prose-only policy with no machine linkage

Use campaign prose only; no stable machine-linked identity/currentness/adjudication basis.

### Evidence disposition

- D is inconsistent with the preserved semantic-layer purpose and risks a second rules engine.
- E cannot satisfy currentness/frozen-input/conflict/typed-handoff requirements.
- B adds a new runtime owner not yet proven necessary.
- A reuses current owners and matches YAGNI.
- C is needed narrowly for identity/currentness/accepted-input linkage but need not become a semantic owner.

### AGENT RECOMMENDATION H1

**Approve `A + narrow C` as the responsibility shape.**

Meaning:

```text
existing runtime owners keep behavioral/authority responsibilities
+
small structured policy identity/currentness/adoption evidence exists where machine linkage is required
```

Reject B/D/E for the baseline. Reopen B only if the selected adoption semantics later prove impossible to express cleanly through existing owners without duplicate responsibility.

### HUMAN DECISION H1

Choose one:

```text
H1-A+C  approve existing-owner runtime + narrow structured sidecar   [RECOMMENDED]
H1-B    require a dedicated narrow runtime House-Rules owner
H1-D    require predominantly structured policy
H1-E    require prose-only policy
H1-OTHER provide another responsibility shape
```

---

# 4. MATERIAL HUMAN DECISION H2 — campaign policy-adoption authority

This is the unresolved product-semantic question exposed by the audit.

The decision concerns **adoption of durable reusable campaign-wide policy**, not ordinary local adjudication.

A lawful Master may still make the smallest bounded local ruling needed to continue play under existing ADJUDICATION law. Adoption answers whether that ruling/proposal becomes a reusable norm that future Masters/players must apply.

## P1 — creator-only policy adoption

### Singleplayer

Campaign creator is the only principal who may adopt permanent House Rules/Rulings.

### Multiplayer

Campaign creator remains the only campaign-wide policy adopter. Other authorized participants/Master sessions may make lawful local rulings but cannot make them normative without creator approval.

### Delegation

No delegation.

### Policy kinds

One authority rule for all durable policy kinds.

### Enforcement

Existing creator identity check + current campaign publication/CAS. Repository write or PLAYER binding alone is insufficient.

### Benefit

Simple and strong authority.

### Cost

Creator becomes a bottleneck and delegated/co-Master operation cannot independently stabilize precedent.

---

## P2 — creator-root authority with explicit scoped delegation

### Singleplayer

Creator is default/root policy authority. They may optionally delegate durable policy-adoption authority.

### Multiplayer

Creator remains root authority. An explicitly delegated authenticated campaign principal may adopt policy within the granted scope; active PLAYER/write authority alone does not imply the grant.

### Creator approval per rule

Not required when a valid delegation already covers the policy kind/scope. Creator may revoke/change delegation prospectively through ordinary authorized campaign publication.

### Delegation target

Reuse existing authenticated campaign principals/current PLAYER binding where applicable. The logical Master role does not require a new persistent “Master entity” solely for this purpose.

### Enforcement

A narrow campaign policy-adoption grant is checked after identity/binding resolution and before authoritative policy publication. Existing Step-5 publication/currentness/CAS then makes an authorized adoption current. This is not a generic ACL subsystem.

### Benefit

Preserves creator sovereignty while allowing real delegated/co-Master operation without per-ruling approval workflow.

### Cost

Requires one narrow semantic delegation surface and a scope decision.

---

## P3 — table/participant consensus adoption

### Singleplayer

Creator is effectively the table.

### Multiplayer

Permanent policy requires explicit consent under a defined participant set/quorum.

### Creator approval

Could be included as mandatory or merely one vote, which itself requires another policy choice.

### Enforcement

Would require durable contribution/consent collection, likely using a new policy-specific use of collaboration semantics.

### Benefit

Strong social legitimacy.

### Cost

Adds coordination latency, quorum/inactivity questions and substantial governance machinery to ordinary precedent stabilization. Existing requirements do not prove this is necessary.

---

## P4 — any authorized Master/session may adopt campaign policy

### Singleplayer

Creator's Master session may adopt directly.

### Multiplayer

Any authenticated gameplay-authorized Master/session may promote a ruling to campaign-wide policy.

### Creator approval/delegation

Neither is required beyond ordinary gameplay/write authority.

### Enforcement

Existing PLAYER/write authorization + publication.

### Benefit

Fastest operational flow.

### Cost

Conflates gameplay-write authority with campaign-legislative authority and permits one participant line to alter norms for all others without explicit grant. This is exactly the ambiguity identified by the Senior Auditor.

---

# 5. MATERIAL HUMAN DECISION H3 — delegation scope if P2 is selected

If H2 selects P2, one additional semantic choice remains.

## S1 — one uniform policy-adoption grant

A delegate may adopt any valid House Rule/Ruling within the campaign.

**Benefit:** simplest.

**Risk:** an authority granted mainly to stabilize contextual precedents also permits broad baseline mechanical overrides.

## S2 — two scoped grants

Distinguish at least:

```text
INTERPRETIVE_POLICY
    contextual applicability, stable precedent, semantic interpretation

MECHANICAL_OVERRIDE_POLICY
    deliberate campaign rule that changes baseline mechanical cost/threshold/
    activation/consequence semantics and may require a different structured realization
```

Default proposal:

- creator owns both;
- an `INTERPRETIVE_POLICY` delegation may be granted independently;
- `MECHANICAL_OVERRIDE_POLICY` remains creator-only unless the creator explicitly grants that stronger scope;
- neither scope bypasses deterministic realization/currentness rules.

This is an authority classification, **not** a second mechanical taxonomy or execution engine.

### AGENT RECOMMENDATION H2/H3

**Select P2 + S2.**

Rationale:

1. creator remains the root semantic owner of campaign-wide norms;
2. co-Master/delegated operation remains practical;
3. ordinary stable rulings do not need per-rule creator bureaucracy after delegation;
4. broad mechanical house-rule changes have a larger campaign-wide blast radius and deserve a stronger explicit grant;
5. enforcement can reuse existing authenticated identity/binding + publication/CAS rather than inventing generic ACL or voting infrastructure.

### HUMAN DECISION H2/H3

Choose:

```text
H2-P1        creator-only adoption
H2-P2-S1     creator-root + delegable, one uniform adoption scope
H2-P2-S2     creator-root + delegable, split interpretive/mechanical scopes   [RECOMMENDED]
H2-P3        table/participant consensus
H2-P4        any gameplay-authorized Master/session may adopt
H2-OTHER     another explicit authority model
```

---

# 6. Enforcement shape after human choice

The architecture deliberately separates semantic authority from transport permission.

Whichever H2 answer is selected, enforcement should reuse:

```text
authenticated GitHub/campaign identity
    -> creator or active PLAYER binding resolution
    -> selected narrow policy-adoption authority check
    -> current policy source/base check
    -> existing campaign publication/CAS
    -> Context Runtime current policy acquisition
```

Do not add a generic role/ACL graph merely to implement policy adoption.

Exact configuration/schema fields for P2 delegation are **not** materialized before H2/H3 because their meaning depends on the human authority decision. Once selected, those fields are derivable machine detail and should be materialized before Step 4 continues.

---

# 7. GAME runtime-surface disposition

`GAME/CAMPAIGN/RULES/HOUSE_RULES.md` is classified as an intentionally required runtime-facing policy projection, not an implementation of the House-Rules subsystem.

It may state the already accepted purpose/limits of House Rules because the runtime Master must know those limits. It must **not**:

- claim policy-adoption authority is already defined;
- claim retrieval/conflict/currentness enforcement already exists merely because prose says so;
- depend on DEV artifacts being shipped in the runtime package.

The current GAME wording will be narrowed accordingly while the architecture remains on HOLD.

---

# 8. Exact gate state

```text
FACTS / INHERITED ARCHITECTURE: ESTABLISHED
DERIVABLE RICHER MACHINE CONTRACT: MATERIALIZED
RESPONSIBILITY SHAPE: HUMAN H1 REQUIRED
POLICY ADOPTION AUTHORITY: HUMAN H2 REQUIRED
DELEGATION SCOPE IF P2: HUMAN H3 REQUIRED
STEP 4: BLOCKED
STEP 5-8 PRIOR ARTIFACTS: HISTORICAL CANDIDATES / NOT CURRENT CLOSURE AUTHORITY
S6D: NOT STARTED
R2_7_WP06: PAUSED
```

No inference should convert silence or the earlier `GO FOR STEP 2–8` into these decisions.
