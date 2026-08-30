# Documentation Corpus Refactor — Frozen Execution Manifest

Status: **FROZEN MECHANICAL EXECUTION INPUT — DO NOT RE-DISCOVER POLICY**

This durable manifest set replaces ordinary continuation dependence on GitHub Actions artifact `dcr-reference-audit` (run `33275237058`, artifact `9721368558`, proof HEAD `0a354e3e5d82c5941f27f642bccb67b674311989`, artifact SHA-256 `f6d4709029fd796de17695982bed41c80e78e4c5286f7dbb21b8e54d9be99cf4`). The Actions artifact expires on 2026-09-05; these repository files are the durable mechanical continuation source.

Semantic authority remains in the completed DCR census and accepted architecture owners. This manifest encodes **419 targets, 1 extraction, 503 frozen reference-plan repairs, 1 mandatory verifier-derived repair (504 actionable total), 2 historical exceptions, and the final closure/STOP gate**. The 783 basename-only references that remain same-directory require no rewrite and are intentionally omitted from repair rows.

## Execution law

- `MOVE` is a true rename; never leave old/new duplicates.
- Repairs are exact line-scoped transformations anchored to proof HEAD; never global-replace.
- If a repair SOURCE target has already moved, use that target's final path.
- Each small coherent cluster must include its move(s) and every coupled repair in one internally valid atomic commit.
- Before publication: unreferenced candidate -> exact compare -> fresh remote HEAD -> `force=false` fast-forward -> read-back.
- Preserve the two historical exceptions.
- `X` is additional to the 503 reference-plan repairs and is mandatory before closure.
- After all work reaches zero, perform full replay/closure verification, then remove temporary DCR tooling and update durable status.
- **STOP after DCR closure. Do not begin WP-07 or any later workstream.**

## Encoding

Target: `ID|DEST|BASENAME`. Old root: `R-*` -> `DEV/docs/superpowers/research/`, `S-*` -> `DEV/docs/superpowers/specs/`. DEST: `K` retain, `D` -> `DEV/docs/superpowers/design/`, `R` -> `DEV/docs/superpowers/research/`.

Repair: `SOURCE|LINE|TARGET|KIND`. SOURCE is a target ID when possible or `E##` from Part 02. Kinds: `F` full old path -> full final path; `H` root-relative old -> final; `B` basename -> `../design/<basename>`; `I` basename -> full final path; `Q` release-fixture basename construction; `X` fixed replacement inline.

## Parts — read in order

1. `2026-08-30-dcr-frozen-execution-manifest-part-01.md` — targets 1–210.
2. `2026-08-30-dcr-frozen-execution-manifest-part-02.md` — remaining targets, extraction, external-source dictionary.
3. `2026-08-30-dcr-frozen-execution-manifest-part-03.md` — actionable repairs 1–252.
4. `2026-08-30-dcr-frozen-execution-manifest-part-04.md` — actionable repairs 253–504, exceptions, closure gate.

Progress is **not** frozen here; read `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-migration-journal.md` for the current cursor.
