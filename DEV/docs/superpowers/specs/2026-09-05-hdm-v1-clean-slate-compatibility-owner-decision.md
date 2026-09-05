# HDM v1 Clean-Slate Compatibility — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT SEMANTICS — CANONICAL INPUT**

Date: 2026-09-05

Source: direct Product Owner decision.

## Product Owner input — VERBATIM / IMMUTABLE

```text
В данный момент нигде не существует обязательств по совместимости. Версия 1.0 начинается с чистого листа и не совместима с версией 0.8. Весь абсолютно pre-release Skaffold можно считать obsolete и не тащить за собой. Всю структуру и, модели и инструкции можно переписать хоть полностью.
```

## Accepted product semantics

1. **No pre-release compatibility obligation exists.** HDM v1.0 starts from a clean product baseline.
2. HDM v1.0 is **not required to open, migrate, import, preserve or remain compatible with v0.8 or any other pre-release campaign/scaffold representation**.
3. Any pre-release scaffold, schema, structure, model, instruction surface, template or machine contract may be treated as obsolete and may be removed or replaced when current accepted architecture requires it.
4. No migration path, dual-read/dual-write compatibility layer, rollback-to-v0.8 path, adapter, compatibility shim or retained obsolete representation shall be introduced **solely** to preserve pre-release compatibility.
5. Existing pre-release repository artifacts have no compatibility authority merely because they exist. They remain subject to normal owner/currentness/staleness analysis and may be classified as current, stale, historical or debt by evidence.
6. This decision does **not** remove the need for WP-20 to define safe compatibility/update/migration semantics for campaigns created by released HDM versions from v1.0 onward. Future released-campaign evolution remains a real product/runtime concern.
7. This decision does not itself authorize implementation. WP-20 must consume it through the normal Source Manifest, Task Brief, critic and later architecture gates.

## WP-20 framing consequence

WP-20 must not spend architecture effort preserving obsolete pre-release formats. Its compatibility horizon begins at the released v1.0 baseline.

The core questions therefore become:

```text
released v1.0+ campaign/runtime/schema identity
 -> detect compatibility explicitly
 -> select only valid forward evolution/migration paths
 -> preserve stable IDs, authority, history/currentness/recovery/multiplayer semantics
 -> fail safely on unsupported/incompatible states
 -> define atomic migration/update success and recovery
```

Pre-release `0.8 -> 1.0` migration is explicitly outside the required compatibility surface.

## Classification

```text
PRODUCT / COMPATIBILITY POLICY
CLEAN-SLATE RELEASE BASELINE
PRE-RELEASE COMPATIBILITY: NONE
V0.8 -> V1.0 MIGRATION OBLIGATION: NONE
PRE-RELEASE STRUCTURAL FREEZE: NONE
CURRENT WP-20 CONSUMER: YES
NEEDS_PO: NONE
```

This owner decision does not change WP-19 clean-creation semantics and does not start WP-20 Step 1 by itself.