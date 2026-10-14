# SP00 accepted-owner decision evidence integration

Status: **BOUNDED IMPLEMENTATION EVIDENCE — SIX ACCEPTED OWNER INTERPRETATIONS; SOURCE QUALIFICATION REMAINS PARTIAL**

This record documents synchronization of the accepted A–F owner decision into the existing SP00 development-only source-qualification evidence. It is not an independent review of the final machine candidate, a gameplay implementation, native proof, or a source-ready declaration.

## Pinned authorization and source basis

| Input | Exact identity and role |
|---|---|
| Published implementation base | `0a046bd6bb1c1990e54c3ebe18c94f570d23be9f` |
| Accepted final owner | `DEV/docs/superpowers/specs/2026-10-14-sp00-source-interpretation-owner-decision.md`; Git blob `662d17d8299fae1ac264863a7da31bd99a9da183`; raw-file SHA-256 `9de384b36657bafe7e93252959825ed4ba4494f287ee972904d589f5c8759e5c` |
| Historical targeted source review | `DEV/docs/superpowers/design/2026-10-14-sp00-source-interpretation-review.md`; raw-file SHA-256 `c23981544f9dd0cac9e90f9fd6fe5020bb756bd16fd7cb5a2f0878e6c783b581` |
| Historical pre-acceptance Decision Brief | `DEV/docs/superpowers/design/2026-10-13-sp00-source-interpretation-decision-brief.md`; raw-file SHA-256 `ba763309d102089ac82853178f072e2c3e5b09f2d874a3f11d611f06e3226e6a` |
| Senior Stop 2 ruling | `ses_ec4c23b17ffeguPvUedtqzevkv`: GO for this accepted-owner source-evidence integration only. No registry/native closure, runtime/profile activation, or production claim is authorized. |
| Stable SP00 draft/version owner | `DEV/docs/superpowers/plans/implementation-wave-05-machine-bootstrap-integration.md` §W05.SP00, especially its minimum impact envelope: development source schema `1`, DEV-only `VERSION_IMPACT: NONE` absent semantic package-member changes, no catalog-generation bump. `DEV/RELEASE/VERSIONING.md` §§4 and 7 plus `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md` §§2 and 12 preserve independent development-schema and released-protocol namespaces. |

The final A–F owner is the sole normative owner for these six judgments. The targeted review remains historical evidence: its prior `NEEDS_PO` status is superseded by the accepted owner. The revised Decision Brief is explicitly historical pre-acceptance material. The machine evidence records `ACCEPTED_PRODUCT_OWNER_DECISION` and `ACCEPTED_OWNER_INTERPRETATION_NOT_LITERAL_SRD_WORDING`; it does not promote every selected result to explicit SRD text.

## Exact six source-key bindings

Each row is one existing `SP00_SOURCE` subobligation, bound to the original classification/history pointers, current map entry, source-pass record, body witness, and exact current Markdown span. The original classification indexes are the six selected indexes, not an interval expansion.

| Index / key | Owner section | Source record and current Markdown span | Grounding distinction and accepted interpretation |
|---:|---|---|---|
| `0` — `source.spell.aid.unresolved.health_normalization_policy` | A — Aid | source-pass `/rows/2`, body witness `/rows/2`, map entry `2`, SRD lines `9307–9321`, span SHA-256 `735037ddd8bc5621e8e0a5fade21ea6bc73c26c688d93115911b88a36b4863a0` | The duration-bound maximum/current HP increase is source text. The accepted owner selects current-HP change by `b_after - b_before`, normalized to zero and the current derived maximum, preserving intervening damage/healing; no entry snapshot, separate HP balance, stacking, or repeat healing. |
| `52` — `source.spell.magic_missile.unresolved.rng_damage_grouping` | B — Magic Missile | source-pass `/rows/87`, body witness `/rows/198`, map entry `85`, SRD lines `13259–13273`, span SHA-256 `e772f726833c5dcb9d05591eeb8537634ea860acf3412da63fb95599182b2a0d` | Ordinary independent dart draws and the simultaneous group are source-grounded. The accepted owner selects distinct per-dart damage instances and Concentration obligations, while preserving one simultaneous group, fixed-result identity/reuse, actual turn-controller ordering, and no unnecessary later saves after Concentration ends. |
| `60` — `source.spell.pass_without_trace.unresolved.selection_timing` | C — Pass without Trace | source-pass `/rows/97`, body witness `/rows/224`, map entry `95`, SRD lines `13735–13747`, span SHA-256 `5286728517f232fad21e7a35ba72d36862ab98170e3a06ca57889586678a2132` | The chosen-creature set and current aura eligibility are source text; membership timing is not. The accepted owner commits identities at casting, preserves membership through leave/reentry, grants benefit only inside the current aura, and adds no free reassignment or general range leash. |
| `66` — `source.spell.ray_of_frost.unresolved.movement_composition` | D — Speed | source-pass `/rows/107`, body witness `/rows/251`, map entry `105`, SRD lines `14272–14286`, span SHA-256 `dae3f77c2b494c1afd20ba279f16583438d1df80127bf260e3a243c491b77ea0` | Ray of Frost's fixed `−10` modifier is source text; a universal floor is not. The accepted owner floors each final derived movement capability at zero after complete lawful composition, preserves negative contributions/special-speed rules, and requires exact-zero consumers to observe the final capability. |
| `68` — `source.spell.resistance.unresolved.damage_grouping_order` | E — Resistance | source-pass `/rows/109`, body witness `/rows/257`, map entry `107`, SRD lines `14389–14401`, span SHA-256 `c8eb5178fade2834aa5ad5c504723c2499bcbfaeeb821d120b5dbc729ab3432c` | The automatic chosen-type damage trigger and once-per-turn rule are source-grounded. The accepted owner selects first eligible positive damaging occurrence per actual turn and chosen-type-subtotal-only `d4` reduction, floored at zero with no spill, followed by ordinary type defenses. The reviewed golden `5 Fire + 5 Cold`, Fire, `d4=3`, ordinary Fire Resistance yields `floor((5−3)/2)+5=6`. |
| `80` — `source.spell.warding_bond.unresolved.copied_damage_policy` | F — Warding Bond | source-pass `/rows/138`, body witness `/rows/329`, map entry `136`, SRD lines `15811–15825`, span SHA-256 `cc1be68ce4911478cbf85ba39ea14612445549e3126ce317f8583707ce51a244` | The source states that caster and target take the same amount. The accepted owner defines target-taken typed damage after target defenses and before HP allocation as linked input to the caster's ordinary defenses and temporary-HP buffer; Warding Bond is the new proximate cause, with no blanket copied attack/origin/bypass attributes or exceptional final-loss equality. |

