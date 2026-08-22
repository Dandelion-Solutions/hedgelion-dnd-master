# HDM External Architecture Intelligence — Idea Dossier

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-21  
**Purpose:** материал для второго раунда архитектурного проектирования HDM  
**Repository policy:** документ намеренно не содержит названий внешних продуктов, проектов, исходных функций, URL или source provenance.  
**Decision policy:** ни одна запись ниже не является принятым решением HDM.

---

## 0. Как читать документ

Это не спецификация, не backlog и не roadmap. Это очищенный резервуар архитектурных идей, полученных из анализа существующих AI storytelling/RPG systems, scripting ecosystems, memory/context systems, community extensions и независимых экспериментальных движков.

Внешняя терминология намеренно удалена. Каждая идея нормализована по цепочке:

`observed mechanism -> underlying problem -> general architectural principle -> HDM-oriented formulation`

Классы:

- **DIAMOND** — фундаментальный кандидат. Может оправдать изменение уже существующей архитектуры или повлиять на новый roadmap.
- **STRONG** — сильная идея, которую надо сознательно рассмотреть, но она не требует немедленного изменения foundation.
- **RESERVE** — полезная/интересная мысль, преждевременная, узкая или platform-specific.
- **NEGATIVE INTELLIGENCE** — наблюдавшийся failure pattern или архитектурный анти-паттерн, который стоит помнить.

Текущая архитектура HDM считается strong base, но **не использовалась как фильтр**. Подробное сопоставление и конфликты с существующими этапами намеренно отложены до второго архитектурного раунда.

## 1. Executive synthesis

Разведка дала несколько повторяющихся независимых сигналов:

1. **«Память» должна распасться на несколько семантически разных систем.** Global summary, episodic retrieval, exact history, authoritative state и private actor continuity решают разные задачи.
2. **Context — это execution product.** Он должен собираться из durable sources по policy, иметь budget allocator и объяснимый trace.
3. **Главный риск автоматической памяти — не забывание, а ложная долговечность.** Ошибочно сконсолидированный факт начинает многократно усиливать сам себя.
4. **Retry/Undo — state problem, а не только text UX.** Любой history-dependent derived state должен понимать ветку/ancestry или уметь быть пересчитанным.
5. **NPC continuity требует epistemic separation.** Объективная истина, знание, убеждение, намерение и отношение одного NPC к другому нельзя хранить одним biography blob.
6. **LLM лучше всего работает как semantic interpreter/proposer, не commit authority.** Наиболее зрелый паттерн: bounded evidence -> proposed operation -> deterministic validation -> commit.
7. **Correctness under context pressure требует отказа от частичных decision inputs.** Для некоторых calls лучше defer, чем дать модели половину evidence.
8. **Auxiliary generation должен быть отдельным execution channel.** Summaries, cognition, extraction и repair не должны превращаться в видимые игровые turns.
9. **Deep archive и working context — разные вещи.** Сильная долгосрочная continuity требует и компактной рабочей памяти, и возможности глубокого exact retrieval.
10. **Наблюдаемость контекста — архитектурная необходимость.** Без inclusion/exclusion trace будет невозможно системно отлаживать забывание, starvation и disclosure.
11. **Shared history приобретает observational finality.** Retry/Edit перестают быть локальной операцией, как только другой участник мог увидеть результат или действовать на его основе.
12. **Async multiplayer — это collaboration protocol, а не сохранённый групповой чат.** Нужны persistent handoff/readiness/catch-up semantics, которые переживают отсутствие участников.
13. **Split-party является архитектурным тестом качества shared-world model.** Независимые сцены должны иметь отдельные context/chronology frontiers и сходиться только через material causal bridges.
14. **У multiplayer нет одного универсального turn model.** Свободная социальная/исследовательская сцена и строгая механическая последовательность требуют разных coordination policies.
15. **Один shared canon должен давать participant-scoped projections.** Objective truth общая, но доступное знание, секреты, narration и contextual evidence зависят от recipient/controlled actor.

Итоговая классификация этого прохода:

- **DIAMOND:** 24
- **STRONG:** 58
- **RESERVE / NEGATIVE INTELLIGENCE:** 48

---

# 2. DIAMOND — фундаментальные кандидаты

## D01 — Многослойная модель непрерывности вместо единой «памяти»

**Проблема.** Длинная кампания одновременно содержит объективное состояние мира, общую историю, конкретные старые эпизоды, свежую сцену, частные знания персонажей и временные намерения. Один общий memory blob неизбежно смешивает разные семантики и начинает конкурировать сам с собой за контекст.

**Почему это DIAMOND.** Это не оптимизация prompt-а, а разделение разных видов истины, производных представлений и кратковременного рабочего состояния. Такое разделение делает возможными независимые lifecycle, retention, rollback и selection rules.

**Возможная HDM-форма.** Рассматривать continuity как набор специализированных слоёв: authoritative structured state; always-required essentials; global narrative summary; episodic memories; entity-local history; recent exact history; transient scene state; private actor state; optional generation steering. Ни один слой не обязан быть копией другого.

**Архитектурные последствия.** Потребуется общий контракт происхождения и допустимых преобразований между слоями. Особое внимание — не создавать duplicate authority.

**Самый простой вариант.** Начать с authoritative state, recent exact history, global summary и episodic retrieval. Остальные слои вводить только при подтверждённой потребности.

**Сильнейший контраргумент.** Чем больше слоёв, тем выше сложность синхронизации и диагностики.

**Риски.** Несогласованные derived layers; чрезмерный background maintenance; неочевидный приоритет источников.

**Обратимость.** Высокая, если слои остаются projections/derived artifacts и не получают скрытую authority.

**Рекомендация.** Во втором раунде рассмотреть как базовую информационную модель, а не отдельную feature.

## D02 — Контекст вызова как материализованная проекция, а не хранилище знаний

**Проблема.** LLM context конечен и эфемерен, тогда как мир и кампания долговечны и значительно больше окна модели.

**Почему это DIAMOND.** Жёстко отделяет durable knowledge/state от того, что конкретный вызов модели увидит сейчас. Непопавшая в context запись не считается потерянной.

**Возможная HDM-форма.** Context Assembler строит bounded projection из authoritative и derived источников по typed relevance, privilege, role и budget policy.

**Последствия.** Контекст становится самостоятельным runtime product с входами, policy и trace, но не authority.

**Простой вариант.** Каждый candidate имеет source, semantic class, eligibility reason и размер.

**Контраргумент.** При очень больших context windows это может казаться избыточным.

**Риски.** Переусложнение selection; ошибочная уверенность, что retrieval всегда найдёт нужное.

**Обратимость.** Высокая: policy отбора можно менять без миграции канона.

**Рекомендация.** Считать фундаментальным принципом второго раунда.

## D03 — Единый семантический allocator контекста с reservations и degradation policy

**Проблема.** Если каждый subsystem сам «берёт сколько нужно», важные блоки вытесняются случайно; рост одного источника памяти способен уничтожить доступность другого.

**Почему это DIAMOND.** Переводит context pressure из случайного поведения в управляемую политику качества и correctness.

**HDM-форма.** Semantic budget classes, минимальные резервы, max budgets, protected/no-trim entries, допустимые downgrade representations и правила конкуренции внутри bucket. Важность и позиция — разные параметры.

**Последствия.** Нужны tokenizer-aware размеры и единый owner allocation policy.

**Простой вариант.** 4–6 semantic classes с min/max budget и `required | optional`; без сложного оптимизатора.

**Контраргумент.** Фиксированные квоты могут тратить окно впустую или не подходить разным моделям.

**Риски.** Rigid policy; starvation; чрезмерная настройка.

**Обратимость.** Высокая при policy-as-data.

