# Superpowers artifact taxonomy

Status: **NON-AUTHORITATIVE NAVIGATION ENTRY**

This directory contains development-only research, design provenance, accepted implementation-facing specifications, and implementation plans. Semantic authority remains in the actual owning architecture/specification/decision/machine contract; this README only routes readers.

```text
DEV/docs/superpowers/
├── research/   what we investigated, learned, measured or discovered
├── design/     how a design/decision was developed and reviewed
├── specs/      final accepted implementation-facing specifications/decisions
└── plans/      implementation plans after approved design
```

## Default routing

| Directory | Put here | Do not treat as |
|---|---|---|
| `research/` | durable research findings, experiments, measurements, feasibility/comparative studies, idea dossiers | accepted architecture merely because evidence is retained |
| `design/` | Task Briefs, scope discovery, Source Manifests/working evidence, pre-acceptance Decision Briefs, critics, reviews, candidates, resolution gates, intermediate Step-1…8 records, process-history closure records, audit reports/status/cursors, rejected/superseded proposals | the default implementation-planning authority corpus |
| `specs/` | final approved specifications, accepted canonical amendments, final accepted owner decisions and other final documents required to implement the accepted design | an archive of every design-process artifact |
| `plans/` | implementation plans and execution-status records after approved design | architecture authority when the owning spec says otherwise |

For the eight-step design loop, standalone research belongs in `research/`; workflow/provenance artifacts belong in `design/`; the final accepted implementation-facing result belongs in `specs/`; implementation plans belong in `plans/`.

A mixed historical source may be split. If an intermediate/research artifact is the only carrier of accepted implementation-relevant law, promote/consolidate that law into a final spec or durable architecture owner before demoting the historical artifact. Avoid duplicate normative copies.

## Reading order for implementation planning

Start with current durable architecture owners and `specs/`. Use `design/` for provenance/reopening/audit and `research/` for evidence/applicability questions. A planner should not need to bulk-read design or research history merely to reconstruct already accepted architecture.

Historical old paths may remain inside exact historical statements, but current live routing references must follow current locations.