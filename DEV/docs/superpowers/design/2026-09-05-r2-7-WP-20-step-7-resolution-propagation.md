# R2.7 WP-20 Step 7 — Resolution and Finding Propagation

Status: **STEP 7 COMPLETE — ALL MATERIAL FINDINGS CLOSED**

Date: 2026-09-05

Inputs:

- Step-5 candidate specification;
- Step-6 whole-project adversarial review.

This record is the mandatory finding-propagation sweep for every Step-6 `SIGNIFICANT` finding and also resolves the recorded `MINOR` findings.

---

## 1. Resolution summary

```text
BLOCKING_OPEN: 0
SIGNIFICANT_OPEN: 0
MINOR_OPEN: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
MATERIAL_REDESIGN_REQUIRED: NO
```

The Step-6 findings strengthened boundaries but did not change the selected architecture. No second Step-6 cycle is required because the repairs are constraint clarifications and current-owner synchronization rather than a new material alternative or authority model.

---

## 2. Finding-by-finding resolution

### F20-01 — multiple valid migration paths

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** final law requires one valid path or an exact target-declared canonical path/order. More than one valid undeclared path returns `INDETERMINATE`. No shortest/newest/lexical tie-breaker exists.

**Architectural consequence:** deterministic path selection is an explicit target support responsibility.

**Propagation:**

- Step-2 draft — already contains ambiguity rule; remains valid provenance.
- Step-3 Decision Brief — recommendation already assumes deterministic exact support; remains valid.
- Step-4 review — explicitly clarifies graph is finite package support.
- Step-5 candidate — normative section 6.4 contains the repair.
- Step-6 finding — current finding record.
- final canonical spec — becomes current final owner.
- `GAME/MIGRATIONS/README.md` — synchronized with ambiguity rule.
- `DEV/TESTS/ENGINE_UPDATE_CASES.md` — regression requirement added.

**Disposition:** CLOSED.

---

### F20-02 — storage/campaign authority collapse

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** storage-format/default-baseline evolution remains storage-owner-only and separately published. Existing-campaign semantic/native migration/adoption remains creator-only. A storage target may be a campaign prerequisite, but transactions and outcomes remain separate.

**Architectural consequence:** no cross-authority atomic super-transaction is introduced.

**Propagation:**

- Step-5 candidate sections 7.1–7.3 already contain repaired law.
- final canonical spec becomes current final owner.
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` receives targeted wording repair.
- `GAME/CORE/ENGINE_UPDATES.md` receives explicit storage/campaign split.
- `GAME/MIGRATIONS/README.md` receives separate-edge rule.
- tests receive separate-authority/partial-success case.

**Disposition:** CLOSED.

---

### F20-03 — same-version Git ancestry treated as released compatibility

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** for released v1.0+ packages:

```text
same semantic engine_version/package_id
OR source commit ancestry
!= compatibility proof
```

Exact digest proves exact artifact identity. Different released bytes require affirmative exact-target compatibility support. Git ancestry remains provenance evidence only and may never by itself authorize silent use/adoption.

Historical 2026-08-18 runtime-selection/update documents retain their storage-baseline separation and exact provenance value but are superseded on released same-version compatibility inference.

**Architectural consequence:** released asset immutability and accepted versioning law are restored consistently.

**Propagation:**

- final canonical spec explicitly owns supersession;
- `GAME/CORE/ENGINE_UPDATES.md` synchronized;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md` gains same-version/ancestry negative case;
- historical amendments remain unchanged as historical design provenance.

**Disposition:** CLOSED.

---

### F20-04 — CLOSED LIVE pending absorption

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** migration requires:

```text
no active LIVE-selected mutable authority
AND
no CLOSED LIVE state awaiting required absorption/reconciliation
```

The branch must be the authoritative durable basis before migration preparation.

**Propagation:**

- Step-5 candidate section 8.2 already repaired;
- final canonical spec owns the law;
- `GAME/CORE/ENGINE_UPDATES.md` and tests synchronized.

**Disposition:** CLOSED.

---

### F20-05 — accepted resumable work compatibility omitted by schema-only reasoning

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** target compatibility includes proof that all current preserved accepted-work closures remain interpretable under their frozen causal/ruleset/package/RNG/currentness evidence. Failure blocks migration/adoption; migration may not rebind/reroll/drop accepted closure.

**Propagation:**

- Step-5 candidate section 8.3 repaired;
- final canonical spec owns the law;
- runtime update guidance and tests synchronized.

**Disposition:** CLOSED.

---

