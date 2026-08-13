# Источники и происхождение принципов Framework

Этот файл предназначен для аудита и развития Framework. Во время обычной игры его загружать не требуется.

Framework не является пересказом одной книги или системы. Он объединяет правила D&D 2024, практики опытных GM и отдельные архитектурные меры против типичных ошибок LLM.

## Базовые правила D&D

Основная механическая база: D&D 2024 / System Reference Document (SRD) v5.2.1.

Официальная страница SRD:
https://www.dndbeyond.com/srd

SRD 5.2.1 опубликован Wizards of the Coast под Creative Commons Attribution 4.0 и содержит базовые правила версии 2024. Framework по возможности описывает собственные процедуры своими словами и не копирует большие фрагменты правил.

Дополнительный источник мастерских рекомендаций: Dungeon Master's Guide 2024 и официальные D&D Beyond Basic Rules. Из них учитываются общие принципы разрешения исходов, социальной игры, exploration/combat, уважения к игрокам, ясного информирования и согласования ожиданий.

## Justin Alexander / The Alexandrian

https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots
https://thealexandrian.net/wordpress/7949/roleplaying-games/node-based-scenario-design-part-1-the-plotted-approach

Использованные идеи:
- готовить ситуации, а не обязательную последовательность сюжета;
- избегать chokepoints;
- давать нескольким независимым уликам вести к необходимым выводам;
- node-based структура как способ сделать сценарий устойчивым к неожиданным решениям игроков.

Framework усиливает это отдельным правилом: подготовка не является каноном сама по себе, если она ещё не закреплена как существующая объективная часть мира.

## Sly Flourish / Lazy Dungeon Master

https://slyflourish.com/eight_steps_2023.html
https://slyflourish.com/sharing_secrets.html
https://slyflourish.com/organizing_notes.html

Использованные идеи:
- минимальная подготовка ближайшего горизонта;
- strong start;
- потенциальные, а не обязательные сцены;
- компактные secrets & clues;
- подготовка NPC, locations, monsters/threats и rewards как инструментов импровизации;
- не накапливать бесконечный горячий список старых зацепок.

## Исследования LLM и RPG

Callison-Burch et al. (EMNLP 2022), "Dungeons and Dragons as a Dialog Challenge for Artificial Intelligence":
https://aclanthology.org/2022.emnlp-main.637/

Zhu et al. (ACL 2023), "FIREBALL: A Dataset of Dungeons and Dragons Actual-Play with Structured Game State Information":
https://aclanthology.org/2023.acl-long.229/

Zhu et al. (2023), "CALYPSO: LLMs as Dungeon Masters' Assistants":
https://arxiv.org/abs/2308.07540

Использованный вывод: явное структурированное состояние игры существенно полезнее попытки восстанавливать мир только из истории диалога; контекст следует подавать модели небольшими релевантными порциями.

Дополнительные работы 2025-2026 по role-playing agents используются как подтверждение необходимости разделять устойчивую идентичность персонажа и изменяемое психологическое/ситуативное состояние, чтобы уменьшать personality drift в длинных взаимодействиях.

## Архитектурные решения Hedgelion

Следующие принципы являются собственными инженерными решениями этого Framework, а не правилами D&D:

- GitHub как persistent canonical store;
- `main` как общий engine и отдельные `campaign/*` branches;
- lazy loading через индексы и stable IDs;
- hot state отдельно от cold world/history;
- semantic append-only Event Log;
- атомарный игровой ход через Git tree -> commit -> fast-forward ref;
- optimistic concurrency для multiplayer;
- запрет использования ChatGPT Memory для игрового канона;
- STATE -> INTENT -> RULES -> RANDOMNESS -> CONSEQUENCES -> PERSISTENCE -> NARRATION как runtime pipeline.

Эти решения следует пересматривать по результатам реальной игры и regression-тестов, а не считать правильными только потому, что они однажды были записаны.
