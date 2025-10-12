## 📋 Системные требования

- **Python** ≥ 3.13.8 (желательно)
- **Docker**

## ⚙️ Настройка окружения

Создайте файл `.env` в корне проекта по образцу `example.env` и настройте переменные по сценарию:

### 🎯 Переменные для разных сценариев

| Сценарий | API_HOST | API_PORT | DB_HOST | DB_PORT |
|----------|----------|----------|---------|---------|
| 🔴 **API (локально)** | `localhost` | `8000` | `localhost` | `54321` |
| 🟢 **Всё приложение** | `backend` | `5000` | `db` | `5432` |

## 🚀 Запуск приложения

Перед запуском приложения локально создайте и активируйте виртуальное окружение и установите зависимости:
```sh
pip install -r requirements.txt
```

### 🔴 Запуск API
```sh
# Запуск базы данных
docker compose -f infra.yml up -d

# Запуск API
cd backend
alembic upgrade head
uvicorn src.entrypoints.fastapi_app.main:app --reload
```

### 🤖 Запуск бота
```bash
cd bot
python -m src.bot
```

### 🟢 Запуск всего приложения
```sh
docker compose up
```

### 🌐 Доступ к сервисам
После успешного запуска:

- 📚 Документация API → http://127.0.0.1:8000/docs

- 🗄️ Панель управления БД (PGAdmin) → http://127.0.0.1:8080 (для API)

### 🧪 Тестирование
Для запуска тестов выполните следующие команды:
```sh
cd backend

# Запуск тестовой базы данных
docker run -p 54321:5432 \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_USER=test \
  -e POSTGRES_DB=test \
  -d postgres

# Запуск тестов
pytest
```