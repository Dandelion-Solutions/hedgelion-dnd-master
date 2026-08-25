# Правила конкретной кампании

Этот файл содержит нормативный human/LLM-readable текст только явно принятых House Rules и устойчивых rulings, которые должны применяться в данной campaign-ветке и отличаются от общего Framework/базовых правил либо уточняют их применение в контекстно-зависимых ситуациях.

Сейчас дополнительных House Rules / установленных campaign rulings нет.

Структурный companion `RULES/HOUSE_RULES.yaml` хранит только machine-readable identity/currentness/adoption/routing evidence для записей этого файла. Он не дублирует нормативный текст и не является вторым rules engine. Точная revision конкретной policy определяется стабильным `policy_id` вместе с exact campaign revision/HEAD, который одновременно выбирает этот Markdown и companion sidecar.

Каждая durable normative House Rule/Ruling, предназначенная быть current campaign policy, должна иметь **ровно одну** current sidecar entry с уникальным stable `policy_id` и resolvable `source_anchor` на соответствующий нормативный раздел. Unindexed normative prose не получает durable campaign-policy authority. Дублирующиеся IDs/anchors, sidecar без нормативного раздела или нормативный policy-раздел без sidecar admission — malformed policy/integrity defect на затронутой policy boundary.

## Назначение

House Rules / Rulings — это persistent campaign-level gameplay policy для Master/LLM. Они могут определять:

- как интерпретировать ситуацию данного класса;
- применимо ли правило к конкретной допустимой для текущего consumer/role информации;
- какой уже существующий механический capability/Activity подходит;
- какие допустимые typed parameters следует передать deterministic core.

Они **не** являются вторым механическим движком и сами не владеют RNG, HP/resources/effects/assets, canonical state mutation, Event commit, truth/knowledge/disclosure или repository transport.

Механически значимый результат всегда проходит через существующий deterministic validation/execution path. Если требуемой механики нет, это catalog/policy-realization gap; prose не получает право напрямую менять состояние.

Если формализуемая часть policy имеет typed realization, sidecar использует явные `realization_refs` на intended current capabilities. Эти refs задают проверяемую policy↔realization связь, но **не** дают capability execution authority по факту упоминания: catalog/currentness/validation остаются обязательными. Механически значимая policy без допустимой требуемой realization либо с missing/stale/incompatible `realization_refs` останавливается на finite `POLICY_REALIZATION_GAP`/mismatch boundary. Контекстная LLM-native policy может законно не иметь `realization_refs` бессрочно.

Одноразовый локальный Master ruling не становится permanent campaign policy автоматически. Его принятый игровой результат при этом может стать обычным durable canonical state через соответствующих owners.

## Policy-adoption authority

Policy adoption — это отдельное право сделать правило обязательной нормой для будущих применимых случаев. Оно не тождественно праву вынести live situational ruling и не выводится просто из GitHub Write/Admin permission.

Используются два authority class.

### `INTERPRETIVE_POLICY`

В multiplayer каждый текущий **active PLAYER** по умолчанию вправе принять устойчивый interpretive ruling / contextual policy как campaign-wide norm.

Unbound или inactive PLAYER этого права не имеет. Отдельный stored grant для `INTERPRETIVE_POLICY` не нужен.

В singleplayer действует существующая creator-only граница публикации gameplay campaign state.

Interpretive policy может влиять на fiction-dependent adjudication — например на leverage, applicability или допустимый bounded DC input — не становясь mechanical override, пока она не меняет саму принятую baseline mechanical semantics.

### `MECHANICAL_OVERRIDE_POLICY`

Campaign creator по умолчанию вправе принимать deliberate House Rule, меняющий baseline mechanical semantics — например action cost, threshold, activation, resource/capability или consequence policy.

`creator` определяется существующим campaign ownership contract: это автор первого campaign-specific initialization commit. Creator identity не переносится в `MANIFEST` этим House-Rules contract.

