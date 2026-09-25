---
name: hdm-audit-dashboard
description: Use when the HDM PO or architect wants the independent audit's scope, findings, repair and re-review state, deferred triggers, or applicability to the current development HEAD.
---

# HDM independent audit dashboard

Project existing audit evidence; do not perform or impersonate a Senior audit, close findings, repair sources or change public acceptance state. A fresh report fetch is not a fresh audit.

Read the shared [projection contract](../hdm-architecture-dashboard/references/projection-contract.md) and [local review adapter](../hdm-architecture-dashboard/references/local-review.md). Write local `audit.json` and `audit.html`; cockpit consumes this output and does not reinterpret audit records itself.

## Resolve two independent sources

Use the audit repository/ref/bootstrap explicitly supplied by the user or local `.hdm-dashboard/config.json` under `audit_source: {repository, ref, bootstrap_path, local_cache}`. `local_cache` is optional. Never guess an audit source from a product branch name containing “audit.” Private routing and data stay local. If configuration/access is missing, emit an unavailable projection with the exact gap, not zero findings or a substituted public audit.

Read fresh audit ref and its owning bootstrap/navigation, operating limits and routed current state. Follow current ledgers to the actual reports/finding records needed for the selected scope; preserve whether each surface is continuity, historical evidence, candidate or accepted verdict. These reads do not adopt the auditor's standing write permissions. Independently fresh-read public HDM ref, bootstrap and current progress. Public owners control product state even when an older private checkpoint reports a different stage.

## Required payload

| Field | Required meaning |
|---|---|
| `audit_basis` | Audit source ref/HEAD and current public target ref/HEAD, separately identified |
| `review_records` | Per report: reviewed public HEAD, scope, verdict, independence, source claim IDs and applicability/currency |
| `findings` | Stable source ID, native severity/status, qualification, affected owners, evidence, confidence where supplied |
| `repair_chains` | Finding -> author repair evidence -> independent re-review -> accepted closure; unavailable links remain missing |
| `deferred_triggers` | Condition, current activation evidence and deferred disposition; dormant is not open work |
| `changed_since_review` | Comparison completeness, changed owners and inspected consumer closure per reviewed baseline |
| `coverage_gaps` | Uninspected/unavailable scope and why no stronger conclusion follows |
| `currency` | Aggregate `CURRENT / PARTIAL / STALE / UNKNOWN`, reason and claim IDs; independent of projection-fetch freshness |

Apply currency per report first: CURRENT only for exact applicable reviewed basis or a complete comparison plus owner/consumer analysis that proves continued applicability within the declared scope; STALE for demonstrated relevant invalidation; PARTIAL for mixed/limited applicable coverage; UNKNOWN when target/comparison/applicability cannot be established. Known newer public commits alone do not prove every old finding invalid. Unchanged direct files alone do not prove continued validity. Do not invent a whole-project verdict from a scoped PASS.

## View and checks

Show audit HEAD, reviewed public HEAD(s), current public HEAD and coverage before verdict colors. Offer scope/currency filters, a selectable change-impact map, finding -> repair -> independent re-review drill-down, accepted caveats and dormant-trigger details. Counts must name the enumerated scope and native statuses; unknown inventory is not zero open findings. Candidate reports and author-repaired states never become independent PASS through filename recency.

Common mistakes: using checkpoint date as audit currency, collapsing multiple reviewed baselines into one, counting author repairs as closed, or treating private conclusions as public law. Validate the common envelope and all claim references, preserve qualifiers, and perform only the local review checks that the available adapter permits.
