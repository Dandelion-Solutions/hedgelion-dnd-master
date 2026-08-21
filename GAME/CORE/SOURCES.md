# Источники и происхождение принципов Framework

load_when: explicit source provenance/audit/research request or bounded preparation source audit
Этот файл предназначен для аудита и развития Framework. Он входит в локальный CORE cache, но во время обычной игры не должен активироваться как инструкция и не является списком страниц, которые Мастер обязан открывать в интернете.

Framework не является пересказом одной книги. Он разделяет три слоя: точные правила D&D, практику ведения настольных RPG и инженерные меры против типичных ошибок LLM.

## D&D 2024 / DMG / SRD

Механическая база: D&D 2024 (на D&D Beyond с 2026 года маркируется как 5.5e) / System Reference Document 5.2.1.

https://www.dndbeyond.com/srd
https://www.dndbeyond.com/sources/dnd/dmg-2024
https://www.dndbeyond.com/posts/1829-how-the-2024-dungeon-masters-guide-makes-it-easier
https://www.dndbeyond.com/posts/1850-creating-your-first-campaign-using-the-2024
https://www.dndbeyond.com/posts/1851-lets-prepare-an-adventure-using-the-2024-dungeon

Использованы общие мастерские принципы DMG 2024: роли DM, уважение и согласование ожиданий, подготовка и проведение сессии, recap, encounters, campaign journal, premise, Session 0, вовлечение персонажей/игроков, планирование приключений и кампаний. Точный защищённый текст DMG в репозиторий не копируется.

SRD 5.2.1 используется как открытая механическая база под CC BY 4.0; атрибуция хранится в `LICENSES/`.

## D&D Beyond — Session Zero, premise, tone и horror craft

Следующие материалы исследованы на этапе разработки движка и сведены в локальные `GM_CRAFT.md`, `CAMPAIGN_SETUP.md` и `SAFETY.md`. В игровом runtime Мастер НЕ должен открывать эти страницы заново ради общих советов по ведению.

https://www.dndbeyond.com/posts/929-how-to-run-a-session-0-for-your-d-d-game
https://www.dndbeyond.com/posts/728-new-players-guide-the-group-that-games-together
https://www.dndbeyond.com/posts/1372-running-a-session-zero-for-dragonlance-shadow-of
https://www.dndbeyond.com/posts/881-creating-terror-without-being-a-jerk
https://www.dndbeyond.com/posts/986-how-to-introduce-psychological-horror-in-your-next

Зафиксированная выжимка:
- Session Zero нужна для ожиданий, границ, character fit и важных правил, но может быть очень короткой; её допустимо повторять позже, если кампания или ожидания изменились;
- общий premise / flavor of fantasy / setting полезно обозначать, когда они уже известны, но не нужно раскрывать сюжетные повороты;
- character creation и фактическое поведение игроков дают Мастеру информацию о том, какие истории им интересны; не всё нужно выяснять анкетой заранее;
- жанры и тон могут смешиваться: тёмная драма и лёгкость не взаимоисключают друг друга, если один тон не разрушает эмоциональный момент другого;
- для кампании, построенной вокруг тяжёлых тем, игроку стоит заранее обозначить общий характер материала и спросить только реально нужные границы;
- horror не обязан быть непрерывной стеной напряжения: эпизоды levity могут помогать, но баланс зависит от конкретной группы и определяется практикой;
- если тон систематически не совпадает с ожиданиями, лучше коротко обсудить это вне игры, чем продолжать угадывать;
- из этих источников НЕ импортируется обязательный стиль юмора. Движок не предписывает чёрный, едкий, добродушный, абсурдный или иной «правильный» юмор; он только разрешает естественную ситуативную лёгкость там, где она не ломает установленный тон.

Практическое следствие для интерфейса Hedgelion: игроку предлагается возможность назвать жанр/настроение, но отсутствие предпочтения является полноценным ответом. Мастер не обязан задавать отдельные вопросы `какой жанр?`, `сколько юмора?`, `насколько серьёзно?`, если они не нужны для ближайшего решения.

