# Миграции кампаний

Этот каталог используется только когда новая версия engine меняет persistent schema или семантику campaign data и для перехода существующей кампании требуется явное преобразование данных.

Engine-файлы не копируются и не merge'ятся в campaign repository. Runtime всегда берётся из точного локального runtime package; миграция кампании меняет только определённые campaign data/schema paths и engine provenance в manifest.

Каждая миграция должна указывать исходную и целевую schema/engine version, преобразуемые campaign paths, проверки после преобразования и rollback/checkpoint requirement.

Если обновление engine не меняет persistent campaign data, отдельная migration не нужна.
