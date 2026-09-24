# Independent review — W04.T04B and W04.T07B

Status: **FINAL DISPOSITION — T04B TARGETED REPAIR REQUIRED / T07B PASS**

Date: 2026-09-24

## Exact review basis

- Reviewed remote HEAD: `a5cd9c517913bcf04d7acfbe895be49cdf941111`.
- Parent / combined code candidate: `55fb0a52a933b90a15ad2bc8b0af624635edaf26`.
- T04B implementation: `f0ba25f34cb60d9b9f0019bcbb414bc6e97b2372`.
- T07B boolean-ordinal repair: `55fb0a52a933b90a15ad2bc8b0af624635edaf26`.
- Role: independent task reviewer; no production, test, schema or architecture implementation is performed by this review.

The earlier `2026-09-24-w04-t04a-t07b-independent-re-review.md` records the prior exact-state review. Its T04A PASS remains accepted. This report supersedes its remaining T07B disposition after checking the submitted repair, and separately reviews the new T04B consumer. No earlier accepted task is reopened.

## Bounded source manifest and method

All current repository evidence was read through GitHub Connector at the reviewed HEAD. The review graph is W03 access/LIVE currentness -> T04A preparation -> T04B W02 publication/recovery -> T05C, and T07B M-SEG admission/schema -> T07C. No local repository or recursive corpus preload was used.

| Current source | Use |
|---|---|
| `AGENTS.md`, ChatGPT Work overlay, development execution process | Role, review, transport, verification and publication rules |
| Stable Wave-04 plan, blob `e64902d1b1df6ed8cebde411231a3d0ddee33be5` | Task scopes, outputs and downstream gates |
| Current progress and execution cursor | Exact candidates, accepted chains and retained qualifications |
| `GAME/TOOLS/collaboration.py`, blob `6ab2f10bfeb06bb7a782bb50bba46075e82ac3df` | Reconciliation carrier, operation construction, publication and recovery paths |
| `DEV/TESTS/test_rd12_collaboration.py`, blob `22980eda4e2698cec145a45ef4b43ccc653cc778` | Eight new same-closure tests and existing T04A fixtures |
| `GAME/TOOLS/access_control.py`, blob `54e22e268026765892c9e82bdab6eb19a5e89ffe` | Frozen access transition, candidate-vs-physical-publication distinction, native multi-LIVE freeze/forward proof |
| `GAME/TOOLS/runtime_host.py`, blob `bf1639e7d6f41ff2fbc52195a16dcddb5b2689fe` | Actual W02 publication service and selected-LIVE route validation |
| Step-5.8 canonical spec, blob `dbecaee7cdaec62f57bf51941cc31034531cc157` | Laws 5.8-54/55/59/60: revocation freeze, same-boundary absorption and partial failure |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | Current authorization and prospective deactivation laws |
| `GAME/TOOLS/story.py`, blob `cfb08b91312e79b5e676a765218f7e7b4266358d` | Strict ordinal validation before exact selector comparison |
| `DEV/SCHEMAS/story-mechanics-unit.schema.json`, blob `8543eec4131e3f3cbea2b104c0979bd1f7fd3eb8` | Unchanged MECHANICS v4 structural contract |
| Exact `55fb0a5...` diff and current RD13 tests in hosted execution | Resolution/receipt boolean and nonpositive-ordinal witnesses |

Findings below are established by deterministic tracing of the current code and its owning contracts. The new T04B negative scenarios described below were not executed by this reviewer. Existing repository tests, including the submitted T07B regression table, were independently verified in exact-head hosted CI. Passing those existing tests is not used as proof that untested recovery/barrier paths are correct.

## Exact-head hosted verification

```text
workflow: Validate engine source
head_sha: a5cd9c517913bcf04d7acfbe895be49cdf941111
run: 35988891445
job: 107597978376
status: completed
conclusion: success
Run full maintenance audit: success
Run DEV unit tests: success
command: .hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
Ran 1186 tests
OK (skipped=5)
VERSION_UNCLASSIFIED=[]
VERSION_LEGACY_HITS=[]
```

The log includes all eight new `CollaborationAccessPublicationClosureTests`, retained T04A tests and `test_m_seg_payload_contract_table_runs_through_python_and_json_schema`. The worker's local `.entire/` census error did not reproduce in this clean hosted checkout. The local census/capture interaction is not claimed repaired. No protected captures or permission settings are changed. This CI evidence is for the reviewed HEAD, not for a later review-documentation commit.