## D&D Beyond — improvisation, encounters, worldbuilding и closure

Следующие материалы также были просмотрены именно как GM-craft источники и переведены в локальные правила, пригодные для AI Master. Они не являются runtime-зависимостью.

https://www.dndbeyond.com/posts/160-improvisation-in-d-d-for-new-dungeon-masters
https://www.dndbeyond.com/posts/769-worldbuilding-through-encounters
https://www.dndbeyond.com/posts/1829-how-the-2024-dungeon-masters-guide-makes-it-easier
https://www.dndbeyond.com/posts/1850-creating-your-first-campaign-using-the-2024

Зафиксированная выжимка:
- базовый ритм игры — Мастер даёт ситуацию, игрок заявляет действие/намерение, правила и fiction разрешают его, затем игрок получает изменившуюся ситуацию для следующего решения;
- неожиданное действие игрока не следует возвращать на заранее подготовленный маршрут только потому, что Мастер ожидал другого;
- `yes, and` / `no, but` полезны как инструменты импровизации, но не отменяют невозможность, правила или объективную правду мира;
- worldbuilding лучше запоминается, когда проявляется через encounters, людей, места, обычаи, последствия и конкретные детали, а не только через энциклопедическую экспозицию;
- encounters не сводятся к бою: социальные, исследовательские, переговорные и иные пространства решений полноценны сами по себе;
- campaign journal может помогать замечать, что оказалось значимым для игроков, но наблюдение не равно автоматически устойчивому предпочтению;
- завершение кампании является нормальной частью campaign craft: разрешённый центральный конфликт не обязан немедленно заменяться новым, а удовлетворительный финал лучше искусственного бесконечного продолжения.

AI-адаптация этих рекомендаций:
- модель склонна автодополнять вероятное продолжение, поэтому локальный `NARRATIVE.md` запрещает перескакивать через новые значимые решения PC;
- модель склонна соглашаться с формулировкой пользователя, поэтому `GM_CRAFT.md` + `AI_REASONING.md` отделяют цель действия от встроенных в фразу предположений о мире;
- модель способна бесконечно генерировать lore/hooks, поэтому богатство генерации не считается основанием для расширения мира или нового конфликта;
- один удачный тон/персонаж/шутка — слабый сигнал, а не автоматическая долговременная настройка;
- завершение истории не трактуется как нехватка контента: `CAMPAIGN_OPERATIONS.md` разрешает активной кампании иметь спокойный aftermath и допускает настоящее завершение без обязательного sequel hook.

## Justin Alexander / The Alexandrian

https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots
https://thealexandrian.net/wordpress/1101/roleplaying-games/three-clue-rule-part-3-the-three-clue-rule
https://thealexandrian.net/wordpress/7949/roleplaying-games/node-based-scenario-design-part-1-the-plotted-approach
https://thealexandrian.net/wordpress/39885/roleplaying-games/smart-prep
https://thealexandrian.net/wordpress/39893/roleplaying-games/smart-prep-part-2-the-principles-of-smart-prep
https://thealexandrian.net/wordpress/43714/roleplaying-games/smart-prep-the-exposition-drip

Использованные идеи:
- готовить ситуации, а не обязательный plot;
- избегать chokepoints;
- redundant clues / Three Clue Rule для важных выводов;
- node-based структура сложных сценариев;
- smart prep: тратить подготовку на то, что действительно выигрывает от предварительной работы;
- exposition drip: сложный lore лучше раскрывать небольшими связанными фрагментами.

## Sly Flourish / Lazy GM

https://slyflourish.com/eight_steps_2023.html
https://slyflourish.com/using_the_8_steps_at_the_table.html
https://slyflourish.com/revealing_secrets.html
https://slyflourish.com/spiral_campaign_building.html
https://slyflourish.com/thinking_two_horizons_out.html
https://slyflourish.com/bathe_your_world_in_lore.html
https://slyflourish.com/prepping_and_running_lazy_campaigns.html
https://slyflourish.com/lazy_gm_resource_document.html

