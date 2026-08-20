# Step 5.2 — Resumable Runtime Closure — Resolution Gate Addendum

Status: **RESOLUTION ADDENDUM ACCEPTED**

Date: 2026-08-20

This addendum supplements:

- `2026-08-20-step-5-2-resumable-runtime-closure-resolution-gate.md`
- `2026-08-20-step-5-2-resumable-runtime-closure-adversarial-review-addendum.md`

The original resolution gate remains valid except for its conditional temporal-root enrollment wording.

## Superseding refinement — armed due-capable temporal enrollment

The original gate retained:

```text
otherwise-unreachable armed due-capable temporal source owner
```

as the temporal root class.

That optimization is superseded.

Canonical resolution:

> Every armed native temporal source owner whose admitted obligation can become mechanically due independently of ordinary direct owner loading SHALL remain enrolled in bounded typed temporal-source routing throughout its armed lifetime, even when it is also transitively reachable through another active recovery root.

Reason:

- avoids dynamic transitive-reachability analysis on unrelated root termination;
- avoids an extra enrollment crash window;
- keeps temporal continuity local to temporal owner activation/terminality;
- simplifies write-time validation and cold recovery;
- remains bounded by currently armed independently-due obligations, not campaign history.

This does not make temporal routing a scheduler or semantic owner. Routing stores only typed owner/scope retrieval evidence. Deadline, due state, ordering, selected firing and lifecycle remain native.

The generic root-admission rule for non-temporal operational owners remains unchanged.

Human decision required: **NO**.

Canonicalization must incorporate this addendum and treat the prior conditional temporal-enrollment wording as superseded.