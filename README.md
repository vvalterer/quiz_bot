# 🤖 Lead Quiz Bot

[![Tests](https://github.com/vvalterer/quiz_bot/actions/workflows/tests.yml/badge.svg)](https://github.com/vvalterer/quiz_bot/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![aiogram 3.x](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://docs.aiogram.dev/)

Создан под бренд Вячеслав Ветошкин (https://1vetoshkin.ru)  
Контакт: [Telegram](https://t.me/TkAs007bot)

Telegram бот для сбора лидов через квиз из 7 вопросов с уведомлением администратора.

## ✨ Возможности

- 📝 Квиз из 7 настраиваемых вопросов
- 💾 Сохранение ответов в SQLite
- 📬 Уведомление администраторов о новых лидах
- ❌ Отмена квиза командой `/cancel`
- 🐳 Docker-ready

## 🚀 Быстрый старт

### Локально

```bash
# Клонировать репозиторий
git clone https://github.com/vvalterer/quiz_bot.git
cd quiz_bot

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или .venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_IDS в .env

# Запустить
python -m app.main
```

### Docker

```bash
cp .env.example .env
# Заполнить BOT_TOKEN и ADMIN_IDS
docker-compose up -d --build
```

## ⚙️ Настройка (.env)

| Переменная | Описание | Пример |
|------------|----------|--------|
| `BOT_TOKEN` | Токен от @BotFather | `123456:ABC-DEF...` |
| `ADMIN_IDS` | ID администраторов (через запятую) | `123456789,987654321` |
| `DB_PATH` | Путь к базе данных | `data/database.sqlite3` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

## 📁 Структура проекта

```
quiz_bot/
├── app/
│   ├── main.py           # Точка входа
│   ├── database.py       # Работа с SQLite
│   └── handlers/
│       └── feature.py    # Логика квиза (FSM)
├── tests/                # Тесты
├── .env.example          # Пример переменных
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🧪 Тесты

```bash
pip install pytest pytest-asyncio
pytest -v
```

## 📋 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Запуск бота |
| `/help` | Список команд |
| `/quiz` | Начать квиз |
| `/cancel` | Отменить квиз |

## 📝 Лицензия

© 2025 Вячеслав Ветошкин. Single Use License.
