# S6D-07 Step 5 — Candidate Specification

Status: **CANDIDATE — TDD MACHINE REALIZATION COMPLETE — STEP 6 REQUIRED**

Implementation boundary: **IMPLEMENTABLE ARCHITECTURE + MACHINE CONTRACTS; PRODUCTION RUNTIME EXECUTION DEFERRED**

## 1. Result

Adopt a definition-owned, sparse-binding character model and one capability-declared playable MVP package profile. The profile contains exactly one Human/Criminal Fighter 1–2 path and one Human/Criminal Sorcerer 1 path. It is not a full SRD corpus and creates no character-builder questionnaire.

The machine realization consists of:

- `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-capabilities.json` — honest supported-surface declaration;
- `character-mvp-seed.json` — the unique package compiler source for exact character/support/Activity definitions, registered values, stable choice slots, dependency closure, READY_PC evidence contract and Fighter 1→2 proof;
- `NOTICE.md` — required source/license notice;
- the amended S6D-06 base catalog/schema — eleven exact draft replacements, never an overlay;
- focused conformance tests.

## 2. Character authority

Reusable definitions own grants, level applicability, prerequisites and choice-slot identities. `world.actor` owns only accepted build anchors, class progression, owner-relative choice bindings and spell selection state. Derived sheet values remain projections. A binding is interpreted only against the Actor's accepted `ResolvedCatalogContext`; an ID match in another package generation is insufficient.

Each binding records the owning definition/revision, `choice_id`, selected `option_id` values and selection basis (`EXPLICIT_PLAYER`, `RULES_VALID_INFERENCE`, `DELEGATED_POLICY`, or `DETERMINISTIC_DEFAULT`). The compiler rejects duplicate bindings, cardinality violations, defaults outside the option set, unresolved grants and selections not admitted by the pinned package context.

## 3. Onboarding and READY_PC

The Master applies, in order: explicit concept/input, rules-valid inheritance/inference, campaign/rules defaults, delegated bookkeeping, then a player question only for a remaining materially different player-owned choice. A definition option is not a mandatory prompt.

Provisional gameplay is legal before READY_PC. Each attempted mechanic requires only its local committed dependencies. READY_PC becomes true when the accepted catalog context and Actor anchors reconstruct one legal build; every required initial binding is closed; required assets/health/defense/resources and selected spell paths are admitted; and no selected path reaches a quarantined dependency. A genuine future advancement choice is not initial debt until its boundary opens.

## 4. Advancement

Advancement is an entitlement-bound transaction: pin current Actor/catalog context; derive the next stage; bind only choices opened at that boundary; validate prerequisites/cardinality/reference closure; publish one idempotent Actor transition; reconstruct; then emit existing event/receipt/recovery evidence. Pending work has no independent character lifecycle owner. Fighter 1→2 is deterministic and grants Action Surge and Tactical Mind without reopening the level-1 style.

## 5. Primitive activations

S6D-06 base contracts remain authoritative. S6D-07 replaces exactly eleven rows in that base catalog after their consumer/dependency challenges; no overlay can supersede a quarantined row. Arguments, results, reads, mutation, RNG, suspension, atomicity, failures and evidence ownership remain exact and are now reviewed with the concrete consumers.

- `op.select_targets`: bounded validation of declared candidates; no world search or mutation.
- `op.roll`: accepted RNG result for a frozen request; no semantic threshold or mutation authority.
- `op.resolve_attack`: deterministic attack comparison; no RNG, target mutation or damage authority.
- `op.resolve_save`: deterministic save comparison; no RNG, discovery, damage or mutation authority.
- `op.apply_damage`: typed prospective HP/LifeState transition routed through existing owners; no target/hit decision, arbitrary path or direct commit.
- `op.apply_healing`: typed prospective bounded healing for Second Wind; no target discovery, maximum change, arbitrary path or direct commit.
- `op.consume_resource`: checked owner-bound resource decrement for spell slots and limited features; no capacity/resource creation, arbitrary path or direct commit.
- `op.for_each_target`: bounded compilation over an already selected ordered target list; no discovery, unbounded loop, child-authority widening or independent commit.
- `op.resolve_check`: deterministic Tactical Mind augmented-check comparison; no RNG, DC authorship, resource mutation or original-check replacement.
- `op.create_effect`: exact Innate Sorcery Effect activation with stable instance identity, pinned one-minute temporal binding, same-identity atomic replacement and idempotent expiry/recovery; no generic Effect authorship or lifecycle authority.
- `op.emit_fact`: exact Action Surge current-turn entitlement, atomic with resource consumption, one-use and non-magic scoped; no generic fact authorship or durable Actor flag.

All other primitives remain quarantined/nonselectable. Build choices do not use `op.request_choice`; they are preparation/advancement bindings, not Activity suspension. The chosen spell set opens no reaction/effect primitive.

## 6. Exact content boundary

The machine inventory is exhaustive for the profile: Human, Criminal, Fighter 1–2, Sorcerer 1, four required feats, eight character features and six Sorcerer spells, plus only their resolved support definitions, registered values and twelve exact Activities. The seed is the sole package compiler source, not a second index; its content hash is bound by `character-capabilities.json`. All other character content is absent/nonselectable. The package name does not imply breadth; the identity-bound capability declaration limits breadth.

`Burning Hands`, rather than `Shield`, is used because it reuses target/save/damage dependencies and does not open reaction/effect lifecycle. Unsupported content cannot be inferred from SRD provenance or package compatibility identity.

## 7. Verification

TDD first produced a missing-artifact failure. The focused suite then proved exact inventory uniqueness/reference closure, bounded package claims, material plus defaulted/delegated choice presence, progressive READY_PC semantics, exact primitive activation set/authority denials and bounded Fighter advancement.

Step 6 must review the whole-project graph, with special attention to whether the eleven base-catalog primitive replacements meet the S6D-06 challenge; whether the seed is the unique package compiler source rather than a second inventory; and whether every dependency is realized/admitted rather than self-asserted.

## 8. Runtime realization boundary

The package compiler/readiness/advancement tool and fixtures are executable conformance references for machine-contract closure. They are not parallel production owners and do not claim to implement the accepted catalog resolver, Activity runtime, ExecutionSegment publisher or durable repository. Production realization remains blocked until Implementation Planning.

The candidate is complete only if those future implementations can follow the canonical envelopes, exact dependency/primitive contracts, READY_PC evidence and advancement publication/recovery trace without a new architectural choice. Once implemented, a mandatory behavioral fast-start test must replay both Step-4 walkthroughs and verify actual question count, provisional local sufficiency, READY_PC timing and absence of procedural GM scripting or hidden dependencies.
