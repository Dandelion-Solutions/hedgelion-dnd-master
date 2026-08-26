# S6D-07 Step 3 — Supported Character Seed Scope — Decision Brief

Status: **HUMAN DECISION REQUIRED — STEPS 4–8 NOT STARTED**

Pinned evidence ref: `f8cfcdd3166f4bc5306f47c37c9da5730d01929e`

## Decision

What concrete character-content breadth must the built-in `hdm.rules.dnd2024-srd52-core` package support for the current MVP/S6D closure?

## Established facts

1. The required package profile exists only as admission metadata; its semantic content directory and every concrete character definition are absent.
2. Existing schemas are structural capability, not a supported seed.
3. READY_PC cannot be proved end-to-end without at least one closed definition graph and representative initial/advancement cases.
4. The public SRD 5.2.1 baseline is legally reusable under CC BY 4.0 with attribution, but “SRD-based” does not determine whether HDM ships the full corpus now.
5. All Activity primitives remain quarantined. Any executable spell/feature path requires exact primitive completion and review; a definition reference cannot bypass this.
6. The scope choice changes shipped capability, S6D-08/09 coverage, implementation volume and package naming expectations.

## Alternatives

### A. Bounded MVP vertical slice — recommended

Ship the smallest honest character seed that demonstrates both major build shapes and advancement:

- at least one martial class path and one spellcasting class path;
- enough species/background/feat/feature/spell/advancement options to exercise required, delegated/default and player-required choices;
- initial level plus at least one meaningful later subclass/feat/spell advancement boundary;
- only mechanics whose dependencies can receive exact reviewed contracts.

The package manifest must explicitly describe this as the current MVP subset; unsupported SRD content remains absent/nonselectable rather than implied. Later additions are compatible package-content growth under existing identity/admission laws.

Benefits: closes READY_PC and progression with real vertical evidence, bounded workload, no false full-SRD claim. Cost: the exact included list becomes a product-supported subset and must be named/documented clearly.

### B. Full SRD 5.2.1 character corpus now

Encode every SRD character option relevant to the eight families and close all transitive mechanics needed by them.

Benefits: package name naturally matches broad expectations; strongest baseline coverage. Costs: much larger content, schema and primitive surface; S6D-07 would expand substantially into S6D-08/09 dependencies and delay closure.

### C. Architecture/conformance fixtures only

Use synthetic nonselectable fixtures to prove schemas and READY_PC logic, but ship no playable built-in character seed yet.

Benefits: smallest immediate architecture work. Costs: does not satisfy the current S6D exit promise of a supported reconstructable D&D seed; package remains nonselectable and S6D-07 closes only as deferred debt. Not recommended unless current MVP intentionally excludes playable built-in D&D content.

## Recommendation

Choose **A — bounded MVP vertical slice**. It is the narrowest scope that honestly satisfies S6D-07 while preserving future additive growth and avoiding a false claim of complete SRD coverage.

After selecting A, the agent will derive and present the exact minimal item list from official/public SRD evidence and dependency closure during Step 4; inclusion details that are forced by that selected profile remain agent work. If the exact breadth within A leaves two materially different viable product profiles, the agent will return with one further narrowed decision rather than guessing.

## Exact human question

Which scope is authoritative for the current built-in package: **A — bounded playable MVP vertical slice**, **B — full SRD 5.2.1 character corpus**, or **C — nonplayable conformance fixtures only**?

