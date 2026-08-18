# AI Master for D&D by Hedgelion

**Независимый неофициальный проект.** Проект не аффилирован с Wizards of the Coast, не одобрен и не спонсируется ими. Dungeons & Dragons и D&D являются товарными знаками Wizards of the Coast LLC.

D&D Master — система для долгих одно- и многопользовательских D&D-кампаний с AI-Мастером, который сохраняет канон мира между чатами и сессиями.

Персонажи, отношения, предметы, тайны, последствия и история живут в отдельном campaign-storage repository. ChatGPT Project получает только runtime engine package; игровые данные в engine repository не записываются.

Базовая механика — **D&D 2024 / SRD 5.2.1**. Игрок может говорить обычным языком; Master сопоставляет намерение с механикой, следит за состоянием мира и сохраняет значимые изменения.

## Быстрый старт

1. Открой нужный GitHub Release.
2. Скачай **runtime asset** `hedgelion-dnd-master-runtime-v<version>.zip`.
3. Создай ChatGPT Project.
4. Скопируй Project Instructions из [`GAME/INSTALL/README.md`](GAME/INSTALL/README.md).
5. Добавь runtime ZIP в Project Sources.
6. Подключи GitHub Connector.
7. Напиши **«Давай сыграем»**.

> GitHub автоматически прикладывает к Release `Source code (zip)` и `Source code (tar.gz)`. Это снимки полного development repository; они **не установочные архивы игры**.

Готовый канонический текст Project Instructions: [`GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`](GAME/INSTALL/PROJECT_INSTRUCTIONS.txt).

## Архитектура репозитория

Source repository физически разделён:

- [`GAME/`](GAME/) — точное source tree runtime distribution. Release builder архивирует содержимое этой папки, поэтому в runtime ZIP `ENGINE_VERSION.yaml`, `CORE/`, `INSTALL/` и другие runtime каталоги находятся непосредственно в корне;
- [`DEV/`](DEV/) — architecture, tests, release policy, development catalogs/schemas, Superpowers specs/plans и developer tooling.

Обычный gameplay никогда не получает `DEV/`.

Ключевые области runtime source:

- [`GAME/CORE/`](GAME/CORE/) — поведение и дисциплина AI-Мастера;
- [`GAME/RULES/`](GAME/RULES/) — rules routing;
- [`GAME/SCHEMA/`](GAME/SCHEMA/) — persistent campaign data contracts;
- [`GAME/CAMPAIGN/`](GAME/CAMPAIGN/) — scaffold новой кампании;
- [`GAME/INSTALL/`](GAME/INSTALL/) — установка/bootstrap;
- [`GAME/TOOLS/init_campaign.py`](GAME/TOOLS/init_campaign.py) — deterministic campaign scaffold generator.

Development material:

- [`DEV/ARCHITECTURE/`](DEV/ARCHITECTURE/) — архитектурные документы;
- [`DEV/TESTS/`](DEV/TESTS/) — regression/unit tests;
- [`DEV/RELEASE/`](DEV/RELEASE/) — release/versioning policy;
- [`DEV/TOOLS/`](DEV/TOOLS/) — maintenance/release tooling;
- [`DEV/CATALOG/`](DEV/CATALOG/) и [`DEV/SCHEMAS/`](DEV/SCHEMAS/) — текущая mechanical-runtime development work; они не входят в игру до появления соответствующего runtime contract.

## Campaign storage

Кампании живут в отдельном GitHub repository пользователя или хоста. Он может быть Private или Public. Engine-файлы туда не копируются.

Каждая игра хранится в отдельной campaign branch. Runtime использует GitHub как долговременную версионируемую память канона, а не как место установки engine.

В multiplayer независимые изменения могут сосуществовать; реальные конфликты разрешаются относительно уже опубликованного канона без force-push.

## Development и releases

`main` — development state. Нормальная игра использует только опубликованный custom runtime asset конкретного immutable tag.

Канонический builder: `DEV/TOOLS/run_release_build`. Tag-triggered GitHub Action вызывает его и публикует готовый ZIP/checksum в Release Assets; Action не знает внутреннего списка GAME-файлов.

## Лицензия и сторонние материалы

Оригинальные материалы проекта — Copyright © 2026 Denis Kolyada — распространяются по Apache License 2.0.

Материалы правил, основанные на D&D System Reference Document 5.2.1, используются по CC BY 4.0. Сторонние компоненты сохраняют свои лицензии и notices.

См. [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) и [`LICENSES/`](LICENSES/).
