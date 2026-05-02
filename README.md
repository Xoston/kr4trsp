# Контрольная работа: FastAPI, Alembic, обработка ошибок, тесты

## Установка

    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    pip install -r requirements.txt

## Миграции

    alembic upgrade head
    python seed.py
    alembic upgrade head

## Запуск

    uvicorn app.main:app --reload

## Тестирование

    pytest tests/test_main.py -v
    pytest tests/test_async.py -v