**Рекомендация.** Брать принцип allocator, не копировать чужие проценты.

## D04 — Execution trace сборки контекста

**Проблема.** При забывании или утечке секрета без trace невозможно отличить отсутствие данных, ошибочный selector, budget eviction, privilege failure и неправильную позицию.

**Почему это DIAMOND.** Делает LLM context наблюдаемым и тестируемым, превращая «почему модель не знала?» в инженерный вопрос.

**HDM-форма.** Для каждого candidate record фиксировать source/revision, eligibility, matched selectors, privilege decision, rank, budget class, reserved/actual tokens, chosen representation, inclusion/exclusion reason, trim/downgrade и final position.

**Последствия.** Trace — development/debug evidence, не дополнительный runtime prompt.

**Простой вариант.** Структурированный trace для tests/diagnostics; UI не обязателен.

**Контраргумент.** Дополнительная instrumentation complexity.

**Риски.** Trace сам может содержать секреты; нужен access control.

**Обратимость.** Высокая.

**Рекомендация.** Закладывать до реализации Context Assembler: после факта добавить полную объяснимость сложнее.

## D05 — Mutable recent horizon перед долговременной консолидацией

**Проблема.** Свежий текст может быть Retry/Edit/Undo, поэтому немедленное создание долговременных summaries/memories приводит к derived artifacts, ссылающимся на уже отменённую историю.

**Почему это DIAMOND.** Создаёт чёткую границу между редактируемым фронтом истории и материалом, который уже безопасно консолидировать.

**HDM-форма.** Новые сообщения/события сначала остаются в exact mutable horizon. Derived consolidation допускается только после semantic/stability boundary либо хранит ancestry/revision и умеет откатываться.

**Простой вариант.** Не консолидировать последний bounded segment, пока он не вышел из retry/edit horizon.

**Контраргумент.** Увеличивает raw-context pressure и задерживает useful memory.

**Риски.** Слишком длинный horizon; неясная stability boundary.

**Обратимость.** Средняя.

**Рекомендация.** Рассматривать вместе с D06.

## D06 — History-aligned state: rollback/branch перемещает не только текст

**Проблема.** Retry/Undo, который меняет narration, но оставляет derived/mechanical/actor state из отменённой ветки, создаёт скрытую контаминацию.

**Почему это DIAMOND.** Синхронизирует narrative history и все history-dependent projections по общему ancestry, не делая prose источником истины.

**HDM-форма.** History-dependent state хранит association с history node/revision/accepted semantic event. При переходе по дереву истории восстанавливается ближайшее совместимое состояние/ancestry projection; canonical events требуют отдельной policy для branch/retry.

**Простой вариант.** Сначала сделать history-aware только truly derived/transient state; не применять автоматически ко всей canonical mechanics.

**Контраргумент.** Полный event-sourcing/branching state может быть чрезмерно дорог.

**Риски.** Случайное превращение UI-history tree в canonical chronology; дорогое snapshotting.

**Обратимость.** Средняя.

**Рекомендация.** Обязательная тема второго раунда retry/branch semantics.

## D07 — Разделить глобальное summary и episodic retrieval

**Проблема.** Один summary хорошо отвечает «о чём вообще кампания», но плохо возвращает редкую конкретную деталь; один semantic retrieval теряет общий сюжетный вектор.

**Почему это DIAMOND.** Это две разные cognitive задачи с разными failure modes.

**HDM-форма.** Поддерживать compact broad continuity summary и отдельный corpus небольших episodic records; retrieval строить по текущей сцене/actor/location/thread.

**Простой вариант.** Global summary + небольшие revisioned event summaries с retrieval.

**Контраргумент.** Дублирование увеличивает maintenance.

**Риски.** Summary drift; overlap; retrieval miss.

**Обратимость.** Высокая.

**Рекомендация.** Считать базовой memory decomposition.

## D08 — Per-entity continuity lifecycle вместо одной глобальной энциклопедии

**Проблема.** Для возвращающегося NPC/места/организации релевантна не вся история кампании, а её индивидуальная история и текущее состояние.

**Почему это DIAMOND.** Снижает retrieval search space и позволяет lifecycle/compaction, соответствующий entity.

**HDM-форма.** Entity имеет stable identity/canonical facts, mutable current state, bounded episodic trail и compressed older history. Entity history извлекается вместе с entity, но не становится новым canonical source.

**Последствия.** Нужны entity IDs, alias resolution, provenance и dedup с global memories.

**Простой вариант.** Только NPC и ключевые locations.

**Контраргумент.** Создаёт много мелких derived artifacts.

**Риски.** Расхождение global и entity summaries; ошибочное связывание aliases.

**Обратимость.** Средняя.

**Рекомендация.** Высокоприоритетный candidate для continuity subsystem.

## D09 — Evidence-bound durable mutation: модель предлагает, детерминированный валидатор коммитит

**Проблема.** LLM хорошо понимает смысл неоднозначного текста, но ненадёжно соблюдает authority, stale revisions, IDs и допустимые изменения.

**Почему это DIAMOND.** Позволяет использовать semantic intelligence модели без передачи ей права напрямую переписывать durable state.

**HDM-форма.** Bounded fresh evidence с IDs -> LLM предлагает строго ограниченную mutation или NO_CHANGE -> parser -> deterministic validator проверяет evidence membership, target ownership, current revision, legal shape/value -> максимум один commit -> audit/provenance.

**Последствия.** Может стать общим паттерном для memory promotion, actor continuity, entity extraction и natural-language mechanics proposals.

**Простой вариант.** Одна proposed operation за assessment; reject on ambiguity/staleness.

**Контраргумент.** Больше LLM calls и plumbing.

**Риски.** Валидатор проверяет форму лучше, чем смысл; evidence set тоже должен быть bounded корректно.

**Обратимость.** Высокая.

**Рекомендация.** Один из главных кандидатов второго раунда.

## D10 — Разделить stable identity, mutable continuity и transient state персонажа

**Проблема.** Если биография, текущая эмоция, долгосрочная цель и временная ситуация живут в одном тексте, любое обновление либо стирает основу личности, либо превращает мимолётный факт в вечный.

**Почему это DIAMOND.** Делает character continuity управляемой во времени.

**HDM-форма.** Stable foundation редактируется только explicit authority; durable evolving continuity меняется редко по evidence; transient private state имеет TTL/refresh; current scene projection собирается из этих слоёв.

**Простой вариант.** Foundation + durable relation/belief + transient goal/feeling.

**Контраргумент.** Большинство второстепенных NPC не нуждаются в таком уровне моделирования.

**Риски.** Over-modeling.

**Обратимость.** Высокая при tiered activation.

**Рекомендация.** Применять только к actors, которым continuity действительно нужна.

## D11 — Эпистемическая модель: объективный мир, знание, убеждение, подозрение и намерение — разные сущности

**Проблема.** LLM-RPG легко смешивает истину мира с тем, что конкретный NPC думает или знает.

**Почему это DIAMOND.** Позволяет настоящие тайны, ложные убеждения, расследования и последовательное поведение без contamination канона.

**HDM-форма.** Разделять world fact, observed evidence, private knowledge, belief, suspicion/hypothesis, intention/plan. Actor-local state имеет owner и provenance/evidence.

**Простой вариант.** Только `known`, `believed`, `intended` для material facts/actors.

**Контраргумент.** Полная epistemic logic быстро становится слишком сложной.

**Риски.** Record explosion; false precision.

**Обратимость.** Средняя.

**Рекомендация.** Narrow typed model, без универсального theorem prover.

## D12 — Направленные отношения и жёсткая граница player agency

**Проблема.** Симметричное `relationship(A,B)` теряет асимметричные чувства, долги, доверие и знания; автоматическая система легко начинает решать за игрока его чувства/согласие.

