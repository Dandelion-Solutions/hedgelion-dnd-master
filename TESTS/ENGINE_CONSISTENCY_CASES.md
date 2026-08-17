# Engine Consistency Regression Cases

`python TOOLS/audit_engine.py` is the executable release-level consistency gate
for these cases. Install its declared dependencies from
`requirements-maintenance.txt`. It is maintenance-only and is never part of
campaign runtime.

## EC00 — JSON schemas and catalog instances
Pass: every `SCHEMAS/*.schema.json` is a valid Draft 2020-12 schema, and the
core catalog plus identifier-policy catalog validate against their declared
schemas. A missing `jsonschema` dependency fails with an actionable install
command instead of silently skipping validation.

## EC01 — One CORE cache policy
Pass: complete local CORE is preloaded once; activation is header-driven; CORE_INDEX does not define a competing roster.

## EC02 — Exact always-active guard set
Pass: RUNTIME, AI_REASONING, PLAY_POLICY, DURABILITY_GUARD, MECHANICS_INTEGRITY and CHARACTER_READINESS are the modules whose headers say `ALWAYS_DURING_GAMEPLAY`.

## EC03 — Campaign data stays lazy
Pass: full CORE preload never implies preload of WORLD/STATE/INDEX/LOG/entities.

## EC04 — One owner for persistence timing
Pass: DURABILITY_GUARD owns ordinary WHEN, SAVE_CONTRACT owns explicit save, domain-specific shared/access modules may add explicit boundaries, and PERSISTENCE owns HOW only.

## EC05 — Sparse singleplayer survives generic scene events
Pass: ordinary scene/encounter/action completion, quest/NPC/item/resource changes do not independently create commits.

## EC06 — Stable IDs do not force solo commits
Pass: IDs may be reserved in hot state; when a durable reference is published, record+index are included in the same transaction.

## EC07 — Onboarding lifecycle is unambiguous
Pass: pre-live vignette/provisional PC may be durable while initializing; active requires READY_PC+PLAY_READY; stopping unfinished setup remains initializing; paused is post-PLAY_READY.

## EC08 — Story-first identity persistence
Pass: adopted name can create PROVISIONAL_IDENTITY even though exploratory drafting otherwise stays local.

## EC09 — Character authority is layered
Pass: DM may seed harmless surface defaults; explicit compatible player correction wins; player inner life remains player-owned; seeded details do not become player-authored by silence.

## EC10 — Campaign title is one authoritative value
Pass: MANIFEST owns title/origin; card is exact projection; README is supplementary protected projection.

## EC11 — README template protection
Pass: overview markers and guide markers are unique/in order; ordinary save cannot regenerate the protected guide.

## EC12 — Existing campaign persistence preserves base tree
Pass: routine transactions contain only semantic dirty paths and never publish formatting-only/unrelated template rewrites.

## EC13 — Concurrency safeguards remain tested
Pass: regression suite retains pre-commit ref probe, narrow post-commit race recovery, non-force update and known-frontier reuse cases.

## EC14 — Scaffold smoke test
Pass: exact local init_campaign.py creates root-layout initializing unnamed campaign, no storage marker leak, and protected README markers.

## EC15 — Engine maintenance cannot leak into gameplay
Pass: campaign bootstrap/setup/resume/gameplay/save/pause/session transitions do not run `audit_engine.py`, regression tests, lint/compile/release checks, or read TESTS/RELEASE/ARCHITECTURE/TEMPLATE as behavior instructions. `init_campaign.py` remains the narrow explicit-New-Game runtime tool exception.

## EC16 — Explicit engine maintenance favors thoroughness
Pass: only explicit engine-development/release/debug intent enters ENGINE_MAINTENANCE. In that mode long audits/tests/reasoning are allowed and gameplay latency constraints do not apply; an ordinary turn/save/scene boundary never enters it automatically.