### F20-06 — migration evidence duplicates publication authority / circular final commit identity

**Severity:** SIGNIFICANT

**Agree:** YES

**Resolution:** migration evidence is bounded evidence only. It records source basis, exact target, ordered edge/artifact identities, authorization basis and validation result. The campaign ref/commit established through existing CAS remains authority. A record inside the commit is not required to embed the final containing commit hash.

**Propagation:**

- Step-5 candidate section 14 repaired;
- final canonical spec owns the law;
- migration README synchronized.

**Disposition:** CLOSED.

---

### F20-07 — derived versus HOT rebuild timing

**Severity:** MINOR

**Agree:** YES

**Resolution:** required branch-persistent derived/index projections may rebuild in the prepared tree before validation/publication; local HOT/SQLite/runtime caches rebuild only after confirmed authoritative publication; asynchronous projections follow native owners.

**Propagation:** final spec + migration/update docs + tests.

**Disposition:** CLOSED.

---

### F20-08 — U17 pre-release legacy-layout implication

**Severity:** MINOR

**Agree:** YES

**Resolution:** U17 is reframed around a **released v1.0+ source layout**. Layout changes occur only when an explicit applicable migration edge declares them. No pre-release/v0.8 layout support is implied.

**Propagation:** `DEV/TESTS/ENGINE_UPDATE_CASES.md` targeted repair.

**Disposition:** CLOSED.

---

## 3. Current-owner synchronization plan executed at Step 8

The following current surfaces must be synchronized in the same coherent Step-8 checkpoint:

1. `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` — one final implementation-facing WP-20 owner.
2. `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — campaign migration creator/storage-owner wording repaired.
3. `GAME/CORE/ENGINE_UPDATES.md` — released-v1+ classification/ancestry/LIVE/accepted-work/publication law aligned.
4. `GAME/MIGRATIONS/README.md` — explicit edge/path/reverse/publication/storage laws aligned.
5. `DEV/TESTS/ENGINE_UPDATE_CASES.md` — architecture-level regression catalog aligned.
6. `DEV/CURRENT_PROGRESS.md` — global cursor moved to Step-8 complete / mandatory Senior review pending.
7. Step-8 canonicalization record — records final self-review and exact next gate.

The roadmap does not require an edit because WP-20 scope/sequence/dependencies did not change. `DEV/PROJECT_MAP.md` does not require an edit because it already routes update/migration to the same owner families and homogeneous final-spec directory. The canonical architecture index is derivative and no current route becomes misleading without a per-WP entry.

`DEV/PRODUCT_OWNER_INPUT.md` PO-004 remains immutable Product Owner intent/routing evidence. Its product semantics are fully incorporated by the final spec; no verbatim owner input is rewritten as part of architecture synchronization.

---

## 4. Supersession / retained-history accounting

### Current accepted law retained unchanged

- v1.0 clean-slate compatibility decision;
- versioning namespace/compatibility policy;
- versioning machine-realization status amendment;
- WP-19 creation semantics;
- WP-10…16 existing owners;
- ruleset package identity/compatibility owners;
- existing persistence/recovery/CAS authority.

### Historical design retained but materially qualified

`DEV/docs/superpowers/specs/2026-08-18-runtime-selection-and-storage-baseline-amendment.md` and related 2026-08-18 update design provenance remain historically accurate for how earlier runtime update behavior was developed.

For **released v1.0+** compatibility, their rule that same-version proven Git ancestry itself authorizes compatible forward refresh is superseded by WP-20 final law. Their following concepts remain valid where not otherwise superseded:

- storage baseline and campaign current identity are separate authorities;
- local runtime root is ephemeral;
- exact package-carried provenance is preferable to mutable tag inference;
- non-creator cannot persist creator-owned campaign adoption identity.

Historical artifacts are not rewritten as if they originally contained the later correction.

---

## 5. Finding-propagation completeness

For every `SIGNIFICANT` Step-6 finding, this record identifies:

- finding and current disposition;
- affected candidate/final owner;
- current runtime/architecture/test/status surfaces requiring synchronization;
- whether historical material remains historical and how its current applicability is qualified.

After the Step-8 coherent synchronization checkpoint, one current final owner will exist for every changed normative statement.

```text
STEP_7_COMPLETE: YES
BLOCKING_OPEN: 0
SIGNIFICANT_OPEN: 0
FINDING_PROPAGATION_SWEEP: COMPLETE / PENDING STEP-8 PUBLICATION OF SYNCHRONIZED FILES
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
STEP_8_ALLOWED: YES
```