**Почему это DIAMOND.** Асимметрия отношений фундаментальна, а player agency — продуктовая гарантия.

**HDM-форма.** Actor-owned relation/view `A -> B`, отдельно от `B -> A`; NPC subsystem меняет только собственное отношение NPC. Player-owned mental/consent states не inferred/committed автоматически.

**Простой вариант.** Directed trust/stance/obligation records без универсальной social graph.

**Контраргумент.** Больше records и сложнее UI.

**Риски.** Переусложнение числовыми шкалами.

**Обратимость.** Высокая.

**Рекомендация.** Считать базовой семантикой actor continuity.

## D13 — Sparse/event-driven cognition вместо симуляции всех NPC каждый ход

**Проблема.** Постоянно «думать» за каждого NPC дорого, создаёт шум и провоцирует искусственное развитие персонажей вне значимых событий.

**Почему это DIAMOND.** Делает автономность экономичной и причинно привязанной к истории.

**HDM-форма.** Cognition запускается только для bounded focus actor при material evidence/trigger; режим выбирается из react/update-belief/reflect/plan/reconsider. Допустим NO_CHANGE.

**Простой вариант.** Один focus actor на accepted scene/turn при сильном trigger.

**Контраргумент.** Редко активируемые NPC могут казаться пассивными.

**Риски.** Trigger bias; starvation secondary actors.

**Обратимость.** Высокая.

**Рекомендация.** Предпочитать sparse cognition always-on multi-agent simulation.

## D14 — Целостный decision packet важнее частично втиснутого контекста

**Проблема.** Для bounded semantic decision случайное обрезание evidence/constraints делает результат формально валидным, но фактически недостоверным.

**Почему это DIAMOND.** Correctness principle: неполный вход хуже отложенного решения.

**HDM-форма.** Резервировать полный минимальный decision packet. Сначала деградировать representation (`full -> compact -> emergency`), затем убрать optional context; если packet всё равно не помещается — defer, не truncate.

**Последствия.** Allocator должен различать generative texture и decision-critical input.

**Простой вариант.** `min_complete_tokens` + известные downgrade representations.

**Контраргумент.** Некоторые decisions могут откладываться слишком долго.

**Риски.** Chronic pressure/defer loop; нужен bounded fallback.

**Обратимость.** Высокая.

**Рекомендация.** Применять к state mutation, mechanics interpretation и sensitive classification.

## D15 — Retry как отрицательное пространство предыдущих веток

**Проблема.** Повторный вызов с тем же context часто выдаёт почти то же продолжение.

**Почему это DIAMOND.** Использует информацию о том, что пользователь уже отверг, вместо слепой повторной выборки.

**HDM-форма.** При retry bounded subset предыдущих sibling continuations подаётся как `rejected alternatives / avoid these directions`, с отдельным total/per-attempt token budget. Это advisory context, не story truth.

**Простой вариант.** Последние 1–3 rejected siblings при manual retry.

**Контраргумент.** Негативные примеры могут якорить модель или расходовать context.

**Риски.** Prompt injection из rejected text; accidental canonization.

**Обратимость.** Высокая.

**Рекомендация.** Отдельный PoC; потенциально сильное улучшение Retry UX.

## D16 — Отдельный канал невидимых auxiliary generations

**Проблема.** Summarization, classification, entity extraction, cognition и repair не должны выглядеть как игровые turns или загрязнять narrative history.

**Почему это DIAMOND.** Разделяет пользовательское действие и engine maintenance, позволяет разные models/budgets/permissions.

**HDM-форма.** Auxiliary LLM calls имеют purpose, role/context policy, rate budget, cancellation/retry и output validator; не публикуются как narration.

**Простой вариант.** Синхронные невидимые auxiliary calls до/после visible turn; async не обязателен.

**Контраргумент.** Latency/cost.

**Риски.** Скрытая цепочка calls становится непрозрачной без traces.

**Обратимость.** Высокая.

**Рекомендация.** Считать orchestration primitive, если host profiles позволяют.

## D17 — LLM интерпретирует намерение; детерминированный runtime владеет механическим результатом

**Проблема.** Natural language богат и неоднозначен, а arithmetic/eligibility/resources/RNG outcomes должны быть воспроизводимы.

**Почему это DIAMOND.** Даёт immersive natural-language UI без передачи mechanical authority prose/model output.

**HDM-форма.** Input -> semantic candidates -> deterministic validation/eligibility -> deterministic resolution/RNG -> validated result -> narration. Narrative output никогда не вычитывается обратно в mechanics как authority.

**Контраргумент.** Интерпретатор всё равно может неверно понять intent.

**Риски.** Нужны correction/clarification paths.

**Обратимость.** Высокая.

**Рекомендация.** Сохранить как жёсткий принцип; разведка дала сильное независимое подтверждение.

## D18 — Двухступенчатый long-range archive retrieval + selective exact preservation

**Проблема.** Semantic search по всей многолетней кампании одновременно дорог, шумен и плохо возвращает точную формулировку редкого события.

**Почему это DIAMOND.** Комбинирует coarse relevance и fine exact evidence; позволяет compact working context без потери deep recall.

**HDM-форма.** Сначала выбрать relevant chapters/segments по overview/index, затем искать scenes/events внутри них; exact archive остаётся отдельным evidence source. Critical fragments могут иметь exact-protection.

**Простой вариант.** Segment summaries + bounded exact transcript/event archive lookup.

**Контраргумент.** Первый coarse selector может скрыть нужный segment.

**Риски.** Нужен fallback/global search.

**Обратимость.** Высокая.

**Рекомендация.** Высокий приоритет для длинных кампаний, не обязательно baseline MVP.

## D19 — Typed reactive selectors вместо keyword-only lore activation

**Проблема.** Совпадение слова слишком грубо: false positives, пропущенные смысловые зависимости, отсутствие scene/actor/location/role semantics.

**Почему это DIAMOND.** Превращает context activation в управляемую query boundary, пригодную для тестирования.

**HDM-форма.** Explicit entity refs, current scope, actor presence, state predicates, chronology/thread membership, semantic relevance и bounded dependency activation. Любая recursion имеет depth/budget/cycle limits.

**Простой вариант.** Entity IDs + scope predicates + optional semantic retrieval.

**Контраргумент.** Сложнее простых triggers и требует metadata.

**Риски.** Selector system может превратиться во второй rules engine.

**Обратимость.** Высокая.

**Рекомендация.** Проектировать narrow typed selectors под реальные consumers.


## D20 — Observational finality shared history

**Проблема.** В single-player Retry/Edit может быть локальной навигацией по ещё не принятой ветке. В multiplayer уже показанный outcome способен изменить намерения, решения и действия других людей. Тихая замена такого прошлого создаёт две несовместимые версии общей истории даже если storage технически умеет rollback.

**Почему это DIAMOND.** Появляется новая граница необратимости, заданная не только durability, а совместным наблюдением и использованием результата. Это напрямую влияет на retry/edit/branch semantics, disclosure и live publication.

**HDM-форма.** Различать как минимум private draft/candidate и shared-established outcome. До shared boundary локальный Retry/Edit может оставаться дешёвым. После неё изменение требует explicit branch, correction/reconciliation или нового compensating development; нельзя молча переписать прошлое, на которое другой participant уже мог опереться. Точную delivery-ACK на каждого recipient требовать не обязательно: допустима консервативная граница «опубликовано в shared frontier / отдано общему столу».

**Простой вариант.** Считать outcome observationally established сразу после успешного shared-state publication + player-visible emission, без per-recipient receipts.

