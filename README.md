### Для запуска локально
- Запустите базу данных при помощи скрипта `start-db-dev.sh`
- В файле `.env` напишите `DB_HOST=localhost` и `DB_PORT=54321`
- Выполните команду `uvicorn src.entrypoints.fastapi_app.main:app --reload`

### Для запуска в контейнере
- В файле `.env` напишите `DB_HOST=db` и `DB_PORT=5432`
- Выполните команду `docker compose up`