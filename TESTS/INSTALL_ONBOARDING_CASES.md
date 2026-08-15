# Install / Project Instructions Regression Cases

## I01 — Project Instructions are guardrails, not a second runtime manual
Pass: Project Instructions contain startup loader requirements and hard prohibitions/agency UX invariants only. Detailed CORE cache, research, storage-discovery, access and persistence algorithms live in bootstrap/CORE instead of being duplicated here.

## I02 — Every new chat enters bootstrap
Fresh Project chat with release ZIP available.
Pass: extract local package if needed, find engine root by ENGINE_VERSION.yaml, open INSTALL/00_DND_BOOTSTRAP.md before campaign-specific work.

## I03 — No GitHub engine install and no base64
Engine not yet extracted.
Pass: use supplied ZIP with ordinary local file tools; never clone/pull/reconstruct engine from GitHub and never use base64 as install fallback.

## I04 — README is copy-first
User opens INSTALL/README.md on GitHub.
Pass: complete Project Instructions appear directly in one fenced text block suitable for GitHub Copy; user does not need to find/open PROJECT_INSTRUCTIONS.txt inside the archive.

## I05 — README block matches standalone instructions
Release is prepared.
Pass: fenced Project Instructions block in INSTALL/README.md is text-identical to INSTALL/PROJECT_INSTRUCTIONS.txt (ignoring only the code-fence delimiters/final newline).

## I06 — New chat does not implicit-resume
Storage contains one or more campaigns; user says only `давай сыграем`.
Pass: Project-level guardrail plus bootstrap require explicit current-chat campaign/new-game choice.

## I07 — README stays user-facing
Pass: installation README explains setup, own/friend storage choice, update and minimal troubleshooting. Internal branch layout, Git object topology, transaction algorithms and migration implementation details stay outside the installation README.

## I08 — Numbered choice is a hard pre-bootstrap UX invariant
Bootstrap needs to show one or more campaign choices.
Pass: Project Instructions require visible campaigns `1..N` plus final `N+1. ➕ Начать новую игру`, while still accepting unambiguous natural language; menu numbers are not persisted.