**Контраргумент.** Слишком ранняя finality может сделать collaborative Retry неудобным и не позволит группе совместно исправлять очевидную неудачную генерацию.

**Риски.** Смешение fictional canon и presentation history; чрезмерное ограничение редактирования; дорогое per-recipient acknowledgement, если попытаться сделать границу слишком точной.

**Обратимость.** Средняя: поздняя смена shared-history semantics затрагивает retry, persistence и multiplayer UX.

**Рекомендация.** Обязательно решить во втором раунде вместе с history/branch/disclosure architecture.

## D21 — Async multiplayer как persistent collaboration protocol

**Проблема.** В асинхронной кампании участники появляются в разное время. Chat transcript сам по себе не отвечает, чей ход/вклад ожидается, что уже принято, что человек пропустил, где его rejoin frontier и можно ли продолжать без него.

**Почему это DIAMOND.** Async play превращает multiplayer из «несколько клиентов видят одну сцену» в durable coordination problem. Без отдельной collaboration semantics долгоживущая кампания либо блокируется самым медленным игроком, либо начинает действовать за отсутствующих участников.

**HDM-форма.** Persistent participant/session collaboration state может выражать readiness/expected contribution, handoff ownership, optional deadline/idle policy, last-consumed shared frontier, catch-up projection и explicit rejoin. Эти данные не обязаны быть fictional canon и не должны автоматически давать право действовать за PC.

**Простой вариант.** `participant -> last_seen_frontier + status + current expected-action state`; отсутствие участника никогда само по себе не authorizes PC action.

**Контраргумент.** Для свободной narrative игры formal readiness/handoff может ощущаться бюрократией.

**Риски.** Превращение RPG в workflow system; needless timers; смешение human availability и fictional chronology.

**Обратимость.** Средняя.

**Рекомендация.** Проектировать narrow collaboration layer, который поддерживает и synchronous, и asynchronous profiles без навязывания строгого round-robin вне нужных режимов.

## D22 — Split-party как несколько независимых scene/context frontiers

**Проблема.** Когда PCs находятся в разных местах или временно преследуют разные цели, один общий conversational context заставляет модель смешивать сцены, знания, NPC и causality. Запрет «никогда не разделяться» лечит ограничение prompt-а ценой самой RPG-свободы.

**Почему это DIAMOND.** Split-party проверяет, действительно ли мир является persistent state model, а context — проекцией, или вся игра существует как один линейный рассказ. Правильная модель одновременно улучшает multiplayer, concurrency и single-player multi-scene simulation.

**HDM-форма.** Каждая independently actionable scene получает собственный participant set, local context projection, local chronology frontier и mutable scope. Сцены не обязаны иметь total order. Reconciliation происходит только при material causal bridge: персонаж/предмет/информация/процесс пересекает границу, сцены сходятся или один outcome ограничивает другой.

**Простой вариант.** Separate scene records + recipient-scoped Context Assembler; никаких cross-scene merges без typed dependency.

**Контраргумент.** Параллельные сцены увеличивают orchestration complexity и могут ухудшать pacing группы.

**Риски.** Cross-scene causal races; секреты между subgroups; трудно определить момент convergence.

**Обратимость.** Средняя.

**Рекомендация.** Использовать как обязательный adversarial scenario второго архитектурного раунда, даже если baseline UX поощряет держать party вместе.

## D23 — Mode-specific turn orchestration вместо одного global turn model

**Проблема.** Exploration/social play допускает overlapping intentions, короткие реплики и совместное планирование, тогда как combat/contested mechanics требуют строгого actor order и eligibility gate. Один `active_player` для всего мира либо душит свободную сцену, либо не защищает механический порядок.

**Почему это DIAMOND.** Turn ownership — часть authority model, а не UI decoration. Разные interaction modes требуют разных rules for input acceptance, batching, resolution trigger и ordering.

**HDM-форма.** Coordination policy является mode/scope-owned: free-form scene может принимать несколько participant inputs и решать, когда запускать GM resolution; strict sequence разрешает только eligible actor/action; special group operations могут иметь отдельный collective trigger. Network/message arrival никогда само по себе не определяет fictional order.

**Простой вариант.** Два baseline режима: `free_form_shared_scene` и `strict_actor_sequence`, с explicit transition boundary.

**Контраргумент.** Дополнительный mode state и переходы могут дать edge cases вокруг начала/конца боя или одновременных заявок.

**Риски.** Double-resolution при переходе; starvation тихих игроков; неясный GM-response trigger в free-form режиме.

**Обратимость.** Средняя.

**Рекомендация.** Считать fundamental collaboration primitive, а не combat-only feature.

## D24 — Один shared canon, participant-scoped context и disclosure

**Проблема.** Multiplayer должен одновременно поддерживать общую объективную реальность и разные знания/секреты/местоположения игроков. Один shared prompt либо раскрывает лишнее, либо заставляет строить отдельные расходящиеся копии мира.

**Почему это DIAMOND.** Это объединяет truth ownership, epistemics, Context Assembler и multiplayer security. Ошибка здесь превращает repository/UI visibility в fictional knowledge и разрушает расследования, scouting, deception и split-party play.

**HDM-форма.** Canonical objective state остаётся единым. Каждый LLM/player-facing invocation получает recipient/controlled-actor scoped projection: только допустимая objective evidence, actor knowledge, current scene, party-visible state и role-specific private material. Disclosure itself может стать shared fact только через normal evidence/promotion boundary.

**Простой вариант.** `ContextRequest(recipient_player_id, controlled_actor_ids, scene_id, role)` + deterministic disclosure filter перед ranking/budget allocation.

**Контраргумент.** Recipient-specific context увеличивает calls/cache fragmentation и усложняет group narration.

**Риски.** Secret leakage через shared summaries, UI metadata, tool results или shared context caches; divergent narration if projections are built inconsistently.

**Обратимость.** Низкая-средняя: если privacy/knowledge semantics добавить поздно, уже созданные shared representations могут быть непригодны.

**Рекомендация.** Рассмотреть как один из core invariants multiplayer/context round-two design.
---

# 3. STRONG — сильные кандидаты

## S01 — Отложенная материализация новых сущностей
Не создавать durable entity record при первом упоминании. Требовать maturity/evidence threshold или повторную релевантность. Это снижает мусор, ошибочное связывание и auto-canonization. **Главный риск:** редкие, но важные entities могут не пройти threshold. **Вернуться:** при автоматическом entity discovery.

## S02 — Candidate ranking по recurrence + recency + diversity
При выборе entity/memory учитывать не только частоту, но давность и starvation/diversity. Популярные записи не должны навсегда захватывать весь budget. **Риск:** непрозрачная эвристика. **Вернуться:** при candidate queues/retrieval ranking.

## S03 — Разная степень доверия к источникам evidence
Player proposal, narrator draft, validated event и authoritative state не должны одинаково поддерживать автоматическую materialization/mutation. **Риск:** слишком сложная provenance lattice. **Вернуться:** при extraction/promotion.

## S04 — Semantic dedup между global и entity-local memory
Не отправлять модели один факт одновременно через несколько memory channels. Dedup должен учитывать смысл, provenance и priority. **Риск:** ошибочно схлопнуть похожие, но различные facts. **Вернуться:** после появления нескольких memory layers.

## S05 — Самовосстановление derived records
Derived indexes/memory metadata должны уметь обнаруживать malformed, duplicate и orphan records и ремонтироваться без изменения канона. **Риск:** repair маскирует producer bugs. **Вернуться:** при persistent derived indexes.

## S06 — Bounded active cast
Deep continuity/cognition поддерживать только для ограниченного активного состава; остальных переводить в compact/inactive representation с восстановлением при возврате. **Риск:** неверная demotion потеряет material context. **Вернуться:** при масштабировании NPC subsystem.

