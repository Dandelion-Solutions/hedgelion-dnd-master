# W05.T06-P1A — Sorcerer override System-Impact review

Status: **NEEDS_PO — BOUNDED PRODUCT-SCOPE DECISION; P1A HELD**
Date: 2026-10-04
Reviewed implementation-stop HEAD: `6dbdf160824060b64cf9586ee1c29ddbb3470f0e`
Published continuation basis: `65d063c5d75664270b2df3cfa07ddb743ddee062`
Review: independent Senior System-Impact technical review, not production acceptance.

## Disposition

The accepted S6D-07 Sorcerer override promise cannot currently produce a
different complete legal spell loadout from the admitted package. This is a
bounded product-scope conflict, not a missing Python mechanism.

P1A's stable acceptance text says **explicit player override generically**; it
does not itself require a different Sorcerer loadout. The worker's stronger
reading of that sentence is corrected. However, the canonical S6D-07 owner
separately promises an overridable six-spell Sorcerer bundle. Proving the generic
P1A override with another packaged choice would leave that promise unresolved.

No GO to invent an alternate spell option, weaken the mismatch validator,
expand package content, or change acquisition cardinality is granted here.
P0 and S1/S2 remain accepted. P1A output is unproduced; no later task starts.

## Source evidence and qualifiers

| Source | Evidence and effect |
|---|---|
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` §§invariants/MVP acceptance | Definitions own grants and owner-relative choice slots; unsupported content is nonselectable. The Human/Criminal Sorcerer acceptance promises a recommended six-spell bundle overridable before READY_PC. |
| S6D-07 collaborative review `DEV/docs/superpowers/design/2026-08-26-s6d-07-character-progression-ready-pc-seed-collaborative-review.md` | Accepted profile requires four cantrips and two prepared level-1 spells, packages exactly those six selectable spells, and excludes unpackaged alternatives. |
| `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json` | `advancement.sorcerer.level_1.spells` selects `option.spells.mvp_default`. Actual spell definitions contain exactly four level-0 spells and two level-1 spells: one complete 4+2 membership in this corpus. |
| `DEV/SCHEMAS/build-choice-slot.schema.json` | Spell bindings are definition-owned option data. No caller-parameterized alternate spell-selection contract is declared. |
| `DEV/SCHEMAS/world-actor-state.schema.json`; `DEV/ARCHITECTURE/ACTOR_MODEL.md` §3 | Actor stores known/prepared spell IDs, but structural validity does not establish acquisition legality or supersede resolved choice definitions. |
| `DEV/TOOLS/validate_character_mvp_seed.py`; `DEV/TESTS/test_s6d_07_character_mvp_seed.py` | Selected membership must equal the bound option's spell grants. Removing a supported spell yields `spell_selection_binding_mismatch`; that negative remains valid. |
| S6D-09/S6D-11 additions in the canonical character owner | Later amendments change dependencies/package identity, not character-choice semantics or READY_PC predicate. |
| Stable W05 plan P1A acceptance/envelope | Generic explicit override is required; new D&D content and new mechanical primitives/selectors are excluded. |

Exact evidence was independently inspected by the reviewer rather than inferred
from the worker's brief. Navigation indexes supplied routing only.

## What is already admitted

Explicit player selection of the sole `option.spells.mvp_default` with
`choice_basis.player_explicit` is legal. It changes selection provenance, not
spell membership. The same six IDs may be normalized to that existing option;
this cannot prove a different spell loadout. Reordering IDs, dropping spells,
or changing known/prepared carriers cannot create an alternative acquisition
contract.

## Exact Product Owner decision

May the current MVP remain bounded to its sole complete six-spell Sorcerer
loadout, with the override promise explicitly limited to admitted alternatives
and unsupported different requests rejected; or must the current release
demonstrate a genuinely different legal Sorcerer loadout?

**Recommendation:** retain the narrow corpus and qualify the Sorcerer acceptance
promise to admitted alternatives. Preserve explicit-selection precedence and
prove P1A's generic override case with an actual packaged alternative. This
narrows an accepted product promise and requires PO approval; it is not silently
adopted by this review.

If a different Sorcerer loadout is required, accept the sufficient spell
alternatives and acquisition/selection contract through the S6D-07 owner route
before implementing them. The review does not choose that content or cardinality.

## Repair boundary after decision

Reconcile affected S6D-07 acceptance wording, stable P1A acceptance/envelope,
conformance witnesses and current cursor under the chosen owner route. Preserve
Host-bound exact catalog validation, option/spell-state agreement, unsupported
ID rejection, fixed initial choices, no situational reselection, and
Actor/Asset/allocator atomicity/repeat/rollback. Do not weaken mismatch negatives.
The automatic continuation authorization remains valid after the actual gate
is resolved; ordinary task boundaries do not acquire a new PO approval step.

## Verification

Independent reviewer executed S6D-07 + RD15 catalog + RD03 Actor suites:
**74 passed**. A read-only resolved-package diagnostic found exactly one
complete 4+2 spell membership; default and explicit same-membership selection
have no conformance blockers, while removing one spell yields
`spell_selection_binding_mismatch`. These results are conformance evidence,
not P1A production acceptance.

Worker baseline: six existing P1A owner suites **200 passed**; current-progress
authority **2 passed**. No production P1A files/tests remain. Full DEV,
maintenance/build and hosted CI are not claimed for this stop.

VERSION_IMPACT: NONE — review/implementation-start/status provenance only;
no versioned semantic, schema, module, package or generation owner changed.
SYSTEM_IMPACT: NEEDS_PO — bounded Sorcerer product-scope qualification.
NEXT_EXACT_TASK: obtain the product decision above, reconcile its owned
acceptance contract and resume P1A under the resulting stable envelope.