## T07B re-review — PASS / GO

**IRR-T07B-02: CLOSED.** `validate_story_unit` now checks that the actual segment selector is a mapping and that `segment_sequence` is an integer, not a boolean, and greater than zero before comparing the selector with the exact decoded candidate identity. No coercion or schema weakening was introduced.

The shared fixture table contains boolean resolution and command/receipt cases and nonpositive ordinals, alongside valid payload/receipt linkage and missing/empty/wrong-owner cases. The table and the separate exact-positive-segment-mismatch test execute successfully in the hosted suite. Explicit payload linkage from the IRR-T07B-01 repair remains enforced.

```text
W04.T07B: PASS / GO
W04_STORY_SOURCE_CONTRACTS_READY: ACCEPTED
W04.T07C: AUTHORIZED from this producer PASS, subject to its existing owners/gates
```

This is the task re-review disposition, not a full Story integration or Wave-04 PASS. Structural schema validation need not decode and prove cross-field candidate equality; Python retains that semantic obligation. The existing SOURCE_CLASSIFIED omission qualification remains: unconditional rejection of OMITTED is not positive proof of a native-evidence-consuming lawful omission route. No caller MAY_OMIT/reason flag may enable omission, and downstream materialization/integration must not claim that positive support has been verified here.

## T04B findings

### IRR-T04B-01 — BLOCKING — recovery trusts a caller-truncated effect set

**Evidence.** `CollaborationAccessReconciliation.__post_init__` checks agreement between its `affected_obligation_ids` and `obligations`, but does not prove completeness; both may be empty. The normal expected-head publication path recomputes the canonical reconciliation and compares it to the supplied carrier. The advanced-head branch instead calls `_recover_access_reconciliation_after_publication` before that canonical comparison.

Recovery checks the current MANIFEST and target PLAYER through `FrozenAccessPolicyTransition.recover_after_authority`, then validates only the obligations supplied by the carrier. It never independently establishes the complete effect set. W03's PLAYER semantic/history comparison deliberately does not own collaboration route refs. With an empty or consistently truncated carrier, omitted obligations and their route cleanup are not checked.

**Concrete static counterexample.** Use the existing `_open_reconciliation()` deactivation fixture, which has one affected OPEN obligation and both PLAYER route refs. Keep its legitimate W03 transition and after-authority view. Construct an ordinary public carrier with:

```python
replace(reconciliation, affected_obligation_ids=(), obligations=())
```

At a newer native campaign pin, expose the correct after-authority target PLAYER status/deactivation fields while leaving the obligation OPEN and its route refs unchanged. Keep unrelated MANIFEST fields unchanged. This is an inconsistent/partial cross-owner state that recovery must reject, not fabrication of a RuntimeHost or private Python mutation.

The W03 after-authority check succeeds on the fields it owns, the obligation loop is empty, and recovery returns a successful reconciliation. The same bypass is reachable through `publish_collaboration_access_reconciliation` when the current revision differs from the frozen predecessor. A proper subset of multiple affected obligations has the analogous omission problem.

**Violated contract.** T04B must recover the complete same-closure authority/obligation/route effect, not accept a caller-selected subset or treat agreement between two caller fields as completeness proof.

**Minimal repair destination.** T04B code and RD12 tests. Bind/revalidate the complete effect set against the existing exact owner/publication/recovery evidence before acknowledging recovery, including the advanced-head publish path. Preserve cold recovery and bounded known-ID routing. Do not fix this with a public `complete=true`, a caller-minted receipt, a whole-campaign scan, or an in-memory-only marker that loses the required crash-recovery route.

**Required RED/GREEN.** Empty and proper-subset effect sets must fail against partially applied native state; extra/mismatched effect identities must fail; both direct recovery and the advanced-head publish path must reject without a write. The complete genuine after-state must remain idempotently recoverable, retaining historical associations and exact route cleanup.

### IRR-T04B-02 — BLOCKING — campaign publication bypasses a required W03 LIVE revocation barrier

**Evidence.** W03 `_freeze_player_access_transition` returns `LIVE_TRANSITION_REQUIRED` for deactivation/revocation with selected LIVE entries. Its `publish_access_policy_transition` explicitly authorizes a candidate after-view; it does not perform physical publication or complete source freeze.