## S07 — Явные cognition modes
Разделять react, update belief, reflect, plan, reconsider goal. Один generic «подумай как NPC» prompt слишком смешивает задачи. **Риск:** orchestration branching. **Вернуться:** после базовой actor continuity.

## S08 — Защищённое ядро и selective forgetting
При pruning actor continuity защищать stable identity/core commitments; удалять stale/wrong/low-value мысли, а не просто самое старое. **Риск:** модель ненадёжно определяет «least useful» без deterministic constraints. **Вернуться:** при actor-local pressure.

## S09 — Authority-defined staged evolution
Долгая character arc может иметь разрешённое направление/стадии; runtime обновляет progress/stage по evidence, а не свободно переписывает личность. **Риск:** railroad. **Вернуться:** для authored companions/major NPCs.

## S10 — NO_CHANGE как полноценный outcome
Assessment может закончиться `NO_CHANGE`; это успешное рассмотрение, не ошибка. Оно может продвинуть opportunity clock и предотвращает forced mutation. **Риск:** чрезмерное бездействие. **Вернуться:** для evidence-bound assessments.

## S11 — TTL для временного private state
Текущая эмоция, напряжение, краткая цель или ситуация должны истекать без refresh, а не становиться вечной биографией. **Риск:** turn-count TTL может не соответствовать fictional time. **Вернуться:** при transient actor state.

## S12 — Lifecycle aliases/names
Alias проходит candidate/emerging/active/retired/rejected; активируется по evidence и ownership. **Риск:** лишняя machinery для простых campaigns. **Вернуться:** когда alias resolution станет реальной проблемой.

## S13 — Evidence accumulator с decay и promotion threshold
Повторяющийся слабый сигнал набирает confidence; неиспользуемые candidates затухают; threshold переводит hypothesis в более устойчивое состояние. Подходит для aliases, recurring motifs, inferred habits, emergent skills. **Риск:** искусственные numeric thresholds. **Вернуться:** для slow inference.

## S14 — Inspectable noncanonical planning artifact
Current pressures, unresolved threads, likely developments, beats и `do-not-resolve-yet` могут жить отдельно от prose/canon и быть заменяемыми. **Риск:** planner начинает диктовать сюжет. **Вернуться:** если появится отдельная planning role.

## S15 — World-pressure progression ladder
Долговременная угроза/фракция движется по стадиям и проявляется от ambient signs до direct confrontation. **Риск:** превращение в predetermined plot. **Вернуться:** для systemic authored threats.

## S16 — Timeskip simulation как bounded domain advancement
При пропуске времени выполнить ограниченные domain ticks: goals, factions, obligations, world state — затем построить re-entry context. **Риск:** causality и concurrent changes. **Вернуться:** если material timeskips становятся supported mechanic.

## S17 — Anti-stagnation pressure как soft signal
После серии тихих ходов priority ambient event может расти и сбрасываться после значимого события. **Риск:** искусственный шум. **Вернуться:** только как advisory pacing input, не источник событий.

## S18 — Bookmarks как ссылки на history nodes
Именованная точка истории хранит identity узла/ветки, а не копию всего state. Stale/missing target обнаруживается явно. **Риск:** нужен устойчивый history identity. **Вернуться:** при explicit branching/navigation UX.

## S19 — Reviewable summarization transformation
Высокоценное summary генерируется как candidate; может быть проверено/отредактировано/валидировано до promotion. **Риск:** human review нельзя делать gameplay requirement. **Вернуться:** tooling/maintenance и high-value summaries.

## S20 — Pinned critical context
Selected exact facts/evidence временно закрепляются в context до explicit discharge/unpin, вместо помещения в вечную global memory. **Риск:** pins копятся и захватывают budget. **Вернуться:** investigations, contracts, exact unresolved wording.

## S21 — Late steering как отдельный канал
Текущая narrative задача/тон/ограничение сцены находится ближе к generation frontier и не смешивается с world facts и campaign essentials. **Риск:** position effects model-dependent. **Вернуться:** при physical prompt topology.

## S22 — Bounded dependency activation
Активированная запись может активировать зависимые records, но recursion ограничена depth, budget и cycle detection. **Риск:** fan-out. **Вернуться:** при compositional world records.

## S23 — Visibility/secrecy как свойство записи
`secret to player`, `private to actor`, `inactive`, `unknown`, `false belief` — разные семантики. UI hiding не определяет semantic visibility. **Риск:** access model complexity. **Вернуться:** уже полезно как conceptual hygiene.

## S24 — Timed/ephemeral context
Некоторые guidance/conditions живут ограниченный semantic interval и автоматически исчезают. **Риск:** turns могут быть неправильным clock. **Вернуться:** для temporary narrative pressures/effects.

## S25 — Центральный tokenizer/token-cost service
Subsystems не считают chars самостоятельно; tokenization, model limits, cached-prefix accounting и fallback estimates принадлежат инфраструктуре. **Риск:** host может не раскрывать точный tokenizer. **Вернуться:** при physical orchestration profiles.

## S26 — Resumable maintenance workpiece
Многошаговое auxiliary обслуживание хранит bounded progress, продолжает после interruption и имеет retry/abandon limits. **Риск:** случайно построить distributed job platform. **Вернуться:** multi-call compression/materialization.

## S27 — Одна durable mutation на semantic assessment
Даже если обнаружено несколько possible updates, один assessment коммитит максимум одну bounded mutation. **Риск:** увеличивает backlog updates. **Вернуться:** при LLM-assisted state evolution.

## S28 — Sanitize operational protocol from visible output
Control markers, commands, JSON и maintenance artifacts не должны попадать игроку. Лучше physical channel separation; sanitization — дополнительная защита. **Риск:** string stripping не является security boundary. **Вернуться:** до auxiliary protocols.

## S29 — Dry-run context assembly
Assembler должен собирать полный context/trace без generation и side effects. **Риск:** дополнительный API. **Вернуться:** практически сразу при реализации context runtime.

## S30 — Capability-scoped extensions
Extension получает только явно разрешённые права: read world, propose delta, edit actor-private state, mechanics, file/network и т.д. **Риск:** capability taxonomy разрастается. **Вернуться:** если HDM становится расширяемым.

## S31 — Explicit lifecycle phases и ordering для extensions
Hooks имеют phase, deterministic order, propagation/stop semantics и ownership. **Риск:** переинженерить до появления plugins. **Вернуться:** принцип сохранить, реализацию отложить.

## S32 — Budget/rate-limit auxiliary generations как ресурс
Auxiliary calls имеют отдельные token/rate/cost budgets, cancellation и backpressure; background не означает бесплатный. **Риск:** scheduler complexity. **Вернуться:** при multi-call orchestration.

## S33 — Cheap deterministic lexical parser как hint generator
Глаголы, actor/object proximity, amounts и delimiters могут давать дешёвые candidates до LLM, но не final authority. **Риск:** brittle across languages/styles. **Вернуться:** optimization/fallback.

## S34 — Entity match: exact first, partial second, затем eligibility
Natural-language resolution сначала ищет exact semantic identity, затем controlled partial/alias match; до execution проверяет ресурсы/conditions. **Риск:** зависит от identity model. **Вернуться:** для natural-language mechanics.

## S35 — Structured fact register с semantic clustering
Крупные world changes, promises, debts и party facts могут иметь compact projection/index с near-duplicate clustering и provenance. **Риск:** создать вторую authority. **Вернуться:** только как projection поверх canonical owners.

## S36 — Witness/knowledge-aware retrieval weighting
Для actor recall реально witnessed/known evidence сильнее простого textual mention. **Риск:** нужны knowledge records. **Вернуться:** при actor-specific context.

