# Game Runtime Text Transport Design

Status: approved design direction; implementation pending review gate.

## Goal

Prevent HDM gameplay/runtime agents from wasting model context and work on manual Base64 conversion of semantically textual repository content during campaign-storage GitHub reads and writes.

This is a transport-efficiency rule only. It must not alter campaign canon, persistence timing, transaction atomicity, concurrency semantics, access control, or gameplay behavior.

## Scope

The rule applies to semantically textual repository payloads handled by the game runtime, including YAML, JSON, Markdown, plain text, source/configuration text, generated campaign scaffold text, storage metadata, campaign state, indexes, logs, checkpoints, and multiplayer live-state text.

It applies when the LLM/runtime prepares, reads, chunks, verifies, or publishes text through the GitHub Connector.

It does not prohibit Base64 for genuinely binary content. It also does not prohibit an internal Connector implementation from Base64-encoding UTF-8 text when the underlying GitHub API requires that representation; the LLM/runtime must not perform a redundant manual text -> Base64 -> text conversion around that Connector operation.

## Placement

Use two normative layers.

### 1. Early bootstrap guard

Add a concise text-transport rule to `INSTALL/00_DND_BOOTSTRAP.md` in the GitHub Connector/bootstrap transport area.

Reason: fresh storage initialization can write root `README.md` and `DND_STORAGE.yaml` before the complete CORE instruction cache is loaded. The bootstrap therefore must protect these earliest text writes.

The bootstrap rule must require UTF-8/text Connector interfaces for semantically textual repository content and forbid manual Base64 encoding/decoding for repository transport, chunking, staging, reconstruction, or verification when a correct text mode exists.

### 2. Canonical runtime rule

Add the detailed canonical rule to `CORE/PERSISTENCE.md`, which is authoritative for HOW GitHub writes are sequenced.

The rule applies to all existing persistence transport profiles:

- `CAMPAIGN_TREE_TXN`;
- `LIVE_STATE_CAS`;
- `STORAGE_METADATA_SINGLE`.

Other CORE modules should rely on this authority rather than repeat the same detailed policy.

## Required runtime behavior

For semantically textual content:

- read repository files through UTF-8/text Connector interfaces when available;
- create/update text through ordinary UTF-8 text arguments when the Connector operation supports them;
- for Git-data publication, create textual blobs using UTF-8 encoding rather than manually Base64-encoding content;
- preserve large text as text when chunking or reconstructing it; use line/range reads or equivalent text-safe chunking instead of Base64 merely to move chunks;
- verify exactness using actual file bytes, Git blob SHA, content SHA, or equivalent direct byte/blob identity checks rather than transforming text to Base64 first;
- do not create helper scripts whose only purpose is Base64 conversion of textual repository payloads.

If a specific required Connector operation has no usable UTF-8/text mode and explicitly requires Base64, Base64 is allowed only for that boundary. The runtime must not add additional encode/decode cycles beyond what is technically necessary.

## Existing specialized rules

Existing narrower rules remain valid:

- Project/bootstrap rules that forbid Base64 fallback for engine ZIP reconstruction remain unchanged;
- new-campaign scaffold rules that already require a coherent UTF-8 Git tree and forbid explicit Base64 remain unchanged;
- `LIVE_SCENE.md` does not need duplicate wording because its one-file CAS write remains governed by the persistence transport rule;
- `CAMPAIGN_SETUP.md` does not need duplicate general wording because its existing scaffold-specific UTF-8/Base64 prohibition is already stricter for that path.

## Regression coverage

Update `TESTS/PERSISTENCE_TRANSACTION_CASES.md` with a case that protects ordinary runtime persistence:

- campaign, live-state, and storage-metadata text publication uses UTF-8/text transport where available;
- no manual LLM/runtime Base64 encode/decode cycle is introduced for text;
- Connector-internal Base64 required by an underlying API is explicitly not a failure.

Update `TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` with a case that protects pre-CORE storage initialization:

- initial storage `README.md` and `DND_STORAGE.yaml` writes use Connector text/UTF-8 mode;
- no explicit Base64 reconstruction or text transport occurs at the LLM/runtime level.

## Non-goals

Do not change:

- persistence boundaries or durability classification;
- campaign/live transaction shapes;
- optimistic concurrency or CAS behavior;
- commit counts or ref-update rules except insofar as avoiding redundant transport work;
- game Project Instructions unless a later concrete gap proves the bootstrap guard insufficient;
- binary-file handling;
- Connector internals.

## Success criteria

After implementation:

1. a fresh storage initialization has an explicit early rule against manual Base64 transport for its text files;
2. ordinary campaign, live-state, and storage-metadata writes inherit one canonical runtime text-transport rule from `CORE/PERSISTENCE.md`;
3. text uses UTF-8/text Connector modes whenever available;
4. model-visible manual `text -> Base64 -> text` transport is forbidden unless no correct text-capable Connector operation exists;
5. existing transaction/concurrency/gameplay semantics remain unchanged;
6. regression documentation covers both bootstrap and normal persistence paths.
