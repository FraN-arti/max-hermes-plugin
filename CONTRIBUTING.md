# Contributing to max-hermes-plugin

Спасибо, что хочешь помочь проекту! 🚀 Это займёт 5 минут.

## Как помочь

### 🐛 Нашёл баг?
Создай [issue](https://github.com/FraN-arti/max-hermes-plugin/issues/new?template=bug_report.md) — опиши шаги, окружение, логи.

### ✨ Хочешь фичу?
Создай [issue](https://github.com/FraN-arti/max-hermes-plugin/issues/new?template=feature_request.md) — что решает, как видишь решение.

### 💻 Хочешь написать код?

1. **Форкни** репозиторий
2. Создай ветку: `git checkout -b feat/your-feature`
3. Меняй код (не забудь тесты!)
4. Запусти тесты:
   ```bash
   # Тесты плагина требуют окружение Hermes (gateway.* модули).
   # Проще всего: скопировать плагин в HERMES_HOME и запустить оттуда:
   # python -m pytest tests/gateway/test_max_plugin.py -q
   ```
5. Коммит по [Conventional Commits](https://www.conventionalcommits.org/): `feat: ...`, `fix: ...`, `docs: ...`
6. Открой PR

## Стиль

- Python 3.11+, типизация (typing)
- HTTP-клиент — httpx (async), как в adapter.py
- Не ломай обратную совместимость: env-переменные `MAX_*` остаются
- При добавлении фичи — обнови README.md и README.en.md

## Структура

```
plugins/platforms/max/
├── __init__.py      # регистрация плагина
├── adapter.py       # Long Polling + отправка + авто-сертификат + typing
├── plugin.yaml      # метаданные для hermes setup gateway
├── README.md        # RU
└── README.en.md     # EN
```

## Тесты

- `tests/gateway/test_max_plugin.py` — 31+ тестов (парсинг, dedup, send, standalone, register)
- Новые фичи — покрывай тестами (моки httpx, без реальных запросов к MAX)

## Лицензия

[MIT](LICENSE) — внося код, ты соглашаешься на MIT.