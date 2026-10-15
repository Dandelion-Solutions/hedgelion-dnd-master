# SP00 Prayer accepted-owner evidence binding

Date: 2026-10-15. Status: **BOUNDED IMPLEMENTATION CANDIDATE — LOCAL VERIFICATION COMPLETE; COORDINATOR INTEGRATION / INDEPENDENT REVIEW PENDING**.

## Task and accepted inputs

This is the bounded SP00 source-mapping evidence binding that follows explicit Product Owner acceptance of all three Prayer recommendations and the supplied final Prayer Stop2 GO. It does not reopen the choices or authorize a runtime recipe, active registry member, native consumer, or readiness claim.

| Input | Exact identity / disposition |
|---|---|
| Pinned base | Published commit `52923a33c3b9cf2d09778552d8df3225e1f1851d`, tree `1f303232a5345200ace5a5bec5b395d2ad49f293`; detached worktree was clean before edits. |
| Product Owner decision | Exact accepted owner `DEV/docs/superpowers/specs/2026-10-15-sp00-prayer-benefits-owner-decision.md`; §1 records **“да, все три”**. |
| Final Senior gate | `ses_ebfb86733ffe6WM60pM7dEia3j`, supplied as an accepted task input. This worker did not independently rerun or re-review that session. |
| Existing key 62 | `source.spell.prayer_of_healing.unresolved.responder_census`; original source-history pointer `/source_mapping_lanes/0/mapping_payload/unresolved_key_index/62`, current mapping entry `/source_mapping_lanes/0/mapping_payload/entries/98`, source-pass row100 and body-witness row237 remain unchanged. |
| Census evidence | Tracked `DEV/docs/superpowers/research/2026-10-15-prayer-short-rest-responder-census.json`; the existing research artifact is read and verified in place, not copied into a new fixture. |

The configured SSH remote could not be refreshed in this worker environment (`Permission denied (publickey)`). The user-supplied published base identity was verified locally; there is no fresh remote-read claim and no publication attempt.

## Bounded delta

Only these six tracked paths are in scope:

1. `DEV/SCHEMAS/spell-source-qualification.schema.json`
2. `DEV/TESTS/fixtures/spell-source-qualification.json`
3. `DEV/TESTS/fixtures/spell-source-qualification-rejected.json`
4. `DEV/TOOLS/validate_spell_source_qualification.py`
5. `DEV/TESTS/test_spell_source_qualification.py`
6. `DEV/docs/superpowers/design/2026-10-15-sp00-prayer-owner-evidence-integration.md`

The source validator now binds key62's `source_mapping_review` subobligation to the exact accepted owner bytes, exact source-map history, current entry98, retained pass/witness locators, and tracked census. It verifies owner SHA-256 and Git blob identity, reads and validates the full source census and adopted SRD Markdown, checks all 805 full source-span records plus 137 matched blocks (942 exact source records), and records the seven accepted completion-row pointers and actual grant conditions. Fourteen primary-source line identities are rehashed and their source text checked. The row references remain provenance; they do not admit features by census membership.

The product/source facts and owner decisions remain separate in the evidence record. The record binds all five final owner sections and the three accepted choices: BROADER-7, NO mount-pace renewal, and DIFFERENTIATED Simulacrum/curse branches. It distinguishes lawful zero-delta/declined options from proved-all-blocked and unknown eligibility, and retains the source-specific cost/replay and recipient-owned gate boundaries.

The original six A–F owner records are not rewritten. The earlier Prayer `SOURCE_HELD` record and original key62 classification/history remain intact. A new `OWNER_DECIDED` record closes only key62's source-mapping subobligation. The census's historical six-candidate classification, including Tireless's prior source disposition, remains untouched; the accepted owner binding separately identifies the seven completion rows (12,13,14,18,19,21,28) and preserves Tireless's actual grant/exhaustion condition without refilling its Long-Rest-only temporary-HP uses.

## Derived result and explicit limits

The validator derives **77 reviewed; 71 resolved = 64 source-closed + 7 owner-decided; 6 held; 75 source subobligations resolved; 33 FUTURE_PROOF subobligations still NOT_ESTABLISHED**. The source count is derived from original histories and the new exact binding, not accepted from a caller-supplied counter tuple. Tenth-batch history remains 70 resolved / 7 held.

`source_ready` remains false; the separate default repair and Word of Recall residual remain open. No new feature, class, item, prerequisite, profile, recipe, runtime module, native transition, migration, or package member is granted. The evidence does not establish full339 support, source readiness, native conformance, production readiness, or runtime behavior. The simulated health/recovery, restrictions, mount, and gate cases are required evidence qualifiers, not executed gameplay tests.

## Verification and impact

- Baseline of the owning source-qualification module — **63 passed**; exact executable path and invocation are recorded in the external task receipt.
- RED: the new Prayer binding test failed as intended with `source_resolved_key_count == 70`, expected71.
- GREEN/focused: the Prayer binding plus cold-negative tests — **2 passed**; source-owner and census byte drift probes — **3 passed**.
- Final owning-module, Ruff, maintenance-audit, and full DEV-suite invocations/results are captured verbatim in the external task receipt. The canonical maintenance wrapper would create `.hdm-devtools/` in this isolated checkout; it was not used because that path is outside the six-path write set. The same audit engine ran with the repository-declared venv.
- `ruff format --check` leaves the test file formatted; its sole remaining finding is the pinned-base `SIXTH_EVIDENCE_ORDER` formatting drift at tool line5762, verified directly on the base with Ruff's `--diff` over the same lines. No unrelated formatter mutation was made.
- Full local DEV suite: **2054 passed, 91 skipped, 1 failed**. The sole failure is `test_runtime_package_provenance::test_clean_checkout_metadata_records_exact_head`, which expects `clean_head` but observes `dirty_worktree` because this task is intentionally uncommitted. It reproduced sequentially with the same result. No commit was permitted to manufacture a clean-head result.

**VERSION_IMPACT: NONE.** The actual changed namespace is the DEV-only source-qualification draft schema (`schema_version: 1`) and its fixture/tool evidence. This is not a persisted campaign family, runtime schema, active profile/catalog/package namespace, or coordinated digest-generation contract; no released/runtime reader or migration consumer is affected. Schema and current fixture changed together. The fixture SHA-256 pin was updated to the exact new fixture bytes. Engine/module versions, GAME/DEV projections, catalog, campaign/storage generations, runtime package identity, and digest generations remain unchanged.

**SYSTEM_IMPACT: NONE.** The delta is the approved source-owner evidence binding for one pre-existing source-mapping hold. No runtime or GAME path changed, and no new authority boundary or consumer contract was introduced.

## Residual state and integration handoff

- This local candidate is uncommitted and unpublished by assignment. There was no shared index, cursor, main checkout, branch, or remote-ref mutation.
- The existing canonicalization note and global/cursor records still carry pre-integration pending/count wording at the pinned base. This worker did not update those protected status routes. The coordinator must reconcile them after accepting/reviewing this candidate; keep `source_ready=false`, native proof NOT_ESTABLISHED, and remaining six holds explicit.
- The uncommitted full-suite clean-head provenance test remains the sole known local verification failure; it must be rerun on a permitted clean published integration head by the coordinator, not masked here.
- No independent review is claimed. The supplied Senior GO is an accepted input, not a review of these six candidate bytes.

**Exact next integration action:** the coordinator should inspect the six-path byte delta and external receipt, obtain the required independent candidate review on frozen bytes, integrate without touching the shared cursor until accepted, synchronize key62/current counts and stale status wording, then run final exact-head verification plus a clean-head provenance check before any separately authorized publication.
