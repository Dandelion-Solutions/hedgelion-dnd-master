# Independent re-review — W04.T04A and W04.T07B repair round 2

Status: **FINAL REVIEW DISPOSITION — BOTH CANDIDATES FAIL / REPAIR REQUIRED**

Date: 2026-09-24

## Exact review basis

- Reviewed combined remote HEAD: `b13496b19bc8a7f11b82a24e11508036e815596f`.
- Parent: `b16ba8d2b4e3cffa86736fb20d10a34b01c97ff9`.
- T04A implementation: `20dd5301310bf5db250c229655ac957fe56e23c3`.
- T07B repair-round-2 implementation: `5a53b8e4323f53cde2f3c718e477003a4da3ce29`.
- Role: independent task re-reviewer. This review makes no implementation, test, schema or architecture change.

The prior full execution ledger, including author reports, previous findings, accepted task chains and the T04A Senior clarification, is retained at the same execution-status path in reviewed commit `b13496b19bc8a7f11b82a24e11508036e815596f`, blob `82560dd4b321a91c9f438401b964bcd6904f6ed3`. The rolling cursor routes current dispositions; that exact prior snapshot retains the detailed historical evidence, not a competing current cursor.

## Bounded source manifest and method

The review follows the stable Wave-04 task scope, current development execution process and ChatGPT Work transport overlay. Sources were read through GitHub Connector at the reviewed HEAD; no local repository transport or repository-wide preload was used.

| Source | Review use |
|---|---|
| `GAME/TOOLS/collaboration.py`, blob `e8efcb01d01da295c8b2b28e0f3c64d8e232837b` | historical hydration and after-authority reconciliation |
| `GAME/TOOLS/access_control.py`, blob `54e22e268026765892c9e82bdab6eb19a5e89ffe` | W03 exact-body guard and frozen transition |
| `GAME/TOOLS/runtime_host.py`, blob `bf1639e7d6f41ff2fbc52195a16dcddb5b2689fe` | actual pin/read boundary |
| `DEV/TESTS/test_rd12_collaboration.py`, blob `c97989048d0895e074244afbe3a81490a129b37b` | T04A witnesses |
| `GAME/TOOLS/story.py`, blob `6e54fa3993968dfe9d4da4088cc79de6a98c564b` | repaired unit, result and source-window validation |
| `DEV/SCHEMAS/story-mechanics-unit.schema.json`, blob `ad5a2cd11d2c6a5d24da1fc8de7a5a09efed440c` | MECHANICS v4 shape |
| `DEV/SCHEMAS/story-projection-state.schema.json` | contiguous coverage repair |
| `DEV/TESTS/test_rd13_story_t0_commentator.py`, blob `0140185c2ea2f3928dcd1e7357d158b670cd9991` | round-2 tests and registered-unit fixture |
| WP-17 canonical specification, blob `d49d817d796929c816ea2ae7bcd815d0986f1102` | accepted history, current agency, lifecycle and uncertainty |
| `2026-09-08-story-baseline-projection-source-contracts.md` | M-SEG/M-OUT and conditional omission contracts |
| stable Wave-04 plan and current execution ledger | task boundaries and producer gates |

Findings below are established by exact code/contract comparison and deterministic static path tracing. The proposed new regressions were **not executed by this reviewer**. Existing hosted tests were independently checked separately. A green existing suite does not prove an untested branch correct.

## Existing verification independently confirmed

Hosted run `35945179177`, job `107461446825`, ran on exact reviewed HEAD:

```text
workflow: Validate engine source
status: completed
conclusion: success
Run full maintenance audit: success
Run DEV unit tests: success
canonical command: .hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
Ran 1175 tests
OK (skipped=5)
VERSION_UNCLASSIFIED=[]
VERSION_LEGACY_HITS=[]
```

The local `.entire/` census failure did not reproduce in the clean hosted checkout. This does not claim the local capture-file/census interaction is repaired. No capture files or OpenCode permissions are changed here.

## Findings

### IRR-T04A-01 — BLOCKING — frozen campaign body is compared with itself

**Evidence.** `collaboration.py::_reconcile_access_transition` calls:

```python
publish_access_policy_transition(
    transition,
    current_campaign_revision=basis.pinned_campaign.revision,
    current_campaign=transition.current_campaign,
    current_player=current_player,
)
```

The PLAYER is reloaded, but the campaign body supplied as current is the transition's own frozen predecessor. `RuntimeHost._begin_operation` provides a campaign pin and selected LIVE routing, not an independently loaded campaign body. W03 compares its `current_campaign` argument to `transition.current_campaign`; this call makes the full-body guard tautological. Final host-basis equality does not perform the missing body comparison.

**Static witness / required RED.** Freeze a legitimate W03 transition from campaign body M. Keep the declared revision and PLAYER/obligation fixtures fixed, but have the exact native campaign read supply M' with an unrelated frozen field changed, removed or added. T04A never reads M', so the W03 full-body guard cannot reject that mismatch. This is inconsistent source/body evidence, not arbitrary mutation of trusted Python internals.

