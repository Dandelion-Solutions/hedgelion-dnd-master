# Миграции кампаний

Этот каталог используется только когда released persistent campaign contract или конкретная persistent schema меняется несовместимо и для перехода существующей кампании требуется явное преобразование данных.

Engine-файлы не копируются и не merge'ятся в campaign repository. Runtime всегда берётся из точного локального runtime package; миграция кампании меняет только определённые campaign data/schema paths и допустимые campaign identity/adoption projections.

Каждая миграция должна явно указывать применимые source/target `campaign_contract_generation` и local `schema_version` значения, преобразуемые campaign paths, проверки после преобразования и rollback/checkpoint requirement. Если затрагивается отдельная совместимость storage repository, она принадлежит `storage_format_generation` и отдельному storage migration edge.

`engine_version` сам по себе не создаёт migration path и не доказывает необходимость миграции. Если обновление engine не меняет released persistent campaign contract/data, отдельная campaign migration не нужна.
