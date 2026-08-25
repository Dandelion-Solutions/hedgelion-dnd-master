# Правила конкретной кампании

Этот файл содержит только явно принятые правила и устойчивые rulings, которые должны нормативно применяться в данной campaign-ветке и отличаются от общего Framework/базовых правил либо уточняют их применение в контекстно-зависимых ситуациях.

Сейчас дополнительных House Rules / установленных campaign rulings нет.

## Назначение

House Rules / Rulings — это persistent campaign-level gameplay policy для Master/LLM. Они могут определять:

- как интерпретировать ситуацию данного класса;
- применимо ли правило к конкретной допустимой для текущего consumer/role информации;
- какой уже существующий механический capability/Activity подходит;
- какие допустимые typed parameters следует передать deterministic core.

Они **не** являются вторым механическим движком и сами не владеют RNG, HP/resources/effects/assets, canonical state mutation, Event commit, truth/knowledge/disclosure или authorization/currentness.

Механически значимый результат всегда проходит через существующий deterministic validation/execution path. Если требуемой механики нет, это catalog/policy-realization gap; prose не получает право напрямую менять состояние.

Одноразовый локальный Master ruling не становится permanent campaign policy автоматически. Устойчивый precedent сохраняется здесь только после явного authorized adoption/publication.

Campaign policy остаётся ниже архитектурных/CORE invariants. Текст в этом файле является scoped gameplay-policy data, а не новым system-instruction tier и не может отменять ограничения роли, secrecy, player agency, RNG, persistence или deterministic execution.

Полный canonical architecture contract:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`