## S37 — Deterministic spatial/travel sidecar
Координаты/связи/дистанции/route eligibility лучше считать структурно, narration получает validated result. **Риск:** не каждой кампании нужна карта. **Вернуться:** как модульный subsystem.

## S38 — Явные команды как admin/debug fallback
Immersive path остаётся natural language, но repair/admin/testing может иметь explicit commands для однозначной коррекции. **Риск:** не допустить command-first gameplay. **Вернуться:** diagnostics/recovery.

## S39 — Cache-aware rolling context
При provider prompt caching assembler может удерживать стабильный prefix и rollover старых элементов для снижения стоимости/лимитов. **Риск:** provider-specific. **Вернуться:** после deployment profile selection.

## S40 — Fairness против positional starvation
При равном priority учитывать starvation-age или менять placement policy, чтобы одни records не вытеснялись постоянно из-за стабильного порядка. **Риск:** random ordering ухудшает reproducibility. **Вернуться:** предпочесть deterministic starvation score.


## S41 — Authenticated participant -> controlled actor binding
Intent должен связываться не с display name и не с тем, кого модель «поняла» из текста, а с authenticated participant identity и explicit controlled actor set. **Ценность:** предотвращает acting-as-other-PC и делает provenance/security проверяемыми. **Риск:** host может не дать trustworthy principal identity. **Вернуться:** platform feasibility + multiplayer authority.

## S42 — Table administration отдельно от PC agency
Создатель/leader может иметь права invite/kick/settings/session management, но это не даёт его персонажу дополнительной fictional authority и не разрешает действовать за чужих PCs. **Риск:** convenience shortcuts начнут смешивать роли. **Вернуться:** access-control/profile design.

## S43 — Social/meta channel отдельно от diegetic action channel
Party chat, OOC coordination, ready signals и обсуждение плана не должны автоматически становиться character speech/action или canonical world evidence. **Риск:** лишняя UI-модель. **Вернуться:** multiplayer input protocol.

## S44 — Catch-up projection для returning participant
Возвращающемуся игроку нужен bounded recipient-specific пакет: material shared changes since last consumed frontier, current scene/party state, unresolved own obligations/expected input. Не нужно заставлять читать весь transcript. **Риск:** summary может скрыть важную exact detail. **Вернуться:** async/rejoin design.

## S45 — Mid-session join/rejoin как explicit frontier acquisition
Вход посреди сцены/боя — не просто добавление имени в participant list. Нужно atomically получить current authoritative frontier, bind/control actor, применить mode-specific admission (например initiative), определить knowledge baseline и только потом разрешить input. **Риск:** сложные join races. **Вернуться:** multiplayer lifecycle.

## S46 — Absence/idle policy без автоматического захвата PC
Async system может nudge, skip ожидание, разрешать observer status или explicit delegated control, но молчание игрока не означает согласие на AI/host control его PC. **Риск:** кампания может зависнуть без заранее выбранной policy. **Вернуться:** campaign multiplayer preferences.

## S47 — Presence/typing/reconnect являются operational UX, не authority
Online/offline, typing и connection state полезны для coordination, но не должны определять fictional presence, player binding или durability. **Риск:** product logic начнёт делать выводы из unreliable presence. **Вернуться:** host/live profile.

## S48 — Explicit entity/actor targeting как context hint
В shared conversation полезно иметь structured mention/target semantics: какой NPC, PC, item, scene или rule является объектом текущего сообщения. Это повышает retrieval precision, но не заменяет authority/identity checks. **Риск:** user mention может попытаться вытянуть secret entity. **Вернуться:** ContextRequest/selectors.

## S49 — Party-size-aware context budgeting
Чем больше участников/PCs, тем быстрее character sheets, private knowledge и recent dialogue захватывают context. Budget policy должна масштабировать representation (`full -> compact`) по relevance/scene participation, а не линейно добавлять всех игроков. **Риск:** второстепенный PC выпадет из внимания. **Вернуться:** context allocator.

## S50 — Per-scope serialization для truly conflicting live mutations
При собственном runtime shared actionable scope может использовать short critical section / revision lock / CAS, чтобы два concurrent resolutions не исполнились из одного stale base. Lock — transport/runtime tool, не fictional turn order. **Риск:** coarse global lock убьёт concurrency. **Вернуться:** API-controlled/live substrate profile.

## S51 — Push или cheap incremental synchronization для shared frontier
Другой participant должен узнавать material shared mutation без необходимости самому совершить действие. Если push невозможен, нужен дешёвый bounded currentness probe/resync. **Риск:** polling/streaming cost. **Вернуться:** host capability study.

## S52 — Bounded collaboration transfer state + durable deeper history
Async transport/session envelope не должен тащить весь campaign log. Recent actions/chat/catch-up можно cap/compact, если durable history и canonical state живут отдельно и recoverable. **Риск:** transport cap случайно станет retention policy. **Вернуться:** state hosting + sync protocol.

## S53 — Shared serving/model/safety profile должен быть явным
Если один host/owner выбирает модель, safety/tone/cost settings или другие serving параметры для всей группы, остальные должны понимать применяемый profile; это table policy, а не скрытая per-user preference. **Риск:** слишком много технических деталей в gameplay UI. **Вернуться:** deployment/host profile.

## S54 — Input collection window / batch как отдельный concept
В free-form shared scene иногда полезно принять несколько коротких intentions/replies до одного GM resolution, вместо генерации после каждого сообщения. Trigger может быть explicit ready, bounded debounce или GM policy. **Риск:** задержка и ambiguity «кто ещё собирался действовать». **Вернуться:** free-form turn orchestration.

## S55 — Read-only spectator/replay projection
Просмотр кампании можно отделить от gameplay membership: spectator/replay получает sanitized derived projection без write authority и без hidden/private state. **Риск:** accidental disclosure через replay assets/context. **Вернуться:** sharing/publication features.

## S56 — Solo fork shared campaign как explicit branch operation
Участник может продолжить копию общей истории самостоятельно, но fork наследует только выбранный established frontier и дальше имеет отдельную authority/chronology. Никакой обратной записи в исходную кампанию без отдельного merge/reconciliation design. **Риск:** пользователи могут принять fork за «тот же мир». **Вернуться:** branch/product semantics.

## S57 — Invite/discovery mechanism не равен durable authority binding
Join code/link/request полезен для discovery/onboarding, но право изменять shared canon должно появляться только после authenticated membership/binding transition. **Риск:** дополнительный onboarding friction. **Вернуться:** host identity/access feasibility.

## S58 — Mixed human/AI controller assignment должен быть explicit
Party member может быть human-controlled, temporarily delegated или AI-controlled, но controller ownership должен храниться отдельно от character identity и меняться явным transition. **Риск:** AI takeover может нарушить player agency. **Вернуться:** absence/delegation/companion design.
---

# 4. RESERVE / NEGATIVE INTELLIGENCE

## R01 — Keyword-only activation
**Тип:** RESERVE. Прост и дешёв, но даёт substring false positives, требует ручных trigger hacks и не знает semantic scope. **Вывод:** только один signal среди typed selectors.

## R02 — Неограниченная cascading activation
**Тип:** NEGATIVE INTELLIGENCE. Удобна для связанного lore, но создаёт fan-out/cycles/context explosion. **Вывод:** dependency activation требует depth/budget/cycle caps.

## R03 — Автоматическое создание новых durable facts при генерации entity record
**Тип:** NEGATIVE INTELLIGENCE. Нормально для co-writing, опасно для RPG canon. **Вывод:** extraction/summarization можно автоматизировать; invention durable canon — отдельная authority process.

## R04 — Парсить художественный output ради HP/damage/resources
**Тип:** NEGATIVE INTELLIGENCE. Mechanics становятся зависимыми от формулировки prose. **Вывод:** narration никогда не mechanical authority.

