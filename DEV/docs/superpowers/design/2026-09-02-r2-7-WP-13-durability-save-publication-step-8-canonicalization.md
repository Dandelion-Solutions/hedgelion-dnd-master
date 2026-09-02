# R2.7 WP-13 — Durability / SAVE / Publication — Step 8 Canonicalization

Status: **STEP 8 COMPLETE — MANDATORY FINAL SENIOR AUDIT REQUIRED**

Date: 2026-09-02

Final canonical artifact:

- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`

Derivation chain:

- repaired Step-1 Task Brief / Source Manifest / critic;
- `SR13-01` Senior recovery;
- Step-2 evidence extraction + Source Manifest expansion;
- Step-3 Decision Brief;
- Step-4 collaborative review;
- Step-5 candidate specification;
- Step-6 whole-project adversarial review;
- Step-7 resolution gate;
- final canonical specification above.

---

## 1. Step-8 result

WP-13 selects one implementation-facing realization direction:

> **SCOPE-EVALUATED NATIVE-DOMAIN DURABILITY COMPOSITION + IMMUTABLE EPHEMERAL PUBLICATION ATTEMPTS**

The result realizes already-accepted Step-5 / R2.6 / WP-11 / WP-12 architecture. It does not add a new gameplay owner, distributed transaction, global durability frontier, publication journal, transport alternative, checkpoint authority or chronology source.

---

## 2. Canonicalized machine boundaries

The final specification now fixes these realization laws:

- establishment remains distinct from durability;
- durability obligation is scope-relative and owner-triggered;
- no campaign-global one-hour/frontier/save-clock/HARD-queue architecture;
- scope risk-control exposure follows actual oldest still-relevant unpublished state and remains MAY_DEFER unless another owner supplies a HARD edge;
- required durable source closure is distinct from physical pending write set;
- explicit SAVE composes admitted native durability domains without distributed transaction/global order;
- domain no-write requires operation-current compatible closure, not stale local cleanliness;
- overall SAVE/HARD success requires one current compatible participating-source composition at the acknowledgement boundary;
- partial native-domain publication remains real while overall SAVE may remain incomplete;
- SAVE quiescence has explicit success/failure/indeterminate release behavior;
- campaign publication attempt freezes immutable exact owner/auth/currentness/dependency/path basis before first remote Git-object mutation;
- trustworthy application principal evidence is required independently of technical repository write capability;
- WP-11 exact UPSERT/DELETE + required index/projection companions share campaign publication closure;
- bounded resulting-tree proof precedes remote mutation;
- semantic no-op delta creates no campaign write only after current closure proof;
- shipped transport remains R2.6 `Python/core -> GitHub Connector -> non-force ref transition` with no runtime fallback/probing;
- one campaign durability boundary uses one base-derived tree + one single-parent commit;
- final ref transition preserves `CONFIRMED_ACCEPTED / CONFIRMED_REJECTED / INDETERMINATE` epistemics;
- confirmed rejection cause is classified before retry/failure handling;
- indeterminate result cannot acknowledge/clear/release/replay/blind-retry;
- ambiguity uses bounded current-ref + lineage/current-closure evidence;
- semantic conflict footprint includes paths, owners, reads/dependencies, authorization/routing and recovery/reference dependencies;
- proven-disjoint movement rebuilds transport basis without replaying accepted mechanics/IDs/RNG;
- relevant overlap requires native-owner reconciliation/revalidation, never generic text merge;
- retry is bounded;
- G-specific adoption preserves G+1;
- crash after remote success/local adoption loss recovers from actual native authority without generic journal/gameplay replay;
- live exact-source CAS, checkpoint optionality, storage metadata separation and engine-update authority remain with their existing owners.

---

## 3. Step-6 findings and Step-7 closure

The mandatory Step-6 whole-project critic found:

```text
F01 BLOCKING    final current compatible source-composition proof
F02 BLOCKING    operation-current NO_WRITE_NEEDED proof
F03 SIGNIFICANT trustworthy acting-principal/delegation source
F04 SIGNIFICANT confirmed rejection cause classification
F05 SIGNIFICANT SAVE quiescence release/abandonment
F06 SIGNIFICANT risk-control exposure must remain MAY_DEFER
```

Step 7 resolved every item mechanically from accepted authority.

Final state:

```text
STEP_6_BLOCKING:         2
STEP_6_SIGNIFICANT:      4
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPENED:       NO
```

---

## 4. Source Manifest closure

The repaired Step-1 manifest remained open-world during Step 2.

Step 2 added real direct consumers:

- `GAME/CORE/ENGINE_UPDATES.md`;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md`.

It also promoted conditionally routed canonical evidence to direct inspected constraints where triggered:

- Step 5.1 frontier/domain typing;
- Step 5.9 chronology order prohibition;
- Step 5.13 prepared-object/cleanup boundary.

No additional source gap remained before synthesis.

`SR13-01` remained a mandatory cross-stage input throughout Steps 2–8: gameplay repository transport selection stays closed, and development-agent rules are not substituted for shipped runtime architecture.

---

## 5. Cross-system consistency review

### Step 5.2 / 5.5 / 5.7

Final SAVE success is a bounded current compatible native-source closure, not a global snapshot/frontier. CONSISTENT.

### Step 5.6

Frozen attempt, resulting-tree proof, tri-state ref outcome, ambiguity verification, semantic conflict footprint and G-specific adoption are preserved/refined, not replaced. CONSISTENT.

### R2.6

The only supported shipped repository path is deterministic Python/core + GitHub Connector + non-force authoritative ref transition; capability failure never authorizes alternate runtime transport. CONSISTENT.

### WP-11

Known-ID direct routing is preserved. Native record and required index/projection UPSERT/DELETE companions remain one campaign publication closure without making indexes authoritative. CONSISTENT.

### WP-12

Owner-generation dirty bookkeeping remains scope-relative; no global timer/frontier is reintroduced; publication clears exact frozen G only; repository I/O remains outside SQLite; live pre-CAS remains non-current. CONSISTENT.

### Access / multiplayer / House Rules

Application authorization remains independent of repository capability; trustworthy principal evidence is consumed, not redefined. Named membership/policy HARD edges retain their owners. CONSISTENT.

### Checkpoint / live / chronology / cleanup

Checkpoint remains optional evidence, live exact-source CAS remains authoritative, Git order is not fictional chronology, prepared object cleanup is not publication authority. CONSISTENT.

### Engine updates

Campaign engine/rules adoption/provenance is a publication consumer after its own owner gates; storage baseline remains separate. CONSISTENT.

---

## 6. Current machine impact

No runtime/schema/catalog/test implementation was changed in Steps 2–8.

The canonical spec explicitly routes later implementation repair for current debt including:

- `DURABILITY_GUARD.md` one-hour/global `durable_frontier_time` contract;
- `SAVE_CONTRACT.md` campaign-only universal SAVE framing;
- `PERSISTENCE.md` incomplete frozen/currentness/ambiguity/rejection/G-specific machine contract;
- `STORAGE.md` global durable-frontier-time support;
- stale `EXPLICIT_SAVE_CASES` campaign-only/blanket-clear cases;
- stale `PERSISTENCE_TRANSACTION_CASES` blanket-clear/old-live cases;
- `test_hourly_durability_contract.py` noncanonical global timer assertions;
- R2.6 fixed-Connector currentness/CAS/conflict/failure/capability coverage;
- engine-update publication consumer regressions.

Executable changes remain later implementation/WP-22 work after the required architecture/planning gates.

---

## 7. Downstream obligations

- **WP-14:** checkpoint/recovery machine must consume current-authority-first native sources; checkpoint cannot become SAVE proof.
- **WP-16:** final live realization must preserve exact-source CAS/currentness/outcomes and fixed Connector path.
- **WP-19/WP-20:** bootstrap/migration may consume publication machinery but cannot weaken authority/durability/currentness.
- **WP-22:** executable conformance/failure-injection coverage for all WP-13 laws, including Step-7 repairs and R2.6 transport.
- **WP-24:** measure before optimizing publication/closure/Connector costs.
- **WP-26:** existing Storage-v2 prose consistency remains separate.
- **implementation planning:** exact APIs/local metadata/retry bounds/errors only after architecture authorization.

These routes do not authorize those domains now.

---

## 8. Final self-review

```text
[x] Step-1 repaired package + SR13-01 preserved
[x] Step-2 Source Manifest expansion recorded
[x] Step-2 completeness gate passed before synthesis
[x] Step-3 alternatives/tradeoffs/recommendation documented
[x] Step-4 collaborative refinements incorporated
[x] Step-5 candidate written before adversarial critic
[x] Step-6 whole-project critic itemized findings
[x] Step-7 all BLOCKING/SIGNIFICANT findings mechanically resolved
[x] final canonical source contains Step-7 amendments
[x] no human-owned product/authority/risk decision remains
[x] no upstream architecture reopened without contradiction
[x] no runtime/schema/catalog/test implementation changed
[x] no WP-14 work started
[x] no implementation planning started
[x] final next gate is mandatory Senior final audit
```

---

## 9. Step-8 gate

```text
WP-13_STEPS_2_8:          COMPLETE
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
NEXT_GATE:                MANDATORY SENIOR FINAL AUDIT
```

Do not start WP-14 or implementation planning before the mandatory Senior final audit and explicit subsequent authorization.