T04B consumes that candidate, builds campaign/PLAYER/obligation operations, and calls `host.publication.publish_owner_delta`. Neither this path nor its recovery acknowledgement consumes the required W03 final-source proof or rejects a still-required rollover. The generic RuntimeHost W02 publication service validates its Git publication basis, but receives no W03 transition/final-source proof and cannot silently enforce the missing owner-specific barrier.

The existing W03 multi-LIVE owner already distinguishes partial/indeterminate source closes from confirmed final CLOSED revisions and validates owner-issued freeze progress before a forward campaign after-view. The new T04B path bypasses that distinction.

**Concrete static counterexample.** Produce a legitimate W03 deactivation transition against an exact complete selected route with an ACTIVE epoch whose authorization is affected. Supply otherwise valid current PLAYER/obligation/native records and a successful ordinary W02 publication transport. T04A may prepare reconciliation without writing. T04B currently has no barrier preventing the campaign authority/route-cleanup write while that LIVE epoch is still ACTIVE. A green campaign Git transaction cannot supply the missing source-close evidence.

**Violated owners.** Step-5.8 LAW 5.8-54 requires exact source close before relevant revocation. LAW 5.8-55 requires absorption/finalization, authorization and routing changes to share one campaign transition when they are one boundary. Laws 5.8-59/60 preserve partial freeze without establishing the intended transfer. W03 remains the owner of those proofs; Collaboration cannot replace them with a prepared access after-view.

**Minimal repair destination.** T04B integration and RD12 cross-owner tests. Before physical publication or success acknowledgement, consume the applicable existing W03 owner-bound final-source/forward evidence and required closure. When required evidence is unavailable or incomplete, stop without a campaign write. Keep the no-LIVE path working. Do not invent a boolean ACK, local CAS issuer, new generic publication authority, rollback, or a second semantic W03 implementation. A safe rejection is not evidence that the positive LIVE-sensitive publication path is implemented.

**Required RED/GREEN.** A real W03 transition with `LIVE_TRANSITION_REQUIRED` and an ACTIVE affected source must cause zero campaign ref writes; stale/rejected/indeterminate or partially completed source proof must not authorize the transition. Retain positive no-LIVE coverage and add the applicable genuine owner-proven completed-forward case before claiming LIVE-sensitive closure support. Recovery must not acknowledge a transition whose required LIVE boundary remains unproved.

## Version Impact and preserved scope

- T07B Story module `1.0.5 -> 1.0.6` is accepted. MECHANICS/projection-state schema v4 remains unchanged; this repair changes no persistent fields or migration/dual-read route.
- T04B collaboration module `1.0.16 -> 1.0.17` is the submitted, unaccepted candidate. Obligation schema v3 is unchanged. Its next material repair requires the normal fresh Version Impact assessment; the review does not approve its task merely because the version values are coherent.
- T04A full-body reload, unknown-agency bounded failure, historical hydration/current-admission separation and its prior PASS remain intact.
- W02, W03 and RuntimeHost are read-only producers for this review. Their earlier acceptance is not reopened by defects in the new T04B consumer.
- The existing CLS-HDM preflight and explicit reopen triggers remain unchanged. This review does not reread private CLS or waive a future actual trigger.
- No new host prerequisite, scope deletion, migration, release or gameplay bootstrap is authorized.

## Final dispositions and continuation

```text
W04.T04B: FAIL / TARGETED_REPAIR_REQUIRED
IRR-T04B-01: BLOCKING
IRR-T04B-02: BLOCKING
W04_AUTHORITY_COLLABORATION_RECONCILED: NOT ACCEPTED
W04.T05C: BLOCKED until repaired T04B independent PASS and other named inputs

W04.T07B: PASS / GO
IRR-T07B-02: CLOSED
W04_STORY_SOURCE_CONTRACTS_READY: ACCEPTED
W04.T07C: AUTHORIZED; not implemented or accepted by this review

WAVE_04: NOT COMPLETE
WAVE_05: NOT AUTHORIZED
VERSION_IMPACT: NONE for this review/control publication
SYSTEM_IMPACT: no new owner decision; enforce existing contracts in the T04B consumer
```

Run bounded T04B repairs and T07C in parallel only while write sets remain disjoint. Keep normal TDD, exact-head verification, independent review and publication/read-back gates. Do not reimplement accepted T04A/T07B or perform a whole-wave restore. If a genuinely missing accepted producer interface prevents the repair, record that concrete gap before crossing the owner boundary; do not invent one or turn ordinary code defects into a new architecture project. OpenCode reviewer permission denial is not permission for self-approval or bypass; coherent candidates may return to the independent reviewer here.