## R05 — Выводить механическую стоимость/число из сгенерированного текста
**Тип:** NEGATIVE INTELLIGENCE. Model-generated number превращается в правило через regex. **Вывод:** числа/формулы приходят из policy/catalog/resolution.

## R06 — Один call одновременно меняет private mind и пишет видимый рассказ
**Тип:** NEGATIVE INTELLIGENCE. Смешивает privileges и валидацию. **Вывод:** auxiliary semantic decision и narration разделять.

## R07 — Скрытая provenance через zero-width/in-band markers
**Тип:** NEGATIVE INTELLIGENCE. Хрупко, может утечь и портиться. **Вывод:** out-of-band structured IDs.

## R08 — Maintenance, потребляющий видимый Continue/turn
**Тип:** NEGATIVE INTELLIGENCE. Служебная операция становится gameplay. **Вывод:** invisible auxiliary channel.

## R09 — Огромная regex/keyword grammar как authority parser
**Тип:** RESERVE. Может быть hint layer, плохо масштабируется по языкам. **Вывод:** candidates/fallback, не authority.

## R10 — Дублировать state во внутреннем объекте и редактируемой текстовой карточке
**Тип:** NEGATIVE INTELLIGENCE. Неясно, какая копия authoritative. **Вывод:** editor/projection над одним owner.

## R11 — Симметричное relationship value
**Тип:** NEGATIVE INTELLIGENCE. Теряет асимметрию знания/доверия/долга. **Вывод:** directional actor-owned relation.

## R12 — Симулировать мысли каждого NPC каждый turn
**Тип:** NEGATIVE INTELLIGENCE. Дорого и создаёт искусственные events без evidence. **Вывод:** sparse/event-driven cognition.

## R13 — Жёсткая plot ladder как обязательный сюжет
**Тип:** RESERVE. Держит историю собранной, но подрывает свободу. **Вывод:** только authored pressure/advisory, не predetermined outcome.

## R14 — Model/tokenizer-specific phrase bias
**Тип:** RESERVE. Низкая portability. **Вывод:** profile-specific optional tuning, не core architecture.

## R15 — Banned-token/word-control как основной steering/safety механизм
**Тип:** NEGATIVE INTELLIGENCE. Provider support и tokenizer semantics нестабильны. **Вывод:** semantic instructions/policies.

## R16 — Prompt-format folklore без измеряемой contract semantics
**Тип:** NEGATIVE INTELLIGENCE. Скобки/separators/ритуалы часто привязаны к конкретной модели. **Вывод:** model-specific formatting только как evidence-backed profile optimization.

## R17 — Случайное событие только ради того, чтобы «что-то произошло»
**Тип:** RESERVE. Борется со стагнацией, но без causal pressure выглядит шумом. **Вывод:** сначала causal event candidate; randomness только selector.

## R18 — Автоматическое summary без provenance/verification
**Тип:** NEGATIVE INTELLIGENCE. Ошибка summary может многократно усилить себя. **Вывод:** derived candidate с source coverage/provenance и repair path.

## R19 — Копировать фиксированные проценты context budget
**Тип:** NEGATIVE INTELLIGENCE. Чужие числа отражают другой продукт/model tier. **Вывод:** брать allocator, не квоты.

## R20 — Char-count вместо tokenizer-aware budget
**Тип:** RESERVE. Разъезжается между языками/моделями. **Вывод:** только emergency estimate.

## R21 — Первое совпавшее имя = entity identity
**Тип:** NEGATIVE INTELLIGENCE. Aliases/омонимы ломают continuity. **Вывод:** IDs + scoped resolution + aliases.

## R22 — Хранить каждую transient мысль навсегда
**Тип:** NEGATIVE INTELLIGENCE. Actor memory превращается в мусорный журнал. **Вывод:** TTL/pruning/promotion.

## R23 — Создавать долговременную memory каждый turn
**Тип:** NEGATIVE INTELLIGENCE. Memory захватывает budget и накапливает шум. **Вывод:** stability horizon + selective consolidation.

## R24 — Постоянный отдельный комментатор на каждую сцену
**Тип:** RESERVE. Может быть entertaining, но добавляет latency/context и нарушает tone. **Вывод:** optional role/profile.

## R25 — Встраивать metadata/lore в изображения ради переносимости
**Тип:** RESERVE. Интересный distribution trick, сейчас не соответствует storage model. **Вывод:** вернуться только для community-content packaging.

## R26 — Пользователь вручную лечит memory, удаляя записи и регулируя triggers
**Тип:** NEGATIVE INTELLIGENCE. Engine problem переносится на игрока. **Вывод:** automated diagnostics/repair; ручная коррекция — escape hatch.

## R27 — Always-on essentials без hard size discipline
**Тип:** NEGATIVE INTELLIGENCE. Oversized required context вытесняет всё остальное. **Вывод:** always-required class тоже имеет schema/size discipline.

## R28 — Рекурсивные world records, активируемые собственным текстом без explicit dependency model
**Тип:** NEGATIVE INTELLIGENCE. Скрытые цепочки и order dependence. **Вывод:** explicit typed dependencies + trace.

## R29 — Retry без информации об отвергнутых попытках
**Тип:** NEGATIVE INTELLIGENCE. Temperature часто возвращает тот же attractor. **Вывод:** проверить D15.

## R30 — Изобретать отсутствующие детали вместо явного `unknown`
**Тип:** NEGATIVE INTELLIGENCE. Модель естественно заполняет пробелы и превращает догадку в continuity. **Вывод:** unknown/uncertain должны быть representable states.


## R31 — Второе лицо `you` как multiplayer identity
**Тип:** NEGATIVE INTELLIGENCE. Несколько PCs, каждый называющий себя `I/you`, легко сливаются в одного protagonist. **Вывод:** originator/actor identity должна быть structured; grammatical perspective только presentation aid.

## R32 — Host автоматически становится главным героем
**Тип:** NEGATIVE INTELLIGENCE. Общий narrator склонен центрировать инициатора/host и превращать остальных PCs в side-NPCs. **Вывод:** host/table authority не даёт narrative protagonist priority; attention/fairness policy должна смотреть на scene participation.

## R33 — AI дописывает действия за чужих player characters
**Тип:** NEGATIVE INTELLIGENCE. Даже явный prompt «не действуй за PCs» не является достаточной agency protection. **Вывод:** player-controlled actor action requires owned intent/evidence; narration ограничена последствиями и непроизвольными реакциями по правилам.

## R34 — Запрет split-party ради ограничения модели
**Тип:** NEGATIVE INTELLIGENCE. «Никогда не разделяйтесь» маскирует отсутствие scene isolation и лишает RPG естественной свободы. **Вывод:** split-party должен быть supported architecture scenario, даже если UX предупреждает о pacing cost.

## R35 — Внешний мессенджер как обязательный turn coordinator
**Тип:** NEGATIVE INTELLIGENCE. Если игроки должны отдельно сообщать «я закончил ход», host не владеет собственным collaboration protocol. **Вывод:** readiness/handoff должны быть доступны внутри supported multiplayer profile.

## R36 — Overlapping actions без arbitration
**Тип:** NEGATIVE INTELLIGENCE. Unlimited concurrent inputs при одном линейном narrator output дают races, contradictory outcomes и protagonist confusion. **Вывод:** mode-specific input collection + shared resolution boundary.

## R37 — Network/message order становится fictional chronology
**Тип:** NEGATIVE INTELLIGENCE. Кто раньше отправил пакет/commit, не обязательно раньше действовал в мире. **Вывод:** technical ordering — evidence/currentness, fictional order принадлежит mechanics/chronology.

