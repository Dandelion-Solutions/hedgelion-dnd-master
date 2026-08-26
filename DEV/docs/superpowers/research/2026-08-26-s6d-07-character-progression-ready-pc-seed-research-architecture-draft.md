# S6D-07 Step 2 — Character Progression and READY_PC Seed — Research & Architecture Draft

Status: **EVIDENCE COMPLETE FOR STEP-3 SCOPE DECISION — NO MACHINE CHANGE STARTED**

Pinned remote ref: `f8cfcdd3166f4bc5306f47c37c9da5730d01929e`

## 1. Source Manifest result

The current process owners, PROJECT_MAP, roadmap, S6D owner/task/plan, S6D-01 through S6D-06 owners, current Character/Readiness/Onboarding/Advancement/Durability/Mechanics-Integrity owners, Actor/Asset/Effect/catalog owners, character definition schemas, `world-actor-state`, `entity-structures`, GAME PC/player schemas, readiness regression cases and relevant conformance tests were inspected at the pinned ref. The repository tree was enumerated for character, choice, advancement, package and seed artifacts.

Official SRD evidence was consulted only to establish the legal/public-baseline boundary: SRD 5.2.1 is published for reuse under CC BY 4.0 with required attribution. No external wording or content has been copied into HDM.

## 2. Established facts

### 2.1 Package/content state

- S6D-02 requires one built-in profile: `hdm.rules.dnd2024-srd52-core`, compatibility `hdm.rules.dnd2024-srd52.v1`, generation `2.0.0`.
- Its required semantic root `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/` does not exist at the pinned tree.
- The repository contains no concrete `species.*`, `background.*`, `class.*`, `subclass.*`, `feat.*`, `feature.*`, `spell.*` or `advancement.*` definition instances. Current IDs in schema examples are illustrative, not admitted seed content.
- The package is correctly `selectable_now=false`; S6D-11 retains manifest/lock/digest/builder/loader proof.

### 2.2 Existing schema capability

- Strict definition roots exist for all eight S6D-07 families.
- `build-choice-slot.schema.json` already carries stable `choice_id`, closed inline options, cardinality, defaults and decision policy.
- Actor build stores class progression, species/background IDs, choice bindings and known/prepared/spellbook sets without a flattened derived sheet.
- Gaps remain: cross-slot/global stable-ID uniqueness is compiler-only; option prerequisites/acquisition boundary/owner revision are not explicit; generic `build_parameters` can hide domain-specific grants; no machine READY_PC predicate/evidence contract exists; no concrete definitions exercise the model.

### 2.3 Canonical readiness law

- Harmless or locally sufficient provisional gameplay may precede READY_PC.
- READY_PC is the reconstructable initial mechanical commitment frontier for unrestricted mechanics-capable play, not a full dossier predicate.
- Initial material choices must close before situational exposure. Genuine later advancement/preparation choices are future evolution.
- `CHARACTER_READINESS_CASES.md` C08 says no first live scene before READY_PC and is stale regression debt against the current canonical law.

### 2.4 Projection debt

- `world.actor` plus referenced definitions, Assets and Effects is mechanical authority.
- `GAME/SCHEMA/pc.schema.yaml` still exposes flattened mechanics, inventory, knowledge and relationships. Its own invariant marks these non-authoritative projection/input surfaces pending S6D-07 and Round-2 migration.
- `player.schema.yaml` owns player/PC control binding and policy/presentation preferences, not character mechanics.
- Therefore S6D-07 must either define and test an explicit derived PC projection or remove/reroute duplicate fields/readers; it cannot certify the current flattened schema as authority.

### 2.5 S6D-06 dependency

- All 31 Activity primitives are quarantined and unconditionally rejected.
- `spell-definition-data.schema.json` requires one or more `activity_ids`; meaningful class/features may also reference Activities/resources/effects.
- A concrete character definition may reference only active admitted dependencies. A seed consumer alone cannot activate a primitive draft.
- Consequently a supported spellcaster/executable feature seed either requires independently completing the exact primitive contracts it consumes or must remain nonselectable.

## 3. Item-level disposition of Step-2 evidence products

| Product | Current evidence disposition |
|---|---|
| Definition-family census | 8 schema families exist; 0 concrete package definitions found. |
| Grant/choice matrix | Schema capability exists; no real slots/options to inventory. |
| Initial commitment matrix | Canonical prose is complete enough to frame it; no executable predicate or seed fixtures exist. |
| Advancement matrix | Schema supports initial/level stages; no entitlement/pending/publication realization or concrete advancement instance exists. |
| Representative cases | Prose cases exist; no concrete valid definition graph supports them. |
| PC/player projection ledger | Duplicate projection debt is explicitly acknowledged but not machine-reconciled. |
| Cross-owner graph | Owners are identifiable; executable leaves are absent/quarantined. |
| Verification | Existing tests prove structural Actor separation, not a reconstructable supported D&D character seed. |

## 4. Architecture consequences already determined

Regardless of content breadth, the safe architecture is:

1. reusable definitions own grants and choice slots;
2. Actor stores sparse owner-relative bindings and progression anchors;
3. package snapshot pins the option universe;
4. READY_PC validator derives closure from Actor + definitions + Assets/Effects and returns typed missing/invalid dependencies, without becoming a state owner;
5. later advancement uses a separate acquisition boundary; it cannot reopen initial choices;
6. PC schema is a derived projection/input compatibility surface only, or its duplicate fields are removed;
7. no quarantined Activity primitive is bypassed;
8. exact seed content and attribution live in the package, not in GAME prose.

## 5. Residual material decision

Repository evidence does not define how much concrete SRD character content the built-in package must support at S6D closure. Three materially different scopes remain:

- full SRD 5.2.1 character corpus;
- bounded MVP vertical slice sufficient to prove initial creation and advancement;
- architecture/conformance fixtures only, leaving the built-in package nonselectable.

This affects public product capability, workload, package identity expectations, S6D-08/09 breadth and whether S6D-06 primitive contracts must be completed now. It cannot be inferred mechanically.

## 6. Completeness gate

- relevant owner/dependency subgraph inspected: yes;
- enumerated Task-Brief evidence products accounted: yes;
- authoritative owners distinguished from regression/projection artifacts: yes;
- current package/seed absence established from full tree: yes;
- upstream decisions and S6D-06 quarantine reconciled: yes;
- remaining question requires human product-scope judgment: yes.