## Machine realization and preserved state

The source-qualification schema remains draft `schema_version: 1`. Its additive owner/provenance record names the exact final owner path, raw SHA-256, Git blob, six sections, scope, accepted keys, historical review, and historical brief. Each of the six new resolution records carries its owner section, authority/basis distinction, source-grounded findings, exact source locator/hash, owner-qualified interpretation, retained qualifiers, and empty native-proof refs. `OWNER_DECIDED` is distinct from `SOURCE_CLOSED`.

The validator checks the accepted owner/review/brief bytes; each owner section heading and required clauses; all six exact key/category/classification/history/map/pass/body identities; source body phrases and line-span hashes; prior `SOURCE_HELD` evidence; required qualifier text; and the Resistance arithmetic witness. The derived classification uses the union of prior source closures and the six owner decisions, while preserving the 82 original classification records and all old resolution arrays as historical evidence.

| Measure | Before this integration | Delta | Derived result |
|---|---:|---:|---:|
| Original classification records | 82 | 0 | 82 |
| Original source-blocking keys / downstream-only keys | 77 / 5 | 0 / 0 | 77 / 5 historical classifications |
| Reviewed original source keys | 77 | 0 new keys; six prior holds receive owner decisions | 77 |
| Distinct source-blocking keys resolved | 60 | +6 accepted owner decisions | 66 |
| Resolved source subobligations | 64 | +6 accepted owner decisions | 70 |
| Current source-held keys / subobligations | 17 / 17 | −6 | 11 / 11 |
| Current active source blockers | 17 | −6 | 11 |
| Prior resolution records | 81 | +6 | 87 |
| Future-proof subobligations | 33 | 0 | 33, all `NOT_ESTABLISHED` |

These values are derived from the exact identities and dispositions; `66` resolved keys comprise the prior 60 source closures plus six accepted owner decisions, not 66 literal-SRD closures. The remaining 11 source-held keys are Arcane Lock destruction/access, Create or Destroy Water container/extent, Detect Magic aura overlay, Gentle Repose corpse/revival binding, Locate Animals or Plants eligible search domain, Magic Mouth episode frequency, Mending repair/missing matter, Prayer of Healing responder census, Spike Growth displacement/distance, Unseen Servant subject classification, and Find Familiar eligible-form census. Warding Bond's prior seventh-batch `SOURCE_HELD` row remains unchanged as historical evidence; only its current selected source interpretation is owner-decided.

The final result remains `W05_SPELL_SOURCE_CENSUS_PARTIAL` / `source_qualification_status: NOT_ESTABLISHED` with `source_ready_gate.ready: false`. Source mapping, remaining holds, all 33 future-proof obligations, native proof, full-339 qualification, package promotion and runtime admission remain open. The conditional Thunderclap installed-default repair remains `REQUIRED_BEFORE_PACKAGE_PROMOTION`; Word of Recall remains `NOT_ESTABLISHED`. No GAME, profile, definition, recipe, catalog, module, package, persistence, or runtime behavior changed.

## Impact and verification

**VERSION_IMPACT: NONE.** The actual machine owner is the accepted DEV-only SP00 source-evidence schema/fixture/validator/test set. The accepted W05.SP00 owner bounds this development draft at schema version `1`; this is additive evidence under that unchanged namespace, not a released package/protocol or persistent schema, coordinated catalog generation, runtime module, or digest/canonicalization change. No GAME projection or package identity changed.

**SYSTEM_IMPACT: NONE.** The work synchronizes accepted owner evidence only. It creates no profile, active definition, executable primitive, runtime consumer, package admission, native closure, source-ready result, or new state/authority owner; no System-Impact Gate was crossed.

The implementer did not independently review the final candidate. Review of the frozen scoped delta and integration remain the coordinator's next action. Exact command/result surfaces and final byte identities are recorded in the external task receipt at `/tmp/hdm-dev/spell-recovery/SP00-owner-decision-integration-receipt-20261014.md`.