## R38 — Local Retry/Edit после того, как outcome уже использован другими
**Тип:** NEGATIVE INTELLIGENCE. Тихо переписывает общий past и оставляет чужие действия без причинной основы. **Вывод:** после shared-established boundary только explicit correction/branch/reconciliation.

## R39 — Один общий context blob для всех participants и secrets
**Тип:** NEGATIVE INTELLIGENCE. Упрощает generation, но делает private knowledge и split scenes практически незащищёнными. **Вывод:** recipient-scoped projections поверх shared canon.

## R40 — Party chat автоматически становится diegetic/canonical
**Тип:** NEGATIVE INTELLIGENCE. OOC planning, шутки и coordination начинают восприниматься как сказанное/сделанное персонажами. **Вывод:** channel semantics должны быть explicit.

## R41 — Invite token/link считается достаточной write authority
**Тип:** NEGATIVE INTELLIGENCE. Possession of a share secret — discovery proof, не устойчивая campaign identity. **Вывод:** authenticated binding отдельно от invitation.

## R42 — Unlimited party size без degradation/load policy
**Тип:** NEGATIVE INTELLIGENCE. Количество игроков растёт быстрее, чем context attention, input arbitration и narration bandwidth. **Вывод:** capability profile должен иметь tested envelope и representation degradation, а не маркетинговое «без лимита».

## R43 — Другие клиенты узнают shared mutation только после собственного действия
**Тип:** NEGATIVE INTELLIGENCE. Создаёт stale-world interaction и delayed reactions. **Вывод:** push/incremental resync либо cheap currentness probe до race-sensitive action.

## R44 — Один global active-player gate во всех режимах
**Тип:** NEGATIVE INTELLIGENCE. Работает для strict sequence, но делает dialogue/exploration механистичным и блокирует короткую групповую координацию. **Вывод:** active-actor semantics принадлежат конкретному mode/scope.

## R45 — Все участники одновременно редактируют shared prompt/context essentials
**Тип:** NEGATIVE INTELLIGENCE. Неструктурированные concurrent edits к global instructions/character essentials дают de-sync и гонки authority. **Вывод:** explicit owner/editor permissions + revisioned structured state; runtime context собирается из него.

## R46 — Общий model/safety profile применяется к группе скрытно
**Тип:** NEGATIVE INTELLIGENCE. Участники могут ожидать свои настройки, а фактически играть под host policy. **Вывод:** shared serving policy должна быть видима и consent-compatible.

## R47 — UI раскрывает неизвестные entity names/images раньше fictional discovery
**Тип:** NEGATIVE INTELLIGENCE. Даже если narration соблюдает secrets, metadata/sidebar может сделать disclosure необратимым. **Вывод:** player-visible surface inventory должен включать entity lists, images, tool cards и navigation metadata.

## R48 — Convenience ownership позволяет leader/AI захватывать чужого PC без transition
**Тип:** NEGATIVE INTELLIGENCE. «Кто-то должен походить за отсутствующего» превращается в скрытую смену agency. **Вывод:** delegation/controller transfer — explicit, scoped и reversible policy.
---

# 5. Cross-cutting design questions for round two

## 5.1 Continuity ownership
- Какие виды continuity существуют и кто authoritative для каждого?
- Какие representations derived и могут быть rebuilt?
- Как предотвращается promotion hallucinated summary -> canon?
- Где проходит stability/consolidation boundary?

## 5.2 History / Retry / Branching
- Какие state domains обязаны двигаться вместе с history navigation?
- Какие canonical events допускают retry, а какие требуют нового semantic branch?
- Нужна ли явная history-node identity независимо от host UI?
- Как rejected sibling generations могут безопасно влиять на следующий retry?

## 5.3 Context allocation
- Какие semantic classes имеют hard minimum?
- Какие допускают downgrade/summary/omission?
- Что никогда нельзя trim частично?
- Как обеспечивается starvation protection?
- Как trace объясняет каждый inclusion/exclusion?

## 5.4 Actor continuity
- Какие actors заслуживают deep private continuity?
- Какие actor states transient, какие durable?
- Как actor-local beliefs не становятся world truth?
- Как защищается player agency?
- Как relationships/knowledge scopes выражаются без universal social/epistemic over-engineering?

## 5.5 Auxiliary orchestration
- Какие semantic decisions допустимо поручать LLM?
- Какие должны возвращать strictly typed proposal?
- Где обязательна deterministic validation?
- Как auxiliary calls rate-limit/cancel/retry?
- Какие calls можно defer при context pressure?

## 5.6 Long-range recall
- Что HDM обещает помнить exact, а что только семантически?
- Когда нужен global summary, episodic retrieval и exact archive?
- Нужен ли двухступенчатый retrieval?
- Как memory records теряют актуальность, объединяются и удаляются?

## 5.7 Extensibility
- Нужны ли plugins/scripts вообще в V1?
- Если да, какие capabilities и lifecycle phases?
- Как не допустить duplicate authority и callback soup?
- Какие extension artifacts должны участвовать в rollback/recovery?

## 5.8 Multiplayer / shared-world collaboration
- В какой момент output/action становится shared-established и перестаёт допускать silent local Retry/Edit?
- Как один architecture profile поддерживает synchronous и asynchronous play без universal round-robin?
- Какие collaboration state действительно нужны: readiness, handoff, last-consumed frontier, idle/delegation?
- Как split-party получает независимые scene/context/chronology frontiers и как они causal-reconcile?
- Какие interaction modes используют free-form input batching, а какие strict actor gate?
- Как authenticated participant identity связывается с controlled actor и как меняется controller ownership?
- Как строится recipient-specific context/disclosure поверх одного shared canon?
- Как отделяются OOC/social coordination, diegetic speech и actionable intent?
- Какая live currentness/synchronization primitive нужна при concurrent players на одном shared scope?
- Что означает join/rejoin посреди active scene/strict sequence?
- Нужен ли supported solo/shared fork и что именно он наследует?

---

# 6. Возможная группировка второго архитектурного раунда

Это **не новый roadmap**, а способ разложить добытые вопросы по связным блокам:

1. **Truth / Continuity / Memory Model** — D01, D05, D07, D08, D10, D11.
2. **History / Retry / Branch Semantics** — D06, D15, D20.
3. **Context Runtime / Retrieval / Observability** — D02, D03, D04, D14, D18, D19.
4. **Actor Agency / Cognition / Relationships** — D10–D13 и соответствующие STRONG candidates.
5. **Multiplayer / Shared World / Collaboration** — D20–D24 и multiplayer STRONG/NEGATIVE candidates.
6. **Semantic Mutation Boundary** — D09, D17.
7. **Physical LLM Orchestration / Auxiliary Work** — D16 и token/caching/rate-limit candidates.
8. **Narrative Planning / World Dynamics** — planning, pressures, timeskips, pacing.
9. **Extensibility / Tooling / Diagnostics** — capabilities, hooks, dry-run, repair.
10. **Holistic challenge / simplification pass** — проверить, какие идеи действительно оправдывают complexity.

---

# 7. Decision hygiene

Перед promotion любой DIAMOND/STRONG идеи в architecture отдельно проверить:

- какую конкретную HDM-проблему она решает;
- есть ли более простой вариант;
- создаёт ли duplicate authority;
- можно ли получить 80% эффекта без нового subsystem;
- как она ведёт себя при crash/retry/branch/multiplayer;
- меняется ли её rollback/edit semantics после того, как outcome становится observable другим participant;
- какое evidence является source of truth;
- что происходит при нехватке context;
- как наблюдать и тестировать failure;
- может ли она быть optional/profile capability вместо baseline requirement;
- какова стоимость отказа после начала реализации.

---
