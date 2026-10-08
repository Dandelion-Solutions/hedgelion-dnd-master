# SP03 finite roll-policy checkpoint — independent review and proof

Status: **BOUNDED PRE-RNG ROLL POLICY PASS; FULL SP03 NOT PRODUCED**
Published implementation: `36987abf9e73187ff946b167d6dcca0db2256c96`
Frozen worker source: `68dd7e1567a24e297303c0f094056623be75fb07`
Independent reviewer: `ses_ee70bd82affeeSB7I39V93DEQ6`
Date: 2026-10-08

## Realized scope and review

Seven frozen paths were independently hash-checked: two allocated DEV schemas,
structural projection producer/generated output, `activity_runtime.py`, new
`calculation.py` and the installed-source roll-policy test. The final integrated
tree is identical to the reviewed worker tree.

`calculate_selector` checks genuine exact context issuance before calling the
raw DAG. The closed typed result retains occurrence/subject/source/policy/read/
membership and Contribution trace, sums exact scalar flat values, and normalizes
applicable advantage/disadvantage by presence. Counts and caller order do not
choose a winner; duplicate same-state grants do not stack. Predicate false and
missing remain distinct. Source/activity and native equipped/accessible Asset
eligibility are checked. Opposite operation conformance is isolated; production
metadata and dormant roster are unchanged.

Independent review initially found three Important defects: copied-context
provenance bypass, ignored native Resource gates and bool-as-integer acceptance
at cold compilation. Final re-review marked all three ADDRESSED and returned
SPEC PASS / QUALITY PASS, no open blocking issues. Twenty-one independent focused
tests covered repairs, genuine policy/cache positives and older raw/compiler
contracts. Required currentness and source guards were not replaced by fixture
completeness flags or caller truth.

Unsupported Resource gates, priority/stacking and unknown members reject in this
exact typed admission path; if a gate reaches consumption it produces the
existing AUTHORITY_UNAVAILABLE hold, not an ungated result. This does not claim
the whole Rule Element arbitration/gating law is implemented. Fixed raw-roll
selection remains explicitly held because the present root issuer supplies no
fixed-roll authority. No RNG, base D20 total, native spend or establishment is
produced by this slice.

## Final verification and transport

Actual coordinator commands on the clean committed source snapshot, using the
declared Python environment and `PYTHONDONTWRITEBYTECODE=1`:

- `python -m pytest DEV/TESTS -n auto`: **1809 passed / 42 skipped**.
- `python -m unittest discover -s DEV/TESTS -p 'test_*.py' -q`:
  **1644 tests OK / skipped42**; actual installed drivers run
  **24 context tests OK / 17 membership tests OK**.
- The roll-policy module adds **13 installed-source pytest cases**.
- `python DEV/TOOLS/run_maintenance_audit.py`: **PASS**.
- `python DEV/TOOLS/run_release_build.py --output <task-owned scratch>`: **PASS**.
- Version census unclassified/legacy sets empty; diff check **PASS**.

The earlier uncommitted worker run failed the clean-head provenance assertion;
its filtered rerun was not treated as full-suite acceptance. The final unfiltered
committed run above passes. Existing jsonschema deprecation warnings remain;
hosted CI and target latency were not inspected/measured.

Normal non-force publication, successful fresh `git fetch --prune origin` and
native ref/tree read-back exactly matched the implementation checkpoint.

## Version and remaining obligations

VERSION_IMPACT for code: `activity_runtime` 1.0.4 -> 1.0.5;
new `calculation.py` 1.0.1. Compatible optional/nonpersistent schema and projection
additions retain their versions; catalog2/profile1 and engine/persistent/campaign/
storage/digest generations unchanged. Review repairs did not create extra bumps.
This development-only review/control record VERSION_IMPACT: NONE.
SYSTEM_IMPACT: NONE within the accepted serialized policy allocation;
NEEDS_PO: NONE.

Damage-defense, AC base selection, capability projection, common cast preflight,
remaining DAG/arbitration/gating and broader native issuer joins remain. Next
typed damage realization must preserve exact type/origin/bypass and instance/group
identity, use actual source/compiled inputs, and implement source-defined ordered
rounding; it must not accept caller amount/base or substitute a generic override.
Original full-task/wave integration, source/recipe/native/product/performance and
activation gates remain; this checkpoint does not issue the SP03 ready output.
