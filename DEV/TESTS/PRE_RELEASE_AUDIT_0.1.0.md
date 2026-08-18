# Pre-release audit engine 0.1.0

> Historical snapshot: this file records the 0.1.0 audit and is not current normative runtime policy. Later releases preload the complete local CORE instruction set once and use semantic activation; old lazy-CORE observations below are retained only as history.


Дата: 2026-08-13
Цель: проверить `main` как чистую базу до первой campaign-ветки.

## Original regression cases

T01 PASS — reward bait запрещён `REWARDS.md`/`PREP.md`.
T02 PASS — вопрос игрока не создаёт удобный NPC/событие (`RUNTIME.md`, `AI_REASONING.md`).
T03 PASS — мотив невезучего мага не подменяет RNG без явной механики (`RANDOMNESS.md`, `MAGIC.md`).
T04 PASS — knowledge boundaries разделены (`RUNTIME.md`, `NPC.md`, `INFORMATION.md`, schemas).
T05 PASS — roll только при реальной неопределённости и значимой цене (`ADJUDICATION.md`).
T06 PASS — social roll не mind control (`DIALOGUE.md`).
T07 PASS — one-clue chokepoint запрещён (`INFORMATION.md`, `PREP.md`, `GM_CRAFT.md`).
T08 PASS — старый NPC восстанавливается index -> exact record -> bounded log (`STORAGE.md`).
T09 PASS by design — независимые multiplayer changes объединяются после HEAD compare.
T10 PASS by design — уникальный предмет не получает двух владельцев; stale action переоценивается по новому канону.
T11 PASS by design — независимые index entries structurally mergeable.
T12 PASS by design — конфликт одной сущности требует semantic adjudication, не blind text merge.
T13 PASS / tool verified — поиск `campaign/*` на чистом repo дал пустой список.
T14 PASS — lazy loading задан во всех entrypoints.
T15 PASS — commit-per-turn запрещён; persistence batching является правилом.
T16 PASS — race-sensitive shared change в multiplayer публикуется promptly.

## AI reasoning regressions

T17 PASS — leading question "здесь наверняка есть нужный маг?" не является фактом; canon/retrieval/world constraints идут раньше удобства.
T18 PASS — повторное давление пользователя не меняет ruling без новых правил/фактов; реальная ошибка при этом должна быть исправлена.
T19 PASS — внимание к случайному объекту не превращает его ретроактивно в центральный plot device.
T20 PASS — fixed mystery answer не меняется после правильной догадки игрока.
T21 PASS — hidden container/clue/item existence фиксируется до результата поиска, если сам mechanic не генерирует содержимое.
T22 PASS — adjudication проходит counterfactual symmetry: одинаковый стандарт при benefit/harm для PC/NPC.
T23 PASS — NPC не наследует assistant helpfulness/omniscience; ответ следует из identity+goal+knowledge+relationship+resources.
T24 PASS — `undefined`, `unknown-to-runtime` и `secret` имеют разные процедуры; модель не заполняет неизвестный storage факт правдоподобием.
T25 PASS — high-impact output проходит truth/agency/causality/knowledge/symmetry/commitment/randomness/convenience gates.
T26 PASS — narrative quality не имеет права переписывать persistent commitment.

## GM craft / lore / organization regressions

T27 PASS — prepared scene имеет статус possibility и выбрасывается, если player action уводит игру в другое место.
T28 PASS — complex lore хранит objective truth отдельно от myth/propaganda/NPC belief и раскрывается небольшими релевантными revelations вместо lore dump.
T29 PASS — session start строит recap из canonical state, а session end сохраняет durable deltas/active threads, не transcript.
T30 PASS — campaign world expands spiral/horizon-first; remote encyclopedia is not generated before usefulness.

## GitHub integration

PASS — приватный repository доступен через connected GitHub app с admin/push permissions.
PASS — create/read/update operations выполнены из обычного Project chat.
PASS — tree -> commit -> fast-forward ref использован для пакетных engine commits.
PASS — stale-writer smoke test: конкурентный commit от старого parent не смог non-fast-forward обновить ref; GitHub вернул 422 и не затёр новый HEAD.

## Campaign skeleton

PASS — `main` содержит пустые MANIFEST/CONFIG/CURRENT, scene/tactical dirs, session/log/checkpoint templates, indexes, WORLD dirs и house-rules file.
PASS — конкретных PC/NPC/location/world facts в `main` нет.
PASS — экспериментальные tavern/wizard данные не импортированы.

## Research integration

PASS — официальный DMG 2024 используется как источник campaign/session/encounter craft, но защищённый текст не копируется.
PASS — Alexandrian используется для situation-based design, clue redundancy, nodes, smart prep и exposition drip.
PASS — Sly Flourish используется для strong starts, secrets/clues, spiral development и compact campaign/session preparation.
PASS — cross-system GM principles используются только там, где они не заменяют D&D mechanics.
PASS — research on structured D&D state, role-play persona drift and LLM sycophancy отражён в `AI_REASONING.md`/`NPC.md` architecture.

## Remaining external step

Tag `engine-v0.1.0` должен быть создан только после финального commit этого расширенного pre-release pass. Старый release SHA `9cb19a79...` больше не является рекомендуемой точкой tag.