**Rule.** T04A exact after-authority reconciliation and the existing W03 full-campaign-body currentness rule.

**Minimal repair.** In the collaboration consumer, obtain the actual current campaign body through the existing pinned owner route and pass it to the W03 guard. Do not change the W03 semantic owner, introduce a new port, or defer this prerequisite to T04B. Add matching-body success and changed/missing/added-field negatives at the T04A entry point.

### IRR-T04A-02 — BLOCKING — unknown authority becomes terminal obsolescence

**Evidence.** `_pending_contributors_remain_authorized` returns `False` immediately for `campaign_mode == "singleplayer"`, explicitly because creator identity is unavailable in the frozen transition. This happens before checking the pending set. `_reconcile_access_transition` turns that `False` into `replace(obligation, lifecycle="OBSOLETE")` for affected OPEN/CLOSED obligations.

`test_singleplayer_transition_fails_closed_for_unverified_pending_agency` expects that terminal mutation. It ratifies the conflation instead of testing uncertainty separately.

**Rule.** WP17-27/41 require invalidated opportunity/required agency for obsolescence; WP17-73 prescribes bounded refresh/block/repair for uncertainty. Unknown creator authority does not establish invalidity. The T04A clarification preserves accepted inputs and distinguishes proved loss of current required agency from historical authorship.

**Required RED.** Where the available after-authority evidence cannot establish singleplayer creator/agency validity, reconciliation must fail closed without producing an OBSOLETE candidate. Separately retain a positive test where proven invalid required agency does justify obsolescence. Include a CLOSED or already-satisfied-input case so the unconditional branch cannot terminalize it solely because evidence is unavailable.

**Minimal repair.** Distinguish proved invalidity from unavailable evidence using existing failure/error paths. No new owner or host capability is required. Do not invent a blanket mode-change terminalization law as a substitute for the missing evidence.

### IRR-T07B-01 — BLOCKING — M-SEG Python admission and schema v4 disagree

**Evidence.** For M-SEG, `validate_story_unit` merges optional payload `resolution_refs`, optional `receipt_refs` and source-manifest refs into `owner_refs`. A matching segment selector in `sources` suffices even when both payload arrays are absent.

The current `story-mechanics-unit.schema.json` v4 condition for `campaign.mechanical_segments@...` requires at least one of those two payload fields. The same unit therefore passes Python admission and fails its declared serialized contract.

**Concrete static witness.** Start with existing `_registered_story_unit("MECHANICS")`. Delete `payload.resolution_refs` but retain `sources.owner.ref`, already bound to `runtime.resolution`, `resolution-1`, segment sequence 1. Python still finds the exact segment ref; the schema's conditional `anyOf` fails. The round-2 tests did not run this exact object through both validators.

**Minimal repair.** Align the owner-native validator and schema to one intended representation while preserving exact candidate/segment/receipt binding. Run the same positive/negative table through both validators: absent payload links, empty links, wrong owner, wrong segment, and valid linkage. Do not weaken source binding just to make the schema permissive.

## Other observations and evidence limits

T04A meaningfully separates historical accepted-association hydration from new input/catch-up admission. It retains input identities and does not publish or automatically create a successor. These improvements are not rejected or rolled back by the findings above.

T07B now checks exact M-SEG segment selectors and removes SPARSE from the baseline persisted coverage contract. Its unconditional SOURCE_CLASSIFIED/OMITTED rejection closes the previously permissive untrusted omission path. It is not evidence that legal native-proven omissions are implemented: the current helper has no positive proof-consuming route. This review gives no such completeness credit, but does not classify safe blanket rejection by itself as a new authority bypass. Keep that qualification explicit in downstream source/materialization evidence; never enable omission from a caller MAY_OMIT/reason flag. The blocking T07B disposition here is the concrete validator/schema disagreement above.

Accepted earlier tasks remain accepted. The existing CLS preflight is not reopened by this code/schema review. The arbitrary-Python-mutation/TCB threat model is unchanged.

## Final dispositions and continuation

```text
W04.T04A: FAIL / REPAIR REQUIRED
  IRR-T04A-01: BLOCKING
  IRR-T04A-02: BLOCKING
W04.T04B: BLOCKED until repaired T04A independent PASS

W04.T07B fix-round-2: FAIL / REPAIR REQUIRED
  IRR-T07B-01: BLOCKING
W04.T07C+: BLOCKED until repaired T07B independent PASS and normal prerequisites

WAVE_04: NOT COMPLETE
WAVE_05: NOT AUTHORIZED
VERSION_IMPACT: NONE for this review/control publication
SYSTEM_IMPACT: no new architecture decision made; bounded code/contract repairs required
```

Repair the two disjoint owner/test lanes in place. No whole-wave rollback, new RuntimeHost prerequisite, migration, branch or private-CLS work is authorized by this report. Preserve the accepted historical-input clarification and normal Version Impact discipline. Publish coherent candidates with focused/cross-owner tests and exact-head hosted evidence, then obtain fresh independent re-review. An OpenCode reviewer permission denial must not be bypassed or converted into self-approval.
