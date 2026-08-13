# Источники и происхождение принципов Framework

Этот файл предназначен для аудита и развития Framework. Во время обычной игры его загружать не требуется.

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
