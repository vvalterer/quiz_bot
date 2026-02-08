# 🤖 Вячеслав Ветошкин — Lead Quiz Bot

Создан под бренд Вячеслав Ветошкин (https://1vetoshkin.ru)  
Контакт: [Telegram](https://t.me/TkAs007bot)

## 🚀 Быстрый запуск
1) Создайте файл `.env` из `.env.example`, вставьте `BOT_TOKEN` и `ADMIN_IDS` (через запятую).
2) Локально:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python app/main.py
   ```
3) Через Docker:
   ```bash
   docker-compose up -d --build
   ```

## 📦 Структура
```
app/
  main.py
  handlers/
  keyboards/
  services/
  database/
.env.example
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

## 🧩 Настройки (.env)
```ini
BOT_TOKEN=
ADMIN_IDS=123456789,987654321
DB_PATH=data/database.sqlite3
LOG_LEVEL=INFO
```

## ✅ Готово!
Бот запускается, команда /start работает. Функции ниши — в `app/handlers/feature.py`.
