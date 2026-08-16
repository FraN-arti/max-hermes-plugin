# Changelog

Все заметные изменения проекта — в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
проект придерживается [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Планируется (v1.1)

- Групповые чаты и @упоминания ([#2](https://github.com/FraN-arti/max-hermes-plugin/issues/2))
- Webhook-режим для production ([#3](https://github.com/FraN-arti/max-hermes-plugin/issues/3))
- CI: GitHub Actions — автотесты и линтер ([#4](https://github.com/FraN-arti/max-hermes-plugin/issues/4))

## [0.20.0] — 2026-08-16

### Добавлено

- **Вложения**: приём и отправка изображений, файлов, видео, аудио через
  `POST /uploads` + CDN. Токен извлекается из ответа на загрузку
  (для image — из `photos` map). CDN-загрузка использует обычный CA,
  не сертификат Минцифры. ([#1](https://github.com/FraN-arti/max-hermes-plugin/issues/1))
- **Парсер входящих**: распознаёт вложения и описывает их
  (`[Фото]`, `[Видео]`, `[Файл]`); скачивает входящие изображения в кэш.
- **`send_document` / `send_image_file` / `send_image`** — переопределяют
  базовый fallback, реально доставляют файлы в MAX.
- **Typing indicator**: «печатает…» через `POST /chats/{id}/actions` (`typing_on`).
- **Маркер персистится** в `max/marker.json` — нет повторов после рестарта.
- **Умный сплит** длинных сообщений (>4000) на несколько, с учётом rate limit.
- **Автоскачивание Russian Trusted Root CA** с таймаутом 10с и проверкой PEM.
- **Backoff с jitter**, rate limit (2 msg/сек), health-поля
  (`last_poll_at`, `last_poll_error`).

### Исправлено

- Дедупликация: записи старше окна вычищаются при каждом вызове.
- Обрезка длинных сообщений: вместо молчаливой — умный сплит + заметка.

### Изменено

- Версия выровнена с Hermes (0.20.0).
- README двуязычный (RU/EN), добавлены шаблоны issues, CONTRIBUTING.md.

[0.20.0]: https://github.com/FraN-arti/max-hermes-plugin/releases/tag/0.20.0