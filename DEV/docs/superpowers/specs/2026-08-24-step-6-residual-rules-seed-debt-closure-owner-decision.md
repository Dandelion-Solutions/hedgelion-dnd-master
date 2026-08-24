# Step 6 Residual Rules/Seed Debt Closure — Owner Decision

Status: **OWNER-APPROVED PROGRAM SEQUENCING DECISION**

Date: 2026-08-24

Applies to:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- active R2.7 whole-project audit state;
- residual obligations historically deferred to former Step 6 by Steps 1–2;
- current WP-06 rules/adjudication/domain audit findings.

## 1. Decision

The owner pauses R2.7 at WP-06 and inserts one bounded debt-closure workstream before the audit continues:

```text
S6D — Step-6 Residual Rules/Seed Debt Closure
```

S6D is prepared now and executed only after the current architecture discussion is complete and the owner asks to start it.

After S6D closes, R2.7 resumes from the saved WP-06 checkpoint.

Broad runtime implementation remains blocked.

## 2. This does not resurrect the retired physical Step 6

The former Round-1 Step 6 was closed as a separate stage because its decomposition around mandatory physical LLM/context isolation was superseded.

S6D does **not** reopen:

- mandatory separate chats/agents/model calls;
- mandatory physical context reset;
- minimum physical invocation counts derived from secrecy;
- provider-abstraction work;
- the retired physical-topology definition of role containment.

Those matters remain governed by the later single-context and Round-2 canonical architecture.

S6D exists only because earlier accepted Steps 1–2 explicitly deferred concrete rules/catalog/seed closure to a later Step 6 and R2.7 WP-06 has now proven that some of that debt is still present in current machine contracts.

## 3. Residual debt admitted into S6D

S6D owns closure of the following inherited obligations where they remain unsatisfied:

1. exact engine/ruleset/package/catalog snapshot identity and compatibility metadata;
2. full D&D seed/catalog-gap coverage required by the supported MVP rules baseline;
3. complete structured Calculation Selector metadata coverage;
4. complete registered MechanicalContext accessor/input/dependency metadata required by the supported seed;
5. exact typed contracts for registered mechanical protocol values where current architecture requires them;
6. exact registered Activity primitive argument/result contracts required by the supported seed;
7. stable character advancement/choice-slot realization sufficient for reconstructable Actor build and READY_PC;
8. concrete HP/LifeState/Resource/Effect/Condition/Duration/Recovery seed verification, including owner-local responders at rules boundaries;
9. any extension of scheduled-trigger or invocation-adjudicated fact shapes proven necessary by actual supported rules cases;
10. ruleset/package seed packaging and deterministic ResolvedCatalogContext reconstruction requirements;
11. final catalog/schema/seed gap audit before returning to R2.7.

## 4. Clean-slate correction to the historical migration wording

There are no existing user campaigns whose current scaffold must remain backward compatible.

Therefore S6D does **not** preserve obsolete current schemas/catalog shapes and does not build a compatibility layer for them.

Historical Step-6 wording about migrating the current pre-release scaffold is superseded by the R2.7 clean-slate owner decision.

S6D still must define enough package/snapshot compatibility semantics to make exact ruleset identity and future post-release evolution possible. The general future released-campaign migration policy remains owned by R2.7 WP-20.

## 5. R2.7 checkpoint

R2.7 is paused after:

```text
WP-01 CLOSED
WP-02 CLOSED
WP-03 CLOSED
WP-04 CLOSED
WP-05 CLOSED
WP-06 IN PROGRESS
```

The current WP-06 evidence slice and structural changes remain valid input to S6D and to the later resumed WP-06. They are not rolled back.

No WP-07+ work begins while S6D is open.

## 6. S6D completion requirement

S6D may close only when:

- every inherited Step-6 rules/seed/catalog deferral is item-level dispositioned;
- every registered selector is either fully machine-described or explicitly removed as unsupported/stale;
- every supported seed mechanic has an execution route without inventing a second authority;
- registered operations and protocol values have exact machine destinations where required;
- character progression choices can be deterministically validated against stable definition-owned choice slots;
- package/catalog snapshot identity is sufficient for deterministic compatible reconstruction;
- no known supported D&D seed case requires arbitrary executable code, arbitrary query access, hidden scheduler authority, or LLM ownership of engine state;
- structural catalog/schema changes have focused regression coverage;
- adversarial review finds no remaining debt that would materially change implementation topology;
- a fresh closure gate explicitly authorizes resuming R2.7 WP-06.

## 7. Human decision policy

The agent continues S6D automatically for technical questions when the accepted architecture determines one clearly preferable answer.

Stop for the owner only when evidence leaves a material choice involving:

- supported product/rules semantics;
- materially different architecture boundaries;
- new semantic authority;
- deliberate scope reduction of the MVP rules seed;
- nontrivial risk acceptance;
- a decision to supersede accepted architecture.
