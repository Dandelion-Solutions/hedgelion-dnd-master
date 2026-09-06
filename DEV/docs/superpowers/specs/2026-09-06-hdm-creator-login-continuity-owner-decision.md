# HDM Creator Login Continuity — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT / AUTHORITY SEMANTICS — CANONICAL INPUT**

Date: 2026-09-06

Source: direct Product Owner decision.

## Product Owner input — VERBATIM / IMMUTABLE

```text
Переименование GH юзера мы не будем поддерживать. Тут 2 риска: кража сессии игры под видом "я переименовал пользователя" с одной стороны и получение R/O игры с другой стороны. Я выбираю второе! в крайнем случае, если это действительно хозяин репозитория - он может вручную создать копию этой ветки со всей историей и тогда владелец новой ветки-сессии будет новый юзер. Игра тут стоит на своём и ничего менять не будет. Правила есть правила.
```

## Accepted product semantics

1. HDM does **not** support automatic continuity of campaign-creator authority across a GitHub login rename or another condition in which the current authenticated login cannot be proven equal to the historical creator-login provenance required by the current owner contract.
2. When creator identity cannot be established under the accepted creator-login rule, creator-only operations fail closed. A resulting read-only campaign is an accepted safety outcome.
3. HDM shall not substitute another identifier, infer a rename, accept a caller claim such as "I renamed my account", or silently transfer creator authority merely to recover write access.
4. Stable external user IDs used for PLAYER binding do not automatically replace creator-login provenance and do not confer creator authority.
5. Repository ownership, collaborator/Admin/Write capability or technical ability to mutate Git history does not by itself authorize the runtime to reinterpret the creator.
6. Manual repository-level recovery/copy performed deliberately by the repository owner is outside the automatic HDM creator-continuity guarantee. HDM does not promise or infer a particular recovery transformation from that possibility, and the runtime fail-closed rule remains unchanged.
7. This decision deliberately prefers preventing creator-session takeover over preserving automatic write continuity after login identity becomes unresolvable.

## Architecture consequence

Current login-derived creator authority is not considered incomplete merely because login continuity across rename is unsupported. Future access-control, bootstrap, migration and recovery work must preserve the fail-closed boundary and must not introduce automatic rename/ownership-transfer semantics without a new explicit Product Owner decision.

## Classification

```text
PRODUCT / AUTHORITY / SECURITY POLICY
AUTOMATIC CREATOR LOGIN-RENAME CONTINUITY: NOT SUPPORTED
UNRESOLVABLE CREATOR LOGIN: FAIL CLOSED
READ-ONLY CONSEQUENCE: ACCEPTED
STABLE-ID SUBSTITUTION FOR CREATOR AUTHORITY: FORBIDDEN
SILENT OWNER TRANSFER: FORBIDDEN
AUTOMATIC RECOVERY CLAIM: NONE
NEEDS_PO: NONE
```