Использованные идеи:
- review characters, strong start, potential scenes, secrets/clues, locations, NPCs, threats and rewards как набор инструментов подготовки;
- secrets/clues — короткие релевантные факты, не обязательно привязанные заранее к единственному месту обнаружения;
- spiral campaign development: строить мир от текущего положения персонажей наружу;
- думать на один-два горизонта вперёд, не генерируя энциклопедию;
- lore должен делать мир отличимым, но раскрываться через игру;
- Session 0 и компактный campaign guide помогают согласовать premise, связи персонажей и ожидания.

## Dungeon World SRD — только как межсистемная школа GM craft

https://www.dwsrd.org/gm/

Это НЕ источник правил D&D. Отсюда заимствованы только совместимые общие идеи мастерства: мир в движении, NPC/угрозы со своими целями, последствия должны следовать из fiction, думать об off-screen процессах и не защищать заранее написанную историю. Формулировка "play to find out" используется как принцип неопределённости исхода, но механика Dungeon World в D&D не импортируется.

## Исследования LLM и RPG

Callison-Burch et al., EMNLP 2022, "Dungeons and Dragons as a Dialog Challenge for Artificial Intelligence":
https://aclanthology.org/2022.emnlp-main.637/

Zhu et al., ACL 2023, "FIREBALL: A Dataset of Dungeons and Dragons Actual-Play with Structured Game State Information":
https://aclanthology.org/2023.acl-long.229/

Zhu et al. 2023, "CALYPSO: LLMs as Dungeon Masters' Assistants":
https://arxiv.org/abs/2308.07540

Вывод для архитектуры: структурированное состояние и маленькие релевантные порции контекста надёжнее, чем попытка восстанавливать мир только из длинной истории диалога.

Qi et al., ACL 2026, "Beyond Static Persona Consistency: Dynamic Persona Coherence in LLM Role-Playing":
https://aclanthology.org/2026.acl-long.1336/

Wang et al., Findings ACL 2026, "Memory-Driven Role-Playing":
https://aclanthology.org/2026.findings-acl.1175/

Использованный вывод: устойчивую идентичность персонажа следует отделять от изменяемого ситуативного/психологического состояния; explicit retrieval уменьшает долгосрочный drift.

Hong et al., Findings EMNLP 2025, "Measuring Sycophancy of Language Models in Multi-turn Dialogues":
https://aclanthology.org/2025.findings-emnlp.121/

Ranaldi & Pucci, EACL 2026, "Learning Multilingual Agentic Policy to Control Sycophancy":
https://aclanthology.org/2026.eacl-long.169/

Shah et al., ACL 2026, "Too Nice to Tell the Truth: Quantifying Agreeableness-Driven Sycophancy in Role-Playing Language Models":
https://aclanthology.org/2026.acl-long.1421/

Использованный вывод: согласительность/угодливость LLM является реальным failure mode, особенно опасным для DM, потому что может превращать предложение игрока в факт мира или менять adjudication под давление пользователя. Поэтому `AI_REASONING.md` явно отделяет user preference от truth/rules.

Ma et al. 2026, "Can LLM Agents Stick to the Script? A Benchmark for Long-Horizon Consistency in Interactive Narratives":
https://arxiv.org/abs/2608.08160

Работа используется как дополнительное подтверждение проблемы long-horizon commitment preservation: качественная проза сама по себе не гарантирует сохранность ранее установленных фактов.

## Архитектурные решения Hedgelion

Следующие решения являются инженерными решениями этого Framework, а не правилами D&D:
- GitHub как canonical persistent store;
- `main` как engine и отдельные `campaign/*` branches;
- lazy loading через stable IDs и индексы;
- hot state отдельно от WORLD/LOG;
- batching вместо commit-per-turn;
- optimistic concurrency и semantic conflict resolution в multiplayer;
- запрет ChatGPT Memory для игрового канона;
- STATE -> INTENT -> RULES -> RANDOMNESS -> CONSEQUENCES -> PERSISTENCE -> NARRATION;
- обязательный `AI_REASONING.md` как защитный слой между состоянием и прозой.

Все эти решения должны пересматриваться по результатам реальной игры и regression-тестов.