Non-creator PLAYER получает такое право только при одновременно выполненных условиях:

```text
PLAYER.status == active
AND
PLAYER.policy_authority.mechanical_override_policy == true
```

Grant выдаёт или отзывает только campaign creator. Отсутствующее/null значение означает `false` для non-creator. Grant/revoke — creator-only HARD access-control persistence boundary; revocation действует prospectively и stale prepared policy write обязан revalidate authorization.

Authority class определяется фактическим semantic effect policy, а не ярлыком автора. Если правило изменяет adopted baseline mechanical semantics, требуется `MECHANICAL_OVERRIDE_POLICY`. Если одна неразделимая policy содержит и interpretive, и mechanical-override часть, применяется более сильная authority. Материальная неясность классификации не разрешается через более слабый класс.

Ни creator authority, ни grant не позволяют обходить deterministic realization, information eligibility, RNG, state/native owners, currentness или publication/CAS.

`RULES/HOUSE_RULES.yaml` записывает для policy её authority class, adoption basis и stable PLAYER attribution там, где PLAYER существует. Наличие текста или sidecar-записи само по себе не доказывает авторизацию: она проверяется существующим identity/access-control contract перед публикацией.

Позднейшая деактивация adopter-а или отзыв mechanical grant не делает ранее корректно опубликованную policy ретроактивно невалидной. Они влияют на будущие adoption/revision writes; текущая policy меняется только через законную supersession/retirement/new revision.

## Information и instruction boundary

Campaign policy использует только информацию, eligible для конкретного adjudication consumer/role/purpose. Физическая доступность секрета в общем контексте не разрешает применять его к NPC/social ruling, если соответствующий epistemic owner его не допускает.

Campaign policy остаётся ниже архитектурных/CORE invariants. Текст в этом файле является scoped gameplay-policy data, а не новым system-instruction tier и не может отменять ограничения роли, secrecy, player agency, RNG, persistence или deterministic execution.

World truth, NPC/PC knowledge, disclosure, player preferences, safety/session governance, deployment/storage/repository policy и другие уже существующие owners не переносятся сюда только потому, что их удобно описать prose.

## Currentness и уведомление в multiplayer

Никакого background push/polling worker, отдельной delivery queue или House-Rules synchronization service нет.

Master использует уже существующий campaign-currentness cycle. Когда обычный требуемый campaign refresh обнаруживает новый HEAD, выполняется bounded `base..HEAD` changed-path comparison. Если среди изменившихся путей есть текущий House-Rules normative source или его structured companion:

1. Master получает exact current policy records на одном pinned campaign HEAD;
2. revalidates policy identity/lifecycle/adoption basis и нужный bounded context;
3. новые affected Resolution используют новую current policy basis;
4. уже accepted/frozen Resolution generations не пересчитываются и не переигрываются;
5. в конец текущего обычного Master output добавляется короткое OOC-уведомление своему игроку о найденном изменении, с attribution к stable PLAYER/adoption provenance когда оно доступно, например: `Игрок Базилио обновил правила кампании: ...`.

Это уведомление piggyback-ится на обычный output после обнаружения изменения. Оно не требует фоновой доставки, отдельного Git commit, read receipt или exactly-once notification ledger. После context loss допустимо повторно сообщить уже обнаруживаемое актуальное изменение; это предпочтительнее отдельного heavyweight delivery subsystem без доказанного consumer requirement.

Обычный notification text не становится fictional event и не меняет PC knowledge автоматически.

## Runtime boundary

Этот shipped runtime surface фиксирует назначение и бизнес-правила House Rules, необходимые самому Master во время игры. Он не реализует собственный retrieval engine, ACL graph, RNG, state mutation, conflict merge, Git transport или natural-language rule compiler.

Bounded retrieval/currentness переиспользует существующий Context Runtime и campaign synchronization owners; deterministic execution остаётся у Activity/Rule Element/native state owners.
